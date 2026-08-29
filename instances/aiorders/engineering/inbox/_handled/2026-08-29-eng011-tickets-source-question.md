---
type: eng-decision
agent: product-manager
gate: intake-question
project: aiorders-admin-hub
ticket: ENG-011
recommendation: Answer when convenient — does not block ENG-011's G1 or build. Once answered, this becomes its own small ticket (or folds into a later one) depending on scope.
raised: 2026-08-29
notified: 2026-08-29T11:04:44
decision: rejected
decided: 2026-08-29T11:16:32.000840+00:00
---

# One open thing before "tickets" can be scoped — does not block ENG-011

**You said:** "...also the health of restaurant and maybe tickets" (from
the same request as `ENG-011`,
`agents/eng-manager/board/ENG-011-client-stage-health-visibility.md`)

Two independent readings of this request (this PM's and, separately and
blind to it, the architect's) both landed on the same gap: neither could
tell what "tickets" means here. Checked both repos directly before asking
— no support-ticket or ticket-count concept of any kind exists anywhere in
`aiorders-api` or `aiorders-admin-hub` today, so this isn't a small
extension of something already there; it's a genuinely open question with
a wide cost range.

**Reading A:** A support-ticket system that doesn't exist yet, and this
request means building one (even a minimal one — issue, status, who's
handling it) from scratch, then showing an open-count per restaurant on
the Brands page.

**Reading B:** Support tickets already exist somewhere outside AIOrders'
own systems (email, a helpdesk tool, a shared inbox, something the team
already uses day to day) and this is asking to surface a count or link
from that source on the Brands page — much smaller, but needs to know
what that source is and whether it has an API.

**Which one — or is there a third thing you mean by "tickets"?** If
support requests already live somewhere today (even informally), naming
where settles this immediately.

This does not hold up `ENG-011`, which covers stage visibility, filtering,
and a minimal health signal and has no dependency on this answer. Once
answered, "tickets" gets shaped into its own ticket — sized properly once
we know whether it's new infrastructure or a display layer on something
that already exists.

## Decision

Filled in by the approver.

## Decision

**rejected** — 2026-08-29T11:16:32.000840+00:00

Reading A

---

**Processed 2026-08-29**, same `intake` event pass that raised this item —
answered by hand-edit while this pass was still running. **Read the
`decision: rejected` frontmatter and the free-text "Reading A" together,
not the field alone**, since taken literally they point opposite ways: a
flat rejection would mean drop the idea, but "Reading A" names a specific,
concrete option this same item defined two paragraphs above, which isn't
something you write down for a question whose answer is "no." This item's
own template only ever offered a bare "Filled in by the approver," not an
approve/reject choice — most likely `rejected` is whatever this instance's
reply channel defaults to when a free-text answer doesn't map onto a
gate's normal approve/reject shape (this item is a standing question, not
a gate), rather than a considered rejection of the idea itself. Taken as:
**build Reading A** — a minimal support-ticket system (issue, status, who's
handling it) from scratch, with an open-count shown per restaurant on the
Brands page — not Reading B (an external source). Flagged in
`decision-journal.md` as an interpretation, not a certainty, and worth
watching for a second occurrence before treating this as how this
approver's replies generally work through the control center.

Shaped directly into `ENG-012` in the same pass (`agents/eng-manager/board/ENG-012-restaurant-support-tickets.md`) —
this item itself already named the next step ("gets shaped into its own
ticket") once answered, so filing it is finishing this same request, not
new agent-invented scope, per the same reasoning `ENG-006`/`ENG-007`/`ENG-008`
established for a sequence's own next item. Its own fresh G1:
`inbox/2026-08-29-eng012-g1-scope.md`.
