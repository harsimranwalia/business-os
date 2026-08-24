---
id: ENG-001
title: Register this business's repos and prove the loop runs end to end
project: aiorders
type: chore
size: S
severity: P3
priority: now
state: intake
owner: product-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-23
updated: 2026-08-24
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

## Log

Append-only. One line per state transition, newest last.

- `2026-08-24` note (eng-manager) — gate-check-unavailable incident
  (`inbox/2026-08-24-eng-gate-check-unavailable.md`, raised against this ticket
  because it was in flight when the pre-pass check found `lib/eng-gate-check.sh`
  absent/unreadable) resolved. Root cause fixed in business-os `9366b84` (nine
  `$ROOT/lib/` call sites repointed to `$ENG_DEPT/lib/` after the carve-out).
  Approver decision: **approved**, 2026-08-24T17:00:57Z. Independently re-ran
  `lib/eng-gate-check.sh` against this instance this pass: exit 0, clean. **AC3
  satisfied.** AC1/AC2/AC4 untouched by this pass.
- `2026-08-24` chained: ENG-001 (eng-manager) — this pass was scoped to the
  answered gate only; firing `continue` so the PM can pick up shaping at
  `intake` with a fresh pass.
