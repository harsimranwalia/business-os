# ENG-020 — get_acquisition_breakdown(p_restaurant_id, p_from, p_to)

**Project:** aiorders-api
**Migration file:** `supabase/migrations/20260905190000_add_acquisition_breakdown_rpc.sql`
**Branch:** `feat/ENG-020-marketing-roi-attribution-reporting`

## The numbers

No new table, no new column. One new `SECURITY DEFINER` SQL function, read-only,
over `customers` and `orders` — the two tables the brand dashboard's own
`analytics/database.ts` already queries for this restaurant. Zero backfill,
zero rewrite, zero lock beyond the function's own `CREATE OR REPLACE`.

## Verification actually performed this pass

The Supabase CLI is linked on this host now (`supabase link --project-ref
bmnmnejwdxbcqinqkwko`, read-only from here — no `db push`), the same
capability `ENG-037`'s pass first used. `supabase db dump --linked --schema
public` (schema-only, zero cost, zero write) against the live project, not
assumed from the design or from `git grep`:

- **All seven attribution columns the design names exist on `customers`
  exactly as named and typed:** `first_touch_source text`, `first_touch_medium
  text`, `first_touch_campaign text`, `first_referrer text`, `first_touch_at
  timestamptz`, `last_touch_source text`, `last_touch_at timestamptz`. No
  substitute needed, nothing to stop and report.
- **Correction to one load-bearing design assumption:** `orders.customer_id`
  is `uuid NOT NULL` on the live schema (with an enforced
  `orders_customer_id_fkey → customers.id`), not nullable as the design's Data
  section assumed for its "guest order" path. There is no `customer_id IS
  NULL` row this function will ever see. **This does not weaken AC3** — the
  other two paths into `direct_unknown` the design names (an all-null
  attribution tuple; a capture-surface sentinel with no medium/referrer) are
  both independent of this column and fully intact; the guest-order path was
  one of three, not load-bearing on its own. The `LEFT JOIN` from `orders` to
  `customers` is kept regardless — it costs nothing over an `INNER JOIN` here,
  matches the function's documented contract of never dropping an order row,
  and stays correct if that constraint is ever relaxed later.
- **Index presumption on `orders` confirmed:** `idx_orders_analytics_optimized
  (restaurant_id, created_at, total_amount, tip_amount, order_type)` exists
  and covers this function's `orders` filter as a leading-column prefix —
  the same index `analytics/database.ts`'s own RPCs already rely on.
- **Index presumption on `customers` only partially holds — flagged, not
  fixed here, per the design's own instruction.** No `(restaurant_id,
  created_at)` composite exists; what's live is `customers_restaurant_id_idx
  (restaurant_id)` alone (plus `idx_customers_analytics
  (restaurant_id, total_orders, total_spend)`, not useful for a `created_at`
  range). A restaurant-scoped index scan followed by a `created_at` filter is
  adequate at this table's per-restaurant scale (nothing here approaches the
  row counts that would make the missing composite matter), so this migration
  proceeds without it — but the gap is real and named, and the design is
  explicit that an index gap "raises it as a separate ticket rather than
  adding an index inside this one." Filed as a `proposals.md` row rather than
  bundled into this diff.
- **`status <> 'cancelled'` matches the sibling RPCs' own filter exactly**
  (`get_monthly_breakdown`, `get_service_breakdown` — both
  `AND status != 'cancelled'`), confirmed by reading their live definitions in
  the same schema dump, not assumed from the design's citation of
  `analytics/database.ts`'s TypeScript-side `.neq('status', 'cancelled')`.
- **`SECURITY DEFINER` is not a meaningful authorization boundary change
  either way.** The two RPCs this function is closest to in shape
  (`get_monthly_breakdown`, `get_service_breakdown`) are plain `STABLE SQL`
  with no `SECURITY DEFINER` at all — they don't need it because
  `analytics/index.ts` (and `brand-portal/index.ts`) always call as
  `service_role`, which bypasses RLS regardless of the function's own security
  mode. Kept `SECURITY DEFINER` anyway, matching the design's explicit
  instruction and `calculate_platform_analytics()`'s precedent — harmless
  here since the definer role (whoever runs the migration) and the caller
  role (`service_role`) both already have full table access; `p_restaurant_id`
  is the real scoping boundary, enforced in `acquisition.ts` before this
  function is ever called, exactly as the design states.
- **RLS is a non-issue for the same reason `ENG-013`'s doc gave:** every call
  path into this function goes through `brand-portal/index.ts`'s service-role
  client, which bypasses RLS entirely regardless of what policies exist (or
  don't) on `customers`/`orders`. No policy to check or update.
- `list_migrations` on the live project: `20260905190000_...` is not
  present — production is exactly where this doc assumes it is, unapplied.

**Against production: deliberately not done, and why.** The statement has not
been executed against production. Per this same repo's own precedent
(`ENG-013`'s migration doc: "applying DDL directly to production ahead of this
ticket's own PR/review would jump the L1 human-merge gate. Not this pass's
call to make unilaterally") — unchanged here. The design's own Rollout section
already names this as a distinct, first, human/devops-executed step, separate
from and prior to the edge function and portal deploys — not something this
build hop performs inline.

**Against a disposable local replica — done, following `ENG-037`'s
precedent** (this host has docker; `ENG-013`'s "no docker on this host"
excuse no longer applies). Fresh `public.ecr.aws/supabase/postgres:15.8.1.073`
container (same image `ENG-037` used), seeded with a minimal stand-in for the
two live tables this function actually reads (`customers`, `orders`, exact
column names/types from the live dump above) plus two fixture restaurants.
Applied the real migration file unmodified.

**This caught a real bug before it ever reached a PR.** The first version of
the function failed outright: `ERROR: FULL JOIN is only supported with
merge-joinable or hash-joinable join conditions`. A multi-column `IS NOT
DISTINCT FROM` chain (used for null-safe matching across
`first_touch_source`/`first_touch_medium`/`referrer_host`) has no
hash/merge-join strategy in Postgres, full stop — this is not a data-dependent
edge case, it fails on every invocation, with any data, including the
all-empty-tables case. No amount of reading the SQL would have surfaced this
as clearly as running it did. Fixed by coalescing each side to a `chr(1)`
sentinel before comparing (plain, hash-joinable `=`, still null-safe — a
control character cannot appear in a real UTM value or hostname). Migration
file updated in place; re-applied to the same container after the fix.

Against the corrected function, with fixture data covering the cases that
matter most:
- **Two-grain split confirmed with real data, not just read from the SQL:** a
  customer acquired 2026-01-08 (before the test range) who orders once inside
  the range 2026-06-01..2026-09-01 shows `customers_acquired = 0`,
  `orders_count = 1`, `revenue = 100.00` — acquisition doesn't count, the
  order does, exactly the design's stated semantics.
- **`status <> 'cancelled'` confirmed by an actual cancelled row**: a
  customer with one `completed` ($50) and one `cancelled` ($999) order in
  range returns `orders_count = 1`, `revenue = 50.00` — the cancelled $999
  is excluded from the sum, not just from the count.
- **Restaurant scoping confirmed by cross-tenant fixture data**, not by
  reading the `WHERE p_restaurant_id` clause: restaurant A's report contains
  zero rows from restaurant B's `facebook`/$5000 fixture, and restaurant B's
  own report returns exactly its own row and nothing else.
- **All-null tuple confirmed to survive the join and the group-by** — a
  customer with no `first_touch_*`/`first_referrer` set at all appears as its
  own `(NULL, NULL, NULL)` row with its own order correctly attached, not
  merged into a different group and not dropped.
- **A range with zero matching rows returns zero rows**, not an error or a
  null-filled row.
- **`prosecdef = t`** (confirmed `SECURITY DEFINER` took effect) and
  `has_function_privilege('service_role', ..., 'EXECUTE') = t` — the grant is
  live, queried directly rather than assumed from the `GRANT` statement
  executing without error.

## Rollback

```sql
DROP FUNCTION IF EXISTS public.get_acquisition_breakdown(uuid, timestamptz, timestamptz);
```

**Actually run, not just asserted** — against the same disposable container,
after the verification queries above: the drop succeeded and a follow-up
`pg_proc` lookup confirmed zero rows for `get_acquisition_breakdown`. Safe
alone — nothing else references this function until `brand-portal`'s
`acquisition.ts` ships in the same PR, and the RPC-missing branch in that
handler is an explicit, tested case rather than a crash if a rollback of just
this migration is ever needed ahead of the code.

Container removed after the test (`docker rm -f`); nothing left running.

## Gate verdict

**pass.** Additive-only, no table/column change, no backfill, no RLS change,
no new write path. One design assumption (nullable `orders.customer_id`)
was found incorrect against the live schema and corrected in this doc without
changing the function's shape or weakening the acceptance criterion it
supports. One genuine correctness bug (the multi-column `IS NOT DISTINCT
FROM` FULL JOIN, which fails on every invocation) was caught by actually
running the migration against a disposable Postgres replica rather than by
reading the SQL, and fixed before this ticket's first PR. One real index gap
on `customers` is named and routed to
`proposals.md` rather than silently absorbed or silently ignored. The one
open item — the statement has not executed against any live Postgres — is the
same category of residual gap every prior migration on this board has carried
forward, and is smaller in kind than several of them (a pure function
addition, not a table alteration).
