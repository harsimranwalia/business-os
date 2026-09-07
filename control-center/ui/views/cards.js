// Cards are drawn once, here, and used by both the Inbox and the department
// views — so an engineering gate looks and behaves identically wherever you
// meet it. bindActions() is the one click handler for every [data-act]
// button; it calls the same endpoints the old page did, with the same
// payloads. Nothing here auto-sends: every action is a human clicking.
import { icon, esc, attr, cssId, relTime, fmtDur, fmtWhen, dueLabel, fmtDate, api, toast, fail, confirm, promptText, navigate, renderDecisionBody, renderMarkdown, eventVerb, plural, prefs, dialog, isAdmin, copyText } from '../core.js';

export const GATE_LABEL = { merge: 'Merge gate', scope: 'Scope gate', 'intake-question': 'Question', incident: 'Incident', decision: 'Decision', release: 'Release gate', 'one-way-door': 'One-way door', 'g1-proposals': 'Proposals' };
export const PIPE_LABELS = { '1-signal': 'Signal', '2-qualified': 'Qualified', '3-contacted': 'Contacted', '4-engaged': 'Engaged',
  '5-proposal-sent': 'Proposal sent', '6-negotiating': 'Negotiating', '7-closed/won': 'Won', '7-closed/lost': 'Lost' };

export const tag = (t, cls = '') => `<span class="tag ${cls}">${esc(t)}</span>`;
export const pill = s => `<span class="pill ${esc(String(s || '').toLowerCase())}">${esc(s)}</span>`;
export function kindHead(ic, label, ago = '', late = false, extra = '') {
  return `<div class="card-kind">${icon(ic)}<span>${label}</span>${ago ? `<span class="ago ${late ? 'late' : ''}">${esc(ago)}</span>` : ''}${extra}</div>`;
}
function firstHeading(body, ticket) { const m = String(body || '').match(/^\s*#{1,2}\s+(.+)$/m); let t = m ? m[1].trim() : ''; if (ticket) t = t.replace(new RegExp('\\s*[(\\[]?' + ticket + '[)\\]]?\\s*$'), '').replace(new RegExp('^' + ticket + '\\s*[—:-]\\s*'), ''); return t; }
function stripFirstHeading(body) { return String(body || '').replace(/^\s*#{1,2}\s+.+\n?/, ''); }
export function prLinks(links) {
  if (!links || !links.length) return '';
  return `<div class="card-meta">${links.map(l => `<a href="${attr(l.url)}" target="_blank" rel="noopener">${l.repo ? esc(l.repo) + ' PR' : 'Open the PR'} ${icon('arrowUpRight', 'ic-sm')}</a>`).join('')}</div>`;
}
const act = (label, cls, ic, data, key) => `<button class="btn ${cls}" ${Object.entries(data).map(([k, v]) => `data-${k}="${attr(v)}"`).join(' ')}${key ? ` data-key="${key}"` : ''}>${ic ? icon(ic) : ''}${label}${key ? `<span class="kbd">${key.toUpperCase()}</span>` : ''}</button>`;

// ── Engineering ───────────────────────────────────────────────────────────
// The whole item as plain text — header line, recommendation, estimate, the
// full body, PR links — for pasting into a chat, a doc, or another model.
export function gateText(w) {
  const lines = [[w.ticket, GATE_LABEL[w.gate] || w.gate, w.project, w.raised ? 'raised ' + w.raised : ''].filter(Boolean).join(' · ')];
  if (w.recommendation) lines.push(`Recommendation: ${w.recommendation}`);
  if (w.time_estimate) lines.push(`Estimate: ${w.time_estimate}${w.time_impact ? ' (+' + w.time_impact + ')' : ''}`);
  lines.push('', String(w.body || '').trim());
  (w.pr_links || []).forEach(l => lines.push(`PR${l.repo ? ' (' + l.repo + ')' : ''}: ${l.url}`));
  return lines.join('\n') + '\n';
}
const copyBtn = text => `<button class="btn btn-ghost btn-sm btn-icon copy" data-act="copy" data-text="${attr(text)}" title="Copy this item, in full" aria-label="Copy this item">${icon('copy')}</button>`;

export function engGateCard(w, o = {}) {
  const gate = w.gate || 'decision';
  const title = firstHeading(w.body, w.ticket);
  const noteId = 'note-' + cssId(w.file);
  const base = { act: 'eng-decide', file: w.file, note: noteId, instance: o.instance || '' };
  return `<article class="card need item" data-item="${attr('eng:' + w.file)}" data-kind="eng">
    ${kindHead('branch', (o.inbox ? 'Engineering · ' : '') + (GATE_LABEL[gate] || gate), w.raised ? 'raised ' + relTime(w.raised) : '', false, copyBtn(gateText(w)))}
    <div class="card-head"><div class="card-title"><span class="id">${esc(w.ticket)}</span>${esc(title || w.ticket)}</div>
      <div class="card-tags">${w.project ? tag(w.project) : ''}${w.time_estimate ? tag('est. ' + w.time_estimate, 'tag-text') : ''}${w.time_impact ? tag('+' + w.time_impact, 'tag-accent tag-text') : ''}</div></div>
    ${w.recommendation ? `<div class="rec"><span class="lbl">Recommendation</span>${esc(w.recommendation)}</div>` : ''}
    <div class="card-body"><div class="prose clamp" data-clamp>${renderDecisionBody(title ? stripFirstHeading(w.body) : w.body)}</div><button class="more" data-more>${icon('chevronDown')}Read everything</button></div>
    ${prLinks(w.pr_links)}
    <textarea id="${noteId}" rows="1" placeholder="Add a note — required when requesting changes" data-note style="margin-top:12px"></textarea>
    <div class="actions card-actions">
      ${act('Approve', 'btn-ok', 'check', { ...base, decision: 'approved' }, 'a')}
      ${act('Request changes', 'btn-warn', 'pencil', { ...base, decision: 'changed' }, 'c')}
      ${act('Reject', 'btn-bad', 'x', { ...base, decision: 'rejected' }, 'x')}
    </div></article>`;
}
export function engBlockedCard(t, o = {}) {
  return `<article class="card need item" data-item="${attr('engb:' + t.id)}" data-kind="eng">
    ${kindHead('branch', (o.inbox ? 'Engineering · ' : '') + 'Blocked on you', t.updated ? 'since ' + relTime(t.updated) : '')}
    <div class="card-head"><div class="card-title"><span class="id">${esc(t.id)}</span>${esc(t.title)}</div><div class="card-tags">${t.project ? tag(t.project) : ''}</div></div>
    <div class="card-meta">See the ticket for what it needs.${t.pr_url ? ` <a href="${attr(t.pr_url)}" target="_blank" rel="noopener">Open the PR ${icon('arrowUpRight', 'ic-sm')}</a>` : ''}</div>
    <div class="actions card-actions">${act('Open board', 'btn', 'columns', { act: 'go', to: 'eng/board' }, 'enter')}</div></article>`;
}
export function engDecidingCard(w, activity) {
  const a = activity;
  const note = a && a.running ? `the department is working on it now (${esc(a.current_event || 'a pass')})`
    : (a && a.pending_count > 0 ? `queued — ${plural(a.pending_count, 'item')} ahead of it, nothing running right now`
      : 'nothing is running and nothing is queued — if this sits here, the trigger may not have fired; check "Right now"');
  return `<article class="card">
    ${kindHead('hourglass', GATE_LABEL[w.gate] || w.gate || 'Decision')}
    <div class="card-head"><div class="card-title"><span class="id">${esc(w.ticket)}</span>${esc(firstHeading(w.body) || w.ticket)}</div><div class="card-tags">${w.project ? tag(w.project) : ''}</div></div>
    <div class="card-meta">You said <b>${esc(w.decision)}</b> ${esc(relTime(w.decided))} · ${note}</div>
    ${prLinks(w.pr_links)}
    ${w.body ? `<details class="disclosure" style="margin-top:10px"><summary>${icon('chevronRight')}Show what you approved</summary><div class="body prose">${renderDecisionBody(w.body)}</div></details>` : ''}
  </article>`;
}
export function activityCard(a) {
  if (!a) return '';
  const dot = a.mode_halting || a.backoff_active ? 'warn' : (a.running ? 'on' : '');
  const status = a.mode_halting ? `Paused — MODE=${esc(a.mode)}` : a.running ? esc(eventVerb(a)) : 'Idle';
  const bits = [];
  if (a.running && a.running_seconds != null) bits.push(`<span>session <span class="num">${fmtDur(a.running_seconds)}</span></span>`);
  bits.push(`<span><span class="num">${a.pending_count}</span> queued</span>`);
  if (a.refunds_today) bits.push(`<span><span class="num">${a.refunds_today}</span> refunded</span>`);
  const pct = a.hops_budget ? Math.min(100, (a.hops_today / a.hops_budget) * 100) : 0;
  const disc = [];
  if (a.pending_preview && a.pending_preview.length) {
    const label = a.pending_count > a.pending_preview.length ? `Up next (${a.pending_preview.length} of ${a.pending_count})` : `Up next (${a.pending_count})`;
    disc.push(`<details class="disclosure"><summary>${icon('chevronRight')}${esc(label)}</summary><div class="body queue">${a.pending_preview.map(p => `<div class="queue-row">${tag(p.event)}<span>${esc(shortCtx(p.context))}</span></div>`).join('')}</div></details>`);
  }
  if (a.recent_log && a.recent_log.length) disc.push(`<details class="disclosure"><summary>${icon('chevronRight')}Recent activity</summary><div class="body"><pre class="logtail">${esc(a.recent_log.join('\n'))}</pre></div></details>`);
  return `<div class="now">
    <span class="agent-dot ${dot}"></span>
    <div style="min-width:0">
      <div class="now-title">${status}${a.running && a.current_ticket ? `<span class="id">${esc(a.current_ticket)}</span>` : ''}</div>
      <div class="now-meta">${bits.join('')}</div>
      ${a.running && a.current_activity ? `<div class="now-line">${esc(a.current_activity)}</div>` : ''}
      ${a.mode_halting ? `<div class="now-warn">This instance goes silent under MODE=${esc(a.mode)} — nothing notifies or posts until it is cleared.</div>` : ''}
      ${a.backoff_active ? `<div class="now-warn">Backed off after repeated failed starts — next attempt in ~${fmtDur(a.backoff_seconds)}.</div>` : ''}
    </div>
    <div class="budget"><b>${a.hops_today}${a.hops_budget ? ` / ${a.hops_budget}` : ''}</b><span>hops today</span>${a.hops_budget ? `<div class="bar"><i style="width:${pct}%"></i></div>` : ''}</div>
    ${disc.length ? `<div class="disclosures">${disc.join('')}</div>` : ''}
  </div>`;
}
export function shortCtx(context) { return context ? String(context).split(/[\\/]/).pop().replace(/\.md$/, '') : ''; }

// ── Marketing ─────────────────────────────────────────────────────────────
export function mktPieceCard(p, o = {}) {
  const chan = (o.channels || []).find(c => c.id === p.channel);
  // A planned date only reads as a deadline while the piece still needs
  // someone: once approved it ships on the channel's next slot, and once
  // shipped the date is history — neither is "late".
  const showDue = o.gate || p.phase === 'awaiting' || p.phase === 'drafting';
  const due = showDue && p.date ? dueLabel(p.date, o.today) : '';
  const late = /late/.test(due);
  const tags = [];
  if (p.archetype) tags.push(tag(p.archetype));
  if (p.has_carousel) tags.push(tag('carousel')); else if (p.format) tags.push(tag(p.format));
  if (p.series_stage) tags.push(tag('stage ' + p.series_stage));
  const actions = o.gate ? `<div class="actions card-actions">
      ${act('Approve', 'btn-ok', 'check', { act: 'mkt-approve', path: p.path, instance: o.instance || '' }, 'a')}
      ${act('Open in Content', 'btn', 'arrowUpRight', { act: 'go', to: 'marketing/content', piece: p.path }, 'enter')}
    </div>` : '';
  return `<article class="card ${o.gate ? 'need' : ''} item" id="piece-${cssId(p.path)}" data-item="${attr('mkt:' + p.path)}" data-kind="mkt">
    ${kindHead('megaphone', (o.inbox ? 'Marketing · ' : '') + esc(chan ? chan.label : (p.channel || 'piece')), due ? (late ? due : 'due ' + due) : (p.phase === 'shipped' ? 'shipped' : p.phase === 'queued' ? 'next slot' : (p.date ? '' : 'no planned date')), late)}
    <div class="card-head"><div class="card-title">${esc(p.title)}</div><div class="card-tags">${tags.join('')}</div></div>
    <div class="card-meta">${p.date ? `planned <span class="num">${esc(p.date)}</span>` : 'no planned date'}${o.meta ? ` · ${esc(o.meta)}` : ''}</div>
    ${o.body ? `<div class="card-body"><div class="prose pre keep">${esc(p.body) || '—'}</div></div>` : ''}
    ${actions}</article>`;
}
export function redditCard(it, o = {}) {
  const pending = it.status === 'PENDING';
  const bodyId = 'rd-body-' + cssId(it.id);
  return `<article class="card ${pending ? 'need' : ''} item" data-item="${attr('rd:' + it.id)}" data-kind="reddit">
    ${kindHead('reddit', (o.inbox ? 'Reddit · ' : '') + (it.community ? 'r/' + esc(it.community) : esc(it.channel || 'reddit')), '', false, `<span class="dim" style="letter-spacing:0;text-transform:none;font-weight:500">${esc(it.key)}</span>`)}
    <div class="card-head"><div class="card-title">${esc(it.title)}</div><div class="card-tags">${pill(it.status)}</div></div>
    ${pending ? `<div class="card-body"><textarea id="${bodyId}" rows="6" style="font-size:14px;line-height:1.6">${esc(it.body)}</textarea><div class="hint" style="margin-top:6px;font-size:12px;color:var(--text-3)">Edit freely — what you approve is what posts.</div></div>`
              : `<div class="card-body"><div class="prose pre">${esc(it.body) || '—'}</div></div>`}
    ${it.rationale ? `<div class="rec"><span class="lbl">Why this thread</span>${esc(it.rationale)}</div>` : ''}
    ${it.notes ? `<div class="card-meta">${esc(it.notes)}</div>` : ''}
    <div class="card-meta">${it.posted_url ? `<a href="${attr(it.posted_url)}" target="_blank" rel="noopener">Open posted thread ${icon('arrowUpRight', 'ic-sm')}</a>` : ''}
      ${it.permalink && !it.posted_url ? `<a href="${attr(it.permalink)}" target="_blank" rel="noopener">Open target thread ${icon('arrowUpRight', 'ic-sm')}</a>` : ''}</div>
    ${pending ? `<div class="actions card-actions">
      ${act('Approve', 'btn-ok', 'check', { act: 'reddit-approve', id: it.id, body: bodyId }, 'a')}
      ${act('Skip', 'btn-bad', 'x', { act: 'reddit-skip', id: it.id }, 'x')}</div>` : ''}
  </article>`;
}

// ── SMS ───────────────────────────────────────────────────────────────────
export function segLabel(sms, id) { const s = (sms.segments || []).find(x => x.id === id); return s ? s.label : id; }
export function smsCampaignCard(c, sms, o = {}) {
  const canEdit = c.status === 'draft' || c.status === 'approved';
  const base = { instance: sms.instance || '', id: c.id };
  const need = c.status === 'draft' || c.status === 'approved';
  return `<article class="card ${need ? 'need' : ''} item" data-item="${attr('smsc:' + c.id)}" data-kind="sms">
    ${kindHead('message', (o.inbox ? 'SMS · ' : '') + (c.status === 'approved' ? 'Ready to send' : c.status === 'draft' ? 'Campaign draft' : 'Campaign'), 'created ' + fmtWhen(c.created_at))}
    <div class="card-head"><div class="card-title">${esc(c.name)}</div><div class="card-tags">${pill(c.status)}</div></div>
    <div class="card-meta">${esc(segLabel(sms, c.segment))} · <span class="num">${c.recipient_count}</span> ${c.recipient_count === 1 ? 'recipient' : 'recipients'} at last count</div>
    <div class="sms-body">${esc(c.body)}</div>
    ${c.sizing_error ? `<div class="msg-bad" style="margin-top:8px">Could not size this segment: ${esc(c.sizing_error)}</div>` : ''}
    ${c.approved_by ? `<div class="fact">Approved by <b>${esc(c.approved_by)}</b> ${esc(fmtWhen(c.approved_at))}</div>` : ''}
    ${c.sent_at ? `<div class="fact">Sent ${esc(fmtWhen(c.sent_at))} — <b>${c.results ? c.results.sent : 0}</b> delivered, <b>${c.results ? c.results.failed : 0}</b> failed</div>` : ''}
    ${(c.results && (c.results.errors || []).length) ? `<div class="msgs" style="margin-top:8px">${c.results.errors.map(e => `<div class="msg failed"><div class="msg-head"><span class="msg-num">…${esc(e.phone)}</span></div><div class="msg-err">${esc(e.error)}</div></div>`).join('')}</div>` : ''}
    ${(canEdit || (c.status !== 'sent' && c.status !== 'discarded')) ? `<div class="actions card-actions">
      ${c.status === 'draft' ? act('Approve', 'btn-ok', 'check', { ...base, act: 'sms-camp', do: 'approve' }, 'a') : ''}
      ${c.status === 'approved' ? act('Send now', 'btn-primary', 'send', { ...base, act: 'sms-camp', do: 'send', name: c.name, n: c.recipient_count }, 'a') : ''}
      ${canEdit ? act('Edit', 'btn', 'pencil', { act: 'go', to: 'marketing/sms', edit: c.id }, 'c') : ''}
      ${(c.status !== 'sent' && c.status !== 'discarded') ? act('Discard', 'btn-bad', 'x', { ...base, act: 'sms-camp', do: 'discard' }, 'x') : ''}
    </div>` : ''}
  </article>`;
}
const reactState = m => m.state || (m.sent ? 'sent' : 'failed');
export const reactPending = run => (run.messages || []).filter(m => reactState(m) === 'pending');
function msgRow(run, m, sms) {
  const st = reactState(m);
  const base = { act: 'sms-react', instance: sms.instance || '', id: run.id, message: m.id };
  return `<div class="msg ${esc(st)}">
    <div class="msg-head"><span class="msg-to">${esc(m.name || 'No name on file')}</span><span class="msg-num">${esc(m.phone || '')}</span><span class="msg-state">${st === 'discarded' ? 'skipped' : esc(st)}</span></div>
    <div class="msg-body">${esc(m.message)}</div>
    ${m.detail && st !== 'sent' ? `<div class="msg-err">${st === 'pending' ? 'Last attempt failed: ' : 'Not sent: '}${esc(m.detail)}</div>` : ''}
    ${st === 'pending' ? `<div class="msg-acts">${act('Send', 'btn-ok btn-sm', 'send', { ...base, do: 'send' })}${act('Skip', 'btn-bad btn-sm', 'x', { ...base, do: 'discard' })}</div>` : ''}
  </div>`;
}
export function smsRunCard(run, sms, o = {}) {
  const waiting = reactPending(run);
  const base = { act: 'sms-react-run', instance: sms.instance || '', id: run.id, n: waiting.length };
  return `<article class="card ${waiting.length ? 'need' : ''} item" data-item="${attr('smsr:' + run.id)}" data-kind="sms">
    ${kindHead('sparkles', (o.inbox ? 'SMS · ' : '') + 'Smart reactivation' + (waiting.length ? ' · review' : ''), 'run ' + fmtWhen(run.created_at))}
    <div class="card-head"><div class="card-title">${waiting.length ? `${plural(waiting.length, 'message')} waiting on you` : `Run ${esc(fmtWhen(run.created_at))}`}</div><div class="card-tags">${pill(run.status)}</div></div>
    <div class="card-meta"><span><span class="num">${run.candidates}</span> lapsed</span><span><span class="num">${run.skipped_cooldown || 0}</span> in cooldown</span><span><span class="num">${run.considered}</span> considered</span><span><span class="num">${run.chosen == null ? 0 : run.chosen}</span> chosen</span>${run.mode === 'review' ? '<span>reviewed before sending</span>' : ''}</div>
    ${run.offer ? `<div class="rec"><span class="lbl">Offer</span>${esc(run.offer)}</div>` : ''}
    ${run.error ? `<div class="msg-bad" style="margin-top:8px">${esc(run.error)}</div>` : ''}
    ${waiting.length ? `<div class="fact">Nothing below has been sent unless it says so.</div>` : ''}
    ${(run.messages || []).length ? `<div class="msgs">${run.messages.map(m => msgRow(run, m, sms)).join('')}</div>` : ''}
    ${waiting.length ? `<div class="actions card-actions">
      ${act(`Send all ${waiting.length}`, 'btn-primary', 'send', { ...base, do: 'send' }, 'a')}
      ${act('Skip the rest', 'btn-bad', 'x', { ...base, do: 'discard' }, 'x')}</div>` : ''}
    ${run.approved_by ? `<div class="fact">Approved by <b>${esc(run.approved_by)}</b> ${esc(fmtWhen(run.approved_at))}</div>` : ''}
    <div class="fact"><b>${run.results ? run.results.sent : 0}</b> sent${waiting.length ? ` · <b>${waiting.length}</b> waiting` : ''}${(run.results && run.results.failed) ? ` · <b>${run.results.failed}</b> ${waiting.length ? 'refused so far' : 'failed'}` : ''}</div>
  </article>`;
}

// ── Sales (inbox follow-up) ───────────────────────────────────────────────
export function leadTitle(l) { const c = (l.contact || '').trim(); const n = c.split(/\s+[—–-]{1,2}\s+/)[0].trim(); return n || companyShort(l) || l.slug; }
export function companyShort(l) { return (l.company || '').split(' (')[0].trim(); }
export function leadFollowCard(item) {
  const l = item.data;
  const why = [];
  if (l.action_overdue) why.push('next action overdue');
  if (l.days_since_touch != null && l.days_since_touch >= 7) why.push(`${l.days_since_touch} days silent`);
  return `<article class="card need item" data-item="${attr('lead:' + l.slug)}" data-kind="sales">
    ${kindHead('handshake', 'Sales · Follow-up', why.join(' · '), true)}
    <div class="card-head"><div class="card-title">${esc(leadTitle(l))}${companyShort(l) && companyShort(l) !== leadTitle(l) ? ` <span class="dim" style="font-weight:500">· ${esc(companyShort(l))}</span>` : ''}</div>
      <div class="card-tags">${tag(PIPE_LABELS[item.stage] || item.stage)}${l.value ? tag('$' + Number(l.value).toLocaleString()) : ''}</div></div>
    ${l.status_note ? `<div class="card-meta">${esc(l.status_note)}</div>` : ''}
    <div class="actions card-actions">${act('Open lead', 'btn', 'arrowUpRight', { act: 'go', to: 'sales', lead: l.slug }, 'enter')}</div>
  </article>`;
}

// ── After render: clamps, note auto-grow ──────────────────────────────────
// Which cards the reader has opened with "Read everything", by item id. Views
// re-render on every poll; without this the body snapped shut mid-read.
const expanded = new Set();
const itemId = el => { const c = el.closest('[data-item]'); return c ? c.dataset.item : ''; };
const moreLabel = open => `${icon('chevronDown')}${open ? 'Collapse' : 'Read everything'}`;
export function afterRender(root) {
  root.querySelectorAll('[data-clamp]').forEach(el => {
    // Short bodies do not need a "read everything": drop the fade and button.
    if (el.scrollHeight <= el.clientHeight + 8) { el.classList.remove('clamp'); const m = el.parentElement.querySelector('[data-more]'); if (m) m.remove(); return; }
    if (expanded.has(itemId(el))) { el.classList.remove('clamp'); const m = el.parentElement.querySelector('[data-more]'); if (m) m.innerHTML = moreLabel(true); }
  });
}
function grow(t) { t.style.height = 'auto'; t.style.height = Math.min(320, t.scrollHeight + 2) + 'px'; }

// Notes typed into cards survive a re-render: capture every input/textarea
// with an id before the view rebuilds its HTML, put the text back after. The
// store outlives a single render so a note on a card a filter hid for a
// moment is still there when the card comes back.
const kept = {};
export function captureInputs(root) {
  root.querySelectorAll('input[id], textarea[id]').forEach(el => { if (el.type === 'file') return; if (el.value) kept[el.id] = el.value; else delete kept[el.id]; });
  return kept;
}
export function restoreInputs(root) {
  Object.entries(kept).forEach(([id, v]) => { const el = root.querySelector('#' + CSS.escape(id)); if (el && !el.value) { el.value = v; if (el.tagName === 'TEXTAREA') grow(el); } });
}

// ── Actions ───────────────────────────────────────────────────────────────
// One delegated handler per root. `onChange` re-loads the view (and pings the
// shell so the badges follow). Buttons go disabled while their request runs.
export function bindActions(root, onChange) {
  const changed = () => { window.dispatchEvent(new CustomEvent('cc:changed')); onChange && onChange(); };
  root.addEventListener('input', e => { if (e.target.matches('[data-note]')) grow(e.target); });
  root.addEventListener('click', async e => {
    const more = e.target.closest('[data-more]');
    if (more) { const c = more.parentElement.querySelector('[data-clamp]'); const open = c.classList.toggle('clamp') === false; more.innerHTML = moreLabel(open); const id = itemId(c); if (id) { open ? expanded.add(id) : expanded.delete(id); } return; }
    const b = e.target.closest('[data-act]');
    if (!b || b.disabled) return;
    const d = b.dataset;
    const card = b.closest('.card');
    const busy = on => { if (card) card.querySelectorAll('[data-act]').forEach(x => x.disabled = on); };
    try {
      switch (d.act) {
        case 'go': { const { act, to, ...params } = d; delete params.key; navigate(to, params); return; }
        case 'copy': { const ok = await copyText(d.text); toast(ok ? 'Copied to the clipboard.' : 'Could not copy — the browser blocked clipboard access.', ok ? 'ok' : 'bad'); return; }
        case 'eng-decide': {
          const noteEl = document.getElementById(d.note);
          const note = noteEl ? noteEl.value.trim() : '';
          if (d.decision === 'changed' && !note) { noteEl && noteEl.focus(); toast('Say what should change — "request changes" needs a note.', 'warn'); return; }
          if (d.decision === 'rejected' && !(await confirm({ title: 'Reject this?', body: 'The ticket stops here. Add a note first if the team should know why.', ok: 'Reject', danger: true }))) return;
          busy(true);
          await api.post('/api/eng/decide', { file: d.file, decision: d.decision, note, instance: d.instance });
          card && card.classList.add('pending-out');
          toast(d.decision === 'approved' ? 'Approved — the department picks it up on its next pass.' : d.decision === 'changed' ? 'Sent back with your note.' : 'Rejected.', 'ok');
          changed(); return;
        }
        case 'eng-priority': { busy(true); await api.post('/api/eng/priority', { ticket: d.ticket, priority: d.priority, instance: d.instance }); changed(); return; }
        case 'eng-merge-check': {
          const force = d.force === '1';
          if (force && !(await confirm({ title: `Mark ${d.ticket} as merged?`, body: 'Only if you actually merged the PR. This advances the ticket to shipped without checking git.', ok: 'Mark merged', danger: true }))) return;
          busy(true);
          const r = await api.post('/api/eng/merge-check', { ticket: d.ticket, force, instance: d.instance });
          if (!r.merged) { dialog({ title: `${d.ticket} does not look merged yet`, size: 'sm', body: `<p>${esc(r.detail || '')}</p>${r.hint ? `<p class="dim">${esc(r.hint)}</p>` : ''}`, foot: `<button class="btn btn-primary" onclick="this.closest('.backdrop').remove()">OK</button>` }); busy(false); return; }
          toast(`${d.ticket} marked merged.`, 'ok'); changed(); return;
        }
        case 'mkt-approve': { busy(true); await api.post('/api/mkt/approve', { path: d.path, instance: d.instance }); card && card.classList.add('pending-out'); toast('Approved — it ships on its channel\'s next slot.', 'ok'); changed(); return; }
        case 'reddit-approve': { const t = document.getElementById(d.body); busy(true); await api.post('/api/reddit/action', { id: d.id, action: 'edit_approve', body: t ? t.value : undefined }); card && card.classList.add('pending-out'); toast('Approved — the poster sends it on its next cycle.', 'ok'); changed(); return; }
        case 'reddit-skip': { const reason = await promptText({ title: 'Skip this thread', label: 'Reason (optional)', placeholder: 'e.g. off-topic, already answered well', ok: 'Skip' }); if (reason === null) return; busy(true); await api.post('/api/reddit/action', { id: d.id, action: 'skip', reason }); card && card.classList.add('pending-out'); toast('Skipped.', 'ok'); changed(); return; }
        case 'sms-camp': {
          const owner = prefs.get('sms-owner') || undefined;
          if (d.do === 'send' && !(await confirm({ title: `Send "${d.name}" now?`, body: `Roughly ${d.n} people get this text. It cannot be recalled.`, ok: `Send to ~${d.n}`, danger: true }))) return;
          if (d.do === 'discard' && !(await confirm({ title: 'Discard this campaign?', body: 'It stays on the board as discarded; nothing sends.', ok: 'Discard', danger: true }))) return;
          busy(true);
          await api.post('/api/sms/campaign/' + d.do, { instance: d.instance, id: d.id, config_owner: owner });
          toast(d.do === 'approve' ? 'Approved — send it whenever you are ready.' : d.do === 'send' ? 'Sending.' : 'Discarded.', 'ok'); changed(); return;
        }
        case 'sms-react': { busy(true); await api.post('/api/sms/reactivation/' + d.do, { instance: d.instance, id: d.id, messages: [d.message], config_owner: prefs.get('sms-owner') || undefined }); toast(d.do === 'send' ? 'Sent.' : 'Skipped.', 'ok'); changed(); return; }
        case 'sms-react-run': {
          const n = Number(d.n);
          const ok = d.do === 'send' ? await confirm({ title: `Send all ${plural(n, 'remaining message')} now?`, body: 'They go to real phones and cannot be recalled.', ok: `Send ${n}`, danger: true })
                                     : await confirm({ title: `Skip the ${plural(n, 'message')} still waiting?`, body: 'They will not be sent, and this run stops holding their phone numbers.', ok: 'Skip them', danger: true });
          if (!ok) return;
          busy(true);
          await api.post('/api/sms/reactivation/' + d.do, { instance: d.instance, id: d.id, messages: null, config_owner: prefs.get('sms-owner') || undefined });
          toast(d.do === 'send' ? 'Sending all.' : 'Skipped the rest.', 'ok'); changed(); return;
        }
      }
    } catch (err) { busy(false); fail(err); }
  });
}
