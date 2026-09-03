# ENG-008 — staff_rating, collaboration_count, accepts_paid on influencers

**Project:** aiorders-api
**Migration file:** `supabase/migrations/20260829220000_add_influencer_admin_fields.sql`
**Branch:** `feat/ENG-008-influencer-admin-management`

**Amended 2026-09-02, post-merge-request:** the approver rejected the
originally-planned fourth column, `accepts_barter`, as redundant with the
already-existing `barter_visit` boolean ("There is no need for a new column
when we already have a column to signify the same intent"). Dropped from the
migration; every read/write below that referenced it now targets
`barter_visit` instead, which this migration never touches. Everything below
is updated to reflect that — no `accepts_barter` column exists anywhere in
this ticket's shipped shape.

## The numbers

Verified live (Supabase MCP, read-only, project `bmnmnejwdxbcqinqkwko`, zero
cost): `influencers` holds 306 rows. Of those, 226 have `barter_visit = true`,
29 have `barter_visit = false`, and 51 have `barter_visit = null`. The
backfill (`accepts_paid = NOT barter_visit`) turns those into 226 rows
`{barter_visit: true, accepts_paid: false}`, 29 rows `{barter_visit: false,
accepts_paid: true}`, and 51 rows left `{barter_visit: null, accepts_paid:
null}` — preserving "unknown" as unknown rather than guessing a value for the
51, exactly as the design specified. `information_schema.columns` confirmed
before writing the migration that none of the new column names
(`staff_rating`, `collaboration_count`, `accepts_paid`) already exist under
this or a colliding name.

## Design for the query, not the diagram

No new query path for reads — `src/pages/Influencers.tsx` already does
`select('*')`, so the new columns arrive for free. Writes are a single
new endpoint, `PATCH /admin-portal/influencers/{id}`
(`admin-portal/handlers/influencers.ts`), a single-row `UPDATE ... WHERE id =
$1` keyed on `influencers.id` (primary key) — no new index needed, no scan.

## Why extend the existing boolean rather than add a third preference column

Considered and rejected in the design
(`agents/architect/designs/ENG-008-influencer-profile-admin-management.md` →
Alternatives): a new `text[]` `preferred_campaign_types` column was the
original plan, dropped once `Influencers.tsx` showed `barter_visit` is
already live and displayed — a second, parallel representation of the same
fact would have created two sources of truth for "does this influencer take
paid work." The original build paired a new `accepts_paid` with a new
`accepts_barter`, two independent booleans instead of one four-state enum, so
both flags stay independently settable ("paid, barter, or both"). The
approver's own merge-request reply corrected the second half of that:
`accepts_barter` duplicated `barter_visit`'s existing signal, so only
`accepts_paid` is actually new — the independent-booleans shape survives
(`accepts_paid` + the pre-existing `barter_visit`), just with one column
fewer than originally built.

## Constraint choice

`staff_rating smallint CHECK (staff_rating BETWEEN 1 AND 5)`. In Postgres a
`CHECK` expression that evaluates to `NULL` satisfies the constraint (it
only fails on an explicit `false`), so this one line permits both "no rating
yet" and 1–5 without an `OR staff_rating IS NULL` clause. `collaboration_count
integer NOT NULL DEFAULT 0` — unlike the rating, "no collaborations yet" and
"not yet answered" are the same real-world state, so a hard default is
correct here rather than nullable. `accepts_paid` is left an unconstrained
boolean (nullable, no default), matching the existing `barter_visit` column
it's paired with — see Backfill below for why null is a meaningful third
state for both.

## Expand/contract sequence

Single step. One `ALTER TABLE` adding all three columns plus the backfill
`UPDATE`, in one migration — no coexistence window, since no existing code
path reads `accepts_paid`/`staff_rating`/`collaboration_count` until this
same PR's handler and frontend changes ship alongside it. `barter_visit`
itself is untouched (not dropped, not renamed, and now also not duplicated),
so every existing reader of that column — in this repo or, per the design's
own flagged risk, possibly in `aiorders-api` code this ticket didn't touch —
keeps working unmodified; this ticket's own handler and frontend gain a new
writer for it rather than a competing column.

## Runtime and locks

Three `ADD COLUMN`s, two with no `DEFAULT` and one (`collaboration_count`)
with a constant `DEFAULT 0` — both are metadata-only catalog changes in
Postgres 11+ (no table rewrite, no per-row write, same as `NOT NULL DEFAULT
<constant>` specifically). The backfill `UPDATE` touches all 306 rows once;
at this table size that's near-instant regardless. A brief `ACCESS
EXCLUSIVE` catalog lock is taken for the `ALTER TABLE` itself, standard and
momentary. No online strategy or maintenance window needed at 306 rows.

## Backfill

`UPDATE influencers SET accepts_paid = NOT barter_visit` — no `WHERE` clause
needed since the column is brand new (every row is `NULL` immediately after
the `ADD COLUMN`, so there is nothing to avoid overwriting). Postgres `NOT
NULL` is `NULL`, so the 51 rows with `barter_visit IS NULL` backfill to
`accepts_paid = NULL` rather than a guessed `false`/`true` — preserving
exactly what the existing data does and does not know, per the design's
explicit instruction not to invent information the source column didn't
have. `barter_visit` itself needs no backfill; it already carries its own
values.

## Rollback

```sql
ALTER TABLE influencers
  DROP COLUMN IF EXISTS staff_rating,
  DROP COLUMN IF EXISTS collaboration_count,
  DROP COLUMN IF EXISTS accepts_paid;
```

Should be paired with reverting the handler (`admin-portal/handlers/
influencers.ts`, and the `influencers` routing branch in `admin-portal/
index.ts`) and the frontend edit form in `src/pages/Influencers.tsx` in the
same rollback — reading a dropped column isn't possible, so like ENG-013's
rollback this is a hard dependency across all three, not a column-only
revert. `barter_visit` needs no rollback step of its own since this
migration never modifies it.

## Verification actually performed this pass

No live/staging Postgres CLI reachable from this host (no `docker`, no
`psql`, no `supabase` CLI — same limitation ENG-007's, ENG-011's, and
ENG-013's migration docs recorded), so the statement itself has not been
executed anywhere. What was verified instead, via the read-only Supabase MCP
connection to the real `aiorders-api` project (`bmnmnejwdxbcqinqkwko`):

- `information_schema.columns` on `influencers`: confirmed the full existing
  column set (`barter_visit boolean`, `min_visit_payment numeric`,
  `city_preference text[]`, `cuisine_preference text[]`, plus identity/social
  fields) matches what both the existing frontend and this ticket's design
  assume, and confirmed none of the three new column names already exist.
- Row-level counts on `barter_visit` (306 total / 226 true / 29 false / 51
  null) computed directly against production data, not estimated — see The
  numbers above.
- `relrowsecurity` on `influencers` is `true`, but this is a non-issue for
  this change: every read and write this ticket adds goes through
  `auth.adminSupabase` (the service-role client `admin-portal/index.ts`
  already constructs for every request this handler serves), which bypasses
  RLS entirely — same as every other write in `admin-portal/handlers/*`. No
  policy needs adding or updating.
- `list_migrations` on the live project: confirmed the latest **applied**
  migration is `20260828120000_platform_customer_identity`, matching the
  latest file on `origin/main` — this migration
  (`20260829220000_add_influencer_admin_fields`) is not present, so
  production is exactly where this doc assumes it is, unapplied, and the
  chosen timestamp sorts after every applied migration.

**Deliberately not done, and why:** dry-running the actual `ALTER TABLE`/
`UPDATE` pair (e.g. via a throwaway Supabase branch) was not attempted —
`create_branch` is gated behind a real recurring charge (`confirm_cost`),
and applying DDL directly to production ahead of this ticket's own PR/review
would jump the L1 human-merge gate. Not this pass's call to make
unilaterally. Named as the same residual gap ENG-007's, ENG-011's, and
ENG-013's migration docs each carried forward, not closed here — a
two-statement additive `ALTER TABLE` + unconditional `UPDATE` on a 306-row
table is comparable in risk to ENG-013's single `ADD COLUMN` and materially
smaller than ENG-011's `DROP FUNCTION`/`CREATE FUNCTION` pair.

## Migration file

`supabase/migrations/20260829220000_add_influencer_admin_fields.sql` in
`aiorders-api`, on branch `feat/ENG-008-influencer-admin-management`.
Timestamp chosen after the latest applied migration
(`20260828120000_platform_customer_identity`, confirmed via `list_migrations`
above) and after the highest-numbered file on `origin/main`'s disk tree.
Deliberately not `20260829200000` or adjacent — that timestamp belongs to
`ENG-013`'s still-unmerged migration on a different branch, and the two
tickets' migrations must not collide if both land close together. Header
comment style matches the surrounding migrations in this directory.

## Gate verdict

**pass.** Additive-only: two nullable columns, one `NOT NULL DEFAULT 0`
column, a backward-compatible backfill (`barter_visit` → `accepts_paid`)
that leaves `barter_visit` itself untouched. No RLS change, no new query
path beyond one indexed single-row `UPDATE`, no index need at current or
foreseeable scale (306 influencers).
The one open gap — the statement has not executed against any live Postgres
— is named rather than assumed away, consistent with every other migration
gate on this instance to date.
