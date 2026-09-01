# Exemplars — TEMPLATE

**This is a template. Fill it in as the corpus grows, and expect it to be empty
on day one — that is the designed starting state, not a failure.** The live copy
lives at `$MKT_INSTANCE/agents/cmo/config/exemplars.md`.

## What this file is for

`voice/samples/{register}.md` is the corpus — everything the business has
published in that register. This file is the **shortlist**: for each archetype,
the two or three samples that best show what *good* looks like for that shape.
The content writer reads it to pull the right samples for a brief, rather than
reading the whole corpus and averaging it.

The distinction matters. A corpus teaches rhythm and fingerprint. An exemplar
teaches structure — where the hook turns, how long the setup runs, where the
point lands. Averaging thirty samples of five different shapes produces
something that is faithfully in the business's voice and structurally shapeless.

## How an entry gets here

A piece becomes an exemplar when it **shipped** and the approver rated it as one
of the good ones. Nothing enters this file on an agent's judgment, and nothing
enters before it has been published — an exemplar is a piece that survived M2
and met a real audience.

Reference a sample by its slug in the register file. Do not paste content in
here: a second copy drifts, and then two files disagree about what the good
version says.

## Below the floor

Until a register has **ten samples** (`config/conventions.yaml` → `voice.floor`),
this file will be thin or empty and the content writer falls back to the voice
guide's fingerprint alone. Drafting still runs — it just leans harder on the
review pass and on M2. That is the deliberate trade; do not fill this file with
material the business did not publish to make the number look better. A borrowed
exemplar teaches the wrong shape with full confidence.

---

## {archetype}

> _Repeat this block per archetype the business actually uses. The archetype
> names come from the channel playbook — a long-form channel typically runs
> something like `data-insight`, `case-study`, `pov`, `frame-shift`,
> `teardown`; a short-form channel may only have `tweet` and `thread`. Do not
> keep an archetype section for a shape the business never publishes._

**What it is for:** _one line_

**Exemplar samples** (`voice/samples/{register}.md`):
- _slug — one line on why this one_
- _slug —_

**Structural notes:** _What the shape actually is, in three or four lines.
Where the hook turns, what the middle carries, where the point lands. Write
these from the exemplars, not from theory — the notes are a description of what
worked here, not a recipe from a marketing book._

---

## Worked example — the shape of a filled entry

> Illustration only. Delete it, or replace it with a real archetype. It is here
> so the format is unambiguous, and it deliberately uses a business that is not
> yours.

### case-study

**What it is for:** what we built or shipped for a client, and what actually
happened — including the part that broke.

**Exemplar samples** (`voice/samples/long-form.md`):
- `2026-04-11-warehouse-routing` — opens on the decision, not the architecture
- `2026-06-02-invoice-triage` — the failure is in the middle, not hidden

**Structural notes:**
- Open with the **product decision**, never the stack. The stack is evidence.
- One thing broke or surprised, stated plainly. A case study with no friction
  in it reads as marketing and gets discounted accordingly.
- The measured outcome is a sentence, not a table.
- The lesson is the **last** line, not the first — putting it up top turns the
  piece into an argument with an anecdote attached.
