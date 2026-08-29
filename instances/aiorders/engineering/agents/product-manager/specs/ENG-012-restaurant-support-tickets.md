---
ticket: ENG-012
project: aiorders-admin-hub
status: awaiting-scope
size: L
author: product-manager
created: 2026-08-29
decided:
---

# Restaurant support tickets — minimal tracking, plus an open-count on the Brands page

## Readback

**You said:** "...also the health of restaurant and maybe tickets" (the
original request, `ENG-011`'s own `## Input`), then, on the standing
question that request's "maybe tickets" raised
(`inbox/_handled/2026-08-29-eng011-tickets-source-question.md`): `decision:
rejected` with free-text **"Reading A."**

**Understood as:** No support-ticket system exists anywhere in AIOrders'
own systems today (confirmed by checking, not assuming — see `ENG-011`'s
own PRD). Reading A, which you selected, means building a minimal one from
scratch: an issue, a status, who's handling it — then showing an open
count per restaurant on the admin Brands page (`ENG-011`'s own surface).
Not building against or linking to any external tool, since Reading B
(tickets already live somewhere outside AIOrders) was the option not
picked.

**This ticket does not re-run a full independent readback.** The standing
question it answers already laid out two fully-specified options
side by side — this is a selection between two pre-drafted readings, not
a fresh ambiguous raw request, the same shape `ENG-009` was when it
answered `ENG-008`'s "engagement" question. A fresh blind architect
reading would be re-litigating a fork that's already resolved.

**One reading note, flagged rather than silently resolved.** The gate
item's `decision:` field read `rejected`, which taken alone would mean
"drop this" — but the free-text answer directly beneath it names a
specific option this same item had already defined, which isn't something
written down for a "no." Read together as "build Reading A," not a
rejection of the idea (full reasoning on the gate item's own processed
footer). If this reading is wrong, this ticket's own G1 is where to say so.

**Requirements for this ticket:**
1. `[confirmed]` A restaurant/brand can have one or more support tickets
   recorded against it: at minimum an issue description, a status (e.g.
   open/in progress/closed), and who on staff is handling it.
2. `[confirmed]` Staff can create, update, and close a ticket.
3. `[confirmed]` The Brands admin page (`ENG-011`) shows an open-ticket
   count per restaurant.
4. `[inferred]` Only admin staff can create, view, or update tickets — no
   restaurant-facing or public submission path was asked for.

**Assumed, and worth correcting if wrong:**
- **No customer/restaurant-facing submission form** — tickets are
  staff-entered only. "Reading A" describes staff tracking an issue, not a
  restaurant filing one.
- **No SLA, escalation, or notification logic** — a bare issue/status/owner
  record is what was asked for; anything more is a later ticket if wanted.
- **No integration with an external helpdesk tool** — that was Reading B,
  not the one selected.

## Problem

Staff have no system of record for restaurant-reported issues — no way to
see what's open, who owns it, or how many issues a given restaurant has
outstanding, which is exactly the kind of thing `ENG-011`'s own
prioritization page needs to point at.

## Why now

Direct follow-on to `ENG-011`'s standing question, answered this same
session. Depends on nothing else queued; `ENG-011` itself has no
dependency on this ticket (its Brands-page work ships without it — this
ticket's count is an addition once it exists).

## Users

AIOrders admin staff — the same audience as `ENG-011`.

## Proposed change

Staff can open a restaurant's record and log a support ticket (issue,
status, owner), update it as work happens, and close it. The Brands page
shows how many are currently open per restaurant.

## Acceptance criteria

1. `[confirmed]` Given a restaurant with no tickets, when staff create one
   with an issue description, then it appears with a default open status
   and persists.
2. `[confirmed]` Given an open ticket, when staff assign or reassign who's
   handling it, then the assignment persists and is visible.
3. `[confirmed]` Given an open ticket, when staff change its status
   (e.g. in progress, closed), then the change persists and is reflected
   wherever tickets are listed.
4. `[confirmed]` Given a restaurant with N open tickets, when staff view
   the Brands page, then that restaurant's row shows an open-ticket count
   of N.
5. `[inferred]` Given a closed ticket, it no longer counts toward the
   Brands-page open count.
6. `[inferred]` Given a non-staff request to any ticket read/write path,
   then it's rejected by the existing admin-portal authorization gate.

## Non-goals

- Restaurant-facing or public ticket submission — staff-entered only.
- SLAs, escalation rules, or automated notifications.
- Any external helpdesk/support-tool integration (Reading B, not selected).
- A full audit history/comment thread per ticket — this ticket is
  issue/status/owner only; anything richer is a later ticket if asked for.

## Risks and unknowns

- **Genuinely a new subsystem** — new data model, new CRUD surface, new
  admin UI (list + detail, at minimum) — materially bigger than `ENG-011`'s
  derived-field approach. Sized `L`, not `M`; the architect may find a
  one-way door here (a new table's shape is harder to walk back once staff
  have real tickets logged against it) that `ENG-011`'s design didn't have
  to consider.
- **The "rejected + Reading A" reading is an interpretation**, not a
  certainty — flagged plainly in the Readback above and in
  `decision-journal.md`. If wrong, correcting it here costs nothing; if
  built first and found wrong later, it costs the whole ticket.
- No stated deadline.

## Cost

- Build: `L` — a new table, new endpoints (`aiorders-api`), and new admin
  UI (list + detail, `aiorders-admin-hub`) for the ticket record itself,
  plus a small addition to `ENG-011`'s own Brands-page work for the count.
  Rough band: several days to a week, pending the architect's own design.
- Run: `$0/month` — no new vendor, no new external service (Reading B, the
  paid/integration-flavored option, was not selected).

## Decision

Filled in by the approver.
