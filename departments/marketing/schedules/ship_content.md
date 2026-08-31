# Schedule: ship_content

**Status:** 📋 PORTED — the routine this came from was implemented, verified
and running daily for months. Not wired here; the instance binds the
scheduler.

**Description:** Publish at most **one** approved piece per publishing day on
the channel that uses the **API publishing seam**, choosing the single oldest
approved piece that is due. Never a burst, never out of order.

**Agent:** none, directly. `agents/campaign-strategist/agent.md` owns
*oversight* — it reads this routine's output and trace for backlog, skipped
days and errors, and folds anything worth knowing into the channel report. It
does not invoke the routine, and the routine does not report to it.

**Skill(s):** `skills/ship-content/SKILL.md`

**One ship routine per channel.** The file name carries the channel:
`ship_content_{channel}`, with the unsuffixed name belonging to the channel
the department was first built around. Adding a channel that publishes adds a
routine file here and a registry entry in `config/config.yaml` — it does not
add an agent, and the routines never touch each other's queue, because each
filters on the piece's `channel` field.

**Trigger:** the clock, **daily**. The skill decides whether today is a
publishing day for this channel by reading `config/channels/{channel}.md` and
`config/config.yaml` → `channels.{channel}` — never from a hardcoded day list
and never from the scheduler.

**Capability required:** something that can start an unattended CLI session
once a day, and an environment holding the channel's API credential. Headless
is fine — that is the whole advantage of this seam. On an always-on host,
cron; on a machine that sleeps, a wake-aware calendar scheduler.

*This instance's binding, as an example:* daily at 08:00 local, on an
always-on container, publishing weekdays only.

**Suppressed on `MODE` = sabbath / retreat / quiet:** yes. Checked inside the
run before the queue is touched.

**Blocked by `MKT_PUBLISH_FREEZE`:** **yes.** This is the routine the freeze
exists for. Approved pieces stay in `content/approved/` and drain oldest-first,
one per publishing day, when it lifts — never as a burst on the first day
back.

---

## What it does

1. **Mode and freeze check.** Halt value in `MODE`, or any non-empty
   `MKT_PUBLISH_FREEZE` → log one line and exit before reading the queue.

2. **Is today a publishing day for this channel?** Compute the weekday
   **fresh** from the system date; compare against the channel's configured
   publishing days. Not a publishing day → log `non_publishing_day` and stop.
   That is the expected outcome on most days for most cadences and is not a
   problem to report.

3. **Has anything already published on this channel today?** The guard is the
   **calendar day, not the run** — a second invocation from a manual trigger,
   a retry, or an overlapping scheduler must not publish again. Check
   `content/shipped/` for a piece on this channel with today's publish date.
   Found one → log `already_shipped_today` and stop, regardless of how many
   other pieces are approved.

4. **Select exactly one piece.** Of all pieces with `channel:` matching this
   routine's channel, `status: approved`, and a filename date of today or
   earlier: take **the single oldest**. Log the rest as `deferred_backlog` with
   their filenames so the next day's run picks up the next-oldest.

   **Never skip ahead in the queue, and never publish more than one per day.**
   Both halves come from a real incident: on 2026-07-16 a backlog of three
   approved pieces went out in a single run, and the approver had to delete two
   from the platform by hand and keep one. A backlog is not permission to catch
   up — it is a queue to resume from where it broke off.

5. **Revalidate the format limits.** Against the live file, now, not against
   the check the writer ran hours ago on a version since edited. Over the
   channel's hard limit → publish nothing, log the reason, leave the piece at
   `status: approved` for a human to shorten.

6. **Check asset readiness.** Every image, carousel or document the piece
   references must exist on disk. Missing → do not publish. A text-only
   version of a piece designed around its visual is a silent quality failure,
   and the file is either there or it isn't.

7. **Publish** through the channel's API integration, with the credential read
   from the environment. The department never holds a credential and never
   writes one into a file, in the template or the instance.

8. **Verify by reading the result back** — never by the absence of an error.
   Record how strongly the publish was verified. Where read-back is genuinely
   impossible for this channel, the playbook says so and says what is checked
   instead, and the publish is recorded as **unverified** rather than as
   verified-by-silence.

9. **Update state.** Move the piece to `content/shipped/` with its publish
   timestamp and any returned identifier. Append it to
   `voice/samples/{register}.md` — a published piece is by definition a piece
   in the business's voice, and this is how an empty corpus becomes a
   calibrated one. Record `used_in` on any proof entry the piece drew from.

10. **Log the run.** One trace line whichever way it went, including the quiet
    outcomes. `non_publishing_day` and `already_shipped_today` are results, not
    silence.

## The approval gate — never bypass, never re-ask

`status: approved` in the piece's frontmatter is the **only** publish trigger.
It is set by the approver's explicit action and by nothing else.

Equally: **do not ask again.** This routine runs unattended and nobody is
present to answer. A run has exactly two valid outcomes — it publishes, or it
stops and logs a **named** reason. There is no third outcome where it asks a
question and waits, because that outcome looks identical to a piece that
silently never shipped.

## What it never does

- Publish more than one piece per channel per calendar day.
- Publish out of order to clear a backlog faster.
- Publish on a day the channel's config does not list.
- Publish while `MKT_PUBLISH_FREEZE` is set, or under a halt mode.
- Set `status: approved` on anything, for any reason.
- Delete a published piece — not to fix a duplicate, not to fix a typo. That
  is the approver's call and the approver's hands.
- Touch another channel's queue. Each ship routine filters on the piece's
  `channel` field and the queues never overlap.

## When it cannot run

| Failure | What happens | How you find out |
|---|---|---|
| Halt mode or publish freeze | Exits at step 1 | One log line. Approved pieces queue and drain oldest-first afterwards |
| Not a publishing day | Exits at step 2 | `non_publishing_day` in the trace — the common case, not an error |
| Already published today | Exits at step 3 | `already_shipped_today`. The cap held; nothing is wrong |
| Nothing approved and due | Publishes nothing | An empty queue is a normal outcome, and usually means M2 is where the work is sitting |
| Credential missing or rejected | Publishes nothing, piece untouched at `status: approved` | Named error in the trace; the next run retries cleanly with no residue |
| Over the format limit | Publishes nothing | Named error. Needs a human edit — the routine will not truncate a piece to fit |
| Asset missing on disk | Publishes nothing | Named error. Re-render, or drop the asset reference |
| Publish call fails ambiguously | **Do not retry in the same run.** Verify by reading the platform back first | A second attempt after a slow-but-successful publish posts twice, and duplicates on a public timeline are the approver's to clean up |
| Host down at the slot | The day's publish does not happen | The queue simply advances a day later. Cadence guards mean nothing catches up in a burst |

Every failure above leaves the piece exactly as it was, at `status: approved`,
with nothing half-done. That is deliberate: the next run should retry from
scratch with no residue, which is only true if a failed run wrote nothing.

## Notes

Ported 2026-08-29. The original fired weekdays-only from the scheduler **and**
checked the day inside the skill, belt-and-braces, after the day rule was set
by the approver's own preference. The template keeps the check in the skill and
fires **daily**, for the reason set out in `schedules/ship_content_x.md`:
cadence becomes a config value rather than scheduler configuration, so changing
it is a one-line edit with nothing to reconfigure. A scheduler that also
enforces the days is not wrong, just redundant — and redundant enforcement in
two places is how the two eventually disagree.
