# ENG-011 — last_order_at on calculate_platform_analytics()

**Project:** aiorders-api
**Migration file:** `supabase/migrations/20260829190000_add_last_order_at_to_platform_analytics.sql`
**Branch:** `feat/ENG-011-client-stage-health-visibility`

## The numbers

No new table, no new row. This modifies an existing function
(`calculate_platform_analytics()`, `20260217000001_platform_analytics_cron.sql`)
that pg_cron's `platform-analytics-hourly` schedule already invokes every
hour via an HTTP POST to the `platform-analytics` edge function. Nothing
this ticket adds changes the row count read (`orders` LEFT JOIN
`restaurants`, same `GROUPING SETS`) or the write volume (the function's
own bulk KV write, unchanged in shape). Cardinality, growth and
query-frequency are therefore identical to the function's existing,
already-live behavior — this migration adds one aggregate expression
(`MAX(o.created_at)`) to a query that already scans the same rows.

## Design for the query, not the diagram

Same query as before, one more aggregate column. `MAX(o.created_at)`
inside the existing `GROUP BY GROUPING SETS ((), (r.brand_id),
(r.brand_id, o.restaurant_id))` costs nothing extra the query wasn't
already paying for — it's computed in the same aggregation pass as
`COUNT(*)`/`SUM(o.total_amount)`, no second scan, no new join, no new
index. If `orders`/`restaurants` already had an index need for this
query, this ticket doesn't change it either way; sizing that is out of
scope here since the query shape is unchanged.

## A real defect caught before it could fail at apply time

The first version of this migration used `CREATE OR REPLACE FUNCTION` to
add `last_order_at` to `calculate_platform_analytics()`'s `RETURNS TABLE`
column list. **Postgres does not allow `CREATE OR REPLACE FUNCTION` to
change a function's output columns** — the standard failure is `ERROR:
cannot change return type of existing function`, `HINT: Use DROP
FUNCTION calculate_platform_analytics() first`, and a `RETURNS TABLE`
function's column list is exactly the kind of "return type" that rule
covers. Adding a column to this function's output is precisely that
case, so the migration as first written would very likely have failed
the moment it was applied.

No live Postgres was reachable to reproduce the error directly and
confirm it that way — same gap `ENG-007`'s own migration doc named:
Docker Desktop is installed on this host but its daemon does not come up
(`docker info` timed out after 15s; no `psql`, no `supabase` CLI present
either). Rather than ship on an unverified assumption in either
direction, fixed proactively to the pattern that is correct regardless
of which way that specific error resolves: `DROP FUNCTION IF EXISTS
calculate_platform_analytics();` followed by a plain `CREATE FUNCTION`
with the new column list. `DROP ... IF EXISTS` is defensive (idempotent
if this migration is ever re-run against a database where the prior
step already ran); the plain `CREATE` after it always succeeds
regardless of the old function's shape.

**Checked what DROP could break, rather than assuming it's safe just
because it's a common pattern.** Read `20260217000001_platform_analytics_cron.sql`
in full: `cron.schedule('platform-analytics-hourly', '0 * * * *', ...)`
calls `net.http_post` against the `platform-analytics` edge function's
URL — it does **not** call `calculate_platform_analytics()` directly, so
pg_cron holds no reference to the function that a DROP could invalidate.
The only direct callers are the edge function's own `supabase.rpc('calculate_platform_analytics')`
(`platform-analytics/index.ts`, unaffected by a DROP+CREATE inside one
migration transaction — no caller can observe the function missing
mid-deploy) and this migration itself. Grepped the rest of the repo for
any other reference (`grep -rn "calculate_platform_analytics"`): only the
two files above and this migration. No view, no trigger, no other
function depends on it.

## Expand/contract sequence

Single step. `DROP FUNCTION IF EXISTS` + `CREATE FUNCTION` + `GRANT` +
`COMMENT`, all in one migration, all inside one transaction — there is no
data to expand/contract, only a function definition to replace. No
coexistence window: nothing needs the old and new shapes to coexist,
since every caller reads whatever the function currently returns via
`SELECT *`-style destructuring (`row.last_order_at`), not a
positionally-pinned column list.

## Runtime and locks

`DROP FUNCTION` + `CREATE FUNCTION` on a function (not a table) takes
only a brief catalog lock and is near-instant regardless of `orders`
table size — no table rewrite, no table-level lock, no scan performed by
the DDL itself. No online strategy or maintenance window needed.

## Backfill — and the one real transitional gap, named rather than assumed away

No backfill in the traditional sense: the function recomputes fresh on
its next scheduled run (top of the next hour) and overwrites every KV
entry wholesale (`bulkWriteToKV`), so there's no historical row to
migrate. The real transitional question is what `admin-portal/handlers/brands.ts`
sees for the **up to ~1h window between this migration deploying and the
next hourly cron tick**: existing KV entries written by the *old*
function version have no `last_order_at` key at all.

Verified this is handled correctly, not just hoped: `readBrandAnalytics`
returns the parsed KV JSON as `BrandAnalytics`, and `analytics-kv.ts`/
`brands.ts` never assume the key is present — `deriveHealth(analytics?.last_order_at ?? null)`
reads a missing key as `undefined`, and `?? null` folds that into the
same `no_data` path already designed for a brand with no orders ever.
So the transitional window degrades to "every brand reads as `no_data`
for up to an hour after deploy," not a crash, a wrong value, or a
misleading `inactive` — consistent with the design's own requirement
that `no_data` never be conflated with `inactive`.

## Rollback

```sql
DROP FUNCTION IF EXISTS calculate_platform_analytics();

CREATE FUNCTION calculate_platform_analytics()
RETURNS TABLE (
  brand_id uuid,
  restaurant_id uuid,
  total_orders bigint,
  total_order_value numeric
)
LANGUAGE sql
SECURITY DEFINER
AS $$
  SELECT
    r.brand_id::uuid,
    o.restaurant_id::uuid,
    COUNT(*)::bigint as total_orders,
    COALESCE(SUM(o.total_amount), 0)::numeric as total_order_value
  FROM orders o
  LEFT JOIN restaurants r ON o.restaurant_id = r.id
  GROUP BY GROUPING SETS (
    (),
    (r.brand_id),
    (r.brand_id, o.restaurant_id)
  )
$$;

GRANT EXECUTE ON FUNCTION calculate_platform_analytics() TO service_role;
```

Reverts to the exact function body `20260217000001_platform_analytics_cron.sql`
already applied. Should be paired with reverting `platform-analytics/index.ts`
and `admin-portal/handlers/brands.ts` in the same rollback — reading
`row.last_order_at`/`analytics?.last_order_at` off a function that no
longer returns it isn't a crash (both read paths already treat a missing
key as `null`/`no_data`), but rolling back both halves together is
cleaner and is what this repo's convention expects for a paired
handler+migration revert.

## Verification actually performed this pass

No live/staging Postgres reachable (`docker info` timeout, no `psql`, no
`supabase` CLI) — same host limitation `ENG-007`'s migration doc
recorded. What was verified instead:

- **The DROP+CREATE fix itself**, reasoned through above rather than
  merely pattern-matched from habit — checked what depends on the
  function (pg_cron's actual invocation mechanism, every caller in the
  repo) before concluding DROP is safe.
- **SQL syntax read character-by-character** against the original,
  already-applied function body — the only change inside the function is
  one added `SELECT` expression (`MAX(o.created_at) as last_order_at`)
  and one added `RETURNS TABLE` column; the `FROM`/`LEFT JOIN`/`GROUP BY
  GROUPING SETS` clauses are byte-for-byte identical to the version
  already live in this database.
- **`o.created_at` exists and is the right column** — confirmed via
  `platform-analytics/index.ts`'s own fallback query, which already
  selects `orders.created_at` elsewhere in the same file family, and via
  `20250729143357_initial_restaurant_rls.sql` defining `orders` (checked
  the column is a plain `timestamptz`, no default that would make `MAX()`
  behave unexpectedly).

**Not verified, and named rather than assumed:** the migration has not
been applied to any real Postgres instance this pass, so a syntax error
in the exact statement — while believed absent after the above — cannot
be called impossible with the same confidence a live `psql` run would
give. Materially weaker than a container-verified migration; carried
forward to release readiness as the same kind of gap `ENG-007` carried,
not closed here.

## Migration file

`supabase/migrations/20260829190000_add_last_order_at_to_platform_analytics.sql`
in `aiorders-api`, on branch `feat/ENG-011-client-stage-health-visibility`.
Naming and style matched against `20260217000001_platform_analytics_cron.sql`
(the function this migration extends) — same header-comment convention,
same lowercase-keyword SQL style, `DROP ... IF EXISTS` for defensive
idempotency on the one statement it's needed for.

## Addendum — live read-only verification (2026-08-29, later `continue` pass)

The gap named above ("not verified... the migration has not been applied to
any real Postgres instance this pass") is now partially closed, without
spending anything or touching production DDL. This host still has no
Docker/psql/`supabase` CLI (third occurrence of that exact limitation on
this host, after `ENG-007`'s migration doc and this pass's own dead-end
sweep — see `observations.md`/`proposals.md`), but the Supabase MCP
connection available to this session reaches the real `aiorders-api`
project (`bmnmnejwdxbcqinqkwko`) directly, read-only, at zero cost:

- `information_schema.columns` on `orders`: confirms `created_at` is
  `timestamp with time zone`, `NOT NULL` — matches this doc's assumption
  exactly.
- `pg_get_functiondef` on the live `calculate_platform_analytics`: the
  current production function body is byte-for-byte identical to what
  this migration's rollback SQL (above) restores, and to what the "before"
  state section describes — independently confirms both are accurate,
  not just internally consistent with each other.
- `pg_depend` against the function's OID, and `cron.job` for any direct
  command reference: both empty. Confirms nothing in the database catalog
  — no view, no trigger, no pg_cron job — depends on this function
  directly, corroborating the earlier repo-grep finding with a live-catalog
  read instead of a text search.
- `list_migrations` on the same project: `20260829190000_...` is not yet
  applied — production is exactly where this doc assumes it is.

**Deliberately not done, and why:** creating a Supabase branch
(`create_branch`) to actually dry-run the DROP+CREATE statement was
available but requires `confirm_cost` — a real, if small, recurring
charge — and running the statement directly against production, before
this ticket's PR has even been opened for the approver to see, would jump
the L1 human-merge gate entirely. Neither is this pass's call to make
unilaterally; spending the approver's money or writing DDL to a live
business's database ahead of review is exactly the kind of action that
needs a human in the loop first, not a verification shortcut. So the
narrowest honest claim stands: the statement's *safety* (nothing depends
on the function, the target state matches what rollback assumes) is now
independently confirmed against live production catalog data, but the
DROP+CREATE statement itself still has not been executed anywhere. That
residual gap is small and specific, not the open-ended one named above.

## Gate verdict

**pass, with a named verification gap.** No destructive change to any
table, no data loss (the function recomputes wholesale on its own
schedule), rollback written (not live-tested — see above), no
coexistence issue (nothing else calls this function), backfill n/a in
the row sense — the one real transitional behavior (missing
`last_order_at` for up to ~1h post-deploy) was checked against the
actual reading code and confirmed to degrade safely to `no_data` rather
than assumed. The gap is the lack of a live/container-based dry run of
the corrected DROP+CREATE statement, carried forward openly. The defect
this review caught and fixed (`CREATE OR REPLACE` on a changed
`RETURNS TABLE`) is exactly the kind of thing `schema-change`'s own
failure-modes list warns about — reasoned through and fixed here rather
than shipped on the pattern the first draft copied without checking.
