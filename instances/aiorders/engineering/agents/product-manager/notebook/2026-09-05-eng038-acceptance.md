# Acceptance — ENG-038 (broadcast composer API, dispatch poller, unsubscribe function)

## Why this ran in full, not as receipt bookkeeping

Unlike `ENG-037` (0 of the parent's 7 criteria apply to a schema-only diff —
`ENG-031`'s own precedent), `2026-09-04-eng019-work-breakdown.md`'s own
Acceptance-criteria-coverage table maps **all seven** of `ENG-019`'s ACs to
this ticket specifically: "every criterion is backend-enforced... mapped
here so a later gate doesn't have to re-derive it." That instruction is to
this pass. `acceptance-check/SKILL.md`'s trigger ("a ticket enters state
`shipped`") has no sub-ticket carve-out either way — same reasoning
`ENG-034`'s and `ENG-016`'s own notebooks already applied today.

## Scope

All 7 acceptance criteria in the PRD
(`agents/product-manager/specs/ENG-019-restaurant-marketing-broadcasts.md`),
backend half only. `ENG-039` (frontend, not yet built) owns surfacing AC1-5
in the UI; AC6/AC7 have nothing left for it to add per the same work-breakdown
mapping.

## Check against the live result — not the proxies

**Checked twice, because the answer changed mid-pass.** Release-readiness
(the pass before this one) found `broadcast-dispatch`/`broadcast-unsubscribe`
undeployed (`supabase functions list`) — the same "no auto-deploy workflow on
this repo" state every prior `aiorders-api` release on this board recorded.
Re-checked fresh anyway rather than trusted, per this project's own
established substitute (`ENG-007` onward): **all four touched functions are
now deployed** — `brand-portal` (v81), `broadcast-dispatch` (v1),
`broadcast-unsubscribe` (v1), `outgoing-communications` (v70), version
timestamps `2026-09-05T07:25:20Z`–`07:25:55Z`, roughly 3-8 minutes after PR
#16's own `mergedAt` (`07:22:20Z`). No workflow did this — it reads as the
approver deploying by hand immediately after merging, the same
GitHub-PR-list-driven pattern `decision-journal.md` already has eight data
points for, extended one step further than usual.

**This means the source of truth for this check is genuinely live, not just
merged** — read via `git show origin/main:{path}` (merge commit `89c6fdb1`)
since that's confirmed identical to what's deployed (same commit, no drift
window), then traced line-by-line myself. **What this check does not do:**
create a real campaign or exercise a real send against
`bmnmnejwdxbcqinqkwko` — that would dispatch actual email/SMS to real
customers on a live restaurant's list, which is exactly the kind of
irreversible production action this check has no business taking to prove a
point. Verification below is direct code inspection of the live-confirmed
source, plus read-only schema/config queries (row counts, constraint/index
existence, secret *names* never values, cron run status) — the same
boundary every live-project check on this board has already held.

## Walk every criterion

| AC | Criterion | Checked against | Result |
|---|---|---|---|
| 1 | Send immediately or schedule for a future date/time | `broadcasts.ts` `createBroadcast` (L309-311): `send_at` omitted/past → `scheduledSendAt = now` ("one dispatch mechanism, no separate immediate-send path"); a future `send_at` stores as-is. `dispatch.ts` `promoteDueCampaigns` (L50-57): promotes only `status='scheduled' AND scheduled_send_at <= now` | **Pass** |
| 2 | Drip: each step sends at its own delay, once per customer | `dispatch.ts` `enrollAudience` (L124-137): one `broadcast_campaign_recipients` row per `(customer × step)`, `due_at = enrolledAt + step.delay_hours`; `selectDueRecipientCandidates`/`claimRecipients` (L146-191) select and atomically claim by `due_at`/`status='pending'` — a customer gets exactly one row per step, never re-enrolled by a later tick (enrollment happens once, at promotion) | **Pass** |
| 3 | Audience "all" vs. "inactive for N days," scoped strictly to the owner's own restaurant | `enrollAudience` (L72-85): `customers` query always carries `.eq('restaurant_id', campaign.restaurant_id)`; `inactive_days` mode adds `last_order_at.lt.{cutoff} OR is.null`. `audienceExceedsCap`/`createBroadcast`/`updateBroadcast` apply the identical restaurant-scoped query at creation time for the size cap | **Pass** |
| 4 | Campaign report shows redemption count and revenue for its attached coupon | `broadcasts.ts` `getBroadcastReport`/`computeRedemptions` (L586-619, 656-702): scoped to `campaign.offer_id`'s own `coupon_code`, matches `orders.promos[].code` for orders since `scheduled_send_at`, returns `{redemptions, revenue}` — `null` (not `0`) when no coupon attached, so "not tracked" is distinguishable from "tracked, zero so far." API-level only — rendering this on "the campaign's own page" is `ENG-039`'s scope, not built here | **Pass (backend half)** |
| 5 | Every send logged the same way existing automation logs (channel, recipient, status, timestamp), visible in that campaign's history | `consumers.ts` `buildBroadcastEmailLogRow`/`buildBroadcastSmsLogRow` (L897-946) write to `communication_log` with the identical column set `sendFirstOrderOffer`'s own pre-existing insert already uses (L360-397 of the same file: `restaurant_id`, `customer_id`, `trigger_type`, `channel`, `recipient_email`/`recipient_phone`, `subject`/`body`, `status`, `error_message`, `reference_id`, `reference_type`, `sent_at`, `provider_message_id`) — only `trigger_type`/`reference_type` values differ (`broadcast_message`/`broadcast_campaign`). `getBroadcastReport` (L620-654) reads the same table back, scoped by `reference_type`/`reference_id`, for history/delivery-by-channel | **Pass** — compared directly against the pre-existing insert, not assumed similar |
| 6 | Unsubscribe/opt-out path works; opted-out customer excluded from every future send regardless of audience | `_shared/broadcastUnsubscribe.ts`: real HMAC-SHA256 sign/verify pair (`crypto.subtle`, constant-time verify), `buildUnsubscribeUrl` embeds a live token in every sent message (`consumers.ts` L1045, L1076); `broadcast-unsubscribe/index.ts` verifies the token and flips `customers.consent_email`/`consent_sms` (per-channel) to `{consent: false, ...}`, idempotently. Exclusion enforced twice: `enrollAudience`'s `contactable` filter (L98-100, both channels false → never enrolled) and `sendBroadcastMessage`'s own `decideBroadcastChannelEligibility` re-check at send time (so a mid-drip unsubscribe still stops the next step) | **Pass, code-level** — functional round-trip traced, not just present. **Confirmed live, not just theoretical: `BROADCAST_UNSUBSCRIBE_SECRET` is not in `supabase secrets list` right now** (checked this pass, name only, no value read) — `hmacKey()` will throw the instant this path is actually exercised. Same non-blocking shape as `ENG-037`'s own named Vault-secret prerequisite: dormant today (zero campaigns exist, and `ENG-039` — the only way to create one — hasn't shipped), self-diagnosable, already tracked in three notebooks (backend build, review, QA). Named again here with fresher evidence because the functions turned out to already be deployed (below) — this is armed, not hypothetical |
| 7 | Cross-tenant read/send of campaign data rejected server-side | Every `broadcasts.ts` action (`list`/`get`/`create`/`update`/`pause`/`resume`/`cancel`/`report`, L191/248/295/380/485/518/607) calls `requireRestaurantAccess(restaurant_id, supabase, user)` before touching data, throwing on denial — a pre-existing, reused guard, not new logic this ticket introduces. The system-triggered dispatch path carries no caller-supplied `restaurant_id` at all (security round 2's own re-verification, cross-checked directly against `dispatch.ts`/`consumers.ts` this pass, not cited from the review alone) | **Pass** |

## Live infrastructure, checked read-only

Beyond reading source, queried the linked project directly (`supabase db
query`, read-only; row/name data only, never values, per the CLI's own
untrusted-data envelope):

- **Migration is live**: `broadcast_campaign_recipients_status_check` includes
  `'claimed'`; `broadcast_campaign_recipients_step_id_idx` and the
  `campaign_id`/`status_due_at` indexes all present.
- **`service_role_key` exists in Vault** (name only) — `ENG-037`'s own
  dispatch-auth prerequisite is actually met, not just assumed.
- **`broadcast-dispatch-tick`'s last 30 minutes of HTTP calls**
  (`net._http_response`, project-wide table, not scoped to this job alone):
  9× `200`, 1× `401`, 3× `null` (in-flight/unscoped). Reads as healthy for the
  current no-op case (0 campaigns, tick returns fast) — not chased further;
  auditing pg_net traffic in general is devops's ongoing job, not this
  ticket's acceptance criteria.

## Check the non-goals

Diff scanned against `ENG-019`'s non-goals list (deeper ROI/attribution
beyond redemption+revenue; a segment builder beyond all/inactive-N-days;
AI-generated content; reseller access) — none present.

**Worth naming rather than passing over silently:** `getBroadcastReport`'s
`buildDeliveryByChannel` (L568-584) counts `opened`/`clicked` from
`communication_log.opened_at`/`clicked_at`. Those columns are real and
populated elsewhere (`external-integrations/handlers/brevo.ts`,
`url-shortener/index.ts`, both pre-existing) — but this ticket adds no new
instrumentation to produce them for broadcast sends specifically; it reads
whatever the same shared `sendEmail`/`sendSMS` services
(`services/email.ts`/`services/sms.ts`, confirmed by import, not
broadcast-specific copies) already populate for every message type. Not the
"deeper ROI/attribution" the PRD excludes — nothing was built to originate
open/click tracking for this feature — but flagging it since the column
names are adjacent to the excluded scope.

## Check the cost

PRD: `$0/month` expected ("reuses the already-contracted email/SMS
delivery... flag only if a real new per-message or per-job cost surfaces").
No new vendor, no new dependency in the diff (`npm:@supabase/supabase-js@2`
already used everywhere else); already confirmed at release-readiness.
Matches.

## Route

**All 7 criteria this ticket owns: pass**, verified directly against the
exact merged source (`origin/main` at `89c6fdb1`), not against the test
suite, the PR description, or any gate's own summary. State → `verified`,
owner → `eng-manager`.

## Step 6b — continue an approved sequence?

Does not apply at this sub-ticket's level, same reasoning `ENG-034`'s own
notebook recorded: the PRD's sequencing lives with the parent (`ENG-019`),
not with a work-breakdown child. `ENG-039` is the family's last piece, not a
new sequence item — nothing to raise here.

## What the estimate got right

`time_estimate: ~2-3 days` undercounted actual elapsed time (six review
rounds plus two security rounds before reaching `ready-to-ship`), but the
ticket's own log already carries that history in detail — nothing new this
entry adds there. The work-breakdown's own AC-ownership pre-mapping (all 7
to this ticket) held exactly as written; no criterion needed reassignment.

## What it missed

Nothing at the criteria level. One real surprise: this check assumed, going
in, that "not deployed yet" (true at release-readiness, a pass earlier the
same night) would still be true now. It wasn't — re-checking rather than
trusting the prior gate's own snapshot is what caught it. Worth naming
plainly: a receipt written earlier in the same pipeline can go stale by the
time the acceptance-check runs, even within one evening, once a human is
merging *and* deploying by hand outside any tracked workflow. Filed as an
observation (`observations.md`) rather than a proposal — one instance isn't
a pattern, and nothing broke; the deploy landed correctly and the one
config gap it exposed was already tracked, just not yet confirmed as
still-missing at the moment it started to matter.

## Also worth recording

**Unblocks `ENG-039`** (`depends_on: [ENG-038]`) — the family's last
sub-ticket, frontend only, `restaurant-portal`. `continue ENG-039` fired
this same pass rather than building it inline. `ENG-019` (parent) still
cannot reach `shipped` until `ENG-039` is settled too (`ADR-003`).
