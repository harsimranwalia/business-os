---
id: ENG-011
title: Client stage & health visibility on the Brands admin page — plus stage filtering
project: aiorders-admin-hub
type: feature
size: M
time_estimate: half a day to a couple of days
time_spent: not separately clocked — build, review, QA, security and the
  database gate all completed in an unrecorded prior pass (see Log); read as
  most of the estimate consumed
time_remaining: "0 — verified, closed out"
severity: P3
priority:
state: verified
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-08-30
branch: feat/ENG-011-client-stage-health-visibility (same name, both repos)
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-011-client-stage-health-visibility.md
  design: agents/architect/designs/ENG-011-client-stage-health-visibility.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-011.md
  test_plan: agents/qa/test-plans/ENG-011.md
  security_review: agents/security/reviews/ENG-011.md
  release: agents/devops/releases/2026-08-29-aiorders-admin-hub-ENG-011.md
  pr: "aiorders-api: https://github.com/harsimranwalia/aiorders-api/pull/3 | aiorders-admin-hub: https://github.com/harsimranwalia/aiorders-admin-hub/pull/3"
---

## Input

Verbatim, from
`agents/product-manager/inbox/2026-08-29-on-the-admin-panel-we-are-unable-to-see-if-the-restaurant-is.md`
(now `agents/product-manager/inbox/_handled/`), filed by the approver, `via:
control-center`, received 2026-08-29T08:17:22.970586+00:00 — preserved here
per `skills/request-readback/SKILL.md` step 1, never edited:

> # on the admin panel we are unable to see if the restaurant is our client or what stage he is at on the brands page we have.
>
> the admin staff should be able to filter according to the stage of the client so they can prioritize the clients based on the stage they are at . also the health of restaurant and maybe tickets

## Readback

See
`agents/product-manager/specs/ENG-011-client-stage-health-visibility.md` →
Readback — the full two-reading comparison lives there rather than
duplicated here.

## Problem

Admin staff working the Brands page can't tell which restaurants are
actual clients versus earlier-stage or inactive ones, and can't see a
restaurant's health — so the list can't be worked in priority order.

## Outcome

Staff can see each restaurant's client stage and a minimal health signal
on the Brands page, and can filter the list by stage.

## Notes

**Scope split, not the whole raw request.** The raw input bundles four
things: (1) client-stage visibility, (2) filtering by stage, (3) a health
signal, (4) "maybe tickets." This ticket is (1)+(2)+(3). Item (4) is a
standing, non-blocking question with the approver
(`inbox/2026-08-29-eng011-tickets-source-question.md`) rather than folded
in or dropped — same move `ENG-008` made for its own "engagement" item, and
for the same reason: the answer swings cost by roughly an order of
magnitude and neither independent reading could resolve it from the text.

**Evidence found, not assumed.** `aiorders-admin-hub`'s live worktree
(`src/pages/Brands.tsx`) confirms the page exists, and today filters only
`'all'` vs `'website_created'` — no stage, client, health, or ticket
concept anywhere on it. Its `Brand`/`Restaurant` interfaces already carry
`onboarding_step: number` (a real onboarding wizard writes it, per
`aiorders-api`'s `restaurant-portal-onboarding/brands.ts`) and `is_active`
(set at brand creation, per `restaurant-claims/index.ts`) — raw signals
that already exist but aren't surfaced or labeled on this page. Searched
`aiorders-api`'s migrations and functions for `stage`, `lifecycle`,
`health`, `last_order`, `churn`, `ticket`, `support` — none exist. So the
proposed stage taxonomy in the PRD is grounded in real columns, and
"tickets" is confirmed net-new rather than an extension of something
already there — the standing question is asking what it should draw from,
not whether it exists.

**Project scoping.** Primary project set to `aiorders-admin-hub` (the
literal admin panel, where acceptance criteria are observed), same split
precedent `ENG-003`/`ENG-008` used: the other repo's work
(`aiorders-api` — a stage-bearing column/mapping) is named here rather
than inventing a multi-project ticket shape. Both worktrees already exist
on this host (`_eng/aiorders-admin-hub`, `_eng/aiorders-api`).

**One item intentionally not filed yet:** "tickets" — a standing,
non-blocking question is open with the approver
(`inbox/2026-08-29-eng011-tickets-source-question.md`). Does not block this
ticket. Will become its own small ticket, or fold into a later one, once
answered.

**Found and left untouched, out of scope for this `intake` event's own
narrower contract:** `inbox/2026-08-29-eng009-g1-scope.md` and
`inbox/2026-08-29-eng010-g1-scope.md` both carry `decision: approved`
(decided 09:20:42 and 10:49:55 respectively) but are still sitting in
`inbox/` — their tickets (`ENG-009`, `ENG-010`) still read `state:
awaiting-scope`, `owner: approver` on disk. Verified fresh rather than
trusted from the board index (which is stale on this point — see board
entry). Treated both as **answered, not open**, for this pass's own
approval-cap and approver-WIP arithmetic — consistent with this instance's
own established convention (an answered gate item is "off the list"
immediately, board index precedent, e.g. `ENG-007`'s G2) rather than the
mechanical `state:` field, since the cap exists to protect the approver's
attention, and their attention is not what's pending here — department
follow-through is. Not processed (no state advance, no journal, no
archive) — that's dead-end-sweep/decision-event work on two unrelated
tickets, out of bounds for an `intake` event scoped to this one request.
Filed as an observation, not fixed, since fixing it isn't this pass's job
either.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-29` `intake → shaped → awaiting-scope` (product-manager,
  `intake` event pass, context this exact request file). Mode check clean
  (business-os `.env` → `MODE=` empty). Caps checked fresh from ground
  truth rather than the (stale) board index before raising G1:
  approver-facing WIP 0/2, approval cap 0/3 — both readings treat
  `ENG-009`/`ENG-010`'s answered-but-unprocessed G1s as closed, not open
  (see Notes). Both fully free either way this pass reads them.

  **Ran the full request-readback** (`skills/request-readback/SKILL.md`):
  this PM's own reading plus a blind architect reading (subagent, `opus`,
  raw request + `knowledge/business-profile.md` only, no repo access, no
  exposure to this PM's own reading). **No material divergence** — both
  converged on the same shape (missing stage/client concept, explicit
  filter requirement, undefined health, undefined tickets). The
  architect's reading additionally named a one-way-door risk (a manually
  set "is client" flag drifting from stage if client status is ever
  derived from billing) — folded into the PRD's proposed
  one-field-answers-both approach rather than treated as a fork.

  **Checked the live repos before proposing defaults**, same practice
  `ENG-005`/`ENG-008` established: confirmed `Brands.tsx` exists with no
  stage/health/ticket concept today, found `onboarding_step`/`is_active`
  as real existing signals to ground a proposed stage taxonomy, and
  confirmed no ticket/support system exists anywhere in either repo —
  turning what could have been three separate approver questions into two
  evidence-grounded proposed defaults (stage taxonomy, health signal) plus
  one genuine standing question (tickets), rather than asking three or
  guessing three.

  **PRD written**:
  `agents/product-manager/specs/ENG-011-client-stage-health-visibility.md`,
  acceptance criteria + non-goals naming the tickets item explicitly.

  **G1 required** — full lane, not XS/bug/chore. Wrote
  `inbox/2026-08-29-eng011-g1-scope.md` (`agent: product-manager`, `gate:
  scope`, `project: aiorders-admin-hub`, recommendation to build now).
  Separately wrote the non-blocking standing question,
  `inbox/2026-08-29-eng011-tickets-source-question.md` (`agent:
  product-manager`, `gate: intake-question`) — kept separate rather than
  folded into the G1 text, same reasoning `ENG-008`'s engagement question
  used: it scopes a possibly-different, not-yet-filed future ticket, not a
  condition on approving this one.

  Ran `departments/engineering/lib/eng-notify.sh raise` on both files; see
  each item's own frontmatter for the result and `notified:` timestamp.

  **No dissent section** — `agents/critic/agent.md` doesn't exist at the
  department or instance level (confirmed absent again this pass, same
  open proposal, `proposals.md` 2026-08-25 row); not refiled.

  **State:** `intake → shaped → awaiting-scope`, all in this pass. `owner`
  moves `product-manager → approver`. **Consequence:** approver-facing WIP
  0 → 1 (cap 2); approval cap 0 → 2 (the G1 plus the standing question,
  counted conservatively, same convention `ENG-008` used). `machine_wip`
  unaffected.

  **Dead-end sweep:** out of scope for this `intake` event's own narrower
  contract (act on the named request; don't sweep the whole board) — not
  run beyond the fresh cap-verification above. `ENG-007`, `ENG-008`,
  `ENG-009`, `ENG-010` untouched.

  **Notify sweep:** both of this pass's own items raised and stamped
  above. Nothing else to nudge. Approval cap 2/3 (this pass's own read),
  not full — no stall.

  **Observations filed** (`observations.md`): the confirmed-absent
  stage/health/ticket concepts and the evidence grounding the proposed
  taxonomy; the `ENG-009`/`ENG-010` answered-but-unprocessed gate items
  found while verifying caps.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-011`) and
  whole-board: exit 0, clean.

- `2026-08-29` `awaiting-scope → designed → ready` (architect, then
  eng-manager — same `intake` event pass, continued). The approver
  answered this ticket's own G1 by hand-edit (`decision: approved`,
  `decided: 2026-08-29T11:14:54.862156+00:00`, bare approval, no rider)
  while this pass was still running. Per this instance's established
  practice (whichever event reaches a fact first does the real work — see
  `ENG-007`'s and `ENG-008`'s own G1 log entries), processed it here rather
  than leaving it for a separately-queued `decision` event to rediscover
  as a no-op. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-011`) and whole-board: both exit 0, clean.

  **Real design work done against the live repos**, same practice
  `ENG-005`/`ENG-007`/`ENG-008` established. Checked `aiorders-api`'s
  order data before assuming the PRD's "no new cost" health claim would
  hold: `get-online-orders` proxies live to a third-party vendor
  (CloudWaitress, `cw_api_key`/`cw_restaurant_id`) for some paths, which
  could have meant no cheap internal order history existed — but
  `20260217000001_platform_analytics_cron.sql` confirmed a real internal
  `orders` table (`restaurant_id`, `total_amount`) and an existing hourly
  cron (`calculate_platform_analytics()`) already aggregating
  `total_orders`/`total_order_value` per restaurant into Cloudflare KV.
  Checking paid off by confirming feasibility rather than finding a
  landmine this time (unlike `ENG-007`'s Walletly discovery) — health can
  reuse this existing pipeline with one added column
  (`last_order_at`) rather than a new query path or job.

  **Design**: `agents/architect/designs/ENG-011-client-stage-health-visibility.md`.
  `stage` and `health` both derived at read time (from `is_active`/
  `onboarding_step`, and from the extended analytics aggregate,
  respectively) rather than new stored fields — this is what closes the
  drift-risk the G1 readback itself flagged for a separately-set "client"
  column. No new table, no new vendor, no new datastore; one additive
  column in an existing aggregate function's output is the only schema
  change. **No one-way door** — moved straight through `designed`, no G2.

  Moved the G1 gate item to `inbox/_handled/` with a processed footer;
  journaled in `agents/eng-manager/config/decision-journal.md`.

  **2 transitions this pass** (`awaiting-scope → designed → ready`) on top
  of the 2 already spent shaping the ticket earlier in this same pass — 4
  total, at the cap of 4, stopping here by design: `building` needs a
  backend/frontend/database engineer actually writing code, new
  implementation work this pass does not do. **Consequence:**
  approver-facing WIP 1/2 → 0/2 (substantively; see board index for the
  `ENG-009`/`ENG-010` mechanical-vs-substantive note, unaffected by this
  ticket's own move either way); approval cap 2/3 → 1/3 (this ticket's G1
  closed; its standing "tickets" question also closed this same pass, see
  below); machine WIP 2/6 → 3/6 (`ENG-011` now inside the counted
  `ready`..`ready-to-ship` range alongside `ENG-007`/`ENG-008`).

  **The standing "tickets" question was also answered this same pass** —
  `decision: rejected` with free-text "Reading A," read together as
  "build Reading A" rather than a flat no (full reasoning on the gate
  item's own processed footer, `inbox/_handled/2026-08-29-eng011-tickets-source-question.md`).
  Shaped directly into `ENG-012` (own board file, PRD, and G1) in this
  same pass, per the same sequence-continuation reasoning
  `ENG-006`/`ENG-007`/`ENG-008` established — this item itself already
  named filing the next ticket as its own next step once answered.

  **Dead-end sweep:** scoped to this event's own lineage — `ENG-007`,
  `ENG-008`, `ENG-009`, `ENG-010` untouched. **Notify sweep:** nothing new
  to raise for this ticket (a gate closing doesn't get re-notified);
  `ENG-012`'s own G1 raised separately, see its own log. **Observations
  filed** (`observations.md`): the confirmed-live internal orders/analytics
  pipeline; the ambiguous `rejected`+free-text answer shape.

  `chained: ENG-011` — `ready` is eng-manager-owned (a
  backend/frontend/database engineer builds next), not the approver, not
  blocked, not terminal, not held by a cap. Fired
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-011`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-011`) and whole-board: see pass notes.

- `2026-08-29` **the predicted twin no-op: G1 scope decision event arrived
  after its own fact was already consumed** (eng-manager, `decision` event
  pass, context `inbox/_handled/2026-08-29-eng011-g1-scope.md`). Same
  duplicate-queued-event shape already logged for `ENG-008`'s two gate
  items, `ENG-009`'s G1, and `ENG-010`'s G1. Per this event's own narrower
  contract, scoped to `ENG-011` only — no board-wide sweep. Mode check
  clean (business-os `.env` → `MODE=` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-011`) and
  whole-board: both exit 0, clean.

  **Confirmed rather than assumed.** `traces/eng-loop-2026-08-29.log`:
  `10:59:40 queue: collapsed 2 duplicate event(s)` fires immediately before
  `10:59:40 draining queued event: decision (2026-08-29-eng011-g1-scope.md)`
  — duplicate copies of this event collapsed to the oldest, which is this
  pass. This item's frontmatter carries a processed footer naming the exact
  pass that consumed it — the same `intake` pass that raised it, which
  caught the approver's hand-edit (`decision: approved`, `decided:
  2026-08-29T11:14:54.862156+00:00`) while still running: architect design
  work done (`stage`/`health` both derived at read time from existing
  columns/pipelines, no new stored fields — closing the drift-risk the
  readback itself flagged), the ticket carried `awaiting-scope → designed →
  ready` in the log entry directly above, journaled
  (`agents/eng-manager/config/decision-journal.md`, row 26), and the gate
  item itself already moved to `inbox/_handled/`. Checked fresh rather than
  trusted: this ticket's own frontmatter (`state: ready`, `owner:
  eng-manager`) and the journal row both agree with the footer. Nothing
  left for this event to act on.

  **0 transitions.** No cap affected — this ticket was already inside the
  counted `ready`..`ready-to-ship` machine-WIP range (6/6, at cap) before
  this pass, and this G1 was already off both the approver-facing WIP and
  approval-cap counts.

  **Dead-end sweep (scoped to this event):** confirmed `continue ENG-011` —
  fired by the pass directly above — still sitting in `traces/.pending`,
  undrained, behind several older not-yet-drained fires; not a broken
  chain, just not yet its turn in the FIFO queue. Unlike `ENG-009`/
  `ENG-010`, this ticket carries no documented sequencing hold against a
  sibling ticket — nothing else in flight on `aiorders-admin-hub` touches
  `Brands.tsx` — so once that fire reaches the front it should proceed
  straight into `building` rather than parking again.

  **Notify sweep:** nothing to raise (no new gate item); nothing to nudge
  (this item's `notified:`/`decision:` cycle closed same-day, hours before
  this pass).

  `chained: none` — no state change; this ticket's existing chain
  (`continue ENG-011`) is already queued and will run on its own turn.
  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-011`) and whole-board: both exit 0, clean. Also recorded on the
  board index (`_index.md`, matching dated entry).

- `2026-08-29` **a second predicted twin no-op, same shape, different gate
  item** (eng-manager, `decision` event pass, context
  `inbox/_handled/2026-08-29-eng011-tickets-source-question.md`). This
  ticket's standing "tickets" question was queued as its own separate
  `decision` event, independent of the G1-scope twin logged directly
  above — same duplicate-queued-event shape already seen five times today
  (`ENG-008`'s two gate items, `ENG-009`'s G1, `ENG-010`'s G1, `ENG-011`'s
  own G1). Per this event's own narrower contract (act on the answered
  gate item, advance only the ticket it belongs to), scoped to `ENG-011`
  only — no board-wide sweep. Mode check clean (business-os `.env` →
  `MODE=` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-011`) and whole-board: both exit 0, clean.

  **Confirmed rather than assumed.** `traces/eng-loop-2026-08-29.log`:
  `11:13:54 queue: collapsed 3 duplicate event(s)` fires immediately before
  `11:13:54 draining queued event: decision
  (2026-08-29-eng011-tickets-source-question.md)`, pass start `11:13:55`,
  claude launched `11:14:48`. By the time this pass reached the file, the
  fact was already fully consumed — and not just consumed but carried to a
  closed end: the same `intake` pass that raised this standing question
  caught the approver's hand-edit (`decision: rejected`, free text "Reading
  A", `decided: 2026-08-29T11:16:32.000840+00:00`) while still running,
  read the two together as a selection of Reading A rather than a flat
  rejection (full reasoning on the gate item's own processed footer),
  shaped it directly into `ENG-012` in that same pass (own PRD, own G1),
  and journaled the read (`decision-journal.md` row 27). Checked fresh
  rather than trusted: the gate item's frontmatter and footer, the journal
  row, and `ENG-012`'s own board file all agree — and `ENG-012`'s own log
  shows the thread went further still, in a later `scheduled` pass: its G1
  came back `rejected` ("later"), and it reached terminal `state: dropped`.
  Nothing of this remains open anywhere.

  **0 transitions.** No cap affected — `ENG-011` was already inside the
  counted `ready`..`ready-to-ship` machine-WIP range (6/6, at cap) before
  this pass, and this standing question was already off both
  approver-facing WIP and the approval cap (closed the same pass it was
  raised).

  **Dead-end sweep (scoped to this event):** re-confirmed `continue
  ENG-011` still sitting in `traces/.pending`, undrained — now behind a
  considerably longer backlog than when the G1-scope twin entry above last
  checked (fires for `ENG-013` through `ENG-024` have since queued). Still
  not stuck: `ENG-011` carries no documented sequencing hold against a
  sibling ticket, so this is purely FIFO position, not a parked wait.

  **Notify sweep:** nothing to raise (no new gate item); nothing to nudge
  (this item's `notified:`/`decision:` cycle closed same-day, hours before
  this pass).

  `chained: none` — no state change; `ENG-011`'s existing chain (`continue
  ENG-011`) is already queued and will run when it reaches the front.
  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-011`) and whole-board: both exit 0, clean. Also recorded on the
  board index (`_index.md`, matching dated entry).

- `2026-08-29` `ready → building → in-review → in-security → ready-to-ship`
  (backend/database/frontend, then principal-engineer + qa combined, then
  security — `continue` event pass, context `ENG-011`, its actual turn at
  the front of `traces/.pending` this time). Narrow scope per the event's
  own contract (resume this ticket from its current state; no board-wide
  sweep). Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  **Recovered a fully unrecorded build — the same failure family `ENG-006`
  named first and `ENG-007` showed one step further along, now a third
  time.** This ticket's own frontmatter and log still read `ready` at pass
  start, but both `_eng` worktrees (`C:/Users/jerryai/Documents/_eng/aiorders-admin-hub`,
  `.../aiorders-api`) already carried the `feat/ENG-011-client-stage-health-visibility`
  branch, pushed, and **all four gate receipts already existed on disk**
  with `pass` verdicts, all referencing the same commits:
  `agents/database/migrations/ENG-011-client-stage-health-visibility.md`,
  `agents/principal-engineer/reviews/ENG-011.md`, `agents/qa/test-plans/ENG-011.md`,
  `agents/security/reviews/ENG-011.md`. Unlike `ENG-007`'s recovery (where
  the ticket's own bookkeeping was the only thing behind), this ticket's
  board file hadn't been touched at all since it was set to `ready` two
  passes ago — consistent with the chain firing correctly each time
  (visible in both prior no-op log entries above) and this ticket simply
  not having reached the front of the FIFO queue until now, at which point
  a build pass ran to completion, wrote all four receipts, and then didn't
  reach the board-file write. `traces/eng-loop-2026-08-29.log` confirms
  the queue depth both prior entries flagged (`ENG-013` through `ENG-024`
  ahead of this ticket) was real, not a stall.

  **Verified fresh rather than trusted, before recording anything —**
  same practice this board has used at every recovery so far, extended
  one step further here:
  - `git status`/`log`/`diff --stat` in both worktrees: `aiorders-admin-hub`
    at `6cf5e8c` (1 commit, `Brands.tsx` only, matches the review's own
    diff reference exactly); `aiorders-api` at `4a5eb4d` (2 commits, 6
    files, matches exactly). Both `[origin/feat/ENG-011-client-stage-health-visibility]`,
    pushed. One unrelated, harmless artifact noted and left alone:
    `aiorders-admin-hub`'s `package-lock.json` carries unstaged `"peer":
    true` metadata churn from a newer local npm reading an older lockfile
    — no package added, removed or bumped; not part of this ticket's diff,
    not committed.
  - Re-ran, not trusted from the receipts: `deno test --no-check --allow-net`
    on `brands.test.ts` — **12 passed, 0 failed**, identical to the QA
    plan's own result. `npm run build` in `aiorders-admin-hub` — clean,
    3340 modules, same chunk-size warning already named as pre-existing.
  - **New verification beyond what any receipt had**: the database
    migration doc named one real residual gap — no live Postgres reachable
    on this host (Docker's daemon still doesn't come up, no `psql`, no
    `supabase` CLI — the same limitation `ENG-007`'s migration doc first
    named, now confirmed a third time). This pass had a path the prior
    ones didn't: the Supabase MCP connection reaches the real
    `aiorders-api` project (`bmnmnejwdxbcqinqkwko`) directly. Used it
    **read-only, at zero cost**, to independently confirm what the
    migration doc could only reason through: `orders.created_at` is
    `timestamptz NOT NULL` exactly as assumed; the live
    `calculate_platform_analytics` function body is byte-for-byte
    identical to what the doc's rollback restores; `pg_depend`/`cron.job`
    against the function's OID are both empty, confirming nothing in the
    database catalog depends on it; and the migration is confirmed not yet
    applied. Full detail and reasoning: addendum on the database migration
    doc, dated this pass.

    **Deliberately not done, named rather than quietly skipped**: creating
    a Supabase branch to actually dry-run the DROP+CREATE statement was
    available (`create_branch`) but gated behind `confirm_cost` — a real
    recurring charge — and applying the migration directly to production
    before this ticket's PR has even been opened would jump the L1
    human-merge gate entirely. Neither is a call this pass makes
    unilaterally; both would need the approver first. So the gap is now
    narrower (the statement's safety is independently confirmed against
    live catalog data) but not fully closed (the statement itself has
    still never executed anywhere) — stated exactly, not rounded up to
    "verified" or left at the old, wider "not verified" either.

  **Third occurrence of the same host limitation, crossing the threshold
  this board's own observations ledger set.** The 2026-08-29 observation
  logged during `ENG-007`'s recovery named this "worth one [a proposal] if
  a future pass needs live-Postgres verification and hits the same wall a
  third time" — this is that third time (after `ENG-007`'s migration doc,
  then that same day's dead-end-sweep observation). Filed as a proposal,
  not another observation (`agents/eng-manager/proposals.md`), carrying
  the concrete finding this pass adds: the Supabase MCP connection already
  closes the read-only half of the gap for free today; what's missing is
  an approved, budgeted path for the write half (a throwaway branch,
  pre-approved up to some small monthly cap) for the rare ticket whose
  gate genuinely needs a live dry-run.

  **State recorded to match the verified reality**, `building → in-review`
  folding in `in-qa` per `config.yaml`'s own `combined_hop: [code_review,
  quality]` (no separate sit-state, same as `ENG-005`/`ENG-006`/`ENG-007`):
  `branch: feat/ENG-011-client-stage-health-visibility` (both repos);
  `links.review`, `links.test_plan`, `links.security_review` all set to
  the receipts above.

  **4 transitions this pass** (`ready→building`, `building→in-review`,
  `in-review→in-security`, `in-security→ready-to-ship`), at the cap of 4 —
  same count, same stopping point `ENG-007`'s recovery used earlier the
  same day. **Consequence:** `machine_wip` unaffected — `ENG-011` was
  already inside the counted `ready..ready-to-ship` range at `ready`,
  stays inside it at `ready-to-ship`. Approver-facing WIP and approval cap
  both unaffected — no gate raised this pass; the L1 merge request (both
  repos) is the next hop's work, same split `ENG-007` used at this
  identical boundary.

  **Release window checked fresh, independently reconfirmed, deliberately
  not acted on this pass** — same split `ENG-006`/`ENG-007` used at this
  exact boundary: `date` → Saturday 2026-08-29, 12:51 local, inside
  `releases.block_weekends`; `.env` → `MODE=` empty, no
  `ENG_RELEASE_FREEZE`; instance `config/config.yaml` → `mode:` empty.
  Flagged here so the next hop doesn't have to rediscover it, not decided
  here — opening two PRs (first cross-repo release on this board) is real,
  distinct devops work for that hop.

  **Dead-end sweep (scoped to this event):** this ticket's log now ends in
  a valid, accounted-for state with the chain record below. No sweep of
  the rest of the board — out of scope for a `continue` event naming this
  ticket specifically.

  **Notify sweep:** nothing raised this pass — a state recorded to match
  already-completed work doesn't get its own notification; the proposal
  filed above rides the weekly batch, not an immediate notify, same as
  every other proposal-lane item.

  **Observations filed** (`observations.md`): the Supabase MCP connection
  as a free, zero-setup read-only path to the live `aiorders-api`
  database, usable by any future ticket that needs to check current schema
  or catalog state without Docker/psql.

  `chained: ENG-011` — `ready-to-ship` is agent-owned (devops opens the PR
  next), not the approver, not blocked, not terminal, not held by a cap.
  Fired `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-011`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-011`) and whole-board: see pass notes.

- `2026-08-29` `ready-to-ship → blocked` (devops — `continue` event pass,
  context `ENG-011`, this fire's own turn at the front of `traces/.pending`).
  Narrow scope per the event's own contract (resume this ticket from its
  current state; no board-wide sweep). Mode check clean (business-os `.env`
  → `MODE=` empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-011`) and
  whole-board: both exit 0, clean.

  **Read the current `skills/release-runner/SKILL.md` before acting, not the
  stale assumption carried in this ticket's own prior log entry.** The prior
  entry flagged the release window as a real question for this hop to
  decide; the skill (corrected earlier today, 2026-08-29, after the approver's
  own words: *"you anyway don't ship anything, just raise a PR... doesn't
  matter"*) answers it directly — **step 1's window check governs an actual
  production release (L2 merge-to-main-and-deploy, L3 deploy) and explicitly
  does not apply to L1**, which both `aiorders-admin-hub` and `aiorders-api`
  are registered as (`config/projects.md`). Opening a PR touches nothing in
  production. So the Saturday date this pass ran on is not a hold — matches
  the precedent `ENG-005` already set at this identical boundary (L1 PR
  opened and merge-requested same-day, no window applied).

  **Verified every upstream gate fresh from the receipt files rather than
  trusted from the board summary**: migration
  (`agents/database/migrations/ENG-011-client-stage-health-visibility.md`,
  **pass with a named gap** — no live Postgres on this host, corrected
  DROP+CREATE statement verified by reading plus a read-only Supabase MCP
  catalog check, not a container dry-run), code review
  (`agents/principal-engineer/reviews/ENG-011.md`, **pass**), quality
  (`agents/qa/test-plans/ENG-011.md`, **pass**, 12/12 tests), security
  (`agents/security/reviews/ENG-011.md`, **pass**). All four reference the
  same commits re-verified below — no drift.

  **Re-verified the live worktrees before touching anything**, since both
  `_eng` worktrees were sitting on `ENG-008`'s branch (that ticket's own
  `building` work), not this ticket's: confirmed both trees clean
  (`git status` — nothing to commit) before switching, so no in-progress
  `ENG-008` work was at risk. `git fetch` + `git checkout
  feat/ENG-011-client-stage-health-visibility` in both, then diffed against
  `origin/main`: `aiorders-admin-hub` at `6cf5e8c` (1 file, 63+/5-, matches
  the review's own diff reference exactly); `aiorders-api` at `4a5eb4d` (6
  files, 255+/12-, matches exactly). Both already pushed. Checked for an
  already-opened PR before creating one, same caution `ENG-005` used given
  this instance's own history of recovering unrecorded work: `gh pr list
  --head feat/ENG-011-client-stage-health-visibility --state all` on both
  repos — empty on both. None existed.

  **Opened both PRs** (`gh pr create`): `aiorders-api`
  https://github.com/harsimranwalia/aiorders-api/pull/3, `aiorders-admin-hub`
  https://github.com/harsimranwalia/aiorders-admin-hub/pull/3. `aiorders-api`
  opened first, per the code review's own recommended deploy order (either
  order degrades gracefully — both pill renderers fall back to `-` — but the
  intended order is now documented rather than left to chance). Each PR body
  states what changed, why, and its own project's gate verdicts. Restored
  both worktrees to `feat/ENG-008-influencer-admin-management` afterward
  (re-verified clean) so `ENG-008`'s own in-flight state is undisturbed.

  Wrote the L1 merge-request item
  (`inbox/2026-08-29-eng011-merge-request.md`, `gate: merge`, `agent:
  eng-manager`) carrying both PR links and all four gate verdicts by file
  reference, plus the two non-blocking gaps (no live-app verification either
  repo; unbatched per-brand KV read fan-out) named rather than hidden. Ran
  `departments/engineering/lib/eng-notify.sh raise` — reproduced the
  already-known `SLACK_WEBHOOK_URL unset` gap (`traces/eng-notify-2026-08-29.log`
  17:04:29), the same standing issue every gate item today has hit, not a new
  finding. Stamped `notified: 2026-08-29T17:04:29` by hand, since the script
  never writes back to the item either way. State → `blocked`, `blocked_on:
  approver`, `blocked_from: ready-to-ship`, owner `devops → approver`.

  **Cap check before this transition, read fresh from `inbox/`'s actual
  contents rather than trusted from the board header**: exactly two open
  gate items existed going in (`ENG-023`'s G1, this ticket's soon-to-be-raised
  merge request) — approver-facing WIP was 1/2, approval cap 1/3. `ENG-011`
  is an already-in-flight, already-fully-gated ticket reaching its own next
  gate, not a new start — same reasoning `ENG-005` used at this identical
  boundary. Advancing brings approver-facing WIP to 2/2 (at the limit, not
  over) and approval cap to 2/3 (not over) — proceeded on that basis.

  **1 transition this pass** (`ready-to-ship → blocked`), well under the cap
  of 4 — opening two PRs and writing the gate item is itself the real work of
  this hop. **Consequence:** `machine_wip` 6/1 → 5/1 (`blocked` sits outside
  the counted `ready`..`ready-to-ship` range — one closer to the cap, though
  still over until the remaining five drain to `shipped`). Approver-facing
  WIP 1/2 → 2/2; approval cap 1/3 → 2/3.

  **Dead-end sweep (scoped to this event):** this ticket's log now ends in a
  valid, accounted-for state with the chain record below. `ENG-008` (the
  ticket whose branch occupied both worktrees) untouched beyond the
  clean-before/clean-after check — out of scope for a `continue` event naming
  `ENG-011` specifically, and its own worktree state was fully restored.

  **Notify sweep:** this pass's own gate item raised and stamped above.
  Nothing else to nudge (`ENG-023`'s G1 not yet 24h old). Approval cap now
  2/3, not full — no stall.

  One observation filed (`observations.md`): the release-runner skill's own
  L1/window correction (made earlier today) directly resolved a question this
  ticket's own prior log entry had left open for this exact hop — worth
  naming so a future pass trusts the current skill file over an older
  ticket-log note when the two disagree on policy, not just on ticket state.

  `chained: none` — `blocked`, `blocked_on: approver`. This is the human gate
  the whole hop was driving toward; firing `continue ENG-011` again would
  just re-queue against a ticket with nothing left for a machine to do until
  the approver merges one or both PRs or replies to the gate item. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-011`) and
  whole-board: see pass notes.

- `2026-08-29` `blocked → shipped` (eng-manager, `watch` event pass, context
  `schtasks`). Per this event's own contract, swept all three watched inboxes
  fresh: `agents/product-manager/inbox/` and `agents/eng-manager/inbox/`
  held only already-`_handled/`-or-`.gitkeep` entries plus one new,
  unrelated P1 finding (`2026-08-29-restaurant-detail-write-partner-exposure.md`,
  handled separately per its own log/`proposals.md`); `inbox/` held exactly
  one live item — **this ticket's own merge request**, found carrying
  `decision: approved`, `decided: 2026-08-30T01:43:13.118048+00:00`, and a
  trailing "merged" line, a hand-edit rather than a reply through
  `lib/eng-notify.sh`'s channel, consistent with every gate answer on this
  instance but `ENG-002`'s. Multiple earlier passes today (`ENG-007`'s and
  `ENG-025`'s own logs) had already noticed this same fact in passing and
  explicitly left it "for whichever pass owns reconciling it," out of scope
  for their own narrower events — this `watch` sweep's job is exactly that
  scope. Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-011`) and
  whole-board: both exit 0, clean.

  **Not taken on the text alone — independently re-derived via git ancestry
  in this department's own worktrees, both repos:**

  ```
  $ cd _eng/aiorders-api && git fetch origin
  $ git merge-base --is-ancestor origin/feat/ENG-011-client-stage-health-visibility origin/main
  MERGED
  $ cd _eng/aiorders-admin-hub && git fetch origin
  $ git merge-base --is-ancestor origin/feat/ENG-011-client-stage-health-visibility origin/main
  MERGED
  ```

  Per `eng_build_loop.md` step 5, a multi-repo ticket ships only once every
  repo's branch has merged — confirmed for both, not just one.

  **Deploy verified live, not assumed from the merge alone**, using the
  Supabase MCP connection read-only against `bmnmnejwdxbcqinqkwko` plus
  GitHub's own run status:
  - `list_migrations` shows `20260829190000_add_last_order_at_to_platform_analytics`
    applied; `pg_get_functiondef('public.calculate_platform_analytics')`
    returns the live function already carrying `last_order_at` in both its
    `RETURNS TABLE` signature and its body — the merged shape, not the
    pre-migration one.
  - The `admin-portal` edge function (`version: 115`, `updated_at:
    2026-08-30T02:47:37Z`, deployed from the approver's own checkout) —
    the same redeploy `ENG-007`'s own reconciliation pass this session
    confirmed carries that ticket's handler live also carries this ticket's
    `last_order_at`-driven derivation code.
  - `aiorders-admin-hub`: a GitHub Actions Cloudflare Pages workflow didn't
    exist at this ticket's own merge commit (`e12342d`) — it was added two
    commits later (`698b7c1`, then `ceb9552`). The first run failed
    (missing environment scoping); the second (`ceb9552`) succeeded
    (`gh run list`: `completed/success`, `57s`) and, being a descendant of
    `e12342d`, deployed the full current `main` — this ticket's `Brands.tsx`
    change included. No CI/CD ran for this repo at merge time, but the
    frontend is confirmed live anyway, not just merged.

  **Wrote the release record**
  (`agents/devops/releases/2026-08-29-aiorders-admin-hub-ENG-011.md`),
  covering both repos as one release (this ticket's own precedent as the
  first two-repo ticket on this board). Moved
  `inbox/2026-08-29-eng011-merge-request.md` → `inbox/_handled/` with a
  processed footer. **Journaled**
  (`agents/eng-manager/config/decision-journal.md`) as an L1 merge, both
  repos.

  **State: `blocked → shipped`**, `blocked_on`/`blocked_from` cleared per
  `eng_build_loop.md` step 8 (cleared on the way out of `blocked`), `owner:
  approver → devops` per `definition-of-done.md`'s `shipped`-state
  ownership. `links.release` set above. **1 transition this pass**, well
  under the cap of 4. **Consequence:** `machine_wip` unaffected (`blocked`
  and `shipped` both sit outside the counted `ready`..`ready-to-ship`
  range — no change). Approver-facing WIP **2/2 → 1/2**; approval cap **2/3
  → 1/3** — this ticket's merge request was the only thing occupying one of
  each slot (`ENG-007`'s own slot had already been vacated by its earlier,
  separate control-center bypass, per its own reconciliation this same
  pass — see board index for the combined arithmetic).

  **Dead-end sweep:** this ticket's log now ends in a valid, accounted-for
  state with the chain record below. `ENG-007` was also touched this pass
  (its own separate reconciliation, same underlying cause — a control-center
  action outrunning the tracked gate item); no wider board sweep beyond
  these two — out of scope for a `watch` event's own narrower contract.

  **Notify sweep:** nothing raised this pass — a gate closing doesn't get
  re-notified. No stall — approval cap now 1/3, well under.

  **Observations filed** (`observations.md`): resolution of the
  long-flagged `ENG-011`/`ENG-007` board staleness (closing the loop several
  prior passes explicitly deferred); the `admin-portal` redeploy carrying
  two tickets' handler changes in one event; the `aiorders-admin-hub`
  Cloudflare Pages workflow's existence and its first-run failure/second-run
  fix, both landing after this ticket's own merge but still covering it.

  `chained: ENG-011` — `shipped` is product-manager-owned next
  (`skills/acceptance-check/SKILL.md` triggers on entering `shipped`), not
  the approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-011`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-011`) and whole-board: see pass notes.

- `2026-08-30` `shipped → verified` (product-manager, `skills/acceptance-check/SKILL.md`,
  `continue` event pass, context `ENG-011`). Narrow scope per this event's
  own contract (resume this ticket from its current state; no board-wide
  sweep). Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

  **Checked against the live result, not the proxies** — the skill's own
  standing instruction, and the first time this board has actually run this
  skill to completion. No browser access on this host (same gap the release
  record named for monitoring dashboards), so verification used three
  independent live paths instead of trusting the migration/review/QA/security
  receipts' own static checks: (1) reading the exact deployed source at
  `origin/main` in both `_eng` worktrees via `git show`, without touching
  either worktree's checked-out branch (`aiorders-api` was mid-`ENG-013`,
  `aiorders-admin-hub` mid-`ENG-008` — both left undisturbed); (2) sampling
  real production rows through the read-only Supabase MCP connection
  (`bmnmnejwdxbcqinqkwko`) to catch data-shape issues synthetic unit-test
  inputs can't; (3) one live unauthenticated `curl` against the actual
  production endpoint.

  **Criteria walked, against `agents/product-manager/specs/ENG-011-client-stage-health-visibility.md`:**
  1. **Stage shown, finite set — PASS.** `admin-portal/handlers/brands.ts`'s
     `deriveStage` (live at `origin/main`, both repos) and `Brands.tsx`'s
     `getStagePill` confirmed by direct read: 3 real branches (`live`/
     `onboarding`/`inactive`) plus a `default → '-'` branch for anything
     else, never a crash. Cross-checked against 15 real production `brands`
     rows (Supabase MCP): real `is_active`/`onboarding_step` values map
     cleanly, no nulls or unexpected types found.
  2. **Stage alone answers "is client" — PASS.** One `stage` field on the
     `Brand` interface; no second `isClient`-shaped field anywhere in either
     diff at `origin/main`.
  3. **Stage filter — PASS.** `<Select value={stageFilter}
     onValueChange={setStageFilter}>` confirmed present in the rendered JSX
     (`Brands.tsx` line ~859), wired into `filteredBrands` via `matchesStage
     = stageFilter === 'all' || brand.stage === stageFilter`, `&&`-composed
     with the three pre-existing filters — independently re-read at the
     merged commit, not trusted from QA's trace.
  4. **Clearing the filter — PASS.** `"All Stages"` option's `value="all"`
     short-circuits `matchesStage` to `true` unconditionally — same
     mechanism as criterion 3, confirmed in the same read.
  5. **Health indicator shown — PASS, with a live issue found and routed
     (not blocking this criterion).** `deriveHealth`/`getHealthPill`
     confirmed with 4 real branches (`active`/`at_risk`/`inactive`/
     `no_data`) plus a safe default. Traced the full live data path beyond
     what any prior gate checked: confirmed `calculate_platform_analytics()`
     actually emits 49 brand-level rollup rows in production (not just in
     its declared `RETURNS TABLE` shape), confirmed the KV key format
     `analytics:brand:{id}` matches exactly between the writer
     (`platform-analytics`'s `KVKeys.brand()`) and the reader
     (`admin-portal`'s `readBrandAnalytics`), and confirmed a real successful
     write occurred this morning (`2026-08-30T00:00:06Z`,
     "brands=49, restaurants=60") with current `last_order_at` values. While
     checking this, found the hourly cron feeding that cache has 401'd on
     every run since `01:00:00Z` today (7/7 as of this pass) — a live,
     ongoing production issue, unrelated to this ticket's own diff (onset
     predates this ticket's own `decided:` timestamp, and
     `platform-analytics`'s auth path was never touched by this ticket).
     Health data is real and correctly derived, just growing staler than the
     ~1h the design assumed. Filed as `BUG-001`
     (`agents/qa/bugs/BUG-001-platform-analytics-cron-401.md`, P2, owner
     devops) and routed as a proposal
     (`agents/eng-manager/proposals.md`, 2026-08-30 row) per
     `eng_build_loop.md` step 3 — not authorized to fix inline, and P2 per
     `bug-triage/SKILL.md` doesn't send this ticket back to `building` (the
     defect isn't in this ticket's own diff, so there's nothing here for
     `building` to fix).
  6. **Non-staff request rejected — PASS, independently verified live.**
     `admin-portal/index.ts`'s `authenticate()` (shared middleware, runs
     before every handler including `brands`) rejects a missing
     `authorization` header before any handler code runs. Not left at
     "pass by construction" the way QA's own gate did — sent a real
     unauthenticated `GET` to
     `https://backend.aiorders.io/functions/v1/admin-portal/brands` this
     pass: `401 UNAUTHORIZED_NO_AUTH_HEADER`. Closes the gap QA's test plan
     named explicitly as not independently re-verified.

  **Non-goals check** — clean. Grepped both diffs at `origin/main`: no
  ticket/support code, no weighted health score, no agency/reseller scoping
  change, no configurable stage taxonomy (`ONBOARDING_FINAL_STEP` is a fixed
  constant), `Leads.tsx`/`FranchiseeLeads.tsx` untouched.

  **Cost check** — matches. Release record: $0/month delta, one additive
  column, no new vendor. Matches the PRD's own Cost section exactly.

  **Step 6b (continue an approved sequence)** — checked, does not apply.
  This PRD carries no "feature shape and sequencing" section naming a next
  item — the raw request's "tickets" item was split out as its own standing
  question, already answered and already carried to `ENG-012`, already
  `dropped`, in an earlier pass. Nothing left to auto-continue.

  **Notebook entry written**:
  `agents/product-manager/notebook/2026-08-30-acceptance.md` — what the cost
  estimate got right (held at $0/month, evidence-grounded G1 defaults all
  survived unchanged), what it missed (reusing an already-live pipeline
  inherits that pipeline's own operational risk, on a timeline this ticket
  doesn't control — worth a Risks-section line on future PRDs with the same
  shape), and the no-browser-access substitution method for reuse next time.

  **State: `shipped → verified`**, `owner: devops → eng-manager` per the
  skill's own step 6 routing. **1 transition this pass**, well under the cap
  of 4. **Consequence:** `machine_wip` unaffected (`shipped` and `verified`
  both sit outside the counted `ready`..`ready-to-ship` range — no change).
  Approver-facing WIP and approval cap both unaffected — no gate raised or
  answered for this ticket this pass; `BUG-001`'s proposal row is a
  department-originated finding for the approver's next batched G1, not a
  gate on this ticket.

  **Dead-end sweep (scoped to this event):** this ticket's log now ends in a
  valid, accounted-for terminal state. No wider board sweep — out of scope
  for a `continue` event naming `ENG-011` specifically.

  **Notify sweep:** nothing raised for this ticket (reaching `verified`
  doesn't notify). `BUG-001`'s proposal rides the weekly batch like every
  other proposal, no immediate notify.

  **Observations filed** (`observations.md`): the no-browser-access
  substitution method (read deployed source at the merged commit, sample
  live data via Supabase MCP, one live unauthenticated probe) as a reusable
  pattern for the next ticket that hits the same host gap.

  `chained: none` — `verified` is terminal (acceptance-check's own step 6
  routing, and `definition-of-done.md`'s state table). Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-011`) and
  whole-board: see pass notes.
<!-- merge note: local (HEAD) and remote logs diverged after the ready-to-ship-to-blocked step. Local records the department own watch-pass reconciliation of the control-center merge (blocked to shipped, release record 2026-08-29-aiorders-admin-hub-ENG-011.md) followed by a full acceptance-check to verified. Remote (dated 2026-08-30) reaches the same terminal verified state via a single combined scheduled-pass entry doing equivalent git-ancestry and deploy verification. Kept local fuller, first-hand account below; remote independent verification covered the same ground by a different method without adding new information. -->
