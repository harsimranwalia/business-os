// Sales — the CRM funnel, per business instance. A kanban on desktop with
// drag-and-drop between stages; one stage at a time on a phone, with the
// stage move inside the lead sheet instead.
import { api, setTop, selectHtml, refreshBtn, esc, attr, icon, empty, skeleton, prefs, toast, fail, dialog, renderMarkdown, setViewKeys, makePoller, errorBox, money0, setPaletteCommands } from '../core.js';
import { PIPE_LABELS, leadTitle, companyShort } from './cards.js';

let root, data = null, instance = prefs.get('sales-instance', ''), poller = null, loading = false, params = {};
let stageShown = prefs.get('sales-stage', '1-signal');
let drag = null;

function top() {
  const insts = (data && data.instances) || [];
  setTop({ title: 'Sales', right: `<button class="btn btn-primary btn-sm" id="lead-add">${icon('plus')}<span class="only-desktop">Add lead</span></button>` + (insts.length > 1 ? selectHtml('sales-inst', insts, instance) : '') + refreshBtn() });
  document.getElementById('lead-add').onclick = addLeadDialog;
  const sel = document.getElementById('sales-inst'); if (sel) sel.onchange = () => { instance = sel.value; prefs.set('sales-instance', instance); data = null; render(); load(); };
  document.querySelector('[data-refresh]').onclick = () => load(true);
}

function leadHtml(l, stage) {
  const closed = stage.startsWith('7-');
  const stale = !closed && l.days_since_touch != null && l.days_since_touch >= 7;
  const late = l.action_overdue || stale;
  const co = companyShort(l), who = leadTitle(l);
  return `<div class="lead ${late && !closed ? 'late' : ''}" draggable="true" data-slug="${attr(l.slug)}" data-stage="${attr(stage)}">
    <div class="lead-who">${esc(who)}</div>
    ${co && co !== who ? `<div class="lead-co">${esc(co)}</div>` : ''}
    ${l.status_note ? `<div class="lead-note">${esc(l.status_note)}</div>` : ''}
    <div class="lead-meta">
      ${l.value ? `<span class="val">${money0(l.value)}</span>` : ''}
      ${l.source ? `<span>${esc(l.source)}</span>` : ''}
      ${stale ? `<span class="stale">${l.days_since_touch}d silent</span>` : ''}
      ${l.action_overdue ? '<span class="due">due</span>' : ''}
    </div></div>`;
}

function render() {
  const el = root.querySelector('#sales'); if (!el) return;
  if (!data) { el.innerHTML = skeleton(2); return; }
  if (data.empty) { el.innerHTML = empty(data.empty, '', 'handshake'); return; }
  const stages = data.stages || [];
  const open = stages.filter(s => !s.name.startsWith('7-'));
  const active = open.reduce((n, s) => n + s.leads.length, 0);
  const late = open.reduce((n, s) => n + s.leads.filter(l => l.action_overdue || (l.days_since_touch != null && l.days_since_touch >= 7)).length, 0);
  const won = (stages.find(s => s.name === '7-closed/won') || { leads: [] }).leads;
  let h = `<div class="stats">
    <div class="stat"><b>${active}</b><span>active leads</span></div>
    <div class="stat"><b>${money0(data.total_value || 0)}</b><span>pipeline value</span></div>
    <div class="stat ${late ? 'hot' : ''}"><b>${late}</b><span>need a follow-up</span></div>
    <div class="stat"><b>${won.length}</b><span>won</span></div>
  </div>`;
  if (!stages.some(s => s.leads.length)) h += `<div class="empty" style="margin-bottom:18px">${icon('handshake')}<div><b>No leads yet</b><p>Add one, or let the departments surface signals here.</p></div></div>`;
  h += `<div class="stage-picker">${stages.map(s => `<button class="chip ${s.name === stageShown ? 'on' : ''}" data-stage-pick="${attr(s.name)}">${esc(PIPE_LABELS[s.name] || s.name)}<span class="n">${s.leads.length}</span></button>`).join('')}</div>`;
  h += `<div class="board">${stages.map(s => {
    const sum = s.leads.reduce((n, l) => n + (Number(l.value) || 0), 0);
    const cls = s.name === '7-closed/won' ? 'won' : s.name === '7-closed/lost' ? 'lost' : '';
    return `<div class="col ${cls} ${s.name === stageShown ? 'show' : ''}" data-col="${attr(s.name)}">
      <div class="col-h"><span class="col-name">${esc(PIPE_LABELS[s.name] || s.name)}</span><span class="col-n">${s.leads.length}</span>${sum ? `<span class="col-sum">${money0(sum)}</span>` : ''}</div>
      ${s.leads.length ? s.leads.map(l => leadHtml(l, s.name)).join('') : '<div class="lane-empty">—</div>'}</div>`;
  }).join('')}</div>`;
  el.innerHTML = h;
  el.querySelectorAll('[data-stage-pick]').forEach(b => b.onclick = () => { stageShown = b.dataset.stagePick; prefs.set('sales-stage', stageShown); render(); });
  el.querySelectorAll('.lead').forEach(card => {
    card.onclick = () => openLead(card.dataset.stage, card.dataset.slug);
    card.ondragstart = e => { drag = card.dataset.slug; card.classList.add('dragging'); e.dataTransfer.effectAllowed = 'move'; try { e.dataTransfer.setData('text/plain', drag); } catch (err) {} };
    card.ondragend = () => { card.classList.remove('dragging'); el.querySelectorAll('.col.over').forEach(c => c.classList.remove('over')); };
  });
  el.querySelectorAll('.col').forEach(col => {
    col.ondragover = e => { if (!drag) return; e.preventDefault(); e.dataTransfer.dropEffect = 'move'; col.classList.add('over'); };
    col.ondragleave = e => { if (!col.contains(e.relatedTarget)) col.classList.remove('over'); };
    col.ondrop = async e => { e.preventDefault(); col.classList.remove('over'); const slug = drag; drag = null; if (!slug) return; await moveLead(slug, col.dataset.col); };
  });
  if (params.lead) { const slug = params.lead; params.lead = ''; const st = stages.find(s => s.leads.some(l => l.slug === slug)); if (st) openLead(st.name, slug); }
}

async function moveLead(slug, stage) {
  try { await api.post('/api/sales/move-lead', { instance, slug, to_stage: stage }); toast(`Moved to ${PIPE_LABELS[stage] || stage}.`, 'ok', 1800); }
  catch (e) { fail(e); }
  load(true);
}

function openLead(stageName, slug) {
  const stage = (data.stages || []).find(s => s.name === stageName);
  const l = stage && (stage.leads || []).find(x => x.slug === slug);
  if (!l) return;
  const meta = [['Stage', PIPE_LABELS[stageName] || stageName], ['Source', l.source], ['Segment', l.icp_segment],
    ['Last touch', l.last_touch || (l.days_since_touch != null ? l.days_since_touch + 'd ago' : '')], ['Contract end', l.contract_end_date], ['Custom cadence', l.custom_cadence]].filter(([, v]) => v);
  const stages = (data.stages || []).map(s => ({ id: s.name, label: PIPE_LABELS[s.name] || s.name }));
  const d = dialog({
    title: esc(l.contact || l.slug), sub: esc(l.company || ''),
    body: `<div class="meta-grid" style="margin-bottom:16px">${meta.map(([k, v]) => `<div><div class="k">${esc(k)}</div><div class="v">${esc(String(v))}</div></div>`).join('')}</div>
      <div class="prose" style="margin-bottom:18px">${l.body ? renderMarkdown(l.body, { breaks: true }) : '<span class="dim">No history recorded.</span>'}</div>
      <div class="form-grid">
        <div class="field full"><label>Stage</label>${selectHtml('lm-stage', stages, stageName, 'block')}</div>
        <div class="field full"><label>Status note</label><input id="lm-status-note" value="${attr(l.status_note || '')}" /></div>
        <div class="field"><label>Estimated value ($)</label><input id="lm-value" class="mono" inputmode="numeric" value="${attr(l.value || '')}" /></div>
        <div class="field"><label>Next action due</label><input id="lm-due" class="mono" placeholder="YYYY-MM-DD" value="${attr(l.next_action_due || '')}" /></div>
        <div class="field full"><label>Log a note <small>stamps last touch</small></label><textarea id="lm-note" rows="2"></textarea></div>
      </div>`,
    foot: `<button class="btn" data-x>Close</button><button class="btn btn-primary" data-ok>Save</button>`,
  });
  d.q('[data-x]').onclick = d.close;
  d.q('[data-ok]').onclick = async () => {
    const btn = d.q('[data-ok]'); btn.disabled = true;
    try {
      const newStage = d.q('#lm-stage').value;
      await api.post('/api/sales/lead/update', { instance, slug, note: d.q('#lm-note').value,
        fields: { status_note: d.q('#lm-status-note').value, estimated_value: d.q('#lm-value').value, next_action_due: d.q('#lm-due').value } });
      if (newStage !== stageName) await api.post('/api/sales/move-lead', { instance, slug, to_stage: newStage });
      d.close(); toast('Saved.', 'ok', 1800); load(true);
    } catch (e) { btn.disabled = false; fail(e); }
  };
}

function addLeadDialog() {
  const d = dialog({
    title: 'New lead', sub: 'Lands in Signal. Move it along as it earns its way.', size: 'sm',
    body: `<div class="form-grid">
      <div class="field"><label>Contact</label><input id="la-contact" placeholder="Name — role" /></div>
      <div class="field"><label>Company</label><input id="la-company" /></div>
      <div class="field"><label>Source</label><input id="la-source" placeholder="referral, inbound, outbound…" /></div>
      <div class="field"><label>Estimated value ($)</label><input id="la-value" class="mono" inputmode="numeric" /></div>
      <div class="field full"><label>Why this is a signal</label><textarea id="la-note" rows="2"></textarea></div></div>`,
    foot: `<button class="btn" data-x>Cancel</button><button class="btn btn-primary" data-ok>Add to Signal</button>`,
  });
  d.q('[data-x]').onclick = d.close;
  d.q('[data-ok]').onclick = async () => {
    const btn = d.q('[data-ok]'); btn.disabled = true;
    try {
      await api.post('/api/sales/lead', { instance, contact: d.q('#la-contact').value, company: d.q('#la-company').value, source: d.q('#la-source').value, estimated_value: d.q('#la-value').value, status_note: d.q('#la-note').value });
      d.close(); toast('Added to Signal.', 'ok'); load(true);
    } catch (e) { btn.disabled = false; fail(e); }
  };
}

async function load(quiet = false) {
  if (loading) return; loading = true;
  const el = root.querySelector('#sales'); if (!el) return; if (quiet && el) el.classList.add('refreshing');
  try { data = await api.get('/api/sales', { instance }); instance = data.instance || instance; prefs.set('sales-instance', instance); top(); render(); }
  catch (e) { if (el) el.innerHTML = errorBox(e, 'the pipeline'); }
  finally { loading = false; el && el.classList.remove('refreshing'); }
}

export default {
  id: 'sales', title: 'Sales', short: 'Sales', dept: 'sales', icon: 'handshake', hot: true, section: 'main',
  async mount(r, route) {
    root = r; data = null; params = route.params || {};
    if (params.instance) { instance = params.instance; prefs.set('sales-instance', instance); }
    root.innerHTML = `<div class="content-inner wide" id="sales"></div>`;
    top(); render();
    await load();
    poller = makePoller(() => load(true), 30000); poller.start();
    setViewKeys({ r: () => load(true), n: addLeadDialog });
    setPaletteCommands(() => [{ group: 'Sales', icon: 'plus', label: 'Add lead', k: 'N', run: addLeadDialog }].concat(
      ((data && data.stages) || []).flatMap(s => s.leads.map(l => ({ group: 'Leads', icon: 'handshake', label: leadTitle(l), sub: `${companyShort(l)} · ${PIPE_LABELS[s.name] || s.name}`, run: () => openLead(s.name, l.slug) })))));
    this._refresh = () => load(true); window.addEventListener('cc:refresh', this._refresh);
  },
  update(route) { params = route.params || {}; render(); },
  unmount() { poller && poller.stop(); window.removeEventListener('cc:refresh', this._refresh); },
};
