# ENG-038 — `claimed` recipient status, `step_id` index, `scheduled_send_at` check

**Project:** aiorders-api
**Migration file:** `supabase/migrations/20260904150000_broadcast_recipients_claimed_status.sql`
**Branch:** `feat/ENG-038-broadcast-composer-dispatcher-unsubscribe`

## Provenance — why this receipt is retroactive

`backend` wrote this migration directly during `ENG-038`'s `building` hop
instead of requesting it through `database` — a process gap release-readiness
caught and returned for (`agents/devops/notebook/2026-09-04-release-readiness-log.md`,
`## ENG-038`), already fully reasoned there and in a filed proposal
(`proposals.md`, 2026-09-04). Not re-litigated here. This receipt answers the
one question that was actually open: **is the migration itself sound** —
independent of whether the right agent wrote it.

## The numbers

Live project (`bmnmnejwdxbcqinqkwko`, linked, confirmed via `supabase projects
list`), checked fresh this pass rather than assumed:

- `supabase migration list --linked` shows `20260904140000` (ENG-037's base
  schema) already applied on the remote — the three broadcast tables are real,
  live tables, not just a local/CI fixture. `20260904150000` (this migration)
  is local-only, not yet pushed — no conflict, nothing to reconcile.
- Row counts, read-only aggregate queries against the linked project (no
  customer data pulled): `broadcast_campaigns` = 0, `broadcast_campaign_steps`
  = 0, `broadcast_campaign_recipients` = 0. Expected: `ENG-038`'s own
  brand-portal actions are the only writer of the first row ever, and that
  code hasn't shipped/deployed yet.
- Growth: none yet, by construction — pre-launch.
- Query frequency / cardinality on what's being indexed (`step_id`): the new
  index supports the referencing side of `broadcast_campaign_recipients
  .step_id`'s `on delete cascade` FK, which Postgres never indexes
  automatically. Current fire rate is zero — no reachable code path deletes a
  step today (`update_broadcast` replaces a campaign's steps by delete-then-
  reinsert only while `status` is `draft`/`scheduled`, before any recipient
  row exists to cascade). The index is defensive against the day a step *does*
  get deleted with recipient rows attached (a drip campaign mid-flight,
  edited) — cheap now, expensive to discover missing later, consistent with
  this same migration family's own established pattern of indexing every FK
  on this table (`campaign_id`, `status`+`due_at`, both from `ENG-037`).
- The `scheduled_send_at` check is a write-time constraint, not a query — no
  frequency/cardinality question applies.

## Design for the query, not the diagram

No new read path. `step_id`'s index exists for a write-side cascade, not a
`SELECT`. The `scheduled_send_at` constraint exists to make an invariant the
dispatcher's own promotion query already assumes (`WHERE status = 'scheduled'
AND scheduled_send_at <= now()`, `dispatch.ts:56-57`) true by construction
instead of by convention.

## Constraint choice

- **`'claimed'` added to `broadcast_campaign_recipients_status_check`** —
  drop-and-recreate the same plain-`CHECK` shape `ENG-037`'s own migration
  already chose over an enum type (this project's established convention).
  Necessary: the dispatcher's atomic claim (`UPDATE ... WHERE status =
  'pending' ... RETURNING`) needs a state that means "claimed, outcome not
  yet known," and none of the four existing terminal values can hold that
  meaning without lying about an outcome that hasn't happened. Widening a
  `CHECK` is additive and reversible as long as no row holds the new value at
  rollback time — true here (table confirmed empty above).
- **`broadcast_campaign_recipients_step_id_idx`** — plain btree, matches this
  table's own existing FK-index convention (`campaign_id`).
- **`broadcast_campaigns_scheduled_requires_time`** — `check (status = 'draft'
  or scheduled_send_at is not null)`. Ties a column that was previously
  nullable-with-no-enforcement to the one status value that's allowed to
  leave it null. Confirmed by reading the application code directly (not
  taken on the build hop's or either review round's word) that this can never
  reject a real write: `createBroadcast` (`brand-portal/broadcasts.ts:311-323`)
  inserts `status: 'scheduled'` and a computed non-null `scheduledSendAt` in
  the same statement — it never inserts `'draft'` at all, so `'draft'` exists
  only as the column's schema-level default, unused by any code path today.
  `updateBroadcast` (`:413-423`) likewise always sets `scheduled_send_at`
  alongside any edit, and only while `status` is still `draft`/`scheduled`
  (`:396-398`). Every later transition — `setBroadcastStatus` (pause/resume,
  `:490-497`), `cancelBroadcast` (`:520-`), and the dispatcher's own
  `promoteDueCampaigns` (`dispatch.ts:53-58`) — updates only `status` (and
  `updated_at`), never touches `scheduled_send_at`, so a row's non-null value
  from creation persists unchanged through every subsequent state. No
  reachable code path can produce the row shape this constraint forbids.

## Expand/contract sequence

Single migration, additive-only: one constraint widened (not narrowed), one
new index, one new constraint on a previously-unconstrained nullable column.
No rename, no column drop, no type change. Old and new application code
coexist trivially — nothing before this ticket ever wrote `'claimed'` or
relied on `scheduled_send_at` being unconstrained, so there is no version of
the deployed application that this migration could break.

## Index

`broadcast_campaign_recipients_step_id_idx` (btree, `step_id`) — see Numbers
and Constraint choice above. No index added or reconsidered for
`broadcast_campaigns_scheduled_requires_time`: it's a row-level check, not a
predicate any query filters on.

## Runtime and locks

Both tables confirmed empty (0 rows, live, this pass). `ALTER TABLE ... DROP/
ADD CONSTRAINT` and `CREATE INDEX` each take a brief `ACCESS EXCLUSIVE` (the
first two) or `SHARE` (the index) lock, but the validation scan behind each —
the part whose duration actually scales with table size — has zero rows to
scan. Confirmed empirically, not just asserted from the row count: all three
DDL statements completed instantly against the disposable replica (below),
and the same replica's `140000` base schema plus this migration together
applied in under a second. No online strategy or maintenance window needed at
any point before `ENG-037`'s tables see real traffic.

## Backfill

None. No existing row of either affected table needs a value for a new
column (no new column added) or needs to satisfy a new constraint
retroactively (zero rows).

## Rollback

```sql
alter table public.broadcast_campaigns drop constraint broadcast_campaigns_scheduled_requires_time;
drop index if exists public.broadcast_campaign_recipients_step_id_idx;
alter table public.broadcast_campaign_recipients drop constraint broadcast_campaign_recipients_status_check;
alter table public.broadcast_campaign_recipients add constraint broadcast_campaign_recipients_status_check
  check (status in ('pending', 'sent', 'failed', 'skipped_opted_out', 'cancelled'));
```

**Actually run this pass, not just asserted** — this is the specific gap
release-readiness returned the ticket for: the migration shipped with this
SQL sitting in a trailing comment, never executed. Closed below.

Safe any time before a real `'claimed'` row exists in production (true now —
table confirmed empty) or before anything depends on the index/constraint
existing. Once `ENG-038` ships and the dispatcher runs against a non-empty
queue, rolling back the `'claimed'` half must happen together with reverting
`ENG-038`'s own claim logic — same paired-revert caveat `ENG-037`'s and
`ENG-031`'s own plans already recorded for their columns.

## Verification actually performed this pass

**Against the live project (read-only only — see Numbers).** Schema-migration
status and three aggregate row counts; no row-level customer data read.

**Against a disposable local replica**, same image and method
`agents/database/notebook/2026-09-04-host-tooling-capability.md` and `ENG-037`'s
own migration doc established (`public.ecr.aws/supabase/postgres:15.8.1.073`,
the image `supabase db start` itself uses): seeded a minimal stand-in for the
tables this migration's FKs/checks touch (`restaurants(id)`,
`customers(id, restaurant_id, consent_sms, consent_email)`,
`offers(id, restaurant_id, coupon_code)` — `auth.users`/`pgcrypto`/`pg_cron`/
`pg_net` are pre-installed in the image itself) plus a copy of the live
`update_updated_at_column()` function body (fetched via `pg_get_functiondef`
against the linked project, not retyped from memory). Applied `20260904140000`
(ENG-037's base schema) unmodified, then `20260904150000` (this migration)
unmodified, both clean.

Then, by direct query and actual failing/succeeding inserts — not by reading
the SQL back:

- A `'claimed'` recipient row **succeeds** post-migration (previously would
  have been a `check_violation`).
- A bogus status (`'bogus_status'`) still **fails** with `check_violation` —
  the widen didn't accidentally open the column up entirely.
- `broadcast_campaign_recipients_step_id_idx` **exists**, confirmed via
  `pg_indexes`, not assumed from the `CREATE INDEX` statement succeeding.
- A campaign with `status = 'scheduled'` and `scheduled_send_at = null`
  **fails** with `check_violation` (the new constraint's actual job).
- A campaign with `status = 'scheduled'` and a real `scheduled_send_at`
  **succeeds** (the constraint doesn't overreach into the valid case).

**Rollback — the gap this receipt exists to close:**

- Ran the exact rollback SQL above against the same replica. All four
  statements succeeded with no error.
- Re-verified behaviourally, not just "it ran clean": a fresh `'claimed'`
  insert now **fails** again (`check_violation` — the status check is back to
  five values), the `step_id` index is **absent** from `pg_indexes`, and a
  `status = 'scheduled'` / `scheduled_send_at = null` campaign **succeeds**
  again (the constraint is gone). All three confirm the rollback actually
  reverses the forward migration's effect, not merely that the DDL executed.
- Final state confirmed empty on all three tables (`campaigns=0, steps=0,
  recipients=0`) — the test left no residue, matching the live project's own
  current state.

Container removed after the test (`docker rm -f`); nothing left running.

## Migration file

`supabase/migrations/20260904150000_broadcast_recipients_claimed_status.sql`
in `aiorders-api`, on branch
`feat/ENG-038-broadcast-composer-dispatcher-unsubscribe`, committed `4f0dccf`
(part of the ticket's original build), already pushed to `origin`. Not yet
applied to the live project (`supabase migration list --linked` — see
Numbers); pushing it live is `devops`'s/the release step's own act, same
precedent `ENG-037`'s release-readiness hop already established for
`20260904140000`, not this gate's to perform.

## Gate verdict

**pass.** Additive-only (one widened `CHECK`, one new index, one new `CHECK`
on a previously-unconstrained column), no destructive change, no rename, both
affected tables confirmed empty live so no backfill and no lock concern at any
realistic size. Rollback actually executed against a disposable replica and
behaviourally confirmed to reverse the migration, closing the specific gap
release-readiness returned the ticket for. Schema/code coexistence confirmed
by reading every write path to `broadcast_campaigns.status` directly (`brand-
portal/broadcasts.ts`, `broadcast-dispatch/dispatch.ts`): no reachable code
produces a row the new constraint would reject.
