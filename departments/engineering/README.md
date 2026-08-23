# Engineering department

Ten agents that build software end-to-end, from a business need to a merged PR.
Ported out of `life-os` on 2026-08-22 to become reusable across businesses.

**Read `docs/engineering-team.md`** for the pipeline, the eight gates, the
artifact chain and the autonomy model. That document is the department. This one
only explains how to run it for a business.

## The two roots

The single structural difference from the life-os original: life-os had one root,
because the department and the state it wrote lived in the same repo. A reusable
department has two.

| | |
|---|---|
| `$ENG_DEPT` | `departments/engineering/` — the shared template. **Read-only at runtime.** |
| `$ENG_INSTANCE` | `instances/{business}/engineering/` — one business's state. The only thing ever written to. |

A pass that writes under `$ENG_DEPT` is a bug. Changing the template is a
deliberate commit against business-os, not something a run does.

Agent **definitions** are shared. Agent **memory** is per-instance — a notebook is
business-specific learning and is never shared across businesses.

## Install

```sh
./install.sh <business> --approver <name>            # dry run, writes nothing
./install.sh <business> --approver <name> --apply    # create the instance
```

It creates a life-os-shaped instance root, seeds `ENG-001`, and validates itself
by running `lib/eng-gate-check.sh` against the result. Exit 0 means the instance
is real.

The shape is deliberate. `lib/eng-gate-check.sh` hardcodes its receipt paths, and
per ADR-002 the scripts are the only enforceable surface this department has — so
an instance matches those paths and runs the enforcement unmodified rather than
having the enforcement edited to match a prettier layout.

## Run

```sh
export ENG_DEPT=/path/to/departments/engineering
export ENG_INSTANCE=/path/to/instances/<business>/engineering
sh "$ENG_DEPT/lib/eng-trigger.sh" scheduled
```

`ENG_INSTANCE` is never guessed. Guessing wrong means writing one business's
board into another's repo, which is the one failure the split exists to prevent.

## Roles

**The approver** — the single human with gate authority: G1 scope, G2
one-way-door, G3 release. The five machine gates (code review, migration,
quality, release readiness, security) stay machine-owned and blocking; only the
approver overrides one, explicitly, logged as an ADR.

**A filer** — may submit a request, holds no gate authority. Requests land in
`inbox/requests/` with `source: filer` and are shaped by the PM like any other
intake. A filer never receives a gate.

Bound per instance in `config/config.yaml`. No file in the template names a person.

## Pause

`.env` → `MODE` set to `sabbath`, `retreat` or `quiet` halts every component.
Checked inside each component at start of run, never by the scheduler — cron keeps
firing and the run exits silently. Same convention the rest of business-os uses.

## Contract

`config/conventions.yaml` is the seam between the template and a business: the
two roots, the instance layout, the role vocabulary, the notify seam, and the
naming conventions. Read it before changing anything structural.
