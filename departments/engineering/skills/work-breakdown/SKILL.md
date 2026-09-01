# Skill: work-breakdown

**Owner:** eng-manager
**Model:** sonnet (sequencing and assignment — mechanical once the design exists)
**Trigger:** a ticket enters state `ready`
**Suppressed when:** sabbath, retreat

---

## Purpose

Turn a technical design into assigned, sequenced sub-tickets that can be built
without anyone waiting on an answer.

---

## Inputs

- `agents/architect/designs/{ENG-NNN}-{slug}.md` (required)
- `agents/product-manager/specs/{ENG-NNN}-{slug}.md` — acceptance criteria
- `agents/eng-manager/board/_index.md` — WIP state and `next_id`
- `agents/eng-manager/config/projects.md` — autonomy level
- `.env` → `MODE`

---

## Steps

### 0. Autonomy check — before anything else

Read the ticket's project in `agents/eng-manager/config/projects.md`.

**If the project is L0 (`<project>`): stop. This skill must not run.** An L0
ticket terminates at `advised` — it never reaches `ready`, because breaking it
down would assign work to engineers who are forbidden to write code on that
repo. Route it back to the EM to package as an advisory for the approver.

This guard exists because the failure it prevents lands on a live client
engagement, not a hypothetical. Caught in review 2026-07-27.

### 1. Mode and WIP check

`sabbath` or `retreat`: exit. Then check WIP against `config.yaml` → `wip.limit`
(default 2). **At the limit, stop here** — the ticket stays at `ready` and waits.
Starting a third parallel ticket produces a queue of finished-but-unapproved
work landing on the approver, which is the failure this department was built
to prevent.

### 2. Split by surface, not by layer of effort

One sub-ticket per owning agent per coherent unit of work:

| Surface | Owner |
|---|---|
| Schema, migration, indexes | `database` |
| APIs, services, jobs, integrations | `backend` |
| UI, client state, routing | `frontend` |

A sub-ticket that needs two agents is split wrong. If a piece genuinely can't be
split, assign it to the agent whose surface dominates and note the dependency.

### 3. Sequence by dependency

Data before the code that reads it. Contract agreed before either side builds
against it. Anything that unblocks two other pieces goes first.

Write the order explicitly in the parent ticket. `depends_on` and `blocks` in
each sub-ticket's frontmatter. A sub-ticket whose dependency isn't shipped
doesn't start.

### 4. Confirm each sub-ticket is answerable

Before assigning, check the sub-ticket can be built without the engineer needing
a decision nobody has made. If it can't, the design has a gap — return the parent
to `designed` with the specific question. Do not hand an engineer an unanswered
question and expect them to invent an answer.

### 5. Create the sub-tickets

From `config/templates/ticket.md`, one file each, incrementing `next_id` in
`board/_index.md` per creation. Each carries: parent ticket ID, the design
section it implements, the acceptance criteria it serves, the owner, and the
sequence position.

### 6. Assign and dispatch

Set each sub-ticket to `building` with its owning agent, in sequence order. Only
the sub-tickets whose dependencies are met start now; the rest stay at `ready`.

### 7. Update the board

`board/_index.md` — the in-flight table, the WIP count, and `next_id`.

---

## Outputs

| File | Purpose |
|---|---|
| `agents/eng-manager/board/{ENG-NNN}-{slug}.md` | Sub-tickets, one per surface |
| Parent ticket | Breakdown, sequence, and links to sub-tickets |
| `agents/eng-manager/board/_index.md` | `next_id`, in-flight view, WIP count |

---

## Trace

`traces/eng-manager-{run-id}.json` — parent ticket, sub-tickets created, WIP
before and after, anything held at `ready` and why.

---

## Failure modes to avoid

- **Breaking the WIP limit** because the work "feels parallel". It isn't; the
  approver's WIP limit is the real constraint.
- **Sub-tickets that span two agents.** Split again.
- **Assigning work with an open question in it.** Send it back to design instead.
- **Sequencing by convenience** rather than by dependency — the frontend building
  against an unbuilt contract is the classic version of this.
