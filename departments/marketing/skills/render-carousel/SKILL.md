# Skill: render-carousel

**Owner:** shared — invoked inline by the writer skill during draft creation
**Model:** none at runtime. The renderer is a deterministic subprocess; the
caller writes the spec at the generation tier and makes the selection call at
the reasoning tier.
**Trigger:** never scheduled. Invoked in the same pass as the piece, whenever the
chosen archetype is `carousel`.
**Suppressed when:** nothing — it writes only local assets and publishes nothing.

---

## Paths

Bare paths are **instance-relative** (`$MKT_INSTANCE`). Paths prefixed
`$MKT_DEPT` are template-side and read-only at runtime.

---

## Purpose

Turn a JSON spec into a **1080×1350 vector PDF plus one PNG per slide** — the
assets a document post needs.

**This skill only renders.** The caller makes the selection call, writes the
spec, eyeballs the output, and writes the frontmatter. The renderer has no
opinion about whether the deck should exist.

---

## When a piece should be a carousel — the selection rule

This is the judgment the caller makes *before* rendering anything, and it is the
most valuable part of this file. Carousels out-dwell single images on feed
channels — swiping is an active engagement action — which makes the format
tempting to over-use. Resist that. **A padded carousel performs worse than a good
single image and reads as filler.**

**The test: does every slide earn its own swipe?** If slide 4 exists only because
you promised five of something, it is not a carousel.

**Carousel — when the substance is genuinely sequential and decomposable:**

| Signal in the source material | Why carousel wins |
|---|---|
| A framework or model with 3–6 **named** parts | Each part gets a beat; one image would compress them into unreadable bullets |
| A step sequence where **order matters** | The swipe *is* the sequence |
| "N gaps / mistakes / lessons" where each item is specific, not a restatement | One idea per slide is the format's whole point |
| A before → after teardown with distinct stages | Stages need separation to land |
| A stat that needs unpacking — number → why → what to do | The unpack is the payoff and it needs room |

**Single image — when the piece is one idea, however good:**

| Signal | Use instead |
|---|---|
| A single punchy declarative frame, no decomposition | one image |
| One number plus a comment | one image |
| 2–5 comparable numbers | one image — a chart in **one** frame beats five slides of one bar each |
| Opens by naming a wrong take | one image |
| A claim plus 2–3 supporting points | one image |
| You can say the whole thing in three sentences | one image |

**Hard gates — all four must hold, or it is not a carousel:**

1. **≥ 4 genuinely distinct beats** after the cover, each with its own payoff.
   Fewer, and it is a single image with extra steps.
2. **The substance already exists** — real source material, a proof entry, a
   shipped project. A carousel cannot be padded into existence; the format makes
   thin content *more* obvious, not less.
3. **≤ 30 words per slide.** Decks are read at swipe speed. A slide that needs
   re-reading is overweight — split it or cut it.
4. **Format variety in the surrounding run** (below).

**Frequency is set by the material, not by a quota.** If the substance is
genuinely a framework, a sequence or a checklist, use the format; if it is one
idea, do not. A teaching series where most parts enumerate real practices will
earn carousels often, and that is correct.

**The one thing that does limit frequency — and it is not a quota.** Feed
classifiers began downranking posts that read as templated or automated in May
2026, and a user-facing "seems like AI slop" report control shipped on
2026-07-30 (recorded in the channel playbook). **An unbroken run of document
posts is structural uniformity in its purest form**, regardless of how good each
deck is. So: pick carousel whenever the material warrants it, **and keep genuine
format variety in the surrounding run** — if converting a stretch of pieces would
leave three or four carousels back-to-back, hold the weakest as a single image.
Vary slide archetypes *inside* each deck too: two decks that both run cover →
list → cards → takeaway read as a template even with different words.

---

## Inputs

- A JSON spec (schema below), written by the caller
- An output **directory** — the renderer writes several files
- The renderer: `$MKT_DEPT/skills/render-carousel/render.py`
- Its runtime: a PDF library able to embed fonts (`reportlab`), a PDF→PNG
  rasteriser (`pdftoppm`/poppler), an image library for the paper grain
  (`Pillow`), and `fontTools` for the font work below
- Brand tokens: `config/config.yaml → brand.profiles.{name}` — palette, fonts,
  footer text, and the theme list. The profile is *whose* deck it is; the theme
  is which treatment within that brand. `--profile` / `--theme` on the command
  line override the spec.

**Renderer availability is a hard stop, not a fallback.** If
`$MKT_DEPT/skills/render-carousel/render.py` is absent or its runtime is not
installed, stop with `renderer_missing` and tell the caller to pick a single
image. Never emit carousel frontmatter for assets that do not exist.

### How many themes a profile should have

**One theme is a legitimate answer.** A brand whose guide names one accent as
"the whole palette" should get one treatment; rotating four would break the brand
to solve a problem it does not have. Rotation exists for a brand that publishes
daily and needs adjacent posts to look different from each other. **Do not add
themes to a restrained profile to "add variety"** — variety there comes from
slide archetypes, not from repainting the brand.

### Fonts — the part that silently ruins output

- **A variable font cannot be embedded as-is.** `reportlab` cannot interpolate
  one: it embeds the default instance and **every weight renders identically**.
  The renderer cuts static Light/Regular/Medium/Bold instances with `fontTools`
  into a cache directory on first run, keyed on the source file's mtime —
  automatic, and never a setup step for anyone.
- **`updateFontNames=True` is required when cutting instances.** Without it all
  four cuts keep the variable font's internal name, `reportlab` collides them
  into one embedded face, and the whole deck renders in a single weight.
- **Never fall back to a PDF builtin base-14 face for a profile that ships
  PNGs.** Builtins are *referenced*, not embedded. A PDF viewer resolves them to
  real faces and the PDF looks right — but the rasteriser substitutes a single
  face for both weights, so the slide PNGs come out with **no weight contrast at
  all**. Measured 2026-08-10: the same string in regular and bold rasterised to
  byte-identical ink. That matters because the PNGs are the publish fallback and
  the cross-posting assets, not just a preview. Without `fontTools`, warn and
  degrade explicitly rather than pretending the output is fine.
- One consequence worth knowing when editing: with a builtin family that has no
  medium cut, `med` maps to **regular**. While the rasteriser was flattening
  everything this was invisible; the moment real faces were embedded, every list
  row and footer set in `med` came out as heavy as the headline.

### Spec schema

```json
{
  "title": "Used as the PDF title",
  "profile": "the brand profile name from config",
  "theme": "a theme registered for that profile",
  "meta": { "archetype": "carousel", "sources": ["https://..."] },
  "slides": [ ... ],
  "caption": "The post commentary, written to caption.txt"
}
```

### Slide types

Sequence them; a standard deck is 6–9 slides. Cover and CTA are twinned — same
treatment — so the deck reads as a loop.

| Type | Required | Optional | Notes |
|---|---|---|---|
| `cover` | `headline` | `eyebrow`, `accent_word`, `size`, `leading`, `variant` | `accent_word` gets the emphasis treatment. It must be an **exact substring** of `headline` or nothing is marked — it may wrap across lines |
| `context` | `chip`, `headline`, `body` (list) | — | Two short paragraphs max |
| `stat` | `chip`, `number`, `qualifier` | `number_to`, `labels` (2), `source` | `number_to` renders `78% → 14%`. **`source` is mandatory for any real stat** — see Failure handling |
| `list` | `chip`, `headline`, `items` | `highlight` (index), `icon` | Max 6 items; one highlighted row |
| `cards` | `chip`, `headline`, `cards` (list of `{text}`) | `surface` | Max 3 cards |
| `takeaway` | `headline` | `body` | The one thing to remember |
| `cta` | `headline` | `body`, `url` | Ends the loop. If `url` equals the profile footer, the footer's left text is suppressed so the address does not print twice |

**`accent_word` is valid on every slide type, not just the cover.** It marks a
phrase in that slide's `headline`, or a `stat` slide's `qualifier`. It was
cover-only until 2026-08-10, which is why older decks have solid-ink interior
headlines while single-image posts put colour in theirs.

### Emphasis — colour and weight inside the copy

A single-image post carries accent colour *inside* its body copy: the figure is
coloured, the label is bold. Decks read flat next to them unless body copy gets
the same treatment.

**Explicit — wrap a span in asterisks.** Works in every copy field: `context.body`,
`list.items`, `cards[].text`, `takeaway.body`, `cta.body`.

```json
"items": ["*Ten thousand* requests, not ten"]
```

**Automatic — applies only to a block with no `*…*` of its own:**

| Pattern | Treatment | Why |
|---|---|---|
| `Label:` at the head of a block | label in accent + medium weight | Cards name their subject |
| any word containing a digit | accent | Numbers are the proof, same as the single-image system |

Figures are marked **uniformly** — every number in the block, not the first one
or two. A rule the reader can perceive reads as a system; marking `25K` but not
the `200K` three words later just reads as a mistake.

**Write the marks in; do not lean on the auto rule.** It exists so decks written
before the feature still gained emphasis without anyone rewriting them — it is a
floor, not the intent. Copy written with a deliberate `*mark*` and one
`accent_word` per slide always beats copy where the renderer guessed from
punctuation.

---

## Steps

### 1. Make the selection call

Apply the rule above. Fails any of the four hard gates → **do not render**. Pick a
single image instead and note why in the piece. Stop code:
`selection_rejected`.

### 2. Write the spec

Every slide under 30 words. Copy rules are unchanged from the caller's voice
pass. Sentence case in the JSON — a profile that uppercases headlines does it at
render time, and pre-uppercasing makes the caps logic double-apply to body copy.

### 3. Render

```bash
python3 "$MKT_DEPT/skills/render-carousel/render.py" \
  path/to/spec.json \
  content/carousels/{slug} \
  --profile {profile}
```

On success it prints the absolute PDF path, byte size and slide count, and exits
0. On failure it prints the reason to stderr and exits non-zero →
`render_failed`.

**Read the stderr overflow warnings.** The renderer measures each slide's content
against the footer band and names any slide that runs past it:

```
overflow warnings:
  slide 5 (cards): content reaches 1722px, footer band starts at 1230px — trim copy
```

An unresolved overflow warning is `overflow_unresolved` — fix the copy and
re-render. It is still **not** a substitute for step 4: it catches content
running off the bottom, not a headline colliding with a chip or an accent mark
landing on the wrong word.

### 4. Eyeball every slide — mandatory

**Open every PNG in `slides/` before writing any frontmatter.** Clipping is the
number-one recurring bug with rendered post images, and **a zero exit code does
not mean the layout is right.** Check: nothing cut off at the bottom, the accent
word marked on the intended word, the highlighted list row on the intended item,
and the cover headline not shrunk so far it looks weak.

A slide is wrong → fix the **JSON**, not the output, and re-render. Stop code
`slide_clipped` if it cannot be fixed.

### 5. Hand back the paths

Return to the caller, for the piece's frontmatter:

```yaml
carousel_pdf: content/carousels/{slug}/carousel.pdf
slide_paths:
  - content/carousels/{slug}/slides/slide-1.png
  - content/carousels/{slug}/slides/slide-2.png
  # ... every slide, in order
image_path: content/carousels/{slug}/slides/slide-1.png
image_format: carousel
```

All four fields are required, and each earns its place:

- **`carousel_pdf` — what publishes**, as a true document post (a swipeable
  multi-page deck). It is also what an approval surface renders so the approver
  can flip through the deck before M2.
- **`slide_paths` — the multi-image fallback** if the document route fails (2–20
  PNGs). **Order matters**, and the rasteriser does not zero-pad its output
  names, so list them explicitly rather than globbing — a glob sorts
  `slide-10.png` before `slide-2.png` and ships the deck out of order. Never omit
  these: they are the only thing standing between a document-API hiccup and a
  lost post.
- **`image_path` — slide 1**, the preview for approval surfaces. Without it the
  approver approves the deck blind. It never causes a single-image publish:
  `ship-content` checks the carousel fields first.
- **`image_format: carousel`** — keeps a single-image rotation check honest, so
  shipping a deck does not count as having used a single-image layout.

---

## Outputs

Into `content/carousels/{slug}/`:

| File | Contents |
|---|---|
| `carousel.pdf` | 1080×1350 vector, one page per slide — what publishes |
| `slides/slide-N.png` | one per slide, 1080×1350 — publish fallback and cross-posting assets (already 4:5) |
| `caption.txt` | the spec's `caption` |
| `meta.json` | the spec's `meta` plus the resolved profile, theme and slide count |

---

## Stop codes

| Code | Meaning |
|---|---|
| `rendered` | the only success |
| `selection_rejected` | failed a hard gate — the caller renders a single image instead |
| `spec_invalid` | a required key missing, or a slide over the word limit |
| `stat_unsourced` | a `stat` slide with a real number and no `source` |
| `renderer_missing` | the renderer or its runtime is not installed |
| `render_failed` | non-zero exit, or a missing/implausibly small PDF |
| `overflow_unresolved` | the renderer named an overflowing slide and it was not fixed |
| `slide_clipped` | step 4 found a broken slide that the spec could not fix |

---

## Failure handling — a missing carousel beats a broken one

- **Any slide clips, or a stat has no `source`: do not write the frontmatter.** An
  unsourced number published under the business's name is a credibility risk.
  Drop the stat slide, or drop the carousel.
- Render exits non-zero, or the PDF is missing or tiny → log and flag the piece
  for review rather than shipping. `ship-content` treats missing carousel assets
  as `carousel_assets_missing` and notifies — it does **not** silently ship the
  post text-only, because for a deck the text is a caption and publishing it
  alone guts the post.
- **Never hand `ship-content` a broken PDF.** A text-only post is always the
  better failure mode, and choosing it is the caller's decision, made before
  frontmatter is written — not the publisher's, made at 8am unattended.

---

## Format rules — do not drift

- **1080×1350 (4:5) for every profile.** This is a deliberate departure from a
  square single-image standard, and it applies to **carousels only**. Reasons: a
  document post is a different surface from an image post; 4:5 portrait is the
  researched document-post standard for mobile dwell. **Do not change the
  single-image format to match**, and do not change this one to match single
  images — either way that is the approver's call, made explicitly.
- **One accent *element* per slide** — one fill, one drawn mark. The accent is a
  scalpel, not a highlighter. This governs marks and fills, **not** inline colour:
  coloured figures inside a paragraph are a type role, and they are what make a
  slide look like it came from the same system as a single image.
- **A restrained profile keeps its discipline**: two or three colours, no
  gradients, no dark backgrounds, no clip-art icons. Icon sets are ignored on a
  profile whose guide uses typographic markers instead.
- **A full-bleed accent CTA is usually wrong.** A wall of the accent colour
  contradicts the two-colour discipline directly above it, and the endcap reads
  better mirroring the cover — same ground, ink headline, one accent mark — which
  is what makes the deck read as a loop. It was a full accent slab on the source
  profile until 2026-08-10. The CTA surface is a **per-theme key**: a brand whose
  identity *is* a saturated slab keeps it. Do not hardcode either.
- Where a brand guide contradicts itself — one section sanctioning a dark theme
  and another forbidding dark backgrounds — the later, more specific rule ships,
  and the contradiction is flagged to the approver rather than silently resolved
  in the renderer.
