# Skill: request-readback

**Owner:** product-manager (second reading by architect)
**Model:** opus for both readings — this is the step where being subtly wrong is most expensive
**Trigger:** every full-lane business request, before any PRD is written
**Suppressed when:** sabbath, retreat

---

## Purpose

Turn a request into requirements, and prove the request was understood **before**
anything gets built from it.

The failure this exists to prevent: a badly-framed request produces a well-built
wrong thing, faster than a human would have built the wrong thing. Every gate
downstream checks whether the code matches the spec. Nothing checked whether the
spec matched what the approver meant.

Added 2026-07-27 at the approver's instruction — "generate the prompt from
input, then requirements, then run it."

---

## The chain

```
  input (verbatim, never paraphrased away)
     │
     ├──▶ interpretation A — product-manager, from the raw input
     │
     ├──▶ interpretation B — architect, from the raw input, BLIND to A
     │
     ▼
  divergence check ── they differ materially? → the request is ambiguous.
     │                  Ask the approver ONE question. Stop here.
     ▼
  requirements — what must be true when this is done
     │
     ▼
  the brief — what the department will actually build from
     │
     ▼
  readback at the top of the G1 item → the approver confirms meaning AND scope
                                        in one tap
```

## Why two readings

**Divergence is the ambiguity detector.** Asking one agent "is this ambiguous?"
gets you a confident yes or no with nothing behind it. Asking two agents to read
the same sentence independently and comparing them is an actual test: if two
careful readers of the same request build different pictures, the request was
underspecified, and no amount of care downstream fixes that.

The second reader must be **blind to the first**. A reader shown interpretation A
will anchor to it and agree, which produces false confidence — worse than not
checking, because it looks like verification.

`product-manager` reads for the problem. `architect` reads for what would have to
exist. Those two lenses diverge in exactly the places that produce well-built
wrong things.

---

## Inputs

- The raw request, verbatim — from `agents/product-manager/inbox/`, a request
  filed to `inbox/requests/`, a Delivery handoff, or the approver in a session
- `../knowledge/business-profile.md` — what the business is, who it
  serves, what it sells. Shared ground truth, not an interpretation — both
  readers read it (see step 3, blind does not mean uninformed).
- `agents/eng-manager/config/decision-journal.md` — has the approver asked for
  something like this before, and what happened?
- `agents/eng-manager/observations.md` — is this request a symptom of something
  already noticed?
- `agents/eng-manager/config/projects.md` — the target project's constraints

---

## Steps

### 1. Preserve the input verbatim

Copy the request into the ticket **exactly as written**, before any processing.
Not cleaned up, not corrected, not expanded. Everything downstream is derived
from it, and the original wording is the only ground truth about what was asked.

Typos and half-sentences are data too — they often mark the part the approver
cared least about phrasing carefully and most about getting.

### 2. Interpretation A — the product manager

From the raw input only, write:

- **What I think you want:** one paragraph, plain, no hedging
- **The problem underneath:** what this is really for, if the request is a
  proposed solution rather than a problem
- **What I'm inferring:** everything not literally stated but assumed. Be
  exhaustive and slightly paranoid here — this is the list that catches errors.
- **What I'd have to guess:** anything you genuinely cannot infer

### 3. Interpretation B — the architect, blind

Hand the architect **the raw input only**. Not interpretation A, not the ticket,
not the PM's inference list. It writes the same four sections independently, in
its own lens: what would have to exist for this to be true.

If interpretation A leaks into this step, the check is worthless. Blind means
blind to the *other reading*, not to the business: the architect reads
`../knowledge/business-profile.md` same as the PM did — that's shared
ground truth both interpretations should be grounded in, not a leak from one
to the other.

### 4. Compare

Put the two side by side. Classify each difference:

| Difference | Means | Action |
|---|---|---|
| Same picture, different words | Fine | Proceed |
| Different scope — one includes something the other doesn't | **Ambiguous** | Ask |
| Different problem — they disagree about what this is *for* | **Ambiguous, seriously** | Ask |
| Different assumption on something material | **Ambiguous** | Ask |
| Different technical approach | Fine — that's the design's job, not this step's | Proceed |

**A material divergence is not a failure to resolve internally.** Do not average
the two readings, pick the more likely one, or ask a third agent to break the
tie. Two careful readers disagreeing *is the finding*: the request didn't contain
the answer, so it has to come from the approver.

### 5. Ask, if you must — one question, and make it a choice

State the two readings and ask which. Never an open question.

> ENG-004 — one thing before I spec this.
> **You said:** "make the bill split automatic"
> **Reading A:** it runs monthly and files the split for me to send
> **Reading B:** it runs monthly and sends it, end to end
> Which?

That's answerable in three seconds from a phone. "Can you clarify the scope of
the bill split feature?" is not — it hands the work back.

Hold the ticket at `intake` until answered. **Ask once.** A second question on the
same request means the first one was badly chosen; write that in the notebook.

### 6. Requirements

Now — and only now — write what must be true when this is done. Each requirement
traceable to something in the input or to a confirmed inference. If you cannot
point at where a requirement came from, it's scope you invented: cut it, or name
it as a proposal in the PRD.

Mark every one:
- **Stated** — the approver said it
- **Inferred** — both readings agreed on it without it being said
- **Confirmed** — the approver answered a question about it
- **Proposed** — the department thinks it should be there; the approver hasn't
  weighed in

### 7. The brief

The thing the department actually builds from: the requirements plus the
constraints, in the shape a builder can work from. This is what the approver
is really approving at G1 — not a vibe, an executable statement of intent.

### 8. Readback — put it at the TOP of the G1 item

Above the recommendation, in this order:

```markdown
## Readback

**You said:** "{verbatim}"

**Understood as:** {one paragraph}

**Requirements:**
1. {stated} …
2. {inferred} …
3. {proposed} …

**Assumed, and worth correcting if wrong:**
- {each inference that would change the build if it's wrong}

**Not doing:** {non-goals}
```

The point of putting it first: **the approver confirms meaning and scope in
the same tap.** If the readback is wrong they stop at the first paragraph, and
the whole department is saved from building the wrong thing correctly. No
extra gate, no extra step — the same G1 item, restructured to catch the more
expensive error first.

---

## When this does NOT run

- **Fast lane** (XS bug or chore). "Fix the typo on the pricing page" is not
  ambiguous, and a readback would be ceremony.
- **Agent-originated work** — a QA bug, a security finding, a devops incident.
  These come with reproduction steps and evidence, not intent to interpret.
- **A request that is already a spec.** If the approver wrote acceptance
  criteria themself, read them back in one line and move on.

Running this on everything would make it noise, and noise gets skimmed — which
is exactly how a readback stops working.

---

## Outputs

| File | Purpose |
|---|---|
| ticket — `## Input` | The verbatim request, never edited |
| ticket — `## Readback` | Both interpretations, divergences, resolution |
| `agents/product-manager/specs/{ENG-NNN}-{slug}.md` | Requirements with provenance tags |
| `inbox/` G1 item | Readback first, then the recommendation |
| `agents/product-manager/notebook/` | Every divergence found, and whether it mattered |

---

## Trace

`traces/product-manager-{run-id}.json` — ticket, divergences found by class,
question asked or not, requirements by provenance tag.

---

## The measure

**Divergences caught here versus wrong things discovered at acceptance.** Log
both. If the department is regularly failing acceptance verification on
"that's not what I meant", this step isn't working and the fix is here — not in
more testing downstream.

A divergence rate near zero is also a signal, and not a good one: it usually
means the second reading isn't genuinely blind.

---

## Failure modes to avoid

- **Resolving a divergence internally.** The disagreement is the finding.
- **Showing interpretation A to the second reader.** It anchors, agrees, and
  produces false confidence.
- **An open clarifying question.** Always a choice between two readings.
- **More than one question per request.** Bundle or choose better.
- **A readback that's a summary.** "Build the bill split feature" reads back
  nothing. It must contain the inferences, because that's where being wrong
  hides.
- **Running it on a typo fix.** Ceremony teaches people to skim.
