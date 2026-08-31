#!/bin/sh
# Business OS Control Center — standalone, no life-os dependency.
# Binds to 127.0.0.1 by default and is gated by email+PIN (server.py,
# CONTROL_CENTER_USERS in .env). Run this directly on whichever desktop you
# want the command center on; see cloudflare-tunnel.sh to also reach it from
# the internet.
#
#   sh start.sh              start it and open the browser at it
#   sh start.sh --no-open    start it and leave the browser alone
#
# --no-open exists for autostart.sh: a server started at login has nobody
# watching yet, and a browser tab that opens itself on every single login is a
# nuisance rather than a convenience. Nothing else about the two paths differs.
#
# /bin/sh, not /bin/zsh: there is no zsh on a Windows host, and nothing in here
# needed zsh. The three things that WERE mac-only — lsof, open, and a bare
# `python3` — each get a host-appropriate branch below rather than a rewrite.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT=6666

OPEN_BROWSER=1
case "${1:-}" in
  --no-open) OPEN_BROWSER=0 ;;
  "")        : ;;
  *) echo "usage: start.sh [--no-open]" >&2; exit 2 ;;
esac

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
  [ "$OPEN_BROWSER" -eq 1 ] && open_url "http://localhost:$PORT"
  exit 0
fi

echo "Starting Business OS Control Center..."
if [ "$OPEN_BROWSER" -eq 1 ]; then
  open_url "http://localhost:$PORT" &
  sleep 1
fi
# -u because autostart.sh redirects this into a log file: python block-buffers
# stdout when it is not a terminal, so an unbuffered server is the difference
# between a log you can tail and one that stays empty until the process dies.
#
# -X utf8 because Windows python defaults its I/O encoding to the ANSI codepage
# (cp1252 here), not UTF-8. Two things break under that, and the first one is
# how it was found: redirected into a log file, the startup banner's arrow died
# with UnicodeEncodeError before serve_forever() was ever reached, so the task
# bound the port and then exited. The second is worse and quieter — server.py
# reads and writes the board, the inboxes and the leads with bare read_text()/
# write_text(), which take that same codepage, and every one of those files is
# UTF-8 markdown full of em-dashes. PEP 540 UTF-8 mode fixes both at the
# interpreter rather than at twenty call sites, and is a no-op on mac/Linux,
# where UTF-8 is already the default.
exec "$PY" -X utf8 -u "$ROOT/control-center/server.py"
