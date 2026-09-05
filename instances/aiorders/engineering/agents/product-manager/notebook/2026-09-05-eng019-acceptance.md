# Acceptance — ENG-019 (restaurant self-service marketing broadcasts — parent)

## Why this ticket's own check is not a rubber stamp

`ENG-019` has no diff of its own — the `ADR-003`-class parent exemption means
it is never itself reviewed, tested, or security-scanned; its evidence is its
children's. But `acceptance-check/SKILL.md`'s trigger is "a ticket enters
state `shipped`," with no parent carve-out, same reasoning `ENG-016`'s own
parent check applied 2026-09-04.

**Unlike `ENG-016`'s family, this one has no gap to backfill.** Three of
`ENG-016`'s four children shipped via the receipt-bookkeeping shortcut (the
open `proposals.md` row, 2026-09-04), leaving several criteria never
individually walked until the parent's own check did it. Here, both of
`ENG-019`'s non-schema children — `ENG-038` and `ENG-039` — already ran
`acceptance-check/SKILL.md` **in full**, against live/merged code, at their
own shipping point (each one's own notebook says so explicitly, citing the
same open proposal as the reason not to take the shortcut). So this pass's
job is a rollup and a fresh no-drift check, not a rediscovery.

## Scope

All 7 acceptance criteria in the PRD
(`agents/product-manager/specs/ENG-019-restaurant-marketing-broadcasts.md`),
per the work-breakdown's own AC-mapping
(`agents/eng-manager/notebook/2026-09-04-eng019-work-breakdown.md`):

| AC | Owner | This pass |
|---|---|---|
| 1–7 | `ENG-038` (`aiorders-api`) | Cross-referenced from `ENG-038`'s own notebook — each already checked line-by-line against the exact live/merged source, not re-derived |
| 1–5 (surfacing only) | `ENG-039` (`restaurant-portal`) | Cross-referenced from `ENG-039`'s own notebook — corroborates 1–5 against the UI, including its own line-by-line cross-check of `ENG-038`'s contract |
| — | `ENG-037` (`aiorders-api`, migration) | 0 of the 7 apply — schema-only, inert until `ENG-038` (`ENG-031`'s own precedent on `ENG-016`) |

## Check against the live result — not the proxies

Re-fetched both repos fresh this pass rather than trusting either child's own
notebook date: `git fetch origin main` on `aiorders-api` → `89c6fdb1`,
**identical** to the commit `ENG-038`'s own acceptance-check walked; on
`restaurant-portal` → `aeeb7b9`, **identical** to the commit `ENG-039`'s own
acceptance-check walked. Zero drift on either repo since those checks ran
(both today) — nothing to re-derive, and the cross-references below are
against the current live state, not a stale snapshot.

## Walk every criterion

| AC | Criterion | Result |
|---|---|---|
| 1 | Send immediately or schedule for a future date/time | **Pass** — backend contract (`ENG-038`: `broadcasts.ts`/`dispatch.ts`) and UI (`ENG-039`: `BroadcastComposer.tsx`, confirmed matching the "omitted = immediate" contract verbatim) both walked fresh against live code |
| 2 | Drip: each step sends at its own delay, once per customer | **Pass** — enrollment/claim logic (`ENG-038`: `enrollAudience`/`claimRecipients`) and the step editor surfacing it (`ENG-039`: `BroadcastComposer.tsx` delay `Select`) both walked |
| 3 | Audience "all"/"inactive for N days," scoped strictly to the owner's own restaurant | **Pass** — restaurant-scoped query (`ENG-038`: `.eq('restaurant_id', ...)` on every audience path) and session-derived (not URL-param) scoping in the picker (`ENG-039`: `useRestaurant()`) both walked |
| 4 | Campaign report shows redemption count and revenue for its coupon | **Pass** — `null`-vs-`0` "not tracked" distinction traced end to end: API (`ENG-038`: `getBroadcastReport`) through UI (`ENG-039`: `BroadcastReport.tsx`, confirmed matching the contract verbatim) |
| 5 | Every send logged like existing automation sends, visible in campaign history | **Pass** — write path compared directly against `sendFirstOrderOffer`'s pre-existing insert shape (`ENG-038`), read/display path walked in the UI (`ENG-039`) |
| 6 | Working unsubscribe path; opted-out customer excluded from every future send | **Pass, code-level** — real HMAC sign/verify round-trip, double-enforced (enrollment-time and send-time re-check), walked fully at `ENG-038`. Fully backend-enforced; nothing for `ENG-039` to add, per the work-breakdown's own mapping |
| 7 | Cross-tenant read/send rejected server-side | **Pass** — every action requires `requireRestaurantAccess`; the system-triggered dispatch path independently confirmed to carry no caller-supplied `restaurant_id` at all. Fully backend-enforced; nothing for `ENG-039` to add |

**All 7 criteria: pass.** No criterion required rework; nothing routes back
to `building`.

## Check the non-goals (whole-family sweep)

Cross-referenced both non-schema children's own scans rather than re-running
them: `ENG-038`'s diff checked against the PRD's non-goals list (deeper ROI/
attribution, a segment builder beyond all/inactive-N-days, AI-generated
content, reseller access) — none present, one adjacent-but-not-violating note
(pre-existing `opened`/`clicked` columns read but not newly instrumented).
`ENG-039`'s diff independently confirmed `git diff --stat` touches no
reactive-`Automations` file (`types/autopilot.ts`, `Templates.tsx` both
untouched) and carries the same adjacent-but-not-violating note for its own
display of those columns. `ENG-037` is a schema-only migration — three new
tables and a cron schedule are storage/scheduling primitives already inside
this ticket's own approved model, not an implementation of any excluded
capability, so there is no separate non-goals surface to check on that diff.
**None of the PRD's excluded scope present anywhere in the family.**

## Check the cost

PRD: `$0/month` expected. All three children's own release records confirm
`cost_delta_monthly: 0` independently (`ENG-037`, `ENG-038`, `ENG-039`) — no
new vendor, no new dependency anywhere in the family. Matches.

## Route

**All 7 criteria pass.** State → `verified`, owner → `eng-manager` — see
`ENG-019`'s own board-file log for the transition (`building → shipped →
verified`, the `ADR-003`-class exemption for the `shipped` half).

## Step 6b — continue an approved sequence?

**Neither condition holds.** The PRD's Non-goals section names three
deferred ideas in prose (deeper ROI/attribution, a fuller segment/list
builder, AI-generated content) but none is a "Feature shape and sequencing"
section naming a specific next ticket with real shape the way `ENG-006`'s and
`ENG-016`'s PRDs did — condition 1 (enough shape to draft from) is not met.
Condition 2 fails independently regardless: the G1 answer on this ticket was
a bare "approved," no additional comment — no explicit sequence sign-off of
the kind 6b's bar requires (`ENG-006`'s own recorded answer is the standard;
this one doesn't clear it, same reading `ENG-016`'s own check gave its
identically-bare G1 before finding its own separate, PRD-named sequence
question instead). Nothing filed.

## What the estimate got right

`time_estimate: several days to a week+` (`L`) held: the work-breakdown's own
sizing summed to ~4–5 days of raw build time before gate rounds
(`2026-09-04-eng019-work-breakdown.md`), and total elapsed — including
`ENG-038`'s six review rounds and two security rounds — still landed inside
"week+."

## What it missed

Nothing at the criteria level — all seven pass exactly as scoped, no
criterion needed rework or reassignment. Two things worth naming again here,
not because they're new but because this is the point the whole family goes
terminal and nothing downstream will re-surface them:

- `ENG-038`'s own acceptance-check found its release-readiness snapshot
  ("not deployed") had gone stale within the same evening, once a human
  started merging *and* deploying by hand outside any tracked workflow.
  Already an observation on that ticket; restated here because it's a
  standing risk for every future `aiorders-api` ticket on this project, not
  just this one.
- `BROADCAST_UNSUBSCRIBE_SECRET` is still unprovisioned as this family
  reaches `verified`. By design this fails closed (loud, logged) rather than
  silently, and it stays inert until a real campaign exists — but it is the
  one thing standing between "the feature is verified" and "the feature
  works end to end the first time someone uses it." Named in three prior
  notebooks (`ENG-037`, `ENG-038`, `ENG-039`); one more mention here since
  this is the last checkpoint before the family leaves the board's active
  attention.

## Also worth recording

**First family on this board where the parent's own acceptance-check found
zero backfill work.** Contrast with `ENG-016` (3 of 4 children shipped via
the receipt-bookkeeping shortcut, leaving 5 criteria never individually
walked until the parent's own check did it). Here both non-schema children
ran `acceptance-check` in full at their own shipping point, each one citing
the same open `proposals.md` row (2026-09-04) as the reason not to take the
shortcut — so this parent check is a pure rollup plus a fresh no-drift
confirmation. One data point, not evidence the standing proposal is
resolved: both children compensated for the named gap by choosing not to
take the shortcut, which is a per-ticket judgment call, not a mechanical
close of the proposal's own recommended fix (a `lib/eng-gate-check.sh`
receipt check or a formal skill amendment — neither exists yet). Filed as an
observation (`observations.md`), not treated as closing the proposal.
