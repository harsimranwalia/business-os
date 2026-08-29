# Board

**Next ID: ENG-007** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.)

**Machine WIP 6** (`config/config.yaml` → `wip.machine_limit`) — counts states
`ready` through `ready-to-ship`. **Currently 0/6** — no ticket is in flight;
`ENG-006` reached `verified` this pass.
**Approver-facing WIP 2 — currently 0/2** — nothing waiting on a human.
**Approval cap 3 — currently 0/3** — `ENG-001`'s G3, `ENG-002`'s merge
request, `ENG-003`'s G1, `ENG-004`'s G1 **and** G3, `ENG-005`'s G1 — fork,
surface follow-up — **and** its merge request, and `ENG-006`'s G1, G2,
**and** merge request are all already answered and off the board.

`priority:` is a field on every ticket, and **only the approver sets it.** It is
not `severity`, which is the agent's read of how bad a problem is.

## In flight

| ID | Title | Project | State | Priority | Owner | Size | Updated |
|---|---|---|---|---|---|---|---|
| *(none — all six tickets are terminal)* | | | | | | | |

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
`ENG-006` — a control-center dashboard action advanced `blocked → shipped`
ahead of this pass; its L1 merge request answered **approved** and
independently confirmed by git ancestry, then this pass carried it
`shipped → verified` — off the In-flight table (terminal); see its own board
file and `agents/devops/releases/2026-08-28-aiorders-api-ENG-006.md`.

## Waiting on the approver

Cap: 3 across all gates. **Currently 0/3.** Nothing waiting — `ENG-006`'s L1
merge request was answered and independently confirmed this pass; see the
dated entry below.

## 2026-08-28 — continue ENG-006: fired externally against an already-terminal ticket — no-op

`continue` event pass, context `ENG-006`. Per the event's own contract
(resume the named ticket from its current state), scoped to this ticket
only — no board-wide sweep. Mode check clean (business-os `.env` →
`MODE=active`; instance `config/config.yaml` → `mode:` empty, falls
through). Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-006`) and whole-board: both exit 0, clean.

**Nothing to resume.** `ENG-006` has been `state: verified` — terminal —
since the `decision` pass at 20:12:38, confirmed independently twice more
since (the `watch` and `scheduled` passes immediately below). Re-confirmed
fresh rather than trusted from the board's own account: the ticket's own
frontmatter and log, this file's header/In-flight table, and
`decision-journal.md` (all three of its gates — G1, G2, L1 merge — already
journaled) all agree. `traces/.pending` empty; all three watched inboxes
hold only `.gitkeep` and the already-notified, non-P0
`2026-08-28-eng-events-dropped.md`. Nothing anywhere for a machine to act on.

**This fire does not fit the instance's well-documented duplicate-queued-event
race** (`observations.md`, eleven-plus prior rows) — that pattern is always
two events the loop itself legitimately queued for the same underlying
change, racing each other. This one doesn't: `traces/eng-loop-2026-08-28.log`
shows no `continue — queued as pending` line and no pass since the
`ready-to-ship → blocked` transition (14:38:21, its own chain already
consumed) ever recording `chained: ENG-006` — the `decision`, `watch`, and
`scheduled` passes since all correctly logged `chained: none`. This fire
lands at 21:02:49, 27 minutes after the `scheduled` pass's own `pass end`
line, with nothing queued between them — meaning it reached the lock and
drained its own freshly-appended line, not an older one left waiting. That
shape means the fire itself came from outside the loop's own chain
mechanism — a direct invocation of `eng-trigger.sh continue ENG-006` — not
from two internally-queued events racing. Filed as its own,
differently-shaped observation rather than folded into the existing race
count.

**A concrete, plausible source surfaced mid-pass, while re-checking the
working tree.** Commit `3c3dcd0` ("ENG-006: verify against production —
migration and function confirmed deployed") landed at
2026-08-28T21:09:07-07:00, authored by Harsimran — inside this pass's own
window. Its message: the approver ran `supabase db push` and `supabase
functions deploy platform-customer-auth` directly against production,
confirmed by CLI output, and updated the release record's `environment`/
`health_check` frontmatter accordingly — all "outside this department's own
L1 workflow, which still only opens PRs." That's a plausible source for an
external trigger fire landing on this exact ticket in this exact window,
though nothing ties the commit to the fire directly (no log line names a
cause), so it's recorded as circumstantial, not confirmed. Checking that
commit's diff also surfaced a second thing, unrelated to the fire itself:
its frontmatter update to `agents/devops/releases/2026-08-28-aiorders-api-ENG-006.md`
wasn't matched by an update to that file's own prose body, which still reads
the opposite (`## Deploy`/`## Health note`: "not established that a live
Supabase deploy has happened yet"). Not fixed here — see the observation
below for why.

**0 transitions.** No cap affected — machine WIP 0/6, approver WIP 0/2,
approval cap 0/3, all unchanged; `ENG-006` sits outside every counted range.

**Dead-end sweep (scoped to this event):** `ENG-006`'s own log already ended
in a valid, terminal, accounted-for state before this pass started, and this
pass added one line confirming that rather than reopening it. No other
ticket is in flight to check.

**Notify sweep:** nothing to raise, nothing to nudge. Approval cap 0/3 — no
stall.

**Observation filed** (`observations.md`) — this fire's shape, distinct from
the duplicate-event race.

No ticket state changed, no gate item was written. `chained: none` —
`verified` is terminal; firing `continue ENG-006` again would just repeat
this same no-op. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-006`) and whole-board: both exit 0, clean.

## 2026-08-28 — scheduled (launchd): safety-net sweep — board fully terminal, nothing to act on

`scheduled` event pass, context `launchd`, the four-times-daily safety net
(20:30 firing). `traces/eng-loop-2026-08-28.log`: queued behind the `watch`
pass that ended at 20:24:32 (exit 0, 714s); this fire drained at 20:30:05 —
the scheduled calendar time itself, not an immediate queue-drain artifact.
Mode check clean (business-os `.env` → `MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (this event
names no ticket to scope to): exit 0, clean — run fresh myself, not taken on
the preceding passes' own recorded claim.

**Found the working tree already carrying the preceding `decision
ENG-006` + `watch` passes' edits, uncommitted.** Verified rather than
trusted before relying on any of it: independently re-ran the whole-board
gate-check (above); independently grepped every board file's own
`state`/`owner`/`blocked_on` frontmatter directly rather than reading the
index's summary (`ENG-001`, `ENG-002`, `ENG-004`, `ENG-005`, `ENG-006` all
`state: verified`; `ENG-003` `state: dropped`; none `blocked_on` anything);
independently grepped every ticket log's last `chained:` line (all six read
`chained: none`) — no broken chain anywhere on the board. `lib/eng-env.sh:14`
confirms committing this bookkeeping repo is "a deliberate git commit
against business-os, not something a run does," matching this instance's
already-established convention (the immediately preceding passes' own
entries) — left the tree uncommitted, did not commit on this pass's behalf.

**Business intake:** `agents/product-manager/inbox/` and `inbox/requests/`
hold only `.gitkeep`. Nothing to shape.

**Technical intake:** `agents/eng-manager/inbox/` holds only `.gitkeep`.
Nothing to batch into `proposals.md`.

**Gate returns:** `inbox/` holds exactly one live item,
`2026-08-28-eng-events-dropped.md` — read fresh: still no `decision:` field,
still not P0, still no `notified:` stamp (the earlier raise attempt failed on
the already-filed `MODE`-collision bug, not compelling a retry for a non-P0
item). Nothing new, nothing to act on. `2026-08-28-eng006-merge-request.md`
is no longer live — already moved to `_handled/` by the preceding `decision`
pass.

**Merge detection:** no ticket is `blocked` on an L1 PR — all six terminal
(confirmed above). Nothing to check.

**Dispatch:** To-do (`intake`/`shaped`/`awaiting-scope`) is empty; no free
slot to fill regardless (machine WIP 0/6).

**Dead-end sweep:** all six ticket logs end in a valid, accounted-for
terminal state with `chained: none` on record (confirmed above). No ticket
without an owner. No broken chain.

**Notify sweep:** nothing to raise, nothing to nudge (one nudge is the limit
and the events-dropped item never even got a first successful notify —
out of this pass's scope, already a corroborated open proposal), no stall
(approval cap 0/3, not full).

**Observations/exceptions/journal:** nothing new — no gate answered this
pass, no exception request open on any (terminal) ticket log.

No ticket was touched, no ticket state changed, no gate item was written.
`chained: none` — this pass advanced no ticket, so there is no hop of its
own to fire. All WIP/approval-cap figures unchanged (0/6, 0/2, 0/3). Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

## 2026-08-28 — watch: swept all three inboxes, nothing new — board already fully terminal

`watch` event pass, context `launchd`. Per the event's own narrower contract,
swept `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`, and
`inbox/` (including `inbox/requests/`) only — not a board-wide sweep. Mode
check clean (business-os `.env` → `MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (this event
names no ticket to scope to): exit 0, clean.

**Drained immediately behind the `decision ENG-006` pass directly below, in
the same lock hold, not a separate concurrent invocation.**
`traces/eng-loop-2026-08-28.log`: that pass ended at 20:12:38 (785s, exit
0), the queue then collapsed 2 duplicate event(s), and this `watch` fire was
drained next and launched in the same breath. Verified rather than assumed:
process ancestry (`traces/.loop.lock`, pid 33561, `eng-trigger.sh decision
...`) traces to this session's own `claude` process via `lib/run-claude.sh`
— the same wrapper invocation working through its queue, not a second live
pass touching the same files.

**Swept all three inboxes fresh; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
`.gitkeep` (plus the former's already-`_handled/` entries); `inbox/requests/`
is empty. `inbox/` holds exactly one live item,
`2026-08-28-eng-events-dropped.md` — read directly: still no `decision:`
field, still not P0, already notified once (10:42:17), and already fully
accounted for both in `ENG-006`'s own ticket log and the immediately
preceding `decision` pass's addendum. `2026-08-28-eng006-merge-request.md`
is no longer a live inbox item at all — that same preceding pass closed it
out and moved it to `_handled/`. Nothing new anywhere.

**Board already fully terminal by the time this pass ran** — confirmed
against the header the preceding pass already updated, not re-derived:
`ENG-001`–`ENG-006` all terminal (`verified` ×5, `dropped` ×1); machine WIP
0/6, approver-facing WIP 0/2, approval cap 0/3. No ticket to dispatch, no
free slot to fill from an empty To-do regardless.

**Dead-end sweep:** nothing beyond the inboxes to check — no ticket in
flight, so no chain to verify.

**Notify sweep:** nothing to raise, nothing to nudge, approval cap 0/3 —
no stall.

**Nothing to journal** — no gate was answered this pass.

No ticket was touched, no ticket state changed, no gate item was written.
`chained: none` — this pass advanced no ticket, so there is no hop of its
own to fire. All WIP/approval-cap figures unchanged. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

