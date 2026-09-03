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

## Investigated 2026-09-02 (`watch` event pass, context `launchd`, 22:00) — five named drops, four already accounted for, one arrived after the decision above

**The 19:45:51 entry landed on disk after `decision: rejected` was already
recorded (`decided: 2026-09-03T02:18:12Z`, ~19:18 local) — the exact
append-after-decision race `eng_build_loop.md` names as already-observed on
this same file's 2026-08-30 predecessor.** Read as: the approver's rejection
covers the four drops that existed when they answered (01:15:54, 03:32:38,
10:37:41, 16:30:53); it cannot cover a fifth entry written roughly 27
minutes later. Checked that fifth entry on its own rather than assuming the
rejection swallows it.

**All five named files re-checked directly, not trusted from this notice's
own account:**

| Dropped event | Current state |
|---|---|
| `2026-09-01-eng-gate-violation-watch.md` | Still loose in `inbox/`, `decision:` blank — correctly waiting on the approver, re-confirmed by tonight's own 20:30 `scheduled` sweep minutes before this pass |
| `2026-08-31-eng-events-dropped.md` | Still loose in `inbox/`, `decision:` blank — same, re-confirmed 20:30 |
| `2026-08-31-eng008-merge-request.md` | Still loose in `inbox/`, `decision:` blank — both PRs still open, correctly waiting on the approver's merge |
| `2026-08-30-eng007-continue-sequence-question.md` | Still loose in `inbox/`, `decision:` blank — correctly waiting, already nudged once |
| `2026-08-30-eng-loop-halted.md` (the late-arriving fifth) | **Already in `inbox/_handled/`** — fully investigated and closed independently of this drop notice (see that file's own footer) |

**Nothing was actually lost.** The event-dispatch failure this notice
reports is real (a `decision` fire failed twice and was discarded each
time), but every one of the five files it names has since been reached
anyway through the ordinary per-file frontmatter sweep every `watch`/
`scheduled` pass runs regardless of the event queue — four are exactly
where an unanswered gate should be, and the fifth was closed by a separate
pass entirely. This is the safety net the dual mechanism (event dispatch
*and* independent sweep) is designed to provide; it worked here.

**Approver's rejection read plainly, per this journal's own established
convention for a bare answer with no comment:** declines the recommendation
to "find out why passes are failing before re-firing anything" as its own
investigation task — not a claim that the drops didn't happen, and not
license to stop the general per-file sweep this pass just ran anyway. Root
causes for this class of failure are already well-documented elsewhere on
this board (monthly spend limits, TCC/EPERM on the Mac, and now the
Windows-host lock-staleness bug closed alongside this same pass's other
incident) — nothing further to chase for tonight's five specifically.
