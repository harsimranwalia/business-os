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
| ENG-008 | Influencer board admin management — region/campaign-type preference, rating, collaboration count | aiorders-admin-hub | building | | eng-manager | M | 2026-08-31 |
| ENG-009 | Influencer engagement info — internal activity signal plus a staff-editable social stat | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-29 |
| ENG-010 | Influencer relationship notes — staff log for personality, preferences, and off-platform conversations | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-29 |
| ENG-013 | Foodswipe funnel page — staff-settable pipeline stages | aiorders-admin-hub | in-qa | | eng-manager | M | 2026-08-31 |
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

