---
ticket: ENG-035
project: aiorders-api
status: draft
size: S
author: architect
created: 2026-09-03
decided:
---

# `autopilot`'s system-triggered marketing actions skip authentication entirely — a client-controlled flag reaches a real message-send trigger with no gate

**Auto-approved type (`security`) — no readback, no G1.** Per
`skills/request-readback/SKILL.md`, agent-originated findings with their own
evidence skip the readback. Per
`agents/eng-manager/config/definition-of-done.md`'s ticket-states table,
`security`-typed tickets auto-skip `awaiting-scope` (G1). This PRD is
intentionally short — the evidence below stands in for a Problem/Users
narrative.

**Discovered incidentally**, not the thing this pass was assigned to build:
`continue ENG-029`'s own tech-design research (restaurant-ownership check on
`autopilot`'s 8 template/log actions) required reading `index.ts` in full to
design the fix. That read found a third routing branch, gated by a
client-supplied `systemTriggered` flag, that `ENG-029`'s own PRD never
examined — its evidence explicitly scoped to "every one of the 8 [template/
log] actions." Different bug class from `ENG-029` (an authentication bypass
via a trusted-flag-from-the-client, not a missing ownership check) and a
non-overlapping code path (`marketing/`, not `handlers/templates.ts`/
`handlers/logs.ts`) — out of scope for that ticket's own design to fix
quietly inside its diff, so filed as its own ticket per
`schedules/eng_build_loop.md` step 3's P0 carve-out, same as `ENG-029` and
`ENG-030` earlier today.

## Problem (the evidence)

`supabase/functions/autopilot/index.ts` checks for a system-triggered
marketing call **before** any authentication check runs, and the flag it
trusts is read straight from the caller's own request body:

```ts
// index.ts
const { action, systemTriggered, ...payload } = await req.json();
const marketingActions = ['welcome_offer', 'birthday_offer', 'winback_offer'];
if (systemTriggered && marketingActions.includes(action)) {
  const result = await handleMarketing(action, payload, supabase);
  return new Response(JSON.stringify(result), { status: 200, headers: responseHeaders });
}
// apikey check happens only below this point — never reached for a systemTriggered call
```

`systemTriggered` is not a header, signature, or secret — it is a plain
boolean field in the JSON body, indistinguishable from any other payload
field. Nothing verifies the caller is actually the trusted system component
(a Postgres database trigger, per `handlers/welcome.ts`'s own comment: "Called
by database trigger when a new customer is created") rather than an arbitrary
HTTP caller. This is a documented assumption in the repo's own
`supabase/functions/README.md` (`## autopilot`, Notes): "system-triggered
marketing calls skip auth entirely (**should never be publicly reachable
without another gate**)" — read directly, confirmed no such gate exists
anywhere before `handleMarketing` runs.

Of the three marketing actions, `welcome_offer` is the one with a real
implementation (`marketing/welcome.ts`); `birthday_offer`/`winback_offer` are
unimplemented stubs that always return `{success: false}` (confirmed by
reading both files directly, and matches `README.md`'s own "Known issues"
list). `handleWelcomeOffer` takes `customer_id`, `restaurant_id`, and
`first_touch_source` straight from the payload with no validation that the
pairing is real or that the caller has any relationship to either, and
either:

- queues two delayed sends via QStash (`marketing/utils.ts`'s
  `scheduleWithQStash`), or
- calls `outgoing-communications` **immediately**, authenticated with the
  function's own `SUPABASE_SERVICE_ROLE_KEY` (`sendViaOutgoingComms` — the
  secret is read server-side from `Deno.env`, never exposed to the caller,
  but its presence is what makes `outgoing-communications` act on the
  request).

## Impact — who is affected and how

Any caller, with **no key, no session, and no credential of any kind** — not
even the non-secret publishable key the other 8 `autopilot` actions require —
can `POST` `{action: 'welcome_offer', systemTriggered: true, customer_id:
<uuid>, restaurant_id: <uuid>, first_touch_source: 'manual'}` and cause a real
"welcome offer" email/SMS to be sent to that customer, attributed to that
restaurant, on the business's own send budget (QStash + email/SMS provider
cost) — repeatably, since nothing checks whether the pairing is genuine or
whether this customer already received one. This is a live, unauthenticated
trigger for a real-world side effect (message send, real cost, potential
customer harassment/spam and brand-deliverability damage), not a data read —
different in kind from `ENG-022`/`ENG-029`/`ENG-030`'s cross-tenant *read*
exposures, and arguably reachable by a lower bar than any of them (those
three all require at least the committed publishable key; this requires
nothing).

`customer_id`/`restaurant_id` are UUIDs, not sequential — a caller needs to
already hold or guess a valid pairing for the send to land on a real person,
which bounds blind mass-abuse somewhat, but does not require any
authentication once a pairing is known (e.g., leaked via `ENG-022`'s or
`ENG-029`'s own exposures, or simply observed client-side by a customer of
one restaurant targeting another).

Per `agents/eng-manager/config/security-baseline.md` ("An active security
incident (leaked credential, live exploit, exposed data) — P0"): this is a
live, currently-reachable exploit with a real production side effect and
cost, in `aiorders-api`, registered "Highest blast radius of the set — shared
backend for all four frontends" (`config/projects.md`). Rated **P0**, same
bar `ENG-022`/`ENG-029`/`ENG-030` were rated at — a live exploit needing zero
credentials clears the bar at least as clearly as their read-only exposures
did.

## Proposed change

Behavior, not implementation. The `systemTriggered` branch needs a real trust
check before it runs `handleMarketing` — something only the legitimate
system caller (the database trigger's own invocation path) can present, not
a value copied from the request body. Whether that's a shared-secret header
compared against a new dedicated env var, routing the trigger through a
mechanism that already carries a verifiable signature, or removing the
early-auth-bypass and giving the marketing actions their own service-level
credential check is the architect's call at the design step — this PRD
states the requirement, not the mechanism.

## Acceptance criteria

1. `[stated]` Given a caller with no valid system credential, when they POST
   `systemTriggered: true` with any `marketingActions` value, then the call
   is denied, not served.
2. `[stated]` Given the legitimate system caller (however that's verified),
   when it triggers `welcome_offer` for a real new customer, then behavior is
   unchanged — the existing new-customer welcome flow must keep working.
3. `[inferred]` `birthday_offer`/`winback_offer` (unimplemented stubs) are
   gated the same way as `welcome_offer`, not left on the old check, so
   implementing either later doesn't silently reopen this gap.
4. `[proposed]` A regression test proves the negative case (no/invalid system
   credential → denied) per marketing action, not just the positive case —
   same test-runner gap and precedent `ENG-022`/`ENG-029`/`ENG-030` already
   named for this repo.

## Non-goals

- Fixing `birthday_offer`/`winback_offer`'s own unimplemented logic — they
  stay stubs; only the auth gate in front of them is this ticket's concern.
- `ENG-029`'s own 8 template/log actions — separate code path, separate
  ticket, already in flight.
- Auditing `outgoing-communications` itself for the same
  `systemTriggered`-trusts-the-body pattern (it has an identical-shaped
  check, `index.ts:35`, not read in depth for this PRD) — worth a follow-on
  if this pattern recurs a fourth time; named here rather than expanded into
  scope.

## Risks and unknowns

- **The legitimate invocation path (the actual Postgres trigger/webhook
  config) was not located in this repo** — `welcome.ts`'s own comment names
  it, but the trigger/webhook definition itself lives in the Supabase project
  config or a migration this PRD did not find. The design step needs to
  confirm how the real caller invokes this today before choosing a mechanism
  that caller can actually satisfy.
- **No evidence of actual exploitation** — confirmed live vulnerability, not
  a confirmed breach; customer notification is the approver/security's call,
  not this PRD's.
- **`outgoing-communications` has the same-shaped check** (see Non-goals) —
  not verified fixed or broken; if this ticket's fix pattern applies there
  too, that's a fast follow, not blocking this one.

## Cost

- **Build:** `S` — one function, one routing branch, likely a single new
  trust check. Does not displace machine-WIP on its own — starts once a slot
  is free and `priority` (approver-only) says to jump the queue, same as
  `ENG-022`/`ENG-029`/`ENG-030`.
- **Run:** $0/month.

## Decision

N/A — `security`-typed tickets auto-skip G1
(`agents/eng-manager/config/definition-of-done.md`). Filed directly per the
P0 carve-out. The approver is notified as an incident, not asked to approve
starting the fix.
