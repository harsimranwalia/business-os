---
id: ADR-021
title: "Loyalty auto-complete uses a pg_cron batch poller, not a per-order Cloudflare Queue delay"
project: aiorders-api
ticket: ENG-027
status: accepted
decided_by: architect
date: 2026-09-05
supersedes:
superseded_by:
---

# ADR-021: Loyalty auto-complete uses a pg_cron batch poller, not a per-order Cloudflare Queue delay

## Context

`ENG-027`'s approved design needs a durable 24-hour timer: an online order
that gets neither a completion nor a cancellation report within 24 hours of
placement is treated as fulfilled and credited. Two durable-delay mechanisms
already exist live in this exact codebase, the same choice `ADR-018` faced
for `broadcast-dispatch`: `platform_analytics_cron`'s `pg_cron` +
`net.http_post` (a recurring tick, `ADR-018`'s own chosen shape for that
ticket), and `sendFeedbackQueueMessage`'s per-order Cloudflare Queue
`delay_seconds` (`cloudflare-queue.ts:73`, called from the exact same
`order_new` webhook handler this ticket modifies, at a 3-hour default).

The per-order queue delay is the more obvious fit at first glance — it is
already wired to the same webhook, already fires once per order, and this
ticket's own timer is conceptually "the same idea, longer." Two things rule
it out on inspection. First, this repo has nothing establishing Cloudflare
Queues' own maximum `delay_seconds` — the existing usage is 3 hours, a
fraction of the 24 hours this ticket needs, and asserting the platform
supports a 24-hour single-message delay would be a guess this design isn't
willing to make without a source. Second, and more load-bearing: the PRD's
own acceptance criterion 15 ("given the auto-complete sweep fails while
processing one order, when it continues, then the remaining eligible orders
are still processed, and a subsequent run retries the failed one") describes
a batch that keeps going when one item in it fails — a claim-a-batch shape,
not a fleet of independent per-order callbacks with no relationship to each
other's failure.

## Decision

A new `cron.schedule('loyalty-auto-complete-tick', '*/15 * * * *', ...)`
job, structurally identical to `ADR-018`'s `broadcast-dispatch-tick`,
invokes a new `loyalty-auto-complete` edge function via `net.http_post`
every 15 minutes. Each tick selects a bounded batch of orders eligible for
auto-completion (`cw_order_id IS NOT NULL AND loyalty_processed_at IS NULL
AND status IS DISTINCT FROM 'cancelled' AND created_at <= now() - interval
'24 hours'`) and calls the same `credit_order_if_eligible()` function the
webhook path uses, once per order, catching each row's own failure without
aborting the rest of the batch.

Same internal-call convention `ADR-016`–`018` already established:
`Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}` on the `net.http_post`
call, not `platform_analytics_cron`'s older headerless precedent.

## Alternatives

| Option | Why not |
|---|---|
| Per-order Cloudflare Queue delay (`sendFeedbackQueueMessage`'s own mechanism, scheduled at 24 hours instead of 3) | This repo has no source for Cloudflare Queues' own maximum `delay_seconds`; the only proven value here is 3 hours. Even if a longer delay is supported, one message per order gives each order an independent failure domain, which doesn't match AC15's own "batch keeps going, failed item retries next run" language. |
| One edge-function invocation, triggered per-order at placement time with an in-process `setTimeout`-style wait | Not viable in an edge-function execution model at all — nothing stays alive for 24 hours inside one invocation. |
| Poll CloudWaitress's own order-status API on a schedule instead of relying on pushed webhooks + a fallback timer | Rejected in the PRD itself (Non-goals) — the on-demand proxy exists and is worth knowing about, but this ticket consumes pushed events and a local timer, not a poll loop against a third party. |

## Consequences

**Accepted:** auto-completion timing is bounded by the 15-minute tick, not
exact-to-the-second — irrelevant here, since nothing reads a balance yet
(no frontend, PRD non-goal) and a quarter-hour of slop on a 24-hour window
is invisible. Batch size and tick interval are runtime constants; `database`
sizes them against real numbers when the migration is written
(`skills/schema-change/SKILL.md` step 2), not guessed in this design.

**Gained:** zero new vendor, zero new billed infrastructure — `pg_cron` is
already enabled on this project. The credit logic lives in one DB function
called from two triggers (webhook, sweep) instead of being duplicated
per-mechanism.

**Reversibility: cheap**, same as `ADR-018`'s own framing — swapping the
sweep's internals for a queue-based mechanism later, if a real Cloudflare
Queues delay ceiling is ever confirmed to comfortably cover 24 hours,
changes nothing about `loyalty_ledger_entries`'s shape or the
`credit_order_if_eligible()` contract either trigger calls.

## Review trigger

If a real production need arises for sub-15-minute auto-complete precision,
lower the tick interval first (a runtime constant) before reaching for a
different mechanism.
