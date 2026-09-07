// Logs — logs/*.log, newest first, with a tail viewer. Admin only.
import { api, setTop, refreshBtn, esc, attr, icon, empty, skeleton, relTime, setViewKeys, errorBox } from '../core.js';

let root, files = null, current = null, text = null;

function top() {
  setTop({ title: 'Logs', count: files ? files.length : null, right: refreshBtn() });
  document.querySelector('[data-refresh]').onclick = () => { loadList(); if (current) view(current); };
}
function colorize(t) {
  return esc(t).replace(/^(\[[^\]]+\])/gm, '<span class="ts">$1</span>');
}
function render() {
  const el = root.querySelector('#logs'); if (!el) return;
  el.classList.toggle('viewing', !!current);
  const list = el.querySelector('.logs-list'), main = el.querySelector('.logs-view');
  if (!files) list.innerHTML = skeleton(4);
  else if (!files.length) list.innerHTML = empty('No log files yet', '', 'scroll', true);
  else list.innerHTML = files.map(f => `<button class="log-item ${f.name === current ? 'on' : ''}" data-log="${attr(f.name)}"><div class="name">${esc(f.name)}</div><div class="sub">${(f.size / 1024).toFixed(1)} KB · ${esc(relTime(new Date(f.mtime * 1000).toISOString()))}</div></button>`).join('');
  list.querySelectorAll('[data-log]').forEach(b => b.onclick = () => view(b.dataset.log));
  if (!current) { main.innerHTML = `<div class="empty quiet">${icon('scroll')}<div><b>Pick a log file</b></div></div>`; return; }
  if (!text) { main.innerHTML = skeleton(2); return; }
  main.innerHTML = `<div class="meta"><button class="btn btn-ghost btn-sm only-mobile" id="logs-back">${icon('chevronLeft')}All logs</button><span class="mono">${esc(current)}</span><span>last ${text.shown} of ${text.total_lines} lines</span></div>
    <pre class="logtext">${text.text ? colorize(text.text) : '(empty)'}</pre>`;
  const back = main.querySelector('#logs-back'); if (back) back.onclick = () => { current = null; text = null; render(); };
  main.scrollTop = main.scrollHeight;
}
async function loadList() {
  try { const d = await api.get('/api/logs'); files = d.files || []; top(); render(); if (!current && files.length && window.innerWidth > 760) view(files[0].name); }
  catch (e) { const l = root.querySelector('.logs-list'); if (l) l.innerHTML = errorBox(e, 'the log list'); }
}
async function view(name) {
  current = name; text = null; render();
  try { text = await api.get('/api/logs/view', { name }); render(); }
  catch (e) { const v = root.querySelector('.logs-view'); if (v) v.innerHTML = errorBox(e, name); }
}
export default {
  id: 'logs', title: 'Logs', short: 'Logs', icon: 'scroll', section: 'system', adminOnly: true,
  async mount(r) {
    root = r; files = null; current = null; text = null;
    root.innerHTML = `<div class="logs" id="logs"><div class="logs-list"></div><div class="logs-view"></div></div>`;
    top(); render(); await loadList();
    setViewKeys({ r: () => { loadList(); if (current) view(current); } });
  },
};
