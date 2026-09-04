---
id: ADR-014
title: Customer chat-bar questions are shown to the owner verbatim — no redaction, no new copy, no export, never in a URL or a log line
project: restaurant-portal
ticket: ENG-021
status: accepted
decided_by: architect
date: 2026-09-03
supersedes:
superseded_by:
---

# ADR-014: Customer chat-bar questions are shown to the owner verbatim — no redaction, no new copy, no export, never in a URL or a log line

## Context

`ENG-021`'s questions view renders free text customers typed into a public
website's chat bar. Customers type anything: names, phone numbers, addresses,
allergies, health details. The PRD named this as an open risk and explicitly
declined to resolve it by omission — "the architect and security gate should
look at this plainly rather than it being an accident of shipping a log
viewer" — and the G1 approval passed it through unresolved rather than settling
it.

Three facts frame the answer.

**The owner is already the authorised reader.** The database's own tracked
policy grants exactly this — `"Restaurant managers can view their restaurant
conversations"`, `FOR SELECT`, `USING (user_has_restaurant_access(auth.uid(),
restaurant_id::uuid))` — and has since 2025-09-03. This ticket does not widen
who may read the data. It builds the first surface that uses a grant already
written for this exact purpose.

**The customer is talking to the restaurant.** A question typed into a
restaurant's own website chat bar has the same custodial shape as a phone call
to that restaurant or the free-text note on their order. Withholding it from the
owner would not protect the customer; it would only mean the message reached no
one.

**Redaction is not a free improvement.** A regex scrubber over open text fails
in both directions at once. It over-redacts the case that justifies the page —
"my son is allergic to peanuts, is the pad thai safe?" is exactly the question an
owner needs to read and exactly what a naive PII filter mangles — and it
under-redacts, since most identifying detail in natural language matches no
pattern. A page that shows redacted text also invites the belief that what
remains has been made safe.

## Decision

Questions are rendered **verbatim and unredacted** to the authorised owner. The
protection is not transformation of the text; it is the five properties below,
each of which is a design constraint the build must satisfy:

1. **No new copy.** The view is read-only over existing rows. Nothing is
   duplicated into a new table, a cache, local storage, or a derived "questions"
   entity. The data lives in exactly the one place it already lived, under the
   one policy that already guards it.
2. **Never in a URL.** The "Add to FAQs" hand-off carries the question in
   react-router location state, not a query parameter — free text in a URL lands
   in browser history and in every upstream access log, which is the "no PII in
   log lines" rule broken through a side door.
3. **Never in a log line or an error payload.** Query failures log the PostgREST
   error code; they never log the rows, the payload, or any question text. No
   error reporter receives it.
4. **The customer's own turns only.** `role: 'assistant'` messages are never
   rendered. This halves what is on screen and confines the surface to what the
   customer chose to type — and it is what AC6 asks for independently.
5. **No export.** No CSV, no download, no copy-all. An export creates an
   uncontrolled copy outside the RLS boundary, on a laptop, forever — the single
   change most likely to turn an authorised view into a data-loss event.

Retention is inherited, not extended: the page shows whatever
`cleanup_old_ai_conversations` has left, and this ticket changes neither the job
nor the window.

The page carries one line of plain copy stating that these are customers' own
words, shown as typed. That is the honest framing, and it is also what makes an
owner think before pasting one into a public FAQ.

## Alternatives

| Option | Why not |
|---|---|
| **Regex-redact emails, phone numbers and card-shaped digits before display** | Fails in both directions simultaneously (see Context). It also creates a false assurance: an owner shown partially-masked text reasonably infers the rest was checked, and it was not. If redaction is wanted it needs its own acceptance criteria and its own evaluation of what it misses — a follow-on ticket, not a silent filter bolted onto a log viewer. Explicitly a PRD non-goal. |
| **Truncate each question to N characters** | Cheap and superficially safer, but PII is usually at the start of a sentence, not the end, so it removes the meaning while keeping the identifier. It also breaks the feature: a truncated question cannot be judged worth an FAQ. |
| **Show only aggregate/derived signals** (counts, topics) and never raw text | Would sidestep the risk entirely — and would not satisfy AC1 or AC3, both of which are about the owner reading and acting on the actual question. It is also the PRD's explicitly deferred "quality/gap metric," not this ticket. |
| **Restrict the page to a narrower role than "restaurant manager"** | There is no narrower role. `restaurant_managers` membership is the grain the existing policy, the portal's restaurant switcher, and every other owner-facing page already use. Inventing a role for one page would be a real auth-model change for no measurable reduction in exposure. |
| **Add an export button** ("owners will want it") | Nobody asked for it, and it is the one addition that moves data outside the boundary everything else here is built on. Left out deliberately rather than by oversight — recorded here so its absence is not read as a gap to fill. |

## Consequences

**Accepted:** a restaurant owner can read whatever a customer typed, including
information the customer may not have meant to volunteer, and the platform has
made that easier than it was yesterday. That is the deliberate trade: the grant
already existed, the alternative protections are worse than the exposure, and
the residual risk is bounded by the five constraints above rather than by a
filter that would claim more than it delivers. The security gate reviews this
decision as stated, which was the PRD's actual request — that it be looked at
plainly rather than happen by accident.

**Gained:** the exposure surface is smaller than the raw data, not equal to it —
half the transcript is never rendered, nothing is copied, nothing leaves the
authorised session, and nothing reaches a log. A page built without these
constraints would look identical to the owner and be materially worse.

**Reversibility:** every constraint is a code-level property with no data
consequence. Adding redaction later is a pure display-layer change over
unmodified rows; removing the page is deleting a route. Nothing here is written
to disk, so nothing has to be unwound.

## Review trigger

Revisit if the security gate on this ticket reaches a different conclusion —
this ADR is the artifact it reviews, and its verdict supersedes. Revisit if any
future ticket proposes an export, a staff-facing mirror (which would widen the
reader set beyond the restaurant's own managers, a genuinely different
question), or notification/digest emails containing question text, since each
moves the data out of the boundary this decision depends on. Revisit if a
customer-facing privacy notice or consent flow lands on the chat bar itself,
since that would change what the customer has been told and therefore what the
honest framing on this page should say.
