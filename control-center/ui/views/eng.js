// Engineering — the board, per business instance. Decide is the gate; Board
// is the state of play; Bugs is the open list. Polls while open so "Right
// now" stays current.
import { api, setTop, seg, selectHtml, refreshBtn, esc, attr, icon, empty, skeleton, prefs, navigate, parseRoute, toast, fail, relTime, setViewKeys, makePoller, errorBox, plural, setAgent, setPaletteCommands } from '../core.js';
import { engGateCard, engBlockedCard, engDecidingCard, activityCard, bindActions, afterRender, tag, GATE_LABEL } from './cards.js';
import { eventVerb } from '../core.js';

const WORKING = ['ready', 'building', 'in-review', 'in-qa', 'in-security', 'ready-to-ship'];
const GROUPS = [
  ['To-do', ['intake', 'shaped', 'awaiting-scope']],
  ['In progress', ['designed', 'awaiting-decision', 'ready', 'building', 'in-review', 'in-qa', 'in-security']],
  ['Ready to ship', ['ready-to-ship', 'awaiting-release']],
  ['Done', ['shipped', 'verified', 'advised']],
  ['Blocked', ['blocked']],
  ['Dropped', ['dropped']],
];
const WAITING_ON_YOU = ['awaiting-scope', 'awaiting-decision', 'awaiting-release'];
const PRIO_RANK = { now: 0, next: 1, '': 2, hold: 3 };

let root, data = null, sub = 'decide', instance = prefs.get('eng-instance', ''), poller = null;
let showDropped = prefs.get('eng-dropped') === '1', waitingFilter = prefs.get('eng-waiting', 'all'), loading = false;

function top() {
  const insts = (data && data.instances) || [];
  const waiting = data ? (data.waiting || []).length + (data.blocked_on_harry || []).length : null;
  const s = seg([{ id: 'decide', label: 'Decide', n: waiting, hot: !!waiting }, { id: 'board', label: 'Board' }, { id: 'bugs', label: 'Bugs', n: data ? (data.bugs || []).length : null }], sub);
  setTop({ title: 'Engineering', sub: s, right: (insts.length > 1 ? selectHtml('eng-inst', insts, instance) : '') + refreshBtn() });
  document.querySelectorAll('[data-seg]').forEach(b => b.onclick = () => navigate('eng/' + b.dataset.seg));
  const sel = document.getElementById('eng-inst'); if (sel) sel.onchange = () => { instance = sel.value; prefs.set('eng-instance', instance); data = null; render(); load(); };
  document.querySelector('[data-refresh]').onclick = () => load(true);
}

function statsHtml(s) {
  return `<div class="stats">
    <div class="stat ${s.waiting_on_harry ? 'hot' : ''}"><b>${s.waiting_on_harry}</b><span>waiting on you</span></div>
    <div class="stat"><b>${s.in_flight}<small>/${s.machine_limit}</small></b><span>in flight</span></div>
    <div class="stat"><b>${s.pending_apply}</b><span>pending apply</span></div>
    <div class="stat ${s.open_bugs ? 'bad' : ''}"><b>${s.open_bugs}</b><span>open bugs</span></div>
    <div class="stat"><b>${s.shipped_recent}</b><span>verified</span></div>
  </div>`;
}

function decideHtml(d) {
  const blocked = d.blocked_on_harry || [];
  const total = d.waiting.length + blocked.length;
  const gateCount = g => d.waiting.filter(w => w.gate === g).length;
  let h = `<section class="section"><div class="section-h"><h2>Waiting on you</h2><span class="n ${total ? 'hot' : ''}">${total}</span>
    ${total ? `<span class="right"><div class="chips">${[['all', 'All', total], ['merge', 'Merge', gateCount('merge')], ['scope', 'Scope', gateCount('scope')]]
      .map(([v, l, n]) => `<button class="chip ${waitingFilter === v ? 'on' : ''}" data-wf="${v}">${l}<span class="n">${n}</span></button>`).join('')}</div></span>` : ''}</div>`;
  const showBlocked = waitingFilter === 'all';
  const shown = d.waiting.filter(w => waitingFilter === 'all' || w.gate === waitingFilter);
  if (!shown.length && !(showBlocked && blocked.length)) {
    h += total ? empty('Nothing waiting on you matches this filter', '', 'inbox', true)
               : `<div class="empty">${icon('check')}<div><b>Nothing needs you</b><p>The department is either working or idle — both are fine.</p></div></div>`;
  }
  h += '<div class="stack">';
  if (showBlocked) blocked.forEach(t => h += engBlockedCard(t, { instance: d.instance }));
  shown.forEach(w => h += engGateCard(w, { instance: d.instance }));
  h += '</div></section>';

  if (d.deciding && d.deciding.length) {
    h += `<section class="section"><div class="section-h"><h2>Applying your answer</h2><span class="n">${d.deciding.length}</span></div><div class="stack">${d.deciding.map(w => engDecidingCard(w, d.activity)).join('')}</div></section>`;
  }
  if (d.submitted && d.submitted.length) {
    h += `<section class="section"><div class="section-h"><h2>Waiting to be shaped</h2><span class="n">${d.submitted.length}</span></div><div class="stack">${d.submitted.map(s => {
      const via = s.origin === 'filed' ? 'filed' + (s.source ? ` by ${esc(s.source)}` : '') : 'sent from here';
      return `<div class="card"><div class="card-title" style="font-size:14px">${esc(s.title)}</div><div class="card-meta">${via}${s.received ? ' ' + esc(relTime(s.received)) : ''} · the PM shapes this into a ticket next pass</div></div>`;
    }).join('')}</div></section>`;
  }
  h += `<section class="section"><div class="section-h"><h2>Give the team something to build</h2></div>
    <div class="composer">
      <input id="eng-intake-title" placeholder="What do you want built?" />
      <textarea id="eng-intake-desc" rows="2" placeholder="Any context worth having (optional)"></textarea>
      <div class="foot"><button class="btn btn-primary" id="eng-intake-btn">${icon('send')}Send to the PM</button>
        <span class="hint" id="eng-intake-note">The Product Manager shapes it, writes the spec, and brings back a recommendation before anything gets built.</span></div>
    </div></section>`;
  return h;
}

function boardHtml(d) {
  const droppedCount = (d.by_state['dropped'] || []).length;
  let h = '';
  if (droppedCount) h += `<div class="boardbar"><button class="chip ${showDropped ? 'on' : ''}" data-dropped>${showDropped ? 'Hide' : 'Show'} dropped<span class="n">${droppedCount}</span></button></div>`;
  const cols = GROUPS.filter(([name]) => name !== 'Dropped' || showDropped).map(([name, states]) => {
    const items = [];
    states.forEach(st => (d.by_state[st] || []).forEach(t => items.push([st, t])));
    if (name === 'To-do') items.sort((a, b) => (PRIO_RANK[a[1].priority || ''] ?? 2) - (PRIO_RANK[b[1].priority || ''] ?? 2));
    return [name, items];
  }).filter(([name, items]) => name !== 'Dropped' || items.length);
  if (!cols.some(([, items]) => items.length)) return h + empty('Nothing on the board yet', '', 'columns');
  h += '<div class="lanes">';
  cols.forEach(([name, items]) => {
    h += `<div class="lane"><div class="lane-h">${esc(name)}<span class="n">${items.length}</span></div>`;
    if (!items.length) h += '<div class="lane-empty">—</div>';
    items.forEach(([st, t]) => {
      const live = d.activity && d.activity.running && d.activity.current_ticket === t.id;
      const need = WAITING_ON_YOU.includes(st) || t.blocked_on === 'approver';
      const tags = [tag(st)];
      if (live) tags.push(`<span class="tag tag-live">${esc(eventVerb(d.activity))}</span>`);
      if (need) tags.push(tag('waiting on you', 'tag-accent'));
      if (t.priority) tags.push(tag(t.priority, t.priority === 'now' ? 'tag-fill' : ''));
      if (t.lane && t.lane !== 'full') tags.push(tag(t.lane));
      let controls = '';
      if (st === 'blocked' && t.pr_url) controls += `<div class="mini-row"><a class="pbtn" href="${attr(t.pr_url)}" target="_blank" rel="noopener">${icon('arrowUpRight')}open PR</a>
        <button class="pbtn" data-act="eng-merge-check" data-ticket="${attr(t.id)}" data-force="0" data-instance="${attr(d.instance)}">check if merged</button>
        <button class="pbtn" data-act="eng-merge-check" data-ticket="${attr(t.id)}" data-force="1" data-instance="${attr(d.instance)}">mark merged</button></div>`;
      if (name === 'To-do') {
        const canHold = !WORKING.includes(st);
        const opt = (v, l) => `<button class="pbtn ${t.priority === v ? 'on' : ''}" data-act="eng-priority" data-ticket="${attr(t.id)}" data-priority="${v}" data-instance="${attr(d.instance)}">${l}</button>`;
        controls += `<div class="mini-row">${opt('now', 'now')}${opt('next', 'next')}${canHold ? opt('hold', 'hold') : ''}${t.priority ? opt('', 'clear') : ''}</div>`;
      }
      const time = [];
      if (t.time_spent || t.time_remaining) { if (t.time_spent) time.push(`${esc(t.time_spent)} spent`); if (t.time_remaining) time.push(`${esc(t.time_remaining)} left`); }
      else if (t.time_estimate) time.push(`est. ${esc(t.time_estimate)}`);
      h += `<div class="mini ${live ? 'live' : ''} ${need ? 'need' : ''}"><div class="mini-title">${esc(t.title)}</div><div class="mini-tags">${tags.join('')}</div>
        <div class="mini-sub">${esc(t.id)} · ${esc(t.project)} · ${esc(t.owner)}${time.length ? ' · ' + time.join(' · ') : ''}</div>${controls}</div>`;
    });
    h += '</div>';
  });
  return h + '</div>';
}

function bugsHtml(d) {
  let h = `<section class="section"><div class="section-h"><h2>Open bugs</h2><span class="n ${d.bugs.length ? 'hot' : ''}">${d.bugs.length}</span></div>`;
  if (!d.bugs.length) return h + `<div class="empty">${icon('check')}<div><b>No open bugs</b></div></div></section>`;
  h += '<div class="stack">' + d.bugs.map(b => {
    const sev = String(b.severity || '').toLowerCase();
    return `<div class="card"><div class="card-head"><div class="card-title"><span class="id">${esc(b.id)}</span>${esc(b.title)}</div><div class="card-tags">${tag(b.severity, /p0|p1/.test(sev) ? 'tag-bad' : '')}</div></div>
      <div class="card-meta">${esc(b.project)} · owner ${esc(b.owner)} · ${esc(b.age)}</div></div>`;
  }).join('') + '</div></section>';
  return h;
}

function render() {
  const el = root.querySelector('#eng'); if (!el) return;
  if (!data) { el.innerHTML = skeleton(3); return; }
  if (!data.instance) { el.innerHTML = empty(data.empty || 'No engineering instance yet', '', 'branch'); return; }
  let h = statsHtml(data.stats);
  if (sub !== 'board') h += `<section class="section"><div class="section-h"><h2>Right now</h2></div>${activityCard(data.activity)}</section>`;
  if (sub === 'decide') h += decideHtml(data);
  if (sub === 'board') h += boardHtml(data);
  if (sub === 'bugs') h += bugsHtml(data);
  el.innerHTML = h;
  el.parentElement.classList.toggle('wide', sub === 'board');
  afterRender(el);
  el.querySelectorAll('[data-wf]').forEach(b => b.onclick = () => { waitingFilter = b.dataset.wf; prefs.set('eng-waiting', waitingFilter); render(); });
  const dr = el.querySelector('[data-dropped]'); if (dr) dr.onclick = () => { showDropped = !showDropped; prefs.set('eng-dropped', showDropped ? '1' : '0'); render(); };
  const ib = el.querySelector('#eng-intake-btn'); if (ib) ib.onclick = intake;
}

async function intake() {
  const t = root.querySelector('#eng-intake-title'), dsc = root.querySelector('#eng-intake-desc'), note = root.querySelector('#eng-intake-note');
  if (!t.value.trim()) { t.focus(); return; }
  try {
    await api.post('/api/eng/intake', { title: t.value, description: dsc.value, instance });
    t.value = ''; dsc.value = '';
    note.textContent = 'Received — the Product Manager is shaping it now, usually a few minutes. It shows up under "Waiting to be shaped" until it becomes a ticket.';
    toast('Sent to the PM.', 'ok');
    load(true);
  } catch (e) { fail(e); }
}

async function load(quiet = false) {
  if (loading) return; loading = true;
  const el = root.querySelector('#eng'); if (!el) return;
  if (quiet && el) el.classList.add('refreshing');
  try {
    data = await api.get('/api/engineering', { instance });
    instance = data.instance || ''; prefs.set('eng-instance', instance);
    setAgent(data.activity);
    top(); render();
  } catch (e) { if (el) el.innerHTML = errorBox(e, 'engineering'); }
  finally { loading = false; el && el.classList.remove('refreshing'); }
}

export default {
  id: 'eng', title: 'Engineering', short: 'Eng', dept: 'eng', icon: 'branch', hot: true, section: 'main',
  async mount(r, route) {
    root = r; data = null; sub = route.sub || 'decide';
    root.innerHTML = `<div class="content-inner" id="eng"></div>`;
    top(); render();
    bindActions(root, () => load(true));
    await load();
    poller = makePoller(() => load(true), 10000); poller.start();
    setViewKeys({ r: () => load(true), '1': () => navigate('eng/decide'), '2': () => navigate('eng/board'), '3': () => navigate('eng/bugs') });
    setPaletteCommands(() => (data && data.tickets ? data.tickets : []).map(t => ({ group: 'Tickets', icon: 'branch', label: `${t.id} ${t.title}`, sub: t.state, run: () => navigate('eng/board') })));
    this._refresh = () => load(true); window.addEventListener('cc:refresh', this._refresh);
  },
  update(route) { sub = route.sub || 'decide'; top(); render(); root.scrollTop = 0; },
  unmount() { poller && poller.stop(); window.removeEventListener('cc:refresh', this._refresh); },
};
