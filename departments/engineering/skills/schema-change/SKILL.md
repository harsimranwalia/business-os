# Skill: schema-change

**Owner:** database
**Model:** opus (migrations are the one thing a redeploy can't undo)
**Trigger:** a design with `touches_data: true`; then again at the migration gate
**Suppressed when:** sabbath, retreat; no production migrations while `ENG_RELEASE_FREEZE` is set

---

## Purpose

Design the schema, write the migration and its tested rollback, and hold the
migration gate. Application bugs are fixed with a deploy; data bugs are fixed
with a restore. This skill is slow on purpose.

---

## Inputs

- `agents/architect/designs/{ENG-NNN}-{slug}.md` — intent and constraints (required)
- The project's existing schema and migration history
- `agents/eng-manager/config/templates/*` and the project's own migration dir
  (for example, `supabase/migrations/`)
- `agents/database/notebook/` — what has gone wrong before on this project
- `.env` → `MODE`

---

## Steps

### 1. Mode check

`sabbath` or `retreat`: exit. `ENG_RELEASE_FREEZE`: design and plan only, no
production migration.

### 2. Get the numbers — before designing anything

- Current row count on every affected table
- Growth per month
- Query frequency and read/write ratio
- Cardinality of any column being indexed

If the design doesn't carry them, ask through the EM. **A schema designed
without numbers is a guess**, and saying so is better than guessing politely.

### 3. Design for the query, not the diagram

Normalise until it hurts; denormalise where it's measured. Know which one you're
doing and write the reason in the plan.

Constraints go in the database, not only the application: `NOT NULL`, foreign
keys, unique constraints, checks. The application is one client of this data and
it will not be the last.

### 4. Plan the expand/contract sequence

Schema and code deploy separately, so they must overlap:

`add new` → `backfill` → `dual-write` → `switch reads` → `drop old`

As separate migrations, often separate tickets. **A rename in one step is an
outage.** Write the sequence explicitly, and state which steps are in this
ticket and which are follow-ups.

### 5. Index deliberately

An index for every new access pattern on a table over ~10k rows. No index
"just in case" — each one costs write throughput. Remove indexes nothing
queries. Read the query plan; don't assume the planner agrees with you.

### 6. Estimate runtime and locks

Against realistic volume, not an empty table. Write both into the plan. Anything
that locks a hot table for a noticeable window needs an online strategy or a
scheduled window — and `devops` needs to know before the release.

### 7. Plan the backfill

Batched, resumable, with a runtime estimate. An unbatched backfill over a large
table in production is a self-inflicted outage.

### 8. Write the rollback, then run it

In that order, before the forward migration ships. Test both directions against
synthetic data at realistic volume. **Test data is synthetic — never a
production dump.**

If the change is genuinely irreversible (a drop, a destructive transform), it
needs an approved ADR and a verified backup taken immediately before.

### 9. Write the plan and the migration

Plan → `agents/database/migrations/{ENG-NNN}-{slug}.md`: schema change, indexes,
expand/contract sequence, runtime estimate, lock profile, backfill batching,
rollback, and the numbers from step 2.

Migration file → the project's own migration directory, following its
conventions exactly.

### 10. Hold the gate

Before release, verify and fail on any of:

- Destructive change with no verified backup
- Irreversible change with no approved ADR
- Missing or untested rollback
- New query pattern with no index on a table over 10k rows
- Blocking lock on a hot table with no online strategy
- Backfill with no runtime estimate or no batching
- Schema and code that cannot coexist across the deploy

**pass** → continue the pipeline. **fail** → state `building`, owner `database`,
with the specific failure named.

---

## Outputs

| File | Purpose |
|---|---|
| `agents/database/migrations/{ENG-NNN}-{slug}.md` | The plan, the numbers, the rollback |
| The project's migration directory | The migration itself |
| ticket log | One line: gate verdict |

---

## Trace

`traces/database-{run-id}.json` — ticket, tables touched, estimated runtime,
rollback tested, gate verdict.

---

## Failure modes to avoid

- **Designing without the numbers.**
- **A rename in one step.**
- **An untested rollback.** Asserted is not tested.
- **A production dump as test data.**
- **Being hurried.** The gate is the gate, and a slipped release is cheaper than
  a restore.
