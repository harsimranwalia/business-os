---
type: eng-decision
agent: product-manager
gate: intake-question
project: aiorders-api
ticket: ENG-007
recommendation: File ticket 3 (points ledger / earn API) now, continuing the approved five-ticket loyalty sequence. Does not block anything currently in flight — answer when convenient.
raised: 2026-08-30
notified: 2026-08-30T07:43:29
decision: approved
decided: 2026-09-01T17:02:39.576746+00:00
---

# Continue the loyalty sequence — file ticket 3 (points ledger) next?

**Context.** `ENG-007` (per-restaurant loyalty configuration) just passed
acceptance-check — all 6 criteria verified against the live production
system, no scope creep, cost matched. It's item 2 of the five-ticket loyalty
sequence `ENG-006`'s PRD proposed and its G1 got the shape approved for.

**Why this is a question rather than an automatic next step.**
`skills/acceptance-check/SKILL.md` step 6b auto-files the next item in a
sequence only when this ticket's *own* G1 explicitly re-affirmed continuing
the whole sequence — the bar `ENG-006`'s G1 set ("the proposed five-ticket
sequence stands as shape to file incrementally"). `ENG-007`'s own G1
(`inbox/_handled/2026-08-28-eng007-g1-scope.md`) was answered with a bare,
unconditional "approved" — it never independently touched the continuation
question, so per 6b's own worked example for exactly this case, this is
asked rather than assumed.

**What's already settled, so this isn't re-litigating anything.** The one
open risk `ENG-007`'s own design work surfaced — a live third-party loyalty
vendor (Walletly) already integrated — was resolved at `ENG-007`'s G2:
"Walletly is being retired/replaced." That was the one thing that could have
changed ticket 3's shape or blocked it outright; it didn't. Ticket 3's own
shape is already named in `ENG-006`'s PRD ("Feature shape and sequencing")
and in `ENG-007`'s own non-goals ("the points ledger, balances, and
earn/redeem transaction history").

**Yes** — file ticket 3 now, same process as `ENG-007` (fresh PRD, readback,
its own G1). **No** — hold the sequence here; nothing currently in flight
depends on ticket 3 existing yet. Either answer, `ENG-007` itself is already
`verified` regardless.

## Decision

Filled in by the approver.

## Decision

**approved** — 2026-09-01T17:02:39.576746+00:00

yes
