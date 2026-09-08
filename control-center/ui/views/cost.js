// Cost — spend by agent, model, routine and version, over a window. API-
// equivalent pricing for comparing agents against each other; not an invoice.
import { api, setTop, seg, refreshBtn, esc, icon, skeleton, money, compact, setViewKeys, errorBox } from '../core.js';

let root, data = null, days = 7, loading = false;

function top() {
  setTop({ title: 'Cost', sub: seg([{ id: '7', label: '7 days' }, { id: '30', label: '30 days' }, { id: '90', label: '90 days' }], String(days)), right: refreshBtn() });
  document.querySelectorAll('[data-seg]').forEach(b => b.onclick = () => { days = Number(b.dataset.seg); top(); load(); });
  document.querySelector('[data-refresh]').onclick = () => load(true);
}

function table(title, rows, keyLabel, keyField, extra) {
  const max = Math.max(...rows.map(r => r.cost), 0.0001);
  const bar = keyField === 'agent' || keyField === 'routine';
  return `<section class="section"><div class="section-h"><h2>${esc(title)}</h2><span class="n">${rows.length}</span></div>
    <div class="table-wrap"><table class="table"><thead><tr><th class="${bar ? 'bar-cell' : ''}">${esc(keyLabel)}</th>${(extra || []).map(c => `<th class="l">${esc(c)}</th>`).join('')}<th>Runs</th><th>Cost</th><th>Avg run</th><th>Avg time</th><th>Tokens</th><th>Errors</th></tr></thead><tbody>
    ${rows.map(r => `<tr><td>${esc(r[keyField])}${bar ? `<div class="bar"><i style="width:${Math.max(1.5, (r.cost / max) * 100)}%"></i></div>` : ''}</td>
      ${(extra || []).map(c => c === 'Tier' ? `<td class="l"><span class="tier">${esc(r.tier || 'unmapped')}</span> <span class="dim">${esc(r.model || '')}</span></td>` : '<td></td>').join('')}
      <td>${r.runs}</td><td>${money(r.cost)}</td><td>${money(r.avg_cost)}</td><td>${r.avg_s != null ? Math.round(r.avg_s) + 's' : '—'}</td><td>${compact(r.tokens)}</td><td class="${r.errors ? 'flag' : 'zero'}">${r.errors || '—'}</td></tr>`).join('')}
    </tbody></table></div></section>`;
}

function render() {
  const el = root.querySelector('#cost'); if (!el) return;
  const d = data;
  if (!d) { el.innerHTML = skeleton(3); return; }
  if (!d.runs) { el.innerHTML = `<div class="empty">${icon('coins')}<div><b>No runs recorded in the last ${d.days} days</b><p>Rows are written by <code>departments/engineering/lib/run-stream.py</code> on every <code>claude -p</code> run under an engineering instance.</p></div></div>`; return; }
  let h = `<div class="stats">
    <div class="stat"><b>${money(d.total_cost)}</b><span>total, ${d.days} days</span></div>
    <div class="stat"><b>${d.runs}</b><span>runs</span></div>
    <div class="stat"><b>${money(d.avg_cost)}</b><span>average run</span></div>
    <div class="stat ${d.errors ? 'bad' : ''}"><b>${d.errors || '—'}</b><span>errored</span></div>
    <div class="stat ${d.drift ? 'hot' : ''}"><b>${d.drift || '—'}</b><span>model drift</span></div>
  </div>`;
  if (d.by_business && d.by_business.length > 1) h += table('Spend by business', d.by_business, 'Business', 'business');
  h += table('Spend by agent', d.by_agent || [], 'Agent', 'agent');
  h += table('Spend by model billed', d.by_model || [], 'Model', 'model');
  h += table('Spend by routine', d.by_routine || [], 'Routine', 'routine', ['Tier']);
  if (d.by_version && d.by_version.length > 1) h += table('Spend by agent version', d.by_version, 'Version', 'version');
  h += `<div class="footnote">${esc(d.note || '')}<br>Tiers resolve through <code>departments/engineering/lib/model-tier.sh</code>: ${Object.entries(d.tiers || {}).map(([t, m]) => `${esc(t)} → ${esc(m)}`).join(' · ')}.${d.drift ? '<br><span style="color:var(--accent-2)">Model drift means a run asked for one model and billed another.</span>' : ''}</div>`;
  el.innerHTML = h;
}

async function load(quiet = false) {
  if (loading) return; loading = true;
  const el = root.querySelector('#cost'); if (!el) return; if (quiet && el) el.classList.add('refreshing');
  try { data = await api.get('/api/costs', { days }); render(); }
  catch (e) { if (el) el.innerHTML = errorBox(e, 'costs'); }
  finally { loading = false; el && el.classList.remove('refreshing'); }
}

export default {
  id: 'cost', title: 'Cost', short: 'Cost', dept: 'cost', icon: 'coins', section: 'system',
  async mount(r) {
    root = r; data = null;
    root.innerHTML = `<div class="content-inner" id="cost"></div>`;
    top(); render(); await load();
    setViewKeys({ r: () => load(true) });
    this._refresh = () => load(true); window.addEventListener('cc:refresh', this._refresh);
  },
  unmount() { window.removeEventListener('cc:refresh', this._refresh); },
};
