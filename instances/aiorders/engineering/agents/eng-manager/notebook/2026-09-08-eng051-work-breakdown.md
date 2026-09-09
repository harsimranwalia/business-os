# ENG-051 work-breakdown — sixth decomposition run on this board

`continue ENG-051` landed with the ticket at `ready`, owner `eng-manager`, per
`skills/work-breakdown/SKILL.md`. Sixth time this skill has run (`ENG-016`,
`2026-09-03-eng016-work-breakdown.md`; `ENG-019`,
`2026-09-04-eng019-work-breakdown.md`; `ENG-021`,
`2026-09-05-eng021-work-breakdown.md`; `ENG-026`,
`2026-09-07-eng026-work-breakdown.md`; `ENG-027`,
`2026-09-07-eng027-work-breakdown.md`) — reusing those passes' settled
precedents rather than re-litigating them. Single-repo, two-surface split with
a strict two-node chain, same shape as `ENG-027`'s own family (`ENG-048`/
`ENG-049`) — the closest precedent, both in surface split and in the fact that
this design also reuses `ENG-027`'s own ledger table rather than adding a new
one.

## Step 0 — autonomy check

The one touched project, `aiorders-api`, is **L1** in `config/projects.md`.
Not L0. Proceeds.

## Step 1 — mode and WIP check

Mode `active`. Machine WIP re-checked fresh from every ticket's own
frontmatter (`grep '^state:'` across every `board/ENG-*.md`, not the cached
table): exactly one ticket sits in `ready..ready-to-ship` — `ENG-051` itself,
`ready`, no `parent:`. `1/1`, held by `ENG-051` alone. Per the `ENG-016`/
`ENG-019`/`ENG-021`/`ENG-026`/`ENG-027` precedent, a ticket's own family isn't
a second occupant of its own slot — proceeds.

## Split by surface (SKILL.md step 2)

Read the design's own `## Components` table role-by-role:

| Sub-ticket | Surface | Repo | Components (design's own table rows) |
|---|---|---|---|
| ENG-052 | `database` | `aiorders-api` | `loyalty_ledger_entries` altered (widen `source` check to add `'redemption'`; widen the three per-source checks for `order_id`/`fulfillment_reason`/`created_by`; add a new points-sign-by-source check; add nullable `idempotency_key text`, unique when present); new function `redeem_points_if_eligible(...)` |
| ENG-053 | `backend` | `aiorders-api` | `brand-portal/loyalty.ts` (new `redeemPoints` handler, extends `handleLoyalty`'s switch, widens `LoyaltyLedgerEntry.source`'s union type); `brand-portal/index.ts` (+1 `case 'redeem_points':` line) |

Two owning-agent sub-tickets, not three — **no `frontend` sub-ticket**, same
as `ENG-027`'s own family. The PRD's own non-goals and the design's own Out
of scope section both state this directly: "any frontend, in any repo" is
deferred for the whole five-ticket sequence, restated on this ticket's own
board file. Both surfaces live in the same repo (`aiorders-api`) and stay
separate tickets — the axis is agent-surface first, repo second (`ENG-026`'s
own stated rule, reused by `ENG-027`'s own split).

**`platform_customers`, `platform_customer_legacy_links`,
`restaurant_loyalty_configs`, `restaurants`: no sub-ticket.** The design's own
Components table marks these "None — read-only from this ticket." The
design's own central finding is that AC1/AC2 ("QR issuance") are already
fully satisfied by `ENG-006`'s shipped `platform_customers.id` — there is no
issuance component to split out at all, unlike a literal reading of this
ticket's own title might suggest. Verification-only, not a coherent unit of
work, same treatment `ENG-021`'s, `ENG-026`'s and `ENG-027`'s own no-diff rows
already received.

## Sequence (SKILL.md step 3)

Data before the code that reads it — the same single edge every schema/backend
split on this board has used, and the exact shape `ENG-048 → ENG-049` already
set for this same ledger table:

```
ENG-052 (database, no dep) -> ENG-053 (backend, depends_on: [ENG-052])
```

`ENG-053`'s `redeemPoints` handler calls `redeem_points_if_eligible` via
`supabase.rpc(...)` — that function, and the widened `loyalty_ledger_entries`
constraints/column it depends on, don't exist before `ENG-052` ships. No
narrower edge is possible: both of `ENG-053`'s components touch something
`ENG-052` creates.

## Step 4 — confirm each sub-ticket is answerable

**ENG-052 (database):** the design's `## Data` section gives the exact
constraint changes (three widened per-source checks, the new
points-sign-by-source check, the new nullable-unique `idempotency_key`
column) and `## Interfaces` gives the full 7-step function body — signature,
grants (explicit `revoke ... from public, anon, authenticated` +
`grant ... to service_role`, per `ENG-048`'s own hard-won B1 finding, already
named as precedent in this design's own Interfaces section), advisory-lock
seed (`1`, deliberately not `ENG-007`'s `0`), and the exact idempotency-before-
balance ordering with the reason spelled out. Answerable without a further
decision.

**ENG-053 (backend):** the design's `## Interfaces` section gives the exact
new action name, payload shape, validation depth, the `requireRestaurantAccess`
call-order requirement (AC10), the RPC call's exact argument names, and the
response shaping for all four status values including the existing
`readBalance` reuse for the last two. Answerable without a further decision.

Neither sub-ticket needs to return to `designed` — the design leaves no open
question a builder would have to invent an answer to.

## Machine-WIP reading

Same family-slot reading `ENG-016`/`ENG-019`/`ENG-021`/`ENG-026`/`ENG-027`
already established: the `1/1` slot is held by the family (`ENG-051` plus its
`parent:`-linked children), not by each state-holding row separately.
`ENG-052` dispatching to `building` is not a second occupant of the slot
`ENG-051` already holds. `ENG-053` stays `ready` (unmet `depends_on`) — also
not a second occupant, and moot regardless since the strict chain never lets
both be startable at once.

## What state the parent itself takes

Same shape as every prior work-breakdown on this board: `ready`'s exit
condition ("work broken down, sequenced, assigned; WIP slot available" —
`definition-of-done.md`) is satisfied by this breakdown itself. `ENG-051`
moves `ready → building`, owner stays `eng-manager` — no engineer builds a
two-surface parent with no diff of its own. It sits as an umbrella marker
until both children reach `shipped`/`verified`/`dropped` with at least one
`shipped`/`verified` (`ADR-003`-class exemption), then jumps directly to
`shipped`. Not chained forward this pass on its own account — nothing
agent-actionable on the parent until a child reports back; `chained: ENG-052`
is recorded on `ENG-052`'s own log instead, same split `ENG-027`'s own closing
line used for `ENG-048`.

## Branch point, checked fresh rather than assumed

Unlike `ENG-027`, this ticket's own Notes carry no stale shared-branch
instruction to correct — nothing on `ENG-051`'s board file names a branch.
Checked anyway, since both prerequisite tickets this design reuses
(`ENG-048`, `ENG-049`) merged only hours before this pass: from the
department worktree (`~/Documents/projects/_eng/aiorders-api`, currently
still checked out on `ENG-049`'s own branch — not switched, read via
`git fetch`/`git log` only, same git-show-not-checkout practice this ticket's
own design pass used), `git fetch origin main` then `git log origin/main
--oneline -3`: tip `fb26921`, with `ENG-048`'s merge commit (`2e5333a`) and
`ENG-049`'s merge commit (`a36c0de`) both direct ancestors — both
prerequisites are live on `main`, not just on their own now-stale branches.
`gh pr list --state open` on `aiorders-api`: empty — no open PR either
sub-ticket would need to stack on. **Both `ENG-052` and `ENG-053` branch
fresh off `origin/main`**, matching every non-stacked work-breakdown
sub-ticket on this board.

**One anomaly noticed, not chased further — filed as an observation, not a
blocker.** `origin/main`'s tip (`fb26921`, "Adopt 23 production edge
functions that had no source in this repo") is a commit authored directly by
the approver, outside this department's own pipeline (co-authored by a
separate Opus session, not this loop's own `sonnet`/`--effort max` hops) —
confirmed it touches neither `loyalty_ledger_entries` nor any `brand-portal`
file (`git show --stat fb26921 | grep -iE "loyalty|brand-portal"`: no hits),
so it doesn't affect either sub-ticket's own branch point. Separately,
`ENG-048`'s own merge commit message reads "Merge pull request **#23**", not
the `#21` recorded in `ENG-048`'s own `links.pr` frontmatter — a real
mismatch, not investigated further here since it doesn't bear on this ticket
and both commits are confirmed ancestors of `main` regardless of which PR
number actually carried them. Recorded in `observations.md`, this date, for
whoever next touches `ENG-048`'s own release record.

## Fields decided without an explicit rule

Same calls the prior five work-breakdown passes made, applied the same way:

- **`priority`**: left empty on both children, not copied from the parent
  (parent also carries no `priority`). The strict two-node chain means only
  one child is ever startable at a time regardless.
- **`source`**: `approver` on both — traces to the approver's own G1 approval
  of the PRD, delegated through work-breakdown.
- **`owner` while a child sits at `ready` waiting on its dependency**:
  `eng-manager` (the state table's documented owner for `ready` generally),
  reassigned to the owning surface agent once its dependency ships and it
  dispatches.
- **`severity`**: `P3` on both, copied from the parent — same underlying
  problem, no new severity judgement needed per surface.
- **`links.adrs`**: `ADR-022` (the code-format decision — `platform_customers.id`
  itself, not a new opaque/rotatable token) on neither child directly. The
  decision is embodied in the parent's own design and PRD, not in either
  sub-ticket's own diff — `ENG-052`'s migration doesn't create or format the
  code (it already exists, per `ENG-006`), and `ENG-053`'s handler only
  passes the caller-supplied `code` value through unchanged. Named in both
  sub-tickets' own Notes for context, matching the reasoning `ENG-027`'s own
  breakdown used to *withhold* `ADR-021` from `ENG-049`.
- **`touches_data`/`touches_models`**: omitted on both, matching `ENG-026`'s
  and `ENG-027`'s own precedent — these fields are written by the architect
  at `designed` and aren't part of the base ticket template; sub-tickets
  created directly by work-breakdown inherit the parent's design instead.

## Acceptance-criteria coverage per child

The PRD's own 11 acceptance criteria, mapped here so a later gate doesn't have
to re-derive it.

- **Neither child owns AC1 or AC2 (QR issuance) — already satisfied, not
  built by either.** Per the design's own central finding: `platform_customers.id`
  (`ENG-006`, already shipped) is the code; nothing in this ticket issues it.
  Recorded here so a later acceptance-check doesn't go looking for an
  issuance code path that doesn't exist.
- **`ENG-052` owns in full:** AC5 (over-balance rejected, no ledger entry —
  the function's own balance-sum check before insert), AC6 (no configured
  rate → `not_enrolled` — the function's own rate-resolution branch), AC9
  (retry doesn't double-debit — the idempotency-key-first check, the
  function's one genuinely new mechanism).
- **`ENG-053` owns in full:** AC10 (staff without restaurant access rejected
  — `requireRestaurantAccess` first in the new handler, same pattern AC17
  used on `ENG-049`).
- **Split — no single child proves these alone:**
  - AC3 (code + points amount resolves to exactly one diner): `ENG-053`'s
    handler passes `code` straight through as `p_platform_customer_id`;
    `ENG-052`'s function resolves it against `platform_customers` (a primary
    key, so resolution is always exactly one row or none) and returns
    `invalid_code` if missing.
  - AC4 (only that diner's balance at that specific restaurant is affected):
    `ENG-053`'s handler supplies `restaurant_id` from the authenticated
    staff member's own access-checked context, never from client input
    beyond the initial `requireRestaurantAccess` call; `ENG-052`'s function
    scopes every read and the insert itself to
    `(p_platform_customer_id, p_restaurant_id)` — the ticket's own central
    requirement, and neither side proves it without the other.
  - AC7 (converts to dollar value at the restaurant's current rate, writes
    one permanent ledger entry): `ENG-052`'s function resolves the rate and
    performs the insert; `ENG-053`'s handler is what makes a real request
    reach it with real, validated inputs.
  - AC8 (balance reflects the debit immediately on read): automatic from
    `ENG-027`'s own sum-on-read design, inherited unchanged by `ENG-052`'s
    new row shape; `ENG-053`'s handler is what surfaces it back to the
    caller (via the existing, unchanged `readBalance`).
  - AC11 (earns and redemptions visible in one ordered history): automatic
    from `ENG-027`'s existing read surface plus `ENG-052`'s widened `source`
    check — no code change needed in either sub-ticket beyond the schema
    widening itself; `ENG-053` doesn't add a new read endpoint for this (the
    design's own Out of scope section: no code-based variant of
    `get_loyalty_balance` is needed since `redeem_points`'s own response
    already carries the post-redemption balance).

No child owns AC3, AC4, AC7, AC8, or AC11 alone — a gate checking any of
these against only one ticket's diff will find it incomplete by design. Check
`ENG-052` and `ENG-053` together.

## Sizing

- `ENG-052`: `S` — one migration (three widened check constraints, one new
  nullable-unique column, both additive) and one new function with real
  branching logic reusing two already-established lookup/locking patterns
  (`ENG-007`'s effective-dated rate read, `ENG-027`'s own guarded-function
  shape) rather than inventing new ones. `time_estimate`: half a day.
- `ENG-053`: `S` — one new `brand-portal` action following the exact
  established `requireRestaurantAccess`-first / validate / RPC-call shape
  `record_dine_in_earn` already set, plus a one-line switch/router addition.
  No new architecture. `time_estimate`: half a day.

**Sum (about a day) sits comfortably inside the parent's own `M` band**,
smaller in total than `ENG-027`'s family (`S`+`M`) — this design's own
explanation is that half the ticket's nominal scope (QR issuance) turned out
to already be shipped, and the redemption half reuses three established
patterns wholesale rather than combining a new webhook integration, a new
cron-invoked sweep, and a new staff API the way `ENG-027`'s own backend child
did.
