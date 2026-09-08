# ENG-027 continue — fourth consecutive idle re-confirmation

`continue` event pass, context `ENG-027`. Reading map for `continue`: steps 6
and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
instructed*; *The four lanes*; *Guards*). Read the full procedure document
regardless, since the reading map is a floor not a ceiling and this pass
turned up state the map didn't anticipate (see "Where this event actually
came from" below).

Mode check clean: repo-root `.env` → `MODE=active`. Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-027`) and whole-board: both exit 0.

## Treated the checkpoint as untrusted, per its own instruction

The prompt's checkpoint block (copied from `ENG-027`'s own board file, its
last log entry ending line 669) claimed: container ticket, both children
dispatched, neither settled, `ADR-003` holds the parent at `building`,
machine WIP `0/1` free, four To-do candidates all blocked on unanswered
gates, `IDLE-2026-09-07` open and accurate, notify sweep clean. Re-derived
every one of these independently rather than trusting the copy:

- `ENG-048`/`ENG-049` frontmatter read fresh: both `state: blocked`,
  `blocked_on: approver`, `parent: ENG-027`. Neither `shipped`/`verified`/
  `dropped`, so `ADR-003`'s parent-exemption condition is unmet — `ENG-027`
  correctly stays `building`.
- PR states: `gh pr view 21 --json state,baseRefName,headRefName,mergedAt`
  → `OPEN`, base `main`, `mergedAt: null`. `gh pr view 22` (same fields) →
  `OPEN`, base `feat/ENG-048-...` (stacked, matching `ENG-049`'s own
  `depends_on: [ENG-048]`), `mergedAt: null`. Both confirm not merged.
- Whole-board state sweep (`grep -m1 "^state:"`/`"^parent:"` across every
  `ENG-*.md`): no ticket in `ready|in-review|in-qa|in-security|
  ready-to-ship`. `ENG-027` is the only `building` row, and per Guards'
  2026-09-07(b) amendment a container (children carry `parent: ENG-027`)
  holds no slot in any state. Machine WIP `0/1`, genuinely free.
- To-do column (`intake`/`shaped`/`awaiting-scope`, the only source per
  step 6): same four occupants — `ENG-018`, `ENG-028`, `ENG-042`,
  `ENG-043`. Checked each one's named blocking `inbox/` item directly
  (`grep -E "^(decision|notified|nudged):"` plus the `## Decision` body):
  all four still read the unfilled template text ("Filled in by the
  approver.") — none answered.
- `inbox/IDLE-2026-09-07.md`: no `decision:` field, content matches what
  the checkpoint described. Re-confirmed still accurate — every fact in it
  (four To-do tickets, their blocking items, the ENG-050 aside) still holds
  fresh.
- Notify sweep: current wall-clock re-checked twice during this pass
  (`20:29` and again `20:35` PDT / `03:29`–`03:35` UTC). `ENG-048`
  (~4h20m), `ENG-049` (~1h50m), `ENG-050` (~4h30m), `IDLE-2026-09-07`
  (~1h50m) all under 24h; everything older already carries its one-ever
  `nudged:`. Nothing due.

No divergence found anywhere — the checkpoint was accurate. But the
re-derivation surfaced something the checkpoint couldn't have shown, because
it only ever sees `ENG-027`'s own file.

## Where this event actually came from — read `board/_index.md` and the trace log

`board/_index.md` carried a **fourth** dated entry beyond what the
checkpoint implied: `## 2026-09-08 — scheduled (auto-drain): whole-board
sweep — no change since the immediately preceding continue (ENG-027), idle
confirmed a third time` (UTC-dated; local wall-clock was still `2026-09-07`
evening — this board's dated headers use UTC, ticket-log bullets use local
date, a pre-existing inconsistency not chased further here). That entry's
own text: *"Between this pass and the previous dated entry above, one more
pass ran and is not yet reflected here: `continue (ENG-027)` ... itself
found nothing new."* — i.e. it already knew about the checkpoint pass and
about a further pass still to come.

Cross-checked `traces/eng-loop-2026-09-07.log` directly rather than
guessing:

```
[20:16:18] pass end: continue (exit 0, 707s)              <- the checkpoint pass
[20:16:21] draining queued event: scheduled (auto-drain)
[20:16:21] pass start: scheduled (auto-drain) [day 48/200, 5 refunded]
[20:27:11] pass end: scheduled (exit 0, 648s)              <- the board-index entry above
[20:27:14] draining queued event: continue (ENG-027)
[20:27:14] pass start: continue (ENG-027) [day 49/200, 5 refunded, ENG-027 4/20]  <- THIS PASS
[20:30:04] scheduled — pass in flight, queued as pending    <- next event already waiting
```

So this pass is a genuine, distinct queued event — not a duplicate of the
checkpoint pass and not a re-fire I triggered. Traced further back
(`grep -n "ENG-027\|pass start\|pass end" `, full afternoon/evening range)
to rule out a broken-chain scenario: `ENG-027` itself last logged
`chained: none` (the checkpoint entry), and neither `ENG-048`'s nor
`ENG-049`'s own final chain lines name `ENG-027` (`ENG-048`:
`chained: ENG-049 — slot freed by ENG-048`; `ENG-049`:
`chained: none — idle: nothing startable`) — so no child fired this either.
Also visible in the same log range: `continue (ENG-027)` failed twice
earlier in the evening before the checkpoint pass ever ran successfully —
`19:54:18` exit 1 (real failure, re-queued attempt 2/3), `19:59:26` exit 1
(NEVER STARTED, all 3 OAuth accounts limited, refunded, back-off armed
300s), then succeeded at `20:04:29`–`20:16:18` (that success is the
checkpoint). The queue's own "collapse duplicates before each pop" rule
means a second, independently-fired `continue ENG-027` line must have been
appended to `traces/.pending` sometime after the collapse-check that
preceded the `20:16:21` pop (which only found `scheduled (auto-drain)` to
drain) — the log as captured doesn't show the append line itself (fires
below the lock only log the pop side in this trace format), so the exact
origin of this pass's own trigger is not fully reconstructable from this
file alone. Did not chase further: reconstructing exactly which external
actor fired it is not this pass's job, and nothing above suggests a broken
chain (every ticket's own `chained:` line is present and consistent with
what actually ran) — it reads as this being a genuinely fast-moving queue
(likely the `auto-drain` mode itself, given the naming), not a bug.

**Filed as an observation, not chased into a fix**: four consecutive
passes (two `continue ENG-027` — the checkpoint and this one — and two
`scheduled (auto-drain)`) independently re-derived the identical idle
conclusion within about 40 minutes of wall-clock time, each spending a
full session and a hop against `ENG-027`'s and the department's own daily
budget to do it. See `observations.md`, this date.

## Process note: repo-isolation slip during PR verification

This pass's own `git fetch origin` and `gh pr view 21`/`22` calls (used to
independently confirm the PR states above, not trusted off the board
narrative) were run from `~/Documents/projects/aiorders/aiorders-api` —
`config/projects.md`'s "Working copies" section names this path as **"the
human's. Never touched by an agent"**, distinct from the department's own
dedicated worktree at `~/Documents/projects/_eng/aiorders-api` (confirmed
both exist as linked worktrees of the same repo via `git worktree list`,
run from either path).

Assessed for actual harm before deciding how to log it:

- `git fetch` only writes to the shared object database and updates
  `refs/remotes/origin/*` — both shared across all worktrees of a repo
  regardless of which one invokes the fetch. It does not touch a
  worktree's checked-out files, index, or `HEAD`.
- `gh pr view` is a pure GitHub API read; it does not touch git state at
  all.
- `git status --short --branch` in that directory, run immediately after
  to check, showed pre-existing uncommitted changes (`supabase/functions/
  README.md`, `supabase/functions/restaurant-marketplace/deno.json`, an
  untracked `$OUT`, and three untracked migration files under
  `20260903*`/`20260904*`) — none plausibly caused by a read-only fetch or
  API call, and unrelated to anything `ENG-027`/`ENG-048`/`ENG-049` touch.

Conclusion: no actual interference with the approver's own working
directory, but the rule as written is "never touched," not "never
mutated," so this was a real, if harmless, violation of it. Disclosed to
the approver directly in this pass's own chat output (not just filed
quietly), and logged as an observation (`observations.md`, this date) —
not raised as a finding or incident, since a P0-style escalation for a
read-only command with a confirmed-harmless outcome would misrepresent its
severity. Future passes verifying PR/merge state on `aiorders-api` should
use `~/Documents/projects/_eng/aiorders-api`, matching what the checkpoint
pass and the `scheduled (auto-drain)` pass both did correctly (see either
one's own notebook entry, this date).

## Machine WIP, To-do, and the idle conclusion — unchanged

Same conclusion as the checkpoint and the intervening `scheduled
(auto-drain)` pass, independently re-reached rather than copied: `ENG-027`
stays `building` (container, `ADR-003` unmet), Machine WIP `0/1` free, four
To-do occupants all genuinely blocked on unanswered approver items,
`IDLE-2026-09-07.md` still the single correct place that's recorded, not
duplicated.

## Not done this pass, deliberately

No dead-end sweep beyond `ENG-027` itself and the trace-log check above —
out of a `continue` event's own narrower contract. `ENG-048`'s and
`ENG-049`'s own board files were read, never written to. Did not attempt to
fully reconstruct which process appended the second `continue ENG-027`
queue entry — the evidence available (every ticket's own `chained:` line
consistent, no dropped-event file for today, `lib/eng-gate-check.sh` clean
pre- and post-pass) gives no reason to treat this as a bug rather than fast
queue activity, and chasing it further is proposal-worthy at most, not
something this pass needs to resolve to correctly process its own event.

## Outcome

`chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged, not
duplicated (fourth consecutive confirmation)`. Post-pass
`lib/eng-gate-check.sh`, scoped and whole-board: exit 0, clean. business-os
left uncommitted — standing default, commit-convention question still
open.
