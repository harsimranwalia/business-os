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
decision, same as `ENG-005`/`ENG-007`/`ENG-011`). `ENG-008`'s L1 merge
request (`inbox/2026-08-31-eng008-merge-request.md`) — both PRs open
(`aiorders-api` #6, `aiorders-admin-hub` #5), all four gates passed, same
no-reply-needed shape. **`ENG-016`'s G1**
(`inbox/2026-08-29-eng016-g1-scope.md`) — raised and notified 2026-08-29,
missing from this section until this pass (see the header note above for
why); nudged this pass, first nudge, 2.5 days overdue. `ENG-019` through
`ENG-021` are G1-drafted and not yet raised, correctly left for a future
pass — the WIP-2 cap is already over, so none of their G1s may be raised
regardless of the (nonexistent) approval cap this board used to cite.

## 2026-09-01 — same scheduled pass, continued: a git pull mid-pass surfaced two days of the other host's backlog

Still the 09:30 `scheduled` pass above — recorded as a second dated entry
rather than folded into the first because what follows was discovered
*after* that entry was written and pushed, from a `git pull` this pass
triggered itself (a `git fetch`/ancestor re-check before allocating a new
ticket id) that fast-forwarded local `main` through merge commit `e281c71`
("reconcile 26 diverged engineering-board files") and a follow-up commit
from this instance's Windows host. Confirmed via `git reflog` before acting
on any of it, not assumed from file contents alone.

**Root cause of why this was still sitting unseen**:
`inbox/2026-09-01-eng-events-dropped.md` (itself newly arrived, already
answered `decision: approved` by the time it appeared) documents ~7.5 hours
of continuous `watch schtasks` failures (exit 1, `00:05`–`07:45` today) on
that host, including the two fires that would have processed a new
PM-inbox request and `ENG-017`'s answered G1. Recovery confirmed via git
history (two successful pushes at `09:17`/`09:28` local from the same host
identity) — investigated and moved to `_handled/`, full detail in that
file's own footer and `observations.md`.

**Both concrete drops recovered by hand, in this pass:**

- **`ENG-017`'s G1** (`decision: approved`, with a UI rider) — journaled,
  design written (`agents/architect/designs/
  ENG-017-presignup-lead-nurture-autopilot.md`, dispatched a read-only
  investigation of both live repos first rather than trusting the PRD's own
  evidence unverified — found one correction: `ENG-013` is not on `main`,
  still unmerged). `awaiting-scope → designed`. **Does not advance to
  `ready`** — machine WIP is 2/1 (`ENG-009`/`ENG-010`), already over cap;
  starting a third ticket into that band would compound the violation
  rather than let it shrink. No one-way door; the one real risk (CASL
  consent exposure on unsolicited nurture sends) is named prominently in
  the design with both the consent column and the feature's own on/off
  toggle defaulted **off**, rather than the design silently deciding a
  legal question the approver hasn't weighed in on.
- **A new PM-inbox request** (brand-portal/FoodSwipe: multi-channel filters,
  operational status, promo badges) — filed `ENG-026`. Full request-readback
  run (PM reading + blind architect subagent reading, no repo access, not
  shown the PM's reading): **one material divergence found** — the
  request's own title asks for an independent per-channel visibility
  toggle, but none of its three body tasks build one, and both readers
  independently noticed the gap unprompted. Asked one question, framed as a
  two-reading choice; held at `intake`. This is a standing, non-blocking
  question (same shape as `ENG-007`'s), so it costs neither the
  approver-facing WIP cap nor the approval cap — unlike a G1, nothing here
  is confirmed enough yet to raise one.

**Other new-to-this-host items, all already resolved or correctly
inert — no further action taken:**
`inbox/2026-09-01-eng-gate-violation-watch.md` (a Windows-host frontmatter
PARSE failure on 8 ticket files, already fixed by `e281c71`'s own BOM strip
— this pass's fresh `eng-gate-check.sh` runs confirm clean, corroborating
rather than re-fixing); `inbox/2026-08-30-eng-loop-halted.md` (a daily
hop-ceiling halt, two days moot, clears at midnight by design);
`inbox/2026-08-30-eng007-continue-sequence-question.md` (a real, still-open,
non-blocking question, now 3+ days old — **nudged** this pass, stamped
`nudged:`); `agents/eng-manager/inbox/_processed/
2026-08-29-restaurant-detail-write-partner-exposure.md` (an EM-finding
already fully routed to `proposals.md` by the other host — found it
substantially overlaps the 2026-08-31 `updateBrandOwner()` row already on
this board; flagged in `observations.md` rather than merged/deleted
unilaterally).

**2 transitions this entry** (`ENG-017`: `awaiting-scope → designed`;
`ENG-026`: `(new) → intake`), on top of the 0 from the entry above — both
well under each ticket's own cap of 4. **Consequence:** no cap numbers
change — neither `designed` nor a standing intake-question is counted
anywhere.

`chained: none` — `ENG-017` held by the machine-WIP cap; `ENG-026` held by
its own open question, owned by the approver. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean,
no `WAIVED:` lines. Re-verified `ENG-008`/`ENG-013` merge status fresh one
more time before finishing (fetch + ancestor check, both repos): still not
merged.

## 2026-09-01 — watch sweep (~10:10): the approver-facing WIP cap was actually 3/2, not 2/2

`watch` event pass, context `launchd` — one of 7 duplicate `watch (launchd)`
fires queued while the 09:30 `scheduled` pass above was still running
(2,409s); the queue collapsed all 7 to the oldest copy before draining it
(`traces/eng-loop-2026-09-01.log`, `10:10:16`). Narrow scope per this
event's own contract: sweep the three watched inboxes, act on what's new,
ignore what's already processed — no whole-board dead-end sweep.

Mode check clean (`MODE=active`).

**All three inboxes swept fresh.** `agents/product-manager/inbox/` and
`agents/eng-manager/inbox/` both empty (archives only). `inbox/`'s nine
items all re-read directly rather than trusted from the pass above: two
open G1s (`ENG-016`, see below; `ENG-026`'s standing readback question),
two open merge requests (`ENG-008`, `ENG-013`), and three self-closed
incident notices plus one already-nudged question the pass above had
already investigated to conclusion the same morning
(`2026-08-30-eng-loop-halted.md`, `2026-08-30`/`2026-08-31-eng-events-dropped.md`,
`2026-09-01-eng-gate-violation-watch.md`, `2026-08-30-eng007-continue-sequence-question.md`)
— none carries a `decision:` filled in or content postdating that pass's own
read; not re-investigated, since doing so would repeat the exact waste that
pass's own proposal was filed to stop.

**Merge detection re-run anyway**, since `ENG-008`/`ENG-013`'s merge-request
files are literally the inbox items being swept: `git fetch origin main`
plus the `ENG-013` branch on both `_eng` worktrees (both clean, no
uncommitted changes), then `git merge-base --is-ancestor` for all four PR
branch heads against `origin/main` — same four commits the pass above
verified (`aiorders-api@57f8c4b`/`aiorders-admin-hub@63be255` for `ENG-008`,
`aiorders-api@c95b25b`/`aiorders-admin-hub@a1c3bdf` for `ENG-013`) — **none
merged.** Both tickets remain `blocked`/`blocked_on: approver`, unchanged.

**One real finding: `ENG-016`'s own board file and PRD disagreed with this
index.** Both read `awaiting-scope`/`owner: approver`, G1 raised and
notified `2026-08-29T23:13:49` — this index's In-flight table and "Waiting
on the approver" section instead read `shaped`/`product-manager`, "G1
drafted, ready to raise," carried forward unquestioned since the 09:30
pass's cross-host merge (`e281c71`) kept a rival host's account of this row
specifically. Checked `decision-journal.md` (no `ENG-016` row) and the
PRD's own `status:` before treating this as staleness rather than a
legitimate reset — neither shows one. **Consequence, not cosmetic:**
approver-facing WIP was actually 3/2 (`ENG-008`, `ENG-013`, `ENG-016` all
have a path running through the approver), not the 2/2 this index claimed —
and the G1 itself sat un-nudged for 2.5 days because every intervening pass
trusted this table over the ticket's own file. Corrected in place (header
WIP accounting, In-flight row, "Waiting on the approver" section) and in
`ENG-016`'s own log; nudged the G1 (`nudged: 2026-09-01T10:20:06`, first
nudge). Filed a proposal (`proposals.md`) so the next cross-host merge
re-derives this table from each ticket's own frontmatter rather than
keeping one side's account wholesale.

**Dispatch: nothing starts.** No ticket sits in a state this pass could
legally advance: `ENG-008`/`ENG-013`/`ENG-016` all wait on the approver
(WIP 3/2, over); `ENG-009`/`ENG-010` wait on the machine-WIP cap (2/1,
unchanged); every `shaped`/`designed` ticket's own next gate waits on the
same approver-WIP cap; `ENG-026` waits on its own open question. The
`ENG-016` correction doesn't change any dispatch outcome — the last two
passes already declined to raise a new G1 this cycle, just for a reason
that wasn't quite right.

**0 transitions.** No ticket changed state. **1 board correction** (the
`ENG-016` row above).

`chained: none` — every in-flight ticket is either approver-blocked or
capped; nothing sits in a state owned by an agent. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

## 2026-09-01 — watch sweep (~10:25): duplicate fire off the prior pass's own nudge write, nothing new

`watch` event pass, context `launchd` — drained immediately behind the
"watch sweep (~10:10)" pass above (`traces/eng-loop-2026-09-01.log`,
`10:25:05`, 2s after that pass's own end). Narrow scope per this event's
own contract: sweep the three watched inboxes only.

Mode check clean (`MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (`ENG_ROOT`
set explicitly to this instance): exit 0, clean, no `WAIVED:` lines.

**Traced this fire to its source before treating it as a new arrival.**
`.watch-seen`'s committed fingerprint is captured before a watch pass runs
and written only after it succeeds (`eng-trigger.sh`, ENG-005), so an inbox
edit a pass makes *during* its own run changes the live fingerprint out
from under that stale baseline and can queue a fresh fire against itself.
The pass above wrote exactly one thing to a watched inbox during its 886s
run — the nudge stamp on `inbox/2026-08-29-eng016-g1-scope.md` (`nudged:
2026-09-01T10:20:06`) — and every other file across all three inboxes is
unchanged since before that pass started (checked mtimes directly, not
inferred).

**All three inboxes re-swept anyway, not trusted from the entry above.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` both hold
only their `_handled`/`_processed` archives, nothing loose. `inbox/`'s nine
items re-read directly: all nine `decision:` fields still blank or absent —
nothing answered since the pass above. `inbox/requests/` empty.

**Nothing re-done.** `ENG-016` already corrected and nudged (one nudge,
ever — not repeated); its proposal already filed; the self-closed incident
notices and the `ENG-007`-sequence question already investigated to
conclusion and already nudged respectively, by the pass above or earlier
ones. Re-verifying and re-acting on unchanged state is the exact waste the
09:30 pass's own proposal (now archived above) was filed to stop.

**Dispatch: nothing starts.** Same caps, unchanged: machine WIP 2/1 (over),
approver-facing WIP 3/2 (over) — `ENG-008`, `ENG-013`, `ENG-016` all still
block it. No ticket sits in a state this pass could legally advance.

**0 transitions. No board correction needed this time.**

`chained: none` — nothing in this pass's scope sits in a state owned by an
agent; every in-flight ticket is either approver-blocked or capped, same as
the pass immediately above. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

