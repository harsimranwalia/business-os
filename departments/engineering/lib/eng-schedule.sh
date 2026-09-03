#!/bin/sh
# eng-schedule.sh [--apply] — install/refresh the department's launchd jobs.
#
#   ./eng-schedule.sh            dry run: print what would change, write nothing
#   ./eng-schedule.sh --apply    write the plists and (re)load them
#   ./eng-schedule.sh --remove   unload and delete both jobs
#
# FOUR jobs for ALL businesses, not four per business. install.sh calls this
# on every onboard, so adding a business never means installing host wiring by
# hand.
#
#   com.businessos.eng-loop    daily 09:30 / 15:30 / 20:30 / 02:00 — the
#                              safety-net sweep. One job; lib/eng-loop-all.sh
#                              discovers instances.
#   com.businessos.eng-watch   an inbox changed outside the notify channel.
#   com.businessos.eng-report  Sundays 18:30 — schedules/eng_weekly_report.md.
#                              Not an eng-trigger.sh event; a dedicated runner,
#                              lib/eng-report.sh, discovers instances the same
#                              way the other two do. See that file's header.
#   com.businessos.eng-drain   every 5 min — retries a pass that fired and
#                              FAILED (not never-started; see
#                              handle_failed_pass in eng-trigger.sh), which
#                              neither of the two above promptly catches:
#                              eng-loop's gaps run up to ~6h, and eng-watch's
#                              own fingerprint short-circuit (eng-trigger.sh
#                              ~line 488) can skip a stuck backlog that isn't
#                              tied to a fresh inbox write. lib/eng-drain-poll.sh
#                              checks traces/.pending per instance — a bare
#                              `test -s`, no claude session — and only fires
#                              eng-trigger.sh for one that actually has
#                              something stuck. Added 2026-09-02 after an
#                              OAuth failure left 2 events queued for ~4h with
#                              nothing due to fire again until 02:00.
#
# Why the watch job is regenerated and the loop job is not: launchd's WatchPaths
# is a STATIC array. It cannot glob, and it is not recursive — watching
# instances/ would not see instances/x/engineering/inbox/. So the array has to
# name every instance's three inboxes, which means rewriting it whenever a
# business is onboarded. The loop job takes no per-instance argument at all, so
# it is written once and never needs to change.
#
# launchd cannot say WHICH watched path changed, so the watch job sweeps every
# instance and each pass decides for itself whether it has work. That is the
# same shape as the scheduled sweep, with a different event name.
#
# life-os's own com.lifeos.eng-{loop,watch} are separate jobs under a different
# label and are left alone — life-os is not a business-os instance.
set -eu

DEPT="$(CDPATH= cd -P -- "$(dirname -- "$0")/.." && pwd -P)"
BUSINESS_OS="$(CDPATH= cd -P -- "$DEPT/../.." && pwd -P)"
AGENTS="$HOME/Library/LaunchAgents"
RUNNER="$DEPT/lib/eng-loop-all.sh"

# Host dispatch. Everything below this line is launchd, which exists only on
# macOS. The Windows equivalent is Task Scheduler and lives in its own file
# rather than as branches threaded through this one: the two schedulers share a
# job LIST and nothing else — no plists, no launchctl, a different idempotency
# story and a poll where this has a filesystem watch — so interleaving them
# would make both harder to read than either is alone.
#
# Dispatched here rather than at every caller so install.sh and lib/eng-setup.sh
# keep calling the one name they have always called.
case "$(uname -s)" in
  Darwin) : ;;
  MINGW*|MSYS*|CYGWIN*) exec /bin/sh "$DEPT/lib/eng-schedule-win.sh" "$@" ;;
  *)
    # Linux/container: no wiring is generated, and that is said out loud. A
    # scheduler that silently installs nothing is indistinguishable from one
    # that installed something broken. Exit 0, not 1 — install.sh calls this on
    # every onboard, and an unschedulable host must not fail the onboard.
    echo "eng-schedule: no scheduler wiring for $(uname -s) — no jobs installed." >&2
    echo "eng-schedule: wire lib/eng-loop-all.sh into cron by hand on this host:" >&2
    echo "  30 2,9,15,20 * * *  /bin/sh $DEPT/lib/eng-loop-all.sh scheduled cron" >&2
    exit 0 ;;
esac

MODE_ARG="${1:-}"
APPLY=0; REMOVE=0
case "$MODE_ARG" in
  --apply)  APPLY=1 ;;
  --remove) REMOVE=1 ;;
  "")       : ;;
  *) echo "usage: eng-schedule.sh [--apply|--remove]" >&2; exit 2 ;;
esac

LOOP_LABEL="com.businessos.eng-loop"
WATCH_LABEL="com.businessos.eng-watch"
REPORT_LABEL="com.businessos.eng-report"
DRAIN_LABEL="com.businessos.eng-drain"
LOOP_PLIST="$AGENTS/$LOOP_LABEL.plist"
WATCH_PLIST="$AGENTS/$WATCH_LABEL.plist"
REPORT_PLIST="$AGENTS/$REPORT_LABEL.plist"
DRAIN_PLIST="$AGENTS/$DRAIN_LABEL.plist"
REPORT_RUNNER="$DEPT/lib/eng-report.sh"
DRAIN_RUNNER="$DEPT/lib/eng-drain-poll.sh"

if [ "$REMOVE" -eq 1 ]; then
  for l in "$LOOP_LABEL" "$WATCH_LABEL" "$REPORT_LABEL" "$DRAIN_LABEL"; do
    launchctl bootout "gui/$(id -u)/$l" 2>/dev/null || true
    rm -f "$AGENTS/$l.plist"
    echo "  removed $l"
  done
  exit 0
fi

# ── Discover instances ─────────────────────────────────────────────────────
INSTANCES=""
for eng in "$BUSINESS_OS"/instances/*/engineering; do
  [ -d "$eng" ] || continue
  [ -f "$eng/config/instantiated-from" ] || continue
  INSTANCES="$INSTANCES $eng"
done

if [ -z "$INSTANCES" ]; then
  echo "eng-schedule: no instances found under $BUSINESS_OS/instances — nothing to schedule." >&2
  exit 0
fi

echo "Engineering schedule ($([ "$APPLY" -eq 1 ] && echo APPLY || echo "dry run"))"
for eng in $INSTANCES; do echo "  instance: $(basename "$(dirname "$eng")")"; done

# ── The loop job ───────────────────────────────────────────────────────────
# Every day — 09:30, 15:30, 20:30, and 02:00. A safety net, not the engine:
# the control center and the chain fire events immediately, and this catches
# what a local event cannot see. Runs weekends too; the release window
# (config.yaml build_loop.release_window.block_weekends) is what actually
# stops a Saturday/Sunday pass from shipping, not this schedule.
loop_plist() {
  cat <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>$LOOP_LABEL</string>
	<key>ProgramArguments</key>
	<array>
		<string>/bin/sh</string>
		<string>$RUNNER</string>
		<string>scheduled</string>
		<string>launchd</string>
	</array>
	<key>RunAtLoad</key>
	<false/>
	<key>StandardOutPath</key>
	<string>/tmp/businessos-eng-loop.log</string>
	<key>StandardErrorPath</key>
	<string>/tmp/businessos-eng-loop.log</string>
	<key>StartCalendarInterval</key>
	<array>
$(for wd in 0 1 2 3 4 5 6; do for hm in 9:30 15:30 20:30 2:00; do
hr="${hm%:*}"; mn="${hm#*:}"
printf '\t\t<dict><key>Hour</key><integer>%s</integer><key>Minute</key><integer>%s</integer><key>Weekday</key><integer>%s</integer></dict>\n' "$hr" "$mn" "$wd"
done; done)
	</array>
</dict>
</plist>
PLIST
}

# ── The watch job ──────────────────────────────────────────────────────────
# ThrottleInterval 60 because launchd fires WatchPaths on ANY change inside a
# watched directory, including an agent moving a handled item into _handled/.
# eng-trigger.sh fingerprints top-level files to drop the duplicates; this just
# keeps the firing rate sane.
watch_plist() {
  cat <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>$WATCH_LABEL</string>
	<key>ProgramArguments</key>
	<array>
		<string>/bin/sh</string>
		<string>$RUNNER</string>
		<string>watch</string>
		<string>launchd</string>
	</array>
	<key>RunAtLoad</key>
	<false/>
	<key>StandardOutPath</key>
	<string>/tmp/businessos-eng-watch.log</string>
	<key>StandardErrorPath</key>
	<string>/tmp/businessos-eng-watch.log</string>
	<key>ThrottleInterval</key>
	<integer>60</integer>
	<key>WatchPaths</key>
	<array>
$(for eng in $INSTANCES; do
for sub in agents/product-manager/inbox agents/eng-manager/inbox inbox; do
printf '\t\t<string>%s/%s</string>\n' "$eng" "$sub"
done; done)
	</array>
</dict>
</plist>
PLIST
}

# ── The weekly report job ──────────────────────────────────────────────────
# Sunday 18:30 — schedules/eng_weekly_report.md's own cron expression
# (30 18 * * 0), thirty minutes ahead of the Marketing weekly run so the
# approver reads one evening's worth of reports, not seven separate pings.
#
# Not an eng-trigger.sh event (see lib/eng-report.sh's own header), so this
# points at a dedicated runner instead of $RUNNER with an event name —
# eng-trigger.sh's five-event vocabulary has no "report" case, and none of its
# per-ticket machinery (hop budget, WIP caps, chaining, retry) applies to a
# pass that touches no ticket.
report_plist() {
  cat <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>$REPORT_LABEL</string>
	<key>ProgramArguments</key>
	<array>
		<string>/bin/sh</string>
		<string>$REPORT_RUNNER</string>
	</array>
	<key>RunAtLoad</key>
	<false/>
	<key>StandardOutPath</key>
	<string>/tmp/businessos-eng-report.log</string>
	<key>StandardErrorPath</key>
	<string>/tmp/businessos-eng-report.log</string>
	<key>StartCalendarInterval</key>
	<dict>
		<key>Hour</key>
		<integer>18</integer>
		<key>Minute</key>
		<integer>30</integer>
		<key>Weekday</key>
		<integer>0</integer>
	</dict>
</dict>
</plist>
PLIST
}

# ── The drain-poll job ──────────────────────────────────────────────────────
# No event/context args, unlike loop and watch: eng-drain-poll.sh discovers
# instances and decides per-instance whether there's anything to fire, the
# same way eng-report.sh does. StartInterval, not StartCalendarInterval —
# this wants a fixed cadence starting from whenever the job loads, not
# specific clock times.
drain_plist() {
  cat <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>$DRAIN_LABEL</string>
	<key>ProgramArguments</key>
	<array>
		<string>/bin/sh</string>
		<string>$DRAIN_RUNNER</string>
	</array>
	<key>RunAtLoad</key>
	<false/>
	<key>StandardOutPath</key>
	<string>/tmp/businessos-eng-drain.log</string>
	<key>StandardErrorPath</key>
	<string>/tmp/businessos-eng-drain.log</string>
	<key>StartInterval</key>
	<integer>300</integer>
</dict>
</plist>
PLIST
}

install_one() { # install_one <label> <plist-path> <generator>
  _label="$1"; _path="$2"; _gen="$3"
  _new="$("$_gen" 2>/dev/null || $_gen)"
  if [ -f "$_path" ] && [ "$_new" = "$(cat "$_path")" ]; then
    echo "  $_label — unchanged"
    return 0
  fi
  if [ "$APPLY" -eq 0 ]; then
    echo "  $_label — would $([ -f "$_path" ] && echo update || echo create) $_path"
    return 0
  fi
  mkdir -p "$AGENTS"
  printf '%s\n' "$_new" > "$_path"
  # bootout then bootstrap: `load -w` on an already-loaded job is a no-op, which
  # would leave a regenerated WatchPaths array unread until the next logout.
  launchctl bootout "gui/$(id -u)/$_label" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$_path"
  echo "  $_label — written and loaded"
}

echo
install_one "$LOOP_LABEL"   "$LOOP_PLIST"   loop_plist
install_one "$WATCH_LABEL"  "$WATCH_PLIST"  watch_plist
install_one "$REPORT_LABEL" "$REPORT_PLIST" report_plist
install_one "$DRAIN_LABEL"  "$DRAIN_PLIST"  drain_plist

if [ "$APPLY" -eq 0 ]; then
  echo
  echo "Dry run — nothing written. Re-run with --apply."
fi
