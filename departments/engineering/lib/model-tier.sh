#!/usr/bin/env bash
# lib/model-tier.sh <tier> — resolve a work tier to the model that runs it.
#
#   lib/model-tier.sh reasoning   -> sonnet
#   lib/model-tier.sh --list      -> every tier, one per line
#
# THE SINGLE PLACE THE TIER→MODEL MAPPING LIVES. `config/settings.yaml`'s
# `models:` block is the source; CLAUDE.md names that file authoritative for
# model routing, so this script reads it rather than restating it. ENG-016 AC5
# requires the mapping be written down in exactly one place, and before this
# script there were two: settings.yaml (documentation nothing read) and
# lib/eng-trigger.sh (two hardcoded strings that were the only thing actually
# routing anything).
#
# THE VOCABULARY COLLISION THIS RESOLVES. eng-trigger.sh called opus
# "HOP_MODEL_REASONING" while settings.yaml calls sonnet "reasoning". Same word,
# two different models, in two files that both claimed to route models. Anyone
# reading both would have been wrong about one of them. settings.yaml wins
# because CLAUDE.md says it does:
#
#   classification -> haiku    tagging, extraction, log scans, arithmetic
#   reasoning      -> sonnet   drafting, analysis, judgment
#   complex        -> opus     deep reasoning, generation quality, the gates
#
# eng-trigger.sh's two variables now resolve through here and keep their values
# (opus, sonnet), so its behaviour and its tests are unchanged — only the place
# the strings come from moved.
#
# Fails soft on purpose: an unreadable settings.yaml returns the built-in
# default rather than nothing, because every caller is on a production path
# where "no model" is worse than "the documented default".

set -uo pipefail

# Ported from life-os 2026-08-24. $ENG_DEPT wins over $LIFE_OS: this copy lives
# in the department template, and a stray LIFE_OS inherited from a parent process
# would otherwise point it back at life-os's settings.yaml and silently apply
# another repo's model mapping to this business's passes.
ROOT="${ENG_DEPT:-${LIFE_OS:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}}"
# business-os carries no config/settings.yaml, so read_tier finds nothing and
# every lookup falls through to fallback_for below. That is the intended state,
# not a defect: the tier→model mapping is not configurable per business yet, and
# the built-ins ARE the documented defaults. Add a `models:` block here to make
# it configurable — nothing else needs to change.
CFG="$ROOT/config/settings.yaml"

# Built-in fallbacks — must stay identical to the settings.yaml block above.
fallback_for() {
  case "$1" in
    classification) printf 'haiku\n' ;;
    reasoning)      printf 'sonnet\n' ;;
    complex)        printf 'opus\n' ;;
    *)              return 1 ;;
  esac
}

read_tier() {
  # Shallow parse of the top-level `models:` block. Same style as
  # read_plan_budget in lib/eng-trigger.sh: no yq, no python, two lookups.
  local tier="$1"
  [ -f "$CFG" ] || return 1
  awk -v want="$tier" '
    /^models:[[:space:]]*$/ { in_block=1; next }
    in_block && /^[^[:space:]#]/ { in_block=0 }          # next top-level key ends it
    in_block {
      line=$0
      sub(/#.*/, "", line)                                # strip trailing comment
      if (match(line, /^[[:space:]]+[a-z_]+:/)) {
        key=line; sub(/:.*/, "", key); gsub(/[[:space:]]/, "", key)
        val=line; sub(/^[^:]*:/, "", val); gsub(/[[:space:]]/, "", val)
        if (key == want && val != "") { print val; exit }
      }
    }
  ' "$CFG"
}

if [ "${1:-}" = "--list" ]; then
  for t in classification reasoning complex; do
    printf '%s\t%s\n' "$t" "$( { read_tier "$t" | grep . ; } 2>/dev/null || fallback_for "$t")"
  done
  exit 0
fi

TIER="${1:-}"
if [ -z "$TIER" ]; then
  echo "usage: model-tier.sh <classification|reasoning|complex> | --list" >&2
  exit 1
fi

# `none` is a real answer: the routine runs no LLM at all.
if [ "$TIER" = "none" ]; then
  exit 1
fi

VAL="$(read_tier "$TIER" 2>/dev/null | head -1)"
if [ -n "$VAL" ]; then
  printf '%s\n' "$VAL"
  exit 0
fi

if fallback_for "$TIER"; then
  exit 0
fi

# Unknown tier. Print nothing and fail — the caller decides whether to inherit
# the account default or treat it as an error. Never guess a model.
exit 1
