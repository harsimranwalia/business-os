# Board

**Next ID: ENG-007** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.)

**Machine WIP 6** (`config/config.yaml` → `wip.machine_limit`) — counts states
`ready` through `ready-to-ship`. **Currently 0/6** — `ENG-006` left this range
this pass, moving `ready-to-ship → blocked` once its L1 PR opened; no other
ticket is in flight.
**Approver-facing WIP 2 — currently 1/2** — `ENG-006`'s L1 merge request,
opened this pass, waiting on a human merge.
**Approval cap 3 — currently 1/3** — same item. `ENG-001`'s G3, `ENG-002`'s
merge request, `ENG-003`'s G1, `ENG-004`'s G1 **and** G3, `ENG-005`'s G1 —
fork, surface follow-up — **and** its merge request, and `ENG-006`'s G1
**and** G2 are all already answered and off the board.

`priority:` is a field on every ticket, and **only the approver sets it.** It is
not `severity`, which is the agent's read of how bad a problem is.

## In flight

| ID | Title | Project | State | Priority | Owner | Size | Updated |
|---|---|---|---|---|---|---|---|
| ENG-006 | Introduce a unified cross-restaurant customer identity with phone/OTP auth and legacy-customer mapping | aiorders-api | blocked (blocked_on: approver) | (empty) | approver | L | 2026-08-28 |

`ENG-002` shipped and reached `verified` in an earlier pass today — off the
In-flight table (terminal); see its own board file. `ENG-001` — this
instance's seed ticket — reached `verified` in an earlier pass today, its G3
answered **approved**; off the In-flight table (terminal); see its own board
file. `ENG-003` — its G1 answered **rejected** in an earlier pass today —
reached `dropped`; off the In-flight table (terminal); see its own board
file. `ENG-004` — its `ready-to-ship` confirmation and G3 were both raised
and answered **approved** in an earlier pass — reached `verified`; off the
In-flight table (terminal); see its own board file and the dated entry now
in `_index-archive.md` (rolled this pass, per the keep-three rule). `ENG-005`
— its L1 merge request answered **merged**, independently confirmed by git
ancestry — reached `verified`; off the In-flight table (terminal); see its
own board file and `agents/devops/releases/2026-08-28-aiorders-admin-hub-ENG-005.md`.

## Waiting on the approver

Cap: 3 across all gates. **Currently 1/3.** `ENG-006`'s L1 merge request
(`inbox/2026-08-28-eng006-merge-request.md`) — PR opened, waiting for a
human merge.

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

