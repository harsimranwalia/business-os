---
ticket: ENG-015
project: aiorders-admin-hub
author: architect
created: 2026-08-31
adrs: [ADR-006]
<!-- merge note: local claimed created 2026-08-29 / adrs: [], remote claimed created 2026-08-31 / adrs: [ADR-006] (more recent), kept remote -->
one_way_doors: []
touches_data: true
touches_models: false
---

# Agency/reseller (partner) users — brand-scoped locations and a working add-location path — technical design

## Approach

Both confirmed defects trace to the same root cause: the `partner-admin`/
`partner-user` roles were added to the top-level `admin-portal` gate
(`index.ts`'s `hasAdminAccess()`) and to the Brands page's own handler, but
never propagated to `restaurants.ts` or to `restaurants`' own RLS. Every
function in `restaurants.ts` that reads or writes a restaurant row
(`getRestaurants`, `getRestaurantById`, `updateRestaurant`) uses the
service-role client unconditionally, with no role branch at all — unlike
`brands.ts`, which at least branches by role even if what it trusts on the
non-admin side (RLS) turns out not to hold up under tracing (see `ADR-006`).

Fix, in one file, one pattern, three call sites: a local `isStaff(profile)`
helper (`role` or `additional_roles` containing `admin`/`sub-admin`) and a
local `getPartnerBrandIds(userId, adminSupabase)` helper (one query:
`brands.select('id').eq('partner_id', userId)`, via the service-role client —
bypasses whatever `brands`' own untracked RLS does or doesn't enforce,
sidestepping that question entirely). Staff keep today's behavior exactly.
Everyone else — by elimination, since the top-level gate already restricts
entry to these four roles — gets their query filtered or their target row's
`brand_id` checked against their own owned-brand set before anything is
returned or written. See `ADR-006` for why this is done in code rather than
by branching to the RLS-scoped client the way `brands.ts` does.

`getRestaurantById` and `updateRestaurant` get the identical treatment,
beyond what the PRD's own Evidence section named — both are reachable today
by a partner via a direct call to `GET`/`PUT
/admin-portal/restaurants/:id`, the same resource and the same missing check,
and AC2 asks for scoping "not just [as] a UI filter." Flagged here explicitly
rather than silently expanded or silently left open: the PRD's Evidence
section names `getRestaurants()` specifically, but its Outcome ("sees and can
add only restaurants under brand(s) assigned to them ... enforced
server-side") reads as covering the resource, not one endpoint on it.

The write-side defect (AC3/4) is fixed at the actual enforcement point:
`AddRestaurantModal.tsx` inserts directly through the ambient RLS-scoped
client, never through this edge function, so the fix is a new RLS `INSERT`
policy, not a handler change. AC5 (held for review, not auto-approved) is
folded into the same policy as a hard `WITH CHECK (approved = false)` rather
than left to the frontend's discretion — cheap (one clause, same policy,
already being added) and it means the "held for review" default the approver
signed off on can't be bypassed by a client that sends `approved: true`
directly. `AddRestaurantModal.tsx` needs one small change regardless: it
hardcodes `approved: true` today, which would make every partner-attempted
insert fail the new `WITH CHECK` outright rather than succeed and land held —
so the modal needs to send `approved: false` for a partner caller for AC3 to
actually work end to end, not only for AC5's default to be honest.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `aiorders-api`: `supabase/functions/admin-portal/handlers/restaurants.ts` | modify — `isStaff`/`getPartnerBrandIds` helpers; brand-scope `getRestaurants`, `getRestaurantById`, `updateRestaurant` | backend |
| `aiorders-api`: `supabase/migrations/20260831120000_partner_restaurant_insert_scoping.sql` | new — one `INSERT` policy: partner role, brand-owned, `approved = false` required | backend |
| `aiorders-admin-hub`: `src/components/AddRestaurantModal.tsx` | modify — read `profile.role` via existing `useAuth()`; send `approved: false` instead of `true` when the caller is `partner-admin`/`partner-user` | frontend |

No change needed to `Restaurants.tsx` (PM's own investigation, re-confirmed
reading the file: it renders whatever the API returns, no role-specific
branching in the render path) or to any route/nav config — partner already
reaches both the Restaurants page and the Brands→Add-Restaurant flow today;
what's missing is only what the backend does with that reach.

## Interfaces

### `restaurants.ts` — new local helpers

```ts
function isStaff(profile: { role: string; additional_roles?: string[] }): boolean {
  const staffRoles = ['admin', 'sub-admin'];
  if (staffRoles.includes(profile.role)) return true;
  return Array.isArray(profile.additional_roles) &&
    profile.additional_roles.some((r: string) => staffRoles.includes(r));
}

async function getPartnerBrandIds(partnerId: string, adminSupabase: any): Promise<string[]> {
  const { data, error } = await adminSupabase
    .from('brands')
    .select('id')
    .eq('partner_id', partnerId);
  if (error) throw error;
  return (data || []).map((b: any) => b.id);
}
```

`isStaff` is framed as "admin-or-sub-admin", never "is a partner" —
deliberately. The top-level gate already restricts every caller reaching this
file to one of four roles; testing the staff side and treating everyone else
as brand-scoped, by elimination, means the branch is correct regardless of
whether a given partner's grant lives in `role` or `additional_roles`, with
no separate "is this a partner" detector to keep in sync with the staff one.

### `getRestaurants(auth)`

Unchanged for staff. For everyone else: resolve `brandIds =
getPartnerBrandIds(auth.user.id, adminSupabase)`; if empty, return
`{success:true, data:[], count:0}` immediately — a partner with no brand
assigned yet is a real, valid state (e.g. before `/partners/:id/assign-brands`
has ever been run for them), not an error. Otherwise add
`.in('brand_id', brandIds)` to the existing query before it runs. Response
shape, joins (`restaurant_website`, `kitchenhub`), and the
`has_ai_website`/`website_deployed`/`ordering_link`/`kitchenhub_status`
mapping are all untouched.

### `getRestaurantById(restaurantId, auth)`

Unchanged fetch. Immediately after it, for non-staff: if
`!restaurant.brand_id || !brandIds.includes(restaurant.brand_id)`, return
`{ error: 'Access denied to this restaurant' }`, 403 — same wording
`_shared/restaurantAccess.ts` already uses for the equivalent check on
`brand-portal`, kept consistent rather than inventing new copy. The existing
`brand_owner` lookup and response shape are otherwise untouched, and run only
after the ownership check passes.

### `updateRestaurant(restaurantId, body, auth)`

Same ownership check, same 403, run before the `adminSupabase.from
('restaurants').update(...)` call. Staff behavior (AC6) unchanged.

### New migration — `INSERT` policy on `restaurants`

```sql
-- Partners (partner-admin/partner-user) may add a restaurant only under a
-- brand assigned to them (brands.partner_id), and only held for staff
-- review (approved = false) — never auto-approved the way staff-created
-- rows are. ENG-015.
CREATE POLICY "Partners can add restaurants to their assigned brands"
ON public.restaurants
FOR INSERT
WITH CHECK (
  approved = false
  AND EXISTS (
    SELECT 1 FROM public.profiles
    WHERE id = auth.uid() AND role IN ('partner-admin', 'partner-user')
  )
  AND EXISTS (
    SELECT 1 FROM public.brands
    WHERE brands.id = restaurants.brand_id AND brands.partner_id = auth.uid()
  )
);
```

Role check is `profiles.role IN (...)` only, deliberately matching the
existing "Admins can manage all restaurants" policy's own strictness
(no `additional_roles`) rather than importing the more defensive check from
`proxy-login`/`restaurantAccess.ts` — consistency with this table's nearest
sibling policy, not a new inconsistency introduced here. Staff inserts are
untouched: they satisfy the pre-existing "Admins can manage all restaurants"
policy and never reach this one.

### `AddRestaurantModal.tsx`

Add `import { useAuth } from '@/contexts/AuthContext';`, read `const { profile
} = useAuth();`, and in `addRestaurantToBrand`'s new-restaurant insert:
`approved: profile?.role === 'partner-admin' || profile?.role ===
'partner-user' ? false : true`. The `update` branch (existing-restaurant
Google-Place connect) is untouched — it never sets `approved`.

## Alternatives considered

- **Branch to the RLS-scoped client for non-staff, mirroring `brands.ts`
  literally.** Traced in `ADR-006` to return zero rows today, not "the
  partner's own brand's rows" — `restaurants`' live SELECT policies grant a
  partner nothing. Would need a new SELECT policy added regardless, at which
  point the code-side filter already gives the same result without depending
  on `brands`' own untracked RLS state.
- **Add a real partner-scoped SELECT policy on `restaurants` as the
  enforcement mechanism, alongside the client branch.** Reasonable
  defense-in-depth, not designed here — AC1/AC2 ask the API to enforce
  scoping, not RLS specifically, and adding it isn't blocked by this design.
- **A `BEFORE INSERT` trigger forcing `approved = false` for a partner caller**,
  instead of a `WITH CHECK` clause. Rejected — one more moving part (a new
  function) for the same guarantee `WITH CHECK` already gives in the same
  policy this ticket is already adding, and this table has no existing
  trigger to extend (the closest precedent, `handle_new_user()`, lives on a
  different table for a different reason).
- **Leave `getRestaurantById`/`updateRestaurant` unfixed**, staying literally
  inside the PRD's own Evidence section. Rejected — see Approach; both are
  reachable today by the same actor this ticket is about, on the same
  resource, and AC2's own wording asks for more than a list-endpoint fix.

## One-way doors

None escalated. Every change here is a reversible code/policy diff with no
existing row touched — a new `INSERT` policy affects only future inserts, and
removing or loosening it later needs no backfill. The one real judgment call
— enforcing brand scope in code rather than trusting RLS the way `brands.ts`
does — is recorded as `ADR-006` for the "why doesn't this just mirror
`brands.ts`" question a future engineer will ask, not escalated to G2. Moves
straight through `designed`, same precedent `ENG-011`/`ENG-013`/`ENG-014` set.

## Risks

- **`brands` has zero RLS policies in tracked migration history** (`ADR-006`)
  — the same untracked-schema-history gap the PRD already names for
  `profiles`/`influencers`, now confirmed for a second table. This design
  doesn't depend on it (everything here uses the service-role client with an
  explicit filter), but it means the Brands page's own partner-scoping is
  unverified from this repo, and worth closing generally — not this ticket's
  problem; not fixed here.
- **Migration and frontend fix must ship together.** If the `INSERT` policy
  lands without the `AddRestaurantModal.tsx` change, every partner add-location
  attempt fails outright (RLS violation) instead of landing held for review —
  still broken, just a different failure mode than today's silent rejection.
  Both are in this one ticket's branch, so this is a sequencing note for the
  build hop, not an open risk.
- **A partner with no brand assigned yet sees an empty Restaurants page,
  indistinguishable in the UI from "no restaurants exist."** Matches the PRD's
  acceptance criteria as written; no AC asks for a distinct empty-state
  message, so none is designed here.
- **Scope note, not a risk:** `getRestaurantById`/`updateRestaurant` are
  in this design despite not being named in the PRD's Evidence section — see
  Approach for the reasoning. Flagged here again so it's visible in the one
  place a reviewer skimming risk/scope is most likely to look.

## Rollout

Straight. The handler change and the new policy are both additive — no
existing action's behavior changes for staff, and no existing row is
touched (the `WITH CHECK` only gates future inserts). No flag needed.
Rollback is reverting the three component changes; nothing here backfills
or unwinds on the data side.

## Out of scope

- **`updateBrandOwner()`** (same file) — unconditional `adminSupabase` use, no
  role or ownership check at all, on `profiles.name/email/phone` for a brand's
  owner contact. Real, but a different resource and a different failure mode
  than anything this PRD's Problem/Outcome/AC describe (this ticket is about
  restaurant visibility and add-location, not brand-owner profile data) — not
  implied by the approved scope, so not fixed here. Filed as a proposal in
  `agents/eng-manager/proposals.md` this same pass (architect-originated
  finding, per `schedules/eng_build_loop.md` step 3) rather than folded in
  silently.
- A defense-in-depth SELECT policy on `restaurants` scoped to brand
  ownership — see Alternatives. Not required by AC1/AC2; may be added later
  without touching anything designed here.
- Dashboard, Influencers, Users pages — per the PRD's own non-goals,
  investigated and confirmed already blocking partner roles outright, not
  leaking.
- Any UI-level "access denied" treatment for a partner navigating directly to
  `RestaurantDetails.tsx` for a restaurant not theirs, beyond whatever generic
  fetch-error handling the page already has. No AC calls for one.

## Prior pass (superseded)

An earlier pass (2026-08-29, titled "Agency/reseller brand-scoped
restaurants") proposed a different enforcement mechanism for the read side:
two additive RLS policies (SELECT + INSERT) on `public.restaurants`, scoped
through `brands.partner_id`, in a single migration
(`20260829230000_partner_restaurant_scoping.sql`), with `getRestaurants()`/
`getRestaurantById()` branching between the service-role client (staff) and
an RLS-scoped `auth.supabase` client (partner roles) — the same
client-selection shape `brands.ts#getAllBrands()` already uses, widened to
cover both `admin` and `sub-admin`. `ADR-006` in the newer pass traces this
approach and finds it would return zero rows for a partner today, since
`restaurants`' live SELECT policies don't currently grant partners anything —
the newer pass's code-side `getPartnerBrandIds` filter avoids depending on
that untracked RLS state entirely. Other points from the earlier pass not
carried forward, kept for reference:

- Its SELECT policy text:
  ```sql
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
  ```
- Its own manual QA verification checklist (Partner A sees only their own
  brand's restaurants; `GET .../restaurants/{Partner B's id}` no longer
  returns Partner B's data; Partner A can add under their own brand landing
  `approved: false`; Partner A is rejected adding under Partner B's brand;
  admin/sub-admin behavior unchanged) — materially the same verification
  surface the newer pass's Rollout/Risks sections still require, just not
  spelled out as a itemized checklist in the newer text.
- Noted the same `updateRestaurant()`/`updateBrandOwner()` unfixed-write
  finding later filed to `agents/eng-manager/proposals.md` in both passes.
- Cited `ENG-022` as the precedent for this shape of gap and fix, same as the
  newer pass.

