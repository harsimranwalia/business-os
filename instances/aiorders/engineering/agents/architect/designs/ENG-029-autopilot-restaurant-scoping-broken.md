---
ticket: ENG-029
project: aiorders-api
author: architect
created: 2026-09-03
adrs: [ADR-015]
one_way_doors: []
touches_data: false
touches_models: false
---

# Autopilot restaurant-ownership check — technical design

## Approach

All 8 actions need the same two checks, in the same order, before touching the
database: (1) a valid session exists at all (`user !== null`), and (2) that
user has access to the specific `restaurant_id` in scope. Check (1) is
identical for every action and belongs in exactly one place —
`index.ts`, immediately after `user` is decoded from the JWT, before routing
to any handler. Check (2) is action-specific because the 8 actions split into
two payload shapes: `list_templates`, `create_template`, `get_logs`,
`get_stats` carry `restaurant_id` directly; `get_template`, `update_template`,
`delete_template`, `toggle_template` carry only `template_id` and need it
resolved to a `restaurant_id` first (one `select restaurant_id from
communication_templates where id = template_id` lookup) before the same check
applies — matching the PRD's own AC1 language ("or a `template_id` resolving
to restaurant B"). Both files (`templates.ts`, `logs.ts`) already return
`{success:false, error}` for every failure mode, never throw — the fix follows
that existing convention rather than introducing a throw path neither file
uses today (see `ENG-022`'s design for why matching each file's own
convention, not unifying, is the standing rule here).

The ownership primitive itself is not written fresh: `_shared/
restaurantAccess.ts`'s `verifyRestaurantAccess(restaurantId, supabase, user)`
already implements the correct rule (platform-admin bypass, then
`brand_managers`, then `restaurant_managers`), already returns rather than
throws (matching this file's convention with no wrapper needed), and is
already deployed and imported cross-directory by `api-key-auth` for exactly
this "not part of the module I'm calling from" reason — see `ADR-015` for why
this is used instead of `brand-portal/utils.ts`'s version the PRD's own Notes
speculated about.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `supabase/functions/autopilot/index.ts` | modify — after `user` is decoded (~line 65), add: deny with 401 if `user` is `null`. One `console.warn` denial log line (no user id available in this case — log the attempted action only). Closes AC2 for all 8 actions in one place; the earlier `systemTriggered` marketing branch (~line 40) returns before this point and is untouched — separate bug class, filed as `ENG-035`. | backend |
| `supabase/functions/autopilot/handlers/templates.ts` | modify — thread `user` from `handleTemplates`'s own signature (already received, currently unused) down into all 6 action functions. `listTemplates`/`createTemplate`: check `verifyRestaurantAccess(restaurant_id, supabase, user)` right after the existing `restaurant_id` presence check. `getTemplate`/`updateTemplate`/`deleteTemplate`/`toggleTemplate`: resolve `template_id → restaurant_id` first (new lookup), then the same check. Import `verifyRestaurantAccess` from `../../_shared/restaurantAccess.ts`. | backend |
| `supabase/functions/autopilot/handlers/logs.ts` | modify — thread `user` from `handleLogs` into `getLogs`/`getStats`; same ownership check right after each function's existing `restaurant_id` presence check. Same import. | backend |
| `supabase/functions/autopilot/handlers/*_test.ts` (new, one per fixed source file) | new — `Deno.test` negative case per action (8) plus one positive case per payload shape (4: direct-`restaurant_id` actions, `template_id`-resolved actions, `logs.ts`'s own two actions treated as one shape, no-session case), per acceptance criterion 4 | backend |

**Test approach**, same precedent `ENG-022` already set for this repo (no
test runner registered in `config/projects.md`, not a blocker — Deno ships
one, no config needed): a minimal stubbed `SupabaseClient`-shaped object
(`.from().select().eq()...single()`/`.insert()`/`.update()`/`.delete()`
chains, only what each handler actually calls), no live project, no network.
Canned rows simulate "user manages restaurant A" for the positive cases and
"restaurant B" (or a `template_id` that resolves to restaurant B) for the
negative ones.

## Interfaces

`templates.ts`/`logs.ts`, every action function gains a `user: User` (or
compatible `any`, matching the file's existing loose typing) parameter and,
right after its existing `restaurant_id`-required check, this shape:

```ts
if (!user) {
  // unreachable in practice — index.ts already denies before this point —
  // kept as a defensive boundary check, not a second gate to maintain
}
const access = await verifyRestaurantAccess(restaurant_id, supabase, user)
if (!access.hasAccess) {
  console.warn(`Autopilot access denied: user=${user.id} restaurant=${restaurant_id}`)
  return { success: false, error: access.error || 'Access denied to this restaurant' }
}
```

For the four `template_id`-only actions, inserted before the block above:

```ts
const { data: existing, error: lookupError } = await supabase
  .from('communication_templates')
  .select('restaurant_id')
  .eq('id', template_id)
  .single()

if (lookupError || !existing) {
  return { success: false, error: 'Template not found' }
}
const restaurant_id = existing.restaurant_id
```

Failure response as seen by the brand portal: always HTTP 200 with
`{success:false, error}` — both files already use this convention uniformly
for every existing failure mode, so denial introduces no new response shape
(contrast `ENG-022`, where two different conventions co-existed across the
target directory).

`index.ts`'s new 401 path:

```ts
if (!user) {
  console.warn(`Autopilot: unauthenticated request, action=${action}`)
  return new Response(JSON.stringify({ error: 'Authentication required' }), {
    status: 401,
    headers: responseHeaders,
  })
}
```

placed immediately after the existing `user` decode, before the `!action`
check — a request with no valid session is denied regardless of which action
(or no action at all) it names, matching the PRD's framing of this as a
blanket gap, not a per-action one.

## Alternatives considered

1. **Import `brand-portal/utils.ts`'s check instead** (what the PRD's own
   Notes flagged as the likely primitive). Rejected: the throwing variant the
   PRD refers to (`requireRestaurantAccess`) exists only on `ENG-022`'s own
   unmerged branch today — using it would force `ENG-029` to either depend on
   `ENG-022` merging first or duplicate an unmerged rename, for no benefit
   over a primitive that already does the same check, already returns rather
   than throws (a better fit here), and is already on `main`. See `ADR-015`.
2. **Centralize the restaurant-ownership check in `index.ts` too**, alongside
   the new session check. Rejected — `index.ts` would need to know each
   action's field shape (`restaurant_id` directly vs. via `template_id`) and
   reach into `communication_templates` itself, mixing routing concerns with
   handler-specific domain knowledge. Keeping it in each handler, where the
   payload shape is already known, is the smaller change.
3. **Change the frontend contract so every action always sends `restaurant_id`
   directly**, removing the need to resolve `template_id`. Rejected — a
   client-facing interface change for a backend authorization bug, larger
   blast radius than necessary, and the resolve-by-lookup approach satisfies
   the acceptance criteria without touching the frontend at all.

## One-way doors

None. Adding an authorization check by importing an existing, already-deployed
shared primitive is fully reversible — no schema change, no new datastore, no
vendor, no contract change visible to any legitimate caller (AC3).

## Risks

- **Four actions gain a new lookup query** (`template_id → restaurant_id`)
  they didn't run before. Minor latency cost, no behavior risk — the same
  shape as any ownership-check-then-act pattern elsewhere in this codebase.
- **`deleteTemplate`/`updateTemplate`/`toggleTemplate` currently no-op
  (`deleteTemplate`) or PostgREST-error (`updateTemplate`/`toggleTemplate`'s
  own `.single()`) on a nonexistent `template_id`, inconsistently.** The new
  lookup makes all three return the same clean `{success:false, error:
  'Template not found'}` before reaching the original query — a minor,
  strictly-more-consistent behavior change, not a regression; not called out
  as its own fix since it falls directly out of the ownership-check lookup
  this ticket already adds.
- **No CI wiring runs `deno test`/`deno check`** (`config/projects.md`, same
  standing gap `ENG-022` already named for this repo). Tests run manually as
  part of `building`'s self-test step and QA's verification.
- **No evidence of actual exploitation** (carried from the PRD). Customer
  notification is a business/legal call, already surfaced to the approver via
  the P0 incident notice (`inbox/2026-09-03-eng029-p0-incident.md`).
- **Same file (`index.ts`) as `ENG-035`'s own fix, non-overlapping regions.**
  `ENG-035` edits the `systemTriggered` branch near the top of `serve()`;
  this design edits after the `apikey`/`user` block, further down. Not a
  `depends_on` — neither diff relies on the other's code being present, only
  a routine rebase if both are in flight at once. Flagged here the same way
  `ENG-022` flagged `feedback.ts`'s shared-file overlap with `ENG-023`.

## Rollout

Straight, no flag, no backfill — a logic-only fix on existing endpoints, no
schema change, no migration. Branch → PR → gates → human merge (`aiorders-api`
is L1) → deploy to the Supabase project. Qualifies for
`definition-of-done.md`'s P0-hotfix exception to the release window, same as
`ENG-022`. Rollback: revert the merge commit; no migration, so a revert fully
restores prior (broken) behavior with nothing further to clean up.

## Out of scope

- The `systemTriggered` marketing branch (`welcome_offer`/`birthday_offer`/
  `winback_offer`) — different bug class, different code path, filed
  separately as `ENG-035`.
- Auditing restaurant-ownership checks on edge functions outside `autopilot`
  and `brand-portal` (PRD non-goal; `ENG-022`'s and `ENG-030`'s PRDs already
  name this as a real, deferred question).
- Redesigning `communication_templates`/`communication_log` schema (PRD
  non-goal).
- Wiring `deno test`/`deno check` into CI — same standing out-of-scope item
  `ENG-022`'s design already named.
