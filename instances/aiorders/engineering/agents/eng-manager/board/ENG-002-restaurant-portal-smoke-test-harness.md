---
id: ENG-002
title: Add a smoke-test harness to restaurant-portal
project: restaurant-portal
type: chore
size: M
severity: P2
priority:
state: ready
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-25
updated: 2026-08-25
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-002-restaurant-portal-smoke-test-harness.md
  design: agents/architect/designs/ENG-002-restaurant-portal-smoke-test-harness.md
  adrs: []
  review:
  test_plan:
  security_review:
  release:
---

## Input

Verbatim, from `inbox/requests/2026-08-23-test-harness.md` (now
`inbox/_handled/`), filed by the approver, received 2026-08-23 — preserved
here per `skills/request-readback/SKILL.md` step 1, never edited:

> No registered AIOrders project has a single test. Verified 2026-08-23: none
> of the four `package.json` files defines a `test` script, `aiorders-api`
> has no `package.json` at all, and a filesystem sweep finds zero
> `*.test.*` or `*.spec.*` files outside `node_modules` anywhere in the five
> repos.
>
> That makes the quality gate unenforceable rather than merely weak. The
> `full` lane requires a QA test-plan receipt and
> `skills/test-suite-run/SKILL.md` needs something to execute; with no
> suite, the receipt exists and proves nothing — the exact failure
> `skills/code-review-gate/SKILL.md` names in its own receipt table, where a
> receipt written on a fail satisfies the check it was meant to prove.
>
> Verido-CRM was in this position and it was solved the same way, for the
> same stated reason: ENG-002 built a smoke test harness because the app had
> no CI to prove a change had not broken a route.
>
> **What this asks for:** Shape and scope this. The department decides the
> shape — this is a problem statement, not a design. Start with one repo,
> not five — `restaurant-portal` has a clean working tree and already
> builds. `aiorders-api` is the highest blast radius and the hardest case —
> it probably deserves its own ticket rather than being folded into a
> frontend harness.

Full text, including the "why it's worth building" close, in the handled
request file.

## Readback

See `agents/product-manager/specs/ENG-002-restaurant-portal-smoke-test-harness.md`
→ Readback — the full two-reading comparison lives there rather than
duplicated here.

## Problem

None of the five registered AIOrders repos has a single test. That makes the
`full` lane's quality gate structurally unable to prove anything: a receipt
file is enough to satisfy `lib/eng-gate-check.sh`, and
`skills/test-suite-run/SKILL.md` writes an honest "no suite" result that
still produces a non-empty receipt. Filed by the approver
(`inbox/requests/2026-08-23-test-harness.md`) after verifying no
`package.json` defines a `test` script and no `*.test.*`/`*.spec.*` file
exists anywhere in the five repos.

## Outcome

`restaurant-portal` has a real test command and at least one test that fails
on a broken build or a route that stops rendering. The registry's Commands
table names the real command. `test-suite-run` executes it and produces a
real result instead of the "no suite" branch.

## Notes

Scoped to one repo deliberately — see the PRD's Non-goals. `aiorders-api`
(Deno, no `package.json`, highest blast radius) and the other three
frontends are out of scope; `aiorders-api` will likely need its own ticket
but that isn't committed here.

This ticket is also what satisfies AC4 of `ENG-001` (the seed ticket needs
one real ticket to reach `shaped`) — see that ticket's log.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-25` `intake → shaped → awaiting-scope` (product-manager) — shaped
  from `inbox/requests/2026-08-23-test-harness.md` (filed by the approver,
  received 2026-08-23, unprocessed for two days — this pass's PM work, not a
  self-originated finding). Ran the full request-readback
  (`skills/request-readback/SKILL.md`): this PM's reading plus a blind
  architect reading, no material divergence — see the PRD's Readback
  section. `size: M` chore, so **G1 is required** per
  `agents/eng-manager/config/definition-of-done.md` → Size table (only `S`
  bug/chore auto-skips; `prd-writer/SKILL.md`'s coarser "bug/chore skips G1"
  reading was not used here — flagged as a doc inconsistency, not resolved
  in this pass). PRD written at
  `agents/product-manager/specs/ENG-002-restaurant-portal-smoke-test-harness.md`.
  No `## Dissent` — `agents/critic/agent.md` doesn't exist on this instance
  or the department template; filed as a proposal instead of worked around.
  G1 item written to `inbox/2026-08-25-eng002-g1-scope.md` and notified.
- `2026-08-25` `awaiting-scope → designed → ready` (eng-manager, `scheduled
  manual-unblock` pass) — G1 **approved** by the approver, 2026-08-25T21:43:57Z,
  no additional comment. Gate item moved to `inbox/_handled/`; PRD `status:
  approved`; journaled in `agents/eng-manager/config/decision-journal.md`.
  **Designed:** architect design written at
  `agents/architect/designs/ENG-002-restaurant-portal-smoke-test-harness.md` —
  Vitest + React Testing Library (reuses the project's own `vite.config.ts`,
  no second transform config), one smoke test rendering the real app entry
  point with its actual provider tree, asserting a known landmark renders.
  Playwright and Jest considered and rejected — see design's Alternatives.
  No one-way door (a test-runner choice is reversible); no ADR, no G2. **Ready:**
  work is a single unit (one repo, one test file, one config change) — no
  further breakdown needed; `machine_wip` (6) had 0/6 in flight, well within
  cap. **Not proceeding into `building` this pass, deliberately** — this pass
  is a `scheduled manual-unblock` sweep recovering from an earlier timeout
  (see this ticket's board-index entry), not a fresh, dedicated context, and
  `schedules/eng_build_loop.md` names `building` as the pass's own stopping
  point precisely because writing the actual code deserves a clean session
  ("an engineer writing code is the pass's real unit of work"). `chained:
  ENG-002` — sitting at `ready`, owned by eng-manager (agent, not approver,
  not blocked, not terminal) — firing `continue` for a dedicated building hop.
