# ENG-009 — social_stats_updated_at, social_stats_platform on influencers

**Project:** aiorders-api
**Migration file:** `supabase/migrations/20260830100000_add_influencer_social_stats.sql`
**Branch:** `feat/ENG-009-influencer-engagement-info`

## The numbers

Re-verified live (Supabase MCP, read-only, project `bmnmnejwdxbcqinqkwko`,
zero cost) immediately before writing this migration: `followers integer
DEFAULT 0` and `engagement numeric DEFAULT 0` both exist and are non-null on
every row; `follower_count text` (no default) exists separately. Neither
`social_stats_updated_at` nor `social_stats_platform` exists under this or a
colliding name — confirmed via `information_schema.columns`, not assumed
from the architect design doc's own same-day reading.

`list_migrations` on the live project: latest **applied** migration is
`20260829190000_add_last_order_at_to_platform_analytics`. Neither
`ENG-013`'s (`20260829200000`) nor `ENG-008`'s (`20260829220000`) is applied
yet — both are still on unmerged branches, exactly as the architect design
recorded. This migration's timestamp (`20260830100000`) sorts after all
three.

## Design for the query, not the diagram

No schema change for Reading B's storage — `followers`/`engagement` are
reused as-is (see the architect design's Alternatives section for why a
second pair of columns was rejected). The only new columns are
`social_stats_updated_at` (the field-specific "when was this set" marker
AC4 needs, since `ENG-008`'s edit form bumps the table-wide `updated_at`
too) and `social_stats_platform` (optional label). Both are additive,
nullable, no default, no backfill.

Reading A (internal activity signal) is computed on read from
`influencer_invitations` and stored nowhere — no migration surface at all.
It requires the service-role client (`auth.adminSupabase`), never the anon
client: `influencer_invitations` carries `SELECT` policies only for
influencer-sees-own and restaurant-owner-sees-theirs, no staff/admin policy.
Confirmed this is unchanged from the architect design's own reading rather
than re-verified from scratch this pass (RLS policy shape doesn't drift
between same-week passes on a table nothing has touched).

Writes go through `PATCH /admin-portal/influencers/{id}`
(`admin-portal/handlers/influencers.ts`, extending `ENG-008`'s handler and
`EDITABLE_FIELDS`), a single-row `UPDATE ... WHERE id = $1` keyed on the
primary key — no new index needed, no scan. The activity read is a new `GET
/admin-portal/influencers/activity` (no id — routed before the generic
per-id match, since the id-match regex would otherwise treat the literal
string "activity" as an id), a single unfiltered `SELECT` over
`influencer_invitations` (809 rows today) grouped in memory — never one
query per influencer.

## Constraint choice

Both new columns are unconstrained (`timestamptz` nullable no default,
`text` nullable no default) — unlike `ENG-008`'s `staff_rating`, there is no
finite legal range to enforce with a `CHECK`. `social_stats_platform`'s
32-character cap is enforced in the handler, not the schema, matching this
repo's existing convention of doing string-shape validation in the write
path rather than a `CHECK (length(...) <= n)` constraint (no other text
column on this table uses one).

## Expand/contract sequence

Single step, same shape as `ENG-008`'s and `ENG-013`'s migrations on this
board: one `ALTER TABLE`, no coexistence window, since no existing code path
reads either new column until this same branch's handler and frontend
changes ship alongside it. `followers`/`engagement`/`follower_count` are
all left untouched — this migration adds no column that already holds
meaning, only the metadata describing when the reused pair was last
touched.

## Runtime and locks

Two `ADD COLUMN`s, neither with a computed default (`IF NOT EXISTS`,
nullable, no `DEFAULT` expression) — metadata-only catalog changes in
Postgres 11+, no table rewrite, no per-row write. No backfill `UPDATE` at
all (contrast `ENG-008`, which needed one for its boolean split) — every
row simply starts `NULL` on both new columns, which is the correct "never
set" state, not a value to compute. A brief `ACCESS EXCLUSIVE` catalog lock
is taken for the `ALTER TABLE` itself, standard and momentary at 306 rows.

## Backfill

None. `social_stats_updated_at IS NULL` on every row after this migration
is exactly correct — it's the "no human has entered a figure yet" state,
and inventing a value (e.g. defaulting it to `now()`) would falsely claim
staff had reviewed all 306 rows on migration day. Same reasoning the
architect design's Alternatives section already applied to rejecting a
backfill of `followers` itself from `follower_count`'s self-reported bands.

## Rollback

```sql
ALTER TABLE influencers
  DROP COLUMN IF EXISTS social_stats_updated_at,
  DROP COLUMN IF EXISTS social_stats_platform;
```

Should be paired with reverting the handler additions (`EDITABLE_FIELDS`,
the `updateInfluencer` validation blocks, and the new
`getInfluencerActivity` function/route in `admin-portal/handlers/
influencers.ts`) and the frontend additions in `src/pages/Influencers.tsx`
in the same rollback — same hard three-way dependency `ENG-008`'s own
rollback note already established for this file pair. `followers` and
`engagement` themselves need no rollback step; this migration never adds a
default or constraint to either, so dropping the two new columns alone
returns the table to exactly its pre-`ENG-009` shape. `follower_count` is
never written by this ticket and needs no rollback consideration at all.

## Verification actually performed this pass

No live/staging Postgres CLI reachable from this host (no `docker`, no
`psql`, no `supabase` CLI) — same repo-wide gap `ENG-007`'s, `ENG-008`'s,
`ENG-011`'s, and `ENG-013`'s migration docs each already recorded, so the
statement itself has not been executed anywhere. What was verified instead,
via the same read-only Supabase MCP connection:

- `information_schema.columns` on `influencers`, scoped to the six columns
  this ticket's design and handler touch or read
  (`social_stats_updated_at`, `social_stats_platform`, `followers`,
  `engagement`, `follower_count`, `updated_at`) — confirms the reused pair's
  types and defaults match what the handler validates against
  (`followers integer DEFAULT 0`, `engagement numeric DEFAULT 0`), and
  confirms neither new column name collides with anything already on the
  table.
- `list_migrations` — confirmed production's actual applied head and that
  this migration's chosen timestamp sorts after every applied migration and
  after both sibling tickets' still-pending ones, avoiding the same
  filename/timestamp collision `ENG-008`'s own migration doc named as a risk
  against `ENG-013`.
- RLS: not re-queried this pass (the architect design's same-day read of
  `influencer_invitations`'s policy set is trusted rather than re-verified
  hours later on a table nothing else has touched) — the consequence of
  this constraint being wrong would be `getInfluencerActivity` silently
  returning empty data via the anon path, not a security gap, since the
  handler unconditionally uses `auth.adminSupabase` regardless of what the
  policy turns out to be.

**Deliberately not done, and why:** dry-running the `ALTER TABLE` on a
throwaway Supabase branch was not attempted — `create_branch` is gated
behind a real recurring charge (`confirm_cost`), and applying DDL directly
to production ahead of this ticket's own PR/review would jump the L1
human-merge gate. Not this pass's call to make unilaterally. A two-column
additive `ALTER TABLE` with no default expression and no backfill is
smaller in scope than `ENG-008`'s own same-table migration (which added a
`NOT NULL DEFAULT` column and ran a full-table `UPDATE`) and that one
already reached a `pass` verdict on this identical host constraint.

## Migration file

`supabase/migrations/20260830100000_add_influencer_social_stats.sql` in
`aiorders-api`, on branch `feat/ENG-009-influencer-engagement-info` (based
on `ENG-008`'s branch — see the ticket log for why). Timestamp chosen after
the latest applied migration and after both `ENG-008`'s and `ENG-013`'s
pending ones, confirmed via `list_migrations` above. Header comment style
matches the surrounding migrations in this directory.

## Gate verdict

**pass.** Additive-only: two nullable columns, no default expression, no
backfill, no constraint. No RLS change (reads go through the service-role
client that already bypasses it for every other `admin-portal` write/read).
No new query path beyond one indexed single-row `UPDATE` and one unfiltered,
un-indexed `SELECT` over an 809-row table grouped in memory — no index need
at current or foreseeable scale. The one open gap — the statement has not
executed against any live Postgres — is named rather than assumed away,
consistent with every other migration gate on this instance to date.
