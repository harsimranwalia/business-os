#!/bin/sh
# eng-setup.sh — bring one instance's host wiring up to date.
#
#   ENG_INSTANCE=… ./lib/eng-setup.sh          check everything, change nothing
#   ENG_INSTANCE=… ./lib/eng-setup.sh --apply  create what's missing
#
# Everything here is idempotent: run it again after a change, on a new machine,
# or when something looks wrong, and it fixes what's missing and leaves the rest
# alone.
#
# What this NO LONGER does: generate launchd plists. lib/eng-schedule.sh owns
# those, and owns them alone — it writes ONE pair of jobs covering every
# instance, and install.sh calls it on every onboard. Two scripts generating the
# same plists is how a freshly regenerated WatchPaths array gets overwritten by
# a stale copy and an instance's inboxes quietly stop being watched. Section 5
# delegates to it rather than reimplementing it.
#
# Its real remaining job is the two things nothing else does: the department's
# git worktrees, and the instance directories a run writes into.
set -u

DEPT="$(CDPATH= cd -P -- "$(dirname -- "$0")/.." && pwd -P)"
ENG_DEPT="${ENG_DEPT:-$DEPT}"
export ENG_DEPT
. "$ENG_DEPT/lib/eng-env.sh" || exit 1

APPLY=0
[ "${1:-}" = "--apply" ] && APPLY=1

BUSINESS="$(basename "$(dirname "$ENG_INSTANCE")")"
FAILED=0
ok()   { echo "  OK    $*"; }
warn() { echo "  WARN  $*"; }
bad()  { echo "  FAIL  $*"; FAILED=1; }
act()  { if [ "$APPLY" = "1" ]; then echo "  ->    $*"; else echo "  ·     would: $*"; fi; }

echo
echo "Engineering setup — $BUSINESS"
echo "  instance:  $ENG_INSTANCE"
echo "  mode:      ${ENG_MODE:-<unset>}$(eng_mode_halts && echo "  (PAUSED — passes exit without running)")"
[ "$APPLY" = "1" ] && echo "  (applying changes)" || echo "  (dry run — pass --apply to make changes)"
echo

# ── 1. Instance directories ────────────────────────────────────────────────
# The list is READ FROM install.sh rather than copied here. A second copy of a
# 30-entry directory list is a drift hazard: install.sh would gain a directory,
# this would keep passing, and the gap would only show up as a write failure
# mid-pass. One source of truth, parsed.
echo "1. Instance directories"
DIRS="$(sed -n '/^DIRS="/,/"$/p' "$ENG_DEPT/install.sh" | sed 's/^DIRS="//; s/"$//')"
if [ -z "$DIRS" ]; then
  bad "could not read the DIRS list out of install.sh — its format changed, fix this parser"
else
  missing=0
  for d in $DIRS; do
    if [ ! -d "$ENG_INSTANCE/$d" ]; then
      missing=$((missing + 1))
      act "create $d"
      if [ "$APPLY" = "1" ]; then mkdir -p "$ENG_INSTANCE/$d" && touch "$ENG_INSTANCE/$d/.gitkeep"; fi
    fi
  done
  [ "$missing" -eq 0 ] && ok "all $(echo "$DIRS" | wc -w | tr -d ' ') present"
fi
echo

# ── 2. The department's working copies ─────────────────────────────────────
# The department never runs git in a human's own checkout — a scheduled pass
# committing under someone's uncommitted changes is a way to lose work. Every
# registered repo gets a worktree the department owns, at $ENG_WORKTREES.
#
# The project list comes from THIS INSTANCE's registry, not a hardcoded table.
# The hardcoded one was life-os's project set and was wrong for every business
# that isn't life-os; worse, onboarding a repo would have meant editing a shared
# template by hand. Registering a repo in projects.md is now the only step.
echo "2. Working copies — $ENG_WORKTREES"
REGISTRY="$ENG_INSTANCE/agents/eng-manager/config/projects.md"
if [ ! -f "$REGISTRY" ]; then
  bad "no project registry at ${REGISTRY#$ENG_INSTANCE/} — run install.sh"
else
  if [ ! -d "$ENG_WORKTREES" ]; then
    act "create $ENG_WORKTREES"
    [ "$APPLY" = "1" ] && mkdir -p "$ENG_WORKTREES"
  fi

  # Registered-projects rows only. Every table in projects.md has a backticked
  # project name in column 1, so the name cannot be the discriminator — column 2
  # is. Only the registry table puts a filesystem path there; the Commands table
  # has "npm run lint" or an em-dash, and the autonomy table has prose.
  ROWS="$(awk -F'|' 'NF>=4 {
      n=$2; p=$3
      gsub(/[`[:space:]]/, "", n); gsub(/[`[:space:]]/, "", p)
      if (n != "" && p ~ /^[~\/]/) print n "\t" p
    }' "$REGISTRY")"

  if [ -z "$ROWS" ]; then
    warn "no repos registered yet — nothing to check out (skills/repo-onboarder/SKILL.md registers one)"
  else
    echo "$ROWS" | while IFS="$(printf '\t')" read -r proj src; do
      case "$src" in "~/"*) src="$HOME/${src#\~/}" ;; esac
      dst="$ENG_WORKTREES/$proj"

      # The instance's own operating repo is the documented exception: agents
      # already run inside it by design, so a worktree would be a second copy of
      # the thing they are standing in.
      if [ "$src" = "$BUSINESS_OS_ROOT" ]; then
        ok "$proj — no worktree needed (the department runs in it by design)"
        continue
      fi
      if [ ! -d "$src/.git" ] && [ ! -f "$src/.git" ]; then
        warn "$proj — no repo at $src, skipping (a multi-repo project registers one row per repo)"
        continue
      fi
      # A repo with zero commits cannot have a real worktree — `git worktree add`
      # leaves a broken null-HEAD stub the build loop would choke on.
      if ! git -C "$src" rev-parse HEAD >/dev/null 2>&1; then
        warn "$proj — no commits yet, skipping worktree (make an initial commit first)"
        continue
      fi
      if [ -d "$dst" ]; then
        ok "$proj"
        continue
      fi
      act "git -C $src worktree add -b eng/base $dst"
      if [ "$APPLY" = "1" ]; then
        git -C "$src" worktree add -b eng/base "$dst" 2>/dev/null \
          || git -C "$src" worktree add "$dst" 2>/dev/null \
          || warn "$proj — worktree add failed; create it by hand and re-run"
      fi
    done
  fi
fi
echo

# ── 3. Toolchain ───────────────────────────────────────────────────────────
# Checked because a scheduled pass does NOT get your shell's PATH. launchd hands
# a job PATH=/usr/bin:/bin:/usr/sbin:/sbin and nothing more, so node, npm, gh and
# timeout are all invisible to it unless eng-env.sh puts them back. This runs
# after eng-env.sh, so it is checking exactly what a pass will see.
echo "3. Toolchain (as a scheduled pass sees it, not as your shell does)"
for entry in "node:npm run build / lint — every registered project's verification" \
             "npm:the quality gate has nothing to run without it" \
             "git:branches, worktrees, merge-base" \
             "gh:opening the pull request an L1 project ends at" \
             "python3:lib/run-stream.py and eng-notify.sh" \
             "timeout:caps a pass; without it ENG_PASS_TIMEOUT is ignored and a hung pass runs forever"; do
  bin="${entry%%:*}"; why="${entry#*:}"
  if command -v "$bin" >/dev/null 2>&1; then
    ok "$(printf '%-8s %s' "$bin" "$(command -v "$bin")")"
  else
    bad "$(printf '%-8s missing — %s' "$bin" "$why")"
  fi
done
echo

# ── 4. Notifications ───────────────────────────────────────────────────────
echo "4. Notifications"
if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
  ok "SLACK_WEBHOOK_URL set — gate items will reach you"
else
  bad "SLACK_WEBHOOK_URL missing from $BUSINESS_OS_ROOT/.env — the department will"
  echo "        still work, but nothing will tell you a decision is waiting."
  echo "        Quote the value if it contains spaces or parentheses; eng-env.sh warns"
  echo "        when .env fails to source, which silently drops every line after it."
fi
echo

# ── 5. Scheduling ──────────────────────────────────────────────────────────
echo "5. Scheduling (lib/eng-schedule.sh owns these — one pair of jobs, all instances)"
for label in com.businessos.eng-loop com.businessos.eng-watch; do
  if launchctl list 2>/dev/null | grep -q "$label"; then ok "$label loaded"; else warn "$label not loaded"; fi
done
echo
if [ "$APPLY" = "1" ]; then sh "$ENG_DEPT/lib/eng-schedule.sh" --apply; else sh "$ENG_DEPT/lib/eng-schedule.sh"; fi
echo

# ── 6. The control center ──────────────────────────────────────────────────
echo "6. Control center (fires intake + decision events)"
if curl -s -o /dev/null -m 2 "http://localhost:7777/api/engineering?instance=$BUSINESS" 2>/dev/null; then
  ok "running and serving $BUSINESS"
else
  warn "not responding on :7777 — the Engineering tab and its Approve buttons need it."
  echo "        It is a life-os component: launchctl load ~/Library/LaunchAgents/com.lifeos.control-center.plist"
fi
echo

# ── 7. Full Disk Access ────────────────────────────────────────────────────
# Cannot be checked programmatically — TCC failures look like ordinary
# permission errors and only appear when a launchd-spawned pass tries to read
# ~/Documents. Printed every run because it is the single most common reason a
# correctly wired routine silently does nothing.
echo "7. Full Disk Access — check by hand, once"
echo "   System Settings -> Privacy & Security -> Full Disk Access must include:"
echo "     /bin/sh        (launchd runs the scheduler with it)"
echo "     /bin/zsh       (\$ENG_SHELL — runs each pass)"
echo "     /Users/hwalia/.local/bin/claude"
echo "   launchd-spawned processes do NOT inherit Terminal's grant."
echo

echo "──────────────────────────────────────────────"
if [ "$APPLY" = "0" ]; then
  echo "Dry run. Nothing changed. Re-run with --apply."
elif [ "$FAILED" = "1" ]; then
  echo "Wired, with failures above. Fix those before trusting it."
else
  echo "Wired. $BUSINESS is live."
fi
echo
echo "How it runs:"
echo "  You send a build request in the Engineering tab   -> PM shapes it immediately"
echo "  You approve a gate (tab, or in Slack)             -> that ticket moves immediately"
echo "  An agent files a bug / finding                    -> picked up on the inbox write"
echo "  A pass finishes mid-flow                          -> it fires its own next hop"
echo "  Daily 09:30 / 15:30 / 20:30 / 02:00                -> safety-net sweep, every instance"
echo
echo "Watch it:  tail -f $ENG_INSTANCE/traces/eng-loop-\$(date +%Y-%m-%d).log"
echo "Pause it:  set 'mode: sabbath' in $ENG_INSTANCE/config/config.yaml (this business only)"
