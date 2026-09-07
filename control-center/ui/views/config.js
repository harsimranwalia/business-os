// Config — your own credentials (an admin can open a partner's). Secrets go
// up but never come back: the server returns `_set` plus a hint, so a blank
// secret field means "leave it alone" — clearing one is the ✕, deliberately.
import { api, setTop, refreshBtn, esc, attr, icon, skeleton, dialog, confirm, toast, fail, me, isAdmin, setViewKeys, errorBox, selectHtml, navigate } from '../core.js';

let root, data = null, who = '', users = null;
const forSelf = () => !who || who === me.email;
const SOURCE_FIELDS = ['source', 'brand_id', 'pg_dsn', 'crm_url', 'crm_api_key', 'ghl_location_id', 'ghl_api_key'];

function top() {
  const list = users && users.length > 1 ? users.map(u => ({ id: u.email, label: u.name || u.email })) : null;
  setTop({ title: 'Config', right: (list ? selectHtml('cfg-who', list, who || me.email) : '') + refreshBtn() });
  const sel = document.getElementById('cfg-who'); if (sel) sel.onchange = () => { who = sel.value === me.email ? '' : sel.value; navigate('config', who ? { who } : {}); };
  document.querySelector('[data-refresh]').onclick = load;
}
const badge = (id, on, label) => `<span class="set-line" id="${id}" style="margin:0">${on ? '✓ ' + label : ''}</span>`;
function secret(id, label, hint) {
  const set = data[id + '_set'];
  return `<dt><label for="cfg-${id}">${esc(label)}</label></dt><dd>
    <div class="secret"><input type="password" id="cfg-${id}" autocomplete="new-password" placeholder="${set ? 'unchanged' : 'not set'}" />${set ? `<button class="btn btn-icon btn-bad" title="Clear this value" data-clear="${id}">${icon('x')}</button>` : ''}</div>
    ${set ? `<div class="set-line">set · ${esc(data[id + '_hint'])}</div>` : ''}<div class="hint">${hint}</div></dd>`;
}
function render() {
  const el = root.querySelector('#config'); if (!el) return;
  if (!data) { el.innerHTML = skeleton(3); return; }
  const d = data, source = d.customer_source || '';
  const show = s => `style="display:${source === s ? 'contents' : 'none'}"`;
  el.innerHTML = `
    ${(d.missing || []).length ? `<div class="banner warn">${icon('alert')}<div><b>Not usable yet</b>Still missing: ${esc(d.missing.join(', '))}. SMS campaigns need the gateway; Smart reactivation needs all of it.</div></div>` : `<div class="banner info">${icon('check')}<div><b>Ready</b>Everything Smart reactivation and campaigns need is in place.</div></div>`}
    ${!forSelf() ? `<div class="banner info">${icon('users')}<div>You are editing <b>${esc(who)}</b>'s configuration as an admin.</div></div>` : ''}
    <div class="cfg-section"><h2>Business</h2><div class="note">Context for anything a model drafts on your behalf — right now, that's Smart reactivation's messages.</div>
      <dl class="kv"><dt><label for="cfg-business_blurb">About this business</label></dt><dd><textarea id="cfg-business_blurb" rows="3" placeholder="What you sell, the tone you write in, anything worth knowing before someone drafts a message in your voice.">${esc(d.business_blurb || '')}</textarea></dd></dl></div>
    <div class="cfg-section"><h2>Claude</h2><div class="note">Agent work runs on your own account, not the host's. Generate a token with <code>claude setup-token</code> on any machine with a browser; it lasts a year.</div>
      <dl class="kv">${secret('claude_oauth_token', 'OAuth token', 'Required for Smart reactivation. Without it, nothing that needs a model runs for you.')}</dl></div>
    <div class="cfg-section"><h2>SMS server ${badge('cfg-sms-test-badge', d.sms_tested_ok, 'Working')}</h2><div class="note">An HTTP gateway. The control center authenticates with HTTP Basic Auth and POSTs JSON: <code>{"textMessage":{"text":…},"phoneNumbers":[…]}</code> — one request can carry many numbers when they all get the same text.</div>
      <dl class="kv">
        <dt><label for="cfg-sms_url">Server URL</label></dt><dd><input type="text" id="cfg-sms_url" class="mono" value="${attr(d.sms_url || '')}" placeholder="https://sms.example.com/send" /><div class="hint">Must start with http:// or https://.</div></dd>
        <dt><label for="cfg-sms_username">Username</label></dt><dd><input type="text" id="cfg-sms_username" autocomplete="off" value="${attr(d.sms_username || '')}" /></dd>
        ${secret('sms_password', 'Password', 'Stored server-side; never sent back to this page.')}
        ${d.sms_url ? `<dt>Test server</dt><dd><div class="inline-row"><input type="text" id="cfg-sms-test-phone" class="mono" placeholder="+15551234567" style="max-width:190px" /><button class="btn" id="cfg-sms-test">Send test</button>${me.phone && forSelf() ? `<button class="btn" id="cfg-sms-test-me">Send to me</button>` : ''}</div><div class="hint" id="cfg-sms-test-out">Tests the saved configuration above, not unsaved edits.</div></dd>` : ''}
      </dl></div>
    <div class="cfg-section"><h2>Customer database ${badge('cfg-source-test-badge', d.source_tested_ok, 'Connected')}</h2><div class="note">Where campaign segments and reactivation candidates are read from.</div>
      <dl class="kv">
        <dt><label for="cfg-source">Source</label></dt><dd>${selectHtml('cfg-source', [{ id: '', label: '— pick one —' }, { id: 'aiorders', label: 'AIOrders' }, { id: 'crm', label: 'CRM (Twenty)' }, { id: 'ghl', label: 'HighLevel (GoHighLevel)' }], source, 'block')}
          <div class="hint">AIOrders reads your brand's customers directly and gives you order-based segments. The CRM and HighLevel carry no order history, so they offer only date-based ones.</div></dd>
        <div id="cfg-aiorders" ${show('aiorders')}>
          <dt><label for="cfg-brand_id">Brand id</label></dt><dd><input type="text" id="cfg-brand_id" class="mono" autocomplete="off" value="${attr(d.brand_id || '')}" placeholder="uuid" /></dd>
          ${secret('pg_dsn', 'Database connection', 'Postgres/Supabase connection string, e.g. postgresql://user:pass@host:5432/db. Needs the psycopg driver installed on the machine running this server.')}</div>
        <div id="cfg-crm" ${show('crm')}>
          <dt><label for="cfg-crm_url">Twenty URL</label></dt><dd><input type="text" id="cfg-crm_url" class="mono" autocomplete="off" value="${attr(d.crm_url || '')}" placeholder="https://crm.example.com" /><div class="hint">Your Twenty workspace's base URL — the GraphQL endpoint is derived from it.</div></dd>
          ${secret('crm_api_key', 'API key', 'From Twenty: Settings → APIs & Webhooks → generate a key.')}</div>
        <div id="cfg-ghl" ${show('ghl')}>
          <dt><label for="cfg-ghl_location_id">Location id</label></dt><dd><input type="text" id="cfg-ghl_location_id" class="mono" autocomplete="off" value="${attr(d.ghl_location_id || '')}" placeholder="e.g. C2QujeCh8ZnC7al2InWR" /><div class="hint">The sub-account the contacts live in — HighLevel shows it under Settings → Business Profile, and it is also in the dashboard URL.</div></dd>
          ${secret('ghl_api_key', 'API token', 'A Private Integration token with the contacts read scope, from HighLevel: Settings → Private Integrations. Sent as a bearer token.')}</div>
        <div id="cfg-source-test" style="display:${source ? 'contents' : 'none'}"><dt>Test configuration</dt><dd><button class="btn" id="cfg-source-test-btn">Test configuration</button><div class="hint" id="cfg-source-test-out">Reads a couple of real customers back from the saved configuration above, not unsaved edits.</div></dd></div>
      </dl></div>
    <div class="savebar"><button class="btn btn-primary" id="cfg-save">${icon('check')}Save configuration</button><span class="msg-ok" id="cfg-saved"></span><span class="msg-bad" id="cfg-err"></span></div>`;
  el.querySelector('#cfg-source').onchange = onSourceChange;
  el.querySelector('#cfg-save').onclick = () => postConfig(payload());
  el.querySelectorAll('[data-clear]').forEach(b => b.onclick = async () => { if (await confirm({ title: 'Clear this value?', ok: 'Clear', danger: true })) postConfig(payload({ clear: [b.dataset.clear] })); });
  const st = el.querySelector('#cfg-sms-test'); if (st) st.onclick = () => testSms();
  const sm = el.querySelector('#cfg-sms-test-me'); if (sm) sm.onclick = () => testSms(me.phone);
  const ts = el.querySelector('#cfg-source-test-btn'); if (ts) ts.onclick = testSource;
  SOURCE_FIELDS.forEach(id => { const f = el.querySelector('#cfg-' + id); if (f && id !== 'source') f.addEventListener('input', untested); });
}
function onSourceChange() {
  const v = root.querySelector('#cfg-source').value;
  ['aiorders', 'crm', 'ghl'].forEach(s => root.querySelector('#cfg-' + s).style.display = v === s ? 'contents' : 'none');
  root.querySelector('#cfg-source-test').style.display = v ? 'contents' : 'none';
  untested();
}
function untested() {
  const b = root.querySelector('#cfg-source-test-badge'); if (!b || !b.textContent) return;
  b.textContent = ''; const out = root.querySelector('#cfg-source-test-out'); if (out) out.textContent = 'Configuration changed — save it, then test again.';
  if (data) data.source_tested_ok = false;
}
const val = id => (root.querySelector('#cfg-' + id)?.value || '').trim();
function payload(extra) {
  return Object.assign({ email: who || me.email, business_blurb: val('business_blurb'), sms_url: val('sms_url'), sms_username: val('sms_username'), sms_password: val('sms_password'),
    claude_oauth_token: val('claude_oauth_token'), customer_source: val('source'), brand_id: val('brand_id'), pg_dsn: val('pg_dsn'), crm_url: val('crm_url'), crm_api_key: val('crm_api_key'),
    ghl_location_id: val('ghl_location_id'), ghl_api_key: val('ghl_api_key') }, extra || {});
}
async function postConfig(p) {
  const err = root.querySelector('#cfg-err'), saved = root.querySelector('#cfg-saved'); err.textContent = ''; saved.textContent = '';
  try { data = await api.post('/api/config', p); render(); root.querySelector('#cfg-saved').textContent = 'Saved.'; toast('Configuration saved.', 'ok'); window.dispatchEvent(new CustomEvent('cc:changed')); }
  catch (e) { root.querySelector('#cfg-err').textContent = e.message; }
}
async function testSms(phoneOverride) {
  const input = root.querySelector('#cfg-sms-test-phone'), out = root.querySelector('#cfg-sms-test-out'), badge = root.querySelector('#cfg-sms-test-badge');
  const phone = (phoneOverride || input.value || '').trim(); if (!phone) { input.focus(); return; }
  out.textContent = 'Sending…';
  try { const d = await api.post('/api/config/test-sms', { email: who || me.email, phone }); if (d.ok) { out.textContent = 'Sent — check the phone.'; badge.textContent = '✓ Working'; data.sms_tested_ok = true; } else out.textContent = 'Gateway said: ' + (d.detail || 'failed'); }
  catch (e) { out.textContent = e.message; }
}
async function testSource() {
  const btn = root.querySelector('#cfg-source-test-btn'), out = root.querySelector('#cfg-source-test-out'), badge = root.querySelector('#cfg-source-test-badge');
  btn.disabled = true; badge.textContent = ''; out.textContent = 'Reading…';
  try {
    const d = await api.post('/api/config/test-source', { email: who || me.email }); btn.disabled = false;
    if (!d.ok) { out.textContent = d.detail || 'Connection failed'; return; }
    badge.textContent = '✓ Connected'; data.source_tested_ok = true;
    out.innerHTML = `${esc(d.detail)} — ${d.count} customer${d.count === 1 ? '' : 's'} with a phone number.` + ((d.sample || []).length ? `<div class="sample">${d.sample.map(c => `<div><b>${esc(c.name)}</b> · ${esc(c.phone)}</div>`).join('')}</div>` : '');
  } catch (e) { btn.disabled = false; out.textContent = e.message; }
}
async function load() {
  try {
    if (isAdmin() && !users) { try { users = (await api.get('/api/partners')).users || []; } catch (e) { users = []; } }
    top();
    data = await api.get('/api/config', who && who !== me.email ? { email: who } : {}); render();
  } catch (e) { const el = root.querySelector('#config'); if (el) el.innerHTML = errorBox(e, 'configuration'); }
}
export default {
  id: 'config', title: 'Config', short: 'Config', icon: 'settings', section: 'system',
  async mount(r, route) { root = r; data = null; who = (route.params && route.params.who) || ''; root.innerHTML = `<div class="content-inner narrow" id="config"></div>`; top(); render(); await load(); setViewKeys({ r: load }); },
  update(route) { who = (route.params && route.params.who) || ''; data = null; render(); load(); },
};
