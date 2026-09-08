# ENG-026 child dispatch — ENG-044 shipped, ENG-045 selected over ENG-046

`continue` event pass, context `ENG-026`. Reading map for `continue`: steps 6
and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
instructed*, *The four lanes*, *Guards*). Mode check clean (`MODE=active`).
Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-026`) and whole-board: both
exit 0.

## What triggered this pass

`ENG-026` is the parent/container from its own 2026-09-07 work-breakdown
(`2026-09-07-eng026-work-breakdown.md`), sitting at `building` with four
children: `ENG-044` (database, no dependency, dispatched that pass),
`ENG-045`/`ENG-046` (both `depends_on: [ENG-044]`), `ENG-047`
(`depends_on: [ENG-045]`). That prior pass explicitly left this exact moment
for "a future `continue ENG-026`" to handle — this is that pass.

## ENG-044's state — verified, not trusted off one read

Read `ENG-044`'s frontmatter twice in quick succession while orienting:
first `state: blocked`/`owner: approver`, then (seconds later) `state:
shipped`/`owner: approver`, `blocked_on`/`blocked_from` both cleared. The
ticket's own log tail explains it: a `blocked → shipped` line stamped
"(control center, merge detected)" — the approver merged PR #19 on GitHub
and the dashboard wrote the transition live, mid-pass, between the two
reads. Not taken on faith either way — independently confirmed from the
department's own dedicated worktree (`~/Documents/projects/_eng/aiorders-api`,
never the approver's interactive checkout, per *Repo isolation*):

- `git fetch origin main`, then `git merge-base --is-ancestor
  origin/feat/ENG-044-foodswipe-channel-visibility-schema origin/main` →
  true.
- `gh pr view 19 --json state,baseRefName,mergedAt,mergeCommit,headRefName`
  → `state: MERGED`, `baseRefName: main`, `mergedAt:
  2026-09-07T16:03:56Z`.

Genuine merge, correctly reflected. No corruption, no partial write — just a
live dashboard update landing inside this pass's own read window.

## Dependency check

Guards, "Amended 2026-09-07 — two readings closed" (a): `depends_on` clears
once the upstream is `blocked` with `blocked_on: approver` and a PR open, or
any later state — never gated on the upstream reaching `verified`. `ENG-044`
at `shipped` is past that bar. Both `ENG-045` and `ENG-046`
(`depends_on: [ENG-044]` only, independent of each other) are now startable
for the first time. `ENG-047` (`depends_on: [ENG-045]`) stays unmet —
`ENG-045` hasn't even started.

## Which child, and why only one

This ticket's own work-breakdown notebook already named this exact fork
("Machine-WIP reading" section): dispatching `ENG-044` alone that pass, and
predicting that once it ships, "a future `continue ENG-026` ... will find
*two* children simultaneously startable ... still dispatches only one per
pass, same reasoning `ENG-021`'s own notebook already recorded ('one chained
`continue` fires one session at a time regardless of how many tickets are
technically startable ... the family still counts as one `1/1` slot either
way')," and named the tie-break in advance: "likely lowest-id (`ENG-045`)
absent a new reason, but not decided here."

No new reason surfaced to deviate. `ENG-045` is both the lower id and the
one that unblocks `ENG-047` downstream (`ENG-046` blocks nothing further) —
the two available heuristics agree. Dispatching `ENG-045`. `ENG-046` stays
`ready`, dependency satisfied but not its turn; a future `continue ENG-026`
(or a `scheduled`/`watch` step-5 sweep reaching the same fork) picks it up
next, same as this pass did for `ENG-045`.

## Machine WIP

Family-slot reading (`ENG-016`/`ENG-019`/`ENG-021`/`ENG-026` precedent)
unaffected: `1/1`, held by the `ENG-026` family throughout. Dispatching
`ENG-045` is not a second occupant.

## Not done this pass, deliberately

`ENG-044` was not carried to `verified` here — that's a different ticket's
own concern (acceptance-check territory), out of this `continue` event's
narrower contract (dead-end sweep: "no other ticket touched"). Left for
step-5 merge detection or a `scheduled`/`watch` sweep to do explicitly, or
to surface as an upstream-gate re-check inside `ENG-045`'s own building hop
— same shape `ENG-031`→`ENG-032` and others on this board already used,
where `shipped` (not `verified`) was what actually unblocked the next child.

One observation filed (`observations.md`, this date): the concurrent
control-center write caught mid-read on `ENG-044`, and how it was verified
rather than assumed either way.
