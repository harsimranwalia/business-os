---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-api
ticket: ENG-049
recommendation: merge #21 (ENG-048) first, then this one — code review, quality, and security all passed (security round 2, after round 1 blocked and was fixed); last sub-ticket of the ENG-027 family. Before deploying, set CLOUDWAITRESS_WEBHOOK_SECRET in the Supabase Function secrets store — see the "Read before merging" note below, this is not optional
time_estimate: a day to a couple of days
pr_url: https://github.com/harsimranwalia/aiorders-api/pull/22
raised: 2026-09-07
notified: 2026-09-07T18:44:54
nudged:
---

# Merge request — Loyalty accrual: webhook handler, auto-complete sweep, and dine-in earn API (ENG-049)

Sub-ticket of `ENG-027` (loyalty points ledger and earn), sequence 2 of 2 —
the last one. Depends on `ENG-048` alone; that dependency was satisfied once
`ENG-048`'s own PR opened (`blocked_on: approver`, per the Guards
2026-09-07 amendment), not waiting for it to merge. **This PR is stacked on
`ENG-048`'s branch** (`feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron`,
PR #21, still open), not on `main` — merge #21 first.

## What this does

- `cloudwaitress.ts`'s `createOrder()` persists CloudWaitress's own order id
  into `orders.cw_order_id`. The webhook handler stops discarding
  `order_completed_updated` (credits loyalty points on a fulfilment report),
  `order_cancelled_updated`/`order_cancel` (marks the order cancelled,
  never touches the ledger). Every branch still returns `200
  {success:true}` regardless of credit outcome — order recording can't be
  blocked by a loyalty-side failure.
- New edge function `loyalty-auto-complete` — the endpoint `ENG-048`'s own
  15-minute cron has been 404ing against since it shipped. Selects the
  eligible batch (24h past order creation, not yet processed, not
  cancelled) and credits each via the same RPC the webhook uses.
- Two new `brand-portal` actions: `record_dine_in_earn`, `get_loyalty_balance`.

## Read before merging — a pre-deploy requirement, not a nice-to-have

**`CLOUDWAITRESS_WEBHOOK_SECRET` is not provisioned** (checked live this
pass against the actual Supabase Function secrets store — 34 entries, none
named this). This diff's security fix (below) gates **every** CloudWaitress
webhook call through this route, including plain `order_new`, not only the
three new terminal events — read directly in the code, not taken on any
gate's account: `verifyCloudWaitressSecret` runs immediately after parsing
the request body, before any other check. Deploying without this secret set
means the route 401s all real CloudWaitress traffic and **order intake stops
entirely**, not just loyalty crediting. The value is the one CloudWaitress
is already configured with (see `cloudwaitress-middleware/handlers/
restaurant.ts`'s `AIORDERS_WEBHOOK.secret` in this same repo — not
reproduced here). This department doesn't provision production secrets
itself; whoever runs the eventual `supabase functions deploy` needs to set
it first or in the same step.

## Gates passed

- **Code review: pass, round 2** — `agents/principal-engineer/reviews/ENG-049.md`.
- **Quality: pass, round 2** — `agents/qa/test-plans/ENG-049.md`. All six
  fully-owned ACs (6, 10, 13, 14, 17, 18) and the webhook/sweep/dine-in half
  of seven more (1, 2, 3, 7, 11, 15, 16 — guard/crediting half is `ENG-048`'s
  own) covered. 45/45 tests, 0 open P0/P1.
- **Security: pass, round 2** — `agents/security/reviews/ENG-049.md`. Round
  1 blocked on one critical finding (below); the fix passed round 2 clean.
- **Migration:** none owed — Deno/TS only, no `*.sql`; schema is `ENG-048`'s.

## Security: round 1 failed, fixed, round 2 passed

Round 1 found the CloudWaitress webhook route never verified the inbound
caller — an unauthenticated POST could fabricate an order that the
auto-complete sweep would credit real loyalty points against, unbounded.
Fixed (`0bec87c`): a shared-secret check before any branching on the event
type, failing closed on misconfiguration, 8 new tests including a direct
regression for the traced exploit chain (asserts zero Supabase calls on an
unauthenticated request, not just a 401). Round 2 re-verified the fix
against the finding's own requirement independently at every gate — pass.

## Release readiness

- **Rollback:** reasoned, not drilled — this ticket's own diff has no
  migration (schema is `ENG-048`'s); reverting the merge removes these code
  paths going forward. One asymmetry, already accepted by the ticket's own
  design: a loyalty entry credited before a revert is not retroactively
  undone — cancellation/correction of an already-credited entry is a human
  action, named in this ticket's own Notes as a future ticket's surface, not
  a gap this release introduces.
- **Observability:** the `CLOUDWAITRESS_WEBHOOK_SECRET` gap above is the
  live one — named prominently, not fixed here (out of this department's
  authority to provision unilaterally). Separately, this PR is what closes
  `ENG-048`'s own already-named observability gap (the cron 404ing every 15
  minutes) once both PRs are merged and deployed.
- **Cost:** $0/month — same Supabase project, no new infrastructure; the
  cron itself is `ENG-048`'s, already scheduled.
- **Window:** n/a — `aiorders-api` is registered L1; opening a PR is not a
  release.

## PR

https://github.com/harsimranwalia/aiorders-api/pull/22 (base: `ENG-048`'s
branch, PR #21 — merge that one first)

This project is registered **L1** — this department opens the PR, a human
merges. The next build-loop pass detects the merge itself (local git
ancestry, no reply needed from you) and advances the ticket.

## Non-blocking findings, named not fixed

- Secret comparison isn't constant-time — theoretical timing side channel,
  not practically exploitable given a high-entropy UUID over a public HTTP
  round trip. Fix next time this function is touched.
- `loyalty.test.ts`'s `INVALID_AMOUNTS` test-naming collision (cosmetic;
  coverage itself is real).
- AC17's "403-shaped" design language doesn't match this file's actual
  `500` — systemic across `brand-portal`, filed as a proposal, not fixed on
  this ticket alone.

## Out of scope

- Migrating the pre-existing hardcoded webhook secret in
  `cloudwaitress-middleware` to an env var — separate, already-tracked
  cleanup.
- Any frontend.

**This is `ENG-027`'s last sub-ticket.** Once both this PR and `ENG-048`'s
merge, a future pass's step-5 merge detection carries `ENG-049` to
`shipped`, which — per the family's own `ADR-003`-class exemption — makes
`ENG-027` itself eligible to close out directly. Not this hop's to process.

The `ENG-027` family's machine slot is now fully free (both sub-tickets
parked, no third child) — nothing on the board's To-do column is currently
startable without an answer from you; see `inbox/IDLE-2026-09-07.md`.
