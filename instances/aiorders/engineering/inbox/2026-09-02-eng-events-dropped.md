---
type: eng-decision
agent: eng-manager
gate: incident
project: aiorders
ticket: unknown
recommendation: find out why passes are failing before re-firing anything
raised: 2026-09-02
decision: rejected
decided: 2026-09-03T02:18:12.195875+00:00
---

# Engineering events were dropped today

The loop has NOT halted — every other ticket is still moving. What happened is
narrower and worse than a halt: one or more events were accepted, could not be
processed, and have been discarded. Whatever triggered them has not been done,
and nothing will retry it on its own.

Each drop is appended below as it happens, with the event and the reason.

## 01:15:54 — decision 2026-09-01-eng-gate-violation-watch.md

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 124

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 03:32:38 — decision 2026-08-31-eng-events-dropped.md

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 10:37:41 — decision 2026-08-31-eng008-merge-request.md

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 16:30:53 — decision 2026-08-30-eng007-continue-sequence-question.md

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 124

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## Decision

**rejected** — 2026-09-03T02:18:12.195875+00:00

## 19:45:51 — decision 2026-08-30-eng-loop-halted.md

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 124

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.
