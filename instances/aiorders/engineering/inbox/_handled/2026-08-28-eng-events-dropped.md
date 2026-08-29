---
type: eng-decision
agent: eng-manager
gate: incident
project: aiorders
ticket: unknown
recommendation: find out why passes are failing before re-firing anything
raised: 2026-08-28
decision: approved
decided: 2026-08-29T08:27:47.038600+00:00
---

# Engineering events were dropped today

The loop has NOT halted — every other ticket is still moving. What happened is
narrower and worse than a halt: one or more events were accepted, could not be
processed, and have been discarded. Whatever triggered them has not been done,
and nothing will retry it on its own.

Each drop is appended below as it happens, with the event and the reason.

## 10:42:17 — watch launchd

A build-loop pass failed on this event twice — once on each attempt — so the event has been dropped rather than retried forever.

**Last exit status:** 1

Whatever triggered it has NOT been processed. The usual causes do not clear on their own: the automation account at its monthly spend limit, or a TCC/EPERM denial on the Mac. Check `traces/` for this pass's log.

Raised by ENG-005's event-lifecycle guard. Before it existed, this event would have been consumed silently by the pass that died and the board would have looked like a quiet night.

## Decision

**approved** — 2026-08-29T08:27:47.038600+00:00

recheck the request and report back how to fix. fix if you can

---

## Investigation (2026-08-29, `watch` event pass, context `schtasks`)

**Rechecked, and here is the honest limit of what "rechecked" can mean from
here.** This instance now runs on two hosts — the Mac that raised this
incident at 10:42:17 that morning, and this Windows machine (the port landed
that same night, `168cb89`, 23:34:44). `traces/` is `.gitignore`d at the repo
root (`instances/*/engineering/traces/`) — deliberately host-local scratch
state, never committed, never synced between the two. This Windows
checkout's own `traces/eng-loop-2026-08-28.log` starts at 23:33:59, the
Windows port's first fire; nothing from that morning exists here, and
structurally never will. **The actual pass output for the 10:42:17 failure —
the one piece of evidence that would settle this — is sitting on the Mac's
own disk and is not reachable from this session.** Reading harder in this
checkout will not find it; it isn't here.

**Best available reasoning, short of that evidence.** This incident's own
text names two candidate causes: the automation account's monthly spend
limit, or a TCC/EPERM permission denial on the Mac. `observations.md`'s
2026-08-28 entries record two *other* spend-limit deaths that same day —
08:35 (mid-edit on `ENG-006`'s PRD) and 21:33 (mid-`ENG-007` intake) — and
both "retried cleanly on the next fire." This incident is different in
exactly one respect: it failed **both** of its two allowed attempts, back to
back, and was dropped rather than recovering. A vendor-side spend limit that
cleared twice that same day on retry doesn't fit a failure that held across
two consecutive automated attempts; a TCC/EPERM denial does — macOS doesn't
grant that permission back between two scripted retries seconds apart, only
a human does, in System Settings. Reasoned from the day's other two data
points, not confirmed from this failure's own log, which is unavailable here.

**What a human at the Mac can check to actually confirm it:** System
Settings → Privacy & Security → check whether the terminal/automation
process that runs this loop has Full Disk Access (or whichever permission
the failing operation needed). Separately, the vendor account's own
usage/billing dashboard for 2026-08-28 ~10:40 local would rule the spend
limit in or out directly. Neither is reachable from this session.

**Fix — the part actually within reach from here.** The root cause isn't
fixable remotely, but the reason it's *undiagnosable* remotely is: this
department's failure diagnostics live only in the host-local `traces/` that
raised them. A dropped event's own inbox item — the thing that travels, the
thing any future host or session actually reads — names `traces/` by
pointer ("Check `traces/` for this pass's log") rather than carrying any of
the failure itself. That's fine on one host; it's a dead end the moment a
second host is in the picture, which is now permanent for this instance.
Filed as a proposal (`agents/eng-manager/proposals.md`, 2026-08-29 row) to
have the drop path that writes this style of item also embed a short,
git-independent excerpt of the failure — last few lines of the pass's own
output, and the classified cause if `lib/eng-trigger.sh` determined one —
directly in the item text. Not fixed inline: it touches
`lib/eng-trigger.sh`'s core failure-handling path, the same bar prior
proposals against that file have held to (approver sign-off before a
hand-edit changes it).

---

**Processed 2026-08-29 (`watch` event pass, context `schtasks`).** Found
during this event's own three-inbox sweep — the answer arrived by hand-edit
to this file directly, not through `lib/eng-notify.sh`'s reply path (mode
check and gate-check both ran clean before touching anything). `ticket:
unknown` — this is an incident report, not a ticket gate, so nothing on the
board moved; the investigation above and the proposal it filed are the
complete response to "recheck the request and report back how to fix. fix if
you can." Journaled in `agents/eng-manager/config/decision-journal.md`.

---

**Re-checked 2026-08-29 (`decision` event pass, context this file).** This
event's own queued line (`decision 2026-08-28-eng-events-dropped.md` in
`traces/.pending`) was appended behind the `watch schtasks` line above, so by
the time it reached the front and this pass launched, the `watch` pass had
already done the complete job — investigation, the `proposals.md` row, and
the decision-journal entry all already on disk. Mirror image of `ENG-007`'s
G2 (`decision-journal.md`, 2026-08-29 row): there the dedicated `decision`
event drained first and a trailing `watch` found nothing left; here it's the
other way around. Mode check clean (`MODE=` empty); pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.
Re-read this file end to end and confirmed no content past the "Processed"
footer above, and `proposals.md` / `decision-journal.md` both already carry
their 2026-08-29 rows for this incident — nothing left to do.

`chained: none` — `ticket: unknown`; this is an incident report, not a
ticket, so there is nothing in an agent-owned state to fire a next hop for.
Full reasoning in `agents/eng-manager/observations.md`, 2026-08-29 (last
row).
