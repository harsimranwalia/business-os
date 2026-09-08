# ENG-027 continue — twenty-third consecutive idle re-confirmation

`continue` event, context `ENG-027`. Reading map for `continue`: steps 6 and
6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*;
*The four lanes*; *Guards*) — read the full procedure document this pass
regardless, per the map-is-a-floor rule.

Mode check: repo-root `.env` → `MODE=active`.

Treated the prompt's checkpoint (copied from the ticket's own line-1190
entry, the 22nd confirmation) as untrusted per its own instruction, and
re-derived every claim independently against live state rather than taking
it, or the 22nd check's own notebook entry, on its word:

- `ENG-027` frontmatter read fresh: `state: building`, `priority: now`,
  `owner: eng-manager`, `blocked_on:` empty, `depends_on: [ENG-006, ENG-007]`
  (both `verified`). Ticket log's real tail read directly (not just the
  prompt's copy): 1211 lines, newest entry the 22nd confirmation, matches
  the checkpoint verbatim.
- `ENG-048`/`ENG-049` frontmatter read fresh: both `state: blocked`,
  `owner: approver`, `blocked_on: approver`, `blocked_from: ready-to-ship`.
  Board-wide `grep -rl "^parent: ENG-027"` → exactly these two files, no
  third child.
- PR state, checked live from the department's own worktree
  (`~/Documents/projects/_eng/aiorders-api`, `cd` there explicitly — not the
  human's checkout, see the finding below), fresh `git fetch origin` first,
  then `gh pr view {n} --json number,state,baseRefName,mergedAt,url`:
  `#21` → `OPEN`, `mergedAt: null`, base `main`. `#22` → `OPEN`,
  `mergedAt: null`, base `feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron`
  (still stacked). Unchanged from the 22nd check.
- Machine WIP: board's In-flight table read fresh, cross-checked against
  each listed ticket's own frontmatter. The only ticket anywhere in
  `ready`..`ready-to-ship` is `ENG-027` itself (`building`), a container
  with both children parked — genuinely `0/1` free.
- To-do column (`intake`/`shaped`/`awaiting-scope`), same fresh read:
  `ENG-018` (`awaiting-scope`, `now`), `ENG-028` (`awaiting-scope`, `now`),
  `ENG-042` (`awaiting-scope`, unset priority), `ENG-043` (`intake`, unset)
  — no fifth candidate, none `hold`. Cross-checked every open top-level
  `inbox/` item (8 files: `eng016`-piece2, `eng018`-g1, `eng028`-g1,
  `eng042`-g1, `eng043`-clarification, `eng048`-merge, `eng049`-merge,
  `eng050`-p0, plus `IDLE-2026-09-07` and `PROP-2026-W36` — 10 total) for
  `^decision:` — none present on any. Nothing answered.
- Held-for-slot / `designed`-pool tension: `proposals.md` line 89 (devops,
  2026-09-07) re-read fresh — still `## Open`, still disputing whether step
  6's literal To-do-only reading should be amended. Step 6 itself still
  names only the To-do column. Not this pass's to resolve; took the literal
  reading again, same as every prior check.
- `inbox/IDLE-2026-09-07.md` read in full: `notified: 2026-09-07T18:44:54`,
  `nudged:` empty, no `decision:`. Wall clock `2026-09-08T12:23:08` (UTC) —
  17h38m old, still under the 24h nudge threshold. Content re-checked
  against everything verified above (same four candidates, same blockers) —
  still accurate, not stale. Only "nothing startable" item open anywhere in
  `inbox/`.
- `proposals.md`'s `## Open` section: both the devops designed-pool row
  (line 89) and the eng-manager idle-recurrence-cost row (line 91)
  confirmed still present, same content, still under `## Open`. Left
  alone — resolving either is the approver's call.
- Runaway-guard counters, read directly from `traces/.hops-2026-09-08` and
  `traces/.hops-2026-09-08-ENG-027`: `day 11/200`, `ENG-027 10/20` — both up
  by exactly 1 from the 22nd check's `10/200`/`9/20`, consistent with this
  being the one hop this pass itself consumes. Cross-checked against
  `plan.tier: max_5x` in `departments/engineering/agents/eng-manager/config.yaml`
  (`hops_per_day: 200`, `hops_per_ticket: 20`) rather than assumed from
  memory of prior checks' own citations. Still nowhere near either ceiling.
- Fresh, field-anchored `exception-request:` sweep on `ENG-027`'s own log:
  every hit is a prior pass's own "none found" prose, not a live field.
  None found this pass either.
- Pre-pass `lib/eng-gate-check.sh`: scoped (`ENG-027`, positional arg — not
  `--ticket`, confirmed by reading the script's own arg handling) and
  whole-board both exit 0, clean.

No divergence found in any board-state fact. Same conclusion as
confirmations 5 through 22 and the intervening `scheduled` sweeps,
independently re-derived from live `gh`/`grep`/frontmatter reads rather
than copied from the checkpoint or the prior notebook entry.

## Finding: a third occurrence of the repo-isolation slip — filed as a proposal, not a fourth observation

While re-deriving the PR-state check above, cross-referenced the 22nd
check's own notebook (`2026-09-08-eng027-continue-twentysecond-idle-check.md`,
line 25) rather than trusting its conclusion at face value. It states its
`git fetch`/`gh pr view` ran "from `~/Documents/projects/aiorders/aiorders-api`"
— the human's interactive checkout (`config/projects.md`'s Working copies
section: "Never touched by an agent"), not the department's own
`~/Documents/projects/_eng/aiorders-api` worktree — with no isolation
caveat the way checks 11/16/17 stated one explicitly.

This is not a first occurrence. `agents/eng-manager/observations.md`
already carries two 2026-09-07 rows on the identical slip: the 4th
`continue ENG-027` idle-check made it and self-caught it in the same pass;
a second, later same-day pass repeated it, was also caught, and that row's
own closing line was "Worth a look if a second pass is found making the
same mistake." That tripwire has now fired a third time.

Assessed for harm the same way both prior occurrences were, not assumed
either way: `git fetch` only updates shared remote-tracking refs (identical
effect from any worktree) and touches no checked-out files/index/HEAD;
`gh pr view` is a pure API read. This pass's own fresh check from the
correct worktree found the same PR states the 22nd check reported, so
nothing on the board was affected. Harmless again, this time.

Filed to `proposals.md`'s `## Open` table (2026-09-08, eng-manager,
`aiorders-api`) rather than a third `observations.md` row: the department's
own idle-recurrence-cost row (line 91, same file) already makes the
argument that a pattern which keeps re-triggering its own "worth watching"
clause should stop being re-logged identically and get an actual fix
decision instead — the same logic applies here, one strike earlier than
that convention's literal three, because this is a safety rule with a
plausible-worse-case (a repo that does carry live uncommitted WIP)
rather than a pure cost concern. Did not touch `observations.md` for this —
picking one ledger per finding per the file's own guidance against
double-filing.

## Not done this pass, deliberately

Did not fall back to the `designed`-state pool — still the approver's call,
per the open proposal. Did not duplicate `IDLE-2026-09-07.md` or nudge it
(17h38m old, under 24h). Did not touch `board/_index.md` — established
convention since roughly the 12th confirmation is that a `continue
ENG-027` idle pass which changes no ticket state and creates no new board
entry leaves the index alone; its dated-entries section is for `scheduled`
sweeps and real transitions. Did not open or act on
`inbox/2026-09-07-eng050-p0-incident.md` — a different ticket's incident
item, outside a `continue ENG-027` event's scope. Did not fire
`lib/eng-trigger.sh` for any ticket — nothing on the board is startable.

## Outcome

`chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged, not
duplicated (23rd consecutive confirmation)`. One proposal filed
(repo-isolation recurrence, `proposals.md`, 2026-09-08 row) — not board-state
affecting, left for the approver's batched G1. Post-pass
`lib/eng-gate-check.sh`, scoped and whole-board: run after this file and the
ticket log are written. business-os left uncommitted — standing default,
commit-convention question still open.
