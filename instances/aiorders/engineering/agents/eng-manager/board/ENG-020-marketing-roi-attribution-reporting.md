---
id: ENG-020
title: Marketing ROI reporting — traffic source and revenue attribution on the brand dashboard
project: restaurant-portal
type: feature
size: M
time_estimate: a day and a half to two days
time_spent: ~1 build hop (both repos), 3 review+quality rounds (round 1 fail
  — no frontend tests; round 2 fail — AC4 partially tested; round 3 pass),
  1 security round (pass), 1 release-readiness hop (both PRs opened)
time_remaining: none — shipped and verified.
severity: P2
priority: now
state: verified
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-09-05
branch: feat/ENG-020-marketing-roi-attribution-reporting (aiorders-api@cd82579, restaurant-portal@5783a2d)
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-020-marketing-roi-attribution-reporting.md
  design: agents/architect/designs/ENG-020-marketing-roi-attribution-reporting.md
  adrs: [ADR-011, ADR-012]
  review: agents/principal-engineer/reviews/ENG-020.md
  test_plan: agents/qa/test-plans/ENG-020.md
  security_review: agents/security/reviews/ENG-020.md
  release: agents/devops/releases/2026-09-05-ENG-020-aiorders-api-and-restaurant-portal.md
  pr:
    aiorders-api: https://github.com/harsimranwalia/aiorders-api/pull/17
    restaurant-portal: https://github.com/harsimranwalia/restaurant-portal/pull/4
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

## 2026-09-05 — scheduled: claimed the free machine-WIP slot — `designed → ready`

`scheduled` event pass (four-times-daily safety net). Reading map for
`scheduled`: the whole document, never narrowed. Mode check clean
(repo-root `.env` → `MODE=active`). Pre-pass `lib/eng-gate-check.sh`,
whole-board and scoped (`ENG-020`): both exit 0, clean.

**Machine WIP re-checked fresh from every ticket's own frontmatter: `0/1`,
free.** The whole `ENG-019` family (`ENG-019`, `ENG-037`–`039`) reached
`verified` in the two passes immediately before this one — see
`agents/eng-manager/board/_index.md`'s own dated entries. No ticket anywhere
on the board is `blocked`, so step 5 (merge detection) found nothing to
check this pass.

**To-do column (`intake`/`shaped`/`awaiting-scope`) had nothing
machine-actionable**, re-confirmed off every ticket's own frontmatter, not
the board header's cached prose: `ENG-018` stays `shaped`/`priority: hold`,
excluded outright; `ENG-028` sits `awaiting-scope`/`owner: approver`, its G1
(`inbox/2026-09-03-eng028-g1-scope.md`) still unanswered (`decision:`
empty) and already past its one-ever nudge, same for `ENG-016`'s
continue-to-Piece-2 question (`inbox/2026-09-04-eng016-continue-piece2-question.md`)
— neither re-nudged this pass, and neither read as approval by silence.

**Picked from the held-for-slot pool instead**, same shape `ENG-019`'s own
pick used 2026-09-04: of the `designed` tickets with a completed design and
no one-way door (`ENG-014`, `ENG-017`, `ENG-020`, `ENG-021`, `ENG-023`,
`ENG-025`, `ENG-026`, `ENG-027`, `ENG-029`, `ENG-030`, `ENG-035`, `ENG-036`),
`ENG-020`, `ENG-021`, `ENG-026` and `ENG-027` all carry `priority: now` —
lowest id decided.

**No fresh design work — this ticket's routing was already determined and
logged by its own 2026-09-03 `continue` pass**, held at `designed` purely by
the machine-WIP cap since: `tech-design/SKILL.md` step 11 read `ready`,
`owner: eng-manager`; neither an L0 project nor a one-way door (`ADR-011`
and `ADR-012` both architect-decided, reversible, not escalated). That
routing conclusion is re-used here, not re-derived — re-verifying the
design's own code-level claims against current `main` is the `building`
hop's job (same split every prior build hop on this board has drawn), not
this dispatch's. `state: designed → ready`, `owner: architect →
eng-manager`. **Machine WIP: `0/1 → 1/1`, now held by `ENG-020`.**

**1 transition**, well under the cap of 4. Work-breakdown/building is new
implementation work and stays out of a `scheduled` pass — stopped here,
chained instead, same handoff shape every `ENG-016`/`ENG-019` sub-ticket
dispatch already used.

**Dead-end sweep:** no broken chains found — the two passes immediately
prior (`watch ENG-039`, `continue ENG-019`) both carry proper `chained:`
records; no ticket sits in an agent-owned state with no chain note. No
`*-eng-events-dropped.md` file exists for today. `traces/.pending` holds one
already-queued `watch launchd` entry, unrelated to this ticket and not
something this pass drains directly — that queue is `lib/eng-trigger.sh`'s
own mechanism, not re-implemented here.

**Notify sweep:** no new gate item raised this pass (no G2 — already
determined). Nothing crosses the 24h/no-nudge/no-decision threshold beyond
`ENG-028` and `ENG-016`'s Piece-2 question, both already carrying their
one-ever nudge. **Observations/exceptions:** none filed this pass — nothing
noticed outside the ordinary dispatch. **Journal:** n/a — no G1/G2/G3 or
merge request answered this pass.

**Board update:** In-flight row (`state`, `owner`, `updated`); header
paragraph added noting the slot's new occupant. Live file held three dated
entries before this one — oldest (`continue ENG-027`, tech design) rolled to
`_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both
exit 0, clean.

`chained: ENG-020` — `ready` is agent-owned (`eng-manager`), not the
approver, not blocked, not terminal, not held by a cap. Fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-020` before this pass exits.

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.

## 2026-09-05 — continue: build — `ready → building`

`continue` event pass. Reading map: steps 6 and 6b, plus the not-negotiable
set. Mode clean (`MODE=active`). Pre-pass gate-check, scoped and whole-board:
both exit 0.

Built across both repos in one hop, per the `ENG-008`/`ENG-013` precedent for
an `M`-sized multi-repo ticket (no work-breakdown split). Full narrative,
verification detail, and the disposable-container migration test that caught
a real `FULL JOIN` bug before it reached a PR:
`agents/backend/notebook/2026-09-05-eng020-build.md` and
`agents/database/migrations/ENG-020-marketing-roi-attribution-reporting.md`.

Self-tested clean both repos (40/40 Deno tests, `deno check` adds no new
errors; `npm run lint`/`build`/`test` all clean, 14/14). Step 6b artifact
grep (`get_acquisition_report`, `get_acquisition_breakdown`): no conflicting
instruction or map found. Two deferred findings routed off-ticket: a stale
post-`ENG-022` README note (`observations.md`) and a missing
`customers(restaurant_id, created_at)` index (`proposals.md`, per the
design's own instruction not to bundle it here).

Branches pushed, no PR opened (devops's step): `aiorders-api@cd82579`,
`restaurant-portal@2d3dc15`.

**1 transition** (`ready → building`), well under the cap of 4 — review/QA
is a fresh session's work per `eng_build_loop.md`'s "a pass stops after
`building` on purpose." **Consequence:** no WIP-cap change, `building` is
still inside the counted `ready`..`ready-to-ship` range.

Dead-end sweep (scoped to this event): no other ticket touched. Notify
sweep: no new gate item this pass. Post-pass gate-check, scoped and
whole-board: both exit 0.

`chained: ENG-020` — `building` is agent-owned, not the approver, not
blocked, not terminal, not capped. Fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-020` before this pass exits.

## 2026-09-05 — continue: review+quality combined hop, round 1 — REVIEW pass, QUALITY fail — stays `building`

`continue` event pass, context `ENG-020`. Reading map: steps 6 and 6b, plus
the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
lanes*; *Guards*). Mode clean (`MODE=active`). Pre-pass `eng-gate-check.sh`,
scoped and whole-board: both exit 0. Acted as principal-engineer and qa on
this combined hop, per this board's own standing precedent — no delegation to
a subagent.

**Code review: PASS, round 1, both repos.** 0/10 automatic failures. Both
ADRs (`ADR-011`, `ADR-012`) confirmed honored against the actual diff. AC5
(tenant isolation) mutation-tested, not read-and-trusted: forcing the access
check off failed exactly the one denial test. Independently re-ran both
repos' suites fresh — `aiorders-api` 40/40, `restaurant-portal` 14/14 — and
`deno check`/`npm run lint`/`npm run build`, all matching the build hop's own
account with zero new issues. Three non-blocking findings. Receipt written:
`agents/principal-engineer/reviews/ENG-020.md`, `links.review` set. Full
reasoning: `agents/principal-engineer/notebook/2026-09-05-review-log.md`.

**Quality gate: FAIL, round 1 — first real run on this ticket.**
`acquisition.ts`/`channels.ts` (`aiorders-api`) are thoroughly covered (the
same 40 tests review re-ran). But **AC1, AC2, AC3, and AC4 have no test at
the layer they're actually written against** — what the restaurant owner
*sees*. `restaurant-portal`'s diff (`Index.tsx`, `ChannelBreakdown.tsx`)
adds no `*.test.tsx` file at all, despite this exact repo already carrying
direct, repeated precedent for testing this shape of component
(`BroadcastReport.test.tsx` most directly — a report page fetching data and
asserting rendered totals/conditional sections, with test names tagged to
the AC they cover). Not a manual-verification case: the test runner exists,
the pattern exists next to this diff, nothing here is unreachable by
automation. Three gaps filed, each with a specific fix a build hop can apply
in one round: **Gap 1** (AC1/AC3) — no test renders the channel table, the
totals, the always-present `direct_unknown` row, the empty state, or the
low-volume column toggle. **Gap 2** (AC2) — `resolveRange`'s own date-window
math is untested, and nothing exercises range-change → refetch → updated
figures end to end. **Gap 3** (AC4) — the organic-search honesty disclaimer,
the coverage sentence, and the low-volume caveat are unverified to actually
render under the conditions the design specifies. AC5 passes, mutation-
verified. Test plan written regardless of verdict, per its own documented
receipt exception: `agents/qa/test-plans/ENG-020.md`, `links.test_plan` set.
Full reasoning: `agents/qa/notebook/2026-09-05-coverage-gaps.md`.

**0 net transitions** — ticket entered this hop at `building`/`eng-manager`
and leaves it there, same bookkeeping this board used for `ENG-033`'s own
round 3 (review pass, quality fail, on a ticket's first quality run): the
gate that concluded against the ticket is what the state reflects, not the
one that happened to pass in the same hop. **Consequence:** no WIP-cap
change — `building` is still inside the counted `ready`..`ready-to-ship`
range, still the ticket holding the 1/1 machine-WIP slot. Owner stays
`eng-manager`, matching this ticket's own established multi-repo-single-hop
convention (never delegated to a `backend`/`frontend` frontmatter identity
across either of its two prior build-hop entries) rather than switching to
`frontend` for a fix that's scoped to one repo.

**Next hop, fully specified so a third gate round isn't needed:** add
`ChannelBreakdown.test.tsx`/`Index.test.tsx` (or one combined file) per Gap
1/Gap 3's cases, export and unit-test `resolveRange` per Gap 2, then review
round 2 re-confirms the diff since this round (code review's own PASS is not
re-litigated) and the quality gate re-checks the acceptance table fresh.

**Dead-end sweep (scoped to this event):** no other ticket touched. **Notify
sweep:** nothing raised this pass (no gate item — this is an internal
machine-gate round, not approver-facing); both open `inbox/` items
(`eng028`, `eng016`'s Piece-2 question) already carry their one-ever
`nudged:`, neither re-nudged. **Observations/exceptions:** none filed — no
`exception-request:` found, nothing noticed outside this ticket's own scope.
**Journal:** n/a, no G1/G2/G3 or merge request answered this pass.

**Board update:** In-flight row unchanged (`state`/`owner` both stay
`building`/`eng-manager`), `updated` date unchanged (same day). Live file
held three dated entries before this one; rolled the oldest (`scheduled:
claimed the free machine-WIP slot`) to `_index-archive.md` per the keep-three
rule.

Post-pass `eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both
exit 0, clean.

`chained: ENG-020` — `building` is agent-owned (the fix hop is the next
step), not the approver, not blocked, not terminal, not held by a cap. Fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-020` before this pass exits.

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.

## 2026-09-05 — continue: fix hop for round-1 quality gaps — stays `building`

`continue` event pass, context `ENG-020`. Reading map: steps 6 and 6b, plus
the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
lanes*; *Guards*). Mode clean (`MODE=active`). Pre-pass `eng-gate-check.sh`,
scoped and whole-board: both exit 0. `restaurant-portal` worktree clean at
`2d3dc15` before starting (no prior pass died mid-work); `aiorders-api`
worktree clean but for its own standing untracked `deno.lock`, already noted,
untouched — this hop never opened that repo, since round 1's gaps were all
`restaurant-portal`-side.

**Closed all three gaps from `agents/qa/test-plans/ENG-020.md` per the prior
round's own fully-specified next hop** — no re-derivation, the fix list was
already exact:

- `src/components/acquisition/ChannelBreakdown.test.tsx` (Gap 1, AC1/AC3):
  one row per channel in fixture order, `direct_unknown` rendered even at
  zero, a channel the caller didn't include never appears as a row, and the
  `low_volume`-gated "Share of revenue" column shown/suppressed both ways.
- `src/pages/acquisition/Index.test.tsx` (Gaps 1/3/2's rendering case,
  AC1/AC2/AC3/AC4): totals rendered from a fixture, empty state, error state
  (the `{success:false}` contract shape, not a raw rejection), the
  organic-search disclaimer shown/hidden by whether `channels` includes
  `organic_search`, and range-change → refetch → updated totals.
- `src/pages/acquisition/dateRange.ts` + `dateRange.test.ts` (Gap 2):
  `resolveRange` unit-tested per preset (`vi.setSystemTime`-fixed clock, each
  expected boundary built independently via the same Date primitives rather
  than calling the function under test, so a wrong offset would still be
  caught).

**One structural deviation from the fix note, both driven by things only
visible once the tests were actually run, not by design taste:**

1. **`resolveRange` moved out of `Index.tsx` into its own module rather than
   staying in place merely `export`ed.** Exporting it alongside the
   page's default export tripped
   `react-refresh/only-export-components` (a file exporting both a
   component and a plain function breaks Vite's fast-refresh boundary) — a
   new lint warning `npm run lint` didn't have before this hop, which would
   have failed the same "zero new issues in a touched file" bar round 1's
   own review applied. Extracting to `src/pages/acquisition/dateRange.ts`
   resolved it at the source rather than suppressing the rule; re-ran lint
   after, confirmed back to the exact pre-existing baseline (62 errors/34
   warnings, matching round 1's review account exactly).
2. **Radix `Select` needed a `scrollIntoView` polyfill to test at all.**
   jsdom implements no `scrollIntoView`; `SelectContent`'s own mount effect
   calls it on the selected item, and the uncaught `TypeError` tore down the
   entire React tree (silently, until traced — the failure surfaced as
   `getAcquisitionReport` never being called a second time, not as a visible
   error). Fixed with `Element.prototype.scrollIntoView = vi.fn()` scoped
   to `Index.test.tsx` alone via `beforeAll` (this repo's `setup.ts` already
   polyfills `matchMedia`/`ResizeObserver`/`IntersectionObserver` for the
   same reason — jsdom gaps other components hit on mount — but no other
   test here opens a Radix `Select`, so the polyfill stayed local rather than
   going in the shared file for one caller). The range-change interaction
   itself drives the real component: focus the trigger, `keyDown: Enter` to
   open (Radix's native keyboard path, not a pointer event jsdom can't
   synthesize), then click the resulting `role="option"` node.

**Fixture design note, since it cost one throwaway iteration:**
`StatsCard`'s totals and `ChannelBreakdown`'s table cells both render a bare
number as an element's entire text content, so a first draft that reused a
totals figure as a channel's own figure (e.g. one channel carrying the same
customer count as the grand total) made `getByText` ambiguous between the
two and failed three tests that had nothing wrong with the component under
test. Fixed by keeping every fixture's per-channel numbers distinct from its
own totals; the acceptance-relevant fixture (two channels summing to
`{40, 95, 3120.5}`) mirrors the exact numbers principal-engineer's own round
1 review hand-traced, so the two receipts describe the same scenario rather
than two unrelated ones.

**Self-tested clean:** `npm run test` — 29/29 across 9 suites (14
pre-existing + 15 new: 5 in `ChannelBreakdown.test.tsx`, 10 across
`Index.test.tsx`/`dateRange.test.ts`), no regression. `npm run lint` — 0 new
issues, exact pre-existing baseline (62 errors/34 warnings, all outside this
diff). `npm run build` — clean, same pre-existing chunk-size-only warning.
Did not re-run `aiorders-api`'s suite — untouched this hop, round 1's own
40/40 stands.

Committed `f129f14` (`restaurant-portal`, one commit, 5 files) on the
existing `feat/ENG-020-marketing-roi-attribution-reporting` branch and
pushed to `origin` — same branch round 1 opened, no new PR (still devops's
step, unchanged from round 1). `aiorders-api` stays at `cd82579`, untouched.

**0 net transitions** — enters and leaves this hop at `building`/
`eng-manager`, same bookkeeping this ticket's own round-1 entry used: the
fix is what a gate asked for, not itself a gate, so the state doesn't move
until the next review+quality round rules on it.

**Dead-end sweep (scoped to this event):** no other ticket touched. **Notify
sweep:** nothing raised this pass (no gate item — internal fix hop, not
approver-facing); both open `inbox/` items (`eng028`, `eng016`'s Piece-2
question) already carry their one-ever `nudged:`, neither re-nudged.
**Observations/exceptions:** none filed — nothing noticed outside this
ticket's own scope; the `scrollIntoView`/fast-refresh notes above are logged
here because they're this ticket's own receipts, not filed again as
observations. **Journal:** n/a, no G1/G2/G3 or merge request answered this
pass.

**Board update:** In-flight row unchanged (`state`/`owner` both stay
`building`/`eng-manager`), `updated` date unchanged (same day). Live file
already held three dated entries before this one (the keep-three rule was
already satisfied by the immediately-prior round-1 entry's own roll); no
roll needed this pass.

Post-pass `eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both exit
0, clean.

`chained: ENG-020` — `building` is agent-owned (review+quality round 2 is
the next step), not the approver, not blocked, not terminal, not held by a
cap. Fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-020` before this pass exits.

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.

## 2026-09-05 — continue: review+quality combined hop, round 2 — REVIEW pass, QUALITY fail (narrower) — stays `building`

`continue` event pass, context `ENG-020`, per prior pass's own
`chained: ENG-020`. Reading map for `continue`: steps 6 and 6b, plus the
not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
lanes*; *Guards*). Mode check clean (`MODE=active`). Pre-pass
`eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both exit 0, clean.
Acted as principal-engineer and qa on this combined hop, same standing
precedent this ticket's own round 1 used — no delegation to a subagent.

Worktrees re-checked fresh before anything else: `git fetch origin` both
repos. `restaurant-portal` HEAD `f129f14`, matching the fix hop's own
checkpoint exactly; `aiorders-api` HEAD `cd82579`, matching round 1's. `git
log HEAD..origin/main` empty in both — no drift, no other pass landed work
here since the fix hop.

Ran the combined review+quality hop scoped to the diff since round 1's
reviewed commit (`code-review-gate/SKILL.md` step 9: round 1's own PASS
stands, not re-litigated): `restaurant-portal@2d3dc15..f129f14` (5 files,
270/21 — `ChannelBreakdown.test.tsx`, `Index.test.tsx`,
`dateRange.ts`/`.test.ts`, the `resolveRange` extraction out of `Index.tsx`).
`aiorders-api` carries zero commits since round 1 — nothing to review there
this round.

**Code review: PASS, round 2, second consecutive pass.** 0/10 automatic
failures. The `resolveRange` extraction confirmed behaviour-preserving by
direct diff inspection (every line of the function body byte-identical
between the deleted and added hunks), not inferred from the tests passing.
Independently re-ran `restaurant-portal`'s suite fresh — 29/29, 9 suites (14
pre-existing + 15 new) — plus `npm run lint` (62 errors/34 warnings, exactly
round 1's baseline, zero in any file this round touches, confirmed by
grepping the full lint output for `acquisition`/`dateRange`) and `npm run
build` (clean, same pre-existing chunk-size warning). **Two mutation tests
on this round's only behaviours genuinely new to automated coverage** (no
new production decision logic this round, only tests plus a mechanical
move): mutated `dateRange.ts`'s `30d` offset (`- 30` → `- 29`) and reran
`dateRange.test.ts` — exactly the `30d` case failed, the other three stayed
green; mutated `Index.tsx`'s `useQuery` `queryKey` to drop `preset` and
reran `Index.test.tsx` — exactly the AC2 refetch test failed (timed out on
the second call), the other five stayed green. Both restored via backup,
`git status --short` empty after each. Also confirmed the
`Element.prototype.scrollIntoView` polyfill in `Index.test.tsx`'s `beforeAll`
can't leak into other test files — this repo sets no `test.isolate: false`,
so vitest's default per-file isolation applies. Receipt rewritten (per this
board's own convention — the receipt file holds only the latest passing
round, not an accumulation):
`agents/principal-engineer/reviews/ENG-020.md` (round 2), `links.review`
re-set. Full reasoning there.

**Quality gate: FAIL, round 2 — narrower than round 1.** Fresh re-check of
the whole acceptance table, not just confirmation that the three named gaps
closed. **Gaps 1–3 (AC1/AC3 rendering, AC2) close this round** — the new
tests cover exactly what they specified, cross-checked line by line against
the actual `Index.tsx`/`ChannelBreakdown.tsx` markup, not just trusted by
test name. **AC4 is only partly closed, and this is a real finding, not a
formality**: round 1's own Gap 3 narrative named three unverified things
(the organic-search disclaimer, the coverage sentence, the low-volume
caveat) but its "Specific fix" bullet asked for tests covering only the
first — the round-1 fix hop built exactly what the bullet specified, and the
other two shipped in this same round's diff still untested. Confirmed by
grep, not assumed: `coverage.attributed_pct` and `low_volume` are set in
every `Index.test.tsx` fixture but never read back with
`getByText`/`findByText` anywhere; `low_volume: true` is never set in any
fixture at all, so the caveat sentence's own render branch has zero test
runs reaching it. The architect's own design (`agents/architect/designs/
ENG-020-*.md` → "Risks" → "Attribution honesty — AC4") names these as two of
AC4's four concrete mechanisms, not a separate concern from the disclaimer —
so this is the same acceptance criterion, still short one verified
mechanism and its small-restaurant counterpart. Filed as **Gap 4**, blocking,
fully specified (two `Index.test.tsx` additions, no production-code change
implied): `agents/qa/test-plans/ENG-020.md`.

Filed one observation (`agents/eng-manager/observations.md`) on the process
shape that let this ride: a gap's own narrative naming more than its
"Specific fix" bullet delivers, and a fix hop that reasonably follows the
bullet literally, leaves the rest silently unclosed. Second occurrence of
this general shape after `ENG-038`'s round-3→4 finding (different immediate
mechanism — that one was an unnumbered gap folded into a sibling's blocking
status); not yet a proposal, a third occurrence would make it one.

Per `code-review-gate/SKILL.md` step 9 and this ticket's own round-1
precedent (review pass + quality fail → stays at `building`, review's own
pass stands and is not re-litigated next round): **0 net transitions** —
ticket entered this hop at `building`/`eng-manager` and leaves it there.
Not a third-failed-round escalation — that clause counts code review's own
failures, and review has now passed twice running; the quality gate carries
no equivalent three-strike rule anywhere in this department's docs (per
`ENG-038`'s own round-4 precedent on this exact question). **Consequence:**
no WIP-cap change — `building` is still inside the counted
`ready`..`ready-to-ship` range, still the ticket holding the 1/1 machine-WIP
slot. Owner stays `eng-manager`, same multi-repo-single-hop convention this
ticket has used throughout.

**Next hop, fully specified so a third quality round isn't needed:** add the
two `Index.test.tsx` cases Gap 4 names (coverage-sentence rendering with the
fixture's real numbers; a `low_volume: true` fixture asserting the caveat
renders, confirming the existing default fixture asserts it doesn't), then
review round 3 re-confirms the diff since round 2 (round 2's own PASS stands)
and the quality gate re-checks the table fresh once more.

**Dead-end sweep (scoped to this event):** no other ticket touched. **Notify
sweep:** nothing raised this pass (no gate item — an internal machine-gate
round, not approver-facing); both open `inbox/` items re-read fresh
(`eng028`: `notified: 2026-09-03T16:10:27`, `nudged: 2026-09-04T09:13:37`;
`eng016`'s Piece-2 question: `notified: 2026-09-04T10:58:06`, `nudged:
2026-09-05T09:31:45`) — both already carry their one-ever `nudged:`
(`max_pings_per_item: 2`), neither re-nudged, neither carries a `decision:`.
**Observations/exceptions:** one observation filed (above); no
`exception-request:` found. **Journal:** n/a, no G1/G2/G3 or merge request
answered this pass.

**Board update:** In-flight row unchanged (`state`/`owner` both stay
`building`/`eng-manager`), `updated` date unchanged (same day). Live file
already held three dated entries before this one (satisfied by the round-1
entry's own roll); no roll needed this pass.

Post-pass `eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both exit
0, clean.

`chained: ENG-020` — `building` is agent-owned (the Gap 4 fix hop is the
next step), not the approver, not blocked, not terminal, not held by a cap.
Fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-020` before this pass exits.

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.

## 2026-09-05 — continue: fix hop for round-2 quality gap (Gap 4) — stays `building`

`continue` event pass, context `ENG-020`. Reading map: steps 6 and 6b, plus
the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
lanes*; *Guards*). Mode check clean: instance `config/config.yaml` →
`mode:` empty, business-os `.env` → `MODE=active`. Pre-pass
`eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both exit 0, clean.
`restaurant-portal` worktree clean at `f129f14` before starting, matching
round 2's own reviewed checkpoint exactly — no prior pass died mid-work.
`aiorders-api` untouched, still `cd82579` — Gap 4 is `restaurant-portal`-only,
same as every gap on this ticket so far.

**Closed the one gap `agents/qa/test-plans/ENG-020.md` (round 2) named, per
that report's own fully-specified fix — no re-derivation.** Two additions to
`src/pages/acquisition/Index.test.tsx`:

- `renders the coverage sentence with the fixture's actual numbers (AC4)` —
  asserts `screen.findByText(/61% of orders in this period could be traced to
  a source/)` against the existing `baseReport()` default (`attributed_pct:
  61`), the fixture already in use elsewhere in this file.
- A show/suppress pair for the low-volume caveat, mirroring
  `ChannelBreakdown.test.tsx`'s own existing pattern for the same field one
  component over (cited by the gap itself, not re-derived): `renders the
  low-volume caveat when low_volume is true (AC4)` (`baseReport({ low_volume:
  true })`, a value no existing fixture in this file had used) and `does not
  render the low-volume caveat when low_volume is false (AC4)` — the negative
  case, waiting for the loaded totals (`findByText('40')`) before asserting
  the caveat's absence, so the assertion can't pass merely because the query
  is still loading.

**No deviation from the fix note this round** — unlike round 1's fix hop
(the `resolveRange` extraction and the `scrollIntoView` polyfill), both
additions are test-only assertions against text already rendered by
production code that round 1 shipped; nothing here changes what
`Index.tsx` renders. Step 6b artifact grep not run — this hop introduces no
artifact (no receipt path, state name, config key, or file another agent is
told to produce), only two test assertions on existing UI text, so there is
no rule-about-an-artifact for the grep to check.

**Self-tested clean:** `npm run test -- --run` — 32/32 across 9 suites (29
pre-existing + 3 new), no regression. `npm run lint` — 0 issues in
`acquisition`/`dateRange` (confirmed by grep on the full lint output, not
assumed), 62 errors/34 warnings overall — the exact pre-existing baseline
every prior round on this ticket has recorded. `npm run build` — clean,
same pre-existing chunk-size-only warning. Did not re-run `aiorders-api` —
untouched this hop, round 1's own 40/40 stands.

Committed `5783a2d` (`restaurant-portal`, one commit, one file:
`Index.test.tsx`) on the existing
`feat/ENG-020-marketing-roi-attribution-reporting` branch and pushed to
`origin` — same branch every prior round used, no new PR (still devops's
own step, unchanged).

**0 net transitions** — enters and leaves this hop at `building`/
`eng-manager`, same bookkeeping every fix hop on this ticket has used: a fix
a gate asked for isn't itself a gate, so the state doesn't move until the
next review+quality round rules on it. **Consequence:** no WIP-cap change —
`building` is still inside the counted `ready`..`ready-to-ship` range, still
the ticket holding the 1/1 machine-WIP slot. Owner stays `eng-manager`, same
multi-repo-single-hop convention this ticket has used throughout.

**Dead-end sweep (scoped to this event):** no other ticket touched. **Notify
sweep:** nothing raised this pass (no gate item — internal fix hop, not
approver-facing); both open `inbox/` items re-read fresh this pass —
`eng028` (`notified: 2026-09-03T16:10:27`, `nudged: 2026-09-04T09:13:37`) and
`eng016`'s Piece-2 question (`notified: 2026-09-04T10:58:06`, `nudged:
2026-09-05T09:31:45`) — both already carry their one-ever `nudged:`, neither
carries a `decision:`, neither re-nudged (`max_pings_per_item: 2`, one used).
`traces/.pending` holds the same single already-queued `watch launchd` entry
noted by round 1's own review pass, unrelated to this ticket and not drained
directly by this pass. No `*-eng-events-dropped.md` file exists for today.
**Observations/exceptions:** none filed — no `exception-request:` found, and
nothing noticed outside this ticket's own scope (no deviation this round,
unlike round 1's fix hop, so nothing new to log as a receipt or an
observation). **Journal:** n/a, no G1/G2/G3 or merge request answered this
pass.

**Board update:** In-flight row unchanged (`state`/`owner`/`priority` all
stay `building`/`eng-manager`/`now`), `updated` date unchanged (same day).
Live file (`_index.md`) held three dated entries before this one, all three
this ticket's own — oldest (`continue (ENG-020): review+quality combined
hop, round 1`) rolled to `_index-archive.md` per the keep-three rule.

Post-pass `eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both exit
0, clean.

`chained: ENG-020` — `building` is agent-owned (review+quality round 3 is
the next step), not the approver, not blocked, not terminal, not held by a
cap. Fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-020` before this pass exits.

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.

## 2026-09-05 — continue: review+quality combined hop, round 3 — BOTH PASS — `building → in-security`

`continue` event pass, context `ENG-020`, per prior pass's own
`chained: ENG-020`. Reading map for `continue`: steps 6 and 6b, plus the
not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
lanes*; *Guards*). Mode check clean (repo-root `.env` → `MODE=active`).
Ticket's own log and frontmatter read fresh before touching anything: clean
history, no stale `blocked_from`, no hold-priority conflict, round-2 receipts
present and non-empty. Acted as principal-engineer and qa on this combined
hop, same standing precedent this ticket's own rounds 1–2 used — no
delegation to a subagent.

Worktrees re-checked fresh before anything else: `git fetch origin` both
repos. `restaurant-portal` HEAD `5783a2d`, matching the round-2 fix hop's own
checkpoint exactly; `aiorders-api` HEAD `cd82579`, matching round 1's. `git
log HEAD..origin/main` empty in both — no drift, no other pass landed work
here since the round-2 fix hop. `aiorders-api` still carries its own standing
untracked `deno.lock`, already noted across every prior round, untouched.

Ran the combined review+quality hop scoped to the diff since round 2's
reviewed commit (`code-review-gate/SKILL.md` step 9: rounds 1–2's own PASS
stand, not re-litigated): `restaurant-portal@f129f14..5783a2d` (1 file, 25
insertions — three new `it()` blocks in `Index.test.tsx`, no production
code). `aiorders-api` carries zero commits since round 1 — nothing to review
there this round.

**Code review: PASS, round 3, third consecutive pass.** 0/10 automatic
failures. Read the three new tests against `Index.tsx:102-114` directly, not
trusted from the gap report — each assertion matches what the design's own
AC4 "Attribution honesty" section (mechanism 4) and the QA gap actually
named. Independently re-ran `restaurant-portal`'s suite fresh — 32/32, 9
suites (29 pre-existing + 3 new) — plus `npm run lint` (62 errors/34
warnings, exactly the baseline every prior round recorded, zero in
`acquisition`/`dateRange`) and `npm run build` (clean, same pre-existing
chunk-size warning). **Two mutation tests, one per new assertion**, mirroring
this ticket's own rounds 1–2 discipline: flipped `Index.tsx`'s
`{data.low_volume && (...)}` to `{true && (...)}` and reran
`Index.test.tsx` — exactly the "does not render... when low_volume is false"
test failed, the other 8 (including "renders... when true") stayed green;
changed the coverage sentence's `{data.coverage.attributed_pct}%` to a
hardcoded `{99}%` and reran — exactly the "renders the coverage sentence"
test failed (its regex is pinned to `61%`), the other 8 stayed green. Both
mutations restored via a matching `Edit`, `git status --short` empty after
each. Receipt rewritten (per this board's own convention — latest passing
round only): `agents/principal-engineer/reviews/ENG-020.md` (round 3),
`links.review` re-set. Full reasoning there.

**Quality gate: PASS, round 3 — fresh re-check of the whole acceptance
table, not just confirmation that Gap 4 closed.** AC1, AC2, AC3, AC5 stand
from round 2 (re-confirmed, nothing in this round's diff touches them). AC4
— the last open piece — closes this round: the coverage-sentence test
matches the fixture's actual `attributed_pct: 61`, and the low-volume-caveat
show/suppress pair reaches both branches of `Index.tsx`'s `data.low_volume`
conditional for the first time. **All five acceptance criteria now pass.**
`agents/qa/test-plans/ENG-020.md` updated in place: acceptance table, Gap 4
marked closed, `## Not automated` cleared, Round 3 result entry added,
`last_result: pass`.

Per `code-review-gate/SKILL.md` step 9, both gates passing on the same diff:
**ticket advances `building → in-security`, owner `eng-manager → security`.**
**1 transition**, well under the cap of 4 — the security gate itself is the
next session's work, per this document's "a pass stops after `building` on
purpose" and this ticket's own established one-hop-per-gate cadence.
**Consequence:** no WIP-cap change — `in-security` is still inside the
counted `ready`..`ready-to-ship` range, still the ticket holding the 1/1
machine-WIP slot.

**Dead-end sweep (scoped to this event):** no other ticket touched. **Notify
sweep:** nothing raised this pass (no gate item — an internal machine-gate
round, not approver-facing); both open `inbox/` items re-read fresh
(`eng028`, `eng016`'s Piece-2 question) — both already carry their one-ever
`nudged:`, neither carries a `decision:`, neither re-nudged.
**Observations/exceptions:** none filed — no `exception-request:` found,
nothing noticed outside this ticket's own scope. **Journal:** n/a, no
G1/G2/G3 or merge request answered this pass.

**Board update:** In-flight row (`state: building → in-security`,
`owner: eng-manager → security`), `updated` date unchanged (same day). Live
file already held three dated entries before this one (satisfied by the
round-1 entry's own roll); no roll needed this pass.

Post-pass `eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both exit
0, clean.

`chained: ENG-020` — `in-security` is agent-owned (security), not the
approver, not blocked, not terminal, not held by a cap. Fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-020` before this pass exits.

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.

## 2026-09-05 — continue: security gate, round 1 — PASS — `in-security → ready-to-ship`

`continue` event pass, context `ENG-020`, per prior pass's own
`chained: ENG-020`. Reading map for `continue`: steps 6 and 6b, plus the
not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
lanes*; *Guards*). Mode check clean (repo-root `.env` → `MODE=active`).
Pre-pass `eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both exit
0, clean. Acted as `security` on this hop, per `skills/security-gate/SKILL.md`
(no delegation to a subagent).

Worktrees re-checked fresh before anything else: `git fetch origin` both
repos. `restaurant-portal` HEAD `5783a2d`, matching round 3's own reviewed
checkpoint; `aiorders-api` HEAD `cd82579`, matching round 1's build hop —
`git log HEAD..origin/main` empty in both, no drift.

**Threat-modelled the change** (four questions), **walked OWASP A01–A10**
against the full diff in both repos (not just this ticket's own account of
it — read `acquisition.ts`, `channels.ts`, the migration, `index.ts`'s auth
block, `utils.ts`'s actual `verifyRestaurantAccess` signature, and both new
frontend files directly off disk), **confirmed the LLM checklist n/a**
(`touches_models: false`, independently verified — deterministic aggregation
and a pure string classifier, no model/agent/tool/MCP/RAG anywhere),
**scanned for secrets** (diff and full branch history, both repos: zero
hits) and **dependencies** (zero new or bumped: `restaurant-portal/package.json`
untouched, `recharts` pre-existing; `aiorders-api` has no `package.json`, no
new `npm:` specifier), and **read the negative-case test directly**
(`acquisition.test.ts`'s wrong-tenant test, plus code review's own round-1
mutation test forcing the access check off) rather than trusting the
receipts' own account of it. Full reasoning, the OWASP table, and the SOC 2
evidence-trail check: `agents/security/reviews/ENG-020.md`.

**Verdict: PASS.** No blocking finding. Access control uses the *correct*
`verifyRestaurantAccess(restaurant_id, supabase, user)` call shape (matching
`menus.ts`/`catering.ts`/`restaurants.ts`/`onlineOrders.ts`, not the broken
shape `feedback.ts`/`offers.ts` carry), checks `.hasAccess` before any query,
and is mutation-verified rather than merely read-and-trusted. The new RPC is
fully parameterised (no string-built SQL); the frontend renders exclusively
via JSX text interpolation (zero `dangerouslySetInnerHTML`/`innerHTML` in
either new component), so the one attacker-reachable text
(public-signup-supplied `first_touch_source`, surfaced as an `other:<source>`
channel label when unrecognised) is stored-but-inert, not stored XSS. No
secret, no new dependency.

**One non-blocking finding, filed rather than silently passed over:**
`verifyRestaurantAccess` (unchanged by this diff, shared by every other
`brand-portal` handler) answers an existence question the design's own
Interfaces table says a denial doesn't — a restaurant that doesn't exist gets
`'Restaurant not found'`, one that exists but isn't the caller's gets
`'Access denied to this restaurant'`, and `acquisition.ts` forwards
`access.error` verbatim. Pre-existing, shared verbatim by
`menus.ts`/`catering.ts`/`restaurants.ts`/`onlineOrders.ts`, not introduced or
worsened here, and low exploit value (a restaurant UUID isn't a credential;
the existence bit exposes nothing about the restaurant's data). Not filed as
a proposal — narrower than that bar, and fixing the shared helper's message
granularity for one new caller while every sibling keeps the coarser
behaviour would recreate the half-guarded-function shape `ADR-011` already
declined on this same ticket for a different reason. Logged for the record:
`agents/security/notebook/2026-09-05-findings.md`.

Per `skills/security-gate/SKILL.md` step 9, receipt written **only on this
pass verdict** (`agents/security/reviews/ENG-020.md`), `links.security_review`
set on the ticket in the same edit. **1 transition** (`in-security →
ready-to-ship`), well under the cap of 4 — release readiness is the next
session's own hop, per this document's "a pass stops after `building` on
purpose" extended to every heavy gate. **Consequence:** no WIP-cap change —
`ready-to-ship` is still inside the counted `ready`..`ready-to-ship` range,
still the ticket holding the 1/1 machine-WIP slot. Owner `security → devops`.

**Dead-end sweep (scoped to this event):** no other ticket touched. **Notify
sweep:** nothing raised this pass (a machine-gate pass verdict, not
approver-facing — the eventual G3 is `release-runner`'s own job at the next
hop); both open `inbox/` items re-read fresh (`eng028`, `eng016`'s Piece-2
question) — both already carry their one-ever `nudged:`, neither carries a
`decision:`, neither re-nudged. **Observations/exceptions:** none filed — no
`exception-request:` found; the one finding above is a security-notebook
entry, not an observation or a proposal (reasoning above). **Journal:** n/a,
no G1/G2/G3 or merge request answered this pass.

**Board update:** In-flight row (`state: in-security → ready-to-ship`,
`owner: security → devops`, `links` populated), `updated` date unchanged
(same day). Live file already held three dated entries before this one
(satisfied by the round-1 entry's own roll); no roll needed this pass.

Post-pass `eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both exit
0, clean.

`chained: ENG-020` — `ready-to-ship` is agent-owned (`devops`, via
`release-runner/SKILL.md`), not the approver, not blocked, not terminal, not
held by a cap. Fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-020` before this pass exits.

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.

## 2026-09-05 — continue: release-readiness — `ready-to-ship → blocked`, both PRs opened

`continue` event pass, context `ENG-020`, per prior pass's own
`chained: ENG-020`. Reading map for `continue`: steps 6 and 6b, plus the
not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
lanes*; *Guards*). Mode check clean (repo-root `.env` → `MODE=active`).
Ticket's own log and frontmatter read fresh before touching anything: clean
history, no stale `blocked_from`, no hold-priority conflict, all four
upstream gate receipts present and passing. Acted as `devops` on this hop,
per `skills/release-runner/SKILL.md` (no delegation to a subagent).

**Step 1 (window):** both `aiorders-api` and `restaurant-portal` are L1
(`agents/eng-manager/config/projects.md`, re-confirmed directly) — no window
check applies to either.

**Step 2 (upstream gates) — all four re-read fresh from the receipt files,
not from the ticket log's own account, all passing:**
`agents/principal-engineer/reviews/ENG-020.md` (round 3, `verdict: pass`,
third consecutive pass), `agents/qa/test-plans/ENG-020.md` (round 3,
`last_result: pass`, all 5 acceptance criteria), `agents/security/reviews/
ENG-020.md` (round 1, `verdict: pass`), and `agents/database/migrations/
ENG-020-marketing-roi-attribution-reporting.md` (`Gate verdict: pass`,
rollback tested against a disposable replica).

**Step 3 (readiness gate):**

- *Rollback:* the migration's own `DROP FUNCTION IF EXISTS
  public.get_acquisition_breakdown(...)` was actually run against a
  disposable Postgres replica during the migration doc's own verification,
  not just asserted — a follow-up `pg_proc` lookup confirmed zero rows after.
  Neither repo's diff changes existing behaviour, so reverting the merge
  fully undoes either side: `restaurant-portal`'s `deploy-cf.yml`
  (push-to-`main`-triggered, confirmed by reading the workflow file) redeploys
  the prior build on a revert, same reasoning `ENG-032`'s and `ENG-039`'s own
  release-readiness hops already established for this exact repo;
  `aiorders-api` has no CI at all (`git ls-tree -r origin/main --name-only |
  grep -i workflow` — empty, confirmed fresh), so a revert-and-remerge is
  sufficient there too.
- *Observability:* both new RPC failure branches (not-found, generic error)
  log server-side (`console.error`) before returning a fixed client message
  (security review, A09) — confirmed reading `acquisition.ts` directly. The
  one scenario that could otherwise be a silent gap — the portal shipping
  ahead of the backend — is an explicit, tested case
  (`acquisition.test.ts` — "reports the RPC-missing case distinctly"; design's
  own Rollout section names the resulting UI state), not a dormant risk the
  way `ENG-039`'s `BROADCAST_UNSUBSCRIBE_SECRET`/SMS-mock findings were.
  Nothing new to name.
- *Cost:* $0/month — `git diff origin/main...HEAD -- '*.json' '*.lock'` empty
  in both repos (re-run fresh, not assumed from the security gate's own
  account), one new Postgres function on already-running infrastructure, no
  new service or dependency.
- *Window:* n/a — both projects L1.

No blocking readiness failure.

**Step 4 (route):** worktrees re-checked fresh before anything else: `git
fetch origin` both repos, `git status --short` clean in both (no prior pass
died mid-work). `aiorders-api` HEAD `cd82579eaa62d237e6f85b5c03dc4b9caac9ee01`
(`git rev-list --left-right --count origin/main...HEAD` → `0 1`, matching
every gate's own cited commit exactly); `restaurant-portal` HEAD
`5783a2dd6002c5d773d1b12d5be770c49b3597c9` (`0 3`, matching round 3's own
reviewed checkpoint). No drift. `gh pr list --head
feat/ENG-020-marketing-roi-attribution-reporting --state all` confirmed no
PR already existed on either repo before this hop. Diff vs `origin/main`:
`aiorders-api` 7 files, 695 insertions/1 deletion; `restaurant-portal` 9
files, 567 insertions/0 deletions.

Opened `aiorders-api` PR #17
(https://github.com/harsimranwalia/aiorders-api/pull/17) and
`restaurant-portal` PR #4
(https://github.com/harsimranwalia/restaurant-portal/pull/4). Each body:
what's new, all four gates' verdicts with receipt paths, the self-test
summary, the one non-blocking security finding (the pre-existing,
shared restaurant-existence oracle), a "known limitations at merge time"
section (cross-domain attribution coverage varies per restaurant, no
historical baseline, `ENG-030` named as filed-and-resolved separately and
untouched by this diff), and a rollout note recommending `aiorders-api`
first but stating either merge order is safe (the portal's own tested
"not available yet" state covers the other order).

Wrote `inbox/2026-09-05-eng020-merge-request.md`, `pr_urls:` list format
(two repos — `ENG-011`'s own corrected precedent: never one item per repo,
never a delimited string). `lib/eng-notify.sh raise` run — logged `sent:
active 2026-09-05-eng020-merge-request.md` at `13:40:18`
(`traces/eng-notify-2026-09-05.log`); stamped `notified: 2026-09-05T13:40:18`
on the item by hand, copied verbatim from the log (this board's own
already-flagged local-time-labeled-as-UTC convention, unchanged here).

Ticket set `blocked`, `blocked_on: approver`, `blocked_from: ready-to-ship`,
`owner: devops → approver`, `links.pr` populated as a nested map (both
repos, matching `ENG-013`'s own two-repo convention). No G3 — L1 has none;
the PR merge is the human gate. No release record yet — L1's actual deploy
and the release record both wait for merge detection on a future pass, per
`release-runner/SKILL.md` step 4's L1 row / step 7 split.

**1 transition** (`ready-to-ship → blocked`), well under the cap of 4.
**Consequence:** ticket leaves the counted `ready`..`ready-to-ship`
machine-WIP range — **machine WIP `1/1 → 0/1`, free**, available to whichever
`designed` ticket the next dispatch-scoped pass picks by the board's own
priority order (not this `continue` pass's concern, which is scoped to this
one ticket). The ticket keeps its approver-facing slot per Guards ("a ticket
`blocked` on `blocked_on: approver`... holds its slot there too") — moot in
practice on this instance since `wip.approver_limit: unlimited`, but recorded
for the record regardless.

**Dead-end sweep (scoped to this event):** no other ticket touched — a
`continue` event's own narrower contract. **Notify sweep:** the new gate
item raised and stamped above; both other open `inbox/` items re-read fresh
(`eng028`: `notified: 2026-09-03T16:10:27`, `nudged: 2026-09-04T09:13:37`;
`eng016`'s Piece-2 question: `notified: 2026-09-04T10:58:06`, `nudged:
2026-09-05T09:31:45`) — both already carry their one-ever `nudged:`, neither
carries a `decision:`, neither re-nudged. **Observations/exceptions:** none
filed — no `exception-request:` found, nothing noticed outside this ticket's
own scope. **Journal:** n/a — no G1/G2/G3 or merge request answered this
pass (this pass raised one; unanswered so far).

**Board update:** In-flight row (`state: ready-to-ship → blocked`,
`owner: devops → approver`, `links` populated); "Waiting on the approver"
header count and list updated (two → three items open), new paragraph added
for this ticket's own merge request. Live file held three dated entries
before this one (satisfied by an earlier round's own roll); oldest
(`continue (ENG-020): fix hop for round-2 quality gap (Gap 4)`) rolled to
`_index-archive.md` per the keep-three rule.

Post-pass `eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both exit
0, clean.

`chained: none` — `blocked`, `blocked_on: approver`, is the approver-waiting
no-chain condition. Re-check via a `decision` (if the approver replies to the
merge request) or the next `scheduled`/`watch` pass's own step-5 merge
detection (if either PR merges directly on GitHub with no written reply —
the pattern every prior L1 merge request on this board has actually
followed).

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.

## 2026-09-05 — watch (launchd): step-5 re-check on the fresh merge request — still open, stays `blocked`

`watch` event pass. Context: a file changed in one of the three watched
inboxes outside the notify channel — this ticket's own
`inbox/2026-09-05-eng020-merge-request.md`, written and notified by the
immediately-prior `continue` pass ten minutes before this one
(`notified: 2026-09-05T13:40:18`; this pass running ~13:50). Reading map for
`watch`: steps 2, 3 and 4 (sweep all three inboxes), plus step 5 since the
changed file is a merge-request item — and the not-negotiable set (1, 7, 8b,
9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*). Mode check
clean (repo-root `.env` → `MODE=active`). Pre-pass `eng-gate-check.sh`,
scoped (`ENG-020`) and whole-board: both exit 0, clean.

**Steps 2/3/4 — inbox sweep.** `agents/product-manager/inbox/` and
`agents/eng-manager/inbox/` hold nothing outside their own
`_handled`/`_processed` folders (both last touched 2026-09-01 — no `eng`-tagged
card, no department-originated finding since). Top-level `inbox/` holds
exactly three open items, all still `decision:` empty: `eng028`'s G1 and
`eng016`'s Piece-2 question — both already past their one-ever `nudged:`,
correctly not re-nudged — and this ticket's own merge request. `inbox/requests/`
empty. Nothing answered this pass; no gate return to act on per step 4, and
none inferred from silence.

**Step 5 — merge detection, this ticket's own two PRs (the only open merge
request on the board right now, per "Waiting on the approver").** `git fetch
origin` in the department's own worktrees, never the human's checkout
(`~/Documents/projects/_eng/{aiorders-api,restaurant-portal}`):
`aiorders-api@cd82579` and `restaurant-portal@5783a2d`, neither an ancestor of
its own `origin/main` (`git merge-base --is-ancestor`, both **NOT MERGED**).
Cross-checked with `gh pr view` on both PR URLs directly rather than trusting
ancestry alone (this board's own `ENG-008` branch-tip-contamination precedent
for why ancestry alone can mislead): both `state: OPEN`, `mergedAt: null`,
`baseRefName: main`, `headRefName` matching this ticket's own branch exactly —
no stacking, no contamination. Unsurprising at ten minutes old, but checked
rather than assumed, per step 5's own instruction.

**0 transitions.** Ticket stays `blocked`, `blocked_on: approver`,
`blocked_from: ready-to-ship` — unchanged. **Consequence:** none — machine WIP
already `0/1` (freed by this ticket's own prior release-readiness hop);
approver-facing slot unaffected either way.

**Dead-end sweep (scoped to this event):** no other ticket touched —
`watch`'s own contract here is the three inboxes plus this ticket's merge
check, not a full board sweep (that's `scheduled`'s job). **Notify sweep:** no
new gate item this pass; the 24h/no-nudge/no-decision check matches nothing
new (`eng028`/`eng016` already carry their one-ever nudge; this ticket's own
item is ten minutes old). **Observations/exceptions:** none — no
`exception-request:` found, nothing noticed outside this ticket's own scope.
**Journal:** n/a, no G1/G2/G3 or merge request answered this pass.

**Board update:** none needed — `_index.md`'s In-flight row, header counts,
and "Waiting on the approver" list are all unchanged (state, owner, priority,
and the three-item count all stand). Not appending a fourth dated entry there
with nothing new to report, per step 10's own reason for keeping that file
lean — this ticket's own log is the durable record of this check instead.

Post-pass `eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both exit
0, clean.

`chained: none` — `blocked`, `blocked_on: approver`, unchanged and still one
of the documented no-chain conditions. Re-check via a `decision` (if the
approver replies) or the next `scheduled`/`watch` pass's own step-5, same
forward pointer this ticket's own prior entry already left.

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.

## 2026-09-05 — scheduled: step-5 merge detection + acceptance-check — `blocked → shipped → verified`

`scheduled` event pass (four-times-daily safety net). Reading map:
the whole document, never narrowed. Mode check clean (repo-root `.env` →
`MODE=active`). Pre-pass `eng-gate-check.sh`, scoped (`ENG-020`) and
whole-board: both exit 0, clean.

**Step 5 — merge detection.** `git fetch origin` in both department
worktrees: `aiorders-api` PR #17 and `restaurant-portal` PR #4, both
**MERGED**, 94 seconds apart (`672dfa77` `2026-09-06T00:41:23Z`, `8eea8f15`
`00:42:57Z`) — landing together, as both PR bodies required. Cross-checked
with `gh pr view` on both directly (this board's own `ENG-008`
branch-tip-contamination precedent for why ancestry alone can mislead):
both `baseRefName: main`, no stacking. **Zero drift**: `git diff
{reviewed-tip} origin/main --stat` empty on both repos, and each merge
commit's own parents (`git log -1 --format='%H %P'`) show the reviewed
branch tip merged in as-is (`672dfa77` ← `89c6fdb1` + `cd82579`; `8eea8f15`
← `aeeb7b9a` + `5783a2d`) — no squash, nothing folded in beyond what every
gate already reviewed.

**"A merge is not a gate"** — all four receipts re-read fresh from the
files, not from this ticket's own log: `agents/database/migrations/ENG-020-marketing-roi-attribution-reporting.md`
(`Gate verdict: pass`), `agents/principal-engineer/reviews/ENG-020.md`
(round 3, `pass`), `agents/qa/test-plans/ENG-020.md` (`last_result: pass`,
all 5 ACs), `agents/security/reviews/ENG-020.md` (`verdict: pass`) — all
current. `blocked → shipped`.

**Acceptance-check run in full** (triggered by entering `shipped`; not the
receipt-bookkeeping shortcut — this ticket owns real criteria, not a
schema-only diff). Confirmed both sides actually live, not just merged:
`supabase functions list` shows `brand-portal` redeployed
`2026-09-06T00:45:28Z` (~4 min after merge, by hand, no tracked workflow,
same pattern `ENG-037`/`ENG-038` established); `gh run list` on
`restaurant-portal` shows "Deploy to Cloudflare Pages" completed `success`
on the merge commit at `2026-09-06T00:43:01Z` (~90s after merge, this
repo's own push-triggered CI). `supabase db query --linked` confirms
`get_acquisition_breakdown(p_restaurant_id uuid, p_from timestamptz, p_to
timestamptz)` live with the exact designed signature. Read
`acquisition.ts`/`Index.tsx` directly off `origin/main` (not the test suite,
not the PR description) to walk all 5 criteria: AC1 (own-restaurant scoping,
`verifyRestaurantAccess`/`access.hasAccess` gates the RPC call), AC2
(preset → `queryKey` change → refetch), AC3 (`direct_unknown` always seeded
and always rendered even at zero), AC4 (all four honesty-framing mechanisms
present verbatim — subtitle, coverage sentence, low-volume caveat,
organic-search disclaimer), AC5 (access check rejects server-side before
any data leaves, correct call shape). **All 5: pass.** Non-goals check: diff
is additive-only (`App.tsx`/`Sidebar.tsx` +2 lines each, one route + one nav
entry) — no Clarity, no ROI ratio, no AI-SEO isolation, no admin rollup, no
existing page touched. Cost: `$0/month`, no new dependency, matches
estimate. Full walk:
`agents/product-manager/notebook/2026-09-05-eng020-acceptance.md`. `shipped
→ verified`, owner `eng-manager`.

**Step 6b:** does not apply — the PRD's non-goals name deferred ideas but
none with the shape (named next item + explicit sequence sign-off on the
G1) step 6b requires; this ticket's G1 was a bare `approved`. Nothing
auto-filed.

**2 transitions** (`blocked → shipped → verified`), well under the cap of
4. **Consequence:** none for machine WIP — this ticket already left the
counted `ready`..`ready-to-ship` range at its own prior `ready-to-ship →
blocked` hop; the slot has been held by the `ENG-021` family throughout
(`ENG-021` still `building`) and is unaffected by this ticket reaching
`verified`. `blocks: []` — nothing else unblocked, nothing further to
chain as a consequence of this release.

Release record written:
`agents/devops/releases/2026-09-05-ENG-020-aiorders-api-and-restaurant-portal.md`.
Decision-journal row added (`decision-journal.md`) — no written reply, same
standing pattern. Merge-request item's `## Decision` filled in and moved to
`inbox/_handled/2026-09-05-eng020-merge-request.md`.

**Dead-end sweep (whole board, per `scheduled`'s own reading map):** every
other in-flight ticket's last `chained:` line checked — all `designed`/
held-for-slot tickets (`ENG-014`, `ENG-017`, `ENG-023`, `ENG-025`,
`ENG-026`, `ENG-027`, `ENG-029`, `ENG-030`, `ENG-035`, `ENG-036`) correctly
read `chained: none`, held by the machine-WIP cap; `ENG-018` correctly
`chained: none`, `priority: hold`; `ENG-028` correctly `chained: none`,
waiting on its own unanswered G1; `ENG-041` correctly `chained: none`,
waiting on this ticket's own `depends_on`; `ENG-021` (parent, `building`)
last fired `chained: ENG-040`, still the correct active child. `ENG-040`
(the only other `blocked` ticket) re-checked fresh: `aiorders-api` PR #18
still `OPEN`, not merged — stays `blocked`, `blocked_on: approver`,
unchanged. No `*-eng-events-dropped.md` file exists for today; no ticket
found waiting on a chain that silently broke.

**Notify sweep:** no new gate item this pass (a merge landing isn't a gate
item). Remaining open `inbox/` items re-read fresh: `ENG-028`'s G1 and
`ENG-016`'s Piece-2 question both already carry their one-ever `nudged:`;
`ENG-040`'s merge request (`notified: 2026-09-05T16:51:18`) is under 24h.
No action. **Observations/exceptions:** none new — no `exception-request:`
anywhere on the board; the quality-gate shape this ticket surfaced twice
(round 1 and round 2) is already in `observations.md`, not refiled.
**Journal:** row added above.

**Board update:** `_index.md` — In-flight table row removed (terminal);
"Waiting on the approver" header count and list updated (four → three:
`ENG-028` G1, `ENG-016` Piece-2 question, `ENG-040` merge request); new
dated entry appended to the closing paragraphs; oldest of the four live
dated entries rolled to `_index-archive.md` per the keep-three rule.

Post-pass `eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both exit
0, clean.

`chained: none` — `verified` is terminal, one of the documented no-chain
conditions. Nothing else touched this pass needs a chain either (`ENG-040`
unchanged, still correctly waiting on the approver).

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.
