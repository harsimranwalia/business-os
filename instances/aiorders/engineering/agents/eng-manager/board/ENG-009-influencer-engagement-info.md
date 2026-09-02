---
id: ENG-009
title: Influencer engagement info — internal activity signal plus a staff-editable social stat
project: aiorders-admin-hub
type: feature
size: S
time_estimate: a few hours to half a day
time_spent: ~2h build + ~1h rebase-and-refix (two-repo rebase onto ENG-008's fix commits; one real multi-hunk test conflict resolved by hand in aiorders-api, aiorders-admin-hub's flagged hunk auto-merged correctly; both re-verified and re-pushed)
time_remaining: review + quality round 2, security, release-readiness, then opening the L1 PRs
severity: P3
priority:
state: building
owner: eng-manager
lane: full
blocked_on:
blocked_from:
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
