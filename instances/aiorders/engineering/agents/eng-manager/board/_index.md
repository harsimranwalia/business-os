# Board

**Next ID: ENG-026** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.)

**Machine WIP 1** (`config/config.yaml` → `wip.machine_limit`). **Corrected
2026-08-29 — the approver's direct instruction: one ticket completed end to
end (through `shipped`) before the next one starts, not several tickets each
advanced by one shallow step per pass.** This was 12 (the `max_5x` tier value)
earlier the same day; see that file for the full rationale.

**Currently 2/1 — over the new cap, but shrinking.** `ENG-009` sits at
`in-qa` as of this pass (code review round 2 + the quality gate both
passed; security is the next hop) — earlier today this table wrongly said
`ready` from 2026-09-01 09:30 onward, a stale correction the 09:30 pass
that day made in error, itself corrected by this file's own 09:30
dated entry below (full evidence trail there). `ENG-010`
sits at `ready`, correctly, sequenced behind it. `ENG-008` and `ENG-013` both
left this range on 2026-08-31 — each one's security gate passed, then its own
devops release-readiness hop opened its PR(s) and moved it to
`blocked`/`blocked_on: approver` — all four were already in flight when the
cap changed and are **not** being reverted or paused; they drain naturally as
each reaches `shipped`. **No new ticket enters `ready` until this count is
back at or under 1** — `ENG-014` through `ENG-025` stay at
`designed`/`shaped`/`awaiting-scope` (backlog grooming only, not gated by this
cap) until then.

**Approver-facing WIP 2 — 3/2, over cap, not 2/2.** `ENG-013`
(`inbox/2026-08-31-eng013-merge-request.md`) and `ENG-008`
(`inbox/2026-08-31-eng008-merge-request.md`) each occupy a slot via their own
L1 merge request — a plain merge on GitHub, no reply needed, clears either.
**`ENG-016` occupies the third slot**, missing from this table until this
`watch` pass found it: its own board file and PRD both read `state`/`status:
awaiting-scope`, `owner: approver`, G1 raised and notified
`2026-08-29T23:13:49` (`inbox/2026-08-29-eng016-g1-scope.md`) — the
cross-host board-reconciliation merge (`e281c71`) kept a rival account that
never raised this G1 and showed `shaped`/`product-manager` instead, and
every pass since trusted this table over the ticket's own file. No
`decision-journal.md` entry and no PRD reset exists for it — checked before
concluding this was staleness rather than a legitimate re-open. Nudged this
pass (first nudge; notified 2.5 days ago, never nudged before). Nothing new
may start needing the approver until one of these three clears — already
the practical outcome the last two passes reached, now for the reason that
actually holds.

**No separate approval cap exists.** `approval_cap` was removed 2026-08-29
at the approver's own request (`config/config.yaml`; also stated in
`schedules/eng_build_loop.md`'s Guards section) — `wip.approver_limit` (2,
above) is the only approver-side lever left. The "Approval cap 3" framing
this board carried until this pass was itself part of the same stale merge
account, not a live rule. `ENG-019` through `ENG-021` remain G1-drafted, not
yet raised (`ENG-018` excluded outright, `priority: hold`; `ENG-017` already
past its own G1, now `designed`) — left for a future pass, same as before,
now correctly reasoned against the WIP-2 cap alone.

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
| ENG-008 | Influencer board admin management — region/campaign-type preference, rating, collaboration count | aiorders-admin-hub | blocked | | approver | M | 2026-08-31 |
| ENG-009 | Influencer engagement info — internal activity signal plus a staff-editable social stat | aiorders-admin-hub | in-qa | | eng-manager | S | 2026-09-02 |
| ENG-010 | Influencer relationship notes — staff log for personality, preferences, and off-platform conversations | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-29 |
| ENG-013 | Foodswipe funnel page — staff-settable pipeline stages | aiorders-admin-hub | blocked | | approver | M | 2026-08-31 |
| ENG-014 | Brand portal self-service — restaurant QR codes and marketing media downloads | restaurant-portal | designed | | architect | M | 2026-08-31 |
| ENG-015 | Agency/reseller (partner) users — brand-scoped locations and a working add-location path | aiorders-admin-hub | designed | | architect | M | 2026-08-31 |
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
| ENG-016 | Catering page — self-serve quote generator, with automatic stage update | config-site-builder | awaiting-scope | next | approver | L | 2026-08-29 |
| ENG-017 | Autopilot nurture for the presignup sales lead pipeline — stage-triggered email/SMS | aiorders-api | designed | | architect | L | 2026-09-01 |
| ENG-018 | Sales demonstration account — a fully seeded AIOrders environment to show prospects | aiorders-admin-hub | shaped | hold | product-manager | L | 2026-08-29 |
| ENG-019 | Restaurant self-service marketing broadcasts — mass send and drip sequences, scheduled or immediate | restaurant-portal | shaped | | product-manager | L | 2026-08-29 |
| ENG-020 | Marketing ROI reporting — traffic source and revenue attribution on the brand dashboard | restaurant-portal | shaped | | product-manager | M | 2026-08-29 |
| ENG-021 | Website chat-bar engagement visibility — customer questions and self-service FAQ editing on the brand portal | restaurant-portal | shaped | | product-manager | M | 2026-08-29 |
| ENG-022 | Fix broken restaurant-scoped access check on 5 brand-portal handlers — cross-tenant PII/write exposure | aiorders-api | designed | | eng-manager | M | 2026-08-29 |
| ENG-023 | Add status and internal notes to each brand-portal feedback item | restaurant-portal | designed | | architect | S | 2026-08-31 |
| ENG-024 | Set show_in_marketplace on onboarding's createRestaurant insert, plus a backfill | aiorders-api | shaped | | eng-manager | XS | 2026-08-29 |
| ENG-025 | Recurring feedback issues, per restaurant, over time | restaurant-portal | designed | | architect | S | 2026-08-31 |
| ENG-026 | FoodSwipe multi-channel filters, operational status, and promo badges | restaurant-marketplace | intake | | approver | L | 2026-09-01 |

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

**Approver WIP limit 2 (the only cap — see header above). Currently 3/2,
over.** `ENG-013`'s L1 merge request
(`inbox/2026-08-31-eng013-merge-request.md`) — both PRs open
(`aiorders-api` #5, `aiorders-admin-hub` #4), all four gates passed, no
reply required (merging either PR directly on GitHub is itself the
decision, same as `ENG-005`/`ENG-007`/`ENG-011`); **nudged 2026-09-01T22:41:10
UTC** (~15:30 `scheduled` pass), first and only nudge, 28h+ with no merge or
reply. `ENG-008`'s L1 merge request
(`inbox/2026-08-31-eng008-merge-request.md`) — both PRs open
(`aiorders-api` #6, `aiorders-admin-hub` #5), all four gates passed, same
no-reply-needed shape; **nudged the same pass**, same timestamp, same
first-and-only nudge. **`ENG-016`'s G1**
(`inbox/2026-08-29-eng016-g1-scope.md`) — raised and notified 2026-08-29,
missing from this section until this pass (see the header note above for
why); nudged this pass, first nudge, 2.5 days overdue. `ENG-019` through
`ENG-021` are G1-drafted and not yet raised, correctly left for a future
pass — the WIP-2 cap is already over, so none of their G1s may be raised
regardless of the (nonexistent) approval cap this board used to cite.

## 2026-09-01 — watch sweep (~20:39): third duplicate fire today, off the 20:30 scheduled pass's own closing-note writes, nothing new

`watch` event pass, context `launchd` — fired immediately behind the 20:30
`scheduled` pass's commit (`f376e9c`, `20:38:19`). Narrow scope per this
event's own contract: sweep the three watched inboxes only.

Mode check clean (`MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

**Traced this fire to its source before treating it as new**, same check as
both watch entries before it today. `git status` shows a fully clean
working tree — nothing has changed anywhere in the repo since `f376e9c` —
and a direct mtime sweep of all three watched inboxes turns up exactly two
files newer than the prior watch fire: `inbox/2026-08-30-eng-loop-halted.md`
(`20:36:11`) and `inbox/2026-09-01-eng-gate-violation-watch.md`
(`20:36:16`). Both are the closing notes the 20:30 pass appended to two
incident files it had already verified, individually, as correctly
resolved (see the archived 20:30 entry) — not new information, just that
same pass's own bookkeeping tripping the fingerprint, identical in shape to
the ~10:25 and ~15:46 entries.

**All three inboxes swept anyway, not trusted from the paragraph above.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
their `_handled`/`_processed` archives. `inbox/requests/` holds only its
`.gitkeep`. `inbox/`'s four still-open gate items (`ENG-007`'s
continue-sequence question, `ENG-008`'s and `ENG-013`'s merge requests,
`ENG-026`'s readback question) were re-grepped for `^decision:` directly —
all four still blank. No hand-edit, no reply, no merge since the 20:30
pass ended.

**Nothing re-done.** Both incident files were already closed in place by
the 20:30 pass; re-reading their tails confirms the closing notes match
that pass's own entry, nothing appended since. `ENG-008`/`ENG-013`/
`ENG-016` were each nudged earlier today (first and only nudge, already
spent) — not renudged.

**Dispatch: nothing starts.** Same caps, unchanged: machine WIP 2/1
(`ENG-009`/`ENG-010` at `ready`, over cap, shrinking naturally);
approver-facing WIP 3/2 (`ENG-008`, `ENG-013`, `ENG-016` all still block
it). No ticket sits in a state this pass could legally advance.

**0 ticket-state transitions.** Rolled the 15:30 scheduled entry to
archive, keeping the live board's cap of three.

`chained: none` — nothing in this pass's scope sits in a state owned by
an agent; every in-flight ticket is either approver-blocked or WIP-capped,
same as every pass today. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

## 2026-09-02 — scheduled sweep (02:00): fully quiet — no merges, no answers, one drift note filed

`scheduled` event pass, context `launchd` — the four-times-daily safety
net. Mode check clean (`MODE=active`). Pre-pass `eng-gate-check.sh`,
whole-board: exit 0, clean, no `WAIVED:` lines (confirmed by running it
directly this pass rather than trusting an injected result).

**Business/technical intake:** `agents/product-manager/inbox/` and
`agents/eng-manager/inbox/` hold only their `_handled`/`_processed`
archives; `inbox/requests/` holds only its `.gitkeep`. Nothing new to
shape or route.

**Gate returns:** `git status` on the whole repo is clean and `HEAD` is
still `975a435` — the exact commit the prior (~20:39) pass ended on — so
nothing has touched this instance since. All nine loose `inbox/` items
re-read directly regardless: the four carrying a `decision:` field
(`ENG-007` continue-sequence, `ENG-008` and `ENG-013` merge requests,
`ENG-026` readback question) are all still blank, and `ENG-016`'s G1
(which carries no `decision:` key at all — see the drift note below) still
ends "Filled in by the approver." with nothing after it. No hand-edit, no
reply.

**Merge detection:** checked via `gh pr view` on all four PRs, not just
local ancestry. `aiorders-api` #6 and `aiorders-admin-hub` #5 (`ENG-008`),
`aiorders-api` #5 and `aiorders-admin-hub` #4 (`ENG-013`) — all four still
`OPEN`, `mergedAt: null`. Both tickets unchanged at `blocked`/`blocked_on:
approver`.

**Notify sweep:** nothing qualifies. `ENG-007`/`ENG-008`/`ENG-013`/`ENG-016`
were each already nudged once (exactly one nudge, ever — already spent).
`ENG-026`'s readback question is `notified: 2026-09-01T10:03:26`; current
UTC is `2026-09-02T09:03:13`, so it's ~22h59m old — still under the 24h
threshold by minutes, correctly left alone.

**One drift note, filed rather than fixed.** `ENG-016`'s G1
(`inbox/2026-08-29-eng016-g1-scope.md`) has no `decision:` key in its
frontmatter at all — unlike every other gate item on this board (e.g.
`ENG-009`/`ENG-010`'s G1s, per `observations.md` 2026-08-29), which carry
`decision:` blank until answered. This pass only found it by reading the
file directly; a heuristic that greps `^decision:` across `inbox/*.md` to
find answered gates (the shortcut this board's own recent entries
describe using) would never see this file at all, blank or answered,
since the key doesn't exist to match. Logged to `observations.md` rather
than fixed — it's a single hand-authored gate item, not a template this
pass has reason to touch, and the ticket itself is unaffected: read
directly, it's still unambiguously unanswered.

**Dead-end sweep:** nothing to re-walk. No commit, no inbox edit, no merge
since the ~20:39 pass — the chain-integrity conclusion every pass today
already reached stands unchanged: every `ready`/`designed`/`shaped` ticket's
last `chained:` line reads `none` with a valid cap/hold reason.

**Dispatch: nothing starts.** Same caps, unchanged: machine WIP 2/1
(`ENG-009`/`ENG-010` at `ready`, over cap, draining naturally); approver-facing
WIP 3/2 (`ENG-008`, `ENG-013`, `ENG-016` all still block it, none cleared).
No ticket sits in a state this pass could legally advance.

**0 ticket-state transitions.** 1 observation filed. Rolled the ~15:46
watch-sweep entry to archive, keeping the live board's cap of three.

`chained: none` — nothing in this pass's scope sits in a state owned by
an agent; every in-flight ticket is either approver-blocked or WIP-capped,
same as every pass today. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

## 2026-09-02 — scheduled sweep (09:30): found and resumed ENG-009's broken chain, masked ~28h by a wrong board-index correction

`scheduled` event pass, context `launchd` — the four-times-daily safety
net. Mode check clean (`MODE=active`). Pre-pass `eng-gate-check.sh`,
whole-board: exit 0, clean, no `WAIVED:` lines.

**Business/technical intake:** `agents/product-manager/inbox/` and
`agents/eng-manager/inbox/` hold only their `_handled`/`_processed`
archives; `inbox/requests/` holds only its `.gitkeep`. Nothing new to
shape or route.

**Gate returns:** all nine loose `inbox/` items re-read directly, plus one
timing check that changed a real decision (below). The four carrying a
`decision:` field (`ENG-007`, `ENG-008`, `ENG-013`, `ENG-026`) are all
still blank. `ENG-016`'s G1 still ends "Filled in by the approver." with
nothing after — confirmed by reading the file, not by grepping
`^decision:`, per the 02:00 pass's own drift note (it carries no
`decision:` key at all).

**`ENG-026` checked for its 24h nudge and correctly not nudged — the
field is real, the naive comparison against it isn't.** Fresh
`date`/`date -u` on this host: local is PDT, UTC = local + 7h. `ENG-026`'s
`notified: 2026-09-01T10:03:26` is textually identical to
`traces/eng-notify-2026-09-01.log`'s own local-clock entry for the same
raise (`[10:03:26] sent: active ...`) — which it cannot honestly be if one
is UTC and the other local. `ENG-016` and `ENG-007` (also
`agent: product-manager`) show the identical pattern; both merge-requests
(`agent: eng-manager`) show a genuine 7h gap, i.e. correct UTC. Corrected
for the true raise time (local 10:03:26 PDT = 17:03:26 UTC, 2026-09-01),
current UTC (`16:34:24`) puts this item at ~23h31m, not yet 24h — so it
was **not** nudged this pass, contrary to what a face-value reading of the
field would have done. Proposal filed (`proposals.md`) rather than fixed
inline — this is a stamping bug in whichever code path the product-manager
agent uses for `notified:`/`nudged:`, not this pass's file to edit blind.

**Merge detection:** `gh pr view` on all four PRs. `aiorders-api` #6 and
`aiorders-admin-hub` #5 (`ENG-008`), `aiorders-api` #5 and
`aiorders-admin-hub` #4 (`ENG-013`) — all four still `OPEN`, `mergedAt:
null`. Both tickets unchanged at `blocked`/`blocked_on: approver`.

**Dispatch — the real finding this pass.** Machine WIP read `2/1` (over
cap) on the strength of `ENG-009`/`ENG-010` both "sitting at `ready`," the
same conclusion every pass has repeated since 2026-09-01 09:30. Checking
`ENG-009`'s own board file directly instead of the index found `state:
building`, not `ready` — and has read `building` continuously since
commit `3881cc2` (2026-09-01 08:45), confirmed via `git show` at every
intervening commit (`29af8f2`, `db8bf41`, `3881cc2`, `e281c71`, `HEAD`).
The 09-01 09:30 pass misread this file, "corrected" the board index's
In-flight row from `building` to `ready` on that false premise
(`traces/eng-loop-2026-09-01.log:462-493`), and every pass since dispatched
off the wrong table value instead of the ticket's own file — the identical
root cause as `ENG-016`'s G1 going missing from this same table
(`proposals.md`, 2026-09-01 row, now updated with this second occurrence).

The ticket's own log shows a `chained: ENG-009` fire on 2026-08-30 that
never actually landed a session — zero mentions of `ENG-009` anywhere in
that day's `eng-loop` log, no `traces/.hops-*-ENG-009` file ever created on
this host, `links.review`/`links.test_plan` still blank. Most likely fired
from the Windows host (this ticket's build commit reads as a delayed local
sync, and that host's `traces/` is `.gitignore`d and unreachable from
here) — cannot root-cause further than that, same limit
`2026-08-31-eng-events-dropped.md` already named for the identical
cross-host blind spot. Verified safe to resume before touching anything:
both branches (`aiorders-api@4eb4b1b`, `aiorders-admin-hub@328db29`) still
resolve on `origin`, and `business-os` itself is ahead of, not behind,
`origin/main` (`git fetch` + `git log HEAD..origin/main` empty) — no newer
remote state this pass could be missing.

**Board index corrected**: In-flight row and header narrative both now say
`ENG-009` `building`. Machine WIP count itself is unchanged (2/1, over
cap either way — `building` is inside the same counted range `ready` was)
so nothing about the cap math moves; what changes is that this ticket was
never actually waiting on the cap, it was waiting on a chain nobody had
re-fired. `ENG-010` unaffected — its own hold (machine WIP, not
sequencing) still holds for the same reason as before.

**Full detail, evidence trail, and the fix itself: `ENG-009`'s own board
file, 2026-09-02 log entry** — not re-derived here.

**Notify sweep:** `ENG-026` — see above, not yet due. `ENG-007`/`ENG-008`/
`ENG-013`/`ENG-016` already nudged once each (spent). Nothing else
qualifies.

**Dead-end sweep:** this pass's own finding is the dead-end sweep result —
`ENG-009` was the broken chain. Nothing else changed: no new commits
beyond this pass's own, no other inbox edits, no other merges.

**1 ticket-state correction** (`ENG-009` board-index row: `ready` →
`building`, matching its own frontmatter — no actual state transition,
just removing a false one). **2 proposals filed.** Rolled the 20:30
scheduled-sweep entry to archive, keeping the live board's cap of three.

`chained: ENG-009` — sits at `building`, agent-owned (`eng-manager`), not
the approver, not blocked, not terminal, not held by a cap (already
inside the counted range regardless). Firing
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-009`
before exiting. Every other in-flight ticket is unchanged from every pass
today: approver-blocked (`ENG-008`, `ENG-013`, `ENG-016`, `ENG-026`) or
WIP-capped (`ENG-010`, `ENG-014`, `ENG-015`, `ENG-017`, `ENG-018`–`ENG-021`,
`ENG-022`–`ENG-025`), `chained: none` for all of them, same reasons as
before. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board: exit 0, clean, no `WAIVED:` lines.

