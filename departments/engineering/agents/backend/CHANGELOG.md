# backend — changelog

Behavioural changes to this agent, newest last. Versions are derived from git
history scoped to `agents/backend/` — see `lib/agent-version.sh`. Roll one back with
`lib/agent-rollback.sh backend <version>`.

Append only. A reverted change is not deleted here; the rollback appends its own
entry. Cost and approve/reject outcomes per version come from
`lib/cost-report.py --by version`.

<!-- Seeded from git history on 2026-08-18. Seeded entries carry
     no Why — git recorded a reason per COMMIT, never per agent. -->

## v1 — 2026-07-27 — b885af5
Changed:  Add the engineering department — 10 agents that build software end-to-end
Source:   git

## v2 — 2026-07-27 — 96c7d1d
Changed:  Engineering dept: speed — event triggers, split WIP, parallel gates
Source:   git

## v3 — 2026-08-05 — 5a72b69
Changed:  engineering: ENG-006 gate-check script + the ENG-004 receipt design
Source:   git

## v4 — 2026-08-12 — ecc37bd
Changed:  eng: port the receipt check to POSIX sh, stop a dead pass eating its event
Source:   git

