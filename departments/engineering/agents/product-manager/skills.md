# Approver Product Manager — Skills

This agent is the department's **front door**. Business needs enter here — from
the approver, from a request filed in `inbox/requests/` tagged `eng`, or from
Delivery — and leave as an approved PRD the EM can sequence.

| Skill | Trigger | Model | Purpose |
|---|---|---|---|
| `skills/request-readback/SKILL.md` | every full-lane request, before the PRD | opus ×2 | Input → two blind readings → divergence check → requirements → readback |
| `skills/prd-writer/SKILL.md` | a business need lands in the PM inbox or as an `eng`-tagged filed request | opus | Shape it into a ticket, then a PRD with testable acceptance criteria and a recommendation |
| `skills/acceptance-check/SKILL.md` | ticket enters `shipped` | sonnet | Verify every acceptance criterion against the live result |

## Call graph

```
business need arrives (agents/product-manager/inbox/, inbox/requests/ tagged `eng`, Delivery)
  ├── request-readback (full lane only) — BEFORE any PRD exists
  │     ├── preserves the input verbatim into the ticket
  │     ├── interpretation A: product-manager, from the raw input
  │     ├── interpretation B: architect, from the raw input, BLIND to A
  │     ├── diverge materially? → one question to the approver as a choice
  │     │     └── hold at `intake` until answered — never average, never guess
  │     └── agree? → requirements, each tagged stated/inferred/confirmed/proposed
  │
  └── prd-writer
        ├── shapes: a new ticket at `intake` — project, size, type, lane
        │     ├── L0 project      → lane `advisory` (terminates at `advised`)
        │     ├── XS bug/chore,
        │     │   no sensitive surface → lane `fast`: criteria inline in the
        │     │                          ticket, straight to `building`
        │     └── otherwise       → lane `full`
        ├── reads: board/{ENG-NNN}-{slug}.md
        ├── reads: ../../../knowledge/business-profile.md (what the business
        │     is, who it serves, what it sells — whether this is worth building)
        ├── reads: agents/eng-manager/config/projects.md (constraints, autonomy)
        ├── reads: agents/product-manager/notebook/ (what the approver has
        │     killed before, and whether this is worth their week)
        ├── writes: agents/product-manager/specs/{ENG-NNN}-{slug}.md
        └── → G1 item written straight to inbox/ (this agent owns the
              scope conversation; it does not route through the EM)
              └── answered → the ticket hands over to eng-manager for delivery

ticket → `shipped` (dispatched by eng-manager)
  └── acceptance-check
        ├── reads: the PRD's acceptance criteria
        ├── reads: agents/devops/releases/{release-record}.md
        ├── checks: each criterion against the running thing
        └── pass → state `verified`, owner eng-manager
            fail → state `building`, owner the implementing engineer,
                   with the failed criterion named in the ticket log
```
