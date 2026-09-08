# ENG-027 continue — sixteenth consecutive idle re-confirmation

`continue` event, context `ENG-027`. Reading map for `continue`: steps 6 and
6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*;
*The four lanes*; *Guards*) — read the full procedure document this pass
regardless, per the map-is-a-floor rule.

Mode check: repo-root `.env` → `MODE=active`.

Treated the prompt's checkpoint (copied from this ticket's own line-978
entry, the fifteenth confirmation) as untrusted per its own instruction, and
re-derived independently rather than trusting the copy:

- `ENG-027` frontmatter read fresh: `state: building`, `priority: now`,
  `parent:` empty, `depends_on: [ENG-006, ENG-007]` (both long
  shipped/verified — not re-derived again).
- `ENG-048`/`ENG-049` frontmatter read fresh: both `state: blocked`,
  `owner: approver`, `blocked_on: approver`, `blocked_from: ready-to-ship`,
  `parent: ENG-027`. `ENG-048 depends_on: []`, `ENG-049 depends_on:
  [ENG-048]`.
- Board-wide `grep -rl "parent: ENG-027"` → exactly `ENG-048.md` and
  `ENG-049.md`. No third child.
- PR state, checked live from the department's dedicated worktree
  (`~/Documents/projects/_eng/aiorders-api`, per `config/projects.md`'s
  "Working copies" section — not the human's interactive checkout):
  `git fetch origin main`, then `gh pr view {21,22} --json
  state,baseRefName,mergedAt`: `#21` → `OPEN`, base `main`, `mergedAt:
  null`; `#22` → `OPEN`, base
  `feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron` (still
  stacked), `mergedAt: null`. Unchanged from the fifteenth check.
- Machine WIP: full whole-board frontmatter sweep this pass. Nothing sits
  in `ready`..`ready-to-ship` anywhere. Per Guards' 2026-09-07(b) amendment
  the `ENG-027` container holds no slot while both children are parked.
  `0/1`, genuinely free.
- To-do column (`intake`/`shaped`/`awaiting-scope`) unchanged: `ENG-018`
  (`awaiting-scope`), `ENG-028` (`awaiting-scope`), `ENG-042`
  (`awaiting-scope`), `ENG-043` (`intake`). Checked every top-level
  `inbox/*.md` file for a populated `^decision:` field (fresh grep, all
  ten files, not just the four candidates' own items): none present
  anywhere. None answered.
- `inbox/IDLE-2026-09-07.md` read in full: `notified: 2026-09-07T18:44:54`,
  `nudged:` empty, no `decision:`. Current wall clock `2026-09-08 01:38`
  PDT (`date` command, this pass) — ~6h53m old, still well under the 24h
  nudge threshold (and the timestamp convention is local wall-clock, per
  the timezone-skew finding on `proposals.md`'s 2026-09-07 eng-manager row
  — not diffed naively against UTC). Content re-checked against everything
  above (all four candidates, their blocking items, `ENG-050`'s exclusion):
  still accurate, not stale, not duplicated.
- Swept every other open top-level `inbox/` item for `notified:`/`nudged:`/
  `decision:`: the four G1 items (`eng018`, `eng028`, `eng042`, `eng043`)
  and `PROP-2026-W36` each already carry their one-ever `nudged:` stamp (no
  re-nudge due, ever). `ENG-048`'s merge request (`notified:
  2026-09-07T16:18:23`, ~9h20m old), `ENG-049`'s (`notified:
  2026-09-07T18:44:54`, ~6h53m old), and `ENG-050`'s P0 notice (`notified:
  2026-09-07T16:04:16`, ~9h34m old) are all still under 24h with no
  `nudged:` yet — none due. No file anywhere under `inbox/` carries a
  populated `decision:`. Nothing raised, nothing nudged this pass. Fresh
  `exception-request:` sweep across every board file: none found.
- `ENG-050` board file re-read live: `state: designed`, `owner: architect`.
  Unchanged, still correctly outside To-do's auto-start set.
- `proposals.md`'s `## Open` section (lines 22–92): both the devops
  "designed-pool" tension row (line 89) and the eng-manager
  idle-recurrence-pattern row (line 91, both dated 2026-09-07) confirmed
  still present, still open, untouched — both sit before line 93's `##
  Approved` header. Left alone — resolving the underlying policy question
  is the approver's call via the batched G1, not this pass's to pre-empt,
  and this pass is the same recurrence the second proposal already
  documents, not a new finding requiring a third.
- Runaway-guard counters, read from `traces/eng-loop-2026-09-08.log`
  directly: this fire logged `[day 3/200 charged, 0 refunded today,
  ENG-027 3/20]` at pass start (01:37:14). Both counters reset at the
  calendar rollover to 09-08 (noted by the fourteenth check) and are now on
  their third hop of the new day. Tier `max_5x`
  (`agents/eng-manager/config.yaml` → `plan.tier`), both budgets nowhere
  near their ceiling.
- Pre-pass `lib/eng-gate-check.sh`: first invocation (bare, from
  `departments/engineering/`, no `ENG_ROOT`) was invalid tooling — it
  defaults to deriving `ROOT` from the script's own location
  (`departments/engineering`), which has no `agents/eng-manager/board` at
  all, and separately, its exit code was masked by piping through `tail`.
  Corrected per `lib/eng-trigger.sh`'s own invocation pattern
  (`env ENG_ROOT="$ENG_INSTANCE" sh lib/eng-gate-check.sh`) — POSIX `sh`,
  not `zsh`, and `ENG_ROOT` pinned to this instance. Re-run scoped
  (`ENG-027`) and whole-board, exit code checked directly (not through a
  pipe): both exit 0, clean.

No divergence found anywhere. Same conclusion as confirmations four through
fifteen, independently re-derived rather than copied.

## Not done this pass, deliberately

Did not fall back to the `designed`-state pool (`ENG-050`) or relitigate
that open question. Did not file a third observation or a further proposal
on the repeated-idle pattern — the eng-manager row already on
`proposals.md` covers exactly this recurrence, and does not need a running
tally updated on every re-confirmation. Did not touch `board/_index.md` —
still exactly three dated entries (all 2026-09-07, fifth–seventh
confirmations), under the keep-three cap, unaffected by this ticket-scoped
pass and its In-flight table row still accurate for every ticket checked.
Did not re-verify `ENG-006`/`ENG-007` — both long shipped/verified. Did not
fire `lib/eng-trigger.sh` for any ticket — nothing on the board is
startable, and re-firing `continue ENG-027` itself on an unchanged ticket is
exactly the "burning usage" case the procedure warns against. Did not touch
the stale `inbox/2026-09-04-eng016-continue-piece2-question.md` item
(`ENG-016` is already `verified`; an orphaned artifact, not a blocker, and
outside this event's scope).

## Outcome

`chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged, not
duplicated (16th consecutive confirmation)`. Post-pass
`lib/eng-gate-check.sh`, scoped and whole-board: run after this file and the
ticket log are written. business-os left uncommitted — standing default,
commit-convention question still open.
