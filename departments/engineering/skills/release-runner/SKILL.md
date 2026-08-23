# Skill: release-runner

**Owner:** devops
**Model:** sonnet (checks are mechanical; the go/no-go is judgment)
**Trigger:** a ticket enters state `ready-to-ship`
**Suppressed when:** sabbath, retreat, or `ENG_RELEASE_FREEZE` — P0 hotfixes exempt

---

## Purpose

Hold the readiness gate, deploy at the project's autonomy level, verify it
worked, and write the record.

---

## Inputs

- `agents/eng-manager/board/{ENG-NNN}-{slug}.md` — all gate verdicts (required)
- `agents/eng-manager/config/projects.md` — autonomy level and deploy target
- `agents/database/migrations/{ENG-NNN}-{slug}.md` — when the change touches data
- `.env` → `MODE` — window check
- `agents/eng-manager/config/templates/release-record.md`

---

## Steps

### 1. Window check

Read `.env` → `MODE` and the clock. Refuse the release when:

- `sabbath` or `retreat` is active, or `ENG_RELEASE_FREEZE` is set
- It's Friday after 15:00 local
- It's a weekend

Set the ticket to `blocked` with the window as the reason and the date it opens.
**A feature is never worth a Sunday.** P0 hotfixes are the only exception, and
they still pass the security gate.

### 2. Verify every upstream gate passed

Code review, migration (if applicable), quality, security. A missing verdict is a
fail, not an assumption — return the ticket to the gate that never ran.

### 3. Hold the readiness gate

Fail on any of:

- **No tested rollback.** Theorised is not tested — someone has to have run it.
- **No observability on the new path.** If a failure here would only be
  discovered by a user complaining, this isn't ready.
- **Unbudgeted recurring cost.** Anything above $0/month is written as a cost
  notice to `reports/costs/{YYYY-MM-DD}-{project}-{ENG-NNN}.md` *before* the
  release — project, ticket, monthly delta, driver, first billing date. One
  line per notice surfaces in the weekly report, which is where the approver
  reads it. Terminal for now: it rewires to a finance department's intake if
  business-os grows one that consumes cost data. The approver learning about
  new spend from a bill is a system failure, and this notice is the mechanism
  that prevents it.
- **Window closed** (step 1).

### 4. Route by autonomy level

| Level | Action |
|---|---|
| **L0** | Unreachable — an L0 ticket terminates at `advised` and never gets here. If one does, that's a pipeline bug: stop and flag it. |
| **L1** | Open a PR **and write a merge request to `inbox/`** in the same step. |
| **L2** | Merge after gates, then raise **G3** to the approver through the EM. Deploy on approval. |
| **L3** | Deploy, then notify the approver. G3 is automatic. |

Never deploy above the registered level. Raising a level is the approver's
call alone.

**The L1 merge request is not optional.** Set the ticket to `blocked` with
`blocked_on: approver`, and write an inbox item carrying the PR link, what it
does in one line, and the gates it passed. The ticket keeps its WIP slot and
counts against the approval cap while it waits.

Before this (fixed 2026-07-27) an L1 release just set `blocked` and stopped: the
ticket left the WIP bucket, counted against nothing, freed a slot for a new
ticket, and sat invisible for five working days — building the exact pile of
finished-but-unapproved work the caps exist to prevent. New projects register at
L1 by default, so on most instances this is the common path, not an edge case.

The build loop detects the merge itself on each pass, by local git ancestry
(`git merge-base --is-ancestor {branch} origin/{default}`) — no API call, no
polling cost. Merged → the ticket advances to `shipped` and you write the
release record then.

### 4b. Work in the department's own worktree

Never run git operations in a human's own checkout of `{project}` — that's
their interactive working directory. The department's copy is
`$PROJECTS_DIR/_eng/{project}/`. If it has uncommitted changes at the start of
a pass, a previous pass died mid-work: stop and flag it. Never discard, never
stash blindly. The instance's own operating repo is the exception — agents
already run in it by design. See `agents/eng-manager/config/projects.md`.

### 5. Deploy

Run the project's own deploy path — don't invent one. Where the ticket carries a
migration, run it per `database`'s plan, in the sequence the plan specifies, and
stop at the first unexpected result rather than pushing through.

For an internal-automation project, "deploy" means merged to `main` **and** the
routine actually installed. A cron that never fires is a failed deploy.

### 6. Verify

- Health checks green
- Error rate and latency versus the hour before
- For a scheduled job: **watch the first fire.** Not the next pass — this one.
- For a model-backed path: latency, failure rate, malformed-output rate

Degraded? Roll back first, diagnose after. That decision is already made and
rehearsed; don't re-litigate it live.

### 7. Write the release record

`agents/devops/releases/{YYYY-MM-DD}-{project}-{ENG-NNN}.md`, **from what
actually happened** — not copied from the plan. A record that matches the plan
exactly every time isn't being written honestly.

No release record, no `shipped` state.

### 8. Route on

State `shipped`, owner `product-manager` for acceptance verification. Append one
line to the ticket log.

---

## Outputs

| File | Purpose |
|---|---|
| `agents/devops/releases/{YYYY-MM-DD}-{project}-{ENG-NNN}.md` | The record |
| ticket log | One line: released, or blocked with the reason |
| `agents/devops/notebook/{date}-deploy-log.md` | What shipped, duration, surprises |
| `inbox/` (via eng-manager) | G3 item for L2; cost notice for CFO if above $0 |

---

## Trace

`traces/devops-{run-id}.json` — ticket, project, autonomy, gates verified,
deploy duration, health result, rollback used or not, cost delta.

---

## Failure modes to avoid

- **Releasing without a tested rollback.**
- **Releasing outside the window.** The board can wait until Monday.
- **Deploying above the autonomy level.**
- **Skipping first-fire verification** on a scheduled job — the most common
  silent failure in an internal-automation project.
- **Writing the record from the plan** instead of from reality.
- **Diagnosing before stabilising** when something looks wrong.
