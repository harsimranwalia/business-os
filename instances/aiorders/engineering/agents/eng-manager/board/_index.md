# Board

**Next ID: ENG-025** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.)

**Machine WIP 6** (`config/config.yaml` → `wip.machine_limit`) — counts states
`ready` through `ready-to-ship`. **Currently 6/6 — at cap, not over.**
`ENG-007` and `ENG-011` sit at `ready-to-ship`; `ENG-008`, `ENG-009`,
`ENG-010`, and `ENG-013` sit at `ready`. Nothing further can enter `ready`
until one of these six clears. `ENG-014` and `ENG-015` do not count here
(`awaiting-scope`, short of the counted range).

**Approver-facing WIP 2 — 2/2 mechanically, at cap.** The 2026-08-29
`intake` pass that shaped `ENG-021` checked both G1s fresh from `inbox/`
(not this cached header) and found **`ENG-014`'s and `ENG-015`'s G1s both
now answered**
(`decision: approved`, decided 15:54:50 and 16:12:24) — but neither ticket's
frontmatter has been advanced past `state: awaiting-scope, owner: approver`
yet by a `decision` pass, so both mechanically still hold their
approver-facing WIP slot. Answered-but-unprocessed, not genuinely waiting —
same distinction this section tracked for the `ENG-009`/`ENG-010`/`ENG-012`/
`ENG-013` backlog earlier today. Nothing new should start down a path that
needs the approver until a `decision` pass actually clears one of these two.

**Approval cap 3 — 2/3, mechanically at cap, both slots now
answered-but-unprocessed rather than open.** `ENG-014`'s G1
(`inbox/2026-08-29-eng014-g1-scope.md`) and `ENG-015`'s G1
(`inbox/2026-08-29-eng015-g1-scope.md`) are both decided; a `decision` pass
for each appears to already be independently in flight. One slot free.

`priority:` is a field on every ticket, and **only the approver sets it.** It is
not `severity`, which is the agent's read of how bad a problem is.

## In flight

| ID | Title | Project | State | Priority | Owner | Size | Updated |
|---|---|---|---|---|---|---|---|
| ENG-007 | Per-restaurant loyalty configuration — earn rates and redemption value | aiorders-api | ready-to-ship | | devops | S | 2026-08-29 |
| ENG-008 | Influencer board admin management — region/campaign-type preference, rating, collaboration count | aiorders-admin-hub | ready | | eng-manager | M | 2026-08-29 |
| ENG-009 | Influencer engagement info — internal activity signal plus a staff-editable social stat | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-29 |
| ENG-010 | Influencer relationship notes — staff log for personality, preferences, and off-platform conversations | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-29 |
| ENG-011 | Client stage & health visibility on the Brands admin page — plus stage filtering | aiorders-admin-hub | ready-to-ship | | devops | M | 2026-08-29 |
| ENG-013 | Foodswipe funnel page — staff-settable pipeline stages | aiorders-admin-hub | ready | | eng-manager | M | 2026-08-29 |
| ENG-014 | Brand portal self-service — restaurant QR codes and marketing media downloads | restaurant-portal | awaiting-scope | | approver | M | 2026-08-29 |
| ENG-015 | Agency/reseller (partner) users — brand-scoped locations and a working add-location path | aiorders-admin-hub | awaiting-scope | | approver | M | 2026-08-29 |
| ENG-016 | Catering page — self-serve quote generator, with automatic stage update | config-site-builder | shaped | | product-manager | L | 2026-08-29 |
| ENG-017 | Autopilot nurture for the presignup sales lead pipeline — stage-triggered email/SMS | aiorders-api | shaped | | product-manager | L | 2026-08-29 |
| ENG-018 | Sales demonstration account — a fully seeded AIOrders environment to show prospects | aiorders-admin-hub | shaped | | product-manager | L | 2026-08-29 |
| ENG-019 | Restaurant self-service marketing broadcasts — mass send and drip sequences, scheduled or immediate | restaurant-portal | shaped | | product-manager | L | 2026-08-29 |
| ENG-020 | Marketing ROI reporting — traffic source and revenue attribution on the brand dashboard | restaurant-portal | shaped | | product-manager | M | 2026-08-29 |
| ENG-021 | Website chat-bar engagement visibility — customer questions and self-service FAQ editing on the brand portal | restaurant-portal | shaped | | product-manager | M | 2026-08-29 |
| ENG-022 | Fix broken restaurant-scoped access check on 5 brand-portal handlers — cross-tenant PII/write exposure | aiorders-api | shaped | | architect | M | 2026-08-29 |
| ENG-023 | Add status and internal notes to each brand-portal feedback item | restaurant-portal | shaped | | product-manager | S | 2026-08-29 |
| ENG-024 | Set show_in_marketplace on onboarding's createRestaurant insert, plus a backfill | aiorders-api | shaped | | eng-manager | XS | 2026-08-29 |

`ENG-002` shipped and reached `verified` in an earlier pass today — off the
In-flight table (terminal); see its own board file. `ENG-001` — this
instance's seed ticket — reached `verified` in an earlier pass today, its G3
answered **approved**; off the In-flight table (terminal); see its own board
file. `ENG-003` — its G1 answered **rejected** in an earlier pass today —
reached `dropped`; off the In-flight table (terminal); see its own board
file. `ENG-004` — its `ready-to-ship` confirmation and G3 were both raised
and answered **approved** in an earlier pass — reached `verified`; off the
In-flight table (terminal); see its own board file and the dated entry now
in `_index-archive.md` (rolled this pass, per the keep-three rule). `ENG-005`
— its L1 merge request answered **merged**, independently confirmed by git
ancestry — reached `verified`; off the In-flight table (terminal); see its
own board file and `agents/devops/releases/2026-08-28-aiorders-admin-hub-ENG-005.md`.
`ENG-006` — a control-center dashboard action advanced `blocked → shipped`
ahead of this pass; its L1 merge request answered **approved** and
independently confirmed by git ancestry, then this pass carried it
`shipped → verified` — off the In-flight table (terminal); see its own board
file and `agents/devops/releases/2026-08-28-aiorders-api-ENG-006.md`.
`ENG-012` — its G1 answered **rejected** ("later") in the 2026-08-29
`scheduled` sweep (since rolled to `_index-archive.md`) — reached `dropped`;
off the In-flight table (terminal); see its own board file.

## Waiting on the approver

Cap: 3 across all gates. **2/3, mechanically at cap — both slots now
answered-but-unprocessed, not open.** `ENG-014`'s G1 scope
(`inbox/2026-08-29-eng014-g1-scope.md`) and `ENG-015`'s G1 scope
(`inbox/2026-08-29-eng015-g1-scope.md` — agency/reseller brand-scoping,
`severity: P1`, real cross-tenant data exposure confirmed in code) are both
now `decision: approved` per the 2026-08-29 `intake` pass that shaped
`ENG-021` (checked fresh from `inbox/`, decided 15:54:50 and 16:12:24) —
neither ticket's frontmatter has advanced past `awaiting-scope` yet, so both
still hold their slot until a `decision` pass processes them. The four-item
backlog this section tracked for five consecutive passes
(`ENG-009`/`ENG-010`/`ENG-012`'s G1s, `ENG-013`'s standing question) was
cleared by an earlier 2026-08-29 `scheduled` sweep (since rolled to
`_index-archive.md`).

## 2026-08-29 — decision ENG-013 (G1 scope): another predicted twin no-op — arrived after the fact was already consumed

`decision` event pass, context `inbox/_handled/2026-08-29-eng013-g1-scope.md`
— same shape as `ENG-011`'s own G1 twin logged above (and, before that,
`ENG-008`'s two gate items, `ENG-009`'s G1, `ENG-010`'s G1). Per this
event's own narrower contract (act on the answered gate item, advance only
the ticket it belongs to), scoped to `ENG-013` only — no board-wide sweep.
Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean.

**Confirmed rather than assumed.** `traces/eng-loop-2026-08-29.log`:
`13:01:35 draining queued event: decision (2026-08-29-eng013-g1-scope.md)`
— no `queue: collapsed` line immediately above it this time, so this is a
single fire reaching its own turn late (raised/`notified:` 11:39:39), not a
duplicate-collapse; a long backlog (`ENG-014`..`ENG-024` work) simply sat
ahead of it in the FIFO. By the time it drained, the same `intake` pass
that raised this G1 had already caught the approver's hand-edit
(`decision: approved`, `decided: 2026-08-29T11:45:00.908943+00:00`, bare
approval, ~6 minutes after `notified:`) while still running: the ticket
carried `awaiting-scope → designed → ready`, journaled
(`agents/eng-manager/config/decision-journal.md`, row 28), and the gate
item moved to `inbox/_handled/` with its own processed footer. Checked
fresh rather than trusted: this ticket's own frontmatter (`state: ready`,
`owner: eng-manager`), the journal row, and the footer all agree. Nothing
left for this event to act on.

**0 transitions.** No cap affected — `ENG-013` was already inside the
counted `ready`..`ready-to-ship` machine-WIP range before this pass, and
this G1 was already off both the approver-facing WIP and approval-cap
counts.

**Dead-end sweep (scoped to this event):** confirmed `continue ENG-013` —
fired by the pass that closed this ticket's G1 — still sitting in
`traces/.pending`, undrained, third in line behind two older not-yet-drained
fires (`ENG-013`'s own presignup-leads question, `ENG-012`'s G1). Not a
broken chain, just not yet its turn in the FIFO queue.

**Notify sweep:** nothing to raise (no new gate item this pass); nothing to
nudge (this G1's `notified:`/`decision:` cycle closed same-day, hours
before this pass, well inside the 24h threshold).

Another corroborating occurrence of the open `proposals.md` race (2026-08-27
row, filed by hand — `eng-trigger.sh` should skip the launch when a
`decision` event's named gate item is already in `_handled/`); well past a
dozen occurrences instance-wide as of today, so not re-filed or re-logged as
its own observation — the existing proposal already covers this exactly and
stands unimplemented, waiting on the approver.

`chained: none` — no state change; `ENG-013`'s existing chain (`continue
ENG-013`) is already queued and will run on its own turn. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-013-foodswipe-funnel-stage-control.md`).

## 2026-08-29 — decision ENG-013 (presignup-leads question): a third predicted twin no-op — arrived after the fact was already consumed by a scheduled sweep, not by the pass that raised it

`decision` event pass, context
`inbox/_handled/2026-08-29-eng013-presignup-leads-question.md` — same
twin-no-op shape as `ENG-013`'s own G1 logged directly above, and
`ENG-011`'s tickets-question twin before that. Per this event's own
narrower contract (act on the answered gate item, advance only the ticket
it belongs to), scoped to `ENG-013` only — no board-wide sweep. Mode check
clean (business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
`mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean.

**Confirmed rather than assumed, and a different shape from the two twins
above.** `traces/eng-loop-2026-08-29.log`: `13:15:10 queue: collapsed 1
duplicate event(s)` fires immediately before `13:15:10 draining queued
event: decision (2026-08-29-eng013-presignup-leads-question.md)`, pass
start `13:15:11`, claude launched `13:16:05`. Unlike the G1 twin directly
above (caught live by the same pass that raised it), this question sat
answered-but-unprocessed until a separate `scheduled` event pass (context
`schtasks`, since rolled to `_index-archive.md`) swept it: read the answer
fresh from `inbox/` (`decision: approved`, "Reading B" — a genuine
pre-signup pipeline with autopilot nurture, `decided:
2026-08-29T11:46:34.557123+00:00`), checked for an existing ticket before
filing a new one per the item's own stated next step, and found one — an
independent `intake` pass the same day had already reached the same
conclusion from a different raw request (the "no autopilot for sales
staff/resellers" card) and filed `ENG-017` (presignup lead nurture
autopilot, `agents/eng-manager/board/ENG-017-presignup-lead-nurture-autopilot.md`,
`state: shaped`), already citing this exact verbatim answer as grounding
evidence in its own Notes. Checked fresh rather than trusted: the gate
item's own processed footer, `decision-journal.md` row 31, `ENG-013`'s own
Notes section (added by that scheduled pass), and `ENG-017`'s own Notes
section all agree — the question is closed against `ENG-017`, not
re-opened, and not filed twice. `ENG-013` itself was never blocked by this
question and needed no action from it either way, then or now.

**0 transitions.** No cap affected — `ENG-013` was already inside the
counted `ready`..`ready-to-ship` machine-WIP range before this pass, and
this standing question's approval-cap slot was already freed by the
scheduled pass that closed it — the board header's current cap accounting
(`ENG-014`/`ENG-015`'s G1s only) no longer carries it.

**Dead-end sweep (scoped to this event):** confirmed `continue ENG-013` —
fired when this ticket reached `ready` — still sitting in
`traces/.pending`, undrained, behind a longer backlog than either twin
above last saw. Not stuck — no documented sequencing hold against a
sibling ticket, purely FIFO position.

**Notify sweep:** nothing to raise (no new gate item this pass); nothing to
nudge (this question's `notified:`/`decision:` cycle closed same-day, hours
before this pass, well inside the 24h threshold).

Another corroborating occurrence of the open `proposals.md` race
(2026-08-27 row — `eng-trigger.sh` should skip the launch when a
`decision` event's named gate item is already in `_handled/`); not
re-filed or re-logged as its own observation — the existing proposal
already covers this exactly.

`chained: none` — no state change; `ENG-013`'s existing chain (`continue
ENG-013`) is already queued and will run on its own turn; firing a second
`continue ENG-013` now would only queue a duplicate for the collapse logic
to clean up later. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean. Full detail on the
ticket's own log
(`agents/eng-manager/board/ENG-013-foodswipe-funnel-stage-control.md`).

## 2026-08-29 — decision ENG-012 (G1 scope): a fourth predicted twin no-op — arrived after the fact was already consumed by a scheduled sweep, not by the pass that raised it

`decision` event pass, context `inbox/_handled/2026-08-29-eng012-g1-scope.md`
— same twin-no-op shape as both `ENG-013` entries directly above (the
presignup-leads twin: consumed by a separate scheduled sweep; the G1 twin:
consumed live by the raising pass) and, before those, `ENG-011`'s
tickets-question twin, `ENG-011`'s own G1, `ENG-010`'s G1, `ENG-009`'s G1,
`ENG-008`'s two gate items. Per this event's own narrower contract (act on
the answered gate item, advance only the ticket it belongs to), scoped to
`ENG-012` only — no board-wide sweep. Mode check clean (business-os `.env` →
`MODE=` empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-012`) and
whole-board: both exit 0, clean.

**Confirmed rather than assumed.** `traces/eng-loop-2026-08-29.log`:
`13:24:51 draining queued event: decision (2026-08-29-eng012-g1-scope.md)` —
no `queue: collapsed` line immediately above it, so a single fire reaching
its own turn late (raised/`notified:` 11:22:35), not a duplicate-collapse; a
long backlog simply sat ahead of it in the FIFO. By the time it drained,
this ticket's own G1 (`decision: rejected`, "later", `decided:
2026-08-29T11:46:47.872706+00:00`) had already been fully processed by a
separate `scheduled` event pass (context `schtasks`, since rolled to
`_index-archive.md`): `awaiting-scope → dropped`, journaled
(`decision-journal.md` row 30), gate item moved to `inbox/_handled/` with
its own processed footer. Checked fresh rather than trusted: `ENG-012`'s own
frontmatter (`state: dropped`), the journal row, and the footer all agree.
Nothing left for this event to act on.

**0 transitions.** No cap affected — this G1 was already off both the
approver-facing WIP and approval-cap counts before this pass, closed by the
earlier scheduled sweep; the ticket itself is terminal, off the machine-WIP
range entirely.

**Dead-end sweep (scoped to this event):** no `continue ENG-012` exists in
`traces/.pending`, nor should one — the ticket's prior log entry already
records `chained: none` on the `awaiting-scope → dropped` transition
(terminal state, chaining guard never fires). Confirmed absent from the
pending queue rather than assumed.

**Notify sweep:** nothing to raise (no new gate item this pass); nothing to
nudge (this G1's `notified:`/`decision:` cycle closed same-day, hours before
this pass, well inside the 24h threshold).

Fixed a stale cross-reference while here: the In-flight narrative's `ENG-012`
note still pointed at "the 2026-08-29 `scheduled` sweep below" after that
sweep's own entry had already been rolled to `_index-archive.md` by an
earlier pass — flagged but left unfixed by a prior `intake` pass
(`observations.md`, the `ENG-021`-shaping row); fixed here since it names
the exact ticket this event is about.

Another corroborating occurrence of the open `proposals.md` race (2026-08-27
row — `eng-trigger.sh` should skip the launch when a `decision` event's
named gate item is already in `_handled/`); well past a dozen occurrences
instance-wide as of today, so not re-filed or re-logged as its own
observation — the existing proposal already covers this exactly.

`chained: none` — `dropped` is terminal; the chaining guard never fires on a
terminal state. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-012`) and whole-board: both exit 0, clean. Full detail on the
ticket's own log
(`agents/eng-manager/board/ENG-012-restaurant-support-tickets.md`).
