# ENG-027 continue — twenty-seventh consecutive idle re-confirmation

`continue` event, context `ENG-027`. Reading map for `continue`: steps 6 and
6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*;
*The four lanes*; *Guards*). Read the full `eng_build_loop.md` this pass,
per the map-is-a-floor rule.

Mode check: repo-root `.env` → `MODE=active`.

Treated the prompt's checkpoint (copied from the ticket's own 26th-confirmation
entry) as untrusted per its own instruction — re-derived every claim below
independently against live state rather than taking it on the checkpoint's or
the 26th check's own notebook's word.

Pre-pass `lib/eng-gate-check.sh` (`sh departments/engineering/lib/eng-gate-check.sh`
from the instance root), whole-board: exit 0, clean, no output.

- `ENG-027` frontmatter read fresh: `state: building`, `priority: now`,
  `owner: eng-manager`, `blocked_on:` empty, `depends_on: [ENG-006, ENG-007]`
  (both `verified`), `parent:` empty (it is the parent).
- `ENG-048`/`ENG-049` frontmatter read fresh: both `state: blocked`,
  `owner: approver`, `blocked_on: approver`, `blocked_from: ready-to-ship`.
  `grep -rl "parent: ENG-027" board/*.md` → exactly these two — no third
  child.
- PR state, checked live. **Process slip, self-caught:** located the
  department's worktree by running `git worktree list` from
  `~/Documents/projects/aiorders/aiorders-api` — the human's interactive
  checkout, not the department's own — before realizing the mistake. That
  command only reads `.git/worktrees` metadata (no ref/index/file touched),
  but it is still exactly the repo-isolation slip `proposals.md`'s
  2026-09-08 row already names as a recurring pattern (its own count: three
  occurrences before this one). Logged to `observations.md` (this date)
  rather than re-proposed — the open proposal already covers the failure
  mode and a fix. The actual PR-state read ran correctly from the
  department's own worktree once found: `cd ~/Documents/projects/_eng/aiorders-api`,
  `git fetch origin`, `gh pr view 21/22 --json state,baseRefName,mergedAt,headRefName`.
  `#21` → `OPEN`, `mergedAt: null`, base `main`. `#22` → `OPEN`,
  `mergedAt: null`, base `feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron`
  (still stacked). Unchanged from the 26th check.
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
  `2026-09-08T14:34:23Z` (≈07:41 PDT) → ≈19h49m old, still under the 24h
  nudge threshold. Also checked the other three not-yet-nudged items
  (`ENG-048`-merge ≈22h16m, `ENG-050`-P0 ≈22h30m, both from `notified:`) —
  all still under 24h. Nothing nudged.
- Held-for-slot/`designed`-pool tension, the idle-recurrence-cost proposal,
  and the repo-isolation proposal (`proposals.md`, all three) re-read fresh
  — all still `## Open`, unchanged content except this pass's own addendum
  to the repo-isolation row's neighbor in `observations.md`. Left alone;
  resolving any is the approver's call, not this pass's.
- Runaway-guard counters read directly from `traces/.hops-2026-09-08` (`15`)
  and `traces/.hops-2026-09-08-ENG-027` (`14`) — both up by exactly 1 from
  the 26th check's `14/200`/`13/20`, consistent with this pass's own single
  hop. `plan.tier: max_5x` (`hops_per_day: 200`, `hops_per_ticket: 20`). The
  day total isn't close to its ceiling; **ENG-027's own per-ticket count
  (`14/20`, 70%) is tighter still than the 26th check's own 65%** — not
  filed as a new proposal, the same cost the open idle-recurrence-cost row
  already names, and a trip fires `eng-trigger.sh`'s own per-ticket
  halt_notice automatically.
- `exception-request:` sweep on `ENG-027`'s own log: no live hit (every
  match is a prior pass's own negation sentence).
- Untracked `deno.lock` files in the `_eng/aiorders-api` worktree: same
  three (`brand-portal`, `loyalty-auto-complete`, `restaurant-marketplace`),
  re-checked via `git status --short --branch`, unchanged since the
  2026-09-07 `observations.md` row — not re-filed.

No divergence found anywhere except this pass's own repo-isolation slip
(harmless, self-caught, logged). Same operational conclusion as
confirmations 5 through 26 and the intervening `scheduled` sweeps,
independently re-derived rather than copied forward.

## Not done this pass, deliberately

Did not fall back to the `designed`-state pool (`ENG-050` included) — still
the approver's call, per the open proposal. Did not nudge
`IDLE-2026-09-07.md` (≈19h49m old, under 24h) or duplicate it. Did not touch
`board/_index.md` — no ticket state changed, the index already holds exactly
three dated entries, nothing to roll. Did not re-file the `deno.lock`
observation, the designed-pool tension, or the hop-count trend as new
proposals — all already on record, this pass's numbers are confirmation, not
a new finding. Did not file a fresh repo-isolation proposal for this pass's
own slip — appended one row to `observations.md` instead, since the open
proposal already names the exact failure mode and a fix. Did not fire
`lib/eng-trigger.sh` for any ticket — nothing on the board is startable.

## Outcome

`chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged, not
duplicated (27th consecutive confirmation)`. Post-pass `lib/eng-gate-check.sh`,
whole-board, run after this file and the ticket log are written. business-os
left uncommitted — standing default, commit-convention question still open.
