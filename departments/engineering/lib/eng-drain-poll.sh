#!/bin/sh
# eng-drain-poll.sh — fire eng-trigger.sh for any instance whose pending
# queue is stuck, so a failed pass doesn't sit until the next natural trigger.
#
# The gap this closes: eng-loop (4x/day) and eng-watch (filesystem event on
# Mac, 5-min poll on Windows) are the only two things that ever fire
# eng-trigger.sh. A pass that STARTS and then fails mid-session (an
# expired/rotated CLI login, a transient API error) requeues its event and
# stops — see handle_failed_pass in eng-trigger.sh — but nothing schedules a
# prompt retry. The event just sits in traces/.pending until whichever of the
# two triggers above happens to fire next, which can be hours away (eng-loop's
# gaps are up to ~6h; eng-watch on Mac needs a NEW inbox write to fire at all,
# and even then, its own fingerprint short-circuit at eng-trigger.sh:488 can
# skip past an unrelated stuck backlog without draining it — same gap on
# Windows' 5-min watch poll, not just Mac's instant one). Confirmed live
# 2026-09-02: an OAuth failure at 21:36 left 2 events queued with nothing
# firing again until the 02:00 safety net, ~4h later.
#
# Cheap by construction, same reasoning eng-schedule-win.sh gives for its
# 5-min watch poll: this checks `traces/.pending` per instance (one `test -s`,
# no claude session, no hop) and only invokes eng-trigger.sh — which is where
# a real session and a hop can actually be spent — for an instance that has
# something genuinely stuck. Fired as `scheduled auto-drain` rather than
# `watch`, deliberately: `watch`'s fingerprint check at eng-trigger.sh:488 can
# itself exit 0 before ever reaching the drain loop, which is exactly the
# failure to route around here. `scheduled` has no such gate, so it always
# reaches the drain loop and processes the queue oldest-first.
#
# IDLE CHECK, added 2026-09-02 after this fired straight into a pass that was
# already running: eng-trigger.sh has no "just check, don't act" mode — invoke
# it while another pass holds traces/.loop.lock and it doesn't no-op, it calls
# queue_append and exits (eng-trigger.sh:1586-1590), adding ANOTHER entry to
# .pending. That entry isn't free — the drain loop charges a real hop and
# launches a real claude session for every entry it pops (eng-trigger.sh:1643-
# 1670), so firing into a live pass was spending real sessions on pure no-ops,
# the opposite of "cheap by construction" above. Caught live: a running manual
# drain (pid 32803) had a needless `auto-drain` entry appended behind it by
# this poller's own 5-min tick.
#
# The actual point of this poller is "nothing is running AND something is
# stuck" — not "something is queued," full stop. A pass already in flight
# will drain everything currently in .pending itself (drain_next loops until
# the queue is empty, in-process, before that pass exits) — piling another
# event on top of an active drain achieves nothing a stuck-detector should be
# doing. So: skip an instance outright if its lock is held by a still-live
# PID. Only fire when the lock is absent, or present but its owner is
# actually gone (eng-trigger.sh's own acquire() would steal it as stale
# anyway) — that is what "idle" means here.
#
# IDLE POLL, added 2026-09-07 at the approver's direction ("always busy, 24
# hours"). The drain above only fires when something is QUEUED. It cannot see
# the other way the department stops: a pass that ends with `chained: none`
# for a reason that turns out to be wrong, leaving a ticket mid-build with
# nothing queued and nothing due until the next calendar sweep — up to ~6h.
# Confirmed live 2026-09-07: the ENG-044 pass parked its PR on the approver,
# read its dependents as "wait for verified", did not chain, and the machine
# sat from 04:02 until 09:30 with ENG-026 in `building` and three tickets
# `ready`. The second loop below is the deterministic floor under that
# judgement: no live pass, nothing queued, and the board still shows a
# ticket in the machine's range → fire `continue` for it (mid-work first,
# lowest id first); nothing in range but a startable To-do ticket → fire a
# `scheduled` sweep so the eng-manager picks with judgement. At most one such
# fire per 30 minutes per instance (traces/.idle-fired), so a pass that
# keeps declining to chain costs at most two extra sessions an hour, and the
# daily hop budget in eng-trigger.sh stays the hard cap. It reads only
# frontmatter — no claude session, no hop — same "cheap by construction" as
# the drain. Quiet mode is honoured where it always was: eng-trigger.sh
# exits under MODE=sabbath|retreat|quiet before spending anything.
set -u

DEPT="$(CDPATH= cd -P -- "$(dirname -- "$0")/.." && pwd -P)"
BUSINESS_OS_ROOT="$(CDPATH= cd -P -- "$DEPT/../.." && pwd -P)"
SHELL_BIN="$([ -x /bin/zsh ] && echo /bin/zsh || echo /bin/sh)"

LOG="$BUSINESS_OS_ROOT/logs/eng-drain-poll-$(date '+%Y-%m-%d').log"
mkdir -p "$(dirname "$LOG")" 2>/dev/null || true
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

for eng in "$BUSINESS_OS_ROOT"/instances/*/engineering; do
  [ -d "$eng" ] || continue
  [ -f "$eng/config/instantiated-from" ] || continue
  business="$(basename "$(dirname "$eng")")"
  pending="$eng/traces/.pending"
  [ -s "$pending" ] || continue

  # Idle check — see header comment. A live-owned lock means a pass is
  # already draining this exact queue right now; firing into it would only
  # append another entry for it to pop (a real hop, a real session) instead
  # of skipping a genuinely idle instance the way this poller is meant to.
  lock="$eng/traces/.loop.lock"
  if [ -d "$lock" ]; then
    owner="$(cat "$lock/pid" 2>/dev/null || echo "")"
    if [ -n "$owner" ] && kill -0 "$owner" 2>/dev/null; then
      log "$business — traces/.pending non-empty but lock held by live pid $owner, skipping (already draining)"
      continue
    fi
  fi

  log "$business — traces/.pending non-empty and idle, firing 'scheduled auto-drain'"
  (
    ENG_INSTANCE="$eng" "$SHELL_BIN" "$DEPT/lib/eng-trigger.sh" scheduled auto-drain
    log "$business — trigger exited $?"
  ) &
done
wait

# ── Idle poll — see IDLE POLL in the header ──────────────────────────────
for eng in "$BUSINESS_OS_ROOT"/instances/*/engineering; do
  [ -d "$eng" ] || continue
  [ -f "$eng/config/instantiated-from" ] || continue
  business="$(basename "$(dirname "$eng")")"
  [ -s "$eng/traces/.pending" ] && continue          # the drain above owns a queued instance
  lock="$eng/traces/.loop.lock"
  if [ -d "$lock" ]; then
    owner="$(cat "$lock/pid" 2>/dev/null || echo "")"
    [ -n "$owner" ] && kill -0 "$owner" 2>/dev/null && continue   # a pass is running
  fi
  stamp="$eng/traces/.idle-fired"
  [ -f "$stamp" ] && [ -n "$(find "$stamp" -mmin -30 2>/dev/null)" ] && continue
  board="$eng/agents/eng-manager/board"
  [ -d "$board" ] || continue

  # One line per ticket: "<rank> <id>" for the machine's range, "todo <id>" for
  # a startable To-do ticket. Frontmatter only (stops at the closing ---).
  scan="$(awk '
    FNR == 1 { id = ""; st = ""; pr = ""; fm = 0 }
    /^---[[:space:]]*$/ { fm++; if (fm == 2) { emit(); nextfile } ; next }
    fm == 1 && /^id:/       { id = $2 }
    fm == 1 && /^state:/    { st = $2 }
    fm == 1 && /^priority:/ { pr = $2 }
    function emit() {
      if (id == "" || pr == "hold") return
      if      (st == "building")      print "0 " id
      else if (st == "in-review")     print "1 " id
      else if (st == "in-qa")         print "2 " id
      else if (st == "in-security")   print "3 " id
      else if (st == "ready-to-ship") print "4 " id
      else if (st == "ready")         print "5 " id
      else if (st == "intake" || st == "shaped" || st == "designed") print "todo " id
    }' "$board"/[A-Z]*-[0-9]*.md 2>/dev/null | sort)"

  pick="$(printf '%s\n' "$scan" | grep -E '^[0-9] ' | head -1 | cut -d' ' -f2)"
  if [ -n "$pick" ]; then
    touch "$stamp"
    log "$business — idle with $pick in the machine's range and nothing queued, firing 'continue $pick'"
    (
      ENG_INSTANCE="$eng" "$SHELL_BIN" "$DEPT/lib/eng-trigger.sh" continue "$pick"
      log "$business — trigger exited $?"
    ) &
  elif printf '%s\n' "$scan" | grep -q '^todo '; then
    touch "$stamp"
    log "$business — idle with nothing in the machine's range but To-do work on the board, firing 'scheduled auto-idle'"
    (
      ENG_INSTANCE="$eng" "$SHELL_BIN" "$DEPT/lib/eng-trigger.sh" scheduled auto-idle
      log "$business — trigger exited $?"
    ) &
  fi
done
wait
