#!/bin/sh
# eng-schedule-win.sh [--apply|--remove] — the Windows half of lib/eng-schedule.sh.
#
#   ./eng-schedule-win.sh            dry run: print what would change, write nothing
#   ./eng-schedule-win.sh --apply    register / refresh the three tasks
#   ./eng-schedule-win.sh --remove   delete them
#
# Never invoked directly in normal use: lib/eng-schedule.sh dispatches here on a
# MINGW/MSYS/CYGWIN host, so install.sh and lib/eng-setup.sh keep calling the one
# name they have always called.
#
# Same THREE jobs for ALL businesses that the launchd side installs, for the same
# reason — lib/eng-loop-all.sh discovers instances, so onboarding a business
# never means touching host wiring:
#
#   business-os\eng-loop    daily 02:00 / 09:30 / 15:30 / 20:30 — safety net
#   business-os\eng-watch   an inbox changed outside the notify channel
#   business-os\eng-report  Sundays 18:30 — schedules/eng_weekly_report.md
#
# -- The one real behavioural difference, named rather than papered over -----
# launchd's WatchPaths watches the filesystem. Task Scheduler cannot: it has no
# file-change trigger of any kind. So eng-watch is a POLL — every 5 minutes,
# forever — where the Mac's is an interrupt.
#
# That is affordable only because of work eng-trigger.sh already does. Its
# watch_fingerprint() hashes the top-level files of the three watched inboxes and
# compares against .watch-seen BEFORE taking the lock and BEFORE spending a hop,
# so a fire with no new work costs one `find` and one sha1 — no claude session,
# no hop, no cost. A poll that finds nothing is genuinely almost free, and that
# check is what makes the interval a tuning knob rather than a bill.
#
# The trade that remains is latency, not money: an inbox write is noticed within
# 5 minutes here versus within seconds on the Mac. For a queue whose safety net
# is otherwise SIX HOURS away, that is the right side of the trade.
#
# -- Where Windows is BETTER than the cron this repo defaults to -------------
# schedules/eng_build_loop.md warns that plain cron silently drops anything
# scheduled while the machine was asleep, and asks for a wake-aware scheduler on
# a host that sleeps. A laptop is exactly that host. StartWhenAvailable below is
# Task Scheduler's answer, and is launchd's catch-up behaviour by another name: a
# missed 02:00 run fires when the machine next wakes instead of vanishing.
set -eu

DEPT="$(CDPATH= cd -P -- "$(dirname -- "$0")/.." && pwd -P)"
BUSINESS_OS="$(CDPATH= cd -P -- "$DEPT/../.." && pwd -P)"
RUNNER="$DEPT/lib/eng-loop-all.sh"
REPORT_RUNNER="$DEPT/lib/eng-report.sh"
LOG_DIR="$BUSINESS_OS/logs"

# schtasks is a WINDOWS program, and MSYS rewrites arguments that look like
# POSIX paths before a Windows program ever sees them. `/Create` is indeed
# shaped like an absolute path, so it arrived as "C:/Program Files/Git/Create"
# and schtasks answered:
#
#   ERROR: Invalid argument/option - 'C:/Program Files/Git/Create'.
#
# — an error that names a path nobody in this file ever wrote, and points at the
# Git install rather than at the flag. Every switch here (/Create /Delete /Query
# /TN /XML /F /FO) has the same shape, so conversion is disabled for the whole
# call rather than per argument. Both variable names are set: MSYS_NO_PATHCONV
# is Git-for-Windows', MSYS2_ARG_CONV_EXCL is MSYS2's, and this file is expected
# to run under either.
#
# Scoped to the wrapper, deliberately not exported: path conversion is CORRECT
# for everything else here, and cygpath's output depends on it.
schtasks_() { MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*' schtasks "$@"; }

APPLY=0; REMOVE=0
case "${1:-}" in
  --apply)  APPLY=1 ;;
  --remove) REMOVE=1 ;;
  "")       : ;;
  *) echo "usage: eng-schedule-win.sh [--apply|--remove]" >&2; exit 2 ;;
esac

# Task Scheduler paths use backslashes and a leading one. Kept in a folder so
# `schtasks /Query /TN \business-os\` lists exactly the department's jobs and
# nothing else, and so removing them is a folder-scoped operation rather than a
# hunt through several hundred system tasks.
FOLDER='\business-os'
LOOP_TN="$FOLDER\\eng-loop"
WATCH_TN="$FOLDER\\eng-watch"
REPORT_TN="$FOLDER\\eng-report"

# -- Remove -----------------------------------------------------------------
if [ "$REMOVE" -eq 1 ]; then
  for tn in "$LOOP_TN" "$WATCH_TN" "$REPORT_TN"; do
    if schtasks_ /Delete /TN "$tn" /F >/dev/null 2>&1; then
      echo "  removed $tn"
    else
      echo "  $tn — not present"
    fi
  done
  exit 0
fi

# -- Discover instances -----------------------------------------------------
# Only to REPORT them, and to refuse an empty install. Unlike the launchd watch
# job, no task here embeds a per-instance path — the poll calls eng-loop-all.sh,
# which rediscovers instances on every fire. Onboarding a business therefore
# needs no re-registration on this host at all.
INSTANCES=""
for eng in "$BUSINESS_OS"/instances/*/engineering; do
  [ -d "$eng" ] || continue
  [ -f "$eng/config/instantiated-from" ] || continue
  INSTANCES="$INSTANCES $eng"
done
if [ -z "$INSTANCES" ]; then
  echo "eng-schedule-win: no instances found under $BUSINESS_OS/instances — nothing to schedule." >&2
  exit 0
fi

echo "Engineering schedule — Windows Task Scheduler ($([ "$APPLY" -eq 1 ] && echo APPLY || echo "dry run"))"
for eng in $INSTANCES; do echo "  instance: $(basename "$(dirname "$eng")")"; done

# -- The shell that runs a task ---------------------------------------------
# Task Scheduler launches a Windows executable, so every task is
# `bash.exe -l -c '<runner> <args> >> <log> 2>&1'`. Passing the script as an
# ARGUMENT to the shell rather than exec'ing it is the same shape the launchd
# plists use; there it dodges a TCC taint, here it is simply the only way to hand
# a POSIX script to a Windows scheduler.
#
# TWO details here are load-bearing, and both were found the hard way.
#
# 1. Git\bin\bash.exe, NOT /usr/bin/sh.exe. They are different programs: the one
#    in Git\bin is the launcher meant to be called from outside, the one in
#    usr\bin is MSYS-internal and assumes an MSYS environment already exists.
#    Started by Task Scheduler the internal shell inherits only the Windows
#    PATH — /usr/bin is not on it — so the pass died with
#
#      eng-loop-all.sh: line 28: dirname: command not found
#      eng-loop-all.sh: line 38: date: command not found
#
#    and then wrote its log to `///logs/eng-loop-all-.log`, because the paths it
#    builds out of `dirname` and `date` were empty strings. Nothing in that
#    failure names PATH.
#
# 2. `-l`. A login shell sources /etc/profile, which is what actually assembles
#    the MSYS PATH. Without it the launcher is no better than the internal shell.
#
# Verified from inside a scheduled task: with `-l` the pass sees /usr/bin,
# /mingw64/bin, the Python install and node.
# cygpath -m (mixed: C:/Program Files/Git/), and the POSIX form is deliberately
# NOT used to reach the launcher. MSYS mounts `/bin` onto Git\usr\bin, so the
# POSIX path /bin/bash.exe names the INTERNAL shell and there is no POSIX path
# that names Git\bin\bash.exe at all — `cygpath -u` on the launcher's own
# Windows path even hands back /bin/bash.exe, which is a different file on disk
# (43 KB launcher vs 2.4 MB internal shell). Staying in the mixed form sidesteps
# the mount table entirely, and bash accepts it in a -x test.
_git_root_m="$(cygpath -m / 2>/dev/null || echo /)"
LAUNCH_SH="${_git_root_m%/}/bin/bash.exe"
if [ ! -x "$LAUNCH_SH" ]; then
  echo "eng-schedule-win: FATAL — no login-shell launcher at $LAUNCH_SH." >&2
  echo "eng-schedule-win: expected Git for Windows' bin\\bash.exe. Is this Git Bash?" >&2
  exit 1
fi
SH_WIN="$(cygpath -w "$LAUNCH_SH")"

# -m (mixed: C:/path/like/this) not -w. These land inside a single-quoted string
# in the task's Arguments, where a backslash is an escape character to the very
# shell that will read them back.
runner_m="$(cygpath -m "$RUNNER")"
report_m="$(cygpath -m "$REPORT_RUNNER")"
logdir_m="$(cygpath -m "$LOG_DIR")"
mkdir -p "$LOG_DIR"

# The account the task runs as. InteractiveToken (below) means "only while this
# user is logged on" — deliberate, and the honest limitation of this host: it
# needs no stored password, and a pass that opens a PR or pings an approver
# should not be running against an account nobody is signed in to anyway.
TASK_USER="${USERDOMAIN:-$COMPUTERNAME}\\${USERNAME}"

xml_escape() { sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g'; }

# One task's XML. Written as XML rather than driven by `schtasks /Create /SC`
# flags because the loop job needs FOUR triggers on one task and the flag form
# takes exactly one /ST — the alternative is four separate tasks with four
# separate names to keep in step.
task_xml() { # task_xml <description> <arguments> <triggers-xml> <time-limit>
  _desc="$1"; _args="$2"; _trig="$3"; _limit="$4"
  cat <<XML
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>$(printf '%s' "$_desc" | xml_escape)</Description>
    <Author>business-os departments/engineering</Author>
  </RegistrationInfo>
  <Triggers>
$_trig
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
    <ExecutionTimeLimit>$_limit</ExecutionTimeLimit>
    <!-- 5, not the 7 Task Scheduler defaults to. 7 is below-normal for both CPU
         and I/O, and an on-demand launch on this laptop already measured ~2.5
         minutes from /Run to first output; a pass with a 30-minute timeout
         should not also be starting last. 5 is normal priority. -->
    <Priority>5</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>$(printf '%s' "$SH_WIN" | xml_escape)</Command>
      <Arguments>$(printf '%s' "$_args" | xml_escape)</Arguments>
    </Exec>
  </Actions>
</Task>
XML
}

# StartBoundary's DATE is irrelevant for a recurring trigger — only the time of
# day and the recurrence matter — but it must be in the past or the first fire
# waits for it. A fixed past date is used so regenerating produces identical XML.
daily_trigger() { # daily_trigger <HH:MM>
  printf '    <CalendarTrigger>\n      <StartBoundary>2026-01-01T%s:00</StartBoundary>\n      <Enabled>true</Enabled>\n      <ScheduleByDay><DaysInterval>1</DaysInterval></ScheduleByDay>\n    </CalendarTrigger>\n' "$1"
}

# MultipleInstancesPolicy IgnoreNew above is what makes a 5-minute poll safe: a
# pass that outruns its interval is not joined by a second copy. The per-instance
# mkdir lock in eng-trigger.sh would catch it anyway; this stops it one level up,
# before a process is even spawned. A Repetition with no Duration repeats
# indefinitely, which is what "forever, every 5 minutes" requires.
watch_trigger() {
  printf '    <CalendarTrigger>\n      <StartBoundary>2026-01-01T00:00:00</StartBoundary>\n      <Enabled>true</Enabled>\n      <Repetition>\n        <Interval>PT5M</Interval>\n        <StopAtDurationEnd>false</StopAtDurationEnd>\n      </Repetition>\n      <ScheduleByDay><DaysInterval>1</DaysInterval></ScheduleByDay>\n    </CalendarTrigger>\n'
}

weekly_sunday_trigger() { # weekly_sunday_trigger <HH:MM>
  printf '    <CalendarTrigger>\n      <StartBoundary>2026-01-04T%s:00</StartBoundary>\n      <Enabled>true</Enabled>\n      <ScheduleByWeek>\n        <DaysOfWeek><Sunday /></DaysOfWeek>\n        <WeeksInterval>1</WeeksInterval>\n      </ScheduleByWeek>\n    </CalendarTrigger>\n' "$1"
}

register() { # register <task-name> <description> <arguments> <triggers> <time-limit>
  _tn="$1"; _desc="$2"; _args="$3"; _trig="$4"; _limit="$5"
  if [ "$APPLY" -eq 0 ]; then
    if schtasks_ /Query /TN "$_tn" >/dev/null 2>&1; then
      echo "  $_tn — present, would re-register"
    else
      echo "  $_tn — would create"
    fi
    return 0
  fi

  _f="$(mktemp)"
  # UTF-16LE with a BOM. schtasks /XML rejects a UTF-8 file whose declaration
  # says UTF-16, and is inconsistent across Windows builds about accepting a
  # UTF-8 declaration, so the bytes are written to match what the declaration
  # promises. iconv ships with Git Bash; the fallback keeps a host without it
  # working rather than failing the whole install over an encoding.
  if command -v iconv >/dev/null 2>&1; then
    task_xml "$_desc" "$_args" "$_trig" "$_limit" | iconv -f UTF-8 -t UTF-16LE > "$_f.x"
    printf '\377\376' > "$_f"
    cat "$_f.x" >> "$_f"
    rm -f "$_f.x"
  else
    task_xml "$_desc" "$_args" "$_trig" "$_limit" | sed 's/encoding="UTF-16"/encoding="UTF-8"/' > "$_f"
  fi

  # /F overwrites. Unlike the launchd side there is no "unchanged" case: an
  # exported task is not byte-identical to the XML that created it (Windows
  # normalises it and fills in defaults), so comparing the two would report a
  # spurious change on every run. Re-registering is idempotent, so it always does.
  if schtasks_ /Create /TN "$_tn" /XML "$(cygpath -w "$_f")" /F >/dev/null 2>&1; then
    echo "  $_tn — registered"
    rm -f "$_f"
  else
    echo "  $_tn — FAILED to register. The XML is kept at $_f; reproduce with:" >&2
    echo "      schtasks /Create /TN \"$_tn\" /XML \"$(cygpath -w "$_f")\" /F" >&2
    return 1
  fi
}

# `< /dev/null` on every action. A scheduled task has no console, so stdin is
# whatever handle the scheduler happened to leave attached — and `claude -p`
# reads stdin when it is not a terminal. A pass reaching the launcher with an
# open, never-closed stdin would sit there until ExecutionTimeLimit killed it,
# holding the instance lock the whole time and looking exactly like a slow pass.
echo

register "$LOOP_TN" \
  "business-os engineering — safety-net sweep across every instance (schedules/eng_build_loop.md)" \
  "-l -c \"exec '$runner_m' scheduled schtasks < /dev/null >> '$logdir_m/eng-loop-task.log' 2>&1\"" \
  "$(daily_trigger 02:00; daily_trigger 09:30; daily_trigger 15:30; daily_trigger 20:30)" \
  "PT2H"

register "$WATCH_TN" \
  "business-os engineering — poll the instance inboxes for writes that bypass the control center" \
  "-l -c \"exec '$runner_m' watch schtasks < /dev/null >> '$logdir_m/eng-watch-task.log' 2>&1\"" \
  "$(watch_trigger)" \
  "PT1H"

register "$REPORT_TN" \
  "business-os engineering — weekly report (schedules/eng_weekly_report.md)" \
  "-l -c \"exec '$report_m' < /dev/null >> '$logdir_m/eng-report-task.log' 2>&1\"" \
  "$(weekly_sunday_trigger 18:30)" \
  "PT1H"

echo
if [ "$APPLY" -eq 0 ]; then
  echo "Dry run — nothing written. Re-run with --apply."
else
  echo "Registered. Inspect them with:"
  echo "  schtasks /Query /TN '$LOOP_TN' /V /FO LIST"
  echo "Run one by hand, right now:"
  echo "  schtasks /Run /TN '$LOOP_TN'"
  echo "They run only while $TASK_USER is logged on (LogonType InteractiveToken)."
fi
