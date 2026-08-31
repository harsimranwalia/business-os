# Board

**Next ID: ENG-026** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.)

**Machine WIP 1** (`config/config.yaml` → `wip.machine_limit`). **Corrected
2026-08-29 — the approver's direct instruction: one ticket completed end to
end (through `shipped`) before the next one starts, not several tickets each
advanced by one shallow step per pass.** This was 12 (the `max_5x` tier value)
earlier the same day; see that file for the full rationale.

**Currently 4/1 — over the new cap, but shrinking.** `ENG-009` and `ENG-010`
sit at `ready`; `ENG-008` and `ENG-013` sit at `building` — all were already
in flight when the cap changed and are **not** being reverted or paused; they
drain naturally as each reaches `shipped`. `ENG-007` left this range this
pass — found already merged on GitHub (no gate item ever raised; the
Saturday window-hold blocking its own PR-open step had already been made
moot by the same-day L1 correction), verified against its gate receipts, and
carried `ready-to-ship → shipped → verified` in the same sweep. **No new
ticket enters `ready` until this count is back at or under 1** — `ENG-014`
through `ENG-025` stay at `designed`/`shaped`/`awaiting-scope` (backlog
grooming only, not gated by this cap) until then.

**Approver-facing WIP 2 — 0/2, fully clear.** `ENG-011` (the one occupied
slot, `blocked`/`blocked_on: approver`) found merged on both repos this
pass — both PRs merged by the approver directly, 40 seconds apart,
confirmed via git ancestry and independently via `gh pr view` on each repo —
and carried `blocked → shipped → verified`. Nothing else is currently
gated on the approver.

**Approval cap 3 — 0/3, fully clear.** Same `ENG-011` merge freed the one
occupied slot. Three slots free — `ENG-016` through `ENG-021` are also
G1-drafted and ready, but deliberately left for a future pass rather than
filling every open slot in one sweep; see `ENG-023`'s own ticket log for the
reasoning.

`priority:` is a field on every ticket, and **only the approver sets it.** It is
not `severity`, which is the agent's read of how bad a problem is.

## In flight

| ID | Title | Project | State | Priority | Owner | Size | Updated |
|---|---|---|---|---|---|---|---|
| ENG-008 | Influencer board admin management — region/campaign-type preference, rating, collaboration count | aiorders-admin-hub | building | | eng-manager | M | 2026-08-29 |
| ENG-009 | Influencer engagement info — internal activity signal plus a staff-editable social stat | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-29 |
| ENG-010 | Influencer relationship notes — staff log for personality, preferences, and off-platform conversations | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-29 |
| ENG-013 | Foodswipe funnel page — staff-settable pipeline stages | aiorders-admin-hub | building | | eng-manager | M | 2026-08-29 |
| ENG-014 | Brand portal self-service — restaurant QR codes and marketing media downloads | restaurant-portal | designed | | architect | M | 2026-08-29 |
| ENG-015 | Agency/reseller (partner) users — brand-scoped locations and a working add-location path | aiorders-admin-hub | designed | | architect | M | 2026-08-29 |
| ENG-016 | Catering page — self-serve quote generator, with automatic stage update | config-site-builder | shaped | | product-manager | L | 2026-08-29 |
| ENG-017 | Autopilot nurture for the presignup sales lead pipeline — stage-triggered email/SMS | aiorders-api | shaped | | product-manager | L | 2026-08-29 |
| ENG-018 | Sales demonstration account — a fully seeded AIOrders environment to show prospects | aiorders-admin-hub | shaped | | product-manager | L | 2026-08-29 |
| ENG-019 | Restaurant self-service marketing broadcasts — mass send and drip sequences, scheduled or immediate | restaurant-portal | shaped | | product-manager | L | 2026-08-29 |
| ENG-020 | Marketing ROI reporting — traffic source and revenue attribution on the brand dashboard | restaurant-portal | shaped | | product-manager | M | 2026-08-29 |
| ENG-021 | Website chat-bar engagement visibility — customer questions and self-service FAQ editing on the brand portal | restaurant-portal | shaped | | product-manager | M | 2026-08-29 |
| ENG-022 | Fix broken restaurant-scoped access check on 5 brand-portal handlers — cross-tenant PII/write exposure | aiorders-api | designed | | eng-manager | M | 2026-08-29 |
| ENG-023 | Add status and internal notes to each brand-portal feedback item | restaurant-portal | designed | | architect | S | 2026-08-29 |
| ENG-024 | Set show_in_marketplace on onboarding's createRestaurant insert, plus a backfill | aiorders-api | shaped | | eng-manager | XS | 2026-08-29 |
| ENG-025 | Recurring feedback issues, per restaurant, over time | restaurant-portal | designed | | architect | S | 2026-08-29 |

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

Cap: 3 across all gates. **0/3, fully clear.** `ENG-011`'s L1 merge request
(the one occupied slot) found both PRs merged directly on GitHub this pass
— never answered through the tracked channel, the merge itself was the
decision. `ENG-016` through `ENG-021` are also G1-drafted and ready to
raise, deliberately left for a future pass rather than filling every open
slot in one sweep — see `ENG-023`'s own ticket log for the reasoning.

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

