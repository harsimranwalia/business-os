---
ticket: ENG-011
project: aiorders-admin-hub
author: architect
created: 2026-08-29
adrs: []
one_way_doors: []
touches_data: true
touches_models: false
---

# Client stage & health visibility on the Brands admin page — technical design

## Approach

Derive `stage` from existing `brands`/`restaurants` columns (`is_active`,
`onboarding_step`) rather than adding a new column — this is what closes the
one-way-door risk the G1 readback flagged (a separately-set "client" field
drifting out of sync with the truth it's meant to reflect). Compute it in
the admin-portal brands-list handler as a derived field on the existing
response, and add a client-side stage filter to `Brands.tsx` following the
exact pattern `statusFilter`/`brandTypeFilter` already use there
(`filteredBrands`, `Brands.tsx:351-364`).

Health reuses the existing hourly `calculate_platform_analytics()` pipeline
(`20260217000001_platform_analytics_cron.sql` — already aggregates
`total_orders`/`total_order_value` per restaurant into Cloudflare KV every
hour) rather than a new query path or job: extend the one function to also
emit `last_order_at`, and read that from the same handler alongside the
brand list.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `aiorders-api`: admin-portal brands-list handler | modify — add derived `stage` and `health` fields to the response | backend |
| `aiorders-api`: `calculate_platform_analytics()` (migration) | modify — add `last_order_at` (`MAX(o.created_at)`) alongside the existing aggregates, same `GROUPING SETS` query | database |
| `aiorders-admin-hub`: `src/pages/Brands.tsx` | modify — display stage + health per row; add `stageFilter` state, same pattern as `statusFilter` (lines ~96, 357) | frontend |

## Data

- **No new table, no new column on `brands` or `restaurants`.**
- `stage` is derived, not stored, from columns that already exist and are
  already written by real flows (`restaurant-claims/index.ts`,
  `restaurant-portal-onboarding/brands.ts`):
  - `is_active = false`, `onboarding_step` below the wizard's final step →
    **Onboarding**
  - `is_active = true` → **Live/Active**
  - `is_active = false`, `onboarding_step` at/above the wizard's final step
    (completed onboarding, since deactivated) → **Inactive/Churned**
  The wizard's own final-step number isn't documented anywhere found in
  this repo — confirm against `restaurant-portal-onboarding/brands.ts`
  before hardcoding it, don't guess.
- `health` is derived at read time from `calculate_platform_analytics()`'s
  per-restaurant aggregate plus the one new `last_order_at` column — no new
  stored field beyond that single added column, same cron cadence (hourly),
  same KV write path already in production.

## Interfaces

Admin-portal brands-list response gains two fields per brand:
- `stage: 'onboarding' | 'live' | 'inactive'`
- `health: 'active' | 'at_risk' | 'inactive' | 'no_data'` — `no_data` is a
  real, expected state (a brand new enough to have no analytics cron cycle
  behind it yet), not an error; must render distinctly from `inactive`.

No new endpoint. Both fields extend the existing brands-list read path and
the existing hourly analytics function's existing output shape.

## Alternatives considered

- **A new `stage` column on `brands`, written by a trigger or app code on
  every relevant event.** Rejected — the G1 readback specifically named the
  drift risk of a second, separately-set field; deriving from `is_active`/
  `onboarding_step` avoids that class of bug entirely, since those columns
  already change atomically with the events that would otherwise need to
  keep a separate `stage` column in sync.
- **A new health-scoring service or scheduled job.** Rejected —
  `calculate_platform_analytics()` already runs hourly with restaurant-level
  order aggregates; adding one column to an existing query is smaller than
  any new pipeline, and reuses infrastructure already proven in production.

## One-way doors

None. No new table, no new vendor, no new datastore — the only schema
change is one additive column in an existing aggregate function's output,
not a change to `orders`/`brands`/`restaurants` themselves. Reuses the
existing admin-portal authorization gate for the negative-case acceptance
criterion. Moves straight through `designed`, no G2.

## Risks

- `calculate_platform_analytics()` runs hourly, so `health` can be up to
  ~1h stale — acceptable for a prioritization signal, not advertised as
  real-time; worth a one-line note in the UI if the exact freshness ever
  becomes a question.
- A brand with zero orders ever (brand new, or never actually processed an
  order through CloudWaitress) has no KV entry for itself — must render as
  an explicit "no data yet" state (`no_data`), never silently coerced into
  `inactive`, which would misrepresent a brand that simply hasn't had the
  chance to order yet.
- The `onboarding_step` "final step" threshold must be confirmed against
  the real wizard step count before being hardcoded, not guessed — flagged
  here so whoever builds this checks rather than assumes.

## Rollout

Straight — every change is additive (new response fields, new UI filter,
one new aggregate column). No flag needed: nothing existing changes shape,
only new fields appear alongside what's already there. Rollback is
reverting the three components; no backfill required, since nothing is
stored net-new beyond the one KV aggregate column, which repopulates itself
on the next hourly cron cycle regardless.

## Out of scope

Support-ticket count (a separate ticket — see `ENG-011`'s own standing
question and its answer). A scored/weighted health model beyond the
active/at-risk/inactive/no-data bucket. Making the `onboarding_step`
final-step threshold configurable.
