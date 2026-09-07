// Engineering — the board, per business instance. Decide is the gate; Board
// is the state of play; Bugs is the open list. Polls while open so "Right
// now" stays current — but only re-draws the page when something other than
// the live activity changed, so an open card or a half-written note survives.
import { api, setTop, seg, selectHtml, refreshBtn, esc, attr, icon, empty, skeleton, prefs, navigate, toast, fail, relTime, setViewKeys, makePoller, errorBox, plural, setAgent, setPaletteCommands, copyText, eventVerb } from '../core.js';
import { engGateCard, engBlockedCard, engDecidingCard, activityCard, bindActions, afterRender, captureInputs, restoreInputs, tag, GATE_LABEL } from './cards.js';

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
const FILTERS = [['merge', 'Merge'], ['scope', 'Scope'], ['intake-question', 'Question'], ['incident', 'Incident']];
// What the approver may pin to a request. Mirrors INTAKE_ATTACH_TYPES in server.py.
const ATTACH_TYPES = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.heic', '.pdf', '.doc', '.docx', '.txt', '.md'];
const ATTACH_MAX_FILE = 15 * 1024 * 1024, ATTACH_MAX_FILES = 10;

let root, data = null, sub = 'decide', instance = prefs.get('eng-instance', ''), poller = null, lastSig = '';
let showDropped = prefs.get('eng-dropped') === '1', waitingFilter = prefs.get('eng-waiting', 'all'), loading = false;
let attachments = []; // File objects pinned to the intake composer, kept across re-renders

function top() {
  const insts = (data && data.instances) || [];
  const waiting = data ? (data.waiting || []).length + (data.blocked_on_harry || []).length : null;
  const s = seg([{ id: 'decide', label: 'Decide', n: waiting, hot: !!waiting }, { id: 'board', label: 'Board' }, { id: 'bugs', label: 'Bugs', n: data ? (data.bugs || []).length : null }], sub);
  setTop({ title: 'Engineering', sub: s, right: (insts.length > 1 ? selectHtml('eng-inst', insts, instance) : '') + refreshBtn() });
  document.querySelectorAll('[data-seg]').forEach(b => b.onclick = () => navigate('eng/' + b.dataset.seg));
  const sel = document.getElementById('eng-inst'); if (sel) sel.onchange = () => { instance = sel.value; prefs.set('eng-instance', instance); data = null; lastSig = ''; render(); load(); };
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

// ── Decide ────────────────────────────────────────────────────────────────
const shownWaiting = d => d.waiting.filter(w => waitingFilter === 'all' || w.gate === waitingFilter);

// Everything on screen under "Waiting on you", as plain text with the full
// bodies — for pasting into a chat, a doc, or another model.
function waitingText(d) {
  const parts = [];
  if (waitingFilter === 'all') (d.blocked_on_harry || []).forEach(t => parts.push([`${t.id} · Blocked on you${t.project ? ' · ' + t.project : ''}`, t.title, t.pr_url ? `PR: ${t.pr_url}` : ''].filter(Boolean).join('\n')));
  shownWaiting(d).forEach(w => {
    const lines = [[w.ticket, GATE_LABEL[w.gate] || w.gate, w.project, w.raised ? 'raised ' + w.raised : ''].filter(Boolean).join(' · ')];
    if (w.recommendation) lines.push(`Recommendation: ${w.recommendation}`);
    if (w.time_estimate) lines.push(`Estimate: ${w.time_estimate}${w.time_impact ? ' (+' + w.time_impact + ')' : ''}`);
    lines.push('', String(w.body || '').trim());
    (w.pr_links || []).forEach(l => lines.push(`PR${l.repo ? ' (' + l.repo + ')' : ''}: ${l.url}`));
    parts.push(lines.join('\n'));
  });
  return parts.join('\n\n---\n\n') + '\n';
}

function decideHtml(d) {
  const blocked = d.blocked_on_harry || [];
  const total = d.waiting.length + blocked.length;
  const gateCount = g => d.waiting.filter(w => w.gate === g).length;
  const chipRow = [['all', 'All', total], ...FILTERS.map(([v, l]) => [v, l, gateCount(v)])]
    .map(([v, l, n]) => `<button class="chip ${waitingFilter === v ? 'on' : ''}" data-wf="${v}">${l}<span class="n">${n}</span></button>`).join('');
  let h = `<section class="section"><div class="section-h"><h2>Waiting on you</h2><span class="n ${total ? 'hot' : ''}">${total}</span>
    ${total ? `<span class="right"><div class="chips">${chipRow}</div><button class="btn btn-ghost btn-sm btn-icon" data-copy-waiting title="Copy everything shown here, in full" aria-label="Copy everything shown here">${icon('copy')}</button></span>` : ''}</div>`;
  const showBlocked = waitingFilter === 'all';
  const shown = shownWaiting(d);
  if (!shown.length && !(showBlocked && blocked.length)) {
    h += total ? empty('Nothing waiting on you matches this filter', '', 'inbox', true)
               : `<div class="empty">${icon('check')}<div><b>Nothing needs you</b><p>The department is either working or idle — both are fine.</p></div></div>`;
  }
  h += '<div class="stack">';
  if (showBlocked) blocked.forEach(t => h += engBlockedCard(t, { instance: d.instance }));
  shown.forEach(w => h += engGateCard(w, { instance: d.instance }));
  h += '</div></section>';

  if (d.deciding && d.deciding.length) {
    h += `<section class="section"><div class="section-h"><h2>Applying your answer</h2><span class="n">${d.deciding.length}</span></div><div class="stack" data-deciding>${decidingHtml(d)}</div></section>`;
  }
  if (d.submitted && d.submitted.length) {
    h += `<section class="section"><div class="section-h"><h2>Waiting to be shaped</h2><span class="n">${d.submitted.length}</span></div><div class="stack">${d.submitted.map(s => {
      const via = s.origin === 'filed' ? 'filed' + (s.source ? ` by ${esc(s.source)}` : '') : 'sent from here';
      return `<div class="card"><div class="card-title" style="font-size:14px">${esc(s.title)}</div><div class="card-meta">${via}${s.received ? ' ' + esc(relTime(s.received)) : ''} · the PM shapes this into a ticket next pass</div></div>`;
    }).join('')}</div></section>`;
  }
  h += `<section class="section"><div class="section-h"><h2>Give the team something to build</h2></div>
    <div class="composer" id="eng-composer">
      <input id="eng-intake-title" placeholder="What do you want built?" />
      <textarea id="eng-intake-desc" rows="2" placeholder="Any context worth having (optional) — paste a screenshot here, or drop files on this box"></textarea>
      <div class="attach" id="eng-attach"></div>
      <div class="foot"><button class="btn btn-primary" id="eng-intake-btn">${icon('send')}Send to the PM</button>
        <button class="btn btn-ghost" id="eng-attach-btn" type="button">${icon('paperclip')}Attach</button>
        <input type="file" id="eng-intake-file" multiple accept="${ATTACH_TYPES.join(',')},image/*,application/pdf" hidden>
        <span class="hint" id="eng-intake-note">The Product Manager shapes it, writes the spec, and brings back a recommendation before anything gets built. Images, PDFs and Word documents you attach go with it.</span></div>
    </div></section>`;
  return h;
}
const decidingHtml = d => d.deciding.map(w => engDecidingCard(w, d.activity)).join('');

// ── Intake attachments ────────────────────────────────────────────────────
const fmtSize = n => n >= 1024 * 1024 ? (n / (1024 * 1024)).toFixed(1) + ' MB' : Math.max(1, Math.round(n / 1024)) + ' KB';
const isImage = f => /^image\//.test(f.type);
function addFiles(list) {
  const rejected = [];
  Array.from(list || []).forEach(f => {
    const ext = (f.name.match(/\.[^.]+$/) || [''])[0].toLowerCase();
    if (!ATTACH_TYPES.includes(ext) && !isImage(f)) { rejected.push(`${f.name}: not an image, PDF, Word or text file`); return; }
    if (f.size > ATTACH_MAX_FILE) { rejected.push(`${f.name}: over 15 MB`); return; }
    if (attachments.some(a => a.name === f.name && a.size === f.size)) return;
    if (attachments.length >= ATTACH_MAX_FILES) { rejected.push(`${f.name}: at most ${ATTACH_MAX_FILES} files per request`); return; }
    if (isImage(f)) f._url = URL.createObjectURL(f);
    attachments.push(f);
  });
  if (rejected.length) toast(rejected.join(' · '), 'warn', 6000);
  renderAttach();
}
function removeFile(i) { const f = attachments.splice(i, 1)[0]; if (f && f._url) URL.revokeObjectURL(f._url); renderAttach(); }
function clearFiles() { attachments.forEach(f => f._url && URL.revokeObjectURL(f._url)); attachments = []; }
function renderAttach() {
  const el = root.querySelector('#eng-attach'); if (!el) return;
  const total = attachments.reduce((s, f) => s + f.size, 0);
  el.innerHTML = attachments.map((f, i) => `<span class="chip chip-file" title="${attr(f.name)}">${f._url ? `<img class="thumb" src="${attr(f._url)}" alt="">` : icon('file', 'ic-sm')}<span class="name">${esc(f.name)}</span><span class="n">${fmtSize(f.size)}</span><button type="button" class="rm" data-rm="${i}" aria-label="Remove ${attr(f.name)}">${icon('x', 'ic-sm')}</button></span>`).join('')
    + (attachments.length > 1 ? `<span class="attach-sum dim">${plural(attachments.length, 'file')} · ${fmtSize(total)}</span>` : '');
  el.querySelectorAll('[data-rm]').forEach(b => b.onclick = () => removeFile(Number(b.dataset.rm)));
}
const readB64 = f => new Promise((res, rej) => {
  const r = new FileReader();
  r.onload = () => res({ name: f.name, type: f.type, data: String(r.result).split(',')[1] || '' });
  r.onerror = () => rej(new Error('Could not read ' + f.name));
  r.readAsDataURL(f);
});
function bindComposer(el) {
  const box = el.querySelector('#eng-composer'); if (!box) return;
  const fileIn = el.querySelector('#eng-intake-file');
  el.querySelector('#eng-intake-btn').onclick = intake;
  el.querySelector('#eng-attach-btn').onclick = () => fileIn.click();
  fileIn.onchange = () => { addFiles(fileIn.files); fileIn.value = ''; };
  box.addEventListener('dragover', e => { e.preventDefault(); box.classList.add('drop'); });
  box.addEventListener('dragleave', e => { if (!box.contains(e.relatedTarget)) box.classList.remove('drop'); });
  box.addEventListener('drop', e => { e.preventDefault(); box.classList.remove('drop'); addFiles(e.dataTransfer.files); });
  box.addEventListener('paste', e => { const fs = Array.from(e.clipboardData?.files || []); if (fs.length) { e.preventDefault(); addFiles(fs); } });
  renderAttach();
}

// ── Board ─────────────────────────────────────────────────────────────────
// A blocked ticket whose PR is up is not stuck — it is built and waiting on
// your merge. That belongs under Ready to ship; Blocked keeps only the tickets
// held by something else.
const prRaised = (t, d) => !!t.pr_url || (d.waiting || []).some(w => w.ticket === t.id && w.gate === 'merge');
function boardHtml(d) {
  const droppedCount = (d.by_state['dropped'] || []).length;
  let h = '';
  if (droppedCount) h += `<div class="boardbar"><button class="chip ${showDropped ? 'on' : ''}" data-dropped>${showDropped ? 'Hide' : 'Show'} dropped<span class="n">${droppedCount}</span></button></div>`;
  const byLane = new Map(GROUPS.map(([name]) => [name, []]));
  GROUPS.forEach(([name, states]) => states.forEach(st => (d.by_state[st] || []).forEach(t => {
    const lane = st === 'blocked' && prRaised(t, d) ? 'Ready to ship' : name;
    byLane.get(lane).push([st, t]);
  })));
  byLane.get('To-do').sort((a, b) => (PRIO_RANK[a[1].priority || ''] ?? 2) - (PRIO_RANK[b[1].priority || ''] ?? 2));
  const cols = GROUPS.map(([name]) => [name, byLane.get(name)]).filter(([name, items]) => name !== 'Dropped' || (showDropped && items.length));
  if (!cols.some(([, items]) => items.length)) return h + empty('Nothing on the board yet', '', 'columns');
  h += '<div class="lanes">';
  cols.forEach(([name, items]) => {
    h += `<div class="lane"><div class="lane-h">${esc(name)}<span class="n">${items.length}</span></div>`;
    if (name === 'Ready to ship') h += `<div class="lane-note">Built, PR up, waiting on your merge</div>`;
    if (!items.length) h += '<div class="lane-empty">—</div>';
    items.forEach(([st, t]) => {
      const live = d.activity && d.activity.running && d.activity.current_ticket === t.id;
      const pr = st === 'blocked' && prRaised(t, d);
      const mergeGate = (d.waiting || []).some(w => w.ticket === t.id && w.gate === 'merge');
      const need = WAITING_ON_YOU.includes(st) || t.blocked_on === 'approver';
      const tags = [pr ? tag('pr raised') : tag(st)];
      if (live) tags.push(`<span class="tag tag-live">${esc(eventVerb(d.activity))}</span>`);
      if (need) tags.push(tag('waiting on you', 'tag-accent'));
      if (t.priority) tags.push(tag(t.priority, t.priority === 'now' ? 'tag-fill' : ''));
      if (t.lane && t.lane !== 'full') tags.push(tag(t.lane));
      let controls = '';
      if (pr) controls += `<div class="mini-row">${mergeGate ? `<button class="pbtn" data-act="go" data-to="eng/decide">${icon('check')}decide</button>` : ''}${t.pr_url ? `<a class="pbtn" href="${attr(t.pr_url)}" target="_blank" rel="noopener">${icon('arrowUpRight')}open PR</a>` : ''}
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
  const kept = captureInputs(el);
  let h = statsHtml(data.stats);
  if (sub !== 'board') h += `<section class="section"><div class="section-h"><h2>Right now</h2></div><div data-activity>${activityCard(data.activity)}</div></section>`;
  if (sub === 'decide') h += decideHtml(data);
  if (sub === 'board') h += boardHtml(data);
  if (sub === 'bugs') h += bugsHtml(data);
  el.innerHTML = h;
  el.parentElement.classList.toggle('wide', sub === 'board');
  restoreInputs(el, kept);
  afterRender(el);
  el.querySelectorAll('[data-wf]').forEach(b => b.onclick = () => { waitingFilter = b.dataset.wf; prefs.set('eng-waiting', waitingFilter); render(); });
  const cp = el.querySelector('[data-copy-waiting]'); if (cp) cp.onclick = async () => {
    const n = shownWaiting(data).length + (waitingFilter === 'all' ? (data.blocked_on_harry || []).length : 0);
    const ok = await copyText(waitingText(data));
    toast(ok ? `Copied ${plural(n, 'item')} to the clipboard.` : 'Could not copy — the browser blocked clipboard access.', ok ? 'ok' : 'bad');
  };
  const dr = el.querySelector('[data-dropped]'); if (dr) dr.onclick = () => { showDropped = !showDropped; prefs.set('eng-dropped', showDropped ? '1' : '0'); render(); };
  bindComposer(el);
}

// Only the live bits changed (the agent pill, "Right now", the applying
// notes): swap those in place and leave the rest of the page alone.
function patchLive() {
  const el = root.querySelector('#eng'); if (!el) return;
  const a = el.querySelector('[data-activity]'); if (a) a.innerHTML = activityCard(data.activity);
  const dq = el.querySelector('[data-deciding]'); if (dq) dq.innerHTML = decidingHtml(data);
}

const NOTE_DEFAULT = 'The Product Manager shapes it, writes the spec, and brings back a recommendation before anything gets built. Images, PDFs and Word documents you attach go with it.';
async function intake() {
  const t = root.querySelector('#eng-intake-title'), dsc = root.querySelector('#eng-intake-desc'), note = root.querySelector('#eng-intake-note'), btn = root.querySelector('#eng-intake-btn');
  if (!t.value.trim()) { t.focus(); return; }
  btn.disabled = true;
  note.textContent = attachments.length ? `Sending with ${plural(attachments.length, 'file')}…` : 'Sending…';
  try {
    const files = await Promise.all(attachments.map(readB64));
    await api.post('/api/eng/intake', { title: t.value, description: dsc.value, instance, attachments: files });
    t.value = ''; dsc.value = ''; clearFiles(); renderAttach();
    note.textContent = 'Received — the Product Manager is shaping it now, usually a few minutes. It shows up under "Waiting to be shaped" until it becomes a ticket.';
    toast('Sent to the PM.', 'ok');
    load(true);
  } catch (e) { fail(e); note.textContent = NOTE_DEFAULT; }
  finally { btn.disabled = false; }
}

async function load(quiet = false) {
  if (loading) return; loading = true;
  const el = root.querySelector('#eng'); if (!el) { loading = false; return; }
  // Dim only when a refresh is actually slow; a 10-second poll must not blink.
  const dim = quiet ? setTimeout(() => el.classList.add('refreshing'), 400) : null;
  try {
    const next = await api.get('/api/engineering', { instance });
    const sig = JSON.stringify({ ...next, activity: null });
    const same = quiet && !!data && sig === lastSig && sub !== 'board';
    data = next; lastSig = sig;
    instance = data.instance || ''; prefs.set('eng-instance', instance);
    setAgent(data.activity);
    top();
    if (same) patchLive(); else render();
  } catch (e) { if (el) el.innerHTML = errorBox(e, 'engineering'); }
  finally { loading = false; clearTimeout(dim); el.classList.remove('refreshing'); }
}

export default {
  id: 'eng', title: 'Engineering', short: 'Eng', dept: 'eng', icon: 'branch', hot: true, section: 'main',
  async mount(r, route) {
    root = r; data = null; lastSig = ''; sub = route.sub || 'decide';
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
