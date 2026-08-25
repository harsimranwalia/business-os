# Board

**Next ID: ENG-006** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.)

**Machine WIP 6** (`config/config.yaml` → `wip.machine_limit`) — counts states
`ready` through `ready-to-ship`. **Currently 1/6.**
**Approver-facing WIP 2 — currently 2/2 (full). Approval cap 3 — currently 2/3.**

`priority:` is a field on every ticket, and **only the approver sets it.** It is
not `severity`, which is the agent's read of how bad a problem is.

## In flight

| ID | Title | Project | State | Priority | Owner | Size | Updated |
|---|---|---|---|---|---|---|---|
| ENG-001 | Register this business's repos and prove the loop | aiorders | shaped | now | product-manager | S | 2026-08-25 |
| ENG-002 | Add a smoke-test harness to restaurant-portal | restaurant-portal | ready | (empty) | eng-manager | M | 2026-08-25 |
| ENG-003 | Untrack `.env` from config-site-builder and close related env-hygiene gaps | config-site-builder | awaiting-scope | (empty) | approver | M | 2026-08-25 |
| ENG-004 | Reconcile aiorders-admin-hub's deleted-but-uncommitted migration history | aiorders-admin-hub | awaiting-scope | (empty) | approver | L | 2026-08-25 |
| ENG-005 | Decide and act on the orphaned A4PosterGenerator component | aiorders-admin-hub | shaped | (empty) | product-manager | S | 2026-08-25 |

## Waiting on the approver

Cap: 3 across all gates. At the cap, the EM stops advancing tickets into gate
states — more approvals waiting is a backlog with the approver's name on it,
not throughput.

- **ENG-003 — G1 scope** — `inbox/2026-08-25-eng003-g1-scope.md`, raised
  2026-08-25, notified. Untrack `.env` from `config-site-builder` and close
  related env-hygiene gaps; the Maps-key check and rotation decision come
  back to the approver as explicit action items.
- **ENG-004 — G1 scope** — `inbox/2026-08-25-eng004-g1-scope.md`, raised
  2026-08-25, notified. Reconcile `aiorders-admin-hub`'s deleted-but-uncommitted
  migration history — investigate against the live Supabase project first,
  remediate second.

## 2026-08-25 — scheduled (manual-unblock), retry: ENG-002 gate processed, ENG-004 G1 raised

**This pass is the retry (attempt 2/2) of the `scheduled (manual-unblock)`
event below** — the first attempt timed out at the 1800s pass ceiling while
finishing the board-index edit for the entry directly below this one (see
`traces/eng-loop-2026-08-25.log`: `pass TIMED OUT after 1800s`, re-queued as
attempt 2/2). Before doing anything new, verified the first attempt's
substantive work — `ENG-003`/`ENG-004`/`ENG-005` shaped, `ENG-003`'s G1
raised, two proposals and three observations filed — was complete and
internally consistent on disk; the only gap found was this table missing rows
for the three new tickets, now fixed. Filed one further observation on the
timeout itself (`agents/eng-manager/observations.md`).

**Gate returns:** `ENG-002`'s G1 was answered — **approved**, no additional
comment — while this retry was starting (`decided: 2026-08-25T21:43:57Z`).
Processed it: gate item moved to `inbox/_handled/`, PRD `status: approved`,
entry added to `agents/eng-manager/config/decision-journal.md`. A dedicated
`decision 2026-08-25-eng002-g1-scope.md` event is separately queued
(`traces/.pending`) from the control center's own fire — when it eventually
drains it will find the gate already resolved and be a harmless no-op.
`ENG-003`'s G1 remains unanswered; left as-is.

**Dispatch:** `ENG-001` left alone, same reasoning as the pass below — its
`continue` is still independently queued (`traces/.pending`), so re-opening
the architect's deferred judgement call here would race a pass already
in flight for it. `ENG-002` advanced `awaiting-scope → designed → ready`:
architect design written
(`agents/architect/designs/ENG-002-restaurant-portal-smoke-test-harness.md`
— Vitest + React Testing Library, one smoke test on the real app entry
point; no one-way door, no ADR, no G2); EM sequencing found a single unit of
work and `machine_wip` (6) at 0/6 going in. **Stopped before `building`,
deliberately** — this pass is a recovery/sweep context, not the clean session
`schedules/eng_build_loop.md` reserves for "an engineer writing code," so the
actual implementation is left for a dedicated `continue` hop. `chained:
ENG-002`.

Resolving `ENG-002`'s gate freed the `wip.approver_limit` (2) slot it had
been holding alongside `ENG-003`. Took the freed slot for `ENG-004` over
`ENG-005` — both still `shaped` with no `priority` set, so severity is the
tie-break (`P2` vs `P3`), per `config/definition-of-done.md`. `ENG-004`'s G1
raised and notified; PRD `status: awaiting-scope`. `ENG-005` holds at
`shaped` — approver WIP is 2/2 (full) again with `ENG-003` + `ENG-004`.

**Merge detection:** no ticket is `blocked` on an L1 PR. No-op.

**Dead-end sweep:** every in-flight ticket's log ends in a valid, accounted-for
state (`chained: <id>` or `chained: none — <reason>`); no broken chain found.

## 2026-08-25 — scheduled (manual-unblock), attempt 1: swept the three unshaped requests

`scheduled (manual-unblock)` pass — the safety-net sweep queued behind the
`continue ENG-001` pass earlier today. Per the event's own scope ("sweep the
whole board: everything a local event cannot see"), left `ENG-001` alone —
its `continue` was already queued (`traces/.pending`) from that earlier
pass's own chain, so redoing its architect-judgement question here would
have raced a pass already in flight for it. Confirmed nothing is `blocked`
on an L1 PR (merge detection: no-op this pass) and no ticket's chain
silently broke (`ENG-001`'s and `ENG-002`'s logs both end in a valid,
accounted-for state).

Business intake: found and shaped all three approver-filed requests that had
sat unprocessed in `inbox/requests/` since 2026-08-23 (flagged as an
observation by the prior pass). Ran the full request-readback on each — this
PM's reading plus a blind architect reading via an independent subagent per
request, so the second reading genuinely couldn't see the first. No material
divergence on any of the three; all three architect readings sharpened the
technical picture without disagreeing on scope or problem — see each
ticket's PRD.

- **ENG-003** (`aiorders-env-hygiene`, `config-site-builder`, size M, P2) —
  shaped straight through to `awaiting-scope`. `wip.approver_limit` (2) had
  exactly one free slot (`ENG-002` held the other); this one took it, on
  severity grounds — an ongoing, possibly-live cost exposure (an
  unrestricted Google Maps key) outranks the other two's own "nothing here
  is urgent" framing. G1 raised and notified.
- **ENG-004** (`admin-hub-migration-history`, `aiorders-admin-hub`, size L,
  P2) — shaped to `shaped`, PRD complete, G1 held for the next free slot.
- **ENG-005** (`a4-poster-generator-decision`, `aiorders-admin-hub`, size S,
  P3) — shaped to `shaped`, PRD complete, G1 held for the next free slot. G1
  will be required despite `S`+`chore` auto-skip eligibility — the ticket's
  scope is an unresolved approver decision, not routine work; see its own
  log.

All three source requests moved to `inbox/_handled/`. Two items filed rather
than fixed: a proposal (`agents/eng-manager/proposals.md`) that
`lib/eng-notify.sh` has two real bugs — no channel dispatch (posts to Slack
regardless of this instance's `approver.notify: telegram`), and a `MODE`
variable collision with the sourced business-os `.env` that silently breaks
the `stall` alert and the `nudge` prefix (confirmed live: this pass's own
`raise` call logged `sent: active`, not `sent: raise`); and two observations
(`agents/eng-manager/observations.md`) — a ticket-schema gap (`project:`/
`branch:` are singular, `ENG-003` genuinely spans three repos) and a
registry gap (`config/projects.md` doesn't record which Supabase project
`aiorders-admin-hub` is linked to, which `ENG-004` needs to answer).

Approver-facing WIP now 2/2 (full), approval cap 2/3. `chained: none` on all
three new tickets — `ENG-003` waits on the approver, `ENG-004`/`ENG-005`
wait on a WIP slot freeing; see each ticket's log for the reasoning.

## 2026-08-25 — continue ENG-001: PM shaping + ENG-002 opened

`continue ENG-001` pass. Shaped `ENG-001` (`intake → shaped`): wrote its PRD,
re-confirmed AC1 (five repos registered at L1, approved 2026-07-28,
re-verified 2026-08-23), AC2 (all five worktrees present under `_eng/`), and
AC3 (`lib/eng-gate-check.sh` exit 0) as already satisfied.  `type: chore`
auto-skips G1, so no gate item for `ENG-001` itself.

AC4 (one real ticket to `shaped`) was still open. Found a genuine, already-filed
approver request sitting unprocessed in `inbox/requests/` since 2026-08-23
(`2026-08-23-test-harness.md`) — not a self-originated finding, so shaping it
didn't touch the department's-own-work rule (`schedules/eng_build_loop.md`
step 3). Ran the full request-readback on it (this PM's reading + a blind
architect reading, no material divergence) and shaped it into `ENG-002`
(`intake → shaped → awaiting-scope`) — a smoke-test harness for
`restaurant-portal`, since none of the five AIOrders repos has a single test
and the QA gate is currently unable to prove anything ran. `size: M`, so
(unlike `ENG-001`) **G1 is required** — item raised and notified, see
"Waiting on the approver" above. `ENG-001`'s AC4 is satisfied by `ENG-002`
having reached `shaped` en route to `awaiting-scope`.

Did not push `ENG-001` past `shaped` this pass — what "building" means for a
ticket with no application-code deliverable (config/registry verification,
another ticket) isn't addressed anywhere in the department's docs, and a
snap judgement call on that shouldn't be buried in a PM pass. Left for the
architect on the next `continue`. `chained: ENG-001`.

Two things filed rather than fixed in this pass: a proposal
(`agents/eng-manager/proposals.md`) noting `agents/critic/agent.md` doesn't
exist on this instance or the department template, though
`skills/prd-writer/SKILL.md` step 8b calls for it before every G1 (ENG-002's
G1 went out with no `## Dissent` as a result); and an observation
(`agents/eng-manager/observations.md`) that three other approver requests in
`inbox/requests/` (`a4-poster-generator-unwired`, `admin-hub-migration-history`,
`aiorders-env-hygiene`) are still unshaped, out of scope for this
ticket-scoped pass. The `scheduled manual-unblock` event already queued
behind this one should sweep them.
