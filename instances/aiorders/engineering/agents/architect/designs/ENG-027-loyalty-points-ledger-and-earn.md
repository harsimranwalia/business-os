---
ticket: ENG-027
project: aiorders-api
author: architect
created: 2026-09-05
adrs: ["ADR-021"]
one_way_doors: []
touches_data: true
touches_models: false
---

# Loyalty points ledger, balances, and earn API — online-order and dine-in accrual — technical design

## Approach

Investigated against `origin/main` (`89c6fdb`, includes `ENG-038`'s
just-merged broadcast work) via `git fetch` + `git show`/`git grep`, not by
checking out the department worktree — `~/Documents/projects/_eng/aiorders-api`
currently sits on `ENG-038`'s branch (now merged, a separate in-flight
ticket's checkout at the time of this pass), so reading through git avoided
touching it.

**Re-verified, not just trusted, four load-bearing facts the PRD's rescope
already found:** (1) `cloudwaitress.ts:238` still discards every webhook
event except `order_new` — `if (webhookData.event !== 'order_new') return
{success:true, message: 'ignored'}`. (2) `createOrder()` (`cloudwaitress.ts:188`)
inserts `restaurant_id, customer_id, number, status, notes, order_type, bill,
payment, dishes, config, ready_in, delivery_in, promos, total_amount,
tip_amount, created_at` and nothing else — `orderData._id` (CloudWaitress's
own order id) is read from the payload but never persisted, only
`orderData.number` is. (3) `AIORDERS_WEBHOOK` (`cloudwaitress-middleware/handlers/restaurant.ts:6`)
subscribes to all nine CloudWaitress event types, `enabled: true`, including
`order_completed_updated`, `order_cancelled_updated`, and `order_cancel` —
this ticket newly acts on those three; `order_update_status` and the four
booking/ready-time events stay ignored exactly as today (Alternatives). (4)
`sendFeedbackQueueMessage`'s delay default is `3*60*60` seconds
(`cloudflare-queue.ts:73`) — confirmed, and not reused here (Alternatives).

**One thing not in the PRD, checked directly:** whether anything in this
repo branches on `orders.status`'s specific string value, since this ticket
starts writing real values into a column that has only ever held CloudWaitress's
snapshot-at-placement string. `git grep` across every `.eq('status', ...)`
and `order.status`/`orders.status` reference in `supabase/functions/`: the
only two hits (`brand-portal/onlineOrders.ts:105,187`) pass `order.status`
straight through to the JSON response, no branch. Every other `status`
match belongs to `broadcast_campaigns`/`broadcast_campaign_recipients` or an
influencer-schedule table, not `orders`. Writing real terminal values into
`orders.status` is safe — nothing downstream reads it as anything but a
display string today, matching the PRD's own claim, independently confirmed
here rather than re-cited on trust.

**`orders`' own schema has never been in version control** — no
`CREATE TABLE` for it exists anywhere in `supabase/migrations/`, the same
situation `ENG-006` found for `customers` before any migrations directory
existed. Every column named above comes from `createOrder()`'s insert
statement, not a schema file. This ticket's own migration will be the first
thing in version control that touches this table at all.

**Two established patterns from sibling tickets, reused rather than
reinvented:**

- **The rate-as-of-a-timestamp read** (`ENG-007`, `restaurant_loyalty_configs`):
  `select * from restaurant_loyalty_configs where restaurant_id = $1 and
  effective_from <= $2 order by effective_from desc limit 1` — used here
  with `$2` = the order's own `created_at` (online, rate at placement) or
  `now()` (dine-in, rate at submission). No rows → "not enrolled" (AC11),
  same meaning `ENG-007` already established.
- **The platform identity walk** (`ENG-006`): `orders.customer_id →
  customers.id → platform_customer_legacy_links.legacy_customer_id`
  (`unique`) `→ platform_customer_id`. No link row → no platform identity
  (AC12), same meaning `ENG-006` already established.

**A third pattern, `ADR-018`'s `pg_cron` + `net.http_post` poller
(`broadcast-dispatch`), is reused for the auto-complete sweep instead of
`sendFeedbackQueueMessage`'s per-order Cloudflare Queue delay** — see
`ADR-021`. In short: AC15 describes a sweep that keeps processing the rest
of a batch when one order fails and retries only that one next run, which is
a batch-claim shape, not an independent-per-order-callback shape; and this
project already has a proven poller for exactly this pattern, so introducing
a second, unverified delay mechanism (Cloudflare Queues' own maximum
`delay_seconds` is not established anywhere in this repo or this design) has
no offsetting benefit.

**Idempotency is one guarded, single-row update, not a lock table.** Both
triggers that can credit an order — the webhook's `order_completed_updated`
handler and the sweep — go through one Postgres function,
`credit_order_if_eligible(order_id, fulfillment_reason)`, that does
everything (guard check, identity/rate resolution, ledger insert, order
update) in one transaction. The guard is `WHERE loyalty_processed_at IS NULL
AND status IS DISTINCT FROM 'cancelled'` on the `orders` row itself: ordinary
Postgres row-level locking serializes two concurrent callers touching the
same row, so whichever commits first wins and the second sees the already-updated
row and no-ops. No advisory lock is needed here the way `ENG-007`'s
cross-row race needed one — this is a single-row conditional update, which
Postgres already serializes. A separate `unique` constraint on
`loyalty_ledger_entries.order_id` (where not null) is a second, independent
guard against ever double-crediting one order, on the reasoning that this is
the department's first money-adjacent write path and is worth over-enforcing
(PRD, Risks: "the highest blast radius of the set").

**Cancellation updates `orders.status` unconditionally; it does not touch
`loyalty_processed_at`.** This is what makes AC5 and AC16 both true at once:
if a cancellation commits before any credit attempt, the credit function's
own guard (`status IS DISTINCT FROM 'cancelled'`) blocks it — credited zero
times (AC5). If a credit already committed, a later cancellation still
updates `status` (so the order displays correctly — the PRD's own incidental
fix) but does not delete or rewrite the existing ledger entry (AC16) —
correction stays a manual opposite entry, ticket 5's surface, not built
here.

**A restaurant with no configured rate or a diner with no platform identity
still gets marked processed, just without an entry.** Without this, every
order at every one of today's zero-configured restaurants would be
re-selected by the sweep on every tick, forever — `loyalty_processed_at`
means "this order has been resolved for loyalty purposes," not "this order
earned points."

**The sweep only ever considers orders this ticket can identify by
CloudWaitress id, which is also what keeps it from trying to process the
entire pre-existing order history on its first run.** `cw_order_id` is only
populated going forward (`createOrder()`'s own change, below); a `WHERE
cw_order_id IS NOT NULL` clause on the sweep's query is therefore also
exactly the PRD's own non-goal ("both accrual and status reconciliation
apply to orders recorded after this ships") enforced structurally, with no
separate cutoff-timestamp constant to maintain.

**Dine-in never creates a platform identity — it only credits an existing
one.** A staff member types a phone number; if no `platform_customers` row
exists for it, the entry is a clear "no platform identity for this number"
result, not a fabricated identity. Auto-enrolling someone into a
phone-verified identity system from an unverified staff claim would be a
real integrity problem (this PRD's own Risks already flags dine-in amounts
themselves as unverifiable — compounding that by also fabricating identity
would be worse, not a mitigation).

**Dine-in lives in `brand-portal`, not `admin-portal`.** `admin-portal` is
AIOrders' own platform-admin surface (`ENG-007`'s config endpoint is
deliberately there, gated `admin`/`sub-admin` only). The PRD's "staff member
with access to a restaurant" is a restaurant-side actor — `brand-portal`'s
own population, gated by `requireRestaurantAccess()` (`brand-portal/utils.ts:117`),
the exact same check `feedback.ts` already uses for a structurally similar
"restaurant staff acts on a customer-linked record" handler.

**Balance is `SUM(points)` on read, not a maintained counter.** AC10 states
balance *as* the sum of entries; at today's volume (zero configured rates on
any restaurant) a denormalized running counter buys nothing and adds a
sync-drift risk class for a value that's trivially cheap to compute from its
own source of truth. Alternatives.

## Components

| Component | Change | Owner agent |
|---|---|---|
| New table `loyalty_ledger_entries` | New | database |
| `orders` | Alter — add `cw_order_id`, `loyalty_processed_at` (additive only) | database |
| New DB function `credit_order_if_eligible(order_id, fulfillment_reason)` | New | database |
| New `pg_cron` schedule `loyalty-auto-complete-tick` | New | database |
| `external-integrations/handlers/cloudwaitress.ts` — `createOrder()` | Modify — persist `orderData._id` into `cw_order_id` | backend |
| `external-integrations/handlers/cloudwaitress.ts` — `handleCloudWaitress()` | Modify — stop discarding `order_completed_updated`/`order_cancelled_updated`/`order_cancel`; resolve the local order by `cw_order_id`, then call the credit function or update status | backend |
| New edge function `loyalty-auto-complete` | New — cron-invoked, claims and processes a bounded batch | backend |
| New `brand-portal/loyalty.ts` | New handler — `record_dine_in_earn`, `get_loyalty_balance` | backend |
| `brand-portal/index.ts` | +2 `case` lines, same pattern as every existing entry | backend |
| `restaurant_loyalty_configs`, `platform_customers`, `platform_customer_legacy_links`, `customers` | None — read-only from this ticket | — |

## Data

Intent and constraints only — `database` owns the schema detail and the
migration (`skills/schema-change/SKILL.md`).

**New table, `loyalty_ledger_entries`.** One permanent row per credit, ever.
Needs: which diner (`platform_customer_id`), which restaurant, how many
points, where it came from (`online_order` | `dine_in`), the online order it
came from when applicable (nullable — must be unique when present, the
department's second, independent guard against double-crediting one order),
the dollar amount the points were computed from, the rate actually applied,
when the underlying spend was treated as earned, and — for the online path
only — why (`reported` vs `window_elapsed`, AC7). For dine-in, which staff
member submitted it (audit, given the PRD's own "dine-in amounts are
unverifiable" risk). Append-only in practice — this ticket never updates or
deletes a row; ticket 5 is where a human correction (a new, opposite-signed
entry) eventually gets a surface, so the schema should not prevent a
negative value later even though this ticket only ever writes positive
ones.

Access pattern: `SUM(points) WHERE platform_customer_id = ? AND
restaurant_id = ?` (balance, AC10) and the same filtered list for history.
Both need an index on that pair. Volume: zero rows today (zero restaurants
have a configured rate), so this is provisioning for a pattern, not a
measured load.

**`orders`, two additive columns.** `cw_order_id` — CloudWaitress's own
order id (`data.order._id` in every webhook payload, currently never
stored), needed to match an inbound terminal-event webhook back to a local
row; should be unique when present (a real question for `database`: whether
CloudWaitress ids are safely assumed globally unique across restaurants —
they read as Mongo-style ids, which would make cross-tenant collision
practically impossible, but this repo has nothing to confirm that). `loyalty_processed_at` —
nullable timestamp, set exactly once, meaning "this order has been resolved
for loyalty" regardless of whether it resulted in a credited entry (see
Approach). Both are populated only for orders inserted after this ships;
no backfill (PRD non-goal).

**Query shapes the migration needs to support**, stated as intent for
`database` to size and index:

- Point lookup by `cw_order_id` (webhook path, one row).
- Batch scan: `cw_order_id IS NOT NULL AND loyalty_processed_at IS NULL AND
  status IS DISTINCT FROM 'cancelled' AND created_at <= now() - interval
  '24 hours'`, ordered by `created_at`, bounded batch size — the sweep's
  claim query. `database` should get real numbers before fixing a batch size
  or tick interval; this design has none to offer beyond `ADR-018`'s own
  200/5-minutes, which was sized for a different table.
- `restaurant_loyalty_configs` and the `customers →
  platform_customer_legacy_links` walk: both existing, read-only, already
  indexed by their own tickets.

**One thing this design cannot resolve and flags for `database`/build time
rather than guessing:** whether `bill.cart` and `bill.discount` (the jsonb
fields `createOrder()` already stores) are in the same unit as `bill.total`
(dollars) or `bill.total_cents` (integer cents) — the `CloudWaitressOrder`
TypeScript interface gives `cart`/`discount` only one field each, with no
`_cents` counterpart the way `total` has both, and a TS interface doesn't
constrain what a real payload actually contains. The approved earn base is
`cart - discount` (pre-tax, post-discount food subtotal); getting the unit
wrong makes every balance in the system wrong by a consistent, invisible
factor. Verify against a real captured payload (or CloudWaitress's own API
docs) before writing the computation, not after.

## Interfaces

**Webhook (modified): `external-integrations`, `handleCloudWaitress()`.**
For `event ∈ {order_completed_updated, order_cancelled_updated,
order_cancel}`: look up the local order by `cw_order_id = data.order._id`.
Not found → same `{success:true, message:'...ignored'}` shape already
returned today (AC14 — a report for an order the platform never recorded is
accepted and ignored, not an error). Found, `order_completed_updated` →
call `credit_order_if_eligible(order.id, 'reported')`. Found,
`order_cancelled_updated` or `order_cancel` → unconditional `status =
'cancelled'` update (Approach). `order_update_status` and the four
booking/ready-time events: unchanged, still discarded (Alternatives).
Response is always `200 {success:true}` regardless of credit outcome — a
business-logic no-op is not a webhook failure (AC13's containment principle
extended to this path).

**DB function (new): `credit_order_if_eligible(order_id uuid,
fulfillment_reason text) → result`.** One transaction: guard
(`loyalty_processed_at IS NULL AND status IS DISTINCT FROM 'cancelled'`,
else return `already_processed`); resolve platform identity (none →
mark processed, return `skipped_no_identity`); resolve the restaurant's
online rate as of the order's own `created_at` (none → mark processed,
return `skipped_not_enrolled`); else compute points from `bill.cart -
bill.discount` at that rate, insert the ledger entry, set `status =
'completed', loyalty_processed_at = now()`, return `credited`. Called
synchronously from the webhook (real-time path) and from the sweep
(fallback path) — one code path, two triggers, which is what makes AC4
("already credited on report, window later elapses → no additional credit")
automatic rather than something either caller has to remember to check.

**Edge function (new): `loyalty-auto-complete`, cron-invoked only.**
Authenticates the same way `ADR-016`–`018` already established for
internal/system calls — `Authorization: Bearer
${SUPABASE_SERVICE_ROLE_KEY}`; anything else → `401`. No body. Selects the
eligible batch (Data), calls `credit_order_if_eligible(id, 'window_elapsed')`
per row in a loop, catching and logging each row's own error rather than
aborting the batch (AC15) — a failure on one order leaves it
`loyalty_processed_at IS NULL`, so the next tick retries it without any
special-case recovery logic. Returns `{claimed, credited, skipped, errors}`
for observability. Schedule: `cron.schedule('loyalty-auto-complete-tick',
'*/15 * * * *', net.http_post(...))`, structurally identical to
`ADR-018`'s `broadcast-dispatch-tick`.

**`brand-portal` action (new): `record_dine_in_earn`.** Payload
`{restaurant_id, phone, amount}`. `requireRestaurantAccess(restaurant_id,
supabase, user)` first — failure → the same 403-shaped error every other
brand-portal action already returns (AC17). `amount` not a positive finite
number → `400`, clear reason, no entry (AC18). Resolve the restaurant's
dine-in rate as of now (none → distinct `not_enrolled` result, no entry,
AC11 — dine-in has a live human caller, so this is a real response, not a
silent success). Resolve `platform_customers` by normalized phone (none →
distinct `no_platform_identity` result, no entry, no identity fabricated —
Approach). Else insert the ledger entry (`source: 'dine_in'`, `created_by:
user.id`, no `order_id`) and return the new balance.

**`brand-portal` action (new): `get_loyalty_balance`.** Payload
`{restaurant_id, phone}`, same access check. Returns `{balance, entries:
[...]}` — the minimal unblock for tickets 4/5, no live caller yet, same
shape `ENG-007`'s own admin-portal read endpoint already used for the same
reason.

**RLS, `loyalty_ledger_entries`:** deny-by-default, service-role only — no
client policy, same choice `ENG-006`/`ENG-007` made on this project. Every
write and read goes through a service-role edge function that does its own
authorization in code (`requireRestaurantAccess`), not through RLS keyed to
the caller's own JWT.

## Alternatives considered

- **Per-order Cloudflare Queue delay (`sendFeedbackQueueMessage`'s own
  mechanism) for the 24-hour window, instead of a `pg_cron` poller.**
  Rejected — see `ADR-021`.
- **A denormalized running-balance column, updated alongside each ledger
  insert, instead of `SUM()` on read.** Rejected at this volume: AC10
  defines balance as the sum, and a maintained counter is a second source
  of truth that can drift from it for zero benefit while every restaurant's
  rate table sits at zero rows. Revisit if the sum ever shows up in a query
  budget.
- **Treating the generic `order_update_status` event as loyalty-significant
  too**, since it's already subscribed alongside the two terminal events.
  Rejected: the PRD's own acceptance criteria and proposed-change section
  name only "fulfilment" and "cancellation" reports as loyalty-triggering;
  this repo has no captured payload showing what `order_update_status`
  actually carries or when CloudWaitress fires it relative to the two named
  events, and guessing at a third trigger's semantics is exactly the kind
  of speculative generality `tech-design/SKILL.md` warns against. It keeps
  being discarded, unchanged from today.
- **Matching inbound terminal events on `(restaurant_id, number)` instead of
  adding `cw_order_id`.** Rejected: `number` is a human-facing order number
  with no guarantee against reuse over time; CloudWaitress's own `_id` reads
  as a stable, globally-unique id from their system. One new column, cited
  by the PRD itself as an open option, is cheap and strictly more correct.
- **A dedicated new edge function for dine-in entry, instead of a
  `brand-portal` handler.** Rejected — `brand-portal` already has exactly
  the auth/access-check machinery this needs (`requireRestaurantAccess`);
  a new function would duplicate it for no benefit, the same reasoning
  `ENG-007` used to prefer `admin-portal` over a dedicated function for its
  own config endpoint.

## One-way doors

**None escalated.** The four decisions that would otherwise have been
one-way-shaped for this ticket — the auto-complete window length, the earn
base, which rate applies, and whether `orders.status` itself becomes the
completion signal — were all already decided by the approver at this
ticket's own second G1 (2026-09-05, bare approval of all four proposed
defaults). This design implements those decisions; it does not reopen them.

The mechanism choice for the sweep (`pg_cron` vs. a per-order delayed
queue message) is real but reversible — `ADR-021`, decided here rather than
escalated, on the same reasoning `ADR-018` itself used for the structurally
identical `broadcast-dispatch` choice ("reversibility: cheap" — swapping the
sweep's internals later changes nothing about `loyalty_ledger_entries`'s own
shape or the webhook path).

Nothing here introduces a new datastore, a new vendor, an auth-model change,
or a public contract — the PRD's own non-goals already exclude any frontend
or external caller for this ticket.

## Risks

- **The `bill.cart`/`bill.discount` unit question (Data)** — carried here
  from Data because it's the one open item that could make every balance
  wrong by a consistent, invisible factor if guessed incorrectly. Verify
  against a real payload before writing the computation.
- **Whether restaurant staff ever actually mark orders complete/cancelled in
  CloudWaitress's own dashboard is unknown from this repo** (PRD's own
  flag, not resolved here — it's an operational fact, not a code fact). If
  they never do, the sweep becomes the sole mechanism and every order waits
  the full 24 hours; this design doesn't change based on the answer, but a
  production log check would confirm which path is actually carrying the
  load once this ships.
- **This is the first write-after-insert path on `orders` in this
  codebase's history, on the live production order webhook** (PRD's own
  framing, re-confirmed independently in Approach: nothing branches on the
  values being written, but a comment or a future reader unfamiliar with
  this ticket could still be surprised the column moves at all). Named
  plainly in the migration's own comment, matching `ENG-006`/`ENG-007`'s own
  convention of documenting "why this exists" on the schema itself.
- **A restaurant enabling loyalty after this ships still won't retroactively
  credit any order recorded before the rate existed** — correct per
  `ENG-007`'s own "not enrolled" semantics and this ticket's own
  no-backfill non-goal, but worth naming so it isn't read as a bug later.
- **Dine-in amounts remain unverifiable** (carried from the PRD, unchanged
  by this design) — no POS integration exists, and this ticket adds no
  technical control against a staff member entering an inflated or
  fabricated amount. Detectable only once ticket 5's support/audit surface
  exists.
- **Two independent per-order timers now exist on the same webhook** — the
  shipped 3-hour feedback-queue delay and this ticket's 24-hour sweep,
  tuned for unrelated reasons. Not a bug, but the kind of thing that reads
  as one to whoever finds it next; named here so it isn't rediscovered cold.

## Rollout

Additive only: one new table, two new nullable columns on `orders`, one new
DB function, one new cron job, two new edge-function surfaces, two new
`brand-portal` actions. No existing table is altered destructively, no
existing column's meaning changes, no existing caller's behavior changes
except that `orders.status` starts reflecting real terminal values instead
of staying frozen at placement (confirmed safe, Approach) — restaurant
owners viewing their order list will, for the first time, see a status that
moves. No frontend anywhere calls any of this yet (PRD non-goal for the
whole sequence), so there is no traffic to cut over and nothing to feature-flag:
the cron job and the two new webhook branches simply start being exercised
by real CloudWaitress traffic the moment this deploys. Rollback is dropping
the new table/columns/function/cron job — nothing else in the codebase
reads or depends on any of them.

## Out of scope

Per the PRD's own non-goals: redemption of any kind and QR issuance (ticket
4); admin/support surfaces and manual ledger correction (ticket 5);
migrating Walletly balances; any frontend in any repo; point expiry; pooled
or cross-restaurant balances; backfilling points or status onto orders
recorded before this ships; setting real earn rates for any restaurant;
automatic reversal/clawback of already-credited points; refunds; detecting
order deletion (no signal exists); acting on `order_update_status` or the
four booking/ready-time events (Alternatives); polling CloudWaitress on a
schedule (the on-demand proxy exists but isn't used here). This design also
does not fix the `bill.cart`/`bill.discount` unit question or pick the
sweep's batch size/tick interval — both named above as open, handed to
build time and `database` respectively rather than guessed here.
