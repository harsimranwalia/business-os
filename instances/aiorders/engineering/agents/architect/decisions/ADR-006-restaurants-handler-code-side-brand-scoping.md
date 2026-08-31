---
id: ADR-006
title: admin-portal restaurants handler enforces brand scoping in code, not via RLS/client-branch
project: aiorders-api
ticket: ENG-015
status: accepted
decided_by: architect
date: 2026-08-31
supersedes:
superseded_by:
---

# ADR-006: admin-portal `restaurants` handler enforces brand scoping in code, not via RLS/client-branch

## Context

`ENG-015`'s PRD, written by the PM without repo access to `restaurants.ts`'s
neighbors beyond what the investigation quoted, proposes fixing
`getRestaurants()`'s unconditional `adminSupabase` (service-role) use "the
same way `brands.ts` already does it" — `brands.ts`'s `getAllBrands()`
branches `client = role === 'admin' ? adminSupabase : supabase` and trusts
Postgres RLS to scope the non-admin case to the caller's own rows.

Tracing what that would actually do to `restaurants` today, rather than
trusting the pattern-match: three migrations dated `20250814065341`,
`20250814065439`, `20250814065606` (all after the initial RLS migration)
progressively locked the table down — dropped the original "Public can view
approved restaurants" policy, moved public reads to a new `restaurants_public`
view (safe columns only), and landed a policy literally named
`"No direct public access to restaurants table"` with `USING (false)`. The
live SELECT-eligible policies on `public.restaurants` today are: the
`false` one (grants nothing), "Restaurant managers can view their managed
restaurants" (via `restaurant_managers`, not `brand_managers` — a partner has
no row there), "Admins can manage all restaurants" (`role IN ('admin',
'sub-admin')` — not a partner), and "Restaurant owners can manage their own
restaurant" (`auth.uid() = id` — never true for a restaurant row). **A
partner routed through the RLS-scoped client would see zero rows**, not "their
own brand's rows" — there is no policy today that grants a partner anything on
this table, because no one has ever added one.

Separately: `brands` — the table `brands.ts`'s own branch depends on for the
*same* pattern — has **zero RLS policies in tracked migration history at
all** (`git grep -n "ON public.brands"` across every migration: no matches).
Either `brands`' RLS is disabled, or its policies were hand-added in the
Supabase dashboard and never committed — the same untracked-schema-history gap
this ticket's own PRD already names for `profiles`/`influencers`. From this
repo, there is no way to verify what actually scopes a partner's view of the
Brands page today, or whether it's actually correct.

## Decision

`getRestaurants()`, `getRestaurantById()`, and `updateRestaurant()` (all three
functions in this handler that read or write a `restaurants` row, all sharing
the identical unconditional-`adminSupabase` defect) branch on `isStaff(profile)`
(`role` or `additional_roles` containing `admin`/`sub-admin`) rather than
positively detecting "is a partner." The non-staff branch resolves the
caller's owned brand ids itself — `adminSupabase.from('brands').select('id')
.eq('partner_id', user.id)` — and applies an explicit `.in('brand_id', ids)`
filter (list) or membership check (single-record read/write), still through
the service-role client. RLS is not the enforcement boundary for any of this;
it's bypassed deliberately, the same way every other query in this file
already bypasses it for the staff path.

The new INSERT policy (separate migration, same ticket) is the one place RLS
*is* the enforcement point — because `AddRestaurantModal.tsx` inserts directly
through the ambient RLS-scoped client, not through this edge function. That
policy is scoped narrowly and explicitly (`brands.partner_id = auth.uid()`,
`approved = false`), not by loosening or trusting any pre-existing SELECT
policy.

## Alternatives

| Option | Why not |
|---|---|
| Mirror `brands.ts` literally: branch to `auth.supabase` for non-admin, trust RLS to scope | Traced above to return zero rows for a partner today, not a leak in the other direction — RLS on this table currently has no partner-scoped policy at all. Would need a new SELECT policy added anyway, at which point the client-branch adds nothing the code-side filter doesn't already give for free, and the code-side version doesn't depend on `brands`' own unverifiable, untracked RLS state as a load-bearing assumption. |
| Add a new partner-scoped SELECT policy on `restaurants` and switch to the RLS-scoped client | Not rejected outright — would be reasonable defense-in-depth — but not required by AC1/AC2, which ask the *API* to enforce scoping, not RLS specifically. Left out of this design; nothing here blocks adding it later. |
| Leave `getRestaurantById`/`updateRestaurant` unfixed, since the PRD's Evidence section names only `getRestaurants()` | Both are reachable today by a partner via a direct API call to the same resource this ticket is about, and AC2 says the fix must not be "just a UI filter." Leaving them open would ship a security ticket that closes one of three doors into the same room. |

## Consequences

**Accepted:** `restaurants.ts` now has two enforcement layers that don't trust
each other — code-side brand filtering for reads/updates through this
function, and RLS for the one write path that bypasses this function
entirely. A future engineer adding a fourth `restaurants`-touching action here
needs to pick up the same `isStaff`/`getPartnerBrandIds` pair rather than
assume RLS already covers it — it doesn't.

**Gained:** the fix doesn't depend on verifying or trusting `brands`' own
untracked RLS state, which this codebase currently has no way to do from the
repo alone.

**Reversibility:** removing the code-side filter, or later adding a real
SELECT policy and switching to the RLS-scoped client, is a code change with no
data migration — no existing row is touched by this decision.

## Review trigger

If `brands`' or `restaurants`' RLS policies are ever reconciled into tracked
migrations (closing the untracked-schema-history gap named here and in the
PRD), revisit whether the code-side filter in this file is now redundant with
a real policy — and if so, whether keeping both is worth the duplication or
whether one should be dropped.
