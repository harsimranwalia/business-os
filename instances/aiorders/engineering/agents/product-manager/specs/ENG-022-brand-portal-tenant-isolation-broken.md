---
ticket: ENG-022
project: aiorders-api
status: draft
size: M
author: product-manager
created: 2026-08-29
decided:
---

# Brand-portal API: restaurant-scoped access check is a no-op on 5 of 9 handlers — cross-tenant data exposure

**Auto-approved type (`security`) — no readback, no G1.** Per
`skills/request-readback/SKILL.md`, agent-originated findings with their own
evidence skip the readback (there is no intent to interpret — this is a code
defect, not a request). Per `templates/prd.md` and
`agents/eng-manager/config/definition-of-done.md`'s ticket-states table,
`security`-typed tickets auto-skip G1 and go straight to `designed`. This PRD
is intentionally short — the evidence below stands in for a Problem/Users
narrative.

**Discovered incidentally**, not the thing the intake pass was assigned to
build: shaping `agents/product-manager/inbox/2026-08-29-the-feedback-board-on-the-brand-portal-does-not-have-status-.md`
(now `ENG-023`) required tracing `restaurant-portal`'s Feedback page to its
backend (`aiorders-api`'s `brand-portal` edge function). That trace surfaced a
broken authorization check — out of scope for a PM to fix or judge alone, so
per `agents/product-manager/agent.md`'s `never_touches` list this is filed as
its own ticket rather than folded into `ENG-023`. Per
`schedules/eng_build_loop.md` step 3 and `agents/eng-manager/config/templates/ticket.md`'s
`source:` field note, a P0 on a non-internal-lane project "keeps its agent
source" and is filed directly rather than queued through
`agents/eng-manager/proposals.md`.

## Problem (the evidence)

`supabase/functions/brand-portal/utils.ts` exports
`verifyRestaurantAccess(restaurantId, supabase, user, options)`, returning
`Promise<{hasAccess: boolean, error?: string}>` — it never throws on denial,
callers must check the field. Two different mistakes defeat that check across
the same directory:

**Pattern A — wrong argument order, checked as a bare boolean.**
`feedback.ts:46` and all 8 call sites in `offers.ts` (lines 79, 146, 186, 224,
264, 304, 366, 424):

```ts
const hasAccess = await verifyRestaurantAccess(supabase, user.id, restaurant_id)
if (!hasAccess) { throw / return error }
```

Arguments are shifted by one position against the real signature
(`restaurantId, supabase, user, options`), so `supabase` (an object) lands in
the `restaurantId` slot and the function's own internal
`supabase.from('profiles')...` call throws immediately on a string — caught by
its own `try/catch`, which returns `{hasAccess: false, error: '...'}`. That
whole **object** — always truthy — is what gets bound to the local
`hasAccess`, so `if (!hasAccess)` can never be true, for any caller, any
`restaurant_id`, regardless of who actually owns that restaurant.

**Pattern B — correct arguments, return value discarded.** `customers.ts`
(lines 73, 124, 155, 186, 224), `hiring.ts` (37, 66, 115), `website.ts` (84,
120):

```ts
await verifyRestaurantAccess(restaurant_id, supabase, user)
```

Called for its side effect only. Nothing inspects `.hasAccess`. Since the
function reports denial by return value, never by throwing, this line does
nothing at all — every call proceeds regardless of the result.

**Confirmed correct, for contrast** (proper `if (!result.hasAccess)` /
`if (!access.hasAccess)` checks, correct argument order):
`catering.ts`, `restaurants.ts`, `menus.ts` (7 sites), `onlineOrders.ts`'s
`checkAccess()` wrapper. So this is not a misunderstanding of the utility
itself — 4 of 9 files call it correctly, which is also why this wasn't caught
by a working example elsewhere in the same file being copied wrong.

## Impact — who is affected and how

Any authenticated brand-portal user (any restaurant owner/manager login — no
elevated role needed) can call the `brand-portal` edge function with an
**arbitrary `restaurant_id`** and, for every affected action, get the same
result a legitimate owner of that restaurant would:

| File | Actions | Exposure |
|---|---|---|
| `feedback.ts` | `get_feedback` | Read any restaurant's customer feedback — name, email, phone, message, linked order |
| `offers.ts` | get/create/update/delete/toggle offers, specials | Read **and write** any restaurant's promotions |
| `customers.ts` | get/create/update/delete customers | Read **and write** any restaurant's customer list — name, email, phone |
| `website.ts` | get/update website content | Read **and overwrite** any restaurant's public website content |
| `hiring.ts` | jobs / candidates | Read/write any restaurant's hiring data |

`restaurant_id` is a plain UUID already visible client-side (e.g. the current
restaurant's own ID in `restaurant-portal`'s context) — reaching another
tenant's data needs no exploit tooling, just a different value in an
already-authenticated request. `aiorders-api` is registered in
`config/projects.md` as **"Highest blast radius of the set — shared backend
for all four frontends."**

Per `agents/eng-manager/config/security-baseline.md` ("An active security
incident (leaked credential, live exploit, exposed data) — P0") and
`agents/security/agent.md`'s own `interrupt_rule` ("P0 only — active
incident, leaked credential, or **exposed data**"): this is live, currently
exposed customer PII and write access, in production, reachable today. Rated
**P0**, not P1 — contrast `ENG-015` (also a confirmed cross-tenant exposure,
rated P1), which exposed restaurant/location listings, not customer PII, and
had no unauthenticated-relative-to-tenant write path.

## Proposed change

Behavior, not implementation (the architect owns how) — but flagging the
shape of the problem since it's a repeated pattern, not one typo: whatever
fix is chosen should make "call the function and forget to check the result"
structurally hard to repeat a sixth time, not just patch the five known call
sites. A throwing wrapper (`requireRestaurantAccess`, deprecating the
call-and-check pattern entirely) is one way; there may be better ones.

## Acceptance criteria

1. `[stated]` Given an authenticated user with access to restaurant A only,
   when they call any `brand-portal` action listed above with restaurant B's
   id, then the call is denied (`success: false` / thrown error), not served.
2. `[stated]` Given the same setup, when they call `get_feedback`,
   `get_offers`/`create_offer`/`update_offer`/`delete_offer`/`toggle_offer_status`,
   `get_customers`/`create_customer`/`update_customer`/`delete_customer`,
   `get_website_content`/`update_website_content`, or the hiring actions for
   restaurant B, then every one is denied — this is a full audit of every
   `verifyRestaurantAccess` call site in `brand-portal/`, not just the ones
   named in this ticket, since two independent mistakes already slipped past
   review once.
3. `[inferred]` Given a legitimate owner of restaurant A, when they call these
   same actions for restaurant A, then behavior is unchanged — this is a
   correctness fix, not a new restriction on legitimate use.
4. `[proposed]` A regression test exists per fixed call site proving the
   negative case (wrong tenant → denied), not just the positive case — per
   `agents/security/agent.md`'s own review checklist ("An authz test that only
   proves the authorised user gets in proves nothing"). `aiorders-api` has no
   `deno.json`/test runner today (`config/projects.md`) — see Risks.

## Non-goals

- Redesigning `verifyRestaurantAccess` itself — it is correct; every failure
  is at the call site.
- Auditing access checks outside `supabase/functions/brand-portal/` (other
  edge functions, other projects) — real question, explicitly out of scope
  for this ticket; worth a follow-on proposal if the architect agrees the
  pattern is worth checking elsewhere.
- The feature work this was discovered while shaping (`ENG-023`) — unrelated
  code path, tracked separately.

## Risks and unknowns

- **No test runner on this project.** `aiorders-api` has no `package.json` or
  `deno.json` (`config/projects.md`, confirmed again this pass) — "whatever
  verification it gets will be `deno test`/`deno lint`/`deno check` against a
  `deno.json` that does not exist yet. That is a ticket, not a blank to fill
  in." Acceptance criterion 4 may need that scaffolding built first, or a
  manual verification plan if the architect decides scaffolding a whole test
  runner shouldn't block a P0 fix.
- **Not exhaustively enumerated.** This PM traced every `verifyRestaurantAccess`
  call site found by a repo-wide grep in `brand-portal/` specifically and
  classified each by reading its surrounding code — high confidence on the
  9 files and ~25 call sites listed above, but did not check other edge
  functions outside this one directory (see Non-goals) or re-run the grep
  after any local changes.
- **No evidence of actual exploitation** — this is a confirmed, live
  vulnerability, not a confirmed breach. Nothing here implies customer
  notification is warranted; that determination belongs to the security
  gate/architect/approver, not this PRD.

## Cost

- **Build:** `M` — mechanical fix across a known set of call sites in one
  directory, no new data model. Half a day to a day, plus whatever the
  missing-test-runner risk above adds. Displaces one machine-WIP slot on an
  already-full board (6/6) — this is exactly the kind of ticket the WIP cap
  exists to let jump the queue via `priority`, but that field is the
  approver's alone to set.
- **Run:** $0/month. No new infrastructure.

## Decision

N/A — `security`-typed tickets auto-skip G1
(`agents/eng-manager/config/definition-of-done.md`). Filed directly per the P0
carve-out. The approver is notified as an incident, not asked to approve
starting the fix.
