# Engineering Board — pass log archive

Dated pass entries moved out of `_index.md` once the live board holds more than
three, newest first. The live board keeps its table plus enough recent narrative
to resume a ticket; everything older lives here.

Nothing reads this file on a pass — it is the department's history, not its
state. `lib/eng-gate-check.sh` globs `ENG-*.md` and never sees it.

This exists because every pass reads `_index.md` in full, so an append-only log
there is a tax on every future pass.

---

## 2026-08-28 — decision ENG-006: merge-request gate closed, control-center jump reconciled — shipped → verified

`decision` event pass, context `inbox/2026-08-28-eng006-merge-request.md`.
Narrow scope per the event contract (act on the answered gate item, advance
only this ticket). Mode check clean (business-os `.env` → `MODE=active`).
Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-006`)
and whole-board: both exit 0, clean.

**Found the ticket already past the gate item it was meant to act on.** The
tracked item carried `decision: approved` (`decided: 2026-08-29T02:59:33Z`,
text "approved"), but `ENG-006`'s own `state:` was already `shipped` — a
"control center" dashboard action had advanced `blocked → shipped` ahead of
any build-loop pass (the one-liner immediately above this entry, in the
ticket's own log). Second occurrence of the gap `ENG-002` first hit
(`proposals.md`, 2026-08-26 row), this time hybrid: unlike `ENG-002` (no
reply at all, item left open), the tracked item *was* answered — just
minutes after the merge rather than instead of it. Addendum filed in
`observations.md` rather than a new proposal row; journaled in
`decision-journal.md`.

**Neither signal trusted on its own text.** Re-ran the loop's own
merge-detection check from scratch in the department's own worktree: `git
fetch` + `git merge-base --is-ancestor origin/loyalty-system origin/main` →
MERGED, `40d7c36` (PR #2's merge commit) directly on `c3ab50c` with no
intervening commits; cross-checked via `gh pr view 2` → `MERGED`,
`2026-08-29T02:57:05Z`, ~2m28s before the gate item's `decided:` stamp — same
"merge, then record" shape as `ENG-005`. The control center's `shipped` call
checks out; not redone.

**Closed out `shipped → verified` in one hop.** Acted as devops: confirmed
the migration and all 7 edge-function files present on `origin/main`
(branch-to-main diff empty, so the already-passing 27/27 Deno suite still
holds — not re-run for zero new information); confirmed no CI/CD exists;
confirmed this worktree has no linked Supabase session
(`supabase migration list --linked` → "Cannot find project ref"), so
`health_check: not checked` recorded honestly rather than inferred. Release
record: `agents/devops/releases/2026-08-28-aiorders-api-ENG-006.md`. Acted as
product-manager: AC3/4/7 confirmed directly against the merged tree
(unit-test-covered linking/validation logic, no live OTP needed); AC1/2/5/6
remain **not verified live**, unchanged from the already-named, already
approver-seen gap (Supabase phone-auth + SMS vendor not yet configured) —
carried forward, not new, not blocking, same standard applied at every gate
on this ticket. PRD `status: designed → verified`. Full reasoning on the
ticket's own log.

**1 transition this pass** (`shipped → verified`), well under the cap of 4.
Approver-facing WIP 1 → 0; approval cap 1/3 → 0/3 — `ENG-006` was the only
item on either. `machine_wip` unaffected (0/6).

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for terminal state. No other ticket in flight.

**Notify sweep:** nothing to raise (`verified` raises no gate item); nothing
to nudge (item now closed, not open). Approval cap 0/3 — no stall.

`chained: none` — `verified` is terminal. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-28 — scheduled (launchd): safety-net sweep — merge check confirms PR #2 still open

`scheduled` event pass, context `launchd`, the four-times-daily safety net.
Queued directly behind, and drained immediately after, the `watch` pass that
finished at 15:37:45 (`traces/eng-loop-2026-08-28.log`) — not the
decision/watch race documented on this instance: no hand-edited gate item is
in play here, and the `watch` pass's own narrower contract explicitly left
merge detection, dispatch, and the full dead-end sweep out of scope. Those
are exactly this event's job, so this is the late-safety-net case, not the
race — and unlike that case's usual "found nothing" shape, this pass had one
real check of its own to run. Mode check clean (`MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (this event
names no ticket to scope to): exit 0, clean.

**Business intake:** `agents/product-manager/inbox/` and `inbox/requests/`
hold only `.gitkeep` (plus the former's `_handled/`). Nothing to shape.

**Technical intake:** `agents/eng-manager/inbox/` holds only `.gitkeep`.
Nothing to batch into `proposals.md`.

**Gate returns:** `inbox/` holds the same two live items the immediately
preceding `watch` pass already read fresh and accounted for —
`2026-08-28-eng006-merge-request.md` (still the unfilled "Filled in by the
approver." placeholder, no `decision:`) and `2026-08-28-eng-events-dropped.md`
(no `decision:`, not P0). Re-read both directly rather than trusted from the
board's own account: unchanged, neither new. Nothing to act on.

**Merge detection — the one check this event contributes that the prior pass
didn't.** `ENG-006` is `blocked` on its L1 PR
(https://github.com/harsimranwalia/aiorders-api/pull/2). In the worktree
(`~/Documents/projects/_eng/aiorders-api`, clean): `git fetch origin`, then
`git merge-base --is-ancestor c3ab50c origin/main` — **not an ancestor**;
`origin/main` is still at `5b3bac2`. Cross-checked independently via `gh pr
view 2 --json state,mergedAt`: `state: OPEN`, `mergedAt: null`. Both routes
agree: **not merged.** `ENG-006` stays `blocked`, `blocked_on: approver`,
unchanged — PR opened today (`notified: 2026-08-28T21:42:08`, well under an
hour before this pass), nowhere near the 3-day resurface threshold.

**Dispatch:** nothing to start — `ENG-006` is the only in-flight ticket and
it's `blocked`, not in To-do; no free slot to fill regardless.

**Dead-end sweep:** `ENG-006`'s own ticket log ends validly, `chained: none`
with the blocked-on-approver reason, matching the board. No ticket lacks an
owner; no broken chain.

**Notify sweep:** nothing to raise (no new gate item), nothing to nudge (the
merge-request item is under an hour old), no stall (approval cap 1/3, not
full).

**Observations/exceptions/journal:** none. No gate was answered this pass,
and the two open `inbox/` items plus the `eng_stamp()` fingerprint bug were
already fully accounted for by the `watch` pass that drained immediately
before this one — nothing new to add on top of that.

`chained: none` — `ENG-006` stays `blocked`, `blocked_on: approver`; nothing
for a machine to do until the approver merges the PR or answers the gate
item directly. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board: exit 0, clean.

## 2026-08-28 — watch: swept all three inboxes, nothing new; found the deeper cause of the watch-fingerprint bug

`watch` event pass, context `launchd`. Per the event's own narrower contract,
swept `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`, and
`inbox/` (including `inbox/requests/`) only, acting on whatever is new — not
a board-wide sweep. Mode check clean (business-os `.env` → `MODE=active`).
Pre-pass `departments/engineering/lib/eng-gate-check.sh`, whole-board (this
event names no ticket to scope to): exit 0, clean.

**Swept all three inboxes fresh; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
`.gitkeep` (plus the former's already-`_handled/` entry); `inbox/requests/`
is empty. `inbox/` holds exactly two live items, both read directly rather
than trusted from the board's own summary:
`2026-08-28-eng006-merge-request.md` (`ENG-006`'s own L1 merge-request gate,
raised and notified by the immediately preceding `continue ENG-006` pass at
`21:42:08`) still carries the unfilled "Filled in by the approver."
placeholder — no decision yet; and `2026-08-28-eng-events-dropped.md` (the
day's dropped-event incident notice) still carries no `decision:` field and
is still not P0. Both predate this fire and are already accounted for on the
board's own log — nothing new in any of the three inboxes.

**Chased down the incident notice's "already notified" claim rather than
taking it at face value.** `traces/eng-notify-2026-08-28.log` shows the
10:42:17 raise attempt for that file returned `FAILED: active ... — item
still in inbox and in the tab` — the same already-filed `MODE`-collision bug
every other gate item on this instance has hit (`sent: active`, not `sent:
raise`), not a successful notification. The file's frontmatter carries no
`notified:` field, consistent with the failure. Not re-raised here: it's an
already-corroborated, already-proposed bug in shared department code
(`lib/eng-notify.sh`), out of a `watch` pass's narrow scope to fix, and the
item isn't P0, so nothing compels a retry — it stays visible in `inbox/`
regardless, per the constitution's own design.

**Found a deeper cause underneath the open `.watch-seen` proposal
(`proposals.md`, 2026-08-26 row) rather than just logging another
corroboration of its already-known symptom.** Read `watch_fingerprint()`
(`lib/eng-trigger.sh:366`) and the `eng_stamp()` helper it calls per file
(`lib/eng-env.sh:185`): `eng_stamp()` is `date '+%Y-%m-%dT%H:%M:%S%z'` and
ignores its `$1` argument completely, returning wall-clock time rather than
anything derived from the file it's supposedly stamping (contrast
`eng_mtime()` immediately above it, which correctly `stat`s `$1`). Verified
empirically, not just read: called the real function twice, 2s apart,
against these same two unchanged files — two different SHA-1s
(`cba0b32b...` vs `55b6fbd9...`). So the open proposal's own fix (commit the
fingerprint after every event type, not only `watch`) would not close this —
any two fingerprint computations of a genuinely unchanged, non-empty inbox
more than about a second apart already differ, because the hash is a
function of call-time and file *count*, never file identity. Filed as an
addendum in `observations.md` (2026-08-28, last row) pointing back at the
open proposal rather than as a new row — same shape the 2026-08-26
self-modifying-pass addendum used for the same proposal.

**Merge detection, dispatch, and the full dead-end sweep are out of scope
for this event** — no ticket sits in a startable state regardless; `ENG-006`
is the only in-flight ticket, still `blocked`/`blocked_on: approver` on its
L1 PR. Its own ticket log already ends in a valid, accounted-for state with
`chained: none` from the pass that opened the PR — spot-checked directly
against the file rather than trusted from the board's account: matches.

**Notify sweep:** nothing new to raise. `ENG-006`'s merge-request item is
well under 24h old (raised `21:42:08` today). The incident notice has no
`notified:` to measure a nudge threshold against, and isn't P0 — left as is,
per this pass's own instruction not to surface anything but a P0.

**Nothing to journal** — no gate was answered this pass.

No ticket was touched, no ticket state changed, no gate item was written.
`chained: none` — this pass advanced no ticket, so there is no hop of its
own to fire; `ENG-006` stays `blocked`, `blocked_on: approver`, exactly as
the pass before this one left it. All WIP/approval-cap figures in the header
are unchanged (machine WIP 0/6, approver-facing WIP 1/2, approval cap 1/3).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit
0, clean.

## 2026-08-28 — continue ENG-006: L1 PR opened, merge-request gate raised — ready-to-ship → blocked

`continue ENG-006` event pass, the dedicated session the preceding pass
chained specifically to open the L1 PR. Narrow scope per the event contract
(resume this ticket from its current state; no board-wide sweep). Mode check
clean (`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped and whole-board: both exit 0, clean.

**Release window re-checked fresh**, as the preceding pass explicitly asked
the session that opens the PR to do: Friday 2026-08-28, 14:40 PDT (before the
15:00 cutoff), `MODE=active`, no `ENG_RELEASE_FREEZE`. Inside the window.
Checked for an already-opened PR first (`gh pr list --head loyalty-system`:
empty) and confirmed the worktree (`_eng/aiorders-api`, clean, `loyalty-system`
at `c3ab50c`, not yet merged) before creating one, same discipline `ENG-005`
used at this identical boundary.

**Opened the PR**: https://github.com/harsimranwalia/aiorders-api/pull/2.
Wrote the L1 merge-request item (`inbox/2026-08-28-eng006-merge-request.md`,
`gate: merge`) carrying the PR link and all four gate verdicts (review,
quality, security, migration) by file reference, plus the three
already-designed-around items (SMS/phone-provider config, consent capture,
phone-recycling mitigation) so the approver sees them at the merge decision
itself. Ran `lib/eng-notify.sh raise` — reproduced the already-filed `MODE`-
collision bug (`sent: active`, not `sent: raise`) — corroborating, not new.
Stamped `notified: 2026-08-28T21:42:08` by hand. State → `blocked`,
`blocked_on: approver`, `blocked_from: ready-to-ship`, owner `devops →
approver`, `links.pr` set — same design `ENG-002`/`ENG-005` used at this
boundary.

**1 transition this pass** (`ready-to-ship → blocked`), well under the cap of
4. `machine_wip` 1/6 → 0/6 (`blocked` sits outside the counted range).
Approver-facing WIP 0 → 1; approval cap 0/3 → 1/3.

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for state with the chain record below. No other ticket in
flight.

**Notify sweep:** this pass's own gate item raised and stamped above. Nothing
to nudge (brand new). Approval cap 1/3, not full — no stall.

`chained: none` — `blocked`, `blocked_on: approver`. This is the human gate
the whole hop was driving toward; nothing left for a machine to do until the
approver merges the PR or replies to the gate item. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-28 — continue ENG-006: building through ready-to-ship, recovered from a timeout

`continue` event pass, context `ENG-006`, attempt 2/2 after the first
dispatch timed out at 1800s. Narrow scope per the event contract (resume
this ticket from its current state; no board-wide sweep). Mode check clean
(`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped and whole-board: both exit 0, clean.

**Recovered an unrecorded build** (same shape as `ENG-002`/`ENG-005`'s own
precedent): the dead first attempt had already branched `loyalty-system` in
`_eng/aiorders-api`, written and DB-verified the migration, written the
`platform-customer-auth` edge function plus tests, and fixed a real bug in
its own phone validator — all uncommitted when it hit the timeout mid
re-verification. Ruled out a live concurrent session before trusting any of
it (lock pid, running `claude` pid, and `.pass-out.*` all traced to this
exact invocation). Independently re-verified rather than trusted: deno
test/check/lint re-run fresh via Docker (deno isn't installed on this host)
— 27/27 tests, clean check, clean lint. Full detail on the ticket's own log.

**Ran the full arc in one session, same stopping point as `ENG-005`'s
precedent:** committed and pushed (`building` done) → code review + quality
combined hop (`agents/principal-engineer/reviews/ENG-006.md`,
`agents/qa/test-plans/ENG-006.md`, both **pass**) → security
(`agents/security/reviews/ENG-006.md`, **pass**) → `ready-to-ship` (devops:
migration gate already cleared, $0/month cost, rollback tested, no live
caller yet so zero production blast radius). 4 transitions, at the cap —
stopped before opening the PR (`blocked`), deliberately, same as `ENG-005`.

**Three pre-existing, already-designed-around items carried forward rather
than re-derived by the next reader:** Supabase phone-provider/SMS-vendor
configuration still open (this ticket's OTP-dependent ACs are unreachable
until it lands), consent capture for the new cross-restaurant correlation
not yet wired (approver's/counsel's call per the design), and the
phone-recycling mitigation deliberately deferred as a build-time refinement.
None block this verdict — all three were named in the design doc before
this code was written, not discovered here. Full detail, including the
independent-verification narrative and the per-gate reasoning, is on the
ticket's own log (`agents/eng-manager/board/ENG-006-unified-customer-identity.md`).

**Consequence:** `machine_wip` stays 1/6 — same ticket, later state in the
same counted range. Approver-facing WIP and approval cap both unaffected —
no gate raised this pass (the merge request, which will need the approver,
is the next hop's work).

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for state with the chain record below.

**Notify sweep:** nothing raised this pass. Approval cap 0/3, not full — no
stall.

**Observations/exceptions:** none filed — the recovered-unrecorded-build
shape corroborates `ENG-002`/`ENG-005`'s precedent rather than adding a new
one.

`chained: ENG-006` — `ready-to-ship` is devops-owned, not the approver, not
blocked, not terminal. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-006` before
exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-006`) and whole-board: both exit 0, clean.

## 2026-08-28 — scheduled: ENG-006's G2 caught mid-sweep — awaiting-decision → ready

`scheduled` event pass, context `launchd` — the four-times-daily safety net.
Mode check clean (`MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Full board swept, not just the one ticket.** `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/`, and `inbox/requests/` all empty (bar
`.gitkeep`/already-`_handled/` entries) — no PM or EM intake waiting. No
ticket sits `blocked` on an L1 PR — merge detection had nothing to check.
`ENG-006` was the only in-flight ticket, and its `inbox/` gate item
(`2026-08-28-eng006-g2-oneway-door.md`) had already been answered
(`decided: 2026-08-28T20:09:06`) by the time this pass read it — caught here
precisely because this is what a scheduled sweep is for: neither `watch`
(unwired on this instance) nor a tracked-channel reply (this approver
hand-edits gate files directly, every time so far) had a live path to act on
it sooner. `traces/.pending` held a `decision` event for the same file
queued behind this pass — the already-documented duplicate-event race
(`observations.md`), not new; that queued fire will find the item already in
`_handled/` and no-op.

**Acted on the answer as eng-manager (G2 is the EM's gate).** Approved, with
the approver's own reversibility criterion restated in full rather than a
bare yes — read in full on `inbox/_handled/2026-08-28-eng006-g2-oneway-door.md`
and the ticket's own log. Confirms rather than changes the design's approach:
legacy `customers` stays untouched, the two flows run side by side, and a
unified cross-restaurant order view is explicitly later-ticket scope. Ticket
advanced `awaiting-decision → ready` — one transition, well under the cap of
4, stopping there because `building` is new implementation work and this
event's dispatch step leaves that for a fresh chained session by design.
Journaled in `agents/eng-manager/config/decision-journal.md`. Full detail,
including the cap arithmetic and the design's own breakdown this ticket's
`ready` state relies on, is on the ticket's own log
(`agents/eng-manager/board/ENG-006-unified-customer-identity.md`).

**Consequence:** `machine_wip` 0/6 → 1/6 (`ENG-006` now inside the counted
`ready`..`ready-to-ship` range for the first time). Approver-facing WIP 1/2 →
0/2; approval cap 1/3 → 0/3 — both now clear.

**Dead-end sweep (whole-board):** `ENG-001`–`ENG-005` all terminal with valid
closing log lines. `ENG-006` now ends in a valid state with a chain record
below. `inbox/2026-08-28-eng-events-dropped.md` (incident notice, `ticket:
unknown`) has no `decision:` yet and isn't P0 — left waiting on the approver,
already notified once at creation; not re-surfaced per the constitution's
P0-only rule for this pass.

**Notify sweep:** nothing raised this pass (one gate closed, none opened).
Nothing past 24h with no `nudged:`/`decision:`. Approval cap 0/3, not full —
no stall.

**Observations/exceptions:** none filed — the queued-duplicate race behind
this pass corroborates an already-open pattern rather than adding a new one.

`chained: ENG-006` — `ready` is eng-manager-owned, not the approver, not
blocked, not terminal. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-006` before
exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-006`) and whole-board: both exit 0, clean.

## 2026-08-28 — decision ENG-006: G1 approved, design done, one-way door escalated — awaiting-scope → designed → awaiting-decision

`decision` event pass, context `inbox/2026-08-27-eng006-g1-scope.md`. Narrow
scope per the event contract (act on the answered gate item, advance only
this ticket). Mode check clean (`MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

**Not a clean unanswered gate — found mid-recovery.** An earlier `watch` pass
today (08:35–08:44) had already started processing this exact answer: it
edited the PRD's `## Decision` section and flipped its status to `designed`,
then crashed on the account's monthly spend limit before touching the ticket,
the board, or the gate item. Its retry failed on a network error and the
event was dropped after two attempts
(`inbox/2026-08-28-eng-events-dropped.md`). This pass verified the PRD's
claims against the filesystem rather than trusting them — the frontend
knowledge-capture doc it claimed was "Done" did not exist — and completed the
work for real. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-006-unified-customer-identity.md`); one
observation filed on the general pattern
(`agents/eng-manager/observations.md`).

**Design done fresh against the live `aiorders-api` repo** (no schema in
version control there at all — read the edge functions that query
`customers` instead of trusting the PRD's inferences). Corrected one PRD
assumption in the process: legacy customer records are already scoped by
`restaurant_id` **or** `brand_id`, not restaurant-only. Full design:
`agents/architect/designs/ENG-006-unified-customer-identity.md` — Supabase's
native phone/OTP auth, two new additive tables, `customers` untouched.

**One-way door escalated rather than decided** — the PRD flagged this twice
for the architect to evaluate at G2; given the stakes (largest new subsystem
on this board) and no G2 precedent yet, put the actual question to the
approver instead of deciding unilaterally. Raised
`inbox/2026-08-28-eng006-g2-oneway-door.md`.

**Both G1 riders honored:** wrote
`agents/product-manager/specs/loyalty-program-frontend-understanding.md`
(knowledge capture only, not scheduled); carried the resolved SMS-vendor-cost
note into the design's Risks, with the caveat that delivery still isn't
wired to any real vendor in code.

**2 transitions this pass** (`awaiting-scope → designed → awaiting-decision`),
under the cap of 4. `machine_wip` unaffected. Approver-facing WIP and
approval cap both net unchanged at 1/2 and 1/3 — G1 closed, G2 opened, same
ticket.

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for state with a chain record below.

**Notify sweep:** this pass's own gate item raised and stamped. Nothing to
nudge. Approval cap 1/3, not full — no stall.

`chained: none` — `awaiting-decision`, owned by the approver; the chaining
guard never fires on a ticket waiting on a human. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-006`) and
whole-board: both exit 0, clean.

## 2026-08-28 — watch: swept all three inboxes again, nothing new

`watch` event pass, context `launchd`. Per the event's own narrower contract,
this sweeps `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`, and
`inbox/` only, acting on whatever is new — not a board-wide sweep. Mode check
clean (business-os `.env` → `MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh` (`ENG_ROOT` pinned to this
instance — the default root resolves against the script's own department
location, which has no `board/`; see `observations.md`), whole-board: exit 0,
clean.

**Swept all three inboxes fresh; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
`.gitkeep` (plus the former's already-`_handled/` entry); `inbox/requests/`
is empty. `inbox/` itself holds exactly one live item,
`2026-08-28-eng-events-dropped.md` (the incident notice for today's dropped
build-loop event) — read directly rather than assumed from the board: still
no `decision:` field, still not P0 (an incident notice, not production-down
or an exploitable vuln), still under 24h since its one `raised:` notification
(10:42:17). The immediately-preceding `scheduled` pass already accounted for
this exact file on identical grounds. Nothing else in any of the three
inboxes postdates that pass.

**Another occurrence of the open `.watch-seen` fingerprint-timing race**
(`proposals.md`, 2026-08-26 row; corroborated repeatedly in
`observations.md`). The preceding `scheduled` pass processed this same inbox
state but — being `scheduled`-typed, not `watch`-typed — never called
`commit_watch_fingerprint()`, so `traces/.watch-seen` stayed stamped at
whatever it held before today's `eng-events-dropped.md` arrived. This fire's
recomputed fingerprint still differed from that stale value, cleared the
above-the-lock de-noise check, and spent a full session confirming the
`scheduled` pass had already left nothing behind. Not re-diagnosed at length
here — the mechanism is already on record; this is a data point, not a new
finding. One line added to `observations.md`.

**Merge detection, dispatch, and the full dead-end sweep are out of scope for
this event** — no ticket sits `blocked` on an L1 PR regardless (`ENG-006` is
the only in-flight ticket, at `ready`). `ENG-006`'s own ticket log already
ends in a valid, accounted-for state with `chained: ENG-006`, spot-checked
directly against the file rather than trusted from the board's own account —
matches. That chain's `continue ENG-006` sits queued in `traces/.pending`
behind this pass, unaffected and not duplicated here — also queued behind it,
`1 decision 2026-08-28-eng006-g2-oneway-door.md`, which the prior pass already
predicted will find its file in `_handled/` and no-op.

**Notify sweep:** nothing new to raise. Today's incident notice is under the
24h nudge threshold. Approval cap 0/3, not full — no stall.

**Nothing to journal** — no gate was answered this pass.

No ticket was touched, no ticket state changed, no gate item was written.
`chained: none` — this pass advanced no ticket, so there is no hop of its own
to fire; `ENG-006`'s separately-queued `continue` (from the preceding pass)
runs on its own regardless, once this pass exits. All WIP/approval-cap
figures in the header are unchanged. Post-pass
`departments/engineering/lib/eng-gate-check.sh` (`ENG_ROOT` pinned as above):
exit 0, unchanged.

## 2026-08-28 — decision ENG-005: merge confirmed by git ancestry — blocked → shipped → verified

`decision` event pass, context `inbox/2026-08-27-eng005-merge-request.md`.
Narrow scope per the event contract (act on the answered gate item, advance
only this ticket). Mode check clean (business-os `.env` → `MODE=active`).
Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-005`)
and whole-board: both exit 0, clean.

**The gate item's answer:** `decision: approved`, `decided:
2026-08-28T00:13:09.817494+00:00`, text "merged" — the tracked channel this
time, unlike `ENG-002`'s direct-GitHub/control-center bypass. **Not taken on
the text alone** — re-ran the loop's own merge-detection check
(`schedules/eng_build_loop.md` step 5) from scratch in the department's own
worktree (`~/Documents/projects/_eng/aiorders-admin-hub`): `git fetch origin`
showed `919d355..edf6947 main -> origin/main`; `git merge-base
--is-ancestor chore/ENG-005-a4-poster-generator-wire-in origin/main`
confirmed MERGED; `edf6947` (PR #2's own merge commit) sits directly on
`51cdb29` (this ticket's commit) with no intervening commits, `git diff`
between the branch tip and `origin/main` empty. The merge commit's own
timestamp lands ~20s before the gate item's `decided:` stamp — consistent
with merging and recording the decision in one sitting.

**Acted as devops for `shipped`, then product-manager for `verified`, both
this pass.** Checked out `origin/main` in the worktree, ran `npm run build`
(succeeds; bundle now pulls in the component's own chunks, corroborating it's
genuinely reachable, not just present) and confirmed the wiring directly
(`grep -rn "A4PosterGenerator" src/pages/RestaurantDetails.tsx`). Both PRD
acceptance criteria re-confirmed against the merged tree. **Recorded
`health_check: not checked` and `rollback_tested: false` rather than
`green`/`true`** — unlike `ENG-002`, this release has a real new
production-facing artifact once deployed, and deploying is outside L1
autonomy regardless of diff content (a human merges; a human or their own
process deploys) — this department has no Cloudflare/monitoring access to
confirm live status either way, and said so plainly rather than inferring a
number it can't observe. Release record:
`agents/devops/releases/2026-08-28-aiorders-admin-hub-ENG-005.md`. Gate item
moved to `inbox/_handled/` with a processed footer; journaled in
`agents/eng-manager/config/decision-journal.md`. Full detail on the ticket's
own log.

**2 transitions this pass** (`blocked → shipped`, `shipped → verified`), well
under the cap of 4. Approver-facing WIP 2 → 1; approval cap 2/3 → 1/3
(`ENG-005` no longer counts — `verified` is terminal). `machine_wip`
unchanged at 0/6 (neither `blocked` nor `verified` is in the counted range).

**Dead-end sweep (scoped to this event):** `ENG-005`'s log now ends in a
valid, accounted-for terminal state. `ENG-006` (`awaiting-scope`, owner
approver) untouched — out of scope for a `decision` event naming this
ticket.

**Notify sweep:** nothing to raise (`verified` raises no gate item). Nothing
to nudge — the merge-request item is answered and closed. Approval cap now
1/3, not full — no stall.

**Observation filed, not acted on:** the per-ticket hop-budget file is named
`.hops-{today's date}-{TICKET-ID}` (`lib/eng-trigger.sh`), which resets to a
fresh file every midnight — but this document's own cadence section states
"the day's counter clears at midnight where a ticket's does not." The two
disagree; not investigated further here since it's outside this event's
scope and didn't block this ticket (today's `.hops-2026-08-28-ENG-005` file
didn't exist before this pass, well under the 8/day cap regardless). See
`agents/eng-manager/observations.md`.

`chained: none` — `verified` is a terminal state; nothing left for a machine
or the approver to do on this ticket. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-005`) and
whole-board: both exit 0, clean.

## 2026-08-27 — continue ENG-005: L1 PR opened, merge-request gate raised — ready-to-ship → blocked

`continue ENG-005` event pass — the dedicated session the preceding pass
chained specifically to open the L1 PR. Narrow scope per the event contract
(resume this ticket from its current state; no board-wide sweep). Mode check
clean (`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped and whole-board: both exit 0, clean. `traces/.hops-2026-08-27-ENG-005`
read `3` — third dispatch today, well under `hops_per_ticket` (8, `pro` tier).

**Checked for an already-opened PR first** — the immediately preceding pass
recovered one unrecorded build today already, so a duplicate PR was a real
risk. `gh pr list --head chore/ENG-005-a4-poster-generator-wire-in --state
all`: empty. None existed.

**Opened the PR** (`gh pr create`):
https://github.com/harsimranwalia/aiorders-admin-hub/pull/2. Wrote the L1
merge-request item (`inbox/2026-08-27-eng005-merge-request.md`, `gate:
merge`) carrying the PR link and the three gate verdicts by file reference.
Ran `lib/eng-notify.sh raise` — reproduced the already-filed `MODE`-collision
bug (`sent: active`, not `sent: raise`) — corroborating, not new. Stamped
`notified: 2026-08-27T16:03:58` by hand. State → `blocked`, `blocked_on:
approver`, `blocked_from: ready-to-ship`, owner `devops → approver` — same
design `ENG-002` used at this identical boundary.

**Cap check before advancing, read fresh:** `wip.approver_limit` (2) was at 1
(`ENG-006`'s G1); `awaiting_approver_cap` (3) was at 1/3. `ENG-005` is an
already-in-flight, already-fully-gated ticket reaching its own next gate, not
a new start, so `approver_limit`'s "nothing new starts" consequence is
untouched. Advancing brings `approver_limit` to 2/2 (at the limit, not over)
and `awaiting_approver_cap` to 2/3 (not over) — proceeded on that basis.

**1 transition this pass** (`ready-to-ship → blocked`), well under the cap of
4 — opening the PR and raising the gate is the real work of this hop.
`machine_wip` 1/6 → 0/6 (`blocked` sits outside the counted range).
Approver-facing WIP 1 → 2; approval cap 1/3 → 2/3.

**Dead-end sweep:** this ticket's log now ends in a valid, accounted-for
state with a chain record below. `ENG-006` (`awaiting-scope`, owner
approver) untouched — out of scope for a `continue` event naming this
ticket.

**Notify sweep:** this pass's own gate item raised and stamped above.
Nothing to nudge (brand new). Approval cap 2/3, not full — no stall.

`chained: none` — `blocked`, `blocked_on: approver`. This is the human gate
the whole hop was driving toward; firing `continue ENG-005` again would just
re-queue against a ticket with nothing left for a machine to do until the
approver merges the PR or replies. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-27 — continue ENG-005: recovered an unrecorded build, then ready → ready-to-ship in one hop

`continue ENG-005` event pass — the dedicated `building` (frontend) session
the preceding `decision` pass chained. Narrow scope per the event contract
(resume this ticket from its current state; no board-wide sweep). Mode check
clean (`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped and whole-board: both exit 0, clean.

**The chained `building` session had already run and died before recording
anything.** The worktree carried a clean, pushed commit
(`51cdb29`, "Wire A4PosterGenerator into RestaurantDetails") this ticket's log
had no record of — `traces/.hops-2026-08-27-ENG-005` (`2`) confirms this is
the second dispatch of `continue ENG-005` today. Ruled out a live competing
session first (full `ps`/`ppid` ancestry walk: the process holding
`traces/.loop.lock` is this pass's own top-of-chain orchestrator, not a
second instance), then independently verified the recovered commit rather
than trusting it — diff matches the architect's design exactly, lint
identical to a clean `origin/main` checkout (181 problems, zero new), build
succeeds, no dependency added. Full detail on the ticket's own log.

**Four transitions this pass, at the cap:** `ready → building → in-review →
in-security → ready-to-ship`. Principal-engineer + qa combined hop both
verdict **pass** (`agents/principal-engineer/reviews/ENG-005.md`,
`agents/qa/test-plans/ENG-005.md`); security verdict **pass**
(`agents/security/reviews/ENG-005.md`, confirmed the component's own
edge-function calls stay behind existing Bearer+admin-role gating, no new
capability granted); devops confirmed release readiness (rollback = revert
commit, $0/month, no freeze, no CI/CD to run). **Deliberately stopped at
`ready-to-ship`** rather than also opening the L1 PR and entering `blocked` —
that would be a 5th transition, over the per-pass cap — reserving the PR-open
for its own hop, same as `ENG-002`'s precedent bundles it with the transition
*into* `blocked` rather than before. `machine_wip` unchanged at 1/6
(`ready-to-ship` is inside the counted range); approval cap and approver WIP
both unchanged — none of this pass's transitions raise a gate item.

**Dead-end sweep:** this ticket's log now ends in a valid, accounted-for
state with a chain record below. `ENG-006` (`awaiting-scope`, owner approver)
out of scope for a `continue` event naming this ticket.

**Notify sweep:** nothing to raise (none of this pass's four states raise a
gate item). Nothing to nudge. Approval cap unchanged at 0/3, not full — no
stall.

`chained: ENG-005` — sitting at `ready-to-ship`, owned by devops (agent, not
the approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-005` for the
dedicated session to open the L1 PR and raise the merge-request gate.
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped and
whole-board: both exit 0, clean.

## 2026-08-27 — intake ENG-006: loyalty-points request shaped and split — one foundational ticket raised at G1, four more proposed but not filed

`intake` event pass — a new approver request in
`agents/product-manager/inbox/` (via control center): a cross-restaurant
loyalty points program, backend only for now. Narrow scope per the event
contract (shape the new request and carry it as far as it goes; the board was
not swept). Mode check clean (`MODE=active`; instance `mode:` empty, falls
through). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board (nothing to scope to yet): exit 0, clean.

**Confirmed this was the right event to act on it under.** An earlier
`watch` pass the same day had already found this file and correctly left it
alone — it arrived `via: control-center` with a matching `intake` event
already queued, so shaping it under `watch`'s contract would have both used
the wrong contract and starved the queued `intake` fire of any work to find
(`agents/eng-manager/observations.md`, 2026-08-27). This pass is that queued
fire.

**Full request-readback run** (`skills/request-readback/SKILL.md`): this PM's
reading and a blind architect reading, both independent opus subagents, each
given only the raw request and `knowledge/business-profile.md` — no material
divergence found between them (see `ENG-006`'s own log and PRD for the full
comparison). No question went to the approver as a result; the request is
detailed enough that every load-bearing gap either reading flagged alone was
resolved by proposing a requirement rather than guessing or asking.

**Sized `XL` as a single ticket — split before leaving intake**, per
`config/definition-of-done.md`'s size table. Shaped the identity/OTP-auth/
session/legacy-mapping slice as **`ENG-006`** (`L`, `aiorders-api`, full
lane), the one piece every other slice depends on. PRD written
(`agents/product-manager/specs/ENG-006-unified-customer-identity.md`)
defining the whole proposed five-ticket shape — the other four are
**proposed sequencing only, no IDs allocated, nothing filed** — so this pass
manufactures one ticket's worth of board presence, not five, ahead of the
approver seeing the shape.

**G1 raised** (`size: L` always requires it) — checked caps fresh first:
`wip.approver_limit` (2) at 0, `wip.approval_cap` (3) at 0/3, both free.
`inbox/2026-08-27-eng006-g1-scope.md` written, readback first, then the
recommendation (build `ENG-006` now; the four follow-on slices are open to
correction at this same G1). `lib/eng-notify.sh raise` run (exit 0;
`sent: active` not `sent: raise` — the known `MODE`-collision bug, eighth
corroborating occurrence, still the open `proposals.md` row); `notified:
2026-08-27T13:47:31` stamped. Original request moved
`agents/product-manager/inbox/` → `agents/product-manager/inbox/_handled/`
(new folder — no prior handled-folder existed under the PM's own inbox; this
mirrors the top-level `inbox/_handled/` convention).

**State: `intake → shaped → awaiting-scope`, all in one pass.** `owner`
`product-manager → approver`. Approver-facing WIP 0 → 1; approval cap
0/3 → 1/3. `machine_wip` unchanged at 1/6 — `awaiting-scope` sits outside
that range.

**Dead-end sweep (scoped to this event):** `ENG-006`'s log ends in a valid,
accounted-for state with a chain record. `ENG-005` untouched and out of
scope for this event — it already carries its own valid `chained: ENG-005`
from the immediately preceding pass.

**Notify sweep:** this pass's own gate item raised and stamped above.
Nothing to nudge (brand new). Approval cap 1/3, not full — no stall.

`chained: none` — `ENG-006` sits at `awaiting-scope`, owned by the approver;
the chaining guard never fires on a ticket waiting on a human. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-006`) and
whole-board: both exit 0, clean.

## 2026-08-27 — decision ENG-005: surface follow-up answered — designed → ready in the same pass, no one-way door, chained to building

`decision` event pass — the approver answered `ENG-005`'s G1 follow-up
(`inbox/2026-08-27-eng005-g1-followup-surface.md`). Narrow scope per the
event contract (act on the answered gate item, advance only this ticket).
Mode check clean (business-os `.env` → `MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

**The answer:** `decision: approved`, `decided:
2026-08-27T20:08:53.367622+00:00`, text "lets do RestaurantDetails.tsx" —
confirms the PM's recommendation exactly as offered. Both halves of the
original G1 (fork, then surface) are now answered, so `awaiting-scope`'s exit
condition is met. PRD updated (`status: designed`, acceptance criteria filled
in concretely); gate item moved to `inbox/_handled/` with a processed
footer; journaled in `agents/eng-manager/config/decision-journal.md`.

**Design done this pass** (architect), same one-pass pattern `ENG-002` used
at this boundary. Investigated fresh against `origin/main` in both
`_eng/aiorders-admin-hub` and `_eng/aiorders-api` (`git fetch` first):
confirmed the component's `url-shortener` edge-function dependency exists,
confirmed `jspdf` is already in `package.json` (no new dependency), and
read `RestaurantDetails.tsx` in full to find `Restaurant` has no color field
anywhere — not a correction of the follow-up's own investigation, which
never claimed `primaryColor` was loaded (it named only the four fields that
are), just the next question design had to answer that scope selection
didn't. The design passes `null` and relies on the component's own fallback
accent.
Design written:
`agents/architect/designs/ENG-005-a4-poster-generator-wire-in.md` —
`one_way_doors: []`. No one-way door (additive, reversible, no schema, no
new dependency) → `awaiting-decision` (G2) skipped entirely per
`definition-of-done.md`.

**`ready` reached the same pass** (eng-manager): one task, no sequencing,
assigned to frontend. `machine_wip` 0/6 → 1/6. Approver-facing WIP 1 → 0;
approval cap 1/3 → 0/3. **2 transitions this pass**
(`awaiting-scope → designed`, `designed → ready`), under the cap of 4. Did
not proceed into `building` — new implementation work, which is where a pass
stops and hands off instead of pushing through (`schedules/eng_build_loop.md`
step 6).

**Dead-end sweep:** this ticket's log ends in a valid, accounted-for state
with a chain record below. No other ticket in flight — `ENG-004` is terminal.

**Notify sweep:** nothing to raise (no G2 this pass). Nothing to nudge.
Approval cap 0/3, not full — no stall.

`chained: ENG-005` — sitting at `ready`, owned by eng-manager (agent, not
the approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-005` for the
dedicated `building` (frontend) session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-27 — watch: ENG-005's G1 answered only half its own question — fork resolved, surface carried forward as one follow-up

`watch` (launchd) pass — a file changed in a watched inbox outside the
notify/poll channel. Mode check clean (business-os `.env` → `MODE=active`;
instance `config/config.yaml` → `mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-005`) and
whole-board: both exit 0, clean.

**Swept all three watched inboxes**, per the event's own contract.
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` held one
item directly: `2026-08-27-eng005-g1-scope.md`, changed since the archived
`watch` pass a few entries back confirmed it still blank — now carrying
`decision: approved`, `decided: 2026-08-27T18:03:50.514589+00:00`, a second
`## Decision` section appended below the original placeholder. Answered by
direct file edit, not through `lib/eng-notify.sh`'s reply channel — sixth
such occurrence on this instance (decision journal).

**The answer settles the fork and nothing past it.** Verbatim: "wire it in."
This G1's own text asked for two things at once — decide wire-in vs. revert,
and if wire-in, name the route/surface, "so acceptance criteria can be
written against it." Only the fork came back. Read the two halves
separately rather than treating a partial answer as a complete one: "wire it
in" leaves no real ambiguity about the fork (the revert branch is closed,
the component stays); it says nothing about the surface, which this
ticket's own PRD had already flagged twice (Readback's Assumed section,
Non-goals) as the approver's call, not a default the department infers from
silence or convenience.

**Investigated before asking a second time, rather than bouncing the
question back unhelped.** `git fetch origin` in `_eng/aiorders-admin-hub`
(worktree predated `bfddffe`), then read `A4PosterGenerator.tsx` off
`origin/main`: props are `restaurantName`, `websiteUrl`, `logoUrl`,
`primaryColor`, `restaurantId` — one restaurant's own detail context. Of the
admin hub's 19 pages (`src/pages/*.tsx`) and its sidebar
(`AppSidebar.tsx`), exactly one is shaped to hold that context:
`RestaurantDetails.tsx`, which already loads `name`, `website`, `logo_url`
and `id` for a single restaurant (`Restaurants.tsx` is the list view, not a
detail context). No existing poster/QR/marketing section there — wiring in
means a new section, not flipping on something half-built. Offered as a
recommendation in the follow-up, not adopted as the answer: a well-evidenced
guess is still a guess, and this PRD's non-goal is specifically about not
making this one.

**Closed out the answered item, raised one narrow follow-up, left the fork
resolved on the record.** PRD `## Decision`
(`agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md`)
filled in with the approver's words and this interpretation; `status` stays
`awaiting-scope`. `inbox/2026-08-27-eng005-g1-scope.md` moved to
`inbox/_handled/` with one appended line pointing at the follow-up, so the
closed item is traceable rather than just gone. Wrote
`inbox/2026-08-27-eng005-g1-followup-surface.md` (`agent: product-manager`,
`gate: scope`, `follow_up_to:` the closed item, `recommendation:
RestaurantDetails.tsx`), ran `departments/engineering/lib/eng-notify.sh
raise` on it (reproduced the already-filed `MODE`-collision bug — `sent:
active`, not `sent: raise` — corroborating, not new), stamped `notified:
2026-08-27T18:16:48`. Journaled in
`agents/eng-manager/config/decision-journal.md` — first data point on this
instance of a G1 answer settling part of its own question and leaving a
named, requested sub-detail open.

**Held at `awaiting-scope`, did not advance to `designed`.**
`definition-of-done.md` gives `designed` to the architect for technical
design — not for naming a product surface this PRD explicitly reserved for
the approver. Advancing without the surface would just move the guess one
state later and relabel it a design decision instead of a scope one. `owner`
stays `approver`. No cap or WIP change — still the same one approver-facing
slot this ticket already held (approval cap unchanged at 1/3, approver WIP
unchanged at 1), narrowed to one question on it.

**Dead-end sweep:** `ENG-005`'s log now ends in a valid, accounted-for state
with a chain record below. No other ticket is in flight to check — `ENG-004`
reached `verified` (terminal) in the pass immediately before this one; see
its own board file and the dated entry below.

**Notify sweep:** this pass's own follow-up was raised and stamped above —
nothing else to raise. Nothing to nudge (`ENG-005`'s original G1 is now
answered and closed, its follow-up is minutes old). Approval cap unchanged
at 1/3, not full — no stall.

`chained: none` — sitting at `awaiting-scope`, owned by the approver; the
chaining guard never fires on a ticket waiting on a human. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-27 — continue ENG-004: ready-to-ship through verified in one pass — G3 answered in ~92 seconds, ticket now terminal

`continue ENG-004` event pass — the dedicated `ready-to-ship` (devops)
session the preceding `in-security` hop chained. Narrow scope per the event
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped and whole-board: both exit 0, clean.

**`in-security → ready-to-ship`, 1 transition.** Acted as devops per
`ADR-004`: confirmed no release, rollback, or observability plan is owed —
the change already reached `origin/main` on 2026-08-24, before this ticket
existed. Re-checked `config/projects.md` (L1, worktree present), release
window (Thursday, no `ENG_RELEASE_FREEZE`), and cost (`$0/month`) fresh.
`machine_wip` 1/6 → 0/6.

**Continued into `awaiting-release` the same pass** — unlike `ENG-001`'s
split at this identical boundary, which its own log names as cap-driven; the
approval cap here had room (checked fresh: 1/3, only `ENG-005`'s G1), so
nothing forced a stop. No ADR or schedule rule names a fresh-context
requirement between these two states, unlike security-after-quality. Wrote
and raised `inbox/2026-08-27-eng004-g3-verification.md` (`lib/eng-notify.sh
raise`) — reproduced the already-filed `MODE`-collision/Slack-not-Telegram
bugs (`proposals.md`, 2026-08-25), not a new finding. Cap 1/3 → 2/3; approver
WIP 1 → 2. **2nd transition.**

**The G3 was answered before this pass exited** — `decision: approved`, no
comment, ~92 seconds after `notified:` was stamped, by the same hand-edit
shape every gate on this instance but `ENG-002`'s merge has used. Fifth data
point on that pattern; the turnaround itself journaled as consistent with,
not proof of, the open notify-channel proposal
(`agents/eng-manager/config/decision-journal.md`). Item moved to
`inbox/_handled/`.

**`awaiting-release → shipped`, 3rd transition.** Devops recorded the G3
confirmation in place of a deploy — no release record fabricated at
`agents/devops/releases/`, `links.release` stays empty (`ADR-004`).

**`shipped → verified`, 4th transition — 4 total this pass, at the cap.**
Product-manager re-confirmed all five acceptance criteria fresh against
disk/git (project linkage, admin-hub's empty `supabase/` tree, two re-sampled
blob-SHA matches, the 22-file ordering, `0`/`0` ahead-behind) and re-opened
all three receipts — all hold. Full citations on the ticket's own log.

**This ticket is now terminal.** `machine_wip` stays 0/6; approval cap
2/3 → 1/3 (`ENG-005`'s G1 only); approver WIP 2 → 1 — noted for the next
pass's arithmetic, not acted on here.

**Dead-end sweep (scoped to `ENG-004`):** ends in a valid, terminal state.
`ENG-005` untouched — out of scope for this event.

**Notify sweep:** the pass's own gate item was raised and is already
answered above; nothing else to raise or nudge.

Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped and
whole-board: both exit 0, clean. `chained: none` — `verified`, terminal;
never re-fired.

## 2026-08-27 — continue ENG-004: in-security verdict pass — content-reviewed, not just hash-checked; chained to ready-to-ship

`continue ENG-004` event pass — the dedicated `in-security` session the
preceding combined review+quality hop chained. Narrow scope per the event
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean (business-os `.env` → `MODE=active`; instance
`config/config.yaml` → `mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Dispatch: `in-qa → in-security`, 1 transition.** Acted as security per
`ADR-004` — the one gate on this ticket with real content, not ceremony.
Independently re-derived AC1/presence/AC4 fresh against disk/git in
`_eng/aiorders-admin-hub` and `_eng/aiorders-api` (`git fetch origin` in both
first); re-confirmed AC3 (unmodified) by a second, independent mechanism
(git's own blob SHA, not review/QA's SHA-256) — all six files identical
pairwise across both repos. Then read the six files' actual content, the
substantive check neither review nor QA did: coherent, complete
RLS/`search_path` hardening across `profiles`, `restaurants`, and the new
`restaurant_activations` table. Verdict **pass** —
`agents/security/reviews/ENG-004.md` written, `links.security_review` set.
Full citations on the ticket's own log. `machine_wip` unchanged at 1/6 —
`in-security` falls inside the counted range.

**One observation filed, not a finding** (`observations.md`): a migration
comment about view security semantics that reads backwards against actual
Postgres defaults (`restaurants_public`'s recreate, item 5 of the six) —
explicitly out of this ticket's scope per the PRD's own non-goal ("whether
that policy is still the right policy today"), since the reconciliation
itself is confirmed intact by an independent hash method.

**Not proceeding into `ready-to-ship` this pass, deliberately** — same
discipline this ticket has used at every prior hop; devops's own
confirmation (no release/rollback/observability plan owed, per `ADR-004`) is
real, distinct work reserved for its own session.

**Dead-end sweep (scoped to `ENG-004`):** its log now ends in a valid,
accounted-for state with a chain record below. `ENG-005` (`awaiting-scope`,
owner approver) untouched — out of scope for a `continue` event naming one
ticket.

**Notify sweep:** nothing to raise (`in-security` raises no gate item).
Nothing new to nudge — `ENG-005`'s G1 still under 24h old; approval cap
unchanged at 1/3.

`chained: ENG-004` — sitting at `in-security`, owned by `security` (agent,
not the approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-004` for the
dedicated `ready-to-ship` (devops) session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

## 2026-08-27 — continue ENG-004: combined review+quality hop — building → in-review → in-qa, security deferred to its own session

`continue ENG-004` event pass — the dedicated combined review+quality session
the preceding `ready → building` pass chained (queued behind one intervening
no-op `watch` fire, drained immediately after). Narrow scope per the event
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean (business-os `.env` → `MODE=active`; instance
`config/config.yaml` → `mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

**Dispatch: `building → in-review → in-qa`, 2 transitions.** Acted as
principal-engineer and qa on the combined hop (`schedules/eng_build_loop.md`
step 6): independently re-derived all five acceptance criteria fresh against
disk/git in `_eng/aiorders-admin-hub` and `_eng/aiorders-api` (`git fetch
origin` in both first) rather than citing the design's or `building`'s own
numbers — project linkage, the still-empty `supabase/migrations` on
admin-hub's `origin/main`, both consolidation commit pairs, a fresh
`shasum -a 256` re-hash of all six named files (all identical), the 22-file
migration count/ordering, and the ref-level `0`/`0` ahead-behind on admin-hub's
local `main`. Verdict **pass** on both:
`agents/principal-engineer/reviews/ENG-004.md` and
`agents/qa/test-plans/ENG-004.md` written, `links.review`/`links.test_plan`
set. Full citations on the ticket's own log. `machine_wip` unchanged at 1/6 —
both states fall inside the counted range.

**Not proceeding into `in-security` this pass, deliberately** — sharper than
the "own session" discipline this ticket has used at every prior hop:
`ADR-004` names this ticket's security gate as real, substantive content
(five of six files under review are the RLS/`search_path` hardening surface
itself) and warns explicitly against waving it through as ceremony, unlike
`ENG-001`'s all-`n/a` security pass (the one case here where review, quality
and security were combined into a single session). Reserved for its own
dedicated pass with fresh context.

**Dead-end sweep (scoped to `ENG-004`):** its log now ends in a valid,
accounted-for state with a chain record below. `ENG-005` (`awaiting-scope`,
owner approver) untouched — out of scope for a `continue` event naming one
ticket.

**Notify sweep:** nothing to raise (`in-qa` raises no gate item). Nothing new
to nudge — `ENG-005`'s G1 is still well under 24h old; approval cap unchanged
at 1/3.

`chained: ENG-004` — sitting at `in-qa`, owned by `qa` (agent, not the
approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-004` for the dedicated
`in-security` session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-27 — watch: swept all three inboxes again, nothing new — seventh occurrence, ENG-005's G1 fingerprint-stale exactly as diagnosed

`watch` (launchd) pass, drained immediately behind the `continue ENG-004`
(`ready → building`) pass that ended 10:13:51 (`traces/eng-loop-2026-08-27.log`,
549s, exit 0) — day 5/40 hops charged, 0 refunded today. Per the event's own
narrower contract, swept only `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/` and `inbox/` (including `inbox/requests/`),
acting on whatever is new. Mode check clean (business-os `.env` →
`MODE=active`; instance `config/config.yaml` → `mode:` empty, falls
through). Pre-pass `departments/engineering/lib/eng-gate-check.sh` (`env
ENG_ROOT=<instance> sh eng-gate-check.sh`): exit 0, clean.

**Swept all three inboxes; found nothing to act on.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` holds
exactly one file directly — `2026-08-27-eng005-g1-scope.md` — which is
`ENG-005`'s own G1, raised and notified by the `scheduled` pass earlier this
same day (see that entry below); `inbox/_handled/`'s ten items are all
already accounted for, none new. Read the gate item itself and the PRD's own
`## Decision` section
(`agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md`)
directly rather than trusting the board's characterization of it: both still
carry the unfilled template placeholder ("Filled in by the approver." / "The
approver's answer:" blank) — no decision recorded anywhere. Nothing new to
act on for `ENG-005`; it stays exactly at `awaiting-scope`, owner `approver`.

**Seventh occurrence of the already-diagnosed `.watch-seen` staleness
pattern** (`observations.md` and `proposals.md`'s open 2026-08-26 row carry
the first six; the sixth is this board's own archived entry from earlier
today). Confirmed the mechanism live rather than assuming it still applies:
`traces/.watch-seen` currently holds
`da39a3ee5e6b4b0d3255bfef95601890afd80709` — the SHA-1 of an empty input —
meaning the last `watch`-typed pass to commit a fingerprint saw all three
inboxes empty, and every non-`watch` pass since (today's `continue ENG-004`
×2 and the `scheduled` sweep) changed `inbox/`'s top-level contents without
ever being able to update it, per `commit_watch_fingerprint`'s own `[
"$EVENT" = "watch" ]` guard (`lib/eng-trigger.sh`). Exactly the fix the open
proposal already names. **Not filing a new proposal or observation** — a
seventh data point on an already-diagnosed, already-proposed issue is
corroboration, same restraint every occurrence since the fourth has applied.

**Queue backlog, unchanged from the entry above.** `traces/.pending` still
holds `1 continue ENG-004` — appended by the `ready → building` pass's own
chain fire for the combined `in-review`/`in-qa` session, queued behind this
`watch` fire only because `watch` was older in the queue (the file-watcher
fired on `inbox/2026-08-27-eng005-g1-scope.md`'s creation before that chain
fire ever ran). Not re-fired here: `continue ENG-004` was queued by its own
originating pass, and re-firing it would only duplicate a line the queue's
own dedup collapses back down.

**Dead-end sweep:** out of scope for this event beyond the inboxes it
unblocks. `ENG-004` (`building`, owner `eng-manager`) and `ENG-005`
(`awaiting-scope`, owner `approver`) both already carry valid chain records
from their own last passes, untouched here.

**Notify sweep:** nothing to raise (no gate item written this pass); nothing
to nudge (`ENG-005`'s G1 is under an hour old, no `nudged:` due); approval
cap unchanged at 1/3, not full, no stall.

No ticket was touched this pass, so no ticket log carries a chain record —
the record lives here instead, same convention every no-op `watch` entry on
this board has used. `chained: none` — nothing this pass owns to chain;
`continue ENG-004` is already queued from its own originating pass, not
re-fired. Post-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0,
clean, unchanged.

## 2026-08-27 — continue ENG-004: building-as-verification-record written per ADR-004

`continue ENG-004` event pass — the dedicated session the preceding
`designed → ready` pass chained. Narrow scope per the event contract (resume
the named ticket from its current state; no board-wide sweep). Mode check
clean (business-os `.env` → `MODE=active`; instance `config/config.yaml` →
`mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Dispatch: `ready → building`, 1 transition.** Re-verified all five
acceptance criteria fresh against disk/git in `_eng/aiorders-admin-hub` and
`_eng/aiorders-api` (`git fetch origin` in both first) rather than trusting
`designed`'s prior citations — project linkage, the absence of any
`supabase/migrations`/`functions` directory on admin-hub's `origin/main`,
both consolidation commit pairs, a fresh `sha256` re-hash of all six named
files against their new home in `aiorders-api` (all identical — a stronger
check than the design's own byte-diff), the 22-file migration count and
ordering, and a ref-level (not working-tree) confirmation that admin-hub's
local `main` is 0 ahead/0 behind `origin/main`. All five held exactly as
`designed` recorded them a day earlier — nothing drifted. `branch:` stays
empty per `ADR-004` (the diff this ticket investigated already exists on
`origin/main`, produced by the approver directly on 2026-08-24, not by this
ticket). `machine_wip` unchanged at 1/6 — both `ready` and `building` fall
inside the counted range. Full citations on the ticket's own log.

**Not proceeding into `in-review`/`in-qa` this pass, deliberately** — per
`schedules/eng_build_loop.md` step 6 those are one combined hop, and each
still owes its own independent re-derivation against disk/git per `ADR-004`
— real, distinct gate work reserved for its own session, same discipline
this ticket has applied at every earlier hop.

**Dead-end sweep (scoped to `ENG-004`):** its log now ends in a valid,
accounted-for state with a chain record below. `ENG-005` (`awaiting-scope`,
owner approver) untouched — out of scope for a `continue` event naming one
ticket.

**Notify sweep:** nothing to raise (`building` raises no gate item). Nothing
new to nudge — approval cap unchanged at 1/3 (`ENG-005`'s G1 only).

`chained: ENG-004` — sitting at `building`, owned by `eng-manager` per
`ADR-001`'s owner override as extended by `ADR-004` (agent, not the
approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-004` for the
combined `in-review`/`in-qa` session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

## 2026-08-27 — scheduled: safety-net sweep — ENG-005's G1 raised, ENG-004 left mid-chain

`scheduled` (launchd) pass — the twice-daily safety-net sweep. Mode check
clean (business-os `.env` → `MODE=active`; instance `config/config.yaml` →
`mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Business/technical intake:** `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/` and `inbox/requests/` all empty (`.gitkeep`
only) — nothing new to shape or propose.

**Gate returns:** `inbox/` holds nothing outside `_handled/` — no answered
item to act on. Cross-checked `inbox/_handled/` (ten items) against the
board and the decision journal; all already reflected.

**Merge detection:** no in-flight ticket is `blocked` on anything — no-op.

**Dispatch (priority order `now` → empty; neither in-flight ticket has a
`priority` set):** reviewed both in-flight tickets.

- `ENG-004` (`ready`, owner `eng-manager`) — left untouched, deliberately.
  Its own last log entry already chained a dedicated `continue ENG-004`
  session for the building-as-verification-record step, and
  `traces/.pending` confirms it (`1 continue ENG-004`), still undrained.
  Re-firing it here would only duplicate an already-queued line, and
  attempting `ready → building` inline would break the same discipline this
  exact hop has followed at every prior occurrence on this board — reserved
  for its own dedicated session.
- `ENG-005` (`shaped`, owner `product-manager`) — the only ticket in the
  To-do column (`intake`/`shaped`/`awaiting-scope`), so it's what this
  step's ordering picks up. Re-checked the caps fresh rather than trusting
  the board's cached header: `wip.approver_limit` (2) at 0, `wip.approval_cap`
  (3) at 0/3, both fully free. Raised its G1 —
  `inbox/2026-08-27-eng005-g1-scope.md` — framed as the fork itself rather
  than a plan to approve (wire `A4PosterGenerator.tsx` into a named surface,
  or revert `bfddffe`), matching this ticket's own PRD, which deliberately
  never proposed a direction. Advanced `shaped → awaiting-scope`, `owner`
  `product-manager → approver`. Full reasoning on the ticket's own log.

**Notify sweep.** Ran `departments/engineering/lib/eng-notify.sh raise
inbox/2026-08-27-eng005-g1-scope.md`; stamped `notified: 2026-08-27T09:59:41`
on the gate item. Reproduced the already-filed `MODE`-collision bug
(`traces/eng-notify-2026-08-27.log`: `sent: active`, not `sent: raise`) —
corroborating the open 2026-08-25 proposal, not a new finding. No nudge due
— `ENG-005`'s G1 is minutes old and nothing else is open. Approval cap
0/3 → 1/3, not full — no stall alert.

**Dead-end sweep.** `ENG-004`'s log ends in a valid, accounted-for state
with its own chain record (`continue ENG-004`, already queued, untouched
here). `ENG-005`'s log now ends in a valid state too, written this pass.
`config/exceptions.md` is empty — nothing at a third occurrence.
`proposals.md`'s five open rows are all 0–2 days old, none near the 30-day
expiry.

**One observation filed** (`observations.md`): uncommitted modifications
found in the department's own (shared, read-only-to-an-instance) tree at
this pass's start — `lib/eng-schedule.sh` and
`schedules/eng_weekly_report.md` modified, `lib/eng-report.sh` untracked.
None of the three is a file this loop reads (`eng-gate-check.sh`,
`eng-trigger.sh`, and `eng_build_loop.md` itself are all untouched), so out
of scope to act on from inside this pass; flagged since the department
directory is meant to be read-only from an instance's perspective.

**Chain.** `ENG-005` — `chained: none`, written on the ticket's own log:
sitting at `awaiting-scope`, owned by the approver. `ENG-004` — not touched
this pass, so the record lives here instead: `chained: none — continue
ENG-004` already queued from its own prior pass; re-firing here would only
duplicate a line the queue's own dedup collapses back to one, spending a
fire for no additional effect.

Approver-facing WIP 0 → 1, approval cap 0/3 → 1/3, machine WIP unchanged at
1/6. Post-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0,
clean.

## 2026-08-27 — continue ENG-004: work breakdown done, zero implementation units — advanced to ready

`continue ENG-004` event pass — the dedicated work-breakdown session the
`designed → ready` hand-off named. Narrow scope per the event contract
(resume the named ticket from its current state; no board-wide sweep). Mode
check clean (business-os `.env` → `MODE=active`; instance `config/config.yaml`
→ `mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Work breakdown: zero implementation units.** Per `ADR-003`/`ADR-004`, the
remediation this ticket investigated was already executed by the approver
directly on 2026-08-24 — nothing to sequence, nothing to assign. Advanced
`ENG-004` `designed → ready`, owner `architect → eng-manager` per
`definition-of-done.md`. `machine_wip` 0/6 → 1/6. No approver-facing WIP or
approval-cap impact — `ready` raises no gate. Full reasoning on the ticket's
own log.

**Not proceeding into `building` this pass, deliberately** — same split
`ENG-001`'s history applied at this identical hop, already flagged by this
ticket's own prior log entry: `ready → building` is reserved for its own
session.

**Dead-end sweep (scoped to `ENG-004`):** log ends in a valid state with a
chain record. `ENG-005` untouched — out of scope for a `continue` event
naming one ticket.

**Notify sweep:** nothing to raise (no gate at `ready`); nothing to nudge
(approval cap 0/3).

`chained: ENG-004` — sitting at `ready`, owned by `eng-manager` (agent, not
the approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-004` for the
building-as-verification-record session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

## 2026-08-27 — watch: swept all three inboxes again, nothing new — sixth occurrence, queue backlog sitting behind it

`watch` (launchd) pass, `traces/.pass-out.24282`: `pass start: watch (launchd)
[day 1/40 charged, 0 refunded today]`, after the queue collapsed 1 duplicate
`watch launchd` event into one. Per the event's own narrower contract, swept
only `agents/product-manager/inbox/`, `agents/eng-manager/inbox/` and
`inbox/`, plus `inbox/requests/`, acting on whatever is new. Mode check clean
(business-os `.env` → `MODE=active`; instance `config/config.yaml` → `mode:`
empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh` (`env ENG_ROOT=<instance> sh
eng-gate-check.sh`): exit 0, clean.

**Swept all three inboxes; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` itself
holds no files directly — everything that has ever landed there has already
moved to `inbox/_handled/` (ten items, spanning the original approver
requests through `ENG-003`'s G1), none new. Sixth recorded instance of a
`watch` fire finding nothing (`observations.md`'s rows, `proposals.md`'s open
row, and this board's archived/live entries carry the first five).

**Queue backlog, noted rather than freshly diagnosed.** `traces/.pending`
currently holds `1 continue ENG-004` and `1 scheduled launchd`, both still
undrained as this pass runs — today's own 09:30 safety-net sweep queued
behind an older event rather than running. Consistent with
`eng_build_loop.md`'s description of the queue (a fire drains the front only
when it reaches the lock; an idle stretch leaves whatever's queued sitting
untouched) rather than a new mechanism traced through the code this pass —
unlike the fifth occurrence's addendum, this isn't offered as a sharpened
root cause, just an honest note of what's on disk right now. Not re-fired:
`continue ENG-004` was queued by its own originating pass (`2026-08-26 —
continue ENG-004`, this board), and re-firing it here would only duplicate a
line the queue's own dedup collapses back down — same restraint every
occurrence since the fourth has applied. `scheduled launchd` is likewise left
for the next fire to drain; forcing a board-wide sweep from inside a
`watch`-scoped pass would be exactly the job this event's own narrower
contract reserves for `scheduled` itself.

**Not filing a new proposal or observation.** No new mechanism was traced
here beyond what `proposals.md`'s open row and `observations.md`'s addendum
already cover; a sixth data point on an already-diagnosed, already-proposed
issue is corroboration, same reasoning the fourth occurrence gave for
declining to refile.

**Dead-end sweep:** out of scope for this event beyond the inboxes it
unblocks. `ENG-004` (`designed`, owner `architect`) and `ENG-005` (`shaped`,
owner `product-manager`) both already carry valid chain records from their
own last passes, untouched here.

**Notify sweep:** nothing to raise (no gate item written this pass). Nothing
open to nudge — approval cap is 0/3, nothing waiting on the approver.

No ticket was touched this pass, so no ticket log carries a chain record —
the record lives here instead, same convention every no-op `watch` entry on
this board has used. `chained: none` — nothing this pass owns to chain;
`continue ENG-004` is already queued from its own originating pass, not
re-fired. Post-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0,
clean, unchanged.

## 2026-08-26 — watch: swept all three inboxes again, nothing new — fifth occurrence, a distinct mechanism from the open proposal

`watch` (launchd) pass — drained immediately behind the `decision` no-op
directly above: that pass ended 23:16:55 and this one began draining the
same second (`traces/eng-loop-2026-08-26.log`). Per the event's own narrower
contract, swept only the three watched inboxes plus `inbox/requests/`,
acting on whatever is new. Mode check clean (business-os `.env` →
`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`:
exit 0, clean.

**Swept all three inboxes; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` holds
exactly one item, `2026-08-25-eng003-g1-scope.md` — checked against its last
committed version (`git diff`), the only change is the
`nudged: 2026-08-26T15:43:45` stamp already recorded on this board's
"Waiting on the approver" list; still no `decision:`. `inbox/_handled/`
matches the board exactly (`ENG-001`'s G3, `ENG-002`'s merge request,
`ENG-004`'s G1), all already reflected in ticket state and the decision
journal. Nothing to act on.

**Root cause, read from the code rather than assumed.** Fifth recorded
`watch`-fires-for-nothing occurrence (`observations.md`'s two rows and the
open proposal's row, `proposals.md` 2026-08-26, carry the first four) — but
a different mechanism from the one that proposal diagnoses, which blames
non-`watch` event types never committing `.watch-seen`. Read
`lib/eng-trigger.sh` directly: `WATCH_FP` is computed **before the pass
launches** (line 1583), deliberately — its own comment says anything that
arrives *during* a pass must still look new to the next fire — and
`commit_watch_fingerprint` (line 424) writes that unchanged pre-launch value
to `.watch-seen` **only on a clean exit** (`if [ "$STATUS" -eq 0 ]`, line
1892-1893). The immediately-preceding `watch` pass (pid 73496, `pass end:
watch (exit 0, 669s)` at 23:08:31) exited 0 and so committed — but it had
just moved `2026-08-25-eng004-g1-scope.md` out of `inbox/` into `_handled/`
as part of processing `ENG-004`'s G1, so the fingerprint it committed
reflects `inbox/`'s state *before* that move, not after. Any `watch` pass
that actually processes a gate item modifies a watched inbox this same way,
so this isn't a one-off: it guarantees the next `watch` fire sees a diff and
relaunches for zero new work, every time a `watch` pass does real work. The
open proposal's fix ("commit after every event type") doesn't cover this —
the pass that caused it *was* `watch`-typed and *did* commit. Filed as an
addendum in `observations.md` rather than a second proposal — it sharpens
the existing one's required fix scope, it doesn't ask for a new ticket.

**Dead-end sweep:** `ENG-003` (`awaiting-scope`), `ENG-004` (`designed`) and
`ENG-005` (`shaped`) ticket logs each already end in a valid, accounted-for
state with their own chain record — none touched by this pass, none a dead
end. `traces/.pending` still holds exactly `1 continue ENG-004`, queued by
the preceding `watch` pass and not yet drained; not re-fired here, same
reasoning the preceding `decision` pass gave for the identical situation.

**Notify sweep:** nothing to raise (no gate item written this pass); no
nudge due (`ENG-003` already nudged once, 2026-08-26). Approval cap
unchanged at 1/3 — not full, no stall alert.

No ticket was touched this pass, so no ticket log carries a chain record —
same as the `decision` no-op two entries above; the record lives here
instead. `chained: none` — nothing this pass owns to chain; `continue
ENG-004` is already correctly queued from the prior pass. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean, unchanged.

## 2026-08-26 — continue ENG-004: investigation found the consolidation already done — design + ADR-003 + ADR-004 written

`continue ENG-004` event pass — the dedicated investigation-and-design
session the preceding `watch` pass chained. Narrow scope per the event
contract (resume the named ticket from its current state; no board-wide
sweep). Mode check clean (business-os `.env` → `MODE=active`; instance
`config/config.yaml` → `mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Investigated in the department's own worktrees** (`_eng/aiorders-admin-hub`,
`_eng/aiorders-api`; the human's checkouts were never touched), `git fetch`
first in both. Found both `_eng/` branches diverged from `origin/main` —
admin-hub's mildly, aiorders-api's by dozens of commits predating this
consolidation entirely — so read `origin/main` directly rather than trusting
either worktree's files (logged as an observation, see below).

**The investigation this ticket asked for turned out to already be answered.**
`aiorders-api` is authoritative: two paired same-session commits, both
2026-08-24 (`4b6a835`/`c90c02c` at ~09:52, `5b3bac2`/`919d355` at ~10:18,
seconds apart each pair) moved every migration from `aiorders-admin-hub` to
`aiorders-api` and removed admin-hub's `supabase/migrations` entirely — **the
approver did this directly, one day after filing the request, before the
ticket ever reached `shaped`.** Content-diffed all six named files
byte-for-byte against their new home: all six identical, one renamed
(UUID-suffixed filename → descriptive name), none edited — confirming the
"renamed consolidation" the architect's blind reading flagged as unruled-out
by a filename sweep. `20260312000001_restaurant_activations.sql` now sorts
before `20260408000001_google_review_history.sql` in the same repo, resolving
the replay-order hazard the original request named. The PRD's flagged "four
siblings" discrepancy is resolved too — the real count is three, matching the
three timestamps actually named. `aiorders-admin-hub`'s local `main` already
matches `origin/main` exactly (no ahead/behind), so the pending uncommitted
deletion the request opened with is resolved at the ref level. Attempted an
actual local Docker replay for extra confidence beyond the static diff;
aborted mid-image-pull as disproportionate once it was clear the static
evidence already answered the question — Docker left clean, scratch dirs
removed. Full citations (commit hashes, timestamps, diff results) on the
design doc and the ticket's own log.

**All five acceptance criteria satisfied without a diff — a second
verification-only ticket on this instance, but not `ADR-001`'s reason.**
`aiorders-admin-hub` **is** registered (L1); a diff was the right mechanism
and one happened, just not from this ticket's own `building` state. Wrote
`ADR-003` (`aiorders-api` authoritative, `decided_by: approver`, recorded
retroactively) and `ADR-004` (extends `ADR-001`'s verification-ticket pattern
across this ticket's entire remaining lane in one ADR, `decided_by:
architect`) — explicitly engaging `ADR-001`'s own Review trigger for a second
occurrence and declining both alternatives it raises (internal-lane: admin-hub
fails the lane's own no-deploy-target test on the facts; G2 on the pattern:
premature at two occurrences with different causes). `in-security` is named
explicitly as real work here, not ceremony — five of the six files under this
ticket's history are the security surface itself. No one-way door — the
ownership move is an executed fact, not a pending decision; nothing to
escalate. Tech design at
`agents/architect/designs/ENG-004-admin-hub-migration-history.md`.
`agents/architect/decisions/_index.md` updated, Next ID now `ADR-005`.

**Three observations filed** (`agents/eng-manager/observations.md`), none
folded into this ticket's scope: `_eng/aiorders-api`'s worktree divergence
from `origin/main` (a future investigation trusting that worktree's files for
this repo would be wrong); admin-hub's `supabase/config.toml` still lists 20
orphaned `[functions.*]` stanzas for functions no longer in that repo;
and this ticket's whole subject having been resolved by the approver directly
mid-flight, named in `ADR-004`'s Review trigger as a pattern worth watching
for a second occurrence.

**Not proceeding into `ready` or `building` this pass, deliberately** — same
discipline `ENG-001`'s own history applied at this exact point (each of
`shaped→designed`, `designed→ready`, `ready→building` was its own separate
pass): work breakdown and the building-as-verification-record step are real,
distinct work reserved for their own sessions, and `ADR-004` leaves whoever
picks this up next everything needed to act without re-deriving it.
`machine_wip` (6) and the approval cap are both unaffected — `designed` isn't
in the counted range, no gate item was raised.

**Dead-end sweep (scoped to `ENG-004`, the ticket this event names):** its
log now ends in a valid, accounted-for state with a chain record below.
`ENG-003` (`awaiting-scope`) and `ENG-005` (`shaped`) untouched this pass —
out of scope for a `continue` event naming one ticket.

**Notify sweep:** no gate item written this pass — nothing to raise. No nudge
due (`ENG-003` already nudged once, 2026-08-26). Approval cap unchanged at
1/3 — not full, no stall alert.

`chained: ENG-004` — `designed`'s exit condition now met (design written,
ADRs logged, no one-way door outstanding), owned by `architect` handing to
`eng-manager` for work breakdown (agent, not the approver, not blocked, not
terminal). Fired `/bin/zsh departments/engineering/lib/eng-trigger.sh continue
ENG-004`. Post-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0,
clean.

## 2026-08-26 — decision: ENG-003's G1 rejected — dropped

`decision` event pass, context `2026-08-25-eng003-g1-scope.md` — narrow scope
per the event contract (act on the answered gate item and advance only the
ticket it belongs to; no board-wide sweep). Mode check clean (business-os
`.env` → `MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`:
exit 0, clean.

**Gate return: `ENG-003`'s G1 answered — rejected.** Hand-edited directly
(frontmatter `decision:`/`decided:` set, a second `## Decision` section
appended below the still-blank original placeholder) rather than through
`lib/eng-notify.sh`'s reply channel — fourth such occurrence today,
after `ENG-002`'s GitHub merge, `ENG-001`'s G3, and `ENG-004`'s G1 (decision
journal). `decided: 2026-08-27T06:38:51.515614+00:00`
(2026-08-26T23:38:51.515614-07:00 local). Verbatim answer, the only reason
given: "Drop this ticket do not  need to be done." **First outright G1
rejection this department has recorded** — every prior G1 (`ENG-002`,
`ENG-004`) was approved as scoped.

**Advanced `ENG-003` `awaiting-scope → dropped`, owner `eng-manager` — no
other transition is available at a killed G1.** PRD `status: rejected`
(`agents/product-manager/specs/ENG-003-aiorders-env-hygiene.md`, `##
Decision` filled in). Gate item moved to
`inbox/_handled/2026-08-25-eng003-g1-scope.md` unedited. Journaled in
`agents/eng-manager/config/decision-journal.md`, including a
grounded-but-labelled-as-interpretation read: the PRD's own Problem section
already noted the tracked `.env` values are public-by-design in the shipped
bundle regardless of git tracking, so the git-hygiene fix may have read as
low-value on its own once separated from the Maps-key question it couldn't
resolve anyway — not confirmed, not asked. Flagged there as a relevant prior
data point for the still-open `restaurant-portal` `.env` proposal
(`proposals.md`, 2026-08-26 row, same fix family) whenever that batch reaches
the approver — not acted on now, since an unapproved proposal is a separate
decision on its own timeline. `depends_on`/`blocks` both empty on `ENG-003`
— no other ticket affected by the drop.

**Consequence:** approval cap 1/3 → 0/3; approver-facing WIP 1 → 0. Nothing
dispatched onto the freed capacity this pass — out of scope for a `decision`
event scoped to the one gate item it answers, same restraint prior passes
applied to the same situation.

**Notify sweep:** no gate item written this pass (one was consumed, none
raised) — nothing to `raise`. No nudge due — the only open item was this one,
now answered. Approval cap dropped, not filled — no stall alert.

**Dead-end sweep (scoped to `ENG-003`, the ticket this event names):** its
log now ends in a valid, accounted-for state (`chained: none — dropped,
terminal`), written this pass. `ENG-004` and `ENG-005` untouched, out of
scope for this event.

`chained: none` — `ENG-003` is `dropped`, a terminal state; the chaining
guard never re-fires a terminal ticket. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

## 2026-08-26 — decision: ENG-004's G1 already resolved by the preceding watch pass — no-op

`decision` event pass, context `2026-08-25-eng004-g1-scope.md` — narrow scope
per the event contract (act on the answered gate item and advance only the
ticket it belongs to; no board-wide sweep). Mode check clean (business-os
`.env` → `MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`:
exit 0, clean.

**Gate return: already handled.** The named item was gone from `inbox/`
before this pass opened it — already at `inbox/_handled/2026-08-25-eng004-g1-scope.md`,
`decision: approved`, `decided: 2026-08-27T05:57:21.472123+00:00`. Per
`traces/eng-loop-2026-08-26.log`, the immediately preceding `watch` pass drained
in the same sequence with no gap (`pass end: watch (exit 0, 669s)` →
`draining queued event: decision (2026-08-25-eng004-g1-scope.md)`, same
second) and had already found this same hand-edited gate item and fully
processed it — see the entry directly above. Verified fresh rather than
trusted from that entry: PRD `status: approved` (`agents/product-manager/specs/ENG-004-*.md`),
the decision-journal row present, the ticket at `designed` owned by
`architect`, and the board's own In-flight row already correct. All four
consistent — nothing left to act on.

**Why both fired for one edit.** The approver answered by hand-editing the
gate item file directly — third such bypass of `lib/eng-notify.sh`'s reply
channel in two days (decision journal) — which changes a file inside a
watched `inbox/`. That one edit is visible to both the poll-detected
`decision` path and the raw file-watch `watch` path, and
`schedules/eng_build_loop.md`'s queue dedup only collapses identical
`<event> <context>` lines, so `decision (2026-08-25-eng004-g1-scope.md)` and
`watch (launchd)` never recognize each other as the same work. Whichever
drains first does it; the loser — this pass — finds nothing. Logged as one
data point in `agents/eng-manager/observations.md` rather than proposed: a
first occurrence of this specific race, and distinct from the already-open
`.watch-seen` staleness proposal (that one is watch-after-non-watch; this is
decision-vs-watch on the same edit).

**Dead-end sweep (scoped to `ENG-004`, the ticket this event names):** its
log already ends in a valid, accounted-for state (`chained: ENG-004`,
written by the preceding pass) — not a dead end, nothing to resume.
`ENG-003` and `ENG-005` untouched, out of scope for this event.

**Notify sweep:** nothing to raise (no gate item written this pass); no
nudge due (`ENG-003` already nudged once, 2026-08-26). Approval cap and WIP
unchanged — no stall alert.

No ticket transition made this pass, so no new entry on `ENG-004`'s own log —
its log already ends in a correct, unbroken chain record and this pass added
no new fact beyond confirming that record still holds. Approver-facing WIP
unchanged at 1 (`ENG-003` only), approval cap unchanged at 1/3, machine WIP
unchanged at 0/6. `chained: none` — `continue ENG-004` is already queued
(`traces/.pending`: `1 watch launchd` / `1 continue ENG-004`) from the
preceding pass's own chain fire; re-firing it here would only append a
duplicate line that the queue's own dedup collapses back to one at its next
pop, spending a fire for no additional effect. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean, unchanged.

## 2026-08-26 — watch: ENG-004's G1 answered by direct file edit — handed to the architect

`watch` (launchd) pass — a file changed in a watched inbox outside the
notify/poll channel. Mode check clean (business-os `.env` → `MODE=active`).
Pre-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Swept all three watched inboxes**, per the event's own narrower contract.
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` empty
(`.gitkeep` only); `inbox/requests/` empty. `inbox/` held two items:
`2026-08-25-eng003-g1-scope.md` — read fresh, still blank, still just the
2026-08-26 nudge from a prior pass, nothing new — and
`2026-08-25-eng004-g1-scope.md` — **answered** since the last pass touched
it (the `decision` pass immediately above this entry closed `ENG-001`'s G3
only and left this item untouched).

**Gate return: `ENG-004`'s G1 approved**, `decided:
2026-08-27T05:57:21.472123+00:00` (2026-08-26T22:57:21-07:00 local), no
additional comment. Answered by directly hand-editing the gate item file —
frontmatter `decision:`/`decided:` set and a second `## Decision` section
appended below the still-blank original placeholder — rather than through
`lib/eng-notify.sh`'s reply channel; third such occurrence in two days after
`ENG-002`'s GitHub merge and `ENG-001`'s G3 (decision journal). PRD `status:
approved`; gate item moved to `inbox/_handled/` unedited, same treatment as
`ENG-001`'s G3; journaled in `agents/eng-manager/config/decision-journal.md`.

**Advanced `ENG-004` `awaiting-scope → designed`, owner `architect` —
handoff only, design work not started this pass.** `designed`'s exit
condition for this ticket is a live-database investigation (confirm
`admin-hub`'s Supabase project linkage, read the live migration ledger,
content-diff six files against `aiorders-api`'s nine), not a light design
choice — real work against a project with live operator/customer data,
same class of thing `schedules/eng_build_loop.md`'s Cadence section reserves
`building` for. Left it for a dedicated `continue ENG-004` session rather
than folding it into this narrowly-scoped `watch` pass. Full reasoning on
the ticket's own log.

**Consequence:** approval cap 2/3 → 1/3 (`ENG-003` G1 only); approver-facing
WIP 2 → 1. Not spent on anything else this pass — dispatching the freed
capacity onto another ticket (e.g. raising `ENG-005`'s G1) is left for the
next `scheduled`/`watch`/`continue` pass, same restraint the preceding
`decision` pass applied to this exact situation.

**Notify sweep:** no gate item written this pass (one was consumed, none
raised) — nothing to `raise`. No nudge due: `ENG-003` was already nudged
once, 2026-08-26, and a nudge fires at most once per item. Approval cap
dropped, not filled — no stall alert.

**Dead-end sweep (scoped to `ENG-004`, the ticket this event unblocked):**
its log now ends in a valid, accounted-for state with a chain record below.
`ENG-003` (`awaiting-scope`) and `ENG-005` (`shaped`) untouched this pass —
both already correctly waiting on the approver or the next `scheduled`/`watch`
sweep, neither a dead end.

`chained: ENG-004` — sitting at `designed`, owned by `architect` (an agent,
not the approver, not blocked, not terminal). Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-004` for
the dedicated investigation-and-design session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

## 2026-08-26 — decision: ENG-001's G3 approved — the seed ticket reaches `verified`

`decision` event pass — narrow scope per the event contract (act on the
answered gate item in `inbox/` and advance only the ticket it belongs to; no
board-wide sweep). Mode check clean (business-os `.env` → `MODE=active`).
Pre-pass `departments/engineering/lib/eng-gate-check.sh` (whole board and
`ENG-001`-scoped): exit 0, clean.

**Gate return: `ENG-001`'s G3**
(`inbox/2026-08-26-eng001-g3-verification.md`) **answered — approved**, no
additional comment, `decided: 2026-08-27T05:05:01.598404+00:00`. Per
`ADR-002`, advanced `awaiting-release → shipped → verified`, 2 transitions.
Acted as devops at `shipped`: recorded the G3 confirmation in place of a
deploy, logged on the ticket; no release record fabricated at
`agents/devops/releases/` for a deploy that never happened, per `ADR-002`'s
own instruction. Acted as product-manager at `verified`: re-confirmed all
four acceptance criteria fresh against disk (registry, worktrees, gate-check,
`ENG-002`'s own `verified` state) and re-opened all three existing receipts
(`agents/principal-engineer/reviews/ENG-001.md`,
`agents/qa/test-plans/ENG-001.md`, `agents/security/reviews/ENG-001.md`) to
confirm each still reads `pass` rather than citing the prior hop's numbers.
Full detail on the ticket's own log. Gate item moved to
`inbox/_handled/2026-08-26-eng001-g3-verification.md` unedited — the approver
filled in `## Decision` directly this time. Journaled in
`agents/eng-manager/config/decision-journal.md`.

**This closes the seed ticket.** All four acceptance criteria hold, every
lane receipt is on file and independently re-verified more than once,
`ADR-001`/`ADR-002` stay on record for the next instance's own seed ticket.
`ENG-001` is off the In-flight table, terminal.

**Consequence, not an action this pass:** approval cap drops 3/3 → 2/3
(`ENG-003`+`ENG-004` G1s only); approver-facing WIP drops 3 → 2, back at the
soft limit rather than over it. Dispatching any newly-freed capacity onto
another ticket (e.g. a G1 slot for `ENG-005`) is left for the next
`scheduled`/`watch`/`continue` pass — out of scope for a `decision` event
scoped to the one gate item it answers.

**Dead-end sweep (scoped to this ticket, per the event's own narrower
contract):** `ENG-001`'s log now ends in a valid, accounted-for state
(`chained: none — verified, terminal`). Other in-flight tickets untouched.

`chained: none` — `ENG-001` is `verified`, a terminal state; the chaining
guard never re-fires a terminal ticket. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean (whole board).

## 2026-08-26 — watch: swept all three inboxes again, nothing new — fourth occurrence of the self-inflicted no-op pattern

`watch` (launchd) pass — drained immediately behind the `scheduled`
safety-net sweep directly above: that pass ended 15:48:00 and this one began
draining the same second, after the queue collapsed 2 duplicate `watch`
events into one (`traces/eng-loop-2026-08-26.log`). Per the event's own
narrower contract, swept only `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/` and `inbox/`, acting on whatever is new. Mode
check clean (business-os `.env` → `MODE=active`). Pre-pass
`lib/eng-gate-check.sh`: exit 0, clean.

**Swept all three inboxes; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` holds
exactly the three items already on the board's "Waiting on the approver"
list, and all three are exactly as the immediately-preceding `scheduled`
pass left them seconds earlier — read fresh, not trusted from the board
header: `2026-08-26-eng001-g3-verification.md` (`## Decision` blank,
raised/notified `2026-08-26T15:43:11`), `2026-08-25-eng003-g1-scope.md` and
`2026-08-25-eng004-g1-scope.md` (both `## Decision` blank, both `nudged:
2026-08-26T15:43:45`). Nothing new to act on.

**Notify sweep:** no nudge due — `ENG-001`'s G3 is minutes old; `ENG-003`/
`ENG-004` were each nudged exactly once, seconds ago, by the pass
immediately before this one, and a nudge fires at most once per item.
Approval cap unchanged at 3/3, same composition the `scheduled` pass already
reasoned about (not a fresh stall) — no new stall alert.

**Fourth occurrence of the pattern `proposals.md` already carries a full
root-cause diagnosis for** — filed as a proposal by the `watch` pass two
entries above this one (itself the third occurrence, after two
`observations.md` rows on 2026-08-25 and 2026-08-26 10:13). Mechanism
unchanged from that proposal's own account: `commit_watch_fingerprint()` in
`lib/eng-trigger.sh` only stamps `.watch-seen` on an `$EVENT=watch` pass, so
the G3 raise and the two nudges the `scheduled` pass just wrote to `inbox/`
changed the three watched inboxes' fingerprint without updating
`.watch-seen` — guaranteeing this fire would see "something changed" and
find nothing left to do, exactly as it did. Not refiled as a new proposal or
observation: a fifth data point on an already-diagnosed, already-proposed
issue is corroboration, not a new finding, and refiling it risks the
"proposal batch becomes unreadable" failure mode `schedules/eng_build_loop.md`
step 8b warns against. Left for the approver's existing G1 batch to resolve.

No ticket was touched this pass, no ticket state changed, no gate item was
written, nothing to journal. `chained: none` — this pass advanced no
ticket, so there is no hop of its own to fire, and every in-flight ticket
(`ENG-001` awaiting-release, `ENG-003`/`ENG-004` awaiting-scope, `ENG-005`
shaped) is already correctly waiting on the approver or a WIP/approval cap,
none of which a machine can clear. Approver-facing WIP unchanged (3, still
over the 2 soft limit, still harmless per the header note), approval cap
unchanged at 3/3, machine WIP unchanged at 0/6. Post-pass
`lib/eng-gate-check.sh`: exit 0, unchanged.

## 2026-08-26 — scheduled: safety-net sweep — ENG-002's out-of-band merge reconciled, ENG-001's G3 raised, two G1s nudged

`scheduled` (launchd) pass — the twice-daily safety-net sweep. Mode check
clean (business-os `.env` → `MODE=active`; instance `config.yaml` → `mode:`
empty, falls through). Pre-pass `lib/eng-gate-check.sh`: exit 0, clean.
Confirmed this pass's own lock (`traces/.loop.lock`, pid of this chain's
`eng-trigger.sh scheduled launchd` invocation) is legitimately its own, not a
collision.

**Business/technical intake:** `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/` and `inbox/requests/` all empty — nothing new to
shape or propose.

**Gate returns / merge detection, combined — `ENG-002` found already marked
`shipped` by a direct "control center" edit, ancestry not yet consulted.**
The ticket's own log said so explicitly. Independently re-ran the loop's own
merge-detection check from scratch in the department's worktree
(`~/Documents/projects/_eng/restaurant-portal`, never the human's checkout):
`git fetch origin` → `33c5de6..b3a81ef main -> origin/main`;
`git merge-base --is-ancestor chore/ENG-002-smoke-test-harness origin/main` →
merged; `git diff` between the branch tip and `origin/main` → empty (no
intervening commits on `main`). The control center's claim held up.
`inbox/2026-08-26-eng002-merge-request.md`'s `## Decision` was never actually
filled in — the approver merged directly on GitHub instead, an alternative
the item's own text offered. Treated the merge as the answer: filled the
item's Decision with what happened, moved it to `inbox/_handled/`, and
journaled it (`agents/eng-manager/config/decision-journal.md`) — flagging
that the tracked channel was bypassed, worth watching for a repeat.

**Closed out `ENG-002` (`shipped → verified`).** Acted as devops for the
`shipped` exit condition the control-center edit had skipped: confirmed
`restaurant-portal` has no push-to-`main` CI/CD (`deploy-cf` is a manual
`wrangler pages deploy` script; no `.github/workflows/`), and this ticket's
diff (`devDependency`s + test files) never reaches Vite's build graph —
re-ran `npm run build` on the merged tree and confirmed the `dist/` output is
unchanged in shape. Nothing to deploy, so `npm run deploy-cf` was
deliberately not run. Wrote the release record from what was actually found
(`agents/devops/releases/2026-08-26-restaurant-portal-ENG-002.md`). Then
acted as product-manager: re-ran `npm test` on the merged tree (1 passed),
re-checked `config/projects.md`'s Commands table on disk (present), and
updated `agents/qa/test-plans/ENG-002.md`'s AC3 from `pending` to `pass` —
all four acceptance criteria now confirmed against the live, merged thing.
Full detail on the ticket's own log. **`ENG-002` no longer counts against the
approval cap** — the third of 3/3 is now open.

**Dispatch: `ENG-001` `ready-to-ship → awaiting-release`, 1 transition.**
With the cap at 2/3 (`ENG-003`+`ENG-004` G1s only), raising `ENG-001`'s G3 —
an already-in-flight ticket reaching its own next gate, not a new start — is
legal per the Guards section, the same reasoning `ENG-002`'s own history used
at 2/3→3/3 earlier. Wrote the G3 item per `ADR-002`'s framing (confirm the
record, not "ship to production" — nothing is being deployed) at
`inbox/2026-08-26-eng001-g3-verification.md` and raised it. Approval cap is
back to 3/3 (full) — `ENG-003`, `ENG-004`, and this G3 — a different
composition than before, not a fresh stall (the board was never observed as
anything but full/near-full by any pass boundary in between, so no new stall
alert sent; one was already sent for the ongoing episode and is the known
no-op `MODE`-collision bug). Machine WIP now 0/6 — nothing left in the
`ready`..`ready-to-ship` range.

**Notify sweep — two nudges due.** `ENG-003` (notified 2026-08-25T13:55:41)
and `ENG-004` (notified 2026-08-25T14:55:55) had both crossed the 24h
threshold as of this pass (15:43 local) — the immediately-preceding passes checked
this correctly and found both still under 24h at the time; time alone closed
the gap, which is exactly what a `scheduled` safety-net sweep exists to
catch between local events. Ran `lib/eng-notify.sh nudge` on both, stamped
`nudged:` on each by hand (the script's known `MODE`-collision bug means its
own log line reads `sent: active` rather than `sent: nudge` — reproduced
here too, corroborating the existing proposal, not a new finding).

**One proposal filed** (`proposals.md`): the general gap this pass's
`ENG-002` reconciliation exposed — a ticket's `state:` can move out from
under an open gate item via the control center, and nothing currently
cross-checks the two automatically; this pass only caught it by chance while
re-deriving `ENG-002`'s status for other reasons. Sized `S` — the check
itself (for every open gate item, confirm the ticket it names is still
actually at the state the item implies) is cheap; a repeat occurrence would
make this worth acting on.

**Dead-end sweep:** every in-flight ticket's log now ends in a valid,
accounted-for state. `ENG-001` — `chained: none`, `awaiting-release`, owner
`approver`. `ENG-002` — `chained: none`, `verified`, terminal. `ENG-003`/
`ENG-004` — unchanged, waiting on the approver, both now nudged.
`ENG-005` — unchanged, `chained: none — held by the WIP cap`
(`wip.approver_limit` 2/2, `ENG-003`+`ENG-004` still open; freeing the
approval cap doesn't free this one, since it's a distinct, smaller cap that
was already full before `ENG-002` ever blocked on it). No broken chains
found; `agents/eng-manager/config/exceptions.md` empty; nothing past the
30-day proposal expiry.

Post-pass `lib/eng-gate-check.sh`: exit 0, clean (checked after each of the
`ENG-002` and `ENG-001` edits individually, and once more for the whole
board at the end).

## 2026-08-26 — watch: swept all three inboxes, nothing new to act on

`watch` (launchd) pass — fired by the file-watcher on a change to one of the
three watched inboxes. Per the event's own narrower contract, this sweeps
`agents/product-manager/inbox/`, `agents/eng-manager/inbox/` and `inbox/`
only, acting on whatever is new; the board-wide version of dispatch/merge-
detection/dead-end-sweep is the twice-daily `scheduled` pass's job, not
this one's. Mode check clean (business-os `.env` → `MODE=active`). Pre-pass
`lib/eng-gate-check.sh`: exit 0, clean.

**Swept all three inboxes; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` itself
holds exactly the three items already on the board's "Waiting on the
approver" list, and all three still read `## Decision` / "Filled in by the
approver," unanswered — `2026-08-26-eng002-merge-request.md`,
`2026-08-25-eng003-g1-scope.md`, `2026-08-25-eng004-g1-scope.md`. The
merge-request file is the one genuinely new artifact since the last board
entry (written 11:01 by the immediately-preceding `continue ENG-002`
pass), but that same pass had already raised it (`notified:
2026-08-26T11:01:46`) and reflected it on the board — nothing was left
unprocessed for this pass to act on. Cross-checked against
`traces/.watch-seen` (fingerprint last stamped 10:20, before the file's
11:01 creation) and `traces/eng-loop-2026-08-26.log`: this `watch` fire is
that same write being independently observed by the file-watcher, not a
second, unhandled change — consistent with the fingerprint changing and
the fire not being deduplicated above the lock.

**Notify sweep:** neither `ENG-003` nor `ENG-004`'s G1 has crossed the 24h
nudge threshold (notified 2026-08-25T13:55:41 / T14:55:55, both still under
24h as of this pass). The approval cap reached 3/3 (full) during the
immediately-preceding `continue ENG-002` pass and no stall alert had been
sent for that stall, so ran `lib/eng-notify.sh stall` per step 7 — it is
still the known-broken no-op filed 2026-08-25 (`proposals.md` row 2, the
`MODE`-variable collision with the sourced business-os `.env`): logged
`no such item:` and sent nothing. Corroborating evidence for the existing
proposal, not a new finding.

**Merge detection, board-wide dispatch, and the full dead-end sweep are out
of scope for this event** — `watch` only unblocks the inbox sweep above.
Spot-checked only what bears on the one new file: `ENG-001`'s own
`continue` chain, fired by its own immediately-preceding pass, is intact
and queued at the front of `traces/.pending`, unaffected by this pass.

**One proposal filed** (`proposals.md`): this is the third occurrence of
the no-op-`watch` pattern `observations.md` flagged twice already
(2026-08-25, 2026-08-26 10:13) and explicitly deferred to a proposal "if it
recurs." Traced the actual mechanism this time, in `lib/eng-trigger.sh`:
`commit_watch_fingerprint()` and the `WATCH_FP` capture both key off
`$EVENT = "watch"` specifically, so a gate item raised by a `continue` or
`scheduled` pass changes the watched inboxes' fingerprint but never updates
`.watch-seen` — guaranteeing the next `watch` fire sees "something changed"
and spends a full pass finding nothing, exactly what happened here
(`.watch-seen` stamped 10:20; `continue ENG-002` raised its merge request
at 11:01; this pass is the predictable result). Not fixed inline — it's
department machinery, self-discovered, so `schedules/eng_build_loop.md`
step 3 routes it to the proposal list, not a drive-by patch.

No ticket was touched this pass, no ticket state changed, no gate item was
written, nothing to journal. `chained: none` — this pass advanced no
ticket, so there is no hop of its own to fire; `ENG-001`'s separately-queued
`continue` (from its own prior pass) runs next regardless, once this pass
exits. Approver-facing WIP unchanged (3, still over the 2 soft limit, still
harmless per the header note), approval cap unchanged at 3/3, machine WIP
unchanged at 1/6. Post-pass `lib/eng-gate-check.sh`: exit 0, unchanged.

## 2026-08-26 — continue ENG-001: ADR-002 resolved the release/G3 question, reached ready-to-ship, held there by the approval cap

`continue ENG-001` event pass — narrow scope per the event contract (resume
the named ticket from its current state; no board-wide sweep). Mode check
clean (business-os `.env` → `MODE=active`). Pre-pass `lib/eng-gate-check.sh`
(whole board and `ENG-001`-scoped): exit 0, clean. Fresh sweep of all three
inboxes found nothing pending for `ENG-001`.

**Resolved the boundary the immediately-preceding pass named and stopped
at.** That pass reached `in-security` with a **pass** verdict already on
record, but declined to guess what `ready-to-ship`/`awaiting-release`/
`shipped` mean for a no-deploy verification ticket, since `ADR-001`'s
Decision text names `building` through `in-security` specifically and never
further. Acting as architect, wrote `ADR-002`
(`agents/architect/decisions/ADR-002-verification-ticket-release-and-g3.md`):
a verification ticket owes every remaining full-lane state exactly as any
other ticket — `ready-to-ship`, G3, `shipped`, and `verified` are none of
them skipped or auto-routed by inventing an autonomy level `aiorders` was
never granted (re-confirmed fresh: `config/projects.md` still only the five
app repos at **L1**, `config/internal-projects` still empty). Only the
*content* of each state changes, continuing `ADR-001`'s own pattern —
`ready-to-ship` records devops confirming nothing to release; G3 asks the
approver to confirm the ticket's record rather than approve a deploy that
doesn't exist; `shipped` records that confirmation, not a fabricated
release. G3 is deliberately **not** waived or downgraded to L3's
notify-after treatment: `docs/engineering-team.md` reserves "say yes to
production" to the approver, department-wide, and unlike `building`'s empty
`branch:` field, removing a human checkpoint isn't a reversible logging
convention — see the ADR's own reasoning for why this isn't the same kind of
call `ADR-001` made. No G2 raised. `agents/architect/decisions/_index.md`
updated, Next ID now `ADR-003`.

**Dispatch: `in-security → ready-to-ship`, 1 transition.** Acted as devops
per `ADR-002`: confirmed and logged, not skipped, that no release plan,
rollback, or observability plan exists because no registered project carries
a diff for this ticket — re-verified `config/projects.md` (five rows, all
L1) and `_eng/` (all five worktrees present) fresh rather than citing the
`in-security` hop's numbers. Release window checked for consistency with
today's `ENG-002` hop even though nothing deploys: Wednesday, no
`ENG_RELEASE_FREEZE` — clean, moot either way.

**Not proceeding into `awaiting-release`.** The approval cap is **3/3
(full)** — re-checked fresh, not from this board's cached header:
`inbox/2026-08-26-eng002-merge-request.md`,
`inbox/2026-08-25-eng003-g1-scope.md`, and
`inbox/2026-08-25-eng004-g1-scope.md` all still read "Filled in by the
approver.", unanswered, and `config/config.yaml` confirms `wip.approval_cap:
3` rather than assuming the board header is current. Per the Guards section,
"at the cap, nothing advances into a gate state" — `awaiting-release` is
exactly that, so the G3 item `ADR-002` calls for is not raised this pass.

**`chained: none` — held by the approval cap (3/3, full), not by anything
left for this ticket to decide.** Unlike every earlier stop on this ticket,
this one isn't an undecided question a fresh pass could resolve: all four
acceptance criteria are satisfied, `ADR-002` has settled what every
remaining state means, and devops's own confirmation is done. Nothing
machine-ownable remains until a slot frees. Re-firing `continue ENG-001` now
would only re-derive this same conclusion at the cost of a full pass — the
chaining guard's own list names this condition directly ("held by a cap
(WIP or approvals)"). Resumes at the next `scheduled` safety-net sweep, or a
direct re-fire once the approver clears one of the other three open items.

No gate item raised this pass; nothing to notify. Machine WIP unchanged at
1/6 (`ready-to-ship` is still inside the counted `ready`..`ready-to-ship`
range). Approval cap unchanged at 3/3 — this pass created no new gate item.
**Dead-end sweep (scoped to this ticket, per the event's own narrower
contract):** `ENG-001`'s log now ends in a valid, accounted-for state
(`chained: none`, reason given). Other in-flight tickets untouched. Post-pass
`lib/eng-gate-check.sh`: exit 0, unchanged.

## 2026-08-26 — continue ENG-001: combined review+quality+security hop, stopped short of ready-to-ship

`continue ENG-001` event pass — narrow scope per the event contract (resume
the named ticket from its current state; no board-wide sweep). Mode check
clean (business-os `.env` → `MODE=active`; instance `config.yaml` → `mode:`
empty, falls through). Pre-pass `lib/eng-gate-check.sh`: exit 0, clean.
Fresh sweep of all three inboxes found nothing pending for `ENG-001`.

**Dispatch: `building → in-review → in-security`, 2 transitions.** Acted as
principal-engineer and qa on the combined review+quality hop (step 6):
independently re-derived all four acceptance criteria against disk this
round rather than citing prior numbers — `config/projects.md` (AC1),
`_eng/` worktrees plus `git rev-parse` in each to confirm they're real,
resolvable checkouts (AC2), a fresh `lib/eng-gate-check.sh` run (AC3), and
`ENG-002`'s own board file, now at `blocked` with an open PR — several
states past AC4's literal bar (AC4). Verdict **pass**;
`agents/principal-engineer/reviews/ENG-001.md` and
`agents/qa/test-plans/ENG-001.md` written, `links.review`/`links.test_plan`
set. Acted as security: threat model, full OWASP walk (all ten `n/a` — no
code, dependency, endpoint, or config surface exists), secret-scanned this
ticket's entire paper trail (one prose hit, not a credential). Verdict
**pass**; `agents/security/reviews/ENG-001.md` written, `links.security_review`
set. Full detail on the ticket's own log.

**Not proceeding into `ready-to-ship`, for two independent reasons.** What
`ready-to-ship`/`awaiting-release`/`shipped` mean for a no-deploy
verification ticket is a real open question `ADR-001` does not cover — its
Decision text names `building` through `in-security` specifically, never
further, and the design doc's brief Rollout note was never weighed as a
considered decision the way the ADR was. Improvising it here would repeat
the exact failure this ticket exists to prevent. Independently: the
approval cap is **3/3 (full)** right now — checked fresh this pass by reading each
of the three open items' `## Decision` sections directly (all still "Filled
in by the approver," unanswered) rather than trusted from this board's own
cached header — so reaching `awaiting-release` (a G3 this pseudo-project
cannot auto-route, being registered at no autonomy level) could not be
acted on regardless.

**Dead-end sweep (scoped to this ticket, per the event's own narrower
contract):** `ENG-001`'s log now ends in a valid, accounted-for state
(`chained: ENG-001`). Other in-flight tickets untouched — out of scope for a
`continue` event naming one ticket.

No gate item raised this pass; nothing to notify. Machine WIP unchanged at
1/6 (`in-security` is still inside the `ready`..`ready-to-ship` counted
range). Approval cap unchanged at 3/3 — this pass created no new gate item.
`chained: ENG-001` — sitting at `in-security`, owned by security (agent, not
approver, not blocked, not terminal); the full cap blocks the *next* hop's
gate, not this ticket's present state.

## 2026-08-26 — continue ENG-002: building finished, all three machine gates passed, PR open

`continue ENG-002` event pass — narrow scope per the event contract (resume
the named ticket from its current state; no board-wide sweep). Confirmed via
the trigger log this is exactly the dedicated continuation the safety-net
sweep directly below deferred, not a duplicate: that pass ended 10:44:34 and
this one began draining immediately after. Mode check clean (business-os
`.env` → `MODE=active`). Pre-pass `lib/eng-gate-check.sh` (whole board and
`ENG-002` scoped): exit 0, clean.

**`building → in-review → in-security → ready-to-ship → blocked`, 4
transitions (the per-ticket cap), landing exactly on the human gate.** Did
not take the prior pass's "self-tested" claim on faith: independently re-ran
`npm test` (1 passed), `npm run lint` (96 problems, identical on a clean
`origin/main` checkout via `git stash -u` — zero new), `npm run build`
(succeeds), and `npm audit` (37 vs. 39 on `main` — no new vulnerabilities);
traced the test's Supabase mock and its "Login" tab landmark through the
actual component chain rather than trusting the description. Committed the
five relevant files as `2703add`, pushed the branch. Acted as
principal-engineer (review pass, `agents/principal-engineer/reviews/ENG-002.md`)
and qa (wrote the test plan this ticket never had, `agents/qa/test-plans/ENG-002.md`,
suite green) on the combined review+quality hop; acted as security
(`agents/security/reviews/ENG-002.md`, OWASP walk mostly `n/a` for a dev-only
harness, dependency check clean); acted as devops at `ready-to-ship`
(upstream gates verified on disk, readiness held, `config/projects.md`'s
Commands table updated per the design's own assignment, window check clean —
Wednesday, no freeze). Opened the real PR
(https://github.com/harsimranwalia/restaurant-portal/pull/1) since
`restaurant-portal` is **L1**, wrote and raised the merge-request item
(`inbox/2026-08-26-eng002-merge-request.md`), landed at `blocked`,
`blocked_on: approver`. Full detail, including the approval-cap arithmetic
that justified proceeding while the board was already at 2/3, on the
ticket's own log.

**Approval cap now 3/3 (full)** — checked `config/config.yaml`'s actual
`wip.approver_limit`/`wip.awaiting_approver_cap` definitions rather than the
board header's prose: `approver_limit`'s only enforcement is blocking *new*
starts (already true at 2, still true at 3), and `awaiting_approver_cap` —
the guard `config.yaml` names explicitly for "an L1 PR waiting to be
merged" — had exactly one slot free. Machine WIP now 1/6 (`ENG-001` only).

This pass's own `lib/eng-notify.sh raise` call reproduced the already-filed
`MODE`-collision bug (`sent: active`, not `sent: raise`) — corroborating
evidence for the open 2026-08-25 proposal, not a new one.

**Dead-end sweep (scoped to this ticket, per the event's own narrower
contract):** `ENG-002`'s log now ends `chained: none` with the waiting-on-
approver reason. Other in-flight tickets untouched.

`chained: none` — `ENG-002` is `blocked`, `blocked_on: approver`. The whole
point of this hop was to reach that gate; nothing left for a machine to do
until the approver merges the PR or replies to the inbox item.

## 2026-08-26 — scheduled: safety-net sweep, board already mid-chain — nothing to dispatch

`scheduled` (launchd) pass. Mode check clean (business-os `.env` →
`MODE=active`; instance `config.yaml` → `mode:` empty, falls through).
Pre-pass `lib/eng-gate-check.sh`: exit 0, no violations.

Business intake: `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`
and `inbox/requests/` all empty — nothing new to shape or propose. Gate
returns: `ENG-003`/`ENG-004` G1s both still unanswered (`## Decision` blank
in both; notified 2026-08-25T13:55:41/T14:55:55, still under 24h as of this
pass [10:41] — no nudge due). Merge detection: no ticket `blocked` on an L1
PR, no-op.

**Dispatch — reviewed all five in-flight tickets, advanced none.** `ENG-001`
and `ENG-002` are both already mid-chain from the two dedicated `continue`
passes that ran in the hour before this one (`ENG-001` `ready→building` at
10:20–10:33; `ENG-002`'s uncommitted `building` work found and corrected at
09:56). Each ticket's own chain is already queued: `cat traces/.pending`
shows `continue ENG-002` then `continue ENG-001`, both appended by those
passes themselves, not by this one. Re-firing either here would duplicate an
already-queued line and, since this pass's own parent `eng-trigger.sh
scheduled launchd` (pid 37779, alive since 09:30) holds `traces/.loop.lock`
throughout, would contend a lock its own ancestor holds — the exact
situation two earlier passes today already hit and correctly avoided. Left
both untouched. `ENG-003`/`ENG-004` stay `awaiting-scope` — approver WIP
2/2 (full), both G1s unanswered. `ENG-005` stays `shaped`, held by the same
cap — no slot freed this pass.

**Notify sweep:** no gate item raised this pass, nothing to notify; neither
`ENG-003` nor `ENG-004` has crossed the 24h nudge threshold yet; approval cap
is 2/3, not full, so no stall alert.

**Dead-end sweep:** every in-flight ticket's log ends in a valid,
accounted-for state (`chained: <id>` or `chained: none — <reason>`); no
broken chain. `agents/eng-manager/config/exceptions.md` is empty (nothing at
a third occurrence); `proposals.md`'s three open items and
`observations.md`'s ledger are all within days of filing, none past the
30-day proposal expiry.

Approver-facing WIP unchanged at 2/2 (full), approval cap 2/3, machine WIP
unchanged at 2/6. `chained: none` on all five tickets — `ENG-001`/`ENG-002`
because a dedicated continuation is already queued for each (see above);
`ENG-003`/`ENG-004` because they wait on the approver; `ENG-005` because it's
held by the approver-WIP cap. Post-pass `lib/eng-gate-check.sh`: exit 0,
unchanged.

## 2026-08-26 — continue ENG-001: building-as-verification record written

`continue ENG-001` event pass — narrow scope per the event contract (resume
the named ticket from its current state; no board-wide sweep). Mode check
clean (business-os `.env` → `MODE=active`; instance `config.yaml` → `mode:`
empty, falls through). Confirmed no pending gate item for `ENG-001` in any of
the three inboxes before dispatching — none exists; its last judgement call
(what `building`/receipts mean for a diffless ticket) was decided directly by
the architect via ADR-001, no approver gate raised. Merge detection:
`ENG-001` carries no branch, no-op.

**Dispatch:** `ENG-001` advanced `ready → building` — the
building-as-verification-record step ADR-001 defines. Re-verified all four
acceptance criteria against disk rather than trusting prior citations: AC1
(`config/projects.md`, five rows, all **L1**), AC2 (`_eng/` worktrees, all
five present), AC3 (`lib/eng-gate-check.sh` re-run, exit 0), AC4 (`ENG-002`
now at `building`, already past `shaped`). Full citations on the ticket's
own log. `branch:` stays empty per ADR-001; `machine_wip` (6) unchanged at
2/6 (`ENG-001`, `ENG-002` — both already inside the counted range). **Not
proceeding into `in-review` this pass, deliberately** — the
principal-engineer/QA review of the verification claims is real, distinct
gate work reserved for its own session, same reasoning applied at every
earlier hop on this ticket. `chained: ENG-001`.

**Dead-end sweep (scoped to this ticket, per the event's own narrower
contract):** `ENG-001`'s log now ends in a valid, accounted-for state
(`chained: ENG-001`). Other in-flight tickets untouched — out of scope for a
`continue` event naming one ticket.

No gate item raised this pass; nothing to notify; nothing new to observe or
propose.

## 2026-08-26 — scheduled: safety-net sweep, ENG-002's building state corrected

`scheduled` (launchd) pass — twice-daily safety-net sweep, drained
immediately behind this morning's `continue ENG-002` build hop under the
same lock (pid 37779, 09:30 launchd fire). Mode check clean (business-os
`.env` → `MODE=active`; this instance's own `config.yaml` → `mode:` empty,
falls through). Business intake: `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/` and `inbox/requests/` all empty — nothing new to
shape or propose. Gate returns: `ENG-003`/`ENG-004` G1s both still
unanswered (`## Decision` blank in both inbox items; notified
2026-08-25T13:55/14:55, both under 24h as of this pass — no nudge due yet).
Merge detection: no ticket `blocked` on an L1 PR, no-op.

**Dispatch (priority order `now` → empty):** `ENG-001` reviewed and left
unchanged — still `ready`, its `continue` already queued
(`traces/.pending`) from an earlier pass, nothing to redo. `ENG-002`
reviewed and found mid-flight: the `continue ENG-002` hop that ran
09:36–09:56 just before this pass implemented the smoke test for real
(Vitest + RTL, per the architect's design) but stopped itself uncommitted,
citing a suspected concurrent instance of this automation — which this pass
independently re-checked via `ps` and the lock file and found to be false
(pid 37779 is this exact chain's own orchestrator; no other process
touches this instance or the `restaurant-portal` worktree). Full forensics
on that ticket's own log. Corrected the board to `state: building` and
`branch: chore/ENG-002-smoke-test-harness` to match the real, verified,
on-disk work; left the worktree exactly as found per `config/projects.md`'s
own rule against touching a previous pass's uncommitted state; filed the
`.env`-tracked finding that pass discovered but didn't get to
(`proposals.md`); did not commit/push/finish the build myself — that stays
reserved for a dedicated `continue` session, same reasoning already applied
to every other `ready`→`building` transition on this board. `ENG-003`/
`ENG-004` stay `awaiting-scope` (approver WIP 2/2, both gates unanswered);
`ENG-005` stays `shaped`, held by the same cap — no slot freed this pass.

**Dead-end sweep:** every in-flight ticket's log ends in a valid,
accounted-for state (`chained: <id>` or `chained: none — <reason>`) —
`ENG-002`'s is the one this pass brought current; `ENG-001`, `ENG-003`,
`ENG-004`, `ENG-005` were already correct and untouched. One observation
filed (`observations.md`): a second occurrence of the `scheduled`-event-
with-a-ticket-path-context oddity first seen 2026-08-25, with a correction
to that earlier note — it does charge a ticket's hop counter (`ENG-001`
this time), not ticket-less as previously assumed.

Approver-facing WIP unchanged at 2/2 (full), approval cap 2/3, machine WIP
unchanged at 2/6. `chained: ENG-002` (fired `/bin/zsh eng-trigger.sh
continue ENG-002` — queued behind this pass's own lock, next drain runs
it). `ENG-001`/`ENG-003`/`ENG-004`/`ENG-005`: `chained: none`, all for
reasons unchanged from their own last log entries.

## 2026-08-25 — continue ENG-001: architect resolved the building/receipts gap

`continue ENG-001` pass — the dedicated hop chained by the earlier PM-shaping
pass; the intervening `scheduled (manual-unblock)` sweep and its retry (both
below/archived) deliberately left this ticket alone because this `continue`
was already queued for it.

Architect resolved the question the PM pass raised: what `building` and the
three full-lane receipts mean for a ticket with no application-code
deliverable. Wrote `ADR-001`
(`agents/architect/decisions/ADR-001-verification-ticket-building-and-receipts.md`)
and a short tech design
(`agents/architect/designs/ENG-001-register-repos-and-prove-the-loop.md`): a
**verification ticket** — every acceptance criterion satisfied with no diff
in any registered project — still owes every state and every receipt its
lane specifies, but `building` records what was checked instead of a
branch/PR. Considered and rejected registering `aiorders` in
`config/internal-projects` (reserved to the approver by that file's own
header, and premature for what's expected to be a one-time ticket) and
delegating via `parent:` to `ENG-002` (would misrepresent its real,
independent provenance). No one-way door; decided directly, no G2, no
approver touch — `ENG-003`/`ENG-004` keep both approver-WIP slots
undisturbed.

**Dispatch:** `ENG-001` advanced `shaped → designed → ready`. EM work
breakdown found zero implementation units (no code in any registered
project), so nothing to sequence; `machine_wip` (6) now 2/6 (`ENG-002`,
`ENG-001`). **Stopped before `building`, deliberately** — writing the three
receipts against the verification evidence is real, distinct gate work that
`schedules/eng_build_loop.md` reserves for its own session, same reasoning as
`ENG-002` earlier today. `chained: ENG-001`.

**Merge detection:** no ticket is `blocked` on an L1 PR. No-op.

**Dead-end sweep:** every in-flight ticket's log ends in a valid,
accounted-for state (`chained: <id>` or `chained: none — <reason>`); no
broken chain found.

## 2026-08-25 — scheduled (manual-unblock), retry: ENG-002 gate processed, ENG-004 G1 raised

**This pass is the retry (attempt 2/2) of the `scheduled (manual-unblock)`
event below** — the first attempt timed out at the 1800s pass ceiling while
finishing the board-index edit for the entry directly below this one (see
`traces/eng-loop-2026-08-25.log`: `pass TIMED OUT after 1800s`, re-queued as
attempt 2/2). Before doing anything new, verified the first attempt's
substantive work — `ENG-003`/`ENG-004`/`ENG-005` shaped, `ENG-003`'s G1
raised, two proposals and three observations filed — was complete and
internally consistent on disk; the only gap found was this table missing rows
for the three new tickets, now fixed. Filed one further observation on the
timeout itself (`agents/eng-manager/observations.md`).

**Gate returns:** `ENG-002`'s G1 was answered — **approved**, no additional
comment — while this retry was starting (`decided: 2026-08-25T21:43:57Z`).
Processed it: gate item moved to `inbox/_handled/`, PRD `status: approved`,
entry added to `agents/eng-manager/config/decision-journal.md`. A dedicated
`decision 2026-08-25-eng002-g1-scope.md` event is separately queued
(`traces/.pending`) from the control center's own fire — when it eventually
drains it will find the gate already resolved and be a harmless no-op.
`ENG-003`'s G1 remains unanswered; left as-is.

**Dispatch:** `ENG-001` left alone, same reasoning as the pass below — its
`continue` is still independently queued (`traces/.pending`), so re-opening
the architect's deferred judgement call here would race a pass already
in flight for it. `ENG-002` advanced `awaiting-scope → designed → ready`:
architect design written
(`agents/architect/designs/ENG-002-restaurant-portal-smoke-test-harness.md`
— Vitest + React Testing Library, one smoke test on the real app entry
point; no one-way door, no ADR, no G2); EM sequencing found a single unit of
work and `machine_wip` (6) at 0/6 going in. **Stopped before `building`,
deliberately** — this pass is a recovery/sweep context, not the clean session
`schedules/eng_build_loop.md` reserves for "an engineer writing code," so the
actual implementation is left for a dedicated `continue` hop. `chained:
ENG-002`.

Resolving `ENG-002`'s gate freed the `wip.approver_limit` (2) slot it had
been holding alongside `ENG-003`. Took the freed slot for `ENG-004` over
`ENG-005` — both still `shaped` with no `priority` set, so severity is the
tie-break (`P2` vs `P3`), per `config/definition-of-done.md`. `ENG-004`'s G1
raised and notified; PRD `status: awaiting-scope`. `ENG-005` holds at
`shaped` — approver WIP is 2/2 (full) again with `ENG-003` + `ENG-004`.

**Merge detection:** no ticket is `blocked` on an L1 PR. No-op.

**Dead-end sweep:** every in-flight ticket's log ends in a valid, accounted-for
state (`chained: <id>` or `chained: none — <reason>`); no broken chain found.

## 2026-08-25 — scheduled (manual-unblock), attempt 1: swept the three unshaped requests

`scheduled (manual-unblock)` pass — the safety-net sweep queued behind the
`continue ENG-001` pass earlier today. Per the event's own scope ("sweep the
whole board: everything a local event cannot see"), left `ENG-001` alone —
its `continue` was already queued (`traces/.pending`) from that earlier
pass's own chain, so redoing its architect-judgement question here would
have raced a pass already in flight for it. Confirmed nothing is `blocked`
on an L1 PR (merge detection: no-op this pass) and no ticket's chain
silently broke (`ENG-001`'s and `ENG-002`'s logs both end in a valid,
accounted-for state).

Business intake: found and shaped all three approver-filed requests that had
sat unprocessed in `inbox/requests/` since 2026-08-23 (flagged as an
observation by the prior pass). Ran the full request-readback on each — this
PM's reading plus a blind architect reading via an independent subagent per
request, so the second reading genuinely couldn't see the first. No material
divergence on any of the three; all three architect readings sharpened the
technical picture without disagreeing on scope or problem — see each
ticket's PRD.

- **ENG-003** (`aiorders-env-hygiene`, `config-site-builder`, size M, P2) —
  shaped straight through to `awaiting-scope`. `wip.approver_limit` (2) had
  exactly one free slot (`ENG-002` held the other); this one took it, on
  severity grounds — an ongoing, possibly-live cost exposure (an
  unrestricted Google Maps key) outranks the other two's own "nothing here
  is urgent" framing. G1 raised and notified.
- **ENG-004** (`admin-hub-migration-history`, `aiorders-admin-hub`, size L,
  P2) — shaped to `shaped`, PRD complete, G1 held for the next free slot.
- **ENG-005** (`a4-poster-generator-decision`, `aiorders-admin-hub`, size S,
  P3) — shaped to `shaped`, PRD complete, G1 held for the next free slot. G1
  will be required despite `S`+`chore` auto-skip eligibility — the ticket's
  scope is an unresolved approver decision, not routine work; see its own
  log.

All three source requests moved to `inbox/_handled/`. Two items filed rather
than fixed: a proposal (`agents/eng-manager/proposals.md`) that
`lib/eng-notify.sh` has two real bugs — no channel dispatch (posts to Slack
regardless of this instance's `approver.notify: telegram`), and a `MODE`
variable collision with the sourced business-os `.env` that silently breaks
the `stall` alert and the `nudge` prefix (confirmed live: this pass's own
`raise` call logged `sent: active`, not `sent: raise`); and two observations
(`agents/eng-manager/observations.md`) — a ticket-schema gap (`project:`/
`branch:` are singular, `ENG-003` genuinely spans three repos) and a
registry gap (`config/projects.md` doesn't record which Supabase project
`aiorders-admin-hub` is linked to, which `ENG-004` needs to answer).

Approver-facing WIP now 2/2 (full), approval cap 2/3. `chained: none` on all
three new tickets — `ENG-003` waits on the approver, `ENG-004`/`ENG-005`
wait on a WIP slot freeing; see each ticket's log for the reasoning.

## 2026-08-25 — continue ENG-001: PM shaping + ENG-002 opened

`continue ENG-001` pass. Shaped `ENG-001` (`intake → shaped`): wrote its PRD,
re-confirmed AC1 (five repos registered at L1, approved 2026-07-28,
re-verified 2026-08-23), AC2 (all five worktrees present under `_eng/`), and
AC3 (`lib/eng-gate-check.sh` exit 0) as already satisfied.  `type: chore`
auto-skips G1, so no gate item for `ENG-001` itself.

AC4 (one real ticket to `shaped`) was still open. Found a genuine, already-filed
approver request sitting unprocessed in `inbox/requests/` since 2026-08-23
(`2026-08-23-test-harness.md`) — not a self-originated finding, so shaping it
didn't touch the department's-own-work rule (`schedules/eng_build_loop.md`
step 3). Ran the full request-readback on it (this PM's reading + a blind
architect reading, no material divergence) and shaped it into `ENG-002`
(`intake → shaped → awaiting-scope`) — a smoke-test harness for
`restaurant-portal`, since none of the five AIOrders repos has a single test
and the QA gate is currently unable to prove anything ran. `size: M`, so
(unlike `ENG-001`) **G1 is required** — item raised and notified, see
"Waiting on the approver" above. `ENG-001`'s AC4 is satisfied by `ENG-002`
having reached `shaped` en route to `awaiting-scope`.

Did not push `ENG-001` past `shaped` this pass — what "building" means for a
ticket with no application-code deliverable (config/registry verification,
another ticket) isn't addressed anywhere in the department's docs, and a
snap judgement call on that shouldn't be buried in a PM pass. Left for the
architect on the next `continue`. `chained: ENG-001`.

Two things filed rather than fixed in this pass: a proposal
(`agents/eng-manager/proposals.md`) noting `agents/critic/agent.md` doesn't
exist on this instance or the department template, though
`skills/prd-writer/SKILL.md` step 8b calls for it before every G1 (ENG-002's
G1 went out with no `## Dissent` as a result); and an observation
(`agents/eng-manager/observations.md`) that three other approver requests in
`inbox/requests/` (`a4-poster-generator-unwired`, `admin-hub-migration-history`,
`aiorders-env-hygiene`) are still unshaped, out of scope for this
ticket-scoped pass. The `scheduled manual-unblock` event already queued
behind this one should sweep them.

## 2026-08-24 — decision: gate-check-unavailable resolved

Acted on the answered incident gate `2026-08-24-eng-gate-check-unavailable.md`
(`gate: incident`, tied to ENG-001 because it was the ticket in flight when the
pre-pass check found `lib/eng-gate-check.sh` unreadable). Its `project: life-os`
was stale — a leftover of the pre-carve-out hardcoding bug fixed in business-os
`ed8dd56`/`58ae148`/`9366b84`; `ticket: ENG-001` was correct. Approver had
already recorded `decision: approved`. Independently re-ran
`lib/eng-gate-check.sh` against this instance this pass: exit 0, clean — ENG-001
AC3 satisfied. Logged on ENG-001, moved the gate item to `inbox/_handled/`.
Did not shape ENG-001 further — a decision pass is scoped to the gate it
answers, not PM intake work — so `chained: ENG-001` to hand the ticket to a
fresh `continue` pass.
