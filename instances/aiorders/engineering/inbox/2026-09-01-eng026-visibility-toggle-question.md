---
type: eng-decision
agent: product-manager
gate: intake-question
project: restaurant-marketplace
ticket: ENG-026
recommendation: Answer to unblock shaping. Does not block anything currently in flight — answer when convenient.
raised: 2026-09-01
notified: 2026-09-01T10:03:26
nudged: 2026-09-02T15:37:50
decision:
---

# One thing before ENG-026 gets shaped further — is a channel-visibility toggle part of this?

**Context.** A new request arrived (via control-center) titled "on the brand
portal i want option to make the restaurant visible on order food, dine in
and catering separately," with a body specifying three enhancements:
operational time-clocks/cutoffs, consumer-facing filters for dine-in/
catering, and a promo-badge overlay — plus internal admin-form fields for
the first two.

**Why this is a question rather than an automatic shape.** Both the PM's own
reading and an independent, blind architect reading (raw request only, no
repo access, not shown the PM's reading) converged on the same gap without
being asked to look for it: none of the three body tasks actually adds a
per-channel on/off visibility toggle — the thing the title itself literally
asks for. Two careful readers landing on the same "the title and the body
don't match" finding is exactly the ambiguity this department's readback
process exists to catch before anything gets built from it.

**You said** (this ticket's own title): "i want option to make the
restaurant visible on order food, dine in and catering separately"

**But the body's three tasks** (operational time-clocks, smart filters,
promo badges) never add a per-channel on/off visibility toggle anywhere.

**Reading A:** the three body tasks are the whole ask — the title described
the goal loosely (a restaurant "being visible" for ordering, dine-in, and
catering distinctly, in the sense of having distinct hours/filters/promos
for each), not a literal missing toggle field.

**Reading B:** a real, independent per-channel visibility toggle is also
wanted, as a fourth piece alongside the three body tasks — e.g. a restaurant
could turn off "dine-in" on FoodSwipe entirely while keeping "order food" on.

**Which?**

## Decision

Filled in by the approver.
