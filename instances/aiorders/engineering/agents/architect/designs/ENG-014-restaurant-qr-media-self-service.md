---
ticket: ENG-014
project: restaurant-portal
author: architect
created: 2026-08-29
adrs: []
one_way_doors: []
touches_data: false
touches_models: false
---

# Brand portal self-service: restaurant QR codes and marketing media downloads — technical design

## Approach

Add one new, restaurant-scoped action to `aiorders-api`'s existing `url-shortener`
function — the function that already owns `shortened_urls` and the QR-generation
logic — rather than touching `brand-portal` or loosening `url-shortener`'s
existing admin-only actions. `url-shortener` today has exactly one auth path
(Bearer JWT → `verifyAdminAccess`, hard `role === 'admin'`) gating every
non-`redirect` action. The new action, `get_or_create_restaurant_qr`, sits on a
second auth path — Bearer JWT → `verifyRestaurantAccess` from
`_shared/restaurantAccess.ts` — inserted between JWT verification and the
existing admin gate. Every existing action (`list`/`create`/`update`/`delete`/
`analytics`/`regenerate_qr`) keeps its current code path and admin gate
untouched.

`_shared/restaurantAccess.ts` already exists for exactly this shape of problem:
its own doc comment says it's "duplicated [from `brand-portal/utils.ts`] because
each edge function deploys independently," and `api-key-auth` already imports it
to add a restaurant-scoped path alongside a function whose other actions are
platform-admin-gated (`README.md` → `api-key-auth`). This ticket is the second
consumer of an established pattern, not a new one.

**Why one action, not "view" and "generate" as two.** AC1 (view existing) and
AC2 (generate if missing) are the same operation from the server's point of
view — find-or-create by `destination_url`, matching what today's *admin* flow
already does client-side (`qrUtils.ts#getRestaurantQR`: list, filter, create if
absent). The new action does that same find-or-create server-side, scoped to
one restaurant, in a single round trip, and returns whether the row was just
created (`created: boolean`) so the UI can tell "already had one" from "just
made one" without extra client logic.

**Why the same action also returns restaurant identity fields.** Rendering the
ported generator components (below) needs `restaurants.website` and
`restaurants.logo_url`, which the portal's own `RestaurantContext` does not
currently fetch (`getUserAccessibleRestaurants` selects a fixed column list
that stops at `cuisine`/`approved`). The action already reads the `restaurants`
row to compute `destination_url` and the row's `name`; returning
`website`/`logo_url` alongside is the same query, not a second one, and avoids
widening the shared `RestaurantContext` fetch (used on every page) just for
this one screen.

**Media downloads (AC3) need no new backend surface at all.** The bag-insert
flyer and A4 poster are client-side canvas/PDF renderers
(`BagInsertGenerator.tsx`, `A4PosterGenerator.tsx`) that take restaurant
identity as props and fetch their own embedded QR. Both already resolve to the
*same* `destination_url` as the "Bag-Insert" QR (`${baseUrl}/links/${restaurantId}`,
no `utm_source` — confirmed by reading both components' QR-fetch code, not
assumed). So `qr_type: 'bag_insert'` serves three UI surfaces (the standalone
Bag-Insert QR button, and the QR embedded in each generator), and `qr_type:
'dine_in'` serves one. No third type exists anywhere in `Activation.tsx`,
matching the PRD's non-goal.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `aiorders-api`: `supabase/functions/url-shortener/index.ts` | modify — new `get_or_create_restaurant_qr` action (restaurant-scoped path, inserted before the existing admin gate); reuses existing `generateShortCode`/`generateQRCode`; no existing action's code or gate changes | backend |
| `aiorders-api`: `supabase/functions/url-shortener/index.ts` | modify — import `verifyRestaurantAccess` from `../_shared/restaurantAccess.ts` (first use by this function; already used by `api-key-auth`) | backend |
| `restaurant-portal`: `src/services/qrMediaApi.ts` (new) | new — thin client for the `url-shortener` function, same `{success, data, error}` wrapper shape as `brandPortalApi.ts#callApi`, but invoking `supabase.functions.invoke('url-shortener', ...)`. Not folded into `BrandPortalApi` itself, which is hardcoded to the `brand-portal` function and used everywhere else in the app — a second, smaller client is less invasive than generalizing a class every other page depends on | frontend |
| `restaurant-portal`: `src/components/qr-media/BagInsertGenerator.tsx` (new, ported from `aiorders-admin-hub`) | new — same component, minus the admin-only `action:'list'`/`action:'create'` auto-load effect, replaced with one `qrMediaApi` call for `qr_type:'bag_insert'` | frontend |
| `restaurant-portal`: `src/components/qr-media/A4PosterGenerator.tsx` (new, ported from `aiorders-admin-hub`) | new — same adaptation as above | frontend |
| `restaurant-portal`: `src/pages/qr-media/Index.tsx` (new) | new — restaurant self-service screen: fetches `qr_type:'dine_in'` and `qr_type:'bag_insert'` for `currentRestaurant.id` (parallel calls) on mount, shows each QR with a download button, renders the two ported generators below for media downloads | frontend |
| `restaurant-portal`: `src/components/layout/Sidebar.tsx` | modify — one new nav entry, same `{icon, label, path}` shape as the existing 13 entries | frontend |
| `restaurant-portal`: `src/App.tsx` | modify — register the new route, same pattern as every existing page | frontend |

## Interfaces

**`url-shortener`, new action `get_or_create_restaurant_qr`** (Bearer JWT
required, same as every non-`redirect` action today):

Request:
```
{ action: 'get_or_create_restaurant_qr', restaurant_id: string, qr_type: 'dine_in' | 'bag_insert' }
```

Success response (200), matching the shape `createUrl`/`updateUrl` already
return elsewhere in this file:
```
{
  success: true,
  data: {
    id, short_code, destination_url, qr_code_url, short_url,
    created: boolean,          // false when an existing row was found and returned
    restaurant: { name, website, logo_url }
  }
}
```

Failure responses, all `{ success: false, error: string }` at HTTP 200 (this
file's existing convention — errors are carried in the body, not the status,
for every action except the two auth checks at the top):
- Caller doesn't manage `restaurant_id` → `error: 'Access denied to this restaurant'`
  (verbatim from `verifyRestaurantAccess`) — this is AC4, the negative case,
  using the same mechanism `api-key-auth` already relies on for the same
  purpose.
- Restaurant has no `website` set → `error: 'Domain not set for this restaurant'`
  — a real, expected state (mirrors the admin flow's own "Domain Not Set" toast
  in `qrUtils.ts`), not a 500. A QR needs a destination; there isn't one to
  encode yet.
- `restaurant_id` missing or `qr_type` not one of the two allowed values →
  `error` naming which. The server enforces the allow-list; it does not trust
  a client-supplied `destination_url` or label the way the admin-only `create`
  action does — this new action computes `destination_url` itself from
  `restaurant_id` + `qr_type`, so a caller can never point it at an arbitrary
  URL or another restaurant's link.

The two unauthenticated/authenticated checks above `get_or_create_restaurant_qr`
in the switch are unchanged: `redirect` stays public, everything else still
requires a valid Bearer JWT before any action-specific logic runs.

## Alternatives considered

- **Widen the existing `list`/`create` actions to accept a restaurant-scoped
  caller.** Rejected — `list` has no restaurant filter at all (returns every
  shortened URL platform-wide); teaching it to scope by caller role risks a
  cross-tenant leak on any future call path that forgets the check, and the
  PRD's own non-goals rule this out directly ("Its `list`/`update`/`delete`/
  analytics actions stay admin-only").
- **Put the new action in `brand-portal` instead**, since that's the function
  `restaurant-portal` already calls for everything else. Rejected — `brand-portal`
  doesn't touch `shortened_urls` today; adding QR generation there means either
  a new `_shared/qrCode.ts` (more moving parts than the alternative) or
  duplicating `generateShortCode`/`generateQRCode` a second time.
  `url-shortener` already owns that logic; extending it in place reuses it
  directly, and `_shared/restaurantAccess.ts` already exists so the function
  doesn't need `brand-portal`'s own access helper to gain restaurant-scoping.
- **Let the ported generator components keep calling `action:'list'` and gate
  the response server-side by role.** Rejected for the same reason as the
  first alternative, and it would change behavior for `admin-hub`'s three
  existing call sites too, which are explicitly out of scope.

## One-way doors

None. No new table, column, vendor, or datastore. The only access-model change
is one additive, tightly-scoped branch on an existing function — precedented by
`api-key-auth`'s identical use of `_shared/restaurantAccess.ts` alongside an
otherwise admin-gated function. Every existing `url-shortener` action, and its
admin gate, is untouched. Moves straight through `designed`, no G2.

## Risks

- **Three pre-existing, independent copies of the "list, filter client-side,
  create if absent" logic** (`qrUtils.ts`, `BagInsertGenerator.tsx`,
  `A4PosterGenerator.tsx`, all in `aiorders-admin-hub`) call `action:'list'`,
  which only admins can reach. When `BagInsertGenerator`/`A4PosterGenerator`
  are ported into `restaurant-portal`, their QR auto-load effect **must** be
  rewritten to call `get_or_create_restaurant_qr` instead — porting the file
  unchanged would 403 for every restaurant-manager user. This is called out
  explicitly in Components above so it isn't lost as an implicit detail during
  build.
- **`_shared/restaurantAccess.ts#verifyRestaurantAccess` returns `{hasAccess,
  error}` rather than throwing.** `brand-portal`'s own copy of this pattern has
  two known-broken call sites — `website.ts` discards the result entirely, and
  `feedback.ts`/`offers.ts` call it with arguments in the wrong order — both
  already tracked in `aiorders-api/supabase/functions/README.md` under "Known
  issues," not new findings from this ticket. The new code in `url-shortener`
  must follow `menus.ts`'s correct usage (`if (!result.hasAccess) return
  {success:false, ...}`), not the nearby broken variants — worth stating since
  this is the exact class of mistake already present twice in this codebase.
- **No migration file defines `shortened_urls`** (same situation the README
  already notes for `order-flow`'s `clover` table) — it was created directly
  against the live project. Whether `destination_url` has a uniqueness
  constraint can't be confirmed by reading this repo. Two near-simultaneous
  calls for the same restaurant + `qr_type` could in theory both miss the
  find step and both insert, producing two rows for one destination. This race
  already exists in today's admin flow (`createUrl` has no application-level
  locking either) — not introduced by this ticket, and not worth a bespoke fix
  here; flagged so it isn't mistaken for a new gap during review.
- **`restaurants.website` can be unset** for a restaurant that hasn't finished
  the admin-side domain setup (`Activation.tsx` step 1). The new action treats
  this as an expected error (`'Domain not set for this restaurant'`), matching
  the admin flow's own guard — a restaurant owner who hits this needs a message
  that says "ask staff to finish domain setup," not a raw failure.
- **QR image provider** (`api.qrserver.com`, free, no stated SLA) is unchanged
  and now reachable one hop further downstream (via a restaurant owner's own
  action instead of only staff's) — inherited risk, already named in the PRD.

## Rollout

Straight — every change is additive (one new backend action, new frontend
files, one new nav entry and route). No flag: nothing existing changes shape,
and the new UI is only reachable from a new sidebar entry no restaurant user
has today. No migration, no backfill — `shortened_urls` and `restaurants` are
used exactly as they already exist. Rollback is reverting the diff.

## Out of scope

- AC5 (marking the restaurant's onboarding-checklist QR step complete
  automatically on self-service generation) — the PRD itself flags this as
  `[proposed]`, mechanism left to this design, and possibly a fast-follow.
  The checklist lives in `admin-portal`'s `restaurant_activations`
  (`activation` actions), a table this design otherwise never touches; doing
  it well raises its own small question this ticket doesn't need to answer
  (does *viewing* an existing QR count as completing the step, or only a
  fresh generation, and what happens if staff already marked it done
  manually?). Bundling that into an already two-repo M ticket is more than
  the acceptance criteria require. Recommend a fast-follow ticket once this
  one verifies, same sequencing pattern the PRD already uses for item 2.
- Item 2 (website settings / hours) — separately sequenced per the PRD, not
  touched here.
- Any QR type beyond `dine_in`/`bag_insert` — matches the PRD's non-goal;
  the new action's `qr_type` is a closed allow-list of exactly these two.
- Any change to `aiorders-admin-hub`'s own components, pages, or QR/media
  flow. The two generators are *ported* (copied and adapted), not moved or
  shared — admin's copies keep working exactly as they do today, including
  their existing `list`-based auto-load effect.
- Fixing the pre-existing `verifyRestaurantAccess` misuse in `brand-portal`'s
  `website.ts`/`feedback.ts`/`offers.ts` (see Risks) — already tracked in
  `README.md`'s "Known issues," a separate cleanup from this feature ticket.
- Widening `url-shortener`'s admin gate on `list`/`update`/`delete`/
  `analytics`/`regenerate_qr` — untouched, matches the PRD's non-goal exactly.
