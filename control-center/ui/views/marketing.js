// Marketing — per business instance. Decide is the department's approval
// gate (the only recurring human step); Content is the library; Reddit is the
// Twenty CRM community pipeline; SMS is campaigns + smart reactivation;
// Settings is channel config. A channel filter narrows Decide / Content /
// Settings — Reddit and SMS are channels of their own with their own tabs.
import { api, setTop, seg, chips, selectHtml, refreshBtn, esc, attr, icon, empty, skeleton, prefs, navigate, toast, fail, cssId, isAdmin, dialog, confirm, setViewKeys, makePoller, errorBox, plural, fmtWhen, setPaletteCommands } from '../core.js';
import { mktPieceCard, redditCard, smsCampaignCard, smsRunCard, bindActions, afterRender, tag, pill, segLabel } from './cards.js';

const PHASE = { drafting: 'drafting', awaiting: 'awaiting your approval', queued: 'approved, waiting to ship', shipped: 'shipped' };
const REACT_MODES = {
  review: { label: 'Preview each message, then I approve', button: 'Draft messages for review', note: 'The run stops with every message, and the number it is bound for, on screen. Nothing sends until you press Send.' },
  auto: { label: 'Send automatically, no review', button: 'Run and send now', note: 'Nobody reads them first. The cap, the cooldown and the pause switch are the only things standing in for you.' },
};

let root, sub = 'decide', params = {}, poller = null, loading = false;
let instance = prefs.get('mkt-instance', ''), channel = prefs.get('mkt-channel', '');
let mkt = null, content = null, contentFilter = '', reddit = null, redditFilter = 'PENDING', settings = null, sms = null;
let smsTab = prefs.get('sms-view', 'campaigns'), smsOwner = prefs.get('sms-owner', ''), reactMode = prefs.get('sms-react-mode', 'review');
let settingsBusy = false;

const q = extra => Object.assign({ instance }, extra || {});
const inChannel = x => !channel || x.channel === channel;

function top() {
  const due = mkt && !mkt.empty ? (mkt.due || []).filter(inChannel).length : null;
  const rp = reddit && !reddit.error ? reddit.length : null;
  const smsN = sms && !sms.empty ? ((sms.campaigns || []).filter(c => c.status === 'draft' || c.status === 'approved').length + (sms.reactivations || []).reduce((n, r) => n + (r.messages || []).filter(m => (m.state || (m.sent ? 'sent' : 'failed')) === 'pending').length, 0)) : null;
  const s = seg([
    { id: 'decide', label: 'Decide', n: due, hot: !!due }, { id: 'content', label: 'Content' },
    { id: 'reddit', label: 'Reddit', n: rp, hot: !!rp }, { id: 'sms', label: 'SMS', n: smsN, hot: !!smsN }, { id: 'settings', label: 'Settings' }], sub);
  const insts = (mkt && mkt.instances && mkt.instances.length ? mkt.instances : (sms && sms.instances)) || [];
  setTop({ title: 'Marketing', sub: s, right: (insts.length > 1 ? selectHtml('mkt-inst', insts, instance) : '') + refreshBtn() });
  document.querySelectorAll('[data-seg]').forEach(b => b.onclick = () => navigate('marketing/' + b.dataset.seg));
  const sel = document.getElementById('mkt-inst'); if (sel) sel.onchange = () => { instance = sel.value; prefs.set('mkt-instance', instance); content = settings = sms = null; smsOwner = ''; prefs.set('sms-owner', ''); mkt = null; render(); load(); };
  document.querySelector('[data-refresh]').onclick = () => load(true);
}

function channelChips() {
  if (!mkt || mkt.empty) return '';
  const items = [{ id: '', label: 'All channels' }].concat((mkt.channels || []).map(c => ({ id: c.id, label: c.label + (c.enabled ? '' : ' (off)') })));
  return `<div style="margin-bottom:20px">${chips(items, channel, 'chan')}</div>`;
}

// ── Decide ────────────────────────────────────────────────────────────────
function decideHtml() {
  const d = mkt;
  if (d.empty) return empty(d.empty, '', 'megaphone');
  const due = d.due.filter(inChannel), queued = d.queued.filter(inChannel);
  const chan = channel ? d.channels.find(c => c.id === channel) : null;
  let h = channelChips();
  h += `<div class="stats">
    <div class="stat ${due.length ? 'hot' : ''}"><b>${due.length}</b><span>due for approval</span></div>
    <div class="stat"><b>${queued.length}</b><span>approved, waiting to ship</span></div>
    ${chan ? `<div class="stat compact"><b>${esc(chan.next_slot || '—')}</b><span>next ${esc(chan.label)} slot</span></div>`
           : `<div class="stat"><b>${d.stats.shipped_30d}</b><span>shipped in 30 days</span></div><div class="stat"><b>${d.stats.channels_live}</b><span>channels live</span></div>`}
  </div>`;
  h += `<section class="section"><div class="section-h"><h2>Due for your approval</h2><span class="n ${due.length ? 'hot' : ''}">${due.length}</span></div>`;
  if (!due.length) h += `<div class="empty">${icon('check')}<div><b>Nothing needs you${channel ? ' on this channel' : ''}</b><p>Anything else written is dated further out — approve those when they come due, not now.</p></div></div>`;
  h += `<div class="stack">${due.map(p => mktPieceCard(p, { gate: true, body: true, instance: d.instance, channels: d.channels, today: d.today, meta: 'nothing publishes without this' })).join('')}</div>`;
  if (!channel && d.later_count) h += `<div class="quiet-line">${d.later_count} more written and dated beyond the next ${d.window_days} days${d.later_first ? `, starting ${esc(d.later_first)}` : ''}. They are under Content when you want them.</div>`;
  h += '</section>';
  if (queued.length) {
    h += `<section class="section"><div class="section-h"><h2>Approved, shipping itself</h2><span class="n">${queued.length}</span></div><div class="stack">${queued.slice(0, 6).map(p => mktPieceCard(p, { channels: d.channels, today: d.today, meta: "goes out on its channel's next slot" })).join('')}</div></section>`;
  }
  h += `<section class="section"><div class="section-h"><h2>Give the department something to write</h2></div>
    <div class="composer">
      <input id="mkt-topic" placeholder="A topic worth a piece" />
      <textarea id="mkt-topic-note" rows="2" placeholder="Why it fits, or the real story behind it (optional)"></textarea>
      <div class="foot"><button class="btn btn-primary" id="mkt-topic-btn">${icon('plus')}Add to the topic bank</button>
        <span class="hint" id="mkt-topic-out">The CMO reads the bank on its next planning run and picks the archetype — you don't have to classify it.</span></div>
    </div></section>`;
  return h;
}
async function addTopic() {
  const t = root.querySelector('#mkt-topic'), n = root.querySelector('#mkt-topic-note'), out = root.querySelector('#mkt-topic-out');
  if (!t.value.trim()) { t.focus(); return; }
  try {
    await api.post('/api/mkt/topic', { topic: t.value, note: n.value, instance });
    t.value = ''; n.value = '';
    out.textContent = 'In the bank. The CMO picks it up on its next planning run — nothing else for you to do with it.';
    toast('Added to the topic bank.', 'ok');
  } catch (e) { fail(e); }
}

// ── Content ───────────────────────────────────────────────────────────────
function contentHtml() {
  if (!content) return channelChips() + skeleton(3);
  if (content.empty) return empty(content.empty, '', 'megaphone');
  const items = (content.items || []).filter(inChannel).filter(i => !contentFilter || i.phase === contentFilter);
  const count = ph => (content.items || []).filter(inChannel).filter(i => !ph || i.phase === ph).length;
  let h = channelChips();
  h += `<div style="margin-bottom:18px">${chips([['', 'All'], ['drafting', 'Drafting'], ['awaiting', 'Awaiting'], ['queued', 'Approved'], ['shipped', 'Shipped']].map(([id, label]) => ({ id, label, n: count(id) })), contentFilter, 'phase')}</div>`;
  if (!items.length) return h + empty('Nothing here', '', 'megaphone', true);
  h += `<div class="stack">${items.map(p => mktPieceCard(p, { body: true, channels: mkt && mkt.channels, today: mkt && mkt.today, meta: PHASE[p.phase] || p.phase })).join('')}</div>`;
  return h;
}

// ── Reddit ────────────────────────────────────────────────────────────────
function redditHtml() {
  let h = `<div style="margin-bottom:18px">${chips([['PENDING', 'Pending'], ['APPROVED', 'Approved'], ['POSTED', 'Posted'], ['DISCARDED', 'Discarded'], ['FAILED', 'Failed'], ['', 'All']].map(([id, label]) => ({ id, label })), redditFilter, 'rstatus')}</div>`;
  if (!reddit) return h + skeleton(2);
  if (reddit.error) return h + `<div class="banner bad">${icon('alert')}<div><b>Could not load Marketing Content from Twenty</b><span class="dim">${esc(reddit.error.message || String(reddit.error))} — check TWENTY_BASE_URL / TWENTY_API_KEY in .env.</span></div></div>`;
  if (!reddit.length) return h + `<div class="empty">${icon('reddit')}<div><b>Nothing ${redditFilter ? redditFilter.toLowerCase() : 'here'}</b>${redditFilter === 'PENDING' ? '<p>The community builder drafts replies after each listener sweep; they land here for you to approve.</p>' : ''}</div></div>`;
  return h + `<div class="stack">${reddit.map(it => redditCard(it)).join('')}</div>`;
}

// ── SMS ───────────────────────────────────────────────────────────────────
function smsBanner() {
  let h = '';
  if (sms.quiet_mode) h += `<div class="banner warn">${icon('pause')}<div><b>Paused</b>MODE is set in .env — nothing sends until it is cleared. Drafting and approving still work.</div></div>`;
  const missing = sms.config_missing || [];
  if (missing.length) h += `<div class="banner warn">${icon('alert')}<div><b>Configuration incomplete</b>Missing: ${esc(missing.join(', '))}.${!sms.config_owner_is_self && sms.config_owner ? ` This channel runs on <strong>${esc(sms.config_owner)}</strong>'s configuration.` : ''}
    <div class="actions"><button class="btn btn-sm" id="sms-open-config">Open Config ${icon('chevronRight', 'ic-sm')}</button></div></div></div>`;
  return h;
}
function smsHtml() {
  if (!sms) return skeleton(2);
  if (sms.empty) return empty(sms.empty, '', 'message');
  const owners = sms.config_owners || [];
  let h = `<div class="inline-row" style="justify-content:space-between;margin-bottom:18px;gap:12px">
    ${seg([{ id: 'campaigns', label: 'Campaigns' }, { id: 'reactivation', label: 'Smart reactivation' }], smsTab, 'smstab')}
    ${owners.length > 1 ? `<span class="inline-row"><span class="dim" style="font-size:12.5px">Workspace</span>${selectHtml('sms-owner', owners.map(o => ({ id: o, label: o })), sms.config_owner, 'sm')}</span>` : ''}
  </div>`;
  h += smsBanner();
  h += smsTab === 'reactivation' ? reactivationHtml() : campaignsHtml();
  return h;
}
function campaignsHtml() {
  const noSource = !sms.customer_source;
  const SRC = { aiorders: 'AIOrders', crm: 'CRM', ghl: 'HighLevel' };
  let h = `<div class="inline-row" style="margin-bottom:16px"><button class="btn btn-primary" id="sms-new" ${noSource ? 'disabled' : ''}>${icon('plus')}New campaign</button>
    <span class="dim" style="font-size:12.5px">${noSource ? 'Pick a customer database source in Config before writing a campaign.' : `Segments read from your ${esc(SRC[sms.customer_source] || sms.customer_source)} customer database.`}</span></div>`;
  const items = sms.campaigns || [];
  if (!items.length) return h + `<div class="empty">${icon('message')}<div><b>No campaigns yet</b><p>A campaign is copy you write and approve; nothing sends until you do.</p></div></div>`;
  return h + `<div class="stack">${items.map(c => smsCampaignCard(c, sms)).join('')}</div>`;
}
function reactivationHtml() {
  const r = sms.reactivation || {};
  const mode = REACT_MODES[reactMode] ? reactMode : 'review';
  let h = `<div class="section-note" style="max-width:720px">Smart reactivation takes no segment — it reads the lapsed end of your customer database itself. It needs an offer each run: the one piece of copy a human provides. From your business blurb (Config) and that offer, it runs a pass on <b>your</b> Claude token to choose who is worth reaching and write to each of them. Guardrails either way: at most <b>${r.cap}</b> people per run, nobody texted twice within <b>${r.cooldown_days} days</b>, and the run stops entirely while the global pause switch is set. Phone numbers are never sent to the model.</div>`;
  h += `<div class="composer" style="margin-bottom:24px">
    <div class="form-grid">
      <div class="field full"><label for="react-offer">Offer for this run</label><textarea id="react-offer" rows="2" placeholder="e.g. 20% off any order over $30, this weekend only"></textarea></div>
      <div class="field full"><label for="react-mode">Once the messages are written</label>${selectHtml('react-mode', Object.entries(REACT_MODES).map(([k, v]) => ({ id: k, label: v.label })), mode, 'block')}<div class="hint" id="react-mode-note">${esc(REACT_MODES[mode].note)}</div></div>
    </div>
    <div class="foot"><button class="btn ${mode === 'auto' ? 'btn-warn' : 'btn-primary'}" id="react-btn" disabled>${icon(mode === 'auto' ? 'send' : 'sparkles')}<span>${esc(REACT_MODES[mode].button)}</span></button><span class="hint" id="react-status"></span></div>
  </div>`;
  const runs = sms.reactivations || [];
  if (!runs.length) return h + `<div class="empty">${icon('sparkles')}<div><b>No reactivation runs yet</b></div></div>`;
  return h + `<div class="stack">${runs.map(run => smsRunCard(run, sms)).join('')}</div>`;
}
function wireSms(el) {
  el.querySelectorAll('[data-segname="smstab"] [data-seg]').forEach(b => b.onclick = () => { smsTab = b.dataset.seg; prefs.set('sms-view', smsTab); render(); });
  const own = el.querySelector('#sms-owner'); if (own) own.onchange = () => { smsOwner = own.value; prefs.set('sms-owner', smsOwner); sms = null; render(); loadSms(); };
  const oc = el.querySelector('#sms-open-config'); if (oc) oc.onclick = () => navigate('config', isAdmin() && sms.config_owner && !sms.config_owner_is_self ? { who: sms.config_owner } : {});
  const nw = el.querySelector('#sms-new'); if (nw) nw.onclick = () => campaignDialog(null);
  const offer = el.querySelector('#react-offer'), btn = el.querySelector('#react-btn'), modeSel = el.querySelector('#react-mode');
  const blocked = !!((sms.config_missing || []).length || sms.quiet_mode);
  if (offer) offer.oninput = () => { btn.disabled = blocked || !offer.value.trim(); };
  if (modeSel) modeSel.onchange = () => { reactMode = REACT_MODES[modeSel.value] ? modeSel.value : 'review'; prefs.set('sms-react-mode', reactMode); const v = offer.value; render(); root.querySelector('#react-offer').value = v; root.querySelector('#react-btn').disabled = blocked || !v.trim(); };
  if (btn) btn.onclick = runReactivation;
}
async function runReactivation() {
  const offer = (root.querySelector('#react-offer').value || '').trim();
  if (!offer) return;
  const mode = REACT_MODES[reactMode] ? reactMode : 'review';
  if (mode === 'auto' && !(await confirm({ title: 'Run smart reactivation and send now?', body: 'Messages go out automatically — nobody reviews them first. The per-run cap and the 30-day cooldown still apply.', ok: 'Run and send', danger: true }))) return;
  const btn = root.querySelector('#react-btn'), status = root.querySelector('#react-status');
  btn.disabled = true; status.textContent = (mode === 'auto' ? 'Running' : 'Drafting') + ' — the Claude pass takes a minute or two…';
  try {
    await api.post('/api/sms/reactivate', { instance, offer, mode, config_owner: smsOwner || undefined });
    toast(mode === 'auto' ? 'Run finished.' : 'Drafts are ready to review.', 'ok');
    sms = null; render(); await loadSms();
  } catch (e) { status.textContent = ''; btn.disabled = false; fail(e); }
}
export function campaignDialog(id) {
  const c = id ? (sms.campaigns || []).find(x => x.id === id) : null;
  const max = sms.max_chars || 320;
  const d = dialog({
    title: c ? 'Edit campaign' : 'New campaign',
    sub: c && c.status === 'approved' ? 'Editing an approved campaign sends it back to draft — the gate is on the words, not the record.' : 'Drafts go out only after you approve them.',
    body: `<div class="form-grid">
      <div class="field full"><label for="cm-name">Campaign name</label><input type="text" id="cm-name" value="${attr(c ? c.name : '')}" autocomplete="off" /></div>
      ${c ? '' : `<div class="field full"><label for="cm-segment">Send to</label>${selectHtml('cm-segment', (sms.segments || []).map(s => ({ id: s.id, label: s.label })), '', 'block')}<div class="hint" id="cm-seg-note"></div></div>`}
      <div class="field full"><label for="cm-body">Message <small class="char-count" id="cm-count"></small></label><textarea id="cm-body" rows="5">${esc(c ? c.body : '')}</textarea></div>
      <div class="full msg-bad" id="cm-err"></div></div>`,
    foot: `<button class="btn" data-x>Cancel</button><button class="btn btn-primary" data-ok>${c ? 'Save' : 'Save draft'}</button>`,
  });
  const body = d.q('#cm-body'), count = d.q('#cm-count'), segSel = d.q('#cm-segment'), note = d.q('#cm-seg-note');
  const draw = () => { const n = body.value.length; count.textContent = `${n}/${max}`; count.classList.toggle('over', n > max); };
  const segNote = () => { if (!segSel) return; const sg = (sms.segments || []).find(x => x.id === segSel.value); note.textContent = sg ? sg.note : ''; };
  body.addEventListener('input', draw); draw(); if (segSel) { segSel.onchange = segNote; segNote(); }
  d.q('[data-x]').onclick = d.close;
  d.q('[data-ok]').onclick = async () => {
    const err = d.q('#cm-err'); err.textContent = ''; d.q('[data-ok]').disabled = true;
    try {
      await api.post(c ? '/api/sms/campaign/update' : '/api/sms/campaign', { instance, id: c ? c.id : null, name: d.q('#cm-name').value.trim(), body: body.value.trim(), segment: segSel ? segSel.value : undefined, config_owner: smsOwner || undefined });
      d.close(); toast(c ? 'Saved.' : 'Draft saved — approve it when the words are right.', 'ok'); loadSms();
    } catch (e) { err.textContent = e.message; d.q('[data-ok]').disabled = false; }
  };
}

// ── Settings ──────────────────────────────────────────────────────────────
function settingsHtml() {
  let h = channelChips();
  if (!settings) return h + skeleton(2);
  if (settings.empty) return empty(settings.empty, '', 'settings');
  (settings.sections || []).forEach(sec => {
    if (sec.id !== 'channels') return;
    const shown = (sec.channels || []).filter(c => !channel || c.id === channel);
    h += `<section class="section"><div class="section-h"><h2>${esc(sec.label)}</h2><span class="n mono" style="font-size:11px">${esc(sec.source)}</span></div><div class="section-note">${esc(sec.note)}</div>`;
    if (!shown.length) h += empty(sec.channels.length ? 'No settings for this channel' : 'No channels configured', '', 'settings', true);
    h += `<div class="stack">${shown.map(c => channelCard(c, sec.weekdays)).join('')}</div></section>`;
  });
  return h;
}
function channelCard(c, weekdays) {
  const id = attr(c.id), days = c.publishing_days || [], can = f => (c.editable || []).includes(f);
  const cadence = c.cadence_source === 'config'
    ? `<dt>Publishing days</dt><dd><div class="days">${weekdays.map(d => `<button class="day ${days.includes(d) ? 'on' : ''}" data-day="${d}" data-chan="${id}">${d.slice(0, 3)}</button>`).join('')}</div></dd>
       <dt>Publishing time</dt><dd><span class="inline-row"><input class="mini-input mono" value="${attr(c.publishing_time)}" placeholder="HH:MM" data-field="publishing_time" data-chan="${id}" />${c.next_slot ? `<span class="dim" style="font-size:12.5px">next: ${esc(c.next_slot)}</span>` : ''}</span></dd>`
    : `<dt>Cadence</dt><dd><div class="locked">${esc(c.schedule_human || 'set by its ship routine, not by this config')}${c.next_slot ? ` · next: ${esc(c.next_slot)}` : ''}</div>
       <div class="hint">Not set here — this channel has no day list in the marketing config, and its ship routine would not read one.${c.schedule_file ? ` Changing it is an edit to <code>${esc(c.schedule_file)}</code>.` : ''} Which piece goes out on a given day is its own planned date, oldest first, one a day.</div></dd>`;
  return `<div class="card" id="chan-${id}">
    <div class="chan-h"><span class="chan-name">${esc(c.label)}</span>${tag(c.tier, 'tier-' + String(c.tier).toLowerCase())}<span class="msg-dim" data-msg="${id}" style="margin-left:auto"></span></div>
    <div class="card-meta" style="margin-top:2px">${esc(c.tier_why)}</div>
    <dl class="kv" style="margin-top:16px">
      <dt>Channel</dt><dd>${can('enabled') ? `<button class="toggle ${c.enabled ? 'on' : ''}" data-toggle="enabled" data-chan="${id}" data-val="${c.enabled ? 'false' : 'true'}"><span class="sw"></span>${c.enabled ? 'On' : 'Off'}</button>` : `<span class="locked">${c.enabled ? 'On' : 'Off'}</span>`}</dd>
      <dt>Pieces per week</dt><dd><span class="inline-row">${can('post_count') ? `<input class="mini-input mono" type="number" min="0" max="50" value="${attr(c.post_count)}" data-field="post_count" data-chan="${id}" />` : `<span class="locked">${esc(c.post_count)}</span>`}${c.paused_for && String(c.post_count) === '0' ? '<span class="dim" style="font-size:12.5px">paused — see below</span>' : ''}</span></dd>
      ${cadence}
      <dt>Publishes via</dt><dd class="locked">${esc(c.publish_path)}</dd>
      <dt>Per-piece approval</dt><dd class="locked"><b>${c.require_approval ? 'Required' : 'NOT REQUIRED'}</b> — changing this is an edit to the config file, on purpose</dd>
      <dt>Voice corpus</dt><dd class="locked"><span class="num">${esc(c.voice_have)}/${esc(c.voice_need)}</span> samples${Number(c.voice_have) < Number(c.voice_need) ? ' · below the floor' : ''}</dd>
      ${c.paused_for ? `<dt>Paused</dt><dd class="locked">for <b>${esc(c.paused_for)}</b></dd>` : ''}
      ${c.playbook ? `<dt>Playbook</dt><dd class="locked mono" style="font-size:12.5px">${esc(c.playbook)}</dd>` : ''}
    </dl></div>`;
}
function wireSettings(el) {
  el.querySelectorAll('[data-day]').forEach(b => b.onclick = () => {
    if (settingsBusy) return;
    const sec = (settings.sections || []).find(x => x.id === 'channels'); const c = sec && sec.channels.find(x => x.id === b.dataset.chan); if (!c) return;
    const days = (c.publishing_days || []).slice(); const i = days.indexOf(b.dataset.day); if (i >= 0) days.splice(i, 1); else days.push(b.dataset.day);
    setChannelField(b.dataset.chan, 'publishing_days', days);
  });
  el.querySelectorAll('[data-toggle]').forEach(b => b.onclick = () => setChannelField(b.dataset.chan, b.dataset.toggle, b.dataset.val === 'true'));
  el.querySelectorAll('[data-field]').forEach(i => i.onchange = () => setChannelField(i.dataset.chan, i.dataset.field, i.value));
}
// One write at a time; the file is the truth, so re-read after every write
// (including a refusal — that is exactly when the screen must show the file).
async function setChannelField(chan, field, value) {
  if (settingsBusy) return; settingsBusy = true;
  const msg = root.querySelector(`[data-msg="${chan}"]`);
  if (msg) { msg.className = 'msg-dim'; msg.textContent = 'saving…'; }
  try {
    await api.post('/api/settings/channel', { channel: chan, field, value, instance });
    toast('Saved.', 'ok', 1800);
  } catch (e) { toast('Not saved: ' + e.message, 'bad'); }
  finally {
    await loadSettings();
    if (mkt) loadMkt();
    settingsBusy = false;
  }
}

// ── Render / load ─────────────────────────────────────────────────────────
function render() {
  const el = root.querySelector('#mkt'); if (!el) return;
  let h = '';
  if (sub === 'decide') h = mkt ? decideHtml() : skeleton(3);
  if (sub === 'content') h = contentHtml();
  if (sub === 'reddit') h = redditHtml();
  if (sub === 'sms') h = smsHtml();
  if (sub === 'settings') h = settingsHtml();
  el.innerHTML = h;
  afterRender(el);
  el.querySelectorAll('[data-chipname="chan"] [data-chip]').forEach(c => c.onclick = () => { channel = c.dataset.chip; prefs.set('mkt-channel', channel); top(); render(); });
  el.querySelectorAll('[data-chipname="phase"] [data-chip]').forEach(c => c.onclick = () => { contentFilter = c.dataset.chip; render(); });
  el.querySelectorAll('[data-chipname="rstatus"] [data-chip]').forEach(c => c.onclick = () => { redditFilter = c.dataset.chip; reddit = null; render(); loadReddit(); });
  const tb = el.querySelector('#mkt-topic-btn'); if (tb) tb.onclick = addTopic;
  if (sub === 'sms' && sms && !sms.empty) wireSms(el);
  if (sub === 'settings' && settings && !settings.empty) wireSettings(el);
  if (sub === 'content' && params.piece && content) { const p = el.querySelector('#piece-' + cssId(params.piece)); if (p) { p.scrollIntoView({ block: 'center' }); p.classList.add('focused'); } params.piece = ''; }
  if (sub === 'sms' && params.edit && sms && !sms.empty) { const id = params.edit; params.edit = ''; if ((sms.campaigns || []).some(c => c.id === id)) campaignDialog(id); }
}
async function loadMkt() {
  try { mkt = await api.get('/api/marketing', q()); instance = mkt.instance || instance; prefs.set('mkt-instance', instance);
    const known = new Set((mkt.channels || []).map(c => c.id)); if (channel && !known.has(channel)) { channel = ''; prefs.set('mkt-channel', ''); } }
  catch (e) { mkt = { empty: 'Error loading marketing: ' + e.message, instances: [], channels: [], due: [], queued: [], stats: {} }; }
}
async function loadContent() { try { content = await api.get('/api/content', q()); } catch (e) { content = { empty: 'Error loading content: ' + e.message }; } if (sub === 'content') render(); }
async function loadReddit() { try { const d = await api.get('/api/reddit', { status: redditFilter }); reddit = d.items || []; } catch (e) { reddit = []; reddit.error = e; } if (sub === 'reddit') render(); top(); }
async function loadSettings() { try { settings = await api.get('/api/settings', q()); } catch (e) { settings = { empty: e.status === 404 ? 'This view needs a server restart — the running process predates /api/settings.' : 'Error loading settings (' + e.message + ').' }; } if (sub === 'settings') render(); }
async function loadSms() { try { sms = await api.get('/api/sms', q(smsOwner ? { config_owner: smsOwner } : {})); } catch (e) { sms = { empty: 'Error loading SMS: ' + e.message }; } if (sub === 'sms') render(); top(); }

async function load(quiet = false) {
  if (loading) return; loading = true;
  const el = root.querySelector('#mkt'); if (!el) return; if (quiet && el) el.classList.add('refreshing');
  try {
    const jobs = [loadMkt()];
    if (sub === 'content' || (quiet && content)) jobs.push(loadContent());
    if (sub === 'reddit' || !reddit || quiet) jobs.push(loadReddit());
    if (sub === 'settings' || (quiet && settings)) jobs.push(loadSettings());
    if (sub === 'sms' || !sms || quiet) jobs.push(loadSms());
    await Promise.all(jobs);
    top(); render();
  } finally { loading = false; el && el.classList.remove('refreshing'); }
}

export default {
  id: 'marketing', title: 'Marketing', short: 'Marketing', dept: 'marketing', icon: 'megaphone', hot: true, section: 'main',
  async mount(r, route) {
    root = r; sub = route.sub || 'decide'; params = route.params || {};
    if (params.instance) { instance = params.instance; prefs.set('mkt-instance', instance); }
    root.innerHTML = `<div class="content-inner" id="mkt"></div>`;
    top(); render();
    bindActions(root, () => load(true));
    await load();
    poller = makePoller(() => load(true), 30000); poller.start();
    setViewKeys({ r: () => load(true), '1': () => navigate('marketing/decide'), '2': () => navigate('marketing/content'), '3': () => navigate('marketing/reddit'), '4': () => navigate('marketing/sms'), '5': () => navigate('marketing/settings') });
    setPaletteCommands(() => [{ group: 'Marketing', icon: 'plus', label: 'New SMS campaign', run: () => { navigate('marketing/sms'); setTimeout(() => sms && !sms.empty && campaignDialog(null), 400); } }]);
    this._refresh = () => load(true); window.addEventListener('cc:refresh', this._refresh);
  },
  update(route) {
    sub = route.sub || 'decide'; params = route.params || {};
    top(); render();
    if (sub === 'content' && !content) loadContent();
    if (sub === 'settings' && !settings) loadSettings();
    if (sub === 'sms' && !sms) loadSms();
    if (sub === 'reddit' && !reddit) loadReddit();
  },
  unmount() { poller && poller.stop(); window.removeEventListener('cc:refresh', this._refresh); },
};
