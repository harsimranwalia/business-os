---
type: eng-decision
agent: eng-manager
gate: G3
project: aiorders
ticket: ENG-001
recommendation: confirm — all four acceptance criteria are satisfied and independently re-verified; there is nothing to deploy, so this is a record check, not a production go/no-go
raised: 2026-08-26
notified: 2026-08-26T15:43:11
decision: approved
decided: 2026-08-27T05:05:01.598404+00:00
---

# G3 — Register this business's repos and prove the loop runs end to end

## Not the usual G3

This ticket has no deploy target — it's the seed ticket that registers
`aiorders`'s five repos and proves the build loop itself works, not a code
change to any of them. `ADR-001` and `ADR-002`
(`agents/architect/decisions/`) decided it still owes every state and gate a
normal ticket does, including this one, but that the *question* changes: not
"ship this to production" (nothing is being shipped), but **"is this ticket's
record accurate, and is it actually done?"**

## What this asks you to confirm

1. All five AIOrders repos are registered in `agents/eng-manager/config/projects.md`
   at L1, and you already approved that registration on 2026-07-28.
2. A department-owned git worktree exists under `_eng/` for each — re-verified
   present this pass.
3. `lib/eng-gate-check.sh` exits 0 against this instance — re-run fresh this
   pass, clean.
4. A second real ticket has reached the board and moved past `intake →
   shaped` — `ENG-002` (the `restaurant-portal` smoke-test harness), which
   has since gone all the way to `verified` and shipped for real.

All four were independently re-checked against disk this pass, not cited from
an earlier hop's numbers. Review and security both already passed
(`agents/principal-engineer/reviews/ENG-001.md`,
`agents/security/reviews/ENG-001.md`, both `pass`).

## Recommendation

**Confirm.** There's no risk to weigh — no code shipped, no user-facing
surface touched, no cost. This gate exists because `docs/engineering-team.md`
reserves "say yes to production" to you specifically, department-wide, and
`ADR-002` deliberately didn't invent an exception for a ticket shaped like
this one, even though nothing is actually being deployed. See the ADR's
Review trigger if this framing feels like it asked you something it didn't
need to — that's useful signal for the next instance's own seed ticket, not
just this one.

## PRD / design / ADRs

- `agents/product-manager/specs/ENG-001-register-repos-and-prove-the-loop.md`
- `agents/architect/designs/ENG-001-register-repos-and-prove-the-loop.md`
- `agents/architect/decisions/ADR-001-verification-ticket-building-and-receipts.md`
- `agents/architect/decisions/ADR-002-verification-ticket-release-and-g3.md`

## Decision

Filled in by the approver.

## Decision

**approved** — 2026-08-27T05:05:01.598404+00:00
