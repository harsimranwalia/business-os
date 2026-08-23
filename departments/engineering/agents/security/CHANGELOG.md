# security — changelog

Behavioural changes to this agent, newest last. Versions are derived from git
history scoped to `agents/security/` — see `lib/agent-version.sh`. Roll one back with
`lib/agent-rollback.sh security <version>`.

Append only. A reverted change is not deleted here; the rollback appends its own
entry. Cost and approve/reject outcomes per version come from
`lib/cost-report.py --by version`.

<!-- Seeded from git history on 2026-08-18. Seeded entries carry
     no Why — git recorded a reason per COMMIT, never per agent. -->

## v1 — 2026-07-27 — b885af5
Changed:  Add the engineering department — 10 agents that build software end-to-end
Source:   git

## v2 — 2026-07-27 — 9273379
Changed:  Engineering dept: PM becomes the front door, plus five review fixes
Source:   git

## v3 — 2026-08-11 — 29b3fdc
Changed:  housekeeping: engineering board state from the 2026-08-11 passes
Source:   git

## v4 — 2026-08-12 — 62ce1e9
Changed:  eng: ENG-007 round-2 fail and rework — the fail-path receipt write is gone from the standard that outranked the fix
Source:   git

## v5 — 2026-08-12 — 030acc0
Changed:  eng: release ENG-004 — the department's gate receipts are wired and enforced
Source:   git

## v6 — 2026-08-13 — aaf0eb3
Changed:  eng: board becomes five columns, three tickets close, and a dead pass's partial is kept
Source:   git

