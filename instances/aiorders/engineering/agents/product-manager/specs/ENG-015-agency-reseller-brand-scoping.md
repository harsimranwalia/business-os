---
ticket: ENG-015
project: aiorders-admin-hub
status: approved
size: M
author: product-manager
created: 2026-08-29
decided: 2026-08-29
---

# Agency/reseller users: brand-scoped locations and a working add-location path

## Readback

**You said:** "admin portal is not optimized for new agency users/ resellers of aiorders.

they are not able to add locations , security issue if they go to /restaurant they can see all locations. they dashboard data is super admin data not just their brands. same for other tabs like influencer they are able to see all or user ."

**Understood as:** Agency/reseller staff — the `partner-admin`/`partner-user` roles that already exist in the system, each tied to specific brands via `brands.partner_id` and the existing `/partners/:id/assign-brands` screen — should only ever see and act on their own brand(s)' data in the admin portal, never platform-wide data, and should be able to add a new restaurant location under their own brand themselves. Checked against the live code rather than built from the literal claims alone: two of the four named symptoms are real and precisely reproducible; two are not currently reproducible on this branch. See Evidence below and the correction in "Assumed."

**Assumed, and worth correcting if wrong:**
- "Locations" = restaurants (the `restaurants` table/page); "their brands" = the brand(s) a partner is assigned via the existing `partner_id` relationship.
- **Confirmed true in code:** the Restaurants page (`/restaurants` — what you're calling `/restaurant`) and the ability to add a restaurant are broken exactly as reported. See Evidence.
- **Confirmed NOT currently true in code:** the Dashboard already hard-blocks partner roles with a "Partner Dashboard — coming soon" placeholder (no super-admin figures shown at all), and the Influencers tab already hard-blocks partner roles with an explicit "Access Denied" screen (hidden from the sidebar too). Neither leaks data today on this branch.
- "or user" is read as a second tab, `/users` — also checked, also already fully blocked for partner roles (admin-only, both frontend and backend).
- Given three of the four named surfaces already carry a partner-specific block, the two "already blocked" findings above most likely describe a deployed version older than this branch, or what you saw before a prior partial fix — not something to silently re-break by "fixing" a page that isn't leaking. Worth a fast confirmation rather than assuming either way.
- Super-admin (`admin`, `sub-admin`) visibility and workflow are unaffected — nothing here narrows staff access.

**Second reading agreed / diverged on:** No material divergence on intent. The architect's blind reading (raw request + business profile only, no code access) independently converged on the same shape: a systemic tenancy-scoping gap across the portal rather than isolated per-page bugs, one that has to be fixed at the data layer rather than by hiding UI, implying an agency → brand → location ownership graph. It additionally guessed, unprompted, that "which locations belong to which agency" would have to already exist as a real relationship for the request to make sense at all — confirmed true (`brands.partner_id`, live in the schema, already the backbone of a dedicated assign-brands screen). Both readings' guesses about exactly which tabs leak were necessarily unconfirmed without code access; checking the live repos narrowed the original four named symptoms down to two confirmed, evidenced gaps rather than building against all four as stated.

## Problem

Agency/reseller ("partner") accounts are a real, existing role in the admin portal, already tied to specific brands — but that boundary isn't enforced everywhere it needs to be. On the Restaurants page, a partner-admin/partner-user currently sees every restaurant on the entire platform, not just their own brand's: a live cross-tenant data exposure on a real, reachable page, for real onboarded users, today. Separately, the same role cannot successfully add a new restaurant location under their own brand — the write is silently rejected by the database. Both block agency/reseller users from being safely, usefully onboarded.

**Evidence, not assumed** (checked against the live `aiorders-admin-hub` and `aiorders-api` worktrees):
- `getRestaurants()` in `aiorders-api`'s `admin-portal/handlers/restaurants.ts` always queries with the service-role client (`adminSupabase`), unconditionally — no role check, no `partner_id` filter, unlike its sibling `brands.ts` handler, which already branches: service-role only for `role === 'admin'`, the caller's own RLS-scoped client otherwise. `restaurants.ts` never got that branch. Any of the four roles that pass the top-level `admin-portal` gate (`admin`, `sub-admin`, `partner-admin`, `partner-user`) gets every row.
- The only RLS policies on `restaurants` that permit `INSERT` are "restaurant owners manage their own row" (`auth.uid() = id` — never true for a brand-new row) and "Admins can manage all restaurants" (`role IN ('admin', 'sub-admin')`, FOR ALL). Partner roles are in neither. The "Add Restaurant" button (`AddRestaurantModal.tsx`, reachable from the Brands page, not itself role-gated) does a direct client-side `.insert()` into `restaurants` — which Postgres RLS then silently rejects for a partner caller. This is also why a partner-created row would auto-approve (`approved: true`, unconditionally, in that same insert) if the policy gap were fixed with no other change — see acceptance criterion 5.
- `Dashboard.tsx` returns a placeholder for `role === 'partner-admin' || 'partner-user'` before ever fetching real stats. `ProtectedRoute.tsx` explicitly denies `partner-admin`/`partner-user` on `/influencers` (also hidden from `AppSidebar`). `/users` requires `role === 'admin'` exactly, both in `ProtectedRoute.tsx` and in the backend's own `verifyAdminAccess()` — rejects even `sub-admin`, let alone partner roles. All three read as deliberate, if inconsistent, prior fixes (block outright rather than scope), not oversights.
- `brands.partner_id` is a real foreign key, already the basis of a working `/partners/:id/assign-brands` screen — the ownership graph the fix needs already exists; nothing here is net-new schema.

## Why now

Reported from direct use by newly onboarded agency/reseller users — not hypothetical. It's actively blocking them (can't self-serve a location) and actively over-exposing data (every partner can currently see every other partner's and every restaurant's locations) right now.

## Users

Agency/reseller staff (`partner-admin`, `partner-user`) — external parties, plausibly competitors with each other, which is exactly why unscoped visibility here is a security issue and not just a rough edge.

## Proposed change

- The Restaurants page and its underlying API return, for a partner-admin/partner-user, only restaurants belonging to brand(s) assigned to them — enforced server-side, the same way `brands.ts` already does it, not filtered client-side.
- A partner-admin/partner-user can add a new restaurant under one of their own brands, and the write is rejected if attempted against a brand not assigned to them.
- Dashboard, Influencers, and Users pages are untouched — investigated and found already blocking partner roles outright, not leaking.

## Acceptance criteria

1. `[stated]` Given a partner-admin or partner-user, when they load the Restaurants page, then they see only restaurants belonging to their own assigned brand(s) — never another agency's or the platform's full list.
2. `[inferred]` Given the same user, when the underlying restaurants API is called directly (not only through the page), then it enforces the same brand scoping itself — the fix closes `getRestaurants()`'s unconditional service-role bypass, not just a UI filter.
3. `[stated]` Given a partner-admin or partner-user, when they use "Add Restaurant" under one of their own brands, then the restaurant is created successfully and associated with that brand.
4. `[inferred]` Given a partner-admin or partner-user, when they attempt to add a restaurant under a brand not assigned to them, then the write is rejected — closed by a role/ownership check, not by trusting the frontend's brand selector.
5. `[proposed]` Given a partner-created restaurant, when it's created, then it is held for staff review rather than auto-approved the way admin-created ones are today (today's insert sets `approved: true` unconditionally). Proposed default: held. Reversible with a one-line rider on this G1 if you'd rather they auto-approve the same as staff-created ones.
6. `[stated]` Given an `admin` or `sub-admin` user, when they use the Restaurants page or add a restaurant, then behavior is identical to today.

## Non-goals

- Rebuilding the Dashboard's partner view into a real, brand-scoped dashboard. It's a deliberate placeholder today, not a leak — a real partner dashboard is a reasonable follow-on but is its own scoped feature, not this fix.
- Any change to the Influencers or Users pages — both already fully block partner roles; investigated and found not reproducing the report.
- Any change to super-admin (`admin`/`sub-admin`) access or workflow.
- A full audit of every admin-portal page for partner-role exposure. This fixes the two confirmed gaps; anything else found later during real use is a new bug, not silently folded in here.
- Agencies creating new **brands** — only locations under brand(s) already assigned to them.

## Risks and unknowns

- The Dashboard/Influencers/Users discrepancy above — worth a fast confirmation that you're testing against this same branch/deploy, since building against a stale claim wastes a cycle either way, and *not* investigating it before building would have meant either silently skipping real work or silently redoing work that's already done.
- Whether the `influencers` table has any RLS policy at all — none appears anywhere in tracked migration history (the same untracked-schema-history gap already on record for `profiles`). Not this ticket's problem since the page is already blocked regardless of what the table's policy says, but worth knowing before any future ticket opens that page to partners.

## Cost

- Build: `M` — one backend handler fix (role-based client selection, the same pattern `brands.ts` already uses) plus one RLS migration (add partner roles to the `restaurants` INSERT policy, scoped to their own brand). No frontend change needed for the read path — the page already renders whatever the API returns. Estimate: half a day to a day.
- Run: $0/month — no new infrastructure, no new vendor.

## Decision

Filled in after G1.

- **The approver's answer:**
- **Date:**
- **Notes:**
