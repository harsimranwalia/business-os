---
id: ADR-009
title: The catering order form is an owner opt-in, default off, stored in `restaurant_website.catering`
project: config-site-builder
ticket: ENG-016
status: accepted
decided_by: architect
date: 2026-09-03
supersedes:
superseded_by:
---

# ADR-009: The catering order form is an owner opt-in, default off, stored in `restaurant_website.catering`

## Context

`ENG-016` Piece 1 adds a dish picker to every restaurant's **public** catering
page. AC-1 is scoped "given a restaurant with the catering order form enabled";
AC-9 requires that "a restaurant that has not enabled the catering order form —
**including** any restaurant with no structured menu data (`hasMenu` of `file`
or `embedded`)" sees exactly today's behaviour. The "including" makes the
no-structured-menu case a subset of the not-enabled case, so structured-menu
presence is necessary but not by itself sufficient: there is a second,
independent condition, and neither criterion says what its default is or where
it is stored.

Two facts found in the code decide it. First, `restaurant-portal` already ships
an owner-facing editor for this exact object — Website → Catering
(`pages/website/Index.tsx` → `CateringPageForm`, saving to
`restaurant_website.catering` through `brand-portal`'s `update_website_content`,
which allow-lists `catering` and `careers` as editable pages). A toggle there is
discoverable by the owner on the tab they already use. Second,
`get-brand-website` defaults `hasMenu` to `'embedded'` when unset, so the
population that *could* be enabled is already narrow and already the result of a
deliberate setup choice.

## Decision

The catering order form is **off by default** and requires an explicit
`orderFormEnabled: true` on that restaurant's `restaurant_website.catering`
object, set by the owner through a switch added to the existing Website →
Catering editor. The effective gate is
`config.catering?.orderFormEnabled === true` **and** the selected location's
`hasMenu === 'page'` with a non-empty menu. No new column, no new table, no new
endpoint, no admin surface.

Because that jsonb object is written back wholesale on save
(`updateWebsiteContent` does `.update({ catering: <whole object> })`, and
`CateringPageForm` re-initialises its state from an explicit field list), the
same change must make that form spread `...content` before its normalised
fields. Otherwise an owner editing their catering copy silently wipes the flag
and turns the feature back off — and the same latent bug already eats the legacy
`formFields` key today.

## Alternatives

| Option | Why not |
|---|---|
| **Default on for every restaurant with a structured page menu**, with an explicit opt-out | Turns on a new interactive flow on live public pages for a set of restaurants that never asked for it, and does so with **empty instructional copy** — `fulfillmentCopy` (ADR-008) is unauthored on day one, so the first thing every affected customer would see is a picker with no guidance. AC-1's "with the catering order form enabled" and AC-9's "has not enabled" both read as an affirmative act rather than a condition that happens to hold. It also contradicts the same approver's most recent adjacent decision (`ENG-026`, 2026-09-03: channel visibility is *set*, not defaulted). |
| **A new boolean column on `restaurants`, beside `live_catering` / `party_hall` / `food_truck`** | The most structurally correct option: those flags are already the established per-restaurant catering capability switches, already surfaced per-location by `get-brand-website`, and immune to the brand-override problem below. Rejected because nothing in `restaurant-portal` lets an owner set them — they are staff-set — so every enablement would land permanently on the approver's plate, one restaurant at a time. That is the exact cost `ENG-016`'s own filter answer (question 1: "work off the approver's plate, or onto it?") makes Piece 1 worth building. It also means a new column on a core table plus changes in two places in `get-brand-website`, for a switch the existing editor can carry for free. |
| **A per-location key rather than a brand-wide one** | `config.catering` resolves to a single object for the whole brand, so the toggle is necessarily brand-wide. This is acceptable because the *other* half of the gate — structured menu data — is evaluated per selected location, so the effective answer already varies by location: a brand can enable it and only its page-menu locations render a picker. A genuinely per-location toggle would need the `restaurants`-column option above. |
| **No toggle at all — structured-menu presence is the whole gate** | Simplest, and it was the working assumption handed to this design. Rejected because AC-9's "including" phrasing makes the menu condition a subset of enablement rather than identical to it, and because it removes the owner's ability to decline a change to their own public page. |

## Consequences

**Accepted:** the feature ships doing nothing for everyone, and stays that way
until an owner acts. There is no rollout metric on day one and no way to know it
works in production until the first restaurant enables it — the QA plan and any
demo need a deliberately enabled restaurant. It also inherits a pre-existing
precedence trap: `get-brand-website` resolves `catering: brand.metadata?.catering
|| restaurantData.catering`, so for a brand with brand-level catering content the
restaurant-level switch the portal writes is ignored entirely, and enablement for
those brands is a staff edit at brand level. That is deliberate, documented
behaviour affecting `heardAboutUsOptions` the same way today, but it is newly
consequential now that the object carries a functional switch and not only copy.

**Gained:** the whole ticket is inert on deploy — every one of AC-8, AC-9 and
AC-10 holds trivially for every existing restaurant, and rollback of the public
form is a revert with no data to unwind. Enablement is self-service, so it costs
the approver nothing per restaurant. And it forces the editor addition into
scope, which is what makes `fulfillmentCopy` (ADR-008) authorable at all rather
than a config surface only staff can fill in — the same "who maintains this"
question the PM held Piece 2 on.

**Reversibility:** cheap. Flipping the default to on is one comparison
(`!== false` instead of `=== true`); moving the flag to a `restaurants` column
later is an additive migration plus the `get-brand-website` plumbing, with the
jsonb key readable as the backfill source.

## Review trigger

Revisit if adoption stalls — if, some weeks after ship, no restaurant with a
structured menu has enabled it, the default is wrong or the switch is not
discoverable, and that is evidence rather than a guess. Revisit sooner if the
brand-override case turns out to cover most multi-location brands, since that
would mean self-service enablement — the entire reason this option beat the
`restaurants` column — does not actually reach them.
