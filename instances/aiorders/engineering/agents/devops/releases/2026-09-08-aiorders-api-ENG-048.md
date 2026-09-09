---
ticket: ENG-048
project: aiorders-api
released: 2026-09-08T18:05:03Z
released_by: approver (direct GitHub merge, no written reply to the merge-request item — `inbox/2026-09-07-eng048-merge-request.md`'s `decision:` field is still blank, confirmed via grep this pass)
autonomy: L1
gate_g3: n/a — L1 lane has no G3; the PR merge is the human gate
commit: 051feff8 (merge of 60fa06e, PR #21, base main)
environment: production (Supabase project bmnmnejwdxbcqinqkwko). **Confirmed
  deployed, not just merged** — `supabase migration list --linked` shows
  `20260907130000` (this ticket's own migration) matched on both `local` and
  `remote`, i.e. the migration has actually executed against the live
  database, not just landed in `main`. See Deploy below.
rollback_tested: tested, not just reasoned — run twice against a disposable
  local replica (`supabase/postgres:15.8.1.073`), pre- and post-`CONCURRENTLY`
  fix, both confirmed clean (release-readiness hop, 2026-09-07). Not re-run
  against production; the migration's own rollback block is unchanged from
  what was tested.
health_check: partial, see Deploy note on `loyalty-auto-complete-tick`.
cost_delta_monthly: 0
---

# Release — Loyalty ledger schema, credit function, and auto-complete cron (ENG-048)

## What shipped

`loyalty_ledger_entries` (append-only, `order_id` unique when present),
`orders.cw_order_id` / `orders.loyalty_processed_at`, and
`credit_order_if_eligible(order_id, fulfillment_reason)` — the one guarded
Postgres function both `ENG-049`'s webhook handler and its auto-complete
sweep call. `loyalty-auto-complete-tick` (`pg_cron`, `*/15 * * * *`) fires
`net.http_post` against `ENG-049`'s `loyalty-auto-complete` edge function.
Full detail: this ticket's own board file, `agents/backend/notebook/` build
entries.

## Merge

No reply was ever written to this department's own merge-request item.
`aiorders-api` PR #21 was merged directly on GitHub instead, base `main`,
head `feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron`:

```
$ gh pr view 21 --json state,mergedAt,baseRefName,headRefName,mergeCommit
{"baseRefName":"main","headRefName":"feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron",
 "mergeCommit":{"oid":"051feff8b43d9c3fe4a87468bcd7da5f7e935461"},
 "mergedAt":"2026-09-08T18:05:03Z","state":"MERGED"}
```

Detected fresh this pass (`continue ENG-027`, checking both children's PR
state) — the checkpoint this pass started from still read `OPEN`; the merge
happened between that checkpoint and this check.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass (round 2) | principal-engineer | 2026-09-07 |
| Quality (QA) | pass (round 2) | qa | 2026-09-07 |
| Security | pass (zero blocking findings) | security | 2026-09-07 |
| Migration | pass | database | 2026-09-07 |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-09-08 |

Re-read all three receipts directly before writing this record:
`agents/principal-engineer/reviews/ENG-048.md` (`verdict: pass`),
`agents/qa/test-plans/ENG-048.md` (`Verdict: pass` — both round-1 fails
independently re-tested and closed against a fresh disposable replica),
`agents/security/reviews/ENG-048.md` (`verdict: pass`).

## Deploy

- **Method: a GitHub Actions workflow for automated Supabase deploys**, added
  to `main` around the same time as this merge (found this pass via `git log
  origin/feat/ENG-048-...​..origin/main` — a sibling commit,
  "Add GitHub Actions workflow for automated Supabase deploys", not part of
  this ticket's own diff). Every prior `aiorders-api` release on this board
  was a manual, by-hand deploy; this is the first one this department has
  observed with CI/CD attached. Not investigated further — out of scope for
  this ticket, noted in `observations.md`.
- **What actually happened, checked live this pass:** `supabase migration
  list --linked` shows `20260907130000` applied on `remote`, matching
  `local`. The migration's own DDL (table, columns, function, cron schedule)
  is one file with no partial-apply mode, so a recorded-applied migration
  means all of it ran, including `cron.schedule('loyalty-auto-complete-tick',
  ...)`.
- **Migration:** `supabase/migrations/20260907130000_loyalty_ledger_schema_and_credit_function.sql` — confirmed applied, see above.
- **Feature flag:** none.
- **Duration:** n/a — no deploy run by this department; timing inferred from
  the migration-tracking table and the sibling `ENG-049` deploy's function
  timestamps (both below), not measured directly.

### `loyalty-auto-complete-tick` — the observability gap the release-readiness hop flagged, now closed

The 2026-09-07 release-readiness hop judged the cron's unconditional
`net.http_post` non-blocking for merge *because* `ENG-049`'s
`loyalty-auto-complete` function didn't exist yet, and named the gap as
closing "the moment `ENG-049` ships." Checked fresh this pass, not assumed
closed by narrative: `supabase functions list` shows `loyalty-auto-complete`
now `ACTIVE`, version 1, deployed `2026-09-08T18:17:37Z` (see `ENG-049`'s own
release record for the full deploy evidence). The gap is structurally closed
— the endpoint the cron calls now exists — but **the first tick against the
live endpoint has not been directly observed**: the schedule is
`*/15 * * * *`, the function deployed at `18:17:37Z`, so the first fire
against live code lands at `18:30:00Z`, after this record is being written
(`18:2x`). Marked `health_check: partial` above for this reason — the next
pass to touch this ticket or its parent should confirm `cron.job_run_details`
shows a tick at or after `18:30:00Z` before treating this as fully closed
end-to-end. Note also (release-readiness hop's own finding, unchanged):
`cron.job_run_details` records success regardless of HTTP outcome — a clean
run there is necessary, not sufficient.

## Verification

Read directly from the live-matching migration file
(`supabase/migrations/20260907130000_loyalty_ledger_schema_and_credit_function.sql`,
confirmed applied above), not any gate's own account:
`credit_order_if_eligible` guards on `loyalty_processed_at is null and status
is distinct from 'cancelled'` in the same `UPDATE ... RETURNING` that locks
the row (AC4/AC5); resolves the rate via `effective_from <= v_order.created_at
order by effective_from desc limit 1` — placement-time, not credit-time
(AC8); writes `rate_applied` as a snapshot per row, so a later config change
cannot alter an already-written entry (AC9); returns `skipped_no_identity`
before any ledger insert or `orders` mutation beyond the processed-marker
when no platform identity resolves (AC12). `revoke ... from public, anon,
authenticated` / `grant ... to service_role` present exactly as reviewed.

## Acceptance criteria

Full `acceptance-check/SKILL.md` walk run this pass. This ticket owns AC4,
AC5, AC8, AC9, AC12 in full — the guard/crediting half of AC1, AC2, AC3, AC7,
AC11, AC15, AC16 is real but not provable alone (`ENG-049`'s own half
completes each; see that ticket's record). All 5 owned criteria: **pass**,
against the live-matching migration file above plus
`agents/qa/test-plans/ENG-048.md`'s independently-re-tested evidence (not
accepted on the receipt's own account — cross-checked against the SQL
directly, this pass). Full walk:
`agents/product-manager/notebook/2026-09-08-eng048-acceptance.md`.

## Rollback

- **Path:** `cron.unschedule('loyalty-auto-complete-tick')`; drop the
  function; drop the concurrent index; drop the `orders` constraint/columns;
  drop `loyalty_ledger_entries`. Exact statements in the migration file's own
  trailing comment.
- **Tested:** yes, twice, against a disposable local replica (pre- and
  post-`CONCURRENTLY` fix). Not re-tested against production this pass.
  **No longer "safe any time"** as the migration file's own comment claims —
  that comment was written before `ENG-049` shipped; `ENG-049` now writes to
  `loyalty_ledger_entries` and calls `credit_order_if_eligible` live, so a
  rollback from this point forward must happen together with reverting
  `ENG-049`, exactly the caveat the migration file's own comment already
  names for that case. Worth a note on `ENG-049`'s record too.
- **Used:** no.

## Health note

Partial — see the `loyalty-auto-complete-tick` section above. Everything
else (table, columns, function, grants) is verified directly against live
migration-tracking state, not merely inferred.

## Observability

No new gap introduced beyond the cron one above, which is closing by
construction now that `ENG-049` is also live. `service_role_key` Vault
secret confirmed live and in use (release-readiness hop, 2026-09-07).

## Cost

$0/month — same Supabase project; `pg_cron`/`pg_net`/Vault already in live
use elsewhere; one new table, two nullable columns, four indexes are
storage-negligible at low row counts. Matches the release-readiness hop's own
estimate.

## Follow-ups

- Confirm `loyalty-auto-complete-tick`'s first post-deploy fire (expected
  `18:30:00Z`) actually reaches `loyalty-auto-complete` and returns non-404 —
  not yet observed as of this record.
- The migration file's own rollback comment ("safe any time before `ENG-049`
  ships") is now stale — both tickets are live; note this if the file is
  ever revisited.
- CI/CD auto-deploy on this repo is new and undocumented in
  `config/projects.md` (which still reads "no `.github/workflows/`" as of
  2026-08-23) — logged to `observations.md`, not fixed here (out of this
  ticket's scope).
- `ENG-027` (parent): this settles one of two children. See that ticket's own
  log for the container-level update.
