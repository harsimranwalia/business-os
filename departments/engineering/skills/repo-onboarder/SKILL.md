# Skill: repo-onboarder

**Owner:** eng-manager
**Model:** sonnet
**Trigger:** the approver names a repo the team should be able to work on. Never scheduled.
**Suppressed when:** sabbath, retreat

---

## Purpose

Scan an unregistered repo, produce its project card, and propose an autonomy
level with evidence. Nothing in the department may touch a repo before its card
is approved.

---

## Inputs

- The repo path or URL the approver named (required)
- `agents/eng-manager/config/projects.md` — the registry and its format
- Read access to the repo

---

## Steps

### 1. Mode check

`sabbath` or `retreat`: exit.

### 2. Confirm the boundary before reading

Is this the business's own repo, a partner's, or a client's? A client repo
starts at L0 and the recommendation says so plainly. If the repo's ownership isn't clear from
context, ask through one question — this determines everything downstream.

### 3. Scan the stack

- Languages, frameworks, major libraries, versions
- Package manager and lockfile
- Runtime versions expected
- Monorepo or single package; if monorepo, the packages that matter

### 4. Find the commands

The four that matter, taken from the repo's own scripts and CI, never guessed:

| Command | Where to look |
|---|---|
| Test | `package.json` scripts, `Makefile`, `pyproject.toml`, CI workflow |
| Lint | same |
| Typecheck | same |
| Build | same |

A repo with no test command is a finding, not a blocker — record it, because it
changes what the quality gate can enforce and it's usually the first ticket the
team should file.

### 5. Read the conventions

- Its own `CLAUDE.md` / `AGENTS.md` / `CONTRIBUTING.md` — **these override the
  department's standards inside that repo**
- Style config: formatter, linter rules, editor config
- Branch and commit conventions, from the git log rather than from a document
- PR process: required reviewers, templates, protected branches

### 6. Assess the security posture

- Secret management: env files, a manager, or (badly) committed
- Dependency freshness and any obvious CVE exposure
- Auth model, if the app has one
- Whether CI runs anything security-relevant

Findings here are notes, not a review — the security gate applies to changes,
not to a codebase you've just met.

### 7. Identify the deploy path

Where does this actually go to production, who triggers it, and what does
rollback look like? If nobody knows, that's the single most important thing in
the card.

### 8. Draft the project card

In the exact format of the `projects.md` table, plus a per-project rules
subsection covering: who else reviews, what's high blast radius, and any hard
constraint (cost ceiling, client boundary, vendored code).

### 9. Propose an autonomy level — L1 by default

**Never higher on first registration**, regardless of how well the team knows
the stack. Recommend L0 for any client-governed repo. Say what would have to be
true for a raise: three clean trips through the full pipeline.

### 10. Route to the approver

The card goes to `inbox/` through the EM, as one decision: register this
repo at this level, yes or no. On approval, append it to `projects.md`.

**Until then, nothing in the department touches the repo** beyond this read-only
scan.

---

## Outputs

| File | Purpose |
|---|---|
| `inbox/{date}-project-card-{slug}.md` | The card and the level, for the approver |
| `agents/eng-manager/config/projects.md` | Appended on approval only |

---

## Trace

`traces/eng-manager-{run-id}.json` — repo, stack, commands found, gaps,
proposed level.

---

## Failure modes to avoid

- **Guessing the commands.** Read them from the repo's own scripts and CI.
- **Proposing above L1** on a first registration.
- **Missing the repo's own conventions file.** It outranks the department's
  standards inside that repo.
- **Running anything against a client system** during the scan. Read the code
  and nothing else.
- **Registering before approval.**
