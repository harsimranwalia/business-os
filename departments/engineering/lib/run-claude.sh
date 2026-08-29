#!/bin/sh
# The launcher every department pass goes through. Ported from life-os, and the
# port missed the one line that mattered.
#
# It used to `cd /Users/hwalia/Documents/projects/life-os` — a verbatim carry-over
# that pointed EVERY business's pass at life-os's tree. eng_run_claude cds to
# $ENG_INSTANCE and this cd'd straight back out, so on 2026-08-24 an AIOrders pass
# ran claude against life-os's CLAUDE.md, board, schedules and inboxes while its
# prompt described AIOrders work. Caught mid-pass and killed before it wrote
# anything; nothing in life-os was modified.
#
# The caller owns the working directory. eng_run_claude cds to $ENG_INSTANCE
# immediately before invoking this, so inherit that rather than choosing a
# directory here — choosing one here is exactly how the bug above happened.
# $ENG_INSTANCE is honoured only as a fallback for a direct invocation.

# Both arms silenced, and `true` on the end. Windows allows neither value and
# the second arm's failure was not redirected, so every pass log on that host
# opened with 'ulimit: open files: cannot modify limit: Operation not
# permitted' — a line that means nothing here and looks like a cause during an
# outage. Raising the limit is best-effort everywhere; failing to is not fatal.
ulimit -n unlimited 2>/dev/null || ulimit -n 65536 2>/dev/null || true
unset CLAUDECODE  # allow spawning from within an existing Claude Code session

# POSIX, not zsh's `${0:a:h}`. eng-env.sh sets ENG_SHELL=/bin/sh on any host with
# no zsh, and this file is run as an ARGUMENT to that shell — so the shebang is
# bypassed and a zsh-only expansion would be a hard syntax error there.
if [ -n "${ENG_INSTANCE:-}" ] && [ "$PWD" != "$ENG_INSTANCE" ]; then
  cd "$ENG_INSTANCE" || exit 1
fi

# Deliberately does NOT source .env. The old line sourced "$SCRIPT_DIR/../.env",
# which was life-os's repo root and here resolves to departments/engineering/.env
# — a file that does not exist, so it silently did nothing. eng-env.sh already
# loads and exports what a pass needs before it ever calls this, and env is
# inherited across exec. Re-sourcing here would add a second place for a
# malformed .env to kill a pass, with nothing gained.

# Resolved, not hardcoded. This line read `exec /Users/hwalia/.local/bin/claude`
# — one developer's home directory, and the last hardcoded host assumption in
# the template. On any other machine every pass died instantly with a "no such
# file or directory" that reaches no log anyone reads, because this is exec'd
# with its output already redirected into the pass log by the caller.
#
# The ORDER preserves the macOS reason the path was absolute in the first place.
# Under TCC a `claude` reached by PATH lookup can resolve to a binary launchd is
# not permitted to read, so a KNOWN install location is tried before PATH rather
# than after it:
#   $ENG_CLAUDE_BIN      explicit override, for a non-standard install
#   ~/.local/bin/claude  the native installer's location on mac, linux AND
#                        Windows (Git Bash execs the extensionless binary fine)
#   PATH                 winget, npm and homebrew installs, and anything else
if [ -n "${ENG_CLAUDE_BIN:-}" ] && [ -x "$ENG_CLAUDE_BIN" ]; then
  ENG_CLAUDE="$ENG_CLAUDE_BIN"
elif [ -x "$HOME/.local/bin/claude" ]; then
  ENG_CLAUDE="$HOME/.local/bin/claude"
else
  ENG_CLAUDE="$(command -v claude 2>/dev/null)"
fi

# Loud, and on stderr. A pass that cannot find its binary must not look like a
# pass that ran and found nothing to do — that ambiguity is what made the
# 2026-08 outages take six days to spot.
if [ -z "${ENG_CLAUDE:-}" ]; then
  echo "run-claude.sh: FATAL — no claude binary found." >&2
  echo "run-claude.sh: looked at \$ENG_CLAUDE_BIN, ~/.local/bin/claude, and PATH." >&2
  echo "run-claude.sh: install Claude Code, or set ENG_CLAUDE_BIN to its full path." >&2
  exit 127
fi

exec "$ENG_CLAUDE" --dangerously-skip-permissions "$@"
