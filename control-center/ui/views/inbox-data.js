// The one aggregation in the app: every pending decision across departments,
// as a flat, prioritised list. Used by the Inbox view (to draw it) and by the
// shell (to badge the rail). It reads only what this account may see, and it
// reads each department through the same endpoint the department's own view
// uses, so the two can never disagree.
import { api, canSee, prefs, setCount, setAgent, daysAgo, dueLabel } from '../core.js';
import { inFlight, passStale } from './cards.js';

export const KIND = {
  'eng-gate':   { dept: 'eng', label: 'Engineering', rank: 3 },
  'eng-merge':  { dept: 'eng', label: 'Engineering', rank: 0 },
  'eng-blocked':{ dept: 'eng', label: 'Engineering', rank: 1 },
  'mkt-due':    { dept: 'marketing', label: 'Marketing', rank: 2 },
  'reddit':     { dept: 'marketing', label: 'Reddit', rank: 4 },
  'sms-review': { dept: 'marketing', label: 'SMS', rank: 5 },
  'sms-draft':  { dept: 'marketing', label: 'SMS', rank: 6 },
  'sms-send':   { dept: 'marketing', label: 'SMS', rank: 6 },
  'sales-follow':{ dept: 'sales', label: 'Sales', rank: 7 },
};

export async function gather() {
  const out = { items: [], errors: [], eng: null, mkt: null, sms: null, sales: null, reddit: null, motion: { deciding: [], queued: [], submitted: [], building: [] } };
  const jobs = [];
  if (canSee('eng')) jobs.push(api.get('/api/engineering', { instance: prefs.get('eng-instance') }).then(d => { out.eng = d; }).catch(e => out.errors.push(['Engineering', e])));
  if (canSee('marketing')) {
    jobs.push(api.get('/api/marketing', { instance: prefs.get('mkt-instance') }).then(d => { out.mkt = d; }).catch(e => out.errors.push(['Marketing', e])));
    jobs.push(api.get('/api/reddit', { status: 'PENDING' }).then(d => { out.reddit = d; }).catch(e => { out.reddit = { items: [], error: e }; }));
    jobs.push(api.get('/api/sms', { instance: prefs.get('mkt-instance') }).then(d => { out.sms = d; }).catch(e => { out.sms = null; }));
  }
  if (canSee('sales')) jobs.push(api.get('/api/sales', { instance: prefs.get('sales-instance') }).then(d => { out.sales = d; }).catch(e => out.errors.push(['Sales', e])));
  await Promise.all(jobs);

  const items = out.items;
  const eng = out.eng;
  if (eng && eng.instance) {
    (eng.waiting || []).forEach(w => items.push({ kind: w.gate === 'merge' ? 'eng-merge' : 'eng-gate', id: 'eng:' + w.file, age: ageOf(w.raised), data: w, instance: eng.instance }));
    (eng.blocked_on_harry || []).forEach(t => items.push({ kind: 'eng-blocked', id: 'engb:' + t.id, age: ageOf(t.updated), data: t, instance: eng.instance }));
    out.motion.deciding = eng.deciding || [];
    out.motion.submitted = eng.submitted || [];
    out.motion.building = (eng.by_state && eng.by_state.building) || [];
    const h = !eng.activity.running && inFlight(eng)[0];
    setAgent(eng.activity, h ? { id: h[1].id, word: h[0] === 'ready' ? 'ready to start' : h[0].replace(/-/g, ' '), stale: passStale(eng.activity) } : null);
  }
  const mkt = out.mkt;
  if (mkt && !mkt.empty) {
    (mkt.due || []).forEach(p => items.push({ kind: 'mkt-due', id: 'mkt:' + p.path, due: p.date, age: 0, data: p, instance: mkt.instance, channels: mkt.channels, today: mkt.today }));
    out.motion.queued = mkt.queued || [];
  }
  if (out.reddit && out.reddit.items) out.reddit.items.forEach(it => items.push({ kind: 'reddit', id: 'rd:' + it.id, age: 0, data: it }));
  const sms = out.sms;
  if (sms && !sms.empty) {
    (sms.campaigns || []).forEach(c => {
      if (c.status === 'draft') items.push({ kind: 'sms-draft', id: 'smsc:' + c.id, age: ageOf(c.created_at), data: c, sms });
      if (c.status === 'approved') items.push({ kind: 'sms-send', id: 'smsc:' + c.id, age: ageOf(c.created_at), data: c, sms });
    });
    (sms.reactivations || []).forEach(r => {
      const pending = (r.messages || []).filter(m => (m.state || (m.sent ? 'sent' : 'failed')) === 'pending');
      if (pending.length) items.push({ kind: 'sms-review', id: 'smsr:' + r.id, age: ageOf(r.created_at), data: r, pending, sms });
    });
  }
  const sales = out.sales;
  if (sales && !sales.empty) {
    (sales.stages || []).filter(s => !s.name.startsWith('7-')).forEach(s => (s.leads || []).forEach(l => {
      const stale = l.days_since_touch != null && l.days_since_touch >= 7;
      if (l.action_overdue || stale) items.push({ kind: 'sales-follow', id: 'lead:' + l.slug, age: l.days_since_touch || 0, data: l, stage: s.name, instance: sales.instance });
    }));
  }
  // Rank, then within a rank: marketing by planned date (late first), the rest oldest first.
  items.sort((a, b) => {
    const ra = KIND[a.kind].rank, rb = KIND[b.kind].rank;
    if (ra !== rb) return ra - rb;
    if (a.kind === 'mkt-due') return String(a.due || '').localeCompare(String(b.due || ''));
    return (b.age || 0) - (a.age || 0);
  });
  return out;
}

function ageOf(iso) { const d = daysAgo(iso); return d == null ? 0 : d; }

export function countsByView(items) {
  const c = { inbox: items.length, marketing: 0, sales: 0, eng: 0 };
  items.forEach(i => { const d = KIND[i.kind].dept; c[d] = (c[d] || 0) + 1; });
  return c;
}

let sweeping = false;
export async function sweep() {
  if (sweeping) return;
  sweeping = true;
  try {
    const out = await gather();
    const c = countsByView(out.items);
    Object.entries(c).forEach(([k, v]) => setCount(k, v));
    window.dispatchEvent(new CustomEvent('cc:swept', { detail: out }));
    return out;
  } catch (e) { /* the view that failed will say so itself */ }
  finally { sweeping = false; }
}
