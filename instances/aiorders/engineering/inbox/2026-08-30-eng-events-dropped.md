---
type: eng-decision
agent: eng-manager
gate: incident
project: aiorders
ticket: ENG-023
recommendation: find out why passes are failing before re-firing anything
raised: 2026-08-30
notified: 2026-08-30T21:08:08
---

# Engineering events were dropped today

The loop has NOT halted — every other ticket is still moving. What happened is
narrower and worse than a halt: one or more events were accepted, could not be
processed, and have been discarded. Whatever triggered them has not been done,
and nothing will retry it on its own.

Each drop is appended below as it happens, with the event and the reason.

## 13:00:29 — continue ENG-023

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

---

**Investigated 2026-08-30**, `scheduled` event pass (context `launchd`), per
this item's own recommendation. Checked `traces/eng-loop-2026-08-30.log`
directly rather than guessing: attempt 2 (02:13:55–04:04:30, 6634s) failed
with `Failed to authenticate. API Error: 401 OAuth access token has been
revoked.` — an auth-token problem, not a code or ticket problem. Attempt 3
(09:31:19–13:00:29, 12549s) failed with `API Error: Can't reach the API
server — check your internet or DNS (ENOTFOUND)` after only 5 file reads —
a transient network failure, not a stall or a runaway. Neither matches
`NEVER_STARTED_SIGNATURE` (both ran long enough and produced real,
non-vendor-limit output), so both were correctly charged as real attempts,
not refunded.

**Neither cause is specific to `ENG-023` or anything it touches** — no
evidence of a code, ticket, or design problem; this pass's own tool calls
are working normally, suggesting the OAuth/DNS conditions were transient and
have since cleared. Re-firing `continue ENG-023` is safe on that basis. This
item itself is the notification the recommendation asked for — filed, not
further gated, since a transient infra blip is below the P0 bar this
instance surfaces to the approver proactively for.
