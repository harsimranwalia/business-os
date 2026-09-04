---
id: ADR-019
title: "Coupon-code ROI matches `orders.promos` against the campaign's code; no redemption-tracking table exists to reuse"
project: aiorders-api
ticket: ENG-019
status: accepted
decided_by: architect
date: 2026-09-03
supersedes:
superseded_by:
---

# ADR-019: Coupon-code ROI matches `orders.promos` against the campaign's code; no redemption-tracking table exists to reuse

## Context

The PRD's Assumed section reads AC4's ROI mechanism as "reusing the exact
mechanic the existing welcome/first-order/every-order offers already use
(`offers.coupon_code`)" — worded as if a redemption-tracking system already
exists to reuse. Reading `origin/main` directly finds otherwise:
`brand-portal/offers.ts`, all three `outgoing-communications` offer-sending
paths, and `admin-portal/handlers/activation.ts` all treat `coupon_code` as a
plain display string shown to the customer. The actual checkout system is
CloudWaitress, not this codebase — `config-site-builder/src/pages/Offers.tsx`
only ever copies the code to the clipboard — and nothing in `aiorders-api`
validates, applies, or records which coupon a given order used, except what
CloudWaitress's own webhook already reports.

That report already exists and is already persisted. CloudWaitress natively
supports checkout-time discount promos (`cloudwaitress-middleware/handlers/
restaurant.ts`'s `handleCreateDiscount` proxy creates them via
`conventional_discount_promos`), and its `order_new` webhook payload includes
`order.promos` and `order.bill.discount`. `external-integrations/handlers/
cloudwaitress.ts`'s `createOrder` already writes `orders.promos` (the raw
CloudWaitress array, untouched) and `orders.total_amount`/`created_at`,
scoped to `restaurant_id`/`customer_id`, on every order — since before this
ticket, for a different reason (order history). So there is no existing
"redemption count" query anywhere on this platform, but the raw data to build
one, with no new capture path, already lands in `orders`.

## Decision

A campaign's redemption count and revenue (AC4) are computed by querying
`orders` scoped to the campaign's `restaurant_id`, `created_at >=` the
campaign's own send (or, for a drip, the relevant step's send) time, where
`orders.promos` contains an entry matching the referenced offer's
`coupon_code`. Count of matching orders = redemptions; `SUM(total_amount)`
over the same set = revenue. Read-only. No write to `orders` or `offers`, no
new capture path.

## Alternatives

| Option | Why not |
|---|---|
| A dedicated redemption-tracking table, written at order time | Requires a write path into checkout processing this codebase does not own — CloudWaitress is authoritative for checkout, and this ticket has no scope or access to change it. |
| Take the PRD's Assumed section at face value, ship assuming the mechanic already exists | False, confirmed directly against `origin/main` — shipping on that assumption means AC4 fails the first time anyone opens a campaign report. |
| Track redemptions via a unique link per campaign instead of a coupon code | Rejected by the PRD's own Non-goals: "attribution for campaigns that carry no coupon code" is explicitly later, separate work. This ticket is scoped to the coupon-code mechanism only. |

## Consequences

**Accepted:** `orders.promos`' exact internal shape — which key names the code
within each array entry — cannot be confirmed from this repo. No tracked
migration defines `orders` at all (the same untracked-schema gap `ADR-006` and
`ENG-020`'s own design already name for `brands`/`profiles`/`customers`).
Whoever builds this confirms the real key against a live sample before writing
the query, and the query fails loud (logs, returns a zero/unavailable state)
rather than silently matching nothing if the assumed key turns out wrong.

**Accepted:** revenue is computed off `orders.total_amount` as recorded at
order-creation time. This platform has no reliable order-status-update path
yet — `cloudwaitress-middleware`'s webhook discards every event except
`order_new` (`ENG-027`'s own finding) — so a later-cancelled order cannot
currently be excluded from a campaign's revenue figure. Named, not solved,
here; matches how every other revenue figure on this platform, including
`ENG-020`'s acquisition report, already computes today.

**Gained:** zero new schema for the read path itself — only the campaign/
recipient tables this design's own Data section adds.

## Review trigger

If `ENG-027` or later work wires up `order_completed_updated`/
`order_cancelled_updated` handling, revisit whether campaign revenue should
filter on a real completion/cancellation status instead of order-creation
time — the same review trigger `ENG-020`'s own revenue figure should
logically carry.
