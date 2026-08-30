# Board

**Next ID: ENG-026** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.)

**Machine WIP 1** (`config/config.yaml` → `wip.machine_limit`). **Corrected
2026-08-29 — the approver's direct instruction: one ticket completed end to
end (through `shipped`) before the next one starts, not several tickets each
advanced by one shallow step per pass.** This was 12 (the `max_5x` tier value)
earlier the same day; see that file for the full rationale.

**Currently 5/1 — over the new cap.** `ENG-007` sits at `ready-to-ship`;
`ENG-009` and `ENG-010` sit at `ready`; `ENG-008` and `ENG-013` sit at
`building` — all were already in flight when the cap changed and are
**not** being reverted or paused; they drain naturally as each reaches
`shipped`. `ENG-011` left this range this pass (`ready-to-ship → blocked`,
both PRs opened) — see its own dated entry below. **No new ticket enters
`ready` until this count is back at or under 1** — `ENG-014` through
`ENG-025` stay at `designed`/`shaped`/`awaiting-scope` (backlog grooming
only, not gated by this cap) until then. `ENG-007` is both the oldest of
the five and the closest to done (`ready-to-ship`) — finish it first;
per the corrected `skills/release-runner/SKILL.md` (2026-08-29), its own
window hold no longer applies either, since `aiorders-api` is L1 — worth a
fresh look next pass rather than assuming Monday.

**Approver-facing WIP 2 — 2/2, at the limit.** `ENG-025`'s G1 was processed
earlier this pass sequence (`scheduled`, context `schtasks`) — moved
`awaiting-scope → designed`, off this count. `ENG-023` (its G1 raised the
same pass, from its own already-drafted PRD content) holds one slot;
`ENG-011` (`ready-to-ship → blocked`, both PRs opened, merge request raised
this pass) now holds the second. At the limit, not over — nothing new
starts that would need the approver until one of these two clears.

**Approval cap 3 — 2/3.** `ENG-023`'s G1
(`inbox/2026-08-29-eng023-g1-scope.md`) and `ENG-011`'s new merge request
(`inbox/2026-08-29-eng011-merge-request.md`, both PR links) occupy two of
the three. One slot free — `ENG-016` through `ENG-021` are also G1-drafted
and ready, but deliberately left for a future pass rather than filling
every open slot in one sweep; see `ENG-023`'s own ticket log for the
reasoning.

`priority:` is a field on every ticket, and **only the approver sets it.** It is
not `severity`, which is the agent's read of how bad a problem is.

## In flight

| ID | Title | Project | State | Priority | Owner | Size | Updated |
|---|---|---|---|---|---|---|---|
| ENG-007 | Per-restaurant loyalty configuration — earn rates and redemption value | aiorders-api | ready-to-ship | | devops | S | 2026-08-29 |
| ENG-008 | Influencer board admin management — region/campaign-type preference, rating, collaboration count | aiorders-admin-hub | building | | eng-manager | M | 2026-08-29 |
| ENG-009 | Influencer engagement info — internal activity signal plus a staff-editable social stat | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-29 |
| ENG-010 | Influencer relationship notes — staff log for personality, preferences, and off-platform conversations | aiorders-admin-hub | ready | | eng-manager | S | 2026-08-29 |
| ENG-011 | Client stage & health visibility on the Brands admin page — plus stage filtering | aiorders-admin-hub | blocked | | approver | M | 2026-08-29 |
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
| ENG-023 | Add status and internal notes to each brand-portal feedback item | restaurant-portal | awaiting-scope | | approver | S | 2026-08-29 |
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
off the In-flight table (terminal); see its own board file.

## Waiting on the approver

Cap: 3 across all gates. **2/3.** `ENG-023`'s G1
(`inbox/2026-08-29-eng023-g1-scope.md` — status and internal notes on each
brand-portal feedback item) and `ENG-011`'s new L1 merge request
(`inbox/2026-08-29-eng011-merge-request.md` — two PRs, `aiorders-api` #3 and
`aiorders-admin-hub` #3) occupy two of the three slots. `ENG-016` through
`ENG-021` are also G1-drafted and ready to raise, deliberately left for a
future pass rather than filling every open slot in one sweep — see
`ENG-023`'s own ticket log for the reasoning.

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

