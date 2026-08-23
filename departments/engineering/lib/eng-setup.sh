#!/bin/zsh
# eng-setup.sh — turn the engineering department on.
#
# One command instead of a checklist. Everything here is idempotent: run it
# again after a change, on a new machine, or when something looks wrong, and it
# will fix what's missing and leave the rest alone.
#
#   ./lib/eng-setup.sh          check everything, report, change nothing
#   ./lib/eng-setup.sh --apply  actually create dirs, worktrees, and load agents
#
# There is no cron here. macOS launchd does both jobs — filesystem events
# (WatchPaths) and the scheduled safety net (StartCalendarInterval) — and this
# machine already runs the control center and cloudflared that way. One
# scheduling mechanism, not two.

set -uo pipefail

# ── NOT YET PORTED ─────────────────────────────────────────────────────────
# This script installs the life-os host wiring: macOS launchd plists, git
# worktrees laid out for one person's projects directory, and a Slack webhook
# check. Almost none of it applies to a business-os instance, which runs on
# cron and notifies through lib/eng-notify.sh.
#
# It is kept here as the reference implementation for the Phase 2 port, and
# guarded so it cannot be run by accident — its hardcoded ROOT below points at
# life-os, so running it from business-os would install schedulers pointing at
# the wrong repository entirely.
if [ -z "${ENG_SETUP_I_KNOW_THIS_IS_UNPORTED:-}" ]; then
  echo "eng-setup.sh is not yet ported to the instance model (Phase 2)." >&2
  echo "It would install host wiring pointing at life-os, not at this instance." >&2
  echo "Use lib/eng-env.sh + your own cron entry until the port lands." >&2
  exit 2
fi


ROOT="/Users/hwalia/Documents/projects/life-os"
PROJECTS_DIR="$(dirname "$ROOT")"
ENG_WORKTREES="$PROJECTS_DIR/_eng"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"
PLIST_SRC="$ROOT/lib/launchd"

APPLY=0
[ "${1:-}" = "--apply" ] && APPLY=1

ok()   { echo "  ✅ $*"; }
warn() { echo "  ⚠️  $*"; }
bad()  { echo "  ❌ $*"; FAILED=1; }
act()  { if [ "$APPLY" = "1" ]; then echo "  → $*"; else echo "  · would: $*"; fi }
FAILED=0

echo
echo "Engineering department — setup check"
[ "$APPLY" = "1" ] && echo "(applying changes)" || echo "(dry run — pass --apply to make changes)"
echo

# ── 1. State directories ───────────────────────────────────────────────────
echo "1. Directories"
for d in "$ROOT/traces/eng" "$ROOT/input/inbox" \
         "$ROOT/agents/product-manager/inbox" \
         "$ROOT/agents/eng-manager/inbox" \
         "$ROOT/agents/cfo/inbox"; do
  if [ -d "$d" ]; then
    ok "${d#$ROOT/}"
  else
    act "create ${d#$ROOT/}"
    [ "$APPLY" = "1" ] && mkdir -p "$d"
  fi
done
echo

# ── 2. Working copies ──────────────────────────────────────────────────────
# The department never runs git in Harry's own directories — a cron-triggered
# checkout under his uncommitted changes is a way to lose work. Every project
# except life-os gets a worktree it owns.
echo "2. Working copies (projects/_eng/) — the department never touches your directories"
if [ ! -d "$ENG_WORKTREES" ]; then
  act "create $ENG_WORKTREES"
  [ "$APPLY" = "1" ] && mkdir -p "$ENG_WORKTREES"
fi

# project → repo path relative to PROJECTS_DIR. Harry's repos are not all flat
# siblings: verido lives under 42works/, mirror-hq under personal/ — so map each
# name to its real location instead of assuming $PROJECTS_DIR/$proj. Keep this in
# sync with the Repo path column in agents/eng-manager/config/projects.md.
# aiorders is a multi-repo container (no single .git) and correctly hits the skip
# below until it is onboarded one worktree per sub-repo.
# Each entry is project-name:path-relative-to-PROJECTS_DIR. Multi-repo projects
# (aiorders) register as one entry per sub-repo, each with its own flat
# _eng/{name}/ worktree — matching the _eng/{project}/ convention the build loop
# and release-runner assume. OpenWA (third-party) and twenty-crm (vendored OSS)
# are deliberately excluded — see projects.md "Deliberately not registered".
for entry in \
  "verido:42works/verido" \
  "mirror-hq:personal/mirror-hq" \
  "business-os:personal/business-os" \
  "aiorders-admin-hub:aiorders/aiorders-admin-hub" \
  "aiorders-api:aiorders/aiorders-api" \
  "config-site-builder:aiorders/config-site-builder" \
  "restaurant-marketplace:aiorders/restaurant-marketplace" \
  "restaurant-portal:aiorders/restaurant-portal"; do
  proj="${entry%%:*}"
  src="$PROJECTS_DIR/${entry#*:}"
  dst="$ENG_WORKTREES/$proj"
  if [ ! -d "$src/.git" ] && [ ! -f "$src/.git" ]; then
    warn "$proj — no repo at $src, skipping (multi-repo projects need one worktree per repo)"
    continue
  fi
  # A repo with zero commits can't have a real worktree — `git worktree add`
  # leaves a broken null-HEAD stub the build loop would choke on. Skip until it
  # has an initial commit.
  if ! git -C "$src" rev-parse HEAD >/dev/null 2>&1; then
    warn "$proj — repo has no commits yet, skipping worktree (make an initial commit first)"
    continue
  fi
  if [ -d "$dst" ]; then
    ok "$proj worktree exists"
  else
    branch="eng/base"
    act "git -C $src worktree add -b $branch $dst"
    if [ "$APPLY" = "1" ]; then
      git -C "$src" worktree add -b "$branch" "$dst" 2>/dev/null \
        || git -C "$src" worktree add "$dst" 2>/dev/null \
        || warn "$proj — worktree add failed; create it by hand and re-run"
    fi
  fi
done
ok "life-os — no worktree needed (agents already run in it by design)"
echo

# ── 3. Secrets ─────────────────────────────────────────────────────────────
echo "3. Notifications"
source "$ROOT/.env" 2>/dev/null
if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
  ok "SLACK_WEBHOOK_URL set — gate items will reach you in #life-os"
else
  bad "SLACK_WEBHOOK_URL missing from .env — the department will still work, but"
  echo "     nothing will tell you a decision is waiting. Fix this before relying on it."
fi
echo

# ── 4. launchd agents ──────────────────────────────────────────────────────
echo "4. launchd agents (no cron anywhere)"
mkdir -p "$LAUNCH_AGENTS" 2>/dev/null

for label in com.lifeos.eng-watch com.lifeos.eng-loop; do
  src="$PLIST_SRC/$label.plist"
  dst="$LAUNCH_AGENTS/$label.plist"
  if [ ! -f "$src" ]; then
    bad "$label — source plist missing at ${src#$ROOT/}"
    continue
  fi
  if [ -f "$dst" ] && cmp -s "$src" "$dst"; then
    ok "$label installed and current"
  else
    act "install $label.plist → $dst"
    [ "$APPLY" = "1" ] && cp "$src" "$dst"
  fi

  if launchctl list 2>/dev/null | grep -q "$label"; then
    ok "$label loaded"
  else
    act "launchctl load $dst"
    [ "$APPLY" = "1" ] && launchctl load "$dst" 2>/dev/null
  fi
done
echo

# ── 5. The control center ──────────────────────────────────────────────────
echo "5. Control center (fires intake + decision events)"
if curl -s -o /dev/null -m 2 http://localhost:7777/api/engineering 2>/dev/null; then
  ok "running and serving /api/engineering"
else
  warn "not responding on :7777 — the Engineering tab and its Approve buttons"
  echo "     need it. Start it: launchctl load ~/Library/LaunchAgents/com.lifeos.control-center.plist"
fi
echo

# ── 6. Full Disk Access ────────────────────────────────────────────────────
# Can't be checked programmatically — TCC failures look like ordinary
# permission errors, and only show up when a launchd-spawned pass tries to read
# ~/Documents. Flagged every run because it's the single most common reason a
# correctly-wired Life OS routine silently does nothing.
echo "6. Full Disk Access — check by hand, once"
echo "   System Settings → Privacy & Security → Full Disk Access must include:"
echo "     /bin/zsh"
echo "     /Users/hwalia/.local/bin/claude"
echo "   launchd-spawned processes do NOT inherit Terminal's grant. Without this,"
echo "   passes run but silently can't read ~/Documents. See docs/cron-with-tools-mac.md."
echo

# ── Summary ────────────────────────────────────────────────────────────────
echo "──────────────────────────────────────────────"
if [ "$APPLY" = "0" ]; then
  echo "Dry run. Nothing changed. Re-run with --apply to wire it up."
elif [ "$FAILED" = "1" ]; then
  echo "Wired, with problems above. Fix those before trusting it."
else
  echo "Wired. The department is live."
fi
echo
echo "How it runs now:"
echo "  • You send a build request in the Engineering tab   → PM shapes it immediately"
echo "  • You approve a gate (tab, or 'approve ENG-004'     → that ticket moves immediately"
echo "    in Slack)"
echo "  • An agent files a bug / finding                    → picked up on the inbox write"
echo "  • A pass finishes mid-flow                          → it fires its own next hop"
echo "  • Weekdays 09:30 / 15:30                            → safety-net sweep only"
echo
echo "Smoke test it end to end:"
echo "  1. Open http://localhost:7777 → Engineering → send a small build request"
echo "  2. Watch: tail -f $ROOT/traces/eng/eng-loop-\$(date +%Y-%m-%d).log"
echo "  3. Within a minute or two a G1 item should appear in #life-os"
echo "  4. Reply 'approve ENG-001' and watch the next hop fire"
echo
echo "To stop everything:"
echo "  launchctl unload ~/Library/LaunchAgents/com.lifeos.eng-{watch,loop}.plist"
