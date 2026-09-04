---
ticket: ENG-030
project: aiorders-api
author: architect
created: 2026-09-03
adrs: []
one_way_doors: []
touches_data: false
touches_models: false
---

# `analytics` edge function has no authentication or authorization — technical design

## Approach

`analytics/index.ts` needs the same two checks `_shared/restaurantAccess.ts`
already gives every other cross-directory consumer: a valid session, then
ownership of the specific `restaurantId` in the request body. Both checks are
extracted into one new file, `analytics/auth.ts`, exporting a single function
— `authorizeAnalyticsRequest(req, supabase, restaurantId, corsHeaders)` —
that returns a denial `Response` or `null` (proceed). `index.ts` calls it
once, right after the client is created and `restaurantId` is parsed, before
the existing `source`/switch block.

This shape, not a direct inline check in `index.ts`, exists for one reason:
`index.ts` calls `serve(...)` at module scope, so importing it for a test
starts a listener — confirmed by reading every existing `*.test.ts` in this
repo (none imports a `serve`-wrapping `index.ts`; each imports a plain
exported function from a sibling module). Extracting only the new gate,
not the whole handler, is the smaller cut: `platform-customer-auth/handler.ts`
extracts its *entire* request handler for this same reason, but that
function has no existing, working, out-of-scope aggregation behind it the
way `analytics` has in `database.ts`/`cloudwaitress.ts`. Pulling the gate out
on its own keeps the untouched, unread aggregation code and its `source`
switch exactly where they are.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `supabase/functions/analytics/auth.ts` | new — `authorizeAnalyticsRequest(req, supabase, restaurantId, corsHeaders)`: decodes the caller from `Authorization`, denies with 401 if no valid session; else calls `verifyRestaurantAccess` (`_shared/restaurantAccess.ts`), denies with 403 if the caller doesn't own `restaurantId`; else returns `null`. | backend |
| `supabase/functions/analytics/index.ts` | modify — import `authorizeAnalyticsRequest`; move client creation above the `source` block (it already exists, just earlier); call the gate right after `restaurantId` is parsed and return its `Response` if non-null. No other line changes — the `source`/switch/error-catch-all block is untouched. | backend |
| `supabase/functions/analytics/auth.test.ts` | new — `Deno.test` per acceptance criterion, per the Interfaces section below | backend |

**Test approach**, same shape `ENG-029`'s design already committed to for
this same bug class today, and wider than `platform-customer-auth/handler.test.ts`'s
already-merged precedent: that file's own comment names not testing the
DB-dependent branches (invalid session past the header check, the ownership
lookup itself) as a "named, not silent, gap," because this repo has "no
precedent or infrastructure" for a mocked `SupabaseClient." AC4 here requires
exactly that branch (`wrong tenant → denied`), so this design can't reuse the
narrower approach — it needs the stub `ENG-029` already planned: a minimal
object implementing `.auth.getUser()` and the `.from().select().eq()...single()`
chains `verifyRestaurantAccess`/`isPlatformAdmin` call, canned per test case.
No live project, no network — same `DENO_NO_PACKAGE_JSON=1 deno test
--node-modules-dir=none` invocation `loyalty-config.test.ts` already proves
works on this repo.

## Interfaces

`auth.ts`:

```ts
export async function authorizeAnalyticsRequest(
  req: Request,
  supabase: SupabaseClient,
  restaurantId: string,
  corsHeaders: Record<string, string>,
): Promise<Response | null>
```

| Case | Result |
|---|---|
| No `Authorization` header, or `auth.getUser` returns no user | `401 {error: 'Authentication required', source: 'analytics-middleware'}` |
| Valid session, `verifyRestaurantAccess` → `hasAccess: false` (wrong tenant, or `restaurantId` doesn't exist) | `403 {error: access.error, source: 'analytics-middleware'}` — `access.error` is already differentiated ("Restaurant not found" vs. "Access denied to this restaurant") by the shared primitive itself; not a new distinction this design introduces (see Risks) |
| Valid session, `verifyRestaurantAccess` → `hasAccess: true` | `null` — `index.ts` proceeds to the existing, unchanged data-fetch switch |

`index.ts`'s only new lines:

```ts
const denied = await authorizeAnalyticsRequest(req, supabase, restaurantId, corsHeaders);
if (denied) return denied;
```

placed after the existing `if (!restaurantId) throw ...` check and client
creation, before the `source` variable and switch. Response body shape on
success is unchanged — still the raw `analyticsData` object `Dashboard.tsx`
already expects.

## Alternatives considered

1. **Mint a new ADR for the primitive choice.** Rejected — `analytics` is in
   the identical position `autopilot` was in (a function outside
   `brand-portal/`, needing the same cross-directory-safe check), and
   `ADR-015` already decided this exact question with reasoning that
   transfers unchanged: `_shared/restaurantAccess.ts`'s `verifyRestaurantAccess`
   over `brand-portal/utils.ts`'s, because the latter is a sibling module
   import and the throwing `requireRestaurantAccess` variant still only
   exists on `ENG-022`'s unmerged branch. A second ADR restating the same
   comparison for the same reason is a record with nothing new in it — this
   design cites `ADR-015` directly instead.
2. **Extract the whole handler into `handler.ts`**, matching
   `platform-customer-auth`'s proven shape exactly. Rejected — that repo-wide
   precedent exists because its whole handler needed testing; here only the
   new gate does. Moving the untouched `source`/switch/aggregation code into
   a second file is a pure refactor with no behavior or test coverage gained,
   against `tech-design`'s own "bundling a refactor" failure mode.
3. **Retire `analytics` and fold `Dashboard.tsx` into `brand-portal`'s new
   authenticated analytics surface**, floated as a real option in the PRD
   since `ENG-020`'s design already puts one there (`ADR-011`). Rejected for
   this ticket — `ADR-011` chose that path specifically to avoid extending
   `analytics` further, not to replace it, and retiring a function with a
   live consumer is a frontend contract change riding on a P0 security fix.
   Worth a follow-up proposal once `ENG-020` ships; not this ticket's
   "smallest thing."

## One-way doors

None. Same conclusion as `ENG-022`/`ENG-029`: importing an existing,
already-deployed shared primitive is fully reversible — no schema change, no
new datastore, no vendor, no contract change visible to a legitimate caller
(Interfaces table, success row).

## Risks

- **`access.error` distinguishes "restaurant not found" from "access denied"
  in the response body** — a caller can tell a nonexistent `restaurantId`
  from one that exists but isn't theirs (minor enumeration signal). Inherited
  from `_shared/restaurantAccess.ts` itself, already surfaced identically by
  `api-key-auth` and by `ENG-029`'s design for `autopilot` — changing it is a
  change to the shared primitive affecting three functions, out of scope for
  a single-function S ticket.
- **No CI wiring runs `deno test`** (`config/projects.md`, same standing gap
  every prior edge-function ticket this week has named). Tests run manually
  at `building`'s self-test step and QA's verification.
- **The existing 500 catch-all still returns `error.message` verbatim** for
  any unhandled exception (e.g. a `fetchDatabaseAnalytics` failure) —
  pre-existing behavior, unrelated to authorization, out of this PRD's scope
  (Non-goals: "redesigning `analytics/database.ts`'s aggregation logic").
  Noted, not fixed.
- **No evidence of actual exploitation** (carried from the PRD). Customer
  notification is a business/legal call, already surfaced via the P0
  incident notice (`inbox/2026-09-03-eng030-p0-incident.md`).

## Rollout

Straight, no flag, no backfill — a logic-only addition ahead of existing,
unchanged aggregation code; no schema change, no migration. Branch → PR →
gates → human merge (`aiorders-api` is L1) → deploy to the Supabase project.
Qualifies for `definition-of-done.md`'s P0-hotfix exception to the release
window, same as `ENG-022`/`ENG-029`. Rollback: revert the merge commit — no
migration, so a revert fully restores prior (broken) behavior with nothing
further to clean up.

## Out of scope

- Redesigning `analytics/database.ts`'s aggregation logic (PRD non-goal).
- Fixing the dead `cloudwaitress.ts` reseller-token path (PRD non-goal,
  already named in `README.md`'s own Notes).
- Auditing restaurant-ownership checks on edge functions outside `analytics`,
  `autopilot`, and `brand-portal` (PRD non-goal; third instance this week —
  worth the EM's or approver's attention as a pattern, named in the ticket's
  own board-file Notes, not expanded into a fourth PRD here).
- Wiring `deno test`/`deno check` into CI (standing out-of-scope item every
  prior edge-function ticket this week has named).
- Reconciling `_shared/restaurantAccess.ts` and `brand-portal/utils.ts`'s two
  independent implementations of the same rule — `ADR-015`'s own review
  trigger, not this ticket's.
