# Board

**Next ID: ENG-026** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.)

**Machine WIP 1** (`config/config.yaml` → `wip.machine_limit`). **Corrected
2026-08-29 — the approver's direct instruction: one ticket completed end to
end (through `shipped`) before the next one starts, not several tickets each
advanced by one shallow step per pass.** This was 12 (the `max_5x` tier value)
earlier the same day; see that file for the full rationale.

**Currently 1/1 — at cap, not over.** `ENG-009` left this range this pass:
code review round 2, the quality gate, and the security gate all passed
(one three-strike security proposal filed, not blocking:
`agents/principal-engineer/notebook/2026-09-02-security-proposal-verbose-error-response.md`),
then its own devops release-readiness hop opened both PRs
(`aiorders-api#7`, `aiorders-admin-hub#6`, stacked on `ENG-008`'s
still-unmerged branch — see the ticket's own log for why) and moved it to
`blocked`/`blocked_on: approver` — same shape `ENG-008` and `ENG-013` each
already went through on 2026-08-31. `ENG-010` now sits alone at `ready`,
exactly at the cap rather than over it, and holds the one slot until it
itself reaches `shipped` — the cap's own rule, not shrinking-toward-target
phrasing anymore now that the count is no longer over. **No new ticket
enters `ready` until then** — `ENG-014` through `ENG-025` stay at
`designed`/`shaped`/`awaiting-scope` (backlog grooming only, not gated by
this cap) in the meantime.

**15:30 update:** the 15:30 `scheduled` sweep re-checked `ENG-010`'s own
two hold reasons directly (per its own log, both last cited stale
numbers) and found both cleared — `ENG-008`/`ENG-009` are both long past
`in-review` (the sequencing condition), and `ENG-010` is the sole
occupant of the machine-WIP-1 slot, not one waiting behind it. Chained
`continue ENG-010`. Count itself stays 1/1 until that hop actually opens
a branch — see `ENG-010`'s own board file, 2026-09-02 entry.

**16:02 update:** the chained `continue ENG-010` build hop landed —
`ready → building`, both repos, branch `feat/ENG-010-influencer-
relationship-notes` off `ENG-009`'s tip, committed and pushed
(`aiorders-api@d79d963`, `aiorders-admin-hub@f7d8fd7`), no PR opened yet.
Count stays 1/1 (`building` is still inside the counted
`ready`..`ready-to-ship` range) — see `ENG-010`'s own board file for the
full build entry.

**Approver-facing WIP 2 — 4/2, over cap.** `ENG-013`
(`inbox/2026-08-31-eng013-merge-request.md`) and `ENG-008`
(`inbox/2026-08-31-eng008-merge-request.md`) each occupy a slot via their own
L1 merge request — a plain merge on GitHub, no reply needed, clears either.
`ENG-016` occupies a third slot: its own board file and PRD both read
`state`/`status: awaiting-scope`, `owner: approver`, G1 raised and notified
`2026-08-29T23:13:49` (`inbox/2026-08-29-eng016-g1-scope.md`) — the
cross-host board-reconciliation merge (`e281c71`) kept a rival account that
never raised this G1 and showed `shaped`/`product-manager` instead, and
every pass since trusted this table over the ticket's own file, until a
2026-09-01 `watch` pass found it. No `decision-journal.md` entry and no PRD
reset exists for it — checked before concluding this was staleness rather
than a legitimate re-open. Nudged once (2026-08-29, first and only nudge).
**`ENG-009` now occupies a fourth slot**, added this pass: its own devops
release-readiness hop passed all four gates, opened both PRs, and raised
its own L1 merge request
(`inbox/2026-09-02-eng009-merge-request.md`) — same
shape as `ENG-008`/`ENG-013`, not a new start (see the ticket's own log for
why this isn't gated by the cap). Nothing new may start needing the
approver until one of these four clears — already the practical outcome
the last several passes reached, now for the reason that actually holds.

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
| ENG-009 | Influencer engagement info — internal activity signal plus a staff-editable social stat | aiorders-admin-hub | blocked | | approver | S | 2026-09-02 |
| ENG-010 | Influencer relationship notes — staff log for personality, preferences, and off-platform conversations | aiorders-admin-hub | building | | eng-manager | S | 2026-09-02 |
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
| ENG-026 | FoodSwipe multi-channel filters, operational status, and promo badges | restaurant-marketplace | intake | | approver | L | 2026-09-02 |

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

**Approver WIP limit 2 (the only cap — see header above). Currently 4/2,
over.** `ENG-013`'s L1 merge request
(`inbox/2026-08-31-eng013-merge-request.md`) — both PRs open
(`aiorders-api` #5, `aiorders-admin-hub` #4), all four gates passed, no
reply required (merging either PR directly on GitHub is itself the
decision, same as `ENG-005`/`ENG-007`/`ENG-011`); nudged 2026-09-01, first
and only nudge, no merge or reply yet. `ENG-008`'s L1 merge request
(`inbox/2026-08-31-eng008-merge-request.md`) — both PRs open
(`aiorders-api` #6, `aiorders-admin-hub` #5), all four gates passed, same
no-reply-needed shape; nudged the same pass, same first-and-only nudge.
`ENG-016`'s G1 (`inbox/2026-08-29-eng016-g1-scope.md`) — raised and
notified 2026-08-29, nudged once, 2.5+ days overdue. **`ENG-009`'s L1
merge request** (`inbox/2026-09-02-eng009-merge-request.md`) — raised
this morning (~10:51): both PRs open (`aiorders-api` #7,
`aiorders-admin-hub` #6, each stacked on `ENG-008`'s still-open branch
rather than `main` — see the item's own Sequencing section), all four
gates passed, same no-reply-needed shape; still under 24h, not yet due
for a nudge. `ENG-019` through `ENG-021` are G1-drafted and not yet
raised, correctly left for a future pass — the WIP-2 cap is already over,
so none of their G1s may be raised regardless of the (nonexistent)
approval cap this board used to cite.

Separately — not counted in the 4/2 above, same as `ENG-007`'s own
continue-sequence-question: `ENG-026`'s intake-question
(`inbox/2026-09-01-eng026-visibility-toggle-question.md`, title-vs-body
readback ambiguity) doesn't gate this ticket's own shaping the way a
G1/G2/G3/merge does (both intake-questions are explicitly "answer when
convenient," non-blocking). This 15:30 `scheduled` sweep found it past its
true 24h mark under either timestamp reading (naive face-value **and**
the corrected local-time interpretation both land past 24h as of this
pass — see the ticket's own frontmatter) and sent its first, only nudge.

## 2026-09-02 — scheduled sweep (15:30): found and resumed ENG-010's cleared hold; ENG-026 past its true 24h mark, nudged

`scheduled` event pass, context `launchd` — the four-times-daily safety
net. Mode check clean (`MODE=active`, repo-root `.env`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

**Business/technical intake:** `agents/product-manager/inbox/` and
`agents/eng-manager/inbox/` hold only their `_handled`/`_processed`
archives; `inbox/requests/` holds only its `.gitkeep`. Nothing new to
shape or route.

**Gate returns:** all ten loose `inbox/` items checked individually. The
four incident items (`2026-08-30-eng-loop-halted`,
`2026-08-30-eng-events-dropped`, `2026-08-31-eng-events-dropped`,
`2026-09-01-eng-gate-violation-watch`) all carry mtimes from 2026-09-01,
unchanged since the last sweep — still closed, nothing to do. The six
`decision:`-bearing items (`ENG-007` continue-sequence question,
`ENG-008`/`ENG-013`/`ENG-009` merge requests, `ENG-016` G1, `ENG-026`
readback question) all still show `decision:` blank (`ENG-016` still has
no `decision:` key at all, per the standing drift note).

**`ENG-026` re-derived from the trace log rather than trusted from the
prior pass's math, and found past due this time.** Same method as the
09:30 pass: `traces/eng-notify-2026-09-01.log`'s `[10:03:26] sent: ...`
line is still textually identical to the frontmatter's `notified:`,
confirming local time mislabeled as UTC (this host: local PDT, UTC =
local + 7h). True raise = 2026-09-01T17:03:26 UTC. Current UTC
(`22:31:22`) puts elapsed at ~29h28m — past 24h under the corrected
reading. Also checked the naive (face-value) reading for the same
reason the 09:30 pass's finding matters here: naive elapsed is ~36h28m,
also past 24h. **Both readings agree this time**, so the disputed
convention doesn't actually decide this one — nudged
(`lib/eng-notify.sh nudge`, `traces/eng-notify-2026-09-02.log` `15:37:50`)
and stamped `nudged: 2026-09-02T15:37:50` (matching the log line, same
convention every other item on this board already uses — not switched to
a "corrected" UTC value for this one field, which would just introduce a
second, inconsistent convention alongside the existing bug rather than
fix it). First and only nudge, per policy.

**Merge detection.** `git fetch` on both `aiorders-api` and
`aiorders-admin-hub` worktrees; local ancestry checks (`git merge-base
--is-ancestor`) confirm `ENG-008`, `ENG-013`, and `ENG-009` all still
unmerged to `main` on both repos. `gh pr view` on all six PRs confirms the
same: all `OPEN`, `mergedAt: null`. `ENG-009`'s stacked-on-`ENG-008`
relationship re-checked and still intact on both repos (`ENG-008`'s tip is
still an ancestor of `ENG-009`'s tip — no rebase needed). `business-os`
itself: `git fetch` shows 7 ahead / 0 behind `origin/main` — no newer
remote state (e.g. from the Windows host) this pass could be missing.
All three tickets unchanged at `blocked`/`blocked_on: approver`.

**Dispatch — checked every in-flight ticket's own last `chained:` line for
a broken chain, not just the one ticket the last few passes touched**
(this event's own remit: "a chain that broke" is exactly what a whole-
board scheduled sweep exists to catch). All seventeen tickets' board files
read directly. Sixteen of seventeen check out: `ENG-008`/`ENG-009`/
`ENG-013` genuinely still `blocked` on the approver (confirmed above);
`ENG-016`/`ENG-026` genuinely still waiting on an answer; the ten
`designed`/`shaped` backlog tickets (`ENG-014`, `ENG-015`, `ENG-017`–
`ENG-025`) are all correctly held — each needs a G1 or G2 next, and
approver-facing WIP (4/2) is already over cap, so none of those gates may
be raised regardless of what machine-WIP number their own log last cited.

**`ENG-010` was the one exception, and the real finding this pass.** Its
own log's last entry (2026-08-31) cited two hold reasons, both now stale:
a sequencing hold on `ENG-008`/`ENG-009` reaching `in-review` (both are now
long past it, sitting `blocked` at `ready-to-ship`'s far side), and a
machine-WIP hold of "2/1, over" (the true count is now 1/1 — `ENG-009`
left the counted `ready`..`ready-to-ship` range this morning per its own
`continue` hop, and `ENG-010` is the sole remaining occupant, not one
waiting behind it). Both conditions this ticket's log has ever cited are
now satisfied. No branch exists yet, so the actual build hasn't started —
per this loop's own design, a whole-board sweep doesn't start
implementation itself; it hands off. **0 transitions** (state stays
`ready`); full evidence and reasoning in `ENG-010`'s own board file,
2026-09-02 entry.

**Notify sweep:** `ENG-026` nudged (above). `ENG-007`/`ENG-008`/`ENG-013`/
`ENG-016` already nudged once each (spent, no further nudge). `ENG-009`
raised this morning, still under 24h, correctly not yet due.

**Dead-end sweep:** `ENG-010`'s cleared hold (above) is this pass's own
dead-end finding. One additional non-blocking drift noted: six held
tickets (`ENG-014`, `ENG-015`, `ENG-017`, `ENG-022`, `ENG-023`, `ENG-025`)
each cite a superseded machine-WIP count in their own last log line — same
root cause as `ENG-010`'s, but their conclusions are unaffected (each is
still one approver gate away from `ready`, independently barred by the
over-cap approver WIP) — filed as an observation, not a proposal, since
nothing is actually mis-held. No other broken chains found.

**1 ticket dispatched** (`ENG-010`: hold cleared, 0 transitions, chained).
**1 nudge sent** (`ENG-026`). **1 observation filed.** No new proposals.
Rolled the 09:30 scheduled-sweep entry to archive, keeping the live
board's cap of three.

`chained: ENG-010` — sits at `ready`, agent-owned (`eng-manager`), not the
approver, not blocked, not terminal, no cap actually holding it (sole
occupant of the machine-WIP-1 slot). Firing
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-010`
before exiting. Every other in-flight ticket is unchanged: approver-
blocked (`ENG-008`, `ENG-009`, `ENG-013`, `ENG-016`, `ENG-026`) or WIP-
capped behind an over-cap approver gate (`ENG-014`, `ENG-015`, `ENG-017`,
`ENG-018`–`ENG-021`, `ENG-022`–`ENG-025`), `chained: none` for all of
them, same reasons as before. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

## 2026-09-02 — watch sweep (15:47): self-triggered by the 15:30 pass's own ENG-026 nudge-stamp, nothing new

`watch` event pass, context `launchd` — drained immediately behind the
15:30 `scheduled` pass's own exit (`pass end: scheduled (exit 0, 874s)` at
`15:44:41`, per `traces/eng-loop-2026-09-02.log`). Narrow scope per this
event's own contract: sweep the three watched inboxes only, act on what's
new, ignore what's already processed.

Mode check clean (`MODE=active`, repo-root `.env`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

**Traced this fire to its source before treating it as new**, same
discipline as the 10:58 watch entry above and the three duplicate fires
recorded 2026-09-01. `departments/engineering/lib/eng-trigger.sh`'s
`watch_fingerprint()` hashes name+mtime+size of the top-level files in all
three watched inboxes — a hand-edit to an existing gate item changes the
set exactly like a new arrival would. The 15:30 pass's own log entry above
stamped `nudged: 2026-09-02T15:37:50` onto
`inbox/2026-09-01-eng026-visibility-toggle-question.md`; that file's mtime
(`15:37:58`) is the newest of any file in the three inboxes and the only
one newer than the 15:30 pass's own start. No other candidate exists.

**All three inboxes swept anyway, not trusted from the paragraph above.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
their `_handled`/`_processed` archives — nothing loose. `inbox/requests/`
holds only its `.gitkeep`. `inbox/`'s ten loose items, each re-checked
individually:

- The four `gate: incident` items (`2026-08-30-eng-loop-halted`,
  `2026-08-30-eng-events-dropped`, `2026-08-31-eng-events-dropped`,
  `2026-09-01-eng-gate-violation-watch`) all carry mtimes from 2026-09-01,
  unchanged since the last sweep — still closed, nothing to do.
- The six `decision:`-bearing items (`ENG-007` continue-sequence question,
  `ENG-008`/`ENG-013`/`ENG-009` merge requests, `ENG-016` G1, `ENG-026`
  readback question) all still show `decision:` blank (`ENG-016` still
  carries no `decision:` key at all, per the standing drift note). Only
  `ENG-026`'s file has today's newest mtime, and that's the nudge stamp
  traced above, not a reply. `ENG-009` was raised `~10:51`; current time
  `~15:47` puts it at under 5h elapsed under any reading — correctly not
  yet due for its one nudge.

**No merge detection re-run.** The 15:30 pass completed a full `git fetch`
+ ancestry check on both repos eight minutes before this fire; nothing in
the three inboxes changed in that window apart from the traced nudge
stamp, so re-running it here would re-derive the same answer at the cost
of another `git fetch` for no new evidence.

**No dispatch, no chaining.** Nothing in this pass's scope was newly
unblocked, and no ticket was touched: `ENG-010`'s hold-clear and chain
were the 15:30 pass's own action, already recorded there and already
draining (`traces/.pending` held `1 continue ENG-010` behind this fire at
start). Machine WIP unchanged (`ENG-010` alone at `ready`, 1/1);
approver-facing WIP unchanged (4/2, over cap, already named above).

**0 ticket-state transitions.** No new observations, no new proposals —
nothing surfaced that isn't already tracked. Rolled the `continue ENG-009`
entry to archive, keeping the live board's cap of three.

`chained: none` — no ticket in this pass's scope was touched or unblocked;
this pass only confirmed that what already looked settled is in fact
settled. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board: exit 0, clean, no `WAIVED:` lines.

## 2026-09-02 — continue ENG-010 (16:02): built per the design, both repos — now `building`, handed to code review + quality

`continue` event pass, context `ENG-010` — the build hop the 15:30
`scheduled` sweep chained after finding both of this ticket's hold reasons
cleared. Narrow scope per this event's own contract (resume this ticket
from its current state; no board-wide sweep). Mode check clean
(`MODE=active`, repo-root `.env`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
whole-board: both exit 0, clean.

Both `_eng` worktrees already sat on `ENG-009`'s own tip, clean; `git fetch`
confirmed no drift on either. Branched
`feat/ENG-010-influencer-relationship-notes` off that tip in both repos —
this ticket's own sequencing was keyed on `ENG-009` specifically, and
`src/pages/Influencers.tsx` needs `ENG-009`'s own changes present to avoid
branching from a stale copy. New, isolated `influencer_notes` table and a
dedicated handler (`admin-portal/handlers/influencer-notes.ts`, reusing
`hasInfluencerAdminAccess` from `influencers.ts` rather than duplicating the
admin/sub-admin check), routed in `index.ts`; frontend Notes section added
to the existing detail dialog in `src/pages/Influencers.tsx`. No Supabase
MCP tool available this session (unlike `ENG-008`'s/`ENG-009`'s own build
hops) — fell back to static evidence, named explicitly as narrower in the
migration doc; filed as an observation, not assumed to be a lasting change.
Resolved the design's own open question (name-field authority for the
resolved author display name) from the signup trigger's evidence rather
than guessing. Self-tested both repos: 16 new tests passed
(`influencer-notes.test.ts`, including the explicit `role: 'influencer'`
negative-authorization case), the existing 34-test sibling suite unaffected,
whole-tree `deno check` still exactly 17 pre-existing errors none of them
new, `npm run lint`/`build` both at the established pre-existing baseline
with zero new issues. Also brought `supabase/functions/README.md`'s
`admin-portal` entry up to date — found it never documented the
`influencers` routes `ENG-008`/`ENG-009` added, fixed in the same commit
per `aiorders-api/CLAUDE.md`'s own rule, filed as an observation rather than
a proposal since it's already fixed. Both branches committed and pushed
(`aiorders-api@d79d963`, `aiorders-admin-hub@f7d8fd7`); PR bodies drafted,
not opened — devops's release step next. Full detail, evidence, and both
observations: `ENG-010`'s own board file, 2026-09-02 16:02 entry.

**1 transition** (`ready → building`), well under the cap of 4. **Consequence:**
machine WIP unaffected — `building` is still inside the counted
`ready`..`ready-to-ship` range, so the slot count stays 1/1. Approver-facing
WIP and cap both unaffected — no gate touched this hop.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing raised (no gate item — a build hop doesn't
notify); nothing to nudge. **2 observations filed** (`observations.md`): the
missing-MCP-tool finding and the README-documentation-gap finding, both
above.

`chained: ENG-010` — ticket sits at `building`, agent-owned (the build
itself is done; the next hop is code review + quality, combined, per this
loop's own design) — not the approver, not blocked, not terminal, not held
by a cap. Firing
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-010`
before this pass exits. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
whole-board: both exit 0, clean, no `WAIVED:` lines.

