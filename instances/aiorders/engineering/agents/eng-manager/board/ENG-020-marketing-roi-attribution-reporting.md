---
id: ENG-020
title: Marketing ROI reporting — traffic source and revenue attribution on the brand dashboard
project: restaurant-portal
type: feature
size: M
time_estimate: a day and a half to two days
time_spent:
time_remaining:
severity: P2
priority:
state: shaped
owner: product-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-08-29
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-020-marketing-roi-attribution-reporting.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

Restaurant owners have no way to see, anywhere in the product, whether the
AI-generated SEO applied to their website is doing anything — no visibility
into where customers come from, and no link from that traffic to orders or
revenue. Microsoft Clarity, already being installed as a stopgap, can't answer
this either (it's a behaviour-analytics tool, not attribution or revenue, and
isn't integrated with AIOrders at all).

## Outcome

A restaurant owner on the brand portal can see their own customers, orders,
and revenue broken down by acquisition channel (organic, direct, social,
referral, paid, QR/in-store, etc.), over a selectable time range, framed
honestly rather than as a number that claims to isolate AI SEO's effect alone.

## Notes

- **This is a reporting gap, not a capture gap — confirmed in code, not
  assumed.** Every customer-signup path this platform has (online order,
  email signup, catering form, `config-site-builder/public/tracking/
  user-tracking.js`) already writes `utm_source`/`utm_medium`/`utm_campaign`/
  `first_touch_source`/`last_touch_source`/`first_referrer` onto the
  `customers` row (`website-submissions/customer-signup.ts`,
  `email-signup.ts`, `update-customer-tracking.ts`, `catering-request/
  index.ts`, `crm/customers.ts`), and `autopilot/marketing/welcome.ts`
  already branches its own logic on `first_touch_source`. Nothing reads those
  columns back out to an owner.
- **Extension point, confirmed by reading the code, not assumed.**
  `aiorders-api/supabase/functions/analytics/database.ts` (backing the brand
  portal's `Dashboard`/`analyticsService.ts`) already queries both `orders`
  and `customers` for a restaurant — the join surface this needs already
  exists there, so this is an extension, not a new subsystem.
- **"AI SEO" traced to a real, specific feature, not a vague marketing
  term.** `aiorders-admin-hub/src/pages/RestaurantAIWebsite.tsx` has a "SEO
  Settings" tab with an "Generate with AI" button that writes `seo.title`/
  `description`/`keywords`/OG tags, consumed by `config-site-builder`'s
  `buildSeo.ts`. Staff-only, admin-hub-side — the restaurant owner never sees
  this feature or its output performance today.
- **Microsoft Clarity is not in this codebase anywhere** — confirmed by a
  case-insensitive search across all five repos, zero hits. If it's been
  installed, it's via the generic custom-code head/body injection
  (`config-site-builder/src/hooks/useCustomCode.ts`) or done entirely outside
  AIOrders. Proposed out of scope — see PRD Non-goals for why pulling its
  data in wouldn't answer the question this ticket is actually about.
- **Don't confuse with the existing "Analytics" nav item.**
  `restaurant-portal/src/pages/analytics/Index.tsx` is entirely mock data
  about influencer-campaign performance (Instagram/TikTok/YouTube) —
  unrelated to website traffic, and not to be reused or extended by this
  ticket.
- **Cross-tenant scoping risk, named because it has already happened on this
  codebase.** `ENG-015` found a handler missing the role/brand check its
  sibling handler had. Acceptance criterion 5 in the PRD exists specifically
  because of that precedent.
- **Cross-domain attribution coverage is unconfirmed.** `user-tracking.js`'s
  own `README.md` documents the online-ordering-side wiring as something each
  deployment still has to add, not guaranteed live everywhere — the architect
  should verify actual per-restaurant coverage before this report's numbers
  are presented as complete. Acceptance criterion 3's "unknown/direct" bucket
  exists to absorb this honestly.
- **Privacy/legal (PIPEDA, Quebec Law 25)**, raised by the blind architect
  reading — session recording and first-party tracking both touch it; worth a
  real check, not assumed clean.
- **Possible delivery-mechanism prior art, flagged in `observations.md`
  (2026-08-29, `ENG-019` shaping, row 97), worth the architect's look rather
  than re-derived here.** `aiorders-api/outgoing-communications/actors/
  brands.ts` already has routed, scheduled `sendPerformanceReport`/
  `sendMonthlySummary` actions, called from a real `processScheduledReports`
  batch path — but both bodies are unimplemented (`// TODO`, always
  `notificationsSent: 0`). The platform already intended owner-facing
  performance reporting once and never finished it. Not assumed as this
  ticket's delivery mechanism (an in-app view is what the PRD scopes), but a
  real candidate if the architect or approver would rather this land as an
  emailed digest instead of or alongside an in-app page.

## Log

- 2026-08-29 `intake → shaped` (product-manager) — sized M, project
  `restaurant-portal` (`aiorders-api` also touched, named in the PRD).
  Ran the full request-readback (`skills/request-readback/SKILL.md`): this
  PM's own reading, grounded in live code read across `aiorders-admin-hub`,
  `config-site-builder` (created this host's missing worktree to do so —
  same recurring gap this board has flagged repeatedly for other projects
  this session), `aiorders-api`, and `restaurant-portal`, plus a blind
  architect reading (subagent, `opus`, raw request + `knowledge/
  business-profile.md` only, no repo access, no exposure to this PM's own
  reading). No material divergence — see PRD Readback for the full
  comparison and the risks the architect raised unprompted (attribution
  honesty, cross-domain stitching, PIPEDA/Law 25, no historical baseline,
  small-restaurant noise, tenant isolation).
  PRD: `agents/product-manager/specs/ENG-020-marketing-roi-attribution-reporting.md`.
  **Held at `shaped`, not advanced to `awaiting-scope`** —
  approver-facing WIP cap (2) re-verified fresh from `inbox/` immediately
  before this decision: `ENG-014`'s and `ENG-015`'s G1s both still read
  `decision:` empty, at cap, same as this board's own header going into this
  pass. G1 content is fully drafted in the PRD's own Decision section and
  ready to raise the moment a slot frees. **1 transition**
  (`intake → shaped`), well under the cap of 4. No cap numbers change —
  `shaped` counts toward neither approver-facing WIP nor machine WIP.
  No `inbox/` item raised this pass (no G1 to notify on yet), so no
  `lib/eng-notify.sh` call.
  `chained: none` — sits at `shaped`, held by the approver-facing WIP cap
  rather than genuinely blocked or waiting on a human for this ticket
  specifically; firing `continue ENG-020` now would only re-discover the
  same cap with no new work to do. Re-check once a
  `decision`/`watch`/`scheduled` pass clears `ENG-014` or `ENG-015`, or via
  a dedicated `continue ENG-020` once either does.
