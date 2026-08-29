#!/bin/sh
# autostart.sh [--apply|--remove] — start the Control Center when you log in.
#
#   sh control-center/autostart.sh            dry run: print what would change
#   sh control-center/autostart.sh --apply    register it, and start it now
#   sh control-center/autostart.sh --remove   unregister it (leaves a running
#                                             server alone — it only removes the
#                                             wiring that starts the next one)
#
# ONE job, not a schedule: `start.sh --no-open`, held open for the whole login
# session. The Control Center is a server, so unlike the engineering
# department's jobs there is nothing periodic here — the only event is "you
# logged in".
#
# -- Why login and not boot ------------------------------------------------
# It binds 127.0.0.1 and is reached from a browser on this desktop, so it is
# useless before somebody is signed in, and both hosts have a login-time hook
# that needs neither a stored password nor an elevation prompt (Task
# Scheduler's LogonTrigger + InteractiveToken; launchd's per-user LaunchAgent).
# A true boot-time service would buy nothing and cost both of those.
#
# -- Both hosts in one file, unlike lib/eng-schedule{,-win}.sh --------------
# That pair is split because the two schedulers shared a job LIST and nothing
# else. Here they share the whole job — same runner, same argument, same log
# file, same restart rule — and differ only in how it is spelled, ~25 lines
# each. Splitting it would separate two halves that have to be read together.
#
# -- Restart rule ----------------------------------------------------------
# Restart on a CRASH, never on a clean exit — both hosts, deliberately.
# start.sh exits 0 when something is already listening on :7777, and Ctrl-C in
# a foreground server also exits 0; neither should be fought by a supervisor
# respawning it in a loop. A traceback out of serve_forever() exits non-zero,
# and that is worth restarting.
set -eu

CC="$(CDPATH= cd -P -- "$(dirname -- "$0")" && pwd -P)"
ROOT="$(CDPATH= cd -P -- "$CC/.." && pwd -P)"
START="$CC/start.sh"
LOG_DIR="$ROOT/logs"
LOG="$LOG_DIR/control-center.log"
PORT=7777

APPLY=0; REMOVE=0
case "${1:-}" in
  --apply)  APPLY=1 ;;
  --remove) REMOVE=1 ;;
  "")       : ;;
  *) echo "usage: autostart.sh [--apply|--remove]" >&2; exit 2 ;;
esac

case "$(uname -s)" in
  Darwin)               HOST_KIND=mac ;;
  MINGW*|MSYS*|CYGWIN*) HOST_KIND=windows ;;
  *)                    HOST_KIND=other ;;
esac

if [ "$HOST_KIND" = other ]; then
  # Same rule as lib/eng-schedule.sh's unknown-host branch: say out loud that
  # nothing was installed rather than exit silently, and hand over the line
  # that does it by hand. Exit 0 — this is not a broken repo, just a host with
  # no login hook this script knows.
  echo "autostart: no login hook known for $(uname -s) — nothing installed." >&2
  echo "autostart: wire it into this host's session startup by hand:" >&2
  echo "  /bin/sh $START --no-open >> $LOG 2>&1 &" >&2
  exit 0
fi

mkdir -p "$LOG_DIR"

# -- macOS: a per-user LaunchAgent ------------------------------------------
if [ "$HOST_KIND" = mac ]; then
  AGENTS="$HOME/Library/LaunchAgents"
  LABEL="com.businessos.control-center"
  PLIST="$AGENTS/$LABEL.plist"

  if [ "$REMOVE" -eq 1 ]; then
    launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
    rm -f "$PLIST"
    echo "  removed $LABEL"
    exit 0
  fi

  # RunAtLoad is what makes this a login job: a LaunchAgent is bootstrapped
  # into the GUI session at login, so "run at load" IS "run at login" — there
  # is no calendar or watch trigger here at all.
  #
  # life-os ships its own com.lifeos.control-center; this is a different label
  # for a different repo's server and the two leave each other alone. They
  # cannot both hold :7777 though — whichever loses says so and exits 0.
  plist() {
    cat <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>$LABEL</string>
	<key>ProgramArguments</key>
	<array>
		<string>/bin/sh</string>
		<string>$START</string>
		<string>--no-open</string>
	</array>
	<key>RunAtLoad</key>
	<true/>
	<key>KeepAlive</key>
	<dict>
		<key>SuccessfulExit</key>
		<false/>
	</dict>
	<key>ThrottleInterval</key>
	<integer>30</integer>
	<key>StandardOutPath</key>
	<string>$LOG</string>
	<key>StandardErrorPath</key>
	<string>$LOG</string>
</dict>
</plist>
PLIST
  }

  _new="$(plist)"
  if [ "$APPLY" -eq 0 ]; then
    if [ -f "$PLIST" ] && [ "$_new" = "$(cat "$PLIST")" ]; then
      echo "  $LABEL — unchanged"
    else
      echo "  $LABEL — would $([ -f "$PLIST" ] && echo update || echo create) $PLIST"
    fi
    echo
    echo "Dry run — nothing written. Re-run with --apply."
    exit 0
  fi

  mkdir -p "$AGENTS"
  printf '%s\n' "$_new" > "$PLIST"
  # bootout then bootstrap, same reason as lib/eng-schedule.sh: `load -w` on an
  # already-loaded job is a no-op. bootstrap is also what starts it now.
  launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$PLIST"
  echo "  $LABEL — written and loaded"
  echo
  echo "Now running -> http://localhost:$PORT   (log: $LOG)"
  echo "Stop the current one:  launchctl kill TERM gui/$(id -u)/$LABEL"
  exit 0
fi

# -- Windows: a Task Scheduler job with a logon trigger ---------------------
# Everything below mirrors lib/eng-schedule-win.sh, which carries the long-form
# reasoning for each of these decisions; only what is DIFFERENT here is
# re-explained. The shared parts, one line each:
#   schtasks_        MSYS rewrites /Create into a path, so conversion is off
#   Git\bin\bash.exe the launcher, not usr\bin\sh.exe, and -l for the MSYS PATH
#   cygpath -m       mixed paths, because these land inside a quoted shell string
#   UTF-16LE + BOM   schtasks /XML rejects bytes that disagree with the decl
#   < /dev/null      a scheduled task's stdin is not a terminal and not closed
schtasks_() { MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*' schtasks "$@"; }

FOLDER='\business-os'
TN="$FOLDER\\control-center"

if [ "$REMOVE" -eq 1 ]; then
  if schtasks_ /Delete /TN "$TN" /F >/dev/null 2>&1; then
    echo "  removed $TN"
  else
    echo "  $TN — not present"
  fi
  exit 0
fi

_git_root_m="$(cygpath -m / 2>/dev/null || echo /)"
LAUNCH_SH="${_git_root_m%/}/bin/bash.exe"
if [ ! -x "$LAUNCH_SH" ]; then
  echo "autostart: FATAL — no login-shell launcher at $LAUNCH_SH." >&2
  echo "autostart: expected Git for Windows' bin\\bash.exe. Is this Git Bash?" >&2
  exit 1
fi
SH_WIN="$(cygpath -w "$LAUNCH_SH")"
start_m="$(cygpath -m "$START")"
log_m="$(cygpath -m "$LOG")"

TASK_USER="${USERDOMAIN:-$COMPUTERNAME}\\${USERNAME}"
ARGS="-l -c \"exec '$start_m' --no-open < /dev/null >> '$log_m' 2>&1\""

xml_escape() { sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g'; }

task_xml() {
  cat <<XML
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>business-os Control Center — http://localhost:$PORT, started at logon (control-center/autostart.sh)</Description>
    <Author>business-os control-center</Author>
  </RegistrationInfo>
  <Triggers>
    <!-- Scoped to this user, not "any user": the server reads this repo's .env
         and writes into this checkout, so it belongs to the account that owns
         them. Delay PT30S keeps it out of the logon rush — nobody is looking
         at :7777 half a minute after signing in, and the shell PATH, the
         network stack and the desktop all settle first. -->
    <LogonTrigger>
      <Enabled>true</Enabled>
      <UserId>$(printf '%s' "$TASK_USER" | xml_escape)</UserId>
      <Delay>PT30S</Delay>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>$(printf '%s' "$TASK_USER" | xml_escape)</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <!-- PT0S is Task Scheduler's spelling of "no limit". The default is 72
         hours, which for a server is not a safety valve but a scheduled
         outage three days into every uptime streak. -->
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <!-- Only fires on a non-zero exit; see the restart rule in the header. -->
    <RestartOnFailure>
      <Interval>PT1M</Interval>
      <Count>3</Count>
    </RestartOnFailure>
    <Priority>5</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>$(printf '%s' "$SH_WIN" | xml_escape)</Command>
      <Arguments>$(printf '%s' "$ARGS" | xml_escape)</Arguments>
    </Exec>
  </Actions>
</Task>
XML
}

echo "Control Center autostart — Windows Task Scheduler ($([ "$APPLY" -eq 1 ] && echo APPLY || echo "dry run"))"
echo "  runs: $start_m --no-open"
echo "  log:  $log_m"
echo

if [ "$APPLY" -eq 0 ]; then
  if schtasks_ /Query /TN "$TN" >/dev/null 2>&1; then
    echo "  $TN — present, would re-register"
  else
    echo "  $TN — would create"
  fi
  echo
  echo "Dry run — nothing written. Re-run with --apply."
  exit 0
fi

_f="$(mktemp)"
if command -v iconv >/dev/null 2>&1; then
  task_xml | iconv -f UTF-8 -t UTF-16LE > "$_f.x"
  printf '\377\376' > "$_f"
  cat "$_f.x" >> "$_f"
  rm -f "$_f.x"
else
  task_xml | sed 's/encoding="UTF-16"/encoding="UTF-8"/' > "$_f"
fi

if schtasks_ /Create /TN "$TN" /XML "$(cygpath -w "$_f")" /F >/dev/null 2>&1; then
  echo "  $TN — registered"
  rm -f "$_f"
else
  echo "  $TN — FAILED to register. The XML is kept at $_f; reproduce with:" >&2
  echo "      schtasks /Create /TN \"$TN\" /XML \"$(cygpath -w "$_f")\" /F" >&2
  exit 1
fi

# Start it now rather than making the next login the first run. Whether one is
# already listening is start.sh's question, not this script's — it answers it
# the same way on every host, and says so and exits 0 when the answer is yes.
if schtasks_ /Run /TN "$TN" >/dev/null 2>&1; then
  echo "  $TN — started now"
else
  echo "  $TN — registered, but /Run failed; it will still fire at next logon" >&2
fi

echo
echo "Now running -> http://localhost:$PORT   (log: $log_m)"
echo "It starts at $TASK_USER's next logon too, and runs only while that user is"
echo "logged on (LogonType InteractiveToken — same as the engineering tasks)."
echo "Inspect it:  schtasks /Query /TN '$TN' /V /FO LIST"
echo "Stop it:     schtasks /End /TN '$TN'"
