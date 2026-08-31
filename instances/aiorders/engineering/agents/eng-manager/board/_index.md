# Board

**Next ID: ENG-026** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.)

**Machine WIP 1** (`config/config.yaml` → `wip.machine_limit`). **Corrected
2026-08-29 — the approver's direct instruction: one ticket completed end to
end (through `shipped`) before the next one starts, not several tickets each
advanced by one shallow step per pass.** This was 12 (the `max_5x` tier value)
earlier the same day; see that file for the full rationale.

**Currently 4/1 — over the new cap, but shrinking.** `ENG-009` and `ENG-010`
sit at `ready`; `ENG-008` sits at `in-qa` (security next, fresh session);
`ENG-013` passed its security gate this pass and now sits at
`ready-to-ship` (devops's release-readiness hop next) — all were already
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
| ENG-008 | Influencer board admin management — region/campaign-type preference, rating, collaboration count | aiorders-admin-hub | in-qa | | eng-manager | M | 2026-08-31 |
| ENG-009 | Influencer engagement info — internal activity signal plus a staff-editable social stat | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-29 |
| ENG-010 | Influencer relationship notes — staff log for personality, preferences, and off-platform conversations | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-29 |
| ENG-013 | Foodswipe funnel page — staff-settable pipeline stages | aiorders-admin-hub | ready-to-ship | | devops | M | 2026-08-31 |
| ENG-014 | Brand portal self-service — restaurant QR codes and marketing media downloads | restaurant-portal | designed | | architect | M | 2026-08-31 |
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

