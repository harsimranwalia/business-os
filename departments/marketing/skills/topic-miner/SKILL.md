# Skill: topic-miner

**Owner:** cmo — `conventions.yaml` makes the CMO the drainer of `inbox/requests/` at planning
**Model:** `reasoning` tier (scoring and judgment over source material; not generation)
**Trigger:** the first step of the weekly planning run, before any piece is briefed
**Suppressed when:** `MODE` is `sabbath`, `retreat`, or `quiet`

---

## Purpose

Keep `content/topic-bank.md` stocked with real, specific, non-recycled material,
and make sure every topic a human files actually goes somewhere.

Two jobs, and the second is the one that quietly matters. **Harvesting** finds
post-worthy material in what the business has genuinely done and scores it.
**Draining** empties `inbox/requests/` so a person who files a topic gets an
answer — banked or declined, with a reason — rather than filing into a void.

The bank exists to stop the planner recycling the same three stories. Without
it, a weekly cadence converges on whatever was easiest to reach for in week
two, and the audience notices before the department does.

---

## Paths

Bare paths are **instance-relative** (`$MKT_INSTANCE`); `$MKT_DEPT` prefixes are
template-side and read-only.

---

## Inputs

- `content/topic-bank.md` — the bank itself; read before writing, always
- `inbox/requests/` — topics filed by a filer, in whatever shape they arrived
- `proof/case-studies/` — client work with a measured outcome
- `proof/internal/` — real work, no client; still proof of capability
- `../engineering/reports/proof/` — written by the engineering department,
  **read-only here.** Engineering owns what it built; marketing owns what it
  says about it.
- `../knowledge/business-profile.md` — what the business is, who it serves.
  Read fresh; "would this reach the buyer?" is unanswerable without it.
- `agents/cmo/config/positioning-statement.md` — the ICP, for the relevance score
- `content/series/` — running series and their unfilled slots
- `content/shipped/` — the **last 8 pieces**, for their `source_refs`
- `performance/` — which archetypes have actually been landing
- `$MKT_DEPT/skills/content-writer/SKILL.md` § Archetypes — the authoritative
  archetype list and each one's succeeds-when criteria. Score against that
  file, never against a remembered version of it.

---

## Steps

### 1. Mode
`.env` → `MODE`. `sabbath` / `retreat` / `quiet` → exit without writing.
Stop code `mode_halt`.

### 2. Build the exclusion list

Read the last 8 pieces in `content/shipped/` and collect every `source_refs`
entry. Material used in the last 8 pieces is excluded from primary candidates.

Also read `proof/*/` entries' `used_in` fields. A proof entry reused silently
across three pieces reads as one story told three times, and that is exactly
what this field exists to prevent.

Exclusion is not deletion: an excluded entry stays in the bank at
`state: used`, with the piece that used it recorded. The planner can still
deliberately return to it; what it can't do is stumble back onto it.

### 3. Drain `inbox/requests/` — every request gets an answer

For each file in `inbox/requests/`, in filing order:

1. Read it as it is. A filer writes prose, not frontmatter. If there is no
   frontmatter, add one — don't reject a request for arriving in the wrong
   shape. That would train people to stop filing.
2. Decide: **bank it** or **decline it**. Decline only for a real reason —
   it's already in the bank (point at the entry), it names something
   confidential (`naming_rules.never_name`), it has no substance to build a
   piece on, or it is a request for a *piece* rather than a *topic* and belongs
   in the plan instead.
3. **Banked:** create the bank entry with `source: filer`, `filed_by`, and
   `request_file` pointing back at the original. Stamp the request file
   `state: banked` and `topic_id: TB-NNNN`.
4. **Declined:** stamp the request file `state: declined` and `reason: {one
   line}`, and **tell the filer** — `lib/mkt-notify.sh raise {request_file}`.
   A silent decline is the failure this step exists to prevent; the second
   time someone's filed topic disappears without a word, they stop filing.
5. **Never delete a request file.** It stays as the audit trail of what was
   asked and what happened to it.

A filer has no gate authority. A banked request is a candidate like any other
and competes on its scores — filing a topic is not approving it.

### 4. Harvest candidates

Walk `proof/case-studies/`, `proof/internal/`,
`../engineering/reports/proof/`, and any decisions the instance records, plus
unfilled slots in `content/series/`.

For each piece of material, produce a candidate with:

- **Which archetypes it fits** — one entry may fit two; say which and why.
- **A one-line note on what the piece would actually say.** Not a topic label:
  "we rebuilt the intake form" is not a candidate, "the intake form's 40%
  drop-off was three required fields nobody needed" is.
- **Its refs**, so the writer can be handed the raw material rather than a
  summary of it. Summarising here sands off the specific detail that makes a
  piece worth reading.

**For `data-insight`**, the candidate is the business's own experience or angle
that an external published number could confirm or extend — the external stat
itself is sourced at drafting time. Surface material with a concrete,
specific experience a number could sit against.

**A candidate needs something real underneath it.** Material with no outcome,
no number and no specific incident is not a candidate; it is a subject. Do not
bank subjects to hit a count.

### 5. Score every candidate — four dimensions, 1–5

| Dimension | Question |
|---|---|
| `fit` | How cleanly does it fit its best archetype's structure and succeeds-when line? |
| `specificity` | How non-generic is it? Could a competitor have written the same thing? 5 means only this business could. |
| `freshness` | How recent is the underlying work? |
| `icp` | Would this plausibly reach the buyer described in the positioning and the business profile? |

**Recompute `freshness` from the source's own date on every run — never carry
the previous run's number forward.** That is what makes the bank age honestly
instead of preserving a candidate that scored 5 for recency four months ago.

`performance/` informs `fit` only where there is real history: if an archetype
has been landing and another has not, that is a weight on the score, not a ban
on the archetype. Under 5 pieces of history, ignore performance entirely and
say so in the run note rather than scoring off two rows.

### 6. Merge into `content/topic-bank.md`

**Read the bank first, then merge — never overwrite it.**

- Match a new candidate against existing entries **by source ref**. A match
  updates the existing entry (scores, note) and keeps its id. It does not
  create a second entry.
- New candidates take the next id from the header's `next_id` and increment it.
- Entries whose refs appear in the exclusion list move to `state: used` with
  `used_in` set to the shipped piece.
- Entries that have been `open` for more than 12 weeks and have never been
  planned move to `state: retired` with a one-line reason. A bank that only
  grows is a bank nobody reads.

**Bank format** — one header block, then one section per entry:

```markdown
# Topic bank

next_id: TB-0043
updated: 2026-08-29

---

## TB-0042 — three required fields were 40% of the drop-off

- state: open              # open | planned | used | retired | declined
- source: harvest          # harvest | filer | series
- archetypes: [case-study, teardown]
- source_refs:
    - proof/internal/intake-form-rebuild.md
- scores: { fit: 4, specificity: 5, freshness: 4, icp: 4 }
- first_seen: 2026-08-29
- last_scored: 2026-08-29
- note: >
    The 40% drop-off wasn't the form's length, it was three required fields
    that existed because a report needed them once. Has the before/after number.
# filer entries additionally carry:
#   filed_by: {name}
#   request_file: inbox/requests/2026-08-20-intake-form.md
# used entries additionally carry:
#   used_in: content/shipped/2026-09-03-case-study-intake-form.md
```

`state: planned` is written by the planner when it briefs a piece, not by this
skill. This skill only ever moves an entry to `used` or `retired`.

### 7. Write the run note

`agents/cmo/notebook/{YYYY-MM-DD}-topic-mining.md` — a short record, not a copy
of the bank: how many candidates were harvested, how many requests were drained
and their outcomes, what was excluded, and any escalation from step 8. The bank
is the durable artifact; this is the run's receipt.

### 8. Escalate starvation honestly

Two conditions, both reported rather than papered over:

- **`insufficient_fresh_material`** — fewer than 2 candidates score ≥ 3 in
  *every* dimension for a given archetype. Return
  `{ archetype, candidates: [], note: 'insufficient fresh material' }` for it.
  The planner substitutes a different archetype or defers the slot. It does
  **not** lower the bar to fill the slot.
- **`heavy_recycling_risk`** — the exclusion list covers more than 80% of
  candidates. Flag it in the run note, in the return, and via
  `lib/mkt-notify.sh raise`, **once**. Say what the actual fix is: the business
  needs more recorded proof, which means doing work and writing it down, not
  mining harder. A department that responds to a thin bank by lowering its
  scoring standard produces a slow decline nobody can point at a date for.

### 9. Return to the caller

The ranked candidate list, grouped by archetype, **top 3 per archetype**, each
with its id, note, refs and scores — plus any escalation from step 8. The
planner reads this to choose source material for the week's briefs.

---

## Outputs

| Artifact | Purpose |
|---|---|
| `content/topic-bank.md` | The durable queue the planner works from. Merged, never overwritten. |
| `inbox/requests/*.md` | Stamped `state: banked` or `state: declined` with a reason. Never deleted. |
| `agents/cmo/notebook/{YYYY-MM-DD}-topic-mining.md` | The run receipt |
| `traces/topic-miner-{run-id}.json` | Candidates harvested, requests drained by outcome, escalations |
| Structured return | Top 3 candidates per archetype, plus escalations |

---

## Stop codes

| Code | When | What the caller does |
|---|---|---|
| `mode_halt` | `MODE` is sabbath/retreat/quiet | Exit silently, nothing written. |
| `no_proof_sources` | Every proof directory is missing or empty **and** `inbox/requests/` is empty | Nothing to mine. Return an empty bank update and say so plainly — do not invent candidates from the business profile. Notify once: the fix is recording real work, not writing better prompts. |
| `bank_unreadable` | `content/topic-bank.md` exists but won't parse | **Do not overwrite it.** Stop, notify, and let a human look. A bank rebuilt from scratch loses every `used_in` and every decline reason. |
| `insufficient_fresh_material` | Per-archetype, fewer than 2 candidates score ≥3 everywhere | Substitute an archetype or defer the slot. Never lower the bar. |
| `heavy_recycling_risk` | Exclusions cover >80% of candidates | One notification, one line in the run note. Upstream fix. |

---

## Failure modes to avoid

- **Overwriting the bank.** Read, merge, write. `used_in` and decline reasons
  are the only memory this skill has.
- **Silently declining a filed request.** Every request ends stamped, and a
  decline is told to the person who filed it.
- **Banking subjects instead of candidates.** "We should post about our
  onboarding" is not material. If there is no outcome, number or incident
  underneath it, it is not a candidate.
- **Carrying freshness forward.** Recompute it, or the bank preserves stale
  material at fresh scores.
- **Summarising the source material into the bank.** The bank holds the ref and
  a one-line note; the writer gets the raw file. A pre-digested topic drafts
  into a generic piece.
- **Lowering the score threshold to fill a week.** An empty archetype slot is
  information. A padded one is a bad piece with a plan behind it.
- **Writing to `proof/` or to engineering's `reports/proof/`.** Both are read
  here, never written. `used_in` is recorded on a proof entry at ship time, by
  the ship path — this skill only reads it. Marketing says what the work means;
  it does not author the evidence.
