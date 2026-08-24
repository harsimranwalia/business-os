#!/bin/bash
# lib/agent-version.sh <agent-name> [--verbose|--history|--resolve <vN>]
#
# Prints a derived version string for one agent: v{commits}-{sha}, e.g. v47-a3f9c21.
#   --history          every version, newest first: vN <sha> <date> <subject>
#   --resolve <vN>     the sha for that version, so rollback has a target
#
# DERIVED, never typed. A hand-maintained `version:` field across 23 agents is a
# recurring manual step, and a recurring manual step is a design failure in this
# system (CLAUDE.md, prime directive). So the version is computed from git
# history scoped to the agent's OWN paths — which is the thing a repo-wide
# commit SHA cannot tell you. A commit touching twelve files across sales and
# cfo bumps exactly those two agents and leaves the other twenty-one alone.
#
# THE ROLLBACK UNIT IS THE AGENT'S DIRECTORY, NOT ITS DEPENDENCIES.
# `skills/` is deliberately excluded from the path scope. skills/outreach-drafter/
# is shared between sales and hiring; folding it into the sales version would
# mean a hiring-driven edit silently bumps sales, and rolling sales back would
# drag hiring's skill with it. Shared skills need their own version line. That
# is a real limit of this scheme, stated here rather than papered over.
#
# Consumed by lib/vps-cron.sh (stamps every cost record) and by the rollback
# tooling. Safe to call from anywhere; never fails the caller.

set -uo pipefail

AGENT="${1:-}"
if [ -z "$AGENT" ]; then
  echo "usage: agent-version.sh <agent-name> [--verbose]" >&2
  exit 1
fi
VERBOSE="${2:-}"

# Ported from life-os 2026-08-24. Resolves to $ENG_DEPT — the DEPARTMENT, not the
# instance — because an agent's version is a property of the shared template that
# defines it, not of the business it is currently acting for. `agents/eng-manager`
# exists under the department, and the department is inside the business-os repo,
# so the `git log -- $DIR` below reports the template's own history.
#
# $ENG_DEPT wins over $LIFE_OS for the same reason as model-tier.sh: an inherited
# LIFE_OS would send this at life-os's agents and report another repo's version.
LIFE_OS="${ENG_DEPT:-${LIFE_OS:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}}"
cd "$LIFE_OS" 2>/dev/null || { echo "unknown"; exit 0; }

DIR="agents/$AGENT"

# An unmapped or deleted agent is not an error worth failing a cron run over.
if [ ! -d "$DIR" ]; then
  echo "unknown"
  [ "$VERBOSE" = "--verbose" ] && echo "no such agent directory: $DIR" >&2
  exit 0
fi

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "nogit"
  exit 0
fi

# A shallow clone makes the commit COUNT a lie — Coolify clones from GitHub and
# a depth-1 checkout would report v1 for every agent forever, and would make
# rollback impossible because the history to roll back to is not present.
# Report it in-band rather than emitting a confidently wrong number.
SHALLOW=""
if [ "$(git rev-parse --is-shallow-repository 2>/dev/null)" = "true" ]; then
  SHALLOW="shallow"
fi

SHA="$(git log -1 --format=%h -- "$DIR" 2>/dev/null)"
if [ -z "$SHA" ]; then
  # Directory exists but nothing has ever been committed under it.
  echo "v0-none"
  exit 0
fi

if [ -n "$SHALLOW" ]; then
  echo "v?-$SHA"
  [ "$VERBOSE" = "--verbose" ] && echo "shallow clone: commit count unavailable, rollback unavailable" >&2
  exit 0
fi

COUNT="$(git log --format=%h -- "$DIR" 2>/dev/null | wc -l | tr -d ' ')"

# --history / --resolve exist so rollback has something to aim at. A version is
# only useful if you can name an earlier one and get back to it; without these
# "v27" is a label with no inverse.
if [ "$VERBOSE" = "--history" ]; then
  # Oldest commit is v1, so the Nth from the end is vN. git log is
  # newest-first, hence counting down.
  n="$COUNT"
  git log --format='%h%x09%ad%x09%s' --date=short -- "$DIR" 2>/dev/null | while IFS="$(printf '\t')" read -r h d subj; do
    printf 'v%s\t%s\t%s\t%s\n' "$n" "$h" "$d" "$subj"
    n=$((n - 1))
  done
  exit 0
fi

if [ "$VERBOSE" = "--resolve" ]; then
  want="${3:-}"
  [ -n "$want" ] || { echo "usage: agent-version.sh <agent> --resolve <vN|vN-sha|sha>" >&2; exit 1; }
  # Accept v27, v27-aaf0eb3, or a bare sha — a human reading a cost report has
  # the middle form in front of them and should not have to strip it.
  case "$want" in
    v*-*) printf '%s\n' "${want#*-}"; exit 0 ;;
    v*)
      idx="${want#v}"
      case "$idx" in (*[!0-9]*|"") echo "not a version: $want" >&2; exit 1 ;; esac
      [ "$idx" -ge 1 ] 2>/dev/null && [ "$idx" -le "$COUNT" ] || {
        echo "no $want for $AGENT (has v1..v$COUNT)" >&2; exit 1; }
      # vN is the Nth commit counting from the oldest.
      git log --reverse --format=%h -- "$DIR" 2>/dev/null | sed -n "${idx}p"
      exit 0 ;;
    *) printf '%s\n' "$want"; exit 0 ;;
  esac
fi

echo "v${COUNT}-${SHA}"

if [ "$VERBOSE" = "--verbose" ]; then
  echo "agent:   $AGENT" >&2
  echo "paths:   $DIR" >&2
  echo "commits: $COUNT" >&2
  echo "head:    $(git log -1 --format='%h %ad %s' --date=short -- "$DIR" 2>/dev/null)" >&2
fi
exit 0
