---
id: BUG-001
title: Hourly platform-analytics cron POST returns 401 since 2026-08-30T01:00 UTC — Cloudflare KV analytics cache stopped refreshing
project: aiorders-api
severity: P2
status: open
owner: devops
found_by: product-manager
found_in: production
fix_ticket:
created: 2026-08-30
updated: 2026-08-30
---

## Symptom

Every hourly POST to `https://backend.aiorders.io/functions/v1/platform-analytics`
(the `pg_cron` job `platform-analytics-hourly`, schedule `0 * * * *`, project
`bmnmnejwdxbcqinqkwko`) has returned HTTP 401 on every attempt since
**2026-08-30T01:00:00Z** — 7 consecutive hourly failures as of this check
(01:00, 02:00, 03:00, 04:00, 05:00, 06:00, 07:00). The function's own
application log (`function_logs` source) shows no `"Starting analytics
calculation..."` line for any of these attempts — the request is being
rejected before the handler's own code ever runs. Last confirmed successful
run: **2026-08-30T00:00:06Z** (`"Analytics calculated: global=1, brands=49,
restaurants=60"`). Every hourly run on 2026-08-29 (00:00 through 10:00+
checked) returned 200.

## Reproduction

1. Query project `bmnmnejwdxbcqinqkwko`'s unified log stream (Supabase
   `query_logs`), `source = 'function_edge_logs'`,
   `event_message ilike '%platform-analytics%'`, last 24h.
2. Observe: POST requests at each hour boundary return 401 from
   2026-08-30T01:00 UTC onward; the same query for 2026-08-29 shows 200 at
   every hour boundary that day.

Reproduced every time so far (7/7 since onset) — not intermittent.

**Environment:** Supabase project `bmnmnejwdxbcqinqkwko` (`aiorders-api`),
edge function `platform-analytics` (function_id
`3e64d0ae-d630-4d82-a20e-23c6a4189799`, deployment version 13 as of the last
successful run). `origin/main`'s `supabase/functions/platform-analytics/index.ts`
has no `authenticate()` call or any auth check of its own — so the 401 is not
coming from this function's application code, it's coming from a layer in
front of it (Supabase's own edge-function gateway / JWT verification, most
likely). Corroborating data point from the same pass: an unauthenticated
`curl` against a sibling function (`admin-portal/brands`) returned
`{"code":"UNAUTHORIZED_NO_AUTH_HEADER","message":"Missing authorization
header"}` — a response shape that does **not** match `admin-portal`'s own
custom `authenticate()` code (which returns a plain `{"error": "..."}"`, no
`code` field) — consistent with a platform/gateway-level check sitting in
front of these functions, separate from each function's own code, and a
plausible shared cause for both observations.

## Expected

The hourly cron keeps succeeding as it did every hour on 2026-08-29, keeping
the `analytics:brand:*` / `analytics:restaurant:*` / `analytics:global`
Cloudflare KV entries current. This is the same KV cache `ENG-011`'s new
health column on the Brands admin page reads via
`admin-portal/utils/analytics-kv.ts`'s `readBrandAnalytics()`.

## Impact

`ENG-011`'s health signal (and any other consumer of this KV cache — not
fully enumerated this pass) is not being refreshed and grows staler by the
hour. No data loss and no crash: every currently-cached KV value was
correctly computed and written before the outage started (confirmed via a
direct `calculate_platform_analytics()` query returning correct, current
`last_order_at` values for real brands, and via the KV write path's own key
format matching the read path's exactly). Admin-facing only — orders and
checkout are unaffected; the `orders` table is confirmed still receiving new
rows normally throughout this window. Not a defect in `ENG-011`'s own diff:
`platform-analytics/index.ts` and whatever handles its auth were not touched
by that ticket, and the timing (onset 01:00 UTC) sits before that ticket's
own G1-approved merge was even marked `decided` (01:43:13 UTC).

Rated **P2** — degraded experience with an implicit workaround (cached
values remain correct, just aging; nothing crashes or blocks staff from
using the Brands page) — not P1: no core function is broken for a real user
with no workaround, and not P0: production is not down and no data loss is
occurring.

## Evidence

`query_logs` against `bmnmnejwdxbcqinqkwko`, `function_edge_logs` and
`function_logs` sources, window 2026-08-29T00:00Z–2026-08-30T07:16Z. Direct
`calculate_platform_analytics()` SQL check confirming 49 live brand-level
rollup rows with current `last_order_at` values. Live `curl` against
`https://backend.aiorders.io/functions/v1/admin-portal/brands` (no auth
header) → `401 UNAUTHORIZED_NO_AUTH_HEADER`, same pass, 2026-08-30.

## Fix

Filled in by the engineer.

- **Cause:**
- **Change:**
- **Regression test:**
- **Verified by:**
