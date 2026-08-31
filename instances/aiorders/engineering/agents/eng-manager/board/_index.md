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
| ENG-013 | Foodswipe funnel page — staff-settable pipeline stages | aiorders-admin-hub | building | | eng-manager | M | 2026-08-30 |
| ENG-014 | Brand portal self-service — restaurant QR codes and marketing media downloads | restaurant-portal | designed | | architect | M | 2026-08-29 |
| ENG-015 | Agency/reseller (partner) users — brand-scoped locations and a working add-location path | aiorders-admin-hub | designed | | architect | M | 2026-08-29 |
| ENG-016 | Catering page — self-serve quote generator, with automatic stage update | config-site-builder | shaped | | product-manager | L | 2026-08-29 |
| ENG-017 | Autopilot nurture for the presignup sales lead pipeline — stage-triggered email/SMS | aiorders-api | shaped | | product-manager | L | 2026-08-29 |
| ENG-018 | Sales demonstration account — a fully seeded AIOrders environment to show prospects | aiorders-admin-hub | shaped | | product-manager | L | 2026-08-29 |
| ENG-019 | Restaurant self-service marketing broadcasts — mass send and drip sequences, scheduled or immediate | restaurant-portal | shaped | | product-manager | L | 2026-08-29 |
| ENG-020 | Marketing ROI reporting — traffic source and revenue attribution on the brand dashboard | restaurant-portal | shaped | | product-manager | M | 2026-08-29 |
| ENG-021 | Website chat-bar engagement visibility — customer questions and self-service FAQ editing on the brand portal | restaurant-portal | shaped | | product-manager | M | 2026-08-29 |
| ENG-022 | Fix broken restaurant-scoped access check on 5 brand-portal handlers — cross-tenant PII/write exposure | aiorders-api | designed | | eng-manager | M | 2026-08-29 |
| ENG-023 | Add status and internal notes to each brand-portal feedback item | restaurant-portal | designed | | architect | S | 2026-08-31 |
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

