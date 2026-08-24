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

ulimit -n unlimited 2>/dev/null || ulimit -n 65536
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

# Absolute path on purpose: a PATH lookup resolves to a binary launchd cannot
# read under macOS TCC. NOTE: this path is machine-specific and is the last
# hardcoded host assumption left in the department template.
exec /Users/hwalia/.local/bin/claude --dangerously-skip-permissions "$@"
