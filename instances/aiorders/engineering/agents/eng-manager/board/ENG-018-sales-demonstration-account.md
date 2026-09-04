---
id: ENG-018
title: Sales demonstration account — a fully seeded AIOrders environment to show prospects
project: aiorders-admin-hub
type: feature
size: L
time_estimate: several days to a week
time_spent:
time_remaining:
severity: P2
priority: hold
state: shaped
owner: product-manager
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
  prd: agents/product-manager/specs/ENG-018-sales-demonstration-account.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Input

Verbatim, from
`agents/product-manager/inbox/2026-08-29-no-autopilot-on-admin-panel-for-our-sales-staff-resellers-to.md`
(now `agents/product-manager/inbox/_handled/`), filed by the approver, `via:
control-center`, received 2026-08-29T08:35:46.246211+00:00 — preserved here
per `skills/request-readback/SKILL.md` step 1, never edited:

> # no autopilot on admin panel for our sales staff/ resellers to use .
>
> how can we demonstrate to a client what we sell if we dont have it for
> us. have a proper fully demonstration account on how all aiorders work.
> also autopilot nurturing for resellers/sales/admin staff on admin panel
> which works based on stages update/ auto nurturing .

## Readback

See
`agents/product-manager/specs/ENG-018-sales-demonstration-account.md` →
Readback — the full two-reading comparison and code evidence live there
rather than duplicated here.

## Problem

There is no working example of the AIOrders platform a sales rep or
reseller can show a prospective restaurant owner — confirmed absent across
all five repos, not assumed. A demo today would mean either talking
through the product with nothing to point at, or showing a real
customer's live account, which is both an awkward pitch and a privacy
exposure.

## Outcome

A single seeded demo restaurant exists with a populated menu, order
history, loyalty activity, and a public ordering site, reachable from one
entry point in the admin panel, resettable on demand, and isolated from
real sends and real platform-wide analytics.

## Notes

**Split from one raw request, not the whole of it.** The raw input bundles
two separable asks — this ticket is the demonstration-account half. The
autopilot-nurture half is `ENG-017`, filed in this same pass from the same
request.

**Evidence found, not assumed.** Searched all five repos for any existing
"demo" concept before proposing a net-new one: the only hit is
`config-site-builder/public/config/demo-restaurant.json`, a static
placeholder SEO/config fixture for the site-generation pipeline — not a
loggable-into account with real portal/order/loyalty behavior. No
`is_demo` flag, no seed script, no sandboxing of outbound sends or
analytics exists anywhere today. Also confirmed (via `ENG-011`'s own prior
evidence) that a real internal analytics pipeline
(`platform_analytics_cron`) already aggregates `orders`/`total_amount`
platform-wide per restaurant — the concrete reason this ticket treats
excluding demo activity from that rollup as an acceptance criterion,
not an afterthought.

**Project scoping.** Primary `aiorders-admin-hub` (the raw request frames
this under "admin panel," and the proposed entry point to reach/reset the
demo lives there); `restaurant-portal`, `config-site-builder`, and
`aiorders-api` are named and touched (the demo restaurant's portal, public
site, and seed/isolation data respectively) rather than inventing a
multi-project ticket shape, same split precedent `ENG-003`/`ENG-006`/
`ENG-016` used for genuinely cross-repo work.

**Depends on nothing already on the board**, but its "populated
catering pipeline" acceptance criterion (PRD, criterion 2) reads more
convincingly once `ENG-016` (currently `shaped`, held at the same cap)
ships — noted as a soft sequencing preference, not a hard `depends_on`,
since the demo is still buildable and useful without it.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-29` `intake → shaped` (product-manager, `intake` event pass,
  context this exact request file). Per this event's own narrower
  contract, worked only this one request end to end — did not sweep the
  rest of `agents/product-manager/inbox/`.

  Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board (no ticket
  yet to scope to): exit 0, clean.

  **Caps verified fresh from `inbox/` directly before deciding how far to
  carry this ticket.** `ENG-014`'s and `ENG-015`'s G1s both still sit in
  `inbox/`, unanswered — approver-facing WIP substantively 2/2, at cap.
  Full detail on this pass's own cap check recorded on `ENG-017`'s ticket
  log (filed in the same pass, from the same request) rather than
  repeated here.

  **Ran the full request-readback**
  (`skills/request-readback/SKILL.md`): this PM's own reading, grounded in
  a live search across all five repos, plus a blind architect reading
  (subagent, `opus`, raw request + `knowledge/business-profile.md` only,
  no repo access, no exposure to this PM's own reading, shared with
  `ENG-017` since both readings addressed the whole raw request before
  either ticket was split out). **No material divergence** — both
  independently split the raw request into the same two pieces and both
  independently arrived at "a seeded, fully working fake restaurant";
  the architect's reading additionally, unprompted, flagged
  send/analytics isolation and reseller-branding as considerations,
  folded into this PRD's acceptance criteria and Non-goals respectively.

  **PRD written**:
  `agents/product-manager/specs/ENG-018-sales-demonstration-account.md`.

  **G1 drafted but not raised.** Approver-facing WIP is substantively 2/2
  (`ENG-014`, `ENG-015`) — per `eng_build_loop.md`'s Guards, this ticket
  was carried through readback and PRD-writing but not advanced into
  `awaiting-scope`. Same move this instance's own immediately preceding
  pass made for `ENG-016`, and the same move made for this pass's sibling
  ticket `ENG-017`. The PRD's G1 content is fully drafted and ready to
  raise the moment a slot frees. **1 transition** (`intake → shaped`),
  well under the cap of 4. **Consequence:** no cap numbers change —
  `shaped` counts toward neither approver-facing WIP nor machine WIP.

  No `inbox/` item raised this pass (no G1 to notify on yet), so no
  `lib/eng-notify.sh` call.

  **No dissent section** — `agents/critic/agent.md` still doesn't exist at
  the department or instance level (confirmed absent again this pass, same
  open proposal, `proposals.md` 2026-08-25 row); not refiled.

  **Dead-end sweep:** out of scope for this `intake` event's own narrower
  contract — not run beyond the fresh cap-verification above.

  **Observations filed** (`observations.md`): the confirmed-absent
  demo/sandbox concept and isolation mechanism across all five repos; the
  live analytics-rollup pipeline as the concrete reason isolation is an
  acceptance criterion here.

  `chained: none` — `ENG-018` sits at `shaped`, an agent-owned state, but
  held there by the approver-facing WIP cap rather than genuinely blocked
  or waiting on a human for this ticket specifically; firing `continue
  ENG-018` now would only re-discover the same cap with no new work to do.
  Re-check once a `decision`/`watch`/`scheduled` pass clears `ENG-014` or
  `ENG-015`, or via a dedicated `continue ENG-018` once either does. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-018`) and
  whole-board: both exit 0, clean.

## 2026-09-03 — scheduled: dead-end sweep found and restored an erased `priority: hold`

`scheduled` event pass (whole-board safety-net sweep). Cross-checking
`board/_index.md`'s In-flight table against every ticket's own fresh
frontmatter (this pass's own step-10 groundwork) found this ticket's file
carrying `priority:` blank where the table, the board index's own header
prose (two separate mentions, written on two different days), and every
other ticket's cross-references to this one all still say `priority: hold`.

**Traced to a specific commit, not assumed.** `git log -p` on this file
shows `priority: hold` was set 2026-08-29 (`ad4c6c4`) and stood unchanged
for five days until `2d66236` (2026-09-03T13:25:56-07:00, "aiorders:
whole-board reconciliation — index, journal, notebooks, WIP fix") silently
changed it to blank. That commit's own message frames the touch as
"ENG-018's own priority/date touch from the same WIP-limit correction
pass" — but the WIP-limit correction that evening was about the
**approver-facing WIP cap** (`wip.approver_limit`, raised to unlimited
2026-09-02) and the **priority-column** staleness bug already named in
`observations.md` (table cell vs. each ticket's own frontmatter) —
correcting that bug means copying the ticket file's value *into* the
table, never the reverse. Nothing in that commit's message, this ticket's
own log (no entry mentions `priority` at all), `decision-journal.md`, or
`exceptions.md` documents an actual approver instruction to un-hold this
ticket. Read as an accidental clobber during a large bundled "cross-ticket
bookkeeping... not attributable to any one ticket" commit, not a real
decision — every other artifact on the board still treats this ticket as
held, unbroken, across five days and multiple unrelated passes.

**Restored `priority: hold`** in this ticket's own frontmatter. This is a
data-integrity correction (undoing an unintended edit to match the
approver's own last known explicit value, corroborated by every other
surviving artifact), not a fresh priority judgement call — `eng_build_loop.md`
step 6's "never write to priority yourself" governs *setting* a new value
from inference, which this isn't. Left `updated:` at `2026-09-03` (the
clobbering commit's own stamp) rather than re-touching it, since the
content is now what it should have read all along.

**No ticket-state consequence.** `ENG-018` was already excluded from
dispatch consideration this pass on `priority: hold` grounds (state
`shaped`, never started); this fix prevents a *future* pass from reading
the blank value at face value and treating it as eligible.

Logged in `observations.md` (2026-09-03, eng-manager) for pattern-tracking
— first occurrence of this specific failure shape (a bundled
"whole-board reconciliation" commit clobbering one ticket's own
approver-set field while fixing an unrelated staleness bug), not yet a
third occurrence warranting a proposal per step 8b's own threshold.

`chained: none` — unchanged: `shaped`, `priority: hold`, never started;
nothing for a machine to do here regardless of the WIP cap's own current
(unlimited) state. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-018`) and whole-board: both exit 0, clean.
