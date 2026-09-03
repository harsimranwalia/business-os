---
id: ENG-009
title: Influencer engagement info — internal activity signal plus a staff-editable social stat
project: aiorders-admin-hub
type: feature
size: S
time_estimate: a few hours to half a day
time_spent: ~2h build + ~1h rebase-and-refix (two-repo rebase onto ENG-008's fix commits; one real multi-hunk test conflict resolved by hand in aiorders-api, aiorders-admin-hub's flagged hunk auto-merged correctly; both re-verified and re-pushed) + ~30m review/quality round 2 + ~25m security gate (pass, one three-strike proposal filed) + ~15m release-readiness (two PRs opened, stacked on ENG-008's branch)
time_remaining: 0 machine time — release-readiness done, both PRs open. What's left is the approver's own merge, on their own schedule (L1).
severity: P3
priority:
state: blocked
owner: approver
lane: full
blocked_on: approver
blocked_from: ready-to-ship
source: approver
created: 2026-08-29
updated: 2026-09-02
branch: feat/ENG-009-influencer-engagement-info (aiorders-api@d37e0c9, aiorders-admin-hub@92bcacd)
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-009-influencer-engagement-info.md
  design: agents/architect/designs/ENG-009-influencer-engagement-info.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-009.md
  test_plan: agents/qa/test-plans/ENG-009.md
  security_review: agents/security/reviews/ENG-009.md
  release:
  pr:
    - repo: aiorders-api
      url: https://github.com/harsimranwalia/aiorders-api/pull/7
    - repo: aiorders-admin-hub
      url: https://github.com/harsimranwalia/aiorders-admin-hub/pull/6
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

- `2026-08-29` **approver override, filed by hand in an interactive session —
  not a department pass.** Direct instruction: run `ENG-009` and `ENG-010`
  next, ahead of `ENG-008` finishing its `in-review` gate, rather than
  leaving the board to work the existing `.pending` queue in its prior
  order (several unrelated `continue`/`decision`/`watch` fires for other
  tickets were queued ahead of all four of these and would have burned
  passes before touching any of them). `priority: → next` set directly by
  the approver (this repo's own lever — `eng_build_loop.md`'s "never write
  to priority yourself" binds *agents*, not the approver giving the
  instruction directly). `traces/.pending` reordered by hand to
  `continue ENG-009, continue ENG-010, continue ENG-008, continue ENG-013`
  at the front, the rest of the prior queue preserved unchanged behind
  them.

  **Known risk, surfaced rather than silently accepted:** the sequencing
  hold above exists for a real reason, not shallow-parallelism policy —
  this ticket's own design and `ENG-008`'s both extend the *same
  not-yet-created* handler file, and `ENG-008` is still `building` (not
  yet at `in-review`), so the conflict this hold was written to prevent
  hasn't actually been cleared yet. Proceeding anyway is the approver's
  call to make with fuller context than the board has; if `ENG-009`'s build
  hits that same file and finds `ENG-008`'s branch got there first, that is
  the expected shape of the risk, not a surprise — a rebase, not a bug. No
  other field changed; state stays `ready`, owner stays `eng-manager`.

- `2026-08-29` **approver reversal, same interactive session, minutes
  later.** New instruction: clear the `building`/`in-review` queue
  (`ENG-008`, `ENG-013`) before going to `ready` tickets — the opposite of
  the override just above. That override is superseded, not deleted (left
  intact above for the audit trail). `priority: next → ` (empty) — reverted
  to the original sequencing hold's own logic rather than left inconsistent
  with it, since a `next` priority would rank this ticket ahead of
  `ENG-008`/`ENG-013` (both unset) in any board-wide dispatch sweep, which
  is exactly backwards from this instruction. `traces/.pending` reordered
  by hand back to `continue ENG-008, continue ENG-013, continue ENG-009,
  continue ENG-010` — see that file and the matching entry on `ENG-010`.
  State stays `ready`, owner stays `eng-manager`; this ticket is once again
  simply waiting its turn behind `ENG-008`, which is where the original
  sequencing hold already had it.

- `2026-08-29` **`continue` event pass, context `ENG-009`** — the queue
  reaching this ticket's turn behind `ENG-008` and `ENG-013`, per the
  approver's hand-reordering above. Narrow scope per this event's own
  contract (resume this ticket from its current state; no board-wide
  sweep). Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh` (`ENG_ROOT` exported to
  the instance root), scoped (`ENG-009`) and whole-board: both exit 0,
  clean.

  **Re-checked the sequencing hold's own condition rather than assuming it
  still holds.** Read `ENG-008`'s own frontmatter directly rather than
  trusting the board's In-flight table: `state: building`. Its round-1 test
  gap was closed this same pass sequence (`aiorders-api@dc6972a`, per its
  own log) and it re-enters code review next, but it has not yet reached
  `in-review`. The condition this ticket is held on — `ENG-008` reaching
  `in-review` or later, both designs extending the same not-yet-created
  `admin-portal/handlers/influencers.ts` — is therefore still unmet.
  Checked `agents/eng-manager/inbox/`, `agents/product-manager/inbox/` and
  `inbox/` for anything newly filed against this ticket specifically — none
  found.

  **0 transitions.** State stays `ready`, owner stays `eng-manager`,
  `priority` stays empty. **Consequence:** machine WIP unaffected —
  verified fresh from each counted ticket's own `state:` field: `ENG-008`
  `building`, `ENG-009`/`ENG-010` `ready`, `ENG-013` `building` — still
  4/1, over the new cap, draining naturally per the board header's
  grandfather clause. Approver-facing WIP and approval cap both unaffected
  — no gate touched.

  **Dead-end sweep (scoped to this event):** nothing to resume — this is a
  deliberate wait with a re-verified condition, not a stall. **Notify
  sweep:** nothing to raise (no new gate item); nothing to nudge.

  `chained: none` — held for sequencing, unchanged: `ENG-008` has not yet
  reached `in-review`. Re-check once it does. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-009`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines. Also recorded on the
  board index (`_index.md`, matching dated entry; oldest of its three prior
  entries — `ENG-025` — rolled to `_index-archive.md` to make room, per the
  keep-three rule).

- `2026-08-29` **sequencing hold lifted — the condition this ticket has been
  waiting on is now met** (eng-manager, `scheduled` event pass, context
  `schtasks`, whole-board sweep). Re-checked `ENG-008`'s own frontmatter
  fresh rather than trusting the last `continue ENG-009` pass's finding:
  `state: in-qa`. Its round-2 code review + quality combined hop both
  passed earlier this same day (`building → in-review → in-qa` — see
  `ENG-008`'s own log). This ticket's hold condition — "re-check once
  `ENG-008` reaches `in-review` or later" — is therefore met: `in-qa` is
  later than `in-review`. `ENG-008`'s own chain (security next) is already
  correctly fired and recorded (`chained: ENG-008`) — not re-fired here, to
  avoid a second session racing the same ticket.

  **0 transitions.** State stays `ready`, owner stays `eng-manager` — the
  next transition (`ready → building`) needs an engineer actually writing
  code, this pass's stopping point by design (`eng_build_loop.md` step 6).
  **Consequence:** machine WIP unaffected — this ticket was already inside
  the counted range; lifting the hold changes what happens next, not the
  count.

  **Dead-end sweep:** this re-check, plus raising `ENG-016`/`ENG-017`'s G1s
  and correcting the board's stale "approval cap" framing, are this pass's
  whole-board findings — see `_index.md`'s dated entry for the full sweep.
  `ENG-010` remains correctly held (see its own log this same pass) — it is
  sequenced behind both `ENG-008` **and** this ticket, and this ticket has
  not built yet.

  `chained: ENG-009` — the hold that was suppressing the chain is lifted;
  `ready` is normally agent-owned and chains immediately once nothing else
  holds it. Fired
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-009`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-009`) and whole-board: see board index.

- `2026-08-30` `ready → building`: built per the design, both repos — staff
  social-figure editing (reused `followers`/`engagement` columns) and the
  derived internal activity signal (eng-manager, `continue` event pass,
  context `ENG-009`, this ticket's turn at the front of `traces/.pending`).
  Narrow scope per the event's own contract (resume this ticket from its
  current state; no board-wide sweep). Mode check clean (business-os `.env`
  → `MODE=` empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-009`) and
  whole-board: both exit 0, clean.

  **Both `_eng` worktrees existed, clean.** `aiorders-api` was sitting on
  `ENG-013`'s branch (its own build long finished, now at `in-qa`);
  `aiorders-admin-hub` was already sitting on `ENG-008`'s own branch
  (`f2ea36c`, matching that ticket's frontmatter exactly) — this ticket's
  own design explicitly assumes `ENG-008` has landed its handler and edit
  form, so branching from its tip rather than `origin/main` is required, not
  a convenience. `git fetch origin` on both confirmed no drift: `ENG-008`
  still at `dc6972a`/`f2ea36c`, `origin/main` unchanged. Branched
  `feat/ENG-009-influencer-engagement-info` off
  `origin/feat/ENG-008-influencer-admin-management` in `aiorders-api` and off
  the already-checked-out `ENG-008` tip in `aiorders-admin-hub` — neither
  branch operation disturbed `ENG-008`'s or `ENG-013`'s own branch refs,
  both remain fully intact and pushed.

  **Live schema re-verified before writing the migration**, per this
  instance's standing practice: Supabase MCP, read-only, project
  `bmnmnejwdxbcqinqkwko`. Confirmed `social_stats_updated_at`/
  `social_stats_platform` don't already exist, confirmed `followers`/
  `engagement`'s live types match what the handler validates, and confirmed
  via `list_migrations` that production's applied head is still
  `20260829190000` — neither `ENG-008`'s nor `ENG-013`'s migration has
  landed yet, so `20260830100000` was chosen to sort after both.

  **Built exactly what the design named, with one interface resolution the
  design couldn't have made itself.** The design's Interfaces section
  specifies extending "`GET /admin-portal/influencers`" to return an
  activity-augmented list — written against `ENG-008`'s own *design*, before
  `ENG-008` actually built. What `ENG-008` actually shipped is a **per-id**
  `GET /admin-portal/influencers/{id}` that the frontend never calls (the
  list itself is read directly via the anon Supabase client in
  `Influencers.tsx`'s `fetchData()`) — there is no list-shaped endpoint to
  extend. Resolved by adding a third route, `GET
  /admin-portal/influencers/activity` (checked in `handleInfluencers` ahead
  of the generic per-id match, since that regex would otherwise read the
  literal string "activity" as an id) returning one aggregate per
  influencer, fetched once by the frontend and merged client-side by id —
  same two-query-then-merge shape the design asked for, just split across
  the handler/frontend boundary differently than assumed. Same category of
  design-vs-shipped gap `ENG-008`'s own build hop hit on PUT-vs-PATCH; ran
  the step 6b artifact-enumeration grep before considering this build done
  (below) and found no other file in the department instructs or assumes
  the list-shaped form, so this is a local resolution, not a cross-file fix.

  **Both repos, exactly the components the design named:**
  `supabase/migrations/20260830100000_add_influencer_social_stats.sql`
  (two nullable columns, no backfill — see the migration doc); extended
  `admin-portal/handlers/influencers.ts` — `followers`/`engagement`/
  `social_stats_platform` added to `EDITABLE_FIELDS` and validated
  (`followers`: integer 0–1e9; `engagement`: number 0–100; `platform`:
  string ≤32 chars or null), `social_stats_updated_at` stamped server-side
  whenever either numeric field is written, new `getInfluencerActivity`
  (single unfiltered `SELECT` over `influencer_invitations`, grouped in
  memory into `{invitations, visits, completed_visits, responded,
  response_rate, last_activity_at}` per influencer — never one query per
  influencer, matching the design's own stated constraint); `index.ts`
  untouched (already routes `influencers` broadly). `src/pages/
  Influencers.tsx` — edit form gains followers/engagement/platform inputs,
  table gains an Activity column, dialog gains an Activity block plus
  `follower_count` shown as labelled read-only context, and the existing
  Followers/Engagement table cells and dialog fields now render "Not set"
  rather than a fabricated `0`/`0.0%` when `social_stats_updated_at` is
  null — exactly the behaviour the design's Data section specifies.
  `activityById` fetched independently of `fetchData()`'s own
  `Promise.all`, its own try/catch defaulting to `{}` on failure, so a
  broken activity endpoint degrades the activity column/block to "no
  activity data" without blanking the influencer list — the design's own
  named failure behaviour. `constants.ts` left untouched, matching `ENG-008`'s
  own established precedent of an inline fetch URL rather than a
  centralised endpoint constant for this same handler family.

  **One deliberate, minor deviation from the design's literal wording, flagged
  rather than silently taken.** The design says `social_stats_updated_at` is
  set "when either numeric field is present **and changed**." Implemented as
  "present" only — no existing field in this handler diffs an incoming value
  against the current row before writing (every other `EDITABLE_FIELDS`
  entry is a blind apply), and adding a fetch-then-compare for just these two
  fields would introduce a read-modify-write race none of the surrounding
  code has. Functionally near-equivalent for the design's own stated goal
  (an honest "is this stale" signal): a staff member re-submitting the same
  figure is still confirming it's current as of now, which is an honest
  thing for the timestamp to say. Covered by its own test
  (`does not stamp ... when neither social field is written`) proving the
  stamp is scoped to the two social fields, not "any field."

  **Artifact-enumeration grep (step 6b) run before closing out this hop.**
  Grepped `social_stats_updated_at`, `social_stats_platform`,
  `influencers/activity`, and `getInfluencerActivity` across
  `instances/`/`departments/`: only this ticket's own design doc and the
  migration doc just written this pass reference any of them — no
  *instruction* or *map* elsewhere in the department assumes a different
  shape, so nothing else needed fixing. Also re-confirmed
  `Access-Control-Allow-Methods` still agrees between `index.ts` and
  `influencers.ts` (both list `PATCH`, unchanged by this ticket) — the exact
  drift class `ENG-008`'s own build hop caught against this ticket's design
  doc, checked here in the other direction for the same reason.

  **Self-tested.** `aiorders-api`: `deno check` on the modified handler and
  test file — clean. `deno test influencers.test.ts` — **32 passed, 0
  failed** (17 pre-existing + 15 new: 8 rejection cases across
  followers/engagement/social_stats_platform, 4 stamping-behaviour cases,
  1 access + 2 aggregation cases for the new activity route). Whole-tree
  `deno check handlers/*.ts` — 17 errors, matching the exact count every
  prior ticket on this board has recorded, all in `auth.ts`/`partners.ts`/
  `users.ts`, none touched here; confirmed `influencers.ts` itself
  contributes zero. `aiorders-admin-hub`: `npm run lint` — 150 pre-existing
  errors (unchanged count), 31 warnings; grepped for `Influencers.tsx`
  specifically — the same one pre-existing `react-hooks/exhaustive-deps`
  warning every prior pass on this file recorded, zero new. `npm run build`
  — clean, same pre-existing chunk-size notice as every other ticket on this
  board.

  **Database migration doc written**
  (`agents/database/migrations/ENG-009-influencer-engagement-info.md`) —
  live re-verification of both new column names and the current applied
  migration head, rollback statement, the same not-dry-run gap every prior
  migration on this board carries forward, gate verdict **pass**.

  **Both branches committed and pushed**
  (`aiorders-api@4eb4b1b`, `aiorders-admin-hub@328db29`, both based on
  `ENG-008`'s still-unmerged tip); no PR opened yet — devops's release step,
  same as `ENG-008`. PR bodies drafted here:

  *aiorders-api* — title: `Add internal activity signal and staff-editable
  social stats for influencers (ENG-009)`. Body: two new nullable columns on
  `influencers` (`social_stats_updated_at`, `social_stats_platform`); reuses
  the existing, previously-unwritten `followers`/`engagement` columns for
  the staff-entered figure via `PATCH admin-portal/influencers/{id}`
  (extends `ENG-008`'s handler); new `GET admin-portal/influencers/activity`
  (admin/sub-admin gated, service-role client — `influencer_invitations` has
  no staff RLS policy) returns a per-influencer activity aggregate derived
  from invitation history, computed on read, stored nowhere. Depends on
  `ENG-008`'s branch (based off it, not `main`). Migration doc:
  `agents/database/migrations/ENG-009-influencer-engagement-info.md`.

  *aiorders-admin-hub* — title: `Add activity signal and social stats
  editing to influencer board (ENG-009)`. Body: extends `ENG-008`'s edit
  form and detail dialog with followers/engagement/platform fields; adds an
  Activity column to the table and an Activity block to the dialog, sourced
  from the new `aiorders-api` endpoint above; Followers/Engagement now show
  "Not set" instead of a misleading `0`/`0.0%` before staff enter a value.
  Depends on `ENG-008`'s branch (based off it, not `main`).

  **1 transition** (`ready → building`; the build itself happened inside
  it), well under the cap of 4 — the next hop (review + quality, combined)
  is a fresh session's work by design, same as every other ticket at this
  state on this board. **Consequence:** machine WIP unaffected — verified
  fresh from each ticket's own `state:` field: `ENG-008` `ready-to-ship`,
  `ENG-009` now `building`, `ENG-010` `ready`, `ENG-013` `in-qa` — still 4
  inside the counted `ready..ready-to-ship` range, unchanged by this pass
  (already inside it at `ready`; `building` is still inside it), draining
  naturally per the board header's grandfather clause. Approver-facing WIP
  and approval cap both unaffected — no gate touched this hop.

  **Dead-end sweep (scoped to this event):** no other ticket touched;
  `ENG-010` remains correctly held behind both `ENG-008` and this ticket
  (see its own log). **Notify sweep:** nothing raised this pass (no gate
  item written — a build hop doesn't notify). **Observation filed**
  (`observations.md`): the design-doc-vs-shipped-endpoint-shape gap above,
  as a second same-week data point (after `ENG-008`'s PUT/PATCH catch) that
  a design written against a sibling ticket's own *design* rather than its
  *shipped* code is a recurring, low-cost-to-catch class of drift on this
  board — worth considering whether the architect should re-read the actual
  diff, not just the design doc, when a ticket explicitly extends another.

  `chained: ENG-009` — ticket sits at `building`, agent-owned (the build
  itself is done; the next hop is code review + quality, combined, per this
  loop's own design for why that isn't done in the same session) — not the
  approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-009`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-009`) and whole-board: see board index.
<!-- merge note: remote said ENG-009 was still at ready on 2026-08-31, held by the machine-WIP cap, with the sequencing hold reason merely corrected. This contradicts the frontmatter both branches agree on (state: building, branch commits aiorders-api@4eb4b1b / aiorders-admin-hub@328db29) and local's own detailed 2026-08-30 building entry above. Kept local's account (the build genuinely happened) and dropped remote's stale ready/held entry as superseded. -->

- `2026-09-02` **broken chain found and resumed — the 2026-08-30 `chained:
  ENG-009` fire never actually landed a session, and a later pass's
  mistaken "fix" masked it for ~28 hours** (eng-manager, `scheduled` event
  pass, context `launchd` — whole-board sweep). Mode check clean
  (`MODE=active`). Pre-pass `eng-gate-check.sh`, whole-board: exit 0, clean.

  **What was found.** This ticket's own frontmatter has read `state:
  building` continuously since commit `3881cc2` (2026-09-01 08:45:35 -0700,
  "sync local sweep/board state before pulling remote history") and was
  explicitly kept over a rival `ready` account by the cross-host merge
  `e281c71` the same morning (see this file's own merge note directly
  above) — `git log -p` on this file and `git show <rev>:<path>` at each of
  `29af8f2`, `db8bf41`, `3881cc2`, `e281c71`, and `HEAD` confirm `state:
  building` and this ticket's full 2026-08-30 build log entry arrived
  together in `3881cc2` and have been unchanged since. Despite that, the
  09-01 09:30 `scheduled` pass's own session log
  (`traces/eng-loop-2026-09-01.log:462-493`) recorded reading this ticket's
  file as `state: ready` and "corrected" the board index's In-flight row
  from `building` to `ready` on that basis — the row this pass just found
  and reverted. That 09:30 pass's premise was wrong: nothing in this
  ticket's git history ever set `state: ready` after `29af8f2`
  (2026-08-29). The misread, not the ticket file, was stale. Every pass
  since (five, by commit count) then read the *board index* rather than
  this file and concluded "`ENG-009`/`ENG-010` both sit at `ready`,
  WIP-capped, nothing to dispatch" — technically true of the cap math
  (both tickets are inside the counted range regardless of which exact
  state) but wrong about what was actually being held: this ticket was not
  waiting on the WIP cap, it was waiting on a chain nobody re-fired,
  because nobody re-fired.

  **Why the chain never landed — investigated, not fully resolved.**
  `traces/eng-loop-2026-08-30.log` contains zero mentions of `ENG-009` —
  no `pass start`, no queue line — despite the ticket's own log recording
  `chained: ENG-009` and a literal `eng-trigger.sh continue ENG-009`
  invocation that same day. `traces/.pending` is empty now and no
  `traces/.hops-*-ENG-009` file exists on this host, meaning this host has
  never charged this ticket a hop. The build log's own commit
  (`3881cc2`, "sync local... before pulling remote history") reads as
  locally-committed work later synced in, consistent with the fire having
  happened on the other host (Windows — this instance's `traces/` is
  host-local and `.gitignore`d there, per
  `inbox/2026-08-31-eng-events-dropped.md`'s own same finding). Cannot
  root-cause further from this host, same limitation that incident already
  named. What's checked and certain, not inferred: `links.review` and
  `links.test_plan` are both still blank in this ticket's own frontmatter,
  and `state` is still `building` — wherever the fire went, the review +
  quality hop it should have triggered never ran, on either host.

  **Verified safe to resume before doing so.** `git fetch origin` on both
  worktrees: `aiorders-api@4eb4b1b` and `aiorders-admin-hub@328db29` both
  still resolve on `origin` — neither branch was deleted or rewritten.
  `business-os` itself: `git fetch origin` then `git log HEAD..origin/main`
  — empty; this host is ahead of, not behind, `origin/main`, so there is no
  newer remote board state this pass is missing.

  **Board index corrected** (`board/_index.md`): In-flight row `ready` →
  `building`, updated date bumped to today; header narrative corrected to
  stop citing the wrong state as fact, with a pointer to this entry rather
  than a re-derivation.

  **0 transitions on this ticket's own state** — this pass restores the
  record, it does not itself perform the review + quality hop (that stays
  a fresh session's work, same as every other ticket at this state on this
  board). `ENG-010` is unaffected: its own hold reason (machine WIP 2/1,
  over cap) is unchanged by this correction, since `ENG-009` was already
  inside the counted `ready`..`ready-to-ship` range either way.

  **Proposal filed** (`proposals.md`): nothing in `eng-gate-check.sh` or
  any board-update step cross-checks `board/_index.md`'s In-flight `state`
  column against each ticket's own frontmatter `state:` — this is the
  second time that specific gap has produced a real miss (after `ENG-016`'s
  G1 missing from the same table), and this one cost the ticket roughly a
  day and a half of wall-clock time sitting on a dead chain no pass
  thought to check.

  `chained: ENG-009` — sits at `building`, agent-owned (`eng-manager`), not
  the approver, not blocked, not terminal, not held by a cap (already
  inside the counted range). Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-009`
  before exiting, per this schedule's own macOS EPERM note. Post-pass
  `eng-gate-check.sh`, whole-board: see board index.

- `2026-09-02` **code review round 1: FAIL — this branch still carries a bug
  `ENG-008` already found and fixed on its own branch, because `ENG-009`
  forked before the fix landed and was never rebased** (principal-engineer,
  `continue` event pass, context `ENG-009` — the chain fired by the 09:30
  `scheduled` sweep above). Narrow scope per the event's own contract
  (resume this ticket only; no board-wide sweep). Mode check clean
  (business-os `.env` → `MODE=active`; instance `config/config.yaml` →
  `mode:` empty, falls through). Pre-pass `eng-gate-check.sh`, scoped
  (`ENG-009`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

  **Re-derived both diffs from disk.** Both worktrees fetched and checked
  out onto this ticket's branch, confirmed clean, at the exact commits this
  ticket's own frontmatter records (`aiorders-api@4eb4b1b`,
  `aiorders-admin-hub@328db29`). Reviewed the isolated single-commit patch
  on each branch (`git show {commit}`) rather than the two-dot diff against
  `origin/main`, which is polluted by `ENG-008`'s own still-unmerged commits
  underneath plus real main-drift (`ENG-007`/`ENG-011`) — same reasoning
  `ENG-008`'s own round-1 review already used at this identical point.

  **The finding that fails this round, found by checking this ticket's
  branch point against its own acknowledged dependency, not just against
  `main`.** Both designs and both tickets' logs are explicit that `ENG-009`
  builds on top of `ENG-008`'s branch, not `main` — correct at build time
  (2026-08-30 01:39), but `ENG-008` has moved twice since, fixing a real
  bug on each repo (2026-08-31, see `ENG-008`'s own log), and `ENG-009`'s
  branch was never updated to track it:

  - `git merge-base --is-ancestor 57f8c4b feat/ENG-009-...` (`aiorders-api`)
    → **not an ancestor.** `ENG-009`'s branch point is `dc6972a`, one commit
    before `ENG-008`'s fix (`57f8c4b`). Confirmed directly in the working
    tree: `hasInfluencerAdminAccess` (`influencers.ts:27-33`) still reads
    unguarded `userProfile.role`/`userProfile.additional_roles`, not the
    optional-chained `userProfile?.role` `ENG-008`'s round-2 review put
    there — and the missing-profile test plus the field-allowlist test that
    fix added are both absent from `ENG-009`'s copy of the test file.
    Checked whether this is live risk, same as `ENG-008`'s own round-2
    review already did for this exact line: `admin-portal/index.ts` 401s on
    no user and 403s on no `profiles` row before any handler runs, so this
    specific gap is defensive-only, not exploitable today — lower severity,
    named below, not the reason this round fails.
  - `git merge-base --is-ancestor 63be255 feat/ENG-009-...`
    (`aiorders-admin-hub`) → **not an ancestor.** `ENG-009`'s branch point is
    `f2ea36c`, `ENG-008`'s *original* build, one commit before its own
    round-1 fix (`63be255`). Confirmed directly in the working tree,
    `Influencers.tsx:139-140`:
    ```
    accepts_paid: influencer.accepts_paid ?? !influencer.barter_visit,
    accepts_barter: influencer.accepts_barter ?? !!influencer.barter_visit,
    ```
    **This is the exact null-coalescing bug `ENG-008`'s own round-1 review
    found and round-1-fix removed** — `!null === true` in JS, so opening
    the edit dialog on any of the 51/306 influencers with a genuinely unset
    preference computes `accepts_paid: true, accepts_barter: false` as if
    known. `Influencers.tsx:194-195` still sends both fields unconditionally
    on every save (`ENG-008`'s fix made this conditional, omitting either
    while still `null`), so saving *any* unrelated field on one of those 51
    rows still silently writes a fabricated preference. Every symptom
    `ENG-008`'s round-1 review described reproduces verbatim on this
    branch, because this branch is textually the pre-fix version of the
    file `ENG-008` was reviewing that day.

  **Why this wasn't caught at the 2026-08-30 build hop:** it couldn't have
  been — `ENG-008`'s fix (`57f8c4b`/`63be255`) landed 2026-08-31, the day
  *after* `ENG-009` branched and built. This is a staleness gap that opened
  up after the build, sitting uncaught through every `scheduled`/`watch`
  sweep since because none of them diff a ticket's branch against a
  sibling it was cut from — they check `git fetch` + ancestry against
  `origin/main` for merge detection, which this ticket doesn't reach yet,
  and against nothing else. First time this specific check has been run on
  this board. Proposal filed below.

  **Why this blocks rather than just getting named as a carry-forward
  gap**, unlike row 5's unbounded-query finding further down: that one is a
  judgement call on a query this ticket wrote, accepted on real precedent.
  This one is a *known, already-fixed, already-described* correctness bug
  that would ship if this branch went out as-is — passing it and leaving
  the rebase to whoever opens the PR is exactly "passing under time
  pressure," the failure mode `code-review-gate/SKILL.md` names first.

  **A real complication for whoever fixes this, named now rather than
  discovered mid-fix:** `ENG-008`'s fix and `ENG-009`'s own diff both touch
  the same object literal in `handleSaveInfluencer` — `ENG-008`'s fix
  converts `accepts_paid`/`accepts_barter` from unconditional literal
  entries to conditional (`if (... !== null) body.x = ...`) omissions;
  `ENG-009` adds `social_stats_platform: ...` as a new literal entry in
  that same block. Rebasing/merging this is not a clean auto-resolve on
  that hunk; whoever does it needs to apply *both* changes by hand, not
  pick a side.

  **Automatic-failure scan** (recorded here; no receipt on a fail —
  `code-review-gate/SKILL.md` step 8):

  | # | Check | Result |
  |---|---|---|
  | 1 | Secret/credential/token/key | Clean |
  | 2 | Silent exception swallow | Clean — new backend/frontend catches all log before returning/degrading |
  | 3 | Missing test on a bug fix | N/a, feature ticket |
  | 4 | Untyped public interface, undocumented | Clean, nothing new introduced |
  | 5 | Unbounded query / missing pagination | **Real hit, reviewed and accepted, not the reason this round fails.** `getInfluencerActivity`'s `influencer_invitations` read carries no `.limit()`. Same class this board has already accepted three times (`ENG-006`'s `customers` lookup, `ENG-007`'s rate-history query, `ENG-011`'s `getAllBrands`): cardinality bounded by a real constraint (809 rows/138 influencers today, internal-only admin surface), and the architect's own design explicitly evaluated and rejected a scheduled/cached alternative at this volume. Flagged, not silently passed |
  | 6 | New dependency | Clean |
  | 7 | Unrelated refactor bundled in | Clean |
  | 8 | Commented-out code / unowned `TODO` | Clean |
  | 9 | Datastore write bypassing the data layer | N/a, same house style as every prior ticket |
  | 10 | Auth/payment/deletion path changed, no failure-case test | Clean on `ENG-009`'s own new route (`GET /influencers/activity` has a dedicated 403 test) |

  **Also found this round, secondary, would not have blocked alone:**
  - The architect's design doc (`Interfaces` section) still says
    `PUT`/body-`id`; the shipped code correctly uses `PATCH`/path-`id`,
    matching `ENG-008`'s own resolution of the identical fork. Code is
    right, design doc is stale, and neither ticket's log ever corrected the
    doc itself — not this review's file to edit, named so it isn't read at
    face value.
  - Setting `social_stats_platform` alone (no `followers`/`engagement`)
    persists successfully but never renders anywhere — the dialog's
    platform/updated-date line is gated on `social_stats_updated_at`, which
    only a numeric write sets. P3, has a workaround (enter a number too,
    the intended flow), not in any AC.
  - `getInfluencerActivity`'s `response_rate: invitations === 0 ? null : …`
    branch is unreachable by construction (an entry only exists after its
    first row already incremented `invitations`). Harmless, style-only.
  - Two of the four new stamping tests assert `social_stats_updated_at` was
    captured but not that `captured.followers`/`captured.engagement`
    themselves carry the submitted value. Low severity.

  Findings logged here in full (this board has no
  `agents/principal-engineer/notebook/` entry pattern that would duplicate
  this rather than summarize it — see that directory's 2026-09-02 entry for
  the summary form).

  **No receipt written** (`agents/principal-engineer/reviews/ENG-009.md`
  stays absent) and **QA's hop not run this round** — discarded per the
  combined-hop design, same as every prior round-1 fail on this board;
  no `agents/qa/test-plans/ENG-009.md` written either.

  **Proposal filed** (`proposals.md`): code review's own inputs/steps
  (`skills/code-review-gate/SKILL.md`) check a ticket's diff against
  `main` and against its design, but nothing asks whether a ticket's
  branch is stale relative to a *sibling* ticket it was deliberately
  sequenced/branched behind — the exact gap that let this sit unnoticed
  for two days across four sweep passes. First occurrence on this board,
  not (yet) a pattern; logged as a proposal rather than fixed inline, per
  `eng_build_loop.md` step 3.

  **0 net transitions** — `state`/`owner` unchanged (`building`/
  `eng-manager`), same precedent `ENG-008`'s own round-1 fail set: a review
  failure routes back to `building` without a persisted `in-review`
  frontmatter state. `machine_wip` unaffected. No approver-facing or
  approval-cap change — a review failure is not an approver-facing gate.
  `time_remaining` updated in frontmatter to name the rebase-and-refix work
  plus round 2, in the same edit as this entry, per
  `definition-of-done.md`'s time-tracking rule.

  **Dead-end sweep (scoped to this event):** nothing else on this ticket's
  own lineage to resume — this finding *is* this pass's dead-end-sweep
  result. **Notify sweep:** nothing to raise (a review failure isn't a
  gate item to the approver).

  `chained: ENG-009` — `building` is agent-owned (the rebase-and-refix
  above is the next hop's work), not the approver, not blocked, not
  terminal, not held by a cap. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-009`
  before exiting. Post-pass `eng-gate-check.sh`, scoped (`ENG-009`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines.

- `2026-09-02` **rebase-and-refix hop — the work round 1 named, done** (the
  fixing engineer, `continue` event pass, context `ENG-009` — the chain fired
  by the round-1-FAIL pass above). Narrow scope per this event's own contract
  (this ticket only; no board-wide sweep). Mode check clean (business-os
  `.env` → `MODE=active`). Pre-pass `eng-gate-check.sh`, scoped (`ENG-009`)
  and whole-board: both exit 0, clean, no `WAIVED:` lines. Ticket hop count
  (`traces/.hops-2026-09-02-ENG-009`) at 2 coming in, well inside the
  `max_5x` tier's 20/ticket ceiling.

  **Both worktrees fetched and re-confirmed against round 1's own findings
  before touching anything**, rather than trusted from the log above:
  `git merge-base --is-ancestor` repeated fresh on both repos, both still
  **not an ancestor** (`aiorders-api`: branch point `dc6972a`, one commit
  behind `origin/feat/ENG-008-influencer-admin-management`'s `57f8c4b`;
  `aiorders-admin-hub`: branch point `f2ea36c`, one behind `63be255`) — the
  gap round 1 found was still open, not something a later pass had already
  closed.

  **`aiorders-api`: `git rebase origin/feat/ENG-008-influencer-admin-management`.**
  `influencers.ts` itself — the file carrying the actual bug round 1
  named — auto-merged cleanly: ENG-009's diff only adds new `EDITABLE_FIELDS`
  entries and a new const above `hasInfluencerAdminAccess`, never touches the
  function body ENG-008's fix changed, so the optional-chaining fix
  (`userProfile?.role`) carried through untouched. `influencers.test.ts` did
  conflict — a real one, not spurious: both commits append an independent
  `Deno.test`/helper block immediately after the same last pre-existing test
  (`"...returns the updated row on success"`), and the two blocks share
  near-identical mock-Supabase-client boilerplate (`adminSupabase: { from()
  { return { update(patch) { ...select... Promise.resolve(...) } } } } as
  unknown as AuthenticatedRequest`), which the line-based merge interleaved
  as four nested conflict markers rather than two clean sequential
  insertions. Resolved by reconstructing both blocks whole and in sequence
  (ENG-008's "allowlist enforcement" test first, since it's the earlier
  commit, then ENG-009's `adminAuthCapturing` helper and all five tests that
  use it) rather than editing markers in place — checked against each
  commit's own `git show` output directly to avoid transcribing either side
  from memory. Observation filed (`observations.md`) — this conflict shape
  (independent additions colliding on shared boilerplate, not on shared
  logic) is worth naming since it's the opposite of what round 1's own
  "not a clean auto-resolve" framing predicted for the *other* repo, and
  code review's current checks wouldn't catch it either way.

  **`aiorders-admin-hub`: same rebase command.** The hunk round 1 explicitly
  flagged as needing hand-resolution (`handleSaveInfluencer`'s returned
  `body` literal — ENG-008 deletes the `accepts_paid`/`accepts_barter`
  literal entries in favor of conditional `if` assignments, ENG-009 inserts
  `social_stats_platform` as a new literal entry in the same object) in fact
  auto-merged with **zero conflicts** via git's default `ort` three-way
  strategy. Not trusted on the strategy's silence alone: read the resulting
  `handleSaveInfluencer` body, the `openInfluencer` prefill block, and both
  the `Influencer`/`InfluencerEditForm` interfaces directly afterward, plus
  grepped for the specific `?? false` checkbox guards and the `<Button>`
  cosmetic revert round 1's own diff named — every one of ENG-008's fix
  lines and every one of ENG-009's additions is present, correctly combined,
  nothing silently dropped from either side. Second half of the same
  observation above.

  **Re-verified both repos after resolving, not assumed from the merge
  succeeding.** `aiorders-api`: `deno` was not installed on this host at
  all (not on `PATH`, no `~/.deno`) — installed via `brew install deno`
  (2.9.6) before running anything, a local dev-tool install, not a change to
  anything shared. `deno check` on the modified handler and test file —
  clean. `deno test influencers.test.ts` — **34 passed, 0 failed** (the
  prior 32 plus the 2 tests ENG-008's own fix commit added — missing-profile
  rejection, allowlist-enforcement — both now present since the rebase
  carried that commit in). Whole-tree `deno check handlers/*.ts` — still
  exactly 17 errors, all in `auth.ts`/`partners.ts`/`users.ts`, zero
  attributable to `influencers.ts`/`influencers.test.ts` (confirmed by
  grepping the check output directly rather than trusting the count alone).
  `aiorders-admin-hub`: `npm run lint` — 150 pre-existing errors (unchanged),
  31 warnings, `Influencers.tsx` carrying only the same one pre-existing
  `react-hooks/exhaustive-deps` warning every prior pass on this file
  recorded. `npm run build` — clean, same pre-existing chunk-size notice as
  every other ticket on this board.

  **No new artifact or cross-file rule introduced this hop** — step 6b's
  enumeration grep is for a change that writes or relies on a rule about an
  artifact (a receipt path, a state name, a config key); this hop only
  brought two already-shipped files back in sync with each other, so there
  is nothing new to enumerate. The original build hop already ran 6b for
  everything this ticket itself introduces.

  **Both branches force-pushed** (`--force-with-lease`, since the rebase
  rewrote each branch's history) — `aiorders-api@d37e0c9`,
  `aiorders-admin-hub@92bcacd`, both still based on `ENG-008`'s (now current)
  tip. No PR open yet on either repo — unchanged from before this hop, still
  devops's release step. `time_spent`/`time_remaining` updated in
  frontmatter in the same edit as this entry, per
  `definition-of-done.md`'s time-tracking rule.

  **0 net transitions** — `state`/`owner` unchanged (`building`/
  `eng-manager`); the next transition (`building → in-review`) is the
  review + quality hop's own write, not this one's. `machine_wip`
  unaffected. No approver-facing or approval-cap change.

  **Dead-end sweep (scoped to this event):** nothing else on this ticket's
  own lineage to resume — the rebase-and-refix round 1 asked for is this
  pass's entire result. **Notify sweep:** nothing to raise (a build hop
  doesn't notify); nothing to nudge.

  `chained: ENG-009` — `building` is agent-owned (review + quality round 2
  is the next hop's work), not the approver, not blocked, not terminal, not
  held by a cap. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-009`
  before exiting. Post-pass `eng-gate-check.sh`, scoped (`ENG-009`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines.

- `2026-09-02` **code review round 2: PASS, plus the quality gate — now
  in-qa** (principal-engineer then qa, `continue` event pass, context
  `ENG-009` — the chain fired by the rebase-and-refix hop above). Narrow
  scope per the event's own contract (resume this ticket only; no
  board-wide sweep). Mode check clean (business-os `.env` → `MODE=active`).
  Pre-pass `eng-gate-check.sh`, scoped (`ENG-009`) and whole-board: both
  exit 0, clean, no `WAIVED:` lines. Ticket hop count
  (`traces/.hops-2026-09-02-ENG-009`) at 3 coming in, well inside the
  `max_5x` tier's 20/ticket ceiling.

  **Re-derived both diffs from disk rather than trusting round 1's or the
  rebase hop's own account.** Both worktrees fetched, confirmed clean, at
  the recorded commits (`aiorders-api@d37e0c9`, `aiorders-admin-hub@92bcacd`).
  `git merge-base --is-ancestor` re-run fresh on both fix commits
  (`57f8c4b`, `63be255`) against this branch's tip — both now **true**,
  reversing round 1's finding. `git merge-base origin/feat/ENG-008-...
  {this-branch}` on each repo returns exactly `ENG-008`'s own tip, meaning
  this branch forks cleanly off `ENG-008`'s current head with zero
  divergence — the rebase did what it claimed.

  **Both merge outcomes read in full, not trusted from the rebase's exit
  code.** `aiorders-api`'s hand-resolved test-file conflict: read all 380
  lines of `influencers.test.ts` — `ENG-008`'s two closing-round tests and
  every one of `ENG-009`'s own are present exactly once, correctly
  sequenced, no duplication. `aiorders-admin-hub`'s zero-conflict
  auto-merge: read `handleSaveInfluencer` in full — `ENG-008`'s conditional
  `accepts_paid`/`accepts_barter` omission and `ENG-009`'s unconditional
  `social_stats_platform` entry are both present and correctly combined in
  the same object literal.

  **Automatic-failure scan: 0/10 open**, re-run fresh against the
  post-rebase diff. One accepted precedent unchanged from round 1
  (`getInfluencerActivity`'s unbounded query — 4th occurrence of this
  exact class on this board, cardinality-bounded, architect-evaluated).

  **Verification independently reproduced, not taken on the rebase hop's
  word:** `deno check` on both changed files — clean. `deno test
  influencers.test.ts` — **34 passed, 0 failed**, actually executed
  (`deno` 2.9.6, installed on this host during the rebase hop) — first
  ticket on this board where `aiorders-api`'s suite runs rather than being
  hand-traced. `npm run lint` (`aiorders-admin-hub`) — 150 errors/31
  warnings, unchanged baseline, `Influencers.tsx` carrying its one
  pre-existing warning, zero new. `npm run build` — clean, 3340 modules,
  same pre-existing chunk-size notice. Checked one incidental question
  this round raised — whether `fetchActivity`'s `supabase.supabaseUrl`
  usage was a novel, untested client-API surface — via `git log
  -S"supabase.supabaseUrl"`: `ENG-008`'s own build introduced this pattern
  first, `ENG-009` reuses it verbatim.

  **Quality gate (QA): test plan written**,
  `agents/qa/test-plans/ENG-009.md` — all 4 acceptance criteria covered
  (executed Deno.test cases for AC1/2/4, shared-mechanism inspection for
  AC3, matching AC5/6's precedent on `ENG-008`'s own plan). No open P0/P1
  bug anywhere on this board (`agents/qa/bugs/` empty).

  **Receipts written:** `agents/principal-engineer/reviews/ENG-009.md`
  (verdict `pass`, round 2), `agents/qa/test-plans/ENG-009.md`.
  `links.review`/`links.test_plan` set on this ticket in the same edit as
  this entry. `time_spent`/`time_remaining` updated in frontmatter per
  `definition-of-done.md`'s time-tracking rule.

  **Named, non-blocking gaps** (full detail in the review receipt): the new
  activity endpoint's 500 path is untested (same standing gap this file's
  other two endpoints already carry); the defensive `if (!id) continue`
  branch in `getInfluencerActivity` is untested against data the live
  schema doesn't currently produce; `index.ts`'s 404 `availableRoutes` hint
  list doesn't name the new route (cosmetic, pre-existing incompleteness,
  never consulted by the router itself). None block this round.

  **2 transitions** (`building → in-review → in-qa`), well under the cap
  of 4 — stopped deliberately, not by the cap: security is a separate hop
  by design, needs this pass's own just-written test plan, and
  `eng_build_loop.md` calls for a fresh session there. `machine_wip`
  unaffected (`ENG-009` stays inside the counted `ready`..`ready-to-ship`
  range). Approver-facing WIP and approval cap both unaffected — no gate
  raised this pass.

  **Dead-end sweep (scoped to this event):** nothing else on this ticket's
  own lineage to resume. **Notify sweep:** nothing to raise (a review/
  quality pass isn't a gate item to the approver).

  `chained: ENG-009` — `in-qa` is agent-owned (security next, fresh
  session — needs this pass's own test plan), not the approver, not
  blocked, not terminal, not held by a cap. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-009`
  before exiting. Post-pass `eng-gate-check.sh`, scoped (`ENG-009`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines.

- `2026-09-02` **security gate: PASS — now `ready-to-ship`** (security,
  `continue` event pass, context `ENG-009` — the chain fired by the
  round-2-PASS pass above). Narrow scope per the event's own contract
  (resume this ticket only; no board-wide sweep). Mode check clean
  (business-os `.env` → `MODE=active`). Pre-pass `eng-gate-check.sh`,
  scoped (`ENG-009`) and whole-board: both exit 0, clean.

  **Re-derived both diffs from disk rather than trusting the review's own
  account.** Both worktrees fetched, confirmed clean, at the recorded
  commits (`aiorders-api@d37e0c9`, `aiorders-admin-hub@92bcacd`).
  `git merge-base --is-ancestor 57f8c4b/63be255 HEAD` re-run fresh on both
  — both **true**, matching round 2's own finding. Read both isolated
  commits (`git show`) in full, plus the current file state of
  `hasInfluencerAdminAccess` and `handleSaveInfluencer`'s merged body
  directly, rather than taking the code-review receipt's word for what
  survived the rebase.

  **Threat-modelled the change** (4 questions, full detail in the
  receipt): the new route and the three new writable fields sit behind
  the exact same single gate every pre-existing field already sits
  behind — confirmed by reading `handleInfluencers` line-by-line, not
  assumed from the design doc. No new data-classification tier: the
  activity aggregate carries counts/dates only, no PII; `social_stats_platform`
  is a staff-typed label rendered through a plain (auto-escaped) JSX text
  node, not an injection sink.

  **Negative-auth cases independently re-verified**, including one
  re-run specific to the new route: `deno test` executed fresh this pass
  (not taken from the prior hop's log) — **34 passed, 0 failed**, and
  `handleInfluencers GET activity rejects a non-admin caller with 403`
  (a throwing-`Proxy` `adminSupabase`, mutation-sensitive, not a shape
  check) passed individually. `hasInfluencerAdminAccess rejects a
  missing profile` and `PATCH strips fields outside the editable
  allowlist before writing` — both `ENG-008`'s own closing-round
  regression tests — independently grepped present and green, not
  inferred from round 2's receipt. `deno check` on both changed files:
  clean.

  **OWASP A01–A10 walked**, each marked applicable or `n/a` with a
  reason; full table in the receipt. Nothing blocking.

  **One finding, non-blocking, and it is this gate's third occurrence of
  the same class — the three-strike rule fires.** `getInfluencerActivity`'s
  catch block returns raw `error.message` in a 500 body, same shape
  `ENG-013` (1st) and `ENG-008` (2nd) already carried in this exact file
  family; this is the 3rd gate-reviewed occurrence. Disposition unchanged
  from the first two (role-gated, copies rather than introduces the
  pattern) — **not** a reason to fail this round. Per
  `skills/security-gate/SKILL.md` step 10, logged
  (`agents/security/notebook/2026-09-02-findings.md`) and **proposed** to
  `principal-engineer` — who owns `engineering-standards.md`, not this
  agent —
  in `agents/principal-engineer/notebook/2026-09-02-security-proposal-verbose-error-response.md`.
  Proposal only; the standards file itself is untouched by this pass.

  **Secrets**: both isolated commits scanned in full (the only two
  commits added since `ENG-008`'s own security review already scanned
  every ancestor) for key/token/password/PEM/service-role patterns — no
  leaked credential, two benign matches (a code comment, the forwarded
  user session token, same pattern already cleared on `ENG-008`).
  **Dependencies**: none new on either repo — confirmed by re-reading
  both diff stats (3 files/1 file, no `package.json`/`deno.json`/lockfile
  among them). **LLM checklist**: n/a, design frontmatter confirms
  `touches_models: false`, matches both diffs.

  **SOC 2 evidence trail checked complete**: ticket → PRD → design →
  migration review (pass) → code review (round 2, pass) → QA (pass) →
  this verdict → release record (pending). No gap.

  **Receipt written**: `agents/security/reviews/ENG-009.md` (verdict
  `pass`). `links.security_review` set on this ticket in the same write.
  `time_spent`/`time_remaining` updated in frontmatter in the same edit
  as this entry — only release-readiness (opening the PRs) remains.

  **1 transition** (`in-qa → ready-to-ship`), well under the cap of 4 —
  same precedent `ENG-008`'s own security-gate pass set (the gate's own
  `in-security` state is not persisted to frontmatter on a pass; SKILL.md
  step 9 writes `ready-to-ship` directly). **Consequence:** `machine_wip`
  unaffected — `ENG-009` stays inside the counted `ready`..`ready-to-ship`
  range, `in-qa` and `ready-to-ship` both counted. No approver-facing or
  approval-cap change — a security-gate pass isn't a gate item to the
  approver, and `owner` moving to `devops` is an agent-to-agent handoff,
  not a human wait.

  **Dead-end sweep (scoped to this event):** nothing else on this
  ticket's own lineage to resume. **Notify sweep:** nothing to raise (a
  security pass isn't a gate item to the approver); nothing to nudge.
  **Observations/proposals filed:** the three-strike standards proposal
  above is the only new one this pass — the frontend-test-harness
  proposal and the unbounded-`influencer_invitations`-query precedent are
  both already tracked elsewhere and unchanged by this pass.

  `chained: ENG-009` — `ready-to-ship` is agent-owned (devops's
  release-readiness hop next: open the PR), not the approver, not
  blocked, not terminal, not held by a cap (still inside the same counted
  machine-WIP range this ticket already occupied). Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-009`
  before exiting. Post-pass `eng-gate-check.sh`, scoped (`ENG-009`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines.

- `2026-09-02` **release-readiness: both PRs opened, now `blocked` on the
  approver** (devops, `continue` event pass, context `ENG-009` — the chain
  fired by the security-gate-PASS pass above). Narrow scope per the event's
  own contract (resume this ticket only; no board-wide sweep). Mode check
  clean (business-os `.env` → `MODE=active`; instance `config/config.yaml`
  → `mode:` empty, falls through). Pre-pass `eng-gate-check.sh`, scoped
  (`ENG-009`) and whole-board: both exit 0, clean, no `WAIVED:` lines.
  Ticket hop count (`traces/.hops-2026-09-02-ENG-009`) at 5 coming in, well
  inside the `max_5x` tier's 20/ticket ceiling.

  **Read `skills/release-runner/SKILL.md` fresh before acting, same
  discipline `ENG-013`'s own equivalent hop used.** Step 1's window check
  doesn't apply — both `aiorders-api` and `aiorders-admin-hub` are
  registered **L1** (`config/projects.md`) — so went straight to step 4.

  **Verified all four upstream gates fresh from the receipt files
  themselves**, not from this ticket's own log summary: migration doc
  (**pass**), `agents/principal-engineer/reviews/ENG-009.md` (**pass**,
  round 2), `agents/qa/test-plans/ENG-009.md` (present, all 4 ACs
  covered), `agents/security/reviews/ENG-009.md` (**pass**). All four
  opened and read, not just grepped for a verdict line.

  **Worktrees clean, on this ticket's own branch already** — unlike
  `ENG-013`'s equivalent hop, neither worktree needed a checkout switch
  coming in; both `~/Documents/projects/_eng/{aiorders-api,
  aiorders-admin-hub}` were already sitting on
  `feat/ENG-009-influencer-engagement-info` at the exact commits this
  ticket's frontmatter records (`d37e0c9`, `92bcacd`), confirmed via
  `git fetch` + `git status --short --branch` on both. Checked for an
  already-opened PR before creating one, same caution `ENG-011`/`ENG-013`
  used: `gh pr list --head feat/ENG-009-influencer-engagement-info
  --state all` on both repos — empty on both. None existed.

  **The real judgment call this hop made, not covered word-for-word by
  the skill: which branch to open the PR against.** This ticket's own
  branch is built on top of `ENG-008`'s branch, not `main` — `git
  merge-base --is-ancestor` confirms `ENG-008`'s current tip
  (`57f8c4b`/`63be255`) is an ancestor of this branch on both repos, and
  the build-hop's own PR-body draft from 2026-08-30 already flagged this
  explicitly ("Depends on ENG-008's branch (based off it, not main)").
  `ENG-008` is still `blocked`/`blocked_on: approver`, its own two PRs
  (`aiorders-api#6`, `aiorders-admin-hub#5`) still open and unmerged —
  confirmed fresh via `gh pr view` on both before deciding anything, not
  assumed from the board. Opening this ticket's PRs against `main` as
  usual would have pulled `ENG-008`'s three still-unreviewed-by-GitHub
  commits into this diff as well, duplicating a PR already open and
  awaiting merge, and would let merging *this* PR alone silently carry
  `ENG-008`'s changes into `main` too. Opened both PRs with
  `--base feat/ENG-008-influencer-admin-management` instead — confirmed
  by diffing this ticket's branch against that base directly before
  creating anything (`aiorders-api`: 3 files, 314 insertions only;
  `aiorders-admin-hub`: 1 file, 196 insertions/10 deletions only) that
  this produces exactly ENG-009's own change and nothing of ENG-008's.

  **Opened both PRs** (`gh pr create`): `aiorders-api`
  https://github.com/harsimranwalia/aiorders-api/pull/7,
  `aiorders-admin-hub`
  https://github.com/harsimranwalia/aiorders-admin-hub/pull/6. Verified
  both via `gh pr view` immediately after (`baseRefName`/`headRefName`/
  `state`) rather than trusting the create command's own stdout. Each PR
  body states what it does, the base-branch sequencing choice and both
  ways to resolve it, all four gate verdicts by file reference, and the
  named non-blocking gaps carried forward from review/security. Neither
  worktree left dirty; both still sit cleanly on this ticket's own branch
  (no other ticket had a claim on either worktree this pass, so no
  restore-after step was needed, unlike `ENG-013`'s hop).

  **Wrote the L1 merge-request item**
  (`inbox/2026-09-02-eng009-merge-request.md`, `gate: merge`, `agent:
  eng-manager`) carrying both PR links (`pr_urls:` as a YAML list of
  `{repo, url}` pairs, per the skill's corrected instruction), all four
  gate verdicts by file reference, the named non-blocking gaps, and an
  explicit Sequencing section explaining the stacked-branch choice above
  and both legal ways to resolve merge order. Ran
  `departments/engineering/lib/eng-notify.sh raise`: sent cleanly
  (`traces/eng-notify-2026-09-02.log`: `sent: active`).

  **Stamped `notified:` from the trace log's own local-clock value
  directly (`2026-09-02T10:51:07`), not a `date -u` conversion — and
  caught a live error in an existing proposal while checking which
  convention was actually correct.** The 09:30 `scheduled` pass's own
  proposal (`proposals.md`, 2026-09-02 row) claims `ENG-008`'s and
  `ENG-013`'s merge-request `notified:` stamps are genuine UTC, "exactly
  7h ahead" of their trace-log line, unlike the PM-agent items it was
  actually investigating. Checked directly rather than carried forward,
  per this instance's own standing practice of not trusting a citation
  about a file this pass could just open: `inbox/2026-08-31-eng013-merge-request.md`'s
  `notified: 2026-08-31T11:05:16` against
  `traces/eng-notify-2026-08-31.log`'s `[11:05:16] sent: ...` line for the
  same raise — textually identical, zero gap. `ENG-008`'s pair
  (`11:15:29`/`11:15:29`) match the same way. The proposal's specific claim
  was wrong: there is no second, already-correct code path this board's
  merge requests follow — every gate item, regardless of which agent
  raises it, stamps local wall-clock time in a bare ISO string with no
  offset. Corrected the proposal's three cells in place (`What`/`Why it
  matters`/`Size`) rather than filing a disconnected duplicate, matching
  this file's own `ENG-016` row's precedent of appending a correction into
  an existing entry. Stamping this item consistently with the *actual*,
  verified, board-wide convention (not the disproven claim) so it reads
  the same way every other gate item on this board does.

  **Cap check before this transition, read fresh from `inbox/`'s actual
  top-level contents**: nine items present besides this pass's own new
  one — none newly added since the 09:30 pass's own accounting, none
  answered. Approver-facing WIP was already `3/2`, over cap
  (`ENG-008`, `ENG-013`, `ENG-016`) going in. This transition adds a
  fourth. Per `eng_build_loop.md`'s own guard, the cap gates **new** work
  from starting that will need the approver — it does not hold a ticket
  that has already earned `ready-to-ship` back from reaching its required,
  non-discretionary L1 conclusion, and `ENG-008`/`ENG-013` both already
  set this exact precedent (their own release-readiness hops proceeded
  while the cap was over, because neither was a new start). Not treated
  as a reason to hold this hop.

  State → `blocked`, `blocked_on: approver`, `blocked_from:
  ready-to-ship`, owner `devops → approver`. `links.pr` set to both PR
  URLs (`pr:` as a YAML list of `{repo, url}` pairs, matching `ENG-008`'s
  corrected convention, not `ENG-011`'s original delimited-string bug).
  `time_spent`/`time_remaining` updated in the same edit as this entry.

  **1 transition this pass** (`ready-to-ship → blocked`), well under the
  cap of 4 — opening two PRs and writing the gate item is itself the real
  work of this hop. **Consequence:** `machine_wip` 2/1 → 1/1 (`blocked`
  sits outside the counted `ready`..`ready-to-ship` range; `ENG-010` at
  `ready` is now the only ticket inside it, at cap exactly, not over).
  Approver-facing WIP `3/2 → 4/2`; no separate approval cap exists to
  update (removed 2026-08-29).

  **Dead-end sweep (scoped to this event):** this ticket's log now ends in
  a valid, accounted-for state with the chain record below. `ENG-008` (the
  ticket this branch stacks on) untouched beyond the read-only `gh pr
  view`/ancestry checks above.

  **Notify sweep:** this pass's own gate item raised and stamped above.
  Nothing else newly eligible to nudge — `ENG-008`/`ENG-013`/`ENG-016`
  already spent their one nudge each; this new item is 0h old.

  **1 proposal corrected** (`proposals.md`, 2026-09-02 row — see above; not
  a new filing, a correction to an existing one that turned out to be
  wrong on direct re-check). No new observations this pass.

  `chained: none` — `blocked`, `blocked_on: approver`. This is the human
  gate the whole hop was driving toward; firing `continue ENG-009` again
  would only queue against a ticket with nothing left for a machine to do
  until the approver merges one or both PRs (in either sequencing order,
  per the item's own Sequencing section) or replies to the gate item.
  Post-pass `eng-gate-check.sh`, scoped (`ENG-009`) and whole-board: both
  exit 0, clean, no `WAIVED:` lines.

- **2026-09-02, informational cross-reference only — no state change, this
  ticket not touched.** Found by `ENG-008`'s own round-3 code review
  (`continue ENG-008` event pass): this ticket's branch is stale against
  `ENG-008` again. `git merge-base --is-ancestor` on `ENG-008`'s latest fix
  commits (`aiorders-api@7c6e4b8`, `aiorders-admin-hub@141f2eb` — dropping
  the redundant `accepts_barter` column per the approver's merge-request
  reply) against this ticket's tip (`aiorders-api@d37e0c9`,
  `aiorders-admin-hub@92bcacd`) returns **false** on both repos. This is the
  *second* time this exact staleness has happened between these two tickets
  today — see this ticket's own round-1 review above (the null-coalescing
  bug reappearing because this branch forked before `ENG-008`'s round-2 fix)
  and the rebase hop that fixed it. That rebase synced against `ENG-008`'s
  round-2 tip; `ENG-008` has since moved again (round 3), so the sync is
  stale a second time.

  **Not acted on here** — out of scope for the event that found it
  (`continue ENG-008`, resume that ticket only); this ticket's own ready
  state (`blocked`/`blocked_on: approver`, merge request open and
  unanswered) is untouched, no code or branch on this ticket was read or
  written. Full detail: `agents/principal-engineer/reviews/ENG-008.md`
  (round 3, "A cross-ticket finding" section) and
  `agents/principal-engineer/notebook/2026-09-02-review-log.md`. A proposal
  for the general gap (check a ticket's branch against the sibling it
  forked from, not just `main`) is already filed
  (`agents/eng-manager/proposals.md`, 2026-09-02, `principal-engineer`) off
  this same pair's first occurrence — not re-filed. Practical consequence
  for whoever next picks up this ticket or answers its merge request:
  merging either of this ticket's two PRs as they stand today would ship
  code stacked on `ENG-008`'s pre-round-3 commits, which still reference the
  `accepts_barter` column the approver already rejected — this ticket needs
  a rebase onto `ENG-008`'s current tip and a fresh review/quality/security
  cycle before its own merge request should be treated as safe to action,
  the same way its own round-1→round-2 rebase worked earlier today.

  `chained: none` — no state on this ticket changed; this entry exists so
  the fact is on record before either PR is merged, not to restart this
  ticket's own machine-owned pipeline.

- `2026-09-03` **gate item corrected — the fact above had reached this
  ticket's own log but not the merge-request the approver actually reads**
  (eng-manager, `scheduled` event pass, context `auto-drain` — whole-board
  sweep). Mode check clean (`MODE=active`). Pre-pass `eng-gate-check.sh`,
  whole-board: exit 0, clean.

  Merge detection (step 5) on all five `blocked` tickets included the
  sibling-staleness check by habit, not by procedure mandate (the standing
  proposal below is still unimplemented). Re-ran `git merge-base
  --is-ancestor` on `ENG-008`'s current tips against this ticket's, fresh
  rather than trusted from the entry above — same result, still **false**
  on both repos. Went one step further than that entry did: checked
  whether the two branches' diffs actually *overlap*, not just share a
  file. `aiorders-api`: this ticket's diff never mentions
  `accepts_barter` — clean, no real conflict coming. `aiorders-admin-hub`:
  grepped this ticket's tip directly, found all 11 `accepts_barter` lines
  `ENG-008`'s round-3 fix deleted/renamed are still present verbatim in
  `Influencers.tsx`, untouched by this ticket's own diff (confirmed
  against the diff stat, not just the grep) — a real conflict, not
  cosmetic proximity.

  **The actual gap this pass closes: `inbox/2026-09-02-eng009-merge-request.md`**
  — raised 10:51 on 2026-09-02, well before `ENG-008`'s round-3 fix
  (~22:48 the same day) — **still read "recommendation: merge" and told the
  approver merging `ENG-008` first would let this PR "merge cleanly," which
  is no longer true.** The prior entry's own finding never reached that
  file. Corrected in place: `recommendation:` now reads `hold` with a
  one-line reason; an "Update, 2026-09-03" block under Sequencing gives the
  same repo-by-repo finding this entry states, plus a concrete
  recommendation (rebase onto `ENG-008`'s current tip, re-run
  review/quality/security on the delta, same repair the round-1→round-2
  rebase already did once today). `ENG-010`'s merge request
  (`inbox/2026-09-02-eng010-merge-request.md`) also corrected with a
  shorter cross-reference — its own diff doesn't touch the conflicted
  lines (checked fresh), but it inherits this branch wholesale and will
  need the same rebase-and-follow treatment once this one is fixed.

  **Deliberately not re-notified.** `eng-notify.sh`'s own header states the
  budget precisely: one `raise`, one `nudge`, ever, then the daily
  brief/weekly report — this item already spent its `raise`
  (`notified: 2026-09-02T10:51:07`) and isn't yet 24h old, so a `nudge`
  isn't due and using one now would spend this item's only reminder on a
  content correction rather than "still waiting," blurring what a nudge
  means. The correction lives in the file itself, which is where the
  approver actually reads and answers from (established pattern — hand-edits
  the gate file directly rather than replying via Telegram); no code or
  branch on this ticket touched.

  **0 transitions** — `state`/`owner` unchanged (`blocked`/`approver`); this
  is a correction to an already-raised gate item, not a new one, so no
  approver-facing WIP or cap change. `machine_wip` unaffected (this ticket
  sits outside the counted range).

  **Dead-end sweep (scoped to this finding):** `ENG-010`'s own merge
  request corrected in the same pass, above — not a separate dead end,
  the same fact reaching a second stacked ticket. **Notify sweep:**
  covered above — deliberately not re-pinged. **No new proposal filed** —
  the standing one (`proposals.md`, 2026-09-02, principal-engineer)
  already names this exact gap generally; this is that same proposal's
  second confirmed occurrence on the same ticket pair, not a third
  distinct one, so no new row.

  `chained: none` — `blocked`, `blocked_on: approver`, unchanged. Nothing
  for a machine to do on this ticket until the approver acts (merge, hold
  per the corrected recommendation, or reply otherwise) or a future pass
  rebases it. Post-pass `eng-gate-check.sh`, whole-board: see board index.

- `2026-09-03` **merge request nudged — crossed 24h unanswered** (eng-manager,
  `watch` event pass, context `launchd`). Mode check clean (`MODE=active`).

  Notify sweep (step 7) computed this item's age against current UTC
  (`date -u`: `2026-09-03T11:33:19Z`) against its own `notified:
  2026-09-02T10:51:07` — 24h42m, `nudged:` and `decision:` both still empty.
  Ran `lib/eng-notify.sh nudge inbox/2026-09-02-eng009-merge-request.md`,
  stamped `nudged: 2026-09-03T11:34:08`. Board index's own "Waiting on the
  approver" line corrected to match (previously still said "not yet due").

  Re-ran this ticket's own merge-detection check while here (step 5, this
  pass swept every `blocked` ticket since the watch fired on merge-request
  files): `feat/ENG-009-influencer-engagement-info` still **not** an
  ancestor of `origin/main` on either repo — unchanged from the prior
  entry, still blocked on the rebase-then-remerge this ticket's own
  `recommendation: hold` already asks for.

  Noted, not re-filed: the nudge's own log line read `sent: active`, the
  same `$MODE`-clobbered-by-`.env` symptom `proposals.md`'s 2026-08-25 row
  already tracks — the Slack message still carried the right content, just
  without the "still waiting" framing line.

  `chained: none` — `blocked`, `blocked_on: approver`, unchanged. A nudge
  doesn't advance a ticket; the next hop is still the approver's own
  merge/hold/rebase decision, or a future pass finding the rebase already
  done.
