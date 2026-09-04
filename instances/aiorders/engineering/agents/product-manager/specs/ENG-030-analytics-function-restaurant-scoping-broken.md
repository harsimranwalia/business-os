---
ticket: ENG-030
project: aiorders-api
status: draft
size: S
author: architect
created: 2026-09-03
decided:
---

# `analytics` edge function has no authentication or authorization at all — cross-tenant revenue/order/customer exposure

**Auto-approved type (`security`) — no readback, no G1.** Per
`skills/request-readback/SKILL.md`, agent-originated findings with their own
evidence skip the readback. Per
`agents/eng-manager/config/definition-of-done.md`'s ticket-states table,
`security`-typed tickets auto-skip `awaiting-scope` (G1). This PRD is
intentionally short — the evidence below stands in for a Problem/Users
narrative.

**Discovered incidentally**, not the thing this pass was assigned to build:
`continue ENG-020`'s own tech-design research (marketing ROI/traffic-source
reporting) required reading the `analytics` function in full, because the
PRD it was designing against named `analytics/database.ts` as this ticket's
extension point. Reading the rest of that function — `index.ts`, which
neither the PRD, the ticket's own Notes, nor `observations.md` had looked at
— found it has no access check of any kind. Out of scope for a design pass
to fix quietly inside another ticket's diff, so filed as its own ticket per
`schedules/eng_build_loop.md` step 3's P0 carve-out, same as `ENG-029` two
passes ago today.

## Problem (the evidence)

`supabase/functions/analytics/index.ts` reads `restaurantId` straight from
the JSON request body, builds a Supabase client with
`SUPABASE_SERVICE_ROLE_KEY`, and calls `fetchDatabaseAnalytics(supabase,
restaurantId)` — at no point does it read the `Authorization` header, call
`auth.getUser`, or check any role/ownership relationship between the caller
and the restaurant being queried:

```ts
// supabase/functions/analytics/index.ts
const { restaurantId } = await req.json();
if (!restaurantId) { throw new Error('Restaurant ID is required'); }
const supabase = createClient(supabaseUrl, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
analyticsData = await fetchDatabaseAnalytics(supabase, restaurantId);
```

Whatever the Supabase gateway's `verify_jwt` default contributes proves only
that *some* valid project JWT was presented — the project's
publishable/anon key is committed in
`restaurant-portal/src/integrations/supabase/client.ts`, so any caller can
obtain one. Nothing in the request path ties the caller to the restaurant
being queried.

**Why this stayed invisible.** `supabase/functions/README.md` — the
document `aiorders-api/CLAUDE.md` tells every engineer to read first —
maintains an explicit, consolidated list of functions with "no auth check at
all," and `analytics` is not on it. Its own per-function section (`##
analytics`) likewise says nothing about authorization in its Notes. The
function reads as covered by omission.

This is not a partial defeat like `ENG-022`'s (a correct check called with
the wrong arguments or its result discarded) or `ENG-029`'s (a check that
exists but is never threaded into the handlers) — it is a function with zero
access-check code anywhere in its request path.

## Impact — who is affected and how

Any caller holding the project's publishable key — shipped in every
frontend bundle, not a secret — and a restaurant UUID — a plain value
already visible client-side on every one of this product's own pages, same
as `ENG-022`'s and `ENG-029`'s findings — can supply an arbitrary
`restaurantId` and receive that restaurant's full yearly analytics payload:
total revenue, order count, tip totals, dish/service counts, and
customer-count metrics (`analytics/database.ts`'s aggregation). No valid
login is required — only the same publishable key every visitor's browser
already has.

`aiorders-api` is registered "Highest blast radius of the set — shared
backend for all four frontends" (`config/projects.md`).

Per `agents/eng-manager/config/security-baseline.md` ("An active security
incident (leaked credential, live exploit, exposed data) — P0") and its A01
Broken Access Control checklist item ("Every new route/endpoint/action has
an authz check... No IDOR: object access is scoped by owner, not by ID
alone"): this is live, currently exposed business data (revenue, order
volume, customer counts) for any restaurant on the platform, in production,
reachable today with no authenticated session required. Rated **P0**, same
bar `ENG-022` and `ENG-029` were rated at, for the same reason: the caller
needs no pre-existing relationship to the target restaurant at all.

## Proposed change

Behavior, not implementation. `analytics`'s one request path needs a real
ownership check before it queries the database —
`brand-portal/utils.ts`'s `verifyRestaurantAccess` (or `ENG-022`'s promoted,
throwing `requireRestaurantAccess`, once that ticket ships) is the existing,
already-correct primitive; whether `analytics` imports it directly, gets its
own copy (as `api-key-auth` did into `_shared/restaurantAccess.ts`), or the
function is retired in favour of folding its one consumer into
`brand-portal` (a real option now that `ENG-020`'s design puts a second,
authenticated analytics surface into `brand-portal` already) is the
architect's call at the design step.

## Acceptance criteria

1. `[stated]` Given an authenticated user with access to restaurant A only,
   when they call `analytics` with restaurant B's `restaurantId`, then the
   call is denied, not served.
2. `[stated]` Given an unauthenticated caller (no valid JWT, publishable key
   only), when they call `analytics` with any `restaurantId`, then the call
   is denied — closing the "no session required at all" gap, not just the
   cross-tenant one.
3. `[inferred]` Given a legitimate owner of restaurant A calling `analytics`
   for restaurant A, behavior is unchanged — the brand portal's existing
   `Dashboard.tsx` must keep working exactly as it does today.
4. `[proposed]` A regression test proves the negative case (wrong tenant,
   and no session, → denied), not just the positive case. `aiorders-api` has
   a working Deno test invocation and a real precedent
   (`admin-portal/handlers/loyalty-config.test.ts`,
   `DENO_NO_PACKAGE_JSON=1 deno test --node-modules-dir=none`) —
   `config/projects.md`'s all-empty command row for this repo is stale, not
   a blocker.

## Non-goals

- Redesigning `analytics/database.ts`'s aggregation logic — the exposure is
  authorization, not the metrics themselves.
- Fixing the dead `cloudwaitress.ts` path's hardcoded reseller bearer token
  (already flagged in `README.md`'s own Notes for this function) — separate,
  already-named cleanup, not a cross-tenant exposure.
- Auditing every other edge function's access checks — `ENG-022`'s and
  `ENG-029`'s PRDs already named this as a real, deferred question. Three
  independent instances of this bug class this week (`ENG-022`, `ENG-029`,
  this ticket) is worth a dedicated sweep if a fourth turns up; not repeated
  per-instance as an ever-growing PRD scope. Worth the EM's or approver's
  attention regardless of this ticket's own scope.

## Risks and unknowns

- **`Dashboard.tsx` is `analytics`'s one known live consumer** — whatever
  check the design adds must not break the brand portal's existing
  dashboard for a legitimate owner; AC3 exists because of this.
- **No evidence of actual exploitation** — confirmed live vulnerability, not
  a confirmed breach; customer notification is the approver/security's call,
  not this PRD's.
- **Not exhaustively enumerated beyond `analytics`** — this finding traced
  one function fully; it does not re-check every edge function in the repo
  (see Non-goals).

## Cost

- **Build:** `S` — one function, one request path, an existing
  ownership-check primitive to reuse, no new data model. Likely smaller than
  `ENG-022`/`ENG-029` (single call site, not five-to-eight). Does not
  displace machine-WIP on its own — starts once a slot is free and
  `priority` (approver-only) says to jump the queue, same as `ENG-022`/`ENG-029`.
- **Run:** $0/month.

## Decision

N/A — `security`-typed tickets auto-skip G1
(`agents/eng-manager/config/definition-of-done.md`). Filed directly per the
P0 carve-out. The approver is notified as an incident, not asked to approve
starting the fix.
