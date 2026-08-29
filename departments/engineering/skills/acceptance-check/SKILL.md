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

- **All criteria pass** → state `verified`, owner `eng-manager`. Done — but see
  step 6b before you exit the pass.
- **Any criterion fails** → state `building`, owner the implementing engineer,
  **with the specific criterion named** in the ticket log. Not "doesn't work" —
  "criterion 3 fails: given an empty cart, the total renders as NaN."

A failed acceptance check on something already in production also gets a bug
filed through `qa`, at the severity its impact warrants.

### 6b. Continue an approved sequence

This only runs off the `verified` branch. Look at the ticket's own PRD for a
proposed multi-ticket sequence — usually a section titled something like
"Feature shape and sequencing," written because the original ask didn't fit
in one ticket (`ENG-006` set the precedent: five items, and this was item
one).

File the next item now, in this same pass, only if **both** of these hold:

1. The PRD names a next item and gives it enough shape to draft from — a
   single line is enough, since the new PRD will do the actual work.
2. The **G1 answer on this ticket** explicitly signed off on the whole
   sequence, not just the ticket that was in front of the approver.
   `ENG-006`'s recorded answer is the bar to clear: *"the proposed five-ticket
   sequence stands as shape to file incrementally, not as four pre-approved
   tickets"* — nothing left to guess about continuing. A plain "approved"
   that never touches the sequence does **not** clear this bar; handle it
   like any other partial G1 (`docs/engineering-team.md` already has a
   precedent for this in the decision journal, from `ENG-005`'s two-part G1)
   — ask a targeted follow-up question rather than assume the rest was
   approved by implication.

When both hold and the board doesn't already have a ticket for that next
item, shape it the same way a brand-new intake would: new ticket, problem
statement, PRD, acceptance criteria, non-goals, a recommendation — the
complete `skills/prd-writer/SKILL.md` process, with no shortcut just because
the shape already existed on paper — then raise its own G1 to `inbox/` like
any other ticket. WIP and approval caps apply exactly as `eng_build_loop.md`
specifies; if a cap is in the way, say so in the ticket log and leave it for
the next pass rather than working around the cap.

None of this is the department commissioning itself
(`docs/engineering-team.md`, "The department cannot commission itself") — the
approver already reviewed and approved this shape at the sequence's first
G1. Only the drafting and filing becomes automatic; everything else stays
exactly as gated as before, with its own full G1, design, and
review/QA/security passes for every item. A rejected or held G1 stops the
chain on the spot — no retrying, no jumping to the next item anyway.

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
