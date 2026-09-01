# Board

**Next ID: ENG-026** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.)

**Machine WIP 1** (`config/config.yaml` → `wip.machine_limit`). **Corrected
2026-08-29 — the approver's direct instruction: one ticket completed end to
end (through `shipped`) before the next one starts, not several tickets each
advanced by one shallow step per pass.** This was 12 (the `max_5x` tier value)
earlier the same day; see that file for the full rationale.

**Currently 4/1 — over the new cap.** `ENG-009` has moved to `building`
(2026-08-30, extending `ENG-008`'s still-unmerged branch — see its own dated
entry below); `ENG-010` sits at `ready`; `ENG-013` sits at `in-qa`; `ENG-008`
has moved on to `ready-to-ship` (security passed 2026-08-30, release-readiness
confirmed, held there rather than opening its PR — see its own dated entry
below) — all were already in flight when the cap changed and are **not**
being reverted or paused; they drain naturally as each reaches `shipped`.
`ENG-011` and `ENG-007` have both
now left this range for good (`shipped`, both independently confirmed
merged **and deployed live** — see their own dated entries and
`agents/devops/releases/`) — neither counted in this range even while they
sat at `blocked`, so this cap is unchanged by their reconciliation. **No new
ticket enters `ready` until this count is back at or under 1** — `ENG-014`
through `ENG-025` stay at `designed`/`shaped`/`awaiting-scope` (backlog
grooming only, not gated by this cap) until then.

**Approver-facing WIP 2 — 2/2, at cap.** `ENG-016` and `ENG-017` both raised
this pass (`scheduled`, context `schtasks`): `ENG-014` and `ENG-015` had
each since reached `designed` (past their own G1s), freeing the two slots
both had been waiting behind since `shaped`. Picked per
`eng_build_loop.md` step 6's own dispatch ordering — `ENG-016`'s
`priority: next` first, then lowest-id among the unset-priority remainder
(`ENG-017`) — filling exactly the two free slots without exceeding the cap.
**Nothing further should start into an approver-facing state until one of
these two clears.**

**No separate approval cap.** `config/config.yaml` → `wip` records
`approval_cap` as removed 2026-08-29 at the approver's request (a life-os
holdover — "business-os has no cap on decisions queued for the approver").
This board's own prior entries referenced a "3, across all gates" cap that
no longer exists; confirmed against `config.yaml` fresh this pass rather
than propagated from stale board narrative. Approver-facing WIP (above) is
the one real lever on their side now.

`priority:` is a field on every ticket, and **only the approver sets it.** It is
not `severity`, which is the agent's read of how bad a problem is.

## In flight

| ID | Title | Project | State | Priority | Owner | Size | Updated |
|---|---|---|---|---|---|---|---|
| ENG-008 | Influencer board admin management — region/campaign-type preference, rating, collaboration count | aiorders-admin-hub | ready-to-ship | | devops | M | 2026-08-30 |
| ENG-009 | Influencer engagement info — internal activity signal plus a staff-editable social stat | aiorders-admin-hub | building | | eng-manager | S | 2026-08-30 |
| ENG-010 | Influencer relationship notes — staff log for personality, preferences, and off-platform conversations | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-29 |
| ENG-013 | Foodswipe funnel page — staff-settable pipeline stages | aiorders-admin-hub | in-qa | | eng-manager | M | 2026-08-29 |
| ENG-014 | Brand portal self-service — restaurant QR codes and marketing media downloads | restaurant-portal | designed | | eng-manager | M | 2026-08-29 |
| ENG-015 | Agency/reseller (partner) users — brand-scoped locations and a working add-location path | aiorders-admin-hub | designed | | eng-manager | M | 2026-08-29 |
| ENG-016 | Catering page — self-serve quote generator, with automatic stage update | config-site-builder | awaiting-scope | next | approver | L | 2026-08-29 |
| ENG-017 | Autopilot nurture for the presignup sales lead pipeline — stage-triggered email/SMS | aiorders-api | awaiting-scope | | approver | L | 2026-08-29 |
| ENG-018 | Sales demonstration account — a fully seeded AIOrders environment to show prospects | aiorders-admin-hub | shaped | hold | product-manager | L | 2026-08-29 |
| ENG-019 | Restaurant self-service marketing broadcasts — mass send and drip sequences, scheduled or immediate | restaurant-portal | shaped | | product-manager | L | 2026-08-29 |
| ENG-020 | Marketing ROI reporting — traffic source and revenue attribution on the brand dashboard | restaurant-portal | shaped | | product-manager | M | 2026-08-29 |
| ENG-021 | Website chat-bar engagement visibility — customer questions and self-service FAQ editing on the brand portal | restaurant-portal | shaped | | product-manager | M | 2026-08-29 |
| ENG-022 | Fix broken restaurant-scoped access check on 5 brand-portal handlers — cross-tenant PII/write exposure | aiorders-api | designed | | eng-manager | M | 2026-08-29 |
| ENG-023 | Add status and internal notes to each brand-portal feedback item | restaurant-portal | designed | | eng-manager | S | 2026-08-29 |
| ENG-024 | Set show_in_marketplace on onboarding's createRestaurant insert, plus a backfill | aiorders-api | shaped | | eng-manager | XS | 2026-08-29 |
| ENG-025 | Recurring feedback issues, per restaurant, over time | restaurant-portal | designed | | eng-manager | S | 2026-08-29 |

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
off the In-flight table (terminal); see its own board file. `ENG-011` — its
acceptance-check ran this pass (2026-08-30), all 6 acceptance criteria
verified against live production data, no scope creep, cost matched —
reached `verified`; off the In-flight table (terminal); see its own board
file. One live production issue found during that check, unrelated to this
ticket's own diff, filed as `agents/qa/bugs/BUG-001-platform-analytics-cron-401.md`
(P2) and routed via `agents/eng-manager/proposals.md`, 2026-08-30 row.
`ENG-007` — its acceptance-check also ran 2026-08-30 (item 2 of the approved
loyalty sequence), all 6 criteria verified against the live production
schema/trigger/deployed handler code (no live write test — see its own log),
no scope creep, cost matched — reached `verified`; off the In-flight table
(terminal); see its own board file. Step 6b (continue the sequence) did not
fire — `ENG-007`'s own G1 never independently re-affirmed continuing past
this ticket — so a standing question went to the approver instead
(`inbox/2026-08-30-eng007-continue-sequence-question.md`) rather than ticket
3 being auto-filed.

## Waiting on the approver

**Approver-facing WIP 2/2, at cap** (no separate approval cap — see
header).
- `ENG-016` — G1, `inbox/2026-08-29-eng016-g1-scope.md`, raised and
  notified this pass.
- `ENG-017` — G1, `inbox/2026-08-29-eng017-g1-scope.md`, raised and
  notified this pass.

Both notifications logged `SLACK_WEBHOOK_URL unset — cannot notify`
(non-fatal — `lib/eng-notify.sh`'s own designed fallback); both items still
sit live in `inbox/` and the control center. `ENG-018` (`priority: hold`)
and `ENG-019`–`ENG-021` remain at `shaped`, their own G1s drafted but not
raised, until one of the two above clears.

**Also open, not counted against the WIP cap above** (a standing
intake-question, not a ticket in flight — same treatment as the
`ENG-008`/`ENG-013` precedents):
- `ENG-007` — continue the loyalty sequence?,
  `inbox/2026-08-30-eng007-continue-sequence-question.md`, raised and
  notified 2026-08-30.

## 2026-08-30 — continue ENG-007: acceptance-check, `shipped → verified` (terminal); sequence continuation asked, not auto-filed

`continue` event pass, context `ENG-007` — the ticket's own chain fired at
the end of the `shipped` reconciliation pass. Narrow scope per this event's
own contract (resume this ticket from its current state; no board-wide
sweep). Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`) and
whole-board: both exit 0, clean.

Full detail in the ticket's own log. Summary: ran `acceptance-check` to
completion. This ticket has no frontend or user path anywhere in the
sequence, and its acceptance criteria are almost entirely insert-time
DB-trigger behavior — the one gap the migration doc, QA, and the release
record had each independently carried forward as "no live Postgres dry run."
Closed most of it without risking a live write against real financial-config
data: introspected the **deployed** schema/trigger (`pg_proc`/`pg_trigger`/
`information_schema`, read-only via Supabase MCP) and confirmed it
byte-for-byte identical to the design; fetched the deployed `admin-portal`
edge-function bundle and confirmed the actual shipped
`deriveCurrentConfig`/`validateLoyaltyConfigInput`/`mapLoyaltyConfigInsertError`
logic matches what QA unit-tested against source; one live unauthenticated
`GET` against the production endpoint confirmed the admin/sub-admin auth
gate is enforced live (`401 UNAUTHORIZED_NO_AUTH_HEADER`); confirmed 0 rows
in `restaurant_loyalty_configs` today, matching the non-goal that no real
rate has been entered for any restaurant. Hand-traced the confirmed-deployed
trigger logic (not just its git source) against all six acceptance criteria
— all 6 **PASS**. No scope creep against the non-goals (exactly one new
table exists, no ledger/points/redemption table). Cost: $0/month, matches
the PRD.

**Step 6b (continue an approved sequence) checked — did not fire.**
`ENG-007`'s own G1 (`inbox/_handled/2026-08-28-eng007-g1-scope.md`) was a
bare, unconditional "approved" that never itself asked or answered the
continuation question — the literal worked example the skill names as
insufficient ("a plain 'approved' that never touches the sequence does not
clear this bar"). Not inferred from `ENG-006`'s original sequence-wide G1
either, despite `eng_build_loop.md` step 3's narrative reading that way at a
glance — see the observation filed on this tension, since it's likely to
recur at ticket 3's own eventual acceptance-check. Asked rather than
assumed: raised `inbox/2026-08-30-eng007-continue-sequence-question.md`
(`gate: intake-question`, standing/non-blocking, same shape as the
`ENG-008`/`ENG-013` precedents), naming that the one real open risk
(Walletly) is already resolved at `ENG-007`'s own G2. Ran
`lib/eng-notify.sh raise` — same established `SLACK_WEBHOOK_URL unset`
failure; `notified:` stamped at write time.

**State: `shipped → verified`**, `owner: devops → eng-manager`. **1
transition**, well under the cap of 4. **Consequence:** `machine_wip`
unaffected (both states outside the counted range). Approver-facing WIP
unchanged at 2/2 — a standing intake-question isn't a ticket in flight, same
treatment the `ENG-008`/`ENG-013` precedents established.

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for terminal state. No wider sweep — out of scope for a
`continue` event naming `ENG-007` specifically. **Notify sweep:** this
pass's own standing question raised and stamped above; nothing else to
nudge within this event's scope. **Observations filed** (`observations.md`):
the deployed-artifact verification method (reusable for the next
trigger-heavy, no-frontend ticket), and the `eng_build_loop.md`
step 3 / `SKILL.md` 6b tension on what "the G1 answer" means for a ticket
that continues, rather than originates, a sequence.

`chained: none` — `verified` is terminal, and no new ticket was filed this
pass (6b's condition on the G1 not met), so there is nothing else to chain
— the standing question waits on the approver like any gate item. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`) and
whole-board: both exit 0, clean, no `WAIVED:` lines. Board already held
three dated entries (`continue ENG-008` round 2, `watch (schtasks)`,
`continue ENG-011`) before this one, so the oldest (`continue ENG-008`
round 2) was moved to `_index-archive.md`, prepended under its header, to
make room — leaving three (`watch (schtasks)`, `continue ENG-011`, this
one), per the keep-three rule.

## 2026-08-30 — continue ENG-008: security PASS, release-readiness confirmed, `in-qa → in-security → ready-to-ship` — held, not chained, by the approver-facing WIP cap

`continue` event pass, context `ENG-008`, this ticket's turn at the front
of `traces/.pending`. Narrow scope per the event's own contract (resume
this ticket from its current state; no board-wide sweep). Mode check clean
(business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
`mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean.

Full detail in the ticket's own log. Summary: ran the security gate fresh
against both remotes (no worktree disruption — `aiorders-api` was mid-flight
on `ENG-013`'s branch, read via `git diff` against the remote refs).
Threat-modelled the change, walked OWASP A01–A10, hand-traced the auth
chain (`hasInfluencerAdminAccess` consumes a server-derived profile, never
a client claim), and independently re-read the test file to confirm the
403/405 negative cases are real and automated. One classification note (the
new `GET` route's `select('*')` returns real PII — email/phone — so
**Confidential** rather than the design doc's "business-internal" framing;
not new exposure, and not blocking). **Verdict: PASS**, no blocking
finding. Receipt written: `agents/security/reviews/ENG-008.md`.

Release-readiness (devops role) held in the same pass: all four upstream
gate receipts re-verified present (review, migration, quality, security);
rollback reasoned through (drop four new columns) but not live-drilled —
same repo-wide host constraint `ENG-007`'s own release record carried at
this identical boundary and still passed; observability and cost ($0/month)
both confirmed. Readiness checklist **passes**.

**Step 4 (open the L1 PRs, write the merge request) deliberately withheld.**
Approver-facing WIP is genuinely 2/2 (`ENG-016`, `ENG-017`, both re-checked
directly in `inbox/` — neither carries a `decision:` field). An L1 PR
awaiting merge is explicitly one of the three things `eng_build_loop.md`'s
Guards section counts against this cap, and names no carve-out for a ticket
already in flight before the cap filled (unlike machine WIP, which
explicitly does grandfather that case) — read as deliberate, not guessed
past. Confirmed first that no PR already existed in either repo
(`gh pr list`, both empty) — a fresh hold, not a missed recovery.

**3 transitions** (`in-qa → in-security → ready-to-ship`), under the cap of
4 — the fourth (`ready-to-ship → blocked` via the PR) is exactly what's
withheld. `machine_wip` unaffected, still 4 (inside `ready..ready-to-ship`,
unchanged count). Approver-facing WIP unchanged at 2/2 — the point of the
hold.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing to raise or nudge — a machine gate passing
doesn't reach the approver. **Observation filed** (`observations.md`):
first time this board has checked the approver-facing WIP cap at the
`ready-to-ship → PR-open` boundary rather than at intake/G1 time.

`chained: none` — held by the approver-facing WIP cap (2/2), one of the
explicit non-chain conditions. Resumes naturally once `ENG-016` or
`ENG-017`'s `decision` event clears the cap, or the next `scheduled`/`watch`
sweep finds it freed. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
whole-board: both exit 0, clean, no `WAIVED:` lines. Board held three dated
entries (`watch (schtasks)`, `continue ENG-011`, `continue ENG-007`) before
this one, so the oldest (`watch (schtasks)`) was moved to
`_index-archive.md`, prepended under its header, to make room — leaving
three (`continue ENG-011`, `continue ENG-007`, this one), per the
keep-three rule.

## 2026-08-30 — continue ENG-009: built, `ready → building` — both repos, extending ENG-008's still-unmerged branch

`continue` event pass, context `ENG-009`, this ticket's turn at the front of
`traces/.pending` following the sequencing hold lifted earlier today. Narrow
scope per the event's own contract (resume this ticket from its current
state; no board-wide sweep). Mode check clean (business-os `.env` → `MODE=`
empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-009`) and
whole-board: both exit 0, clean.

Full detail in the ticket's own log. Summary: branched
`feat/ENG-009-influencer-engagement-info` off `ENG-008`'s still-unmerged tip
in both repos (required, not optional — this ticket's design extends the
handler and edit form `ENG-008` built, which don't exist on `main` yet).
Re-verified the live schema before writing the migration (Supabase MCP,
read-only): confirmed the two new columns don't exist and that production's
applied migration head hasn't moved past either sibling ticket's own
still-pending migration, so `20260830100000` sorts after both. Built both
readings the PRD asked for: Reading B reuses the existing, previously-unwritten
`followers`/`engagement` columns via `PATCH admin-portal/influencers/{id}`
(extending `ENG-008`'s `EDITABLE_FIELDS`), stamping a new
`social_stats_updated_at` server-side; Reading A is a new `GET
admin-portal/influencers/activity`, service-role-only, deriving an activity
aggregate from `influencer_invitations` on read and storing it nowhere.

**One design-vs-shipped gap resolved mid-build**, same class as `ENG-008`'s
own PUT/PATCH catch against this ticket's design (2026-08-29), found from the
other direction this time: the design's Interfaces section assumed a
list-shaped `GET /admin-portal/influencers` that `ENG-008` never actually
built (it shipped a per-id, frontend-uncalled `GET .../influencers/{id}`
instead — written against `ENG-008`'s design, not its diff). Resolved with
the new `/activity` route rather than reshaping the existing per-id GET; the
step 6b artifact grep found no other file in the department assumes the
list-shaped form, so this stayed a local fix. Second same-week occurrence of
this exact gap class — observation filed flagging it as a pattern, not just
an incident.

Self-tested both repos: `aiorders-api` — `deno check` clean, `deno test`
**32/32 passing** (17 pre-existing + 15 new), whole-tree `deno check` still
exactly 17 pre-existing errors, none in `influencers.ts`. `aiorders-admin-hub`
— `npm run lint` 150 pre-existing errors (unchanged), zero new; `npm run
build` clean. Migration doc written
(`agents/database/migrations/ENG-009-influencer-engagement-info.md`, gate
verdict **pass**). Both branches committed and pushed
(`aiorders-api@4eb4b1b`, `aiorders-admin-hub@328db29`); PR bodies drafted in
the ticket log, PRs not yet opened (devops's step, same as `ENG-008`).

**State: `ready → building`**, `owner` unchanged (`eng-manager`). **1
transition**, well under the cap of 4 — review + quality (combined hop) is a
fresh session's work by design. **Consequence:** `machine_wip` unaffected —
`ENG-009` was already inside the counted `ready..ready-to-ship` range at
`ready`; `building` is still inside it, so the board stays 4 (over the 1
cap, still draining naturally per the header's grandfather clause).
Approver-facing WIP and approval cap both unaffected — no gate touched this
hop.

**Dead-end sweep (scoped to this event):** no other ticket touched;
`ENG-010` remains correctly held behind both `ENG-008` and this ticket (see
its own log, unchanged this pass). **Notify sweep:** nothing to raise (no
gate item written) or nudge. **Observation filed** (`observations.md`): the
design-vs-shipped-endpoint-shape gap above.

`chained: ENG-009` — `building` is agent-owned (review + quality next, a
fresh session by this loop's own design) — not the approver, not blocked,
not terminal, not held by a cap. Fired
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-009` before
exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-009`) and whole-board: see below. Board held two dated entries
(`continue ENG-007`, `continue ENG-008`) before this one — under the
keep-three limit, so nothing rolled to `_index-archive.md` this pass.

