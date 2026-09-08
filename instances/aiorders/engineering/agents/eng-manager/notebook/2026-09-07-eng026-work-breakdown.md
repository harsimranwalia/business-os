# ENG-026 work-breakdown — fourth decomposition run on this board

`continue ENG-026` landed with the ticket at `ready`, owner `eng-manager`, per
`skills/work-breakdown/SKILL.md`. Fourth time this skill has run (`ENG-016`,
`2026-09-03-eng016-work-breakdown.md`; `ENG-019`,
`2026-09-04-eng019-work-breakdown.md`; `ENG-021`,
`2026-09-05-eng021-work-breakdown.md`) — reusing those passes' settled
precedents rather than re-litigating them, and recording only what's specific
to this ticket. First ticket on this board whose split is a genuine DAG rather
than a single dependency chain: two of the four children depend on the same
parent, not on each other in sequence.

## Step 0 — autonomy check

All three touched projects — `aiorders-api`, `aiorders-admin-hub`,
`restaurant-marketplace` — are **L1** in `config/projects.md`. None is L0.
Proceeds.

## Step 1 — mode and WIP check

Mode `active`. Machine WIP re-checked fresh from every ticket's own
frontmatter, not the cached board header: only `ENG-026` itself (`ready`) sits
outside terminal/pre-ready states. `1/1`, held by `ENG-026` itself. Per the
`ENG-016`/`ENG-019`/`ENG-021` precedent, a ticket's own family doesn't count
as a second occupant of its own slot — proceeds.

## Split by surface (SKILL.md step 2)

Read the design's own `## Components` table role-by-role:

| Sub-ticket | Surface | Repo | Files (design's own Components rows) |
|---|---|---|---|
| ENG-044 | `database` | `aiorders-api` | Both migrations — `..._add_channel_visibility_to_restaurants.sql`, `..._gate_get_restaurants_optimized_by_channel.sql` |
| ENG-045 | `backend` | `aiorders-api` | `_shared/openingHours.ts` (new), `handlers/restaurants.ts` (`handleRestaurantDiscovery`/`Fallback`/`Detail`) |
| ENG-046 | `frontend` | `aiorders-admin-hub` | `RestaurantDetails.tsx`, `integrations/supabase/types.ts` (regenerated) |
| ENG-047 | `frontend` | `restaurant-marketplace` | `types/index.ts`, `services/api.ts`, `hooks/useRestaurants.tsx`, `FilterBar.tsx`, `RestaurantCard.tsx` |

Four owning-agent/repo pairs, not three — **`frontend` splits into two
sub-tickets here**, unlike `ENG-021`'s single-repo frontend surface. Precedent
for this is `ENG-016`'s own family (`ENG-032` on `restaurant-portal`, `ENG-034`
on `config-site-builder` — two `frontend` sub-tickets, two different repos,
same parent), not a new call. The axis is agent-surface first, repo second:
`database` and `backend` both live in `aiorders-api` but stay separate
tickets (same reasoning `ENG-016`'s `ENG-031`/`ENG-033` split already
established for that repo), while `frontend` splits across its two repos
because neither `aiorders-admin-hub` nor `restaurant-marketplace` engineer can
build the other's diff.

**`admin-portal/handlers/restaurants.ts`: no sub-ticket.** The design's own
Components table marks it explicitly "no change" — `updateRestaurant`'s
`.update(updates)` already passes arbitrary keys through, so the three new
flags ride an already-open surface with zero code required. Same treatment
`ENG-021`'s work-breakdown gave its own no-diff `database` role: a
verification or a no-op isn't a "coherent unit of work" (SKILL.md step 2),
it's a note. Here it isn't even a verification — folded into `ENG-045`'s own
Notes as a plain statement so nobody adds an unneeded whitelist as a drive-by.

**`aiorders-admin-hub/.../types.ts`: no sub-ticket of its own** — regenerated
via `supabase gen types typescript`, not hand-written, folded into `ENG-046`'s
own build step (same treatment `ENG-021`'s design gave its own generated-types
file).

## Sequence (SKILL.md step 3)

Taken from the design's own `## Rollout` section, which is explicit about
order (migration → handler+gate → admin toggle → consumer UI) but groups two
of those steps (admin toggle, consumer UI) as parallel-safe once their own
prerequisite ships. Read literally per the `ENG-016`/`ENG-019`/`ENG-021`
precedent — "a sub-ticket whose dependency isn't shipped doesn't start" means
*shipped*, not merely built:

```
ENG-044 (database, no dep)
  -> ENG-045 (backend, depends_on: [ENG-044])
       -> ENG-047 (frontend/marketplace, depends_on: [ENG-045])
  -> ENG-046 (frontend/admin-hub, depends_on: [ENG-044])
```

**Why `ENG-046` depends on `ENG-044` only, not `ENG-045`.** `ENG-046`'s write
path is `PUT /admin-portal/restaurants/:id` (`admin-portal/handlers/
restaurants.ts`), untouched by this design and unrelated to
`get_restaurants_optimized`/the discovery handlers `ENG-045` builds. It needs
the three columns to exist (`ENG-044`) and nothing about the discovery-side
gate. Sequencing it behind `ENG-045` anyway would be sequencing for a
parallelism this department's single machine-WIP slot can't spend (same
reasoning `ENG-021`'s own work-breakdown used for its unsequenced
questions-page half) — the design's own Rollout section groups admin-toggle
and consumer-UI as two independent last steps, not one after the other, and
this DAG reflects that directly rather than flattening it into an arbitrary
chain.

**Why `ENG-047` depends on `ENG-045`, not `ENG-044` directly.** It reads
`open_now` and `status`, both of which `ENG-045` introduces; `ENG-044` alone
(schema only, no handler change) leaves those fields absent from every API
response. Transitively gated on `ENG-044` through `ENG-045` — no separate
edge needed.

**The Rollout section's own deployment-coordination risk, restated rather
than turned into a dependency edge.** The design's Risks/Rollout both warn
that deploying `ENG-045`'s channel gate without `ENG-046`'s toggle UI shipped
close behind it leaves the Dine-In tab near-empty (every restaurant defaults
`has_dine_in: false` unless `ENG-044` found a real column to backfill from) —
staff need the toggle UI to opt restaurants back in. This is a *deployment
timing* concern, not a *build* dependency: `ENG-046` does not need `ENG-045`'s
code to exist to be built or to function. Given every ticket here ships as its
own independently-merged PR (L1 — the approver merges "at their own
convenience," not on a department-controlled schedule), a `depends_on` edge
can't actually enforce simultaneous deployment anyway — it would only delay
`ENG-046`'s *build* for no real safety gained, while doing nothing about the
gap between merge and the approver's own merge timing. Named explicitly, on
both `ENG-044`'s and this notebook's own record, rather than encoded as a
dependency it can't make true: whoever merges `ENG-045`'s PR should merge
`ENG-046`'s in the same window. Flagged again at `ENG-045`'s own
release-readiness hop is the natural place to re-surface it with concrete PR
links, not guessed at here.

## Machine-WIP reading

Applied the `ENG-016`/`ENG-019`/`ENG-021` precedent directly: the WIP slot is
held by the ticket family (`ENG-026` plus its `parent:`-linked children), not
by each state-holding row separately. `ENG-044` dispatching to `building` is
not a second occupant of the `1/1` slot `ENG-026` already holds.

**Only one child dispatched to `building` despite two (`ENG-045`, `ENG-046`)
sharing the same eventual unblock.** Neither is startable yet regardless —
both `depends_on: [ENG-044]`, unmet — so this pass dispatches exactly the one
child with a met dependency (`ENG-044`) and leaves the other three at `ready`.
Once `ENG-044` ships, a future `continue ENG-026` (or a `scheduled`/`watch`
sweep's own step-5 detection) will find *two* children simultaneously
startable (`ENG-045` and `ENG-046`) for the first time on this board — still
dispatches only one per pass, same reasoning `ENG-021`'s own notebook already
recorded ("one chained `continue` fires one session at a time regardless of
how many tickets are technically startable... the family still counts as one
`1/1` slot either way"). Which of the two goes first at that point is a call
for that future pass, not this one — likely lowest-id (`ENG-045`) absent a new
reason, but not decided here.

## What state the parent itself takes

Same shape as `ENG-016`/`ENG-019`/`ENG-021`: `ready`'s exit condition ("work
broken down, sequenced, assigned; WIP slot available" —
`definition-of-done.md`) is satisfied once this breakdown is written, and the
only forward state in the full lane is `building`. `ENG-026` moves
`ready -> building`, owner stays `eng-manager` — no engineer builds a
four-surface parent with no diff of its own. It sits as an umbrella marker
until all four children reach `shipped`/`verified`/`dropped` with at least one
`shipped`/`verified` (`ADR-003`-class exemption), then jumps directly to
`shipped` without its own review/QA/security hops. Not chained forward this
pass — nothing agent-actionable on the parent until a child reports back.

## Fields decided without an explicit rule

Same calls the prior three work-breakdown passes made, applied the same way:

- **`priority`**: left empty on all four children, not copied from the
  parent's `now`. The dependency graph already determines what can start when;
  a priority value would only matter if two *startable* tickets ever competed
  for the one slot, which this graph avoids by construction until `ENG-044`
  ships.
- **`source`**: `approver` on all four — traces to the approver's own G1
  approval of the PRD, delegated through work-breakdown.
- **`owner` while a child sits at `ready` waiting on its dependency**:
  `eng-manager` (the state table's documented owner for `ready` generally),
  reassigned to the owning surface agent once its dependency ships.
- **`severity`**: `P3` on all four, copied from the parent — same underlying
  problem, no new severity judgement needed per surface.
- **`links.adrs` per child** — only where the ADR directly governs that
  surface, per `ENG-021`'s own precedent. `ADR-010` (open-now evaluated
  post-query in TypeScript, not as a SQL predicate) governs `ENG-045`'s own
  diff — the handler is where that evaluation actually runs. `ENG-047`
  consumes the resulting `open_now`/`status` fields and inherits the
  pagination trade-off, but doesn't implement or decide anything `ADR-010`
  covers, so it carries `links.adrs: []` (the caveat is still named in its own
  Notes, so the engineer isn't surprised by it — naming a consequence in
  prose is not the same as claiming ownership of the decision behind it).
  `ENG-044` and `ENG-046` carry `links.adrs: []`: neither touches anything
  `ADR-010` governs.
- **`touches_data`/`touches_models`**: omitted on all four, matching
  `ENG-037`–`041`'s own precedent — these fields are written by the architect
  at `designed` and aren't part of the base ticket template; sub-tickets
  created directly by work-breakdown don't pass through that gate themselves
  and inherit the parent's design instead.

## Acceptance-criteria coverage per child

The PRD's own five acceptance criteria, mapped here so a later gate doesn't
have to re-derive it, same reason every prior work-breakdown on this board has
done this:

- `ENG-044`: AC1 in full (migration adds all three flags with stated
  defaults, `has_order_food` default doesn't regress current behavior) and
  AC5 in full (the rollout/backfill question resolved with an evidence-based
  answer on file, via the live-schema check, not silently defaulted).
- `ENG-045`: AC3 in full (Dine-In/Catering tabs show only flag-`true`
  merchants, negative case included, regardless of `open_now`) and AC4's
  filter/status-computation half (a closed-but-enabled merchant appears by
  default with a status string, excluded only when `open_now` is explicitly
  on — the *logic*, not the UI).
- `ENG-046`: AC2 in full (staff can view and set all three flags from
  `aiorders-admin-hub`).
- `ENG-047`: the other half of AC4 — the "Open Now" chip and the `status`
  render. Not independently provable from this ticket's own diff alone; it
  calls `ENG-045`'s handler and inherits the guarantee, it doesn't establish
  it.

No child owns AC4 alone — same shape `ENG-021`'s AC3 split already
established; a gate checking AC4 against only one ticket's diff will find it
incomplete by design. Check `ENG-045` and `ENG-047` together.

## Sizing

- `ENG-044`: `S` — two migrations plus a live-schema check that must actually
  run (not just write SQL) before the second migration can be finalized. A bit
  more than the department's `XS` schema-only precedent (`ENG-031`, `ENG-037`)
  because of that conditional check, not because the SQL itself is large.
- `ENG-045`: `S` — a straightforward Deno port of an already-written parser
  plus wiring three existing handlers; no new architecture, one clear surface.
- `ENG-046`: `XS` — two new Switch rows plus a repoint, matching six existing
  rows' markup exactly, same shape `ENG-040`'s own XS precedent set.
- `ENG-047`: `S` — five file touches (types, two hooks/services files, a
  filter chip, a card render), each individually mechanical, no new
  architecture.

**Sum runs slightly past the PRD's own "half a day to a day" band** — roughly
a day to a day and a half across all four pieces. Not a resize, same
disposition `ENG-021`'s own work-breakdown recorded for its unanticipated
`ENG-040`: the PRD's Cost section already named this as "likely the board's
first three-repo ticket" and priced the band loosely against that; four
sub-tickets (two of them touching the same repo from different surfaces)
carry more per-ticket overhead — a review/QA/security cycle each — than the
single continuous build the original estimate implicitly pictured. Recorded
here so a future reader doesn't mistake the total for scope creep.
