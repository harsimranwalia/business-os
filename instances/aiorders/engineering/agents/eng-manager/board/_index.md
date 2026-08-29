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

