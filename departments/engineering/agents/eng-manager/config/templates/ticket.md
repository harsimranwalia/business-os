# Ticket template

One file per ticket at `agents/eng-manager/board/{ENG-NNN}-{slug}.md`.
The ticket is the spine — every other artifact links back to it, and every state
transition is written here by the agent that made it.

```markdown
---
id: ENG-000
title: One line, imperative, what changes
project: <project>          # must exist in config/projects.md
type: feature               # feature | bug | chore | security | spike
size: M                     # XS | S | M | L  (XL must be split)
severity: P2                # P0 | P1 | P2 | P3 — how bad the problem is. The AGENT's call.
priority:                   # now | next | hold | empty — what to work first. THE PRINCIPAL'S call.
                            # Empty is the default and means the EM orders it. Never set or
                            # change this on your own judgement: severity is where an agent
                            # argues that something matters, priority is where the approver
                            # answers.
                            # `hold` at ready/building/in-review/in-qa/in-security/ready-to-ship
                            # is an ENFORCED violation — the approver said don't start it and
                            # you did.
state: intake               # see config/definition-of-done.md
owner: product-manager      # the agent holding it right now — or `approver` at a gate
lane: full                  # full | fast | advisory (L0)
blocked_on:                 # agent | approver — required whenever state is `blocked`
blocked_from:               # the state this ticket left to enter `blocked` — written on entry, read on the way out
source: approver           # approver | filer | kanban | delivery | proposal
                            # `filer` = a request from a non-approver human, filed to
                            # inbox/requests/ and shaped by the PM like any other intake.
                            # `proposal` = an agent-originated finding the approver approved
                            # in the weekly report's batched G1. Agents no longer file tickets
                            # directly (qa/security/devops/architect are proposal sources now,
                            # not ticket sources) — see agents/eng-manager/proposals.md. The
                            # exception is a P0 on a project not on the internal lane, which
                            # keeps its agent source.
created: YYYY-MM-DD
updated: YYYY-MM-DD
branch:                     # set by the engineer at `building`
depends_on: []              # ticket IDs that must ship first
blocks: []
parent:                     # the ticket this one was split out of — ANOTHER ticket's id, never its own
links:
  prd:
  design:
  adrs: []
  review:                   # agents/principal-engineer/reviews/{ID}.md — receipt
  test_plan:                # agents/qa/test-plans/{ID}.md — receipt
  security_review:          # agents/security/reviews/{ID}.md — receipt
  release:
  pr:
---

## Problem

Two or three sentences. What is wrong or missing, for whom, and what it costs.
No solution here.

## Outcome

What is true when this is done, in observable terms.

## Notes

Context the next agent needs and can't get from the linked artifacts.

## Log

Append-only. One line per state transition, newest last.

- `YYYY-MM-DD` `intake → shaped` (eng-manager) — sized M, project <project>
- `YYYY-MM-DD` `shaped → awaiting-scope` (product-manager) — PRD written, G1 raised
```

## Rules

- **The log is append-only.** Never rewrite history; a wrong entry gets a
  correcting entry.
- **`owner` is always exactly one name** — an agent, or `approver` while the
  ticket sits at a gate (`awaiting-scope`, `awaiting-decision`,
  `awaiting-release`, or `blocked` with `blocked_on: approver`). A ticket
  with no owner is a dead end and the build loop will flag it.
- **`state` and `owner` move together.** Changing one without the other is a bug
  in the pipeline, not a shortcut.
- **`blocked` requires `blocked_on` set and three things in the log:** what's
  blocking, who owns the unblock, and what condition clears it. `blocked_on:
  approver` counts against the approval cap and holds its WIP slot — see
  `definition-of-done.md`.
- **`blocked` also requires `blocked_from`, written on entry and read on the way
  out.** It holds the state the ticket left — `building`, `in-review`,
  `in-security`, whatever it was. Set it in the same write that sets `state:
  blocked`; the ticket returns to it when the blocker clears, and clearing the
  field is part of that same write. **Its presence is enforced** — since ENG-009
  `lib/eng-gate-check.sh` counts a `blocked` ticket with no `blocked_from` as a
  violation and exits 1. Where the ticket *goes* when it leaves is still prose.
  Without it, leaving `blocked` is a guess a
  later pass has to reconstruct from the log, and the guess is forward — which is
  how a ticket skips the gate it was sitting at. `lib/eng-gate-check.sh` reads
  this field.
- **The three receipt links name files, and the files are what count.**
  `review`, `test_plan` and `security_review` point at
  `agents/principal-engineer/reviews/{ID}.md`, `agents/qa/test-plans/{ID}.md`,
  and `agents/security/reviews/{ID}.md`. A full-lane ticket may not sit at
  `shipped` or `verified` unless all three exist on disk and are non-empty; a
  fast-lane ticket owes the first one only. Each is written by its gate on a
  **`pass` verdict only** — a receipt is the record that a gate was cleared, not
  that it was reached. Filling the field without the file is not a receipt:
  `lib/eng-gate-check.sh` reads the filesystem, never the frontmatter.
- **`parent` names ANOTHER ticket, and never itself.** It is set on a sub-ticket
  when an M/L ticket is decomposed, and it points at the ticket the work was
  split out of. Since ADR-003 it is not bookkeeping: a parent at `shipped` or
  `verified` owes **no receipts of its own**, because its evidence is its
  children's — so this one field decides whether the department's only enforced
  surface asks a ticket for three files or for none. The exemption applies only
  when the parent has at least one child, **every** child is at `shipped`,
  `verified` or `dropped`, and at least one is at `shipped` or `verified`.
  Children are checked normally; delegation moves receipts, it does not delete
  them.

  **A ticket may not be its own parent, and a ring of tickets may not be each
  other's.** `parent:` set to a ticket's own id would otherwise make it its own
  settled, shipped child and drop all three receipts at exit 0 — one line,
  silent, cheaper than every bypass the check already guards. Two tickets naming
  each other did the same, as did a ring of three. `lib/eng-gate-check.sh` prunes
  any `parent:` edge that closes a cycle and reports the ticket, so the attempt
  makes the board louder rather than quieter — and a `parent:` naming a ticket
  that is not on the board is reported too. Filed as B1 on ENG-009's review round
  1, where the rule existed only in ADR-003, which is not a file anyone reads
  while writing a ticket.
- **`lane` is set at intake and can only move one way** — a ticket drops from
  `fast` to `full`, never the reverse.
- **IDs are never reused.** Next ID lives in `agents/eng-manager/board/_index.md`.
