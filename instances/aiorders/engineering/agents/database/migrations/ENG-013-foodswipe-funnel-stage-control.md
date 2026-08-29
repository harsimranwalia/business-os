# ENG-013 — foodswipe_stage_override on profiles

**Project:** aiorders-api
**Migration file:** `supabase/migrations/20260829200000_add_foodswipe_stage_override.sql`
**Branch:** `feat/ENG-013-foodswipe-funnel-stage-control`

## The numbers

One nullable `text` column added to `profiles`, no default, no backfill.
Verified live (Supabase MCP, read-only, project `bmnmnejwdxbcqinqkwko`,
zero cost): `profiles` holds 528 rows total, 36 with `source = 'foodswipe'`
— the only rows this feature ever reads or writes. `ADD COLUMN` with no
`DEFAULT` is a metadata-only catalog change in Postgres regardless of
table size (no table rewrite, no full-table lock); at 528 rows the
question would not matter anyway.

## Design for the query, not the diagram

No new query path. The existing kanban read (`handleFoodswipe`) already
selects a fixed column list off `profiles` filtered on `source =
'foodswipe'` — this adds one column to that same `select()` call. The two
new write actions (`setStageOverride`, `resetStageOverride`) are single-row
`UPDATE ... WHERE id = $1 AND source = 'foodswipe'`, keyed on `profiles.id`
(primary key) — no new index needed, no scan.

## Why a column, not a new table

Considered and rejected in the design
(`agents/architect/designs/ENG-013-foodswipe-funnel-stage-control.md` →
Alternatives): a dedicated `foodswipe_overrides` table would be the
conventional choice if this needed a history/audit trail, but this
ticket's acceptance criteria only ask for the current value to stick and
be resettable — a nullable column on the one entity present at every
stage is the smaller, fully reversible change. Verified live that
`profiles` is in fact that entity: `information_schema.columns` confirms
`id uuid NOT NULL` (primary key) and `source text` both already exist
exactly as the handler code assumes.

## Constraint choice

`CHECK (foodswipe_stage_override IN (...six values...))`, column
otherwise unconstrained (nullable, no default). Mirrors the `Stage` union
type in `admin-portal/handlers/foodswipe.ts` and the `VALID_STAGES` array
added there — three independent copies of the same six literals (this
constraint, the TS union, the frontend's `StageKey` type), which is a
real but pre-existing pattern in this codebase (the union type itself was
never backed by a shared source of truth even before this ticket).
Flagged in the design's own Risks section as something a future
stage-set change must update in all three places at once; not solved
here since solving it isn't in this ticket's acceptance criteria.

## Expand/contract sequence

Single step. One `ALTER TABLE ... ADD COLUMN ... CHECK (...)` in one
migration — no coexistence window, since no existing code path reads or
writes this column until this same PR's handler/frontend changes ship
alongside it. `null` is a valid state from the moment the column exists,
and every existing row gets exactly that.

## Runtime and locks

`ADD COLUMN` with no `DEFAULT` takes a brief `ACCESS EXCLUSIVE` catalog
lock (standard Postgres behavior for any `ALTER TABLE`) but performs no
table rewrite and no per-row work — near-instant at any table size,
confirmed proportionate here at 528 rows. No online strategy or
maintenance window needed.

## Backfill

None. Every existing row's new column starts `null`, which is exactly
"keep computing the stage automatically" — the behavior every listing
already has today. Nothing to migrate forward.

## Rollback

```sql
ALTER TABLE profiles DROP COLUMN IF EXISTS foodswipe_stage_override;
```

Should be paired with reverting the handler's override-check branch and
the frontend's stage-control UI in the same rollback. Reading a dropped
column isn't possible (the handler would fail to compile/select it), so
unlike ENG-011's function-only rollback, this one is a hard dependency:
roll back all three together, not the column alone.

## Verification actually performed this pass

No live/staging Postgres CLI reachable from this host (no `docker`, no
`psql`, no `supabase` CLI — same limitation `ENG-007`'s and `ENG-011`'s
migration docs recorded), so the statement itself has not been executed
anywhere. What was verified instead, via the read-only Supabase MCP
connection to the real `aiorders-api` project (`bmnmnejwdxbcqinqkwko`),
the same path ENG-011's addendum used:

- `information_schema.columns` on `profiles`: confirms every column the
  handler's `select()` calls already assume (`id`, `name`, `first_name`,
  `last_name`, `email`, `phone`, `source`, `created_at`) exists with the
  expected type/nullability, and confirms `foodswipe_stage_override`
  does **not** already exist under this or a colliding name.
- `id uuid NOT NULL` is the primary key column both new write actions key
  on (`.eq('id', profileId)`) — a single-row, indexed lookup.
- `source text` (nullable) backs the `.eq('source', 'foodswipe')` scoping
  already used by the existing read path and now also by both new write
  actions — confirmed to be a real, populated column (36 of 528 rows
  carry the literal value `'foodswipe'`), not an assumption.
- `list_migrations` on the live project: this migration
  (`20260829200000_add_foodswipe_stage_override`) is not present —
  production is exactly where this doc assumes it is, unapplied.
- RLS is a non-issue for this change: every read and write this ticket
  adds goes through `auth.adminSupabase` (the service-role client
  `admin-portal/index.ts` already constructs for every request this
  handler serves), which bypasses RLS entirely — same as every other
  write in `admin-portal/handlers/*`. No policy needs updating.

**Deliberately not done, and why:** dry-running the actual `ALTER TABLE`
statement (e.g. via a throwaway Supabase branch) was not attempted —
`create_branch` is gated behind a real recurring charge
(`confirm_cost`), and applying DDL directly to production ahead of this
ticket's own PR/review would jump the L1 human-merge gate. Not this
pass's call to make unilaterally. Named as the same category of residual
gap ENG-007's and ENG-011's migration docs carried forward, not closed
here — but a plain, single-statement `ADD COLUMN` with a `CHECK` on a
528-row table is a materially smaller unverified-execution risk than
ENG-011's `DROP FUNCTION`/`CREATE FUNCTION` pair.

## Migration file

`supabase/migrations/20260829200000_add_foodswipe_stage_override.sql` in
`aiorders-api`, on branch `feat/ENG-013-foodswipe-funnel-stage-control`.
Timestamp chosen after the latest applied migration
(`20260829190000_add_last_order_at_to_platform_analytics.sql`, itself not
yet applied per `list_migrations` above, but the highest-numbered file on
disk). Header-comment style matches the surrounding migrations in this
directory.

## Gate verdict

**pass.** Additive-only, nullable, no default, no backfill, no RLS
change, no new query path, no index need at current or foreseeable scale
for this feature (36 foodswipe profiles). One real design question (table
vs. column) was already resolved at the architecture stage with a
reversible answer. The one open gap — the statement has not executed
against any live Postgres — is named rather than assumed away, and is
smaller in kind than the two prior tickets' gates accepted on this same
host for materially riskier statements.
