#!/bin/zsh
# Business OS Control Center — standalone, no life-os dependency.
# Local-only: binds to 127.0.0.1, no passcode gate, no tunnel. Run this
# directly on whichever desktop you want the command center on.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT=7777

if lsof -ti :$PORT >/dev/null 2>&1; then
  echo "Control Center already running → http://localhost:$PORT"
  echo "Edited server.py? Kill the process on :$PORT and re-run this script."
  open "http://localhost:$PORT"
  exit 0
fi

echo "Starting Business OS Control Center..."
open "http://localhost:$PORT" &
sleep 0.5
python3 "$ROOT/control-center/server.py"
