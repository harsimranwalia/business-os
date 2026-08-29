#!/bin/sh
# cloudflare-tunnel.sh [--apply|--remove] — expose the Control Center at
# CONTROL_CENTER_TUNNEL_HOSTNAME (repo-root .env) via a Cloudflare Tunnel, so
# it is reachable from the internet without opening a port or a static IP.
# The email+PIN gate in server.py (CONTROL_CENTER_USERS) is what makes that
# safe to do at all; this script only gets you the pipe.
#
#   sh control-center/cloudflare-tunnel.sh            dry run: show what's missing/would change
#   sh control-center/cloudflare-tunnel.sh --apply    create the tunnel, route DNS, register at login, start it
#   sh control-center/cloudflare-tunnel.sh --remove   stop it and unregister the login hook only — the
#                                                      tunnel and its DNS record are left alone in your
#                                                      Cloudflare account; delete those yourself
#                                                      (`cloudflared tunnel delete business-os-control-center`,
#                                                      then the DNS record) if you want them gone entirely
#
# ---- Two steps this script genuinely cannot do for you -------------------
#   1. Install cloudflared for your OS (this script tells you the command).
#   2. `cloudflared tunnel login` — opens a browser, you approve on
#      dash.cloudflare.com against YOUR Cloudflare account, and cloudflared
#      drops a cert at ~/.cloudflared/cert.pem. That has to be an interactive
#      browser session logged in as you; nothing here can automate it.
# Once cert.pem exists, --apply does everything else: create the tunnel,
# write its config, add the DNS record, and register it to run at login.
#
# ---- Same host-split as autostart.sh, same reasons -------------------------
# Login trigger, not boot: a tunnel to a server that only exists once someone
# is signed in is useless before then, and both hosts have a login hook that
# needs neither a stored password nor an elevation prompt.
set -eu

CC="$(CDPATH= cd -P -- "$(dirname -- "$0")" && pwd -P)"
ROOT="$(CDPATH= cd -P -- "$CC/.." && pwd -P)"
LOG_DIR="$ROOT/logs"
LOG="$LOG_DIR/cloudflare-tunnel.log"
TUNNEL_NAME="business-os-control-center"
PORT=7777

# One value out of .env, not a general parser (server.py's load_env() already
# owns that job for the Python side) — grep is enough for a single key and
# can't misparse the rest of the file the way a hand-rolled shell parser could.
env_var() {
  [ -f "$ROOT/.env" ] || return 0
  grep -m1 "^$1=" "$ROOT/.env" 2>/dev/null | cut -d= -f2- \
    | sed -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//"
}
HOSTNAME="$(env_var CONTROL_CENTER_TUNNEL_HOSTNAME)"

APPLY=0; REMOVE=0
case "${1:-}" in
  --apply)  APPLY=1 ;;
  --remove) REMOVE=1 ;;
  "")       : ;;
  *) echo "usage: cloudflare-tunnel.sh [--apply|--remove]" >&2; exit 2 ;;
esac

case "$(uname -s)" in
  Darwin)               HOST_KIND=mac ;;
  MINGW*|MSYS*|CYGWIN*) HOST_KIND=windows ;;
  *)                    HOST_KIND=other ;;
esac

if [ "$HOST_KIND" = other ] && [ "$REMOVE" -eq 0 ]; then
  echo "cloudflare-tunnel: no login hook known for $(uname -s)." >&2
  echo "  Everything up through 'cloudflared tunnel run $TUNNEL_NAME --config ...' below" >&2
  echo "  still applies by hand; you just supervise the process yourself." >&2
fi

if [ -z "$HOSTNAME" ] && [ "$REMOVE" -eq 0 ]; then
  echo "CONTROL_CENTER_TUNNEL_HOSTNAME is not set in .env — add e.g." >&2
  echo "  CONTROL_CENTER_TUNNEL_HOSTNAME=control.aiorders.io" >&2
  echo "(that subdomain's zone — aiorders.io — needs to already be added to your" >&2
  echo " Cloudflare account for the DNS route step below to work)." >&2
  exit 1
fi

CLOUDFLARED="$(command -v cloudflared 2>/dev/null || true)"

# -- Remove: unregister the login hook only; never touch the live tunnel ---
if [ "$REMOVE" -eq 1 ]; then
  if [ "$HOST_KIND" = mac ]; then
    LABEL="com.businessos.cloudflare-tunnel"
    launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
    rm -f "$HOME/Library/LaunchAgents/$LABEL.plist"
    echo "  removed $LABEL"
  elif [ "$HOST_KIND" = windows ]; then
    MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*' schtasks /Delete /TN '\business-os\cloudflare-tunnel' /F >/dev/null 2>&1 \
      && echo "  removed \\business-os\\cloudflare-tunnel" \
      || echo "  \\business-os\\cloudflare-tunnel — not present"
  fi
  echo "Tunnel + DNS record are untouched. To delete them entirely:"
  echo "  cloudflared tunnel route dns --delete $TUNNEL_NAME $HOSTNAME   # or just delete the DNS record in the dashboard"
  echo "  cloudflared tunnel delete $TUNNEL_NAME"
  exit 0
fi

# -- Preflight: the two manual steps ----------------------------------------
if [ -z "$CLOUDFLARED" ]; then
  echo "cloudflared is not installed." >&2
  case "$HOST_KIND" in
    windows) echo "  winget install --id Cloudflare.cloudflared -e" >&2 ;;
    mac)     echo "  brew install cloudflared" >&2 ;;
    *)       echo "  https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/" >&2 ;;
  esac
  echo "Then re-run this script." >&2
  exit 1
fi

CERT="$HOME/.cloudflared/cert.pem"
if [ ! -f "$CERT" ]; then
  echo "cloudflared is installed but not authenticated to Cloudflare yet." >&2
  echo "Run this yourself — it opens a browser against YOUR Cloudflare account," >&2
  echo "which nothing in this repo can do on your behalf:" >&2
  echo "    cloudflared tunnel login" >&2
  echo "Then re-run this script." >&2
  exit 1
fi

# -- Find or create the tunnel ----------------------------------------------
existing_id() {
  "$CLOUDFLARED" tunnel list 2>/dev/null | awk -v n="$TUNNEL_NAME" '$0 ~ n {print $1; exit}'
}
TUNNEL_ID="$(existing_id)"

echo "Cloudflare Tunnel for the Control Center ($([ "$APPLY" -eq 1 ] && echo APPLY || echo "dry run"))"
echo "  hostname: $HOSTNAME -> http://localhost:$PORT"
echo

if [ -z "$TUNNEL_ID" ]; then
  if [ "$APPLY" -eq 0 ]; then
    echo "  tunnel '$TUNNEL_NAME' — would create"
    echo
    echo "Dry run — nothing written. Re-run with --apply."
    exit 0
  fi
  echo "Creating tunnel '$TUNNEL_NAME'..."
  "$CLOUDFLARED" tunnel create "$TUNNEL_NAME"
  TUNNEL_ID="$(existing_id)"
  [ -n "$TUNNEL_ID" ] || { echo "tunnel create ran but the id could not be read back" >&2; exit 1; }
else
  echo "  tunnel '$TUNNEL_NAME' — exists ($TUNNEL_ID)"
  if [ "$APPLY" -eq 0 ]; then
    echo
    echo "Dry run — nothing written. Re-run with --apply."
    exit 0
  fi
fi

CRED_FILE="$HOME/.cloudflared/$TUNNEL_ID.json"
CONFIG_FILE="$HOME/.cloudflared/$TUNNEL_NAME.yml"

# cloudflared.exe is a native Windows binary, not an MSYS-aware one — it
# cannot parse the /c/Users/... form $HOME takes under Git Bash. The YAML
# it reads needs a Windows-style path; the shell script writing that YAML
# does not, so only the value INSIDE the file gets the cygpath treatment.
CRED_FILE_FOR_YAML="$CRED_FILE"
[ "$HOST_KIND" = windows ] && CRED_FILE_FOR_YAML="$(cygpath -m "$CRED_FILE")"

# credentials-file/config live in ~/.cloudflared, not the repo: they're
# host-specific absolute paths and a tunnel-account secret, neither of which
# belongs in git even gitignored-and-local — same reasoning as .env itself.
cat > "$CONFIG_FILE" <<YAML
tunnel: $TUNNEL_ID
credentials-file: $CRED_FILE_FOR_YAML

ingress:
  - hostname: $HOSTNAME
    service: http://localhost:$PORT
  - service: http_status:404
YAML
echo "  config written -> $CONFIG_FILE"

echo "Routing DNS $HOSTNAME -> tunnel $TUNNEL_NAME..."
"$CLOUDFLARED" tunnel route dns "$TUNNEL_NAME" "$HOSTNAME"

mkdir -p "$LOG_DIR"

# -- macOS: a per-user LaunchAgent, same shape as autostart.sh's ------------
if [ "$HOST_KIND" = mac ]; then
  LABEL="com.businessos.cloudflare-tunnel"
  PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
  cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>$LABEL</string>
	<key>ProgramArguments</key>
	<array>
		<string>$CLOUDFLARED</string>
		<string>tunnel</string>
		<string>--config</string>
		<string>$CONFIG_FILE</string>
		<string>run</string>
		<string>$TUNNEL_NAME</string>
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
  launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$PLIST"
  echo "  $LABEL — written and loaded"
  echo
  echo "Now running -> https://$HOSTNAME   (log: $LOG)"
  exit 0
fi

# -- Windows: a Task Scheduler job, same shape as autostart.sh's -----------
if [ "$HOST_KIND" = windows ]; then
  schtasks_() { MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*' schtasks "$@"; }
  TN='\business-os\cloudflare-tunnel'

  CLOUDFLARED_W="$(cygpath -w "$CLOUDFLARED")"
  CONFIG_W="$(cygpath -w "$CONFIG_FILE")"
  LOG_W="$(cygpath -w "$LOG")"
  TASK_USER="${USERDOMAIN:-$COMPUTERNAME}\\${USERNAME}"
  ARGS="tunnel --config \"$CONFIG_W\" run $TUNNEL_NAME"

  xml_escape() { sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g'; }

  _f="$(mktemp)"
  {
    cat <<XML
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Cloudflare Tunnel for business-os Control Center -> https://$HOSTNAME, started at logon (control-center/cloudflare-tunnel.sh)</Description>
    <Author>business-os control-center</Author>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <UserId>$(printf '%s' "$TASK_USER" | xml_escape)</UserId>
      <Delay>PT45S</Delay>
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
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <RestartOnFailure>
      <Interval>PT1M</Interval>
      <Count>3</Count>
    </RestartOnFailure>
    <Priority>5</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>$(printf '%s' "$CLOUDFLARED_W" | xml_escape)</Command>
      <Arguments>$(printf '%s' "$ARGS" | xml_escape)</Arguments>
      <WorkingDirectory>$(printf '%s' "$(cygpath -w "$CC")" | xml_escape)</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
XML
  } | { if command -v iconv >/dev/null 2>&1; then
          printf '\377\376' > "$_f"; iconv -f UTF-8 -t UTF-16LE >> "$_f"
        else
          sed 's/encoding="UTF-16"/encoding="UTF-8"/' > "$_f"
        fi; }

  if schtasks_ /Create /TN "$TN" /XML "$(cygpath -w "$_f")" /F >/dev/null 2>&1; then
    echo "  $TN — registered"
    rm -f "$_f"
  else
    echo "  $TN — FAILED to register. XML kept at $_f; reproduce with:" >&2
    echo "      schtasks /Create /TN \"$TN\" /XML \"$(cygpath -w "$_f")\" /F" >&2
    exit 1
  fi

  if schtasks_ /Run /TN "$TN" >/dev/null 2>&1; then
    echo "  $TN — started now"
  else
    echo "  $TN — registered, but /Run failed; it will still fire at next logon" >&2
  fi

  echo
  echo "Now running -> https://$HOSTNAME   (log: $LOG_W)"
  echo "Inspect it:  schtasks /Query /TN '$TN' /V /FO LIST"
  echo "Stop it:     schtasks /End /TN '$TN'"
  exit 0
fi

echo "Config and DNS route are done. Start it by hand on this host:"
echo "  $CLOUDFLARED tunnel --config '$CONFIG_FILE' run $TUNNEL_NAME"
