# 2026-09-09 — acceptance-check: ENG-052 + ENG-053 (ENG-051's two children)

Run mid-`continue ENG-051` pass, after finding both children already advanced
`blocked → shipped` by the control center's own merge detection (PRs #24/#25,
both merged to `aiorders-api` `main` — `16a4932`, `3a7ca91`). Neither had run
`skills/acceptance-check/SKILL.md` yet. Both share `ENG-051`'s PRD
(`agents/product-manager/specs/ENG-051-...md`); AC ownership per each child's
own Notes: `ENG-052` owns AC5/6/9 fully + the guard/debit half of
AC3/4/7/8/11; `ENG-053` owns AC10 fully + the caller half of the same five.
Neither owns AC1/2 (QR issuance) — independently re-confirmed against
`ADR-022` (`platform_customers.id` already satisfies it; no new issuance path
in this ticket's design at all).

## Method — against the live-shipped artifact, not the test suite

Worked from the department's own isolated worktree,
`~/Documents/projects/_eng/aiorders-api` (repo-isolation guard — never the
approver's interactive clone), `git fetch origin main` first.

- **Migration**: `supabase migration list --linked` shows `20260908160000`
  applied (local hash == remote). Read the full file,
  `supabase/migrations/20260908160000_loyalty_ledger_redemption_widening_and_redeem_function.sql`
  — matches the design's `## Data`/`## Interfaces` sections exactly: the
  three widened per-source checks, the new points-sign-by-source check
  (`>= 0` earn / `< 0` redemption), the nullable-unique `idempotency_key`,
  `rate_applied` widened `numeric(5,2) → numeric(10,4)`, and the full
  `redeem_points_if_eligible` function body.
- **Grants — the one thing worth a live query, not just a read.** `ENG-048`'s
  own history on this exact project: a `revoke ... from public` that looked
  right still left `credit_order_if_eligible` callable by `anon`, because
  `pg_default_acl` grants `EXECUTE` to `anon`/`authenticated` by name at
  function-creation time. Ran, live, against production
  (`supabase db query --linked`, pure `select has_function_privilege(...)`,
  no mutation):
  `anon` → `false`, `authenticated` → `false`, `service_role` → `true`. The
  exact gap class is closed here, confirmed rather than assumed from the
  migration text alone.
- **Edge function actually redeployed, not just merged.** `supabase
  functions list` (JSON): `brand-portal` `version 87`, `updated_at`
  `2026-09-09T14:16:53Z` — after both merge commits (`14:14:03Z` /
  `14:16:17Z`), consistent with the CI/CD auto-deploy `ENG-048`'s own journal
  entry first found. Merged code is live, not just committed.
- **Read the deployed handler directly**
  (`supabase/functions/brand-portal/loyalty.ts`,
  `supabase/functions/brand-portal/utils.ts`, `index.ts`'s router/catch) —
  behavior read from source, since it's plpgsql/TS, not a black box.

## Per-criterion result

- **AC1/AC2** (QR issuance, neither child's) — pass, pre-existing. `ADR-022`:
  `platform_customers.id` is a permanent, cross-restaurant, already-issued
  UUID; no new issuance path anywhere in this design.
- **AC3** (resolve code to exactly one diner) — pass. Guard half: PK lookup
  against `platform_customers`, `invalid_code` sentinel if absent (migration
  lines ~200-205). Caller half: `code` passed verbatim as
  `p_platform_customer_id` (`loyalty.ts` `redeemPoints`).
- **AC4** (balance affected only at that restaurant) — pass. Every
  balance-sum and the insert itself are both scoped
  `(platform_customer_id, restaurant_id)`; `restaurant_id` comes from the
  authenticated staff member's own `requireRestaurantAccess`-checked request,
  never the diner.
- **AC5** (over-balance rejected, no entry) — pass, `ENG-052` alone. Balance
  checked before any insert; `insufficient_balance` returned, function exits
  before the `insert`.
- **AC6** (unconfigured restaurant → not enrolled) — pass, `ENG-052` alone.
  `v_rate is null → return 'not_enrolled'`, no exceptions raised.
- **AC7** (converts at effective rate, one append-only entry) — pass. Single
  `insert`, `v_amount := p_points * v_rate`, no update/delete path anywhere
  in the function.
- **AC8** (balance read afterward reflects the debit immediately) — pass.
  Balance is sum-on-read (`readBalance`, no cache); `redeemPoints` calls it
  right after the RPC on both `insufficient_balance` and `redeemed`.
- **AC9** (duplicate retry doesn't double-debit) — pass, `ENG-052` alone.
  `idempotency_key` matched **before** the balance read, inside the advisory
  lock; a genuine replay returns `'redeemed'` again with no second insert; a
  key reused for a different `(diner, restaurant, points)` raises instead of
  silently succeeding.
- **AC10** (unauthorized staff rejected) — pass, `ENG-053` alone.
  `requireRestaurantAccess` is the first call in `redeemPoints`, before any
  validation or RPC; denial throws `Error` → `index.ts`'s top-level catch →
  `500`, the same shape `recordDineInEarn`/`getLoyaltyBalance` already use in
  this file. Ticket's own note ("500-shaped, not 403-shaped, matches
  siblings") checked against `utils.ts`/`index.ts` directly, not taken on
  faith — accurate.
- **AC11** (earns + redemptions in one ordered history) — pass.
  `readBalance`'s `entries` query has no `source` filter, orders by
  `earned_at desc` — a `'redemption'` row surfaces automatically once one
  exists. `LoyaltyLedgerEntry`'s `source` union already widened to include
  it.

## Non-goals — nothing built outside scope

No frontend/QR-image rendering, no admin/support surface, no Walletly
migration, no change to any earn path, no expiry/pooling, no rate-limiting,
no code rotation. Confirmed by the actual diff read above, not inferred from
the ticket's own claim.

## Cost

PRD estimated Build `M` (narrowed from a provisional `L`), Run `$0`/month, no
new vendor. Actual: two `S` tickets, same total order of magnitude; no new
Supabase project, no cron, no external service — matches. No CFO escalation.

## What the estimate missed

Nothing material. The two-ticket guard/caller split (`ENG-048`/`ENG-049`'s
own shape, reused here) continues to work cleanly for a debit-shaped write —
worth keeping as the default decomposition for any future ledger-adjacent
pair on this table. The CI/CD auto-deploy path (first confirmed on
`ENG-048`) is now confirmed twice; safe to stop calling it out as a fresh
finding in future acceptance-checks on this project unless it actually
breaks.
