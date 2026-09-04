---
id: ADR-012
title: acquisition channels are classified post-query in TypeScript; SQL only aggregates
project: aiorders-api
ticket: ENG-020
status: accepted
decided_by: architect
date: 2026-09-03
supersedes:
superseded_by:
---

# ADR-012: acquisition channels are classified post-query in TypeScript; SQL only aggregates

## Context

`ENG-020` needs a restaurant's customers, orders and revenue bucketed into
named acquisition channels (organic search, direct, social, referral, paid,
email, …) over a date range. The raw material is the attribution data on
`customers`. Two questions had to be answered separately: *where does the
aggregation run*, and *where does the raw-value-to-channel mapping run*.

Three facts from `origin/main` decide it.

**The stored values are not a controlled vocabulary.** The columns that
actually exist are `first_touch_at`, `first_touch_source`, `first_touch_medium`,
`first_touch_campaign`, `first_referrer`, `last_touch_at`, `last_touch_source`.
(`utm_source`/`utm_medium`/`utm_campaign` are *not* columns on `customers`,
despite the PRD and ticket saying so — every capture path folds them into a
`first_touch`/`last_touch` object, and the separate `utm_data` object those
callers also send is never referenced in `crm/customers.ts` and is discarded.)
`first_touch_source` then mixes two unrelated kinds of value: real UTM sources
when a UTM was present, and **capture-surface names when one was not** —
`customer-signup.ts` writes `first_touch_source || utm_source || source ||
"offers-signup"`, and its siblings write `"email-signup"`, `"catering-form"`,
`"online-order"`. Elsewhere the platform writes `"online_order"` (underscore) —
`autopilot/marketing/welcome.ts` branches on that spelling while
`update-customer-tracking.ts` writes the hyphenated one. Nothing constrains
the column.

**The largest real channel is not in that column at all.**
`config-site-builder/src/utils/userTracking.ts` — the tracking every restaurant
website actually runs, initialised from `Layout.tsx` on every page load — sets
`first_touch_source: existingData?.first_touch_source || utmParams.utm_source`.
A visitor arriving from Google organic has no UTM, so the column stores
nothing; the only signal is `first_referrer`, a full URL captured by
`getReferrer()` (which correctly excludes same-hostname referrers). Classifying
organic search therefore requires parsing a referrer host, not matching a
source string.

So the mapping is a precedence chain — medium first, then source, then
sentinel detection, then referrer host, then unknown — not a lookup table.

**Pulling rows into the function to do it is not an option either.** The
function family this extends already tried and abandoned that: the comments in
`analytics/database.ts` read *"TIER 1: Pure Database Aggregations (O(1)
Performance - No Record Limits!)"*, *"TIER 2: RPC-based Aggregated Breakdowns
(No row limits!)"*, and *"TIER 3: Removed"*. Fetching a restaurant's orders
into the edge function to bucket them there would re-introduce the tier they
deleted and would trip automatic review failure #5 (unbounded query / missing
pagination).

`ADR-010` set this board's precedent for the general shape: run derived and
bucketing logic in the edge function's TypeScript layer, after the DB query
returns rows, when the SQL version would be substantially more complex.

## Decision

Split the work at the classification boundary.

**SQL aggregates.** A new `SECURITY DEFINER` RPC,
`get_acquisition_breakdown(p_restaurant_id, p_from, p_to)`, returns one row per
distinct `(first_touch_source, first_touch_medium, referrer_host)` tuple, each
with `customers_acquired`, `orders_count` and `revenue`. The result set is
bounded by attribution cardinality — a handful to a few dozen rows for a real
restaurant — not by order volume. `referrer_host` is `split_part(first_referrer,
'/', 3)`: the one piece of derivation SQL is allowed to do, because it is pure
cardinality reduction (collapsing thousands of distinct URLs into a few hosts)
and carries no judgement about what a host *means*.

**TypeScript classifies.** A pure `classifyChannel(source, medium, host) →
ChannelKey` in `brand-portal/channels.ts` — no I/O, no Supabase import, unit
testable on its own — maps each returned tuple to one of nine channel keys,
running the precedence chain in one place. The handler folds the tuples into
channels, computes the coverage and low-volume figures, and returns them.

The line is: **SQL reduces cardinality, TypeScript assigns meaning.** No
`CASE` expression in the RPC names a channel; no aggregation happens in the
edge function.

## Alternatives

| Option | Why not |
|---|---|
| Push the channel `CASE` into the RPC and return finished buckets | The classification is a five-step precedence chain over an uncontrolled vocabulary that mixes UTM values with form names and needs referrer-host matching against ~20 known domains. Expressing it in SQL is materially harder to read, far harder to unit test (no DB-free test path exists in this repo), and makes every future taxonomy change — adding a social network, recognising a new sentinel — a migration and a deploy rather than a code edit. |
| Fetch order rows into the edge function and do both aggregation and classification there | Unbounded query, automatic review failure #5, and the exact tier `analytics/database.ts` already removed for this reason with the comments still in the file. |
| Skip the RPC: use PostgREST's aggregate syntax with grouping over an embedded `customers` resource | Attractive — it would keep `touches_data: false` and avoid a migration entirely, and `database.ts` proves aggregates are enabled on this project. Rejected because grouping across an embedded resource could not be verified as working from the repo alone, and a query of that shape failing *quietly* (returning plausible but wrongly-grouped rows) is the worst failure mode available for a report whose whole purpose is being trustworthy. |
| Store a normalised `channel` column on `customers`, written at capture time | Would make reporting trivial, but it is a schema change plus edits to all five capture paths plus a backfill that cannot be computed for rows whose referrer was never stored — far outside an M, and it freezes the taxonomy into data where a mistake is expensive. The taxonomy should stay cheap to change while it is new. |

## Consequences

**Accepted:** the channel taxonomy exists only in code, so two callers reading
the same raw data could disagree about channels. Today there is exactly one
caller, and `channels.ts` is deliberately dependency-free so a second one
imports it rather than re-deriving it.

**Accepted:** one migration, so `touches_data: true` and `database` is in the
chain, for a ticket the PRD costed as having "no new data model." Accurate as
far as it goes — no table, no column, no row is added or altered; the migration
adds a read-only function.

**Gained:** the messy, opinionated, most-likely-to-change half of this feature
is a pure function with no database, no auth and no network in it — the
cheapest possible thing to test, and the classifier's precedence chain and
every sentinel string get real unit tests without a live schema. Changing or
extending the taxonomy later is a code change and a normal deploy.

**Reversibility:** cheap in both directions. Moving classification into SQL
later means a `CREATE OR REPLACE` on one function plus deleting a TypeScript
file; moving the aggregation back into TypeScript means dropping the RPC. No
data migration either way, no stored value depends on the current taxonomy.

## Review trigger

Revisit if a second consumer of the channel taxonomy appears — the staff-facing
all-restaurants rollup the PRD defers is the obvious candidate — and re-check
then whether the classifier still wants to live inside `brand-portal` or should
move to `_shared/`, the way `verifyRestaurantAccess` was duplicated into
`_shared/restaurantAccess.ts` once a second function needed it. Also revisit if
the attribution values ever become a controlled vocabulary (a `channel` column
written at capture time, or an enum), at which point most of the precedence
chain becomes dead weight.
