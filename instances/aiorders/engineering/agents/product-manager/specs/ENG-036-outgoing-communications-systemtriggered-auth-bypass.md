---
ticket: ENG-036
project: aiorders-api
status: draft
size: S
author: architect
created: 2026-09-03
decided:
---

# `outgoing-communications` skips authentication entirely for any system-triggered send — cross-actor unauthenticated message dispatch

**Auto-approved type (`security`) — no readback, no G1.** Per
`skills/request-readback/SKILL.md`, agent-originated findings with their own
evidence skip the readback. Per
`agents/eng-manager/config/definition-of-done.md`'s ticket-states table,
`security`-typed tickets auto-skip `awaiting-scope` (G1). This PRD is
intentionally short.

**Discovered incidentally**, not the thing this pass was assigned to build:
`continue ENG-035`'s own tech-design research required reading
`outgoing-communications/index.ts` in full, since `autopilot/marketing/utils.ts`'s
`sendViaOutgoingComms`/`scheduleWithQStash` both call it directly and
understanding the receiving side's own trust model was necessary to design
`ENG-035`'s fix. That read found `outgoing-communications` has the identical
bug shape `ENG-035` itself has — a client-supplied `systemTriggered` boolean
that skips authentication entirely — but wider: it gates *every* actor and
action this function serves, not just three marketing offers behind one
flag. Different file, non-overlapping diff from `ENG-035`'s own
(`autopilot/marketing/`, not `outgoing-communications/`) — out of scope for
that ticket's own diff, so filed as its own ticket per
`schedules/eng_build_loop.md` step 3's P0 carve-out, same as `ENG-029` →
`ENG-035` earlier today.

## Problem (the evidence)

`outgoing-communications/index.ts` parses the request body, and if
`systemTriggered` is true, skips its entire authentication block:

```ts
// index.ts
const { action, actor, data, systemTriggered } = await req.json()
let user = null
if (!systemTriggered) {
  const authHeader = req.headers.get('Authorization')
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    throw new Error('Authorization header required for user-triggered communications')
  }
  const token = authHeader.replace('Bearer ', '')
  const { data: { user: authUser }, error: authError } = await supabase.auth.getUser(token)
  if (authError || !authUser) {
    throw new Error('Unauthorized')
  }
  user = authUser
}
```

Exactly like `ENG-035`'s own `autopilot` bug, `systemTriggered` is a plain
boolean read straight from the caller's own JSON body — not a header,
signature, or secret. Unlike `ENG-035`, this check gates the function's
*entire* auth requirement, for *every* `actor`/`action` pair it routes
(`influencer`, `brand`, `consumer`, `admin`), not one narrow branch.

Confirmed reachable and real (not stub) by reading all four `actors/*.ts`
handlers in full:
- `consumers.ts` (857 lines): `welcome_offer`/`every_order`/`first_order`
  (the same sends `ENG-035`'s own `autopilot` triggers) plus
  `order_feedback_request` — a real implementation that fetches a live
  order/customer/restaurant/brand record by a caller-supplied `orderId` and
  sends an email, optionally to a caller-supplied `customerEmail` instead of
  the order's own.
- `brands.ts` (466 lines): real campaign-notification emails to a
  restaurant's actual owners/managers, fetched live from `brand_managers`/
  `restaurant_managers`.
- `admin.ts` (47 lines) and most of `influencers.ts`: stubs, `TODO`, not
  implemented.

`autopilot/marketing/utils.ts` calls this function with
`Authorization: Bearer <SUPABASE_SERVICE_ROLE_KEY>` when it's the legitimate
caller — but that header is never checked on the receiving end;
`systemTriggered` in the body is sufficient on its own.

## Impact — who is affected and how

Any caller, with no key, no session, and no credential of any kind, can
`POST {actor: 'consumer', action: 'order_feedback_request', systemTriggered:
true, data: {orderId: <any real or guessed uuid>, customerEmail:
<any address>}}` and cause a real email — built from a real order's live
data — to be sent wherever they specify, on the business's own send budget
and sender reputation. The same zero-credential bar reaches `brands.ts`'s
campaign-notification path, hitting real restaurant owners/managers. Same
class of harm as `ENG-035` (real-world side effect and cost, not a data
read) but broader surface: every actor/action this function serves, not
three offers behind one flag.

Per `agents/eng-manager/config/security-baseline.md`, in `aiorders-api`
("Highest blast radius of the set — shared backend for all four
frontends"). Rated **P0**, same bar `ENG-022`/`ENG-029`/`ENG-030`/`ENG-035`
were rated at.

## Proposed change

Behavior, not implementation — the architect's call at the design step, same
as `ENG-035`. `ENG-035`'s own design (`ADR-016`, once it lands) is the most
direct precedent available: this function already receives
`Authorization: Bearer <SUPABASE_SERVICE_ROLE_KEY>` from its one confirmed
legitimate internal caller (`autopilot/marketing/utils.ts`) today, so the
same mechanism may transfer directly — the design step confirms this against
this function's actual callers rather than assuming it, since this function
may have callers `ENG-035`'s own narrower research didn't need to enumerate.

## Acceptance criteria

1. `[stated]` Given a caller with no valid system credential, when they POST
   `systemTriggered: true` for any `actor`/`action` pair, the call is
   denied, not served.
2. `[stated]` Given the legitimate system caller(s) —
   `autopilot/marketing/utils.ts`'s `scheduleWithQStash` and
   `sendViaOutgoingComms`, and any other in-repo caller the design step
   finds — behavior is unchanged.
3. `[inferred]` The fix applies once, ahead of the `actor` switch, so it
   covers every current and future actor/action pair rather than needing a
   per-action gate.
4. `[proposed]` A regression test proves both the negative case (no/invalid
   system credential → denied) and the positive case (legitimate credential
   → proceeds), same test-runner gap and precedent
   `ENG-022`/`ENG-029`/`ENG-030`/`ENG-035` already named for this repo.

## Non-goals

- Fixing any of the stub actions (`system_alert`, `user_signup`,
  `error_notification`, most of `influencers.ts`) — they stay stubs; only
  the auth gate in front of them is this ticket's concern.
- `ENG-035`'s own `autopilot` fix — separate file, separate ticket, already
  in flight.
- Auditing `consumers.ts`'s `customerEmail` override behavior itself (a
  caller with a *valid* credential can still redirect a feedback email to an
  address they supply) — a real question, but a different one from
  authentication; named here as a follow-on worth asking, not expanded into
  this ticket's scope.

## Risks and unknowns

- **Every legitimate caller of this function must be enumerated at design
  time**, not just the one this PRD found (`autopilot/marketing/utils.ts`) —
  a wider audit than `ENG-035`'s own single-caller case, since this function
  may serve more of the codebase than the one path this PRD's evidence
  covers. Missing one silently breaks it, same risk class `ENG-035`'s own
  Risks names for its trigger.
- **No evidence of actual exploitation** — confirmed live vulnerability, not
  a confirmed breach.

## Cost

- **Build:** `S` — one function, one auth block, likely reusing `ENG-035`'s
  own resolved mechanism once it lands. Does not displace machine-WIP on its
  own.
- **Run:** $0/month.

## Decision

N/A — `security`-typed tickets auto-skip G1
(`agents/eng-manager/config/definition-of-done.md`). Filed directly per the
P0 carve-out. The approver is notified as an incident, not asked to approve
starting the fix.
