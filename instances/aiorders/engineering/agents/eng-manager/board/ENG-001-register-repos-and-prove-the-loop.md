---
id: ENG-001
title: Register this business's repos and prove the loop runs end to end
project: aiorders
type: chore
size: S
severity: P3
priority: now
state: shaped
owner: product-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-23
updated: 2026-08-25
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-001-register-repos-and-prove-the-loop.md
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
- `2026-08-25` `intake → shaped` (product-manager) — PRD written at
  `agents/product-manager/specs/ENG-001-register-repos-and-prove-the-loop.md`.
  Read the ticket's own criteria back rather than running the full
  request-readback ceremony (already a spec — see PRD). **AC1/AC2/AC3
  confirmed already satisfied** on re-check this pass: `config/projects.md`
  carries all five repos at L1 (approved 2026-07-28, re-verified
  2026-08-23); all five worktrees present under `~/Documents/projects/_eng/`;
  `lib/eng-gate-check.sh` re-run clean, exit 0. **AC4 open** — no second
  ticket exists yet. `type: chore` auto-skips G1 per
  `config/templates/prd.md`, so no gate item raised; PRD status recorded as
  `approved` directly. Not proceeding to `designed` in this pass — see the
  next line.
- `2026-08-25` note (product-manager) — **AC4 satisfied.** Found a genuine
  approver-filed request already sitting in `inbox/requests/` since
  2026-08-23 (`test-harness.md`) — not a self-originated finding, so no
  conflict with the department's-own-work rule. Ran it through the full
  request-readback (this PM's reading + a blind architect reading; no
  material divergence) and shaped it into `ENG-002` (`intake → shaped →
  awaiting-scope`, `agents/eng-manager/board/ENG-002-*.md`), a smoke-test
  harness for `restaurant-portal`. `ENG-002` reached `shaped` en route to
  `awaiting-scope` (its `size: M` requires G1, unlike this ticket's
  auto-skipped chore), which satisfies this ticket's AC4 literally: "one
  real ticket has moved intake → shaped." All four acceptance criteria are
  now met. Source request moved to `inbox/_handled/2026-08-23-test-harness.md`.
- `2026-08-25` note (product-manager) — **Not advancing this ticket past
  `shaped` this pass, deliberately.** What "building" (branch pushed,
  self-tested, PR body written) means for a ticket whose own deliverable is
  config/registry verification and another ticket — not application code in
  any registered repo — is not addressed anywhere in this department's docs
  (checked `schedules/eng_build_loop.md`, `docs/engineering-team.md`,
  `config/definition-of-done.md`, both `agent.md` files for architect and
  eng-manager). All four ACs are satisfied, so nothing is actually blocked —
  but deciding how a config-only, no-code ticket earns its three enforced
  receipts (review/test-plan/security) is a real design call, arguably worth
  an ADR since it sets precedent for every future instance's own ENG-001.
  Leaving it for the architect with a fresh pass rather than guessing it here.
  `chained: ENG-001` — sitting at `shaped`, owned by the architect (agent,
  not approver, not blocked, not terminal).
