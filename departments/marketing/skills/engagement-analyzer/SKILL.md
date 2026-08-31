# Skill: engagement-analyzer

**Owner:** campaign-strategist
**Model:** small for extraction and arithmetic — escalating to reasoning for the
harvest loop (deciding whether a read added anything new, whether the feed has
actually ended, whether a piece is really missing) and for the weekly pattern
pass
**Trigger:** a daily routine, on a machine that can reach the channel's metrics
surface. Also callable inline with an explicit piece path immediately after a
collection, so a fresh number does not wait for the next scheduled run.
**Suppressed when:** `MODE` is `sabbath`, `retreat` or `quiet`. Not suppressed by
`MKT_PUBLISH_FREEZE` — a freeze blocks publishing, not measurement.

---

## Paths

Bare paths are **instance-relative** (`$MKT_INSTANCE`). Paths prefixed
`$MKT_DEPT` are template-side and read-only at runtime.

---

## Purpose

Collect engagement for shipped pieces, compare each against a rolling baseline,
detect outperformers, and write the record to `performance/`.

---

## No manual data entry. Ever.

**If a metric cannot be collected automatically, it is not collected.** This
skill never asks a human for a number — not in a notification, not in a
"quick ask", not as a skippable optional field. A metric that requires someone to
go and look something up is a recurring manual step, and a department that adds
one has failed at its own job.

The concrete case that set this rule: **direct-message counts.** No view on the
source channel exposes them, so no automation can ever populate the field. Asking
for them by hand was tried and rejected, on evidence: nobody had ever messaged
about a *specific* piece, and when people do reference a post they do it vaguely
("saw you writing about X") rather than by exact piece, so **reliable per-piece
attribution is not realistically possible even with a willing human.** Asking
would have produced a recurring chore that yields unreliable data.

So the field is written as `null`, permanently, and **`comments` is the north-star
metric** — it is a genuine signal of reader engagement, it is collected
automatically, and it needs no input from anyone. A metric that cannot be
collected is named as uncollectable in the record, not left looking pending.

---

## Execution model — where this can and cannot run

The collection half needs whatever the channel's metrics surface needs. Be
precise about which lane a given run is in, because the answer changes what a
zero-collection run *means*:

- **A scheduled run on a machine with a live authenticated session** — the
  automated path, and the intended home. This is the instance's binding of the
  `publishing.methods.browser` seam for reads.
- **An interactive or on-demand run** on the same machine — same capability.
- **A headless run** — the browser tooling does not exist there. Collection
  returns every candidate `uncollected` with reason `session_unavailable` and the
  analysis half still runs over whatever numbers are already on file. **This is a
  correct outcome, not a failure**, and it must never error the caller.
- **A remote/cloud run** — no access to the local session; auth-walled.

Settled, do not re-litigate on the source channel: **headless scraping does not
work** (the platform auth-walls a headless browser even with cookies), and the
per-post analytics deep-link is stale (it redirects to the feed). Both confirmed
dead 2026-07-09. Where an instance's channel does expose analytics through an
API, bind that instead and delete step 3 — but keep step 4's parsing rules and
step 5 onward unchanged.

---

## Config keys read

| Key | Use |
|---|---|
| `channels.{channel}.enabled` | skip disabled channels entirely |
| `channels.{channel}.metrics_surface` | the URL or command the collector reads |
| `channels.{channel}.handle` | identifies the account, and builds `url` for a piece |
| `channels.{channel}.metrics_available` | list of metrics this channel can actually yield; anything not listed is written `null` and named uncollectable |
| `performance.baseline_window` | how many recent pieces the median is taken over (default 10) |
| `performance.interrupt_multiple` | default 3.0 |

Credentials, where a channel needs one, are referenced **by env var name** and
never written to a record or a trace.

---

## Inputs

- `content/shipped/*.md` — every shipped piece, with `shipped_at`, `channel`,
  `archetype`, and body text (the body's opening line is what matches a feed entry
  to a file). The piece's identifier is `post_id` on a single-post channel and the
  **first** entry of the ordered `post_ids` on a thread channel — a thread's
  metrics attach to its hook, and summing across a thread's parts would
  double-count a reader who saw one thread
- `performance/` — prior records, for the baseline
- `performance/baselines.md` — the current rolling medians
- `.env` → `MODE`
- Optionally, explicit piece path(s) from a caller — then report only on those

### Frontmatter this skill reads and writes

Reads: `channel`, `shipped_at`, `archetype`, `publish_verified`, and
`post_id` / `post_ids[0]` / `post_url`.

Writes exactly one block, on the shipped piece, and nothing else:

```yaml
engagement:
  impressions: N
  likes: N
  comments: N          # north star
  reposts: N
  inbound_dms: null    # uncollectable — see the rule above. Never solicited
  url: "{live post url}"
  auto_collected: true
  auto_collected_at: {ISO timestamp}
  source: "{which surface, which session}"
  final: false         # true once the last snapshot stage lands
  snapshots:
    - stage: 48h
      collected_at: {ISO timestamp}
      impressions: N
      likes: N
      comments: N
      reposts: N
```

**Writing this block does not reopen a shipped piece.** `content/shipped/` is
terminal for the *piece* — its `status` is never touched here and it never
re-enters the publishing queue. Metrics accrue to a published thing; that is not
the same as work resuming on it.

**Two independent lifecycles, never conflate them:**

| Flag | Governs |
|---|---|
| `auto_collected: true` | this piece's numbers are being handled by automation. Terminal on its own — nothing further is ever asked of a human about this piece |
| `final: true` | the last snapshot stage has landed. Governs whether this skill still re-visits the piece to take another snapshot |

A piece can be `auto_collected: true` and `final: false` at the same time: fully
automated, still maturing.

---

## Steps

### 1. Mode check, then identify candidates

`MODE` is `sabbath`/`retreat`/`quiet` → exit silently, `mode_halt`.

**Impressions keep climbing well past the first read**, so one early snapshot
understates real reach. Take up to three per piece — **48h, 7d, 30d** — and stop
revisiting once the 30d snapshot lands.

Scan `content/shipped/*.md`. A piece qualifies when:

- `engagement.final` is not `true`, **and**
- at least one stage's threshold has passed (`shipped_at` + 48h, + 7d, + 30d)
  that is not already present in `engagement.snapshots`.

If more than one stage is simultaneously due — the first run on a piece happens
ten days after it shipped — collect only the **most mature satisfied stage.**
There is no way to retroactively recover an earlier stage's number, so do not
fabricate one. Collecting the 30d stage sets `final: true` immediately even
though 48h and 7d were skipped.

Neither `post_id` nor `post_ids` → log `no_post_id`, skip. `final: true` → done forever.

**No candidates → write the trace and exit. Do not open a session.**

Also catch the dropped-invocation case on every daily run: a piece with
`auto_collected: true` but **no matching record in `performance/`** had numbers
written and was never analysed — an inline invocation died mid-run. Process it
now from the numbers already on file; no re-collection needed.

**Re-processing is normal, not an error.** Each new snapshot supersedes the prior
analysis for that piece. Just recompute from whatever is currently in the
frontmatter.

### 2. Preflight the session

Confirm the collector is pointed at the right authenticated session for the
account in `channels.{channel}.handle` — not a different profile that happens to
be logged in somewhere. Wrong account reads the wrong numbers and writes them to
the right files, which is worse than collecting nothing.

No session available → return every candidate `uncollected` with reason
`session_unavailable` and exit cleanly. **Never error the caller**; the analysis
half of this skill still runs.

Redirect to a login, auth-wall, or checkpoint → `auth_expired`. Notify once with
a one-line, actionable message ("the session needs a refresh — log in once"), and
exit. Do not retry in a loop.

### 3. Harvest — the loop, and why one read is never enough

The account's own recent-activity view lists every piece you need with its
metrics inline: no per-post navigation, no analytics deep-link. **The page has
never been the problem. Reading it in a single shot is.**

**The feed is virtualised.** Only a handful of entries (~5) exist in the DOM at
any moment; entries that scroll out of view are **destroyed, not hidden**. So one
read returns a five-entry window, and a later read after a long jump returns a
*different* five-entry window with the earlier entries gone from the text
entirely. The page's own "N posts loaded" counter says nothing about how many are
readable right now.

That is a reading-strategy problem with a known fix, not a platform limit.
**"Virtual scrolling limitation" is not an accepted outcome of this skill.** On
2026-08-20 five pieces that a run had just reported as unreachable were sitting
on the same page, plainly visible, a few scrolls further down — found by hand.
If you are about to write that phrase into a trace, you have not finished this
step.

**3a. Set the floor before you scroll.** Take the **oldest** candidate's
`shipped_at`. That date is the **scroll floor**: the depth you must reach before
you are entitled to conclude anything is missing. Hold it for the whole loop. The
floor comes from the candidates, **never from a fixed age window** — if a caller
mentions a rough depth ("go back about 30 days"), treat it as a hint at scale,
never a cap. A 30d snapshot routinely falls due on a piece 50+ days old, and a
run that stopped at an arbitrary line would strand exactly the pieces it exists
to collect.

**3b. The loop.** Keep a running **accumulator** of entries keyed by opening body
line. Because the DOM is virtualised, **every read merges into the accumulator
and no read is ever the full page.** Repeat:

1. Read the page text. Merge any entries not already in the accumulator.
2. If a "show more results" control is present, click it, wait ~2s, return to 1.
3. Scroll down **one short step — roughly one viewport or less.** Short steps are
   the point: consecutive reads must **overlap**, or entries fall into the gap
   between two windows and are lost for the run. A jump to the page bottom reads
   *far fewer* posts than ten small scrolls, not more.
4. Wait 1–2s for lazy-load, return to 1.

Clearing a 30-day window normally takes **20–40 iterations. That is the job, not a
symptom of something wrong.** Do not stop at five. Do not read two flat windows
and conclude the feed ended — these feeds routinely pause a second or two before
appending the next batch.

**3c. When you may stop.** On the **first** of these, recorded as `stop_reason`:

| `stop_reason` | Condition |
|---|---|
| `all_candidates_matched` | every candidate is in the accumulator. The normal ending |
| `reached_floor` | an entry has been read whose age is clearly older than the floor — everything that could qualify has been passed |
| `feed_exhausted` | **five consecutive** scroll steps produced zero new distinct entries **and** the scroll height did not grow. Both conditions, five times in a row — not one flat read |

**Nothing else is a reason to stop.** Not iteration count, not elapsed time, not
"the older ones appear unreachable."

A candidate still absent once the loop ended at `reached_floor` or
`feed_exhausted` → `not_found_on_page`. A piece really can be gone — deleted, or
restricted. But **that conclusion is earned by scrolling to the floor**, and the
trace must carry the loop evidence (step 8) to back it. Without that evidence it
is a guess, and this skill does not guess.

### 4. Parse and match

**Impressions** are explicitly labelled (`94 impressions`). This is the definitive
author-only signal. Absent for an entry → do **not** write partial numbers for it;
mark that piece `extraction_failed`.

**Reactions, comments, reposts:** these feeds **omit the label when the count is
zero.** So parse a number when the label is present; when it is absent, the value
is a genuine **0, not null**. Getting this backwards turns every quiet post into
a hole in the baseline.

**Match each entry to a shipped file by the piece's opening body line** — the most
reliable key. Sanity-check the entry's relative age ("6d", "1w") against the
file's `shipped_at`. Genuinely ambiguous → re-read that entry against the full
candidate list before deciding; still unclear → `match_ambiguous`, write nothing.
**Never write numbers to the wrong piece.**

**Sanity check:** `impressions < reactions` is implausible → `implausible_numbers`,
skip that piece. Do not write scrambled data.

### 5. Write the engagement block

Append this stage's snapshot to `engagement.snapshots` and **mirror its values to
the top-level fields**, so every consumer that reads `engagement.impressions`
keeps working unchanged and always sees the most mature number. Set
`auto_collected: true`, `auto_collected_at`, and `source`. Set `final: true` only
on the last stage.

Fill `url` from `post_url` if the piece carries one, otherwise derive it from
`post_id` (or `post_ids[0]`) and the channel's URL form. Anything in
`channels.{channel}.metrics_available` that the surface did not yield stays
`null`, and anything not in that list is named uncollectable in the record rather
than left looking pending.

### 6. Compute the baseline

Read the last `performance.baseline_window` records (default 10) for **the same
channel**, by `shipped_at` descending, where `impressions > 0`.

Baseline = **median** impressions, median likes, median comments across them.
Median, not mean: one outlier post otherwise moves the bar for a month and every
subsequent piece reads as an underperformer.

Fewer than 5 in history → use what exists and mark the record
`low_sample_baseline: true`. A new channel has no baseline and saying so is
better than computing a confident number from two data points.

Rewrite `performance/baselines.md` with the current medians per channel, the
window size, and the sample count. It is the one file a human or another agent
reads to know what "normal" currently means.

### 7. Classify, and detect the interrupt

```
performance_multiple = impressions / baseline_impressions
```

| Multiple | Reading |
|---|---|
| < 0.5× | underperformer |
| 0.5× – 1.5× | normal |
| 1.5× – 3× | strong |
| ≥ `performance.interrupt_multiple` (3.0) | interrupt trigger |

**`comments` is the north star** and is always noted separately, regardless of
the impressions multiple. Impressions measure distribution; comments measure
whether anyone cared.

Interrupt trigger **and** `shipped_at` within the last 6 hours → append to
`agents/campaign-strategist/notebook/interrupts.md`:

```
- {timestamp} | interrupt | piece: {slug} | {multiple}x baseline | comments: {N}
```

The strategist's interrupt check picks it up on its next pass. The 6-hour window
is what makes it actionable — a 3× post discovered a week later is a pattern for
the weekly report, not an interrupt.

### 8. Write the record and the trace

`performance/{slug}.md` — one file per piece, rewritten (not appended) on each
snapshot so it always shows the most mature numbers plus the full snapshot
history:

```markdown
# {slug} — {archetype} — {channel}

- shipped: {date}
- verified: {publish_verified}
- impressions: {N} ({multiple}x baseline)
- likes: {N}
- comments: {N}   <- north star
- reposts: {N}
- inbound_dms: uncollectable — no surface exposes it, never solicited
- hook: "{first line}"
- baseline: {impressions} / {likes} / {comments} over {n} pieces{, low sample}
- snapshots: 48h {N} | 7d {N} | 30d {N}
- notes: {any pattern worth noting}
```

`traces/mkt-engagement-{YYYY-MM-DD}.log`, carrying: `run_at`, the method, the
candidate count, the **scroll block** (`iterations`, `show_more_clicks`,
`distinct_entries_seen`, `oldest_entry_age_seen`, `floor`, `stop_reason`), what
was collected with its stage, and what failed with its reason.

**The scroll block is required on every run that opened a session** — it is what
makes a `not_found_on_page` claim checkable instead of an excuse. A trace
reporting `not_found_on_page` alongside a low iteration count, or a `stop_reason`
other than `reached_floor`/`feed_exhausted`, is a **failed run, not a completed
one**: the loop was abandoned early and the pieces are still on the page.
`virtual_scroll_limit` and its equivalents are not valid reasons and must never
be written.

**`run_at` is the real wall-clock moment the trace is written.** Read the system
clock at write time and write a full ISO-8601 UTC timestamp, seconds included.
**Never the run's calendar date padded to `T00:00:00Z`**, never a date lifted from
a run id or a filename. Fixed 2026-08-27, after every trace for several days had
written midnight of its own date — off by 7 to 16 hours, and always *early*, so
every downstream staleness read was biased toward "more stale than it is." That
is what made a daily brief measure a 39-hour collection gap where the real gap
was 21, cross its threshold, and report the automation as possibly down. **A bare
date is not a timestamp.**

Write the trace even on a zero-candidate exit — anything that reasons about
whether collection is healthy reads `run_at`, and a missing trace reads
identically to a dead routine.

### 9. Weekly pattern pass

Only when invoked as part of the weekly plan, not on the daily run. Read the last
4 weeks of `performance/` records and answer:

- Which archetypes are outperforming? Underperforming?
- Is there a day-of-week pattern? (If there is, it is evidence for a
  `publishing_days` change in config — raise it, do not drift the cadence.)
- Do pieces with a CTA generate more comments than pieces without?
- Any topic cluster that is consistently strong?

Write to `agents/campaign-strategist/notebook/{YYYY-MM-DD}-audience-obs.md` and
return the observations to the campaign strategist for the weekly report. **Do
not act on them** — cadence, archetype mix and topic selection are the
strategist's calls and, where they change the plan, the approver's.

---

## Outputs

| Path | Contents |
|---|---|
| `performance/{slug}.md` | per-piece record, rewritten on each snapshot |
| `performance/baselines.md` | current rolling medians per channel, window size, sample count |
| `content/shipped/{piece}.md` | the `engagement:` block only — `status` untouched |
| `agents/campaign-strategist/notebook/interrupts.md` | appended when a piece crosses the interrupt multiple inside 6 hours |
| `agents/campaign-strategist/notebook/{YYYY-MM-DD}-audience-obs.md` | weekly pattern pass only |
| `traces/mkt-engagement-{YYYY-MM-DD}.log` | including the mandatory scroll block |

---

## Stop codes

| Code | Meaning |
|---|---|
| `analyzed` | success — collected and/or analysed |
| `mode_halt` | `MODE` is sabbath / retreat / quiet |
| `no_candidates` | nothing due. Exits without opening a session |
| `session_unavailable` | no authenticated session in this lane — analysis still ran, caller not errored |
| `auth_expired` | session redirected to a login or checkpoint |
| `no_post_id` | piece carries neither `post_id` nor `post_ids` — nothing to match against |
| `not_found_on_page` | absent after the loop reached the floor — **only valid with loop evidence in the trace** |
| `extraction_failed` | impressions label absent for a matched entry; no partial numbers written |
| `match_ambiguous` | could not confidently map an entry to a piece; nothing written |
| `implausible_numbers` | failed the sanity check; nothing written |
| `low_sample_baseline` | informational — fewer than 5 pieces of history |
| `metric_unavailable` | informational — a metric this channel cannot yield; recorded as uncollectable, never asked for |

---

## Failure modes to avoid

- **Adding a manual ask** for any metric, in any form, however small or skippable.
- **Stopping the harvest loop early** and calling the remainder unreachable
  (2026-08-20).
- **Big scroll jumps** instead of overlapping short steps — entries fall into the
  gap between windows and are silently lost.
- **Reading an absent label as `null` instead of `0`**, which puts holes in the
  baseline.
- **Writing numbers to the wrong piece** on an ambiguous match.
- **Padding `run_at` to midnight** instead of reading the clock (2026-08-27).
- **Skipping the trace on a zero-candidate run** — it reads identically to a dead
  routine.
- **Using a mean instead of a median** for the baseline.
- **Acting on the weekly patterns** rather than handing them to the strategist.
