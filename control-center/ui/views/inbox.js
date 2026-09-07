// Inbox — the home screen. One list of everything waiting on a human, across
// every department this account can see, most blocking first. Approve, hold,
// skip inline; drill into a department only when you want its context.
import { setTop, refreshBtn, chips, empty, skeleton, esc, attr, icon, todayLabel, setViewKeys, setPaletteCommands, navigate, plural, makePoller, errorBox, relTime, canSee } from '../core.js';
import { gather, countsByView, KIND } from './inbox-data.js';
import { engGateCard, engBlockedCard, mktPieceCard, redditCard, smsCampaignCard, smsRunCard, leadFollowCard, activityCard, bindActions, afterRender, captureInputs, restoreInputs, GATE_LABEL, shortCtx } from './cards.js';

let root, data = null, filter = 'all', focus = -1, poller = null, loading = false, lastSig = '';

function itemHtml(it) {
  switch (it.kind) {
    case 'eng-gate': case 'eng-merge': return engGateCard(it.data, { instance: it.instance, inbox: true });
    case 'eng-blocked': return engBlockedCard(it.data, { inbox: true });
    case 'mkt-due': return mktPieceCard(it.data, { gate: true, body: true, inbox: true, instance: it.instance, channels: it.channels, today: it.today, meta: 'nothing publishes without this' });
    case 'reddit': return redditCard(it.data, { inbox: true });
    case 'sms-draft': case 'sms-send': return smsCampaignCard(it.data, it.sms, { inbox: true });
    case 'sms-review': return smsRunCard(it.data, it.sms, { inbox: true });
    case 'sales-follow': return leadFollowCard(it);
  }
  return '';
}

function motionHtml(m, eng) {
  const rows = [];
  (m.building || []).forEach(t => rows.push(`<div class="queue-row"><span class="tag tag-live">building</span><span class="num dim">${esc(t.id)}</span><span>${esc(t.title)}</span></div>`));
  (m.deciding || []).forEach(w => rows.push(`<div class="queue-row"><span class="tag">${esc(GATE_LABEL[w.gate] || w.gate || 'decision')}</span><span class="num dim">${esc(w.ticket)}</span><span>you said <b>${esc(w.decision)}</b> ${esc(relTime(w.decided))} — applying</span></div>`));
  (m.queued || []).slice(0, 6).forEach(p => rows.push(`<div class="queue-row"><span class="tag">${esc(p.channel || 'piece')}</span><span>${esc(p.title)}</span><span class="dim">ships on its next slot</span></div>`));
  (m.submitted || []).forEach(s => rows.push(`<div class="queue-row"><span class="tag">intake</span><span>${esc(s.title)}</span><span class="dim">the PM shapes this next pass</span></div>`));
  if (!rows.length) return '';
  return `<section class="section"><div class="section-h"><h2>In motion</h2><span class="n">${rows.length}</span><span class="right"><button class="btn btn-ghost btn-sm" data-act="go" data-to="eng/board">Board ${icon('chevronRight', 'ic-sm')}</button></span></div>
    <div class="card" style="padding:12px 16px"><div class="queue" style="gap:8px">${rows.join('')}</div></div></section>`;
}

function render() {
  const el = root.querySelector('#inbox'); if (!el) return;
  if (!data) { el.innerHTML = `<div class="inbox-hero"><div><h1>Inbox</h1><p>${esc(todayLabel())}</p></div></div>${skeleton(3)}`; return; }
  const items = data.items;
  const counts = countsByView(items);
  const shown = items.filter(i => filter === 'all' || KIND[i.kind].dept === filter);
  const n = items.length;
  const depts = [{ id: 'all', label: 'All', n }];
  if (canSee('eng')) depts.push({ id: 'eng', label: 'Engineering', n: counts.eng || 0, hot: !!counts.eng });
  if (canSee('marketing')) depts.push({ id: 'marketing', label: 'Marketing', n: counts.marketing || 0, hot: !!counts.marketing });
  if (canSee('sales')) depts.push({ id: 'sales', label: 'Sales', n: counts.sales || 0, hot: !!counts.sales });
  const errs = (data.errors || []).map(([what, e]) => errorBox(e, what)).join('');
  let h = `<div class="inbox-hero"><div>
      <h1>${n ? `<span class="n">${n}</span> ${n === 1 ? 'thing needs' : 'things need'} you` : 'Nothing needs you'}</h1>
      <p>${esc(todayLabel())}${n ? ' · most blocking first' : ' · the departments are either working or idle, and both are fine'}</p>
    </div></div>`;
  h += errs;
  if (n) h += `<div class="inbox-summary">${chips(depts, filter, 'dept')}</div>`;
  h += `<div class="stack" id="items">${shown.map(itemHtml).join('')}</div>`;
  if (n && !shown.length) h += empty('Nothing here for this filter', '', 'inbox', true);
  if (!n) h += `<div class="empty">${icon('check')}<div><b>All clear</b><p>Anything written and dated further out waits under its department until it comes due.</p></div></div>`;
  h += motionHtml(data.motion, data.eng);
  if (data.eng && data.eng.activity) h += `<section class="section"><div class="section-h"><h2>Right now</h2><span class="right"><button class="btn btn-ghost btn-sm" data-act="go" data-to="eng">Engineering ${icon('chevronRight', 'ic-sm')}</button></span></div><div data-activity>${activityCard(data.eng.activity)}</div></section>`;
  if (n) h += `<div class="hint-bar"><span><span class="kbd">J</span><span class="kbd">K</span> move</span><span><span class="kbd">A</span> approve</span><span><span class="kbd">C</span> changes</span><span><span class="kbd">X</span> reject</span><span><span class="kbd">Enter</span> expand</span><span><span class="kbd">N</span> note</span><span><span class="kbd">?</span> all shortcuts</span></div>`;
  const kept = captureInputs(el);
  el.innerHTML = h;
  restoreInputs(el, kept);
  afterRender(el);
  el.querySelectorAll('[data-chip]').forEach(c => c.onclick = () => { filter = c.dataset.chip; focus = -1; render(); });
  setFocus(focus, false);
}

const itemEls = () => Array.from(root.querySelectorAll('#items .item'));
function setFocus(i, scroll = true) {
  const els = itemEls();
  els.forEach(e => e.classList.remove('focused'));
  if (i < 0 || i >= els.length) { focus = -1; return; }
  focus = i;
  els[i].classList.add('focused');
  if (scroll) els[i].scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}
function focused() { const els = itemEls(); return focus >= 0 ? els[focus] : null; }
function pressKey(k) { const f = focused(); if (!f) return; const b = f.querySelector(`[data-key="${k}"]`); if (b) b.click(); }

// Polls re-fetch everything, but only re-draw the list when something other
// than the live activity changed — so an opened card, a half-typed note and
// the keyboard focus all survive. Dim only if the refresh is actually slow.
async function load(quiet = false) {
  if (loading) return; loading = true;
  const el = root.querySelector('#inbox'); if (!el) { loading = false; return; }
  const dim = quiet ? setTimeout(() => el.classList.add('refreshing'), 400) : null;
  try {
    const next = await gather();
    const sig = JSON.stringify({ items: next.items, motion: next.motion, errors: (next.errors || []).map(([w, e]) => [w, String(e && e.message || e)]) });
    const same = quiet && !!data && sig === lastSig;
    data = next; lastSig = sig;
    if (same) { const a = el.querySelector('[data-activity]'); if (a && data.eng && data.eng.activity) a.innerHTML = activityCard(data.eng.activity); }
    else render();
  }
  catch (e) { data = { items: [], errors: [['the inbox', e]], motion: {} }; lastSig = ''; render(); }
  finally { loading = false; clearTimeout(dim); el.classList.remove('refreshing'); }
}

export default {
  id: 'inbox', title: 'Inbox', short: 'Inbox', icon: 'inbox', hot: true, section: 'main',
  async mount(r) {
    root = r; data = null; focus = -1; lastSig = '';
    root.innerHTML = `<div class="content-inner" id="inbox"></div>`;
    setTop({ title: 'Inbox', right: refreshBtn() });
    document.querySelector('[data-refresh]').onclick = () => load(true);
    bindActions(root, () => load(true));
    // Clicking anywhere on an item makes it the keyboard-focused one, so a
    // mouse user can pick up with J/K/A from wherever they are.
    root.addEventListener('mousedown', e => { const it = e.target.closest('#items .item'); if (it) setFocus(itemEls().indexOf(it), false); });
    render();
    await load();
    poller = makePoller(() => load(true), 15000); poller.start();
    setViewKeys({
      j: () => setFocus(Math.min(focus + 1, itemEls().length - 1)), k: () => setFocus(Math.max(focus - 1, 0)),
      a: () => pressKey('a'), c: () => pressKey('c'), x: () => pressKey('x'),
      Enter: () => { const f = focused(); if (!f) return; const m = f.querySelector('[data-more]'); if (m) m.click(); else pressKey('enter'); },
      n: () => { const f = focused(); const t = f && f.querySelector('[data-note], textarea'); if (t) { t.focus(); } },
      r: () => load(true),
    });
    setPaletteCommands(() => (data ? data.items : []).slice(0, 30).map((it, i) => ({
      group: 'Needs you', icon: 'inbox', label: it.data.ticket ? `${it.data.ticket} — ${GATE_LABEL[it.data.gate] || it.data.gate || ''}` : (it.data.title || it.data.name || it.data.contact || it.id),
      run: () => { filter = 'all'; render(); setFocus(i); },
    })));
    this._refresh = () => load(true);
    window.addEventListener('cc:refresh', this._refresh);
  },
  unmount() { poller && poller.stop(); window.removeEventListener('cc:refresh', this._refresh); },
};
