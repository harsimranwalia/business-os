---
type: eng-decision
agent: eng-manager
gate: one-way-door
project: aiorders-api
ticket: ENG-006
recommendation: proceed — the schema itself is additive and reversible; what isn't reversible is diner adoption, and that's a product call, not a technical one
raised: 2026-08-28
notified: 2026-08-28T20:04:15
decision: approved
decided: 2026-08-28T20:09:06.151165+00:00
---

# G2 — Is a phone/OTP platform-level customer identity, once diners adopt it, an acceptable one-way door?

## The question

ENG-006's design (`agents/architect/designs/ENG-006-unified-customer-identity.md`)
introduces a new identity layer: a diner verifies a phone number once via SMS
OTP and is recognized as the same person at every AIOrders restaurant from
then on, with their existing per-restaurant order history linked to it. The
PRD flagged this twice as a possible one-way door and asked the architect to
evaluate it for G2 rather than decide it quietly — this is that evaluation,
put to you rather than settled unilaterally, given it's the largest new
subsystem this department has designed so far and there's no G2 precedent yet
to lean on.

**Not being re-asked here:** the separate "marketplace owns the identity vs.
restaurant owns their customer" positioning tension. That was already in the
PRD's own Risks at G1, explicitly classified there as "a positioning fact
worth having on the record... not a build question" — and your G1 approval
passed that without comment. This gate is narrower: adoption reversibility
only.

## What is and isn't reversible

**The schema is fully additive and reversible.** Two new tables
(`platform_customers`, `platform_customer_legacy_links`) sit alongside the
existing `customers` table, which this ticket never modifies or deletes from.
Dropping both new tables tomorrow would break nothing else — no existing
order flow, no existing restaurant-scoped customer record, touches any of
today's data. There's no live caller yet either; nothing in any of the three
frontend repos calls this until a later, separately-scoped ticket wires it
in.

**What isn't reversible is adoption itself.** Once real diners have verified
a phone number, logged in more than once, and had their history linked
across restaurants, walking the mechanism back is a user-facing regression
(sessions invalidated, "why do I have to re-register everywhere again"), not
a clean migration. That's the sense in which the PRD called this expensive
to change later, and it's real regardless of how clean the schema is.

## Recommendation

**Proceed.** The technical design is conservative — Supabase's own native
phone/OTP auth rather than anything custom, additive schema only, no new
infrastructure. If this needs to be unwound later, the cost is a product
migration for diners, not an engineering rewrite. Given the ticket is
invisible to any diner or restaurant until a later ticket wires a frontend to
it, there's also a natural checkpoint before real adoption exists at all —
this design doesn't force irreversibility on day one.

If you'd rather not commit to the identity model at the platform level yet,
the alternative is holding ENG-006 at `designed` until the frontend
discussion happens and the model can be validated against an actual UI
before any diner touches it — slower, but removes the "diners are already on
it" risk entirely by construction.

## Decision

Filled in by the approver.

## Decision

**approved** — 2026-08-28T20:09:06.151165+00:00

So the existing system will still continue to function where users at restaurant level would continue to get created and they should be mapped at login time or session time to new restaurants which you would do now with the one time migration. So if both the flows continue to work then everything is reversible. The user knows they have foodswipe identity and they also know that restaurants can continue to use their existing system where restaurant specific customers are getting created. Its the job of the new system to still surface their orders from all restaurants and show them one identity

---

**Processed 2026-08-28 (`scheduled` event pass).** Found during the
whole-board safety-net sweep — the answer had not yet been picked up by any
local event; `traces/.pending` held a `decision` event for this same file
queued behind this pass at the time it was found, which is the department's
already-documented duplicate-event race (`observations.md`), not a new
failure — this pass simply reached the file first.

Read as a full approval, restated in the approver's own terms rather than a
bare "approved": reversibility rests on the **legacy per-restaurant
customer-creation flow and the new platform identity continuing to operate
side by side**, not on the schema alone — which is exactly the design's own
argument (`agents/architect/designs/ENG-006-unified-customer-identity.md`,
One-way doors). Confirms two things already true of the design rather than
changing either: (1) legacy per-restaurant customer creation is untouched by
this ticket, and (2) surfacing a diner's orders across every restaurant under
one identity is explicitly later-ticket scope (the loyalty ledger/UI slices),
not this one's. No scope change. Ticket advanced `awaiting-decision → ready`.
Journaled in `agents/eng-manager/config/decision-journal.md`. Full detail on
the ticket's own log
(`agents/eng-manager/board/ENG-006-unified-customer-identity.md`).
