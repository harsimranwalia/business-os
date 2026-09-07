// Partners — the user store (admin only). Who exists, what role they hold,
// which departments and businesses each partner may work on. Changes take
// effect on the partner's very next request.
import { api, setTop, refreshBtn, esc, attr, icon, empty, skeleton, dialog, confirm, toast, fail, setViewKeys, errorBox, selectHtml } from '../core.js';
import { tag } from './cards.js';

let root, data = null;
const instLabel = id => { const i = (data.instances || []).find(x => x.id === id); return i ? i.label : id; };
const deptLabel = id => { const d = (data.departments || []).find(x => x.id === id); return d ? d.label : id; };

function top() {
  setTop({ title: 'Partners', count: data ? data.users.length : null, right: `<button class="btn btn-primary btn-sm" id="user-add">${icon('plus')}<span class="only-desktop">Add user</span></button>` + refreshBtn() });
  document.getElementById('user-add').onclick = () => userDialog(null);
  document.querySelector('[data-refresh]').onclick = load;
}
function render() {
  const el = root.querySelector('#partners'); if (!el) return;
  if (!data) { el.innerHTML = skeleton(3); return; }
  const users = data.users || [];
  if (!users.length) { el.innerHTML = empty('No users', '', 'users'); return; }
  el.innerHTML = `<div class="rows"><div class="row head"><div>User</div><div>Phone</div><div>Departments</div><div>Instances</div><div>Role</div><div>Last sign-in</div><div></div></div>
    ${users.map(u => {
      const admin = u.role === 'admin';
      const depts = admin ? '<span class="dim">all</span>' : (u.departments.length ? `<span class="chipset">${u.departments.map(d => tag(deptLabel(d))).join('')}</span>` : '<span class="dim">none assigned</span>');
      const insts = admin ? '<span class="dim">all</span>' : (!u.departments.includes('eng') ? '<span class="dim">n/a — no Engineering</span>' : (u.instances.length ? `<span class="chipset">${u.instances.map(i => tag(instLabel(i))).join('')}</span>` : '<span class="dim">none assigned</span>'));
      return `<div class="row">
        <div class="who-cell"><div class="who">${esc(u.name || u.email)}</div><div class="sub">${esc(u.name ? u.email : '')}${u.pin_set ? '' : ' · no PIN set'}</div>${u.role === 'partner' && !u.config_ready ? '<div class="sub warn">configuration incomplete</div>' : ''}</div>
        <div class="cell mono lbl" data-l="Phone">${esc(u.phone) || '—'}</div>
        <div class="cell lbl" data-l="Departments">${depts}</div>
        <div class="cell lbl" data-l="Instances">${insts}</div>
        <div class="cell lbl" data-l="Role"><span class="pill ${admin ? 'approved' : ''}">${esc(u.role)}</span></div>
        <div class="cell mono lbl" data-l="Last sign-in">${esc((u.last_login || '').slice(0, 10)) || 'never'}</div>
        <div class="edit-cell"><button class="btn btn-sm" data-edit="${attr(u.email)}">Edit</button></div>
      </div>`;
    }).join('')}</div>`;
  el.querySelectorAll('[data-edit]').forEach(b => b.onclick = () => userDialog(b.dataset.edit));
}
function picker(items, selected, key) {
  const sel = new Set(selected || []);
  return `<div class="days" data-picker="${key}">${items.map(i => `<button type="button" class="day ${sel.has(i.id) ? 'on' : ''}" data-v="${attr(i.id)}">${esc(i.label)}</button>`).join('') || '<span class="dim">No business instances exist yet.</span>'}</div>`;
}
function userDialog(email) {
  const u = email ? data.users.find(x => x.email === email) : null;
  const d = dialog({
    title: u ? 'Edit user' : 'Add user', sub: u ? esc(u.email) : 'A partner sees only the departments and businesses assigned here.',
    body: `<div class="form-grid">
      <div class="field full"><label for="um-email">Email</label><input type="email" id="um-email" value="${attr(u ? u.email : '')}" ${u ? 'disabled' : ''} autocomplete="off" /></div>
      <div class="field"><label for="um-name">Name</label><input id="um-name" value="${attr(u ? u.name : '')}" autocomplete="off" /></div>
      <div class="field"><label for="um-phone">Phone</label><input id="um-phone" class="mono" value="${attr(u ? u.phone : '')}" autocomplete="off" /></div>
      <div class="field"><label for="um-pin">PIN <small>${u ? 'leave blank to keep the current one' : '4 to 12 digits'}</small></label><input id="um-pin" class="mono" inputmode="numeric" maxlength="12" autocomplete="off" /></div>
      <div class="field"><label for="um-role">Role</label>${selectHtml('um-role', [{ id: 'partner', label: 'Partner' }, { id: 'admin', label: 'Admin' }], u ? u.role : 'partner', 'block')}</div>
      <div class="field full" id="um-dept-wrap"><label>Departments this partner may work on</label>${picker(data.departments, u ? u.departments : data.departments.map(x => x.id), 'dept')}<div class="hint">Only these tabs show up for them. An admin has no restrictions.</div></div>
      <div class="field full" id="um-inst-wrap"><label>Instances this partner may work on</label>${picker(data.instances, u ? u.instances : [], 'inst')}<div class="hint">Only matters for Engineering — a business-specific ticket board. Other departments show every business the partner is not otherwise kept out of.</div></div>
      <div class="full msg-bad" id="um-err"></div></div>`,
    foot: `${u ? `<button class="btn btn-bad" data-del>Delete</button>` : ''}<span class="spacer"></span><button class="btn" data-x>Cancel</button><button class="btn btn-primary" data-ok>Save</button>`,
  });
  const picked = key => Array.from(d.el.querySelectorAll(`[data-picker="${key}"] .day.on`)).map(b => b.dataset.v);
  const sync = () => { const admin = d.q('#um-role').value === 'admin'; d.q('#um-dept-wrap').hidden = admin; d.q('#um-inst-wrap').hidden = admin || !picked('dept').includes('eng'); };
  d.el.querySelectorAll('.day').forEach(b => b.onclick = () => { b.classList.toggle('on'); sync(); });
  d.q('#um-role').onchange = sync; sync();
  d.q('[data-x]').onclick = d.close;
  d.q('[data-ok]').onclick = async () => {
    const err = d.q('#um-err'), btn = d.q('[data-ok]'); err.textContent = ''; btn.disabled = true;
    try {
      await api.post(u ? '/api/partners/update' : '/api/partners/create', { email: d.q('#um-email').value.trim().toLowerCase(), name: d.q('#um-name').value.trim(), phone: d.q('#um-phone').value.trim(), pin: d.q('#um-pin').value.trim(), role: d.q('#um-role').value, departments: picked('dept'), instances: picked('inst') });
      d.close(); toast(u ? 'Saved.' : 'User added.', 'ok'); load();
    } catch (e) { err.textContent = e.message; btn.disabled = false; }
  };
  const del = d.q('[data-del]');
  if (del) del.onclick = async () => {
    if (!(await confirm({ title: `Delete ${u.email}?`, body: 'Their configuration — Claude token, SMS server, customer source — is deleted with them. Campaigns they created stay on the board.', ok: 'Delete', danger: true }))) return;
    try { await api.post('/api/partners/delete', { email: u.email }); d.close(); toast('Deleted.', 'ok'); load(); } catch (e) { d.q('#um-err').textContent = e.message; }
  };
}
async function load() {
  try { data = await api.get('/api/partners'); top(); render(); }
  catch (e) { const el = root.querySelector('#partners'); if (el) el.innerHTML = errorBox(e, 'users'); }
}
export default {
  id: 'partners', title: 'Partners', short: 'Partners', icon: 'users', section: 'system', adminOnly: true,
  async mount(r) { root = r; data = null; root.innerHTML = `<div class="content-inner" id="partners"></div>`; top(); render(); await load(); setViewKeys({ r: load, n: () => data && userDialog(null) }); },
};
