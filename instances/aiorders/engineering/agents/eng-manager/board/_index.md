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

`priority:` is a field on every ticket, and **only the approver sets it.** It is
not `severity`, which is the agent's read of how bad a problem is.

## In flight

| ID | Title | Project | State | Priority | Owner | Size | Updated |
|---|---|---|---|---|---|---|---|
| ENG-008 | Influencer board admin management — region/campaign-type preference, rating, collaboration count | aiorders-admin-hub | blocked | | approver | M | 2026-08-31 |
| ENG-009 | Influencer engagement info — internal activity signal plus a staff-editable social stat | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-29 |
| ENG-010 | Influencer relationship notes — staff log for personality, preferences, and off-platform conversations | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-29 |
| ENG-013 | Foodswipe funnel page — staff-settable pipeline stages | aiorders-admin-hub | blocked | | approver | M | 2026-08-31 |
| ENG-014 | Brand portal self-service — restaurant QR codes and marketing media downloads | restaurant-portal | designed | | architect | M | 2026-08-31 |
| ENG-015 | Agency/reseller (partner) users — brand-scoped locations and a working add-location path | aiorders-admin-hub | designed | | architect | M | 2026-08-31 |
| ENG-016 | Catering page — self-serve quote generator, with automatic stage update | config-site-builder | shaped | | product-manager | L | 2026-08-29 |
| ENG-017 | Autopilot nurture for the presignup sales lead pipeline — stage-triggered email/SMS | aiorders-api | shaped | | product-manager | L | 2026-08-29 |
| ENG-018 | Sales demonstration account — a fully seeded AIOrders environment to show prospects | aiorders-admin-hub | shaped | | product-manager | L | 2026-08-29 |
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

