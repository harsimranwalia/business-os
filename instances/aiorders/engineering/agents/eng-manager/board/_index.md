# Board

**Next ID: ENG-006** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.)

**Machine WIP 6** (`config/config.yaml` → `wip.machine_limit`) — counts states
`ready` through `ready-to-ship`. **Currently 0/6.**
**Approver-facing WIP 2 — currently 0** (`ENG-003`'s G1 answered — rejected —
this pass; `ENG-004` already past its own G1, sitting at `designed` under the
architect). **Approval cap 3 — currently 0/3** (`ENG-001`'s G3, `ENG-002`'s
merge request, and `ENG-004`'s G1 were already answered and off the board;
`ENG-003`'s G1 is now answered too — nothing open).

`priority:` is a field on every ticket, and **only the approver sets it.** It is
not `severity`, which is the agent's read of how bad a problem is.

## In flight

| ID | Title | Project | State | Priority | Owner | Size | Updated |
|---|---|---|---|---|---|---|---|
| ENG-004 | Reconcile aiorders-admin-hub's deleted-but-uncommitted migration history | aiorders-admin-hub | designed | (empty) | architect | L | 2026-08-26 |
| ENG-005 | Decide and act on the orphaned A4PosterGenerator component | aiorders-admin-hub | shaped | (empty) | product-manager | S | 2026-08-25 |

`ENG-002` shipped and reached `verified` in an earlier pass today — off the
In-flight table (terminal); see its own board file. `ENG-001` — this
instance's seed ticket — reached `verified` this pass, its G3 answered
**approved**; off the In-flight table (terminal); see its own board file and
the dated entry below. `ENG-003` — its G1 answered **rejected** this pass —
reached `dropped`; off the In-flight table (terminal); see its own board
file and the dated entry below.

## Waiting on the approver

Cap: 3 across all gates. **Currently 0/3** — nothing open.

Nothing waiting. `ENG-003`'s G1 — the only item on this list — was answered
(rejected) this pass; see the dated entry below.

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
