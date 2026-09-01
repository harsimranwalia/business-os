# Skill: content-writer

**Owner:** content-writer (the craft agent under the campaign strategist)
**Model:** `generation` tier for the draft pass, `reasoning` tier for the critique pass. Tiers, not product names: the instance binds a tier to a model, and a model that goes stale is a config change, not an edit to this file
**Trigger:** a per-piece brief from the campaign strategist's planning run; callable directly by any agent holding a complete brief
**Suppressed when:** `MODE` is `sabbath`, `retreat`, or `quiet`; or the brief's channel sits at autonomy tier `c0`

---

## Purpose

Stateless procedure that turns one per-piece brief into one reviewed draft, in
the business's own voice. No memory. No opinions about strategy — the brief
already decided what to say and when; this skill decides only how it reads.

Covers the **long-form registers**: a scrolled feed post, an article, a
newsletter, an email. Its sibling `$MKT_DEPT/skills/x-content-writer/SKILL.md`
covers the 280-character registers. That split is deliberate and explained
there — a weighted 280-character unit is a different craft, not this craft with
a smaller number.

**A publish freeze does not stop this skill.** `MKT_PUBLISH_FREEZE` blocks
publishing only; drafting, review and approval keep running and the queue
drains when it lifts. Only `MODE` halts drafting.

---

## Paths

Bare paths are **instance-relative** (`$MKT_INSTANCE`). Paths prefixed
`$MKT_DEPT` are template-side and read-only at runtime. Nothing here hardcodes
a repository path; every location resolves through
`$MKT_DEPT/config/conventions.yaml`.

---

## Interface

**Inputs:**

```
channel:      string            — a channel registered in config/config.yaml -> channels
register:     string            — the shape of the writing; must name a real
                                  voice/samples/{register}.md. Department defaults:
                                  long-form-post | article | email | dm
archetype:    'teardown' | 'case-study' | 'pov' | 'frame-shift' | 'data-insight'
              | 'carousel' | 'raw'
source_material:                — at least one field non-null
  proof_ref?:      string       — slug in proof/case-studies/ or proof/internal/
  eng_proof_ref?:  string       — entry under ../engineering/reports/proof/
  topic_ref?:      string       — an entry id in content/topic-bank.md
  decision_ref?:   string       — a recorded decision the business made
  free_form?:      string       — raw notes from the caller
series?:      string            — slug of a plan in content/series/
max_length_words?: number       — archetype defaults apply if omitted
include_cta?: boolean           — default false
cta_style?:   string            — the CTA text/shape, passed by the caller
notes_from_caller?: string      — e.g. "tone this one down, the last one was sharp enough"
revision_target?:
  existing_draft_path: string   — a draft in content/drafts/
  reviewer_notes:      string   — concrete, evidence-cited revision requests (from content-reviewer)
```

**When `revision_target` is present:** revise that draft in place instead of
writing a fresh one. Read `channel`, `register`, `archetype`, `series`, and
`source_refs` from the existing draft's **own frontmatter** — never make the
caller re-supply what the file already states. Preserve every frontmatter field
except the content, and **never touch `status`**: this skill and content-reviewer
both operate strictly pre-approval, and status transitions past
`ready-to-send` belong to the approver. Apply `reviewer_notes` as targeted
edits, not a rewrite — keep what wasn't flagged. Run the normal critique pass
against the revision, same as a fresh draft.

**Outputs (written to file and returned to the caller):**

```
hook:           string
body:           string
close:          string
cta?:           string
full_text:      string          — exactly what would publish, hashtags included
reasoning:      string          — why this source material, why this structure
critique_notes: string          — what the critique pass found
source_refs:    string[]        — every ref used, for the draft frontmatter
```

---

## Pre-flight — all six, before Pass 1

### 1. Mode

Read `.env` → `MODE`. On `sabbath`, `retreat`, or `quiet`: exit without
writing. Stop code `mode_halt`.

### 2. Channel autonomy

Read `config/config.yaml` → the brief's channel. At **`c0` (observe)** nothing
is drafted — exit with `channel_not_live`. `c1` and above draft normally;
`c1` means there is no publishing path yet, which is the caller's problem to
have declared, not a reason to write worse.

### 3. Brief completeness

`channel`, `register`, and `archetype` must all be present and `register` must
name a file that exists at `voice/samples/{register}.md` **or** be explicitly
declared new by the caller. A missing field is `brief_incomplete` — return it,
don't guess. A piece drafted from an invented register calibrates against
nothing.

### 4. Source material

At least one field of `source_material` non-null. All null → `no_source_material`.
The caller decides whether to substitute material or drop the piece; this skill
does not go looking for something to write about. That is topic-miner's job and
it is a different job.

### 5. Voice floor — count, stamp, never silently degrade

Count the samples in `voice/samples/{register}.md`.

- **Zero samples AND no `voice/guide.md`** → stop, `no_voice_reference`. There
  is nothing to write *as*. Escalate once via `lib/mkt-notify.sh raise` with
  the seeding instruction from `conventions.yaml` → `voice.seeding`: seed from
  real published material in the business's own voice, in this register, never
  from a description of the voice.
- **Below the floor of 10** (including zero, when the guide exists) → **draft
  anyway.** Stamp `voice_sample_count: {N}` and `below_voice_floor: true` in
  the frontmatter. This is the contract's own rule
  (`conventions.yaml` → `voice.below_floor`): a thin corpus does not silently
  produce worse output, it leans harder on the review pass and on the
  approver's M2, and the gap is recorded so it is visible rather than
  discovered later.
- **At or above 10** → stamp `voice_sample_count: {N}` anyway. The number is
  cheap and it is how anyone later reads whether a bad run was a voice problem.

Every piece that ships is a candidate sample for its register. That is the
intended path from an empty corpus to a calibrated one, and it means the
corpus can only ever hold material the approver already published.

### 6. Naming rules — anonymize in the prompt, never redact after

Raw source material may name a real client by name even when that client
requires anonymization. **The source file is allowed to say it; the output is
not.**

- Read `config/config.yaml` → `naming_rules`. If the instance has none,
  **default to treating every named client as requiring anonymization.**
- Any name in `naming_rules.never_name` that appears in the source material
  gets replaced in the prompt **before** Pass 1 — "a client in the security
  industry", "a mid-market logistics operator". The drafting model never sees
  the real name. Drafting with the real name and redacting afterwards is how
  it survives into a field nobody re-read.
- Names in `naming_rules.ok_to_name_with_public_metrics` may be used as given.
- This applies to **every field the model reads or writes** — `reasoning`,
  `critique_notes`, and `source_refs` included. An anonymized body with the
  real name still sitting in the frontmatter is still a leak.

This check exists because a shipped post named a client directly. It was
caught by a human, after publication.

---

## House style — binding on every draft

Set after an AI detector scored a run of drafts 100% AI-written across three
different post shapes. These are hard rules, not preferences. They are the
**department's floor**: `voice/guide.md` may override a specific rule only by
naming that rule explicitly, and the override lives in the guide where anyone
can see it. Silence in the guide is not an override.

**Voice.** Be direct. Have opinions. Use specific examples and numbers, not
vague claims. State the point first, then support it. Trust the reader to
recognise what matters without labelling it "significant" or "important."

**Banned words.** delve · dive into · navigate (figurative) · underscore ·
bolster · foster · harness · leverage · unpack · shed light on · pave the way ·
pivotal · groundbreaking · cutting-edge · transformative · game-changing ·
innovative · robust · comprehensive · seamless · intricate · nuanced (as empty
praise) · vibrant · multifaceted · holistic · testament · landscape
(figurative) · realm.

**Banned phrases.** "In today's [fast-paced/rapidly evolving/digital] world…" ·
"It's important/worth noting that…" · "One of the most
[important/significant/crucial]…" · "When it comes to…" · "At its core…" ·
"At the end of the day…" · "This is where X comes in" · "Let's break it down" ·
"Plays a crucial role in…" · "It cannot be overstated…" · "…underscoring the
importance of…" · "…highlighting the need for…" · "…reflecting a broader trend
toward…" · "…marking a significant shift in…"

**Banned structures.** "It's not just X — it's Y" · "Not only X, but Y" ·
"This isn't about X. It's about Y." · "No X. No Y. Just Z." They mimic insight
without providing any.

**Structure.**
- Vary paragraph and sentence length. Never write uniform blocks.
- **Never use the "Term. Explanation." / "Bold term: explanation" list format.**
  It is the single most recognisable AI pattern.
- Bullets are allowed where the content is genuinely a list a reader scans —
  written as flowing sentences or lowercase fragments. Use them **where they're
  needed, not everywhere**; prose is usually clearer.
- No signposting ("Let's explore", "Now let's turn to"). Make the point.
- Don't open with a sweeping contextual statement about the state of the world.
  Don't close with a summary or an inspirational wrap-up. Start and end on
  substance.
- Don't restate the question before answering it.

**Style.**
- Use contractions.
- **Maximum one em dash per piece.** A series marker in the hook (`Part 4/12 — …`)
  spends that allowance, so a series body runs at zero. Use commas or
  parentheses.
- No preamble, no performative enthusiasm ("exciting", "incredible",
  "powerful"), no unsolicited caveats.

**The contrarian reframe — the fingerprint, and the way it goes wrong.** Name
the wrong approach *briefly*, then spend the majority on the better path.
Business outcomes land last, not first. A draft that spends half its length on
what everyone else gets wrong is a complaint, not a point of view.

**Anchor the take.** A thought-leadership piece names a real number, a real
company, or a real finding. Data-backed pieces outperform opinion-only pieces
by a margin large enough that this is a rule, not a preference. Emails, client
updates and DMs are exempt — apply judgment there.

**Before returning a draft, check three things:**
1. Read it aloud. Does any sentence sound like a press release? Rewrite it.
2. Are you making the same point twice in different words? Say it once.
3. Does the opening sentence set the scene with a grand statement? Delete it
   and start with the second sentence.

**What this buys and doesn't.** It removes the most-flagged markers and makes
the writing better. It does **not** make generated text pass an AI detector —
that was tested, and it failed. Never claim otherwise to the approver.

---

## Steps

### 1. Load the prompt stack — in this order

**a. Frame.** `../knowledge/business-profile.md` (what the business is, who it
serves, what it sells) · `agents/cmo/config/positioning-statement.md` ·
`agents/cmo/config/anti-patterns.md`. Read the profile fresh every run; a
writer that can't say what the business does will write something that sounds
professional and means nothing.

**b. Voice.** `voice/guide.md` in full — the use list, the never-use list, the
fingerprint. Then **3 samples** from `voice/samples/{register}.md`, preferring
any the guide marks as exemplars. Inject as: *"Write like this — in voice and
rhythm, not in content."*

**c. Archetype.** The structural instruction, word-count target, and the
succeeds-when / fails-when pair from §Archetypes below.

**d. Channel.** `config/channels/{channel}.md` — format limits, hashtag and
mention conventions, what works on this channel. Read it; don't carry another
channel's habits across.

**e. Series, if `series` is set.** `content/series/series-{slug}.md` — the arc,
the position, the marker convention, what the previous instalment already said.
A series instalment that repeats its predecessor is the most common series
failure.

**f. Source material — raw, never pre-digested.** Pass the content of the proof
entry, decision, or notes directly. Don't summarize it; summarizing is where
the specific detail that makes the piece worth reading gets sanded off.

**g. Caller notes.** `notes_from_caller`, verbatim.

### 2. Pass 1 — draft (`generation` tier)

Instruction:

```
Produce a {register} draft for {channel} using the {archetype} archetype.
Write in the business's voice. Use the source material as evidence, not as
the point. Produce: hook, body, close{, CTA if include_cta}.
Do not pad to hit the length. Do not rush to cut.
Return your reasoning for the structure you chose.

Bullets: numbered for sequences, rankings and ordered steps; unnumbered for
parallel items with no order dependency. Never bullet prose that reads better
as sentences. A reader skimming the bullets alone should get the substance.

Formatting — assume no markdown renderer unless the channel playbook says
otherwise:
- No `#` headers. No `[text](url)` links. Neither has a plain-text fallback;
  both publish as literal broken punctuation. Write the URL, or say it in words.
- **bold** / _italic_ only where a single short phrase needs emphasis a
  sentence break can't give it, never as decoration. Whether the ship path
  converts them to Unicode styling is stated in the channel playbook; if the
  playbook is silent, assume it does not and avoid them.
- Bullets and arrows are literal characters ("•", "-", "→"), not list
  constructs waiting for a renderer. "1. " typed literally is fine.
```

Return structured JSON: `{ hook, body, close, cta, full_text, reasoning,
source_refs, hashtags }`.

### 3. Pass 2 — critique (`reasoning` tier)

A separate call, eight criteria, each `pass` or `fail: one line saying what's
wrong and why`.

1. **depth_specificity** — could only someone with this business's actual depth
   have written it? A draft anyone in the category could have published is a
   fail.
2. **evidence_not_subject** — does it lead with the decision or the insight and
   use the detail as evidence, rather than making the detail the subject?
3. **anti_patterns** — does it avoid every anti-pattern in
   `agents/cmo/config/anti-patterns.md`?
4. **hook_strength** — is the hook strong enough that someone scrolling stops?
5. **close_quality** — does the close land, or does it trail off?
6. **house_style** — banned words, banned phrases, banned structures, the
   one-em-dash cap, the "Term. Explanation." bullet format. Mechanical; check
   it mechanically.
7. **client_naming** — scan `hook`, `body`, `close`, `full_text`, `reasoning`,
   `critique_notes` and `source_refs` for any name in
   `naming_rules.never_name`. **Any match is an automatic critical failure**
   regardless of how everything else scores. This is a confidentiality rule,
   not a style preference.
8. **no_broken_markup** — any `#` header or `[text](url)` link in `full_text`
   is a **critical failure**: no fallback exists and it publishes broken. Bold
   and italic are not a failure here, but flag them as a note when they appear
   more than once or twice, or on more than a short phrase.

Return `{ criteria: {...}, critical_failures: N, summary: "..." }`.

### 4. Pass 3 — conditional regeneration

- **0 critical failures** → return draft + critique. Done.
- **1 critical failure** → regenerate **once**, with the critique as extra
  input: *"The critique found one issue: {criterion}. Fix it. Do not change
  what isn't broken."* Return the regenerated draft + its critique.
- **2 or more** → **do not regenerate.** Return the original with the critique
  attached and stop code `critique_failed`. Two independent failures usually
  means the source material is wrong, and a second draft off the same wrong
  material costs a cycle to learn the same thing. The caller decides: different
  material, or drop the piece.

### 5. The visual — same pass, never a follow-up

For any channel whose playbook declares a visual, produce the visual **in the
same run that writes the draft.** Never queue it as a later step: a draft with
a promised-but-absent image is the exact artifact that reaches the approver as
a decision they can't make.

**Carousel archetype** → `$MKT_DEPT/skills/render-carousel/SKILL.md`.

**Single image** → the renderer named in `config/channels/{channel}.md` →
`image_renderer`, if the instance registered one.

**No renderer registered** → write `image: none` and an `image_note` giving the
reason. Do not leave both absent: content-reviewer's image gate blocks a piece
that has neither an image nor a declaration, precisely so "we forgot" and "we
decided" stop looking identical.

Craft rules that transfer regardless of which renderer runs:

- **Fit, don't clip.** Size the copy to the renderer's budget *before*
  rendering. Overrun typically overlaps the footer silently instead of
  erroring, so a clean exit code proves nothing.
- **Eyeball the rendered file.** Clipping, a unit error in a label, a currency
  symbol hardcoded to the wrong one, and the wrong post's content are all
  invisible to an exit code and obvious to an eye. This is not optional.
- **Rotate the layout.** Record which layout was used in `image_format` so the
  next piece can avoid repeating it. Five shapes cover almost everything:
  `chart` (2–5 ranked comparable numbers) · `flow` (a 3–4 step sequence) ·
  `versus` (opens by naming a wrong take) · `statement` (one declarative frame,
  no data) · `poster` (a claim plus 2–3 supports). **Never pad one number into
  a fake chart.** Never run the same layout twice in a row unless nothing else
  genuinely fits.
- **Match the slug.** The image filename uses the draft's own slug. A mismatch
  orphans the file and breaks every surface that resolves a piece's visual by
  slug.

On success write `image_path` and `image_format`. On failure write **neither**
and flag for review — a dangling `image_path` is worse than none.

### 6. Channel conventions

Hashtags, mentions and any @-handle rules come from
`config/channels/{channel}.md`, not from this skill and not from habit. What a
playbook should be specifying, from what has actually held up:

- 3–5 hashtags on channels that reward them, appended after a blank line at the
  end of `full_text`. **More than 5 dilutes reach.**
- 1–2 stable brand tags plus 2–3 topic tags per piece; rotate the brand tags
  rather than stacking the whole pool.
- Never generic filler (`#Success`, `#Growth`, `#Motivation`).
- A running series carries its own tag on every instalment.
- Some channels punish hashtags outright — see x-content-writer. Never copy a
  hashtag rule across channels by reflex.

### 7. Write the file

`content/drafts/{YYYY-MM-DD}-{archetype}-{slug}.md`, where the date is the
**planned publish date**, not today. If that filename already exists for a
different channel, append the channel to the slug.

---

## Draft frontmatter — the contract downstream ships dispatch on

Every draft carries this block. The ship skills read these fields, so a missing
one is a broken deliverable, not an untidy one.

```yaml
---
kind: content-draft
channel: linkedin                 # a channel registered in config/config.yaml
register: long-form-post          # names a real voice/samples/{register}.md
format: post                      # post | carousel | article | email | dm
archetype: case-study             # teardown|case-study|pov|frame-shift|data-insight|carousel|raw
slug: pilot-to-production-handoff
planned_date: 2026-09-03          # the intended publish date; equals the filename date
status: draft                     # draft | ready-to-send | approved | shipped
series: onboarding-teardowns      # omit when not part of a series
series_position: "4/12"           # omit when not part of a series
source_refs:
  - proof/case-studies/{slug}.md
  - content/topic-bank.md#{entry-id}
include_cta: false
cta_style: ""                     # present only when include_cta is true
voice_sample_count: 12
below_voice_floor: false
critique_notes: "{summary from the critique pass}"
# --- visual: exactly one of the three variants, or the declaration ---
image_path: content/images/{slug}.png
image_format: chart               # chart|flow|versus|statement|poster|carousel
# carousel archetype adds:
#   carousel_pdf: content/carousels/{slug}/carousel.pdf   <- this is what publishes
#   slide_paths: [ ... ordered PNGs ... ]                 <- the multi-image fallback
#   image_format: carousel
#   image_path: {slide 1 PNG}                             <- the approval-surface preview
# declared text-only instead:
#   image: none
#   image_note: "no renderer registered for this channel"
created_at: 2026-08-29T18:04:11Z
created_by: content-writer
---
```

**`status` values are exactly the stage folder names**, so a piece's field and
its location can be compared without a lookup table. Where they disagree the
field wins — except in `content/shipped/`, which is terminal: a published piece
must never reappear as work because its frontmatter went stale.

One value sits outside the progression: **`needs_attention`** parks a piece and
makes it unselectable by every downstream skill. No skill in this port writes
it — it exists so a human or an instance-specific pass can take a piece out of
the flow without deleting it, and so a parked piece can never be selected for
publishing by a folder scan.

**On the carousel triple:** `carousel_pdf` is what publishes, as a real
swipeable document. `slide_paths` is the fallback if the document path fails —
list the PNGs explicitly rather than globbing, because page-extraction tools
don't reliably zero-pad. `image_path` set to slide 1 exists so the approval
surface can show something; without it the approver is approving a carousel
blind. It never causes a single-image publish, because a ship skill checks
`slide_paths` first.

---

## Archetypes

### teardown — "here's what's actually happening under the hood"
Hook (specific) → the common misunderstanding → the reality → the implication.
**150–250 words.** Succeeds when the reality surprises someone who thought they
knew. Fails when the "reality" is obvious or the hook is abstract. Reads as
critique — use it sparingly.

### case-study — "here's what we built and what happened"
The situation → the approach → what worked and what broke → the lesson.
**180–300 words.** Succeeds when it opens with the decision rather than the
architecture, and names at least one thing that broke or surprised. Fails when
it reads as a success story with no friction. Naming rules apply in full.

### pov — "here's what we actually think"
The take (sharp, specific) → why most people believe the opposite → why they're
wrong → the implication. **120–200 words.** Succeeds when the take is specific
enough that someone could disagree with it. Fails when it's hedged ("it
depends") or the counter-case is a strawman.

### frame-shift — "here's a useful way to think about this"
The frame → why it helps → how to apply it. **100–180 words.** Succeeds when
the frame is memorable, often a comparison, and applied to something specific.
Fails when the application section is "it depends."

### data-insight — "here's what the data shows, and what it means"
An external finding, specific and cited where possible → what it means for the
reader → the business's own angle that confirms or extends it → the practical
implication. **150–250 words.** The **hook is the number itself** — never "I
read a study that…". The angle must connect specifically to the data, not just
agree with it. Record the source in `source_refs` even when it isn't cited
inline. This is the most shareable archetype because it hands readers something
concrete to reference. Fails when it's a stat with a comment stapled on.

### carousel — "one idea, unpacked slide by slide"
A multi-page document post. **Frequency follows the material, not a quota.**

Hook slide → one idea per slide (4–7 content slides) → close slide (takeaway,
optional CTA). **6–9 slides, ≤ 30 words per slide** — carousels are read at
swipe speed and a slide needing a re-read is overweight. The commentary above
the document stays **50–120 words**: hook, why to swipe, tags. The slides carry
the substance; the commentary sells the swipe.

**Decide before drafting: is this actually a carousel?** The full selection
rule lives in `$MKT_DEPT/skills/render-carousel/SKILL.md`. The one-line
version: **does every slide earn its own swipe?** A padded carousel
underperforms a good single image. Never promote a piece to a carousel because
the format performs well on average.

**Mark the emphasis as you write** — an accent word in each slide's headline
and marked spans in the body. A deck with neither reads as a wall of flat ink
next to a single-image post. A renderer's automatic emphasis rule is a floor,
not a substitute for choosing the word.

Watch two failure shapes. Slides that are paragraphs pasted onto images. And a
normal post chopped into pieces with no per-slide payoff — the second is what
happens when a carousel is built out of one repeated square layout, and it is
why a dedicated renderer with real per-slide archetypes exists. Also keep
format variety in the surrounding run: an unbroken sequence of document posts
is what templated-content downranking is built to catch.

### raw — no archetype
Full flexibility for the caller, who supplies structure through
`notes_from_caller`. Voice, house style and every mechanical rule still apply.
No default word count — the caller sets `max_length_words`.

---

## Outputs

| Artifact | Purpose |
|---|---|
| `content/drafts/{YYYY-MM-DD}-{archetype}-{slug}.md` | The draft plus the full frontmatter contract |
| `content/images/{slug}.png` | The single image, when a renderer is registered |
| `content/carousels/{slug}/` | `slides/*.png` + `carousel.pdf` + the spec, for the carousel archetype |
| Structured return to the caller | `hook`, `body`, `close`, `cta`, `full_text`, `reasoning`, `critique_notes`, `source_refs` |

A draft is a **consequential** artifact — content written for external
publication under the business's name. It sits in `content/drafts/` until
content-reviewer and then the approver's M2 move it. **Its existence is not
approval, and silence is not approval.**

---

## Trace

`traces/content-writer-{run-id}.json` — channel, register, archetype, slug,
`voice_sample_count`, `below_voice_floor`, critical-failure count, whether a
regeneration ran, visual variant written, stop code if any.

---

## Stop codes

| Code | When | What the caller does |
|---|---|---|
| `mode_halt` | `MODE` is sabbath/retreat/quiet | Nothing. Exit silently; cron keeps firing. |
| `channel_not_live` | Channel is at `c0` | Drop the piece, or raise M3 to move the channel up a tier. |
| `brief_incomplete` | Missing channel, register or archetype | Fix the brief. Never guess a register. |
| `no_source_material` | Every `source_material` field null | Substitute material from the topic bank, or drop the piece. |
| `no_voice_reference` | No samples **and** no `voice/guide.md` | Seed the voice corpus. One notify, then stop asking. |
| `critique_failed` | 2+ critical failures in Pass 2 | Retry with different source material, or drop. Do not re-run on the same material. |
| `render_failed` | The visual didn't render | Draft is kept, `image_path` unwritten. Fix the renderer or declare `image: none`. |

`below_voice_floor` is **not** a stop code. It is a stamped frontmatter field
and a warning that travels with the piece.

---

## Failure modes to avoid

- **Redacting after drafting.** Anonymize in the prompt or the name survives in
  a field nobody re-reads.
- **Queuing the visual for later.** Same pass, always. A draft the approver
  can't see is a decision they can't make.
- **Trusting a clean exit code on a render.** Look at the file.
- **Writing to the voice corpus.** Only published pieces become samples, and
  only after they publish.
- **Padding to a word count.** The ranges are targets, not quotas. A 140-word
  pov that lands beats a 200-word one that repeats itself.
- **Regenerating twice.** One regeneration on one failure. Two failures is a
  material problem, and a third draft learns nothing new.
- **Carrying another channel's conventions across.** Hashtags help on one
  channel and read as spam on another. The playbook decides.
