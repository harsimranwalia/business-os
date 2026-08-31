# Schedule: mkt_weekly_plan

**Status:** 📋 PORTED — designed and proven in the system it came from, not
wired here. The instance binds the scheduler; nothing in `$MKT_DEPT` installs
a job.

**Description:** The department's engine. One run a week takes the business
from "what should we publish" to reviewed drafts sitting on the approval
surface, and closes with the unified weekly report.

**Agents:** `agents/cmo/agent.md` (entry) → `agents/campaign-strategist/agent.md`
(execution) → `agents/content-writer/agent.md` (craft, per piece)

**Skill(s):** `skills/topic-miner/SKILL.md` → `skills/content-writer/SKILL.md`
(or the channel's own writer skill, e.g. `skills/x-content-writer/SKILL.md`) →
`skills/content-reviewer/SKILL.md`, plus `skills/engagement-analyzer/SKILL.md`
for the performance read that opens the run.

There is no separate critique skill in the chain, and the omission is
deliberate rather than a gap. The writer skills run their own critique as
Pass 2, against the same voice guide and anti-patterns a standalone critic
would read. Extracting it would give the pipeline two places to keep the
craft criteria in sync, and the failure mode of that is silent: the two
drift, and the draft passes the one that got stale.

**Trigger:** the clock. Two fires, one routine:

| Fire | When | Purpose |
|---|---|---|
| primary | the instance's planning slot, weekly | The week's plan |
| catch-up | the same time, the next day | Backstop. Runs the same routine; the agent decides whether the primary actually completed |

**Capability required:** something that can start an unattended CLI session on
a weekly cadence and again a day later. On an always-on host, cron. On a
machine that sleeps, prefer a wake-aware calendar scheduler — plain cron
silently drops anything scheduled while the machine was asleep, and a silently
dropped planning run is a week with no content queued.

*This instance's binding, as an example:* the port ran the primary Sunday 19:00
local and the catch-up Monday 19:00, on an always-on container via cron.
Sunday evening because it puts the week's plan in place before the week starts
and folds into an existing Sunday reporting cadence rather than adding a new
touchpoint — the approver reads one evening's worth of reports, not seven.

**Suppressed on `MODE` = sabbath / retreat / quiet:** yes. Checked inside the
run, at the top, never by the scheduler. The scheduler keeps firing; the run
logs one line and exits.

**Blocked by `MKT_PUBLISH_FREEZE`:** no. A freeze stops publishing, not
planning. Drafting, review and M2 all continue, and approved pieces queue.

---

## What it does

Each run, in order:

1. **Mode check.** `.env` → `MODE`. On a halt value, log one line and exit.
   Nothing below runs, including the report.

2. **Did the primary already complete?** Only meaningful on the catch-up fire,
   but harmless on both, so it runs on both.

   Compute the primary run's date **fresh** — never from a stored weekday
   label — then look in **both** `content/drafts/` and `content/shipped/` for
   pieces carrying that date in their filename. Both directories, because a
   ship routine *moves* a piece out of `drafts/` when it publishes: on a
   one-piece week the lone draft can publish before the catch-up fires, and
   checking `drafts/` alone would report a failure that did not happen and run
   the whole week twice.

   Drafts are the completion marker specifically because they are produced
   **deep** in the chain. The topic candidates file is written by the first
   skill, so its presence proves only that the run started — which is exactly
   the partial failure this backstop exists to catch.

   Complete → log one line and exit. Incomplete → this run *is* this week's
   plan; execute the full chain below for whichever channels are short.

3. **Read the ground.** The CMO reads `../knowledge/business-profile.md`
   fresh, last week's `performance/` and baselines, each channel's playbook in
   `config/channels/`, and the agents' notebooks. A CMO that cannot say what
   the business does cannot say what is worth publishing, and will approve
   anything that sounds professional.

4. **Drain the requests.** `inbox/requests/` — topics filed by a filer since
   the last run. They enter the topic bank like any other candidate and get no
   priority for having been filed by a human; a filer files topics, not
   instructions.

5. **Write the allocation brief** — the week's plan file,
   `plan-{YYYY}-W{WW}.md`. How many pieces, any emphasis, any trades,
   and the current narrative arc in one line. The default when nothing demands
   otherwise is each channel's own default mix. **Do not fill the calendar
   because it is planning day** — the question is where the week's limited
   content capacity is highest-leverage, and the honest answer is sometimes
   "fewer than last week."

6. **Split it across channels.** The campaign strategist decides, per live
   channel, how many pieces, which archetype or format each gets, and whether
   any piece is a repurpose of another channel's beat rather than a fresh
   topic. Channels at C0 get nothing. Channels at C1 get drafts only if they
   have a live reason to be at C1 at all.

7. **Brief each piece.** `{channel, archetype/format, source_material,
   register, include_cta, notes}` — every field. **The brief-completeness gate
   is here**, and it is the cheapest gate in the department: a writer that has
   to guess the register produces something plausible and wrong, and the cost
   of that lands at M2 on the approver's attention.

8. **Draft, critique, render, review.** The content writer dispatches on the
   brief's `channel`, drafts, runs the critique pass, generates the image or
   carousel **in the same run** (never queued separately — a piece whose asset
   arrives later is a piece that publishes without it), then runs the review
   loop: **max two rounds.** After round two, unresolved concerns are attached
   to the draft and it is returned anyway, visibly. Never a third round, never
   a suppressed flag to make a draft look cleaner than it is.

9. **Land the drafts.** `content/drafts/` → `content/ready-to-send/` with
   `status: draft` and the review verdict in frontmatter. **That is the
   approval surface.** No second inbox is created for content, on any channel,
   ever. The run does not notify per piece — pieces are read on the surface,
   in a batch, when the approver chooses.

10. **Close the loop.** The campaign strategist writes a short section per
    active channel — what shipped, what the numbers say, what it would change.
    The CMO folds them into one report at `reports/marketing-{YYYY}-W{WW}.md`,
    300–500 words, and that report is what next week's allocation brief reads.
    Terminal by design: the approver reads it or doesn't.

11. **Raise anything that needs M1 or M3** — as an inbox item, with the cost
    named in the approver's hours, via `lib/mkt-notify.sh`. Most weeks this
    produces nothing, and nothing is the correct outcome.

## What it never does

- **Notify per piece.** Drafts appear on the surface; the surface is read when
  the approver reads it. A department that pings on every draft has recreated
  the job it replaced.
- **Set `status: approved`.** Not for a piece it is confident about, not for a
  piece that has been sitting for a week. Only the approver's explicit action
  sets it.
- **Skip the review loop** under time pressure, for a "quick" piece, or
  because the draft looks fine. Two rounds, always, before the approver sees
  it.
- **Run a second full batch when the primary succeeded.** A blind catch-up
  rerun doubles the week's pipeline, which was considered and rejected: the
  completion check exists precisely so the backstop can be silent when it has
  nothing to do.
- **Fill the calendar to hit a number.** The allocation is a ceiling, not a
  quota.

## When it cannot run

| Failure | What happens | How you find out |
|---|---|---|
| Halt mode set | Exits at step 1, silently, by design | One log line. Clearing `MODE` resumes with nothing to reinstall |
| Machine asleep / host down at the primary slot | Nothing runs | The catch-up fire the next day finds no drafts and runs the full chain |
| Crash partway through the chain | Partial output — some pieces drafted, some not | The catch-up's drafts check sees the shortfall per channel and drafts only what is missing |
| **Both fires miss** | **A week with no content queued** | Nothing inside this department notices. This is the routine's real failure mode and it is unmonitored — see below |
| Voice corpus below the floor | Drafting still happens; the gap is recorded on the draft | The draft says so, and M2 carries more weight that week |
| A channel's playbook missing | That channel is skipped, with a line in the report | The weekly report's channel section is absent for it |

**The unmonitored case is the last one, and it is named rather than hidden.**
Two consecutive silent misses produce a quiet week that looks exactly like a
week where the CMO decided to publish nothing — which is a legitimate outcome
this department deliberately allows. Distinguishing them needs something
outside this routine watching for the absence of a report, and that does not
exist here yet. In the meantime the honest mitigation is that the ship
routines drain any existing approved backlog regardless, so a missed planning
week degrades gradually rather than stopping publishing dead.

## Notes

Ported 2026-08-29 from a system where this was two schedule files — a primary
and a separately-documented catch-up. They are one file here because they are
one routine with two fires and identical behaviour; the only difference is
that on the second fire step 2 usually exits. Two files meant two descriptions
of one chain, and the second had already started to drift.

**The catch-up carries no logic of its own, and this is load-bearing.** An
earlier version of the original embedded the did-it-complete check
step-by-step in the scheduler's prompt and was rejected: a real employee who
missed planning checks and catches up without being told how. The check lives
with the agent. **Do not move it back into the prompt** — a scheduler fires
things on a timer, agents decide what to do about it, and every rule that
leaks into a scheduler prompt is a rule that has to be re-pasted somewhere to
change.
