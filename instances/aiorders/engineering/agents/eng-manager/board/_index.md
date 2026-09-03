# Board

**Next ID: ENG-029** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.)

**Machine WIP 1** (`config/config.yaml` → `wip.machine_limit`). **Corrected
2026-08-29 — the approver's direct instruction: one ticket completed end to
end (through `shipped`) before the next one starts, not several tickets each
advanced by one shallow step per pass.** This was 12 (the `max_5x` tier value)
earlier the same day; see that file for the full rationale.

**Currently 0/1 — free.** `ENG-024` left the slot this pass (`ready-to-ship →
blocked` — release-readiness complete, PR opened
(`aiorders-api` #11), merge request raised
(`inbox/2026-09-03-eng024-merge-request.md`)); see `ENG-024`'s own
board-file log. `ENG-015` freed the slot earlier today the same way
(`ready-to-ship → blocked`); see `ENG-015`'s own board-file log for all six
hops. `ENG-014`, `ENG-017`, `ENG-023`, `ENG-025` (all `designed`) still owe
an unraised G2 and are not yet candidates for this slot regardless of
priority/severity — `ENG-018` stays excluded outright (`priority: hold`).
No ticket has started into the freed slot yet — narrow scope, this event's
own contract (`continue ENG-024` touches only its own ticket); picking the
next To-do-column ticket is the next `scheduled`/`continue`-elsewhere pass's
work.

**Approver-facing WIP: uncapped.** `wip.approver_limit` was raised from `2`
to `unlimited` on 2026-09-02, by the approver's own explicit, dated decision
recorded in this instance's own override, `config/config.yaml` (not the
department-template default of 2, which is stale for this instance and
never updated to match — the two files disagree on purpose, per the
"instance overrides the template" split, but at least one prior pass read
the wrong one). Read the override's own comment as the live rule: "never
withhold a new ticket for this reason, no matter how many are already
`blocked_on: approver`." **This pass corrected a real consequence of the
stale reading**: `ENG-019`/`ENG-020`/`ENG-021` were sitting at `shaped`,
each held only by "the WIP-2 cap is already over" — true when written
(2026-08-29), false since 2026-09-02, and never rechecked in the five days
since. All three PRDs were complete with no material divergence; this pass
raised all three G1s. One observation filed (`observations.md`) on the
pattern itself. The list below is now informational — a live count of what
the approver has open, not a gate on anything new starting.

- `ENG-008` — its original merge request was answered `changed`
  (2026-09-01) and closed; this pass's own fix went through round-3
  review/quality/security and devops's release-readiness hop then raised a
  **fresh** merge request (`inbox/2026-09-02-eng008-merge-request.md`,
  unanswered) once both PRs reflected the corrected diff. Rejoins the
  count — not a new start, since the ticket was already the sole machine-WIP
  occupant before this hop; a continuing ticket reaching its own next gate
  is not gated by this cap, only a fresh To-do-column start is (see the
  ticket's own log for the reasoning, cross-referencing `ENG-009`'s and
  `ENG-010`'s identical precedent earlier tonight).
- `ENG-013` — its follow-up scope question
  (`inbox/2026-09-02-eng013-stage-config-question.md`) came back **approved,
  "Reading a"**: ship the two open PRs as-is, file stage-taxonomy
  configuration separately (`ENG-028`, below). Question closed, moved to
  `inbox/_handled/`. Both PRs (`aiorders-api#5`, `aiorders-admin-hub#4`)
  confirmed still open, not merged (`git`/`gh`, fresh this pass) — ticket
  stays `blocked`, but **drops off this count**: no inbox file is open for
  it any more (its merge request closed 2026-09-01, its question closes
  this pass), same shape `ENG-007`/`ENG-011` once had. Not a gap — merging
  either PR on GitHub is the only remaining step, and it needs no written
  reply to do it.
- `ENG-009` — its own devops release-readiness hop passed all four gates,
  opened both PRs, and raised its own L1 merge request
  (`inbox/2026-09-02-eng009-merge-request.md`), still unanswered. Counted.
- `ENG-010` — same shape, still unanswered
  (`inbox/2026-09-02-eng010-merge-request.md`). Counted.
- `ENG-026` — its G1 was answered **approved**, no additional comment
  (2026-09-03T15:51:04), and processed this pass: `awaiting-scope →
  designed`, `owner: approver → architect`, PRD `status: approved`.
  **Drops off this count** — same shape `ENG-013`/`ENG-016` already set:
  no inbox file is open for it any more
  (`inbox/_handled/2026-09-02-eng026-g1-scope.md`). Handed to the
  architect for the tech design, not attempted inline; see the ticket's
  own log for full reasoning.
- `ENG-016` — its rescope G1 (Piece 1) was answered **approved**, "Lets
  start with piece 1" (2026-09-03T15:47:46), and processed this pass:
  `awaiting-scope → designed`, `owner: approver → architect`, PRD `status:
  approved`. **Drops off this count** — same shape `ENG-013` already set:
  no inbox file is open for it any more
  (`inbox/_handled/2026-09-02-eng016-g1-rescope.md`). Handed to the
  architect for the tech design itself, not attempted inline; see the
  ticket's own log for full reasoning.
- `ENG-027` — item 3 of `ENG-006`'s approved loyalty sequence, per the
  approver's own **yes** on
  `inbox/2026-08-30-eng007-continue-sequence-question.md`. First G1
  answered **changed** (2026-09-03T16:00:32) — accrual moves from
  placement to fulfilment, approver-specified mechanism (auto-complete
  timer). Rescoped this pass: re-verifying the fork found the department's
  own prior G1 was wrong — AIOrders already subscribes to CloudWaitress's
  completion/cancellation webhooks and discards them, so the signal needs
  un-ignoring, not building. `size: M → L`. Fresh G1 raised
  (`inbox/2026-09-03-eng027-g1-rescope.md`), unanswered. Counted — the
  sequence's own approved continuation per `eng_build_loop.md` step 3's
  carve-out, not agent-invented scope, so not held behind the cap being
  over (same as the shaping itself wasn't).
- `ENG-028` — new ticket, filed this pass: staff-configurable Foodswipe
  pipeline stage set, filed per the approver's own **Reading A** on
  `ENG-013`'s stage-config question ("file stage-taxonomy configuration as
  ENG-0XX, a new ticket, built on top of this"). Same carve-out `ENG-027`
  used — the approver's own request, not agent-invented scope. G1 raised
  (`inbox/2026-09-03-eng028-g1-scope.md`), unanswered. Sized `L`; depends
  on `ENG-013`.
- `ENG-022` — P0 cross-tenant PII/write exposure; code review, quality, and
  security all passed this pass, then devops's own release-readiness hop
  opened the PR and raised a fresh L1 merge request
  (`inbox/2026-09-03-eng022-merge-request.md`), unanswered. Counted — not a
  new start, since the ticket was already the sole machine-WIP occupant
  before this hop; a continuing ticket reaching its own next gate is not
  gated by this cap, only a fresh To-do-column start is, same precedent
  `ENG-008`/`ENG-009`/`ENG-010`/`ENG-016` already set tonight.
- `ENG-015` — code review (round 2), quality, security, and migration all
  passed; devops's own release-readiness hop found both projects L1,
  confirmed rollback/observability/cost all clear, then opened both PRs
  (`aiorders-api` #10, `aiorders-admin-hub` #8) and raised a single L1 merge
  request covering both (`inbox/2026-09-03-eng015-merge-request.md`). P1 fix
  for a live cross-tenant restaurant-visibility/write exposure.
- `ENG-024` — fast-lane combined review (review/suite/OWASP) passed;
  devops's own release-readiness hop confirmed rollback (reasoned, not
  live-drilled — standing host limitation), observability, and cost ($0/mo)
  all clear, named the one gap (no dedicated `database`-gate verdict exists
  for the backfill migration on this lane — assessed low-risk instead, see
  the ticket's own log), then opened `aiorders-api` PR #11 and raised this
  merge request (`inbox/2026-09-03-eng024-merge-request.md`). P1 fix for
  onboarded restaurants missing from marketplace search.
- `ENG-019` — its G1 was answered **approved**, no additional comment
  (2026-09-03T15:52:30.648626+00:00), and processed this pass:
  `awaiting-scope → designed`, `owner: approver → architect`, PRD `status:
  approved`. **Drops off this count** — same shape `ENG-016`/`ENG-026`
  already set: no inbox file is open for it any more
  (`inbox/_handled/2026-09-03-eng019-g1-scope.md`). Handed to the architect
  for the tech design, not attempted inline; see the ticket's own log for
  full reasoning.
- `ENG-020` — its G1 was answered **approved**, no additional comment
  (2026-09-03T15:53:14.495206+00:00), and processed this pass:
  `awaiting-scope → designed`, `owner: approver → architect`, PRD `status:
  approved`. **Drops off this count** — same shape `ENG-016`/`ENG-026`/
  `ENG-019` already set: no inbox file is open for it any more
  (`inbox/_handled/2026-09-03-eng020-g1-scope.md`). Handed to the architect
  for the tech design, not attempted inline; see the ticket's own log for
  full reasoning.
- `ENG-021` — its G1 was answered **approved**, no additional comment
  (2026-09-03T15:54:34.623417+00:00), and processed this pass:
  `awaiting-scope → designed`, `owner: approver → architect`, PRD `status:
  approved`. **Drops off this count** — same shape `ENG-016`/`ENG-026`/
  `ENG-019`/`ENG-020` already set: no inbox file is open for it any more
  (`inbox/_handled/2026-09-03-eng021-g1-scope.md`). Handed to the architect
  for the tech design, not attempted inline; see the ticket's own log for
  full reasoning.

Eight items genuinely on the approver's plate right now, all unanswered:
`ENG-008` (fresh merge request), `ENG-009`, `ENG-010`,
`ENG-027` (**fresh G1 raised this pass** — the first G1's `changed` answer
was processed and the ticket rescoped `M → L`; see the header bullet above
and the ticket's own board-file log for the full reasoning), `ENG-028`
(new G1), `ENG-022`
(merge request), `ENG-015` (merge request), `ENG-024` (new merge request,
this pass). No cap on how many of
these may be open at once — see header above; nothing here gates a new
start. **`ENG-013`, `ENG-016`, `ENG-026`, `ENG-019`, `ENG-020` and `ENG-021`
drop off this list, not off the board** —
`ENG-013`'s scope question closed with no new written item, same shape
`ENG-007`/`ENG-011` once had: `blocked`, `blocked_on: approver`, two open
PRs, nothing in `inbox/` left to answer. `ENG-016`'s rescope G1, `ENG-026`'s
G1, `ENG-019`'s G1, `ENG-020`'s G1 and `ENG-021`'s G1 were all answered
**approved** and moved to `designed`/`architect` — see the header bullets
above. Merging either of `ENG-013`'s PRs on GitHub is the only remaining
step for that ticket; see the In-flight table.

**No separate approval cap exists.** `approval_cap` was removed 2026-08-29
at the approver's own request (`config/config.yaml`; also stated in
`schedules/eng_build_loop.md`'s Guards section). `wip.approver_limit` is the
only approver-side lever left, and it is itself `unlimited` since
2026-09-02 (see header above) — not `2`; that number is the department
template's default, superseded by this instance's own override, and this
paragraph itself carried the stale value until this pass. `ENG-018` stays
excluded outright (`priority: hold`); `ENG-017` already past its own G1, now
`designed`.

<!-- merge note: local (HEAD) recorded a parallel 2026-08-30 history where
  `ENG-009` reached `building`, `ENG-008` reached `ready-to-ship` and the
  approver-facing WIP cap was filled by `ENG-016`/`ENG-017`'s G1s instead of
  merge requests. Remote's account above is dated later (through
  2026-08-31) and is internally consistent with the rest of this merge
  (ENG-008/ENG-013/ENG-014/ENG-015/ENG-023/ENG-025 all resolved in remote's
  favor elsewhere in this merge) — kept as the board's current state; local's
  contradicting header dropped rather than merged in. -->

`priority:` is a field on every ticket, and **only the approver sets it.** It is
not `severity`, which is the agent's read of how bad a problem is.

## In flight

| ID | Title | Project | State | Priority | Owner | Size | Updated |
|---|---|---|---|---|---|---|---|
| ENG-008 | Influencer board admin management — region/campaign-type preference, rating, collaboration count | aiorders-admin-hub | blocked | | approver | M | 2026-09-02 |
| ENG-009 | Influencer engagement info — internal activity signal plus a staff-editable social stat | aiorders-admin-hub | blocked | | approver | S | 2026-09-02 |
| ENG-010 | Influencer relationship notes — staff log for personality, preferences, and off-platform conversations | aiorders-admin-hub | blocked | | approver | S | 2026-09-02 |
| ENG-013 | Foodswipe funnel page — staff-settable pipeline stages | aiorders-admin-hub | blocked | | approver | M | 2026-09-03 |
| ENG-014 | Brand portal self-service — restaurant QR codes and marketing media downloads | restaurant-portal | designed | | architect | M | 2026-08-31 |
| ENG-015 | Agency/reseller (partner) users — brand-scoped locations and a working add-location path | aiorders-admin-hub | blocked | | approver | M | 2026-09-03 |
<!-- merge note: local (HEAD) had ENG-016/ENG-017 at `awaiting-scope`/`approver`
  (G1s raised 2026-08-29, same date as remote's row) while remote has them
  still `shaped`/`product-manager`, G1 deliberately not yet raised — a real
  contradiction between the two branches' divergent histories, not just a
  stale date. Kept remote's rows for consistency with remote's later
  (2026-08-31) "Waiting on the approver" section below, which explicitly
  states ENG-016 through ENG-021 are G1-drafted but not yet raised.
  ADDENDUM, 2026-09-01 `watch` pass: this was wrong for ENG-016 specifically
  and has been reversed below — remote's account wasn't stale, it was
  missing an event outright (local really did raise this G1 on 2026-08-29;
  remote's host never saw that pass run). Confirmed against ENG-016's own
  board file and PRD, both still `awaiting-scope`/`status: awaiting-scope`
  and never touched by the merge. ENG-017's row is unaffected by this
  addendum — it independently reached `designed` via the 09:30 pass's own
  recovery work, on top of whichever account this merge originally kept. -->
| ENG-016 | Catering page — self-serve quote generator, with automatic stage update (rescoped to Piece 1: order capture + stage automation, no pricing) | config-site-builder | designed | next | architect | L | 2026-09-03 |
| ENG-017 | Autopilot nurture for the presignup sales lead pipeline — stage-triggered email/SMS | aiorders-api | designed | | architect | L | 2026-09-01 |
| ENG-018 | Sales demonstration account — a fully seeded AIOrders environment to show prospects | aiorders-admin-hub | shaped | hold | product-manager | L | 2026-08-29 |
| ENG-019 | Restaurant self-service marketing broadcasts — mass send and drip sequences, scheduled or immediate | restaurant-portal | designed | now | architect | L | 2026-09-03 |
| ENG-020 | Marketing ROI reporting — traffic source and revenue attribution on the brand dashboard | restaurant-portal | designed | now | architect | M | 2026-09-03 |
| ENG-021 | Website chat-bar engagement visibility — customer questions and self-service FAQ editing on the brand portal | restaurant-portal | designed | now | architect | M | 2026-09-03 |
| ENG-022 | Fix broken restaurant-scoped access check on 5 brand-portal handlers — cross-tenant PII/write exposure | aiorders-api | blocked | | approver | M | 2026-09-03 |
| ENG-023 | Add status and internal notes to each brand-portal feedback item | restaurant-portal | designed | | architect | S | 2026-08-31 |
| ENG-024 | Set show_in_marketplace on onboarding's createRestaurant insert, plus a backfill | aiorders-api | blocked | | approver | XS | 2026-09-03 |
| ENG-025 | Recurring feedback issues, per restaurant, over time | restaurant-portal | designed | | architect | S | 2026-08-31 |
| ENG-026 | FoodSwipe channel-visibility toggles and capability-based discovery | restaurant-marketplace | designed | now | architect | M | 2026-09-03 |
| ENG-027 | Loyalty points ledger, balances, and earn API — online-order and dine-in accrual | aiorders-api | awaiting-scope | | approver | L | 2026-09-03 |
| ENG-028 | Foodswipe funnel — staff-configurable pipeline stage set | aiorders-admin-hub | awaiting-scope | | approver | L | 2026-09-03 |

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
<!-- merge note: local (HEAD) and remote diverge here into two parallel
  2026-08-30+ histories for `ENG-007`/`ENG-008`/`ENG-009`/`ENG-011` and the
  "Waiting on the approver" section — different, contradictory accounts of
  the same days (e.g. local has `ENG-007` reaching `verified` via a
  `continue`-event acceptance-check with an outstanding "continue the
  sequence?" question; remote has it found already merged on GitHub and
  carried to `verified` by a `scheduled` sweep, with no such question).
  Kept remote's account, which is dated later (through 2026-08-31) and is
  consistent with the rest of this merge favoring remote's state for
  `ENG-008`/`ENG-013`/`ENG-014`/`ENG-015`/`ENG-023`/`ENG-025` above; local's
  contradicting narrative and its 2026-08-30 log entries (`continue ENG-007`
  acceptance-check, `continue ENG-008` security/release-readiness,
  `continue ENG-009` build) are dropped rather than merged in, since they
  describe a divergent sequence of events on the same tickets rather than
  independent, additive progress. -->
off the In-flight table (terminal); see its own board file. `ENG-007` — found
merged on GitHub with no gate item ever raised (a now-moot Saturday
window-hold had blocked the department's own PR-open step); confirmed via
git ancestry and `gh pr view`, receipts verified, carried
`ready-to-ship → shipped → verified` in the 2026-08-30 `scheduled` sweep —
off the In-flight table (terminal); see its own board file and
`agents/devops/releases/2026-08-30-aiorders-api-ENG-007.md`. `ENG-011` —
this board's first two-repo ticket; both PRs found merged directly on
GitHub, 40 seconds apart, confirmed independently on each repo, carried
`blocked → shipped → verified` in the same 2026-08-30 sweep — off the
In-flight table (terminal); see its own board file and
`agents/devops/releases/2026-08-30-ENG-011-aiorders-api-and-admin-hub.md`.

## Waiting on the approver

**No cap — `wip.approver_limit: unlimited` since 2026-09-02 (see header
above). Eight items currently open** (composition changed this pass:
`ENG-021`'s G1 answered and closed; `ENG-020`'s, `ENG-026`'s, `ENG-019`'s
and `ENG-016`'s rescope G1 all closed in earlier passes today), listed here
for visibility, not because any number of them blocks a new start. **`ENG-008`'s L1 merge request, revised**
(`inbox/2026-09-02-eng008-merge-request.md`) — raised tonight (~23:24):
both PRs updated in place (`aiorders-api` #6, `aiorders-admin-hub` #5, same
PR numbers as the original request), bodies rewritten to describe the
corrected diff, all four gates passed on round 3; not yet due for a nudge.
**`ENG-009`'s L1 merge request**
(`inbox/2026-09-02-eng009-merge-request.md`) — raised this morning
(~10:51): both PRs open (`aiorders-api` #7, `aiorders-admin-hub` #6, each
stacked on `ENG-008`'s branch rather than `main`), all four gates passed,
no reply required (merging either PR directly on GitHub is itself the
decision); crossed 24h unanswered this pass (~11:34 UTC) — nudged,
`nudged: 2026-09-03T11:34:08` stamped. **`ENG-010`'s L1
merge request** (`inbox/2026-09-02-eng010-merge-request.md`) — raised this
evening (~17:45): both PRs open (`aiorders-api` #8, `aiorders-admin-hub`
#7, each stacked on `ENG-009`'s branch), all four gates passed, same
shape; crossed 24h unanswered during `ENG-021`'s decision pass (~17:46
UTC) — nudged, `nudged: 2026-09-03T17:46:05` stamped. `ENG-013`'s
stage-configuration question
(`inbox/2026-09-02-eng013-stage-config-question.md`) was answered
**approved, "Reading a"** (2026-09-03T15:23:36) and closed this pass — ship
the two open PRs as-is, file stage-taxonomy configuration separately (see
`ENG-028` below). No new written item for `ENG-013` itself: both PRs
confirmed still open (`git`/`gh`, fresh this pass), and merging either on
GitHub is the only remaining step, same shape `ENG-009`/`ENG-010` are
already in. **`ENG-026`'s G1**
(`inbox/_handled/2026-09-02-eng026-g1-scope.md`) — raised 2026-09-02
(~22:19): the approver's own hand-edited answer to its standing
intake-question confirmed a per-channel visibility toggle and specified it
completely; PM scoped the ticket to that piece alone (three other bundled
capabilities named as deferred future tickets). Answered **approved**, no
additional comment (2026-09-03T15:51:04), and closed this pass —
`awaiting-scope → designed`, `owner: approver → architect`, PRD `status:
approved`, handed to the architect for the tech design. `ENG-016`'s rescope G1
(`inbox/_handled/2026-09-02-eng016-g1-rescope.md`) was answered
**approved**, "Lets start with piece 1" (2026-09-03T15:47:46), and closed
this pass — `awaiting-scope → designed`, `owner: approver → architect`,
handed to the architect for the tech design. Pieces 2 (pricing/price-book)
and 3 (owner edit/resend + view tracking) remain named in the PRD, still
not filed; Piece 2 still waits on a named answer for who maintains each
restaurant's price book. **`ENG-027`'s first G1**
(`inbox/_handled/2026-09-03-eng027-g1-scope.md`) — raised 2026-09-03
(~00:03): item 3 of `ENG-006`'s approved loyalty sequence (points ledger,
balances, earn API), filed per the approver's own **yes** on the standing
continuation question. Answered **changed** (2026-09-03T16:00:32):
"Accrual at fulfillment, have ticket completed as autocompleted after x
hours if not cancelled or deleted." Processed this pass — rescoped in
place rather than advanced, since a `changed` answer isn't an approval.
Re-verifying the fork against live code found the department's own prior
G1 wrong in the approver's favour: AIOrders already subscribes to
CloudWaitress's `order_completed_updated`/`order_cancelled_updated`
webhooks and its own handler discards everything but `order_new`, so the
fulfilment signal needs un-ignoring, not building from scratch. But the
approver's own condition ("if not cancelled or deleted") is vacuous as the
code stands — nothing can mark an order cancelled today — named plainly
rather than built as decorative. Sized fresh at `L` (was `M`). **`ENG-027`'s
fresh G1** (`inbox/2026-09-03-eng027-g1-rescope.md`) — raised this pass
(~13:15): recommends building the approver's version now, one ticket,
carrying four riders (a concrete number for the "x hours" placeholder,
proposed 24h; the still-open earn-% base rider from the first G1, not
dropped for going unanswered; which rate applies now that placement and
accrual are hours apart; whether the order's own status column becomes the
completion signal). Full reasoning: `ENG-027`'s own board-file log,
`agents/product-manager/specs/ENG-027-loyalty-points-ledger-and-earn.md`,
and `decision-journal.md`. **`ENG-022`'s L1 merge request**
(`inbox/2026-09-03-eng022-merge-request.md`) — raised this pass (~01:26):
code review, quality, and security all passed fresh this pass; devops's own
release-readiness hop found the project L1, confirmed rollback (no
migration — reverting the single commit undoes the whole diff),
observability (the fix's own denial logging), and cost ($0/month) all
clear, then opened `aiorders-api` PR #9 and raised this request. The P0
this ticket exists for — live cross-tenant PII read/write exposure — is
resolved by this PR alone; merging is the only step left. **`ENG-015`'s L1
merge request** (`inbox/2026-09-03-eng015-merge-request.md`) — raised this
pass (~10:03): code review (round 2, after a round-1 fail on missing tests
plus a mass-assignment authz bug, both closed), quality, security, and
migration all passed; devops's own release-readiness hop found both
projects L1, confirmed rollback/observability/cost all clear, then opened
`aiorders-api` PR #10 and `aiorders-admin-hub` PR #8 and raised this single
two-repo request. The P1 this ticket exists for — a partner seeing/writing
every restaurant on the platform, and a broken add-location path — is
resolved once **both** PRs merge; they must land together, named explicitly
in both PR bodies and this request. **`ENG-019`'s G1**
(`inbox/_handled/2026-09-03-eng019-g1-scope.md`) — raised earlier today
(~11:51 UTC): restaurant marketing broadcasts (one-time + drip, email/SMS,
coupon-code ROI), scoped exactly as the PRD proposes; readback showed no
material divergence, so it went straight to G1. Answered **approved**, no
additional comment (2026-09-03T15:52:30), and closed this pass —
`awaiting-scope → designed`, `owner: approver → architect`, PRD `status:
approved`, handed to the architect for the tech design. **`ENG-020`'s G1**
(`inbox/_handled/2026-09-03-eng020-g1-scope.md`) — raised earlier today
(~11:56 UTC): per-restaurant traffic-source/revenue attribution on the
brand dashboard, reusing already-captured data; same no-divergence shape.
Answered **approved**, no additional comment (2026-09-03T15:53:14), and
closed this pass — `awaiting-scope → designed`, `owner: approver →
architect`, PRD `status: approved`, handed to the architect for the tech
design. **`ENG-021`'s G1**
(`inbox/_handled/2026-09-03-eng021-g1-scope.md`) — raised this pass (~11:56
UTC): chat-bar question visibility plus a self-service FAQ editor on the
brand portal; same no-divergence shape. All three were sitting at `shaped`,
each held only by a stale "WIP-2 cap is already over" reading — true when
written (2026-08-29), false since the approver's own 2026-09-02 override
raised the cap to unlimited, never rechecked in the five days since. See
the header above for the full correction. Answered **approved**, no
additional comment (2026-09-03T15:54:34), and closed this pass —
`awaiting-scope → designed`, `owner: approver → architect`, PRD `status:
approved`, handed to the architect for the tech design. **`ENG-028`'s G1**
(`inbox/2026-09-03-eng028-g1-scope.md`) — raised this pass (~16:10 UTC):
staff-configurable Foodswipe pipeline stage set, filed per the approver's
own **Reading A** on `ENG-013`'s stage-config question ("file
stage-taxonomy configuration as ENG-0XX, a new ticket, built on top of
this"); sized `L` (new data model, cross-project). Carries a rider on the
one assumption most worth correcting — that staff-defined stages are
manual-only, since no generic auto-classification mechanism exists in
`classifyStage()` today — and flags both that `ENG-022` (P0) outranks it
and that `ENG-013`'s two PRs should merge first. **`ENG-024`'s L1 merge
request** (`inbox/2026-09-03-eng024-merge-request.md`) — raised this pass
(~10:58 local): fast-lane combined review (review/suite/OWASP) passed
earlier today; devops's own release-readiness hop confirmed rollback
(reasoned, not live-drilled — the same standing host limitation
`ENG-007`'s release record already named), observability, and cost
($0/month) all clear, named the one real gap (the backfill migration has no
dedicated `database`-gate verdict — the fast lane has no path that triggers
that gate; assessed low-risk instead and routed to the already-open
`proposals.md` mechanism-level entry rather than blocking this ticket on
it), then opened `aiorders-api` PR #11 and raised this request. The P1 this
ticket exists for — onboarded restaurants silently invisible in marketplace
search — is resolved once this PR merges.

## 2026-09-03 — decision (ENG-021 G1): approved — `awaiting-scope → designed`

`decision` event pass, context `inbox/2026-09-03-eng021-g1-scope.md`.
Reading map for `decision`: steps 4 and 8c, plus step 6 (this answer
advances the ticket into a machine-owned state) and the not-negotiable set
(step 1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four lanes*,
*Guards*). Mode check clean (repo-root `.env` → `MODE=active`).

**Not a single continuous pass — resumed after a mid-pass rate-limit
crash.** This event's first attempt (`traces/eng-loop-2026-09-03.log`,
`pass FAILED (exit 1, 379s)`, re-queued, then several `pass NEVER STARTED`
rate-limit refunds) wrote `ENG-021`'s own board-file frontmatter/log update
— including prose narrating the journal entry, the PRD update, the gate
item's move to `inbox/_handled/`, and the `continue ENG-021` chain-fire as
already done — then hit the session's rate limit before any of those four
things actually happened. This pass verified every claim in that narration
against the underlying files (all accurate as a description of what should
happen, none yet true) before trusting it, then completed exactly the gap:
journal entry, PRD, gate-item move, this board index, and the actual
chain-fire below. The decision itself was not re-derived. Full account on
`ENG-021`'s own board-file log (addendum) and `observations.md`. Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-021`) and whole-board: both exit 0,
clean (re-run fresh by this resumption, not assumed from the crashed
attempt's own unverified claim).

**The answer:** `approved` (`decided: 2026-09-03T15:54:34.623417+00:00`).
No additional comment. Read as accepting the recommendation exactly as
scoped — customer questions surfaced on the brand portal plus a
self-service FAQ editor writing the same `restaurant_website.faqs` table
the bot already reads from; scoring answer quality, clustering questions, a
staff-facing admin-hub mirror, and any change to the chat bar's own runtime
behavior all named as later, separate work — and as accepting every item in
the readback's "Assumed, correctable here" list since none was corrected.
Full reasoning on `ENG-021`'s own board file, not repeated here.

`ENG-021` moved `awaiting-scope → designed`, `owner: approver →
architect`. PRD `status: approved`
(`agents/product-manager/specs/ENG-021-chat-bar-engagement-and-faq-self-service.md`).
Journaled (`decision-journal.md`). Gate item's `## Decision` footer already
carried the answer; appended a processed note and moved the file
`inbox/2026-09-03-eng021-g1-scope.md` →
`inbox/_handled/2026-09-03-eng021-g1-scope.md`.

**Risks named in the PRD stay open, inherited by the architect at
`designed`, not resolved by this approval:** PII in free-text customer
questions (the owner is arguably the right custodian of their own
customers' data, but the security gate should look at this plainly rather
than it being an accident of shipping a log viewer); RLS on
`restaurant_website` assumed from a sibling page's (`hiring`) behavior, not
read literally — confirm the actual policy before relying on it; retention
window and per-restaurant query volume both unknown, worth a quick check at
design time rather than a guess here. Restated here so the `continue
ENG-021` hop below doesn't have to re-derive them from the PRD alone.

Machine WIP re-checked fresh from every ticket's own frontmatter, not the
cached header: still `1/1`, occupied by `ENG-024` (`ready-to-ship`, not yet
`shipped`) — irrelevant to this transition, since `designed` sits outside
the counted `ready`..`ready-to-ship` range and shaping/design work is
backlog grooming regardless of who holds the slot. Handed to the architect
for the tech design itself (a `continue ENG-021` session) rather than
attempted inline, same precedent `ENG-020`'s, `ENG-019`'s, `ENG-026`'s and
`ENG-016`'s identical G1-approved hand-offs already set.

**1 transition** (`awaiting-scope → designed`), well under the cap of 4.
**Consequence:** approver-facing WIP drops by one item, down to seven — this
G1 drops off the "Waiting on the approver" list, same shape `ENG-013`'s,
`ENG-016`'s, `ENG-026`'s, `ENG-019`'s and `ENG-020`'s closures already set.
Machine WIP unaffected (`designed` sits outside the counted range).

**Dead-end sweep (scoped to this event):** no other ticket touched, per
this event's own narrower contract (act on the answered gate item, advance
only the ticket it belongs to). The recovered crash itself is the one
dead-end this pass exists to close — see the resumption note above.

**Notify sweep:** nothing raised this pass — no new gate item written.
`ENG-010`'s L1 merge request (`inbox/2026-09-02-eng010-merge-request.md`)
crossed 24h unanswered during this pass (notified 2026-09-02T17:45:02,
checked fresh at 2026-09-03T17:46:05) — nudged
(`lib/eng-notify.sh nudge`, exit 0), `nudged: 2026-09-03T17:46:05` stamped.
Every other open item checked and still under threshold or already
one-time-nudged: `ENG-008` (~18h21m), `ENG-015` (~7h42m), `ENG-022`
(~16h19m), `ENG-028` (~1h36m) all under 24h; `ENG-009` already carries its
one-ever nudge; `ENG-027` carries `decision: changed` (a separate ticket's
answered gate, not this event's to process — see the dead-end sweep note
above).

**Observations/proposals filed:** one observation
(`agents/eng-manager/observations.md`) on the crash-and-resume itself — the
first attempt's narration described completed work before it was true,
which would have been indistinguishable from a genuine done state had this
event never been resumed.

**Board update** — In-flight table's `ENG-021` row (`state`, `owner`,
`priority` synced to the ticket's own frontmatter, `updated` date); header's
approver-facing bullet, "unanswered items" paragraph and count, "Waiting on
the approver" section's `ENG-021` paragraph, its stale `ENG-010`
"not yet due for a nudge" text, and item count. Rolled the oldest of the
four now-live dated entries (`decision (ENG-026 G1)`) to
`_index-archive.md` per the keep-three rule. `inbox/2026-09-02-eng010-merge-request.md`'s
own `nudged:` frontmatter stamped separately from this file.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-021`) and whole-board: both
exit 0, clean.

`chained: ENG-021` — `designed` is agent-owned (`architect`, via
`tech-design/SKILL.md`, triggered by this exact state); not the approver,
not blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-021` —
confirmed landed in `traces/.pending` (this pass itself holds the lock, so
the trigger queued it rather than launching immediately; the next drain
after this pass exits runs it), not just assumed from the command's silent
exit.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-024 (release-readiness): `ready-to-ship → blocked`

`continue` event pass, context `ENG-024` — this fire's own turn at the front
of the queue, per the prior (`principal-engineer`) pass's own `chained:
ENG-024`. Narrow scope per the event's own contract — this ticket only.
Reading map for `continue`: steps 6 and 6b. Mode check clean (business-os
`.env` → `MODE=active`; instance `config/config.yaml` → `mode:` empty).
Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-024`) and whole-board: both
exit 0, clean.

**Closed a stale incident before starting the ticket work**, found only
because the reading map's own floor-not-ceiling clause covers exactly this
shape: `inbox/2026-09-03-eng-loop-stalled.md` (raised 06:37:12, named
`ENG-024`, never investigated). Classified directly from
`traces/eng-loop-2026-09-03.log`: every `NEVER STARTED` line in that run
carries the `vendor limit signature` text, and the same log shows the
back-off clearing on its own at 08:56:01 followed by eleven further clean
passes since. Resolved, moved to `inbox/_handled/`; full reasoning on the
file itself. Also checked (not acted on): `ENG-027`'s G1 carries `decision:
changed` while this index's own prior text still described it as an open
rider — corrected the stale text below, but confirmed `traces/.pending`
already carries its own queued `decision` event, so nothing was actually
stuck.

Verified all upstream gates fresh from `agents/principal-engineer/reviews/ENG-024.md`
(`verdict: pass`). Project L1 (`config/projects.md`) — window check n/a.
Readiness checks (rollback reasoned/not-drilled per the same standing host
limitation `ENG-007` already established precedent for; observability
unchanged/adequate; cost $0/month) all clear. One gap decided rather than
silently passed: no dedicated `database`-gate verdict exists for the
backfill migration (fast lane has no path that triggers it) — read
`release-runner/SKILL.md` step 2 as requiring an existing gate to return to,
not authority to invent one this lane has no slot for; independently
re-read the migration SQL, concurred with the review's low-risk assessment,
and named the gap plainly rather than writing `pass`. Full reasoning:
`ENG-024`'s own board-file log.

Opened `aiorders-api` PR #11, wrote the L1 merge request
(`inbox/2026-09-03-eng024-merge-request.md`), notified
(`lib/eng-notify.sh raise`, exit 0). State `ready-to-ship → blocked`,
`blocked_on: approver`, `blocked_from: ready-to-ship`, owner `devops →
approver`. No release record yet — written once merge detection confirms
the PR merged, same position `ENG-008`/`ENG-009`/`ENG-010`/`ENG-022` are
already in.

**1 transition** (`ready-to-ship → blocked`). **Consequence:** machine WIP
`1/1 → 0/1`, freed (not filled this pass — narrow scope). Approver-facing
WIP uncapped; this item adds to the informational count only.

**Dead-end sweep (scoped to this event):** the stale incident above is the
one dead-end this hop found and closed; nothing else on this ticket's own
lineage. **Notify sweep:** this pass's own item raised and stamped; every
other open item checked fresh and under its own threshold or already
one-time-nudged (full detail on `ENG-024`'s own board-file log).
**Observations/proposals filed:** none new — the migration-verdict gap and
the rollback-testing host limitation are both already-open proposals; this
hop applies them, it doesn't discover them fresh.

**Board update** — In-flight table's `ENG-024` row (`state`, `owner`);
header's Machine WIP paragraph and approver-facing bullet list (`ENG-024`
added); "unanswered items" paragraph, count, and `ENG-027`'s stale
characterization corrected; "Waiting on the approver" section's count and
new `ENG-024` paragraph. Rolled the oldest of the four now-live dated
entries (`decision (ENG-019 G1)`) to `_index-archive.md` per the
keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-024`) and whole-board: see
below.

`chained: none` — `blocked`, `blocked_on: approver`. This is the human gate
the whole hop was driving toward; firing `continue ENG-024` again would
queue against a ticket with nothing left for a machine to do, same reasoning
`ENG-008`'s and `ENG-022`'s own release-readiness entries already recorded
at this identical state.

business-os itself left uncommitted — same standing default every pass has
used, including this ticket's own incident-closure move; the
commit-convention question remains open, not re-decided here.

## 2026-09-03 — decision (ENG-027 G1): changed — rescoped in place, fresh G1 raised

`decision` event pass, context `inbox/2026-09-03-eng027-g1-scope.md`.
Reading map for `decision`: steps 4 and 8c, plus step 6 checked and found
not to apply (a `changed` answer is not one of the three G1 outcomes —
approved, changed, killed — that hands the ticket to the EM; only
`approved` does), plus the not-negotiable set (step 1, 7, 8b, 9, 10;
*Enforced vs instructed*, *The four lanes*, *Guards*). Mode check clean
(repo-root `.env` → `MODE=active`; instance `config/config.yaml` →
`mode:` empty). Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-027`) and
whole-board: both exit 0, clean.

**The answer:** `changed` (`decided: 2026-09-03T16:00:32.878229+00:00`),
in full: *"Accrual at fulfillment, have ticket completed as autocompleted
after x hours if not cancelled or deleted."* Two clauses — the first takes
the fork the first G1 named explicitly ("if you want accrual on fulfilment
instead, that signal has to be built first and this ticket goes from `M`
to `L`"), the second supplies the approver's own mechanism for the missing
signal. Same shape `ENG-016`'s rescope was: a real scope change, not an
edit and not a rejection, so the ticket goes back to the approver rather
than advancing to the EM.

Delegated the rescope to an `opus` subagent per `prd-writer/SKILL.md`'s
own model designation, pointed at the `ENG-016` rescope precedent for
structure/tone. Independently re-verified its central, most load-bearing
claim myself before trusting it (`cloudwaitress-middleware/handlers/
restaurant.ts` line 6, `AIORDERS_WEBHOOK.events`; `handleAddWebhook()`
line 93) rather than taking a subagent's report of a fact this consequential
at face value — confirmed accurate.

**What the rescope found: this department's own first G1 on this ticket
was wrong.** It read "the webhook handler discards every event except
`order_new`" as "no completion signal exists." Re-checked against live
`aiorders-api` code: AIOrders' own webhook registration already subscribes
to `order_completed_updated`, `order_cancelled_updated`, `order_cancel`
and `order_update_status`, delivered to production and thrown away at
`external-integrations/handlers/cloudwaitress.ts` line 238. The fulfilment
signal doesn't need building — it needs un-ignoring. Separately, the
approver's own condition ("if not cancelled or deleted") is **vacuous**
against the current code: nothing anywhere updates or deletes an order row
(zero `.update(`/`.delete(` calls against `orders` in the whole repo), so
a timer-only sweep with no cancellation fix would credit every order,
X hours after placement, no exceptions — named plainly on the fresh G1
rather than built and reported as satisfying the clause. "Deleted" has no
signal at all and can't be built as stated. Full evidence, all re-cited
with file/line references: `ENG-027`'s own board-file log,
`agents/product-manager/specs/ENG-027-loyalty-points-ledger-and-earn.md`
(new `## Approver's` `changed` `response` section), and the fresh G1
itself.

**Sizing re-derived, not inherited either direction:** `L` (was `M`), and
deliberately not the old G1's own `M → L` warning's reasoning either —
that warning priced building a signal that turns out to already exist.
What earns the `L` on its own re-derived merits: the first
write-after-insert path on `orders` in this codebase's history, on the
live production order webhook; a scheduled sweep with its own idempotency
and failure semantics; and moving the accrual trigger point, where
double-crediting bugs live. Not `XL` — one project, one new data model,
no cross-repo surface — so it proceeds whole rather than going back to be
split the way `ENG-016`'s full rewrite did.

**Four riders carried on the fresh G1**, up from the first G1's one: a
concrete number for the "x hours" placeholder (proposed 24h, with the
shipped feedback queue's own 3-hour delay named as the same-day
alternative); the first G1's earn-% base rider, **carried forward as
still open** since the `changed` answer never addressed it and silence is
never read as approval; which moment's rate applies now that placement
and accrual are hours apart (proposed: placement); and whether the
order's own `status` column becomes the completion signal (proposed:
yes — it also fixes a frozen status `brand-portal` currently shows
restaurant owners).

PRD rescoped in place (`agents/product-manager/specs/ENG-027-loyalty-
points-ledger-and-earn.md`) — original placement-based content marked
superseded rather than deleted, per `ENG-016`'s own precedent for this
exact situation. Acceptance criteria 11 → 18 (criteria 1, 6 and 9
re-derived for the new trigger; criterion 2, dine-in, untouched since
dine-in has no fulfilment step). Fresh G1 written:
`inbox/2026-09-03-eng027-g1-rescope.md`. Old G1 moved to
`inbox/_handled/2026-09-03-eng027-g1-scope.md` as-is, no appended note —
same precedent, the narrative lives in the PRD section, the fresh G1, and
the journal row instead. Decision-journal row appended for the `changed`
verdict (`decision-journal.md`) — first entry on this board naming a
`changed` answer that made a ticket *cheaper* to get right than the G1
that prompted it, by being wrong in the approver's favour.

**No dissent section** — `agents/critic/agent.md` still doesn't exist at
department or instance level, same gap this ticket's first G1 already
recorded; not refiled, the open proposal (`proposals.md`, 2026-08-25 row)
already covers it.

**0 transitions** — `awaiting-scope → awaiting-scope`, `owner: approver`
throughout; a `changed` answer is processed, not advanced. Machine WIP
unaffected (`awaiting-scope` sits outside the counted range).
Approver-facing WIP unchanged at eight — the same item returns to the same
desk under a fresh G1, not a new one.

**Notify sweep:** this pass's own gate item raised —
`lib/eng-notify.sh raise inbox/2026-09-03-eng027-g1-rescope.md`, exit 0,
confirmed in `traces/eng-notify-2026-09-03.log` (`13:15:26 sent`);
`notified: 2026-09-03T13:15:26` stamped. Nothing else nudged or due this
pass — out of this event's own narrow scope regardless (act on the
answered gate item, advance only the ticket it belongs to).
**Observations/proposals filed:** none new.

**Board update** — header's Machine-WIP-section `ENG-027` bullet
(rewritten to describe the rescope rather than the original filing);
"eight items" paragraph (`ENG-027` now a plain unanswered fresh G1, not
"already answered, not yet processed"); In-flight table's `ENG-027` row
(`size` `M → L`); "Waiting on the approver" section's `ENG-027` paragraph
(split into "first G1" / "fresh G1" to keep both decisions legible).
Rolled the oldest of the four now-live dated entries (`decision (ENG-020
G1)`) to `_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-027`) and whole-board: both
exit 0, clean.

`chained: none` — `awaiting-scope`, owner `approver`. The fresh G1 just
raised is a new item waiting on the approver, not an agent-owned state;
firing `continue ENG-027` would queue against a ticket with nothing left
for a machine to do until it's answered.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

