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
priority: now
state: designed
owner: architect
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-09-03
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-020-marketing-roi-attribution-reporting.md
  design: agents/architect/designs/ENG-020-marketing-roi-attribution-reporting.md
  adrs: [ADR-011, ADR-012]
  review:
  test_plan:
  security_review:
  release:
  pr:
touches_data: true
touches_models: false
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

## 2026-09-03 — scheduled: G1 raised — `shaped → awaiting-scope`

Same stale premise as `ENG-019` (see that ticket's own dated entry for the
full derivation): `agents/eng-manager/config.yaml`'s `approver_limit: 2` is
the department default, but this instance's own override,
`config/config.yaml`, raised it to `unlimited` on 2026-09-02 by the
approver's own explicit, dated decision — never checked by any pass that
held this ticket at `shaped`. Readback already converged (no material
divergence), so straight to G1.

Wrote `inbox/2026-09-03-eng020-g1-scope.md` (recommendation: build now,
scoped to per-restaurant traffic-source/revenue breakdown, exactly as the
PRD proposes). `lib/eng-notify.sh raise` called, exit 0 (logged
`sent: active`, the already-tracked `MODE`-clobber bug, not re-filed).
Stamped `notified: 2026-09-03T11:56:39`.

**1 transition** (`shaped → awaiting-scope`). **Consequence:** no
machine-WIP change. Approver-facing WIP uncapped, so this adds to the queue
without displacing anything — `owner` moves `product-manager → approver`.

`chained: none` — `awaiting-scope` is one of the documented no-chain
conditions (waiting on the approver).

## 2026-09-03 — decision: G1 approved — `awaiting-scope → designed`

`decision` event pass, context `inbox/2026-09-03-eng020-g1-scope.md`.
Reading map for `decision`: steps 4 and 8c, plus step 6 (this answer
advances the ticket into a machine-owned state) and the not-negotiable set
(step 1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four lanes*,
*Guards*). Mode check clean (repo-root `.env` → `MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both exit 0,
clean.

**The answer:** `approved` (`decided: 2026-09-03T15:53:14.495206+00:00`).
No additional comment. Read as accepting the recommendation exactly as
scoped — per-restaurant traffic-source/revenue breakdown on the brand
dashboard, reusing already-captured attribution data, Clarity integration/a
true ROI ratio/AI-SEO isolation/a staff-facing rollup all named as later,
separate work — and as accepting every item in the readback's "Assumed,
correctable here" list since none was corrected. Full reasoning on this
ticket's own PRD, not repeated here.

`ENG-020` moved `awaiting-scope → designed`, `owner: approver →
architect`. PRD `status: approved`, `decided:` stamped
(`agents/product-manager/specs/ENG-020-marketing-roi-attribution-reporting.md`).
Journaled (`decision-journal.md`). Gate item's `## Decision` footer filled
in and moved to `inbox/_handled/`.

**Risks named in the PRD are not resolved by this approval and stay open,
inherited by the architect at `designed`:** attribution honesty (a
last-click number will overstate SEO's specific effect); cross-domain
attribution completeness (`user-tracking.js`'s own README documents the
online-ordering-side wiring as a per-deployment task, not guaranteed live
everywhere — verify actual coverage before presenting numbers as complete);
privacy/legal exposure (PIPEDA and Quebec's Law 25 — session recording and
first-party UTM capture both touch consent questions); no historical
baseline for existing customers; small-restaurant traffic noise; and tenant
isolation (`ENG-015` precedent — acceptance criterion 5 exists because of
it). Restated here so the `continue ENG-020` hop below doesn't have to
re-derive them from the PRD alone.

**Priority column corrected while already touching this row:** this
ticket's own frontmatter has carried `priority: now` since the G1 was
raised; the board index's In-flight table still cached it blank (the same
drift `ENG-016`'s, `ENG-026`'s and `ENG-019`'s decision passes each flagged
or fixed for their own rows) — fixed here as part of this pass's board
update.

**Machine WIP re-checked fresh from every ticket's own frontmatter, not the
cached board header:** `1/1`, occupied by `ENG-024` (`ready-to-ship`, not
yet `shipped`). Irrelevant to this transition — `designed` sits outside the
counted `ready`..`ready-to-ship` range; shaping/design work is backlog
grooming regardless of who holds the slot (`eng_build_loop.md` step 6).

**1 transition** (`awaiting-scope → designed`), well under the cap of 4 —
the actual design work is the architect's own next hop, not attempted
inline here, same precedent `ENG-019`'s, `ENG-026`'s, `ENG-016`'s and
`ENG-015`'s identical G1-approved hand-offs already set. **Consequence:**
ticket now owned by `architect`, outside both the machine-WIP and
approver-WIP counted ranges. Approver-facing WIP uncapped
(`wip.approver_limit: unlimited`); this G1 drops off the "Waiting on the
approver" list.

**Dead-end sweep (scoped to this event):** no other ticket touched, per
this event's own narrower contract (act on the answered gate item, advance
only the ticket it belongs to).

**Notify sweep:** nothing raised this pass — no new gate item written.
Nothing else nudged — `ENG-008`'s and `ENG-010`'s open merge requests are
both still under the 24h nudge threshold (~17.5h and ~23.2h respectively as
of this pass), `ENG-009`'s already carries its one-ever nudge; out of this
event's own scope regardless.

**Observations/proposals filed:** none this pass. The priority-column drift
fixed above is the same mechanism gap already on file from `ENG-016`'s
decision pass, not re-filed.

**Board update** — In-flight table's `ENG-020` row (`state`, `owner`,
`priority` corrected to match the ticket's own frontmatter, `updated`
date); header bullet, "unanswered items" paragraph and count, "Waiting on
the approver" section's `ENG-020` paragraph and item count. Rolled the
oldest of the four now-live dated entries (`decision (ENG-016 rescope
G1)`) to `_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both
exit 0, clean.

`chained: ENG-020` — `designed` is agent-owned (`architect`, via
`tech-design/SKILL.md`, triggered by this exact state); not the approver,
not blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-020`
before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue: design pass — held at `designed` (machine WIP occupied)

`continue` event pass. Reading map: steps 6 and 6b, plus the not-negotiable
set (steps 1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four lanes*,
*Guards*). Mode check clean (repo-root `.env` → `MODE=active`; instance
`config/config.yaml` → `mode:` empty). Pre-pass `lib/eng-gate-check.sh`,
whole-board and scoped `ENG-020`: both exit 0, clean.

**Design work dispatched to an `opus` subagent** (`tech-design/SKILL.md`'s
own model designation, same precedent `ENG-016`'s design pass set), handed
the PRD, this ticket's own evidence packet, `projects.md`,
`engineering-standards.md`, `decision-journal.md`, `observations.md`, and
`ADR-006`/`ADR-010` as the two directly-on-point priors — with the explicit
instruction to verify the handed-over packet against `origin/main` rather
than trust it, same instruction `ENG-016`'s pass gave.

**Independently re-verified the three most load-bearing claims before
trusting them** (same discipline `ENG-016`'s pass applied to its own two):
read `analytics/index.ts` directly off `origin/main` and confirmed it
performs no authentication or authorization of any kind — no
`Authorization` header read anywhere in the file — and confirmed
`supabase/functions/README.md` names `analytics` in neither its consolidated
"no auth check at all" list nor its own per-function Notes; read
`crm/customers.ts` directly and confirmed the seven columns it actually
persists (`first_touch_at/_source/_medium/_campaign`, `first_referrer`,
`last_touch_at/_source`) and confirmed zero references to
`utm_source`/`utm_medium`/`utm_campaign`/`utm_data` anywhere in the file, contra
the PRD, this ticket's own Notes, and `observations.md`'s row 100, all three
of which name those as the persisted columns; read
`_shared/restaurantAccess.ts` and `brand-portal/utils.ts` and confirmed
`verifyRestaurantAccess`'s real signature and its return-an-object (never
throws) behaviour, then spot-checked `customers.ts`/`offers.ts`/`feedback.ts`/
`menus.ts`'s actual call sites and confirmed the design's claim exactly:
`customers.ts` discards the result at 5 sites, `offers.ts`/`feedback.ts`
call it with arguments in the wrong order at 13 sites combined, and both
defects are already inside `ENG-022`'s own fix scope (confirmed by reading
that ticket's own design `Components` table) — not a second, undiscovered
instance of the same bug class, so nothing new to file there. All three
verifications confirmed the design's claims exactly; nothing sent back for
rework.

**Shape:** a new `brand-portal` action (`get_acquisition_report`) plus one
new read-only aggregate RPC, not an extension of the `analytics` function
the PRD named — `analytics/index.ts` has no access check to build AC5 on,
and guarding either the new path alone (a half-guarded function, the
standards' own *failure direction is uniform* defect) or the whole function
(a P0 fix bundled into a P2 ticket, against "no drive-by refactors") were
both wrong. `ADR-011`. Channel classification (an uncontrolled-vocabulary
precedence chain, not a lookup) runs post-query in TypeScript; SQL only
aggregates — `ADR-012`, applying `ADR-010`'s precedent. Full reasoning,
every AC walked individually, and failure-mode table: the design itself.
Process notes, dead ends, and the corrections that didn't change the
design: `agents/architect/notebook/2026-09-03-eng020-design.md`.

**One-way doors: none.** Both `ADR-011` and `ADR-012` are reversible
decisions, decided here rather than escalated — no G2, no `awaiting-decision`.

**`touches_data: true`, `touches_models: false`.** No table/column/row
change, but the one new `SECURITY DEFINER` RPC is a migration, so `database`
is in the work-breakdown chain once this starts building. Confirmed
`touches_models: false` independently — deterministic aggregation and a
pure string/host classifier, no model call anywhere; AI-SEO output is one
attributed channel among others, never generated. `ai-architecture-standards.md`
not read.

**Byproduct P0 finding, filed separately, not absorbed here:** the same
`analytics/index.ts` read that motivated `ADR-011` is a live, unauthenticated
cross-tenant data exposure in its own right — any caller holding the
committed publishable key and a restaurant UUID can read that restaurant's
yearly revenue/orders/customers, no session or ownership check anywhere.
Same bug class as `ENG-022` and `ENG-029`, different function, invisible to
`supabase/functions/README.md`'s own "no auth check at all" list. Per
`eng_build_loop.md` step 3's P0 carve-out (`aiorders-api` is L1, not
internal-lane) and today's own `ENG-029` precedent (an identical
byproduct-of-design-research P0), filed immediately as **`ENG-030`** — see
that ticket's own log — rather than a proposal or absorbed into this
ticket's diff. `ENG-020` does not depend on `ENG-030`; the new report never
touches `analytics`.

**Routing (step 11): would be `ready` — held at `designed` instead.**
Neither an L0 project nor a one-way door, so the skill's own routing reads
`ready`, `owner: eng-manager`. **Machine WIP re-checked fresh from every
ticket's own frontmatter, not the cached board header: `1/1`, occupied by
`ENG-016`** (`state: ready`, not yet `shipped`). Per this board's own
standing precedent for exactly this situation (`ENG-014`, `ENG-017`,
`ENG-019`, `ENG-023`, `ENG-025`, `ENG-026` are all sitting at `designed`
with completed designs for the same reason), `ENG-020` is **held at
`designed`, owner staying `architect`**, rather than writing `state: ready`
into frontmatter while the one slot is occupied — entering `ready` is what
claims the slot, not being designed. Joins that same held-for-slot pool;
whichever of these the machine WIP slot's own priority order (`now` first,
then `next`, then unset, lowest id among ties) selects next gets it when
`ENG-016` ships.

**Two observations filed** (`agents/eng-manager/observations.md`): (1) a
correction to `observations.md`'s own row 100/101-adjacent claims about
`utm_source`-as-column and the mock "Analytics" page being live-in-nav, both
found wrong this pass; (2) `ENG-019` and `ENG-020` will ship two independent
revenue-attribution surfaces on the same portal the same evening — worth
someone's attention before both ship, not a blocker for either. Neither
rises to a proposal — nothing to decide, nothing anyone would be
disappointed to see unactioned.

**Notify sweep:** no new gate item written for `ENG-020` itself (no
one-way door). Swept `inbox/` for the 24h-no-nudge-no-decision nudge
check: nothing crosses it — closest is `eng008` at ~23h (under 24h);
`eng009`/`eng010` already carry their one-ever nudge. (`ENG-030`'s own
incident item is raised and notified separately — see its own log.)

**Dead-end sweep:** out of scope for a `continue` event (narrower contract:
resume the named ticket, don't sweep the board) — not attempted.

**Board update** — `ENG-020`'s In-flight row (`state` stays `designed`,
`links` populated); `ENG-030` added as a new row; header/counts adjusted for
the new ticket and the still-occupied machine-WIP slot.

Post-pass `lib/eng-gate-check.sh`, whole-board and scoped `ENG-020` and
`ENG-030`: see pass notes in `agents/eng-manager/board/_index.md`.

`chained: none` — held by the machine-WIP cap (`1/1`, `ENG-016`, `ready`),
one of the documented no-chain conditions. Re-check via a `decision`/
`watch`/`scheduled` pass once `ENG-016` reaches `shipped`, or via a
dedicated `continue ENG-020`.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.
