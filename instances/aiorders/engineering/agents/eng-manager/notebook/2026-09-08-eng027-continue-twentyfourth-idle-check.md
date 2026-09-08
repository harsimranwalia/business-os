# ENG-027 continue — twenty-fourth consecutive idle re-confirmation

`continue` event, context `ENG-027`. Reading map for `continue`: steps 6 and
6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*;
*The four lanes*; *Guards*) — read the full procedure document this pass
regardless, per the map-is-a-floor rule.

Mode check: repo-root `.env` → `MODE=active`.

Treated the prompt's checkpoint (copied from the ticket's own line-1213
entry, the 23rd confirmation) as untrusted per its own instruction, and
re-derived every claim independently against live state rather than taking
it, or the 23rd check's own notebook entry, on its word.

Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-027`) and whole-board: both
exit 0, clean.

- `ENG-027` frontmatter read fresh: `state: building`, `priority: now`,
  `owner: eng-manager`, `blocked_on:` empty, `depends_on: [ENG-006, ENG-007]`
  (both `verified`), `parent:` empty (it is the parent). Ticket log's real
  tail read directly: 1246 lines, newest entry the 23rd confirmation,
  matches the checkpoint verbatim.
- `ENG-048`/`ENG-049` frontmatter read fresh: both `state: blocked`,
  `owner: approver`, `blocked_on: approver`, `blocked_from: ready-to-ship`.
  Board-wide `grep -l "parent: ENG-027" *.md` in `board/` → exactly these
  two files, no third child.
- PR state, checked live from the department's own worktree
  (`~/Documents/projects/_eng/aiorders-api`, `cd` there explicitly — not the
  human's checkout), fresh `git fetch origin` first, then `gh pr view {n}
  --json number,state,baseRefName,mergedAt,url`: `#21` → `OPEN`,
  `mergedAt: null`, base `main`. `#22` → `OPEN`, `mergedAt: null`, base
  `feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron` (still
  stacked). Unchanged from the 23rd check.
- Machine WIP: board's In-flight table read fresh. The only ticket anywhere
  in `ready`..`ready-to-ship` is `ENG-027` itself (`building`), a container
  with both children parked — genuinely `0/1` free.
- To-do column (`intake`/`shaped`/`awaiting-scope`), same fresh read:
  `ENG-018` (`awaiting-scope`, `now`), `ENG-028` (`awaiting-scope`, `now`),
  `ENG-042` (`awaiting-scope`, unset priority), `ENG-043` (`intake`, unset)
  — no fifth candidate, none `hold`. Cross-checked every open top-level
  `inbox/` item (10 files, same set the 23rd check named) for `^decision:`
  — none present on any. Nothing answered.
- Held-for-slot / `designed`-pool tension and the idle-recurrence-cost
  proposal (`proposals.md` lines 89/91) re-read fresh — both still `## Open`,
  same content. The 23rd check's own repo-isolation proposal (line 92) also
  confirmed still present, still `## Open`. Left alone — resolving any of
  the three is the approver's call, not this pass's.
- `inbox/IDLE-2026-09-07.md` read in full: `notified: 2026-09-07T18:44:54`,
  `nudged:` empty, no `decision:`.

## Correction to the 23rd check's own age arithmetic on `IDLE-2026-09-07`

The 23rd check's notebook computed the item's age as "17h38m old" by diffing
UTC wall-clock (`2026-09-08T12:23:08`) directly against the frontmatter
`notified: 2026-09-07T18:44:54` as if that field were also UTC. It is not.
Cross-referenced against `traces/eng-notify-2026-09-07.log`, which logs via
bare `date '+%H:%M:%S'` (no `-u`, i.e. local system time — confirmed this
pass, system `TZ` is `PDT -0700`): the log's own line for this item reads
`[18:44:54] sent: active IDLE-2026-09-07.md`, matching the frontmatter value
to the second. So `notified:` is stamped in **local PDT**, not UTC, despite
the Z-less ISO-8601 shape inviting a UTC read.

Recomputed correctly (local-to-local): current local time this pass,
`2026-09-08T05:55:42 PDT`, against `notified: 2026-09-07T18:44:54` →
**~11h11m old**, not 17h38m. Both figures land under the 24h nudge
threshold, so the 23rd check's conclusion (no nudge owed) was right despite
the wrong arithmetic behind it, and nothing this pass did depended on the
figure either way.

This is the identical bug `proposals.md` line 91 already names (agents
computing "current time" via inconsistent conventions — some `date -u`,
some local `date` — before diffing against a `notified:`/`nudged:` field
that is always stamped in local time), now caught a further time, this time
in a notebook's own reasoning rather than in a wrong nudge action. **Not
re-filed** — the existing proposal (still `## Open`, unapproved) already
covers this exact pattern and root cause; a fresh row would be double-filing
the same finding under a new date for no new information, which
`proposals.md`'s own guidance (and this ticket's 23rd-check precedent on the
repo-isolation slip) both argue against. Noted here only so the correct
figure is on record and the next check doesn't propagate the wrong one.

- Runaway-guard counters, read directly from `traces/.hops-2026-09-08` and
  `traces/.hops-2026-09-08-ENG-027`: `day 12/200`, `ENG-027 11/20` — both up
  by exactly 1 from the 23rd check's `11/200`/`10/20`, consistent with this
  being the one hop this pass itself consumes. Cross-checked against
  `plan.tier: max_5x` (`hops_per_day: 200`, `hops_per_ticket: 20`) in
  `departments/engineering/agents/eng-manager/config.yaml`. Nowhere near
  either ceiling.
- Fresh, field-anchored `exception-request:` sweep on `ENG-027`'s own log:
  none found.

No divergence found in any board-state fact. Same conclusion as
confirmations 5 through 23 and the intervening `scheduled` sweeps,
independently re-derived from live `gh`/`grep`/frontmatter reads rather than
copied from the checkpoint or the prior notebook entry.

## The untracked `deno.lock` files — checked, unchanged, not re-filed

`git status --short` in the department's `_eng/aiorders-api` worktree (on
branch `feat/ENG-049-loyalty-webhook-accrual-sweep-and-dine-in-earn-api`)
still shows the same three untracked files (`brand-portal`,
`loyalty-auto-complete`, `restaurant-marketplace` — each `deno.lock`),
timestamped `2026-09-07 18:25:00`, i.e. predating even the 22nd check. This
exact finding is already logged (`observations.md`, 2026-09-07 row):
assessed harmless (byproduct of `ENG-049`'s own already-completed
verification hops, `.gitignore` doesn't cover them, no active work
disturbed), not a died-mid-work situation (checkout matches the most
recently active ticket). Unchanged since that row was written — not a new
occurrence, so not re-logged.

## Not done this pass, deliberately

Did not fall back to the `designed`-state pool — still the approver's call,
per the open proposal. Did not duplicate `IDLE-2026-09-07.md` or nudge it
(~11h11m old, under 24h). Did not touch `board/_index.md` — established
convention since roughly the 12th confirmation is that a `continue
ENG-027` idle pass which changes no ticket state and creates no new board
entry leaves the index alone. Did not re-file the `deno.lock` observation or
the timestamp-arithmetic finding — both already on record, unchanged. Did
not fire `lib/eng-trigger.sh` for any ticket — nothing on the board is
startable.

## Outcome

`chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged, not
duplicated (24th consecutive confirmation)`. No new proposal or observation
filed — the two things checked closely this pass (the `deno.lock` leftovers,
the notified-timestamp arithmetic) were both already on record and
unchanged. Post-pass `lib/eng-gate-check.sh`, scoped and whole-board: run
after this file and the ticket log are written. business-os left
uncommitted — standing default, commit-convention question still open.
