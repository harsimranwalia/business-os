# ENG-027 work-breakdown — fifth decomposition run on this board

`continue ENG-027` landed with the ticket at `ready`, owner `eng-manager`, per
`skills/work-breakdown/SKILL.md`. Fifth time this skill has run (`ENG-016`,
`2026-09-03-eng016-work-breakdown.md`; `ENG-019`,
`2026-09-04-eng019-work-breakdown.md`; `ENG-021`,
`2026-09-05-eng021-work-breakdown.md`; `ENG-026`,
`2026-09-07-eng026-work-breakdown.md`) — reusing those passes' settled
precedents rather than re-litigating them, and recording only what's specific
to this ticket. Single-repo, two-surface split with a strict two-node chain —
closer in shape to `ENG-021`'s own family than to `ENG-026`'s four-node DAG.

## Step 0 — autonomy check

The one touched project, `aiorders-api`, is **L1** in `config/projects.md`.
Not L0. Proceeds.

## Step 1 — mode and WIP check

Mode `active`. Machine WIP re-checked fresh from every ticket's own
frontmatter, not the cached board header: `ENG-026` (`building`, a settled
container — every child is `shipped` or `blocked_on: approver`, none in
`ready..ready-to-ship`, so it holds zero machine slots per Guards'
2026-09-07(b) amendment) and `ENG-027` itself (`ready`) are the only two rows
outside terminal/pre-ready states. `1/1`, held by `ENG-027` alone. Per the
`ENG-016`/`ENG-019`/`ENG-021`/`ENG-026` precedent, a ticket's own family isn't
a second occupant of its own slot — proceeds.

## Split by surface (SKILL.md step 2)

Read the design's own `## Components` table role-by-role:

| Sub-ticket | Surface | Repo | Components (design's own table rows) |
|---|---|---|---|
| ENG-048 | `database` | `aiorders-api` | New table `loyalty_ledger_entries`; `orders` +2 columns (`cw_order_id`, `loyalty_processed_at`); new function `credit_order_if_eligible`; new `pg_cron` schedule `loyalty-auto-complete-tick` |
| ENG-049 | `backend` | `aiorders-api` | `cloudwaitress.ts` `createOrder()` (persist `cw_order_id`) and `handleCloudWaitress()` (un-ignore 3 events) modifications; new edge function `loyalty-auto-complete`; new `brand-portal/loyalty.ts` (`record_dine_in_earn`, `get_loyalty_balance`); `brand-portal/index.ts` +2 case lines |

Two owning-agent pairs, not three — **no `frontend` sub-ticket**, unlike
`ENG-026`'s family. The design's own `## Rollout` section states this
directly: "No frontend anywhere calls any of this yet" (the whole
five-ticket sequence's own non-goal, restated here rather than assumed). Both
surfaces live in the same repo (`aiorders-api`) and stay separate tickets —
same reasoning `ENG-016`'s `ENG-031`/`ENG-033` split and `ENG-026`'s own
`ENG-044`/`ENG-045` split already established for a single-repo,
multi-surface design.

**`restaurant_loyalty_configs`, `platform_customers`,
`platform_customer_legacy_links`, `customers`: no sub-ticket.** The design's
own Components table marks these "None — read-only from this ticket."
Verification-only, not a coherent unit of work, same treatment `ENG-021`'s
and `ENG-026`'s own no-diff rows already received.

**`brand-portal`'s two new interfaces (`record_dine_in_earn`,
`get_loyalty_balance`) stay inside the one `backend` sub-ticket, not split
out on their own**, even though they serve a different caller (a staff
member, not the webhook/sweep). Both are `backend` surface in the same repo
as the webhook/sweep work — the axis is agent-surface first, repo second
(`ENG-026`'s own stated rule), and neither piece needs a second agent. Each
depends on nothing the other doesn't already share (only `ENG-048`'s ledger
table), so there is no ordering reason to split them either.

## Sequence (SKILL.md step 3)

Data before the code that reads it — the same single edge every schema/backend
split on this board has used:

```
ENG-048 (database, no dep) -> ENG-049 (backend, depends_on: [ENG-048])
```

`ENG-049` calls `credit_order_if_eligible` (webhook path and sweep) and reads
from / writes to `loyalty_ledger_entries` and `orders.cw_order_id` /
`orders.loyalty_processed_at` directly (`record_dine_in_earn`,
`get_loyalty_balance`) — none of it exists before `ENG-048` ships. No
narrower edge is possible: every one of `ENG-049`'s five components touches
something `ENG-048` creates.

## Machine-WIP reading

Same family-slot reading `ENG-016`/`ENG-019`/`ENG-021`/`ENG-026` already
established: the `1/1` slot is held by the family (`ENG-027` plus its
`parent:`-linked children), not by each state-holding row separately.
`ENG-048` dispatching to `building` is not a second occupant of the slot
`ENG-027` already holds. `ENG-049` stays `ready` (unmet `depends_on`) — also
not a second occupant, and moot here regardless since the dependency chain
never lets both be startable at once.

## What state the parent itself takes

Same shape as every prior work-breakdown on this board: `ready`'s exit
condition ("work broken down, sequenced, assigned; WIP slot available" —
`definition-of-done.md`) is satisfied by this breakdown itself. `ENG-027`
moves `ready -> building`, owner stays `eng-manager` — no engineer builds a
two-surface parent with no diff of its own. It sits as an umbrella marker
until both children reach `shipped`/`verified`/`dropped` with at least one
`shipped`/`verified` (`ADR-003`-class exemption), then jumps directly to
`shipped`. Not chained forward this pass — nothing agent-actionable on the
parent until a child reports back.

## Branch: the ticket's own Notes are stale, corrected here rather than propagated

`ENG-027`'s Notes (written 2026-09-03, before design or breakdown existed)
say the whole loyalty sequence shares one branch, `loyalty-system`, and that
whoever builds this ticket branches from and merges back into it — true when
written: `ENG-006` and `ENG-007` both used `branch: loyalty-system` and each
opened their own PR from it (`#2`, `#4`). Checked fresh before writing either
sub-ticket, in the shared worktree, without switching its own checkout
(`~/Documents/projects/_eng/aiorders-api`, currently on `ENG-045`'s branch):
`git fetch origin`, then `git merge-base --is-ancestor origin/loyalty-system
origin/main` — true, zero unique commits — and `git log
origin/loyalty-system..origin/main --oneline` — 59 commits, spanning
`ENG-038`, `ENG-020`, `ENG-040`, `ENG-044`, `ENG-045`, and others. Both
predecessor PRs already merged individually; the shared branch has fully
served its purpose rather than remaining a live integration target, and
resuming it now would mean rebasing 59 unrelated commits before either child
could cleanly PR. **Both `ENG-048` and `ENG-049` branch fresh off
`origin/main` instead**, matching every other work-breakdown sub-ticket on
this board (`ENG-031`–`034`, `ENG-044`–`047`). `ENG-027`'s own Notes marked
superseded in place (same strikethrough convention that ticket's Notes
already uses twice) rather than silently overridden. Observation filed
(`observations.md`, this date) rather than an exception-request — this is a
technical fact discovered by direct investigation (git ancestry), not a
scope or business judgement call, so it doesn't need the approver's sign-off
the way overriding a G1/G2 decision would.

## Fields decided without an explicit rule

Same calls the prior four work-breakdown passes made, applied the same way:

- **`priority`**: left empty on both children, not copied from the parent's
  `now`. The strict two-node chain means only one child is ever startable at
  a time regardless — a priority value would only matter if two startable
  tickets competed for the one slot, which can't happen here by construction.
- **`source`**: `approver` on both — traces to the approver's own G1 approval
  of the PRD, delegated through work-breakdown.
- **`owner` while a child sits at `ready` waiting on its dependency**:
  `eng-manager` (the state table's documented owner for `ready` generally),
  reassigned to the owning surface agent once its dependency ships and it
  dispatches.
- **`severity`**: `P3` on both, copied from the parent — same underlying
  problem, no new severity judgement needed per surface.
- **`links.adrs`**: `ADR-021` (the `pg_cron`/`net.http_post` sweep-mechanism
  choice) on `ENG-048` only. The decision is embodied entirely in the cron
  schedule's own definition (a migration artifact); `ENG-049`'s edge function
  is an ordinary authenticated HTTP handler regardless of what invokes it —
  same attribution logic `ENG-026`'s own work-breakdown used for `ADR-010`
  ("the handler is where that evaluation actually runs"). `ENG-049` carries
  `links.adrs: []`, with the mechanism choice named in its own Notes so the
  engineer has the context without owning the decision.
- **`touches_data`/`touches_models`**: omitted on both, matching
  `ENG-026`'s own precedent — these fields are written by the architect at
  `designed` and aren't part of the base ticket template; sub-tickets created
  directly by work-breakdown don't pass through that gate themselves and
  inherit the parent's design instead.

## Acceptance-criteria coverage per child

The PRD's own 18 acceptance criteria (rescoped set), mapped here so a later
gate doesn't have to re-derive it. Heavier cross-cutting than `ENG-026`'s
family: most online-path criteria need both the DB function's guard logic
*and* the webhook/sweep actually invoking it correctly, so more criteria are
split than owned outright by one side.

- **`ENG-048` owns in full:** AC4 (already-credited, window elapses, no
  double credit — the function's own `loyalty_processed_at IS NULL` guard),
  AC5 (idempotent under any report ordering — the function's single-row-lock
  guard plus the ledger's own unique-`order_id` constraint), AC8 (rate at
  placement, not at credit time — the rate lookup inside the function), AC9
  (a later rate change doesn't touch an already-written entry — inherent in
  never updating a row), AC12 (no platform identity, online path — the
  function's identity-resolution branch).
- **`ENG-049` owns in full:** AC6 (dine-in credit — `record_dine_in_earn`),
  AC10 (balance = sum at that restaurant — `get_loyalty_balance`'s query),
  AC13 (accrual/reconciliation failure never blocks order recording — the
  webhook's own containment), AC14 (report for an unknown order — the
  webhook's not-found branch), AC17 (staff without restaurant access
  rejected — `requireRestaurantAccess` in `record_dine_in_earn`), AC18
  (invalid dine-in amount rejected — input validation in the same handler).
- **Split — no single child proves these alone:**
  - AC1 (fulfilment credits): `ENG-049` must call the function on
    `order_completed_updated`; `ENG-048`'s function must credit correctly
    given that call.
  - AC2 (cancellation blocks credit, permanently): `ENG-049` must write
    `status = 'cancelled'` unconditionally on the two cancellation events;
    `ENG-048`'s guard (`status IS DISTINCT FROM 'cancelled'`) is what makes
    that write actually block a credit.
  - AC3 (auto-complete sweep credits like AC1): `ENG-049`'s sweep edge
    function must select and call correctly; `ENG-048`'s function credits.
  - AC7 (an entry records amount/rate/source/reference/reason): `ENG-048`
    owns the schema shape and the online-path population (inside its own
    function); `ENG-049` owns the dine-in-path population (source, staff-id,
    no order reference) inside `record_dine_in_earn`.
  - AC11 (not-enrolled restaurant → no credit, no entry, dine-in caller told
    why): `ENG-048` owns the online-path half (function returns
    `skipped_not_enrolled`); `ENG-049` owns the dine-in-path half (a live,
    distinct `not_enrolled` response, not a silent success).
  - AC15 (sweep failure on one order doesn't block the batch, retries
    without double-crediting): `ENG-049` owns the per-row catch-and-continue
    loop; `ENG-048`'s guard is what makes the retry safe rather than a
    double credit.
  - AC16 (cancellation after credit doesn't delete/rewrite the entry):
    `ENG-048` owns it by construction (the function and the table have no
    update/delete path, ever); `ENG-049` owns it by omission (the
    cancellation branch touches only `orders.status`, never the ledger).

No child owns AC1, AC2, AC3, AC7, AC11, AC15, or AC16 alone — a gate checking
any of these against only one ticket's diff will find it incomplete by
design. Check `ENG-048` and `ENG-049` together.

## Sizing

- `ENG-048`: `S` — one migration (one new table with its own index, two
  additive columns), one function with real branching logic reusing two
  already-established lookup patterns (`ENG-006`'s identity walk, `ENG-007`'s
  rate-as-of-timestamp read) rather than inventing new ones, and one cron
  schedule structurally identical to `ADR-018`'s own. `time_estimate`: half a
  day.
- `ENG-049`: `M` — modifies one existing handler (two call sites), adds one
  new cron-invoked edge function with its own auth/batch/error-handling
  shape, and adds two new `brand-portal` actions with their own
  access-check/validation shape. Three genuinely separate interfaces, no new
  architecture. `time_estimate`: a day to a couple of days.

**Sum (roughly a day and a half to two and a half days) sits within the
parent's own "several days to a week" `L` band**, unlike `ENG-026`'s family,
which ran slightly past its parent's estimate. Two sub-tickets carry less
per-ticket review/QA/security overhead than four, and neither piece
introduces new architecture on its own — the `L` sizing was earned by what
the *combination* requires (first write-after-insert path on `orders`, a
scheduled sweep with real idempotency semantics, moving the accrual trigger
point), not by sheer file count, so splitting it in two doesn't inflate the
total the way a four-way split spread more per-ticket ceremony over the same
work.
