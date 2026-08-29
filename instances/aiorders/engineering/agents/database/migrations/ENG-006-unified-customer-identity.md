# ENG-006 — platform_customers, platform_customer_legacy_links

**Project:** aiorders-api
**Migration file:** `supabase/migrations/20260828120000_platform_customer_identity.sql`
**Branch:** `loyalty-system`

## The numbers

Both tables are brand new — 0 rows today, no prior traffic, because nothing
calls them yet (this ticket is backend-only; the earliest caller is a later,
unscheduled frontend ticket). `schema-change`'s "get the numbers first" step
is largely N/A for that reason, stated rather than silently skipped:

- Current row count: 0 on both tables.
- Growth per month: unknown pre-launch. Bounded by signups × restaurants
  matched per signup — not a number this ticket can estimate honestly.
- Query frequency / read-write ratio: none yet.
- Cardinality driving the two new indexes (`restaurant_id`, `brand_id` on
  the links table): bounded by the number of restaurants/brands in the
  system today (small, tens–low hundreds), not by row count.

The one existing-data fact that matters came from `git log`, not a live
query: `20260221000001_normalize_customer_phone_numbers.sql` already
backfilled every `customers.phone` to the same `+{countrycode}{digits}`
canonical form this ticket matches against (`crm/utils.ts#normalizePhone`'s
algorithm, ported to `plpgsql`). So the phone-equality match in
`platform-customer-auth/index.ts` is comparing like with like without this
ticket doing any of its own backfill work.

## Design for the query, not the diagram

Normalised, not denormalised, with one deliberate exception: `restaurant_id`
and `brand_id` are copied onto `platform_customer_legacy_links` at link time
even though they're derivable by joining `customers`. Every real read this
feature does ("this platform customer's restaurants") wants them directly,
and `customers.restaurant_id`/`brand_id` could in principle change after the
link is made — the link should describe the scope it was made under, not
silently follow if the legacy row's own scope is ever edited later.

## Expand/contract sequence

Single step, no sequencing needed: `add new` only. Both tables are additive;
nothing reads or writes them yet, so there's no `backfill` / `dual-write` /
`switch reads` / `drop old` sequence to plan — those verbs apply to changing
an existing table, and this migration touches none. `customers` is
unmodified.

## Indexes

- `platform_customers.phone` — covered by the table's own `unique` constraint
  (Postgres indexes unique constraints automatically); no separate index
  needed.
- `platform_customer_legacy_links.platform_customer_id` — supports "read a
  platform customer's linked restaurants back" (design AC4).
- `platform_customer_legacy_links.restaurant_id` / `.brand_id` — supports a
  later ticket's admin lookup ("which platform customer is this legacy row
  linked to, from the restaurant side"); cheap now, expensive to add under
  load later. Cardinality is low (see Numbers above), so write-throughput
  cost is negligible.
- `customers.phone` — already exists
  (`idx_customers_phone`, added by `20260221000001_normalize_customer_phone_numbers.sql`);
  this ticket's own lookup (`select ... from customers where phone = :phone`)
  rides that existing index, nothing new needed there.

## Runtime and locks

`CREATE TABLE` on a table that doesn't exist yet takes no lock on anything
else and is effectively instant regardless of database size — there's no
existing data to scan or rewrite. The only statements that touch an existing
object are the two `CREATE INDEX ... ON customers`-shaped queries — except
there are none: the `customers` index already exists (above), so this
migration issues zero `ALTER`/`CREATE INDEX` against any existing table.
Runtime is sub-second; no online strategy or maintenance window needed.

## Backfill

None. Both tables start empty; nothing to backfill. `platform_customer_legacy_links`
fills in gradually, per-user, the first time each diner completes OTP
verification — not a bulk operation this migration or ticket performs.

## Rollback

Written and **tested against a throwaway Postgres container** (see
Verification below), not just asserted:

```sql
drop table public.platform_customer_legacy_links;
drop table public.platform_customers;
```

Order matters — the links table has the FK, so it drops first. Confirmed
clean: `customers` (and its row count) is untouched by either direction.
Reversible without an ADR because nothing else in the codebase reads or
writes either table yet (this ticket is the only caller, and it isn't wired
into any client), so there is no coexistence window to break.

## Verification actually performed this pass

No live/staging Supabase project is reachable from this pass, and spinning
up the full local Supabase stack (`supabase start`) was skipped deliberately
— it would add ~10 containers to the same shared Docker daemon already
running unrelated live work on this machine. Instead: a single throwaway
`postgres:16` container (`--rm`, non-default port, removed immediately after),
with a minimal hand-written stand-in for the two pieces of Supabase's own
managed schema the migration references (`auth.users`, `auth.uid()`) plus a
stub `public.customers`.

Confirmed for real, not assumed:
- The migration applies cleanly end to end (tables, indexes, RLS, all three
  policies).
- `platform_customers.phone` unique constraint rejects a second row with the
  same phone.
- `platform_customer_legacy_links.legacy_customer_id` unique constraint
  rejects a second link to the same legacy row — this is the exact
  constraint `platform-customer-auth/index.ts` leans on for race safety
  (`upsert(..., { onConflict: 'legacy_customer_id', ignoreDuplicates: true })`);
  confirmed the `on conflict ... do nothing` shape no-ops cleanly rather than
  erroring.
- A bogus `legacy_customer_id` is rejected by the FK.
- An out-of-set `matched_via` is rejected by the check constraint.
- Deleting the owning `auth.users` row cascades through `platform_customers`
  and both its link rows — no orphan rows left behind.
- The rollback drops both tables cleanly; `customers`' row count is
  unaffected by either direction.

**Not verified, and named rather than assumed:** behaviour against the real
Supabase project's actual `customers` schema (column types beyond what
`platform-customer-auth`'s design already confirmed by reading the edge
functions that query it — no direct schema inspection was done or attempted
against the live project from this pass), RLS behaviour under a real
`authenticated`/`anon` Supabase role (the stub's `auth.uid()` always returns
`NULL`, so policy *presence* was confirmed but not policy *behavior* under a
real session), and load/performance at any real volume (there is none yet).

## Migration file

`supabase/migrations/20260828120000_platform_customer_identity.sql` in
`aiorders-api`, on branch `loyalty-system`. Naming and style matched against
the two most recent existing migrations in that repo
(`20260821000001_create_api_keys.sql`, `20260821000002_api_keys_allow_blanket_scope.sql`)
rather than the oldest ones — lowercase keywords, `public.`-qualified names,
a header comment naming the consuming code, explicit unique-constraint names,
no `if not exists` (this is a fresh migration, never applied before, not an
idempotent rerun). `create policy` statements omit a `to authenticated`
clause to match this repo's own established convention — checked across
every existing `CREATE POLICY` in this repo's migration history and none use
one; access control is done entirely through `USING (auth.uid() = ...)`.

## Gate verdict

**pass.** No destructive change, no irreversible change, rollback tested,
new-query-pattern indexes present, no coexistence issue (nothing else calls
either table), backfill N/A (nothing to backfill).
