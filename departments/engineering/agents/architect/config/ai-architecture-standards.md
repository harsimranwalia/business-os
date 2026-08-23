# AI Architecture Standards

Binding on any design where `touches_models: true` — a model call, an agent
loop, a tool, an MCP server, a RAG pipeline, or an eval. Owned by `architect`,
enforced at the design stage and re-checked at the security gate.

Code-level rules live in `agents/eng-manager/config/engineering-standards.md`
(the AI/LLM section). This file is about *shape*.

## The first question

**Does this need a model at all?** A regex, a lookup table, a rule, or a
deterministic parser beats a model call on cost, latency, reliability, and
debuggability. Use a model when the input is genuinely open-ended and the task
needs judgment or language. "It would be cool" is not a reason.

The second question: **can a smaller model do it?** Extraction, classification,
tagging, and arithmetic don't need frontier reasoning. Route on task fit — the
same rule `config/conventions.yaml` already applies to skills.

## Placement

Every model call is placed in exactly one of three positions, and the choice
determines everything downstream:

| Placement | When | Requirements |
|---|---|---|
| **In the request path** | The user is waiting | Hard timeout, streaming where it helps, a non-model fallback for timeout, a visible failure state |
| **In a background job** | Nobody is waiting | Bounded retries, idempotency, dead-letter path, success/failure visible to `devops` |
| **In an agent loop** | Multi-step with tools | Step cap, token budget, wall-clock cap, kill switch, and an audit trail of every tool call |

A model call with no defined behaviour when it is slow, unavailable, or wrong is
not a design. State that behaviour explicitly.

## Model choice and routing

- Name the model and the reason: task fit, cost, latency, context window.
- Name the fallback and when it triggers. "It'll retry" is not a fallback.
- Model IDs are configuration, never literals in business logic — they change,
  and a hardcoded ID becomes a silent outage.
- Verify current model IDs at design time rather than trusting memory; they move.
- Pin behaviour, not just the ID: a prompt tuned against one model is not
  portable, and swapping models is a change that goes through the pipeline.

## Prompts and context

- Prompts are version-controlled files, never strings concatenated inside
  business logic. A prompt change is a code change and gets reviewed like one.
- **Provenance is tracked.** Every piece of content entering a context window is
  labelled: system, trusted application data, or untrusted external input.
- Untrusted input — user text, web pages, emails, PR comments, tool output,
  retrieved documents, file contents — is delimited and explicitly marked as
  data, not instruction.
- Context is assembled deliberately. Dumping everything available into the
  window is a cost, latency, and accuracy problem at once.
- No secrets, credentials, or `Restricted`-class data in a prompt (see
  `agents/eng-manager/config/security-baseline.md` → data classification).

## Output contract

- Every model output crossing into business logic is parsed against a schema
  before use. Structured output modes where the provider supports them.
- **Three failure cases have defined, tested behaviour:** malformed output,
  empty output, and confidently wrong output. The third is the one that gets
  skipped and the one that hurts.
- Model output never becomes a command, a file path, a URL to fetch, a
  recipient, a query, or a permission decision without validation against an
  allowlist.
- Confidence is not a score the model reports. If the design needs to know when
  the model is unsure, that's an evaluation problem, not a prompt instruction.

## Trust boundary

The rule: **a model-driven action can never exceed the authority of the user on
whose behalf it runs.**

- Tools available to a model are scoped to the least authority the task needs.
- Destructive tools — delete, send, pay, deploy, publish — require a
  confirmation path a prompt injection cannot forge. A model saying "the user
  approved this" is not approval.
- An agent that reads untrusted content and also holds a destructive tool is a
  design smell. Split the roles, or gate the tool behind a human.
- Nothing auto-sends, auto-publishes, or auto-commits outside what the
  approver has explicitly authorised. Silence is not approval, and a model
  cannot manufacture consent.

## Evaluation

- **How would we know this stopped working?** Answer it in the design or the
  design isn't finished. Silent degradation is the characteristic failure mode
  of model-backed features — nothing throws, results just get worse.
- Every model-backed feature ships with an eval set: a small, versioned set of
  inputs with known-good outputs, runnable on demand. Ten good cases beat a
  thousand generated ones.
- Regression: the eval runs before any prompt or model change ships.
- Log inputs and outputs where classification allows, so failures are
  reconstructable. Redact `Restricted` data.

## Cost and limits

- Every model call has a token budget. Every loop has a call cap and a
  wall-clock cap. Every autonomous loop has a kill switch.
- **Unbounded model spend is a denial-of-wallet vulnerability**, not just a
  budgeting problem — treat it as a security property.
- Estimate recurring cost at design time in $/month at expected volume, plus the
  worst case if a loop misbehaves. Anything above zero goes to the CFO through
  the EM before release.
- **For anything this department builds as part of the instance's own
  tooling, architectural at any plan tier: no Anthropic API billing, no
  deployed endpoints.** Designs route through Claude Code sessions, events,
  and MCP connections that cost nothing extra. Not negotiable, not a
  trade-off — metered spend has no ceiling where a subscription does.
- The **subscription tier is a setting**, not a design constraint
  (`agents/eng-manager/config.yaml` → `plan.tier`). Don't design a weaker system
  to fit the current plan; design the right one and state what it costs.

## RAG and retrieval

- Chunking, embedding model, and index are versioned together. Changing one
  without re-indexing is a silent correctness bug.
- Retrieved content is untrusted input. Always. It is delimited and labelled.
- Retrieval quality is measured before generation quality — most bad RAG output
  is a retrieval failure wearing a generation costume.
- Cite what was retrieved so an answer can be audited back to its source.

## Agents and tools

- One agent, one clear job. A multi-role agent is harder to evaluate, harder to
  debug, and more dangerous when it holds tools.
- Tool definitions are explicit about what they do, what they cost, and what
  they can destroy.
- Every tool call in an autonomous loop is logged with its arguments and result.
- Loops terminate. State the termination condition, the step cap, and what
  happens when the cap is hit.
- Human-in-the-loop is a design position, not a fallback for a weak design.
  Where the approver approves, say exactly what they see and what they're
  deciding.

## The meta-rule: building on the department's own tooling

This department can build AI systems inside an AI system — its own agents and
skills, not just client projects. The same standards apply either way: a
skill that calls a model with no output contract is the same bug whether it's
in a client project or in `skills/`. When designing changes to this system's
own tooling, the instance's own doc-authoring conventions still apply — check
the instance's root config before drafting `SKILL.md`, agent config, or
`schedules/*.md` prose.
