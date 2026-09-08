# ENG-027 continue — twenty-eighth consecutive idle re-confirmation

`continue` event, context `ENG-027`. Reading map for `continue`: steps 6 and
6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*;
*The four lanes*; *Guards*). Read the full `eng_build_loop.md` this pass, per
the map-is-a-floor rule.

Mode check: repo-root `.env` → `MODE=active`.

Treated the prompt's checkpoint (copied from the ticket's own 27th-confirmation
entry) as untrusted per its own instruction — re-derived every claim below
independently against live state rather than taking it on the checkpoint's or
the 27th check's own notebook's word.

Pre-pass `lib/eng-gate-check.sh` (`sh departments/engineering/lib/eng-gate-check.sh`
from the instance root), whole-board: exit 0, clean, no output.

- `ENG-027` frontmatter read fresh: `state: building`, `priority: now`,
  `owner: eng-manager`, `blocked_on:` empty, `depends_on: [ENG-006, ENG-007]`
  (both `verified`), `parent:` empty (it is the parent).
- `ENG-048`/`ENG-049` frontmatter read fresh: both `state: blocked`,
  `owner: approver`, `blocked_on: approver`, `blocked_from: ready-to-ship`
  (`ENG-048` `depends_on: []`, `ENG-049` `depends_on: [ENG-048]`).
  `grep -rl "parent: ENG-027" board/*.md` → exactly these two — no third
  child.
- PR state, checked live, **from the department's own worktree from the
  start this time** — no repo-isolation slip this pass, unlike the 22nd and
  27th checks: went straight to `cd ~/Documents/projects/_eng/aiorders-api`
  (never touched `~/Documents/projects/aiorders/aiorders-api`), then
  `git fetch origin`, then `gh pr view 21/22 --json number,state,mergedAt,baseRefName`.
  `#21` → `OPEN`, `mergedAt: null`, base `main`. `#22` → `OPEN`,
  `mergedAt: null`, base `feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron`
  (still stacked). Unchanged from the 27th check.
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
  `IDLE-2026-09-07`, `PROP-2026-W36`) grepped for `^decision:` — none
  present on any.
- `inbox/IDLE-2026-09-07.md` read in full, not just its frontmatter: still an
  exact match for today's state — same four To-do occupants, same blocking
  gates, same `ENG-050` callout and the same lever offered to the approver
  ("say so and `ENG-050` starts instead"). Nothing stale. `notified:
  2026-09-07T18:44:54`, `nudged:` empty. Wall clock now
  `2026-09-08T15:08:18Z` → ≈20h23m old, still under the 24h nudge threshold.
  Also checked the other two not-yet-nudged items: `ENG-048`-merge
  (`notified: 2026-09-07T16:18:23`) ≈22h50m old, `ENG-050`-P0 (`notified:
  2026-09-07T16:04:16`) ≈23h04m old — both still under 24h, `ENG-050` now the
  closest of the three to the threshold; whichever pass finds it past 24h
  owes it the one standing nudge. Nothing nudged this pass.
- Held-for-slot/`designed`-pool tension (`proposals.md` row, 2026-09-07),
  the idle-recurrence-cost proposal (2026-09-07 row), and the repo-isolation
  proposal (2026-09-08 row) re-read fresh — all three still under `## Open`
  (confirmed against the file's own section headers: `## Open` at line 22,
  `## Approved` at line 94, all three rows between them), content unchanged.
  Left alone; resolving any is the approver's call, not this pass's.
- Runaway-guard counters read directly from `traces/.hops-2026-09-08` (`16`)
  and `traces/.hops-2026-09-08-ENG-027` (`15`) — both up by exactly 1 from
  the 27th check's `15/200`/`14/20`, consistent with this pass's own single
  hop. `plan.tier: max_5x` (`hops_per_day: 200`, `hops_per_ticket: 20`). The
  day total isn't close to its ceiling; **ENG-027's own per-ticket count
  (`15/20`, 75%) is tighter still than the 27th check's own 70%** — not
  filed as a new proposal, the same cost the open idle-recurrence-cost row
  already names; a trip fires `eng-trigger.sh`'s own per-ticket halt_notice
  automatically, the guard working as designed.
- `exception-request:` sweep on `ENG-027`'s own log: no live hit (every
  match is a prior pass's own negation sentence, now eight of them).
- Untracked `deno.lock` files in the `_eng/aiorders-api` worktree: same
  three (`brand-portal`, `loyalty-auto-complete`, `restaurant-marketplace`),
  re-checked via `git status --porcelain=v1`, unchanged since the
  2026-09-07 `observations.md` row — not re-filed.
- `board/_index.md`: exactly three dated entries confirmed
  (`2026-09-07` ×2, `2026-09-08` ×1) — unchanged, nothing to roll.

No divergence found anywhere, and — unlike the 22nd and 27th checks — no
repo-isolation slip of this pass's own to disclose either. Same operational
conclusion as confirmations 5 through 27 and the intervening `scheduled`
sweeps, independently re-derived rather than copied forward.

## Not done this pass, deliberately

Did not fall back to the `designed`-state pool (`ENG-050` included) — still
the approver's call, per the open proposal. Did not nudge
`IDLE-2026-09-07.md`, `ENG-048`-merge, or `ENG-050`-P0 (all still under 24h)
or duplicate the idle item. Did not touch `board/_index.md` — no ticket state
changed, the index already holds exactly three dated entries, nothing to
roll. Did not re-file the `deno.lock` observation, the designed-pool
tension, or the hop-count trend as new proposals — all already on record,
this pass's numbers are confirmation, not a new finding. Did not fire
`lib/eng-trigger.sh` for any ticket — nothing on the board is startable.

## Outcome

`chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged, not
duplicated (28th consecutive confirmation)`. Post-pass `lib/eng-gate-check.sh`,
whole-board, run after this file and the ticket log are written. business-os
left uncommitted — standing default, commit-convention question still open.
