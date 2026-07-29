#!/usr/bin/env bash
#
# install_cron.sh — installs (idempotently) all cron entries for the
# business-os reddit pipeline. Re-running replaces the managed block,
# never duplicates it and never touches your other cron entries.
#
# Architecture note: the agent is cron-INVOKED, not a persistent loop.
# Every run is stateless — state lives in the CRM, memory/, and inbox/ —
# so a crash costs nothing and context never accumulates across hours.
# The deterministic scripts (listener, notify, poll, poster) run on
# tight cycles with no LLM. The agent (a Claude Code headless call)
# runs a few times daily, right after each sweep.
#
# Quiet mode (sabbath/retreat) is enforced INSIDE every component via
# MODE=sabbath|retreat|quiet in repo-root .env — cron keeps firing,
# everything exits silently.
#
# Usage:
#   ./scripts/install_cron.sh            # install / refresh
#   ./scripts/install_cron.sh --remove   # uninstall the managed block
#
# Prereqs: `claude` CLI on PATH, python3, repo-root .env populated
# (Reddit read creds, Reddit write creds, TWENTY_*, TELEGRAM_*).

set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$(command -v python3)"
CLAUDE="$(command -v claude || true)"
MARK_BEGIN="# >>> business-os reddit pipeline >>>"
MARK_END="# <<< business-os reddit pipeline <<<"
LOG_DIR="$BASE_DIR/logs/cron"
mkdir -p "$LOG_DIR"

if [[ "${1:-}" == "--remove" ]]; then
  crontab -l 2>/dev/null | sed "/^${MARK_BEGIN}$/,/^${MARK_END}$/d" | crontab -
  echo "removed managed cron block"
  exit 0
fi

if [[ -z "$CLAUDE" ]]; then
  echo "warn: 'claude' CLI not found on PATH — installing anyway;" \
       "fix PATH in the crontab line if your shell differs" >&2
  CLAUDE="claude"
fi

# The agent run: headless Claude Code, non-interactive, tools restricted.
# --allowedTools keeps the blast radius small: it can read/write the repo
# and run scripts, nothing else. Adjust model/flags to taste.
AGENT_PROMPT="Use the reddit-community-builder agent to process unprocessed sweeps in inbox/listeners/reddit/ per its run procedure, then stop."
AGENT_CMD="cd $BASE_DIR && $CLAUDE -p \"$AGENT_PROMPT\" --allowedTools \"Read,Write,Bash\" --max-turns 40"

BLOCK=$(cat <<CRON
$MARK_BEGIN
# listener sweep: 3x daily (read-only Reddit)
0 8,13,18 * * *   cd $BASE_DIR && $PYTHON scripts/reddit_listen.py >> $LOG_DIR/listen.log 2>&1
# agent triage: 30 min after each sweep (headless Claude Code)
30 8,13,18 * * *  $AGENT_CMD >> $LOG_DIR/agent.log 2>&1
# telegram: notify pending drafts + apply approve/skip/edit replies
*/10 * * * *      cd $BASE_DIR && $PYTHON scripts/content_loop.py notify >> $LOG_DIR/notify.log 2>&1
*/5 * * * *       cd $BASE_DIR && $PYTHON scripts/content_loop.py poll >> $LOG_DIR/poll.log 2>&1
# poster: applies approved records (max 1 post/run, 45m min gap internally)
*/30 * * * *      cd $BASE_DIR && $PYTHON scripts/reddit_post.py >> $LOG_DIR/post.log 2>&1
$MARK_END
CRON
)

( crontab -l 2>/dev/null | sed "/^${MARK_BEGIN}$/,/^${MARK_END}$/d"
  echo "$BLOCK" ) | crontab -

echo "installed. current managed block:"
crontab -l | sed -n "/^${MARK_BEGIN}$/,/^${MARK_END}$/p"
