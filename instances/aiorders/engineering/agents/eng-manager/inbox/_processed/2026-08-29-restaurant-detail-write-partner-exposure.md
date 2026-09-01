---
type: finding
agent: architect
project: aiorders-admin-hub
severity: P1
found_during: ENG-015 design
created: 2026-08-29
---

# `updateRestaurant()`/`updateBrandOwner()` — same unconditional-service-role defect ENG-015 fixes, but reachable and unfixed

## Symptom

A `partner-admin`/`partner-user` who has, or can guess, another agency's
`restaurant.id` can write to that restaurant's record — not just read it.

## Evidence

`aiorders-api`'s `admin-portal/handlers/restaurants.ts` — `updateRestaurant()`
(PUT `/admin-portal/restaurants/:id`) and `updateBrandOwner()` (PUT
`/admin-portal/restaurants/:id/brand-owner`) both use `adminSupabase`
(service-role) unconditionally, with no role check and no ownership check —
the identical shape `ENG-015` is fixing in this same file's `getRestaurants()`
and `getRestaurantById()`.

Confirmed reachable, not hypothetical: `aiorders-admin-hub`'s
`RestaurantDetails.tsx` (route `/restaurants/:id/details`) and
`Activation.tsx` (route `/restaurants/:id/activation`) both call this PUT
endpoint. Both routes are gated only by `ProtectedRoute.tsx`'s generic
`hasAdminAccess()` (`admin`, `sub-admin`, `partner-admin`, `partner-user`) —
neither carries the partner-specific block `/influencers` and `/billing`
have. So a partner can open either page for any restaurant id and submit a
write that lands.

## Impact

Cross-tenant write access, not just the read exposure `ENG-015` names — one
agency editing (or reassigning the brand owner of) another agency's
restaurant record. Same severity class as `ENG-015`'s two confirmed defects,
same root cause, same file.

## Why not fixed inline on ENG-015

`ENG-015`'s PRD scope and G1 approval are explicitly "the two confirmed
gaps" (Restaurants-page read-scoping, add-restaurant write-rejection) — its
own non-goals: "A full audit of every admin-portal page for partner-role
exposure... anything else found later during real use is a new bug, not
silently folded in here." This wasn't one of the two investigated or named
defects; per `schedules/eng_build_loop.md` step 3, an agent-originated
finding becomes a proposals.md line for a batched G1, not a ticket or an
in-flight scope change, unless it's a P0 on a non-internal project. This is
rated P1 (a workaround exists — don't ship restaurant ids to partners you
don't trust, in practice unenforceable, but not "production down" or the
kind of live exploitation `aiorders-admin-hub`'s existing P0 incident
process — see `ENG-022` — was built for), so it does not qualify for that
carve-out.

## Smallest fix, for whoever proposes/scopes it

Same shape as `ENG-015`: role branch (`admin`/`sub-admin` → `adminSupabase`
unchanged; `partner-admin`/`partner-user` → RLS-scoped client) plus a
partner-scoped `UPDATE` RLS policy on `restaurants` (`WITH CHECK`/`USING`
via `brands.partner_id`, same join `ENG-015`'s new SELECT/INSERT policies
use). Likely `S`–`M`: two functions, one additive migration, no new
concepts — `ENG-015`'s design doc
(`agents/architect/designs/ENG-015-agency-reseller-brand-scoping.md`) has
the exact policy shape to copy.

---

**Processed 2026-08-29**, `watch` event pass (context `schtasks`), per
`schedules/eng_build_loop.md` step 3: rated P1, not P0, so it does not
qualify for the immediate-ticket carve-out (that's reserved for a P0 on a
non-internal-lane project). Added as a line to `agents/eng-manager/proposals.md`
(Open) rather than shaped into a ticket — no id allocated, no board row
created. Moved here to `_processed/` to match. Surfaces to the approver as
part of the next batched proposals G1 in the weekly report.
