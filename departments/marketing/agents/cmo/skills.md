# CMO — Skills

Skills this agent invokes directly: **none.**

That is not an omission. The CMO's work is judgment — an allocation brief, a
positioning read, a report — and none of it is a repeatable procedure with a
fixed input contract. Everything it produces, it writes itself. The execution
skills below are invoked by the agents underneath it, and are listed here only
so the chain the CMO starts is legible in one place.

All skills resolve under `$MKT_DEPT/skills/`.

| Skill | Invoked by | Trigger |
|---|---|---|
| `skills/topic-miner/SKILL.md` | campaign strategist | the planning run, per channel that needs fresh topics |
| `skills/content-writer/SKILL.md` | content writer | brief received, long-form channel |
| `skills/x-content-writer/SKILL.md` | content writer | brief received, `channel: x` |
| `skills/content-reviewer/SKILL.md` | content writer | after each draft, before it is returned |
| `skills/render-carousel/SKILL.md` | content writer | format is a carousel |
| `skills/ship-content/SKILL.md` | its own schedule | a publishing day, LinkedIn queue |
| `skills/ship-content-x/SKILL.md` | its own schedule | a publishing day, X queue |
| `skills/engagement-analyzer/SKILL.md` | campaign strategist | after metrics land for a shipped piece |

**There is no positioning-auditor skill.** The biweekly positioning audit is the
CMO's own read of the last eight shipped pieces against
`positioning-statement.md`. Kept unautomated deliberately: the useful output is
a judgment about drift across a run of pieces, and a per-piece scoring skill is
worst at exactly that — it produces eight numbers and no conclusion.

## Call graph

```
weekly planning run (schedule: instance's config; catch-up re-enters here too)
  └── CMO (this agent)
        ├── reads: MODE from .env → exit on sabbath/retreat
        ├── catch-up entry only: did the scheduled run complete?
        │     compute the date fresh, then look for pieces carrying it in BOTH
        │     $MKT_INSTANCE/content/drafts/ AND $MKT_INSTANCE/content/shipped/
        │     complete → log one line, exit
        ├── reads: ../knowledge/business-profile.md          (fresh, every planning run)
        ├── reads: agents/campaign-strategist/notebook/      (performance, audience, routed signals)
        ├── reads: inbox/requests/                            (topics filed by a filer)
        ├── reads: proof/case-studies/, proof/internal/,
        │          ../engineering/reports/proof/              (read-only)
        ├── reads: config/config.yaml → channels              (live channels, tiers, default mixes)
        ├── writes: the ALLOCATION BRIEF
        │     {piece count, per-channel emphasis, trades, narrative arc in one line}
        │
        ├── invokes: agents/campaign-strategist/agent.md
        │     └── splits the allocation, briefs the content writer per piece,
        │         logs each returned draft, and leaves it on the approval
        │         surface. Full chain: agents/campaign-strategist/skills.md
        │
        └── writes: reports/marketing-{YYYY}-W{WW}.md
              (the unified report — folds in the campaign strategist's section)

positioning audit (biweekly, the CMO's own read — no skill)
  └── CMO
        ├── reads: content/shipped/ (last 8 pieces)
        ├── reads: agents/cmo/config/positioning-statement.md
        └── writes: agents/cmo/notebook/{date}-positioning-audit.md
              drift found → M1 proposal. No drift → one line, nothing raised.

M1 / M3 proposals (never scheduled — raised when evidence demands)
  └── CMO
        ├── writes: inbox/{item}.md — one decision per item, recommendation
        │     first, the recurring cost in the approver's hours named
        └── notify: lib/mkt-notify.sh
              The CMO never adopts its own proposal. Silence is not approval.
```

## Handoff contract

The CMO hands the campaign strategist exactly one thing: **the allocation
brief** — piece count, per-channel emphasis, trades, and the narrative arc in
one line. Nothing else, and nothing verbal.

What it does *not* hand over: which archetype, which format, which channel a
given beat serves, or what any individual piece should say. Those are the
campaign strategist's calls, and re-deciding them inside an allocation brief
collapses two jobs into one — at which point the department has a CMO writing
briefs for itself and no strategist.

Back the other way, the CMO receives the campaign strategist's channel report
section(s) — facts and channel-level calls only. Positioning commentary in a
channel section is a contract violation in the other direction.
