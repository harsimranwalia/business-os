---
id: ENG-011
title: Client stage & health visibility on the Brands admin page — plus stage filtering
project: aiorders-admin-hub
type: feature
size: M
time_estimate: half a day to a couple of days
time_spent:
time_remaining:
severity: P3
priority:
state: awaiting-scope
owner: approver
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-08-29
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-011-client-stage-health-visibility.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
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
  whole-board: see pass notes.
