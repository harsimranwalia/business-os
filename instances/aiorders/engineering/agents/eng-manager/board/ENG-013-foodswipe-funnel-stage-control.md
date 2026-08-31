---
id: ENG-013
title: Foodswipe funnel page — staff-settable pipeline stages
project: aiorders-admin-hub
type: feature
size: M
time_estimate: half a day to a couple of days
time_spent: ~3h build, one code-review round (principal-engineer), plus the
  test-writing round 1 asked for — done by an untracked pass on the other
  host, discovered and independently verified (not redone) this pass; see log
time_remaining: ~1.5-3h — round 1's finding (no automated test on the new
  authz-gated write path) is closed: `foodswipe.test.ts` exists on the
  pushed branch and this pass traced every case against the live handler by
  hand, confirming it covers the access-gate negative case, stage
  validation, and the source='foodswipe' tenant-scoping. Remaining is a
  fresh review+quality hop, then in-security/ready-to-ship/release admin as
  before. No approver time_impact.
severity: P2
priority:
state: building
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-08-30
branch: feat/ENG-013-foodswipe-funnel-stage-control (same name, both repos)
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

- `2026-08-29` `ready → building` — the actual build (backend, database,
  frontend — `continue` event pass, context `ENG-013`, its turn at the front
  of `traces/.pending` finally reached). Narrow scope per the event's own
  contract (resume this ticket from its current state; no board-wide sweep).
  Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty).

  **Pre-pass gate check flagged as not-clean (exit 2), investigated rather
  than trusted or ignored.** The check injected into this pass's prompt
  reported all twelve of `ENG-013`..`ENG-024`'s board files as "not a
  regular file. Fail-closed." — including this ticket's own. Verified fresh:
  `stat` on this file and a directory listing of the whole board confirmed
  every one of the twelve is in fact an ordinary regular file (`ls -la`
  showed normal `-rw-r--r--` entries, all modified `13:37` today).
  Re-running `departments/engineering/lib/eng-gate-check.sh` fresh, both
  scoped to `ENG-013` and whole-board, returned exit 0 clean with no output
  on both. Conclusion: the injected report was captured at a moment during
  the immediately-prior pass's own commit
  (`1a6fe83`, "intake ENG-012..024 from approver inbox") when these files
  were still being written to disk — a transient race in when the check ran
  relative to that write, not a real defect in any ticket. Nothing to fix;
  recorded here rather than silently dropped, per this pass's own
  instruction to investigate a flagged ticket that is the one in hand.

  **Worktrees.** Both `~/Documents/_eng/aiorders-api` and
  `~/Documents/_eng/aiorders-admin-hub` already existed on this host. Both
  were sitting on `feat/ENG-011-client-stage-health-visibility` — correct
  and expected, since `ENG-011` is `ready-to-ship` with its own PR not yet
  opened (devops's release step still owns that branch; not safe to delete
  or abandon). `aiorders-admin-hub` carried one uncommitted change on top of
  that branch: `package-lock.json`, pure `"peer": true` metadata churn on
  existing entries (no package added, removed, or version-bumped) — the
  exact artifact `ENG-011`'s own recovery pass already found and named as
  "unrelated, harmless... not part of this ticket's diff, not committed."
  Not mine to carry onto a different ticket's branch either way: stashed
  with a labeled message (`git stash push -m "..."`, not a blind stash)
  rather than discarded, so it stays recoverable for whoever next touches
  that branch. Branched both repos fresh off `origin/main` (not local
  `main`, which git refuses to check out here since the human's own
  worktree at `~/Documents/projects/aiorders/{project}` already has it) as
  `feat/ENG-013-foodswipe-funnel-stage-control`, same name both repos, same
  convention `ENG-011` used.

  **Built against the live repos, per the architect's design
  (`agents/architect/designs/ENG-013-foodswipe-funnel-stage-control.md`)
  and the PM's acceptance criteria
  (`agents/product-manager/specs/ENG-013-foodswipe-funnel-stage-control.md`),
  read fresh at the start of this pass:**

  - **`aiorders-api`** — `supabase/migrations/20260829200000_add_foodswipe_stage_override.sql`:
    one nullable `text` column, `profiles.foodswipe_stage_override`,
    six-value `CHECK` constraint matching the handler's `Stage` union, no
    default, no backfill. `admin-portal/handlers/foodswipe.ts`: the kanban
    read now selects and returns this column per profile, and the
    stage-assignment loop checks it before falling back to `classifyStage()`
    unchanged; two new actions, `setStageOverride`/`resetStageOverride`,
    routed on `POST /foodswipe/stage/set` and `POST /foodswipe/stage/reset`
    inside the same `handleFoodswipe` entry point (mirrors `leads.ts`'s own
    internal path-branching convention — the top-level router in `index.ts`
    already forwards anything under `/admin-portal/foodswipe` here
    unchanged). Both new actions reuse the handler's existing
    admin/sub-admin gate (checked once, before any path branching) and both
    scope their `UPDATE` to `.eq('source', 'foodswipe')` in addition to the
    id, so neither can touch a non-Foodswipe profile even with a crafted
    id. `stage` is validated server-side against a `VALID_STAGES` array
    before the write, not left to the DB constraint alone.
  - **`aiorders-admin-hub`** — `src/config/constants.ts`: two new endpoint
    constants. `src/pages/FoodswipeListings.tsx`: each kanban card gets a
    `DropdownMenu` ("Set stage" / conditionally "Reset to automatic") and a
    shared `Dialog` with a `Select` of the six stages, styled directly after
    `Leads.tsx`'s existing edit-dialog pattern per the design's own
    instruction. A profile with an active override shows a small "Manually
    set" `Badge`. `handleManageStage` pre-selects the dialog's value from
    the override if one exists, else the card's current bucket — never
    opens blank.
  - **One implementation call made at the building stage, not pre-decided
    by the design**: the design's Interfaces section left the read
    response's exact shape ambiguous ("no new field needed... the frontend
    distinguishes source separately"). Read as: the *bucketing* logic needs
    no new field (unchanged), but *distinguishing manual vs. automatic on
    the card* does need one — added `foodswipe_stage_override` (the raw
    override value, `null` when automatic) to each profile object in the
    existing kanban response, rather than a second round-trip or a
    separately-computed boolean. Noted here since the design text alone
    doesn't fully resolve it.

  **Self-tested, per this state's own exit condition and
  `engineering-standards.md`'s checklist:**
  - `deno check supabase/functions/admin-portal/handlers/foodswipe.ts` —
    clean, no errors. No `deno.json` exists in this repo yet (a separate,
    already-named gap in `config/projects.md`), so this is a direct
    single-file check rather than a project-wide one.
  - `npm run lint` in `aiorders-admin-hub` — repo-wide, 150 pre-existing
    errors / 31 warnings across files this ticket never touches (confirmed
    by grepping the output for `FoodswipeListings.tsx` and
    `src/config/constants.ts` specifically): one pre-existing `any` on
    `listingData.menus` and one pre-existing missing-dependency warning on
    `fetchListings` — both present, unchanged, before this diff (verified
    against the file as first read this pass). Zero new lint issues
    introduced by this change.
  - `npm run build` in `aiorders-admin-hub` — clean, 3340 modules, same
    pre-existing large-chunk warning `ENG-011`'s own verification already
    named.
  - No live Postgres reachable on this host to execute the migration
    itself (no `docker`, `psql`, or `supabase` CLI — third occurrence of
    the exact host limitation `ENG-007`'s and `ENG-011`'s migration docs
    already recorded; not re-filed as a new observation). Used the
    read-only Supabase MCP connection instead, same path `ENG-011`'s own
    recovery pass used, against the real `aiorders-api` project
    (`bmnmnejwdxbcqinqkwko`, confirmed `ACTIVE_HEALTHY` via
    `list_projects` before trusting it): confirmed `profiles`' real column
    set matches every assumption the handler code and this migration make
    (`id uuid NOT NULL`, `source text`, no pre-existing
    `foodswipe_stage_override`); confirmed table scale (528 rows total, 36
    `source = 'foodswipe'`) makes the `ADD COLUMN`'s already-metadata-only
    nature immaterial to size; confirmed via `list_migrations` that this
    migration is not yet applied and that production is exactly where this
    doc assumes. Full detail, reasoning, and the gate verdict:
    `agents/database/migrations/ENG-013-foodswipe-funnel-stage-control.md`
    (written this pass — the receipt the `database` gate's "Yes — migration
    gate" gate authority reviews next, same artifact shape `ENG-006`,
    `ENG-007`, and `ENG-011` each used).

  **Artifact enumeration run before finishing** (step 6b): `grep -rln
  "foodswipe" --include="*.md" --include="*.sh" --include="*.yaml"` across
  both the instance and department roots. Two hits worth checking beyond
  this ticket's own files: `ENG-024`'s board/spec use "FoodSwipe" only for
  the unrelated consumer sign-up/marketplace-visibility flow (no overlap
  with this admin funnel page); `ENG-009`'s design doc cites
  `FoodswipeListings.tsx:207-223` as a worked example of this repo's
  fetch-with-bearer-token pattern — a **location** reference (step 6b's own
  classification), not an instruction or a map, and one this pass's ~9
  added lines above that point in the file will have shifted by a few
  lines. Left alone: fixing another ticket's already-shaped design doc for
  a citation drift of this kind is outside this event's contract, and step
  6b itself says a location reference is "usually fine." No instruction or
  map conflicts found.

  **Branches committed and pushed, both repos** — `feat/ENG-013-foodswipe-funnel-stage-control`:
  `aiorders-api` (`ac4efba`, 2 files: the migration + the handler),
  `aiorders-admin-hub` (`a1c3bdf`, 2 files: constants + the page). Both
  `git push -u origin ...` succeeded; both now
  `[origin/feat/ENG-013-foodswipe-funnel-stage-control]`, no PR opened yet
  (that's devops's release-readiness step, per the pipeline — L1 autonomy
  means a human merges, not this pass).

  **PR body written, both repos** (`building`'s own exit condition, and
  `backend/config.yaml`'s required shape: what it does / what it
  deliberately does not / uncertainties / what to review hardest) — kept
  here rather than in a new file, since no separate convention for this
  artifact exists yet anywhere in this department's docs:

  ***`aiorders-api`***
  - *What it does:* Adds a nullable `foodswipe_stage_override` column to
    `profiles` (six-value `CHECK`), and makes the kanban handler prefer it
    over `classifyStage()`'s automatic derivation when set. Adds
    `POST /foodswipe/stage/set` (`{profileId, stage}`) and
    `POST /foodswipe/stage/reset` (`{profileId}`), both behind the
    handler's existing admin/sub-admin gate, both scoped to
    `source = 'foodswipe'`. The existing listing read now also returns the
    override per profile.
  - *What it deliberately does not do:* Touch `restaurants` or
    `restaurant_listing_data`; add an audit trail of who set an override or
    when (named as a future risk in the design, not in this ticket's
    acceptance criteria); change the six-stage taxonomy; add a `deno.json`
    or test harness (a separate, already-named repo gap).
  - *Uncertainties:* The `ALTER TABLE` has not executed against any live
    Postgres on this host — verified instead via read-only Supabase MCP
    against the real production schema (migration doc has full detail).
    Low risk given a single nullable column, no default, no rewrite, and a
    528-row table.
  - *What to review hardest:* The `.eq('source', 'foodswipe')` scoping on
    both new write actions — it's the only thing stopping a valid
    six-value write from landing on an arbitrary profile id, since the DB
    constraint alone would allow it. Also: `stage` validated server-side
    against `VALID_STAGES` rather than relying on the DB `CHECK` alone.
  - *Addendum, 2026-08-30:* `foodswipe.test.ts` now exists on the branch
    (commit `c95b25b`) — see this ticket's own log for provenance and
    verification. It also exports `AuthenticatedRequest`/`hasFoodswipeAccess`
    (additive, needed for the tests to import them) and wraps
    `hasFoodswipeAccess`'s return in `Boolean(...)` so a profile with no
    `additional_roles` returns `false` rather than `undefined` — same
    truthiness at the sole call site, no behavior change, caught by the new
    tests. What to review hardest is unchanged; it now has direct test
    coverage.

  ***`aiorders-admin-hub`***
  - *What it does:* Adds a "Set stage" / "Reset to automatic" dropdown to
    each kanban card (styled after `Leads.tsx`'s edit affordance:
    `DropdownMenu` + `Dialog` + `Select`), plus a "Manually set" badge when
    an override is active. Both actions call the two new endpoints and
    refetch on success.
  - *What it deliberately does not do:* Drag-and-drop (PRD non-goal); edit
    any other listing field; confirm before "Reset to automatic" (treated
    as low-risk and fully reversible, per the design's "no one-way door"
    framing — unlike the existing delete-lead flow, which does confirm).
  - *Uncertainties:* None functional. The file's one pre-existing lint
    error and one pre-existing lint warning (an `any` on `listingData.menus`,
    a missing-dependency warning on `fetchListings` shared by every other
    page in this codebase) both predate this diff and are unchanged by it.
  - *What to review hardest:* `foodswipe_stage_override` threading from
    `KanbanEntry` through to the dialog's pre-selected value —
    `handleManageStage` falls back to the card's current bucket when no
    override is set, so the dialog never opens blank.

  **1 transition this pass** (`ready → building`), well under the cap of 4
  — the next states (`in-review`, folding in `in-qa` per the combined-hop
  convention `ENG-005`/`ENG-006`/`ENG-007`/`ENG-011` all used) are a fresh
  session's work, not this one's, per `schedules/eng_build_loop.md`'s own
  "a pass stops after `building` on purpose." **Consequence:** no cap
  change — `ENG-013` was already inside the counted `ready`..`ready-to-ship`
  machine-WIP range at `ready`; `building` is still inside that same range.
  Approver-facing WIP and approval cap both untouched (no gate item raised
  this pass).

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  `ENG-008`/`ENG-009`/`ENG-010` (also `ready`, also `aiorders-admin-hub`)
  left untouched — each has or will have its own `continue` event.

  **Notify sweep:** nothing to raise — `building` needs no approver gate.
  Nothing to nudge.

  **Observations:** the `package-lock.json` drift and the host's missing
  `docker`/`psql`/`supabase` CLI are both already-named, recurring facts
  (see above); not re-logged a fourth/second time respectively. One new
  observation filed: three unrelated, uncommitted, in-progress changes
  found on disk at pass start (department `eng-manager/config.yaml`'s
  `plan.tier` correction, `eng-trigger.sh`'s matching config-path fix,
  this instance's own `config.yaml` raising `machine_limit` to 12) —
  coherent and clearly intentional, left untouched and not committed
  alongside this ticket's own changes; flagged because it makes
  `board/_index.md`'s cached "Machine WIP 6... 6/6 at cap" header stale
  against the real (if uncommitted) limit. See `observations.md`.

  `chained: ENG-013` — `building` is eng-manager-owned (principal-engineer
  + qa combined hop next), not the approver, not blocked, not terminal, not
  held by a cap. Fired
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-013`
  before exiting. **Confirmed, not just assumed, sent:**
  `traces/eng-loop-2026-08-29.log` shows this fire hit the single-flight
  lock, found it held by this pass's own still-running PID (454, launched
  13:37:11 for this same event), correctly declined to steal it, and
  queued rather than launched — `traces/.pending` shows `continue ENG-013`
  appended at the tail, twelfth behind a real backlog (`ENG-007`,
  `watch schtasks`, `ENG-008`, three `decision`s, `scheduled schtasks`,
  `ENG-022`, two more `decision`s, `ENG-024`, `ENG-011`). Not a broken
  chain — the same FIFO-position shape this ticket's own two twin-no-op
  entries above already documented for other events, now true of this one
  too; a later fire or the safety-net scheduled pass will drain it. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
  whole-board: both exit 0, clean (re-verified immediately before this
  entry was written).

- `2026-08-29` **code review round 1: FAIL — automatic-failure #10, no
  failure-case test on the new authz-gated write path** (principal-engineer,
  `continue` event pass, context `ENG-013`, this fire's own turn at the
  front of `traces/.pending` finally reached). Narrow scope per the event's
  own contract (resume this ticket from its current state; no board-wide
  sweep). Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
  whole-board: both exit 0, clean.

  **Read the actual diff fresh from both worktrees rather than trusting the
  building pass's own PR-body summary**, and without disturbing either
  worktree: both `_eng` worktrees were sitting on `ENG-008`'s branch, not
  this ticket's, same as the building pass itself found — so this review
  read via `git diff origin/main...feat/ENG-013-foodswipe-funnel-stage-control`
  and `git show <branch>:<path>` rather than checking either worktree out.
  Confirmed both branches match this ticket's own frontmatter
  (`aiorders-api@ac4efba`, `aiorders-admin-hub@a1c3bdf`) and the PR bodies
  already recorded on this ticket's log.

  **Ran `skills/code-review-gate/SKILL.md` step 2 (the automatic-failure
  scan) before any deeper review**, per the skill's own instruction not to
  conduct a thorough review of a change that already hits one. Found one:
  **#10, "auth[-adjacent]/authorization path changed with no failure-case
  test."** `foodswipe.ts` adds two brand-new write actions —
  `setStageOverride` (line 155) and `resetStageOverride` (line 203), routed
  at lines 69/72 — both mutating `profiles.foodswipe_stage_override` behind
  the handler's admin/sub-admin gate (`hasFoodswipeAccess`, line 42) and
  both scoped by `.eq('source', 'foodswipe')` (lines 178, 219) as the only
  thing stopping a valid six-value write from landing on a non-Foodswipe
  profile — the ticket's own PR body already names this line as "what to
  review hardest." **Zero test coverage exists for any of it**: `git diff
  --stat` against both branches shows only `foodswipe.ts` and the migration
  changed in `aiorders-api`, no `.test.ts` anywhere in the diff; `git
  ls-tree origin/main` confirms this repo already carries five precedent
  test files, two written on this exact board for this exact reason
  (`brands.test.ts` — `ENG-011`; `loyalty-config.test.ts` — `ENG-007`, 44
  tests including a dedicated non-admin-role-gets-403 case) despite the same
  "no `deno.json`" gap `config/projects.md` names for this repo — so the
  absence here is a regression against this board's own established
  practice, not an unreasonable new bar being invented at review time.
  `engineering-standards.md`'s Tests section is explicit that tests are the
  implementing engineer's own job, not something QA backfills onto untested
  code ("QA is not a test-writing service that cleans up after untested
  code") — so this is a code-review finding routed back to `building`, not
  something to wave through for QA to quietly absorb.

  Per the skill's own step 2 instruction, stopped here rather than running
  the full line-by-line review (shape, correctness, naming) steps 3–7 would
  otherwise cover. For what it's worth, a quick skim for anything else
  automatic-failure-shaped found nothing else: no secret, no silent catch
  (`console.error` before every error response, in both new functions), no
  unbounded query, no new dependency, no commented-out code, no drive-by
  refactor (`hasFoodswipeAccess`'s extraction is exactly the shared check
  the two new branches need, not unrelated cleanup), no datastore bypass.
  The `aiorders-admin-hub` side (`FoodswipeListings.tsx`, `constants.ts`)
  read clean on the same pass: typed throughout (`StageKey`, no new `any`),
  dialog/dropdown pattern matches `Leads.tsx` as the design specified, error
  handling via `toast` consistent with the rest of the page.

  **No receipt written**, per the skill's own rule
  (`agents/principal-engineer/reviews/ENG-013.md` stays absent — a receipt
  written on a fail would satisfy the exact filesystem check it exists to
  prove). Verdict and finding written here and to
  `agents/principal-engineer/notebook/2026-08-29-review-log.md` instead.
  **QA's hop not run this round** — the combined-hop design discards it on
  a review fail since the code is about to change (`config.yaml` →
  `machine_gates.combined_hop`), so no point spending it yet.

  **0 net frontmatter transitions** — `state` was `building` at pass start
  and is `building` at pass end; the gate was reached (that's what
  triggered this review at all) and immediately routed back on the fail
  verdict, so nothing was ever persisted as `in-review`. `owner` unchanged
  (`eng-manager`, this instance's established convention throughout the
  machine-owned range — see `ENG-008`'s identical frontmatter at the same
  state). `time_spent`/`time_remaining` updated in frontmatter this pass.
  `machine_wip` unaffected (`ENG-013` was and remains inside the counted
  `ready`..`ready-to-ship` range, still 5/1). Approver-facing WIP and
  approval cap both unaffected — no gate raised, nothing resolved.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  `ENG-007`/`ENG-008`/`ENG-009`/`ENG-010` left untouched — each has or will
  have its own `continue` event.

  **Notify sweep:** nothing to raise — a failed *machine* gate doesn't reach
  the approver (only G1/G2/G3/merge requests do); nothing to nudge.

  **Observation filed** (`observations.md`): this is the first code-review
  failure recorded on this board — worth a marker for
  `speed.first_pass_gate_rate` once a weekly report actually computes it,
  not itself an action.

  `chained: ENG-013` — `building` is an agent-owned state (the implementing
  engineer adds the missing test next), not the approver, not blocked, not
  terminal, not held by a cap. `failed_gate` sends it back to `building` and
  stops this pass there by design (`config.yaml` → `build_loop.stop_at`),
  but a *fresh* session is exactly what the missing work needs, per
  `eng_build_loop.md`'s "a pass stops after building on purpose." Fired
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-013`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-013`) and whole-board: both exit 0, clean, no `WAIVED:`
  lines.

- `2026-08-30` (dead-end sweep, no state change) `scheduled` event pass,
  context `launchd`. Ticket still `building`/`eng-manager`, missing test not
  yet added, unchanged since the entry above. Same finding as `ENG-008`'s
  identical row today: no `continue (ENG-013)` drain appears in either day's
  trigger log, only `ENG-023`'s two failed attempts and this pass. Re-firing:
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-013`.
  Collapsing makes this safe even if the original fire is still queued
  somewhere rather than lost. `chained: ENG-013`.

- `2026-08-30` **the missing test already existed — found undocumented, not
  written this pass** (eng-manager, `continue` event pass, context
  `ENG-013`, this fire's own turn reached — the re-fire from the entry
  above). Narrow scope per the event's own contract (resume this ticket from
  its current state; no board-wide sweep). Mode check clean (business-os
  `.env` → `MODE=active`; instance `config/config.yaml` → `mode:` not set,
  falls through). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
  whole-board: both exit 0, clean.

  **Went to the worktree expecting to write the test file the ticket's own
  `time_remaining` named, and found one already there.** Real worktree paths
  are `~/Documents/projects/_eng/{project}` (`config/projects.md`), not the
  `~/Documents/_eng/...` shorthand earlier entries on this ticket used —
  neither existed at that literal path; not a regression, just an imprecise
  path in prose. Fetched and checked out
  `feat/ENG-013-foodswipe-funnel-stage-control` in `aiorders-api` (untouched,
  clean, sitting on an unrelated branch beforehand — no mid-work found).
  `git log` showed a second commit already on top of this ticket's recorded
  `ac4efba`: `c95b25b`, *"Add missing test coverage for foodswipe
  stage-override write path (ENG-013)"*, already pushed
  (`origin/feat/ENG-013-...` 0 ahead/0 behind).

  **Investigated rather than trusted, per this instance's own established
  practice, because a commit nobody logged is exactly the shape of thing
  that should not be taken on faith.** Author on both `ac4efba` and `c95b25b`
  is the same identity (`businesspilotcare-gif`) — the department's own
  automation account, not the approver's personal one (`Harsimran
  <walia.harsimran@gmail.com>`, used for his own direct commits elsewhere in
  this same `git log`) and not an unknown third party — so this is the
  department's own prior work, not something to treat as suspicious in
  origin. But it is genuinely undocumented: grepped every
  `traces/eng-loop-2026-08-29.log` / `-30.log` line for `ENG-013` and found
  no pass between the code-review-fail entry and this one; this ticket's own
  log had no entry for it; `business-os`'s own `git log`/`git fetch` showed
  `main` exactly in sync with `origin/main` (0/0), ruling out an unpulled
  business-os-side commit from elsewhere. `proposals.md`'s 2026-08-29 row
  (filed investigating the dropped-events incident) already names the
  mechanism: **this instance runs on two hosts (Mac, Windows since
  `168cb89`), and `traces/` is `.gitignore`d and host-local** — so a
  `continue ENG-013` pass most likely ran on the Windows host, wrote and
  pushed this exact commit, and either never reached or never pushed the
  ticket-log/board update before ending. Reasoned, not confirmed — the
  Windows host isn't reachable from here to check its own local `traces/`.

  **Verified the commit's content rather than assuming a plausible-sounding
  message meant correct code.** No live way to self-test the normal way:
  `deno` isn't installed on this Mac host at all (not on `PATH`, not in
  `~/.deno/bin`) — a new, sharper data point on the same tool-availability
  split `proposals.md`'s 2026-08-29 row already names for `docker`/`psql`/
  `supabase` (that row's fix, formally adopting a documented substitute
  verification path, would cover this too; not re-filed as a fresh proposal
  for that reason — same root cause, same open fix). Read
  `foodswipe.ts` and `foodswipe.test.ts` in full and traced every one of the
  17 new test cases against the live handler logic by hand: method-before-
  role ordering (`DELETE` → 405 before any role check), all three routes'
  403 on a non-admin/sub-admin role, `hasFoodswipeAccess`'s five cases
  including the `Boolean(...)` fix (confirmed the pre-fix `undefined` return
  was genuinely truthiness-equivalent to `false` at its one call site — a
  real but inert bug, exactly as the commit message claims, not a cover
  story), `profileId`/`stage` validation on both actions including the exact
  joined `VALID_STAGES` error string, and the two-`.eq()`-call recording fake
  proving the `source='foodswipe'` scoping is exercised by construction (the
  assertion on `calls` would fail if that `.eq()` were removed, which is
  what the commit message's own "mutation-tested... during this pass" claims
  — verified by construction, not by re-running their test). All three gaps
  round 1 named — access-gate negative case, stage validation, the
  source='foodswipe' tenant-scoping — are covered, correctly, against the
  code as it stands on this branch today. Nothing left to add.

  **Decision: accept the existing commit, do not duplicate it.** Writing a
  second test file (or amending this one) over correct, already-pushed work
  would be pure waste and would risk disagreeing with tests already proven
  correct by hand. Added a short addendum to this ticket's own PR-body notes
  above (`aiorders-api` section) recording the file's existence and the two
  additive fixes, so devops's eventual PR description doesn't omit them.
  `time_spent`/`time_remaining` updated in frontmatter to stop describing
  finished work as pending.

  **Step 6b not run.** Nothing this pass wrote establishes or relies on a
  new rule about an artifact path/state name/config key — it records a
  discovery and corrects stale prose, the same category step 6b itself
  calls "usually fine" for a location reference.

  **0 net frontmatter transitions** — `state` was `building` at pass start
  and remains `building`: the code (including its test coverage) was
  already complete before this pass began, so there was no "reaches
  `in-review`" moment for this session to stop short of. Per
  `eng_build_loop.md`'s "a pass stops after `building` on purpose," running
  the review hop itself in this same session would still be wrong even
  though this pass wrote no code — the rule is state-based, not
  effort-based, and improvising past it is exactly what this event's own
  instructions rule out. `machine_wip` unaffected (`ENG-013` remains inside
  the counted `ready`..`ready-to-ship` range). Approver-facing WIP and
  approval cap both unaffected — no gate raised or resolved.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  `ENG-008`/`ENG-023` each have their own already-queued `continue` fires
  from the `scheduled` sweep two entries above; not this event's contract.

  **Notify sweep:** nothing to raise — no gate this pass. Nothing to nudge.

  **Proposal filed** (`agents/eng-manager/proposals.md`, Open table): a build
  hop that finds a ticket at `building` currently has no step that checks
  the ticket's own remote branch(es) for commits beyond what its log last
  recorded, so cross-host work that completes and pushes but dies before its
  business-os-side commit lands is invisible until someone happens to `git
  log` the branch directly, as this pass did. Distinct from the existing
  2026-08-29 row (that one is about a *dropped-event incident item* not
  carrying enough detail cross-host; this is about *no incident existing at
  all* for a pass that actually finished its real work and only lost the
  bookkeeping) — filed separately rather than folded in.

  `chained: ENG-013` — `building` is agent-owned (the review+quality
  combined hop is next), not the approver, not blocked, not terminal, not
  held by a cap. A *fresh* session is exactly what that hop needs, same
  reasoning every prior entry on this ticket has used. Fired
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-013`
  before exiting. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines.
