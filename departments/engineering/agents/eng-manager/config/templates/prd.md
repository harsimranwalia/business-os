# PRD template

Written by `product-manager` at `agents/product-manager/specs/{ENG-NNN}-{slug}.md`.
This is the document the approver reads at Gate 1. Keep it to one screen
unless the problem genuinely needs more — a long PRD is usually an unsplit
ticket.

```markdown
---
ticket: ENG-000
project: <project>
status: draft            # draft | awaiting-scope | approved | rejected | superseded
size: M
author: product-manager
created: YYYY-MM-DD
decided: YYYY-MM-DD      # when the approver answered G1
---

# {Title}

## Readback

Written first, read first. The approver confirms **meaning and scope in the
same tap** — if the readback is wrong they stop at the first paragraph and the
department is saved from building the wrong thing correctly. See
`skills/request-readback/SKILL.md`.

**You said:** "{verbatim — never cleaned up, never paraphrased}"

**Understood as:** {one paragraph}

**Assumed, and worth correcting if wrong:**
- {each inference that would change the build if it turned out wrong}

**Second reading agreed / diverged on:** {what the architect's blind reading
matched or differed on, and how it was resolved}

## Problem

Who has this problem, how often, and what it costs them today. Evidence if
there is any — a bug count, a support message, a number. If there's no evidence,
say so plainly; an assumption named is fine, an assumption hidden is not.

## Why now

Why this, ahead of everything else on the board. If the honest answer is "no
particular reason", that belongs here too — it's a fair reason for the
approver to say not yet.

## Users

Who this is for. For internal work on the instance's own tooling this is
usually the approver, and the answer still matters: which of their jobs gets
easier.

## Proposed change

What the user can do afterwards that they can't do now. Behaviour, not
implementation — the architect owns how.

## Acceptance criteria

Numbered, testable, each one independently verifiable. QA writes a test per
criterion, so a criterion that can't be tested isn't a criterion.

**Every one carries its provenance** — if you can't point at where a requirement
came from, it's scope that got invented somewhere:

- `[stated]` the approver said it
- `[inferred]` both readings agreed without it being said
- `[confirmed]` the approver answered a question about it
- `[proposed]` the department thinks it belongs; the approver hasn't weighed in

1. `[stated]` Given {context}, when {action}, then {observable result}
2. `[inferred]` ...
3. `[proposed]` ...

## Non-goals

What this deliberately does not do. This section is what makes scope creep
visible later — take it seriously.

## Risks and unknowns

What could make this the wrong call, and what we'd have to learn to know.

## Cost

- Build: rough size, a rough build-time estimate (see `definition-of-done.md`'s
  Size table for the band; narrow it with specifics when this ticket has them),
  and what it displaces on the board
- Run: recurring $/month, if any. Anything above zero goes to CFO before release.

## Decision

Filled in after G1.

- **The approver's answer:** approved / rejected / changed to {…}
- **Date:**
- **Notes:**
```

## Rules

- **Acceptance criteria before code.** A PRD without them doesn't leave `shaped`.
- **The PM writes the problem, not the solution.** If the PRD is describing
  tables and endpoints, it has crossed into the architect's lane.
- **Recommend.** The approver gets a recommendation, not a menu. Say what you'd do and why.
- **Say when it isn't worth it.** A PRD that concludes "don't build this" is a
  successful PRD and the highest-value thing this agent produces.
- **Auto-approved types skip G1** (XS, bug, chore, security) — the PRD is still
  written, just shorter, and it goes straight to `designed`.
