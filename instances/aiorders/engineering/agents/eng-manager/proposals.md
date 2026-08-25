# Proposals

Things the department thinks are worth building and is **not allowed to build
until the approver says so.** Agent-originated findings land here rather than
shaping straight into tickets: no id, no board row, nothing sequenced.

See `schedules/eng_build_loop.md` step 3.

## How this works

| | |
|---|---|
| **Who writes here** | Any agent — QA, security, devops, the architect, the EM |
| **What becomes a ticket** | Only a proposal the approver has approved |
| **How they see it** | One batched G1 in the weekly report — never a per-item ping |
| **What happens to silence** | Nothing. It stays listed, is re-surfaced weekly, and expires after 30 days |
| **The one bypass** | A **P0 on a registered project** — production down or actively exploitable, with real users — goes straight to a ticket |

Silence is not approval, and an unapproved proposal is not a rejection. Expiry
is the terminus, chosen deliberately over a queue that only grows.

## Open

| Filed | By | Project | What | Why it matters | Size |
|---|---|---|---|---|---|
| 2026-08-25 | product-manager | aiorders | `agents/critic/agent.md` doesn't exist at the department or instance level, though `skills/prd-writer/SKILL.md` step 8b requires every G1 item to carry a dissent pass from it before reaching the approver. Confirmed absent at both `departments/engineering/agents/critic/` and this instance's `agents/critic/` — not a config gap, the agent itself was never ported. | Every G1 raised since the 2026-08-22 life-os port (including this pass's own ENG-002 G1) has gone to the approver with no counter-case attached — `docs/engineering-team.md` describes the critic seat as already wired, which is stale. Either port the agent or drop the step 8b reference; leaving both in place means the gap repeats silently on every G1. | S |
| 2026-08-25 | eng-manager | aiorders | `lib/eng-notify.sh` has two separate correctness bugs, both confirmed by reading the full script and by this pass's own live call. **(1) No channel dispatch:** it posts unconditionally to Slack via `SLACK_WEBHOOK_URL`, with no reference anywhere to `config/config.yaml` or a `telegram`/`slack`/`none` branch, even though `departments/engineering/config/conventions.yaml` documents exactly that seam ("the instance's config decides where that goes") and this instance's own `config/config.yaml` sets `approver.notify: telegram`. **(2) A variable collision breaks `stall` and `nudge`:** the script's own `MODE` (set from `$1` — `raise`/`nudge`/`stall`) is silently overwritten a few lines later when it sources `eng-env.sh`, which sources `$BUSINESS_OS_ROOT/.env` — and that file defines an unrelated `MODE=active` (the sabbath/retreat/quiet pause switch, same variable name, different purpose). Confirmed live: this pass's own `eng-notify.sh raise ...` call logged `sent: active`, not `sent: raise`. Since `$MODE` is never actually `stall` or `nudge` after the clobber, `if [ "$MODE" = "stall" ]` (line 92) can never match — `eng-notify.sh stall` currently falls through to the generic item-lookup, finds no item (stall passes none), logs `no such item:`, and exits 0 having sent nothing — and `[ "$MODE" = "nudge" ]` (line 130) can never match either, so a 24h nudge is sent with no `_Still waiting_` prefix, indistinguishable from a fresh raise. | The gate-notification mechanism is the one thing standing between a decision and it "just sitting there" (the script's own stated purpose), and the department's own runaway-guard design (`schedules/eng_build_loop.md` step 7) depends on the stall alert specifically to make "the board has stopped" a state change someone is told about rather than a silent freeze. Bug (2) means that alert has never once fired, on any instance running this script, regardless of channel. Bug (1) compounds it: if Harry is watching Telegram (per his own config, and the working Telegram integration already used elsewhere in this repo for the Reddit/marketing side) rather than a Slack `#life-os` channel, then even the raise/nudge messages that *do* send successfully — including this pass's own `ENG-003` raise — may not be reaching him where he's actually looking. Fix (2) is a five-minute rename (the clobbered local variable just needs a name that doesn't collide with the sourced `.env`'s `MODE`); fix (1) is the larger piece — real channel dispatch, and for `telegram` specifically, reply-routing back into `approve`/`reject`/`changed` decisions, which nothing here has built yet. | M |

## Approved

Moved here with its ticket id when the approver approves it. The row leaves
Open; it is never deleted.

| Filed | Approved | Ticket | Project | What |
|---|---|---|---|---|
