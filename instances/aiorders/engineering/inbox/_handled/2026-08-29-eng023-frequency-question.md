---
type: eng-decision
agent: product-manager
gate: intake-question
project: restaurant-portal
ticket: ENG-023
recommendation: Answer when convenient — does not block ENG-023's G1 or build. Once answered, "yes" becomes its own new ticket; "no" closes this with nothing further to do.
raised: 2026-08-29
decision: approved
decided: 2026-08-29T17:41:07.724420+00:00
---

# One open thing on the feedback board request — does not block ENG-023

**You said:** "...is this frequent what are the bottomline issue that need to
be resolved by the restaurant location" (from the same request as
`ENG-023`, `agents/eng-manager/board/ENG-023-feedback-status-and-notes.md`)

Two independent readings of this request (this PM's, and, separately and
blind to it, the architect's) diverged on exactly this phrase. `ENG-023`
builds the confirmed, bounded fix regardless of this answer: a status and an
internal note on each feedback item, so a restaurant can track what it did
about each one. This question is about whether something bigger is also
wanted.

**Reading A:** No — once notes exist, a restaurant (or AIOrders staff
reviewing an account) can answer "is this frequent" themselves by reading
back through the notes over time. Nothing needs to be built or computed for
this specifically.

**Reading B:** Yes — you want the system itself to tell a restaurant what's
recurring: counts of similar feedback, or a called-out list of "these are
your bottom-line issues" — something that looks across items, not just
within one. That's a real aggregation/analysis feature (possibly grouping
similar free-text feedback, which likely means AI-assisted categorization,
not just a count), materially bigger than `ENG-023`'s per-item fields.

**Which one — or is it a third thing?** If Reading B, roughly how you'd want
"frequent" judged (e.g. same restaurant over time, or patterns across all
restaurants) would help scope it correctly.

This does not hold up `ENG-023`. Once answered, "yes" gets shaped into its
own ticket, sized once we know what "frequent" should actually mean; "no"
just closes this question.

## Decision

Filled in by the approver.

## Decision

**approved** — 2026-08-29T17:41:07.724420+00:00

reading b, frequent is same restaurant over time

---

**Processed 2026-08-29**, `watch` event pass (context `schtasks`) — found
this answered since the last pass touched it, while sweeping all three
watched inboxes. Per this item's own stated next step, shaped into
`ENG-025` (recurring feedback issues, per restaurant, over time) end to
end: PRD written, ticket filed at `awaiting-scope`, G1 raised
(`inbox/2026-08-29-eng025-g1-scope.md`). Live schema evidence gathered
while shaping it overturned this item's own speculation that Reading B
"likely means AI-assisted categorization" — `restaurant_feedback` already
carries a populated `sub_type`/`nature` taxonomy, so `ENG-025` is a `GROUP
BY` over existing data, sized `S`, not the heavier build this question
guessed at. `ENG-023` itself is unaffected — it ships the confirmed core
regardless of this answer, per this item's own text. Journaled in
`decision-journal.md`.
