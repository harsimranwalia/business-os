# ENG-021 work-breakdown — third decomposition run on this board

`continue ENG-021` landed with the ticket at `ready`, owner `eng-manager`, per
`skills/work-breakdown/SKILL.md`. Third time this skill has run (`ENG-016`,
`2026-09-03-eng016-work-breakdown.md`; `ENG-019`,
`2026-09-04-eng019-work-breakdown.md`) — reusing those passes' settled
precedents rather than re-litigating them, and recording only what's specific
to this ticket. First time the skill has run on an `M`-sized ticket rather than
`L` — `definition-of-done.md`'s own "Parent tickets" section names "an M or L
ticket that gets decomposed," so size alone isn't a reason to skip it, and
nothing in `work-breakdown/SKILL.md`'s trigger ("a ticket enters state `ready`")
carves out a size floor either.

## Step 0 — autonomy check

Both touched projects (`aiorders-api`, `restaurant-portal`) are **L1** in
`config/projects.md`. Neither is L0. Proceeds.

## Step 1 — mode and WIP check

Mode `active`. Machine WIP re-checked fresh from every ticket's own
frontmatter, not the cached board header: only `ENG-020` (`blocked`, outside
the counted `ready`..`ready-to-ship` range) and `ENG-021` itself (`ready`) are
outside terminal/pre-ready states. `1/1`, held by `ENG-021` itself. Per the
`ENG-016`/`ENG-019` precedent, a ticket's own family doesn't count as a second
occupant of its own slot — proceeds.

## Split by surface (SKILL.md step 2)

Read the design's own `## Components` table role-by-role:

| Sub-ticket | Surface | Repo | Files (design's own Components rows) |
|---|---|---|---|
| ENG-040 | `backend` | `aiorders-api` | `brand-portal/website.ts` (3 lines: `EDITABLE_PAGES`, `getWebsiteContent`'s returned content, `WebsiteFaq` export), `supabase/functions/README.md` |
| ENG-041 | `frontend` | `restaurant-portal` | `types/website.ts`, `WebsiteFaqForm.tsx` (new), `pages/website/Index.tsx`, `pages/questions/Index.tsx` (new), `App.tsx`, `Sidebar.tsx` |

Two owning agents, two repos, no repo-boundary split needed inside either —
same shape `ENG-019`'s `ENG-038`/`ENG-039` split had.

**No `database` sub-ticket**, unlike `ENG-016`'s and `ENG-019`'s families. The
design's own `## Data` section is explicit that this ticket has "no schema
change of any kind: no new table, no new column, no index, no migration, no
RPC" — `database`'s role here is a **read-only verification against the live
project**, not authorship of anything. SKILL.md step 2 splits by "coherent
unit of work"; a verification with no diff isn't one, the same way QA/security
gates don't get their own tickets even though every ticket passes through
them. Folded into `ENG-041`'s own Notes instead, as a required first step of
its build hop, since the query it gates (`ai_conversations`, direct client
read) is that ticket's own surface — see `ENG-041`'s Notes for the exact
checks carried over from the design's Data section, items 1-3.

**Considered and rejected: leaving `EDITABLE_PAGES` out of a sub-ticket
entirely and letting `ENG-041` add it.** The design's own Components table
marks it `backend`-owned explicitly, and `restaurant-portal` has no service-role
credential to touch `aiorders-api`'s edge function — a frontend engineer
literally cannot make this edit from the owning repo. Kept as a separate
`backend` sub-ticket despite its size (three lines plus one README line) —
smaller than `ENG-037`'s own schema-only precedent, but the same principle
applies: the split axis is agent-surface, not size.

## Sequence (SKILL.md step 3)

Taken from the design's own `## Rollout` section: "API first... Portal
second," with an explicit note that the questions page itself is unaffected by
build order (it never calls `ENG-040`'s action) while the FAQ tab's save path
does. Read literally per the `ENG-016`/`ENG-019` precedent — "a sub-ticket
whose dependency isn't shipped doesn't start" means *shipped*, not merely
built — `ENG-041` is held on `ENG-040` reaching `shipped`/`verified` even
though half its own scope (the questions page) has no functional dependency at
all. Not split further to let the questions-page half start early: the design
bundles both into one component list and one deploy ("route, nav entry, FAQ
tab and questions page ship together" — Rollout step 2), and splitting one
frontend surface into two frontend sub-tickets over a soft ordering preference
would be sequencing for a parallelism this department's single machine-WIP
slot can't actually spend (below).

```
ENG-040 (backend, no dep)
  -> ENG-041 (frontend, depends_on: [ENG-040])
```

`depends_on`/`blocks` set accordingly.

## Machine-WIP reading

Applied the `ENG-016`/`ENG-019` precedent directly: the WIP slot is held by
the ticket family (`ENG-021` plus its `parent:`-linked children), not by each
state-holding row separately. `ENG-040` dispatching to `building` is not a
second occupant of the `1/1` slot `ENG-021` already holds. Not re-flagged as a
fresh observation — the interpretive call was already logged for review on
`ENG-016`'s own pass and re-applied without re-derivation on `ENG-019`'s; this
is a third, unremarkable application of the same settled reading.

**No parallel-dispatch benefit to weigh, unlike a design with genuinely
independent pieces.** Even though the questions-page half of `ENG-041` has no
real dependency on `ENG-040`, dispatching both sub-tickets to `building`
simultaneously would not buy any wall-clock speed under this department's own
execution model — one chained `continue` fires one session at a time
regardless of how many tickets are technically startable, and the family
still counts as one `1/1` slot either way. Sequencing safely (avoiding the
described-but-tolerated "FAQ save fails" window if portal ships first) costs
nothing and is what the design's own Rollout section asked for.

## What state the parent itself takes

Same shape as `ENG-016`/`ENG-019`: `ready`'s exit condition ("work broken
down, sequenced, assigned; WIP slot available" — `definition-of-done.md`) is
satisfied once this breakdown is written, and the only forward state in the
full lane is `building`. `ENG-021` moves `ready -> building`, owner stays
`eng-manager` — no engineer builds a two-surface parent with no diff of its
own. It sits as an umbrella marker until both children reach
`shipped`/`verified`/`dropped` with at least one `shipped`/`verified`
(ADR-003-class exemption), then jumps directly to `shipped` without its own
review/QA/security hops. Not chained forward this pass — nothing
agent-actionable on the parent until a child reports back.

## Fields decided without an explicit rule

Same calls the prior two work-breakdown passes made, applied the same way:

- **`priority`**: left empty on both children, not copied from the parent's
  `now`. The two-item `depends_on` chain already fully determines order.
- **`source`**: `approver` on both — traces to the approver's own G1 approval
  of the PRD, delegated through work-breakdown.
- **`owner` while `ENG-041` sits at `ready` waiting on its dependency**:
  `eng-manager` (the state table's documented owner for `ready` generally),
  reassigned to `frontend` once `ENG-040` ships.
- **`severity`**: `P2` on both, copied from the parent — same underlying
  problem, no new severity judgement needed per surface.
- **`links.adrs` per child** — only where the ADR directly governs that
  surface. `ADR-013` (the read-path choice: direct client read over a new
  `brand-portal` action) and `ADR-014` (showing customer text verbatim, the
  PII position) both govern the questions page and nothing about the write
  widening — both to `ENG-041` only. `ENG-040` carries `links.adrs: []`: the
  allow-list widening was reversible-and-decided, not escalated, so no ADR
  exists for it specifically.
- **`touches_data`/`touches_models`**: omitted on both, matching
  `ENG-037`/`ENG-038`/`ENG-039`'s own precedent — these fields are written by
  the architect at `designed` and aren't part of the base ticket template;
  sub-tickets created directly by work-breakdown don't pass through that gate
  themselves and inherit the parent's design instead.

## Acceptance-criteria coverage per child

The design's own `## Acceptance criteria — walked` section (AC1-AC6) doesn't
map to components explicitly — mapped here so a later gate doesn't have to
re-derive it, same reason `ENG-019`'s own work-breakdown did this:

- `ENG-040`: AC4 and AC5 in full (same column, no second store, no cache
  between the write and the bot's/site's read — both satisfied by construction
  of the widened action, not by anything frontend does). Half of AC3 — the
  write *capability* the FAQ editor needs to exist before it can do anything.
- `ENG-041`: AC1, AC2, AC6 in full (the questions page: restaurant-scoped
  query + RLS, empty/error states, legible most-recent-first rendering). The
  other half of AC3 — the editor UI itself and the "Add to FAQs" hand-off,
  which is the stronger reading of the ticket's own Outcome ("directly from
  that view"). AC4/AC5 aren't independently provable from this ticket's own
  diff — it calls `ENG-040`'s action and inherits the guarantee, it doesn't
  establish it.

Neither child owns AC3 alone; a gate checking AC3 against only one ticket's
diff will find it incomplete by design; check both.

## Sizing

- `ENG-040`: smaller than `ENG-037`'s own schema-only precedent (three lines
  in one file plus one required README line, versus three tables, a cron
  schedule, and two indexes). `XS`, under an hour.
- `ENG-041`: the bulk of the parent's own `M` estimate — two new files, four
  modified files, a keyset-paginated query, a normaliser with five named edge
  cases, and the cross-page hand-off. `M`, ~1 to 1.5 days — effectively the
  parent's full original estimate, since `ENG-040` adds negligible time on top
  of it. Noted because the PRD's own Cost section predicted "Touches
  `restaurant-portal` only... No new backend endpoint or edge function
  anticipated" — the architect's design found a real (if tiny) backend piece
  the PRD didn't anticipate. Not a resize: the total is still comfortably
  inside the `M` band the PRD and G1 already covered, and the architect chose
  not to flag a resize at `designed`. Recorded here only so a future reader
  doesn't mistake `ENG-040`'s existence for scope creep.
