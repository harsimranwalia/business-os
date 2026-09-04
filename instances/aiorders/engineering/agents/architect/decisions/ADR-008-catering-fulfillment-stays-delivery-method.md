---
id: ADR-008
title: Catering fulfillment stays on `delivery_method` — configurable copy, not new values
project: config-site-builder
ticket: ENG-016
status: accepted
decided_by: architect
date: 2026-09-03
supersedes:
superseded_by:
---

# ADR-008: Catering fulfillment stays on `delivery_method` — configurable copy, not new values

## Context

The approver's `changed` answer to `ENG-016`'s first G1 specified three
fulfillment options — On-site Catering, Pickup & Delivery, Drop-off Trays — for
the public catering form. The live form has five, and they are not a flat list:
`pickup` and `delivery` are always offered, while `live_catering`, `party_hall`
and `food_truck` each appear only when that per-restaurant boolean flag is set
(`CateringForm.tsx`, mirroring the flags `brand-portal/catering.ts`'s
`get_catering_settings` reads). The selected value is stored in
`catering.delivery_method`, rendered on the owner's detail modal, and present on
every historical row. The re-raised G1 named the resulting fork —
"we'll need to decide whether to remap existing restaurants' data or add your
three alongside the current five" — proposed no default, and came back
`approved` with no comment on it, leaving the decision here.

Reading the thirteen approved acceptance criteria against that fork changes the
question. **No acceptance criterion names the three values, or any values at
all.** AC-1 requires that "a fulfillment option control is shown"; AC-2 requires
that the instructional copy for the selected option "comes from that
restaurant's own configuration — no copy is hardcoded to one restaurant"; AC-12
requires the owner to see "the fulfillment option" on the request. The three
labels appear only in the superseded rewrite and in the PRD's Risks section,
where they are stated as a problem to be solved rather than a requirement to be
met.

## Decision

Keep `catering.delivery_method` exactly as it is — same column, same five
flag-gated values, same control, no migration, no remap, no second field — and
express the rewrite's fulfillment intent as **per-restaurant configurable copy
keyed by the existing option values**, in a new optional `fulfillmentCopy` key
on the `restaurant_website.catering` jsonb object. Each entry may carry a
`label` (overriding today's hardcoded "Pickup" / "Live Catering" / …), a
`description` (AC-2's instructional copy), and a `guestCountNote` (AC-1's helper
note). A restaurant that wants its `live_catering` option to read "On-site
Catering" sets the label; a restaurant that offers a food truck can author copy
for it too, which a fixed three-value enum could not express.

## Alternatives

| Option | Why not |
|---|---|
| **Remap the five live values to the approver's three** (the G1's first branch) | A destructive migration on live rows that changes what the owner's board displays for historical requests, and it cannot express what the current model does: the three values have no per-restaurant flag gating, so `live_catering` / `party_hall` / `food_truck` — which are exactly the restaurant-level capability switches AIOrders sells — would collapse into one undifferentiated "On-site Catering" for every tenant. `Drop-off Trays` also has no existing counterpart, so the remap is lossy in one direction and inventive in the other. Directly against AC-8's and AC-10's additive-only posture. |
| **Add a `fulfillment_option` column alongside the untouched `delivery_method`** (the G1's second branch, and the recommendation this design was handed) | Additive and safe, but permanent: two overlapping fulfillment fields on every row, forever. `restaurant-marketplace` and the GoHighLevel path would keep writing only `delivery_method`, so the new column would be null for a large share of rows; the detail modal would have to render both or silently pick one; and every future consumer inherits the question of which one is authoritative. All of that cost to satisfy no acceptance criterion. |
| **Add the three new values to the existing `delivery_method` option list** | One column, no migration — but an eight-value list mixing two vocabularies ("Pickup", "Live Catering", "Pickup & Delivery", "On-site Catering") that a customer would have to disambiguate, and that the owner would then see mixed across their board. Worse for the user than either the old set or the new one. |
| **Hardcode the three labels in `CateringForm.tsx` without changing storage** | Fails AC-2 outright — the copy would be hardcoded for every restaurant, which is the one thing that criterion forbids. |

## Consequences

**Accepted:** the three labels from the approver's rewrite do not appear
anywhere by default. A restaurant gets them only by authoring them, and no
restaurant has authored anything on day one, so the shipped default is today's
labels. If the approver actually wanted the three names as a platform-wide
vocabulary, this decision does not deliver that and should be revisited — which
is the honest read of a rider answered by silence rather than by a sentence.
`Drop-off Trays` in particular has no existing value to relabel; a restaurant
that wants it would need a sixth `delivery_method` value, which is a small
additive change but is not made here.

**Gained:** no migration, no data-compatibility question, no second fulfillment
field, no change to `restaurant-marketplace`'s or GoHighLevel's stored rows, and
no work at all for AC-12 — the owner's detail modal already renders
`delivery_method`. AC-2 is satisfied more completely than a fixed enum would
satisfy it, because copy is authored per restaurant over whichever options that
restaurant actually offers. The per-restaurant flag gating that
`live_catering` / `party_hall` / `food_truck` provide survives intact.

**Reversibility:** cheap. Adding a `fulfillment_option` column later is the same
additive nullable migration this ticket already performs twice; nothing here
forecloses it. Nothing is written that would have to be unwound first.

## Review trigger

Revisit if the approver names the three fulfillment labels again — in a G1
answer, a follow-up request, or Piece 2's scope — or if Piece 2's package model
turns out to need pricing keyed to a fulfillment *type* rather than to a
per-restaurant option, which is the one plausible reason the platform would need
a fixed vocabulary rather than per-restaurant copy.
