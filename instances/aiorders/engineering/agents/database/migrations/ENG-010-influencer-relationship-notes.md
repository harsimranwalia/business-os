# ENG-010 — influencer_notes (new table)

**Project:** aiorders-api
**Migration file:** `supabase/migrations/20260902120000_create_influencer_notes.sql`
**Branch:** `feat/ENG-010-influencer-relationship-notes` (based on `ENG-009`'s branch,
`d37e0c9` — see the ticket log for why)

## What was and wasn't verified this pass

No Supabase MCP tool was available in this session (checked via `ToolSearch`
before starting — absent from the deferred-tool list this pass), unlike
`ENG-008`/`ENG-009`, which both re-verified live schema state through it
immediately before writing their migrations. That live check was not
possible here, and this doc says so rather than presenting the same
confidence level as those two docs on unequal evidence.

What was checked instead, statically:

- `supabase/migrations/` on disk (`ls | tail`) — latest migration is
  `20260830100000_add_influencer_social_stats.sql` (`ENG-009`'s own,
  unapplied); nothing dated `20260902` exists yet, so this migration's
  timestamp doesn't collide.
- `grep -rl "influencer_notes"` across `supabase/` — zero hits anywhere in
  tracked migrations or function code, confirming no prior migration
  already created this table or a colliding name under a different one.
- The architect design doc's own live-schema evidence (`agents/architect/
  designs/ENG-010-influencer-relationship-notes.md`, read this same
  session, itself confirmed against the live project on 2026-08-29):
  `influencers(id uuid primary key ...)` and `profiles(id uuid primary
  key ...)` both exist, which is what this migration's two foreign keys
  need to resolve. Trusted rather than re-verified hours/days later,
  same as `ENG-009`'s migration doc trusted the architect's same-day RLS
  reading for `influencer_invitations` rather than re-querying it.

**Why the gap matters less here than it would for an `ALTER TABLE`:** this
migration only creates a new table with two foreign keys into tables two
prior migrations on this same board already confirmed live. It reads
nothing from and writes nothing to any existing column, so there is no
existing-data shape to get wrong the way a new `ALTER ... ADD COLUMN` with a
default or backfill could. The one way this could still fail is if
`influencers.id` or `profiles.id` were not actually `uuid` live despite the
migrations directory saying so — not verified live this pass, flagged here
rather than assumed away.

## Design for the query, not the diagram

New, isolated table — not an extension of `influencers` itself, since notes
are an independently-growing list/append sub-resource (no field-level
PATCH), not another field on the influencer record. See the architect
design's Alternatives section for why a generic polymorphic `notes` table
was rejected in favor of this influencer-only one (nothing else in this
codebase has a notes concept yet).

Reads: `GET /admin-portal/influencer-notes?influencer_id={id}` —
`SELECT ... WHERE influencer_id = $1 ORDER BY created_at DESC`, served by
the new `influencer_notes_influencer_id_idx` composite index (matches the
query's own filter + sort columns exactly, so no separate sort step).
Writes: `POST /admin-portal/influencer-notes` — a single-row `INSERT`,
`author_id` always taken from the authenticated session
(`admin-portal/handlers/influencer-notes.ts`), never from the request body.

## Constraint choice

Both foreign keys (`influencer_id`, `author_id`) are `not null` — a note
with no subject or no author isn't a note this feature can produce, since
the handler requires both before ever reaching the insert. No `CHECK` on
`body` beyond `not null`; the handler enforces "non-empty after trim" in
the write path (matching this repo's existing convention, already noted in
`ENG-009`'s own migration doc, of doing string-shape validation in the
handler rather than a schema `CHECK`). No length cap on `body` — unlike
`social_stats_platform`'s handler-enforced 32-character cap, the design
doesn't call for one on a freeform relationship-notes field, and adding one
speculatively would be validating a scenario the PRD never named.

## Expand/contract sequence

Single step. A brand-new table has no existing reader to coexist with —
the handler and frontend that read/write it ship in this same branch, so
there's no window where code expects the table before it exists or after
some future removal.

## Runtime and locks

`CREATE TABLE IF NOT EXISTS` plus one `CREATE INDEX IF NOT EXISTS` on a
table with zero rows at creation time — no lock contention on any existing
table, no rewrite, no per-row cost. Cheaper than either of `ENG-008`'s or
`ENG-009`'s migrations, neither of which had the option of starting empty.

## Backfill

None, and none is possible — there is no prior notes data anywhere in this
codebase to migrate (confirmed absent, see the architect design's own
Evidence section: grepped for any existing `notes`/`influencer_notes`
concept, no hit).

## Rollback

```sql
drop table if exists influencer_notes;
```

Should be paired with reverting the handler
(`admin-portal/handlers/influencer-notes.ts`), its route registration in
`admin-portal/index.ts`, and the frontend Notes section in
`src/pages/Influencers.tsx` in the same rollback — same three-way
dependency shape `ENG-008`'s and `ENG-009`'s own rollback notes already
established for this file pair, extended to the one new file this ticket
adds. Nothing else in the codebase reads or writes `influencer_notes`, so
the drop has zero blast radius elsewhere — no existing table is altered by
this migration at all.

## Verification actually performed this pass

No live/staging Postgres CLI reachable from this host (no `docker`, no
`psql`, no `supabase` CLI) — same repo-wide gap `ENG-007`'s, `ENG-008`'s,
`ENG-009`'s, `ENG-011`'s, and `ENG-013`'s migration docs each already
recorded, so the statement itself has not been executed anywhere. Combined
with the missing MCP tool noted above, this migration's live-schema
verification is weaker than every prior ticket's on this board — named
plainly rather than dressed up as equivalent.

**Deliberately not done, and why:** a throwaway Supabase branch dry-run was
not attempted, same reasoning `ENG-009`'s doc already recorded (gated
behind a real recurring charge via `confirm_cost`, and applying DDL
directly to production ahead of this ticket's own PR/review would jump the
L1 human-merge gate) — not this pass's call to make unilaterally.

## Migration file

`supabase/migrations/20260902120000_create_influencer_notes.sql` in
`aiorders-api`, on branch `feat/ENG-010-influencer-relationship-notes`
(based on `ENG-009`'s branch). Timestamp chosen after the latest migration
on disk (`20260830100000`), confirmed via a directory listing rather than
`list_migrations` (unavailable this pass — see above). Header comment style
matches the surrounding migrations in this directory.

## Gate verdict

**pass, evidence narrower than precedent and said so above.** Additive-only:
one new table, two `not null` foreign keys into tables this migration
doesn't modify, one composite index matching the only query shape this
feature has, no default expression, no backfill, no change to any existing
table, column, or RLS policy. The two open gaps — no live Postgres reachable
from this host, and no MCP-based live-schema re-verification this specific
pass — are both named rather than assumed away; neither changes the verdict,
since a new, isolated table with foreign keys into two already-live tables
carries less risk than either prior ticket's `ALTER TABLE` on this same
board, both of which already passed this gate on this identical
unreachable-Postgres constraint.
