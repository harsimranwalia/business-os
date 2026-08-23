# Tech design template

Written by `architect` at `agents/architect/designs/{ENG-NNN}-{slug}.md`.
Read by every engineer before they write a line. Sized to the change — an S
ticket gets half a page, an L ticket gets the whole thing.

```markdown
---
ticket: ENG-000
project: <project>
author: architect
created: YYYY-MM-DD
adrs: []                 # ADR IDs produced by this design
one_way_doors: []        # decisions escalated to the approver at G2, if any
touches_data: false      # true → database agent is in the chain
touches_models: false    # true → the AI architecture section is mandatory
---

# {Title} — technical design

## Approach

The shape of the solution in a paragraph. What changes, where, and why this
shape rather than the obvious alternative.

## Components

What gets added, changed, or deleted. One line each, by file or module.

| Component | Change | Owner agent |
|---|---|---|
| `path/to/thing` | new / modify / delete | backend |

## Data

Only if `touches_data`. Entities, fields, relationships, and the migration
shape. `database` owns the detail — this section states the intent and the
constraints it must satisfy.

## Interfaces

New or changed contracts: endpoints, function signatures, events, schemas.
Include the failure responses, not just the success one.

## AI architecture

Only if `touches_models`. Required subsections:

- **Where the model sits** — in the request path, in a background job, or in an
  agent loop, and what happens when it's slow or unavailable
- **Model choice and routing** — which model, why, and the fallback
- **Prompt and context** — where prompts live, what enters the context, what
  is untrusted and how it's delimited
- **Output contract** — the schema, and the defined behaviour on malformed or
  empty output
- **Evaluation** — how we know it works, and how we'd know it stopped working
- **Cost and limits** — token budget, call cap, kill switch
- **Trust boundary** — what authority model output has, and what it can never do

## Alternatives considered

At least one, with the reason it lost. A design with no alternatives considered
is a design that wasn't made.

## One-way doors

Decisions that are expensive to reverse: a new datastore, a vendor, an auth
model, a public contract, a data model that's painful to migrate, anything with
recurring cost. Each one either becomes an ADR (architect decided) or is
escalated to the approver at G2 with the trade-off stated in two sentences.

Reversible decisions are never escalated. Decide, log, move.

## Risks

What could go wrong in production, and what we've done about each.

## Rollout

How this reaches production safely: flag, phased, backfill-then-switch, or
straight. Rollback path in one sentence.

## Out of scope

Explicitly not being built here, and where it goes instead.
```

## Rules

- **The design serves the PRD's acceptance criteria.** If it can't satisfy one,
  that's a conversation with the PM before code, not a discovery during QA.
- **Prefer reversible.** In an early-stage project, keeping the decision cheap
  to change is worth more than getting it right the first time.
- **Constraints are design inputs.** For anything built as part of the
  instance's own tooling, "no API billing, no deployed endpoints" is a hard
  boundary at any plan tier — a design that violates it is invalid, not a
  trade-off. The **subscription tier is not** such a boundary: design what
  the work needs and let the cost be visible.
- **Simplest thing that satisfies the criteria wins.** The architect's job is to
  remove work, not to add structure.
