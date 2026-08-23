# ADR template

Architecture Decision Record. Written by `architect` at
`agents/architect/decisions/ADR-{NNN}-{slug}.md`. Numbered sequentially across
all projects; next number lives in `agents/architect/decisions/_index.md`.

An ADR is a record, not a proposal. It is written when the decision is made, not
before, and it is never edited afterwards — a decision that changes gets a new
ADR that supersedes the old one.

```markdown
---
id: ADR-000
title: Short noun phrase — "Postgres for the ordering read model"
project: <project>
ticket: ENG-000
status: accepted          # accepted | superseded | reverted
decided_by: architect     # architect | approver (G2) | approver (risk acceptance)
date: YYYY-MM-DD
supersedes:
superseded_by:
---

# ADR-000: {Title}

## Context

The situation that forced a decision. Constraints in play — technical, cost,
time, the project's autonomy level, someone else's codebase. Two paragraphs at
most.

## Decision

What was decided, in the active voice. One paragraph.

## Alternatives

| Option | Why not |
|---|---|
| {alternative} | {the honest reason} |

## Consequences

**Accepted:** what gets harder or more expensive because of this.
**Gained:** what gets easier.
**Reversibility:** cheap / moderate / one-way, and what reversing would cost.

## Review trigger

The condition under which this decision should be revisited — a scale threshold,
a cost threshold, a date, a change in the product. If there isn't one, say so.
```

## When to write one

- Any one-way door, whoever decided it
- Any deviation from `engineering-standards.md` or a project's own conventions
- Any accepted security risk (the approver's decision, recorded verbatim)
- Any divergence from an upstream vendored dependency
- Any choice a future engineer would otherwise ask "why on earth" about

## When not to write one

- Routine implementation choices inside a single module
- Anything already covered by the standards
- Decisions still being made — that's the design doc's "alternatives" section

## Rules

- **Never edit an accepted ADR.** Supersede it.
- **Record rejected options honestly.** "We didn't have time" is a real reason
  and worth more to a future reader than a rationalisation.
- **A reverted decision still keeps its ADR**, marked `reverted`, with the new
  one linked. Deleting the record deletes the lesson.
