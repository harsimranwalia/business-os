---
type: eng-decision
agent: eng-manager
gate: incident
project: aiorders
ticket: unknown
recommendation: find out why passes are failing before re-firing anything
raised: 2026-09-01
decision: rejected
decided: 2026-09-03T02:18:09.271126+00:00
---

# Engineering events were dropped today

The loop has NOT halted — every other ticket is still moving. What happened is
narrower and worse than a halt: one or more events were accepted, could not be
processed, and have been discarded. Whatever triggered them has not been done,
and nothing will retry it on its own.

Each drop is appended below as it happens, with the event and the reason.

## 18:45:54 — scheduled schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 124

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## 22:00:54 — decision 2026-08-30-eng-events-dropped.md

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 124

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## Decision

**rejected** — 2026-09-03T02:18:09.271126+00:00

**Investigated 2026-09-02** (`watch` event pass, context `launchd`, ~22:35)
— decided 3 seconds before this same date's `2026-09-02-eng-events-dropped.md`
rejection, part of the same batch. Two entries: a routine `scheduled` poll
drop (self-healing, nothing unique lost), and a dropped notification for
`decision 2026-08-30-eng-events-dropped.md` — moot now regardless of that
notification's own fate, since this same pass independently found and
fully processed `2026-08-30-eng-events-dropped.md` itself earlier tonight
(the ordinary per-file sweep catching what the failed notification
couldn't). Nothing lost. Rejection read the same as this evening's other
two: declines further investigation into an already-fixed failure class.

**Filename note, added correcting an in-session mistake:** this file
shares its base name (`2026-09-01-eng-events-dropped.md`) with an earlier,
wholly separate incident report from the same calendar date (raised
`00:05:55`, decided `2026-09-01T16:23:42Z` **approved**, already properly
closed in `inbox/_handled/2026-09-01-eng-events-dropped.md`) — the
date-based naming convention collided because two distinct events-dropped
incidents both landed on 2026-09-01. This pass's own `mv` briefly
overwrote that earlier, already-closed file with this one; caught
immediately via an unexpected `git status` " M" (modified-tracked) instead
of the expected "??" (new) on the destination path, and fixed by
restoring the original from `git show HEAD:...` and giving this one the
`-b` suffix instead. Filed as an observation
(`agents/eng-manager/observations.md`) rather than a proposal — a real
near-miss, but this pass's own recovery is the fix for this occurrence;
whether the naming convention itself needs a counter or timestamp suffix
to prevent a next collision is a judgment call for whoever reviews the
pattern, not urgent enough to block on.
