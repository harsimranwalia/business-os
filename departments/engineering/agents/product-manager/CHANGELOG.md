# product-manager — changelog

Behavioural changes to this agent, newest last. Versions are derived from git
history scoped to `agents/product-manager/` — see `lib/agent-version.sh`. Roll one back with
`lib/agent-rollback.sh product-manager <version>`.

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

## v3 — 2026-07-27 — 5876e27
Changed:  Plan tier is a setting, not a design constraint
Source:   git

## v4 — 2026-07-27 — 42b34c0
Changed:  Readback: prove the request was understood before building from it
Source:   git

## v5 — 2026-07-30 — d8ca8bf
Changed:  engineering: ENG-001 intake — Verido-CRM 7-touchpoint funnel PRD, G1 raised
Source:   git

## v6 — 2026-07-31 — 4c4afb0
Changed:  engineering: ENG-001 build-through-PR, control-center gate UX, Slack changed-decision path
Source:   git

