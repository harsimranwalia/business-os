---
ticket: ENG-015
project: aiorders-admin-hub
author: architect
created: 2026-08-29
adrs: []
one_way_doors: []
touches_data: true
touches_models: false
---

# Agency/reseller brand-scoped restaurants — technical design

## Approach

Close the propagation gap the PRD names: the `partner-admin`/`partner-user`
role pair and the `brands.partner_id` ownership relationship already exist
and are already enforced on the Brands/assign-brands screen, but
`admin-portal/handlers/restaurants.ts` never got a role branch when partner
roles were added to the top-level `admin-portal` gate, and `restaurants`'
RLS was never given a partner-scoped policy. Two additive RLS policies
(SELECT + INSERT, scoped through `brands.partner_id`) close the
database-level gap; the one handler file's two read functions that still
unconditionally use the service-role client get the same role-branch shape
`brands.ts`'s `getAllBrands()` already uses (widened to cover both `admin`
and `sub-admin`, since AC6 requires both unaffected — `brands.ts` only
special-cases `admin`, which doesn't fit here; see Alternatives); one
frontend conditional stops a partner-created restaurant from self-approving.
No new table, column, role, or ownership relationship — this wires an
existing model into the one file and the one insert path that missed it,
the same shape `ENG-022` used for a sibling tenant-isolation gap.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `supabase/migrations/20260829230000_partner_restaurant_scoping.sql` (`aiorders-api`) | new — two additive RLS policies on `public.restaurants` (SELECT, INSERT), scoped through `brands.partner_id`; see Data | database |
| `supabase/functions/admin-portal/handlers/restaurants.ts` — `getRestaurants()` (`aiorders-api`) | modify — role branch: `admin`/`sub-admin` keep the unconditional `adminSupabase` call (unchanged, AC6); `partner-admin`/`partner-user` (the only other roles that reach this handler, per the top-level gate in `index.ts`) use `auth.supabase`, which the new SELECT policy scopes to their own brand(s)' restaurants | backend |
| `supabase/functions/admin-portal/handlers/restaurants.ts` — `getRestaurantById()` (`aiorders-api`) | modify — same role branch as `getRestaurants()`. Not named in the PRD's evidence paragraph, but same file, same unconditional-`adminSupabase` defect; left open it stays a direct-object-reference leak of one full restaurant record (another agency's, by guessed/known id) immediately beside the fix. See Alternatives. | backend |
| `src/components/AddRestaurantModal.tsx` (`aiorders-admin-hub`) | modify — the unconditional `approved: true` (current insert payload, `addRestaurantToBrand()`) becomes conditional on the caller's role: partner roles insert `approved: false`; `admin`/`sub-admin` unchanged at `approved: true`. Component doesn't currently call `useAuth()` — needs that added to read `profile.role`/`additional_roles` | frontend |

## Data

`brands.partner_id` (nullable uuid, FK to `profiles` — `brands_partner_id_fkey`)
already exists live, confirmed via `aiorders-admin-hub`'s generated
`src/integrations/supabase/types.ts`. Neither that column nor any policy on
`public.brands` appears anywhere in `aiorders-api`'s tracked migration
history — grepped the full `supabase/migrations/` tree for `partner_id` and
for any `CREATE TABLE`/`CREATE POLICY` naming `brands`: zero hits either
way. The table predates tracked migrations entirely — the same class of gap
the PRD's own Risks section names for `profiles`, just not previously
confirmed for `brands` too. This design adds no column; it adds two
policies on `public.restaurants` that reference the already-live column:

```sql
-- Partners may view restaurants belonging to brand(s) assigned to them
CREATE POLICY "Partners can view their assigned brands' restaurants"
ON public.restaurants
FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM public.brands
    WHERE brands.id = restaurants.brand_id
      AND brands.partner_id = auth.uid()
  )
  AND EXISTS (
    SELECT 1 FROM public.profiles
    WHERE profiles.id = auth.uid()
      AND profiles.role IN ('partner-admin', 'partner-user')
  )
);

-- Partners may add a restaurant only under brand(s) assigned to them, and
-- it must land unapproved (AC5) -- checked against the row being inserted,
-- not the caller's claim about it
CREATE POLICY "Partners can add restaurants to their assigned brands"
ON public.restaurants
FOR INSERT
WITH CHECK (
  approved = false
  AND EXISTS (
    SELECT 1 FROM public.brands
    WHERE brands.id = restaurants.brand_id
      AND brands.partner_id = auth.uid()
  )
  AND EXISTS (
    SELECT 1 FROM public.profiles
    WHERE profiles.id = auth.uid()
      AND profiles.role IN ('partner-admin', 'partner-user')
  )
);
```

Both are additive — no `DROP POLICY` — so "Public can view approved
restaurants", "Restaurant owners…", "Restaurant managers…", and "Admins can
manage all restaurants" are untouched and keep applying exactly as today
(Postgres RLS policies are permissive and OR'd; a new policy only grants,
never revokes). `role` is checked explicitly against `profiles`, matching
every existing policy in this same migration file's own idiom, rather than
trusting `partner_id` alone — defense in depth against that column ever
being set to a non-partner profile by anything other than the existing
assign-brands screen, which only ever offers partner-role profiles
(`partners.ts`'s `getAllPartners()` filter) — a frontend guarantee, not a
database one.

No backfill: no column is added, so no existing row needs a new value.

## Interfaces

`GET /admin-portal/restaurants` (`getRestaurants`) and
`GET /admin-portal/restaurants/:id` (`getRestaurantById`): response shape
unchanged for every role. For `partner-admin`/`partner-user` the row set
narrows to their own brand(s); for `admin`/`sub-admin`, unchanged. No new
error shape — a partner requesting another agency's restaurant by id now
gets today's existing not-found handling (`getRestaurantById`'s `.single()`
throws when no row matches, already caught by the existing `try/catch` → 500
"Failed to fetch restaurant"), not a distinguishable 403. That's arguably
better than a 403 here (doesn't confirm the id exists at all), and it's free
— not a new behavior to design.

Client-side `.insert()` into `restaurants` from `AddRestaurantModal.tsx`: a
partner inserting under a brand not assigned to them now fails the new
`WITH CHECK` (a Postgres RLS violation, surfaced by the modal's existing
generic `catch` → "Failed to add restaurant" toast — no new error handling
needed). A partner inserting under their own brand now always lands
`approved: false` regardless of what the client sends, because the frontend
stops sending `true` for partner callers — the same "don't trust the
frontend" reasoning the PRD already applies to AC4 (brand ownership) applies
here to AC5 (the approval default).

## Alternatives considered

1. **Fix only `getRestaurants()`, leave `getRestaurantById()` untouched**,
   matching the PRD evidence paragraph's literal wording (it names
   `getRestaurants()` specifically). Rejected — it would close the list-page
   leak while leaving a same-shaped single-record leak reachable by anyone
   who can construct or guess a `/restaurants/{id}` call, in the same file,
   from the root cause the ticket's own Notes describe as "the restaurants
   handler never got that branch" — the handler, not one function in it.
2. **Filter by brand in application code** (fetch the caller's brand ids,
   then `.in('brand_id', ids)`) instead of adding RLS policies. Rejected as
   the sole fix: the handler already has exactly this general shape today
   (an unconditional query with no filter) and still leaks everything,
   because the underlying client is service-role — an application-level
   filter is trivially bypassed by any other current or future caller of
   the same table (a direct PostgREST call carrying the partner's own JWT,
   bypassing this edge function entirely). RLS is the actual enforcement
   boundary; the handler's client-selection branch only decides whether
   that boundary applies to a given call — `brands.ts`'s own existing
   pattern, kept here rather than reinvented.
3. **Copy `brands.ts`'s exact role check** (`role === 'admin' ?
   adminSupabase : supabase`). Rejected as-is: AC6 requires `sub-admin`
   unaffected too, and today — with no role branch at all — `sub-admin`
   already gets the full, unconditional list via `adminSupabase`. Copying
   `brands.ts` literally would silently narrow `sub-admin`'s own access,
   which is a regression the PRD doesn't ask for and QA would have to catch
   as a new bug. The branch condition here is `role === 'admin' ||
   role === 'sub-admin'`, not a literal copy.
4. **Trust `AddRestaurantModal.tsx`'s own role check for AC5** (client sends
   `approved: false` for partners; no RLS check on the value). Rejected for
   the same reason the PRD already gives for AC4 (brand ownership) — a value
   the frontend chooses to send is not enforcement. `WITH CHECK (approved =
   false AND …)` is what actually holds if a partner calls the insert
   directly; the frontend change only avoids an avoidable RLS rejection on
   the happy path for a legitimate partner user.

## One-way doors

None. Both new policies are additive and reversible (a follow-up migration
can `DROP POLICY` either, no data loss); the handler and frontend changes
are ordinary branches on an already-existing role and an already-existing
ownership column. No new datastore, vendor, auth model, public contract, or
data model — the same verdict `ENG-022` reached for the same shape of fix.

## Risks

- **`brands.partner_id` and every policy on `public.brands` are absent from
  tracked migration history** (confirmed: zero `partner_id` hits and no
  `CREATE TABLE`/`CREATE POLICY` for `public.brands` anywhere under
  `supabase/migrations/`; the table predates tracked migrations entirely).
  This design's two new policies are the first tracked-migration reference
  to `partner_id`. If it's ever renamed or dropped outside a tracked
  migration, both policies fail closed (deny / Postgres error on the
  missing column) rather than open — the safe direction, but worth naming
  so a future "why did partner restaurants disappear" investigation starts
  here instead of re-discovering the gap.
- **`updateRestaurant()` and `updateBrandOwner()`, same file, same
  unconditional-`adminSupabase` shape, are not fixed by this design — and
  unlike `getRestaurantById`, they're reachable today.** `RestaurantDetails.tsx`
  (`/restaurants/:id/details`) and `Activation.tsx`
  (`/restaurants/:id/activation`) both call `PUT /admin-portal/restaurants/:id`,
  and neither route carries a partner-specific block in `ProtectedRoute.tsx`
  the way `/influencers` and `/billing` do — only the generic
  `hasAdminAccess()` check, which partner roles pass. A partner who has (or
  guesses) another agency's restaurant id can open that page and submit an
  edit that writes. Same root cause as the two confirmed defects, same
  file, but a write capability the PRD never named or investigated
  (non-goals: "the two confirmed gaps... anything else found later... is a
  new bug, not silently folded in here") — filed as a finding to the EM
  (`agents/eng-manager/inbox/`) rather than fixed here or silently added to
  this ticket's already-G1'd scope.
- **Whether the Brands page itself (`getAllBrands`) already scopes to a
  partner's own brands is unconfirmed** — its non-admin branch already uses
  the RLS-scoped client (the same pattern this design extends to
  `restaurants.ts`), but `public.brands`' own RLS is exactly the untracked
  history named above, so what it actually returns for a partner caller
  can't be verified by reading code alone. Not this ticket's problem (the
  PRD names Restaurants, not Brands, as the leaking list) and not
  investigated further here; logged as an observation rather than assumed
  either way.
- **RLS policy behavior can't be unit-tested with this repo's current
  tooling** (no local Postgres/Docker on this host — `config/projects.md`
  already names this gap). The handler's role-branch logic gets a real
  `deno test` (see Rollout); the two policies themselves need a manual
  spot-check against the live Supabase project, same as every other
  RLS-touching ticket on this instance today.

## Rollout

Straight, no flag — an additive migration plus a logic-only branch on
existing endpoints and an existing insert path, no backfill. Branch → PR →
gates → human merge (`aiorders-admin-hub` and `aiorders-api` are both L1) →
deploy (Cloudflare for the frontend; the migration applied to Supabase
project `bmnmnejwdxbcqinqkwko`).

**Test approach**, matching `ENG-022`'s own precedent for this same
no-test-runner backend (`config/projects.md`: `aiorders-api` has no
`package.json`, so no npm test target — Deno ships its own runner, no config
file required): `deno test` against a new
`admin-portal/handlers/restaurants_test.ts`, stubbing a minimal
`SupabaseClient`-shaped object per role (admin, sub-admin,
partner-owns-the-brand, partner-does-not-own-the-brand) and asserting which
client (`adminSupabase` vs `supabase`) each role resolves to and what rows
come back. The two new SQL policies aren't reachable by that stub (no live
Postgres on this host) — QA verifies them by hand against the live Supabase
project, a real manual-verification case per `definition-of-done.md`, not
automation this repo currently has the means to write.
`aiorders-admin-hub`'s change gets `npm run lint` + `npm run build` (its own
registered commands — no test command exists on any registered project)
plus the same manual check.

Rollback: revert the migration (`DROP POLICY` on both, or a follow-up
migration) and revert the handler/frontend commits — no data was migrated,
so a revert fully restores prior (broken) behavior with nothing further to
clean up, same as `ENG-022`.

**Manual verification checklist for QA:**
1. Partner A, own brand: Restaurants page shows only Partner A's brand(s)'
   restaurants.
2. Partner A: `GET /admin-portal/restaurants/{Partner B's restaurant id}` —
   no longer returns Partner B's data.
3. Partner A: adds a restaurant under their own brand — succeeds, lands
   `approved: false`.
4. Partner A: attempts to add a restaurant under Partner B's brand (tamper
   the request past the UI) — rejected.
5. Admin and sub-admin: Restaurants page and Add Restaurant behave exactly
   as before (full list, auto-approved).

## Out of scope

- `updateRestaurant()` / `updateBrandOwner()` and the two pages that reach
  them — see Risks; filed as a finding, not fixed here.
- The Brands page's own partner-scoping — unconfirmed, not investigated
  further (see Risks).
- Dashboard, Influencers, Users pages — PRD non-goals; already confirmed
  blocking partner roles outright.
- Any change to `admin`/`sub-admin` behavior, workflow, or the existing
  public/manager RLS policies on `restaurants`.
- Wiring `deno test` into CI for `admin-portal/` — same as `ENG-022`, tests
  run manually as part of `building`'s self-test and QA's verification; a
  repo-wide harness is its own ticket if the pattern keeps proving worth
  extending.
