#!/bin/sh
# eng-env.sh — resolve the department's two roots and provide the shared shell
# helpers. Sourced, never executed.
#
# Ported from life-os's lib/life-os-env.sh 2026-08-22. The one structural
# change: life-os had a single root, because the department and the state it
# wrote lived in the same repo. A reusable department has two.
#
#   ENG_DEPT      departments/engineering — the shared template. READ-ONLY.
#   ENG_INSTANCE  instances/{business}/engineering — this business's state.
#                 Everything the department writes goes here, and nowhere else.
#
# A pass that writes under $ENG_DEPT is a bug. Changing the template is a
# deliberate git commit against business-os, not something a run does.

# ── ENG_DEPT ───────────────────────────────────────────────────────────────
# Derived from this file's own location, so it is correct however the caller
# was invoked — cron, a skill, or by hand. An explicit ENG_DEPT wins, which is
# what the test harness uses.
ENG_SELF_DIR="$(CDPATH= cd -P -- "$(dirname -- "$0")" && pwd -P)"
if [ -z "${ENG_DEPT:-}" ]; then
  ENG_DEPT="$(CDPATH= cd -P -- "$ENG_SELF_DIR/.." && pwd -P)"
fi
if [ ! -f "$ENG_DEPT/VERSION" ]; then
  echo "[eng-env] FATAL: \$ENG_DEPT does not look like a department template (no VERSION at $ENG_DEPT)" >&2
  return 1 2>/dev/null || exit 1
fi
export ENG_DEPT

# ── ENG_INSTANCE ───────────────────────────────────────────────────────────
# Never guessed. An instance is chosen explicitly, because guessing wrong means
# writing one business's board into another's repo — the one failure this
# split exists to make impossible.
if [ -z "${ENG_INSTANCE:-}" ]; then
  echo "[eng-env] FATAL: \$ENG_INSTANCE is unset. Every run must name the instance it acts on." >&2
  echo "[eng-env]   e.g. ENG_INSTANCE=\"\$PWD/instances/aiorders/engineering\"" >&2
  return 1 2>/dev/null || exit 1
fi
if [ ! -f "$ENG_INSTANCE/config/instantiated-from" ]; then
  echo "[eng-env] FATAL: $ENG_INSTANCE is not an instance (no config/instantiated-from). Run install.sh first." >&2
  return 1 2>/dev/null || exit 1
fi
export ENG_INSTANCE

# ENG_ROOT is what lib/eng-gate-check.sh reads. It is the INSTANCE: the board,
# the receipts and the waivers it checks are all per-business state.
ENG_ROOT="$ENG_INSTANCE"
export ENG_ROOT

# ── The pause switch ───────────────────────────────────────────────────────
# business-os convention (.env → MODE), replacing life-os's clone/context/modes.md.
# Checked inside the component, never by the scheduler: cron keeps firing and
# the run exits silently. Same semantics the existing business-os components use.
BUSINESS_OS_ROOT="${BUSINESS_OS_ROOT:-$(CDPATH= cd -P -- "$ENG_DEPT/../.." && pwd -P)}"
export BUSINESS_OS_ROOT
# The failure is REPORTED, not swallowed. `. .env 2>/dev/null` hid a real one:
# an unquoted `REDDIT_USER_AGENT=…v1.0 (by /u/aiorders-io)` was a shell syntax
# error, so sourcing aborted at that line and every variable BELOW it was never
# loaded. MODE sits above it and loaded fine, so the pause switch worked and the
# breakage was invisible — SLACK_WEBHOOK_URL, added below it, silently did not
# exist. A partial source is the worst outcome here: it looks exactly like a
# working one. Python components are unaffected (load_env() parses line by line);
# this only ever bit the shell path.
if [ -f "$BUSINESS_OS_ROOT/.env" ]; then
  if ! . "$BUSINESS_OS_ROOT/.env" 2>/dev/null; then
    echo "[eng-env] WARNING: $BUSINESS_OS_ROOT/.env did not source cleanly — variables after the first bad line are NOT loaded. Quote any value containing spaces or parentheses." >&2
  fi
fi

# business-os writes .env as bare `KEY=value` because its Python components parse
# the file themselves (see load_env() in scripts/telegram.py). Sourcing a bare
# assignment sets a SHELL variable, which is enough for MODE — read in this same
# shell — but not for anything read by a CHILD process. eng-notify.sh is a child,
# and reads SLACK_WEBHOOK_URL from os.environ, so without this export it would
# find nothing and log "SLACK_WEBHOOK_URL unset — cannot notify" on every raise.
# Exported here rather than by writing `export` into .env: that would make the
# key parse as "export SLACK_WEBHOOK_URL" in load_env(), which is a trap for the
# next component that reads it that way.
# `if`, not `[ … ] && export`: this is the last statement in the block, and the
# `&&` form returns 1 when the variable is unset, which a caller sourcing this
# under `set -e` would take as a failed source.
if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then export SLACK_WEBHOOK_URL; fi

# The pause switch is PER-INSTANCE, falling back to the business-os-wide MODE.
# It was global only: one `sabbath` in business-os/.env silenced every business
# at once, which is wrong the moment there is more than one — pausing AIOrders
# because another business is mid-incident stops work nobody asked to stop.
# An instance's own `mode:` wins; the global value remains the default so a
# genuine all-stop is still one edit.
ENG_MODE="$(sed -n 's/^mode:[[:space:]]*\([^[:space:]#]*\).*/\1/p' \
            "$ENG_INSTANCE/config/config.yaml" 2>/dev/null | head -1)"
[ -n "$ENG_MODE" ] || ENG_MODE="${MODE:-}"
export ENG_MODE

eng_mode_halts() {
  case "${ENG_MODE:-}" in
    sabbath|retreat|quiet) return 0 ;;
    *) return 1 ;;
  esac
}

# ── Host + shell detection ─────────────────────────────────────────────────
case "$(uname -s)" in
  Darwin) ENG_HOST="mac" ;;
  Linux)  ENG_HOST="linux" ;;
  *)      ENG_HOST="unknown" ;;
esac
ENG_SHELL="$([ -x /bin/zsh ] && echo /bin/zsh || echo /bin/sh)"
export ENG_HOST ENG_SHELL

# ── Helpers ────────────────────────────────────────────────────────────────
eng_timeout() {
  _t_secs="$1"; shift
  if command -v timeout >/dev/null 2>&1; then timeout "$_t_secs" "$@"
  elif command -v gtimeout >/dev/null 2>&1; then gtimeout "$_t_secs" "$@"
  else "$@"; fi
}
eng_timed_out() { [ "$1" -eq 124 ] || [ "$1" -eq 137 ]; }

eng_mtime() {
  if [ "$ENG_HOST" = "mac" ]; then stat -f %m "$1" 2>/dev/null
  else stat -c %Y "$1" 2>/dev/null; fi
}
eng_stamp() { date '+%Y-%m-%dT%H:%M:%S%z'; }

# Run a headless Claude pass from the INSTANCE directory — that is the cwd every
# agent's relative paths resolve against.
eng_run_claude() {
  _rc_secs="${ENG_PASS_TIMEOUT:-}"
  cd "$ENG_INSTANCE" || return 1
  if [ -n "$_rc_secs" ]; then
    eng_timeout "$_rc_secs" "$ENG_SHELL" "$ENG_DEPT/lib/run-claude.sh" "$@"
  else
    "$ENG_SHELL" "$ENG_DEPT/lib/run-claude.sh" "$@"
  fi
}

eng_sha1() {
  if command -v shasum >/dev/null 2>&1; then shasum | cut -d' ' -f1
  elif command -v sha1sum >/dev/null 2>&1; then sha1sum | cut -d' ' -f1
  else cksum | cut -d' ' -f1; fi   # not a hash, but a stable change detector
}

# A git sync running against the instance holds the repo lock. Launching a
# claude pass into that is how a half-written tree gets read as the real one.
eng_wait_for_git_sync() {
  _wg_lock="$ENG_INSTANCE/traces/.git-sync.lock"
  _wg_waited=0
  command -v flock >/dev/null 2>&1 || return 0
  while [ "$_wg_waited" -lt 60 ]; do
    flock -n -E 99 "$_wg_lock" true >/dev/null 2>&1
    if [ "$?" -ne 99 ]; then
      [ "$_wg_waited" -gt 0 ] && echo "[eng-env] git-sync finished after ${_wg_waited}s — proceeding"
      return 0
    fi
    [ "$_wg_waited" -eq 0 ] && echo "[eng-env] git-sync holds the repo lock — waiting before launching claude"
    sleep 2
    _wg_waited=$(( _wg_waited + 2 ))
  done
  echo "[eng-env] git-sync still holds the lock after 60s — proceeding anyway" >&2
  return 0
}
