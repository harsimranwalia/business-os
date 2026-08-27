---
ticket: ENG-001
project: aiorders
author: architect
created: 2026-08-25
adrs: [ADR-001]
one_way_doors: []
touches_data: false
touches_models: false
---

# Register this business's repos and prove the loop runs end to end — technical design

## Approach

No code is written. All four acceptance criteria are already true on disk —
see the PRD's Acceptance criteria section for the citations. The remaining
work is recording that verification honestly in the states that normally
expect a diff, and defining what those states and their receipts mean when
there is none. See ADR-001 for the decision and the rejected alternatives.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `agents/eng-manager/board/ENG-001-*.md` | log entry at `building`, citing the exact `config/projects.md` rows, `_eng/` worktree paths, and the `lib/eng-gate-check.sh` re-run that satisfy AC1-3, plus `ENG-002`'s state for AC4 | eng-manager |
| `agents/principal-engineer/reviews/ENG-001.md` | new — reviews the verification claims against disk, not a diff | principal-engineer |
| `agents/qa/test-plans/ENG-001.md` | new — confirms AC1-4 against disk; no suite exists to run | qa |
| `agents/security/reviews/ENG-001.md` | new — confirms there is no code, dependency, endpoint, or secret to scan | security |

## Data

Not applicable — `touches_data: false`.

## Interfaces

None. No code, no contract change.

## Alternatives considered

See ADR-001 — internal-lane registration and `parent:` delegation, both
considered and rejected there.

## One-way doors

None. See ADR-001 → Consequences → Reversibility.

## Risks

- **A future skill or script assumes every `full`-lane ticket carries a
  `branch:`.** Mitigated by leaving `branch:` empty with a log note rather
  than fabricating one — an empty field is a "not yet set" state every
  existing consumer already has to handle, not a new shape.

## Rollout

Not applicable — nothing is deployed. The ticket's own "release" is this
instance's board correctly reflecting facts that are already true.

## Out of scope

Whether this pattern should generalise into the department's shared template
(`departments/engineering/`) so every future instance's own seed ticket
inherits it — this instance cannot write there. ADR-001's Review trigger
leaves this for the approver if a second occurrence ever makes it worth
raising.
