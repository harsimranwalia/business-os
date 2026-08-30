#!/bin/sh
# install.sh — instantiate the engineering department for one business.
#
#   ./install.sh <business> [--approver NAME] [--apply]
#
# Dry-run by default: prints every path it would create and writes nothing.
# Pass --apply to actually create the instance.
#
# What this produces is a life-os-shaped root. That is deliberate, not
# incidental: lib/eng-gate-check.sh hardcodes its receipt paths and per ADR-002
# the scripts are the only enforceable surface the department has. An instance
# that matches those paths runs the enforcement unmodified.
set -eu

DEPT="$(CDPATH= cd -P -- "$(dirname -- "$0")" && pwd -P)"
BUSINESS_OS="$(CDPATH= cd -P -- "$DEPT/../.." && pwd -P)"
VERSION="$(cat "$DEPT/VERSION")"

BUSINESS=""; PRINCIPAL="approver"; APPLY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --apply) APPLY=1 ;;
    --approver) shift; PRINCIPAL="${1:?--approver needs a name}" ;;
    -*) echo "unknown flag: $1" >&2; exit 2 ;;
    *) BUSINESS="$1" ;;
  esac
  shift
done
[ -n "$BUSINESS" ] || { echo "usage: ./install.sh <business> [--approver NAME] [--apply]" >&2; exit 2; }

INST="$BUSINESS_OS/instances/$BUSINESS/engineering"
KNOW="$BUSINESS_OS/instances/$BUSINESS/knowledge"
[ "$APPLY" -eq 1 ] || echo "DRY RUN — nothing will be written. Re-run with --apply."
echo "template : $DEPT (v$VERSION)"
echo "instance : $INST"
echo "approver: $PRINCIPAL"
echo

if [ -e "$INST" ] && [ "$APPLY" -eq 1 ]; then
  echo "REFUSING: $INST already exists. Delete it deliberately, or pick another name." >&2
  exit 1
fi

DIRS="inbox inbox/requests inbox/_handled traces
reports reports/costs reports/proof
agents/eng-manager/board agents/eng-manager/config agents/eng-manager/inbox agents/eng-manager/notebook
agents/product-manager/specs agents/product-manager/inbox agents/product-manager/notebook
agents/architect/designs agents/architect/decisions agents/architect/notebook
agents/principal-engineer/reviews agents/principal-engineer/notebook
agents/backend/notebook agents/frontend/notebook
agents/database/migrations agents/database/notebook
agents/qa/test-plans agents/qa/bugs agents/qa/notebook
agents/devops/releases agents/devops/incidents agents/devops/notebook
agents/security/reviews agents/security/notebook
config"

if [ "$APPLY" -eq 1 ]; then mkdir -p "$KNOW"; else echo "  mkdir ../knowledge"; fi

for d in $DIRS; do
  if [ "$APPLY" -eq 1 ]; then mkdir -p "$INST/$d"; touch "$INST/$d/.gitkeep"; else echo "  mkdir $d"; fi
done

emit() { # emit <relative-path> — content on stdin
  _p="$1"
  if [ "$APPLY" -eq 1 ]; then cat > "$INST/$_p"; else echo "  write $_p"; cat >/dev/null; fi
}

emit config/instantiated-from <<EOF
$VERSION
EOF

emit config/config.yaml <<EOF
# Instance overrides for $BUSINESS. The template supplies every default;
# this file only records what is true for this business.

business: $BUSINESS
instantiated_from: $VERSION

# The single human with gate authority. Owns G1 scope, G2 one-way-door and
# G3 release. The five machine gates stay machine-owned and blocking.
approver:
  name: $PRINCIPAL
  notify: telegram

# Humans who may file a request but hold no gate authority. Their requests land
# in inbox/requests/ with \`source: filer\` and are shaped by the PM like any
# other intake. A filer never receives a gate.
filers: []

# Pause switch for THIS business only. sabbath | retreat | quiet halt every pass
# for this instance; empty means normal operation. Falls back to MODE in
# business-os/.env when empty, so the global switch still stops everything at
# once — this only adds the ability to stop one business without stopping the
# rest.
mode:

# Delivery caps. Raising these is the approver's call.
wip:
  machine_limit: 1      # states ready..ready-to-ship — one ticket shipped
                        # before the next starts (the approver's correction,
                        # 2026-08-29; see departments/engineering/agents/eng-manager/config.yaml)
  approver_limit: 2    # items awaiting the approver at once
  approval_cap: 3       # gates queued across the whole board
EOF

# agents/eng-manager/config/, NOT config/. This emitted config/projects.md while
# every reader — lib/eng-gate-check.sh's PROJECTS, agents/eng-manager/config.yaml
# -> paths.projects, and the devops/architect/PM configs — looks for it under
# agents/eng-manager/config/, which is also what conventions.yaml declares. So
# every instance shipped with a project registry the gate check could not read:
# the autonomy level it enforces was unreadable, and nothing said so.
emit agents/eng-manager/config/projects.md <<'EOF'
# Project Registry

Every repo this instance's engineering team is allowed to touch, and how far it
may go. **If a repo is not in this table, the team does not touch it.** Adding
one is the approver's call — run `skills/repo-onboarder/SKILL.md`.

## Autonomy levels

| Level | Means |
|---|---|
| **L0** observe | Read and propose only. Never writes code, never opens a PR. |
| **L1** branch | Writes on a branch, opens a PR after all machine gates pass. A human merges. |
| **L2** merge | Merges to main once all machine gates pass. The approver approves releases (G3). |
| **L3** ship | Deploys to production after gates. The approver is notified after, not asked before. |

Autonomy belongs to the project, never the ticket. **New projects register at L1,
never higher.** Only the approver raises a level.

## Registered projects

| Project | Repo path | Stack | Deploy target | Autonomy | Notes |
|---|---|---|---|---|---|
| _(none yet — register with `repo-onboarder`)_ | | | | | |

## Commands

How each project is verified. `skills/test-suite-run/SKILL.md` reads this when a
test plan carries no `suite_command` of its own, and
`skills/repo-onboarder/SKILL.md` fills it in at registration from the repo's own
scripts and CI — `package.json`, `Makefile`, `pyproject.toml`, `deno.json`, the
workflow file. **Never guessed.**

An empty cell means the command does not exist. That is a finding, not a blank
to fill in with something plausible: it changes what the quality gate can
actually enforce, and a receipt written against a command that was invented
proves nothing.

| Project | Test | Lint | Typecheck | Build |
|---|---|---|---|---|
| _(none yet — `repo-onboarder` fills this in)_ | | | | |

## Working copies — the department never touches a human's directories

Every project gets a dedicated working copy the department owns, created as a
git worktree beside the repo:

```
<repo>/                 # a human's. Never touched by an agent.
_eng/<project>/         # the department's worktree.
```

- The build loop refuses to run against a path that isn't under `_eng/`.
- Before any work: `git fetch`, then create the branch in the worktree.
- Uncommitted changes in the worktree at the start of a pass means a previous
  pass died mid-work. Stop and flag it. Never discard, never stash blindly.
EOF

emit config/internal-projects <<'EOF'
# Projects allowed on the `internal` lane, one per line. Blank means none.
#
# The internal lane waives the QA and security receipts. That is only ever
# defensible for a project with no real deploy target — an internal automation
# repo, not anything a customer touches. Adding a line here is the approver's
# call and should be rare.
EOF

if [ "$APPLY" -eq 1 ]; then
  if [ -f "$KNOW/business-profile.md" ]; then
    echo "  ../knowledge/business-profile.md already exists — left alone"
  else
    cat > "$KNOW/business-profile.md" <<PROFILE
# Business Profile — $BUSINESS

**Fill this in before the first scope conversation.** The product manager and
architect read this file at the start of request shaping, G1 framing, PRD
writing and any architectural call. A PM that cannot say what the business does
cannot say whether a request is worth building, and will approve anything that
sounds reasonable.

**Business:** <what it is, what it sells, who it serves>

**Customers:** <who pays, and for what>

**What good looks like:** <the outcome the business is actually optimising for>

**Out of scope:** <what this business does not do — the boundary that lets the
PM say no to a request that sounds plausible>
PROFILE
    echo "  wrote ../knowledge/business-profile.md (stub — fill it in)"
  fi
else
  echo "  write ../knowledge/business-profile.md"
fi

emit agents/eng-manager/config/gate-waivers.md <<'EOF'
# Gate waivers

A waiver suspends one machine gate for one ticket, and says why and until when.
Only the approver grants one. `lib/eng-gate-check.sh` reads this file.

| Ticket | Gate | Reason | Granted by | Expires |
|---|---|---|---|---|
EOF

emit agents/eng-manager/config/exceptions.md <<'EOF'
# Process exceptions

Every time the department did not follow its own rule, and why. Three of the
same exception means the rule is wrong — fix the rule, stop granting the
exception.

| Date | Rule | Ticket | Why | Granted by |
|---|---|---|---|---|
EOF

emit agents/eng-manager/config/decision-journal.md <<'EOF'
# Decision journal

What the approver approved, changed, or killed at a gate — and the pattern in
what they change. The PM and EM read this before framing the next gate.

EOF

emit agents/eng-manager/board/_index.md <<'EOF'
# Board

**Machine WIP 1** (`config/config.yaml` → `wip.machine_limit`) — counts states
`ready` through `ready-to-ship`. One ticket in flight at a time, shipped
before the next starts. **Currently 0/1.**
**Approver-facing WIP 2 — currently 0/2. Approval cap 3 — currently 0/3.**

`priority:` is a field on every ticket, and **only the approver sets it.** It is
not `severity`, which is the agent's read of how bad a problem is.

## In flight

| ID | Title | Project | State | Priority | Owner | Size | Updated |
|---|---|---|---|---|---|---|---|
| ENG-001 | Register this business's repos and prove the loop | __BUSINESS__ | intake | — | product-manager | S | __TODAY__ |

## Waiting on the approver

Cap: 3 across all gates. At the cap, the EM stops advancing tickets into gate
states — more approvals waiting is a backlog with the approver's name on it,
not throughput.

_(none)_
EOF

# Declared by config/conventions.yaml -> instance_layout, and never created by
# this installer. schedules/eng_build_loop.md reads all three by name — step 3
# moves agent findings into proposals.md, step 10 archives old pass entries into
# _index-archive.md, and the observation rule appends to observations.md — so an
# instance without them sends every pass looking for files that are not there.
emit agents/eng-manager/observations.md <<'EOF'
# Observations

"While I was in there, I noticed..." — the thing a good engineer mentions on the
way past. Not a bug, not a ticket, not a request. Cheap to file, no obligation
on anyone, and worth more in aggregate than any single one is alone.

## Rules

- Any agent may append. No permission, no owner, no reply expected.
- One line each, newest last, under the Ledger below.
- An observation is not work. If it needs doing it is a bug or a proposal —
  file it as one instead of writing it here and hoping.
- Nothing reads this on a pass. It is read by the weekly report and by a human.

## Format

`| {date} | {agent} | {project} | {what you noticed} |`

## Ledger

| Date | By | Project | Observation |
|---|---|---|---|
EOF

emit agents/eng-manager/proposals.md <<'EOF'
# Proposals

Things the department thinks are worth building and is **not allowed to build
until the approver says so.** Agent-originated findings land here rather than
shaping straight into tickets: no id, no board row, nothing sequenced.

See `schedules/eng_build_loop.md` step 3.

## How this works

| | |
|---|---|
| **Who writes here** | Any agent — QA, security, devops, the architect, the EM |
| **What becomes a ticket** | Only a proposal the approver has approved |
| **How they see it** | One batched G1 in the weekly report — never a per-item ping |
| **What happens to silence** | Nothing. It stays listed, is re-surfaced weekly, and expires after 30 days |
| **The one bypass** | A **P0 on a registered project** — production down or actively exploitable, with real users — goes straight to a ticket |

Silence is not approval, and an unapproved proposal is not a rejection. Expiry
is the terminus, chosen deliberately over a queue that only grows.

## Open

| Filed | By | Project | What | Why it matters | Size |
|---|---|---|---|---|---|

## Approved

Moved here with its ticket id when the approver approves it. The row leaves
Open; it is never deleted.

| Filed | Approved | Ticket | Project | What |
|---|---|---|---|---|
EOF

emit agents/eng-manager/board/_index-archive.md <<'EOF'
# Engineering Board — pass log archive

Dated pass entries moved out of `_index.md` once the live board holds more than
three, newest first. The live board keeps its table plus enough recent narrative
to resume a ticket; everything older lives here.

Nothing reads this file on a pass — it is the department's history, not its
state. `lib/eng-gate-check.sh` globs `ENG-*.md` and never sees it.

This exists because every pass reads `_index.md` in full, so an append-only log
there is a tax on every future pass.

---

_(no archived entries yet)_
EOF

emit agents/eng-manager/board/ENG-001-register-repos-and-prove-the-loop.md <<EOF
---
id: ENG-001
title: Register this business's repos and prove the loop runs end to end
project: $BUSINESS
type: chore
size: S
severity: P3
priority:
state: intake
owner: product-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: $(date '+%Y-%m-%d')
updated: $(date '+%Y-%m-%d')
branch:
depends_on: []
blocks: []
parent:
links:
  prd:
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
---

# Register this business's repos and prove the loop runs end to end

The seed ticket every instance starts with. It exists for two reasons.

**First, a board with nothing on it is not a clean board.** \`lib/eng-gate-check.sh\`
fails closed on an empty board directory, deliberately — the riskiest failure in
this department is a root that resolves somewhere real and empty, which under a
permissive rule would print nothing and exit 0. This ticket is what makes a fresh
instance distinguishable from a misresolved one.

**Second, it is genuinely the first work.** Nothing can be built until the repos
are registered.

## Acceptance criteria

1. Every repo this business owns is registered in \`config/projects.md\` at **L1**,
   via \`skills/repo-onboarder/SKILL.md\`, and the approver has approved each.
2. A department-owned git worktree exists under \`_eng/\` for each registered repo.
3. \`lib/eng-gate-check.sh\` exits 0 against this instance.
4. One real ticket has moved \`intake → shaped\` and the board renders it.

## Notes

Close this ticket once the first real ticket is on the board — not before, or the
board is empty again.
EOF

echo
if [ "$APPLY" -eq 1 ]; then
  # The board index is written from a quoted heredoc (it contains backticks),
  # so its two variable fields are placeholders expanded here.
  sed -i.bak -e "s/__BUSINESS__/$BUSINESS/g" -e "s/__TODAY__/$(date '+%Y-%m-%d')/g" \
    "$INST/agents/eng-manager/board/_index.md" && rm -f "$INST/agents/eng-manager/board/_index.md.bak"
  echo "Instance created. Validating…"
  if ENG_ROOT="$INST" sh "$DEPT/lib/eng-gate-check.sh"; then
    echo "eng-gate-check: exit 0 — instance is valid."
  else
    echo "eng-gate-check: FAILED (exit $?) — instance is not valid." >&2; exit 1
  fi
  echo
  sh "$DEPT/lib/eng-schedule.sh" --apply
  echo
  echo "Next:"
  echo "  1. Fill in config/config.yaml — approver name and any filers."
  echo "  2. Register repos:  skills/repo-onboarder/SKILL.md"
  echo "  3. ENG_INSTANCE=$INST sh $DEPT/lib/eng-setup.sh --apply"
  echo "     repo-onboarder runs this itself on approval, so this is the repair"
  echo "     command: it verifies the instance directories and checks out a"
  echo "     worktree for any registry row that lacks one. Safe to re-run."
  echo "  4. Run the department with ENG_INSTANCE=$INST"
else
  echo "DRY RUN complete. Re-run with --apply to create it."
  echo
  sh "$DEPT/lib/eng-schedule.sh"
fi
