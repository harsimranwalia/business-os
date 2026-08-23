# Schedule: eng_weekly_report

**Status:** 📋 DESIGNED — not yet cron-wired

**Description:** One engineering report a week — shipped, in flight, blocked, bugs, cost, and what needs the approver.

**Agent:** `agents/eng-manager/agent.md`

**Schedule (human):** weekly on sunday at 18:30

**Cron expression:** `30 18 * * 0`

**Suppressed on sabbath/retreat/quiet:** yes

---

## What it does

Reads the board, the bug ledger, the release records, and every department
notebook entry from the past week, then writes
`reports/engineering-{YYYY-WXX}.md`. Terminal for now — the approver reads it
there, or doesn't; rewires if business-os grows an aggregator that consumes it.

Sections, in this order:

1. **Shipped** — one line each, in plain language. What the approver got
   this week.
2. **In flight** — ticket, state, owner, and whether it's moving.
3. **Waiting on you** — every open G1/G2/G3 item, oldest first, with the
   recommendation restated. This section is the only one that asks anything
   of the approver.
3b. **Proposals — one batched G1** — the Open table of
   `agents/eng-manager/proposals.md`, every row, as a single decision: approve
   any subset, or none. Only an approved proposal becomes a ticket.

   **This is the department's only route to creating its own work**, and it was
   made so on 2026-08-13 because the previous route — agent findings shaping
   straight onto the board — had produced a board that was eleven-fifteenths the
   department's own machinery. Every ticket on it was individually defensible;
   the fan-out was structural. See `schedules/eng_build_loop.md` step 3.

   **Present them for skimming, not for study.** One line each, ordered by the
   consequence of not doing it, with the department's own recommendation stated —
   including "we would not start this one." A proposal the approver cannot
   decide in about ten seconds is written wrong, and the fix belongs in the
   proposal, not in this section.

   **Expire in the same pass.** Anything filed more than 30 days ago and still
   unapproved moves to the Expired table with one line here saying it went and
   what it was. Do not ask about it again, do not re-file it, and do not treat
   the expiry as a rejection worth appealing — if it mattered it will be
   re-noticed. Say "nothing expired" in one line when nothing did, and say "no
   open proposals" when the table is empty. An empty list being visibly empty is
   how this stays trustworthy.

   **Never nudged, never pinged, never escalated.** Silence on a proposal is
   silence, not a queue with the approver's name on it — this section is a
   menu, and a menu that chases you is not a menu.

   **How the approver answers it, because a section in a report they cannot
   reply to is a dead end.** When the Open table is non-empty, write **one**
   item to `inbox/` with `type: eng-decision`, `agent: eng-manager`, `gate:
   g1-proposals`, and `ticket: PROP-{YYYY-WXX}`, listing the rows numbered
   `P1`, `P2`, … `agent: eng-manager` because the EM raises this digest —
   the batched rows underneath it can span any project or origin agent, but
   `project:` names what the work is about, not who's asking, and
   `lib/tuner-harvest.py` groups repeated corrections by `agent:` alone; an
   item missing it lands `unattributed` and stops being actionable. Raise it
   with `lib/eng-notify.sh raise`, exactly once, on the same Sunday run. The
   approver answers on whichever channel the instance has configured
   (e.g. `approve PROP-2026-W33: P1, P3`) — `lib/eng-notify.sh` routes the
   reply back, bucket **G2** — which fires a pass immediately. The build
   loop's step 4 turns each approved row into a ticket.

   **This item does not count against the approval cap, and gets no 24h nudge.**
   Both are deliberate exceptions to how every other gate item is handled. The
   cap exists to stop finished work piling up on the approver — a proposal is
   not finished work, nothing is blocked behind it, and letting a weekly menu
   consume one of three approval slots every week would starve the gates that
   actually hold shipped code. The nudge is skipped for the same reason: there
   is nothing to chase. It appears once, it expires at 30 days, and that is
   the whole mechanism.

4. **Blocked** — anything blocked on an agent past 5 working days, framed as a
   decision: unblock it or kill it. (Tickets blocked on the approver appear
   in section 3 instead — they're waiting on the approver, not stuck.)

4b. **Oldest untouched backlog item** — one line, whenever the top of the backlog
   has sat unstarted for 60 days, and always naming the oldest tech-debt card if
   there is one. Debt has no natural forcing function: the architect files it, it
   sits behind whatever the approver asked for most recently, and it rots
   invisibly.
   One line a week is the whole mechanism — enough to be seen, not enough to nag.
5. **Bugs** — open by severity, anything past SLA, and anything that escaped to
   production with the test that should have existed.

4b. **Gate waivers** — **every row** in
   `agents/eng-manager/config/gate-waivers.md`, both sections, every week,
   regardless of age or how many times it has appeared before. Historical rows
   say plainly that they predate the check and nobody approved them; Granted rows
   name the ADR and what was overridden.

   **This section prints even when nothing changed, and it is deliberately not
   folded into §6b.** §6b suppresses anything appearing fewer than three times,
   which is right for patterns and exactly wrong here: a waiver is the
   department's only total exemption from a machine gate, and it has to be visible
   the *first* week it exists, not the third. If the ledger is empty, say
   "no waivers" in one line — an empty ledger being visibly empty is the point.

   Added 2026-08-12 to make `gate-waivers.md`'s own claim true. That file said
   "Every row here appears in the weekly report, so waivers cannot accumulate
   quietly" while **nothing outside the ledger read it** — a compensating control
   that existed only as a sentence about itself. Found by ENG-006's security gate
   (finding 2) and made a blocking condition on ENG-004's G3, because the ledger
   is what stands between "a gate was overridden" and "a gate was overridden and
   nobody ever heard about it."
6. **Cost** — recurring spend per project and any delta this week, plus the
   current plan tier and whether the department is bumping its hop budgets.
   Hitting the budgets is a signal to consider an upgrade, not a reason to
   ration — say which it looks like.
6b. **What the team noticed** — patterns only, from
   `agents/eng-manager/observations.md`. Three or more related observations, or
   one that recurs across projects. A single observation never appears here and
   never reaches the approver — the value of noticing is in the repetition.

   Prune the ledger in the same pass: anything over 90 days old with no pattern
   around it gets deleted. If it mattered, it would have recurred.

6c. **Exceptions** — only when the same kind has been granted three times, which
   means the process is wrong rather than the tickets unusual. One line, plus
   the intake card filed to fix it. Individual exceptions are the EM's business
   and don't belong in the approver's report.

7. **Speed** — four numbers, not prose:
   - median cycle time, and the state tickets sat in longest
   - **hours waiting on the approver vs. hours waiting on the machine** — the
     split matters more than the total, because the two have completely
     different fixes and conflating them wastes effort
   - first-pass gate rate (target 70%; below it, the brief is the problem)
   - rework rounds per ticket

   Never framed as a target missed. It's a diagnostic — it tells the
   approver which lever is worth pulling, or that none is.

8. **Health** — the honest paragraph: is this department taking work off the
   approver's plate or adding to it? Gates that fired late, handoffs that
   dropped something, anything the team learned. If the answer this week is
   "adding", say so plainly — that's the most valuable line in the report.

## Why 18:30 Sunday

Thirty minutes before the Marketing weekly run at 19:00, inside the existing
Sunday cadence rather than adding a new touchpoint to the approver's week.
The approver reads one evening's worth of reports, not seven.

## What it never does

- Manufacture urgency. Severity has a definition; the report uses it.
- Ask for anything that isn't a real decision.
- Report activity as progress. Ten tickets moved and nothing shipped is a bad
  week, and the report says so.
- Interrupt. If something genuinely couldn't wait, it already reached the
  approver as a P0 and this report just records it.

## Notes

Built 2026-07-27 with the engineering department. Not yet cron-wired.

The report is terminal by design: the approver reads it or doesn't. An
aggregator may pull a single line from it into a daily brief later, if the
instance grows one that consumes it. Silence is a valid line — a quiet
engineering week doesn't need announcing.
