# Skill: content-reviewer

**Owner:** content-writer (the craft agent under the campaign strategist)
**Model:** `reasoning` tier — **do not upgrade it to the `generation` tier.** This
is a deliberate exception to the department's default of authoring at the
highest tier. Reviewing is judgment against evidence, not generation, and a
reviewer running at the drafting tier reliably starts rewriting the piece
instead of reviewing it — which produces a second draft nobody briefed and
quietly costs a revision round.
**Trigger:** a piece lands in `content/drafts/` with `status: draft`; or a direct call
**Suppressed when:** `MODE` is `sabbath`, `retreat`, or `quiet`

---

## Purpose

The **machine review pass**, run before the approver ever sees a piece. It
compares a draft against what has actually earned engagement on that channel,
sends specific evidence-cited revisions back to the writer, re-reviews, and then
moves the piece from `content/drafts/` to `content/ready-to-send/`.

**It never approves.** `ready-to-send` means *reviewed*, not *approved*. The
approver's M2 is the only publish gate and it is completely separate from this
loop. A `satisfied` verdict grants nothing.

**A publish freeze does not stop this skill** — `MKT_PUBLISH_FREEZE` blocks
publishing only.

---

## Paths

Bare paths are **instance-relative** (`$MKT_INSTANCE`); `$MKT_DEPT` prefixes are
template-side and read-only.

---

## What "the data" is, and what it is not

Be honest about the evidence base, because the temptation to invent it is real.

- **Performance numbers come from `performance/`**, written by
  `$MKT_DEPT/skills/engagement-analyzer/SKILL.md`. This skill **consumes**
  them. It never collects or computes engagement numbers itself, and it never
  guesses at a missing one. A shipped piece with no numbers is a gap for the
  analyzer, not a hole for this skill to fill.
- **Most channels do not expose the metric you actually want** at the access
  tier a small business has. Reach and impressions are commonly gated behind a
  partner programme; comment text is often not readable at all. What a channel
  can and cannot be read for is recorded in `config/channels/{channel}.md`, and
  that record is the authority — not an assumption about what an API "should"
  return.
- **A metrics call returning zero is inconclusive**, not evidence of zero
  engagement, unless the channel playbook states that the read is verified.
  Reads that silently return empty for scope reasons rather than erroring are
  common enough that treating a zero as data has produced confidently wrong
  reviews.

**The north-star metric is declared per channel** in `performance/baselines.md`
or the channel playbook. Two constraints on what may be chosen: it must be
**attributable to a single piece**, and it must be **collectible without a
human typing it in.** An earlier north star was abandoned for failing the
second test — it required someone to hand-count and paste a number per post
every week, which is not a metric a department can steer on, it is a chore
wearing a metric's clothes. Reach and likes are secondary context, never the
headline.

---

## Inputs

- One or more draft paths in `content/drafts/` with `kind: content-draft` and
  `status: draft` (required)
- `performance/` — per-piece metrics, the primary evidence source
- `performance/baselines.md` — the north star, and what normal looks like
- `agents/campaign-strategist/notebook/` — recent audience observations, if any
- `agents/cmo/config/anti-patterns.md` — **mandatory read; the run does not
  start without it**
- `agents/cmo/config/positioning-statement.md`
- `voice/guide.md` — voice integrity check on every suggestion
- `config/channels/{channel}.md` — format limits, what is readable, what works here
- `max_rounds?: number` — default **2**; do not raise it without the approver's
  instruction

---

## Pre-flight

### 1. Mode
`.env` → `MODE`. `sabbath` / `retreat` / `quiet` → exit without writing.
Stop code `mode_halt`.

### 2. Status — pre-approval only
If the piece is `status: approved` or `status: shipped`, or sits in
`content/approved/` or `content/shipped/`: **do not touch it.** Skip, log
`post_approval_status` to the trace, move on. This skill operates strictly
before the gate.

A piece already at `ready-to-send` is re-reviewable only when a new round was
explicitly requested — otherwise skip it too, or the loop re-litigates pieces
that are already queued for the approver.

### 3. Anti-patterns must be readable
Read `agents/cmo/config/anti-patterns.md` in full. Every suggestion in steps
4–6 is filtered through it. **If the file can't be read, do not run** — stop
code `anti_patterns_unreadable`. A data-only review with no anti-pattern filter
is worse than no review: it optimises straight into the things the business
decided not to say.

### 4. Count usable history
Count pieces in `performance/` carrying real numbers for the channel's north
star.

- **≥ 5 pieces** → full data-informed review.
- **< 5 pieces** → **low-data mode.** Review against anti-patterns, the
  archetype's own succeeds-when / fails-when criteria (from
  `$MKT_DEPT/skills/content-writer/SKILL.md` § Archetypes), the house style,
  and voice. **Invent no engagement claims.** Stamp `low_data_mode: true` in
  the review block and every trace entry.

A fresh instance is always in low-data mode, and that is the normal starting
state, not a failure.

---

## Steps

### 1. Load the evidence

In this order: the most recent 10–20 entries in `performance/`; then
`performance/baselines.md`; then the latest audience-observation note in
`agents/campaign-strategist/notebook/`, if one exists. Reuse a conclusion the
observation note already reached rather than re-deriving it — re-derivation
from the same rows produces the same answer at a cost.

### 2. Refresh — best effort, supplementary only

For pieces shipped in the last 14 days that carry a platform post id, and only
where `config/channels/{channel}.md` says a read is available: attempt the
read.

Rules for what comes back:
- A **zero result is inconclusive**. Never treat it as data.
- A nonzero result that differs from the stored number: log the discrepancy to
  the trace and note it in the review log **for the analyzer's next run**. Do
  not write to `performance/` yourself — one writer per store.
- An error: log it and continue. **This step failing must never block a
  review.**

### 3. Build the pattern brief

From step 1, extract what correlates with the north star. Look at: which
archetypes drive it versus which only drive reach; the hook shape of the top
performers (a number? a claim? a question?); CTA presence; length; prose versus
bullets; whether a data anchor was present.

**Every pattern cites its evidence** — which pieces, which numbers, from which
entries. A pattern resting on fewer than 3 pieces is marked `weak_signal` and
weighted accordingly. In low-data mode there is no pattern brief; say so rather
than assembling one out of two rows.

### 4. House-style gate — blocking, and it runs first

Check the draft against `$MKT_DEPT/skills/content-writer/SKILL.md` §House style:
banned words, banned phrases, banned structures, the em-dash cap for the
channel (one for long-form, **zero** for X), and the "Term. Explanation." bullet
format. If `$MKT_DEPT/lib/style-check.py` exists, run it and treat a nonzero
exit as failure; otherwise apply the list mechanically — it is finite and
closed.

**A draft that fails this gate does not get an engagement review.** Send it
straight back to the writer with the violations as `reviewer_notes` and re-run.
Style violations are objective and cheap to fix, and reviewing prose that is
about to be rewritten burns one of only two rounds.

Two judgment items no checker sees. Check both, every draft:
- Does the opening sentence set the scene with a grand statement? Then the
  piece should start at the second sentence.
- Does it close on a summary or an inspirational wrap-up rather than on
  substance?

Log `style_gate: pass` or the violation list either way.

### 5. Review the draft

Every concern must be all three of these:

1. **Concrete** — it points at a specific line or element and names the change.
   Not *"make the hook stronger"* but *"the three highest-performing pieces all
   open with the number itself; this hook opens with setup. Move `$140k` to
   word one."*
2. **Evidence-cited** — it names the pattern and its evidence: *"case-study
   pieces averaged 4 comments against 0–1 for pov pieces across the last 12
   entries."*
3. **Anti-pattern-filtered** — checked against `anti-patterns.md` before it is
   written down. **If a pattern correlates with engagement but is banned —
   listicles, contrarian-as-default, hype words — do not suggest it.** Note the
   tension in the review log instead. Data-*informed*, never data-*only*: voice
   and positioning integrity beat a raw engagement number every time. This is
   the rule that keeps a review loop from slowly turning a distinctive voice
   into whatever the platform rewards this quarter.

In low-data mode the same concreteness standard applies, grounded in
anti-patterns, archetype criteria, house style and voice, with **no engagement
claims at all**.

### 5a. Voice check — weighted by how much voice data exists

Read `below_voice_floor` and `voice_borrowed` from the draft's frontmatter.

- `below_voice_floor: true` → the piece was drafted against fewer than 10 real
  samples in its register. Look harder at voice, and say in the review log that
  you did.
- `voice_borrowed: true` → the piece was drafted against samples from a
  **different register** (see the X writer's documented asymmetry). This is the
  channel with the least voice protection in the department, by design. The
  specific thing to look for is **long-form rhythm surviving compression**:
  paragraph-length setup, a scene-setting opening, a hook that behaves like a
  first line rather than a standalone claim.

### 5b. Image gate — blocks `satisfied`, checked before the text verdict

A review is not only of the words.

1. `image_path` is present **and the file exists on disk** — **or** the
   frontmatter carries an explicit `image: none` with an `image_note` giving the
   reason. A missing or dangling image with no declaration means the verdict
   **cannot be `satisfied`**: return `revise` with "image missing" as a concern
   for the caller to render or declare.
2. The image filename uses the draft's **own slug**. A mismatched slug orphans
   the file and breaks every surface that resolves a piece's visual by slug.
   Three pieces once cleared review with no linked image this way, and a human
   caught it, not the system.
3. **Open the image and look at it.** A unit error in a label (`$35 days`), a
   currency symbol hardcoded to the wrong one, clipped content, the wrong
   piece's content — none of these are visible to an exit code and all of them
   are obvious to an eye. A hardcoded currency symbol once shipped through two
   reviews on a clean render.
4. Carousel pieces: `carousel_pdf` exists, `slide_paths` lists real files in
   order, and `image_path` points at slide 1 so the approval surface can show
   something. Look at **every** slide — one clipped slide ruins the document.

**Verdict:**
- **`satisfied`** — no material concerns and the image gate passed → step 8.
- **`revise`** — **1 to 3 concerns, maximum**, ranked by expected effect on the
  north star. More than 3 means the source material is probably wrong, which is
  the campaign strategist's call — flag that instead of writing six notes.

### 6. Request the revision

Call the matching writer with its `revision_target` input —
`$MKT_DEPT/skills/content-writer/SKILL.md` for long-form,
`$MKT_DEPT/skills/x-content-writer/SKILL.md` for 280-character channels
(dispatch on the draft's `channel` and `register`):

```
revision_target:
  existing_draft_path: {draft path}
  reviewer_notes:      {the ranked, evidence-cited concerns from step 5}
```

The writer revises **in place**, reading archetype, register and source refs
from the draft's own frontmatter, and runs its own critique pass on the
revision. Its model tiers are unchanged by this skill. If the writer returns a
stop code, record it and treat the round as spent — stop code
`writer_unavailable` if it could not run at all.

### 7. Re-review

Run step 5 again on the revised draft. This is round 2.

- `satisfied` → step 8.
- Still `revise` and rounds < `max_rounds` → step 6 again.
- Still not satisfied at `max_rounds` (default 2): **stop.** Do not loop, do
  not silently pass the piece off as reviewed, and **do not block it from the
  approver.** The verdict becomes `unresolved` and the piece still moves. Three
  rounds of a machine arguing with a machine costs more than one human glance.

### 8. Record, move, and hand it to the approver

**a. Write the review block** into the draft's frontmatter — this block only:

```yaml
review:
  reviewed_by: content-reviewer
  rounds: 0                     # 0 | 1 | 2
  verdict: satisfied            # satisfied | unresolved
  reviewed_at: 2026-08-29T18:40:02Z
  low_data_mode: false
  style_gate: pass
  patterns_applied:
    - "hook opens on the number (evidence: 3 pieces, north star 4/6/5)"
  tensions:                     # a pattern that correlates but is banned
    - "listicle format leads on reach; banned by anti-patterns. Not suggested."
  unresolved_concerns:          # present only when verdict is unresolved
    - "{remaining concern, evidence-cited}"
```

**b. Set `status: ready-to-send` and move the file** to
`content/ready-to-send/`, keeping the filename. This is the **only** status
transition this skill may make, and it may only make it from `draft`. Writing
`approved` or `shipped`, or moving a file into `content/approved/` or
`content/shipped/`, is out of bounds under every circumstance.

**c. Raise the M2 item.** Write the approval item to `inbox/` — the piece, its
`full_text` **complete and untruncated**, its visual, and the `review` block
including any unresolved concerns — then `lib/mkt-notify.sh raise {item}`. If
an M2 item already exists for this slug, **update it rather than raising a
second**; a second notification for the same piece trains the approver to stop
reading them.

Never truncate the body the approver is about to approve or reject. A decision
made on a shortened version of the text is not a decision about the text.

**d. Write the review log** to
`agents/campaign-strategist/notebook/{YYYY-MM-DD}-review-log.md`: slug, rounds,
verdict, which patterns were applied, any data-versus-anti-pattern tension from
step 5, any metric discrepancy from step 2.

**e. Trace** to `traces/content-reviewer-{run-id}.json`.

---

## Outputs

| Artifact | Purpose |
|---|---|
| `content/ready-to-send/{piece}.md` | The reviewed piece, moved, `status: ready-to-send`, `review:` block written |
| `inbox/{piece}.md` | The M2 approval item, with the full body and any unresolved concerns |
| `agents/campaign-strategist/notebook/{YYYY-MM-DD}-review-log.md` | What was applied, what was refused, what disagreed |
| `traces/content-reviewer-{run-id}.json` | Run record |

---

## Stop codes

| Code | When | What happens |
|---|---|---|
| `mode_halt` | `MODE` is sabbath/retreat/quiet | Exit silently, nothing written. |
| `post_approval_status` | Piece is approved, shipped, or already queued | Skip it. Logged, not an error. |
| `anti_patterns_unreadable` | `agents/cmo/config/anti-patterns.md` unreadable | **Do not run.** An unfiltered review is worse than none. |
| `style_gate_failed` | Banned words/phrases/structures present | Straight back to the writer; no engagement review this round. |
| `image_undeclared` | No image on disk and no `image: none` declaration | Verdict cannot be `satisfied`; returned as a concern. |
| `writer_unavailable` | The writer skill could not run for the revision | Round is spent; if rounds remain, retry once, else verdict `unresolved`. |
| `max_rounds_unresolved` | Still not satisfied after `max_rounds` | Verdict `unresolved`. **The piece still moves and still reaches the approver.** |

---

## Boundaries — never cross these

- **This loop is not the approval gate.** Never write `status: approved` or
  `status: shipped`, never move a file into `content/approved/` or
  `content/shipped/`, never call a ship skill. `satisfied` means reviewed.
- **Never touch approved or shipped content.** Pre-approval only.
- **Never chase engagement past the guardrails.** No suggestion may reintroduce
  an anti-pattern, whatever the numbers appear to show.
- **Never fabricate or over-trust engagement data.** Stored numbers are the
  source of truth; zeros from an unverified read are inconclusive; small
  samples get flagged, not extrapolated.
- **Never exceed 2 rounds.** After that the remaining concerns travel with the
  piece to the approver. Their judgment, not another iteration.
- **Never write to `performance/`.** One writer per store, and it is the
  analyzer.
- **Never block a piece from reaching the approver.** Every path through this
  skill ends with the piece in `content/ready-to-send/` and an M2 item raised.
  A piece this skill could not satisfy is still a decision the approver is
  entitled to make.
