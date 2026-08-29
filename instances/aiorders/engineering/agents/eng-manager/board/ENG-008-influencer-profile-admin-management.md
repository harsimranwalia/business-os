---
id: ENG-008
title: Influencer board admin management — region/campaign-type preference, rating, collaboration count
project: aiorders-admin-hub
type: feature
size: M
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
  prd: agents/product-manager/specs/ENG-008-influencer-profile-admin-management.md
  design: agents/architect/designs/ENG-008-influencer-profile-admin-management.md
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Input

Verbatim, from `agents/product-manager/inbox/2026-08-29-for-the-influencer-board-on-admin-panel-we-are-unable-to-see.md`
(now `agents/product-manager/inbox/_handled/`), filed by the approver, `via:
control-center`, received 2026-08-29T08:14:43.907126+00:00 — preserved here
per `skills/request-readback/SKILL.md` step 1, never edited:

> # for the influencer board on admin panel we are unable to see or edit the preference of the influencer in a certain area or update those. also information on the engagement is missing .
>
> influencers should only be able to see the opportunities available but only be able to apply to ones they selected for their region. also same thing for the type of campaign paid or barter. on admin side our staff should be able to rate or add the number of collaborations the influencer has done with us

## Readback

See `agents/product-manager/specs/ENG-008-influencer-profile-admin-management.md`
→ Readback — the full two-reading comparison lives there rather than
duplicated here.

## Problem

Staff managing the admin panel's influencer board can't see or edit an
influencer's region and campaign-type (paid/barter) preferences, can't rate
an influencer, and can't track how many collaborations an influencer has
done with AIOrders — so matching and vetting influencers happens off-system
today.

## Outcome

Staff can view and edit an influencer's preferred region(s) and preferred
campaign type(s) on the admin board, rate an influencer, and view/update a
collaboration count. Nothing influencer-facing changes yet — this ticket is
staff-side only.

## Notes

**Scope split, not the whole raw request.** The raw input bundles four
things: (1) admin-side region/campaign-type preference visibility+editing,
(2) admin-side rating, (3) admin-side collaboration count, (4)
influencer-facing opportunity visibility restricted to matching
region/campaign-type, plus a fifth item — "information on the engagement is
missing" — that both independent readings flagged as genuinely unresolvable
from the text alone. This ticket is (1)+(2)+(3) only. See PRD → "Feature
shape and sequencing" for why (4) and the engagement item are handled
separately rather than folded in or dropped.

**Evidence found, not assumed.** `aiorders-api`'s own `origin/main` (this
host's only existing project worktree) already has
`supabase/functions/restaurant-influencer-campaigns/` (with an
`influencer-invitations.ts` handler and its own `utils/auth.ts`),
`supabase/functions/outgoing-communications/actors/influencers.ts`, and
`supabase/functions/migrate-influencer-images/`. So "influencer" is a real,
already-live concept with existing backend surface — this ticket extends an
existing thing, it does not create the concept of an influencer from
scratch. That resolved the one material divergence between the two
independent readings (see PRD Readback) without needing to ask the
approver. The existing campaign surface reads as **invitation-based**
(restaurant/staff invites a specific influencer to a specific campaign),
not an open browsable list — worth flagging for whoever designs item 4 of
this shape (the influencer-facing "see all, apply to matching ones" flow),
since that may be a new access pattern layered on top rather than a small
edit to the existing invitation flow. Not decided here; a design-time
question.

**Project scoping.** Primary project set to `aiorders-admin-hub` (the
literal "admin panel," and where this ticket's acceptance criteria are
actually observed) even though the schema/migration and endpoint work
belongs in `aiorders-api` (same split precedent `ENG-003` used for its own
multi-repo scope: one primary project field, the other repo's work named
explicitly rather than inventing a multi-project ticket shape). Whoever
picks this up at `building` needs a branch in both `_eng/aiorders-api` and
`_eng/aiorders-admin-hub` — only the former's worktree exists on this
Windows host today (per `config/projects.md`'s host-specific note);
`_eng/aiorders-admin-hub` still needs creating, the same way `ENG-007`
created `aiorders-api`'s, or via `lib/eng-setup.sh --apply`.

**Two related items intentionally not filed yet:**
- Item 4 (influencer-facing region/campaign-type gated opportunity
  visibility + apply) — depends on this ticket's preference fields
  existing. To be filed once this ticket verifies, per the same
  incremental-sequence mechanism `ENG-006`/`ENG-007` established
  (`skills/acceptance-check/SKILL.md` step 6b). Not agent-invented work —
  it's the other half of this same approver request, just correctly
  ordered behind its own dependency.
- The "engagement" item — a standing, non-blocking question is open with
  the approver (`inbox/2026-08-29-eng008-engagement-source-question.md`),
  since its answer changes size by roughly an order of magnitude (a
  display field vs. a new third-party social-platform integration with
  recurring cost). Does not block this ticket. Will become its own small
  ticket once answered.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-29` `intake → shaped → awaiting-scope` (product-manager, `intake`
  event pass, context this exact request file). Mode check clean
  (business-os `.env` → `MODE=` empty). Caps checked fresh before raising
  G1: approver-facing WIP 0/2, approval cap 0/3 — both fully free.

  **Ran the full request-readback** (`skills/request-readback/SKILL.md`):
  this PM's own reading plus a blind architect reading (a subagent given
  only the raw request verbatim and `knowledge/business-profile.md`, model
  `opus` per the skill's own direction, no spend-limit compromise this
  time). **One material divergence found**: this PM's reading assumed an
  influencer-facing apply flow already exists and is simply
  over-permissive; the architect's reading explicitly declined to assume
  that, naming "does an influencer-facing authenticated surface exist at
  all" as the request's biggest potential one-way door (new identity/auth
  class, PII, privacy law) if it doesn't. Per the skill's own classification
  table this is a "different scope" fork — but rather than asking the
  approver a question answerable from evidence already on disk, checked
  `aiorders-api`'s `origin/main` directly (the one project worktree that
  exists on this host) and found real, live influencer/campaign backend
  code (see Notes) — resolving the fork by evidence, not by picking a
  reading or asking. Both readings independently and separately flagged
  "engagement" as unresolvable from the text alone (not a disagreement
  between them — a joint gap) — that one **is** going to the approver, as a
  standing question that does not block this ticket.

  **Split the raw request rather than building one oversized ticket**: the
  admin-side fields (this ticket) and the influencer-facing gating logic
  (future item 4) have different users, non-overlapping acceptance
  criteria, and materially different risk profile (item 4 is an
  authorization/access-control surface needing negative-case security
  testing; this ticket is back-office CRUD) — per the PM's own standing
  instruction to split a request that's really more than one. Sized `M`
  (not `S`): spans two repos/surfaces (`aiorders-api` schema+endpoint,
  `aiorders-admin-hub` UI) even though each individually is simple.

  **PRD written**:
  `agents/product-manager/specs/ENG-008-influencer-profile-admin-management.md`,
  acceptance criteria + non-goals naming item 4 and the engagement item
  explicitly.

  **G1 required** — full lane, not XS/bug/chore. Wrote
  `inbox/2026-08-29-eng008-g1-scope.md` (`agent: product-manager`, `gate:
  scope`, `project: aiorders-admin-hub`, recommendation to build now).
  Separately wrote the non-blocking standing question,
  `inbox/2026-08-29-eng008-engagement-source-question.md` (`agent:
  product-manager`, `gate: intake-question`) — kept as its own item rather
  than folded into the G1 text, since it scopes a *different*, not-yet-filed
  future ticket rather than anything this ticket's own acceptance criteria
  depend on; bundling it into this G1 risked the approver reading it as a
  condition on approving ENG-008 itself, which it isn't.

  Ran `departments/engineering/lib/eng-notify.sh raise` on both files; see
  each item's own frontmatter for the result and `notified:` timestamp.

  **No dissent section** — `agents/critic/agent.md` doesn't exist at the
  department or instance level (confirmed absent again this pass); this is
  the same already-open proposal (`proposals.md`, 2026-08-25 row), not
  refiled.

  **State:** `intake → shaped → awaiting-scope`, all in this pass. `owner`
  moves `product-manager → approver`. **Consequence:** approver-facing WIP
  0 → 1 (cap 2); approval cap 0 → 2 (the G1 plus the standing question,
  counted conservatively even though the question isn't strictly a
  ticket-blocking gate — see board index for the reasoning). `machine_wip`
  unaffected.

  **Dead-end sweep:** out of scope for this `intake` event's own narrower
  contract (act on the named request; don't sweep the whole board) — not
  run. `ENG-007` untouched, not re-verified here.

  **Notify sweep:** both of this pass's own items raised and stamped above.
  Nothing else to nudge. Approval cap 2/3, not full — no stall.

  **Observations filed** (`observations.md`): the confirmed-live
  `restaurant-influencer-campaigns` backend surface and its
  invitation-shaped implication for item 4.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
  whole-board: see pass notes.

- `2026-08-29` `awaiting-scope → designed → ready` (architect, then
  eng-manager — `intake` event pass, context the original influencer-board
  request file). This event's own contract is narrow ("shape the new
  request and carry it as far as it goes," not a whole-board sweep), but
  this ticket **is** that same request's own lineage, so carrying it
  forward here rather than waiting for a separately-queued `decision`
  event follows this instance's established practice (whichever event
  reaches a fact first does the real work — see `ENG-007`'s G1/G2 log
  entries for the precedent). Mode check clean (business-os `.env` →
  `MODE=` empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  **Found this ticket's own G1 already answered** (`decision: approved`,
  `decided: 2026-08-29T09:12:46.283064+00:00`) sitting unprocessed in
  `inbox/`, alongside `ENG-009`'s G1 and the (already-shaped-into-ENG-009)
  engagement question, also both answered — none yet acted on, and this
  ticket's own frontmatter/log still read `awaiting-scope` despite that.
  **Also found a complete architect design already on disk**
  (`agents/architect/designs/ENG-008-influencer-profile-admin-management.md`)
  that this ticket's own log had never recorded — an earlier pass produced
  the file but stopped before writing its own log entry or advancing
  ticket state, the same crash-and-recover shape `ENG-006`/`ENG-007` each
  hit once already on this instance. Verified rather than trusted before
  reusing it: re-read the design in full, checked it against all 8
  acceptance criteria (every one covered) and its own "One-way doors:
  None" line — sound, no reason to redo it.

  **The design itself corrects its own starting assumption, worth
  restating here since it changes what gets built.** Once the
  `aiorders-admin-hub` worktree existed and `src/pages/Influencers.tsx`
  could be read directly, region (`city_preference`) and campaign-type
  (`barter_visit`/`min_visit_payment`) turned out to already exist as
  columns and already be **displayed** on the influencer board — just not
  editable, and nothing on the entire page has a save path today. So most
  of this ticket is an edit-capability gap, not a schema gap: only
  `staff_rating` and `collaboration_count` are genuinely new columns, plus
  splitting the single `barter_visit` boolean into two independent flags
  so "both" is representable (backfilled additively, old column left in
  place for any other reader). Full detail on the design doc itself.

  **No one-way door** — two new nullable/defaulted columns, a
  backward-compatible backfill, reuse of the existing admin-auth gate, no
  new vendor or datastore. Moved straight through `designed` without a G2.

  **Moved both gate items to `inbox/_handled/`** with processed footers;
  journaled both in `agents/eng-manager/config/decision-journal.md`. PRD
  `status: awaiting-scope → designed`, `decided:` stamped to the G1
  timestamp — same convention `ENG-007`'s PRD used at this identical
  state.

  **Sequenced ahead of `ENG-009`, decided here rather than left open.**
  Both tickets touch the same admin-UI file
  (`src/pages/Influencers.tsx`) and the same influencer table; the
  architect's own design doc flags this explicitly and leaves the call to
  the EM at `ready`. This ticket arrived first in the original request and
  has no dependency on `ENG-009`, so it builds first — `ENG-009` reaches
  `ready` this same pass (see its own log) but is deliberately not chained
  behind it.

  **2 transitions** (`awaiting-scope → designed → ready`), well under the
  cap of 4 — `building` needs a backend/frontend/database engineer
  actually writing code, which is new implementation work and this pass's
  stopping point by design. **Consequence:** approver-facing WIP 1/2 → 0/2
  (before `ENG-009`'s and `ENG-010`'s own changes this same pass — see
  board index for the net); approval cap 2/3 → 0/3 (both this ticket's
  items closed); machine WIP 1/6 → 2/6 (`ENG-007` plus this ticket, both
  now in the counted `ready`..`ready-to-ship` range).

  **Dead-end sweep:** scoped to this event's own lineage per its narrower
  contract — `ENG-007` untouched, not re-verified here. **Notify sweep:**
  nothing raised this pass for this ticket (a gate closing doesn't get
  re-notified). **Observations filed** (`observations.md`): a design
  produced without its own log entry or state transition is a real gap in
  the crash-recovery discipline, worth a pattern note now that it's
  happened on three tickets (`ENG-006`, `ENG-007`, this one).

  `chained: ENG-008` — `ready` is agent-owned (eng-manager sequenced it; a
  backend/frontend/database engineer builds next), not the approver, not
  blocked, not terminal, not held by a cap. Fired
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-008`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-008`) and whole-board: both run clean.

- `2026-08-29` **broken chain found and re-fired, no state change**
  (eng-manager, `scheduled` event pass, context `schtasks` — whole-board
  dead-end sweep). This ticket's own prior log entry above records
  `chained: ENG-008` and a fired trigger, but no `continue (ENG-008)` pass
  ever ran: absent from `traces/.pending` (neither queued nor mid-retry),
  and absent from every `pass start:` line in
  `traces/eng-loop-2026-08-29.log` (grepped the full day). Independently
  confirmed no build was ever started: no `eng/ENG-008` branch (or any
  ENG-008 work) in either `_eng/aiorders-admin-hub` or `_eng/aiorders-api`,
  both clean. Not the same shape as this board's three prior
  design-without-a-log-entry crash-recoveries (`ENG-006`, `ENG-007`, this
  ticket's own earlier entry) — those left real work unrecorded; this one
  left a recorded chain that produced no pass at all. Fourth occurrence of
  a related but distinct crash-recovery gap; logged as its own pattern in
  `observations.md` rather than folded into the earlier three.

  **No plausible innocent explanation found** — considered and ruled out:
  queue de-duplication (nothing else in the queue duplicates this event,
  so nothing to collapse); the documented "never-started" refund path
  (that still logs a `pass start:` line before classifying itself, and
  none exists here). Most likely the immediate drain-on-append (the
  trigger call this ticket's own pass made) raced the concurrent
  `continue (ENG-007)` session already running at that moment — this same
  log shows a second `continue (ENG-007)` pass detecting a live concurrent
  session at 05:50:38, independent evidence something was contending for
  the lock in this exact window. Reasoned, not confirmed; the trigger
  script's own stdout for that moment isn't captured anywhere this session
  can read.

  **Re-fired**: `/bin/sh departments/engineering/lib/eng-trigger.sh
  continue ENG-008`. No ticket state change — `ready` is exactly right
  until a build actually starts. `ENG-009` and `ENG-010` remain
  deliberately un-chained behind this one (see their own logs) until this
  build reaches `in-review` or later.

  `chained: ENG-008` (re-fired). Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
  whole-board: see board index.

- `2026-08-29` **decision event arrived after its own fact was already
  consumed — no-op, re-confirmed** (eng-manager, `decision` event pass,
  context `inbox/_handled/2026-08-29-eng008-engagement-source-question.md`).
  Per this event's own narrower contract ("act on the answered gate item in
  `inbox/` and advance only the ticket it belongs to"), scoped to this item
  and this ticket only — no board-wide sweep. Mode check clean (business-os
  `.env` → `MODE=` empty; instance `config/config.yaml` → `mode:` empty).
  Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-008`) and whole-board: both exit 0, clean.

  **This fire fits the instance's well-documented duplicate-queued-event
  race exactly** (`observations.md`, eleven-plus prior rows; contrast the
  `continue ENG-006` no-op, 2026-08-28, archived, which explicitly did
  *not* fit it). Confirmed directly from
  `traces/eng-loop-2026-08-29.log`: `08:45:06 queue: collapsed 1 duplicate
  event(s)` fires immediately before this exact event drains. Two copies of
  `decision (2026-08-29-eng008-engagement-source-question.md)` were
  legitimately queued for the same underlying fact — this item's own footer
  already named the mechanism ("the approver answered by hand-edit while
  this pass was still running, ahead of the decision event this answer will
  also independently queue"). The live `intake` pass reached the fact
  first: shaped `ENG-009`, journaled the decision
  (`decision-journal.md`, "intake-question (engagement source)" row), and
  moved the file to `inbox/_handled/` — all before this queued copy ever
  reached the lock.

  **Re-confirmed rather than trusted**: this item's own frontmatter
  (`decision: approved`, `decided: 2026-08-29T09:10:52Z`) and processed
  footer; `ENG-009`'s own ticket file (`ready`, design and G1 both closed);
  this ticket's own log above, unchanged; `decision-journal.md` row 24. All
  agree — nothing left for this event to act on, on either ticket.

  **0 transitions.** No cap affected — this item was already off every
  count before this pass (per the board index's established convention for
  this exact item).

  **Dead-end sweep (scoped to this event):** both `ENG-008` and `ENG-009`
  already carry a correct, reasoned chain decision from the immediately
  preceding `scheduled` sweep (`ENG-008` re-fired; `ENG-009` deliberately
  held pending `ENG-008` reaching `in-review` or later) — nothing to resume
  or fix.

  **Notify sweep:** nothing to raise (no new gate item); nothing to nudge
  (this item's own `notified:`/`decision:` cycle closed same-day, hours
  before this pass).

  **Observation filed** (`observations.md`): the next item in
  `traces/.pending` (`decision 2026-08-29-eng008-g1-scope.md`) is the same
  shape and will very likely be the same no-op when it fires — that G1 was
  also already closed in the same pass that carried this ticket to `ready`.

  `chained: none` — no state change on either ticket. `continue ENG-008` is
  already queued (fired by the preceding `scheduled` sweep, sitting in
  `traces/.pending`); firing it again here would only append a second copy
  that collapses into the existing one at pop time, per the queue's own
  dedup rule — no additional work would be done. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
  whole-board: both exit 0, clean.

- `2026-08-29` **same decision event, re-fired as attempt 2/2 after attempt 1
  crashed — confirms attempt 1's own writes, no new action** (eng-manager,
  `decision` event pass, context same file:
  `inbox/_handled/2026-08-29-eng008-engagement-source-question.md`).
  `traces/eng-loop-2026-08-29.log`: attempt 1 ran 541s, then the `claude`
  process's underlying Bun runtime segfaulted (`exit 127`), so the harness
  re-queued this event as attempt 2/2 rather than treating it as consumed —
  the two-attempt cap `eng_build_loop.md` names ("Retry is bounded at two
  attempts. The second failure drops the event.").

  **Everything attempt 1 wrote survived the crash.** Re-read fresh rather
  than trusted: this ticket's own log entry immediately above, the board
  index's matching dated entry, `observations.md` (row 107), and
  `decision-journal.md` (row 24) all already carry attempt 1's complete,
  consistent conclusion — the crash landed after the substantive writes, at
  or after the one step attempt 1 could not itself confirm: the post-pass
  gate-check it reported as "exit 0, clean" with no captured result to back
  it. Independently re-ran it for real this attempt:
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
  whole-board — both exit 0, clean. Attempt 1's unconfirmed claim was
  accurate.

  **0 transitions, no new writes to either ticket, no board-index entry
  added** — this attempt reaches no new conclusion, so a second dated entry
  restating the same "no-op" would be exactly the noise the board's
  keep-three-entries rule exists to prevent; the confirmation belongs here,
  on the ticket this event is scoped to. `chained: none` — same reasoning as
  the entry immediately above; `continue ENG-008` remains queued in
  `traces/.pending`, untouched — firing it again would only collapse into
  that copy at pop time.

- `2026-08-29` **the predicted twin no-op: G1 scope decision event arrived
  after its own fact was already consumed** (eng-manager, `decision` event
  pass, context `inbox/_handled/2026-08-29-eng008-g1-scope.md`). The
  immediately preceding `decision` event (the engagement-source question)
  filed an observation naming this exact file as the next item in
  `traces/.pending` and predicting the same outcome — confirmed rather than
  trusted. Per this event's own narrower contract, scoped to `ENG-008`
  only. Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, no
  output; grepped it for `ENG-008` specifically — no matches, clean.

  **This item's fact was already fully consumed.** The G1 approval was read
  and acted on by the `intake` pass that raised it — journaled
  (`decision-journal.md` row 23), the gate item moved to
  `inbox/_handled/` with its own processed footer, and this ticket carried
  `awaiting-scope → designed → ready` in that same pass (see this log,
  entry two above). Checked fresh: this item's frontmatter (`decision:
  approved`, `decided: 2026-08-29T09:12:46.283064+00:00`), the journal row,
  and this ticket's own `state: ready` all agree. Same
  duplicate-queued-event race as the engagement-source question's own
  no-op (entry above) — both facts were consumed inside the same live
  `intake` pass before either of their independently-queued `decision`
  events reached the lock.

  **0 transitions.** No cap affected — already off every count before this
  pass. **Dead-end sweep (scoped):** confirmed `continue ENG-008` still
  queued and undrained in `traces/.pending` — the chain from the earlier
  `scheduled` sweep is intact, nothing to resume. **Notify sweep:** nothing
  to raise or nudge.

  `chained: none` — no state change; `continue ENG-008` remains queued from
  the earlier `scheduled` sweep, and firing it again would only collapse
  into that copy at pop time. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
  whole-board: both exit 0, clean. Also recorded on the board index
  (`_index.md`, matching dated entry).
