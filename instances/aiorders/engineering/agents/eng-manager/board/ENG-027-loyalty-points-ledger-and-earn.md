---
id: ENG-027
title: Loyalty points ledger, balances, and earn API — online-order and dine-in accrual
project: aiorders-api
type: feature
size: L
time_estimate: several days to a week
time_spent:
time_remaining:
severity: P3
priority: now
state: verified
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-03
updated: 2026-09-08
branch:
depends_on: [ENG-006, ENG-007]
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-027-loyalty-points-ledger-and-earn.md
  design: agents/architect/designs/ENG-027-loyalty-points-ledger-and-earn.md
  adrs: ["ADR-021"]
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

`ENG-006` (identity) and `ENG-007` (per-restaurant rates) are both shipped
and verified, and both are inert: there's an identity with nothing to
award and a rate table with zero rows that nothing reads. No part of the
loyalty program is observable yet, and the vendor currently holding
restaurants' existing points (Walletly) is being retired with nothing of
AIOrders' own to replace it.

## Outcome

A diner with a verified platform identity accumulates points at a
restaurant when they order online there, and when a staff member records a
dine-in amount for them — each computed against that restaurant's own
earn rate as it stood at that moment, into a balance specific to that
restaurant. Every credit is a permanent, append-only ledger entry.
Balances and history are readable per diner per restaurant. Nothing can be
spent yet — points only go up.

## Notes

Item 3 of `ENG-006`'s approved five-ticket loyalty sequence, filed per the
approver's own **yes** on the standing continuation question
(`inbox/2026-08-30-eng007-continue-sequence-question.md`, decided
2026-09-01T17:02:39Z) — not agent-invented scope, per
`eng_build_loop.md` step 3's carve-out for a PRD's own already-approved
sequence. No fresh request-readback run: there's no raw ambiguous input
here, the scope was already precisely named in `ENG-006`'s own PRD and
approved as a whole shape.

~~**Sized `M`, not `L`.**~~ **Superseded 2026-09-03** — the G1 came back
`changed` asking for accrual at fulfilment, and the ticket is now `L`. The
original note read: "One new record shape plus three thin surfaces …
What would push it to `L`: if accrual needs to fire on order *completion*
rather than *placement* — no completion/cancellation signal exists in the
system today, only the single `order_new` write path." The first half still
holds; the reason given for the `L` does not. AIOrders' own CloudWaitress
webhook registration already subscribes to `order_completed_updated`,
`order_cancelled_updated`, `order_cancel` and `order_update_status` — the
handler discards them at line 238. See the log entry below and the PRD's
"Approver's `changed` response" section.

~~**Branch: shared, not per-ticket.** Per the approver's own instruction
recorded on `ENG-006`'s ticket and restated on `ENG-007`'s (lines
109–113), the whole loyalty sequence shares one branch, `loyalty-system`,
in `aiorders-api`. Whoever picks this up at `building` branches from (and
merges back into) `loyalty-system`, not a fresh `feat/ENG-027-...` off
`main`.~~ **Superseded 2026-09-07** — true when written (2026-09-03), before
`ENG-006`/`ENG-007` had merged. Checked fresh at this ticket's own
work-breakdown pass: `origin/loyalty-system` is now an ancestor of
`origin/main` with zero unique commits — both predecessor PRs (`#2`, `#4`)
already merged individually — and `main` has moved 59 commits ahead of it
since. The shared branch has fully served its purpose; resuming it now would
mean rebasing 59 unrelated commits for no offsetting benefit. `ENG-048` and
`ENG-049` (this ticket's own sub-tickets) each branch fresh off `origin/main`
instead, same as every other work-breakdown sub-ticket on this board. Full
reasoning: `agents/eng-manager/notebook/2026-09-07-eng027-work-breakdown.md`.
Observation filed (`observations.md`, this date).

**Full lane, checked against the exclusion list rather than assumed.**
`type: feature` at `M` already fails the fast-lane size bar, and it also
trips schema (new tables), PII (a per-restaurant spend record tied to a
verified identity), and public-contract (a new authenticated staff
surface, plus a behaviour addition inside the live production order
webhook) independently.

~~**One rider on the G1** (same bar `ENG-015`/`ENG-016` used): what the earn
% applies to — proposed as the pre-tax, post-discount food subtotal,
excluding tax/fees/delivery/tip. `ENG-007` stored a percentage; nobody
has ever said a percentage of what. Still unanswered as of the rescope —
the `changed` answer addressed accrual timing and was silent on this, and
silence isn't read as approval, so it is carried forward onto the fresh G1
rather than treated as settled. Three further riders joined it there; see
the log entry below.~~ **Superseded 2026-09-05.** The fresh G1 carried four
riders in total — this one plus the auto-complete window length, which
moment's rate applies, and whether the order's own status column becomes
the completion signal. The approver's bare `approved` adopts all four
exactly as proposed: pre-tax, post-discount food subtotal; 24 hours; the
rate in effect at placement; the order's own status. See the log entry
below.

**Two risks flagged for the approver, not resolved here:** the Walletly
migration question (existing point balances aren't stored locally by the
current integration — a pure proxy — and become unreachable once that
contract lapses; a goodwill/business call, not this ticket's to make) and
the fact that `ENG-022` (`type: security`, `severity: P0`, cross-tenant PII
exposure on five live handlers, already `designed`) outranks this ticket
if the approver's attention is scarce this week — said plainly in the G1
rather than left for them to notice on their own.

**No dissent section** — `agents/critic/agent.md` still doesn't exist at
department or instance level, same gap `ENG-016`'s and `ENG-017`'s G1s
already logged; not re-filed as a second proposal, the open one
(`proposals.md`, 2026-08-25) already covers it.

## Log

- `2026-09-03` `intake → shaped → awaiting-scope` (product-manager,
  `scheduled` event pass, context `manual`) — gate-return step of a
  whole-board sweep: `inbox/2026-08-30-eng007-continue-sequence-question.md`
  came back `approved`/"yes" on 2026-09-01, naming this as item 3 of
  `ENG-006`'s sequence; not yet actioned by any intervening pass. Mode
  check clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`,
  whole-board: exit 0, clean.

  Delegated PM judgment (sizing, the filter, PRD/G1 drafting) to an `opus`
  subagent per `prd-writer/SKILL.md`'s own model designation, grounded in
  a fresh read of `ENG-006`'s sequencing section, `ENG-007`'s shipped
  schema and branch convention, and live `aiorders-api` code (confirmed:
  no order-completion signal exists, only `order_new`; the Walletly
  integration is a pure pass-through proxy storing nothing locally; no
  second repo needed since `brand-portal`'s existing auth gate covers
  staff-side dine-in entry).

  PRD written (`agents/product-manager/specs/ENG-027-loyalty-points-
  ledger-and-earn.md`) with an explicit readback-equivalent section citing
  what was actually approved (`ENG-006`'s named shape, its G1's sequence
  affirmation, and the standing question's own "yes") rather than
  inventing a customer quote that doesn't exist for this ticket. `next_id`
  incremented `ENG-027 → ENG-028` in the same edit that created this file.
  G1 raised: `inbox/2026-09-03-eng027-g1-scope.md`.

  **1 transition** (`intake → awaiting-scope` — shaping happens inline
  since there was no pre-existing ticket). `machine_wip` unaffected
  (`awaiting-scope` sits outside the counted range). Approver-facing WIP:
  rejoins/extends the count — this is the sequence's own approved
  continuation, not a fresh To-do-column start, per `ENG-006`'s G1 already
  blessing the whole shape; not blocked by the WIP-2 cap being over for
  the same reason tonight's `ENG-008`/`ENG-009`/`ENG-010`/`ENG-016`
  continuations weren't.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard doesn't fire on a ticket waiting on a human. Post-pass
  `lib/eng-gate-check.sh`, whole-board: see board index.

- `2026-09-03` **no state change — G1 answered `changed`, PRD rescoped in
  place, fresh G1 raised** (product-manager). Mode check clean
  (`MODE=active`). Same shape as `ENG-016`'s own rescope four hours
  earlier: the ticket goes straight back to the approver, it does not
  advance.

  **The answer** (`inbox/2026-09-03-eng027-g1-scope.md`, `decision:
  changed`, decided 2026-09-03T16:00:32.878229+00:00), in full: *"Accrual
  at fulfillment, have ticket completed as autocompleted after x hours if
  not cancelled or deleted."* Two clauses. The first takes the fork this
  ticket's own first G1 named explicitly (`M` → `L` if accrual moves to
  fulfilment); the second supplies the approver's own mechanism for the
  signal that fork said didn't exist.

  **What re-verification found — including that this department's own last
  G1 was wrong.** Read live against `~/Documents/projects/aiorders/
  aiorders-api` (read-only, no git operations) rather than trusting the
  first pass's evidence: the local `orders.status` really is written once
  at insert (`cloudwaitress.ts` `createOrder()` line 188, `status:
  orderData.status` line 195) and really is never updated or deleted
  anywhere — eleven `from('orders')` sites, ten selects, one insert, zero
  updates, zero deletes. **But the inference drawn from that last time —
  "there is no order-completion signal in the system" — does not hold.**
  AIOrders' own webhook registration constant (`cloudwaitress-middleware/
  handlers/restaurant.ts`, `AIORDERS_WEBHOOK` line 6, written into each
  restaurant's CloudWaitress account by `handleAddWebhook()` line 93)
  subscribes to nine events including `order_completed_updated`,
  `order_cancelled_updated`, `order_cancel` and `order_update_status` — and
  the handler discards every one of them at line 238. The fulfilment signal
  is already being delivered to production and thrown away. Two further
  supporting facts: scheduling is not new here (`pg_cron`/`pg_net` enabled
  and running two jobs; plus a shipped **per-order** 3-hour delayed
  callback, the feedback queue, on this same handler at line 274), and the
  authoritative status is readable on demand through the already-shipped
  `cloudwaitress-middleware` order proxy.

  **The gap named rather than papered over.** As the code stands, the
  approver's own condition — "if not cancelled or deleted" — is **vacuous**:
  nothing can mark an order cancelled, so a timer-only sweep credits every
  order X hours after placement, the same accrual-integrity exposure as the
  placement-based accrual they just rejected. **Resolution recommended:
  stop discarding the cancellation events**, which makes the condition real
  on the day it ships and is cheaper than either alternative considered — a
  from-scratch cancel-marking capability (ticket 5's admin surfaces are an
  explicit non-goal here), or a forward-compatible no-op `WHERE` clause,
  rejected because a check that can never fire is worse than inert: it
  looks like a safety property while being none. **"Deleted" has no signal
  and gets none** — no delete event in the subscription, no local path;
  said plainly rather than folded into "cancelled." And one thing left
  explicitly unresolved because code can't answer it: whether restaurant
  staff actually mark orders in the CloudWaitress dashboard at all. If they
  don't, the timer is the only mechanism and the cancellation branch never
  fires — a production-log question for design time, not a G1 blocker.

  **Sizing verdict: `L`, one ticket** — frontmatter `size` `M` → `L`,
  `time_estimate` → several days to a week. Derived fresh, not inherited
  and not rubber-stamped from the old `M → L` warning, whose stated reason
  ("that signal has to be built first") is exactly what the evidence above
  overturns. What earns the `L` is what sits on top of the original `M`:
  the first write-after-insert path on `orders` in this codebase's history,
  on the live production order webhook; a scheduled sweep with its own
  idempotency and failure semantics; and moving the accrual trigger point.
  **Not `XL`**, so it does not go back to be split
  (`prd-writer/SKILL.md` step 7) — one project, one new data model already
  in scope, no new vendor, no cross-repo surface. Splitting order-lifecycle
  from ledger was considered and rejected: it would ship a ledger crediting
  at the moment the approver just rejected.

  **Four riders on the fresh G1**, up from one: the auto-complete window
  ("x hours" is a literal unfilled placeholder — proposed **24 hours**,
  with the shipped feedback queue's **3 hours** named as the same-day
  alternative); **the earn-% base carried forward still open**, since the
  `changed` answer was silent on it and silence isn't approval; which
  moment's rate applies now that placement and accrual are hours apart
  (proposed: placement); and whether the order's own status becomes true or
  loyalty keeps a private view (proposed: the order's own — it also fixes
  the frozen status `brand-portal`'s order lists show restaurant owners
  today).

  PRD rescoped in place, original content marked superseded rather than
  deleted, per `ENG-016`'s precedent: a new "Approver's `changed` response"
  section with the five verified facts and the sizing verdict;
  Proposed change, Acceptance criteria (11 → 18, with 1/6/9 re-derived and
  2 explicitly left alone since dine-in has no fulfilment step), Non-goals,
  Risks, Cost, Recommendation and the 5-question filter all updated. Fresh
  G1 raised: `inbox/2026-09-03-eng027-g1-rescope.md`. Old G1 moved to
  `inbox/_handled/2026-09-03-eng027-g1-scope.md` as-is, no appended note
  (`ENG-016` precedent — the narrative lives in the PRD section, the fresh
  G1, and the journal row). Decision-journal row appended for the `changed`
  verdict.

  **No dissent section** — `agents/critic/agent.md` still doesn't exist at
  department or instance level, same gap this ticket's first G1 already
  recorded; not refiled, the open proposal (`proposals.md`, 2026-08-25 row)
  covers it.

  **0 transitions** — `awaiting-scope → awaiting-scope`, `owner: approver`
  throughout. This pass answered the gate return; it did not move the
  ticket. `machine_wip` unaffected (`awaiting-scope` sits outside the
  counted range). Approver-facing WIP unchanged — the same item goes back
  to the same desk, not a new one.

  **Notify sweep:** the fresh G1 is this pass's own gate item —
  `lib/eng-notify.sh raise inbox/2026-09-03-eng027-g1-rescope.md` run
  immediately, exit 0, confirmed in `traces/eng-notify-2026-09-03.log`
  (`13:15:26 sent`); `notified: 2026-09-03T13:15:26` stamped in the item's
  frontmatter. **Dead-end sweep (scoped to this event):** no other ticket
  touched, per this event's own narrower contract (act on the answered
  gate item, advance only the ticket it belongs to).

  Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-027`) and whole-board:
  see board index.

  `chained: none` — `awaiting-scope`, owner `approver`. The fresh G1 just
  raised is a new item waiting on the approver, not an agent-owned state;
  firing `continue ENG-027` would queue against a ticket with nothing left
  for a machine to do until it's answered, same reasoning every other
  awaiting-scope/G1-raised entry on this board already uses.

- `2026-09-05` **`awaiting-scope → designed`** (product-manager, `decision`
  event pass, context `inbox/2026-09-03-eng027-g1-rescope.md`). Reading map
  for `decision`: steps 4 and 8c, plus the not-negotiable set (1, 7, 8b, 9,
  10; *Enforced vs instructed*; *the four lanes*; *Guards*). Mode check
  clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, whole-board: exit
  0, clean.

  **The answer** (`decision: approved`, decided
  2026-09-05T17:01:12.758537+00:00): a bare approval, no additional
  comment. Read the same way this board already reads a silent rider or
  assumption (`ENG-016`'s, `ENG-019`'s, `ENG-020`'s, `ENG-021`'s and
  `ENG-026`'s own unremarked G1 answers, per `decision-journal.md`) — as
  accepting the recommendation exactly as proposed, not as overlooked:
  **build now, one ticket, `L`**, accrual on fulfilment driven by the
  CloudWaitress completion/cancellation events with the auto-complete timer
  as fallback, and all four riders adopted at their proposed default —
  24-hour auto-complete window; pre-tax, post-discount food subtotal as the
  earn base; the rate in effect at placement; the order's own status column
  becomes the completion signal rather than a private loyalty-side view.

  PRD frontmatter `status: awaiting-scope → approved`, `decided:
  2026-09-05T17:01:12.758537+00:00`, `## Decision` section filled in. Old
  G1 moved to `inbox/_handled/2026-09-03-eng027-g1-rescope.md` as-is, no
  appended note (`ENG-016`/`ENG-026` precedent — the narrative lives in the
  PRD, this log, and the decision journal, not a note bolted onto the raw
  item). Decision-journal row appended.

  **Handed to the architect for the tech design, not attempted inline** —
  same shape `ENG-016`'s and `ENG-026`'s own G1 approvals already used: a
  design is a heavy step that earns its own session
  (`eng_build_loop.md`, "The chain — why this isn't a cron job"), and
  `designed` is the state `tech-design/SKILL.md` triggers on, not a claim
  that the design already exists.

  **1 transition** (`awaiting-scope → designed`), under the cap of 4.
  `machine_wip` unaffected — `designed` sits outside the counted range
  (`ready`..`ready-to-ship`), same as `awaiting-scope` did. Approver-facing
  WIP: drops off the open count — no inbox file remains open for this gate
  (moved to `_handled/`), same shape `ENG-013`/`ENG-016`/`ENG-026` already
  set.

  **Dead-end sweep (scoped to this event):** no other ticket touched, per
  this event's own narrower contract (act on the answered gate item,
  advance only the ticket it belongs to). **Notify sweep:** no new gate
  item raised this pass — nothing to notify. No `exception-request:` on this
  ticket's log; no observation beyond what the decision journal already
  captures.

  business-os itself left uncommitted — same standing default carried by
  every pass since the last reconciliation commit; the commit-convention
  question remains open, not re-decided here.

  Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-027`) and whole-board: see
  board index.

  `chained: ENG-027` — fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-027`
  before this pass exits. `designed` is owned by the architect: not waiting
  on the approver, not blocked, not terminal, not capped by machine WIP.
  Named plainly rather than smoothed over: this fire was invoked twice in a
  row (checking the first call's exit code re-ran it rather than just
  inspecting `$?`), landing two `continue ENG-027` lines in
  `traces/.pending` behind two pre-existing `watch launchd` lines — both
  queued rather than launched, since this pass's own process held
  `traces/.loop.lock` throughout. Left as-is rather than hand-edited: the
  queue's own documented dedup ("Duplicate lines... collapse before each
  pop, keeping the oldest copy," `eng_build_loop.md`, "The chain") collapses
  it to one at the next drain, and editing `traces/.pending` by hand is a
  bigger risk than the duplicate it would fix.

- `2026-09-05` **`designed` — tech design written; routing held at
  `designed` rather than `ready`** (architect, `continue` event pass,
  context: resume `ENG-027` from its `designed` checkpoint). Reading map for
  `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10;
  *Enforced vs instructed*; *The four lanes*; *Guards*). Mode check clean
  (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  **This pass ran `tech-design/SKILL.md` in full**, which is what entering
  `designed` actually triggers — the checkpoint handed off by the prior pass
  was explicit that the design didn't exist yet. Read the PRD's acceptance
  criteria, `config/projects.md`'s hard constraints, both prior ADRs/designs
  this ticket depends on (`ENG-006` identity, `ENG-007` rate table), and
  investigated `aiorders-api` fresh against `origin/main` (`89c6fdb`) via
  `git show`/`git grep` rather than checking out the department's shared
  worktree — that worktree currently sits on `ENG-038`'s branch (merged
  during this same pass's investigation; already correctly `verified` on
  this board, not touched here). Re-verified, independently, four of the
  PRD's own load-bearing facts (the discard branch at
  `cloudwaitress.ts:238`, `createOrder()`'s exact insert columns, all nine
  `AIORDERS_WEBHOOK` subscriptions, the 3-hour `sendFeedbackQueueMessage`
  default) plus one fact the PRD didn't check: whether anything in this repo
  branches on `orders.status`'s string value (`git grep` across every
  `.eq('status', ...)` site — nothing does; only `onlineOrders.ts` passes it
  through display-only). Full reasoning, all citations, and the resulting
  shape: `agents/architect/designs/ENG-027-loyalty-points-ledger-and-earn.md`.

  **Shape, briefly:** one new table (`loyalty_ledger_entries`, balance
  computed as `SUM(points)` on read, no maintained counter); two additive
  `orders` columns (`cw_order_id`, `loyalty_processed_at`) closing the
  join-key gap the PRD named; one Postgres function
  (`credit_order_if_eligible`) called from both the webhook path and a new
  `pg_cron` sweep, giving idempotency via ordinary single-row locking rather
  than a lock table; the webhook handler un-ignores exactly three event
  types (`order_completed_updated`, `order_cancelled_updated`,
  `order_cancel`) and leaves `order_update_status` and the four
  booking/ready-time events discarded, unchanged; dine-in lands in
  `brand-portal` (staff-facing, `requireRestaurantAccess`), not
  `admin-portal` (platform-admin-facing, `ENG-007`'s own home). **`ADR-021`
  logged** (architect-decided, not escalated): the auto-complete sweep
  reuses `ADR-018`'s `pg_cron` + `net.http_post` batch-poller shape rather
  than `sendFeedbackQueueMessage`'s per-order Cloudflare Queue delay — this
  repo has no source for that mechanism's own maximum delay, and AC15's
  "batch keeps going, failed item retries next run" language is a
  claim-a-batch shape, not an independent-per-order-callback one. `next_id`
  in `agents/architect/decisions/_index.md` incremented to `ADR-022` in the
  same edit.

  **No one-way door escalated.** The four decisions that would otherwise
  have needed a G2 — window length, earn base, which rate, and whether
  `orders.status` itself becomes the signal — were already settled by the
  approver at this ticket's own second G1. `ADR-021`'s mechanism choice is
  reversible (`ADR-018`'s own "reversibility: cheap" framing applies
  identically) and is logged, not escalated. `links.design` and
  `links.adrs` set on this ticket's own frontmatter in the same pass.

  **Routing (step 11 of `tech-design/SKILL.md`): would be `ready` — held at
  `designed` instead.** Neither an L0 project nor a one-way door, so the
  skill's own routing reads `ready`, `owner: eng-manager`. **Machine WIP
  re-checked fresh from every ticket's own frontmatter, not a cached
  header: `1/1`, occupied by `ENG-019`** (`state: building`). Per this
  board's own standing precedent for exactly this situation (`ENG-014`,
  `ENG-017`, `ENG-023`, `ENG-025`, `ENG-029`, `ENG-030`, `ENG-035`, `ENG-036`
  are all currently sitting at `designed` with a completed design for the
  same reason — `ENG-020`'s own board-file log names the same pattern one
  pass earlier), `ENG-027` is **held at `designed`, owner staying
  `architect`**, rather than writing `state: ready` while the one slot is
  occupied — entering `ready` is what claims the slot, not being designed.
  Joins the held-for-slot pool. **Not first in line despite carrying
  `priority: now`**: `ENG-020`, `ENG-021` and `ENG-026` are also `now` and
  carry lower ids, so the board's own tie-break (lowest id among equal
  priority) puts each of them ahead of `ENG-027` when the slot frees —
  checked fresh this pass rather than assumed, precisely so the next
  dispatch-scoped pass doesn't have to re-derive it.

  **One observation filed** (`agents/eng-manager/observations.md`): the
  in-code comment on `cloudwaitress.ts`'s feedback-queue call says "5 second
  delay" while the actual default parameter is 3 hours (`3*60*60`) —
  harmless, noticed only because this ticket's own design needed to verify
  that exact delay value, not something this ticket touches or fixes.

  **Dead-end sweep (scoped to this event):** no other ticket touched, per
  this event's own narrower contract. **Notify sweep:** no new gate item
  raised this pass — nothing to notify. Checked all three open `inbox/`
  items fresh (current `2026-09-05T17:39:48Z`): `ENG-028` and `ENG-016`'s
  Piece-2 question have both already used their one-ever nudge;
  `ENG-039`'s merge request (`notified: 2026-09-05T03:41:22`) is ~14h old,
  under the 24h threshold. Nothing crosses it. No `exception-request:` on
  this ticket's log. **Journal:** n/a — no gate answered this pass, none
  raised either.

  **Board update:** In-flight row for `ENG-027` unchanged (`state`,
  `priority`, `owner`, `size` and `updated` were already `designed` / `now`
  / `architect` / `L` / `2026-09-05` — nothing in the summary row actually
  moved). New dated entry appended below; live file held three dated
  entries before this one — oldest (`ENG-039`, security gate round 1)
  rolled to `_index-archive.md` per the keep-three rule.

  business-os itself left uncommitted — same standing default carried by
  every pass since the last reconciliation commit; the commit-convention
  question remains open, not re-decided here.

  Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-027`) and whole-board: see
  board index.

  `chained: none` — held by the machine-WIP cap (`1/1`, `ENG-019`,
  `building`), one of the documented no-chain conditions. Re-check via a
  `decision`/`watch`/`scheduled` pass once the slot frees, or via a
  dedicated `continue ENG-027`.

- 2026-09-07 `designed → ready` (eng-manager, acting as `devops` for the
  triggering ticket, `continue ENG-047` event pass — this ticket is the
  slot-fill side effect of that pass's own chain obligation, not its own
  `continue` event). Reading map used by the driving pass: steps 6 and 6b,
  plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*;
  *The four lanes*; *Guards*). Mode check clean (`MODE=active`).

  **Why this ticket moved on someone else's pass.** `ENG-047`'s own
  release-readiness hop parked it on the approver (`ready-to-ship →
  blocked`), which freed the `ENG-026` family's machine slot. `ENG-047` was
  that family's last undispatched child — `ENG-044` shipped, `ENG-045` and
  `ENG-046` both already parked on the approver — so `eng_build_loop.md`
  Guards' 2026-09-07(b) amendment's "else the top of To-do" applied rather
  than a sibling fill. To-do (`ENG-018`/`ENG-028`/`ENG-042`/`ENG-043`) had
  nothing startable (all genuinely on an unanswered approver
  question/dependency, confirmed via `grep -n "^decision:" inbox/*.md`), so
  the pick fell back to the held-for-slot pool — same precedent `ENG-019`,
  `ENG-020`, `ENG-021` and `ENG-026` each already set for this exact
  situation.

  **This ticket won that pool outright, no tie-break needed.** Of the eight
  other `designed` tickets in the pool (`ENG-014`, `ENG-017`, `ENG-023`,
  `ENG-025`, `ENG-029`, `ENG-030`, `ENG-035`, `ENG-036`), none carries a
  `priority`; this ticket alone carries `priority: now`. Its own
  2026-09-05 entry had named `ENG-020`, `ENG-021` and `ENG-026` as the only
  `now`-priority designed tickets ahead of it by id — all three have since
  shipped/verified or (for `ENG-026`) dispatched their own last child this
  same pass, so none contends any more.

  **Both preconditions re-verified fresh, not carried forward from this
  ticket's own 2026-09-05 entry:** `depends_on: [ENG-006, ENG-007]` — both
  still `state: verified` (re-read directly, unchanged). One-way door — none;
  already settled at this ticket's own tech-design pass (2026-09-05): the
  four decisions that would otherwise have needed a G2 were already decided
  at this ticket's own second G1, and `ADR-021`'s mechanism choice is
  logged, reversible, and not escalated.

  **Routing:** `designed → ready`, `owner: architect → eng-manager`, no G2
  — reusing the determination already made and recorded at the 2026-09-05
  entry above, not re-derived. Machine WIP `0/1 → 1/1`.

  Stopped there — work-breakdown/building is new implementation work and
  belongs to its own session with fresh context, per *The chain* ("one
  Claude session that designs, builds, reviews, tests and security-reviews
  runs out of context and does all of it badly"). Chained instead.

  **6b:** not applicable — this transition reuses an already-recorded
  routing decision; no new instruction, state name, config key, or artifact
  path introduced.

  Full reasoning for the dispatch decision itself (To-do sweep, pool
  comparison, family-slot derivation) lives on `ENG-047`'s own board-file
  log and this same date's entry on `agents/eng-manager/board/_index.md` —
  not duplicated here beyond what this ticket's own record needs.

  `chained: ENG-027` — fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-027`
  before the driving pass exits. `ready` is owned by `eng-manager`: not
  waiting on the approver, not blocked, not terminal, not capped (this
  transition is what claims the one machine slot).

  business-os itself left uncommitted through this edit — standing default
  per the open commit-convention question, not re-decided here.

- 2026-09-07 `ready → building` — work-breakdown, two sub-tickets
  (eng-manager, `continue ENG-027` event pass, per the prior entry's own
  `chained: ENG-027`). Reading map for `continue`: steps 6 and 6b, plus the
  not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
  lanes*; *Guards*). Mode check clean (`MODE=active`). Pre-pass
  `lib/eng-gate-check.sh`, scoped (`ENG-027`) and whole-board: both exit 0,
  clean.

  Ran `work-breakdown/SKILL.md`. Autonomy check: `aiorders-api` is L1 —
  proceeds. Machine WIP re-checked fresh from every ticket's own frontmatter:
  `1/1`, held by `ENG-027` itself — `ENG-026` (`building`) is a settled
  container, every child either `shipped` or `blocked_on: approver`, none in
  `ready..ready-to-ship`, so it holds zero machine slots (Guards'
  2026-09-07(b) amendment). A ticket's own family isn't a second occupant of
  its own slot, same reading `ENG-016`/`ENG-019`/`ENG-021`/`ENG-026` already
  established, so work-breakdown proceeds.

  Split by the design's own `## Components` table into two owning-agent
  sub-tickets, both `aiorders-api` — `ENG-048` (`database`: new table
  `loyalty_ledger_entries`, `orders` +2 columns,
  `credit_order_if_eligible()`, `loyalty-auto-complete-tick` cron) and
  `ENG-049` (`backend`: webhook modifications, new `loyalty-auto-complete`
  edge function, two new `brand-portal` actions). No `frontend` sub-ticket —
  the design's own Rollout section states plainly that no frontend anywhere
  calls any of this yet. Sequenced as a strict chain: `ENG-048` first (no
  dependency), `ENG-049` `depends_on: [ENG-048]` (every one of its five
  components touches something `ENG-048` creates). Full reasoning, the
  18-criterion AC ownership mapping, and every field decided without an
  explicit rule:
  `agents/eng-manager/notebook/2026-09-07-eng027-work-breakdown.md`.

  **This ticket's own Notes carried a stale instruction, caught and
  corrected before either sub-ticket was written, not propagated.** The
  2026-09-03 "shared branch, `loyalty-system`" note was true when written
  but predates `ENG-006`/`ENG-007` merging it away — checked fresh in the
  shared worktree (without switching its own checkout, currently on
  `ENG-045`'s branch): `git merge-base --is-ancestor origin/loyalty-system
  origin/main` is true (zero unique commits), and `main` is 59 commits
  ahead of it since (`ENG-038`, `ENG-020`, `ENG-040`, `ENG-044`, `ENG-045`,
  others). Both predecessor PRs already merged individually — the shared
  branch fully served its purpose. Marked superseded in place, above,
  rather than silently overridden; both sub-tickets branch fresh off
  `origin/main` instead, matching every other work-breakdown sub-ticket on
  this board. Observation filed (`observations.md`, this date) rather than
  an exception-request — a technical fact from direct git investigation, not
  a scope or business call.

  **Routing:** `ready → building`, owner stays `eng-manager` — no engineer
  builds a two-surface parent with no diff of its own (`ready`'s exit
  condition, `definition-of-done.md`, is satisfied by the breakdown itself).
  `ENG-048` dispatched straight to `building`, owner `database` (no
  dependency). `ENG-049` stays `ready`, owner `eng-manager` (unmet
  `depends_on: [ENG-048]`).

  **1 transition** on this ticket (`ready → building`), well under the cap
  of 4. Machine WIP: still `1/1`, same family (`ENG-027` + `ENG-048`/
  `ENG-049`), not `2/1` — see notebook. No gate raised, no G1/G2/G3, no
  one-way door.

  **6b:** the branch correction above is exactly what this step exists to
  catch — a rule about an artifact (which branch a ticket builds against)
  fixed in the file someone thought of (this ticket's own Notes) rather than
  left to contradict a file that outranks it. No other artifact-mention
  sweep needed this hop: no new receipt path, state name, or config key
  introduced.

  **Dead-end sweep (scoped to this event):** no other ticket touched, per
  this event's own narrower contract.

  **Notify sweep:** nothing raised this pass — work-breakdown isn't a gate.
  Checked every open `inbox/` item fresh against local wall-clock
  `2026-09-07T13:37:31` PDT (not UTC — `observations.md`'s own 2026-09-06/07
  rows on this exact skew): `ENG-018`'s, `ENG-028`'s, `ENG-042`'s G1s,
  `ENG-043`'s clarification, and `ENG-016`'s continue-Piece-2 question all
  already carry their one-ever `nudged:` — no action. `PROP-2026-W36`
  already nudged — no action. `ENG-045`'s (~2h40m), `ENG-046`'s (~1h22m),
  and `ENG-047`'s (~21m) merge requests are all well under 24h — no action.

  **Observations/exceptions/journal:** one observation filed (branch
  staleness, above and `observations.md`); no `exception-request:`; no
  G1/G2/G3/merge-request answered this pass, so no decision-journal entry
  owed.

  **Board update:** In-flight table — this ticket's own row (`state:
  building`, `updated`); new rows added for `ENG-048`, `ENG-049`; header's
  `Next ID` advanced `ENG-048 → ENG-050` with a prose note, same convention
  every prior work-breakdown allocation on this board has used. Live
  `_index.md` held exactly three dated `## {date} —` entries — at, not
  over, the keep-three threshold, so nothing rolled to `_index-archive.md`
  this pass; this dispatch is recorded as a header-paragraph note, same
  convention `ENG-016`'s/`ENG-019`'s/`ENG-021`'s/`ENG-026`'s own
  work-breakdown dispatches already used, not a new dated entry.

  Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-027`, `ENG-048`,
  `ENG-049`) and whole-board: see board index.

  `chained: ENG-048` — the only child with a met dependency and something
  agent-actionable now. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-048`
  before this pass exits — confirmed queued, not dropped:
  `traces/.pending` shows `1 continue ENG-048` appended behind five
  already-outstanding events, behind this pass's own single-flight lock
  (`traces/.loop.lock`, pid `75800`), to drain the moment this pass exits.
  `chained: none` on `ENG-027` itself (parent, no action until a child
  reports back) and on `ENG-049` (unmet dependency), recorded on each
  ticket's own log.

  business-os itself left uncommitted through this edit — same standing
  default carried by every pass since the last reconciliation commit; the
  commit-convention question remains open, not re-decided here.

- `2026-09-07` **`continue` — re-verified idle, no action; `ENG-027` stays
  `building`** (eng-manager, `continue ENG-027` event pass). Reading map for
  `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10;
  *Enforced vs instructed*; *The four lanes*; *Guards*). Mode check clean
  (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped and whole-board:
  both exit 0.

  Container ticket, both children already dispatched; neither
  `shipped`/`verified`/`dropped` yet, so `ADR-003` keeps `ENG-027` at
  `building`. Re-verified fresh, not trusted off either child's own log:
  `ENG-048`/`ENG-049` both still `blocked`/`blocked_on: approver`, PRs
  `#21`/`#22` both `OPEN`, unmerged (`gh pr view`, `git merge-base
  --is-ancestor` against `origin/main`). Machine WIP re-swept whole-board:
  `0/1`, genuinely free. To-do re-swept: same four tickets
  `IDLE-2026-09-07` already named, none newly answered — that item stays
  open, accurate, and not duplicated. Notify sweep: nothing due. One
  observation filed (`observations.md`, this date). Full reasoning:
  `agents/eng-manager/notebook/2026-09-07-eng027-continue-recheck.md`.

  Post-pass `lib/eng-gate-check.sh`, scoped and whole-board: exit 0, clean.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 already open,
  re-verified accurate, not duplicated`.

  business-os left uncommitted — standing default, commit-convention
  question still open.

- `2026-09-07` **`continue` — idle re-confirmed, no transition** (eng-manager,
  `continue ENG-027`; drained `20:27:14`, right behind `_index.md`'s
  `2026-09-08 — scheduled (auto-drain)` entry). Gate check clean, pre/post,
  scoped + whole-board.

  No gate ran, no receipt written, no WIP/cap change: `ENG-048`/`ENG-049`
  still `blocked`/`blocked_on: approver`, PRs `#21`/`#22` still `OPEN`
  (`gh pr view`, fresh); Machine WIP still `0/1`; To-do's same four
  tickets still unanswered; `IDLE-2026-09-07` still accurate, not
  duplicated. Fourth consecutive pass reaching this conclusion since
  `19:52`.

  Process note (disclosed to the approver directly + `observations.md`):
  this pass's own `gh`/`git` checks ran from the human's checkout, not
  `_eng/`.

  Full reasoning: `agents/eng-manager/notebook/2026-09-07-eng027-continue-fourth-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (4th confirmation)`.

  business-os left uncommitted — standing default.

- `2026-09-07` **`continue` — eighth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`; `traces/eng-loop-2026-09-07.log`:
  prior `scheduled` pass ended `21:14:57` (exit 0, 373s, the seventh
  confirmation, logged in `_index.md`), this event drained `21:14:59`,
  launched `21:15:02` on `CLAUDE_CODE_OAUTH_TOKEN_2` — `day 53/200
  charged, 6 refunded today, ENG-027 5/20`, nowhere near either budget).
  Reading map for `continue`: steps 6 and 6b, plus the not-negotiable set
  (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*).
  Mode check clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`,
  scoped (`ENG-027`) and whole-board: both actually run this pass, exit 0.

  **This ticket's own file was last touched at the fourth confirmation** —
  the fifth through seventh ran as `scheduled` sweeps and logged centrally
  in `_index.md` instead, since neither touched a single ticket file. This
  pass's context is `continue ENG-027` specifically, so it resumes logging
  here, same convention confirmations one through four used.

  Re-verified fresh, nothing taken on any prior entry's word: `gh pr view
  21`/`22 --json state,baseRefName,headRefName,mergedAt` from the
  department's own `_eng/aiorders-api` worktree (not the human's checkout —
  the fourth confirmation's own process note, corrected there and every
  pass since) — both still `OPEN`, `mergedAt: null`, `#22` still stacked on
  `#21`'s branch. `ENG-048`/`ENG-049` frontmatter both still `blocked`/
  `blocked_on: approver`. Machine WIP read directly from every ticket's own
  frontmatter via the In-flight table: `0/1`, genuinely free — `ENG-027` is
  the sole `building` ticket and a container holding zero slots (Guards,
  2026-09-07(b)), both children parked on the approver. To-do (`ENG-018`,
  `ENG-028`, `ENG-042`, `ENG-043`) re-checked: `grep -n "^decision:"`
  against each one's own gate file in `inbox/` — none present, all four
  still genuinely unanswered, and all four already carry their one-ever
  `nudged:` stamp (`2026-09-07T09:37:5x`), so no further notify action is
  owed on them. No `priority: hold` ticket found sitting in a working
  state. `IDLE-2026-09-07.md` re-read in full: still accurate against every
  fact above; `notified: 2026-09-07T18:44:54`, under 24h old, no `nudged:`
  yet — not due, not duplicated.

  **Did not fall back to the `designed`-state pool (`ENG-050` included),
  and did not relitigate that question.** It is already an open proposal
  (`proposals.md`, 2026-09-07, devops row) awaiting the approver's batched
  decision; deciding it now, on an eighth pass, would be the department
  overriding its own open question rather than waiting on it. **Did not
  file a third observation or a second proposal on the repeated-idle
  pattern itself** — the eng-manager row already filed in `proposals.md`
  (2026-09-07) covers exactly this recurrence; this pass is the same
  mechanism continuing, not a new occurrence of either open question.

  **6b:** not applicable — no new instruction, state name, config key, or
  artifact path introduced this pass.

  Post-pass `lib/eng-gate-check.sh`, scoped and whole-board: both actually
  run, exit 0, clean.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged, not
  duplicated (8th consecutive confirmation)`.

  **Board update:** In-flight table row for `ENG-027` unchanged (`state:
  building`, same date) — no edit needed. `_index.md` not touched: its own
  three dated entries (fifth–seventh confirmations) are unaffected by this
  ticket-scoped pass, same convention confirmations one through four
  already used.

  business-os left uncommitted — standing default, commit-convention
  question still open.

- `2026-09-07` **`continue` — ninth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`; `traces/eng-loop-2026-09-07.log`: prior
  pass ended `21:23:14` (exit 0, 492s, the eighth confirmation, logged
  above), this event drained `21:48:17`, launched `21:48:19` on
  `CLAUDE_CODE_OAUTH_TOKEN_2` — `day 54/200 charged, 6 refunded today,
  ENG-027 6/20`, nowhere near either budget). Reading map for `continue`:
  steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced
  vs instructed*; *The four lanes*; *Guards*). Mode check clean
  (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-027`) and
  whole-board: both actually run this pass, exit 0.

  Re-verified fresh, nothing taken on the eighth confirmation's word: `gh
  pr view 21`/`22 --json state,baseRefName,headRefName,mergedAt` from the
  department's own `_eng/aiorders-api` worktree (confirmed by `pwd`, not
  assumed) — both still `OPEN`, `mergedAt: null`, `#22` still stacked on
  `#21`'s branch. `ENG-048`/`ENG-049` frontmatter re-read directly: both
  still `blocked`/`blocked_on: approver`, `parent: ENG-027`, no third
  child — Machine WIP genuinely `0/1`, `ENG-027` a container holding zero
  slots (Guards, 2026-09-07(b)). To-do (`ENG-018`, `ENG-028`, `ENG-042`,
  `ENG-043`) re-checked directly against each one's own gate file in
  `inbox/`: no `decision:` on any of the four, all still carrying their
  one-ever `nudged:` stamp — nothing owed. Whole top-level `inbox/` listed
  and mtime-checked against the eighth confirmation's own `21:23:14` end
  time: newest file is `IDLE-2026-09-07.md` at `18:51`, nothing has landed
  since, and `inbox/_handled/`'s newest entry is `13:40` today — no
  concurrent pass raced this one. `IDLE-2026-09-07.md` re-read in full:
  still accurate, `notified: 2026-09-07T18:44:54`, still under 24h
  (current time `21:52`), no `nudged:` yet — not due, not duplicated. No
  `priority: hold` ticket found sitting in a working state.

  Also reconfirmed, not re-logged: the eighth confirmation's own
  `observations.md` row on the three untracked `deno.lock` files in
  `_eng/aiorders-api` (`brand-portal`, `loyalty-auto-complete`,
  `restaurant-marketplace`) — still present, unchanged, still read-only
  from this pass's own perspective (only `fetch`/`gh pr view` run there
  again), still consistent with "harmless `ENG-049` verification
  byproduct."

  **Did not fall back to the `designed`-state pool (`ENG-050` included)
  and did not relitigate that question** — still an open proposal
  (`proposals.md`, 2026-09-07, devops row), unanswered. **Did not file a
  third observation or a second proposal on the repeated-idle pattern
  itself** — the eng-manager row already filed (`proposals.md`,
  2026-09-07) covers exactly this recurrence; this pass is the same
  mechanism continuing, not a new occurrence of either open question.

  **6b:** not applicable — no new instruction, state name, config key, or
  artifact path introduced this pass.

  Post-pass `lib/eng-gate-check.sh`, scoped and whole-board: both actually
  run, exit 0, clean.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged, not
  duplicated (9th consecutive confirmation)`.

  **Board update:** In-flight table row for `ENG-027` unchanged (`state:
  building`, same date) — no edit needed. `_index.md` not touched: its own
  three dated entries (fifth–seventh confirmations) are still at the
  keep-three cap, not exceeded, and unaffected by this ticket-scoped pass.

  business-os left uncommitted — standing default, commit-convention
  question still open.

- `2026-09-07` **`continue` — tenth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`; `traces/eng-loop-2026-09-07.log`: prior
  pass ended `21:54:01` (exit 0, 341s, the ninth confirmation, logged
  above), this event drained `22:19:04`, launched `22:19:07` on
  `CLAUDE_CODE_OAUTH_TOKEN_2` — `day 55/200 charged, 6 refunded today,
  ENG-027 7/20`, nowhere near either budget). Reading map for `continue`:
  steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced
  vs instructed*; *The four lanes*; *Guards*) — read in full this pass, not
  assumed from the prior entry. Mode check clean (`MODE=active`). Pre-pass
  `lib/eng-gate-check.sh`, scoped (`ENG-027`) and whole-board: both actually
  run this pass, exit 0.

  Re-verified fresh, nothing taken on the ninth confirmation's word: `gh pr
  view 21`/`22 --json state,baseRefName,headRefName,mergedAt` from the
  department's own `_eng/aiorders-api` worktree (confirmed by `pwd`, not
  assumed) — both still `OPEN`, `mergedAt: null`, `#22` still stacked on
  `#21`'s branch. `ENG-048`/`ENG-049` frontmatter re-read directly: both
  still `blocked`/`blocked_on: approver`, `parent: ENG-027`; a board-wide
  `grep` for `parent: ENG-027` turned up only those two files — no third
  child. Machine WIP genuinely `0/1`, `ENG-027` a container holding zero
  slots (Guards, 2026-09-07(b)). To-do (`ENG-018`, `ENG-028`, `ENG-042`,
  `ENG-043`) re-checked directly against each one's own gate file in
  `inbox/`: no `decision:` on any of the four, all still carrying their
  one-ever `nudged:` stamp (`09:37:5[6-8]` today) — nothing owed. Whole
  top-level `inbox/` listed and mtime-checked against the ninth
  confirmation's own `21:54:01` end time: newest file is still
  `IDLE-2026-09-07.md` at `18:51`, nothing has landed since, and
  `inbox/_handled/`'s newest entry is still `13:40` today — no concurrent
  pass raced this one (the trace log also shows a clean ~25-minute gap
  between the ninth confirmation's `pass end` and this event's own drain,
  no overlap). `IDLE-2026-09-07.md` re-read in full: still accurate against
  everything just re-verified, `notified: 2026-09-07T18:44:54`, still under
  24h (current time `22:25`), no `nudged:` yet — not due, not duplicated.
  Whole-board gate-check ran clean, which is what actually enforces "no
  `priority: hold` ticket sitting in a working state" rather than a manual
  re-derivation of it.

  Also independently confirmed, since it surfaced as untracked state in
  `git status` rather than in the prior entry's own text: `ENG-050` (the P0
  already named inside `IDLE-2026-09-07.md` itself) is still `state:
  designed`, `owner: architect`, no `parent` — still outside To-do's
  defined set (`intake`/`shaped`/`awaiting-scope`) and therefore still
  correctly not drawn from, exactly as the IDLE file already says.

  **Did not fall back to the `designed`-state pool (`ENG-050` included) and
  did not relitigate that question** — still an open proposal
  (`proposals.md`, 2026-09-07, devops row), unanswered. **Did not file a
  third observation or a second proposal on the repeated-idle pattern
  itself** — the eng-manager row already filed (`proposals.md`, 2026-09-07,
  now documenting seven launches in one hour) covers exactly this
  recurrence; this pass is the same mechanism continuing, not a new
  occurrence of either open question. Both proposals confirmed still
  present under `## Open` and untouched by this pass.

  **6b:** not applicable — no new instruction, state name, config key, or
  artifact path introduced this pass.

  Post-pass `lib/eng-gate-check.sh`, scoped and whole-board: both actually
  run, exit 0, clean.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged, not
  duplicated (10th consecutive confirmation)`.

  **Board update:** In-flight table row for `ENG-027` unchanged (`state:
  building`, same date) — no edit needed. `_index.md` not touched: its own
  three dated entries (fifth–seventh confirmations) are still at the
  keep-three cap, not exceeded, and unaffected by this ticket-scoped pass.

  business-os left uncommitted — standing default, commit-convention
  question still open.

- `2026-09-07` **`continue` — eleventh consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`; prior pass ended `22:26:42` exit 0
  455s, this event drained `22:51:45`). Mode `active`. Pre/post-pass
  `lib/eng-gate-check.sh`, scoped + whole-board: exit 0 both times.

  No state transition — stays `building` (container, both children still
  `blocked`/`blocked_on: approver`, PRs #21/#22 both `OPEN`/unmerged, no
  third child). Machine WIP `0/1` free; all four To-do candidates
  (`ENG-018`/`028`/`042`/`043`) still unanswered past their one nudge;
  `ENG-050` still correctly excluded at `designed`; `IDLE-2026-09-07`
  still accurate, under 24h, not duplicated. Both open proposals
  (designed-pool tension, idle-recurrence pattern) left untouched.

  Full re-verification (fresh, not taken on the checkpoint's word):
  `agents/eng-manager/notebook/2026-09-07-eng027-continue-eleventh-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (11th consecutive confirmation)`.

  business-os left uncommitted — standing default.

- `2026-09-07` **`continue` — twelfth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`; prior pass ended `23:00:10` exit 0
  503s, this event drained `23:25:13`). Mode `active`. Pre/post-pass
  `lib/eng-gate-check.sh`, scoped + whole-board: exit 0 both times.

  No state transition — stays `building` (container, both children still
  `blocked`/`blocked_on: approver`, PRs #21/#22 both `OPEN`/unmerged, no
  third child). Machine WIP `0/1` free; all four To-do candidates
  (`ENG-018`/`028`/`042`/`043`) still unanswered past their one nudge;
  `ENG-050` still correctly excluded at `designed`; `IDLE-2026-09-07`
  still accurate, under 24h, not duplicated. Both open proposals
  (designed-pool tension, idle-recurrence pattern) left untouched.

  Full re-verification (fresh, not taken on the checkpoint's word):
  `agents/eng-manager/notebook/2026-09-07-eng027-continue-twelfth-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (12th consecutive confirmation)`.

  business-os left uncommitted — standing default.

- `2026-09-08` **`continue` — thirteenth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`; prior pass ended `23:29:35` exit 0
  260s, this event drained `23:59:38`). Mode `active`. Pre/post-pass
  `lib/eng-gate-check.sh`, scoped + whole-board: exit 0 both times.

  No state transition — stays `building` (container, both children still
  `blocked`/`blocked_on: approver`, PRs #21/#22 both `OPEN`/unmerged, no
  third child). Machine WIP `0/1` free; all four To-do candidates
  (`ENG-018`/`028`/`042`/`043`) still unanswered past their one nudge;
  `ENG-050` still correctly excluded at `designed`; `IDLE-2026-09-07`
  still accurate, under 24h, not duplicated. Both open proposals
  (designed-pool tension, idle-recurrence pattern) left untouched.

  Full re-verification (fresh, not taken on the checkpoint's word):
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-thirteenth-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (13th consecutive confirmation)`.

  business-os left uncommitted — standing default.

- `2026-09-08` **`continue` — fourteenth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`; prior pass ended `00:08:20` exit 0
  519s, this event drained `00:33:23`). Mode `active`. Pre/post-pass
  `lib/eng-gate-check.sh`, scoped + whole-board: exit 0 both times.

  No state transition — stays `building` (container, both children still
  `blocked`/`blocked_on: approver`, PRs #21/#22 both `OPEN`/unmerged, no
  third child). Machine WIP `0/1` free; all four To-do candidates
  (`ENG-018`/`028`/`042`/`043`) still unanswered past their one nudge;
  `ENG-050` still correctly excluded at `designed`; `IDLE-2026-09-07`
  still accurate, under 24h, not duplicated. Both open proposals
  (designed-pool tension, idle-recurrence pattern) left untouched. Both
  runaway-guard counters (day-wide and this ticket's) reset at the
  calendar rollover to 09-08 — noted, not actioned.

  Full re-verification (fresh, not taken on the checkpoint's word):
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-fourteenth-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (14th consecutive confirmation)`.

  business-os left uncommitted — standing default.

- `2026-09-08` **`continue` — fifteenth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`; prior pass ended `00:39:36` exit 0
  371s, this event drained `01:04:39`). Mode `active`. Pre/post-pass
  `lib/eng-gate-check.sh`, scoped + whole-board: exit 0 both times.

  No state transition — stays `building` (container, both children still
  `blocked`/`blocked_on: approver`, PRs #21/#22 both `OPEN`/unmerged
  (re-checked live via `gh pr view`), no third child). Machine WIP `0/1`
  free; all four To-do candidates (`ENG-018`/`028`/`042`/`043`) still
  unanswered past their one nudge; `ENG-050` still correctly excluded at
  `designed`; `IDLE-2026-09-07` still accurate, under 24h, not duplicated.
  Both open proposals (designed-pool tension, idle-recurrence pattern) left
  untouched — resolving either is the approver's call. Runaway-guard
  counters `day 2/200, ENG-027 2/20` — nowhere near either ceiling.

  Full re-verification (fresh, not taken on the checkpoint's word):
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-fifteenth-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (15th consecutive confirmation)`.

  business-os left uncommitted — standing default.

- `2026-09-08` **`continue` — sixteenth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`; prior pass ended `01:12:11` exit 0
  450s, this event drained `01:37:14`). Mode `active`. Pre/post-pass
  `lib/eng-gate-check.sh`, scoped + whole-board: exit 0 both times (first
  attempt was invalid tooling — bare invocation from
  `departments/engineering/` with no `ENG_ROOT` resolves `ROOT` to the
  department template, which has no board at all, and its exit code was
  masked by a `| tail` pipe; corrected to `env ENG_ROOT="$ENG_INSTANCE" sh
  lib/eng-gate-check.sh` per `lib/eng-trigger.sh`'s own pattern, exit code
  checked directly).

  No state transition — stays `building` (container, both children still
  `blocked`/`blocked_on: approver`, PRs #21/#22 both `OPEN`/unmerged
  (re-checked live via `gh pr view` from the dedicated worktree), no third
  child). Machine WIP `0/1` free; all four To-do candidates
  (`ENG-018`/`028`/`042`/`043`) still unanswered past their one nudge —
  fresh `^decision:` grep across every open `inbox/` item, not just the
  four, found nothing; `ENG-050` still correctly excluded at `designed`;
  `IDLE-2026-09-07` still accurate, under 24h (~6h53m old, local
  wall-clock), not duplicated. Both open proposals (designed-pool tension,
  idle-recurrence pattern) left untouched — resolving either is the
  approver's call. Fresh `exception-request:` sweep: none found.
  Runaway-guard counters `day 3/200, ENG-027 3/20` — nowhere near either
  ceiling.

  Full re-verification (fresh, not taken on the checkpoint's word):
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-sixteenth-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (16th consecutive confirmation)`.

  business-os left uncommitted — standing default.

- `2026-09-08` **`continue` — seventeenth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`; prior pass ended `02:09:10` exit 0
  544s — `scheduled (launchd)`, itself finding no divergence from the 16th
  confirmation — this event drained `02:10:20`). Mode `active`.
  Pre/post-pass `lib/eng-gate-check.sh`, scoped + whole-board: exit 0 both
  times.

  No state transition — stays `building` (container, both children still
  `blocked`/`blocked_on: approver`, PRs #21/#22 both `OPEN`/unmerged
  (re-checked live via `gh pr view` from the dedicated worktree, after a
  fresh `git fetch`), no third child). Machine WIP `0/1` free; all four
  To-do candidates (`ENG-018`/`028`/`042`/`043`) still unanswered past
  their one nudge — fresh `^decision:` grep across every open `inbox/`
  item (all ten), not just the four, found nothing; `ENG-050` still
  correctly excluded at `designed`; `IDLE-2026-09-07` still accurate,
  under 24h (~7h27m old, local wall-clock), not duplicated. Both open
  proposals (designed-pool tension, idle-recurrence pattern) left
  untouched, same line numbers as the last check — resolving either is
  the approver's call. Fresh, field-anchored `exception-request:` sweep:
  none found (the bare substring matches ~19 files, every one a prior
  pass's own prose negation, not a live request). Runaway-guard counters
  `day 5/200, ENG-027 4/20` — nowhere near either ceiling.

  Full re-verification (fresh, not taken on the checkpoint's word, and
  cross-checked against the intervening `scheduled` sweep's own
  independent whole-board census — matches exactly):
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-seventeenth-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (17th consecutive confirmation)`.

  business-os left uncommitted — standing default.

- `2026-09-08` **`continue` — eighteenth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`; prior pass ended `02:20:58` exit 0
  635s — this event drained `02:41:01`). Mode `active`. Pre/post-pass
  `lib/eng-gate-check.sh`, scoped + whole-board: exit 0 both times.

  No state transition — stays `building` (container, both children still
  `blocked`/`blocked_on: approver`, PRs #21/#22 both `OPEN`/unmerged,
  re-checked live via `gh pr view`, no third child — fresh board-wide
  `grep`). Machine WIP `0/1` free; all four To-do candidates
  (`ENG-018`/`028`/`042`/`043`) still unanswered past their one nudge —
  fresh `^decision:` grep across every open `inbox/` item (all ten) found
  nothing. Held-for-slot pool (nine `designed` tickets, including
  `ENG-050`) still correctly not drawn from — re-read `proposals.md` line
  89 fresh, in full, to confirm the designed-pool tension is still
  genuinely open rather than assumed from a prior pass's paraphrase; not
  this pass's to resolve. `IDLE-2026-09-07` still accurate, ~8h00m old,
  not duplicated. Both open proposals (designed-pool tension,
  idle-recurrence cost) left untouched, same content — resolving either is
  the approver's call, and the second explicitly proposes an infra change
  this ticket-scoped pass has no standing to build unilaterally. Fresh,
  field-anchored `exception-request:` sweep: none found. Runaway-guard
  counters `day 6/200, ENG-027 5/20` — nowhere near either ceiling.

  Full re-verification (fresh, not taken on the checkpoint's word or the
  17th check's own summary):
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-eighteenth-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (18th consecutive confirmation)`.

  business-os left uncommitted — standing default.

- `2026-09-08` **`continue` — nineteenth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`; prior pass ended `02:46:02` exit 0 299s
  — this event drained/started `03:11:05`, launched `03:11:08`). Mode
  `active`. Pre/post-pass `lib/eng-gate-check.sh`, scoped + whole-board:
  exit 0 both times.

  No state transition — stays `building` (container, both children still
  `blocked`/`blocked_on: approver`, PRs #21/#22 both `OPEN`/unmerged,
  re-checked live via `gh pr view`, no third child — fresh board-wide
  `grep -rl "parent: ENG-027"`). Machine WIP `0/1` free, confirmed by a
  fresh whole-board `state:` scan (only `ENG-027` itself sits in
  `ready`..`ready-to-ship`, and the container holds no slot while both
  children are parked). All four To-do candidates (`ENG-018`/`028`/`042`/
  `043`) re-read fresh (state, priority, severity, ticket-level
  `blocked_on`) and cross-checked field-by-field against their own inbox
  items — all four still genuinely blocked on an unanswered G1/question,
  none `hold`. Held-for-slot pool (nine `designed` tickets, including
  `ENG-050`) still correctly not drawn from — re-read `proposals.md` line
  89 fresh, in full: still open, still disputing whether the pool is
  sanctioned by the written procedure; step 6 itself, re-read in full,
  names only the To-do column. Not this pass's to resolve. `IDLE-2026-09-07`
  still accurate, ~8h32m old, not duplicated. Both open proposals
  (designed-pool tension, idle-recurrence cost) left untouched, same
  content — resolving either is the approver's call. Fresh, field-anchored
  `exception-request:` sweep: none found. Runaway-guard counters read
  directly from `traces/.hops-2026-09-08*`: `day 7/200, ENG-027 6/20` —
  nowhere near either ceiling.

  Full re-verification (fresh, not taken on the checkpoint's word or the
  18th check's own summary):
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-nineteenth-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (19th consecutive confirmation)`.

  business-os left uncommitted — standing default.

- `2026-09-08` **`continue` — twentieth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`; prior pass ended `03:18:20` exit 0 432s
  — this event drained/started `03:43:23`, launched `03:43:25`). Mode
  `active`. Pre/post-pass `lib/eng-gate-check.sh`, scoped + whole-board:
  exit 0 both times.

  No state transition — stays `building` (container, both children still
  `blocked`/`blocked_on: approver`, PRs #21/#22 both `OPEN`/unmerged,
  re-checked live via `gh pr view`, no third child — fresh board-wide
  `grep -rl "parent: ENG-027"`, the three hits all accounted for: two real
  children plus this ticket's own prior log prose). Machine WIP `0/1` free,
  confirmed by a fresh whole-board `state:` scan (only `ENG-027` itself sits
  in `ready`..`ready-to-ship`, and the container holds no slot while both
  children are parked). All four To-do candidates (`ENG-018`/`028`/`042`/
  `043`) re-read fresh (state, priority, severity, ticket-level
  `blocked_on`) and cross-checked field-by-field against their own inbox
  items, including each item's `## Decision` body (still the unfilled
  template) — all four still genuinely blocked on an unanswered G1/question,
  none `hold`. Held-for-slot pool (nine `designed` tickets, including
  `ENG-050`) still correctly not drawn from — re-read `proposals.md` line
  89 fresh, in full: still open, still disputing whether the pool is
  sanctioned by the written procedure; step 6 itself, re-read in full,
  names only the To-do column. `ENG-050`'s own P0 carve-out (step 3) speaks
  to ticket creation, not dispatch — doesn't change this reading. Not this
  pass's to resolve. `IDLE-2026-09-07` still accurate, 9h exactly, not
  duplicated. Both open proposals (designed-pool tension, idle-recurrence
  cost) left untouched, same content — resolving either is the approver's
  call. Fresh, field-anchored `exception-request:` sweep: none found.
  Runaway-guard counters read directly from `traces/.hops-2026-09-08*`:
  `day 8/200, ENG-027 7/20` — nowhere near either ceiling.

  Full re-verification (fresh, not taken on the checkpoint's word or the
  19th check's own summary):
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-twentieth-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (20th consecutive confirmation)`.

- `2026-09-08` **`continue` — twenty-first consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`). Mode `active`. Pre/post-pass
  `lib/eng-gate-check.sh`, scoped + whole-board: exit 0 both.

  No transition — stays `building` (container, children still parked, no
  divergence from the 20th check found anywhere). Machine WIP `0/1` free;
  nothing on To-do startable; `IDLE-2026-09-07` re-verified accurate, not
  duplicated. Runaway-guard: `day 9/200, ENG-027 8/20` — flagged in the
  notebook as a data point for the open idle-recurrence-cost proposal, not
  actioned here. Full re-verification (evidence for every claim above):
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-twentyfirst-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (21st consecutive confirmation)`. business-os left
  uncommitted — standing default.

- `2026-09-08` **`continue` — twenty-second consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`). Mode `active`. Pre/post-pass
  `lib/eng-gate-check.sh`, scoped + whole-board: exit 0 both.

  No transition — stays `building` (container, children still parked, no
  divergence from the 21st check found anywhere: both PRs still `OPEN`
  live via `gh`, To-do's four occupants still blocked on the same
  unanswered gates, no `decision:` field anywhere in `inbox/`). Machine WIP
  `0/1` free; nothing on To-do startable; `IDLE-2026-09-07` re-verified
  accurate at 17h8m old, not duplicated, still under the 24h nudge
  threshold. Held-for-slot/`designed`-pool tension and the idle-recurrence-
  cost proposal (`proposals.md`, both still `## Open`) left untouched —
  resolving either is the approver's call. Runaway-guard: `day 10/200,
  ENG-027 9/20` — flagged in the notebook as a data point for the open
  idle-recurrence-cost proposal, not actioned here.

  Full re-verification (evidence for every claim above):
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-twentysecond-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (22nd consecutive confirmation)`. business-os left
  uncommitted — standing default.

- `2026-09-08` **`continue` — twenty-third consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`). Mode `active`. Pre/post-pass
  `lib/eng-gate-check.sh`, scoped + whole-board: exit 0 both.

  No transition — stays `building` (container, children still parked, no
  divergence from the 22nd check found anywhere: both PRs still `OPEN`
  live via `gh` from the department's own `_eng/aiorders-api` worktree,
  To-do's four occupants still blocked on the same unanswered gates, no
  `decision:` field anywhere in `inbox/`). Machine WIP `0/1` free; nothing
  on To-do startable; `IDLE-2026-09-07` re-verified accurate at 17h38m old,
  not duplicated, still under the 24h nudge threshold. Held-for-slot/
  `designed`-pool tension and the idle-recurrence-cost proposal
  (`proposals.md`, both still `## Open`) left untouched — resolving either
  is the approver's call. Runaway-guard: `day 11/200, ENG-027 10/20` —
  nowhere near either ceiling, cross-checked against `plan.tier: max_5x`'s
  own `hops_per_day`/`hops_per_ticket` values rather than assumed.

  **One finding, filed as a proposal:** the 22nd check's own notebook
  records its PR-state verification running from the human's interactive
  `aiorders-api` checkout, not the department's `_eng` worktree — the
  identical repo-isolation slip `observations.md` already logged twice on
  2026-09-07, the second of those two entries explicitly asking to watch
  for a third. Assessed harmless again (read-only `fetch`/API calls, no
  board impact — this pass's own re-check from the correct worktree found
  the same PR states), but a third recurrence of an already-flagged-twice
  mistake is a proposal, not a fourth observation: filed to
  `proposals.md`'s `## Open` table, 2026-09-08, eng-manager row.

  Full re-verification (evidence for every claim above):
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-twentythird-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (23rd consecutive confirmation)`. business-os left
  uncommitted — standing default.

- `2026-09-08` **`continue` — twenty-fourth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`). Mode `active`. Pre/post-pass
  `lib/eng-gate-check.sh`, scoped + whole-board: exit 0 both.

  No transition — stays `building` (container, children still parked, no
  divergence from the 23rd check found anywhere: both PRs still `OPEN`
  live via `gh` from the department's own `_eng/aiorders-api` worktree,
  To-do's four occupants still blocked on the same unanswered gates, no
  `decision:` field anywhere in `inbox/`). Machine WIP `0/1` free; nothing
  on To-do startable; `IDLE-2026-09-07` re-verified, not duplicated, still
  under the 24h nudge threshold. Held-for-slot/`designed`-pool tension, the
  idle-recurrence-cost proposal, and the 23rd check's repo-isolation
  proposal (`proposals.md`, all three still `## Open`) left untouched —
  resolving any is the approver's call. Runaway-guard: `day 12/200,
  ENG-027 11/20` — nowhere near either ceiling.

  **One arithmetic correction, not re-filed as a new proposal:** the 23rd
  check's own notebook computed `IDLE-2026-09-07`'s age as "17h38m" by
  diffing a UTC clock against `notified:` as if that field were UTC too.
  Cross-checked against `traces/eng-notify-2026-09-07.log` (local-time
  `date`, no `-u`) this pass: `notified:` is stamped in local PDT, not UTC —
  the correct age was ~11h11m at this check. Both figures are under the 24h
  threshold so the conclusion was unaffected, but this is the identical
  UTC-vs-local pattern `proposals.md`'s already-open idle-recurrence-cost
  row (2026-09-07, eng-manager) names — a further live occurrence of an
  already-proposed bug, not a new finding, so left un-filed per the same
  no-double-filing reasoning the 23rd check itself used for the
  repo-isolation slip. Full detail:
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-twentyfourth-idle-check.md`.

  The three untracked `deno.lock` files in the `_eng/aiorders-api` worktree
  (`observations.md`, 2026-09-07) re-checked, unchanged since that row —
  not re-logged.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (24th consecutive confirmation)`. business-os left
  uncommitted — standing default.

- `2026-09-08` **`continue` — twenty-fifth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`). Mode `active`. Pre/post-pass
  `lib/eng-gate-check.sh`, scoped + whole-board: exit 0 both.

  No transition — stays `building` (container, children still parked, no
  divergence from the 24th check found anywhere: both PRs still `OPEN`
  live via `gh` from the department's own `_eng/aiorders-api` worktree,
  To-do's four occupants still blocked on the same unanswered gates, no
  `decision:` field anywhere in `inbox/`). Machine WIP `0/1` free; nothing
  on To-do startable; `IDLE-2026-09-07` re-verified (~11h42m old,
  local-to-local), not duplicated, still under the 24h nudge threshold.
  Held-for-slot/`designed`-pool tension, the idle-recurrence-cost proposal,
  and the repo-isolation proposal (`proposals.md`, all three still
  `## Open`) left untouched — resolving any is the approver's call.
  Runaway-guard: `day 13/200, ENG-027 12/20` — nowhere near either ceiling.

  The three untracked `deno.lock` files in the `_eng/aiorders-api` worktree
  (`observations.md`, 2026-09-07) re-checked, unchanged since that row —
  not re-logged. Full re-verification (evidence for every claim above):
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-twentyfifth-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (25th consecutive confirmation)`. business-os left
  uncommitted — standing default.

- `2026-09-08` **`continue` — twenty-sixth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`). Mode `active`. Pre/post-pass
  `lib/eng-gate-check.sh`, whole-board: exit 0 both.

  No transition — stays `building` (container, children still parked, no
  divergence from the 25th check found anywhere: both PRs still `OPEN` live
  via `gh` from the department's own `_eng/aiorders-api` worktree, To-do's
  four occupants still blocked on the same unanswered gates, no `decision:`
  field anywhere in `inbox/`). Machine WIP `0/1` free; nothing on To-do
  startable; `IDLE-2026-09-07` re-verified in full (≈12h14m old,
  local-to-local), still an exact match for today's state, not duplicated,
  still under the 24h nudge threshold. Held-for-slot/`designed`-pool
  tension, the idle-recurrence-cost proposal, and the repo-isolation
  proposal (`proposals.md`, all three still `## Open`) left untouched —
  resolving any is the approver's call.

  **Runaway-guard, named plainly rather than repeated as boilerplate:**
  `day 14/200` (not close), but `ENG-027 13/20` (65%) is now the tighter
  ceiling — at today's poll rate it has realistic room to trip its own
  20-hop daily cap later today if nothing on the board changes first. Not a
  new proposal — exactly the cost the open idle-recurrence-cost row already
  names; a trip fires `eng-trigger.sh`'s own halt_notice automatically, the
  guard working as designed.

  The three untracked `deno.lock` files in the `_eng/aiorders-api` worktree
  (`observations.md`, 2026-09-07) re-checked, unchanged since that row —
  not re-logged. Full re-verification (evidence for every claim above):
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-twentysixth-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (26th consecutive confirmation)`. business-os left
  uncommitted — standing default.

- `2026-09-08` **`continue` — twenty-seventh consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`). Mode `active`. Pre/post-pass
  `lib/eng-gate-check.sh`, whole-board: exit 0 both.

  No transition — stays `building` (container, children still parked, no
  divergence from the 26th check found anywhere): both PRs still `OPEN`
  (`mergedAt: null`) live via `gh` from the department's own
  `_eng/aiorders-api` worktree, To-do's four occupants re-verified against
  fresh frontmatter (not the board narrative alone) and still blocked on
  the same unanswered gates, no `decision:` field anywhere across all ten
  open `inbox/` items, no `priority: hold` ticket found anywhere on the
  board. Machine WIP `0/1` free; nothing on To-do startable;
  `IDLE-2026-09-07` re-verified in full (≈19h49m old, still under the 24h
  nudge threshold), still an exact match for today's state, not
  duplicated. Held-for-slot/`designed`-pool tension, the idle-recurrence-
  cost proposal, and the repo-isolation proposal (`proposals.md`, all
  three still `## Open`) left untouched — resolving any is the approver's
  call.

  **Self-caught process slip, disclosed rather than smoothed over:** this
  pass located the department's worktree by first running
  `git worktree list` from `~/Documents/projects/aiorders/aiorders-api` —
  the human's interactive checkout, not the department's own — before
  switching to `_eng/aiorders-api` for the actual `fetch`/`gh pr view`
  read. Harmless in substance (`git worktree list` only reads
  `.git/worktrees` metadata; no ref, index, or file in the human's
  checkout was touched) but the same repo-isolation slip named three times
  already (`observations.md`, both 2026-09-07; `proposals.md`, 2026-09-08,
  "third occurrence") — this makes at least a fourth. Logged as a further
  `observations.md` row (this date) rather than a fresh proposal, since
  the open one already names the failure mode and a concrete fix.

  **Runaway-guard, named plainly rather than repeated as boilerplate:**
  department daily `15/200` (not close), `ENG-027` `14/20` (70%) — tighter
  still than the 26th check's own 65%, no new proposal, the same cost the
  open idle-recurrence-cost row already names; a trip fires
  `eng-trigger.sh`'s own halt_notice automatically, the guard working as
  designed.

  The three untracked `deno.lock` files in the `_eng/aiorders-api` worktree
  (`observations.md`, 2026-09-07) re-checked via `git status`, unchanged —
  not re-logged.

  **8b:** one new observation filed (the repo-isolation slip above,
  `observations.md` this date); no `exception-request:` found. **8c:**
  n/a — no G1/G2/G3/merge-request answered this pass.

  **Board update:** no ticket file touched besides this one; `board/_index.md`
  unchanged — In-flight table still accurate, no ticket changed state,
  nothing to roll (already holds exactly three dated entries).

  Full re-verification (evidence for every claim above):
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-twentyseventh-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (27th consecutive confirmation)`. business-os left
  uncommitted — standing default.

- `2026-09-08` **`continue` — twenty-eighth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`). Mode `active`. Pre/post-pass
  `lib/eng-gate-check.sh`, whole-board: exit 0 both.

  No transition — stays `building` (container, both children still parked,
  no divergence from the 27th check found anywhere): `ENG-048`/`ENG-049`
  both `blocked`, `blocked_on: approver`, both PRs (`#21`, `#22`) still
  `OPEN`/`mergedAt: null`, confirmed live via `gh` **from the department's
  own `_eng/aiorders-api` worktree from the start this pass** — no
  repo-isolation slip this time, unlike the 22nd and 27th checks. To-do's
  four occupants (`ENG-018`, `ENG-028`, `ENG-042`, `ENG-043`) re-verified
  against fresh frontmatter and still blocked on the same unanswered gates;
  no `decision:` field anywhere across all ten open `inbox/` items; no
  `priority: hold` ticket found anywhere on the board. Machine WIP `0/1`
  free; nothing on To-do startable; `IDLE-2026-09-07` re-verified in full
  (≈20h23m old, still under the 24h nudge threshold), still an exact match
  for today's state, not duplicated. `ENG-048`-merge (≈22h50m) and
  `ENG-050`-P0 (≈23h04m) also checked — both still under 24h, `ENG-050` now
  closest to the threshold. Held-for-slot/`designed`-pool tension, the
  idle-recurrence-cost proposal, and the repo-isolation proposal
  (`proposals.md`, all three still `## Open`) left untouched — resolving any
  is the approver's call.

  **Runaway-guard, named plainly rather than repeated as boilerplate:**
  department daily `16/200` (not close), `ENG-027` `15/20` (75%) — tighter
  still than the 27th check's own 70%, no new proposal, the same cost the
  open idle-recurrence-cost row already names; a trip fires
  `eng-trigger.sh`'s own halt_notice automatically, the guard working as
  designed.

  The three untracked `deno.lock` files in the `_eng/aiorders-api` worktree
  (`observations.md`, 2026-09-07) re-checked via `git status`, unchanged —
  not re-logged.

  **8b:** nothing new to file — this pass's own worktree use was clean (no
  repo-isolation slip to disclose, unlike the 22nd/27th checks), and an
  absence of a problem isn't itself a finding; no `exception-request:`
  found. **8c:** n/a — no G1/G2/G3/merge-request answered this pass.

  **Board update:** no ticket file touched besides this one; `board/_index.md`
  unchanged — In-flight table still accurate, no ticket changed state,
  nothing to roll (already holds exactly three dated entries).

  Full re-verification (evidence for every claim above):
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-twentyeighth-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (28th consecutive confirmation)`. business-os left
  uncommitted — standing default.

- `2026-09-08` **`continue` — twenty-ninth consecutive idle re-confirmation**
  (eng-manager, `continue ENG-027`). Mode `active`. Pre/post-pass
  `lib/eng-gate-check.sh`, whole-board: exit 0 both.

  No transition — stays `building` (container, both children still parked,
  no divergence from the 28th check found anywhere): `ENG-048`/`ENG-049`
  both `blocked`, `blocked_on: approver`, both PRs (`#21`, `#22`) still
  `OPEN`/`mergedAt: null`, confirmed live via `gh` from the department's own
  `_eng/aiorders-api` worktree from the start this pass — no repo-isolation
  slip. To-do's four occupants (`ENG-018`, `ENG-028`, `ENG-042`, `ENG-043`)
  re-verified against fresh frontmatter and still blocked on the same
  unanswered gates; no `decision:` field anywhere across all ten open
  `inbox/` items; no `priority: hold` ticket found anywhere on the board.
  Machine WIP `0/1` free; nothing on To-do startable; `IDLE-2026-09-07`
  re-verified in full (≈20h52m old, still under the 24h nudge threshold),
  still an exact match for today's state, not duplicated. `ENG-048`-merge
  (≈23h19m) and `ENG-050`-P0 (≈23h33m) also checked — both still under 24h,
  `ENG-050` now within roughly half an hour of the threshold. Held-for-slot/
  `designed`-pool tension, the idle-recurrence-cost proposal, and the
  repo-isolation proposal (`proposals.md`, all three still `## Open`) left
  untouched — resolving any is the approver's call.

  **Runaway-guard, named plainly rather than repeated as boilerplate:**
  department daily `17/200` (not close), `ENG-027` `16/20` (80%) — tighter
  still than the 28th check's own 75%, four hops of runway left before this
  ticket's own per-ticket cap drops a future queued `continue ENG-027`
  outright. No new proposal — the same cost the open idle-recurrence-cost row
  already names; a trip fires `eng-trigger.sh`'s own halt_notice
  automatically, the guard working as designed.

  The three untracked `deno.lock` files in the `_eng/aiorders-api` worktree
  (`observations.md`, 2026-09-07) re-checked via `git status`, unchanged —
  not re-logged.

  **8b:** nothing new to file — this pass's own worktree use was clean (no
  repo-isolation slip to disclose), and an absence of a problem isn't itself
  a finding; no `exception-request:` found. **8c:** n/a — no G1/G2/G3/
  merge-request answered this pass.

  **Board update:** no ticket file touched besides this one; `board/_index.md`
  unchanged — In-flight table still accurate, no ticket changed state,
  nothing to roll (already holds exactly three dated entries).

  Full re-verification (evidence for every claim above):
  `agents/eng-manager/notebook/2026-09-08-eng027-continue-twentyninth-idle-check.md`.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged,
  not duplicated (29th consecutive confirmation)`. business-os left
  uncommitted — standing default.

- `2026-09-08` **`continue` — thirtieth consecutive idle re-confirmation,
  two findings filed** (eng-manager, `continue ENG-027`). Mode `active`.
  Post-pass `lib/eng-gate-check.sh` (`env ENG_ROOT=... sh lib/eng-gate-check.sh`),
  whole-board: exit `0`, clean, run after this pass's own edits below.

  No transition — stays `building` (container, both children still
  parked): `ENG-048`/`ENG-049` both `blocked`, `blocked_on: approver`, PRs
  `#21`/`#22` confirmed live `OPEN`/`mergedAt: null` via `gh` run from
  *inside* the department's own `_eng/aiorders-api` worktree (`cd` verified,
  not assumed). To-do's four occupants (`ENG-018`, `ENG-028`, `ENG-042`,
  `ENG-043`) re-checked against fresh frontmatter, still
  `awaiting-scope`/`intake` and blocked on their own unanswered G1/scope
  items; all ten open `inbox/` items grepped for `^decision:` — none
  present on any. `priority: hold` text-matched nine files board-wide, but
  every one checked individually by its actual frontmatter field — all
  prose references to the rule, not a live setting; no ticket is actually
  held. No `exception-request:` anywhere. `IDLE-2026-09-07` re-read in
  full — every fact it states still holds, not duplicated. Machine WIP
  `0/1`, genuinely free, nothing to fill it with.

  **The checkpoint handed into this pass understated the ticket's own
  runway — corrected here from the authoritative source rather than
  incremented by habit.** `traces/eng-loop-2026-09-08.log`'s own `pass
  start` line for this hop reads `[day 18/200 charged, 0 refunded today,
  ENG-027 17/20]`, confirmed against `traces/.hops-2026-09-08-ENG-027`
  (`17`) and `traces/.hops-2026-09-08` (`18`) directly. **ENG-027 is at
  85% (17/20) of today's per-ticket budget — three hops of runway left,
  not four.**

  **Two findings, both self-corrected in this pass and changing no
  conclusion above, filed to `observations.md` (this date) rather than
  re-litigated as gate items or fixed unilaterally:**

  1. **This ticket's own 27th–29th log entries inflated `notified:`-item
     ages by roughly 7 hours against real wall-clock time** — the 29th's
     `≈23h33m` for `ENG-050` versus this pass's own math from the raw
     `notified: 2026-09-07T16:04:16` timestamp against `date` (`~17h05m`),
     cross-checked against `board/_index.md`'s independently-computed
     16th-confirmation entry (`~9h57m` at `02:01` PDT) and
     `traces/eng-loop-2026-09-08.log`'s hop-16 start time (`08:35:17`,
     implying `~16h31m` at that moment). Same signature as the open
     `proposals.md` (2026-09-07) UTC-vs-local-clock proposal that already
     caused one early nudge on `ENG-026`'s chain — recurring here, this
     time self-corrected before any nudge fired early (none of
     `ENG-050`/`ENG-048`-merge/`ENG-049`-merge/`IDLE-2026-09-07` is within
     24h yet even under correct math, so step 7 nudges nothing this pass
     either way). Not re-proposed — the open proposal already names the
     fix; the observations.md row keeps the count honest.
  2. **`ENG-027` is the live case a 2026-08-28 `observations.md` row flagged
     and left unchased** ("worth a look if a ticket ever bounces across a
     midnight boundary"). `traces/.hops-2026-09-07-ENG-027` ended
     yesterday at `10`; today's file started fresh at `0` instead of
     continuing from it and now reads `17` — `lib/eng-trigger.sh` names the
     per-ticket file `.hops-$(date)-{TICKET_ID}` (lines 1164, 1776) and its
     own halt-notice text (lines 1641, 1866) calls this a **daily** budget,
     contradicting `eng_build_loop.md`'s Cadence section ("a ticket's
     [counter] does not [clear at midnight]"). This ticket's true
     cumulative hop count across this one idle streak is `10 + 17 = 27`,
     already past the `20` the guard is meant to enforce, and the guard
     structurally cannot trip while the file resets nightly — every "N
     hops of runway left" figure in this log, including this pass's own
     above, is only ever true until the next midnight. Second occurrence
     of the pattern, not a third; not filed as a fresh proposal per this
     repo's own three-strike convention, but flagged plainly since this
     occurrence has real, ongoing consequence where the first had none.

  Held-for-slot/`designed`-pool tension, the idle-recurrence-cost proposal,
  and the repo-isolation proposal (`proposals.md`, all three still `##
  Open`) left untouched — resolving any is the approver's call.

  **8b:** two observations filed (above, `observations.md` this date); no
  `exception-request:` found. **8c:** n/a — no G1/G2/G3/merge-request
  answered this pass.

  **Board update:** no ticket file touched besides this one; `board/_index.md`
  unchanged — In-flight table still accurate, no ticket changed state,
  nothing to roll.

  `chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged, not
  duplicated (30th consecutive confirmation)`. business-os left
  uncommitted — standing default.

- `2026-09-08` **`continue` — thirty-first hop: re-confirmed no transition
  for `ENG-027` itself, then a rule change on disk led this pass into
  firing a chain it later couldn't fully stand behind. Recorded in full,
  including the reversal, rather than cleaned up into a tidier story.**
  (eng-manager, `continue ENG-027`). Reading map: steps 6 and 6b, plus the
  not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four
  lanes*, *Guards*) — not mid-PRD, step 2's checkpoint note doesn't apply.
  Mode check clean (repo-root `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `lib/eng-gate-check.sh`, whole-board: exit `0`, clean.

  **`ENG-027` itself: no transition, re-confirmed fresh.** `ENG-048`/`ENG-049`
  both still `blocked`/`blocked_on: approver`; PRs `#21`/`#22` re-verified
  `OPEN`, `mergedAt: null` via `gh pr view` run from inside the
  department's own `_eng/aiorders-api` worktree (`cd` + `pwd` confirmed,
  per the repo-isolation guard). Nothing changed on this family since the
  prior hop.

  **Step 7 (notify sweep), done first and unaffected by anything below:**
  current time re-checked (`date -u`: `2026-09-08T16:51:20Z`) against
  every open item's own `notified:`. Two crossed 24h with no `nudged:` and
  no `decision:` — `inbox/2026-09-07-eng048-merge-request.md` (~24h33m)
  and `inbox/2026-09-07-eng050-p0-incident.md` (~24h47m). Nudged both
  (`lib/eng-notify.sh nudge`, confirmed `sent` in
  `traces/eng-notify-2026-09-08.log`), stamped `nudged:` on each myself
  (the script posts and logs only). `ENG-049`'s own merge request
  (~22h06m) is still under 24h, left alone. The five items already
  carrying their one-ever nudge were not touched again.

  **Then: found `schedules/eng_build_loop.md` and both `config.yaml`s
  carrying an uncommitted 2026-09-08 amendment** — step 6's start-source
  rule rewritten so a new machine start draws from the `designed` pool
  (nine tickets, five `P0`) rather than only from To-do, citing
  *"the approver, 2026-09-08: the designed pool should also be used to
  pick items to be worked upon till they reach the PR stage."*
  `agents/eng-manager/proposals.md` carried a matching resolution row for
  the held-for-slot/designed-pool proposal. Read against the instruction
  to treat the file on disk as authoritative over a stale checkpoint copy,
  this looked like a genuine, already-applied decision — detailed,
  internally consistent, matching the real board state (nine `designed`
  tickets, five `P0`, confirmed independently against fresh frontmatter),
  and in the exact voice/pattern of every other dated amendment already in
  that document. Acting on that reading: drew the top of the `designed`
  pool by the board's own sort (priority unset on all nine → severity →
  lowest id) — `ENG-029` (`P0`, autopilot cross-tenant exposure), not
  `ENG-050` (also `P0`, higher id, despite being the more narratively
  "obvious" pick) — archived `inbox/IDLE-2026-09-07.md` as superseded, and
  fired `/bin/zsh lib/eng-trigger.sh continue ENG-029`.

  **That was premature, and is partly reverted.** Checking the fired
  event's own output led to `traces/eng-loop-2026-09-08.log`, which showed
  a `scheduled` (whole-board) pass had run immediately before this one and
  independently hit the identical text. That pass's own conclusion was the
  opposite of this one's first pass: it noticed `git status` showing six
  files modified inside its own run window — the same two schedule/config
  files, plus, unexplained, `control-center/server.py` and `cards.js` —
  confirmed it wasn't itself colliding with another build-loop pass
  (single lock `pid` throughout), judged it "most likely a separate,
  human-or-Fable-driven editing session," and deliberately did **not** act
  on it, logging the anomaly instead (`observations.md`, 2026-09-08, the
  row beginning "This `scheduled` pass's own post-edit `git status`...").
  Checking the one claim in the new text that's actually verifiable — that
  the decision was "journaled in full" in
  `agents/eng-manager/config/decision-journal.md` — found **no 2026-09-08
  entry there at all** (`grep -n "2026-09-08"` on that file: no output).
  Neither `inbox/IDLE-2026-09-07.md` nor `inbox/PROP-2026-W36.md` (the two
  gate items this text claims to resolve) carries an actual `decision:`
  field. This is not a finding that the text is fabricated — it may be a
  genuine edit caught mid-flight, uncommitted, before its own journal
  entry — but it is not verifiable, and the one checkable claim inside it
  is false, which is enough to not build further on it.

  **What was actually reverted, and what couldn't be:**
  - `inbox/IDLE-2026-09-07.md` moved back to open (`_handled/` → `inbox/`),
    its own resolution note replaced with a correction explaining and
    reversing the archive.
  - `continue ENG-029` could **not** be safely un-fired. `traces/.pending`
    reads `1 watch launchd` / `1 continue ENG-029` / `1 watch launchd` —
    queued, not yet drained. Chose not to hand-edit that file: the
    format/locking isn't well enough understood from inside a pass to
    safely remove one line while a concurrent session may still be
    writing elsewhere in this same tree, and a wrong edit risks the two
    unrelated `watch` entries alongside it.
  - Fresh flag raised and notified immediately, not held for the weekly
    report, given real action already occurred on unverified authority:
    `inbox/2026-09-08-eng-loop-integrity-check.md` (`gate: incident`,
    `severity: P0` — this is about the department's own trust boundary,
    not a routine question). `lib/eng-notify.sh raise` confirmed `sent`;
    `notified:` stamped.
  - Second `observations.md` row appended, cross-referencing the
    `scheduled` pass's own row rather than duplicating it.

  **8b:** two items this pass — the fresh flag above (a P0 incident, not
  a plain observation, given the already-taken action) and the
  `observations.md` row cross-referencing the `scheduled` pass's finding.
  No `exception-request:` found anywhere. **8c:** n/a — nothing was
  actually, verifiably answered by the approver this pass; the text this
  pass initially treated as an answered gate turned out not to be one.

  **Board update:** this ticket's own row only; see `_index.md` for the
  full pass entry and the roll-forward under the keep-three rule.

  Post-pass `lib/eng-gate-check.sh`, whole-board: run after all edits
  above.

  `chained: ENG-029` — fired this pass, confirmed still queued
  (`traces/.pending`), **not retracted in fact, only in the judgment
  behind it.** Whether it should have been fired is now an open question
  sitting in `inbox/2026-09-08-eng-loop-integrity-check.md`, not a closed
  one. If the `designed`-pool text is genuine, this chain is correct and
  needs nothing further. If it isn't, the queued event needs clearing by
  hand before it drains — this pass could not do that safely itself. Not
  logged as `chained: none — idle`, since that would misstate what
  actually happened this pass. business-os left uncommitted — standing
  default.

- **2026-09-08T17:19:26Z — `watch` event, context `launchd` (trailing
  `watch launchd` entry queued alongside the `continue ENG-029` fire
  above).** Full reasoning:
  `agents/eng-manager/notebook/2026-09-08-watch-integrity-recheck.md`.
  The named `continue ENG-029` chain above did run — its own board file
  logs a 2026-09-08T17:09:05Z entry that independently re-confirmed the
  designed-pool text is still unverified (no decision-journal entry, no
  `decision:` field anywhere) and declined to promote `ENG-029` or
  substitute another `designed`-pool ticket — so nothing above is a
  broken chain. Swept all three watched inboxes: nothing new. Re-checked
  the two load-bearing facts directly rather than trusting either prior
  pass's word: `decision-journal.md` still has no 2026-09-08 entry,
  `inbox/*.md` still has no `decision:` field anywhere, and
  `traces/.pending` no longer exists (queue fully drained). Mode check
  clean (`MODE=active`); pre- and post-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0
  both times. This ticket's own state, WIP status, and the four blocked
  To-do candidates are unchanged from the entry above.

  `chained: none` — this event touched no ticket in an agent-owned state.
  The machine slot is free (`ENG-027` container, both children parked)
  but nothing is startable under verified authority; `IDLE-2026-09-07.md`
  already says so, is not stale, and is not duplicated. The open P0
  (`inbox/2026-09-08-eng-loop-integrity-check.md`) still awaits the
  approver's confirm-or-reject; unchanged, not duplicated. business-os
  left uncommitted — standing default.

- `2026-09-08` **`continue` — next hop after the watch event: fresh
  re-confirmation from source, nothing changed, nothing new acted on.**
  (eng-manager, `continue ENG-027`). Reading map: steps 6 and 6b, plus the
  not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four
  lanes*, *Guards*) — not mid-PRD, step 2's checkpoint note doesn't apply.
  Cross-checked against `traces/eng-loop-2026-09-08.log` itself rather than
  only the ticket log's narrative: the watch pass ended cleanly
  (`pass end: watch (exit 0, 633s)` at `10:26:09` local), this event was
  the very next thing drained (`10:31:13`), nothing else ran in between.
  On entry the trace read `[day 23/200 charged, 0 refunded today, ENG-027
  19/20]` — this pass is the ticket's 20th charged hop today under the
  per-ticket counter, so a further `continue ENG-027` later today would be
  dropped by that ceiling. Not a fresh finding: this is the same
  nightly-resetting counter bug the 30th hop already flagged in
  `observations.md`, noted here only because it's now one hop from
  binding, not re-diagnosed. Mode check clean (repo-root `.env` →
  `MODE=active`; instance `config/config.yaml` → `mode:` empty). Pre-pass
  `eng-gate-check.sh`, whole-board (`ENG_INSTANCE="$PWD" sh
  .../lib/eng-gate-check.sh`): exit `0`, clean.

  **`ENG-027` itself: no transition, re-confirmed fresh, not assumed from
  the checkpoint.** `ENG-048`/`ENG-049` both still `blocked`/`blocked_on:
  approver`/`blocked_from: ready-to-ship`; PR `#21` (base `main`) and `#22`
  (base `feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron`,
  stacked) re-verified `OPEN`, `mergedAt: null` via `gh pr view
  --json state,mergedAt,baseRefName` run from inside the department's own
  `_eng/aiorders-api` worktree (`cd`+`pwd` confirmed). Nothing changed on
  this family since the prior hop.

  **Step 7 (notify sweep):** current time re-pulled (`date -u`:
  `2026-09-08T17:35:28Z`) and checked against every open item's own
  `notified:`/`nudged:` fresh — `grep` across all of `inbox/*.md`, not
  taken on any prior pass's arithmetic. Two items remain under the 24h
  threshold with no `nudged:` yet: `inbox/2026-09-07-eng049-merge-request.md`
  (~22h51m) and `inbox/IDLE-2026-09-07.md` (~22h51m). `inbox/2026-09-08-eng-loop-integrity-check.md`
  (the P0) is only ~7h37m old, nowhere near its one-ever nudge. The
  remaining eight open items already carry their one-ever `nudged:` and
  were left untouched. Nothing sent this pass.

  **The disputed designed-pool amendment: re-checked both load-bearing
  facts fresh, from source, independently of the ticket log's or the watch
  event's own narrative — nothing changed.** `grep -n "2026-09-08"
  agents/eng-manager/config/decision-journal.md`: still no output.
  `grep -rn "^decision:" inbox/*.md`: still no output, across all 11 open
  items. `traces/.pending` no longer exists as a file at all (queue fully
  drained, independently re-confirmed rather than repeated from the watch
  event's word). `inbox/IDLE-2026-09-07.md` confirmed still sitting in
  `inbox/` proper (not `_handled/`) via a fresh `ls`.
  `inbox/2026-09-08-eng-loop-integrity-check.md` read in full: still ends
  on the 17:09Z update, no further reply appended. **No new evidence
  exists in either direction, so this pass reaches the same conclusion the
  31st hop and the watch event already reached: the text is not acted
  on.** This is a third independent re-confirmation, not a fresh judgment
  call — reverting to the literal procedure text with no new evidence
  would make the department's behavior depend on which hop happens to run
  next, which is exactly the instability the open P0 exists to prevent
  until the approver actually answers.

  Board's own To-do column re-confirmed fresh: `ENG-018`, `ENG-028`,
  `ENG-042`, `ENG-043` all still on their own unanswered gate items (same
  `decision:` grep above covers these). Machine slot free (`ENG-027`
  container, both children parked) but nothing startable under verified
  authority — the `designed` pool's nine tickets (five `P0`) remain
  excluded only by the unverified-authority question, not by their own
  state.

  **8b:** nothing new to file — every fact re-confirmed above was already
  logged by the 31st hop or the watch event; filing it again would be
  duplication, not a new observation. No `exception-request:` found
  anywhere. **8c:** n/a — nothing answered this pass.

  **Board update:** this ticket's own row only. `board/_index.md`'s
  In-flight table is still accurate and its three dated entries are
  unchanged (keep-three rule: exactly three `## {date} —` headers present,
  nothing to roll); a pure re-confirmation with no new fact doesn't
  warrant a fourth, same call the watch event itself made.

  Post-pass `eng-gate-check.sh`, whole-board: run after this entry.

  `chained: none — idle: nothing startable under verified authority;
  IDLE-2026-09-07 unchanged, not duplicated; integrity-check P0
  (inbox/2026-09-08-eng-loop-integrity-check.md) unchanged, not due a
  nudge, still awaiting the approver's confirm-or-reject`. business-os
  left uncommitted — standing default.

- `2026-09-08` **`building → shipped → verified` — both children found
  shipped mid-pass while re-verifying the checkpoint; parent settled the
  same pass under `ADR-003`; item 4 of the sequence (`ENG-051`) filed per
  step 6b.** (eng-manager, `continue ENG-027`, launched
  `11:06:38` local on account 3/3 after an account-2 rate-limit
  never-started at `11:01:33` — `traces/eng-loop-2026-09-08.log`.) Reading
  map: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10;
  *Enforced vs instructed*; *The four lanes*; *Guards*) — not mid-PRD, step
  2 doesn't apply. **Process note, named plainly rather than glossed over:
  the pre-pass gate check did not run at the top of this pass** — this hop
  went straight into re-verifying the checkpoint instead. Run mid-pass,
  after discovering the merges but before any state edit: exit `0`, clean,
  both invocation forms (`sh .../lib/eng-gate-check.sh` and `env
  ENG_ROOT="$(pwd)" sh ...`). No violation found either way, but the skip
  itself is a process miss worth naming, not a fact worth hiding. **Second
  process note:** the live `supabase secrets list`/`functions list` checks
  below ran with `--project-ref` from this instance's own working
  directory rather than the `_eng/aiorders-api` worktree — harmless to the
  project (read-only, and the ref was explicit) but it left a stray
  `supabase/.temp/` cache directory in this instance's own repo, caught in
  this pass's own closing `git status` review and removed before this
  entry was written (confirmed empty after). Not the repo-isolation guard
  `config/projects.md` actually protects against (that's about writing in
  the *human's* interactive checkout; this is a different repo entirely),
  but worth naming so a future pass reaches for the worktree by habit
  regardless of which command it's running.

  **Mode check clean:** repo-root `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty (both re-read fresh, not taken from
  the checkpoint).

  **The checkpoint's own claims verified fresh before use, per the
  standing rule that the file on disk — not the copy — is authoritative.**
  Every load-bearing fact the checkpoint carried forward (mode, the
  disputed designed-pool text's non-corroboration, `IDLE-2026-09-07`'s
  location, the P0's unanswered state) re-confirmed accurate as of when
  the *previous* hop wrote it. What had changed since: `traces/.pending`
  now held a queued `scheduled auto-drain` (not empty as the checkpoint's
  hop had found — a fact of the moment, not a discrepancy), and, far more
  materially, **both of this ticket's children's PR state.**

  **The disputed `designed`-pool amendment: re-checked fresh, independently
  of every prior hop's word — still unconfirmed, now with one genuinely
  new wrinkle, handled rather than left to confuse a future check.**
  `decision-journal.md`: no 2026-09-08 entry *about the designed-pool
  decision* — but this pass's own work below added two 2026-09-08 rows for
  routine `ENG-048`/`ENG-049` merge journaling, so the file now has
  *2026-09-08 entries*, a fact a shallow re-check could mistake for
  corroboration. Flagged explicitly, in three places, so it isn't:
  `observations.md` (2026-09-08, last row), an addendum to
  `inbox/2026-09-08-eng-loop-integrity-check.md`, and here. `inbox/*.md`
  `^decision:` grep: still zero hits, across every open item including the
  two now-archived merge requests before their move. **Not acted on, same
  as every prior hop** — nothing drawn from `designed` for the freed slot
  (below).

  **`ENG-048` merge found and processed.** The checkpoint (copied from the
  prior hop) read PR #21 `OPEN`. Re-verified fresh via `gh pr view` from
  `_eng/aiorders-api`: `MERGED`, `18:05:03Z`, no written reply. Gates
  re-read fresh (review/QA/security all `pass`), migration confirmed
  actually applied to production (`supabase migration list --linked`, not
  just merged to `main`). `blocked → shipped → verified` — full detail,
  including the closed cron-observability gap and its one remaining
  unwatched follow-up (first live tick, expected `18:30:00Z`): the
  ticket's own board-file log, release record
  (`agents/devops/releases/2026-09-08-aiorders-api-ENG-048.md`), acceptance
  walk (`agents/product-manager/notebook/2026-09-08-eng048-acceptance.md`).

  **`ENG-049` merge found and processed — the harder of the two, a stacked
  PR resolved properly rather than assumed.** PR #22 showed `MERGED` but
  into its own base (`feat/ENG-048-...`), not `main` — checked by ancestry
  (`git merge-base --is-ancestor ... origin/main`: true, via a third PR,
  #23, `18:16:55Z`) rather than trusted from PR state alone, per
  `eng_build_loop.md` step 5's stacked-PR provision. **The one thing that
  had to be right before calling this deploy safe:** `ENG-049`'s own
  release-readiness hop (2026-09-07) had flagged
  `CLOUDWAITRESS_WEBHOOK_SECRET` as unprovisioned and a hard pre-deploy
  requirement — missing it would 401 *all* CloudWaitress traffic, not only
  loyalty. Checked live: present, `updated_at: 18:12:56Z`, set between PR
  #21's merge and the actual functions deploy (`18:17:3xZ`) — correct
  order, incident avoided. Deploy confirmed live via `supabase functions
  list` (`external-integrations` v109, `brand-portal` v86,
  `loyalty-auto-complete` v1 brand-new, all within a 7-second window).
  `blocked → shipped → verified`. Full detail: the ticket's own board-file
  log, release record
  (`agents/devops/releases/2026-09-08-aiorders-api-ENG-049.md`), acceptance
  walk (`agents/product-manager/notebook/2026-09-08-eng049-acceptance.md`).

  **This ticket (`ENG-027`) itself: `building → shipped → verified`,
  `ADR-003` exemption met** (both children `verified`, both actually
  shipped) — no diff, review, QA, or security hop of its own, same
  no-receipts-owed shape `ENG-016`'s and `ENG-021`'s own parent closures
  used. **Ran `acceptance-check/SKILL.md` in full despite the exemption**
  (the trigger has no parent carve-out): all 18 of the PRD's criteria
  walked as a rollup, cross-referenced from both children's own fresh full
  walks rather than re-derived — all pass, no criterion left with an
  unproven half. Non-goals swept whole-family (no backfill, no
  edit/delete of a ledger row, no cross-restaurant balance movement, no
  scope creep toward items 4/5 of the sequence). Cost `$0/month`, matching
  both children's own independent estimates. Full walk:
  `agents/product-manager/notebook/2026-09-08-eng027-acceptance.md`.

  **Two transitions on this ticket** (`building → shipped`, `shipped →
  verified`); **two more each on `ENG-048` and `ENG-049`**
  (`blocked → shipped → verified` apiece) — three separate per-ticket
  budgets, none near the 4-per-pass cap.

  **Step 6b — continue an approved sequence: condition met, unlike
  `ENG-016`'s and `ENG-021`'s own closing checks.** This PRD's own
  `## Readback` names the sequence (`ENG-006`'s `## Feature shape and
  sequencing`) and the standing authorization to file incrementally
  (`ENG-006`'s G1, 2026-08-28: "the proposed five-ticket sequence stands
  as shape to file incrementally"). `ENG-027` is item 3; item 4
  ("Redemption API and QR issuance/scanning... Depends on ENG-006 and
  (3)") is now dependency-clear. **Filed the stub only** (`ENG-051`,
  `board/_index.md` `Next ID` → `ENG-052`) — step 1b (id, project, type,
  size, lane, one-line problem, `depends_on`), not the PRD content.
  Checked the reason to stop before asserting it: `prd-writer/SKILL.md`
  declares `Model: opus`, which first read as the reason, but
  `lib/eng-trigger.sh`'s `pass_model()` shows opus routing was retired
  department-wide 2026-08-20 (the approver's own direct instruction) —
  every hop, including whatever picks up `ENG-051`, runs the same
  `sonnet`+`--effort max` tier this pass itself does. Stopped at the stub
  anyway, for the reason `eng_build_loop.md` step 2 gives PRD-writing
  generally (open-ended judgment, not a rush job on top of an
  already-long pass), not a model-tier one. Full reasoning on both counts:
  `ENG-051`'s own board-file log and `board/_index.md`'s `Next ID` note.
  `chained: ENG-051` fired before this pass exits.

  **Step 8c (journal):** two entries added to
  `agents/eng-manager/config/decision-journal.md` — `ENG-048`'s L1 merge
  and `ENG-049`'s stacked L1 merge, same format every prior silent
  GitHub merge on this board has used.

  **Step 8b (observations):** three filed —
  (1) the newly-present GitHub Actions Supabase auto-deploy workflow on
  `aiorders-api`, undocumented in `config/projects.md`;
  (2) `ENG-048`'s migration's own rollback comment ("safe any time before
  `ENG-049` ships") now stale, both tickets live;
  (3) the decision-journal disambiguation above, so a later pass doesn't
  misread this pass's own routine merge rows as designed-pool
  corroboration. No `exception-request:` found anywhere touched this pass.

  **Inbox housekeeping:** `inbox/2026-09-07-eng048-merge-request.md` and
  `...-eng049-merge-request.md` moved to `inbox/_handled/` — both shipped,
  same archival every resolved merge-request item on this board has had,
  `decision:` left blank on both (never answered, same as roughly twenty
  prior silent merges this journal already records). `inbox/IDLE-2026-09-07.md`
  updated in place (not re-raised — one item per idle episode): the
  premise changed (family fully terminal, not merely parked; `ENG-051`
  added as a fifth To-do occupant of the same non-`designed` kind) but the
  conclusion didn't (still nothing startable without the approver — same
  literal To-do reading every prior hop has used, `designed` still not
  drawn from). `inbox/2026-09-08-eng-loop-integrity-check.md` got the
  decision-journal disambiguation addendum only — its `decision:` field
  untouched, still the approver's alone.

  **Step 7 (notify sweep), timestamp re-pulled immediately before writing
  this entry (`2026-09-08T18:38:47Z`), not reused from earlier in this
  long pass:** `IDLE-2026-09-07` (`notified: 2026-09-07T18:44:54`) is
  ≈23h54m — still under 24h by several minutes, genuinely close given how
  long this pass has run; re-check at exit, below. `eng-loop-integrity-check`
  (≈8h40m) is nowhere near. `eng050-p0-incident` and every G1/rescope/
  clarification item already carry their one-ever `nudged:`. Nothing
  raised or nudged at this check.

  **Machine WIP: `1/1 → 0/1`, free — the whole `ENG-027` family is now
  terminal.** Swept To-do fresh: `ENG-018`, `ENG-028`, `ENG-042`, `ENG-043`,
  and now `ENG-051` — none `designed`, all correctly excluded under the
  confirmed (not the disputed) reading. `ENG-050` (P0, `designed`, sized,
  ready to start) remains the one candidate worth naming directly, same as
  every prior hop has named it — not started, still the approver's call to
  override.

  **Board update, this pass:** `_index.md`'s In-flight table — `ENG-027`,
  `ENG-048`, `ENG-049` rows removed (terminal); `ENG-051` row added.
  `Next ID` counter updated with reasoning. Live file held three dated
  entries before this one; oldest (`scheduled (launchd)`, 30th-confirmation
  entry) rolled to `_index-archive.md` per the keep-three rule, done
  before this entry was written.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh`, whole-board
  (both invocation forms): exit `0`, clean, run after every edit above.

  `chained: ENG-051` — the only ticket this pass leaves in an agent-owned
  state (`intake`, PM-owned PRD shaping). `ENG-027`, `ENG-048`, `ENG-049`
  are all terminal (`verified`) and do not chain. business-os left
  uncommitted — standing default, not re-decided here.
