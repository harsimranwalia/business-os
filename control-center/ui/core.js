// Control Center core: data layer, formatting, toasts, dialogs, router, shell,
// keyboard. Views live in ./views/*.js and only ever touch the DOM inside the
// root they are handed. Nothing here knows what a ticket or a lead is.
import { icon, DEPT_ICON } from './icons.js';
export { icon };

// ── Escaping & formatting ─────────────────────────────────────────────────
export const esc = s => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
export const attr = s => String(s == null ? '' : s)
  .replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
export const cssId = s => String(s || '').replace(/[^A-Za-z0-9]/g, '-');
export const plural = (n, one, many) => `${n} ${n === 1 ? one : (many || one + 's')}`;

export function relTime(iso) {
  if (!iso) return '';
  const ms = Date.now() - new Date(iso).getTime();
  if (!isFinite(ms) || ms < 0) return '';
  const min = Math.round(ms / 60000);
  if (min < 1) return 'just now';
  if (min < 60) return `${min}m ago`;
  const hr = Math.round(min / 60);
  if (hr < 24) return `${hr}h ago`;
  const d = Math.round(hr / 24);
  return d === 1 ? 'yesterday' : `${d}d ago`;
}
export function daysAgo(iso) {
  if (!iso) return null;
  const ms = Date.now() - new Date(iso).getTime();
  return isFinite(ms) ? Math.floor(ms / 86400000) : null;
}
export function fmtDur(sec) {
  if (sec == null) return '';
  sec = Math.max(0, Math.round(sec));
  if (sec < 60) return `${sec}s`;
  const min = Math.floor(sec / 60);
  if (min < 60) return `${min}m`;
  const hr = Math.floor(min / 60), rem = min % 60;
  return `${hr}h${rem ? ' ' + rem + 'm' : ''}`;
}
export const money = (n, dp = 2) => '$' + Number(n || 0).toLocaleString('en-US', { minimumFractionDigits: dp, maximumFractionDigits: dp });
export const money0 = n => '$' + Math.round(Number(n || 0)).toLocaleString('en-US');
export function compact(n) {
  n = Number(n || 0);
  if (n >= 1e9) return (n / 1e9).toFixed(2).replace(/\.?0+$/, '') + 'B';
  if (n >= 1e6) return (n / 1e6).toFixed(1).replace(/\.0$/, '') + 'M';
  if (n >= 1e3) return (n / 1e3).toFixed(1).replace(/\.0$/, '') + 'k';
  return String(n);
}
export function fmtWhen(ts) { return (ts || '').replace('T', ' ').replace(/Z$/, '').replace(/:\d\d$/, '') || '—'; }
export function fmtDate(iso, opts) {
  if (!iso) return '';
  const d = new Date(iso.length === 10 ? iso + 'T12:00:00' : iso);
  if (!isFinite(d)) return iso;
  return d.toLocaleDateString('en-US', opts || { weekday: 'short', month: 'short', day: 'numeric' });
}
export function dueLabel(isoDate, today) {
  // "today", "tomorrow", "Mon", "in 5d", "3d late"
  if (!isoDate) return '';
  const t = new Date((today || new Date().toISOString().slice(0, 10)) + 'T12:00:00');
  const d = new Date(isoDate + 'T12:00:00');
  const diff = Math.round((d - t) / 86400000);
  if (diff === 0) return 'today';
  if (diff === 1) return 'tomorrow';
  if (diff < 0) return `${-diff}d late`;
  if (diff < 7) return d.toLocaleDateString('en-US', { weekday: 'short' });
  return `in ${diff}d`;
}
export const todayLabel = () => new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });

// Minimal markdown for decision bodies and lead histories. Headings, bold,
// inline code, bullets, numbered lists, blockquotes, paragraphs. Hard-wrapped
// prose (the files are written at ~72 cols) is reflowed first.
export function reflowHardWraps(text) {
  const lines = String(text == null ? '' : text).split('\n');
  const out = [];
  for (const line of lines) {
    const t = line.trim();
    const startsNew = out.length === 0 || t === '' || /^#{1,3}\s/.test(t) || /^(\d+\.|[-*>])\s/.test(t) || /^```/.test(t);
    if (startsNew) { out.push(line); continue; }
    const prevT = out[out.length - 1].trim();
    if (prevT === '' || /^#{1,3}\s/.test(prevT) || /^```/.test(prevT)) out.push(line);
    else out[out.length - 1] = out[out.length - 1].replace(/\s+$/, '') + ' ' + t;
  }
  return out.join('\n');
}
function inline(s) {
  return esc(s)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[\s(])\*([^*\n]+)\*(?=[\s).,;:!?]|$)/g, '$1<em>$2</em>')
    .replace(/(https?:\/\/[^\s<)]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>');
}
export function renderMarkdown(text, opts = {}) {
  const lines = String(text == null ? '' : text).split('\n');
  let html = '', para = [], list = null;
  const flushP = () => { if (para.length) { html += `<p>${para.map(inline).join(opts.breaks ? '<br>' : ' ')}</p>`; para = []; } };
  const flushL = () => { if (list) { html += `<${list.tag}>${list.items.map(i => `<li>${inline(i)}</li>`).join('')}</${list.tag}>`; list = null; } };
  for (const raw of lines) {
    const t = raw.trim();
    if (!t) { flushP(); flushL(); continue; }
    let m;
    if ((m = t.match(/^(#{1,3})\s+(.*)$/))) { flushP(); flushL(); html += `<h${Math.min(3, m[1].length + 1)}>${inline(m[2])}</h${Math.min(3, m[1].length + 1)}>`; continue; }
    if ((m = t.match(/^[-*]\s+(.*)$/))) { flushP(); if (!list || list.tag !== 'ul') { flushL(); list = { tag: 'ul', items: [] }; } list.items.push(m[1]); continue; }
    if ((m = t.match(/^\d+\.\s+(.*)$/))) { flushP(); if (!list || list.tag !== 'ol') { flushL(); list = { tag: 'ol', items: [] }; } list.items.push(m[1]); continue; }
    if ((m = t.match(/^>\s?(.*)$/))) { flushP(); flushL(); html += `<blockquote>${inline(m[1])}</blockquote>`; continue; }
    if (t === '---') { flushP(); flushL(); continue; }
    flushL(); para.push(t);
  }
  flushP(); flushL();
  return html;
}
export const renderDecisionBody = text => renderMarkdown(reflowHardWraps(text));

// ── Data layer ────────────────────────────────────────────────────────────
// A 401 anywhere means the session is gone (expired, or the server restarted
// and dropped its in-memory store): one redirect here, not one per call site.
async function request(path, opts) {
  const r = await fetch(path, opts);
  if (r.status === 401) { window.location.href = '/login'; throw new Error('signed out'); }
  let data = null;
  try { data = await r.json(); } catch (e) { data = {}; }
  if (!r.ok) { const err = new Error((data && data.error) || `HTTP ${r.status}`); err.status = r.status; err.data = data; throw err; }
  return data;
}
export const api = {
  get: (path, params) => {
    const p = new URLSearchParams();
    Object.entries(params || {}).forEach(([k, v]) => { if (v !== undefined && v !== null && v !== '') p.set(k, v); });
    const q = p.toString();
    return request(path + (q ? '?' + q : ''));
  },
  post: (path, body) => request(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body || {}) }),
};

// ── Session ───────────────────────────────────────────────────────────────
export const me = { email: '', name: '', phone: '', role: 'partner', instances: [], departments: [], config_ready: false, config_missing: [] };
export async function loadMe() {
  const d = await request('/api/auth/me');
  if (!d || !d.email) { window.location.href = '/login'; throw new Error('signed out'); }
  Object.assign(me, d);
  return me;
}
export const isAdmin = () => me.role === 'admin';
export const canSee = dept => !dept || isAdmin() || (me.departments || []).includes(dept);
export async function logout() { try { await api.post('/api/auth/logout'); } catch (e) {} window.location.href = '/login'; }

// Remembered picks (which business, which channel…). One place, so a key is
// never spelled two ways.
export const prefs = {
  get: (k, d) => { try { const v = localStorage.getItem('cc:' + k); return v == null ? d : v; } catch (e) { return d; } },
  set: (k, v) => { try { if (v == null || v === '') localStorage.removeItem('cc:' + k); else localStorage.setItem('cc:' + k, String(v)); } catch (e) {} },
};

// ── Toasts ────────────────────────────────────────────────────────────────
let toastRoot = null;
export function toast(message, kind = 'info', ms = 4200) {
  if (!toastRoot) { toastRoot = document.createElement('div'); toastRoot.className = 'toasts'; document.body.appendChild(toastRoot); }
  const el = document.createElement('div');
  el.className = 'toast ' + kind;
  const ic = kind === 'ok' ? 'check' : kind === 'bad' ? 'alert' : kind === 'warn' ? 'alert' : 'circle';
  el.innerHTML = `${icon(ic)}<div>${esc(message)}</div><button class="close" aria-label="Dismiss">${icon('x', 'ic-sm')}</button>`;
  el.querySelector('.close').onclick = () => el.remove();
  toastRoot.appendChild(el);
  if (ms) setTimeout(() => { el.style.transition = 'opacity 200ms'; el.style.opacity = '0'; setTimeout(() => el.remove(), 220); }, ms);
  return el;
}
export const fail = e => toast(e && e.message ? e.message : String(e || 'Something went wrong'), 'bad', 6000);

// ── Dialogs ───────────────────────────────────────────────────────────────
// One backdrop at a time. Escape closes, click outside closes, focus lands on
// the first field. Every former alert()/confirm()/prompt() goes through here.
let openDialog = null;
export function dialog({ title, sub, body = '', foot = '', size = '', onClose, cls = '' }) {
  closeDialog();
  const back = document.createElement('div');
  back.className = 'backdrop';
  back.innerHTML = `<div class="dialog ${size} ${cls}" role="dialog" aria-modal="true" aria-label="${attr(title || 'Dialog')}">
    <div class="sheet-handle"></div>
    ${title !== undefined ? `<div class="dialog-head"><div style="min-width:0"><div class="dialog-title">${title}</div>${sub ? `<div class="dialog-sub">${sub}</div>` : ''}</div>
      <button class="dialog-x" aria-label="Close">${icon('x')}</button></div>` : ''}
    <div class="dialog-body">${body}</div>
    ${foot ? `<div class="dialog-foot">${foot}</div>` : ''}
  </div>`;
  const ctl = {
    el: back, box: back.querySelector('.dialog'),
    q: sel => back.querySelector(sel),
    close: () => { if (openDialog === ctl) { back.remove(); openDialog = null; onClose && onClose(); } },
  };
  back.addEventListener('click', e => { if (e.target === back) ctl.close(); });
  const x = back.querySelector('.dialog-x'); if (x) x.onclick = ctl.close;
  document.body.appendChild(back);
  openDialog = ctl;
  const first = back.querySelector('input:not([type=hidden]), textarea, select, button.btn-primary, button');
  if (first) setTimeout(() => first.focus(), 30);
  return ctl;
}
export function closeDialog() { if (openDialog) openDialog.close(); }
export const dialogOpen = () => !!openDialog;

export function confirm({ title, body, ok = 'Confirm', danger = false, cancel = 'Cancel' }) {
  return new Promise(resolve => {
    const d = dialog({
      title, size: 'sm', body: body ? `<div>${body}</div>` : '',
      foot: `<button class="btn" data-x>${esc(cancel)}</button><button class="btn ${danger ? 'btn-bad' : 'btn-primary'}" data-ok>${esc(ok)}</button>`,
      onClose: () => resolve(false),
    });
    d.q('[data-x]').onclick = d.close;
    d.q('[data-ok]').onclick = () => { const c = d.close; openDialog = null; d.el.remove(); resolve(true); };
    d.q('[data-ok]').focus();
  });
}
export function promptText({ title, sub, label, placeholder = '', value = '', ok = 'Save', multiline = true, required = false }) {
  return new Promise(resolve => {
    const d = dialog({
      title, sub, size: 'sm',
      body: `<div class="field">${label ? `<label>${esc(label)}</label>` : ''}${multiline
        ? `<textarea rows="3" placeholder="${attr(placeholder)}">${esc(value)}</textarea>`
        : `<input type="text" placeholder="${attr(placeholder)}" value="${attr(value)}" />`}</div>`,
      foot: `<button class="btn" data-x>Cancel</button><button class="btn btn-primary" data-ok>${esc(ok)}</button>`,
      onClose: () => resolve(null),
    });
    const input = d.q('textarea, input');
    const submit = () => { const v = input.value.trim(); if (required && !v) { input.focus(); return; } openDialog = null; d.el.remove(); resolve(v); };
    d.q('[data-x]').onclick = d.close;
    d.q('[data-ok]').onclick = submit;
    input.addEventListener('keydown', e => { if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') submit(); if (!multiline && e.key === 'Enter') submit(); });
  });
}

// ── Router ────────────────────────────────────────────────────────────────
// Hash routes: #/inbox · #/marketing/decide?channel=linkedin · #/eng/board.
// The hash keeps deep links and the back button working with no server help.
export function parseRoute() {
  const h = (location.hash || '#/inbox').replace(/^#\/?/, '');
  const [pathPart, query = ''] = h.split('?');
  const seg = pathPart.split('/').filter(Boolean);
  const params = Object.fromEntries(new URLSearchParams(query));
  return { view: seg[0] || 'inbox', sub: seg[1] || '', params, path: pathPart };
}
export function navigate(path, params) {
  const p = params ? new URLSearchParams(Object.entries(params).filter(([, v]) => v != null && v !== '')).toString() : '';
  const target = '#/' + path.replace(/^\/+/, '') + (p ? '?' + p : '');
  if (location.hash === target) window.dispatchEvent(new HashChangeEvent('hashchange'));
  else location.hash = target;
}

// ── Keyboard ──────────────────────────────────────────────────────────────
// Two scopes: global (navigation, palette, help) and the active view's own
// bindings. Anything typed inside a field is left alone.
const globalKeys = {};
let viewKeys = {};
export function setViewKeys(map) { viewKeys = map || {}; }
export function bindGlobalKey(combo, fn) { globalKeys[combo] = fn; }
export const isTyping = () => {
  const a = document.activeElement;
  return a && (a.tagName === 'INPUT' || a.tagName === 'TEXTAREA' || a.tagName === 'SELECT' || a.isContentEditable);
};
let pendingG = false;
document.addEventListener('keydown', e => {
  const combo = (e.metaKey || e.ctrlKey ? 'mod+' : '') + (e.shiftKey && e.key.length > 1 ? 'shift+' : '') + e.key.toLowerCase();
  if (combo === 'mod+k') { e.preventDefault(); (globalKeys['mod+k'] || (() => {}))(); return; }
  if (e.key === 'Escape') { if (openDialog) { openDialog.close(); e.preventDefault(); return; } if (isTyping()) { document.activeElement.blur(); return; } }
  if (isTyping() || openDialog) return;
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  if (pendingG) { pendingG = false; const fn = globalKeys['g ' + e.key.toLowerCase()]; if (fn) { e.preventDefault(); fn(); } return; }
  if (e.key === 'g') { pendingG = true; setTimeout(() => { pendingG = false; }, 900); return; }
  const fn = viewKeys[e.key] || globalKeys[e.key];
  if (fn) { e.preventDefault(); fn(e); }
});

// ── Shell ─────────────────────────────────────────────────────────────────
// Rail (desktop) · bottom tab bar (phone) · topbar. Views register once; the
// shell draws only the ones this account may open.
const registry = [];
export function registerView(v) { registry.push(v); }
export const views = () => registry;
export const visibleViews = () => registry.filter(v => (!v.adminOnly || isAdmin()) && canSee(v.dept));
const counts = {};   // view id -> number needing attention (badges)
export function setCount(id, n) { counts[id] = n; paintBadges(); }
function paintBadges() {
  document.querySelectorAll('[data-badge]').forEach(el => {
    const n = counts[el.dataset.badge] || 0;
    el.textContent = n > 99 ? '99+' : String(n);
    el.classList.toggle('zero', !n);
    el.classList.toggle('hot', !!n && el.dataset.hot === '1');
  });
}

let agentInfo = null, agentHead = null;   // last-seen engineering activity (+ the in-flight ticket), for the rail pill
export function setAgent(a, head) { agentInfo = a; agentHead = head || null; paintAgent(); }
function agentSummary(a) {
  if (!a) return { cls: '', title: 'Agent', sub: 'no signal yet' };
  if (a.mode_halting) return { cls: 'warn', title: 'Paused', sub: `MODE=${a.mode}` };
  if (a.backoff_active) return { cls: 'warn', title: 'Backed off', sub: `retry in ~${fmtDur(a.backoff_seconds)}` };
  if (a.running) {
    const verb = eventVerb(a);
    return { cls: 'on', title: a.current_ticket ? `${verb} ${a.current_ticket}` : verb, sub: `${fmtDur(a.running_seconds)} · ${a.hops_today}/${a.hops_budget || '∞'} hops today` };
  }
  const hops = `${a.hops_today}/${a.hops_budget || '∞'} hops`;
  if (agentHead) return { cls: agentHead.stale ? 'warn' : '', title: `${agentHead.id} ${agentHead.word}`, sub: agentHead.stale ? 'no pass queued' : `between passes · ${hops}` };
  return { cls: '', title: 'Agent idle', sub: `${hops} · ${a.pending_count} queued` };
}
const EVENT_VERBS = { continue: 'Building', decision: 'Applying decision', intake: 'Shaping request', scheduled: 'Running sweep', watch: 'Checking inbox', finding: 'Handling finding' };
export function eventVerb(a) { const head = String(a.current_event || '').split(/\s/)[0]; return EVENT_VERBS[head] || 'Working'; }
function paintAgent() {
  const s = agentSummary(agentInfo);
  document.querySelectorAll('[data-agent]').forEach(el => {
    el.querySelector('.agent-dot').className = 'agent-dot ' + s.cls;
    el.querySelector('.agent-title').textContent = s.title;
    el.querySelector('.agent-sub').textContent = s.sub;
  });
}

function initials(name, email) {
  const n = (name || '').trim();
  if (n) return n.split(/\s+/).map(w => w[0]).slice(0, 2).join('').toUpperCase();
  return (email || '?')[0].toUpperCase();
}

export function renderShell(app) {
  const vis = visibleViews();
  const cfgDot = v => v.id === 'config' && !isAdmin() && (me.config_missing || []).length ? '<span class="dot-warn" title="Configuration incomplete"></span>' : '';
  const item = v => `<button class="nav-item" data-nav="${v.id}">${icon(v.icon || DEPT_ICON[v.id] || 'circle')}<span>${esc(v.title)}</span>${cfgDot(v)}
    <span class="badge zero" data-badge="${v.id}" data-hot="${v.hot ? '1' : '0'}"></span></button>`;
  const main = vis.filter(v => v.section !== 'system'), sys = vis.filter(v => v.section === 'system');
  app.innerHTML = `
    <aside class="rail">
      <div class="brand"><div class="brand-mark">${icon('mark')}</div><div class="brand-name">Business OS<small>Control Center</small></div></div>
      <nav class="nav">
        ${main.map(item).join('')}
        ${sys.length ? `<div class="nav-label">System</div>${sys.map(item).join('')}` : ''}
      </nav>
      <div class="rail-foot">
        ${canSee('eng') ? `<button class="agent" data-agent data-nav="eng" title="Open Engineering">
          <span class="agent-dot"></span><span class="agent-text"><span class="agent-title">Agent</span><span class="agent-sub"></span></span>
        </button>` : ''}
        <button class="user" data-user-menu>
          <span class="avatar">${esc(initials(me.name, me.email))}</span>
          <span class="user-text"><span class="user-name">${esc(me.name || me.email)}</span><span class="user-sub">${esc(me.name ? me.email : me.role)}</span></span>
        </button>
      </div>
    </aside>
    <div class="main">
      <header class="topbar" id="topbar"></header>
      <div class="subnav-mobile only-mobile" id="subnav-mobile" hidden></div>
      <main class="content" id="content"></main>
    </div>
    <nav class="tabbar" id="tabbar"></nav>`;
  renderTabbar(vis);
  app.addEventListener('click', e => {
    const nav = e.target.closest('[data-nav]');
    if (nav) { navigate(nav.dataset.nav); return; }
    const um = e.target.closest('[data-user-menu]');
    if (um) { openUserMenu(um); }
  });
  paintBadges(); paintAgent();
}

function renderTabbar(vis) {
  // Five slots: the first four department-ish views, then "More" for the rest.
  const primary = vis.filter(v => v.section !== 'system').slice(0, 4);
  const rest = vis.filter(v => !primary.includes(v));
  const tb = document.getElementById('tabbar');
  tb.innerHTML = primary.map(v => `<button class="tab" data-nav="${v.id}" data-tab="${v.id}">${icon(v.icon || DEPT_ICON[v.id])}<span>${esc(v.short || v.title)}</span>
      <span class="badge zero" data-badge="${v.id}" data-hot="${v.hot ? '1' : '0'}"></span></button>`).join('') +
    (rest.length ? `<button class="tab" data-more-tab data-tab="more">${icon('more')}<span>More</span></button>` : '');
  const more = tb.querySelector('[data-more-tab]');
  if (more) more.onclick = e => {
    e.stopPropagation();
    const d = dialog({ title: 'More', size: 'sm', body: `<div class="stack" style="gap:4px">${rest.map(v =>
      `<button class="nav-item" data-go="${v.id}">${icon(v.icon || DEPT_ICON[v.id])}<span>${esc(v.title)}</span></button>`).join('')}
      <div class="menu-sep" style="height:1px;background:var(--line);margin:6px 0"></div>
      <button class="nav-item" data-help>${icon('keyboard')}<span>Keyboard shortcuts</span></button>
      <button class="nav-item" data-logout>${icon('logout')}<span>Log out</span></button></div>` });
    d.el.querySelectorAll('[data-go]').forEach(b => b.onclick = () => { d.close(); navigate(b.dataset.go); });
    d.el.querySelector('[data-logout]').onclick = logout;
    d.el.querySelector('[data-help]').onclick = () => { d.close(); showShortcuts(); };
  };
}

function openUserMenu(anchor) {
  document.querySelectorAll('.menu').forEach(m => m.remove());
  const m = document.createElement('div');
  m.className = 'menu';
  m.innerHTML = `<div class="meta"><b>${esc(me.name || me.email)}</b>${esc(me.email)} · ${esc(me.role)}</div><div class="sep"></div>
    <button data-help>${icon('keyboard')}Keyboard shortcuts <span class="kbd" style="margin-left:auto">?</span></button>
    <button data-logout>${icon('logout')}Log out</button>`;
  const r = anchor.getBoundingClientRect();
  m.style.left = r.left + 'px'; m.style.bottom = (window.innerHeight - r.top + 6) + 'px';
  document.body.appendChild(m);
  m.querySelector('[data-logout]').onclick = logout;
  m.querySelector('[data-help]').onclick = () => { m.remove(); showShortcuts(); };
  const off = e => { if (!m.contains(e.target)) { m.remove(); document.removeEventListener('mousedown', off); } };
  setTimeout(() => document.addEventListener('mousedown', off), 0);
}

export function showShortcuts() {
  const k = (...ks) => ks.map(x => `<span class="kbd">${esc(x)}</span>`).join('');
  dialog({ title: 'Keyboard shortcuts', size: 'sm', body: `<div class="shortcuts">
    <div><span>Search / jump</span><span>${k('⌘', 'K')}</span></div>
    <div><span>Next / previous item</span><span>${k('J')} ${k('K')}</span></div>
    <div><span>Approve focused item</span><span>${k('A')}</span></div>
    <div><span>Request changes / edit</span><span>${k('C')}</span></div>
    <div><span>Reject / skip</span><span>${k('X')}</span></div>
    <div><span>Expand / open</span><span>${k('Enter')}</span></div>
    <div><span>Write a note</span><span>${k('N')}</span></div>
    <div><span>Refresh</span><span>${k('R')}</span></div>
    <div><span>Go to Inbox</span><span>${k('G')} ${k('I')}</span></div>
    <div><span>Go to Marketing / Sales / Eng / Cost</span><span>${k('G')} ${k('M')} · ${k('S')} · ${k('E')} · ${k('$')}</span></div>
    <div><span>Close / blur</span><span>${k('Esc')}</span></div>
    <div><span>This list</span><span>${k('?')}</span></div>
  </div>` });
}

// Topbar contents are the view's: title, an optional sub-nav (segmented
// control or chips), and right-hand actions. Views call this on mount and
// whenever their sub-view changes.
export function setTop({ title, count, sub = '', right = '', mobileSub = '' }) {
  const tb = document.getElementById('topbar');
  tb.innerHTML = `<div class="topbar-title">${esc(title)}${count != null ? `<span class="count">${count}</span>` : ''}</div>
    <div class="topbar-sub">${sub}</div>
    <div class="topbar-right">${right}
      <button class="btn btn-ghost btn-icon only-desktop" data-palette title="Search (⌘K)">${icon('search')}</button>
    </div>`;
  const ms = document.getElementById('subnav-mobile');
  ms.innerHTML = mobileSub || sub;
  ms.hidden = !(mobileSub || sub);
  const p = tb.querySelector('[data-palette]'); if (p) p.onclick = () => (globalKeys['mod+k'] || (() => {}))();
  return tb;
}
export const topEl = () => document.getElementById('topbar');
export const subEl = () => document.getElementById('subnav-mobile');

// A segmented control. items: [{id,label,n,hot}]. Returns html; the caller
// wires clicks via [data-seg] delegation with `onSeg`.
export function seg(items, active, name = 'seg') {
  return `<div class="seg" data-segname="${name}">${items.map(i =>
    `<button class="${i.id === active ? 'on' : ''}" data-seg="${attr(i.id)}">${esc(i.label)}${i.n != null ? `<span class="n ${i.hot ? 'hot' : ''}">${i.n}</span>` : ''}</button>`).join('')}</div>`;
}
export function chips(items, active, name = 'chip') {
  return `<div class="chips" data-chipname="${name}">${items.map(i =>
    `<button class="chip ${i.id === active ? 'on' : ''} ${i.hot ? 'hot' : ''}" data-chip="${attr(i.id)}">${esc(i.label)}${i.n != null ? `<span class="n">${i.n}</span>` : ''}</button>`).join('')}</div>`;
}
export function selectHtml(id, options, value, cls = '') {
  return `<span class="select ${cls}"><select id="${attr(id)}">${options.map(o =>
    `<option value="${attr(o.id)}"${String(o.id) === String(value) ? ' selected' : ''}>${esc(o.label)}</option>`).join('')}</select>${icon('chevronDown')}</span>`;
}
export const refreshBtn = (label = 'Refresh') => `<button class="btn btn-ghost btn-icon" data-refresh title="${attr(label)} (R)">${icon('refresh')}</button>`;

// Empty state + skeleton helpers
export function empty(text, sub = '', ic = 'inbox', quiet = false) {
  return `<div class="empty ${quiet ? 'quiet' : ''}">${icon(ic)}<div><b>${text}</b>${sub ? `<p>${sub}</p>` : ''}</div></div>`;
}
export const skeleton = (n = 3) => Array.from({ length: n }, () => '<div class="sk-card"><div class="sk"></div><div class="sk"></div><div class="sk"></div><div class="sk"></div></div>').join('');
export function errorBox(e, what = 'this view') {
  return `<div class="banner bad">${icon('alert')}<div><b>Could not load ${esc(what)}</b><span class="dim">${esc(e && e.message ? e.message : String(e))}</span></div></div>`;
}

// Command palette: jump anywhere, plus any commands the active view offers.
let paletteCommands = () => [];
export function setPaletteCommands(fn) { paletteCommands = fn || (() => []); }
bindGlobalKey('mod+k', () => {
  const nav = visibleViews().map(v => ({ label: `Go to ${v.title}`, icon: v.icon || DEPT_ICON[v.id], k: '', run: () => navigate(v.id), group: 'Navigate' }));
  const extra = paletteCommands() || [];
  const all = [...extra, ...nav, { label: 'Keyboard shortcuts', icon: 'keyboard', k: '?', run: showShortcuts, group: 'Help' }, { label: 'Log out', icon: 'logout', run: logout, group: 'Account' }];
  const d = dialog({ cls: 'palette', body: `<input type="text" placeholder="Jump to a view, ticket, lead…" autocomplete="off" spellcheck="false" /><div class="palette-list"></div>` });
  d.box.querySelector('.dialog-body').style.padding = '0';
  const input = d.q('input'), list = d.q('.palette-list');
  let sel = 0, shown = [];
  const draw = () => {
    const q = input.value.trim().toLowerCase();
    const score = c => { const l = c.label.toLowerCase(); if (!q) return 0; if (l === q || l === 'go to ' + q) return 0; if (l.startsWith(q) || l.startsWith('go to ' + q)) return 1; if (l.includes(q)) return 2; return 3; };
    shown = all.filter(c => !q || c.label.toLowerCase().includes(q) || (c.sub || '').toLowerCase().includes(q))
      .map((c, i) => [c, score(c), c.group === 'Navigate' ? 0 : 1, i]).sort((a, b) => a[1] - b[1] || a[2] - b[2] || a[3] - b[3]).map(x => x[0]).slice(0, 40);
    sel = Math.min(sel, Math.max(0, shown.length - 1));
    let group = null, h = '';
    shown.forEach((c, i) => {
      if (c.group !== group) { group = c.group; h += `<div class="palette-group">${esc(group || '')}</div>`; }
      h += `<button class="palette-item ${i === sel ? 'on' : ''}" data-i="${i}">${icon(c.icon || 'chevronRight')}<span style="min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(c.label)}${c.sub ? ` <span class="dim">· ${esc(c.sub)}</span>` : ''}</span>${c.k ? `<span class="k">${esc(c.k)}</span>` : ''}</button>`;
    });
    list.innerHTML = h || '<div class="empty quiet">Nothing matches.</div>';
  };
  const go = i => { const c = shown[i]; if (!c) return; d.close(); c.run(); };
  input.addEventListener('input', () => { sel = 0; draw(); });
  input.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown') { e.preventDefault(); sel = Math.min(sel + 1, shown.length - 1); draw(); list.querySelector('.on')?.scrollIntoView({ block: 'nearest' }); }
    if (e.key === 'ArrowUp') { e.preventDefault(); sel = Math.max(sel - 1, 0); draw(); list.querySelector('.on')?.scrollIntoView({ block: 'nearest' }); }
    if (e.key === 'Enter') { e.preventDefault(); go(sel); }
  });
  list.addEventListener('click', e => { const b = e.target.closest('[data-i]'); if (b) go(Number(b.dataset.i)); });
  draw();
});
bindGlobalKey('?', showShortcuts);
bindGlobalKey('g i', () => navigate('inbox'));
bindGlobalKey('g m', () => navigate('marketing'));
bindGlobalKey('g s', () => navigate('sales'));
bindGlobalKey('g e', () => navigate('eng'));
bindGlobalKey('g $', () => navigate('cost'));
bindGlobalKey('g c', () => navigate('config'));

// ── Polling helper for views ──────────────────────────────────────────────
// Live-ish refresh while the view is open. Skips a tick when the operator is
// mid-typing in the view (a re-render would eat their text), and stops when
// the tab is hidden — a dashboard nobody is looking at should not poll.
// Clipboard: the async API needs a secure context (localhost or https). Over a
// LAN address on a phone it is absent, so fall back to a selected textarea.
export async function copyText(text) {
  try { if (navigator.clipboard && window.isSecureContext) { await navigator.clipboard.writeText(text); return true; } } catch (e) {}
  try {
    const ta = document.createElement('textarea'); ta.value = text; ta.setAttribute('readonly', '');
    ta.style.cssText = 'position:fixed;top:0;left:0;width:1px;height:1px;opacity:0';
    document.body.appendChild(ta); ta.focus(); ta.select();
    const ok = document.execCommand('copy'); ta.remove(); return ok;
  } catch (e) { return false; }
}

export function makePoller(fn, ms) {
  let t = null;
  const tick = () => { if (document.hidden) return; if (isTyping() || dialogOpen()) return; fn(); };
  return { start() { if (!t) t = setInterval(tick, ms); }, stop() { if (t) { clearInterval(t); t = null; } } };
}
