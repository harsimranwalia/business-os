# Engineering Board — pass log archive

Dated pass entries moved out of `_index.md` once the live board holds more than
three, newest first. The live board keeps its table plus enough recent narrative
to resume a ticket; everything older lives here.

Nothing reads this file on a pass — it is the department's history, not its
state. `lib/eng-gate-check.sh` globs `ENG-*.md` and never sees it.

This exists because every pass reads `_index.md` in full, so an append-only log
there is a tax on every future pass.

---

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
