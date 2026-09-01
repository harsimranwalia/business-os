# Anti-Patterns — TEMPLATE

**This is a template, and it is the one that ships closest to usable.** Most of
what follows is platform physics and craft, and transfers to any business
unchanged. The parts that do not — the client-naming rules, and anything in
"Business-specific blocks" — are marked and must be filled in before the first
publishing run. The live copy lives at
`$MKT_INSTANCE/agents/cmo/config/anti-patterns.md`.

**Who reads this and what happens.** The content writer refuses to produce a
piece containing a hard block. The review pass (`skills/content-reviewer/`)
treats a hard block as a **critical failure**, not a style flag. The CMO's
biweekly positioning audit catches anything that slipped through. Only the CMO
edits this file.

---

## Hard blocks — never, under any circumstances

**Naming a client without confirmed permission.** _[Fill in per business.]_ The
CMO's `config.yaml` → `naming_rules` holds the machine-readable list:
`never_name` (with the substitute phrasing to use instead) and
`ok_to_name_with_public_metrics`. Default to anonymized framing for anyone not
on the permitted list, and note the second half of the rule that gets missed: a
name being permitted does not make a private metric publishable.

This block exists because a shipped piece once named a client that was never to
be named, and the writer had nothing to check against. The lesson was not "be
more careful" — it was that a naming rule has to live somewhere a review pass
can mechanically read. A paraphrase specific enough to identify them is the
same leak with extra steps.

**Opinion with no anchor.** Every piece needs a real number, a real project, or
a real observation as evidence. A take with nothing under it is noise, and it is
the single most common thing a language model will produce if you let it.

**Contrarian framing as the default structure.** Opening every piece with "here's
what everyone gets wrong about X" or equivalent. Occasional and specific is
fine; structural is a negative identity, and a feed of it reads as someone who
is against things for a living.

**Inventing a metric.** A baseline exists when the data exists. "Unknown —
pending collection" is a valid line; a plausible number is a fabrication that
will be quoted back later.

**Business-specific blocks.** _[Fill in. Regulatory language, claims the
business may not make, competitor references, anything legal has ruled on.
`../knowledge/claims-allowed.md`, where the instance keeps one, belongs here by
reference.]_

## The generic-content list

These are refusals, not preferences. Each one is a tell that the draft was
generated rather than written.

- "In today's fast-paced world" and every relative of it
- Listicles: "7 ways to X", "5 things I learned about Y"
- Decorative emoji strings (one or two contextual emoji are fine)
- "DM me to learn more" as a call to action
- Trend commentary with no specific angle from this business's own experience
- Three consecutive sentences opening with the same word
- "Game-changer", "leverage" as a verb, "dive in", "unpack", "delve"
- Copy that is smooth, correct and hollow — the register of a paraphraser
- A humblebrag wearing a lesson as a disguise
- Vague inspiration: a claim about the future with nothing specific in it
- "Here's what most people get wrong about X" when the answer is obvious
- Ending on a question any answer could answer ("What do you think?")
- The hook + ten one-line bullets + CTA skeleton
- A thread pretending to be one piece — if it needs two, it is not ready
- Posting about posting

## Positioning violations — flags drift, does not auto-reject

These do not block a draft. They are what the biweekly audit counts, and a
pattern of them is a finding worth a report line.

- Leading with what was built instead of the decision or the outcome
- Generic advice with no angle specific to what this business does
- Any price or offer mention in body copy — the CTA file owns that surface
- Comparisons to named competitors that make the business sound reactive
- Hedged takes: "it depends", "there's no one-size-fits-all", with no claim
- Advice about the platform itself, unless that is genuinely the business

## Structural uniformity — the ranking risk

**Keep this section. It is platform physics, and it is the least obvious thing
in this file.**

Major platforms began downranking content their classifiers read as templated
or automated in 2026, and added user-facing "this looks AI-generated" reporting
controls. Independent analysis has measured a large fraction of long-form social
posts as fully machine-generated. The exposure for a department like this one is
**not substance** — its pieces carry real projects and real numbers. It is
**form**: the same skeleton repeating across one author's corpus.

This was caught on a 31-post series where every post shared an identical opener
prefix, one bullet glyph throughout, the same one-word closing label on 27 of
31, and exactly four hashtags on 26 of 31. Individually invisible. Across a
corpus, a signature.

Across any batch or series, these must vary piece to piece:

- **Bullet glyph** — rotate. Never one glyph across a whole series. Avoid using
  an em-dash as a bullet where the prose is already em-dash heavy; a
  line-leading dash collides with the in-sentence ones and reads muddy.
- **The closing move** — vary the label *and* the structure. Never repeat one
  token across a batch. Mix unlabelled final paragraphs, a question, an
  imperative, and varied labels.
- **Hashtag count** — vary it. A fixed count every time is a signature by
  itself.
- **Length** — let it range. Six pieces all landing within a hundred characters
  of each other is a tell.

**What must stay identical is only deliberate series identity** — a stage
marker, an anchor hashtag. That is a reader-facing wayfinding device and it is
the approver's call. Do not "fix" it.

**Scope of this rule — read it before promising more than it delivers.**
Varying structure addresses the **ranking** signal. It does **not** defeat AI
**detection**. This was tested: after both a de-templatizing pass and a full
humanizing rewrite — em-dashes cut, sentence length forced to vary, specifics
added — every sampled piece still scored as machine-written. Detectors classify
the statistical signature of the text, not its formatting.

So do these variations because uniform output is genuinely worse content and
plausibly worse for reach. **Never tell the approver that a rewrite pass will
move a detector score.** It will not, and the claim is the kind of thing that
gets believed once and remembered forever.

---

## Adding to this file

An entry earns its place by having been **observed**, not imagined. The best
entries in any instance's copy will be the ones added the day after something
went out wrong, with the incident in one line beside the rule.

Say what happened. "X, because Y happened" survives a re-read six months later;
"do X" gets quietly relaxed by whoever finds it inconvenient.
