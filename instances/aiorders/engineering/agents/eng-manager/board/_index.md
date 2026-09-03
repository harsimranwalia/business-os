# Board

**Next ID: ENG-027** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.)

**Machine WIP 1** (`config/config.yaml` → `wip.machine_limit`). **Corrected
2026-08-29 — the approver's direct instruction: one ticket completed end to
end (through `shipped`) before the next one starts, not several tickets each
advanced by one shallow step per pass.** This was 12 (the `max_5x` tier value)
earlier the same day; see that file for the full rationale.

**Currently 0/1 — free.** `ENG-008` left this range this `continue` pass: its
round-3 code review, quality, and security all passed (chained straight
through from the `watch` sweep's `blocked → building` routing), then its own
devops release-readiness hop refreshed both PR bodies to the revised shape
and raised a fresh L1 merge request, sending it `ready-to-ship → blocked`/
`blocked_on: approver`. Nothing occupies the counted `ready`..`ready-to-ship`
range right now — the next To-do-column start (priority order) may take this
slot on a future pass. `ENG-010` left this same range earlier tonight (code
review round 3 pass, quality, security, then its own devops
release-readiness hop opened both PRs and moved it to
`blocked`/`blocked_on: approver`); `ENG-014` through `ENG-025` stay at
`designed`/`shaped`/`awaiting-scope` (backlog grooming only, not gated by
this cap) in the meantime. Full build/review/qa/security trace for
`ENG-010`: its own board file.

**Approver-facing WIP 2 — 5/2, over cap.** Recomputed in full earlier tonight
after discovering that three of the five items previously counted here had
actually already been answered — on a different host/checkout, invisible
to this Mac until tonight's `1b72b26` merge finally reconciled it. **An
item stops counting the moment the approver answers it, not once the
department finishes acting on the answer** — the cap protects the
approver's attention, and an answered item has already had that attention
spent, however much processing debt it leaves behind.

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
- `ENG-013` — its *original* merge request was also answered `changed`
  (2026-09-01) and is now closed; **but this pass raised a fresh question
  on the same ticket** (`inbox/2026-09-02-eng013-stage-config-question.md`,
  unanswered) to resolve a genuine ambiguity in that reply. Stays counted,
  via the new item, not the old one.
- `ENG-016` — its G1 was also answered `changed`, this evening
  (`inbox/2026-08-29-eng016-g1-scope.md`), a full rewrite of the ticket's
  own scope, not yet processed (see "Waiting on the approver" below for why
  this pass didn't attempt it). **Off the approver-facing count** — the
  approver has already spoken — but very much NOT off this department's own
  to-do list; flagged explicitly so it isn't mistaken for either.
- `ENG-009` — its own devops release-readiness hop passed all four gates,
  opened both PRs, and raised its own L1 merge request
  (`inbox/2026-09-02-eng009-merge-request.md`), still unanswered. Counted.
- `ENG-010` — same shape, still unanswered
  (`inbox/2026-09-02-eng010-merge-request.md`). Counted.
- `ENG-026` — new this pass: its standing intake-question (open since
  2026-09-01) was answered by hand, the PM completed its shaping in the
  same pass, and its own G1 was raised
  (`inbox/2026-09-02-eng026-g1-scope.md`), unanswered. Counted, same
  precedent `ENG-016`'s own G1 already set (an `awaiting-scope` ticket with
  a raised G1 counts the same as a merge request) — not a new start either
  way, since `ENG-026`'s shaping was already in flight since 2026-09-01.

Five unanswered items genuinely on the approver's plate right now:
`ENG-008` (fresh merge request), `ENG-009`, `ENG-010`, `ENG-013` (new
question), `ENG-026`. Nothing new may start needing the approver until one
of these five clears.

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
| ENG-008 | Influencer board admin management — region/campaign-type preference, rating, collaboration count | aiorders-admin-hub | blocked | | approver | M | 2026-09-02 |
| ENG-009 | Influencer engagement info — internal activity signal plus a staff-editable social stat | aiorders-admin-hub | blocked | | approver | S | 2026-09-02 |
| ENG-010 | Influencer relationship notes — staff log for personality, preferences, and off-platform conversations | aiorders-admin-hub | blocked | | approver | S | 2026-09-02 |
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
| ENG-026 | FoodSwipe channel-visibility toggles and capability-based discovery | restaurant-marketplace | awaiting-scope | | approver | M | 2026-09-02 |

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

**Approver WIP limit 2 (the only cap — see header above). Currently 5/2,
over** — see the header's own recomputation for why this reads lower than
this pass briefly recorded it. **`ENG-008`'s L1 merge request, revised**
(`inbox/2026-09-02-eng008-merge-request.md`) — raised tonight (~23:24):
both PRs updated in place (`aiorders-api` #6, `aiorders-admin-hub` #5, same
PR numbers as the original request), bodies rewritten to describe the
corrected diff, all four gates passed on round 3; not yet due for a nudge.
**`ENG-009`'s L1 merge request**
(`inbox/2026-09-02-eng009-merge-request.md`) — raised this morning
(~10:51): both PRs open (`aiorders-api` #7, `aiorders-admin-hub` #6, each
stacked on `ENG-008`'s branch rather than `main`), all four gates passed,
no reply required (merging either PR directly on GitHub is itself the
decision); still under 24h, not yet due for a nudge. **`ENG-010`'s L1
merge request** (`inbox/2026-09-02-eng010-merge-request.md`) — raised this
evening (~17:45): both PRs open (`aiorders-api` #8, `aiorders-admin-hub`
#7, each stacked on `ENG-009`'s branch), all four gates passed, same
shape; not yet due for a nudge. **`ENG-013`'s stage-configuration
question** (`inbox/2026-09-02-eng013-stage-config-question.md`) — raised
this pass (~22:34): its original merge request came back `changed`
("meant to allow custom pipeline stages... not just per card"), and
whether to ship the already-built per-card override now (filing custom
stage definitions separately) or hold for one combined ship is genuinely
unclear from the reply alone — asked as one question rather than guessed.
**`ENG-026`'s G1** (`inbox/2026-09-02-eng026-g1-scope.md`) — raised this
pass (~22:19): the approver's own hand-edited answer to its standing
intake-question confirmed a per-channel visibility toggle and specified it
completely; PM scoped the ticket to that piece alone (three other bundled
capabilities named as deferred future tickets).

**Answered, but not yet actioned — flagged so it isn't lost, not counted
above since the approver has already spoken:** `ENG-016`'s G1
(`inbox/2026-08-29-eng016-g1-scope.md`) came back `changed` this evening —
not a small edit but a complete, detailed replacement spec for the whole
quote-generator flow (categorized menu selection, package-based pricing,
guest-count-driven fulfillment options, a three-way kanban stage mapping),
materially different from the PRD this G1 originally raised. This `watch`
pass deliberately did not attempt the rewrite: shaping a PRD of this size
correctly is its own dedicated unit of work, not something to fold into an
already-large inbox sweep alongside everything else this pass touched. Left
exactly as answered, for a `watch`/`scheduled` pass with room to do it
justice. **`ENG-007`'s continue-sequence-question**
(`inbox/2026-08-30-eng007-continue-sequence-question.md`) also came back
answered (**yes** — file ticket 3, the loyalty points ledger, per
`ENG-006`'s own named five-ticket sequence) and is similarly not yet
actioned, for the same reason — a fresh PRD/readback/G1 cycle, not a quick
edit. Neither of these two was ever counted toward the WIP-2 cap above (a
standing question and a G1 don't gate the same way once answered — the
first was never gating, and `ENG-016`'s G1 stopped gating the moment it was
answered), so leaving them for a subsequent pass costs nothing on that
front; it costs only their own delay.

`ENG-019` through `ENG-021` are G1-drafted and not yet raised, correctly
left for a future pass — the WIP-2 cap is already over, so none of their
G1s may be raised regardless of the (nonexistent) approval cap this board
used to cite.

## 2026-09-02 — watch sweep (~22:00–22:35): a whole day of cross-host decisions surfaced at once, four resolved, two deliberately left for a dedicated pass

`watch` event pass, context `launchd`. **This is a retry, not a fresh
fire** — the same `watch launchd` event first launched at 21:27, ran a
long read-only investigation, and failed at 21:36
(`Failed to authenticate: OAuth session expired`), re-queued as attempt 2.
Nothing from that attempt persisted to disk (its own transcript shows only
`Read`/`Bash` calls, no `Edit`/`Write`), so this attempt re-derived
everything from scratch rather than trusting that attempt's own narration —
including its claim about a git merge conflict, which turned out to be
already resolved and irrelevant by the time this attempt checked fresh.

Mode check clean (`MODE=active`). Confirmed no merge in progress
(`MERGE_HEAD` absent) and — correcting a misreading of my own mid-pass —
`origin/main` is **not** ahead of local `HEAD`; local is 11 commits ahead,
origin has nothing local lacks. No pull needed.

**Why so much surfaced at once.** Tonight's `1b72b26` merge (a plain `git
pull`-style merge, timestamp `21:27:45`, outside any build-loop pass)
reconciled this Mac's history with a different host/checkout for the first
time since several of today's items were actually decided. Six inbox items
that every local pass today (09:30, 15:30, 17:52, 20:30) had correctly
reported as `decision:` blank were, in fact, already answered — five of
them a full day ago (2026-09-01, ~09:37–10:14 local), one this evening. No
prior pass failed to notice anything; the content genuinely was not on this
Mac until this merge. Caught by re-verifying every loose item's frontmatter
directly rather than trusting the 20:30 entry's own account of it, which
this pass initially (briefly) did not do carefully enough for the four
larger items below.

**Closed, four incidents** (all `gate: incident`, all reached via the same
merge): `2026-08-30-eng-events-dropped.md` (rejected; 69 entries over ~17h,
3 real ticket-chain drops all independently recovered, root cause since
fixed), `2026-08-31-eng-events-dropped.md` (rejected; 48 entries, all
routine polls, same root cause), `2026-09-01-eng-gate-violation-watch.md`
(rejected; already carried a finished investigation, re-confirmed still
true), `2026-09-01-eng-events-dropped-b.md` (rejected; 2 entries, the
one non-routine drop moot since this same pass independently processed the
file it named — `-b` suffix because this date's own filename collided with
an earlier, unrelated, already-closed incident of the same name; see the
near-miss note below). The sustained ~2-day near-continuous Windows-host
(`schtasks`) failure window these describe is now understood: fixed
tonight by `469e548`'s lock-staleness correction, itself the same fix that
closed this pass's fifth incident, `2026-09-02-eng-loop-stalled.md`
(no `decision:` — self-raised, closed on evidence rather than
Windows-host access this Mac doesn't have).

**Resolved, two merge requests answered `changed`:** `ENG-008`
(`inbox/_handled/2026-08-31-eng008-merge-request.md`) — objected to a
redundant new column (`accepts_barter` duplicating the existing
`barter_visit`); a narrow, mechanical fix, so routed straight to
`building` (`blocked → building`) rather than back to `designed`, and
chained. `ENG-013` (`inbox/_handled/2026-08-31-eng013-merge-request.md`)
— surfaced a real ambiguity instead (ship the built per-card override and
file custom stage-definitions separately, or hold for one combined ship);
asked rather than guessed
(`inbox/2026-09-02-eng013-stage-config-question.md`), ticket stays
`blocked`/`blocked_on: approver`.

**Shaped, one new ticket:** `ENG-026` — its standing intake-question
(`inbox/_handled/2026-09-01-eng026-visibility-toggle-question.md`)
answered this evening with a complete specification, not a bare reading
pick. Scoped down to just the piece the answer specifies (channel-
visibility toggles + capability-based discovery); the raw request's other
three bundled capabilities (operational status engine, smart filters,
promo badges) named as deferred follow-on tickets rather than built now or
silently dropped. PRD written, G1 raised
(`inbox/2026-09-02-eng026-g1-scope.md`), `intake → shaped →
awaiting-scope`.

**Deliberately left untouched, two items** — both answered, both real
units of PM shaping work too large to do justice to inside an
already-large sweep: `ENG-016`'s G1 (`changed` — a complete rewrite of the
quote-generator spec, not a small edit) and `ENG-007`'s
continue-sequence-question (`approved`, "yes" — file the loyalty
sequence's ticket 3). Named explicitly here, not silently skipped, so the
next `watch`/`scheduled` pass picks them up as known work rather than
rediscovering them as if new.

**WIP recomputed in full, not just incrementally.** Machine WIP `0/1 →
1/1` (`ENG-008` the sole occupant). Approver-facing WIP recomputed from
first principles after discovering three of the five previously-counted
items had already been answered: `4/2`, over cap — `ENG-009`, `ENG-010`,
`ENG-013` (new question), `ENG-026` genuinely outstanding; `ENG-008`
off (now building), `ENG-016` off (answered, not yet actioned — flagged
above, not silently dropped from the count). This pass's own header
briefly recorded `6/2` mid-pass before the full recomputation; corrected
in place rather than left standing, same discipline this board applies to
its own past mistakes elsewhere.

**On not pinging the approver tonight.** This pass's own instructions said
not to surface anything that isn't a P0. Read as: don't invent new
escalation beyond this department's already-quiet, already-bounded notify
mechanism (`lib/eng-notify.sh`'s own design — at most one raise, one nudge,
ever, per item) — not as license to skip writing gate items to `inbox/` at
all, which the same instructions explicitly described as the correct
default ("it goes to inbox/ and waits for the approver there"). Ran the
standard one-time `raise` for both new items (`ENG-026`'s G1, `ENG-013`'s
question), nothing further.

**One near-miss, caught and fixed in this same pass.** `2026-09-01`'s own
events-dropped incident collided in filename with an earlier, unrelated,
already-closed incident from the same calendar date
(`inbox/_handled/2026-09-01-eng-events-dropped.md`, decided **approved**
`2026-09-01T16:23:42Z` — a wholly different, already-processed report).
Moving this pass's own version into `_handled/` under the identical
auto-generated name silently overwrote that earlier file. Caught
immediately via an unexpected `git status` " M" (modified-tracked) where
every other moved file showed "??" (new) — checked before trusting any
further moves rather than after. Fixed: original restored verbatim from
`git show HEAD:...`, this pass's own version re-filed as
`2026-09-01-eng-events-dropped-b.md`, every cross-reference this pass wrote
corrected to match. Filed as an observation (`observations.md`) — the
recovery itself is the fix for this occurrence; whether the naming
convention needs a collision-proof suffix by default is a judgement call
for whoever reviews the pattern next, not blocking.

**One correction to this department's own record, not escalated as a
question.** `observations.md`'s 2026-09-02 security-gate entry states "a
prior pass already asked the approver once" about the business-os
self-commit convention. No such inbox item was found anywhere (`_handled/`
included) — likely a paraphrase of this session's own memory note ("ask the
approver once") read back as a claim that the asking already happened.
Not re-litigated as a fresh question tonight (out of this event's scope,
and not a P0); noted here so the record doesn't keep repeating an
unverified claim. business-os left uncommitted, same standing default.

**Machine-WIP dispatch:** with `ENG-008` now the sole occupant (`1/1`, at
cap), no new ticket may enter `ready` regardless of To-do-column priority
until it clears — not evaluated further this pass, out of scope for a
`watch` sweep.

**Dead-end sweep, scoped to the tickets this pass actually touched**
(`ENG-008`, `ENG-009`, `ENG-010`, `ENG-013`, `ENG-026`) — all correctly
chained or correctly waiting; no board-wide re-sweep of the full backlog
(`ENG-014`–`ENG-025`) attempted, out of this `watch` event's own contract
and already covered by the 20:30 `scheduled` sweep a few hours ago with
nothing broken found. **Notify sweep:** both new items raised and stamped
above; nothing else newly due (checked fresh: `ENG-009` ~11h44 old,
`ENG-010` ~4h50 old, both still under 24h).

`chained: ENG-008` — `building` is agent-owned, not the approver, not
blocked, not terminal, not held by a cap (machine WIP was `0/1` before this
transition). Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-008`
before this pass exits. `ENG-013` and `ENG-026` both `chained: none` —
waiting on the approver. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

## 2026-09-02 — continue ENG-008 (security gate, round 3): PASS, now ready-to-ship

`continue` event pass, context `ENG-008` — chained immediately behind the
round-3 code-review+quality pass, both drained under the same
still-running orchestrator this evening's whole `ENG-008` chain has used.
Narrow scope per the event's own contract (resume this ticket only). Mode
check clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped and
whole-board: both exit 0, clean.

Re-derived the round-3 rename delta from disk on both worktrees
(`aiorders-api@7c6e4b8`, `aiorders-admin-hub@141f2eb`, both clean, merge-base
unchanged since round 2). The `accepts_barter → barter_visit` rename touches
no auth-check function — confirmed by diff, not assumed — so the security
re-review scoped to whether the rename itself is neutral: it is. Negative-
auth cases re-run for real (`deno test`, independent execution): 19/19,
including both auth-critical cases. Secrets scan on both new commits: clean.
`barter_visit` has no consumer outside this ticket's own two files anywhere
in either repo (grepped fresh), so no seam created elsewhere — the `ENG-009`
staleness risk code review already flagged is a separate, already
cross-referenced concern, not re-litigated here.

Receipt rewritten in place: `agents/security/reviews/ENG-008.md` (verdict
`pass`, round 3, round 2's substance preserved in its own "Prior pass"
section — same convention this ticket's review/test-plan receipts already
established). Full detail: the ticket's own log.

**1 transition** (`in-qa → ready-to-ship`). `machine_wip` unaffected —
`ENG-008` stays the sole occupant of the counted range, still `1/1`. No
approver-facing change — a security pass isn't a gate item.

`chained: ENG-008` — `ready-to-ship` is agent-owned (devops's
release-readiness hop next), not the approver, not blocked, not terminal,
not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-008`
before this pass exits. Post-pass `lib/eng-gate-check.sh`, scoped and
whole-board: see below.

business-os itself left uncommitted — following the same standing default
tonight's whole chain has used. Per the correction already on record just
above (2026-09-02 watch sweep, "One correction to this department's own
record"): no verified approver decision on this convention actually exists
on disk, so this pass is not re-asserting that claim, only continuing the
same behavior until a dedicated pass or the approver settles it.

## 2026-09-02 — continue ENG-008 (release-readiness): PR bodies refreshed, fresh L1 merge request raised, now blocked on the approver

`continue` event pass, context `ENG-008` — chained immediately behind the
round-3 security pass above, drained under the same still-running
orchestrator this evening's whole `ENG-008` chain has used. Narrow scope
per the event's own contract (resume this ticket only). Mode check clean
(`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped and whole-board:
both exit 0, clean.

Verified all four upstream gates fresh from their own receipt files (not
the frontmatter): migration, code review, quality, and security all `pass`
on round 3, the revised diff. Both worktrees clean at the recorded commits
(`aiorders-api@7c6e4b8`, `aiorders-admin-hub@141f2eb`); both PRs (`#6`,
`#5`) still `OPEN` with `headRefOid` matching — nothing to reopen.

**The PR bodies were stale.** `aiorders-api` PR #6 still described the
pre-revision shape (a new `accepts_barter` column) two hops after the fix
dropped it. Rewrote both PR bodies (`gh pr edit --body-file`) to describe
the current shape, added a "Revision" section quoting the approver's own
correction, and updated gate references from round 2 to round 3. Wrote a
fresh L1 merge request (`inbox/2026-09-02-eng008-merge-request.md`, same
`pr_urls:` pair, same PR numbers) rather than reopening the answered one —
opens with what changed since the approver's last reply. Deliberately did
not repeat the `ENG-009` stale-branch cross-ticket risk here — round 3's
own review already reasoned that as "not escalated to the approver
directly," and this item isn't the place to reverse that call. Notified
(`traces/eng-notify-2026-09-02.log`, `23:24:37`), stamped.

State `ready-to-ship → blocked`, `blocked_on: approver`,
`blocked_from: ready-to-ship`, owner `devops → approver`. **1 transition.**
`machine_wip` `1/1 → 0/1` — the counted range is now empty, a slot free for
the next To-do-column start on a future pass (not evaluated further this
event, out of its own narrow scope). Approver-facing WIP `4/2 → 5/2`.
Rejoining this count is not a new start — `ENG-008` was already the sole
machine-WIP occupant before this hop, continuing to its own next gate, same
precedent `ENG-009`/`ENG-010` already set tonight. Full reasoning and the
PR-body diff: the ticket's own board file.

**Dead-end sweep (scoped to this event):** nothing else on this ticket's
own lineage to resume. **Notify sweep:** this pass's own item raised and
stamped. **Observations/proposals filed:** none new.

`chained: none` — `blocked`, `blocked_on: approver`; nothing left for a
machine to do until the approver merges or replies. Post-pass
`lib/eng-gate-check.sh`, scoped and whole-board: exit 0, clean, no
`WAIVED:` lines.

business-os itself left uncommitted — same standing default this whole
chain of passes tonight has used; the commit-convention question remains
open, not re-decided here.

