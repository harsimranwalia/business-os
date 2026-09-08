# ENG-048 — loyalty_ledger_entries, orders join-key columns, credit_order_if_eligible, and the auto-complete cron

**Project:** aiorders-api
**Migration file:** `supabase/migrations/20260907130000_loyalty_ledger_schema_and_credit_function.sql`
**Branch:** `feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron`

## Provenance — this migration was found half-built at pass start, not written from a blank file

Before any of the work below, the department worktree (`~/Documents/projects/_eng/aiorders-api`)
was found checked out to `feat/ENG-045-foodswipe-channel-visibility-discovery-handlers` (unrelated,
already merged-to-in-progress ticket) with the migration file already present, complete, and
**untracked** — no branch of its own, no commit, no entry in this ticket's own board-file log, no
plan doc (this file didn't exist yet), `traces/.hops-2026-09-07-ENG-048` already at `2`. Read
plainly: an earlier hop did real work — the file's own inline comments cite a specific captured
order (`cart(99.94) - discount(15) + taxes(4.26) + fees(0.25) = total(89.45)`) and a disposable-
replica rollback test — and then never committed it, never branched correctly, and never recorded
that any of it happened. A second piece of direct evidence, found independently while starting this
pass's own disposable-replica test: an **orphaned Docker container** (`eng048-pgtest`, up since
`2026-09-07T20:54:54Z`) still running with the migration applied and two synthetic test rows
already in `loyalty_ledger_entries` — `amount: 84.94` matches the same captured-order arithmetic
above, `points: 4.2470` at a 5% rate. Consistent with the file's own claims, not contradicting them.

Per `agents/eng-manager/config/projects.md`'s own instruction for exactly this situation
("uncommitted changes in the worktree at the start of a pass means a previous pass died mid-work.
Stop and flag it. Never discard, never stash blindly."): **not discarded.** Verified independently
instead (below — schema shapes re-confirmed against a fresh live dump, full functional behavior
re-proven against a fresh disposable replica this pass, not assumed from the file's own comments),
one real gap fixed (a missing `CONCURRENTLY` on the one index built against a live, non-empty
table — see Runtime and locks), then branched correctly, committed, and documented here. The
orphaned container was removed as routine disposable-test cleanup (matching "container removed
after the test" being the stated norm every prior pass on this board has followed), not treated as
work to preserve — it was a rebuildable test fixture, not a deliverable.

## The numbers

`loyalty_ledger_entries`: zero rows today (zero restaurants carry a configured rate) — provisioning
for a pattern, not a measured load, same framing the design itself uses.

`orders` is not a new table — it is this repo's live, continuously-written webhook target.
Confirmed this pass via `supabase db query --linked` (single aggregate, `pg_class.reltuples` +
`pg_total_relation_size`, no row data read): **~21,905 rows, 140MB.** This number is exactly why
the one index this migration adds to `orders` needed a second look — see Runtime and locks.

## Verification against the live project

Ran read-only against the linked project this pass (`supabase db dump --linked --schema public`
for schema, plus two single-purpose `supabase db query --linked` calls — never a row scan of order/
customer data):

- **Every FK target and column this function reads, re-confirmed from the live dump, not assumed
  from the design or from the inherited file's own comments:** `orders` (`id`, `restaurant_id`,
  `customer_id` not null, `status`, `bill` **jsonb**, `created_at` not null, `total_amount`), no
  pre-existing `cw_order_id`/`loyalty_processed_at` (clean additive, no collision); `customers.id`;
  `platform_customer_legacy_links.platform_customer_id`/`legacy_customer_id` (not null, matches the
  function's own identity-walk query exactly); `platform_customers.id`/`phone`;
  `restaurant_loyalty_configs.restaurant_id`/`online_earn_pct`/`effective_from` (matches the
  function's rate-lookup query exactly). Primary keys confirmed present on all four FK targets
  (`orders_pkey`, `customers_pkey`, `platform_customers_pkey`, `restaurants_pkey`) — the new
  table's FKs will resolve.
- **No existing index anywhere on this project overlaps `(platform_customer_id, restaurant_id)`** —
  confirmed by reading every `CREATE INDEX` in the live dump, not just grepping this repo's tracked
  migrations (which is all the inherited file's own comment had checked). The only two
  `platform_customer_id`/`restaurant_id`-adjacent indexes live are
  `platform_customer_legacy_links_platform_customer_id_idx` (single-column, different table) and
  `restaurant_loyalty_configs_restaurant_id_effective_from_idx` (different column pair, different
  table) — neither makes the new composite index redundant.
- **Vault secret `service_role_key` — confirmed live this pass**, not carried on trust from the
  inherited file's own comment: `supabase db query --linked "select name from vault.secrets where
  name = 'service_role_key'"` returns exactly one row. (For contrast: `ENG-037`'s own pass, four
  days earlier, ran the identical check and found zero rows — someone completed the one-time
  `vault.create_secret(...)` step that pass flagged as an operational prerequisite, sometime
  between then and now.) No secret value read, matching every prior pass's own care here.
- **`bill.cart`/`bill.discount` unit (dollars, not cents) — corroborated, not independently
  re-derived from a fresh payload this pass.** This environment has no query-execution path to real
  order rows (schema dump and narrowly-scoped aggregates only, both read-only by design — pulling
  an actual order's `bill` payload would be exactly the kind of row-level customer-data read every
  prior pass on this board has deliberately avoided). Two independent pieces of static evidence
  both point the same way: (1) `createOrder()` (`external-integrations/handlers/cloudwaitress.ts:205`)
  stores `orderData.bill?.total || 0` — not `bill.total_cents`, despite the `CloudWaitressOrder`
  interface defining both — as this repo's own `total_amount` (dollars) column, so this codebase's
  established convention for *this* payload's bill fields is dollars, not cents; (2) the inherited
  file's own cited example reconciles exactly to the cent across four independent-looking figures
  (`99.94 - 15 = 84.94`, `+ 4.26 = 89.20`, `+ 0.25 = 89.45`) — arithmetic that precise is very hard
  to get by accident from mismatched units. Treated as confirmed for this migration on that basis,
  named honestly as corroboration rather than a fresh live check, since it is the one claim in the
  inherited file this pass could not re-run directly.

## Constraint choice

- **Three cross-field `CHECK` constraints** (`..._order_id_matches_source`,
  `..._reason_matches_source`, `..._created_by_matches_source`) tie `source` to which of
  `order_id`/`fulfillment_reason`/`created_by` may be populated — enforced in the database, not
  only in `ENG-049`'s application code, per this role's own charter ("constraints in the database,
  not only the application"). All three tested directly against both the passing and failing shape
  this pass (below), not just read from the constraint definitions.
- **`loyalty_ledger_entries_order_id_key unique (order_id)`, nullable-safe by construction** —
  Postgres treats every `NULL` as distinct under a plain `UNIQUE` constraint, so `dine_in` rows
  (always `order_id null`) never collide with each other; only two `online_order` rows sharing the
  same real `order_id` would. This is the second, independent guard against ever double-crediting
  one order, alongside `credit_order_if_eligible`'s own `loyalty_processed_at` guard — confirmed
  independently effective this pass with a raw insert that bypasses the function entirely (below).
- **`orders_cw_order_id_key unique (cw_order_id)`, also nullable-safe** — every pre-existing row is
  `null` forever (no backfill), so this constraint costs nothing against them; confirmed this pass
  that two `null` rows coexist and two equal non-`null` values collide, exactly as intended.
- **`points numeric(12,4)`, not positive-only** — deliberately allows a future negative value (a
  human correction, ticket 5 of this sequence) without a schema change then, even though this
  ticket only ever writes positive values. No `CHECK (points > 0)` added for the same reason.
- **RLS enabled, zero policies** on `loyalty_ledger_entries` — same deny-by-default, service-role-
  only choice `ENG-006`/`ENG-007`/`ENG-037` already made on this project, and the design's own
  explicit instruction.

## Runtime and locks

- `create table loyalty_ledger_entries` and its own index/constraints: new, empty table — no lock
  contention possible against data nothing else references yet. Near-instant.
- `alter table orders add column cw_order_id / loyalty_processed_at`: both nullable, no default —
  metadata-only in Postgres, no table rewrite, near-instant regardless of table size.
- `alter table orders add constraint orders_cw_order_id_key unique (cw_order_id)`: takes an
  `ACCESS EXCLUSIVE` lock for its full duration (Postgres has no concurrent path for a single
  `ADD CONSTRAINT ... UNIQUE` statement) — but every existing row is `null` in the column this
  constraint indexes, at `~140MB`/`~21.9k` rows. Not treated as a bare assumption: timed directly
  against a disposable replica seeded to the live row count (below) at **6.6ms**. Accepted as-is
  (single statement, brief, measured) rather than split into the lock-free
  `CREATE UNIQUE INDEX CONCURRENTLY` + `ADD CONSTRAINT ... UNIQUE USING INDEX` two-step form — that
  form is available if a reviewer wants zero read/write blocking at the cost of two statements
  instead of one; naming it here as a reviewable trade-off rather than silently picking one.
- **`create index orders_loyalty_sweep_idx on orders (...)` — this is the one real finding of this
  pass's own diligence, not present in the inherited file.** `orders` is a live, continuously
  written table (~21.9k rows, 140MB, confirmed above), and a plain `CREATE INDEX` takes a `SHARE`
  lock for the full scan-and-build, blocking every concurrent order insert (the webhook's own write
  path) for that window — exactly the "blocking lock on a hot table with no online strategy"
  failure condition this role's own migration gate names explicitly. **Changed to `CREATE INDEX
  CONCURRENTLY IF NOT EXISTS`** (and the rollback's matching `DROP INDEX CONCURRENTLY`). Confirmed,
  not assumed, that this executes correctly under how this file actually runs: `CONCURRENTLY`
  cannot execute inside a transaction block, this file has no explicit `BEGIN`, and a disposable-
  replica run of a minimal `CREATE INDEX CONCURRENTLY ... WHERE ...` statement via plain
  `psql -f` (the same execution shape `supabase db push`'s own migration runner uses — no
  single-transaction-per-file wrapping, matching this repo's own established convention of already
  containing multi-statement, non-atomic migrations) succeeded and produced the index. The full
  amended migration file was then re-run end-to-end (fresh replica) after this edit — applies
  clean, function behavior unchanged, rollback (including the concurrent index drop) clean. One
  residual, named rather than hidden: this confirms the *local* execution model, not a literal
  dry-run against the hosted project's own push path, since applying to the live project is exactly
  the step that stays a human's call (merge, then a manual `supabase db push`/migration deploy,
  same by-hand pattern every prior `aiorders-api` release on this board has used).
- `select cron.schedule(...)`: registers a row in `cron.job`, metadata-only.

## Expand/contract sequence

Additive only, per the design's own Rollout: one new table, two new nullable columns, one new
function, one new cron job. Nothing existing is read or written by any of it until `ENG-049` ships
(the webhook/sweep callers) — no coexistence window, same "inert until the sibling ships" shape
`ENG-031`'s and `ENG-044`'s own releases already used.

## Backfill

None — both new `orders` columns are populated only for orders inserted after this ships (design's
own non-goal), and the new table starts empty.

## Rollback

```sql
select cron.unschedule('loyalty-auto-complete-tick');
drop function if exists public.credit_order_if_eligible(uuid, text);
drop index concurrently if exists public.orders_loyalty_sweep_idx;
alter table public.orders drop constraint if exists orders_cw_order_id_key;
alter table public.orders drop column if exists cw_order_id;
alter table public.orders drop column if exists loyalty_processed_at;
drop table if exists public.loyalty_ledger_entries;
```

**Actually run, twice** — once against the pre-`CONCURRENTLY` version of the file (inherited,
independently re-verified this pass) and once against the final amended version, both on disposable
replicas, both confirmed clean: `cron.unschedule` returns `t`, all statements succeed, zero
`loyalty_ledger_entries`/`orders_loyalty_sweep_idx` relations and zero matching `cron.job` rows
remain afterward, both `cw_order_id`/`loyalty_processed_at` columns confirmed gone from
`information_schema.columns`. Safe any time before `ENG-049` ships (nothing reads or writes any of
this before then); once `ENG-049` ships, rolling back must happen together with reverting its own
changes, same caveat every prior migration plan on this board has recorded for its own
columns/tables.

## Verification actually performed this pass

**Against the live project** — see "Verification against the live project" above (schema dump,
row-count/size aggregate, vault-secret existence check; no row-level order/customer data read).

**Against a disposable local replica** (`supabase/postgres:15.8.1.073`, same image `ENG-037`'s and
`ENG-044`'s own passes used): a minimal stand-in for the six live tables this migration actually
references (`restaurants(id, name)`, `customers(id, restaurant_id)`,
`orders(id, restaurant_id, customer_id, status, bill, total_amount, created_at)`,
`platform_customers`, `platform_customer_legacy_links`, `restaurant_loyalty_configs` — column
shapes taken from the live dump above, not guessed), plus `auth.users` (pre-shipped in the image).

Applied the real migration file unmodified (pre-`CONCURRENTLY` version first) and confirmed by
direct query, not by reading the SQL back:

- Table created, `relrowsecurity = t`; all four indexes present with the exact column/predicate
  lists intended, including the two on `loyalty_ledger_entries` and the one partial index on
  `orders`; `orders_cw_order_id_key` present on `orders`.
- `cron.job` carries `loyalty-auto-complete-tick`, schedule `*/15 * * * *`, `active = t`.
- **`credit_order_if_eligible`, all named branches exercised, each confirmed by querying the actual
  resulting rows, not by reading the function body:**
  - Eligible order (identity + enrolled restaurant, `cart 100 - discount 10` at a 5% rate) →
    `credited`; ledger row `points 4.5000`, `amount 90.00`, `rate_applied 5.00`, correct
    `source`/`fulfillment_reason`; `orders.status → 'completed'`, `loyalty_processed_at` set.
  - Same order, called again with the other `fulfillment_reason` → `already_processed`; ledger
    still exactly one row for that order (idempotent across both callers, per design).
  - Customer with no platform-identity link → `skipped_no_identity`; order still marked processed
    (never re-selected by a future sweep tick); zero ledger rows.
  - Restaurant with no `restaurant_loyalty_configs` row → `skipped_not_enrolled`.
  - Cancelled order → guard blocks before the update; `already_processed`; `status` left untouched
    at `cancelled`; `loyalty_processed_at` **not** set (harmless — the sweep's own claim query
    independently excludes `status = 'cancelled'` too, so this order is never reconsidered by
    either path); zero ledger rows.
  - Invalid `fulfillment_reason` (a value outside `reported`/`window_elapsed`) → raises, confirmed
    by an actual error, not read from the `if` statement.
  - A raw insert duplicating an already-used `order_id`, bypassing the function entirely → rejected
    by `loyalty_ledger_entries_order_id_key` (the second, independent guard, confirmed on its own,
    not merely inferred from the function's own guard working).
  - Dine-in-shaped row (valid: `order_id null`, `fulfillment_reason null`, `created_by` set) →
    succeeds. Dine-in with `order_id` set, and online-order with `created_by` set → both rejected by
    their respective cross-field `CHECK` constraints, confirmed by actual constraint-violation
    errors quoting the failing row.
  - Two orders both `cw_order_id null` → both succeed (nullable-safe unique). Two orders given the
    same non-null `cw_order_id` → second rejected.
- **`CREATE INDEX CONCURRENTLY` under this file's own execution shape (no explicit transaction) —
  confirmed in isolation** on a throwaway table/predicate before touching the real migration, then
  **the full amended file re-applied end to end** on a fresh replica: same table/index/constraint
  checks above, same `credited`/`already_processed` smoke test, same rollback (this time including
  `DROP INDEX CONCURRENTLY`) — all clean, zero drift from the pre-amendment behavior.
- **Rollback executed twice** (pre- and post-amendment), both confirmed clean — see Rollback above.

All containers removed after use, including one **orphaned container left running by the earlier,
uncommitted attempt** (`eng048-pgtest` — see Provenance) — nothing left running at the end of this
pass.

**Deliberately not done:** the cron job was verified to *register* correctly (`cron.job` row
present, correct schedule, `active`); it was not left running long enough to fire, since firing it
would call a `loyalty-auto-complete` URL that doesn't exist yet (`ENG-049`) — a no-op-by-construction
test, matching `ENG-037`'s own identical call on `broadcast-dispatch-tick`.

## Migration file

`supabase/migrations/20260907130000_loyalty_ledger_schema_and_credit_function.sql` in
`aiorders-api`, on branch `feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron`, branched
fresh from `origin/main` tip this pass (the worktree was left mid-checkout on `ENG-045`'s own
already-pushed branch by the earlier, uncommitted attempt — switched away safely, nothing lost,
nothing stashed, matching `ENG-044`'s own remediation for the same class of stale-worktree finding).

## Gate verdict

**pass.** Every FK target and column re-confirmed against a live schema dump rather than trusted
from the inherited file's own comments; the one live-data claim this pass could not directly
re-run (`bill.cart`/`discount` unit) is corroborated by two independent pieces of static evidence
and named as such rather than silently re-asserted as freshly confirmed; every constraint and every
named function branch proven against a disposable replica by direct query, including both
independent double-credit guards; rollback actually executed, twice; and the one real gap this
pass's own diligence found — a plain `CREATE INDEX` against a live, continuously-written 140MB
table with no online strategy — fixed with `CONCURRENTLY`, confirmed executable under this file's
own execution model, and re-verified end to end after the fix.

## Round 2 — review-fail remediation (2026-09-07)

Round 1 (`agents/principal-engineer/notebook/2026-09-07-review-log.md`, `agents/qa/notebook/2026-09-07-coverage-gaps.md`)
failed on two findings. Both fixed this round, and — since this ticket's own discipline throughout
has been "verify, don't trust a fix because it reads correctly" — both re-proven against a fresh
disposable replica of the exact image this project runs (`supabase/postgres:15.8.1.073`), not
accepted on the reviewer's own text.

**B2 (negative `v_amount` on an over-discounted order) — straightforward, fixed as recommended.**
`v_amount := greatest(coalesce((v_order.bill->>'cart')::numeric, 0) - coalesce((v_order.bill->>'discount')::numeric, 0), 0)`.
Re-verified: `cart 20, discount 35` (a `discount > cart` promo) now produces `credited` with
`amount 0.00, points 0.0000` — floored, not negative. Full happy-path/idempotency/skip/cancelled/
invalid-reason matrix re-run on the same replica afterward to confirm no regression from this line
alone: all six outcomes match round 1's own numbers exactly (happy path `amount 90.00, points 4.5000,
rate 5.00`; repeat call `already_processed`, ledger count still 1; `skipped_no_identity`;
`skipped_not_enrolled`; cancelled order `already_processed` with `status` untouched at `cancelled`;
invalid `fulfillment_reason` raises).

**B1 (no `GRANT`/`REVOKE`) — review's own recommended fix text, `revoke ... from public; grant ... to
service_role;`, does NOT actually close the hole on this project. Found by testing the fix rather than
applying it on trust.** Applied review's literal text first, against a fresh replica seeded from this
same migration; `has_function_privilege('anon', ..., 'EXECUTE')` still returned `true` afterward.
Root cause is one layer under "PUBLIC's default is in effect," which is what both the review and the
board-file log said: `pg_default_acl` for this project's `public` schema (queried directly on the
replica, not inferred) carries an explicit default-privileges entry — grantor `postgres`, object type
`f` — granting `EXECUTE` to `anon`, `authenticated`, and `service_role` **by name**, applied
automatically at function-creation time. That is a separate ACL mechanism from the `PUBLIC`
pseudo-grant, and `REVOKE ... FROM PUBLIC` does not touch it. Confirmed with a throwaway function
carrying only `GRANT ... TO service_role` (no revoke at all, the exact shape of this repo's own two
precedent functions) on the same replica: `anon` could still execute it — matching the review's own
live finding on `calculate_platform_analytics`/`get_acquisition_breakdown` byte for byte, and
confirming this replica's default-privileges behavior matches the live project's, not just this local
image's own idiosyncrasy.

Fix applied instead, then verified to actually close it: `revoke execute on function
public.credit_order_if_eligible(uuid, text) from public, anon, authenticated; grant execute on
function public.credit_order_if_eligible(uuid, text) to service_role;` — naming `anon`/`authenticated`
directly. Re-ran `has_function_privilege` for all four roles on the corrected file: `anon` → `false`,
`authenticated` → `false`, `service_role` → `true`, `postgres` → `true` (superuser, expected).

**The systemic proposal this round-1 finding already spawned
(`agents/eng-manager/proposals.md`, 2026-09-07, principal-engineer) recommended the same insufficient
`from public`-only fix for the two precedent functions.** Corrected in place this round rather than
left to mislead whoever picks it up — see that file's own entry.

**Full re-verification after both fixes, fresh replica, end to end:** fixture → migration → grant
check (four roles) → full behavioral matrix above → rollback. Rollback run via `psql -f` (matching
this repo's own no-single-transaction-per-file execution shape, same as every prior verification on
this ticket) rather than `-c` — an earlier attempt through `-c` sent all seven rollback statements as
one implicit multi-statement transaction and errored on `DROP INDEX CONCURRENTLY cannot run inside a
transaction block`, which rolled back the whole batch; this is an artifact of how `-c` batches
statements, not a finding about the migration, and does not recur running the identical statements
from a file. Confirmed clean via `-f`: `cron.unschedule` → `t`, all seven statements succeed, zero
`loyalty_ledger_entries` table, zero `orders_loyalty_sweep_idx` index, zero matching `cron.job` row,
both `orders` columns gone from `information_schema.columns`, function gone from `pg_proc`. Container
removed after use; nothing left running.

**New commit on top of `9fccdad`, not an amend.** `9fccdad` is already pushed to
`origin/feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron` (round 1's own build hop), so
amending it would need a force-push to a shared remote to rewrite already-public history — unlike
round 1's own `CONCURRENTLY` fix, folded in before that commit's first push, which rewrote nothing
anyone else could have already fetched. A second, additive commit avoids that and matches this
project's own established convention of more than one commit per ticket branch (`ENG-045`:
`b647508`/`a9693b6`/`5f35b92`, three commits, merged together via one PR).
