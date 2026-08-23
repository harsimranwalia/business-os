# eng-manager — changelog

Behavioural changes to this agent, newest last. Versions are derived from git
history scoped to `agents/eng-manager/` — see `lib/agent-version.sh`. Roll one back with
`lib/agent-rollback.sh eng-manager <version>`.

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

## v3 — 2026-07-27 — 96c7d1d
Changed:  Engineering dept: speed — event triggers, split WIP, parallel gates
Source:   git

## v4 — 2026-07-27 — d0a3a41
Changed:  Engineering dept: make the loop genuinely event-driven, not cron
Source:   git

## v5 — 2026-07-27 — 3e3e820
Changed:  Engineering dept: notify Harry when a decision is waiting
Source:   git

## v6 — 2026-07-27 — c11fed8
Changed:  Engineering event loop: fix 8 defects found in review
Source:   git

## v7 — 2026-07-27 — 5876e27
Changed:  Plan tier is a setting, not a design constraint
Source:   git

## v8 — 2026-07-27 — 9fa3ecf
Changed:  Make "what a real team does better" real, not a disclaimer
Source:   git

## v9 — 2026-07-27 — 42b34c0
Changed:  Readback: prove the request was understood before building from it
Source:   git

## v10 — 2026-07-28 — aae3180
Changed:  feat(engineering): register business-os + aiorders sub-repos; fix multi-repo worktrees
Source:   git

## v11 — 2026-07-28 — 39feb30
Changed:  fix(engineering): skip watch re-fires from inbox subfolder churn before launch
Source:   git

## v12 — 2026-07-28 — a546607
Changed:  engineering: business-os is live — initial commit + worktree created
Source:   git

## v13 — 2026-07-29 — 9e9be84
Changed:  Housekeeping: agent-run notebooks, staging, and pipeline churn (2026-07-28..29)
Source:   git

## v14 — 2026-07-30 — 5e98df3
Changed:  engineering: register Verido-CRM at L1
Source:   git

## v15 — 2026-07-30 — d8ca8bf
Changed:  engineering: ENG-001 intake — Verido-CRM 7-touchpoint funnel PRD, G1 raised
Source:   git

## v16 — 2026-07-31 — 4c4afb0
Changed:  engineering: ENG-001 build-through-PR, control-center gate UX, Slack changed-decision path
Source:   git

## v17 — 2026-07-31 — f41cf5a
Changed:  engineering: ENG-001 PR approved + Akshat-reviewed, surface blocked-on-harry tickets in control center
Source:   git

## v18 — 2026-07-31 — 90a7b97
Changed:  engineering: ENG-001 merged + verified; file ENG-003 (no RLS) and ENG-004 (gate bypass)
Source:   git

## v19 — 2026-07-31 — 0e29309
Changed:  engineering: ENG-003 design — RLS gap is five tables, not two; G2 raised
Source:   git

## v20 — 2026-08-05 — 5a72b69
Changed:  engineering: ENG-006 gate-check script + the ENG-004 receipt design
Source:   git

## v21 — 2026-08-11 — 29b3fdc
Changed:  housekeeping: engineering board state from the 2026-08-11 passes
Source:   git

## v22 — 2026-08-11 — 4037a7e
Changed:  eng: ENG-003 through its first review gate, and the gate skills it exercised
Source:   git

## v23 — 2026-08-11 — d48fa9b
Changed:  fix: board-fired triggers were Mac-only — every VPS agent run died at exec
Source:   git

## v24 — 2026-08-12 — 62ce1e9
Changed:  eng: ENG-007 round-2 fail and rework — the fail-path receipt write is gone from the standard that outranked the fix
Source:   git

## v25 — 2026-08-12 — 7da140e
Changed:  eng: cut what every build-loop pass carries — pin the model, archive the board log, grep before editing
Source:   git

## v26 — 2026-08-12 — 030acc0
Changed:  eng: release ENG-004 — the department's gate receipts are wired and enforced
Source:   git

## v27 — 2026-08-12 — 6efebab
Changed:  eng: close out the ENG-004 release — subs verified, release record, proof entry
Source:   git

## v28 — 2026-08-12 — ecc37bd
Changed:  eng: port the receipt check to POSIX sh, stop a dead pass eating its event
Source:   git

## v29 — 2026-08-13 — 55ad332
Changed:  eng: ENG-005 round-2 rework — the alarm no longer depends on a pass succeeding
Source:   git

## v30 — 2026-08-13 — 5647051
Changed:  eng: recover ENG-005/ENG-009 round-3 gate verdicts — reviewing session died on spend limit before committing
Source:   git

## v31 — 2026-08-13 — 36e3db9
Changed:  eng: commit the day's policy work — the internal lane, proposals, priority, and two verified tickets
Source:   git

## v32 — 2026-08-13 — 2f3e54e
Changed:  eng: second data point on stale queued events — a decision event outliving its handled item
Source:   git

## v33 — 2026-08-13 — aaf0eb3
Changed:  eng: board becomes five columns, three tickets close, and a dead pass's partial is kept
Source:   git

## v34 — 2026-08-13 — b3db990
Changed:  eng: ENG-003 L1 release — PR #6 opened, merge request raised
Source:   git

