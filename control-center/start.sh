#!/bin/sh
# Business OS Control Center — standalone, no life-os dependency.
# Local-only: binds to 127.0.0.1, no passcode gate, no tunnel. Run this
# directly on whichever desktop you want the command center on.
#
# /bin/sh, not /bin/zsh: there is no zsh on a Windows host, and nothing in here
# needed zsh. The three things that WERE mac-only — lsof, open, and a bare
# `python3` — each get a host-appropriate branch below rather than a rewrite.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT=7777

case "$(uname -s)" in
  Darwin)               HOST_KIND=mac ;;
  MINGW*|MSYS*|CYGWIN*) HOST_KIND=windows ;;
  *)                    HOST_KIND=other ;;
esac

# Open a URL in the desktop browser.
open_url() {
  case "$HOST_KIND" in
    mac)     open "$1" ;;
    # `start` is a cmd builtin, not a program, so it needs cmd to run it. The
    # empty "" is cmd's window-title argument: without it, start treats a quoted
    # URL as the title and opens nothing.
    windows) cmd //c start "" "$1" >/dev/null 2>&1 ;;
    *)       xdg-open "$1" >/dev/null 2>&1 || true ;;
  esac
}

# Is something already listening on $PORT? lsof is not present on Windows and is
# not guaranteed on a minimal Linux, so each host is asked the way it answers.
port_in_use() {
  case "$HOST_KIND" in
    windows) netstat -ano 2>/dev/null | grep -q "LISTENING" \
             && netstat -ano 2>/dev/null | grep -qE "[:.]$PORT[[:space:]].*LISTENING" ;;
    *)       if command -v lsof >/dev/null 2>&1; then
               lsof -ti ":$PORT" >/dev/null 2>&1
             else
               netstat -an 2>/dev/null | grep -qE "[:.]$PORT[[:space:]].*LISTEN"
             fi ;;
  esac
}

# `python3` is a Microsoft Store redirector on a stock Windows — it exits 49
# instead of running anything — so the interpreter is resolved by EXECUTING a
# candidate rather than by finding one on PATH. Same rule, and same reason, as
# departments/engineering/lib/eng-env.sh.
PY=""
for c in python3 python python3.exe python.exe; do
  p="$(command -v "$c" 2>/dev/null)" || continue
  if "$p" -c 'import sys' >/dev/null 2>&1; then PY="$p"; break; fi
done
if [ -z "$PY" ] && command -v py >/dev/null 2>&1; then
  p="$(py -3 -c 'import sys; print(sys.executable)' 2>/dev/null)"
  if [ -n "$p" ] && "$p" -c 'import sys' >/dev/null 2>&1; then PY="$p"; fi
fi
if [ -z "$PY" ]; then
  echo "No working python3 found. Install Python 3 and re-run." >&2
  exit 1
fi

if port_in_use; then
  echo "Control Center already running → http://localhost:$PORT"
  echo "Edited server.py? Kill the process on :$PORT and re-run this script."
  open_url "http://localhost:$PORT"
  exit 0
fi

echo "Starting Business OS Control Center..."
open_url "http://localhost:$PORT" &
sleep 1
exec "$PY" "$ROOT/control-center/server.py"
