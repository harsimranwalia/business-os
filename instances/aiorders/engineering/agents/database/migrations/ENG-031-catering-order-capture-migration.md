# ENG-031 — action_type + selections on public.catering

**Project:** aiorders-api
**Migration file:** `supabase/migrations/20260903130000_add_order_capture_to_catering.sql`
**Branch:** `feat/ENG-031-catering-order-capture-migration`

## The numbers

No live Postgres or Supabase MCP connection reachable this pass (no `docker`,
`psql`, or `supabase` CLI on this host, and no Supabase MCP server configured
in this session — the same host limitation `ENG-007`/`ENG-011`/`ENG-013`'s
migration docs recorded, minus the MCP fallback those three had). Relying
instead on the design's own stated volume
(`agents/architect/designs/ENG-016-catering-quote-generator.md` → `## Data`):
catering submissions are "a low-hundreds-per-year lead volume, not an event
stream," with `selections` capped at 200 items / 500 chars per note at the
request boundary (ENG-033's job, not this migration's), so worst case is
single-digit KB per row. `ADD COLUMN` with no `DEFAULT` is a metadata-only
catalog change in Postgres regardless of table size — no table rewrite, no
full-table lock — so the row count would not change this ticket's plan even
if it were larger.

## Design for the query, not the diagram

No new query path. `selections` is only ever read via the parent row
(`get_catering_requests`, already filtered on `restaurant_id`/`archived`);
`action_type` is not queried by anything in this ticket. Both columns are
write-only from this migration's perspective until `ENG-033`'s edge function
starts populating them.

## Constraint choice

Nullable, no default, no `CHECK`, no enum type — deliberate, per the design.
`catering-request` is a public, unauthenticated POST; a malformed third-party
payload (GoHighLevel or otherwise) must fail *open* on these two fields, not
fail the insert. Validation of `action_type`'s two literals and `selections`'
shape happens at the edge-function boundary (`ENG-033`), not the database.
Column comments are the only schema documentation `public.catering` has (no
tracked `CREATE TABLE`), so both columns carry one, matching
`20260807000001_add_heard_about_us_to_catering.sql` (plain text comment) and
`20260807000002_add_catering_to_restaurant_website.sql` (shape-in-comment for
the jsonb column).

## Expand/contract sequence

Single step, additive-only: two `add column if not exists` statements in one
migration. No coexistence window beyond "the columns exist and are null" —
nothing reads or writes them until `ENG-033` ships. This migration must land
before `ENG-033`'s edge function deploys (its INSERT will conditionally
include both fields; deploying the function first means the INSERT fails on
a missing column) — the same deploy-order rule
`20260807000001_add_heard_about_us_to_catering.sql`'s header states for
`heard_about_us`, repeated in this migration's own header comment.

## Index

None. `selections` is read only via the parent row; `action_type` isn't
queried by anything in this ticket or its known siblings (`ENG-032`,
`ENG-033`, `ENG-034`). Table is nowhere near the ~10k-row threshold that
would make either worth reconsidering (see The numbers).

## Runtime and locks

Two `ADD COLUMN` statements, neither with a `DEFAULT`: catalog-only changes,
brief `ACCESS EXCLUSIVE` lock, no table rewrite, no per-row work, near-instant
at any table size. No online strategy or maintenance window needed.

## Backfill

None. Every existing row gets `null` for both columns, which is the correct
value — "not captured under the new flow" — not a placeholder needing a
follow-up fill.

## Rollback

```sql
alter table public.catering drop column if exists action_type;
alter table public.catering drop column if exists selections;
```

Safe standalone, unlike a column already in active use: nothing reads or
writes either column until `ENG-033` ships, so this rollback has no
paired-revert dependency as long as it runs before `ENG-033`'s branch merges.
Once `ENG-033` ships, rolling back this migration must happen together with
reverting `ENG-033`'s handler changes — reading/writing a dropped column
would break that function.

## Verification actually performed this pass

No live database access this session (see The numbers). What was verified
from the repo instead:

- `grep -rn "action_type\|selections" supabase/migrations/` before writing
  found no prior migration already defining either column on
  `public.catering` — no naming collision.
- `grep -rln "action_type\|selections" supabase/functions/` found no
  existing reference anywhere in the function tree — confirms the design's
  own statement that this ticket is inert until `ENG-033` starts writing to
  it.
- New migration's timestamp (`20260903130000`) sorts after the latest
  on-disk migration (`20260903120000_backfill_onboarding_show_in_marketplace.sql`)
  — no ordering collision.
- Migration text checked line-by-line against both cited templates:
  `20260807000001_add_heard_about_us_to_catering.sql` (deploy-order header
  wording, `add column if not exists`, comment-per-column) and
  `20260807000002_add_catering_to_restaurant_website.sql` (shape-in-comment
  convention for a jsonb column) — matches both.

**Deliberately not done, and why:** the statement has not executed against
any live or staging Postgres. No CLI reachable from this host, no Supabase
MCP connection in this session, and applying DDL ahead of this ticket's own
PR/review would jump the L1 human-merge gate — not this pass's call to make
unilaterally. Same reasoning `ENG-007`/`ENG-011`/`ENG-013` recorded. Lower
residual risk than any of those three: two `add column if not exists`
statements, both nullable, no default, no `CHECK`, no rewrite, is about as
small as a schema change gets.

## Migration file

`supabase/migrations/20260903130000_add_order_capture_to_catering.sql` in
`aiorders-api`, on branch `feat/ENG-031-catering-order-capture-migration`,
committed `06e8e84` and pushed to `origin`. No PR opened yet — L1 autonomy
opens the PR at release-readiness (`skills/release-runner/SKILL.md`), not at
`building`.

## Gate verdict

**pass.** Additive-only, nullable, no default, no `CHECK`, no enum, no
index, no backfill, no destructive change, no rename. The one open gap — not
executed against a live database — is named rather than assumed away, and is
smaller in kind than the gaps `ENG-007`/`ENG-011`/`ENG-013` each accepted for
statements with materially more surface (a `CHECK` constraint, a
`DROP FUNCTION`/`CREATE FUNCTION` pair, a foreign-key-adjacent identity
merge).
