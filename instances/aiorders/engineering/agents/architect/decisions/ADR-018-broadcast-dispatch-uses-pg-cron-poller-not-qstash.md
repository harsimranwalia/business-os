---
id: ADR-018
title: "Broadcast scheduling and mass dispatch use a pg_cron poller claiming due rows, not per-recipient QStash messages"
project: aiorders-api
ticket: ENG-019
status: accepted
decided_by: architect
date: 2026-09-03
supersedes:
superseded_by:
---

# ADR-018: Broadcast scheduling and mass dispatch use a pg_cron poller claiming due rows, not per-recipient QStash messages

## Context

`ENG-019`'s PRD names its own Risk as "left to the architect": durable
scheduling/drip delivery needs a real job, not an in-process timer, and notes
`platform_analytics_cron` as existing precedent for the primitive without
committing to it. Reading `origin/main` directly finds **two** proven durable-
delay mechanisms already live in this codebase, not one:
`20260217000001_platform_analytics_cron.sql`'s `pg_cron` + `net.http_post`
(one recurring tick, aggregate work, no per-item scheduling), and
`autopilot/marketing/utils.ts`'s `scheduleWithQStash` (one Upstash QStash
message per delayed send, `Upstash-Delay` up to 7+ days, calling
`outgoing-communications` directly on expiry — proven by every `welcome_offer`/
`every_order`/`first_order` send today).

The two differ exactly where this ticket's audience-fan-out risk lives. QStash
is proven at *one message per event* — a single customer crossing a lifecycle
trigger, naturally spread over time by when each trigger fires. This ticket
introduces a materially different shape: one owner action can enroll an entire
restaurant's customer list at once, for a one-time send or a multi-step drip.
Scheduling that via QStash means one publish call per recipient per step at
compose/enrollment time — thousands of HTTP calls to set up a single campaign,
before any message has actually gone out, and pausing a campaign mid-flight
means deleting each already-published message individually.

## Decision

A new `cron.schedule('broadcast-dispatch-tick', '*/5 * * * *', ...)` job,
structurally identical to `platform-analytics-hourly`, invokes a new
`broadcast-dispatch` edge function every 5 minutes via `net.http_post`. Each
tick does two things: (1) promotes any `broadcast_campaigns` row past its
`scheduled_send_at` from `scheduled` to `active`, resolving and bulk-inserting
its recipient audience **at that moment**, not at compose time; (2) claims a
bounded batch (default 200) of `broadcast_campaign_recipients` rows where
`due_at <= now() AND status = 'pending'`, atomically, and dispatches each
through the same `outgoing-communications` call path every other
system-triggered sender already uses.

Unlike `platform_analytics_cron`'s own `net.http_post` (no `Authorization`
header at all), this job's call sets `Authorization: Bearer
${SUPABASE_SERVICE_ROLE_KEY}` — a deliberate break from that precedent, made
because `ADR-016`/`ADR-017` (this same evening) just established service-role
bearer as this project's one system-trust convention for exactly this kind of
internal call. Copying the older, headerless precedent here would immediately
create the second inconsistent case those two ADRs were written to prevent.

## Alternatives

| Option | Why not |
|---|---|
| Per-recipient QStash scheduling (`autopilot`'s own precedent) | Proven at one-message-per-event scale, not at one-campaign-creates-thousands-of-messages scale. Pausing/cancelling means deleting each published message individually (bookkeeping this design doesn't otherwise need); a large campaign means thousands of publish calls just to set up, itself slow inside one request. |
| One edge-function invocation loops the whole audience synchronously at send time | Not literally the unbounded query automatic-review-failure #5 targets, but the same instinct applies: restaurant customer-list size is bounded in practice, not bounded enough to guarantee completion inside one HTTP request's execution limit. |
| A Cloudflare Queue consumer (already used elsewhere, e.g. `aiorders-admin-hub`'s `queue-consumer`) | A second infra dependency for one project when Postgres — already this project's system of record — already has a proven, zero-marginal-cost scheduling primitive live in this exact database. |

## Consequences

**Accepted:** dispatch timing is bounded by the 5-minute tick, not exact-second
— fine for a marketing send, named plainly in the design's Risks rather than
implied to be instant. A very large one-time send can take longer than one
tick to fully clear (recipients / batch-size × interval); tunable, not a
blocker.

**Gained:** zero new vendor and zero new billed infrastructure — `pg_cron` is
already enabled in this project. Pause/cancel is a one-column status flip the
poller's own `WHERE` clause already respects, not a per-message delete.
Batch size and tick interval are runtime constants, changeable without a
schema change.

**Reversibility:** cheap. Swapping the dispatcher's internals for QStash later
— if a campaign volume profile ever needs sub-minute precision — changes
nothing about `broadcast_campaign_recipients`'s own shape or the
`outgoing-communications` call it makes per recipient.

## Review trigger

If a restaurant's audience regularly exceeds what 5-minute batches clear in a
reasonable window (say, over an hour for a "send now"), raise the batch size
or the tick frequency first — both are runtime constants — before reaching
for a different dispatch mechanism.
