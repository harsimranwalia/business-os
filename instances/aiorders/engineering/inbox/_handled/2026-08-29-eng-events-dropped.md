---
type: eng-decision
agent: eng-manager
gate: incident
project: aiorders
ticket: unknown
recommendation: find out why passes are failing before re-firing anything
raised: 2026-08-29
decision: rejected
decided: 2026-08-29T15:52:51.834010+00:00
---

# Engineering events were dropped today

The loop has NOT halted — every other ticket is still moving. What happened is
narrower and worse than a halt: one or more events were accepted, could not be
processed, and have been discarded. Whatever triggered them has not been done,
and nothing will retry it on its own.

Each drop is appended below as it happens, with the event and the reason.

## 08:40:57 — scheduled schtasks

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 3

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## Decision

**rejected** — 2026-08-29T15:52:51.834010+00:00

---

**Processed 2026-08-29**, `watch` event pass (context `schtasks`) — found
this answered since the last pass touched it. No verbatim comment
accompanied the rejection, so read plainly rather than over-interpreted:
the approver declined the recommendation to investigate this specific
dropped event (`08:40:57 scheduled schtasks`, exit status 3) further — not
a rejection of the drop/notify mechanism itself. No further investigation
of that specific drop undertaken here, per the decision. Separately, and
not as an effect of this decision: this same pass independently
investigated the *later*, department-wide daily-hop-ceiling halt
(`inbox/2026-08-29-eng-loop-halted.md`, processed below) and found a
plausible root cause for that one — a config-path bug in
`read_plan_budget()` silently pinning every instance to the `pro` tier's
40-hop ceiling regardless of the configured tier, fixed but uncommitted
before this pass started. Whether that same root cause also explains
*this* drop (exit status 3, 08:40:57 — hours before the tier fix landed) is
not established either way; left unopened per the approver's own decision
on this item. Journaled in `decision-journal.md`.
