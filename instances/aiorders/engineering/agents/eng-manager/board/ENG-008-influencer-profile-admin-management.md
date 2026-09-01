---
id: ENG-008
title: Influencer board admin management — region/campaign-type preference, rating, collaboration count
project: aiorders-admin-hub
type: feature
size: M
time_estimate: half a day to a couple of days
time_spent: ~1 day machine time — build, two code-review rounds (round 1
  fail, round 2 pass), the QA quality gate, plus the security gate; all
  machine time, see log
time_remaining: 0 machine time — release-readiness done, both PRs open. What's
  left is the approver's own merge, on their own schedule (L1). No approver
  time_impact beyond that merge.
severity: P3
priority:
state: blocked
owner: approver
lane: full
blocked_on: approver
blocked_from: ready-to-ship
source: approver
created: 2026-08-29
updated: 2026-08-31
branch: feat/ENG-008-influencer-admin-management (aiorders-api@57f8c4b, aiorders-admin-hub@63be255)
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-008-influencer-profile-admin-management.md
  design: agents/architect/designs/ENG-008-influencer-profile-admin-management.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-008.md
  test_plan: agents/qa/test-plans/ENG-008.md
  security_review: agents/security/reviews/ENG-008.md
  release:
  pr:
    - repo: aiorders-api
      url: https://github.com/harsimranwalia/aiorders-api/pull/6
    - repo: aiorders-admin-hub
      url: https://github.com/harsimranwalia/aiorders-admin-hub/pull/5
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

- `2026-08-29` `ready → building`: built per the design, both repos —
  region/campaign-type edit path, staff rating, collaboration count
  (eng-manager, `continue` event pass, context `ENG-008`, its turn at the
  front of `traces/.pending` finally reached). Narrow scope per the event's
  own contract. Mode check clean (business-os `.env` → `MODE=` empty;
  instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
  whole-board: both exit 0, clean.

  **Both `_eng` worktrees existed** (`aiorders-api`, `aiorders-admin-hub`),
  clean, sitting on `ENG-013`'s branch from its own still-in-flight build —
  not touched. `git fetch` on both confirmed `origin/main` unchanged since
  `ENG-013` last branched (`aiorders-admin-hub` at `edf6947`, `aiorders-api`
  at `40d7c36`). Branched both fresh off `origin/main` as
  `feat/ENG-008-influencer-admin-management`, deliberately not reusing or
  adjacent to `ENG-013`'s `20260829200000` migration timestamp (that one is
  still unmerged on a different branch) — chose `20260829220000`.

  **Verified the live schema before writing the migration**, per the
  design's own named risk (untracked base schema, no `CREATE TABLE` for
  `influencers` in any migration): Supabase MCP, read-only, project
  `bmnmnejwdxbcqinqkwko`. Confirmed none of the four new column names
  already exist, and pulled real distribution on `barter_visit` (306 rows:
  226 true, 29 false, 51 null) to size the backfill and confirm nulls
  backfill to nulls on both new flags rather than a guessed value.

  **Built exactly the four components the design named:**
  `supabase/migrations/20260829220000_add_influencer_admin_fields.sql`
  (`staff_rating smallint CHECK 1–5`, `collaboration_count integer NOT NULL
  DEFAULT 0`, `accepts_paid`/`accepts_barter` booleans backfilled from
  `barter_visit`, which is left untouched); new
  `admin-portal/handlers/influencers.ts` (`GET`/`PATCH` by id, admin/
  sub-admin gate checked in-handler — same narrower pattern `ENG-007`'s
  `loyalty-config.ts` and `ENG-013`'s `foodswipe.ts` both already use, not
  the shared four-role gate); routed from `index.ts`; edit form added to
  `aiorders-admin-hub`'s existing (previously entirely read-only) influencer
  detail dialog — region preference, independent paid/barter checkboxes
  plus a minimum-payment field, a 1–5 rating select, a collaboration-count
  input — plus the table's Payment Type badge now reads the two new flags
  instead of the single `barter_visit` boolean, so "both" renders for the
  first time.

  **Artifact-enumeration grep (step 6b) caught a real cross-ticket bug
  before it shipped.** Grepped `accepts_paid`, `accepts_barter`,
  `staff_rating`, `collaboration_count`, and `handlers/influencers` across
  `instances/` and `departments/`. Found `ENG-009`'s own design doc (a
  sibling ticket touching this same handler and this same page, sequenced
  to build after this one) had already read `admin-portal/index.ts`'s CORS
  header and recorded `Access-Control-Allow-Methods` as `'GET, POST, PUT,
  DELETE, OPTIONS'` — **no `PATCH`** — while this ticket's own design
  specifies a `PATCH` endpoint. Confirmed directly against the file rather
  than trusting the other ticket's doc: accurate. Unfixed, every browser
  preflight for this endpoint would have failed silently (CORS rejects the
  actual request client-side, before it's ever sent) — `deno check`,
  `npm run lint`, and `npm run build` would all have stayed green, since
  none of them execute an actual cross-origin request. Fixed in this same
  hop, in both files that carry the constant (`index.ts` and this ticket's
  own `influencers.ts`): added `PATCH` to the allow-list. `ENG-009`'s doc
  had named the same two options (widen CORS, or use `PUT` instead) and
  left the choice to whichever ticket lands first — took the CORS-widening
  option to stay consistent with this ticket's own already-approved design,
  which specifies `PATCH` explicitly.

  **`ENG-009`'s design also flags a cross-ticket naming overlap on
  `collaboration_count`** — it can derive a true collaboration signal from
  `influencer_invitations` and recommends "drop `collaboration_count` from
  `ENG-008`, or keep it only if explicitly relabelled an off-platform
  tally," explicitly leaving the call to "the EM's and PM's call" and
  touching nothing here itself (its own proposed field is named `activity`,
  not `collaboration_count`, and it reads/writes no column this ticket
  owns). Not acted on in this pass: this ticket's G1 and design are already
  approved with `collaboration_count` as a manually staff-edited field
  (PRD: "not derived from a real collaboration-history ledger" — a product
  choice, not only a fact-gap, since a manual tally can include off-platform
  collaborations no invitation row would ever capture), and re-opening an
  approved scope mid-build on a sibling ticket's not-yet-approved
  recommendation is outside this event's narrow contract. Left for
  `ENG-009`'s own build pass or the PM to weigh in on when that ticket is
  next picked up — already correctly flagged in `ENG-009`'s own design doc,
  restated here only so this ticket's own log carries the same context.

  **Self-tested:** `deno check` on the new/modified edge function files —
  clean, zero errors (isolated the new handler file specifically to confirm
  the 17 errors surfaced by a whole-tree check are 100% pre-existing, in
  `auth.ts`/`partners.ts`/`users.ts`, none touched by this ticket, same
  shape `ENG-013` recorded). `npm run lint` on `aiorders-admin-hub` — 150
  pre-existing errors, same count `ENG-013` recorded, zero new; the one
  warning inside `Influencers.tsx` (`useEffect` missing-dependency on
  `fetchData`) predates this change, confirmed against the pre-edit file
  rather than assumed. `npm run build` — clean, no new warnings beyond the
  pre-existing chunk-size notice. No live/staging Postgres CLI on this
  host, so the migration statement itself has not been executed anywhere —
  named rather than assumed away in the migration doc, same residual gap
  `ENG-007`/`ENG-011`/`ENG-013` each already carry.

  **Database migration doc written**
  (`agents/database/migrations/ENG-008-influencer-profile-admin-management.md`)
  — live row counts, RLS non-issue (service-role client bypasses it, same
  as every other admin-portal write), rollback statement, and the
  deliberately-not-dry-run gap, same structure `ENG-007`/`ENG-011`/`ENG-013`
  established.

  **Both branches committed and pushed**
  (`aiorders-api@e240767`, `aiorders-admin-hub@f2ea36c`); no PR opened yet
  — that's devops's release step. PR bodies drafted here:

  *aiorders-api* — title: `Add admin-editable influencer preference,
  rating, and collaboration fields (ENG-008)`. Body: new `staff_rating`
  (1–5) and `collaboration_count` columns on `influencers`; splits
  `barter_visit` into independent `accepts_paid`/`accepts_barter` flags so
  "both" is representable, backfilled additively, `barter_visit` itself
  untouched. New `GET`/`PATCH admin-portal/influencers/{id}`, admin/
  sub-admin gated. Widens CORS `Access-Control-Allow-Methods` to include
  `PATCH` (previously absent — see migration doc and ticket log for how
  this was caught). No RLS change (service-role client). Migration doc:
  `agents/database/migrations/ENG-008-influencer-profile-admin-management.md`.

  *aiorders-admin-hub* — title: `Add edit form for influencer region,
  campaign type, rating, and collaborations (ENG-008)`. Body: the
  Influencer Management page had no save path anywhere; adds one to the
  existing detail dialog (region, paid/barter + min payment, rating,
  collaboration count) via the new `aiorders-api` endpoint above. Payment
  Type badge now reads the two new flags instead of the single
  `barter_visit` boolean. No visual change to any other page.

  **1 transition** (`ready → building`; the actual build work happened
  inside it), well under the cap of 4 — the next hop (review + quality,
  combined) is a fresh session's work by design, same as every other ticket
  at this state on this board. **Consequence:**
  machine WIP unaffected (`ENG-008` was already inside the counted
  `ready..ready-to-ship` range at `ready`; `building` is still inside it).
  No approver-facing or approval-cap change — this hop touches no gate.

  **Dead-end sweep:** scoped to this event's own lineage per its narrower
  contract — the rest of the board untouched, not re-verified here.
  **Notify sweep:** nothing raised this pass (no gate item written).
  **Observations filed** (`observations.md`): the CORS/PATCH catch above,
  as a concrete example of step 6b's artifact-enumeration paying for itself
  on a bug none of the three local self-tests (`deno check`, lint, build)
  could have caught.

  `chained: ENG-008` — ticket sits at `building`, agent-owned (the build
  itself is done; the next hop is code review + quality, combined, per this
  loop's own design for why that isn't done in the same session) — not the
  approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-008`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-008`) and whole-board: see board index.

<!-- merge note: local (HEAD) and remote logs diverged after the round-1 test-gap-closed entry. Local recorded round-2 review, security, and release-readiness all passing on 2026-08-29, holding at ready-to-ship behind the approver-facing WIP cap. Remote (dated 2026-08-30/08-31, run on a separate host that never saw local's pass) found the ticket still at building, re-ran round-1 review, and caught a second, real bug (a null-coalescing default on accepts_paid/accepts_barter that fabricated a value for null preferences) that local's pipeline had missed. Kept remote's fuller, later account below since it supersedes local's: it re-verifies everything local's pipeline covered, fixes an additional real defect, and carries the ticket further (both PRs opened, blocked on the approver) than local's cap-held ready-to-ship. -->
- `2026-08-30` (dead-end sweep, no state change) `scheduled` event pass,
  context `launchd`. Ticket still `building`/`eng-manager`, unchanged since
  the entry above. That entry's own `continue ENG-008` fire is not visible
  in any drain of `traces/eng-loop-2026-08-29.log` or `-30.log` — the only
  `continue` that actually ran on either day was `ENG-023`'s (twice, both
  failed on infra, see `inbox/2026-08-30-eng-events-dropped.md`) and this
  pass itself. No evidence the code-review-plus-quality hop this ticket is
  waiting on ever ran. Re-firing rather than leaving it starved:
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-008`.
  Safe regardless of whether the original fire is genuinely lost or merely
  still queued — duplicate `<event> <context>` lines collapse to one before
  each pop, so this cannot double-run the hop. `chained: ENG-008`.

- `2026-08-30` **code review round 1: FAIL — automatic-failure #10, plus a
  real null-handling bug** (principal-engineer, `continue` event pass,
  context `ENG-008` — this fire's own turn at the front of
  `traces/.pending`, re-fired by the 2026-08-30 `scheduled` sweep above
  after the original 2026-08-29 fire never ran). Narrow scope per the
  event's own contract (resume this ticket only; no board-wide sweep). Mode
  check clean (business-os `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty, falls through). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
  whole-board: both exit 0, clean.

  **Read the diff correctly, not naively.** Both branches
  (`aiorders-api@e240767`, `aiorders-admin-hub@f2ea36c`) were cut before
  `ENG-007` and `ENG-011` merged directly to `main` (2026-08-30 `scheduled`
  sweep, above); a raw `git diff origin/main..{commit}` therefore shows both
  tickets' shipped work as spurious deletions (`loyalty-config.test.ts`,
  `brands.ts`'s `deriveStage`/`deriveHealth`, `Brands.tsx`'s stage/health UI,
  `.github/workflows/deploy-cf.yml`) that ENG-008 never touched. Confirmed
  via `git show --stat` on each commit (3 files / 197 insertions on
  `aiorders-api`; 1 file / 190 insertions on `aiorders-admin-hub`, matching
  the build entry's own account exactly) and via merge-base diffing
  (`git merge-base origin/main {commit}`) that these are 100% main-drift
  artifacts, not this ticket's changes — reviewed the isolated single-commit
  patch on each branch instead of the polluted two-dot diff.

  **Automatic failure #10 — zero test coverage on the new admin-gated write
  path**, same class that failed `ENG-013`'s own round 1 one cycle earlier on
  this identical repo (`observations.md` row 130).
  `supabase/functions/admin-portal/handlers/influencers.ts`:
  `hasInfluencerAdminAccess` (line 22) and `updateInfluencer` (line 97) carry
  no test at all. No test proves a non-admin/sub-admin caller is rejected —
  PRD acceptance criterion 8, verbatim: "Given a non-admin/non-staff request
  to any of the above write paths, then it's rejected." No test proves
  `staff_rating` outside 1–5 or a negative `collaboration_count` is rejected.
  No test proves the field allowlist (`EDITABLE_FIELDS`, line 13) actually
  restricts what a caller can write. Direct, exact precedent in this same
  repo: `loyalty-config.test.ts` (44 tests, including the identical
  access-check shape — admin, sub-admin, wrong role, missing profile) and
  `brands.test.ts`. Not this repo's baseline (there is none — no
  `deno.json`, per `config/projects.md`) but this *board's* baseline, twice
  now in two days.

  **A second, independent finding: a real correctness bug, not a style
  preference.** `src/pages/Influencers.tsx`, `openInfluencer` (line 92),
  specifically lines 96–97:
  ```
  accepts_paid: influencer.accepts_paid ?? !influencer.barter_visit,
  accepts_barter: influencer.accepts_barter ?? !!influencer.barter_visit,
  ```
  For the 51/306 influencer rows where `barter_visit` was `null` in
  production (the exact figure this ticket's own `building` entry pulled
  from Supabase), the migration correctly backfills `accepts_paid`/
  `accepts_barter` to `null` on both — preserving "unknown" as the design
  doc explicitly requires ("null must stay distinguishable from a real
  value," design → Data). This line then silently discards that: `null ??
  !null` evaluates `!null`, and `!null === true` in JavaScript — so opening
  the edit dialog on any of these 51 influencers computes `accepts_paid:
  true, accepts_barter: false` as if known. `handleSaveInfluencer` (line
  104) includes both fields in the `PATCH` body unconditionally, with no
  dirty-tracking — so staff saving *any* unrelated field (a rating, a
  collaboration count) on one of these records silently writes a fabricated
  "Paid only" preference into the database. This is exactly the failure
  mode the migration's own backfill was written to avoid, one layer up.
  **The fix belongs with the missing test above**: default both to `false`
  (or track which the user actually touched) when the source is null, and
  add the regression test — an influencer with `accepts_paid`/
  `accepts_barter`/`barter_visit` all null, open the dialog, confirm neither
  checkbox pre-checks and neither is written unless the user checks it.

  **One unrelated line, flagged but not blocking by itself**:
  `Influencers.tsx` line 539, `<Button variant="secondary">` on the existing
  "Contact" button — a cosmetic change to code this ticket had no reason to
  touch (automatic-failure #7 territory, but trivial and zero-risk; worth
  dropping to keep the diff to exactly what the ticket describes, not worth
  a round on its own).

  **One heads-up for whoever opens the PR, not a review finding**:
  `aiorders-api`'s `index.ts` has a genuine adjacent-line addition from both
  this ticket and `ENG-007` (now on `main`) at the same anchor (the
  router's `else if` chain, right after `foodswipe`) — each branch's own
  single-commit diff is independently correct, and a real three-way merge
  should interleave both cleanly, but worth confirming rather than assuming
  when `release-runner` rebases this branch before opening the PR, since the
  merge-base is now two tickets behind `main`.

  **Genuinely good work, worth saying plainly**: the build hop's own
  step-6b artifact-enumeration grep (already logged in the `ready →
  building` entry above) caught a real CORS/`PATCH` bug before it ever
  reached this gate — exactly what that step exists for, and it means this
  review found two remaining issues instead of three.

  **Verdict: FAIL, round 1.** No receipt written
  (`agents/principal-engineer/reviews/ENG-008.md` stays absent, per
  `skills/code-review-gate/SKILL.md` step 8 — a receipt is written on `pass`
  only). QA's hop not run this round — discarded per the combined-hop
  design, no test-plan file written. Findings logged here and in
  `agents/principal-engineer/notebook/2026-08-30-review-log.md`.

  **0 net transitions** — `state`/`owner` unchanged (`building`/
  `eng-manager`), matching this board's own `ENG-013` round-1 precedent: the
  gate is reached and routed back on the fail verdict without a persisted
  `in-review` frontmatter state. `machine_wip` unaffected, still 4/1.
  Approver-facing WIP and approval cap both unaffected — a code-review
  failure is not an approver-facing gate.

  **Dead-end sweep (scoped to this event):** nothing else on this ticket's
  own lineage to resume. **Notify sweep:** nothing raised (a review failure
  isn't a gate item; it routes back to `building`, not to the approver).
  **Observations filed** (`observations.md`): the second occurrence, same
  day, same repo, of the identical automatic-failure-#10 shape (ties to row
  130); a genuine gap found but not fixed here — this ticket's own
  frontmatter has never carried `time_estimate`/`time_spent`/
  `time_remaining` despite `definition-of-done.md` and the ticket template
  both calling for them from `building` onward.

  `chained: ENG-008` — `building` is agent-owned (the two findings above are
  the next hop's work), not the approver, not blocked, not terminal, not
  held by a cap. Fired
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-008`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-008`) and whole-board: see board index.

- `2026-08-31` **round 1's two findings fixed: missing-profile/allowlist test
  gaps closed on top of an undocumented existing commit, and the null-bug
  fixed for real** (eng-manager, `continue` event pass, context `ENG-008`).
  Narrow scope per the event's own contract (resume this ticket only; no
  board-wide sweep). Mode check clean (business-os `.env` → `MODE=active`;
  instance `config/config.yaml` → `mode:` empty, falls through). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
  whole-board: both exit 0, clean.

  **Both worktrees fetched and checked out onto this ticket's branch**
  (`aiorders-api` was sitting clean on `ENG-013`'s branch, `aiorders-admin-hub`
  clean on `ENG-005`'s — both from other tickets' own continue passes; no
  mid-work found on either, safe to switch).

  **Found a second undocumented commit, same shape as `ENG-013`'s
  2026-08-30 discovery, but not the same outcome.** `aiorders-api` carried
  `dc6972a` ("Add missing test coverage for admin-portal influencer handler
  (ENG-008)") on top of this ticket's own recorded `e240767`, same
  automation identity (`businesspilotcare-gif`), already pushed — this
  ticket's own log and frontmatter knew nothing about it. Investigated
  rather than trusted, per the same practice `ENG-013` established: read
  `influencers.ts` and the new `influencers.test.ts` in full and
  hand-traced every test against the live handler logic (no `deno` on this
  host, same residual gap `ENG-013` already named). Unlike `ENG-013`, this
  commit was **not simply accept-and-move-on** — it was correct as far as
  it went (all field-validation rejections, the three role-shaped access
  cases, one mocked success path — all hand-traced and confirmed correct)
  but **incomplete against round 1's own review notebook**
  (`agents/principal-engineer/notebook/2026-08-30-review-log.md`), which
  named exactly four `hasInfluencerAdminAccess` cases — "admin, sub-admin,
  wrong role, missing/undefined profile" — and asked for proof "the field
  allowlist (`EDITABLE_FIELDS`) actually restricts what a caller can
  write." The found commit covered the first three access cases and every
  field's own validation, but neither of those two. Observation filed
  (`observations.md`) naming this as its own nuance: verifying a found
  commit means checking it against the finding it was supposed to close,
  not only checking that what's already there is internally correct.

  **Checked whether the missing-profile case was live risk before treating
  it as one.** Read `admin-portal/index.ts`'s router (`getAuthenticatedUser`
  equivalent, lines 62–126): it already 401s on no user and 403s on no
  `profiles` row **before any handler runs**, so `auth.user.profile` is
  guaranteed non-null by the time `hasInfluencerAdminAccess` is called —
  not reachable in production today. Fixed anyway: round 1 named it
  explicitly, the repo's own established precedent
  (`loyalty-config.ts`'s `hasLoyaltyConfigAccess(profile: ... | null |
  undefined)`, with its own dedicated "rejects a missing profile" test)
  already treats this defensively, and closing what a failed review
  explicitly asked for is this hop's job, not a judgement call to
  second-guess. `hasInfluencerAdminAccess`: `userProfile.role` /
  `userProfile.additional_roles` → `userProfile?.role` /
  `userProfile?.additional_roles`. Added
  `hasInfluencerAdminAccess rejects a missing profile` (null and undefined,
  both hand-traced to `false`, no throw).

  **Field-allowlist test**: added
  `handleInfluencers PATCH strips fields outside the editable allowlist
  before writing` — a PATCH body mixing a valid field (`staff_rating: 4`)
  with three fields never named in `EDITABLE_FIELDS` (`role`, `is_admin`,
  `id`, the exact shape a privilege-escalation or cross-record write
  attempt would take) — captures what's actually passed to
  `adminSupabase....update()` and asserts it's exactly `{ staff_rating: 4
  }`. Hand-traced against `updateInfluencer`'s field-by-field
  `if ('x' in body)` construction: correct, since unlisted keys are never
  copied into `update` regardless of what the caller sends.

  **Independently re-verified the CORS/`PATCH` fix from the original build
  hop is still intact** (untouched by this pass, but it's the kind of thing
  a rebase or a sibling ticket's touch could have quietly reverted):
  `admin-portal/index.ts` line 17 still carries `PATCH` in
  `Access-Control-Allow-Methods`. Fine.

  **The real bug — `Influencers.tsx`'s null-coalescing default — fixed
  properly, not just patched.** Read the review notebook's own prescribed
  fix closely: "default both to false (or track which the user actually
  touched)... **and add the regression test**... confirm neither checkbox
  pre-checks and **neither is written unless the user checks it**." The
  second half only holds under dirty-tracking — a blanket default-to-`false`
  would stop pre-checking the box but would still send `false`
  unconditionally on every save (same unconditional-inclusion bug the
  review flagged, just with a less actively-wrong value), so implemented
  the stronger fix: `InfluencerEditForm.accepts_paid`/`accepts_barter`
  widened to `boolean | null`; `openInfluencer` now passes
  `influencer.accepts_paid`/`accepts_barter` straight through instead of
  coalescing against `barter_visit` at all (confirmed this fallback was
  never reachable with a correct substitute: the migration backfills both
  new flags from `barter_visit` **additively**, so every row where
  `accepts_paid` is null also has `barter_visit` null in that same row —
  the `!barter_visit` fallback evaluated `!null → true` in 100% of the
  cases it ever fired, never anything else); both `Checkbox` components
  render `checked={editForm.accepts_paid ?? false}` (visually unchecked for
  null, independent of the stored form state); `handleSaveInfluencer` now
  omits `accepts_paid`/`accepts_barter` from the PATCH body entirely while
  either is still `null`, following the exact conditional-inclusion pattern
  the function already uses for `min_visit_payment` — so the backend's own
  `'accepts_paid' in body` check (unchanged, `influencers.ts` line 109)
  never fires and the column stays untouched. An influencer whose
  preference was never set now stays unset through any number of saves
  until a staff member actually clicks one of the two checkboxes.

  **Dropped the one unrelated cosmetic change round 1 flagged but didn't
  block on**: `<Button variant="secondary">` on the Contact button reverted
  to `<Button>`, keeping the diff to exactly what this ticket describes.

  **Self-tested with this repo's only available tools** (no test framework
  installed, per the proposal filed below): `npm run build` — clean, same
  pre-existing chunk-size notice only, no new warnings. `npm run lint` —
  150 errors, identical count to this ticket's own `ready → building`
  entry and to `ENG-013`'s recorded baseline, zero new; `Influencers.tsx`
  carries only the same pre-existing `useEffect` missing-dependency
  warning on `fetchData`, confirmed unchanged.

  **No automated frontend regression test.** Confirmed fresh this pass
  (not assumed from `config/projects.md`'s week-old table):
  `aiorders-admin-hub`'s `package.json` has no `vitest`/`jest`/
  `@testing-library` dependency and no `test` script; a repo-wide sweep
  found zero `*.test.*`/`*.spec.*` files. Building a test harness from
  scratch inside this fix is out of scope for a bug fix — same reasoning
  `restaurant-portal`'s own harness (`ENG-002`) was an approver-originated
  ticket, not something a feature pass invented for itself. Proposal filed
  (`proposals.md`) naming the gap and sizing the fix (`M`) rather than
  silently shipping without one.

  **Both branches committed and pushed**, automation identity
  (`businesspilotcare-gif`, same as every prior commit on this ticket):
  `aiorders-api@57f8c4b` ("Cover missing-profile and
  allowlist-enforcement gaps in influencer admin tests (ENG-008)", on top
  of the found `dc6972a`), `aiorders-admin-hub@63be255` ("Fix
  accepts_paid/accepts_barter fabricating a value on null preferences
  (ENG-008)"). Frontmatter `branch:` updated to both new hashes.

  **0 net frontmatter transitions** — `state`/`owner` unchanged
  (`building`/`eng-manager`): fixing a failed review's findings is build
  work, and the next machine-owned checkpoint (`in-review`) is only reached
  by a fresh review-plus-quality session actually passing it, same
  precedent this ticket's own round-1 entry and `ENG-013`'s 2026-08-30
  entry both already established. `machine_wip` unaffected (still inside
  the counted `ready..ready-to-ship` range at `building`). No
  approver-facing or approval-cap change — this hop touches no gate.

  **Dead-end sweep (scoped to this event):** nothing else on this ticket's
  own lineage to resume. **Notify sweep:** nothing raised this pass (no
  gate item written; a build-fix hop isn't a gate). **Observations/
  proposals filed:** see above — one proposal (`aiorders-admin-hub` test
  infrastructure), one observation (verify-found-work-against-the-finding,
  not just against the code).

  `chained: ENG-008` — `building` is agent-owned (the next hop is code
  review + quality, combined, round 2), not the approver, not blocked, not
  terminal, not held by a cap. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-008`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-008`) and whole-board: see board index.

- `2026-08-31` **code review round 2: PASS, plus the quality gate — now
  in-qa** (principal-engineer then qa, `continue` event pass, context
  `ENG-008`, this fire's own turn at the front of `traces/.pending`). Narrow
  scope per the event's own contract (resume this ticket only; no
  board-wide sweep). Mode check clean (business-os `.env` → `MODE=active`;
  instance `config/config.yaml` → `mode:` empty, falls through). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
  whole-board: both exit 0, clean.

  **Re-derived both diffs from disk rather than trusting the prior pass's
  own account.** Both worktrees confirmed clean, on branch, at the recorded
  commits (`aiorders-api@57f8c4b`, `aiorders-admin-hub@63be255`); `git
  fetch origin main` plus `git merge-base` on each repo confirmed a clean
  diff (4 files / 404 insertions on `aiorders-api`, 1 file / 202
  insertions/14 deletions on `aiorders-admin-hub` against each repo's own
  merge-base) — no main-drift pollution this round.

  **Automatic-failure scan: 0/10 open.** Both round-1 findings independently
  re-verified, not taken on trust: hand-traced all 19 `Deno.test` cases in
  `influencers.test.ts` against `influencers.ts` at HEAD (no `deno` on this
  host, same residual gap every ticket on this repo carries) — the
  missing-profile null-safety fix and the field-allowlist test both check
  out exactly as the fix-pass described. Hand-traced the frontend fix
  independently too: with the migration's additive backfill guaranteeing
  `barter_visit` is null in every row where the new flags are also null, the
  removed `?? !barter_visit` fallback never had a correct value to fall back
  to — confirmed by re-reading the migration's `UPDATE` statement directly,
  not assumed. `#4` (`any`-typed `AuthenticatedRequest`) is pre-existing and
  already tracked as a 2-occurrence pattern by `ENG-013`'s own round-2
  review today; not re-litigated here.

  **One new, non-blocking finding from this round's own full review** (not
  a round-1 regression): `Influencers.tsx`'s `handleSaveInfluencer` sends
  `min_visit_payment` whenever the field is non-empty, independent of the
  current `accepts_paid` value — unchecking "Paid" after a min payment was
  set leaves the stale value in local state and it gets written alongside
  `accepts_paid: false`. Not visible anywhere today (the read path gates
  the "Min: $" display on `accepts_paid`), not named in any of the 8
  acceptance criteria, P3 per `definition-of-done.md`'s severity table (has
  a workaround: re-enter the value). Named in the review receipt rather
  than filed as a bug or proposal — single occurrence, non-blocking, and
  this board has never yet filed anything to `agents/qa/bugs/` for a finding
  at this scale.

  **Frontend regression test still not possible** — reconfirmed fresh
  (not assumed from the fix-pass's own claim) that `aiorders-admin-hub` has
  no test framework, no `test` script, and zero test files anywhere in the
  repo. Same non-blocking treatment `ENG-011`'s own round of review already
  gave this exact class of gap on this exact project. Substitute
  verification: `npm run build` (clean, 3340 modules, same pre-existing
  chunk-size notice) and `npm run lint` (150 errors / 31 warnings, identical
  to this ticket's recorded baseline; `Influencers.tsx` carries exactly the
  one pre-existing `fetchData` missing-dependency warning, zero new) — both
  reproduced fresh this pass, not carried forward from the log.

  **Quality gate (QA):** test plan written,
  `agents/qa/test-plans/ENG-008.md` — all 8 acceptance criteria covered
  (executed-via-fake-client, hand-traced, or inspected; none untestable),
  failure-path table includes the allowlist-escalation shape and the new
  `min_visit_payment` gap named rather than silently dropped. No open P0/P1
  bug anywhere on this board.

  **Receipts written:** `agents/principal-engineer/reviews/ENG-008.md`
  (verdict `pass`, round 2), `agents/qa/test-plans/ENG-008.md`.
  `links.review`/`links.test_plan` set on this ticket. `time_estimate`/
  `time_spent`/`time_remaining` populated for the first time — round 1's
  own observation had flagged these as never carried on this ticket despite
  `definition-of-done.md` calling for them from `building` onward; closed
  here rather than left for another pass to notice again.

  **2 transitions** (`building → in-review → in-qa`), well under the cap of
  4 — stopped deliberately, not by the cap: `config.yaml`'s `combined_hop`
  licenses exactly `[code_review, quality]` together; security is a separate
  hop by design (`sequential_after_quality`), needs this pass's own
  just-written test plan, and `eng_build_loop.md` calls for a fresh session
  there. `machine_wip` unaffected (`ENG-008` stays inside the counted
  `ready`..`ready-to-ship` range). Approver-facing WIP and approval cap both
  unaffected — no gate raised.

  **Dead-end sweep (scoped to this event):** nothing else on this ticket's
  own lineage to resume. **Notify sweep:** nothing to raise (a review/quality
  pass isn't a gate item). **Observations/proposals filed:** none new —
  the frontend-test-harness proposal and the shared-`any`-interface pattern
  are both already tracked by this ticket's own prior entry and by
  `ENG-013`'s today; the `min_visit_payment` gap is named in the review
  receipt, not separately filed, per the reasoning above.

  `chained: ENG-008` — `in-qa` is agent-owned (security next, fresh
  session), not the approver, not blocked, not terminal, not held by a cap.
  Firing `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-008`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-008`) and whole-board: see board index.

- `2026-08-31` **security gate: PASS — now `ready-to-ship`** (security,
  `continue` event pass, context `ENG-008`, this fire's own turn at the
  front of `traces/.pending`). Narrow scope per the event's own contract
  (resume this ticket only; no board-wide sweep). Mode check clean
  (business-os `.env` → `MODE=active`; instance `config/config.yaml` →
  `mode:` empty, falls through). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
  whole-board: both exit 0, clean.

  **Re-derived the diff from disk rather than trusting the prior review's
  own account.** Both worktrees confirmed clean, on branch, at the recorded
  commits (`aiorders-api@57f8c4b`, `aiorders-admin-hub@63be255`); `git fetch
  origin main` plus `git merge-base` on each repo matched code review's own
  figures exactly (4 files/404 insertions on `aiorders-api`, 1 file/202
  insertions/14 deletions on `aiorders-admin-hub`). Read
  `influencers.ts`, `influencers.test.ts`, the migration, `index.ts`'s diff,
  and the full `Influencers.tsx` diff directly — none of the findings below
  are taken on the review's or QA's word alone.

  **Threat-modelled the change** (4 questions, full detail in the receipt):
  new capability is read+write on 6 fields for the same admin/sub-admin
  population that already read all of them (page was 100% read-only
  before this ticket); no new data-classification tier; blast radius if
  fully compromised is identical to `loyalty-config.ts`/`foodswipe.ts`
  (service-role client, RLS bypassed, only the in-code role checks gate
  access) — already-accepted architecture, not a new risk this ticket
  introduces.

  **Negative-auth cases independently verified, not assumed**: no-token/
  invalid-token 401 and no-profile 403 confirmed live in `index.ts`'s
  unmodified `authenticate()`; wrong-role 403 proven by a
  throwing-Proxy-`adminSupabase` test that fails if the gate is ever
  bypassed; the field-allowlist test confirmed mutation-sensitive (asserts
  the exact object passed to `.update()`, not just the response shape) —
  hand-traced against `influencers.ts` at HEAD myself rather than
  re-reading only the code review's summary of it. Body-supplied `id` is
  never used for row selection (URL path id is), so no IDOR shape exists
  even though this handler intentionally has no per-row tenant scoping —
  "any admin/sub-admin, any influencer" is the ticket's own intended shape
  (a shared internal roster), not a gap.

  **OWASP A01–A10 walked**, each marked applicable or `n/a` with a reason;
  full table in the receipt. Nothing blocking. **One non-blocking finding**
  (A05): `getInfluencer`/`updateInfluencer` return a raw `error.message` in
  a 500 body — same shape `ENG-013`'s review already tracked as occurrence
  1/3 on `foodswipe.ts`. Checked this repo's actual extent before logging
  it as a repeat rather than assuming: a grep across
  `admin-portal/handlers/` finds the identical pattern in **8 files total**,
  six pre-dating this department's review process — so three-strike
  tracking here counts *gate-reviewed* occurrences (this is the 2nd), not
  the repo's pre-existing total, or every legacy file would already read as
  a third strike. Logged to `agents/security/notebook/2026-08-31-findings.md`
  rather than blocking on it, same disposition `ENG-013` got for the first
  occurrence. CORS's widened `Access-Control-Allow-Methods` (now including
  `PATCH`) reviewed and found not to change the endpoint's real security
  boundary — the wildcard origin predates this diff and the actual
  authorization boundary is the bearer token, which CORS doesn't protect
  against a direct caller anyway.

  **Secrets**: full diff and branch history on both repos scanned
  (`aiorders-api`: `e240767`/`dc6972a`/`57f8c4b`; `aiorders-admin-hub`:
  `f2ea36c`/`63be255`) for key/token/password/PEM/service-role patterns.
  Two matches, both benign (the CORS header's literal string `apikey`, and
  the frontend's own forwarded user session token) — no leaked credential.
  **Dependencies**: none new on either repo. **LLM checklist**: n/a, design
  frontmatter confirms `touches_models: false`, matches the diff.

  **`min_visit_payment` stale-value-on-uncheck** (code review's own new
  finding this round, P3): independently re-confirmed against the diff
  directly rather than taken on trust — `handleSaveInfluencer` does send it
  unconditionally whenever non-empty, independent of `accepts_paid`. Not a
  security finding (no unauthorized access, no crash, has a workaround);
  named in the receipt's carry-forward section rather than re-raised as a
  fresh finding.

  **Receipt written**: `agents/security/reviews/ENG-008.md` (verdict
  `pass`). `links.security_review` set on this ticket in the same write.
  `time_spent`/`time_remaining` updated — only release-readiness remains.

  **1 transition** (`in-qa → ready-to-ship`), well under the cap of 4.
  **Consequence:** `machine_wip` unaffected — `ENG-008` stays inside the
  counted `ready`..`ready-to-ship` range, still 4/1 (`ENG-009`/`ENG-010` at
  `ready`, `ENG-013` at `ready-to-ship` alongside this ticket now). No
  approver-facing or approval-cap change — a security-gate pass isn't a
  gate item to the approver, and `owner` moving to `devops` is an
  agent-to-agent handoff, not a human wait.

  **Dead-end sweep (scoped to this event):** nothing else on this ticket's
  own lineage to resume. **Notify sweep:** nothing to raise (a security
  pass isn't a gate item). **Observations/proposals filed:** none new — the
  frontend-test-harness proposal and the `AuthenticatedRequest`-`any`
  pattern are both already tracked elsewhere; the raw-error-message finding
  is tracked in the security notebook, not filed as a separate proposal.

  `chained: ENG-008` — `ready-to-ship` is agent-owned (devops's
  release-readiness hop next: open the PR), not the approver, not blocked,
  not terminal, not held by a cap (still inside the same counted machine-WIP
  range this ticket already occupied). Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-008`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-008`) and whole-board: see board index.

- `2026-08-31` **release-readiness: both PRs opened, now blocked on the
  approver** (devops, `continue` event pass, context `ENG-008` — this
  fire's own turn at the front of `traces/.pending`, queued by the
  immediately preceding security-gate pass and drained right behind
  `continue (ENG-013)`, per that ticket's own board-index entry). Narrow
  scope per the event's own contract (resume this ticket only; no
  board-wide sweep). Mode check clean (business-os `.env` → `MODE=active`;
  instance `config/config.yaml` → `mode:` empty, falls through). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
  whole-board: both exit 0, clean.

  **Verified all four upstream gates fresh from the receipt files**, not
  assumed from the frontmatter alone: migration
  (`agents/database/migrations/ENG-008-influencer-profile-admin-management.md`,
  pass), code review (`agents/principal-engineer/reviews/ENG-008.md`, round
  2, pass), quality (`agents/qa/test-plans/ENG-008.md`, pass), security
  (`agents/security/reviews/ENG-008.md`, pass). Both worktrees confirmed
  clean, on `feat/ENG-008-influencer-admin-management`, at the exact commits
  this ticket's own frontmatter records (`aiorders-api@57f8c4b`,
  `aiorders-admin-hub@63be255`), already pushed to `origin` (no ahead/behind
  against the remote branch). `gh pr list --search ENG-008` on both repos
  confirmed no PR already existed — not a duplicate open.

  **Both projects registered L1** (`config/projects.md`) — step 1's window
  check does not apply; went straight to step 4. **Step 3 readiness checks**,
  same interpretation this board already established for `ENG-007`/`ENG-013`
  given no live Postgres CLI reachable from either build host:
  - Rollback: SQL written and reasoned through in the migration doc (not
    live-tested — the named, carried-forward gap every migration on this
    instance shares), paired with reverting the handler/router/frontend
    edit form in the same rollback, same shape `ENG-007`/`ENG-013` already
    used at this identical gate.
  - Observability: both new failure branches log via `console.error` before
    responding (confirmed directly in the security review's A09 line),
    surfaced through Supabase's existing function logs — no new mechanism
    needed.
  - Cost: **$0/month delta** — no new vendor, no new dependency on either
    repo (security review's own Dependencies section, re-confirmed here).
  - Window: n/a, L1.

  **Opened both PRs** (`aiorders-api` first, since `aiorders-admin-hub`'s
  edit form depends on its endpoint): `aiorders-api` PR #6
  (https://github.com/harsimranwalia/aiorders-api/pull/6),
  `aiorders-admin-hub` PR #5
  (https://github.com/harsimranwalia/aiorders-admin-hub/pull/5). Each PR
  body states what it does, the four gates passed with receipt paths, and
  the named non-blocking gaps (raw `error.message` on 500 — 2nd tracked
  occurrence; no frontend test harness on `aiorders-admin-hub`;
  `min_visit_payment` stale-value-on-uncheck, P3) rather than leaving them
  for the approver to discover unaided. Neither worktree needed restoring
  to a different ticket's branch afterward — both were already sitting on
  this ticket's own branch going in, unlike `ENG-013`'s hop which had to
  switch away and back.

  **Wrote the L1 merge-request item**
  (`inbox/2026-08-31-eng008-merge-request.md`), `pr_urls:` as a YAML list of
  `{repo, url}` pairs per `skills/release-runner/SKILL.md` step 4 (one item
  covering both repos, never one per repo). Ran
  `departments/engineering/lib/eng-notify.sh raise` — sent cleanly
  (`traces/eng-notify-2026-08-31.log`: `sent: active
  2026-08-31-eng008-merge-request.md`); stamped `notified:
  2026-08-31T11:15:29` on the item by hand, since the script itself doesn't
  write its own frontmatter back.

  State `ready-to-ship → blocked`, `blocked_on: approver`,
  `blocked_from: ready-to-ship`, owner `devops → approver`. No release
  record yet, per `release-runner`'s own step 7/step 4 split — that's
  written only once the build loop's merge-detection confirms both PRs
  merged, same as `ENG-013`'s current position.

  **1 transition** (`ready-to-ship → blocked`). **Consequence:** `machine_wip`
  3/1 → 2/1 (`ENG-008` leaves the counted `ready`..`ready-to-ship` range —
  `ENG-009`/`ENG-010` at `ready` remain the only two left inside it).
  Approver-facing WIP 1/2 → 2/2 (`ENG-013` plus this ticket now occupy both
  slots — **cap reached**). Approval cap 1/3 → 2/3.

  **Dead-end sweep (scoped to this event):** nothing else on this ticket's
  own lineage to resume. **Notify sweep:** this pass's own item raised and
  stamped above; nothing else to nudge. Approver-facing WIP is now at cap
  (2/2) but the approval cap itself is not (2/3) — no stall notice per
  `lib/eng-notify.sh stall`'s own trigger condition (approval cap full, not
  WIP-cap full). **Observations/proposals filed:** none new — every named
  gap above is already tracked elsewhere (the frontend-test-harness
  proposal, the raw-error-message security-notebook entry).

  `chained: none` — `blocked`, `blocked_on: approver`. This is the human
  gate the whole hop was driving toward; firing `continue ENG-008` again
  would only queue against a ticket with nothing left for a machine to do,
  same reasoning `ENG-013`'s own immediately preceding entry already
  recorded at this identical state. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines.

- **2026-09-01, `scheduled` pass (~15:30, context `launchd`).** Merge
  detection re-run: `git fetch` + `git merge-base --is-ancestor` on both
  repos' worktrees for `feat/ENG-008-influencer-admin-management` against
  `origin/main` — neither merged, ticket unchanged at `blocked`/
  `blocked_on: approver`. The L1 merge-request item
  (`inbox/2026-08-31-eng008-merge-request.md`) was `notified: 2026-08-31T11:15:29`
  with no `nudged:` and no `decision:` — over 24h with no reply, so nudged
  per `eng_build_loop.md` step 7: `lib/eng-notify.sh nudge`, sent cleanly
  (`traces/eng-notify-2026-09-01.log`: `sent: active
  2026-08-31-eng008-merge-request.md`), stamped `nudged: 2026-09-01T22:41:10`
  by hand. First and only nudge — none further after this regardless of how
  long it stays open. `chained: none` — still `blocked` on the approver;
  merging either PR on GitHub is the only thing that advances this ticket.
