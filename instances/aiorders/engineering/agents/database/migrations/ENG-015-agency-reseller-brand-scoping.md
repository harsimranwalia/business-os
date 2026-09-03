# ENG-015 — partner INSERT policy on `restaurants`

**Project:** aiorders-api
**Migration file:** `supabase/migrations/20260903120000_partner_restaurant_insert_scoping.sql`
**Branch:** `fix/ENG-015-agency-reseller-brand-scoping`

## The numbers

No schema change — this migration adds one RLS policy, no column, no table,
no index. `brands` and `restaurants` row counts were not available this pass
(no live DB tool reachable — see Verification below), but both are
tenant/location-count-bounded tables (one row per registered brand or
restaurant location on the platform), not per-user or per-event tables —
structurally nothing like the volumes that make a missing index urgent.

## Design for the query, not the diagram

The policy's `WITH CHECK` runs two `EXISTS` subqueries, both on `INSERT`
only (low frequency, not a hot read path):

- `profiles WHERE id = auth.uid() AND role IN (...)` — `id` is the primary
  key, so this is a single-row PK lookup regardless of `profiles` size.
- `brands WHERE brands.id = restaurants.brand_id AND brands.partner_id =
  auth.uid()` — filtered first on `brands.id` (primary key, unique), so
  this is also effectively a PK lookup; the `partner_id` clause narrows a
  result set that's already at most one row.

Separately, the **handler-code** change (`getPartnerBrandIds` in
`restaurants.ts`, same ticket) runs `brands WHERE partner_id = $1` —
this one *is* a new query pattern on `brands` filtered by `partner_id`
directly, not by primary key, on every `GET`/`PUT` a partner makes against
this handler. Checked for precedent: `proxy-login/index.ts` queries
`brands` by `id` then compares `partner_id` in application code, which is
a different access path and gives no evidence either way about an index.
No tracked migration creates `brands` at all (ADR-006's untracked-schema-history
finding, confirmed again here) or indexes `partner_id`. Flagged, not
blocking: `brands` is one row per registered brand/agency, not a
consumer-scale table, and this handler's own call frequency (partner
portal usage) is low relative to the platform's real hot paths. If `brands`
ever grows into the thousands, add `CREATE INDEX ON brands(partner_id)` —
cheap, additive, no migration risk — but nothing here requires it today.

## Why a policy, not a broader RLS rework

Considered and rejected in the design
(`agents/architect/designs/ENG-015-agency-reseller-brand-scoping.md` →
Alternatives, `ADR-006`): branching to the RLS-scoped client for reads,
mirroring `brands.ts`, was traced to return **zero rows** for a partner
today — `restaurants`' live SELECT policies grant a partner nothing, and
`brands`' own RLS state can't be verified from this repo at all. Enforcing
brand-scope in code (already-shipped handler change, same ticket) sidesteps
depending on either table's RLS for the read/update side entirely. This
migration is the one place RLS *is* the enforcement boundary — because
`AddRestaurantModal.tsx` inserts directly through the ambient RLS-scoped
client, never through the edge function — so it has to be a real policy,
not another code-side check.

## Constraint choice

`WITH CHECK (approved = false AND EXISTS(...) AND EXISTS(...))`. The
`approved = false` clause is a hard, un-bypassable default (AC5) — a client
that sends `approved: true` directly is rejected outright, not silently
corrected, which is why `AddRestaurantModal.tsx` also had to change in the
same ticket (a partner insert with the old `approved: true` hardcode would
now fail closed instead of landing auto-approved). Role check is
`profiles.role IN (...)` only, deliberately matching the existing "Admins
can manage all restaurants" policy's own strictness (verified verbatim in
`supabase/migrations/20250729143357_initial_restaurant_rls.sql`) rather
than also checking `additional_roles` — consistency with this table's
nearest sibling policy on this table specifically, not a project-wide
convention.

## Expand/contract sequence

Single step, additive only. A new `FOR INSERT` policy on an already-`ALTER
TABLE ... ENABLE ROW LEVEL SECURITY`'d table adds a new permission; it
removes none. Existing staff inserts are unaffected — they already satisfy
"Admins can manage all restaurants" (`FOR ALL`) and never reach this policy.
No existing row is touched (the check only gates future inserts), so there
is no coexistence window to manage.

## Runtime and locks

`CREATE POLICY` takes a brief catalog-level lock, no table rewrite, no
per-row work, near-instant regardless of `restaurants`' size. No online
strategy or maintenance window needed.

## Backfill

None. Nothing is computed or set on existing rows.

## Rollback

```sql
DROP POLICY IF EXISTS "Partners can add restaurants to their assigned brands" ON public.restaurants;
```

Independent of the handler-code changes in this same ticket — dropping this
policy alone returns partner inserts to their pre-ticket state (silently
rejected by RLS, the original bug), which is a regression but not a break;
unlike `ENG-013`'s column-drop, no other code reads or depends on this
policy's existence to compile or run.

## Verification actually performed this pass

No live/staging Postgres CLI or Supabase MCP connection reachable from this
host this pass (`deno`, `docker`, and the `supabase` CLI binaries are
present, but no authenticated/linked session was available to query the
live project read-only) — narrower than `ENG-007`/`ENG-011`/`ENG-013`'s own
migration docs, which had a working read-only MCP connection at the time.
What was verified instead, directly against this repo's tracked migration
history rather than assumed from the PRD/design's own citations:

- Re-read `supabase/migrations/20250729143357_initial_restaurant_rls.sql`
  in full: confirmed verbatim the exact "Admins can manage all restaurants"
  policy text this new policy's role-check strictness matches, and confirmed
  "Restaurant owners can manage their own restaurant" (`auth.uid() = id`) is
  the only other `INSERT`-capable policy on this table — neither grants a
  partner anything, matching `ADR-006`'s claim.
- Grepped all three RLS-lockdown migrations `ADR-006` cites
  (`20250814065341`, `20250814065439`, `20250814065606`) in full: confirmed
  the `USING (false)` public-SELECT lockdown and the `restaurants_public`
  view exist exactly as described — this migration doesn't touch SELECT at
  all, so that lockdown is unaffected either way.
- Grepped every migration for a policy already named "Partners can add
  restaurants to their assigned brands" — zero matches, no name collision.
- Grepped every migration for `brands`' own `CREATE TABLE` or any index on
  `partner_id` — zero matches, confirming (not just trusting) `ADR-006`'s
  untracked-schema-history claim for this table independently this pass.
- Grepped the live handler code (not migrations) for existing `partner_id`
  query precedent — found one (`proxy-login/index.ts`), different access
  pattern (by `id`, not by `partner_id`), noted above.

**Deliberately not done, and why:** executing the `CREATE POLICY` statement
itself against any live database — same residual gap `ENG-007`/`ENG-011`/
`ENG-013`'s migration docs each carried forward on this host, now also
without the read-only MCP fallback those three had. A single additive
`CREATE POLICY` with no table rewrite is a smaller unverified-execution
risk in kind than a column add or a function drop/recreate, but the gap is
real and named rather than assumed away.

## Migration file

`supabase/migrations/20260903120000_partner_restaurant_insert_scoping.sql`
in `aiorders-api`, on branch `fix/ENG-015-agency-reseller-brand-scoping`.
Timestamp chosen after the latest file on disk
(`20260829190000_add_last_order_at_to_platform_analytics.sql`). Header-comment
style matches the surrounding migrations in this directory.

## Gate verdict

**pass.** Additive-only policy, no schema change, no backfill, no existing
row touched, no coexistence window. The one open gap — no live execution
this pass, and no read-only MCP fallback available either — is named
plainly rather than assumed away, and is smaller in kind (a single `CREATE
POLICY`, no table rewrite) than what prior tickets' gates already accepted
on this same class of host limitation. The `brands.partner_id` query-pattern
flag above is a forward-looking note for the database agent's own notebook,
not a blocker at today's table size.
