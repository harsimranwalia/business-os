# Acceptance — ENG-048 (Loyalty ledger schema, credit function, and cron; `ENG-027` sub-ticket 1 of 2)

## Why this ran in full, not as receipt bookkeeping

`ENG-048` is a work-breakdown child of `ENG-027` with real, checkable
behaviour (a guarded crediting function, not schema-only) — the
`ENG-031`/`ENG-037`-style 0-criteria carve-out doesn't apply. Per the
standing proposal filed 2026-09-04, a ticket with real criteria gets the
skill run in full.

## Scope

Per `agents/eng-manager/notebook/2026-09-07-eng027-work-breakdown.md`'s own
AC-mapping (also recorded on the ticket's own board file), `ENG-048` owns
**AC4, AC5, AC8, AC9, AC12 in full**, plus the guard/crediting half of AC1,
AC2, AC3, AC7, AC11, AC15, AC16 from `ENG-027`'s PRD
(`agents/product-manager/specs/ENG-027-loyalty-points-ledger-and-earn.md`).
The webhook/sweep-caller/dine-in half of those seven belongs to `ENG-049`
(processed in this same pass — see that ticket's own acceptance notebook
entry) — not claimed here alone.

## Check against the live result — not the proxies

`aiorders-api` PR #21 merged directly on GitHub with no written reply
(`decision:` still blank on `inbox/2026-09-07-eng048-merge-request.md`):

```
$ gh pr view 21 --json state,mergedAt,baseRefName,headRefName,mergeCommit
{"baseRefName":"main","headRefName":"feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron",
 "mergeCommit":{"oid":"051feff8b43d9c3fe4a87468bcd7da5f7e935461"},
 "mergedAt":"2026-09-08T18:05:03Z","state":"MERGED"}
```

**Confirmed live, not just merged:** `supabase migration list --linked`
shows `20260907130000` on both `local` and `remote` — the migration actually
executed against the production database, not just landed in `main`. No
edge function of its own to check a version-bump on; the artifact is schema
plus one Postgres function plus one cron job, all created by the same single
migration file.

Read the merged, live-matching source directly
(`supabase/migrations/20260907130000_loyalty_ledger_schema_and_credit_function.sql`),
not any gate's account of it.

## Walk every owned criterion

| AC | Criterion (owned portion) | Checked against | Result |
|---|---|---|---|
| 4 | An order already credited on fulfilment gets no additional credit when its auto-complete window later elapses | `credit_order_if_eligible`'s opening `update orders set loyalty_processed_at = now() where id = p_order_id and loyalty_processed_at is null and status is distinct from 'cancelled' returning *` — a second call (regardless of `fulfillment_reason`) finds zero matching rows once the first has set `loyalty_processed_at`, returns `already_processed` before reaching the insert. Independently re-tested this round per `agents/qa/test-plans/ENG-048.md`'s regression check (`window_elapsed` after `reported`: `already_processed`, ledger count still 1) | **Pass** |
| 5 | Any sequence of repeated/duplicated/out-of-order fulfilment and cancellation reports credits at most once, ever, and a cancellation anywhere means zero credits | Same guard clause — `status is distinct from 'cancelled'` in the same `WHERE` as the idempotency check, one atomic `UPDATE...RETURNING` serializing concurrent callers via ordinary row locking. QA's round-1 concurrent-caller test (webhook + sweep, exactly one credit) unaffected by round 2's diff, not re-tested but not touched either (`git diff 9fccdad 60fa06e` confirmed to leave the guard clause untouched) | **Pass** |
| 8 | Rate used is the one in effect when the order was **placed**, not when credited | `select rlc.online_earn_pct ... where rlc.restaurant_id = v_order.restaurant_id and rlc.effective_from <= v_order.created_at order by rlc.effective_from desc limit 1` — keyed on `v_order.created_at` (placement time), never `now()` | **Pass** |
| 9 | A later rate-config change has no effect on an already-written entry | `rate_applied` is written into the ledger row at insert time as a plain snapshot column (`numeric(5,2) not null`), never recomputed or joined live on read. Append-only table, no `UPDATE`/`DELETE` path exists anywhere in this migration or the function | **Pass** |
| 12 | No linked platform identity → no points, no entry, order itself unaffected | `select ... into v_platform_customer_id from platform_customer_legacy_links ... if v_platform_customer_id is null then return 'skipped_no_identity'` — returns before any `loyalty_ledger_entries` insert and before the `orders.status` update (only `loyalty_processed_at`, a new column with no other reader yet, was touched, by the guard step above). Independently re-traced through real application code by principal-engineer round 1, per QA's own coverage note | **Pass** |

## Check the non-goals / bundling risk

PRD's non-goals (implicit in "Notes"): no backfill of `cw_order_id`/
`loyalty_processed_at` for pre-existing orders, and this function never
updates or deletes a ledger row. Confirmed on the live migration: both new
`orders` columns are plain `add column if not exists` with no backfill
statement; the function has exactly one `insert into loyalty_ledger_entries`
and no `update`/`delete` against that table anywhere in the file.

## Check the cost

PRD/ticket: `$0/month`. Migration adds one table, two nullable columns, one
`concurrently`-built partial index — storage-negligible at current row
counts (`orders` confirmed ~21.9k rows / 140MB by the build hop); `pg_cron`/
`pg_net`/Vault already in live, billed use elsewhere on this project. No new
extension beyond `pg_cron`/`pg_net`, both `create extension if not exists`
(idempotent, already present). Matches.

## Route

**All 5 owned criteria (AC4, AC5, AC8, AC9, AC12): pass**, verified directly
against the live-matching migration file, not against any gate's own
summary. The guard/crediting half of AC1, AC2, AC3, AC7, AC11, AC15, AC16 is
real but not provable by this ticket alone — see `ENG-049`'s own acceptance
notebook entry for the other half; between the two, none of those seven is
left with an unproven half as of this pass. State → `verified`, owner →
`eng-manager`.

**One caveat carried into the release record, not swept under this pass's
own pass verdict:** `loyalty-auto-complete-tick`'s first fire against the
now-live `loyalty-auto-complete` endpoint (deployed `18:17:37Z`, next tick
`18:30:00Z`) has not been directly observed as of this check. Does not touch
any criterion owned here — the cron's *caller*-side behaviour (AC3, AC15) is
`ENG-049`'s half — but flagged so it isn't lost.

## Step 6b — continue an approved sequence?

Does not apply at the child level — `ENG-027`'s own G1 (the 2026-09-03
approver `changed` response) named the rescoped sequence itself; both
children (`ENG-048`, `ENG-049`) were already filed and sequenced as part of
that same work-breakdown, not fresh items to auto-file from here.

## Also worth recording

`ENG-049` (the sibling, `depends_on: [ENG-048]`) was already past `ready` —
its own PR (#22) had already merged by the time this check ran (processed in
the same pass, its own acceptance entry filed separately) — so this doesn't
start or free a fresh machine-WIP slot on its own. `ENG-027` (parent) settles
only once both children are `shipped`/`verified`/`dropped` (`ADR-003`) — see
that ticket's own log for the container-level update, done in this same
pass now that both children are.
