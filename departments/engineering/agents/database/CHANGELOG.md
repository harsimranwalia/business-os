# database — changelog

Behavioural changes to this agent, newest last. Versions are derived from git
history scoped to `agents/database/` — see `lib/agent-version.sh`. Roll one back with
`lib/agent-rollback.sh database <version>`.

Append only. A reverted change is not deleted here; the rollback appends its own
entry. Cost and approve/reject outcomes per version come from
`lib/cost-report.py --by version`.

<!-- Seeded from git history on 2026-08-18. Seeded entries carry
     no Why — git recorded a reason per COMMIT, never per agent. -->

## v1 — 2026-07-27 — b885af5
Changed:  Add the engineering department — 10 agents that build software end-to-end
Source:   git

