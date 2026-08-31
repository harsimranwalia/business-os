# Schedule: ship_content_x

**Status:** 📋 PORTED — implemented in the system it came from on 2026-08-29,
with its first publish still ahead of it at the time of the port. Not wired
here; the instance binds the scheduler and the browser session.

**Description:** Publish at most **one** approved piece per publishing day on
the channel that uses the **authenticated-browser publishing seam**. One piece
means a single post **or one whole thread**, however many parts the thread
holds.

**Agent:** none, directly — same as `ship_content`.
`agents/campaign-strategist/agent.md` watches the output, not the routine.

**Skill(s):** `skills/ship-content-x/SKILL.md`

**The `_x` in the name is the channel suffix** — see the naming note in
`ship_content.md`. This is the second channel's ship routine, kept in the port
because the seam it demonstrates is the one most businesses will hit second.

**Trigger:** the clock, **daily**. The skill gates the days.

**Capability required:** something that can start a session **on a machine
with a live, logged-in browser**. This seam has **no headless path**. It cannot
run on the container or server that runs the rest of the department's
scheduled work, which means this one routine lives on a different host from
everything else — write that down in the instance's own notes, because it is
the fact that explains every future "why didn't this run".

*This instance's binding, as an example:* a desktop-app routine on the
approver's own machine, firing every morning, publishing on three configured
weekdays.

**Suppressed on `MODE` = sabbath / retreat / quiet:** yes.

**Blocked by `MKT_PUBLISH_FREEZE`:** yes. Approved pieces queue and drain
oldest-first when it lifts.

---

## Why this channel publishes through a browser at all

Not a preference. On the account this was ported from, that platform's API was
**entitlement-blocked behind pay-per-use billing**: with the connection showing
ACTIVE, reads returned 401, writes returned 401, and search returned **402
Payment Required**. A billing gate, not a scope problem — no amount of
re-linking or re-authorising moves it. Publishing went to the browser because
there was no second working option, and the scheduler shim written for the
API design was deleted rather than left to rot.

**What that costs, stated plainly:**

- **No headless run.** It needs a real machine with a real session.
- **It silently does not run if the machine is asleep.** No error, no alert,
  no partial output — a publishing day just quietly passes.
- **It cannot re-authenticate.** A dropped session stops the run and logs
  `not_logged_in` rather than guessing.
- **It is less robust than a container cron, permanently.** That is the price
  of a zero-cost, non-metered publishing path.

**What it buys**, and it is not nothing: no metered spend, atomic multi-part
publishing through the platform's own composer instead of a chain of replies,
and a read-back check *stronger* than the API's — it confirms the piece as
rendered on the timeline rather than as an identifier returned by a call.

## The routine fires DAILY and the skill enforces the days

The scheduler this was built against offered "every day" or one fixed weekday,
and could not express three weekdays. **Keep this design even where the
scheduler is more capable**, because the reasoning is about the department, not
about that scheduler:

1. **Three copies of a prompt drift.** Three weekly routines are three copies
   of the same instruction, and the moment one is edited the other two are
   subtly wrong — with no mechanism anywhere that notices.
2. **It makes cadence a config value instead of scheduler configuration.**
   Adding a publishing day or dropping to two is a one-line edit in
   `config/config.yaml`, with nothing to reconfigure, re-install, or re-paste.
   Under three routines the same change means re-doing scheduler config — the
   recurring manual step this department is not allowed to add.

The skill reads the allowed days **every run** and stops immediately on the
others. Four quiet no-ops in a week is the design working, not a routine
misfiring.

## What it does

1. **Mode and freeze check.** Halt value in `MODE`, or a non-empty
   `MKT_PUBLISH_FREEZE` → log one line and exit.

2. **Day gate.** Compute today's weekday **fresh** from the system date and
   compare against the channel's configured publishing days. Never hardcode
   the list, never trust a stored weekday label, and read it every run —
   config is where the cadence actually lives. Not a publishing day → log
   `non_publishing_day` and stop.

3. **Daily cap.** Anything already published on this channel today → stop.
   The guard is the calendar day, not the run.

4. **Select exactly one piece.** Of all pieces with this channel, `status:
   approved`, and a filename date of today or earlier: **the single oldest.**
   A thread is one piece regardless of length. Everything else is
   `deferred_backlog` for tomorrow.

5. **Session check before anything is typed.** Confirm the browser is logged
   in as the configured account. Wrong account or no session → publish
   nothing, log the reason, stop. Publishing a business's content from the
   wrong logged-in account is a mistake with no clean undo.

6. **Pre-flight the whole piece.** Validate **every part** before posting
   **any** part: per-part length against the platform's limit, counted the way
   the platform counts it. Where a limit is *weighted* — some scripts and
   emoji counting as more than one character, links counting as a fixed
   length regardless of their real length — it is computed mechanically, never
   judged by eye. Also confirm every referenced asset exists on disk.

   Whole-piece validation before the first part is the rule that stops a limit
   failure leaving **half a thread live** on a public timeline.

7. **Publish through the platform's own composer**, not by chaining replies —
   the composer is atomic, which is most of this routine's failure handling.
   Fill every field, then **read every field back** and confirm it matches the
   draft before committing. Anything off → publish nothing and stop; the piece
   is untouched and the next run retries cleanly, because nothing reached the
   timeline.

8. **Verify by looking.** Read the account's public timeline back and confirm
   the piece appears with the expected number of parts, capturing each part's
   identifier. **Do not mark a piece shipped on the strength of the click
   alone.**

9. **Update state** exactly as `ship_content` does: move to
   `content/shipped/`, append to `voice/samples/{register}.md`, record
   `used_in` on any proof entry used, log the run.

## What it never does

- Publish more than one piece per publishing day, thread or not.
- Publish out of order to drain a backlog.
- **Click publish a second time** because the first attempt looked like it
  failed. Go and *look* first. A second click after a slow-but-successful
  publish posts the piece twice, and duplicates on a public timeline are the
  approver's to clean up, not the system's.
- Attempt the platform's API "just in case". Those calls return 401/402 on this
  seam by definition, and a routine that tries both paths hides which one it
  actually used.
- Delete a published piece. Not for a duplicate, not for a typo.
- Ask a question and wait. Unattended run: publish, or stop with a named
  reason.

## When it cannot run

| Failure | What happens | How you find out |
|---|---|---|
| Halt mode or publish freeze | Exits at step 1 | One log line |
| Not a publishing day | Exits at step 2 | `non_publishing_day` — the expected outcome most days |
| Already published today | Exits at step 3 | `already_shipped_today` |
| Nothing approved and due | Publishes nothing | Empty queue; usually means the work is sitting at M2 |
| **Machine asleep** | **Nothing runs at all** | **Nothing tells you.** The first signal is a publishing day that passed with an approved piece still queued |
| Session dropped or wrong account | Publishes nothing, piece untouched | `not_logged_in` / wrong-account in the run's own log — which lives wherever the host writes it, **not** necessarily in the instance's `traces/` |
| Length or readback validation fails | Publishes nothing, no partial thread | Named error |
| Ambiguous publish outcome | Verify by reading the timeline before doing anything else | Step 8 exists for exactly this |

**When a publishing day passes with an approved piece still queued, the causes
in order of likelihood are: the machine was asleep, the session dropped, or the
piece's filename date is in the future.** Check them in that order.

**The asleep case is the honest gap in this routine**, and it is a property of
the seam rather than a bug in the schedule. Closing it needs something outside
this department watching for the *absence* of a publish. Until that exists, the
first live signal that this routine works is a published piece, not a log line.

## Notes

Ported 2026-08-29.

**The routine lives in the host's scheduler config, not in this repository.**
Nothing here installs it or edits it. That has one consequence worth knowing
before you touch anything: **changing the cadence is a config edit** (one line
in `config/config.yaml`, nothing else touched), but **changing the routine's
prompt is a manual re-paste** on the host. So change the prompt only when the
skill's contract has genuinely moved — and put every knob that might plausibly
change into config instead, where it costs nothing to turn.

**On choosing the publishing days and the hour.** That belongs in the
channel's playbook with its evidence, not here — but three principles from the
port survive the move: prefer a cadence supported by **two independent
large-sample datasets** over one; the "best time" studies mean the *audience's*
timezone, not the publisher's, which for a business selling into another region
moves the slot by hours; and **stagger** a channel's slot from the other
channels' so two publishing routines never fire into the same minute.

And the caveat that keeps a benchmark from hardening into a fact: platform-wide
averages are not an account baseline. Treat roughly the first eight weeks as
calibration rather than optimisation, and revisit the slot once the channel has
real numbers of its own.
