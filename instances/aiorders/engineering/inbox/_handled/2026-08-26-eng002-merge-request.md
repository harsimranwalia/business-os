---
type: eng-decision
agent: eng-manager
gate: merge
project: restaurant-portal
ticket: ENG-002
recommendation: merge — code review, quality, and security all passed; dev-only change, nothing deployed
pr_url: https://github.com/harsimranwalia/restaurant-portal/pull/1
raised: 2026-08-26
notified: 2026-08-26T11:01:46
---

# Merge request — Add a smoke-test harness to restaurant-portal

## What this does

`restaurant-portal` gets a real `npm run test` command and one smoke test
that fails if the build breaks or the login route stops rendering — the
first real test on any AIOrders repo. No application behaviour changes,
nothing deployed, $0/month.

## Gates passed

- Code review: **pass** — `agents/principal-engineer/reviews/ENG-002.md`
- Quality (suite green, 1/1): **pass** — `agents/qa/test-plans/ENG-002.md`
- Security: **pass** — `agents/security/reviews/ENG-002.md`

## PR

https://github.com/harsimranwalia/restaurant-portal/pull/1

restaurant-portal is registered **L1** — this department opens the PR, a
human merges it. Merge whenever suits you on GitHub directly; the next
build-loop pass detects the merge itself (local git ancestry check, no
action needed from you beyond the merge) and advances the ticket to
`shipped`.

## Decision

Not filled in by the approver in this file — merged directly on GitHub
instead (PR #1, merge commit `b3a81ef`), the alternative this item's own text
offered ("Merge whenever suits you on GitHub directly"). Recorded here by the
`scheduled` pass that detected it 2026-08-26, via local git ancestry
(`git merge-base --is-ancestor chore/ENG-002-smoke-test-harness origin/main`),
independent of the direct `state: shipped` edit a separate "control center"
action had already made to the ticket file. Treated as resolved: the merge
itself is the decision. Ticket advanced to `verified` — see
`agents/eng-manager/board/ENG-002-restaurant-portal-smoke-test-harness.md`
and `agents/devops/releases/2026-08-26-restaurant-portal-ENG-002.md`.
