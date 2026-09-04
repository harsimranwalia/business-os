---
ticket: ENG-029
project: aiorders-api
status: draft
size: M
author: architect
created: 2026-09-03
decided:
---

# Autopilot API: every action trusts `restaurant_id` from the request body — cross-tenant customer-data exposure

**Auto-approved type (`security`) — no readback, no G1.** Per
`skills/request-readback/SKILL.md`, agent-originated findings with their own
evidence skip the readback. Per
`agents/eng-manager/config/definition-of-done.md`'s ticket-states table,
`security`-typed tickets auto-skip G1 and go straight to `designed`. This PRD
is intentionally short — the evidence below stands in for a Problem/Users
narrative.

**Discovered incidentally**, not the thing this pass was assigned to build:
`continue ENG-019`'s own tech-design research (restaurant marketing
broadcasts) required reading `aiorders-api`'s `outgoing-communications`/
`autopilot` send-and-log system as reusable prior art. That read surfaced
that this function has no restaurant-ownership check anywhere in it — out of
scope for an architect design pass to fix quietly inside another ticket's
diff, so filed as its own ticket per `schedules/eng_build_loop.md` step 3's
P0 carve-out and the ticket template's `source:` field note (a P0 on a
non-internal-lane project "keeps its agent source").

## Problem (the evidence)

`supabase/functions/autopilot/index.ts` gates every request behind one check
only: the caller's `apikey` header equals `SB_PUBLISHABLE_KEY`
(`index.ts:54-55`) — Supabase's publishable/anon key, shipped in every
frontend bundle, the same value for every tenant and not a secret. It then
optionally decodes a JWT into `user` (`index.ts:65`), and its own comment
says why: "Get user from JWT for logging/context" — confirmed by reading
every handler it's threaded into: **`user` is never passed to, or checked
by, a single one of the eight actions this function serves.**

Every handler takes `restaurant_id` straight from the request payload and
queries by it with no ownership check:

```ts
// handlers/templates.ts:28-41 (listTemplates) — same shape at getTemplate (52),
// createTemplate (76-97), updateTemplate (150+), deleteTemplate (186+), toggleTemplate (209+)
const { restaurant_id } = payload;
if (!restaurant_id) { return { success: false, error: 'restaurant_id is required' }; }
const { data, error } = await supabase.from('communication_templates')...eq('restaurant_id', restaurant_id)...
```

```ts
// handlers/logs.ts:19-41 (getLogs), 84-97 (getStats) — identical shape against communication_log
```

The Supabase client in this function is created with the **service-role
key**, which bypasses RLS entirely — so even if `communication_templates`/
`communication_log` carried a tenant-scoping RLS policy, it would not apply
here. There is no other layer between the request and the query.

This is not a partial defeat like `ENG-022`'s (a check called wrong at 5 of 9
sites) — it is a total absence: none of the 8 actions (`list_templates`,
`get_template`, `create_template`, `update_template`, `delete_template`,
`toggle_template`, `get_logs`, `get_stats`) has ever had a restaurant-ownership
check.

## Impact — who is affected and how

Any caller who can reach this endpoint — which needs only the public,
non-secret publishable key, not even a valid logged-in session, since `user`
is never required to be non-null — can supply an arbitrary `restaurant_id`
and get:

| File | Actions | Exposure |
|---|---|---|
| `handlers/templates.ts` | list/get/create/update/delete/toggle | Read **and write** any restaurant's automation templates — email/SMS subject, body, delay, active/inactive |
| `handlers/logs.ts` | get_logs, get_stats | Read any restaurant's `communication_log` — customer name (via join), **recipient email, recipient phone**, message subject/body, delivery status |

`restaurant_id` is a plain UUID already visible client-side, same as
`ENG-022`'s finding — no exploit tooling needed. `aiorders-api` is registered
"Highest blast radius of the set — shared backend for all four frontends"
(`config/projects.md`).

Per `agents/eng-manager/config/security-baseline.md` ("An active security
incident (leaked credential, live exploit, exposed data) — P0"): this is
live, currently exposed customer PII (email, phone) plus write/delete access
to another restaurant's marketing automation, in production, reachable today
with no authenticated session required. Rated **P0**, same bar `ENG-022` was
rated at, for the same reason — contrast `ENG-026`'s finding on
`admin-portal`'s `updateRestaurant()` (no field allow-list, filed as a
proposal, not a P0), which requires the caller to already be a legitimate
user of the target restaurant; this one does not.

## Proposed change

Behavior, not implementation. Every `autopilot` action that takes a
`restaurant_id` needs a real ownership check before it touches the
database — `brand-portal/utils.ts`'s `verifyRestaurantAccess` (or `ENG-022`'s
promoted `requireRestaurantAccess`, once that ticket ships) is the existing,
already-correct primitive; whether `autopilot` imports it directly or gets
its own copy is the architect's call.

## Acceptance criteria

1. `[stated]` Given an authenticated user with access to restaurant A only,
   when they call any of the 8 `autopilot` actions with restaurant B's
   `restaurant_id` (or a `template_id` resolving to restaurant B), then the
   call is denied, not served.
2. `[stated]` Given an unauthenticated caller (no valid JWT, publishable key
   only), when they call any of the 8 actions, then the call is denied —
   closing the "no session required at all" gap named above, not just the
   cross-tenant one.
3. `[inferred]` Given a legitimate owner of restaurant A calling these same
   actions for restaurant A, behavior is unchanged.
4. `[proposed]` A regression test exists per fixed action proving the
   negative case (wrong tenant, and no session, → denied), not just the
   positive case. `aiorders-api` has no test runner today
   (`config/projects.md`) — same standing gap `ENG-022` named; whatever
   scaffolding that ticket builds, this one reuses.

## Non-goals

- Redesigning `communication_templates`/`communication_log` schema — the
  exposure is authorization, not data modeling.
- Auditing restaurant-ownership checks on edge functions outside `autopilot`
  and `brand-portal` — `ENG-022`'s own PRD already named this as a real,
  deferred question; worth a dedicated sweep if a third instance turns up,
  not repeated per-instance as an ever-growing PRD scope.
- `ENG-019`'s own broadcast feature (the ticket whose research surfaced
  this) — unrelated code path, tracked separately, and its own design will
  not reuse `autopilot`'s current pattern regardless of this ticket's
  timeline.

## Risks and unknowns

- **No test runner on this project** — same standing gap `ENG-022`'s PRD
  already named for the same repo.
- **Not exhaustively enumerated beyond `autopilot`** — this design pass
  traced `index.ts` and both handler files fully; it did not re-check every
  edge function in the repo for the same absence (see Non-goals).
- **No evidence of actual exploitation** — confirmed live vulnerability, not
  a confirmed breach; customer notification is the approver/security's call,
  not this PRD's.

## Cost

- **Build:** `M` — one function, two handler files, a known small action
  set, no new data model. Likely similar band to `ENG-022` (half a day to a
  day). Does not displace machine-WIP on its own — starts once a slot is
  free and `priority` (approver-only) says to jump the queue, same as
  `ENG-022`.
- **Run:** $0/month.

## Decision

N/A — `security`-typed tickets auto-skip G1
(`agents/eng-manager/config/definition-of-done.md`). Filed directly per the
P0 carve-out. The approver is notified as an incident, not asked to approve
starting the fix.
