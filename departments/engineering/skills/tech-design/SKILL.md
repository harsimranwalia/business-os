# Skill: tech-design

**Owner:** architect
**Model:** opus (design judgment + one-way-door calls)
**Trigger:** a ticket enters state `designed`, dispatched by eng-manager
**Suppressed when:** sabbath, retreat

---

## Purpose

Turn an approved PRD into a technical design an engineer can build from, decide
everything that's reversible, and escalate only the one-way doors.

---

## Inputs

- `agents/product-manager/specs/{ENG-NNN}-{slug}.md` — acceptance criteria (required)
- `agents/eng-manager/board/{ENG-NNN}-{slug}.md`
- `agents/eng-manager/config/projects.md` — hard constraints, autonomy level
- `agents/eng-manager/config/engineering-standards.md`
- `agents/architect/config/ai-architecture-standards.md` — if the change touches models
- `agents/architect/decisions/` — prior ADRs on this project
- `agents/eng-manager/config/decision-journal.md` — what the approver has
  actually decided on this project and this kind of change. A design that
  contradicts a standing pattern there needs to say why it's different, not
  ignore it.
- `agents/eng-manager/observations.md` — has anyone noticed something here
  already? An observation about this area is often the real constraint.
- The project's own code — conventions, existing patterns, what's already there
- `.env` → `MODE`

---

## Steps

### 1. Mode check

`sabbath` or `retreat`: exit without writing.

### 2. Read the codebase before designing

Non-negotiable. A design that fights the project's existing shape costs more
than it saves. Find how this project already solves adjacent problems and match
it. Note any existing pattern you're deliberately breaking, and why — that's an
ADR.

### 3. Check the hard constraints

From `projects.md`. A project may mark something invalid at any plan tier —
e.g. metered API billing, deployed endpoints. A design that breaks a marked
constraint is **invalid** — redesign, don't negotiate.

The **subscription tier is not** in that category. Don't cripple a design to fit
the current plan; build what the work needs and let the cost be visible. If the acceptance criteria genuinely cannot be met within the
constraints, that goes back to the PM through the EM before any code.

### 4. Design the smallest thing that satisfies the criteria

Not the most elegant. Not the most extensible. The smallest. Walk each
acceptance criterion and confirm the design satisfies it — if one can't be met,
stop and raise it now, not in QA.

### 5. Design the failure before the feature

Explicitly: timeouts, bounded retries, idempotency, partial writes, concurrent
access, empty and boundary inputs, third-party contract changes, and what the
user sees when each breaks. A design that only describes the happy path is
unfinished.

### 6. AI architecture section — when `touches_models`

`ai-architecture-standards.md` is binding. All seven subsections required:
placement and failure behaviour, model choice and fallback, prompt and context
provenance, output contract and malformed behaviour, evaluation and drift
detection, cost limits and kill switch, trust boundary.

First ask whether it needs a model at all — a parser, rule, or lookup beats a
model call on cost, latency, and debuggability. Then ask whether a smaller model
does the job. Verify current model IDs rather than trusting memory; they change.

### 7. Data section — when `touches_data`

State the intent and the constraints only: what needs storing, how it will be
queried, expected volume and growth. `database` owns the schema and the
migration — hand it over via `skills/schema-change/SKILL.md`. Do not design the
tables yourself.

### 8. Identify one-way doors

A decision is one-way when reversing it is expensive: new datastore, new vendor,
auth model change, public contract, a data model that's painful to migrate,
anything with recurring cost.

- **Reversible** → decide it, log an ADR if it's worth a record, move on.
  Escalating a reversible decision wastes the resource this department exists to
  protect.
- **One-way** → escalate at G2, with the trade-off in two sentences and a
  recommendation. Still your recommendation; the approver's call.

### 9. Write the alternatives section

At least one rejected alternative with the honest reason. "We didn't have time"
is a real reason and more useful to a future reader than a rationalisation.

### 10. Write the design and any ADRs

Design → `agents/architect/designs/{ENG-NNN}-{slug}.md` from the template, sized
to the change. ADRs → `agents/architect/decisions/ADR-{NNN}-{slug}.md`,
incrementing `next_id` in `_index.md` in the same write.

### 11. Route

- **L0 project (`<project>`):** state `advised`, owner `eng-manager` —
  **terminal.** Package the design and its findings for the approver to carry
  into the client's own process. Nothing is built, branched, or scanned. An L0
  ticket must never reach `ready`.
- **One-way door escalated:** state `awaiting-decision`, owner `approver`, G2
  package to the EM.
- **Otherwise:** state `ready`, owner `eng-manager` (work-breakdown next).

Append one line to the ticket log.

---

## Outputs

| File | Purpose |
|---|---|
| `agents/architect/designs/{ENG-NNN}-{slug}.md` | The design |
| `agents/architect/decisions/ADR-{NNN}-{slug}.md` | 0..n decision records |
| `agents/architect/decisions/_index.md` | `next_id` incremented, row added |
| ticket frontmatter | `links.design`, `links.adrs`, `touches_data`, `touches_models` |

---

## Trace

`traces/architect-{run-id}.json` — ticket ID, ADRs written, one-way doors found
and escalated, constraints checked.

---

## Failure modes to avoid

- **Escalating a reversible decision.** Decide it.
- **Speculative generality** — structure for a use case that doesn't exist.
- **Designing without reading the codebase.**
- **A design that can't satisfy an acceptance criterion**, discovered in QA.
- **Bundling a refactor.** Separate ticket, always.
- **Silence on failure behaviour.** That silence becomes a production incident.
