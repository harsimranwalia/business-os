---
id: ENG-012
title: Restaurant support tickets — minimal tracking, plus an open-count on the Brands page
project: aiorders-admin-hub
type: feature
size: L
time_estimate: several days to a week
time_spent:
time_remaining:
severity: P3
priority:
state: dropped
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
  prd: agents/product-manager/specs/ENG-012-restaurant-support-tickets.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Input

Not a fresh raw request — this ticket is the resolved half of `ENG-011`'s
own standing question. Original text, from
`agents/eng-manager/board/ENG-011-client-stage-health-visibility.md`'s own
`## Input`: "...also the health of restaurant and maybe tickets". The
question that resolved it,
`inbox/_handled/2026-08-29-eng011-tickets-source-question.md`, offered two
readings; the approver's answer (`decision: rejected`, free-text "Reading
A", 2026-08-29T11:16:32.000840+00:00) selected:

> A support-ticket system that doesn't exist yet, and this request means
> building one (even a minimal one — issue, status, who's handling it)
> from scratch, then showing an open-count per restaurant on the Brands
> page.

## Readback

See `agents/product-manager/specs/ENG-012-restaurant-support-tickets.md` →
Readback — including the `rejected`-vs-free-text reading note.

## Problem

Staff have no system of record for restaurant-reported issues, and
`ENG-011`'s own Brands page has nowhere to pull an open-ticket count from.

## Outcome

Staff can log, assign, update, and close a support ticket against a
restaurant; the Brands page shows each restaurant's open-ticket count.

## Notes

**Not agent-invented scope.** This ticket is the direct, named continuation
of `ENG-011`'s own standing question — the question itself said "once
answered, this becomes its own ticket." Filing it in the same pass the
answer arrived follows the same precedent `ENG-006`/`ENG-007`/`ENG-008`
established for a sequence's own next item
(`skills/acceptance-check/SKILL.md` step 6b's reasoning, applied here to an
intake-question rather than a G1, since the mechanism is the same: the
approver already reviewed this shape once, by defining both readings
themselves in the question they answered).

**Sized `L`, not `M`** — unlike `ENG-011` (derived fields on existing
columns, no new table), this is a genuinely new data model and CRUD
surface. See the PRD's own Risks section: the architect may find a
one-way door here that `ENG-011`'s design didn't have to consider.

**Project scoping.** Primary project `aiorders-admin-hub` (where the count
is observed and where the ticket list/detail UI lives), same split
precedent as `ENG-008`/`ENG-011` — the new table and endpoints belong in
`aiorders-api`, named here rather than inventing a multi-project ticket
shape.

**Depends on nothing; nothing depends on it.** `ENG-011` ships its own
acceptance criteria without this ticket — the open-count is additive to
`ENG-011`'s Brands page once this lands, not a blocker either direction.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-29` `intake → shaped → awaiting-scope` (product-manager, same
  `intake` event pass as `ENG-011`, continued — the approver's answer to
  `ENG-011`'s standing "tickets" question arrived while that pass was
  still running). Read the answer's `decision: rejected` field together
  with its free-text "Reading A" rather than the field alone — full
  reasoning on the source gate item's own processed footer
  (`inbox/_handled/2026-08-29-eng011-tickets-source-question.md`) and this
  ticket's own PRD Readback.

  **No fresh blind-readback subagent run** — this ticket answers a
  two-option question the department itself already fully specified
  (`inbox/_handled/2026-08-29-eng011-tickets-source-question.md`'s own
  Reading A / Reading B text), not a new ambiguous raw request. Same light
  treatment `ENG-009` used when it answered `ENG-008`'s "engagement"
  question directly from the approver's selection.

  **PRD written**:
  `agents/product-manager/specs/ENG-012-restaurant-support-tickets.md`.
  Sized `L` — genuinely new data model and CRUD surface, materially
  bigger than `ENG-011`'s derived-field approach.

  **G1 required** — full lane, size `L` always requires it regardless of
  bug/chore auto-skip rules (which don't apply to a `feature` anyway).
  Wrote `inbox/2026-08-29-eng012-g1-scope.md` (`agent: product-manager`,
  `gate: scope`, `project: aiorders-admin-hub`). Ran
  `departments/engineering/lib/eng-notify.sh raise`; see the item's own
  frontmatter for the result and `notified:` timestamp.

  **No dissent section** — `agents/critic/agent.md` doesn't exist at the
  department or instance level (confirmed absent again this pass, same
  open proposal, `proposals.md` 2026-08-25 row); not refiled.

  **State:** `intake → shaped → awaiting-scope`, all in this pass. `owner`
  moves `product-manager → approver`.

  **Dead-end sweep:** out of scope for this `intake` event's own narrower
  contract — not run beyond what `ENG-011`'s own log already covers this
  pass. `ENG-007`, `ENG-008`, `ENG-009`, `ENG-010` untouched.

  **Observations filed** (`observations.md`): the ambiguous
  `rejected`-plus-free-text answer shape, worth watching for a second
  occurrence.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-012`) and
  whole-board: see pass notes.

- `2026-08-29` `awaiting-scope → dropped` (eng-manager, `scheduled` event
  pass, context `schtasks`). Found this ticket's own G1
  (`inbox/2026-08-29-eng012-g1-scope.md`) answered `decision: rejected`,
  `decided: 2026-08-29T11:46:47.872706+00:00`, free-text "later" — sitting
  unprocessed, part of the four-item answered-but-unprocessed backlog this
  board's header had flagged for five consecutive passes. Mode check clean
  (`MODE=` empty); pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  whole-board: exit 0, clean.

  **Read `rejected` + "later" as a plain rejection with a deferral note,
  not the same shape as this ticket's own originating question** (`decision:
  rejected` + "Reading A", read there as a selection because a named option
  sat underneath the rejection — see `decision-journal.md`, 2026-08-29 row
  27). Here "later" names no alternative reading, and directly restates
  "not now" rather than contradicting `rejected` — no ambiguity to flag.
  Closest precedent is `ENG-003`'s G1 ("Drop this ticket do not need to be
  done" → `dropped`), not `ENG-011`'s tickets-question.

  **No design work started** — a G1 rejection closes the ticket before the
  architect stage, same as `ENG-003`. Moved
  `inbox/2026-08-29-eng012-g1-scope.md` → `inbox/_handled/` with a processed
  footer; journaled in `agents/eng-manager/config/decision-journal.md`.

  **1 transition** (`awaiting-scope → dropped`). **Consequence:**
  approver-facing WIP and approval cap both unaffected — this item was
  already counted as closed/off-cap in this board's own established
  convention before this pass touched it (see board index header); this
  pass only makes the ticket's own `state:` agree with that accounting.
  Machine WIP unaffected (never entered the counted range).

  **Dead-end sweep:** this ticket's own resolution is this entry; the
  broader whole-board sweep this pass ran is recorded on the board index
  and in `observations.md` rather than repeated on every ticket it touched.

  `chained: none` — `dropped` is terminal; the chaining guard never fires
  on a terminal state. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-012`) and
  whole-board: see board index.

- `2026-08-29` **a fourth predicted twin no-op: this ticket's own G1
  decision event arrived after its fact was already consumed — not by the
  pass that raised it, but by the later `scheduled` sweep that dropped this
  ticket** (eng-manager, `decision` event pass, context
  `inbox/_handled/2026-08-29-eng012-g1-scope.md`). Same shape as `ENG-013`'s
  own presignup-leads twin (consumed by a separate scheduled sweep, not the
  raising pass) and, before that, `ENG-013`'s G1 twin, `ENG-011`'s
  tickets-question twin, `ENG-011`'s own G1, `ENG-010`'s G1, `ENG-009`'s G1,
  `ENG-008`'s two gate items. Per this event's own narrower contract (act on
  the answered gate item, advance only the ticket it belongs to), scoped to
  `ENG-012` only — no board-wide sweep. Mode check clean (business-os
  `.env` → `MODE=` empty; instance `config/config.yaml` → `mode:` empty).
  Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-012`) and whole-board: both exit 0, clean.

  **Confirmed rather than assumed.** `traces/eng-loop-2026-08-29.log`:
  `13:24:51 draining queued event: decision (2026-08-29-eng012-g1-scope.md)`
  — no `queue: collapsed` line immediately above it, so this is a single
  queued fire reaching its own turn late (raised/`notified:` 11:22:35,
  drained roughly two hours later), not a duplicate-collapse; a long
  backlog simply sat ahead of it in the FIFO. By the time it drained, this
  ticket's own G1 (`decision: rejected`, "later", `decided:
  2026-08-29T11:46:47.872706+00:00`) had already been fully processed by
  the separate `scheduled` event pass logged directly above (context
  `schtasks`): `awaiting-scope → dropped`, journaled
  (`decision-journal.md` row 30), gate item moved to `inbox/_handled/` with
  its own processed footer. Checked fresh rather than trusted: this
  ticket's own frontmatter (`state: dropped`), the journal row, and the
  footer all agree. Nothing left for this event to act on.

  **0 transitions.** No cap affected — this G1 was already off both the
  approver-facing WIP and approval-cap counts before this pass, closed by
  the earlier scheduled sweep; the ticket itself sits terminal, off the
  machine-WIP range entirely.

  **Dead-end sweep (scoped to this event):** no `continue ENG-012` exists
  in `traces/.pending`, nor should one — the log entry directly above
  already records `chained: none` on the transition to `dropped` (terminal
  state, chaining guard never fires). Confirmed absent from the pending
  queue rather than assumed.

  **Notify sweep:** nothing to raise (no new gate item this pass); nothing
  to nudge (this G1's `notified:`/`decision:` cycle closed same-day, hours
  before this pass, well inside the 24h threshold).

  Another corroborating occurrence of the open `proposals.md` race
  (2026-08-27 row — `eng-trigger.sh` should skip the launch when a
  `decision` event's named gate item is already in `_handled/`); well past
  a dozen occurrences instance-wide as of today, so not re-filed or
  re-logged as its own observation — the existing proposal already covers
  this exactly.

  `chained: none` — `dropped` is terminal; the chaining guard never fires
  on a terminal state, and there is no other in-flight work on this ticket
  to resume. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-012`) and whole-board: both exit 0, clean. Also recorded on
  the board index (`_index.md`, matching dated entry).
