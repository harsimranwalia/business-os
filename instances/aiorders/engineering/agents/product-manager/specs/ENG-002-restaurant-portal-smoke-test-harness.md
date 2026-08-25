---
ticket: ENG-002
project: restaurant-portal
status: approved
size: M
author: product-manager
created: 2026-08-25
decided: 2026-08-25
---

# Add a smoke-test harness to restaurant-portal

## Readback

**You said:** "No registered AIOrders project has a single test... That makes
the quality gate unenforceable rather than merely weak... Shape and scope
this. The department decides the shape — this is a problem statement, not a
design... Start with one repo, not five. `restaurant-portal` has a clean
working tree and already builds... `aiorders-api`... probably deserves its
own ticket rather than being folded into a frontend harness."
(`inbox/requests/2026-08-23-test-harness.md`, filed by Harry, 2026-08-23)

**Understood as:** Give one AIOrders repo — `restaurant-portal` by default —
a real, working test command and at least one real test that would actually
fail if the app broke, so the quality gate on this repo stops being
structurally unable to prove anything. The other three frontends and
`aiorders-api` are explicitly out of this ticket.

Two independent readings were run on the raw request — this PM's and, blind
to it, the architect's — per `skills/request-readback/SKILL.md`. They agreed
on scope, repo default, and test depth; the architect's reading sharpened the
problem statement below with a mechanism this PM's first pass didn't name,
and that sharper version is what's used here. No material divergence, so no
question was raised to the approver before writing this.

**Requirements, tagged by where they came from:**
1. `[stated]` One registered repo gets a real, runnable test command.
2. `[stated]` `aiorders-api`, the four repos' other three frontends, and
   comprehensive coverage are all out of scope for this ticket.
3. `[inferred]` "Real" means a test that would fail on a broken build or a
   route that stops rendering — not a placeholder that always passes.
4. `[proposed]` `restaurant-portal` is the repo, on the request's own
   technical read (clean tree, already builds) — not mandated, and the
   architect can pick a different one of the four frontends if design turns
   up a reason to.

**Assumed, and worth correcting if wrong:**
- "Before anything else ships" is read as urgency framing, not a literal
  instruction to hold other tickets on the board until this one ships. If
  that reading is wrong, this needs `priority: now` (or an explicit hold on
  other work) from the approver directly — that's not something to infer.
- The exact test framework is left to the architect's design step; this PRD
  deliberately doesn't name one (Vitest is the obvious fit for a Vite repo,
  but that's a design choice, not a requirement).
- No other repo is promised a follow-up ticket by this one. `aiorders-api`
  "probably" needs its own (it has no `package.json` to hang a script on,
  per the request) — that's a likely next proposal, not a commitment made
  here.

## Problem

`lib/eng-gate-check.sh` verifies a receipt file exists and is non-empty — it
never checks what's inside. `skills/test-suite-run/SKILL.md` already writes
an honest "no suite exists" result when a project has no test command, but
that write still produces a non-empty QA receipt. The net effect: the `full`
lane's quality gate is satisfied on every AIOrders ticket today regardless of
whether any test ever ran, because none of the five registered repos has one.
Verified 2026-08-23 (repeated in this pass): no `test` script in any
`package.json`, no `package.json` at all in `aiorders-api`, zero
`*.test.*`/`*.spec.*` files outside `node_modules` anywhere in the five repos.

This is also what's been holding ENG-001's AC4 open (`agents/eng-manager/board/ENG-001-*.md`)
— the department's seed ticket needs one real ticket to reach `shaped`, and
this gap is the first substantive piece of AIOrders work the registry itself
points at.

## Why now

Every AIOrders ticket after this one inherits a QA receipt that currently
proves nothing. The longer that's true, the more tickets ship on a gate that
was never real.

## Users

Not user-facing. This is for the department itself — specifically,
`skills/test-suite-run/SKILL.md` (something real to execute) and anyone
reading a QA receipt and trusting it means what it says.

## Proposed change

`restaurant-portal` gets a working test command and at least one test that
exercises something real — the app builds, and a real route renders — so a
change that breaks either produces a red suite instead of a silent gap. No
behavioural change to the app itself.

## Acceptance criteria

1. `[stated]` Given `restaurant-portal`, when its test command is run, then
   it executes real test code (not a no-op) and exits non-zero if a test
   fails.
2. `[stated]` Given a change that breaks `restaurant-portal`'s build or stops
   its entry route from rendering, when the test suite runs, then it fails.
3. `[stated]` Given `agents/eng-manager/config/projects.md`'s Commands table,
   when this ticket ships, then `restaurant-portal`'s Test cell names the
   real command (not an empty cell).
4. `[inferred]` Given `skills/test-suite-run/SKILL.md` running against
   `restaurant-portal` after this ships, then it executes the new suite and
   produces a non-vacuous pass/fail result, not the "no suite" branch.

## Non-goals

- Does not add a test command or any test to `aiorders-admin-hub`,
  `config-site-builder`, `restaurant-marketplace`, or `aiorders-api`. Each
  would need its own ticket; none is promised one by this ticket.
- Does not pursue comprehensive coverage. Smoke-level — build succeeds, a
  real route renders — is the bar, not a coverage percentage.
- Does not change `restaurant-portal`'s application behaviour.
- Does not modify `skills/test-suite-run/SKILL.md` itself — it already
  branches on suite-exists vs. not; only the repo and the registry entry
  change.
- Does not stand up a hosted CI pipeline (e.g. GitHub Actions). The
  immediate consumer is the department's own skill-driven quality gate,
  which runs inside the department's worktree, not an externally hosted
  runner.

## Risks and unknowns

- Framework choice (Vitest is the likely fit for a Vite app, but that's the
  architect's call, not fixed here).
- Whether `restaurant-portal`'s tree is still clean at build time — reconfirmed
  clean as of this PRD (2026-08-25), but trees drift; worth one more check
  when building starts.
- Whether the approver actually wants `restaurant-portal` specifically, given
  the request explicitly reopened repo choice rather than naming it outright.

## Cost

- Build: M — new dev dependency (a test framework), new test file(s), a
  registry update. No new runtime dependency.
- Run: $0/month. A test runner is a dev-time tool; nothing deployed, nothing
  billed.

## Decision

- **The approver's answer:** approved
- **Date:** 2026-08-25T21:43:57Z
- **Notes:** No `## Dissent` section — `agents/critic/agent.md`, which
  `skills/prd-writer/SKILL.md` step 8b calls for before every G1, doesn't
  exist at the department or instance level. Filed as a proposal
  (`agents/eng-manager/proposals.md`, 2026-08-25) rather than worked around
  here.
