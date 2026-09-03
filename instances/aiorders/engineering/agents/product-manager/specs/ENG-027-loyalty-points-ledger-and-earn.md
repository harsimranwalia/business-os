---
ticket: ENG-027
project: aiorders-api
status: awaiting-scope
size: L
author: product-manager
created: 2026-09-03
decided:
---

# Loyalty points ledger, balances, and earn API — online-order and dine-in accrual

## Readback

**There is no raw request to quote this time, and inventing one would be
worse than saying so.** Every other PRD on this board opens with the
approver's verbatim words. This ticket has none of its own: nobody wrote a
new request for it. It is item 3 of a five-item sequence the approver
reviewed and approved the shape of at `ENG-006`'s G1, and its scope is
already stated precisely — by this department, in a document the approver
read and approved. So the "request" being read back is that text, quoted as
what it is: **the approved sequencing note, not a customer's words.**

**What was approved,** verbatim from
`agents/product-manager/specs/ENG-006-unified-customer-identity.md`,
`## Feature shape and sequencing`, item 3:

> **Points ledger, balances, and earn API** — the points-per-customer-per-restaurant
> record, an earn/redeem transaction history, online-order-triggered
> accrual, and manually-entered dine-in spend and its accrual. Depends on
> ENG-006 (needs an identity to award to) and on (2) (needs a rate).

**And that it stands as a sequence,** verbatim from that PRD's `## Decision`
(the approver's own G1 answer, 2026-08-28): the identity slice proceeds
"and the proposed five-ticket sequence stands as shape to file
incrementally, not as four pre-approved tickets."

**And that this specific ticket is wanted now,** verbatim answer
`approved` / "yes" on
`inbox/2026-08-30-eng007-continue-sequence-question.md`
(2026-09-01T17:02:39): file ticket 3, same process as `ENG-007` — fresh
PRD, its own G1. That is why this ticket exists today rather than waiting.

**Understood as:** Both halves of this ticket's dependency are now shipped
and verified, and neither one does anything on its own. `ENG-006` gave the
platform a single identity per verified phone number that maps onto the
existing per-restaurant customer records. `ENG-007` gave every restaurant an
effective-dated online earn %, dine-in earn %, and redemption value —
and that table currently holds zero rows, because nothing reads it.
This ticket is the piece that connects them: a permanent, append-only
record of points earned, per diner per restaurant, credited automatically
when an online order is recorded and manually when a staff member enters a
dine-in amount, each computed against whichever rate was in effect at the
moment it happened. Balances are readable per diner per restaurant.
Nothing here spends points.

**Assumed, and worth correcting if wrong** (only the ones that change the
build, not its details):

- ~~**Points accrue when an order is recorded, because that is the only
  signal the system has.**~~ **Superseded 2026-09-03 by the approver's
  `changed` answer — and the reasoning behind it was partly wrong. See
  "Approver's `changed` response" below, fact 3:** the database has no
  completion signal, but AIOrders' own CloudWaitress webhook registration
  already *subscribes* to `order_completed_updated`, `order_cancelled_updated`,
  `order_cancel` and `order_update_status`, and the handler discards them.
  The signal does not have to be built; it has to stop being ignored. The
  original text of this assumption read: "the CloudWaitress `order_new`
  webhook is the *only* thing that ever writes an order, and there is no
  update or delete path for an order anywhere in the codebase … If points
  must only land once an order is actually fulfilled, that signal has to be
  built first and this ticket becomes materially larger." The first clause
  is still exactly true; the inference drawn from it was not.
- **What the earn % applies to is unresolved, and this is where it stops
  being theoretical.** The order record carries a bill total (which
  includes taxes and fees), a separate tip figure, a cart figure, and a
  discount figure. `ENG-006`'s second reading flagged this and `ENG-007`
  deliberately left it open. Proposed here: **the pre-tax, post-discount
  food subtotal — excluding tax, fees, delivery and tip.** That is the
  common restaurant-loyalty convention and it avoids paying a diner points
  for the government's share. Stated as a proposal because the approver has
  never been asked; correcting it at this G1 is cheap and correcting it
  after diners have balances is not.
- **A diner with no platform identity earns nothing, silently.** Most
  existing customers have never done phone/OTP verification, so most orders
  today would resolve to nobody. That is not an error condition — the order
  is recorded exactly as it is now and no points are credited.
- **A restaurant with no configured rate earns nothing.** `ENG-007` already
  established "not enrolled" rather than a default rate or an error, and
  this ticket inherits that meaning rather than reinterpreting it. Today
  that describes every restaurant.
- **Ledger entries are never edited or deleted.** A correction is a new,
  opposite entry, not a rewrite. The surface for making one by hand is
  ticket 5; the property that makes it possible belongs here.
- **Balances are per diner per restaurant, keyed on the restaurant the
  transaction happened at** — never on whatever restaurant or brand the
  legacy customer record happens to be scoped to. Points never move between
  restaurants, per `ENG-006`.

**Second reading:** none run for this ticket, and that is deliberate rather
than skipped. `skills/request-readback/SKILL.md` exists to catch two careful
readers disagreeing about ambiguous raw input; there is no raw input here.
The two readings that mattered were run at `ENG-006`, converged with no
material divergence, and independently produced this same ticket 3 — that
is the reading this PRD is written from.

---

## Approver's `changed` response (2026-09-03T16:00:32Z) — accrual moves to fulfilment

The approver's G1 answer (`decision: changed`, full text in
`inbox/_handled/2026-09-03-eng027-g1-scope.md`'s `## Decision` section) is
two clauses:

> Accrual at fulfillment, have ticket completed as autocompleted after x
> hours if not cancelled or deleted.

This is not an edit and not a rejection. It takes the fork the first G1
named explicitly — *"If you want accrual on fulfilment instead, that signal
has to be built first and this ticket goes from `M` to `L`"* — picks the
second branch, and then supplies its own mechanism for the missing signal:
an order auto-completes on a timer unless it was cancelled or deleted
first.

**Five load-bearing facts, verified against live `aiorders-api` before
anything below was written. Four were absent from the original evidence;
the third contradicts its central inference.**

1. **The local `orders.status` column is a frozen snapshot, written once.**
   `supabase/functions/external-integrations/handlers/cloudwaitress.ts`,
   `createOrder()` (line 188), inserts `status: orderData.status` (line 195)
   straight from the CloudWaitress webhook payload — `unconfirmed`,
   `confirmed`, whatever the vendor said at that instant. Nothing ever
   writes it again.

2. **No code path anywhere in the repo updates or deletes an order row.**
   Eleven `from('orders')` call sites across seven edge functions: ten are
   `.select(...)`, one is the `.insert(...)` above. Zero `.update(`, zero
   `.delete(`. The original PRD's claim holds, and is stronger than it
   stated — this ticket would introduce the first write-after-insert on
   `orders` the codebase has ever had.

3. **But the completion and cancellation signals are already arriving at
   the production endpoint and being thrown away.** This is the finding
   that reshapes the ticket. `handleCloudWaitress()` (line 220) discards
   every event that isn't `order_new` at line 238 —
   `if (webhookData.event !== 'order_new') { return ... 'Event ${webhookData.event} ignored' }`
   — and the original PRD read that as *"there is no order-completion
   signal in the system."* But AIOrders' **own webhook registration
   subscribes to nine events, not one.**
   `cloudwaitress-middleware/handlers/restaurant.ts`'s `AIORDERS_WEBHOOK`
   constant (line 6) sets `order_update_status`, `order_cancel`,
   `order_completed_updated` and `order_cancelled_updated` all to `true`
   alongside `order_new`, and `handleAddWebhook()` (line 93) is what writes
   that object into each restaurant's CloudWaitress account. **The
   fulfilment signal the approver is asking for does not have to be built.
   It has to stop being ignored.**

4. **A scheduled sweep is not a new category of infrastructure here —
   there are two shipped precedents, and one of them is already a per-order
   timer.** `supabase/migrations/20260217000001_platform_analytics_cron.sql`
   enables `pg_cron` and `pg_net` and schedules
   `cron.schedule('platform-analytics-hourly', '0 * * * *', ...)` against an
   edge function; `20260408000001_google_review_history.sql` does the same
   monthly. Closer still: the same `order_new` handler already schedules a
   **delayed per-order callback** — `sendFeedbackQueueMessage(orderId)`
   (line 274), whose default delay is `3*60*60` seconds, three hours
   (`external-integrations/utils/cloudflare-queue.ts` line 73). An
   auto-complete-after-X-hours job is a shape this codebase already runs,
   twice, two different ways.

5. **The authoritative current status is also readable on demand today.**
   `cloudwaitress-middleware/handlers/orders.ts` proxies CloudWaitress's own
   API: `handleGetOrder()` (line 56) fetches one order's live document,
   `handleGetOrders()` (line 7) lists them filtered by `status`, and
   `handleUpdateOrder()` (line 92) writes status back — each authenticated
   by a per-restaurant token that `utils/token.ts`'s `getRestaurantToken()`
   resolves and auto-refreshes from a reseller credential. So a missed
   webhook is recoverable through shipped code rather than a new
   integration.

### The gap in "if not cancelled or deleted", named rather than assumed away

Read strictly against the code as it stands, **the approver's own condition
is vacuous.** Nothing in the system can mark an order cancelled or deleted
(fact 2), so "if not cancelled or deleted" is always true, and a timer-only
sweep would credit points on *literally every order* X hours after
placement — the same accrual-integrity exposure as placement-time accrual,
delayed by a fixed window. Building it that way and calling the clause
satisfied would be a silent misread of the answer.

Fact 3 is what rescues it. **Cancellation becomes a real condition** the
moment the handler stops discarding `order_cancel` and
`order_cancelled_updated` — no new vendor, no new subscription, no new
signal, just a branch where there is currently a `return`. That is the
resolution this rescope recommends, and it is genuinely lighter than the
alternative it replaces: it costs less than building a cancel-marking
capability from scratch, and unlike a forward-compatible-but-inert `WHERE`
clause it is *true on the day it ships* rather than decorative. (A no-op
condition was considered and rejected. `ENG-007`'s rate table sitting at
zero rows was inert-but-correct — nothing read it, so nothing was wrong.
A cancellation check that can never fire is worse than inert: it looks like
a safety property while being none.)

**Deletion is not rescued.** There is no `order_delete` in the subscription
list and no deletion signal at any layer of this integration. The fallback
window is the only protection against a deleted order, and that is a limit
of the vendor's event set, not a design choice. Named plainly rather than
quietly folded into "cancelled."

And one operational fact this department **cannot verify from code and will
not assert**: whether restaurant staff actually mark orders complete or
cancelled in the CloudWaitress dashboard. The vocabulary is real —
`order-flow/utils/order-mapping.ts`'s `mapOrderStatus()` (line 167) maps
`'complete' → 'completed'` and `'cancelled' → 'cancelled'`, though that is
the KitchenHub kitchen-display bridge, a *different* integration from the
customer order record loyalty attaches to, and it proves only that the
terms exist in CloudWaitress's API vocabulary. Whether the events fire in
practice for these restaurants needs a production log check, not a code
read. This is why the timer is load-bearing rather than a safety net: if no
restaurant ever marks anything, the sweep *is* the mechanism and the
cancellation branch never runs.

**One further mechanical gap:** the local row carries no CloudWaitress order
id. `createOrder()` stores `number` but not `orderData._id`; that id appears
only in the handler's HTTP response body (line 332), never persisted.
Matching an inbound terminal event back to a local row therefore needs
either that id stored going forward or a match on
`(restaurant_id, number)`. Small, but real — and it is why reconciliation
applies to orders recorded after this ships, which the existing "no
backfilling" non-goal already covers.

### Sizing verdict: `L`, one ticket — not the `M` this was, not `XL`

The first G1's warning priced a capability that turns out to be already
subscribed and already delivered to a live endpoint, with two shipped
scheduling precedents in the same repo (facts 3 and 4). So the honest
number is **below** what that warning implied — this is not automatically
`L`-because-we-said-so, and it is nowhere near `XL`.

It is above `M`, though. On top of the ledger the original already sized
`M`, this adds two mechanisms that ticket did not have: the first
write-after-insert path on `orders` in this codebase's history, hanging off
the live production order webhook, and a scheduled sweep with its own
idempotency and failure semantics. It also moves the accrual trigger point,
which is exactly where double-crediting bugs live.

It stays **one ticket** rather than going back to be split
(`prd-writer/SKILL.md` step 7 sends only `XL` back): one project, one new
data model — the ledger, already in scope — no new vendor, no cross-repo
surface. And splitting "order lifecycle" from "loyalty ledger" would ship a
ledger that credits at the moment the approver has just rejected; the two
halves are not independently useful in the order they would land.

**One thing this incidentally fixes, named as a benefit rather than left to
look like scope creep:** `brand-portal/onlineOrders.ts`'s
`get_online_orders` and `get_customer_orders` (lines 56 and 135) return
`status` straight from the local row. Every restaurant owner reading their
order list today is looking at a status that was correct once, at
placement, and has never changed since. Reconciling terminal events onto
the order row makes that column true for the first time.

---

## Problem

`ENG-006` and `ENG-007` are both shipped, verified, and inert. There is one
identity per verified phone with nothing to award it, and a per-restaurant
rate table holding zero rows that nothing in the system reads. Nothing
anywhere records that a diner earned anything, so the loyalty program the
approver asked for does not yet exist in any observable form — and dine-in
spend, which the approver named explicitly, is still entirely invisible to
the platform.

There is also a live clock on this. The points AIOrders' restaurants
currently run are held by a third-party vendor (Walletly) that the approver
confirmed at `ENG-007`'s G2 is "being retired/replaced." Checked in the
repo rather than assumed: that integration is a pure pass-through proxy to
the vendor's own API — **no points are stored in AIOrders' database at
all.** When the vendor goes, the platform has nothing of its own to hold
points in unless this ticket ships first.

## Why now

Item 3 of the sequence the approver approved the shape of, and the approver
answered "yes" on 2026-09-01 to filing it now specifically. It is also the
first item in the sequence that produces anything observable — items 1 and
2 are pure foundation. And the one risk that could have blocked or reshaped
it, the live Walletly integration discovered during `ENG-007`'s design, was
resolved at `ENG-007`'s own G2 in this ticket's favour: the vendor is being
replaced, so there is no dual-system conflict to design around.

Said plainly: no restaurant is asking for this today and no launch date
exists. This is sequenced work the approver initiated, which is a fair
reason to build something.

## Users

Not directly user-facing. Nothing a diner or a restaurant operator can see
changes when this ships — there is no UI in any repo for the whole
sequence, by the approver's own instruction. The eventual users are diners
(who accumulate a restaurant-specific balance), restaurant operators (who
fund and eventually enter dine-in amounts), and AIOrders support (ticket 5).
The immediate consumer is ticket 4, which cannot exist without a balance to
spend.

## Proposed change (rescoped — accrual at fulfilment)

After this ships, a diner who has verified their phone number accumulates
points at a restaurant when an online order they placed there is
**fulfilled**, and when a staff member records a dine-in amount for them —
each earning at that restaurant's own rate, into a balance that is specific
to that restaurant and never mixes with any other. Every credit is a
permanent line in a history that says how much was spent, what rate
applied, when the order was treated as fulfilled, and what caused it, and
that no later rate change can rewrite. Balances and history can be read
back per diner per restaurant.

An online order becomes fulfilled one of two ways, in this order of
precedence:

- **CloudWaitress says so.** The platform stops discarding the completion
  and cancellation events it is already subscribed to. A completion credits
  the order; a cancellation permanently disqualifies it.
- **Nothing said anything and the window elapsed.** If neither a completion
  nor a cancellation has arrived within the auto-complete window, the order
  is treated as fulfilled and credited. This is the approver's
  "autocompleted after x hours," and given the operational unknown above it
  may in practice be the path most orders take.

Either way, an order is credited **at most once, ever**.

Dine-in is unchanged: there is no fulfilment step to wait for, so a
staff-entered amount accrues on submission.

Nothing can be spent. Points only go up.

## Acceptance criteria (rescoped)

Criteria 1, 6 and 9 of the original set assumed accrual at order recording
and have been re-derived. Criterion 2 (dine-in) is carried over unchanged —
dine-in has no fulfilment step, so the approver's change does not touch it.
Criteria 3–5 and 7–11 are carried over with only the wording needed to keep
them true under the new trigger. Everything numbered 12 and above is new,
and exists to pin down the sweep and the terminal-event path.

**Accrual, online:**

1. `[stated]` Given a diner with a platform identity placed an online order
   at a restaurant that has an effective loyalty configuration, when that
   order is reported **fulfilled**, then points are credited to that
   diner's balance at that restaurant, computed from the restaurant's
   **online** earn rate.
2. `[stated]` Given an online order is reported **cancelled**, when that
   report is processed, then no points are credited for that order, then or
   at any later time — including after the auto-complete window elapses.
3. `[stated]` Given an online order for which neither a fulfilment nor a
   cancellation has been reported, when the auto-complete window has
   elapsed since the order was placed, then the order is treated as
   fulfilled and points are credited exactly as in criterion 1.
4. `[proposed]` Given an online order already credited on a fulfilment
   report, when its auto-complete window later elapses, then no additional
   points are credited.
5. `[proposed]` Given any sequence of repeated, duplicated, or
   out-of-order fulfilment and cancellation reports for a single order,
   when they are all processed, then that order has been credited at most
   once, ever, and a cancellation anywhere in that sequence means it was
   credited zero times.

**Accrual, dine-in (unchanged by the rescope):**

6. `[stated]` Given a staff member with access to a restaurant records a
   dine-in amount for a diner with a platform identity, when it is
   submitted, then points are credited to that diner's balance at that
   restaurant, computed from the restaurant's **dine-in** earn rate in
   effect at that moment.

**What an entry records, and what can't change it:**

7. `[inferred]` Given points are credited by either path, when the entry is
   written, then it permanently records the spend amount, the rate applied,
   whether it came from an online order or a dine-in entry, a reference to
   what caused it, and — for an online order — the moment and the reason it
   was treated as fulfilled (reported, or window elapsed).
8. `[proposed]` Given a restaurant's rate changed between an online order
   being placed and that order being credited, when the points are
   computed, then the rate used is the one in effect **when the order was
   placed**, not when it was credited.
9. `[inferred]` Given a rate change is configured for a restaurant after an
   entry was written, when that entry is read back, then it still reports
   the rate that was applied at the time and the same number of points —
   the change has no effect on it.
10. `[inferred]` Given a diner has entries at more than one restaurant,
    when their balance at one restaurant is read, then it equals exactly
    the sum of their entries at that restaurant and is unaffected by any
    entry at any other.

**Who earns nothing, and silently:**

11. `[inferred]` Given a restaurant that reads as not enrolled (no
    configuration), when one of its online orders is fulfilled or a dine-in
    amount is submitted for it, then no points are credited, no entry is
    created, and the dine-in caller is told why rather than receiving a
    silent success.
12. `[inferred]` Given an online order placed by a customer with no linked
    platform identity, when that order is fulfilled by either path, then no
    points are credited and no entry is created, and the order itself is
    unaffected.

**Blast-radius containment — the reason several of these exist:**

13. `[proposed]` Given point accrual or order-status reconciliation fails
    for any reason at all, when an online order arrives, then the order is
    still recorded successfully — neither can ever block, fail, or reject
    the recording of an order.
14. `[proposed]` Given a fulfilment or cancellation report for an order the
    platform has no record of, when it is processed, then it is accepted
    and ignored without error and nothing is created.
15. `[proposed]` Given the auto-complete sweep fails while processing one
    order, when it continues, then the remaining eligible orders are still
    processed, and a subsequent run retries the failed one without
    double-crediting any order it already credited.
16. `[proposed]` Given a cancellation is reported for an order whose points
    were already credited, when it is processed, then the existing ledger
    entry is not deleted or rewritten — correction remains a new, opposite
    entry made by hand (ticket 5).

**Dine-in input validation (unchanged):**

17. `[proposed]` Given a staff member submits a dine-in amount for a
    restaurant they do not have access to, when it is submitted, then it is
    rejected and no entry is created.
18. `[proposed]` Given a dine-in amount that is zero, negative, or not a
    number, when it is submitted, then it is rejected with a clear reason
    and no entry is created.

## Non-goals

- **Spending points — redemption of any kind, and QR code issuance or
  scanning.** Ticket 4. This ticket has no redemption surface at all;
  the redemption value `ENG-007` stores is not read here.
- **Admin and support surfaces** — internal lookup, the cross-restaurant
  support view, and manual ledger adjustment or void. Ticket 5. This
  ticket makes correction *possible* (entries are append-only, so a
  correction is a new opposite entry) but builds no surface for anyone to
  make one.
- **Migrating existing point balances out of Walletly.** Not this ticket,
  and this is a deliberate call rather than an omission — see Risks. The
  ledger starts at zero for everyone.
- **Any frontend in any repo**, including the restaurant-portal staff
  screen that will eventually drive the dine-in entry this ticket exposes.
  Deferred for the whole sequence by the approver.
- **Point expiry**, in either direction. Not built, not scheduled.
- **Any pooled, transferable, or cross-restaurant balance.** Earned at a
  restaurant, held at that restaurant.
- **Backfilling points for orders already in the system**, and backfilling
  a true status onto orders already recorded. Both accrual and status
  reconciliation apply to orders recorded after this ships.
- **Setting real earn rates for any real restaurant.** `ENG-007` built the
  capability; nobody has used it, and this ticket does not either.

**Added at the rescope** (the previous non-goal "changing when an order is
considered complete, or adding a cancellation or refund path" is
**superseded** — the completion and cancellation halves of it are now this
ticket's core; what remains out is narrower and listed here):

- **Automatic reversal or clawback of points already credited**, when a
  cancellation arrives after the fact. Entries stay append-only; the
  correction is a manual opposite entry whose surface is ticket 5. The
  rescope makes this case *rarer* than placement-time accrual did, not
  impossible — see Risks.
- **Refunds and partial refunds.** No signal exists for either, they are
  not the same event as a cancellation, and nothing here models them.
- **Detecting order deletion.** No deletion signal exists at any layer;
  the approver's "or deleted" is unbuildable as stated. Named in the
  rescope section and in Risks rather than silently folded into
  "cancelled."
- **Acting on the other webhook events AIOrders subscribes to but
  discards** — `booking_new`, `booking_update_status`, `booking_cancel`,
  `order_update_ready_time`. They keep being ignored; only the terminal
  order events are picked up.
- **Any customer- or owner-facing surface for order status.** The order
  record's status becoming true for the first time is a data correction
  that existing screens read; it is not a new screen, a notification, or a
  status-change alert.
- **Reconciling status by polling CloudWaitress on a schedule.** The
  on-demand proxy exists (rescope fact 5) and is worth knowing about, but
  this ticket consumes pushed events and a local timer, not a poll.

## Risks and unknowns (rescoped)

- ~~**Points accrue at order placement, not at fulfilment**~~ — resolved by
  the approver's `changed` answer; superseded by the four risks immediately
  below, which are what that resolution costs.
- **The whole fulfilment path may quietly degrade to a timer, and nobody
  here can tell in advance.** Everything above rests on CloudWaitress
  actually emitting `order_completed_updated` / `order_cancelled_updated`
  for these restaurants — which requires restaurant staff to mark orders in
  the CloudWaitress dashboard. AIOrders subscribes to those events by
  design (rescope fact 3); whether they *fire* is an operational fact
  readable only from production logs, and the current handler discards them
  without recording that they arrived, so this repo holds no evidence
  either way. **If they never fire, the auto-complete sweep becomes the
  sole mechanism and "if not cancelled" never once evaluates false** —
  landing exactly where a timer-only build would have, just honestly. First
  thing to check at design time; cheap to check, and it changes nothing
  about whether to build.
- **"Deleted" has no signal and will not have one.** No `order_delete`
  event exists in the subscription; no deletion path exists locally. Half
  the approver's stated condition is unbuildable, and the auto-complete
  window is the only thing standing between a deleted order and its points.
- **A late cancellation still can't claw points back automatically.** If a
  cancellation arrives after the window elapsed and points were credited,
  the entry stands and correction is a manual opposite entry (ticket 5).
  The rescope shrinks this from *every* cancelled order to *only those
  cancelled after the window*, which is a real improvement, not a fix.
- **This adds the first write-after-insert on `orders` in the codebase's
  history, on the live production order webhook.** Eleven call sites read
  that table today (rescope fact 2) and none of them have ever seen the
  status change. The most visible consequence is a behaviour change for
  restaurant owners: `brand-portal`'s two order-listing actions return
  `status` from that column, so owners who have only ever seen one frozen
  value will start seeing it move. That is a fix, but it is a fix arriving
  through a loyalty ticket, which is worth saying out loud.
- **The auto-complete window is a money-adjacent number chosen without
  data.** No fulfilment-time measurement exists in the platform. The only
  empirical anchor is the three-hour delay the shipped feedback queue
  already uses on this exact webhook — a different question ("is the meal
  over?") answered by whoever wrote that line, with no recorded reasoning.
- **Two independent per-order timers will exist on the same webhook** —
  the shipped 3-hour feedback delay and this one — tuned differently for
  different reasons. Minor, but it is the kind of thing that reads as a bug
  to whoever finds it next.
- **The join key is missing.** The local order row stores no CloudWaitress
  order id (rescope fact, `createOrder()` persists `number` but not
  `orderData._id`), so matching an inbound terminal event to a local order
  needs that id stored going forward or a `(restaurant_id, number)` match.
  Cheap; a real design decision, not a detail.
- **Walletly balances become unreachable when the vendor is switched off,
  and this ticket does not save them.** The integration holds nothing
  locally — it proxies the vendor's API. Whether AIOrders honours the
  points diners have already accumulated is a commercial decision about
  customer goodwill, not an engineering one, and it is not in the shape
  the approver approved for this ticket. But it is **time-sensitive**: once
  the contract lapses, an export may not be possible at any price. If the
  answer is "yes, honour them," that is a separate ticket that should be
  filed before the vendor goes, not after.
- **The earn base is a money decision being made by inference, and it is
  still open.** See the readback's second assumption. The first G1 asked
  what the earn % applies to and proposed the pre-tax, post-discount food
  subtotal; the `changed` answer addressed accrual timing and said nothing
  about the base. Per this department's standing rule, **silence is not
  approval** — it is carried forward to the fresh G1 as an open question,
  not treated as settled. Wrong here means every balance in the system is
  wrong by a consistent, invisible margin.
- **Which moment's rate applies is a new question the rescope creates.**
  Under placement-time accrual, placement and accrual were the same instant
  and "the rate in effect at that moment" was unambiguous. They are now
  hours apart, and a rate change in between makes them differ. Criterion 8
  proposes the rate at placement — what the diner could in principle have
  been told when they ordered, and deterministic regardless of when the
  sweep runs. Small, rare, and free to fix now.
- **Dine-in amounts are unverifiable.** There is no POS integration —
  `ENG-006` assumed this and it is still true. A staff member types a
  number and the platform credits it. That is an abuse surface (staff
  inflating their own or a friend's balance) with no technical fix
  available at this scope; it needs the support/audit surfaces of ticket 5
  to become detectable.
- **The dine-in path has no operator until the portal work lands.** It will
  be exercised by tests and nothing else, possibly for months. Code that
  has never been used in anger is the code most likely to be wrong when it
  finally is.
- **This is the first money-adjacent write path this department has added
  to `aiorders-api`**, the project `config/projects.md` calls "highest
  blast radius of the set," and it hangs off the live production order
  webhook. Criterion 9 exists because of this.
- **PIPEDA**, unchanged from `ENG-006`: a per-restaurant spend history tied
  to a verified phone number is a more sensitive record than an order log,
  and it is being built before any consent or opt-out surface exists.

## Cost

- **Build: `L`** — several days to a week. Re-derived at the rescope, not
  inherited from the original `M` and not taken from that PRD's own
  `M → L` warning, whose stated reason ("building an order-completion
  signal that does not exist") turned out to be wrong: the signal is
  already subscribed and already delivered (rescope fact 3), and the
  scheduler has two shipped precedents in the same repo (fact 4). What
  actually earns the `L` is what sits on top of the original `M` — the
  first write-after-insert path on `orders` in this codebase's history,
  hanging off the live production webhook, plus a scheduled sweep with its
  own idempotency and failure semantics, plus moving the accrual trigger
  point. Still comfortably short of `XL`: one project, one new data model,
  no new vendor, no cross-repo surface — so it proceeds whole rather than
  going back to be split, unlike `ENG-016`'s rewrite.
- **What it displaces:** nothing at build time — machine WIP is 0/1 and
  free. At the approver's desk it is a sixth item against a cap of two.
  The honest competitor on the board is **`ENG-022`** (`type: security`,
  `severity: P0`, `designed`) — cross-tenant PII and write exposure on five
  live brand-portal handlers. If the approver has attention for exactly one
  thing, it is not this ticket. Going from `M` to `L` roughly doubles the
  build and makes that comparison worse, not better.
- **Run: `$0`/month.** Checked, not assumed. Same Supabase project, no new
  vendor, no new infrastructure. The two vendors adjacent to this feature
  are unaffected: the SMS vendor from `ENG-006` is fixed-cost and unlimited
  and this ticket sends no messages, and Walletly is on its way out. The
  only cost movement in this feature area is **downward**, when the vendor
  this replaces is retired.

## Recommendation (rescoped)

**Build the approver's version now**, one ticket, `L` — several days to a
week. Accrual on fulfilment, driven primarily by the CloudWaitress
completion and cancellation events AIOrders already subscribes to and
currently discards, with the auto-complete timer as the fallback for orders
that never get a terminal event. That combination gives the approver
exactly what they asked for *and* makes the "if not cancelled" condition
mean something, which a timer-only build could not.

**Four riders to answer inline rather than at a second gate** (same bar
`ENG-015`/`ENG-016`/this ticket's own first G1 used):

1. **How long is "x hours"?** It is a literal unfilled placeholder in the
   answer. **Proposed: 24 hours.** With terminal events live, the timer
   only catches orders whose restaurant never marked them anything — and
   those same restaurants won't send a cancellation either, so a longer
   window buys the only protection available. It costs nothing observable:
   points are unspendable until ticket 4 and no screen shows a balance, so
   a day's delay is invisible today. The alternative anchor, if the
   approver wants points same-day, is the **3 hours** the shipped feedback
   queue already uses on this exact webhook.
2. **What does the earn % apply to?** Still open — the first G1 asked, the
   `changed` answer didn't address it, and silence is not read as approval.
   **Proposed, unchanged: the pre-tax, post-discount food subtotal**,
   excluding tax, fees, delivery and tip.
3. **Which moment's rate?** New, created by the change itself. **Proposed:
   the rate in effect when the order was placed**, not when it was
   credited. Smallest of the four.
4. **Does the order's own status become true, or does loyalty keep a
   private view?** **Proposed: the order's own status.** Two disagreeing
   answers to "was this order completed" is worse than one, the terminal
   events genuinely belong on the order row, and it fixes the frozen-status
   staleness restaurant owners see today. The cost is honest: this ticket
   then writes to a table eleven read sites depend on.

**Unchanged from the first G1, and still true:** this is not the most
urgent item on the board. `ENG-022` (`type: security`, `severity: P0`,
cross-tenant PII and write exposure, already `designed`) outranks it if the
approver's attention is scarce — more so now that this one costs `L`.

## The 5-question filter, answered honestly

Read `knowledge/business-profile.md` fresh this run. AIOrders sells
independent Canadian restaurants commission-free direct ordering and
**owned customer relationships** against UberEats/DoorDash/SkipTheDishes;
loyalty and repeat-customer strategy sits inside its own answerable domain.

1. **Work off the approver's plate, or onto it?** Adds, mildly and
   permanently — a points ledger is a liability the business will answer
   questions about ("why does this customer have 40 points?") forever.
   Real offset: this replaces a *rented* system with an *owned* one, and
   the vendor holding today's points is being retired regardless of
   whether this ledger is built. Net: additive, with the alternative also
   additive and more expensive.
2. **Freedom created or removed?** Both. Real freedom: loyalty data becomes
   AIOrders' own rather than a third party's — literally the product's own
   pitch, applied to itself. Also the highest-consequence surface this
   department has added to `aiorders-api`: an append-only money-adjacent
   table hanging off the live production order webhook — a permanent
   recurring cost of attention.
3. **Current problem, or anticipated?** Mostly anticipated — no restaurant
   is asking, no launch date, no pilot, zero configured rates. One
   genuinely current pressure: the incumbent vendor is being retired with
   nothing to replace it.
4. **What does it displace?** Nothing at build time (machine WIP 0/1,
   free). At the approver's desk, item six against a cap of two. The
   honest competitor is `ENG-022` — a live tenant-isolation hole outranks
   a sequenced feature.
5. **Would not building it be fine?** Not indefinitely — it strands two
   verified tickets with nothing to show for them. But delaying it behind
   `ENG-022` would be completely fine, and that's worth saying plainly
   rather than pretending this sequence has urgency it doesn't.

**Filter verdict:** build it, and say out loud that it isn't the most
urgent thing on this board.

**Re-checked at the rescope (2026-09-03).** Three of the five answers move,
none of them enough to flip the verdict:

- **(2) Freedom.** Worse. The original added an append-only table beside
  the order webhook; this also puts the department's first mutation path on
  a table eleven read sites depend on, and a recurring scheduled job. More
  surface, permanently.
- **(4) Displacement.** Worse. `M → L` roughly doubles the build, against
  an unchanged `ENG-022` sitting `designed` at `P0`.
- **(1) Work on or off the plate.** Slightly better, and this is the
  genuine gain. Under the original scope, every cancelled order needed a
  human correcting entry forever. Under this one, most cancellations are
  handled by a signal already being delivered — the manual case shrinks to
  cancellations landing after the window.

Net: a more expensive ticket that is more correct where it matters, on a
board where it is still not the top item. Verdict holds: build it, say so
plainly.

## Decision

Filled in by the approver.

- **The approver's answer:**
- **Date:**
- **Notes:**
