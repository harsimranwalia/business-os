# principal-engineer — changelog

Behavioural changes to this agent, newest last. Versions are derived from git
history scoped to `agents/principal-engineer/` — see `lib/agent-version.sh`. Roll one back with
`lib/agent-rollback.sh principal-engineer <version>`.

Append only. A reverted change is not deleted here; the rollback appends its own
entry. Cost and approve/reject outcomes per version come from
`lib/cost-report.py --by version`.

<!-- Seeded from git history on 2026-08-18. Seeded entries carry
     no Why — git recorded a reason per COMMIT, never per agent. -->

## v1 — 2026-07-27 — b885af5
Changed:  Add the engineering department — 10 agents that build software end-to-end
Source:   git

## v2 — 2026-08-05 — 5a72b69
Changed:  engineering: ENG-006 gate-check script + the ENG-004 receipt design
Source:   git

## v3 — 2026-08-11 — 4037a7e
Changed:  eng: ENG-003 through its first review gate, and the gate skills it exercised
Source:   git

## v4 — 2026-08-12 — 62ce1e9
Changed:  eng: ENG-007 round-2 fail and rework — the fail-path receipt write is gone from the standard that outranked the fix
Source:   git

## v5 — 2026-08-12 — 030acc0
Changed:  eng: release ENG-004 — the department's gate receipts are wired and enforced
Source:   git

## v6 — 2026-08-12 — ecc37bd
Changed:  eng: port the receipt check to POSIX sh, stop a dead pass eating its event
Source:   git

## v7 — 2026-08-13 — 5647051
Changed:  eng: recover ENG-005/ENG-009 round-3 gate verdicts — reviewing session died on spend limit before committing
Source:   git

## v8 — 2026-08-13 — 36e3db9
Changed:  eng: commit the day's policy work — the internal lane, proposals, priority, and two verified tickets
Source:   git

