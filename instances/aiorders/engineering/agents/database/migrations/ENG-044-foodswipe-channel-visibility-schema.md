# ENG-044 — restaurants channel-visibility columns + get_restaurants_optimized channel gate

**Project:** aiorders-api
**Migration files:**
- `supabase/migrations/20260907120000_add_channel_visibility_to_restaurants.sql`
- `supabase/migrations/20260907120001_gate_get_restaurants_optimized_by_channel.sql`
**Branch:** `feat/ENG-044-foodswipe-channel-visibility-schema`

## Filename change from the design — a real timestamp collision, not a style choice

The design (`agents/architect/designs/ENG-026-foodswipe-channel-visibility.md`,
written 2026-09-03) and this ticket's own Notes both name
`20260903130000_add_channel_visibility_to_restaurants.sql` /
`20260903130001_gate_get_restaurants_optimized_by_channel.sql`. By the time
this ticket actually built, `20260903130000` had already been claimed —
byte-for-byte, same thirteen digits — by `ENG-031`'s own shipped migration,
`supabase/migrations/20260903130000_add_order_capture_to_catering.sql`
(merged `06e8e84`, verified 2026-09-03). Different suffix, so no file
overwrite, but the numeric prefix is supposed to reflect real authorship
order and these two migrations were written four days apart. Renamed both
files to `20260907120000`/`20260907120001` — today's actual date, later than
every existing migration (`20260904150000` was the most recent), preserving
the original's same-second-plus-one pairing between the two files. Fixed at
the source (this ticket's own board file and the design's Components table)
rather than left for a future reader to trip over — see step 6b in
`eng_build_loop.md`; both are one-line map/location fixes, not decisions.

## The numbers

`supabase db query --linked` against `bmnmnejwdxbcqinqkwko` (single aggregate
query, no per-row data pulled):

```
total: 243, catering_true (live_catering): 7, dine_in_true: 241, dine_in_not_default: 2
```

243 rows. A plain boolean `ADD COLUMN ... DEFAULT` backfills for free (no
separate UPDATE, no rewrite at this size); the two explicit `UPDATE`s this
migration does run touch at most 243 rows each, both single-table, no join,
no index. No lock or runtime concern at any size band this table is
realistically in.

## Live-schema check — requirement 7 / AC5, this ticket's own load-bearing piece

Design and ticket both require checking the live schema before deciding how
`has_dine_in` backfills, rather than guessing. `supabase db dump --linked
--schema public` (schema only, no row data), then read `restaurants`' own
`CREATE TABLE` block directly:

```
"dine_in" boolean DEFAULT true NOT NULL
```

**`dine_in` is real, live, and NOT NULL** — not a dead form field. Branch
taken: backfill `has_dine_in` from `dine_in`'s own per-row value in the same
migration (matching `has_catering`'s treatment), and leave `dine_in` in place,
not dropped. Because it's `NOT NULL`, the copy is total and unambiguous — no
row has a null to reason about, unlike `show_in_marketplace`'s own untracked
history (`20260903120000`'s own comment). **Recorded here and in this
ticket's own Log because `ENG-046` depends on knowing which branch applied**
before it can decide whether its own `dine_in`-bound Switch is a repoint or a
fresh addition: this is a **repoint**.

The same dump also confirms `restaurants.opening_hours` is `"jsonb"[]` — a
Postgres array of jsonb, not a plain `jsonb` column (same shape as `ADR-019`'s
`orders.promos` finding on `ENG-037`). `RETURNS TABLE`'s new `opening_hours`
column is typed `jsonb[]` to match, per the design's own "same type as the
column" instruction.

Also confirmed via the same dump: the live `get_restaurants_optimized`
signature and `RETURNS TABLE` are byte-for-byte identical to
`restaurant-marketplace`'s `20240302_optimize_restaurant_discovery.sql` (read
directly, not from memory or the fallback handler, per the design's own
instruction) — no drift between that file and what's actually live. Ported
from that file unmodified except for the two changes below.

## Two changes on top of the ported function, and why each is safe

- **`p_channel text default null`, appended last** (after `p_offset`, not
  inserted mid-list) — every existing parameter already carries a default, so
  it could legally go anywhere, but appending is the only placement that
  can't perturb an existing *positional* caller. `DEFAULT NULL` plus the `IS
  NULL` branch reproduces today's exact unfiltered behavior for any caller
  that omits it — tested below, not just asserted.
- **`opening_hours jsonb[]`, appended last to `RETURNS TABLE`** — additive,
  named-column consumption (`supabase-js` `.rpc()` returns keyed objects) so
  position doesn't matter functionally, but appending keeps the diff a clean
  extension of the original rather than a reshuffle.

## Constraint / style choices

- **Lowercase SQL keywords throughout**, including in the ported function
  body (the 2024 source file is uppercase). Matches this repo's own current
  convention (`20260829130000_restaurant_loyalty_configs.sql`,
  `20260903130000_add_order_capture_to_catering.sql` — both post-2026-08-29,
  both lowercase), not a stylistic preference invented here. Logic is
  otherwise an unmodified port — every filter, join, and the Haversine
  distance calculation are byte-for-byte the same computation as the source.
- **`add column if not exists` + `comment on column`**, matching
  `20260807000001_add_heard_about_us_to_catering.sql`'s convention, cited
  directly by both the design and this ticket's own Notes.
- **`update ... where has_x is distinct from y`** on both backfills, not an
  unconditional `UPDATE` — matches `20260903120000`'s own precedent for
  exactly this shape of backfill (skip rows that already match, so the
  `RAISE NOTICE` count means something). No `updated_at`-bump trigger exists
  on `restaurants` (confirmed: no `CREATE TRIGGER ... restaurants` anywhere
  in the live dump) so this is a courtesy, not a correctness requirement —
  recorded so nobody has to re-derive that absence later.
- **No separate migration for `has_order_food`'s backfill** — per the design
  and ticket, the column default (`true`) *is* the backfill; a distinct
  `UPDATE ... SET has_order_food = true` would be a no-op write across all
  243 rows for zero benefit.

## The one real defect this pass's own testing caught

**A bare `create or replace function` with a changed parameter count does
NOT error in Postgres — it silently creates a second overload.** Tried this
directly (disposable container, below): recreated the live 13-arg function,
then ran `create or replace function get_restaurants_optimized(...)` with the
new 14-arg signature and no leading `drop`. It succeeded — `pg_proc` then
showed **both** the old 13-arg and new 14-arg functions coexisting. Postgres's
overload resolution prefers the candidate needing the fewest defaulted
arguments, so a positional call with the historical 13 arguments would keep
resolving to the **old, ungated** function forever, silently defeating the
channel gate for any caller that never adopts the 14th argument — a real
production bug, not a theoretical one, and not something `in-review` could
catch by reading the migration file alone (it looks correct on the page; the
bug is in what Postgres does with two files, not one).

`DROP FUNCTION IF EXISTS get_restaurants_optimized(<exact 13-arg type list>)`
before the `CREATE OR REPLACE` is what closes this — not defensive
boilerplate copied from the 2024 source file (which drops for a different
historical reason), but load-bearing for this exact migration. Verified
directly: re-ran migration 2 unmodified against the two-overload state above
and confirmed exactly one function (14 args) remained afterward
(`select proname, pronargs from pg_proc` → one row).

## Verification against a disposable local replica

`supabase/postgres:15.8.1.073` (the `public.ecr.aws` mirror, already cached
on this host from a prior ticket's pass — using the uncached
`docker.io/supabase/postgres` tag re-triggered a full pull and was killed and
redone against the cached one instead). Seeded a minimal stand-in for
`restaurants`/`brands`/`offers` at the pre-migration shape (no `has_*`
columns yet), five rows chosen to exercise every branch: an approved
catering-only restaurant with `dine_in` explicitly `false`, an approved
"default" restaurant matching the 241-of-243 common case, an unapproved
restaurant, an approved-but-`show_in_marketplace=false` restaurant, and an
approved order-food-only restaurant.

Applied both migration files unmodified, then confirmed by direct query, not
by reading the SQL back:

- Column types/defaults/nullability match the design exactly (`has_order_food
  boolean not null default true`, `has_dine_in`/`has_catering` same shape,
  default `false`).
- `has_catering` matches `live_catering` and `has_dine_in` matches `dine_in`
  on every row, zero mismatches (`is distinct from` count = 0 both ways).
  `has_order_food` is `true` on every row, zero exceptions.
- `p_channel := NULL` returns the same 3 approved+visible rows every existing
  caller sees today (backward compatible, not just asserted) —
  `total_count` field reads `3`.
- `p_channel := 'order_food'` returns the same 3 (every row's
  `has_order_food` is `true`) — the pre-existing, untouched `orderingLink`
  filter still applies independently, confirmed by a separate
  `p_has_ordering_link := true` call still correctly excluding the row with
  no brand.
- `p_channel := 'dine_in'` returns exactly the one visible row with
  `has_dine_in = true`; `p_channel := 'catering'` returns exactly the one
  visible row with `has_catering = true`.
- The unapproved row and the `show_in_marketplace = false` row appear under
  **no** channel value, including `NULL` — the pre-existing `approved`/
  `show_in_marketplace` gate is untouched by this change.
- `total_count` reflects the **post-filter** count (`1` under `p_channel :=
  'dine_in'`), not the pre-filter total — confirms the window aggregate is
  computed inside the same filtered CTE chain, not against the unfiltered
  set.
- `opening_hours` passes through as seeded (`jsonb[]`, present on the one row
  that had it, `null` on the rest).
- The historical 13-positional-argument call shape (no `p_channel`) still
  executes and returns the same 3 rows — the exact backward-compatibility
  claim this migration depends on, proven by an actual call in the old
  shape, not inferred from `DEFAULT NULL` alone.

## Rollback

Migration 2's rollback (restore the exact pre-ENG-044 13-arg function,
original body, same drop-first pattern since the arg count is changing
again) — **actually run**, not asserted: `pg_proc` afterward shows exactly
one function, 13 args; a 13-arg positional call still executes and returns
the correct 3 rows.

Migration 1's rollback (`drop column if exists` on all three) — also run and
confirmed (`information_schema.columns` shows zero of the three afterward) —
**but per the design's own Rollout/Risks, not required in practice**: "the
columns can stay in place unused if code reverts, no destructive
down-migration needed." Written and tested anyway because a rollback path
this agent hasn't run is a rollback path this agent doesn't trust, not
because this ticket expects to need it.

Container removed after testing (`docker rm -f`); nothing left running.
Temp SQL files and the schema dump removed from `/tmp`.

## What this migration deliberately does not do

No index (design's own call — both new columns and the RPC's existing filter
columns are read through each tab's already-indexed-or-not discovery query,
never queried in isolation). No `CHECK`, no enum — three independent
booleans, matching this table's existing flag columns
(`cafe`/`bar`/`live_catering`/`party_hall`/`food_truck` are all plain
booleans with no cross-constraint). Does not touch `admin-portal/handlers/
restaurants.ts` (design's own Components table: already passes arbitrary
keys through, zero code needed) or `restaurants_public` or any other view —
out of scope, not named in the design's Data or Interfaces sections.

## Gate verdict

**pass.** Three additive, backward-compatible columns plus one function
replacement, every column and interface change traced to the design's Data
or Interfaces section, the one open backfill question (`has_dine_in`)
resolved against the live schema with real numbers rather than guessed, a
real Postgres overload-resolution defect caught and closed by testing rather
than by inspection, both migrations verified end-to-end against a disposable
replica seeded to exercise every branch, and both rollbacks actually
executed and confirmed rather than asserted.
