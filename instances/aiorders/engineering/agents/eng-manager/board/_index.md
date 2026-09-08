# Board

**Next ID: ENG-051** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.) `ENG-050` allocated this
pass — `finding` event, context `rpc-execute-grant-exposure`: a P0 carve-out
ticket (`schedules/eng_build_loop.md` step 3), not a proposal, for two
`aiorders-api` RPC functions (`calculate_platform_analytics`,
`get_acquisition_breakdown`) confirmed live-callable by `anon` in
production. Full reasoning: `ENG-050`'s own board-file log and the dated
pass entry below. `ENG-048`–`ENG-049` allocated an earlier pass —
`ENG-027`'s own `work-breakdown` run, two sub-tickets
(database/backend, both `aiorders-api` — no `frontend` sub-ticket, the
design's own Rollout section states no frontend calls any of this yet),
sequenced as a strict chain (`ENG-048` → `ENG-049`). Full reasoning:
`ENG-027`'s own board-file log and
`agents/eng-manager/notebook/2026-09-07-eng027-work-breakdown.md`.
`ENG-044`–`ENG-047` allocated an earlier pass — `ENG-026`'s own
`work-breakdown` run, four sub-tickets this time
(database/backend/frontend×2 — `frontend` splits across `aiorders-admin-hub`
and `restaurant-marketplace`, the two-repos-one-surface shape `ENG-016`'s own
family used first), sequenced as a DAG rather than a single chain. Full
reasoning: `ENG-026`'s own board-file log and
`agents/eng-manager/notebook/2026-09-07-eng026-work-breakdown.md`. `ENG-043`
allocated an earlier pass — not new feature scope, but a home for the
intake-question raised
against a garbled control-center submission whose title cited `ENG-011`
but may have meant `ENG-028` (see the ticket's own Notes and
`inbox/2026-09-06-eng043-stage-names-clarification.md`, unanswered); held
at `intake`, no PRD, per PM agent.md's "don't write a PRD around a problem
you can't state." `ENG-042` allocated the immediately preceding pass — the
autopilot ask split out of `ENG-028`'s own `changed` G1 answer, its own new
ticket rather than folded into `ENG-028` or `ENG-017`. `ENG-040`–`ENG-041`
allocated an earlier pass — `ENG-021`'s own `work-breakdown` run, one
sub-ticket per owning agent (backend/frontend; no `database` ticket — this
design has no schema change). In-flight row and this counter both updated
in the same edit the tickets were filed, not left for a later sweep.

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

**`ENG-020`'s own release-readiness hop freed the slot again the same day —
this `scheduled` pass picked `ENG-021`.** `ENG-020` left the counted
`ready`..`ready-to-ship` range at its `ready-to-ship → blocked` hop (both PRs
opened, waiting on the approver); the `watch (launchd)` pass in between swept
inboxes and re-checked that ticket's own merge status but, correctly per its
own narrower reading map, did not pick a replacement. This pass re-checked
the To-do column fresh and found nothing machine-actionable again (`ENG-018`
held; `ENG-028`'s G1 still unanswered), so the pick again came from the
held-for-slot pool: `ENG-021`, `ENG-026` and `ENG-027` all carry `priority:
now` and a completed design with no one-way door; lowest id decided.
`ENG-021`'s own routing (`ready`, `owner: eng-manager`, no G2) was already
determined by its 2026-09-03 design pass and only re-confirmed here, not
re-derived. **Machine WIP: `0/1 → 1/1`**, `ENG-021` `designed → ready`,
`owner: architect → eng-manager`. Stopped there — building is new
implementation work, chained instead (`continue ENG-021`). `ENG-026` and
`ENG-027` stay `designed`, correctly capped again the moment `ENG-021`
claimed the slot. **Also fixed while sweeping this dispatch:** `ENG-028`'s
In-flight row carried a blank `priority` cell despite its own frontmatter
reading `now` — corrected; no functional consequence (it was already
excluded from the pool by state, not priority), but left wrong it misleads a
reader. Full reasoning: `ENG-021`'s own board-file log.

**`ENG-021` ran `work-breakdown` this pass (`ready → building`, no diff of its
own — see its own `## Breakdown` section) and decomposed into two
sub-tickets, `ENG-040`–`041`, one per owning agent (backend/frontend; no
`database` ticket — this design has no schema change, only a read-only
verification folded into `ENG-041`'s own build hop).** Same WIP-family
reading `ENG-016`'s and `ENG-019`'s own decompositions already established:
the slot is held by the ticket family, not by each row separately, so this
is still `1/1`, not `2/1`. `ENG-040` (backend, no dependency) dispatched
straight to `building`; `ENG-041` (frontend) stays `ready`, waiting on its
unmet `depends_on: [ENG-040]`. Full reasoning:
`agents/eng-manager/notebook/2026-09-05-eng021-work-breakdown.md`.

**This `scheduled` pass's own step-5 re-check finds `ENG-040` merged too** —
`aiorders-api` PR #18, base `main`, no stacking, `mergedAt:
2026-09-06T16:11:40Z`, no written reply. All three gate receipts re-read
fresh and confirmed `pass`; no migration owed. Full `acceptance-check` run
(AC4/AC5 in full, AC3's write half — this ticket's owned share of `ENG-021`'s
PRD); `brand-portal` confirmed actually redeployed, not just merged. Carried
`blocked → shipped → verified` — the `ENG-021` family's first sub-ticket now
terminal. Satisfies `ENG-041`'s sole dependency — this pass fired `continue
ENG-041` rather than building it inline, same handoff shape every prior
work-breakdown family on this board has used. **Machine WIP unaffected —
still `1/1`, held by the `ENG-021` family** (`ENG-021` parent still
`building`, waiting on `ENG-041`, the family's last child).

**This `scheduled (launchd)` 02:00 pass's own step-5 re-check finds
`ENG-041` merged too** — `restaurant-portal` PR #5, base `main`, no
stacking, `mergedAt: 2026-09-07T06:18:50Z`, no written reply. All three gate
receipts (review round 2, quality, security) re-read fresh and confirmed
`pass`; no migration owed; zero drift (`git diff 01c6ddb origin/main
--stat` empty). **Confirmed actually deployed**, not just merged: the
push-triggered "Deploy to Cloudflare Pages" run at this commit completed
successfully 3 seconds after the merge. **Full `acceptance-check` run** —
this ticket owns AC1, AC2, AC6 in full plus AC3's UI half, the last of
`ENG-021`'s six criteria not yet independently checked; all 4 owned
criteria pass, including a fresh, code-level re-confirmation (not taken on
the review log's word) that round 1's cross-restaurant FAQ-draft leak fix
is present in the actual shipped tip. Carried `blocked → shipped →
verified` this pass — the `ENG-021` family's second and last sub-ticket now
shipped. Full walk:
`agents/product-manager/notebook/2026-09-07-eng041-acceptance.md`; release
record: `agents/devops/releases/2026-09-07-restaurant-portal-ENG-041.md`.
Both of `ENG-021`'s children are now settled — the parent's own
`ADR-003`-class exemption is satisfied. Not processed inline this pass
(same precedent `ENG-016`'s and `ENG-019`'s own last-child-found passes
already set — the parent's no-diff shipped transition gets its own
dedicated hop); `continue ENG-021` fired instead. That fire queued behind
this same pass's own single-flight lock
(`traces/eng-loop-2026-09-07.log`, `02:08:51 continue — pass in flight,
queued as pending`) rather than launching immediately — expected, since
this pass itself still held the lock at that moment — and will drain the
moment this pass exits. **Machine WIP unaffected — still `1/1`, held by the
`ENG-021` family** (`ENG-021` parent still `building` until its own
chained pass carries it to `shipped`).

**That queued fire is this pass's own predecessor state, now resolved:
`ENG-021` itself carried `building → shipped → verified`**, `ADR-003`-class
exemption (both children settled, both actually shipped), acceptance-check
run in full despite the exemption — all 6 PRD criteria pass, cross-referenced
from `ENG-040`'s and `ENG-041`'s own already-full walks, zero drift on
either repo since. See
`agents/product-manager/notebook/2026-09-07-eng021-acceptance.md` and the
ticket's own board-file log. **Machine WIP: `1/1 → 0/1`, free** — the whole
`ENG-021` family is now terminal.

**Per `eng_build_loop.md` Guards → Machine WIP limit, amended 2026-09-06
("never idle"), this same pass filled the freed slot rather than leaving it
for the next dispatch-scoped pass** — the first time this board has applied
that amendment to a parent's own closing hop (`ENG-016`'s and `ENG-019`'s
own closures both predate the amendment and left the pick to a later
`scheduled` sweep). To-do column swept fresh: `ENG-018`, `ENG-028`,
`ENG-042` and `ENG-043` are the only occupants, and all four are genuinely
on an unanswered approver question (`grep -l "^decision:" inbox/*.md`
returns nothing) — nothing there is startable. Fell back to the
held-for-slot pool, same precedent `ENG-019`'s, `ENG-020`'s and `ENG-021`'s
own prior dispatches already set: `designed` tickets with a completed
design and no one-way door, deferred only by the cap. `ENG-026` and
`ENG-027` both carry `priority: now`; lowest id decided. **Machine WIP:
`0/1 → 1/1`**, `ENG-026` `designed → ready`, `owner: architect →
eng-manager`, no G2 (routing per `tech-design/SKILL.md` step 11, already
determined 2026-09-03 — no one-way door). Stopped there — work-breakdown/
building is new implementation work, chained instead (`continue ENG-026`).
`ENG-027` stays `designed`, correctly capped again the moment `ENG-026`
claimed the slot. Full reasoning: `ENG-021`'s and `ENG-026`'s own
board-file logs.

**`ENG-026` ran `work-breakdown` this pass (`ready → building`, no diff of
its own — see its own `## Breakdown` section) and decomposed into four
sub-tickets, `ENG-044`–`047`, sequenced as a DAG rather than a single
chain.** `ENG-044` (database, `aiorders-api`) has no dependency; `ENG-045`
(backend, `aiorders-api`) and `ENG-046` (frontend, `aiorders-admin-hub`) both
depend on `ENG-044` alone and are independent of each other; `ENG-047`
(frontend, `restaurant-marketplace`) depends on `ENG-045`. `frontend` splits
into two sub-tickets across two repos — the same two-repos-one-surface shape
`ENG-016`'s own family (`ENG-032`/`ENG-034`) used first, not a new call. Same
WIP-family reading `ENG-016`'s/`ENG-019`'s/`ENG-021`'s own decompositions
already established: the slot is held by the ticket family, not by each row
separately, so this is still `1/1`, not `2/1`. `ENG-044` (no dependency)
dispatched straight to `building`; `ENG-045`, `ENG-046`, and `ENG-047` stay
`ready`, each waiting on its own unmet `depends_on`. Full reasoning:
`agents/eng-manager/notebook/2026-09-07-eng026-work-breakdown.md`.

**This `continue ENG-026` pass found `ENG-044` at `shipped`** — its
frontmatter changed `blocked → shipped` between two reads seconds apart
(the control center writing the merge-detected transition live, mid-pass);
confirmed genuine rather than trusted off either read, via `gh pr view 19`
(`MERGED`, `mergedAt: 2026-09-07T16:03:56Z`) and `git merge-base
--is-ancestor` against `origin/main` from the dedicated worktree. Clears
`depends_on: [ENG-044]` for `ENG-045` and `ENG-046` both (Guards, "two
readings closed" (a) — `shipped` is past the `blocked_on: approver`-plus-PR
bar). This ticket's own work-breakdown notebook had already anticipated
two children becoming simultaneously startable and named the tie-break in
advance; dispatches exactly one: `ENG-045` — lower id, unblocks `ENG-047`
downstream, no reason found to deviate. `ENG-046` stays `ready`, its turn
deferred to a future pass; `ENG-047` stays correctly blocked
(`depends_on: [ENG-045]` unmet). Machine WIP unaffected — still `1/1`, held
by the `ENG-026` family. `continue ENG-045` fired. Full reasoning:
`agents/eng-manager/notebook/2026-09-07-eng026-child-dispatch.md` and the
ticket's own board-file log.

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
| ENG-018 | Sales demonstration account — a fully seeded AIOrders environment to show prospects | aiorders-admin-hub | awaiting-scope | now | approver | L | 2026-09-06 |
| ENG-023 | Add status and internal notes to each brand-portal feedback item | restaurant-portal | designed | | architect | S | 2026-08-31 |
| ENG-025 | Recurring feedback issues, per restaurant, over time | restaurant-portal | designed | | architect | S | 2026-09-04 |
| ENG-027 | Loyalty points ledger, balances, and earn API — online-order and dine-in accrual | aiorders-api | building | now | eng-manager | L | 2026-09-07 |
| ENG-048 | Loyalty ledger schema, credit function, and auto-complete cron | aiorders-api | blocked | | approver | S | 2026-09-07 |
| ENG-049 | Loyalty accrual — webhook handler, auto-complete sweep, and dine-in earn API | aiorders-api | blocked | | approver | M | 2026-09-07 |
| ENG-028 | Foodswipe funnel — hardcoded nine-stage pipeline (rescoped) | aiorders-admin-hub | awaiting-scope | now | approver | M | 2026-09-06 |
| ENG-042 | Foodswipe funnel — stage-triggered autopilot email/SMS | aiorders-api | awaiting-scope | | approver | L | 2026-09-06 |
| ENG-029 | Autopilot API has no restaurant-ownership check on any of its 8 actions — cross-tenant customer-data exposure | aiorders-api | designed | | architect | M | 2026-09-04 |
| ENG-030 | `analytics` edge function has no authentication or authorization at all — cross-tenant revenue/order/customer exposure | aiorders-api | designed | | architect | S | 2026-09-04 |
| ENG-035 | `autopilot`'s system-triggered marketing actions skip authentication entirely — client-controlled flag reaches a real message-send trigger | aiorders-api | designed | | architect | S | 2026-09-04 |
| ENG-036 | `outgoing-communications` skips authentication entirely for any system-triggered send — cross-actor unauthenticated message dispatch | aiorders-api | designed | | architect | S | 2026-09-04 |
| ENG-050 | Two production RPC functions grant `EXECUTE` to `anon`/`authenticated` — unauthenticated platform-analytics and acquisition-breakdown exposure | aiorders-api | designed | | architect | S | 2026-09-07 |
| ENG-043 | Clarify which ticket "stage names" belongs to before shaping (ENG-011 or ENG-028) | aiorders-admin-hub | intake | | product-manager | | 2026-09-06 |

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

**`ENG-020` joins the terminal group too, found by this `scheduled` pass's
own step-5 re-check.** Not part of any work-breakdown family — a standalone
two-repo ticket. `aiorders-api` PR #17 and `restaurant-portal` PR #4 merged
directly to `main`, 94 seconds apart, no stacking, no written reply. Zero
drift confirmed (`git diff {reviewed-tip} origin/main --stat` empty on both;
each merge commit's own parents show the reviewed tip merged in as-is). All
four gate receipts re-read fresh and confirmed `pass`. **Full
`acceptance-check` run** — this ticket owns all 5 of its own PRD's criteria,
no schema-only carve-out applies. Both sides confirmed actually deployed,
not just merged: `aiorders-api`'s `brand-portal` function redeployed ~4
minutes after merge (by hand, no tracked workflow); `restaurant-portal`'s
own push-triggered Cloudflare Pages workflow completed ~90 seconds after
merge. All 5 criteria pass — carried `blocked → shipped → verified` this
pass; see its own board-file log,
`agents/product-manager/notebook/2026-09-05-eng020-acceptance.md`, and
`agents/devops/releases/2026-09-05-ENG-020-aiorders-api-and-restaurant-portal.md`.
**Off the In-flight table (terminal).** `blocks: []` — nothing unblocked,
nothing chained as a consequence. Machine WIP unaffected throughout — this
ticket left the counted `ready`..`ready-to-ship` range at its own prior
`ready-to-ship → blocked` hop, well before this pass; the slot has been held
by the `ENG-021` family the whole time (`ENG-021` still `building`).

**`ENG-040` joins the terminal group too, found by this `scheduled` pass's
own step-5 re-check.** `ENG-021`'s first sub-ticket. `aiorders-api` PR #18
merged directly to `main`, no stacking, no written reply. Zero drift on this
ticket's own diff — the one file changed beyond the reviewed tip
(`README.md`) is `ENG-020`'s own already-verified addition landing via
`main`'s other merge parent, not this ticket's. All three gate receipts
re-read fresh and confirmed `pass`; no migration owed. **Full
`acceptance-check` run** — this ticket owns AC4/AC5 in full plus AC3's write
half of `ENG-021`'s PRD, per the work-breakdown's own AC-mapping (neither
child owns AC3 alone). Confirmed actually deployed, not just merged:
`brand-portal` redeployed (version 84) ~18 minutes after merge. All 3 owned
criteria pass — carried `blocked → shipped → verified` this pass; see its
own board-file log, `agents/product-manager/notebook/2026-09-06-eng040-acceptance.md`,
and `agents/devops/releases/2026-09-06-aiorders-api-ENG-040.md`. **Off the
In-flight table (terminal).** `blocks: [ENG-041]` — that ticket's sole
`depends_on` is now satisfied; `continue ENG-041` fired this same pass
rather than building it inline (same handoff shape every prior
work-breakdown family has used). Machine WIP unaffected — this ticket left
the counted `ready`..`ready-to-ship` range at its own prior
`ready-to-ship → blocked` hop; the slot is still held by the `ENG-021`
family (`ENG-021` still `building`, one child — `ENG-041` — left).

**`ENG-041` joins the terminal group too, found by this `scheduled` pass's
own step-5 re-check.** `ENG-021`'s second and last sub-ticket. `restaurant-portal`
PR #5 merged directly to `main`, no stacking, no written reply. Zero drift
on this ticket's own diff (`git diff 01c6ddb origin/main --stat` empty —
the merged tree matches the QA-reviewed tip exactly). All three gate
receipts re-read fresh and confirmed `pass`; no migration owed. **Full
`acceptance-check` run** — this ticket owns AC1, AC2, AC6 in full plus AC3's
UI half of `ENG-021`'s PRD, per the work-breakdown's own AC-mapping.
Confirmed actually deployed, not just merged: the push-triggered "Deploy to
Cloudflare Pages" run at the merge commit completed successfully 3 seconds
after the merge. All 4 owned criteria pass, including a fresh re-read of
the actual shipped code confirming round 1's cross-restaurant FAQ-draft
leak fix is present — carried `blocked → shipped → verified` this pass; see
its own board-file log,
`agents/product-manager/notebook/2026-09-07-eng041-acceptance.md`, and
`agents/devops/releases/2026-09-07-restaurant-portal-ENG-041.md`. **Off the
In-flight table (terminal).** `blocks: []` — no other ticket directly
unblocked, but this was `ENG-021`'s last sub-ticket: both children now
settled, satisfying the parent's own `ADR-003`-class exemption. `continue
ENG-021` fired this same pass rather than processing the parent's own
no-diff shipped transition inline (same handoff shape `ENG-016`'s and
`ENG-019`'s own closing passes already used). Machine WIP unaffected —
still `1/1`, held by the `ENG-021` family until the parent's own chained
pass carries it to `shipped`.

**`ENG-021` itself joins the terminal group too, from the very next
`continue` pass its own predecessor fired.** `building → shipped →
verified`, `ADR-003`-class exemption (both children settled, both actually
shipped) — no diff, review, QA, or security hop of its own. Ran
`acceptance-check/SKILL.md` in full anyway (the trigger has no parent
carve-out): all 6 PRD criteria pass — cross-referenced from `ENG-040`'s and
`ENG-041`'s own already-full walks (both repos re-fetched fresh, zero drift
from the commits those walks checked), no gap to backfill, same shape
`ENG-019`'s own closing check found for its family. No scope creep, cost
`$0/month` as estimated — off the In-flight table (terminal); see its own
board file and
`agents/product-manager/notebook/2026-09-07-eng021-acceptance.md`. **Machine
WIP `1/1 → 0/1`, free.**

**Unlike `ENG-016`'s and `ENG-019`'s own closures, this slot did not sit
free for a later pass to notice.** `eng_build_loop.md` Guards → Machine WIP
limit, amended 2026-09-06 ("never idle") — applied here for the first time
to a parent's own closing hop, since the amendment post-dates both prior
closures. To-do column had nothing startable (`ENG-018`, `ENG-028`,
`ENG-042`, `ENG-043` all genuinely on an unanswered approver question,
confirmed against `inbox/` directly); fell back to the held-for-slot pool,
same precedent this family's own prior dispatches set: `ENG-026` and
`ENG-027` both `priority: now`, lowest id decided. **Machine WIP:
`0/1 → 1/1`** the same pass — `ENG-026` `designed → ready`, `owner:
architect → eng-manager`, no G2 (no one-way door). Stopped there —
work-breakdown/building is new implementation work, chained instead
(`continue ENG-026`). Full reasoning: `ENG-021`'s and `ENG-026`'s own
board-file logs and the header narrative above.

## Waiting on the approver

**No cap — `wip.approver_limit: unlimited` since 2026-09-02 (see header
above). Ten items currently open** (`ENG-048`'s new L1 merge request,
`ENG-049`'s new L1 merge request, `ENG-028`'s fresh rescope G1, `ENG-042`'s
new G1, `ENG-016`'s continue-to-Piece-2 question, `ENG-043`'s
intake-question, `ENG-018`'s G1, `ENG-050`'s P0 notice, `IDLE-2026-09-07`'s
"nothing I can start" notice —
see each one's own paragraph below — and `PROP-2026-W36`, the weekly
batched-proposal G1 (42 open rows from `proposals.md`); see the
"`PROP-2026-W36` arrived" dated entry, now in `_index-archive.md` per the
keep-three rule, for its full detail).
**`ENG-045`'s, `ENG-046`'s, and `ENG-047`'s L1 merge requests are off this
list, corrected this pass** — all three are `shipped` on their own board
files (`inbox/_handled/`), found stale here (still shown `blocked`/open)
while this pass was updating this same table for its own ticket; see each
one's own board file, not this section's paragraphs below, which were not
rewritten to match (flagged in `observations.md`, this date, rather than
rewritten in full here).
**`ENG-040`'s and `ENG-041`'s L1 merge requests are off this list** —
this `scheduled` pass's own step-5 re-check found both PRs merged with no
written reply (`ENG-040` an earlier pass the same day, `ENG-041` this one)
— see each one's own paragraph below and the closing paragraphs above.
`ENG-028`'s original G1 — answered **changed** (2026-09-06T09:09:08),
rescoped in place and re-raised as a fresh G1, see its own paragraph below
— is off this list in its original form.
`ENG-027`'s rescope G1 — answered **approved** (2026-09-05T17:01:12),
processed by a `decision` event pass, see its own paragraph below — and
`ENG-038`'s, `ENG-039`'s and now `ENG-020`'s own L1 merge requests — all
resolved by a `watch (launchd)` or `scheduled` pass's own step-5 re-check
finding their PRs merged with no written reply — are now off this list too,
the same way `ENG-008`/`ENG-009`/`ENG-010`/`ENG-033`/`ENG-034` already left
it earlier the same day; see each one's own paragraph below and the closing
paragraphs above. Listed here
for visibility, not because any number of them blocks a new start.

**`ENG-048`'s L1 merge request** (`inbox/2026-09-07-eng048-merge-request.md`)
— new, open. Code review (round 2), quality (round 2), security (zero
blocking findings), and the migration gate all passed; devops's own
release-readiness hop held the readiness gate (rollback drilled twice
against a disposable replica; one non-blocking observability note — the
cron unconditionally 404s until `ENG-049` ships, judged non-blocking on the
same reasoning `ENG-037`/`ENG-038` established; cost `$0/month`), then
opened `aiorders-api` PR #21. First of `ENG-027`'s two sub-tickets (a
strict chain, not a DAG) — this ticket parking freed the family's machine
slot, and per the Guards amendment dated this same day, `ENG-049`'s own
`depends_on: [ENG-048]` is satisfied now that this PR is open, not only once
this ticket reaches `verified`. `continue ENG-049` fired before this pass
exited. Full reasoning: `ENG-048`'s own board-file log and
`agents/devops/notebook/2026-09-07-release-readiness-log.md`.

**`ENG-049`'s L1 merge request** (`inbox/2026-09-07-eng049-merge-request.md`)
— new, open. Code review (round 2), quality (round 2, 45/45), and security
(round 2 — round 1 failed one critical finding, fixed, re-verified pass)
all passed; no migration owed. Devops's own release-readiness hop held the
readiness gate: rollback reasoned (no migration in this diff; a loyalty
entry already credited before a revert stands, per this ticket's own
already-accepted design); the load-bearing finding was
`CLOUDWAITRESS_WEBHOOK_SECRET` — checked live, not provisioned, and this
diff's own security fix gates **all** CloudWaitress traffic through it,
including plain `order_new`, so an unset secret 401s all order intake the
moment this deploys, not just loyalty crediting. Judged non-blocking for
opening this PR (no CI/CD on this repo; the actual deploy is a separate,
future, manual act) but named at maximum prominence as a hard pre-deploy
requirement in the PR, the merge-request item, and the devops notebook —
materially more severe than `ENG-039`'s own `BROADCAST_UNSUBSCRIBE_SECRET`
gap, which degraded loudly per-message rather than failing all intake
silently closed. Then opened `aiorders-api` PR #22, stacked on `ENG-048`'s
own branch (PR #21, still open) rather than `main`. **Last of `ENG-027`'s
two sub-tickets** — with both children now `blocked_on: approver` and no
third child, the family's machine slot is free with no sibling to fill it.
Checked the top of To-do (the only place a new start is drawn from):
`ENG-018`, `ENG-028`, `ENG-042`, `ENG-043` are all genuinely blocked on an
already-open, unanswered inbox item — nothing startable, and deliberately
not drawn from the `designed`-state pool `ENG-019`/`ENG-020`/`ENG-021`/
`ENG-026` once used in this same situation (that pool isn't in
`eng_build_loop.md` step 6's own literal definition of To-do; filed as a
proposal rather than repeated a fifth time). Raised `IDLE-2026-09-07.md`
instead — see its own paragraph below. Full reasoning: `ENG-049`'s own
board-file log and `agents/devops/notebook/2026-09-07-release-readiness-log.md`.

**`IDLE-2026-09-07`'s "nothing I can start" notice** (`inbox/IDLE-2026-09-07.md`)
— new, open. Not a ticket-specific gate; raised because `ENG-049` parking
freed the `ENG-027` family's machine slot (its last child, no sibling left)
and every To-do occupant (`ENG-018`, `ENG-028`, `ENG-042`, `ENG-043`) is
already blocked on its own open item in this same list. Recommends
answering `ENG-018`'s G1 first (lowest id of the two `priority: now`
candidates, both a day past their one nudge) but names all four candidates
and what would clear each. Resolves itself the moment any one of them is
answered and the freed slot is filled — no reply needed to this item
specifically.

**`ENG-044`'s L1 merge request** (`inbox/_handled/2026-09-07-eng044-merge-request.md`)
— raised ~03:48 PDT: code review, quality, and security (zero findings) all
passed; devops's own release-readiness hop held the readiness gate (rollback
actually drilled against a disposable replica; observability traced to the
one live caller's existing `console.error` + automatic fallback on Postgres
`42883`; cost `$0/month`), then opened `aiorders-api` PR #19. **Resolved,
terminal.** A control-center dashboard action advanced `blocked → shipped`
ahead of a build-loop pass — local git ancestry confirms
`feat/ENG-044-foodswipe-channel-visibility-schema` is an ancestor of
`origin/main`. **Off this list**, item now in `inbox/_handled/`; see its own
board file. First of `ENG-026`'s four sub-tickets — cleared the way for
`ENG-045` (built, reviewed, tested, and security-passed the same day) and
`ENG-046` (dependency now satisfied, next in the family's own slot; see the
`ENG-045` paragraph below and its own dated entry).

**`ENG-045`'s L1 merge request** (`inbox/2026-09-07-eng045-merge-request.md`)
— raised this pass (~10:58 PDT): code review (round 2 — round 1 found one
blocking finding, decision logic not exported per
`engineering-standards.md`, fixed with a two-line diff), quality (15/15,
mutation-checked), and security (zero findings) all passed; devops's own
release-readiness hop found the project L1, held the readiness gate (no
migration owed — schema shipped with `ENG-044`; rollback trivial, no stored
state; observability confirmed pre-existing on all three touched handlers;
cost `$0/month`), then opened `aiorders-api` PR #20. Second of `ENG-026`'s
four sub-tickets — `ENG-046`'s own dependency (`ENG-044` alone) is already
satisfied and independent of this branch. **Correction, `ENG-046`'s own
2026-09-07 devops hop:** the "`ENG-047` ... stays `ready` until it reaches
`verified`" clause above was the pre-amendment reading; `eng_build_loop.md`
Guards (amended 2026-09-07, same day) closed it — an open PR satisfies
`depends_on`, so `ENG-047`'s dependency on *this* ticket is satisfied now,
by this PR being open, not waiting for it to merge. Full reasoning:
`agents/devops/notebook/2026-09-05-release-readiness-log.md` (pattern) and
this ticket's own board-file log (detail). **Slot freed:** this ticket
leaving the `ready-to-ship` state frees the `ENG-026` family's one machine
slot (Guards, amended 2026-09-06/07) — `continue ENG-046` fired the same
pass (queued behind the long-running family wrapper, not lost; see the
dated entry below and `ENG-045`'s own board-file log). See the dated entry
below.

**`ENG-046`'s L1 merge request** (`inbox/2026-09-07-eng046-merge-request.md`)
— raised this pass (~12:16 PDT): code review, quality, and security (zero
findings) all passed; devops's own release-readiness hop found the project
L1, held the readiness gate (no migration owed — frontend-only diff;
rollback trivial, no stored state; observability confirmed pre-existing on
`handleSave`'s own try/catch; cost `$0/month`), then opened
`aiorders-admin-hub` PR #10. Third of `ENG-026`'s four sub-tickets — with
this ticket parking, every family member is now either `shipped`
(`ENG-044`) or parked on the approver (`ENG-045`, `ENG-046`) except
`ENG-047`, whose sole dependency (`ENG-045`) is satisfied by that PR being
open (see the correction in `ENG-045`'s own paragraph above). Full
reasoning: this ticket's own board-file log. **Slot freed:** this ticket
leaving the `ready-to-ship` state frees the `ENG-026` family's one machine
slot (Guards, amended 2026-09-06/07) to `ENG-047` specifically — the
family's next child with a satisfied dependency, per the same amendment's
part (b), not a fresh draw from the top of To-do. `continue ENG-047` fired
the same pass (queued behind this still-in-flight pass, not lost; see the
dated entry below and this ticket's own board-file log). See the dated
entry below.

**`ENG-041`'s L1 merge request**
(`inbox/2026-09-06-eng041-merge-request.md`) — raised this pass (~11:16
PDT): code review (round 2 — round 1 found and fixed a real cross-restaurant
FAQ-draft leak), quality, and security all passed; devops's own
release-readiness hop found the project L1, held the readiness gate (no
blocking failure — rollback reasoned not drilled, cost $0/month, no
client-side error tracking anywhere in this repo, a pre-existing gap already
accepted on `ENG-002`/`ENG-032`/`ENG-039`), then opened `restaurant-portal`
PR #5. This is `ENG-021`'s last sub-ticket — once this merges and ships, the
parent qualifies for its own `ADR-003`-class exemption. Full reasoning:
`agents/devops/notebook/2026-09-06-release-readiness-log.md`. **Resolved,
terminal.** This `scheduled` pass's own step-5 re-check (02:00 PDT) found
PR #5 merged directly to `main`, no written reply — full acceptance-check
run, all 4 owned criteria pass, deploy confirmed live (Cloudflare Pages run
completed 3s after merge), carried `blocked → shipped → verified`. Both of
`ENG-021`'s children now settled — the parent's `ADR-003`-class exemption
is satisfied; `continue ENG-021` fired. **Off this list and off the board
entirely (terminal)**, item now in `inbox/_handled/`; see the closing
paragraphs above and its own board file.

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

**`ENG-028`'s G1** (`inbox/_handled/2026-09-03-eng028-g1-scope.md`) was
answered **changed** (2026-09-06T09:09:08), two clauses: "Lets hard code
stages Make new stages waitlisted, contacted, meeting scheduled, Follow
Up,Onboarding,Not Interested,On Hold, activated,Upsell. Can we have
autopilot email/sms setup on admin panel like brand portal for each stage
update." Processed this pass — rescoped in place rather than advanced,
since a `changed` answer isn't an approval. First clause rejects the
staff-configurable editor outright in favour of hardcoding a named
nine-stage list; checked against live code and confirmed none of the nine
correspond to the six stages `classifyStage()` computes today, so the
rescope proposes retiring automatic classification and resetting every
listing to `Waitlisted` — flagged prominently rather than assumed. Sized
`M` (was `L`), no G2 now expected. **`ENG-028`'s fresh G1**
(`inbox/2026-09-06-eng028-g1-rescope.md`) — raised this pass: recommends
building the hardcoded nine-stage version now, with one rider (confirm
retire-and-reset over keeping the old six alongside the new nine as a
dual-taxonomy system). Second clause is a new, separate ask this ticket's
own non-goals had pointed at `ENG-017` — but `ENG-017` covers the
unrelated presignup-`leads` pipeline, not Foodswipe listings, so it didn't
fold in there. Filed as a new ticket instead, **`ENG-042`** (Foodswipe
funnel — stage-triggered autopilot email/SMS, `aiorders-api`, `L`,
`depends_on: [ENG-028]`), same split this board already used once for this
shape (`ENG-013` → `ENG-028`). Ran a full request-readback for `ENG-042`
(this PM's reading plus a blind subagent reading, no material divergence;
the blind reading independently surfaced the same CASL-shaped consent gap
`ENG-017`'s own design already found for its sibling pipeline). **`ENG-042`'s
own first G1** (`inbox/2026-09-06-eng042-g1-scope.md`) raised alongside the
rescope. Both notified (`traces/eng-notify-2026-09-06.log`, `02:28:29`,
both `sent`); decision-journal row added for the `changed` verdict. Full
reasoning: `ENG-028`'s and `ENG-042`'s own board-file logs,
`agents/product-manager/specs/ENG-028-foodswipe-custom-pipeline-stages.md`,
`agents/product-manager/specs/ENG-042-foodswipe-funnel-stage-autopilot.md`,
and `decision-journal.md`.

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

**`ENG-020`'s L1 merge request — resolved, terminal.** Raised
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
diff. **This `scheduled` pass's own step-5 re-check found both PRs merged
directly to `main`, 94 seconds apart, no written reply** — full
acceptance-check run, all 5 owned criteria pass, both sides confirmed
actually deployed (not just merged), carried `blocked → shipped → verified`.
**Off this list and off the board entirely (terminal)**, item now in
`inbox/_handled/`; see the closing paragraph below and its own board file.

**`ENG-040`'s L1 merge request — new, open.** Raised by this pass
(`inbox/2026-09-05-eng040-merge-request.md`, ~16:51 local): code review,
quality, and security all passed, round 1, no migration owed (no schema
change); devops's own release-readiness hop found the project L1 (window
check skipped), held the readiness gate (rollback/observability/cost all
clear — no migration to revert, existing per-key error logging already
covers the new `faqs` key, $0/month, no new dependency), then opened
`aiorders-api` PR #18. Two non-blocking findings carried in the request
(review's `??`-vs-`||` rationale note; security's A04 shape-validation gap,
tenant-confined and not a three-strike). This is `ENG-021`'s first
sub-ticket to reach the approver — `ENG-041` (the FAQ editor UI) stays
`ready`, still waiting on this ticket's own `depends_on`, which clears on
`verified`, not on a merge request being raised. Full reasoning: this
ticket's own board-file log and
`agents/devops/notebook/2026-09-05-release-readiness-log.md`.
**Resolved, terminal.** This `scheduled` pass's own step-5 re-check found
PR #18 merged directly to `main`, no stacking, no written reply — receipts
(review/quality/security) re-read fresh and confirmed `pass`, no migration
owed, zero drift on this ticket's own diff (the one file changed beyond the
reviewed tip is `ENG-020`'s own already-verified README addition landing via
`main`'s other merge parent), `brand-portal` confirmed actually redeployed
(version 84) ~18 minutes after merge. Full acceptance-check run — all 3
owned criteria (AC4, AC5 in full, AC3's write half) pass — carried
`blocked → shipped → verified`. **Off this list and off the board entirely
(terminal)**, item now in `inbox/_handled/`; see the closing paragraph above,
this ticket's own board-file log,
`agents/product-manager/notebook/2026-09-06-eng040-acceptance.md`, and
`agents/devops/releases/2026-09-06-aiorders-api-ENG-040.md`. Unblocked
`ENG-041` — `continue ENG-041` fired this same pass rather than building it
inline.

**`ENG-043`'s own intake-question — new, open.** Raised by the `intake`
pass that created the ticket
(`inbox/2026-09-06-eng043-stage-names-clarification.md`, ~02:47 local): a
garbled control-center submission (title citing `ENG-011`, body reduced to
"Healf") couldn't be shaped into a PRD as written. Two candidate readings
named rather than guessed between — genuinely about `ENG-011`'s own
client-stage labels (`verified`, a declared non-goal on record) vs. a
same-day follow-up on `ENG-028`'s own fresh rescope G1, answered six
minutes before this message arrived — plus an explicit "or neither."
`ENG-043` holds at `intake`, no PRD, `owner: product-manager`; nothing else
is blocked on this. Full reasoning: this ticket's own board-file log and
the dated entry below.

**`ENG-018`'s G1 — new, open.** This `scheduled` sweep found this ticket's
own `priority` had gone `hold → now` — an uncommitted, two-field working-tree
edit with no commit, no ticket-log entry, and no journal/exceptions row
anywhere, caught only because this pass's own table-vs-frontmatter
cross-check (step 10 groundwork) reads every ticket's live file rather than
trusting the table. Read as the approver's own direct hand-edit — the only
channel that field has, and the same one its original `hold` value arrived
through on 2026-08-29 — not a clobber to revert; full reasoning, including
why this reads opposite to the 2026-09-03 blank-out incident rather than as
a repeat of it, on the ticket's own board-file log. With `hold` lifted and
the approver-facing WIP cap that also once held this ticket back already
resolved 2026-09-02, nothing was left blocking a G1 that has sat fully
drafted since intake — re-verified fresh against live code (no demo
mechanism anywhere in any of the five repos, `ENG-016`'s catering pipeline
now actually shipped) before raising it this pass:
`inbox/2026-09-06-eng018-g1-scope.md`. `awaiting-scope`, `owner:
product-manager → approver`. Full reasoning: this ticket's own board-file
log and the dated entry below.

## 2026-09-07 — scheduled (launchd, retry): sixth consecutive idle re-confirmation — completes the session-limit-interrupted fifth, no corruption found

Not a fresh firing — this is attempt 2 of the same `scheduled (launchd)`
event the previous entry's own pass was handling. That pass wrote the
entry above (including filing the repeated-idle proposal), then hit the
account's session usage limit on its next action and exited 1 at
`20:50:48` (570s runtime — a genuine failure, correctly not classified
never-started). Per the documented retry rule its event went back to the
front of the queue one attempt older; the very next fire never started at
all (3s, account-limit, refunded, rotated `CLAUDE_CODE_OAUTH_TOKEN` →
`_2`); this pass is the one after that, on the rotated account
(`traces/eng-loop-2026-09-07.log`: `20:55:56` refund/rotate, `21:00:59`
draining this event, `21:01:01` launch).

**Verified the crash left nothing broken before trusting any of it:**
`_index.md` holds exactly three dated entries (keep-three rule intact —
the failed pass's own roll-to-archive step had completed), the proposal
row it was mid-editing (`proposals.md`, 2026-09-07 eng-manager row) reads
internally consistent (arithmetic now says "seven launches ... five
completed" throughout, no leftover "six"), and `lib/eng-gate-check.sh`
whole-board exits `0` clean. The failure was a session-budget artifact,
not a correctness bug — nothing here needed repair.

**Full fresh re-verification, not taken on the interrupted pass's word:**
mode check clean (`MODE=active`). Steps 2–4: all three inboxes swept,
nothing new; all ten open `inbox/` items re-grepped for `^decision:` —
none answered. Step 5: `git fetch origin main` +
`gh pr view --json state,baseRefName,mergedAt` from the department's own
`_eng/aiorders-api` worktree — PR #21 (`ENG-048`) and PR #22 (`ENG-049`,
stacked on #21) both still `OPEN`, `mergedAt: null`. Step 6: whole-board
`state:` census re-run directly against every ticket file — unchanged (32
`verified`, 9 `designed`, 3 `awaiting-scope`, 2 `dropped`, 2 `blocked`, 1
`intake`, 1 `building`). `ENG-027` is the only ticket in
`ready..ready-to-ship` and is a container holding zero slots (both
children `blocked_on: approver`) — Machine WIP `0/1`, genuinely free.
To-do (`ENG-018`, `ENG-028`, `ENG-042`, `ENG-043`) re-checked against fresh
frontmatter: all four still `awaiting-scope`/`intake`, owner `approver` or
`product-manager`, still genuinely unanswered. Checked all nine `designed`
tickets for a `priority` change that might reopen the fallback question —
none carry `now`/`next`, all still empty, same as every prior check today;
**not relitigated**, same open tension already filed in `proposals.md`. No
`priority: hold` ticket found in a working state. `IDLE-2026-09-07.md`
re-read in full, still accurate, not duplicated — sixth consecutive
confirmation.

**Dead-end sweep:** `lib/eng-gate-check.sh` whole-board exit `0` (above).
Both `blocked` tickets still carry `blocked_from: ready-to-ship`. No
`*-eng-events-dropped.md` for today beyond what the trace log already
accounts for (the interrupted pass's own failure and the never-started
retry were both handled by the documented rules, not silently dropped —
named for completeness, not as a new finding).

**Step 7 (notify):** every open item's `notified:`/`nudged:` re-checked
against wall clock (`21:02` PDT): `ENG-048`, `ENG-049`, `ENG-050`, and
`IDLE-2026-09-07` all still under 24h old; every older item already
carries its one-ever `nudged:` stamp. Nothing raised, nothing nudged.

**Step 8b/8c:** nothing new to decide, except, or journal — no gate
answered this pass. Not logging a further observation on the repeated-idle
pattern itself: it already escalated to a proposal last entry, and this
pass's own crash-plus-retry is the same mechanism recurring, not a new
one — noted above in this entry's own narrative instead of a fresh
`observations.md` line, per the "don't relitigate/re-log an already-named
pattern" reasoning already applied to the fallback question this same
pass.

Post-pass `lib/eng-gate-check.sh`, whole-board: exit 0, clean.

`chained: none — idle: nothing startable` — same idle condition
`IDLE-2026-09-07.md` already names, unchanged by five prior passes and by
this one. No ticket changed state, so nothing to chain.

**Board update, this pass:** no ticket file touched. Live file held three
dated entries before this one; oldest (`scheduled (auto-drain)`: whole-board
sweep, third idle confirmation) rolled to `_index-archive.md` per the
keep-three rule, done before this entry was written so the count stays at
three.

business-os itself left uncommitted this pass (this index and its archive
touched) — same standing default every pass on this board has used; the
commit-convention question remains open, not re-decided here.

## 2026-09-07 — scheduled (auto-drain): seventh consecutive idle re-confirmation — designed-pool fallback still withheld pending the open proposal

`scheduled` safety-net event, context `auto-drain`, per the task prompt.
Reading map for `scheduled` is never narrowed — whole `eng_build_loop.md`
read fresh this pass, not just a subset. Trace log: prior pass (sixth
confirmation) ended `21:08:39` (exit 0, 458s); this event drained
`21:08:42`, launched `21:08:44` on `CLAUDE_CODE_OAUTH_TOKEN_2`. Mode check
clean (`.env` → `MODE=active`; wall clock `21:09`–`21:14` PDT this pass).
`traces/.pending` empty on inspection — nothing queued behind this one.

**Steps 2–4, re-verified fresh:** `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/`, and `inbox/requests/` hold only their own
`.gitkeep`/`_handled`/`_processed` — nothing new. All ten open `inbox/`
items (`ENG-016`-piece2, `ENG-018`, `ENG-028`, `ENG-042`, `ENG-043`,
`ENG-048`, `ENG-049`, `ENG-050`-P0, `IDLE-2026-09-07`, `PROP-2026-W36`)
re-grepped for `^decision:` — none present on any.

**Step 5, from the department's own `_eng/aiorders-api` worktree** (not the
human's checkout): `git fetch origin main`, then `gh pr view
--json state,baseRefName,mergedAt,headRefName` on both — PR `#21`
(`ENG-048`) `OPEN`/`mergedAt: null`; PR `#22` (`ENG-049`, stacked on `#21`)
`OPEN`/`mergedAt: null`. Unchanged.

**Step 6:** whole-board `state:` census re-run directly against every
ticket file: 32 `verified`, 9 `designed`, 3 `awaiting-scope`, 2 `dropped`,
2 `blocked`, 1 `intake`, 1 `building` — identical to the immediately
preceding pass. `ENG-027` is the sole ticket in `ready`..`ready-to-ship`
and is a container holding zero slots (both children `ENG-048`/`ENG-049`
`blocked_on: approver`) — Machine WIP `0/1`, genuinely free. To-do
(`ENG-018`, `ENG-028`, `ENG-042`, `ENG-043`) re-checked against fresh
frontmatter: all four still `awaiting-scope`/`intake`, owner `approver` or
`product-manager`, still genuinely unanswered. No `priority: hold` ticket
found in a working state.

**Did not fall back to the `designed`-state pool — same fork as the two
immediately preceding passes, same reasoning, not re-decided a third
time.** `eng_build_loop.md` step 6's own literal text — read in full this
pass, as every `scheduled` pass must — names only `intake`/`shaped`/
`awaiting-scope` as "the only place a *new* start is drawn from"; it says
nothing about a `designed` ticket with a completed design and no one-way
door. The four board dispatches that drew from that pool anyway
(`ENG-019`, `ENG-020`, `ENG-021`, `ENG-026`) are precedent, not written
policy, and whether that precedent is sound is now an open question
sitting in `proposals.md` (2026-09-07, devops row) awaiting the approver's
batched decision. Drawing from the pool this pass would be the department
re-deciding, a third time today, the exact question it already routed to
the approver — the self-authorized-scope-creep step 3 exists to stop, just
aimed at a process question instead of a ticket. Nothing new arrived to
change that read, so it stands. `IDLE-2026-09-07.md` re-read in full,
still accurate against every fact above, not duplicated — **seventh**
consecutive pass to reach this identical conclusion.

**Dead-end sweep:** `lib/eng-gate-check.sh`, whole-board: exit 0, clean,
both pre- and post-pass. Both `blocked` tickets still carry
`blocked_from: ready-to-ship`. Fresh `exception-request:` sweep across
every ticket file: every hit is a prior pass's own "none found" negation,
not a live request. No `*-eng-events-dropped.md` file for today beyond
what the trace log already accounts for. `ENG-027`'s own board-file log
still ends on an intact `chained:` record from the fourth confirmation —
the fifth and sixth recorded their own `chained:` line in this index
instead, since neither touched any ticket file; same choice made here for
the same reason.

**Step 7 (notify):** every open item's `notified:`/`nudged:` pair
re-checked against wall clock (`21:14` PDT): `ENG-048`, `ENG-049`,
`ENG-050`, and `IDLE-2026-09-07` all still under 24h old; every older item
already carries its one-ever `nudged:` stamp. Nothing raised, nothing
nudged.

**Step 8b/8c:** nothing new to observe or journal. The repeated-idle
pattern is already tracked as a proposal (`proposals.md`, 2026-09-07,
eng-manager row) and the designed-pool tension as another (devops row,
same date); this pass is the same mechanism continuing, not a new
occurrence of either, so neither is re-logged. No gate was answered this
pass, so nothing to journal (8c).

Post-pass `lib/eng-gate-check.sh`, whole-board: exit 0, clean.

`chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged, not
duplicated (seventh consecutive confirmation)`. No ticket changed state,
so nothing to chain.

**Board update, this pass:** no ticket file touched. Live file held three
dated entries before this one; oldest (`continue (ENG-027)`: fourth
consecutive confirmation) rolled to `_index-archive.md` per the keep-three
rule, done before this entry was written so the count stays at three.

business-os itself left uncommitted this pass (this index and its archive
touched) — same standing default every pass on this board has used; the
commit-convention question remains open, not re-decided here.

## 2026-09-08 — scheduled (launchd): idle streak continues unbroken — no divergence from the 16th `continue ENG-027` confirmation

`scheduled` safety-net event, context `launchd`, per the task prompt.
Reading map for `scheduled` is never narrowed — whole `eng_build_loop.md`
read fresh this pass. `traces/eng-loop-2026-09-08.log`: prior pass
(`continue ENG-027`, 16th consecutive confirmation on that ticket) ended
`01:45:18` (exit 0, 480s); this event drained `02:00:04`, launched
`02:00:06`. `traces/.pending` empty on inspection — nothing queued behind
this one. Mode check clean (`.env` → `MODE=active`; wall clock `02:01`
PDT).

**Steps 2–4, re-verified fresh, not taken on the prior pass's word.**
`agents/product-manager/inbox/`, `agents/eng-manager/inbox/`, and
`inbox/requests/` hold only their own `.gitkeep`/`_handled`/`_processed` —
nothing new for either the PM or the EM, nothing filed since midnight's
counter rollover. All ten open `inbox/` items (`ENG-016`-piece2, `ENG-018`,
`ENG-028`, `ENG-042`, `ENG-043`, `ENG-048`, `ENG-049`, `ENG-050`-P0,
`IDLE-2026-09-07`, `PROP-2026-W36`) re-grepped for `^decision:` — none
present on any.

**Step 5, from the department's own `_eng/aiorders-api` worktree** (not
the human's checkout): `git fetch origin main`, then `gh pr view --json
state,baseRefName,mergedAt,headRefName` on both — PR `#21` (`ENG-048`)
`OPEN`/`mergedAt: null`; PR `#22` (`ENG-049`, stacked on `#21`)
`OPEN`/`mergedAt: null`. Unchanged. No other `blocked` ticket exists on
the board to check (whole-board census below counts exactly these two).

**Step 6:** whole-board `state:` census re-run directly against every one
of the board's 50 ticket files, not the In-flight table: 32 `verified`, 9
`designed`, 3 `awaiting-scope`, 2 `dropped`, 2 `blocked`, 1 `intake`, 1
`building` — identical to every check tonight back through the fifth
confirmation. Confirmed by name, not just by count, that the four
`awaiting-scope`/`intake` tickets are still exactly `ENG-018`, `ENG-028`,
`ENG-042`, `ENG-043` — no new arrival in To-do. `ENG-027` is the sole
ticket in `ready`..`ready-to-ship` and is a container holding zero slots
(both children `ENG-048`/`ENG-049` `blocked_on: approver`, confirmed via
fresh frontmatter reads) — Machine WIP `0/1`, genuinely free. All four
To-do occupants re-checked against fresh frontmatter: still genuinely
blocked on their own already-open, unanswered `inbox/` item apiece. No
`priority: hold` ticket found in a working state.

**Did not fall back to the `designed`-state pool — same fork as every
pass since the seventh confirmation, not re-decided again.** The
tension between `eng_build_loop.md` step 6's literal To-do definition and
this board's own four-time precedent for drawing from `designed` is
sitting in `proposals.md` (2026-09-07, devops row) awaiting the approver's
batched decision; nothing new arrived to justify re-litigating it.
`ENG-050` (the P0 security ticket) stays correctly excluded at `designed`
for the identical reason. `IDLE-2026-09-07.md` re-read in full, still
accurate against every fact above, not duplicated.

**Dead-end sweep:** `lib/eng-gate-check.sh`, invoked as `env
ENG_ROOT="$ENG_INSTANCE" sh lib/eng-gate-check.sh` per
`lib/eng-trigger.sh`'s own pattern — whole-board: exit `0`, clean,
pre-pass. Both `blocked` tickets (`ENG-048`, `ENG-049`) still carry
`blocked_from: ready-to-ship`. Fresh `exception-request:` sweep across
every board file: every hit is a prior pass's own prose negation ("no
`exception-request:` on this ticket"), not a live request. No
`*-eng-events-dropped.md` file for today. `ENG-027`'s own ticket log ends
on an intact `chained: none — idle: nothing startable` record from the
16th confirmation — no broken chain to resume.

**Step 7 (notify):** every open item's `notified:`/`nudged:` pair
re-checked against wall clock (`02:01` PDT): the four 2026-09-06 items
(`ENG-018`, `ENG-028`, `ENG-042`, `ENG-043`) already carry their one-ever
`nudged:` stamp; `ENG-048`, `ENG-049`, `ENG-050`, and `IDLE-2026-09-07` are
all still under 24h old (oldest of these, `ENG-050`, ~9h57m);
`PROP-2026-W36` already nudged. Nothing raised, nothing nudged.

**Step 8b/8c:** nothing new to observe or journal. The repeated-idle
pattern and the designed-pool tension are both already tracked as open
proposals (`proposals.md`, 2026-09-07, eng-manager and devops rows,
respectively); this pass is the same mechanism continuing into a new
calendar day, not a new occurrence of either, so neither is re-logged. No
gate was answered this pass, so nothing to journal.

Post-pass `lib/eng-gate-check.sh`, whole-board: exit `0`, clean.

`chained: none — idle: nothing startable; IDLE-2026-09-07 unchanged, not
duplicated`. No ticket changed state, so nothing to chain.

**Board update, this pass:** no ticket file touched. Live file held three
dated entries before this one; oldest (`scheduled (launchd, retry)`:
sixth consecutive idle re-confirmation) rolled to `_index-archive.md` per
the keep-three rule, done before this entry was written so the count
stays at three.

business-os itself left uncommitted this pass (this index and its archive
touched) — same standing default every pass on this board has used; the
commit-convention question remains open, not re-decided here.
