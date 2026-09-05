# ENG-037 — broadcast_campaigns / broadcast_campaign_steps / broadcast_campaign_recipients + dispatch cron

**Project:** aiorders-api
**Migration file:** `supabase/migrations/20260904140000_broadcast_campaigns.sql`
**Branch:** `feat/ENG-037-broadcast-campaigns-schema-and-dispatch-cron`

## The numbers

Unlike `ENG-031`/`ENG-007`/`ENG-011`/`ENG-013`'s own passes (all recorded "no
docker, psql, or supabase CLI on this host"), **this host has both**, and the
CLI is already linked and authenticated to `aiorders-api`
(`bmnmnejwdxbcqinqkwko`, confirmed via `supabase projects list`). Recorded
in `agents/database/notebook/` so future tickets check this before assuming
repo-grep is the only option.

Three brand-new tables, zero existing rows — "the numbers" that matter here
are the projected write rate, not current volume: `broadcast_campaign_recipients`
is a fan-out (one row per customer per step), so a large restaurant's
one-time send to its full customer list is this schema's actual load case.
No number available yet for typical restaurant customer-list size on this
platform; not blocking, since every new-row path here is a plain indexed
insert/update, not a scan.

## Design for the query, not the diagram

Two hot paths, both already indexed by this migration:
- Dispatcher's every-5-minute claim: `WHERE status = 'pending' AND due_at <=
  now()` → `(status, due_at)` btree, leftmost-prefix match on both predicates.
- Report's per-campaign aggregation: `WHERE campaign_id = ?` → `(campaign_id)`
  btree on both `steps` and `recipients`.
- `list_broadcasts`' per-restaurant list: `WHERE restaurant_id = ?` →
  `(restaurant_id)` btree on `broadcast_campaigns`, matching the same access
  pattern `customers_restaurant_id_idx`/`api_keys_restaurant_id_idx` already
  index on this project. Not explicitly named in the design's own Data
  section, but the design's Interfaces section names `list_broadcasts` as a
  paginated per-restaurant query, and no multi-tenant table on this project
  ships without one — added here rather than left for a follow-up.

## Verification against the live project (this ticket's own explicit job)

Ran read-only against the linked live project this pass — schema-only
(`supabase db dump --linked --schema public`) plus two single-value/single-row
queries, never a customer-data scan:

- **`orders.promos`' exact internal key (`ADR-019`).** Confirmed from the
  live dump: `"promos" "jsonb"[] NOT NULL` — a **Postgres array of jsonb**
  (`jsonb[]`), not a `jsonb` column holding a JSON array. This distinction
  matters for `ENG-038`'s query shape: unnesting/indexing a native array
  (`unnest(promos)`, `promos[1]`) is not the same call as
  `jsonb_array_elements()` on a single jsonb column. Sampled one non-empty
  row (`SELECT promos FROM orders WHERE array_length(promos,1) > 0 LIMIT 1`,
  one column, one row, no customer/order identifying data pulled): each
  element is a full CloudWaitress promo-definition object, matching a coupon
  code via its **`code`** key (e.g. `{"code": "10 Off", "percent_discount":
  10, "stats": {"used": 671}, ...}` — the promo's own metadata snapshot at
  order time, not a bare code string or a foreign id). `offers.coupon_code`
  (confirmed `text`, nullable, on the live `offers` table) is what
  `ENG-038`'s ROI query matches against `promos[n]->>'code'` across the
  unnested array, per element — **not** a `promos @> '["CODE"]'` style
  containment check, which would assume a plain string array and silently
  match nothing. Documented as a column comment on `broadcast_campaigns.offer_id`
  in the migration itself, so this doesn't have to be re-derived when
  `ENG-038` starts building.
- **`communication_log`'s exact column set.** Confirmed from the live dump:
  `reference_type`/`reference_id` (both `character varying`, matching the
  design's `reference_type: 'broadcast_campaign'`, `reference_id:
  campaign.id` plan exactly — `campaign.id` is `uuid`, `reference_id` is
  varchar, so `ENG-038` casts on write, same as every other existing
  `reference_id` writer already must), plus `channel`, `status`,
  `provider_message_id`, `opened_at`, `clicked_at` — all present, all
  matching the design's stated read plan for the report's email open/click
  figures. No migration needed here; confirms the design's "unchanged" claim
  rather than assuming it.
- **`orders(restaurant_id, created_at)` index — presumed present, design
  said raise a separate item if missing.** Not missing, and not literally
  named either: `idx_orders_analytics_optimized` already covers
  `(restaurant_id, created_at, total_amount, tip_amount, order_type)` —
  `restaurant_id, created_at` as its leading two columns satisfies (and
  exceeds) the presumed index under Postgres's leftmost-prefix rule. No
  proposal filed; nothing missing to raise. Read literally, "raise a
  separate ticket" in the ticket's own Outcome section would mean creating a
  new board ticket directly — not followed even hypothetically, since
  `eng_build_loop.md` step 3 routes a database-agent-originated finding
  through `proposals.md`, not a direct ticket; moot here since there was
  nothing to raise.

## Constraint choice

- `type`/`status`/`audience_mode`/recipient `status`: `CHECK (... IN (...))`
  over the design's own enumerated literal sets — no enum type, matching
  this project's existing convention (`offers.offer_type`/`application_context`
  use the same plain-`CHECK` shape, not a Postgres enum, anywhere on this
  project).
- `broadcast_campaigns_audience_param_check`: ties `audience_mode` to
  `audience_inactive_days` (`inactive_days` mode requires a positive value;
  `all` mode requires null) — a direct database-level enforcement of a rule
  otherwise only implied in prose ("audience mode and its parameter").
  Tested against both the failing and passing case in the disposable
  container (below).
- **No cross-column CHECK requiring at least one of `email_body`/`sms_body`
  on a step**, even though the design's own Interfaces section states
  `create_broadcast` "validates... at least one channel populated per step."
  Deliberately not mirrored into the schema: the design also says this
  table's content columns are "same shape as `communication_templates`' own
  email/SMS content fields, for consistency" — and `communication_templates`
  itself (`email_subject`/`email_body`/`sms_body`, all nullable, no
  cross-check, gated instead by separate `email_enabled`/`sms_enabled`
  booleans) carries no such constraint. Matching the precedent the design
  itself named beats inventing a stricter one; the validation stays exactly
  where the design's own Interfaces section already puts it — the
  `create_broadcast` action, `ENG-038`.
- `email_subject varchar(255)` / `sms_body varchar(320)` (not plain `text`):
  copied byte-for-byte from `communication_templates`' own column types, per
  the same "same shape" instruction. `email_body` stays `text`, also
  matching `communication_templates`.
- `broadcast_campaign_steps_order_unique unique (campaign_id, step_order)`:
  not explicitly requested by the design, but a drip sequence with two steps
  claiming the same order is a data-integrity hole no application check
  alone should be trusted to close — cheap, and exactly the kind of
  constraint-in-the-database-not-only-the-application `database`'s own
  charter asks for.
- **RLS enabled, zero policies, on all three new tables** — not requested by
  the design's Data section, but a direct, cheap match to this project's own
  established convention for a service-role-only table
  (`20260821000001_create_api_keys.sql`'s `alter table ... enable row level
  security` + "No policies: only the service-role key... can read/write this
  table" comment, copied verbatim in intent). No caller in the design's own
  Interfaces section reaches these three tables with anything but a
  service-role bearer (`brand-portal` actions, `broadcast-dispatch` — both
  service-role); RLS with no policies costs nothing on that access pattern
  and closes the exact class of gap this project's own security reviews have
  flagged twice already this week (`ENG-015`, `ENG-022`, and the still-open
  RLS-verification note on `ENG-031`'s own security review). Pre-empting
  this here rather than leaving it for `in-security` to find.

## Open question for `ENG-038`, named rather than guessed

The design's Interfaces section says `get_broadcast_report` returns "counts
by status and channel **from `broadcast_campaign_recipients`**" — but the
same design's Data section states, twice, unambiguously, "one row per
(campaign, step, customer)" for that table, with no channel dimension. A
step can carry both `email_body` and `sms_body` at once, so a single
recipient row cannot itself carry a single "channel" value without
contradicting the stated one-row-per-triple shape. **No `channel` column was
added here** — the explicit, twice-stated grain wins over one ambiguous
parenthetical elsewhere in the same document. `ENG-038` resolves this by
either deriving "channel" via a join to `broadcast_campaign_steps` (which
`email_body`/`sms_body` is non-null) or reading `communication_log` directly
(which already has a real `channel` column, keyed by this migration's own
`reference_type`/`reference_id` convention) — named here so it's a decision,
not a rediscovery.

## Expand/contract sequence

Additive-only, single migration: three new tables, one new cron job, nothing
existing touched. No coexistence window beyond "the tables exist and are
empty" — nothing reads or writes them until `ENG-038` ships, matching the
design's own Rollout order exactly (migration → functions → frontend).

## Runtime and locks

Three `CREATE TABLE IF NOT EXISTS` (no existing data, no rewrite), five
`CREATE INDEX IF NOT EXISTS` (new tables, empty — no `CONCURRENTLY` needed;
nothing else has ever seen these table names), one trigger, three `ENABLE
ROW LEVEL SECURITY` (all metadata-only), two `CREATE EXTENSION IF NOT
EXISTS` (already installed live, both idempotent no-ops), one
`cron.schedule`. No table over rows, no lock contention possible against a
table nothing else references yet. Near-instant at any point this migration
could run.

## Backfill

None — three new tables, nothing to backfill into.

## Rollback

```sql
select cron.unschedule('broadcast-dispatch-tick');
drop table if exists public.broadcast_campaign_recipients;
drop table if exists public.broadcast_campaign_steps;
drop table if exists public.broadcast_campaigns;
```

**Actually run, not just asserted** — against the disposable container
described below: unschedule returned `t`, all three drops succeeded, and a
post-drop check confirmed zero `broadcast_campaign*` relations and zero
matching `cron.job` rows remained. Safe any time before `ENG-038` ships
(nothing reads or writes these tables before then); once `ENG-038` ships,
rolling back must happen together with reverting `ENG-038`'s own changes,
same caveat `ENG-031`'s plan recorded for its own columns.

## Verification actually performed this pass

**Against the live project (read-only, schema and two narrowly-scoped
queries — see "Verification against the live project" above).**

**Against a disposable local replica** (new this pass — the tooling gap that
kept `ENG-031`/`ENG-007`/`ENG-011`/`ENG-013` to repo-grep-only doesn't exist
on this host): a fresh `supabase/postgres:15.8.1.073` container (the same
image `supabase db start` itself uses), seeded with a minimal stand-in for
the three live tables this migration actually references
(`restaurants(id)`, `customers(id, restaurant_id, consent_sms,
consent_email)`, `offers(id, restaurant_id, coupon_code)`, `auth.users` —
pre-shipped in the image — plus a copy of the live `update_updated_at_column()`
function body). **Not** a full replay of this repo's tracked migration
history: that path was tried first and fails independent of this ticket —
`20250729143357_initial_restaurant_rls.sql`, the earliest tracked migration,
assumes `public.restaurants` already exists, confirming in a second, more
direct way the same gap `ADR-006`/`ENG-020`'s design already recorded
(`customers`/`offers`/`orders`/`communication_log` are all created outside
any tracked migration) — this repo cannot be replayed from empty by any
ticket, not a limitation specific to this one.

Against that replica, applied the real migration file unmodified and
confirmed, by direct query rather than by reading the SQL back:
- All three tables created, `relrowsecurity = t` on all three.
- All five indexes created with the exact column lists intended (`\d`-
  equivalent `pg_indexes` read, not assumed from the file).
- `cron.job` carries `broadcast-dispatch-tick`, schedule `*/5 * * * *`, `active = t`.
- `broadcast_campaigns_audience_param_check` rejects `('all', 5)` — confirmed
  by an actual failing insert, not just read from the constraint definition.
- A real insert (valid restaurant FK, `audience_mode = 'all'`) succeeds,
  defaults to `status = 'draft'`; a subsequent `UPDATE` bumps `updated_at`
  past `created_at` — the trigger fires, confirmed by comparing the two
  timestamps in the query result, not assumed from the `CREATE TRIGGER`
  statement.
- `broadcast_campaign_steps_order_unique` rejects a second `step_order = 0`
  row on the same campaign — confirmed by an actual duplicate-key error.
- Rollback executed and confirmed clean (see Rollback above).

Container removed after the test (`docker rm -f`); nothing left running.

**Deliberately not done:** the `cron.schedule` call was verified to
*register* correctly (`cron.job` row present, correct schedule string); the
job was not left running long enough to actually fire, since firing it would
call a `broadcast-dispatch` URL that doesn't exist yet (`ENG-038`) — a
no-op-by-construction test, not a gap.

## Migration file

`supabase/migrations/20260904140000_broadcast_campaigns.sql` in
`aiorders-api`, on branch `feat/ENG-037-broadcast-campaigns-schema-and-dispatch-cron`,
branched fresh from `origin/main` tip (`5415ef0`, confirmed current via
`git fetch` — the shared `_eng/aiorders-api` worktree was mid-checkout on an
unrelated ticket's already-pushed branch, `ENG-033`, at pass start; switched
away safely since nothing was uncommitted there beyond the same
long-standing stray `deno.lock` three prior passes have already independently
noticed).

## Operational prerequisite — not this migration's to complete

The cron job's `net.http_post` call authenticates via `Authorization: Bearer
<key>`, where `<key>` is read from Vault by name
(`(select decrypted_secret from vault.decrypted_secrets where name =
'service_role_key')`), matching `ADR-016`/`ADR-017`'s stated requirement
that `broadcast-dispatch` (`ENG-038`) checks this header. **No existing
migration in this repo authenticates a `pg_cron` → `net.http_post` call at
all** — the only prior cron job, `platform_analytics_cron`, sends none — so
this is a new pattern for this repo, chosen because Vault is already live
here (`resend_api_key` exists; confirmed via `SELECT name FROM vault.secrets`,
names only, no secret value ever read) rather than inventing a different
mechanism.

The secret itself does not exist yet (confirmed by the same query) and this
pass cannot create it — the real service-role key value isn't something
this session has or should handle. **Someone with that key runs, once,
outside any tracked migration:**
```sql
select vault.create_secret('<the real service_role key>', 'service_role_key',
  'used by broadcast-dispatch-tick to authenticate its call to broadcast-dispatch');
```
Until then the cron tick's header evaluates to a null bearer and every call
gets a 401 from `broadcast-dispatch`'s own auth check — harmless while these
tables are empty (nothing queued, nothing lost), same "no-op until ENG-038
ships" safety the design's own Rollout section already establishes for the
tables themselves. Must be done before the first real campaign is expected
to send, not before `ENG-037` or `ENG-038` can ship.

## Gate verdict

**pass.** Three additive tables, no existing table touched, every column
traced to either the design's Data section or its Interfaces section (the
one gap between them — `broadcast_campaigns.name` — resolved from the more
specific Interfaces section rather than guessed), every foreign-key target
confirmed live rather than assumed, the one open ADR-019 risk (`orders.promos`'
internal shape) resolved with an actual sample rather than left open,
rollback actually executed rather than asserted, and the one real
schema-adjacent gap this pass found (authenticating the cron call) named as
a concrete, bounded, non-blocking operational prerequisite rather than
silently worked around or silently skipped.
