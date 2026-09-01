#!/bin/sh
# install.sh — instantiate the marketing department for one business.
#
#   ./install.sh <business> [--approver NAME] [--apply]
#
# Dry-run by default: prints every path it would create and writes nothing.
# Pass --apply to actually create the instance.
#
# Deliberately the same shape and the same flags as
# departments/engineering/install.sh. A business that runs both departments
# should install them the same way.
set -eu

DEPT="$(CDPATH= cd -P -- "$(dirname -- "$0")" && pwd -P)"
BUSINESS_OS="$(CDPATH= cd -P -- "$DEPT/../.." && pwd -P)"
VERSION="$(cat "$DEPT/VERSION")"

BUSINESS=""; PRINCIPAL="approver"; APPLY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --apply) APPLY=1 ;;
    --approver) shift; PRINCIPAL="${1:?--approver needs a name}" ;;
    -*) echo "unknown flag: $1" >&2; exit 2 ;;
    *) BUSINESS="$1" ;;
  esac
  shift
done
[ -n "$BUSINESS" ] || { echo "usage: ./install.sh <business> [--approver NAME] [--apply]" >&2; exit 2; }

INST="$BUSINESS_OS/instances/$BUSINESS/marketing"
KNOW="$BUSINESS_OS/instances/$BUSINESS/knowledge"
[ "$APPLY" -eq 1 ] || echo "DRY RUN — nothing will be written. Re-run with --apply."
echo "template : $DEPT (v$VERSION)"
echo "instance : $INST"
echo "approver : $PRINCIPAL"
echo

if [ -e "$INST" ] && [ "$APPLY" -eq 1 ]; then
  echo "REFUSING: $INST already exists. Delete it deliberately, or pick another name." >&2
  exit 1
fi

# Mirrors config/conventions.yaml -> instance_layout. If you add a directory
# there, add it here — an instance missing a declared directory sends every
# pass looking for a path that is not there.
DIRS="inbox inbox/requests inbox/_handled traces reports
content content/drafts content/ready-to-send content/approved content/shipped
content/images content/carousels content/series
voice voice/samples
performance
proof proof/case-studies proof/internal
agents/cmo/config agents/cmo/notebook
agents/campaign-strategist/config agents/campaign-strategist/config/channels agents/campaign-strategist/notebook
agents/content-writer/notebook
config config/channels"

if [ "$APPLY" -eq 1 ]; then mkdir -p "$KNOW"; else echo "  mkdir ../knowledge"; fi

for d in $DIRS; do
  if [ "$APPLY" -eq 1 ]; then mkdir -p "$INST/$d"; touch "$INST/$d/.gitkeep"; else echo "  mkdir $d"; fi
done

emit() { # emit <relative-path> — content on stdin
  _p="$1"
  if [ "$APPLY" -eq 1 ]; then cat > "$INST/$_p"; else echo "  write $_p"; cat >/dev/null; fi
}

emit config/instantiated-from <<EOF
$VERSION
EOF

emit config/config.yaml <<EOF
# Instance overrides for $BUSINESS. The template supplies every default;
# this file only records what is true for this business.

business: $BUSINESS
instantiated_from: $VERSION

# The single human with gate authority. Owns M1 strategy, M2 the piece, and
# M3 channel autonomy. The five machine gates stay machine-owned and blocking.
approver:
  name: $PRINCIPAL
  notify: telegram

# Humans who may file a topic but hold no gate authority. Their topics land in
# inbox/requests/ with \`source: filer\` and are drained by the CMO at planning.
filers: []

# Pause switch for THIS business only. sabbath | retreat | quiet halt every
# pass for this instance; empty means normal operation. Falls back to MODE in
# business-os/.env when empty, so the global switch still stops everything at
# once — this only adds the ability to stop one business without the rest.
mode:

# ---------------------------------------------------------------------------
# Channels.
#
# A channel is a playbook plus a row here — never a new agent. Adding one means
# writing config/channels/{name}.md and adding it below.
#
# Every channel starts at C1 (draft, no publishing path) and moves up only when
# the approver says so — that is gate M3. C1 is not a resting place: a draft
# with nowhere to go is a dead end, so a channel left here needs a live reason
# and a date.
#
# NOTHING IS SHIPPED UNTIL YOU EDIT THIS. That is deliberate. An installer that
# armed a publishing path would publish to an account nobody had confirmed.
# ---------------------------------------------------------------------------
channels: {}
  # Worked example — delete the braces above and uncomment to use:
  #
  # linkedin:
  #   enabled: true
  #   autonomy: c2              # c0 observe | c1 draft | c2 approve-to-ship | c3 autoship
  #   playbook: config/channels/linkedin.md
  #   weekly_plan:
  #     post_count: 3
  #     # THIS is the cadence and it is the only place it lives. The ship skill
  #     # reads this list every run and stops on any day not in it, so changing
  #     # cadence is an edit here and nothing else — no scheduler to reconfigure.
  #     publishing_days: [tuesday, thursday]
  #     publishing_time: "08:00"
  #   publishing:
  #     method: api             # api | browser | manual — see conventions.yaml
  #     credential_env: LINKEDIN_TOKEN   # the NAME of an env var. Never a value.
  #     account_ref:            # the author/page this publishes as
  #     require_approval: true  # M2. Do not set false without an M3 decision.
  #   voice:
  #     register: long-form-post
  #     floor: 10
  #     current_samples: 0      # honest count — update as samples are added

# Delivery caps. Raising these is the approver's call.
limits:
  pieces_per_channel_per_day: 1   # a thread or carousel counts as ONE piece
  awaiting_approval_cap: 5        # pieces queued for M2 at once
EOF

emit config/channels/README.md <<'EOF'
# Channel playbooks

One file per live channel, named for the channel. A playbook is MECHANICS
only — it is the reference for how a channel works, never for what to say on
it.

| Belongs here | Belongs elsewhere |
|---|---|
| Format limits, and how they are counted | What to say — the campaign strategist |
| Cadence, and the evidence for those slots | Positioning — the CMO |
| The publishing path, and how a publish is verified | This week's plan — the weekly plan |
| What is known to work on this channel | Voice — `voice/guide.md` |
| Hashtag and mention conventions | |
| Current performance baselines, or an honest "none yet" | |

Two rules learned the hard way:

**Never invent a baseline.** A channel that has shipped nothing has no
baseline, and writing a plausible number here means every later comparison is
against fiction. Write "none yet — nothing has shipped" and leave it.

**Cadence evidence, not just cadence.** A playbook that says "Tuesday and
Thursday" and not why cannot be argued with, so it never gets revisited. One
that cites what it was based on can be.

The template ships two example playbooks under
`$MKT_DEPT/agents/campaign-strategist/config/channels/`. Copy one as a
starting point; it is an example of the shape, not a description of your
channel.
EOF

emit voice/guide.md <<'EOF'
# Voice guide

**Fill this in before the first draft.** Every writing skill reads this file,
and a draft written without it comes out competent and generic — correct
sentences that sound like nobody. That is the specific failure this department
exists to avoid, and it is not fixable at review time.

Write it about the BUSINESS, not about a writing style you admire.

## Words and phrases we use

_Actual words from actual published material. Not aspirations._

## Words and phrases we never use

_The list that does the most work. Be specific and be ruthless — "leverage",
"unlock", "in today's fast-paced world". Every entry should be a phrase
somebody would otherwise write._

## The fingerprint

_How the writing is built, not how it feels. Sentence length. Whether it opens
with a claim or a scene. Where the business outcome sits — first line or last.
Active or passive. Whether it hedges. Whether it uses questions._

## The structure that works

_The shape a good piece takes here. If a contrarian reframe is the move, say
how much of the piece is spent naming the wrong approach versus the better
one — the ratio matters more than the technique._

## What we never claim

_Guardrails. Claims the business cannot back, positions it will not take,
competitors it will not name, topics that are off limits._

## Registers

_One per channel format. A long-form post and a 280-character unit are
different registers, not the same voice at different lengths, and each needs
its own samples in `voice/samples/{register}.md`._
EOF

emit voice/samples/README.md <<'EOF'
# Voice samples

One file per register, named for the register — `long-form-post.md`,
`short-post.md`, `thread.md`, `article.md`. Each holds real published pieces
in the business's own voice, verbatim.

**The floor is 10 per register.** Below it the department still drafts; it
leans harder on the review pass and on the approver's M2, and the channel's
`current_samples` in `config/config.yaml` records the gap so it is visible
rather than discovered.

Three rules, each of which has cost somebody something:

**Real published material only.** Not a description of the voice, not a piece
written to demonstrate the voice. What is being calibrated is rhythm and
shape, and only real material carries those.

**Match the register.** Long-form samples cannot calibrate a 280-character
unit. Borrowing across registers is defensible for tone and fingerprint, never
for shape, and a skill that does it must say so out loud.

**Check what the account actually contains before seeding from it.** An
account with hundreds of posts can still have almost nothing usable — if its
live register is personal and its professional material is five stale link
shares, seeding from it pulls drafts AWAY from the business's voice. Read
before you harvest.

The corpus grows from the front: every piece the approver publishes is a
candidate sample, which means it can only ever contain material already
approved of. A fresh instance starting empty is the normal case, not a fault.
EOF

emit content/topic-bank.md <<'EOF'
# Topic bank

The queue the CMO plans from. Read on every planning run. Anyone may add;
`inbox/requests/` drains into here at planning.

## Format

`- **{archetype}** | {topic} | {why it fits} | {priority: high|medium|low}`

An archetype of `unset` is fine and is the right default when the topic
arrives as a thought rather than a plan — classifying it is the CMO's job.

## Queued topics

_(empty — a first planning run with an empty bank will mine the business
profile and any proof entries instead, which works but produces safer, more
generic topics than a bank with real material in it.)_

---

## Blocked topics

Topics that are not to be written, and why. A reason here saves the same topic
being re-proposed every quarter.

| Topic | Why not | Reconsider when |
|---|---|---|

---

## Used

Moved here when a topic ships, with the piece that used it. Never deleted — a
topic quietly reused reads as one story told twice.

| Topic | Shipped as | Date |
|---|---|---|
EOF

emit performance/baselines.md <<'EOF'
# Performance baselines

Per-channel baselines, written by `engagement-analyzer` from real collected
data. **Never write a number here by hand, and never estimate one.**

A channel with nothing shipped has no baseline. The honest entry is "none yet
— nothing has shipped on this channel", and it stays that way until real data
exists. A plausible placeholder is worse than a blank: every later comparison
silently measures against fiction, and nothing about the output looks wrong.

| Channel | Window | Baseline | Piece count | Updated |
|---|---|---|---|---|
| _(none yet)_ | | | | |
EOF

emit proof/README.md <<'EOF'
# Proof

Evidence — real work with a real outcome, structured so it can be pulled into
a piece later. Not publish-ready content, and not voice: this is what the
business can prove.

Two branches, split by one question — **is there a client on the other end?**

**`case-studies/`** requires all three: a named or anonymised client, a real
problem, and a MEASURED outcome (hours saved, revenue up, cost down,
time-to-X down). Missing any one of them, it is not a case study. Mark it
`status: pending` or file it as internal rather than publishing it as proof.

**`internal/`** is the same shape without a client or a business metric. Real
work, real difficulty, still proof of capability — an internal build, a hard
call, a system that had to be designed. Usable in content, just never as a
client outcome.

Getting this split wrong is what turns an evidence library into a claims
library, and it is not recoverable once a piece has shipped on it.

## Also read, never written

`../engineering/reports/proof/` — proof-of-work entries written by the
engineering department for this same business. Marketing reads them and never
writes there. Engineering owns what it built; marketing owns what gets said
about it.

## When a piece uses an entry

Record it on the entry. Proof reused silently across three posts reads as one
story told three times, and by the time that is obvious it has already shipped.
EOF

emit inbox/requests/README.md <<'EOF'
# Filed requests

Topics filed by someone who is not the approver. Each carries `source: filer`
and the filer's name. The CMO drains this directory into the topic bank at
planning and treats them like any other topic — no priority, no fast path.

A filer never approves a piece and never appears in the publishing path. That
boundary is what makes filing cheap: anyone can drop an idea here without it
becoming a commitment on anyone.
EOF

if [ "$APPLY" -eq 1 ]; then
  if [ -f "$KNOW/business-profile.md" ]; then
    echo "  ../knowledge/business-profile.md already exists — left alone"
  else
    cat > "$KNOW/business-profile.md" <<PROFILE
# Business Profile — $BUSINESS

**Fill this in before the first planning run.** The CMO and campaign
strategist read this file when deciding positioning, ICP and what is worth
publishing. A CMO that cannot say what the business does will approve anything
that sounds professional.

Shared with the engineering department if one is installed for this business —
one description, not two that drift.

**Business:** <what it is, what it sells, who it serves>

**Customers:** <who pays, and for what>

**What good looks like:** <the outcome the business is actually optimising
for. For marketing this is rarely impressions — name the thing further down
the funnel that actually matters>

**Out of scope:** <what this business does not do — the boundary that lets the
CMO say no to a topic that sounds plausible>
PROFILE
    echo "  wrote ../knowledge/business-profile.md (stub — fill it in)"
  fi
else
  echo "  write ../knowledge/business-profile.md"
fi

echo
if [ "$APPLY" -eq 1 ]; then
  echo "Instance created. Validating…"
  fail=0
  for d in $DIRS; do
    [ -d "$INST/$d" ] || { echo "  MISSING: $d" >&2; fail=1; }
  done
  # Every file a first pass reads. A missing one is not a crash — it is a pass
  # that quietly proceeds without the thing it needed, which is worse.
  for f in config/config.yaml config/instantiated-from voice/guide.md \
           content/topic-bank.md performance/baselines.md; do
    [ -f "$INST/$f" ] || { echo "  MISSING: $f" >&2; fail=1; }
  done
  [ -f "$KNOW/business-profile.md" ] || { echo "  MISSING: ../knowledge/business-profile.md" >&2; fail=1; }
  if [ "$fail" -ne 0 ]; then
    echo "install: FAILED — instance is not valid." >&2; exit 1
  fi
  echo "install: exit 0 — instance is valid."
  echo
  echo "Next, in this order — each one is load-bearing:"
  echo "  1. Fill in ../knowledge/business-profile.md."
  echo "  2. Fill in voice/guide.md."
  echo "  3. Put REAL published material in voice/samples/{register}.md."
  echo "     This is the step people skip and the one that decides whether the"
  echo "     drafts are usable. Ten per register is the floor."
  echo "  4. Register channels in config/config.yaml and write a playbook for"
  echo "     each in config/channels/. Nothing publishes until you do — the"
  echo "     installer deliberately arms no publishing path."
  echo "  5. Run with MKT_DEPT=$DEPT MKT_INSTANCE=$INST"
else
  echo "DRY RUN complete. Re-run with --apply to create it."
fi
