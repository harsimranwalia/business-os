# Skill: acceptance-check

**Owner:** product-manager
**Model:** sonnet
**Trigger:** a ticket enters state `shipped`
**Suppressed when:** sabbath, retreat

---

## Purpose

Confirm the shipped thing does what the PRD promised. This is the step that
makes "done" mean something — without it, "merged" quietly becomes the finish
line.

---

## Inputs

- `agents/product-manager/specs/{ENG-NNN}-{slug}.md` — the acceptance criteria (required)
- `agents/devops/releases/{YYYY-MM-DD}-{project}-{ENG-NNN}.md` — what shipped, where
- `agents/eng-manager/board/{ENG-NNN}-{slug}.md`
- The running result itself

---

## Steps

### 1. Mode check

`sabbath` or `retreat`: exit.

### 2. Check against the live result — not the proxies

Each criterion is verified against the thing that actually shipped. **Not**
against the test suite, **not** against the PR description, **not** against the
engineer's summary. Those are all upstream evidence that the code does what
someone intended; this step asks whether what shipped does what was promised.

For an internal-automation project, that means running the routine or reading
the artifact it produced. For a deployed app, that means using the path a user
would.

### 3. Walk every criterion

One at a time, in order. For each: pass or fail, with the observation that
justifies it. "Looks fine" is not an observation.

### 4. Check the non-goals

Did anything from the non-goals list get built anyway? That's scope creep that
survived the pipeline, and it's worth a line in the notebook — it means the gates
let something through that they should have caught.

### 5. Check the cost

Did the release add recurring cost? Does it match what the PRD estimated? A
material gap goes to the CFO through the EM, and into the notebook so the next
estimate is better.

### 6. Route

- **All criteria pass** → state `verified`, owner `eng-manager`. Done.
- **Any criterion fails** → state `building`, owner the implementing engineer,
  **with the specific criterion named** in the ticket log. Not "doesn't work" —
  "criterion 3 fails: given an empty cart, the total renders as NaN."

A failed acceptance check on something already in production also gets a bug
filed through `qa`, at the severity its impact warrants.

### 7. Note what the estimate missed

Into `agents/product-manager/notebook/`: was the impact what you predicted?
Would you write these criteria differently now? This is how the next PRD gets
sharper.

---

## Outputs

| File | Purpose |
|---|---|
| ticket log | One line per criterion: pass/fail with the observation |
| `agents/product-manager/notebook/{date}-acceptance.md` | What the estimate missed |
| `agents/qa/bugs/` (via bug-triage) | When a criterion fails in production |

---

## Trace

`traces/product-manager-{run-id}.json` — ticket, criteria passed/failed, scope
creep found, cost variance.

---

## Failure modes to avoid

- **Verifying against the test suite.** The suite proves the code does what the
  engineer meant. This step asks something different.
- **Passing a criterion you couldn't actually check.** Say it's unverifiable and
  send it back — that's a defect in the criterion, and worth fixing at the source.
- **Vague failure reports.** Name the criterion and the observation.
- **Letting scope creep pass silently** because the extra thing is nice.
