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

## Investigated 2026-09-02 (`watch` event pass, context `launchd`, 22:00)

**Cannot check the Windows host directly** — this pass runs on the Mac, and
`traces/` is host-local and `.gitignore`d, the same limitation the
decision-journal's 2026-08-29 dropped-events entry named for an equivalent
cross-host question. No false confirmation offered.

**Indirect evidence is strong, not just "things look fine now."** This
file's own path (`/c/Users/jerryai/...`) identifies the Windows host as the
one that stalled, both episodes (05:10:59, 12:15:59) matching the documented
"pass NEVER STARTED" signature (no session launches at all, so nothing is
charged or dropped — the back-off just grows to its 60-minute ceiling and
sits there). `git log` shows that same host later committed real,
successful work well after both timestamps — most directly,
`469e5483f0b6e7f44da99111b53621b7ecc38f5a` ("fix decision-queue priority,
orphaned-chain detection, PRD checkpointing, and lock staleness", authored
`businesspilotcare-gif`, 2026-09-02T21:18:35-07:00), whose own message says
it was "found and fixed during a live debugging session on the Windows
host" and names the exact mechanism that produces a never-started pass: a
lock-owner PID that doesn't match any process in its own still-running
chain, so `acquire()`'s `kill -0` liveness check reports the lock free (or
stale) when it isn't reliable on that host — `STALE_LOCK_SECONDS` raised
from 1800 to 3900 (above `PASS_TIMEOUT_BASE_SECONDS`) as the fix. A launcher
that can never validate its own lock is exactly a launcher that can end
without ever starting a session, repeatedly, which is this notice's entire
symptom.

**Conclusion: resolved, not merely quiet.** Closing on the strength of a
named, plausible, already-fixed root cause rather than only the absence of
further stall entries — the distinction this department's own precedent
(the 2026-08-29 dropped-events journal entry) draws between "reasoned
hypothesis" and "confirmed." If a third stall entry appears after this fix's
timestamp, treat it as a new, separate incident rather than a reopening of
this one.

## Decision

No `decision:` field — self-raised informational notice, not an
approver-facing gate; the four/five `gate: incident` items on this board
have never carried one, per established precedent
(`decision-journal.md`'s incident rows only exist for the ones the approver
actively replied to). Closed by this investigation alone.
