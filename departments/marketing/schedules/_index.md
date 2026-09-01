# Marketing schedules

One file per routine, git-tracked and portable — this directory is what an
instance reads to recreate every scheduled job on a new machine. This file is
the single "what runs when" view; the per-routine files hold the reasoning.

**Nothing here installs anything.** The department describes the routine and
the **capability** it needs; the **instance binds the mechanism** — cron on an
always-on host, a wake-aware calendar scheduler on a machine that sleeps, or a
desktop-app routine where a live browser session is required. A pass that
writes under `$MKT_DEPT` is a bug, and that includes writing a scheduler
entry.

## At a glance

| Routine | Status | Fires | Publishes / produces | Halted by `MODE` | Blocked by `MKT_PUBLISH_FREEZE` | Headless? |
|---|---|---|---|---|---|---|
| [`mkt_weekly_plan`](mkt_weekly_plan.md) | 📋 ported | Weekly, plus a catch-up fire the next day | The week's drafts on the approval surface + the unified weekly report | yes | no — planning continues under a freeze | yes |
| [`ship_content`](ship_content.md) | 📋 ported | **Daily**; the skill gates the publishing days | One piece, on the **API-seam** channel | yes | **yes** | yes |
| [`ship_content_x`](ship_content_x.md) | 📋 ported | **Daily**; the skill gates the publishing days | One piece, on the **browser-seam** channel | yes | **yes** | **no — needs a live logged-in session** |

## Named in the department doc, no schedule file here

Not ported. Each ran, or was designed to run, in the system this came from;
none is wired, and none has a file in this directory to wire from. Listed so
the gap is visible rather than discovered.

| Routine | What it would do | Why it isn't here |
|---|---|---|
| engagement collection | Read the numbers back for shipped pieces and write `performance/` | Every platform's collection path is different, and the port's ran behind an authenticated browser session — no portable form to ship |
| outperformer interrupt | Detect a piece well above baseline early and brief follow-ups | Designed, never wired, in the original too. It needs a live performance store to watch |
| positioning audit | Score recent shipped pieces against the positioning statement | Designed, never wired. Runs when invoked |

Until engagement collection exists, `performance/` fills only when something
writes to it, and the baselines every channel playbook refers to stay
`unknown`. That is the honest state — and "unknown" in a playbook is correct
behaviour, not a to-do someone forgot.

## Status legend

- ✅ **WIRED** — installed in a scheduler on a host, verified running.
- 📋 **PORTED** — designed, and proven in the system it came from, but not
  wired here. Safe to bind following the routine file's *Capability required*
  section.
- 📋 **DESIGNED** — defined here, never run anywhere.

## Two rules that hold across every routine

**The mode check lives inside the run, never in the scheduler.** Cron keeps
firing while `MODE` is set to `sabbath`, `retreat` or `quiet`; each run reads
it, logs one line, and exits. That is deliberate — a paused department that is
still being scheduled resumes by itself when the value is cleared, with nothing
to re-install.

**A ship routine publishes at most one piece per channel per publishing day,
oldest approved first.** Never a burst, never out of order, and a backlog is a
queue to resume rather than permission to catch up. This is per channel, so two
channels may both publish on the same day — but neither one publishes twice.

## Binding these to a host

Read the routine file's **Capability required** section first; it names what
the scheduler must be able to do rather than which scheduler to use. Two
things decide the binding:

1. **Does it need a live browser session?** `ship_content_x` does, so it cannot
   live on the same host as the rest. Every other routine is headless and can
   run wherever the department runs.
2. **Does the host sleep?** If it does, prefer a scheduler that catches a
   missed run on wake. Plain cron silently drops anything scheduled while the
   machine was asleep, and a silently dropped planning run is a week with no
   content queued.

The instance is also where **cadence** is bound, and it belongs in
`config/config.yaml` → `channels`, not in the scheduler. Both ship routines
fire daily and gate the days from config on purpose: it keeps a cadence change
to a one-line edit, and it stops one prompt existing in three drifting copies.
