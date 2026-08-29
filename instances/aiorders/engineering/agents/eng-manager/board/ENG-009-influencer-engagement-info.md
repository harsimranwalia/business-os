---
id: ENG-009
title: Influencer engagement info — internal activity signal plus a staff-editable social stat
project: aiorders-admin-hub
type: feature
size: S
severity: P3
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
  prd: agents/product-manager/specs/ENG-009-influencer-engagement-info.md
  design: agents/architect/designs/ENG-009-influencer-engagement-info.md
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Input

This ticket is the direct, approver-answered resolution of the standing
question raised while shaping `ENG-008`
(`inbox/_handled/2026-08-29-eng008-engagement-source-question.md`), itself
carved out of the same original request as `ENG-008`
(`agents/product-manager/inbox/_handled/2026-08-29-for-the-influencer-board-on-admin-panel-we-are-unable-to-see.md`).
Verbatim answer, given as a hand-edit to the question item while this
pass was still running:

> i mean both reading a and reading B. reading A is something we can start
> with now so we know how active the particular influencer is. reading B
> is something our staff can update or later we can connect using some api
> from meta.

## Readback

**Understood as:** Both candidate readings of "engagement" are wanted, not
one instead of the other:
- **Reading A** — an internal signal showing how active a given influencer
  is on AIOrders (derived from existing/adjacent data — campaigns,
  collaborations, responses). Build now.
- **Reading B** — a social-media engagement figure (e.g. follower count or
  engagement rate). For now this is **staff-entered by hand**, not pulled
  from any platform. A live Meta API connection is explicitly named as
  future work, not this ticket — "later we can connect."

No second blind reading run for this ticket: the standing question this
answers already went through the full request-readback comparison (both
independent readings flagged the same gap; see `ENG-008`'s PRD), and the
approver's own reply directly resolves it with concrete instructions
rather than reopening any ambiguity a second reading could usefully test.

**Requirements:**
1. `[confirmed]` Staff can see an internally-derived indicator of how
   active an influencer is on AIOrders.
2. `[confirmed]` Staff can view and manually enter/update a social-media
   engagement figure for an influencer.
3. `[inferred]` The two figures are shown distinctly, not merged into one
   number — they answer different questions (platform activity vs.
   external social reach).
4. `[proposed]` The manually-entered social figure shows when it was last
   updated, since nothing keeps it fresh automatically.

**Assumed, and worth correcting if wrong:**
- "How active" (reading A) is a derived read, not a new field staff types
  in — the architect picks the concrete measure (e.g. campaigns applied
  to, collaborations count, response rate) from what already exists,
  rather than this PRD inventing a formula.
- The social figure (reading B) is a single number (e.g. a follower count
  or a percentage) staff overwrite each time they check, not a
  history/timeline of past values — a timeline is a bigger feature nobody
  asked for.
- No specific platform (Instagram vs. TikTok vs. both) is named for the
  manual figure — staff can label or choose per influencer; this ticket
  doesn't hardcode one platform.

## Problem

Staff have no way to judge how active an influencer actually is on
AIOrders, or to record what their social reach looks like, even
informally — both are needed to make a sensible match/rating decision, and
today neither exists anywhere on the admin board.

## Outcome

An influencer's admin record shows an internally-derived activity signal
and a staff-editable social engagement figure. No external API call is
made by this ticket.

## Notes

**No hard dependency on `ENG-008`**, but sequenced after it in practice:
both tickets touch the same influencer-detail admin UI (`aiorders-admin-hub`)
and the same influencer table (`aiorders-api`), and building them
concurrently risks a merge conflict on the same files for no real benefit
— not a data dependency, an engineering-sequencing one. The EM's call at
`ready`, not decided here.

**Explicitly not the Meta API integration.** The approver's own words defer
that ("later we can connect") — this ticket delivers the staff-manual
version now. Whoever files the future API-connected version should treat
this ticket's manual field as the thing it eventually replaces or
augments, not something to redesign from zero.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-29` `intake → shaped → awaiting-scope` (product-manager, same
  `intake` event pass as `ENG-008`, continued after the standing question
  it depended on was answered mid-pass). Caps checked fresh: approver-facing
  WIP 1/2 (from `ENG-008` this same pass) → this ticket would take the
  second and last free slot; approval cap 2/3 → closing the now-answered
  question and opening this G1 nets to 2/3 (unchanged count, different
  contents).

  **Shaped directly from the approver's own answer** rather than running a
  fresh two-reading comparison — the ambiguity that comparison exists to
  catch was already found and is now resolved by direct instruction; a
  second blind reading here would be ceremony over an approver-authored
  spec, per `skills/request-readback/SKILL.md`'s own exemption for a
  request that's already effectively a spec.

  PRD written:
  `agents/product-manager/specs/ENG-009-influencer-engagement-info.md`. G1
  raised: `inbox/2026-08-29-eng009-g1-scope.md`. Ran
  `departments/engineering/lib/eng-notify.sh raise`; see the item's own
  frontmatter for the result.

  **No dissent section** — `agents/critic/agent.md` still doesn't exist
  (same open proposal, not refiled).

  **State:** `intake → shaped → awaiting-scope`, all in this pass. `owner`
  moves `product-manager → approver`. **Consequence:** approver-facing WIP
  1/2 → 2/2 (cap reached, not exceeded — no further approver-dependent
  work starts until one of these two clears). Approval cap stays 2/3 (the
  answered question closed, this G1 opened). Machine WIP unaffected.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human.

- `2026-08-29` `awaiting-scope → designed → ready` (architect, then
  eng-manager — `scheduled` event pass, context `schtasks`). Found this
  ticket's own G1 (`inbox/2026-08-29-eng009-g1-scope.md`) answered
  `decision: approved`, `decided: 2026-08-29T09:20:42.679606+00:00`,
  sitting unprocessed — part of the four-item answered-but-unprocessed
  backlog this board's header had flagged for five consecutive passes; the
  G1 itself was already journaled by the pass that shaped `ENG-010` from
  its rider, so only the ticket's own state advancement was outstanding.
  Mode check clean (`MODE=` empty); pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  **Real design work done against the live repos, and this ticket's own
  premise corrected before writing it — `ENG-008`'s design doc said a note
  to that effect had been left here; it hadn't (see `observations.md`).**
  Checked directly rather than trusting the citation: `followers`,
  `engagement`, `followers_growth`, `engagement_growth` already exist on
  `influencers` and are already displayed on the admin board (`src/pages/
  Influencers.tsx`, confirmed by reading the file directly) — same
  edit-capability-gap shape `ENG-008` already found for region/
  campaign-type. Shrinks this ticket (one new timestamp column instead of
  new social-figure columns); the acceptance criteria are unaffected —
  staff can still see and edit a social engagement figure, it's just an
  existing pair of columns gaining a write path rather than new ones.
  Reading A (internal activity) derives from `influencer_invitations`
  (count + most recent date) rather than a stored column — deliberately
  status-agnostic since the full `status` enum isn't confirmed from this
  repo alone. Full detail, including the additional undisplayed
  `follower_count`/`ig_handle`/social-handle fields found on the same
  table (flagged, not acted on): `agents/architect/designs/
  ENG-009-influencer-engagement-info.md`.

  **No one-way door** — one new nullable column, two existing columns
  gaining a write path through the same handler file `ENG-008` is already
  adding, a read-only derived query against an existing table, no new
  auth surface. Moved straight through `designed` without a G2.

  **File-level sequencing confirmed, not just a general concern anymore.**
  This design extends the exact file `ENG-008`'s own design proposes
  (`admin-portal/handlers/influencers.ts`), which does not exist yet —
  `ENG-008` itself hasn't started building. Deliberately **not chained**
  this pass; see this pass's own dead-end-sweep finding on `ENG-008`
  below and in `observations.md`.

  Moved `inbox/2026-08-29-eng009-g1-scope.md` → `inbox/_handled/` with a
  processed footer. G1 already journaled (`decision-journal.md`,
  2026-08-29 row 25); no new journal row needed for this state
  advancement alone.

  **2 transitions** (`awaiting-scope → designed → ready`), well under the
  cap of 4 — `building` needs a backend/frontend/database engineer
  actually writing code, this pass's stopping point by design.
  **Consequence:** machine WIP 4/6 → 5/6 (this ticket now inside the
  counted `ready`..`ready-to-ship` range alongside `ENG-007`/`ENG-008`/
  `ENG-011`/`ENG-013`); approver-facing WIP and approval cap unaffected
  (this G1 was already off both counts before this pass, per the board
  index's established convention).

  **Dead-end sweep:** this ticket's own resolution is this entry; see the
  board index and `observations.md` for the whole-board findings this
  pass also made (`ENG-008`'s broken chain, chief among them).

  `chained: none — held for sequencing.` `ready` is normally agent-owned
  and would chain immediately, but this ticket's own design (and `ENG-008`'s
  before it) explicitly calls out that both extend the same not-yet-created
  handler file — starting a build here before `ENG-008` builds risks two
  engineers editing the same new file concurrently, the exact conflict
  both tickets' own notes already flagged. `ENG-008`'s chain is being
  re-fired this same pass (see its own log); re-check `ENG-009` once
  `ENG-008` reaches `in-review` or later. This is the EM's own sequencing
  call, reserved explicitly by both tickets' design docs rather than
  decided by default. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-009`) and
  whole-board: see board index.

- `2026-08-29` **the predicted twin no-op: G1 scope decision event arrived
  after its own fact was already consumed** (eng-manager, `decision` event
  pass, context `inbox/_handled/2026-08-29-eng009-g1-scope.md`). Per this
  event's own narrower contract, scoped to `ENG-009` only — no board-wide
  sweep. Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-009`) and
  whole-board: both exit 0, clean.

  **Confirmed the duplicate-queued-event race directly rather than assuming
  it from its two prior occurrences on `ENG-008`'s own gate items.**
  `traces/eng-loop-2026-08-29.log`: `10:18:40 queue: collapsed 3 duplicate
  event(s)` fires immediately before `10:18:40 draining queued event:
  decision (2026-08-29-eng009-g1-scope.md)` — three legitimately-queued
  copies of this event collapsed to the oldest, which is this pass.

  **This item's fact was already fully consumed.** The G1 approval — plus
  the approver's unprompted staff-notes addendum, already shaped into
  `ENG-010` and journaled separately — was read and acted on by the
  `scheduled` pass (context `schtasks`) that found it sitting
  answered-but-unprocessed: journaled (`decision-journal.md` row 25), the
  gate item moved to `inbox/_handled/` with its own processed footer, and
  this ticket carried `awaiting-scope → designed → ready` in that same pass
  (see this log, entry above). Checked fresh rather than trusted: this
  item's own frontmatter (`decision: approved`, `decided:
  2026-08-29T09:20:42.679606+00:00`) and processed footer, the journal row,
  and this ticket's own `state: ready` all agree — nothing left for this
  event to act on.

  **0 transitions.** No cap affected — this ticket was already inside the
  counted `ready`..`ready-to-ship` machine-WIP range (6/6, at cap) before
  this pass, and this G1 was already off both the approver-facing WIP and
  approval-cap counts.

  **Dead-end sweep (scoped to this event):** confirmed `continue ENG-008`
  still queued and undrained in `traces/.pending`, behind several other
  not-yet-drained fires — consistent with `ENG-008` still sitting at
  `ready` with no branch or build started in either worktree. This ticket's
  existing sequencing hold (re-check once `ENG-008` reaches `in-review` or
  later) therefore still applies unchanged. Nothing to resume or fix.

  **Notify sweep:** nothing to raise (no new gate item); nothing to nudge
  (this item's `notified:`/`decision:` cycle closed same-day, hours before
  this pass).

  `chained: none` — no state change; this ticket remains deliberately held
  at `ready` pending `ENG-008` reaching `in-review` or later, per the
  reasoning already recorded above. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-009`) and
  whole-board: both exit 0, clean. Also recorded on the board index
  (`_index.md`, matching dated entry).
