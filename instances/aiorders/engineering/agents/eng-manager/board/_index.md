# Board

**Machine WIP 6** (`config/config.yaml` → `wip.machine_limit`) — counts states
`ready` through `ready-to-ship`. **Currently 0/6.**
**Approver-facing WIP 2 — currently 0/2. Approval cap 3 — currently 0/3.**

`priority:` is a field on every ticket, and **only the approver sets it.** It is
not `severity`, which is the agent's read of how bad a problem is.

## In flight

| ID | Title | Project | State | Priority | Owner | Size | Updated |
|---|---|---|---|---|---|---|---|
| ENG-001 | Register this business's repos and prove the loop | aiorders | intake | now | product-manager | S | 2026-08-24 |

## Waiting on the approver

Cap: 3 across all gates. At the cap, the EM stops advancing tickets into gate
states — more approvals waiting is a backlog with the approver's name on it,
not throughput.

_(none)_

## 2026-08-24 — decision: gate-check-unavailable resolved

Acted on the answered incident gate `2026-08-24-eng-gate-check-unavailable.md`
(`gate: incident`, tied to ENG-001 because it was the ticket in flight when the
pre-pass check found `lib/eng-gate-check.sh` unreadable). Its `project: life-os`
was stale — a leftover of the pre-carve-out hardcoding bug fixed in business-os
`ed8dd56`/`58ae148`/`9366b84`; `ticket: ENG-001` was correct. Approver had
already recorded `decision: approved`. Independently re-ran
`lib/eng-gate-check.sh` against this instance this pass: exit 0, clean — ENG-001
AC3 satisfied. Logged on ENG-001, moved the gate item to `inbox/_handled/`.
Did not shape ENG-001 further — a decision pass is scoped to the gate it
answers, not PM intake work — so `chained: ENG-001` to hand the ticket to a
fresh `continue` pass.
