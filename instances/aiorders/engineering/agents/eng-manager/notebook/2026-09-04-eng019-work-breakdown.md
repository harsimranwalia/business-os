# ENG-019 work-breakdown — second decomposition run on this board

`continue ENG-019` landed with the ticket at `ready`, owner `eng-manager`, per
`skills/work-breakdown/SKILL.md`. Second time this skill has run (first:
`ENG-016`, `2026-09-03-eng016-work-breakdown.md`) — reusing that pass's
already-settled precedents rather than re-litigating them, and recording only
what's specific to this ticket.

## Step 0 — autonomy check

Both touched projects (`aiorders-api`, `restaurant-portal`) are **L1** in
`config/projects.md`. Neither is L0. Proceeds.

## Step 1 — mode and WIP check

Mode `active`. SKILL.md's own text ("check WIP against `config.yaml` →
`wip.limit` (default 2)") names a key that no longer exists —
`config/config.yaml` has `wip.machine_limit`/`wip.approver_limit`, not
`wip.limit`, since the 2026-08-29 correction. Read the current authoritative
value instead of the stale key name: `machine_limit: 1`, currently `1/1`,
held by `ENG-019` itself (this ticket's own `ready → building` transition
from the prior `scheduled` pass). Per the `ENG-016` precedent below, a
ticket's own family doesn't count as a second occupant of its own slot, so
this isn't "at the limit" in any sense that stops work-breakdown from
running on the ticket that already holds it. Proceeds. Filed as an
observation (stale config-key name in a skill file, not touched here per
this repo's Fable-only editing rule for skill files) rather than silently
worked around with no record.

## Split by surface (SKILL.md step 2)

Read the design's own `## Components` table role-by-role:

| Sub-ticket | Surface | Repo | Files (design's own Components rows) |
|---|---|---|---|
| ENG-037 | `database` | `aiorders-api` | one new migration (3 tables + cron schedule) |
| ENG-038 | `backend` | `aiorders-api` | `brand-portal/broadcasts.ts` (+test), `brand-portal/index.ts` (route), `broadcast-dispatch/index.ts` (+test), `broadcast-unsubscribe/index.ts`, `outgoing-communications/actors/consumers.ts` (new case), `supabase/functions/README.md` |
| ENG-039 | `frontend` | `restaurant-portal` | `Automations.tsx` (tab), `Broadcasts.tsx`, `BroadcastComposer.tsx`, `BroadcastReport.tsx`, `brandPortalApi.ts`, `types/broadcasts.ts`, `use-broadcasts.ts` |

Unlike `ENG-016`, this design touches only two repos and both `backend` and
`frontend` are single-repo, single-surface units — no repo-boundary split
needed inside either.

**Considered and rejected: splitting `backend` further** (owner-facing CRUD
in `broadcasts.ts` vs. the system-triggered `broadcast-dispatch`/
`broadcast-unsubscribe` pair). The two pieces are functionally independent —
dispatch never calls `broadcasts.ts` and vice versa — so the split is
mechanically possible. Rejected anyway: (a) SKILL.md's split axis is
agent-surface, not sub-surface within one agent — "split by surface, not by
layer of effort" reads as a caution against exactly this; (b) both pieces
have the same owning agent, and machine WIP is 1 for the whole family
regardless of ticket boundaries, so splitting would add a fourth ticket and
a fourth dependency edge without enabling any actual parallel work — the
same agent does the same total work in the same order either way; (c) the
parent's own `L` sizing (not `XL`) from the PM/architect already priced in
this exact scope. Kept as one `backend` sub-ticket.

## Sequence (SKILL.md step 3)

Taken directly from the design's own `## Rollout` section: "migration (new
tables, cron job created but the tables it polls start empty) →
broadcast-dispatch/broadcast-unsubscribe/brand-portal functions → frontend."
A strictly serial chain, and the default case SKILL.md step 3 already
describes ("data before the code that reads it, contract agreed before
either side builds against it") — no domain-specific reordering like
`ENG-016`'s kanban-before-backend constraint applies here.

```
ENG-037 (database, no dep)
  -> ENG-038 (backend, depends_on: [ENG-037])
    -> ENG-039 (frontend, depends_on: [ENG-038])
```

`depends_on`/`blocks` set accordingly. Per SKILL.md step 6 and the `ENG-016`
precedent, "a sub-ticket whose dependency isn't shipped doesn't start" is
read literally as *shipped* — so `ENG-038`/`ENG-039` stay at `ready` until
their dependency reaches `shipped`/`verified`, not merely `building`.

## Machine-WIP reading

Applied the `ENG-016` precedent directly rather than re-deriving it: the WIP
slot is held by the ticket family (`ENG-019` plus its `parent:`-linked
children), not by each state-holding row separately. `ENG-037` dispatching
to `building` is not a second occupant of the `1/1` slot `ENG-019` already
holds. Not re-flagged as a fresh observation — the interpretive call was
already logged for review on `ENG-016`'s own pass, and this run is a repeat
application of the same settled reading, not a new one.

## What state the parent itself takes

Same shape as `ENG-016`: no state in `VALID_STATES` is parent-specific,
`ready`'s exit condition ("work broken down, sequenced, assigned; WIP slot
available" — `definition-of-done.md`) is satisfied once this breakdown is
written, and the only forward state in the full lane is `building`. `ENG-019`
moves `ready -> building`, owner stays `eng-manager` — no single engineer
builds a three-surface parent with no diff of its own. It sits as an
umbrella marker until every child reaches `shipped`/`verified`/`dropped`
with at least one `shipped`/`verified` (ADR-003-class exemption,
`definition-of-done.md` → "Parent tickets"), then jumps directly to
`shipped` without its own review/QA/security hops. Not chained forward this
pass — nothing agent-actionable on the parent until children report back.

## Fields decided without an explicit rule

Same four calls `ENG-016`'s pass made, applied the same way here:

- **`priority`**: left empty on all three children, not copied from the
  parent's `now`. Sibling order is already fully determined by the explicit
  `depends_on` chain, not by priority, and the no-agent-writes-priority rule
  carries no inheritance carve-out.
- **`source`**: `approver` on all three — traces to the approver's own G1
  approval of the PRD, delegated through work-breakdown rather than entering
  fresh at intake.
- **`owner` while a child sits at `ready` waiting on its dependency**:
  `eng-manager` (the state table's documented owner for `ready` generally),
  not the eventual building agent — nothing is actionable for `backend`/
  `frontend` until their dependency ships.
- **`links.adrs` per child** — only where the ADR directly governs that
  surface:
  - `ENG-037` (database): `ADR-018` (the cron schedule and claim-supporting
    index are schema decisions), `ADR-019` (the reason this ticket owns
    verifying `orders.promos`'/`communication_log`'s live shape before
    `ENG-038` writes queries against them — the verification task lives here
    specifically because of this ADR).
  - `ENG-038` (backend): `ADR-018` (poller/claim logic), `ADR-019` (the ROI
    report query itself), `ADR-020` (consent-field reuse, the unsubscribe
    function, dispatch's re-check-at-send-time).
  - `ENG-039` (frontend): none — the UI consumes `ENG-038`'s contract as
    specified; no ADR here changes what the UI renders or how.

## Acceptance-criteria coverage per child

PRD carries 7 ACs, none of which the design maps to components explicitly —
mapped here so a later gate doesn't have to re-derive it:

- `ENG-037`: none directly verifiable from this diff alone (schema-only,
  matches `ENG-031`'s own precedent on `ENG-016`) — inert until `ENG-038`.
- `ENG-038`: AC1–AC7, all of them — every criterion is backend-enforced
  (compose/schedule logic, drip timing, audience scoping, ROI query,
  send logging, unsubscribe + re-check, server-side tenant rejection).
- `ENG-039`: AC1–AC5 (surfaces what `ENG-038` returns — composer, drip step
  editor, audience picker, report view, history view). AC6/AC7 have nothing
  for this ticket to add; not listed against it.

## Sizing

- `ENG-037`: comparable to `ENG-031`'s schema-only shape but larger (3 tables
  + cron schedule + 2 indexes + live-schema verification of two existing
  tables, vs. 2 nullable columns). `S`, ~half a day.
- `ENG-038`: the largest piece — an 8-action CRUD/report handler, a poller
  with idempotent-claim logic, a public unsubscribe function, two test
  files, a new `outgoing-communications` consumer case, a README update.
  `L`, ~2–3 days.
- `ENG-039`: comparable to `ENG-032`'s frontend shape (~1 day, `M`) but
  somewhat larger given the composer's audience picker + drip step editor.
  `M`, ~1–1.5 days.

Sum (~4–5 days of raw build time before review/QA/security rounds) is
consistent with the parent's own `L` / "several days to a week+" band. None
of the three independently exceeds `L`.
