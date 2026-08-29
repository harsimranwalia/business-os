---
status: knowledge-capture
author: product-manager
created: 2026-08-28
related_ticket: ENG-006
---

# Loyalty program — frontend understanding across the three portals

**This is not a ticket, not a spec to build against, and not sequenced.** The
approver was explicit, twice: frontend work across every repo is "a separate
discussion, later." This document exists solely because the approver asked,
in the same breath as approving ENG-006's G1, that the understanding already
worked out during that ticket's readback not be lost in the gap between now
and that later discussion:

> "Do create a PRD for the understanding you got for the frontend work in
> different portals so that the knowledge is not lost. We will discuss and
> execute later doesnt mean lose the knowledge and findings and learnings
> while building the backend."

Everything below is inference from the original request and the ENG-006
readback, carried forward so it doesn't have to be re-derived from scratch
when the frontend discussion actually happens. None of it has been scoped,
sized, or run through a G1 of its own — treat every acceptance-criterion-style
statement below as a **starting hypothesis for that future discussion**, not
as agreed scope.

## Where frontend lives, per the original request

The approver named three repos, each with a different audience:

| Repo | Audience | Registered? | Autonomy |
|---|---|---|---|
| `restaurant-marketplace` | The diner/customer | Yes (`config/projects.md`) | L1 |
| `restaurant-portal` | The restaurant operator/staff | Yes | L1 |
| `admin-hub` | AIOrders' own internal staff | Yes (as `aiorders-admin-hub`) | L1 |

All three are registered and already have working trees and CI-adjacent
tooling (`config/projects.md`), so none of this needs new repo onboarding
when the day comes — just tickets.

## Per-portal understanding

### `restaurant-marketplace` (the diner)

This is where the identity ENG-006 builds actually gets exercised by a human
for the first time. Implications surfaced during the readback:

- A phone-entry + OTP-code UI, replacing or sitting alongside whatever
  checkout/account flow exists today. Session persistence needs the same
  "don't re-OTP on every visit" behavior ENG-006's backend guarantees — the
  frontend's job is to hold onto the Supabase session the SDK already gives
  it (the same pattern already used elsewhere in this codebase, e.g. the
  admin hub's `supabase.auth.getSession()` calls), not to invent its own.
- A single QR code, shown once the diner has an identity, that every
  restaurant's staff scans. This is a ticket (4) concern (QR issuance) but
  the *display surface* for it is here.
- A "one UI, restaurant-scoped balances" points view — the diner sees every
  restaurant they've earned or redeemed at, each restaurant's own balance
  under one shared visual identity, never a combined total (points don't
  move between restaurants, per the approver's explicit instruction).
- Whatever checkout flow exists today presumably already collects a phone
  number in some form (the legacy `customers` table's `phone` column is
  populated from somewhere) — worth checking at build time whether that
  existing capture point can *become* the OTP entry point, rather than
  adding a second, separate "who are you" step next to it.

### `restaurant-portal` (the restaurant operator)

- A config screen for the two per-restaurant loyalty rates ticket (2)
  defines: earn % (online, separately dine-in) and redemption value,
  effective-dated.
- A redemption/scan surface for staff — this is where "one restaurant staff
  member enters a dine-in amount by hand" (the assumed mechanism, since
  there's no POS integration) actually happens, and where a QR gets scanned
  to redeem. Restaurant-scoped: staff here can only ever touch their own
  restaurant's balance for a given customer, never see or affect another
  restaurant's — enforced at the API layer (ticket 4), surfaced here as
  simply not offering the option.
- Whatever this portal already has for viewing a customer's order history
  is the natural neighbor for a "this customer's loyalty activity at my
  restaurant" view — no cross-restaurant visibility here, by design (a
  restaurant operator doesn't get to see a competitor's customer
  relationship, which is exactly the positioning tension ENG-006's PRD
  named in its own Risks).

### `admin-hub` (AIOrders' internal staff)

- Support tooling: look up a platform customer (by phone, most likely) and
  see every restaurant they're linked to — this is the one legitimate
  cross-restaurant read the whole feature has, and it's internal-only.
- Manual ledger adjustment/void (ticket 5's admin surfaces) — support fixing
  a wrong redemption or a double-scan.
- Likely also where an ambiguous-match review queue would surface — ENG-006's
  backend design flags phone matches it isn't confident about
  (`needs_review`) rather than silently guessing; something needs to show a
  human that list. Admin-hub is the natural home, not a new surface.

## What's still genuinely open, for the later discussion

- Whether the diner's *existing* checkout phone-capture can double as OTP
  entry, or whether this is a net-new step in the flow (materially different
  UX cost).
- Any UI for the phone-recycling risk ENG-006's design flags (a diner
  logging in and seeing a stranger's order history because they inherited a
  recycled number) — not designed here at all; the backend's mitigation
  posture is a review queue, not a frontend-visible flow.
- Branding/naming for the customer-facing identity and the points currency —
  explicitly out of this department's lane per the PRD's own non-goals,
  regardless of which portal.
- Actual visual/component design — nothing here is a mockup or a component
  spec, only a list of surfaces and the backend behavior they'd need to
  reflect.

## Source

Everything above is drawn from `agents/product-manager/specs/ENG-006-unified-customer-identity.md`'s
own Readback, Users, and Feature-shape sections, plus the original verbatim
request preserved in the ticket's `## Input`
(`agents/eng-manager/board/ENG-006-unified-customer-identity.md`). No new
investigation was run against any of the three frontend repos themselves —
this is knowledge already surfaced while shaping the backend ticket, written
down rather than re-derived, not a fresh audit of `restaurant-marketplace`,
`restaurant-portal`, or `admin-hub`'s actual code.
