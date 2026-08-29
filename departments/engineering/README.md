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

## Hosts

The department runs on macOS and on Windows (Git Bash). `lib/eng-env.sh` sets
`$ENG_HOST` to `mac`, `windows`, `linux` or `unknown`, and every host difference
in the department resolves through that one variable.

| | macOS | Windows (Git Bash) |
|---|---|---|
| Scheduler | `launchd`, `~/Library/LaunchAgents` | Task Scheduler, tasks under `\business-os\` |
| Installed by | `lib/eng-schedule.sh --apply` | the same command — it dispatches to `lib/eng-schedule-win.sh` |
| Inbox watch | `WatchPaths` — a filesystem interrupt | a 5-minute poll (Task Scheduler has no file trigger) |
| Missed run while asleep | caught up by `StartCalendarInterval` | caught up by `StartWhenAvailable` |
| Runs a pass with | `/bin/zsh lib/run-claude.sh` | `Git\bin\bash.exe -l` → `lib/run-claude.sh` |
| Needs by hand | Full Disk Access for `sh`, `zsh`, `claude` | nothing; but tasks run only while you are logged on |

Three things are worth knowing before debugging a Windows pass:

- **`-l` is required.** A scheduled task inherits only the Windows `PATH`, so a
  non-login shell cannot find `dirname` or `date`, let alone `node`. The login
  shell sources `/etc/profile`, which builds the MSYS `PATH`.
- **`python3` is not an interpreter on a stock Windows.** It is a Microsoft Store
  redirector that exits 49. `lib/eng-env.sh` resolves a real one into
  `$ENG_PYTHON` and puts `lib/shims/python3` on `PATH` so the bare-name call
  sites keep working.
- **On-demand task launches are slow** — measured at ~2.5 minutes from
  `schtasks /Run` to first output on a laptop. Scheduled fires are prompt. If a
  task looks hung, check `Get-ScheduledTaskInfo` before assuming it is.

Neither host is guessed at install time: `lib/eng-setup.sh` reports what it
finds, and says what is missing.

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
Checked inside each component at start of run, never by the scheduler — the
scheduler (cron, launchd or Task Scheduler) keeps firing and the run exits
silently. That is what makes resuming a one-line edit with nothing to reinstall.
Same convention the rest of business-os uses.

To pause ONE business rather than all of them, set `mode:` in that instance's
`config/config.yaml`; it wins over the global value.

## Contract

`config/conventions.yaml` is the seam between the template and a business: the
two roots, the instance layout, the role vocabulary, the notify seam, and the
naming conventions. Read it before changing anything structural.
