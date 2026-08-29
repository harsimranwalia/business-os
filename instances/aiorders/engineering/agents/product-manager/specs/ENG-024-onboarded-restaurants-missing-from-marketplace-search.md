---
ticket: ENG-024
project: aiorders-api
status: approved         # auto-approved — type: bug, fast lane; see Decision
size: XS
author: product-manager
created: 2026-08-29
decided: 2026-08-29      # auto-skipped, not a human answer — see Decision
---

# Restaurants added through onboarding never appear in FoodSwipe marketplace search

## Readback

**You said:** "restraurants being added from foodswipe sign up page are not showing up on search by location."

**Understood as:** A restaurant added through the brand-portal onboarding wizard's
"Add Locations" step (the FoodSwipe/AIOrders sign-up flow) does not appear when a
customer searches the FoodSwipe marketplace by location — or, as traced below, in
any marketplace search at all, not only the location-sorted view.

**Assumed, and worth correcting if wrong:**
- "Foodswipe sign up page" means `restaurant-portal`'s onboarding wizard
  (`AddLocationsStep.tsx`, part of `OnboardingWizard`) — the flow a brand owner
  uses to add their own restaurant location(s) after signing up — not the public
  "claim your restaurant" flow (`restaurant-claims`, a different insert path, see
  Risks below). If the approver meant the claim flow instead, the fix target
  changes.

**Second reading:** skipped by design — fast lane (`type: bug`, `size: XS`);
`skills/request-readback/SKILL.md`'s dual-reading/divergence check is for
full-lane requests only. Root cause below was confirmed directly against live
code across two repos rather than inferred, which is what a bug report gets
instead of a second blind reading.

## Problem

Every restaurant added via the onboarding wizard is inserted with `approved:
true` (auto-approved — no admin review, since these are self-service brand
owners, not public claims) but the insert never sets the separate
`show_in_marketplace` flag. Every marketplace search path — the primary
geo-sorted RPC, its fallback query, and the sitemap — hard-requires
`show_in_marketplace = true` in addition to `approved = true`. The row is left
at whatever the column's default resolves to, which the approver's own report
confirms is not `true`. Nothing in the sign-up flow ever sets it, there is no
error shown to the owner (they get a "Location Added" success toast), and
nothing tells anyone a manual step is still needed. The only way a signed-up
restaurant becomes visible today is a staff member separately opening the
internal admin tool and manually flipping a "Show in Marketplace" toggle — a
step this flow gives no one any reason to know about.

**Evidence, traced end to end:**
- `aiorders-api/supabase/functions/restaurant-portal-onboarding/restaurants.ts`,
  `createRestaurant` — inserts `name`, `address`, `google_place_id`, `brand_id`,
  `approved: true`. No `show_in_marketplace`.
- The same file's `updateRestaurantDetails`, called immediately after in the
  same onboarding action (`AddLocationsStep.tsx` → `addLocationFromPlace`),
  writes Google Places data via `mapPlaceToRestaurantRow`
  (`_shared/googlePlaces.ts`) — whose `RESTAURANT_PLACE_COLUMNS` whitelist also
  excludes `show_in_marketplace`. Confirmed: nothing anywhere in the sign-up
  path ever writes this field.
- `aiorders-api/supabase/functions/restaurant-marketplace/handlers/restaurants.ts`
  — both `handleRestaurantDiscovery` (via the `get_restaurants_optimized` RPC)
  and its own fallback query filter `.eq('approved', true).eq('show_in_marketplace',
  true)`. `handleRestaurantDetail` and `sitemap.ts` carry the same
  `show_in_marketplace = true` requirement.
- `restaurant-marketplace/supabase/migrations/20240302_optimize_restaurant_discovery.sql`
  — `get_restaurants_optimized` filters `WHERE r.approved = true AND
  r.show_in_marketplace = true` before any city/cuisine/geo logic runs, so a
  restaurant failing this gate never reaches the distance sort regardless of
  its `geo` value (which onboarding does set correctly via
  `updateRestaurantDetails` — this is specifically a visibility-flag gap, not a
  geocoding one).
- `aiorders-admin-hub/src/pages/RestaurantDetails.tsx` — the only place in the
  codebase that ever sets `show_in_marketplace: true`: a manual "Show in
  Marketplace" checkbox on the internal admin tool's restaurant detail page.

## Why now

The bug silently defeats the entire point of the sign-up flow — a restaurant
that signs up expecting FoodSwipe customer discovery gets none, with no error
and no signal to the owner or to staff that anything is wrong. Every restaurant
onboarded through this path to date is affected.

## Users

Restaurant owners who complete FoodSwipe onboarding (expecting to be
discoverable immediately), and the customers searching the marketplace who
should be finding them.

## Proposed change

A restaurant added through onboarding is visible in FoodSwipe marketplace
search — including location-sorted search — as soon as onboarding completes,
with no separate manual step. Restaurants already added through this flow
before the fix become visible too, not only new sign-ups going forward.

## Acceptance criteria

1. `[stated]` Given a brand owner completes the "Add Locations" onboarding
   step for a new restaurant, when the location is added, then that restaurant
   appears in FoodSwipe marketplace search results — including a
   location/distance-sorted search — with no manual admin action.
2. `[inferred]` Given a restaurant was added through this flow before the fix
   ships, when the fix ships, then a one-time backfill makes that restaurant
   visible in search too — "fix the bug" means the restaurants already added,
   not only future ones.
3. `[proposed]` Given the insert already sets `approved: true` (the code's own
   expressed intent: this restaurant is immediately live), when a restaurant is
   created through this path, then `show_in_marketplace` is set consistently
   with that same intent, rather than left to whatever the column defaults to.

## Non-goals

- **The `restaurant-claims` insert path** (`aiorders-api/supabase/functions/restaurant-claims/index.ts`)
  — a separate "claim your restaurant" flow with the identical omission, but
  which also sets `approved: false` by design pending manual review, so the
  same *symptom* may not be the same *bug*: whether the claims-approval step
  (wherever a pending claim gets approved) sets `show_in_marketplace` at that
  point is unverified and out of scope here. The reported bug is specifically
  the onboarding sign-up path. Flagged as an observation for a follow-up look,
  not folded into this ticket.
- Not changing the admin "Show in Marketplace" toggle's existence or behavior,
  and not building an approval workflow or notification around it.
- Not auditing every other write path to `restaurants` beyond the two insert
  sites found (`restaurant-portal-onboarding`, `restaurant-claims`).

## Risks and unknowns

- `show_in_marketplace`'s actual DB-level default (`false` vs. `NULL`) isn't
  defined in any tracked migration across all five repos — the column appears
  to have been added directly in the Supabase dashboard rather than through a
  migration file. The approver's own report is the confirmation that it does
  not resolve to `true`; the engineer building this should confirm the literal
  default while there, since it may be worth fixing at the column level (not
  just in this one insert) so any future insert path doesn't reintroduce the
  same gap. That's a design choice for whoever builds this, not decided here.

## Cost

- Build: **XS** — one field added to one existing insert
  (`createRestaurant`), plus a one-time backfill `UPDATE` for existing
  affected rows. Single file for the code change, no schema change (column
  already exists), no new interface. Rough build time: under an hour
  (`definition-of-done.md` Size table).
- Run: $0/month — no new infrastructure, no new recurring cost.

## Decision

- **The approver's answer:** auto-approved — `type: bug` auto-skips G1 per
  `definition-of-done.md`'s state table (`awaiting-scope` "auto-skipped for
  XS / bug / chore / security"). Not a human answer; recorded here so the
  skip is visible rather than silent.
- **Date:** 2026-08-29
- **Notes:** Lane is `fast` (`size: XS`, `type: bug`, touches none of the
  fast-lane exclusion list: auth, payments, data deletion, schema,
  dependencies, model calls, public contracts, PII) — see
  `definition-of-done.md`, "The four lanes."
