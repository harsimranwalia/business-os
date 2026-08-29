---
source: harry
via: eng-006-sequence-continuation
received: 2026-08-29T04:30:00.000000+00:00
tag: eng
---

# Continue the approved ENG-006 loyalty-identity sequence — file ticket 2

`ENG-006` (unified cross-restaurant customer identity) is `verified` and its
PRD (`agents/product-manager/specs/ENG-006-unified-customer-identity.md`,
"Feature shape and sequencing") proposed a five-ticket sequence for the
loyalty feature, of which `ENG-006` was item one. The G1 answer on that
ticket explicitly affirmed proceeding with the whole shape: *"the proposed
five-ticket sequence stands as shape to file incrementally, not as four
pre-approved tickets."* Harry's own later clarification of what that meant:
*"we finish one ticket then you file next and seek approval then next then
next till feature is complete"* — and that filing the next item is not the
department inventing work, since the shape was already reviewed once.

This request exists because `skills/acceptance-check/SKILL.md` step 6b (the
mechanism meant to do this automatically the moment a sequenced ticket
verifies) didn't exist yet when `ENG-006` actually passed acceptance-check,
so nothing fired. Filing this directly through the normal front door rather
than trying to retroactively re-trigger a pass that already completed.

**Item 2, as ENG-006's own PRD scoped it:** "Per-restaurant loyalty
configuration — earn % (online, dine-in) and a redemption value, per
restaurant, effective-dated so a later rate change doesn't rewrite the
meaning of past ledger entries. No dependency on `ENG-006`; could build in
parallel." Backend and migrations go in `aiorders-api`, same as `ENG-006`.
Frontend is out of scope for this whole sequence, same as `ENG-006` — a
separate, later discussion.

Shape this into its own ticket and PRD exactly as any fresh intake would —
this note only carries forward the shape already agreed at `ENG-006`'s G1,
not a pre-approval of this ticket's own scope, acceptance criteria, or size.
