# Engineering Weekly Report — 2026-W36

**Covering:** 2026-08-30 through 2026-09-06. This is the department's first weekly
report — the 2026-08-30 run was skipped (the build-loop lock was held at fire
time; see `traces/eng-report-2026-08-30.log`), so nothing before this date has
been reported before now.

## 1. Shipped

- Per-restaurant loyalty configuration — restaurants can now set their own earn rate and redemption value.
- Influencer program admin tools — profile management (region/campaign-type preference, rating), an engagement signal, and a staff notes log.
- The Brands admin page now shows each client's lifecycle stage and health at a glance, with filtering.
- Foodswipe funnel — staff can now set a listing's pipeline stage by hand.
- Agency/reseller partner accounts are now properly scoped to their own brands, with a working add-location flow.
- Catering — a self-serve quote generator with automatic pipeline-stage updates, an itemized order view for owners, and a public category-grouped dish picker.
- **Security fix (P0):** five brand-portal endpoints that leaked cross-restaurant data and write access are now properly scoped.
- Newly onboarded restaurants now correctly appear in marketplace search, plus a backfill for the ones that were missing.
- Restaurant marketing broadcasts — mass-send and drip campaigns, scheduled or immediate, with unsubscribe handling and a delivery report.
- Marketing ROI reporting — traffic-source and revenue attribution on the brand dashboard.
- Brand-portal FAQ editing groundwork — the write path now accepts FAQ content (sets up next week's editor UI).

## 2. In flight

- **`ENG-021`** — chat-bar engagement visibility + FAQ self-service. State `building`, owner eng-manager, holds the department's one work-in-progress slot. Not moving on its own merits: both pieces are already done on the engineering side (`ENG-040` shipped, `ENG-041` fully gated with an open PR) — it's waiting entirely on your merge call, item 6 in the next section. Ten more tickets are fully designed and sitting ready behind this one slot (see Health).

## 3. Waiting on you

Oldest first. Each of these is a real decision, not a status update.

1. **(2 days old — raised 09-04, nudged 09-05)** `ENG-016` — continue to catering Piece 2 (pricing)? Not a gate, a sequencing question. *Recommendation:* proceed only once you've named who maintains each restaurant's price book; otherwise Piece 1 stands on its own. Nothing else is waiting on this answer.
2. **(raised today 02:28)** `ENG-028` G1 rescope — your nine sales-pipeline stage names don't map to today's six auto-detected ones. *Recommendation:* build your version now (M, half a day–2 days) — but confirm you want the old six retired and every existing listing reset to "Waitlisted," since keeping both alive would be a bigger, different ticket.
3. **(raised today 02:28)** `ENG-042` G1 scope — Foodswipe stage-triggered autopilot email/SMS. *Recommendation:* shape and size now (L), build only once `ENG-028`'s stage list ships. Confirm four assumptions: the message goes to the listing's own contact, not a staff alert; consent plus a global switch gate every send, both off by default; a stage fires its message once per listing ever, not on re-entry; a listing with no email/phone just skips that channel.
4. **(raised today 02:47)** `ENG-043` — which ticket did "stage names should be editable" mean: `ENG-011` (shipped last week — this would reopen a stated non-goal) or `ENG-028` (item 2, above)? Also: your message arrived cut off after "Healf" — resend if there was more.
5. **(raised today 03:13)** `ENG-018` G1 scope — sales demonstration account. *Recommendation:* build now as scoped (L) — one shared, neutrally-branded demo restaurant with real-looking menu/order/loyalty/catering activity, resettable from one admin entry point, isolated from real sends and platform analytics.
6. **(raised today 11:16)** `ENG-041` merge request — Customer Questions page + FAQ editor. *Recommendation:* merge. Code review passed on round 2 (round 1 found and fixed a real cross-restaurant data leak), quality and security both passed, no migration. This is `ENG-021`'s last piece — merging it closes out the whole feature and frees the one work slot for whatever you approve next. PR: `restaurant-portal#5`.

## 3b. Proposals — one batched decision

`agents/eng-manager/proposals.md`'s Open table carries **42 distinct items** (43
rows — two the department has already declared "one item, not two":
`updateBrandOwner()`, P3 below). Nothing has been approved or rejected since
this ledger opened 12 days ago, and nothing is old enough to expire yet (30-day
clock, oldest row is 12 days). Ordered by the consequence of leaving it alone.
Approve any subset, none, or all — see `inbox/PROP-2026-W36.md` to answer.

**Live security/data exposure — not yet fixed:**

| # | Filed | Project | What | Recommendation |
|---|---|---|---|---|
| P1 | 09-03 | aiorders-api | `updateRestaurant()` has no field allow-list — any authorized caller can overwrite Stripe/CloudWaitress secret columns via extra PUT keys. | Fix now (S). |
| P2 | 08-29 | aiorders-api | `update_catering_request` has a correct access check but an unconstrained write — a caller can reassign a catering row to a restaurant they don't own. | Fix now (S). |
| P3 | 08-29 & 08-31 | aiorders-api | `updateBrandOwner()` has no ownership check at all — any partner-admin/partner-user can rewrite any brand owner's contact info platform-wide. | Fix now (S) — `ENG-015` already shipped the identical fix shape on the sibling function; this is a copy. |
| P4 | 09-04 | aiorders-api | Unescaped HTML injection into the real, unauthenticated catering-request owner notification — a live phishing/spoofing vector today. | Fix now (S), small and contained. |
| P5 | 09-03 | aiorders-api | Structured customer consent (`consent_sms`/`consent_email`) is already collected but never checked by any send path. | Fix (M) — compliance exposure, not just a bug. |
| P6 | 09-03 | aiorders-api | `verifyRestaurantAccess` gives partner roles the same platform-wide tenant bypass as true admins, apparently unintentionally. | Confirm intent, then narrow (S). |
| P7 | 09-03 | aiorders-api | SMS sending is fully mocked platform-wide — `ENG-039`'s new broadcast UI will show "sent" to real customers while delivering nothing, no error surfaced. | Fix before broadcasts see real use (M, plus a separate XS field-name bug). |

**Department machinery — silently losing or misreporting its own work:**

| # | Filed | Project | What | Recommendation |
|---|---|---|---|---|
| P8 | 08-25 | aiorders | The notify script posts to Slack, not this instance's configured Telegram — plus a variable bug silently breaks the 24h nudge/stall alerts. Reconfirmed 3× over 11 days. | Fix (M) — this is the exact mechanism used to raise this digest; see Health. |
| P9 | 09-04 | aiorders | Merge detection only checks a branch tip against `main` — a stacked-PR ticket can read as unmerged when shipped, or shipped when it isn't. Cost `ENG-008` a false "not merged" for 3.5h. | Fix (S). |
| P10 | 08-31 | aiorders | A fired chain can be queued and never drain — no error, nothing. Cost `ENG-015` (a live P1) two full days. | Fix (M) — highest-cost machinery gap this month. |
| P11 | 09-03 | aiorders | A pass can exit 0, log success, and have done nothing — its delegated subagent was silently killed by an internal time budget first. | Fix (S–M). |
| P12 | 09-04 | aiorders | The acceptance-check skill (verifying a ship against its actual PRD, not just upstream approvals) hasn't genuinely run in 10 straight ships. | Decide: enforce it mechanically, or formally redefine what a merge-detected ship requires (S). |
| P13 | 09-04 | aiorders-api | A full-lane ticket (`ENG-038`) shipped a real schema migration with zero database-agent sign-off or rollback drill. | Fix (S). |
| P14 | 09-03 | aiorders | Fast-lane tickets can do the same — the database-review trigger only fires off a design step the fast lane skips entirely. | Fix (S) — likely one fix closes P13 and P14 together. |
| P15 | 09-01 | aiorders | The board index's own summary table went stale against real ticket files twice, each time pushing WIP accounting over cap and stalling a chain for hours unnoticed. | Fix (S) — derive the table from frontmatter, never hand-keep it. |
| P16 | 09-02 | aiorders | Every gate item's notified/nudged timestamp is local time mislabeled as UTC, department-wide. | Fix (S), one shared code path. |
| P17 | 09-03 | aiorders | Third occurrence: a new ticket can go missing from the board index entirely — this time cost a P0 (`ENG-035`) a silent ~9h stall. | Fix (S) — third strike. |
| P18 | 09-02 | aiorders | business-os's own git state isn't pulled on a schedule — twice now, real decisions sat answered-but-invisible on one host for over a day. | Fix (S–M). |
| P19 | 09-01 | aiorders | A failed pass's automatic retry doesn't check whether the spend limit actually reset before firing again. | Fix (S–M). |

**Quality and coverage gaps — real but bounded:**

| # | Filed | Project | What | Recommendation |
|---|---|---|---|---|
| P20 | 08-31 | aiorders-admin-hub | Zero test infrastructure — a real bug fix shipped on manual verification alone. | Build it (M) — this project ships the most staff-facing surface area. |
| P21 | 09-04 | config-site-builder | Same zero-test-infra gap; now the most actively-developed repo on the board. | Build it (M). |
| P22 | 09-03 | aiorders-api | "Highest blast radius" of the five projects has no test harness at the tooling level at all. | Build it (M) — wiring/documentation, not discovery. |
| P23 | 08-29 | aiorders-api | No live Postgres/Docker on this host to dry-run migration DDL (3rd occurrence). | Adopt the read-only MCP check as standard now; hold the paid branch-per-migration option for your budget sign-off. |
| P24 | 08-29 | aiorders-admin-hub | The same admin access-check helper was rewritten 3× and forked into two incompatible conventions, one of which crashes on a null profile. | Fix (S) — extract one shared helper. |
| P25 | 09-02 | aiorders | A ticket stacked on an unmerged sibling shipped the sibling's already-fixed bug verbatim; 4 review sweeps missed it. | Fix (S). |
| P26 | 09-03 | aiorders-api | `catering.ts`'s access checks are correct today but untested, unlike 5 of 9 sibling handlers — now consequential since its output renders to an owner. | Fix (S) — three test cases, mirrors an existing pattern. |
| P27 | 09-04 | aiorders | The 20-line ticket-log cap has been violated 3×, including twice in a row on the same ticket right after it self-corrected. | Enforce mechanically rather than by reminder (S). |
| P28 | 09-01 | aiorders | Nothing ever closes a self-closing "incident" item — the same dropped-event notice was independently re-derived, identically, 4 passes running. | Fix (S, doc-only). |
| P29 | 09-03 | aiorders | A rescope forked a new board file instead of editing in place — one ticket ID lived twice for a day, and a priority flag was silently dropped. | Fix (S) — add the missing uniqueness check. |
| P30 | 08-26 | aiorders | A control-center dashboard action once moved a ticket straight from `blocked` to `shipped`, bypassing the inbox decision field and the merge check. | Fix (S). |
| P31 | 08-26 | aiorders | The `watch` dedup fingerprint only updates on `watch`-typed passes, so any other event type guarantees the next `watch` pass wrongly concludes "nothing to do." | Fix (S). |

**Hygiene and bookkeeping — low urgency:**

| # | Filed | Project | What | Recommendation |
|---|---|---|---|---|
| P32 | 08-26 | restaurant-portal | `.env` is tracked in git — the 4th repo with this exact pattern (exposure not materially increased; all keys already ship client-side). | Fix opportunistically (S). |
| P33 | 09-04 | aiorders-api | `deno.lock` is untracked, 4th occurrence, now spreading to every new function directory. | Decide once, either way (XS). |
| P34 | 09-04 | aiorders | The board index's own header narrative has grown to ~350 lines, mostly documenting tickets already done. | Cheap one-time cleanup (S). |
| P35 | 09-03 | aiorders-api | `show_in_marketplace` has no database-level default; a third insert path could silently reintroduce `ENG-024`'s bug. | Fix (XS), low urgency. |
| P36 | 09-05 | aiorders-api | `customers` is missing a composite index its sibling table already has. | Fine to defer (XS) — no measurable impact yet. |
| P37 | 09-05 | aiorders-api | The write-path test gap on `brand-portal/website.ts` is closed for `faqs` only; `catering`/`careers` remain uncovered. | Finish it (S), cheap follow-on. |
| P38 | 08-27 | aiorders | A hand-completed decision and a queued automated retry for the same event aren't reconciled. | Fix (S) — touches core dispatch, your sign-off first. |
| P39 | 08-25 | aiorders | The critic agent (a mandatory dissent pass on every G1) was never ported — every G1 so far has gone out with no counter-case attached. | Port it, or formally drop the requirement (S) — the gap has stood since day one. |

**Already tracked elsewhere — informational:**

| # | Filed | Project | What | Recommendation |
|---|---|---|---|---|
| P40 | 08-30 | aiorders-api | Platform-analytics cron 401 — already tracked as `BUG-001` (see Bugs, below). | No separate decision needed. |
| P41 | 08-30 | aiorders-api | A cross-host trace gap nearly caused duplicate work on `ENG-013` (caught in time) and recurred in a different shape on `ENG-033` (also caught). | Fix (S), one cheap check. |
| P42 | 08-29 | aiorders | A dropped-event incident notice doesn't carry its own evidence, so it's undiagnosable from any host but the one that failed. | Fix (S) — embed evidence at write time. |

## 4. Blocked

Nothing. No ticket is currently blocked on an agent past 5 working days — the
department's one blocked ticket (`ENG-041`) is blocked on you, and appears in
section 3 instead.

## 4b. Oldest untouched backlog item

Nothing qualifies on the 60-day threshold yet — the oldest ticket on the whole
board is 14 days old. The oldest item actually waiting for a work slot is 8
days (`ENG-014`, `017`, `023`, `025` — all fully designed, queued behind the
one-ticket-at-a-time cap since 2026-08-29). No open tech-debt card exists right
now: all five `chore`-type tickets filed so far have already shipped or been
dropped.

## 5. Bugs

One open bug: **`BUG-001`** (P2) — the hourly platform-analytics cron has
returned 401 in production since 2026-08-30, so the Brands page's
health/analytics cache is aging instead of refreshing (every cached value is
correct as of its last good write; no data loss, orders/checkout unaffected).
7 days old against a 10-day P2 SLA — breaches 2026-09-09 if still open. Root
cause needs direct access to the Supabase function/cron auth config, which
nothing in this department's toolset can reach. No missing test caused this —
it's a platform/gateway auth setting, not application code.

## Gate waivers

No waivers — the ledger is empty.

## 6. Cost

**$845.23** in tracked usage this week (2026-08-30–2026-09-06, 253 passes)
against the flat **`max_5x`** plan (\$100/month — this figure is internal
usage-tracking, not a separate bill). No per-project breakdown exists in the
cost log; it records department-level passes only, not which repo each one
touched. Usage was quiet through 09-02, then surged 09-03–09-05
($185–257/day) as more tickets moved through gates.

Hop budget — the number that actually caps throughput — has comfortable
headroom: 51/200 daily hops at peak (09-04), 17/20 per-ticket at peak
(`ENG-038`'s heavy rework). No ceiling was hit this week. **Verdict: normal
usage, no upgrade signal yet.** If the 09-03–09-05 pace becomes the norm
rather than a burst, hop-ceiling proximity — not spend — is what would justify
`max_20x`.

## 6b. What the team noticed

Most of what recurred 3+ times this week is already carried as its own line in
§3b above rather than repeated here — the event-dispatch/gate-bypass family,
the board-index drift, the several "chained but never ran" variants, the
missing-test-harness gap on four different repos, the unconstrained-write
handlers, and the untracked `deno.lock` files. See §3b for each one's own
recommendation.

Three more patterns cross the same 3-occurrence bar but were **never actually
filed** anywhere:

- `config/projects.md`'s "all five worktrees exist" claim went stale on the
  Windows host — hit 4 times in one day (2026-08-29) across four different
  repos, last left with 2 of 5 unconfirmed and no later fix logged.
- A cached "N pre-existing lint/typecheck errors" baseline has been cited
  stale 3 times across two repos, most recently 2026-09-05.
- The department's own code-review rule names a specific failure — a new
  authz-gated write path shipped with zero tests — as auto-promotable into a
  written standard on its third occurrence. That third occurrence happened
  2026-09-03 (`ENG-013`, `ENG-008`, `ENG-015`); the promotion into
  `engineering-standards.md` was never carried out.

Worth naming plainly: the mechanism meant to turn "noticed three times" into
"written down" has itself now been missed three times. Nothing in the ledger
is old enough to prune — the oldest entry is 13 days old, well short of the
90-day mark.

## 6c. Exceptions

Nothing to report — the ledger is empty.

## 7. Speed

- **Median cycle time: ~3.5 days**, created → verified (20 tickets shipped
  this week). Longest-sitting state is `designed` — up to 8 days and counting,
  purely on the one-ticket work-in-progress cap, not on any engineering work
  still owed.
- **Approver-wait dominates machine-wait, by roughly two orders of
  magnitude.** ~772 hours across 33 decisions this week (average 23.4h, up to
  65h on the slowest). Machine-side — build through every gate to a mergeable
  state — ran 0.5–8h per ticket typically, about a day at worst even under
  heavy rework.
- **First-pass gate rate: 75%** (43 of 57 first-attempt gate submissions
  passed) — above the 70% target.
- **Rework rounds per ticket: 2.1 average**, one heavy outlier (`ENG-038`, 11
  total gate events across review, security, and release-readiness).

## 8. Health

First report ever for this instance — the 2026-08-30 run was skipped by lock
contention, not written and then lost, so nothing before this week could have
been reported regardless.

The numbers above say plainly where the calendar time actually goes: the
department is not the bottleneck, decisions are — approver-wait outweighs
machine-wait by roughly two orders of magnitude, and every ticket that shipped
this week cleared its own engineering work in a day or less even when it
needed four review rounds. That's not a complaint; it's the diagnostic the
Speed section exists to produce.

One place that shows up concretely: four P0 security findings (`ENG-029`,
`030`, `035`, `036` — two cross-tenant data-exposure bugs and two
"a caller-supplied flag substitutes for real auth" bugs that let anyone
trigger a real customer email/SMS at no cost) have sat fully designed and
ready to build for **3 days**, not because anyone decided they could wait, but
because nothing lets P0 severity jump the same one-ticket queue as everything
else — only your own `priority: now` flag would, and none of these four has
it. Worth an explicit answer: should these four go next, ahead of whatever
else you approve from §3b?

Two things worked well this week, worth keeping rather than just fixing
forward from: a real production P0 (`ENG-022`, cross-restaurant data leak)
went from found to shipped the same day, and the first-pass gate rate (75%)
is above target even with `ENG-038` pulling the average down hard.

Two things did not go well. A Windows-host lock-staleness bug caused roughly
30 hours of intermittent dropped and stalled passes (2026-08-30 evening
through 2026-09-01 morning) — real delay, not just noise; `ENG-009` sat stuck
3 days before an unrelated sweep caught it. It was root-caused and fixed on
09-02, and every affected ticket was eventually caught and carried forward
with nothing permanently lost — but "eventually caught by a different
mechanism" is still a real cost paid this week, not a non-event. Separately,
the notification script this report is about to use to raise §3b's digest has
a known, already-proposed bug (P8): it posts to Slack, not the Telegram
channel this instance is actually configured for, and this host's Telegram
chat id is empty regardless. So this report and this week's proposal digest
are both reliably on disk, but the push meant to tell you they exist may not
reach you the way you'd expect — worth checking the Engineering tab or
`inbox/` directly this week rather than waiting for a ping.

Net: this week the department took real work off your plate — 20 shippable
things landed, including a same-day P0 fix — but it's also carrying 42 open
proposals with a zero-clearance rate so far and four live P0s waiting on a
queue-order answer, and neither of those will resolve on its own no matter how
much further engineering throughput follows.
