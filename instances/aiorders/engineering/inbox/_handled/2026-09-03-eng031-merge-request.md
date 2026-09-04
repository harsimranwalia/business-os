---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-api
ticket: ENG-031
recommendation: merge — code review, QA, security, and migration gates all
  passed; additive schema-only change (two nullable columns), no reachable
  code path yet, inert until ENG-033 ships; single repo, no cross-ticket
  branch dependency
time_estimate: ~1-2h (S band, definition-of-done.md)
pr_url: https://github.com/harsimranwalia/aiorders-api/pull/12
raised: 2026-09-03
notified: 2026-09-04T01:46:26
nudged:
decision:
---

# Merge request — Add order-capture columns to catering (ENG-031)

## What this does

Two new nullable columns on `public.catering`: `action_type text` and
`selections jsonb`, added via `add column if not exists` with a column
comment on each. No default, no `NOT NULL`, no `CHECK`, no enum type, no
index. Schema-only, inert until `ENG-033` starts writing to it — no
endpoint, handler, or frontend touched anywhere in this diff. Step 1 of 4 in
`ENG-016`'s (catering quote generator) work-breakdown; `ENG-032` and
`ENG-033` both `depends_on` this ticket. Full trace: `ENG-031`'s own board
file and PRD.

## Gates passed

- Code review: **pass** — `agents/principal-engineer/reviews/ENG-031.md`
- QA: **pass** — `agents/qa/test-plans/ENG-031.md` (no suite applies — pure
  DDL diff)
- Security: **pass** — `agents/security/reviews/ENG-031.md` (0 blocking
  findings; one non-blocking finding routed to `ENG-033`, see PR body)
- Migration: **pass** — `agents/database/migrations/ENG-031-catering-order-capture-migration.md`

## PR

https://github.com/harsimranwalia/aiorders-api/pull/12
