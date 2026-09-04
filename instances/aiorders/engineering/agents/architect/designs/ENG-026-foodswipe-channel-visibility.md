---
ticket: ENG-026
project: restaurant-marketplace
author: architect
created: 2026-09-03
adrs: [ADR-010]
one_way_doors: []
touches_data: true
touches_models: false
---

# FoodSwipe channel-visibility toggles and capability-based discovery — technical design

## Approach

Three new booleans on `restaurants` (`has_order_food` default `true`,
`has_dine_in` default `false`, `has_catering` default `false`) gate which of
FoodSwipe's three already-existing tabs (`order-food`/`dine-in`/`catering` —
`MobileBottomNav.tsx`/`Header.tsx`) a restaurant appears under. Today those
tabs render the *same* restaurant set regardless of which is active — no
restaurant-level gate exists for Dine-In or Catering at all, and Order Food's
only restaurant-level filter is an unrelated `orderingLink`-presence check that
this design leaves untouched. The new flags are an additional `AND` on top of
whatever each tab already filters, not a replacement.

Three things drive this shape rather than the more obvious one.

**The backend for this app no longer lives in this repo.** `restaurant-marketplace`'s
own `supabase/functions/*` was deleted 2026-08-23 ("now owned by aiorders-api" —
`f733e68`); the discovery RPC (`get_restaurants_optimized`) and its handler
(`restaurants.ts`) live in `aiorders-api` today, confirmed directly against
`origin/main`. Every backend change in this design lands in `aiorders-api`,
not here — `restaurant-marketplace` is frontend-only for this ticket. One
loose end this move left behind: the RPC's own defining migration
(`20240302_optimize_restaurant_discovery.sql`) was never ported and still
lives only in `restaurant-marketplace`'s migration history, un-tracked from
`aiorders-api`'s side. This ticket has to touch that function's body anyway
(to add the channel gate), so its `CREATE OR REPLACE` moves into
`aiorders-api`'s own migrations in the same edit — completing ADR-003's
migration-ownership call rather than making a new one. `restaurant-marketplace`'s
copy becomes purely historical; left in place, not deleted (see Risks).

**`has_dine_in` has a naming collision with a real, pre-existing, currently
dead column, and it cannot be resolved by inference alone.** `restaurants`
already carries a `dine_in` boolean, staff-editable today from the exact admin
surface (`aiorders-admin-hub`'s `RestaurantDetails.tsx` "Restaurant Features"
card) requirement 6 names for the new flags — but it is read by nothing on the
consumer/marketplace side (absent from `restaurants_public`, from the
discovery RPC/fallback, from `restaurant-marketplace/types/api.ts`) and absent
from `aiorders-admin-hub`'s own generated Supabase types, which is at least as
consistent with "never a real column, always a dead form field" as with
"real column, stale typegen snapshot." Static repo inspection cannot settle
which, so this design does not guess: see Data, below, for the concrete,
conditional handling this hands to `database`.

**"Open Now" reuses an existing parser instead of building a second
operational-status engine the PRD explicitly defers.** `restaurant-marketplace`'s
`origin/master` already ships `src/utils/openingHours.ts` (`getOpenState`),
wired only into the single-restaurant detail page. This design ports it to
Deno once (`aiorders-api/_shared/openingHours.ts`), evaluates it server-side
after the DB query returns rows, and has both the discovery list and the
detail page read the same computed label — see ADR-010 for why this runs
post-query rather than as a SQL predicate, and what that costs.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `aiorders-api`: `supabase/migrations/20260903130000_add_channel_visibility_to_restaurants.sql` | new — three columns on `public.restaurants` (see Data) | database |
| `aiorders-api`: `supabase/migrations/20260903130001_gate_get_restaurants_optimized_by_channel.sql` | new — `CREATE OR REPLACE FUNCTION get_restaurants_optimized`, porting the existing definition forward from `restaurant-marketplace`'s `20240302_optimize_restaurant_discovery.sql` plus the channel gate and `opening_hours` in `RETURNS TABLE` (see Interfaces) | database |
| `aiorders-api`: `supabase/functions/_shared/openingHours.ts` | new — Deno port of `restaurant-marketplace`'s `src/utils/openingHours.ts` `getOpenState`; single source of truth for "is this restaurant open" server-side | backend |
| `aiorders-api`: `supabase/functions/restaurant-marketplace/handlers/restaurants.ts` | modify — `handleRestaurantDiscovery`: map `mode` → `p_channel` on the RPC call; `handleRestaurantDiscoveryFallback`: add the matching `.eq()` gate and `opening_hours` to `.select()`; both paths: compute a `status` label per row via the new shared util, apply the `open_now` filter post-fetch; `handleRestaurantDetail`: include the three flags in the response (cheap, already an open `select`, not required by any AC but natural) | backend |
| `aiorders-api`: `supabase/functions/admin-portal/handlers/restaurants.ts` | **no change** — `updateRestaurant`'s `.update(updates)` and `getRestaurantById`/`getRestaurants`'s `select('*')` already pass the three new fields through with zero code change. Listed so nobody "adds" a whitelist here as part of this ticket (see Risks/Out of scope — that gap is real but pre-existing and proposed separately) | — |
| `aiorders-admin-hub`: `src/pages/RestaurantDetails.tsx` | modify — extend the local `Restaurant` interface with `has_order_food`, `has_catering`; repoint the existing `dine_in` field/Switch to `has_dine_in` (see Data); add two new Switch rows to the "Restaurant Features" card, matching the six existing rows' exact markup | frontend |
| `aiorders-admin-hub`: `src/integrations/supabase/types.ts` | regenerate via `supabase gen types typescript` after the migration deploys — not hand-edited | — |
| `restaurant-marketplace`: `src/types/index.ts` | modify — add `has_order_food`, `has_dine_in`, `has_catering`, `status?: string \| null` to `RestaurantCard`; `show_in_marketplace` stays server-only, unchanged, no AC needs it client-side | frontend |
| `restaurant-marketplace`: `src/services/api.ts`, `src/hooks/useRestaurants.tsx` | modify — thread a new `openNow` boolean param through to the `open_now` query param | frontend |
| `restaurant-marketplace`: `src/components/restaurants/FilterBar.tsx` | modify — new "Open Now" quick-filter chip (Pattern A style, matching "Offers"/"Rating 4+"), shown for all three modes (today's two quick chips are gated to `order-food`/`dine-in` only — this one is not, see Interfaces) | frontend |
| `restaurant-marketplace`: `src/components/restaurants/RestaurantCard.tsx` | modify — render `restaurant.status` when present, near the card's existing secondary info; no client-side hours parsing added here (server already computed the label) | frontend |
| `restaurant-marketplace`: `src/components/layout/MobileBottomNav.tsx`, `Header.tsx` | **no change** — the three tabs (`order-food`/`dine-in`/`catering`) already exist and already name exactly the three channels this ticket gates | — |

## Data

`touches_data: true`. `database` owns the migration; this states intent and
constraints.

**Three new columns on the existing `public.restaurants` table**, additive
only, following this table's own established convention (`add column if not
exists`, matching `20260807000001_add_heard_about_us_to_catering.sql` and
`ENG-024`'s own `show_in_marketplace` backfill precedent):

| Column | Type | Null | Default | Purpose |
|---|---|---|---|---|
| `has_order_food` | `boolean` | no | `true` | Gates the Order Food tab |
| `has_dine_in` | `boolean` | no | `false` | Gates the Dine-In tab |
| `has_catering` | `boolean` | no | `false` | Gates the Catering tab |

Defaults are the approver's own spec (PRD requirement 1), verbatim.

**Backfill — requirement 7, resolved as far as static analysis permits, one
piece left for `database` to confirm against the live schema:**

- **`has_order_food`**: default `true` for every row *is* the backfill. No
  restaurant-level gate currently restricts the Order Food tab at all (the
  existing `orderingLink` filter is a different, narrower thing — see
  Interfaces), so defaulting every existing row to visible reproduces today's
  behavior exactly. No merchant loses Order Food visibility at rollout.
- **`has_catering`**: backfill from `live_catering`'s existing value in the
  same migration (`UPDATE restaurants SET has_catering = live_catering`).
  `live_catering` is `NOT NULL` on every row today and is already this
  codebase's working stand-in for "does this restaurant do catering"
  (`brand-portal/catering.ts`'s `get_catering_settings` labels it exactly
  that) — a real, populated, already-correct-today signal, not a guess.
  Kept as a **separate** column rather than aliased to `live_catering`
  directly: the PRD's `has_catering` is a staff-controlled *discovery*
  decision, `live_catering` is an *operational capability* flag, and they
  are allowed to diverge later (a restaurant capable of catering but not
  yet ready for FoodSwipe leads) — see Alternatives.
- **`has_dine_in`**: cannot be resolved from the repo alone. Before running
  this migration, `database` must check the live schema
  (`information_schema.columns` or the Supabase dashboard) for a `dine_in`
  boolean on `restaurants`. **If it exists:** backfill
  `has_dine_in` from its value in the same migration, exactly like
  `has_catering` above, and leave the old `dine_in` column in place (not
  dropped this migration — reversibility during rollout; a follow-up
  cleanup ticket can drop it once `aiorders-admin-hub`'s repoint, below,
  has shipped and nothing reads the old name). **If it does not exist:**
  there is genuinely no existing per-restaurant dine-in signal anywhere in
  this schema, and `has_dine_in` starts `false` for every row exactly as
  the approver's own spec defaults it — read as the approver already having
  made this rollout call explicitly (unlike `has_order_food`, they chose
  `false`, not `true`), not as this design defaulting blindly.

**Column comments on all three**, matching this table's own convention.

**No index** — same reasoning as `ENG-016`'s `selections` column: these are
read via the tab's own already-indexed-or-not discovery query, never queried
in isolation.

## Interfaces

### `get_restaurants_optimized` — new `p_channel` parameter

```
p_channel text DEFAULT NULL
```

Added as the RPC's own `WHERE` clause addition:

```
AND (
  p_channel IS NULL
  OR (p_channel = 'order_food' AND has_order_food)
  OR (p_channel = 'dine_in'    AND has_dine_in)
  OR (p_channel = 'catering'   AND has_catering)
)
```

`DEFAULT NULL` plus the `IS NULL` branch means an existing caller that omits
the parameter sees exactly today's unfiltered behavior — backward compatible
by construction, not by promise. `RETURNS TABLE` also gains `opening_hours`
(same type as the column) so the handler can compute a status label without a
second query. An explicit `CASE`-shaped predicate over three named values was
chosen over a dynamic/formatted column reference — see Alternatives.

### `restaurants.ts` — channel mapping and the two gates staying independent

`handleRestaurantDiscovery` maps the existing `mode` param (`'order-food'` →
`'order_food'`, `'dine-in'` → `'dine_in'`, `'catering'` → `'catering'`) to
`p_channel` on the RPC call, and to the matching `.eq()` on the fallback's
`.from('restaurants')` query. **Today's `orderingLink`-presence filter on the
`order-food` mode (`restaurants.ts` / `RestaurantList.tsx:64-65`) is untouched
and stays independent** — it and the new `has_order_food` gate are both `AND`ed
onto the same query; neither replaces the other. This is a deliberate
boundary, not an oversight: conflating "has an ordering-link integration
configured" with "staff wants this restaurant discoverable under Order Food"
risks silently changing which restaurants show up for a reason this ticket's
acceptance criteria never asked for.

**`open_now` — evaluated post-fetch, uniformly for both the RPC and fallback
paths** (ADR-010): for each returned row, `_shared/openingHours.ts` evaluates
`opening_hours` against the current time.

- `isOpen === false` (confirmed closed): when `open_now=true`, the row is
  dropped from the page. Regardless of `open_now`, the row's `status` field
  is set to the parser's own closed-label text (e.g. `"Closed · opens 11 AM"` —
  the utility's real output format, not the PRD Outcome section's more
  elaborate illustrative copy like "Pre-order for tomorrow"; flagged here so
  QA and the PM know the exact string comes from the existing parser, not
  new copy this ticket writes).
- `isOpen === true` or `isOpen === null` (no usable `opening_hours` data):
  **never excluded**, `status` stays `null`. Fail-open is deliberate — a
  restaurant this system cannot evaluate must not disappear just because its
  hours are unknown, which is the same "don't hide" principle requirement 3
  already establishes for confirmed-closed restaurants.

**Detail endpoint** (`handleRestaurantDetail`): unaffected by the channel
gate or `open_now` (a direct `id` lookup, not a list) — gains the three flags
in its response for completeness; its own existing `opening_hours`/
`business_status` fields and the *client-side* `getOpenState` call already
wired into `RestaurantDetail.tsx` (that page's own separate section-tab UI)
are untouched.

### `FilterBar.tsx` — the "Open Now" chip

A new always-visible quick-filter chip, styled like the existing "Offers"/
"Rating 4+" chips (`FilterBar.tsx:186-220`) but **shown for all three modes**
— those two are gated to `order-food`/`dine-in` only (line 187), this one is
not, since Catering restaurants close too. `openNow` is **not** reset when
the active tab changes, unlike `hasOffers`/`rating4Plus`
(`RestaurantList.tsx:112-119`) — a deliberate divergence from that pattern:
"show me who's open right now" is a standing intent about the current moment,
not scoped to one channel, so switching tabs shouldn't silently clear it.
Not persisted to `localStorage`, matching `hasOffers`/`rating4Plus`'s
precedent (time-sensitive filters shouldn't outlive the session).

### `aiorders-admin-hub` — the toggle surface

No new API call: the existing `PUT /admin-portal/restaurants/:id` already
accepts and persists arbitrary keys (Components, above). `RestaurantDetails.tsx`
sends its entire `restaurant` state object on save, so the two new fields and
the repointed `has_dine_in` field are included automatically once added to the
interface and the form — no frontend wiring beyond the interface/JSX change
itself.

## One-way doors

**None.** Checked rather than asserted:

| Criterion | Verdict |
|---|---|
| New datastore | No — three columns on an existing table |
| New vendor | No — nothing new is called; `$0/month` |
| Auth model change | No — the three flags ride the existing `PUT /admin-portal/restaurants/:id` path and its existing (pre-existing, unchanged) access gate |
| Public contract break | No — `p_channel`/`open_now` are additive, `DEFAULT NULL`/off; existing callers see unchanged behavior |
| Data model painful to migrate | No — three nullable-by-default-value booleans (`NOT NULL` with a literal default, no `CHECK`, no enum); reversing is dropping three columns |
| Recurring cost | None |

The closest call is porting `get_restaurants_optimized` into `aiorders-api`'s
migration history. Reversing it costs nothing technically (the function's live
definition is what Postgres executes regardless of which repo's migration
folder wrote it last) — the only thing at stake is which repo's history is
authoritative, and ADR-003 already settled that question for this schema.
Not escalated; not a new decision.

## Alternatives considered

- **Alias `has_catering`/`has_dine_in` directly to `live_catering`/`dine_in`
  instead of adding new columns.** Rejected: the PRD's requirement 1 is an
  approver-authored spec naming exact new field names, not a suggestion to
  reuse; and semantically, "has this operational capability" and "staff wants
  this discoverable on FoodSwipe" are different decisions that happen to
  correlate today. Backfilling `has_catering` *from* `live_catering`'s value
  captures the correlation without permanently coupling the two.
- **A full SQL/PL-pgSQL port of the opening-hours parser for `open_now`,
  evaluated in the RPC's `WHERE` clause.** Rejected — ADR-010.
- **Over-fetch and truncate to mask `open_now`'s pagination shrinkage.**
  Rejected — ADR-010.
- **Dynamic SQL (`format()`-built column reference) for the channel gate**
  instead of an explicit three-way `CASE`-shaped predicate. Rejected: this
  function's existing style is entirely explicit named parameters
  (`p_cuisines`, `p_services`, `p_price_levels`, …); dynamic column references
  are a footgun this codebase doesn't use elsewhere, and three fixed, known
  channels don't need the generality.
- **A single `channel_flags jsonb` column instead of three booleans.**
  Rejected: breaks the simple `.eq(column, true)` filtering every other
  capability flag on this table uses, contradicts the approver's own
  exact-field-name spec, and buys nothing for a fixed set of three.

## Risks

- **The Dine-In tab can go empty, or near-empty, the moment the `aiorders-api`
  deploy lands — before `aiorders-admin-hub`'s toggle UI ships.** Unlike
  `has_catering` (backfilled from a real signal), `has_dine_in` most likely
  starts `false` for every restaurant (pending the live-schema check in
  Data). The instant the channel gate goes live, every restaurant that
  actually does dine-in today disappears from that tab until staff opt each
  one back in. **Mitigation:** deploy `aiorders-admin-hub`'s toggle UI in the
  same window as `aiorders-api`'s gate (Rollout), and treat a bulk staff
  review of known dine-in restaurants right after deploy as part of shipping
  this, not a follow-up. Named explicitly rather than left to be discovered
  as "the Dine-In tab is broken."
- **`dine_in`'s existence is unverified from static repo analysis** (Data).
  Wrong handling here either loses real staff-set data (treating a real
  column as dead) or fails a migration outright (attempting to reference a
  column that was never real) — the conditional check is not optional
  cleanup, it's load-bearing for requirement 7.
- **`has_catering`'s backfill inherits any existing wrongness in
  `live_catering`.** If a restaurant's `live_catering` value is stale or
  wrong today, that wrongness becomes `has_catering`'s starting value too —
  inherited, not created by this ticket.
- **`open_now` pagination is approximate** — ADR-010's accepted consequence.
  A page can under-return relative to `limit`, and `count: 'exact'` can
  overstate what's visible once the filter applies.
- **Two independent implementations of "is this restaurant open" now exist**
  — the new server-side `_shared/openingHours.ts` (this ticket) and
  `RestaurantDetail.tsx`'s own client-side `getOpenState` call (already live
  on `origin/master`, untouched here). Ported from the same source today;
  nothing enforces they stay in sync if either changes later. No shared
  package exists between these repos to close this properly.
- **Restaurants with no usable `opening_hours` are always shown, never
  marked closed** — a deliberate fail-open choice (Interfaces), named so it
  isn't mistaken for a bug when a restaurant with missing hours data never
  gets excluded by "Open Now."
- **`restaurant-marketplace`'s own `20240302_optimize_restaurant_discovery.sql`
  becomes fully historical** once this ticket's `aiorders-api` migration
  ships — not deleted, not this ticket's job to clean up, named so a future
  reader isn't confused about which copy is live.
- **The FoodSwipe-side `catering.ts` endpoints (`handleCateringRequest`,
  `handleGetFilters`) gate only on `approved`, not `show_in_marketplace` and
  not the new `has_catering`.** Pre-existing, not created here, out of scope
  — this PRD's acceptance criteria are about discovery/display, not
  submission. Worth a proposal if it isn't already one; not filed here.
- **`admin-portal/handlers/restaurants.ts`'s `updateRestaurant` has no field
  whitelist at all** — the three new flags ride along on an already-open
  surface (Components). Not new, not created by this ticket, and not the
  same gap as the already-tracked ownership-check issue on this function
  (`proposals.md`, 2026-08-29/2026-09-03-corrected) — that one is about *who*
  can call it, this is about *which fields* a caller can write once
  authorized. Filed separately (see this pass's proposal).

## Rollout

**Phased, gated by existing default values, not a new flag:**

1. **`aiorders-api` migration 1** (columns + backfill). Inert — nothing reads
   the new columns yet.
2. **`aiorders-api` migration 2 + handler changes** (RPC gate, fallback gate,
   `open_now`, status label). **This step alone changes production
   behavior** the moment it deploys: Catering tab narrows to
   `live_catering`-backfilled restaurants (expected, correct), Dine-In tab
   narrows to whatever `has_dine_in` backfilled to — likely near-empty (Risks).
   Coordinate this with step 3, not days apart.
3. **`aiorders-admin-hub`** — toggle UI ships; staff can see and set all
   three flags, including recovering Dine-In visibility per-restaurant.
4. **`restaurant-marketplace`** — "Open Now" chip and status label ship.
   Purely additive; `open_now` defaults off, so this step changes nothing
   for a consumer who never touches the new chip.

**Rollback:** revert each repo's deploy independently. The columns can stay
in place unused if code reverts — no destructive down-migration needed. If
step 1 must also come out, first confirm nothing in a later, independently
deployed change has started reading the columns.

## Out of scope

- **Operational status engine** (kitchen cutoffs, alcohol-license time,
  happy-hour scheduling, `getVenueOperationalStatus`) — PRD non-goal,
  deferred future ticket. "Open Now" here reuses the existing hours parser
  as-is; it does not build the richer engine.
- **Smart dine-in/catering filters** (capacity, amenities, lead time,
  minimum spend) — PRD non-goal, deferred.
- **Promo badge overlay** — PRD non-goal, deferred.
- **Restaurant self-service editing via `restaurant-portal`** — PRD non-goal
  / requirement 6's confirmed default.
- **Per-channel operating hours** — this schema has one `opening_hours` per
  restaurant, not one per channel. "For that channel" in requirements 4/5
  narrows to "for the tab's already-flag-filtered set, using the restaurant's
  one existing hours signal" — there is no per-channel cutoff model to build
  here; that's the deferred operational-status engine's territory.
- **`restaurant-marketplace/handlers/catering.ts`'s own catering-request/
  filters endpoints** — untouched (Risks).
- **`config-site-builder`'s separate public catering-request flow**
  (`ENG-016`'s own feature area) — unrelated; a different meaning of
  "catering" on a different repo, not touched here.
- **`RestaurantDetail.tsx`'s internal section-tabs** (`online-offers`/
  `dine-in-offers`/`catering`/`menu`/`reviews`/`about`) — not gated by the
  new flags; only the marketplace-level discovery tabs are in scope.
- **Fixing `admin-portal/handlers/restaurants.ts`'s missing field
  whitelist or the already-tracked ownership-check gap on `updateBrandOwner`**
  — named in Risks, proposed separately, not fixed here.
