# Engineering Board — pass log archive

Dated pass entries moved out of `_index.md` once the live board holds more than
three, newest first. The live board keeps its table plus enough recent narrative
to resume a ticket; everything older lives here.

Nothing reads this file on a pass — it is the department's history, not its
state. `lib/eng-gate-check.sh` globs `ENG-*.md` and never sees it.

This exists because every pass reads `_index.md` in full, so an append-only log
there is a tax on every future pass.

---

## 2026-09-04 — decision (`ENG-035`'s P0 incident): acknowledged, ticket unchanged — still `designed`, still held by the `ENG-016` family's machine-WIP cap

`decision` event pass, context `2026-09-03-eng035-p0-incident.md`. Reading
map for `decision`: steps 4 and 8c, plus the not-negotiable set (1, 7, 8b,
9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*) — steps 5, 6,
and 8's `blocked_from` paragraphs don't apply (not an L1 merge request, the
answer doesn't advance the ticket, the ticket isn't leaving `blocked`), and
neither does *The chain* (this incident is about a ticket, not the
loop/queue). Mode check clean (repo-root `.env` → `MODE=active`).

**The item:** `ENG-035`'s own P0 (`autopilot`'s system-triggered marketing
actions skip authentication entirely), raised 2026-09-03, answered
`decision: approved` at `2026-09-04T14:57:18Z` — no `priority` set, no
question asked back. Same shape as `ENG-022`'s and `ENG-029`'s own P0
incident acknowledgements: the item's own text offered nothing to decide
beyond an optional priority bump or question, and a bare approval reads as
acknowledging the interrupt, not reordering the board.

**`ENG-035` re-verified, not assumed unchanged.** Machine WIP re-checked
fresh from every ticket's own frontmatter: `ENG-016` `building`, `ENG-031`/
`ENG-032` `verified`, `ENG-033` `blocked` (`owner: approver`), `ENG-034`
`ready` — still `1/1`, the `ENG-016` family still holds the slot (the
parent not yet `shipped`, `ENG-034` still inside the counted
`ready..ready-to-ship` range). `ENG-035` stays `designed`, `owner:
architect`, exactly where its own last log entry left it. Processed note
appended to the incident item and moved to
`inbox/_handled/2026-09-03-eng035-p0-incident.md`, per step 4's Incident
handling. Full detail: `ENG-035`'s own board-file log.

Checked `traces/.pending` while here: `ENG-036`'s own P0 incident item
already carries `decision: changed` with a `decision
2026-09-03-eng036-p0-incident.md` event already queued behind one `watch
launchd` self-echo — a properly queued fire, not a lost one, and a
different ticket's answered gate besides — out of scope for this pass.

**Step 7 (notify sweep):** current `2026-09-04T15:13:17Z`. Six other open
`inbox/` items checked — `ENG-009`/`ENG-010`/`ENG-027` already carry a
`nudged:` timestamp; `ENG-028` (~23h03m since `notified:`), `ENG-030`'s P0
(~23h49m — close enough that the next pass to touch `inbox/` should expect
to nudge it), and `ENG-033` (~13h30m) all still under 24h; `ENG-036`'s P0
already carries a `decision:`. Nothing crossed; no nudge sent.

**Step 8c (journal):** row added to `decision-journal.md` for this
answered gate.

**Board update:** In-flight table's `ENG-035` row date bumped
(2026-09-03 → 2026-09-04), no state/owner change. The file held three live
dated entries before this one; rolled the oldest (`watch (launchd): all
three inboxes swept, no new signal...`) to `_index-archive.md` first, then
appended this entry, keeping three per the keep-three rule.

`lib/eng-gate-check.sh`, scoped (`ENG-035`) and whole-board: pre-pass both
exit 0, clean; post-pass re-run after this pass's edits, see below.

`chained: none` — `ENG-035` stays held by the machine-WIP cap (`1/1`, the
`ENG-016` family), re-confirmed fresh, not assumed. Not blocked, not
terminal, not waiting on the approver — only the cap.

business-os itself left uncommitted — same standing default every pass has
used, restated identically by each of the last several entries; not
re-decided here. Flagged plainly in this session's own final summary
instead, same as the immediately preceding entries have done.

## 2026-09-04 — decision (`ENG-029`'s P0 incident): acknowledged, ticket unchanged — still `designed`, still held by the `ENG-016` family's machine-WIP cap

`decision` event pass, context `2026-09-03-eng029-p0-incident.md`. Reading
map for `decision`: steps 4 and 8c, plus the not-negotiable set (1, 7, 8b,
9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*) — steps 5, 6,
and 8's `blocked_from` paragraphs don't apply (not an L1 merge request, the
answer doesn't advance the ticket, the ticket isn't leaving `blocked`), and
neither does *The chain* (this incident is about a ticket, not the
loop/queue). Mode check clean (repo-root `.env` → `MODE=active`).

**The item:** `ENG-029`'s own P0 (autopilot API, cross-tenant customer-data
exposure), raised 2026-09-03, answered `decision: approved` at
`2026-09-04T14:57:09Z` — no `priority` set, no question asked back. Same
shape as `ENG-022`'s own P0 incident acknowledgement: the item's own text
offered nothing to decide beyond an optional priority bump or question, and
a bare approval reads as acknowledging the interrupt, not reordering the
board.

**`ENG-029` re-verified, not assumed unchanged.** Machine WIP re-checked
fresh from every ticket's own frontmatter: `ENG-016` `building`, `ENG-031`/
`ENG-032` `verified`, `ENG-033` `blocked` (`owner: approver`), `ENG-034`
`ready` — still `1/1`, the `ENG-016` family still holds the slot (the
parent not yet `shipped`, `ENG-034` still inside the counted
`ready..ready-to-ship` range). `ENG-029` stays `designed`, `owner:
architect`, exactly where its own last log entry left it. Processed note
appended to the incident item and moved to
`inbox/_handled/2026-09-03-eng029-p0-incident.md`, per step 4's Incident
handling. Full detail: `ENG-029`'s own board-file log.

**Step 7 (notify sweep):** current `2026-09-04T15:02:16Z`. Nine other open
`inbox/` items checked — `ENG-009`/`ENG-010`/`ENG-027` already carry a
`nudged:` timestamp; `ENG-028` (~22h51m), `ENG-030`'s P0 (~23h38m), and
`ENG-033` (~13h19m) all still under 24h; `ENG-035`/`ENG-036`'s P0s already
carry a `decision:`. Nothing crossed; no nudge sent.

**Step 8c (journal):** row added to `decision-journal.md` for this
answered gate.

**Board update:** In-flight table's `ENG-029` row date bumped
(2026-09-03 → 2026-09-04), no state/owner change. The file held three live
dated entries before this one; rolled the oldest (`scheduled (context
ENG-028): ENG-008 found fully merged...`) to `_index-archive.md` first,
then appended this entry, keeping three per the keep-three rule.

`lib/eng-gate-check.sh`, scoped (`ENG-029`) and whole-board, run once after
this pass's edits rather than separately pre/post: both exit 0, clean.

`chained: none` — `ENG-029` stays held by the machine-WIP cap (`1/1`, the
`ENG-016` family), re-confirmed fresh, not assumed. Not blocked, not
terminal, not waiting on the approver — only the cap.

business-os itself left uncommitted — same standing default every pass has
used, restated identically by each of the last several entries; not
re-decided here. Flagged plainly in this session's own final summary
instead, same as the immediately preceding entries have done.

## 2026-09-04 — scheduled: no gate answered, two 24h nudges sent (`ENG-027`, `ENG-029`) — `eng-notify.sh`'s known MODE-clobber bug reconfirmed live, not re-proposed

`scheduled` event pass, context `manual`. Per the reading map, a `scheduled`
pass is never narrowed — read the whole `eng_build_loop.md` fresh and swept
the whole board. Mode check clean (repo-root `.env` → `MODE=active`).
Pre-pass `lib/eng-gate-check.sh`, whole-board: exit 0, clean.

The immediately preceding pass (`watch (launchd)`, entry above) left its own
step-7 timestamp at `2026-09-04T10:26:03Z`; this pass started at
`2026-09-04T14:45:28Z`, a ~4h19m gap wide enough that nothing here was
assumed carried-forward — every check below was re-run fresh rather than
trusted from adjacency.

**Step 2 (PM intake):** `agents/product-manager/inbox/` and
`inbox/requests/` hold nothing beyond `_handled/`/`.gitkeep` — no new
business intake.

**Step 3 (EM technical intake):** `agents/eng-manager/inbox/` holds nothing
beyond `_processed/`/`.gitkeep` — no new department-originated finding.

**Step 4 (gate returns):** all nine open `inbox/` items' frontmatter
re-read fresh (`ENG-009`/`ENG-010`/`ENG-033` merge requests, `ENG-027`'s
rescope G1, `ENG-028`'s G1, and all four P0 incident notices
`ENG-029`/`ENG-030`/`ENG-035`/`ENG-036`) — every `decision:` field still
blank on every one. Nothing answered since the last pass.

**Step 5 (merge detection):** re-ran fresh for the three `blocked` tickets.
`git fetch origin` on both worktrees, then `gh pr view` directly rather than
branch-tip ancestry alone (this board's own standing practice since the
`ENG-008` false-negative):

| Ticket | Branch | aiorders-api | aiorders-admin-hub |
|---|---|---|---|
| ENG-009 | `feat/ENG-009-influencer-engagement-info` | PR #7 `MERGED` into `feat/ENG-008-...` (not `main`) | PR #6 `MERGED` into `feat/ENG-008-...` (not `main`) |
| ENG-010 | `feat/ENG-010-influencer-relationship-notes` | PR #8 `MERGED` into `feat/ENG-009-...` (not `main`) | PR #7 `MERGED` into `feat/ENG-009-...` (not `main`) |
| ENG-033 | `feat/ENG-033-catering-request-order-capture-endpoint` | PR #13 `OPEN` into `main` | n/a (single-repo) |

Identical to every check since the finding was first made — no new merge
activity on any of the three. No ticket advances; all three stay `blocked`.

**Step 6 (dispatch):** machine WIP re-derived from the delta, not re-walked
from scratch — nothing that could move `ENG-016`'s family arrived this pass
(no gate answered, no PR merged), so the family's own state is unchanged:
`ENG-016` `building`, `ENG-031`/`ENG-032` `verified`, `ENG-033` still
`blocked` on the approver, `ENG-034` still `ready` behind its unmet
`depends_on: [ENG-033]`. WIP stays `1/1`. The twelve `designed` tickets
held behind the family cap
(`ENG-014`/`017`/`019`/`020`/`021`/`023`/`025`/`026`/`029`/`030`/`035`/`036`)
are unchanged for the same reason — nothing this pass found reopens that
question. No new ticket starts.

**Step 6b:** not run — this pass wrote no rule about an artifact path,
state name, or config key.

**Step 7 (notify sweep) — the substance of this pass.** Two items had
crossed 24h with no `nudged:` yet, computed fresh against their `notified:`
timestamps: `ENG-027` (notified `2026-09-03T13:15:26`, ~25h30m elapsed) and
`ENG-029` (notified `2026-09-03T14:37:25`, ~24h08m elapsed) — both nudged
(`lib/eng-notify.sh nudge`), both stamped `nudged: 2026-09-04T14:48:03`.
`ENG-028` (~22h35m), `ENG-033` (~13h), and `ENG-030`/`ENG-035`/`ENG-036`
(~23h21m/~21h48m/~11h53m) all still under 24h. `ENG-009`/`ENG-010` already
carry their one-time `nudged:` from earlier passes — done, rides the weekly
report now.

**Both nudge calls logged `sent: active`, not `sent: nudge`**
(`traces/eng-notify-2026-09-04.log`) — `lib/eng-notify.sh`'s own `MODE`
(set from `$1`) gets clobbered when it sources repo-root `.env`, whose
unrelated `MODE=active` (the quiet-mode switch) overwrites it under the
same variable name. This is not a new finding — it's the exact bug
`proposals.md` already carries from 2026-08-25, unfixed for ten days.
Confirmed still live and amended that row in place with today's
reconfirmation rather than filing a duplicate; not fixed inline —
self-discovered department machinery, so it stays a proposal per step 3,
same as every other self-found bug on this board, regardless of how small
the fix looks.

**Step 8 (dead-end sweep):** no `*-eng-events-dropped.md` file exists for
today (2026-09-04) — checked directly. `traces/.pending` was empty at pass
start; the two frontmatter stamps above (writes inside `inbox/`) shifted
the watched-inbox fingerprint and queued one self-triggered `1 watch
launchd` entry after — the same watch-echo mechanism this instance has
repeatedly documented as benign (the eventual watch pass will sweep and
correctly find nothing left to do, since everything it would find is
already recorded here). `blocked_from` present and correct on all three
`blocked` tickets (`ENG-009`/`ENG-010`/`ENG-033`, all `ready-to-ship`). No
`exception-request:` anywhere on the board (grepped directly). No ticket
sits in an agent-owned state with a missing or stale chain record — none
transitioned this pass to begin with.

**Step 8b (observations/exceptions):** the `eng-notify.sh` finding above is
an amendment to an existing proposal, not a fresh one — no new observation
or proposal row filed. No exceptions granted.

**Step 8c (journal):** n/a — no G1/G2/G3 or merge request was answered this
pass.

**Board update:** this entry appended; rolled the oldest of the four
now-live dated entries (`scheduled (auto-drain queue, context ENG-028):
whole-board sweep — no change since prior pass`) to `_index-archive.md` per
the keep-three rule, verified the seam clean on both files before
appending here.

Post-pass `lib/eng-gate-check.sh`, whole-board: exit 0, clean.

`chained: none` — no ticket was touched or transitioned this pass.
`ENG-009`/`ENG-010`/`ENG-033` genuinely wait on the approver, the twelve
`designed` tickets are genuinely held by the machine-WIP cap, `ENG-018`
stays excluded by its own `priority: hold`, and `ENG-034` waits on its own
unmet dependency. Nothing here is a chain to resume.

business-os itself left uncommitted — same standing default every pass has
used, restated identically by each of the last several entries; not
re-decided here. Flagged plainly in this session's own final summary
instead, same as the immediately preceding entries have done.

## 2026-09-04 — watch (launchd): all three inboxes swept, no new signal — this instance's own predicted self-triggered watch-echo, confirmed

`watch` event pass, context `launchd`. Per the reading map, read steps 2, 3,
4 (sweep all three inboxes) and 5 (merge detection, since the two changed
files — `ENG-009`'s and `ENG-010`'s merge-request items — are
merge-request items). Mode check clean (repo-root `.env` → `MODE=active`).
Pre-pass `lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Why this fired.** The immediately preceding `scheduled (context
ENG-028)` pass (entry above) amended `ENG-009`'s and `ENG-010`'s
merge-request bodies in place and moved `ENG-008`'s to `_handled/` — all
three writes land inside the watched `inbox/`, so they shift the
watched-inbox fingerprint and self-trigger a `watch` fire, exactly as that
pass's own step-8 note predicted ("the watch fire that eventually drains
will correctly find nothing left to do, since everything it would find is
already recorded here"). `traces/.pending` is empty — this fire already
drained with nothing queued behind it.

**Step 2 (PM intake):** `agents/product-manager/inbox/` holds nothing
beyond `_handled/`/`.gitkeep` (checked directly, fresh) — no new business
intake.

**Step 3 (EM technical intake):** `agents/eng-manager/inbox/` holds
nothing beyond `_processed/`/`.gitkeep` (checked directly, fresh) — no new
department-originated finding.

**Step 4 (gate returns):** all nine open `inbox/` items (`ENG-008` is now
in `_handled/`, off this count) grepped for `decision:` and read in full —
`ENG-009`/`ENG-010`/`ENG-033` merge requests, `ENG-027`'s rescope G1,
`ENG-028`'s G1, and all four P0 incident notices
(`ENG-029`/`ENG-030`/`ENG-035`/`ENG-036`) — every `decision:` field still
blank on every one. Nothing answered this pass; the `ENG-009`/`ENG-010`
edits an earlier pass made are informational updates from that pass, not
approver answers. No `exception-request:` found grepping
`agents/eng-manager/board/*.md` directly.

**Step 5 (merge detection)** — run because the two files that triggered
this watch are merge-request items. `git fetch origin` fresh on both
worktrees, then re-verified independently rather than trusting the board's
own just-written table:

| Ticket | Branch | aiorders-api | aiorders-admin-hub |
|---|---|---|---|
| ENG-009 | `feat/ENG-009-influencer-engagement-info` | not merged into `main` | not merged into `main` |
| ENG-010 | `feat/ENG-010-influencer-relationship-notes` | not merged into `main` | not merged into `main` |
| ENG-033 | `feat/ENG-033-catering-request-order-capture-endpoint` | not merged into `main` | n/a (single-repo) |

Cross-checked `aiorders-api` PRs #7, #8 and #13 directly with `gh pr view`
rather than relying on branch-tip ancestry alone, given this board's own
recent `ENG-008` false-negative on that exact check: PR #7 (`ENG-009`)
`MERGED` into base `feat/ENG-008-influencer-admin-management` at
`2026-09-04T06:06:00Z`; PR #8 (`ENG-010`) `MERGED` into base
`feat/ENG-009-influencer-engagement-info` at `2026-09-04T06:06:28Z`; PR #13
(`ENG-033`) still `OPEN` into `main`. All three identical to what the
preceding pass already recorded on `ENG-009`'s and `ENG-010`'s own
merge-request items and this board's closing paragraph — no new merge
activity since. No ticket advances.

Step 6 (dispatch) is outside this event's reading map and moot regardless
— step 5 freed no slot; machine WIP unchanged at `1/1`, still held by the
`ENG-016` family.

**Step 7 (notify sweep):** current `2026-09-04T10:26:03Z`. `ENG-009`/
`ENG-010` already carry their one-time `nudged:` (amended bodies aren't a
new gate). `ENG-027` (~21h11m since `notified:`), `ENG-028` (~18h16m),
`ENG-033` (~8h43m), and all four P0 incident notices (oldest, `ENG-029`,
~19h49m) all still under 24h. Nothing crossed, nothing raised.

**Step 8b (observations/exceptions):** none new — the watch-echo mechanism
itself was already anticipated and named by the pass that caused it; no
fresh observation warranted for a predicted, harmless recurrence. No
`exception-request:` in any ticket log (confirmed above).

**Board update:** this entry appended; rolled the oldest of the three live
dated entries (`scheduled (launchd): whole-board sweep — ENG-008 partial
merge found`) to `_index-archive.md` per the keep-three rule, verified the
seam clean on both files before appending here.

Post-pass `lib/eng-gate-check.sh`, whole-board: exit 0, clean.

`chained: none` — no ticket was touched or transitioned this pass: both
inboxes outside `inbox/` came up empty, every `inbox/` item's `decision:`
is still blank, and merge detection found exactly the state already on
record. Nothing here is a chain to resume.

business-os itself left uncommitted — same standing default every pass has
used, restated identically by each of the last four entries; not
re-decided here. The working tree now carries a large, multi-pass backlog
of uncommitted instance work (many tickets' worth, `ENG-016`'s family
through `ENG-036`) — worth the approver's own attention regardless of which
way the convention question is eventually settled, so raised plainly in
this session's own final summary rather than acted on unilaterally here.

## 2026-09-04 — scheduled (context `ENG-028`): `ENG-008` found fully merged (a ~3.5h detection gap, root-caused and fixed) — carried to `verified`; `ENG-009`/`ENG-010` found merged-but-not-shipped, a new failure shape

`scheduled` event pass, context a pointer to `ENG-028`'s own board file
(the trigger's copy of that ticket's checkpoint, not a narrowing
instruction — per the reading map's own "never narrowed" rule, read the
whole `eng_build_loop.md` fresh and swept the whole board regardless).
Mode check clean (repo-root `.env` → `MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, whole-board: exit 0, clean.

This fire drained about 4 minutes behind the immediately preceding
`scheduled (auto-drain queue, context ENG-028)` pass (09:57:30Z →
~10:02Z) — adjacent enough that treating it as a probable no-op would have
been reasonable, but per this instance's own established discipline
(`observations.md`'s repeated "verify fresh, don't assume from adjacency"
findings), every step below was independently re-derived rather than
carried forward from that pass's own conclusions. It found real, material
change.

**Step 2 (PM intake):** `agents/product-manager/inbox/` and
`inbox/requests/` hold nothing beyond `_handled/`/`.gitkeep` — no new
business intake.

**Step 3 (EM technical intake):** `agents/eng-manager/inbox/` holds
nothing beyond `_processed/`/`.gitkeep` — no new department-originated
finding.

**Step 4 (gate returns):** all ten open `inbox/` items re-read fresh —
`ENG-008`/`ENG-009`/`ENG-010` merge requests, `ENG-027`'s rescope G1,
`ENG-028`'s G1, `ENG-033`'s merge request, and all four P0 incident
notices (`ENG-029`/`ENG-030`/`ENG-035`/`ENG-036`, each still explicitly
"nothing to decide — informational") — every `decision:` field still
blank on every one. Nothing answered in the tracked channel this pass.

**Step 5 (merge detection) — the substance of this pass.** Re-ran fresh
for every ticket sitting `blocked`: `ENG-008`, `ENG-009`, `ENG-010`,
`ENG-033`. `git fetch origin` clean on both worktrees. The naive check
every prior sweep has used —
`git merge-base --is-ancestor origin/feat/ENG-008-influencer-admin-management
origin/main` — **still returned `not merged` on both repos**, identical to
every sweep since 09:37Z. Rather than record an eighth identical "no
change," checked *why* it keeps returning that given `ENG-008`'s own
merge-request item had been open and gated for days: re-verified via `gh
pr view` directly instead of trusting the branch-tip check.

**Found `aiorders-api` PR #6 merged** (`bd67e86`, base `main`,
`2026-09-04T06:04:41Z`) — **roughly 3.5 hours before the first sweep that
checked it (09:37Z) reported "not merged," and every sweep since repeated
that same wrong reading.** Root cause, confirmed by direct inspection, not
inferred: `ENG-009`'s and `ENG-010`'s PRs are deliberately stacked on
`feat/ENG-008-influencer-admin-management` (their own configured base,
not `main`), and both merged *into that branch* — 06:06:00Z and
06:10:29Z(ish) respectively — *after* `ENG-008`'s own PR had already
merged separately to `main`. That moved the branch's live tip past what
shipped, so "is the branch tip an ancestor of `main`" stopped answering
"did `ENG-008` ship" three-plus hours before anyone asked it the right
question instead. Checking the ticket's own recorded commit
(`branch:` frontmatter, already on file) or `gh pr view` directly
sidesteps this entirely.

**`ENG-008` gate receipts re-verified fresh** (step 5's "a merge is not a
gate" clause): review (round 3, `pass`), quality (`pass`, 19/19 `deno
test`), security (`pass`) — all three against the exact diff that's on
`main` now, no drift. Carried `blocked → shipped → verified`. Release
record written
(`agents/devops/releases/2026-09-04-ENG-008-aiorders-api-and-admin-hub.md`),
merge-request item moved to `inbox/_handled/`, journaled
(`decision-journal.md`, occurrences 13/14). Full detail:
`ENG-008`'s own board-file log.

**The mirror-image discovery: `ENG-009`'s and `ENG-010`'s own PRs also show
`MERGED`, but neither shipped.** Both merged into their own stacked base
branches (`ENG-009` → `feat/ENG-008-...`, `ENG-010` → `feat/ENG-009-...`),
which had already been separately consumed into `main` (`ENG-008`'s case)
or hadn't reached `main` at all (`ENG-009`'s case) by the time the child
PR landed — confirmed by content (`git grep` for each ticket's
distinguishing code against `origin/main` on both repos: no hits) not just
ancestry. **First occurrence on this board of a merge click that did not
ship the ticket** — every prior silent-GitHub-merge (`ENG-002` through
`ENG-015`, fourteen occurrences before this one) correctly delivered code
to `main`. Checked whether the specific regression `ENG-008`'s own
round-3 review once warned `ENG-009` risked (reintroducing the rejected
`accepts_barter` column) actually happened: it did not — the merged
branch carries the correct post-fix code, because this was a `git merge`
(not a rebase) and `ENG-009`'s own diff never touched the specific lines
that had gone stale, so the merge's non-conflicting side took `ENG-008`'s
newer version automatically. Correct outcome, but not a property to rely
on generally. Both tickets stay `blocked` — the operational gap (no PR
anywhere now targets `main` with either ticket's changes) is independent
of content correctness. Both merge-request items amended in place with a
plain-language explanation (not moved — the underlying question is still
open); both ticket logs carry the full finding; journaled as one combined
row. Full detail: `ENG-009`'s and `ENG-010`'s own board-file logs.

`ENG-033` unchanged: `aiorders-api` PR #13 still `OPEN` (`gh pr view`,
`baseRefName: main`, no stacking involved) — stays `blocked`.

**Step 6 (dispatch):** machine WIP re-checked fresh from frontmatter —
still `1/1`, held by the `ENG-016` family (`ENG-016` `building`, `ENG-031`/
`ENG-032` `verified`, `ENG-033` `blocked` on the approver, `ENG-034`
`ready` behind its unmet `depends_on: [ENG-033]`). `ENG-008` reaching
`verified` frees no machine-WIP slot — it was never inside the counted
`ready..ready-to-ship` range while `blocked`, same as every other
silent-merge ticket this board has carried to `verified`. No new ticket
starts. Every ticket held behind the `ENG-016` family cap
(`ENG-014`/`017`/`019`/`020`/`021`/`023`/`025`/`026`/`029`/`030`/`035`/`036`)
stays exactly where it was — spot-checked, not re-derived from scratch,
since nothing changed for any of them this pass.

**Step 6b:** not run — this pass's own instruction/rule-shaped writing (the
`gh`-over-branch-tip check for stacked branches) is captured as a
`proposals.md` row for the department to adopt deliberately, not written
into any agent/skill instruction file directly by this sweep — no
artifact-mention grep owed for a proposal that hasn't been approved yet.

**Step 7 (notify sweep):** current `2026-09-04T10:18Z`. `ENG-008`
(terminal, nothing to notify), `ENG-009`/`ENG-010` (one-time `nudged:`
already spent on each, amending the item body isn't a new gate). `ENG-027`
(~21h, `notified:` ~13:15Z 09-03), `ENG-028` (~18h, ~16:10Z 09-03),
`ENG-033` (~8.5h, ~01:43Z 09-04), and all four P0 incident notices
(oldest, `ENG-029`, ~19h40m) all still under 24h. Nothing crossed, nothing
raised.

**Step 8 (dead-end sweep):** `traces/.pending` picked up three duplicate
`watch launchd` lines during this pass (this pass's own edits to files
inside `inbox/` — moving `ENG-008`'s merge request to `_handled/`, amending
`ENG-009`'s and `ENG-010`'s bodies — each shifting the watched-inbox
fingerprint out from under the pre-pass baseline, the same self-triggered
watch-echo mechanism this instance has documented before). Expected, not a
broken chain: duplicate `<event> <context>` lines collapse to one at pop
time, and the watch fire that eventually drains will correctly find
nothing left to do, since everything it would find is already recorded
here. No `*-eng-events-dropped.md` file exists for today (2026-09-04) —
checked directly. `blocked_from` present and correct on the three
remaining `blocked` tickets (`ENG-009`/`ENG-010`/`ENG-033`, all
`ready-to-ship`; `ENG-008`'s cleared on reaching `verified`). No ticket
sits in an agent-owned state with a missing or stale chain record.

**Step 8b (observations/exceptions):** none filed as observations — the
finding was significant enough to be a proposal outright (below), not a
note. No `exception-request:` in any ticket log.

**Step 8c (journal):** two entries added to
`agents/eng-manager/config/decision-journal.md` — `ENG-008` (merged, no
written reply, occurrences 13/14) and a combined `ENG-009`/`ENG-010` row
(merged but did not ship — first occurrence of this shape on this board).

**New proposal filed** (`agents/eng-manager/proposals.md`): the general
mechanism gap — a stacked PR's merge can satisfy GitHub's UI without the
code ever reaching the default branch, in both directions (a shipped
ticket can read as unmerged; an unshipped ticket can read as merged) —
distinct from, but corroborating a second time, the existing 2026-09-02
sibling-staleness proposal.

**Board update:** header's `ENG-008` bullet, the "on the approver's plate"
paragraph (six → five items), the In-flight table (`ENG-008` row removed),
and the closing terminal-tickets paragraph (both `ENG-008` and the
`ENG-009`/`ENG-010` finding added) all updated. The file held three live
dated entries before this one; rolled the oldest
(`scheduled (launchd): whole-board sweep — ENG-008 partial merge found`)
to `_index-archive.md` first, then appended this entry, keeping three per
the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, whole-board and scoped (`ENG-008`,
`ENG-009`, `ENG-010`): all four exit 0, clean.

`chained: none` — `ENG-008` is `verified` (terminal). `ENG-009`/`ENG-010`
stay `blocked`, `blocked_on: approver`; getting either to `main` needs a
real rebase/re-PR decision this sweep's own contract doesn't cover, not a
chained hop. `ENG-033` unchanged, still `blocked`. No ticket in this pass
is in a state a machine hop would advance.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.
This pass's own diff is large enough (a shipped ticket, two amended gate
items, a new proposal, two journal entries, one release record, three
ticket-log entries, one board-index rebalance) that it's flagged to the
approver directly in this session's own final summary, separate from the
board file itself — the standing question stays unresolved either way.

## 2026-09-04 — scheduled (auto-drain queue, context `ENG-028`): whole-board sweep — no change since prior pass

`scheduled` event pass, context `auto-drain`. `traces/.pending` held this
fire as `1 scheduled ...ENG-028-foodswipe-custom-pipeline-stages.md` — a
ticket-context label riding the queue's own collapse/drain mechanics, not a
narrowing instruction: per the reading map's own "never narrowed" rule, a
`scheduled` pass reads the whole procedure document and sweeps the whole
board regardless of what context string it arrives with. Read the full
`eng_build_loop.md` fresh this pass. Mode check clean (repo-root `.env` →
`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, whole-board: exit 0,
clean.

**Step 2 (PM intake):** `agents/product-manager/inbox/` and
`inbox/requests/` hold nothing beyond `_handled/`/`.gitkeep` — no new
business intake.

**Step 3 (EM technical intake):** `agents/eng-manager/inbox/` holds
nothing beyond `_processed/`/`.gitkeep` — no new department-originated
finding.

**Step 4 (gate returns):** all ten open `inbox/` items re-read fresh
(current `2026-09-04T09:52:38Z`) — `ENG-008`/`ENG-009`/`ENG-010` merge
requests, `ENG-027`'s rescope G1, `ENG-028`'s G1, `ENG-033`'s merge
request, and all four P0 incident notices (`ENG-029`/`ENG-030`/`ENG-035`/
`ENG-036`, each still explicitly "nothing to decide — informational" in its
own body) — every `decision:` field still blank on every one. Nothing
answered this pass.

**Step 5 (merge detection).** Re-ran fresh for every ticket sitting
`blocked`: `ENG-008`, `ENG-009`, `ENG-010`, `ENG-033`. `git fetch origin` on
both worktrees (`aiorders-api`: still carries only its standing untracked
`supabase/functions/brand-portal/deno.lock`; `aiorders-admin-hub`: clean),
then `git merge-base --is-ancestor` for each ticket's own branch (via its
`origin/` ref where no local branch exists in the worktree, `ENG-008`'s
`aiorders-api` side specifically) against `origin/main`:

| Ticket | Branch | aiorders-api | aiorders-admin-hub |
|---|---|---|---|
| ENG-008 | `feat/ENG-008-influencer-admin-management` | not merged | **MERGED** (unchanged, already recorded) |
| ENG-009 | `feat/ENG-009-influencer-engagement-info` | not merged | not merged |
| ENG-010 | `feat/ENG-010-influencer-relationship-notes` | not merged | not merged |
| ENG-033 | `feat/ENG-033-catering-request-order-capture-endpoint` | not merged | n/a (single-repo) |

Identical to the immediately preceding `watch` pass's own table. `ENG-008`
stays `blocked` on its already-recorded partial merge (`aiorders-api` PR #6
the sole outstanding repo); `ENG-009`/`ENG-010`/`ENG-033` unchanged. No
ticket advances.

**Step 6 (dispatch):** machine WIP re-checked fresh from each ticket's own
frontmatter, not the cached header — `ENG-016` `state: building`, `ENG-031`
`verified`, `ENG-032` `verified`, `ENG-033` `blocked`/`blocked_on: approver`,
`ENG-034` `ready` with `depends_on: [ENG-033]` still unmet. Still `1/1`,
held by the `ENG-016` family per this board's own first-precedent reading.
No slot frees, so nothing new starts, and nothing in the family itself has
anywhere to go: `ENG-033` waits on the approver merging `aiorders-api` PR
#13, `ENG-034` waits on `ENG-033`. Spot-checked (not re-derived from
scratch) `ENG-034`'s and `ENG-033`'s own most recent log entries rather than
trusting the board's summary — both carry a correctly reasoned `chained:
none` (unmet dependency; blocked on approver, respectively), so neither is a
dropped chain. The twelve `designed` tickets the immediately preceding
`scheduled` sweep already audited line-by-line (cap-held-after-completion,
confirmed via each one's own `links.design` and routing note) are unchanged
— nothing this pass found reopens that question.

**Step 6b:** not run — this pass wrote no new rule about an artifact path,
state name, or config key; it re-read existing gate receipts, merge state,
and ticket frontmatter, and confirmed no change.

**Step 7 (notify sweep):** current `2026-09-04T09:57:30Z`. `ENG-008`/
`ENG-009`/`ENG-010` already carry their one-time `nudged:`. `ENG-027`
(~20h42m since `notified:`), `ENG-028` (~17h47m), `ENG-033` (~8h14m), and
all four P0 incident notices (oldest, `ENG-029`, ~19h20m) all still under
24h. Nothing crossed, nothing raised.

**Step 8 (dead-end sweep):** `traces/.pending` is now empty — this pass was
the sole queued fire and nothing else is backed up behind it. No
`*-eng-events-dropped.md` file exists for today (2026-09-04) — checked
directly. `blocked_from` present and correct on all four currently-`blocked`
tickets (`ENG-008`/`ENG-009`/`ENG-010`/`ENG-033`, all `ready-to-ship`). No
ticket sits in an agent-owned state with a missing or stale chain record.

**Step 8b (observations/exceptions):** none new — nothing surprising
surfaced this pass. Grepped `agents/eng-manager/board/*.md` directly for
`exception-request:`: none found.

**Step 8c (journal):** n/a — no G1/G2/G3 or merge request was answered this
pass.

**Board update:** this entry appended; rolled the oldest of the now-four
live dated entries (`scheduled (queue context ENG-027): whole-board sweep —
no state change; dead-end check clears all twelve designed tickets`) to
`_index-archive.md` per the keep-three rule, verified the seam clean on
both files before appending here.

Post-pass `lib/eng-gate-check.sh`, whole-board: exit 0, clean.

`chained: none` — no ticket was touched or transitioned this pass. The four
`blocked` tickets genuinely wait on the approver, the twelve `designed`
tickets are genuinely held by the machine-WIP cap, `ENG-018` stays excluded
by its own `priority: hold`, and `ENG-034` waits on its own unmet
dependency. Nothing here is a chain to resume.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-04 — watch (launchd): all three inboxes swept, no new signal — confirms the immediately preceding `scheduled` pass rather than repeating it blind

`watch` event pass, context `launchd` — a file changed in a watched inbox
outside the notify/poll channel. Per the reading map, read steps 2, 3, 4
(sweep all three inboxes) and 5 (merge detection, since open merge-request
items exist). Mode check clean (`MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, whole-board: exit 0, clean.

This event drained `traces/.pending` 4 seconds after the immediately
preceding `scheduled (launchd)` pass ended (02:43:57 → 02:44:01 local, per
`traces/eng-loop-2026-09-04.log`) — that prior pass had just re-verified
every inbox item and every blocked ticket's merge state fresh. Rather than
treat that adjacency as license to skip this pass's own required steps,
each was re-run independently:

**Step 2 (PM intake):** `agents/product-manager/inbox/` and
`inbox/requests/` hold nothing beyond `_handled/`/`.gitkeep` — no new
business intake.

**Step 3 (EM technical intake):** `agents/eng-manager/inbox/` holds
nothing beyond `_processed/`/`.gitkeep` — no new department-originated
finding.

**Step 4 (gate returns):** all ten open `inbox/` items re-read fresh
(current `2026-09-04T09:45:07Z`) — `ENG-008`/`ENG-009`/`ENG-010` merge
requests, `ENG-027`'s rescope G1, `ENG-028`'s G1, `ENG-033`'s merge
request, and all four P0 incident notices (`ENG-029`/`ENG-030`/`ENG-035`/
`ENG-036`) — every `decision:` field still blank on every one. Nothing
answered this pass; nothing in this inbox is what triggered the watch.

**Step 5 (merge detection)** — run because open merge-request items exist
for every currently-`blocked` ticket. `git fetch origin` on both
worktrees (`aiorders-api`: still carries only its standing untracked
`supabase/functions/brand-portal/deno.lock`; `aiorders-admin-hub`: clean),
then `git merge-base --is-ancestor` for each ticket's own branch against
`origin/main`:

| Ticket | Branch | aiorders-api | aiorders-admin-hub |
|---|---|---|---|
| ENG-008 | `feat/ENG-008-influencer-admin-management` | not merged | **MERGED** |
| ENG-009 | `feat/ENG-009-influencer-engagement-info` | not merged | not merged |
| ENG-010 | `feat/ENG-010-influencer-relationship-notes` | not merged | not merged |
| ENG-033 | `feat/ENG-033-catering-request-order-capture-endpoint` | not merged | n/a (single-repo) |

Identical to the immediately preceding pass's own table — `ENG-008` stays
`blocked` on its already-recorded partial merge (`aiorders-api` PR #6
outstanding), the other three unchanged. No ticket advances.

Step 6 (dispatch) is outside this event's reading map and moot regardless
— step 5 freed no slot, so machine WIP is unchanged at `1/1`.

**Step 7 (notify sweep):** current `2026-09-04T09:45:07Z`. `ENG-008`/
`ENG-009`/`ENG-010` already carry their one-time `nudged:`. `ENG-027`
(~20h30m since `notified:`), `ENG-028` (~17h35m), `ENG-033` (~8h02m), and
all four P0 incident notices (oldest, `ENG-029`, ~19h08m) all still under
24h. Nothing crossed, nothing raised.

**Step 8b (observations/exceptions):** none new — nothing surprising
surfaced. No `exception-request:` in any ticket log.

**Board update:** this entry appended; rolled the oldest of the three live
dated entries (`scheduled (auto-drain queue, context ENG-026): whole-board
re-sweep`) to `_index-archive.md` per the keep-three rule, verified the
seam clean on both files before appending here.

Post-pass `lib/eng-gate-check.sh`, whole-board: exit 0, clean.

`chained: none` — no ticket was touched or transitioned this pass: every
inbox came up empty of anything new, and merge detection found the same
state the pass four seconds before it already found and recorded. There is
nothing to fire a next hop onto.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-04 — scheduled (launchd): whole-board sweep — `ENG-008` partial merge found (`aiorders-admin-hub` side in, `aiorders-api` side still open)

`scheduled` event pass, context `launchd` — the scheduler firing directly,
not a ticket-context label riding the queue's own collapse/drain mechanics
like the two entries above. Reading map: whole document, never narrowed.
Mode check clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`,
whole-board: exit 0, clean.

**Step 2 (PM intake):** `agents/product-manager/inbox/` and
`inbox/requests/` hold nothing beyond `_handled/`/`.gitkeep` — no new
business intake.

**Step 3 (EM technical intake):** `agents/eng-manager/inbox/` holds
nothing beyond `_processed/`/`.gitkeep` — no new department-originated
finding.

**Step 4 (gate returns):** all ten open `inbox/` items re-read fresh
(current `2026-09-04T09:37:10Z`) — `ENG-008`/`ENG-009`/`ENG-010` merge
requests, `ENG-027`'s rescope G1, `ENG-028`'s G1, `ENG-033`'s merge
request, and all four P0 incident notices (`ENG-029`/`ENG-030`/`ENG-035`/
`ENG-036`) — every `decision:` field still blank on every one. Nothing
answered this pass.

**Step 5 (merge detection) — the substance of this pass.** Re-ran fresh
for every ticket sitting `blocked`: `ENG-008`, `ENG-009`, `ENG-010`,
`ENG-033`. `git fetch origin` on both worktrees (`aiorders-api` carries
only its standing untracked `supabase/functions/brand-portal/deno.lock`;
`aiorders-admin-hub` clean), then `git merge-base --is-ancestor` for each
ticket's own branch against `origin/main` on each repo it touches:

| Ticket | Branch | aiorders-api | aiorders-admin-hub |
|---|---|---|---|
| ENG-008 | `feat/ENG-008-influencer-admin-management` | not merged | **MERGED** |
| ENG-009 | `feat/ENG-009-influencer-engagement-info` | not merged | not merged |
| ENG-010 | `feat/ENG-010-influencer-relationship-notes` | not merged | not merged |
| ENG-033 | `feat/ENG-033-catering-request-order-capture-endpoint` | not merged | n/a (single-repo) |

**`ENG-008`'s `aiorders-admin-hub` branch merged directly on GitHub**
(`141f2eb`, 2026-09-02T22:48:15-07:00, "Drop redundant accepts_barter, edit
barter_visit directly (ENG-008)"), no written reply — a genuine change from
the immediately prior sweep nine minutes earlier, which found both repos
not-merged. `aiorders-api` PR #6 is not merged. Per step 5's own
partial-merge clause, a multi-repo ticket ships only once every repo has
merged — stays `blocked`, `aiorders-api` PR #6 named as the sole
outstanding repo on the ticket's own log and in the board header/
waiting-on-approver sections above. `ENG-009`/`ENG-010`/`ENG-033`
unchanged, all branches not merged, identical to the prior sweep's own
table.

**Step 6 (dispatch):** machine WIP re-checked fresh from frontmatter —
still `1/1`, held by the `ENG-016` family (`ENG-016` `building`, `ENG-033`
`blocked` on the approver, `ENG-034` `ready` behind its unmet
`depends_on: [ENG-033]`). `ENG-008`'s partial merge frees no machine-WIP
slot — it was never inside the counted `ready..ready-to-ship` range while
`blocked` — so this pass starts nothing new. Every ticket held behind the
`ENG-016` family cap (`ENG-014`, `ENG-017`, `ENG-019`, `ENG-020`, `ENG-021`,
`ENG-023`, `ENG-025`, `ENG-026`, `ENG-029`, `ENG-030`, `ENG-035`, `ENG-036`)
stays exactly where the immediately prior sweep left it — not re-derived
from scratch this pass, since nothing changed for any of them.

**Step 6b:** not run — this pass wrote no new rule about an artifact path,
state name, or config key; it recorded one silent partial merge, the
bookkeeping category the rule doesn't apply to.

**Step 7 (notify sweep):** current `2026-09-04T09:37:10Z`. `ENG-008`/
`ENG-009`/`ENG-010` already carry their one-time `nudged:`. `ENG-027`
(~20h22m since `notified:`), `ENG-028` (~17h27m), `ENG-033` (~7h54m), and
all four P0 incident notices (oldest, `ENG-029`, ~19h00m) all still under
24h. Nothing crossed, nothing raised — `ENG-008`'s partial merge needs no
gate; the existing merge-request item already anticipates exactly this
shape and its one nudge is already spent.

**Step 8 (dead-end sweep):** `traces/.pending` holds three queued fires
behind this one (`watch launchd`, `scheduled auto-drain`,
`scheduled ...ENG-028...`) — one fewer than the prior sweep's own four,
consistent with this pass being that list's own `scheduled launchd` entry
now drained; normal FIFO backlog under the still-running `auto-drain`
wrapper, not a broken chain. No `*-eng-events-dropped.md` file exists for
today (2026-09-04) — checked directly. `blocked_from` present and correct
on all four currently-`blocked` tickets (unchanged, all `ready-to-ship`).
No ticket sits in an agent-owned state with a missing or stale chain
record.

**Step 8b (observations/exceptions):** none new filed — step 5 already
names exactly where partial-merge bookkeeping belongs (the ticket's own
log). No `exception-request:` in any ticket log.

**Step 8c (journal):** n/a — no G1/G2/G3 or merge request was answered
this pass; a partial merge with no written reply isn't an answered gate.

**Board update:** header's `ENG-008` bullet and the "Waiting on the
approver" section's `ENG-008` paragraph both extended with the
partial-merge finding (`aiorders-admin-hub` in, `aiorders-api` still
open). The file held three live dated entries before this one; rolled the
oldest (`scheduled (auto-drain queue, carrying a stale ENG-021 context
pointer): ENG-013 & ENG-015 found merged`) to `_index-archive.md` first,
then appended this entry, keeping three per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, whole-board and scoped (`ENG-008`): both
exit 0, clean.

`chained: none` — `ENG-008` stays `blocked`, `blocked_on: approver`; the
one remaining step (merging `aiorders-api` PR #6) is caught by the next
pass's own merge-detection, not a chained hop. No other ticket
transitioned this pass.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-04 — scheduled (queue context `ENG-027`): whole-board sweep — no state change; dead-end check clears all twelve `designed` tickets as correctly cap-held

`scheduled` event pass. The event arrived with context
`agents/eng-manager/board/ENG-027-loyalty-points-ledger-and-earn.md` — a
label riding this fire from the queue's own collapse/drain mechanics, not a
narrowing instruction: a `scheduled` pass reads the whole procedure document
and sweeps the whole board regardless of what context string it arrives
with, per the reading map's own "never narrowed" rule. Read the full
`eng_build_loop.md` fresh this pass (not from memory), plus the *Machine
WIP limit* rationale section, consulted deliberately per the reading map's
own allowance to read the rationale file "when hunting a lost event or a
stalled queue." Mode check clean (`MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Step 2 (PM intake):** `agents/product-manager/inbox/` and
`inbox/requests/` hold nothing beyond `_handled/`/`.gitkeep` — no new
business intake.

**Step 3 (EM technical intake):** `agents/eng-manager/inbox/` holds nothing
beyond `_processed/`/`.gitkeep` — no new department-originated finding.

**Step 4 (gate returns):** all ten open `inbox/` items re-read fresh —
`ENG-008`/`ENG-009`/`ENG-010` merge requests, `ENG-027`'s rescope G1,
`ENG-028`'s G1, `ENG-033`'s merge request, and all four P0 incident notices
(`ENG-029`/`ENG-030`/`ENG-035`/`ENG-036`) — every `decision:` field is still
blank on every one, `ENG-027`'s rescope G1 included. Nothing answered this
pass.

**Step 5 (merge detection).** Re-ran fresh for every ticket sitting
`blocked`: `ENG-008`, `ENG-009`, `ENG-010`, `ENG-033`. `git fetch origin` on
both the `aiorders-api` and `aiorders-admin-hub` worktrees
(`~/Documents/projects/_eng/{project}`; `aiorders-api` carries only its
standing untracked `supabase/functions/brand-portal/deno.lock`,
`aiorders-admin-hub` fully clean), then `git merge-base --is-ancestor` for
each ticket's own branch against `origin/main` on each repo it touches — all
seven branch checks (`ENG-008`/`ENG-009`/`ENG-010` on both repos, `ENG-033`
on `aiorders-api` only) return **not merged**, identical to the immediately
prior sweep's own table. No ticket advances; all four stay `blocked`.

**Step 6 (dispatch) — the substance of this pass.** Machine WIP re-checked
fresh from frontmatter, not the cached header: still `1/1`, held by the
`ENG-016` family (`ENG-016` `building`, `ENG-033` `blocked` on the approver,
`ENG-034` `ready` behind its unmet `depends_on: [ENG-033]`). No slot frees,
so no new ticket starts.

That made the twelve tickets sitting at `designed`
(`ENG-014`/`ENG-017`/`ENG-019`/`ENG-020`/`ENG-021`/`ENG-023`/`ENG-025`/
`ENG-026`/`ENG-029`/`ENG-030`/`ENG-035`/`ENG-036`, all `owner: architect`
except `ENG-014`/`ENG-025` at `owner: eng-manager`) worth checking properly
rather than waving through on the strength of the prior sweeps' own
summary line — every one of their own last log entries reads `chained: none
— held by the machine-WIP cap`, the identical reason repeated twelve times
across a board that otherwise takes real care to distinguish genuine holds
from stale ones (see the header's own `ENG-019`/`ENG-020`/`ENG-021`
approver-cap correction, three paragraphs up). Twelve independent-looking
confirmations of the same rule, cited from a precedent chain each next
ticket copied from the last, is exactly the shape a propagated error takes,
not proof the rule is being applied correctly — so this pass read the
underlying facts rather than the count of agreeing citations.

`eng_build_loop.md` step 6 states plainly that `designed` is cap-exempt
("Shaping and design work... is not gated by this slot and may continue as
backlog grooming — it is paperwork, not code in flight"), and the Guards
section defines the machine-WIP cap as counting only `ready` through
`ready-to-ship` — `designed` is outside that range by the cap's own
definition. Taken alone, that would make all twelve citations wrong. Reading
each ticket's own log resolved the apparent conflict instead of stopping at
it: `designed` conflates two sub-states, named explicitly on this board
since the 2026-08-31 `ENG-014`/`ENG-015`/`ENG-025` investigation —
"un-designed" (no tech design written yet, genuinely cap-exempt, should keep
progressing) and "cap-held-after-completion" (design finished, the
architect's own routing would write `ready`, and *that* transition is
correctly gated). All twelve read as the second kind: each ticket's own
`links.design` frontmatter field is populated and points at a real,
substantial design document (`agents/architect/designs/ENG-*.md`, 145–503
lines each, confirmed to exist and hold real content, not just a linked
path), and seven of the twelve (`ENG-019`, `ENG-020`, `ENG-021`, `ENG-029`,
`ENG-030`, `ENG-035`, `ENG-036`) carry an explicit "Routing: would be
`ready` — held at `designed` instead" line in their own design write-up,
confirming the architect's routing logic already resolved to `ready` and
was deliberately not written. The remaining five (`ENG-014`, `ENG-017`,
`ENG-023`, `ENG-025`, `ENG-026`) state the identical fact in their own
different words instead of that exact phrase — each confirmed individually
by reading its own log paragraph, not inferred from the other seven's
wording. So the citation is correct on all twelve: `chained: none — held by
a cap` is one of
`eng_build_loop.md`'s own four documented no-chain conditions, and re-firing
`continue` on any of them now would only re-discover the same cap with no
new work to do — the exact "burning usage" anti-pattern the chain guardrails
warn against, not a repair. No chain fired for any of the twelve.

One process gap named, not fixed: nothing on this board marks the
cap-held-after-completion sub-state cheaply (a state name, a frontmatter
flag), so every pass that wants to confirm it has to read prose. Filed as an
observation (`observations.md`, this date) rather than a proposal — the
existing `links.design`-populated check is cheap enough that the gap costs
minutes, not a process fix.

**Step 6b:** not run — this pass wrote no new rule about an artifact path,
state name, or config key; it re-read existing gate receipts, merge state,
and ticket frontmatter, and confirmed no change — the bookkeeping category
the rule doesn't apply to.

**Step 7 (notify sweep):** current `2026-09-04T09:31:10Z`. `ENG-008`/
`ENG-009`/`ENG-010` already carry their one-time `nudged:`. `ENG-027`
(~20h16m since `notified:`), `ENG-028` (~17h21m), `ENG-033` (~7h48m), and
all four P0 incident notices (oldest, `ENG-029`, ~18h54m) all still under
24h. Nothing crossed, nothing raised.

**Step 8 (dead-end sweep):** the twelve `designed` tickets above are this
pass's own substantive dead-end check — result: no broken chain, all
correctly cap-held. Beyond that: `traces/.pending` holds the same four
queued fires the prior sweep left (`scheduled launchd`, `watch launchd`,
`scheduled auto-drain`, `scheduled ENG-028`) — normal FIFO backlog under the
still-running `auto-drain` wrapper, not a broken chain. No
`*-eng-events-dropped.md` file exists for today (2026-09-04) — checked
directly. `blocked_from` is present and correct on all four currently
`blocked` tickets (`ENG-008`/`ENG-009`/`ENG-010`/`ENG-033`, all
`ready-to-ship`). `ENG-021`'s own `depends_on: [ENG-022]` remains stale on
its frontmatter (satisfied, per the header's own already-recorded
correction) but not itself a chain break — its sole live hold is the
machine-WIP cap, same as its eleven siblings; left as the header already
has it, not re-corrected a second time.

**Step 8b (observations/exceptions):** one observation filed (above) — the
`links.design`-populated heuristic for the `designed` sub-state split. No
`exception-request:` in any ticket log — grepped `agents/eng-manager/
board/*.md` directly.

**Step 8c (journal):** n/a — no G1/G2/G3 or merge request answered this
pass.

**Board update:** this entry appended; rolled the oldest of the now-four
live dated entries (`continue ENG-033 (security + release-readiness): both
PASS`) to `_index-archive.md` per the keep-three rule. In-flight table and
header prose both unchanged — nothing this pass found required either to
move.

Post-pass `lib/eng-gate-check.sh`, whole-board: exit 0, clean.

`chained: none` — no ticket was touched or transitioned this pass. The
twelve `designed` tickets are genuinely held by the machine-WIP cap (one of
`eng_build_loop.md`'s own four documented no-chain conditions), the four
`blocked` tickets genuinely wait on the approver, and `ENG-018` stays
excluded by its own `priority: hold`. Nothing here is a chain to resume.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-04 — scheduled (auto-drain queue, context `ENG-026`): whole-board re-sweep — no change since prior pass

`scheduled` event pass. The event arrived with context
`agents/eng-manager/board/ENG-026-foodswipe-channel-visibility.md` — a
label riding this fire from the queue's own collapse/drain mechanics
(`traces/.pending` held it as `scheduled ENG-026`, one of the six queued
fires the immediately prior `scheduled` sweep listed as behind it), not a
narrowing instruction: a `scheduled` pass reads the whole procedure
document and sweeps the whole board regardless of what context string it
arrives with, per the reading map's own "never narrowed" rule. Read the
full `eng_build_loop.md` fresh this pass rather than trusting memory of it.
Mode check clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`,
whole-board: exit 0, clean.

**Step 2 (PM intake):** `agents/product-manager/inbox/` and
`inbox/requests/` hold nothing beyond `_handled/`/`.gitkeep` — no new
business intake.

**Step 3 (EM technical intake):** `agents/eng-manager/inbox/` holds nothing
beyond `_processed/`/`.gitkeep` — no new department-originated finding.

**Step 4 (gate returns):** all ten open `inbox/` items re-read fresh —
`ENG-008`/`ENG-009`/`ENG-010` merge requests, `ENG-027`'s rescope G1,
`ENG-028`'s G1, `ENG-033`'s merge request, and all four P0 incident notices
(`ENG-029`/`ENG-030`/`ENG-035`/`ENG-036`, each explicitly "nothing to
decide — informational" in its own body) — every `decision:` field is
still blank on every one. Nothing answered this pass.

**Step 5 (merge detection).** Re-ran fresh for every ticket sitting
`blocked`: `ENG-008`, `ENG-009`, `ENG-010`, `ENG-033` — the same four the
prior sweep found, `ENG-013`/`ENG-015`/`ENG-022`/`ENG-032` all already off
the board as of that pass. `git fetch origin` on both the `aiorders-api`
and `aiorders-admin-hub` worktrees (`~/Documents/projects/_eng/{project}`;
`aiorders-api` carries only its standing untracked
`supabase/functions/brand-portal/deno.lock`, `aiorders-admin-hub` fully
clean), then `git merge-base --is-ancestor` for each ticket's own branch
against `origin/main` on each repo it touches:

| Ticket | Branch | aiorders-api | aiorders-admin-hub |
|---|---|---|---|
| ENG-008 | `feat/ENG-008-influencer-admin-management` | not merged | not merged |
| ENG-009 | `feat/ENG-009-influencer-engagement-info` | not merged | not merged |
| ENG-010 | `feat/ENG-010-influencer-relationship-notes` | not merged | not merged |
| ENG-033 | `feat/ENG-033-catering-request-order-capture-endpoint` | not merged | n/a (single-repo) |

All seven branch checks return **not merged** — identical to the prior
sweep's own table nine minutes earlier. No ticket advances; all four stay
`blocked`.

**Step 6 (dispatch):** machine WIP re-checked fresh from frontmatter, not
the cached header — still `1/1`, held by the `ENG-016` family (`ENG-016`
`building`, `ENG-033` `blocked` on the approver, `ENG-034` `ready` behind
its unmet `depends_on: [ENG-033]`). Step 5 freed nothing, so this pass
frees no machine-WIP slot and starts nothing new. Every `designed` ticket
held behind the family (`ENG-014`, `ENG-017`, `ENG-019`, `ENG-020`,
`ENG-021`, `ENG-023`, `ENG-025`, `ENG-026`, `ENG-029`, `ENG-030`, `ENG-035`,
`ENG-036`) stays exactly where it was — none is a candidate until the
family reaches `shipped`.

**Step 6b:** not run — this pass wrote no new rule about an artifact path,
state name, or config key; it re-read existing gate receipts and merge
state and confirmed no change, the bookkeeping category the rule doesn't
apply to.

**Step 7 (notify sweep):** current `2026-09-04T09:13:55Z`. `ENG-008`/
`ENG-009`/`ENG-010` already carry their one-time `nudged:`. `ENG-027`
(~19h59m since `notified:`), `ENG-028` (~17h4m), `ENG-033` (~7h31m), and
all four P0 incident notices (oldest, `ENG-029`, ~18h37m) all still under
24h — none crosses this pass. Nothing raised: this pass's own findings
(seven unchanged merge-ancestry checks) need no gate.

**Step 8 (dead-end sweep):** `traces/.pending` holds five queued fires
behind this one (`scheduled ENG-027`, `scheduled launchd`, `watch launchd`,
`scheduled auto-drain`, `scheduled ENG-028`) — one fewer than the prior
sweep's own six, consistent with this pass being that list's own
`scheduled ENG-026` entry now drained; normal FIFO backlog under the
still-running `auto-drain` wrapper, not a broken chain. No
`*-eng-events-dropped.md` file exists for today (2026-09-04) — checked
directly. No ticket sits in an agent-owned state with a missing or stale
chain record — this pass touched no ticket, so there is nothing new to
cross-check beyond the prior sweep's own clean result nine minutes ago.
`blocked_from` remains present and correct on all four currently-`blocked`
tickets (unchanged).

**Step 8b (observations/exceptions):** none new filed. Grepped
`agents/eng-manager/board/*.md` for `exception-request:` directly — the
only hits are prior passes' own log lines reporting none found; no live
exception request anywhere on the board.

**Step 8c (journal):** n/a — no G1/G2/G3 or merge request answered this
pass.

**Board update:** this entry appended; rolled the oldest of the now-four
live dated entries (`continue ENG-033 (review+quality): round 4 review
PASS, quality gate round 2 PASS`) to `_index-archive.md` per the keep-three
rule. In-flight table and header prose both unchanged — nothing this pass
found required either to move.

Post-pass `lib/eng-gate-check.sh`, whole-board: exit 0, clean.

`chained: none` — no ticket was touched or transitioned this pass: merge
detection found every branch exactly where the prior sweep left it, no
gate item was answered, and the machine-WIP cap admitted no new start.
There is nothing to fire a next hop onto. The five fires still queued
behind this one in `traces/.pending` will drain on their own; this pass
does not act on them.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-04 — scheduled (auto-drain queue, carrying a stale `ENG-021` context pointer): whole-board sweep — `ENG-013` & `ENG-015` found merged, both `verified`

`scheduled` event pass. The event arrived with context
`agents/eng-manager/board/ENG-021-chat-bar-engagement-and-faq-self-service.md`
— a label riding this `scheduled` fire from the queue's own collapse/drain
mechanics, not a narrowing instruction: a `scheduled` pass reads the whole
procedure document and sweeps the whole board regardless of what context
string it arrives with, per the reading map's own "never narrowed" rule.
Mode check clean (`MODE=active`). Confirmed this pass runs inside the
still-live `auto-drain` wrapper (pid 43028, `eng-trigger.sh scheduled
auto-drain`, ~1h22m into draining tonight's queue when this event
launched) rather than a colliding concurrent process — its own captured
`traces/.pass-out.43028` matched this pass's own transcript, and the
immediately preceding log lines showed the prior `continue ENG-033`
(security + release-readiness) pass end cleanly (`exit 0, 1629s`) before
this event drained. Pre-pass `lib/eng-gate-check.sh`, whole-board and
scoped (`ENG-013`, `ENG-015`): all exit 0, clean.

**Step 2 (PM intake):** `agents/product-manager/inbox/` and
`inbox/requests/` hold nothing beyond `_handled/`/`.gitkeep` — no new
business intake.

**Step 3 (EM technical intake):** `agents/eng-manager/inbox/` holds
nothing beyond `_processed/`/`.gitkeep` — no new department-originated
finding.

**Step 4 (gate returns):** every open item in `inbox/` checked fresh —
`ENG-008`/`ENG-009`/`ENG-010` merge requests, `ENG-027`'s rescope G1,
`ENG-028`'s G1, `ENG-033`'s merge request, and all four P0 incident notices
(`ENG-029`/`ENG-030`/`ENG-035`/`ENG-036`) — every `decision:` field is
still blank. Nothing answered this pass.

**Step 5 (merge detection) — the substance of this pass.** Re-ran fresh for
every ticket sitting `blocked`: `ENG-008`, `ENG-009`, `ENG-010`, `ENG-013`,
`ENG-015`, `ENG-033`. `git fetch origin` on both `aiorders-api` and
`aiorders-admin-hub` worktrees (`~/Documents/projects/_eng/{project}`, both
clean), then `git merge-base --is-ancestor` for each ticket's own branch
against `origin/main`:

| Ticket | Branch | aiorders-api | aiorders-admin-hub |
|---|---|---|---|
| ENG-008 | `feat/ENG-008-influencer-admin-management` | not merged | not merged |
| ENG-009 | `feat/ENG-009-influencer-engagement-info` | not merged | not merged |
| ENG-010 | `feat/ENG-010-influencer-relationship-notes` | not merged | not merged |
| ENG-013 | `feat/ENG-013-foodswipe-funnel-stage-control` | **MERGED** | **MERGED** |
| ENG-015 | `fix/ENG-015-agency-reseller-brand-scoping` | **MERGED** | **MERGED** |
| ENG-033 | `feat/ENG-033-catering-request-order-capture-endpoint` | not merged | n/a (single-repo) |

`ENG-013` and `ENG-015` both merged on **both** repos — cross-checked with
`gh pr view` given both carry security-relevant fixes: `ENG-013`
(`aiorders-api#5` → `1b0c504`, `2026-09-04T06:45:54Z`;
`aiorders-admin-hub#4` → `0583962`, `06:45:37Z`) and `ENG-015`
(`aiorders-api#10` → `d9e0c6d`, `06:44:33Z`; `aiorders-admin-hub#8` →
`2389790`, `06:45:05Z`) — all four merges land within roughly 90 seconds of
each other, the same batch-merge session `ENG-022`'s and `ENG-032`'s own
merges (found by an earlier pass tonight) sat in.

**Not advanced past a state that owes gates**, per step 5's own clause: all
four of each ticket's own gate receipts (migration, code review, quality,
security) re-read directly from disk — `pass` across the board for both —
and both fixes independently re-verified on the merged tree itself, not
taken from the receipts' word alone, before writing `shipped`. Both
carried `blocked → shipped → verified` this pass. Full detail on each
ticket's own board-file log and release record:
`agents/devops/releases/2026-09-04-ENG-013-aiorders-api-and-admin-hub.md`,
`agents/devops/releases/2026-09-04-ENG-015-aiorders-api-and-admin-hub.md`.
`ENG-013`'s own merge-request item had already closed in an earlier pass (a
real scope ambiguity, resolved "Reading A"); `ENG-015`'s
(`inbox/2026-09-03-eng015-merge-request.md`) was still open and moved to
`inbox/_handled/` unchanged, `decision:` left blank — the file itself is
the record, same convention every other silent GitHub merge on this board
has used. Both journaled (`decision-journal.md`).

`ENG-013`'s shipping satisfies `ENG-028`'s sole dependency
(`depends_on: [ENG-013]`); `ENG-028` stays `awaiting-scope`, unaffected in
state, still gated by its own unanswered G1. No other ticket depends on
either.

**Also corrected while sweeping the board for other stale dependency
notes**: the header's own paragraph about `ENG-021`'s `depends_on:
[ENG-022]` still read that branch as "unmerged," but `ENG-022` shipped and
reached `verified` in an earlier pass tonight — checked fresh against
`ENG-022`'s own board file before fixing the prose. `ENG-021` stays
`designed` regardless (machine WIP is its sole remaining hold); see its own
board-file log for the same correction recorded there.

**Step 6 (dispatch):** machine WIP re-checked fresh from frontmatter, not
the cached header — still `1/1`, held by the `ENG-016` family (`ENG-033`
`blocked` on the approver, `ENG-034` `ready` behind it). Neither `ENG-013`
nor `ENG-015` was ever inside the counted `ready..ready-to-ship` range
(both were `blocked`), so this pass **frees no machine-WIP slot** and
starts nothing new. Every `designed` ticket held behind the family
(`ENG-014`, `ENG-017`, `ENG-019`, `ENG-020`, `ENG-021`, `ENG-023`,
`ENG-025`, `ENG-026`) stays exactly where it was.

**Step 6b:** not run — this pass wrote no new rule about an artifact path,
state name, or config key; it read and confirmed existing gate receipts
and recorded two merges, the ordinary bookkeeping category the rule itself
doesn't apply to.

**Step 7 (notify sweep):** current `2026-09-04T09:08:52Z`. `ENG-008`/
`ENG-009`/`ENG-010` already carry their one-time `nudged:`. `ENG-027`
(~19h54m since `notified:`), `ENG-028` (~16h58m), `ENG-033` (~7h26m), and
all four P0 incident notices (oldest, `ENG-029`, ~18h32m) all still under
24h. Nothing crossed, nothing raised — this pass's own findings (two
silent merges) need no gate; they're recorded, not asked about.

**Step 8 (dead-end sweep):** `traces/.pending` holds six queued fires
behind this one (`scheduled ENG-026`, `scheduled ENG-027`, `scheduled
launchd`, `watch launchd`, `scheduled auto-drain`, `scheduled ENG-028`) —
normal FIFO backlog under the still-running `auto-drain` wrapper, not a
broken chain. No `*-eng-events-dropped.md` file exists for today
(2026-09-04) — checked directly, not assumed. Every ticket's last
`chained:` line cross-checked against its own state: no ticket sits in an
agent-owned state with a missing or stale chain record. `blocked_from` is
present and correct on every currently-`blocked` ticket.

**Step 8b (observations/exceptions):** none new filed. No
`exception-request:` in any ticket log this pass.

**Step 8c (journal):** two rows added (`decision-journal.md`) — `ENG-013`
and `ENG-015`'s silent GitHub merges, both dated 2026-09-04.

**Board update:** In-flight table — `ENG-013` and `ENG-015` rows removed
(terminal). Header's unanswered-item count corrected `Seven → Six`
(`ENG-015` drops off); "Waiting on the approver" section's own count,
`ENG-015`'s own paragraph, and its closing "no longer listed here" sentence
all updated to match; closing terminal-tickets paragraph (after the
In-flight table) extended with both tickets' own accounts; `ENG-021`'s
stale `ENG-022`-unmerged note corrected (see above). This entry appended;
rolled the oldest of the now-four live dated entries (`continue ENG-033
(fix): quality-gate finding fixed, stays building`) to `_index-archive.md`
per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, whole-board and scoped (`ENG-013`,
`ENG-015`): all exit 0, clean.

`chained: none` — every ticket this pass actually touched (`ENG-013`,
`ENG-015`) is now `verified`, a terminal state the chaining guard never
fires on. No machine-WIP slot freed, so no other ticket became dispatchable
as a consequence of this pass's own work — `ENG-033` stays `blocked` on the
approver (its own prior pass already correctly declined to chain further),
and every `designed` ticket behind the `ENG-016` family stays held by the
same cap it was held by at pass start.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

---

## 2026-09-04 — continue ENG-033 (security + release-readiness): both PASS, `in-qa → blocked` (L1 merge request raised)

`continue` event pass, context `ENG-033` — the security hop the prior
`continue ENG-033` (review+quality) pass's own `chained: ENG-033` handed off
to. Reading map for `continue`: steps 6 and 6b, plus the not-negotiable set
(1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*).
Mode clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped
(`ENG-033`) and whole-board: both exit 0, clean. Worktree confirmed on
`aiorders-api@697df79`, clean aside from the standing untracked
`brand-portal/deno.lock`; `origin/main` re-fetched, no new commits since
round 4's own check.

**Security gate: PASS.** Full threat model, OWASP walk, LLM checklist n/a,
secrets scan clean. Read `restaurant-portal/CateringDetailModal.tsx` and the
full `catering-request/index.ts` directly rather than trusting prior
rounds' accounts of the render path and the trust boundary. Two
non-blocking findings, both pre-existing and outside this diff: (1) a real
HTML-injection gap in the owner-notification email (Medium — filed as a
proposal, `proposals.md`, 2026-09-04) and (2) `selections[].name` has no
length cap unlike sibling field `note` (Low — logged as an observation
only). Also independently re-verified the standing RLS-on-`catering`
question `agents/security/notebook/2026-09-03-findings.md` named this exact
gate to close empirically — no live DB/Supabase MCP tool available this
session either, so re-derived the static evidence directly instead (found
slightly stronger evidence than the prior account: the migration's own
"Critical Database Security Fixes" framing), reached the same non-blocking
conclusion, and surfaced a direct ask to the approver in this pass's own
merge-request item rather than punting to a fourth ticket. Full writeup:
`agents/security/reviews/ENG-033.md`, `links.security_review` set.

**Release-readiness: PASS.** All three upstream gate receipts re-verified
fresh (review round 4, quality round 2, security this pass). Project is L1
— step 1's window check doesn't apply; step 3's readiness checks (rollback,
observability, cost) all clear, same interpretation this board already
established for `ENG-007`/`ENG-008`/`ENG-013`/`ENG-022`. Opened `aiorders-api`
PR #13 and raised a single-repo L1 merge request
(`inbox/2026-09-04-eng033-merge-request.md`), carrying both security
findings and the RLS ask transparently rather than only in a notebook file.

**2 transitions** (`in-qa → ready-to-ship → blocked`), under the cap of 4.
Machine WIP unaffected — still 1/1, `ENG-016` family (`ENG-034` still
`ready`, dependent on this ticket, so the family's slot doesn't free on one
child leaving the counted range). No approver-facing WIP cap to report
against — uncapped since 2026-09-02; now 7 items listed for visibility (see
header and "Waiting on the approver" above).

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** current `2026-09-04T08:36:57Z` — `ENG-008`/`ENG-009`/
`ENG-010` already carry their one-time `nudged:`; `ENG-015` (~22h33m),
`ENG-027` (~19h21m), `ENG-028` (~16h26m), and all four P0 incident notices
(oldest, `ENG-029`, ~17h59m) still under 24h. Nothing crossed. This pass's
own merge-request item raised and notified — see the ticket's own board-file
log for the exact trace/stamp detail. **Proposal and observation filed**
(both above, both non-blocking). Step 6b: not run — this hop wrote review/
security/merge-request receipts and ticket frontmatter/log only, no
cross-agent artifact rule involved. Journal: n/a — no G1/G2/G3 or merge
request *answered* this pass (one raised; journaling happens once it's
answered).

**Board update:** this entry appended; rolled the oldest of the four
now-live dated entries (`continue ENG-033 (review+quality): round 3 review
PASS, quality gate FAIL`) to `_index-archive.md` per the keep-three rule.
In-flight table: `ENG-033` row `State` moved `in-qa → blocked`, `Owner`
moved `eng-manager → approver`. "Waiting on the approver" header count and
list updated (six → seven items); detailed section carries the new merge
request's own paragraph.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-033`) and whole-board: see
below.

`chained: none` — `blocked`, `blocked_on: approver`. The human gate this
whole pass was driving toward; firing `continue ENG-033` again would only
queue against a ticket with nothing left for a machine to do, same
reasoning `ENG-008`'s and `ENG-022`'s own release-readiness entries already
recorded at this identical state.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-04 — continue ENG-033 (review+quality): round 4 review PASS, quality gate round 2 PASS, `building → in-qa`

`continue` event pass, context `ENG-033` — the combined review+quality hop
the prior `continue ENG-033` (fix) pass's own `chained: ENG-033` handed off
to. Reading map for `continue`: steps 6 and 6b, plus the not-negotiable
set. Mode clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped
(`ENG-033`) and whole-board: both exit 0, clean. Worktree confirmed on
`aiorders-api@697df79`, clean aside from the standing untracked
`deno.lock`; `origin/main` re-fetched — two new merges since round 3's own
check (`ENG-013`, `ENG-015`), neither touching `catering-request/` or
`brand-portal/website.ts` (`admin-portal/` handlers and migrations only).

**Code review: PASS, round 4.** 0/10 automatic failures, re-run fresh.
Isolated the actual change since round 3's own reviewed commit
(`git diff b319a82..697df79`: 3 files) rather than re-reviewing the whole
cumulative diff, and traced the extraction branch-by-branch against the
pre-extraction code: behaviour-preserving on every path (same stored
values, same 400 body/headers/status). Full writeup:
`agents/principal-engineer/reviews/ENG-033.md`, `links.review` content
replaced in place.

**Quality gate: PASS, round 2.** The three criteria round 1 of this gate
found untested — AC-5(storage), AC-6, AC-7 — now each have a passing test
against the extracted `deriveActionStatus`. AC-10/AC-13 unchanged,
not-automated-with-reasons, neither touched by this round's diff. No open
P0/P1. Full writeup: `agents/qa/test-plans/ENG-033.md`, `links.test_plan`
content updated in place (round 1 kept as history in the same file).

**Independent verification was this hop's own center of gravity, not
trusted from the fix hop's account.** Ran the suite fresh (17/17), then
mutation-tested two branches of `deriveActionStatus` directly — removing
the `MANUAL_CONTACT_REQUESTED` force-null flipped exactly the
discard-on-purpose test (16 passed/1 failed, right reason); corrupting the
absent/unrecognised fallback's `status` flipped exactly the two tests on
that branch (15 passed/2 failed) — each mutation restored via
`git checkout --` against the committed `697df79` baseline (safe here,
unlike the fix hop's own noted mistake against an uncommitted diff), suite
re-confirmed clean after each. Lint on all four touched files: 11
problems, reconciling exactly against round 3's own count, attributed
file-by-file this time — 0 new, and `validation.ts` itself (the only file
carrying this hop's logic) has zero lint issues. `deno check` fails
identically (pre-existing `npm:openai` gap). No other caller of the moved
symbols anywhere in the repo. Round 3's deferred header-comment correction
verified against the actual `platform-customer-auth/validation.ts` file
rather than accepted on faith: accurate.

**2 transitions** (`building → in-review → in-qa`), under the cap of 4.
Machine WIP unaffected — still 1/1, `ENG-016` family. No approver-facing
WIP or approval-cap change. `time_spent`/`time_remaining` updated in
frontmatter.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** current `2026-09-04T08:18:28Z` — `ENG-008`/`ENG-009`/
`ENG-010` already carry their one-time `nudged:`; `ENG-015` (~22h15m),
`ENG-027` (~19h3m), `ENG-028` (~16h8m), and all four P0 incident notices
(oldest, `ENG-029`, ~17h41m) still under 24h. Nothing crossed, nothing
raised — a review/quality pass isn't approver-facing on its own. No new
proposal or observation filed: this hop's own minor finding (round 3's
prose loosely described the lint reconciliation as "two pre-existing
`no-explicit-any`/`no-prototype-builtins` items" where the actual
file-by-file count is four `no-explicit-any` plus one
`no-prototype-builtins`) changed no verdict and isn't filed further — noted
in the ticket log only. Step 6b: not run — this hop wrote review/test-plan
receipts and ticket frontmatter/log only. Journal: n/a — no G1/G2/G3 or
merge request answered this pass.

**Board update:** this entry appended; rolled the oldest of the now-four
live dated entries (`continue ENG-033 (fix): round 2 finding fixed`) to
`_index-archive.md` per the keep-three rule. In-flight table: `ENG-033` row
`State` moved `building → in-qa`, `Updated` unchanged (`2026-09-04`).

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-033`) and whole-board: both
exit 0, clean.

`chained: ENG-033` — `in-qa` is agent-owned (security next); not the
approver, not blocked, not terminal, not held by a cap. Fired `/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-033` before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-04 — continue ENG-033 (fix): quality-gate finding fixed, stays `building`

`continue` event pass, context `ENG-033` — the fix hop the prior `continue
ENG-033` (review+quality) pass's own `chained: ENG-033` handed off to.
Reading map for `continue`: steps 6 and 6b, plus the not-negotiable set.
Mode clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped
(`ENG-033`) and whole-board: both exit 0, clean. Worktree confirmed on
`aiorders-api@b319a82`, clean aside from the standing untracked
`deno.lock`; `origin/main` re-fetched, no new commits since round 3's own
check.

**Applied the specific fix quality gate named, no more.** Extracted the
status-derivation block (`index.ts:247-264`) into `deriveActionStatus()` in
`validation.ts`, alongside `isValidSelections` — same file, using the
latitude round 2's own export was given. Pure function, no `Response`, no
I/O: returns `{ actionType, selections, status, selectionsInvalid }`;
`index.ts` destructures it and turns `selectionsInvalid` into the existing
400 — the insert-object code below needed no edit, since it already read
`normalizedActionType`/`normalizedSelections`/`derivedStatus` by name.
`VALID_ACTION_TYPES` moved into `validation.ts` with it (its only caller).
Also fixed round 3's own deferred non-blocking note while touching this
file for the first time since it was raised: the header comment named the
wrong `platform-customer-auth` sibling (`handler.ts`) as precedent —
corrected to `validation.ts`.

**Tests:** added the five cases quality gate's finding named, in
`index.test.ts` — `action_type` absent; unrecognized `action_type` treated
the same as absent; `MANUAL_CONTACT_REQUESTED` with non-empty `selections`
still forcing `null` (the discard-on-purpose case flagged as most likely to
silently regress); `QUOTE_SUBMITTED` valid → stored as-is; `QUOTE_SUBMITTED`
invalid → `selectionsInvalid`. 17/17 pass (`deno test --no-check
index.test.ts`, the QA test plan's own `suite_command`).
**Self-mutation-tested the discard-on-purpose case** before trusting the
green run: removed the force-null, got 16 passed/1 failed — the right test,
for the right reason. **One error during this step, corrected in the same
hop:** restored via `git checkout --`, which discarded this hop's entire
*uncommitted* extraction rather than just the mutation, since none of it
had been committed yet (unlike round 3's own use of that command against an
already-committed baseline). Caught immediately, redid the extraction
identically, re-ran clean: 17/17. Full account, including this correction:
`ENG-033`'s own board-file log.

**Lint:** 6 problems on the three touched files, reconciling exactly
against round 3's own combined count (6 + 5 on `website.ts`, not touched
this round = 11) — 0 new. **`deno check`:** fails identically, same
pre-existing `npm:openai` resolution gap, unrelated. Committed and pushed:
`aiorders-api@697df79`.

**0 transitions** — `state`/`owner` unchanged (`building`/`eng-manager`): a
review pass, not this fix, is what moves the ticket forward.
`time_spent`/`time_remaining`/`branch` updated in frontmatter. WIP/approval
caps unaffected.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** current `2026-09-04T08:05:05Z` — `ENG-008`/`ENG-009`/
`ENG-010` already carry their one-time `nudged:`; `ENG-015` (~22h1m),
`ENG-027` (~18h50m), `ENG-028` (~15h55m), and all four P0 incident notices
(oldest, `ENG-029`, ~17h28m) still under 24h. Nothing crossed, nothing
raised — a build/fix hop isn't approver-facing. No new proposal or
observation beyond the `git checkout --` correction noted above (recorded
in the ticket log, not filed separately — cost this hop one redo, nothing
downstream). Step 6b: not run — product code internal to one repo, no
artifact rule involved. Journal: n/a — no G1/G2/G3 or merge request
answered this pass.

**Board update:** this entry appended; rolled the oldest of the now-four
live dated entries (`continue ENG-033 (review): round 2 FAIL`) to
`_index-archive.md` per the keep-three rule. In-flight table: `ENG-033` row
`Updated` unchanged (`2026-09-04`, `building`/`eng-manager` — state didn't
move).

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-033`) and whole-board: both
exit 0, clean.

`chained: ENG-033` — `building` is agent-owned (next hop is review+quality
round 4, against the fresh diff); not the approver, not blocked, not
terminal, not held by a cap. Fired `/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-033` before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-04 — continue ENG-033 (review+quality): round 3 review PASS, quality gate FAIL, stays `building`

`continue` event pass, context `ENG-033` — the combined review+quality hop
the prior `continue ENG-033` (fix) pass's own `chained: ENG-033` handed off
to. Reading map for `continue`: steps 6 and 6b, plus the not-negotiable
set. Mode clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped
(`ENG-033`) and whole-board: both exit 0, clean. Worktree confirmed on
`aiorders-api@b319a82`, clean aside from the standing untracked
`deno.lock`; `origin/main` re-fetched, no new commits since round 2's own
check.

**Code review: PASS, round 3.** 0/10 automatic failures. Round 2's sole
finding (missing test on the round-1 `note` bug fix) closed:
`index.test.ts` covers the regression by name plus every design-named
boundary. Mutation-tested the regression test directly this round (reverted
`validation.ts`'s note check to the round-1 buggy line, got 11 passed/1
failed — the right test, for the right reason) rather than trusting the
fix hop's own "12/12 pass" account, since round 2 had explicitly asked for
this verification and the fix hop's log didn't record doing it. One new
non-blocking note: `validation.ts`'s header comment names the wrong
`platform-customer-auth` sibling as its mirrored precedent (`handler.ts`
instead of `validation.ts`) — reasoning still correct, not blocking. Full
writeup: `agents/principal-engineer/reviews/ENG-033.md`, `links.review`
set.

**Quality gate: FAIL — the first time it has actually run on this ticket**
(rounds 1 and 2 both failed at review, so QA's result was discarded both
times). AC-5/6/7 (this ticket's own, per `ENG-032`'s scope note) are
implemented by `index.ts:247-264`'s status-derivation branching, and
nothing tests it — only its downstream `isValidSelections` dependency is
tested. Traced by hand against the design's table and confirmed correct,
but per `agents/qa/agent.md`'s own refusal of "manually verified" standing
in for a test the logic could actually support, this doesn't clear the
gate: the branching has no I/O of its own and can be extracted and tested
the same way `isValidSelections` just was. AC-10/AC-13 recorded as not
automated, with reasons, not blocking. Specific fix and full finding:
`agents/qa/test-plans/ENG-033.md`.

**0 net transitions** — `state`/`owner` unchanged (`building`/
`eng-manager`): the ticket returns to `building` on the quality finding,
not the review one; review's own PASS stands and will be re-confirmed
fresh against the next diff, not re-litigated. WIP/approval caps
unaffected. `links.review` and `links.test_plan` both set for the first
time this ticket. `time_spent`/`time_remaining` updated in frontmatter.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** current `2026-09-04T07:53:12Z` — `ENG-008`/`ENG-009`/
`ENG-010` already carry their one-time `nudged:`; `ENG-015` (~21h49m),
`ENG-027` (~18h38m), `ENG-028` (~15h43m), and all four P0 incident notices
(oldest, `ENG-029`, ~17h16m) still under 24h. Nothing crossed, nothing
raised — a quality-gate fail isn't approver-facing. No new proposal — the
finding closes within this ticket's own next hop; recorded instead in
`agents/qa/notebook/2026-09-04-coverage-gaps.md` as a two-instance pattern
worth watching (logic left inline in `index.ts`'s `serve()` callback
turning out untestable), not yet a three-occurrence promotion. Step 6b: not
run — this hop wrote review/test-plan receipts and ticket frontmatter/log
only. Journal: n/a — no G1/G2/G3 or merge request answered this pass.

**Board update:** this entry appended; rolled the oldest of the four
now-live dated entries (`continue ENG-033 (fix): round 1 finding fixed`) to
`_index-archive.md` per the keep-three rule. In-flight table: `ENG-033` row
`Updated` unchanged (`building`/`eng-manager` — state didn't move).

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-033`) and whole-board: both
exit 0, clean.

`chained: ENG-033` — `building` is agent-owned (next hop is the fix:
extract and test the derivation logic, then review+quality round 4); not
the approver, not blocked, not terminal, not held by a cap. Fired `/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-033` before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-04 — continue ENG-033 (fix): round 2 finding fixed, stays `building`

`continue` event pass, context `ENG-033` — the fix hop the prior `continue
ENG-033` (review) pass's own `chained: ENG-033` handed off to. Reading map
for `continue`: steps 6 and 6b, plus the not-negotiable set. Mode clean
(`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-033`) and
whole-board: both exit 0, clean.

**Found the fix already sitting uncommitted in the worktree, from a session
that crashed before finishing.** `traces/eng-loop-2026-09-04.log` shows a
`continue (ENG-033)` launch at `00:27:23` and then stops dead — 18 lines
total, no `pass end` ever written, `traces/.hops-2026-09-04-ENG-033` still
at the same count that session started with. That session had done the
real work in the meantime (`catering-request/validation.ts` and
`index.test.ts`, mtimes `00:30:11`–`00:30:59`, plus a matching `index.ts`
edit) — exactly round 2's own spec — but never committed, logged, or
chained. Verified rather than trusted before building on it: read the full
diff, cross-checked all 12 test cases against the design's own validation
table, ran `deno test` (12/12 pass) and `deno lint` (found and fixed one
real new issue — an unused destructured `note`; the other 6 problems are
this repo's standing no-`deno.json` gap, confirmed pre-existing via a
`git stash`-isolated baseline lint), and grepped the repo for any other
reference to the extracted `isValidSelections`/`MAX_SELECTIONS`/
`MAX_NOTE_LENGTH` (none). Committed and pushed: `aiorders-api@b319a82`.
Widened the open `proposals.md` (2026-08-30) row rather than filing a new
one — this occurrence never reached a commit at all, so that row's
proposed `git log`-against-hash fix wouldn't have caught it; needs a
working-tree check too. Full account, including the trace-log evidence:
`ENG-033`'s own board-file log.

**0 transitions** — `state`/`owner` unchanged (`building`/`eng-manager`):
a review *pass*, not this fix, is what moves the ticket forward.
WIP/approval caps unaffected.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** current `2026-09-04T07:31:47Z` — every open `inbox/`
item still under 24h or already carrying its one nudge; the four P0
incident notices left as-is, same standing treatment. Nothing crossed,
nothing raised. No new observations beyond the widened proposal noted
above. Step 6b: not run — product code internal to one repo, no artifact
rule involved. Journal: n/a — no G1/G2/G3 or merge request answered this
pass.

**Board update:** this entry appended; rolled the oldest of the now-four
live dated entries (`continue ENG-033 (review): round 1 FAIL`) to
`_index-archive.md` per the keep-three rule. In-flight table: `ENG-033`
row `Updated` bumped to `2026-09-04` (state didn't move,
`building`/`eng-manager`).

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-033`) and whole-board: both
exit 0, clean.

`chained: ENG-033` — `building` is agent-owned (next hop is review round
3, principal-engineer); not the approver, not blocked, not terminal, not
held by a cap. Fired `/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-033` before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-04 — continue ENG-033 (review): round 2 FAIL, stays `building`

`continue` event pass, context `ENG-033` — the combined review+quality hop
the prior `continue ENG-033` (fix) pass's own `chained: ENG-033` handed off
to. Reading map for `continue`: steps 6 and 6b, plus the not-negotiable
set. Mode clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped
(`ENG-033`) and whole-board: both exit 0, clean. Worktree confirmed on
`aiorders-api@b9a22a2`, clean aside from the standing untracked
`deno.lock`; `origin/main` re-fetched, its only new commits since this
branch's base (`ENG-013`/`ENG-015`) confirmed not touching either file this
ticket changes.

**Principal-engineer review: FAIL, round 2.** 1/10 automatic failures —
"missing test on a bug fix." Round 1's blocking finding (a
present-but-non-string `note` bypassing validation and reaching
`restaurant-portal`'s unguarded render) was fixed correctly in `b9a22a2`,
re-verified line-for-line against the current diff — but shipped with no
regression test, and `catering-request/` has no test file at all despite
`isValidSelections` being the same shape (a pure boundary-validation
predicate) as this same repo's own same-day precedent,
`platform-customer-auth/validation.ts`, which already tests exactly this
edge-case class. `engineering-standards.md` treats this with no exceptions.
Full finding, the empirical infra check, and the direct `ENG-032`
round-1/round-2 precedent this ticket's fix hop didn't follow:
`agents/principal-engineer/notebook/2026-09-04-review-log.md`; ticket log:
`ENG-033`'s own board file.

No receipt written, `links.review` untouched. QA's hop discarded this round
too — same precedent `ENG-032`'s own round 1 set for this identical
failure class, no test-plan file. **0 net transitions** — `state`/`owner`
unchanged (`building`/`eng-manager`), same shape round 1 used.
WIP/approval caps unaffected.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** current `2026-09-04T07:07:55Z`, re-read fresh from each
inbox file — `ENG-008`/`ENG-009`/`ENG-010` already carry their one-time
`nudged:`; `ENG-015` (~21h), `ENG-027` (~18h), `ENG-028` (~15h), and all
four P0 incident notices (oldest ~16h30m) still under 24h. Nothing crossed,
nothing raised — a review fail isn't approver-facing. No new observations —
the missing-test finding is this round's own verdict, not a process gap;
the already-open proposal on `aiorders-api`'s unregistered test command
(`proposals.md`, 2026-09-03) covers the adjacent config-staleness point and
isn't restated here. Step 6b: not run, review hop not a build hop. Journal:
n/a.

**Board update:** this entry appended; rolled the oldest of the now-four
live dated entries (`continue ENG-033 (build): ready → building`) to
`_index-archive.md` per the keep-three rule. In-flight table: `ENG-033` row
unchanged (`building`/`eng-manager` — state didn't move).

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-033`) and whole-board: both
exit 0, clean.

`chained: ENG-033` — `building` is agent-owned (next hop is fix round 2:
add the missing test, then review round 3); not the approver, not blocked,
not terminal, not held by a cap. Fired `/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-033` before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-033 (fix): round 1 finding fixed, stays `building`

`continue` event pass, context `ENG-033` — the fix hop the prior `continue
ENG-033` (review) pass's own `chained: ENG-033` handed off to. Reading map
for `continue`: steps 6 and 6b, plus the not-negotiable set. Mode clean
(`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-033`) and
whole-board: both exit 0, clean.

**Applied the exact fix round 1 specified.** `isValidSelections`
(`catering-request/index.ts:176`) checked `note`'s length only when it was
already a `string`; changed to reject any present non-string `note`,
symmetric with `name`. Cross-checked against the design's own `## Data`
section (`"note": string | null`) — the fix enforces exactly that contract.
The two non-blocking notes and the style preference from round 1 were left
alone, as specified. `deno check` fails identically before/after
(pre-existing, unrelated); `deno lint` on both touched files: 10 problems
at the committed baseline and 10 after — zero new. Committed and pushed:
`aiorders-api@b9a22a2`. Full account: `ENG-033`'s own board-file log.

**0 transitions** — `state`/`owner` unchanged (`building`/`eng-manager`): a
review *pass*, not this fix, is what moves the ticket forward. WIP/approval
caps unaffected.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** current `2026-09-04T06:55:55Z` — every open `inbox/` item
still under 24h or already carrying its one nudge; the four P0 incident
notices left as-is, same standing treatment. Nothing crossed, nothing
raised. No new observations. Step 6b: not run — one-line logic fix, no
artifact rule involved. Journal: n/a — no G1/G2/G3 or merge request
answered this pass.

`chained: ENG-033` — `building` is agent-owned (next hop is review round
2, principal-engineer); not the approver, not blocked, not terminal, not
held by a cap. Fired `/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-033` before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-033 (review): round 1 FAIL, stays `building`

`continue` event pass, context `ENG-033` — the combined review+quality hop
the prior `continue ENG-033` (build) pass's own `chained: ENG-033` handed
off to. Reading map for `continue`: steps 6 and 6b, plus the not-negotiable
set. Mode clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped
(`ENG-033`) and whole-board: both exit 0, clean. Machine WIP re-checked
fresh off frontmatter: still `1/1`, the `ENG-016` family unchanged.

**Principal-engineer review: FAIL, round 1.** 0/10 automatic failures, but
one blocking correctness finding in `catering-request/index.ts`'s new
`isValidSelections`: a present-but-non-string `note` skips validation
entirely and reaches `restaurant-portal`'s already-shipped
`CateringDetailModal`, which renders it as a bare JSX child with no error
boundary anywhere in that app — an object `note`, trivially postable
through this unauthenticated endpoint, throws on render. Cites
`engineering-standards.md`'s existing "failure direction is uniform" rule
directly rather than raising a new preference. Full finding, the
interpretation-call reasoning, and two non-blocking notes:
`agents/principal-engineer/notebook/2026-09-03-review-log.md`; ticket log:
`ENG-033`'s own board file.

No receipt written, `links.review` untouched. QA's hop not run this round
(discarded — the flagged code is about to change), no test-plan file. **0
net transitions** — `state`/`owner` unchanged (`building`/`eng-manager`),
same shape this board's other round-1 fails (`ENG-008`/`ENG-013`/`ENG-015`/
`ENG-032`) already set. WIP/approval caps unaffected.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** current `2026-09-04T06:48:23Z` — every open `inbox/` item
still under 24h or already carrying its one nudge; the four P0 incident
notices left as-is, same standing treatment. Nothing crossed, nothing
raised — a review fail isn't approver-facing. No new observations — the
`ticket_log.entry` cap-lines gap this entry itself is written under is
already tracked (`observations.md`, 2026-09-03). Step 6b: not run, this is
a review hop, not a build hop. Journal: n/a — no G1/G2/G3 or merge request
answered this pass.

**Board update:** this entry appended, still three live dated entries (no
roll needed this pass). In-flight table: `ENG-033` row unchanged
(`building`/`eng-manager` — state didn't move).

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-033`) and whole-board: both
exit 0, clean.

`chained: ENG-033` — `building` is agent-owned (round 1's finding is the
next hop's own work: fix `isValidSelections`, then review round 2); not the
approver, not blocked, not terminal, not held by a cap. Fired `/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-033` before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-033 (build): `ready → building`

`continue` event pass, context `ENG-033` — per the prior `scheduled`
sweep's own `chained: ENG-033`. Reading map for `continue`: steps 6 and 6b
(design already complete, no mid-PRD checkpoint applies), plus the
not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four
lanes*, *Guards*). Mode check clean (`MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-033`) and whole-board: both exit 0,
clean.

Machine WIP re-checked fresh off every ticket's own frontmatter: still
`1/1`, the `ENG-016` family (`ENG-016` `building`; `ENG-031`/`ENG-032`
`verified`; `ENG-034` `ready`) — this transition swaps which family member
is active, not the count.

Fixed the `aiorders-api` worktree's branch before use (still on `ENG-031`'s
own now-merged branch, the identical slip `ENG-031` and `ENG-032` each
already caught) and branched fresh off updated `origin/main` rather than
renaming in place, since `origin/main` had moved past `ENG-031`'s tip in
the interim. Built both `aiorders-api` rows of the design's `## Components`
table: `catering-request/index.ts` (destructure/validate/derive-status) and
`brand-portal/website.ts` (`CateringPageContent`'s two new keys, mirrored
off `restaurant-portal`'s already-shipped copy of the same interface).
`deno lint`: zero new (10/10, pristine-diffed); `deno check` fails
identically before and after (pre-existing — no `deno.json` anywhere in
this repo). Committed and pushed: `aiorders-api@e3ef26a`
(`feat/ENG-033-catering-request-order-capture-endpoint`). No PR yet —
devops's release-readiness hop opens it. Full account, including the one
interpretation call on non-string `note` handling:
`ENG-033`'s own board-file log.

**1 transition** (`ready → building`), under the cap of 4. No WIP/approval
cap change. Notify sweep: nothing crossed 24h. Dead-end sweep (scoped): no
other ticket touched. No observations filed. Step 6b: not run — product
data/interface keys, not business-os process artifacts (same reasoning
`ENG-032`'s and `ENG-024`'s own hops already set). Journal: n/a.

**Board update:** this entry appended; rolled the oldest of the now-four
live dated entries (`scheduled: whole-board sweep — ENG-022 shipped, two
dead ends found and fixed`) to `_index-archive.md` per the keep-three rule.
In-flight table: `ENG-033` row `ready → building`. Closing terminal-tickets
paragraph (`ENG-022`/`ENG-032`) gained a clause noting the dedicated
session has since moved `ENG-033` to `building`.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-033`) and whole-board: both
exit 0, clean.

`chained: ENG-033` — `building` is agent-owned (next hop `in-review`,
principal-engineer); not the approver, not blocked, not terminal, not held
by a cap. Fired `/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-033` before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

---

## 2026-09-03 — scheduled: whole-board sweep — ENG-032 shipped, ENG-033 dispatched

`scheduled` event pass (safety-net sweep, four-times-daily cadence; fired
with `ENG-020` tagged as context but read in full per the reading map's own
instruction — a scheduled pass is never narrowed). Mode check clean
(repo-root `.env` → `MODE=active`). Pre-pass board state confirmed clean via
the prior pass's own recorded post-pass `lib/eng-gate-check.sh` result
(whole-board, exit 0); re-run whole-board at the end of this pass (below).

**Steps 2–4:** all three watched inboxes swept.
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold
nothing but their own `_handled`/`_processed` folders; `inbox/requests/` is
empty. `inbox/` held 11 open items (12 minus `ENG-031`'s, already archived
by an earlier pass tonight) — every `decision:` field and `## Decision`
body read fresh and directly: all 11 blank/unfilled boilerplate. Nothing to
act on.

**Step 5 — merge detection**, every ticket `blocked` on an L1 PR: `git
fetch origin` + `git merge-base --is-ancestor` in each of the three
worktrees (`aiorders-api`, `aiorders-admin-hub`, `restaurant-portal`).
`ENG-008`, `ENG-009`, `ENG-010`, `ENG-013` (both repos each) and `ENG-015`
(both repos) all **not merged** — stay `blocked`. `ENG-032`
(`feat/ENG-032-catering-portal-stages-and-itemized-view`,
`restaurant-portal`): **merged** — branch tip (`77631b0`) is itself the
merge-base of the branch and `origin/main`, i.e. the whole branch is
cleanly contained; cross-checked with `gh pr view 2 --repo
harsimranwalia/restaurant-portal` (not required at this severity, done
anyway since the tool was already open): `state: MERGED`, mergedAt
`2026-09-04T04:56:20Z`, merge commit `5276a53` = `origin/main`'s exact tip.
All three receipts re-read fresh (`pass` on review round 2/quality/
security), no migration owed (none applies — confirmed no `*.sql` in the
diff), the two new stages/itemized-selections block/`orderFormEnabled`
switch independently re-verified present on `origin/main` via `git show`.
Carried `blocked → shipped → verified` — release record
`agents/devops/releases/2026-09-03-restaurant-portal-ENG-032.md`,
merge-request item moved to `inbox/_handled/`, `decision-journal.md` row
added (eighth silent-GitHub-merge occurrence, second on an `ENG-016`-family
sub-ticket). Full account: `ENG-032`'s own board-file log.

**Step 6 — dispatch.** `ENG-032`'s shipping satisfies `ENG-033`'s last
unmet dependency (`depends_on: [ENG-031, ENG-032]`, `ENG-031` already
`verified`). Machine WIP re-verified fresh from every ticket's own
frontmatter: still `1/1`, the `ENG-016` family — `ENG-033` was already
inside the counted `ready..ready-to-ship` range as a family member, so
dispatching it swaps which member is active, not how many. **Not built
inline this pass** — same precedent this board set on `ENG-032` itself when
`ENG-031` shipped for it (and on `ENG-024`/`ENG-022` before that): a
whole-board sweep does not perform new implementation work. `ENG-034`
(`depends_on: [ENG-033]`) remains blocked on `ENG-033` specifically — no
other family member is dispatchable, so no ordering choice to make. Fired
`continue ENG-033`; full reasoning on `ENG-033`'s own board-file log.
Checked all 12 `designed`-state tickets (`ENG-014`, `017`, `019`–`021`,
`023`, `025`, `026`, `029`, `030`, `035`, `036`) for an unraised G2 — all 12
still carry their own "no one-way door, no G2" determination from their
design pass (grepped each directly; two files' hits fell across a line
wrap, re-read in full to confirm rather than trusted from the grep count
alone), nothing further to raise.

**Step 6b:** not run — no build hop this pass, no new rule about an
artifact path/state name/config key written or relied on.

**Step 7 — notify sweep.** No new gate item raised this pass (`ENG-032`'s
merge request was archived, not created). Nudge-eligibility checked for
every open, non-incident item against current time (`2026-09-04T06:04:13Z`):
`ENG-015` (~20h00m), `ENG-027` rescope (~16h49m), `ENG-028` (~13h54m) — all
under 24h. `ENG-008`/`ENG-009`/`ENG-010` already carry their one-time
`nudged:`. The four P0 incident notices (`ENG-029`/`030`/`035`/`036`) left
un-nudged, same standing informational treatment. Nothing due.

**Step 8 — dead-end sweep, run in full.** Owner-blank check across every
board file: none. `ENG-018`'s `priority: hold` re-verified intact (restored
by the immediately prior `scheduled` pass; no re-clobber). `traces/.pending`:
queued `scheduled`/`watch` backlog persists (unremediated, same "busy-day
backlog, drains on subsequent fires" reading the prior pass gave it) plus
this pass's own fresh `continue ENG-033`. No `*-eng-events-dropped.md` file
dated 2026-09-03 or 2026-09-04 — no drops to remediate. No live
`exception-request:` anywhere on the board (grepped directly; the only two
hits are prior passes' own "none found" notes). `agents/qa/bugs/_index.md`:
`BUG-001` owned (devops), not a dead end. **Chain-health check** across
every ticket sitting in an agent-owned state (all `designed`/`building`/
`ready` rows): each carries a valid last `chained:` record — either a
`chained: none` with a documented cap/wait reason, or a fresh `chained:
ENG-033` from this pass. No broken or silently-dropped chain found.

**One real finding, non-blocking, filed as an observation rather than
fixed in place:** the header's now-superseded `ENG-032` paragraph read "P1
fix for a live cross-tenant restaurant-visibility/write exposure" — a
copy-paste bleed from the adjacent `ENG-015` paragraph, not a claim about
`ENG-032`'s own diff (catering-board stages, `severity: P2` throughout).
Corrected naturally while rewriting that paragraph to record the merge/ship
this pass; no operational consequence (frontmatter was never wrong, gate
receipts were re-read directly). Logged: `observations.md`.

**Step 8c — journal.** `ENG-032`'s silent GitHub merge journaled in
`decision-journal.md` (see step 5 above). No G1/G2/G3 answered this pass.

**Step 9 — chain.** `ENG-032` reached `verified` (terminal, no chain).
`ENG-033` dispatched via `continue ENG-033`, fired this pass (confirmed
appended to `traces/.pending`). No other ticket was touched.

**Board update:** this entry appended; rolled the oldest of the four
now-live dated entries (`watch: inbox sweep, no new work — ENG-032's PR
still open`) to `_index-archive.md` per the keep-three rule. In-flight
table: `ENG-032` row removed (terminal). Header bullet, "Waiting on the
approver" count (`seven → six`) and list, and the closing terminal-tickets
paragraph all updated to record `ENG-032` alongside `ENG-022` and to note
`ENG-033`'s dispatch.

Post-pass `lib/eng-gate-check.sh`, whole-board: exit 0, clean.

`chained: ENG-033` recorded on this pass's own account; `chained: none`
(terminal) on `ENG-032`'s own log.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.


## 2026-09-03 — continue ENG-019 (design): stays `designed`, held by machine WIP

`continue` event pass, context `ENG-019` — resuming the chain the prior
`scheduled` sweep re-fired after finding the last attempt's background
design subagent killed at its own 600s timeout with nothing written. Reading
map for `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b,
9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*). Mode check
clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-019`)
and whole-board: both exit 0, clean.

Ran `tech-design/SKILL.md` **in this session directly, no background
subagent delegated for the substantive work** — the thing that killed the
last attempt. Read the PRD, this ticket's own Notes, `decision-journal.md`,
`observations.md`, `projects.md`, and — the bulk of it — `origin/main`
directly across `aiorders-api` (`outgoing-communications`, `autopilot`,
`brand-portal`, `_shared/restaurantAccess.ts`, `cloudwaitress-middleware`,
`external-integrations/handlers/cloudwaitress.ts`) and `restaurant-portal`
(`pages/autopilot/Automations.tsx`), plus tonight's sibling ADRs
(`ADR-011`/`012`/`015`/`016`/`017`).

**Three ADRs, all reversible, resolving the three risks the PRD's own G1
approval named as the architect's to resolve:** `ADR-018` (mass
dispatch/scheduling is a `pg_cron` poller claiming due rows every 5 minutes
— `platform_analytics_cron`'s own structural precedent — not per-recipient
`autopilot`-style QStash scheduling, which is proven at one-message-per-
event scale, not one-action-enrolls-thousands scale); `ADR-019` (the PRD's
own assumed redemption-tracking mechanic doesn't exist — `coupon_code` is a
plain display string everywhere in this codebase — but the data AC4 needs
already lands in `orders.promos`/`total_amount` via CloudWaitress's
existing webhook, so this is a read against already-captured data, not a
new capture path); `ADR-020` (opt-out reuses `customers.consent_email`/
`consent_sms`, already written on every customer at creation with the exact
CASL "implied consent" reasoning the PRD's own Risks argue in prose, via a
new small public `broadcast-unsubscribe` function rather than a hole cut
into `outgoing-communications`' just-tightened auth gate). **No one-way
door** — checked against all five categories explicitly in the design's own
section; none qualify.

**Design:** `agents/architect/designs/ENG-019-restaurant-marketing-broadcasts.md`.
Three new tables (`broadcast_campaigns`/`broadcast_campaign_steps`/
`broadcast_campaign_recipients`), one new `brand-portal` action file
(`ADR-011`'s own precedent), one new dispatcher function, one new public
unsubscribe function — full component list, data intent/constraints, and
failure-mode reasoning (idempotent claiming under an overlapping tick,
opted-out-between-drip-steps re-check, empty-audience no-op, mid-flight-edit
rejection) in the design itself. `touches_data: true` (`database` owns the
migration at work-breakdown); `touches_models: false` (owner-authored
content throughout, no model call anywhere in this design).

**Routing (step 11): would be `ready` — held at `designed` instead.**
Neither L0 nor a one-way door. **Machine WIP re-checked fresh from every
ticket's own frontmatter this pass:** still `1/1`, the `ENG-016` family
(`ENG-016` `building`; `ENG-032` `blocked`/approver; `ENG-033`/`ENG-034`
`ready`, both still behind their own unmet `depends_on`). Same precedent
`ENG-014`/`ENG-017`/`ENG-020`/`ENG-021`/`ENG-023`/`ENG-025`/`ENG-026`
already set today: held at `designed`, owner staying `architect`, rather
than writing `ready` while the one slot is occupied. `ENG-019` added to the
header's held-for-slot list above (it read as broken/incomplete, not yet
belonging there, until this pass actually finished the design).

**One observation filed** (`observations.md`): `supabase/functions/
README.md`'s "Known issues" section still names a `brand-portal/offers.ts`
argument-order bug that reading `offers.ts` directly shows already fixed
(consistent with `ENG-022`, merged this evening) — the doc just never
caught up. Not this ticket's to fix.

**Notify sweep:** no new gate item (no one-way door). Swept `inbox/`'s 11
open items fresh against the 24h threshold (current
`2026-09-03T22:55:24-07:00`): nothing crosses it — closest is
`eng015-merge-request` at ~12h51m; `eng008`/`009`/`010` already carry their
one-ever nudge; the four P0 incident notices left un-nudged, same standing
treatment.

**Dead-end sweep (scoped to this event):** no other ticket touched — the
machine-WIP occupancy check above doubled as a fresh confirmation that the
`ENG-016` family's own four rows still match `_index.md`'s own account
exactly.

**Board update:** header's Machine-WIP paragraph gained `ENG-019` in the
held-for-slot list. In-flight table: `ENG-019`'s own row unchanged
(state/owner/priority didn't move). This entry appended; rolled the oldest
of the now-four live dated entries (`continue ENG-032: release-readiness
PASS, PR opened, now blocked`) to `_index-archive.md` per the keep-three
rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-019`) and whole-board: both
exit 0, clean.

`chained: none` — held by the machine-WIP cap (`1/1`, the `ENG-016`
family), one of the documented no-chain conditions. Full reasoning:
`ENG-019`'s own board-file log.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — scheduled: whole-board sweep — ENG-022 shipped, two dead ends found and fixed

`scheduled` event pass (safety-net sweep, four-times-daily cadence; fired
with `ENG-019` tagged as context but read in full per the reading map's own
instruction — a scheduled pass is never narrowed). Mode check clean
(repo-root `.env` → `MODE=active`; instance `config/config.yaml` →
`mode:` empty, falls through). Pre-pass `lib/eng-gate-check.sh`, whole-board:
exit 0, clean.

**Steps 2–4:** all three watched inboxes swept. `agents/product-manager/inbox/`
and `agents/eng-manager/inbox/` hold nothing but their own
`_handled`/`_processed` folders. `inbox/` holds 12 open items — every
`decision:` field and `## Decision` body read fresh and directly, not
assumed: all 12 blank/unfilled. Nothing to act on.

**Step 5 — merge detection**, all 7 tickets `blocked` on an L1 PR:
`git fetch origin` + `git merge-base --is-ancestor` in each of the three
worktrees (`aiorders-api`, `aiorders-admin-hub`, `restaurant-portal`).
`ENG-008`, `ENG-009`, `ENG-010`, `ENG-013`, `ENG-015` (both repos each) and
`ENG-032` all **not merged** — stay `blocked`. `ENG-022`
(`fix/ENG-022-brand-portal-tenant-isolation`, `aiorders-api`): **merged** —
cross-checked with `gh pr view 9` given the P0 severity (`state: MERGED`,
mergedAt `2026-09-04T02:03:48Z`, merge commit `78194da8` = `origin/main`'s
exact tip); no drift between the branch tip that passed every gate and the
merged tree. All three receipts re-read fresh (`pass` on review/quality/
security), no migration owed, fix independently re-verified on the merged
tree (all 19 call sites across 5 files). Carried `blocked → shipped →
verified` — release record `agents/devops/releases/2026-09-03-aiorders-api-ENG-022.md`,
merge-request item moved to `inbox/_handled/`, `decision-journal.md` row
added (seventh silent-GitHub-merge occurrence, first on a P0). Full
account: `ENG-022`'s own board-file log.

**Step 6 — dispatch.** Machine WIP re-verified fresh from every ticket's
own frontmatter, not the cached header: still `1/1`, the `ENG-016` family
(`ENG-016` `building`; `ENG-032` `blocked`/approver; `ENG-033`/`ENG-034`
`ready`, both still behind their own unmet `depends_on`). Nothing in the
family is dispatchable this pass — `ENG-032` waits on the approver,
`ENG-033`/`ENG-034` wait on `ENG-032` shipping. With the slot full, no
other ticket may enter `ready` regardless of priority. Checked every
`designed`-state ticket (12: `ENG-014`, `017`, `019`–`021`, `023`, `025`,
`026`, `029`, `030`, `035`, `036`) for an unraised G2 that dispatch
wouldn't otherwise catch — all 12 already resolved "no one-way door, no
G2" during their own design pass (grepped each for the determination
directly, not assumed), so all correctly sit parked on the WIP cap alone,
nothing further to raise. Zero transitions from dispatch itself this pass
(`ENG-022`'s transitions were step 5's, not step 6's).

**Step 6b:** not run — no build hop this pass, no new rule about an
artifact path/state name/config key written or relied on.

**Step 7 — notify sweep.** No new gate item raised this pass (ENG-022's
merge request was archived, not created). Nudge-eligibility checked for
every open, not-yet-nudged, non-incident item by cross-referencing each
item's own line in `traces/eng-notify-2026-09-03.log` against current local
time (21:49:49 PDT) rather than trusting the frontmatter `notified:` value
at face value — the standing, still-open proposal on this file's own
local-time-vs-UTC stamping inconsistency (`proposals.md`, 2026-09-02) means
the frontmatter alone isn't reliable, and the log line is unambiguous.
`ENG-015` (~18h46m), `ENG-027` rescope (~8h34m), `ENG-028` (~12h39m),
`ENG-032` (~22m) — all comfortably under 24h either way. `ENG-008`/
`ENG-009`/`ENG-010` already carry their one-time `nudged:`. The four P0
incident notices (`ENG-029`/`030`/`035`/`036`) left un-nudged, same
standing informational treatment. Nothing due.

**Step 8 — dead-end sweep, run in full** (the scheduled pass's own
mandate). Owner-blank check across every board file: none. `traces/.pending`:
6 queued `scheduled`/`watch` entries, all attempt 1 (never retried), no
`*-eng-events-dropped.md` file for today — a busy-day backlog under the
2026-09-02 priority rule (`continue`/`decision`/`finding`/`intake` always
drain ahead of `scheduled`/`watch`), not a stall; left to drain on
subsequent fires, nothing to remediate. `agents/qa/bugs/_index.md`:
`BUG-001` owned, not a dead end.

**Two real dead ends found and fixed, both by reading each ticket's own
artifacts rather than trusting its last log line:**

1. **`ENG-019`'s `continue` chain fired, ran, exited 0, and reported
   `chained: ENG-019` — but the architect's tech-design work never landed.**
   The pass had delegated it to a background subagent that got terminated
   at a 600s internal timeout before writing anything (`links.design`
   blank, no design file, confirmed via `git status` and a directory
   listing). A sibling `continue ENG-020` pass caught this by inspection
   hours earlier and explicitly left it for this sweep
   (`observations.md`); no later pass had picked it up. Re-fired
   `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-019`
   this pass (confirmed appended to `traces/.pending`, will drain ahead of
   the queued `scheduled`/`watch` backlog under the priority rule). Full
   trace: `ENG-019`'s own board-file log. Filed as a proposal
   (`proposals.md`, 2026-09-03) — a `continue` pass whose delegated
   subagent times out exits clean and looks healthy to every mechanical
   check this department runs, which is a real gap in the chain-health
   model, not just this one ticket's bad luck.
2. **`ENG-018`'s `priority: hold` — the approver's own field — had been
   silently changed to blank** by `2d66236` ("whole-board reconciliation,"
   2026-09-03T13:25:56-07:00), a large bundled commit whose message frames
   the touch as part of that evening's priority-*column* correction work,
   which was about fixing the table's stale cache from each ticket's file,
   never the reverse. Every other artifact (header prose ×2, the table,
   five days of other tickets' own cross-references) still treated it as
   held; nothing documents an actual approver instruction to un-hold it.
   Restored `priority: hold` on the ticket file — a data-integrity
   correction, not a fresh priority judgement (`eng_build_loop.md` step 6's
   "never write to priority yourself" governs setting a *new* value from
   inference). No ticket-state consequence — already excluded from dispatch
   either way. Full trace: `ENG-018`'s own board-file log; logged in
   `observations.md` as a first occurrence, not yet a pattern.

**In-flight table also corrected against fresh frontmatter while already
rewriting it this pass** (the standing "regenerate from each ticket's own
file, never hand-keep" fix, `observations.md` 2026-09-01/09-02/09-03):
`ENG-014` and `ENG-025` owner `architect → eng-manager` (both transitioned
2026-09-01, table never caught up), `ENG-027` priority blank `→ now`
(matching frontmatter, same gap already named for its siblings and missed
on this one row), `ENG-018`'s Updated column `→ 2026-09-03` (matching the
restored file's own stamp).

**Step 8b — observations/exceptions.** Four observations filed this pass
(two above, plus the ENG-019 chain-fix closing-the-loop entry and the
ENG-018 clobber) — see `observations.md`. One proposal filed (the
background-subagent-timeout chain-health gap) — see `proposals.md`. No
`exception-request:` found anywhere on the board (checked directly).

**Step 8c — journal.** `ENG-022`'s silent GitHub merge journaled in
`decision-journal.md` (see step 5 above). No G1/G2/G3 answered this pass.

**Step 9 — chain.** `ENG-022` reached `verified` (terminal, no chain).
`ENG-019` re-fired as this pass's broken-chain remediation (see step 8).
No other ticket was touched. `chained: ENG-019` recorded on this pass's
account; `chained: none` (terminal) on `ENG-022`'s own log.

**Board update:** this entry appended; rolled the oldest of the now-four
live dated entries (`continue ENG-032: security gate PASS, now
ready-to-ship`) to `_index-archive.md` per the keep-three rule. In-flight
table: `ENG-022` row removed (terminal), four cells corrected per the
paragraph above. "Waiting on the approver" header count `8 → 7`, `ENG-022`
paragraph removed and folded into the closing terminal-tickets note
alongside `ENG-024`/`ENG-031`.

Post-pass `lib/eng-gate-check.sh`, whole-board: exit 0, clean.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — watch: inbox sweep, no new work — ENG-032's PR still open

`watch` event pass, context `launchd`. The scheduler's file-watch fired on
`inbox/2026-09-03-eng032-merge-request.md` appearing in `inbox/` — written
directly by the prior `continue ENG-032` pass's release-runner hop, not
through the notify/decision-poll channel. Read the whole document (the
reading map's floor for `watch` is steps 2/3/4 plus step 5 since the
changed file is a merge-request item, plus the not-negotiable set — this
pass read past that floor rather than guessing at any rule it might have
skipped). Mode check clean (`MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-032`) and whole-board: both exit 0,
clean.

**Steps 2–4:** swept all three watched inboxes.
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold
nothing but their own `_handled`/`_processed` folders, untouched since
2026-09-01; `inbox/requests/` is empty. `inbox/` holds twelve open items —
checked each one's frontmatter `decision:` field and its `## Decision`
section body directly, not the field alone: every `decision:` is blank and
every `## Decision` section still reads its own unfilled boilerplate.
Nothing answered, nothing new to act on.

**Step 5 — merge detection**, since the changed file is ENG-032's own
merge request: `git fetch origin` in
`~/Documents/projects/_eng/restaurant-portal` (clean, no drift), then
`git merge-base --is-ancestor origin/feat/ENG-032-catering-portal-stages-and-itemized-view
origin/main` — **not an ancestor**. PR #2 still open, not merged. `ENG-032`
stays `blocked`/`approver`. No other ticket currently has an open inbox
item of its own that changed this pass, so no other ticket's merge status
was re-checked — that broader sweep is the `scheduled` pass's job, not
this event's.

**0 tickets transitioned.** Machine WIP unaffected — still 1/1 (`ENG-016`
family). Approver-facing WIP unaffected — still eight items, unchanged
composition.

**Dead-end sweep:** not run in full — outside a `watch` event's reading-map
floor (steps 2–5 plus the not-negotiable set), and this event's own
narrower contract is to sweep the three inboxes, not the whole board. The
one ticket this pass did touch, `ENG-032`, closes clean: its own last log
line (below) correctly carries `chained: none` with a reason. **Notify sweep:** every open `inbox/` item's
`notified:`/`nudged:` rechecked fresh against the 24h threshold (current
`2026-09-03T21:37:47-07:00` / `2026-09-04T04:37:47Z`) —
`ENG-008`/`ENG-009`/`ENG-010`/`ENG-022` already carry their one-time
`nudged:`; `ENG-015`/`ENG-027`/`ENG-028` all still under 24h (reading their
own local-time-mislabeled timestamps at face value against local now, same
standing convention prior passes on this board have used); the four P0
incident notices (`ENG-029`/`ENG-030`/`ENG-035`/`ENG-036`) left as-is, same
standing treatment; `ENG-032`'s own item was notified ~14 minutes before
this pass, nowhere near due. Nothing crossed, nothing raised this pass. **No
observations filed** — this pass confirmed steady state, found nothing
novel. **Step 6b:** not run — no artifact rule written or relied on this
hop. **Journal:** n/a — no G1/G2/G3 or merge request answered this pass.

**Board update:** this entry appended; rolled the oldest of the four
now-live dated entries (`continue ENG-032: round 2 — review PASS, quality
gate PASS, in-qa`) to `_index-archive.md` per the keep-three rule. No
In-flight table changes — no ticket's state moved.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-032`) and whole-board: both
exit 0, clean.

`chained: none` — **waiting on the approver**, unchanged (`ENG-032`
remains `blocked`, `blocked_on: approver`; no other ticket touched this
pass). Full reasoning: `ENG-032`'s own board-file log.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

---

## 2026-09-03 — continue ENG-032: release-readiness PASS, PR opened, now `blocked`

`continue` event pass, context `ENG-032`, per the security-gate pass's own
`chained: ENG-032`. Narrow scope per the event's own contract — this ticket
only. Reading map for `continue`: steps 6 and 6b, plus the not-negotiable
set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*).
Mode check clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped
(`ENG-032`) and whole-board: both exit 0, clean.

Ran `skills/release-runner/SKILL.md`. `restaurant-portal` is **L1** — step
1's window check skipped entirely (opening a PR is not a release). Step 2:
verified all three upstream gates by reading each receipt directly
(`agents/principal-engineer/reviews/ENG-032.md`,
`agents/qa/test-plans/ENG-032.md`, `agents/security/reviews/ENG-032.md`,
all `pass`); no migration file, correctly — no schema touched.

**Step 3, readiness gate: PASS.** Rollback — no migration, so a plain
revert of the three-commit branch is complete on its own; newly found this
hop, `.github/workflows/deploy-cf.yml` now exists on `main`
(push-triggered), which didn't exist as of `ENG-002`'s own release
(2026-08-26) — a revert re-triggers it and redeploys the prior build
automatically. Observability — the one named throw risk is mutation-tested
pre-merge (QA's AC-8); no client-side error tracking exists anywhere in
this repo (`grep`, zero hits), a pre-existing gap this ticket doesn't
worsen, same posture `ENG-002` already passed on. Cost — $0/month,
independently confirmed (no lockfile in the diff, no new service). Window
criterion n/a (L1).

**Step 4: opened the PR** —
`https://github.com/harsimranwalia/restaurant-portal/pull/2` — and wrote
the merge request (`inbox/2026-09-03-eng032-merge-request.md`) in the same
step, from the department's own worktree. Notified immediately
(`lib/eng-notify.sh raise`, confirmed sent in today's notify log).

**State: `ready-to-ship → blocked`, `owner: devops → approver`,
`blocked_on: approver`, `blocked_from: ready-to-ship`. 1 transition**, under
the cap of 4. `links.pr` set. Machine WIP unaffected — still 1/1, held by
the `ENG-016` family via `ENG-016` itself (still `building`). Approver-facing
WIP: `wip.approver_limit: unlimited` — verified directly against
`config/config.yaml` this hop, not taken from this file's own narrative;
this item joins the visibility-only list, gating nothing.

**Dead-end sweep (scoped to this event):** no other ticket touched;
spot-checked the other six `blocked_on: approver` tickets and two
`awaiting-scope` tickets fresh off their own frontmatter while confirming
the WIP framing — all already consistent. **Notify sweep:** every open
`inbox/` item checked fresh against the 24h threshold — nothing newly
crosses it; this pass's own new item just notified. **Observation filed**
(`observations.md`): the newly-discovered `deploy-cf.yml` workflow, and
what it changes for the next release-readiness hop on this repo. **Step
6b:** not run — follows the already-established `blocked`/
`blocked_on: approver`/`pr_url` pattern exactly. **Journal:** n/a — a gate
was raised this pass, not answered.

**Board update:** this entry, appended; rolled the oldest of the four
now-live dated entries (`continue ENG-032: round 2 — review PASS...`) to
`_index-archive.md` per the keep-three rule. In-flight table row for
`ENG-032` updated (`ready-to-ship`/`devops` → `blocked`/`approver`).
Approver-facing-WIP header count and list updated (seven → eight items);
`ENG-032`'s own paragraph added under "Waiting on the approver."

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-032`) and whole-board: both
exit 0, clean.

`chained: none` — **waiting on the approver** (`blocked`,
`blocked_on: approver`; PR #2 open, merge request raised). Per
`eng_build_loop.md` step 9, a ticket waiting on the approver is never
chained. Full reasoning: `ENG-032`'s own board-file log.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

---

## 2026-09-03 — continue ENG-032: security gate PASS, now `ready-to-ship`

`continue` event pass, context `ENG-032`, per round 2's own `chained:
ENG-032`. Narrow scope per the event's own contract — this ticket only.
Reading map for `continue`: steps 6 and 6b, plus the not-negotiable set (1,
7, 8b, 9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*); not
mid-PRD, so step 2's checkpoint note doesn't apply. Mode check clean
(`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-032`): exit
0, clean.

Ran the security gate (`skills/security-gate/SKILL.md`). Threat-modeled the
diff (4 questions), walked OWASP A01–A10, LLM checklist n/a (no model/
agent/tool touched), secret scan clean over the diff and the full 3-commit
branch history, no new/bumped dependency. Independently re-verified rather
than taken on the design's or QA's account: grepped the whole diff for
`supabase.from(` — zero hits, confirming the itemized-selections block
renders an already-fetched prop and adds no new query; read
`aiorders-api`'s `brand-portal/catering.ts` directly on `origin/main` and
confirmed `get_catering_requests`/`create_catering_request`/
`update_catering_request` all call `verifyRestaurantAccess` before
touching a row, correctly ordered. Checked the new
`(acc[selection.category] ||= []).push(...)` grouping pattern for
prototype pollution — not exploitable, `||=`'s short-circuit on a plain
object's always-truthy inherited `__proto__`/`constructor` means the
assignment branch never fires for those keys.

**Verdict: PASS.** Zero blocking findings. Receipt:
`agents/security/reviews/ENG-032.md`; `links.security_review` set on the
ticket in the same edit.

**One non-blocking finding, routed out rather than held against this
ticket.** Verifying QA's stated reason for skipping a new negative-authz
test ("`ENG-022`'s own suite already covers `brand-portal`'s access-check
call sites generally") found it overstated: `ENG-022`'s 19 tests cover 5 of
`brand-portal`'s 10 handler files, and `catering.ts` — the file this
ticket's rendered data flows through — isn't one of them, though its own
access checks read correctly. Doesn't change `ENG-032`'s own verdict (no
authz-relevant code in this diff either way), but the gap is real and now
matters more than before this ticket (the data it guards reaches the owner's
screen for the first time). Filed as a proposal
(`agents/eng-manager/proposals.md`, 2026-09-03, security, `aiorders-api`)
per `eng_build_loop.md` step 3, and logged in
`agents/security/notebook/2026-09-03-findings.md`.

**State: `in-qa → in-security → ready-to-ship`, `owner: qa → devops`. 2
transitions**, under the cap of 4. Machine WIP unaffected — still `1/1`
(`ENG-016` family; `ENG-032` remains the active member, now at
`ready-to-ship`). No approver-facing or approval-cap change —
`ready-to-ship` needs no approver gate on its own; devops's
release-readiness hop is next.

**Dead-end sweep:** not run — outside a `continue` event's reading map
(steps 6/6b plus the not-negotiable set), and this pass's own chain landing
here confirms `ENG-032`'s own chain is intact. **Notify sweep:** every open
`inbox/` item checked fresh against the 24h threshold (current local
~21:19 PDT / `2026-09-04T04:19:02Z`) — `ENG-015`/`027`/`028` all still
under 24h since their own `notified:` (reading local-time-mislabeled
timestamps at face value against local now, per the standing, still-open
proposal on this exact bug); `ENG-008`/`009`/`010`/`022` already carry
their one-time `nudged:`; the four P0 incident notices left un-nudged, same
standing treatment this board's prior passes have used. Nothing newly
crossed the threshold — no gate item raised this pass either (a machine
gate, not an approver decision). **Step 6b:** not run — this hop writes no
new rule about an artifact path, state name, or config key. **Journal:**
n/a — no G1/G2/G3 or merge request answered this pass.

**Board update:** this entry, appended; rolled the oldest of the four
now-live dated entries (`continue ENG-036`) to `_index-archive.md` per the
keep-three rule. In-flight table row for `ENG-032` updated
(`in-qa`/`qa` → `ready-to-ship`/`devops`).

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-032`) and whole-board: both
exit 0, clean.

`chained: ENG-032` — `ready-to-ship` is agent-owned (devops next,
release-readiness), not the approver, not blocked, not terminal, not held
by a cap. Not combined with this hop — security and release-readiness
aren't named as a combinable pair anywhere in `eng_build_loop.md`, unlike
review+quality, and each heavy gate gets its own fresh-context session by
design (`eng_build_loop.md`, "The chain"). Fired `/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-032` before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

---

## 2026-09-03 — continue ENG-032: round 2 — review PASS, quality gate PASS, `in-qa`

`continue` event pass, context `ENG-032`, per round 1's fix hop's own
`chained: ENG-032`. Narrow scope per the event's own contract — this
ticket only. Reading map for `continue`: steps 6 and 6b, plus the
not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four
lanes*, *Guards*). Mode check clean (`MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-032`): exit 0, clean.

Ran the combined review + quality hop (`eng_build_loop.md` step 6).
Worktree confirmed on
`feat/ENG-032-catering-portal-stages-and-itemized-view@7950a93`, clean, no
drift after `git fetch origin main`; `git diff ab3fa4e..7950a93 --stat`
confirmed the only change since round 1's reviewed commit is the new
`CateringPageForm.test.tsx` — every other file round 1 already reviewed
line-by-line is byte-identical, so this round re-verified the delta rather
than re-deriving unchanged conclusions.

**Review: PASS, round 2.** 0/10 automatic failures — round 1's sole
finding (missing regression test) closed. Independently re-verified rather
than trusted: swapped the pre-fix `CateringPageForm.tsx` back in and
re-ran the new test — failed with `expected undefined to be true` on
`saved.orderFormEnabled`, the exact defect the fix addresses; restored,
re-ran green. Also independently re-derived the lint baseline (96
problems, 0 new) by a different method than either prior hop used —
temporarily swapped `CateringDetailModal.tsx`'s content back to
`origin/main` and re-linted in place: the one real lint error in any
touched file (`react-hooks/rules-of-hooks`) is present on `origin/main`
too, confirming pre-existing. Full detail:
`agents/principal-engineer/reviews/ENG-032.md`.

**Quality gate: PASS.** The design assigned AC-8's UI slice and AC-12
(narrowed — "fulfillment option and guest count... need no work") to QA's
plan rather than the build hop; neither `CateringKanban.tsx` nor
`CateringDetailModal.tsx` had a test file before this pass. Wrote both —
`CateringKanban.test.tsx` (a pre-existing-stage request renders unchanged
alongside both new stages) and `CateringDetailModal.test.tsx` (itemized
selections render grouped by category; the block stays absent with no
selections) — and mutation-verified each against the exact risk it
targets: removing one `statusConfig` entry reproduced the design's own
named risk verbatim (`Cannot read properties of undefined (reading
'borderColor')`); forcing the itemized block to always render broke the
omit-block test with `Cannot read properties of null (reading 'reduce')`.
Both reverted after. No open P0/P1 (`agents/qa/bugs/_index.md`: one open
item, `BUG-001`, P2, unrelated project). Full detail:
`agents/qa/test-plans/ENG-032.md`.

New test files committed and pushed: `restaurant-portal@77631b0`
(`feat/ENG-032-catering-portal-stages-and-itemized-view`). Both receipts
written: `agents/principal-engineer/reviews/ENG-032.md`,
`agents/qa/test-plans/ENG-032.md`. `links.review`/`links.test_plan` set on
the ticket in the same edit as the state change.

**State: `building → in-review → in-qa`, `owner: frontend → qa`. 2
transitions**, under the cap of 4. Machine WIP unaffected — still `1/1`
(`ENG-016` family; `ENG-032` remains the active member). No
approver-facing or approval-cap change — `in-qa` needs no approver gate.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** every open `inbox/` item checked fresh against the 24h
threshold — nothing newly crosses it; `in-qa` itself raises nothing.
**3 observations filed** (`observations.md`): the brand-level
catering-content precedence override, named directly by ADR-009 and the
design as "worth a line in QA's test plan and worth an observation"; both
new components turning out cheaper to test than expected (props-driven, no
context needed); round-1's test-coverage-gap observation now partly
closed. **Step 6b:** not run — a review+quality hop, not a build hop.
**Journal:** not applicable — no G1/G2/G3 or merge request answered this
pass.

**Board update:** this entry, appended; rolled the oldest of the four
now-live dated entries (`continue ENG-032: code review round 1 FAILS...`)
to `_index-archive.md` per the keep-three rule. In-flight table row for
`ENG-032` updated (`building`/`frontend` → `in-qa`/`qa`).

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-032`) and whole-board: see
below.

`chained: ENG-032` — `in-qa` is agent-owned (security next), not the
approver, not blocked, not terminal, not held by a cap. Fired `/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-032` before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-032: round-1 fix — regression test added, still `building`

`continue` event pass, context `ENG-032`, per round 1's own `chained:
ENG-032`. Narrow scope per the event's own contract — this ticket only.
Reading map for `continue`: steps 6 and 6b, plus the not-negotiable set (1,
7, 8b, 9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*). Mode
check clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`: exit 0,
clean. Worktree confirmed on
`feat/ENG-032-catering-portal-stages-and-itemized-view@ab3fa4e`, clean, no
drift after `git fetch origin main`.

Built round 1's own fix shape: added
`restaurant-portal/src/components/website/CateringPageForm.test.tsx`
(render with `orderFormEnabled`/`fulfillmentCopy` populated, submit
untouched, assert `onSave` receives both intact). Verified the test is
meaningful, not just green: temporarily removed the `...content` spread
that is the actual fix, confirmed the assertion failed (`orderFormEnabled`
came back `undefined`), restored it, confirmed green again — `git diff`
on the source file was empty afterward. Full suite: lint 96 pre-existing
problems / 0 new (round 1's own logged "63" turned out stale — see
below), build clean, test 2/2. Two non-blocking notes from round 1 left
unaddressed, deliberately — neither was in round 1's own "fix shape"
paragraph, and touching the flagged kanban whitespace would manufacture
the "unrelated refactor" pattern the review was careful to rule out.
Committed and pushed: `restaurant-portal@7950a93`, same branch.

**A prior hop's self-tested claim didn't hold up, checked rather than
inherited.** The `ready → building` hop recorded "63 pre-existing lint
problems, confirmed zero new." This hop's own `npm run lint` on the
unmodified branch tip showed 96. Isolated the cause before writing either
number down: the new test file alone lints clean; removing it and
re-running against the untouched branch still shows 96; a throwaway
detached worktree at `origin/main` (symlinked `node_modules`, removed
after) also shows 96. `ENG-032`'s own commit touches no lint config, no
`package.json`, no lockfile. So 96 is the real current baseline and this
ticket has always introduced zero new problems — same conclusion, stale
number, most likely an eslint/plugin or cache difference between the two
runs rather than a regression on any ticket. Not chased further.

**0 net transitions** — `state`/`owner` unchanged (`building`/`frontend`);
this hop is the frontend fix round 1 asked for, not the review itself
("a pass stops after `building` on purpose" — a fresh session reviews it
next). Machine WIP unaffected, still 1/1 (`ENG-016` family, re-checked
fresh off all in-flight tickets' own frontmatter). No approver-facing or
approval-cap change.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** every open `inbox/` item checked fresh against the 24h
threshold — nothing newly crosses it beyond what already carries its
one-time `nudged:`; the four P0 incident notices left un-nudged, same
standing treatment. **Two observations filed** (`observations.md`): the
lint-baseline discrepancy above, and the per-component test convention
this hop establishes (colocated `ComponentName.test.tsx`, `fireEvent` over
the uninstalled `user-event`, assert on the mock callback's payload) for
whichever ticket writes this repo's third test file. **Step 6b:** not
run — the test file is product code, not a business-os process artifact.
**Journal:** not applicable — no gate answered this pass. Full reasoning:
`agents/frontend/notebook/2026-09-03-eng032-catering-stages-and-order-form-editor.md`.

**Board update:** this entry, appended; rolled the oldest of the four
now-live dated entries (`continue ENG-035`) to `_index-archive.md` per the
keep-three rule. In-flight table row for `ENG-032` unchanged
(`building`/`frontend`, no state or owner change to record).

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-032`) and whole-board: see
below.

`chained: ENG-032` — `building` still agent-owned (review round 2 next,
principal-engineer), not the approver, not blocked, not terminal, not held
by a cap. Fired `/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-032` before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-036: `shaped → designed`, service-role-bearer gate reused, three real callers confirmed

`continue` event pass, context `ENG-036`, its own turn per the prior
`continue ENG-035` pass's own second, separate `chained: ENG-036`. Narrow
scope per the event's own contract — this ticket only. Reading map for
`continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10;
*Enforced vs instructed*, *The four lanes*, *Guards*); not mid-PRD, so step
2's checkpoint note doesn't apply. Mode check clean (repo-root `.env` →
`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, whole-board and scoped
(`ENG-036`): both exit 0, clean.

**Design work — full reasoning in
`agents/architect/designs/ENG-036-outgoing-communications-systemtriggered-auth-bypass.md`
and `ADR-017`.** Read `index.ts` via `git show origin/main:` (worktree still
on `feat/ENG-031-...`, same read-only-against-remote approach `ENG-035`'s
own design pass used) — confirmed the whole auth block sits behind one
`if (!systemTriggered)` with no `else`. Grepped `outgoing-communications`
across all five registered repos at each one's own remote default branch,
not `aiorders-api` alone — the PRD's own named risk, since it had verified
only one caller. Found two more: `aiorders-admin-hub`'s
`cloudflare-workers/queue-consumer/index.ts` (a third legitimate
`systemTriggered: true` caller, confirmed sending
`Authorization: Bearer ${env.SUPABASE_SERVICE_ROLE_KEY}`) and three
non-`systemTriggered` callers across `aiorders-admin-hub` and
`restaurant-portal` that forward or use an ambient user session and stay on
the untouched branch either way. All three real `systemTriggered: true`
callers already send `ADR-016`'s exact header — stronger evidence than
`ENG-035` had (an HTTP call site read in full beats an untracked DB
trigger).

Designed `outgoing-communications/auth.ts` (new,
`authorizeSystemTrigger(req, responseHeaders)`, `ADR-016`'s own signature),
called from the missing `else` on the existing `if (!systemTriggered)`
block — one call site, ahead of the `actor` switch. `ADR-017` records two
decisions: reuse `ADR-016`'s mechanism (three live callers across two repos
would need coordinated reconfiguration this session can't make or verify,
against one header all three already send correctly), and keep it as its
own file rather than extracting to `_shared/` now (`ADR-016`'s own file
isn't built yet either — `ENG-035` still `designed` — so sharing now would
couple this ticket's build to `ENG-035`'s branch for a ~20-line,
zero-behavior-cost duplicate). One-way doors: none, decided here rather
than escalated. Filed as an observation (`observations.md`), not a
proposal.

**State:** `shaped → designed`, `owner: architect` unchanged. **1
transition**, under the cap of 4. **Routing: would be `ready` — held at
`designed`.** Machine WIP re-checked fresh off `ENG-016`/`032`/`033`/`034`'s
own frontmatter: `ENG-016`/`ENG-032` `building`, `ENG-033`/`ENG-034`
`ready` — still `1/1`, none `shipped`. No approver-facing or approval-cap
change — G1 already auto-skipped at intake, and no one-way door means no G2
either (`definition-of-done.md`).

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** every open `inbox/` item checked fresh against the 24h
threshold (current `2026-09-04T03:29:11Z`) — `ENG-015`/`027`/`028` all
still under 24h since their own `notified:`; `ENG-008`/`009`/`010`/`022`
already carry their one-time `nudged:`; the four P0 incident notices
(`029`/`030`/`035`/`036`) left un-nudged per the standing, still-open
question flagged in `observations.md`'s 2026-09-03 row on `ENG-031` — not
re-litigated here. Nothing newly crossed the threshold. **Step 6b:** not
run — a design hop, not a build hop; no product code written this pass.
**Journal:** not applicable — no G1/G2/G3 answered this pass.

**Board update:** this entry; In-flight row for `ENG-036` (`shaped →
designed`).

Post-pass `lib/eng-gate-check.sh`, whole-board and scoped `ENG-036`: see
below.

`chained: none` — `ENG-036` sits at `designed`, owned by `architect`, not
the approver, not blocked, not terminal, but held by the machine-WIP cap
(`1/1`, the `ENG-016` family); re-check once that family reaches `shipped`.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-032: code review round 1 FAILS on a missing regression test

`continue` event pass, context `ENG-032`, its own turn per the prior
`continue ENG-032` (build) pass's own `chained: ENG-032`. Narrow scope per
the event's own contract — this ticket only. Reading map for `continue`:
steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
instructed*, *The four lanes*, *Guards*). Mode check clean (`MODE=active`).
Pre-pass `lib/eng-gate-check.sh`: exit 0, clean.

Ran the combined review + quality hop (`eng_build_loop.md` step 6):
worktree confirmed on `feat/ENG-032-catering-portal-stages-and-itemized-view@ab3fa4e`,
clean, matching frontmatter; diff reviewed in full (11 files, 207
insertions / 6 deletions). Automatic-failure scan hit #3 — the
`CateringPageForm.tsx` save-path fix (the one closing ADR-009's
silent-revert risk) ships with no test, and `restaurant-portal` already has
`@testing-library/react`/`jsdom`/`vitest` installed (`ENG-002`) with
nothing blocking a first component test from being written. Fix verified
correct by tracing the full path (`useEffect` → `handleSubmit` → the
`pages/website/Index.tsx` call site) before flagging only the missing
evidence, not the fix itself. Two non-blocking notes (trailing whitespace,
an array-index key) logged but not the reason this round fails. Full
findings: `agents/principal-engineer/notebook/2026-09-03-review-log.md`.

**Verdict: FAIL, round 1.** No receipt written; QA's hop not run this
round, discarded per the combined-hop design. **0 net transitions** —
`state`/`owner` unchanged (`building`/`frontend`), same precedent
`ENG-008`/`ENG-013`/`ENG-015`'s own round-1 entries set. Machine WIP
unaffected, still 1/1 (`ENG-016` family). No approver-facing or
approval-cap change — a review failure is not an approver-facing gate.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** every open inbox item checked fresh against the 24h
threshold (current `2026-09-04T03:09:49Z`) — nothing crossed, nothing
raised; a review failure routes back to `building`, not to the approver.
**Observations filed:** `restaurant-portal` has component-test tooling
installed but no example test file yet — see `observations.md`. **Step
6b:** not run — a review hop, not a build hop. **Journal:** not applicable
— no gate answered this pass.

**Board update:** this entry, appended. In-flight table row for `ENG-032`
unchanged (`building`/`frontend`, no state or owner change to record).
File held exactly three dated entries after this pass's own edits — no
roll needed beyond the one already performed removing the oldest
(`scheduled: whole-board sweep...`) to make room for this entry.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-032`) and whole-board: see
below.

`chained: ENG-032` — `building` is agent-owned (round 1's finding is the
next hop's own work: add the missing regression test), not the approver,
not blocked, not terminal, not held by a cap. Fired `/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-032` before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

---

## 2026-09-03 — continue ENG-035: `shaped → designed`, service-role-bearer gate designed, ENG-036 byproduct found and filed

`continue` event pass, context `ENG-035`, its own turn per the recovery
sweep's own re-fired `chained: ENG-035`. Narrow scope per the event's own
contract — this ticket only, plus the one byproduct P0 it surfaced. Reading
map for `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b,
9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*); not mid-PRD,
so step 2's checkpoint note doesn't apply. Mode check clean (repo-root
`.env` → `MODE=active`). Pre-pass `lib/eng-gate-check.sh`, whole-board and
scoped (`ENG-035`): both exit 0, clean.

**Design work — full reasoning on the ticket's own board file and in
`agents/architect/designs/ENG-035-autopilot-systemtriggered-auth-bypass.md`.**
Read `index.ts` and every `marketing/*.ts` file via `git show origin/main:`
(the shared `_eng/aiorders-api` worktree was on a stale, already-shipped
feature branch, not `main` — read-only against the remote ref rather than
disturbing it, same approach `ENG-029`'s own design pass used). Confirmed
the PRD's own risk — the real DB-trigger invocation path is untracked in
this repo — then found the closest available evidence anyway: two general
trigger-to-edge-function conventions in this project's own migration
history, one row-level and header-carrying
(`20260807000004_fix_restaurant_website_cache_invalidation_trigger.sql`),
one scheduled and headerless
(`20260217000001_platform_analytics_cron.sql`). `welcome_offer`'s own
trigger matches the row-level, header-carrying shape. Designed a new
`marketing/auth.ts` gate requiring `Authorization: Bearer
${SUPABASE_SERVICE_ROLE_KEY}` on that reasoning (`ADR-016`, `_index.md`
`next_id → ADR-017`) — reversible, no one-way door, `touches_data`/
`touches_models` both `false`. The named residual risk (the live trigger's
actual headers are still unverifiable without DB/CLI/MCP access, and this
exact "new header check silently rejects a legitimate trigger" failure has
already happened once in this codebase) is mitigated with a distinct denial
log line and a mandatory manual post-deploy verification step in the
design's own Rollout section, not left as a bare statement.

**Byproduct P0 found and filed: `ENG-036`.** Reading `outgoing-communications/index.ts`
(required to understand `marketing/utils.ts`'s own legitimate call pattern)
found the identical `systemTriggered`-trusts-the-body bug, wider in surface
— it gates the function's entire auth requirement, for every actor, not one
branch. Confirmed live via all four `actors/*.ts` handlers read in full.
Filed per step 3's P0 carve-out, same shape as `ENG-029` → `ENG-035`: PRD
(`agents/product-manager/specs/ENG-036-outgoing-communications-systemtriggered-auth-bypass.md`),
board ticket (`intake → shaped`, owner `architect`), incident notice
(`inbox/2026-09-03-eng036-p0-incident.md`, `lib/eng-notify.sh raise` exit 0,
`notified: 2026-09-04T02:52:24` stamped by hand). Does not consume
approver-facing WIP (`security`-typed, G1 auto-skip, informational
incident) or machine WIP (`shaped` sits outside the counted range).

**Routing: `ENG-035` would be `ready` — held at `designed`.** Machine WIP
re-checked fresh from every ticket's own frontmatter, not this header:
`ENG-016`/`ENG-032` `building`, `ENG-033`/`ENG-034` `ready` — still `1/1`,
none `shipped`. Same precedent this board has applied all day: held at
`designed`, owner staying `architect`.

**Dead-end sweep (scoped to this event):** no other ticket touched beyond
the `ENG-036` byproduct above. **Notify sweep:** `ENG-036`'s incident raised
and stamped above; swept every open `inbox/` item's `notified:`/`nudged:`
against the 24h threshold (`date -u` ~`2026-09-04T02:52`) — nothing newly
crosses it since the immediately preceding pass's own check. **Two
observations filed** (`observations.md`): the "byproduct found designing the
previous byproduct's fix" pattern, now three of four gaps this week; and
`platform-analytics-hourly`'s own headerless cron call, noticed tangentially
and not chased (not clearly P0 on this pass's own limited read). **Journal:**
not applicable — no G1/G2/G3 answered this pass.

**Board update** — this entry; In-flight row for `ENG-035` (`shaped →
designed`), new row added for `ENG-036`; `Next ID` corrected `ENG-036 →
ENG-037`. Rolled the oldest of the four now-live dated entries (`continue
ENG-031: ready-to-ship → blocked`) to `_index-archive.md` per the
keep-three rule.

Post-pass `lib/eng-gate-check.sh`, whole-board and scoped `ENG-035`/`ENG-036`:
see below.

`chained: none` — `ENG-035` sits at `designed`, owned by `architect`, not
the approver, not blocked, not terminal, but held by the machine-WIP cap
(`1/1`, the `ENG-016` family); re-check once that family reaches `shipped`.
`chained: ENG-036` — `shaped`, owned by `architect`, an agent-owned state,
not held by any cap; fired `/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-036` before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-032: `ready → building`, catering stages/itemized view/order-form switch built

`continue` event pass, context `ENG-032`, its own turn per the prior pass's
own `chained: ENG-032`. Narrow scope per the event's own contract — this
ticket only. Reading map for `continue`: steps 6 and 6b, plus the
not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four
lanes*, *Guards*). Mode check clean (`MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-032`): exit 0, clean.

WIP re-checked fresh off all 33 board files' own frontmatter: still 1/1,
held by the `ENG-016` family — this transition swaps which member is
active (`ENG-032` now the one in `building`), not the count.

Fixed a stray worktree-branch slip before building (`restaurant-portal`
was on the parent ticket's slug, `feat/ENG-016-catering-quote-generator`,
0 commits — the same pattern `ENG-031`'s own log already caught once on
`aiorders-api`; `git branch -m`, lossless). Built all 11 `restaurant-portal`
rows of the design's `## Components` table: the two new stages appended
after `New Enquiry` across every hardcoded copy (kanban, three modals,
calendar, request card, table view, staff form, CSS), the itemized-
selections block in the owner's detail modal (AC-12), and the
`orderFormEnabled` switch plus per-option `fulfillmentCopy` editor in the
Website → Catering page (ADR-008, ADR-009) — including the save-path fix
that stops the editor from silently reverting the switch on an unrelated
save. `Dashboard.tsx` confirmed untouched, matching the design's explicit
non-goal. Self-tested: lint (0 new problems, confirmed via `git stash`
diff), build clean, existing smoke suite still 1/1. No new automated test
written — QA's plan owns `restaurant-portal` coverage for this ticket per
the design's own Risks section; full reasoning in the ticket's own log and
`agents/frontend/notebook/2026-09-03-eng032-catering-stages-and-order-form-editor.md`
(first entry in that notebook).

Committed and pushed (`restaurant-portal@ab3fa4e`,
`feat/ENG-032-catering-portal-stages-and-itemized-view`); no PR opened yet
— devops's own release-readiness hop, same precedent this board already
set repeatedly. **1 transition** (`ready → building`), under the cap of 4.
Machine WIP unaffected. No gate touched this hop.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** every open inbox item checked fresh against the 24h
threshold (current `2026-09-04T02:31:02Z`) — nothing crossed, nothing
raised. **Observations filed:** the branch-slug slip is now a confirmed
second occurrence (`aiorders-api` then `restaurant-portal`) — see
`observations.md`. **Step 6b:** not run — the new status strings and jsonb
config keys are product data, not business-os process artifacts (same
reasoning `ENG-024`'s `show_in_marketplace` hop set). **Journal:** not
applicable — no gate answered this pass.

**Board update:** this entry; In-flight row for `ENG-032`
(`ready → building`, owner → `frontend`); header paragraph's stale "still
`ready`" references corrected. Rolled the oldest of the four now-live
dated entries (`continue ENG-031: in-qa → ready-to-ship`) to
`_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-032`) and whole-board:
exit 0, clean.

`chained: ENG-032` — `building` is agent-owned (next hop `in-review`); not
the approver, not blocked, not terminal, not held by a cap. Fired
`/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-032` before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — scheduled: whole-board sweep, two silent GitHub merges found and shipped, ENG-035's broken chain recovered

`scheduled` event pass (02:00, context `auto-drain`) — the safety-net sweep,
read in full per its own reading-map entry ("never narrowed"). Mode check
clean (repo-root `.env` → `MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Step 2/3 (business/technical intake):** `agents/product-manager/inbox/`
and `inbox/requests/` both empty but for `.gitkeep`; `agents/eng-manager/inbox/`
empty, `_processed/` already settled. Nothing to shape or propose.

**Step 4 (gate returns):** every open item in `inbox/` checked fresh —
`ENG-008`/`009`/`010`/`015`/`022`/`027`/`028` all still carry a blank
`decision:`, unchanged since the immediately preceding pass. The three P0
incident notices (`ENG-029`/`030`/`035`, `agent: architect`, informational —
not one of `lib/eng-trigger.sh`'s own four self-raised incident types, so
step 4's "move to `_handled/`" clause doesn't apply to these) are all still
under the 24h nudge threshold (11h21m, 10h34m, 9h01m old respectively at
check time, current UTC 01:58:14) — the prior pass's own open question
(whether an FYI-only incident should ever be nudged) stays moot for another
cycle, not re-litigated here.

**Step 5 (merge detection) — the sweep's own reason to exist.** Local git
only, no `gh` call, for every ticket `blocked` on an L1 PR: `aiorders-api`
(`git fetch origin main` → `origin/main@3cf5607`) and `aiorders-admin-hub`
(→ `origin/main@93617c6`), then fetched each open PR's head
(`refs/pull/N/head`) and ran `git merge-base --is-ancestor` against each
repo's `origin/main`. Results: `aiorders-api` PR #11 (`ENG-024`) and PR #12
(`ENG-031`) **merged**; PRs #5–#10 on `aiorders-api` and #4–#8 on
`aiorders-admin-hub` (`ENG-008`/`009`/`010`/`013`/`015`/`022`) **not
merged** — all eight stay `blocked`, unchanged.

**Step 6 (dispatch), two tickets carried to terminal, one dispatched:**
- `ENG-024` and `ENG-031`: both `blocked → shipped → verified` this pass —
  pure receipt-confirmation (all upstream gate receipts re-read directly,
  not trusted from frontmatter) plus a release record each
  (`agents/devops/releases/2026-09-03-aiorders-api-ENG-024.md`,
  `...-ENG-031.md`), no new implementation work. Merge-request items moved
  to `inbox/_handled/`; `decision-journal.md` rows added (silent GitHub
  merge, no written reply — sixth and seventh such occurrence on this
  board). Full detail on each ticket's own board file.
- `ENG-031`'s shipping satisfies `ENG-032`'s sole `depends_on`. Confirmed
  `ENG-032` is the only newly-dispatchable ticket — `ENG-033`/`ENG-034`
  remain behind their own unmet dependency on `ENG-032` itself, so there
  was no ordering choice to make. **Not built in this pass** — same
  precedent `ENG-024`'s and `ENG-022`'s own dispatch hops already set (a
  whole-board sweep does not perform new implementation work); chained
  instead so a dedicated session does the `ready → building` hop.

**Step 8 (dead-end sweep) — a genuine broken chain, not just a stale
reading.** Cross-checked every ticket's last `chained:` line against
today's traces, per step 8's "a chain that was fired is not the same as a
chain that ran." `ENG-035` (P0, `shaped`, owner `architect`) logged
`chained: ENG-035` at creation (~16:56) but: no
`traces/.hops-2026-09-03-ENG-035` file exists (every other ticket touched
today has one), no `continue ENG-035` line anywhere in `traces/.pending`,
and no `*-eng-events-dropped.md` file names a dropped fire for it — a lost
fire, ~9h with nothing resumed. Compounding it, the ticket had no In-flight
row and the `Next ID` counter was never bumped past it — a gap
`observations.md` had already flagged twice (2026-09-02 `ENG-026`,
2026-09-03 `ENG-035` itself) as out-of-scope for the narrow `continue`
events that found it. **Fixed in this pass:** In-flight row added,
`Next ID → ENG-036`, and `continue ENG-035` re-fired. Third occurrence of
the board-index-omission gap promoted from observation to proposal (below)
— a mechanical `lib/eng-gate-check.sh` check is cheaper than a fourth pass
re-noticing it by hand.

**Step 8b (observations/proposals):** one proposal filed
(`proposals.md`) — extend `lib/eng-gate-check.sh` to verify every
`agents/eng-manager/board/ENG-*.md` has a matching In-flight row (or a
terminal mention) and that `Next ID` exceeds every allocated id.

**Step 8c (journal):** two rows added for `ENG-024`'s and `ENG-031`'s
silent merges (above).

**Consequences:** approver-facing "Waiting on the approver" count
`nine → seven` (`ENG-024`/`ENG-031` both fully resolved, not just
answered). Machine WIP unaffected — `ENG-024`/`ENG-031` were already
outside the counted `ready..ready-to-ship` range; the `ENG-016` family's
slot continues uninterrupted, now represented by `ENG-032` (about to move
to `building`) instead of `ENG-031`.

**Chain:** two separate fires, one per ticket left in an agent-owned state
this pass (same precedent `ENG-029`'s/`ENG-035`'s own creation pass set for
firing more than one chain in a single sweep):
`chained: ENG-032` and `chained: ENG-035` — both fired via
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue {TICKET-ID}` before this pass exits. `ENG-024` and `ENG-031`
themselves are terminal — `chained: none` for both, no reason needed beyond
that.

**Board update:** this entry; In-flight table rows removed for `ENG-024`/
`ENG-031` (terminal), added for `ENG-035`; header, "Waiting on the
approver," and the terminal-tickets closing paragraph all updated in the
same edit. Rolled the oldest of the four now-live dated entries
(`continue ENG-031: in-review → in-qa`) to `_index-archive.md` per the
keep-three rule.

Post-pass `lib/eng-gate-check.sh`, whole-board: exit 0, clean.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-031: `ready-to-ship → blocked`, PR opened, merge request raised

`continue` event pass, context `ENG-031`, its own turn per the prior pass's
own `chained: ENG-031`. Narrow scope per the event's own contract — this
ticket only. Reading map for `continue`: steps 6 and 6b, plus the
not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four
lanes*, *Guards*). Mode check clean (`MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-031`): exit 0, clean.

Ran `skills/release-runner/SKILL.md` steps 1–4. `aiorders-api` is L1
(`config/projects.md`) — window check skipped. All four upstream gates
re-read directly from their own receipts (not trusted from the ticket log's
account) and confirmed **pass**: `agents/principal-engineer/reviews/ENG-031.md`,
`agents/qa/test-plans/ENG-031.md`, `agents/security/reviews/ENG-031.md`,
`agents/database/migrations/ENG-031-catering-order-capture-migration.md`.

**Readiness gate held**, matching the bar `ENG-007`'s own `ready-to-ship`
hop already set for the identical no-live-DB host limitation: rollback
written, not live-drilled (no Docker/psql/supabase CLI or MCP reachable this
session); observability n/a — no reachable runtime path exists anywhere
yet, independently re-confirmed by grep; cost $0/month (metadata-only DDL).
Full reasoning: `agents/devops/notebook/2026-09-03-release-readiness-log.md`.

Worktree `_eng/aiorders-api` checked clean (one pre-existing, already-flagged
stray `deno.lock` — third notice, see `observations.md`) before `git fetch`
+ ancestry check confirmed the branch not yet merged, and `gh pr list`
confirmed no PR already existed. Opened `aiorders-api` PR #12 and wrote
`inbox/2026-09-03-eng031-merge-request.md`. `lib/eng-notify.sh raise`
exited 0 with no delivery confirmation; `notified:` stamped by hand.

Ticket set `blocked`, `blocked_on: approver`, `blocked_from: ready-to-ship`,
`owner: approver`, `links.pr` set to PR #12. **1 transition**
(`ready-to-ship → blocked`), well under the cap of 4. Approver-facing WIP
uncapped (`wip.approver_limit: unlimited`) — nine items now open, listed
above. Machine WIP unaffected — `blocked` leaves the counted
`ready`..`ready-to-ship` range; the `ENG-016` family's slot now holds
`ENG-032`/`ENG-033`/`ENG-034`, still `ready`, still behind their sibling
`depends_on`.

**Dead-end sweep (scoped to this event):** no other ticket touched. Noticed
but not acted on — out of this event's own narrow contract: three
unprocessed-looking P0 incident notices in `inbox/` (`ENG-029`, `ENG-030`,
`ENG-035`, all "no action needed... fix proceeding without waiting on a
gate"), and `ENG-035` has a real board ticket
(`agents/eng-manager/board/ENG-035-autopilot-systemtriggered-auth-bypass.md`)
missing from this file's own In-flight table and `Next ID` counter. Both
filed in `observations.md` rather than chased here.

**Notify sweep:** this pass's own merge request raised and stamped above.
Checked every open item's `notified:`/`nudged:` against the 24h threshold
(step 7 is in the not-negotiable set, not scoped to this ticket alone):
`ENG-022`'s merge request (P0, cross-tenant PII fix) was notified
2026-09-03T01:26:47, never nudged, 24h24m old at check time — nudged this
pass, `nudged: 2026-09-04T01:52:01` stamped by hand (script gave no
delivery confirmation, same as this ticket's own merge request above).
`ENG-008`/`ENG-009`/`ENG-010` already used their one nudge each; every
other open item (`ENG-015`, `ENG-024`, `ENG-027`, `ENG-028`) is under 24h.
The three `gate: incident` P0 notices (`ENG-029`/`030`/`035`, all
"no action needed") were left un-nudged — nudging an FYI-only notice with
nothing to answer reads against the mechanism's own purpose, but this is a
judgment call, not a rule found in writing; flagged in `observations.md`
rather than decided unilaterally here. **Journal:** no G1/G2/G3 answered
this pass — not
applicable to a merge-request gate.

**Board update** — In-flight row for `ENG-031` (`ready-to-ship → blocked`,
owner → `approver`); header and "Waiting on the approver" section counts
corrected `eight → nine`, `ENG-031` added to both. Rolled the oldest of the
four now-live dated entries (`continue ENG-031: building → in-review`) to
`_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-031`) and whole-board: see
below.

`chained: none` — `blocked`, `blocked_on: approver`; the chaining guard
never fires on a ticket waiting on a human. Resume happens naturally: the
build loop's own merge detection (step 5) finds the merge on a future pass
via local git ancestry and advances this ticket to `shipped` then.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-031: `in-qa → ready-to-ship`, security gate pass, RLS-verification finding routed to ENG-033

`continue` event pass, context `ENG-031`, its own turn per the prior pass's
own `chained: ENG-031`. Narrow scope per the event's own contract — this
ticket only. Reading map for `continue`: steps 6 and 6b, plus the
not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four
lanes*, *Guards*). Mode check clean (`MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-031`): exit 0, clean.

Ran `skills/security-gate/SKILL.md` in full against the single-file diff
(`06e8e84`, 26 lines, pure DDL, no reachable code path yet — independently
re-confirmed via grep rather than trusted from QA's/review's own accounts).
Threat model, OWASP A01–A10, LLM checklist, secrets/dependency/config scan
all clean or `n/a` with a stated reason. **Verdict: PASS**, 0 blocking
findings.

**One non-blocking finding, investigated rather than taken on trust from
the design's AC-13 claim:** whether RLS is actually enabled on
`public.catering` is unverified from the repo — no tracked migration runs
`ALTER TABLE ... ENABLE ROW LEVEL SECURITY` on it, though
`20250729143357_initial_restaurant_rls.sql` defines seven policies against
it and the design's "zero new authorization code" argument depends on those
being enforced. Second occurrence of this exact class today (first:
`agents/security/reviews/ENG-015.md` Finding #1, `public.restaurants`).
Reasoned, not asserted, as pre-existing and low-likelihood (the same
migration drops older, already-restrictive named policies on `catering`,
which would be dead text on a table with RLS off); not worsened by this
diff; not fixable blind in a schema-only ticket's scope. Routed forward
rather than filed as a proposal or folded into a smoke test — `ENG-031` has
nothing live to test yet, so the empirical check (a non-owning account
attempting `catering` SELECT/UPDATE) is logged for `ENG-033`'s own future
gate, which reads this notebook as a matter of course. Full detail:
`agents/security/reviews/ENG-031.md`,
`agents/security/notebook/2026-09-03-findings.md`.

Receipt written (`agents/security/reviews/ENG-031.md`), `links.security_review`
set on the ticket in the same edit. **1 transition** (`in-qa →
ready-to-ship`), under the cap of 4 — security is its own fresh-context
session per `eng_build_loop.md`'s "each heavy step gets its own session,"
and nothing names it combinable with the release-readiness hop that
follows. No WIP-cap change — still inside the counted
`ready`..`ready-to-ship` range.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** inbox swept fresh — nothing crosses the 24h
no-nudge-no-decision threshold; `ready-to-ship` itself needs no approver
gate (devops's release-readiness hop raises G3, not this one). **Journal:**
no G1/G2/G3 or merge-request answered this pass — not applicable.
**Observations filed** (`observations.md`): this pass's own ticket-log
entry initially blew well past `config/conventions.yaml`'s
`ticket_log.entry.cap_lines: 20` before being caught and rewritten down to
a facts-and-pointers entry — same non-compliance pattern the immediately
prior hop had just flagged on this ticket. Also: this hop's and the prior
hop's logged `eng-trigger.sh` chain command use a path that does not
resolve from the instance cwd; fired the absolute path instead (below),
which is also what this event's own instructions specify verbatim — left
the discrepancy itself unresolved rather than guessing at its cause.

**Board update** — In-flight row for `ENG-031` (`in-qa → ready-to-ship`,
owner → `devops`); header paragraph's stale "now at `in-qa`" corrected.
Rolled the oldest of the four now-live dated entries (`continue ENG-030`)
to `_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-031`) and whole-board: see
below.

`chained: ENG-031` — `ready-to-ship` is agent-owned (devops's
release-readiness hop next), not the approver, not blocked, not terminal,
not held by a cap. Fired `/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-031` before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-031: `in-review → in-qa`, recovered a second dead pass's receipt, aiorders-api test-harness gap proposed

`continue` event pass, context `ENG-031`, its own turn per the prior pass's
own `chained: ENG-031`. Narrow scope per the event's own contract — this
ticket only. Reading map for `continue`: steps 6 and 6b, plus the
not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four
lanes*, *Guards*). Mode check clean (`MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-031`) and whole-board: both exit 0,
clean.

**Found a second dead pass, not a clean handover.**
`agents/principal-engineer/reviews/ENG-031.md` already existed at pass
start — untracked, dated today, verdict `pass` — but the ticket's own
frontmatter/log still read `in-review`, `links.review` blank, and
`agents/qa/test-plans/ENG-031.md` didn't exist. Same shape the previous hop
already found once on this ticket (a pass that did real work and died
before logging/committing it), one hop later: the code-review half of the
combined hop finished and wrote its receipt; the QA half, the ticket log,
the board index, and the chain fire never happened. Verified rather than
trusted: re-checked the migration against the design's `## Data` section
myself and re-confirmed the receipt's own citation (`proposals.md`,
2026-08-29, still open, 5 days old) — no divergence found, accepted as
genuine rather than redone from zero.

**Code review: pass** (unchanged, completed and logged) — 0/10 automatic
failures, no divergence from `ENG-016`'s design, style/git conventions
clean. Full detail already on the receipt.

**QA: pass, run fresh this pass.** No suite applies — the diff is one SQL
migration, no `.ts` file changed, so there was nothing for `deno
check`/`deno test` to run against (unlike `ENG-022`/`ENG-024`, same
project, same day). None of `ENG-016`'s 13 acceptance criteria apply to
this ticket's own diff — all require `ENG-032`/`ENG-033`/`ENG-034`, none of
which exist yet. This ticket's own criterion (the two columns exist exactly
as designed) verified by direct inspection, independently re-grepped for
collisions/references rather than trusted from the review or the build
hop. Zero open P0/P1 (`agents/qa/bugs/_index.md`: one open item, unrelated
project area). Full detail: `agents/qa/test-plans/ENG-031.md`.

Both receipts written: `agents/principal-engineer/reviews/ENG-031.md`,
`agents/qa/test-plans/ENG-031.md`. `links.review`/`links.test_plan` set on
the ticket in the same edit as the state change.

**Stopped at `in-qa`, not carried further to `in-security` this pass —
deliberate, not the transition cap.** 1 transition (`in-review → in-qa`),
well under 4. `sequential_after_quality: [security, release_readiness]`
keeps security a separate hop on purpose — it needs QA's *finished* plan,
which didn't exist until this pass wrote it. Same precedent `ENG-013`'s and
`ENG-022`'s own review+quality passes already set.

**Consequence:** `machine_wip` unaffected — `ENG-031` was and remains
inside the counted `ready`..`ready-to-ship` range (`in-qa` is inside it),
still `1/1` (the `ENG-016` family). Approver-facing WIP unaffected — no
gate raised or resolved this pass (`in-qa` needs no approver gate).

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing to raise. **Observation filed**
(`observations.md`): `config/conventions.yaml`'s `ticket_log.entry.
cap_lines: 20` (landed 2026-09-02, alongside the checkpoint mechanism this
pass's own prompt was built from) has not been followed by any pass since
— this ticket's own prior entries included, at ~118 lines. This pass's own
ticket-log entry follows the cap; reasoning moved to
`agents/principal-engineer/notebook/2026-09-03-review-log.md` and
`agents/qa/notebook/2026-09-03-coverage-gaps.md`. **Proposal filed**
(`proposals.md`): `aiorders-api` has no registered test harness anywhere
(no repo-root `deno.json`, empty Commands row) — the first ticket on this
project with zero code to even informally check either way.

**Board update** — In-flight row for `ENG-031` (`in-review → in-qa`, owner
→ `qa`); header paragraph's stale "now at `in-review`" corrected. Rolled
the oldest of the four now-live dated entries (`continue ENG-029`) to
`_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-031`) and whole-board: both
exit 0, clean.

`chained: ENG-031` — `in-qa` is agent-owned (security next), not the
approver, not blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-031`
before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-031: `building → in-review`, recovered a dead pass's uncommitted work, branch-naming fix

`continue` event pass, context `ENG-031`, its own turn per the prior
(work-breakdown) pass's `chained: ENG-031`. Narrow scope per the event's own
contract — this ticket only. Reading map for `continue`: steps 6 and 6b,
plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The
four lanes*, *Guards*). Mode check clean (`MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-031`): exit 0, clean.

**Worktree was mid-build, not clean.** `~/Documents/projects/_eng/aiorders-api`
sat on a branch with two uncommitted files: this ticket's own migration
(complete, correct) and an unrelated pre-existing `deno.lock` (already
independently noted by `ENG-029`'s own pass). Per `config/projects.md`'s
guard on a dirty worktree at pass start, investigated rather than trusted or
discarded: zero commits existed on the branch (confirmed via `git log
origin/main..HEAD`), no plan doc existed yet, and no ticket-log entry
recorded any of this — so the prior `continue ENG-031` pass this ticket's
own `chained:` line fired did the real work and died before committing.
Verified the migration line-by-line against the design's `## Data` section
and both cited template migrations; exact match, recovered and completed
rather than re-derived or discarded.

**Branch also renamed.** It was named after the parent (`ENG-016`) instead
of this ticket, against `engineering-standards.md`'s own
`{type}/{ENG-NNN}-{slug}` convention — no evidence of a deliberate
shared-branch call, and one wouldn't make sense given `ENG-033` depends on
`ENG-031` being *shipped*, not just built. Zero commits existed, so `git
branch -m` to `feat/ENG-031-catering-order-capture-migration` cost nothing.
Filed as an observation (`observations.md`) — first ticket-family this board
has run through `building`, worth a look if it recurs.

Committed (`06e8e84`) and pushed. Wrote the migration plan doc
(`agents/database/migrations/ENG-031-catering-order-capture-migration.md`)
— no live Postgres or Supabase MCP reachable this session, so verification
was repo-level (no naming collision, no existing reference, timestamp
ordering, template match), named honestly as a gap rather than assumed
away, same category of gap `ENG-007`/`ENG-011`/`ENG-013` each already
recorded. Step 6b artifact enumeration (`action_type`/`selections`/`ENG-031`
across both roots): every hit agrees on shape; no instruction or map in
conflict. PR body drafted on the ticket log (`building`'s own exit
condition) — no PR opened yet, L1 opens it at release-readiness. Full
detail: `ENG-031`'s own board-file log.

**1 transition** (`building → in-review`), under the cap of 4 —
`in-review`/`in-qa` is a fresh session's work per `eng_build_loop.md`'s "a
pass stops after `building` on purpose." No WIP-cap change: already inside
the counted `ready`..`ready-to-ship` range.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing to raise — `in-review` needs no approver gate.
**Observations filed:** two (`observations.md`) — the branch-naming fix, and
the still-unexplained stray `deno.lock`, now flagged by two independent
passes.

**Board update** — In-flight row for `ENG-031` (`building → in-review`,
owner → `principal-engineer`). Rolled the oldest of the four now-live dated
entries (`continue ENG-016`) to `_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-031`) and whole-board: both
exit 0, clean.

`chained: ENG-031` — `in-review` is agent-owned (principal-engineer + qa
combined hop next), not the approver, not blocked, not terminal, not held
by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-031`
before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-030 (design): `shaped → designed`, held by machine WIP

`continue` event pass, context `ENG-030` — this ticket's own turn at the
front of `traces/.pending`. Reading map for `continue`: steps 6 and 6b, plus
the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four
lanes*, *Guards*) — not mid-PRD, so step 2's checkpoint note doesn't apply.
Mode check clean (repo-root `.env` → `MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-030`) and whole-board: both exit 0,
clean.

Ran `tech-design/SKILL.md` for the architect role myself (no subagent
dispatch this time — single-function, single-repo change, small enough not
to need the split `ENG-016`'s/`ENG-020`'s/`ENG-021`'s passes used). Read
`analytics/index.ts`, `_shared/restaurantAccess.ts`, `api-key-auth/index.ts`
(closest structural precedent — single-file `index.ts`, no `handlers/`
split, already importing this same shared primitive), `brand-portal/utils.ts`,
`autopilot/index.ts`, `ADR-015`, and every existing `*.test.ts` in the repo,
all via `git show origin/main:` in `~/Documents/projects/_eng/aiorders-api`.
Also read `restaurant-portal/src/services/analyticsService.ts` and its
Supabase client config (`~/Documents/projects/_eng/restaurant-portal`) to
confirm `supabase.functions.invoke` already attaches the caller's session
`Authorization` header automatically — AC3 needs no frontend change — and
`App.tsx` to confirm `Dashboard` sits behind this portal's private-route
block today.

**Design:** `agents/architect/designs/ENG-030-analytics-function-restaurant-scoping-broken.md`.
New `analytics/auth.ts` exporting `authorizeAnalyticsRequest(req, supabase,
restaurantId, corsHeaders)` — 401s with no valid session, else calls
`verifyRestaurantAccess` (`_shared/restaurantAccess.ts`, same primitive
`ADR-015` already chose for `autopilot`, for the identical "outside
`brand-portal/`" reason), 403s if denied, else returns `null`; `index.ts`
calls it once, existing `source`/switch/aggregation code otherwise
untouched. **No new ADR** — `ADR-015`'s comparison transfers to `analytics`
unchanged, so this design cites it directly rather than minting a
content-free restatement (`next_id` stays `ADR-016`). **No one-way door**,
same conclusion as `ENG-022`/`ENG-029`. `touches_data: false`,
`touches_models: false`. Test approach commits to the same not-yet-built
stubbed-`SupabaseClient` shape `ENG-029`'s design already planned — required
here since AC4 names the wrong-tenant case, which only a stub (or a live
project) can exercise; one observation filed (`observations.md`) on the two
tickets converging on the same not-yet-shared stub. Full reasoning, every AC
walked, risk table: the design itself and `ENG-030`'s own board-file log.

**Routing (step 11): would be `ready` — held at `designed` instead.** Neither
L0 nor a one-way door. Machine WIP re-checked fresh from every ticket's own
frontmatter: still `1/1`, the `ENG-016` family (`ENG-016`/`ENG-031`
`building`, `ENG-032`–`034` `ready`), none `shipped`. Same precedent
`ENG-014`/`ENG-017`/`ENG-019`/`ENG-020`/`ENG-021`/`ENG-023`/`ENG-025`/
`ENG-026`/`ENG-029` already set: held at `designed`, owner staying
`architect`.

**Dead-end sweep:** out of scope for a `continue` event — this pass found no
new byproduct P0 (unlike `ENG-020`'s and `ENG-029`'s own design passes),
so nothing beyond the observation above surfaced unsought. **Notify sweep:**
no new gate item this pass. Swept `inbox/` (`date -u`: `2026-09-04T00:31:57`)
— nothing crosses the 24h no-nudge-no-decision threshold: closest is
`ENG-022`'s merge request at ~23h05m, not yet due; `ENG-008`/`ENG-009`/
`ENG-010` already carry their one-ever nudge; every other open item is well
under and/or informational-only. **Journal:** no gate answered this pass —
not applicable.

**Board update** — In-flight row for `ENG-030` (`shaped → designed`). Rolled
the oldest of the four now-live dated entries (`continue ENG-021`) to
`_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-030`) and whole-board: both
exit 0, clean.

`chained: none` — held by the machine-WIP cap (`1/1`, the `ENG-016` family),
one of the documented no-chain conditions; re-check once that family
reaches `shipped`. Not blocked, not terminal, not waiting on the approver —
only the cap.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-029: stays `designed`, held by machine WIP — stale board row fixed, ENG-008 nudged

`continue` event pass, context `ENG-029` — this ticket's own turn at the
front of `traces/.pending`. Reading map for `continue`: steps 6 and 6b, plus
the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four
lanes*, *Guards*) — not mid-PRD, so step 2's checkpoint note doesn't apply.
Mode check clean (`MODE=active`; instance `config/config.yaml` → `mode:`
empty). Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-029`) and
whole-board: both exit 0, clean.

**Dispatch (step 6): no transition available.** Machine WIP re-checked
fresh from every ticket's own frontmatter, not this table (see below for
why that distinction mattered this pass): `1/1`, the `ENG-016` family
(`ENG-016`/`ENG-031` `building`, `ENG-032`–`034` `ready`), none `shipped`.
`ENG-029`'s own `depends_on: []` and empty `priority:` (the approver did not
exercise the one lever its P0 incident notice offered) confirm the WIP cap
is the only hold. Stays `designed` — same conclusion the prior pass
reached, reconfirmed against live state rather than trusted from the log.

**Found and fixed: this ticket's own In-flight row was stale**, still
reading `shaped` hours after the ticket's own frontmatter and board-file log
moved to `designed`. Checked both this file and
`_index-archive.md` for a dated entry from that `shaped → designed` pass:
**neither has one** — its own step 10 never ran, and `ENG-035` (filed the
same pass) has no In-flight row at all. Second instance of the identical
shape `ENG-020`'s own pass already logged for `ENG-019` (a design pass that
files a P0 byproduct in full, then never writes its own board update).
Fixed `ENG-029`'s own row here (below); `ENG-035`'s is a different ticket,
left alone per the same precedent `ENG-020`'s pass set for the `ENG-014` gap
it found — see the observation filed below.

**Notify sweep:** swept `inbox/` (`date -u`: `2026-09-04T00:17:18`) —
`ENG-008`'s merge request (notified `2026-09-02T23:24:37`, no `nudged:`, no
`decision:`) crossed 24h (~24h53m). Ran `lib/eng-notify.sh nudge`, stamped
`nudged: 2026-09-04T00:18:02`. Everything else open is either still under
24h (`ENG-015`, `ENG-022`, `ENG-024`, `ENG-027` rescope, `ENG-028`, and the
`ENG-029`/`ENG-030`/`ENG-035` P0 incidents — all informational, nothing
owed) or already carries its one-ever nudge (`ENG-009`, `ENG-010`).

**One observation filed** (`observations.md`): the design-pass-skips-its-
own-board-update pattern is now two instances (`ENG-019`→`ENG-029`,
`ENG-029`→`ENG-035`) — both times immediately after fully filing a P0
byproduct. Not a ticket (no code is broken); flagged so a third instance
reads as a pattern rather than a surprise.

**Dead-end sweep:** out of scope for a `continue` event — not attempted
beyond the observation above. **Journal:** no gate answered this pass, not
applicable.

**Board update** — In-flight row for `ENG-029` corrected (`shaped →
designed`); "Waiting on the approver" `ENG-008` prose updated to drop the
stale "not yet due for a nudge" line. Rolled the oldest of the four
now-live dated entries (`continue ENG-020`) to `_index-archive.md` per the
keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-029`) and whole-board: both
exit 0, clean.

`chained: none` — held by the machine-WIP cap (`1/1`, the `ENG-016` family),
one of the documented no-chain conditions; re-check once that family
reaches `shipped`.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-016 (work-breakdown): `ready → building`, decomposed into four sub-tickets

`continue` event pass, context `ENG-016` — this ticket's own turn, per the
prior (`continue`) pass's own `chained: ENG-016`. Narrow scope per the
event's own contract — this ticket (and the sub-tickets it creates) only.
Reading map for `continue`: steps 6 and 6b, plus the not-negotiable set (1,
7, 8b, 9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*). Mode
check clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped
(`ENG-016`) and whole-board: both exit 0, clean.

Ran `work-breakdown/SKILL.md`. Autonomy check clean (all three touched
projects — `config-site-builder`, `aiorders-api`, `restaurant-portal` — are
L1). Split the design into four sub-tickets by surface, sequenced by
dependency per the design's own Rollout order (its own stated correctness
requirement, not a preference): `ENG-031` (database, `aiorders-api`, no
dependency, dispatched to `building`), `ENG-032` (frontend,
`restaurant-portal`, `depends_on: [ENG-031]`), `ENG-033` (backend,
`aiorders-api`, `depends_on: [ENG-031, ENG-032]`), `ENG-034` (frontend,
`config-site-builder`, `depends_on: [ENG-033]`) — the last three held at
`ready`. Full split/sequencing rationale, every field decided without an
explicit rule, and sizing:
`agents/eng-manager/notebook/2026-09-03-eng016-work-breakdown.md`.

**First work-breakdown on this board** (checked: no prior ticket has ever
carried `parent:`), so the machine-WIP interaction with a decomposed ticket
had no precedent to read from. Took the reading that the WIP slot is held by
the ticket *family* (parent + `parent:`-linked children) rather than by each
`ready..ready-to-ship` row separately — the only reading under which
work-breakdown's own step 6 (dispatch a met-dependency child to `building`)
and the 1-wide cap can both hold at once. Filed as an observation
(`observations.md`) rather than silently assumed, since it's a genuine
interpretive call on a cap the approver cares about, not a lookup.

`ENG-016` itself carries no diff of its own from here on — per
`definition-of-done.md`'s parent-ticket section, it moves directly to
`shipped` once every child settles (at least one `shipped`/`verified`),
skipping `in-review`/`in-qa`/`in-security` on itself.

**1 transition** on `ENG-016` (`ready → building`). Machine WIP: still `1/1`
— the family, not 5/1 (see above). Approver-facing WIP/approval cap
unaffected — no gate raised, no G1/G2/G3, no one-way door (the design
already cleared that).

**Dead-end sweep (scoped to this event):** the four new sub-tickets are the
only other tickets touched, and each carries its own owner and `chained:`
record already (see their own board files) — no dead end created.
**Notify sweep:** nothing raised this pass.
**Observations filed:** one (`observations.md`) — the machine-WIP-family
reading above. **One aside, not acted on:** `eng-gate-check.sh` cites this
exemption as "ADR-003," but this instance's real `ADR-003` is an unrelated,
earlier decision (migrations authority) — a citation-label mismatch, not a
functional bug; out of an instance-scoped pass's reach (department-template
script), left for whoever is next in that file. Full detail in the notebook.

**Board update** — `next_id` (`→ ENG-035`), header's Machine-WIP paragraph
(rewritten for the family reading), In-flight table (`ENG-016`'s row to
`building`; four new rows for `ENG-031`..`034`). Rolled the oldest of the
four now-live dated entries (`continue ENG-026`) to `_index-archive.md` per
the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-016`) and whole-board: both
exit 0, clean.

`chained: ENG-031` — the only child with every dependency met (it has none)
and something agent-actionable now. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-031`
before this pass exits. `chained: none` on `ENG-016` itself (parent has
nothing actionable until a child reports back) and on `ENG-032`/`ENG-033`/
`ENG-034` (each waiting on an unmet sibling dependency) — recorded on each
ticket's own board file.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-021 (design): stays `designed`, held by machine WIP — plus a new `ENG-022` dependency

`continue` event pass, context `ENG-021` — this ticket's own turn per the
prior (`decision`) pass's own `chained: ENG-021`. Reading map for `continue`:
steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
instructed*, *The four lanes*, *Guards*). Mode check clean (`MODE=active`;
instance `config/config.yaml` → `mode:` empty). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-021`) and whole-board: both exit 0,
clean.

Ran `tech-design/SKILL.md` for the architect role: gathered evidence across
all four repos this ticket touches myself (`aiorders-api`, `restaurant-portal`,
`aiorders-admin-hub`, `config-site-builder` — read via `git show origin/main:`
in each `~/Documents/projects/_eng/` worktree, none of which is checked out on
`main`), then dispatched design judgment and write-up to an `opus` subagent per
the skill's own model header, same split `ENG-016`'s and `ENG-020`'s passes
used. Did not take the report on faith: independently re-verified its most
consequential claim myself (below).

**The PRD's assumed write mechanism does not exist, and the correction shrinks
the ticket.** The PRD and ticket Notes name `restaurant-portal/src/pages/hiring/Index.tsx`
as the precedent for "the portal already writes `restaurant_website` directly"
and frame `restaurant_website`'s own RLS as the thing to confirm. Read in full:
`hiring/Index.tsx` contains no `.from(` call at all — every read/write goes
through `supabase.functions.invoke('brand-portal', {action: 'get_jobs'|'update_jobs'})`.
The real precedent is `src/pages/website/Index.tsx`, via `brand-portal`'s
`get_website_content`/`update_website_content` actions
(`aiorders-api/supabase/functions/brand-portal/website.ts`), which hard-codes
an `EDITABLE_PAGES = ['catering', 'careers']` allow-list. `restaurant_website.faqs`
is already a top-level column on that table (confirmed via the staff editor and
the bot's own `ai-search-openrouter` select list) — so the entire write-path
change is a one-element allow-list widening, not a new write mechanism, and
`restaurant_website`'s RLS (untracked in either repo's migration history, same
gap `ADR-006` recorded for `brands`) never becomes load-bearing.

**Design:** `agents/architect/designs/ENG-021-chat-bar-engagement-and-faq-self-service.md`.
A new "Customer Questions" page reading `ai_conversations` directly (its RLS
*is* tracked and readable — verified by reading the actual policy text, not
inferred), bounded to the most recent 100 sessions, flattened to one row per
customer question; a third "FAQs" tab on the existing Website page, writing
through the widened `update_website_content` action; a per-row "Add to FAQs"
hand-off via router state (never a URL parameter, so a customer's free text
never lands in browser history or an access log). **Two ADRs**
(`ADR-013` — the read/write split and why RLS is trustworthy for one table and
not the other; `ADR-014` — customer questions shown verbatim, protected by five
structural constraints rather than redaction), both `decided_by: architect`,
`_index.md` there updated (`next_id` → `ADR-015`). **No one-way doors**, all
six criteria checked. `touches_data: true` (no schema change — `database` does
a read-only live-project check that `ai_conversations`' RLS is actually enabled,
since no tracked migration creates the table itself), `touches_models: false`
(argued, not assumed: the owner already authors 4 of the bot's 5 context inputs
via `menus.ts`/`offers.ts`). Full reasoning, alternatives, every AC walked,
failure-mode table: the design itself. Process notes:
`agents/architect/notebook/2026-09-03-eng021-design.md`.

**New finding, verified independently before acting on it — not just taken
from the subagent's report.** This design edits `brand-portal/website.ts`,
whose `verifyRestaurantAccess` call is currently defeated (the helper returns
`{hasAccess}` and never throws; both call sites in `website.ts` discard the
result) — already `ENG-022` (P0, `blocked`/`approver`, all three gates passed,
PR #9 open). Confirmed myself, not trusted from the subagent or the board note:
`git merge-base --is-ancestor origin/fix/ENG-022-brand-portal-tenant-isolation
origin/main` → **not merged**; `git diff --stat` against that branch confirms
`website.ts` (6 lines) and `utils.ts` (19 lines) both touched, and the full diff
on `website.ts` is exactly the `verifyRestaurantAccess` → `requireRestaurantAccess`
swap at the same two call sites this design's own edits sit beside. `ENG-021`
adds a **new** owner-facing write to that handler while its gate is open, not
merely inheriting an old exposure — set `depends_on: [ENG-022]` on `ENG-021`'s
frontmatter myself (a technical sequencing fact, squarely the architect's own
call, not `priority`). Full verification trail: the notebook's addendum.

**One observation filed** (`observations.md`): confirming today's "held at
`designed`, owner stays `architect`" convention before applying it here found
`ENG-014`'s board file still at `owner: eng-manager` while `state: designed` —
violates the ticket template's own "state and owner move together" rule, a
stale bug from 2026-08-31, not a pattern to repeat. Not corrected there — a
different ticket, out of this event's own narrow contract.

**Routing (step 11): would be `ready` — held at `designed` instead.** Neither
L0 nor a one-way door. Machine WIP re-checked fresh from every ticket's own
frontmatter: `1/1`, `ENG-016` (`ready`, not yet `shipped`). Same precedent
`ENG-014`/`ENG-017`/`ENG-023`/`ENG-025`/`ENG-026`/`ENG-020` already set: held
at `designed`, owner staying `architect`, rather than writing `ready` while the
slot is occupied. **Unlike those, even once the slot frees `ENG-021` still
cannot start** — `depends_on: [ENG-022]` is a second, independent hold.

**Dead-end sweep:** out of scope for a `continue` event (narrower contract) —
not attempted beyond the `ENG-014` note above, which surfaced unsought while
confirming this pass's own routing precedent. **Notify sweep:** no gate item
written this pass. Swept `inbox/` for the 24h-no-nudge-no-decision check
(`date -u`: `2026-09-03T23:04:29`): nothing crosses it — closest is `ENG-008`'s
merge request at ~23h40m; `ENG-009`/`ENG-010` already carry their one-ever
nudge; every other open item (`ENG-015`, `ENG-022`, `ENG-024`, `ENG-027`
rescope, `ENG-028`, `ENG-029`/`ENG-030` incidents) is well under.

**Board update** — header's Machine-WIP paragraph (`ENG-021` added to the
held-for-slot list, with its `depends_on: [ENG-022]` noted inline); In-flight
row unchanged (state/owner didn't move). Rolled the oldest of the four now-live
dated entries (`continue ENG-016`) to `_index-archive.md` per the keep-three
rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-021`) and whole-board: both
exit 0, clean.

`chained: none` — held by the machine-WIP cap (`1/1`, `ENG-016`, `ready`) and,
independently, by the new `depends_on: [ENG-022]` (P0, unmerged); not waiting
on the approver, not blocked, not terminal, but two of the documented no-chain
conditions apply at once. Re-check once `ENG-016` ships **and** `ENG-022`
merges.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-020 (design): stays `designed`, held by machine WIP — plus ENG-030 filed (P0 byproduct)

`continue` event pass, context `ENG-020` — this ticket's own turn per the
prior (`decision`) pass's own `chained: ENG-020`. Reading map for
`continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10;
*Enforced vs instructed*, *The four lanes*, *Guards*). Mode check clean
(`MODE=active`; instance `config/config.yaml` → `mode:` empty). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both exit 0,
clean.

Ran `tech-design/SKILL.md` for the architect role: dispatched to an `opus`
subagent (skill's own model designation, same split `ENG-016`'s and
`ENG-027`'s passes used) with the PRD, this ticket's own evidence packet,
`projects.md`, `engineering-standards.md`, `decision-journal.md`,
`observations.md`, and `ADR-006`/`ADR-010` as the two directly-on-point
priors, instructed explicitly to verify the handed-over packet against
`origin/main` rather than trust it. **Independently re-verified the three
most load-bearing claims myself before trusting them** (same discipline
`ENG-016`'s pass applied): read `analytics/index.ts` directly and confirmed
it has no authentication or authorization of any kind, and confirmed
`supabase/functions/README.md` names it in neither its "no auth check at
all" list nor its own per-function notes; read `crm/customers.ts` directly
and confirmed the seven columns it actually persists
(`first_touch_at/_source/_medium/_campaign`, `first_referrer`,
`last_touch_at/_source`) and zero references to `utm_source`/`utm_medium`/
`utm_campaign`/`utm_data`, contra the PRD, the ticket's own Notes, and
`observations.md` row 100; read `_shared/restaurantAccess.ts` and
`brand-portal/utils.ts` and confirmed `verifyRestaurantAccess`'s real
signature and return-not-throw behaviour, then spot-checked
`customers.ts`/`offers.ts`/`feedback.ts`/`menus.ts`'s actual call sites and
confirmed the claimed misuse exactly — already inside `ENG-022`'s own fix
scope, not a new instance. All three confirmed exactly; nothing sent back.

**Design:** `agents/architect/designs/ENG-020-marketing-roi-attribution-reporting.md`.
**Two ADRs**, both `decided_by: architect`, both reversible, `_index.md`
there updated (`next_id` → `ADR-013`): `ADR-011` (the report ships as a new
`brand-portal` action, not an extension of `analytics` — `analytics` has no
access check to build AC5 on, and guarding either the new path alone or the
whole function were both wrong for a P2 feature ticket to do) and `ADR-012`
(channel classification runs post-query in TypeScript against an
uncontrolled-vocabulary precedence chain; SQL only aggregates, applying
`ADR-010`'s precedent). **No one-way doors** — both decisions reversible,
decided here rather than escalated; no G2. `touches_data: true` (one new
read-only `SECURITY DEFINER` RPC — `database` joins the chain at
work-breakdown), `touches_models: false` (deterministic aggregation, no
model call). Every acceptance criterion walked individually, full
failure-mode table, in the design itself. Process notes and dead ends:
`agents/architect/notebook/2026-09-03-eng020-design.md`.

**Byproduct P0, filed separately: `ENG-030`.** The same `analytics/index.ts`
read that motivated `ADR-011` is a live, unauthenticated cross-tenant data
exposure in its own right — any caller holding the committed publishable
key and a restaurant UUID can read that restaurant's yearly
revenue/orders/customers, no session or ownership check anywhere, and the
gap is invisible to `README.md`'s own "no auth check at all" list. Same bug
class as `ENG-022` and `ENG-029` (third instance this week, third
function, third failure shape), different function from both, not covered
by either's fix scope. Filed per `eng_build_loop.md` step 3's P0 carve-out
(`aiorders-api` is L1, not internal-lane) and today's own `ENG-029`
precedent (an identical byproduct-of-design-research P0): PRD
(`agents/product-manager/specs/ENG-030-analytics-function-restaurant-scoping-broken.md`,
short-form, `security`-type auto-skip G1), board ticket
(`agents/eng-manager/board/ENG-030-analytics-function-restaurant-scoping-broken.md`,
`intake → shaped`, `owner: architect`), incident notice
(`inbox/2026-09-03-eng030-p0-incident.md`, `lib/eng-notify.sh raise` run,
exit 0, `notified: 2026-09-03T15:24:21` stamped). Not absorbed into
`ENG-020`'s own diff — that ticket never touches `analytics`. `ENG-020`
does not depend on `ENG-030`.

**Routing (step 11): would be `ready` — held at `designed` instead.**
Neither L0 nor a one-way door, so the skill's own routing reads `ready`,
`owner: eng-manager`. **Machine WIP re-checked fresh from every ticket's
own frontmatter: `1/1`, `ENG-016`** (`ready`, not yet `shipped`). Same
precedent `ENG-014`/`ENG-017`/`ENG-023`/`ENG-025`/`ENG-026` already set:
held at `designed`, owner staying `architect`, rather than writing
`ready` while the one slot is occupied. `ENG-030` is unaffected by this
cap — `shaped` sits outside the counted range.

**Two observations filed** (`agents/eng-manager/observations.md`): a
correction to this file's own row 100 (`utm_source`-as-column claim) and
the PRD/ticket's shared claim about the mock "Analytics" page being live
in the nav, both wrong once checked against `origin/main`; and a note that
`ENG-019` and `ENG-020` will ship two independent revenue-attribution
surfaces on the same portal the same evening, worth reconciling before both
ship. Neither is a proposal — nothing to decide.

**Also checked, not acted on:** `ENG-019`'s own `continue` pass (the one
whose design research surfaced `ENG-029`) appears to have ended after
filing `ENG-029` and delegating its own design to a background subagent,
without writing `ENG-019`'s own board update — its ticket log still ends
`chained: ENG-019` with no further entry, and no design doc exists yet
(`traces/eng-loop-2026-09-03.log`, last `ENG-019`-relevant line: "I'll pick
back up once that finishes — no need to poll in the meantime"). Not this
event's ticket to resume — out of a `continue ENG-020` pass's own narrow
contract — so left for the dead-end sweep or a dedicated `continue ENG-019`
to pick up; noted as a third observation rather than fixed here.

**Notify sweep:** no new gate item for `ENG-020` itself (no one-way door).
`ENG-030`'s incident raised and notified separately, above. Swept `inbox/`
for the 24h-no-nudge-no-decision check: nothing crosses it this pass —
closest is `ENG-008`'s merge request at ~23h; `ENG-009`/`ENG-010` already
carry their one-ever nudge.

**Dead-end sweep:** out of scope for a `continue` event (narrower
contract) — not attempted, beyond the `ENG-019` note above, which surfaced
unsought while reading the design subagent's own cross-check.

**Board update** — header's Next-ID counter (`→ ENG-031`) and Machine-WIP
paragraph (`ENG-020` added to the held-for-slot list); In-flight table's
new `ENG-030` row; `ENG-020`'s own row unchanged (state/owner didn't move).
Rolled the oldest of the four now-live dated entries (`decision (ENG-027
G1)`) to `_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, whole-board and scoped `ENG-020` and
`ENG-030`: both exit 0, clean (see below).

`chained: none` (`ENG-020`) — held by the machine-WIP cap (`1/1`,
`ENG-016`, `ready`), one of the documented no-chain conditions. `chained:
ENG-030` — `shaped`, owned by `architect`, an agent-owned state; fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-030`
before this pass exits so its own design step starts without waiting for a
scheduled sweep, given the severity — same precedent `ENG-022`'s and
`ENG-029`'s own creation entries set.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

---

## 2026-09-03 — continue ENG-026 (design): stays `designed`, held by machine WIP

`continue` event pass, context `ENG-026` — this ticket's own turn per the
prior (`decision`) pass's own `chained: ENG-026`. Narrow scope per the
event's own contract — this ticket only. Reading map for `continue`: steps
6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
instructed*, *The four lanes*, *Guards*). Mode check clean (`MODE=active`).
Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-026`) and whole-board: both
exit 0, clean.

Ran `tech-design/SKILL.md` for the architect role. Read the live codebase
fresh across all three touched repos (`aiorders-api`, `aiorders-admin-hub`,
`restaurant-marketplace`) rather than trusting the PRD's framing or a stale
worktree — `restaurant-marketplace`'s own worktree (`eng/base`) was 16
commits behind `origin/master`, and its stale copy would have misdirected
every backend change in this design had `origin/master`/`origin/main` not
been checked directly: that repo's entire `supabase/functions/*` tree was
deleted 2026-08-23 ("now owned by aiorders-api"), so every backend change
in this design lands in `aiorders-api`, not here.

**Design:** `agents/architect/designs/ENG-026-foodswipe-channel-visibility.md`.
**One ADR** (`ADR-010`, post-query "Open Now" filtering rather than a SQL
predicate — reversible, `_index.md` updated, `next_id` → `ADR-011`). **No
one-way doors**, checked against all six criteria. Resolved requirement 7's
long-open rollout/backfill question as far as static analysis permits:
`has_order_food` defaulting `true` reproduces today's actual behavior
exactly (nothing gates that tab today); `has_catering` backfills from
`live_catering` (`NOT NULL`, already this codebase's working catering
signal); `has_dine_in` collides with a real but unverifiable pre-existing
`dine_in` column — handed to `database` as a concrete conditional check
rather than guessed either way. Full reasoning, all three repos' Components,
and the Dine-In-tab-can-go-empty rollout risk this found: the design's own
Data/Risks/Rollout sections, not repeated here.

**One proposal filed:** `admin-portal/handlers/restaurants.ts`'s
`updateRestaurant()` has no field allow-list — found while confirming how
the new flags reach the database, distinct from the already-tracked
ownership-check finding on the same function (`proposals.md`, corrected
this same pass's research to note `ENG-015` has since fixed the ownership
half). Not fixed inline, per `eng_build_loop.md` step 3.

**Machine WIP re-checked fresh from every ticket's own frontmatter:** `1/1`,
`ENG-016` (`ready`, not yet `building`) — every other ticket sits outside
the counted `ready`..`ready-to-ship` range. **Stays at `designed` — held by
the machine WIP cap, not a gate**, same precedent `ENG-025`'s and
`ENG-014`'s identical dispatch-hold already set: design work is cap-exempt,
entering `ready` is not, so this pass does not attempt that transition. No
branch created in any of the three worktrees, no code written.

**0 transitions.** Machine WIP unaffected (still `1/1`; `ENG-026` was never
inside the counted range). Approver-facing WIP and approval cap unaffected
— no gate raised.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing raised — no G2, no gate item written.
**Observations/proposals filed:** one proposal (above); no
`observations.md` entry — every finding from this pass's research already
has a home in the design doc itself or the proposal.

**Board update** — header's Machine-WIP paragraph (`ENG-026` added to the
cap-held list). In-flight table's `ENG-026` row unchanged (`state`/`owner`
didn't move). Rolled the oldest of the four now-live dated entries
(`continue ENG-024`) to `_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-026`) and whole-board: both
exit 0, clean.

`chained: none` — held by the machine WIP cap (`1/1`: `ENG-016`
occupying), one of the documented no-chain conditions; not waiting on the
approver, not blocked. The design is already complete, so whichever pass
next finds the slot free only needs to flip `state`/`owner` — nothing to
re-derive.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-016 (design): `designed → ready`, no one-way door

`continue` event pass, context `ENG-016` — this ticket's own turn at the
front of the queue, per the prior (`decision`) pass's own `chained:
ENG-016`. Narrow scope per the event's own contract — this ticket only.
Reading map for `continue`: steps 6 and 6b, plus not-negotiable set (1, 7,
8b, 9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*). Mode
check clean (`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped
(`ENG-016`) and whole-board: both exit 0, clean.

**The checkpoint this pass launched with was already stale** — it read
machine WIP as `1/1, ENG-024`, copied from the prior pass's own text. Two
intervening `continue ENG-024` and (implicitly) `ENG-015` hops had already
freed the slot before this pass started; re-checked fresh from every
ticket's own frontmatter (`grep state:` across the whole board, not the
cached header) rather than trusted, and found genuinely `0/1`, free. This
is exactly what "the file on disk is authoritative, not the checkpoint"
is for, not a gap in either pass.

Ran `tech-design/SKILL.md` (steps 1–11) for the architect role. Gathered
fresh `origin/main` evidence myself across all three repos this ticket
touches (`config-site-builder`, `aiorders-api`, `restaurant-portal` —
worktrees at `~/Documents/projects/_eng/`, read via `git show`/`git grep`
rather than trusted from each worktree's own stale local branch), then
delegated the design judgment and write-up to an `opus` subagent per the
skill's own model header (`Model: opus (design judgment + one-way-door
calls)`), the same sonnet-researches/opus-decides split this ticket's own
prior PRD-rewrite hop used. Did not take its report on faith: independently
re-verified its two most consequential claims — a live owner-facing editor
for `restaurant_website.catering` in `restaurant-portal`
(`CateringPageForm.tsx`), and `catering.status`'s undocumented
`'New Enquiry'` column default (`restaurant-marketplace/README.md`) — against
`origin/main` myself before trusting either into the routing decision.

**Design:** `agents/architect/designs/ENG-016-catering-quote-generator.md`.
**Two ADRs** (`agents/architect/decisions/ADR-008-catering-fulfillment-
stays-delivery-method.md`, `ADR-009-catering-order-form-opt-in-gate.md`),
both `decided_by: architect`, both reversible, `_index.md` there updated
(`next_id` → `ADR-010`). Both reverse the recommendation this pass itself
handed the design agent, on evidence rather than deference: `ADR-008` keeps
`catering.delivery_method` exactly as-is (no remap, no second field) and
expresses the approver's fulfillment intent as per-restaurant configurable
copy instead, since no acceptance criterion names the three values the
approver's rewrite proposed; `ADR-009` gates the whole feature behind an
explicit owner opt-in defaulting **off**, reversing this pass's own
default-on recommendation, once the design agent found the live
`restaurant-portal` editor surface that makes a default-off toggle
actually reachable rather than shipping dark. Full reasoning, alternatives,
and risks (a deploy-order crash risk in `CateringKanban`'s unguarded
`statusConfig` lookup; a catering-editor silent-field-wipe risk; a
brand-over-restaurant config precedence trap) are in the design itself, not
repeated here. Process notes and two research dead-ends:
`agents/architect/notebook/2026-09-03-eng016-piece1-design.md`.

**One-way-door verdict: none**, checked against all six criteria in the
design's own table (new datastore, new vendor, auth-model change, public
contract break, expensive-to-migrate data model, recurring cost) — two
nullable additive columns via `add column if not exists`, zero new
authorization code (existing row-scoped RLS plus `verifyRestaurantAccess`
already cover the new columns automatically), `$0/month` run cost, and
AC-10 backward-compatibility verified against `restaurant-marketplace`'s
and the GoHighLevel path's actual code rather than assumed. No G2 raised.

**Machine WIP re-checked fresh a second time, immediately before writing
this transition** (not just at pass start, in case anything changed
mid-pass — nothing did, single-flight lock holds): still `0/1`. **1
transition** (`designed → ready`), well under the cap of 4. **Consequence:**
machine WIP `0/1 → 1/1`, occupied by `ENG-016`. Approver-facing WIP
unaffected (uncapped since 2026-09-02; `ready` was never counted there
either way).

**Dead-end sweep (scoped to this event):** no other ticket touched, per
this event's own narrower contract (resume the named ticket only). The
stale-checkpoint gap above is the one thing this pass found and closed by
re-deriving fresh rather than trusting it.

**Notify sweep:** nothing raised this pass — no one-way door, no new gate
item. Out of this event's own scope to sweep the rest of `inbox/` for
unrelated nudges.

**Observations/proposals filed:** none new — the design and both ADRs
already carry every finding that came out of this pass (the option-set/
modifier gap, the two silent-failure traps, the brand-override
precedence); nothing surfaced without a home there.

**Board update** — In-flight table's `ENG-016` row (`state`, `owner`);
header's Machine-WIP paragraph, rewritten for the occupied slot. Rolled the
oldest of the four now-live dated entries (`decision (ENG-021 G1)`) to
`_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-016`) and whole-board: both
exit 0, clean.

`chained: ENG-016` — `ready` is agent-owned (`eng-manager`, work-breakdown
next); not the approver, not blocked, not terminal, and no longer cap-held
— this ticket now holds the slot it was previously waiting on. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-016`
before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

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

---

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

## 2026-09-03 — decision (ENG-020 G1): approved — `awaiting-scope → designed`

`decision` event pass, context `inbox/2026-09-03-eng020-g1-scope.md`.
Reading map for `decision`: steps 4 and 8c, plus step 6 (this answer
advances the ticket into a machine-owned state) and the not-negotiable set
(step 1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four lanes*,
*Guards*). Mode check clean (repo-root `.env` → `MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both exit 0,
clean.

**The answer:** `approved` (`decided: 2026-09-03T15:53:14.495206+00:00`).
No additional comment. Read as accepting the recommendation exactly as
scoped — a per-restaurant traffic-source/revenue breakdown on the brand
dashboard, reusing attribution data already captured on every customer row;
Clarity integration, a true ROI ratio, isolating AI-SEO specifically from
organic traffic, and a staff-facing all-restaurants rollup all named as
later, separate work — and as accepting every item in the readback's
"Assumed, correctable here" list since none was corrected. Full reasoning
on `ENG-020`'s own board file, not repeated here.

`ENG-020` moved `awaiting-scope → designed`, `owner: approver →
architect`. PRD `status: approved`
(`agents/product-manager/specs/ENG-020-marketing-roi-attribution-reporting.md`).
Journaled (`decision-journal.md`). Gate item's `## Decision` footer filled
in and moved to `inbox/_handled/`.

**Risks named in the PRD stay open, inherited by the architect at
`designed`, not resolved by this approval**: attribution honesty,
cross-domain attribution completeness, PIPEDA/Law 25 exposure, no
historical baseline for existing customers, small-restaurant traffic noise,
and tenant isolation (`ENG-015` precedent). Restated on the ticket's own
board file so the `continue ENG-020` hop doesn't have to re-derive them
from the PRD alone.

Machine WIP re-checked fresh from every ticket's own frontmatter, not the
cached header: still `1/1`, occupied by `ENG-024` (`ready-to-ship`, not
yet `shipped`) — irrelevant to this transition, since `designed` sits
outside the counted `ready`..`ready-to-ship` range and shaping/design work
is backlog grooming regardless of who holds the slot. Handed to the
architect for the tech design itself (a `continue ENG-020` session) rather
than attempted inline, same precedent `ENG-019`'s, `ENG-026`'s and
`ENG-016`'s identical G1-approved hand-offs already set.

**1 transition** (`awaiting-scope → designed`), well under the cap of 4.
**Consequence:** approver-facing WIP eight items open, down from nine —
this G1 drops off the "Waiting on the approver" list, same shape
`ENG-013`'s, `ENG-016`'s, `ENG-026`'s and `ENG-019`'s closures already set.
Machine WIP unaffected (`designed` sits outside the counted range).

**Dead-end sweep (scoped to this event):** no other ticket touched, per
this event's own narrower contract. **Notify sweep:** nothing raised this
pass — no new gate item written. Nothing else nudged — `ENG-008`'s and
`ENG-010`'s open merge requests are both still under the 24h threshold,
`ENG-009`'s already carries its one-ever nudge — out of this event's own
scope regardless. **Observations/proposals filed:** none new — this
ticket's own In-flight `priority` column had drifted from its frontmatter
(`now` on disk, cached blank), the same class of drift `ENG-016`'s
decision pass first named and `ENG-019`'s already fixed on its own row;
fixed directly on this row while already touching it rather than filed
again, since the mechanism gap is already on file.

**Board update** — In-flight table's `ENG-020` row (`state`, `owner`,
`priority` corrected to match the ticket's own frontmatter); header's
approver-facing bullet, "unanswered items" paragraph and count, "Waiting
on the approver" section's `ENG-020` paragraph and item count. Rolled the
oldest of the four now-live dated entries (`decision (ENG-016 rescope
G1)`) to `_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-020`) and whole-board: both
exit 0, clean.

`chained: ENG-020` — `designed` is agent-owned (`architect`, via
`tech-design/SKILL.md`, triggered by this exact state); not the approver,
not blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-020`
before this pass exits.

business-os itself left uncommitted — same standing default every pass
has used; the commit-convention question remains open, not re-decided
here.

---

## 2026-09-03 — decision (ENG-019 G1): approved — `awaiting-scope → designed`

`decision` event pass, context `inbox/2026-09-03-eng019-g1-scope.md`.
Reading map for `decision`: steps 4 and 8c, plus step 6 (this answer
advances the ticket into a machine-owned state) and the not-negotiable set
(step 1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four lanes*,
*Guards*). Mode check clean (repo-root `.env` → `MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-019`) and whole-board: both exit 0,
clean.

**The answer:** `approved` (`decided: 2026-09-03T15:52:30.648626+00:00`).
No additional comment. Read as accepting the recommendation exactly as
scoped — one-time and drip broadcasts, all-customers/inactive-for-N-days
audience, coupon-code redemption/revenue as ROI, owner-authored content,
owner/manager access only — and as accepting every item in the readback's
"Assumed, correctable here" list since none was corrected. Full reasoning
on `ENG-019`'s own board file, not repeated here.

`ENG-019` moved `awaiting-scope → designed`, `owner: approver →
architect`. PRD `status: approved`
(`agents/product-manager/specs/ENG-019-restaurant-marketing-broadcasts.md`).
Journaled (`decision-journal.md`). Gate item's `## Decision` footer filled
in and moved to `inbox/_handled/`.

**Risks named in the PRD stay open, inherited by the architect at
`designed`, not resolved by this approval**: durable scheduling/drip
infrastructure, whether the existing send services need changes for a
chosen-audience fan-out, and the CASL consent posture. Restated on the
ticket's own board file so the `continue ENG-019` hop doesn't have to
re-derive them from the PRD alone.

Machine WIP re-checked fresh from every ticket's own frontmatter, not the
cached header: still `1/1`, occupied by `ENG-024` (`ready-to-ship`, not
yet `shipped`) — irrelevant to this transition, since `designed` sits
outside the counted `ready`..`ready-to-ship` range and shaping/design work
is backlog grooming regardless of who holds the slot. Handed to the
architect for the tech design itself (a `continue ENG-019` session) rather
than attempted inline, same precedent `ENG-026`'s, `ENG-016`'s and
`ENG-015`'s identical G1-approved hand-offs already set.

**1 transition** (`awaiting-scope → designed`), well under the cap of 4.
**Consequence:** approver-facing WIP nine items open, down from ten — this
G1 drops off the "Waiting on the approver" list, same shape `ENG-013`'s,
`ENG-016`'s and `ENG-026`'s closures already set. Machine WIP unaffected
(`designed` sits outside the counted range).

**Dead-end sweep (scoped to this event):** no other ticket touched, per
this event's own narrower contract. **Notify sweep:** nothing raised this
pass — no new gate item written. **Observations/proposals filed:** none
new — this ticket's own In-flight `priority` column had drifted from its
frontmatter (`now` on disk, cached as `next`), the same class of drift the
`ENG-016` decision pass's own observation already named for this exact
row without fixing it; fixed directly on this row while already touching
it rather than filed again, since the mechanism gap is already on file.

**Board update** — In-flight table's `ENG-019` row (`state`, `owner`,
`priority` corrected to match the ticket's own frontmatter); header's
approver-facing bullet, "unanswered items" paragraph and count, "Waiting
on the approver" section's `ENG-019` paragraph and item count. Rolled the
oldest of the four now-live dated entries (`decision (ENG-013
stage-config question)`) to `_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-019`) and whole-board: both
exit 0, clean.

`chained: ENG-019` — `designed` is agent-owned (`architect`, via
`tech-design/SKILL.md`, triggered by this exact state); not the approver,
not blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-019`
before this pass exits.

business-os itself left uncommitted — same standing default every pass
has used; the commit-convention question remains open, not re-decided
here.


## 2026-09-03 — decision (ENG-026 G1): approved — `awaiting-scope → designed`

`decision` event pass, context `inbox/2026-09-02-eng026-g1-scope.md`.
Reading map for `decision`: steps 4 and 8c, plus step 6 (this answer
advances the ticket into a machine-owned state) and the not-negotiable set
(step 1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four lanes*,
*Guards*). Mode check clean (repo-root `.env` → `MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-026`) and whole-board: both exit 0,
clean.

**The answer:** `approved` (`decided: 2026-09-03T15:51:04.400168+00:00`).
No additional comment. Read as accepting the PM's recommendation exactly
as scoped — channel-visibility toggles and capability-based discovery
only, the other three bundled capabilities (operational status engine,
smart filters, promo badges) deferred as separate future tickets — and as
accepting requirement 6's proposed default (the three flags are staff-set
via `aiorders-admin-hub`, not restaurant self-service via
`restaurant-portal`) since the readback's explicit "correct this if wrong"
went uncorrected.

**One gap found and fixed while processing this decision, not a scope
change:** the PRD (`agents/product-manager/specs/
ENG-026-foodswipe-channel-visibility.md`) had neither the frontmatter
block nor the `## Decision` section every sibling PRD carries — the
`shaped` pass that wrote it skipped both, and nothing caught it before now
because no gate reads a PRD's own structure, only the ticket board's.
Added both per `templates/prd.md`: frontmatter (`status: approved`,
`decided:` stamped), and a `## Decision` section recording the bare
approval and naming requirement 7's rollout/backfill question as still
open. Not a proposal — a template-conformance gap on one document, fixed
in the same edit this decision already required, not a mechanism issue
worth a process change.

`ENG-026` moved `awaiting-scope → designed`, `owner: approver →
architect`. Journal entry written (`agents/eng-manager/config/
decision-journal.md`). Gate item's own `## Decision` footer already
carried the answer; appended a processed note and moved the file
`inbox/2026-09-02-eng026-g1-scope.md` →
`inbox/_handled/2026-09-02-eng026-g1-scope.md`.

**Requirement 7 (rollout/backfill for existing merchants) stays open,
inherited by the architect at `designed` — not resolved by this
approval and not silently defaulted.** The ticket's own Notes section
already flags it; restated here so the `continue ENG-026` hop below
doesn't have to re-derive it from the PRD alone.

**Machine WIP re-checked fresh from every ticket's own frontmatter, not
the cached board header:** `1/1`, occupied by `ENG-024` (`ready-to-ship`,
not yet `shipped`). Irrelevant to this transition — `designed` sits
outside the counted `ready`..`ready-to-ship` range; shaping/design work is
backlog grooming regardless of who holds the slot (`eng_build_loop.md`
step 6).

**1 transition** (`awaiting-scope → designed`), well under the cap of 4 —
the actual design work is the architect's own next hop, not attempted
inline here, same precedent `ENG-016`'s and `ENG-015`'s identical
G1-approved hand-offs already set. **Consequence:** ticket now owned by
`architect`, outside both the machine-WIP and approver-WIP counted
ranges. Approver-facing WIP uncapped (`wip.approver_limit: unlimited`);
this G1 drops off the "Waiting on the approver" list — same shape
`ENG-013`'s and `ENG-016`'s closures already set, ten items now open, down
from eleven.

**Dead-end sweep (scoped to this event):** no other ticket touched, per
this event's own narrower contract (act on the answered gate item,
advance only the ticket it belongs to).

**Notify sweep:** nothing raised this pass — no new gate item written.
Nothing else nudged — out of this event's own scope.

**Observations/proposals filed:** none this pass. The PRD-template gap
above was fixed inline rather than filed, since it's a one-document
authoring miss with an obvious fix, not a recurring mechanism gap — worth
watching for a second occurrence before treating it as one.

**Board update** — In-flight table's `ENG-026` row (`state`, `owner`,
`priority` corrected to match the ticket's own frontmatter — `now` — same
drift the prior pass's observation already flagged for this row without
fixing it, fixed here since this pass was already touching it;
`ENG-019`/`ENG-020`/`ENG-021`/`ENG-027`'s rows carry the same drift and
stay unfixed, out of this event's own scope, `updated` date); header's
approver-facing bullet, "unanswered items" paragraph and count, "Waiting
on the approver" section's `ENG-026` paragraph and item count. Rolled the
oldest of the four now-live dated entries (`continue ENG-024` review hop)
to `_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-026`) and whole-board:
both exit 0, clean.

`chained: ENG-026` — `designed` is agent-owned (`architect`, via
`tech-design/SKILL.md`, triggered by this exact state); not the approver,
not blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-026`
before this pass exits.

business-os itself left uncommitted — same standing default every pass
has used; the commit-convention question remains open, not re-decided
here.

## 2026-09-03 — decision (ENG-016 rescope G1): approved, "Lets start with piece 1" — `awaiting-scope → designed`

`decision` event pass, context `inbox/2026-09-02-eng016-g1-rescope.md`.
Reading map for `decision`: steps 4 and 8c (not negotiable), plus step 6
(this answer advances the ticket into a machine-owned state). Mode check
clean (`MODE=active`, repo-root `.env`; instance `config/config.yaml` →
`mode:` empty). Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-016`) and
whole-board: both exit 0, clean.

**The answer:** `approved` (`decided: 2026-09-03T15:47:46.139489+00:00`).
Full text: "Lets start with piece 1" (sic) — a bare approval of the split
this G1 proposed, silent on both riders it carried (the 3-vs-2 stage-count
resolution; the fulfillment-value remap question), read as accepting each
as proposed rather than overlooked. Confirms the recommended build order
without pre-authorizing Pieces 2 or 3 — neither is filed. Full reasoning
on `ENG-016`'s own board file, not repeated here.

`ENG-016` moved `awaiting-scope → designed`, `owner: approver →
architect`. PRD `status: approved`
(`agents/product-manager/specs/ENG-016-catering-quote-generator.md`).
Journaled (`decision-journal.md`). Gate item's `## Decision` footer filled
in and moved to `inbox/_handled/`.

Machine WIP re-checked fresh from every ticket's own frontmatter, not the
cached header: still `1/1`, occupied by `ENG-024` (`ready-to-ship`, not
yet `shipped`) — irrelevant to this transition, since `designed` sits
outside the counted `ready`..`ready-to-ship` range and shaping/design work
is backlog grooming regardless of who holds the slot. Handed to the
architect for the tech design itself (a `continue ENG-016` session)
rather than attempted inline, same precedent `ENG-015`'s identical
G1-approved hand-off already set.

**1 transition** (`awaiting-scope → designed`), well under the cap of 4.
**Consequence:** approver-facing WIP 11 items open, down from twelve —
this G1 drops off the "Waiting on the approver" list, same shape
`ENG-013`'s question closing already set. Machine WIP unaffected
(`designed` sits outside the counted range).

**Dead-end sweep (scoped to this event):** no other ticket touched, per
this event's own narrower contract. **Notify sweep:** nothing raised this
pass — no new gate item written. **Observations/proposals filed:** two
observations (`observations.md`) — the board index's cached `priority`
column disagreed with several tickets' own frontmatter
(`ENG-019`/`ENG-020`/`ENG-021`/`ENG-026`/`ENG-027`, all actually
`priority: now` on disk), noticed while re-checking dispatch order; same
root cause the open 2026-09-01 proposal on this file already names, not
re-filed, and not corrected here — out of this event's own scope. Second:
firing this ticket's own chain found `traces/.pending` 16 events deep —
not investigated, out of scope for a normal pass; full detail on the
observation itself.

**Board update** — In-flight table's `ENG-016` row (`state`, `owner`);
header bullet and "Twelve/Eleven unanswered items" count; "Waiting on the
approver" section's `ENG-016` paragraph and item count. Rolled the oldest
of the four now-live dated entries (`continue ENG-024` build hop) to
`_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-016`) and whole-board: both
exit 0, clean.

`chained: ENG-016` — `designed` is agent-owned (`architect`, via
`tech-design/SKILL.md`, triggered by this exact state); not the approver,
not blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-016`
before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — decision (ENG-013 stage-config question): approved, Reading A — PRs stay unmerged, ENG-028 filed

`decision` event pass, context
`inbox/2026-09-02-eng013-stage-config-question.md`. Reading map for
`decision`: steps 4 and 8c (not negotiable), plus step 5 (this answer
un-gates what was functionally an L1 merge decision, so merge status was
re-checked fresh rather than assumed). Mode check clean (`MODE=active`,
repo-root `.env`). Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean.

**The answer:** `approved`, "Reading a approved" (`decided:
2026-09-03T15:23:36.496711+00:00`) — ship `ENG-013`'s two already-gated PRs
as-is; file custom pipeline-stage definitions as a new, separate ticket
built on top. Full reasoning, the fresh merge-status check (`aiorders-api#5`,
`aiorders-admin-hub#4` — both confirmed `OPEN`, not merged), and the new
ticket's own derivation are on `ENG-013`'s own board file; not repeated
here.

**`ENG-028` filed** — staff-configurable Foodswipe pipeline stage set,
`aiorders-admin-hub`, `L`, `depends_on: [ENG-013]` — per Reading A's own
explicit direction, the same approver-affirmed-sequence carve-out
(`eng_build_loop.md` step 3) `ENG-027` already used. PM judgment (filter,
sizing, PRD/G1) delegated to an `opus` subagent per `prd-writer/SKILL.md`'s
model designation, grounded in the live code
(`classifyStage()`'s fixed if/else chain, the override column's own `CHECK`
constraint and its prescient comment naming this exact future risk) rather
than the raw request alone. G1 raised
(`inbox/2026-09-03-eng028-g1-scope.md`), carrying a rider on the one
assumption most worth the approver correcting (staff-defined stages are
manual-only — no generic auto-classification mechanism exists today) and
flagging that `ENG-022` (P0) outranks it for attention.

Both gate items journaled in `decision-journal.md`. `ENG-013`'s question
moved to `inbox/_handled/` with a processed footer.

**2 tickets touched, 0 net state transitions** (`ENG-013` stays `blocked`;
`ENG-028` created directly at `awaiting-scope` — shaping happens inline
since there was no pre-existing ticket, same as every other ticket filed
this way on this board). **Consequence:** `machine_wip` unaffected
(`ENG-028` sits outside the counted range — shaping is backlog grooming,
not gated by the WIP-1 slot, currently 1/1 with `ENG-024`).
Approver-facing WIP uncapped; the "Waiting on the approver" list's
composition changed (`ENG-013`'s question closed, `ENG-028`'s G1 opened)
but its count holds at twelve.

**Dead-end sweep:** out of this event's own narrower contract (act on the
answered gate item; advance only the ticket it belongs to, plus the direct
consequence of that decision). No other ticket swept.

**Notify sweep:** `ENG-028`'s new G1 raised and stamped
(`notified: 2026-09-03T16:10:27`). Nothing to nudge — no other item
crossed 24h this pass beyond what the prior `scheduled` sweep already
handled.

**Observations/proposals:** none filed this pass — the one pattern worth
tracking (a `changed` merge-request reply resolved as "ship the small
thing, file the big thing separately") is a decision-journal concern, not
a process gap, and is recorded there.

**Board update** — updated the In-flight table (`ENG-013`'s `updated`
date, new `ENG-028` row); rolled the oldest of the four now-live dated
entries (`scheduled` safety-net sweep, 3 G1s) to `_index-archive.md` per
the keep-three rule; corrected the header's `ENG-013` bullet and the
"Waiting on the approver" section's `ENG-013`/`ENG-028` paragraphs.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-013`, `ENG-028`) and
whole-board: both exit 0, clean.

`chained: none` — `ENG-013` is `blocked`/`blocked_on: approver` (the
chaining guard never fires on a ticket waiting on a human, and the only
remaining step is the approver's own GitHub merge). `ENG-028` is
`awaiting-scope`/`approver` (same guard, different gate). Neither ticket
this pass touched is in a machine-owned state.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-024 (review): fast-lane combined gate — `building → ready-to-ship`

`continue` event pass, context `ENG-024` — this ticket's own turn per the
prior build pass's own `chained: ENG-024`. Reading map for `continue`: steps
6 and 6b (6b doesn't apply — this hop reviews, it doesn't edit code). Mode
check clean (`MODE=active`). Gate-check run **after** the review and its
writes rather than before — a miss against the pattern prior hops set, named
on `ENG-024`'s own board file rather than silently corrected; both
`ENG-024`-scoped and whole-board runs came back exit 0, clean regardless.

Full review, independently reproduced rather than trusted from the build
hop's own log: automatic-10 scan (0/10 open), PRD conformance re-verified
against live code (including two claims cheap to check and load-bearing —
the marketplace read paths' actual column requirement, and
`updateRestaurantDetails`'s inability to clobber the new field), `deno
check`/`deno test` reproduced (6 pre-existing errors confirmed via a
corrected before/after comparison after an initial flawed attempt — see the
notebook), a mutation check executed directly (not hand-traced), and a full
OWASP A01–A10 walk (fast lane folds this into principal-engineer's own
gate) — every category `n/a` with a reason, no new input/capability/auth
surface. Full detail on `agents/principal-engineer/reviews/ENG-024.md`.

**One real gap found and not silently passed over**: this ticket's backfill
migration was never routed to `database`'s own migration gate — fast lane
skips the architect-design step that's the only thing that normally
triggers `schema-change/SKILL.md`. Assessed informally against that skill's
own 7 failure conditions as a sanity check (outside this review's actual
authority to gate): low risk, one soft miss (no stated runtime
estimate/batching, matching this repo's only backfill precedent exactly).
Not blocking — filed as a proposal (`proposals.md`, this pass,
`by: principal-engineer`) since the gap is in the fast-lane mechanism
generally, not particular to this migration; `release-runner` step 2
remains the documented backstop.

**Verdict: PASS.** Receipt written, `links.review` set. `state: building →
ready-to-ship`, `owner: backend → devops` — fast lane's own terminal machine
state before the L1 PR opens; no separate `in-qa`/`in-security` stop exists
on this lane.

**1 transition.** **Consequence:** ticket stays inside machine WIP's counted
range (`ready`..`ready-to-ship`), still `1/1`. Approver-facing WIP/approval
cap unaffected — no gate item raised this pass.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing to raise. **Observations/proposals filed:** one
proposal (fast-lane migration-gate mechanism gap, reasoning above).

**Board update** — this entry rolled the oldest of the three prior dated
entries (`watch`, inbox sweep) to `_index-archive.md` per the keep-three
rule; header's WIP-occupant paragraph and the In-flight table's `ENG-024`
row both updated to `ready-to-ship`/`devops`.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-024`) and whole-board: both
exit 0, clean.

`chained: ENG-024` — `ready-to-ship` is agent-owned (`devops`, via
`release-runner/SKILL.md`, triggered by this exact state); not the approver,
not blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-024`
before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-024 (build): `shaped → building` — fix + backfill + regression test, pushed

`continue` event pass, context `ENG-024` — this ticket's own turn at the
front of the queue, per the prior `scheduled` pass's own `chained:
ENG-024`. Reading map for `continue`: steps 6 and 6b, plus the
not-negotiable set (step 1, 7, 8b, 9, 10; *Enforced vs instructed*, *The
four lanes*, *Guards*). Mode check clean (`MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-024`) and whole-board: both exit 0,
clean.

Machine WIP re-checked fresh from every ticket's own frontmatter (not the
header's cached count): still `0/1`, free, unchanged since the prior pass.
`ENG-024` confirmed still `shaped`, still the only gate-clear To-do-column
candidate.

Built per the PRD, single repo (`aiorders-api`): branched
`fix/ENG-024-onboarding-marketplace-visibility` off a freshly fetched
`origin/main` (worktree was sitting on `ENG-015`'s old branch, no
uncommitted changes); added `show_in_marketplace: true` to
`createRestaurant`'s insert, same intent as the adjacent `approved: true`;
wrote a backfill migration scoped to exclude `restaurant-claims` rows on
purpose (`claimed_by_user_id IS NOT NULL`), after actually reading that
flow's insert to confirm the DB-level signature rather than assuming
"unapproved" would always hold; added a regression test proving the insert
payload carries the field, and proved the test would have caught the bug
by reverting the fix locally and re-running (went red, then green again
after restoring). `deno check`: 6 pre-existing `TS18046` errors, confirmed
unchanged against the pre-edit tree, none introduced. Committed
(`aiorders-api@8c97bd3`) and pushed; PR body drafted in the ticket's own
log, not opened yet (devops's release-readiness hop). Full narrative,
including the DB-level-default question investigated and deliberately
routed to a proposal instead of built (schema change, would break fast-lane
eligibility), is on `ENG-024`'s own board file — not repeated here.

**One environment gotcha hit and fixed, not just noted**: `deno
check`/`deno test` failed even from the target function's own directory
(the workaround `ENG-022`'s review hop recorded) — an unrelated
`~/package.json`/`~/node_modules` at the home directory, which Deno's
auto-discovery walks up and finds regardless of working directory. Fix:
`DENO_NO_PACKAGE_JSON=1 deno check --node-modules-dir=none` (same for
`deno test`). Logged to `observations.md` so the next pass touching Deno
tooling on this repo doesn't rediscover it.

**1 transition** (`shaped → building`). **Consequence:** machine WIP
`0/1 → 1/1` — the counted `ready`..`ready-to-ship` range is occupied again,
this time by `ENG-024`. Approver-facing WIP and approval cap both
unaffected — no gate touched this hop (the DB-default finding is a
proposal, not a gate item; batched into the weekly report per step 3).

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing raised this pass — a build hop doesn't reach a
gate. **Observations/proposals filed:** one proposal
(`proposals.md`, `show_in_marketplace`'s missing DB-level default) and one
observation (`observations.md`, the Deno/`node_modules` environment fix).

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-024`) and whole-board: both
exit 0, clean.

`chained: ENG-024` — `building` is agent-owned (next hop: fast lane's
combined review + quality + OWASP gate, owned by `principal-engineer`); not
the approver, not blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-024`
before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

---

## 2026-09-03 — scheduled (launchd): safety-net sweep — 3 G1s raised, 1 chain fired

`scheduled` event pass. Per the reading map, read the whole document (never
narrowed). Mode check clean (`MODE=active`, repo-root `.env`). Pre-pass
`lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Steps 2–4** — `agents/product-manager/inbox/`, `inbox/requests/`,
`agents/eng-manager/inbox/`: all empty but for `.gitkeep`/`_handled`/
`_processed`. All nine (now twelve) `inbox/` items re-read directly:
`decision:` empty on every one. Nothing to shape, nothing to propose,
nothing answered.

**Step 5 (merge detection)** — fetched both worktrees fresh
(`aiorders-api`, `aiorders-admin-hub`; the latter clean, the former with the
same pre-existing untracked `deno.lock`). `git merge-base --is-ancestor`
against `origin/main` for all nine branch/repo pairs behind the six
`blocked` tickets (`ENG-008`/`009`/`010`/`015`, both repos; `ENG-022`,
`aiorders-api`). All nine: not merged. `ENG-013` correctly excluded — it's
`blocked_on: approver` for its stage-config question, not an L1 PR.

**Step 6 (dispatch) — the substantial finding this pass.** Investigating
whether the machine-WIP-1 slot (free, 0/1) had a real candidate led to the
board's own "9/2, over cap" framing, which turned out to be **wrong**: this
instance's `config/config.yaml` raised `wip.approver_limit` to `unlimited`
on 2026-09-02, by the approver's own explicit, dated decision — the
department-template default of `2` this board had been citing is stale for
this instance. (First read this as the reverse problem — that "unlimited"
was an unverified/fabricated claim — until `config/config.yaml` itself was
actually opened; recorded here because the near-miss is itself worth
knowing about, not because it went anywhere.) Consequence: `ENG-019`,
`ENG-020`, `ENG-021` were sitting at `shaped`, each held only by "the WIP-2
cap is already over" — true 2026-08-29, false since 2026-09-02, never
rechecked in five days. All three PRDs are complete with no material
divergence between the PM's and the blind architect's readings. Raised all
three G1s (`inbox/2026-09-03-eng01{9,20,21}-g1-scope.md`),
`lib/eng-notify.sh raise` on each (exit 0, `sent: active` — the
already-tracked `MODE`-clobber bug, not re-filed), stamped `notified:` on
each. Each ticket's own board file carries the full derivation and its own
`shaped → awaiting-scope` transition; `chained: none` on all three
(awaiting-scope is a no-chain state).

Separately, `ENG-024` (fast lane, G1 auto-skipped) has had no gate of any
kind blocking it since 2026-08-29 — only the machine-WIP cap, then 6/1, now
confirmed 0/1 free. Correct next pick for the slot (only To-do-column
ticket with zero outstanding gate). Not moved into `building` this
pass — same precedent `ENG-022`'s own dispatch hop set: new implementation
work belongs in its own dedicated session. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-024`
before this pass exits; queued correctly behind this pass's own lock
(confirmed via `traces/eng-loop-2026-09-03.log` — four `watch` fires from
this pass's own inbox writes and the `continue ENG-024` fire all logged
`pass in flight, queued as pending`, none dropped).

**Step 7 (notify sweep)** — ages recomputed against `date -u`
(`2026-09-03T12:00:56Z`). `ENG-009` already nudged by the prior `watch`
pass (~11:34 UTC); no second nudge (exactly one, ever). All other open
items, including this pass's own three new G1s, under 24h.

**Step 8 (dead-end sweep)** — no ticket found with a missing chain record
or an unjustified `chained: none`. `blocked_from` present on all six
`blocked` tickets.

**Step 8b** — one observation filed (`observations.md`): at least two prior
passes (spanning 2026-09-02 into tonight) read the approver-facing WIP cap
as the department-template default (`2`) rather than checking this
instance's own override (`unlimited`), stalling three complete, ready
tickets for up to a day past when they were actually free to proceed — the
same class of miss as reading a rule instead of checking the config it
claims to describe.

**Board update** — this entry rolled the oldest of the three prior dated
entries (`continue ENG-015`, security gate) to `_index-archive.md` per the
keep-three rule; corrected the header's approver-WIP framing and the "No
separate approval cap exists" paragraph, both of which still cited `2`;
updated the In-flight table for `ENG-019`/`020`/`021`.

**4 tickets touched, 3 transitions** (`ENG-019`/`020`/`021`, each
`shaped → awaiting-scope`; `ENG-024` unchanged in state but re-evaluated
and chained). Post-pass `lib/eng-gate-check.sh`, whole-board: exit 0,
clean.

`chained: ENG-024` — the one agent-owned, gate-free ticket this pass found
genuinely able to move. `chained: none` on `ENG-019`/`020`/`021`
individually (awaiting-scope, waiting on the approver).

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — watch (launchd): swept all three inboxes, nothing new — one 24h nudge sent

`watch` event pass, context `launchd`. Per the reading map: steps 2, 3, 4, and
step 5 (several of the changed files that woke this pass are merge-request
items — `ENG-015`'s and `ENG-022`'s freshly raised this morning). Mode check
clean (`MODE=active`, repo-root `.env`). Post-pass `lib/eng-gate-check.sh`,
whole-board: exit 0, clean (no ticket state changed this pass, so pre- and
post-pass share the same clean result).

**Step 2** — `agents/product-manager/inbox/` and `inbox/requests/`: both empty
but for `.gitkeep`. Nothing to shape.

**Step 3** — `agents/eng-manager/inbox/`: empty but for `.gitkeep` and the
existing `_processed/` entry. No internally-originated finding to turn into a
proposal.

**Step 4** — read all nine open items in `inbox/` (the same nine the header
above counts). All nine still carry an empty `## Decision` / `decision:` —
re-confirmed by reading each file directly, not inferred from the board's own
narrative. Nothing answered, nothing to act on; per the standing rule, silence
is not an answer.

**Step 5** — merge detection, run because the watch fired on merge-request
files. `git fetch origin` in both department worktrees
(`~/Documents/projects/_eng/aiorders-api`, `~/Documents/projects/_eng/aiorders-admin-hub`;
both worktrees clean but for an untracked, harmless `deno.lock` in
`aiorders-api`, left by a prior gate's `deno` run — not a sign of a died pass).
`git merge-base --is-ancestor` checked for every branch backing a currently
`blocked` ticket against its repo's `origin/main`:
`feat/ENG-008-influencer-admin-management`,
`feat/ENG-009-influencer-engagement-info`,
`feat/ENG-010-influencer-relationship-notes` (all three, both repos),
`fix/ENG-015-agency-reseller-brand-scoping` (both repos), and
`fix/ENG-022-brand-portal-tenant-isolation` (`aiorders-api`). All ten checks:
**not merged**. No ticket state changes.

**Step 7 (notify sweep)** — computed each open item's age against current UTC
(`date -u`: `2026-09-03T11:33:19Z`) rather than trusting the board's own
narrative, since that narrative is exactly what goes stale between passes.
Eight of nine are under 24h. `ENG-009`'s merge request
(`inbox/2026-09-02-eng009-merge-request.md`, `notified: 2026-09-02T10:51:07`)
is not: 24h42m old, `nudged:` empty, `decision:` empty. Ran
`lib/eng-notify.sh nudge` on it and stamped `nudged: 2026-09-03T11:34:08`.
Board's own "Waiting on the approver" line for `ENG-009` corrected to match
(was still saying "not yet due").

**Independently reconfirmed, not re-proposed:** the nudge call's own log line
read `sent: active`, not `sent: nudge` — the exact `$MODE`-clobbered-by-`.env`
defect `proposals.md`'s 2026-08-25 `eng-manager` row already names (this
script's local `MODE` var, set from argv, gets overwritten when it sources
`.env`'s unrelated `MODE=active`). The Slack message itself still carries the
right ticket/gate/recommendation/PR-link content; it's only missing the
`_Still waiting, 24h on._` framing line. Already tracked, still open, still
unfixed — not filing a duplicate.

**1 transition: none.** No ticket's `state:` changed this pass — nothing was
answered, nothing merged. **Dead-end sweep:** out of this event's contract
(the reading map sends `watch` to steps 2–5, not step 8's whole-board sweep);
not run beyond what those steps already touched. **Notify sweep:** covered
above — one nudge, no new raises.

`chained: none` — no ticket was touched or advanced this pass, so there is no
agent-owned state to hand forward. The nudge changes no ticket's `state:`.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-015 (release-readiness): both PRs opened — `ready-to-ship → blocked`

`continue` event pass, context `ENG-015` — this ticket's own turn at the
front of the queue, per the prior pass's own `chained: ENG-015`. Narrow
scope per the event's own contract — this ticket only. Mode check clean
(`MODE=active`). Pre/post-pass `lib/eng-gate-check.sh`, scoped (`ENG-015`)
and whole-board: both exit 0, clean.

Ran `skills/release-runner/SKILL.md` steps 1–4. Both projects are L1, so
step 1 (window check) didn't apply. Step 2: all four upstream gates
re-confirmed `pass`. Step 3 (readiness gate): rollback (a single `DROP
POLICY`, reasoned independent of the handler-code change), observability
(existing `console.error`/Supabase logs, same convention every other
handler in this file already uses), and cost ($0/month — no new
service/dependency) all held clean, same bar this instance's own
`ENG-007` precedent already accepted given the standing no-live-DB
constraint. Worked in the department's own worktrees
(`_eng/aiorders-api`, `_eng/aiorders-admin-hub`), both verified fresh
against `origin/main` before touching anything: neither branch merged yet,
no PR already existed for either.

Opened `aiorders-api` PR #10 (backend first, same ordering `ENG-013` used),
then `aiorders-admin-hub` PR #8. Each PR body states the two must merge
together — the backend's new `approved = false` INSERT policy only becomes
load-bearing once the frontend stops sending `approved: true`, and vice
versa. Raised one L1 merge request covering both
(`inbox/2026-09-03-eng015-merge-request.md`, `pr_urls:` YAML-list format),
naming both round-1 findings' resolution and the security review's one
non-blocking RLS-activation finding with its folded-in staging-smoke-test
recommendation. Notified (`eng-notify.sh raise`, exit 0), stamped
`notified: 2026-09-03T10:03:53`.

**1 transition** (`ready-to-ship → blocked`). **Consequence:** machine WIP
`1/1 → 0/1` — `blocked` sits outside the counted `ready`..`ready-to-ship`
range, freeing the slot; picking the next To-do-column candidate is left
for a future pass, not this one (same precedent `ENG-004`/`ENG-022` set).
`owner` moves `devops → approver`. Approver-facing WIP: item added to the
queue (now 9 unanswered, `wip.approver_limit` itself `unlimited` since
2026-09-02 — the board header's "over cap" framing is the already-flagged,
still-unresolved stale accounting from before that change, not
re-litigated here).

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** this pass's own merge-request item raised and stamped
above; nothing else swept, out of this event's own narrower contract.

`chained: none` — blocked on the approver (`blocked_on: approver`), one of
the documented no-chain conditions. The next hop is a human merging both
PRs; a future pass detects the merge itself by local git ancestry and
advances the ticket to `shipped` once **both** repos have merged.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-015 (security gate): PASS — `in-security → ready-to-ship`

`continue` event pass, context `ENG-015` — this ticket's own turn at the
front of the queue, per the prior pass's own `chained: ENG-015`. Narrow
scope per the event's own contract — this ticket only. Mode check clean
(`MODE=active`). Pre/post-pass `lib/eng-gate-check.sh`, scoped (`ENG-015`)
and whole-board: both exit 0, clean.

Threat-modeled the change, then walked OWASP A01–A10 against
`security-baseline.md`. Independently re-ran `deno check`/`deno test`
rather than trusting the round-2 review's/QA's own accounts (22/22,
matched by name); did not re-run the mutation check a third time (already
independently confirmed twice today). Both round-1 findings re-verified
closed by reading the live diff. Zero blocking findings. One new,
non-blocking finding sharper than anything named so far: whether RLS is
actually *enabled* on `public.restaurants` — not just whether the new
policy's logic is correct — is unverified from this repo (no live Postgres
reachable; the table predates tracked migration history entirely, same
untracked-schema-history shape `ADR-006` already names for `brands`).
Reasoned as low-risk and pre-existing rather than blocking: this table's
own multi-migration public-SELECT lockdown would be pointless otherwise,
and no incident anywhere in this business's history suggests it's actually
off. Not fixed blind (a defensive RLS-enable would be an unbounded-blast-
radius change across four frontends) — folded into a sharpened version of
QA's own already-planned staging smoke test instead. Second finding
(verbose `error.message`, pre-existing) not re-proposed, already tracked
under `ENG-009`'s standing proposal. Full detail: `ENG-015`'s own
board-file log, this date; `agents/security/reviews/ENG-015.md`;
`agents/security/notebook/2026-09-03-findings.md`.

**1 transition** (`in-security → ready-to-ship`). **Consequence:** no
machine-WIP change — still inside the counted `ready`..`ready-to-ship`
range, `ENG-015` remains the sole occupant. Approver-facing WIP
unaffected — this hop raised no gate; devops's release-readiness hop
raises the L1 merge request next. `owner` moves `security → devops`.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing to raise or nudge — `ready-to-ship` needs no
approver gate yet.

`chained: ENG-015` — `ready-to-ship` is agent-owned (devops), not the
approver, not blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-015`
before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-015 (combined review+quality): PASS, round 2 — now `in-security`

`continue` event pass, context `ENG-015` — this ticket's own turn at the
front of the queue, per the prior pass's own `chained: ENG-015`. Narrow
scope per the event's own contract — this ticket only. Mode check clean
(`MODE=active`). Pre/post-pass `lib/eng-gate-check.sh`, scoped (`ENG-015`)
and whole-board: both exit 0, clean.

Re-reviewed the full branch diff (both repos, now including the round-1
fix) rather than only the incremental change. Both round-1 findings
(self-approve bypass, brand-reassignment bypass) verified fixed by
independently re-running the mutation check — reverted the fix, got
exactly the three tests naming those findings red, 19 others stayed
green, restored clean — rather than trusting the fix hop's own account.
Automatic-failure scan: all 10 clear. Test quality: sound (assertions on
what reaches the persistence layer, not implementation details; the
"empty-brand-list never queries `restaurants`" test cannot pass
vacuously).

**One substantive gap found and named, not silently passed over**: AC3/4/5
(the add-location write path) are enforced entirely by the new RLS
`INSERT` policy plus a frontend conditional, and neither is reachable by
any automated or live test this pass — no live Postgres (the same
standing gap every prior hop on this ticket named), and
`aiorders-admin-hub` has zero test infrastructure at all (open proposal,
`proposals.md` 2026-08-31, not re-filed). De-risked by a full static trace
of the policy against this table's entire RLS history (no `RESTRICTIVE`
policy anywhere, no other `INSERT`-capable policy interferes, the `WITH
CHECK` is a plain three-term AND with no path to accidental
over-permissiveness) rather than silently assumed fine — full trace in
`agents/qa/test-plans/ENG-015.md`. Verdict reasoned as **pass, with a
named manual-verification recommendation** (a staging smoke test) rather
than a hold, consistent with every other gate on this ticket's own
identical "no live DB" limitation and with `definition-of-done.md`'s own
allowance for a manual-verification note where automation genuinely can't
reach. Two further non-blocking notes (an untested empty-update-payload
edge case; a pre-existing, non-atomic read-then-write ownership check) —
full detail in the receipts below.

Receipts written: `agents/principal-engineer/reviews/ENG-015.md`,
`agents/qa/test-plans/ENG-015.md`. Notebooks:
`agents/principal-engineer/notebook/2026-09-03-review-log.md`,
`agents/qa/notebook/2026-09-03-coverage-gaps.md` (first entry in that
notebook — flags the coverage-gap pattern for future tickets on this same
handler family).

**1 transition** (`building → in-security`). **Consequence:** no
machine-WIP change — `in-security` is still inside the counted
`ready`..`ready-to-ship` range, `ENG-015` remains the sole occupant.
Approver-facing WIP and approval cap both unaffected — no gate raised.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing to raise or nudge — `in-security` needs no
approver gate.

`chained: ENG-015` — `in-security` is agent-owned (security), not the
approver, not blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-015`
before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-015 (round-1-fix build hop): mass-assignment bug closed, 22 tests added

`continue` event pass, context `ENG-015` — this ticket's own turn at the
front of the queue, per the round-1 review's own `chained: ENG-015`. Narrow
scope per the event's own contract — this ticket only. Mode check clean
(`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-015`) and
whole-board: both exit 0, clean.

Fixed the round-1 blocking finding in `aiorders-api`'s
`admin-portal/handlers/restaurants.ts`: `updateRestaurant` validated only
the restaurant's *existing* `brand_id`, then wrote every other body field
unfiltered via the service-role client — a partner could self-approve their
own held-for-review restaurant or reassign it to a brand they don't own.
Added `stripPartnerRestrictedFields`, deleting `approved`/`brand_id` from a
non-staff update before the write (the review's own first-listed fix shape,
over a presence-based 403 — stripping no-ops on a caller that merely echoes
back an unchanged value). Added the missing test coverage the same review
flagged (zero tests, third occurrence of the shape this week): new
`restaurants.test.ts`, 22 cases, fake-Supabase-client shape modeled on
`ENG-022`'s reviewed `offers.test.ts`. Executed a mutation check (not
hand-traced): reverting the fix made exactly the three tests naming round
1's findings go red, all other 19 stayed green — confirmed wired, not
vacuous. `deno check` clean; full suite 22/22, and 78/78 across the whole
`admin-portal/handlers/` directory on a clean re-run (one flaky,
unrelated-file failure on a first pass, traced to a pre-existing
wall-clock-boundary test in `brands.test.ts` and filed to
`observations.md`, not fixed). Step 6b artifact enumeration: both
`proposals.md` rows about this file were already corrected by the prior
build hop and remain accurate — nothing stale found this round. Full
detail: `ENG-015`'s own board-file log, this date.

Committed and pushed, `aiorders-api` only (`aiorders-admin-hub` had no
round-1 findings): `99ea353` on
`fix/ENG-015-agency-reseller-brand-scoping`. No PR yet — unchanged, still
devops's release-readiness step.

**0 transitions** — `state`/`owner` unchanged (`building`/`eng-manager`).
Machine WIP unaffected, still 1/1 (`ENG-015`). Approver-facing WIP
unaffected — no gate touched.

`chained: ENG-015` — `building` → combined review+QA hop next (round 2),
owned by `principal-engineer`/`qa`, not the approver, not blocked, not
terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-015`
before this pass exits. Post-pass `lib/eng-gate-check.sh`, scoped
(`ENG-015`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

---

## 2026-09-03 — continue ENG-015 (combined review+quality): FAIL, round 1 — back to `building`

`continue` event pass, context `ENG-015` — this ticket's own turn at the
front of the queue, per the prior pass's own `chained: ENG-015`. Narrow
scope per the event's own contract — this ticket only. Mode check clean
(`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-015`) and
whole-board: both exit 0, clean.

Reviewed both repos' diffs against the design/PRD/`ADR-006`. Automatic-failure
scan hit twice: **#3/#10, zero test coverage** on the new brand-scoping logic
— the **third** occurrence of this exact shape this week on the
`admin-portal/handlers/` family (`ENG-013` round 1, `ENG-008` round 1, both
already logged as "not yet a third, waiting for one more"), crossing
`code-review-gate/SKILL.md` step 10's promotion threshold (flagged to
`observations.md` rather than actioned — the target file lives in the
read-only department tree). Line-level review then found a real,
independent authorization bug: `updateRestaurant` checks only the
restaurant's *existing* `brand_id` against the caller's owned brands, then
writes every other body field unfiltered via the service-role client (no
RLS backstop) — a partner can self-approve their own held-for-review
restaurant (`{approved: true}`, defeating this ticket's own AC5) or
reassign it to a brand they don't own (`{brand_id: ...}`). The build hop's
own PR-body claim that this can't happen was checked against the code and
is wrong. Full detail, both findings and independent verification:
`ENG-015`'s own board-file log, this date.

**0 transitions** — `state`/`owner` unchanged (`building`/`eng-manager`),
same precedent `ENG-008`/`ENG-013`'s own round-1 fails set. No receipt
written; QA's hop discarded, no test-plan file. Machine WIP unaffected,
still `ENG-015`'s own slot (1/1). Approver-facing WIP and approval cap both
unaffected — a review failure is not an approver-facing gate.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing raised — routes back to `building`, not the
approver. **Observations filed:** the third-occurrence standards-promotion
flag above, and, unrelated to this ticket's own diff, a noticed
discrepancy between `config/config.yaml`'s `wip.approver_limit: unlimited`
(raised 2026-09-02) and this board's own continued `8/2, over cap`
computation — flagged, not resolved, outside this event's own contract.

`chained: ENG-015` — `building` is agent-owned (round 1's two findings are
the next hop's own work), not the approver, not blocked, not terminal, not
held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-015`
before this pass exits. Post-pass `lib/eng-gate-check.sh`, scoped
(`ENG-015`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-015 (build): both repos, now `in-review`-bound

`continue` event pass, context `ENG-015` — this ticket's own turn at the
front of the queue, per the prior `scheduled` pass's own `chained:
ENG-015`. Narrow scope per the event's own contract — this ticket only.
Mode check clean (`MODE=active`). Gate check, scoped (`ENG-015`) and
whole-board: both exit 0, clean.

Branched both `aiorders-api` and `aiorders-admin-hub` fresh off
`origin/main` as `fix/ENG-015-agency-reseller-brand-scoping` (re-verified
no drift between what the design cited and the live `origin/main` files
before writing anything). Built exactly per the architect's design and
`ADR-006`: `restaurants.ts` brand-scopes `getRestaurants`/
`getRestaurantById`/`updateRestaurant` in code (service-role client,
explicit `brands.partner_id` filter/check — not RLS, per `ADR-006`'s own
reasoning); one new migration adds the partner `INSERT` policy, hard-held
for review (`approved = false`); `AddRestaurantModal.tsx` sends `approved:
false` for a partner caller so that policy doesn't reject every partner
add-location attempt outright. `deno check` clean; `aiorders-admin-hub`
lint/build clean (zero new issues — the four `any`/one missing-dep hits in
the touched file are pre-existing, confirmed shifted by exactly this
diff's own +2 lines). No live Postgres reachable this pass (narrower than
`ENG-007`/`ENG-011`/`ENG-013`'s own build passes — no read-only MCP
fallback available either); verified the design's/`ADR-006`'s schema
claims directly against tracked migrations instead, all confirmed still
accurate. Database receipt:
`agents/database/migrations/ENG-015-agency-reseller-brand-scoping.md`.

**Step 6b found and fixed one real staleness**: `proposals.md`'s
2026-08-29 row still named `updateRestaurant()` as open future work —
superseded by the 2026-08-31 design's own decision to fix it inside
`ENG-015`, now shipped this pass. Corrected in place (inline addendum,
cross-referenced against the fully-overlapping 2026-08-31 row) rather than
left to mislead the next batched G1. Full detail: `ENG-015`'s own board-file
log, this date.

Branches pushed, both repos: `aiorders-api@b6b3024`,
`aiorders-admin-hub@8c0db46`. No PR yet — devops's release-readiness step.

**1 transition** (`ready → building`). **Consequence:** no machine-WIP
change — `ENG-015` was already the sole occupant of the counted range.
Approver-facing WIP and approval cap both unaffected.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing to raise or nudge — `building` needs no
approver gate.

`chained: ENG-015` — `building` → combined review+QA hop next, owned by
`principal-engineer`/`qa`; not the approver, not blocked, not terminal,
not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-015`
before this pass exits. Post-pass `lib/eng-gate-check.sh`, scoped
(`ENG-015`) and whole-board: both exit 0, clean.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — scheduled (auto-drain): whole-board sweep, one live safety correction, next ticket dispatched

`scheduled` event pass, context `auto-drain` — fired by
`lib/eng-drain-poll.sh` (idle check confirmed: `traces/.loop.lock` absent,
`traces/.pending` held one stuck `watch launchd` entry). Never narrowed,
per this event's own contract — full document read, whole board swept.
Mode check clean (`MODE=active`). Pre-pass `eng-gate-check.sh`, whole-board:
exit 0, clean.

**Gate returns (step 4):** all eight items sitting in `inbox/` checked
fresh against their own frontmatter, not the board's prior narrative — all
eight still carry an empty `decision:` and an unfilled `## Decision`
section. Nothing answered; nothing to act on.

**Merge detection (step 5):** `git fetch` + ancestry on all five `blocked`
tickets, both repos where applicable (`ENG-008`, `ENG-009`, `ENG-010`,
`ENG-013`, `ENG-022`) — none merged, all correctly remain `blocked`.

**Sibling-branch staleness re-checked while merge detection was already in
the worktrees** (the standing gap `proposals.md`'s 2026-09-02
principal-engineer row names): `ENG-009` vs. `ENG-008`'s current tip —
still stale on both repos (`git merge-base --is-ancestor` false), same
fact `ENG-008`'s own round-3 review already found and logged onto
`ENG-009`'s ticket file earlier tonight. **What this pass added: that
finding had reached the ticket log but never reached
`inbox/2026-09-02-eng009-merge-request.md`** — the artifact the approver
actually reads — which still said `recommendation: merge` and promised a
clean merge. Checked real overlap, not just file adjacency:
`aiorders-api` side clean (no `accepts_barter` reference in `ENG-009`'s
diff); `aiorders-admin-hub` side carries the full pre-fix `accepts_barter`
UI verbatim, a real conflict once `ENG-008` merges. Corrected both
`ENG-009`'s merge request (`recommendation: → hold`, dated update section
with the repo-by-repo finding and a rebase recommendation) and `ENG-010`'s
(shorter cross-reference — its own diff doesn't touch the conflict, but it
inherits `ENG-009`'s branch wholesale). Deliberately not re-notified —
both items already spent their one `raise`, neither is past 24h, and
`eng-notify.sh`'s own budget is one raise plus one nudge, ever; the
correction lives in the files themselves. Full detail: `ENG-009`'s and
`ENG-010`'s own board-file logs, this date. One observation filed
(`observations.md`) naming the general shape — a logged cross-ticket
finding not propagating to an already-raised gate item — distinct from the
sibling-staleness gap itself. No new proposal — the standing one already
covers it.

**Dead-end sweep (step 8, whole board):** every one of the 27 tickets'
last `chained:` line checked against its own current `state:`/`owner:` —
all `none`, and all correctly so (terminal, blocked-on-approver,
awaiting-scope, or a paperwork state legitimately waiting on its own
G1/G2). `traces/eng-loop-2026-09-0{2,3}.log` grepped for `DROPPED` — zero
hits both days; no unhandled `*-eng-events-dropped.md` sitting in `inbox/`.
No broken chain found.

**Notify sweep (step 7):** all eight pending items' `notified:` timestamps
checked against current local time (these stamps are local wall-clock,
not true UTC — `proposals.md`, 2026-09-02 row) — the oldest
(`ENG-009`, raised 10:51) is ~14h40m elapsed, none past the 24h nudge
threshold. Nothing nudged.

**Dispatch (step 6):** machine WIP was `0/1`, free (`ENG-022` vacated it
this same pass-chain). Took the next candidate per priority/severity/id:
`ENG-015` (`designed → ready`, no G2 owed — `ADR-006` already covers the
risk call), tie-broken over `ENG-024` (same `P1`, same unset priority) by
lower id. Mechanical transition only — no code written, no branch cut;
`chained: ENG-015` fired for the build itself in a fresh session, per this
loop's own fresh-context-per-heavy-step design. Full detail: `ENG-015`'s
own board-file log, this date.

**Consequence:** machine WIP `0/1 → 1/1` (`ENG-015`). Approver-facing WIP
unchanged, `8/2`, still over cap — nothing this pass did was a new
approver-facing start. No approval cap exists to update (removed
2026-08-29).

`chained: ENG-015` — recorded on that ticket's own log; this pass's other
two touches (`ENG-009`, `ENG-010`) both stay `chained: none`, unchanged,
still `blocked`/`blocked_on: approver` — a gate-item correction is not a
state transition. Post-pass `eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-022 (release-readiness): PR opened, now `blocked` on the approver

`continue` event pass, context `ENG-022` — this fire's own turn at the front
of the queue, per the prior pass's own `chained: ENG-022`. Narrow scope per
the event's own contract — this ticket only. Mode check clean
(`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-022`) and
whole-board: both exit 0, clean.

Verified all three upstream gates fresh from the receipt files (code review,
quality, security — all `pass`; no migration applies, pure access-check
logic fix). Worktree confirmed clean but for the pre-existing untracked
`deno.lock`, on `fix/ENG-022-brand-portal-tenant-isolation@d5078c5`, 1 ahead
/ 0 behind `origin/main` — no drift. `gh pr list --search ENG-022` confirmed
no duplicate PR existed.

Project registered **L1** — step 1's window check doesn't apply. Step 3
readiness checks: rollback trivial (no migration, reverting the single
commit undoes the whole diff), observability already built into the fix
(A09 denial logging via `console.warn`, surfaced through Supabase's
existing function logs), cost **$0/month** (no new dependency or vendor).
Opened `aiorders-api` PR #9
(https://github.com/harsimranwalia/aiorders-api/pull/9) and raised the L1
merge request (`inbox/2026-09-03-eng022-merge-request.md`), notified
cleanly. Full detail, including the flagged `time_estimate:` field gap on
prior merge-request items: `ENG-022`'s own board file.

**1 transition** (`ready-to-ship → blocked`, `blocked_on: approver`,
`blocked_from: ready-to-ship`, owner `devops → approver`).
**Consequence:** machine WIP `1/1 → 0/1` (slot freed, not filled this
pass — narrow scope). Approver-facing WIP `7/2 → 8/2`, still over cap; not a
new start, so not gated by it (same precedent `ENG-008`/`ENG-009`/`ENG-010`
already set).

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** this pass's own item raised and stamped; nothing else to
nudge.

`chained: none` — `blocked`, `blocked_on: approver`. This is the human gate
the whole hop was driving toward; nothing left for a machine to do on this
ticket until the approver merges. Post-pass `lib/eng-gate-check.sh`, scoped
(`ENG-022`) and whole-board: both exit 0, clean.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-022 (security gate): PASS, now `ready-to-ship`

`continue` event pass, context `ENG-022` — this fire's own turn at the front
of the queue, per the prior pass's own `chained: ENG-022`. Narrow scope per
the event's own contract — this ticket only. Mode check clean
(`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-022`) and
whole-board: both exit 0, clean.

Re-derived everything from disk rather than trusted from the prior hops'
own accounts: worktree confirmed on `fix/ENG-022-brand-portal-tenant-isolation@d5078c5`,
no drift against `origin/main`; all six changed source diffs read directly;
`deno check`/`deno test` re-run fresh (10 pre-existing errors, 24/24 tests
passed, every one of the 19 negative cases confirmed individually by name).
OWASP A01–A10 walked — **zero blocking findings**. The load-bearing
architectural fact confirmed this pass: `brand-portal/index.ts` runs every
handler on a **service-role** client, so `verifyRestaurantAccess`/
`requireRestaurantAccess` is the *only* access control in this function, not
one layer among several — which is why the fix is sufficient on its own.
Two non-blocking findings, both pre-existing and outside this diff: a
verbose-error path in `verifyRestaurantAccess`'s own catch (same class
already three-struck on `ENG-009`, not re-proposed) and a scoping question
on the same function's admin/partner-role bypass (filed as a new proposal,
`agents/eng-manager/proposals.md`, 2026-09-03 row — not a confirmed defect).

Receipt written: `agents/security/reviews/ENG-022.md`. Full detail: that
file and `ENG-022`'s own board log.

**1 transition** (`in-qa → ready-to-ship`). **Consequence:** machine WIP
unaffected, still `1/1` (`ready-to-ship` is inside the counted range).
Approver-facing WIP and approval cap both unaffected — a security-gate pass
isn't a gate item to the approver.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing to raise or nudge from this action.

`chained: ENG-022` — `ready-to-ship`, owned by `devops` (release-readiness:
open the PR), an agent-owned state; not the approver, not blocked, not
terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-022`
before this pass exits. Post-pass `lib/eng-gate-check.sh`, scoped
(`ENG-022`) and whole-board: both exit 0, clean.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — continue ENG-022 (review + quality, combined hop, round 1): both PASS

`continue` event pass, context `ENG-022` — this ticket's own turn at the
front of the queue, per the prior pass's own `chained: ENG-022`. Narrow
scope per the event's own contract — this ticket only. Mode check clean
(`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped and whole-board:
both exit 0, clean.

Ran both gates fresh in one session (`config.yaml` → `combined_hop:
[code_review, quality]`) against `aiorders-api@d5078c5` — neither receipt
existed at pass start. **Code review: 0/10 automatic-failure items, PASS.**
Diff independently checked against the design's Approach/Interfaces
sections line by line, including confirming by direct read (not the
design's word) that `feedback.ts`/`customers.ts` have no local `try/catch`
(denial reaches `index.ts`'s top-level catch as a 500) while
`hiring.ts`/`website.ts` do (denial becomes `{success:false}` at 200),
exactly as the design describes. One non-blocking finding logged to the
notebook: `offers.ts`'s 8 call sites repeat an identical two-line denial
block a small helper could collapse — first occurrence, not blocking.

**Verified fresh rather than trusted from the build pass's own account:**
`deno check` on the 6 changed files (from `supabase/functions/brand-portal/`
— running from the repo root hits a byonm/node_modules resolution error,
now documented in the QA plan's `suite_command`): **10 errors, all
pre-existing**, independently re-derived line-for-line, not just
count-for-count. `deno test --no-check`: **24 passed, 0 failed**, matching
the build pass's claim exactly. **Executed a real mutation check** (not a
hand-trace): disabled the access check at one throw-convention site
(`customers.ts:73`) and one return-convention site (`offers.ts:80`), reran
both test files — exactly the two matching negative tests went red, every
other test in both files stayed green; reverted immediately after,
worktree confirmed clean again.

**QA: test plan written, PASS.** All 4 acceptance criteria covered; AC3
(legitimate access unchanged) deliberately sampled at one positive test per
file/code-path shape rather than per call site, reasoned explicitly in the
plan rather than left as an unexplained gap (every site in one file shares
the identical access-check substitution). No open P0/P1 bug on this board.
Full detail on both gates: `agents/principal-engineer/reviews/ENG-022.md`,
`agents/qa/test-plans/ENG-022.md`; `links.review`/`links.test_plan` set.

**2 transitions** (`building → in-review → in-qa`), well under the cap of
4. **Stopped at `in-qa` deliberately, not carried to `in-security` this
pass** — `sequential_after_quality: [security, release_readiness]` keeps
security a separate hop, since it needs QA's just-written plan to check
negative-authz coverage against. Same precedent this board's own `ENG-013`
round-2 review+quality pass set (2026-08-31). **Consequence:** machine WIP
unaffected, still `1/1` (`in-qa` is inside the counted range). Approver-facing
WIP and approval cap both unaffected — no gate touched.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing to raise — `in-qa` needs no approver gate.
Nothing to nudge.

`chained: ENG-022` — `in-qa`, owned by `qa` (security next), an agent-owned
state; not the approver, not blocked, not terminal, not held by a cap.
Fired `/bin/zsh departments/engineering/lib/eng-trigger.sh continue
ENG-022` before this pass exits. Post-pass `lib/eng-gate-check.sh`, scoped
(`ENG-022`) and whole-board: see below.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

---

## 2026-09-03 — continue ENG-022 (build): fix built, tested, committed and pushed — single-repo, no PR yet

`continue` event pass, context `ENG-022` — this ticket's own turn at the
front of the queue, per the prior sweep's own `chained: ENG-022`. Narrow
scope per the event's own contract — this ticket only. Mode check clean
(`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, whole-board: exit 0,
clean.

Built exactly per the architect's design in `aiorders-api`
(`fix/ENG-022-brand-portal-tenant-isolation`, off `origin/main`, no
cross-ticket branch dependency): promoted the dead
`verifyRestaurantAccessLegacy` to `requireRestaurantAccess` for the 4
throw-convention files (11 call sites), fixed `offers.ts` in place (8 call
sites, matching its own correct siblings), added the A09 denial log on both
paths (the offers.ts half is one line beyond the design's literal text —
flagged in the ticket's own log, not silently added). 24 new `Deno.test`
cases (19 negative — one per call site — plus 5 positive, proving the test
stub isn't just failing everything): **24 passed, 0 failed**. `deno check`
on the six changed files: 19 pre-existing errors → 10, all nine eliminated
being the exact wrong-argument-order bug surfacing as `TS2345` — confirmed
against the original tree via `git stash` before attributing any of it, not
assumed. Committed (`aiorders-api@d5078c5`) and pushed; no PR opened yet —
devops's own release-readiness hop, same precedent `ENG-008`/`ENG-009`/
`ENG-010` each set. Full account, PR body draft, and the two flagged
deviations (test-file naming, offers.ts's extra log line): the ticket's own
board file.

**1 transition** (`ready → building`). **Consequence:** machine WIP
unaffected (`1/1`, `building` still inside the counted range). Approver-facing
WIP and approval cap both unaffected — no gate touched.

**Dead-end sweep, notify sweep:** nothing else to resume or raise from this
scoped event. **Observations filed** (`observations.md`, 2 rows): a
`deno.lock` generated by this pass's own self-test, deliberately left
uncommitted (a repo-wide tooling decision this ticket shouldn't make
unilaterally); and the `TS2345`-was-the-bug finding, concrete evidence for
the already-known no-CI-wiring gap in `config/projects.md` (not
re-proposed).

`chained: ENG-022` — `building`, owned by `backend`, an agent-owned state;
its own next hop (review + quality, combined) belongs in a dedicated
session, not this one. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-022`
before this pass exits. Post-pass `lib/eng-gate-check.sh`, scoped
(`ENG-022`) and whole-board: see below.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-03 — scheduled sweep (manual-drain): a stale gate item archived, a real ticket-id collision found and fixed, ENG-022 (P0) dispatched after a 5-day wait

`scheduled` event pass, context `manual-drain` — a second manual fire the
same night as the `manual` sweep directly below, drained by the same
still-running orchestrator (`eng-trigger.sh`, alive since ~22:00). Full
whole-board sweep per the reading map's own instruction that `scheduled`
is never narrowed. Mode check clean (`MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Business/technical intake.** `agents/product-manager/inbox/` and
`agents/eng-manager/inbox/` both empty but for `.gitkeep`/`_handled`/
`_processed`; nothing new since the prior pass.

**Gate returns.** Re-read all `inbox/*.md` fresh rather than trusted from
the board. Seven items are genuinely still unanswered (`ENG-008`/`ENG-009`/
`ENG-010` merge requests, `ENG-013` stage-config question, `ENG-016`
rescope G1, `ENG-026` G1, `ENG-027` G1) — matches the prior pass exactly,
nothing changed in the few minutes between. **One item wasn't**:
`inbox/2026-08-29-eng016-g1-scope.md` still carried `decision: changed`
from the prior pass's own processing (PRD rewrite, rescope G1 raised,
decision-journal row 51) but was never moved to `_handled/` — confirmed
fully processed (cross-checked the journal row and `ENG-016`'s own board
log, not re-derived) before archiving it now. A processed-but-unarchived
gate item reads identically to an unanswered one to every later sweep, so
this was worth the two-minute check rather than skipping it.

**Merge detection.** Fresh `git fetch` + ancestry check, both repos, all
three branches (`ENG-008`/`ENG-009`/`ENG-010`) — still unmerged, no change
since the prior pass's `gh pr view` minutes earlier. `ENG-013` has no open
PR (blocked on a question), not applicable.

**Dead-end sweep — one real finding.** `ENG-026` had two live board files
answering to the same `id: ENG-026`: the current, gated ticket
(`ENG-026-foodswipe-channel-visibility.md`) and a pre-rescope original
(`ENG-026-foodswipe-multichannel-filters-and-promo-engine.md`, frozen at
`intake` since 2026-09-01) that the 2026-09-02 rescope should have edited
in place — the way `ENG-016`'s own rescope the same night did — but
instead left orphaned with an unresolved `priority: now` stamp
(commit `a862607`) never carried to the surviving file.
`lib/eng-gate-check.sh` has no id-uniqueness check (confirmed by reading
it), so nothing mechanical would have caught this. Retired the orphaned
file: content folded into the live ticket's own log, full original kept in
git history, `priority: now` flagged unresolved rather than guessed at or
silently dropped — see `ENG-026`'s own 2026-09-03 log entry for the full
account. Observation and a proposal filed (id-uniqueness check for
`eng-gate-check.sh`; write down the "rescope in place, same file/id" rule
explicitly). No other broken chains, no `*-eng-events-dropped.md` files
outside `_handled/`, no incident items outstanding.

**Dispatch — the pass's main action.** Re-derived machine WIP from each
blocked ticket's own frontmatter rather than the header: `ENG-008`/
`ENG-009`/`ENG-010`/`ENG-013` all `blocked`. **0/1, genuinely free**, and
had been since the prior sweep. Checked every `designed`/`shaped` ticket
for whether it's actually gate-clear rather than assuming only the
obvious candidate is: `ENG-022` (P0, `type: security`, G1 auto-skipped,
no G2 — no one-way door), `ENG-015` (P1, same shape, decided-not-escalated
per `ADR-006`), and `ENG-024` (P1, fast lane, `type: bug`, G1
auto-skipped) are all gate-clear; every other candidate still owes an
unraised G1 or G2. Priority unset on all three, so severity decided it:
`ENG-022` (`P0` — live, currently-reachable cross-tenant PII exposure plus
unauthorized writes, waiting on this slot alone since 2026-08-29) over
`ENG-015`/`ENG-024` (both `P1`). Dispatched `ENG-022` `designed → ready`.
Full reasoning, file-level sequencing check, and the next-in-line note:
`ENG-022`'s own board file and this file's header, above.

**Notify sweep.** No new gate item raised this pass (the dispatch needed
neither G1 nor G2). Checked all seven open items against 24h/nudge —
none due yet, matching the prior pass's own check minutes earlier.

**Board update.** Rolled the oldest of four dated entries
(`2026-09-02 — continue ENG-008 (security gate, round 3)`) to
`_index-archive.md`, keeping three live, per the keep-three rule.

**0 gate items touched this pass; 1 ticket dispatched.** Machine WIP
`0/1 → 1/1` (`ENG-022`). Approver-facing WIP unaffected, still `7/2` —
archiving an already-answered item doesn't change a live count.

`chained: ENG-022` — `ready`, owned by `eng-manager`, an agent-owned state;
its own next hop is new implementation work and belongs in a dedicated
session, not this sweep. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-022`
before this pass exits. Post-pass `lib/eng-gate-check.sh`, whole-board: see
below.

business-os itself left uncommitted — same standing default every pass
tonight has used; the commit-convention question remains open, not
re-decided here.

## 2026-09-03 — scheduled sweep (manual): both deferred gate-return items processed, six PRs re-confirmed unmerged, nothing else broken

`scheduled` event pass, context `manual`. Mode check clean (`MODE=active`).
Pre-pass `lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Gate returns, oldest first, per the loop's own discipline** — the two
items the prior `watch` sweep deliberately left for a pass with room to do
them justice:

**`ENG-016`'s G1** (`changed`, decided 2026-09-03T00:53:17Z) carried a
complete replacement engineering spec, not an edit — reintroducing the
catering-specific tiered pricing model and owner-side quote editing the
original PRD named as non-goals, plus a three-stage pipeline matrix whose
own enum-update instruction named only two of the three. Gathered fresh
codebase evidence (`sonnet` subagent) before delegating the sizing/filter/
PRD judgment to an `opus` subagent per `prd-writer/SKILL.md`'s own model
designation — kept the two apart deliberately, fact-finding doesn't need
opus. **Verdict: `XL`, not `L`** — the rewrite deletes the original's
SMS/email link entirely (moves the selector onto the public page, which is
also why the literal `Quote Viewed` stage is unbuildable — no link, no
token, nothing to attach a "viewed" event to before a submission creates a
record), and the five-stage board is hardcoded across eight files, not
three. Split per `prd-writer/SKILL.md` step 7: `L`-sized Piece 1 (structured
order capture, itemized owner view, two automatic stages, no pricing)
rescoped onto this ticket, fresh G1 raised
(`inbox/2026-09-02-eng016-g1-rescope.md`); Piece 2 (package/price-book,
depends on Piece 1) and Piece 3 (owner edit/resend + view tracking,
depends on 1–2) named in the PRD's Recommendation, **not filed** — the
approver hasn't seen the split yet, and Piece 2 explicitly waits on a named
answer (who maintains each restaurant's price book). Stage inconsistency
resolved as a rider (building the two stages the reply's own enum
instruction names; `Quote Viewed` moves to Piece 3), not a blocking
question — evidence-resolvable, not a coin flip, so it doesn't meet this
board's bar for asking (`ENG-013`'s precedent). PRD rewritten in place,
original Readback/Evidence kept as history. Decision-journal entry written.

**`ENG-007`'s continue-sequence-question** (`approved`/"yes", decided
2026-09-01T17:02:39Z) named ticket 3 of `ENG-006`'s approved five-ticket
loyalty sequence — points ledger, balances, and earn API. No fresh
readback run: the scope was already precisely named in `ENG-006`'s own
approved PRD, so there was no raw ambiguity to interpret. Delegated to an
`opus` subagent, grounded in `ENG-007`'s shipped schema/branch convention
and live `aiorders-api` code. Filed as **`ENG-027`**, sized `M` (not `L` —
reuses the CloudWaitress order webhook, `brand-portal`'s existing
restaurant-scoped auth gate, and `ENG-007`'s own rate lookup; no new
subsystem). Confirmed via code, not assumed: no order-completion signal
exists anywhere in the system (only `order_new`, no update/delete path),
so accrual is scoped to order *placement* with the fulfilment-signal gap
named as a risk; the Walletly loyalty vendor stores nothing locally (a pure
proxy), so migrating existing balances is out of scope and flagged as
time-sensitive before the vendor contract lapses. G1 raised
(`inbox/2026-09-03-eng027-g1-scope.md`) with a rider on what the earn-%
base should be (proposed: pre-tax, post-discount food subtotal) and an
explicit note that `ENG-022` (P0, live cross-tenant PII/write exposure)
outranks this if the approver's attention is scarce. `next_id` incremented
`ENG-027 → ENG-028`. Decision-journal entry written.

**Both G1s skip step 8b (dissent) the same way, logged rather than
silently dropped** — `agents/critic/agent.md` still doesn't exist at
department or instance level, same gap `ENG-017`'s G1 already carried;
the open proposal (`proposals.md`, 2026-08-25) already covers it, not
refiled.

**Merge detection.** `gh pr view` on all six PRs across both repos
(`aiorders-api` #6/#7/#8, `aiorders-admin-hub` #5/#6/#7 — `ENG-008`,
`ENG-009`, `ENG-010`): all six still `OPEN`, `mergedAt: null`. No change
since the prior pass's own check minutes earlier. `ENG-013` has no open PR
(blocked on a question, not a merge) — not applicable.

**Dead-end / broken-chain sweep, whole board.** Every in-flight ticket is
either correctly `blocked`/`blocked_on: approver` (`ENG-008`, `ENG-009`,
`ENG-010`, `ENG-013`) or correctly resting in backlog grooming
(`shaped`/`designed`/`awaiting-scope`, outside the machine-WIP-gated
range) — no ticket sitting in an agent-owned working state with a missing
or unjustified `chained:` line. `_handled/` and today's notify logs show
no unresolved incident files. Machine WIP stays `0/1`, free — no dispatch
from To-do this pass: the one priority-`next` candidate (`ENG-016`) was
itself the ticket being reshaped, not ready to advance, and every other
To-do-column ticket needing a fresh G1/G2 stays held behind the WIP-2 cap
per Guards ("at the limit, nothing new starts that will need them").

**Notify sweep.** Both new G1s raised and stamped
(`traces/eng-notify-2026-09-02.log` 23:51:27, `traces/eng-notify-2026-09-03.log`
00:03:51). Checked fresh: `ENG-009` and `ENG-010`'s merge requests both
still under 24h, not due; nothing else newly due.

**Observations/proposals filed:** none new — both known gaps this pass hit
(`agents/critic/agent.md` missing; the business-os commit-convention
question) already have open, unresolved entries from prior passes; not
duplicated.

**WIP.** Machine WIP unaffected, `0/1`. Approver-facing WIP `5/2 → 7/2`,
still over cap — `ENG-016` (rescope G1) and `ENG-027` (new G1) both rejoin/
join the count; neither is a fresh To-do-column start (the sequence's own
approved continuation, and a ticket's own gate cycle continuing), so
neither was held behind the cap being over, same precedent
`ENG-008`/`ENG-009`/`ENG-010` already set tonight.

`chained: none` for both `ENG-016` and `ENG-027` — both `awaiting-scope`,
owned by the approver; the chaining guard doesn't fire on a ticket waiting
on a human. No other ticket was touched this pass. Post-pass
`lib/eng-gate-check.sh`, whole-board: exit 0, clean, no `WAIVED:` lines.

business-os itself left uncommitted — same standing default the whole
2026-09-02 chain of passes used; per the correction already on record two
entries above, no verified approver decision on this convention exists on
disk, and this pass isn't re-asserting that it does. Not re-raised as a
fresh question here either: out of a `scheduled` sweep's own scope, and
not a P0.

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

---

## 2026-09-02 — scheduled sweep (20:30): whole-board re-check, nothing new

`scheduled` event pass, context `launchd` — the four-times-daily safety net,
drained immediately behind the watch sweep above (`traces/eng-loop-2026-09-02.log`:
`pass end: watch (exit 0, 477s)` at `18:00:18` → `draining queued event:
scheduled (launchd)` at `20:30:06`, no gap, nothing else queued in between).
`traces/.pending` reads empty, drained for this launch. Mode check clean
(`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

**Business/technical intake:** `agents/product-manager/inbox/` and
`agents/eng-manager/inbox/` hold only their `_handled`/`_processed`
archives; `inbox/requests/` holds only `.gitkeep`. Nothing new on either
intake path.

**Gate returns:** all eleven loose `inbox/` items re-read individually by
frontmatter. The four `gate: incident` items still carry no `decision:`
field — closed notices, nothing to do. Of the seven `decision:`-bearing
items, all still show `decision:` blank: `ENG-016`'s G1, `ENG-007`'s
continue-sequence question, `ENG-008`'s/`ENG-013`'s merge requests, and
`ENG-026`'s readback question have each already spent their one nudge;
`ENG-009`'s merge request (`notified: 10:51:07`) is ~9h39 old, still under
the 24h threshold; `ENG-010`'s (`notified: 17:45:02`) is ~2h45 old. Nothing
newly due for a nudge.

**Merge detection** (this pass's own job — last run at 15:30, ~5h stale):
fetched both `aiorders-api` and `aiorders-admin-hub` fresh from
`~/Documents/projects/_eng/` and checked `--is-ancestor` against
`origin/main` for all four blocked-on-approver tickets — by the ticket
log's own recorded commit where one exists, by branch tip otherwise:
`ENG-008` (`57f8c4b`/`63be255`), `ENG-009` (`d37e0c9`/`92bcacd`), `ENG-010`
(`486eec0`/`8b90f0e`), and `ENG-013` (branch tip both repos, no per-commit
record in its own file). All eight checks: **NOT-MERGED**. No state
change — all four stay `blocked`/`blocked_on: approver`.

**Dispatch:** machine WIP `0/1`, free; approver-facing WIP `5/2`, over cap.
Per the Guards section, nothing new starts while the approver cap is over —
every path off the To-do column (`ENG-014`/`015`/`017`/`022`/`023`/`025` at
`designed`, `ENG-018`–`021`/`024` at `shaped`, `ENG-016` at
`awaiting-scope`) reaches the approver at G1 or G2 within one hop, so
starting any of them now would only add to an already-over-cap queue. No
new start made.

**Dead-end sweep:** chain intact across all three prior passes tonight —
the security-gate pass's `chained: ENG-010` was honored by the
release-readiness pass (correctly `chained: none`, `blocked_on: approver`),
and the watch sweep after it correctly recorded `chained: none` (nothing in
its scope). No ticket sits in an agent-owned state without a valid chain
record. No merge-blocked ticket past its 3-day resurface threshold.

One small fix made in passing, in this same file, while rolling the archive
below: `Next ID: ENG-026` was stale — `ENG-026` has itself been an
allocated ticket on this board since earlier today — corrected to
`ENG-027`. Filed as an observation, not a proposal.

**0 ticket-state transitions.** No new proposals — every named gap already
tracked. Rolled the `continue ENG-010 (security gate)` entry to archive,
keeping the live board's cap of three.

`chained: none` — no ticket in this pass's scope was touched or unblocked;
this pass only re-verified that what already looked settled is in fact
settled. Post-pass `lib/eng-gate-check.sh`, whole-board: exit 0, clean, no
`WAIVED:` lines.

## 2026-09-02 — watch sweep (~17:52): self-triggered by ENG-010's own merge-request write, nothing new

`watch` event pass, context `launchd` — drained immediately behind the
release-readiness pass's own exit (`pass end: continue (exit 0, 748s)` at
`17:52:19`, per `traces/eng-loop-2026-09-02.log`). Narrow scope per this
event's own contract: sweep the three watched inboxes only, act on what's
new, ignore what's already processed.

Mode check clean (`MODE=active`, repo-root `.env`; instance
`config/config.yaml` → `mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

**Traced this fire to its source before treating it as new.** The log shows
two fires one minute apart while the release-readiness pass was still
running — `[17:44:59] watch — pass in flight, queued as pending` and
`[17:45:59] watch — pass in flight, queued as pending` — collapsed to one
duplicate at drain time (`queue: collapsed 1 duplicate event(s)`). Both land
inside the same minute that pass raised `ENG-010`'s own merge request:
`traces/eng-notify-2026-09-02.log` records `[17:45:02] sent:` for
`inbox/2026-09-02-eng010-merge-request.md`, and that file's own
`notified: 2026-09-02T17:45:02` stamp was written by the same hop. Checked
every other file in all three watched inboxes for a competing candidate: none
carries a mtime anywhere near this window — the next-newest is
`inbox/2026-09-02-eng009-merge-request.md` from `~10:51`. No other candidate
exists; both fires are this ticket's own write (the create, and the
notified-stamp edit a moment later), not an external arrival.

**All three inboxes swept anyway, not trusted from the paragraph above.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
their `_handled`/`_processed` archives — nothing loose. `inbox/requests/`
holds only its `.gitkeep`. `inbox/`'s eleven loose items, each re-checked
individually by frontmatter, not by filename:

- The four `gate: incident` items (`2026-08-30-eng-loop-halted`,
  `2026-08-30-eng-events-dropped`, `2026-08-31-eng-events-dropped`,
  `2026-09-01-eng-gate-violation-watch`) carry no `decision:` field at all —
  still closed notices, nothing to do.
- The seven `decision:`-bearing items (`ENG-007` continue-sequence question,
  `ENG-008`/`ENG-013`/`ENG-009`/`ENG-010` merge requests, `ENG-016` G1,
  `ENG-026` readback question) all still show `decision:` blank. Nudge status
  checked fresh against each item's own `notified:`/`nudged:` pair: `ENG-016`,
  `ENG-007`, `ENG-008`, `ENG-013`, and `ENG-026` have each already spent their
  one nudge; `ENG-009` (`notified: 10:51:07`) is ~7h old, under the 24h
  threshold; `ENG-010` (`notified: 17:45:02`) is 0h old. Nothing newly due.

**No merge detection re-run.** Out of this event's own scope — merge
detection is the `scheduled` pass's job, next due 20:30 — and nothing found
in this sweep argues for doing it anyway: no gate item was answered, no
external notice arrived, and the release-readiness hop that just ended
independently re-confirmed `ENG-009`'s own PRs still open (`gh pr list
--state all`, as part of its own base-branch check) minutes before this fire.
The whole-board check at 15:30 (`ENG-008`/`ENG-013` unmerged) is now ~2h25m
old rather than minutes, so this is a scope call, not a claim that nothing
could have changed in that window — the 20:30 sweep is what actually re-checks
it board-wide.

**No dispatch, no chaining.** Nothing in this pass's scope was newly
unblocked, and no ticket was touched: `ENG-010`'s release-readiness and its
`chained: none` were the prior pass's own action, already recorded on its own
board file. Machine WIP unchanged (0/1, empty since `ENG-010` left `ready` for
`blocked`); approver-facing WIP unchanged (5/2, over cap, already named
above).

**0 ticket-state transitions.** No new observations, no new proposals —
nothing surfaced that isn't already tracked. Rolled the `continue ENG-010
(round 3)` entry to archive, keeping the live board's cap of three.

`chained: none` — no ticket in this pass's scope was touched or unblocked;
this pass only confirmed that what already looked settled is in fact
settled. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board: exit 0, clean, no `WAIVED:` lines.

## 2026-09-02 — continue ENG-010 (release-readiness): both PRs opened, now blocked on the approver

`continue` event pass, context `ENG-010` — the chain fired by the
security-gate pass above, drained by the same orchestrating process
(`ps -p 17776`) every hop this evening has cited; confirmed this session is
that queued fire by walking its own process ancestry back through
`run-claude.sh` → `eng-trigger.sh continue ENG-010` → `eng-trigger.sh
scheduled launchd` (17776) → `eng-loop-all.sh` → `launchd`. Narrow scope per
the event's own contract. Mode check clean (`MODE=active`). Pre-pass
gate-check, scoped and whole-board: both exit 0, clean. Hop count 8/20
(department daily 18/200).

Both projects registered **L1** — step 1's window check does not apply.
Verified all four upstream gates fresh from the receipt files themselves
(migration pass + RLS addendum, code review pass round 3, quality pass,
security pass). Worktrees clean, already on this ticket's own branch at the
commits its frontmatter records; no PR pre-existed. Re-confirmed the
base-branch choice fresh: `ENG-009`'s tip is still the exact merge-base on
both repos and its own two PRs are still open, so opened both of `ENG-010`'s
PRs against `feat/ENG-009-influencer-engagement-info` rather than `main`,
same reasoning `ENG-009`'s own hop applied against `ENG-008`. Step 3
readiness checks (rollback theorised-not-tested, observability via existing
`console.error`/toast, $0/month cost, window n/a) — same interpretation this
board already established for `ENG-007`/`ENG-008`/`ENG-009`/`ENG-013`.

**Opened both PRs**: `aiorders-api` #8
(https://github.com/harsimranwalia/aiorders-api/pull/8), `aiorders-admin-hub`
#7 (https://github.com/harsimranwalia/aiorders-admin-hub/pull/7), each
verified via `gh pr view` immediately after. Wrote the L1 merge-request item
(`inbox/2026-09-02-eng010-merge-request.md`, `pr_urls:` as a YAML list of
both repos), ran `lib/eng-notify.sh raise` (sent cleanly, `traces/
eng-notify-2026-09-02.log`: `[17:45:02] sent: active`), stamped `notified:
2026-09-02T17:45:02`. Cap check: approver-facing WIP was already `4/2`, over
cap, going in — same precedent `ENG-008`'s/`ENG-009`'s own release-readiness
hops already set (the cap gates a new start, not a ticket finishing its
required, non-discretionary L1 conclusion); not treated as a reason to hold.
Full trace: `ENG-010`'s own board file, this dated entry.

**1 transition** (`ready-to-ship → blocked`). **Consequence:** machine WIP
`1/1 → 0/1` (`ENG-010` was the sole occupant; the range is now empty —
whether a new ticket starts is not decided by this event-scoped pass).
Approver-facing WIP `4/2 → 5/2`. Dead-end sweep (scoped): nothing else on
this ticket's own lineage to resume; `traces/.pending` holds one queued
`watch` fire (arrived while this pass was already running) — out of this
event's own scope, not manually processed, drains on the next fire of any
kind. Notify sweep: this pass's own item raised and stamped above; nothing
else newly eligible to nudge. No new proposals — every named gap is already
tracked elsewhere. One observation filed: `release-runner/SKILL.md`'s own
`traces/devops-{run-id}.json` output has never actually been written on
this instance, on any of the three release-readiness hops run so far.

`chained: none` — `blocked`, `blocked_on: approver`. This is the human gate
the whole hop was driving toward, same precedent `ENG-008`'s and `ENG-009`'s
own release-readiness entries already set at this identical state. Post-pass
gate-check, scoped (`ENG-010`) and whole-board: both exit 0, clean, no
`WAIVED:` lines.

## 2026-09-02 — continue ENG-010 (security gate): PASS — in-qa → in-security → ready-to-ship

`continue` event pass, context `ENG-010` — the chain fired by round 3 above.
Confirmed this session is that queued fire by walking its own process
ancestry (`claude -p` → `run-claude.sh` → `eng-trigger.sh continue ENG-010`
→ `eng-trigger.sh scheduled launchd` (17776, same PID every hop tonight has
cited) → `eng-loop-all.sh` → `launchd`); `traces/.pending` reads empty,
drained for this launch. Narrow scope per the event's own contract. Mode
check clean (`MODE=active`). Pre-pass gate-check, scoped and whole-board:
both exit 0, clean. Hop count 7/20 coming in (department daily 17/200) —
checked against `lib/eng-trigger.sh`'s actual `read_plan_budget()`
resolution, not a department-config comment that mirrors the wrong tier (see
Observations below).

Independently re-verified all five prior uncommitted hops on this ticket
against the live repos before relying on any of them (both worktrees
fetched and re-diffed from disk, `deno test` re-run, `hasInfluencerAdminAccess`,
the router allowlist, the service-role client construction, the RLS
migration, and both its cited precedents all read directly) — everything
matched the ticket log's own account exactly. Full threat model, OWASP walk
(0/10 blocking), negative-auth cases, secrets scan, and SOC 2 trail:
`agents/security/reviews/ENG-010.md` (first receipt on this ticket).
Two non-blocking findings, neither introduced by this ticket: the
already-tracked verbose-`error.message` pattern (4th/5th occurrence, not
re-proposed — an open proposal already covers it) and a repo-wide CORS
wildcard on every admin-portal handler (named explicitly for the first time,
low severity under this app's bearer-token auth model). `links.security_review`
set. Full trace: `ENG-010`'s own board file, this dated entry.

**2 transitions** (`in-qa → in-security → ready-to-ship`), within the cap of
4. Machine WIP unaffected (1/1, still `ENG-010`'s slot — frees only once
devops's own release-readiness hop moves it to `blocked`). Approver-facing
WIP and cap unaffected. Dead-end sweep: all three inboxes checked, nothing
new against `ENG-010`. **2 observations filed**: a stale department-config
comment (`config.yaml` lines 488–489 mirror the `pro` tier's hop ceilings,
not the live `max_5x` ones `plan.tier` actually resolves to — zero runtime
effect, confirmed by reading `read_plan_budget()` directly, but a real
comment-vs-code drift); and this six-consecutive-pass business-os commit gap
continuing unresolved (`[[project-buildloop-instance-repo-commit-gap]]`,
not re-asked to the approver a second time).

`chained: ENG-010` — `ready-to-ship` is agent-owned (release readiness is
next, its own dedicated session per this loop's design), not the approver,
not blocked, not terminal, not held by a cap. Firing
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-010`
before this pass exits. Post-pass gate-check, scoped and whole-board: both
exit 0, clean, no `WAIVED:` lines.

**Fire landed as queued, not launched** — same orchestrating process as
every hop this evening (`ps -p 17776`: alive, ~110 minutes elapsed, lock
never released), confirmed via the trace log and `.pending` (`1 continue
ENG-010`) rather than assumed; not re-fired manually, to avoid racing the
same lock.

## 2026-09-02 — continue ENG-010 (round 3): code review + quality gate PASS — building → in-review → in-qa

`continue` event pass, context `ENG-010` — the chain fired by fix-hop-2
above, drained by the same orchestrating process (`ps -p 17776`) every hop
this evening has cited; confirmed this session is that queued fire rather
than a second concurrent one by walking its own process ancestry back
through `run-claude.sh` → `eng-trigger.sh continue` → `eng-trigger.sh
scheduled launchd` (17776) → `eng-loop-all.sh` → `launchd`. Narrow scope
per the event's own contract. Mode check clean (`MODE=active`). Pre-pass
gate-check, scoped and whole-board: both exit 0, clean. Hop count 6/20.

Re-derived the full cumulative diff (all three commits, not just the delta
since round 2). Both prior fixes re-verified independently and confirmed
correct: round 1's `useRef` guard traced through its full lifecycle; round
2's RLS policy checked one level deeper than before — the same
`EXISTS`-against-`profiles` shape already gates `restaurants` and
`catering` in this project's foundational RLS migration, so it's the
codebase's established pattern, not a one-off precedent trusted twice.
Automatic-failure scan 0/10. A fresh scan for new issues (not just the
delta) found only pre-existing, non-blocking items — a repo-wide RLS
pattern gap (checks `role`, not `additional_roles`, true of every admin
RLS policy in this repo, not new here), the already-tracked verbose-
error-response pattern (named for security's own count, not re-filed), and
two minor UX gaps in the same already-accepted class round 1 named. None
rise to a third fail. All 4 acceptance criteria covered. Verified
independently: 16/16 new tests, 34/34 sibling, whole-tree `deno check` 17
pre-existing errors (zero new), lint 150/31 baseline (zero new on the
touched file), build clean — matching every prior hop's own numbers
exactly. Full findings: `agents/principal-engineer/reviews/ENG-010.md`
(first receipt on this ticket) and `agents/qa/test-plans/ENG-010.md`
(also first); `links.review`/`links.test_plan` set. No open P0/P1 bug.
Full trace: `ENG-010`'s own board file, this dated entry.

**2 transitions** (`building → in-review → in-qa`), within the cap of 4.
Machine WIP unaffected (1/1, still `ENG-010`'s slot). Approver-facing WIP
and cap unaffected. Dead-end sweep: all three inboxes checked, nothing new
against `ENG-010`. No new observation/proposal filed.

`chained: ENG-010` — `in-qa` is agent-owned (security is next, needs this
round's own test plan), not the approver, not blocked, not terminal, not
held by a cap. Firing
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-010`
before this pass exits. Post-pass gate-check, scoped and whole-board: both
exit 0, clean, no `WAIVED:` lines.

## 2026-09-02 — continue ENG-010 (fix hop 2): round 2's missing-RLS gap closed, chained for review round 3

`continue` event pass, context `ENG-010` — the chain fired by the round-2-FAIL
pass above, drained once the 15:30 `scheduled` sweep's orchestrating process
(`ps -p 17776`) released the single-flight lock: `traces/
eng-loop-2026-09-02.log` records `draining queued event: continue (ENG-010)`
then `pass start: continue (ENG-010) [... ENG-010 5/20]`, well inside the
per-ticket ceiling. Narrow scope per this event's own contract (this ticket
only; no board-wide sweep). Mode check clean (`MODE=active`, repo-root
`.env`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-010`) and whole-board: both exit 0, clean, no `WAIVED:` lines.
`aiorders-api` worktree fetched, confirmed clean and at `d79d963` (matching
this ticket's own frontmatter) before touching anything; `aiorders-admin-hub`
untouched — the finding was migration-only.

Added the fix round 2 named to `supabase/migrations/
20260902120000_create_influencer_notes.sql`: `alter table influencer_notes
enable row level security`, then a `for all` policy scoped to
`profiles.role in ('admin', 'sub-admin')` for both `using` and `with check`
— the exact shape the review cited from the existing `proxy_sessions`
precedent, matched to this file's own lowercase statement style. Changes
nothing about the shipped feature's runtime behavior (the handler's
service-role client still bypasses RLS regardless) — it only closes the
direct-PostgREST path the design, the migration gate, and round 1's review
all missed. Also added an Addendum section to the migration doc
(`agents/database/migrations/ENG-010-influencer-relationship-notes.md`)
recording the gap and the fix rather than leaving its original "no RLS
policy changed" verdict standing unexplained next to a table that now has
one. Left the architect design doc's own illustrative SQL snippet untouched
— a pre-implementation sketch, not a producer instruction this fix
contradicts, and no precedent on this board retroactively patches a design
doc for an implementation-stage fix. No Supabase MCP tool available this
session either (checked via `ToolSearch`); not re-filed as a second
observation, since the build hop already filed this exact absence once.

**Verified independently:** `deno check` clean; `deno test --allow-net
influencer-notes.test.ts` — **16 passed, 0 failed**, matching every prior
hop exactly; `deno test influencers.test.ts` (sibling) — **34 passed, 0
failed**; whole-tree `deno check handlers/*.ts` — **17 errors**, same count
and same three pre-existing files every prior ticket on this board has
recorded, zero new. No live Postgres reachable from this host (no `docker`,
`psql`, or `supabase` CLI) — the new `alter table`/`create policy`
statements have not been executed anywhere, named rather than assumed
passing, same standing gap the migration doc already carried.

Committed `aiorders-api@486eec0` ("Enable RLS on influencer_notes
(ENG-010)"), pushed to the existing branch (no rebase needed). Full trace,
the exact SQL, and the migration-doc addendum: `ENG-010`'s own board file,
this dated entry.

**0 net transitions** — `state`/`owner` unchanged (`building`/
`eng-manager`); `building → in-review` is the next (review + quality) hop's
own write. Machine WIP unaffected (1/1, `ENG-010` sole occupant).
Approver-facing WIP and cap unaffected — no gate touched this hop.

**Dead-end sweep (scoped to this event):** nothing else on this ticket's
own lineage to resume. **Notify sweep:** nothing to raise (a fix hop doesn't
notify); nothing to nudge. **No new observation filed** — both the RLS
pattern and the missing-MCP-tool gap were already filed by the round-2-FAIL
and build-hop entries respectively.

`chained: ENG-010` — `building` is agent-owned (review + quality round 3 is
the next hop's work), not the approver, not blocked, not terminal, not held
by a cap. Firing
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-010`
before this pass exits. Every other in-flight ticket is unchanged from the
round-2 entry above. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-010`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

**Fire landed as queued, not launched** — same orchestrating process as the
last two hops (`ps -p 17776`: alive, `eng-trigger.sh scheduled launchd`, now
~89 minutes elapsed — it has held the single-flight lock across the build
hop, both review rounds, and both fix hops without releasing it), confirmed
via the trace log and `.pending` (`1 continue ENG-010`) rather than assumed;
not re-fired manually, to avoid racing the same lock.

## 2026-09-02 — continue ENG-010 (round 2): code review FAIL — the new table has no row-level security, routed back to building

`continue` event pass, context `ENG-010` — the chain fired by the fix-hop
pass above. Narrow scope per this event's own contract (resume this ticket
only; no board-wide sweep). Mode check clean (`MODE=active`, repo-root
`.env`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-010`) and whole-board: both exit 0, clean, no `WAIVED:` lines. Ticket
hop count at 4 coming in, well inside the `max_5x` tier's 20/ticket
ceiling.

Re-derived the diff from disk against the same unmoved base
(`origin/feat/ENG-009-influencer-engagement-info`, re-confirmed via
`git merge-base --is-ancestor`). Automatic-failure scan: 0/10 strictly
"automatic," but item 10 (auth path changed, no failure-case test) is where
the real finding lives this round: a failure-case test does exist
(`rejects the influencer's own role with 403`) and passes, but it calls the
handler function directly, so it can only prove the *handler* rejects that
role — it says nothing about whether the *table* does. It doesn't, because
`supabase/migrations/20260902120000_create_influencer_notes.sql` never
enables row-level security on `influencer_notes`, and the handler's own
`auth.adminSupabase` client uses the service-role key (bypasses RLS by
definition), so nothing in this feature's own code path would even notice
if RLS were on. Supabase exposes every `public`-schema table over PostgREST
by default, and this isn't theoretical here: `src/pages/
Influencers.tsx:102`, the exact file this ticket touches, already calls
`supabase.from('influencers').select('*')` directly from the browser with
the project's anon key, for the sibling table — live proof the direct path
is real on this project today. Nothing at the database layer distinguishes
`influencer_notes` from `influencers`; the same request shape with an
influencer's own valid session JWT reaches either. That reproduces exactly
the one risk this ticket's own PRD names as the thing it cannot get wrong,
through a path neither this review, round 1's review, the architect's
design, nor the database migration gate ever checked — all four verified
the edge-function-level gate carefully and never asked whether the table
itself has one. Not a P0: no PR is open and nothing has merged, which is
exactly what this gate exists to catch before either happens.

The fix is already in this same codebase, unused: `supabase/migrations/
20250926000000_proxy_sessions_audit_logs.sql` creates an existing
admin-only table of the same shape (FKs into `profiles`/`auth.users`,
service-role-only access) and pairs `ENABLE ROW LEVEL SECURITY` with a
policy scoped to `profiles.role IN ('admin', 'sub-admin')` — the identical
boundary this ticket's handler already enforces in code. Two statements,
same shape, close the gap without changing how the shipped feature
behaves. Round 1's own fix (the `useRef` stale-response guard) was
re-verified by tracing its full lifecycle in the current diff, not
re-trusted from the log — correct and complete, unrelated to this round's
finding. Verification independently reproduced: `deno check` clean, `deno
test` 16/16 new + 34/34 sibling, whole-tree `deno check` 17 pre-existing
errors (unchanged, none new), `npm run lint` 150/31 baseline unchanged
(`Influencers.tsx` one pre-existing warning, zero new), `npm run build`
clean — all matching the fix hop's own numbers exactly. Full finding, the
exact SQL fix, and every verification step: `ENG-010`'s own board file,
this dated entry.

**No receipt written** (`agents/principal-engineer/reviews/ENG-010.md`
stays absent) and **QA's hop not run this round** — discarded per the
combined-hop design, same precedent this ticket's own round 1 set.
`time_spent`/`time_remaining` updated in frontmatter in the same edit.

**0 net transitions** — `state`/`owner` unchanged (`building`/
`eng-manager`); `in-review` was never persisted, same precedent every
review-round fail on this board has set. Machine WIP unaffected (still
1/1, `ENG-010` the sole occupant). Approver-facing WIP and cap both
unaffected — a review failure is not an approver-facing gate.

**Dead-end sweep (scoped to this event):** nothing else on this ticket's
own lineage to resume — this finding *is* this pass's dead-end-sweep
result. **Notify sweep:** nothing to raise (a review failure isn't a gate
item to the approver); nothing to nudge. **1 observation filed**
(`observations.md`): the general pattern — a new service-role-only table
shipped with no RLS, and an exact working precedent for the fix
(`proxy_sessions`) sat unconsulted in the same repo the whole time.

`chained: ENG-010` — `building` is agent-owned (the fix is the next hop's
work, a fresh session per this loop's own design), not the approver, not
blocked, not terminal, not held by a cap. Firing
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-010`
before this pass exits. **Fire landed as queued, not launched** — same
orchestrating process as the fix hop above (`ps -p 17776`: alive, `eng-trigger.sh
scheduled launchd`, now elapsed 01:22:16 — it drained the fix hop's own
queued event, launched this round-2-review session itself, and still holds
the single-flight lock), confirmed via the trace log and `.pending` (`1
continue ENG-010`) rather than assumed; not re-fired manually, to avoid
racing the same lock. Every other in-flight ticket is unchanged from the
fix-hop entry above. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-010`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-09-02 — continue ENG-010 (fix hop): round 1's stale-response race closed, chained for review round 2

`continue` event pass, context `ENG-010` — the chain fired by the 16:19
review-round-1-FAIL pass above. Narrow scope per this event's own contract
(resume this ticket only; no board-wide sweep). Mode check clean
(`MODE=active`, repo-root `.env`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
whole-board: both exit 0, clean, no `WAIVED:` lines.

Fixed the finding exactly, but not via its own example line verbatim:
`selectedInfluencer?.id === influencerId` would have read a closure-stale
value (`fetchNotes` is invoked synchronously from `openInfluencer` before
React applies `setSelectedInfluencer`, so that state always reflects the
*previous* selection, not the one the call was just made for) and broken
every normal dialog open, not just the race. Used a `useRef<string | null>`
set synchronously at click time instead — same intent the finding asked
for, correct for React's render-timing model. Guarded both `fetchNotes`'s
`setNotes` and `handleAddNote`'s prepend-plus-input-clear on the ref
matching the call's own target id. Full trace, the exact diff, and why
`notesLoading`/`savingNote` were deliberately left unguarded (out of this
finding's scope): `ENG-010`'s own board file, this dated entry.

Committed and pushed `aiorders-admin-hub@8b90f0e` (no rebase needed —
`ENG-009`'s tip hasn't moved); `aiorders-api` untouched, the finding was
frontend-only. Self-tested: `npm run lint` 150/31 unchanged baseline,
`Influencers.tsx` zero new; `npm run build` clean, same baseline. No test
added — this repo's standing no-frontend-harness gap, not re-filed as a
third data point.

**0 net transitions** — `state`/`owner` unchanged (`building`/
`eng-manager`); `building → in-review` is the next (review + quality) hop's
own write. Machine WIP unaffected (1/1, `ENG-010` sole occupant).
Approver-facing WIP and cap unaffected — no gate touched this hop.

**Dead-end sweep (scoped to this event):** nothing else on this ticket's
own lineage to resume. **Notify sweep:** nothing to raise (a fix hop
doesn't notify); nothing to nudge. **1 observation filed**
(`observations.md`): a review finding's own example fix can carry the same
class of bug it diagnoses when the example touches async-closure timing —
worth re-tracing, not just trusting.

`chained: ENG-010` — `building` is agent-owned (review + quality round 2 is
the next hop's work), not the approver, not blocked, not terminal, not held
by a cap. Firing
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-010`
before this pass exits. **Fire landed as queued, not launched** — the
single-flight lock is still held by the 15:30 `scheduled` sweep's own
orchestrating process (`ps -p 17776`: alive, `eng-trigger.sh scheduled
launchd`, elapsed 01:07:34 — it launched this fix-hop session itself and
never released the lock), and `traces/.pending` confirms the event is
sitting there (`1 continue ENG-010`) rather than dropped. Expected to drain
once this session exits and hands control back to that process; not
re-fired manually, to avoid racing the same lock. Every other in-flight
ticket is unchanged from the 16:19 entry above. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
whole-board: exit 0, clean, no `WAIVED:` lines.

## 2026-09-02 — continue ENG-010 (16:19): code review round 1 FAIL — a stale-response race in the new notes UI, routed back to building

`continue` event pass, context `ENG-010` — the chain fired by the 16:02
build hop above. Narrow scope per this event's own contract (resume this
ticket only; no board-wide sweep). Mode check clean (`MODE=active`,
repo-root `.env`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-010`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

Reviewed this ticket's own diff against its actual base
(`origin/feat/ENG-009-influencer-engagement-info`, confirmed unmoved since
branch time via `git merge-base --is-ancestor`), not against `main` — same
discipline `ENG-009`'s own round 1 established after being burned by the
opposite gap. Automatic-failure scan: 0/10. The round fails on a
correctness finding outside that list: `Influencers.tsx`'s two new
per-dialog note callbacks (`fetchNotes`, `handleAddNote`) apply their async
response unconditionally, with no check that it's still for the influencer
currently open — closing one influencer's dialog and opening another while
a request is in flight can display the wrong influencer's notes, silently,
under the wrong name. Ordinary click-through speed reproduces it; no exotic
timing needed. Not the influencer-visibility risk this ticket's own PRD
names as the one thing it can't get wrong (server-side the note is always
written against the right `influencer_id`), and not a P0 — but it
undermines the feature's whole point (staff acting on accurate notes), and
no test could have caught it: `aiorders-admin-hub` has no frontend test
harness at all (standing gap, `proposals.md` 2026-08-31 — second concrete
data point filed to `observations.md` this pass).

Backend verification independently reproduced, not taken on the build
hop's word: `deno check`/`deno test` — 16/16 new, 34/34 sibling, matching
exactly. `npm run lint`/`build` (`aiorders-admin-hub`) at the established
baseline, `Influencers.tsx` carrying its one pre-existing warning, zero
new. Two of the diff's own comments spot-checked rather than trusted (the
router substring-non-overlap claim, the `influencer-invitations.ts`
fetch-separately-map-by-id precedent) — both confirmed accurate. Full
finding, fix, and secondary non-blocking notes: `ENG-010`'s own board file,
2026-09-02 16:19 entry.

**No receipt written** (`agents/principal-engineer/reviews/ENG-010.md`
stays absent) and **QA's hop not run this round** — discarded per the
combined-hop design, same precedent `ENG-009`'s own round-1 fail set.
`time_estimate`/`time_spent`/`time_remaining` backfilled onto this ticket's
frontmatter in the same edit (previously never populated — a gap from its
own `ready → building` entry, named rather than silently carried forward).

**0 net transitions** — `state`/`owner` unchanged (`building`/
`eng-manager`); `in-review` was never persisted, same precedent
`ENG-008`/`ENG-009` each already set. Machine WIP unaffected (still 1/1,
`ENG-010` the sole occupant). Approver-facing WIP and cap both unaffected —
a review failure is not an approver-facing gate.

**Dead-end sweep (scoped to this event):** nothing else on this ticket's
own lineage to resume — this finding *is* this pass's dead-end-sweep
result. **Notify sweep:** nothing to raise (a review failure isn't a gate
item to the approver); nothing to nudge. **1 observation filed**
(`observations.md`): the frontend-race finding as a second data point for
the standing no-test-harness proposal.

`chained: ENG-010` — `building` is agent-owned (the fix is the next hop's
work, a fresh frontend session per this loop's own design), not the
approver, not blocked, not terminal, not held by a cap. Firing
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-010`
before exiting. Every other in-flight ticket is unchanged from the 16:02
entry above. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-010`) and whole-board: exit 0, clean, no `WAIVED:` lines.

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

## 2026-09-02 — watch sweep (~10:58): self-triggered by ENG-009's own merge-request write, nothing new

`watch` event pass, context `launchd` — fired immediately behind the
`continue ENG-009` pass's own commit (`d407096`, `10:57:26`). Narrow scope
per this event's own contract: sweep the three watched inboxes only, act
on what's new, ignore what's already processed.

Mode check clean (`MODE=active`, repo-root `.env`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

**Traced this fire to its source before treating it as new**, same
discipline as the three duplicate watch fires on 2026-09-01
(`board/_index-archive.md`). `git status` on `business-os` is fully clean
and `HEAD` is `d407096` — exactly the commit the `continue ENG-009` pass
ended on, per its own log entry directly above. A direct mtime sweep of
`inbox/*.md` shows exactly one file newer than that pass's start:
`inbox/2026-09-02-eng009-merge-request.md` (`10:52`), the L1 merge-request
item that same pass wrote, notified (`traces/eng-notify-2026-09-02.log`,
`10:51:07`), and already accounted for in its own log and in this board's
"Waiting on the approver" section. Not new information — that pass's own
bookkeeping tripping the fingerprint, identical in shape to every watch
duplicate fire recorded yesterday.

**All three inboxes swept anyway, not trusted from the paragraph above.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
their `_handled`/`_processed` archives — nothing loose. `inbox/requests/`
holds only its `.gitkeep`. `inbox/`'s ten loose items, each checked
individually rather than as a batch:

- Four `gate: incident` items (`2026-08-30-eng-loop-halted`,
  `2026-08-30-eng-events-dropped`, `2026-08-31-eng-events-dropped`,
  `2026-09-01-eng-gate-violation-watch`) each already carry an
  "Investigated" addendum from an earlier pass concluding "no further
  action; not a gate the approver answers" (or the 08-31 file's equivalent
  closing note). Mtimes on all four predate today. Nothing to do.
- Six `decision:`-bearing items (`ENG-007` continue-sequence question,
  `ENG-008`/`ENG-013`/`ENG-009` merge requests, `ENG-016` G1, `ENG-026`
  readback question) all still show `decision:` blank (or, for `ENG-016`,
  no `decision:` key at all — the drift already logged in
  `observations.md`). Each is already notified and, where 24h has passed,
  already nudged its one permitted time (`ENG-007`, `ENG-008`, `ENG-013`,
  `ENG-016`); `ENG-026` and `ENG-009` are both under the 24h threshold and
  correctly not yet nudged. No hand-edit on any of them — only `ENG-009`'s
  file has today's mtime, and that's its own raising pass, not a reply.

**No dispatch, no chaining.** Nothing in this pass's scope was newly
unblocked: the one ticket this fire traces back to (`ENG-009`) is already
`blocked`/`blocked_on: approver` with its own `chained: none` correctly
recorded by the pass that put it there. Machine WIP unchanged (`ENG-010`
alone at `ready`, 1/1); approver-facing WIP unchanged (4/2, over cap,
already named above).

**0 ticket-state transitions.** No new observations, no new proposals —
nothing surfaced that isn't already tracked. Rolled the 02:00
scheduled-sweep entry to archive, keeping the live board's cap of three.

`chained: none` — no ticket in this pass's scope was touched or unblocked;
this pass only confirmed that what already looked settled is in fact
settled. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board: exit 0, clean, no `WAIVED:` lines.

## 2026-09-02 — continue ENG-009: release-readiness done, both PRs opened stacked on ENG-008, now blocked on the approver

`continue` event pass, context `ENG-009` — the chain fired by the 09:30
`scheduled` pass's own resumption above. Narrow scope per this event's own
contract: resume this ticket only, no board-wide sweep. Mode check clean
(`MODE=active`). Pre-pass `eng-gate-check.sh`, scoped (`ENG-009`) and
whole-board: both exit 0, clean, no `WAIVED:` lines.

**All four upstream gates re-verified from the receipt files themselves**
(migration, code review round 2, QA test plan, security — all **pass**),
not trusted from the ticket's own log summary. Both worktrees were already
clean on this ticket's own branch at its recorded commits; no existing PR
found before creating one.

**The one judgment call this hop made:** this ticket's branch is built on
top of `ENG-008`'s branch, not `main` (confirmed by ancestry check,
matching what the build hop's own PR-body draft already flagged), and
`ENG-008` is still unmerged. Opening against `main` as usual would have
pulled `ENG-008`'s three commits into this diff too, duplicating its own
still-open PR. Opened both PRs with `--base
feat/ENG-008-influencer-admin-management` instead — confirmed by diffing
against that base first that this produces exactly ENG-009's own change
(314 insertions/3 files on `aiorders-api`; 196+/10- on 1 file on
`aiorders-admin-hub`) and nothing of `ENG-008`'s.

**Opened both PRs**: `aiorders-api`
https://github.com/harsimranwalia/aiorders-api/pull/7,
`aiorders-admin-hub`
https://github.com/harsimranwalia/aiorders-admin-hub/pull/6. Wrote the L1
merge-request item (`inbox/2026-09-02-eng009-merge-request.md`), `pr_urls:`
as a YAML list, an explicit Sequencing section explaining the stacked-base
choice and both legal ways to resolve merge order. Notified cleanly
(`traces/eng-notify-2026-09-02.log`).

**Caught and corrected a wrong claim in an existing proposal while
deciding how to stamp `notified:`.** The 09:30 pass's own proposal
(`proposals.md`, 2026-09-02 row) asserted `ENG-008`'s/`ENG-013`'s
merge-request timestamps were genuine UTC, unlike the PM-agent items under
investigation. Checked directly rather than carried forward: both are
textually identical to their own trace-log line, zero gap, same
local-time-mislabeled-as-UTC pattern as every other gate item on this
board. Corrected the proposal's three cells in place (see `ENG-009`'s own
board-file log for the full diff) — the bug is board-wide, not
PM-agent-specific, and there is no second, already-correct path to match
against. Stamped this item's own `notified:` consistently with the actual,
verified convention.

**Cap check, not a hold.** Approver-facing WIP was already `3/2`, over
cap, going in. This transition makes it `4/2`. Per the loop's own guard,
the cap gates *new* work from starting that will need the approver, not a
ticket already at `ready-to-ship` reaching its required, non-discretionary
L1 conclusion — `ENG-008`/`ENG-013` already set this exact precedent. Not
treated as a reason to hold.

State → `blocked`, `blocked_on: approver`, `blocked_from: ready-to-ship`,
owner `devops → approver`. `links.pr` set to both PR URLs. **1 transition**
(`ready-to-ship → blocked`), well under the cap of 4. **Consequence:**
machine WIP `2/1 → 1/1` (`ENG-009` leaves the counted `ready`..`ready-to-ship`
range; `ENG-010` alone remains, exactly at cap). Approver-facing WIP
`3/2 → 4/2`.

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for state with the chain record below. **Notify sweep:**
this pass's own gate item raised and stamped; nothing else newly eligible.
**1 proposal corrected**, no new observations.

Full detail — receipts verified, the base-branch reasoning, the PR bodies,
the proposal correction, the full log record: `ENG-009`'s own board file,
2026-09-02 release-readiness entry.

`chained: none` — `blocked`, `blocked_on: approver`. This is the human gate
the whole hop was driving toward; firing `continue ENG-009` again would
only queue against a ticket with nothing left for a machine to do until the
approver merges one or both PRs or replies to the gate item. Every other
in-flight ticket is unchanged from the 09:30 pass: approver-blocked
(`ENG-008`, `ENG-013`, `ENG-016`, `ENG-026`) or WIP-capped (`ENG-010`,
`ENG-014`, `ENG-015`, `ENG-017`, `ENG-018`–`ENG-021`, `ENG-022`–`ENG-025`),
`chained: none` for all of them, same reasons as before. Post-pass
`eng-gate-check.sh`, scoped (`ENG-009`) and whole-board: both exit 0,
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

---

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

**CORRECTION, filed 2026-09-01T15:30 by the `scheduled` pass that follows
this one in `_index.md`:** this entry's own "already resolved or correctly
inert" line above is wrong about `inbox/2026-08-31-eng-events-dropped.md`
specifically (it lumped that file in with `2026-08-30-eng-loop-halted.md`
and its siblings without actually reading it) — that file had never been
investigated, notified, or nudged, unlike the others named here. See the
15:30 entry in `_index.md` and the file's own closing note for the
correction; not rewritten here, since this section is historical record of
what this pass believed at the time, not a live claim.

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

## 2026-08-31 — continue ENG-013: release-readiness — both PRs opened, now blocked on the approver

`continue` event pass, context `ENG-013`, drained immediately behind the
`ENG-008` security-gate pass (`traces/eng-loop-2026-08-31.log`: `pass end:
continue (exit 0, 589s)` at `10:59:15` → `draining queued event: continue
(ENG-013)` → `pass start` at `10:59:16`). Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean (`MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean.

Verified all four upstream gates fresh from the receipt files: migration,
code review (round 2), quality, security — all **pass**. Both worktrees
were clean on `ENG-008`'s branch; fetched, checked out
`feat/ENG-013-foodswipe-funnel-stage-control`, confirmed both branches
match this ticket's own frontmatter exactly (`aiorders-api@c95b25b`,
`aiorders-admin-hub@a1c3bdf`), confirmed no PR already existed on either
repo. Opened both (`aiorders-api` first): PR #5
(https://github.com/harsimranwalia/aiorders-api/pull/5), PR #4
(https://github.com/harsimranwalia/aiorders-admin-hub/pull/4). Restored
both worktrees to `feat/ENG-008-influencer-admin-management` afterward.

Wrote the L1 merge-request item
(`inbox/2026-08-31-eng013-merge-request.md`), using the skill's current
`pr_urls:` YAML-list format rather than `ENG-011`'s now-superseded single
delimited string. Notify sent cleanly. State → `blocked`,
`blocked_on: approver`, `blocked_from: ready-to-ship`, owner
`devops → approver`.

**1 transition** (`ready-to-ship → blocked`). **Consequence:** `machine_wip`
4/1 → 3/1 (`ENG-013` leaves the counted `ready`..`ready-to-ship` range —
`ENG-009`/`ENG-010` at `ready`, `ENG-008` at `ready-to-ship` remain).
Approver-facing WIP 0/2 → 1/2; approval cap 0/3 → 1/3.

One observation filed (`observations.md`): this pass's `eng-notify.sh
raise` sent cleanly, unlike `ENG-011`'s recorded `SLACK_WEBHOOK_URL unset`
gap at the same step.

`chained: none` — `blocked`, `blocked_on: approver`. This is the human
gate the whole hop was driving toward; firing `continue ENG-013` again
would only queue against a ticket with nothing left for a machine to do.
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-013`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-31 — continue ENG-008: security gate — PASS, now ready-to-ship

`continue` event pass, context `ENG-008`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean.

Ran the security gate fresh — no receipt existed at pass start. Re-derived
both diffs from disk (matched code review's own figures exactly: 4
files/404 insertions on `aiorders-api`, 1 file/202 insertions/14 deletions
on `aiorders-admin-hub`) and read the actual handler, test file, migration,
router diff, and full frontend diff directly rather than trusting the prior
review's account. Threat-modelled the change: new capability is read+write
on 6 fields for the same admin/sub-admin population that already read all
of them (the page was 100% read-only before this ticket); blast radius on
full compromise is identical to `loyalty-config.ts`/`foodswipe.ts`
(service-role client, RLS bypassed, only the in-code role checks gate
access) — already-accepted architecture, not a new risk.

Walked OWASP A01–A10, all ten marked applicable or `n/a` with a reason. A01
clean — one shared gate before the GET/PATCH branch, body-supplied `id`
never used for row selection, no client-side-only authorization. Verified
the negative-auth cases independently rather than assuming QA's/review's
account correct: no-token/invalid-token 401 and no-profile 403 confirmed
live in `index.ts`'s unmodified `authenticate()`; wrong-role 403 proven by a
throwing-Proxy test that fails if the gate is ever bypassed; the
field-allowlist test hand-traced and confirmed mutation-sensitive (asserts
the exact object reaching `.update()`, not just the response shape). A05
found one non-blocking item — the same raw-`error.message`-on-500 shape
`ENG-013`'s review tracked as occurrence 1/3 on `foodswipe.ts`. Checked the
actual extent before logging it as a repeat: a grep across
`admin-portal/handlers/` finds the identical pattern in 8 files total, six
pre-dating this department's review process — so three-strike tracking
counts *gate-reviewed* occurrences (this is the 2nd), not the repo's
pre-existing total. Logged to
`agents/security/notebook/2026-08-31-findings.md`, not blocking.

Secrets: full diff and branch history on both repos scanned — two benign
matches (a CORS header's literal `apikey` string, and the frontend's own
forwarded user session token), no leaked credential. Dependencies: none
new. LLM checklist: n/a, confirmed against the diff. Independently
re-confirmed code review's `min_visit_payment` stale-value finding against
the diff directly — real, but P3/data-integrity, not security; carried
forward rather than re-raised.

**Receipt written**: `agents/security/reviews/ENG-008.md` (verdict `pass`).
`links.security_review` set; `time_spent`/`time_remaining` updated — only
release-readiness remains.

**1 transition** (`in-qa → ready-to-ship`), well under the cap of 4.
Machine WIP unaffected — stays inside the counted `ready`..`ready-to-ship`
range, still 4/1 (`ENG-009`/`ENG-010` at `ready`, `ENG-013` alongside this
ticket now both at `ready-to-ship`). No approver-facing or approval-cap
change — a security pass isn't a gate item, and the `owner` handoff to
`devops` is agent-to-agent.

`chained: ENG-008` — `ready-to-ship` is agent-owned (devops's
release-readiness hop next), not the approver, not blocked, not terminal,
not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-008`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-31 — continue ENG-025: design actually written — PASS, stays at designed (WIP-capped)

`continue` event pass, context `ENG-025`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
This is the dedicated `continue ENG-025` session the prior `scheduled` pass
recorded chaining to and never reached — confirmed at pass start: `ENG-025`
absent from `traces/.pending` (already drained to launch this session; only
`ENG-008` and `ENG-013` remain queued behind it); no design file existed at
`agents/architect/designs/ENG-025-*.md`. Mode check clean. Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-025`) and
whole-board: both exit 0, clean.

Read the real code (`aiorders-api`'s `brand-portal/feedback.ts`,
`restaurant-portal`'s `brandPortalApi.ts` and `feedback/Index.tsx`) rather
than trusting the PRD's summary — confirmed `get_feedback` already returns
the restaurant's entire history with `type`/`sub_type`/`nature` on every row,
already rendered per-card today. Wrote
`agents/architect/designs/ENG-025-feedback-recurring-issues.md`: one new
presentational component (`RecurringIssuesSummary.tsx`, pure client-side
aggregation via `useMemo` over data the page already fetches), one render-call
edit to `Index.tsx`. No new backend action, no migration. `ADR-007` records
the two calls the PRD left open (all-time window, >1 threshold for
"recurring"); judged reversible and not a one-way door, same precedent
`ADR-005`/`ADR-006` set — **no G2**.

**Stays at `designed` regardless — held by the machine WIP cap, not a gate.**
Re-verified fresh from each ticket's own frontmatter: `ENG-008` (`in-qa`),
`ENG-009`/`ENG-010` (`ready`), `ENG-013` (`ready-to-ship`) — four tickets
inside the counted `ready`..`ready-to-ship` range against a cap of 1,
unchanged since this morning's `scheduled` sweep. Design work itself is
exempt from this cap; entering `ready` is not, so this pass does not attempt
it — no branch created, no code written.

Closes the chain gap the 2026-08-31 `scheduled` sweep flagged against this
ticket — the third and last of the three (`ENG-014`, `ENG-015`, `ENG-025`)
it found sitting at `designed` *un-designed*. All three are now genuinely
cap-held-after-completion.

**0 transitions** — ticket stays at `designed`; the cap, not the hop budget,
is what stopped it. Machine WIP unaffected (still 4/1, `ENG-025` was never
inside the counted range). Approver-facing WIP and approval cap both
unaffected — no gate raised.

`chained: none` — held by the machine WIP cap (4/1: `ENG-008`/`ENG-009`/
`ENG-010`/`ENG-013` occupying), one of the documented no-chain conditions.
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-025`)
and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-31 — continue ENG-015: design actually written — PASS, stays at designed (WIP-capped)

`continue` event pass, context `ENG-015`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
This is the design work three prior passes recorded chaining to and none of
them actually reached — confirmed at pass start: `ENG-015` absent from
`traces/.pending` (already drained to launch this session); no design file
existed at `agents/architect/designs/ENG-015-*.md`. Mode check clean.
Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-015`) and whole-board: both exit 0, clean.

Read the real code across both repos this ticket touches — `aiorders-api`'s
`admin-portal/handlers/restaurants.ts` (all four functions, not only the one
the PRD's Evidence section named), `brands.ts`, `_shared/restaurantAccess.ts`,
`proxy-login/index.ts`, every migration touching `restaurants`'/`brands`'
RLS, and `admin-portal/index.ts`'s auth middleware; `aiorders-admin-hub`'s
`AddRestaurantModal.tsx`, `AuthContext.tsx`, `Brands.tsx`,
`PartnerBrandAssignment.tsx`, `Restaurants.tsx` — rather than trusting the
PRD's summary. Wrote
`agents/architect/designs/ENG-015-agency-reseller-brand-scoping.md`: one
local helper pair in `restaurants.ts` (`isStaff`, `getPartnerBrandIds`)
applied to `getRestaurants`/`getRestaurantById`/`updateRestaurant`; one new
`INSERT` policy migration on `restaurants` (brand-scoped, `WITH CHECK
(approved = false)`); one small `AddRestaurantModal.tsx` change.

**Tracing the RLS history changed the design from what the PRD proposed.**
The PRD suggested mirroring `brands.ts`'s client-branch pattern for the read
fix. Three migrations after the one the PRD cited already locked
`restaurants`' public SELECT down to `USING (false)` — that branch would
return zero rows for a partner today, not their own brand's rows. Separately
`brands` has zero RLS policies in tracked migration history at all, the same
untracked-schema-history gap the PRD already names for `profiles`/
`influencers`, now confirmed for a second table. Designed around both
findings — brand scoping enforced in code via the service-role client, not
by trusting either table's RLS. `ADR-006` records the decision; judged
reversible and not a one-way door, same precedent `ADR-004`/`ADR-005` set —
**no G2**.

**Extended the fix to two functions the PRD's Evidence section didn't
name** (`getRestaurantById`, `updateRestaurant` — same file, same defect,
reachable today by a partner via a direct call, squarely inside AC2's own
wording), logged as a deliberate scope decision rather than silently
expanded or silently left open. **Found a third, unrelated defect in the
same file** (`updateBrandOwner()` — no role/ownership check at all, any
partner can rewrite any brand owner's contact info) — different resource
than this PRD describes, not folded in; filed as a proposal in
`agents/eng-manager/proposals.md` (architect-originated finding, step 3)
instead.

**Stays at `designed` regardless — held by the machine WIP cap, not a
gate.** Re-verified fresh from each ticket's own frontmatter: `ENG-008`
(`in-qa`), `ENG-009`/`ENG-010` (`ready`), `ENG-013` (`ready-to-ship`) — four
tickets inside the counted `ready`..`ready-to-ship` range against a cap of
1, unchanged since this morning's `scheduled` sweep. Design work itself is
exempt from this cap; entering `ready` is not, so this pass does not
attempt it — no branch created in either worktree, no code written.

Closes the chain gap the `scheduled` sweep flagged this morning against
this ticket specifically: `ENG-015` was sitting at `designed`
*un-designed*, not cap-held-after-completion. As of this pass it's
genuinely the latter.

**0 transitions** — ticket stays at `designed`; the cap, not the hop
budget, is what stopped it. Machine WIP unaffected (still 4/1, `ENG-015`
was never inside the counted range). Approver-facing WIP and approval cap
both unaffected — no gate raised.

`chained: none` — held by the machine WIP cap (4/1:
`ENG-008`/`ENG-009`/`ENG-010`/`ENG-013` occupying), one of the documented
no-chain conditions. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-015`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-31 — continue ENG-014: design actually written — PASS, stays at designed (WIP-capped)

`continue` event pass, context `ENG-014`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
This is the dedicated `continue ENG-014` session three prior passes recorded
chaining to and none of them actually reached — confirmed at pass start:
`ENG-014` absent from `traces/.pending` (already drained to launch this
session). Mode check clean. Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-014`) and
whole-board: both exit 0, clean.

Read the real code across all three repos this ticket touches
(`aiorders-api`'s `url-shortener` and `brand-portal` functions,
`aiorders-admin-hub`'s three existing QR/media call sites, `restaurant-portal`'s
own context/API/nav) rather than trusting the PRD's summary. Wrote
`agents/architect/designs/ENG-014-restaurant-qr-media-self-service.md`: one
new restaurant-scoped action on `url-shortener` (`get_or_create_restaurant_qr`,
computing its own destination URL server-side rather than trusting the
caller's, which is what makes the restaurant-scoping actually binding), one
new read action on `brand-portal` (`get_restaurant_media_info`), and both
existing generator components ported into `restaurant-portal` (no shared
package exists across these four repos to import from instead). `ADR-005`
records the one real "why on earth" decision (narrowing `url-shortener`'s
trust boundary per-action); judged reversible and not a one-way door, so
decided and logged rather than escalated — **no G2**, same precedent
`ENG-011`/`ENG-013` set.

**Stays at `designed` regardless — held by the machine WIP cap, not a gate.**
Re-verified fresh from each ticket's own frontmatter: `ENG-008` (`in-qa`),
`ENG-009`/`ENG-010` (`ready`), `ENG-013` (`ready-to-ship`) — four tickets
inside the counted `ready`..`ready-to-ship` range against a cap of 1. Design
work itself is exempt from this cap; entering `ready` is not, so this pass
does not attempt it.

Closes the specific ambiguity the architect's own `ENG-023` observation and
the prior `scheduled` sweep both flagged against this ticket: `ENG-014` was
sitting at `designed` *un-designed*, not cap-held-after-completion. As of
this pass it's genuinely the latter. `ENG-015` is untouched (out of scope —
this event names `ENG-014` only) and remains un-designed.

**0 transitions** — ticket stays at `designed`; the cap, not the hop budget,
is what stopped it. Machine WIP unaffected (still 4/1, `ENG-014` was never
inside the counted range). Approver-facing WIP and approval cap both
unaffected — no gate raised.

`chained: none` — held by the machine WIP cap (4/1:
`ENG-008`/`ENG-009`/`ENG-010`/`ENG-013` occupying), one of the documented
no-chain conditions. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-014`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-31 — continue ENG-013: security gate — PASS, now ready-to-ship

`continue` event pass, context `ENG-013`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean.

Ran the security gate fresh — no receipt existed at pass start, a real
first execution. Threat-modelled the change (new input: `profileId`/`stage`
on two new POST routes, both behind the existing bearer-auth middleware and
the handler's existing admin/sub-admin gate; new capability: write access
to one enum field, granted only to the population that could already read
every row; blast radius on full compromise: integrity-only, reversible, no
new confidentiality or financial exposure). Walked OWASP A01–A10, 8 `n/a`
with reason, 2 reviewed in full. A01 clean — both new write routes reuse the
one existing gate call and additionally scope every write to
`source='foodswipe'`, the same tenant boundary the existing read already
enforced; independently re-verified the tenant-scoping test is
mutation-sensitive by construction, not just shape-checked. A05 found one
non-blocking item — both new actions return a raw `error.message` on a
500 — weighed (role-gated before either function runs, copied from this
file's own pre-existing `GET` catch, nothing secret in what it could
contain) and logged as the first tracked occurrence of this finding class
in `agents/security/notebook/2026-08-31-findings.md`, not escalated.
Checked all three of the baseline's negative-auth cases, not just the two
with dedicated tests — read `admin-portal/index.ts` fresh to confirm the
no-token case 401s upstream of this handler entirely, unmodified by this
diff. Secret-scanned the diff and all three unique commits across both
branches: zero matches. SOC 2 evidence trail confirmed complete. Full
detail: `agents/security/reviews/ENG-013.md`, and the ticket's own log.

**1 transition** (`in-qa → ready-to-ship`), well under the cap of 4 —
stopped deliberately, not by the cap: `release_readiness` is a separate
hop after `security` per `config.yaml`'s `sequential_after_quality`, and
this was a fresh security session with no receipt to recover. `machine_wip`
unaffected (`ENG-013` stays inside the counted `ready`..`ready-to-ship`
range, now at its far end). Approver-facing WIP and approval cap both
unaffected — `ready-to-ship` raises no gate for an L1 project; devops's
release-readiness hop is what opens the PR and raises the merge request.

`chained: ENG-013` — `ready-to-ship` is agent-owned (devops's
release-readiness hop next), not the approver, not blocked, not terminal,
not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-013`
before exiting — confirmed queued (not lost): the trigger's own log shows
it queued behind the still-active `scheduled launchd` fire's lock rather
than launching immediately, same FIFO shape every prior hop on this ticket
has used. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-31 — continue ENG-008: review+quality combined hop, round 2 — PASS, now in-qa

`continue` event pass, context `ENG-008`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean.

Ran the code-review-gate and quality gates fresh, re-deriving both diffs
from disk rather than trusting the prior pass's own account (clean diff
against each repo's own merge-base, no main-drift pollution). Automatic-
failure scan: 0/10 open — both round-1 findings independently re-verified:
hand-traced all 19 `Deno.test` cases in `influencers.test.ts` against
`influencers.ts` at HEAD (no `deno` on this host), and independently
re-confirmed the frontend null-coalescing fix by re-reading the migration's
additive backfill, not by trusting the fix-pass's own claim. One new,
non-blocking (P3) finding from this round's own full review — not a round-1
regression: `handleSaveInfluencer` can write a stale `min_visit_payment`
after `accepts_paid` is toggled off, since the two fields are sent
independently of each other. Named in the review receipt rather than filed,
per this board's practice for a single-occurrence, non-blocking finding at
this scale. Full detail: `agents/principal-engineer/reviews/ENG-008.md`,
`agents/qa/test-plans/ENG-008.md`, and the ticket's own log.

**2 transitions** (`building→in-review→in-qa`), well under the cap of 4 —
stopped deliberately, not by the cap: security is a separate hop by design
(`sequential_after_quality`), needing this pass's own just-written QA plan,
and a fresh session is what `eng_build_loop.md` calls for there. `machine_wip`
unaffected (`ENG-008` stays inside the counted `ready`..`ready-to-ship`
range — now at `in-qa`, alongside `ENG-013`). Approver-facing WIP and
approval cap both unaffected — no gate raised.

Also populated `time_estimate`/`time_spent`/`time_remaining` on this ticket
for the first time — round 1's own observation had flagged these as never
carried despite `definition-of-done.md` calling for them from `building`
onward; closed here rather than left for another pass to re-notice.

`chained: ENG-008` — `in-qa` is agent-owned (security next, fresh session),
not the approver, not blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-008`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-31 — scheduled (launchd): three broken chains repaired (ENG-014/015/025), attempt 2/3 on this event

`scheduled` event pass, context `launchd` — the four-times-daily safety-net
sweep, whole-board per this event's own contract. This fire is attempt 2/3
of the `scheduled` event: attempt 1 (02:45–02:56) ran a real 647s
investigation, reached the same conclusion below, then died exit 1 on the
account's monthly spend limit at the moment it tried to act — correctly not
treated as "never started" (real output, real duration) and correctly
re-queued rather than dropped. This pass independently re-verified
everything from disk rather than trusting that narrative, per this
instance's own standing practice.

Mode check clean (business-os `.env` → `MODE=active`; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Gate returns:** `inbox/` holds one item, `2026-08-30-eng-events-dropped.md`
(incident, no `decision:` field) — already self-investigated same-day,
concluding the two causes (OAuth token revoked, transient DNS failure) were
host/network issues unrelated to `ENG-023`. Left in place, not archived:
every prior `eng-events-dropped` item on this board (`decision-journal.md`
rows 22, 35) moved to `_handled/` only once the approver actually answered
it; this one never has, and "never infer approval from silence" applies to
archiving an incident item as much as to advancing a ticket. Not blocking
anything — `gate: incident` items don't occupy the approver-facing WIP or
approval-cap counts. PM inbox and EM inbox both empty (only `_handled/`) —
nothing for business or technical intake this pass.

**Merge detection:** no ticket currently at `state: blocked` (confirmed by
grepping every ticket's own frontmatter, not the board header) — nothing to
check against `origin/main`.

**Dead-end sweep — the substantive finding.** Investigated
`agents/architect/designs/` directly after the `continue ENG-023` entry
above filed an observation that `ENG-014`/`ENG-015` were cited as
`designed`-by-WIP-cap precedent without actually having a design file.
Confirmed and extended: **`ENG-014`, `ENG-015`, and `ENG-025` all have no
design file, and none of them has ever had a `continue` pass actually run**
— grepped every `traces/eng-loop-*.log` this instance has ever written for
`pass start: continue (ENG-014|ENG-015|ENG-025)` (exact format confirmed
live against `ENG-008`'s and `ENG-013`'s own successful runs earlier today):
zero matches, for any of the three, ever. `ENG-014` and `ENG-015` each
carry a ticket-log entry from 2026-08-29 that already found and repaired
this once (the original `watch`-pass fire died before launching; a later
`decision` pass re-fired it and confirmed it landed in `traces/.pending`)
— so this is a *second*, different loss of the same two chains, this time
between a confirmed append and an actual drain, with no code read yet that
explains how. `ENG-025` never had that intermediate repair at all. None of
the three ever produced an `eng-events-dropped` incident, because that
mechanism only fires on a launch that fails or never-starts — this loss
happens earlier, between append and drain, so today's board-reading safety
net is currently the only thing that catches it, and it took two days on a
`P1` security ticket (`ENG-015`).

**Action taken.** `continue ENG-014` was already sitting in
`traces/.pending` at this pass's start — left alone rather than double-fired
(collapses harmlessly at worst; firing blind into a possibly-already-stuck
entry doesn't diagnose anything). `continue ENG-015` and `continue ENG-025`
were not queued — fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-015` and
`continue ENG-025` directly, each confirmed on `traces/.pending` afterward
rather than assumed. All three now queue behind `ENG-008`/`ENG-013`
(already queued, unrelated) and will drain one pass at a time once this
pass releases the lock. Full reasoning on each of the three tickets' own
logs.

**Filed, not fixed:** `agents/eng-manager/proposals.md` — the dispatch gap
itself (append confirmed, drain never happens, no drop-notice either) is
department machinery, not a ticket-shaped change, and this instance's own
rule reserves that class of fix for the approver's sign-off. Corroborating
row in `observations.md`, cross-referencing the architect's own `ENG-023`
observation this same day.

**Notify sweep:** nothing new to raise — no gate opened this pass, and the
one open incident item is well past any nudge threshold but explicitly
exempt (see Gate returns above; it isn't a decision awaiting an answer in
the G1/G2/G3/merge sense the nudge rule targets). Approval cap 0/3, not
full — no stall.

**Caps, re-verified fresh:** machine WIP still 4/1 (`ENG-008`/`ENG-013`
`building`, `ENG-009`/`ENG-010` `ready`) — unaffected by any action this
pass (all three repairs stay at `designed`, below the cap's own range).
Approver-facing WIP 0/2, approval cap 0/3 — both unaffected, no gate raised
or answered.

`chained: ENG-015`, `chained: ENG-025` — both fired and confirmed queued
this pass (see ticket logs). `chained: none` for `ENG-014` — already
queued; a second fire would not be a repair. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

## 2026-08-31 — continue ENG-013: review+quality combined hop, round 2 — PASS, now in-qa

`continue` event pass, context `ENG-013`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean.

Ran the code-review-gate and quality gates fresh — no receipt existed for
either at pass start, so unlike `ENG-007`'s/`ENG-011`'s own recovery passes
this was a real first execution, not a discovery of already-completed work.
Automatic-failure scan: 0/10 open — round 1's #10 (no failure-case test on
the new authz-gated write path) is closed by `foodswipe.test.ts`, with the
`source='foodswipe'` scoping test confirmed mutation-sensitive (a fake
client records every `.eq()` call, so removing that scoping line would fail
the test for the reason it exists, not incidentally). `npm run
lint`/`npm run build` (`aiorders-admin-hub`) reproduced fresh, both clean
against this ticket's own recorded baseline. `deno test` could not execute
on this host (deno absent, `aiorders-api` has no registered suite command)
— hand-traced all 17 cases against the code at HEAD instead, independently
of the prior pass's own trace, zero discrepancies, named plainly as
corroborating evidence rather than a green run. QA plan written covering
all five acceptance criteria. Full detail: `agents/principal-engineer/reviews/ENG-013.md`,
`agents/qa/test-plans/ENG-013.md`, and the ticket's own log.

**2 transitions** (`building→in-review→in-qa`), well under the cap of 4 —
stopped deliberately, not by the cap: `config.yaml`'s `combined_hop`
licenses exactly `[code_review, quality]` together; security is a
separate hop by design (`sequential_after_quality`), needing QA's just-
written plan, and a fresh session is what `eng_build_loop.md` calls for
there. `machine_wip` unaffected (`ENG-013` stays inside the counted
`ready`..`ready-to-ship` range). Approver-facing WIP and approval cap both
unaffected — no gate raised.

**Observation filed** (`observations.md`): the existing Supabase-MCP
substitute-verification proposal (2026-08-29) does not cover this ticket's
own deno-unavailable gap — different tool, no substitute execution path
exists; a prior pass's note conflated the two.

`chained: ENG-013` — `in-qa` is agent-owned (security next), not the
approver, not blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-013`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-31 — continue ENG-008: round 1's findings fixed, chained for review round 2

`continue` event pass, context `ENG-008`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean.

Found a second undocumented commit on `aiorders-api` (`dc6972a`, the missing
test file round 1 asked for) — same cross-host shape `ENG-013` hit
2026-08-30, but this time hand-tracing it against the review notebook (not
just against the handler) found it incomplete: covered three of four named
`hasInfluencerAdminAccess` cases and every field validation, but not the
"missing/undefined profile" case or a test proving `EDITABLE_FIELDS`
actually strips an unauthorized field from a mixed body. Closed both gaps:
`hasInfluencerAdminAccess` now null-safe (optional chaining; confirmed not
live-reachable today since `index.ts`'s router already 403s before any
handler runs on a missing profile, fixed anyway to match this repo's own
`loyalty-config.ts` precedent and close what round 1 explicitly asked for),
plus two new tests. Independently re-confirmed the CORS/`PATCH` fix from the
original build hop is still intact.

Fixed the real bug properly rather than patching the symptom:
`Influencers.tsx`'s `accepts_paid`/`accepts_barter` now pass through
`openInfluencer` as `null` (dropping the `barter_visit` fallback entirely —
hand-confirmed it never had a correct value to fall back to, since the
migration's additive backfill guarantees `barter_visit` is null in every row
where the new flags are also null), checkboxes render unchecked via
`?? false` without mutating the stored form state, and
`handleSaveInfluencer` now omits either field from the PATCH body while
still `null` — an untouched unset preference survives any number of saves
instead of getting overwritten with a guess. This is the stronger of the two
fixes the review offered ("or track which the user actually touched"),
required because the review's own regression-test wording ("neither is
written unless the user checks it") isn't satisfiable by a blanket
default alone. Also dropped the one cosmetic `Button variant="secondary"`
change round 1 flagged but didn't block on.

Self-tested with this repo's only available tools: `npm run build` clean,
`npm run lint` 150 errors / 1 warning, both figures identical to this
ticket's own recorded baseline, zero new. No automated frontend regression
test exists to add — confirmed fresh that `aiorders-admin-hub` has no test
framework, no `test` script, and zero test files anywhere in the repo;
proposal filed (`proposals.md`) rather than standing up a test harness
inside a bug-fix ticket. One observation filed (`observations.md`): a found
commit needs checking against the finding it was meant to close, not only
against the code.

Both branches committed (automation identity `businesspilotcare-gif`,
consistent with every prior commit on this ticket) and pushed:
`aiorders-api@57f8c4b`, `aiorders-admin-hub@63be255`. Frontmatter `branch:`
and `updated:` refreshed.

**0 net frontmatter transitions** — `state`/`owner` unchanged
(`building`/`eng-manager`): fixing a failed review's findings is build work,
and `in-review` is only reached by a fresh review-plus-quality session
actually passing it. `machine_wip` unaffected, still 4/1 (draining
naturally, unrelated to this pass). Approver-facing WIP and approval cap
both unaffected — no gate touched.

`chained: ENG-008` — `building` is agent-owned (the next hop is code review
+ quality, combined, round 2), not the approver, not blocked, not terminal,
not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-008`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: see below.

## 2026-08-31 — continue ENG-023: tech design written, held at `designed` by the WIP cap

`continue` event pass, context `ENG-023`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean (business-os `.env` → `MODE=active`; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-023`) and
whole-board: both exit 0, clean.

Picked up the hand-off the 2026-08-29 `designed`-entry left for this exact
session: the tech design itself, not yet written. Investigated the live
code first (`restaurant-portal`'s feedback page and API client,
`aiorders-api`'s `feedback.ts`/`catering.ts`/`utils.ts`/`index.ts`, the
`restaurant_feedback` migration history and its closest sibling precedent)
and confirmed first-hand the `getFeedback` tenant-isolation bug `ENG-022`
already found (wrong argument order into `verifyRestaurantAccess`, plus a
truthy-object check that never actually denies). Wrote
`agents/architect/designs/ENG-023-feedback-status-and-notes.md`: two new
columns on `restaurant_feedback` (`status`, `notes`), a new `update_feedback`
action modeled on `catering.ts`'s fetch→verify→update→return shape while
keeping `feedback.ts`'s own throw convention for failures (reasoned
explicitly against an apparent PRD/`ENG-022` conflict that resolves cleanly
once shape and error-convention are treated as separate questions), and a
non-blocking sequencing note with `ENG-022` on the access-check helper's
live name. One-way doors: none — status vocabulary and the no-audit-log
choice both decided directly, both reversible. No ADR: no one-way door, no
standards deviation, no accepted risk. Full detail on the ticket's own log.

**0 net frontmatter transitions** — `state`/`owner` unchanged
(`designed`/`architect`). The exit condition for `designed` is now met, and
with no one-way door this ticket's next stop would be `ready` directly, no
G2 — **not taken this pass.** Machine WIP re-verified fresh from every
ticket file's own frontmatter, not the cached header: `ENG-008`/`ENG-013`
`building`, `ENG-009`/`ENG-010` `ready` — 4/1, still over cap, still
draining naturally. Same precedent already on record for `ENG-014`/`ENG-015`:
a clean, one-way-door-free design still holds at `designed` until the count
clears. `ENG-023` now joins `ENG-014`/`ENG-015`/`ENG-025` there.

**Notify sweep:** nothing raised — no gate opened this pass. **Dead-end
sweep** (scoped to this event's contract): no broken chain on this ticket's
own prior entries beyond the one this pass resumed.

`chained: none` — `designed`, held by the machine WIP cap (4/1, re-verified
above), not blocked and not waiting on a human specifically, but firing
`continue ENG-023` now would only re-discover the same cap with no new work
to do. Re-check once a `scheduled`/`watch`/`continue` pass drains
`ENG-008`/`ENG-009`/`ENG-010`/`ENG-013` below the cap. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-023`) and
whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-30 — continue ENG-013: the missing test already existed, found undocumented rather than written

`continue` event pass, context `ENG-013` — the re-fire from the `scheduled`
sweep above. Narrow scope per the event's own contract (resume this ticket
from its current state; no board-wide sweep). Mode check clean. Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean.

Went to write the Deno test file round 1's code review asked for and found
one already on the branch: `foodswipe.test.ts`, commit `c95b25b`, same
automation identity (`businesspilotcare-gif`) as the ticket's own recorded
build commit, already pushed. Nothing in tracked state knew about it — not
this ticket's own log, not `business-os`'s own `git log` (`main` confirmed
0/0 with `origin/main`), not either dated trace log on this host. Root
cause, per `proposals.md`'s existing 2026-08-29 row: this instance runs on
two hosts and `traces/` is host-local and `.gitignore`d, so a pass that ran
on the other host, did the work, and pushed it leaves nothing here if it
never reached (or never pushed) its own ticket-log update. `deno` isn't
installed on this Mac host at all, so verification was by hand: read both
files in full and traced all 17 new test cases against the live handler
logic, confirming they correctly cover the three gaps round 1 named
(access-gate negative case, stage validation, `source='foodswipe'`
tenant-scoping) with no bugs found. Accepted the existing commit rather than
duplicating it; added a short PR-body addendum on the ticket noting the
file and two small additive fixes it carries (exported types, a
`Boolean(...)` wrap with no behavior change). Full investigation and
verification detail on `ENG-013`'s own ticket log.

**0 net frontmatter transitions** — `state` was `building` at pass start and
remains `building`: the work was already complete before this pass began,
so there was no further machine-owned state to advance into within this
same session regardless (`eng_build_loop.md`'s "a pass stops after
`building` on purpose" is state-based, not effort-based). `machine_wip`,
approver-facing WIP, and approval cap all unaffected — no gate raised or
resolved.

**Proposal filed** (`proposals.md`): a build hop has no step that checks a
ticket's recorded commit hash(es) against its remote branch before assuming
code still needs writing — cheap to add (`git log {hash}..origin/{branch}`
per linked repo), and would have surfaced this in one command instead of a
multi-step investigation. Distinct from the existing 2026-08-29 row (that
one is about a dropped-event incident item lacking detail; this is about a
pass that finished correctly and left no incident at all).

`chained: ENG-013` — `building` is agent-owned (the review+quality combined
hop is next), not the approver, not blocked, not terminal, not held by a
cap. Fired `/bin/zsh departments/engineering/lib/eng-trigger.sh continue
ENG-013` before exiting. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-30 — continue ENG-008: code review round 1 FAIL, bounced to building

`continue` event pass, context `ENG-008` — this fire's own turn at the front
of `traces/.pending`, re-fired by the `scheduled` sweep above after the
original 2026-08-29 fire never ran. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean.

Both branches were cut before `ENG-007`/`ENG-011` merged to `main` (this same
board's own `scheduled` entry above), so a raw two-dot diff against current
`main` shows spurious deletions of both tickets' shipped work. Read the
isolated single-commit patch on each branch instead (`git show --stat` /
merge-base diffing) to avoid reviewing noise that was never this ticket's.

Ran the code-review gate's automatic-failure scan: hit **#10** again —
`influencers.ts`'s new admin-gated `PATCH` path (`hasInfluencerAdminAccess`,
`updateInfluencer`) carries **zero test coverage**, identical shape to
`ENG-013`'s own round 1 failure one day earlier, same repo. Also found an
independent correctness bug: `Influencers.tsx`'s `openInfluencer` defaults
`accepts_paid`/`accepts_barter` via `null ?? !null`, which evaluates `true`
in JavaScript — so the 51/306 production rows where the preference is
genuinely unset get a fabricated "accepts paid" value written back on the
next save of *any* field, contradicting the migration's own deliberate
null-preserving backfill. Full detail on the ticket's own log. No receipt
written; findings logged on the ticket and in
`agents/principal-engineer/notebook/2026-08-30-review-log.md`. QA's hop not
run this round — discarded per the combined-hop design.

**0 net frontmatter transitions** — `state`/`owner` unchanged
(`building`/`eng-manager`); the gate was reached and immediately routed
back on the fail verdict. `machine_wip` unaffected, still 4/1.
Approver-facing WIP and approval cap both unaffected. Two observations filed
(`observations.md`): second occurrence of the automatic-failure-#10 shape in
two days (same repo, same handler family); `ENG-008`'s frontmatter missing
`time_estimate`/`time_spent`/`time_remaining` despite both
`definition-of-done.md` and the ticket template calling for them.

`chained: ENG-008` — `building` is agent-owned (both findings are the next
hop's work), not the approver, not blocked, not terminal, not held by a cap.
Fired `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-008`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-30 — scheduled (launchd): two silent merges shipped, three broken chains resumed

`scheduled` event pass, context `launchd`, the 15:30 safety-net slot (fired
15:46, delayed by an in-flight `continue ENG-023` attempt that ran until
13:00 and a lock hand-off after). Mode check clean (business-os `.env` →
`MODE=active`). This pass's own transcript was interrupted once mid-run by
the host machine sleeping — resumed from the same session, nothing lost.

**Found a rough day on disk before touching anything.** `git status` showed
six files uncommitted from the 2026-08-29 `watch` pass that processed
`ENG-023`'s G1 (never committed before this pass started) — read in full via
`git diff` before proceeding, confirmed coherent and already fully described
by that pass's own ticket-log and journal entries, left as-is to commit
together with this pass's own work rather than committed prematurely
mid-investigation. `traces/eng-loop-2026-08-30.log` showed `continue ENG-023`
had failed twice today (`401 OAuth access token has been revoked` at 02:13;
`ENOTFOUND` at 09:31, after only 5 file reads) and been **dropped after 3
attempts total** (across both days) — `inbox/2026-08-30-eng-events-dropped.md`
raised automatically by the trigger script itself, unnotified (its own first
notify attempt hit the same `ENOTFOUND` class of failure).

**Merge detection (step 5) run against every ticket sitting on an L1 PR or
possible PR, not just the one named by the failed `continue`** — this is
what a `continue` event's own narrower contract can never do, and exactly
why today's two failed `ENG-023` attempts left this undetected for hours:

- `ENG-007` (`ready-to-ship`, no gate item ever raised — blocked by a
  Saturday window-hold the same-day L1 correction had already made moot):
  `git merge-base --is-ancestor` **MERGED**; independently confirmed via
  `gh pr view 4` (`mergedAt: 2026-08-30T02:38:08Z`, approver's own account).
  Receipts verified fresh from disk (all 4 present), `eng-gate-check.sh
  ENG-007` exit 0. Carried `ready-to-ship → shipped → verified`. Release
  record: `agents/devops/releases/2026-08-30-aiorders-api-ENG-007.md`.
- `ENG-011` (`blocked`, merge request raised 2026-08-29, never answered —
  its own text told the approver a reply wasn't required): both repos
  checked independently — `aiorders-api` PR #3 **MERGED** 00:12:50Z,
  `aiorders-admin-hub` PR #3 **MERGED** 00:13:30Z, git ancestry confirmed on
  both before treating the ticket as shippable (first two-repo merge
  detection on this board). Receipts verified (3 + migration, all present),
  `eng-gate-check.sh ENG-011` exit 0. Carried `blocked → shipped →
  verified`. Merge-request item closed to `inbox/_handled/`. Release record:
  `agents/devops/releases/2026-08-30-ENG-011-aiorders-api-and-admin-hub.md`.

Both close-outs done to the same standard `ENG-006` set two days ago:
receipts checked before advancing (never trusted from the PR body alone),
what an L1-with-no-CI/CD project can honestly attest to at `shipped`
(deploy status recorded as unknown where no evidence exists, rather than
inferred), and acceptance criteria re-confirmed against the merged tree with
any live-only gap named and carried forward, not hidden. Both PRDs' `status`
moved to `verified`. Both journaled in `decision-journal.md`.

**Dead-end sweep found three broken chains, not one.** `ENG-023`'s own
`continue` chain (fired correctly at the end of the 2026-08-29 `watch`
entry above) is the one this pass was triggered to investigate — root-caused
(both failures infra-level, neither implicating the ticket) and re-fired,
with the diagnosis recorded in `inbox/2026-08-30-eng-events-dropped.md`
before re-firing, per that item's own recommendation. Checking the rest of
the board for the same shape (a ticket ending its last log entry with
`chained: ENG-XXX` and no evidence the fire ever ran) surfaced two more:
`ENG-008` (`building`, chained at end of its 2026-08-29 build entry, waiting
on the combined review+quality hop) and `ENG-013` (`building`, chained at
end of its code-review-fail entry, waiting on the missing test). Neither
`continue (ENG-008)` nor `continue (ENG-013)` appears anywhere in
`traces/eng-loop-2026-08-29.log` or `-30.log` — only `ENG-023`'s two failed
attempts and this pass ever drained. All three re-fired; the trigger queue's
own duplicate-collapse rule makes this safe even where a fire is merely
still queued rather than genuinely lost, so no risk of double-running any
hop. `ENG-007`'s own former hold (the Saturday window note in its prior log
entry) resolved itself via the merge discovery above rather than needing a
fourth chain-fire.

**4 tickets touched, 5 net transitions** (`ENG-007` ×2, `ENG-011` ×2,
`ENG-023` dead-end resume with no state change), all within per-ticket caps.
`machine_wip` 5/1 → 4/1 (`ENG-007` left the counted range; still over cap,
still draining naturally — `ENG-009`/`ENG-010`/`ENG-008`/`ENG-013` remain).
Approver-facing WIP 1/2 → 0/2, fully clear. Approval cap 1/3 → 0/3, fully
clear — both caps clear at once for the first time recorded on this board.

**Notify sweep:** `inbox/2026-08-30-eng-events-dropped.md` raised and
notified this pass (its own automatic first attempt had failed on the same
network error it was reporting); `notified:` stamped. Nothing else new to
raise or nudge.

**Observations filed** (`observations.md`, two rows): merge detection's
`continue`-vs-`scheduled`/`watch` coverage gap made concrete by today's
timeline; fifth and sixth data points of this approver merging L1 PRs
directly on GitHub rather than through the tracked channel.

**Chained:** `ENG-007` — none, terminal (`verified`). `ENG-011` — none,
terminal (`verified`). `ENG-008` — `ENG-008`, re-fired
(`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-008`).
`ENG-013` — `ENG-013`, re-fired (`/bin/sh .../eng-trigger.sh continue
ENG-013`). `ENG-023` — `ENG-023`, re-fired (`/bin/zsh .../eng-trigger.sh
continue ENG-023`). All three fires happen after this board update and the
commit that follows it, per this pass's own closing instructions. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: run clean
before the fires below (see traces for the exact invocation and output).

## 2026-08-29 — watch (launchd): ENG-023's G1 answered and processed, awaiting-scope → designed

`watch` event pass, context `launchd`. Mode check clean (business-os `.env`
→ `MODE=active`; instance `config/config.yaml` → `mode:` not set, falls
through). Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-023`) and whole-board: both exit 0, clean — run fresh, not taken on
any prior pass's own account.

**Swept all three watched inboxes per this event's own contract.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
`.gitkeep` — nothing new. `inbox/` held exactly two live items:
`2026-08-29-eng023-g1-scope.md`, found answered (**approved**, `decided:
2026-08-29T23:38:32.834274+00:00`, no additional comment) since the last
pass touched it; and `2026-08-29-eng011-merge-request.md`, re-checked fresh
and still unanswered (`decision:` empty) — never inferring approval from
silence, nothing to act on there.

**Found the repo mid-recovery from an unrelated `git stash pop` conflict**
on `_index.md`/`_index-archive.md`/`observations.md`
(`stash@{0}: On main: local instance state before marketing port pull`),
resolved to a clean tree matching `HEAD` by something else between this
pass's first and second `git status` check, mid-sweep. Out of scope for
this event — not touched; the stash itself is untouched too. Full detail in
`observations.md` and on `ENG-023`'s own ticket log.

Processed `ENG-023`'s G1: PRD `status: approved`
(`agents/product-manager/specs/ENG-023-feedback-status-and-notes.md`), gate
item moved to `inbox/_handled/` with a processed footer, journaled in
`agents/eng-manager/config/decision-journal.md`. Ticket `awaiting-scope →
designed`, `owner: approver → architect`. **Design work itself not started
this pass** — same reasoning `ENG-014`'s own `watch`-event G1 processing
used: implementation-adjacent work against a project with real customer
data belongs in a dedicated `continue ENG-023` session, not this event's
inbox-sweep scope. Full detail on `ENG-023`'s own ticket log.

**1 transition** (`awaiting-scope → designed`), well under the cap of 4.
Approver-facing WIP 2/2 → 1/2 (`ENG-023` off the count; `ENG-011`'s merge
request the one remaining slot). Approval cap 2/3 → 1/3 (`ENG-023`'s gate
item now in `inbox/_handled/`). Machine WIP unaffected, still 5/1 —
`designed` isn't in the counted range, and the cap already holds
`ENG-014`/`ENG-015` at `designed` for the same reason, so `ENG-023` joining
them there (rather than `ready`) once its design lands is expected, not a
new constraint.

**Capacity freed, not spent on anything else this pass** — same precedent
`ENG-014`'s `watch` entry set: dispatching the freed approver-facing
WIP/approval-cap slot onto a different waiting ticket (`ENG-016` through
`ENG-021`, all G1-drafted) is left for a future `scheduled`/`watch`/
`continue` pass.

One observation filed (`observations.md`): the concurrent git-stash-conflict
recovery found mid-sweep, and the reminder that this instance's board files
can change under a pass from outside the build loop entirely, not just via
the approver answering a gate.

`chained: ENG-023` — `designed`, owned by `architect`, an agent-owned
state; not the approver, not blocked, not terminal, not held by a cap
(design/shaping work is exempt from the machine-WIP limit). Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-023`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-023`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

<!-- merge note: local and remote independently appended new archive
  entries after this point (local through 2026-08-30, remote through
  2026-08-31). One exact duplicate — the `watch`: ENG-023's G1
  answered/processed entry (identical `decided:` timestamp, same
  duplicate-dispatch race noted on ENG-023's own board file) — was kept
  once (remote's `launchd` version, listed first below) and dropped from
  local's copy. Remote's newer (2026-08-31) entries are listed first,
  followed by local's remaining 2026-08-29/08-30 entries not present on
  remote; entries are not otherwise re-sorted across the two branches. -->

## 2026-08-30 — continue ENG-011: acceptance-check, `shipped → verified` (terminal)

`continue` event pass, context `ENG-011` — the ticket's own chain fired at
the end of the `blocked → shipped` pass, since `shipped` is
product-manager-owned next (`skills/acceptance-check/SKILL.md`). Narrow
scope per this event's own contract (resume this ticket from its current
state; no board-wide sweep). Mode check clean (business-os `.env` → `MODE=`
empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-011`) and
whole-board: both exit 0, clean.

Full detail in the ticket's own log. Summary: ran `acceptance-check` to
completion for the first time on this board. No browser access on this
host, so verification used three live paths instead — reading deployed
source at the merged commit (`git show origin/main:<path>`, no worktree
disruption to `ENG-013`/`ENG-008`'s own in-progress branches sitting in the
same `_eng` worktrees), sampling real production rows via the read-only
Supabase MCP connection, and one live unauthenticated `curl` against the
actual production endpoint. All 6 acceptance criteria verified PASS against
the live result, not the receipts — including two (the stage filter's
actual rendered control, and the non-staff-request rejection) QA's own test
plan had explicitly left as "not independently re-verified." No scope
creep found against the non-goals list. Cost confirmed at $0/month, matching
the PRD. Step 6b (continue an approved sequence) checked and does not apply
— no sequence named in this PRD.

**One live production issue found and routed, not blocking the acceptance
verdict**: the hourly `platform-analytics` cron (feeding the Cloudflare KV
cache this ticket's health column reads) has 401'd on every run since
`2026-08-30T01:00 UTC`, 7/7 as of this pass — a gateway-level auth failure,
not a defect in this ticket's own diff (onset predates this ticket's own
`decided:` timestamp; the cron's own code was never touched by this
ticket). Health data is correctly derived and was correctly cached as of
its last successful write (`00:00:06Z`), just going stale faster than the
~1h the design assumed. Filed as `agents/qa/bugs/BUG-001-platform-analytics-cron-401.md`
(P2, owner devops) and routed through `agents/eng-manager/proposals.md`
(2026-08-30 row) per `eng_build_loop.md` step 3 — a department-originated
finding, not something this pass is authorized to fix inline, and P2 per
`bug-triage/SKILL.md` doesn't send `ENG-011` back to `building` (nothing in
this ticket's own diff is what's broken).

**State: `shipped → verified`**, `owner: devops → eng-manager`. **1
transition**, well under the cap of 4. **Consequence:** `machine_wip`
unaffected (both states sit outside the counted `ready`..`ready-to-ship`
range). Approver-facing WIP and approval cap both unaffected — no gate
raised or answered on this ticket; `BUG-001`'s proposal rides the normal
weekly batch.

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for terminal state. No wider sweep — out of scope for a
`continue` event naming `ENG-011` specifically. **Notify sweep:** nothing
to raise (`verified` doesn't notify) or nudge. **Observation filed**
(`observations.md`): the no-browser-access substitution method, as a
reusable pattern for the next ticket that hits the same host gap.

`chained: none` — `verified` is terminal. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-011`) and
whole-board: both exit 0, clean, no `WAIVED:` lines. Board held three
dated entries (`continue ENG-023`, `continue ENG-008` round 2, `watch
(schtasks)`) before this one, so the oldest (`continue ENG-023`) was moved
to `_index-archive.md`, prepended under its header, to make room — leaving
three (`continue ENG-008` round 2, `watch (schtasks)`, this one), per the
keep-three rule.

## 2026-08-30 — watch (schtasks): swept all three inboxes, nothing new to act on

`watch` event pass, context `schtasks`. Per this event's own narrower
contract, swept `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`,
and `inbox/` only, acting on whatever is new — not a board-wide sweep. Mode
check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (this event
names no ticket to scope to): exit 0, clean.

**Swept all three inboxes fresh; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
`.gitkeep` plus their own `_handled/`/`_processed/` items, all already
accounted for on this board (most recently the partner-exposure finding
routed into `ENG-022`'s design, and `ENG-011`/`ENG-007`'s merge requests).
`inbox/` holds exactly the two G1 items the preceding `scheduled (schtasks)`
pass raised and this same day's later passes already recorded —
`2026-08-29-eng016-g1-scope.md` (`notified: 23:13:49`) and
`2026-08-29-eng017-g1-scope.md` (`notified: 23:13:50`) — read directly
again rather than trusted from the table: both still carry the unfilled
`## Decision — Filled in by the approver.` placeholder, ~47 minutes old as
of this pass, well under the 24h nudge threshold. The inbox change that
woke this poll was those two files' own creation; nothing new has arrived
since. Both tickets' own frontmatter confirmed fresh: `state:
awaiting-scope`, `owner: approver` on each, matching the table exactly.

**Merge detection:** no ticket is currently `blocked` on an L1 PR (fresh
frontmatter check: `ENG-008`/`ENG-013` `in-qa`, `ENG-009`/`ENG-010` `ready`,
none `blocked`) — nothing to check.

**Dispatch:** machine WIP still 4/1, over cap — no new ticket starts
regardless of To-do ordering. Unaffected by this pass.

**Dead-end sweep (scoped to this event):** nothing beyond the inbox sweep
above. `ENG-016`/`ENG-017` both correctly sit with the approver, owner
recorded — a valid human-wait, unchanged since the preceding pass. No
ticket touched, so no chain of this pass's own to check.

**Notify sweep:** nothing to raise (nothing new). Nothing to nudge — both
live G1s well under 24h. **Observation:** none — this exact pattern
(watch poll finding only already-notified, unanswered gate items) is
now well established on this board; not novel enough to file again.

No ticket state changed, no gate item was written. `chained: none` — this
pass advanced no ticket, so there is no hop of its own to fire. All WIP
figures unchanged (machine 4/1, approver-facing 2/2, both at/over their
caps as already recorded). Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines. Board held three dated entries (`continue
ENG-013` round 2, `continue ENG-023`, `continue ENG-008` round 2) before
this one, so the oldest (`continue ENG-013` round 2) was moved to
`_index-archive.md`, prepended under its header, to make room — leaving
three (`continue ENG-023`, `continue ENG-008` round 2, this one), per the
keep-three rule.


## 2026-08-29 — continue ENG-008: round 2, code review + quality combined hop, both PASS — `building → in-review → in-qa`

`continue` event pass, context `ENG-008`. Narrow scope per this event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
whole-board: both exit 0, clean.

Full detail in the ticket's own log. Summary: round 1's automatic-failure
#10 (no test on the new auth-gated write path) is closed
(`influencers.test.ts`, 17/17 passing, independently re-run from an
isolated copy rather than trusted from the log, since the shared
`_eng/aiorders-api` worktree was mid-flight on `ENG-013`'s branch at review
time). Automatic-failure scan otherwise clean (0/10). Diff shape, line
review, and test-quality review — none of which round 1 reached, since it
stopped at the first automatic-failure hit — all clear this round. The
regression fix (`Boolean(...)` wrap) was mutation-tested, not just read:
reverting it by hand reproduced the exact 16/17 failure the build pass's
own log described, then restored. QA's quality gate ran in the same
combined hop: `agents/qa/test-plans/ENG-008.md` written, all 8 PRD
acceptance criteria covered at least at the validation boundary, real gaps
named rather than hidden (no live-database round trip; narrow
success-path field coverage; two inspection-only branches) and none of
them blocking. `aiorders-admin-hub`'s lint/build independently re-run on
its own branch — exact match to the build pass's counts (150 pre-existing
lint errors, 0 new; clean build).

One new, non-blocking finding: the admin/sub-admin access-check shape is
now duplicated across three handler files written on three different
tickets today (`foodswipe.ts`, `loyalty-config.ts`, `influencers.ts`), with
two incompatible null-safety conventions live at once. This ticket
correctly matched its nearest same-day sibling rather than inventing a
fourth shape — filed as a proposal (`proposals.md`, `by:
principal-engineer`, size `S`) rather than fixed inline, since unifying
three files is a cross-cutting change this ticket didn't create.

**2 transitions** (`building → in-review → in-qa`), well under the cap of
4 — security is a separate hop by explicit config
(`machine_gates.sequential_after_quality`, needing QA's finished test plan
as its own input), so this pass stops here by design. **Consequence:**
machine WIP unaffected — `ENG-008` was and remains inside the counted
`ready..ready-to-ship` range (still 4/1, over the 2026-08-29 cap, draining
naturally as each in-flight ticket reaches `shipped`). Approver-facing WIP
and approval cap both unaffected — no gate raised.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing to raise (machine gates passing don't reach the
approver) or nudge. **Observation filed** (`observations.md`):
independently reproducing every self-tested number from the two prior
passes found zero discrepancies — a positive data point on this board's
own self-report reliability.

`chained: ENG-008` — `in-qa` is agent-owned (security is next, a fresh
session per `machine_gates.sequential_after_quality`) — not the approver,
not blocked, not terminal, not held by a cap. Fired
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-008`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean, no `WAIVED:`
lines. Board already held three dated entries (`ENG-022`, `watch
(schtasks)`, `continue ENG-023`) before this one, so the oldest
(`ENG-022`) was moved to `_index-archive.md`, prepended under its header,
to make room — leaving three (`watch (schtasks)`, `continue ENG-023`, this
one), per the keep-three rule.

## 2026-08-29 — continue ENG-023: design written, designed → designed, owner → eng-manager (no chain)

`continue` event pass, context `ENG-023` — the dedicated design session the
prior pass's own log named (`designed`'s exit condition is the architect's
own output, not board bookkeeping). Narrow scope per this event's own
contract. Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-023`) and
whole-board: both exit 0, clean.

**Investigated before designing**: `restaurant-portal`'s
`pages/feedback/Index.tsx` and `services/brandPortalApi.ts` in full;
`aiorders-api`'s `brand-portal/feedback.ts`, `catering.ts` (the PRD's named
model), `utils.ts`, and `index.ts`. Confirmed live via read-only Supabase
MCP queries (`bmnmnejwdxbcqinqkwko`): `restaurant_feedback` has no
`status`/`notes` column; its only trigger is `AFTER INSERT`-only (the
notification email — an `UPDATE` cannot re-trigger it); `catering.status`
is plain `text`, no CHECK/enum; `restaurant_feedback` already carries an
unwired `updated_at` column and this codebase has a reusable
`update_updated_at_column()` trigger already wired to six other tables.

**Design written**: `agents/architect/designs/ENG-023-feedback-status-and-notes.md`.
Two additive columns (`status text NOT NULL DEFAULT 'new'`, `notes text
NULL`), the existing `updated_at` trigger wired in, one new
`update_feedback` action modeled on `update_catering_request`'s
access-check shape but not its payload shape (see next paragraph). No RLS
change — service-role client, matching every sibling handler. **One-way
doors: none**, purely additive and reversible — no G2.

**Found and routed a defect in the ticket's own prescribed model, rather
than copying it into new code**: `catering.ts`'s `update_catering_request`
spreads the client's raw `updateData` directly into `.update()` with no
field allow-list — an already-access-checked caller could overwrite any
column on the row, including `restaurant_id`. `ENG-023`'s own new action
allow-lists `status`/`notes` explicitly instead. Filed as a proposal line
(`agents/eng-manager/proposals.md`, `by: architect`, `project:
aiorders-api`, size `S`) per step 3 — needs an already-authenticated
actor's deliberate misuse, not an open unauthenticated hole, so it doesn't
meet the P0 carve-out.

**State stays `designed`** — exit condition now met (design written, no
ADRs needed, one-way doors decided: none), so `owner` moves `architect →
eng-manager` per the state table; the state field itself doesn't advance
because machine WIP is still capped. **Re-checked fresh from each ticket's
own frontmatter**: `ENG-008` `building`, `ENG-013` `building`,
`ENG-009`/`ENG-010` both `ready` — still 4/1, over the 1-ticket cap,
unchanged. `ENG-023` joins `ENG-014`/`ENG-015`/`ENG-022`/`ENG-025` held at
`designed` for the same reason.

**Dead-end sweep:** nothing else to resume for this ticket, narrow scope
per this event's contract. **Notify sweep:** nothing to raise (no gate
opened) or nudge. **Observations filed:** none beyond the proposal above.

`chained: none` — held by the machine WIP cap (4/1, over the 1-ticket
limit). Re-check once `ENG-008`, `ENG-009`, `ENG-010`, or `ENG-013` reaches
`shipped`. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-023`) and whole-board: both exit 0, clean, no `WAIVED:`
lines. Board already held three dated entries (`ENG-010`, `ENG-022`,
`watch (schtasks)`) before this one, so the oldest (`ENG-010`) was moved to
`_index-archive.md`, prepended under its header, to make room — leaving
three (`ENG-022`, `watch (schtasks)`, this one), per the keep-three rule.

## 2026-08-29 — continue ENG-013: round 2, code review + quality combined hop, both PASS — `building → in-review → in-qa`

`continue` event pass, context `ENG-013`. Narrow scope per this event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean.

Full detail in the ticket's own log. Summary: round 1's automatic-failure
#10 (no test on the new authz-gated write path) is closed
(`foodswipe.test.ts`, 19/19 passing, independently re-run in place rather
than trusted from the log). Automatic-failure scan otherwise clean (0/10) —
one new, non-blocking `any` instance from the `hasFoodswipeAccess`
extraction, matching same-day precedent (`ENG-008`). Diff shape, line
review, and test-quality review — none of which round 1 reached — all
clear this round. The tenant-scoping assertion (round 1's own "what to
review hardest" line) was mutation-tested independently, not just read:
removing `.eq('source', 'foodswipe')` by hand reproduced exactly the two
failures the threat predicts, then reverted clean. QA's test plan
(`agents/qa/test-plans/ENG-013.md`) written in the same hop: all 5 PRD
acceptance criteria mapped, real gaps named (no live-database round trip;
1 of 6 stage values exercised through a successful write; "set then
reload" proven as two separate facts, not one end-to-end test), none
blocking. `aiorders-admin-hub`'s lint/build independently re-run on its own
branch (worktree switched over and back, since it was mid-flight on
`ENG-008`) — exact match to the build pass's counts (150 pre-existing lint
errors, 0 new; clean build, 3340 modules).

One correction, not a code finding: the build pass's own log described the
repo's 17 pre-existing `deno check` errors as "all in `users.ts`" —
re-verified fresh this round with each error's file isolated, the real
split is `auth.ts` (4), `partners.ts` (4), `users.ts` (9). The claim that
actually mattered (zero in files this ticket touches) still holds.

**2 transitions** (`building → in-review → in-qa`), well under the cap of
4 — security is a separate hop by explicit config
(`machine_gates.sequential_after_quality`), so this pass stops here by
design. **Consequence:** machine WIP unaffected — `ENG-013` was and
remains inside the counted `ready..ready-to-ship` range (still 4/1, over
the 2026-08-29 cap, draining naturally as each in-flight ticket reaches
`shipped`). Approver-facing WIP and approval cap both unaffected — no gate
raised.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing to raise (machine gates passing don't reach the
approver) or nudge. **Observation filed** (`observations.md`): the
ticket-log inaccuracy above (a self-reported aside wrong even though the
headline number and the load-bearing claim both held).

`chained: ENG-013` — `in-qa` is agent-owned (security is next, a fresh
session per `machine_gates.sequential_after_quality`) — not the approver,
not blocked, not terminal, not held by a cap. Fired
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-013`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean, no `WAIVED:`
lines. Board held three dated entries (`continue ENG-023`, `continue
ENG-008` round 2, `scheduled (schtasks)`) before this one, so the oldest
(`scheduled (schtasks)`) was moved to `_index-archive.md`, prepended under
its header, to make room — leaving three (`continue ENG-023`, `continue
ENG-008` round 2, this one), per the keep-three rule.

## 2026-08-29 — scheduled (schtasks): stale sequencing hold on ENG-009 lifted; ENG-016/ENG-017 G1s raised; stale "approval cap" corrected

`scheduled` event pass (the four-times-daily safety net), context
`schtasks`. Per this event's own contract, swept the whole board rather
than one ticket or the three inboxes alone. Mode check clean (business-os
`.env` → `MODE=` empty; instance `config/config.yaml` → `mode:` empty).
Pre-pass `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit
0, clean.

**Whole-board census taken fresh from every ticket's own frontmatter**
(`state`/`owner`/`priority`/`blocked_on`), not trusted from this table —
confirms no ticket is currently `blocked` (merge detection: nothing to
do), and machine WIP is unchanged at 4 (`ENG-008` `in-qa`, `ENG-009`/
`ENG-010` `ready`, `ENG-013` `building`). All three watched inboxes swept:
`agents/product-manager/inbox/`, `agents/eng-manager/inbox/`, and `inbox/`
each hold only already-processed items — nothing new to shape, propose, or
act on as a gate return.

**`ENG-009`'s sequencing hold was stale — the condition it names was
already met.** Its last three log entries all held it at `ready` pending
"`ENG-008` reaching `in-review` or later," each re-checked and correctly
found unmet at the time. `ENG-008` reached `in-review` and passed it
earlier this same day (`continue ENG-008` round 2, two entries above) and
now sits at `in-qa`— nobody had gone back to re-check `ENG-009` since.
Lifted the hold, fired `continue ENG-009` (queued behind the passes already
in flight — see below). `ENG-008`'s own chain (security next) was **not**
re-fired — it is already correctly recorded, and a second session against
the same ticket would race it. `ENG-010` re-checked in the same pass and
found still correctly held — its own design names it last of the three
influencer tickets, behind `ENG-009` as well as `ENG-008`, and `ENG-009`
has not built yet.

**Approver-facing WIP was genuinely 0/2** (confirmed fresh, not from the
header's own prior claim) — `ENG-014` and `ENG-015` have both reached
`designed`, clearing the two slots `ENG-016` and `ENG-017` were each
explicitly recorded as waiting behind. Raised both G1s
(`inbox/2026-08-29-eng016-g1-scope.md`,
`inbox/2026-08-29-eng017-g1-scope.md`), content drawn from each ticket's
already-fully-drafted PRD — no new readback needed. Ran
`lib/eng-notify.sh raise` on both (logged `SLACK_WEBHOOK_URL unset —
cannot notify`, non-fatal; items still live in `inbox/` and the control
center), stamped `notified:` on both, updated both PRDs' `status:` to
`awaiting-scope` and their `## Decision` sections, advanced both tickets
`shaped → awaiting-scope` with `owner → approver`. Order followed
`eng_build_loop.md` step 6 exactly: `ENG-016`'s `priority: next` outranks
the unset priority the rest of the backlog carries, then lowest-id among
the unset remainder (`ENG-017`) — filling exactly the two freed slots.
`ENG-018` (`priority: hold`) correctly excluded; `ENG-019`–`ENG-021` remain
queued behind.

**Also found and corrected: this board's own repeated "Approval cap 3"
framing is stale.** `config/config.yaml` → `wip` records `approval_cap` as
removed 2026-08-29 at the approver's own request — checked against that
file directly rather than propagated from this board's prior entries.
Corrected in the header and the "Waiting on the approver" section this
pass; **not** retrofitted into any individual ticket's own historical log
(those are point-in-time records of what was true when written — the cap
existed for most of today — and the append-only convention means they are
not rewritten after the fact). Also corrected `ENG-018`'s In-flight table
row: its own frontmatter carries `priority: hold`, but the table's Priority
column had read blank.

**Dead-end sweep:** `ENG-009`'s stale hold, above, is this pass's own
finding. Also checked `traces/.pending` and
`traces/eng-loop-2026-08-29.log` directly to understand the visible
backlog (`continue ENG-013`, several `watch schtasks`, `continue
ENG-011`/`ENG-007`/`ENG-008`) before assuming it meant anything was
broken: it doesn't. This pass's own launch is the `pass start: scheduled
(schtasks)` line at 22:52:30, and every fire arriving after that
(five `watch schtasks` polls, then this pass's own `continue ENG-009`)
correctly found the lock held and queued rather than raced it — the
mechanism is working exactly as `eng_build_loop.md`'s "chain" section
describes; the queue depth reflects several long (~1400s+) passes running
back-to-back against a 5-minute poll cadence, not a stall. Filed as an
observation rather than a proposal — confirms existing design, no fix
needed. No `exception-request:` found anywhere on the board.

**Notify sweep:** `ENG-016`/`ENG-017`'s raises are this pass's own, handled
above. No item anywhere carries `notified:` older than 24h without a
`decision:` or a prior `nudged:` — nothing to nudge.

**Observations filed** (`observations.md`): the confirmed-healthy
queue/lock mechanism under sustained back-to-back long passes; the
stale-approval-cap correction, in case the same phrasing recurs elsewhere
this sweep didn't check.

`chained: ENG-009` — the hold suppressing its chain is lifted; `ready` is
agent-owned. Fired
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-009`
(queued behind the existing backlog, per the lock — see above).
`ENG-016`/`ENG-017` land at `awaiting-scope`, owned by the approver — the
chaining guard does not fire on either. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board and scoped
(`ENG-009`, `ENG-016`, `ENG-017`, `ENG-010`): all exit 0, clean, no
`WAIVED:` lines. Board held only two dated entries before this one
(`continue ENG-023`, `continue ENG-008` round 2) — under the keep-three
limit, so nothing rolled to `_index-archive.md` this pass.

## 2026-08-29 — watch (schtasks): ENG-011 and ENG-007 both reconciled to `shipped` and confirmed deployed live; one new P1 proposal filed

`watch` event pass, context `schtasks`. Per this event's own contract, swept
all three watched inboxes for whatever was new or unprocessed, rather than
sweeping the whole board. Mode check clean (business-os `.env` → `MODE=`
empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board and scoped
(`ENG-007`, `ENG-011`): all exit 0, clean.

**`inbox/`** held exactly one live item: `ENG-011`'s L1 merge request,
carrying `decision: approved`/"merged" but never moved out of `inbox/` —
several earlier passes today (`ENG-007`'s and `ENG-025`'s own logs) had
already noticed this in passing and correctly deferred it as out of their
own narrower scope. **`agents/eng-manager/inbox/`** held one new architect
finding (P1, cross-tenant write exposure in `aiorders-api`'s
`admin-portal/handlers/restaurants.ts`, found during `ENG-015` design).
**`agents/product-manager/inbox/`** held nothing new.

**`ENG-011`:** both PRs' merge independently confirmed via git ancestry in
this department's own worktrees (not the control center's say-so) —
`aiorders-api` and `aiorders-admin-hub` branches both `MERGED` against their
`origin/main`. Went further than ancestry alone: read-only Supabase MCP
queries against `bmnmnejwdxbcqinqkwko` confirm the migration
(`20260829190000_add_last_order_at_to_platform_analytics`) is applied and
the live `calculate_platform_analytics()` already returns `last_order_at`;
the `admin-portal` edge function (redeployed 2026-08-30T02:47:37Z) contains
the derivation code; `aiorders-admin-hub`'s newly-added Cloudflare Pages
GitHub Actions workflow (added two commits after this ticket's own merge,
first run failed on environment scoping, second succeeded) deployed the
current `main` — this ticket's frontend change included. Advanced
`blocked → shipped`, `owner → devops`, wrote
`agents/devops/releases/2026-08-29-aiorders-admin-hub-ENG-011.md`, moved the
gate item to `inbox/_handled/` with a footer, journaled the decision.

**`ENG-007`:** already `state: shipped` via an earlier control-center
bypass ("ancestry not consulted," no release record, its own gate item
never formally answered through any channel). All three gaps closed rather
than left standing: independently confirmed merged via git ancestry
(`loyalty-system` → `origin/main`, `93617c6`); confirmed deployed live via
the same Supabase MCP checks (migration `20260829130000_restaurant_loyalty_configs`
applied, `restaurant_loyalty_configs` table present, the same `admin-portal`
redeploy above also carries this ticket's `loyalty-config` handler code —
one redeploy, two tickets); wrote the missing
`agents/devops/releases/2026-08-29-aiorders-api-ENG-007.md`; added a footer
to the never-answered gate item; journaled as a third control-center-bypass
variant (silent **and** bypassed, distinct from `ENG-002`'s silence-only and
`ENG-006`'s bypass-then-delayed-reply). `owner: approver → devops` to match.

**The new P1 finding** (partner write-exposure, same defect shape `ENG-015`
is already fixing but on the write path, in the same file) does not qualify
for the P0-only immediate-ticket carve-out — added as a line to
`agents/eng-manager/proposals.md` (Open) and moved to
`agents/eng-manager/inbox/_processed/`, per step 3. No id allocated, no
board row created.

**Consequence:** approver-facing WIP **2/2 → 0/2**; approval cap **2/3 →
0/3** — both fully free (see header). `machine_wip` unaffected (`blocked`
and `shipped` both sit outside the counted range) — still 4/1, over cap,
draining naturally.

**Dead-end sweep:** `ENG-007` sitting at an agent-owned state (`shipped`)
with no `chained:` record on its last log line is exactly the broken-chain
shape step 8 names — resumed here. No wider board sweep — out of scope for
this event's own narrower contract beyond the two tickets touched and the
one new inbox item.

**Notify sweep:** nothing raised this pass (no new gate item; reconciling a
bookkeeping gap and filing a proposal don't get notifications of their own).

**Observations filed** (`observations.md`): closing the loop on the
long-flagged `ENG-007`/`ENG-011` staleness; the `admin-portal` redeploy
carrying two tickets' code in one event; the new `aiorders-admin-hub`
Cloudflare Pages workflow (first CI/CD on this board, added mid-flight by
the approver directly).

`chained: ENG-011` and `chained: ENG-007` — both `shipped`, both
product-manager-owned next (`skills/acceptance-check/SKILL.md`), neither the
approver, blocked, terminal, or capped. Fired
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-011` and
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-007` before
exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`, whole-board
and scoped (`ENG-007`, `ENG-011`): see pass notes.

## 2026-08-29 — continue ENG-022: WIP-cap hold re-checked, still unmet, designed → designed (no chain)

`continue` event pass, context `ENG-022`. Narrow scope per this event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

`ENG-022` sits at `designed`, owner `eng-manager`; its own design log already
established no one-way door and no G2, so the next step is straight to
`ready`. Read `ENG-008`, `ENG-009`, `ENG-010`, `ENG-013` frontmatter directly
rather than trusting this file's header: `building`, `ready`, `ready`,
`building` — all unchanged, none has reached `shipped`. Machine WIP is still
4/1, over the 2026-08-29-corrected cap, and this file's own header already
names `ENG-022` inside the range (`ENG-014`–`ENG-025`) held at its current
backlog state until the count drains — so `designed → ready` does not happen
this pass. Checked all three inboxes for anything filed against `ENG-022`
specifically: both its own prior gate items are already in `_handled/`, and
the one live `agents/eng-manager/inbox/` item names it only as a comparison
point for an unrelated ticket/file — already classified out of scope by the
`ENG-010` pass, re-confirmed, left untouched.

**0 transitions.** State stays `designed`, owner stays `eng-manager`.
**Consequence:** machine WIP unaffected — still 4/1, over cap, draining
naturally. Approver-facing WIP and approval cap both unaffected — no gate
touched.

**Dead-end sweep (scoped to this event):** nothing to resume — deliberate
wait on a re-verified cap, not a stall. **Notify sweep:** nothing to raise
(no new gate item); nothing to nudge.

`chained: none` — held by the machine WIP cap (4/1, over cap; no new ticket
enters `ready` until it drains to ≤1). Re-check once one of
`ENG-008`/`ENG-009`/`ENG-010`/`ENG-013` reaches `shipped`. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-022`) and
whole-board: both exit 0, clean, no `WAIVED:` lines. Board already held
three dated entries (`ENG-013`, `ENG-009`, `ENG-010`) before this one, so
the oldest (`ENG-013`) was moved to `_index-archive.md`, prepended under its
header, to make room — leaving three (`ENG-009`, `ENG-010`, this one), per
the keep-three rule.

## 2026-08-29 — continue ENG-010: sequencing hold re-checked, still unmet, ready → ready (no chain)

`continue` event pass, context `ENG-010` — last of the approver's
hand-reordered queue (`continue ENG-008, continue ENG-013, continue ENG-009,
continue ENG-010`), all four now worked this pass sequence. Narrow scope per
this event's own contract (resume this ticket from its current state; no
board-wide sweep). Mode check clean (business-os `.env` → `MODE=` empty;
instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
whole-board: both exit 0, clean.

**Re-checked the sequencing hold's own condition rather than assuming it
still holds — same check just run for `ENG-009`, same result.** `ENG-010`
sits at `ready`, held pending `ENG-008` reaching `in-review` or later — both
tickets' designs extend the same not-yet-created
`admin-portal/handlers/influencers.ts`. Read `ENG-008`'s own frontmatter and
ticket-log tail directly: `state: building`, round-1's test gap closed this
same pass sequence (`aiorders-api@dc6972a`), round-2 review next, but not
yet `in-review`. Hold's condition still unmet. Checked
`agents/eng-manager/inbox/`, `agents/product-manager/inbox/` and `inbox/`
for anything newly filed against `ENG-010` specifically — none found (the
one item in `agents/eng-manager/inbox/`,
`2026-08-29-restaurant-detail-write-partner-exposure.md`, is unrelated,
out of scope for this event).

**0 transitions.** State stays `ready`, owner stays `eng-manager`,
`priority` stays empty. **Consequence:** machine WIP unaffected — verified
fresh from each counted ticket's own `state:` field: `ENG-008` `building`,
`ENG-009`/`ENG-010` `ready`, `ENG-013` `building` — still 4/1, over the new
cap, draining naturally per this file's own header. Approver-facing WIP and
approval cap both unaffected — no gate touched.

**Dead-end sweep (scoped to this event):** nothing to resume — deliberate
wait with a re-verified condition, not a stall. `ENG-008` (the dependency)
is already chained and progressing under its own event. **Notify sweep:**
nothing to raise (no new gate item); nothing to nudge.

`chained: none` — held for sequencing, unchanged from the prior entry:
`ENG-008` has not yet reached `in-review`. Re-check once it does. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
whole-board: both exit 0, clean, no `WAIVED:` lines. Board already held
three dated entries (`ENG-008`, `ENG-013`, `ENG-009`) before this one, so
the oldest (`ENG-008`) was moved to `_index-archive.md`, prepended under its
header, to make room — leaving three (`ENG-013`, `ENG-009`, this one), per
the keep-three rule.

## 2026-08-29 — continue ENG-009: sequencing hold re-checked, still unmet, ready → ready (no chain)

`continue` event pass, context `ENG-009` — draining the approver's
hand-reordered queue (`continue ENG-008, continue ENG-013, continue ENG-009,
continue ENG-010`) now that both `ENG-008` and `ENG-013` have been worked
this pass sequence. Narrow scope per this event's own contract (resume this
ticket from its current state; no board-wide sweep). Mode check clean
(business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
`mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`
(`ENG_ROOT` exported to the instance root), scoped (`ENG-009`) and
whole-board: both exit 0, clean.

**Re-checked the sequencing hold's own condition rather than assuming it
still holds.** `ENG-009` sits at `ready`, held pending `ENG-008` reaching
`in-review` or later — both tickets' designs extend the same not-yet-created
`admin-portal/handlers/influencers.ts`, and building `ENG-009` first risks
two engineers landing the same new file concurrently. Read `ENG-008`'s own
frontmatter directly rather than trusting this board's In-flight table:
`state: building`. Its round-1 test gap was closed this same pass sequence
(`aiorders-api@dc6972a`) and it re-enters code review next, but it has not
yet reached `in-review`. The hold's condition is therefore still unmet.
Checked `agents/eng-manager/inbox/`, `agents/product-manager/inbox/` and
`inbox/` for anything newly filed against `ENG-009` specifically — none
found.

**0 transitions.** State stays `ready`, owner stays `eng-manager`,
`priority` stays empty (per the approver's own reversal already recorded on
the ticket's own log). **Consequence:** machine WIP unaffected — verified
fresh from each counted ticket's own `state:` field: `ENG-008` `building`,
`ENG-009`/`ENG-010` `ready`, `ENG-013` `building` — still 4/1, over the new
cap, draining naturally per this file's own header. Approver-facing WIP and
approval cap both unaffected — no gate touched.

**Dead-end sweep (scoped to this event):** nothing to resume — this is a
deliberate wait with a re-verified condition, not a stall. **Notify sweep:**
nothing to raise (no new gate item); nothing to nudge.

`chained: none` — held for sequencing, unchanged from the prior entry:
`ENG-008` has not yet reached `in-review`. Re-check once it does. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-009`) and
whole-board: both exit 0, clean, no `WAIVED:` lines. Board already held
three dated entries (`ENG-025`, `ENG-008`, `ENG-013`) before this one, so
the oldest (`ENG-025`) was moved to `_index-archive.md`, prepended under its
header, to make room — leaving three (`ENG-008`, `ENG-013`, this one), per
the keep-three rule.

## 2026-08-29 — continue ENG-013: round-1 test gap closed, building → building (no chain state change, re-entering review next)

`continue` event pass, context `ENG-013`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean.

Same shape as the `ENG-008` entry directly above, same day, same automatic
failure (#10 — an authz-gated write path with no failure-case test). Switched
the `aiorders-api` worktree from `ENG-008`'s branch (clean, safe to leave) to
this ticket's own `feat/ENG-013-foodswipe-funnel-stage-control` and wrote
`supabase/functions/admin-portal/handlers/foodswipe.test.ts` (19 tests):
`hasFoodswipeAccess` unit tests, method/access-gate tests proving both new
write routes (`setStageOverride`/`resetStageOverride`) are gated, validation
tests, and — since this handler's write path chains **two** `.eq()` calls
(`id` then `source='foodswipe'`) rather than `ENG-008`'s one — a fake
Supabase client that **records** every `.eq()` call so the assertion is on
the tenant-scoping actually firing, the exact line round 1's review flagged
as "what to review hardest," not just on the response shape.

**The new tests caught the same bug class `ENG-008`'s round already found**:
`hasFoodswipeAccess` returned `undefined`, not `false`, for a profile with no
`additional_roles` (identical `&&`-short-circuit shape) — fixed in the same
hop (`Boolean(...)` wrap), no production impact. Second occurrence of this
exact pattern today; both logged in `observations.md`.

**Mutation-tested the tenant-scoping assertion itself** before trusting it
(`engineering-standards.md`'s "seen red for the reason it exists"):
temporarily removed `.eq('source', 'foodswipe')`, confirmed the scoping test
and its neighboring 404 test both failed, reverted, confirmed 19/19 clean
again. Self-tested: `deno check` clean on both files; whole-tree
`deno check admin-portal/handlers/*.ts` still 17 pre-existing errors, none in
files this ticket touches; `aiorders-admin-hub` untouched (round 1 read that
side clean). Committed and pushed: `aiorders-api@c95b25b`. Frontmatter
`time_spent`/`time_remaining` updated on the ticket.

**0 transitions** — `state` stays `building`: the gap is closed, but round-2
review is a fresh session's work by this loop's own design, same as round 1
was. **Consequence:** machine WIP unaffected — verified fresh from each
ticket's own `state:` field: `ENG-008` `building`, `ENG-009`/`ENG-010`
`ready`, `ENG-013` `building` — unchanged, still inside the counted range.
Approver-facing WIP and approval cap both unaffected — no gate touched.

**Dead-end sweep (scoped to this event):** no other ticket touched.
**Notify sweep:** nothing to raise or nudge — a machine gate re-entering
review doesn't reach the approver.

`chained: ENG-013` — `building` is agent-owned (round-2 code review next),
not the approver, not blocked, not terminal, not held by a cap. Fired
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-013` before
exiting; confirmed via `traces/eng-loop-2026-08-29.log` rather than assumed:
the fire hit the single-flight lock, found it held by this pass's own
still-running PID (1909), correctly declined to steal it, and queued at the
tail of `traces/.pending` (thirteenth behind a real backlog — `ENG-009`,
`ENG-010`, `ENG-022`, a G1 decision, `watch`×4, `ENG-023`, a merge-request
decision, `ENG-008`, `scheduled`). Not a broken chain — the same
still-running-PID shape this ticket's own code-review-round-1 entry already
documented; a later fire or the safety-net scheduled pass drains it once
this pass actually exits. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean, no `WAIVED:` lines. Board was at three dated
entries (`ENG-007`, `ENG-025`, `ENG-008`) before this pass — rolled the
oldest (`ENG-007`) to `_index-archive.md`, prepended under its header, to
make room, then added this entry — leaving three (`ENG-025`, `ENG-008`, this
one), per the keep-three rule.

## 2026-08-29 — continue ENG-008: round-1 test gap closed, building → building (no chain state change, re-entering review next)

`continue` event pass, context `ENG-008`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty) — run, along with the pre-pass gate
check, after the worktree edits rather than before (a procedural slip this
pass, noted on the ticket's own log rather than glossed over). Pre-pass
`departments/engineering/lib/eng-gate-check.sh` (`ENG_INSTANCE` exported;
the script takes `[ENG-NNN]` only, not an instance path — first attempt
passed the path positionally and fail-closed on `PARSE`, corrected before
trusting the result), scoped (`ENG-008`) and whole-board: both exit 0,
clean — still ahead of any board/ticket-log write this pass, so it served
its real purpose regardless of ordering.

Round 1 of code review (previous entry) found zero test coverage on the new
admin-auth-gated `PATCH`/`GET admin-portal/influencers/{id}` path. Both
worktrees confirmed on this ticket's own branch first (`e240767`/`f2ea36c`,
matching frontmatter). Wrote
`supabase/functions/admin-portal/handlers/influencers.test.ts`, same shape
as `loyalty-config.test.ts` (`ENG-007`, read off `origin/loyalty-system`
since that ticket is still unmerged): 5 `hasInfluencerAdminAccess` unit
tests, 2 access/method tests through `handleInfluencers` (403, 405) via an
`uncalledAuth()` throwing-`Proxy` helper, 8 `PATCH` rejection tests (one per
`EDITABLE_FIELDS` entry, `city_preference` getting two for its two distinct
validation branches, plus the empty-body guard), 1 successful-`PATCH` test
against a hand-built fake `adminSupabase` chain
(`.from().update().eq().select()`) — the first Supabase-client mock in this
repo; `loyalty-config.test.ts` named the same gap and left it open. Exported
`AuthenticatedRequest` and `hasInfluencerAdminAccess` (additive only) so the
test file could import them.

**The new test caught a real bug**: `hasInfluencerAdminAccess` returned
`undefined`, not `false`, for a profile with no `additional_roles` key (an
`&&` short-circuit issue) — a declared-`boolean`-return violation with no
production impact (sole call site only ever checks truthiness). Fixed in
the same hop (`Boolean(...)` wrap) since the function was already being
touched for its new `export`. Filed as its own row in `observations.md`.

**Self-tested**: `deno check` on both touched files — clean. `deno test` —
16/17 on the first run (the bug above), 17/17 after the fix. Whole-tree
`deno check admin-portal/handlers/*.ts` — 17 pre-existing errors, matching
the count the original building pass recorded, none in files this ticket
touches. `aiorders-admin-hub` untouched this pass (clean `git status`), no
re-test needed. Committed and pushed: `aiorders-api@dc6972a` (test file +
the `Boolean(...)` fix, one commit — same hop, same gap). Frontmatter
`branch:`/`time_spent:`/`time_remaining:` updated on the ticket.

**0 transitions** — `state` stays `building`: the gap is closed, but
round-2 review is a fresh session's work by this loop's own design, same as
round 1 was. **Consequence:** machine WIP unaffected — verified fresh from
each ticket's own `state:` field: `ENG-008` `building`, `ENG-009`/`ENG-010`
`ready`, `ENG-013` `building` = 4 inside the counted range, unchanged.
Approver-facing WIP and approval cap both unaffected — no gate touched.

**Noted, not reconciled** (third pass in a row to defer it, out of scope
for this ticket-scoped event): `ENG-007`'s own ticket file reads `state:
shipped` while this board's header and In-flight table still show it
`blocked` — same staleness `ENG-025`'s entry above already flagged.

`chained: ENG-008` — `building` is agent-owned (round-2 review is next, not
the approver, not blocked, not terminal, not held by a cap). Fired
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-008`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean, no `WAIVED:` lines.
Board holds three dated entries now (`ENG-007`, `ENG-025`, this one) — the
roll that keeps it at three (moving `ENG-015` to `_index-archive.md`)
already happened above, ahead of this entry's own addition, since the board
was at three before this entry and would otherwise have gone to four.

## 2026-08-29 — continue ENG-025: design written, designed → designed (capped, no chain)

`continue` event pass, context `ENG-025` — the ticket the immediately-
preceding `scheduled` pass named and chained by id. Narrow scope per this
event's own contract (resume this ticket from its current state; no
board-wide sweep). Mode check clean (business-os `.env` → `MODE=` empty;
instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-025`) and
whole-board: both exit 0, clean.

**Incidental discovery, not reconciled here (out of scope for this
ticket-scoped pass):** `ENG-007`'s own ticket file now reads `state:
shipped` (`blocked → shipped`, "control center, merge detected... recorded
on Harry's say-so; ancestry not consulted") though this file's own header
and In-flight table above still show it `blocked`, and its merge-request
inbox item still carries no `decision:` field. Same shape as the `ENG-011`
staleness `ENG-007`'s own pass logged earlier today. Flagged in
`observations.md`, not fixed here; both gate checks above still ran clean.

Did the architect's design work this ticket's prior entry deferred to a
dedicated session. Read `restaurant-portal` fresh from its `_eng` worktree
(clean on `eng/base`, fast-forwarded 2 commits behind `origin/main` —
confirmed both unrelated CI/deploy-workflow changes before merging).
Confirmed the PRD's evidence firsthand: `src/pages/feedback/Index.tsx`
fetches a restaurant's entire feedback history in one call with no
per-category breakdown; `RestaurantFeedback` already carries `type`
(non-null), `sub_type`/`nature` (nullable). Read `aiorders-api`'s
`brand-portal/feedback.ts` (worktree on `ENG-008`'s branch; `git diff
origin/main...HEAD --stat` confirmed that branch touches only
`admin-portal/handlers/influencers.ts` and its own migration, safe to read
without switching) and confirmed the PRD's access-check warning firsthand —
`getFeedback` calls `verifyRestaurantAccess` with arguments in the wrong
order and checks the result's truthiness instead of `.hasAccess`, same bug
class `ENG-022` already covers; separately flagged in `observations.md`
since it's unconfirmed whether `feedback.ts` is already one of that
ticket's named 5 handlers.

**Design conclusion: no backend change needed.** All three acceptance
criteria are answerable from data already in the browser. Wrote
`agents/architect/designs/ENG-025-feedback-recurring-issues.md`: one
exported pure function (`groupRecurringIssues`) plus one new "Recurring
Issues" `Card` section, both inside the existing `Index.tsx` — no new file,
no new backend action, no new table/column/migration, no one-way door, no
G2, no ADR. Full detail, including the three design calls the PRD left open
(recurrence threshold, windowing, keeping the helper inline), on the
ticket's own log.

**State stays `designed`** — exit condition met, but the flip to `ready`
belongs to whichever pass finds machine WIP clear, same convention
`ENG-014`'s and `ENG-015`'s own entries used. **`owner: architect →
eng-manager`.** **Not chained** — machine WIP verified fresh (each counted
ticket's own `state:` read directly, not the board header, per the
`ENG-007` discovery above): `ENG-007` `shipped` (outside range), `ENG-008`
`building`, `ENG-009`/`ENG-010` `ready`, `ENG-011` `blocked` (outside
range), `ENG-013` `building` — 4/1, still over the one-ticket cap.
`chained: none` — held by the machine WIP cap.

**0 net board consequence**: `machine_wip` unaffected (still 4/1 —
`designed` sits outside the counted range); approver-facing WIP and
approval cap both unaffected by this ticket's own transition (2/2, 2/3 per
this file's header — the `ENG-007` discovery above would lower both if
reconciled, but isn't acted on in this pass). In-flight table's `ENG-025`
row: Owner column updated to `eng-manager`, State unchanged.

Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-025`) and whole-board: both run clean, no `WAIVED:` lines. Board was
already at three dated entries (`ENG-014`, `ENG-015`, `ENG-007`) before this
one was added, so the oldest (`ENG-014`) was moved to `_index-archive.md`,
prepended under its header, to make room, then added this entry — leaving
three (`ENG-015`, `ENG-007`, this one), per the keep-three rule.

## 2026-08-29 — continue ENG-007: PR opened, ready-to-ship → blocked, L1 merge request raised

`continue` event pass, context `ENG-007`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`) and
whole-board: both exit 0, clean.

Per the approver's own override on this ticket's log (weekend/window checks
never applied to L1 in the first place) and the same-day correction to
`skills/release-runner/SKILL.md`, ran steps 1–4 fresh: all four upstream
gates re-confirmed `pass`, readiness gate already held, step 1 skipped for
L1, step 4 executed. Verified fresh in the department's `aiorders-api`
worktree (`git fetch`; `loyalty-system` still at `2aec86f`, unmerged; no PR
already open) before opening one: `gh pr create` → **PR #4**
(https://github.com/harsimranwalia/aiorders-api/pull/4, confirmed `OPEN`,
`main<-loyalty-system`). Wrote and raised
`inbox/2026-08-29-eng007-merge-request.md`; `lib/eng-notify.sh` hit the same
`SLACK_WEBHOOK_URL unset` gap every notify call has hit today, `notified:`
stamped by hand. Full detail on the ticket's own log.

**1 transition** (`ready-to-ship → blocked`, `blocked_on: approver`,
`blocked_from: ready-to-ship`, `owner: devops → approver`). **Consequence:**
machine WIP 5/1 → 4/1 (leaves the counted range); approver-facing WIP 1/2 →
2/2, at cap; approval cap 1/3 → 2/3. Board header, In-flight table, and
"Waiting on the approver" all updated to match.

**Noted, not reconciled** (out of scope for this ticket-scoped pass): while
reading `ENG-011`'s merge request as a formatting precedent, found it now
carries `decision: approved` and a trailing "merged" line — apparently
already resolved since this board's own header was last written. One
observation filed (`observations.md`) rather than acted on here.

`chained: none` — `blocked`, `blocked_on: approver`. Resume happens via the
build loop's own merge detection (step 5) on a future pass. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`) and
whole-board: both run clean. Board still holds three dated entries
(`ENG-014`, `ENG-015`, this one) — no roll needed.

## 2026-08-29 — continue ENG-015: design written, designed → designed (capped, no chain)

`continue` event pass, context `ENG-015` — the fire the immediately-preceding
`decision` pass on this same ticket re-queued after finding its predecessor's
chain had died mid-flight. Narrow scope per this event's own contract
(resume this ticket from its current state; no board-wide sweep). Mode check
clean (business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
`mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-015`) and whole-board: both exit 0, clean.

Did the architect's design work this ticket's prior entries had twice
deferred to a dedicated session — same shape as `ENG-014` directly above.
Read both repos fresh from the `_eng` worktrees (both sitting on `ENG-008`'s
branch; confirmed via `git diff origin/main...HEAD --stat` in each that it
touches only influencer-admin files, nowhere near `restaurants`/`brands`, so
safe to read without switching branches). Traced the two confirmed defects
to the exact code the PRD's Evidence names, and extended the fix to
`getRestaurantById()` (same file, same unconditional-service-role shape, not
named in the PRD's evidence paragraph but the same root cause) rather than
leaving a same-shaped hole beside the one being closed. Wrote
`agents/architect/designs/ENG-015-agency-reseller-brand-scoping.md`: two
additive RLS policies on `public.restaurants` (SELECT + INSERT, scoped
through the already-live `brands.partner_id`), a role branch in the two read
functions, and a frontend conditional so a partner-created restaurant lands
unapproved. No new table/column/vendor/role; no one-way door; no G2; no ADR.

**Found and did not fix a third, adjacent exposure**: `updateRestaurant()`/
`updateBrandOwner()`, same file, same defect shape, reachable today via two
partner-accessible pages neither the PRD nor this ticket's non-goals cover.
Filed as a finding rather than folded in or dropped:
`agents/eng-manager/inbox/2026-08-29-restaurant-detail-write-partner-exposure.md`
(`agent: architect`, P1 — real but not the P0 bar the step-3 carve-out
needs, so it goes through the normal proposal path). One observation also
filed (`observations.md`): whether the Brands page itself already scopes to
a partner's own brands is unconfirmed (`public.brands`' own RLS is likewise
absent from tracked migration history) — not chased further, out of this
PRD's named scope.

**State stays `designed`** — exit condition met, but the flip to `ready`
belongs to whichever pass finds machine WIP clear. **`owner: architect →
eng-manager`**, same convention `ENG-014`'s entry above used. **Not
chained** — machine WIP verified fresh (each counted ticket's own `state:`
read directly, not the board header): `ENG-007` `ready-to-ship`, `ENG-008`
`building`, `ENG-009`/`ENG-010` `ready`, `ENG-013` `building` — 5/1, still
over the corrected one-ticket cap, unchanged since `ENG-014`'s own design
pass found the same count. `chained: none` — held by the machine WIP cap.

**0 net board consequence**: `machine_wip` unaffected (still 5/1 —
`designed` sits outside the counted range); approver-facing WIP and approval
cap both unaffected (1/2, 1/3). In-flight table's `ENG-015` row: Owner
column updated to `eng-manager`, State unchanged.

Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-015`)
and whole-board: both exit 0, clean, no `WAIVED:` lines. Board held four
dated entries once this one was added (`ENG-023` watch, `ENG-008`, `ENG-014`,
this one) — moved the oldest (`ENG-023` watch) to `_index-archive.md`,
prepended under its header, per the keep-three rule.

## 2026-08-29 — continue ENG-014: design written, designed → designed (capped, no chain)

`continue` event pass, context `ENG-014` — this fire's own turn, resuming the
ticket from its current state per the event's own narrower contract (no
board-wide sweep). Mode check clean (business-os `.env` → `MODE=` empty;
instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-014`) and
whole-board: both exit 0, clean.

Did the architect's design work this ticket's prior entries had twice
deferred to a dedicated session: read both repos fresh from the `_eng`
worktrees (`restaurant-portal` clean on `eng/base`; `aiorders-api` clean but
sitting on `ENG-008`'s branch — confirmed via `git diff origin/main...HEAD
--stat` that branch never touches anything this design reads, so safe to
read without switching branches), traced `url-shortener/index.ts`'s
admin-only gate, confirmed `_shared/restaurantAccess.ts` already exists and
is already consumed by `api-key-auth` for the identical "restaurant-scoped
path beside an admin-gated function" shape, and confirmed all three of
`aiorders-admin-hub`'s existing QR-fetch call sites resolve to only two
distinct `destination_url`s, matching the PRD's own two-QR-type non-goal.
Wrote `agents/architect/designs/ENG-014-restaurant-qr-media-self-service.md`:
one new restaurant-scoped `url-shortener` action, two ported (not shared)
frontend generator components, one new `restaurant-portal` page. No new
table/column/vendor/migration; no one-way door; no G2; no ADR.

**State stays `designed`** — its exit condition is now met, but the flip to
`ready` is that state's own owner's job. **`owner: architect → eng-manager`**,
naming the next actor, same convention `ENG-022`'s equivalent entry used.
**Not chained** — machine WIP verified fresh at 5/1 (over the corrected
1-ticket cap), and the board's own header already names `ENG-014` by name as
held at `designed` until that count clears; firing the next hop now would
only re-derive that same fact. Full reasoning, including why this differs
from `ENG-022`'s own chain-then (not capped at that moment), is on the
ticket's own log. `chained: none` — held by the machine WIP cap.

**0 net board consequence**: `machine_wip` unaffected (still 5/1 — `designed`
sits outside the counted `ready`...`ready-to-ship` range); approver-facing
WIP and approval cap both unaffected (1/2, 1/3). In-flight table's `ENG-014`
row: Owner column updated to `eng-manager`, State unchanged.

One observation filed (`observations.md`): this pass checking the WIP cap
before deciding to chain, contrasted with the `continue ENG-024` row that
didn't and paid a wasted hop for it.

Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-014`)
and whole-board: both exit 0, clean, no `WAIVED:` lines. Board still holds
three dated entries (this one, `ENG-023` watch, `ENG-008`) — no roll needed.

## 2026-08-29 — continue ENG-008: code review round 1 FAIL, bounced to building

`continue` event pass, context `ENG-008` — this fire's own turn at the front
of `traces/.pending` finally reached. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
whole-board: both exit 0, clean.

Read the diff fresh from both worktrees — both already sitting on this
ticket's own branch (`feat/ENG-008-influencer-admin-management` at
`e240767`/`f2ea36c`, tree clean, matching frontmatter exactly), so no
checkout was needed, just `git fetch origin main` + `git diff
origin/main...HEAD` in each. Ran the code-review gate's automatic-failure
scan first: hit **#10**, the same number `ENG-013` hit earlier today — the
new `PATCH /admin-portal/influencers/{id}` (admin/sub-admin gated, six
validated fields) carries **zero test coverage**, against the same
in-repo precedent (`ENG-007`/`ENG-011`) `ENG-013`'s own finding cited. No
receipt written; verdict and finding logged on the ticket and in
`agents/principal-engineer/notebook/2026-08-29-review-log.md`. QA's hop
not run this round — discarded per the combined-hop design.

**0 net frontmatter transitions** — `state`/`owner` unchanged
(`building`/`eng-manager`); the gate was reached and immediately routed
back on the fail verdict. `machine_wip` unaffected, still 5/1.
Approver-facing WIP and approval cap both unaffected. `time_estimate`/
`time_spent`/`time_remaining` backfilled on the ticket frontmatter this
pass (never previously set); `time_estimate` taken from the PRD's own Cost
section, not invented.

One observation filed (`observations.md`): second code-review failure on
this board, same day, same automatic-failure number and shape as
`ENG-013` — worth treating a third occurrence as a real gap rather than a
third isolated data point.

`chained: ENG-008` — `building` is agent-owned (the missing test is the
next hop's work), not the approver, not blocked, not terminal, not held by
a cap. Fired `/bin/sh departments/engineering/lib/eng-trigger.sh continue
ENG-008` before exiting. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
whole-board: both exit 0, clean, no `WAIVED:` lines.

**Board rolled**: the live index held four dated entries once this one was
added (`ENG-011`, `ENG-013`, `ENG-023` watch, this one) — moved the oldest
(`continue ENG-011`) to `_index-archive.md`, prepended under its header,
per the keep-three rule.

## 2026-08-29 — continue ENG-013: code review round 1 FAIL, bounced to building

`continue` event pass, context `ENG-013` — this fire's own turn at the front
of `traces/.pending` finally reached. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean.

Read the actual diff fresh from both worktrees via `git diff`/`git show`
against the branch (`aiorders-api@ac4efba`, `aiorders-admin-hub@a1c3bdf`)
rather than checking either worktree out — both were sitting on `ENG-008`'s
branch, same as the building pass itself found. Ran the code-review gate's
automatic-failure scan before any deeper review: hit **#10** — the two new
authz-gated write actions (`setStageOverride`/`resetStageOverride` in
`foodswipe.ts`, tenant-scoped by `.eq('source', 'foodswipe')`, the diff's
own "review hardest" line) carry **zero test coverage**, against direct
precedent from `ENG-007`/`ENG-011` on this same repo. No receipt written;
verdict and finding logged on the ticket and in
`agents/principal-engineer/notebook/2026-08-29-review-log.md`. QA's hop not
run this round — discarded per the combined-hop design.

**0 net frontmatter transitions** — `state`/`owner` unchanged
(`building`/`eng-manager`); the gate was reached and immediately routed
back on the fail verdict. `machine_wip` unaffected, still 5/1.
Approver-facing WIP and approval cap both unaffected. One observation filed
(`observations.md`): first code-review failure recorded on this board.

`chained: ENG-013` — `building` is agent-owned (the missing test is the
next hop's work), not the approver, not blocked, not terminal, not held by
a cap. Fired `/bin/sh departments/engineering/lib/eng-trigger.sh continue
ENG-013` before exiting. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-29 — continue ENG-011: both L1 PRs opened, ready-to-ship → blocked

`continue` event pass, context `ENG-011` — this fire's own turn at the front
of `traces/.pending`. Narrow scope per the event's own contract (resume this
ticket from its current state; no board-wide sweep). Mode check clean
(business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
`mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-011`) and whole-board: both exit 0, clean.

Read the current `skills/release-runner/SKILL.md` rather than the release-
window question this ticket's own prior log entry had left open: the skill
was corrected earlier today to state that the window check is L2/L3-only and
never applies to L1, and both of this ticket's projects are L1 — so no hold
applied. Verified all four upstream gates fresh from their own receipt files
(migration, code review, quality, security — all **pass**, one named
non-blocking gap on the missing live-Postgres run). Re-checked both `_eng`
worktrees before touching them (both were sitting on `ENG-008`'s branch, not
this ticket's — confirmed clean first so nothing of `ENG-008`'s was at risk),
checked out `feat/ENG-011-client-stage-health-visibility` in both, confirmed
commit hashes matched every receipt exactly, checked for an already-open PR
on each repo (none), then opened both: `aiorders-api`
https://github.com/harsimranwalia/aiorders-api/pull/3,
`aiorders-admin-hub` https://github.com/harsimranwalia/aiorders-admin-hub/pull/3.
Restored both worktrees to `ENG-008`'s branch afterward. Wrote the merge
request (`inbox/2026-08-29-eng011-merge-request.md`), ran `eng-notify.sh
raise` (hit the same standing `SLACK_WEBHOOK_URL unset` gap every gate item
today has hit — not new), stamped `notified:` by hand. Ticket →
`ready-to-ship → blocked`, `blocked_on: approver`, `blocked_from:
ready-to-ship`, owner `devops → approver`. Full detail on the ticket's own
log.

**1 transition**, well under the cap of 4. `machine_wip` 6/1 → 5/1 (`ENG-011`
now outside the counted range). Approver-facing WIP 1/2 → 2/2 (at the limit,
not over — an already-gated ticket reaching its next gate, not a new start,
same reasoning `ENG-005` used at this identical boundary). Approval cap
1/3 → 2/3.

One observation filed (`observations.md`): the skill correction and this
ticket's own prior log entry disagreed on an open policy question, and the
current skill file is what should win — worth a future pass trusting that
ordering rather than re-litigating a stale ticket-log note.

`chained: none` — `blocked`, `blocked_on: approver`; the human gate this hop
was driving toward. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-011`) and whole-board: exit 0, clean, no `WAIVED:` lines.

## 2026-08-29 — continue ENG-024: shaped, held — machine WIP still 6/1 over cap, no slot free

`continue` event pass, context `ENG-024` — its own chain fire from the
`intake` pass that shaped it. Narrow scope per this event's own contract:
this ticket only. Mode check clean (business-os `.env` → `MODE=` empty;
instance `config/config.yaml` → `mode:` empty). Pre-pass gate check: exit
0, clean, both scoped (`ENG-024`) and whole-board.

Re-checked fresh rather than trusted the board's cached header: all six
machine-WIP tickets' own frontmatter (`ENG-007` ready-to-ship, `ENG-008`
building, `ENG-009` ready, `ENG-010` ready, `ENG-011` ready-to-ship,
`ENG-013` building) — count unchanged at 6/1, still over the cap of 1. Per
`eng_build_loop.md` step 6, the To-do column is the only place a new start
is drawn from, and "there is exactly one slot [that] does not free until
the ticket occupying it reaches `shipped`" — `ENG-024` (severity P1, fast
lane, `shaped`) cannot enter `building` this pass regardless of severity;
nothing in the loop's dispatch rule exempts P1 from the WIP cap. Only the
unrelated proposal-batching P0 carve-out (step 3) mentions P0 at all, and
that gate doesn't apply here since ENG-024 already has an approved ticket.
`agents/eng-manager/inbox/` empty — no technical-intake item for this
ticket; G1 was already correctly auto-skipped (bug type, fast lane), so
there is no gate item to check either. Ticket correctly stays at `shaped`.

**0 transitions.** `chained: none` — held by the machine WIP cap (6/1, no
free slot); one of the explicit do-not-chain conditions. Recorded on the
ticket's own log.

One observation filed (`observations.md`): the `intake` pass that shaped
this ticket fired its chain without checking the machine-WIP cap, which was
already known full at the time (six tickets already in flight) — this pass
is the cost of that gap, one hop spent to re-derive a hold the shaping pass
could have recognized itself.

Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-024`) and whole-board: exit 0, clean, no `WAIVED:` lines.

## 2026-08-29 — continue ENG-022: architect's design written, shaped → designed

`continue` event pass, context `ENG-022` — this fire's own turn at the
front of `traces/.pending`, reached after the approver's plain "approved"
acknowledgement on the P0 incident notice (no priority change, nothing
else to act on). Narrow scope per this event's own contract — this ticket
only. Mode check clean. Pre-pass gate check: exit 0, clean, both scoped and
whole-board.

Read the live `aiorders-api` worktree before designing against it rather
than trusting the PRD's summary alone; confirmed all 19 broken call sites
and the 4 correct contrast files match exactly. Found one thing the PRD
didn't surface: `utils.ts` already contains a correct, unused throwing
wrapper (`verifyRestaurantAccessLegacy`, called from nowhere in the repo) —
promoted it (renamed, `@deprecated` dropped) instead of designing a new one.
Design written: `agents/architect/designs/ENG-022-brand-portal-tenant-isolation-broken.md`
— fixes each of the 5 broken files per its *own* pre-existing error
convention (throw vs. `{success:false}`) rather than unifying all 9, which
would be a refactor bundled into a P0 bug fix. Test plan: colocated
`Deno.test` files with a stubbed Supabase client, proving the negative case
per call site with no live project and no new CI wiring. No one-way door,
no ADR. Full detail on the ticket's own log.

**1 transition** (`shaped → designed`), well under the cap. `ENG-022` stays
short of the counted `ready..ready-to-ship` machine-WIP range (6/12
unaffected); `security`-typed, no G1/G2 raised, approver-facing WIP and
approval cap both unchanged (1/2, 1/3).

One observation filed (`observations.md`): `brand-portal/`'s two
pre-existing, unrelated error-response conventions, so a future pass
doesn't mistake the split for something this ticket introduced.

`chained: ENG-022` — `designed`, owned by `eng-manager` next (no one-way
door, so `awaiting-decision` does not apply), an agent-owned state; firing
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-022`
before this pass exits. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-022`) and
whole-board: exit 0, clean, no `WAIVED:` lines.

## 2026-08-29 — scheduled schtasks: safety-net sweep — processed ENG-025's G1, raised ENG-023's, recovered five passes of uncommitted work

`scheduled` event pass, context `schtasks` — the four-times-daily safety-net
sweep, drained immediately behind the `decision ENG-015` pass above in the
same held lock (`traces/.loop.lock/pid 1909`, confirmed alive throughout).
Whole-board sweep per this event's own contract, not one named ticket. Mode
check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

**Business/technical intake:** `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/`, and `inbox/requests/` all empty. Nothing to
shape, nothing to batch as a proposal.

**Gate returns:** `inbox/` held exactly one file,
`2026-08-29-eng025-g1-scope.md` (`decision: approved`,
`decided: 2026-08-29T22:22:18.827452+00:00`). Processed:
`ENG-025` `awaiting-scope → designed`, owner `approver → architect`; PRD
`status: approved`; gate item moved to `inbox/_handled/`; journaled
(`decision-journal.md`). That freed both the approver-facing WIP slot and
the approval-cap slot ENG-025 held — reused in this same pass, per
`_index.md`'s own standing note, to raise `ENG-023`'s G1 (fully drafted
already in its PRD's Decision section, nothing written fresh): `ENG-023`
`shaped → awaiting-scope`, owner `product-manager → approver`;
`inbox/2026-08-29-eng023-g1-scope.md` raised, `eng-notify.sh raise` run
(logged `SLACK_WEBHOOK_URL unset`, same open gap every gate item today has
hit), `notified:` stamped manually. Net: approver-facing WIP and approval
cap both end this pass exactly where they started (1/2, 1/3), now against
`ENG-023` instead of `ENG-025`. `ENG-016`–`ENG-021` (also G1-drafted)
deliberately left unraised — see `ENG-023`'s own log for why only the one
explicitly-earmarked ticket was raised rather than filling every free slot.

**Merge detection:** no ticket sits at `blocked` anywhere on the board — no
L1 PRs to check ancestry on this pass.

**Dispatch / dead-end sweep, whole board:** `ENG-007` (`ready-to-ship`)
re-confirmed correctly held — release window still closed (Saturday);
resumes naturally Monday. `ENG-009`/`ENG-010` (`ready`) re-confirmed
correctly held pending `ENG-008` reaching `in-review` or later — neither
worktree shows a branch or build started yet. `ENG-011`'s
`chained: ENG-011` already fired and sits genuinely queued in
`traces/.pending`, not stale. No broken chain found on any in-flight
ticket beyond the two already repaired by the two passes immediately
above. Removed `_index-archive.md.tmp.4632.31c9ee9459a2`, the stale
5,027-line crash-artifact temp file `observations.md`'s immediately
preceding row flagged as safe to clear on a dead-end sweep — verified
against that row's own description (size, mtime, stale content) before
deleting.

**Uncommitted-work recovery, the main substance of this pass.** Pre-pass
`git status` showed nothing committed since `a143d9b` despite the board's
own narrative recording five further passes' worth of real, verified work
since: `continue ENG-008` (built the influencer admin-edit path),
`continue ENG-013` (built the FoodSwipe stage-override path), the
`ENG-014`/`ENG-015` chain repairs, and the `ENG-022`/`ENG-023` incident/
question processing — including the `eng-loop-halted` repair pass's own
config-path fix for `read_plan_budget()` (the actual cause of today's
40-hop ceiling firing early). That repair pass's own log states it
committed three of those files "alongside this pass's own changes," but a
fresh `git status` at this pass's start showed all three still modified —
the commit most likely never ran. Verified each change against its own
ticket log before trusting it (per this instance's standing practice, and
the specific lesson `observations.md` names for exactly this shape of
mismatch) rather than committing blindly. Committed the accumulated,
verified work in this pass — see the commit itself for the exact file
list; the stray temp file above was deleted, not committed, and nothing
else in the tree looked suspicious (no secrets, no `.env`, no unrelated
files). Filed as its own `observations.md` row for the pattern (a pass's
own narrated git action not matching the filesystem — a new variant of an
already-seen lesson).

**Notify sweep:** `ENG-023`'s new item raised and stamped this pass (see
above). No item found with `notified:` older than 24h and no `decision:` —
nothing to nudge. Approval cap 1/3, not full — no stall.

**Journal:** `ENG-025`'s G1 answer added to `decision-journal.md`.

`chained: ENG-025` — fired this pass (see that ticket's own log);
`ENG-023` and all `ready`/`ready-to-ship` tickets correctly recorded
`chained: none` (approver-owned or deliberately held) and are not
re-chained here. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

## 2026-08-29 — decision ENG-015: G1 already processed by the same dying `watch` pass as ENG-014, its own recorded chain never fired either — repaired

`decision` event pass, context `2026-08-29-eng015-g1-scope.md` — this
event's own queued fire, drained behind the `decision ENG-014` repair pass
immediately before it (`pass end: decision (exit 0, 685s)` at 15:33:53 →
`draining queued event: decision (2026-08-29-eng015-g1-scope.md)`,
15:34:45, no gap, one duplicate collapsed). Mode check clean. Pre-pass gate
check: exit 0, clean, scoped (`ENG-015`) and whole-board.

Exactly the gap the immediately-preceding pass predicted and flagged in
`observations.md`: `ENG-015`'s G1 was genuinely fully processed (approved,
`awaiting-scope → designed`, owner `architect`, journaled — all verified
fresh against `inbox/_handled/`, the PRD, and `decision-journal.md` rather
than trusted), but its own recorded `chained: ENG-015` line never actually
fired — same dying `watch` pass (pid 36150), same absence from
`traces/eng-loop-2026-08-29.log` and from `traces/.pending` beforehand.

**Action:** re-fired `/bin/sh
departments/engineering/lib/eng-trigger.sh continue ENG-015` directly.
Confirmed on `traces/.pending` afterward (`1 continue ENG-015`) and via
`traces/.loop.lock/pid` (`1909`) confirmed alive with `ps -W` — queued
correctly behind this still-running pass rather than lost again. No ticket
state changed.

**0 transitions**, no cap impact — this was a chain repair, not new gate
or state movement. This closes out both halves of the pair `ENG-014`'s own
repair pass surfaced; no further tickets carry this shape as far as this
pass found.

`chained: ENG-015` — re-fired and confirmed queued this pass (see above).
Post-pass gate check: exit 0, clean, both scoped and whole-board. Full
detail on the ticket's own log
(`agents/eng-manager/board/ENG-015-agency-reseller-brand-scoping.md`).

## 2026-08-29 — continue ENG-013: built the stage-override column, handler, and UI across both repos, ready → building

`continue` event pass, context `ENG-013`, its turn at the front of
`traces/.pending` finally reached. Narrow scope per the event's own
contract. Mode check clean.

Pre-pass gate check arrived flagged (exit 2, all of `ENG-013`..`ENG-024`
reported "not a regular file"). Investigated rather than trusted: `stat`
confirmed every file is a normal regular file, and a fresh re-run (scoped
and whole-board) returned exit 0 clean. Transient — the injected report was
captured mid-write during the prior pass's own commit
(`1a6fe83`). Nothing to fix.

Both `_eng` worktrees existed, sitting on `feat/ENG-011-...` (still owed —
`ENG-011` hasn't opened its PR yet). `aiorders-admin-hub` carried the same
benign `package-lock.json` `peer:true` drift `ENG-011`'s own recovery
already named — stashed, labeled, not discarded, not committed. Branched
both repos fresh off `origin/main` as `feat/ENG-013-foodswipe-funnel-stage-control`.

Built per the design: one nullable `foodswipe_stage_override` column on
`profiles` (six-value `CHECK`); `classifyStage()`'s caller now prefers it;
two new gated, source-scoped write actions
(`/foodswipe/stage/{set,reset}`) in `aiorders-api`. Per-card stage dropdown
+ dialog (styled after `Leads.tsx`) and a "Manually set" badge in
`aiorders-admin-hub`. Self-tested: `deno check` clean, `npm run lint`
(zero new issues — the repo's 150 pre-existing errors are all in files
this ticket didn't touch), `npm run build` clean. Live-verified read-only
via Supabase MCP against the real `aiorders-api` project
(`bmnmnejwdxbcqinqkwko`): schema assumptions, table scale (528 rows, 36
`source='foodswipe'`), and non-applied migration status all confirmed.
Database migration doc written
(`agents/database/migrations/ENG-013-foodswipe-funnel-stage-control.md`).
Both branches committed and pushed; PR bodies drafted in the ticket's own
log (no PR opened yet — that's devops's release step). Artifact-enumeration
grep for "foodswipe" across instance+department docs found no
instruction/map conflicts, only one harmless location-citation drift in
`ENG-009`'s design doc, left alone.

**1 transition** (`ready → building`), well under the cap — the next hop
(review + quality, combined) is a fresh session's work by design. No cap
change; `ENG-013` stays inside the counted `ready..ready-to-ship` range.

`chained: ENG-013` — `building` is agent-owned (principal-engineer + qa
next). Fired `continue ENG-013`. Post-pass gate check: exit 0, clean, both
scoped and whole-board. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-013-foodswipe-funnel-stage-control.md`).

## 2026-08-29 — continue ENG-008: built the preference/rating/collaboration-count edit path across both repos, ready → building

`continue` event pass, context `ENG-008`, its turn at the front of
`traces/.pending` finally reached. Narrow scope per the event's own
contract. Mode check clean. Pre-pass gate check: exit 0, clean, both scoped
and whole-board.

Both `_eng` worktrees existed, clean, sitting on `ENG-013`'s own
still-in-flight branch — not touched. Fetched both; `origin/main` unchanged
since `ENG-013` last branched. Branched both fresh as
`feat/ENG-008-influencer-admin-management`, migration timestamp
`20260829220000` chosen deliberately clear of `ENG-013`'s unmerged
`20260829200000`.

Built per the design: `staff_rating`/`collaboration_count` plus
`accepts_paid`/`accepts_barter` (backfilled from `barter_visit`, which is
left untouched) on `influencers`; new `GET`/`PATCH
admin-portal/influencers/{id}` (admin/sub-admin gate, same narrower pattern
`ENG-007` and `ENG-013` both use); edit form added to `aiorders-admin-hub`'s
previously entirely-read-only influencer detail dialog. Self-tested: `deno
check` clean on the new handler in isolation, `npm run lint` zero new
issues (150 pre-existing, same count `ENG-013` recorded), `npm run build`
clean.

**Step 6b's artifact-enumeration grep caught a real bug before it shipped**:
`ENG-009`'s design doc (sibling ticket, same handler, sequenced to build
after this one) had already recorded `admin-portal/index.ts`'s CORS
`Access-Control-Allow-Methods` as missing `PATCH` — exactly the method this
ticket's design specifies. None of the three local self-tests would have
caught it (a CORS failure only shows up against a real browser preflight).
Fixed in this same hop by widening the allow-list in both files that carry
it. Full detail, plus the separate (deliberately not acted on)
`collaboration_count` naming-overlap flag from the same doc, on the
ticket's own log.

Both branches committed and pushed (`aiorders-api@e240767`,
`aiorders-admin-hub@f2ea36c`); no PR opened yet — devops's step. PR bodies
drafted on the ticket's own log. Database migration doc written
(`agents/database/migrations/ENG-008-influencer-profile-admin-management.md`).

**1 transition** (`ready → building`), well under the cap — the next hop
(review + quality, combined) is a fresh session's work by design. No cap
change; `ENG-008` stays inside the counted `ready..ready-to-ship` range.

`chained: ENG-008` — `building` is agent-owned (code review + quality
next). Fired `continue ENG-008`. Post-pass gate check: exit 0, clean, both
scoped and whole-board. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-008-influencer-profile-admin-management.md`).

## 2026-08-29 — decision ENG-014: G1 already processed by an earlier `watch` pass, but its own recorded chain never fired — repaired

`decision` event pass, context `2026-08-29-eng014-g1-scope.md` — this
event's own queued fire, drained behind a `watch`/`schtasks` fire that
reached the same gate item first. Mode check clean. Pre-pass gate check:
exit 0, clean, scoped (`ENG-014`) and whole-board.

Verified fresh rather than assumed stale: the gate item is genuinely
already in `inbox/_handled/` with a "Processed" footer, `ENG-014` is
genuinely at `designed`/`architect`, and `decision-journal.md` genuinely
carries the G1 row — the earlier `watch` pass's substantive work all
checks out. What doesn't check out is its own `chained: ENG-014` line:
`traces/eng-loop-2026-08-29.log` shows no `continue (ENG-014)` ever ran,
and it wasn't sitting in `traces/.pending` either. That `watch` pass's
process (pid 36150) died before exiting cleanly (`clearing stale lock
(2103s old, owner 36150 gone)`) — almost certainly right around writing
that log line, before the shell fire behind it ever executed. `ENG-015`
carries the identical shape from the same dying pass; out of scope for
this event (named ticket is `ENG-014` only), flagged in `observations.md`
instead.

**Action:** re-fired `/bin/sh
departments/engineering/lib/eng-trigger.sh continue ENG-014` directly.
Confirmed on `traces/.pending` afterward and via the trigger's own stderr
(queued correctly behind this still-running pass rather than lost again).
No ticket state changed — the architect's actual design work stays a
dedicated session's job, which the now-genuine chain will launch.

**0 transitions**, no cap impact — this was a chain repair, not new
gate or state movement.

`chained: ENG-014` — re-fired and confirmed queued this pass (see above).
Post-pass gate check: exit 0, clean, both scoped and whole-board. Full
detail on the ticket's own log
(`agents/eng-manager/board/ENG-014-restaurant-qr-media-self-service.md`).

## 2026-08-29 — continue ENG-007: verified fresh, held at `ready-to-ship` — release window closed for the weekend

`continue` event pass, context `ENG-007`, the chain fire from the pass that
reached `ready-to-ship`. Narrow scope per the event's own contract. Mode
check clean. Pre-pass gate check: exit 0, clean, both scoped and
whole-board.

Verified fresh rather than trusted, given this ticket's two prior
unrecorded-build recoveries: the `aiorders-api` worktree confirms
`loyalty-system` unchanged at `2aec86f`, tree clean, not merged into
`origin/main`, and no PR open against it (`gh pr list` shows only `ENG-006`'s
own already-merged PR #2) — genuinely still `ready-to-ship`, not a third
unrecorded advance.

Release window re-checked fresh, as the prior entry explicitly asked the
next hop to do: Saturday 2026-08-29, 14:09 local, inside
`releases.block_weekends`. `ENG-006` hit this identical boundary on a Friday
before the 15:00 cutoff and proceeded to open its PR; this lands outside the
window. Consistent with that precedent — this department treats the PR-open
step itself, not just the eventual merge, as the release-window-gated
action — and with this pass's own prompt, which names "a closed release
window" as a chaining exclusion alongside the approver: no PR opened, no
state change.

**0 transitions.** No cap affected either way — what's holding this ticket
is the release window, not WIP or approval capacity.

`chained: none` — release window closed (weekend). Expected to clear on its
own: the next scheduled safety-net pass, or a fresh `continue ENG-007` fire,
landing once the window reopens Monday will find this same state and
proceed to open the PR — this is the guard's first real activation on this
instance (`observations.md`), not previously seen blocking anything. Post-pass
gate check: exit 0, clean, both scoped and whole-board. Full detail on the
ticket's own log
(`agents/eng-manager/board/ENG-007-per-restaurant-loyalty-configuration.md`).

## 2026-08-29 — decision ENG-013 (presignup-leads question): a third predicted twin no-op — arrived after the fact was already consumed by a scheduled sweep, not by the pass that raised it

`decision` event pass, context
`inbox/_handled/2026-08-29-eng013-presignup-leads-question.md` — same
twin-no-op shape as `ENG-013`'s own G1 logged directly above, and
`ENG-011`'s tickets-question twin before that. Per this event's own
narrower contract (act on the answered gate item, advance only the ticket
it belongs to), scoped to `ENG-013` only — no board-wide sweep. Mode check
clean (business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
`mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean.

**Confirmed rather than assumed, and a different shape from the two twins
above.** `traces/eng-loop-2026-08-29.log`: `13:15:10 queue: collapsed 1
duplicate event(s)` fires immediately before `13:15:10 draining queued
event: decision (2026-08-29-eng013-presignup-leads-question.md)`, pass
start `13:15:11`, claude launched `13:16:05`. Unlike the G1 twin directly
above (caught live by the same pass that raised it), this question sat
answered-but-unprocessed until a separate `scheduled` event pass (context
`schtasks`, since rolled to `_index-archive.md`) swept it: read the answer
fresh from `inbox/` (`decision: approved`, "Reading B" — a genuine
pre-signup pipeline with autopilot nurture, `decided:
2026-08-29T11:46:34.557123+00:00`), checked for an existing ticket before
filing a new one per the item's own stated next step, and found one — an
independent `intake` pass the same day had already reached the same
conclusion from a different raw request (the "no autopilot for sales
staff/resellers" card) and filed `ENG-017` (presignup lead nurture
autopilot, `agents/eng-manager/board/ENG-017-presignup-lead-nurture-autopilot.md`,
`state: shaped`), already citing this exact verbatim answer as grounding
evidence in its own Notes. Checked fresh rather than trusted: the gate
item's own processed footer, `decision-journal.md` row 31, `ENG-013`'s own
Notes section (added by that scheduled pass), and `ENG-017`'s own Notes
section all agree — the question is closed against `ENG-017`, not
re-opened, and not filed twice. `ENG-013` itself was never blocked by this
question and needed no action from it either way, then or now.

**0 transitions.** No cap affected — `ENG-013` was already inside the
counted `ready`..`ready-to-ship` machine-WIP range before this pass, and
this standing question's approval-cap slot was already freed by the
scheduled pass that closed it — the board header's current cap accounting
(`ENG-014`/`ENG-015`'s G1s only) no longer carries it.

**Dead-end sweep (scoped to this event):** confirmed `continue ENG-013` —
fired when this ticket reached `ready` — still sitting in
`traces/.pending`, undrained, behind a longer backlog than either twin
above last saw. Not stuck — no documented sequencing hold against a
sibling ticket, purely FIFO position.

**Notify sweep:** nothing to raise (no new gate item this pass); nothing to
nudge (this question's `notified:`/`decision:` cycle closed same-day, hours
before this pass, well inside the 24h threshold).

Another corroborating occurrence of the open `proposals.md` race
(2026-08-27 row — `eng-trigger.sh` should skip the launch when a
`decision` event's named gate item is already in `_handled/`); not
re-filed or re-logged as its own observation — the existing proposal
already covers this exactly.

`chained: none` — no state change; `ENG-013`'s existing chain (`continue
ENG-013`) is already queued and will run on its own turn; firing a second
`continue ENG-013` now would only queue a duplicate for the collapse logic
to clean up later. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean. Full detail on the
ticket's own log
(`agents/eng-manager/board/ENG-013-foodswipe-funnel-stage-control.md`).

## 2026-08-29 — decision ENG-013 (G1 scope): another predicted twin no-op — arrived after the fact was already consumed

`decision` event pass, context `inbox/_handled/2026-08-29-eng013-g1-scope.md`
— same shape as `ENG-011`'s own G1 twin logged above (and, before that,
`ENG-008`'s two gate items, `ENG-009`'s G1, `ENG-010`'s G1). Per this
event's own narrower contract (act on the answered gate item, advance only
the ticket it belongs to), scoped to `ENG-013` only — no board-wide sweep.
Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean.

**Confirmed rather than assumed.** `traces/eng-loop-2026-08-29.log`:
`13:01:35 draining queued event: decision (2026-08-29-eng013-g1-scope.md)`
— no `queue: collapsed` line immediately above it this time, so this is a
single fire reaching its own turn late (raised/`notified:` 11:39:39), not a
duplicate-collapse; a long backlog (`ENG-014`..`ENG-024` work) simply sat
ahead of it in the FIFO. By the time it drained, the same `intake` pass
that raised this G1 had already caught the approver's hand-edit
(`decision: approved`, `decided: 2026-08-29T11:45:00.908943+00:00`, bare
approval, ~6 minutes after `notified:`) while still running: the ticket
carried `awaiting-scope → designed → ready`, journaled
(`agents/eng-manager/config/decision-journal.md`, row 28), and the gate
item moved to `inbox/_handled/` with its own processed footer. Checked
fresh rather than trusted: this ticket's own frontmatter (`state: ready`,
`owner: eng-manager`), the journal row, and the footer all agree. Nothing
left for this event to act on.

**0 transitions.** No cap affected — `ENG-013` was already inside the
counted `ready`..`ready-to-ship` machine-WIP range before this pass, and
this G1 was already off both the approver-facing WIP and approval-cap
counts.

**Dead-end sweep (scoped to this event):** confirmed `continue ENG-013` —
fired by the pass that closed this ticket's G1 — still sitting in
`traces/.pending`, undrained, third in line behind two older not-yet-drained
fires (`ENG-013`'s own presignup-leads question, `ENG-012`'s G1). Not a
broken chain, just not yet its turn in the FIFO queue.

**Notify sweep:** nothing to raise (no new gate item this pass); nothing to
nudge (this G1's `notified:`/`decision:` cycle closed same-day, hours
before this pass, well inside the 24h threshold).

Another corroborating occurrence of the open `proposals.md` race (2026-08-27
row, filed by hand — `eng-trigger.sh` should skip the launch when a
`decision` event's named gate item is already in `_handled/`); well past a
dozen occurrences instance-wide as of today, so not re-filed or re-logged as
its own observation — the existing proposal already covers this exactly and
stands unimplemented, waiting on the approver.

`chained: none` — no state change; `ENG-013`'s existing chain (`continue
ENG-013`) is already queued and will run on its own turn. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-013-foodswipe-funnel-stage-control.md`).

## 2026-08-29 — continue ENG-011: recovered an unrecorded build already through security, live-DB read verification closed part of the migration gap, ready → ready-to-ship

`continue` event pass, context `ENG-011`, its actual turn at the front of
`traces/.pending`. Narrow scope per the event's own contract. Mode check
clean; pre-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board: exit 0, clean.

Same recovery shape `ENG-007` hit earlier the same day, one occurrence
further: both `_eng` worktrees already carried a pushed
`feat/ENG-011-client-stage-health-visibility` branch, and all four gate
receipts (database migration, code review, QA test plan, security review)
already existed on disk with `pass` verdicts. Verified fresh rather than
trusted — git state, `deno test` (12/12), `npm run build` (clean) all
independently reproduced and matched. New this time: the Supabase MCP
connection reaches the real `aiorders-api` project read-only, used at zero
cost to independently confirm the migration's schema assumptions and rule
out catalog-level dependents — closing the "is it safe" half of the
long-standing no-live-Postgres gap without spending the approver's money
or writing DDL to production ahead of review (both declined as out of this
pass's own authority). Third occurrence of that host limitation crossed
the threshold `observations.md` set for a proposal; filed one
(`proposals.md`), not another observation.

State recorded to match reality: `ready → building → in-review →
in-security → ready-to-ship`, 4 transitions (cap). `machine_wip` and both
approver-facing counters unaffected — no gate raised this pass, the L1
merge request (both repos, this board's first two-repo release) is the
next hop's work. Release window independently reconfirmed closed (Saturday
2026-08-29, `releases.block_weekends`) — flagged for the next hop, not
acted on, same split `ENG-006`/`ENG-007` used at this boundary.

`chained: ENG-011` — `ready-to-ship` is agent-owned (devops opens the PR
next). Fired `continue ENG-011`. Post-pass gate check: see pass notes. Full
detail on the ticket's own log
(`agents/eng-manager/board/ENG-011-client-stage-health-visibility.md`).

## 2026-08-29 — decision ENG-011 (tickets-source question): a second predicted twin no-op, arrived after the fact was carried all the way to a closed thread

`decision` event pass, context
`inbox/_handled/2026-08-29-eng011-tickets-source-question.md` — the same
duplicate-queued-event shape as the entry directly above, but a different
gate item: `ENG-011`'s standing "tickets" question was queued as its own
independent `decision` event, separate from its G1. Sixth occurrence of
this shape today (`ENG-008`'s two gate items, `ENG-009`'s G1, `ENG-010`'s
G1, `ENG-011`'s own G1, now this). Per this event's own narrower contract
(act on the answered gate item, advance only the ticket it belongs to),
scoped to `ENG-011` only — no board-wide sweep. Mode check clean
(business-os `.env` → `MODE=` empty).  Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-011`) and
whole-board: both exit 0, clean.

**Confirmed rather than assumed.** `traces/eng-loop-2026-08-29.log`:
`11:13:54 queue: collapsed 3 duplicate event(s)` fires immediately before
`11:13:54 draining queued event: decision
(2026-08-29-eng011-tickets-source-question.md)`, pass start `11:13:55`,
claude launched `11:14:48`. By the time this pass reached the file, the
same `intake` pass that raised the question had already caught the
approver's hand-edit (`decision: rejected`, free text "Reading A",
`decided: 2026-08-29T11:16:32.000840+00:00`) while still running, read it
as a selection of Reading A rather than a flat rejection, shaped it
directly into `ENG-012` in that same pass, and journaled the read
(`decision-journal.md` row 27). Checked further than the last twin
required: `ENG-012`'s own board file shows the thread didn't stop at
"shaped" — a later `scheduled` pass found its G1 answered `rejected`
("later") and carried it to terminal `state: dropped`. Frontmatter,
footer, journal row, and `ENG-012`'s own log all agree — this thread is
not just consumed, it's closed end to end.

**0 transitions.** No cap affected — `ENG-011` was already inside the
counted `ready`..`ready-to-ship` machine-WIP range before this pass, and
this standing question was already off both approver-facing WIP and the
approval cap (closed the same pass it was raised).

**Dead-end sweep (scoped to this event):** re-confirmed `continue
ENG-011` still sitting in `traces/.pending`, undrained, now behind a
considerably longer backlog than the entry above last saw (fires for
`ENG-013` through `ENG-024` have since queued). Still not stuck — no
documented sequencing hold against a sibling ticket, purely FIFO
position.

**Notify sweep:** nothing to raise or nudge.

`chained: none` — no state change; `ENG-011`'s existing chain (`continue
ENG-011`) is already queued and will run when it reaches the front.
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-011`) and whole-board: both exit 0, clean. Full detail on the
ticket's own log
(`agents/eng-manager/board/ENG-011-client-stage-health-visibility.md`).

## 2026-08-29 — decision ENG-011 (G1 scope): the predicted twin no-op — arrived after the fact was already consumed

`decision` event pass, context `inbox/_handled/2026-08-29-eng011-g1-scope.md`
— the same duplicate-queued-event shape already logged for `ENG-008`'s two
gate items, `ENG-009`'s G1, and `ENG-010`'s G1 earlier today. Per this
event's own narrower contract (act on the answered gate item, advance only
the ticket it belongs to), scoped to `ENG-011` only — no board-wide sweep.
Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-011`) and
whole-board: both exit 0, clean.

**Confirmed rather than assumed.** `traces/eng-loop-2026-08-29.log`:
`10:59:40 queue: collapsed 2 duplicate event(s)` fires immediately before
`10:59:40 draining queued event: decision (2026-08-29-eng011-g1-scope.md)`
— duplicate copies of this event collapsed to the oldest, which is this
pass. This item's fact — the approver's G1 approval — was fully consumed by
the `intake` pass that raised it, which caught the hand-edit (`decided:
2026-08-29T11:14:54.862156+00:00`) while still running: architect design
work done (`stage`/`health` both derived at read time from existing
columns/pipelines, no new stored fields — closing the drift-risk the
readback itself flagged), the ticket carried `awaiting-scope → designed →
ready`, journaled (`agents/eng-manager/config/decision-journal.md`, row
26), and the gate item moved to `inbox/_handled/` with its own processed
footer. Checked fresh: the ticket's own frontmatter (`state: ready`,
`owner: eng-manager`), the journal row, and the footer all agree. Nothing
left for this event to act on.

**0 transitions.** No cap affected — `ENG-011` was already inside the
counted `ready`..`ready-to-ship` machine-WIP range (6/6, at cap) before
this pass, and this G1 was already off both the approver-facing WIP and
approval cap counts.

**Dead-end sweep (scoped to this event):** confirmed `continue ENG-011` —
fired by the pass that closed this ticket's G1 — still queued and
undrained in `traces/.pending`, behind several older not-yet-drained
fires. Unlike `ENG-009`/`ENG-010`, `ENG-011` carries no documented
sequencing hold against a sibling ticket, so nothing here is deliberately
parked — it's simply not yet its turn in the FIFO queue.

**Notify sweep:** nothing to raise or nudge.

`chained: none` — no state change; `ENG-011`'s existing chain
(`continue ENG-011`) is already queued and will run when it reaches the
front. Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-011`) and whole-board: both exit 0, clean. Full detail on the
ticket's own log
(`agents/eng-manager/board/ENG-011-client-stage-health-visibility.md`).

## 2026-08-29 — intake: FoodSwipe location-search bug traced to onboarding's missing `show_in_marketplace`, shaped to ENG-024, fast lane, G1 auto-skipped

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-fix-the-location-bug-on-foodswipe.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own narrower
contract, worked only this one request end to end — did not sweep the rest of
the board. Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` not re-checked separately this pass, no signal it
changed). No pre-pass `lib/eng-gate-check.sh` run through the trigger this
session either (started directly, same known gap prior entries have already
named) — ran it post-pass instead, scoped and whole-board (below).

**No worktree existed on this host for any of the five registered projects**
(`~/Documents/projects/_eng/` itself was absent, not just missing entries) —
none created; `git worktree add` felt like more than an `intake` pass should
reach for on its own initiative when the investigation could be done
read-only. Investigated by reading the human's own checkout directly
(`~/Documents/projects/aiorders/*`), strictly read-only — no git command run
there, no file written there. Whoever next needs to actually build against
`aiorders-api` for this ticket still needs a real worktree
(`config/projects.md`'s by-hand `git worktree add -b eng/base` command, or a
full `lib/eng-setup.sh --apply`); not created here.

**Traced the report to a full, confirmed root cause across two repos before
sizing anything** — skipped `skills/request-readback/SKILL.md`'s dual-reading
ceremony by design (fast lane, see below), and used the saved budget to chase
the actual code instead: `aiorders-api/supabase/functions/restaurant-portal-onboarding/restaurants.ts`'s
`createRestaurant` inserts a new restaurant with `approved: true` but never
sets `show_in_marketplace`; the same file's `updateRestaurantDetails`, called
immediately after in the same onboarding action
(`restaurant-portal/src/components/onboarding/steps/AddLocationsStep.tsx` →
`addLocationFromPlace`), writes Google Places data through
`mapPlaceToRestaurantRow` (`_shared/googlePlaces.ts`) — confirmed its own
`RESTAURANT_PLACE_COLUMNS` whitelist also excludes `show_in_marketplace`, so
nothing anywhere in the sign-up path ever sets it. Every marketplace search
path hard-requires it: `restaurant-marketplace/handlers/restaurants.ts`'s
primary `get_restaurants_optimized` RPC and its own fallback query both filter
`.eq('approved', true).eq('show_in_marketplace', true)`, matching the RPC's
own definition
(`restaurant-marketplace/supabase/migrations/20240302_optimize_restaurant_discovery.sql`);
`sitemap.ts` carries the same requirement. The only place in the codebase that
ever sets the flag `true` is a manual checkbox on an internal admin page
(`aiorders-admin-hub/src/pages/RestaurantDetails.tsx`). `geo` itself **is**
set correctly by `updateRestaurantDetails` — this is specifically a
visibility-flag gap, not a geocoding one, confirmed rather than assumed from
the report's "search by location" wording.

**Sized XS, lane `fast`** — single-file code fix (one field on one existing
insert) plus a one-time backfill `UPDATE` for rows already stuck invisible;
no schema change (column exists already), no new interface, touches none of
the fast-lane exclusion list (auth, payments, data deletion, schema,
dependencies, model calls, public contracts, PII). `type: bug` — G1
auto-skipped per `definition-of-done.md`'s state table, so no gate item
raised and neither approver-facing WIP nor the approval cap is touched by
this ticket at all.

**Filed `ENG-024`** (project `aiorders-api`; severity `P1` — the sign-up
flow's entire point silently fails with no error and no signal to anyone,
though a manual admin workaround exists so it falls short of P0). PRD:
`agents/product-manager/specs/ENG-024-onboarded-restaurants-missing-from-marketplace-search.md`.
Named two things explicitly out of scope rather than silently narrowing: a
second insert site with the identical omission
(`aiorders-api/supabase/functions/restaurant-claims/index.ts`, the separate
"claim your restaurant" flow) sets `approved: false` by design, so whether
*its* eventual approval step also needs to set the flag is a different,
unverified question, not pulled into this ticket; and the column's actual
DB-level default isn't defined in any tracked migration in any of the five
repos, left for whoever builds this to confirm on the way past.

**Held at `shaped` only long enough to write this entry, not blocked by any
cap** — machine WIP counts `ready`..`ready-to-ship` only, and G1 being
auto-skipped means this ticket never touched approver-facing WIP or the
approval cap either. Owner handed to `eng-manager` immediately: per
`agents/product-manager/agent.md`, sequencing/WIP/assignment is the EM's job
even for an auto-approved bug, never the PM's, so this pass deliberately
stopped short of pushing the ticket into `ready`/`building` itself — the
latter is new implementation work, which is this `intake` event's own named
stopping condition regardless of lane. **1 transition**
(`intake → shaped`), well under the cap of 4.

**Rolled the board index this pass** — one more dated entry than the
keep-three rule allows before this one landed; moved the oldest
(`ENG-021`'s chat-bar entry) to the top of `_index-archive.md`'s list,
verified by direct before/after line comparison rather than assumed clean.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract beyond the fresh work above. `ENG-007` through `ENG-023` otherwise
untouched.

**Observations filed** (`observations.md`): the `restaurant-claims` sibling
gap named above, as a suspicion worth a follow-up look rather than a
confirmed second bug — not escalated to a proposal since it's unverified
whether the claims-approval step already closes it downstream.

`chained: ENG-024` — fired `lib/eng-trigger.sh continue ENG-024` before this
pass exits: `shaped`, owner `eng-manager`, an agent-owned state with no gate
to wait at (G1 auto-skipped), nothing about this ticket waiting on a human.
Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-024-onboarded-restaurants-missing-from-marketplace-search.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-024`)
and whole-board: both exit 0, clean.

## 2026-08-29 — decision ENG-009 (G1 scope): the predicted twin no-op — arrived after the fact was already consumed

`decision` event pass, context `inbox/_handled/2026-08-29-eng009-g1-scope.md`
— the same duplicate-queued-event shape already logged twice on this board
for `ENG-008`'s own two gate items (now both archived). Per this event's own
narrower contract (act on the answered gate item, advance only the ticket it
belongs to), scoped to `ENG-009` only — no board-wide sweep. Mode check
clean (business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
`mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-009`) and whole-board: both exit 0, clean.

**Confirmed rather than assumed.** `traces/eng-loop-2026-08-29.log`:
`10:18:40 queue: collapsed 3 duplicate event(s)` fires immediately before
`10:18:40 draining queued event: decision (2026-08-29-eng009-g1-scope.md)`
— three legitimately-queued copies of this event collapsed to the oldest,
which is this pass. This item's fact — the approver's G1 approval, plus an
unprompted staff-notes addendum already shaped into `ENG-010` — was fully
consumed by the `scheduled` pass (context `schtasks`) that found it sitting
answered-but-unprocessed: shaped, journaled (`decision-journal.md` row 25),
moved to `inbox/_handled/` with its own processed footer, and `ENG-009`
itself carried `awaiting-scope → designed → ready` in that same pass.
Checked fresh: this item's frontmatter (`decision: approved`, `decided:
2026-08-29T09:20:42.679606+00:00`), the journal row, and `ENG-009`'s own
`state: ready` all agree — nothing left for this event to act on.

**0 transitions.** No cap affected — `ENG-009` was already inside the
counted `ready`..`ready-to-ship` machine-WIP range (6/6, at cap) before this
pass, and this G1 was already off both the approver-facing WIP and approval
cap counts.

**Dead-end sweep (scoped to this event):** confirmed `continue ENG-008`
still queued and undrained in `traces/.pending`, behind several other
not-yet-drained fires — consistent with `ENG-008` still sitting at `ready`
with no branch or build started. `ENG-009`'s existing sequencing hold
(re-check once `ENG-008` reaches `in-review` or later) therefore still
applies unchanged. Nothing to resume.

**Notify sweep:** nothing to raise or nudge.

`chained: none` — no state change; `ENG-009` remains held at `ready` pending
`ENG-008`. Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-009`) and whole-board: both exit 0, clean. Full detail on the ticket's
own log
(`agents/eng-manager/board/ENG-009-influencer-engagement-info.md`).

## 2026-08-29 — intake: feedback-board status/notes shaped to ENG-023, held at `shaped` — and a P0 tenant-isolation bug found along the way, filed as ENG-022

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-the-feedback-board-on-the-brand-portal-does-not-have-status-.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own narrower
contract, worked only this one request end to end — did not sweep the rest
of `agents/product-manager/inbox/` (`fix-the-location-bug-on-foodswipe`
untouched). Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Caps checked fresh from `inbox/` directly**: `ENG-014`'s and `ENG-015`'s
G1s both still sit in `inbox/`, both `decision: approved`, neither
frontmatter advanced — same answered-but-unprocessed state as every pass
today since `ENG-021`'s. Treated conservatively as still 2/2 approver-facing
WIP, 2/3 approval cap.

**Traced the request to its backend before proposing anything**: brand
portal's Feedback page → `brandPortalApi.getFeedback` →
`aiorders-api`'s `brand-portal/feedback.ts` → `restaurant_feedback` schema
(no `status`/`notes` columns at all, confirmed). That trace surfaced a
second thing: `feedback.ts`'s own access check,
`verifyRestaurantAccess(supabase, user.id, restaurant_id)`, has its
arguments in the wrong order against the real signature
(`restaurantId, supabase, user, options`) *and* checks the returned
`{hasAccess, error}` object's truthiness instead of its `.hasAccess` field
— so the check can never deny access, for anyone, to any restaurant's
feedback. Grepped every `verifyRestaurantAccess` call site in
`brand-portal/` (9 files) rather than assuming this was isolated: found the
identical wrong-order-plus-truthiness bug in all 8 call sites of
`offers.ts`, and a second, different mistake — the check called but its
return value discarded entirely, so it does nothing regardless of argument
order — in `customers.ts` (5 sites), `hiring.ts` (3), `website.ts` (2).
Confirmed correct, for contrast: `catering.ts`, `restaurants.ts`, `menus.ts`
(7 sites), `onlineOrders.ts`. Net: any authenticated brand-portal user can
read or write any other restaurant's customer feedback, customer list,
offers, or website content by supplying a different `restaurant_id` — no
exploit tooling needed. `aiorders-api` is documented in `config/projects.md`
as "Highest blast radius of the set — shared backend for all four
frontends."

**Filed as its own ticket, not folded into the feedback ticket and not
routed through `agents/eng-manager/proposals.md`.** Per
`agents/product-manager/agent.md`'s `never_touches` list, a security finding
isn't the PM's to fix or fold into a feature PRD — but per
`schedules/eng_build_loop.md` step 3's explicit bypass and
`templates/ticket.md`'s `source:` note, **a P0 on a registered non-internal
project "keeps its agent source"** and is filed directly rather than queued
for a weekly batched G1: "a live security hole must not wait for a weekly
batch." Rated **P0** rather than P1 on the merits (weighed directly against
this board's other confirmed cross-tenant finding, `ENG-015`, itself P1):
`agents/eng-manager/config/security-baseline.md` names "exposed data" as an
active-security-incident example on par with a leaked credential, and
`agents/security/agent.md`'s own `interrupt_rule` is "P0 only — active
incident, leaked credential, or exposed data." This exposes live customer
PII (not just listings, as `ENG-015` did) and grants unauthorized
cross-tenant *writes* (offers, website content), across five files rather
than one.

**Filed `ENG-022`** (`type: security`, `severity: P0`, `project:
aiorders-api`). PRD (short-form — auto-skip type, no readback needed for an
agent-originated finding with its own evidence):
`agents/product-manager/specs/ENG-022-brand-portal-tenant-isolation-broken.md`.
Landed at `state: shaped, owner: architect` rather than attempting
`designed` myself — that state's exit condition (tech design, ADRs) is the
architect's own output. **Per `security-baseline.md`, "only two things reach
the approver directly... an active security incident — P0,"** so this also
raised an incident notice rather than only a ticket:
`inbox/2026-08-29-eng022-p0-incident.md` (`gate: incident`). Ran
`departments/engineering/lib/eng-notify.sh raise` on it — **exit 0, but
confirmed via `traces/eng-notify-2026-08-29.log` that this is the
already-known, already-proposed no-op** (`proposals.md`, 2026-08-25 row:
`SLACK_WEBHOOK_URL` unset, and this instance's own `config/config.yaml`
sets `approver.notify: telegram`, which the script has no branch for
regardless). The item is on disk in `inbox/` and will surface via the
control center and the next daily brief/weekly report even though the push
did not fire — noted here rather than silently trusted, same practice this
board used the first time this exact gap was caught (2026-08-25). Did not
attempt a fix — that script's channel-dispatch logic is already a queued
proposal and touching its core dispatch path outside that review felt like
larger scope than this pass should take unilaterally.

**Then completed the assigned intake work.** Ran the full request-readback
(`skills/request-readback/SKILL.md`): this PM's own reading plus a blind
architect reading (subagent, `opus`, raw request +
`knowledge/business-profile.md` only, no repo access, no exposure to this
PM's own reading, no exposure to the `ENG-022` investigation either — kept
genuinely blind). **Strong convergence on the core** — both independently
landed on "each feedback item needs a status and an internal note,"
unprompted. **One material divergence**: the architect's reading treated
"is this frequent" / "bottomline issues" as asking for a built cross-item
aggregation/analytics layer (counts, recurring-issue detection, possibly
AI-assisted categorization); this PM's own reading leaned toward "a
restaurant can judge that for itself once notes exist," a materially
smaller build. Per the skill's divergence table this is genuine — different
scope, not different wording — so not resolved internally.

**Did not hold the ticket for it**, same shape as `ENG-013`'s
presignup-leads question → `ENG-017`: the confirmed core (status + notes)
ships regardless, and the divergence became its own non-blocking question,
`inbox/2026-08-29-eng023-frequency-question.md` (`gate: intake-question`) —
"yes" becomes its own ticket once scoped; "no" just closes it. Ran
`lib/eng-notify.sh raise` on it too (same known no-op logged above).

**Filed `ENG-023`** (`type: feature`, `size: S`, `project:
restaurant-portal`). PRD:
`agents/product-manager/specs/ENG-023-feedback-status-and-notes.md`.
**Cross-referenced both new tickets explicitly**: `ENG-023`'s new write path
touches the same file as `ENG-022`'s fix
(`brand-portal/feedback.ts`) — flagged on both that the new
`update_feedback` handler must be modeled on `catering.ts`'s confirmed-
correct `update_catering_request`, not on this file's own (until `ENG-022`
lands) broken `getFeedback`. Not a formal `depends_on` — sequencing between
them is the EM's call at `ready`.

**Held `ENG-023` at `shaped`, not advanced to `awaiting-scope`** —
approver-facing WIP 2/2 per the fresh check above. G1 content fully drafted
in the PRD's Decision section, ready to raise the moment a slot clears.
**Consequence for both tickets:** no cap numbers change — `shaped` counts
toward neither approver-facing WIP nor machine WIP (still 6/6). **2
transitions total** (`ENG-022` and `ENG-023` each `intake → shaped`), well
under the per-ticket cap of 4.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract beyond the fresh cap-verification above. `ENG-007` through
`ENG-021` otherwise untouched.

**Observations filed** (`observations.md`): none beyond what both new
tickets already carry directly — the `ENG-014`/`ENG-015`
answered-but-unprocessed backlog is now six consecutive passes old without
a `decision` event picking it up, re-flagged again; added one line noting
`eng-notify.sh`'s channel-dispatch gap (`proposals.md`, 2026-08-25) was
confirmed a second time this pass, this time on a P0's own incident notice,
strengthening rather than duplicating that existing proposal.

`chained: ENG-022` — `shaped`, owned by `architect`, an agent-owned state;
fired `lib/eng-trigger.sh continue ENG-022` before this pass exits given the
severity, rather than waiting for a scheduled sweep. Confirmed via
`traces/.pending` and `traces/eng-loop-2026-08-29.log` that this queued
correctly rather than launching immediately — this session has held
`traces/.loop.lock` since this pass's own start (09:46:13; the log's last
entry, 10:11:36, already shows two `watch` fires and one `continue` fire
queuing behind it rather than stealing it, "PID 89985 is alive"), so
`continue ENG-022` joined 15 other fires already queued behind the same
lock. Not a stuck lock — it releases the moment this pass exits, and
whatever fires next drains the queue oldest-first; several of the queued
`decision` items look, from their own filenames, like they'll resolve as the
same already-consumed-before-the-fire-arrived no-ops this board has logged
twice already today. Left alone rather than manually drained — outside this
event's scope and not this pass's concurrency state to hand-edit. `chained:
none` for
`ENG-023` — `shaped`, held by the approver-facing WIP cap, not genuinely
blocked for this ticket specifically; re-check once a
`decision`/`watch`/`scheduled` pass clears `ENG-014` or `ENG-015`. Full
detail on each ticket's own log
(`agents/eng-manager/board/ENG-022-brand-portal-tenant-isolation-broken.md`,
`agents/eng-manager/board/ENG-023-feedback-status-and-notes.md`). Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-022`,
`ENG-023`) and whole-board: all three exit 0, clean.

## 2026-08-29 — intake: website chat-bar engagement gap shaped to ENG-021 — customer-questions view plus brand-portal FAQ editor, held at `shaped`

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-the-search-chat-bar-engagement-on-website-is-not-displayed-v.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own narrower
contract, worked only this one request end to end rather than sweeping the
board — two other unshaped `agents/product-manager/inbox/` requests
untouched (`fix-the-location-bug-on-foodswipe`,
`the-feedback-board-on-the-brand-portal-does-not-have-status-`), each with
its own `intake` event presumably already queued or pending. Mode check
clean (business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
`mode:` empty). No genuine pre-pass gate-check this time either — same gap
`ENG-019`'s own archived entry already named: this session started
directly rather than through `lib/eng-trigger.sh`'s own pre-pass injection.
Ran `departments/engineering/lib/eng-gate-check.sh` for real after
finishing this ticket's edits instead (below) — the only verdict this entry
can honestly report.

**Caps checked fresh from `inbox/` directly, not the cached header.** Found
`ENG-014`'s and `ENG-015`'s G1s both now `decision: approved` (decided
15:54:50 and 16:12:24) — a genuine change since the header was last
written, which claimed both "unanswered." Neither ticket's own frontmatter
has moved past `state: awaiting-scope, owner: approver` yet, so both
mechanically still hold their approver-facing WIP slot until a `decision`
pass processes them — treated conservatively as still 2/2, at cap, for
this pass's own G1 decision below. Processing those two decisions is out of
this event's scope (a `decision` event's job, apparently already in flight
independently for each); corrected the board header and the "Waiting on
the approver" section to say so plainly instead of repeating the
now-stale "both unanswered," and filed an observation
(`observations.md`) rather than acting on them directly.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading, grounded in live code across `config-site-builder`,
`aiorders-api`, `aiorders-admin-hub`, and `restaurant-portal` (all four
worktrees already present on this host at `$ENG_WORKTREES`, no creation
needed this pass), plus a blind architect reading (subagent, `opus`, raw
request + `knowledge/business-profile.md` only, no repo access, no exposure
to this PM's own reading). **No material divergence** — both independently
converged on the same core shape: capture real customer questions from the
chat bar, surface them to the owner, and let the owner act on them via
FAQs, as one closed loop on the brand portal. The architect's blind
reading, reasoning with no code access, correctly flagged as open questions
several things this PM's code-grounded reading confirmed directly instead:
whether queries are even captured today (yes, durably), whether the owner
already has backend read access to that data (yes, via an existing but
entirely unused RLS policy), and who authors the FAQ content today (staff
only, in the internal admin tool). None of these changed the shape of the
request, only its cost. The architect's PII and "answered vs. unanswered"
signal concerns were carried into the PRD's Risks/Non-goals rather than the
acceptance criteria, since neither is what the literal request asks for.

**Investigated all four repos before proposing anything.** Traced the
"search/chat bar" to `config-site-builder`'s `AISearchBar`/`ChatPanel`,
rendered site-wide via `Layout.tsx` behind a per-restaurant `showAIChat`
flag — live today, not hypothetical. Every turn is written by
`aiorders-api`'s `ai-search-openrouter` edge function to `ai_conversations`
(`session_id`, `restaurant_id`, `messages` jsonb, timestamps) — confirmed
this table already carries an RLS policy titled "Restaurant managers can
view their restaurant conversations" (`restaurant-portal` migration
`20250903152559_...sql`), granting the exact access this request needs,
entirely unused by any UI in either `restaurant-portal` or
`aiorders-admin-hub` (grepped both for `ai_conversations` usage beyond
generated types — zero hits). The bot's FAQ source is
`restaurant_website.faqs`, editable today only in `aiorders-admin-hub`'s
`RestaurantAIWebsite.tsx` via direct Supabase calls, no edge function in
the path. Confirmed `restaurant-portal` has a same-named but **unrelated**
FAQ list (`CateringFaq`, catering-page-specific) that does not touch this
data — flagged in the ticket so the next agent doesn't wire the new editor
to the wrong field. Confirmed `restaurant-portal` already reads/writes
`restaurant_website` directly today for a different section
(`src/pages/hiring/Index.tsx`, careers content) — the precedent pattern for
the new editor, and evidence (not proof — the literal RLS policy text on
`restaurant_website` was not read) that the owner's account can likely
already write to this table.

**Filed `ENG-021`** (project `restaurant-portal`; size `M` — two coordinated
frontend pieces in one repo, reusing existing tables/RLS on both sides, no
new backend endpoint anticipated; severity `P2`, same "real capability gap,
real manual workaround" calibration as `ENG-020` earlier today). PRD:
`agents/product-manager/specs/ENG-021-chat-bar-engagement-and-faq-self-service.md`.
Scoped as a real-questions log plus a working FAQ write path, not a
quality/gap-analysis dashboard: "answered vs. unanswered" scoring and
cross-session question clustering are named Non-goals/follow-on work, same
"ship the coherent core, name the harder measurement layer as follow-on"
shape `ENG-016`/`ENG-019`/`ENG-020` already used on this board. A
staff-facing (admin-hub) mirror of the same view is named a Non-goal too —
plausible future value, not what was asked.

**Held at `shaped`, not advanced to `awaiting-scope`.** Approver-facing WIP
reads 2/2 per the fresh-but-conservative check above. G1 content (readback,
both readings' comparison, non-goals, recommendation) is fully drafted in
the PRD's own Decision section and ready to raise the moment a slot
actually clears. **1 transition** (`intake → shaped`), well under the cap
of 4. **Consequence:** no cap numbers change — `shaped` counts toward
neither approver-facing WIP nor machine WIP (still 6/6).

No `inbox/` item raised this pass (no G1 to notify on yet), so no
`lib/eng-notify.sh` call.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract beyond the fresh cap-verification above. `ENG-007` through
`ENG-020` otherwise untouched.

**Observations filed** (`observations.md`): the `ENG-014`/`ENG-015`
answered-but-unprocessed finding above; a pre-existing dangling
`"scheduled sweep below"` cross-reference in this file's `ENG-012`
narrative, left unfixed as out of this event's scope.

`chained: none` — `ENG-021` sits at `shaped`, held by the approver-facing
WIP cap, not genuinely blocked or waiting on a human for this ticket
specifically; firing `continue ENG-021` now would only re-discover the same
cap with no new work to do. Re-check once a `decision`/`watch`/`scheduled`
pass actually clears `ENG-014` or `ENG-015`. Full detail on the ticket's
own log
(`agents/eng-manager/board/ENG-021-chat-bar-engagement-and-faq-self-service.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-021`) and whole-board: both exit 0, clean.

## 2026-08-29 — decision ENG-008 (G1 scope): the predicted twin no-op — arrived after the fact was already consumed

`decision` event pass, context `inbox/_handled/2026-08-29-eng008-g1-scope.md`
— this is the exact item the immediately preceding entry's own
`observations.md` note predicted would be the same no-op. Per this event's
own narrower contract (act on the answered gate item, advance only the
ticket it belongs to), scoped to `ENG-008` only — no board-wide sweep. Mode
check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, no
output — clean, including for `ENG-008` specifically (grepped the output
for it directly rather than trusting a clean exit code alone).

**Confirmed the prediction rather than trusting it.** This item's fact —
the approver's G1 approval of the admin-side scope — was already fully
consumed by the `intake` pass that raised it: shaped, journaled
(`decision-journal.md` row 23, "ENG-008 | G1 scope | approved"), moved to
`inbox/_handled/` with its own processed footer, and `ENG-008` itself
carried `awaiting-scope → designed → ready` in that same pass. Checked
fresh rather than assumed: this item's own frontmatter (`decision:
approved`, `decided: 2026-08-29T09:12:46.283064+00:00`) and processed
footer; the journal row; `ENG-008`'s own frontmatter (`state: ready`) and
log. All agree — nothing left for this event to act on. Same
duplicate-queued-event race as its sibling (the engagement-source
question, immediately above): both this G1 and that question were answered
and consumed inside the same live `intake` pass, and the two standalone
`decision` events each independently queued arrived afterward to find
their own facts already closed.

**0 transitions.** No cap affected — this item was already off every count
before this pass (per this file's own header, which already excludes it
from "Waiting on the approver" and the approval cap).

**Dead-end sweep (scoped to this event):** `ENG-008` already carries a
correct, reasoned chain decision from the preceding `scheduled` sweep
(re-fired `continue ENG-008`) — confirmed still queued and undrained in
`traces/.pending` as of this pass, so nothing to resume or fix.

**Notify sweep:** nothing to raise (no new gate item); nothing to nudge
(this item's `notified:`/`decision:` cycle closed same-day, hours before
this pass).

`chained: none` — no state change. `continue ENG-008` remains queued in
`traces/.pending` from the earlier `scheduled` sweep; firing it again would
only collapse into that existing copy at pop time, per the queue's own
dedup rule. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean.

## 2026-08-29 — decision ENG-008 (engagement-source question): arrived after the fact was already consumed — no-op

`decision` event pass, context
`inbox/_handled/2026-08-29-eng008-engagement-source-question.md`. Per this
event's own narrower contract (act on the answered gate item, advance only
the ticket it belongs to), scoped to `ENG-008`/`ENG-009` only — no
board-wide sweep. Mode check clean (business-os `.env` → `MODE=` empty;
instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
whole-board: both exit 0, clean.

**Nothing to act on.** This item's fact — the approver's "both readings"
answer — was already fully consumed by the `intake` pass that raised it,
reading the hand-edit live while still running: shaped into `ENG-009`,
journaled (`decision-journal.md`, "intake-question (engagement source)"
row), moved to `inbox/_handled/`, and `ENG-009` itself carried all the way
to `ready` by the `scheduled` sweep archived immediately above this entry.
Re-confirmed fresh rather than trusted: this item's own frontmatter/footer,
`ENG-009`'s ticket file, `ENG-008`'s own log, and the journal row all
agree.

**Fits the instance's well-documented duplicate-queued-event race
exactly** — confirmed directly from `traces/eng-loop-2026-08-29.log`
(`08:45:06 queue: collapsed 1 duplicate event(s)` immediately before
draining this one): two copies of the same event were legitimately queued
for the same underlying fact, and the live `intake` pass reached it first.
Contrast the `continue ENG-006` no-op (2026-08-28, archived), which did
*not* fit this pattern — that one came from a fire outside the chain
mechanism entirely; this one is the ordinary race.

**0 transitions.** No cap affected — this item was already off every count
before this pass.

**Observation filed** (`observations.md`): the next item in
`traces/.pending` (`decision 2026-08-29-eng008-g1-scope.md`) is the same
shape and will likely be the same no-op — that G1 was also already closed
in the same pass that advanced `ENG-008` to `ready`.

`chained: none` — no state change on either ticket; `continue ENG-008` is
already queued from the preceding `scheduled` sweep, and firing it again
here would only collapse into that existing copy at pop time. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
whole-board: both exit 0, clean.

## 2026-08-29 — intake: "AI SEO has no ROI tracking" shaped to ENG-020 — traffic-source/revenue attribution report, Clarity named out of scope

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-ai-seo-no-way-to-track-if-its-useful-or-working-on-brand-das.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own narrower
contract, worked only this one request end to end rather than sweeping the
board — three other unshaped `agents/product-manager/inbox/` requests
untouched, each with its own `intake` event already queued or pending. Mode
check clean (business-os `.env` → `MODE=` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (no ticket yet
to scope to): exit 0, clean.

**Caps checked fresh from `inbox/` directly, not the cached header, twice —
once before starting and again immediately before deciding whether to raise
G1.** Both checks agreed: `ENG-014`'s and `ENG-015`'s G1s both still read
`decision:` empty — approver-facing WIP substantively 2/2, at cap,
unchanged from the header going into this pass.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading, grounded in live code read across
`aiorders-admin-hub`, `config-site-builder` (created this host's missing
worktree to do so — the same per-host worktree gap this board has flagged
repeatedly this session, now also hit for this project), `aiorders-api`,
and `restaurant-portal`, plus a blind architect reading (subagent, `opus`,
raw request + `knowledge/business-profile.md` only, no repo access, no
exposure to this PM's own reading). **No material divergence** — both
independently converged on the same core shape: a per-restaurant view on
the brand portal joining traffic source to order/revenue outcomes, with
Microsoft Clarity named as the wrong tool for the actual question being
asked (behavioural analytics, not attribution or revenue). The architect's
blind reading additionally, unprompted, caught a real ambiguity in the raw
text itself — "but can demostrate" reads as missing a negation ("but
[cannot] demonstrate") — resolved without a standing question since both
readings independently landed on the same resolution, and raised several
risks folded into the PRD's Risks section: attribution honesty (a
last-touch number will overstate what SEO specifically did), cross-domain
cookie-stitching coverage, PIPEDA/Quebec Law 25 exposure from session
recording, no historical baseline for existing customers, small-restaurant
traffic noise, and tenant isolation.

**Investigated all four touched repos before proposing anything.** Traced
"AI SEO" to a real, specific, already-shipped feature — not a vague
marketing term: `aiorders-admin-hub`'s `RestaurantAIWebsite.tsx`/
`BrandAIWebsite.tsx` has a staff-only "SEO Settings" tab with a "Generate
with AI" button that writes `seo.title`/`description`/`keywords`/OG tags,
consumed by `config-site-builder`'s `buildSeo.ts` when building each
restaurant's public site. The restaurant owner never sees this feature or
its output's performance anywhere today. Confirmed Microsoft Clarity
appears nowhere in any of the five repos (case-insensitive search, zero
hits) — not a first-class integration; if installed at all, it's via the
generic custom-code head/body injection (`config-site-builder`'s
`useCustomCode.ts`) or entirely outside AIOrders. **The core finding that
shapes this ticket's low cost:** this is a reporting gap, not a capture
gap. Every customer-signup path this platform has — online order, email
signup, catering form, and a dedicated cross-subdomain tracking script
(`config-site-builder/public/tracking/user-tracking.js`) — already writes
`utm_source`/`utm_medium`/`utm_campaign`/`first_touch_source`/
`last_touch_source`/`first_referrer` onto the `customers` row
(`website-submissions/customer-signup.ts`, `email-signup.ts`,
`update-customer-tracking.ts`, `catering-request/index.ts`,
`crm/customers.ts`), and `autopilot/marketing/welcome.ts` already branches
its own logic on `first_touch_source` — real, wired, already-populated
columns that nothing reads back out to an owner. Confirmed the extension
point: `aiorders-api`'s `analytics` edge function
(`supabase/functions/analytics/database.ts`) already queries both `orders`
and `customers` for a restaurant, so the join this needs already exists at
that seam. Also confirmed `restaurant-portal`'s existing "Analytics" nav
item (`pages/analytics/Index.tsx`) is entirely mock data about
influencer-campaign performance — unrelated to website traffic, and
flagged in the PRD/ticket so it isn't confused with or reused for this
ticket.

**Filed `ENG-020`** (project `restaurant-portal` — primary; `aiorders-api`
also touched and named explicitly in the PRD, same multi-repo/singular-
`project:`-field precedent this board has used since `ENG-003`; size `M`
— no new data model, extends an already-wired edge function plus a new
report view; severity `P2`, calibrated against this board's now-standard
"real capability gap, real manual workaround" shape). PRD:
`agents/product-manager/specs/ENG-020-marketing-roi-attribution-reporting.md`.
Scoped deliberately smaller than the raw request's full framing: ships
revenue-by-channel, not a true ROI ratio (no billing-cost data exists to
weigh against), and organic-traffic revenue as the proxy for "is AI SEO
working" rather than a dedicated AI-SEO-specific attribution flag (nothing
records which restaurants have AI-generated vs. manual SEO applied today)
— both named as Non-goals/follow-on work rather than built now, same
"ship the coherent core, name the harder measurement layer as follow-on"
shape `ENG-016`/`ENG-019` already used on this board. Microsoft Clarity
integration itself is a Non-goal, with the reasoning stated plainly in the
PRD rather than quietly dropped.

**Held at `shaped`, not advanced to `awaiting-scope`.** Approver-facing WIP
is substantively 2/2 (`ENG-014`, `ENG-015`) — per `eng_build_loop.md`'s
Guards, same move this instance's four immediately preceding intake passes
all made. G1 content (readback, both readings' comparison, non-goals,
recommendation) is fully drafted in the PRD's own Decision section and
ready to raise the moment a slot frees. **1 transition**
(`intake → shaped`), well under the cap of 4. **Consequence:** no cap
numbers change — `shaped` counts toward neither approver-facing WIP nor
machine WIP (still 4/6).

No `inbox/` item raised this pass (no G1 to notify on yet), so no
`lib/eng-notify.sh` call.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract — not run beyond the fresh cap-verification above. `ENG-007`
through `ENG-019` otherwise untouched.

**Observations filed** (`observations.md`): the confirmed staff-only
scope of the "AI SEO" feature and the restaurant owner's total lack of
visibility into it; the confirmed-real attribution data already captured
and wired across five different entry points with nothing reading it back
out; the existing `analytics` edge function as the natural extension
point; the confirmed-mock-data state of the existing "Analytics" nav item,
worth a look in its own right since it presents as live to an owner who
has no way to know otherwise; the confirmed absence of Microsoft Clarity
anywhere in code; the fourth occurrence of this host's stale-worktree-
registry gap, this time for `config-site-builder`.

`chained: none` — `ENG-020` sits at `shaped`, held by the approver-facing
WIP cap rather than genuinely blocked or waiting on a human for this ticket
specifically; firing `continue ENG-020` now would only re-discover the same
cap with no new work to do. Re-check once a `decision`/`watch`/`scheduled`
pass clears `ENG-014` or `ENG-015`, or via a dedicated `continue ENG-020`
once either does. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-020-marketing-roi-attribution-reporting.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-020`) and whole-board: both exit 0, clean.

## 2026-08-29 — intake: brand-portal autopilot campaign gap shaped to ENG-019 (mass send + drip, ROI via coupon redemption), held at `shaped` — approver-facing WIP cap still full

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-client-brand-page-portal-autopilot-on-brand-portal-does-not-.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own narrower
contract, worked only this one request end to end rather than sweeping the
board — four other unshaped `agents/product-manager/inbox/` requests
untouched, each with its own `intake` event already queued or pending. Mode
check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). No genuine pre-pass gate-check this
time either — this session also started directly rather than through
`lib/eng-trigger.sh`'s own pre-pass injection, same gap the immediately
preceding `ENG-016` entry already flagged; ran
`departments/engineering/lib/eng-gate-check.sh` for real after finishing
this ticket's edits instead (see below), the only verdict this entry can
honestly report.

**Caps checked fresh from `inbox/` directly, not the cached header, twice —
once before starting and again immediately before deciding whether to
raise G1.** Both checks agreed: `ENG-014`'s and `ENG-015`'s G1s both still
read `decision:` empty — approver-facing WIP substantively 2/2, at cap,
unchanged from the header going into this pass. The
`ENG-009`/`ENG-010`/`ENG-012`/`ENG-013`-question backlog remains answered
but unprocessed (unchanged, still off the count per this board's
established convention) — a further consecutive pass without a `decision`
event or dead-end sweep clearing it; re-flagged in `observations.md`, not
fixed here, out of scope for this `intake` event.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading, grounded in live code read across `restaurant-portal`
and `aiorders-api` (created this host's missing `restaurant-portal`
worktree to do it — see below), plus a blind architect reading (subagent,
`opus`, raw request + `knowledge/business-profile.md` only, no repo access,
no exposure to this PM's own reading). **No material divergence** — both
independently converged on the same core shape: a self-service send
capability layered beside the existing reactive `Automations` engine, a new
campaign/audience/scheduling data model, and an ROI mechanism that doesn't
exist today. The architect's blind reading additionally, unprompted, raised
CASL consent exposure, cross-tenant scoping, durable scheduling
infrastructure, and whether a restaurant-initiated send needs its own
approval step — the last resolved as a non-issue (this repo's own
human-approval constitution governs business-os's own outbound content, not
a feature the AIOrders product exposes to its own paying customers) rather
than a real fork. Full comparison in the PRD's own Readback section.

**Investigated both touched repos before proposing anything.** This host's
`$ENG_WORKTREES` held `aiorders-api` and `aiorders-admin-hub` but not
`restaurant-portal` — third occurrence of the gap the architect first
flagged 2026-08-29 for `aiorders-api` (`config/projects.md`'s "all five
already exist" is a stale, Mac-only verification); created it with the same
`git worktree add -b eng/base` command `lib/eng-setup.sh` runs, one project
rather than the full script, same as that occurrence. Confirmed a real,
load-bearing naming collision before writing anything: the brand portal
already has a nav item called "Campaigns" (`pages/campaigns/*`,
`services/campaignService.ts`, the `influencer_campaigns` table) that is
entirely about inviting influencers to visit and post — unrelated to this
request, and this PRD proposes a different label ("Broadcasts") for the new
capability specifically to avoid it. Confirmed the brand portal's
`Automations` page (`pages/autopilot/Automations.tsx`) is real,
restaurant-facing self-service already, but every one of its trigger types
(`TriggerType` in `types/autopilot.ts`) is reactive — tied to a customer
lifecycle event — with no manual, scheduled, mass, or drip concept
anywhere. Confirmed `offers.coupon_code` is already wired into three
existing offer-based automations, the reuse target this PRD's proposed ROI
mechanism (acceptance criterion 4) is built on rather than new tracking.
Confirmed `outgoing-communications/actors/brands.ts`'s own
`sendPerformanceReport`/`sendMonthlySummary` actions are unimplemented
`TODO` stubs — the platform already intended owner-facing reporting once
and never finished it, worth knowing before assuming either function does
anything today. Also confirmed `pg_cron` is already live in this database
(`platform_analytics_cron`), useful precedent for the scheduled-send/drip
dispatch mechanism this ticket's architect will need to design.

**Filed `ENG-019`** (project `restaurant-portal` — primary; `aiorders-api`
also touched and named explicitly in the PRD, same multi-repo/singular-
`project:`-field precedent `ENG-003`/`ENG-016` set; size `L`; severity
`P2`, calibrated against `ENG-013`/`ENG-016`/`ENG-017`'s same "real
capability gap, real manual workaround" shape). PRD:
`agents/product-manager/specs/ENG-019-restaurant-marketing-broadcasts.md`.
Scoped deliberately smaller than the raw request's full ask: ROI ships as
coupon-redemption tracking only (reusing existing `offers` plumbing), with
open/click attribution and richer segmentation named as Non-goals /
proposed later work rather than built now — same "ship the coherent core,
name the harder measurement layer as follow-on" shape `ENG-014`'s two-item
split and `ENG-016`'s deferred deeper-autopilot item both already used on
this board.

**Held at `shaped`, not advanced to `awaiting-scope`.** Approver-facing WIP
is substantively 2/2 (`ENG-014`, `ENG-015`) — per `eng_build_loop.md`'s
Guards, same move this instance's three immediately preceding intake passes
all made. G1 content (readback, both readings' comparison, non-goals,
recommendation) is fully drafted in the PRD's own Decision section and
ready to raise the moment a slot frees. **1 transition**
(`intake → shaped`), well under the cap of 4. **Consequence:** no cap
numbers change — `shaped` counts toward neither approver-facing WIP nor
machine WIP (still 4/6).

No `inbox/` item raised this pass (no G1 to notify on yet), so no
`lib/eng-notify.sh` call.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract — not run beyond the fresh cap-verification above. `ENG-007`
through `ENG-018` otherwise untouched.

**Observations filed** (`observations.md`): the confirmed "Campaigns"
naming collision (influencer outreach, not customer messaging) and the
label chosen to avoid it; the confirmed reactive-only shape of every
existing `Automations` trigger type; the reusable `offers.coupon_code` and
`pg_cron` prior art; the unimplemented brand performance-report/monthly-
summary stubs; the third occurrence of this host's stale-worktree-registry
gap.

`chained: none` — `ENG-019` sits at `shaped`, held by the approver-facing
WIP cap rather than genuinely blocked or waiting on a human for this ticket
specifically; firing `continue ENG-019` now would only re-discover the same
cap with no new work to do. Re-check once a `decision`/`watch`/`scheduled`
pass clears `ENG-014` or `ENG-015`, or via a dedicated `continue ENG-019`
once either does. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-019-restaurant-marketing-broadcasts.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-019`) and whole-board: both exit 0, clean.

## 2026-08-29 — scheduled: whole-board safety-net sweep clears the four-item answered-gate backlog, finds and re-fires ENG-008's broken chain

`scheduled` event pass, context `schtasks` — the four-times-daily safety
net, not a single-ticket event, so this entry covers the whole board
rather than one request. Mode check clean (business-os `.env` → `MODE=`
empty); pre-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board: exit 0, clean.

**Cleared the answered-but-unprocessed backlog this board's own header had
flagged for five consecutive passes.** `ENG-009` and `ENG-010`'s G1s
(approved), `ENG-012`'s G1 (rejected), and `ENG-013`'s presignup-leads
standing question (approved) were each read fresh from `inbox/`, acted on,
journaled, and moved to `_handled/`:
- `ENG-009` — design work corrected the ticket's own premise before
  writing it (`followers`/`engagement`/growth fields already exist and are
  already displayed, same edit-capability-gap shape `ENG-008` already
  found for region/campaign-type — the note `ENG-008`'s design doc claimed
  it had left here didn't actually exist; caught and corrected, see
  `observations.md`). No one-way door. `awaiting-scope → designed →
  ready`.
- `ENG-010` — new `influencer_notes` table and a dedicated handler with a
  narrower authorization check than `admin-portal`'s shared gate (excludes
  `partner-admin`/`partner-user`, matching this ticket's own G1 default).
  Also corrects an unverified citation in the ticket's own risk section
  (see `observations.md`). No one-way door. `awaiting-scope → designed →
  ready`.
- `ENG-012` — G1 read as a plain rejection ("later"), not the
  reading-under-rejection shape `ENG-011`'s tickets-question had.
  `awaiting-scope → dropped`.
- `ENG-013`'s presignup question — "yes" (Reading B) already had its own
  ticket: an independent `intake` pass the same day had already filed
  `ENG-017` from a different raw request and cited this same answer as
  grounding. Closed against `ENG-017` rather than filed twice.

Full reasoning on each ticket's own log; design docs at
`agents/architect/designs/ENG-009-influencer-engagement-info.md` and
`agents/architect/designs/ENG-010-influencer-relationship-notes.md`. Both
G1s not previously journaled now are (`decision-journal.md`); `ENG-009`'s
own G1 was already journaled at approval time.

**Dead-end sweep found a broken chain, not just a slow queue.** `ENG-008`'s
own log claims `chained: ENG-008` with the trigger fired, but no
`continue (ENG-008)` pass ever ran — absent from `traces/.pending` and
from every `pass start:` line in today's full loop log; no branch exists
in either worktree. Re-fired `/bin/sh
departments/engineering/lib/eng-trigger.sh continue ENG-008` this pass
(queued cleanly behind this pass's own held lock — confirmed via the
trigger's own "pass in flight" log line, no race). Full reasoning on
`ENG-008`'s own log and `observations.md`. `ENG-009` and `ENG-010` are
deliberately **not** chained yet — both extend/reuse code `ENG-008` builds
first, and three tickets' own notes all flagged the same same-file
concurrent-edit risk; re-check once `ENG-008` reaches `in-review` or
later.

**Merge detection:** no ticket sits at `blocked` — nothing to reconcile
against git ancestry this pass.

**No new gate item raised this pass** (only closures), so no
`lib/eng-notify.sh raise` call. Approval cap and approver-facing WIP are
now mechanically clean, not just substantively — both counts agree with
`inbox/`'s actual contents for the first time in six passes; see the
header above.

**Consequence:** machine WIP 4/6 → 6/6 (**at cap** — `ENG-007`
ready-to-ship; `ENG-008`/`ENG-009`/`ENG-010`/`ENG-011`/`ENG-013` ready;
nothing further can enter `ready` until one clears). Approver-facing WIP
and approval cap unchanged in substance (still `ENG-014`+`ENG-015` only)
but now mechanically exact.

**Observations filed** (`observations.md`, six rows this pass): the
backlog clearing itself; two unverified-citation catches in the same
design pass; the partner-admin/partner-user authorization question left
open on `ENG-008`/`ENG-009`; `ENG-008`'s broken-chain finding; the
machine-WIP-at-cap note above.

`chained: none` for this entry itself — a whole-board sweep, not a
single-ticket `continue`; each ticket's own chain decision is recorded on
its own log (`ENG-008` re-fired; `ENG-009`/`ENG-010` deliberately held;
`ENG-007`/`ENG-011`/`ENG-013` already correctly chained and untouched;
`ENG-014`–`ENG-020` genuinely waiting on the approver or the
approver-facing WIP cap, also untouched). Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean.

## 2026-08-29 — intake: "no autopilot for sales staff/resellers" split into ENG-017 (presignup lead nurture) and ENG-018 (demo account), both held at `shaped` — approver-facing WIP cap still full

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-no-autopilot-on-admin-panel-for-our-sales-staff-resellers-to.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own
narrower contract, worked only this one request end to end rather than
sweeping the board — five other unshaped `agents/product-manager/inbox/`
requests untouched, each with its own `intake` event already queued or
pending. Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (no ticket yet
to scope to): exit 0, clean.

**Caps checked fresh from `inbox/` directly, not the cached header.**
`ENG-014`'s and `ENG-015`'s G1s both still sit in `inbox/`, unanswered —
approver-facing WIP substantively 2/2, at cap, exactly as the header
already read. The `ENG-009`/`ENG-010`/`ENG-012`/`ENG-013`-question backlog
remains answered but unprocessed (unchanged, still off the count per this
board's established convention) — now a further consecutive pass without a
`decision` event or dead-end sweep clearing it; re-flagged in
`observations.md`, not fixed here, out of scope for this `intake` event.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading, grounded in a live search across all five repos,
plus a blind architect reading (subagent, `opus`, raw request +
`knowledge/business-profile.md` only, no repo access, no exposure to
this PM's own reading). **No material divergence** — both independently
read the raw request as **two** bundled asks (a demonstration account; and
stage-triggered nurture automation for the sales/admin lead pipeline), both
independently named "autopilot" as the existing customer-marketing engine
redirected at a second audience, and both independently flagged
reseller-vs-internal-staff scoping as a real, load-bearing prerequisite
rather than a detail. The architect's blind reading additionally,
unprompted, raised CASL-style consent exposure for cold-lead messaging and
demo-data isolation from real sends/analytics — both checked against live
code (see below) and confirmed real, not speculative.

**A significant cross-reference surfaced during investigation, used as
evidence but deliberately not acted on beyond that.** This request
substantially restates `ENG-013`'s own presignup-leads standing question
(`inbox/2026-08-29-eng013-presignup-leads-question.md`), already
`decision: approved` with explicit verbatim direction — "autopilot built
to nurture these leads to next stages autpmatically and send them
emails/sms to nurture" — but still sitting unprocessed, part of the same
backlog flagged every pass this session. Treated as **confirmed** grounding
evidence for `ENG-017`'s core mechanism rather than re-derived from
scratch; that gate item itself was **not** touched, moved, or journaled by
this pass — it belongs to `ENG-013`'s own lifecycle, out of scope for an
`intake` event about a different request. Flagged plainly in both tickets'
Notes and in `observations.md` so a future `decision`/dead-end-sweep pass
points that item at `ENG-017` instead of shaping a duplicate.

**Investigated all five repos before proposing anything.** Confirmed the
`leads` (website "become a client") table has no stage column and no
consent flag at all, unlike the catering-request flow's explicit
`consent_sms`/`consent_email`. Confirmed the existing `autopilot`/
`outgoing-communications` engine's `communication_templates`/`trigger_type`
model is hard-scoped to `restaurant_id` and a closed set of
customer-lifecycle triggers — a presignup lead fits neither, so a
lead-nurture engine reuses the underlying send services but needs a
parallel trigger/template layer, not a drop-in extension; the router's
`actor: 'admin'` path exists but all three of its handlers are
unimplemented `TODO` stubs. Confirmed no mechanism anywhere attributes a
website lead to a specific reseller (no referral code, no `partner_id` on
`leads`). Separately, searched all five repos for any existing demo/sandbox
concept: the only hit, `config-site-builder/public/config/
demo-restaurant.json`, is a static SEO/config fixture, not a working
account — confirmed genuinely net-new, and, combined with `ENG-011`'s
prior finding of a live platform-wide analytics rollup
(`platform_analytics_cron`), grounds why demo-activity isolation is written
as an acceptance criterion rather than an implementation detail.

**Filed two tickets, not one** — the raw request bundles two independently
shippable pieces with different acceptance criteria and different primary
surfaces, same split precedent this instance has applied all session
(`ENG-009`/`ENG-010`, `ENG-011`/`ENG-012`, `ENG-014`'s two-item split):
- `ENG-017` — Autopilot nurture for the presignup sales lead pipeline
  (project `aiorders-api`; `aiorders-admin-hub` touched; size `L`;
  severity `P2`). PRD:
  `agents/product-manager/specs/ENG-017-presignup-lead-nurture-autopilot.md`.
  Reseller access, and extending nurture to the Brands-page/Foodswipe-
  funnel stage fields, both proposed as non-goals/follow-on work rather
  than assumed in.
- `ENG-018` — Sales demonstration account (project `aiorders-admin-hub`;
  `restaurant-portal`, `config-site-builder`, `aiorders-api` touched; size
  `L`; severity `P2`). PRD:
  `agents/product-manager/specs/ENG-018-sales-demonstration-account.md`.
  Reseller-branded demo clones proposed as a non-goal/follow-on; one
  shared, neutrally-branded demo tenant proposed as the buildable-now
  default.

**Both held at `shaped`, not advanced to `awaiting-scope`.**
Approver-facing WIP is substantively 2/2 (`ENG-014`, `ENG-015`) — per
`eng_build_loop.md`'s Guards ("Approver WIP limit (2)... at the limit,
nothing new starts that will need them"), same move this instance's own
immediately preceding pass made for `ENG-016`. Both PRDs' G1 content
(readback, non-goals, recommendation) is fully drafted and ready to raise
the moment a slot frees. **1 transition each** (`intake → shaped`), well
under the cap of 4. **Consequence:** no cap numbers change — `shaped`
counts toward neither approver-facing WIP nor machine WIP (still 4/6).

No `inbox/` item raised this pass (no G1 to notify on yet), so no
`lib/eng-notify.sh` call.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract — not run beyond the fresh cap-verification above. `ENG-007`
through `ENG-016` otherwise untouched.

**Observations filed** (`observations.md`): the `ENG-013`
standing-question cross-reference and the recommendation against
duplicating it; the confirmed-absent stage/consent concepts and the
restaurant-scoped shape of the existing autopilot data model; the
confirmed-absent demo/sandbox concept across all five repos and the live
analytics rollup that makes isolation load-bearing.

`chained: none` — both `ENG-017` and `ENG-018` sit at `shaped`, held by the
approver-facing WIP cap rather than genuinely blocked or waiting on a human
for either ticket specifically; firing `continue` on either now would only
re-discover the same cap with no new work to do. Re-check once a
`decision`/`watch`/`scheduled` pass clears `ENG-014` or `ENG-015`, or via a
dedicated `continue ENG-017`/`continue ENG-018` once either does. Full
detail on each ticket's own log
(`agents/eng-manager/board/ENG-017-presignup-lead-nurture-autopilot.md`,
`agents/eng-manager/board/ENG-018-sales-demonstration-account.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-017`, `ENG-018`) and whole-board: all three exit 0, clean.

## 2026-08-29 — intake: catering page self-serve quote generator shaped to ENG-016, held at `shaped` — approver-facing WIP cap full

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-for-catering-page-need-next-step-quote-generator-page-which-.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own narrower
contract, worked only this one request end to end rather than sweeping the
board — six other unshaped `agents/product-manager/inbox/` requests
untouched, each with its own `intake` event already queued or pending. Mode
check clean (business-os `.env` → `MODE=` empty). **No genuine pre-pass
gate-check this time** — this session started directly rather than through
`lib/eng-trigger.sh`'s own pre-pass injection, so there is no baseline
verdict from before this pass's edits began; noted plainly rather than
claimed. Ran `departments/engineering/lib/eng-gate-check.sh` for real after
finishing this ticket's edits instead (see below), which is the only
verdict this entry can honestly report.

**Caps checked fresh from `inbox/` directly, not the cached header, before
deciding how far to carry this ticket.** `ENG-014`'s and `ENG-015`'s G1s
both still sit in `inbox/`, unanswered — approver-facing WIP substantively
2/2, at cap, exactly as the header already read. `ENG-009`/`ENG-010`/
`ENG-012`'s G1s and `ENG-013`'s standing question remain answered but
unprocessed (unchanged, still off the count per this board's established
convention) — now six consecutive passes without a dead-end sweep or
`decision` event clearing them; re-flagged in `observations.md`, not fixed
here, out of scope for this `intake` event.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading, grounded in live code read across all three repos
this touches, plus a blind architect reading (subagent, `opus`, raw
request + `knowledge/business-profile.md` only, no repo access, no
exposure to this PM's own reading). **No material divergence on the core
shape** — both independently converged on: a catering lead flow that
dead-ends today without an automated path to a price; a self-serve quote
builder with menu selection delivered as an SMS/email link; an
owner-configurable toggle between real pricing and a generic
acknowledgement; automatic stage progression; and owner edit/resend plus
deeper `autopilot` use as separable, later work. **Two real forks
surfaced**, neither assumed away: (1) whether the "generic message"
fallback is the restaurant owner's site-wide setting or the customer's own
per-visit choice — resolved by proposing both, the same "cheap either way"
resolution the approver preferred at `ENG-008`; (2) whether "menu
selection" reuses the existing menu's own per-item prices or implies a new
catering-specific pricing model — resolved by proposing reuse, correctable
at G1. Both bundled into the PRD as G1 riders rather than a separate
blocking standing question, the same bar `ENG-015`'s G1 used for its own
small fork.

**Investigated all three touched repos before proposing anything.**
Confirmed in `config-site-builder`: a live public `Catering.tsx` page whose
own "How It Works" copy already promises a step ("Customize Your Menu")
that doesn't exist anywhere in the code; its `CateringForm.tsx` posts to
`aiorders-api`'s `catering-request` function, which inserts into the
`catering` table, creates a CRM customer record, and notifies the
**restaurant owner only** — nothing is ever sent back to the customer
beyond an on-page "we'll contact you" message, confirming the exact gap
named in the request. Confirmed in `restaurant-portal`: a real, shipped
5-status kanban (`CateringKanban`/`StatusUpdateModal`/
`CateringDetailModal`) with all five status strings hardcoded across three
files and no server-side enum, so a sixth ("Quote Sent"-style) value is
additive, not a migration. Confirmed in `aiorders-api`: a mature, already-
shipped `autopilot`/`outgoing-communications` engine (DB-trigger-initiated,
queued, per-restaurant customizable templates, already sending customer
email/SMS) that today only fires on customer-lifecycle events, never
catering — the concrete system the request's own "autopilot" mention
names, and the natural target for the deeper-automation item named as
future work rather than built now. Also confirmed `restaurant-marketplace`
and the CloudWaitress popup widget each have their own, separate catering-
submission code paths — grounding the PRD's scoping to `config-site-
builder`'s own catering page only, the one surface the raw text actually
names.

**Filed `ENG-016`** (project `config-site-builder` — primary; `aiorders-api`
and `restaurant-portal` also touched and named explicitly in the PRD,
following the multi-repo/singular-`project:`-field precedent `ENG-003`
set; size `L`; severity `P2`, calibrated against `ENG-013`'s same
"real capability gap, real manual workaround" shape rather than `ENG-011`'s
lighter `P3`). PRD:
`agents/product-manager/specs/ENG-016-catering-quote-generator.md`.

**Held at `shaped`, not advanced to `awaiting-scope`.** Approver-facing WIP
is substantively 2/2 (`ENG-014`, `ENG-015`) — per `eng_build_loop.md`'s
Guards ("Approver WIP limit (2)... at the limit, nothing new starts that
will need them"), this ticket was carried through readback and PRD-writing
(agent-owned work, costs the approver's queue nothing) but not advanced
into a state that would raise a third open G1 against a cap of two. The
PRD's G1 content (readback, both forks named as riders, recommendation) is
fully drafted and ready to raise the moment a slot frees — nothing further
to shape. **1 transition** (`intake → shaped`), well under the cap of 4.
**Consequence:** no cap numbers change — `shaped` counts toward neither
approver-facing WIP nor machine WIP. Machine WIP unaffected (4/6).

No `inbox/` item raised this pass (no G1 to notify on yet), so no
`lib/eng-notify.sh` call.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract — not run beyond the fresh cap-verification above. `ENG-007`
through `ENG-015` otherwise untouched.

**Observations filed** (`observations.md`): the confirmed customer-side
notification gap on catering submission; the additive (no-migration)
shape of the existing hardcoded status lists; the already-shipped
`autopilot`/`outgoing-communications` engine as the concrete target for
the request's own deeper-automation ask; the answered-but-unprocessed
inbox backlog, still unresolved, now six consecutive passes old.

`chained: none` — `ENG-016` sits at `shaped`, an agent-owned state, but
held there by the approver-facing WIP cap rather than genuinely blocked or
waiting on a human for this ticket specifically; firing `continue
ENG-016` now would only re-discover the same cap with no new work to do.
Re-check once a `decision`/`watch`/`scheduled` pass clears `ENG-014` or
`ENG-015`, or via a dedicated `continue ENG-016` once either does. Full
detail on the ticket's own log
(`agents/eng-manager/board/ENG-016-catering-quote-generator.md`). Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-016`) and
whole-board: both exit 0, clean.

## 2026-08-29 — intake: agency/reseller brand-scoping shaped to ENG-015 — two of four reported symptoms confirmed and traced to exact code, two found already fixed

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-admin-portal-is-not-optimized-for-new-agency-users-resellers.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own narrower
contract, worked only this one request end to end rather than sweeping the
board — seven other unshaped `agents/product-manager/inbox/` requests
untouched, each with its own `intake` event already queued or pending. Mode
check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (no ticket yet
to scope to): exit 0, clean.

**Caps verified fresh from `inbox/` directly before raising**, same practice
every pass today has used: `ENG-009`'s and `ENG-010`'s G1s and `ENG-013`'s
standing question all read `decision: approved` but sit unprocessed;
`ENG-012`'s G1 reads `decision: rejected`, also unprocessed — all four
treated as closed for cap arithmetic per this board's established
convention. Only `ENG-014`'s G1 was genuinely open before this pass:
approver-facing WIP 1/2, approval cap 1/3, one WIP slot and two approval
slots free.

**This request carried real severity, flagged in advance.** A `watch`
pass earlier today (`observations.md`, 2026-08-29) had already read the raw
request closely enough to note it reads as "a cross-tenant authorization
boundary gap... not a UI polish item" and to ask whoever shaped it to give
it real severity rather than routine `P3`. Treated that as a pointer to
verify, not a conclusion to inherit untested — see Investigation below.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading plus a blind architect reading (subagent, `opus`, raw
request + `knowledge/business-profile.md` only, no repo access, no exposure
to this PM's own reading). **No material divergence on intent** — both
converged on a systemic, data-layer tenancy-scoping gap rather than
isolated page bugs, and the architect's reading independently guessed that
an agency→brand→location ownership relationship would have to already
exist for the request to make sense — confirmed true against the live
schema before writing anything (see below).

**Investigated both live repos in depth before proposing anything**, same
practice every ticket today has used, deeper here because the raw request
names four separate symptoms across four pages. Confirmed the
`partner-admin`/`partner-user` role pair already exists and already has a
real brand-ownership relationship (`brands.partner_id`, backing a working
`/partners/:id/assign-brands` screen) — this is a propagation gap in an
existing model, not a greenfield access-control build. Traced the two
symptoms that are genuinely real to exact code: `admin-portal/handlers/
restaurants.ts`'s `getRestaurants()` always uses the service-role client
with no role check at all (unlike its sibling `brands.ts`, which already
branches service-role-only-for-`admin`), and the `restaurants` table's only
`INSERT`-capable RLS policy names `admin`/`sub-admin` only, which is why the
existing "Add Restaurant" modal's direct client-side insert silently fails
for a partner caller. Also traced the other two named symptoms
(Dashboard, Influencers) to exact code and found them **already blocked
outright** for partner roles today — not leaking, not scoped, just denied
— and resolved the raw text's ambiguous "or user" by checking `/users`
directly rather than asking the approver to pick a reading: also already
admin-only, both frontend and backend. Caught and corrected one of my own
mid-investigation misreads before it reached the PRD (an `AppSidebar.tsx`
conditional read in isolation, which looked like partner access but on
reading its actual branch body and `ProtectedRoute.tsx` in full turned out
to be a hide/deny) — logged in the ticket rather than silently fixed, same
practice this instance applies to any other artifact's claim.

**Filed `ENG-015`** (`awaiting-scope`, size `M`, project
`aiorders-admin-hub`, `type: security`, severity `P1` — real, live,
code-confirmed cross-tenant data exposure on a reachable admin page, for
real onboarded users, today; short of P0 since this is a latent access-control
gap rather than an active incident). PRD:
`agents/product-manager/specs/ENG-015-agency-reseller-brand-scoping.md`. G1:
`inbox/2026-08-29-eng015-g1-scope.md` — raised despite `security` being on
`definition-of-done.md`'s G1-auto-skip list, a deliberate departure logged
in the ticket's own Notes: a real (if small) policy fork exists that the
raw request doesn't address (should a partner-created restaurant
auto-approve like an admin-created one, or hold for review — proposed
default: hold), and two of the four reported symptoms don't reproduce on
this branch, both worth a one-tap confirm-or-correct rather than silently
deciding either way. No separate standing-question item this time, unlike
`ENG-011`/`ENG-013` — the auto-approve fork is a single default, not a
scope fork that could roughly 10x the ticket's cost, so it's bundled into
this same G1 rather than given its own gate.

**2 transitions** (`intake → shaped → awaiting-scope`), well under the cap
of 4 — the next state needs the approver, so this pass stops here by
design. **Consequence:** approver-facing WIP 1/2 → 2/2 (at cap, not over);
approval cap 1/3 → 2/3 (one slot free); machine WIP unaffected (4/6).

Ran `departments/engineering/lib/eng-notify.sh raise` on the new `inbox/`
item — logged the already-open `SLACK_WEBHOOK_URL unset` failure
(`traces/eng-notify-2026-08-29.log`, 13:26:06 local), consistent with every
gate raised on this instance today; `notified:` hand-stamped per
established practice (the field was first written with a stale timestamp
copied from `ENG-014`'s own example by mistake, caught and corrected before
the raise, not after). No dissent section on the G1 — `agents/critic/
agent.md` still doesn't exist (open proposal, `proposals.md` 2026-08-25
row), confirmed absent again rather than assumed.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract — not run beyond the fresh cap-verification above. `ENG-007`
through `ENG-014` otherwise untouched. The answered-but-unprocessed backlog
(`ENG-009`/`ENG-010`/`ENG-012`/`ENG-013`-question) is now five consecutive
`intake` passes old without a `decision` event or dead-end sweep picking
any of them up — re-flagged in `observations.md`, not fixed here, same as
every pass before this one.

**Observations filed** (`observations.md`): the precise root-cause trace for
both confirmed defects; the page-by-page "deny outright rather than scope"
pattern the three already-blocked pages share; the corrected mid-investigation
misread.

**Board:** rolled the oldest of three live dated entries (`intake: foodswipe
funnel page shaped...`) into `_index-archive.md`, newest-first per that
file's own convention, before adding this entry — net three entries live
after this one, matching the keep-three rule. Extracted and moved
programmatically (exact line range, not retyped) to avoid transcription
drift on a ~150-line entry.

`chained: none` — `ENG-015` sits at `awaiting-scope`, owned by the
approver; the chaining guard never fires on a ticket waiting on a human.
Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-015-agency-reseller-brand-scoping.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-015`) and whole-board: see pass notes.

## 2026-08-29 — continue ENG-007: recovered an unrecorded build already through security, real ready-to-ship devops work done fresh

`continue` event pass, context `ENG-007`. Per this event's own narrower
contract, resumed only this ticket from its current state — no board-wide
sweep. Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`) and
whole-board: both exit 0, clean.

**Found the ticket's own board file still reading `ready` while four
complete, dated, mutually-consistent gate receipts already sat on disk**
(migration, code review, QA, security — all citing commit `2aec86f` on
`loyalty-system`). Verified fresh rather than trusted: confirmed the commit
is real, pushed, and unmerged (`git merge-base --is-ancestor` → not an
ancestor of `origin/main`); confirmed no PR is open yet (`gh pr list --head
loyalty-system --state all` shows only `ENG-006`'s already-merged one);
independently re-ran `deno test`/`check`/`lint` against the live worktree
rather than trusting the receipts' own claims — 44/44 passing, clean check,
clean lint, matching every receipt exactly. Recorded the recovered state
machine (`ready → building → in-review → in-security`, 3 transitions) and
then did the genuinely new work `ready-to-ship` still owed — release plan,
rollback, observability, and a $0/month cost delta, none of which any prior
receipt covered — reaching `ready-to-ship` (4th transition, at this pass's
cap). Release window checked fresh and found closed (Saturday,
`block_weekends`) but deliberately left for the next hop to act on, same
split `ENG-006` used at this identical boundary. Full detail, every command
run, and every citation on the ticket's own log
(`agents/eng-manager/board/ENG-007-per-restaurant-loyalty-configuration.md`).

**Consequence:** `machine_wip` unaffected (`ENG-007` was already inside the
counted `ready..ready-to-ship` range at `ready`, stays inside it at
`ready-to-ship`, still 4/6). Approver-facing WIP and approval cap both
unaffected — no gate raised this pass; opening the PR (the merge request) is
the next hop's distinct work.

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for state with the chain record below. No sweep of the rest
of the board — out of scope for a `continue` event naming this ticket
specifically.

**Board:** rolled the `ENG-011` dated entry (the oldest of the four this
pass's own new entry would otherwise leave live) into `_index-archive.md`,
newest-first per that file's own convention — net three entries live after
this one, matching the keep-three rule.

**Observations filed** (`observations.md`): the recovered-unrecorded-build
shape, a third and furthest-progressed data point in the
partially-updated-artifact family `ENG-006` first named; `deno` now working
for real on this Windows host, closing the migration doc's own open fallback
attempt; Docker Desktop still not coming up within a bounded wait, second
occurrence.

`chained: ENG-007` — `ready-to-ship` is a devops-owned state, not the
approver, not blocked, not terminal, not held by a cap. Fired
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-007`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-007`) and whole-board: both run clean.

## 2026-08-29 — intake: brand-portal restaurant self-service (QR codes & marketing media) shaped to ENG-014, website-settings half named for later

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-on-the-brand-portal-restaurant-is-not-able-to-see-or-generea.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own narrower
contract, worked only this one request end to end rather than sweeping the
board — the other unshaped `agents/product-manager/inbox/` requests
untouched, each with its own `intake` event already queued or pending. Mode
check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Caps re-verified fresh from ground truth, not the cached header —
and the ground truth had moved.** All four items the header carried as
"open" or "answered-but-unprocessed" turned out, on a fresh read of
`inbox/`, to be **answered**: `ENG-009`'s and `ENG-010`'s G1s (unchanged from
prior passes, still unprocessed), `ENG-012`'s G1 (**rejected**), and
`ENG-013`'s presignup-leads question (approved) — the latter two newly
answered since the immediately preceding pass. Read as closed, not open,
for this pass's own cap arithmetic per this board's established convention
(an answered gate item is off the count immediately rather than waiting on
the mechanical `state:` field). Approver-facing WIP and approval cap both
fully free (0/2, 0/3) before this ticket's own G1 — not "one slot free" as
the pre-pass header read.

**Identified the exact repos before proposing anything.** "Brand portal" is
`restaurant-portal` (confirmed via its own `brandPortalApi.ts`), not
`aiorders-admin-hub` (the staff-only "admin portal" the request explicitly
names as inaccessible to owners). Read `restaurant-portal`'s `Website` and
`Settings` pages (only `catering`/`careers` content and an unimplemented
stub, respectively — zero QR/media/hours surface anywhere), `aiorders-admin-hub`'s
`Activation.tsx` (a "Share Bag Insert & QR with Owner" step names today's
manual workaround exactly) and `RestaurantAIWebsite.tsx` (where hours
actually live, staff-only), and `aiorders-api`'s `url-shortener` function —
confirmed it checks `profile.role === 'admin'` exactly, so the gap is a real
backend authorization boundary, not only a missing frontend screen. QR
images come from a free public API (`api.qrserver.com`) — $0/month.

**Split the request into a two-item shape, filed the first, named the
second** — same pattern `ENG-006`/`ENG-007`/`ENG-008` established.
`ENG-014` (this pass, `awaiting-scope`, project `restaurant-portal`, size
`M`) covers QR codes and marketing-media downloads only — the more tightly
bounded half (two already-live generators, restricted to the caller's own
restaurant). Item 2 (website settings, including hours) is named in the PRD
as proposed, to be filed once `ENG-014` verifies; its own scoping question
(how far "anythings related to their website" extends) is deferred to when
item 2 is actually shaped, since it doesn't gate this ticket. No separate
standing-question inbox item this time — unlike `ENG-008`/`ENG-011`/
`ENG-013`, the open gap lives entirely inside item 2's future scope and
doesn't need an approver answer to move `ENG-014` forward.

**2 transitions** (`intake → shaped → awaiting-scope`), well under the cap
of 4 — the next state needs the approver, so this pass stops here by
design. Consequence: approver-facing WIP 0/2 → 1/2; approval cap 0/3 → 1/3.
Machine WIP unaffected.

Ran `departments/engineering/lib/eng-notify.sh raise` on the new `inbox/`
item — logged the already-open `SLACK_WEBHOOK_URL unset` failure
(`traces/eng-notify-2026-08-29.log`, 05:08:45 local / 12:08:45 UTC),
consistent with every gate raised on this instance recently; `notified:`
hand-stamped per established practice. No dissent section on the G1 —
`agents/critic/agent.md` still doesn't exist (open proposal,
`proposals.md` 2026-08-25 row), confirmed absent again rather than assumed.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract — not run beyond the fresh cap-verification above. `ENG-007`
through `ENG-013` otherwise untouched.

**Observations filed** (`observations.md`): the confirmed admin-only
`url-shortener` gate and the free-QR-provider cost finding grounding this
PRD; and — flagged more pointedly this time — the answered-but-unprocessed
inbox backlog is now **four items deep and four consecutive passes old**
(`ENG-009`, `ENG-010`, `ENG-012`, `ENG-013`'s question), with no pass yet
picking it up. Worth a dead-end sweep or a `decision` event rather than a
fifth re-verification.

`chained: none` — `ENG-014` sits at `awaiting-scope`, owned by the approver;
the chaining guard never fires on a ticket waiting on a human. Full detail
on the ticket's own log
(`agents/eng-manager/board/ENG-014-restaurant-qr-media-self-service.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-014`) and whole-board: see pass notes.

---

## 2026-08-29 — decision ENG-010 (G1 scope): the predicted twin no-op — arrived after the fact was already consumed

`decision` event pass, context `inbox/_handled/2026-08-29-eng010-g1-scope.md`
— the same duplicate-queued-event shape already logged three times on this
board today (`ENG-008`'s two gate items, then `ENG-009`'s G1, all now
archived). Per this event's own narrower contract (act on the answered gate
item, advance only the ticket it belongs to), scoped to `ENG-010` only — no
board-wide sweep. Mode check clean (business-os `.env` → `MODE=` empty;
instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
whole-board: both exit 0, clean.

**Confirmed rather than assumed.** This item's own frontmatter
(`decision: approved`, `decided: 2026-08-29T10:49:55.456343+00:00`) already
carries a processed footer — "Processed 2026-08-29 (`scheduled` event pass,
context `schtasks`)" — naming the exact pass that consumed it: design work
done (new `influencer_notes` table, dedicated handler), the ticket moved
`awaiting-scope → designed → ready`, journaled
(`agents/eng-manager/config/decision-journal.md`), and the gate item itself
already relocated to `inbox/_handled/`. Checked fresh rather than trusted:
the ticket's own frontmatter (`state: ready`, `owner: eng-manager`) and its
own log entry for that same pass agree with the footer. Nothing left for
this event to act on.

**0 transitions.** No cap affected — this ticket was already inside the
counted `ready`..`ready-to-ship` machine-WIP range (6/6, at cap) before this
pass, and this G1 was already off both the approver-facing WIP and
approval-cap counts.

**Dead-end sweep (scoped to this event):** `ENG-008` — the ticket this
one's own sequencing hold depends on — still sits at `ready` with no branch
or build started. This ticket's existing sequencing hold (re-check once
`ENG-008` reaches `in-review` or later) therefore still applies unchanged.
Nothing to resume.

**Notify sweep:** nothing to raise (no new gate item); nothing to nudge
(this item's `notified:`/`decision:` cycle closed same-day, hours before
this pass).

`chained: none` — no state change; `ENG-010` remains held at `ready`
pending `ENG-008`. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-010`) and whole-board: both exit 0, clean. Full detail on the
ticket's own log
(`agents/eng-manager/board/ENG-010-influencer-relationship-notes.md`).

---

## 2026-08-29 — intake: foodswipe funnel page shaped, designed and readied same-pass after a mid-flight G1 approval; a pre-signup-leads question raised separately

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-for-the-foodswipe-sales-funnel-page-we-are-not-able-to-or-th.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own
narrower contract, worked only this one request end to end rather than
sweeping the board — nine other unshaped `agents/product-manager/inbox/`
requests untouched, each with its own `intake` event already queued or
pending. Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (no ticket yet
to scope to): exit 0, clean.

**Caps verified fresh from ground truth before raising.** `ENG-009`'s and
`ENG-010`'s G1s (`inbox/2026-08-29-eng009-g1-scope.md`,
`inbox/2026-08-29-eng010-g1-scope.md`) still sit answered-but-unprocessed —
the same pair the immediately preceding `ENG-011` pass found (see
`observations.md`, 2026-08-29). Treated as closed for cap arithmetic per
this board's established convention. Only `ENG-012`'s G1 was genuinely
open before this pass: approver-facing WIP 1/2, approval cap 1/3, both
with room for one more.

**Identified the exact page before writing anything.** "Funnel" as a
keyword matches exactly one file in `aiorders-admin-hub`:
`src/pages/FoodswipeListings.tsx` ("Foodswipe Listings" — a six-column
kanban already tracking "restaurant onboarding progress across stages,"
plus a funnel-conversion summary). Read it and its backend handler
(`aiorders-api`'s `admin-portal/handlers/foodswipe.ts`) in full before
proposing anything: **confirmed zero write path anywhere** — no
click/drag/edit affordance in the frontend, no mutation branch in the
handler despite it technically accepting `POST`, `classifyStage()` a pure
function over existing columns. Searched the whole API repo for any
staff-assignable status concept (`assigned_to`, `lead_status`,
`crm_stage`, `sales_stage`, `contact_status`, `owner_id`) — none exist;
confirmed net-new, same shape `ENG-011` found for "tickets." Ruled out
`Leads.tsx` (real edit UI, but for an unrelated record type — website-
interest-form leads, not Foodswipe profiles) and found `claim_status`
(the one plausible existing status field) is dead — written once to a
constant, read nowhere.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading plus a blind architect reading (subagent, `opus`,
raw request + `knowledge/business-profile.md` only, no repo access, no
exposure to this PM's own reading). **No material divergence on
direction** — both converged on an existing, currently non-functional
admin page that should let staff act on a pipeline; both independently
flagged "update" as ambiguous between move-stage and edit-details. The
architect's reading went one step further, unprompted: it guessed "sales"
and "onboarding" might need two different stage vocabularies for two
different phases, and that the current stages might only cover one.
Checked against the code rather than accepted or dismissed on guess
alone — **true**: all six existing stages are post-signup; nothing in
this system tracks a restaurant before it signs up. That turned a
speculative guess into a confirmed, live fork worth asking about, not
something to silently build either way.

**Filed `ENG-013`** (`awaiting-scope`, size `M`, project
`aiorders-admin-hub`, severity `P2` — calibrated against `ENG-011`'s
`P3`: this is missing *all* interactivity, confirmed in code, versus
`ENG-011`'s missing visibility+filter; still non-emergency with a
workaround, so short of P1). PRD:
`agents/product-manager/specs/ENG-013-foodswipe-funnel-stage-control.md`.
G1: `inbox/2026-08-29-eng013-g1-scope.md`. Standing question (pre-signup
leads): `inbox/2026-08-29-eng013-presignup-leads-question.md`. Both
raised via `lib/eng-notify.sh raise`, both logged the already-open
`SLACK_WEBHOOK_URL unset` failure (`traces/eng-notify-2026-08-29.log`,
04:39:39 and 04:39:45 local), `notified:` hand-stamped on both (converted
to UTC) per established practice.

**2 transitions** (`intake → shaped → awaiting-scope`), well under the cap
of 4 — the next state needs the approver, so this pass stopped here by
design, momentarily. **Consequence at that point:** approver-facing WIP
1/2 → 2/2; approval cap 1/3 → 3/3 (at cap) — this pass's own G1 plus
standing question, counted conservatively, same convention
`ENG-008`/`ENG-011` used. Machine WIP unaffected (3/6). Superseded within
the same pass — see "Continued" below.

**Board:** found `_index.md` sitting at exactly three dated entries before
this pass's own — at the keep-three limit already. Rolled the oldest
(`2026-08-29 — watch (schtasks): no ticket touched...`) into
`_index-archive.md`, newest-first per that file's own convention. Checked
for the already-documented duplicate-archive failure mode
(`observations.md`, 2026-08-29) before touching anything — not present
this time, a clean roll.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract — not run beyond the cap verification above. `ENG-007`,
`ENG-008`, `ENG-009`, `ENG-010`, `ENG-011`, `ENG-012` otherwise untouched.
`ENG-009`/`ENG-010` still due a sweep — found and correctly left again
this pass (see `observations.md`, 2026-08-29, and `ENG-011`'s own board
entry).

**Notify sweep:** both of this pass's own items raised and stamped above.
Nothing else to nudge. Approval cap briefly touched 3/3 (full) at this
point in the pass — see "Continued" below for where it settled; no
`lib/eng-notify.sh stall` fired either way, since the cap was reached (and
then relieved) by this pass's own work rather than discovered stuck.

**Observations filed** (`observations.md`): the confirmed-zero write path
and the confirmed-absent staff-status concept grounding this PRD's
defaults; the "foodswipe" brand-name overload between this ticket's
restaurant-onboarding funnel and `ENG-006`'s already-shipped
cross-restaurant consumer loyalty identity; the architect's blind-reading
guess about a pre-signup sales layer turning out to be live once checked
against code.

**Continued, same pass — `ENG-013`'s own G1 came back answered by
hand-edit while this pass was still running.** Processed inline rather
than left for a separately-queued `decision` event, per this instance's
established practice (`ENG-007`, `ENG-008`, `ENG-011` all set the same
precedent earlier today). **G1: approved, bare, no rider.** Real design
work done against the live repos before advancing: searched every
migration in `aiorders-api` for `profiles` before proposing to alter it —
none is its `CREATE TABLE`, corroborating the 2026-08-26 finding that this
repo's schema history was reconstructed after the fact and evidently still
doesn't cover `profiles`' own origin (not blocking; an `ALTER TABLE`
doesn't need it). Checked `admin-portal/index.ts`'s routing and
`leads.ts`'s existing `updateWebsiteLead` write path so the design reuses
a pattern already proven in this codebase. Design:
`agents/architect/designs/ENG-013-foodswipe-funnel-stage-control.md` — one
nullable override column on `profiles` (the only entity present at every
one of the six stages), taking precedence over the existing
`classifyStage()` derivation; new write action reuses the handler's
already-present admin/sub-admin gate. **No one-way door** — additive
column, `null` default, no backfill, no new authorization surface. Moved
straight through `designed → ready`, no G2. Moved the G1 to
`inbox/_handled/`; journaled.

**2 more transitions on `ENG-013`** (`awaiting-scope → designed → ready`),
4 total this pass on that one ticket — at the cap of 4, stopping here by
design (`building` is new implementation work, a different owning role).
**Final consequence this pass:** machine WIP 3/6 → 4/6 (`ENG-007`,
`ENG-008`, `ENG-011` unaffected, `ENG-013` newly in range); approver-facing
WIP 2/2 → 1/2 (`ENG-013`'s own path no longer runs through the approver —
its still-open standing question doesn't hold a WIP slot, since it doesn't
block the ticket); approval cap 3/3 → 2/3 (`ENG-013`'s G1 closed; its
standing question stays open, `ENG-012`'s G1 unaffected) — one slot free
again, not full.

**Observations filed** (`observations.md`): the corroborating
`profiles`-untracked-migration finding.

`chained: ENG-013` — `ready` is eng-manager-owned (a backend/database
engineer builds next), not the approver, not blocked, not terminal, not
held by a cap. Fired
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-013`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: see pass notes.

## 2026-08-29 — intake: ENG-011 shaped, designed and readied same-pass after a mid-flight G1 approval; its tickets question answered and filed as ENG-012

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-on-the-admin-panel-we-are-unable-to-see-if-the-restaurant-is.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own
narrower contract, worked only this one request end to end rather than
sweeping the board. Mode check clean (business-os `.env` → `MODE=` empty).
Pre-pass `departments/engineering/lib/eng-gate-check.sh`, whole-board (no
ticket yet to scope to): exit 0, clean.

**Caps verified fresh from ground truth, not the (stale) cached header** —
found `inbox/2026-08-29-eng009-g1-scope.md` and
`inbox/2026-08-29-eng010-g1-scope.md` both answered (`decision: approved`,
09:20:42 and 10:49:55) but still sitting in `inbox/`, unprocessed; their
tickets still read `state: awaiting-scope` on disk. Left both untouched
(dead-end-sweep/decision-event work, out of scope for an `intake` event on
an unrelated request) but read as closed, not open, for this pass's own
cap arithmetic — see the header note above and `observations.md` for the
full reasoning. Approver-facing WIP and approval cap both fully free by
that reading (0/2, 0/3) before this pass's own G1.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading plus a blind architect reading (subagent, `opus`,
raw request + `knowledge/business-profile.md` only). **No material
divergence** — both converged on the same shape: a missing stage/client
concept on the Brands page, an explicit filter requirement, undefined
health, undefined tickets. Checked both live repos before proposing
defaults, same practice `ENG-005`/`ENG-008` established: `Brands.tsx`
exists with no stage/health/ticket concept today; `onboarding_step` and
`is_active` already exist as raw, unsurfaced signals to ground a proposed
stage taxonomy; no ticket/support system exists anywhere in either repo.
Turned what could have been three guesses into two evidence-grounded
`[proposed]` defaults (stage taxonomy, minimal health signal) plus one
genuine standing question (tickets) — same move `ENG-008` made for its own
"engagement" item.

**Filed `ENG-011`** (`awaiting-scope`, size `M`, project
`aiorders-admin-hub`). PRD:
`agents/product-manager/specs/ENG-011-client-stage-health-visibility.md`.
G1: `inbox/2026-08-29-eng011-g1-scope.md`. Standing question:
`inbox/2026-08-29-eng011-tickets-source-question.md`. Both raised via
`lib/eng-notify.sh raise` — both logged the already-open
`SLACK_WEBHOOK_URL unset` failure (`traces/eng-notify-2026-08-29.log`),
`notified:` hand-stamped on both per established practice.

**2 transitions** (`intake → shaped → awaiting-scope`), well under the cap
of 4 — the next state needs the approver, so this pass stops here by
design. Consequence: approver-facing WIP 0/2 → 1/2; approval cap 0/3 → 2/3
(this pass's own reading — see header for the mechanical count, which
reads over-cap if `ENG-009`/`ENG-010` are counted literally by their
on-disk state instead).

**Board:** found `_index.md` already four dated entries deep (one over the
keep-three limit) even before this pass's own entry — and found the oldest
of those four **already duplicated verbatim in `_index-archive.md`**,
apparently left behind by an earlier roll that completed the copy but never
removed the source. Verified by direct text comparison before touching
anything, not assumed from the matching headings alone. Same general
failure family as the single already-documented "partially-updated,
self-contradictory artifact" occurrence (`observations.md`, 2026-08-28 — a
pass crashing mid-sequence between writes), though a different specific
artifact (a board roll, not a PRD/ticket edit) — noted as corroborating,
not identical. Fixed here: moved the next-oldest entry (`ENG-007`'s G2
answered) into the archive for real, and dropped the already-archived
duplicate from the live file rather than archiving it a second time. Net:
three entries now live (this one plus the two next-newest), matching the
rule.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract — not run beyond the cap verification and the board-duplicate fix
above. `ENG-007`, `ENG-008`, `ENG-009`, `ENG-010` otherwise untouched.

**Notify sweep:** both of this pass's own items raised and stamped above.
Nothing else to nudge. Approval cap 2/3 (this pass's own reading), not
full — no stall.

**Observations filed** (`observations.md`): the confirmed-absent
stage/health/ticket concepts and the evidence grounding the proposed
taxonomy; the `ENG-009`/`ENG-010` answered-but-unprocessed gate items; the
duplicated archive entry.

`chained: none` — `ENG-011` sits at `awaiting-scope`, owned by the
approver; the chaining guard never fires on a ticket waiting on a human.
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-011`) and whole-board: both exit 0, clean.

**Continued, same pass — both of `ENG-011`'s own gate items came back
answered by hand-edit while this pass was still running.** Processed both
rather than leaving them for a separately-queued `decision` event, per
this instance's established practice.

**G1: approved, bare, no rider.** Did real architect-hat design work
against the live repos before advancing: checked whether cheap internal
order data actually exists for the health signal (it does — a real
internal `orders` table plus an existing hourly
`calculate_platform_analytics()` cron already aggregating per-restaurant
order totals into Cloudflare KV, `20260217000001_platform_analytics_cron.sql` —
checking paid off by confirming feasibility this time, not by finding a
landmine). Design: `agents/architect/designs/ENG-011-client-stage-health-visibility.md` —
`stage` and `health` both derived at read time from columns/pipelines that
already exist, no new table, no new vendor. **No one-way door** — moved
straight through `designed → ready`. Moved the gate item to
`inbox/_handled/`; journaled.

**Standing "tickets" question: `decision: rejected`, free-text "Reading
A."** Read together rather than the field alone — a flat rejection
doesn't usually come with a specific named option underneath it; taken as
"build Reading A" (a minimal from-scratch ticket system), not as killing
the idea. Flagged as an interpretation, not a certainty, on the gate
item's own processed footer and in `decision-journal.md` — first
occurrence of a `decision:`/free-text mismatch on this instance, worth
asking the approver directly if it recurs rather than continuing to
infer. **Filed `ENG-012`** (`awaiting-scope`, size `L` — a genuine new
data model/CRUD surface, materially bigger than `ENG-011`'s derived-field
approach) directly from the selected reading, no fresh blind-readback
subagent run (the question itself already fully specified both options —
same light treatment `ENG-009` used answering `ENG-008`'s "engagement"
question). PRD: `agents/product-manager/specs/ENG-012-restaurant-support-tickets.md`.
G1 raised and notified: `inbox/2026-08-29-eng012-g1-scope.md`.

**2 more transitions on `ENG-011`** (`awaiting-scope → designed → ready`),
4 total this pass on that one ticket — at the cap of 4, stopping here by
design (`building` is new implementation work, a different owning role).
`ENG-012` adds its own 2 (`intake → shaped → awaiting-scope`), well under
its own cap. **Final consequence this pass:** machine WIP 1/6 → 3/6
(`ENG-007` unaffected, `ENG-008` unaffected, `ENG-011` newly in range);
approver-facing WIP and approval cap both net to substantively 1/2 and
1/3 (`ENG-012` alone) — see header for the full mechanical-vs-substantive
figures and the still-open `ENG-009`/`ENG-010` gap this pass did not
touch.

**Observations filed** (`observations.md`): the confirmed-live internal
orders/analytics pipeline `ENG-011`'s health signal now reuses; the
`decision:`-vs-free-text mismatch on the tickets question.

`chained: ENG-011` — `ready` is eng-manager-owned (a
backend/frontend/database engineer builds next), not the approver, not
blocked, not terminal, not held by a cap. Fired
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-011`
before exiting. `chained: none` for `ENG-012` — `awaiting-scope`, owned by
the approver. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-011`), scoped (`ENG-012`), and whole-board: all exit 0,
clean.

## 2026-08-29 — intake: influencer-board admin-management request shaped to ENG-008, one non-blocking question raised separately

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-for-the-influencer-board-on-admin-panel-we-are-unable-to-see.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own
narrower contract, worked only this one request end to end rather than
sweeping the board — `ENG-007` and the other pending product-manager-inbox
requests untouched. Mode check clean (business-os `.env` → `MODE=` empty).
Caps checked fresh before raising: approver-facing WIP 0/2, approval cap
0/3, both fully free.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading plus a blind architect reading (subagent, `opus`,
raw request + `knowledge/business-profile.md` only). One material
divergence — whether an influencer-facing surface already exists at all —
resolved by checking `aiorders-api`'s live `origin/main` rather than by
guessing or asking: it already has `restaurant-influencer-campaigns`
(invitation-based), an `outgoing-communications` actor for influencers, and
`migrate-influencer-images`, so this extends a real existing concept.
Both readings independently flagged "engagement" as unresolvable from the
text — a joint gap, not a disagreement — and that's the one thing sent to
the approver as a question.

**Split the request into a two-item shape, filed the first, named the
second.** `ENG-008` (this pass, `awaiting-scope`) covers the admin-side
data only — region/campaign-type preference view+edit, rating,
collaboration count, project `aiorders-admin-hub`, size `M`. Item 2
(influencer-facing opportunity visibility gated by region/campaign-type)
depends on `ENG-008`'s fields and is named in the PRD as proposed, to be
filed once `ENG-008` verifies, per the `ENG-006`/`ENG-007`
sequence-continuation precedent (`skills/acceptance-check/SKILL.md` step
6b) — this is the same request's other half, not agent-invented work.
"Engagement" is deliberately in neither ticket: a standing, non-blocking
question is with the approver instead
(`inbox/2026-08-29-eng008-engagement-source-question.md`), since its
answer swings scope roughly an order of magnitude (a display field vs. a
paid third-party social-platform integration) and neither reading could
settle it from the text.

**2 transitions** (`intake → shaped → awaiting-scope`), well under the cap
of 4 — the next state needs the approver, so this pass stops here by
design. Consequence: approver-facing WIP 0/2 → 1/2; approval cap 0/3 → 2/3
(the G1 plus the standing question, the latter counted conservatively per
the header note above). Machine WIP unaffected.

Ran `departments/engineering/lib/eng-notify.sh raise` on both new `inbox/`
items — both logged the already-open `SLACK_WEBHOOK_URL unset` failure
(`traces/eng-notify-2026-08-29.log`), consistent with every gate raised on
this instance recently; `notified:` hand-stamped on both per established
practice. No dissent section on the G1 — `agents/critic/agent.md` still
doesn't exist (open proposal, `proposals.md` 2026-08-25 row), confirmed
absent again rather than assumed.

**Dead-end sweep:** out of scope for `intake`'s own narrower contract — not
run; `ENG-007` untouched. **Observations filed** (`observations.md`): the
confirmed-live influencer/campaign backend and its invitation-shaped
implication for item 2.

`chained: none` — `ENG-008` sits at `awaiting-scope`, owned by the
approver; the chaining guard never fires on a ticket waiting on a human.
Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-008-influencer-profile-admin-management.md`).

## 2026-08-29 — watch (schtasks): no ticket touched — resolved the standing events-dropped incident, deferred a sixth new business request

`watch` event pass, context `schtasks` — day 5/40 charged, drained immediately
behind the `watch (schtasks)` pass below (`pass end: watch (exit 0, 973s)` at
01:25:17 → `queue: collapsed 3 duplicate event(s)` → `draining queued event:
watch (schtasks)` at 01:25:33), the 5-minute poll cadence backlogging while
that long pass held the lock, already-confirmed-working design (2026-08-28
Windows-port observations), not a bug. Mode check clean (business-os `.env`
→ `MODE=` empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (no ticket to
scope to): exit 0, clean.

**Swept all three watched inboxes fresh rather than trusting the pass
below's own read.** `agents/eng-manager/inbox/` holds only `.gitkeep`.
`inbox/requests/` empty. `ENG-007` unchanged at `ready`, its own log still
ending in a valid `chained: ENG-007` — nothing broken to resume. The five
`agents/product-manager/inbox/` items the immediately preceding pass found
and correctly deferred are all still exactly that: unshaped, their dedicated
`intake` events still sitting in `traces/.pending` — re-confirmed rather than
assumed, since shaping any of them is `intake`'s job under this event's
narrower contract, not `watch`'s, same reasoning the last two passes already
established. **Four more landed mid-sweep, checked at the end of this pass
rather than assumed unchanged from the top of it** — catering/quote-generator
(08:32:55), AI SEO ROI tracking (08:39:27), brand-portal drip/mass campaigns
(08:37:36), and admin-panel autopilot/demo account for resellers (08:35:46),
all `via: control-center`, nine total now landed 08:14–08:39. Read all four
before leaving them: routine feature requests, no security or urgency
language in any. Left untouched for their own `intake` events, same as the
first five; not worth a further `observations.md` entry, it's the same
batch-arrival pattern already recorded there, just a larger batch than first
seen.

**`inbox/2026-08-28-eng-events-dropped.md` came back answered since the last
pass to read it** — `decision: approved`, `decided:
2026-08-29T08:27:47.038600+00:00`, a hand-edit, not a reply through
`lib/eng-notify.sh` (unsurprising: this item was never successfully notified
in the first place, the known `MODE`-collision bug, `proposals.md`
2026-08-25 row — the approver found it by reading `inbox/` directly).
Verbatim: "recheck the request and report back how to fix. fix if you can."
This is exactly the class of thing `watch`'s own contract exists to catch (a
gate item edited by hand), and unlike the five business requests above,
answering it doesn't require `intake`-style PRD shaping — it required an
investigation, which this pass did rather than deferring further (this item
had already sat unanswered through several earlier passes; deferring an
*answered* incident again would just repeat that).

**Investigated as far as this instance's architecture allows, and said so
plainly rather than guessing at a false confirmation.** `traces/` is
`.gitignore`d and host-local; this instance now runs on two hosts (the Mac
that raised this incident at 10:42:17 that morning, and Windows since
`168cb89`); this Windows checkout's own trace history starts at 23:33:59
that night. The actual failure log is on the Mac's disk and unreachable from
here — full detail and the reasoned-not-confirmed TCC/EPERM-over-spend-limit
hypothesis (from `observations.md`'s same-day entries, since the log itself
isn't available) on the item's own file. Filed a proposal
(`agents/eng-manager/proposals.md`, 2026-08-29 row) for the fixable half:
dropped-event items should carry their own failure excerpt instead of a
`traces/` pointer that only resolves on the host that failed. Moved to
`inbox/_handled/`; journaled in
`agents/eng-manager/config/decision-journal.md` as a new data point (an
incident response, not a ticket gate) rather than skipped for not fitting
the G1/G2/G3 shape.

**No ticket transition** — `ticket: unknown` on the incident, and nothing
else was new. WIP/approval-cap figures unchanged (machine 1/6, approver
0/2, approval cap 0/3) — the incident was never counted against the approval
cap (not a G1/G2/G3 or merge request), so resolving it doesn't move any of
the three numbers.

**Dead-end sweep:** `ENG-007` is the only ticket in flight; its chain is
valid, nothing to resume. **Notify sweep:** nothing raised this pass (the
proposal rides the weekly report, not `lib/eng-notify.sh`); nothing to
nudge; approval cap 0/3, not full — no stall. **Observations filed**
(`observations.md`): sharpened, not overturned, the prior pass's "all
non-emergency" read of the five-item batch — the admin-portal/agency-reseller
item is the approver's own words, "security issue," a cross-tenant data
exposure on a registered **L1** project, worth real severity when its
`intake` event shapes it rather than routine `P3`.

`chained: none` — no ticket was touched this pass (the incident carries no
ticket to advance), so there is no hop of its own to fire. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

## 2026-08-29 — watch (schtasks): ENG-007's G2 came back answered — Walletly is retiring, ticket advanced to ready and chained

`watch` event pass, context `schtasks` — a second, distinct fire from the one
immediately below, queued behind (and launched right after) an unrelated
`decision` pass that drained first and correctly no-op'd on this ticket's
already-processed G1. Mode check clean (business-os `.env` → `MODE=` empty;
instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`) and
whole-board: both exit 0, clean.

**Swept all three watched inboxes fresh; found `ENG-007`'s G2 answered**
since the previous pass raised it — `decision: approved`, verbatim
"Walletly is being retired/replaced," a hand-edit to
`inbox/2026-08-29-eng007-g2-walletly-conflict.md` rather than a reply through
`lib/eng-notify.sh`. Re-verified fresh rather than trusted (re-read the file,
checked `traces/.pending` for a live race) before acting. Picks option 1 of
the three the gate offered: the native loyalty sequence is Walletly's
intended replacement, proceed exactly as scoped — settling the boundary
question before ticket 3 (the points ledger) is ever filed.

**Processed here rather than left for a `decision` event already queued
behind this one for the same file** — the mirror image of this ticket's own
G1 a few minutes earlier, where `decision` drained first and `watch` found
nothing left to do; whichever event reaches a fact first does the real work,
per this instance's established practice. Moved the gate item to
`inbox/_handled/` with a processed footer; journaled in
`agents/eng-manager/config/decision-journal.md`. Architect's design doc left
unedited, same precedent `ENG-006`'s own G2 resolution set.

**1 transition** (`awaiting-decision → ready`), well under the cap of 4 —
`building` needs a different owning role (backend/database) actually writing
code, which is new implementation work and this pass's stop point by design.
Approver-facing WIP 1/2 → 0/2; approval cap 1/3 → 0/3 (now empty); machine WIP
0/6 → 1/6 — the first ticket into that range on this host.

**Dead-end sweep:** no other ticket in flight. **Not a clean sweep on the
inboxes, corrected here rather than left standing:** five new files landed in
`agents/product-manager/inbox/` mid-pass (`source: approver`, `via:
control-center`, received 08:14–08:22), after this pass's own initial sweep
had found that directory empty. Read all five before deciding not to act:
UX/functionality gaps on the admin panel (influencer board, brand
stage/health filtering), the FoodSwipe sales-funnel pipeline stages, the
brand portal (QR codes, media downloads, site-timing self-service), and
admin-portal readiness for agency/reseller users — none meets the P0 bar
(production down, data loss, active security incident), so none interrupts.
Left untouched for their own dedicated `intake` events, already visible
queued in `traces/.pending` for four of the five (the fifth landed after that
read and will get its own `watch` or `intake` fire) — shaping five requests'
worth of readback and G1s is `intake`'s own job per this event's narrower
contract, not this `watch` pass's. Observation filed. **Notify sweep:**
nothing to raise or nudge; cap just cleared to 0/3 — no stall.

`chained: ENG-007` — `ready` is agent-owned (eng-manager sequenced it; a
backend/database engineer builds next), not the approver, not blocked, not
terminal, not capped. Fired
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-007` before
exiting. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-007-per-restaurant-loyalty-configuration.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`)
and whole-board: both run clean.

## 2026-08-29 — watch (schtasks): ENG-007's G1 came back approved — designed, then a new G2 raised over an unplanned Walletly finding

`watch` event pass, context `schtasks`. Per the event's own narrower
contract, swept `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`,
and `inbox/` (including `inbox/requests/`) only, acting on whatever is new.
Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty, both fall through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`) and
whole-board: both exit 0, clean.

**Third attempt at tonight's fire** — two earlier launches for the same
event (pid `3199`, `1301`) went stale and were cleared by the trigger
before this one (pid `1067`) reached the lock; both died mid-investigation
with no write ever made, confirmed from their own output before trusting a
clean slate. `.hops-2026-08-29` reads `2`, nowhere near the daily ceiling.
Full detail on the ticket's own log.

**Found `ENG-007`'s G1 answered** (`decision: approved`,
`decided: 2026-08-29T07:15:41.687445+00:00`) — a hand-edit to the gate item
directly, not a reply through `lib/eng-notify.sh`. Moved to
`inbox/_handled/`, journaled. Also fixed the PRD's own stale
`status`/`decided` fields, left unset by an earlier crash-and-recover pass.

**No project worktree existed on this host** — `config/projects.md`'s "all
five worktrees already exist" was true only for the earlier Mac
verification. Created `aiorders-api`'s the same way `lib/eng-setup.sh`
would, then did real design work against the live repo (fresh `git fetch`,
read the now-actually-tracked migrations rather than inferring from
edge-function code). Full design: `restaurant_loyalty_configs`, open-ended
effective-dating, a per-restaurant-advisory-lock trigger closing the PRD's
own concurrent-write risk at the database, and an `admin-portal` handler
reusing the existing admin/sub-admin auth gate — complete and ready to
build. `agents/architect/designs/ENG-007-per-restaurant-loyalty-configuration.md`.

**Significant unplanned finding: a live, documented, actively-maintained
third-party loyalty vendor (Walletly) already runs in this codebase**,
unmentioned in the original request or either PRD. `ENG-007` itself carries
no risk from it, but ticket 3 (the points ledger) would start a second,
competing points system in production alongside it — expensive to unwind
after adoption, not before. Escalated via a new G2 rather than decided
unilaterally or silently carried forward:
`inbox/2026-08-29-eng007-g2-walletly-conflict.md`, recommending `ENG-007`
proceed now (no dependency on the answer) while ticket 3 waits for it.
Raised and notified (`lib/eng-notify.sh raise` logged
`SLACK_WEBHOOK_URL unset — cannot notify` — the plain-failure face of the
already-open channel-dispatch proposal, not a new bug); stamped `notified:`
by hand.

**2 transitions** (`awaiting-scope → designed → awaiting-decision`), well
under the cap of 4 — the next state needs the approver. Approver-facing WIP
and approval cap both net unchanged at 1/2 and 1/3 (this ticket's G1 closed,
its G2 opened). Machine WIP unaffected (0/6).

**Dead-end sweep:** no other ticket in flight; nothing else new across all
three inboxes. **Notify sweep:** this pass's own G2 raised and stamped;
nothing else to nudge; cap 1/3, not full — no stall. **Observations filed**
(`observations.md`): the missing Windows worktree, the now-tracked
migration history correcting `ENG-006`'s design doc, the Walletly
discovery, and today's plainer `eng-notify.sh` failure signature — all
corroborating existing gaps, none new. **Correction filed**
(`config/projects.md`): the worktree-existence claim is host-specific.

`chained: none` — `awaiting-decision` (G2), waiting on the approver. Full
detail on the ticket's own log
(`agents/eng-manager/board/ENG-007-per-restaurant-loyalty-configuration.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-007`) and whole-board: both run clean.

## 2026-08-28 — scheduled (manualtest): safety-net sweep — board fully terminal except ENG-007, nothing to act on; first pass run on Windows

`scheduled` event pass, context `manualtest` — the first fire this instance
has run through the Windows port (`168cb89`, committed 23:34:44 by the human
operator, one minute before this pass's own drain). `traces/eng-loop-2026-08-28.log`:
a `watch (schtasks)` fire arrived first at 23:33:59 while `MODE=quiet`, and
the trigger's pre-lock pause switch (`eng-trigger.sh`, "the pause switch")
queued it without launching — the quiet-mode gate firing correctly on this
host for the first time. This pass's own fire reached the lock at 23:34:36
once `MODE` had cleared, collapsed 3 duplicate queued event(s), and drained
`scheduled (manualtest)` — launched 23:34:53 via
`/c/Users/jerryai/AppData/Local/Microsoft/WinGet/Links/claude` (the
`$ENG_CLAUDE_BIN`/PATH fallback the same commit added, resolving correctly).
Mode check re-confirmed clean in-session (business-os `.env` → `MODE=`
empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Business intake:** `agents/product-manager/inbox/` and `inbox/requests/`
hold only `.gitkeep`. Nothing to shape.

**Technical intake:** `agents/eng-manager/inbox/` holds only `.gitkeep`.
Nothing to batch into `proposals.md`.

**Gate returns:** `inbox/` holds the same two live items as the preceding
pass — `2026-08-28-eng007-g1-scope.md` (`notified: 22:15:21`,
`decision:`/`decided:` both still empty, ~1h20m old, well under the 24h
nudge threshold) and `2026-08-28-eng-events-dropped.md` (still no
`decision:`, still non-P0, still never successfully notified — the known
`eng-notify.sh` `MODE`-collision bug, `proposals.md` 2026-08-25 row).
Nothing new, nothing to act on.

**Merge detection:** no ticket is `blocked` on an L1 PR — `ENG-007` sits at
`awaiting-scope`; all six others terminal. Nothing to check.

**Dispatch:** To-do is `ENG-007` alone, and it's waiting on its own G1
answer, not free to dispatch regardless of slot. No other ticket in flight.
Machine WIP 0/6, unaffected.

**Dead-end sweep:** `ENG-007`'s own log ends `chained: none`, owner
`approver` — a valid human-wait. All six terminal tickets' logs already end
`chained: none` in accounted-for terminal states (confirmed on the two
immediately preceding passes; unchanged since). No ticket without an owner.
No broken chain.

**Notify sweep:** nothing raised this pass. Nothing to nudge (`ENG-007`'s G1
well under 24h; the events-dropped item deliberately not retried, per
established precedent — a corroborated open proposal, not this pass's
bug to fix). Approval cap 1/3, not full — no stall.

**Observations filed** (`observations.md`) — this is the first confirmed
end-to-end run of the Windows scheduler port: the pre-lock quiet-mode queue
gate, duplicate-event collapse, and claude-binary resolution all worked as
designed on this host. Also noted: further `watch (schtasks)` fires queued
behind this pass while it held the lock (23:35:40, 23:42:05 so far — roughly
the documented 5-minute poll cadence, not a busy loop), plus one `scheduled
(schtasks)` fire; left for the next pass to drain, per design.

**Board:** rolled the oldest dated entry (`scheduled (launchd): safety-net
sweep`, 20:30:05) to `_index-archive.md` per the keep-three rule — this
entry is the fourth.

No ticket state changed, no gate item was written. `chained: none` — this
pass advanced no ticket, so there is no hop of its own to fire. All
WIP/approval-cap figures unchanged (machine 0/6, approver 1/2, approval cap
1/3). Post-pass `departments/engineering/lib/eng-gate-check.sh`, whole-board:
exit 0, clean.

## 2026-08-28 — watch: filed ENG-007, item 2 of the approved loyalty sequence — G1 raised

`watch` event pass, context `launchd`, attempt 2/2 of this fire — attempt 1
(21:33–21:38) reached the same request and died mid-flight on the account's
monthly spend limit right after spawning the blind architect-reading
subagent (`traces/eng-loop-2026-08-28.log`: `pass end: watch (exit 1,
352s)`, charged not refunded — 352s clears the 60s never-started
threshold). No artifact from attempt 1 survived on disk or as a live
subagent, so this pass redid the work from scratch. Mode check clean
(business-os `.env` → `MODE=active`).

**Swept all three watched inboxes fresh**, per the `watch` event's own
contract. `agents/product-manager/inbox/` and `agents/eng-manager/inbox/`
held only `.gitkeep` plus already-`_handled/` items; `inbox/` held one
already-notified, non-P0 item (`2026-08-28-eng-events-dropped.md`,
untouched, out of scope). `inbox/requests/` held exactly one new file,
`2026-08-28-eng006-sequence-item-2.md` — the approver continuing the
`ENG-006` loyalty sequence by hand, since `skills/acceptance-check/SKILL.md`
step 6b (the automation meant to do this the moment a sequenced ticket
verifies) didn't exist yet when `ENG-006` itself verified. A queued `intake`
event for the same file sat behind this pass in `traces/.pending` —
matches this instance's well-documented duplicate-queued-event race; that
event will very likely no-op when it drains next, since this pass processed
the file fully.

**Ran the full request-readback** (this PM's reading plus a blind architect
subagent, neither seeing the other) and found no material divergence — both
converged on a per-restaurant, effective-dated config table (two earn
rates, one redemption value), no dependency on `ENG-006`'s identity work.
Full comparison on the ticket's own log and PRD. Sized `S`. `size: L`'s G1
requirement doesn't apply here, but full lane always requires G1 regardless
of size, and caps were fully free (0/2, 0/3) before raising. Wrote and
notified `inbox/2026-08-28-eng007-g1-scope.md`. Filed the intake request to
`inbox/_handled/`.

**1 transition-worthy stop.** `ENG-007`: `intake → shaped → awaiting-scope`
in one pass, `owner` moving `product-manager → approver`. Approver-facing
WIP 0 → 1/2; approval cap 0 → 1/3; machine WIP unaffected (0/6).

**Dead-end sweep:** no other ticket was in flight before this pass — nothing
else to check. **Notify sweep:** this pass's own gate item raised and
stamped; nothing else to nudge; cap 1/3, not full — no stall. **Observation
filed** (`observations.md`) — a second monthly-spend-limit death today,
worth watching as a pattern.

`chained: none` — `ENG-007` sits at `awaiting-scope`, owned by the
approver; the chaining guard never fires on a ticket waiting on a human.
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-007`) and whole-board: both run clean.

## 2026-08-28 — watch (schtasks): swept all three inboxes, nothing new — first confirmed watch drain on the Windows port

`watch` event pass, context `schtasks`. Per the event's own narrower
contract, swept `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`,
and `inbox/` (including `inbox/requests/`) only, acting on whatever is new —
not a board-wide sweep. `traces/eng-loop-2026-08-28.log`: drained
immediately behind the `scheduled (manualtest)` pass directly below (`pass
end: scheduled (exit 0, 554s)` at 23:44:08 → collapsed 2 duplicate event(s)
→ `draining queued event: watch (schtasks)` → `pass start: watch (schtasks)`
23:44:24, launched 23:44:38). Mode check clean (business-os `.env` →
`MODE=` empty; instance `config/config.yaml` → `mode:` empty, both fall
through). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board (this event names no ticket to scope to): exit 0, clean.

**Swept all three inboxes fresh; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
`.gitkeep` (plus the former's already-`_handled/` entry); `inbox/requests/`
is empty. `inbox/` holds exactly the same two live items the immediately
preceding `scheduled (manualtest)` pass already read fresh and accounted
for — read directly again rather than trusted from that account:
`2026-08-28-eng007-g1-scope.md` (`notified: 22:15:21`, `decision:`/
`decided:` both still empty, well under the 24h nudge threshold) and
`2026-08-28-eng-events-dropped.md` (still no `decision:`, still non-P0,
still never successfully notified — the known `eng-notify.sh`
`MODE`-collision bug, `proposals.md` 2026-08-25 row). Nothing new anywhere.

**Merge detection:** no ticket is `blocked` on an L1 PR — `ENG-007` sits at
`awaiting-scope`; nothing else in flight. Nothing to check.

**Dispatch:** To-do is `ENG-007` alone, and it's waiting on its own G1
answer, not free to dispatch regardless of slot. Machine WIP 0/6,
unaffected.

**Dead-end sweep:** `ENG-007`'s own log ends `chained: none`, owner
`approver` — a valid human-wait, unchanged since the preceding pass. No
ticket without an owner. No broken chain.

**Notify sweep:** nothing raised this pass. Nothing to nudge (`ENG-007`'s G1
well under 24h; the events-dropped item deliberately not retried, per
established precedent). Approval cap 1/3, not full — no stall.

**Observation filed** (`observations.md`) — this is the first confirmed
end-to-end completion of a `watch (schtasks)` fire on the Windows port
(the immediately preceding pass confirmed `scheduled (manualtest)`; this is
the first time the 5-minute poll path itself has been seen through to a
clean finish). `traces/.pending` still holds one `scheduled schtasks` and
one `watch schtasks` fire, queued behind this pass while it ran — left for
the next pass to drain, per design.

**Board:** rolled the oldest dated entry (`continue ENG-006: fired
externally...`) to `_index-archive.md` per the keep-three rule — this entry
is the fourth.

No ticket state changed, no gate item was written. `chained: none` — this
pass advanced no ticket, so there is no hop of its own to fire. All
WIP/approval-cap figures unchanged (machine 0/6, approver 1/2, approval cap
1/3). Post-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board: exit 0, clean.

## 2026-08-28 — continue ENG-006: fired externally against an already-terminal ticket — no-op

`continue` event pass, context `ENG-006`. Per the event's own contract
(resume the named ticket from its current state), scoped to this ticket
only — no board-wide sweep. Mode check clean (business-os `.env` →
`MODE=active`; instance `config/config.yaml` → `mode:` empty, falls
through). Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-006`) and whole-board: both exit 0, clean.

**Nothing to resume.** `ENG-006` has been `state: verified` — terminal —
since the `decision` pass at 20:12:38, confirmed independently twice more
since (the `watch` and `scheduled` passes immediately below). Re-confirmed
fresh rather than trusted from the board's own account: the ticket's own
frontmatter and log, this file's header/In-flight table, and
`decision-journal.md` (all three of its gates — G1, G2, L1 merge — already
journaled) all agree. `traces/.pending` empty; all three watched inboxes
hold only `.gitkeep` and the already-notified, non-P0
`2026-08-28-eng-events-dropped.md`. Nothing anywhere for a machine to act on.

**This fire does not fit the instance's well-documented duplicate-queued-event
race** (`observations.md`, eleven-plus prior rows) — that pattern is always
two events the loop itself legitimately queued for the same underlying
change, racing each other. This one doesn't: `traces/eng-loop-2026-08-28.log`
shows no `continue — queued as pending` line and no pass since the
`ready-to-ship → blocked` transition (14:38:21, its own chain already
consumed) ever recording `chained: ENG-006` — the `decision`, `watch`, and
`scheduled` passes since all correctly logged `chained: none`. This fire
lands at 21:02:49, 27 minutes after the `scheduled` pass's own `pass end`
line, with nothing queued between them — meaning it reached the lock and
drained its own freshly-appended line, not an older one left waiting. That
shape means the fire itself came from outside the loop's own chain
mechanism — a direct invocation of `eng-trigger.sh continue ENG-006` — not
from two internally-queued events racing. Filed as its own,
differently-shaped observation rather than folded into the existing race
count.

**A concrete, plausible source surfaced mid-pass, while re-checking the
working tree.** Commit `3c3dcd0` ("ENG-006: verify against production —
migration and function confirmed deployed") landed at
2026-08-28T21:09:07-07:00, authored by Harsimran — inside this pass's own
window. Its message: the approver ran `supabase db push` and `supabase
functions deploy platform-customer-auth` directly against production,
confirmed by CLI output, and updated the release record's `environment`/
`health_check` frontmatter accordingly — all "outside this department's own
L1 workflow, which still only opens PRs." That's a plausible source for an
external trigger fire landing on this exact ticket in this exact window,
though nothing ties the commit to the fire directly (no log line names a
cause), so it's recorded as circumstantial, not confirmed. Checking that
commit's diff also surfaced a second thing, unrelated to the fire itself:
its frontmatter update to `agents/devops/releases/2026-08-28-aiorders-api-ENG-006.md`
wasn't matched by an update to that file's own prose body, which still reads
the opposite (`## Deploy`/`## Health note`: "not established that a live
Supabase deploy has happened yet"). Not fixed here — see the observation
below for why.

**0 transitions.** No cap affected — machine WIP 0/6, approver WIP 0/2,
approval cap 0/3, all unchanged; `ENG-006` sits outside every counted range.

**Dead-end sweep (scoped to this event):** `ENG-006`'s own log already ended
in a valid, terminal, accounted-for state before this pass started, and this
pass added one line confirming that rather than reopening it. No other
ticket is in flight to check.

**Notify sweep:** nothing to raise, nothing to nudge. Approval cap 0/3 — no
stall.

**Observation filed** (`observations.md`) — this fire's shape, distinct from
the duplicate-event race.

No ticket state changed, no gate item was written. `chained: none` —
`verified` is terminal; firing `continue ENG-006` again would just repeat
this same no-op. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-006`) and whole-board: both exit 0, clean.

## 2026-08-28 — scheduled (launchd): safety-net sweep — board fully terminal, nothing to act on

`scheduled` event pass, context `launchd`, the four-times-daily safety net
(20:30 firing). `traces/eng-loop-2026-08-28.log`: queued behind the `watch`
pass that ended at 20:24:32 (exit 0, 714s); this fire drained at 20:30:05 —
the scheduled calendar time itself, not an immediate queue-drain artifact.
Mode check clean (business-os `.env` → `MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (this event
names no ticket to scope to): exit 0, clean — run fresh myself, not taken on
the preceding passes' own recorded claim.

**Found the working tree already carrying the preceding `decision
ENG-006` + `watch` passes' edits, uncommitted.** Verified rather than
trusted before relying on any of it: independently re-ran the whole-board
gate-check (above); independently grepped every board file's own
`state`/`owner`/`blocked_on` frontmatter directly rather than reading the
index's summary (`ENG-001`, `ENG-002`, `ENG-004`, `ENG-005`, `ENG-006` all
`state: verified`; `ENG-003` `state: dropped`; none `blocked_on` anything);
independently grepped every ticket log's last `chained:` line (all six read
`chained: none`) — no broken chain anywhere on the board. `lib/eng-env.sh:14`
confirms committing this bookkeeping repo is "a deliberate git commit
against business-os, not something a run does," matching this instance's
already-established convention (the immediately preceding passes' own
entries) — left the tree uncommitted, did not commit on this pass's behalf.

**Business intake:** `agents/product-manager/inbox/` and `inbox/requests/`
hold only `.gitkeep`. Nothing to shape.

**Technical intake:** `agents/eng-manager/inbox/` holds only `.gitkeep`.
Nothing to batch into `proposals.md`.

**Gate returns:** `inbox/` holds exactly one live item,
`2026-08-28-eng-events-dropped.md` — read fresh: still no `decision:` field,
still not P0, still no `notified:` stamp (the earlier raise attempt failed on
the already-filed `MODE`-collision bug, not compelling a retry for a non-P0
item). Nothing new, nothing to act on. `2026-08-28-eng006-merge-request.md`
is no longer live — already moved to `_handled/` by the preceding `decision`
pass.

**Merge detection:** no ticket is `blocked` on an L1 PR — all six terminal
(confirmed above). Nothing to check.

**Dispatch:** To-do (`intake`/`shaped`/`awaiting-scope`) is empty; no free
slot to fill regardless (machine WIP 0/6).

**Dead-end sweep:** all six ticket logs end in a valid, accounted-for
terminal state with `chained: none` on record (confirmed above). No ticket
without an owner. No broken chain.

**Notify sweep:** nothing to raise, nothing to nudge (one nudge is the limit
and the events-dropped item never even got a first successful notify —
out of this pass's scope, already a corroborated open proposal), no stall
(approval cap 0/3, not full).

**Observations/exceptions/journal:** nothing new — no gate answered this
pass, no exception request open on any (terminal) ticket log.

No ticket was touched, no ticket state changed, no gate item was written.
`chained: none` — this pass advanced no ticket, so there is no hop of its
own to fire. All WIP/approval-cap figures unchanged (0/6, 0/2, 0/3). Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

## 2026-08-28 — watch: swept all three inboxes, nothing new — board already fully terminal

`watch` event pass, context `launchd`. Per the event's own narrower contract,
swept `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`, and
`inbox/` (including `inbox/requests/`) only — not a board-wide sweep. Mode
check clean (business-os `.env` → `MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (this event
names no ticket to scope to): exit 0, clean.

**Drained immediately behind the `decision ENG-006` pass directly below, in
the same lock hold, not a separate concurrent invocation.**
`traces/eng-loop-2026-08-28.log`: that pass ended at 20:12:38 (785s, exit
0), the queue then collapsed 2 duplicate event(s), and this `watch` fire was
drained next and launched in the same breath. Verified rather than assumed:
process ancestry (`traces/.loop.lock`, pid 33561, `eng-trigger.sh decision
...`) traces to this session's own `claude` process via `lib/run-claude.sh`
— the same wrapper invocation working through its queue, not a second live
pass touching the same files.

**Swept all three inboxes fresh; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
`.gitkeep` (plus the former's already-`_handled/` entries); `inbox/requests/`
is empty. `inbox/` holds exactly one live item,
`2026-08-28-eng-events-dropped.md` — read directly: still no `decision:`
field, still not P0, already notified once (10:42:17), and already fully
accounted for both in `ENG-006`'s own ticket log and the immediately
preceding `decision` pass's addendum. `2026-08-28-eng006-merge-request.md`
is no longer a live inbox item at all — that same preceding pass closed it
out and moved it to `_handled/`. Nothing new anywhere.

**Board already fully terminal by the time this pass ran** — confirmed
against the header the preceding pass already updated, not re-derived:
`ENG-001`–`ENG-006` all terminal (`verified` ×5, `dropped` ×1); machine WIP
0/6, approver-facing WIP 0/2, approval cap 0/3. No ticket to dispatch, no
free slot to fill from an empty To-do regardless.

**Dead-end sweep:** nothing beyond the inboxes to check — no ticket in
flight, so no chain to verify.

**Notify sweep:** nothing to raise, nothing to nudge, approval cap 0/3 —
no stall.

**Nothing to journal** — no gate was answered this pass.

No ticket was touched, no ticket state changed, no gate item was written.
`chained: none` — this pass advanced no ticket, so there is no hop of its
own to fire. All WIP/approval-cap figures unchanged. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

## 2026-08-28 — decision ENG-006: merge-request gate closed, control-center jump reconciled — shipped → verified

`decision` event pass, context `inbox/2026-08-28-eng006-merge-request.md`.
Narrow scope per the event contract (act on the answered gate item, advance
only this ticket). Mode check clean (business-os `.env` → `MODE=active`).
Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-006`)
and whole-board: both exit 0, clean.

**Found the ticket already past the gate item it was meant to act on.** The
tracked item carried `decision: approved` (`decided: 2026-08-29T02:59:33Z`,
text "approved"), but `ENG-006`'s own `state:` was already `shipped` — a
"control center" dashboard action had advanced `blocked → shipped` ahead of
any build-loop pass (the one-liner immediately above this entry, in the
ticket's own log). Second occurrence of the gap `ENG-002` first hit
(`proposals.md`, 2026-08-26 row), this time hybrid: unlike `ENG-002` (no
reply at all, item left open), the tracked item *was* answered — just
minutes after the merge rather than instead of it. Addendum filed in
`observations.md` rather than a new proposal row; journaled in
`decision-journal.md`.

**Neither signal trusted on its own text.** Re-ran the loop's own
merge-detection check from scratch in the department's own worktree: `git
fetch` + `git merge-base --is-ancestor origin/loyalty-system origin/main` →
MERGED, `40d7c36` (PR #2's merge commit) directly on `c3ab50c` with no
intervening commits; cross-checked via `gh pr view 2` → `MERGED`,
`2026-08-29T02:57:05Z`, ~2m28s before the gate item's `decided:` stamp — same
"merge, then record" shape as `ENG-005`. The control center's `shipped` call
checks out; not redone.

**Closed out `shipped → verified` in one hop.** Acted as devops: confirmed
the migration and all 7 edge-function files present on `origin/main`
(branch-to-main diff empty, so the already-passing 27/27 Deno suite still
holds — not re-run for zero new information); confirmed no CI/CD exists;
confirmed this worktree has no linked Supabase session
(`supabase migration list --linked` → "Cannot find project ref"), so
`health_check: not checked` recorded honestly rather than inferred. Release
record: `agents/devops/releases/2026-08-28-aiorders-api-ENG-006.md`. Acted as
product-manager: AC3/4/7 confirmed directly against the merged tree
(unit-test-covered linking/validation logic, no live OTP needed); AC1/2/5/6
remain **not verified live**, unchanged from the already-named, already
approver-seen gap (Supabase phone-auth + SMS vendor not yet configured) —
carried forward, not new, not blocking, same standard applied at every gate
on this ticket. PRD `status: designed → verified`. Full reasoning on the
ticket's own log.

**1 transition this pass** (`shipped → verified`), well under the cap of 4.
Approver-facing WIP 1 → 0; approval cap 1/3 → 0/3 — `ENG-006` was the only
item on either. `machine_wip` unaffected (0/6).

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for terminal state. No other ticket in flight.

**Notify sweep:** nothing to raise (`verified` raises no gate item); nothing
to nudge (item now closed, not open). Approval cap 0/3 — no stall.

`chained: none` — `verified` is terminal. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-28 — scheduled (launchd): safety-net sweep — merge check confirms PR #2 still open

`scheduled` event pass, context `launchd`, the four-times-daily safety net.
Queued directly behind, and drained immediately after, the `watch` pass that
finished at 15:37:45 (`traces/eng-loop-2026-08-28.log`) — not the
decision/watch race documented on this instance: no hand-edited gate item is
in play here, and the `watch` pass's own narrower contract explicitly left
merge detection, dispatch, and the full dead-end sweep out of scope. Those
are exactly this event's job, so this is the late-safety-net case, not the
race — and unlike that case's usual "found nothing" shape, this pass had one
real check of its own to run. Mode check clean (`MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (this event
names no ticket to scope to): exit 0, clean.

**Business intake:** `agents/product-manager/inbox/` and `inbox/requests/`
hold only `.gitkeep` (plus the former's `_handled/`). Nothing to shape.

**Technical intake:** `agents/eng-manager/inbox/` holds only `.gitkeep`.
Nothing to batch into `proposals.md`.

**Gate returns:** `inbox/` holds the same two live items the immediately
preceding `watch` pass already read fresh and accounted for —
`2026-08-28-eng006-merge-request.md` (still the unfilled "Filled in by the
approver." placeholder, no `decision:`) and `2026-08-28-eng-events-dropped.md`
(no `decision:`, not P0). Re-read both directly rather than trusted from the
board's own account: unchanged, neither new. Nothing to act on.

**Merge detection — the one check this event contributes that the prior pass
didn't.** `ENG-006` is `blocked` on its L1 PR
(https://github.com/harsimranwalia/aiorders-api/pull/2). In the worktree
(`~/Documents/projects/_eng/aiorders-api`, clean): `git fetch origin`, then
`git merge-base --is-ancestor c3ab50c origin/main` — **not an ancestor**;
`origin/main` is still at `5b3bac2`. Cross-checked independently via `gh pr
view 2 --json state,mergedAt`: `state: OPEN`, `mergedAt: null`. Both routes
agree: **not merged.** `ENG-006` stays `blocked`, `blocked_on: approver`,
unchanged — PR opened today (`notified: 2026-08-28T21:42:08`, well under an
hour before this pass), nowhere near the 3-day resurface threshold.

**Dispatch:** nothing to start — `ENG-006` is the only in-flight ticket and
it's `blocked`, not in To-do; no free slot to fill regardless.

**Dead-end sweep:** `ENG-006`'s own ticket log ends validly, `chained: none`
with the blocked-on-approver reason, matching the board. No ticket lacks an
owner; no broken chain.

**Notify sweep:** nothing to raise (no new gate item), nothing to nudge (the
merge-request item is under an hour old), no stall (approval cap 1/3, not
full).

**Observations/exceptions/journal:** none. No gate was answered this pass,
and the two open `inbox/` items plus the `eng_stamp()` fingerprint bug were
already fully accounted for by the `watch` pass that drained immediately
before this one — nothing new to add on top of that.

`chained: none` — `ENG-006` stays `blocked`, `blocked_on: approver`; nothing
for a machine to do until the approver merges the PR or answers the gate
item directly. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board: exit 0, clean.

## 2026-08-28 — watch: swept all three inboxes, nothing new; found the deeper cause of the watch-fingerprint bug

`watch` event pass, context `launchd`. Per the event's own narrower contract,
swept `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`, and
`inbox/` (including `inbox/requests/`) only, acting on whatever is new — not
a board-wide sweep. Mode check clean (business-os `.env` → `MODE=active`).
Pre-pass `departments/engineering/lib/eng-gate-check.sh`, whole-board (this
event names no ticket to scope to): exit 0, clean.

**Swept all three inboxes fresh; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
`.gitkeep` (plus the former's already-`_handled/` entry); `inbox/requests/`
is empty. `inbox/` holds exactly two live items, both read directly rather
than trusted from the board's own summary:
`2026-08-28-eng006-merge-request.md` (`ENG-006`'s own L1 merge-request gate,
raised and notified by the immediately preceding `continue ENG-006` pass at
`21:42:08`) still carries the unfilled "Filled in by the approver."
placeholder — no decision yet; and `2026-08-28-eng-events-dropped.md` (the
day's dropped-event incident notice) still carries no `decision:` field and
is still not P0. Both predate this fire and are already accounted for on the
board's own log — nothing new in any of the three inboxes.

**Chased down the incident notice's "already notified" claim rather than
taking it at face value.** `traces/eng-notify-2026-08-28.log` shows the
10:42:17 raise attempt for that file returned `FAILED: active ... — item
still in inbox and in the tab` — the same already-filed `MODE`-collision bug
every other gate item on this instance has hit (`sent: active`, not `sent:
raise`), not a successful notification. The file's frontmatter carries no
`notified:` field, consistent with the failure. Not re-raised here: it's an
already-corroborated, already-proposed bug in shared department code
(`lib/eng-notify.sh`), out of a `watch` pass's narrow scope to fix, and the
item isn't P0, so nothing compels a retry — it stays visible in `inbox/`
regardless, per the constitution's own design.

**Found a deeper cause underneath the open `.watch-seen` proposal
(`proposals.md`, 2026-08-26 row) rather than just logging another
corroboration of its already-known symptom.** Read `watch_fingerprint()`
(`lib/eng-trigger.sh:366`) and the `eng_stamp()` helper it calls per file
(`lib/eng-env.sh:185`): `eng_stamp()` is `date '+%Y-%m-%dT%H:%M:%S%z'` and
ignores its `$1` argument completely, returning wall-clock time rather than
anything derived from the file it's supposedly stamping (contrast
`eng_mtime()` immediately above it, which correctly `stat`s `$1`). Verified
empirically, not just read: called the real function twice, 2s apart,
against these same two unchanged files — two different SHA-1s
(`cba0b32b...` vs `55b6fbd9...`). So the open proposal's own fix (commit the
fingerprint after every event type, not only `watch`) would not close this —
any two fingerprint computations of a genuinely unchanged, non-empty inbox
more than about a second apart already differ, because the hash is a
function of call-time and file *count*, never file identity. Filed as an
addendum in `observations.md` (2026-08-28, last row) pointing back at the
open proposal rather than as a new row — same shape the 2026-08-26
self-modifying-pass addendum used for the same proposal.

**Merge detection, dispatch, and the full dead-end sweep are out of scope
for this event** — no ticket sits in a startable state regardless; `ENG-006`
is the only in-flight ticket, still `blocked`/`blocked_on: approver` on its
L1 PR. Its own ticket log already ends in a valid, accounted-for state with
`chained: none` from the pass that opened the PR — spot-checked directly
against the file rather than trusted from the board's account: matches.

**Notify sweep:** nothing new to raise. `ENG-006`'s merge-request item is
well under 24h old (raised `21:42:08` today). The incident notice has no
`notified:` to measure a nudge threshold against, and isn't P0 — left as is,
per this pass's own instruction not to surface anything but a P0.

**Nothing to journal** — no gate was answered this pass.

No ticket was touched, no ticket state changed, no gate item was written.
`chained: none` — this pass advanced no ticket, so there is no hop of its
own to fire; `ENG-006` stays `blocked`, `blocked_on: approver`, exactly as
the pass before this one left it. All WIP/approval-cap figures in the header
are unchanged (machine WIP 0/6, approver-facing WIP 1/2, approval cap 1/3).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit
0, clean.

## 2026-08-28 — continue ENG-006: L1 PR opened, merge-request gate raised — ready-to-ship → blocked

`continue ENG-006` event pass, the dedicated session the preceding pass
chained specifically to open the L1 PR. Narrow scope per the event contract
(resume this ticket from its current state; no board-wide sweep). Mode check
clean (`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped and whole-board: both exit 0, clean.

**Release window re-checked fresh**, as the preceding pass explicitly asked
the session that opens the PR to do: Friday 2026-08-28, 14:40 PDT (before the
15:00 cutoff), `MODE=active`, no `ENG_RELEASE_FREEZE`. Inside the window.
Checked for an already-opened PR first (`gh pr list --head loyalty-system`:
empty) and confirmed the worktree (`_eng/aiorders-api`, clean, `loyalty-system`
at `c3ab50c`, not yet merged) before creating one, same discipline `ENG-005`
used at this identical boundary.

**Opened the PR**: https://github.com/harsimranwalia/aiorders-api/pull/2.
Wrote the L1 merge-request item (`inbox/2026-08-28-eng006-merge-request.md`,
`gate: merge`) carrying the PR link and all four gate verdicts (review,
quality, security, migration) by file reference, plus the three
already-designed-around items (SMS/phone-provider config, consent capture,
phone-recycling mitigation) so the approver sees them at the merge decision
itself. Ran `lib/eng-notify.sh raise` — reproduced the already-filed `MODE`-
collision bug (`sent: active`, not `sent: raise`) — corroborating, not new.
Stamped `notified: 2026-08-28T21:42:08` by hand. State → `blocked`,
`blocked_on: approver`, `blocked_from: ready-to-ship`, owner `devops →
approver`, `links.pr` set — same design `ENG-002`/`ENG-005` used at this
boundary.

**1 transition this pass** (`ready-to-ship → blocked`), well under the cap of
4. `machine_wip` 1/6 → 0/6 (`blocked` sits outside the counted range).
Approver-facing WIP 0 → 1; approval cap 0/3 → 1/3.

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for state with the chain record below. No other ticket in
flight.

**Notify sweep:** this pass's own gate item raised and stamped above. Nothing
to nudge (brand new). Approval cap 1/3, not full — no stall.

`chained: none` — `blocked`, `blocked_on: approver`. This is the human gate
the whole hop was driving toward; nothing left for a machine to do until the
approver merges the PR or replies to the gate item. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-28 — continue ENG-006: building through ready-to-ship, recovered from a timeout

`continue` event pass, context `ENG-006`, attempt 2/2 after the first
dispatch timed out at 1800s. Narrow scope per the event contract (resume
this ticket from its current state; no board-wide sweep). Mode check clean
(`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped and whole-board: both exit 0, clean.

**Recovered an unrecorded build** (same shape as `ENG-002`/`ENG-005`'s own
precedent): the dead first attempt had already branched `loyalty-system` in
`_eng/aiorders-api`, written and DB-verified the migration, written the
`platform-customer-auth` edge function plus tests, and fixed a real bug in
its own phone validator — all uncommitted when it hit the timeout mid
re-verification. Ruled out a live concurrent session before trusting any of
it (lock pid, running `claude` pid, and `.pass-out.*` all traced to this
exact invocation). Independently re-verified rather than trusted: deno
test/check/lint re-run fresh via Docker (deno isn't installed on this host)
— 27/27 tests, clean check, clean lint. Full detail on the ticket's own log.

**Ran the full arc in one session, same stopping point as `ENG-005`'s
precedent:** committed and pushed (`building` done) → code review + quality
combined hop (`agents/principal-engineer/reviews/ENG-006.md`,
`agents/qa/test-plans/ENG-006.md`, both **pass**) → security
(`agents/security/reviews/ENG-006.md`, **pass**) → `ready-to-ship` (devops:
migration gate already cleared, $0/month cost, rollback tested, no live
caller yet so zero production blast radius). 4 transitions, at the cap —
stopped before opening the PR (`blocked`), deliberately, same as `ENG-005`.

**Three pre-existing, already-designed-around items carried forward rather
than re-derived by the next reader:** Supabase phone-provider/SMS-vendor
configuration still open (this ticket's OTP-dependent ACs are unreachable
until it lands), consent capture for the new cross-restaurant correlation
not yet wired (approver's/counsel's call per the design), and the
phone-recycling mitigation deliberately deferred as a build-time refinement.
None block this verdict — all three were named in the design doc before
this code was written, not discovered here. Full detail, including the
independent-verification narrative and the per-gate reasoning, is on the
ticket's own log (`agents/eng-manager/board/ENG-006-unified-customer-identity.md`).

**Consequence:** `machine_wip` stays 1/6 — same ticket, later state in the
same counted range. Approver-facing WIP and approval cap both unaffected —
no gate raised this pass (the merge request, which will need the approver,
is the next hop's work).

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for state with the chain record below.

**Notify sweep:** nothing raised this pass. Approval cap 0/3, not full — no
stall.

**Observations/exceptions:** none filed — the recovered-unrecorded-build
shape corroborates `ENG-002`/`ENG-005`'s precedent rather than adding a new
one.

`chained: ENG-006` — `ready-to-ship` is devops-owned, not the approver, not
blocked, not terminal. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-006` before
exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-006`) and whole-board: both exit 0, clean.

## 2026-08-28 — scheduled: ENG-006's G2 caught mid-sweep — awaiting-decision → ready

`scheduled` event pass, context `launchd` — the four-times-daily safety net.
Mode check clean (`MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Full board swept, not just the one ticket.** `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/`, and `inbox/requests/` all empty (bar
`.gitkeep`/already-`_handled/` entries) — no PM or EM intake waiting. No
ticket sits `blocked` on an L1 PR — merge detection had nothing to check.
`ENG-006` was the only in-flight ticket, and its `inbox/` gate item
(`2026-08-28-eng006-g2-oneway-door.md`) had already been answered
(`decided: 2026-08-28T20:09:06`) by the time this pass read it — caught here
precisely because this is what a scheduled sweep is for: neither `watch`
(unwired on this instance) nor a tracked-channel reply (this approver
hand-edits gate files directly, every time so far) had a live path to act on
it sooner. `traces/.pending` held a `decision` event for the same file
queued behind this pass — the already-documented duplicate-event race
(`observations.md`), not new; that queued fire will find the item already in
`_handled/` and no-op.

**Acted on the answer as eng-manager (G2 is the EM's gate).** Approved, with
the approver's own reversibility criterion restated in full rather than a
bare yes — read in full on `inbox/_handled/2026-08-28-eng006-g2-oneway-door.md`
and the ticket's own log. Confirms rather than changes the design's approach:
legacy `customers` stays untouched, the two flows run side by side, and a
unified cross-restaurant order view is explicitly later-ticket scope. Ticket
advanced `awaiting-decision → ready` — one transition, well under the cap of
4, stopping there because `building` is new implementation work and this
event's dispatch step leaves that for a fresh chained session by design.
Journaled in `agents/eng-manager/config/decision-journal.md`. Full detail,
including the cap arithmetic and the design's own breakdown this ticket's
`ready` state relies on, is on the ticket's own log
(`agents/eng-manager/board/ENG-006-unified-customer-identity.md`).

**Consequence:** `machine_wip` 0/6 → 1/6 (`ENG-006` now inside the counted
`ready`..`ready-to-ship` range for the first time). Approver-facing WIP 1/2 →
0/2; approval cap 1/3 → 0/3 — both now clear.

**Dead-end sweep (whole-board):** `ENG-001`–`ENG-005` all terminal with valid
closing log lines. `ENG-006` now ends in a valid state with a chain record
below. `inbox/2026-08-28-eng-events-dropped.md` (incident notice, `ticket:
unknown`) has no `decision:` yet and isn't P0 — left waiting on the approver,
already notified once at creation; not re-surfaced per the constitution's
P0-only rule for this pass.

**Notify sweep:** nothing raised this pass (one gate closed, none opened).
Nothing past 24h with no `nudged:`/`decision:`. Approval cap 0/3, not full —
no stall.

**Observations/exceptions:** none filed — the queued-duplicate race behind
this pass corroborates an already-open pattern rather than adding a new one.

`chained: ENG-006` — `ready` is eng-manager-owned, not the approver, not
blocked, not terminal. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-006` before
exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-006`) and whole-board: both exit 0, clean.

## 2026-08-28 — decision ENG-006: G1 approved, design done, one-way door escalated — awaiting-scope → designed → awaiting-decision

`decision` event pass, context `inbox/2026-08-27-eng006-g1-scope.md`. Narrow
scope per the event contract (act on the answered gate item, advance only
this ticket). Mode check clean (`MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

**Not a clean unanswered gate — found mid-recovery.** An earlier `watch` pass
today (08:35–08:44) had already started processing this exact answer: it
edited the PRD's `## Decision` section and flipped its status to `designed`,
then crashed on the account's monthly spend limit before touching the ticket,
the board, or the gate item. Its retry failed on a network error and the
event was dropped after two attempts
(`inbox/2026-08-28-eng-events-dropped.md`). This pass verified the PRD's
claims against the filesystem rather than trusting them — the frontend
knowledge-capture doc it claimed was "Done" did not exist — and completed the
work for real. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-006-unified-customer-identity.md`); one
observation filed on the general pattern
(`agents/eng-manager/observations.md`).

**Design done fresh against the live `aiorders-api` repo** (no schema in
version control there at all — read the edge functions that query
`customers` instead of trusting the PRD's inferences). Corrected one PRD
assumption in the process: legacy customer records are already scoped by
`restaurant_id` **or** `brand_id`, not restaurant-only. Full design:
`agents/architect/designs/ENG-006-unified-customer-identity.md` — Supabase's
native phone/OTP auth, two new additive tables, `customers` untouched.

**One-way door escalated rather than decided** — the PRD flagged this twice
for the architect to evaluate at G2; given the stakes (largest new subsystem
on this board) and no G2 precedent yet, put the actual question to the
approver instead of deciding unilaterally. Raised
`inbox/2026-08-28-eng006-g2-oneway-door.md`.

**Both G1 riders honored:** wrote
`agents/product-manager/specs/loyalty-program-frontend-understanding.md`
(knowledge capture only, not scheduled); carried the resolved SMS-vendor-cost
note into the design's Risks, with the caveat that delivery still isn't
wired to any real vendor in code.

**2 transitions this pass** (`awaiting-scope → designed → awaiting-decision`),
under the cap of 4. `machine_wip` unaffected. Approver-facing WIP and
approval cap both net unchanged at 1/2 and 1/3 — G1 closed, G2 opened, same
ticket.

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for state with a chain record below.

**Notify sweep:** this pass's own gate item raised and stamped. Nothing to
nudge. Approval cap 1/3, not full — no stall.

`chained: none` — `awaiting-decision`, owned by the approver; the chaining
guard never fires on a ticket waiting on a human. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-006`) and
whole-board: both exit 0, clean.

## 2026-08-28 — watch: swept all three inboxes again, nothing new

`watch` event pass, context `launchd`. Per the event's own narrower contract,
this sweeps `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`, and
`inbox/` only, acting on whatever is new — not a board-wide sweep. Mode check
clean (business-os `.env` → `MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh` (`ENG_ROOT` pinned to this
instance — the default root resolves against the script's own department
location, which has no `board/`; see `observations.md`), whole-board: exit 0,
clean.

**Swept all three inboxes fresh; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
`.gitkeep` (plus the former's already-`_handled/` entry); `inbox/requests/`
is empty. `inbox/` itself holds exactly one live item,
`2026-08-28-eng-events-dropped.md` (the incident notice for today's dropped
build-loop event) — read directly rather than assumed from the board: still
no `decision:` field, still not P0 (an incident notice, not production-down
or an exploitable vuln), still under 24h since its one `raised:` notification
(10:42:17). The immediately-preceding `scheduled` pass already accounted for
this exact file on identical grounds. Nothing else in any of the three
inboxes postdates that pass.

**Another occurrence of the open `.watch-seen` fingerprint-timing race**
(`proposals.md`, 2026-08-26 row; corroborated repeatedly in
`observations.md`). The preceding `scheduled` pass processed this same inbox
state but — being `scheduled`-typed, not `watch`-typed — never called
`commit_watch_fingerprint()`, so `traces/.watch-seen` stayed stamped at
whatever it held before today's `eng-events-dropped.md` arrived. This fire's
recomputed fingerprint still differed from that stale value, cleared the
above-the-lock de-noise check, and spent a full session confirming the
`scheduled` pass had already left nothing behind. Not re-diagnosed at length
here — the mechanism is already on record; this is a data point, not a new
finding. One line added to `observations.md`.

**Merge detection, dispatch, and the full dead-end sweep are out of scope for
this event** — no ticket sits `blocked` on an L1 PR regardless (`ENG-006` is
the only in-flight ticket, at `ready`). `ENG-006`'s own ticket log already
ends in a valid, accounted-for state with `chained: ENG-006`, spot-checked
directly against the file rather than trusted from the board's own account —
matches. That chain's `continue ENG-006` sits queued in `traces/.pending`
behind this pass, unaffected and not duplicated here — also queued behind it,
`1 decision 2026-08-28-eng006-g2-oneway-door.md`, which the prior pass already
predicted will find its file in `_handled/` and no-op.

**Notify sweep:** nothing new to raise. Today's incident notice is under the
24h nudge threshold. Approval cap 0/3, not full — no stall.

**Nothing to journal** — no gate was answered this pass.

No ticket was touched, no ticket state changed, no gate item was written.
`chained: none` — this pass advanced no ticket, so there is no hop of its own
to fire; `ENG-006`'s separately-queued `continue` (from the preceding pass)
runs on its own regardless, once this pass exits. All WIP/approval-cap
figures in the header are unchanged. Post-pass
`departments/engineering/lib/eng-gate-check.sh` (`ENG_ROOT` pinned as above):
exit 0, unchanged.

## 2026-08-28 — decision ENG-005: merge confirmed by git ancestry — blocked → shipped → verified

`decision` event pass, context `inbox/2026-08-27-eng005-merge-request.md`.
Narrow scope per the event contract (act on the answered gate item, advance
only this ticket). Mode check clean (business-os `.env` → `MODE=active`).
Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-005`)
and whole-board: both exit 0, clean.

**The gate item's answer:** `decision: approved`, `decided:
2026-08-28T00:13:09.817494+00:00`, text "merged" — the tracked channel this
time, unlike `ENG-002`'s direct-GitHub/control-center bypass. **Not taken on
the text alone** — re-ran the loop's own merge-detection check
(`schedules/eng_build_loop.md` step 5) from scratch in the department's own
worktree (`~/Documents/projects/_eng/aiorders-admin-hub`): `git fetch origin`
showed `919d355..edf6947 main -> origin/main`; `git merge-base
--is-ancestor chore/ENG-005-a4-poster-generator-wire-in origin/main`
confirmed MERGED; `edf6947` (PR #2's own merge commit) sits directly on
`51cdb29` (this ticket's commit) with no intervening commits, `git diff`
between the branch tip and `origin/main` empty. The merge commit's own
timestamp lands ~20s before the gate item's `decided:` stamp — consistent
with merging and recording the decision in one sitting.

**Acted as devops for `shipped`, then product-manager for `verified`, both
this pass.** Checked out `origin/main` in the worktree, ran `npm run build`
(succeeds; bundle now pulls in the component's own chunks, corroborating it's
genuinely reachable, not just present) and confirmed the wiring directly
(`grep -rn "A4PosterGenerator" src/pages/RestaurantDetails.tsx`). Both PRD
acceptance criteria re-confirmed against the merged tree. **Recorded
`health_check: not checked` and `rollback_tested: false` rather than
`green`/`true`** — unlike `ENG-002`, this release has a real new
production-facing artifact once deployed, and deploying is outside L1
autonomy regardless of diff content (a human merges; a human or their own
process deploys) — this department has no Cloudflare/monitoring access to
confirm live status either way, and said so plainly rather than inferring a
number it can't observe. Release record:
`agents/devops/releases/2026-08-28-aiorders-admin-hub-ENG-005.md`. Gate item
moved to `inbox/_handled/` with a processed footer; journaled in
`agents/eng-manager/config/decision-journal.md`. Full detail on the ticket's
own log.

**2 transitions this pass** (`blocked → shipped`, `shipped → verified`), well
under the cap of 4. Approver-facing WIP 2 → 1; approval cap 2/3 → 1/3
(`ENG-005` no longer counts — `verified` is terminal). `machine_wip`
unchanged at 0/6 (neither `blocked` nor `verified` is in the counted range).

**Dead-end sweep (scoped to this event):** `ENG-005`'s log now ends in a
valid, accounted-for terminal state. `ENG-006` (`awaiting-scope`, owner
approver) untouched — out of scope for a `decision` event naming this
ticket.

**Notify sweep:** nothing to raise (`verified` raises no gate item). Nothing
to nudge — the merge-request item is answered and closed. Approval cap now
1/3, not full — no stall.

**Observation filed, not acted on:** the per-ticket hop-budget file is named
`.hops-{today's date}-{TICKET-ID}` (`lib/eng-trigger.sh`), which resets to a
fresh file every midnight — but this document's own cadence section states
"the day's counter clears at midnight where a ticket's does not." The two
disagree; not investigated further here since it's outside this event's
scope and didn't block this ticket (today's `.hops-2026-08-28-ENG-005` file
didn't exist before this pass, well under the 8/day cap regardless). See
`agents/eng-manager/observations.md`.

`chained: none` — `verified` is a terminal state; nothing left for a machine
or the approver to do on this ticket. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-005`) and
whole-board: both exit 0, clean.

## 2026-08-27 — continue ENG-005: L1 PR opened, merge-request gate raised — ready-to-ship → blocked

`continue ENG-005` event pass — the dedicated session the preceding pass
chained specifically to open the L1 PR. Narrow scope per the event contract
(resume this ticket from its current state; no board-wide sweep). Mode check
clean (`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped and whole-board: both exit 0, clean. `traces/.hops-2026-08-27-ENG-005`
read `3` — third dispatch today, well under `hops_per_ticket` (8, `pro` tier).

**Checked for an already-opened PR first** — the immediately preceding pass
recovered one unrecorded build today already, so a duplicate PR was a real
risk. `gh pr list --head chore/ENG-005-a4-poster-generator-wire-in --state
all`: empty. None existed.

**Opened the PR** (`gh pr create`):
https://github.com/harsimranwalia/aiorders-admin-hub/pull/2. Wrote the L1
merge-request item (`inbox/2026-08-27-eng005-merge-request.md`, `gate:
merge`) carrying the PR link and the three gate verdicts by file reference.
Ran `lib/eng-notify.sh raise` — reproduced the already-filed `MODE`-collision
bug (`sent: active`, not `sent: raise`) — corroborating, not new. Stamped
`notified: 2026-08-27T16:03:58` by hand. State → `blocked`, `blocked_on:
approver`, `blocked_from: ready-to-ship`, owner `devops → approver` — same
design `ENG-002` used at this identical boundary.

**Cap check before advancing, read fresh:** `wip.approver_limit` (2) was at 1
(`ENG-006`'s G1); `awaiting_approver_cap` (3) was at 1/3. `ENG-005` is an
already-in-flight, already-fully-gated ticket reaching its own next gate, not
a new start, so `approver_limit`'s "nothing new starts" consequence is
untouched. Advancing brings `approver_limit` to 2/2 (at the limit, not over)
and `awaiting_approver_cap` to 2/3 (not over) — proceeded on that basis.

**1 transition this pass** (`ready-to-ship → blocked`), well under the cap of
4 — opening the PR and raising the gate is the real work of this hop.
`machine_wip` 1/6 → 0/6 (`blocked` sits outside the counted range).
Approver-facing WIP 1 → 2; approval cap 1/3 → 2/3.

**Dead-end sweep:** this ticket's log now ends in a valid, accounted-for
state with a chain record below. `ENG-006` (`awaiting-scope`, owner
approver) untouched — out of scope for a `continue` event naming this
ticket.

**Notify sweep:** this pass's own gate item raised and stamped above.
Nothing to nudge (brand new). Approval cap 2/3, not full — no stall.

`chained: none` — `blocked`, `blocked_on: approver`. This is the human gate
the whole hop was driving toward; firing `continue ENG-005` again would just
re-queue against a ticket with nothing left for a machine to do until the
approver merges the PR or replies. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-27 — continue ENG-005: recovered an unrecorded build, then ready → ready-to-ship in one hop

`continue ENG-005` event pass — the dedicated `building` (frontend) session
the preceding `decision` pass chained. Narrow scope per the event contract
(resume this ticket from its current state; no board-wide sweep). Mode check
clean (`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped and whole-board: both exit 0, clean.

**The chained `building` session had already run and died before recording
anything.** The worktree carried a clean, pushed commit
(`51cdb29`, "Wire A4PosterGenerator into RestaurantDetails") this ticket's log
had no record of — `traces/.hops-2026-08-27-ENG-005` (`2`) confirms this is
the second dispatch of `continue ENG-005` today. Ruled out a live competing
session first (full `ps`/`ppid` ancestry walk: the process holding
`traces/.loop.lock` is this pass's own top-of-chain orchestrator, not a
second instance), then independently verified the recovered commit rather
than trusting it — diff matches the architect's design exactly, lint
identical to a clean `origin/main` checkout (181 problems, zero new), build
succeeds, no dependency added. Full detail on the ticket's own log.

**Four transitions this pass, at the cap:** `ready → building → in-review →
in-security → ready-to-ship`. Principal-engineer + qa combined hop both
verdict **pass** (`agents/principal-engineer/reviews/ENG-005.md`,
`agents/qa/test-plans/ENG-005.md`); security verdict **pass**
(`agents/security/reviews/ENG-005.md`, confirmed the component's own
edge-function calls stay behind existing Bearer+admin-role gating, no new
capability granted); devops confirmed release readiness (rollback = revert
commit, $0/month, no freeze, no CI/CD to run). **Deliberately stopped at
`ready-to-ship`** rather than also opening the L1 PR and entering `blocked` —
that would be a 5th transition, over the per-pass cap — reserving the PR-open
for its own hop, same as `ENG-002`'s precedent bundles it with the transition
*into* `blocked` rather than before. `machine_wip` unchanged at 1/6
(`ready-to-ship` is inside the counted range); approval cap and approver WIP
both unchanged — none of this pass's transitions raise a gate item.

**Dead-end sweep:** this ticket's log now ends in a valid, accounted-for
state with a chain record below. `ENG-006` (`awaiting-scope`, owner approver)
out of scope for a `continue` event naming this ticket.

**Notify sweep:** nothing to raise (none of this pass's four states raise a
gate item). Nothing to nudge. Approval cap unchanged at 0/3, not full — no
stall.

`chained: ENG-005` — sitting at `ready-to-ship`, owned by devops (agent, not
the approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-005` for the
dedicated session to open the L1 PR and raise the merge-request gate.
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped and
whole-board: both exit 0, clean.

## 2026-08-27 — intake ENG-006: loyalty-points request shaped and split — one foundational ticket raised at G1, four more proposed but not filed

`intake` event pass — a new approver request in
`agents/product-manager/inbox/` (via control center): a cross-restaurant
loyalty points program, backend only for now. Narrow scope per the event
contract (shape the new request and carry it as far as it goes; the board was
not swept). Mode check clean (`MODE=active`; instance `mode:` empty, falls
through). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board (nothing to scope to yet): exit 0, clean.

**Confirmed this was the right event to act on it under.** An earlier
`watch` pass the same day had already found this file and correctly left it
alone — it arrived `via: control-center` with a matching `intake` event
already queued, so shaping it under `watch`'s contract would have both used
the wrong contract and starved the queued `intake` fire of any work to find
(`agents/eng-manager/observations.md`, 2026-08-27). This pass is that queued
fire.

**Full request-readback run** (`skills/request-readback/SKILL.md`): this PM's
reading and a blind architect reading, both independent opus subagents, each
given only the raw request and `knowledge/business-profile.md` — no material
divergence found between them (see `ENG-006`'s own log and PRD for the full
comparison). No question went to the approver as a result; the request is
detailed enough that every load-bearing gap either reading flagged alone was
resolved by proposing a requirement rather than guessing or asking.

**Sized `XL` as a single ticket — split before leaving intake**, per
`config/definition-of-done.md`'s size table. Shaped the identity/OTP-auth/
session/legacy-mapping slice as **`ENG-006`** (`L`, `aiorders-api`, full
lane), the one piece every other slice depends on. PRD written
(`agents/product-manager/specs/ENG-006-unified-customer-identity.md`)
defining the whole proposed five-ticket shape — the other four are
**proposed sequencing only, no IDs allocated, nothing filed** — so this pass
manufactures one ticket's worth of board presence, not five, ahead of the
approver seeing the shape.

**G1 raised** (`size: L` always requires it) — checked caps fresh first:
`wip.approver_limit` (2) at 0, `wip.approval_cap` (3) at 0/3, both free.
`inbox/2026-08-27-eng006-g1-scope.md` written, readback first, then the
recommendation (build `ENG-006` now; the four follow-on slices are open to
correction at this same G1). `lib/eng-notify.sh raise` run (exit 0;
`sent: active` not `sent: raise` — the known `MODE`-collision bug, eighth
corroborating occurrence, still the open `proposals.md` row); `notified:
2026-08-27T13:47:31` stamped. Original request moved
`agents/product-manager/inbox/` → `agents/product-manager/inbox/_handled/`
(new folder — no prior handled-folder existed under the PM's own inbox; this
mirrors the top-level `inbox/_handled/` convention).

**State: `intake → shaped → awaiting-scope`, all in one pass.** `owner`
`product-manager → approver`. Approver-facing WIP 0 → 1; approval cap
0/3 → 1/3. `machine_wip` unchanged at 1/6 — `awaiting-scope` sits outside
that range.

**Dead-end sweep (scoped to this event):** `ENG-006`'s log ends in a valid,
accounted-for state with a chain record. `ENG-005` untouched and out of
scope for this event — it already carries its own valid `chained: ENG-005`
from the immediately preceding pass.

**Notify sweep:** this pass's own gate item raised and stamped above.
Nothing to nudge (brand new). Approval cap 1/3, not full — no stall.

`chained: none` — `ENG-006` sits at `awaiting-scope`, owned by the approver;
the chaining guard never fires on a ticket waiting on a human. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-006`) and
whole-board: both exit 0, clean.

## 2026-08-27 — decision ENG-005: surface follow-up answered — designed → ready in the same pass, no one-way door, chained to building

`decision` event pass — the approver answered `ENG-005`'s G1 follow-up
(`inbox/2026-08-27-eng005-g1-followup-surface.md`). Narrow scope per the
event contract (act on the answered gate item, advance only this ticket).
Mode check clean (business-os `.env` → `MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

**The answer:** `decision: approved`, `decided:
2026-08-27T20:08:53.367622+00:00`, text "lets do RestaurantDetails.tsx" —
confirms the PM's recommendation exactly as offered. Both halves of the
original G1 (fork, then surface) are now answered, so `awaiting-scope`'s exit
condition is met. PRD updated (`status: designed`, acceptance criteria filled
in concretely); gate item moved to `inbox/_handled/` with a processed
footer; journaled in `agents/eng-manager/config/decision-journal.md`.

**Design done this pass** (architect), same one-pass pattern `ENG-002` used
at this boundary. Investigated fresh against `origin/main` in both
`_eng/aiorders-admin-hub` and `_eng/aiorders-api` (`git fetch` first):
confirmed the component's `url-shortener` edge-function dependency exists,
confirmed `jspdf` is already in `package.json` (no new dependency), and
read `RestaurantDetails.tsx` in full to find `Restaurant` has no color field
anywhere — not a correction of the follow-up's own investigation, which
never claimed `primaryColor` was loaded (it named only the four fields that
are), just the next question design had to answer that scope selection
didn't. The design passes `null` and relies on the component's own fallback
accent.
Design written:
`agents/architect/designs/ENG-005-a4-poster-generator-wire-in.md` —
`one_way_doors: []`. No one-way door (additive, reversible, no schema, no
new dependency) → `awaiting-decision` (G2) skipped entirely per
`definition-of-done.md`.

**`ready` reached the same pass** (eng-manager): one task, no sequencing,
assigned to frontend. `machine_wip` 0/6 → 1/6. Approver-facing WIP 1 → 0;
approval cap 1/3 → 0/3. **2 transitions this pass**
(`awaiting-scope → designed`, `designed → ready`), under the cap of 4. Did
not proceed into `building` — new implementation work, which is where a pass
stops and hands off instead of pushing through (`schedules/eng_build_loop.md`
step 6).

**Dead-end sweep:** this ticket's log ends in a valid, accounted-for state
with a chain record below. No other ticket in flight — `ENG-004` is terminal.

**Notify sweep:** nothing to raise (no G2 this pass). Nothing to nudge.
Approval cap 0/3, not full — no stall.

`chained: ENG-005` — sitting at `ready`, owned by eng-manager (agent, not
the approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-005` for the
dedicated `building` (frontend) session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-27 — watch: ENG-005's G1 answered only half its own question — fork resolved, surface carried forward as one follow-up

`watch` (launchd) pass — a file changed in a watched inbox outside the
notify/poll channel. Mode check clean (business-os `.env` → `MODE=active`;
instance `config/config.yaml` → `mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-005`) and
whole-board: both exit 0, clean.

**Swept all three watched inboxes**, per the event's own contract.
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` held one
item directly: `2026-08-27-eng005-g1-scope.md`, changed since the archived
`watch` pass a few entries back confirmed it still blank — now carrying
`decision: approved`, `decided: 2026-08-27T18:03:50.514589+00:00`, a second
`## Decision` section appended below the original placeholder. Answered by
direct file edit, not through `lib/eng-notify.sh`'s reply channel — sixth
such occurrence on this instance (decision journal).

**The answer settles the fork and nothing past it.** Verbatim: "wire it in."
This G1's own text asked for two things at once — decide wire-in vs. revert,
and if wire-in, name the route/surface, "so acceptance criteria can be
written against it." Only the fork came back. Read the two halves
separately rather than treating a partial answer as a complete one: "wire it
in" leaves no real ambiguity about the fork (the revert branch is closed,
the component stays); it says nothing about the surface, which this
ticket's own PRD had already flagged twice (Readback's Assumed section,
Non-goals) as the approver's call, not a default the department infers from
silence or convenience.

**Investigated before asking a second time, rather than bouncing the
question back unhelped.** `git fetch origin` in `_eng/aiorders-admin-hub`
(worktree predated `bfddffe`), then read `A4PosterGenerator.tsx` off
`origin/main`: props are `restaurantName`, `websiteUrl`, `logoUrl`,
`primaryColor`, `restaurantId` — one restaurant's own detail context. Of the
admin hub's 19 pages (`src/pages/*.tsx`) and its sidebar
(`AppSidebar.tsx`), exactly one is shaped to hold that context:
`RestaurantDetails.tsx`, which already loads `name`, `website`, `logo_url`
and `id` for a single restaurant (`Restaurants.tsx` is the list view, not a
detail context). No existing poster/QR/marketing section there — wiring in
means a new section, not flipping on something half-built. Offered as a
recommendation in the follow-up, not adopted as the answer: a well-evidenced
guess is still a guess, and this PRD's non-goal is specifically about not
making this one.

**Closed out the answered item, raised one narrow follow-up, left the fork
resolved on the record.** PRD `## Decision`
(`agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md`)
filled in with the approver's words and this interpretation; `status` stays
`awaiting-scope`. `inbox/2026-08-27-eng005-g1-scope.md` moved to
`inbox/_handled/` with one appended line pointing at the follow-up, so the
closed item is traceable rather than just gone. Wrote
`inbox/2026-08-27-eng005-g1-followup-surface.md` (`agent: product-manager`,
`gate: scope`, `follow_up_to:` the closed item, `recommendation:
RestaurantDetails.tsx`), ran `departments/engineering/lib/eng-notify.sh
raise` on it (reproduced the already-filed `MODE`-collision bug — `sent:
active`, not `sent: raise` — corroborating, not new), stamped `notified:
2026-08-27T18:16:48`. Journaled in
`agents/eng-manager/config/decision-journal.md` — first data point on this
instance of a G1 answer settling part of its own question and leaving a
named, requested sub-detail open.

**Held at `awaiting-scope`, did not advance to `designed`.**
`definition-of-done.md` gives `designed` to the architect for technical
design — not for naming a product surface this PRD explicitly reserved for
the approver. Advancing without the surface would just move the guess one
state later and relabel it a design decision instead of a scope one. `owner`
stays `approver`. No cap or WIP change — still the same one approver-facing
slot this ticket already held (approval cap unchanged at 1/3, approver WIP
unchanged at 1), narrowed to one question on it.

**Dead-end sweep:** `ENG-005`'s log now ends in a valid, accounted-for state
with a chain record below. No other ticket is in flight to check — `ENG-004`
reached `verified` (terminal) in the pass immediately before this one; see
its own board file and the dated entry below.

**Notify sweep:** this pass's own follow-up was raised and stamped above —
nothing else to raise. Nothing to nudge (`ENG-005`'s original G1 is now
answered and closed, its follow-up is minutes old). Approval cap unchanged
at 1/3, not full — no stall.

`chained: none` — sitting at `awaiting-scope`, owned by the approver; the
chaining guard never fires on a ticket waiting on a human. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-27 — continue ENG-004: ready-to-ship through verified in one pass — G3 answered in ~92 seconds, ticket now terminal

`continue ENG-004` event pass — the dedicated `ready-to-ship` (devops)
session the preceding `in-security` hop chained. Narrow scope per the event
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped and whole-board: both exit 0, clean.

**`in-security → ready-to-ship`, 1 transition.** Acted as devops per
`ADR-004`: confirmed no release, rollback, or observability plan is owed —
the change already reached `origin/main` on 2026-08-24, before this ticket
existed. Re-checked `config/projects.md` (L1, worktree present), release
window (Thursday, no `ENG_RELEASE_FREEZE`), and cost (`$0/month`) fresh.
`machine_wip` 1/6 → 0/6.

**Continued into `awaiting-release` the same pass** — unlike `ENG-001`'s
split at this identical boundary, which its own log names as cap-driven; the
approval cap here had room (checked fresh: 1/3, only `ENG-005`'s G1), so
nothing forced a stop. No ADR or schedule rule names a fresh-context
requirement between these two states, unlike security-after-quality. Wrote
and raised `inbox/2026-08-27-eng004-g3-verification.md` (`lib/eng-notify.sh
raise`) — reproduced the already-filed `MODE`-collision/Slack-not-Telegram
bugs (`proposals.md`, 2026-08-25), not a new finding. Cap 1/3 → 2/3; approver
WIP 1 → 2. **2nd transition.**

**The G3 was answered before this pass exited** — `decision: approved`, no
comment, ~92 seconds after `notified:` was stamped, by the same hand-edit
shape every gate on this instance but `ENG-002`'s merge has used. Fifth data
point on that pattern; the turnaround itself journaled as consistent with,
not proof of, the open notify-channel proposal
(`agents/eng-manager/config/decision-journal.md`). Item moved to
`inbox/_handled/`.

**`awaiting-release → shipped`, 3rd transition.** Devops recorded the G3
confirmation in place of a deploy — no release record fabricated at
`agents/devops/releases/`, `links.release` stays empty (`ADR-004`).

**`shipped → verified`, 4th transition — 4 total this pass, at the cap.**
Product-manager re-confirmed all five acceptance criteria fresh against
disk/git (project linkage, admin-hub's empty `supabase/` tree, two re-sampled
blob-SHA matches, the 22-file ordering, `0`/`0` ahead-behind) and re-opened
all three receipts — all hold. Full citations on the ticket's own log.

**This ticket is now terminal.** `machine_wip` stays 0/6; approval cap
2/3 → 1/3 (`ENG-005`'s G1 only); approver WIP 2 → 1 — noted for the next
pass's arithmetic, not acted on here.

**Dead-end sweep (scoped to `ENG-004`):** ends in a valid, terminal state.
`ENG-005` untouched — out of scope for this event.

**Notify sweep:** the pass's own gate item was raised and is already
answered above; nothing else to raise or nudge.

Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped and
whole-board: both exit 0, clean. `chained: none` — `verified`, terminal;
never re-fired.

## 2026-08-27 — continue ENG-004: in-security verdict pass — content-reviewed, not just hash-checked; chained to ready-to-ship

`continue ENG-004` event pass — the dedicated `in-security` session the
preceding combined review+quality hop chained. Narrow scope per the event
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean (business-os `.env` → `MODE=active`; instance
`config/config.yaml` → `mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Dispatch: `in-qa → in-security`, 1 transition.** Acted as security per
`ADR-004` — the one gate on this ticket with real content, not ceremony.
Independently re-derived AC1/presence/AC4 fresh against disk/git in
`_eng/aiorders-admin-hub` and `_eng/aiorders-api` (`git fetch origin` in both
first); re-confirmed AC3 (unmodified) by a second, independent mechanism
(git's own blob SHA, not review/QA's SHA-256) — all six files identical
pairwise across both repos. Then read the six files' actual content, the
substantive check neither review nor QA did: coherent, complete
RLS/`search_path` hardening across `profiles`, `restaurants`, and the new
`restaurant_activations` table. Verdict **pass** —
`agents/security/reviews/ENG-004.md` written, `links.security_review` set.
Full citations on the ticket's own log. `machine_wip` unchanged at 1/6 —
`in-security` falls inside the counted range.

**One observation filed, not a finding** (`observations.md`): a migration
comment about view security semantics that reads backwards against actual
Postgres defaults (`restaurants_public`'s recreate, item 5 of the six) —
explicitly out of this ticket's scope per the PRD's own non-goal ("whether
that policy is still the right policy today"), since the reconciliation
itself is confirmed intact by an independent hash method.

**Not proceeding into `ready-to-ship` this pass, deliberately** — same
discipline this ticket has used at every prior hop; devops's own
confirmation (no release/rollback/observability plan owed, per `ADR-004`) is
real, distinct work reserved for its own session.

**Dead-end sweep (scoped to `ENG-004`):** its log now ends in a valid,
accounted-for state with a chain record below. `ENG-005` (`awaiting-scope`,
owner approver) untouched — out of scope for a `continue` event naming one
ticket.

**Notify sweep:** nothing to raise (`in-security` raises no gate item).
Nothing new to nudge — `ENG-005`'s G1 still under 24h old; approval cap
unchanged at 1/3.

`chained: ENG-004` — sitting at `in-security`, owned by `security` (agent,
not the approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-004` for the
dedicated `ready-to-ship` (devops) session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

## 2026-08-27 — continue ENG-004: combined review+quality hop — building → in-review → in-qa, security deferred to its own session

`continue ENG-004` event pass — the dedicated combined review+quality session
the preceding `ready → building` pass chained (queued behind one intervening
no-op `watch` fire, drained immediately after). Narrow scope per the event
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean (business-os `.env` → `MODE=active`; instance
`config/config.yaml` → `mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

**Dispatch: `building → in-review → in-qa`, 2 transitions.** Acted as
principal-engineer and qa on the combined hop (`schedules/eng_build_loop.md`
step 6): independently re-derived all five acceptance criteria fresh against
disk/git in `_eng/aiorders-admin-hub` and `_eng/aiorders-api` (`git fetch
origin` in both first) rather than citing the design's or `building`'s own
numbers — project linkage, the still-empty `supabase/migrations` on
admin-hub's `origin/main`, both consolidation commit pairs, a fresh
`shasum -a 256` re-hash of all six named files (all identical), the 22-file
migration count/ordering, and the ref-level `0`/`0` ahead-behind on admin-hub's
local `main`. Verdict **pass** on both:
`agents/principal-engineer/reviews/ENG-004.md` and
`agents/qa/test-plans/ENG-004.md` written, `links.review`/`links.test_plan`
set. Full citations on the ticket's own log. `machine_wip` unchanged at 1/6 —
both states fall inside the counted range.

**Not proceeding into `in-security` this pass, deliberately** — sharper than
the "own session" discipline this ticket has used at every prior hop:
`ADR-004` names this ticket's security gate as real, substantive content
(five of six files under review are the RLS/`search_path` hardening surface
itself) and warns explicitly against waving it through as ceremony, unlike
`ENG-001`'s all-`n/a` security pass (the one case here where review, quality
and security were combined into a single session). Reserved for its own
dedicated pass with fresh context.

**Dead-end sweep (scoped to `ENG-004`):** its log now ends in a valid,
accounted-for state with a chain record below. `ENG-005` (`awaiting-scope`,
owner approver) untouched — out of scope for a `continue` event naming one
ticket.

**Notify sweep:** nothing to raise (`in-qa` raises no gate item). Nothing new
to nudge — `ENG-005`'s G1 is still well under 24h old; approval cap unchanged
at 1/3.

`chained: ENG-004` — sitting at `in-qa`, owned by `qa` (agent, not the
approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-004` for the dedicated
`in-security` session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-27 — watch: swept all three inboxes again, nothing new — seventh occurrence, ENG-005's G1 fingerprint-stale exactly as diagnosed

`watch` (launchd) pass, drained immediately behind the `continue ENG-004`
(`ready → building`) pass that ended 10:13:51 (`traces/eng-loop-2026-08-27.log`,
549s, exit 0) — day 5/40 hops charged, 0 refunded today. Per the event's own
narrower contract, swept only `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/` and `inbox/` (including `inbox/requests/`),
acting on whatever is new. Mode check clean (business-os `.env` →
`MODE=active`; instance `config/config.yaml` → `mode:` empty, falls
through). Pre-pass `departments/engineering/lib/eng-gate-check.sh` (`env
ENG_ROOT=<instance> sh eng-gate-check.sh`): exit 0, clean.

**Swept all three inboxes; found nothing to act on.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` holds
exactly one file directly — `2026-08-27-eng005-g1-scope.md` — which is
`ENG-005`'s own G1, raised and notified by the `scheduled` pass earlier this
same day (see that entry below); `inbox/_handled/`'s ten items are all
already accounted for, none new. Read the gate item itself and the PRD's own
`## Decision` section
(`agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md`)
directly rather than trusting the board's characterization of it: both still
carry the unfilled template placeholder ("Filled in by the approver." / "The
approver's answer:" blank) — no decision recorded anywhere. Nothing new to
act on for `ENG-005`; it stays exactly at `awaiting-scope`, owner `approver`.

**Seventh occurrence of the already-diagnosed `.watch-seen` staleness
pattern** (`observations.md` and `proposals.md`'s open 2026-08-26 row carry
the first six; the sixth is this board's own archived entry from earlier
today). Confirmed the mechanism live rather than assuming it still applies:
`traces/.watch-seen` currently holds
`da39a3ee5e6b4b0d3255bfef95601890afd80709` — the SHA-1 of an empty input —
meaning the last `watch`-typed pass to commit a fingerprint saw all three
inboxes empty, and every non-`watch` pass since (today's `continue ENG-004`
×2 and the `scheduled` sweep) changed `inbox/`'s top-level contents without
ever being able to update it, per `commit_watch_fingerprint`'s own `[
"$EVENT" = "watch" ]` guard (`lib/eng-trigger.sh`). Exactly the fix the open
proposal already names. **Not filing a new proposal or observation** — a
seventh data point on an already-diagnosed, already-proposed issue is
corroboration, same restraint every occurrence since the fourth has applied.

**Queue backlog, unchanged from the entry above.** `traces/.pending` still
holds `1 continue ENG-004` — appended by the `ready → building` pass's own
chain fire for the combined `in-review`/`in-qa` session, queued behind this
`watch` fire only because `watch` was older in the queue (the file-watcher
fired on `inbox/2026-08-27-eng005-g1-scope.md`'s creation before that chain
fire ever ran). Not re-fired here: `continue ENG-004` was queued by its own
originating pass, and re-firing it would only duplicate a line the queue's
own dedup collapses back down.

**Dead-end sweep:** out of scope for this event beyond the inboxes it
unblocks. `ENG-004` (`building`, owner `eng-manager`) and `ENG-005`
(`awaiting-scope`, owner `approver`) both already carry valid chain records
from their own last passes, untouched here.

**Notify sweep:** nothing to raise (no gate item written this pass); nothing
to nudge (`ENG-005`'s G1 is under an hour old, no `nudged:` due); approval
cap unchanged at 1/3, not full, no stall.

No ticket was touched this pass, so no ticket log carries a chain record —
the record lives here instead, same convention every no-op `watch` entry on
this board has used. `chained: none` — nothing this pass owns to chain;
`continue ENG-004` is already queued from its own originating pass, not
re-fired. Post-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0,
clean, unchanged.

## 2026-08-27 — continue ENG-004: building-as-verification-record written per ADR-004

`continue ENG-004` event pass — the dedicated session the preceding
`designed → ready` pass chained. Narrow scope per the event contract (resume
the named ticket from its current state; no board-wide sweep). Mode check
clean (business-os `.env` → `MODE=active`; instance `config/config.yaml` →
`mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Dispatch: `ready → building`, 1 transition.** Re-verified all five
acceptance criteria fresh against disk/git in `_eng/aiorders-admin-hub` and
`_eng/aiorders-api` (`git fetch origin` in both first) rather than trusting
`designed`'s prior citations — project linkage, the absence of any
`supabase/migrations`/`functions` directory on admin-hub's `origin/main`,
both consolidation commit pairs, a fresh `sha256` re-hash of all six named
files against their new home in `aiorders-api` (all identical — a stronger
check than the design's own byte-diff), the 22-file migration count and
ordering, and a ref-level (not working-tree) confirmation that admin-hub's
local `main` is 0 ahead/0 behind `origin/main`. All five held exactly as
`designed` recorded them a day earlier — nothing drifted. `branch:` stays
empty per `ADR-004` (the diff this ticket investigated already exists on
`origin/main`, produced by the approver directly on 2026-08-24, not by this
ticket). `machine_wip` unchanged at 1/6 — both `ready` and `building` fall
inside the counted range. Full citations on the ticket's own log.

**Not proceeding into `in-review`/`in-qa` this pass, deliberately** — per
`schedules/eng_build_loop.md` step 6 those are one combined hop, and each
still owes its own independent re-derivation against disk/git per `ADR-004`
— real, distinct gate work reserved for its own session, same discipline
this ticket has applied at every earlier hop.

**Dead-end sweep (scoped to `ENG-004`):** its log now ends in a valid,
accounted-for state with a chain record below. `ENG-005` (`awaiting-scope`,
owner approver) untouched — out of scope for a `continue` event naming one
ticket.

**Notify sweep:** nothing to raise (`building` raises no gate item). Nothing
new to nudge — approval cap unchanged at 1/3 (`ENG-005`'s G1 only).

`chained: ENG-004` — sitting at `building`, owned by `eng-manager` per
`ADR-001`'s owner override as extended by `ADR-004` (agent, not the
approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-004` for the
combined `in-review`/`in-qa` session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

## 2026-08-27 — scheduled: safety-net sweep — ENG-005's G1 raised, ENG-004 left mid-chain

`scheduled` (launchd) pass — the twice-daily safety-net sweep. Mode check
clean (business-os `.env` → `MODE=active`; instance `config/config.yaml` →
`mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Business/technical intake:** `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/` and `inbox/requests/` all empty (`.gitkeep`
only) — nothing new to shape or propose.

**Gate returns:** `inbox/` holds nothing outside `_handled/` — no answered
item to act on. Cross-checked `inbox/_handled/` (ten items) against the
board and the decision journal; all already reflected.

**Merge detection:** no in-flight ticket is `blocked` on anything — no-op.

**Dispatch (priority order `now` → empty; neither in-flight ticket has a
`priority` set):** reviewed both in-flight tickets.

- `ENG-004` (`ready`, owner `eng-manager`) — left untouched, deliberately.
  Its own last log entry already chained a dedicated `continue ENG-004`
  session for the building-as-verification-record step, and
  `traces/.pending` confirms it (`1 continue ENG-004`), still undrained.
  Re-firing it here would only duplicate an already-queued line, and
  attempting `ready → building` inline would break the same discipline this
  exact hop has followed at every prior occurrence on this board — reserved
  for its own dedicated session.
- `ENG-005` (`shaped`, owner `product-manager`) — the only ticket in the
  To-do column (`intake`/`shaped`/`awaiting-scope`), so it's what this
  step's ordering picks up. Re-checked the caps fresh rather than trusting
  the board's cached header: `wip.approver_limit` (2) at 0, `wip.approval_cap`
  (3) at 0/3, both fully free. Raised its G1 —
  `inbox/2026-08-27-eng005-g1-scope.md` — framed as the fork itself rather
  than a plan to approve (wire `A4PosterGenerator.tsx` into a named surface,
  or revert `bfddffe`), matching this ticket's own PRD, which deliberately
  never proposed a direction. Advanced `shaped → awaiting-scope`, `owner`
  `product-manager → approver`. Full reasoning on the ticket's own log.

**Notify sweep.** Ran `departments/engineering/lib/eng-notify.sh raise
inbox/2026-08-27-eng005-g1-scope.md`; stamped `notified: 2026-08-27T09:59:41`
on the gate item. Reproduced the already-filed `MODE`-collision bug
(`traces/eng-notify-2026-08-27.log`: `sent: active`, not `sent: raise`) —
corroborating the open 2026-08-25 proposal, not a new finding. No nudge due
— `ENG-005`'s G1 is minutes old and nothing else is open. Approval cap
0/3 → 1/3, not full — no stall alert.

**Dead-end sweep.** `ENG-004`'s log ends in a valid, accounted-for state
with its own chain record (`continue ENG-004`, already queued, untouched
here). `ENG-005`'s log now ends in a valid state too, written this pass.
`config/exceptions.md` is empty — nothing at a third occurrence.
`proposals.md`'s five open rows are all 0–2 days old, none near the 30-day
expiry.

**One observation filed** (`observations.md`): uncommitted modifications
found in the department's own (shared, read-only-to-an-instance) tree at
this pass's start — `lib/eng-schedule.sh` and
`schedules/eng_weekly_report.md` modified, `lib/eng-report.sh` untracked.
None of the three is a file this loop reads (`eng-gate-check.sh`,
`eng-trigger.sh`, and `eng_build_loop.md` itself are all untouched), so out
of scope to act on from inside this pass; flagged since the department
directory is meant to be read-only from an instance's perspective.

**Chain.** `ENG-005` — `chained: none`, written on the ticket's own log:
sitting at `awaiting-scope`, owned by the approver. `ENG-004` — not touched
this pass, so the record lives here instead: `chained: none — continue
ENG-004` already queued from its own prior pass; re-firing here would only
duplicate a line the queue's own dedup collapses back to one, spending a
fire for no additional effect.

Approver-facing WIP 0 → 1, approval cap 0/3 → 1/3, machine WIP unchanged at
1/6. Post-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0,
clean.

## 2026-08-27 — continue ENG-004: work breakdown done, zero implementation units — advanced to ready

`continue ENG-004` event pass — the dedicated work-breakdown session the
`designed → ready` hand-off named. Narrow scope per the event contract
(resume the named ticket from its current state; no board-wide sweep). Mode
check clean (business-os `.env` → `MODE=active`; instance `config/config.yaml`
→ `mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Work breakdown: zero implementation units.** Per `ADR-003`/`ADR-004`, the
remediation this ticket investigated was already executed by the approver
directly on 2026-08-24 — nothing to sequence, nothing to assign. Advanced
`ENG-004` `designed → ready`, owner `architect → eng-manager` per
`definition-of-done.md`. `machine_wip` 0/6 → 1/6. No approver-facing WIP or
approval-cap impact — `ready` raises no gate. Full reasoning on the ticket's
own log.

**Not proceeding into `building` this pass, deliberately** — same split
`ENG-001`'s history applied at this identical hop, already flagged by this
ticket's own prior log entry: `ready → building` is reserved for its own
session.

**Dead-end sweep (scoped to `ENG-004`):** log ends in a valid state with a
chain record. `ENG-005` untouched — out of scope for a `continue` event
naming one ticket.

**Notify sweep:** nothing to raise (no gate at `ready`); nothing to nudge
(approval cap 0/3).

`chained: ENG-004` — sitting at `ready`, owned by `eng-manager` (agent, not
the approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-004` for the
building-as-verification-record session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

## 2026-08-27 — watch: swept all three inboxes again, nothing new — sixth occurrence, queue backlog sitting behind it

`watch` (launchd) pass, `traces/.pass-out.24282`: `pass start: watch (launchd)
[day 1/40 charged, 0 refunded today]`, after the queue collapsed 1 duplicate
`watch launchd` event into one. Per the event's own narrower contract, swept
only `agents/product-manager/inbox/`, `agents/eng-manager/inbox/` and
`inbox/`, plus `inbox/requests/`, acting on whatever is new. Mode check clean
(business-os `.env` → `MODE=active`; instance `config/config.yaml` → `mode:`
empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh` (`env ENG_ROOT=<instance> sh
eng-gate-check.sh`): exit 0, clean.

**Swept all three inboxes; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` itself
holds no files directly — everything that has ever landed there has already
moved to `inbox/_handled/` (ten items, spanning the original approver
requests through `ENG-003`'s G1), none new. Sixth recorded instance of a
`watch` fire finding nothing (`observations.md`'s rows, `proposals.md`'s open
row, and this board's archived/live entries carry the first five).

**Queue backlog, noted rather than freshly diagnosed.** `traces/.pending`
currently holds `1 continue ENG-004` and `1 scheduled launchd`, both still
undrained as this pass runs — today's own 09:30 safety-net sweep queued
behind an older event rather than running. Consistent with
`eng_build_loop.md`'s description of the queue (a fire drains the front only
when it reaches the lock; an idle stretch leaves whatever's queued sitting
untouched) rather than a new mechanism traced through the code this pass —
unlike the fifth occurrence's addendum, this isn't offered as a sharpened
root cause, just an honest note of what's on disk right now. Not re-fired:
`continue ENG-004` was queued by its own originating pass (`2026-08-26 —
continue ENG-004`, this board), and re-firing it here would only duplicate a
line the queue's own dedup collapses back down — same restraint every
occurrence since the fourth has applied. `scheduled launchd` is likewise left
for the next fire to drain; forcing a board-wide sweep from inside a
`watch`-scoped pass would be exactly the job this event's own narrower
contract reserves for `scheduled` itself.

**Not filing a new proposal or observation.** No new mechanism was traced
here beyond what `proposals.md`'s open row and `observations.md`'s addendum
already cover; a sixth data point on an already-diagnosed, already-proposed
issue is corroboration, same reasoning the fourth occurrence gave for
declining to refile.

**Dead-end sweep:** out of scope for this event beyond the inboxes it
unblocks. `ENG-004` (`designed`, owner `architect`) and `ENG-005` (`shaped`,
owner `product-manager`) both already carry valid chain records from their
own last passes, untouched here.

**Notify sweep:** nothing to raise (no gate item written this pass). Nothing
open to nudge — approval cap is 0/3, nothing waiting on the approver.

No ticket was touched this pass, so no ticket log carries a chain record —
the record lives here instead, same convention every no-op `watch` entry on
this board has used. `chained: none` — nothing this pass owns to chain;
`continue ENG-004` is already queued from its own originating pass, not
re-fired. Post-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0,
clean, unchanged.

## 2026-08-26 — watch: swept all three inboxes again, nothing new — fifth occurrence, a distinct mechanism from the open proposal

`watch` (launchd) pass — drained immediately behind the `decision` no-op
directly above: that pass ended 23:16:55 and this one began draining the
same second (`traces/eng-loop-2026-08-26.log`). Per the event's own narrower
contract, swept only the three watched inboxes plus `inbox/requests/`,
acting on whatever is new. Mode check clean (business-os `.env` →
`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`:
exit 0, clean.

**Swept all three inboxes; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` holds
exactly one item, `2026-08-25-eng003-g1-scope.md` — checked against its last
committed version (`git diff`), the only change is the
`nudged: 2026-08-26T15:43:45` stamp already recorded on this board's
"Waiting on the approver" list; still no `decision:`. `inbox/_handled/`
matches the board exactly (`ENG-001`'s G3, `ENG-002`'s merge request,
`ENG-004`'s G1), all already reflected in ticket state and the decision
journal. Nothing to act on.

**Root cause, read from the code rather than assumed.** Fifth recorded
`watch`-fires-for-nothing occurrence (`observations.md`'s two rows and the
open proposal's row, `proposals.md` 2026-08-26, carry the first four) — but
a different mechanism from the one that proposal diagnoses, which blames
non-`watch` event types never committing `.watch-seen`. Read
`lib/eng-trigger.sh` directly: `WATCH_FP` is computed **before the pass
launches** (line 1583), deliberately — its own comment says anything that
arrives *during* a pass must still look new to the next fire — and
`commit_watch_fingerprint` (line 424) writes that unchanged pre-launch value
to `.watch-seen` **only on a clean exit** (`if [ "$STATUS" -eq 0 ]`, line
1892-1893). The immediately-preceding `watch` pass (pid 73496, `pass end:
watch (exit 0, 669s)` at 23:08:31) exited 0 and so committed — but it had
just moved `2026-08-25-eng004-g1-scope.md` out of `inbox/` into `_handled/`
as part of processing `ENG-004`'s G1, so the fingerprint it committed
reflects `inbox/`'s state *before* that move, not after. Any `watch` pass
that actually processes a gate item modifies a watched inbox this same way,
so this isn't a one-off: it guarantees the next `watch` fire sees a diff and
relaunches for zero new work, every time a `watch` pass does real work. The
open proposal's fix ("commit after every event type") doesn't cover this —
the pass that caused it *was* `watch`-typed and *did* commit. Filed as an
addendum in `observations.md` rather than a second proposal — it sharpens
the existing one's required fix scope, it doesn't ask for a new ticket.

**Dead-end sweep:** `ENG-003` (`awaiting-scope`), `ENG-004` (`designed`) and
`ENG-005` (`shaped`) ticket logs each already end in a valid, accounted-for
state with their own chain record — none touched by this pass, none a dead
end. `traces/.pending` still holds exactly `1 continue ENG-004`, queued by
the preceding `watch` pass and not yet drained; not re-fired here, same
reasoning the preceding `decision` pass gave for the identical situation.

**Notify sweep:** nothing to raise (no gate item written this pass); no
nudge due (`ENG-003` already nudged once, 2026-08-26). Approval cap
unchanged at 1/3 — not full, no stall alert.

No ticket was touched this pass, so no ticket log carries a chain record —
same as the `decision` no-op two entries above; the record lives here
instead. `chained: none` — nothing this pass owns to chain; `continue
ENG-004` is already correctly queued from the prior pass. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean, unchanged.

## 2026-08-26 — continue ENG-004: investigation found the consolidation already done — design + ADR-003 + ADR-004 written

`continue ENG-004` event pass — the dedicated investigation-and-design
session the preceding `watch` pass chained. Narrow scope per the event
contract (resume the named ticket from its current state; no board-wide
sweep). Mode check clean (business-os `.env` → `MODE=active`; instance
`config/config.yaml` → `mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Investigated in the department's own worktrees** (`_eng/aiorders-admin-hub`,
`_eng/aiorders-api`; the human's checkouts were never touched), `git fetch`
first in both. Found both `_eng/` branches diverged from `origin/main` —
admin-hub's mildly, aiorders-api's by dozens of commits predating this
consolidation entirely — so read `origin/main` directly rather than trusting
either worktree's files (logged as an observation, see below).

**The investigation this ticket asked for turned out to already be answered.**
`aiorders-api` is authoritative: two paired same-session commits, both
2026-08-24 (`4b6a835`/`c90c02c` at ~09:52, `5b3bac2`/`919d355` at ~10:18,
seconds apart each pair) moved every migration from `aiorders-admin-hub` to
`aiorders-api` and removed admin-hub's `supabase/migrations` entirely — **the
approver did this directly, one day after filing the request, before the
ticket ever reached `shaped`.** Content-diffed all six named files
byte-for-byte against their new home: all six identical, one renamed
(UUID-suffixed filename → descriptive name), none edited — confirming the
"renamed consolidation" the architect's blind reading flagged as unruled-out
by a filename sweep. `20260312000001_restaurant_activations.sql` now sorts
before `20260408000001_google_review_history.sql` in the same repo, resolving
the replay-order hazard the original request named. The PRD's flagged "four
siblings" discrepancy is resolved too — the real count is three, matching the
three timestamps actually named. `aiorders-admin-hub`'s local `main` already
matches `origin/main` exactly (no ahead/behind), so the pending uncommitted
deletion the request opened with is resolved at the ref level. Attempted an
actual local Docker replay for extra confidence beyond the static diff;
aborted mid-image-pull as disproportionate once it was clear the static
evidence already answered the question — Docker left clean, scratch dirs
removed. Full citations (commit hashes, timestamps, diff results) on the
design doc and the ticket's own log.

**All five acceptance criteria satisfied without a diff — a second
verification-only ticket on this instance, but not `ADR-001`'s reason.**
`aiorders-admin-hub` **is** registered (L1); a diff was the right mechanism
and one happened, just not from this ticket's own `building` state. Wrote
`ADR-003` (`aiorders-api` authoritative, `decided_by: approver`, recorded
retroactively) and `ADR-004` (extends `ADR-001`'s verification-ticket pattern
across this ticket's entire remaining lane in one ADR, `decided_by:
architect`) — explicitly engaging `ADR-001`'s own Review trigger for a second
occurrence and declining both alternatives it raises (internal-lane: admin-hub
fails the lane's own no-deploy-target test on the facts; G2 on the pattern:
premature at two occurrences with different causes). `in-security` is named
explicitly as real work here, not ceremony — five of the six files under this
ticket's history are the security surface itself. No one-way door — the
ownership move is an executed fact, not a pending decision; nothing to
escalate. Tech design at
`agents/architect/designs/ENG-004-admin-hub-migration-history.md`.
`agents/architect/decisions/_index.md` updated, Next ID now `ADR-005`.

**Three observations filed** (`agents/eng-manager/observations.md`), none
folded into this ticket's scope: `_eng/aiorders-api`'s worktree divergence
from `origin/main` (a future investigation trusting that worktree's files for
this repo would be wrong); admin-hub's `supabase/config.toml` still lists 20
orphaned `[functions.*]` stanzas for functions no longer in that repo;
and this ticket's whole subject having been resolved by the approver directly
mid-flight, named in `ADR-004`'s Review trigger as a pattern worth watching
for a second occurrence.

**Not proceeding into `ready` or `building` this pass, deliberately** — same
discipline `ENG-001`'s own history applied at this exact point (each of
`shaped→designed`, `designed→ready`, `ready→building` was its own separate
pass): work breakdown and the building-as-verification-record step are real,
distinct work reserved for their own sessions, and `ADR-004` leaves whoever
picks this up next everything needed to act without re-deriving it.
`machine_wip` (6) and the approval cap are both unaffected — `designed` isn't
in the counted range, no gate item was raised.

**Dead-end sweep (scoped to `ENG-004`, the ticket this event names):** its
log now ends in a valid, accounted-for state with a chain record below.
`ENG-003` (`awaiting-scope`) and `ENG-005` (`shaped`) untouched this pass —
out of scope for a `continue` event naming one ticket.

**Notify sweep:** no gate item written this pass — nothing to raise. No nudge
due (`ENG-003` already nudged once, 2026-08-26). Approval cap unchanged at
1/3 — not full, no stall alert.

`chained: ENG-004` — `designed`'s exit condition now met (design written,
ADRs logged, no one-way door outstanding), owned by `architect` handing to
`eng-manager` for work breakdown (agent, not the approver, not blocked, not
terminal). Fired `/bin/zsh departments/engineering/lib/eng-trigger.sh continue
ENG-004`. Post-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0,
clean.

## 2026-08-26 — decision: ENG-003's G1 rejected — dropped

`decision` event pass, context `2026-08-25-eng003-g1-scope.md` — narrow scope
per the event contract (act on the answered gate item and advance only the
ticket it belongs to; no board-wide sweep). Mode check clean (business-os
`.env` → `MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`:
exit 0, clean.

**Gate return: `ENG-003`'s G1 answered — rejected.** Hand-edited directly
(frontmatter `decision:`/`decided:` set, a second `## Decision` section
appended below the still-blank original placeholder) rather than through
`lib/eng-notify.sh`'s reply channel — fourth such occurrence today,
after `ENG-002`'s GitHub merge, `ENG-001`'s G3, and `ENG-004`'s G1 (decision
journal). `decided: 2026-08-27T06:38:51.515614+00:00`
(2026-08-26T23:38:51.515614-07:00 local). Verbatim answer, the only reason
given: "Drop this ticket do not  need to be done." **First outright G1
rejection this department has recorded** — every prior G1 (`ENG-002`,
`ENG-004`) was approved as scoped.

**Advanced `ENG-003` `awaiting-scope → dropped`, owner `eng-manager` — no
other transition is available at a killed G1.** PRD `status: rejected`
(`agents/product-manager/specs/ENG-003-aiorders-env-hygiene.md`, `##
Decision` filled in). Gate item moved to
`inbox/_handled/2026-08-25-eng003-g1-scope.md` unedited. Journaled in
`agents/eng-manager/config/decision-journal.md`, including a
grounded-but-labelled-as-interpretation read: the PRD's own Problem section
already noted the tracked `.env` values are public-by-design in the shipped
bundle regardless of git tracking, so the git-hygiene fix may have read as
low-value on its own once separated from the Maps-key question it couldn't
resolve anyway — not confirmed, not asked. Flagged there as a relevant prior
data point for the still-open `restaurant-portal` `.env` proposal
(`proposals.md`, 2026-08-26 row, same fix family) whenever that batch reaches
the approver — not acted on now, since an unapproved proposal is a separate
decision on its own timeline. `depends_on`/`blocks` both empty on `ENG-003`
— no other ticket affected by the drop.

**Consequence:** approval cap 1/3 → 0/3; approver-facing WIP 1 → 0. Nothing
dispatched onto the freed capacity this pass — out of scope for a `decision`
event scoped to the one gate item it answers, same restraint prior passes
applied to the same situation.

**Notify sweep:** no gate item written this pass (one was consumed, none
raised) — nothing to `raise`. No nudge due — the only open item was this one,
now answered. Approval cap dropped, not filled — no stall alert.

**Dead-end sweep (scoped to `ENG-003`, the ticket this event names):** its
log now ends in a valid, accounted-for state (`chained: none — dropped,
terminal`), written this pass. `ENG-004` and `ENG-005` untouched, out of
scope for this event.

`chained: none` — `ENG-003` is `dropped`, a terminal state; the chaining
guard never re-fires a terminal ticket. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

## 2026-08-26 — decision: ENG-004's G1 already resolved by the preceding watch pass — no-op

`decision` event pass, context `2026-08-25-eng004-g1-scope.md` — narrow scope
per the event contract (act on the answered gate item and advance only the
ticket it belongs to; no board-wide sweep). Mode check clean (business-os
`.env` → `MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`:
exit 0, clean.

**Gate return: already handled.** The named item was gone from `inbox/`
before this pass opened it — already at `inbox/_handled/2026-08-25-eng004-g1-scope.md`,
`decision: approved`, `decided: 2026-08-27T05:57:21.472123+00:00`. Per
`traces/eng-loop-2026-08-26.log`, the immediately preceding `watch` pass drained
in the same sequence with no gap (`pass end: watch (exit 0, 669s)` →
`draining queued event: decision (2026-08-25-eng004-g1-scope.md)`, same
second) and had already found this same hand-edited gate item and fully
processed it — see the entry directly above. Verified fresh rather than
trusted from that entry: PRD `status: approved` (`agents/product-manager/specs/ENG-004-*.md`),
the decision-journal row present, the ticket at `designed` owned by
`architect`, and the board's own In-flight row already correct. All four
consistent — nothing left to act on.

**Why both fired for one edit.** The approver answered by hand-editing the
gate item file directly — third such bypass of `lib/eng-notify.sh`'s reply
channel in two days (decision journal) — which changes a file inside a
watched `inbox/`. That one edit is visible to both the poll-detected
`decision` path and the raw file-watch `watch` path, and
`schedules/eng_build_loop.md`'s queue dedup only collapses identical
`<event> <context>` lines, so `decision (2026-08-25-eng004-g1-scope.md)` and
`watch (launchd)` never recognize each other as the same work. Whichever
drains first does it; the loser — this pass — finds nothing. Logged as one
data point in `agents/eng-manager/observations.md` rather than proposed: a
first occurrence of this specific race, and distinct from the already-open
`.watch-seen` staleness proposal (that one is watch-after-non-watch; this is
decision-vs-watch on the same edit).

**Dead-end sweep (scoped to `ENG-004`, the ticket this event names):** its
log already ends in a valid, accounted-for state (`chained: ENG-004`,
written by the preceding pass) — not a dead end, nothing to resume.
`ENG-003` and `ENG-005` untouched, out of scope for this event.

**Notify sweep:** nothing to raise (no gate item written this pass); no
nudge due (`ENG-003` already nudged once, 2026-08-26). Approval cap and WIP
unchanged — no stall alert.

No ticket transition made this pass, so no new entry on `ENG-004`'s own log —
its log already ends in a correct, unbroken chain record and this pass added
no new fact beyond confirming that record still holds. Approver-facing WIP
unchanged at 1 (`ENG-003` only), approval cap unchanged at 1/3, machine WIP
unchanged at 0/6. `chained: none` — `continue ENG-004` is already queued
(`traces/.pending`: `1 watch launchd` / `1 continue ENG-004`) from the
preceding pass's own chain fire; re-firing it here would only append a
duplicate line that the queue's own dedup collapses back to one at its next
pop, spending a fire for no additional effect. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean, unchanged.

## 2026-08-26 — watch: ENG-004's G1 answered by direct file edit — handed to the architect

`watch` (launchd) pass — a file changed in a watched inbox outside the
notify/poll channel. Mode check clean (business-os `.env` → `MODE=active`).
Pre-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Swept all three watched inboxes**, per the event's own narrower contract.
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` empty
(`.gitkeep` only); `inbox/requests/` empty. `inbox/` held two items:
`2026-08-25-eng003-g1-scope.md` — read fresh, still blank, still just the
2026-08-26 nudge from a prior pass, nothing new — and
`2026-08-25-eng004-g1-scope.md` — **answered** since the last pass touched
it (the `decision` pass immediately above this entry closed `ENG-001`'s G3
only and left this item untouched).

**Gate return: `ENG-004`'s G1 approved**, `decided:
2026-08-27T05:57:21.472123+00:00` (2026-08-26T22:57:21-07:00 local), no
additional comment. Answered by directly hand-editing the gate item file —
frontmatter `decision:`/`decided:` set and a second `## Decision` section
appended below the still-blank original placeholder — rather than through
`lib/eng-notify.sh`'s reply channel; third such occurrence in two days after
`ENG-002`'s GitHub merge and `ENG-001`'s G3 (decision journal). PRD `status:
approved`; gate item moved to `inbox/_handled/` unedited, same treatment as
`ENG-001`'s G3; journaled in `agents/eng-manager/config/decision-journal.md`.

**Advanced `ENG-004` `awaiting-scope → designed`, owner `architect` —
handoff only, design work not started this pass.** `designed`'s exit
condition for this ticket is a live-database investigation (confirm
`admin-hub`'s Supabase project linkage, read the live migration ledger,
content-diff six files against `aiorders-api`'s nine), not a light design
choice — real work against a project with live operator/customer data,
same class of thing `schedules/eng_build_loop.md`'s Cadence section reserves
`building` for. Left it for a dedicated `continue ENG-004` session rather
than folding it into this narrowly-scoped `watch` pass. Full reasoning on
the ticket's own log.

**Consequence:** approval cap 2/3 → 1/3 (`ENG-003` G1 only); approver-facing
WIP 2 → 1. Not spent on anything else this pass — dispatching the freed
capacity onto another ticket (e.g. raising `ENG-005`'s G1) is left for the
next `scheduled`/`watch`/`continue` pass, same restraint the preceding
`decision` pass applied to this exact situation.

**Notify sweep:** no gate item written this pass (one was consumed, none
raised) — nothing to `raise`. No nudge due: `ENG-003` was already nudged
once, 2026-08-26, and a nudge fires at most once per item. Approval cap
dropped, not filled — no stall alert.

**Dead-end sweep (scoped to `ENG-004`, the ticket this event unblocked):**
its log now ends in a valid, accounted-for state with a chain record below.
`ENG-003` (`awaiting-scope`) and `ENG-005` (`shaped`) untouched this pass —
both already correctly waiting on the approver or the next `scheduled`/`watch`
sweep, neither a dead end.

`chained: ENG-004` — sitting at `designed`, owned by `architect` (an agent,
not the approver, not blocked, not terminal). Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-004` for
the dedicated investigation-and-design session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

## 2026-08-26 — decision: ENG-001's G3 approved — the seed ticket reaches `verified`

`decision` event pass — narrow scope per the event contract (act on the
answered gate item in `inbox/` and advance only the ticket it belongs to; no
board-wide sweep). Mode check clean (business-os `.env` → `MODE=active`).
Pre-pass `departments/engineering/lib/eng-gate-check.sh` (whole board and
`ENG-001`-scoped): exit 0, clean.

**Gate return: `ENG-001`'s G3**
(`inbox/2026-08-26-eng001-g3-verification.md`) **answered — approved**, no
additional comment, `decided: 2026-08-27T05:05:01.598404+00:00`. Per
`ADR-002`, advanced `awaiting-release → shipped → verified`, 2 transitions.
Acted as devops at `shipped`: recorded the G3 confirmation in place of a
deploy, logged on the ticket; no release record fabricated at
`agents/devops/releases/` for a deploy that never happened, per `ADR-002`'s
own instruction. Acted as product-manager at `verified`: re-confirmed all
four acceptance criteria fresh against disk (registry, worktrees, gate-check,
`ENG-002`'s own `verified` state) and re-opened all three existing receipts
(`agents/principal-engineer/reviews/ENG-001.md`,
`agents/qa/test-plans/ENG-001.md`, `agents/security/reviews/ENG-001.md`) to
confirm each still reads `pass` rather than citing the prior hop's numbers.
Full detail on the ticket's own log. Gate item moved to
`inbox/_handled/2026-08-26-eng001-g3-verification.md` unedited — the approver
filled in `## Decision` directly this time. Journaled in
`agents/eng-manager/config/decision-journal.md`.

**This closes the seed ticket.** All four acceptance criteria hold, every
lane receipt is on file and independently re-verified more than once,
`ADR-001`/`ADR-002` stay on record for the next instance's own seed ticket.
`ENG-001` is off the In-flight table, terminal.

**Consequence, not an action this pass:** approval cap drops 3/3 → 2/3
(`ENG-003`+`ENG-004` G1s only); approver-facing WIP drops 3 → 2, back at the
soft limit rather than over it. Dispatching any newly-freed capacity onto
another ticket (e.g. a G1 slot for `ENG-005`) is left for the next
`scheduled`/`watch`/`continue` pass — out of scope for a `decision` event
scoped to the one gate item it answers.

**Dead-end sweep (scoped to this ticket, per the event's own narrower
contract):** `ENG-001`'s log now ends in a valid, accounted-for state
(`chained: none — verified, terminal`). Other in-flight tickets untouched.

`chained: none` — `ENG-001` is `verified`, a terminal state; the chaining
guard never re-fires a terminal ticket. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean (whole board).

## 2026-08-26 — watch: swept all three inboxes again, nothing new — fourth occurrence of the self-inflicted no-op pattern

`watch` (launchd) pass — drained immediately behind the `scheduled`
safety-net sweep directly above: that pass ended 15:48:00 and this one began
draining the same second, after the queue collapsed 2 duplicate `watch`
events into one (`traces/eng-loop-2026-08-26.log`). Per the event's own
narrower contract, swept only `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/` and `inbox/`, acting on whatever is new. Mode
check clean (business-os `.env` → `MODE=active`). Pre-pass
`lib/eng-gate-check.sh`: exit 0, clean.

**Swept all three inboxes; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` holds
exactly the three items already on the board's "Waiting on the approver"
list, and all three are exactly as the immediately-preceding `scheduled`
pass left them seconds earlier — read fresh, not trusted from the board
header: `2026-08-26-eng001-g3-verification.md` (`## Decision` blank,
raised/notified `2026-08-26T15:43:11`), `2026-08-25-eng003-g1-scope.md` and
`2026-08-25-eng004-g1-scope.md` (both `## Decision` blank, both `nudged:
2026-08-26T15:43:45`). Nothing new to act on.

**Notify sweep:** no nudge due — `ENG-001`'s G3 is minutes old; `ENG-003`/
`ENG-004` were each nudged exactly once, seconds ago, by the pass
immediately before this one, and a nudge fires at most once per item.
Approval cap unchanged at 3/3, same composition the `scheduled` pass already
reasoned about (not a fresh stall) — no new stall alert.

**Fourth occurrence of the pattern `proposals.md` already carries a full
root-cause diagnosis for** — filed as a proposal by the `watch` pass two
entries above this one (itself the third occurrence, after two
`observations.md` rows on 2026-08-25 and 2026-08-26 10:13). Mechanism
unchanged from that proposal's own account: `commit_watch_fingerprint()` in
`lib/eng-trigger.sh` only stamps `.watch-seen` on an `$EVENT=watch` pass, so
the G3 raise and the two nudges the `scheduled` pass just wrote to `inbox/`
changed the three watched inboxes' fingerprint without updating
`.watch-seen` — guaranteeing this fire would see "something changed" and
find nothing left to do, exactly as it did. Not refiled as a new proposal or
observation: a fifth data point on an already-diagnosed, already-proposed
issue is corroboration, not a new finding, and refiling it risks the
"proposal batch becomes unreadable" failure mode `schedules/eng_build_loop.md`
step 8b warns against. Left for the approver's existing G1 batch to resolve.

No ticket was touched this pass, no ticket state changed, no gate item was
written, nothing to journal. `chained: none` — this pass advanced no
ticket, so there is no hop of its own to fire, and every in-flight ticket
(`ENG-001` awaiting-release, `ENG-003`/`ENG-004` awaiting-scope, `ENG-005`
shaped) is already correctly waiting on the approver or a WIP/approval cap,
none of which a machine can clear. Approver-facing WIP unchanged (3, still
over the 2 soft limit, still harmless per the header note), approval cap
unchanged at 3/3, machine WIP unchanged at 0/6. Post-pass
`lib/eng-gate-check.sh`: exit 0, unchanged.

## 2026-08-26 — scheduled: safety-net sweep — ENG-002's out-of-band merge reconciled, ENG-001's G3 raised, two G1s nudged

`scheduled` (launchd) pass — the twice-daily safety-net sweep. Mode check
clean (business-os `.env` → `MODE=active`; instance `config.yaml` → `mode:`
empty, falls through). Pre-pass `lib/eng-gate-check.sh`: exit 0, clean.
Confirmed this pass's own lock (`traces/.loop.lock`, pid of this chain's
`eng-trigger.sh scheduled launchd` invocation) is legitimately its own, not a
collision.

**Business/technical intake:** `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/` and `inbox/requests/` all empty — nothing new to
shape or propose.

**Gate returns / merge detection, combined — `ENG-002` found already marked
`shipped` by a direct "control center" edit, ancestry not yet consulted.**
The ticket's own log said so explicitly. Independently re-ran the loop's own
merge-detection check from scratch in the department's worktree
(`~/Documents/projects/_eng/restaurant-portal`, never the human's checkout):
`git fetch origin` → `33c5de6..b3a81ef main -> origin/main`;
`git merge-base --is-ancestor chore/ENG-002-smoke-test-harness origin/main` →
merged; `git diff` between the branch tip and `origin/main` → empty (no
intervening commits on `main`). The control center's claim held up.
`inbox/2026-08-26-eng002-merge-request.md`'s `## Decision` was never actually
filled in — the approver merged directly on GitHub instead, an alternative
the item's own text offered. Treated the merge as the answer: filled the
item's Decision with what happened, moved it to `inbox/_handled/`, and
journaled it (`agents/eng-manager/config/decision-journal.md`) — flagging
that the tracked channel was bypassed, worth watching for a repeat.

**Closed out `ENG-002` (`shipped → verified`).** Acted as devops for the
`shipped` exit condition the control-center edit had skipped: confirmed
`restaurant-portal` has no push-to-`main` CI/CD (`deploy-cf` is a manual
`wrangler pages deploy` script; no `.github/workflows/`), and this ticket's
diff (`devDependency`s + test files) never reaches Vite's build graph —
re-ran `npm run build` on the merged tree and confirmed the `dist/` output is
unchanged in shape. Nothing to deploy, so `npm run deploy-cf` was
deliberately not run. Wrote the release record from what was actually found
(`agents/devops/releases/2026-08-26-restaurant-portal-ENG-002.md`). Then
acted as product-manager: re-ran `npm test` on the merged tree (1 passed),
re-checked `config/projects.md`'s Commands table on disk (present), and
updated `agents/qa/test-plans/ENG-002.md`'s AC3 from `pending` to `pass` —
all four acceptance criteria now confirmed against the live, merged thing.
Full detail on the ticket's own log. **`ENG-002` no longer counts against the
approval cap** — the third of 3/3 is now open.

**Dispatch: `ENG-001` `ready-to-ship → awaiting-release`, 1 transition.**
With the cap at 2/3 (`ENG-003`+`ENG-004` G1s only), raising `ENG-001`'s G3 —
an already-in-flight ticket reaching its own next gate, not a new start — is
legal per the Guards section, the same reasoning `ENG-002`'s own history used
at 2/3→3/3 earlier. Wrote the G3 item per `ADR-002`'s framing (confirm the
record, not "ship to production" — nothing is being deployed) at
`inbox/2026-08-26-eng001-g3-verification.md` and raised it. Approval cap is
back to 3/3 (full) — `ENG-003`, `ENG-004`, and this G3 — a different
composition than before, not a fresh stall (the board was never observed as
anything but full/near-full by any pass boundary in between, so no new stall
alert sent; one was already sent for the ongoing episode and is the known
no-op `MODE`-collision bug). Machine WIP now 0/6 — nothing left in the
`ready`..`ready-to-ship` range.

**Notify sweep — two nudges due.** `ENG-003` (notified 2026-08-25T13:55:41)
and `ENG-004` (notified 2026-08-25T14:55:55) had both crossed the 24h
threshold as of this pass (15:43 local) — the immediately-preceding passes checked
this correctly and found both still under 24h at the time; time alone closed
the gap, which is exactly what a `scheduled` safety-net sweep exists to
catch between local events. Ran `lib/eng-notify.sh nudge` on both, stamped
`nudged:` on each by hand (the script's known `MODE`-collision bug means its
own log line reads `sent: active` rather than `sent: nudge` — reproduced
here too, corroborating the existing proposal, not a new finding).

**One proposal filed** (`proposals.md`): the general gap this pass's
`ENG-002` reconciliation exposed — a ticket's `state:` can move out from
under an open gate item via the control center, and nothing currently
cross-checks the two automatically; this pass only caught it by chance while
re-deriving `ENG-002`'s status for other reasons. Sized `S` — the check
itself (for every open gate item, confirm the ticket it names is still
actually at the state the item implies) is cheap; a repeat occurrence would
make this worth acting on.

**Dead-end sweep:** every in-flight ticket's log now ends in a valid,
accounted-for state. `ENG-001` — `chained: none`, `awaiting-release`, owner
`approver`. `ENG-002` — `chained: none`, `verified`, terminal. `ENG-003`/
`ENG-004` — unchanged, waiting on the approver, both now nudged.
`ENG-005` — unchanged, `chained: none — held by the WIP cap`
(`wip.approver_limit` 2/2, `ENG-003`+`ENG-004` still open; freeing the
approval cap doesn't free this one, since it's a distinct, smaller cap that
was already full before `ENG-002` ever blocked on it). No broken chains
found; `agents/eng-manager/config/exceptions.md` empty; nothing past the
30-day proposal expiry.

Post-pass `lib/eng-gate-check.sh`: exit 0, clean (checked after each of the
`ENG-002` and `ENG-001` edits individually, and once more for the whole
board at the end).

## 2026-08-26 — watch: swept all three inboxes, nothing new to act on

`watch` (launchd) pass — fired by the file-watcher on a change to one of the
three watched inboxes. Per the event's own narrower contract, this sweeps
`agents/product-manager/inbox/`, `agents/eng-manager/inbox/` and `inbox/`
only, acting on whatever is new; the board-wide version of dispatch/merge-
detection/dead-end-sweep is the twice-daily `scheduled` pass's job, not
this one's. Mode check clean (business-os `.env` → `MODE=active`). Pre-pass
`lib/eng-gate-check.sh`: exit 0, clean.

**Swept all three inboxes; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` itself
holds exactly the three items already on the board's "Waiting on the
approver" list, and all three still read `## Decision` / "Filled in by the
approver," unanswered — `2026-08-26-eng002-merge-request.md`,
`2026-08-25-eng003-g1-scope.md`, `2026-08-25-eng004-g1-scope.md`. The
merge-request file is the one genuinely new artifact since the last board
entry (written 11:01 by the immediately-preceding `continue ENG-002`
pass), but that same pass had already raised it (`notified:
2026-08-26T11:01:46`) and reflected it on the board — nothing was left
unprocessed for this pass to act on. Cross-checked against
`traces/.watch-seen` (fingerprint last stamped 10:20, before the file's
11:01 creation) and `traces/eng-loop-2026-08-26.log`: this `watch` fire is
that same write being independently observed by the file-watcher, not a
second, unhandled change — consistent with the fingerprint changing and
the fire not being deduplicated above the lock.

**Notify sweep:** neither `ENG-003` nor `ENG-004`'s G1 has crossed the 24h
nudge threshold (notified 2026-08-25T13:55:41 / T14:55:55, both still under
24h as of this pass). The approval cap reached 3/3 (full) during the
immediately-preceding `continue ENG-002` pass and no stall alert had been
sent for that stall, so ran `lib/eng-notify.sh stall` per step 7 — it is
still the known-broken no-op filed 2026-08-25 (`proposals.md` row 2, the
`MODE`-variable collision with the sourced business-os `.env`): logged
`no such item:` and sent nothing. Corroborating evidence for the existing
proposal, not a new finding.

**Merge detection, board-wide dispatch, and the full dead-end sweep are out
of scope for this event** — `watch` only unblocks the inbox sweep above.
Spot-checked only what bears on the one new file: `ENG-001`'s own
`continue` chain, fired by its own immediately-preceding pass, is intact
and queued at the front of `traces/.pending`, unaffected by this pass.

**One proposal filed** (`proposals.md`): this is the third occurrence of
the no-op-`watch` pattern `observations.md` flagged twice already
(2026-08-25, 2026-08-26 10:13) and explicitly deferred to a proposal "if it
recurs." Traced the actual mechanism this time, in `lib/eng-trigger.sh`:
`commit_watch_fingerprint()` and the `WATCH_FP` capture both key off
`$EVENT = "watch"` specifically, so a gate item raised by a `continue` or
`scheduled` pass changes the watched inboxes' fingerprint but never updates
`.watch-seen` — guaranteeing the next `watch` fire sees "something changed"
and spends a full pass finding nothing, exactly what happened here
(`.watch-seen` stamped 10:20; `continue ENG-002` raised its merge request
at 11:01; this pass is the predictable result). Not fixed inline — it's
department machinery, self-discovered, so `schedules/eng_build_loop.md`
step 3 routes it to the proposal list, not a drive-by patch.

No ticket was touched this pass, no ticket state changed, no gate item was
written, nothing to journal. `chained: none` — this pass advanced no
ticket, so there is no hop of its own to fire; `ENG-001`'s separately-queued
`continue` (from its own prior pass) runs next regardless, once this pass
exits. Approver-facing WIP unchanged (3, still over the 2 soft limit, still
harmless per the header note), approval cap unchanged at 3/3, machine WIP
unchanged at 1/6. Post-pass `lib/eng-gate-check.sh`: exit 0, unchanged.

## 2026-08-26 — continue ENG-001: ADR-002 resolved the release/G3 question, reached ready-to-ship, held there by the approval cap

`continue ENG-001` event pass — narrow scope per the event contract (resume
the named ticket from its current state; no board-wide sweep). Mode check
clean (business-os `.env` → `MODE=active`). Pre-pass `lib/eng-gate-check.sh`
(whole board and `ENG-001`-scoped): exit 0, clean. Fresh sweep of all three
inboxes found nothing pending for `ENG-001`.

**Resolved the boundary the immediately-preceding pass named and stopped
at.** That pass reached `in-security` with a **pass** verdict already on
record, but declined to guess what `ready-to-ship`/`awaiting-release`/
`shipped` mean for a no-deploy verification ticket, since `ADR-001`'s
Decision text names `building` through `in-security` specifically and never
further. Acting as architect, wrote `ADR-002`
(`agents/architect/decisions/ADR-002-verification-ticket-release-and-g3.md`):
a verification ticket owes every remaining full-lane state exactly as any
other ticket — `ready-to-ship`, G3, `shipped`, and `verified` are none of
them skipped or auto-routed by inventing an autonomy level `aiorders` was
never granted (re-confirmed fresh: `config/projects.md` still only the five
app repos at **L1**, `config/internal-projects` still empty). Only the
*content* of each state changes, continuing `ADR-001`'s own pattern —
`ready-to-ship` records devops confirming nothing to release; G3 asks the
approver to confirm the ticket's record rather than approve a deploy that
doesn't exist; `shipped` records that confirmation, not a fabricated
release. G3 is deliberately **not** waived or downgraded to L3's
notify-after treatment: `docs/engineering-team.md` reserves "say yes to
production" to the approver, department-wide, and unlike `building`'s empty
`branch:` field, removing a human checkpoint isn't a reversible logging
convention — see the ADR's own reasoning for why this isn't the same kind of
call `ADR-001` made. No G2 raised. `agents/architect/decisions/_index.md`
updated, Next ID now `ADR-003`.

**Dispatch: `in-security → ready-to-ship`, 1 transition.** Acted as devops
per `ADR-002`: confirmed and logged, not skipped, that no release plan,
rollback, or observability plan exists because no registered project carries
a diff for this ticket — re-verified `config/projects.md` (five rows, all
L1) and `_eng/` (all five worktrees present) fresh rather than citing the
`in-security` hop's numbers. Release window checked for consistency with
today's `ENG-002` hop even though nothing deploys: Wednesday, no
`ENG_RELEASE_FREEZE` — clean, moot either way.

**Not proceeding into `awaiting-release`.** The approval cap is **3/3
(full)** — re-checked fresh, not from this board's cached header:
`inbox/2026-08-26-eng002-merge-request.md`,
`inbox/2026-08-25-eng003-g1-scope.md`, and
`inbox/2026-08-25-eng004-g1-scope.md` all still read "Filled in by the
approver.", unanswered, and `config/config.yaml` confirms `wip.approval_cap:
3` rather than assuming the board header is current. Per the Guards section,
"at the cap, nothing advances into a gate state" — `awaiting-release` is
exactly that, so the G3 item `ADR-002` calls for is not raised this pass.

**`chained: none` — held by the approval cap (3/3, full), not by anything
left for this ticket to decide.** Unlike every earlier stop on this ticket,
this one isn't an undecided question a fresh pass could resolve: all four
acceptance criteria are satisfied, `ADR-002` has settled what every
remaining state means, and devops's own confirmation is done. Nothing
machine-ownable remains until a slot frees. Re-firing `continue ENG-001` now
would only re-derive this same conclusion at the cost of a full pass — the
chaining guard's own list names this condition directly ("held by a cap
(WIP or approvals)"). Resumes at the next `scheduled` safety-net sweep, or a
direct re-fire once the approver clears one of the other three open items.

No gate item raised this pass; nothing to notify. Machine WIP unchanged at
1/6 (`ready-to-ship` is still inside the counted `ready`..`ready-to-ship`
range). Approval cap unchanged at 3/3 — this pass created no new gate item.
**Dead-end sweep (scoped to this ticket, per the event's own narrower
contract):** `ENG-001`'s log now ends in a valid, accounted-for state
(`chained: none`, reason given). Other in-flight tickets untouched. Post-pass
`lib/eng-gate-check.sh`: exit 0, unchanged.

## 2026-08-26 — continue ENG-001: combined review+quality+security hop, stopped short of ready-to-ship

`continue ENG-001` event pass — narrow scope per the event contract (resume
the named ticket from its current state; no board-wide sweep). Mode check
clean (business-os `.env` → `MODE=active`; instance `config.yaml` → `mode:`
empty, falls through). Pre-pass `lib/eng-gate-check.sh`: exit 0, clean.
Fresh sweep of all three inboxes found nothing pending for `ENG-001`.

**Dispatch: `building → in-review → in-security`, 2 transitions.** Acted as
principal-engineer and qa on the combined review+quality hop (step 6):
independently re-derived all four acceptance criteria against disk this
round rather than citing prior numbers — `config/projects.md` (AC1),
`_eng/` worktrees plus `git rev-parse` in each to confirm they're real,
resolvable checkouts (AC2), a fresh `lib/eng-gate-check.sh` run (AC3), and
`ENG-002`'s own board file, now at `blocked` with an open PR — several
states past AC4's literal bar (AC4). Verdict **pass**;
`agents/principal-engineer/reviews/ENG-001.md` and
`agents/qa/test-plans/ENG-001.md` written, `links.review`/`links.test_plan`
set. Acted as security: threat model, full OWASP walk (all ten `n/a` — no
code, dependency, endpoint, or config surface exists), secret-scanned this
ticket's entire paper trail (one prose hit, not a credential). Verdict
**pass**; `agents/security/reviews/ENG-001.md` written, `links.security_review`
set. Full detail on the ticket's own log.

**Not proceeding into `ready-to-ship`, for two independent reasons.** What
`ready-to-ship`/`awaiting-release`/`shipped` mean for a no-deploy
verification ticket is a real open question `ADR-001` does not cover — its
Decision text names `building` through `in-security` specifically, never
further, and the design doc's brief Rollout note was never weighed as a
considered decision the way the ADR was. Improvising it here would repeat
the exact failure this ticket exists to prevent. Independently: the
approval cap is **3/3 (full)** right now — checked fresh this pass by reading each
of the three open items' `## Decision` sections directly (all still "Filled
in by the approver," unanswered) rather than trusted from this board's own
cached header — so reaching `awaiting-release` (a G3 this pseudo-project
cannot auto-route, being registered at no autonomy level) could not be
acted on regardless.

**Dead-end sweep (scoped to this ticket, per the event's own narrower
contract):** `ENG-001`'s log now ends in a valid, accounted-for state
(`chained: ENG-001`). Other in-flight tickets untouched — out of scope for a
`continue` event naming one ticket.

No gate item raised this pass; nothing to notify. Machine WIP unchanged at
1/6 (`in-security` is still inside the `ready`..`ready-to-ship` counted
range). Approval cap unchanged at 3/3 — this pass created no new gate item.
`chained: ENG-001` — sitting at `in-security`, owned by security (agent, not
approver, not blocked, not terminal); the full cap blocks the *next* hop's
gate, not this ticket's present state.

## 2026-08-26 — continue ENG-002: building finished, all three machine gates passed, PR open

`continue ENG-002` event pass — narrow scope per the event contract (resume
the named ticket from its current state; no board-wide sweep). Confirmed via
the trigger log this is exactly the dedicated continuation the safety-net
sweep directly below deferred, not a duplicate: that pass ended 10:44:34 and
this one began draining immediately after. Mode check clean (business-os
`.env` → `MODE=active`). Pre-pass `lib/eng-gate-check.sh` (whole board and
`ENG-002` scoped): exit 0, clean.

**`building → in-review → in-security → ready-to-ship → blocked`, 4
transitions (the per-ticket cap), landing exactly on the human gate.** Did
not take the prior pass's "self-tested" claim on faith: independently re-ran
`npm test` (1 passed), `npm run lint` (96 problems, identical on a clean
`origin/main` checkout via `git stash -u` — zero new), `npm run build`
(succeeds), and `npm audit` (37 vs. 39 on `main` — no new vulnerabilities);
traced the test's Supabase mock and its "Login" tab landmark through the
actual component chain rather than trusting the description. Committed the
five relevant files as `2703add`, pushed the branch. Acted as
principal-engineer (review pass, `agents/principal-engineer/reviews/ENG-002.md`)
and qa (wrote the test plan this ticket never had, `agents/qa/test-plans/ENG-002.md`,
suite green) on the combined review+quality hop; acted as security
(`agents/security/reviews/ENG-002.md`, OWASP walk mostly `n/a` for a dev-only
harness, dependency check clean); acted as devops at `ready-to-ship`
(upstream gates verified on disk, readiness held, `config/projects.md`'s
Commands table updated per the design's own assignment, window check clean —
Wednesday, no freeze). Opened the real PR
(https://github.com/harsimranwalia/restaurant-portal/pull/1) since
`restaurant-portal` is **L1**, wrote and raised the merge-request item
(`inbox/2026-08-26-eng002-merge-request.md`), landed at `blocked`,
`blocked_on: approver`. Full detail, including the approval-cap arithmetic
that justified proceeding while the board was already at 2/3, on the
ticket's own log.

**Approval cap now 3/3 (full)** — checked `config/config.yaml`'s actual
`wip.approver_limit`/`wip.awaiting_approver_cap` definitions rather than the
board header's prose: `approver_limit`'s only enforcement is blocking *new*
starts (already true at 2, still true at 3), and `awaiting_approver_cap` —
the guard `config.yaml` names explicitly for "an L1 PR waiting to be
merged" — had exactly one slot free. Machine WIP now 1/6 (`ENG-001` only).

This pass's own `lib/eng-notify.sh raise` call reproduced the already-filed
`MODE`-collision bug (`sent: active`, not `sent: raise`) — corroborating
evidence for the open 2026-08-25 proposal, not a new one.

**Dead-end sweep (scoped to this ticket, per the event's own narrower
contract):** `ENG-002`'s log now ends `chained: none` with the waiting-on-
approver reason. Other in-flight tickets untouched.

`chained: none` — `ENG-002` is `blocked`, `blocked_on: approver`. The whole
point of this hop was to reach that gate; nothing left for a machine to do
until the approver merges the PR or replies to the inbox item.

## 2026-08-26 — scheduled: safety-net sweep, board already mid-chain — nothing to dispatch

`scheduled` (launchd) pass. Mode check clean (business-os `.env` →
`MODE=active`; instance `config.yaml` → `mode:` empty, falls through).
Pre-pass `lib/eng-gate-check.sh`: exit 0, no violations.

Business intake: `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`
and `inbox/requests/` all empty — nothing new to shape or propose. Gate
returns: `ENG-003`/`ENG-004` G1s both still unanswered (`## Decision` blank
in both; notified 2026-08-25T13:55:41/T14:55:55, still under 24h as of this
pass [10:41] — no nudge due). Merge detection: no ticket `blocked` on an L1
PR, no-op.

**Dispatch — reviewed all five in-flight tickets, advanced none.** `ENG-001`
and `ENG-002` are both already mid-chain from the two dedicated `continue`
passes that ran in the hour before this one (`ENG-001` `ready→building` at
10:20–10:33; `ENG-002`'s uncommitted `building` work found and corrected at
09:56). Each ticket's own chain is already queued: `cat traces/.pending`
shows `continue ENG-002` then `continue ENG-001`, both appended by those
passes themselves, not by this one. Re-firing either here would duplicate an
already-queued line and, since this pass's own parent `eng-trigger.sh
scheduled launchd` (pid 37779, alive since 09:30) holds `traces/.loop.lock`
throughout, would contend a lock its own ancestor holds — the exact
situation two earlier passes today already hit and correctly avoided. Left
both untouched. `ENG-003`/`ENG-004` stay `awaiting-scope` — approver WIP
2/2 (full), both G1s unanswered. `ENG-005` stays `shaped`, held by the same
cap — no slot freed this pass.

**Notify sweep:** no gate item raised this pass, nothing to notify; neither
`ENG-003` nor `ENG-004` has crossed the 24h nudge threshold yet; approval cap
is 2/3, not full, so no stall alert.

**Dead-end sweep:** every in-flight ticket's log ends in a valid,
accounted-for state (`chained: <id>` or `chained: none — <reason>`); no
broken chain. `agents/eng-manager/config/exceptions.md` is empty (nothing at
a third occurrence); `proposals.md`'s three open items and
`observations.md`'s ledger are all within days of filing, none past the
30-day proposal expiry.

Approver-facing WIP unchanged at 2/2 (full), approval cap 2/3, machine WIP
unchanged at 2/6. `chained: none` on all five tickets — `ENG-001`/`ENG-002`
because a dedicated continuation is already queued for each (see above);
`ENG-003`/`ENG-004` because they wait on the approver; `ENG-005` because it's
held by the approver-WIP cap. Post-pass `lib/eng-gate-check.sh`: exit 0,
unchanged.

## 2026-08-26 — continue ENG-001: building-as-verification record written

`continue ENG-001` event pass — narrow scope per the event contract (resume
the named ticket from its current state; no board-wide sweep). Mode check
clean (business-os `.env` → `MODE=active`; instance `config.yaml` → `mode:`
empty, falls through). Confirmed no pending gate item for `ENG-001` in any of
the three inboxes before dispatching — none exists; its last judgement call
(what `building`/receipts mean for a diffless ticket) was decided directly by
the architect via ADR-001, no approver gate raised. Merge detection:
`ENG-001` carries no branch, no-op.

**Dispatch:** `ENG-001` advanced `ready → building` — the
building-as-verification-record step ADR-001 defines. Re-verified all four
acceptance criteria against disk rather than trusting prior citations: AC1
(`config/projects.md`, five rows, all **L1**), AC2 (`_eng/` worktrees, all
five present), AC3 (`lib/eng-gate-check.sh` re-run, exit 0), AC4 (`ENG-002`
now at `building`, already past `shaped`). Full citations on the ticket's
own log. `branch:` stays empty per ADR-001; `machine_wip` (6) unchanged at
2/6 (`ENG-001`, `ENG-002` — both already inside the counted range). **Not
proceeding into `in-review` this pass, deliberately** — the
principal-engineer/QA review of the verification claims is real, distinct
gate work reserved for its own session, same reasoning applied at every
earlier hop on this ticket. `chained: ENG-001`.

**Dead-end sweep (scoped to this ticket, per the event's own narrower
contract):** `ENG-001`'s log now ends in a valid, accounted-for state
(`chained: ENG-001`). Other in-flight tickets untouched — out of scope for a
`continue` event naming one ticket.

No gate item raised this pass; nothing to notify; nothing new to observe or
propose.

## 2026-08-26 — scheduled: safety-net sweep, ENG-002's building state corrected

`scheduled` (launchd) pass — twice-daily safety-net sweep, drained
immediately behind this morning's `continue ENG-002` build hop under the
same lock (pid 37779, 09:30 launchd fire). Mode check clean (business-os
`.env` → `MODE=active`; this instance's own `config.yaml` → `mode:` empty,
falls through). Business intake: `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/` and `inbox/requests/` all empty — nothing new to
shape or propose. Gate returns: `ENG-003`/`ENG-004` G1s both still
unanswered (`## Decision` blank in both inbox items; notified
2026-08-25T13:55/14:55, both under 24h as of this pass — no nudge due yet).
Merge detection: no ticket `blocked` on an L1 PR, no-op.

**Dispatch (priority order `now` → empty):** `ENG-001` reviewed and left
unchanged — still `ready`, its `continue` already queued
(`traces/.pending`) from an earlier pass, nothing to redo. `ENG-002`
reviewed and found mid-flight: the `continue ENG-002` hop that ran
09:36–09:56 just before this pass implemented the smoke test for real
(Vitest + RTL, per the architect's design) but stopped itself uncommitted,
citing a suspected concurrent instance of this automation — which this pass
independently re-checked via `ps` and the lock file and found to be false
(pid 37779 is this exact chain's own orchestrator; no other process
touches this instance or the `restaurant-portal` worktree). Full forensics
on that ticket's own log. Corrected the board to `state: building` and
`branch: chore/ENG-002-smoke-test-harness` to match the real, verified,
on-disk work; left the worktree exactly as found per `config/projects.md`'s
own rule against touching a previous pass's uncommitted state; filed the
`.env`-tracked finding that pass discovered but didn't get to
(`proposals.md`); did not commit/push/finish the build myself — that stays
reserved for a dedicated `continue` session, same reasoning already applied
to every other `ready`→`building` transition on this board. `ENG-003`/
`ENG-004` stay `awaiting-scope` (approver WIP 2/2, both gates unanswered);
`ENG-005` stays `shaped`, held by the same cap — no slot freed this pass.

**Dead-end sweep:** every in-flight ticket's log ends in a valid,
accounted-for state (`chained: <id>` or `chained: none — <reason>`) —
`ENG-002`'s is the one this pass brought current; `ENG-001`, `ENG-003`,
`ENG-004`, `ENG-005` were already correct and untouched. One observation
filed (`observations.md`): a second occurrence of the `scheduled`-event-
with-a-ticket-path-context oddity first seen 2026-08-25, with a correction
to that earlier note — it does charge a ticket's hop counter (`ENG-001`
this time), not ticket-less as previously assumed.

Approver-facing WIP unchanged at 2/2 (full), approval cap 2/3, machine WIP
unchanged at 2/6. `chained: ENG-002` (fired `/bin/zsh eng-trigger.sh
continue ENG-002` — queued behind this pass's own lock, next drain runs
it). `ENG-001`/`ENG-003`/`ENG-004`/`ENG-005`: `chained: none`, all for
reasons unchanged from their own last log entries.

## 2026-08-25 — continue ENG-001: architect resolved the building/receipts gap

`continue ENG-001` pass — the dedicated hop chained by the earlier PM-shaping
pass; the intervening `scheduled (manual-unblock)` sweep and its retry (both
below/archived) deliberately left this ticket alone because this `continue`
was already queued for it.

Architect resolved the question the PM pass raised: what `building` and the
three full-lane receipts mean for a ticket with no application-code
deliverable. Wrote `ADR-001`
(`agents/architect/decisions/ADR-001-verification-ticket-building-and-receipts.md`)
and a short tech design
(`agents/architect/designs/ENG-001-register-repos-and-prove-the-loop.md`): a
**verification ticket** — every acceptance criterion satisfied with no diff
in any registered project — still owes every state and every receipt its
lane specifies, but `building` records what was checked instead of a
branch/PR. Considered and rejected registering `aiorders` in
`config/internal-projects` (reserved to the approver by that file's own
header, and premature for what's expected to be a one-time ticket) and
delegating via `parent:` to `ENG-002` (would misrepresent its real,
independent provenance). No one-way door; decided directly, no G2, no
approver touch — `ENG-003`/`ENG-004` keep both approver-WIP slots
undisturbed.

**Dispatch:** `ENG-001` advanced `shaped → designed → ready`. EM work
breakdown found zero implementation units (no code in any registered
project), so nothing to sequence; `machine_wip` (6) now 2/6 (`ENG-002`,
`ENG-001`). **Stopped before `building`, deliberately** — writing the three
receipts against the verification evidence is real, distinct gate work that
`schedules/eng_build_loop.md` reserves for its own session, same reasoning as
`ENG-002` earlier today. `chained: ENG-001`.

**Merge detection:** no ticket is `blocked` on an L1 PR. No-op.

**Dead-end sweep:** every in-flight ticket's log ends in a valid,
accounted-for state (`chained: <id>` or `chained: none — <reason>`); no
broken chain found.

## 2026-08-25 — scheduled (manual-unblock), retry: ENG-002 gate processed, ENG-004 G1 raised

**This pass is the retry (attempt 2/2) of the `scheduled (manual-unblock)`
event below** — the first attempt timed out at the 1800s pass ceiling while
finishing the board-index edit for the entry directly below this one (see
`traces/eng-loop-2026-08-25.log`: `pass TIMED OUT after 1800s`, re-queued as
attempt 2/2). Before doing anything new, verified the first attempt's
substantive work — `ENG-003`/`ENG-004`/`ENG-005` shaped, `ENG-003`'s G1
raised, two proposals and three observations filed — was complete and
internally consistent on disk; the only gap found was this table missing rows
for the three new tickets, now fixed. Filed one further observation on the
timeout itself (`agents/eng-manager/observations.md`).

**Gate returns:** `ENG-002`'s G1 was answered — **approved**, no additional
comment — while this retry was starting (`decided: 2026-08-25T21:43:57Z`).
Processed it: gate item moved to `inbox/_handled/`, PRD `status: approved`,
entry added to `agents/eng-manager/config/decision-journal.md`. A dedicated
`decision 2026-08-25-eng002-g1-scope.md` event is separately queued
(`traces/.pending`) from the control center's own fire — when it eventually
drains it will find the gate already resolved and be a harmless no-op.
`ENG-003`'s G1 remains unanswered; left as-is.

**Dispatch:** `ENG-001` left alone, same reasoning as the pass below — its
`continue` is still independently queued (`traces/.pending`), so re-opening
the architect's deferred judgement call here would race a pass already
in flight for it. `ENG-002` advanced `awaiting-scope → designed → ready`:
architect design written
(`agents/architect/designs/ENG-002-restaurant-portal-smoke-test-harness.md`
— Vitest + React Testing Library, one smoke test on the real app entry
point; no one-way door, no ADR, no G2); EM sequencing found a single unit of
work and `machine_wip` (6) at 0/6 going in. **Stopped before `building`,
deliberately** — this pass is a recovery/sweep context, not the clean session
`schedules/eng_build_loop.md` reserves for "an engineer writing code," so the
actual implementation is left for a dedicated `continue` hop. `chained:
ENG-002`.

Resolving `ENG-002`'s gate freed the `wip.approver_limit` (2) slot it had
been holding alongside `ENG-003`. Took the freed slot for `ENG-004` over
`ENG-005` — both still `shaped` with no `priority` set, so severity is the
tie-break (`P2` vs `P3`), per `config/definition-of-done.md`. `ENG-004`'s G1
raised and notified; PRD `status: awaiting-scope`. `ENG-005` holds at
`shaped` — approver WIP is 2/2 (full) again with `ENG-003` + `ENG-004`.

**Merge detection:** no ticket is `blocked` on an L1 PR. No-op.

**Dead-end sweep:** every in-flight ticket's log ends in a valid, accounted-for
state (`chained: <id>` or `chained: none — <reason>`); no broken chain found.

## 2026-08-25 — scheduled (manual-unblock), attempt 1: swept the three unshaped requests

`scheduled (manual-unblock)` pass — the safety-net sweep queued behind the
`continue ENG-001` pass earlier today. Per the event's own scope ("sweep the
whole board: everything a local event cannot see"), left `ENG-001` alone —
its `continue` was already queued (`traces/.pending`) from that earlier
pass's own chain, so redoing its architect-judgement question here would
have raced a pass already in flight for it. Confirmed nothing is `blocked`
on an L1 PR (merge detection: no-op this pass) and no ticket's chain
silently broke (`ENG-001`'s and `ENG-002`'s logs both end in a valid,
accounted-for state).

Business intake: found and shaped all three approver-filed requests that had
sat unprocessed in `inbox/requests/` since 2026-08-23 (flagged as an
observation by the prior pass). Ran the full request-readback on each — this
PM's reading plus a blind architect reading via an independent subagent per
request, so the second reading genuinely couldn't see the first. No material
divergence on any of the three; all three architect readings sharpened the
technical picture without disagreeing on scope or problem — see each
ticket's PRD.

- **ENG-003** (`aiorders-env-hygiene`, `config-site-builder`, size M, P2) —
  shaped straight through to `awaiting-scope`. `wip.approver_limit` (2) had
  exactly one free slot (`ENG-002` held the other); this one took it, on
  severity grounds — an ongoing, possibly-live cost exposure (an
  unrestricted Google Maps key) outranks the other two's own "nothing here
  is urgent" framing. G1 raised and notified.
- **ENG-004** (`admin-hub-migration-history`, `aiorders-admin-hub`, size L,
  P2) — shaped to `shaped`, PRD complete, G1 held for the next free slot.
- **ENG-005** (`a4-poster-generator-decision`, `aiorders-admin-hub`, size S,
  P3) — shaped to `shaped`, PRD complete, G1 held for the next free slot. G1
  will be required despite `S`+`chore` auto-skip eligibility — the ticket's
  scope is an unresolved approver decision, not routine work; see its own
  log.

All three source requests moved to `inbox/_handled/`. Two items filed rather
than fixed: a proposal (`agents/eng-manager/proposals.md`) that
`lib/eng-notify.sh` has two real bugs — no channel dispatch (posts to Slack
regardless of this instance's `approver.notify: telegram`), and a `MODE`
variable collision with the sourced business-os `.env` that silently breaks
the `stall` alert and the `nudge` prefix (confirmed live: this pass's own
`raise` call logged `sent: active`, not `sent: raise`); and two observations
(`agents/eng-manager/observations.md`) — a ticket-schema gap (`project:`/
`branch:` are singular, `ENG-003` genuinely spans three repos) and a
registry gap (`config/projects.md` doesn't record which Supabase project
`aiorders-admin-hub` is linked to, which `ENG-004` needs to answer).

Approver-facing WIP now 2/2 (full), approval cap 2/3. `chained: none` on all
three new tickets — `ENG-003` waits on the approver, `ENG-004`/`ENG-005`
wait on a WIP slot freeing; see each ticket's log for the reasoning.

## 2026-08-25 — continue ENG-001: PM shaping + ENG-002 opened

`continue ENG-001` pass. Shaped `ENG-001` (`intake → shaped`): wrote its PRD,
re-confirmed AC1 (five repos registered at L1, approved 2026-07-28,
re-verified 2026-08-23), AC2 (all five worktrees present under `_eng/`), and
AC3 (`lib/eng-gate-check.sh` exit 0) as already satisfied.  `type: chore`
auto-skips G1, so no gate item for `ENG-001` itself.

AC4 (one real ticket to `shaped`) was still open. Found a genuine, already-filed
approver request sitting unprocessed in `inbox/requests/` since 2026-08-23
(`2026-08-23-test-harness.md`) — not a self-originated finding, so shaping it
didn't touch the department's-own-work rule (`schedules/eng_build_loop.md`
step 3). Ran the full request-readback on it (this PM's reading + a blind
architect reading, no material divergence) and shaped it into `ENG-002`
(`intake → shaped → awaiting-scope`) — a smoke-test harness for
`restaurant-portal`, since none of the five AIOrders repos has a single test
and the QA gate is currently unable to prove anything ran. `size: M`, so
(unlike `ENG-001`) **G1 is required** — item raised and notified, see
"Waiting on the approver" above. `ENG-001`'s AC4 is satisfied by `ENG-002`
having reached `shaped` en route to `awaiting-scope`.

Did not push `ENG-001` past `shaped` this pass — what "building" means for a
ticket with no application-code deliverable (config/registry verification,
another ticket) isn't addressed anywhere in the department's docs, and a
snap judgement call on that shouldn't be buried in a PM pass. Left for the
architect on the next `continue`. `chained: ENG-001`.

Two things filed rather than fixed in this pass: a proposal
(`agents/eng-manager/proposals.md`) noting `agents/critic/agent.md` doesn't
exist on this instance or the department template, though
`skills/prd-writer/SKILL.md` step 8b calls for it before every G1 (ENG-002's
G1 went out with no `## Dissent` as a result); and an observation
(`agents/eng-manager/observations.md`) that three other approver requests in
`inbox/requests/` (`a4-poster-generator-unwired`, `admin-hub-migration-history`,
`aiorders-env-hygiene`) are still unshaped, out of scope for this
ticket-scoped pass. The `scheduled manual-unblock` event already queued
behind this one should sweep them.

## 2026-08-24 — decision: gate-check-unavailable resolved

Acted on the answered incident gate `2026-08-24-eng-gate-check-unavailable.md`
(`gate: incident`, tied to ENG-001 because it was the ticket in flight when the
pre-pass check found `lib/eng-gate-check.sh` unreadable). Its `project: life-os`
was stale — a leftover of the pre-carve-out hardcoding bug fixed in business-os
`ed8dd56`/`58ae148`/`9366b84`; `ticket: ENG-001` was correct. Approver had
already recorded `decision: approved`. Independently re-ran
`lib/eng-gate-check.sh` against this instance this pass: exit 0, clean — ENG-001
AC3 satisfied. Logged on ENG-001, moved the gate item to `inbox/_handled/`.
Did not shape ENG-001 further — a decision pass is scoped to the gate it
answers, not PM intake work — so `chained: ENG-001` to hand the ticket to a
fresh `continue` pass.
