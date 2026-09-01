# Skill: x-content-writer

**Owner:** content-writer (the craft agent under the campaign strategist)
**Model:** `generation` tier for the draft pass, `reasoning` tier for the critique pass — the instance binds each tier to a model
**Trigger:** a per-piece brief whose `channel` resolves to a 280-character channel
**Suppressed when:** `MODE` is `sabbath`, `retreat`, or `quiet`; or the channel sits at autonomy tier `c0`

---

## Purpose

Stateless procedure that turns one brief into one X post — a single tweet or a
thread — in the business's voice. No memory, no strategy opinions.

## Why this is a separate skill and not a `register` on content-writer

Because a 280-character weighted unit is a different craft, not the same craft
with a smaller number. Four things are procedurally different, and folding them
into content-writer would mean putting four conditionals through logic that has
nothing else to do with them:

1. **A hard mechanical limit that must be counted, not judged.** Long-form
   drafting has word-count *targets*; here, 281 weighted characters is a broken
   deliverable. And the count is weighted, not `len()` — see §Character
   counting. A language model cannot be trusted to do this arithmetic, so the
   check is a deterministic pass, not a critique criterion.
2. **The hook has to earn a click.** A feed post is fully visible when someone
   scrolls past it; the rest of a thread is not. The first tweet is doing a job
   the first line of a long-form post never has to do.
3. **A multi-tweet arc instead of a single body.** Each unit must stand alone
   *and* advance the sequence. Long-form structure has no equivalent constraint.
4. **No per-piece visual pass, and the opposite convention on tags.** Threads
   ship as text. Hashtags help on feed channels and read as spam here.

---

## Paths

Bare paths are **instance-relative** (`$MKT_INSTANCE`). Paths prefixed
`$MKT_DEPT` are template-side and read-only at runtime.

---

## Publishing reality — read before scheduling this

This skill produces drafts. Whether they go anywhere is the channel's autonomy
tier and its publishing method, not this skill's business:

- At **`c1`** there is a draft path and no publishing path. That is a legitimate
  state to start in and **not a resting place** — a draft with nowhere to go is
  a dead end, so a channel at `c1` needs a live reason and a date
  (`conventions.yaml` → `channel_autonomy`). Invoke this skill on explicit
  briefs only while a channel is at `c1`; do not schedule it, or drafts pile up
  against a wall.
- At **`c2`** `$MKT_DEPT/skills/ship-content-x/SKILL.md` publishes approved
  pieces, one per publishing day, after the approver's M2.
- The publishing method lives in `config/config.yaml` and the channel playbook.
  A `browser` method cannot run headless and needs a live logged-in session on
  a machine someone maintains. That is a real operational cost and belongs in
  the playbook, not discovered on the first failed run.

---

## Interface

**Inputs:**

```
channel:  string                 — the registered 280-character channel
format:   'tweet' | 'thread'
archetype: 'data-insight' | 'case-study' | 'pov' | 'frame-shift' | 'teardown' | 'raw'
source_material:                 — at least one field non-null
  proof_ref?:     string         — slug in proof/case-studies/ or proof/internal/
  eng_proof_ref?: string         — entry under ../engineering/reports/proof/
  topic_ref?:     string         — an entry id in content/topic-bank.md
  decision_ref?:  string
  free_form?:     string
max_tweets?: number              — thread only; default 7, hard cap 12
include_cta?: boolean            — default false
cta_style?:  string
series?:     string              — slug of a plan in content/series/
notes_from_caller?: string
revision_target?:
  existing_draft_path: string    — a draft in content/drafts/
  reviewer_notes:      string
```

**When `revision_target` is present:** revise in place. Read `channel`,
`format`, `archetype`, `series` and `source_refs` from the draft's own
frontmatter. Preserve every frontmatter field except the content, and **never
touch `status`**. Apply `reviewer_notes` as targeted edits, not a rewrite. If a
note requires cutting a tweet to fit, **cut words — never truncate mid-word or
mid-sentence.** Re-run the deterministic count and the critique against the
revision, same as a fresh draft.

**Outputs:**

```
hook_tweet:  string              — the standalone hook; identical to tweets[0].text
tweets:      [ { n, text, weighted_chars } ]   — in order; format 'tweet' has exactly one
full_text:   string              — the thread rendered with "n/total" numbering,
                                   FOR HUMAN REVIEW ONLY (see §Numbering)
reasoning:      string
critique_notes: string
source_refs:    string[]
```

---

## Pre-flight

### 1. Mode
`.env` → `MODE`. `sabbath` / `retreat` / `quiet` → exit without writing.
Stop code `mode_halt`.

### 2. Channel autonomy
`c0` → exit, `channel_not_live`. `c1` and above → draft.

### 3. Source material
At least one field non-null, else `no_source_material`. This skill does not go
looking for something to write about.

### 4. Naming rules
Identical to the sibling skill — see
`$MKT_DEPT/skills/content-writer/SKILL.md` § Pre-flight 6. Read
`config/config.yaml` → `naming_rules`; **default to anonymizing every named
client** when the instance declares none; substitute the anonymized form **in
the prompt before Pass 1**, never by redacting afterwards; and apply it to
`reasoning`, `critique_notes` and `source_refs` too, not just the tweets.

### 5. Input sanity
`max_tweets` > 12 → clamp to 12 and say so in `reasoning`. Don't error, don't
silently drop it. `format: 'tweet'` with `max_tweets` present → ignore it
(thread-only field) and note it in `reasoning` if it was non-default.

### 6. There is deliberately **no voice-floor pre-flight here**

Read the next section before treating that as an oversight.

---

## The voice asymmetry — deliberate, and it has a cost

`$MKT_DEPT/skills/content-writer/SKILL.md` counts the samples in
`voice/samples/{register}.md` and stamps `voice_sample_count` and
`below_voice_floor` on every draft, against a floor of 10
(`conventions.yaml` → `voice.floor`). **This skill has no such pre-flight, on
purpose**, and the reason is structural: a fresh instance has no short-form
corpus at all. The corpus grows only from pieces the approver actually
published, and a channel that has published nothing has nothing to grow from.
A floor check here would fail every fresh instance on its first run and teach
everyone to skip it.

**What this skill does instead:**

- Borrow **2–3 samples from `voice/samples/long-form-post.md`** (or whichever
  long-form register the instance seeded) for **tone and fingerprint only** —
  sentence length, no passive voice, no corporate-speak, no reflexive hedging,
  the contrarian reframe. Inject them explicitly framed:

  > *"Write like this in voice — but compress hard into 280-character units. Do
  > not carry over paragraph-length rhythm, paragraph-length setup, or the
  > long-form opening. The shape is not transferable; only the voice is."*

- Read `voice/guide.md` in full. The guide is register-independent and is the
  real floor here.
- **Never** use long-form samples as evidence of post *shape*. A thread written
  to the rhythm of a feed post is the specific failure this framing exists to
  prevent.

**The cost, stated plainly:** the channel with the least voice data has the
least voice protection. A long-form draft is checked against ten real examples
of how the business actually sounds in that shape; an X draft is checked
against a description and a borrowed rhythm. **So the review pass and the
approver's M2 carry more weight on this channel than on any other.**
content-reviewer should treat `voice_borrowed: true` as a reason to look harder
at voice, not as a note. Do not quietly equalise this by inventing a floor that
would block every new instance, and do not pretend the gap isn't there.

**How the asymmetry ends:** the moment `voice/samples/{register}.md` for this
channel's own register holds **3 or more** real published samples, use those
and stop borrowing. Stamp `voice_borrowed: false` and the real
`voice_sample_count`. At 10 it is a normal register like any other. That is the
intended path, and it is why the field is stamped on every draft rather than
being inferred later.

---

## House style

The base rules are the sibling skill's — see
`$MKT_DEPT/skills/content-writer/SKILL.md` § House style. The banned words,
banned phrases and banned structures lists are **identical and apply here
without exception.**

**One deliberate difference: zero em dashes, not one.** The sibling's
one-per-piece allowance exists only to cover a series marker in a hook, which
has no equivalent in a 280-character unit. Use a comma, a period, or
restructure.

**X-specific hard rules:**

- **280 weighted characters per tweet, maximum.** Not a style note — an
  over-limit tweet is a broken deliverable and must not be returned. See
  §Character counting.
- **No hashtags.** They read as spam here. This is the opposite of the feed
  channels' convention and must not be copied across by habit.
- **No engagement bait.** No "RT if you agree", no "follow for more", no "reply
  below", no poll bait.
- **The hook tweet stands alone.** It earns the click on its own merits — a
  real claim, a number, an observation. Never "a thread 🧵" or any variant of
  announcing that a thread follows *instead of* starting it.
- **Every tweet carries value on its own.** Someone landing mid-thread from a
  quote-post or a screenshot must get something real from that one tweet, not a
  fragment that only parses in sequence.
- **Links go in the final tweet only, never the hook.** A hook with a link
  reads as an ad, not a thought.
- **Anchor the take** in a real number, a real company, or a real finding. No
  invented metrics. No claims about the content's own performance — that is the
  caller's domain, not the draft's.

---

## Character counting

X does **not** count `len(text)`. It computes a *weighted* length, and the
difference is large enough to break a deliverable that looked fine.

**The rule:**

1. **Base weight 2** for every Unicode code point, **except** code points in
   `U+0000–U+10FF`, `U+2000–U+200D`, `U+2010–U+201F`, `U+2032–U+2037`, which
   weigh **1**. In practice: Latin, Latin-1, Greek, Cyrillic, Hebrew, Arabic
   and common punctuation weigh 1; **CJK, Japanese kana, Hangul and emoji weigh
   2.**
2. **Every emoji counts as one unit of weight 2**, including sequences joined
   with zero-width joiners and those carrying skin-tone modifiers.
3. **Every `http(s)://` URL counts as exactly 23**, regardless of its literal
   length — X shortens every link through its own wrapper. **This applies to
   short links too:** a 12-character URL still costs 23. Assuming the
   adjustment can only *reduce* a count is wrong and under-counts every short
   link.
4. The limit is **weighted length ≤ 280**.

**Count every tweet, always, including ones that look obviously short**, and
record the result in `weighted_chars`. This is arithmetic, not judgment.

A reference implementation, deliberately conservative:

```python
import re
URL = re.compile(r'https?://\S+')

def weight(cp: str) -> int:
    o = ord(cp)
    if o <= 0x10FF or 0x2000 <= o <= 0x200D or 0x2010 <= o <= 0x201F or 0x2032 <= o <= 0x2037:
        return 1
    return 2

def weighted_len(text: str) -> int:
    stripped = URL.sub('', text)
    n_urls = len(URL.findall(text))
    return sum(weight(c) for c in stripped) + 23 * n_urls
```

This over-counts a multi-code-point emoji sequence (each component code point
weighs 2 rather than the sequence as a whole weighing 2). **Over-counting is
the safe direction** — it can only make a tweet shorter than it needed to be,
never publish one that is rejected. Keep it that way unless the instance adds a
real grapheme-aware counter.

---

## Numbering

Tweets in `tweets[]` carry **no** baked-in "1/7" marker by default. The
reply-chain UI already shows thread order, and a visible counter spends
character budget without adding content, which cuts directly against "every
tweet stands alone."

`full_text` adds "n/total" numbering purely so a human can read the whole thread
as one document before approving. **It is not necessarily what gets posted** —
the ship skill posts `tweets[]`.

If a specific thread genuinely benefits from visible position markers (a long
teardown where sequence matters), that is a per-thread call driven by
`notes_from_caller`, not the default. When chosen, the marker is baked into
`tweets[]` itself and **counted toward that tweet's 280**, never bolted on
afterwards.

---

## Steps

### 1. Load the prompt stack

**a. Frame.** `../knowledge/business-profile.md` ·
`agents/cmo/config/positioning-statement.md` · `agents/cmo/config/anti-patterns.md`.

**b. Voice.** `voice/guide.md` in full, plus the borrowed or native samples per
§The voice asymmetry, with the compression framing quoted verbatim.

**c. Archetype and arc.** §Archetypes and §Thread arc below, plus the target
tweet count.

**d. Channel.** `config/channels/{channel}.md` — limits, publishing method,
what works here.

**e. Series**, if set: `content/series/series-{slug}.md`.

**f. Source material — raw, never pre-digested.**

**g. Caller notes**, verbatim.

### 2. Pass 1 — draft (`generation` tier)

```
Produce X content using the {archetype} archetype, format: {format}.
Write in the business's voice, compressed to X's per-tweet discipline.

format 'thread': the hook tweet stands completely alone and earns the click.
Follow the thread arc — brief tension or wrong approach, then the majority of
the thread on the better path, a concrete outcome near the end, an optional
close or CTA last. Target {max_tweets or 7} tweets, never exceed 12. Every
tweet must carry value read in isolation.

format 'tweet': one tweet, the entire deliverable, complete and self-sufficient
— not a teaser for something else.

No hashtags. No engagement bait. A link, if any, goes in the final tweet only,
never the hook. Zero em dashes.

Estimate a character count per tweet, but do not rely on it — it will be
recomputed mechanically and yours will be overwritten.

Return your reasoning for the structure you chose.
```

Return JSON: `{ hook_tweet, tweets: [{n, text, weighted_chars}], full_text,
reasoning, source_refs }`.

### 3. Pass 1b — deterministic count (not model judgment)

Self-reported character counts are not trustworthy enough to gate a hard limit.
Recompute **every** tweet with the §Character counting formula, overwriting
whatever Pass 1 reported. If any tweet exceeds 280:

- **Do not proceed to critique** with an over-limit tweet quietly marked fine.
- Feed the offending tweets into a targeted rewrite: cut words to fit; never
  truncate mid-word or mid-sentence; never drop the tweet's point to save
  characters. Re-count after the rewrite.
- Repeat at most **twice**. If two rewrites both fail, stop with
  `cannot_fit_character_limit` and the offending tweet number. A third attempt
  is the same attempt.

Also verify `hook_tweet` is byte-identical to `tweets[0].text`. They are the
same string in two places, and a divergence means one of them is stale.

### 4. Pass 2 — critique (`reasoning` tier)

Seven criteria, each `pass` or `fail: one line`:

1. **hook_strength** — does the hook stand alone and earn the click, with no
   "a thread" throat-clearing?
2. **standalone_value** — does every tweet carry real value read in isolation?
3. **character_limits** — is every tweet ≤ 280 by the Pass 1b count?
4. **thread_arc** — is the tension brief, does the majority sit on the better
   path, does a concrete outcome land near the end? (N/A for `format: tweet`.)
5. **x_hygiene** — no hashtags, no engagement bait, links only in the final
   tweet, zero em dashes?
6. **client_naming** — do `hook_tweet`, `tweets`, `full_text`, `reasoning`,
   `critique_notes` and `source_refs` avoid every name in
   `naming_rules.never_name`?
7. **anti_patterns** — does it avoid every anti-pattern in
   `agents/cmo/config/anti-patterns.md`, and every banned word, phrase and
   structure in the house style?

**`character_limits` and `client_naming` are automatic critical failures**
regardless of how the other five score. One is a hard mechanical break, the
other a confidentiality rule. Neither is a style preference.

### 5. Pass 3 — conditional regeneration

- **0 critical failures** → return draft + critique. Done.
- **1** → regenerate once: *"The critique found one issue: {criterion}. Fix it.
  Do not change what isn't broken. If it's a character overage, cut words —
  never truncate mid-word or mid-sentence."* **Re-run Pass 1b on the
  regenerated draft** before returning.
- **2 or more** → do not regenerate. Return the original with the critique
  attached and stop code `critique_failed`. The caller decides: different
  source material, or drop the piece.

### 6. Write the file

`content/drafts/{YYYY-MM-DD}-{archetype}-{slug}.md`, the date being the planned
publish date. **Same filename convention as every other piece** — the channel
lives in the frontmatter, not in the filename, because ship skills dispatch on
fields. If the name collides with a piece on another channel, append the
channel to the slug.

---

## Thread arc

The skeleton for every `format: thread` draft on a non-`raw` archetype:

**hook → brief tension / the wrong approach → the better path (the majority of
the thread) → concrete outcome → optional close or CTA**

This is the same contrarian-reframe fingerprint the house style requires, at
sharper compression: *brief* means **one tweet**, not a paragraph, and "the
better path" claims most of the remaining budget. A thread that spends four of
seven tweets on what everyone gets wrong is a complaint.

`format: tweet` has no arc. One tweet carries the whole idea, dense and
complete.

---

## Archetypes

### data-insight
Hook: **the number or finding itself**, never "I read a study that…". Body:
what it means for the reader, then the business's own angle that confirms or
extends it — specific, not agreement. Close: the practical implication.
Fails when it's a stat with a comment stapled on.

### case-study
Hook: the outcome or the decision, in one line — not the setup. Body: the
situation → the approach → what broke or surprised → the number. Naming rules
apply in full; anonymize before drafting, not after. Fails when it reads as a
success story with no friction.

### pov
Hook: the take, sharp enough that someone could disagree with it. One tweet of
tension (why most people believe the opposite). Body: why they're wrong — the
majority of the thread. Close: the implication. Fails when the take is hedged
or the counter-case is a strawman.

### frame-shift
Hook: the frame, stated compactly, often as a comparison. Body: why it helps,
how to apply it. Close: a concrete application, not a restatement. Fails when
the application is "it depends."

### teardown
Hook: the specific claim. One tweet of the common misunderstanding. Body: the
reality, broken across tweets. Close: the implication. Reads as critique — use
it sparingly.

### raw
No arc imposed. The caller supplies structure via `notes_from_caller`. Voice
and every mechanical rule still apply: the 280 limit, no hashtags, the hook
standing alone, zero em dashes. No default tweet count.

---

## Draft frontmatter

The **same contract** as every other piece — see
`$MKT_DEPT/skills/content-writer/SKILL.md` § Draft frontmatter — with the
X-specific fields added and the visual fields absent.

```yaml
---
kind: content-draft
channel: x
register: short-form-post
format: thread                  # tweet | thread
archetype: case-study
slug: migration-rollback-thread
planned_date: 2026-09-04
status: draft                   # draft | ready-to-send | approved | shipped (| needs_attention, parked)
series: onboarding-teardowns    # omit when not part of a series
series_position: "4/12"         # omit when not part of a series
tweet_count: 7
weighted_chars: [104, 231, 198, 240, 176, 212, 143]   # per tweet, in order, from Pass 1b
source_refs:
  - proof/internal/{slug}.md
include_cta: false
voice_borrowed: true            # borrowed long-form samples for tone (see the asymmetry)
voice_sample_count: 0           # samples in THIS register, not the borrowed ones
below_voice_floor: true
critique_notes: "{summary from the critique pass}"
image: none
image_note: "threads ship as text"
created_at: 2026-08-29T18:04:11Z
created_by: content-writer
---
```

**Body of the file, in this order:** `hook_tweet` · the ordered tweet list with
each tweet's `weighted_chars` shown inline · `full_text` (numbered, for review)
· `reasoning` · `critique_notes` · `source_refs`.

`image: none` is written explicitly rather than omitted, so content-reviewer's
image gate reads a decision instead of an absence.

---

## Outputs

| Artifact | Purpose |
|---|---|
| `content/drafts/{YYYY-MM-DD}-{archetype}-{slug}.md` | The draft, its frontmatter, and the tweet list |
| Structured return to the caller | `hook_tweet`, `tweets`, `full_text`, `reasoning`, `critique_notes`, `source_refs` |

A draft is a consequential artifact even when the channel has no publishing
path yet. It waits in `content/drafts/` for review and then M2. **Its existence
is not approval, and silence is not approval.**

---

## Trace

`traces/x-content-writer-{run-id}.json` — channel, format, archetype, slug,
tweet count, max weighted length, rewrite attempts in Pass 1b, `voice_borrowed`,
critical-failure count, stop code if any.

---

## Stop codes

| Code | When | What the caller does |
|---|---|---|
| `mode_halt` | `MODE` is sabbath/retreat/quiet | Nothing. Exit silently. |
| `channel_not_live` | Channel is at `c0` | Drop, or raise M3. |
| `no_source_material` | Every `source_material` field null | Substitute or drop. |
| `cannot_fit_character_limit` | Two rewrites failed to get a tweet under 280 | Split the thread, cut a tweet, or send different material. Returns the tweet number. |
| `critique_failed` | 2+ critical failures in Pass 2 | Different material, or drop. Never re-run on the same material. |
| `hook_desync` | `hook_tweet` ≠ `tweets[0].text` after Pass 1b | Internal bug — regenerate; never publish with both present and different. |

---

## Failure modes to avoid

- **Trusting a model's character count.** It is arithmetic. Compute it.
- **Truncating to fit.** Cut words. A tweet ending mid-sentence is worse than a
  tweet that says less.
- **Carrying long-form rhythm across.** The borrowed samples are for voice, not
  shape. This is the most likely failure of this whole skill.
- **Adding hashtags out of habit** from the feed channels.
- **A hook that announces a thread** rather than starting one.
- **Scheduling this skill while the channel is at `c1`.** Drafts with no
  publishing path accumulate into a queue nobody can drain.
- **Quietly equalising the voice asymmetry** by inventing a floor. It is
  labelled for a reason; the answer is to grow the corpus, not to hide the gap.
