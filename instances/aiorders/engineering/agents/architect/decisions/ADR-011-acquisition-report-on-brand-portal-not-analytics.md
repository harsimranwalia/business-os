---
id: ADR-011
title: the acquisition report is a brand-portal action, not an extension of the analytics function
project: aiorders-api
ticket: ENG-020
status: accepted
decided_by: architect
date: 2026-09-03
supersedes:
superseded_by:
---

# ADR-011: the acquisition report is a `brand-portal` action, not an extension of the `analytics` function

## Context

`ENG-020`'s PRD names its extension point explicitly: *"it extends the existing
`analytics` edge function (already queries both `orders` and `customers` for a
restaurant — `aiorders-api/supabase/functions/analytics/database.ts`)."* The
ticket's own Notes repeat it as *"confirmed by reading the code, not assumed."*
Both are correct that the join surface is there.

Reading the rest of that function against `origin/main` found what neither had
looked at: **`analytics/index.ts` performs no authentication or authorization
of any kind.** It reads `restaurantId` from the JSON body, constructs a client
with `SUPABASE_SERVICE_ROLE_KEY`, and never reads the `Authorization` header —
no `auth.getUser`, no `verifyRestaurantAccess`, no role check. Whatever the
Supabase gateway's `verify_jwt` default contributes proves only that some valid
project JWT was presented; the portal's publishable key is committed in
`restaurant-portal/src/integrations/supabase/client.ts`, and nothing anywhere
in the request path ties the caller to the restaurant being queried. The
repo's own catalog (`supabase/functions/README.md`) maintains a list of
functions with "no auth check at all" and `analytics` is not on it, so the gap
is invisible to the document `aiorders-api/CLAUDE.md` tells every engineer to
read first.

`ENG-020`'s acceptance criterion 5 requires a cross-tenant read to be rejected
server-side. So the PRD's named host cannot satisfy the PRD's own criterion
without first acquiring an access check it has never had.

Two ways to add one, both bad:

- **Guard only the new action.** `analytics` would then have one checked path
  and one open path in the same function. The department's standards name this
  exact shape as a defect in its own right: *"when one call path into it is
  guarded, the adjacent path carries the same guard... A function that fails
  closed on most inputs is read as fail-closed, so the one open path inherits
  that trust and survives review."*
- **Guard the whole function.** That is a P0-class security fix — the same bug
  class as `ENG-022` and `ENG-029` — landed inside a P2 feature ticket, against
  "no drive-by refactors" and "bundling a refactor: separate ticket, always."
  It also changes the behaviour of a live path the brand dashboard depends on,
  which would need its own verification that `functions.invoke` carries a user
  session token on every route that renders `Dashboard.tsx`.

Meanwhile `brand-portal` already is the brand portal's backend. It
authenticates every caller at the router (Bearer JWT → `supabase.auth.getUser`
→ 401), it already reads `customers` and `orders` for a single restaurant, it
already owns every other owner-facing portal read on this product (customers,
online orders, offers, menus, catering, feedback, website content, custom
reports), and `restaurant-portal` already talks to it through a dedicated
client class (`src/services/brandPortalApi.ts`). `analytics` is the outlier
here, not the norm — it is the one owner-facing read that sits outside the
portal's own authenticated API.

## Decision

`ENG-020` ships as a new `brand-portal` action, `get_acquisition_report`,
handled by a new `supabase/functions/brand-portal/acquisition.ts`, routed by
one new `case` in that function's existing `switch`. It authorizes with
`verifyRestaurantAccess(restaurant_id, supabase, user)` and branches on
`accessResult.hasAccess`, matching `menus.ts` / `catering.ts` /
`restaurants.ts` / `onlineOrders.ts` — and explicitly not `customers.ts` (which
discards the returned result) or `offers.ts` / `feedback.ts` (which pass the
arguments in the wrong order). It returns `{success:false, error}` at HTTP 200
on denial, choosing the returning one of this directory's two pre-existing
error conventions deliberately.

`analytics` is not modified by this ticket — not extended, not guarded, not
touched. Its missing access check is written up in the design's Risks and
proposed as its own P0 ticket, including adding it to `README.md`'s
"no auth check at all" list.

This deviates from the PRD's stated Proposed change. It does not deviate from
any acceptance criterion: AC1–AC5 name a restaurant owner, a brand portal, a
breakdown, a time range and server-side rejection, and none of them names a
function. The deviation is recorded here rather than absorbed silently so the
EM and PM can reverse it cheaply if they disagree.

## Alternatives

| Option | Why not |
|---|---|
| Extend `analytics` and guard only the new action | Leaves one guarded and one open path in the same function — the standards' *failure direction is uniform* rule names this exact shape as a reviewable defect, and the open path would keep inheriting the trust the guarded one creates. |
| Extend `analytics` and add the access check to the whole function | A P0-class security fix bundled into a P2 feature ticket, against "no drive-by refactors." Also changes a live path the dashboard depends on, requiring verification work this ticket has no reason to own. Correct thing to do — as its own ticket. |
| A brand-new dedicated edge function for the report | More surface than the work needs: a new function means new CORS handling, a new auth block, a new deploy target and a duplicated copy of the access helper (which `_shared/restaurantAccess.ts` already exists to avoid). It also cuts against this approver's demonstrated instinct — twice, at merge, he has rejected net-new things that duplicated existing intent. |
| Wait for `ENG-022` to merge and then extend `analytics` | `ENG-022` fixes five `brand-portal` handlers; it does not touch `analytics` and would not make it any safer to extend. Ordering does not change the argument. |

## Consequences

**Accepted:** the brand portal's analytics story is now split across two
backends — the year-to-date dashboard metrics still come from the unguarded
`analytics` function, while the acquisition report comes from the
authenticated `brand-portal`. That is an inconsistency a future engineer will
notice. It is the right inconsistency to have while `analytics` is unguarded,
and it resolves in the correct direction when the P0 ticket lands: with
`analytics` guarded, folding the two together becomes a real option.

**Accepted:** `brand-portal/index.ts`'s `switch` gains a third pending claim
this cycle (`ENG-014`'s `get_restaurant_media_info` and `ENG-023`'s
`update_feedback` are the other two). All three add a distinct `case` label;
the merge is mechanical.

**Gained:** AC5 is satisfied by construction on the first line of the handler,
using this codebase's own established ownership primitive, with no new auth
concept invented and no pre-existing security hole half-fixed. The report is
also automatically covered by the router's `API_KEY_ALLOWED_ACTIONS` rejection,
so a static machine key cannot read it.

**Reversibility:** cheap. Moving the handler into `analytics` later is a file
move plus a routing change and a one-line edit to the portal's service method.
No data migration; the RPC it calls is host-agnostic.

## Review trigger

Revisit when the `analytics` access-check ticket lands. At that point
`analytics` becomes a legitimate host, and the question is whether merging the
two owner-facing analytics surfaces into one is worth the churn — or whether
`brand-portal` should instead absorb what is left of `analytics` entirely,
retiring a function whose CloudWaitress half is already documented dead code
carrying a hardcoded reseller bearer token.
