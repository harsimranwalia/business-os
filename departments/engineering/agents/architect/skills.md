# Architect — Skills

| Skill | Trigger | Model | Purpose |
|---|---|---|---|
| `skills/request-readback/SKILL.md` | every full-lane request, at intake | opus | The **blind second reading** — raw input only, never the PM's interpretation |
| `skills/tech-design/SKILL.md` | ticket enters `designed` | opus | PRD → technical design, ADRs, one-way-door calls |
| `skills/schema-change/SKILL.md` | design touches data (co-run with `database`) | opus | Data-model intent and constraints, handed to `database` for the migration |

## Call graph

```
ticket → `designed` (dispatched by eng-manager)
  └── tech-design
        ├── reads: agents/product-manager/specs/{ENG-NNN}-{slug}.md (acceptance criteria)
        ├── reads: ../../../knowledge/business-profile.md (what the business
        │     is, who it serves, what it sells — sizes the design and the
        │     one-way-door call)
        ├── reads: agents/eng-manager/config/projects.md (hard constraints, autonomy)
        ├── reads: agents/eng-manager/config/engineering-standards.md
        ├── reads: agents/architect/config/ai-architecture-standards.md (if touches_models)
        ├── reads: agents/architect/decisions/ (prior ADRs on this project)
        ├── reads: the project's own code — shape, conventions, existing patterns
        ├── writes: agents/architect/designs/{ENG-NNN}-{slug}.md
        ├── writes: agents/architect/decisions/ADR-{NNN}-{slug}.md (0..n)
        └── one-way door found?
              ├── yes → state `awaiting-decision`, G2 package → eng-manager → inbox/
              └── no  → state `ready`, owner eng-manager (work-breakdown next)

design touches data
  └── schema-change (architect states intent + constraints)
        └── → agents/database/ writes the migration plan and owns the migration gate

technical debt observed (any run)
  └── writes: intake card → agents/eng-manager/inbox/
        └── EM sequences it; the approver decides whether it's worth paying down
```

## Contract with the engineers

The design tells them *what* to build and *what it must survive*. It does not
tell them how to name their variables. Where the design is silent, the engineer
decides and the standards apply. Where the design is wrong, the engineer says
so through the EM rather than quietly building something else — a design that
gets silently ignored is worse than no design.
