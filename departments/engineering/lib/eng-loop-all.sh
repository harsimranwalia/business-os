#!/bin/sh
# eng-loop-all.sh <event> [context] — fire one engineering pass per instance.
#
# The scheduler's entry point, and the reason there is ONE launchd job rather
# than one per business. A per-instance plist would mean onboarding a business
# requires installing host wiring by hand, which is the recurring-manual-step
# failure this system exists to remove. This discovers instances instead, the
# same way the control center does: anything under instances/*/engineering
# carrying config/instantiated-from is a real instance.
#
# Isolation is already per-instance and this relies on it rather than adding
# any: the single-flight lock is $ENG_INSTANCE/traces/.loop.lock and the daily
# hop budget is $ENG_INSTANCE/traces/.hops-DATE, so one business can neither
# block another's lock nor spend another's budget.
#
# Instances run CONCURRENTLY, then this waits for all of them. Serial would be
# gentler on rate limits but lets one wedged pass starve every business after
# it — and eng_timeout degrades to running UNCAPPED on a host with no
# timeout/gtimeout (true on this Mac), so "wedged" has no upper bound there.
# Waiting rather than detaching keeps launchd's job status honest: the job is
# running for exactly as long as some business's pass is.
#
# The mode check is deliberately NOT here. Each pass checks its own instance's
# mode inside eng-trigger.sh (eng_mode_halts, per-instance), so a paused business
# exits silently on its own and never blocks the others.
set -u

ENG_DEPT="$(CDPATH= cd -P -- "$(dirname -- "$0")/.." && pwd -P)"
BUSINESS_OS_ROOT="$(CDPATH= cd -P -- "$ENG_DEPT/../.." && pwd -P)"
export ENG_DEPT BUSINESS_OS_ROOT

EVENT="${1:-scheduled}"
CONTEXT="${2:-launchd}"

# Same rule eng-env.sh uses, resolved here because this runs before it.
SHELL_BIN="$([ -x /bin/zsh ] && echo /bin/zsh || echo /bin/sh)"

LOG="$BUSINESS_OS_ROOT/logs/eng-loop-all-$(date '+%Y-%m-%d').log"
mkdir -p "$(dirname "$LOG")" 2>/dev/null || true
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

found=0
for eng in "$BUSINESS_OS_ROOT"/instances/*/engineering; do
  # The literal glob when instances/ is empty, and any half-made directory.
  # config/instantiated-from is install.sh's marker and the same check
  # eng-env.sh fatals on, so a directory without it is not an instance.
  [ -d "$eng" ] || continue
  [ -f "$eng/config/instantiated-from" ] || continue
  found=$((found + 1))
  business="$(basename "$(dirname "$eng")")"
  log "$business — firing '$EVENT'"
  (
    ENG_INSTANCE="$eng" "$SHELL_BIN" "$ENG_DEPT/lib/eng-trigger.sh" "$EVENT" "$CONTEXT"
    log "$business — trigger exited $?"
  ) &
done

if [ "$found" -eq 0 ]; then
  # Loud, not silent. A scheduler that fires twice a day and finds nothing to do
  # looks identical to one that is not running at all.
  log "NO INSTANCES FOUND under $BUSINESS_OS_ROOT/instances — nothing fired"
  exit 0
fi

log "fired $found instance(s) for '$EVENT' — waiting"
wait
log "all instances finished for '$EVENT'"
