# Board

**Next ID: ENG-026** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.)

**Machine WIP 12** (`config/config.yaml` → `wip.machine_limit`, matching the
`max_5x` plan tier). **Currently 6/12 — well under cap.** `ENG-007`
and `ENG-011` sit at `ready-to-ship`; `ENG-009` and `ENG-010`
sit at `ready`; `ENG-008` and `ENG-013` sit at `building`. `ENG-014`,
`ENG-015` and `ENG-025` do not count here (all `designed` as of this pass,
short of the counted range).

**Approver-facing WIP 2 — 1/2.** `ENG-025`'s G1 was processed this pass
(`scheduled`, context `schtasks`) — moved `awaiting-scope → designed`, off
this count. `ENG-023` (its G1 raised this same pass, from its own
already-drafted PRD content) now holds the one occupied slot.

**Approval cap 3 — 1/3.** `ENG-025`'s G1 processed this pass (see above),
freeing the slot it held. `ENG-023`'s new G1
(`inbox/2026-08-29-eng023-g1-scope.md`) occupies one of the three. Two
slots free — `ENG-016` through `ENG-021` are also G1-drafted and ready, but
deliberately left for a future pass rather than filling every open slot in
one sweep; see `ENG-023`'s own ticket log for the reasoning.

`priority:` is a field on every ticket, and **only the approver sets it.** It is
not `severity`, which is the agent's read of how bad a problem is.

## In flight

| ID | Title | Project | State | Priority | Owner | Size | Updated |
|---|---|---|---|---|---|---|---|
| ENG-007 | Per-restaurant loyalty configuration — earn rates and redemption value | aiorders-api | ready-to-ship | | devops | S | 2026-08-29 |
| ENG-008 | Influencer board admin management — region/campaign-type preference, rating, collaboration count | aiorders-admin-hub | building | | eng-manager | M | 2026-08-29 |
| ENG-009 | Influencer engagement info — internal activity signal plus a staff-editable social stat | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-29 |
| ENG-010 | Influencer relationship notes — staff log for personality, preferences, and off-platform conversations | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-29 |
| ENG-011 | Client stage & health visibility on the Brands admin page — plus stage filtering | aiorders-admin-hub | ready-to-ship | | devops | M | 2026-08-29 |
| ENG-013 | Foodswipe funnel page — staff-settable pipeline stages | aiorders-admin-hub | building | | eng-manager | M | 2026-08-29 |
| ENG-014 | Brand portal self-service — restaurant QR codes and marketing media downloads | restaurant-portal | designed | | architect | M | 2026-08-29 |
| ENG-015 | Agency/reseller (partner) users — brand-scoped locations and a working add-location path | aiorders-admin-hub | designed | | architect | M | 2026-08-29 |
| ENG-016 | Catering page — self-serve quote generator, with automatic stage update | config-site-builder | shaped | | product-manager | L | 2026-08-29 |
| ENG-017 | Autopilot nurture for the presignup sales lead pipeline — stage-triggered email/SMS | aiorders-api | shaped | | product-manager | L | 2026-08-29 |
| ENG-018 | Sales demonstration account — a fully seeded AIOrders environment to show prospects | aiorders-admin-hub | shaped | | product-manager | L | 2026-08-29 |
| ENG-019 | Restaurant self-service marketing broadcasts — mass send and drip sequences, scheduled or immediate | restaurant-portal | shaped | | product-manager | L | 2026-08-29 |
| ENG-020 | Marketing ROI reporting — traffic source and revenue attribution on the brand dashboard | restaurant-portal | shaped | | product-manager | M | 2026-08-29 |
| ENG-021 | Website chat-bar engagement visibility — customer questions and self-service FAQ editing on the brand portal | restaurant-portal | shaped | | product-manager | M | 2026-08-29 |
| ENG-022 | Fix broken restaurant-scoped access check on 5 brand-portal handlers — cross-tenant PII/write exposure | aiorders-api | shaped | | architect | M | 2026-08-29 |
| ENG-023 | Add status and internal notes to each brand-portal feedback item | restaurant-portal | awaiting-scope | | approver | S | 2026-08-29 |
| ENG-024 | Set show_in_marketplace on onboarding's createRestaurant insert, plus a backfill | aiorders-api | shaped | | eng-manager | XS | 2026-08-29 |
| ENG-025 | Recurring feedback issues, per restaurant, over time | restaurant-portal | designed | | architect | S | 2026-08-29 |

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
`ENG-012` — its G1 answered **rejected** ("later") in the 2026-08-29
`scheduled` sweep (since rolled to `_index-archive.md`) — reached `dropped`;
off the In-flight table (terminal); see its own board file.

## Waiting on the approver

Cap: 3 across all gates. **1/3.** `ENG-025`'s G1 was processed by this
2026-08-29 `scheduled` pass — moved `awaiting-scope → designed`, off this
section entirely. `ENG-023`'s new G1
(`inbox/2026-08-29-eng023-g1-scope.md` — status and internal notes on each
brand-portal feedback item) is the only thing occupying this cap now,
raised this same pass from its own already-drafted PRD content, per this
board's own standing note naming it as ready the moment a
`scheduled`/`watch`/`continue` pass picked it up. `ENG-016` through
`ENG-021` are also G1-drafted and ready to raise, deliberately left for a
future pass rather than filling every open slot in one sweep — see
`ENG-023`'s own ticket log for the reasoning.

## 2026-08-29 — continue ENG-013: built the stage-override column, handler, and UI across both repos, ready → building

`continue` event pass, context `ENG-013`, its turn at the front of
`traces/.pending` finally reached. Narrow scope per the event's own
contract. Mode check clean.

Pre-pass gate check arrived flagged (exit 2, all of `ENG-013`..`ENG-024`
reported "not a regular file"). Investigated rather than trusted: `stat`
confirmed every file is a normal regular file, and a fresh re-run (scoped
and whole-board) returned exit 0 clean. Transient — the injected report was
captured mid-write during the prior pass's own commit
(`1a6fe83`). Nothing to fix.

Both `_eng` worktrees existed, sitting on `feat/ENG-011-...` (still owed —
`ENG-011` hasn't opened its PR yet). `aiorders-admin-hub` carried the same
benign `package-lock.json` `peer:true` drift `ENG-011`'s own recovery
already named — stashed, labeled, not discarded, not committed. Branched
both repos fresh off `origin/main` as `feat/ENG-013-foodswipe-funnel-stage-control`.

Built per the design: one nullable `foodswipe_stage_override` column on
`profiles` (six-value `CHECK`); `classifyStage()`'s caller now prefers it;
two new gated, source-scoped write actions
(`/foodswipe/stage/{set,reset}`) in `aiorders-api`. Per-card stage dropdown
+ dialog (styled after `Leads.tsx`) and a "Manually set" badge in
`aiorders-admin-hub`. Self-tested: `deno check` clean, `npm run lint`
(zero new issues — the repo's 150 pre-existing errors are all in files
this ticket didn't touch), `npm run build` clean. Live-verified read-only
via Supabase MCP against the real `aiorders-api` project
(`bmnmnejwdxbcqinqkwko`): schema assumptions, table scale (528 rows, 36
`source='foodswipe'`), and non-applied migration status all confirmed.
Database migration doc written
(`agents/database/migrations/ENG-013-foodswipe-funnel-stage-control.md`).
Both branches committed and pushed; PR bodies drafted in the ticket's own
log (no PR opened yet — that's devops's release step). Artifact-enumeration
grep for "foodswipe" across instance+department docs found no
instruction/map conflicts, only one harmless location-citation drift in
`ENG-009`'s design doc, left alone.

**1 transition** (`ready → building`), well under the cap — the next hop
(review + quality, combined) is a fresh session's work by design. No cap
change; `ENG-013` stays inside the counted `ready..ready-to-ship` range.

`chained: ENG-013` — `building` is agent-owned (principal-engineer + qa
next). Fired `continue ENG-013`. Post-pass gate check: exit 0, clean, both
scoped and whole-board. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-013-foodswipe-funnel-stage-control.md`).

## 2026-08-29 — decision ENG-015: G1 already processed by the same dying `watch` pass as ENG-014, its own recorded chain never fired either — repaired

`decision` event pass, context `2026-08-29-eng015-g1-scope.md` — this
event's own queued fire, drained behind the `decision ENG-014` repair pass
immediately before it (`pass end: decision (exit 0, 685s)` at 15:33:53 →
`draining queued event: decision (2026-08-29-eng015-g1-scope.md)`,
15:34:45, no gap, one duplicate collapsed). Mode check clean. Pre-pass gate
check: exit 0, clean, scoped (`ENG-015`) and whole-board.

Exactly the gap the immediately-preceding pass predicted and flagged in
`observations.md`: `ENG-015`'s G1 was genuinely fully processed (approved,
`awaiting-scope → designed`, owner `architect`, journaled — all verified
fresh against `inbox/_handled/`, the PRD, and `decision-journal.md` rather
than trusted), but its own recorded `chained: ENG-015` line never actually
fired — same dying `watch` pass (pid 36150), same absence from
`traces/eng-loop-2026-08-29.log` and from `traces/.pending` beforehand.

**Action:** re-fired `/bin/sh
departments/engineering/lib/eng-trigger.sh continue ENG-015` directly.
Confirmed on `traces/.pending` afterward (`1 continue ENG-015`) and via
`traces/.loop.lock/pid` (`1909`) confirmed alive with `ps -W` — queued
correctly behind this still-running pass rather than lost again. No ticket
state changed.

**0 transitions**, no cap impact — this was a chain repair, not new gate
or state movement. This closes out both halves of the pair `ENG-014`'s own
repair pass surfaced; no further tickets carry this shape as far as this
pass found.

`chained: ENG-015` — re-fired and confirmed queued this pass (see above).
Post-pass gate check: exit 0, clean, both scoped and whole-board. Full
detail on the ticket's own log
(`agents/eng-manager/board/ENG-015-agency-reseller-brand-scoping.md`).

## 2026-08-29 — scheduled schtasks: safety-net sweep — processed ENG-025's G1, raised ENG-023's, recovered five passes of uncommitted work

`scheduled` event pass, context `schtasks` — the four-times-daily safety-net
sweep, drained immediately behind the `decision ENG-015` pass above in the
same held lock (`traces/.loop.lock/pid 1909`, confirmed alive throughout).
Whole-board sweep per this event's own contract, not one named ticket. Mode
check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

**Business/technical intake:** `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/`, and `inbox/requests/` all empty. Nothing to
shape, nothing to batch as a proposal.

**Gate returns:** `inbox/` held exactly one file,
`2026-08-29-eng025-g1-scope.md` (`decision: approved`,
`decided: 2026-08-29T22:22:18.827452+00:00`). Processed:
`ENG-025` `awaiting-scope → designed`, owner `approver → architect`; PRD
`status: approved`; gate item moved to `inbox/_handled/`; journaled
(`decision-journal.md`). That freed both the approver-facing WIP slot and
the approval-cap slot ENG-025 held — reused in this same pass, per
`_index.md`'s own standing note, to raise `ENG-023`'s G1 (fully drafted
already in its PRD's Decision section, nothing written fresh): `ENG-023`
`shaped → awaiting-scope`, owner `product-manager → approver`;
`inbox/2026-08-29-eng023-g1-scope.md` raised, `eng-notify.sh raise` run
(logged `SLACK_WEBHOOK_URL unset`, same open gap every gate item today has
hit), `notified:` stamped manually. Net: approver-facing WIP and approval
cap both end this pass exactly where they started (1/2, 1/3), now against
`ENG-023` instead of `ENG-025`. `ENG-016`–`ENG-021` (also G1-drafted)
deliberately left unraised — see `ENG-023`'s own log for why only the one
explicitly-earmarked ticket was raised rather than filling every free slot.

**Merge detection:** no ticket sits at `blocked` anywhere on the board — no
L1 PRs to check ancestry on this pass.

**Dispatch / dead-end sweep, whole board:** `ENG-007` (`ready-to-ship`)
re-confirmed correctly held — release window still closed (Saturday);
resumes naturally Monday. `ENG-009`/`ENG-010` (`ready`) re-confirmed
correctly held pending `ENG-008` reaching `in-review` or later — neither
worktree shows a branch or build started yet. `ENG-011`'s
`chained: ENG-011` already fired and sits genuinely queued in
`traces/.pending`, not stale. No broken chain found on any in-flight
ticket beyond the two already repaired by the two passes immediately
above. Removed `_index-archive.md.tmp.4632.31c9ee9459a2`, the stale
5,027-line crash-artifact temp file `observations.md`'s immediately
preceding row flagged as safe to clear on a dead-end sweep — verified
against that row's own description (size, mtime, stale content) before
deleting.

**Uncommitted-work recovery, the main substance of this pass.** Pre-pass
`git status` showed nothing committed since `a143d9b` despite the board's
own narrative recording five further passes' worth of real, verified work
since: `continue ENG-008` (built the influencer admin-edit path),
`continue ENG-013` (built the FoodSwipe stage-override path), the
`ENG-014`/`ENG-015` chain repairs, and the `ENG-022`/`ENG-023` incident/
question processing — including the `eng-loop-halted` repair pass's own
config-path fix for `read_plan_budget()` (the actual cause of today's
40-hop ceiling firing early). That repair pass's own log states it
committed three of those files "alongside this pass's own changes," but a
fresh `git status` at this pass's start showed all three still modified —
the commit most likely never ran. Verified each change against its own
ticket log before trusting it (per this instance's standing practice, and
the specific lesson `observations.md` names for exactly this shape of
mismatch) rather than committing blindly. Committed the accumulated,
verified work in this pass — see the commit itself for the exact file
list; the stray temp file above was deleted, not committed, and nothing
else in the tree looked suspicious (no secrets, no `.env`, no unrelated
files). Filed as its own `observations.md` row for the pattern (a pass's
own narrated git action not matching the filesystem — a new variant of an
already-seen lesson).

**Notify sweep:** `ENG-023`'s new item raised and stamped this pass (see
above). No item found with `notified:` older than 24h and no `decision:` —
nothing to nudge. Approval cap 1/3, not full — no stall.

**Journal:** `ENG-025`'s G1 answer added to `decision-journal.md`.

`chained: ENG-025` — fired this pass (see that ticket's own log);
`ENG-023` and all `ready`/`ready-to-ship` tickets correctly recorded
`chained: none` (approver-owned or deliberately held) and are not
re-chained here. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

