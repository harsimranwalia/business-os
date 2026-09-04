# ENG-016 work-breakdown — first decomposition run on this board

`continue ENG-016` landed with the ticket at `ready`, owner `eng-manager`,
per `skills/work-breakdown/SKILL.md`. No prior ticket on this board has ever
carried a `parent:` value (checked: `grep -rl "^parent:" board/*.md` — only
the template-explanation line in `ENG-001`), so several mechanics below are
first-precedent judgement calls, not lookups. Recorded in full here per
`config/conventions.yaml` → `ticket_log.entry.reasoning_goes_to`, since the
ticket log itself is capped at 20 lines.

## Step 0 — autonomy check

All three touched projects (`config-site-builder`, `aiorders-api`,
`restaurant-portal`) are **L1** in `config/projects.md`. None is L0. Proceeds.

## Split by surface (SKILL.md step 2)

Read the design's own `## Components` table role-by-role rather than
repo-by-repo first, then grouped:

| Sub-ticket | Surface | Repo | Files (design's own Components rows) |
|---|---|---|---|
| ENG-031 | `database` | `aiorders-api` | one new migration |
| ENG-032 | `frontend` | `restaurant-portal` | 12 files: kanban/modal/status-copy ×8 + editor ×2 + types |
| ENG-033 | `backend` | `aiorders-api` | `catering-request/index.ts`, `brand-portal/website.ts` (type-only) |
| ENG-034 | `frontend` | `config-site-builder` | `types/restaurant.ts`, new `CateringMenuSelector.tsx`, `CateringForm.tsx` |

**Why two `frontend` sub-tickets instead of one spanning both repos**, even
though ENG-011 already established a ticket may span multiple repos: the
design's own Rollout section makes restaurant-portal ship strictly *before*
config-site-builder, with a full backend deploy in between (see Sequence
below). One frontend ticket touching both repos would need to pause mid-build
for a different agent's ticket (`backend`, ENG-033) to ship — expressible only
as a dependency between siblings, which two separate tickets do cleanly and
one ticket cannot. "One sub-ticket per owning agent per coherent unit of
work" — a coherent unit here is bounded by repo (separate branch, separate
PR, separate lint/build command per `config/projects.md`), not just by agent
identity.

**Why database and backend stay separate** even though both land in
`aiorders-api` and could plausibly be one PR: SKILL.md's own surface table
lists them as different rows/different owning agents, and `database` carries
its own blocking migration gate (`docs/engineering-team.md` roster) that
`backend` doesn't. Splitting by agent, not by repo, is correct here — the
opposite call from the frontend split above, because the two backend pieces
don't share the deploy-order constraint the frontend pieces do.

## Sequence (SKILL.md step 3)

Taken directly from the design's own `## Rollout` section, which states
plainly that deploy order here is "a correctness requirement, not a
preference" (`CateringKanban` renders only statuses in its hardcoded
`columns`; a status written before the portal ships it is invisible, not
just late):

```
ENG-031 (database, no dep)
  -> ENG-032 (frontend/restaurant-portal, depends_on: [ENG-031])
    -> ENG-033 (backend, depends_on: [ENG-031, ENG-032])
      -> ENG-034 (frontend/config-site-builder, depends_on: [ENG-033])
```

`depends_on`/`blocks` set accordingly on each new ticket. Per SKILL.md step
6, "a sub-ticket whose dependency isn't shipped doesn't start" — read
literally as *shipped*, not merely *built*, so this is a strictly serial
chain by design, matching the design's own stated correctness constraint
rather than loosened for parallelism.

## The machine-WIP question this pass had to resolve

`board/_index.md` read "Currently 1/1 — occupied by ENG-016" going into this
pass. Work-breakdown's own step 6 requires dispatching at least one
sub-ticket straight to `building`. Two readings were available:

1. **Each ticket sitting in `ready..ready-to-ship` counts separately.** Under
   this reading, dispatching ENG-031 to `building` while ENG-016 (parent)
   still occupies the counted range would push the count to 2/1 — over cap —
   and work-breakdown could never dispatch anything, on this ticket or any
   future M/L ticket, since the parent always already holds the only slot by
   the time work-breakdown runs. This reading makes the skill and the cap
   mutually impossible to satisfy together, which is a strong signal against
   it rather than a strict constraint to route around.
2. **The WIP slot is held by the ticket *family*** (a parent plus whatever
   `parent:`-linked children exist), not by each state-holding row
   individually. One feature, one slot, however many hands are working
   different surfaces of it concurrently — which is exactly what
   `eng-manager/agent.md`'s own stated reason for the 2026-08-29 correction
   describes ("a build-loop pass advanced *every in-flight ticket* by one
   shallow step each... the board carried six or more tickets simultaneously
   mid-pipeline" — six or more *independent* tickets, not one ticket's own
   internal decomposition).

Took reading 2. It's the only one under which `ready`'s documented exit
condition ("Work broken down, sequenced, assigned; WIP slot available") and
SKILL.md step 6 ("dispatch... in sequence order") can both be true at once.
Flagged as an observation (`observations.md`) rather than silently assumed,
since it's a real interpretive call on an enforced-adjacent number and the
first time this board has had to make it.

## What state the parent itself takes

No state in `VALID_STATES` (`eng-gate-check.sh`) is parent-specific. `ready`'s
exit condition is satisfied once breakdown is done, and the only forward
state in the full lane is `building` — so ENG-016 (parent) moves
`ready -> building`, owner stays `eng-manager` (tracking/coordinating; no
single engineer "builds" a four-surface parent with no diff of its own). It
sits there as an umbrella marker — not itself reviewed, tested, or
security-scanned, since it has no diff — until every child reaches
`shipped`/`verified`/`dropped` with at least one `shipped`/`verified`
(`definition-of-done.md` → "Parent tickets — whose receipts are whose";
ADR-003 per the same section and per `eng-gate-check.sh`'s own citations).
At that point it jumps directly to `shipped`, never through
`in-review`/`in-qa`/`in-security` itself. Not chained forward this pass
(nothing agent-actionable on the parent until children report back) — see
`chained:` reasoning on ENG-016's own log entry.

**Aside, not acted on:** `eng-gate-check.sh` cites this exemption as "ADR-003"
in its violation messages, but this instance's actual `ADR-003` is
`ADR-003-aiorders-api-authoritative-for-migrations.md` — a different, earlier
decision on this board, not the parent-receipts rule. The mechanism itself
reads ticket frontmatter directly and doesn't dereference the ADR file, so
this is a citation label mismatch, not a functional bug. Filed as an
observation rather than fixed — it's a department-template script comment,
out of an instance-scoped pass's reach, same class of gap prior hops on this
board have already logged and left for whoever is next in that file.

## Fields decided without an explicit rule

- **`priority`**: left empty on all four children rather than copied from the
  parent's `next`. The no-agent-writes-priority rule is stated with no
  inheritance carve-out, and it doesn't matter operationally here — sibling
  order is already fully determined by the explicit `depends_on` chain above,
  not by priority.
- **`source`**: `approver` on all four — the work traces to the approver's own
  G1 ("Lets start with piece 1"), just delegated through work-breakdown
  rather than entering fresh at intake. None of the template's other values
  (`filer`/`kanban`/`delivery`/`proposal`) fit a decomposition-born ticket.
- **`owner` while a child sits at `ready` waiting on a dependency**: set to
  `eng-manager`, matching the state table's documented owner for `ready`
  generally, rather than to the eventual building agent — the assignment is
  already decided (recorded in `## Breakdown` on the parent and in each
  child's own frontmatter), but nothing is actionable for that agent until
  the dependency ships, so ownership-while-waiting stays with the agent
  tracking the sequence.
- **`links.adrs` per child**: only where the ADR directly governs that
  surface (ENG-032: ADR-009 only; ENG-033: ADR-008 only; ENG-034: both;
  ENG-031: neither — the column shapes are independent of both decisions),
  rather than copying both onto all four.

## Sizing

Design's own text sizes the pieces implicitly (`## Risks` calls
config-site-builder's picker+gate "the largest single piece of new logic in
this ticket," and restaurant-portal's editor addition "~100 lines across
three files"). Estimates: ENG-031 ~1-2h (S), ENG-032 ~1 day (M), ENG-033
~half a day (M), ENG-034 ~1.5-2 days (M). Sum (~3-4 days of raw build time)
is consistent with the parent's own `L` / "several days to a week" band once
review/QA/security rounds are added on top. None of the four independently
reaches `L` — each is scoped to one project with no new subsystem, which is
the point of having split it.
