---
ticket: ENG-049
project: aiorders-api
released: 2026-09-08T18:16:55Z
released_by: approver (direct GitHub merge, no written reply to the merge-request item — `inbox/2026-09-07-eng049-merge-request.md`'s `decision:` field is still blank, confirmed via grep this pass)
autonomy: L1
gate_g3: n/a — L1 lane has no G3; the PR merge is the human gate
commit: 2e5333a8 (PR #23, base main, merging `feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron` — see Merge below for why this ticket's own path to `main` runs through two PRs, not one)
environment: production (Supabase project bmnmnejwdxbcqinqkwko). **Confirmed
  deployed, not just merged** — `supabase functions list` shows
  `external-integrations` (v109), `brand-portal` (v86), and `loyalty-auto-complete`
  (v1, brand new) all updated within a 7-second window,
  `2026-09-08T18:17:30Z`–`18:17:37Z`. See Deploy below.
rollback_tested: reasoned, not drilled — no migration in this diff;
  reverting removes these code paths going forward; a loyalty entry already
  credited before a revert stands (already-accepted design, per the ticket's
  own Notes). Unchanged from the release-readiness hop's own assessment.
health_check: pass — the one hard pre-deploy requirement this ticket's own
  release-readiness hop flagged (`CLOUDWAITRESS_WEBHOOK_SECRET` not
  provisioned) is now satisfied; see Deploy.
cost_delta_monthly: 0
---

# Release — Loyalty webhook handler, auto-complete sweep, and dine-in earn API (ENG-049)

## What shipped

`external-integrations`'s `cloudwaitress.ts`: `createOrder()` persists
`data.order._id` into `orders.cw_order_id`; `handleCloudWaitress()` now
authenticates every request against `CLOUDWAITRESS_WEBHOOK_SECRET` before
branching on `webhookData.event`, and stops discarding
`order_completed_updated`/`order_cancelled_updated`/`order_cancel` — a
fulfilment report calls `credit_order_if_eligible(order.id, 'reported')`; a
cancellation sets `status = 'cancelled'` unconditionally. A new edge
function, `loyalty-auto-complete`, selects the eligible batch and calls
`credit_order_if_eligible(id, 'window_elapsed')` per row inside a
catch-and-continue loop. `brand-portal` gains `record_dine_in_earn` and
`get_loyalty_balance`, both gated by `requireRestaurantAccess`.

## Merge — two PRs, not one, because this was a stacked PR

`ENG-049` branched from `ENG-048`'s own PR branch, not `main` (`ENG-048` was
still unmerged when this ticket reached `ready`). Its own PR, #22, merged
into that branch — **not into `main` directly**:

```
$ gh pr view 22 --json state,mergedAt,baseRefName,headRefName,mergeCommit
{"baseRefName":"feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron",
 "headRefName":"feat/ENG-049-loyalty-webhook-accrual-sweep-and-dine-in-earn-api",
 "mergeCommit":{"oid":"a36c0de43fb68f12351be6dfe9769e7910e125ab"},
 "mergedAt":"2026-09-08T18:14:19Z","state":"MERGED"}
```

By the time PR #22 merged, `ENG-048`'s own PR #21 had **already** merged into
`main` directly (`18:05:03Z`) — so `feat/ENG-048-...`'s tip, at the moment
#22 landed on it, was ahead of what #21 had brought into `main`. Per
`eng_build_loop.md` step 5's stacked-PR provision ("a base that was merged
away under an OPEN PR → say so in the ticket log, it may not have shipped"),
this was checked directly rather than assumed either way:

```
$ git merge-base --is-ancestor origin/feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron origin/main
YES - ancestor, fully in main
$ git log origin/feat/ENG-048-...​..origin/main --oneline
2e5333a Merge pull request #23 from harsimranwalia/feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron
...
```

A third PR, #23 (base `main`, head `feat/ENG-048-...`, i.e. the same branch
now carrying both tickets), merged at `18:16:55Z` and brought the whole
stack into `main`. Confirmed by ancestry, not inferred from PR state alone —
`git merge-base --is-ancestor` returns true. **Shipped**, via the stacked-PR
path this ticket's own branch took.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass (round 2) | principal-engineer | 2026-09-07 |
| Quality (QA) | pass (round 2), 45/45 | qa | 2026-09-07 |
| Security | pass (round 2), A01/A08/A09 findings closed and re-verified | security | 2026-09-07 |
| Migration | n/a — no schema/data-model change; `ENG-048` owns the schema | database | n/a |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-09-08 |

Re-read all three receipts directly: `agents/principal-engineer/reviews/ENG-049.md`
(`verdict: pass`), `agents/qa/test-plans/ENG-049.md` (round-2 suite run: 45
passed, 0 failed, 0 skipped), `agents/security/reviews/ENG-049.md`
(`verdict: pass` — A01 broken-access-control and A08 integrity findings from
round 1 both closed and independently re-verified this round by reading
`handleCloudWaitress` directly).

## Deploy — the flagged pre-deploy requirement, checked live

The 2026-09-07 release-readiness hop found `CLOUDWAITRESS_WEBHOOK_SECRET`
**not provisioned** in the live secrets store and named it a **hard
pre-deploy requirement**: the secret check in `handleCloudWaitress` runs
before every branch, including plain `order_new`, so deploying without it
would 401 **all** CloudWaitress traffic — not just loyalty crediting —
silently, from the caller's side.

**Checked fresh this pass, before treating the deploy as safe:**

```
$ supabase secrets list --project-ref bmnmnejwdxbcqinqkwko | grep CLOUDWAITRESS
CLOUDWAITRESS_WEBHOOK_SECRET  ...  updated_at: 2026-09-08T18:12:56.781Z
```

**Present, and correctly sequenced** — set at `18:12:56Z`, after PR #21
merged (`18:05:03Z`) and before the functions actually deployed
(`18:17:3xZ`, below). This is the exact ordering the release-readiness hop
asked for; the incident it warned about did not happen.

**Deploy method: a GitHub Actions workflow for automated Supabase deploys**,
newly present on `main` (found this pass, not part of either ticket's own
diff — see `ENG-048`'s release record). This is the first `aiorders-api`
release this department has observed with CI/CD attached; every prior one
was manual.

**Confirmed live, checked directly, not assumed from the workflow's
existence:**

```
$ supabase functions list --project-ref bmnmnejwdxbcqinqkwko
external-integrations   v109  updated_at 1788891454381  (2026-09-08T18:17:34.381Z)
brand-portal             v86  updated_at 1788891450867  (2026-09-08T18:17:30.867Z)
loyalty-auto-complete      v1  updated_at 1788891457220  (2026-09-08T18:17:37.220Z)  — brand new function, created == updated
```

All three within a 7-second window, ~40 seconds after PR #23's merge
(`18:16:55Z`) — consistent with a single merge-triggered deploy batch.
`cloudwaitress-middleware` (a separate, older function, unrelated to this
diff) was **not** in this batch (`updated_at` from 2026 much earlier) —
confirms the deploy touched only what this diff actually changed.

**Not yet observed:** the actual live behavior of a real webhook call
against the new secret check, and the cron's first tick against
`loyalty-auto-complete` (expected `18:30:00Z` — see `ENG-048`'s own release
record). Both are inferred-correct from code plus deploy evidence, not
watched directly this pass.

## Verification

Read the merged, live-matching diff directly (`git show
origin/main:supabase/functions/external-integrations/handlers/cloudwaitress.ts`
via the worktree at `main`'s current tip — not any gate's own account):
the secret comparison gate precedes all event branching; `order_completed_updated`/
`order_cancelled_updated`/`order_cancel` all resolve the local order via
`cw_order_id` and either call `credit_order_if_eligible` or set
`status = 'cancelled'`; both paths return `200 {success:true}` regardless of
credit outcome, matching AC13.

## Acceptance criteria

Full `acceptance-check/SKILL.md` walk run this pass. This ticket owns AC6,
AC10, AC13, AC14, AC17, AC18 in full, plus the webhook/sweep-caller/dine-in
half of AC1, AC2, AC3, AC7, AC11, AC15, AC16 — the guard/crediting half is
`ENG-048`'s (processed the same pass; see that ticket's own record). All 6
owned-in-full criteria: **pass**. Full walk:
`agents/product-manager/notebook/2026-09-08-eng049-acceptance.md`.

## Rollback

- **Path:** reasoned, not drilled. No migration in this diff — reverting the
  merge removes the webhook crediting call, the sweep function, and the two
  new `brand-portal` actions going forward. A loyalty entry already credited
  before a revert stands (accepted in the ticket's own design).
- **Tested:** no — nothing destructive to rehearse; additive diff over an
  existing generic handler shape.
- **Used:** no.
- **Note carried from `ENG-048`'s own record:** a rollback of either ticket
  from this point forward must happen together with the other — both are
  live and interdependent now (the migration's own "safe any time before
  `ENG-049` ships" comment is stale).

## Health note

Pass — see Deploy. The one thing that would have made this a bad deploy
(missing webhook secret) is confirmed absent as a risk, checked live, not
assumed from the PR body's own claim.

## Observability

Round 1's `A09` logging gap (a denial with no visibility) closed this round —
`console.warn` on the 401 path, event name only, no secret value. No new gap
introduced.

## Cost

$0/month — no new infrastructure; `loyalty-auto-complete` runs on existing
Supabase Edge Functions compute, invoked at most every 15 minutes by
`ENG-048`'s own cron. Matches the release-readiness hop's own estimate.

## Follow-ups

- Same open item as `ENG-048`'s record: confirm the `18:30:00Z` cron tick
  actually reaches `loyalty-auto-complete` and returns non-404.
- CI/CD auto-deploy on this repo is new and undocumented in
  `config/projects.md` — logged to `observations.md`, not fixed here.
- `ENG-027` (parent): this settles the second of two children. See that
  ticket's own log for the container-level update, same pass.
