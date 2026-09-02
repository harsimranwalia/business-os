# Board

**Next ID: ENG-026** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.)

**Machine WIP 1** (`config/config.yaml` → `wip.machine_limit`). **Corrected
2026-08-29 — the approver's direct instruction: one ticket completed end to
end (through `shipped`) before the next one starts, not several tickets each
advanced by one shallow step per pass.** This was 12 (the `max_5x` tier value)
earlier the same day; see that file for the full rationale.

**Currently 2/1 — over the new cap, but shrinking.** `ENG-009` and `ENG-010`
sit at `ready`. `ENG-008` and `ENG-013` both left this range today — each
one's security gate passed, then its own devops release-readiness hop opened
its PR(s) and moved it to `blocked`/`blocked_on: approver` — all were already
in flight when the cap changed and are **not** being reverted or paused; they
drain naturally as each reaches `shipped`. **No new ticket enters `ready`
until this count is back at or under 1** — `ENG-014` through `ENG-025` stay
at `designed`/`shaped`/`awaiting-scope` (backlog grooming only, not gated by
this cap) until then.

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
| ENG-009 | Influencer engagement info — internal activity signal plus a staff-editable social stat | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-31 |
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

## 2026-09-01 — scheduled sweep (15:30): a day-old Windows-outage incident file was never actually investigated, despite the board saying it was

`scheduled` event pass, context `launchd` — the four-times-daily safety net,
not a narrow `watch`/`continue`. Mode check clean (`MODE=active`). Pre-pass
`eng-gate-check.sh`, whole-board: exit 0, clean. `git fetch origin main`:
no new commits — nothing arrived from the Windows host since the last pass.

**Business/technical intake:** `agents/product-manager/inbox/`,
`inbox/requests/`, and `agents/eng-manager/inbox/` all hold only their
processed archives — nothing new to shape or route.

**Gate returns:** re-read all 9 loose `inbox/` items directly. None carries
a `decision:` filled in, and file mtimes confirm nothing changed since the
10:32 `watch` pass ended — nothing answered.

**Merge detection:** `git fetch` + `git merge-base --is-ancestor` on both
`aiorders-api` and `aiorders-admin-hub` worktrees, for both `ENG-008`'s and
`ENG-013`'s branches against `origin/main`. Both worktrees clean, no
uncommitted changes. Neither ticket's branches merged in either repo —
`ENG-008`/`ENG-013` unchanged at `blocked`/`blocked_on: approver`.

**One real finding: `inbox/2026-08-31-eng-events-dropped.md` was never
actually investigated, despite two of today's own entries above claiming
it was.** Both the 09:30 pass's "same scheduled pass, continued" entry and
the ~10:10 `watch` pass repeated it grouped this file with
`2026-08-30-eng-loop-halted.md` and its siblings as "already resolved or
correctly inert." True for the `2026-08-30` sibling (investigated
2026-08-30 itself, reconfirmed four times since — now the subject of its
own escalated proposal about incident-closure process). False for this
one: grepped it directly for `Investigated`/`decision:`/`notified:`/
`nudged:` and got zero matches. Caught only because this pass read the
file's own content rather than trusting the summary — the same lesson the
`ENG-016` row learned earlier today, on a source file instead of a merge.

All 48 of its drops are `watch schtasks`/`scheduled schtasks` — no
`continue`/`intake`/`decision`/`finding` among them, confirmed by reading
every header — so nothing here needed hand-recovery the way the `09-01`
sibling's two concrete drops did; a sweep-type event carries no unique
payload, and several later sweeps have already run. Read together with
that sibling, the true outage ran continuously from `12:46:01` on 08-31
(after an earlier, separately-resolved blip at `00:11`–`00:41`) through
`07:45:58` on 09-01 — about 19 hours, not the ~7.5 hours the 09-01
investigation measured from its own file alone. That investigation's
recovery evidence (two successful pushes at `09:17`/`09:28` local, same
host identity) still covers this longer window, same transient cause — the
conclusion doesn't change, only the duration on record.

Closed in place: appended a closing investigation note to the file itself,
matching its 08-30 sibling's shape; corrected the WIP/waiting-on-approver
sections' silence on this above (the two earlier same-day entries are left
as written, historical record — a pointer note was added to the archived
copy instead of rewriting them); filed an observation
(`observations.md`) — second, non-merge instance of board prose
overclaiming a source file's state. Not raised or nudged: an incident
notice self-closes on investigation, it isn't a gate the approver answers,
and the general "incident items have no closure step" gap already has its
own open proposal.

**Also found while re-reading `inbox/_handled/2026-09-01-eng-events-dropped.md`
in full:** a hand-written line after its own `decision: approved` and this
morning's investigation footer, in a distinctly different voice from the
pass's own prose — "If the monhtly limit is hit, then do not retry tasks
rather check that the limit is reset then only it makes sense to retry
tasks instead of just retying tasks for no reason" (sic). Never journaled.
Added to `decision-journal.md` verbatim: a standing instruction that
`lib/eng-trigger.sh`'s retry/back-off path should confirm the vendor limit
has actually reset before retrying, which it currently doesn't (it retries
on elapsed time and attempt count alone). Filed as a proposal rather than
coded on the spot — it touches the same core retry path three other open
proposals already flag as needing sign-off before a hand-edit changes it.

**Notify sweep:** `ENG-013`'s and `ENG-008`'s L1 merge requests were both
`notified: 2026-08-31` (~28h old), no `nudged:`, no `decision:` — nudged
both (`lib/eng-notify.sh nudge`, sent cleanly per
`traces/eng-notify-2026-09-01.log`), stamped `nudged: 2026-09-01T22:41:10`
on each, logged in each ticket's own log. First and only nudge for both.
Nothing else qualified: `ENG-016`'s G1 already nudged this morning;
`ENG-026`'s readback question and the `ENG-007` sequence question are
either under 24h or already nudged; the incident-type items are notices,
not G-gates, and don't nudge — `ENG-013`'s own log already states this
explicitly for the `ENG-023` incident item.

**Dead-end sweep:** chain integrity checked across every ticket at
`ready`/`designed`/`shaped` (`ENG-009`, `010`, `014`, `015`, `017`, `018`,
`019`, `020`, `021`, `022`, `023`, `024`, `025`) — each one's most recent
`chained:` line reads `none` with a valid cap/hold reason; nothing broken.
Ticket count reconciled: 26 board files (`ENG-001`–`ENG-026`), 17 in-flight
plus 9 terminal, no orphans. `agents/qa/bugs/BUG-001` has an owner
(`devops`) and `status: open` — not orphaned, nothing new to do.

**Dispatch: nothing starts.** Machine WIP unchanged, 2/1 (`ENG-009`/
`ENG-010` at `ready`, over cap, shrinking naturally). Approver-facing WIP
unchanged, 3/2 (`ENG-008`, `ENG-013`, `ENG-016` all block it). Every
`shaped`/`designed` ticket's next gate waits on the same cap; `ENG-026`
waits on its own open question. Identical conclusion to both `watch`
passes this morning — nothing here changes it.

**0 ticket-state transitions.** 2 inbox items nudged (`ENG-008`, `ENG-013`
merge requests); 1 incident file closed and corrected; 1 board-prose
correction; 2 observations filed; 1 decision journaled; 1 proposal filed.

`chained: none` — nothing in-flight sits in a state this pass could
legally advance; every ticket is either approver-blocked or capped, same
as both passes before it. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

## 2026-09-01 — watch sweep (~15:46): duplicate fire off the 15:30 scheduled pass's own writes, nothing new

`watch` event pass, context `launchd` — queued while the 15:30 `scheduled`
pass above was still running (1,001s); the queue collapsed 2 duplicate
copies to the oldest before draining it (`traces/eng-loop-2026-09-01.log`,
`15:46:51`). Narrow scope per this event's own contract: sweep the three
watched inboxes only.

Mode check clean (`MODE=active`). Pre-pass `eng-gate-check.sh`,
whole-board: exit 0, clean, no `WAIVED:` lines.

**Traced this fire to its source before treating it as new**, same check
as the ~10:25 entry now in `_index-archive.md`: `traces/.watch-seen`'s
committed fingerprint is still `10:32` (untouched since this morning), so
anything the 15:30 pass itself wrote to a watched inbox during its own run
reads as "changed" against that stale baseline. The 15:30 pass wrote to
three files in `inbox/` during its 1,001s run: the nudge stamps on
`2026-08-31-eng008-merge-request.md` and
`2026-08-31-eng013-merge-request.md` (both `nudged:
2026-09-01T22:41:10`, mtimes `15:41`) and the closing investigation note
appended to `2026-08-31-eng-events-dropped.md` (mtime `15:38`). No other
file across any of the three watched inboxes has an mtime later than
`10:32` this session, apart from
`2026-09-01-eng026-visibility-toggle-question.md` (`10:03`, already
accounted for in the 10:10/10:25 entries) — confirmed with `find`/`stat`
across all three inbox roots, not inferred from the board's own narrative.

**All three inboxes swept anyway**, not trusted from the entries above.
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
their `_handled`/`_processed` archives — nothing loose. `inbox/requests/`
holds only its `.gitkeep`. `inbox/`'s nine loose items re-read directly:
every `decision:` field is still blank (`grep -n "^decision:" inbox/*.md`
— four matches, the `ENG-007` sequence question, `ENG-008` and `ENG-013`
merge requests, `ENG-026` readback question — all empty), and the tails
of the three just-touched files plus `ENG-016`'s G1 confirm nothing was
appended after the automated writes already on record above — no
hand-edit, no reply.

**Nothing re-done.** `ENG-008` and `ENG-013` already nudged this pass
cycle (first and only nudge, per the 15:30 entry) — not renudged.
`ENG-016`'s G1 already nudged this morning — not renudged. The
events-dropped incident is already closed in place. The `ENG-007`
sequence question and `ENG-026`'s readback question are each under 24h
old or already nudged — neither qualifies again.

**Dispatch: nothing starts.** Same caps, unchanged: machine WIP 2/1
(`ENG-009`/`ENG-010` at `ready`, over cap); approver-facing WIP 3/2
(`ENG-008`, `ENG-013`, `ENG-016` all block it, none cleared — no merge,
no decision, no reply since the 15:30 pass). Spot-checked `ENG-008`'s and
`ENG-013`'s own board-file logs: both correctly sit `blocked`/owner
`approver`, not an agent-owned state — nothing here to chain either.

**0 transitions.** No board correction needed this time.

`chained: none` — nothing in this pass's scope sits in a state owned by
an agent; every in-flight ticket is either approver-blocked or capped,
same as the three passes before it. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

## 2026-09-01 — scheduled sweep (20:30): two self-closed incidents get their own closing note; otherwise unchanged

`scheduled` event pass, context `launchd` — the four-times-daily safety
net. Mode check clean (`MODE=active`). Pre-pass `eng-gate-check.sh`,
whole-board: exit 0, clean, no `WAIVED:` lines.

**Business/technical intake:** `agents/product-manager/inbox/` and
`agents/eng-manager/inbox/` hold only their `_handled`/`_processed`
archives; `inbox/requests/` holds only its `.gitkeep`. Nothing new to
shape or route.

**Gate returns:** all nine loose `inbox/` items re-read directly. Every
`decision:` field is still blank, and no file's mtime is newer than
15:41 (the 15:30 pass's own writes) — nothing answered since the 15:46
`watch` pass.

**Merge detection:** checked via `gh pr view` on all four PRs rather than
only local ancestry, since GitHub state is exactly what a local `watch`
can't see between scheduled sweeps. `aiorders-api` #6 and
`aiorders-admin-hub` #5 (`ENG-008`), `aiorders-api` #5 and
`aiorders-admin-hub` #4 (`ENG-013`) — all four still `OPEN`, `mergedAt:
null`. Both tickets unchanged at `blocked`/`blocked_on: approver`.

**Two incident files verified individually and closed in place.**
`inbox/2026-08-30-eng-loop-halted.md` and
`inbox/2026-09-01-eng-gate-violation-watch.md` were each already
correctly investigated and resolved — not a repeat of the false-group-
summary failure from earlier today (that one, on
`2026-08-31-eng-events-dropped.md`, involved a file that was *never*
actually looked at; these two were, individually, by the 09:30 pass's own
"same scheduled pass, continued" entry in `board/_index-archive.md`, and
correctly excluded from that entry's own group claim). Neither had a
closing note appended to the file itself, unlike their
`eng-events-dropped` siblings, so a future pass sweeping `inbox/` fresh
would have no signal short of re-reading the archive. Appended a short
closing note to each, in the same style and pointing back to the archive
record rather than re-deriving it — no new investigation, no decision
required, no nudge (incident notices self-close; they aren't a gate the
approver answers).

**Dispatch: nothing starts.** Same caps, unchanged: machine WIP 2/1
(`ENG-009`/`ENG-010` at `ready`, over cap); approver-facing WIP 3/2
(`ENG-008`, `ENG-013`, `ENG-016` all still block it). No ticket sits in a
state this pass could legally advance.

**Notify sweep:** nothing qualifies. `ENG-008`/`ENG-013`'s merge requests
and `ENG-016`'s G1 were each already nudged once (2026-09-01, per their
own frontmatter) — exactly one nudge, ever. `ENG-007`'s continue-sequence
question was already nudged this morning. `ENG-026`'s readback question
is `notified: 2026-09-01T10:03:26`, ~10.5h old — under the 24h nudge
threshold, correctly left alone.

**Dead-end sweep:** nothing changed since the 15:46 `watch` pass (no new
commits on `origin/main`, no inbox edits besides this pass's own two
closing notes, no merges) — the chain-integrity conclusion it and the
15:30 pass already reached stands unchanged: every `ready`/`designed`/
`shaped` ticket's last `chained:` line reads `none` with a valid cap/hold
reason, nothing broken. Not re-walked ticket by ticket, since re-deriving
an unchanged conclusion from unchanged inputs is exactly the waste this
instance's own proposals already flag.

**0 ticket-state transitions.** 2 incident files closed in place; 1 board
correction (rolled the ~10:25 entry to archive, keeping the cap of three).

`chained: none` — nothing in this pass's scope sits in a state owned by
an agent; every in-flight ticket is either approver-blocked (`ENG-008`,
`ENG-013`, `ENG-016`, `ENG-026`) or WIP-capped (`ENG-009`, `ENG-010`,
`ENG-014`, `ENG-015`, `ENG-017`, `ENG-018`–`ENG-021`, `ENG-022`,
`ENG-023`, `ENG-024`, `ENG-025`), same as every pass today. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

