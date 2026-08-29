---
type: eng-decision
agent: eng-manager
gate: one-way-door
project: aiorders-api
ticket: ENG-007
recommendation: proceed with ENG-007 itself now (low-stakes, additive, easily dropped) — but confirm before ticket 3 (the points ledger) is filed, since that's where a second, real points-tracking system would start running in production alongside Walletly's
raised: 2026-08-29
notified: 2026-08-29T07:53:00
decision: approved
decided: 2026-08-29T08:10:30.599034+00:00
---

# G2 — This department found a live third-party loyalty vendor (Walletly) already integrated. Does the native loyalty sequence still proceed as scoped?

## The question

While designing `ENG-007` (the per-restaurant earn-rate/redemption config
table, item 2 of the loyalty sequence approved at `ENG-006`'s G1), this pass
found `supabase/functions/external-integrations/handlers/walletly.ts` — a
real, currently-wired integration to `api.walletly.ai` that already fetches
a customer's loyalty points balance and a brand's reward catalog. It's
catalogued in the repo's own `supabase/functions/README.md`, and it was last
touched 2026-07-07 in a repo-wide cleanup — seven weeks before this loyalty
sequence was requested, not abandoned years ago.

Neither your original request (preserved verbatim in `ENG-006`'s ticket)
nor `knowledge/business-profile.md` mentions Walletly. This department has
no way to tell, from anything on disk, whether that's because it's a legacy
integration you're already moving away from, a per-brand add-on that's fine
to run alongside a platform-native program, or the thing you actually meant
by "loyalty" when you filed the original request — in which case this
five-ticket sequence would be building a second, competing system instead
of what you asked for.

## Why this is being asked now, at ticket 2, and not decided quietly

`ENG-007` itself carries no risk either way — see its design
(`agents/architect/designs/ENG-007-per-restaurant-loyalty-configuration.md`):
one additive table, nothing calls it yet, trivially dropped if the answer
changes. The actual exposure is ticket 3, the points ledger — that's where
a second real points-tracking system would start running in production
alongside Walletly's. Once diners and restaurants have live balances in
both, unwinding either one is a data-migration and user-facing problem, not
a schema change. Flagging it before ticket 3 is filed is strictly cheaper
than flagging it after.

## Recommendation

**Proceed with `ENG-007` now** — build the config table as designed; it's
useful groundwork regardless of how the Walletly question resolves, and
holding it would cost real time for no real risk reduction, since nothing
in its own design depends on the answer.

**Before ticket 3 is filed, confirm one of:**
1. Walletly is being retired/replaced — the native sequence is the
   intended replacement, proceed as originally scoped.
2. Walletly stays, and this sequence is meant to run alongside it for a
   different purpose (e.g. Walletly per-brand, the native system
   platform-wide) — worth naming the boundary explicitly so ticket 3
   doesn't build a ledger that silently double-counts or conflicts.
3. Something else — you tell us how these two are supposed to relate.

If you already know the answer and it's option 1 or 2, a one-line reply is
enough to unblock ticket 3 the moment it's filed; no need to re-scope
anything already approved at `ENG-006`.

## Decision

Filled in by the approver.

## Decision

**approved** — 2026-08-29T08:10:30.599034+00:00

Walletly is being retired/replaced

---

**Processed 2026-08-29 (`watch` event pass, context `schtasks`).** Found during
this event's own three-inbox sweep — the answer arrived by hand-edit to this
file directly, not through `lib/eng-notify.sh`'s reply path (this pass's own
mode check and gate-check ran clean before touching anything; the earlier
`SLACK_WEBHOOK_URL unset` failure logged when this item was raised is the
known, already-open `proposals.md` channel-dispatch gap, not a new finding).
Caught fresh by this sweep ahead of a `decision` event already queued behind
it for this same file (`traces/.pending`) — processed here rather than left
for that queued event, per this instance's established practice that
whichever event reaches the fact first does the real work; the queued
`decision` will very likely no-op when it drains next, the same shape this
ticket's own G1 hit in reverse order minutes earlier.

Read as answering option 1 of the three the gate offered: Walletly is being
retired/replaced, so the native loyalty sequence proceeds exactly as
originally scoped — no boundary-setting needed (that was only required under
option 2). Ticket advanced `awaiting-decision → ready`. Journaled in
`agents/eng-manager/config/decision-journal.md`. Full reasoning on the
ticket's own log
(`agents/eng-manager/board/ENG-007-per-restaurant-loyalty-configuration.md`).
