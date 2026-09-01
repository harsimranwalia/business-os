#!/usr/bin/env bash
# eng-notify.sh — tell the approver a decision is waiting, so it never just sits there.
#
# The department can do everything else on its own, but three gates and the L1
# merge request need a human. Writing the item to inbox/ and hoping the approver
# opens the control center is not a mechanism — it's a dead end with extra
# steps, and the whole system is built on the rule that every artifact has an
# owner, a next action, AND something that advances it. This is that something.
#
# Posts to #life-os via SLACK_WEBHOOK_URL (connections/slack.md). No new
# connection, no new cost.
#
# Deliberately quiet. Per item, the approver gets AT MOST:
#   1. one message when it's raised
#   2. one nudge if it's still unanswered after 24h
#   3. nothing else — after that it rides the daily brief and weekly report
#
# This system exists to be a counterweight to the approver's attention, not an
# amplifier. Three pings is not urgency; a ping every hour would be.
#
# Usage:
#   eng-notify.sh raise <inbox-file>     first notice
#   eng-notify.sh nudge <inbox-file>     the 24h follow-up

set -uo pipefail

MODE="${1:?mode required}"
ITEM="${2:-}"

LIFEOS_SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$(dirname "$0")/eng-env.sh"

ROOT="$ENG_INSTANCE"      # state lives in the instance, never the template
INBOX="$ROOT/inbox"
LOG="$ROOT/traces/eng-notify-$(date '+%Y-%m-%d').log"
mkdir -p "$ROOT/traces"

source "$BUSINESS_OS_ROOT/.env" 2>/dev/null
if [ -z "${SLACK_WEBHOOK_URL:-}" ]; then
  echo "[$(date '+%H:%M:%S')] SLACK_WEBHOOK_URL unset — cannot notify" >> "$LOG"
  # Not fatal to the loop. The item is still in the inbox and still shows in the
  # Engineering tab; only the push is missing. Fail loud in the log, never
  # silently, and never block a build pass on a notification.
  exit 0
fi

# Build the JSON with python3 rather than string-interpolating into a heredoc.
# Everything below comes out of a markdown file the approver or an agent wrote — a
# single double-quote in a recommendation line would produce invalid JSON, Slack
# would reject it, and the notification would fail silently. Silent failure is
# the one outcome this script exists to prevent.
post() {
  python3 -c '
import json, os, sys, urllib.request
payload = json.dumps({"text": sys.argv[1]}).encode()
req = urllib.request.Request(os.environ["SLACK_WEBHOOK_URL"], data=payload,
                             headers={"Content-Type": "application/json"})
try:
    urllib.request.urlopen(req, timeout=10).read()
except Exception as e:
    print(f"slack post failed: {e}", file=sys.stderr)
    sys.exit(1)
' "$1" 2>> "$LOG"
  if [ $? -eq 0 ]; then
    echo "[$(date '+%H:%M:%S')] sent: $MODE ${ITEM:+$(basename "$ITEM")}" >> "$LOG"
  else
    echo "[$(date '+%H:%M:%S')] FAILED: $MODE ${ITEM:+$(basename "$ITEM")} — item still in inbox and in the tab" >> "$LOG"
  fi
}

# How many decisions are already waiting? Context for the approver — one thing
# to look at reads differently from five.
waiting_count() {
  local n=0
  # `for f in "$INBOX"/*.md` with a -f guard, not zsh's (N) glob qualifier:
  # this file has to run under bash in the container too.
  for f in "$INBOX"/*.md; do
    [ -f "$f" ] || continue
    grep -q '^type: eng-decision' "$f" 2>/dev/null || continue
    grep -q '^decision:' "$f" 2>/dev/null && continue
    n=$(( n + 1 ))
  done
  echo "$n"
}

fm() { grep -m1 "^$1:" "$ITEM" 2>/dev/null | sed "s/^$1:[[:space:]]*//"; }

[ -f "$ITEM" ] || { echo "[$(date '+%H:%M:%S')] no such item: $ITEM" >> "$LOG"; exit 0; }

GATE=$(fm gate); TICKET=$(fm ticket); PROJECT=$(fm project)
REC=$(fm recommendation); PR=$(fm pr_url)
TITLE=$(grep -m1 '^# ' "$ITEM" 2>/dev/null | sed 's/^# //')
N=$(waiting_count)

case "$GATE" in
  G1)    WHAT="Is this worth building?" ;;
  G2)    WHAT="A one-way door — expensive to reverse." ;;
  G3)    WHAT="Ship it to production?" ;;
  merge) WHAT="A PR is ready for you to merge." ;;
  *)     WHAT="A decision is waiting." ;;
esac

# The most useful line in the message: what happens if he does nothing. Without
# it, every notification reads as equally urgent, which is how a system starts
# manufacturing urgency. No hard cap on how many decisions may queue — just an
# honest count of what's waiting.
if [ "$N" -gt 1 ]; then
  CONSEQUENCE="If you do nothing: this ticket waits, the rest of the board keeps moving. ${N} decisions waiting on you right now."
else
  CONSEQUENCE="If you do nothing: this ticket waits, the rest of the board keeps moving."
fi

PREFIX=""
# A real newline, not a literal \n — this string is sent as-is, not echo -e'd.
[ "$MODE" = "nudge" ] && PREFIX="_Still waiting, 24h on._

"

post "${PREFIX}:wrench: *Engineering — ${GATE:-decision}* · \`${TICKET:-?}\` · ${PROJECT:-?}

*${TITLE:-Decision needed}*
${WHAT}
${REC:+
*Recommendation:* ${REC}}${PR:+
<${PR}|Open the PR>}

${CONSEQUENCE}

Reply \`approve ${TICKET}\`, \`reject ${TICKET}\`, or \`changed ${TICKET}: what to change\`."
