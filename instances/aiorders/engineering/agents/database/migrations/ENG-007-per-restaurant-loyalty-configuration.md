# ENG-007 — restaurant_loyalty_configs

**Project:** aiorders-api
**Migration file:** `supabase/migrations/20260829130000_restaurant_loyalty_configs.sql`
**Branch:** `loyalty-system`

## The numbers

Brand new table — 0 rows today, nothing calls it yet (this ticket is
backend-only; tickets 3/4 are the earliest real callers, and even they are
unscheduled). Per `schema-change`'s own step 2, stated rather than silently
skipped:

- Current row count: 0.
- Growth per month: bounded by `restaurants` count × rate changes per
  restaurant, both small — tens to low hundreds of restaurants today, and a
  rate change is a deliberate admin action, not a per-order event. Not a
  number this ticket can size precisely pre-launch, same position ENG-006
  was in for its own two tables.
- Query frequency / read-write ratio: none yet — no live caller.
- Cardinality driving the new index (`restaurant_id`, `effective_from`):
  bounded by the number of restaurants (small) × rate changes per restaurant
  (expected to be rare — an admin action, not routine), not by unbounded
  row growth.

## Design for the query, not the diagram

Normalised: one row per rate change, no denormalisation. The only query this
ticket or tickets 3/4 will ever run against this table is "the latest row
for restaurant X with `effective_from <= T`" — the index is built for
exactly that access pattern (`restaurant_id, effective_from desc`) and
nothing else is optimized for, because nothing else is asked of this table.

Open-ended effective-dating (no `effective_to`) rather than closed ranges —
see Alternatives in
`agents/architect/designs/ENG-007-per-restaurant-loyalty-configuration.md`
for why a closed range was rejected (it would require updating the prior
row on every insert, breaking the insert-only property PRD requirement 6
asks for, and reopening the same race two statements instead of one).

## Expand/contract sequence

Single step, `add new` only — same shape as ENG-006. The table, its index,
and both trigger functions are additive; nothing reads or writes this table
yet, so there is no `backfill` / `dual-write` / `switch reads` / `drop old`
sequence to plan. `restaurants` and every other existing table are
untouched.

## Indexes

- `restaurant_loyalty_configs_restaurant_id_effective_from_idx` on
  `(restaurant_id, effective_from desc)` — supports the one access pattern
  this table has (see above). No other index is needed: there is no
  admin-facing search/filter/sort over this table beyond "history for one
  restaurant," and the GET handler's history query rides this same index
  (`eq('restaurant_id', ...).order('effective_from', { ascending: false })`).

## Runtime and locks

`CREATE TABLE` on a table that doesn't exist yet takes no lock on any
existing object and is effectively instant regardless of database size —
there is no existing data to scan or rewrite, and this migration issues no
`ALTER`/`CREATE INDEX` against any existing table. Runtime is sub-second; no
online strategy or maintenance window needed.

## Backfill

None. The table starts empty. Real restaurant rates get entered one at a
time through the admin write path as restaurants are onboarded to the
loyalty program — not a bulk operation this migration performs, and
deciding actual $/% numbers for any real restaurant is explicitly out of
this ticket's scope (PRD non-goal).

## Rollback

```sql
drop trigger restaurant_loyalty_configs_enforce_order on public.restaurant_loyalty_configs;
drop trigger restaurant_loyalty_configs_updated_at on public.restaurant_loyalty_configs;
drop function public.enforce_loyalty_config_effective_order();
drop function public.update_restaurant_loyalty_configs_updated_at();
drop table public.restaurant_loyalty_configs;
```

Order matters — triggers drop before the functions they call, both drop
before the table, so nothing references a dropped object mid-sequence.
Reversible without an ADR: no other code in this diff or in the wider repo
reads or writes this table (it has no caller — the new `admin-portal` route
is this ticket's only writer, and nothing calls that route from any
frontend, per the PRD's own non-goals), so there is no coexistence window a
rollback would break.

## Verification actually performed this pass

No live/staging Supabase project is reachable from this pass. Docker
Desktop is installed on this Windows host but its daemon was not running;
it was launched this pass and polled for readiness for roughly 170s (two
bounded waits) without the engine coming up in time to be usable within
this pass's budget — recorded honestly rather than spending further budget
polling indefinitely or silently skipping verification. `npm install -g
deno` was attempted as a fallback real-verification path once Docker proved
unavailable; its outcome is recorded in
`agents/principal-engineer/reviews/ENG-007.md` and this ticket's own log
alongside whatever it produced.

**What was verified instead, and how:**

- **Hand-traced the trigger's transaction semantics against a concrete
  sequence**, rather than only reading the SQL for shape:
  - First insert for a restaurant (`current_max` is `null`): the "must be
    later than current latest" branch short-circuits false; only the
    future-only check runs. A same-transaction `effective_from` default of
    `now()` compared against the trigger's own `now()` call is guaranteed
    equal (Postgres's `now()` is stable for the whole transaction), so
    `new.effective_from < now()` is false and a plain insert with no
    explicit `effective_from` always succeeds — confirmed this can't be an
    off-by-one flake before trusting the design.
  - Second insert, earlier or equal `effective_from`: `current_max is not
    null and new.effective_from <= current_max` is true → rejected with the
    "must be later than" message. This is AC6 (conflicting ranges rejected).
  - Two near-simultaneous inserts for the **same** restaurant: both take
    `pg_advisory_xact_lock(hashtextextended(restaurant_id, 0))`; the second
    blocks until the first's transaction commits (the lock is
    transaction-scoped, released exactly at commit/rollback). Under
    Postgres's default READ COMMITTED isolation — which nothing in this
    repo overrides anywhere, checked across every existing migration — the
    second transaction's `select max(effective_from)` re-executes against a
    fresh snapshot once unblocked, so it sees the first transaction's
    now-committed row and correctly rejects if its own `effective_from`
    doesn't come after it. This is the race `schema-change`'s own gate
    asks about explicitly ("concurrent writes... needs an explicit design
    answer") and it resolves at the database, not the application.
  - Two near-simultaneous inserts for **different** restaurants: different
    `hashtextextended` arguments hash (in practice) to different lock keys,
    so neither blocks the other — confirmed by reading `pg_advisory_xact_lock`'s
    own contract (a single 64-bit keyspace, not per-restaurant partitioned,
    so a hash collision between two different restaurant UUIDs is
    theoretically possible but not a correctness bug if it happens — it
    would only serialize two unrelated restaurants' writes, never produce a
    wrong result, since the lock is a mutex around the read-then-check, not
    the source of truth).
- **Matched every pattern against code already applied to this exact
  database**, rather than trusting the design doc's own claims at face
  value: `restaurant_id uuid ... references public.restaurants(id)` against
  the real `restaurants.id uuid` column
  (`20250729143357_initial_restaurant_rls.sql`); `created_by uuid
  references auth.users(id)` character-for-character against `api_keys.created_by`
  (`20260821000001_create_api_keys.sql`); the dedicated
  `update_..._updated_at()` trigger-function shape against
  `restaurant_activations`'s own
  (`20260312000001_restaurant_activations.sql`) — **and found the design
  doc's claim that a shared `update_updated_at_column()` function is "the
  established way to maintain `updated_at`... reused here" does not match
  the codebase**: that function is defined
  (`20250729143432_updated_at_functions.sql`) but `grep`-confirmed to be
  wired to zero tables anywhere in this repo's migration history, while
  `restaurant_activations` — the design's own cited closest structural
  precedent — writes its own dedicated trigger function instead. Followed
  the actual precedent (dedicated function, matching
  `restaurant_activations` exactly) rather than the design doc's inaccurate
  claim; noted here and in the code review rather than silently deviating.
- **No policies, RLS enabled** — matched directly against ENG-006's own
  already-merged, already-live migration
  (`20260828120000_platform_customer_identity.sql`'s
  `platform_customer_legacy_links`, which also carries RLS enabled with no
  insert/update/delete policy for any client role), not merely against the
  design doc's description of it.

**Not verified, and named rather than assumed:** the migration has not been
applied to any real Postgres instance, throwaway or otherwise, this pass —
so a syntax error, while believed absent after the above, cannot be called
impossible with the same confidence a live `psql` run would give. This is a
materially weaker verification than ENG-006's own (which did reach a
throwaway container) and is named as such rather than written up to sound
equivalent.

## Migration file

`supabase/migrations/20260829130000_restaurant_loyalty_configs.sql` in
`aiorders-api`, on branch `loyalty-system`. Naming and style matched against
`20260828120000_platform_customer_identity.sql` (ENG-006, the most recent
migration in this repo) — lowercase keywords, `public.`-qualified names, a
header comment naming the design doc, no `if not exists` (a fresh migration,
never applied before).

## Gate verdict

**pass, with a named verification gap.** No destructive change, no
irreversible change, rollback written (not live-tested this pass — see
above), new-query-pattern index present, no coexistence issue (nothing else
calls this table), backfill n/a (nothing to backfill). The gap is the lack
of a live/container-based dry run, carried forward openly rather than
closed with an unsupported claim; `schema-change`'s own failure-modes list
names exactly this ("designing without the numbers," "an untested
rollback") as what to avoid, and this doc says plainly which one applies
here and why.
