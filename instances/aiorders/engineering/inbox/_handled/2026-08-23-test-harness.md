---
source: approver
filed_by: Harry
via: manual
received: 2026-08-23
---

# Give the AIOrders repos a test harness before anything else ships

No registered AIOrders project has a single test. Verified 2026-08-23: none of
the four `package.json` files defines a `test` script, `aiorders-api` has no
`package.json` at all, and a filesystem sweep finds zero `*.test.*` or
`*.spec.*` files outside `node_modules` anywhere in the five repos.

That makes the quality gate unenforceable rather than merely weak. The `full`
lane requires a QA test-plan receipt and `skills/test-suite-run/SKILL.md` needs
something to execute; with no suite, the receipt exists and proves nothing —
the exact failure `skills/code-review-gate/SKILL.md` names in its own receipt
table, where a receipt written on a fail satisfies the check it was meant to
prove.

Verido-CRM was in this position and it was solved the same way, for the same
stated reason: ENG-002 built a smoke test harness because the app had no CI to
prove a change had not broken a route.

## What this asks for

Shape and scope this. The department decides the shape — this is a problem
statement, not a design.

Two things worth weighing during shaping, offered as constraints rather than
answers:

**Start with one repo, not five.** `restaurant-portal` has a clean working tree
and already builds. The merge friction originally noted here is largely gone —
the human checkouts were committed on 2026-08-23, leaving `aiorders-admin-hub`
with only six held-back migration deletions (see the migration-history request
filed the same day) and `restaurant-marketplace` clean. Repo choice can now be
made on technical grounds rather than on which tree was tidiest.

**`aiorders-api` is the highest blast radius and the hardest case.** It is the
shared backend for all four frontends, it is Deno rather than Node, and it has
no `package.json` to hang a script on. It probably deserves its own ticket
rather than being folded into a frontend harness.

## Why it is worth building

Every ticket after this one is cheaper and safer, and until it exists the
department cannot honestly claim any AIOrders work passed a quality gate.
