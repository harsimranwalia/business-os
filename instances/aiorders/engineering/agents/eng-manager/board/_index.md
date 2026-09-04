# Board

**Next ID: ENG-037** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.) `ENG-036` allocated this pass
— an architect-filed P0, byproduct of `ENG-035`'s own design work, itself a
byproduct of `ENG-029`'s — In-flight row and this counter both updated in
the same edit as the ticket was filed, not left for a later sweep to find
missing (the gap `ENG-035`'s own allocation hit last pass).

**Machine WIP 1** (`config/config.yaml` → `wip.machine_limit`). **Corrected
2026-08-29 — the approver's direct instruction: one ticket completed end to
end (through `shipped`) before the next one starts, not several tickets each
advanced by one shallow step per pass.** This was 12 (the `max_5x` tier value)
earlier the same day; see that file for the full rationale.

**Currently 1/1 — occupied by the `ENG-016` family.** `ENG-016` ran
work-breakdown this pass (`ready → building`, no diff of its own from here —
see its own `## Breakdown` section) and decomposed into four sub-tickets,
`ENG-031`..`034`, one per surface, sequenced by dependency. **First
work-breakdown on this board**, and the read taken: the WIP slot is held by
the ticket *family* (parent plus its `parent:`-linked children), not by each
row in `ready..ready-to-ship` separately — otherwise dispatching even one
child would read as a second occupant of a 1-wide cap, and work-breakdown
could never run at all. Full reasoning, flagged as an observation for
review since it's a first-precedent call:
`agents/eng-manager/notebook/2026-09-03-eng016-work-breakdown.md`. `ENG-031`
(database, no dependency) reached `verified` — its PR merged directly on
GitHub, found by an earlier pass tonight's own step-5 merge detection (no
written reply on its merge request); see its own board-file log and
`agents/devops/releases/2026-09-03-aiorders-api-ENG-031.md`. That satisfied
`ENG-032`'s sole dependency (`depends_on: [ENG-031]`); that pass chained
`continue ENG-032`, and the dedicated session it fired moved `ENG-032`
`ready → building` and on through review/quality/security/release-readiness
to a merge request. **This `scheduled` sweep's own step-5 merge detection
now finds `ENG-032` merged too** — `restaurant-portal` PR #2, no written
reply — and, receipts re-verified fresh, carried it `blocked → shipped →
verified` this pass; see its own board-file log and
`agents/devops/releases/2026-09-03-restaurant-portal-ENG-032.md`. That
satisfies `ENG-033`'s last unmet dependency (`depends_on: [ENG-031,
ENG-032]`, both now `verified`) — this pass fired `continue ENG-033` rather
than building it inline (new implementation work stays out of a `scheduled`
sweep), same handoff shape `ENG-031`'s own shipping pass used for `ENG-032`.
**This `watch (launchd)` event pass's own step-5 re-check — not the next
`scheduled` sweep — now finds `ENG-033` merged too**, about 15 minutes
after the fact: `aiorders-api` PR #13, no written reply, base `main`
directly (no stacking) — and, receipts re-verified fresh, carried it
`blocked → shipped → verified` this pass; see its own board-file log and
`agents/devops/releases/2026-09-04-aiorders-api-ENG-033.md`. That satisfies
`ENG-034`'s sole dependency (`depends_on: [ENG-033]`) — this pass fired
`continue ENG-034` rather than building it inline, same handoff shape
`ENG-031`'s and `ENG-032`'s own shipping passes already used, and the last
hop in this family's own sequenced chain. `ENG-014`, `ENG-017`,
`ENG-023`, `ENG-025`, `ENG-026`, `ENG-019`, `ENG-020`, and `ENG-021` (all
`designed` with a completed design and no one-way door) are not candidates
for a fresh slot until the whole `ENG-016` family reaches `shipped` —
`ENG-018` stays excluded outright (`priority: hold`). **`ENG-021`'s own
`depends_on: [ENG-022]`** (set 2026-09-03 — the design edits
`brand-portal/website.ts`, whose ownership check `ENG-022`, P0, fixed and
whose branch touched the same file) **is now satisfied** — `ENG-022`
shipped and reached `verified` in an earlier pass tonight, checked fresh
against this ticket's own frontmatter this pass, not assumed from this
paragraph's own stale wording (which still read "unmerged" until this
edit). The machine-WIP cap is `ENG-021`'s sole remaining hold now: once a
slot frees, this ticket is a candidate like its siblings, no second
condition left to clear.

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
  unanswered) once both PRs reflected the corrected diff. **Both repos now
  found merged directly on GitHub** — `aiorders-admin-hub` PR #5 found two
  sweeps ago; **this `scheduled` pass's own step-5 merge detection found
  `aiorders-api` PR #6 also merged**, roughly 3.5 hours before the first
  sweep to check reported it "not merged" (branch-tip contamination from
  `ENG-009`/`ENG-010` stacking on the same branch name — full mechanics on
  the ticket's own board-file log and a new `proposals.md` row). Receipts
  re-verified fresh, carried `blocked → shipped → verified` this pass.
  **Off this count and off the board entirely (terminal)** — see the
  closing paragraph below and its own board file.
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
  (`inbox/2026-09-02-eng009-merge-request.md`). Both PRs later found merged
  into a stacked sibling branch rather than `main` (see the closing
  paragraph below) — not shipped by that alone. **A later `watch (launchd)`
  event pass found a fresh consolidating PR on each repo, merged straight to
  `main`, actually shipped it.** Carried `blocked → shipped → verified` in
  that pass. **Off this count and off the board entirely (terminal)** — see
  the closing paragraph below and its own board file.
- `ENG-010` — same shape, same fresh-consolidating-PR resolution, same pass
  (`inbox/_handled/2026-09-02-eng010-merge-request.md`). Carried
  `blocked → shipped → verified` alongside `ENG-009` — one action, both
  repos, both tickets. **Off this count and off the board entirely
  (terminal)** — see the closing paragraph below and its own board file.
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
- `ENG-022` — P0 cross-tenant PII/write exposure; all gates passed, PR #9
  opened, L1 merge request raised — then this `scheduled` sweep's own step-5
  merge detection found the PR merged directly on GitHub, no written reply
  ever given. Receipts re-verified fresh before advancing (step 5's own "a
  merge is not a gate" clause): review/quality/security all `pass`, no
  migration, fix independently re-confirmed on the merged tree. Carried
  `blocked → shipped → verified` this pass — release record:
  `agents/devops/releases/2026-09-03-aiorders-api-ENG-022.md`. **Off this
  count and off the board entirely (terminal)** — see the closing paragraph
  below and its own board file.
- `ENG-015` — code review (round 2), quality, security, and migration all
  passed; devops's own release-readiness hop found both projects L1,
  confirmed rollback/observability/cost all clear, then opened both PRs
  (`aiorders-api` #10, `aiorders-admin-hub` #8) and raised a single L1 merge
  request covering both (`inbox/2026-09-03-eng015-merge-request.md`) — then
  this `scheduled` sweep's own step-5 merge detection found both PRs merged
  directly on GitHub, no written reply, 32 seconds apart, in the same
  batch-merge session as `ENG-013`'s own two PRs below. Receipts
  re-verified fresh (review/quality/security all `pass`), no migration
  drift, both fixes independently re-confirmed on the merged tree. Carried
  `blocked → shipped → verified` this pass — release record:
  `agents/devops/releases/2026-09-04-ENG-015-aiorders-api-and-admin-hub.md`.
  **Off this count and off the board entirely (terminal)** — see the
  closing paragraph below and its own board file.
- `ENG-032` — code review (round 2), quality, and security all passed;
  devops's own release-readiness hop found the project L1, opened
  `restaurant-portal` PR #2 and raised a fresh L1 merge request
  (`inbox/2026-09-03-eng032-merge-request.md`) — then this `scheduled`
  sweep's own step-5 merge detection found the PR merged directly on
  GitHub, no written reply ever given. Receipts re-verified fresh
  (review/quality/security all `pass`), no migration owed, the two new
  stages/itemized block/`orderFormEnabled` switch independently re-confirmed
  on the merged tree. Carried `blocked → shipped → verified` this pass —
  release record `agents/devops/releases/2026-09-03-restaurant-portal-ENG-032.md`.
  **Off this count and off the board entirely (terminal)** — see the closing
  paragraph below and its own board file. Its shipping satisfies `ENG-033`'s
  last unmet dependency; see that ticket's own board-file log for this
  pass's dispatch.
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

Two items genuinely on the approver's plate right now, all unanswered:
`ENG-027` (fresh G1 raised — the first G1's `changed` answer
was processed and the ticket rescoped `M → L`; see the header bullet above
and the ticket's own board-file log for the full reasoning), `ENG-028`
(new G1). No cap on how many of
these may be open at once — see header above; nothing here gates a new
start. `ENG-015`'s own merge request is gone from this list —
this pass's own step-5 merge detection found both of its PRs already merged
directly on GitHub, no written reply; see the header bullet above and the
closing paragraph below. **`ENG-009`, `ENG-010` and `ENG-033` are gone from
this list too, off the board entirely (terminal)** — a later `watch
(launchd)` event pass's own step-5 re-check found `ENG-033`'s PR merged
directly to `main`, and a fresh consolidating PR on each repo finally
shipped `ENG-009`/`ENG-010` past the stacked-branch snag named on their own
rows below; see the header bullet above and the closing paragraph below.
**`ENG-013`, `ENG-016`, `ENG-026`, `ENG-019`, `ENG-020` and `ENG-021`
drop off this list, not off the board** —
`ENG-013`'s scope question closed with no new written item, same shape
`ENG-007`/`ENG-011` once had: `blocked`, `blocked_on: approver`, two open
PRs, nothing in `inbox/` left to answer. `ENG-016`'s rescope G1, `ENG-026`'s
G1, `ENG-019`'s G1, `ENG-020`'s G1 and `ENG-021`'s G1 were all answered
**approved** and moved to `designed`/`architect` — see the header bullets
above. **`ENG-013` no longer needs that GitHub merge watched for** — this
same `scheduled` pass's own step-5 merge detection found both of its PRs
already merged, no written reply; see below. **`ENG-024` and `ENG-031`
drop off this list *and* off the board — both terminal.** An earlier pass
tonight's own step-5 merge detection found both PRs (`aiorders-api` #11 and
#12) merged directly on GitHub, with no written reply to either
merge-request item; both carried `blocked → shipped → verified` in that
pass. **`ENG-022` and now `ENG-032` join them** — this `scheduled` pass's
own step-5 merge detection found `aiorders-api` PR #9 (`ENG-022`) merged
earlier in the same sweep, then `restaurant-portal` PR #2 (`ENG-032`) merged
too, both with no written reply; both carried `blocked → shipped → verified`
this pass. **`ENG-013` and `ENG-015` join them too, same pass** — the same
step-5 merge detection also found all four of their PRs (`aiorders-api`
#5/#10, `aiorders-admin-hub` #4/#8) merged directly on GitHub, no written
reply, all four landing within roughly 90 seconds of each other — one
batch merge session covering four PRs across two unrelated tickets. Both
carried `blocked → shipped → verified` this pass. **`ENG-008` drops off
this list too, joining the terminal group, but from a later `scheduled`
pass** — this pass's own step-5 re-derivation (not the same sweep as the
`ENG-013`/`ENG-015`/`ENG-022`/`ENG-032` batch above) found `aiorders-api`
PR #6 also merged, roughly 3.5 hours after the fact; three sweeps in
between had wrongly reported it unmerged due to branch-tip contamination
from `ENG-009`/`ENG-010` stacking on the same branch name. Carried
`blocked → shipped → verified` this same pass. `ENG-009`'s and `ENG-010`'s
own PRs also show `MERGED` on GitHub now, but into that same stacked
branch rather than `main` — neither actually shipped; both stay on this
list, `blocked`, with their merge-request items amended in place to
explain what's actually still needed. See the closing paragraph below and
each ticket's own board file.

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
| ENG-014 | Brand portal self-service — restaurant QR codes and marketing media downloads | restaurant-portal | designed | | eng-manager | M | 2026-08-31 |
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
| ENG-016 | Catering page — self-serve quote generator, with automatic stage update (rescoped to Piece 1: order capture + stage automation, no pricing) — parent, decomposed into ENG-031..034 | config-site-builder | building | next | eng-manager | L | 2026-09-03 |
| ENG-034 | Public catering form — category-grouped dish picker, gated by owner opt-in | config-site-builder | building | | frontend | M | 2026-09-04 |
| ENG-017 | Autopilot nurture for the presignup sales lead pipeline — stage-triggered email/SMS | aiorders-api | designed | | architect | L | 2026-09-01 |
| ENG-018 | Sales demonstration account — a fully seeded AIOrders environment to show prospects | aiorders-admin-hub | shaped | hold | product-manager | L | 2026-09-03 |
| ENG-019 | Restaurant self-service marketing broadcasts — mass send and drip sequences, scheduled or immediate | restaurant-portal | designed | now | architect | L | 2026-09-03 |
| ENG-020 | Marketing ROI reporting — traffic source and revenue attribution on the brand dashboard | restaurant-portal | designed | now | architect | M | 2026-09-03 |
| ENG-021 | Website chat-bar engagement visibility — customer questions and self-service FAQ editing on the brand portal | restaurant-portal | designed | now | architect | M | 2026-09-03 |
| ENG-023 | Add status and internal notes to each brand-portal feedback item | restaurant-portal | designed | | architect | S | 2026-08-31 |
| ENG-025 | Recurring feedback issues, per restaurant, over time | restaurant-portal | designed | | eng-manager | S | 2026-08-31 |
| ENG-026 | FoodSwipe channel-visibility toggles and capability-based discovery | restaurant-marketplace | designed | now | architect | M | 2026-09-03 |
| ENG-027 | Loyalty points ledger, balances, and earn API — online-order and dine-in accrual | aiorders-api | awaiting-scope | now | approver | L | 2026-09-03 |
| ENG-028 | Foodswipe funnel — staff-configurable pipeline stage set | aiorders-admin-hub | awaiting-scope | | approver | L | 2026-09-03 |
| ENG-029 | Autopilot API has no restaurant-ownership check on any of its 8 actions — cross-tenant customer-data exposure | aiorders-api | designed | | architect | M | 2026-09-04 |
| ENG-030 | `analytics` edge function has no authentication or authorization at all — cross-tenant revenue/order/customer exposure | aiorders-api | designed | | architect | S | 2026-09-03 |
| ENG-035 | `autopilot`'s system-triggered marketing actions skip authentication entirely — client-controlled flag reaches a real message-send trigger | aiorders-api | designed | | architect | S | 2026-09-04 |
| ENG-036 | `outgoing-communications` skips authentication entirely for any system-triggered send — cross-actor unauthenticated message dispatch | aiorders-api | designed | | architect | S | 2026-09-04 |

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
`ENG-024` — `aiorders-api` PR #11 found merged directly on GitHub by this
02:00 `scheduled` sweep's own step-5 merge detection, no written reply to
its merge request; carried `blocked → shipped → verified` this pass — off
the In-flight table (terminal); see its own board file and
`agents/devops/releases/2026-09-03-aiorders-api-ENG-024.md`. `ENG-031` —
same sweep, same shape: `aiorders-api` PR #12 found merged directly on
GitHub, no written reply, carried `blocked → shipped → verified` — off the
In-flight table (terminal); see its own board file and
`agents/devops/releases/2026-09-03-aiorders-api-ENG-031.md`. Its shipping
satisfies `ENG-032`'s sole dependency; that ticket stayed `ready` with
`chained: ENG-032` fired this pass, and the dedicated session it fired has
since moved it to `building` (In-flight table). `ENG-022` — this
`scheduled` sweep's own step-5 merge detection (this pass) found
`aiorders-api` PR #9 merged directly on GitHub, no written reply to its
merge request; all three gate receipts (review/quality/security) re-read
fresh and confirmed `pass`, no migration owed, fix independently
re-verified on the merged tree before advancing — carried
`blocked → shipped → verified` this pass — off the In-flight table
(terminal); see its own board file and
`agents/devops/releases/2026-09-03-aiorders-api-ENG-022.md`. **`ENG-032`
joins it, same pass** — this sweep's own step-5 merge detection also found
`restaurant-portal` PR #2 merged directly on GitHub, no written reply to its
merge request; review/quality/security receipts re-read fresh and confirmed
`pass`, no migration owed, the shipped diff independently re-verified on the
merged tree — carried `blocked → shipped → verified` this pass — off the
In-flight table (terminal); see its own board file and
`agents/devops/releases/2026-09-03-restaurant-portal-ENG-032.md`. Its
shipping satisfies `ENG-033`'s last unmet dependency
(`depends_on: [ENG-031, ENG-032]`, both now `verified`); the dedicated
session that pass's own `chained: ENG-033` fired has since moved it to
`building` (In-flight table) — see that ticket's own board-file log.
**`ENG-013` and `ENG-015` join them too, same pass** — this sweep's own
step-5 merge detection found all four of their PRs (`aiorders-api` #5/#10,
`aiorders-admin-hub` #4/#8) merged directly on GitHub, no written reply to
either, all four landing within roughly 90 seconds of `ENG-022`'s and
`ENG-032`'s own merges above — one batch merge session covering six
tickets' worth of PRs tonight. Both tickets' four gate receipts (migration/
review/quality/security) re-read fresh and confirmed `pass`; both fixes
independently re-verified on the merged tree before advancing — both
carried `blocked → shipped → verified` this pass — off the In-flight table
(terminal); see each ticket's own board file and
`agents/devops/releases/2026-09-04-ENG-013-aiorders-api-and-admin-hub.md` /
`agents/devops/releases/2026-09-04-ENG-015-aiorders-api-and-admin-hub.md`.
`ENG-013`'s shipping satisfies `ENG-028`'s sole dependency
(`depends_on: [ENG-013]`); `ENG-028` itself stays `awaiting-scope`,
unaffected in state, since its own G1 is still unanswered.

**`ENG-008` joins the terminal group too, from a later `scheduled` pass
the same morning.** Its `aiorders-admin-hub` side (PR #5) was found merged
several sweeps earlier; this pass's own step-5 re-derivation found
`aiorders-api` PR #6 also merged (`bd67e86`, 2026-09-04T06:04:41Z) — three
sweeps in between had wrongly read it as unmerged, because the naive
branch-tip check (`git merge-base --is-ancestor
origin/feat/ENG-008-influencer-admin-management origin/main`) gets
contaminated once a downstream ticket stacks on the same branch name and
keeps merging into it after the branch's own PR already shipped
separately — exactly what `ENG-009` and `ENG-010` did to this branch.
Checking the ticket's own recorded commit (frontmatter `branch:`, already
known) instead of the live branch tip resolved it. All three gate receipts
re-read fresh and confirmed `pass` against the shipped diff; carried
`blocked → shipped → verified` — off the In-flight table (terminal); see
its own board file and
`agents/devops/releases/2026-09-04-ENG-008-aiorders-api-and-admin-hub.md`.

**`ENG-033` joins the terminal group too, found by a later `watch
(launchd)` event pass's own step-5 re-check.** `aiorders-api` PR #13
merged directly to `main`, no stacking, no written reply, about 15 minutes
before that pass ran. All three gate receipts re-read fresh and confirmed
`pass`; no migration owed. Carried `blocked → shipped → verified` — off the
In-flight table (terminal); see its own board file and
`agents/devops/releases/2026-09-04-aiorders-api-ENG-033.md`. Its shipping
satisfies `ENG-034`'s sole dependency (`depends_on: [ENG-033]`, the last
`ENG-016` sub-ticket) — `continue ENG-034` fired that same pass rather than
building it inline.

**The mirror-image finding: `ENG-009`'s and `ENG-010`'s own PRs also show
`MERGED` on GitHub, but neither shipped.** Both merged into
`feat/ENG-008-influencer-admin-management` — their own configured stacked
base — which had already shipped separately by the time they merged into
it, so their commits are stranded on a branch nothing further merges to
`main`. Confirmed by content, not just ancestry: neither ticket's
distinguishing code appears anywhere in either repo's `main`. The specific
regression `ENG-008`'s own round-3 review once warned `ENG-009` risked
(reintroducing the rejected `accepts_barter` column) did **not**
materialize — the merged branch carries the correct code — but both
tickets stay `blocked`: there is no longer an open PR anywhere targeting
`main` that carries either ticket's changes. Both merge-request items
amended in place with a plain-language explanation; both ticket logs carry
the full finding; a new `proposals.md` row names the general mechanism gap
(a stacked PR's merge can satisfy GitHub's UI without the code ever
reaching the default branch) so it's caught mechanically next time rather
than by chance, as it was here.

**Resolved by the same later `watch (launchd)` event pass that caught
`ENG-033` above.** A fresh consolidating PR on each repo
(`merge/ENG-009-ENG-010-to-main`, `aiorders-api` #14, `aiorders-admin-hub`
#9), base `main`, head the stacked branch's own tip, was opened and merged
directly on GitHub within a minute of each other — the "fresh PR from the
current stacked-branch tip" option the paragraph above and each ticket's
own board log had left as an open, unresolved question, taken by hand by
the approver. Both tickets' commits landed together, one action per repo.
Receipts re-verified fresh, all `pass`, no migration either side; both
carried `blocked → shipped → verified` — off the In-flight table
(terminal); see each ticket's own board file and the combined release
record
`agents/devops/releases/2026-09-04-ENG-009-ENG-010-aiorders-api-and-admin-hub.md`.
`blocks: []` on both — nothing further unblocked by this one.

## Waiting on the approver

**No cap — `wip.approver_limit: unlimited` since 2026-09-02 (see header
above). Two items currently open** (composition changed sharply this pass:
`ENG-008`, `ENG-009`, `ENG-010` and `ENG-033` all resolved between the prior
write of this section and now — `ENG-008` in an earlier `scheduled` sweep
the same morning, `ENG-009`/`ENG-010`/`ENG-033` in this `watch (launchd)`
event pass's own step-5 re-check; see each ticket's own paragraph below and
the closing paragraph),
listed here
for visibility, not because any number of them blocks a new start.
**`ENG-008`'s L1 merge request — resolved, terminal.** Its partial-merge
position (`aiorders-admin-hub` PR #5 merged, `aiorders-api` PR #6 still
open) recorded here earlier was superseded by a later `scheduled` sweep
finding PR #6 also merged (a ~3.5h detection gap traced to branch-tip
contamination from `ENG-009`/`ENG-010` stacking on this same branch, not a
new merge) — carried `blocked → shipped → verified` that pass. **Off this
list and off the board entirely (terminal)**, item now in
`inbox/_handled/2026-09-02-eng008-merge-request.md`; see the closing
paragraph below and its own board file.
**`ENG-009`'s and `ENG-010`'s L1 merge requests — resolved, terminal.**
Both originally raised stacked on `ENG-008`'s (then `ENG-009`'s own)
branch, not `main` — merging either PR alone was never going to ship them,
recorded in this section historically and on each ticket's own board-file
log. **This `watch (launchd)` event pass's own step-5 re-check found a
fresh consolidating PR on each repo** (`merge/ENG-009-ENG-010-to-main`,
`aiorders-api` #14, `aiorders-admin-hub` #9, base `main`, head the stacked
branch's own tip), merged directly on GitHub within the last few minutes —
carrying both tickets' commits together. Receipts re-verified fresh
(review/quality/security all `pass` on both), no migration owed either
side; carried `blocked → shipped → verified` this pass. **Off this list
and off the board entirely (terminal)**, both items now in
`inbox/_handled/`; see the closing paragraph below, each ticket's own board
file, and the combined release record
`agents/devops/releases/2026-09-04-ENG-009-ENG-010-aiorders-api-and-admin-hub.md`.
`ENG-013`'s
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
and `decision-journal.md`. **`ENG-015`'s L1
merge request** (`inbox/2026-09-03-eng015-merge-request.md`) — raised this
pass (~10:03): code review (round 2, after a round-1 fail on missing tests
plus a mass-assignment authz bug, both closed), quality, security, and
migration all passed; devops's own release-readiness hop found both
projects L1, confirmed rollback/observability/cost all clear, then opened
`aiorders-api` PR #10 and `aiorders-admin-hub` PR #8 and raised this single
two-repo request. The P1 this ticket exists for — a partner seeing/writing
every restaurant on the platform, and a broken add-location path — is
resolved once **both** PRs merge; they must land together, named explicitly
in both PR bodies and this request. **Resolved this same pass**: this
`scheduled` sweep's own step-5 merge detection found both PRs merged
directly on GitHub, no written reply, 32 seconds apart, confirming they
landed together as required — carried `blocked → shipped → verified`;
**off this list and off the board entirely (terminal)**, see the closing
paragraph below and its own board file. **`ENG-019`'s G1**
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
approved`, handed to the architect for the tech design. **`ENG-033`'s L1
merge request — resolved, terminal.** Raised 2026-09-04 (~01:43): code
review (round 4), quality (round 2), and security all passed;
release-readiness confirmed rollback/observability/cost all clear (L1, no
window check) and opened `aiorders-api` PR #13, carrying two non-blocking
security findings and a direct RLS-confirmation ask in its own "Named gaps"
section (visibility only, not a gate condition). **This `watch (launchd)`
event pass's own step-5 re-check found PR #13 merged directly to `main`**,
no written reply, about 15 minutes before this pass ran. Receipts
re-verified fresh, all `pass`, no migration owed; carried
`blocked → shipped → verified`. **Off this list and off the board entirely
(terminal)**, item now in `inbox/_handled/`; see the closing paragraph
below and its own board file
(`agents/devops/releases/2026-09-04-aiorders-api-ENG-033.md`). Unblocked
`ENG-034`, the last `ENG-016` sub-ticket — `continue ENG-034` fired this
same pass. **`ENG-028`'s G1**
(`inbox/2026-09-03-eng028-g1-scope.md`) — raised this pass (~16:10 UTC):
staff-configurable Foodswipe pipeline stage set, filed per the approver's
own **Reading A** on `ENG-013`'s stage-config question ("file
stage-taxonomy configuration as ENG-0XX, a new ticket, built on top of
this"); sized `L` (new data model, cross-project). Carries a rider on the
one assumption most worth correcting — that staff-defined stages are
manual-only, since no generic auto-classification mechanism exists in
`classifyStage()` today — and flags both that `ENG-022` (P0) outranks it
and that `ENG-013`'s two PRs should merge first — moot now, both merged
(below). `ENG-022`'s, `ENG-024`'s,
`ENG-031`'s, `ENG-032`'s and now `ENG-013`'s and `ENG-015`'s L1 merge
requests are no longer listed
here — step-5 merge detection (this pass, for `ENG-022`, `ENG-032`,
`ENG-013` and `ENG-015`; an
earlier pass tonight, for `ENG-024` and `ENG-031`) found all six PRs' worth
of tickets (eight PRs total — `ENG-013` and `ENG-015` are both two-repo)
merged directly
on GitHub with no written reply to any; every item moved to
`inbox/_handled/` (or, for `ENG-013`, was already there) and every one of
these six tickets carried `blocked → shipped →
verified`. `ENG-032`'s shipping in turn satisfies `ENG-033`'s last unmet
dependency — dispatched via `continue ENG-033` this same pass rather than
built inline; `ENG-013`'s shipping satisfies `ENG-028`'s sole dependency,
which stays `awaiting-scope` regardless, still gated by its own unanswered
G1. See the closing paragraph below and each ticket's own board
file.

**A later `watch (launchd)` event pass's own step-5 re-check closed the
loop on both remaining threads.** `ENG-033` — dispatched by the `continue`
above, built through to a merge request — was itself found merged directly
to `main`, unblocking `ENG-034`, the last `ENG-016` sub-ticket
(`continue ENG-034` fired). And `ENG-009`/`ENG-010`, stuck since the
morning on a stacked branch that never reached `main` on its own, shipped
via a fresh consolidating PR on each repo. All three carried
`blocked → shipped → verified`; none remain open in this section. See each
ticket's own paragraph above and board file.

## 2026-09-04 — decision (`ENG-036`'s P0 incident): premise checked against the design, no ticket filed — still `designed`, still held by the `ENG-016` family's machine-WIP cap

`decision` event pass, context `2026-09-03-eng036-p0-incident.md`. Reading
map for `decision`: steps 4 and 8c, plus the not-negotiable set (1, 7, 8b, 9,
10; *Enforced vs instructed*, *The four lanes*, *Guards*) — step 5 doesn't
apply (not an L1 merge request), step 8's `blocked_from` paragraphs don't
apply (ticket isn't leaving `blocked`), and neither does *The chain* (this
incident is about a ticket, not the loop/queue itself). Mode check clean
(repo-root `.env` → `MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board and scoped
(`ENG-036`): both exit 0, clean.

**Unlike its two siblings this pass processed already.** `ENG-029`'s and
`ENG-035`'s own P0 incidents were both bare `approved`, nothing to act on.
`ENG-036`'s was answered `changed` at `2026-09-04T14:58:46.245104+00:00`,
verbatim: "When you add auth to this edge function any code using it will
break, that needs a ticket to update all the code that used it." Step 6's
"does the answer advance the ticket into a machine-owned state" question
doesn't fit cleanly here either — the right response was to check the claim
against the ticket's own design, not transition anything.

**Checked, not assumed either way.** `ENG-036`'s own design and `ADR-017`
already enumerate every caller of `outgoing-communications` across all five
of this instance's registered repos, done at design time because the PRD
named exactly this as a risk. Three call sites set `systemTriggered: true`
— the only ones this fix's new `else` branch gates — and all three already
send the exact credential the gate requires, confirmed by reading each call
site's own source. The other three known callers don't set that flag and
stay on the function's existing, untouched user-session path, unaffected
either way. No caller this codebase's own source shows needs a code change.

**Action: no ticket filed** — there is no callers-to-update work to put in
one. Named plainly rather than quietly declined, same footing as `ENG-027`'s
own vacuous "if not cancelled or deleted" condition earlier on this board:
a mismatch between a reasonable general expectation and this specific
diff's already-verified effect, stated openly rather than silently
overridden. The one real residual risk here (deployed `SUPABASE_SERVICE_ROLE_KEY`
drift between the Cloudflare Worker and Supabase's own secret store) is
already covered by the design's own mandatory post-deploy log check, not
left uncovered by this decision — and if a caller this enumeration missed
turns up later, that's a new finding at that time, not something foreclosed
by closing this item now.

Processed note appended to the incident item and moved to
`inbox/_handled/2026-09-03-eng036-p0-incident.md`, per `eng_build_loop.md`
step 4's Incident handling. **Journal (step 8c):** row added to
`decision-journal.md`, approver's words verbatim plus this interpretation
labelled as interpretation. **Step 8b:** one observation filed
(`observations.md`) — an incident notice is necessarily written before
design happens, so it can't yet carry the design's own caller-safety
evidence; a "won't this break things" reply to one is expected, not a sign
of anything rushed. Full reasoning: `ENG-036`'s own board-file log.

**Machine WIP re-checked fresh, not assumed unchanged:** `ENG-016`
`building`, `ENG-031`/`ENG-032` `verified`, `ENG-033` `blocked` (`owner:
approver`), `ENG-034` `ready` — still `1/1`, the family still holds the
slot. `ENG-036` stays `designed`, `owner: architect`, no design change.

**Notify sweep (step 7):** swept `inbox/` fresh (`date -u`:
`2026-09-04T15:25:51Z`). `ENG-009`/`ENG-010`/`ENG-027` already carry a
`nudged:` timestamp; `ENG-028`'s G1 (~23h15m since `notified:`) and
`ENG-033`'s merge request (~13h43m) both still sit under the 24h threshold.
**`ENG-030`'s P0 incident crossed 24h this pass** (notified
`2026-09-03T15:24:21`, ~24h01m elapsed, no `nudged:`, no `decision:`) —
nudged (`lib/eng-notify.sh nudge`), stamped `nudged: 2026-09-04T15:26:20`.
The nudge call logged `sent: active`, not `sent: nudge`
(`traces/eng-notify-2026-09-04.log`) — the same standing `MODE`-clobber bug
`proposals.md`'s 2026-08-25 row already carries and this instance's own
`scheduled` pass already reconfirmed once today; a third same-day
recurrence with no new signal, not re-amended into that row again.

business-os itself left uncommitted, same standing default the last several
passes have each restated; not re-decided here.

**Board update (step 10):** In-flight row's `ENG-036` `Updated` date bumped
(2026-09-03 → 2026-09-04), state/owner unaffected. The live file held three
dated pass entries before this one; rolled the oldest (`scheduled: no gate
answered, two 24h nudges sent...`) to `_index-archive.md` first, then
appended this entry, keeping three per the keep-three rule.

Post-pass `departments/engineering/lib/eng-gate-check.sh`, whole-board and
scoped `ENG-036`: both exit 0, clean.

`chained: none` — `ENG-036` stays held by the machine-WIP cap (`1/1`, the
`ENG-016` family), re-confirmed fresh, not assumed. Not blocked, not
terminal, not waiting on the approver — only the cap.

## 2026-09-04 — watch (launchd): three silent GitHub merges found and shipped (`ENG-009`, `ENG-010`, `ENG-033`) — `continue ENG-034` fired

`watch` event pass, context `launchd`. Per the reading map: steps 2, 3, 4
(sweep all three inboxes) and 5 (merge detection — run because open
merge-request items exist for every currently-`blocked` ticket, the same
reading this board's own prior `watch` passes already established), plus
the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The
four lanes*, *Guards*). Mode check clean (repo-root `.env` →
`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, whole-board and scoped
(`ENG-009`, `ENG-010`, `ENG-033`): all exit 0, clean.

**Why this fired.** The immediately preceding `decision (ENG-036)` pass
(entry above) closed the last of three P0-incident hand-edits
(`ENG-029`/`ENG-035`/`ENG-036`); each edit landed inside the watched
`inbox/`, and one `watch (launchd)` fire had queued behind them as a
self-echo (`traces/.pending` — noted in advance on the `ENG-035` entry
above). This is that fire draining.

**Step 2 (PM intake):** `agents/product-manager/inbox/` holds nothing
beyond `_handled/`/`.gitkeep` — no new business intake.

**Step 3 (EM technical intake):** `agents/eng-manager/inbox/` holds
nothing beyond `_processed/`/`.gitkeep` — no new department-originated
finding.

**Step 4 (gate returns):** all six open `inbox/` items grepped for
`decision:` fresh — `ENG-009`/`ENG-010`/`ENG-033` merge requests,
`ENG-027`'s rescope G1, `ENG-028`'s G1, `ENG-030`'s P0 incident — every
`decision:` field still blank on every one. Nothing answered in the
tracked channel this pass; the self-echo carried no new signal of its own.

**Step 5 (merge detection) — this is where the pass's real work was.** For
each of the three currently-`blocked`, merge-request-carrying tickets:
`git fetch origin` fresh on both worktrees
(`~/Documents/projects/_eng/{aiorders-api,aiorders-admin-hub}`), then
`git merge-base --is-ancestor` on each ticket's own **recorded** commit
(frontmatter `branch:`, not a live branch tip — this board's standing fix
for the `ENG-008` branch-tip-contamination failure mode) against fresh
`origin/main`:

| Ticket | Recorded commit(s) | Result |
|---|---|---|
| ENG-009 | `aiorders-api@d37e0c9`, `aiorders-admin-hub@92bcacd` | **MERGED**, both repos |
| ENG-010 | `aiorders-api@486eec0`, `aiorders-admin-hub@8b90f0e` | **MERGED**, both repos |
| ENG-033 | `aiorders-api@697df79` | **MERGED** |

All three came back positive — a first for this board's `watch`-pass
history, whose prior two occurrences (`_index-archive.md`) both found no
change from the `scheduled` sweep immediately before them. Re-fetched a
second time on discovering this to rule out reading an in-flight write;
identical result both times.

Cross-checked every hit with `gh pr view`/`gh pr list` rather than taking
the ancestry bit alone, given the severity of getting a `shipped` write
wrong: `ENG-033`'s own PR #13 merged directly to `main`
(`2026-09-04T15:25:13Z`, no stacking). `ENG-009`'s and `ENG-010`'s
*original* PRs (`aiorders-api` #7/#8, `aiorders-admin-hub` #6/#7) were
still merged only into their stacked sibling branches, exactly as this
board's own prior finding recorded — the ancestry hit came from a **new**
PR on each repo, `merge/ENG-009-ENG-010-to-main` (`aiorders-api` #14,
`aiorders-admin-hub` #9), base `main`, head the stacked branch's own
current tip, merged directly on GitHub at `15:39:16Z`/`15:40:31Z` — one
to fifteen minutes before this pass ran. This is the "fresh PR from the
current stacked-branch tip" option `ENG-009`'s own board log had named as
one of two open paths to `main`; the approver took it, by hand, without
being asked.

**Not advanced past a state that owes gates** (step 5's own "a merge is
not a gate" clause) — all three tickets' full receipt sets re-read
directly before writing `shipped`: `ENG-009` (review/QA/security all
`pass`), `ENG-010` (same, all `pass`), `ENG-033` (review round 4/QA round
2/security, all `pass`). No migration owed by any of the three. All
recorded commits confirmed present on `origin/main` by exact SHA. Release
records written: a combined one for `ENG-009`+`ENG-010` (same merge
commits ship both,
`agents/devops/releases/2026-09-04-ENG-009-ENG-010-aiorders-api-and-admin-hub.md`)
and one for `ENG-033`
(`agents/devops/releases/2026-09-04-aiorders-api-ENG-033.md`), `links.pr`
and `links.release` updated on all three tickets in the same edits. All
three: `state: blocked → verified`, `owner: approver → eng-manager`,
`blocked_on`/`blocked_from` cleared. All three merge-request items closed
with a final resolution note and moved to `inbox/_handled/`. Two
`decision-journal.md` rows added (one combined for `ENG-009`/`ENG-010`,
one for `ENG-033`) as new rows documenting the follow-up resolution,
rather than edits to the existing rows that correctly recorded the
original, incomplete finding.

**6 transitions total** (2 each × 3 tickets: `blocked → shipped`,
`shipped → verified`), well under the per-ticket cap of 4. **Consequence:**
no machine-WIP change from `ENG-009`/`ENG-010` (never inside the counted
`ready..ready-to-ship` range, no family membership, `blocks: []` on both).
`ENG-033`'s own exit doesn't free the machine-WIP slot either — it was
already outside that range while `blocked` — but its shipping **does**
satisfy `ENG-034`'s sole dependency (`depends_on: [ENG-033]`), the last
`ENG-016` sub-ticket, sitting `ready`/`owner: eng-manager` with nothing
else holding it. Per this family's own first-precedent reading
(`agents/eng-manager/notebook/2026-09-03-eng016-work-breakdown.md`), the
WIP slot is held by the family as a whole, so dispatching `ENG-034` needs
no fresh slot. **Fired `continue ENG-034`** rather than building it inline
— new implementation work stays out of a `watch` event's contract — same
handoff shape `ENG-031`'s and `ENG-032`'s own shipping passes already used
for their own successors.

**Step 7 (notify sweep):** current `2026-09-04T15:56:07Z`. Three open
`inbox/` items remain (`ENG-027`, `ENG-028`, `ENG-030`'s P0) — `ENG-027`
and `ENG-030` already carry a `nudged:` timestamp; `ENG-028` (~23h46m
since `notified:`) is still under the 24h threshold, by about 14 minutes.
Nothing crossed; no nudge sent.

**Step 8b (observations/exceptions):** one observation filed
(`observations.md`) — this resolves the open "how does a stacked ticket
reach `main`" question with a concrete data point (a fresh PR from the
stacked tip, by hand), and names this as the first `watch` pass to catch a
production merge ahead of the next `scheduled` sweep. No `exception-request:`
in any ticket log.

**Step 8c (journal):** both rows described under step 5 above.

**Board update:** this entry appended; rolled the oldest of the three live
dated entries (`decision (ENG-029's P0 incident)`) to `_index-archive.md`
per the keep-three rule, verified the seam clean on both files before
appending here. In-flight table: `ENG-009`, `ENG-010` and `ENG-033` rows
removed (terminal). Header narrative, the "Waiting on the approver"
section, and the closing terminal-tickets paragraphs all updated in place
to mark the three resolved rather than left to contradict the table — see
each ticket's own paragraph above.

Post-pass `lib/eng-gate-check.sh`, whole-board and scoped (`ENG-009`,
`ENG-010`, `ENG-033`): all exit 0, clean.

`chained: ENG-034` — not any of the three tickets this pass shipped
(`verified` is terminal, the chaining guard never fires on it), but the
sibling their shipping unblocked.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.
This pass's own diff is large (three tickets shipped, two release records,
a board-index rewrite across four sections) — worth the approver's own
attention regardless of which pass eventually commits it.

## 2026-09-04 — continue (`ENG-034`): `ready → building` — `ENG-016` family's last sibling now dispatched

`continue` event pass, context `ENG-034`, per the prior `watch (launchd)`
pass's own `chained: ENG-034` (`ENG-033` shipped, satisfying this ticket's
sole dependency). Reading map for `continue`: steps 6 and 6b (design
already complete, not mid-PRD), plus the not-negotiable set (1, 7, 8b, 9,
10; *Enforced vs instructed*, *The four lanes*, *Guards*). Mode check clean
(repo-root `.env` → `MODE=active`). Pre-pass `eng-gate-check.sh`, scoped
(`ENG-034`) and whole-board: both exit 0, clean.

Ticket file and `ENG-033`'s own board file both read directly rather than
trusted from the trigger's checkpoint — `ENG-033` confirmed `verified`,
`aiorders-api` PR #13 merged to `main`, all three gate receipts `pass`.
Machine WIP re-checked fresh: `ENG-016` `building`, `ENG-031`/`ENG-032`/
`ENG-033` all `verified` — still `1/1`, held by the family as a whole per
this family's own first-precedent reading, so dispatching this last sibling
needed no fresh slot.

**Built all three files the design's own `## Components` table names for
this surface**: `config-site-builder`'s `src/types/restaurant.ts` (extended
with `CateringFulfillmentCopy` and the two new `CateringPageContent` keys,
mirrored field-for-field off `restaurant-portal`'s already-shipped copy of
the same interface), new `src/components/CateringMenuSelector.tsx`
(category-grouped dish picker, quantity + per-dish note, controlled, no
price rendered anywhere per the design's own Out-of-scope section), and
`src/components/CateringForm.tsx` (the gate expression, fulfillment
label/description copy, conditional email requirement, selector mount, the
two submit actions). Every gate-open-only change is expressed as
`orderFormEnabled ? new : original` against the exact original code, so
AC-9's byte-for-byte gate-closed rendering holds by construction rather
than by a parallel branch. Full reasoning and every interpretation call —
selection identity vs. the wire shape, the no-stock/hidden-dish read, which
submit button fired read via `SubmitEvent.submitter`, and more:
`agents/eng-manager/notebook/2026-09-04-eng034-build.md`.

**Self-tested.** First-ever `npm install` in this worktree (`node_modules`
didn't exist). `npm run lint`: the two touched/new files clean;
`types/restaurant.ts`'s 4 `no-explicit-any` hits on the untouched
`brand.metadata` block confirmed pre-existing via `git stash` (identical
count against the pristine file, merely shifted by this diff's own
insertion). `npm run build`: clean. `npx tsc --noEmit` (beyond this
project's own defined check surface — only `lint`/`build` are, per
`config/projects.md` — run for extra rigor since Vite's `build` doesn't
type-check): clean.

**Worktree was on the parent ticket's own stale branch**
(`feat/ENG-016-catering-quote-generator`, never diverged from
`origin/main`) — same slip `ENG-031`/`ENG-032`/`ENG-033` each hit on this
shared worktree. Branched fresh:
`feat/ENG-034-catering-menu-selector-public-form` off `origin/main`,
carrying this hop's working-tree changes over cleanly. Committed
`config-site-builder@62b3ca0`, pushed. No PR opened yet — devops's own
release-readiness hop, same precedent every prior building hop on this
board has set.

**1 transition** (`ready → building`), under the cap of 4. Machine WIP
unaffected — still 1/1, `ENG-016` family. No approver-facing WIP or
approval-cap change — no gate touched this hop. `time_spent`/
`time_remaining` and `branch` set in frontmatter for the first time on this
ticket.

Dead-end sweep (scoped to this event): no other ticket touched. Notify
sweep: current `2026-09-04T16:13:26Z` — `ENG-028`'s G1 crossed 24h with no
`nudged:`/`decision:` (`notified: 2026-09-03T16:10:27`), nudged and stamped
`nudged: 2026-09-04T09:13:37` (copied verbatim from the trace log, same
standing local-time-labeled-as-UTC convention this board already uses);
`ENG-027`/`ENG-030` already carry their one-time nudge. One observation
filed (`observations.md`): `ENG-031`/`ENG-032`/`ENG-033`'s own build-hop
log entries were each written long-form, directly in the ticket log, rather
than routed through `config/conventions.yaml` →
`ticket_log.entry.reasoning_goes_to` the way `cap_lines: 20` is meant to
enable — this hop followed the written convention instead. Step 6b: not
run — product code internal to one repo, no receipt path/state name/config
key/cross-agent artifact rule involved. Journal: n/a — no gate answered
this hop.

**Board update:** In-flight row updated (`ready → building`,
`eng-manager → frontend`, date bumped). The file held three live dated
entries before this one; rolled the oldest (`decision (ENG-035's P0
incident)`) to `_index-archive.md` first, then appended this entry, keeping
three per the keep-three rule.

`chained: ENG-034` — `building` is agent-owned (next hop: code review,
principal-engineer); not the approver, not blocked, not terminal, not held
by a cap. Fired `/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-034` before this pass exits. Post-pass `eng-gate-check.sh`,
scoped (`ENG-034`) and whole-board: see below.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

