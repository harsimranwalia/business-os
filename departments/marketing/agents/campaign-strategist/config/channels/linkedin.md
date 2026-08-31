# LinkedIn — channel playbook

**Mechanics only.** Strategy — what to publish, when, in what mix — lives in
`agents/campaign-strategist/agent.md` and the instance's channel registry. This
file is the reference for *how LinkedIn works*, not what to do with it.

**This is the shipped starting playbook.** `install` copies it to
`$MKT_INSTANCE/config/channels/linkedin.md`, and from then on **the instance's
copy is the only one anyone reads or edits** — it carries this business's
cadence, baselines, publishing identity and hashtag pool, none of which are
template facts. The copy under `$MKT_DEPT` is read-only reference.

Everything marked _[instance]_ must be filled in before the first publish.

## Autonomy

Registers at **C1**. Moves to C2 at gate M3, once the publishing path below is
real and the credential resolves. Current tier: the instance's registry, not
this file — a tier written in two places will eventually be two different tiers.

## Format limits

- **Post body: 3000 characters, a hard API limit.** Enforced by
  `skills/ship-content/SKILL.md` at publish time, and re-checked there rather
  than trusted from draft time — the two can diverge when a draft is edited on
  the approval surface.
- **No markdown rendering, at all.** Bold and italic can be converted to Unicode
  styled characters before posting, and that is the only formatting that
  survives. Headers and markdown links have **no** Unicode fallback and publish
  as literal broken punctuation — never use them.
- **Single images: square, 1200x1200 PNG.** _[instance: confirm, if the business
  has a different standard.]_
- **Carousels: 4:5, 1080x1350**, shipped as a vector PDF document post with the
  ordered slide PNGs as automatic fallback if the PDF is rejected. The two
  formats differ on purpose — a document post is a different surface from an
  image post, and 4:5 is the document standard for mobile dwell. The square rule
  still binds every single image.

## Algorithm behaviour — what actually drives reach

- **Dwell time** — how long a viewer stays before scrolling — is a stronger
  ranking signal than reactions. A piece that reads slowly (short lines, a real
  hook) outperforms one skimmable in half a second.
- **Save rate** and **early velocity** (engagement in the first 60–90 minutes)
  both weight heavily into whether the piece is shown beyond the immediate
  network. This is *why* rotation matters for reach, not only for variety.
- **Native content is favoured over anything that sends the viewer
  off-platform.** No external links in the body — say the URL in words, or move
  it to the first comment if it is genuinely unavoidable. This is also why a
  document post tends to out-dwell a single image.
- **Structural uniformity actively hurts reach.** The platform began
  downranking content a classifier reads as templated or automated in 2026, and
  added a user-facing report control for it. This binds every draft; the
  specifics — which structural elements must vary piece to piece, and what
  varying them does and does **not** buy you — live in the CMO's
  `anti-patterns.md` → "Structural uniformity". Read it before any batch, not
  once.

## Carousel (document post) mechanics

A document post renders as a swipeable PDF. Slide count, per-slide word budget,
the slide archetypes, and **the rule for deciding whether a piece should be a
carousel at all** live in `skills/render-carousel/SKILL.md`; this file does not
duplicate them.

What belongs here is the mechanical reason the format is worth rotating in: the
document surface gets its own algorithmic treatment, and swiping is an active
engagement action, so dwell tends to be strong. That is separate from the
strategic call — occasional, following the material, never a quota — which lives
with the strategist.

**The dwell advantage is exactly why the format needs a selection gate rather
than a green light.** It makes a *decomposable* idea land harder and a padded one
land worse. `render-carousel`'s "does every slide earn its own swipe?" test is
that gate, and it is applied before a carousel is planned into the mix, not after
it is rendered.

## Publishing under a second identity — read before promising it

A business will eventually want to publish some pieces as a **company page**
rather than as a person, or vice versa. Rendering under a second brand profile
is easy; publishing under a second identity is not, and the two get conflated.

Unblocking it needs all four, in order:

1. the second identity's organization/author identifier;
2. the integration's credential authorized to post **as** that identity;
3. its own entry in the instance's channel registry;
4. the ship skill reading the author identity **from the draft** rather than
   from one hardcoded value.

Until all four exist, **do not schedule content for that identity.** It produces
finished assets with no path to publication, which is the dead end this
department exists to avoid. This is a real trap: in the instance this playbook
was ported from, the renderer had a second brand profile for months while no
publishing identity for it existed anywhere.

## Cadence

- **At most one piece per calendar day**, enforced by
  `skills/ship-content/SKILL.md`, weekdays only. _[instance: confirm the working
  week — this is a business decision, not a platform fact.]_
- **A backlog of approved-but-unpublished pieces drains oldest-first, one per
  day. Never a burst**, even when several are approved at once, and especially
  when a publish freeze lifts with a full queue behind it. This rule exists
  because three backlogged approvals once went out in a single run and the
  approver deleted two by hand.
- The default weekly mix size is a **default, not a cap** — a fifth publishing
  day is valid when the plan calls for one.

## Hashtag rules

- **3–5 per piece**, appended after a blank line at the end of the body.
- **1–2 brand hashtags** from a fixed pool, rotated — never the exact same set
  every time, which is itself a structural-uniformity tell. _[instance: define
  the brand pool.]_
- 2–3 topic-specific hashtags per piece.
- **Series exception:** while a named series runs, its anchor hashtag stays fixed
  across every piece in it. That is deliberate reader-facing wayfinding, not a
  uniformity violation. Everything else in the set still varies.
- Never generic filler tags — the ones that describe a mood rather than a
  subject.

## Current performance baselines

- Engagement-rate baseline (rolling 28-day): **unknown — populated by
  `engagement-analyzer`.**
- Save rate: **unknown.** _[instance: note whether the API tier exposes it at
  all — often it does not, and recording that saves the next person the search.]_
- Carousel vs single-image relative performance: **unknown — an open
  experiment**, tracked in the strategist's notebook until it settles.
- Interrupt threshold: the multiple and window in the channel registry.

**Do not substitute an invented number for any "unknown" above.** A baseline
exists once `engagement-analyzer` has logged enough shipped pieces to compute
one, and not before. A placeholder number gets reasoned from within a week.

## Publishing path

**Method: `api`** (`config/conventions.yaml` → `publishing.methods`). A published
integration is called with a token resolved from the environment. The tool name,
the author identity and the visibility setting live in the instance's channel
registry; **the credential itself lives in the environment and never in a file** —
not here, and not in the instance.

`require_approval: true` is not negotiable. `skills/ship-content/SKILL.md`
publishes only a draft carrying `status: approved`, set exclusively by the
approver's explicit action.

**Verification is by read-back where read-back is possible, and this channel is
the cautionary tale.** Some access tiers 403 every read-back route, which means a
publish can only be verified by the *absence of an error* — and that is not
verification. In the ported instance a well-formed publish identifier came back
for a piece that never existed. Where read-back is impossible, say so in this
file, say what is checked instead, and **record the publish as unverified.**
_[instance: state which applies at your API tier.]_

## Archetypes

| Archetype | What it is for |
|---|---|
| `data-insight` | A real external data point plus the business's angle on it. The most shareable shape — it gives readers something concrete to reference. |
| `case-study` | What was built or shipped and what happened, including what broke. Opens with the decision, not the architecture. |
| `pov` | A sharp, specific, disagreeable take. Fails if hedged. |
| `frame-shift` | A memorable way to think about something, applied specifically — never abstract advice. |
| `teardown` | Critique of a common misunderstanding. Occasional only; it reads negative as a weekly default. |
| `carousel` | One idea unpacked slide by slide, as a document post. Frequency follows the material, not a quota — but keep format variety in the run, since a stretch of consecutive document posts is exactly the uniformity the platform downranks. |
| `raw` | No imposed structure. Full flexibility, the brief sets the shape. |

Full structural spec per archetype — length targets, success and failure
conditions — lives in `skills/content-writer/SKILL.md`.

## Voice

Register: `linkedin-post`. Samples: `$MKT_INSTANCE/voice/samples/linkedin-post.md`.

**This channel's writer skill runs a voice preflight** — it reads the guide and
the register's samples before drafting. Below the floor of ten it still drafts;
it leans harder on the review pass and on M2, and the gap is recorded rather
than hidden. **The short-form channel deliberately has no preflight at all** —
see `config/channels/x.md`. The asymmetry is intentional and is documented in
both playbooks so nobody quietly evens it out.
