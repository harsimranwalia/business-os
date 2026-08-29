---
type: eng-decision
agent: product-manager
gate: intake-question
project: aiorders-admin-hub
ticket: ENG-011
recommendation: Answer when convenient — does not block ENG-011's G1 or build. Once answered, this becomes its own small ticket (or folds into a later one) depending on scope.
raised: 2026-08-29
notified: 2026-08-29T11:04:44
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
