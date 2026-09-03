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

# Same reasoning as SLACK_WEBHOOK_URL above, for a different failure mode:
# lib/run-claude.sh execs the `claude` binary as a CHILD process, so this must
# be exported to reach it — a bare shell var here is invisible to that exec.
# When set, the CLI's own credential precedence picks this over the plain
# `/login` session (see .env's own comment on this var), which is the point:
# it pins every automated build-loop pass to one account independent of
# whatever is logged into `claude` interactively elsewhere on this host.
#
# ── More than one account ──────────────────────────────────────────────────
# .env may carry a ROSTER: CLAUDE_CODE_OAUTH_TOKEN plus CLAUDE_CODE_OAUTH_TOKEN_2,
# _3, … one per account. Numbered rather than packed into one delimited value
# because .env is BOTH sourced by this file and parsed line-by-line by the
# Python components (load_env() in scripts/telegram.py), so a delimiter would
# be one more thing to quote wrong in a file that already cost us a silent
# partial source — see the guard above.
#
# Exactly ONE of them is ever exported: the CLI takes a single token. Which one
# is whatever index the first field of $ENG_INSTANCE/traces/.oauth-account
# names. lib/eng-trigger.sh OWNS that file — it is the only component that can
# see an account hit its limit and rotate off it — and every other launcher,
# this file included, only reads it. A missing, empty or garbled file means
# account 1, which is exactly the behaviour from before there was a roster.
#
# Collected in order, SKIPPING gaps rather than stopping at one: an operator who
# deletes _2 and leaves _3 has two accounts and stopping at the hole would
# silently run on one — the failure this roster exists to prevent.
ENG_OAUTH_NAMES=""
ENG_OAUTH_COUNT=0
for _eng_oa in CLAUDE_CODE_OAUTH_TOKEN \
               CLAUDE_CODE_OAUTH_TOKEN_2 CLAUDE_CODE_OAUTH_TOKEN_3 \
               CLAUDE_CODE_OAUTH_TOKEN_4 CLAUDE_CODE_OAUTH_TOKEN_5 \
               CLAUDE_CODE_OAUTH_TOKEN_6 CLAUDE_CODE_OAUTH_TOKEN_7 \
               CLAUDE_CODE_OAUTH_TOKEN_8 CLAUDE_CODE_OAUTH_TOKEN_9; do
  eval "_eng_oa_val=\${$_eng_oa:-}"
  [ -n "$_eng_oa_val" ] || continue
  ENG_OAUTH_COUNT=$(( ENG_OAUTH_COUNT + 1 ))
  ENG_OAUTH_NAMES="${ENG_OAUTH_NAMES}${ENG_OAUTH_NAMES:+ }$_eng_oa"
done
unset _eng_oa _eng_oa_val
export ENG_OAUTH_COUNT ENG_OAUTH_NAMES

# The env var NAME of account N — never its value. This is what the rotation
# log lines print, and a token must not reach a log or a Slack notice.
eng_oauth_name() {
  printf '%s' "${ENG_OAUTH_NAMES:-}" \
    | awk -v n="${1:-0}" 'n+0 >= 1 && n+0 <= NF { print $(n+0) }'
}

# Export account N as the token the `claude` child authenticates with.
eng_oauth_use() {
  _ou_name="$(eng_oauth_name "${1:-0}")"
  [ -n "$_ou_name" ] || return 1
  # The name is one of the nine literals above, so this expands a variable we
  # chose; and an assignment neither word-splits nor globs, so a token holding
  # anything at all is still assigned whole.
  # `:-` because eng-trigger.sh sources this file with `set -u` already on, and
  # an aborted source there kills the whole event loop.
  eval "CLAUDE_CODE_OAUTH_TOKEN=\"\${$_ou_name:-}\""
  export CLAUDE_CODE_OAUTH_TOKEN
  return 0
}

# Pick the account in force for this process. Called once here, so every
# launcher that only reads the roster — lib/eng-report.sh's weekly pass, and
# anything else that sources this file — authenticates as the account currently
# in force without knowing how rotation works. lib/eng-trigger.sh re-selects per
# launch, because it is the one that can change the answer mid-flight.
eng_oauth_select() {
  [ "${ENG_OAUTH_COUNT:-0}" -gt 0 ] || return 0
  ENG_OAUTH_CURRENT="$(sed -n '1s/^\([0-9][0-9]*\).*/\1/p' \
                       "$ENG_INSTANCE/traces/.oauth-account" 2>/dev/null)"
  [ -n "$ENG_OAUTH_CURRENT" ] || ENG_OAUTH_CURRENT=1
  if [ "$ENG_OAUTH_CURRENT" -lt 1 ] || [ "$ENG_OAUTH_CURRENT" -gt "$ENG_OAUTH_COUNT" ]; then
    ENG_OAUTH_CURRENT=1
  fi
  export ENG_OAUTH_CURRENT
  eng_oauth_use "$ENG_OAUTH_CURRENT"
}
eng_oauth_select

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
# `windows` means Git Bash / MSYS2, which is the only way the department's
# shell scripts run there — there is no POSIX shell in stock Windows. uname
# reports MINGW64_NT-* under Git Bash, MSYS_NT-* under an MSYS2 shell and
# CYGWIN_NT-* under Cygwin; all three are the same host to everything below.
case "$(uname -s)" in
  Darwin)               ENG_HOST="mac" ;;
  Linux)                ENG_HOST="linux" ;;
  MINGW*|MSYS*|CYGWIN*) ENG_HOST="windows" ;;
  *)                    ENG_HOST="unknown" ;;
esac
ENG_SHELL="$([ -x /bin/zsh ] && echo /bin/zsh || echo /bin/sh)"
export ENG_HOST ENG_SHELL

# ── PATH ───────────────────────────────────────────────────────────────────
# launchd hands a job PATH=/usr/bin:/bin:/usr/sbin:/sbin and nothing else.
# Verified 2026-08-24 with a throwaway probe job: under launchd `timeout`,
# `gtimeout`, `node`, `npm`, `npx` and `gh` are ALL unreachable, while `git`,
# `python3` and `jq` resolve from /usr/bin and work fine.
#
# That gap is not cosmetic. Every registered project's verification command is
# `npm run lint` / `npm run build`, and L1 autonomy means opening a PR with
# `gh` — so a scheduled pass would fail its quality gate for a reason that
# looks nothing like a PATH problem, while the same pass run by hand from a
# terminal passes. Add `timeout`, and the pass timeout silently degrades to
# uncapped exactly when nobody is watching.
#
# Fixed here rather than in the plists because launchd is not the only
# launcher: cron, a nested spawn and a bare `sh eng-trigger.sh` each inherit
# whatever their parent had. eng-env.sh is the one file every entry point
# sources. APPENDED, never prepended — a caller who deliberately put a
# different toolchain in front keeps it.
eng_path_add() {
  [ -d "$1" ] || return 0
  case ":$PATH:" in *":$1:"*) return 0 ;; esac
  PATH="$PATH:$1"
}
# node FIRST, before homebrew. node lives under nvm, which has no stable path
# — the version is in it. Homebrew also ships a node (v24 here) and it would
# otherwise win, handing the department a different major than the human
# builds on: `node --version` in a terminal says 22, a pass would say 24.
# Honour nvm's own `default` alias (a bare major like "22") before falling back
# to newest-installed: building against a newer node than the human ever tests
# on is a real way to produce a green pass on code that breaks for them.
_eng_nvm="$HOME/.nvm/versions/node"
if [ -d "$_eng_nvm" ]; then
  _eng_node_dir=""
  _eng_alias="$(cat "$HOME/.nvm/alias/default" 2>/dev/null)"
  if [ -n "$_eng_alias" ]; then
    _eng_node_dir="$(ls -d "$_eng_nvm/v${_eng_alias#v}"* 2>/dev/null | sort -V | tail -1)"
  fi
  if [ -z "$_eng_node_dir" ]; then
    _eng_node_dir="$(ls -d "$_eng_nvm"/v* 2>/dev/null | sort -V | tail -1)"
  fi
  if [ -n "$_eng_node_dir" ]; then eng_path_add "$_eng_node_dir/bin"; fi
fi
eng_path_add /opt/homebrew/bin      # timeout, gtimeout, gh, git
eng_path_add /usr/local/bin         # intel homebrew, and anything hand-installed
eng_path_add "$HOME/.local/bin"     # claude

# Windows has the same problem as launchd, from a different direction. Task
# Scheduler builds a task's PATH from the registry and sh.exe prepends the MSYS
# tree on top of it, so a scheduled pass gets /usr/bin, /mingw64/bin and the
# system PATH — but NOT the per-user directories winget and the node .msi
# install into. `claude` and `node` are both reachable from an interactive Git
# Bash and both invisible to a scheduled pass, which is exactly the class of
# failure this block already exists to prevent, so it is fixed in the same place.
if [ "$ENG_HOST" = "windows" ]; then
  # $HOME rather than $LOCALAPPDATA: the Windows form of that variable is
  # C:\Users\... and the backslashes are escapes to every test and glob here.
  eng_path_add "$HOME/AppData/Local/Microsoft/WinGet/Links"   # winget's claude shim
  _eng_pf="$(cygpath -u "${PROGRAMFILES:-}" 2>/dev/null)"
  [ -n "$_eng_pf" ] || _eng_pf="/c/Program Files"
  eng_path_add "$_eng_pf/nodejs"                              # node + npm (.msi)
  eng_path_add "$_eng_pf/GitHub CLI"                          # gh
  # python.org's installer offers "Add to PATH" as an OPT-IN checkbox and writes
  # only the per-user registry PATH when it is ticked, so a scheduled task can
  # easily inherit a PATH with no interpreter on it at all — verified by running
  # a pass under PATH=/usr/bin:/bin, where node and claude were both recovered by
  # the lines above and python3 was not. An unmatched glob expands to itself and
  # eng_path_add's -d test rejects it, so a machine without these is unaffected.
  for _eng_pydir in "$HOME/AppData/Local/Programs/Python"/Python3* /c/Python3*; do
    eng_path_add "$_eng_pydir"
  done
fi

export PATH

# ── python3 ────────────────────────────────────────────────────────────────
# lib/run-stream.py and lib/eng-notify.sh invoke the interpreter by the bare
# name `python3`. That is right on mac and linux and WRONG on Windows, in a way
# that passes every obvious check: a stock Windows PATH carries an App Execution
# Alias at AppData/Local/Microsoft/WindowsApps/python3 which is not an
# interpreter at all. Given arguments it prints "Python was not found; run
# without arguments to install from the Microsoft Store" and exits 49. It sits
# AHEAD of a real python.org install on PATH, so `command -v python3` succeeds,
# eng-setup.sh's toolchain check passes, and the interpreter still never runs —
# cost tracking silently records nothing and every approver notification fails.
#
# So the test here is "does it execute python", not "is it on PATH". The answer
# is resolved once and EXPORTED, which serves both kinds of caller: anything
# that wants to be explicit reads $ENG_PYTHON, and the existing bare-name call
# sites keep working through lib/shims/python3.
#
# PREPENDED, unlike everything above it. eng_path_add appends on purpose, so a
# caller who deliberately put a toolchain in front keeps it; here the whole
# point is to beat an entry that is already on PATH, so this one goes first.
eng_python_ok() { [ -n "${1:-}" ] && "$1" -c 'import sys' >/dev/null 2>&1; }
if ! eng_python_ok "${ENG_PYTHON:-}"; then
  ENG_PYTHON=""
  for _eng_py in python3 python python3.exe python.exe; do
    _eng_py_path="$(command -v "$_eng_py" 2>/dev/null)" || continue
    if eng_python_ok "$_eng_py_path"; then ENG_PYTHON="$_eng_py_path"; break; fi
  done
  # Last resort on Windows: the `py` launcher. It installs to C:\Windows, which
  # is on every PATH that exists at all, and it knows where the interpreters are
  # even when none of them is on PATH. Asked for the real executable rather than
  # used directly, because $ENG_PYTHON is expanded as a single word.
  if [ -z "$ENG_PYTHON" ] && command -v py >/dev/null 2>&1; then
    _eng_py_path="$(py -3 -c 'import sys; print(sys.executable)' 2>/dev/null)"
    if eng_python_ok "$_eng_py_path"; then ENG_PYTHON="$_eng_py_path"; fi
  fi
fi
export ENG_PYTHON

if [ -z "${ENG_PYTHON:-}" ]; then
  echo "[eng-env] WARNING: no working python3 on this host — cost tracking (lib/run-stream.py) and approver notifications (lib/eng-notify.sh) will not run." >&2
elif ! eng_python_ok "$(command -v python3 2>/dev/null)"; then
  # cygpath, and NOT a bare "$ENG_DEPT/lib/shims". On Windows `pwd -P` returns a
  # native path — ENG_DEPT is C:/Users/... — and PATH is colon-separated, so
  # prepending it raw contributes TWO broken entries, "C" and "/Users/...".
  # Nothing errors: PATH looks plausible, the directory is simply never
  # searched, and python3 stays missing for a reason invisible in the value.
  # Everywhere else ENG_DEPT is used as a filesystem path, where the native form
  # is fine; PATH is the one place the colon matters.
  _eng_shims="$ENG_DEPT/lib/shims"
  if command -v cygpath >/dev/null 2>&1; then
    _eng_shims="$(cygpath -u "$_eng_shims" 2>/dev/null || echo "$_eng_shims")"
  fi
  case ":$PATH:" in
    *":$_eng_shims:"*) : ;;
    *) PATH="$_eng_shims:$PATH"; export PATH ;;
  esac
fi

# ── The department's own working copies ────────────────────────────────────
# NEVER a human's checkout: a cron-triggered pass running git under someone's
# uncommitted changes is how work gets lost. Every registered repo gets a
# worktree the department owns, at $ENG_WORKTREES/{project}.
#
# It sits beside the repos it mirrors rather than inside business-os, because a
# git worktree nested inside another repo is a mess for both. Flat, not
# namespaced per business: this directory already holds real worktrees created
# before the carve-out, and skills/release-runner/SKILL.md documents
# `_eng/{project}` as the path. lib/eng-setup.sh creates them.
ENG_WORKTREES="${ENG_WORKTREES:-$(dirname "$(dirname "$BUSINESS_OS_ROOT")")/_eng}"
export ENG_WORKTREES

# ── Helpers ────────────────────────────────────────────────────────────────
eng_timeout() {
  _t_secs="$1"; shift
  if command -v timeout >/dev/null 2>&1; then timeout "$_t_secs" "$@"
  elif command -v gtimeout >/dev/null 2>&1; then gtimeout "$_t_secs" "$@"
  else "$@"; fi
}
eng_timed_out() { [ "$1" -eq 124 ] || [ "$1" -eq 137 ]; }

# BSD stat on mac, GNU stat everywhere else — Git Bash ships GNU coreutils, so
# `windows` takes the same branch as linux and needs no case of its own.
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
