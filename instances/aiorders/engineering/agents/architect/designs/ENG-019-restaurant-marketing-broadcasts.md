---
ticket: ENG-019
project: restaurant-portal
author: architect
created: 2026-09-03
adrs: [ADR-018, ADR-019, ADR-020]
one_way_doors: []
touches_data: true
touches_models: false
---

# Restaurant marketing broadcasts — mass send and drip sequences — technical design

## Approach

A new **"Broadcasts"** tab on the brand portal's existing `Automations` page,
backed by one new `brand-portal` action file (`broadcasts.ts`, following the
exact precedent `ADR-011` already set: an owner-facing capability is a
`brand-portal` action, not a new edge function), three new tables, and one
new recurring dispatcher. An owner composes a one-time message or a
multi-step drip, picks an audience (all customers, or inactive-for-N-days),
optionally attaches an existing offer's coupon code, and sends now or
schedules for later. A `pg_cron` poller — structurally identical to the
already-live `platform_analytics_cron` — wakes every 5 minutes, resolves any
campaign whose scheduled moment has arrived into a concrete recipient list,
and dispatches due sends through the same `outgoing-communications` primitives
every existing automated send already uses. Redemption/revenue reporting
reads `orders` directly; it does not write anything new to it.

Four findings from reading `origin/main`, `agents/architect/decisions/`, and
`agents/eng-manager/observations.md` shaped this rather than the obvious
version.

**The PRD's own ROI mechanic doesn't exist yet, but the data it needs
already lands.** The PRD's Assumed section reads AC4 as "reusing the exact
mechanic the existing offers already use" — implying a redemption-tracking
system to reuse. It doesn't exist: `offers.coupon_code` is a plain display
string everywhere in this codebase (`brand-portal/offers.ts`,
`outgoing-communications`' three offer-sending paths,
`config-site-builder/src/pages/Offers.tsx`'s own copy-to-clipboard button).
The actual checkout system is CloudWaitress, not this codebase. But
CloudWaitress's `order_new` webhook already reports which promo codes an
order used, and `external-integrations/handlers/cloudwaitress.ts`'s
`createOrder` already persists that array (`orders.promos`) plus
`total_amount`/`created_at`, scoped to `restaurant_id`/`customer_id`, on
every order — since before this ticket, for order history, not ROI. AC4 is
a read against data that already exists, not a new capture path. **ADR-019.**

**This platform's two proven durable-delay mechanisms are proven at
different scales, and this ticket's scale is the one neither was built for.**
`autopilot/marketing/utils.ts`'s `scheduleWithQStash` is proven at one message
per lifecycle event — a single customer, naturally spread over time by when
each trigger fires. `platform_analytics_cron` is proven at one recurring
aggregate tick. A broadcast is neither: one owner action can enroll an
entire customer list at once. Scheduling that via QStash means thousands of
publish calls per campaign before a single message goes out, and a "pause"
means deleting each one individually. A `pg_cron` poller claiming a bounded
batch of due rows per tick decouples audience size from any single HTTP call
or compose-time action — the aggregate-job shape, applied to a queue instead
of a rollup. **ADR-018.**

**The CASL consent this PRD's Risks section asks about is already captured,
just never enforced.** `customers.consent_email`/`consent_sms` — JSONB,
`{consent: boolean, consent_at, ...}` — are already written on every
customer at creation (`findOrCreateCustomer`: `consent: true, source:
'online-order'`, the exact "existing order relationship" reasoning the PRD's
Risks section argues in prose). No sender on this platform checks either
field today. Broadcasts becomes the first one to. **ADR-020.**

**Naming collision, already confirmed by the PM at shaping time and
reconfirmed here.** `pages/campaigns/*`/`influencer_campaigns` is a real,
unrelated, shipped feature (inviting influencers to visit and post). This
design uses "Broadcast"/`broadcast_campaigns` throughout and touches no file
under `pages/campaigns/` or the `influencer_campaigns` table.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `aiorders-api`: `supabase/migrations/{ts}_broadcast_campaigns.sql` | new — `broadcast_campaigns`, `broadcast_campaign_steps`, `broadcast_campaign_recipients`; `cron.schedule('broadcast-dispatch-tick', ...)`. See Data | database |
| `aiorders-api`: `supabase/functions/brand-portal/broadcasts.ts` | new — `handleBroadcasts(action, payload, supabase, user)`; ownership check via this directory's own `requireRestaurantAccess`, CRUD + send/pause/cancel + report | backend |
| `aiorders-api`: `supabase/functions/brand-portal/broadcasts.test.ts` | new — access-denied, cross-tenant audience leak, empty-audience, malformed step delay, edit-after-active-rejected cases | backend |
| `aiorders-api`: `supabase/functions/brand-portal/index.ts` | modify — import + route `broadcasts_*` actions to `handleBroadcasts`, same shape as the existing `offers`/`catering` lines | backend |
| `aiorders-api`: `supabase/functions/broadcast-dispatch/index.ts` | new — `pg_cron`-invoked, service-role-bearer gated (matches `ADR-016`/`ADR-017`). Promotes due campaigns, claims a bounded batch of due recipient rows, sends via `outgoing-communications`, logs to `communication_log` | backend |
| `aiorders-api`: `supabase/functions/broadcast-dispatch/dispatch.test.ts` | new — claim idempotency under a simulated overlapping tick, opted-out-between-enrollment-and-send exclusion, partial-batch-failure isolation | backend |
| `aiorders-api`: `supabase/functions/broadcast-unsubscribe/index.ts` | new — public, unauthenticated, GET-only. Token → flips `consent_email.consent`/`consent_sms.consent` to `false` on the matching customer row. See `ADR-020` | backend |
| `aiorders-api`: `supabase/functions/README.md` | modify — `brand-portal` DB-tables list gains `broadcast_campaigns`/`broadcast_campaign_steps`/`broadcast_campaign_recipients`; two new function sections (`broadcast-dispatch`, `broadcast-unsubscribe`) in the house format | backend |
| `restaurant-portal`: `src/pages/autopilot/Automations.tsx` | modify — third `TabsTrigger`/`TabsContent` ("Broadcasts"), rendering the new page component. No change to the existing "flows"/"history" tabs | frontend |
| `restaurant-portal`: `src/pages/autopilot/Broadcasts.tsx` | new — campaign list + create/edit composer (audience picker, one-time vs. drip step editor, coupon attach) + per-campaign report view. Split into sub-components if any piece nears the ~400-line standard | frontend |
| `restaurant-portal`: `src/components/autopilot/BroadcastComposer.tsx` | new — the compose form, isolated from the list/report so the list stays cheap to render | frontend |
| `restaurant-portal`: `src/components/autopilot/BroadcastReport.tsx` | new — per-campaign stats: sent/pending/failed by channel, redemptions/revenue when a coupon is attached | frontend |
| `restaurant-portal`: `src/services/brandPortalApi.ts` | modify — new methods matching the `broadcasts.ts` actions, same idiom as the existing `getOffers`/`createOffer` methods | frontend |
| `restaurant-portal`: `src/types/broadcasts.ts` | new — `BroadcastCampaign`, `BroadcastStep`, `BroadcastAudience`, `BroadcastReport` types | frontend |
| `restaurant-portal`: `src/hooks/use-broadcasts.ts` | new — `useBroadcasts`, `useBroadcast`, `useBroadcastReport`, matching `use-autopilot.ts`'s existing hook shape | frontend |
| `restaurant-portal`: `src/pages/autopilot/Templates.tsx`, `src/types/autopilot.ts`, every reactive `Automations` flow | **no change** — PRD non-goal, and this design's own additive framing. Nothing here is extended or reused as a trigger type | — |

**Not a scope addition, a failure-mode answer.** `pause_broadcast`/
`cancel_broadcast` are not named in any acceptance criterion. They're
included because step 5's "design the failure before the feature" applies
directly to a mass-send feature: an owner who spots a typo mid-blast needs a
stop button, and the poller architecture (`ADR-018`) makes pause a one-column
status flip its own `WHERE` clause already respects — effectively free.
Named here explicitly rather than folded in silently.

## Data

`touches_data: true`. `database` owns the migration; this section states
intent and constraints only.

**Three new tables, no changes to any existing table.**

**`broadcast_campaigns`** — one row per composed campaign. Needs:
restaurant_id, type (`one_time`|`drip`), status (`draft`|`scheduled`|
`active`|`paused`|`completed`|`cancelled`), audience mode (`all`|
`inactive_days`) and its parameter, an optional reference to `offers.id`
(the attached coupon), `scheduled_send_at` (a past/now timestamp for
"immediate", matching the unified-dispatch reasoning below), created_by,
timestamps.

**`broadcast_campaign_steps`** — one row per drip step (a one-time campaign
gets exactly one implicit step). Needs: campaign_id, step order, delay from
enrollment, subject/email body/SMS body — same shape as
`communication_templates`' own email/SMS content fields, for consistency
with the pattern engineers already know.

**`broadcast_campaign_recipients`** — one row per (campaign, step, customer)
— the dispatcher's claim queue and the report's source of truth. Needs:
campaign_id, step_id, customer_id, restaurant_id, `due_at`, status
(`pending`|`sent`|`failed`|`skipped_opted_out`|`cancelled`), sent_at,
error detail. `restaurant_id` is denormalized onto this table deliberately
— the dispatcher's own claim query must never join out to `customers` or
`broadcast_campaigns` just to know which restaurant a row belongs to.

Constraints the migration must satisfy:

- **Immediate and scheduled sends are the same row shape.** "Send now" sets
  `scheduled_send_at = now()`; there is no separate immediate-send code
  path. One dispatch mechanism, one failure mode to reason about, per
  `ADR-018`.
- **The claim query must be safe under an overlapping tick.** If one tick is
  still processing its batch when the next fires (a slow send, a cold
  start), two ticks must never dispatch the same recipient row twice. The
  migration provides (or the dispatcher uses) an atomic claim — `SELECT ...
  FOR UPDATE SKIP LOCKED` or an equivalent claiming `UPDATE ... WHERE
  status = 'pending' RETURNING *` — not a plain `SELECT` followed by a
  separate `UPDATE`. This is the idempotency key the standards' "never retry
  a non-idempotent write" rule asks for.
- **Index on `(status, due_at)`** on `broadcast_campaign_recipients` — the
  dispatcher's every-5-minutes claim query is the hottest read this feature
  adds.
- **Index on `(campaign_id)`** on the same table — the report view's per-
  campaign aggregation.
- **`orders(restaurant_id, created_at)`** — presumed present (`ENG-020`'s
  design already made this same presumption for the same table); `database`
  confirms against the live schema before this ticket's ROI query ships, and
  raises a separate ticket rather than adding an index inside this one if
  it's missing.
- **The schema cannot be verified from this repo for the tables being read,
  not written.** Neither `customers`, `offers`, `orders`, nor
  `communication_log` is created by any tracked migration — the same gap
  `ADR-006` and `ENG-020`'s design already recorded. `database` confirms
  `orders.promos`' exact internal key (for `ADR-019`'s matching query) and
  `communication_log`'s exact column set against the live project before
  writing the functions that depend on them, the same way `ENG-020`'s design
  already required for its own reads.
- **No new column on `customers`.** Opt-out is `consent_email`/
  `consent_sms`, already there — `ADR-020`.
- **`communication_log` is unchanged.** Every campaign send writes a row
  there exactly the way `sendWelcomeOffer` already does, with
  `reference_type: 'broadcast_campaign'`, `reference_id: campaign.id` — a
  new value in an existing polymorphic column, not a new column. This is
  where AC5 comes from at zero schema cost, and — since Brevo's existing
  webhook (`external-integrations/handlers/brevo.ts`) already updates
  `opened_at`/`clicked_at` on that same table keyed by
  `provider_message_id` — the campaign report gets email open/click figures
  for free, with no new webhook and no new column.

## Interfaces

### `brand-portal` actions (`broadcasts.ts`)

All require the existing Bearer JWT + `requireRestaurantAccess(restaurant_id,
...)` gate every sibling action in this router already uses (`ADR-011`'s own
precedent, reconfirmed against `offers.ts`/`catering.ts` directly). Response
shape mirrors `offers.ts`'s convention: `{success, error}` on failure, never
a thrown 500 for an expected condition.

- **`list_broadcasts`** `{restaurant_id, page?, page_size?}` → paginated
  campaign summaries (id, name, type, status, audience summary, recipient
  count). Pagination is not optional — engineering-standards' automatic
  review failure #5.
- **`get_broadcast`** `{restaurant_id, id}` → full campaign + step list.
- **`create_broadcast`** `{restaurant_id, name, type, audience: {mode,
  inactive_days?}, offer_id?, steps: [{delay_hours, email_subject?,
  email_body?, sms_body?}], send_at?}` → `status: 'scheduled'`
  (`send_at` omitted/past = due immediately, per the unified-dispatch
  decision above). Validates: at least one step, at least one channel
  populated per step, `offer_id` (if given) belongs to this restaurant,
  `inactive_days` is a positive integer when `mode: 'inactive_days'`.
- **`update_broadcast`** `{restaurant_id, id, ...same fields}` — **rejected
  once `status` is `active` or past.** Editing content mid-flight would mean
  some recipients already received the old content and some would get the
  new — an inconsistency worse than making the owner cancel and recompose.
  `{success: false, error: 'Cannot edit a campaign that has started sending'}`.
- **`pause_broadcast`** / **`resume_broadcast`** `{restaurant_id, id}` —
  flips `status` between `active`/`paused`; the dispatcher's claim query
  filters on campaign status, so a paused campaign's due rows simply wait.
- **`cancel_broadcast`** `{restaurant_id, id}` — terminal; marks every
  remaining `pending` recipient row `cancelled`, campaign `cancelled`.
  Already-sent rows are untouched — cancellation stops what hasn't gone out,
  it doesn't rewrite history.
- **`get_broadcast_report`** `{restaurant_id, id}` → counts by status and
  channel from `broadcast_campaign_recipients`; when `offer_id` is set,
  redemption count and revenue per `ADR-019`'s query; email open/click
  counts from `communication_log` (Data section, above) when any exist.

### `broadcast-dispatch` (system-triggered, no user-facing contract)

`net.http_post`, `Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}`, no
request body needed — the function reads what's due from the database itself.
Not reachable with any other credential; matches `ADR-016`/`ADR-017`'s gate
shape (a local `auth.ts` in this function's own directory, not a `_shared/`
import — `ADR-017`'s own "third consumer" line is the trigger for
extracting that check to `_shared/`, and this design doesn't cross it since
this ticket is only the second).

Per tick: (1) `UPDATE broadcast_campaigns SET status = 'active' WHERE status
= 'scheduled' AND scheduled_send_at <= now() RETURNING *`, then for each,
resolve the audience (`customers` scoped to `restaurant_id`, filtered by
audience mode, filtered by the relevant channel's `consent.consent IS NOT
FALSE`) and bulk-insert one `broadcast_campaign_recipients` row per
(customer, step) with `due_at = campaign's send moment + step's delay`; (2)
claim up to 200 rows where `status = 'pending' AND due_at <= now()`, joined
to a campaign that is still `active` (not paused/cancelled since being
claimed-eligible), **re-checking the customer's current consent** (not the
snapshot from enrollment — a customer may have unsubscribed between steps),
and for each: call `outgoing-communications` (`actor: 'consumer'`, a new
`broadcast_message` action, `systemTriggered: true`, service-role bearer —
the same call shape `autopilot/marketing/utils.ts#sendViaOutgoingComms`
already makes, duplicated locally rather than imported cross-directory per
`ADR-015`'s own precedent for this exact situation), then write the
recipient row's resulting status. One recipient's failure never aborts the
batch — isolated per-item try/catch, matching `sendCampaignCreatedNotification`'s
existing `Promise.all` pattern in `outgoing-communications/actors/brands.ts`.

### `outgoing-communications` — one new consumer action

`actors/consumers.ts` gains `broadcast_message`, alongside the existing
`welcome_offer`/`every_order`/`first_order` cases: sends the step's
pre-composed subject/body (owner-authored, no template-variable system
needed beyond `replaceTemplateVariables`'s existing `{{customer_name}}` —
reused, not rebuilt), appends the unsubscribe link/line, and writes
`communication_log` with `reference_type: 'broadcast_campaign'`.

### `broadcast-unsubscribe`

`GET /broadcast-unsubscribe?token=<opaque>&channel=email|sms`, public, CORS
`GET, OPTIONS` only, no `Authorization` required — matches the `offers/
index.ts` public-GET precedent. Token resolves to one customer row (opaque,
non-enumerable — HMAC-signed customer_id, not a raw id); flips the matching
consent field to `false`; returns a plain confirmation page, not JSON — the
visitor is a customer's browser, not this platform's own frontend.

| Condition | Response |
|---|---|
| Token missing/invalid/expired | 400, plain-text "This link is no longer valid." |
| Token valid, already unsubscribed | 200, same confirmation copy — idempotent, not an error |
| Token valid | 200, flips consent, confirmation page |

## Alternatives considered

| Option | Why it lost |
|---|---|
| Per-recipient QStash scheduling | `ADR-018` — proven at single-event scale, not mass-fanout scale; pause/cancel means deleting messages individually. |
| A dedicated redemption-tracking table for AC4 | `ADR-019` — no write path into checkout exists for this codebase to use; the read against `orders.promos` already answers AC4 with data already captured. |
| A new `broadcast_opt_out` column | `ADR-020` — `consent_email`/`consent_sms` already exist and already mean this. |
| Bolt broadcasts onto `autopilot`'s existing `TriggerType`/marketing-action model | Rejected by the PRD itself ("a new, parallel mechanism, not a new trigger type") and reinforced by reading `autopilot/index.ts`: its `systemTriggered` bypass is reactive-trigger-only and is mid-fix for a real, unrelated auth gap (`ADR-016`/`ENG-035`) this ticket has no reason to touch or depend on. |
| Add the composer inline as new tab content inside `Automations.tsx` itself | The file is already 400+ lines covering two tabs; a third tab with a full composer/report would blow past the standards' size-smell threshold. A separate `Broadcasts.tsx`, same relationship `Templates.tsx` already has to `Automations.tsx`. |
| Mint a brand-new CloudWaitress discount promo from the composer (via `cloudwaitress-middleware`'s `handleCreateDiscount`) instead of referencing an existing offer | Every existing offer/coupon-code creation path in this codebase already goes through `brand-portal/offers.ts`, not through that proxy directly. Reusing an *existing* offer is smaller, doesn't duplicate offer-creation UI, and matches the PRD's own framing ("attach a coupon code to a campaign," not "create one"). |

## One-way doors

**None.** Each candidate was checked:

- No new vendor, no new datastore — `pg_cron`, `outgoing-communications`,
  `customers`, `orders`, `communication_log` all already exist and are
  reused unmodified at the primitive level.
- No auth-model change — `requireRestaurantAccess` and the service-role-
  bearer `systemTriggered` gate are both applied exactly as this project's
  existing, just-established conventions (`ADR-011`, `ADR-016`/`ADR-017`)
  already use them.
- No public contract change — every new action is additive; nothing existing
  is modified in a way another caller depends on.
- No data model painful to migrate — three new tables, zero rows to
  transform.
- No new recurring cost decision — see Risks for the one cost-adjacent note
  this design does surface.

`ADR-018`, `ADR-019`, and `ADR-020` are the three real decisions here, all
reversible, all decided and logged rather than escalated.

## Risks

**"Immediate" is bounded by the poll interval, not instant.** Default 5
minutes. Named plainly rather than implied — a marketing broadcast does not
need sub-minute delivery, and the interval is a runtime constant, raisable
without a schema change if it proves too slow in practice.

**A very large one-time send can take longer than one tick to fully clear.**
Total dispatch time is roughly `recipients ÷ batch_size × tick_interval`.
Acceptable for a marketing send; named so it's a known trade-off, not a
surprise, and the two knobs (batch size, interval) are cheap to raise.

**`orders.promos`' internal shape is unconfirmed from this repo.** `ADR-019`
— `database` verifies against a live sample before the ROI query ships; it
fails loud (logged, zero-state) rather than silently matching nothing on a
wrong key guess.

**Campaign revenue can't exclude a later-cancelled order.** `ADR-019` — this
platform has no order-status-update path yet (`ENG-027`'s own finding); same
limitation every other revenue figure on this platform, including `ENG-020`'s
acquisition report, already carries.

**Idempotent claiming is load-bearing, not incidental.** If the dispatcher's
claim step is a plain `SELECT` instead of an atomic claim, an overlapping
tick double-sends. This is the one piece of this design where "the smallest
thing" and "correct" are the same requirement, not a trade-off — flagged so
it isn't quietly simplified away at build time.

**Cross-tenant scoping — the class of bug this codebase has a confirmed
history of (`ENG-015`, `ENG-022`).** Every `brand-portal` action checks
`requireRestaurantAccess` *and* every query is filtered by `restaurant_id` —
defense in depth, matching `ADR-006`'s established pattern, not RLS alone.
The dispatcher path carries no caller-supplied `restaurant_id` at all — each
recipient row already carries its own — so there's no cross-tenant vector
inside that path to guard against.

**Mid-flight edits are blocked, not merged.** `update_broadcast` refuses once
a campaign is `active` or later (Interfaces). An owner who needs to change a
live campaign cancels and recomposes. Small, named UX limit, not a bug.

**Empty audience is a clean no-op, not a silent failure.** An
`inactive_days` filter matching nobody produces a `completed` campaign with
`0` recipients and says so in the report — never an error, never a send that
silently does nothing without telling the owner why.

**`ENG-019` and `ENG-020` are two independent revenue-attribution surfaces
shipping the same evening on the same portal.** Already flagged by this same
architect on `ENG-020`'s own design pass (`observations.md`, 2026-09-03): if
their definitions of "revenue" (period, cancelled-order handling, guest
orders) ever diverge, an owner will see two numbers that don't reconcile.
Not a blocker for either individually; restated here so whoever next touches
either has both pointers.

**Brevo/SMS-provider send volume grows with broadcast usage.** No new vendor
decision — existing infrastructure, existing per-message cost model, now
exercised at a higher volume than any single reactive trigger produces alone.
Visible in that vendor's own usage dashboard; worth a devops glance once
broadcasts are in real use, not a design-time blocker (PRD's own Cost
section already frames this as a "flag if surfaced," not a gate).

**Aside, not this ticket's to fix:** `supabase/functions/README.md`'s
"Known issues" section still describes `brand-portal/offers.ts`/`feedback.ts`
calling `verifyRestaurantAccess` with the wrong argument order. Reading
`offers.ts` directly (this design's own Interfaces work) shows correct
argument order today — `ENG-022` (merged this evening, commit `78194da8`)
appears to have fixed this without updating the README note. Filed as an
observation, not touched here.

## Rollout

Additive-only — no existing table, function, or frontend route changes
behavior for any user who never opens the new tab. Safe order: migration
(new tables, cron job created but the tables it polls start empty) →
`broadcast-dispatch`/`broadcast-unsubscribe`/`brand-portal` functions →
frontend. Rollback: `cron.unschedule('broadcast-dispatch-tick')` stops all
future dispatch immediately (any send already claimed by an in-flight tick
still completes); revert the PR(s). No backfill, no data migration, nothing
to undo on the down path — the new tables simply go unused if reverted.

## Out of scope

Everything the PRD's own Non-goals already name (deeper ROI/attribution
beyond coupon-code redemption, a segment builder beyond all/inactive-N-days,
AI-generated content, reseller access, a new outbound channel, any change to
reactive `Automations`), plus what this design itself declines to build:

- **Exact-second scheduling precision** — bounded by the poll interval
  (Risks).
- **Mid-flight campaign editing** — cancel and recompose instead (Interfaces).
- **SMS opt-out via inbound "STOP" reply parsing** — link-based for both
  channels instead (`ADR-020`); this codebase's SMS layer has no inbound
  path to parse replies on at all.
- **Extracting `broadcast-dispatch`'s `outgoing-communications` call into
  `_shared/`** — `ADR-017`'s own "third consumer" bar isn't crossed by this
  ticket (autopilot is the first, this is the second).
