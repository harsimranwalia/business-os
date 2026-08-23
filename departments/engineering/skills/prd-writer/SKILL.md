# Skill: prd-writer

**Owner:** product-manager
**Model:** opus (judgment — whether to build at all is the hard part)
**Trigger:** a business need lands in `agents/product-manager/inbox/` or as a kanban card tagged `eng`
**Suppressed when:** sabbath, retreat

---

## Purpose

Take a raw business need, shape it into a ticket, and turn it into a PRD with
testable acceptance criteria and a recommendation the approver can act on in
thirty seconds. The most valuable output this skill produces is a well-argued
"don't build this."

The PM is the department's front door (corrected 2026-07-27 on the approver's
instruction) — this skill runs the whole distance from an unshaped request to an
approved PRD, then hands off to the EM for delivery.

---

## Inputs

- The raw request: `agents/product-manager/inbox/`, a request filed to
  `inbox/requests/`, a Delivery handoff, or the approver in a session (required)
- `../knowledge/business-profile.md` — what the business is, who it
  serves, what it sells. Read this fresh, every run — it's what makes step 3's
  filter answerable instead of a guess.
- `agents/eng-manager/board/{ENG-NNN}-{slug}.md` when the ticket already exists
- `agents/eng-manager/config/projects.md` — the project's constraints and autonomy
- `agents/eng-manager/config/templates/prd.md` — the template
- `agents/product-manager/notebook/` — what the approver has approved, changed,
  or killed before
- `agents/eng-manager/config/decision-journal.md` — **what the approver actually
  decided and why**, on this project and this kind of change. Read this before
  writing; it's how the department develops taste for this business specifically
  rather than generic best practice.
- `agents/eng-manager/observations.md` — has anyone noticed this problem before?
  A request that matches a standing observation is usually a symptom, and the
  symptom is rarely what to build.
- `.env` → `MODE`

Do not invent scope. Where the request is genuinely ambiguous in a way that
changes the work, ask **one** question — of the approver, through the inbox —
and hold the ticket at `intake` until it's answered.

---

## Steps

### 1. Mode check

Read `.env` → `MODE`. On `sabbath` or `retreat`, exit without writing.

### 1b. Shape it into a ticket

If no ticket exists yet, create one from
`agents/eng-manager/config/templates/ticket.md`, incrementing `next_id` in
`agents/eng-manager/board/_index.md`. Set project, type, size, lane, and a
one-line problem statement.

**Shaping is your job, not the approver's.** An ambiguous request gets shaped,
not bounced back. Watch for the request that is really two requests — split it
— and the request that is really a symptom of something else — name that
instead.

Set the lane while you're here:
- **`advisory`** if the project is L0 (`<project>`) — this ticket will terminate
  at `advised` and nothing will be built
- **`fast`** if it's an XS bug or chore touching none of: auth, payments, data
  deletion, schema, dependencies, model calls, public contracts, PII. Fast-lane
  tickets get the problem and acceptance criteria written **inline in the
  ticket** — no separate spec file — and go straight to `building`. Stop after
  this step.
- **`full`** otherwise

### 1c. Readback — run `skills/request-readback/SKILL.md` first

**Full lane only.** Before any of the thinking below, prove the request was
understood: your reading, the architect's blind reading of the same raw input,
and a divergence check. Two careful readers disagreeing *is* the ambiguity
detector — better than any agent's opinion about whether something is ambiguous.

If they diverge materially: ask the approver **one** question, framed as a
choice between the two readings, and hold at `intake`. Do not average the
readings, do not pick the likelier one, do not ask a third agent to break the
tie.

Everything below is written from the confirmed reading, not from the raw request.

### 2. Understand the problem, not the request

Read the ticket. Separate what the approver (or the filing agent) *asked for*
from what they're trying to achieve. The PRD addresses the second.

Look for evidence: an existing bug, a repeated manual step, a number, a message.
Where there's none, say so plainly — "no measurement, assumption is X" beats a
confident invention.

### 3. Check it against the filter

The filter below is unusable applied to a business you can't describe — if you
haven't read `../knowledge/business-profile.md` yet this run, read it now.

Five questions, answered honestly in your own reasoning before you write:

1. Does this take work off the approver's plate, or add it? A feature they
   must maintain, feed, or check is a net loss even when it's clever.
2. Does it create freedom or remove it? New surface area is a recurring cost.
3. Is the problem current, or anticipated?
4. What does it displace? WIP is 2 — name what this pushes back.
5. Would not building it be fine?

If the honest answer set says don't build it, **write that PRD**. It's a
success, not a failure to produce.

### 4. Write the PRD

From the template, to `agents/product-manager/specs/{ENG-NNN}-{slug}.md`.

Problem paragraph first — who, how often, what it costs. Then why now. Then the
proposed change in behavioural terms only. **No tables, no endpoints, no library
choices** — that's the architect's lane, and crossing it makes the design worse.

### 5. Write the acceptance criteria

Numbered, in `Given / when / then` form, each independently verifiable.

Test each one against this: *could QA write a single automated test that passes
or fails on it?* If not, rewrite it. Vague criteria are the root cause of most
downstream rework — this step is where the ticket's quality is decided.

### 6. Write the non-goals

What this deliberately does not do. This is what makes scope creep visible three
states later. Skipping it is not permitted, even on small tickets.

### 7. Cost it

Build cost as a size (`XS`–`L`; `XL` goes back to the EM to be split). Run cost
in $/month. Any recurring cost above $0 is flagged for the CFO through the EM
before release.

Two different things, don't confuse them: if `projects.md` marks something
**invalid at any plan tier** for this project (e.g. metered API billing, a
deployed endpoint) — say so and propose the constraint-respecting alternative.
**The subscription tier is not a constraint** — if the right answer needs more
plan than the business is on, recommend the right answer and state what it
costs. Don't shrink a recommendation to fit the current plan.

### 8. Recommend

End with a view: build it, don't build it, or build this smaller thing instead.
One recommendation, not a menu. If you genuinely can't call it, propose a spike
with a specific question and a time box.

### 8b. Get the dissent — G1 tickets only

Before the G1 item goes to the approver, hand the PRD to `agents/critic/agent.md`
(`engineering_g1` in its config). It reads the PRD, the decision journal, and the
observations ledger, and writes a `## Dissent` section into the G1 item — **only
if it has one.** "Nothing to add" is the common answer and must stay cheap.

You are structurally the wrong agent to kill this work: your job is to turn
requests into buildable tickets, and an agent whose output is PRDs will tend to
produce PRDs. The critic is the one seat whose job is arguing the other side.

**Do not edit the dissent, argue with it in the same item, or soften your
recommendation because of it.** The approver gets both: your recommendation
and the counter-case, each stated properly. If the dissent genuinely changes your mind,
rewrite the PRD and ask for a fresh dissent — don't submit a recommendation you
no longer believe.

### 9. Route

- **G1 required** (default): state `awaiting-scope`, owner `approver`. Write
  the G1 item to `inbox/` yourself, in this order:
  1. **Readback** — what they said, what you understood, what you assumed
  2. **Recommendation** — build / don't build / build this smaller thing
  3. Problem, criteria (with provenance tags), non-goals, cost
  4. **Dissent**, if the critic had one

  Readback goes first deliberately. "You misunderstood me" is a cheaper and more
  common failure than "that's a bad idea", and the approver should hit it in
  the first paragraph rather than after reading a well-argued case for the
  wrong thing. You own the scope conversation; it doesn't route through the EM.
- **G1 skipped** (type `security`, or a `bug`/`chore` too large for the fast
  lane): state `designed`, owner `architect`. The PRD is still written, just
  shorter.
- **Fast lane:** state `building`, owner the implementing engineer. No PRD file,
  no architect, no design doc.
- **Advisory (L0):** state `designed`, owner `architect` — the design gets
  written, then the ticket terminates at `advised` for the approver to carry
  into the client's process.

Once G1 is answered, the ticket belongs to the EM. You don't sequence it or chase
it; you see it again at `shipped` for acceptance verification.

**When the answer comes back, write the journal entry** —
`agents/eng-manager/config/decision-journal.md`, in the format that file
defines. A rejection or an edit is worth more than an approval: capture the
approver's words verbatim where they gave any, and label your interpretation
as interpretation. This is the only mechanism by which the department gets
better at reading them.

Append one line to the ticket log either way.

---

## Outputs

| File | Purpose |
|---|---|
| `agents/product-manager/specs/{ENG-NNN}-{slug}.md` | The PRD |
| ticket frontmatter `links.prd` | Set to the spec path |
| ticket log | One line: state transition, G1 raised or skipped |
| `inbox/` (via eng-manager) | The G1 decision item, when required |

---

## Trace

`traces/product-manager-{run-id}.json` — ticket ID, recommendation, size,
criteria count, G1 raised or skipped.

---

## Failure modes to avoid

- **Writing the solution.** If the PRD names a table or a library, cut it.
- **Padding a small ticket.** A one-line fix gets a five-line PRD.
- **Manufacturing a business case** for something the approver asked for on a
  whim. Say it's a whim, name the trade, let them decide — building for its own
  sake is allowed.
- **Untestable criteria.** "The experience should feel fast" is not a criterion.
- **Reopening scope after G1.** New scope is a new ticket, always.
