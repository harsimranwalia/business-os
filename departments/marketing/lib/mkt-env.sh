#!/bin/sh
# mkt-env.sh — resolve the department's two roots and the pause switches.
# Sourced, never executed.
#
# Deliberately the lean sibling of departments/engineering/lib/eng-env.sh. That
# file also carries PATH repair, host detection and scheduler plumbing, because
# the engineering department ships its own build loop and had to survive
# launchd, cron and Git Bash. This department does not ship a loop — its
# routines are invoked by whatever scheduler the instance already uses — so
# adding that machinery here would be carrying a solution to a problem this
# department does not have. If marketing ever grows its own loop, take those
# sections from eng-env.sh rather than reinventing them.
#
#   MKT_DEPT      departments/marketing — the shared template. READ-ONLY.
#   MKT_INSTANCE  instances/{business}/marketing — this business's state.
#                 Everything the department writes goes here, and nowhere else.
#
# A pass that writes under $MKT_DEPT is a bug. Changing the template is a
# deliberate git commit against business-os, not something a run does.
#
# ── SOURCE IT WITH `|| exit 1`. ────────────────────────────────────────────
#
#     . "$(dirname "$0")/mkt-env.sh" || exit 1
#
# The `|| exit 1` is not decoration. When a guard below fails, `return 1`
# leaves this file immediately — which means the `|| exit 1` written on the
# same line here never evaluates, and a caller that does not check the status
# carries straight on with $MKT_INSTANCE unset. In this department that ends
# with a component resolving its paths to nowhere, or worse, to the wrong
# business. Every script in lib/ sources it this way; so should yours.

# ── MKT_DEPT ───────────────────────────────────────────────────────────────
# Derived from this file's own location, so it is correct however the caller
# was invoked. An explicit MKT_DEPT wins, which is what a test harness uses.
MKT_SELF_DIR="$(CDPATH= cd -P -- "$(dirname -- "$0")" && pwd -P)"
if [ -z "${MKT_DEPT:-}" ]; then
  MKT_DEPT="$(CDPATH= cd -P -- "$MKT_SELF_DIR/.." && pwd -P)"
fi
if [ ! -f "$MKT_DEPT/VERSION" ]; then
  echo "[mkt-env] FATAL: \$MKT_DEPT does not look like a department template (no VERSION at $MKT_DEPT)" >&2
  return 1 2>/dev/null || exit 1
fi
export MKT_DEPT

# ── MKT_INSTANCE ───────────────────────────────────────────────────────────
# Never guessed. Guessing wrong here is worse than it is in engineering:
# writing the wrong business's board is recoverable, and publishing one
# business's content to another business's account is not.
if [ -z "${MKT_INSTANCE:-}" ]; then
  echo "[mkt-env] FATAL: \$MKT_INSTANCE is unset. Every run must name the instance it acts on." >&2
  echo "[mkt-env]   e.g. MKT_INSTANCE=\"\$PWD/instances/acme/marketing\"" >&2
  return 1 2>/dev/null || exit 1
fi
if [ ! -f "$MKT_INSTANCE/config/instantiated-from" ]; then
  echo "[mkt-env] FATAL: $MKT_INSTANCE is not an instance (no config/instantiated-from). Run install.sh first." >&2
  return 1 2>/dev/null || exit 1
fi
export MKT_INSTANCE

BUSINESS_OS_ROOT="${BUSINESS_OS_ROOT:-$(CDPATH= cd -P -- "$MKT_DEPT/../.." && pwd -P)}"
export BUSINESS_OS_ROOT

# ── .env: PARSED, not sourced. Two bugs avoided, one of them expensive. ────
#
# 1. AN EXPLICIT ENVIRONMENT VARIABLE MUST WIN OVER THE FILE.
#    `. .env` clobbers whatever the caller set. That is merely surprising in
#    most departments and genuinely dangerous in this one: this is the
#    department that PUBLISHES. Pointing a component at a test endpoint and
#    having .env quietly redirect it at the production one is a mistake whose
#    first symptom is a real message in a real channel. Caught exactly that
#    way on 2026-08-29, testing mkt-notify.sh against a local echo server:
#    the script reported success, the echo server received nothing, and the
#    message had gone to the live webhook. So a key already present in the
#    environment is left alone, and .env only fills in what is missing.
#
# 2. A BAD LINE MUST NOT SILENTLY DROP EVERY LINE BELOW IT.
#    A sourced .env that aborts midway looks exactly like one that succeeded:
#    everything above the bad line loads, everything below it does not. That
#    has already happened in this repo — an unquoted value containing
#    parentheses — and the symptom was a notification path that simply never
#    fired. Parsing line by line skips the bad line and reports it.
#
# Exported, not just assigned: business-os writes bare `KEY=value`, and a
# shell variable is not visible to a child process reading os.environ. The
# export happens here rather than by writing `export` into .env, which would
# make the key parse as "export SLACK_WEBHOOK_URL" for the components that
# read that file line by line.
if [ -f "$BUSINESS_OS_ROOT/.env" ]; then
  while IFS= read -r _line || [ -n "$_line" ]; do
    case "$_line" in
      ''|'#'*) continue ;;
    esac
    _key="${_line%%=*}"
    _val="${_line#*=}"
    case "$_key" in
      *[!A-Za-z0-9_]*|'') 
        echo "[mkt-env] WARNING: skipping unparseable .env line: ${_line%%=*}" >&2
        continue ;;
    esac
    # Already set in the environment? The caller meant it. Leave it.
    eval "_cur=\${$_key+set}"
    [ "${_cur:-}" = "set" ] && continue
    # Strip one layer of surrounding quotes, the way the python loader does.
    case "$_val" in
      \"*\") _val="${_val#\"}"; _val="${_val%\"}" ;;
      \'*\') _val="${_val#\'}"; _val="${_val%\'}" ;;
    esac
    export "$_key=$_val"
  done < "$BUSINESS_OS_ROOT/.env"
fi

# ── The pause switch ───────────────────────────────────────────────────────
# Per-instance, falling back to the business-os-wide MODE. Pausing one
# business must not pause the rest; a genuine all-stop is still one edit to
# business-os/.env.
MKT_MODE="$(sed -n 's/^mode:[[:space:]]*\([^[:space:]#]*\).*/\1/p' \
            "$MKT_INSTANCE/config/config.yaml" 2>/dev/null | head -1)"
[ -n "$MKT_MODE" ] || MKT_MODE="${MODE:-}"
export MKT_MODE

mkt_mode_halts() {
  case "${MKT_MODE:-}" in
    sabbath|retreat|quiet) return 0 ;;
    *) return 1 ;;
  esac
}

# ── The publish freeze ─────────────────────────────────────────────────────
# Narrower than a halt and deliberately separate from it. Planning, drafting,
# review and approval all keep running; nothing publishes. Approved pieces
# queue and drain oldest-first when it lifts.
#
# It needs its own switch because the state it describes is real and common:
# the approver is around enough to work, and not around enough to respond if
# something lands badly. Folding that into MODE would mean choosing between
# stopping everything and publishing unattended.
mkt_publish_frozen() {
  [ -n "${MKT_PUBLISH_FREEZE:-}" ]
}

# ── Paths every component uses ─────────────────────────────────────────────
# Declared once, from conventions.yaml -> instance_layout. A component that
# builds these by string concatenation of its own will drift from the contract
# the first time the layout changes.
MKT_CONTENT="$MKT_INSTANCE/content"
MKT_INBOX="$MKT_INSTANCE/inbox"
MKT_TRACES="$MKT_INSTANCE/traces"
MKT_VOICE="$MKT_INSTANCE/voice"
MKT_KNOWLEDGE="$MKT_INSTANCE/../knowledge"
export MKT_CONTENT MKT_INBOX MKT_TRACES MKT_VOICE MKT_KNOWLEDGE

mkt_log() { # mkt_log <routine> <message>
  mkdir -p "$MKT_TRACES"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $2" >> "$MKT_TRACES/mkt-$1-$(date '+%Y-%m-%d').log"
}
