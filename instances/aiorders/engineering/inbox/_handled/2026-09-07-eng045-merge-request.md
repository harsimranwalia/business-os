---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-api
ticket: ENG-045
recommendation: merge — code review (round 2), quality, and security all passed (security: zero findings); no migration owed (schema already shipped with ENG-044); second sub-ticket of the ENG-026 family, unblocks ENG-047's UI half
time_estimate: half a day
pr_url: https://github.com/harsimranwalia/aiorders-api/pull/20
raised: 2026-09-07
notified: 2026-09-07T10:57:56
nudged:
decision: merged
---

# Merge request — FoodSwipe channel-visibility discovery handlers — open-now gating and status (ENG-045)

Sub-ticket of `ENG-026` (FoodSwipe channel-visibility toggles and
capability-based discovery), sequence 2 of 4 — depended on `ENG-044` alone
(merged). `ENG-047` (the "Open Now" chip UI) depends on this ticket.

## What this does

- **New:** `supabase/functions/_shared/openingHours.ts` — a Deno port of
  `restaurant-marketplace`'s client-side `getOpenState`, now also usable
  server-side.
- `handleRestaurantDiscovery` maps the existing `mode` param to `p_channel`
  on the `get_restaurants_optimized` RPC call; `handleRestaurantDiscoveryFallback`
  gets the matching `.eq()` gate on the direct-query path.
- Both paths compute a per-row `status` label and apply the `open_now`
  filter post-fetch, per `ADR-010` (fail-open: unknown/open hours are never
  excluded; only confirmed-closed rows are dropped, and only when
  `open_now=true` is explicitly requested).
- `handleRestaurantDetail` gains the three `has_order_food`/`has_dine_in`/
  `has_catering` flags in its response.
- The pre-existing, independent `orderingLink`-presence filter on
  `order-food` is untouched — both gates are `AND`ed, neither replaces the
  other.

**Found and fixed before shipping:** the live `restaurants.opening_hours`
column stores `{day, open, close, isClosed?, h24?}` objects, not the
`weekday_text` string list the original client-side parser assumed. A
straight port would have silently returned `{isOpen: null, label: null}`
for every row in production, satisfying the code shape while filtering
nothing. Fixed in `toWeekdayLines` (recognizes both shapes); 9 tests cover
it, including `isClosed`/`h24`/overnight-past-midnight. The client-side copy
in `restaurant-marketplace` likely has the same gap — proposed separately
(different repo, already shipped, not this diff).

## Gates passed

- **Code review: pass (round 2)** — `agents/principal-engineer/reviews/ENG-045.md`.
  Round 1's one blocking finding (decision logic not exported, per
  `engineering-standards.md`) fixed with a two-line, zero-behavior-change
  diff; round 2 confirmed nothing else changed.
- **Quality: pass** — `agents/qa/test-plans/ENG-045.md`. Both owned criteria
  (AC3 in full, AC4's backend half) covered, 15/15 tests, mutation-checked
  (forcing `channelForMode`/`evaluateOpenNow` to wrong answers turned exactly
  the expected tests red).
- **Security: pass, zero findings** — `agents/security/reviews/ENG-045.md`.
  Verified directly that the channel value can never reach an arbitrary
  column or RPC argument; confirmed the route's lack of authentication
  pre-exists this diff; no secrets, no new dependency, no PII.
- No migration owed — the schema and RPC argument shipped with `ENG-044`
  (merged); confirmed no `ENG-045-*.md` migration file exists.

## Release readiness

- **Rollback:** no migration and no stored-state change in this diff —
  reverting the merge (once merged) fully undoes it.
- **Observability:** read the actual handler code, not assumed — all three
  touched exported functions (`handleRestaurantDiscovery`,
  `handleRestaurantDiscoveryFallback`, `handleRestaurantDetail`) already
  wrap their full body in try/catch, log a distinct `console.error(...)`
  message, and return a 500 on failure. Pre-existing, unchanged by this
  diff, and it also covers the new `channelForMode`/`evaluateOpenNow` calls
  since they run inside the same try blocks.
- **Cost:** $0/month — same Supabase project, handler-level code only, no
  new dependency, no new infrastructure.
- **Window:** n/a — `aiorders-api` is registered L1; opening a PR is not a
  release.

## PR

https://github.com/harsimranwalia/aiorders-api/pull/20

This project is registered **L1** — this department opens the PR, a human
merges. The next build-loop pass detects the merge itself (local git
ancestry, no reply needed from you) and advances the ticket.

## Non-blocking findings, named not fixed

- `openingHours.ts`'s catch blocks log nothing on the caught-exception path
  — ported from the existing (already-silent) client-side behavior, not a
  regression; worth a `console.error` if this file is next touched.
- `channelForMode`/`evaluateOpenNow` are now exported (per
  `engineering-standards.md`'s decision-logic rule) but have no direct unit
  test of their own yet — real behavioral coverage already exists indirectly
  through the six handler tests.

## Out of scope

- The "Open Now" chip UI (`ENG-047`).
- The pre-existing `orderingLink` filter's own test coverage (predates this
  diff).
- `total`/`hasMore` staying pre-filter under the `open_now` exclusion —
  `ADR-010`'s accepted pagination trade-off, not a gap.

Second of `ENG-026`'s four sub-tickets. `ENG-047` depends on this one and
stays `ready` until this ticket reaches `verified` — noted so whichever pass
finds the merge knows to check it next.
