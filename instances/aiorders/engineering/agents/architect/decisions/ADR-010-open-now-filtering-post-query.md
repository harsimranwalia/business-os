---
id: ADR-010
title: "Open Now" filtering runs post-query in the edge function, not as a SQL predicate
project: restaurant-marketplace
ticket: ENG-026
status: accepted
decided_by: architect
date: 2026-09-03
supersedes:
superseded_by:
---

# ADR-010: "Open Now" filtering runs post-query in the edge function, not as a SQL predicate

## Context

`ENG-026`'s requirement 5 needs discovery results to exclude closed restaurants
when a consumer turns on "Open Now," per channel tab. No SQL-side hours
evaluation exists anywhere in this schema or its migrations. The only existing
hours logic is `restaurant-marketplace`'s client-side `src/utils/openingHours.ts`
(`getOpenState`, shipped on `origin/master`, not yet wired into any list/card
view) — a parser over Google-sourced free-form `opening_hours` weekday text.
Discovery results come from a Postgres RPC (`get_restaurants_optimized`,
`aiorders-api`) with a TypeScript fallback, both paginated via `LIMIT`/`OFFSET`.
The PRD explicitly defers the full operational-status engine (kitchen cutoffs,
alcohol-license time, happy-hour scheduling) as separate future work.

## Decision

Evaluate "is this restaurant open now" in the edge function's TypeScript layer,
after the DB query returns rows — for both the RPC path and the fallback path —
using a Deno port of the existing client parser (`_shared/openingHours.ts`).
`open_now=true` filters the already-fetched page in memory and also drives the
per-row status label shown for closed restaurants (requirement 3). No over-fetch
compensation is added for the resulting page-size shrinkage: a page can
legitimately return fewer than `limit` rows (or zero) when many results in that
slice are closed, and the query's `count: 'exact'` reflects the pre-filter
total, not the open-now-filtered total.

## Alternatives

| Option | Why not |
|---|---|
| Port the opening-hours parser into SQL/PL-pgSQL and filter in the RPC's `WHERE` clause | Substantially more work to parse free-form Google weekday text correctly in SQL; duplicates effort the PRD's own non-goal defers (the operational-status engine); the existing TS parser already does this correctly and porting TS→TS is the smaller, lower-risk change |
| Over-fetch (e.g. 3x `limit`) and truncate client-side to mask the post-filter shrinkage | Adds real complexity (a tuning factor, a cap) to guarantee something no acceptance criterion asks for; "Open Now" is opt-in and off by default, so the blast radius of an occasionally-short page is small and self-correcting on "load more" |

## Consequences

**Accepted:** pagination under `open_now=true` is approximate — a page can
under-return relative to `limit`, and the reported total count can overstate
what's actually visible once the open-now filter is applied.

**Gained:** no new hours-parsing logic to design, review, or maintain in SQL;
a single ported (not re-derived) implementation of "is this restaurant open"
drives both the discovery filter and the closed-status label.

**Reversibility:** cheap. Replacing the in-memory filter with a real SQL
predicate later touches only the discovery handler and the RPC's `WHERE`
clause — no data migration, no client contract change.

## Review trigger

Revisit if `open_now` usage or reported short-page/count-mismatch complaints
show this approximation is a real problem in practice, or when a future ticket
builds the full operational-status engine (PRD's deferred item 2) and a proper
server-side hours predicate becomes available as a side effect anyway.
