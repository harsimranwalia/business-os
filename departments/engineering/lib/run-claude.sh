#!/bin/zsh
ulimit -n unlimited 2>/dev/null || ulimit -n 65536
unset CLAUDECODE  # allow spawning from within an existing Claude Code session
SCRIPT_DIR=${0:a:h}
source "$SCRIPT_DIR/../.env" 2>/dev/null
cd /Users/hwalia/Documents/projects/life-os
exec /Users/hwalia/.local/bin/claude --dangerously-skip-permissions "$@"
