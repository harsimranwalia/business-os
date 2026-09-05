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
state: designed
owner: architect
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-03
updated: 2026-09-05
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

**Branch: shared, not per-ticket.** Per the approver's own instruction
recorded on `ENG-006`'s ticket and restated on `ENG-007`'s (lines
109–113), the whole loyalty sequence shares one branch, `loyalty-system`,
in `aiorders-api`. Whoever picks this up at `building` branches from (and
merges back into) `loyalty-system`, not a fresh `feat/ENG-027-...` off
`main`.

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
