# Campaign Strategist — Skills

Skills this agent invokes directly. All resolve under `$MKT_DEPT/skills/` and
are reusable by any agent in the department.

The drafting and review chain (`content-writer`, `x-content-writer`,
`content-reviewer`, `render-carousel`) is invoked by the **content writer**, not
by this agent — see `agents/content-writer/skills.md` for that chain. The ship
skills run on their own schedule and are invoked by **nobody**; this agent reads
their output.

| Skill | Trigger | Purpose |
|---|---|---|
| `skills/topic-miner/SKILL.md` | the planning run, per channel needing fresh topics | Extract publishable topics from the proof directories and the business's knowledge, scored and tagged by channel fit |
| `skills/engagement-analyzer/SKILL.md` | when metrics land for a shipped piece | Compute the delta against the rolling baseline, detect outliers, write the performance log |

**`topic-miner` is skipped for a trailing series.** Where a channel's queue is
series-driven — each piece repurposed from a piece already shipped on another
channel — mining fresh topics produces content unrelated to the series. Take the
next piece from the series queue instead, falling through to a standalone piece
when nothing is queued. The queue rule lives in that series' own file under
`content/series/`.

## Call graph

```
planning run (enters through the CMO — agents/cmo/skills.md)
  CMO: reads notebooks + outcomes → writes the ALLOCATION BRIEF → invokes this agent

  └── campaign-strategist (this agent)
        ├── reads: MODE from .env → exit on sabbath/retreat
        ├── reads: config/config.yaml → channels    (live channels, tiers, numbers)
        ├── reads: config/channels/{channel}.md     (the playbook, per channel briefed)
        ├── reads: agents/cmo/config/               (positioning, anti-patterns,
        │                                            exemplars, current-cta — read-only)
        ├── reads: content/series/*.md              (any running series + its queue rule)
        │
        ├── topic-miner  (per channel; SKIPPED where the queue is series-driven)
        │     ├── reads: proof/case-studies/, proof/internal/
        │     ├── reads: ../engineering/reports/proof/        (read-only)
        │     ├── reads: ../knowledge/business-profile.md
        │     ├── excludes: recently-used material
        │     └── returns: scored candidates, tagged by channel fit
        │
        ├── splits the allocation across live channels; decides archetype/format
        │   per piece and whether it is fresh or a repurpose
        │
        └── per piece: writes the BRIEF
              {channel, archetype/format, source_material, register, include_cta, notes}
              │
              └── invokes: agents/content-writer/agent.md
                    (draft → critique → image/carousel pass → review loop,
                     max 2 rounds — full chain in agents/content-writer/skills.md)
                    └── returns: final draft path + review verdict
              │
              ├── logs the returned draft to the content log
              └── the draft sits in content/drafts/ with status: draft
                    ── THIS IS THE APPROVAL SURFACE (gate M2).
                       No second inbox is written for content, ever.

  └── writes: content/topic-bank.md               (updated)
  └── writes: the channel report section(s)       → the CMO folds them into the weekly report
  └── writes: notebook/routed-signals.md          (if any inbound signals matched)
  └── routes:  inbound.route_to                    (the signals themselves)

publishing (own schedule — NOT invoked by this agent)
  └── skills/ship-content/SKILL.md      (long-form channel)
  └── skills/ship-content-x/SKILL.md    (short-form channel)
        ├── read: content/approved/ — status: approved, filename date <= today
        ├── enforce: cadence (1/channel/publishing day, oldest first, no burst),
        │            format limits (revalidated at publish), asset readiness
        ├── halt on: MKT_PUBLISH_FREEZE
        └── write: content/shipped/
              campaign-strategist reads shipped/ + the trace log for the channel
              report. Oversight here, never execution.

engagement (after metrics land)
  └── engagement-analyzer
        ├── reads: content/shipped/ (pieces old enough to have numbers)
        └── writes: notebook/{date}-performance-log.md
              ├── outperformer (threshold x baseline in the window)?
              │     → this agent writes 2 follow-up briefs within 48h,
              │       back into the pipeline at the brief step.
              │       Dated for their intended publishing day, like any draft,
              │       with the follow-up origin recorded in frontmatter — never
              │       in the filename, which the ship skills parse for the date.
              └── pattern forming? → notebook + the channel report
```

## Why two ship skills, and why that is not a channel agent

`ship-content` and `ship-content-x` are separate skills rather than one skill
with a branch. The reasoning is worth keeping, because the same question comes
up for every new channel:

The long-form ship path carries machinery the short-form path never uses —
markup conversion, a document/carousel upload path and its fallback, image
attachment. The short-form path needs machinery the long-form one has no
analogue for: composer-driven multi-part posting, per-unit weighted-limit
revalidation, timeline read-back verification, a different cadence. One skill
holding both would be mostly dead code on every run.

That is a **craft** fork, and craft forks are allowed. It is not a strategy
fork, and it is emphatically not a new agent: both skills read the same
`channel` field off the same draft, on a plan this one agent made. When a third
channel arrives, ask the same question — does the *procedure* differ, or only
the *content*? Only the first answer earns a new skill.
