---
id: ENG-013
title: Foodswipe funnel page — staff-settable pipeline stages
project: aiorders-admin-hub
type: feature
size: M
time_estimate: half a day to a couple of days
time_spent:
time_remaining:
severity: P2
priority:
state: ready
owner: eng-manager
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
  prd: agents/product-manager/specs/ENG-013-foodswipe-funnel-stage-control.md
  design: agents/architect/designs/ENG-013-foodswipe-funnel-stage-control.md
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Input

Verbatim, from
`agents/product-manager/inbox/2026-08-29-for-the-foodswipe-sales-funnel-page-we-are-not-able-to-or-th.md`
(now `agents/product-manager/inbox/_handled/`), filed by the approver, `via:
control-center`, received 2026-08-29T08:18:22.573861+00:00 — preserved here
per `skills/request-readback/SKILL.md` step 1, never edited:

> # for the foodswipe SALES funnel page we are not able to or the sales staff is not able to update or have proper peipleine stages
>
> sales, onboarding staff is not able to do anything with the funnel page of foodswipe on admin panel

## Readback

See
`agents/product-manager/specs/ENG-013-foodswipe-funnel-stage-control.md` →
Readback — the full two-reading comparison lives there rather than
duplicated here.

## Problem

Sales and onboarding staff can't act on the Foodswipe funnel page at all —
confirmed in code as a 100% read-only page and backend handler, not just a
reported symptom.

## Outcome

Staff can set or correct a listing's stage on the Foodswipe funnel page,
with the manual choice sticking and a way to reset to automatic.

## Notes

**Severity called P2, not P3.** Calibrated against `ENG-011` (a same-day,
same-shape "staff can't act on an admin list" ticket, called P3): that
ticket was missing *visibility+filtering*; this one is missing *all*
interactivity, confirmed by reading both the frontend and the backend
handler rather than inferred from the report. `observations.md` (2026-08-29,
eng-manager, row on the five-request batch) already read this whole batch
as "real but non-emergency" — consistent with P2, not P1: a workaround
exists (staff presumably track this manually today, same as they always
have), so it clears P0/P1's "no workaround" bar.

**Evidence found, not assumed.** `aiorders-admin-hub`'s live worktree
(`src/pages/FoodswipeListings.tsx`, 339 lines) has no click/drag handler,
no edit affordance, and no mutation call anywhere in the file — a pure
kanban *display* of one `GET` response. `aiorders-api`'s handler
(`admin-portal/handlers/foodswipe.ts`) confirms the same from the other
side: `classifyStage()` is a pure function over existing columns, no
stored stage, no override column, no write branch despite accepting
`POST`. Searched the repo for `assigned_to`, `lead_status`, `crm_stage`,
`sales_stage`, `contact_status`, `owner_id` — none exist; this is
confirmed net-new, not an extension of something already there, same
shape `ENG-011` found for "tickets." `claim_status` (fetched by this same
handler) is written once to a constant `'pending'` and never read
anywhere — a dead field, not usable prior art. `Leads.tsx`'s existing
edit UI touches a different, unrelated record type (website-interest-form
leads) and isn't reusable here.

**The pre-signup-leads standing question is now resolved, and did not need
a new ticket.** Answered `approved`, "Reading B" — a genuinely separate
pre-signup pipeline is wanted, with autopilot nurture — processed by a
`2026-08-29` `scheduled` event pass, which found `ENG-017` (presignup lead
nurture autopilot) already filed and already citing this same answer, from
an independent `intake` pass earlier the same day. No duplicate filed;
see `inbox/_handled/2026-08-29-eng013-presignup-leads-question.md`'s own
processed footer. Does not block or otherwise change this ticket.

**Project scoping.** Primary project set to `aiorders-admin-hub` (the
literal admin panel, where acceptance criteria are observed), same split
precedent `ENG-003`/`ENG-008`/`ENG-011` used — the other repo's work
(`aiorders-api`, a new authenticated write path) is named in the PRD
rather than inventing a multi-project ticket shape. Both worktrees
already exist on this host (`_eng/aiorders-admin-hub`, `_eng/aiorders-api`).

**Found and left untouched, out of scope for this `intake` event's own
narrower contract:** `inbox/2026-08-29-eng009-g1-scope.md` and
`inbox/2026-08-29-eng010-g1-scope.md` still carry `decision: approved`
(09:20:42 and 10:49:55) but are still sitting in `inbox/`, unprocessed —
already recorded in `observations.md` (2026-08-29, row on this exact
pair) by the immediately preceding pass; not re-logged here, only
re-verified fresh (still true) for this pass's own cap arithmetic. Nine
more requests sit unshaped in `agents/product-manager/inbox/` — this
event's own contract is to work only the one request named in context;
the rest are untouched, each with its own `intake` event already queued
or pending.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-29` `intake → shaped → awaiting-scope` (product-manager,
  `intake` event pass, context this exact request file). Mode check clean
  (business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
  `mode:` empty). Caps checked fresh from ground truth before raising:
  `inbox/2026-08-29-eng009-g1-scope.md` and
  `inbox/2026-08-29-eng010-g1-scope.md` answered-but-unprocessed (treated
  as closed, not open, per this instance's established convention — see
  Notes); only `inbox/2026-08-29-eng012-g1-scope.md` genuinely open.
  Approver-facing WIP 1/2, approval cap 1/3 before this pass, both under
  cap.

  **Ran the full request-readback**
  (`skills/request-readback/SKILL.md`): this PM's own reading plus a
  blind architect reading (subagent, `opus`, raw request +
  `knowledge/business-profile.md` only, no repo access, no exposure to
  this PM's own reading). **No material divergence on direction** — both
  converged on the same shape: an existing, currently non-functional
  admin page that should let staff act on a pipeline; both independently
  flagged "update" as ambiguous between move-stage and edit-details. The
  architect's reading additionally hypothesized, unprompted, that "sales"
  and "onboarding" might need genuinely different stage vocabularies —
  checked against the live code (see below) and found live rather than
  speculative, so carried forward as a standing question rather than
  silently folded in either direction.

  **Checked the live repos before proposing defaults**, same practice
  `ENG-005`/`ENG-008`/`ENG-011` established: identified the exact page
  (`FoodswipeListings.tsx` — the only file in the repo matching "funnel"),
  confirmed it and its backend handler
  (`admin-portal/handlers/foodswipe.ts`) are 100% read-only with no
  mutation path anywhere, confirmed no staff-assignable status/notes
  concept exists anywhere in `aiorders-api` (`assigned_to`, `lead_status`,
  `crm_stage`, `sales_stage`, `contact_status`, `owner_id` all absent),
  and confirmed the one present-looking status field (`claim_status`) is
  dead — written once to a constant, read nowhere. Ruled out `Leads.tsx`
  as unrelated (different record type, different existing update path).
  Turned what could have been a guess about whether "update" means
  extending something partial into a confirmed "there is nothing to
  extend — this is a real gap, built from zero."

  **PRD written**:
  `agents/product-manager/specs/ENG-013-foodswipe-funnel-stage-control.md`,
  acceptance criteria + non-goals naming the pre-signup-leads question
  explicitly.

  **G1 required** — full lane, not XS/bug/chore; the request-readback ran
  because the "update" ambiguity was real, not because the ticket is
  large. Wrote `inbox/2026-08-29-eng013-g1-scope.md` (`agent:
  product-manager`, `gate: scope`, `project: aiorders-admin-hub`,
  recommendation to build now). Separately wrote the non-blocking standing
  question, `inbox/2026-08-29-eng013-presignup-leads-question.md` (`agent:
  product-manager`, `gate: intake-question`) — kept separate rather than
  folded into the G1 text, same reasoning `ENG-008`'s engagement question
  and `ENG-011`'s tickets question used: it scopes a possibly-different,
  not-yet-filed future ticket, not a condition on approving this one.

  Ran `departments/engineering/lib/eng-notify.sh raise` on both files; see
  each item's own frontmatter for the result and `notified:` timestamp.

  **No dissent section** — `agents/critic/agent.md` still doesn't exist at
  the department or instance level (confirmed absent again this pass, same
  open proposal, `proposals.md` 2026-08-25 row); not refiled.

  **State:** `intake → shaped → awaiting-scope`, all in this pass. `owner`
  moves `product-manager → approver`. **Consequence:** approver-facing WIP
  1/2 → 2/2 (at cap, not over); approval cap 1/3 → 3/3 (the G1 plus the
  standing question, counted conservatively, same convention
  `ENG-008`/`ENG-011` used — at cap, not over). `machine_wip` unaffected.

  **Dead-end sweep:** out of scope for this `intake` event's own narrower
  contract (act on the named request; don't sweep the whole board) — not
  run beyond the fresh cap-verification above. `ENG-007`, `ENG-008`,
  `ENG-009`, `ENG-010`, `ENG-011`, `ENG-012` untouched.

  **Notify sweep:** both of this pass's own items raised and stamped
  above. Nothing else to nudge. Approval cap 3/3 (this pass's own read) —
  **now at cap**; no ticket after this one may start until one of the
  three clears. Not a stall in the alarm sense (the cap was reached by
  this pass's own new work, not discovered stuck) — no `lib/eng-notify.sh
  stall` fired for that reason, but the next pass should treat the board
  as genuinely full.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
  whole-board: both exit 0, clean.

- `2026-08-29` `awaiting-scope → designed → ready` (architect, then
  eng-manager — same `intake` event pass, continued). The approver
  answered this ticket's own G1 by hand-edit (`decision: approved`,
  `decided: 2026-08-29T11:45:00.908943+00:00`, bare approval, no rider)
  while this pass was still running. Per this instance's established
  practice (whichever event reaches a fact first does the real work —
  `ENG-007`'s, `ENG-008`'s, `ENG-011`'s own G1 log entries), processed it
  here rather than leaving it for a separately-queued `decision` event to
  rediscover as a no-op. Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
  whole-board: both exit 0, clean.

  **Real design work done against the live repos**, same practice
  `ENG-005`/`ENG-007`/`ENG-008`/`ENG-011` established. Searched every
  migration in `aiorders-api` for `profiles` before proposing a column on
  it: found six hits, all RLS policies or later references, none a
  `CREATE TABLE` — `profiles`' own base table predates this repo's
  tracked migration history entirely (consistent with the already-known
  gap `observations.md`, 2026-08-26, found for this same repo). Not
  blocking — an `ALTER TABLE` doesn't need the original `CREATE TABLE` —
  but flagged in the design for whoever builds this. Checked
  `admin-portal/index.ts`'s routing and `leads.ts`'s existing
  `updateWebsiteLead` write path before proposing a new endpoint shape,
  so the design reuses a pattern already proven in this codebase rather
  than inventing one.

  **Design**:
  `agents/architect/designs/ENG-013-foodswipe-funnel-stage-control.md`.
  One nullable override column on `profiles` (the only entity present at
  every one of the six stages, unlike `restaurants`, which doesn't exist
  yet for the two earliest), taking precedence over the existing
  `classifyStage()` derivation rather than replacing it — keeps today's
  correct automatic behavior as the default for every listing nobody
  touches. New write action reuses the handler's already-present
  admin/sub-admin gate. **No one-way door** — additive column, `null`
  default, no backfill, no new authorization surface, fully reversible.
  Moved straight through `designed`, no G2.

  Moved the G1 gate item to `inbox/_handled/` with a processed footer;
  journaled in `agents/eng-manager/config/decision-journal.md`.

  **2 transitions this pass** (`awaiting-scope → designed → ready`) on
  top of the 2 already spent shaping the ticket earlier in this same
  pass — 4 total, at the cap of 4, stopping here by design: `building`
  needs a backend/database engineer actually writing code, new
  implementation work this pass does not do. **Consequence:**
  approver-facing WIP 2/2 → 1/2 (this ticket's own path no longer runs
  through the approver — the still-open standing question doesn't block
  it and isn't a second ticket; only `ENG-012` remains); approval cap
  3/3 → 2/3 (this ticket's G1 closed; its own standing question stays
  open, counted conservatively same as before); machine WIP 3/6 → 4/6
  (`ENG-013` now inside the counted `ready`..`ready-to-ship` range
  alongside `ENG-007`/`ENG-008`/`ENG-011`).

  **Dead-end sweep:** scoped to this event's own lineage — `ENG-007`,
  `ENG-008`, `ENG-009`, `ENG-010`, `ENG-011`, `ENG-012` untouched.
  **Notify sweep:** nothing new to raise for this ticket (a gate closing
  doesn't get re-notified); the standing question's own `notified:` from
  earlier this pass still stands, well under the 24h nudge threshold.
  **Observations filed** (`observations.md`): the `profiles` untracked-
  migration-origin finding, corroborating the 2026-08-26 architect entry
  for the same repo.

  `chained: ENG-013` — `ready` is eng-manager-owned (a backend/database
  engineer builds next), not the approver, not blocked, not terminal, not
  held by a cap. Fired
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-013`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-013`) and whole-board: see pass notes.

- `2026-08-29` **the predicted twin no-op: G1 scope decision event arrived
  after its own fact was already consumed** (eng-manager, `decision` event
  pass, context `inbox/_handled/2026-08-29-eng013-g1-scope.md`). Same shape
  as `ENG-011`'s own G1 twin earlier today (and, before that, `ENG-008`'s
  two gate items, `ENG-009`'s G1, `ENG-010`'s G1). Per this event's own
  narrower contract (act on the answered gate item, advance only the ticket
  it belongs to), scoped to `ENG-013` only — no board-wide sweep. Mode check
  clean (business-os `.env` → `MODE=` empty; instance `config/config.yaml`
  → `mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-013`) and whole-board: both exit 0, clean.

  **Confirmed rather than assumed.** `traces/eng-loop-2026-08-29.log`:
  `13:01:35 draining queued event: decision (2026-08-29-eng013-g1-scope.md)`
  — no `queue: collapsed` line immediately above it this time, so this is a
  single queued fire reaching its own turn late (raised/`notified:` at
  11:39:39), not a duplicate-collapse; the queue simply had a long backlog
  ahead of it (`ENG-014`..`ENG-024` work). By the time it drained, the same
  `intake` pass that raised this G1 had already caught the approver's
  hand-edit (`decision: approved`, `decided:
  2026-08-29T11:45:00.908943+00:00`, bare approval, ~6 minutes after
  `notified:`) while still running — see the log entry directly above,
  which carried `awaiting-scope → designed → ready` and journaled the
  decision in the same pass. Checked fresh rather than trusted: this
  ticket's own frontmatter (`state: ready`, `owner: eng-manager`),
  `decision-journal.md` row 28, and the gate item's own processed footer in
  `inbox/_handled/2026-08-29-eng013-g1-scope.md` all agree. Nothing left
  for this event to act on.

  **0 transitions.** No cap affected — `ENG-013` was already inside the
  counted `ready`..`ready-to-ship` machine-WIP range before this pass, and
  this G1 was already off both the approver-facing WIP and approval-cap
  counts.

  **Dead-end sweep (scoped to this event):** confirmed `continue ENG-013` —
  fired by the pass that closed this ticket's G1 — still sitting in
  `traces/.pending`, undrained, third in line behind two older
  not-yet-drained fires (`ENG-013`'s own presignup-leads question,
  `ENG-012`'s G1). Not a broken chain, just not yet its turn in the FIFO
  queue.

  **Notify sweep:** nothing to raise (no new gate item this pass); nothing
  to nudge (this G1's `notified:`/`decision:` cycle closed same-day, hours
  before this pass, well inside the 24h threshold).

  Another corroborating occurrence of the open `proposals.md` race
  (2026-08-27 row, filed by hand — `eng-trigger.sh` should skip the launch
  when a `decision` event's named gate item is already in `_handled/`);
  well past a dozen occurrences instance-wide as of today, so not re-filed
  or re-logged as its own observation — the existing proposal already
  covers this exactly and stands unimplemented, waiting on the approver.

  `chained: none` — no state change; `ENG-013`'s existing chain (`continue
  ENG-013`) is already queued and will run on its own turn. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
  whole-board: both exit 0, clean. Also recorded on the board index
  (`_index.md`, matching dated entry).

- `2026-08-29` **a third predicted twin no-op: the presignup-leads
  standing question's own decision event arrived after its fact was
  already consumed — not by the pass that raised it, but by a later
  scheduled sweep** (eng-manager, `decision` event pass, context
  `inbox/_handled/2026-08-29-eng013-presignup-leads-question.md`). Same
  twin-no-op shape as the G1 entry directly above, and `ENG-011`'s
  tickets-question twin before that. Per this event's own narrower
  contract (act on the answered gate item, advance only the ticket it
  belongs to), scoped to `ENG-013` only — no board-wide sweep. Mode check
  clean (business-os `.env` → `MODE=` empty; instance `config/config.yaml`
  → `mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-013`) and whole-board: both exit 0, clean.

  **Confirmed rather than assumed, and a different shape from the twin
  above.** `traces/eng-loop-2026-08-29.log`: `13:15:10 queue: collapsed 1
  duplicate event(s)` fires immediately before `13:15:10 draining queued
  event: decision (2026-08-29-eng013-presignup-leads-question.md)`, pass
  start `13:15:11`, claude launched `13:16:05`. Unlike the G1 twin above
  (caught live by the same pass that raised it), this question sat
  answered-but-unprocessed until a separate `scheduled` event pass
  (context `schtasks`, since rolled to `_index-archive.md`) swept it: read
  the answer fresh from `inbox/` (`decision: approved`, "Reading B" — a
  genuine pre-signup pipeline with autopilot nurture, `decided:
  2026-08-29T11:46:34.557123+00:00`), checked for an existing ticket
  before filing a new one per the item's own stated next step, and found
  one — an independent `intake` pass the same day had already reached the
  same conclusion from a different raw request (the "no autopilot for
  sales staff/resellers" card) and filed `ENG-017` (presignup lead nurture
  autopilot,
  `agents/eng-manager/board/ENG-017-presignup-lead-nurture-autopilot.md`,
  `state: shaped`), already citing this exact verbatim answer as grounding
  evidence in its own Notes. Checked fresh rather than trusted: the gate
  item's own processed footer, `decision-journal.md` row 31, this
  ticket's own Notes section above (added by that scheduled pass), and
  `ENG-017`'s own Notes section all agree — the question is closed against
  `ENG-017`, not re-opened, and not filed twice. `ENG-013` itself was
  never blocked by this question and needed no action from it either way,
  then or now.

  **0 transitions.** No cap affected — `ENG-013` was already inside the
  counted `ready`..`ready-to-ship` machine-WIP range before this pass, and
  this standing question's approval-cap slot was already freed by the
  scheduled pass that closed it — the board header's current cap
  accounting (`ENG-014`/`ENG-015`'s G1s only) no longer carries it.

  **Dead-end sweep (scoped to this event):** confirmed `continue ENG-013`
  — fired when this ticket reached `ready` — still sitting in
  `traces/.pending`, undrained, behind a longer backlog than the twin
  above last saw. Not stuck — no documented sequencing hold against a
  sibling ticket, purely FIFO position.

  **Notify sweep:** nothing to raise (no new gate item this pass); nothing
  to nudge (this question's `notified:`/`decision:` cycle closed same-day,
  hours before this pass, well inside the 24h threshold).

  Another corroborating occurrence of the open `proposals.md` race
  (2026-08-27 row — `eng-trigger.sh` should skip the launch when a
  `decision` event's named gate item is already in `_handled/`); not
  re-filed or re-logged as its own observation — the existing proposal
  already covers this exactly.

  `chained: none` — no state change; `ENG-013`'s existing chain (`continue
  ENG-013`) is already queued and will run on its own turn; firing a
  second `continue ENG-013` now would only queue a duplicate for the
  collapse logic to clean up later. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
  whole-board: both exit 0, clean. Also recorded on the board index
  (`_index.md`, matching dated entry).
