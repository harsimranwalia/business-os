---
id: ENG-001
title: Register this business's repos and prove the loop runs end to end
project: aiorders
type: chore
size: S
severity: P3
priority:
state: intake
owner: product-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-23
updated: 2026-08-23
branch:
depends_on: []
blocks: []
parent:
links:
  prd:
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
---

# Register this business's repos and prove the loop runs end to end

The seed ticket every instance starts with. It exists for two reasons.

**First, a board with nothing on it is not a clean board.** `lib/eng-gate-check.sh`
fails closed on an empty board directory, deliberately — the riskiest failure in
this department is a root that resolves somewhere real and empty, which under a
permissive rule would print nothing and exit 0. This ticket is what makes a fresh
instance distinguishable from a misresolved one.

**Second, it is genuinely the first work.** Nothing can be built until the repos
are registered.

## Acceptance criteria

1. Every repo this business owns is registered in `config/projects.md` at **L1**,
   via `skills/repo-onboarder/SKILL.md`, and the approver has approved each.
2. A department-owned git worktree exists under `_eng/` for each registered repo.
3. `lib/eng-gate-check.sh` exits 0 against this instance.
4. One real ticket has moved `intake → shaped` and the board renders it.

## Notes

Close this ticket once the first real ticket is on the board — not before, or the
board is empty again.
