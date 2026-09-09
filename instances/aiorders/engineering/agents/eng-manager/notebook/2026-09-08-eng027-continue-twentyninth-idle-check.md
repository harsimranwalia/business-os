# ENG-027 continue — twenty-ninth consecutive idle re-confirmation

`continue` event, context `ENG-027`. Reading map for `continue`: steps 6 and
6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*;
*The four lanes*; *Guards*). Read the full `eng_build_loop.md` this pass, per
the map-is-a-floor rule.

Mode check: repo-root `.env` → `MODE=active`.

Treated the prompt's checkpoint (copied from the ticket's own 28th-confirmation
entry) as untrusted per its own instruction — re-derived every claim below
independently against live state rather than taking it on the checkpoint's or
the 28th check's own notebook's word.

Pre-pass `lib/eng-gate-check.sh` (`/bin/zsh departments/engineering/lib/eng-gate-check.sh`
from the instance root), whole-board: exit 0, clean, no output.

- `ENG-027` frontmatter read fresh: `state: building`, `priority: now`,
  `owner: eng-manager`, `blocked_on:` empty, `depends_on: [ENG-006, ENG-007]`
  (both `verified`), `parent:` empty (it is the parent).
- `ENG-048`/`ENG-049` frontmatter read fresh: both `state: blocked`,
  `owner: approver`, `blocked_on: approver`, `blocked_from: ready-to-ship`
  (`ENG-048` `depends_on: []`, `ENG-049` `depends_on: [ENG-048]`). Both carry
  `parent: ENG-027` — no third child.
- PR state, checked live, from the department's own worktree from the start
  this pass — no repo-isolation slip: went straight to
  `cd ~/Documents/projects/_eng/aiorders-api` (never touched
  `~/Documents/projects/aiorders/aiorders-api`), then `git fetch origin`, then
  `gh pr view 21/22 --json state,mergedAt,baseRefName,headRefName`. `#21` →
  `OPEN`, `mergedAt: null`, base `main`. `#22` → `OPEN`, `mergedAt: null`, base
  `feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron` (still
  stacked). Unchanged from the 28th check.
- Machine WIP: the only ticket anywhere in `ready`..`ready-to-ship` is
  `ENG-027` itself (`building`), a container with both children parked —
  genuinely `0/1` free.
- To-do column (`intake`/`shaped`/`awaiting-scope`), fresh frontmatter reads:
  `ENG-018` (`awaiting-scope`, `now`), `ENG-028` (`awaiting-scope`, `now`),
  `ENG-042` (`awaiting-scope`, unset priority), `ENG-043` (`intake`, unset) —
  no fifth candidate, none `hold` (whole-board grep for `priority: hold`:
  zero hits anywhere on the board, not just among these four). All 10 open
  top-level `inbox/` items (`ENG-016`-piece2, `ENG-018`, `ENG-028`,
  `ENG-042`, `ENG-043`, `ENG-048`-merge, `ENG-049`-merge, `ENG-050`-P0,
  `IDLE-2026-09-07`, `PROP-2026-W36`) grepped for `^decision:` — none present
  on any.
- `inbox/IDLE-2026-09-07.md` frontmatter re-checked: `notified:
  2026-09-07T18:44:54`, `nudged:` empty, no `decision:`. Wall clock now
  `2026-09-08T15:37:10Z` → ≈20h52m old, still under the 24h nudge threshold,
  and its content (checked against the same four To-do occupants and the same
  `ENG-050` callout the 28th check already verified in full) is still an exact
  match for today's state — nothing stale. Also checked the other two
  not-yet-nudged items: `ENG-048`-merge (`notified: 2026-09-07T16:18:23`)
  ≈23h19m old, `ENG-050`-P0 (`notified: 2026-09-07T16:04:16`) ≈23h33m old —
  both still under 24h, but `ENG-050`-P0 is now within roughly half an hour of
  the threshold; whichever pass finds it past 24h owes it the one standing
  nudge. Nothing nudged this pass.
- Held-for-slot/`designed`-pool tension (`proposals.md` row, 2026-09-07,
  line 89), the idle-recurrence-cost proposal (2026-09-07 row, line 91), and
  the repo-isolation proposal (2026-09-08 row, line 92) re-read fresh — all
  three still under `## Open` (section header at line 22, `## Approved` at
  line 94), content unchanged. Left alone; resolving any is the approver's
  call, not this pass's.
- Runaway-guard counters read directly from `traces/.hops-2026-09-08` (`17`)
  and `traces/.hops-2026-09-08-ENG-027` (`16`) — both up by exactly 1 from
  the 28th check's `16/200`/`15/20`, consistent with this pass's own single
  hop. `plan.tier: max_5x` (`hops_per_day: 200`, `hops_per_ticket: 20`). The
  day total isn't close to its ceiling; **ENG-027's own per-ticket count
  (`16/20`, 80%) is tighter still than the 28th check's own 75%** — four more
  hops of this shape exhausts the per-ticket budget entirely, after which a
  queued `continue ENG-027` would be dropped outright rather than launched
  (`eng_build_loop.md`, "The chain" — "a queued event whose ticket has spent
  its daily hop budget" is dropped). Not filed as a new proposal — the same
  cost the open idle-recurrence-cost row already names, and that row's own
  fix (a cheap external-change fingerprint before ever launching `claude`)
  is exactly what would stop this trend; naming the tightening number plainly
  each time is the only thing this pass adds. No trip yet; the guard is
  working as designed if it does.
- `exception-request:` sweep on `ENG-027`'s own log: no live hit (every match
  is a prior pass's own negation sentence, now nine of them).
- Untracked `deno.lock` files in the `_eng/aiorders-api` worktree: same three
  (`brand-portal`, `loyalty-auto-complete`, `restaurant-marketplace`),
  re-checked via `git status --porcelain=v1`, unchanged since the 2026-09-07
  `observations.md` row — not re-filed.
- `board/_index.md`: exactly three dated entries confirmed (`2026-09-07` ×2,
  `2026-09-08` ×1) — unchanged, nothing to roll.

No divergence found anywhere, and no repo-isolation slip of this pass's own to
disclose. Same operational conclusion as confirmations 5 through 28 and the
intervening `scheduled` sweeps, independently re-derived rather than copied
forward.

## Not done this pass, deliberately

Did not fall back to the `designed`-state pool (`ENG-050` included) — still
the approver's call, per the open proposal. Did not nudge
`IDLE-2026-09-07.md`, `ENG-048`-merge, or `ENG-050`-P0 (all still under 24h)
or duplicate the idle item. Did not touch `board/_index.md` — no ticket state
changed, the index already holds exactly three dated entries, nothing to
roll. Did not re-file the `deno.lock` observation, the designed-pool tension,
or the hop-count trend as new proposals — all already on record, this pass's
numbers are confirmation, not a new finding. Did not fire
`lib/eng-trigger.sh` for any ticket — nothing on the board is startable.

## Outcome

`chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged, not
duplicated (29th consecutive confirmation)`. Post-pass `lib/eng-gate-check.sh`,
whole-board, run after this file and the ticket log are written. business-os
left uncommitted — standing default, commit-convention question still open.
