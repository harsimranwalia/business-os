# ENG-052 — widen loyalty_ledger_entries for redemption, add redeem_points_if_eligible

**Project:** aiorders-api
**Migration file:** `supabase/migrations/20260908160000_loyalty_ledger_redemption_widening_and_redeem_function.sql`
**Branch:** `feat/ENG-052-loyalty-redemption-ledger-widening-and-redeem-function`

## The numbers

`loyalty_ledger_entries`: **zero rows**, confirmed live this pass
(`select count(*) ... ` against the linked project — `ENG-049` is deployed but
nothing has yet exercised the webhook accrual, the auto-complete sweep, or
dine-in earn in production). Every `ALTER` below runs against an empty
table — no existing-row validation cost, no lock-duration risk regardless of
what the table's own steady-state write volume becomes once `ENG-053` ships
the caller. Same "provisioning for a pattern, not a measured load" framing
`ENG-048`'s own plan used for this identical table nine hours earlier.

`restaurant_loyalty_configs`: also zero rows live (no restaurant has a
configured rate yet) — so there is no real `redemption_value_per_point` value
to size the precision question against empirically; the fix below (see
Constraint choice) is made on the column's own declared type, not on
observed data.

Growth per month / query frequency / read-write ratio: unmeasured, same
position every ticket in this sequence has been in pre-launch — `ENG-053`
(backend) is this migration's only intended caller and hasn't shipped yet.

## Verification against the live project

Ran read-only against the linked project this pass (`supabase db query
--linked`, single aggregate/metadata queries only — no row-level customer
data):

- `loyalty_ledger_entries` row count: 0.
- **Every constraint name this migration's `DROP CONSTRAINT` targets,
  confirmed against live `pg_constraint`, not assumed from the design's own
  "best reading" of Postgres's auto-generated names** (the design's own Data
  section flags exactly this as needing confirmation before writing the
  `DROP CONSTRAINT`): `loyalty_ledger_entries_source_check`,
  `loyalty_ledger_entries_order_id_matches_source`,
  `loyalty_ledger_entries_reason_matches_source`,
  `loyalty_ledger_entries_created_by_matches_source` — all four match the
  design's predicted names exactly, byte for byte.
- `restaurant_loyalty_configs.redemption_value_per_point` and
  `platform_customers.id` column shapes confirmed live
  (`information_schema.columns`): `numeric(10,4)` and `uuid` respectively,
  matching the design and `ENG-007`'s/`ENG-006`'s own migrations.
- Existing indexes on `loyalty_ledger_entries` confirmed live
  (`pg_indexes`): `loyalty_ledger_entries_customer_restaurant_idx` on
  `(platform_customer_id, restaurant_id)` and the `order_id` unique index —
  matches the design's own claim that no new index is needed beyond the
  `idempotency_key` unique constraint (Data section) — confirmed rather than
  taken on trust.
- `pg_default_acl` for schema `public`, function objects (`defaclobjtype =
  'f'`): confirmed live this pass, same finding `ENG-048`'s round-2 review
  fix already established for this project — grantor `supabase_admin` grants
  `EXECUTE` to `anon`/`authenticated`/`service_role` **by name** at
  function-creation time, a separate mechanism `REVOKE ... FROM PUBLIC`
  cannot reach. Applied the same two-statement fix from the start (naming
  `anon`/`authenticated` directly) rather than writing the insufficient
  `FROM PUBLIC`-only form and finding this at review, the way `ENG-048`
  round 1 did.
- `vault.secrets` carries `service_role_key` — not needed by this migration
  (no cron job here), checked anyway while linked and noted for completeness.

## Constraint choice

- **Three widened per-source checks** (`order_id`, `fulfillment_reason`,
  `created_by`) each grow a third arm, `redemption` behaving like `dine_in`
  on the first two (no order, no fulfilment window) and, deliberately, also
  like `dine_in` on `created_by` (**not** like `online_order`) — a debit
  needs an audit trail (which staff member authorized it) at least as much
  as `dine_in`'s own unverifiable-amount risk already established. Tested
  directly: a redemption row with `created_by null` is rejected (same
  constraint, same failure mode `dine_in` already gets); a redemption row
  with a non-null `order_id` is rejected.
- **New `loyalty_ledger_entries_points_sign_by_source`** —
  `(source in ('online_order','dine_in') and points >= 0) or (source =
  'redemption' and points < 0)`. `>= 0`, not `> 0`, for the earn sources,
  matching `credit_order_if_eligible`'s own zero-floor and a
  legally-configurable 0%-rate case already being real and unconstrained —
  this migration doesn't tighten a path it doesn't own. Tested both
  directions: a `redemption` row with `points >= 0` is rejected; an
  `online_order` row with `points < 0` is rejected (existing sources stay
  governed by the new check too, confirmed rather than assumed from reading
  the `OR` clause).
- **New nullable `idempotency_key text`, unique when present** — same
  nullable-safe shape `order_id`'s own constraint already uses (Postgres
  treats every `NULL` as distinct under a plain `UNIQUE`). Tested: two
  `redemption` rows with `idempotency_key null` coexist without conflict.
- **`rate_applied` widened `numeric(5,2)` → `numeric(10,4)` — found during
  this pass's own build hop, not named in the architect's design.** The
  design's Interfaces section states the insert row as `rate_applied =
  v_rate` without addressing that the existing column (sized for the earn
  side's percentage rates, `online_earn_pct`/`dine_in_earn_pct`, always
  `0`–`100.00`) is narrower than `redemption_value_per_point`'s own declared
  type, `numeric(10,4)` — a dollars-per-point ratio ENG-007 deliberately gave
  four decimal places (e.g. `1000` points `= $1` → `$0.0010`/point). Storing
  that snapshot into `numeric(5,2)` would silently round anything below
  `0.01` to `0.00` — not caught by any constraint, and defeating the
  column's own documented purpose ("a snapshot ... so a later rate change
  never changes what an already-credited entry says it earned at").
  Same discipline `ENG-007`'s own pass set for a design-vs-repository
  mismatch ("followed the actual precedent ... noted here ... rather than
  silently deviating"), applied here to a design-vs-live-schema-type
  mismatch instead. **Confirmed, not assumed, to be a pure widening:**
  every existing `online_order`/`dine_in` row's `rate_applied` (a
  percentage, always `<= 100.00`) casts up losslessly, and
  `credit_order_if_eligible`'s own `v_rate` (still declared `numeric(5,2)`,
  untouched by this migration) inserts into the widened column exactly as
  before — proven directly this pass with a raw `online_order`-shaped
  insert at `rate_applied 5.00`, read back as `5.0000` under the new type,
  `pg_typeof` confirming `numeric`. **The redemption side's own precision is
  what this fix actually proves**: a `redeem_points_if_eligible` call
  against a restaurant configured at `redemption_value_per_point 0.0025`
  stored (and read back) `rate_applied 0.0025` exactly — not `0.00` — the
  regression this fix exists to prevent, confirmed by direct query rather
  than by reading the migration back.

## Runtime and locks

Every statement in this migration targets a table confirmed at **zero rows**
live this pass. `ALTER TABLE ... DROP/ADD CONSTRAINT` (all five —
three widened checks, the new sign check, the new unique) and `ALTER COLUMN
... TYPE` each take an `ACCESS EXCLUSIVE` lock for their duration, but that
duration is the cost of validating a `CHECK`/`UNIQUE` against the table's
existing rows — with zero rows, each is sub-millisecond regardless of the
table's steady-state write traffic once `ENG-053` ships. No `CONCURRENTLY`
strategy is applicable here the way `ENG-048`'s own `orders` index needed
one (`orders` was live and ~21.9k rows at the time; this table is not, right
now). `ADD COLUMN idempotency_key text` (no default): metadata-only,
near-instant at any table size. `CREATE OR REPLACE FUNCTION`: no lock on any
table, replaces a name that doesn't exist yet (a genuinely new function, not
an argument-count change to an existing one — the `ENG-044`
`CREATE OR REPLACE` overload trap this project's own database notebook
already flags does not apply here).

## Expand/contract sequence

Additive only, per the design's own Rollout: three widened checks (each
strictly adding a previously-impossible arm), one new check, one new
nullable column, one new function, one widened column. Nothing existing is
read or written differently by any of it until `ENG-053` ships the caller —
same "inert until the sibling ships" shape `ENG-048`'s own release used for
`ENG-049`.

## Backfill

None. `idempotency_key` is nullable and starts `null` for the table's zero
existing rows (and stays `null` forever for `online_order`/`dine_in`, which
have no retry-safety need of their own here). `rate_applied`'s widening
changes no stored value, only the column's own representable range.

## Rollback

```sql
drop function if exists public.redeem_points_if_eligible(uuid, uuid, numeric, text, uuid);
alter table public.loyalty_ledger_entries drop constraint if exists loyalty_ledger_entries_idempotency_key_key;
alter table public.loyalty_ledger_entries drop column if exists idempotency_key;
alter table public.loyalty_ledger_entries drop constraint if exists loyalty_ledger_entries_points_sign_by_source;
alter table public.loyalty_ledger_entries alter column rate_applied type numeric(5,2);
alter table public.loyalty_ledger_entries drop constraint if exists loyalty_ledger_entries_created_by_matches_source;
alter table public.loyalty_ledger_entries add constraint loyalty_ledger_entries_created_by_matches_source check ((source = 'dine_in' and created_by is not null) or (source = 'online_order' and created_by is null));
alter table public.loyalty_ledger_entries drop constraint if exists loyalty_ledger_entries_reason_matches_source;
alter table public.loyalty_ledger_entries add constraint loyalty_ledger_entries_reason_matches_source check ((source = 'online_order' and fulfillment_reason is not null) or (source = 'dine_in' and fulfillment_reason is null));
alter table public.loyalty_ledger_entries drop constraint if exists loyalty_ledger_entries_order_id_matches_source;
alter table public.loyalty_ledger_entries add constraint loyalty_ledger_entries_order_id_matches_source check ((source = 'online_order' and order_id is not null) or (source = 'dine_in' and order_id is null));
alter table public.loyalty_ledger_entries drop constraint if exists loyalty_ledger_entries_source_check;
alter table public.loyalty_ledger_entries add constraint loyalty_ledger_entries_source_check check (source in ('online_order', 'dine_in'));
```

Order matters: the function and the `idempotency_key`/sign-check/
`rate_applied` changes unwind first (nothing else depends on them), then the
three per-source checks restore to their original two-arm form, then
`source_check` narrows back last — restoring it before the per-source checks
would still succeed (no row-count-dependent ordering constraint between
them on an empty table), but this order mirrors the forward migration
reversed, which is the easier one to audit by inspection.

**Note beyond the ticket's own three-item rollback description:** the
ticket's Notes list "drop the new function, drop the `idempotency_key`
column and its constraint, restore the three widened checks" — that
enumeration predates this pass's own `rate_applied`-widening finding and the
new sign check, both of which also need unwinding. Both are included above;
named here so a future reader isn't confused by the ticket text undercounting
by two.

**Actually run, against a disposable replica seeded to the exact live shape
`ENG-048`'s own migration created** (`public.ecr.aws/supabase/postgres:15.8.1.073`,
same image every prior pass on this ticket sequence has used): applied on a
**clean** copy (zero rows, matching "safe any time before `ENG-053` ships,"
the actual precondition under which this rollback is meant to run) rather
than the same replica carrying this pass's own test data — the test data
itself includes `redemption`-sourced rows that the original, narrower
`source_check` cannot accept, so re-narrowing it against them would fail
correctly (proving the constraint works) rather than demonstrating the
rollback's real intended precondition. All twelve statements succeeded;
confirmed after, by direct query rather than by reading the SQL back:
`redeem_points_if_eligible` gone from `pg_proc` (`fn_count 0`);
`idempotency_key` absent from `\d+ loyalty_ledger_entries`; `rate_applied`
back to `numeric(5,2)`; all four check constraints' definitions
character-for-character equal to `20260907130000`'s own originals; and a
fresh `redemption`-sourced insert attempt rejected (a `CHECK` violation —
`redemption` is no longer constructible on this table by any of the
restored constraints, the behavioral proof that matters more than which
specific constraint name catches it first).

Safe any time before `ENG-053` ships (nothing calls
`redeem_points_if_eligible` or writes `idempotency_key`/a `redemption` row
until then); once `ENG-053` ships, rolling back must happen together with
reverting its own changes, same caveat `ENG-027`'s and `ENG-048`'s own
migration plans recorded for their columns.

## Verification actually performed this pass

**Against the live project** — see "Verification against the live project"
above (row count, constraint names, column shapes, index list, default ACL;
no row-level customer or restaurant data read).

**Against a disposable local replica**, a minimal stand-in for the five
tables this migration references (`restaurants(id)`, `orders(id)`,
`platform_customers(id, phone, display_name, consent_recorded_at,
created_at, updated_at)`, `restaurant_loyalty_configs(...)` — column shapes
taken from the live reads above — and `loyalty_ledger_entries` created
exactly as `20260907130000` (`ENG-048`) left it live), plus `auth.users`
(pre-shipped in the image; one row inserted for `created_by`/`created_at`
foreign keys, since the image ships the table empty).

Applied the real migration file unmodified and confirmed by direct query,
not by reading the SQL back — full matrix, one restaurant configured at a
deliberately sub-cent `redemption_value_per_point` (`0.0025`) specifically
to exercise the precision fix:

- **Happy path**, 400-point seeded balance, redeem 100 → `redeemed`; row
  reads `points -100.0000, amount 0.25, rate_applied 0.0025` (not `0.00` —
  the regression this pass's own `rate_applied` widening prevents).
- **Idempotent replay** — same key, same `(diner, restaurant, points)` →
  `redeemed` again, confirmed **zero** new rows for that key.
- **Idempotency conflict** — same key, different `points` → raises, confirmed
  by an actual error, not read from the `if` branch.
- **Insufficient balance** (remaining `300`, requested `301`) →
  `insufficient_balance`, zero rows inserted.
- **Exact-balance boundary** (remaining `300`, requested `300`) → `redeemed`
  — confirms "exceeds" is `<`, not `<=`, per the design's own AC5 wording;
  balance afterward `0.0000`.
- **Unenrolled restaurant** → `not_enrolled`.
- **Invalid platform_customer_id** (enrolled restaurant, nonexistent diner)
  → `invalid_code`.
- **Guards**: `p_points <= 0` and `p_idempotency_key null` both raise,
  confirmed as actual errors.
- **Cross-field `CHECK`s, each proven with a real failing/succeeding raw
  insert, not inferred from the constraint text:** `redemption` with a
  non-null `order_id` (real FK-valid `orders` row, not a dangling UUID) →
  rejected; `redemption` with `points >= 0` → rejected; `online_order` with
  `points < 0` → rejected (the new sign check binds the earn sources too);
  `dine_in` with `created_by null` → still rejected (unchanged arm);
  `redemption` with `created_by null` → rejected (the new arm, matching
  `dine_in`'s own requirement); two `redemption` rows with
  `idempotency_key null` → both succeed, coexisting.
- **Grant/revoke**, all four roles: `anon → false`, `authenticated → false`,
  `service_role → true`, matching `ENG-048`'s own corrected shape from the
  start rather than finding the `FROM PUBLIC`-only gap at review.
- **`rate_applied` widening backward-compatibility** — a fresh
  `online_order`-shaped row at `rate_applied 5.00` (a real FK-valid
  `orders` row) stores and reads back as `5.0000`, `pg_typeof numeric` —
  the earn path is unaffected by the widening.
- **Rollback** — see Rollback above; run against a clean (zero-row) copy of
  the same replica shape, all twelve statements succeed, schema shape
  restored character-for-character, function gone, a fresh `redemption`
  insert rejected afterward.

All containers removed after use; nothing left running
(`docker ps -a --filter name=eng052` empty after cleanup).

## Migration file

`supabase/migrations/20260908160000_loyalty_ledger_redemption_widening_and_redeem_function.sql`
in `aiorders-api`, on branch
`feat/ENG-052-loyalty-redemption-ledger-widening-and-redeem-function`,
branched fresh from `origin/main` (`fb26921`) — re-confirmed unchanged this
pass from the ticket's own already-recorded branch point; no open PR to
stack on (`gh pr list --state open` empty on this project).

## Gate verdict

**pass.** No destructive change (every constraint drop is immediately
followed by a wider re-add covering every case the original allowed, plus
new ones; `rate_applied`'s widening is representation-only). No irreversible
change — rollback written and actually run against a disposable replica,
twice (forward-then-verify, and a clean rollback run), not merely asserted.
New query pattern (`idempotency_key` point lookup) backed by the `UNIQUE`
constraint's own index, confirmed no separate index needed. No blocking-lock
concern — every altered table confirmed at zero live rows this pass, so
`ACCESS EXCLUSIVE` duration is negligible regardless of the table's
steady-state traffic once `ENG-053` ships. No backfill owed. Schema and code
coexist across the deploy: additive only, unreachable until `ENG-053`'s
`brand-portal` handler calls it, same "invisible until wired in" position
this whole sequence has shipped in already. One real gap found and fixed
during this pass's own diligence rather than left for review to catch —
`rate_applied`'s precision mismatch against `redemption_value_per_point`,
proven both as a regression (a sub-cent rate now survives instead of
truncating to zero) and as backward-compatible (the earn path's own
percentage values are unaffected).
