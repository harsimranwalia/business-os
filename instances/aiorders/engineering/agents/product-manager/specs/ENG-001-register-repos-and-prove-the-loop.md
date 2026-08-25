---
ticket: ENG-001
project: aiorders
status: approved          # auto-approved — type: chore skips G1 (definition-of-done.md → Size)
size: S
author: product-manager
created: 2026-08-25
decided: 2026-08-25       # auto-approved, no G1 raised
---

# Register this business's repos and prove the loop runs end to end

## Readback

This is already a spec — the ticket was created with its acceptance criteria
written directly on it (`source: approver`), so the full two-blind-readings
ceremony doesn't apply (`skills/request-readback/SKILL.md` → "When this does
NOT run" → "a request that is already a spec"). Reading it back in one pass
instead.

**You said (the ticket's own acceptance criteria, verbatim):**
1. "Every repo this business owns is registered in `config/projects.md` at
   **L1**, via `skills/repo-onboarder/SKILL.md`, and the approver has approved
   each."
2. "A department-owned git worktree exists under `_eng/` for each registered
   repo."
3. "`lib/eng-gate-check.sh` exits 0 against this instance."
4. "One real ticket has moved `intake → shaped` and the board renders it."

**Understood as:** this is the seed ticket every fresh instance carries —
prove the engineering department can actually run against AIOrders before any
real product ticket is trusted to it. Two of its four criteria are
config/registry facts (repos registered and checked out), one is a mechanical
check on the department's own tooling, and the last is proof the pipeline can
carry a ticket at all.

**Second reading:** skipped for the same reason as above (already a spec).

## Problem

Nothing can be built for AIOrders until (a) the department knows which repos
it's allowed to touch and how far, and (b) there's evidence the board's own
machinery — the one enforced check standing between "moved" and "moved by a
legal route" — actually runs clean on this instance. Without this, every
downstream ticket would be the first thing to discover a broken registry or a
silently-failing gate check.

## Why now

First work, by construction — everything else on this board depends on it
transitively.

## Users

The department itself (this is infrastructure, not a user-facing change) and,
through it, the approver — this is what lets them stop being asked to
register repos or babysit the loop by hand.

## Proposed change

No application behaviour changes. The department's own state
(`config/projects.md`, `_eng/` worktrees) is confirmed correct, and the
board is proven to carry at least one ticket through its front door.

## Acceptance criteria

1. `[stated]` Every repo AIOrders owns is registered in
   `agents/eng-manager/config/projects.md` at L1, and the approver has
   approved each. — **Already satisfied**, carried over from the life-os
   registry (approved 2026-07-28) and re-verified against the working trees
   on 2026-08-23: all five (`aiorders-api`, `aiorders-admin-hub`,
   `config-site-builder`, `restaurant-marketplace`, `restaurant-portal`) are
   listed at L1 with stack, deploy target, and commands read from each repo's
   own `package.json` rather than guessed.
2. `[stated]` A department-owned git worktree exists under `_eng/` for each
   registered repo. — **Already satisfied**: confirmed present on disk this
   pass (`~/Documents/projects/_eng/{aiorders-api, aiorders-admin-hub,
   config-site-builder, restaurant-marketplace, restaurant-portal}`).
3. `[stated]` `lib/eng-gate-check.sh` exits 0 against this instance. —
   **Already satisfied**: independently re-run this pass, exit 0, no
   violations.
4. `[stated]` One real ticket has moved `intake → shaped` and the board
   renders it. — **Open.** This is the one criterion this ticket still owes;
   see Non-goals and Risks below for how it's being closed out.

## Non-goals

- Does not raise any project's autonomy above L1 — that's the approver's call
  alone, and none has been asked for.
- Does not onboard the repos explicitly excluded in `config/projects.md`
  (`GoogleMaps-Scraper`, `OpenWA`, `ringcentral`, `twenty-crm`, etc.) — they
  were never approved and this ticket doesn't reopen that.
- Does not itself write application code in any of the five registered
  projects. AC4 is satisfied by getting a ticket through intake, not by this
  ticket producing product work.

## Risks and unknowns

- **AC4's shape is genuinely ambiguous** and is called out explicitly rather
  than resolved by guessing: the department is under a hard rule that it
  "cannot commission itself" — agent-originated findings (QA bugs, security
  findings, devops incidents, architect tech debt) must become one line in
  `agents/eng-manager/proposals.md`, not a ticket, and only the approver's
  batched G1 promotes one. `agents/eng-manager/config/projects.md` already
  names the missing-test-infrastructure gap and points at a prior-art pattern
  (Verido-CRM's own ENG-002, a smoke-test harness, created directly rather
  than proposed) — but that precedent hasn't been independently confirmed yet.
  The architect's design step for this ticket resolves which route AC4 takes;
  this PRD does not pre-empt that call.
- **This ticket has no application-code deliverable**, which makes its own
  `building → in-review → in-qa → in-security` stretch of the full lane an
  unusual fit (those states assume a branch and a PR in a registered project
  repo). Flagged for the architect's design rather than decided here — the PM
  writes the problem, not the pipeline mechanics.

## Cost

- Build: S — no code, config/registry verification plus getting one ticket
  to `shaped`.
- Run: $0/month. No new infrastructure, no deployed endpoint, no API billing.

## Decision

- **The approver's answer:** auto-approved — `type: chore` skips G1 per
  `agents/eng-manager/config/definition-of-done.md` → Size table ("S ...
  Yes, unless bug/chore") and `config/templates/prd.md` ("Auto-approved types
  skip G1 (XS, bug, chore, security)").
- **Date:** 2026-08-25
- **Notes:** No approver decision needed or raised; recorded here for the
  audit trail the gate would otherwise have left.
