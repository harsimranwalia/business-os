# Acceptance — ENG-049 (Loyalty webhook handler, auto-complete sweep, and dine-in earn API; `ENG-027` sub-ticket 2 of 2)

## Why this ran in full, not as receipt bookkeeping

`ENG-049` has real, checkable behaviour (webhook handling, a sweep, two new
API actions) — the `ENG-031`/`ENG-037`-style 0-criteria carve-out doesn't
apply. Per the standing proposal filed 2026-09-04, run in full.

## Scope

Per `agents/eng-manager/notebook/2026-09-07-eng027-work-breakdown.md`'s own
AC-mapping (also recorded on the ticket's own board file and
`agents/qa/test-plans/ENG-049.md`'s `coverage_note`), `ENG-049` owns **AC6,
AC10, AC13, AC14, AC17, AC18 in full**, plus the webhook/sweep-caller/
dine-in-population half of AC1, AC2, AC3, AC7, AC11, AC15, AC16. The
guard/crediting half of those seven is `ENG-048`'s (processed the same pass —
see that ticket's own acceptance notebook entry; combined, none of the seven
is left with an unproven half as of this pass).

## Check against the live result — not the proxies

`ENG-049` was a stacked PR (branched from `ENG-048`'s own PR branch, not
`main`). Its own PR #22 merged into that branch at `18:14:19Z`; the branch
itself (now carrying both tickets) merged into `main` via PR #23 at
`18:16:55Z`:

```
$ git merge-base --is-ancestor origin/feat/ENG-048-...  origin/main
YES - ancestor, fully in main
```

**Confirmed live, not just merged** — `supabase functions list`:
`external-integrations` v109 (`18:17:34Z`), `brand-portal` v86
(`18:17:30Z`), `loyalty-auto-complete` v1, brand new (`18:17:37Z`). All three
within 7 seconds, ~40s after PR #23. Full deploy evidence, including the
webhook-secret pre-deploy check: `ENG-049`'s own release record
(`agents/devops/releases/2026-09-08-aiorders-api-ENG-049.md`).

Read the merged, live-matching source directly (`git show
origin/main:supabase/functions/external-integrations/handlers/cloudwaitress.ts`
and `.../brand-portal/*`), not any gate's account of it.

## Walk every owned criterion

| AC | Criterion (owned portion) | Checked against | Result |
|---|---|---|---|
| 6 | Dine-in submission credits the diner at the restaurant's dine-in rate | `record_dine_in_earn` inserts a `loyalty_ledger_entries` row with `source: 'dine_in'`, `rate_applied` from `restaurant_loyalty_configs.dine_in_earn_pct`, gated by `requireRestaurantAccess`. QA: `record_dine_in_earn: credits the diner and inserts a well-formed dine_in entry (AC6, AC7)` — pass | **Pass** |
| 10 | Balance = sum of entries at that restaurant only, unaffected by entries at any other | `get_loyalty_balance` sums `loyalty_ledger_entries.points` filtered by both `platform_customer_id` and `restaurant_id`, backed by `ENG-048`'s own composite index. QA caught and fixed a real regression here (`readBalance` originally summed only the capped 500-row display list, silently wrong past that cap) — fixed with a separately-capped display query and an unbounded sum query, proven with a 505-row fixture that genuinely exercises both paths differently, not a symbolic test | **Pass** |
| 13 | A loyalty-side failure never blocks, fails, or changes the webhook's own success response | Read `handleCloudWaitress` directly: `credit_order_if_eligible` and the cancellation update are both wrapped so a thrown/RPC error is logged and swallowed, never surfaced past the handler. QA: three tests (order-lookup failure, credit-call error, cancellation-update error) all assert `res.status === 200` and the unconditional `{success:true}` body | **Pass** |
| 14 | A terminal-event report for an order with no local record is accepted and ignored, nothing created | `cw_order_id` lookup miss → early return, `{success:true}`, zero RPC calls. QA: `unknown cw_order_id is accepted and ignored (AC14)` — asserts the response shape and zero calls | **Pass** |
| 17 | A staff member with no access to the restaurant is rejected, no entry created | `record_dine_in_earn` calls `requireRestaurantAccess` (the throwing, post-`ENG-022` version) before any insert. QA: `access denied for a staff member with no restaurant access (AC17)` | **Pass** |
| 18 | A non-positive-finite `amount` is rejected with a clear reason, no entry created | QA's 7-value parameterised test (`0, -5, NaN, Infinity, "10", null, undefined`) — confirmed by reading the actual test source (not just the names, which round 2's own review flagged as partially ambiguous) that each value is a genuinely distinct case, all rejected before any insert | **Pass, all 7 values** |

## Check the non-goals / bundling risk

Ticket's own Notes: this ticket does not touch `ENG-048`'s guard/crediting
logic, and the webhook signature check was originally scoped out by round 1
before the security gate overruled that and blocked on it — closed in round
2 with its own 8-test regression suite, not a scope violation (the gate's
own authority to expand scope on a security finding is standard, not
bundling). Confirmed on the merged diff: `git show 0bec87c --stat` touches
exactly `cloudwaitress.ts` and its test file, nothing in `ENG-048`'s
migration or function.

## Check the cost

PRD/ticket: `$0/month`, no new infrastructure. `loyalty-auto-complete` is a
new edge function but runs on existing Supabase Edge Functions compute, same
billing model as every other function on this project. Matches.

## Route

**All 6 owned-in-full criteria (AC6, AC10, AC13, AC14, AC17, AC18): pass**,
verified directly against the live-matching merged source, not against any
gate's own summary. Combined with `ENG-048`'s own pass on the guard/crediting
half (processed the same pass), none of the seven shared criteria (AC1, AC2,
AC3, AC7, AC11, AC15, AC16) is left with an unproven half as of this check.
State → `verified`, owner → `eng-manager`.

**One caveat carried into the release record, not swept under this pass's
own pass verdict:** the cron's first live tick against `loyalty-auto-complete`
(expected `18:30:00Z`) has not been directly observed. Does not touch any
criterion owned here.

## Step 6b — continue an approved sequence?

`ENG-027`'s own PRD (`## Proposed change (rescoped — accrual at fulfilment)`)
frames this as a two-ticket sequence (`ENG-048` database, `ENG-049` backend)
under the parent `ENG-027`, both already filed and both now settled in this
same pass — no further item to auto-file from this sequence. `ENG-027`
itself (the container) is addressed separately, same pass, per `ADR-003`.

## Also worth recording

This is the second child settled in this pass — `ENG-048` was processed
first (same pass, its own acceptance entry filed separately). With both
children `verified`, `ENG-027` becomes eligible for its own container-level
closeout under `ADR-003` ("every child is shipped, verified or dropped and
at least one actually shipped") — handled in `ENG-027`'s own board file, same
pass, not here (a parent owes no receipts of its own; its evidence is its
children's).
