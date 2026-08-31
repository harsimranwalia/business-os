---
ticket: ENG-014
project: restaurant-portal
author: architect
created: 2026-08-31
adrs: [ADR-005]
one_way_doors: []
touches_data: false
touches_models: false
---

# Brand portal self-service — restaurant QR codes and marketing media downloads — technical design

## Approach

Add one new restaurant-scoped action to the `url-shortener` function — the only
place `shortened_urls` and QR generation live — instead of loosening its
existing admin-only gate. Add one new restaurant-scoped read action to the
`brand-portal` function's existing `restaurants.ts` handler to supply the two
fields (`website`, `logo_url`) the media generators need but the portal's own
`RestaurantContext`/`getUserAccessibleRestaurants` don't carry today. Port
`BagInsertGenerator.tsx` and `A4PosterGenerator.tsx` into `restaurant-portal`
as new files — not a shared import, since the four frontends are independent
repos with no shared package — rewiring their QR-fetch step to the new action
instead of each hand-building a destination URL client-side, which is also
where AC4's negative case actually gets enforced (see Interfaces).

This reuses 100% of the existing generation logic and designs (bag insert, A4
poster, `api.qrserver.com`); the only new work is the restaurant-scoped access
path plus the brand-portal UI shell around it — the shape the PRD's own cost
estimate assumed.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `aiorders-api`: `supabase/functions/url-shortener/index.ts` | modify — new action `get_or_create_restaurant_qr`, gated by `verifyRestaurantAccess`, not admin | backend |
| `aiorders-api`: `supabase/functions/brand-portal/restaurants.ts` | modify — new action `get_restaurant_media_info` in `handleRestaurants`, gated by this file's own existing `verifyRestaurantAccess` (`./utils.ts`) | backend |
| `aiorders-api`: `supabase/functions/brand-portal/index.ts` | modify — route `get_restaurant_media_info` to `handleRestaurants`, same pattern as `get_custom_reports` | backend |
| `restaurant-portal`: `src/services/brandPortalApi.ts` | modify — add `getRestaurantMediaInfo()` and `getRestaurantQR()`; the latter invokes the separate `url-shortener` function, not `brand-portal` | frontend |
| `restaurant-portal`: `src/components/qr-media/BagInsertGenerator.tsx` | new — ported from `aiorders-admin-hub`, QR-fetch rewired to `brandPortalApi.getRestaurantQR` | frontend |
| `restaurant-portal`: `src/components/qr-media/A4PosterGenerator.tsx` | new — ported from `aiorders-admin-hub`, same rewiring | frontend |
| `restaurant-portal`: `src/pages/qr-media/Index.tsx` | new — page shell: reads `currentRestaurant` from `RestaurantContext`, fetches media info once, renders dine-in QR download plus both generators | frontend |
| `restaurant-portal`: `src/components/layout/Sidebar.tsx` | modify — one new nav item, next to `Website` | frontend |
| `restaurant-portal`: `src/App.tsx` | modify — one new nested route under the existing `DashboardLayout` parent route | frontend |
| `restaurant-portal`: `package.json` | modify — add `jspdf` (already a direct dependency in `aiorders-admin-hub`; `html2canvas` is loaded via a runtime `<script>` tag in both, not an npm dependency, so it needs no `package.json` change) | frontend |

## Interfaces

### `url-shortener` — new action `get_or_create_restaurant_qr`

Request: `{ action: 'get_or_create_restaurant_qr', restaurant_id: string, qr_type: 'dine_in' | 'bag_insert' }`.

Auth: a valid Bearer JWT is still required (as for every action except
`redirect`), but the blanket `verifyAdminAccess` check running today before
the action `switch` is bypassed for this one action — the same shape as the
existing `redirect` carve-out, just requiring a real authenticated user
instead of none.

Access check: `verifyRestaurantAccess(restaurant_id, supabase, user)` from
`_shared/restaurantAccess.ts` — already duplicated there for exactly this
reason (its own comment: "duplicated here so `api-key-auth` can gate key
issuance without importing across function directories (each edge function
deploys independently)"). 403 `{success:false, error:'Access denied to this
restaurant'}` on failure, before any restaurant row is read for its `website`
— a denied caller never learns whether the restaurant even has one configured.

On access granted: `SELECT name, website FROM restaurants WHERE id =
restaurant_id`. No `website` → 400 `{success:false, error:'Restaurant has no
website configured'}`.

**Destination URL must byte-for-byte match today's three client-side
constructions** (`qrUtils.ts`, `BagInsertGenerator.tsx`,
`A4PosterGenerator.tsx`), or the portal creates a second shortened URL instead
of finding the one staff already generated — and possibly already printed and
handed to the owner:

- `dine_in` → `${baseUrl}/links/${restaurant_id}?utm_source=dine-in`
- `bag_insert` → `${baseUrl}/links/${restaurant_id}` (no query string)

`baseUrl` = `website`, prefixed with `https://` if it has no `http` prefix
already, trailing slash stripped — identical normalization to `qrUtils.ts:20`.

Lookup: a single `.eq('destination_url', destination_url).maybeSingle()`
read — not the existing `listUrls()` helper, which returns every shortened URL
row platform-wide. That's an acceptable shape for the admin-only `list`
action; it would be the wrong thing to reuse internally for a portal-facing
path, even though nothing here exposes the wider list to the caller. Found →
return its `qr_code_url`/`short_code`. Not found → call the existing
`createUrl()` helper as-is (`name: \`${name} (${qr_type === 'dine_in' ?
'Dine-in' : 'Bag-Insert'})\``, `created_by: user.id`).

Response: `{ success: true, data: { qr_code_url, short_code, short_url } }`,
or `{ success:false, error }` with a matching HTTP status (401/403/400/404/
500) — this file's own convention. Every other action (`list`, `create`,
`update`, `delete`, `analytics`, `regenerate_qr`) is untouched, still behind
the blanket admin check, per the PRD's own non-goal.

### `brand-portal` — new action `get_restaurant_media_info`

Request: `{ action: 'get_restaurant_media_info', restaurantId: string }`,
routed in `index.ts` next to `get_custom_reports`.

Access check: `verifyRestaurantAccess(restaurantId, supabase, user)` from this
function's own `./utils.ts` — `restaurants.ts` already imports it for
`getCustomReports`. This is the richer, brand-aware version (accepts a
`brandId` hint); correct here because `brand-portal` is not the
independently-deployed-and-therefore-must-not-cross-import case
`_shared/restaurantAccess.ts` exists for.

Response: `{ success:true, data: { id, name, website, logo_url } }` on access
granted; `{ success:false, error }` (HTTP 200, this function's own established
convention) on denial or not-found.

### `restaurant-portal` frontend

`brandPortalApi.getRestaurantMediaInfo(restaurantId)` — thin wrapper over
`callApi('get_restaurant_media_info', { restaurantId })`.

`brandPortalApi.getRestaurantQR(restaurantId, qrType)` — a sibling method that
calls `supabase.functions.invoke('url-shortener', { body: { action:
'get_or_create_restaurant_qr', restaurant_id: restaurantId, qr_type: qrType
}})` directly rather than through `callApi`, since `callApi` is hardcoded to
the `brand-portal` function. One inline comment at the call site notes why
this method doesn't go through the shared helper, and that its response shape
(real HTTP status codes) differs from every other method on this class
(always-200-with-body).

## Alternatives considered

- **Widen `url-shortener`'s existing `verifyAdminAccess` check itself** to also
  accept a brand/restaurant manager for their own restaurant. Rejected — every
  other action (`list`, `update`, `delete`, `analytics`) would then need its
  own re-scoping to avoid a real cross-tenant leak (`list` alone returns every
  restaurant's shortened-URL rows). Far more surface than this ticket needs,
  and exactly the loosening the PRD's own Risks section warns against.
- **Have `brand-portal` call `url-shortener` server-to-server**, so the
  frontend only ever talks to one function. Rejected — adds a network hop and
  a second service-role client for no real benefit; the frontend already calls
  multiple Supabase functions directly elsewhere, so this isn't a new pattern.
- **Import the two generator components from `aiorders-admin-hub`** instead of
  porting copies. Not available — the four frontends are four independent
  repos (`agents/eng-manager/config/projects.md`) with no shared package.
  Extracting one now would be a real cross-repo refactor, out of proportion to
  an M ticket, and outside acceptance criteria that only govern
  `restaurant-portal`.
- **Accept a client-supplied `destination_url`** on the new action, matching
  what all three existing admin call sites do today. Rejected — this would let
  the restaurant-scoped gate be bypassed by construction: a caller could pass
  any `destination_url` and either read an unrelated existing shortened link
  that happens to match, or mint a new one pointing anywhere, regardless of
  which restaurant they're scoped to. Computing the destination server-side
  from the restaurant's own `website` column is what makes
  `verifyRestaurantAccess` mean something here.

## One-way doors

None escalated. The one judgment call worth recording — narrowing
`url-shortener`'s trust boundary per-action instead of per-function — is
reversible (removable or tightenable without a data migration) and follows an
existing pattern in this codebase (`_shared/restaurantAccess.ts` already
exists for exactly this kind of scoped reuse). Recorded as `ADR-005` for the
"why on earth does `url-shortener` trust a non-admin now" question a future
engineer will ask, not escalated to G2. **Moves straight through `designed`,
no G2** — same precedent `ENG-011`/`ENG-013` set for a reversible,
non-one-way-door design.

## Risks

- **Destination-URL construction must match the existing client-side logic
  byte-for-byte**, or the portal silently creates a second shortened URL
  instead of finding the one staff already generated — and possibly already
  printed and handed to the owner. A one-time porting risk, closed by testing
  against a restaurant that already has a staff-generated QR before this
  ships. Not an ongoing risk: after this ticket, the new action is the only
  place this construction happens for *future* QR codes from either portal.
  `aiorders-admin-hub`'s three existing call sites are untouched (per
  non-goals) and remain a second, independent implementation of the same
  construction — a latent drift risk if the URL scheme ever changes, but
  pre-existing and not created by this ticket.
- **`api.qrserver.com` has no stated SLA** — unchanged, pre-existing risk, now
  also user-facing to owners rather than staff-only. The existing `createUrl()`
  helper already tolerates a failed QR fetch (continues without one, logs, and
  returns) rather than hard-failing the whole shortened-URL row; the new
  action inherits the same degraded behavior with no extra handling needed.
- **Two different error-response conventions on one page** — `brand-portal`
  always returns HTTP 200 with `success` in the body, `url-shortener` uses
  real HTTP status codes. The frontend needs two different error-checking
  shapes for the two new calls; worth a one-line comment at each call site
  rather than a silent trap for whoever debugs this later.
- **Restaurant with no `website` set** — 400 from the new action. The page
  should render this as an actionable message ("ask staff to set your website
  first"), not a blank or broken state, since the portal has no self-service
  way to set `website` itself (that's the deferred item-2 "website settings"
  ticket).

## Rollout

Straight — every backend change is a new, additive action; no existing
action's behavior or gate changes. No flag needed. Rollback is reverting the
component set above; nothing is stored net-new (no migration), so there's
nothing to backfill or unwind on the data side.

## Out of scope

- **AC5** (onboarding-checklist auto-completion) — not designed here.
  `Activation.tsx` step 8's own completion mechanism wasn't read as part of
  this design: this ticket's acceptance criteria don't require it, and the
  PRD itself flags AC5 as `[proposed]`, possibly a fast-follow. A future
  ticket scopes it once someone has actually read that checklist's state
  model.
- Any change to `aiorders-admin-hub`'s own three QR call sites — untouched,
  per the PRD's own non-goals; they keep constructing destination URLs
  client-side exactly as they do today.
- Item 2 (website settings / hours) — separately sequenced, per the PRD.
- Unifying `brand-portal`'s and `url-shortener`'s error-response
  conventions — a pre-existing inconsistency, out of proportion to this
  ticket.
