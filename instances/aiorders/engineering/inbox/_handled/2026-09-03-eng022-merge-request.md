---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-api
ticket: ENG-022
recommendation: merge — code review, quality, and security all passed; no migration (pure access-check logic fix, no schema or data change); P0 fix for live cross-tenant PII read + write exposure, single repo, no cross-ticket branch dependency
time_estimate: half a day to a day
pr_url: https://github.com/harsimranwalia/aiorders-api/pull/9
raised: 2026-09-03
notified: 2026-09-03T01:26:47
nudged: 2026-09-04T01:52:01
decision:
---

# Merge request — Fix broken restaurant-scoped access checks in brand-portal (ENG-022)

## What this does

Any authenticated brand-portal user could read or write any other
restaurant's feedback, customers, offers, website content, or hiring data by
supplying a different `restaurant_id` — the shared `verifyRestaurantAccess()`
check was silently defeated on 5 of 9 handler files in
`supabase/functions/brand-portal/`, two different ways: wrong argument order
plus a truthy-object check instead of `.hasAccess` (`feedback.ts`,
`offers.ts`), and the check's return value discarded entirely (`customers.ts`,
`hiring.ts`, `website.ts`). No exploit tooling needed — just a different
`restaurant_id`, already visible client-side.

The fix promotes the existing, correctly-implemented but never-called
`verifyRestaurantAccessLegacy` to `requireRestaurantAccess` for the 4
throw-convention files (11 call sites); `offers.ts` (8 call sites) is fixed
in place, matching its own already-correct siblings. A09 denial logging
added on both paths. 24 new `Deno.test` cases (19 negative, one per call
site; 5 positive). Full account: `ENG-022`'s own board file.

**P0** — live, currently-reachable customer PII exposure plus unauthorized
cross-tenant writes, on the platform's highest-blast-radius project
(`aiorders-api`, shared backend for all four frontends).

## Gates passed

- Code review: **pass** — `agents/principal-engineer/reviews/ENG-022.md`
- Quality: **pass** — `agents/qa/test-plans/ENG-022.md` (all 4 acceptance criteria covered; 24/24 tests pass)
- Security: **pass** — `agents/security/reviews/ENG-022.md` (OWASP A01–A10 walked, zero blocking findings; confirmed every `brand-portal` handler runs on a service-role client, so this check is the *only* access control in the function, not one layer among several)
- Migration: n/a — pure access-check logic fix, no schema or data change

## PR

https://github.com/harsimranwalia/aiorders-api/pull/9

`aiorders-api` is registered **L1** — this department opens the PR, a human
merges. Merge whenever suits you on GitHub directly; the next build-loop
pass detects the merge itself (local git ancestry check, no action needed
from you beyond the merge) and advances the ticket to `shipped`.

## Decision

Filled in by the approver.
