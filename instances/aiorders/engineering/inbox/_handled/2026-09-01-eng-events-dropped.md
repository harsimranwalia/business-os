---
type: eng-decision
agent: eng-manager
gate: incident
project: aiorders
ticket: unknown
recommendation: find out why passes are failing before re-firing anything
raised: 2026-09-01
decision: approved
decided: 2026-09-01T16:23:42.685518+00:00
---

# Engineering events were dropped today

The loop has NOT halted — every other ticket is still moving. What happened is
narrower and worse than a halt: one or more events were accepted, could not be
processed, and have been discarded. Whatever triggered them has not been done,
and nothing will retry it on its own.

Each drop is appended below as it happens, with the event and the reason.

## 00:05:55 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 00:20:56 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 00:35:58 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 00:50:58 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 01:05:57 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 01:20:57 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 01:35:59 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 01:51:00 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 02:05:58 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 02:20:59 — scheduled schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 02:35:57 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 02:50:58 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 03:05:58 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 03:20:58 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 03:35:57 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 03:50:58 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 04:05:57 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 04:20:58 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 04:35:57 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 04:50:57 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 05:05:57 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 05:20:56 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 05:35:57 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 05:50:57 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 06:05:57 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 06:20:56 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 06:35:58 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 06:50:57 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 07:00:10 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 07:15:54 — intake instances\aiorders\engineering\agents\product-manager\inbox\2026-09-01-eng-011-on-the-brand-portal-i-want-option-to-make-the-restau.md

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 07:30:56 — decision 2026-08-29-eng017-g1-scope.md

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 07:45:58 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 09:00:54 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 124

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## Decision

**approved** — 2026-09-01T16:23:42.685518+00:00

---

**Investigated 2026-09-01**, `scheduled` event pass (context `launchd`), per
this item's own recommendation. **Cannot check the Windows host's own
`traces/`** — it's `.gitignore`d and host-local, so nothing about *why*
each attempt returned exit 1 is reachable from this Mac; this is the exact
diagnosability gap `proposals.md` (2026-08-29 row) already names, reproduced
live rather than theoretical. What **is** verifiable from here, from tracked
git history alone:

- **The outage window is bounded and already over.** 29 consecutive
  `watch schtasks` (plus one `intake` and one `decision`) fires failed with
  exit 1 from `00:05:55` through `07:45:58` — just under 7.5 hours, every
  ~15 minutes, every one a real attempt (not `NEVER_STARTED_SIGNATURE` —
  each ran long enough to be charged, per `ENG-016`'s classifier). One final
  fire at `09:00:54` returned exit **124** (a timeout, not the same
  signature) — the last drop before recovery.
- **Recovery is confirmed, not assumed**: this same host (`businesspilotcare-gif`
  identity) successfully produced and pushed two real commits shortly after —
  `e281c71` (09:17:43 local, the 26-file board reconciliation merge) and
  `e3d89f5` (09:28:29 local, this exact incident item's own last update).
  Whatever was wrong cleared on its own sometime in the `07:45`–`09:17`
  window, consistent with the transient, self-clearing causes this
  boilerplate names (spend limit, auth/DNS) rather than a standing
  environment break — matching the 2026-08-30 occurrence's own diagnosis,
  not a new failure mode.
- **Both concrete drops this file names are already recovered, by hand, in
  this same pass** — not left for a future retry: the dropped `intake`
  (the brand-portal/FoodSwipe request) was shaped into `ENG-026`, held at
  `intake` on one open question; the dropped `decision`
  (`2026-08-29-eng017-g1-scope.md`) was fully processed — journaled,
  `ENG-017` advanced to `designed`. Re-firing either event would now be a
  no-op against work already done.

**No further re-firing needed or attempted** — everything this incident
actually blocked has been recovered above, and root-causing the exit-1
streak further requires the Windows host's own log, which is out of reach
from this session. If this recurs, worth revisiting the diagnosability
proposal (embed the failure excerpt in the item itself rather than a
`traces/` pointer) so a Mac-side pass isn't dead-ended on a Windows-side
failure a second time.

If the monhtly limit is hit, then do not retry tasks rather check that the limit is reset then only it makes sense to retry tasks instead of just retying tasks for no reason

## 12:15:55 — watch schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 124

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 15:30:53 — decision 2026-09-01-eng-events-dropped.md

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 124

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.
