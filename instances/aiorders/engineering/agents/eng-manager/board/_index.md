# Board

**Next ID: ENG-040** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.) `ENG-037`–`ENG-039` allocated
this pass — `ENG-019`'s own `work-breakdown` run, one sub-ticket per surface
(database/backend/frontend). In-flight row and this counter both updated in
the same edit the tickets were filed, not left for a later sweep.

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

**A later `watch (launchd)` event pass's own step-5 re-check (this pass)
now finds `ENG-034` merged too** — `config-site-builder` PR #4, no written
reply, base `main` directly, no stacking. Receipts re-verified fresh, all
`pass`, no migration owed; unlike the last ten tickets to ship, this pass
ran `acceptance-check/SKILL.md` in full rather than receipt-bookkeeping
alone (the skill's own trigger had gone unexercised, with no notebook
entry, since `ENG-007`/`ENG-011` on 2026-08-30 — proposal filed,
`proposals.md`, this date). All eight owned criteria confirmed pass against
the merged tree directly. Carried `blocked → shipped → verified` — the
`ENG-016` family's fourth and last sub-ticket now shipped or verified. Per
the parent's own `## Breakdown` (`ADR-003`-class exemption), `ENG-016`
itself is now eligible to move `building → shipped` directly, without its
own review/QA/security hops — not processed inline this pass; `continue
ENG-016` fired instead, same handoff shape this family's own prior shipping
passes already used for their successors. The machine-WIP slot itself is
still held by the family (`ENG-016` still `building`) until the parent's
own chained pass carries it to `shipped`.

**That chained pass is this pass's own predecessor state, now resolved:
`ENG-016` itself carried `building → shipped → verified`**, `ADR-003`-class
exemption (all four children settled, at least one shipped), acceptance-check
run in full despite the exemption — all 13 PRD criteria pass, 8
cross-referenced from `ENG-034`'s own walk and 5 (`ENG-032`'s/`ENG-033`'s
own, never individually checked before) walked fresh against live
`origin/main`. See
`agents/product-manager/notebook/2026-09-04-eng016-acceptance.md` and the
ticket's own board-file log. **Machine WIP: `1/1 → 0/1`, free** — the whole
`ENG-016` family is now terminal, and the next free slot goes to whichever
`designed` ticket the next dispatch-scoped pass (`scheduled`, or a
qualifying `decision`/`watch`) picks by the board's own priority order, not
fired inline here (`continue`'s own single-ticket scope). Step 6b's bar
(explicit sequence sign-off) was not met by this ticket's own G1 ("Lets
start with piece 1"), so Piece 2 was not auto-filed — a targeted question
was raised instead:
`inbox/2026-09-04-eng016-continue-piece2-question.md`.

**This `scheduled` pass is that next dispatch-scoped pass — `ENG-019`
picked, now occupying the slot.** To-do column (`intake`/`shaped`/
`awaiting-scope`) had nothing machine-actionable (`ENG-018` held;
`ENG-027`/`ENG-028` genuinely waiting on the approver), so per `ENG-019`'s
own 2026-09-03 entry the pick came from the held-for-slot pool instead:
`designed` tickets with a completed design and no one-way door, deferred
only by the cap. `ENG-019`, `ENG-020` and `ENG-021` all carry
`priority: now`; lowest id decided. **Machine WIP: `0/1 → 1/1`**, `ENG-019`
`designed → ready`, `owner: architect → eng-manager`, no G2 (routing per
`tech-design/SKILL.md` step 11, already determined 2026-09-03). Stopped
there — work-breakdown/building is new implementation work, chained instead
of run inline, same shape every `ENG-031`→`ENG-034`→`ENG-016` handoff
already used today. `ENG-020` and `ENG-021` (also `now`, also
held-for-slot) stay `designed`, correctly capped again the moment `ENG-019`
claimed the slot; not touched further. Full reasoning:
`ENG-019`'s own board-file log.

**Two stale `owner` fields found and fixed while sweeping the whole board
for this dispatch:** `ENG-014` and `ENG-025`, both frontmatter
`owner: eng-manager` despite each one's own log explicitly leaving it
`designed`/`architect`, and despite `ENG-019`'s own 2026-09-03 entry naming
both as part of the same held-for-slot pool as `ENG-019` itself (same
state, same owner). No log entry on either ticket records an intentional
`eng-manager` handoff; likely origin the `e281c71` board-reconciliation
merge, not chased further since the fix is the same regardless of cause.
Both corrected to `owner: architect`. No functional consequence — a
`continue` fire routes off `state:`, not `owner:` — but left wrong it
misleads a reader about whose desk the ticket is on. Neither ticket's
standing changes (both still carry no `priority:`, so neither contends with
`ENG-019` for a slot). Full detail on each ticket's own board file.

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

One item genuinely on the approver's plate right now, unanswered:
`ENG-028` (new G1). **`ENG-027`'s own fresh G1 is gone from this list** —
the first G1's `changed` answer was processed and the ticket rescoped
`M → L`; the fresh G1 that followed was answered **approved**
(2026-09-05T17:01:12), no additional comment, and processed by this
`decision` event pass — see the header bullet above and the ticket's own
board-file log for the full reasoning. **`ENG-037`'s own fresh L1 merge request is gone from this
list** — this `scheduled` sweep's own step-5 merge detection found it
merged directly to `main`, receipts re-verified fresh, carried
`blocked → shipped → verified`; unblocked `ENG-038`, dispatched via
`continue` this same pass rather than built inline. See its own paragraph
above and the closing paragraph below. `ENG-034`'s own fresh L1 merge request — the `ENG-016` family's
last sub-ticket, all three machine gates passed — is gone from this list: a
later `watch (launchd)` event pass's own step-5 re-check found it merged
directly to `main` and, after a full acceptance-check, carried it
`blocked → shipped → verified`; see the ticket's own board-file log and the
closing paragraph below. No cap on how many of these may be open at once —
see header above; nothing here gates a new start. `ENG-015`'s own merge request is gone from this list —
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

**`ENG-019` ran `work-breakdown` this pass (`ready → building`, no diff of its
own — see its own `## Breakdown` section) and decomposed into three
sub-tickets, `ENG-037`–`039`, one per surface, sequenced by the design's own
Rollout order (migration → functions → frontend).** Same WIP-family reading
`ENG-016`'s decomposition already established: the slot is held by the
ticket family, not by each row separately, so this is still `1/1`, not
`2/1`. `ENG-037` (database, no dependency) dispatched straight to
`building`; `ENG-038` (backend) and `ENG-039` (frontend) stay `ready`,
each waiting on its unmet `depends_on`. Full reasoning:
`agents/eng-manager/notebook/2026-09-04-eng019-work-breakdown.md`.

**This `scheduled` pass's own step-5 merge detection finds `ENG-038` merged
too** — `aiorders-api` PR #16, base `main`, no stacking, `mergedAt:
2026-09-05T07:22:20Z`, no written reply. All four gate receipts (review/
quality/security/migration) re-read fresh and confirmed `pass`. **Ran
`acceptance-check/SKILL.md` in full** — this ticket owns all 7 of `ENG-019`'s
acceptance criteria per the work-breakdown's own AC-mapping (unlike
`ENG-037`'s 0-criteria schema-only shape) — and found mid-check that
release-readiness's own "not deployed" snapshot from the pass immediately
before had already gone stale: all four touched functions are now live in
`bmnmnejwdxbcqinqkwko`, deployed by hand within minutes of the merge, no
tracked workflow responsible. Re-verified read-only: the migration's live,
the Vault `service_role_key` `ENG-037`'s cron needs is present,
`BROADCAST_UNSUBSCRIBE_SECRET` is not — dormant until a real campaign exists
(`ENG-039` hasn't shipped), same non-blocking shape as `ENG-037`'s own named
prerequisite. No test campaign created or send exercised — that would reach
real customers. All 7 criteria pass; carried `blocked → shipped → verified`
this pass. Full walk:
`agents/product-manager/notebook/2026-09-05-eng038-acceptance.md`; release
record: `agents/devops/releases/2026-09-05-aiorders-api-ENG-038.md`.
Satisfies `ENG-039`'s sole dependency (`depends_on: [ENG-038]`) — this pass
fired `continue ENG-039` rather than building it inline, the family's last
handoff. **Machine WIP unaffected — still `1/1`, held by the `ENG-019`
family** (`ENG-019` parent still `building`, waiting on `ENG-039`).

**The `ENG-019` family's own completion, two passes later, freed the slot
entirely — `ENG-020` now occupies it.** `ENG-037`, `ENG-038` and `ENG-039`
each reached `verified` in turn, then `ENG-019` itself closed out via its
own `ADR-003`-class exemption (`continue ENG-019`, `building → shipped →
verified`) — Machine WIP `1/1 → 0/1`, free; see each ticket's own closing
paragraph above. **This `scheduled` pass** re-checked the To-do column
fresh and found nothing machine-actionable there again (`ENG-018` held;
`ENG-028`'s G1 still unanswered), so the pick came from the held-for-slot
pool: `ENG-020`, `ENG-021`, `ENG-026` and `ENG-027` all carry `priority:
now` and a completed design with no one-way door; lowest id decided.
`ENG-020`'s own routing (`ready`, `owner: eng-manager`, no G2) was already
determined by its 2026-09-03 design pass and only re-used here, not
re-derived. **Machine WIP: `0/1 → 1/1`**, `ENG-020` `designed → ready`,
`owner: architect → eng-manager`. Stopped there — building is new
implementation work, chained instead (`continue ENG-020`). `ENG-021`,
`ENG-026` and `ENG-027` stay `designed`, correctly capped again the moment
`ENG-020` claimed the slot. Full reasoning: `ENG-020`'s own board-file log.

`priority:` is a field on every ticket, and **only the approver sets it.** It is
not `severity`, which is the agent's read of how bad a problem is.

## In flight

| ID | Title | Project | State | Priority | Owner | Size | Updated |
|---|---|---|---|---|---|---|---|
| ENG-014 | Brand portal self-service — restaurant QR codes and marketing media downloads | restaurant-portal | designed | | architect | M | 2026-09-04 |
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
| ENG-017 | Autopilot nurture for the presignup sales lead pipeline — stage-triggered email/SMS | aiorders-api | designed | | architect | L | 2026-09-01 |
| ENG-018 | Sales demonstration account — a fully seeded AIOrders environment to show prospects | aiorders-admin-hub | shaped | hold | product-manager | L | 2026-09-03 |
| ENG-020 | Marketing ROI reporting — traffic source and revenue attribution on the brand dashboard | restaurant-portal | blocked | now | approver | M | 2026-09-05 |
| ENG-021 | Website chat-bar engagement visibility — customer questions and self-service FAQ editing on the brand portal | restaurant-portal | designed | now | architect | M | 2026-09-03 |
| ENG-023 | Add status and internal notes to each brand-portal feedback item | restaurant-portal | designed | | architect | S | 2026-08-31 |
| ENG-025 | Recurring feedback issues, per restaurant, over time | restaurant-portal | designed | | architect | S | 2026-09-04 |
| ENG-026 | FoodSwipe channel-visibility toggles and capability-based discovery | restaurant-marketplace | designed | now | architect | M | 2026-09-03 |
| ENG-027 | Loyalty points ledger, balances, and earn API — online-order and dine-in accrual | aiorders-api | designed | now | architect | L | 2026-09-05 |
| ENG-028 | Foodswipe funnel — staff-configurable pipeline stage set | aiorders-admin-hub | awaiting-scope | | approver | L | 2026-09-03 |
| ENG-029 | Autopilot API has no restaurant-ownership check on any of its 8 actions — cross-tenant customer-data exposure | aiorders-api | designed | | architect | M | 2026-09-04 |
| ENG-030 | `analytics` edge function has no authentication or authorization at all — cross-tenant revenue/order/customer exposure | aiorders-api | designed | | architect | S | 2026-09-04 |
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

**`ENG-034` joins the terminal group too, found by a later `watch
(launchd)` event pass's own step-5 re-check (this pass).** `config-site-builder`
PR #4 merged directly to `main`, no stacking, no written reply. All three
gate receipts re-read fresh and confirmed `pass`; no migration owed.
**Acceptance-check run in full this pass**, not the receipt-bookkeeping
shortcut every ticket since `ENG-011` (2026-08-30) has used — see
`agents/product-manager/notebook/2026-09-04-acceptance.md` and the proposal
filed the same date. Carried `blocked → shipped → verified` — off the
In-flight table (terminal); see its own board file and
`agents/devops/releases/2026-09-04-config-site-builder-ENG-034.md`. This was
the last of `ENG-016`'s four sub-tickets — `continue ENG-016` fired this
same pass rather than processing the parent's own `ADR-003`-class shipped
exemption inline.

**`ENG-016` itself joins the terminal group, from the very next `continue`
pass its own predecessor fired.** `building → shipped → verified`,
`ADR-003`-class exemption (all four children settled, at least one
shipped) — no diff, review, QA, or security hops of its own. Acceptance-check
run in full anyway (the trigger has no parent carve-out): all 13 PRD
criteria pass, no scope creep, cost `$0/month` as estimated — off the
In-flight table (terminal); see its own board file and
`agents/product-manager/notebook/2026-09-04-eng016-acceptance.md`. Machine
WIP `1/1 → 0/1`, free. Step 6b's sequence-sign-off bar wasn't met by this
ticket's own G1, so Piece 2 wasn't auto-filed — a targeted question went to
`inbox/` instead (see "Waiting on the approver" below).

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

**`ENG-037` joins the terminal group too, found by this `scheduled` pass's
own step-5 re-check.** `aiorders-api` PR #15 merged directly to `main`, no
stacking, no written reply, about 1h40m before this pass ran. All four gate
receipts re-read fresh and confirmed `pass`; no migration owed (this
ticket *is* the migration). **New this pass:** this host's newly-linked
`supabase` CLI confirmed the migration is actually live in production, not
just merged — all three tables and the `broadcast-dispatch-tick` cron job
(`active`, every 5 minutes) present in `bmnmnejwdxbcqinqkwko`, the first
time an `aiorders-api` release on this board has confirmed live deploy
state directly rather than leaving it as an open question. That live check
also confirmed the pre-`ENG-038` observability gap named non-blocking at
release-readiness is now actually occurring (a 404 every 5 minutes, not
merely a named risk) — still non-blocking for the same reasons already
given, named plainly so it isn't mistaken for a regression later. Carried
`blocked → shipped → verified` via receipt-bookkeeping (same route
`ENG-031` set — 0 of the parent's acceptance criteria apply to a
schema-only diff) — off the In-flight table (terminal); see its own board
file and `agents/devops/releases/2026-09-04-aiorders-api-ENG-037.md`. Its
shipping satisfies `ENG-038`'s sole dependency (`depends_on: [ENG-037]`) —
`continue ENG-038` fired this same pass rather than building it inline,
same handoff shape every `ENG-019` sub-ticket and the whole `ENG-016`
family already used. `ENG-039` still waits on `ENG-038` in turn. Machine
WIP unaffected — this ticket already left the counted
`ready..ready-to-ship` range at its prior `ready-to-ship → blocked` hop;
the family's slot (`ENG-019`/`ENG-038`/`ENG-039`) is unchanged at `1/1`.

**`ENG-038` joins the terminal group too, found by this `scheduled` pass's
own step-5 re-check.** `aiorders-api` PR #16 merged directly to `main`, no
stacking, no written reply, `mergedAt: 2026-09-05T07:22:20Z`. All four gate
receipts re-read fresh and confirmed `pass`. **Full `acceptance-check`
run**, not receipt-bookkeeping — this ticket owns all 7 of `ENG-019`'s
criteria per the work-breakdown's own AC-mapping. **New this pass:** found
mid-check that the immediately-prior release-readiness hop's own "not
deployed" snapshot had already gone stale — all four touched functions
(`brand-portal`, `broadcast-dispatch`, `broadcast-unsubscribe`,
`outgoing-communications`) are live in `bmnmnejwdxbcqinqkwko`, deployed by
hand within 3-8 minutes of the merge, no tracked workflow responsible.
Re-verified read-only: the migration's constraint/index are live, the Vault
`service_role_key` `ENG-037`'s cron needs is present,
`BROADCAST_UNSUBSCRIBE_SECRET` is not (dormant — no campaign exists yet, and
`ENG-039` is the only path to create one) — same non-blocking shape as
`ENG-037`'s own named prerequisite, already tracked in three other
notebooks. No test campaign created or send exercised. All 7 criteria pass
— carried `blocked → shipped → verified` this pass; see its own board-file
log, `agents/product-manager/notebook/2026-09-05-eng038-acceptance.md`, and
`agents/devops/releases/2026-09-05-aiorders-api-ENG-038.md`. **Off the
In-flight table (terminal).** Its shipping satisfies `ENG-039`'s sole
dependency — `continue ENG-039` fired this same pass rather than building
it inline, the family's last handoff. Machine WIP unaffected — still `1/1`,
held by the `ENG-019` family (parent still `building`, one sub-ticket left).

**`ENG-039` joins the terminal group too, found by a `watch (launchd)` event
pass's own step-5 re-check** (not the same pass that raised its merge
request, and not the next `scheduled` sweep either — the second time this
board's had a fresh merge caught by `watch` and carried the whole way, after
`ENG-034`'s). `restaurant-portal` PR #3 merged directly to `main`, no
stacking, no written reply, `mergedAt: 2026-09-05T17:05:41Z`. `git diff
2f438e0 aeeb7b9 --stat` empty — zero drift from what all three gates
reviewed. All three gate receipts re-read fresh and confirmed `pass`; no
migration owed (pure frontend diff, confirmed against the 9-file/1,571-line
diff). **Full `acceptance-check` run**, not receipt-bookkeeping — this
ticket owns AC1-5 of `ENG-019`'s 7 per the work-breakdown's own AC-mapping.
Unlike `ENG-038`'s same-evening deploy-by-hand surprise, this is a static
Cloudflare Pages frontend with no live runtime state of its own, so the
merge commit itself was the full source of truth — no drift window, nothing
to re-check live. All 5 owned criteria pass — carried `blocked → shipped →
verified` this pass; see its own board-file log,
`agents/product-manager/notebook/2026-09-05-eng039-acceptance.md`, and
`agents/devops/releases/2026-09-05-restaurant-portal-ENG-039.md`. **Off the
In-flight table (terminal).** Every child of `ENG-019` (`ENG-037`, `ENG-038`,
this ticket) is now `shipped`/`verified` — the `ADR-003` parent exemption is
satisfied. `ENG-019` itself is not touched in this pass; `continue ENG-019`
fired instead, same handoff shape `ENG-034`'s own shipping pass used for
`ENG-016`. Machine WIP unaffected — still `1/1`, held by the `ENG-019`
family until the parent's own chained pass carries it to `shipped`.

**`ENG-019` itself joins the terminal group too, from the very next `continue`
pass its own predecessor fired.** `building → shipped → verified`,
`ADR-003`-class exemption (all three children settled, all three actually
shipped) — no diff, review, QA, or security hop of its own. Ran
`acceptance-check/SKILL.md` in full anyway (the trigger has no parent
carve-out): all 7 PRD criteria pass — cross-referenced from `ENG-038`'s and
`ENG-039`'s own already-full walks (both repos re-fetched fresh, zero drift
from the commits those walks checked), no gap to backfill this time, unlike
`ENG-016`'s family. No scope creep, cost `$0/month` as estimated — off the
In-flight table (terminal); see its own board file and
`agents/product-manager/notebook/2026-09-05-eng019-acceptance.md`. **Machine
WIP `1/1 → 0/1`, free** — the whole `ENG-019` family is now terminal, and the
next free slot goes to whichever `designed` ticket the next dispatch-scoped
pass (`scheduled`, or a qualifying `decision`/`watch`) picks by the board's
own priority order, not fired inline here (`continue`'s own single-ticket
scope). Step 6b did not apply — no PRD-named next item with real shape, and
the G1 was a bare approval with no sequence sign-off.

## Waiting on the approver

**No cap — `wip.approver_limit: unlimited` since 2026-09-02 (see header
above). Three items currently open** (`ENG-028`'s G1, `ENG-016`'s
continue-to-Piece-2 question, `ENG-020`'s L1 merge request — see each one's
own paragraph below).
`ENG-027`'s rescope G1 — answered **approved** (2026-09-05T17:01:12),
processed by a `decision` event pass, see its own paragraph below — and
`ENG-038`'s and `ENG-039`'s own fresh L1 merge requests — both resolved by a
`watch (launchd)` or `scheduled` pass's own step-5 re-check finding their
PRs merged with no written reply — are now off this list too, the same way
`ENG-008`/`ENG-009`/`ENG-010`/`ENG-033`/`ENG-034` already left it earlier
the same day; see each one's own paragraph below and the closing paragraphs
above. Listed here
for visibility, not because any number of them blocks a new start.

**`ENG-039`'s L1 merge request**
(`inbox/2026-09-05-eng039-merge-request.md`) — raised this pass (~03:41
UTC): code review, quality, and security all passed, round 1; devops's own
release-readiness hop found the project L1, held the readiness gate (no
blocking failure), then opened `restaurant-portal` PR #3. Two non-blocking
code-review findings plus an `EmailEditor` observation carried in the
request, and two pre-existing, out-of-scope gaps named prominently because
this ticket is what makes them reachable for the first time:
`BROADCAST_UNSUBSCRIBE_SECRET` not provisioned (every real send fails
loudly, logged, until fixed — one command closes it) and SMS delivery
entirely mocked (a real SMS-channel campaign step will silently report
`'sent'` while delivering nothing — an existing `proposals.md` row,
2026-09-03, corrected rather than duplicated). Full reasoning:
`agents/devops/notebook/2026-09-05-release-readiness-log.md`. This was the
`ENG-019` family's last sub-ticket. **Resolved, terminal.** A `watch
(launchd)` event pass's own step-5 re-check found PR #3 merged directly to
`main`, no written reply — full acceptance-check run, all 5 owned criteria
pass, carried `blocked → shipped → verified`, and, per the `ADR-003`-class
exemption `ENG-016` already used, made the parent `ENG-019` itself eligible
to close out the same way (`continue ENG-019` fired). **Off this list and
off the board entirely (terminal)**, item now in `inbox/_handled/`; see the
closing paragraph above and its own board file.

**`ENG-038`'s L1 merge request**
(`inbox/2026-09-04-eng038-merge-request.md`) — raised this pass (~21:06
PDT): code review (round 6), quality (round 6), security (round 2), and
the migration gate all passed; devops's own release-readiness hop found
the project L1, held the readiness gate (migration rollback already
tested; a live, currently-occurring but presently-inert observability gap
named — `ENG-037`'s cron has been firing every 5 minutes against this
ticket's not-yet-deployed function since that PR merged, harmless today
since no campaign has ever been created), then opened `aiorders-api` PR
#16. Five non-blocking findings carried in the request (a TOCTOU race on
the new interval check; a claimed-row-stuck edge case; `cancel_broadcast`
not reaching already-claimed rows; `enrollAudience`'s untested cross-tenant
scoping; `ENG-036`'s still-open shared auth bypass). Unblocks `ENG-039`
once merged. **Resolved, terminal.** This `scheduled` pass's own step-5
re-check found PR #16 merged directly to `main`, no written reply — full
acceptance-check run, all 7 owned criteria pass, carried
`blocked → shipped → verified`. **Off this list and off the board entirely
(terminal)**, item now in `inbox/_handled/`; see the closing paragraph above
and its own board file.
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
fresh G1** (`inbox/_handled/2026-09-03-eng027-g1-rescope.md`) — raised
2026-09-03 (~13:15): recommended building the approver's version now, one
ticket, carrying four riders (a concrete number for the "x hours"
placeholder, proposed 24h; the still-open earn-% base rider from the first
G1, not dropped for going unanswered; which rate applies now that
placement and accrual are hours apart; whether the order's own status
column becomes the completion signal). **Answered approved**
(2026-09-05T17:01:12), no additional comment, and processed by this
`decision` event pass — all four riders adopted exactly as proposed,
`awaiting-scope → designed`, `owner: approver → architect`, PRD `status:
approved`, handed to the architect for the tech design, `continue ENG-027`
fired. Full reasoning: `ENG-027`'s own board-file log,
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
`blocked → shipped → verified`.

**`ENG-034`'s L1 merge request — resolved, terminal.** Raised by the
`continue ENG-034` dispatch above, immediately after its own `ready-to-ship`
hop (code review round 1, quality round 1, security round 1, all `pass`):
the `ENG-016` family's last sub-ticket, the public-form dish picker.
Project registered L1, so no window check; devops's own readiness checks
(rollback/observability/cost) found no blocker, and no auto-deploy workflow
exists on `origin/main` either. Opened `config-site-builder` PR #4
(https://github.com/harsimranwalia/config-site-builder/pull/4), carrying
four non-blocking code-review findings and two named pre-existing,
non-security-relevant conditions in its own "Named gaps" section
(visibility only, not a gate condition — same shape `ENG-033`'s own request
already set as precedent). **This `watch (launchd)` event pass's own step-5
re-check found PR #4 merged directly to `main`, no stacking, no written
reply.** Receipts re-verified fresh, all `pass`, no migration owed; full
acceptance-check run (not the receipt-bookkeeping shortcut) and all eight
owned criteria confirmed pass — carried `blocked → shipped → verified`.
**Off this list and off the board entirely (terminal)**, item now in
`inbox/_handled/`; see the closing paragraph above,
`agents/devops/releases/2026-09-04-config-site-builder-ENG-034.md`, and
`agents/product-manager/notebook/2026-09-04-acceptance.md`. Unblocked
`ENG-016` itself for its own `ADR-003`-class shipped exemption —
`continue ENG-016` fired this same pass.

**`ENG-016`'s own continue-to-Piece-2 question — new, open.** That
`continue ENG-016` dispatch carried the parent `building → shipped →
verified` (`ADR-003`-class exemption, acceptance-check run in full, all 13
criteria pass — see the closing paragraph above and
`agents/product-manager/notebook/2026-09-04-eng016-acceptance.md`). Step 6b's
bar for auto-filing the PRD's own next item (Piece 2, catering pricing/
price-book) wasn't met — this ticket's G1 ("Lets start with piece 1")
confirmed build order, not a sequence sign-off — so a targeted question was
raised instead of a ticket:
`inbox/2026-09-04-eng016-continue-piece2-question.md`. Bundles two things:
whether to proceed to Piece 2 at all, and — a second condition the PRD's own
Recommendation section names independently of 6b — who maintains each
restaurant's price book, since Piece 2 is held on that regardless of the
sequence answer. **Zero items remain open in this section beyond
`ENG-027`, `ENG-028`, and this one at the time it was written** — since
superseded, see `ENG-037`'s own paragraph below.

**`ENG-037`'s L1 merge request — new, open.** Raised by the `continue
ENG-037` dispatch (`inbox/2026-09-04-eng037-merge-request.md`, ~12:33 UTC):
schema-only migration for `ENG-019`'s broadcast feature (three new tables,
five indexes, a `broadcast-dispatch-tick` `pg_cron` job), sub-ticket 1 of 3,
`ENG-038`/`ENG-039` both waiting on it. Code review, quality, security, and
the migration plan all passed round 1; devops's own release-readiness hop
found the project L1 (window check skipped), rollback actually tested
against a disposable container, cost `$0/month`. Opened `aiorders-api` PR
#15. One precise, non-blocking observability finding carried in the PR
body's own "Uncertainties" section: the cron tick calls `net.http_post`
unconditionally rather than checking for pending work first, so a
pre-`ENG-038` 404 window exists distinct from the already-documented
post-`ENG-038` 401 one — harmless today (no auto-deploy on this repo,
nothing external reaches the path yet) but named so the resulting log noise
isn't later mistaken for a regression. Full reasoning:
`agents/devops/notebook/2026-09-04-release-readiness-log.md`. **Zero items
remain open in this section beyond `ENG-027`, `ENG-028`, and this one at the
time it was written** — since superseded, see `ENG-038`'s own paragraph
above.

**This `scheduled` sweep's own step-5 merge detection (this pass) now finds
`ENG-037` merged too** — `aiorders-api` PR #15, base `main`, no stacking,
`mergedAt: 2026-09-04T21:19:18Z`, about 1h40m after the prior `watch` pass
checked and found it still open. Receipts re-verified fresh (all four
`pass`), one file/148 lines matching exactly, no drift — carried
`blocked → shipped → verified` this pass via the same receipt-bookkeeping
route `ENG-031` set (0 of the parent's acceptance criteria apply to a
schema-only diff). **New this pass:** this host's newly-discovered linked
`supabase` CLI confirmed the migration and its cron job are actually live
in production (not just merged to `main`) — all three tables and
`broadcast-dispatch-tick` (`active`, 5-minute schedule) present in
`bmnmnejwdxbcqinqkwko`. That also confirms the pre-`ENG-038` observability
gap named non-blocking at release-readiness is now actually firing every 5
minutes, not merely a named risk — still non-blocking, see
`agents/devops/releases/2026-09-04-aiorders-api-ENG-037.md`. Satisfies
`ENG-038`'s sole dependency (`depends_on: [ENG-037]`) — this pass fired
`continue ENG-038` rather than building it inline, same handoff shape every
`ENG-031`→`ENG-034` and `ENG-019`'s own sub-tickets have already used.
`ENG-039` still waits on `ENG-038` in turn.

**`ENG-020`'s L1 merge request — new, open.** Raised by this pass
(`inbox/2026-09-05-eng020-merge-request.md`, ~13:40 local): code review (3
rounds, pass), quality (3 rounds, pass, all 5 acceptance criteria), security
(round 1, pass), and the migration gate (pass, rollback tested against a
disposable replica) all passed on both repos; devops's own release-readiness
hop found both projects L1 (window check skipped for both), held the
readiness gate (rollback/observability/cost all clear, $0/month, no new
dependency), then opened `aiorders-api` PR #17 and `restaurant-portal` PR #4
and raised this single two-repo request. One non-blocking security finding
(a pre-existing, shared restaurant-existence oracle) and several by-design,
not-a-gap limitations (cross-domain attribution coverage varies per
restaurant; no historical baseline) carried in the request rather than
hidden; `ENG-030` (the unrelated `analytics` P0 this ticket's design work
surfaced) is named as filed-and-resolved separately, not touched by this
diff. Full reasoning: this ticket's own board-file log and
`agents/devops/notebook/2026-09-05-release-readiness-log.md`. Design's
recommended merge order is `aiorders-api` first, but either order is safe —
the portal renders a tested "not available yet" state if it ships first.

## 2026-09-05 — continue (`ENG-020`): release-readiness — `ready-to-ship → blocked`, both PRs opened

`continue` event pass, context `ENG-020`, per prior pass's own
`chained: ENG-020`. Reading map for `continue`: steps 6 and 6b, plus the
not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
lanes*; *Guards*). Mode check clean (repo-root `.env` → `MODE=active`).
Ticket's own log and frontmatter read fresh before touching anything: clean
history, no stale `blocked_from`, no hold-priority conflict, all four
upstream gate receipts present and passing. Acted as `devops` on this hop,
per `skills/release-runner/SKILL.md` (no delegation to a subagent).

**Step 1 (window):** both `aiorders-api` and `restaurant-portal` are L1
(`config/projects.md`, re-confirmed directly) — no window check applies to
either.

**Step 2 (upstream gates) — all four re-read fresh from the receipt files,
not from the ticket log's own account, all passing:**
`agents/principal-engineer/reviews/ENG-020.md` (round 3, pass, third
consecutive), `agents/qa/test-plans/ENG-020.md` (round 3, pass, all 5 ACs),
`agents/security/reviews/ENG-020.md` (round 1, pass), and
`agents/database/migrations/ENG-020-marketing-roi-attribution-reporting.md`
(pass, rollback tested against a disposable replica).

**Step 3 (readiness gate):**

- *Rollback:* the migration's own `DROP FUNCTION` was actually run against a
  disposable Postgres replica, not just asserted. Neither repo's code diff
  changes existing behaviour — `restaurant-portal`'s `deploy-cf.yml`
  (push-to-`main`-triggered) redeploys the prior build on a revert, same
  reasoning `ENG-032`'s/`ENG-039`'s own release-readiness hops already
  established for this exact repo; `aiorders-api` has no CI (confirmed:
  `git ls-tree -r origin/main --name-only | grep -i workflow` empty), so
  reverting the merge is sufficient there too.
- *Observability:* RPC failures log server-side (`console.error`) before
  returning a generic client message (security review, A09); the
  RPC-missing branch is an explicit, tested case
  (`acquisition.test.ts` — "reports the RPC-missing case distinctly"), not a
  silent gap the way `ENG-039`'s two dormant findings were. Nothing new to
  name.
- *Cost:* $0/month — no new dependency in either repo (`git diff --stat --
  '*.json' '*.lock'` empty in both, confirmed fresh), one new Postgres
  function on already-running infrastructure, no new service.
- *Window:* n/a, both L1.

No blocking readiness failure.

**Step 4 (route):** worktrees re-checked fresh before anything else: `git
fetch origin` both repos. `aiorders-api` HEAD `cd82579` (0 behind, 1 ahead of
`origin/main`, matching every gate's own cited commit); `restaurant-portal`
HEAD `5783a2d` (0 behind, 3 ahead, matching round 3's own checkpoint). No
drift, no prior pass died mid-work. `gh pr list --head
feat/ENG-020-marketing-roi-attribution-reporting --state all` confirmed no
PR already existed on either repo. Diff stat: `aiorders-api` 7 files/695
insertions/1 deletion; `restaurant-portal` 9 files/567 insertions.

Opened `aiorders-api` PR #17
(https://github.com/harsimranwalia/aiorders-api/pull/17) and
`restaurant-portal` PR #4
(https://github.com/harsimranwalia/restaurant-portal/pull/4). Each body
carries what's new, all four gates' receipt paths, the self-test summary,
the one non-blocking security finding, and a "known limitations at merge
time" section naming the by-design attribution-coverage/no-baseline caveats
and `ENG-030` (unrelated, filed separately). Wrote
`inbox/2026-09-05-eng020-merge-request.md`, `pr_urls:` list (two repos, per
`ENG-011`'s own corrected precedent — never one item per repo, never a
delimited string). `lib/eng-notify.sh raise` run — `sent: active
2026-09-05-eng020-merge-request.md` at `13:40:18`,
`traces/eng-notify-2026-09-05.log`; stamped `notified: 2026-09-05T13:40:18`
on the item, copied verbatim from the log (this board's own
already-flagged local-time-labeled-as-UTC convention, unchanged here).

Ticket set `blocked`, `blocked_on: approver`, `blocked_from: ready-to-ship`,
`owner: devops → approver`, `links.pr` set (nested map, both repos). No G3 —
L1 has none; the PR merge is the human gate. No release record yet — L1's
actual deploy and the release record both wait for merge detection on a
future pass, per the skill's own step 4 L1 row / step 7 split.

**1 transition** (`ready-to-ship → blocked`), well under the cap of 4.
**Consequence:** ticket leaves the counted `ready`..`ready-to-ship` machine-WIP
range — **machine WIP `1/1 → 0/1`, free** — but keeps its approver-facing
slot per the Guards section ("a ticket `blocked` on `blocked_on: approver`...
holds its slot there too"); moot on this instance since
`wip.approver_limit: unlimited`, but recorded for the record regardless.

**Dead-end sweep (scoped to this event):** no other ticket touched — a
`continue` event's own narrower contract (resume the named ticket, don't
sweep the board). **Notify sweep:** the new gate item raised and stamped
above; both other open `inbox/` items re-read fresh (`eng028`:
`notified: 2026-09-03T16:10:27`, `nudged: 2026-09-04T09:13:37`; `eng016`'s
Piece-2 question: `notified: 2026-09-04T10:58:06`, `nudged:
2026-09-05T09:31:45`) — both already carry their one-ever `nudged:`, neither
carries a `decision:`, neither re-nudged. **Observations/exceptions:** none
filed — no `exception-request:` found, nothing noticed outside this ticket's
own scope. **Journal:** n/a, no G1/G2/G3 or merge request answered this pass
(this pass raised one; it has not been answered yet).

**Board update:** In-flight row (`state: ready-to-ship → blocked`,
`owner: devops → approver`, `links` populated), `updated` date unchanged
(same day). "Waiting on the approver" header count and list updated (two →
three items open), new paragraph added for this ticket's own merge request.
Live file held three dated entries before this one (satisfied by an earlier
round's own roll); oldest (`continue (ENG-020): fix hop for round-2 quality
gap (Gap 4)`) rolled to `_index-archive.md` per the keep-three rule.

Post-pass `eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both exit
0, clean.

`chained: none` — `blocked`, `blocked_on: approver`, is the approver-waiting
no-chain condition (`eng_build_loop.md` step 9 / "The chain"). Re-check via
a `decision` (if the approver replies to the merge request) or the next
`scheduled`/`watch` pass's own step-5 merge detection (if either PR merges
directly on GitHub with no written reply, the pattern every prior L1 merge
request on this board has actually followed).

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.

## 2026-09-05 — continue (`ENG-020`): review+quality combined hop, round 3 — BOTH PASS — `building → in-security`

`continue` event pass, context `ENG-020`. Reading map: steps 6 and 6b, plus
the not-negotiable set. Mode clean (`MODE=active`). Ticket's own log/
frontmatter read fresh: clean, round-2 receipts present. Post-pass
`eng-gate-check.sh`, scoped and whole-board: both exit 0. Acted as
principal-engineer and qa on this combined hop, same standing pattern.

Scoped to the diff since round 2's reviewed commit
(`restaurant-portal@f129f14..5783a2d`, 1 file/25 lines — three new
`it()` blocks in `Index.test.tsx`, no production code; `aiorders-api`
unchanged, not re-reviewed). **Code review: PASS, round 3, third
consecutive pass** — 0/10 automatic failures; both new assertions
mutation-tested (the `low_volume` conditional and the coverage-sentence
percentage), each catching exactly the one test it should. Full narrative:
`agents/principal-engineer/reviews/ENG-020.md`.

**Quality gate: PASS, round 3.** Fresh re-check of the whole acceptance
table, not just Gap 4's confirmation. AC1–3/AC5 stand from round 2; AC4's
last open piece (the always-rendered coverage percentage and the
low-volume caveat, design's own "Attribution honesty" mechanism 4) closes
this round. **All five acceptance criteria now pass.** Full detail:
`agents/qa/test-plans/ENG-020.md`.

Per `code-review-gate/SKILL.md` step 9, both gates passing on the same
diff: **`building → in-security`, owner `eng-manager → security`.** 1
transition, well under the cap of 4 — security is the next session's own
work, per this document's "a pass stops after `building` on purpose."
Machine WIP unaffected — `in-security` is still inside the counted
`ready`..`ready-to-ship` range, still `ENG-020`'s own slot.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing raised (internal machine-gate round); `eng028`
and `eng016`'s Piece-2 question both re-read fresh, both already carry
their one-ever `nudged:`, neither re-nudged. No observations/exceptions
filed this pass.

**Board update:** In-flight row (`state: building → in-security`,
`owner: eng-manager → security`). Live file held three dated entries
before this one — oldest (`continue (ENG-020): fix hop for round-1 quality
gaps`) rolled to `_index-archive.md` per the keep-three rule.

`chained: ENG-020` — `in-security` is agent-owned (security), not the
approver, not blocked, not terminal, not held by a cap. Fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-020` before this pass exits.

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.

## 2026-09-05 — continue (`ENG-020`): security gate, round 1 — PASS — `in-security → ready-to-ship`

`continue` event pass, context `ENG-020`. Reading map: steps 6 and 6b, plus
the not-negotiable set. Mode clean (`MODE=active`). Pre-pass/post-pass
`eng-gate-check.sh`, scoped and whole-board: all four runs exit 0. Worktrees
re-fetched fresh, no drift in either repo. Acted as `security` on this hop,
per `skills/security-gate/SKILL.md` (no delegation to a subagent).

Threat-modelled the change, walked OWASP A01–A10 against the full diff in
both repos (read `acquisition.ts`, `channels.ts`, the migration, `index.ts`'s
auth block, `utils.ts`'s actual `verifyRestaurantAccess` signature, and both
new frontend files directly off disk), confirmed the LLM checklist n/a
(`touches_models: false`, independently verified), scanned for secrets (diff
+ full branch history, both repos: zero hits) and dependencies (zero new or
bumped), and read the negative-case tenant-isolation test directly rather
than trusting the receipts' own account of it. Full reasoning:
`agents/security/reviews/ENG-020.md`.

**Verdict: PASS.** No blocking finding. Access control uses the correct
`verifyRestaurantAccess(restaurant_id, supabase, user)` call shape (matching
`menus.ts`/`catering.ts`/`restaurants.ts`/`onlineOrders.ts`, not the broken
shape `feedback.ts`/`offers.ts` carry), checks `.hasAccess` before any query,
mutation-verified in code review rather than merely read-and-trusted. New RPC
fully parameterised; frontend renders exclusively via JSX text interpolation
(zero `dangerouslySetInnerHTML`/`innerHTML`), so the one attacker-reachable
text (public-signup-supplied `first_touch_source`, surfaced as an
`other:<source>` channel label when unrecognised) is stored-but-inert, not
stored XSS. No secret, no new dependency.

**One non-blocking finding:** `verifyRestaurantAccess` (unchanged by this
diff, shared by every other `brand-portal` handler) answers an existence
question the design's own Interfaces table says a denial doesn't — a
restaurant that doesn't exist gets `'Restaurant not found'`, one that exists
but isn't the caller's gets `'Access denied to this restaurant'`, and
`acquisition.ts` forwards `access.error` verbatim. Pre-existing, shared
verbatim by every sibling handler, not introduced or worsened here, low
exploit value (a restaurant UUID isn't a credential). Not filed as a
proposal — narrower than that bar; logged for the record:
`agents/security/notebook/2026-09-05-findings.md`.

Receipt written **only on this pass verdict** per the gate's own "no receipt
on fail" rule (`agents/security/reviews/ENG-020.md`), `links.security_review`
set on the ticket in the same edit. **1 transition** (`in-security →
ready-to-ship`), well under the cap of 4 — release readiness is the next
session's own hop. **Consequence:** no WIP-cap change — `ready-to-ship` is
still inside the counted `ready`..`ready-to-ship` range, still the ticket
holding the 1/1 machine-WIP slot. Owner `security → devops`.

**Dead-end sweep (scoped to this event):** no other ticket touched. **Notify
sweep:** nothing raised (a machine-gate verdict, not approver-facing — the
eventual G3 is `release-runner`'s own job at the next hop); `eng028` and
`eng016`'s Piece-2 question both re-read fresh, both already carry their
one-ever `nudged:`, neither re-nudged. No observations/exceptions filed —
the one finding above is a security-notebook entry, not an observation or a
proposal.

**Board update:** In-flight row (`state: in-security → ready-to-ship`,
`owner: security → devops`). Live file held three dated entries before this
one — oldest (`continue (ENG-020): review+quality combined hop, round 2`)
rolled to `_index-archive.md` per the keep-three rule.

`chained: ENG-020` — `ready-to-ship` is agent-owned (`devops`, via
`release-runner/SKILL.md`), not the approver, not blocked, not terminal, not
held by a cap. Fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-020` before this pass exits.

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.
