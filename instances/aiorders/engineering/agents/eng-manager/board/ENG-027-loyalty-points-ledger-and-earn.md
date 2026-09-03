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
state: awaiting-scope
owner: approver
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-03
updated: 2026-09-03
branch:
depends_on: [ENG-006, ENG-007]
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-027-loyalty-points-ledger-and-earn.md
  design:
  adrs: []
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

**One rider on the G1** (same bar `ENG-015`/`ENG-016` used): what the earn
% applies to — proposed as the pre-tax, post-discount food subtotal,
excluding tax/fees/delivery/tip. `ENG-007` stored a percentage; nobody
has ever said a percentage of what. **Still unanswered as of the rescope** —
the `changed` answer addressed accrual timing and was silent on this, and
silence isn't read as approval, so it is carried forward onto the fresh G1
rather than treated as settled. Three further riders joined it there; see
the log entry below.

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
