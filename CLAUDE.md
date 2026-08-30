# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

business-os runs a semi-autonomous marketing/community-engagement operation with a human-in-the-loop
approval step. The current build targets Reddit community engagement for one business (AIOrders), but
the design is meant to be business-agnostic: all business-specific facts live in `knowledge/`, and
everything else (agents, skills, scripts) reads from there instead of hardcoding domain knowledge.

There is no build system, package manifest, or test suite — this is Python stdlib scripts plus
Claude Code agents/skills, wired together by cron.

## Constitution (binding on every agent/skill in this repo)

`.claude/agents/reddit-community-builder.md` explicitly inherits these rules from this file — treat
them as non-negotiable when writing or modifying any agent/skill:

- **No auto-send.** Content reaches an external platform only after a human approves it via Telegram.
  Agents/skills draft and persist to the CRM at `status=pending`; they never flip a record to
  `approved` or `posted` themselves.
- **Quiet mode.** If repo-root `.env` sets `MODE=sabbath|retreat|quiet`, every component (listener,
  notifier, poster, agent) exits immediately/silently. Cron keeps firing; the check happens inside
  each component.
- **One account, no manipulation.** Never suggest alt accounts, vote manipulation, or coordinated
  activity.
- **Honesty over interest.** Never filter out threads just because the honest answer isn't the
  business. Skills must recommend the honest thing even against the business's own interest.
- **Agent/skill updates go through Fable only.** Any edit to an agent or skill definition file —
  `.claude/agents/*.md`, `.claude/skills/*/SKILL.md`, and, in the engineering department,
  `departments/engineering/agents/*/agent.md`, `departments/engineering/agents/*/config.yaml`,
  `departments/engineering/skills/*/SKILL.md` (template and instance copies alike) — is written with
  the Fable model, never whichever model is driving the current session. Delegate the edit to a
  Fable-model agent rather than editing the file directly. Schedules, docs, `lib/` scripts, and
  shared contract files (e.g. `config/conventions.yaml`) are outside this rule. See
  `departments/engineering/config/conventions.yaml` → `authoring` for the engineering department's
  copy of this rule.

## Commands

No installed package manager. Setup and run commands, per script docstring:

```bash
pip install praw                       # only scripts/reddit_listen.py and scripts/reddit_post.py need it
python scripts/reddit_listen.py        # read-only sweep -> inbox/listeners/reddit/
python scripts/content_loop.py notify  # push pending CRM drafts to Telegram
python scripts/content_loop.py poll    # apply approve/skip/edit replies from Telegram
python scripts/content_loop.py list [--community X] [--status Y]
python scripts/reddit_post.py          # posts APPROVED records; the only write path to Reddit
./scripts/install_cron.sh              # install the managed cron block (--remove to uninstall)
```

`install_cron.sh` is POSIX-only — there is no `crontab` on Windows. The
engineering department schedules itself per host instead (`lib/eng-schedule.sh`
dispatches to launchd on macOS and to Task Scheduler on Windows); the Reddit
pipeline above has no Windows scheduler yet.

Everything else (`telegram.py`) is invoked as a subprocess by the other scripts, not run directly.
Config is env vars, loaded from a repo-root `.env` (gitignored) by each script's own `load_env()`.
Required vars are listed in each script's module docstring (Twenty API creds, Telegram bot token/chat
id, Reddit read-only creds, Reddit write creds for the poster) and in `.env` itself. `MODE` in `.env`
is the single quiet-mode switch (`sabbath` / `retreat` / `quiet` / empty for normal operation).

## Architecture

**Layering — manager agent vs. worker skill vs. deterministic script:**

- `.claude/agents/` — manager agents. They hold judgment (which threads, how often, when to stay
  silent) and own memory files, but never draft content and never call an external write API directly.
- `.claude/skills/` — stateless worker skills. `reddit-reply-writer` takes exactly one thread + the
  knowledge-file contents and returns exactly one drafted reply or a `SKIP: <code>`. It holds no
  memory or strategy of its own and must re-read `knowledge/` on every invocation.
- `scripts/` — deterministic Python, no LLM anywhere in the approval or send path. This is the layer
  that's allowed to touch external write APIs (Reddit, Telegram, Twenty).

**The knowledge/ contract:** `knowledge/business-profile.md`, `knowledge/voice-spec.md`, and
`knowledge/claims-allowed.md` are the *only* place business-specific information may live. Agents and
skills load them fresh every run rather than trusting prior context. Porting business-os to a new
business means replacing these three files and nothing else in the codebase.

**Content lifecycle** — Twenty CRM (`Marketing Content` object) is the system of record; a record's
`status` field drives everything:

```
(agent) draft --create--> pending --notify--> [Telegram] --human replies-->
    approve -> approved --reddit_post.py--> posted | failed
    skip[: reason] -> discarded
    edit: <text> -> approved (with body replaced)
```

`scripts/content_loop.py` owns `create` / `notify` / `poll` / `list`. `scripts/reddit_post.py` is the
only component with Reddit write access and is the only thing that moves `approved -> posted|failed`.
See the module docstring in `content_loop.py` for the one-time Twenty object/field setup.

**Directories that hold state, not code:**

- `inbox/` — transient input/signals: `inbox/listeners/reddit/` (sweep JSON from `reddit_listen.py`,
  moved to `inbox/listeners/reddit/processed/` once triaged).
- `memory/` — durable state agents own between runs, e.g. `memory/marketing/subreddit-map.md`
  (per-subreddit rules/cooldowns/status, maintained by the triage agent) and
  `memory/marketing/engagement-log.md` (append-only decision log).
- `logs/` — cron job stdout/stderr, written by `install_cron.sh`'s crontab entries.

**Hosts:** macOS and Windows (Git Bash) are both supported. `$ENG_HOST`, set in
`departments/engineering/lib/eng-env.sh`, is the single place host differences
are decided — scheduler, PATH recovery, `stat` flags and the `python3` shim all
branch on it. `.gitattributes` pins `*.sh`, `*.py` and `*.yaml` to LF so a
Windows checkout does not put a carriage return inside a value the shell parses.

**Execution model:** the agent is cron-invoked, not a persistent loop (see the header comment in
`scripts/install_cron.sh`). Every run is stateless; all state lives in the CRM, `memory/`, and
`inbox/`, so a crash costs nothing and context never silently accumulates. Deterministic scripts run
on tight cycles (5–30 min); the headless `claude -p` triage agent runs a few times daily, shortly after
each listener sweep.
