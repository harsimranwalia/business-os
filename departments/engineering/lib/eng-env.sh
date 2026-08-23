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
[ -f "$BUSINESS_OS_ROOT/.env" ] && . "$BUSINESS_OS_ROOT/.env" 2>/dev/null

eng_mode_halts() {
  case "${MODE:-}" in
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
