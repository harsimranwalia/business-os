# Content Writer — Skills

Skills this agent invokes directly. All resolve under `$MKT_DEPT/skills/` and
are reusable by any agent in the department. This agent is invoked by the
campaign strategist (`agents/campaign-strategist/agent.md`) with a per-piece
brief and runs on no schedule of its own — see the strategist's `skills.md`
for the planning chain above it, and `$MKT_DEPT/docs/marketing-team.md` for
the whole pipeline.

Two absences are deliberate, not gaps. The life-os original invoked a shared
`draft-critique` skill and a `render-infographic` skill; **neither exists in
this port.** Critique is Pass 2 inside each writer skill, so the criteria
live in one place, next to the writing they judge. The single-image renderer
is a per-channel instance registration — `config/channels/{channel}.md` →
`image_renderer` — and a channel with none registered writes `image: none`
plus an `image_note` instead of silently shipping textless. Do not reference
either old skill; a path to a skill that doesn't exist is a dead reference.

The ship skills (`ship-content`, `ship-content-x`) are invoked by **nobody**
— they run on their own schedule. `topic-miner` and `engagement-analyzer`
are the strategist's. This agent's chain is exactly four skills:

| Skill | Trigger | Purpose |
|---|---|---|
| `skills/content-writer/SKILL.md` | brief received; the channel resolves long-form | Draft + critique + the visual, one run — the long-form registers |
| `skills/x-content-writer/SKILL.md` | brief received; the channel resolves to a 280-character channel | Draft + deterministic weighted count + critique — tweet or thread |
| `skills/render-carousel/SKILL.md` | inside the writer pass, archetype `carousel` | The carousel selection gate, then the 1080×1350 vector PDF + per-slide PNGs |
| `skills/content-reviewer/SKILL.md` | after every draft, before anything returns upstream | The machine review pass: evidence-cited revisions, max 2 rounds, moves the piece to `ready-to-send` and raises the M2 item |

Model tiers are declared in each skill's own header — `generation` drafts,
`reasoning` critiques and reviews — and the instance binds each tier to a
model. One binding is pinned: **content-reviewer runs at the `reasoning`
tier and is never raised to `generation`.** A reviewer at the drafting tier
rewrites the piece instead of reviewing it, which produces a second draft
nobody briefed and quietly costs a revision round.

## Call graph

```
brief received (from agents/campaign-strategist/agent.md)
  {channel, archetype/format, source_material, register, include_cta, notes}
  — all six fields, or it fails the brief-completeness gate and goes back

  └── dispatch on the brief's `channel` field — NEVER inferred:

      $MKT_DEPT/skills/content-writer/SKILL.md      (long-form registers)
      OR $MKT_DEPT/skills/x-content-writer/SKILL.md (280-character channels)
        ├── pre-flight: MODE (.env → exit mode_halt on sabbath/retreat/quiet),
        │   channel autonomy (c0 → channel_not_live), brief completeness,
        │   source material, the voice floor (LONG-FORM PATH ONLY — the
        │   short-form path deliberately has none; see the asymmetry in
        │   both skills and agents/campaign-strategist/config.yaml),
        │   naming rules anonymized IN THE PROMPT, never redacted after
        ├── Pass 1: draft (generation tier)
        │     reads: ../knowledge/business-profile.md
        │     reads: agents/cmo/config/ (positioning, anti-patterns — read-only)
        │     reads: voice/guide.md + voice/samples/{register}.md
        │     reads: config/channels/{channel}.md (the playbook)
        │     reads: content/series/series-{slug}.md, when the brief names one
        ├── Pass 1b (short-form path only): deterministic weighted character
        │   count — arithmetic, never model judgment; overwrites Pass 1's
        ├── Pass 2: critique (reasoning tier) — INSIDE the skill; there is
        │   no standalone critique skill in this department
        ├── Pass 3: conditional regen
        │     0 critical failures → done
        │     1 → regenerate once, critique as input
        │     2+ → return original + critique attached (critique_failed);
        │          a second draft off the same wrong material learns nothing
        └── visual, same run, never queued:
              carousel archetype → $MKT_DEPT/skills/render-carousel/SKILL.md
                → content/carousels/{slug}/slides/*.png + carousel.pdf
                → frontmatter: carousel_pdf + slide_paths + image_path
                  (slide 1, the approval-surface preview) + image_format
              single image → the playbook's image_renderer, if registered
                → content/images/{slug}.png
                → frontmatter: image_path + image_format
              no renderer → frontmatter: image: none + image_note
                (a declaration, not a gap — the reviewer's image gate
                 blocks a piece carrying neither)

  └── writes: content/drafts/{YYYY-MM-DD}-{archetype}-{slug}.md
        (status: draft — the date is the PLANNED publish date; the channel
         lives in the frontmatter, never in the filename)

  └── $MKT_DEPT/skills/content-reviewer/SKILL.md
        ├── house-style gate first — a draft that fails it goes straight
        │   back, no engagement review that round
        ├── evidence-cited review, or low-data mode on a fresh instance
        │   (anti-patterns + archetype criteria + voice, zero invented
        │    engagement claims)
        ├── image gate: file exists + slug matches + eyeballed, or an
        │   explicit image: none declaration
        ├── verdict revise → THE REVIEWER calls the matching writer skill
        │   with revision_target (targeted edits, not a rewrite) → re-review
        ├── max 2 rounds; still unresolved → verdict: unresolved, concerns
        │   attached in review.unresolved_concerns — the piece STILL moves
        ├── sets status: ready-to-send, moves the file to
        │   content/ready-to-send/ — the only status transition this whole
        │   chain makes; approved/shipped are out of bounds everywhere
        └── raises the M2 item in inbox/ + lib/mkt-notify.sh — updating an
            existing item for the slug rather than raising a second

  └── returns: final draft path + review verdict
        → agents/campaign-strategist/agent.md (it logs the piece)
        The reviewed draft on the approval surface is the only form in
        which the approver ever meets this agent's work.
```

## The two notifies in this chain — and why neither is this agent speaking

This agent never talks to the approver, and the chain above contains exactly
two calls to `lib/mkt-notify.sh`. Both are pipeline mechanisms defined in
the skills, not this agent raising its voice:

1. **The M2 item** (content-reviewer, step 8) — the draft being delivered to
   the approval surface. Every piece produces one; it is how gate M2 works,
   for every agent's output alike.
2. **The `no_voice_reference` seeding raise** (the long-form writer's
   pre-flight, once) — a blocked precondition of the whole department: no
   samples and no guide means there is nothing to write *as*, and only the
   instance's operator can seed a corpus. One raise, then silence.

Everything else — render failures, unresolved verdicts, upstream contract
violations — returns to the campaign strategist as stop codes and attached
concerns, and goes no further unless the strategist's channel report or the
CMO carries it up. That is the single-front-door design working, not
information being lost.
