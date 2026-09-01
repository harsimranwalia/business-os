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

**Approver-facing WIP 2 — 2/2, cap reached.** `ENG-013`
(`inbox/2026-08-31-eng013-merge-request.md`) and `ENG-008`
(`inbox/2026-08-31-eng008-merge-request.md`) each occupy a slot via their own
L1 merge request, both PRs linked. Nothing new starts that will need this WIP
until one clears — a plain merge on GitHub, needing no reply, does that for
either.

**Approval cap 3 — 2/3.** Same two merge requests occupy two slots. One slot
free — `ENG-016` through `ENG-021` are also G1-drafted and ready, but
deliberately left for a future pass rather than filling every open slot in
one sweep; see `ENG-023`'s own ticket log for the reasoning.

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
| ENG-009 | Influencer engagement info — internal activity signal plus a staff-editable social stat | aiorders-admin-hub | building | | eng-manager | S | 2026-08-30 |
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
  states ENG-016 through ENG-021 are G1-drafted but not yet raised. -->
| ENG-016 | Catering page — self-serve quote generator, with automatic stage update | config-site-builder | shaped | next | product-manager | L | 2026-08-29 |
| ENG-017 | Autopilot nurture for the presignup sales lead pipeline — stage-triggered email/SMS | aiorders-api | shaped | | product-manager | L | 2026-08-29 |
| ENG-018 | Sales demonstration account — a fully seeded AIOrders environment to show prospects | aiorders-admin-hub | shaped | hold | product-manager | L | 2026-08-29 |
| ENG-019 | Restaurant self-service marketing broadcasts — mass send and drip sequences, scheduled or immediate | restaurant-portal | shaped | | product-manager | L | 2026-08-29 |
| ENG-020 | Marketing ROI reporting — traffic source and revenue attribution on the brand dashboard | restaurant-portal | shaped | | product-manager | M | 2026-08-29 |
| ENG-021 | Website chat-bar engagement visibility — customer questions and self-service FAQ editing on the brand portal | restaurant-portal | shaped | | product-manager | M | 2026-08-29 |
| ENG-022 | Fix broken restaurant-scoped access check on 5 brand-portal handlers — cross-tenant PII/write exposure | aiorders-api | designed | | eng-manager | M | 2026-08-29 |
| ENG-023 | Add status and internal notes to each brand-portal feedback item | restaurant-portal | designed | | architect | S | 2026-08-31 |
| ENG-024 | Set show_in_marketplace on onboarding's createRestaurant insert, plus a backfill | aiorders-api | shaped | | eng-manager | XS | 2026-08-29 |
| ENG-025 | Recurring feedback issues, per restaurant, over time | restaurant-portal | designed | | architect | S | 2026-08-31 |

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

Cap: 3 across all gates. **2/3.** `ENG-013`'s L1 merge request
(`inbox/2026-08-31-eng013-merge-request.md`) — both PRs open
(`aiorders-api` #5, `aiorders-admin-hub` #4), all four gates passed, no
reply required (merging either PR directly on GitHub is itself the
decision, same as `ENG-005`/`ENG-007`/`ENG-011`). `ENG-008`'s L1 merge
request (`inbox/2026-08-31-eng008-merge-request.md`) — both PRs open
(`aiorders-api` #6, `aiorders-admin-hub` #5), all four gates passed, same
no-reply-needed shape. `ENG-016` through `ENG-021` are also G1-drafted and
ready to raise, deliberately left for a future pass rather than filling
every open slot in one sweep — see `ENG-023`'s own ticket log for the
reasoning.

## 2026-08-31 — continue ENG-008: release-readiness — both PRs opened, now blocked on the approver

`continue` event pass, context `ENG-008`, this fire's own turn at the front
of `traces/.pending` — queued by the security-gate pass above and drained
right behind `continue (ENG-013)`. Narrow scope per the event's own contract
(resume this ticket from its current state; no board-wide sweep). Mode check
clean (`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean.

Verified all four upstream gates fresh from the receipt files: migration,
code review (round 2), quality, security — all **pass**. Both worktrees were
already clean on this ticket's own branch at the recorded commits
(`aiorders-api@57f8c4b`, `aiorders-admin-hub@63be255`), already pushed;
confirmed no PR already existed on either repo. Same L1 readiness-gate
interpretation `ENG-007`/`ENG-013` already established (rollback reasoned
through but not live-tested, $0 cost, existing `console.error` logging as
observability, window check n/a). Opened both (`aiorders-api` first):
PR #6 (https://github.com/harsimranwalia/aiorders-api/pull/6), PR #5
(https://github.com/harsimranwalia/aiorders-admin-hub/pull/5).

Wrote the L1 merge-request item
(`inbox/2026-08-31-eng008-merge-request.md`), `pr_urls:` YAML-list format.
Notify sent cleanly. State → `blocked`, `blocked_on: approver`,
`blocked_from: ready-to-ship`, owner `devops → approver`.

**1 transition** (`ready-to-ship → blocked`). **Consequence:** `machine_wip`
3/1 → 2/1 (`ENG-008` leaves the counted `ready`..`ready-to-ship` range —
`ENG-009`/`ENG-010` at `ready` are all that's left inside it). Approver-facing
WIP 1/2 → 2/2 (**cap reached**); approval cap 1/3 → 2/3.

`chained: none` — `blocked`, `blocked_on: approver`. This is the human gate
the whole hop was driving toward; firing `continue ENG-008` again would only
queue against a ticket with nothing left for a machine to do. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-31 — scheduled sweep: no merges yet, stale sequencing-hold reason on ENG-009/ENG-010 corrected

`scheduled` event pass, context `launchd` — the 15:30 safety-net sweep.
Whole-board scope per this event's own contract. Mode check clean
(`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board (invoked with `ENG_ROOT` set to this instance explicitly — the
bare form resolves against the department root, not an instance, and reads
as `PARSE:` on a bad argument rather than a clean sweep): exit 0, clean, no
`WAIVED:` lines.

**Inboxes not re-swept — a `watch` pass covered this ground 8 minutes
earlier** (`traces/eng-loop-2026-08-31.log`, `11:22:21`, exit 0):
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` empty;
`inbox/requests/` empty; `inbox/` holds only the two fresh merge-request
items (both `decision:` still blank) and the already-closed 2026-08-30
dropped-events notice. Re-confirmed the same read fresh rather than trusting
the log entry alone — all three still true at this pass's own start.

**Merge detection — the part an inbox-only pass cannot do.** `git fetch
origin main` on both `_eng` worktrees (both clean, both still sitting on
`ENG-008`'s branch, no uncommitted changes), then `git merge-base
--is-ancestor` for all four PR branch heads against `origin/main`:
`aiorders-api@57f8c4b` (ENG-008), `aiorders-admin-hub@63be255` (ENG-008),
`aiorders-api@c95b25b` (ENG-013), `aiorders-admin-hub@a1c3bdf` (ENG-013) —
**none merged.** Both tickets remain `blocked`/`blocked_on: approver`,
unchanged.

**Dead-end sweep (whole board).** Tabulated `state`/`owner`/last `chained:`
for all 25 tickets: every non-terminal ticket's last recorded chain decision
is `none`, and in every case the reason still holds today (approver-blocked,
or held by the machine-WIP/approval caps) — no silently-broken chain found.

**One stale-but-superseded hold reason found and corrected, not a break.**
`ENG-009` and `ENG-010`'s own logs both still cite their original hold
reason verbatim — "held pending `ENG-008` reaching `in-review` or later" —
which `ENG-008` satisfied hours ago (round 2 review, quality, security, and
release-readiness all since passed; it's now `blocked` on the approver's
merge). Re-verified before concluding anything: machine WIP is still 2/1
(only `ENG-009`/`ENG-010` occupy the counted `ready..ready-to-ship` range now
that `ENG-008`/`ENG-013` both left it for `blocked`), still over the cap the
approver set 2026-08-29, still the reason nothing may start building. So the
*conclusion* (stay at `ready`, do not start) is still correct — only the
*stated reason* had gone stale, exactly the shape a whole-board sweep exists
to catch and a narrowly-scoped `continue`/`watch` pass cannot. Corrected in
both tickets' own logs rather than left to read, to a future pass, as a hold
that had quietly lapsed.

**Dispatch: nothing starts.** Machine WIP 2/1 (over cap, unchanged) — no new
ticket may enter `ready`, and the two already there stay un-built per the
correction above. Approver-facing WIP 2/2 (cap reached) and approval cap 2/3
(one free) — consistent with `ENG-023`'s and `ENG-025`'s own established
reasoning, the one free approval-cap slot is deliberately not spent raising
`ENG-016`'s G1 in the same sweep that's still carrying two live merge
requests; nothing material changed to revisit that call.
`ENG-014`/`ENG-015`/`ENG-022`/`ENG-023`/`ENG-024`/`ENG-025` remain at
`designed`/`shaped` — backlog grooming only, not gated by the WIP cap, but no
fresh shaping work is due on any of them this pass.

**Notify sweep:** both open merge requests notified today (11:05, 11:15) —
well under the 24h nudge threshold, nothing to nudge. Approval cap not full
(2/3) — no stall condition.

**0 transitions.** No cap changes.

`chained: none` — `ENG-008`/`ENG-013` wait on the approver; `ENG-009`/
`ENG-010` wait on the machine-WIP cap; every other ticket is capped backlog.
Nothing on the board is in a state this pass could legally hand to another
agent. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board: exit 0, clean, no `WAIVED:` lines.

## 2026-09-01 — scheduled sweep (09:30): no merges yet, inbox-filing-rule gap escalated to a proposal

`scheduled` event pass, context `launchd` — the 09:30 safety-net sweep.
Whole-board scope per this event's own contract. Mode check clean
(`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board (`ENG_ROOT` set explicitly to this instance): exit 0, clean, no
`WAIVED:` lines.

**Inboxes fresh-checked, not trusted from the 02:00 pass's record.**
`agents/product-manager/inbox/`, `agents/eng-manager/inbox/`, and
`inbox/requests/` all still empty. `inbox/` holds the same three items the
last four passes have seen: `ENG-008`/`ENG-013` merge requests (`decision:`
both still blank) and the self-closed `2026-08-30-eng-events-dropped.md`
notice.

**Merge detection.** `git fetch origin main` on both `_eng` worktrees (both
clean, no uncommitted changes), then `git merge-base --is-ancestor` for all
four PR branch heads against `origin/main`: `aiorders-api@57f8c4b` /
`aiorders-admin-hub@63be255` (`ENG-008`), `aiorders-api@c95b25b` /
`aiorders-admin-hub@a1c3bdf` (`ENG-013`) — **none merged.** Both tickets
remain `blocked`/`blocked_on: approver`, unchanged.

**Dead-end sweep.** Zero events fired between the 02:00 pass's own end
(`02:07:54`) and this pass's start (`09:30:05`) — confirmed from
`traces/eng-loop-2026-09-01.log` directly, not assumed — so the exhaustive
whole-board tabulation from 08-31/02:00 still holds. Spot-checked
`ENG-009`/`ENG-010`'s hold reason (machine-WIP cap, 2/1, over) against both
tickets' own logs: still accurate, nothing further gone stale.

**One proposal filed, not another observation.**
`inbox/2026-08-30-eng-events-dropped.md` has now been re-read and reached
the identical "fully investigated, below P0, nothing to do" conclusion by
four consecutive passes (08-31 20:19 `watch`, 08-31 20:30 `scheduled`,
09-01 02:00 `scheduled`, this one) — the exact threshold the 02:00 pass's
own `observations.md` row named as the point to escalate from another
observation to a proposal. Filed to `proposals.md`: `eng_build_loop.md` has
no rule for when a self-closed (no-`decision:`-field) incident notice may
leave `inbox/` for `_handled/`, so nothing short of a procedure change stops
a fifth pass from repeating this. The item itself is left exactly where it
is — the proposal changes the *rule*, not this pass's own unilateral
authority to act on it.

**Dispatch: nothing starts.** Machine WIP 2/1 (over cap, unchanged) —
`ENG-009`/`ENG-010` stay at `ready`. Approver-facing WIP 2/2 (**cap
reached**) — `ENG-016` through `ENG-021` stay un-raised; worth stating
plainly rather than repeating the 08-31 entry's softer framing: raising any
of their G1s would move that ticket to `awaiting-scope`, which needs a free
approver-facing-WIP slot (confirmed against `ENG-009`'s own log, where
exactly this state change was counted against this same cap) — so this is
now cap-enforced, not merely a courtesy stagger, until `ENG-008` or
`ENG-013` clears. Approval cap 2/3 (one free) is moot while the WIP-2 cap
binds first. No other ticket has new information to act on this pass.

**0 transitions.** No cap changes.

`chained: none` — `ENG-008`/`ENG-013` wait on the approver; `ENG-009`/
`ENG-010` wait on the machine-WIP cap; everything else is capped backlog
with no fresh input. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board: exit 0, clean, no `WAIVED:` lines.

