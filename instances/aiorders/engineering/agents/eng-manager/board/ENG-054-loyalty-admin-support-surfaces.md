---
id: ENG-054
title: Loyalty admin/support surfaces — cross-restaurant lookup and manual ledger adjustment/void
project: aiorders-api
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
created: 2026-09-09
updated: 2026-09-09
branch:
depends_on: [ENG-006, ENG-027]
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-054-loyalty-admin-support-surfaces.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

Every loyalty write path built so far (`ENG-027`/`ENG-048`/`ENG-049`/`ENG-051`/`ENG-052`/`ENG-053`)
is restaurant-scoped and diner-or-staff-initiated. There is no internal
surface for support to look up a diner's loyalty activity across
restaurants, or to correct or void a bad ledger entry once one exists.

## Outcome

An authenticated AIOrders staff member can look up a platform customer
(most likely by phone) and see their identity together with every
restaurant they're linked to and their combined earn/redeem history across
all of them, see any legacy-customer match `ENG-006`'s linking logic flagged
as ambiguous (`needs_review`) and record a decision on it, and void or
adjust a specific ledger entry that turns out to be wrong — which posts as
a new, attributed, reason-carrying entry rather than altering what already
happened. Nothing about how points are earned or redeemed by diners or
restaurants changes. Full detail:
`agents/product-manager/specs/ENG-054-loyalty-admin-support-surfaces.md`.

## Notes

Filed per `skills/acceptance-check/SKILL.md` step 6b: `ENG-051` (item 4 of
the approved loyalty sequence) reached `verified` this pass, and the G1
standing behind the sequence (`ENG-006`'s own G1, 2026-08-28 — "the proposed
five-ticket sequence stands as shape to file incrementally, not as four
pre-approved tickets") authorizes shaping the next item without waiting for
the approver to ask — the same mechanism that filed `ENG-051` itself once
`ENG-027` verified.

Item 5, **the last one**, of `ENG-006`'s proposed shape
(`agents/product-manager/specs/ENG-006-unified-customer-identity.md` `##
Feature shape and sequencing`): "Admin/support surfaces — internal lookup,
cross-restaurant view for support, and manual ledger adjustment/void.
Depends on ENG-006 and (3)." `ENG-051`'s own PRD Non-goals independently
named the same scope for "ticket 5": "Admin/support surfaces, internal
cross-restaurant lookup, and manual ledger adjustment or void of a bad
redemption."

Stub only (step 1b) — PRD content (problem depth, acceptance criteria,
non-goals, cost) deliberately left to a dedicated hop, not for a model-tier
reason (`prd-writer`'s own `Model: opus` field is stale — `pass_model()`
retired opus routing department-wide 2026-08-20) but because PRD-writing is
its own open-ended judgment task an already-long pass shouldn't rush, same
rationale `eng_build_loop.md` step 2 gives generally and the same reasoning
`ENG-051`'s own step-1b entry used. `depends_on` set to `[ENG-006, ENG-027]`
per the sequence's own stated dependency (the ledger and identity this
surface reads/adjusts); both already `verified`, so this ticket is
unblocked as soon as its PRD exists. Full reasoning:
`agents/eng-manager/notebook/2026-09-09-eng051-verified-closeout.md`.

## Log

- `2026-09-09T07:38 PDT` `(none) → intake` (product-manager, `continue ENG-051`
  event) — filed per `skills/acceptance-check/SKILL.md` step 6b once
  `ENG-051` (item 4) reached `verified` this same pass; item 5, the last
  one, of `ENG-006`'s approved five-item loyalty sequence. Stub only (step
  1b): project/type/lane set, one-line Problem written, `size`/PRD content
  left to a dedicated hop. `Next ID` counter advanced
  (`agents/eng-manager/board/_index.md`, `ENG-054 → ENG-055`).
  `chained: ENG-054` — recorded on `ENG-051`'s own log, the ticket this
  pass's event named; see there for this pass's overall chain decision and
  gate-check results.

- `2026-09-09T07:57 PDT` `intake → awaiting-scope`, `owner: product-manager →
  approver` (`continue ENG-054` event). Reading map for `continue`: steps 6
  and 6b, plus step 2 (ticket was mid-PRD — stub only, per the checkpoint),
  plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*,
  *The four lanes*, *Guards*). Mode check clean (`.env` → `MODE=active`).

  Resumed `prd-writer` at step 1c: no fresh two-reader readback run, same
  call `ENG-027`'s and `ENG-051`'s own step-1c entries made and logged, for
  the same reason — no raw ambiguous input exists to run two blind readings
  against; the reading that matters ran once at `ENG-006` and has since been
  independently corroborated by `ENG-007`'s, `ENG-027`'s, and `ENG-051`'s own
  PRDs, each naming this exact "ticket 5" boundary in their own non-goals at
  different times. PRD written in full:
  `agents/product-manager/specs/ENG-054-loyalty-admin-support-surfaces.md`.
  Sized `M` (no provisional guess to size down from — the step-1b stub left
  `size` empty) — reuses `ENG-006`'s identity/legacy-link tables and
  `ENG-027`'s/`ENG-051`'s ledger table and patterns directly, no new external
  integration, no cron, no new vendor.

  **One genuinely new finding surfaced while gathering evidence, not just
  corroboration:** an open proposal (`principal-engineer`, `proposals.md`,
  2026-09-07) already names `loyalty_ledger_entries`'s append-only rule as
  enforced by comment/convention only, not by the database, and names *this
  ticket* by number as the scenario it's worried about — flagged in the
  PRD's own Risks rather than left buried in the proposal log. Also found,
  via a direct grep for an existing internal-staff auth concept rather than
  assuming none exists: a live `admin-portal` router gate on `aiorders-api`
  (`admin`/`sub-admin`/`partner-admin`/`partner-user` allowlist), and
  `ENG-010`'s own design already worked through the same "the blanket gate
  over-grants external partner roles" problem this ticket will also hit —
  reused as a Risks pointer for the architect, not named as a solution (PRD
  stays out of naming the actual gate). No dissent section
  (`agents/critic/agent.md` still doesn't exist at either root, checked
  fresh; open proposal, `proposals.md` 2026-08-25 row, covers it). G1 raised:
  `inbox/2026-09-09-eng054-g1-scope.md`, `lib/eng-notify.sh raise` confirmed
  `sent` (`traces/eng-notify-2026-09-09.log`, `07:57:56`). Full reasoning:
  `agents/product-manager/notebook/2026-09-09-eng054-prd.md`.

  **1 transition.** `machine_wip` unaffected — `awaiting-scope` sits outside
  the counted range; this was shaping, not a machine start.

  **Freed machine slot, checked separately from this ticket's own shaping:**
  machine WIP has been `0/1` since the immediately preceding pass (`ENG-051`
  settling). Re-verified fresh, not trusted from memory, whether the
  `designed`-pool draw is authorized: all four files the open integrity
  incident (`inbox/2026-09-08-eng-loop-integrity-check.md`, P0, still no
  `decision:`) names are still `M`/uncommitted
  (`departments/engineering/schedules/eng_build_loop.md`,
  `departments/engineering/agents/eng-manager/config.yaml`,
  `config/config.yaml`, `agents/eng-manager/proposals.md` — `git status
  --porcelain` from the repo root, this pass), and `decision-journal.md`
  carries no row naming the designed-pool decision. Declined to draw from
  `designed`, consistent with roughly twenty independent prior
  reconfirmations (memory: `project-eng-never-idle-policy`); did not
  duplicate `inbox/IDLE-2026-09-07.md` or the incident item itself (both
  checked fresh, both still undecided). This is orthogonal to `ENG-054`'s
  own shaping and not a reason to chain anything into the slot this hop.

  Notify sweep (step 7): the new G1 item, raised and stamped above; no other
  item newly written this pass; no item crossed the 24h/no-`nudged:` nudge
  threshold. 8b: one observation filed
  (`agents/eng-manager/observations.md` — a cosmetic `lib/eng-notify.sh` log
  line labeling its own mode wrong, found while confirming the raise above;
  not a bug worth a proposal, the notification itself sent correctly). 8c:
  not yet — no gate answered this pass to journal.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-054` and
  whole-board: both exit `0`, clean.

  `chained: none` — this ticket now sits at `awaiting-scope`, owned by the
  approver. The freed machine slot (above) is a separate question, not
  filled this hop pending the open integrity incident.
