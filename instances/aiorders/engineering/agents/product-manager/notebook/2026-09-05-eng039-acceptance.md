# Acceptance — ENG-039 (Broadcasts tab, composer, drip editor, report UI)

## Why this ran in full, not as receipt bookkeeping

`2026-09-04-eng019-work-breakdown.md`'s own Acceptance-criteria-coverage
table maps AC1–AC5 of `ENG-019`'s 7 to this ticket specifically ("surfaces
what `ENG-038` returns"). `acceptance-check/SKILL.md`'s trigger ("a ticket
enters state `shipped`") applies the same way it did for `ENG-034`'s and
`ENG-038`'s own notebooks today — this is the family's third and last
sub-ticket to reach it.

## Scope

AC1–AC5 of the PRD
(`agents/product-manager/specs/ENG-019-restaurant-marketing-broadcasts.md`),
frontend half only. AC6 (unsubscribe) and AC7 (server-side tenant rejection)
are fully backend-enforced and already verified at `ENG-038`'s own
acceptance-check — nothing left for this ticket to add.

## Check against the live result — not the proxies

**Merge confirmed two ways** before checking anything else: `git
merge-base --is-ancestor 2f438e0 origin/main` → yes; `gh pr view 3` →
`MERGED`, base `main`, merge commit `aeeb7b9`, `mergedAt:
2026-09-05T17:05:41Z`. `git diff 2f438e0 aeeb7b9 --stat` is empty — the
merge commit is byte-for-byte what code review, quality, and security each
already traced; no drift window to worry about, unlike `ENG-038`'s
same-evening deploy surprise.

**This is a static frontend (Cloudflare Pages)**, not a live backend with
its own runtime state — there is no "deployed but not yet confirmed" gap of
the kind `ENG-038`'s check hit, and no config/secret/cron state of its own
to query read-only. Source of truth is `git show origin/main:{path}` at the
merge commit, read directly rather than trusted from any gate's own summary,
same standing practice.

**What this check does not do:** create a real campaign or exercise a real
send — that's `ENG-037`/`ENG-038`'s send path, already exercised at their
own gates within its own read-only bounds; re-doing it here would be
re-testing someone else's already-verified code, not this ticket's UI.

## Walk every criterion

| AC | Criterion | Checked against | Result |
|---|---|---|---|
| 1 | Send immediately or schedule for a future date/time | `BroadcastComposer.tsx` L107-109 (`scheduleLater`/`scheduleDate`/`scheduleTime` state), L183 (`scheduleValid`), L193-215 (`handleSubmit`: `scheduleLater && scheduleDate` → constructs `send_at` from date+time; otherwise omits it, matching `ENG-038`'s own "omitted = immediate" contract, already verified). Edit-reopen path (L132-145) restores the correct toggle/date/time from `editCampaign.scheduled_send_at` | **Pass** |
| 2 | Drip: each step editable with its own configured delay | `BroadcastComposer.tsx` L167-169 (`addStep`), L363-385 (per-step `Select` bound to `BROADCAST_DELAY_OPTIONS`, `updateStep(index, { delay_hours })`), L286 ("Drip sequence (2+ steps)" type option), L181 (`stepCountValid`: exactly 1 for `one_time`, `>=2` for `drip`). The delay *mechanics* (enrollment, once-per-customer, actual send timing) are `ENG-037`/`ENG-038`'s own, already verified at that gate — this ticket's scope is the editor surfacing them, confirmed present | **Pass** |
| 3 | Audience "all" vs. "inactive for N days," scoped strictly to the owner's own restaurant | `BroadcastComposer.tsx` L127-128 (`audience_mode`/`audience_inactive_days` restore on edit), L206 (submit payload), L302-305 (picker UI, `inactive_days` reveals the N-days input). Restaurant scoping: `restaurantId` sourced from `useRestaurant()`'s session-derived context (confirmed by direct read of `Broadcasts.tsx`'s own hook usage, not just cited from security's account), never a URL/route param — matching every sibling autopilot page and independently re-confirmed by security round 1 the same day | **Pass** |
| 4 | Campaign report shows redemption count and revenue for its attached coupon | `BroadcastReport.tsx` L101-122: `report.redemptions !== null` gates the whole "Coupon Performance" block (so no-coupon reads as absent, not zero — matches `ENG-038`'s own `null`-vs-`0` contract verbatim); `report.redemptions` and `formatCurrency(report.revenue \|\| 0)` rendered as two stat cards | **Pass** |
| 5 | Every send logged the same way, visible in that campaign's history | `BroadcastReport.tsx` L41 (`delivery_by_channel` entries iterated), L52-59 (`recipients_by_status` rendered per status key); reachable per-campaign from `Broadcasts.tsx` L202 ("View report" row action) → L276-281 (dialog rendering `<BroadcastReport restaurantId campaign>`). The underlying write/log format is `ENG-038`'s own (`communication_log`, already verified against `sendFirstOrderOffer`'s pre-existing insert shape) — this ticket's scope is display, confirmed present and correctly gated (no channel-level pending/failed split in the API response, so the UI correctly doesn't claim one) | **Pass** |

## Live infrastructure, checked read-only

None to check — this release has no backend/database/secret surface of its
own (pure frontend). The backend surface this ticket depends on
(`aiorders-api`'s `brand-portal/broadcasts.ts`) was already checked live at
`ENG-038`'s own acceptance-check the day before; not re-derived here.

## Check the non-goals

Diff scanned against `ENG-019`'s non-goals list (deeper ROI/attribution
beyond redemption+revenue, a segment builder beyond all/inactive-N-days,
AI-generated content, reseller access, a new outbound channel, any change
to reactive `Automations`) — `git diff 5276a53 aeeb7b9 --stat` confirms
`types/autopilot.ts`, `Templates.tsx`, and every reactive `Automations` file
untouched; none of the excluded scope present.

**Worth naming rather than passing over silently:** `BroadcastReport.tsx`
displays `opened`/`clicked` counts only for `channel === 'email'` — a
presentation choice on data the API already returns for every channel
(code review's own finding, re-confirmed here), not new tracking
instrumentation added by this ticket. Consistent with `ENG-038`'s own
acceptance-check naming the same adjacent-but-not-violating shape.

## Check the cost

PRD: `$0/month` expected. No new dependency in the diff — code review's own
automatic-failure scan #6 (clean) re-confirmed directly:
`git diff 5276a53 aeeb7b9 --stat` touches no `.json`/`.lock` file. Matches.

## Route

**All 5 criteria this ticket owns: pass**, verified directly against the
exact merged source (`origin/main` at `aeeb7b9`), not against the test
suite, the PR description, or any gate's own summary. State → `verified`,
owner → `eng-manager`.

## Step 6b — continue an approved sequence?

Does not apply at this sub-ticket's level, same reasoning `ENG-034`'s and
`ENG-038`'s own notebooks recorded: the PRD's sequencing lives with the
parent (`ENG-019`), not with a work-breakdown child. This is the family's
last piece, not a new sequence item — nothing to raise here.

## What the estimate got right

`time_estimate: ~1-1.5 days` — build was a single session, and the combined
review/quality hop, security hop, and release-readiness hop each passed
their first round with no bounce. Closest to estimate of the three
`ENG-019` sub-tickets. The work-breakdown's own AC-ownership pre-mapping
(AC1-5 to this ticket) held exactly as written; no criterion needed
reassignment.

## What it missed

Nothing at the criteria level. No live-state surprise of the kind
`ENG-038`'s check hit — a static frontend release has no deploy-timing
window for a receipt to go stale inside.

## Also worth recording

**Every child of `ENG-019` is now settled**: `ENG-037` (`verified`),
`ENG-038` (`verified`), `ENG-039` (`verified`, this entry) — all three
`parent: ENG-019`, none `dropped`, at least two actually shipped. The
`ADR-003` parent exemption condition is satisfied. `continue ENG-019` fired
this same pass so the parent's own next hop (whatever state its own
receipts put it at) can run with fresh context, rather than building that
out inline here.
