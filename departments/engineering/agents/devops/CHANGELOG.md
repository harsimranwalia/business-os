# devops — changelog

Behavioural changes to this agent, newest last. Versions are derived from git
history scoped to `agents/devops/` — see `lib/agent-version.sh`. Roll one back with
`lib/agent-rollback.sh devops <version>`.

Append only. A reverted change is not deleted here; the rollback appends its own
entry. Cost and approve/reject outcomes per version come from
`lib/cost-report.py --by version`.

<!-- Seeded from git history on 2026-08-18. Seeded entries carry
     no Why — git recorded a reason per COMMIT, never per agent. -->

## v1 — 2026-07-27 — b885af5
Changed:  Add the engineering department — 10 agents that build software end-to-end
Source:   git

## v2 — 2026-07-27 — 5876e27
Changed:  Plan tier is a setting, not a design constraint
Source:   git

## v3 — 2026-08-11 — 4037a7e
Changed:  eng: ENG-003 through its first review gate, and the gate skills it exercised
Source:   git

## v4 — 2026-08-12 — 6efebab
Changed:  eng: close out the ENG-004 release — subs verified, release record, proof entry
Source:   git

