#!/bin/sh
# eng-schedule.sh [--apply] — install/refresh the department's launchd jobs.
#
#   ./eng-schedule.sh            dry run: print what would change, write nothing
#   ./eng-schedule.sh --apply    write the plists and (re)load them
#   ./eng-schedule.sh --remove   unload and delete both jobs
#
# TWO jobs for ALL businesses, not two per business. install.sh calls this on
# every onboard, so adding a business never means installing host wiring by hand.
#
#   com.businessos.eng-loop   weekdays 09:30 / 15:30 — the safety-net sweep.
#                             One job; lib/eng-loop-all.sh discovers instances.
#   com.businessos.eng-watch  an inbox changed outside the notify channel.
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
LOOP_PLIST="$AGENTS/$LOOP_LABEL.plist"
WATCH_PLIST="$AGENTS/$WATCH_LABEL.plist"

if [ "$REMOVE" -eq 1 ]; then
  for l in "$LOOP_LABEL" "$WATCH_LABEL"; do
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
# Weekdays 09:30 and 15:30. A safety net, not the engine: the control center
# and the chain fire events immediately, and this catches what a local event
# cannot see.
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
$(for wd in 1 2 3 4 5; do for hr in 9 15; do
printf '\t\t<dict><key>Hour</key><integer>%s</integer><key>Minute</key><integer>30</integer><key>Weekday</key><integer>%s</integer></dict>\n' "$hr" "$wd"
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
install_one "$LOOP_LABEL"  "$LOOP_PLIST"  loop_plist
install_one "$WATCH_LABEL" "$WATCH_PLIST" watch_plist

if [ "$APPLY" -eq 0 ]; then
  echo
  echo "Dry run — nothing written. Re-run with --apply."
fi
