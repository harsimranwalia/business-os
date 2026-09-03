---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-api
ticket: ENG-024
recommendation: merge — code review, suite, and OWASP all passed (fast-lane combined gate); backfill migration is low-risk (assessed informally against the migration gate's own failure conditions, no dedicated database-gate verdict exists on this lane — see PR body); single repo, no cross-ticket branch dependency
time_estimate: under an hour (XS band, definition-of-done.md)
pr_url: https://github.com/harsimranwalia/aiorders-api/pull/11
raised: 2026-09-03
notified: 2026-09-03T10:58:15
nudged:
decision:
---

# Merge request — Set show_in_marketplace on onboarding's createRestaurant insert, plus backfill (ENG-024)

## What this does

Every restaurant added through the FoodSwipe/AIOrders sign-up flow was
inserted with `approved: true` but never `show_in_marketplace: true`, so
every marketplace search path silently excluded it — no error to the owner,
no signal to staff that a manual admin toggle was still needed. The fix adds
the missing field to the insert and backfills existing affected rows with a
one-time, narrowly-scoped `UPDATE` (excludes the separate `restaurant-claims`
path by construction). Full trace: `ENG-024`'s own board file and PRD.

**P1** — every restaurant onboarded through this flow to date has been
invisible in the marketplace search customers actually use.

## Gates passed

- Code review + suite + OWASP (fast-lane combined gate): **pass** —
  `agents/principal-engineer/reviews/ENG-024.md`
- Migration: no dedicated `database`-gate verdict exists on this lane (fast
  lane has no path that triggers `schema-change/SKILL.md` — see the PR body
  and `agents/eng-manager/proposals.md`, 2026-09-03 row, for the mechanism
  gap). Assessed informally, low-risk, by both principal-engineer's review
  and devops's own independent read of the migration SQL this hop.

## PR

https://github.com/harsimranwalia/aiorders-api/pull/11
