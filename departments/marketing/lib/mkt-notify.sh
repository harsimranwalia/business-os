#!/usr/bin/env bash
# mkt-notify.sh — tell the approver a piece is waiting, so it never just sits there.
#
# The department can do everything else on its own. M2 needs a human on every
# single piece, which makes this the highest-frequency human gate anywhere in
# business-os — and that is exactly why the restraint below matters more here
# than it does in engineering. Writing a piece to content/ready-to-send/ and
# hoping someone looks is not a mechanism; it is a dead end with extra steps.
# This is the thing that advances it.
#
# Posts via SLACK_WEBHOOK_URL. No new connection, no new cost. The channel is
# the instance's choice — the department only calls this script, per
# config/conventions.yaml -> notify.
#
# ── The restraint, and where it actually lives ─────────────────────────────
#
# M2 recurs — every piece, forever. A channel running three a week is several
# hundred notifications a year for one person, and the predictable end of that
# is that they stop being read, at which point the gate exists on paper and
# not in fact. So the restraint is real, but it is NOT "notify less than once
# per piece". One notification per piece is the mechanism; a piece nobody was
# told about is a piece that sits.
#
# The restraint is three narrower rules:
#
#   * ONE message per piece, ever. content-reviewer updates an existing M2
#     item rather than raising a second — a second ping for the same piece is
#     what teaches someone to skim.
#   * NO nudges. A piece still waiting is already in the next digest.
#   * NOTHING when there is nothing. A message that says "no action needed"
#     spends the same attention as one that matters.
#
# Modes:
#
#   raise <path>     one piece has reached M2 and needs a decision
#   shipped <path>   one piece went live — a state change worth knowing, and
#                    the receipt that the loop actually closed
#   batch            digest of everything still awaiting M2, for a sweep
#   stall            the approval cap is reached — the queue has stopped
#
# Every <path> is INSTANCE-RELATIVE (`content/shipped/x.md`, `inbox/y.md`),
# because that is what the skills have in hand and an absolute path would make
# them care which machine they are on. An absolute path still works.
#
# Usage:
#   mkt-notify.sh raise   inbox/2026-09-01-pov-thing.md
#   mkt-notify.sh shipped content/shipped/2026-09-01-pov-thing.md
#   mkt-notify.sh batch
#   mkt-notify.sh stall

set -uo pipefail

MODE_ARG="${1:?mode required}"
ITEM="${2:-}"

. "$(dirname "$0")/mkt-env.sh" || exit 1

READY="$MKT_CONTENT/ready-to-send"
LOG="$MKT_TRACES/mkt-notify-$(date '+%Y-%m-%d').log"
mkdir -p "$MKT_TRACES"

if [ -z "${SLACK_WEBHOOK_URL:-}" ]; then
  echo "[$(date '+%H:%M:%S')] SLACK_WEBHOOK_URL unset — cannot notify" >> "$LOG"
  # Not fatal. The pieces are still in ready-to-send/ and still visible on
  # whatever approval surface the instance uses; only the push is missing.
  # Fail loud in the log, never silently, and never block a pass on a
  # notification.
  exit 0
fi

# Build the JSON with python3 rather than interpolating into a heredoc.
# Everything below comes out of a markdown file somebody wrote — one double
# quote in a title produces invalid JSON, the post is rejected, and the
# notification fails silently. Silent failure is the one outcome this script
# exists to prevent.
post() {
  python3 -c '
import json, os, sys, urllib.request
payload = json.dumps({"text": sys.argv[1]}).encode()
req = urllib.request.Request(os.environ["SLACK_WEBHOOK_URL"], data=payload,
                             headers={"Content-Type": "application/json"})
try:
    urllib.request.urlopen(req, timeout=10).read()
except Exception as e:
    print(f"post failed: {e}", file=sys.stderr)
    sys.exit(1)
' "$1" 2>> "$LOG"
  if [ $? -eq 0 ]; then
    echo "[$(date '+%H:%M:%S')] sent: $MODE_ARG ${ITEM:+$(basename "$ITEM")}" >> "$LOG"
  else
    echo "[$(date '+%H:%M:%S')] FAILED: $MODE_ARG ${ITEM:+$(basename "$ITEM")} — piece still in ready-to-send/" >> "$LOG"
  fi
}

fm() { grep -m1 "^$2:" "$1" 2>/dev/null | sed "s/^$2:[[:space:]]*//"; }

# Skills hand over instance-relative paths. Resolve here rather than making
# every caller build an absolute one — a skill that has to know its own
# absolute location has stopped being portable.
if [ -n "$ITEM" ] && [ ! -f "$ITEM" ] && [ -f "$MKT_INSTANCE/$ITEM" ]; then
  ITEM="$MKT_INSTANCE/$ITEM"
fi

# A piece awaits M2 when its frontmatter status is not yet `approved` and not
# `needs_attention`. The FIELD decides, never the folder — same rule the ship
# skills follow, and they must not be able to disagree with this script about
# what is waiting.
awaiting() {
  for f in "$READY"/*.md; do
    [ -f "$f" ] || continue
    st="$(fm "$f" status)"
    case "$st" in
      approved|shipped|needs_attention) continue ;;
    esac
    echo "$f"
  done
}

CAP="$(sed -n 's/^[[:space:]]*awaiting_approval_cap:[[:space:]]*\([0-9]*\).*/\1/p' \
      "$MKT_INSTANCE/config/config.yaml" 2>/dev/null | head -1)"
[ -n "$CAP" ] || CAP=5

if [ "$MODE_ARG" = "stall" ]; then
  post ":octagonal_sign: *Marketing — the queue is full*

All $CAP approval slots are used, so nothing new is being written until one clears. Nothing is broken; it is waiting on you.

Approve or reject anything in the queue and drafting resumes."
  exit 0
fi

if [ "$MODE_ARG" = "batch" ]; then
  N=0; LINES=""
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    N=$(( N + 1 ))
    CH="$(fm "$f" channel)"; [ -n "$CH" ] || CH="?"
    DATE="$(basename "$f" .md | cut -c1-10)"
    TITLE="$(grep -m1 '^# ' "$f" 2>/dev/null | sed 's/^# //')"
    [ -n "$TITLE" ] || TITLE="$(basename "$f" .md)"
    LINES="${LINES}
• \`${CH}\` ${DATE} — ${TITLE}"
  done <<EOF
$(awaiting)
EOF

  # Nothing waiting is not a message. A notification that fires to say there is
  # nothing to do trains the reader to skim the ones that matter.
  if [ "$N" -eq 0 ]; then
    echo "[$(date '+%H:%M:%S')] batch: nothing awaiting — no message sent" >> "$LOG"
    exit 0
  fi

  # The most useful line is what happens if they do nothing. Without it every
  # notification reads as equally urgent, which is how a system starts
  # manufacturing urgency out of its own routine.
  if [ "$N" -ge "$CAP" ]; then
    CONSEQUENCE="*The queue is full* — $N of $CAP slots used. Nothing new is being written until you clear one."
  else
    CONSEQUENCE="If you do nothing: these wait, and each one's publishing slot passes quietly. $N of $CAP slots used."
  fi

  post ":memo: *Marketing — $N piece$([ "$N" -eq 1 ] || echo s) waiting on you*
${LINES}

${CONSEQUENCE}"
  exit 0
fi

# ── raise / shipped: one named piece ───────────────────────────────────────
# A missing file is logged and exits 0, never non-zero: a notification must
# not be able to fail a publishing run that already succeeded.
[ -f "$ITEM" ] || { echo "[$(date '+%H:%M:%S')] no such item: $ITEM" >> "$LOG"; exit 0; }

CH="$(fm "$ITEM" channel)"; [ -n "$CH" ] || CH="?"
TITLE="$(grep -m1 '^# ' "$ITEM" 2>/dev/null | sed 's/^# //')"
[ -n "$TITLE" ] || TITLE="$(basename "$ITEM" .md)"

if [ "$MODE_ARG" = "shipped" ]; then
  URL="$(fm "$ITEM" post_url)"
  VERIFIED="$(fm "$ITEM" publish_verified)"
  # The verification state is on the message, not just in the trace. A publish
  # that could not be read back is a different fact from one that was, and the
  # difference matters most at exactly the moment nobody is looking at logs.
  case "$VERIFIED" in
    ''|*confirmed*|true) NOTE="" ;;
    *) NOTE="
_Published, but read-back said \`${VERIFIED}\` — worth an eye._" ;;
  esac
  post ":rocket: *Marketing — shipped* · \`${CH}\`

*${TITLE}*${URL:+
<${URL}|See it live>}${NOTE}"
  exit 0
fi

# raise — a piece has reached M2.
N=0
while IFS= read -r f; do [ -n "$f" ] && N=$(( N + 1 )); done <<EOF
$(awaiting)
EOF
if [ "$N" -ge "$CAP" ]; then
  CONSEQUENCE="*The queue is full* — $N of $CAP slots used. Nothing new is being written until you clear one."
else
  CONSEQUENCE="If you do nothing: it waits, and its publishing slot passes quietly. $N of $CAP waiting on you."
fi
WHY="$(fm "$ITEM" raised_because)"

post ":memo: *Marketing — ready for you* · \`${CH}\`

*${TITLE}*${WHY:+
${WHY}}

${CONSEQUENCE}"
