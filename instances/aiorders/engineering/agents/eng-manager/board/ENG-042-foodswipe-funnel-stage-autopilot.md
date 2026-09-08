---
id: ENG-042
title: Foodswipe funnel — stage-triggered autopilot email/SMS
project: aiorders-api
type: feature
size: L
time_estimate: several days to a week
time_spent:
time_remaining:
severity: P2
priority:
state: awaiting-scope
owner: approver
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-06
updated: 2026-09-06
branch:
depends_on: [ENG-028]
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-042-foodswipe-funnel-stage-autopilot.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Input

Verbatim — the second half of the approver's `changed` answer on `ENG-028`'s
G1, extracted rather than quoted from a dedicated inbox card (this ask
arrived bundled with that ticket's rescope, not as its own request):
`inbox/_handled/2026-09-03-eng028-g1-scope.md`, `decision: changed`, decided
2026-09-06T09:09:08.947929+00:00:

> "Can we have autopilot email/sms setup on admin panel like brand portal
> for each stage update"

## Readback

See
`agents/product-manager/specs/ENG-042-foodswipe-funnel-stage-autopilot.md`
→ Readback for the full two-reading comparison (this PM's reading grounded
in live code, plus a blind subagent reading of the raw sentence alone) and
the code evidence behind each.

## Problem

Foodswipe listings move through a sales pipeline entirely by a staff
member's own memory and typing — nobody is told a stage changed, and no
follow-up message goes out unless a person writes and sends one by hand.
`restaurant-portal` already gives brand managers exactly this capability
for their own customer lifecycle; the admin panel's sales staff have no
equivalent for the pipeline they work every day.

## Outcome

A listing entering a stage that has a template and channel configured
sends that message to its own contact automatically — no staff member
drafts or sends it by hand. Sending is off by default, per stage and per
listing, until both a template exists and consent is on file.

## Notes

**Split from `ENG-028`'s own `changed` answer, not a fresh request.** The
approver's reply bundled two asks: hardcode a named nine-stage list
(processed as `ENG-028`'s own rescope, see that ticket's log) and this
automation ask, which `ENG-028`'s own PRD had already named as a non-goal
pointing at `ENG-017`. Checked before assuming that pointer still held:
`ENG-017` nurtures the **presignup `leads` table** (a website visitor who
hasn't signed up), a different pipeline with different stages from
Foodswipe `profiles` listings (`source = 'foodswipe'`) — so this ask
doesn't fold into `ENG-017`, and doesn't fold into `ENG-028` either (that
ticket's own scope is the stage *names*, not what happens when one
changes). Filed as its own ticket instead, same split this board already
used once for the same shape (`ENG-013`'s broadened ask splitting into
`ENG-013` plus `ENG-028`).

**"Brand portal['s] autopilot" is real, live code, not a figure of
speech.** `restaurant-portal`'s `Autopilot` section
(`src/pages/autopilot/{Automations,Broadcasts,Templates}.tsx`, a
trigger → message → review wizard) is backed by `aiorders-api`'s
`autopilot` Supabase function. Its `TriggerType` (`supabase/functions/
autopilot/utils/triggers.ts`) is a closed, hardcoded enum of restaurant/
order-lifecycle events (`order_completed`, `abandoned_cart`, `birthday`,
`new_catering_lead`, six more), each with its own hardcoded template
variables. None of it fits a Foodswipe listing, which has no restaurant at
the early stages and never has an order — same shape of finding `ENG-017`'s
own design already made for the presignup-leads pipeline. **Reusable: the
send layer (`sendEmail`/`sendSMS`). Not reusable as-is: the trigger/
template data model.**

**`depends_on: [ENG-028]`** — this ticket's trigger vocabulary is keyed on
stage names `ENG-028` hasn't finished confirming (its own fresh G1,
`inbox/2026-09-06-eng028-g1-rescope.md`, is still open as of this filing).
Blocks *building*, not shaping — this PRD and G1 can be reviewed on their
own timeline, same as `ENG-017` sat fully `designed` while genuinely
unrelated tickets ran ahead of it.

**Sized `L`, anchored to `ENG-017`, not estimated fresh.** Same shape of
work: a new admin-hub UI section modeled on an existing wizard, a parallel
trigger/template data model, consent/kill-switch plumbing reusing a
pattern already designed once. Full reasoning in the PRD's Cost section.

**Four specifics flagged on the G1 rather than assumed** — recipient
(external contact vs. internal staff alert), consent handling (proposed:
off by default, same as `ENG-017`), fire-once semantics (proposed: once
per listing per stage, ever), and contact-data gaps at early stages
(proposed: skip and log, never error). None changes whether to build; the
first two would change what gets built if the proposed default is wrong.

**Full lane, checked against the exclusion list.** `type: feature` at `L`
fails the fast-lane size bar outright, and independently trips schema (a
new trigger/template data model) and cross-project surface.

**Project field.** Primary `aiorders-api` (the trigger/send engine is the
real build surface, same reasoning `ENG-017` used); `aiorders-admin-hub` is
named for the configuration screen rather than inventing a multi-project
ticket shape.

**No dissent section** — `agents/critic/agent.md` still doesn't exist at
department or instance level, confirmed absent again this pass; not
refiled, the open proposal (`proposals.md`, 2026-08-25 row) covers it.

## Log

Append-only. One line per state transition, newest last.

- `2026-09-06` `intake → shaped → awaiting-scope` (product-manager,
  `decision` event pass, context `inbox/2026-09-03-eng028-g1-scope.md` —
  filed as a direct consequence of that decision, same carve-out
  `eng_build_loop.md` step 3 established for `ENG-027`/`ENG-028`: an
  approver-affirmed request, already given, is not the department
  inventing work about its own machinery. Mode check clean (`.env` has no
  `MODE` set). Pre-pass `lib/eng-gate-check.sh`, whole-board: exit 0,
  clean (no `ENG-042` yet to scope to).

  **Ran the full request-readback**, per step 2's default for full-lane
  work (no carve-out applied here: this is genuinely new raw input, unlike
  `ENG-028`'s own filing, which reused an already-answered question).
  This PM's own reading grounded in live code across `aiorders-api` and
  `restaurant-portal`; a blind subagent reading (raw sentence +
  `knowledge/business-profile.md` only, no repo access, no exposure to
  this reading). **No material divergence** on what's being asked; the
  blind reading independently surfaced the consent/CASL exposure
  `ENG-017`'s design had already found for the sibling pipeline, plus
  three further specifics (recipient, fire-once semantics, contact-data
  completeness) carried into the PRD's Risks rather than silently decided.

  **PRD written**:
  `agents/product-manager/specs/ENG-042-foodswipe-funnel-stage-autopilot.md`.

  **G1 required** — full lane, `L`, new data model, cross-project. Wrote
  `inbox/2026-09-06-eng042-g1-scope.md` (`agent: product-manager`, `gate:
  scope`, `project: aiorders-api`). Ran `lib/eng-notify.sh raise`; see the
  item's own frontmatter for the result and `notified:` timestamp.

  **State:** `intake → shaped → awaiting-scope`, all in this pass. `owner`
  `product-manager → approver`. **Consequence:** `machine_wip` unaffected
  (`awaiting-scope` sits outside the counted range). Approver-facing WIP:
  joins the uncapped list (`wip.approver_limit: unlimited` since
  2026-09-02) — visibility only, gates nothing.

  **Dead-end sweep:** out of scope for this `decision` event's own
  contract (act on the answered gate item; advance only `ENG-028` plus
  this direct consequence of that decision). No other ticket touched.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human. Post-pass
  `lib/eng-gate-check.sh`, scoped (`ENG-042`) and whole-board: see this
  pass's own entry on `ENG-028`'s board file and `_index.md`.
