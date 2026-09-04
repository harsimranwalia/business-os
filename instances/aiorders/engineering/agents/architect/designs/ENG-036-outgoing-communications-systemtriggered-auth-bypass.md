---
ticket: ENG-036
project: aiorders-api
author: architect
created: 2026-09-03
adrs: [ADR-017]
one_way_doors: []
touches_data: false
touches_models: false
---

# `outgoing-communications`' `systemTriggered` branch skips authentication — technical design

## Approach

Same mechanism `ADR-016` chose for the sibling `autopilot` bug, reused here
(`ADR-017` records why, and why not as a shared file). `index.ts` also calls
`serve(...)` at module scope — importing it for a test starts a listener,
confirmed against every existing `*.test.ts` in this repo — so the check is
extracted into a new file, `outgoing-communications/auth.ts`, exporting
`authorizeSystemTrigger(req, responseHeaders): Response | null`, the same
signature `ADR-016` used, for the same reason: AC4 needs a regression test
that imports the gate without booting a server.

Unlike `autopilot`, where the check only guards three actions behind one
`marketingActions.includes(action)` branch, this function's entire auth
requirement is the one `if (!systemTriggered) { ...auth... }` block with no
`else` — every `actor`/`action` pair it serves shares it. The fix adds the
missing `else`: run the existing user-auth path when `systemTriggered` is
false (byte-for-byte unchanged), run `authorizeSystemTrigger` when it's true
(currently: nothing runs at all). One call site, ahead of the `actor` switch,
satisfies AC3 without a per-action gate.

**Caller enumeration (AC2), done directly rather than trusting the PRD's own
single example.** The PRD found one caller
(`autopilot/marketing/utils.ts`) because that was the file `ENG-035`'s own
design was already reading. This design step greps `outgoing-communications`
against each of this instance's five registered repos, at each repo's own
remote default branch — not `aiorders-api` alone:

| Caller | Repo | Sends `systemTriggered`? | Credential sent |
|---|---|---|---|
| `autopilot/marketing/utils.ts` `scheduleWithQStash` | aiorders-api | `true` | QStash `Upstash-Forward-Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}` — arrives at this function as `Authorization` |
| `autopilot/marketing/utils.ts` `sendViaOutgoingComms` | aiorders-api | `true` | `Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}`, direct |
| `cloudflare-workers/queue-consumer/index.ts` (the Worker feeding both `autopilot`'s queue and this function's own sends — `welcome_offer`/`every_order`/`first_order`/`birthday`/`winback`/`event_offer`/`order_feedback_request`) | aiorders-admin-hub | `true` | `Authorization: Bearer ${env.SUPABASE_SERVICE_ROLE_KEY}`, direct |
| `restaurant-influencer-campaigns/handlers/influencer-invitations.ts`, `visit_scheduled` | aiorders-api | not set | forwards the calling user's own `Authorization` header |
| `Activation.tsx`, `sendBagInsertEmail` (`bag_insert_shared`) | aiorders-admin-hub | not set | the signed-in user's session token |
| `campaigns/CreateEdit.tsx`, `campaign_created` | restaurant-portal | not set | `supabase.functions.invoke`'s own ambient user session |
| `restaurant-marketplace`, `config-site-builder` | — | — | no reference to this function in either repo |

All three `systemTriggered: true` callers already send exactly the header
`ADR-016` chose — confirmed by reading each call site's own source, not
inferred from an untracked mechanism the way `ENG-035`'s evidence had to be.
Its central risk (the legitimate caller is a DB trigger with no tracked
headers) does not apply here: every caller of this function is an HTTP call
site this repo's or `aiorders-admin-hub`'s own source shows in full. The
three callers that don't set `systemTriggered` already go through the
untouched `!systemTriggered` branch today and stay on it — this diff does
not add an `else` that could catch them, and does not touch that branch's
own lines.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `supabase/functions/outgoing-communications/auth.ts` | new — `authorizeSystemTrigger(req, responseHeaders)`: reads the `Authorization` header, compares to `` `Bearer ${Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')}` ``, logs a distinct, greppable message and returns a 401 `Response` on any mismatch or missing header; returns `null` on match. | backend |
| `supabase/functions/outgoing-communications/index.ts` | modify — import `authorizeSystemTrigger`; add the missing `else` to the existing `if (!systemTriggered) { ... }` block, calling the gate and returning its `Response` if non-null, before the `actor` switch. No other line changes — the switch, every actor handler call, and the non-systemTriggered path are untouched. | backend |
| `supabase/functions/outgoing-communications/auth.test.ts` | new — one `Deno.test` per case in the Interfaces table below | backend |

## Interfaces

```ts
export function authorizeSystemTrigger(
  req: Request,
  responseHeaders: Record<string, string>,
): Response | null
```

| Case | Result |
|---|---|
| No `Authorization` header | 401 `{success: false, error: 'System credential required'}`; `console.error('[outgoing-communications] systemTriggered denied: missing Authorization header')` |
| `Authorization` present but not `Bearer ${SUPABASE_SERVICE_ROLE_KEY}` | same 401 body; `console.error('[outgoing-communications] systemTriggered denied: invalid system credential')` |
| `Authorization` === `` `Bearer ${SUPABASE_SERVICE_ROLE_KEY}` `` | `null` — `index.ts` proceeds to the `actor` switch, behavior unchanged (AC2) |

Response body deliberately matches *this* function's own existing shape
(`{success: false, error: ...}`, from its own catch-all) rather than
`ADR-016`'s (`{error, source}`) — `Activation.tsx`'s own
`sendBagInsertEmail` is a confirmed real caller of this same function
(non-`systemTriggered` path) and already does
`if (!res.ok || !json.success) throw new Error(json.error || ...)`, so
matching this function's own body shape is not just local style but keeps a
real, already-reading caller correct. Status code (401) still follows
`ADR-016`, not this function's own catch-all (400) — see Alternatives.

`index.ts`'s only new lines, completing the existing branch:

```ts
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
} else {
  const denied = authorizeSystemTrigger(req, corsHeaders)
  if (denied) return denied
}
```

## Alternatives considered

1. **Extract into `_shared/`, alongside `restaurantAccess.ts`/`apiKeys.ts`**,
   sharing one `authorizeSystemTrigger` across `autopilot` and this function.
   Rejected for now: `ADR-016`'s own file (`autopilot/marketing/auth.ts`)
   isn't built yet either — `ENG-035` is still `designed`, not `building` —
   so there is nothing to share from in the tree today. Forcing this ticket
   to create the shared version first would couple `ENG-036`'s build to
   `ENG-035`'s branch (stacking, the way `ENG-009`/`ENG-010` stack on
   `ENG-008`) for a ~20-line duplicate with zero behavioral cost.
   `_shared/`'s own precedent (`restaurantAccess.ts`, per `ADR-015`) is a
   substantially larger, genuinely-reused ownership lookup — not a symmetry
   argument for every small duplicate. Filed as an observation, not a
   proposal: worth doing once both tickets ship, blocks neither.
2. **Match this function's own 400-via-catch-all** instead of a dedicated
   401 `Response`. Rejected: `ADR-016` already set 401 as this project's
   convention for "a `systemTriggered` gate denies," its own Review trigger
   asks for one system-trust convention rather than two, and none of the six
   confirmed callers above branch on status code — so there is no functional
   cost to the more correct code. Named here as a deliberate, narrow
   inconsistency with this same function's *other* auth path (still 400,
   untouched, out of scope) rather than left implicit.
3. **New dedicated secret, or a separate secret per caller.** Rejected, same
   reasoning `ADR-016` already recorded, worse here: three live callers
   across two repos (`aiorders-api`, `aiorders-admin-hub`) would all need
   coordinated reconfiguration this session cannot make or verify, against
   one header three independent call sites already send correctly today.
4. **Timing-safe string comparison.** Rejected — same reasoning `ADR-016`
   gives: not a standard this codebase holds itself to anywhere else, and
   edge-function network jitter makes the attack impractical regardless.

## One-way doors

None. An additive header check ahead of existing, unchanged handler code —
no schema change, no new datastore or vendor, no contract change visible to
any of the three confirmed-legitimate callers, which already send this
header. Decided here rather than escalated.

## Risks

- **Lower residual risk than `ADR-016`'s own case, and worth naming why.**
  `ENG-035`'s central risk was a DB trigger whose actual headers are
  unverifiable from source. Nothing here is a DB trigger — all three
  `systemTriggered: true` callers are HTTP call sites read in full this
  pass, so what they send is confirmed, not inferred.
- **What's still unverifiable from source: whether the deployed value of
  `SUPABASE_SERVICE_ROLE_KEY` actually matches between the Cloudflare Worker
  environment (`aiorders-admin-hub`'s `queue-consumer`) and the Supabase
  project's own secret** — an operational/config risk, not a code-logic one,
  and this session has no CLI/dashboard access to either secrets store to
  confirm it directly. Mitigation is the same shape `ADR-016` used: a
  distinct denial log line (Interfaces table) makes a real mismatch visible
  in Supabase function logs immediately after deploy, and Rollout below adds
  a mandatory (if lighter-weight) manual check.
- **No evidence of actual exploitation** (carried from the PRD).

## Rollout

Straight, no flag, no backfill — logic-only, ahead of existing unchanged
handler code; no schema change, no migration. Branch → PR → gates → human
merge (`aiorders-api` is L1) → deploy. Qualifies for
`definition-of-done.md`'s P0-hotfix exception to the release window, same as
`ENG-022`/`ENG-029`/`ENG-030`/`ENG-035`. Rollback: revert the merge commit —
no migration, so a revert fully restores prior (broken) behavior with
nothing further to clean up.

**Mandatory manual post-deploy check**, lighter than `ENG-035`'s (three
confirmed HTTP callers, not one unverifiable DB trigger) but not skipped:
after deploy, check Supabase function logs for `outgoing-communications` for
the new `[outgoing-communications] systemTriggered denied` line over the
following day, during which the queue consumer and `autopilot`'s own
scheduled/immediate sends should both fire at least once. Its absence
confirms the service-role key matches across both deploy targets in
practice, not just in source. If it appears against a real send, this is the
Risks section's named failure materializing — revert immediately, don't
leave it broken while investigating, same as `ADR-016`'s own Review trigger.

## Out of scope

- The three non-`systemTriggered` callers (`visit_scheduled`,
  `bag_insert_shared`, `campaign_created`) — untouched, already correctly
  authenticated via a forwarded or ambient user session.
- `ENG-035`'s own `autopilot` fix — separate file, separate ticket, already
  in flight.
- `_shared/` consolidation of the two `authorizeSystemTrigger` copies — see
  Alternatives; filed as an observation.
- Stub actions (`admin.ts`, most of `influencers.ts`) — unimplemented,
  unaffected, out of scope per the PRD.
- `consumers.ts`'s `customerEmail` override behavior — named in the PRD's
  own Non-goals, not re-litigated here.
