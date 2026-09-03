---
type: eng-decision
agent: eng-manager
gate: incident
project: aiorders
ticket: unknown
recommendation: check whether a session can start on this host at all
raised: 2026-09-02
---

# Engineering loop is stalled — no session has started

Nothing has been dropped and nothing has halted. Every event is still queued in
`/c/Users/jerryai/Documents/GitHub/business-os/instances/aiorders/engineering/traces/.pending` and will run the moment a session starts. What has stopped is the
launching: repeated fires have ended without a claude session ever running, so
the back-off has grown to its ceiling of 60 minutes and stopped growing.

Two shapes of cause, and they need different answers:

- **A vendor limit that self-heals** — a monthly spend limit or a usage ceiling.
  Nothing to do; the next fire after the window runs, and this item can be closed.
- **A host condition that does not** — chiefly `claude not on PATH`, which is
  the case this notice exists for. Nothing on the never-started path escalates on
  its own: no hop is charged, no attempt is spent, nothing is dropped. Without
  this item the loop would stay silent indefinitely.

Check `traces/eng-loop-2026-09-02.log` for the `pass NEVER STARTED`
lines — the exit status and the vendor text on each say which of the two it is.

Each stall is appended below as it is detected.

## 05:10:59 — after 5 consecutive never-started passes

The last 5 launches ended without a session starting. Latest exit **1**, event `decision 2026-08-31-eng008-merge-request.md`, still queued at attempt 1. Launches are now suppressed for 3600s at a time until one starts.

## 12:15:59 — after 5 consecutive never-started passes

The last 5 launches ended without a session starting. Latest exit **1**, event `decision 2026-08-30-eng007-continue-sequence-question.md`, still queued at attempt 1. Launches are now suppressed for 3600s at a time until one starts.
