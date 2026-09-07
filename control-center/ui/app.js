// Boot: confirm the session, draw the shell, route to a view, keep the badges
// and the agent pill fresh in the background.
import { loadMe, renderShell, registerView, visibleViews, parseRoute, navigate, setViewKeys, setPaletteCommands, me, canSee, isAdmin, bindGlobalKey } from './core.js';
import { sweep } from './views/inbox-data.js';
import inbox from './views/inbox.js';
import marketing from './views/marketing.js';
import sales from './views/sales.js';
import eng from './views/eng.js';
import cost from './views/cost.js';
import logs from './views/logs.js';
import partners from './views/partners.js';
import config from './views/config.js';

[inbox, marketing, sales, eng, cost, logs, partners, config].forEach(registerView);

let current = null;
async function route() {
  const r = parseRoute();
  const vis = visibleViews();
  let view = vis.find(v => v.id === r.view);
  if (!view) { navigate(vis[0] ? vis[0].id : 'inbox'); return; }
  const content = document.getElementById('content');
  if (current && current.view === view && current.view.update) {
    // Same view, different sub-route: let it re-route itself without a remount.
    current.view.update(r);
  } else {
    if (current && current.view.unmount) { try { current.view.unmount(); } catch (e) {} }
    setViewKeys({});
    setPaletteCommands(null);
    content.scrollTop = 0;
    content.innerHTML = '';
    current = { view, r };
    try { await view.mount(content, r); } catch (e) { console.error(e); content.innerHTML = `<div class="content-inner"><div class="banner bad">Could not open ${view.title}: ${e.message}</div></div>`; }
  }
  document.title = `${view.title} · Control Center`;
  document.querySelectorAll('[data-nav]').forEach(el => el.classList.toggle('on', el.dataset.nav === view.id && !el.hasAttribute('data-agent')));
  document.querySelectorAll('[data-tab]').forEach(el => el.classList.toggle('on', el.dataset.tab === view.id));
}

async function boot() {
  await loadMe();
  const app = document.getElementById('app');
  renderShell(app);
  app.removeAttribute('aria-busy');
  window.addEventListener('hashchange', route);
  await route();
  // Badge sweep: what needs you, per view, so the rail is truthful before you
  // ever open a department. Re-run on a slow cadence and whenever a view
  // reports that it changed something.
  sweep();
  setInterval(() => { if (!document.hidden) sweep(); }, 60000);
  window.addEventListener('cc:changed', () => sweep());
  bindGlobalKey('r', () => window.dispatchEvent(new CustomEvent('cc:refresh')));
}
boot().catch(e => { console.error(e); });
