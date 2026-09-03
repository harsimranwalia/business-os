---
type: eng-decision
agent: eng-manager
gate: incident
project: aiorders
ticket: ENG-024
recommendation: check whether a session can start on this host at all
raised: 2026-09-03
---

# Engineering loop is stalled — no session has started

Nothing has been dropped and nothing has halted. Every event is still queued in
`/Users/hwalia/Documents/projects/personal/business-os/instances/aiorders/engineering/traces/.pending` and will run the moment a session starts. What has stopped is the
launching: repeated fires have ended without a claude session ever running, so
the back-off has grown to its ceiling of 60 minutes and stopped growing.

Two shapes of cause, and they need different answers:

- **A vendor limit that self-heals** — a monthly spend limit or a usage ceiling.
  Nothing to do; the next fire after the window runs, and this item can be closed.
- **A host condition that does not** — chiefly `claude not on PATH`, which is
  the case this notice exists for. Nothing on the never-started path escalates on
  its own: no hop is charged, no attempt is spent, nothing is dropped. Without
  this item the loop would stay silent indefinitely.

Check `traces/eng-loop-2026-09-03.log` for the `pass NEVER STARTED`
lines — the exit status and the vendor text on each say which of the two it is.

Each stall is appended below as it is detected.

## 06:37:12 — after 5 consecutive never-started passes

The last 5 launches ended without a session starting. Latest exit **1**, event `continue ENG-024`, still queued at attempt 2. Launches are now suppressed for 3600s at a time until one starts.

## Investigated 2026-09-03 (`continue ENG-024` event pass, 17:55 UTC)

**Classification confirmed directly from this same host's own log — no
cross-host inference needed, unlike the 2026-09-02 precedent below.**
`traces/eng-loop-2026-09-03.log`: every `pass NEVER STARTED` line in this
stall's own run (05:21:40 through 06:37:12, six in a row) carries the
explicit text `vendor limit signature` — the self-healing shape this
notice's own text distinguishes from the `claude not on PATH` host-condition
shape. Confirmed the limit actually cleared, not just inferred from later
silence: the same log records `08:56:01 back-off cleared — a session
started normally after 6 never-started pass(es) and 35 suppressed fire(s)`,
immediately followed by a real 1111s `continue ENG-024` pass completing
`exit 0`.

**Sustained normal operation since, not one lucky launch.** The same log
shows eleven further passes completing `exit 0` after that recovery and
before this one — `decision` passes for `ENG-013`, `ENG-016`, `ENG-026`,
`ENG-019`, `ENG-020`, `ENG-021`, one more brief separate vendor-limit blip
at 10:19–10:34 (2 failures, self-cleared the same way, below this notice's
own 5-failure threshold so it never raised a second entry here), and
multiple `continue ENG-024` passes since, including the one immediately
preceding this one (`principal-engineer`'s fast-lane review, `building →
ready-to-ship`). The loop has been working continuously for over eleven
hours since this stall cleared.

**Conclusion: resolved.** Vendor limit, self-healed, confirmed by direct
same-host log evidence rather than absence-of-further-entries alone.

## Decision

No `decision:` field — self-raised informational notice, not an
approver-facing gate, same established precedent as
`inbox/_handled/2026-09-02-eng-loop-stalled.md`. Closed by this
investigation alone.
