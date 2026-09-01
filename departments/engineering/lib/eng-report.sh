#!/usr/bin/env bash
# eng-report.sh — the department's weekly report pass.
#
# ONE job for ALL businesses, same reasoning as lib/eng-schedule.sh's other
# two jobs: this discovers instances rather than being installed per-business.
#
# NOT an eng-trigger.sh event. schedules/eng_weekly_report.md is a standalone
# read-the-board-and-write-a-report pass, not a step in the ticket state
# machine — it has no ticket, no WIP cap, no chaining, and (unlike every
# eng-trigger.sh event) nothing worth retrying: a report that fails this
# Sunday gets written next Sunday, so none of eng-trigger.sh's hop-budget /
# backoff / attempt-tracking machinery applies here. That is why this is its
# own small script rather than a sixth event bolted onto eng-trigger.sh's
# five-event vocabulary (`valid_event` in that file would need to grow, and
# every per-ticket assumption downstream of it would need auditing for a
# ticket-less caller).
#
# What it DOES share with a build-loop pass, on purpose: the mode check (this
# schedule is "suppressed on sabbath/retreat/quiet" same as the others), the
# per-instance single-flight lock (so it never reads the board mid-write by a
# concurrent eng-loop/eng-watch pass), and the run-stream.py cost-tracking
# wrapper every other routine's spend already goes through.
#
# Dual-shell for the same reason eng-trigger.sh is: invoked as `/bin/sh
# lib/eng-report.sh` from the launchd plist (see lib/eng-schedule.sh), same
# TCC-avoidance shape (the plist passes this file as an ARGUMENT to a system
# shell rather than exec'ing it directly — see eng-trigger.sh's own comment on
# why any repo-exec'd ancestor poisons every `claude` spawned beneath it).
set -uo pipefail

ENG_DEPT="$(CDPATH= cd -P -- "$(dirname -- "$0")/.." && pwd -P)"
BUSINESS_OS_ROOT="$(CDPATH= cd -P -- "$ENG_DEPT/../.." && pwd -P)"
export ENG_DEPT BUSINESS_OS_ROOT

found=0
for eng in "$BUSINESS_OS_ROOT"/instances/*/engineering; do
  [ -d "$eng" ] || continue
  [ -f "$eng/config/instantiated-from" ] || continue
  found=$((found + 1))
  (
    ENG_INSTANCE="$eng"
    export ENG_INSTANCE
    # shellcheck source=/dev/null
    . "$ENG_DEPT/lib/eng-env.sh" || exit 1

    STATE="$ENG_INSTANCE/traces"
    LOG="$STATE/eng-report-$(date '+%Y-%m-%d').log"
    log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

    if eng_mode_halts; then
      log "weekly report — MODE=$ENG_MODE, exiting silently"
      exit 0
    fi

    # Same lock file eng-trigger.sh uses ($STATE/.loop.lock), so this can never
    # read the board concurrently with a live build-loop pass. Simpler than
    # eng-trigger.sh's own acquire(): no staleness steal, no queueing — a
    # report is not part of anyone's chain, so if the lock is held, skip this
    # instance for this run rather than wait or retry. Next Sunday tries again.
    LOCK="$STATE/.loop.lock"
    if ! mkdir "$LOCK" 2>/dev/null; then
      owner=$(cat "$LOCK/pid" 2>/dev/null || echo "unknown")
      log "weekly report — .loop.lock held (owner $owner), skipping this week rather than racing a live pass"
      exit 0
    fi
    echo $$ > "$LOCK/pid"
    release() { [ "$(cat "$LOCK/pid" 2>/dev/null)" = "$$" ] && rm -rf "$LOCK"; }
    trap release EXIT

    MODEL="$("$ENG_DEPT/lib/model-tier.sh" reasoning 2>/dev/null || echo sonnet)"

    read -r -d '' PROMPT <<PROMPT_EOF
Run the engineering department's weekly report pass.

This is NOT an eng-trigger.sh event — there is no ticket, no chaining, no WIP
limit in play. Do not touch any ticket's state and do not act on any
gate; this pass reads the board and writes a report, nothing else.

WHERE THINGS LIVE. There are TWO roots, and every relative path in the
procedure below belongs to exactly one of them. Your working directory is the
instance.

  DEPARTMENT (shared template, READ-ONLY — never write here):
    $ENG_DEPT
    holds: schedules/, docs/, skills/, lib/, and each agent's agent.md +
    config.yaml — the definitions, identical for every business.

  INSTANCE (this business's state, where everything you write goes):
    $ENG_INSTANCE
    holds: agents/*/board, agents/*/inbox, agents/*/notebook, config/, inbox/,
    traces/, reports/ — the facts, unique to this business.

Follow $ENG_DEPT/schedules/eng_weekly_report.md exactly. It is the procedure —
do not improvise around it. Write reports/engineering-{YYYY-WXX}.md there, and
if agents/eng-manager/proposals.md's Open table is non-empty, raise the one
batched G1 exactly as that schedule's section 3b describes (one
inbox/PROP-{YYYY-WXX}.md item, via lib/eng-notify.sh raise, once).
PROMPT_EOF

    cd "$ENG_INSTANCE" || exit 1
    REPO_SHA="$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
    AGENT_VERSION="$("$ENG_DEPT/lib/agent-version.sh" eng-manager 2>/dev/null || echo unknown)"
    COSTS="$STATE/costs-$(hostname -s 2>/dev/null || echo unknown).jsonl"
    export ENG_PASS_TIMEOUT=1800

    log "launching weekly report — model: $MODEL"
    eng_run_claude --model "$MODEL" --effort max \
      --output-format stream-json --verbose -p "$PROMPT" 2>&1 \
      | python3 "$ENG_DEPT/lib/run-stream.py" \
          --routine eng_weekly_report \
          --agent eng-manager \
          --agent-version "$AGENT_VERSION" \
          --repo-sha "$REPO_SHA" \
          --host "$(hostname -s 2>/dev/null || echo unknown)" \
          --model-tier reasoning \
          --model-requested "$MODEL" \
          --out "$COSTS" \
      >> "$LOG"
    STATUS=$?
    log "weekly report pass end (exit $STATUS)"
  ) &
done

if [ "$found" -eq 0 ]; then
  echo "eng-report: no instances found under $BUSINESS_OS_ROOT/instances — nothing to report" >&2
  exit 0
fi

wait
