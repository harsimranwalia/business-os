---
ticket: ENG-020
project: restaurant-portal
author: architect
created: 2026-09-03
adrs: [ADR-011, ADR-012]
one_way_doors: []
touches_data: true
touches_models: false
---

# Marketing ROI reporting — traffic source and revenue attribution on the brand dashboard — technical design

## Approach

A new **"Where customers come from"** page on the brand portal, backed by one
new `brand-portal` action (`get_acquisition_report`) and one new Postgres
aggregate RPC. The RPC groups a restaurant's orders and customers over a date
range by the raw attribution tuple already stored on `customers`; the edge
function's TypeScript layer maps those tuples into named channels and computes
the honesty framing; the page renders it with a preset range selector.

Four findings from reading `origin/main` shaped this rather than the obvious
version.

**The PRD's named extension point cannot satisfy its own acceptance criterion
5.** `analytics/index.ts` reads `restaurantId` straight from the request body,
builds a `SUPABASE_SERVICE_ROLE_KEY` client, and never looks at the
`Authorization` header — no `verifyRestaurantAccess`, no `auth.getUser`, no
role check of any kind. Whatever the Supabase gateway's `verify_jwt` default
gives it proves only that *some* valid project JWT was presented (the portal's
publishable key is in committed source, `src/integrations/supabase/client.ts`);
it scopes nothing to a restaurant. Satisfying AC5 there means adding that
function's first-ever access check — and the standards' *failure direction is
uniform* rule ("when one call path into it is guarded, the adjacent path
carries the same guard") means it could not be added to the new action alone
while `fetchDatabaseAnalytics` stays open. Fixing the whole function is a
security ticket bundled into a feature, which the standards forbid outright.
`brand-portal` already authenticates every caller at the router, already owns
every other owner-facing portal read (customers, orders, offers, menus,
catering, feedback, website, custom reports), and already has the ownership
primitive this needs. The report goes there. See **ADR-011**; the `analytics`
hole is written up in Risks and proposed as its own ticket, not absorbed here.

**The attribution columns the PRD and the ticket Notes name do not all
exist.** No code anywhere writes `utm_source`, `utm_medium` or `utm_campaign`
as columns on `customers`. In all five capture paths those are *request
parameters* that get folded into a `first_touch` / `last_touch` object before
`crm/customers.ts` persists them; the `utm_data` object those same callers
also send is never referenced in `crm/customers.ts` and is dropped on the
floor. What is actually stored is `first_touch_at`, `first_touch_source`,
`first_touch_medium`, `first_touch_campaign`, `first_referrer`,
`last_touch_at`, `last_touch_source`. The channel mapper is written against
that list and no other.

**`first_touch_source` is not a traffic source.** `config-site-builder`'s
`src/utils/userTracking.ts` sets `first_touch_source: existingData?.first_touch_source
|| utmParams.utm_source` — so a visitor arriving without a UTM (which is every
organic-search, direct and most referral visitor) stores `undefined`. The
capture endpoints then backfill it with a **form name**:
`first_touch_source || utm_source || source || "offers-signup"` in
`customer-signup.ts`, `"email-signup"`, `"catering-form"`, `"online-order"`.
So the column is a mix of real UTM sources and surface-name sentinels, and for
the largest real channel — organic search — the only signal is `first_referrer`.
The mapper therefore runs a precedence chain (medium → source → sentinel
detection → referrer host → unknown), not a lookup. That chain is why the
classification stays in TypeScript rather than becoming a SQL `CASE`; see
**ADR-012**.

**The aggregation has to happen in SQL.** The function this ticket was pointed
at already learned this: `database.ts`'s own comments read *"TIER 1: Pure
Database Aggregations (O(1) Performance - No Record Limits!)"*, *"TIER 2:
RPC-based Aggregated Breakdowns (No row limits!)"* and *"TIER 3: Removed"*.
Pulling order rows into the edge function to bucket them there would
re-introduce exactly the tier they deleted, and would trip automatic review
failure #5 (unbounded query). The new RPC returns one row per distinct
`(source, medium, referrer host)` tuple — bounded by attribution cardinality,
not by order count.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `aiorders-api`: `supabase/migrations/{ts}_add_acquisition_breakdown_rpc.sql` | new — `get_acquisition_breakdown(p_restaurant_id, p_from, p_to)`, `SECURITY DEFINER`, `GRANT EXECUTE ... TO service_role`. See Data | database |
| `aiorders-api`: `supabase/functions/brand-portal/acquisition.ts` | new — `handleAcquisition(action, payload, supabase, user)`; ownership check, input validation, RPC call, channel mapping, coverage/precision framing | backend |
| `aiorders-api`: `supabase/functions/brand-portal/channels.ts` | new — pure `classifyChannel(tuple) → ChannelKey`, no I/O, no Supabase import. Separated so it is unit-testable without a DB | backend |
| `aiorders-api`: `supabase/functions/brand-portal/channels.test.ts` | new — Deno tests for the classifier's precedence chain and every sentinel | backend |
| `aiorders-api`: `supabase/functions/brand-portal/acquisition.test.ts` | new — access-denied, malformed range, empty result, guest-order, low-volume-suppression cases | backend |
| `aiorders-api`: `supabase/functions/brand-portal/index.ts` | modify — one new `case 'get_acquisition_report':` routed to `handleAcquisition`, same shape as the existing `get_feedback` line | backend |
| `aiorders-api`: `supabase/functions/README.md` | modify — `brand-portal` entry gains the new action; `DB tables` unchanged (already lists `customers`, `orders`). Required by the repo's own `CLAUDE.md` in the same commit | backend |
| `restaurant-portal`: `src/services/brandPortalApi.ts` | modify — one new `getAcquisitionReport(restaurant_id, from, to)` method on the existing class, matching its siblings | frontend |
| `restaurant-portal`: `src/pages/acquisition/Index.tsx` | new — the report page: range `Select`, channel table, one bar chart, coverage banner, empty state | frontend |
| `restaurant-portal`: `src/components/acquisition/ChannelBreakdown.tsx` | new — the table + `recharts` bar, matching `RevenueChart.tsx`'s existing idiom | frontend |
| `restaurant-portal`: `src/App.tsx` | modify — one new nested route `acquisition` under the existing `DashboardLayout` parent | frontend |
| `restaurant-portal`: `src/components/layout/Sidebar.tsx` | modify — one new entry in the `navItemsAfter` array, above `Reports` | frontend |
| `restaurant-portal`: `src/pages/Dashboard.tsx` | **no change** — listed so nobody bolts this onto the existing dashboard. Its analytics block is hardcoded to the current calendar year (`database.ts` computes `startOfYear`/`endOfYear` itself and takes no range), so a range selector there would control half the page and silently not the other half | — |
| `restaurant-portal`: `src/pages/analytics/Index.tsx`, `src/pages/reports/Index.tsx` | **no change** — PRD non-goal. Neither is reused, extended, or renamed here | — |
| `aiorders-api`: `supabase/functions/analytics/*` | **no change** — see Risks; its missing access check is a real P0-class finding this ticket raises and deliberately does not fix | — |

## Data

`touches_data: true`. `database` owns the migration; this section states intent
and constraints only.

**No new table and no new column.** The only new object is one read-only
aggregate function over data that already exists.

**`get_acquisition_breakdown(p_restaurant_id uuid, p_from timestamptz, p_to timestamptz)`**

Returns one row per distinct attribution tuple, with both grains in a single
result so the handler makes one call:

| Returned column | Meaning |
|---|---|
| `first_touch_source` | raw value off `customers`, `NULL` preserved |
| `first_touch_medium` | raw value off `customers`, `NULL` preserved |
| `referrer_host` | host extracted from `customers.first_referrer` (`split_part(first_referrer, '/', 3)`), `NULL` when the referrer is null |
| `customers_acquired` | count of `customers` rows for this restaurant whose `created_at` is in range and whose tuple this is |
| `orders_count` | count of non-cancelled `orders` for this restaurant whose `created_at` is in range, attributed via `orders.customer_id` |
| `revenue` | `SUM(orders.total_amount)` over the same order set |

Constraints the migration must satisfy:

- **Two grains, two date filters, one result.** `customers_acquired` filters
  `customers.created_at`; `orders_count`/`revenue` filter `orders.created_at`.
  A customer acquired before the range who orders inside it contributes
  revenue to their channel but not to the customer count. That is correct and
  is stated in the UI (see Interfaces) rather than smoothed over.
- **`created_at`, not `first_touch_at`, dates the customer.** `first_touch_at`
  is only written when a `first_touch` object was supplied
  (`crm/customers.ts`), so it is null on an unknown share of rows;
  `created_at` always exists.
- **LEFT JOIN from `orders` to `customers`.** `orders.customer_id` can be null
  (guest orders). Those rows must reach the result with a
  `(NULL, NULL, NULL)` tuple, never be dropped — AC3.
- **`status <> 'cancelled'`** on the order side, matching the existing
  `database.ts` aggregation so the two surfaces do not disagree on revenue.
- **`SECURITY DEFINER`** with `GRANT EXECUTE ... TO service_role`, matching
  `calculate_platform_analytics()` (`20260217000001_platform_analytics_cron.sql`).
  It is never the authorization boundary — `p_restaurant_id` is only ever
  passed a value the handler has already checked (ADR-011).
- **Index check, not an index change.** `orders(restaurant_id, created_at)` and
  `customers(restaurant_id, created_at)` are the access paths. The existing
  `analytics` RPCs already filter on the first, so it is presumed present;
  `database` confirms against the live schema and, if either is missing,
  **raises it as a separate ticket** rather than adding an index inside this
  one.

**The schema cannot be verified from this repo, and the migration must account
for that.** Neither `customers` nor `orders` is created by any tracked
migration — `git grep` over `supabase/migrations/` finds no `CREATE TABLE` or
`ALTER TABLE` for either, and zero mentions of any attribution column. The
three RPCs `analytics/database.ts` calls today (`get_monthly_breakdown`,
`get_service_breakdown`, `count_unique_customers_this_year`) are likewise
absent. This is the same untracked-schema-history gap ADR-006 recorded for
`brands`/`profiles`. So the seven attribution columns are known only from the
code that writes them, not from any DDL. **Before writing the migration,
`database` confirms the exact column names, types and nullability against the
live project (`bmnmnejwdxbcqinqkwko`) — the read-only Supabase MCP already
noted on this board is the cheap way — and if any named column does not
exist, stops and reports rather than guessing a substitute.** A `CREATE
FUNCTION` referencing a missing column fails loudly at migration time, which
is the safe direction, but finding out at deploy is worse than finding out
before.

## Interfaces

### `brand-portal` action `get_acquisition_report`

Request (JSON body, Bearer JWT as every other action):

```
{ "action": "get_acquisition_report",
  "restaurant_id": "<uuid>",
  "from": "2026-06-05T00:00:00.000Z",
  "to":   "2026-09-03T23:59:59.999Z" }
```

`restaurant_id` snake_case, matching the majority convention in this router
(`get_customers`, `get_offers`, `get_catering_requests`); `get_custom_reports`'
camelCase `restaurantId` is the outlier and is not copied.

Success (HTTP 200):

```
{ "success": true,
  "range": { "from": "...", "to": "..." },
  "totals": { "customers": 412, "orders": 1180, "revenue": 48210.55 },
  "coverage": { "attributed_orders": 690, "unattributed_orders": 490,
                "attributed_pct": 58.5 },
  "low_volume": false,
  "channels": [
    { "key": "organic_search", "label": "Organic search",
      "customers": 96, "orders": 240, "revenue": 9880.10 },
    { "key": "direct_unknown", "label": "Direct / not tracked",
      "customers": 210, "orders": 490, "revenue": 19110.00 }
  ] }
```

- `channels` is sorted by `revenue` descending, and **omits any channel with
  zero customers and zero orders** — an always-rendered empty bucket implies a
  channel is being measured when it is not. `direct_unknown` is the one
  exception: always present, even at zero, because AC3 requires it to be
  explicit.
- `low_volume` is `true` when `totals.orders < 30`. The UI shows counts only
  and suppresses percentages when it is set (PRD risk: small-restaurant noise).
- `coverage` is always present and always rendered. It is the honest stand-in
  for "how complete is this."

Failure responses — all HTTP 200 with `{ success: false, error }`, deliberately
matching the `onlineOrders.ts` / `catering.ts` / `menus.ts` / `restaurants.ts`
convention rather than the `customers.ts` / `feedback.ts` / `hiring.ts` /
`website.ts` throw-to-generic-500 convention. Both exist in this directory
today; picking the returning one is a conscious choice, not drift.

| Condition | Response |
|---|---|
| Missing/invalid Bearer JWT | HTTP 401 from `index.ts`, unchanged |
| `x-api-key` presented | HTTP 403 from `index.ts` — the action is not in `API_KEY_ALLOWED_ACTIONS` and must not be added to it |
| `restaurant_id` missing or not a uuid | `{success:false, error:'restaurant_id is required'}` |
| Caller does not own the restaurant | `{success:false, error:'Access denied to this restaurant'}` |
| `from`/`to` unparseable, or `from > to` | `{success:false, error:'Invalid date range'}` |
| Range span > 3 years | `{success:false, error:'Date range too large — choose 3 years or less'}` — rejected, never silently clamped |
| RPC absent (migration not deployed) | `{success:false, error:'Acquisition report is not available yet'}`, `console.error` with the PG code |
| RPC errors otherwise | `{success:false, error:'Failed to build acquisition report'}`, underlying error logged, not returned |

No response field ever carries an individual customer id, name, email, phone,
or a full referrer URL — only counts, sums, and a host string. Aggregates only,
by construction.

### Channel taxonomy

Nine keys, all resolved from `(first_touch_source, first_touch_medium,
referrer_host)`. Precedence runs top to bottom; first match wins.

| Key | Matched by |
|---|---|
| `paid` | medium in `cpc`/`ppc`/`paid`/`paid_social`/`paidsearch`/`display`/`banner`, or source in `google_ads`/`googleads`/`adwords`/`fbads` |
| `email` | medium or source in `email`/`newsletter`/`mailchimp`/`klaviyo` — **not** the `email-signup` sentinel, which is a form name |
| `social` | source or referrer host matching facebook/instagram/tiktok/twitter/x/youtube/linkedin/pinterest/snapchat/threads, or medium `social`/`social_media` |
| `organic_search` | referrer host matching google/bing/duckduckgo/yahoo/ecosia/brave/search, or source one of those with medium `organic` |
| `marketplace` | referrer host or source matching the FoodSwipe marketplace domain |
| `qr` | source or medium containing `qr` |
| `referral` | any other non-empty referrer host |
| `direct_unknown` | everything else: all-null tuple, or a source that is only a capture-surface sentinel (`offers-signup`, `email-signup`, `catering-form`, `online-order`, `online_order`, `manual`, `import`, `dine_in`) with no usable medium and no referrer |
| — | a non-empty source that matches nothing above is kept as its own row keyed `other:<source>`, labelled with the raw value, so an unrecognised real source is visible rather than swallowed into `direct_unknown` |

`qr` and `marketplace` are in the mapper but **nothing populates them today** —
confirmed: `url-shortener`'s `get_or_create_restaurant_qr` (ADR-005/ENG-014)
computes `destination_url` from the restaurant's own `website` column and
appends no UTM, so a QR scan is indistinguishable from a direct visit. They
cost two lines each and become live the moment a link is tagged; they are not
rendered while empty. Named in Out of scope with the follow-on.

### Portal page

`/acquisition`, nav label **"Customer Sources"**. Deliberately neither
"Analytics" nor "Reports": `src/pages/reports/Index.tsx` is the staff-curated
external-link viewer (`get_custom_reports`), and `src/pages/analytics/Index.tsx`
is the mock influencer-campaign page. Range control is a shadcn `Select`
(Last 30 days / Last 90 days / Last 12 months / This year), default **Last 90
days**, resolved to ISO instants client-side — the same `Select` + `useQuery`
idiom `reports/Index.tsx` already uses. No calendar range picker: none exists
in this repo, and no acceptance criterion asks for arbitrary dates.

## Alternatives considered

| Option | Why it lost |
|---|---|
| Extend `analytics` as the PRD's Proposed change names | It has no access check at all, so AC5 could only be met by adding one — either to the new path alone (a half-guarded function, the exact shape the standards' *failure direction is uniform* rule names as a defect) or to the whole function (a security fix bundled into a feature ticket, which "no drive-by refactors" forbids). Its one existing consumer would also have to be re-verified against a newly-enforced gate. ADR-011. |
| Fetch order rows into the edge function and bucket them in TypeScript, avoiding a migration entirely | Unbounded query — automatic review failure #5. And `analytics/database.ts` already deleted its own row-fetching tier for this exact reason, with the comments still in the file. Aggregating in SQL is this function family's own established answer. |
| Push the channel `CASE` into the RPC and return finished buckets | The classification is a five-step precedence chain over an uncontrolled vocabulary that mixes UTM values with form names; every taxonomy change would then be a migration and a deploy. ADR-012, applying ADR-010's precedent. |
| Reuse `platform-analytics` / `calculate_platform_analytics()` (ENG-011's prior art) | Real and cheaper for order totals, but it has no attribution dimension, no date-range parameter, and caches an hourly rollup into Cloudflare KV. It cannot answer "revenue by channel between two dates" at any price. Confirmed by reading the migration, not assumed. |
| Ship as the already-routed `sendPerformanceReport` email (ticket Notes' candidate) | Both `outgoing-communications/actors/brands.ts` report bodies are `// TODO` returning `notificationsSent: 0` — this would mean building the report *and* the email system it was supposed to have. The PRD scopes an in-app view. Left as a genuine follow-on once the numbers are trusted. |
| Add the breakdown to the existing `Dashboard` page | The dashboard's analytics block takes no range — `database.ts` computes the current calendar year internally. A range selector there would drive the new section and silently not the existing one. AC2 is cleaner on its own page. |
| Split AC3's bucket into separate "Direct" and "Unknown" buckets | Tempting, but the data cannot support the split: a row with no source and no referrer is equally consistent with a bookmarked visit and with tracking never having been installed. One honestly-labelled bucket plus the always-visible `coverage` figure says more true things than two buckets that guess. |

## One-way doors

**None.** Each candidate was checked and none qualifies:

- No new datastore, no new vendor, no new dependency.
- No auth model change — the design reuses `verifyRestaurantAccess` exactly as
  `catering.ts` and `menus.ts` already call it.
- No public contract. The new action's only consumer is `restaurant-portal`;
  adding a `case` to the router is additive and breaks nothing.
- No data model to migrate — one read-only `CREATE OR REPLACE`-able function,
  zero rows touched.
- No recurring cost — existing Supabase compute, no new scheduled job.

Both decisions worth recording are reversible and were decided here rather than
escalated: **ADR-011** (which function hosts the report) and **ADR-012** (where
the channel classification runs).

## Risks

**Attribution honesty — AC4, and the PRD's first named risk.** Four concrete
mechanisms, not a disclaimer:
1. The report is **first-touch**, and says so in the page's own subtitle
   ("where each customer first found you"). It is not last-click, so it does
   not have last-click's overstatement.
2. The organic-search row carries fixed copy: *organic reflects the
   restaurant's whole web presence — listings, reviews, site content and its
   AI-generated SEO together — and isolates none of them.*
3. The words "AI SEO" appear nowhere in the report. There is no number on this
   page that claims to be AI SEO's contribution, because none can be.
4. `coverage.attributed_pct` is always rendered. A report that can say "42% of
   your orders could not be attributed" can also say SEO is not working, which
   is the PRD's own test for honesty.

**Cross-domain attribution is incomplete, and more specifically than the PRD
knew.** The two halves of the stitch do not agree on cookie scope. The
standalone `public/tracking/user-tracking.js` writes `user_tracking` with
`domain=.<registrable domain>` (cross-subdomain, per its own `CookieUtil.set`);
the React implementation the restaurant sites actually run
(`config-site-builder/src/utils/userTracking.ts`, called from `Layout.tsx` on
every page) writes the **same cookie name with no `domain` attribute** — host
scoped. Same name, two scopes. Separately, `INSTALLATION.md` shows the
ordering-side install is manual per deployment with a hardcoded `restaurantId`,
so coverage genuinely varies per restaurant and is not determinable from any
repo. **What the design does:** every unattributable order lands in
`direct_unknown` rather than being dropped or guessed, and `coverage` puts the
size of the gap on screen every time the page loads. The cookie-scope mismatch
is a real capture-side bug — filed as a follow-on, not fixed here (this ticket
changes no capture path).

**No historical baseline.** `first_touch_source` only exists from whenever each
path started writing it, and there is no per-restaurant "tracking installed on"
date anywhere to caption a chart with. **What the design does:** the report is
range-scoped only — no all-time total, no pre/post comparison, no trend line
that would read as a causal claim. The coverage percentage is the honest
stand-in for the missing install date, and older ranges will visibly show worse
coverage, which is the truth.

**Small-restaurant noise.** **What the design does:** `low_volume` is set
server-side at `< 30` orders in the range; the UI then renders counts only and
suppresses every percentage, with a plain-language line saying there were too
few orders in the period to show a reliable mix. A single threshold, computed
in one place, testable.

**Tenant isolation — AC5, and this codebase's demonstrated bug class.**
**What the design does:** the handler calls
`verifyRestaurantAccess(restaurant_id, supabase, user)` and branches on
`accessResult.hasAccess`. Two specific traps, both live on `origin/main`:
the signature is `(restaurantId, supabase, user, options?)` — `feedback.ts`
and `offers.ts` pass `(supabase, user.id, restaurant_id)` at 9 call sites, and
`deno check` has been failing on them with `TS2345` unnoticed; and the helper
**returns** an object, it does not throw — `customers.ts` awaits it and
discards the result at 5 call sites, so its check does nothing. `menus.ts`,
`catering.ts`, `restaurants.ts` and `onlineOrders.ts` are the correct models.
**Do not copy `customers.ts`, `offers.ts` or `feedback.ts`.** Automatic review
failure #10 (an authz-gated path with no test on the failure case) has failed
round-1 review three times on this repo, so `acquisition.test.ts` covers the
denied case explicitly.

**ENG-022 is unmerged and renames the helper.** ENG-022 (P0, `blocked`,
PR #9 open on `fix/ENG-022-brand-portal-tenant-isolation`) rewrites six files
in this directory and renames `verifyRestaurantAccessLegacy` →
`requireRestaurantAccess`. **What the design does:** the build hop reads
`brand-portal/utils.ts` at build time to see which names are live and uses
that, exactly as ENG-023's design already instructs for the same collision.
This ticket does not depend on ENG-022 merging — the correct call shape works
before and after — and must not "fix" any of ENG-022's five files in passing.

**Privacy — PIPEDA and Quebec Law 25.** **What the design does:** this ticket
adds no capture, no new cookie, no new field, and no new PII egress. It returns
counts, sums and a referrer *host* — never a customer identifier, never a full
referrer URL. That is a genuine reduction in exposure versus the raw data it
reads. The live question is on the capture side, and it is real:
`config-site-builder`'s `initializeUserTracking()` writes a 365-day
`user_tracking` cookie on every page load with no consent gate anywhere near
it (`clearUserTracking`'s own comment names GDPR, so the concern was known and
not acted on). That is out of this ticket's scope and named as a follow-on
rather than silently inherited.

**`analytics` has no access check — a P0-class finding this ticket raises and
does not fix.** Any caller holding the project's publishable key (committed in
`restaurant-portal/src/integrations/supabase/client.ts`) and a restaurant UUID
can read that restaurant's yearly revenue, order count, tips and customer
totals. Same bug class as ENG-022 and ENG-029. It is not in ENG-020's scope,
and the repo's own `supabase/functions/README.md` does not currently list
`analytics` among the "no auth check at all" functions — so it is invisible to
the one document engineers are told to read first. **Proposed as its own P0
ticket**; ENG-020 must not quietly repair it.

**Order-count and revenue must reconcile with the dashboard.** The new RPC and
`analytics/database.ts` will be compared by the first owner who looks at both.
The design matches its `status <> 'cancelled'` filter and its `total_amount`
sum so a same-period comparison agrees; the customer counts will *not* agree,
because the dashboard's are lifetime/current-year and heuristic
(`returning_customers` is an approximation with a hardcoded 1.5 divisor). The
page therefore never restates a dashboard metric under a different name.

## Rollout

Straight, in three ordered steps, no feature flag — the page does not exist
until its route is added, which is the flag.

1. **Migration first.** `database` applies
   `get_acquisition_breakdown` to `bmnmnejwdxbcqinqkwko`. Read-only, additive,
   affects nothing already running.
2. **Edge function second.** Deploy `brand-portal`. The new action is
   unreachable until the portal ships; every existing action is untouched.
3. **Portal last.** Deploy `restaurant-portal`, which adds the route and the
   nav item together.

If step 3 ships before step 1 or 2 the page renders its error state
("Acquisition report is not available yet") rather than a blank or a crash —
which is why the RPC-missing branch is an explicit case in Interfaces rather
than falling into the generic catch.

**Rollback:** remove the nav entry and route from `restaurant-portal` and
redeploy; the RPC and the unused action are inert and can be dropped later or
left in place.

**Verification.** `restaurant-portal`: `npm run test` (vitest, `src/App.test.tsx`
is the existing smoke suite), `npm run lint`, `npm run build`.
`aiorders-api` has no `package.json`; run Deno from the function's own
directory using the invocation this board already established —
`DENO_NO_PACKAGE_JSON=1 deno test --node-modules-dir=none` and the same
env/flag pair for `deno check`. Ten pre-existing `deno check` errors in
`brand-portal/` are known and out of scope; the new files must add none.

## Out of scope

- **Fixing `analytics`'s missing access check.** Separate P0 ticket, described
  in Risks. Includes adding it to `README.md`'s "no auth check at all" list.
- **The `user_tracking` cookie-scope mismatch** between the standalone script
  and the React implementation. Real capture-side bug, own ticket, would
  improve this report's coverage without changing a line of it.
- **A consent gate before first-party tracking cookies** (PIPEDA / Law 25).
  Capture-side, own ticket, needs a legal answer this department does not have.
- **Tagging QR and marketplace links** so those two channels can populate —
  appending `utm_source=qr` in `url-shortener`'s `get_or_create_restaurant_qr`
  is roughly a one-line change, but it lands in ENG-014's function and belongs
  to whoever owns that surface.
- **Deleting the unreachable mock `src/pages/analytics/Index.tsx`.** It is not
  routed, not imported and not in the sidebar on `origin/main` — dead code, not
  a live honesty problem, and cleanup is its own ticket.
- **Adding an index** if `database` finds `orders(restaurant_id, created_at)`
  missing. Separate ticket; do not bundle.
- Everything the PRD already deferred: Clarity integration, a true ROI ratio,
  isolating AI-SEO from organic traffic, and a staff-facing all-restaurants
  rollup.

## Acceptance criteria — walked

**AC1 — breakdown of customers/orders/revenue by acquisition channel, scoped
strictly to their own restaurant.** Satisfied. The RPC returns all three
measures per attribution tuple; `classifyChannel` maps tuples to the nine
channel keys; `channels[]` carries `customers`/`orders`/`revenue` each.
Scoping is `verifyRestaurantAccess` before the call plus `p_restaurant_id`
inside it. *Note on reading:* AC1's binding text does not enumerate channels —
the "organic/direct/social/referral/paid/QR/marketplace" list lives in the
PRD's Proposed change section. Two of those (`qr`, `marketplace`) cannot be
populated by any data this platform writes today; they exist in the mapper and
render only if something ever tags such a link. Named here rather than
absorbed, so the PM can push back before code.

**AC2 — figures update when the owner changes the time range.** Satisfied.
`from`/`to` are request parameters straight through to the RPC's `p_from`/
`p_to`; the page's `Select` drives a `useQuery` key so a change refetches.
Four presets, default 90 days. No stored state, so no staleness.

**AC3 — a customer with no attribution data shows in an explicit
"unknown/direct" bucket, not dropped or miscounted.** Satisfied, and it is the
one bucket always rendered even at zero. Three distinct paths reach it: a
`(NULL, NULL, NULL)` tuple; a capture-surface sentinel with no medium and no
referrer; and a guest order with `customer_id IS NULL`, which the LEFT JOIN
carries through instead of dropping. `coverage.unattributed_orders` quantifies
it on screen. *Note on reading:* implemented as one bucket labelled "Direct /
not tracked" rather than two, because the data cannot distinguish them — see
Alternatives.

**AC4 — framing makes clear organic/direct reflects overall web presence, not
AI SEO in isolation.** Satisfied by the four mechanisms in Risks: first-touch
labelling, the fixed organic-row copy, the total absence of any "AI SEO"
figure, and the always-visible coverage percentage.

**AC5 — a request for a restaurant the caller doesn't belong to is rejected
server-side.** Satisfied. Router-level Bearer JWT (401 with no token), then
`verifyRestaurantAccess(restaurant_id, supabase, user)` with `.hasAccess`
checked before any query runs, then `x-api-key` callers rejected at 403 by the
existing `API_KEY_ALLOWED_ACTIONS` allow-list. This is ADR-006's pattern —
explicit code-side ownership checking, no reliance on RLS, whose state on these
tables cannot be verified from the repo. Covered by an explicit denied-case
test.

## Failure behaviour

| Situation | Behaviour |
|---|---|
| Restaurant with no customers and no orders in range | RPC returns zero rows; `totals` all zero; `channels` contains only `direct_unknown` at zero; page renders an empty state ("No orders in this period"), not a zeroed chart |
| Restaurant with orders but zero attributed customers | Everything lands in `direct_unknown`; `coverage.attributed_pct` is `0`; the page renders a specific line saying no orders in this period could be traced to a source, and points at tracking coverage |
| Time range with no orders but customers acquired | `orders`/`revenue` zero, `customers` populated; `low_volume` true so percentages are suppressed |
| Fewer than 30 orders in range | `low_volume: true` — counts shown, all percentages suppressed |
| Caller requests another restaurant's data | Denied before any query; nothing about that restaurant, including its existence, is in the response |
| Guest order (`customer_id` null) | Counted in `direct_unknown`, never dropped — the revenue total stays correct |
| RPC not yet deployed | Explicit "not available yet" error, PG code logged; no stack trace or SQL to the client |
| RPC times out or errors | Generic failure message to the client, real error to `console.error`; the page shows a retry, not a partial number |
| Malformed or oversized range | Rejected with a specific message; never silently clamped, so a displayed figure always matches the range the owner picked |
| Concurrent requests | Read-only, no writes, no idempotency key needed — nothing to make idempotent, stated so it is not mistaken for an omission |
| Portal deployed ahead of the API | Page renders the "not available yet" error state; no crash, no blank screen |
