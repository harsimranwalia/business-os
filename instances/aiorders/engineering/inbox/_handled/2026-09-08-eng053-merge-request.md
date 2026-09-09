---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-api
ticket: ENG-053
recommendation: merge ENG-052 (PR #24) first, then this PR (#25) — code review, quality, and security all passed (round 2; round 1 failed on missing test coverage only, since fixed); this is sequence 2 of 2 in the ENG-051 (redemption) family — its last child, so once both PRs merge ENG-051 itself is ready to close out
time_estimate: half a day
pr_url: https://github.com/harsimranwalia/aiorders-api/pull/25
raised: 2026-09-08
notified: 2026-09-08T16:35:41
nudged:
---

# Merge request — Loyalty redemption brand-portal redeem_points action (ENG-053)

Sub-ticket of `ENG-051` (redemption API and QR issuance/scanning), sequence 2
of 2 — the family's last child. Depends on `ENG-052` alone
(`redeem_points_if_eligible`), whose own PR #24 is still open; this PR is
stacked on `ENG-052`'s branch (base `feat/ENG-052-loyalty-redemption-ledger-widening-and-redeem-function`,
not `main`) and **must merge after it**.

## What this does

`brand-portal/loyalty.ts` gains a `redeemPoints` handler, wired into
`handleLoyalty`'s switch and `index.ts`'s router (`+1 case 'redeem_points':`).
Payload `{restaurant_id, code, points, idempotency_key}`.
`requireRestaurantAccess` runs first (AC10); missing `code`/`idempotency_key`
or a non-positive/non-finite `points` rejects before any RPC call. Calls
`ENG-052`'s `redeem_points_if_eligible` RPC; `invalid_code`/`not_enrolled`
return the live result directly, `insufficient_balance`/`redeemed` also
attach the diner's current balance via the existing `readBalance`.
`LoyaltyLedgerEntry.source` widens to add `'redemption'`.

## Gates passed

- **Code review: pass, round 2** — `agents/principal-engineer/reviews/ENG-053.md`.
  Round 1 failed on one blocking finding (zero test coverage for
  `redeemPoints` in a file that already carries a real suite for its two
  sibling actions); round 2's fix added 15 new tests, each of round 1's four
  fix-list items verified against the actual assertions, not accepted on
  count alone. 0/10 automatic failures both rounds.
- **Quality: pass, round 2** — `agents/qa/test-plans/ENG-053.md`. AC10 in
  full, the handler-caller half of AC3/AC4/AC7/AC8/AC11 — all now backed by a
  test. 0 open P0/P1.
- **Security: pass** — `agents/security/reviews/ENG-053.md`. Full OWASP walk;
  both items `ENG-052`'s own gate flagged forward (wrong-tenant gate,
  no-token path) independently closed. Two pre-existing, already-tracked,
  non-blocking A05 patterns named (generic `error.message` on the 500 catch;
  repo-wide CORS wildcard), neither new to this diff, neither re-proposed.
  Secrets scan clean, no new dependencies.
- **Migration: n/a** — no schema/data-model change; `ENG-052` owns the
  function this ticket calls.

All independently re-verified from the receipts and the actual diff, not
accepted on a prior gate's or the ticket's own account — `deno test
--no-check`: 34/34 on `loyalty.test.ts` alone, 119/119 on the full
`brand-portal` suite, matching exactly across build, review, and security.

## One judgment call, named rather than silently resolved

The design's own "400-shaped rejection" language for bad input can't be
built literally: `index.ts`'s top-level `catch` is a single hardcoded
`status: 500` with no mechanism for a handler to signal otherwise, and the
design's own Components table caps this ticket's `index.ts` change at one
router-case line. Validation failures `throw new Error(...)`, same
mechanism/depth as `recordDineInEarn`'s own checks, surfacing as `500` —
consistent with every other rejection in this file. This reinforces an
already-open, already-scoped proposal (`proposals.md`, 2026-09-07 row, found
first on `ENG-049`'s AC17 "403-shaped" language) rather than a new defect —
not re-filed. Flagged here in case the design's intent was a literal
wire-level `400`, which would need its own separately-scoped change to
`index.ts`'s catch block.

## Release readiness

- **Rollback:** reasoned, not drilled — no migration in this diff; nothing
  destructive to rehearse. Reverting removes the `redeem_points` code path
  going forward; a redemption already recorded before a revert stands (no
  undo mechanism in either direction, same accepted design `ENG-049`'s own
  crediting-side record carries). Rolling back this ticket alone (leaving
  `ENG-052` merged) is safe — nothing else calls `redeem_points_if_eligible`
  yet.
- **Observability:** no gap. The generic top-level `catch` in `index.ts`
  (`console.error`, pre-existing, unchanged) covers every failure this
  action can produce; the access-denial log carries `user`/`restaurant`
  only, never the diner code.
- **Cost:** $0/month — same Supabase project and edge function, no new
  infrastructure, no new compute.
- **Window:** n/a — `aiorders-api` is registered L1; opening a PR is not a
  release.

## PR

https://github.com/harsimranwalia/aiorders-api/pull/25 — base is `ENG-052`'s
own branch (stacked), **not** `main`. Merge `ENG-052`'s PR #24 first.

This project is registered **L1** — this department opens the PR, a human
merges. The next build-loop pass detects the merge itself (local git
ancestry / PR-state check for the stacked case, no reply needed from you)
and advances the ticket.

## Out of scope

- No frontend, no QR rendering — already satisfied by `ENG-006`'s shipped
  `platform_customers.id`.
- No new balance-read endpoint — AC11's handler-caller half is satisfied by
  the `LoyaltyLedgerEntry.source` widening alone.
- The pre-existing 500-vs-error-code-shaped language gap on
  `requireRestaurantAccess` denials — already flagged, already proposed,
  not this ticket's to fix.

Sequence 2 of `ENG-051`'s two sub-tickets — its last child. Once both this PR
and `ENG-052`'s PR #24 merge, `ENG-051` itself has no remaining child to wait
on.
