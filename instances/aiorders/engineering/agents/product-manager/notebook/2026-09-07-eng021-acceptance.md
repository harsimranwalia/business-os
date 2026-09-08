# Acceptance — ENG-021 (website chat-bar engagement visibility + FAQ self-service — parent)

## Why this ticket's own check is not a rubber stamp

`ENG-021` has no diff of its own — the `ADR-003`-class parent exemption means
it is never itself reviewed, tested, or security-scanned; its evidence is its
children's. But `acceptance-check/SKILL.md`'s trigger is "a ticket enters
state `shipped`," with no parent carve-out, same reasoning `ENG-016`'s and
`ENG-019`'s own parent checks applied.

**Like `ENG-019`'s family, this one has no gap to backfill.** Both of
`ENG-021`'s children — `ENG-040` and `ENG-041` — already ran
`acceptance-check/SKILL.md` **in full**, against merged and live-deployed
code, at their own shipping point (`2026-09-06-eng040-acceptance.md`,
`2026-09-07-eng041-acceptance.md`). No `ENG-031`/`ENG-037`-style 0-criteria
schema-only child exists in this family either — both children own real,
checkable behaviour. So this pass's job is a rollup and a fresh no-drift
check, not a rediscovery.

## Scope

All 6 acceptance criteria in the PRD
(`agents/product-manager/specs/ENG-021-chat-bar-engagement-and-faq-self-service.md`),
per the work-breakdown's own AC-mapping
(`agents/eng-manager/notebook/2026-09-05-eng021-work-breakdown.md`):

| AC | Owner | This pass |
|---|---|---|
| 1, 2, 6, 3 (UI half) | `ENG-041` (`restaurant-portal`) | Cross-referenced from `ENG-041`'s own notebook — each already checked directly against the merged, live-deployed source, not re-derived |
| 4, 5, 3 (write half) | `ENG-040` (`aiorders-api`) | Cross-referenced from `ENG-040`'s own notebook — each already checked directly against the merged, live-deployed source, not re-derived |

No child owns a 0-criteria schema-only shape — this design had no migration
(`ENG-041`'s own required-first-step live check confirmed the RLS policy
already existed; nothing was added to the schema).

## Check against the live result — not the proxies

Re-fetched both repos fresh this pass rather than trusting either child's own
notebook date:

```
$ (cd aiorders-api && git fetch origin main && git log -1 --oneline origin/main)
5e36648 Merge pull request #18 from harsimranwalia/feat/ENG-040-brand-portal-faq-write-path

$ (cd restaurant-portal && git fetch origin main && git log -1 --oneline origin/main)
f649583 Merge pull request #5 from harsimranwalia/feat/ENG-041-customer-questions-and-faq-editor
```

`aiorders-api` `origin/main` is **identical** to `5e36648b`, the exact commit
`ENG-040`'s own acceptance-check walked and confirmed live-deployed
(`brand-portal` v84). `restaurant-portal` `origin/main` is **identical** to
`f649583`, the exact commit `ENG-041`'s own acceptance-check walked and
confirmed live-deployed (Cloudflare Pages run, `conclusion: success`, 3s
after merge). Zero drift on either repo since those checks ran — nothing to
re-derive, and the cross-references below are against the current live
state, not a stale snapshot.

## Walk every criterion

| AC | Criterion | Result |
|---|---|---|
| 1 | Owner sees their own restaurant's chat-bar questions, never another's | **Pass** — `questions/Index.tsx`'s `.eq('restaurant_id', currentRestaurant.id)` query, backed independently by live-confirmed RLS on `ai_conversations`. Walked at `ENG-041` |
| 2 | No chat-bar activity yet → plain empty state, not an error or blank screen | **Pass** — dedicated empty-state card, distinct from the `isError` branch. Walked at `ENG-041` |
| 3 | Create/edit a website FAQ entry directly from the brand portal, no staff involvement | **Pass, both halves** — write path: `EDITABLE_PAGES` gains `faqs`, generic per-key loop persists it including the empty-list case (`ENG-040`). UI path: `WebsiteFaqForm` add/edit/remove, `handleAddToFaqs` hand-off via router state carrying `restaurantId`, the round-1 cross-restaurant-leak fix (`faqDraft?.restaurantId === currentRestaurantId`) confirmed present in the merged tip, `Save FAQs` wired to the same edge-function action `ENG-040` verified (`ENG-041`) |
| 4 | Bot's next answer draws on the same updated FAQ content, not a disconnected copy | **Pass** — every chat-bot search function (`ai-search`, `ai-search-intelligent`, `ai-search-openrouter`) reads `restaurant_website.faqs` directly, the same column/table `ENG-040`'s write path persists to. Walked at `ENG-040` |
| 5 | Brand-portal editor and the existing staff-only admin-hub editor stay in sync | **Pass** — `aiorders-admin-hub`'s own staff save path (`RestaurantAIWebsite.tsx`) upserts the same `restaurant_website.faqs` column `ENG-040`'s edge-function path writes — one source of truth, two editors. Walked at `ENG-040` |
| 6 | Many questions presented legibly (most-recent-first, one per row), not a raw transcript | **Pass** — `flattenSession`'s `role === 'user'`-only filter plus `sortNewestFirst`, each row its own card with relative time. Walked at `ENG-041` |

**All 6 criteria: pass.** No criterion required rework; nothing routes back
to `building`.

## Check the non-goals (whole-family sweep)

Cross-referenced both children's own scans rather than re-running them:
`ENG-040`'s diff confirmed to leave `verifyRestaurantAccess`/
`requireRestaurantAccess` untouched (that's `ENG-022`'s fix, explicitly
out of scope) and add no unrelated `deno check` fix. `ENG-041`'s diff
independently confirmed to touch neither `CateringPageForm.tsx`/`CateringFaq`
(the unrelated catering-page FAQ list) nor any `aiorders-admin-hub` file —
both explicitly named as do-not-touch in the ticket's own Notes. Neither
child built any of the PRD's excluded scope: no answered/unanswered scoring
signal, no clustering/de-duplication, no admin-hub staff-facing mirror, no
change to the chat bar's own runtime behaviour, no retention-window change
(`ENG-041`'s live check found no `cleanup_old_ai_conversations` cron actually
exists — informational only, not acted on), no PII redaction (the PRD's own
Risks section left this to the security gate rather than resolving it by
omission; `ENG-041`'s security review classified the data **Restricted** per
`security-baseline.md` and confirmed it never appears in a URL or log line,
which is control, not redaction — matches the PRD's own framing, not scope
creep). **None of the PRD's excluded scope present anywhere in the family.**

## Check the cost

PRD: `$0/month` expected. Both children's own release records confirm
`cost_delta_monthly: 0` independently (`ENG-040`, `ENG-041`) — no new vendor,
no new dependency, no manifest/lockfile touched in either diff. Matches.

## Route

**All 6 criteria pass.** State → `verified`, owner → `eng-manager` — see
`ENG-021`'s own board-file log for the transition (`building → shipped →
verified`, the `ADR-003`-class exemption for the `shipped` half).

## Step 6b — continue an approved sequence?

**Neither condition holds.** The PRD's Non-goals section names deferred ideas
in prose (an answered/unanswered quality signal, clustering, a staff-facing
admin-hub mirror) but none is a "Feature shape and sequencing" section naming
a specific next ticket with real shape the way `ENG-006`'s/`ENG-016`'s PRDs
did — condition 1 (enough shape to draft from) is not met. Condition 2 fails
independently regardless: the G1 answer was a bare "approved," no additional
comment — no explicit sequence sign-off of the kind 6b's bar requires
(`ENG-006`'s own recorded answer is the standard; this one doesn't clear it,
same reading `ENG-019`'s own check gave its identically-bare G1). Nothing
filed.

## What the estimate got right

`time_estimate: a day to a day and a half` (`M`) held reasonably at the raw
build-time level: `ENG-040` closed in `~35m` (its own `XS` sub-estimate,
"under an hour"); `ENG-041` carried the bulk of the parent's own estimate —
one build hop, one review-fail-and-fix round, a combined QA/security pass,
release-readiness — landing inside "a day to a day and a half" of actual work
even though wall-clock stretched past that once the approver-merge wait
(overnight, `ready-to-ship → blocked` on 2026-09-06 to `verified` at 02:00
2026-09-07) is counted in. Same shape `ENG-019`'s own notebook already named:
raw build time inside estimate, wall-clock extended by a human-paced gate
that isn't part of the estimate.

## What it missed

Nothing at the criteria level — all six pass exactly as scoped, no criterion
needed rework or reassignment. One thing worth restating here, not because
it's new but because this is the point the family goes terminal and nothing
downstream will re-surface it: `ENG-041`'s own build hop found the design's
"Load older" pagination control was *not* dead weight (session volume tops
out at 585/restaurant, median 30) — the PRD's own Risks section had flagged
query volume as unknown and worth a quick check rather than a guess, and the
check paid off by confirming the design's own contingency plan was needed,
not by ruling it out. Next PRD with a similarly-unknown volume risk: naming
the check as a required build-time step (as this one did, not just a design
concern) is what let it get answered instead of assumed.

## Also worth recording

**Second family in a row on this board where the parent's own
acceptance-check found zero backfill work** (after `ENG-019`). Both non-
schema children ran `acceptance-check` in full at their own shipping point,
so this parent check is a pure rollup plus a fresh no-drift confirmation —
same shape, same reason (the standing `proposals.md` row from 2026-09-04
about receipt-bookkeeping leaving criteria unwalked). Two data points now,
not yet three — not treated as closing that proposal, same disposition
`ENG-019`'s own notebook already gave its own first data point.

**A real, blocking cross-tenant finding was caught and fixed inside this
family's own pipeline** (`ENG-041` review round 1: the FAQ-draft hand-off
state could survive a restaurant switch and leak one restaurant's customer
question onto another restaurant's public FAQ). Worth naming at the family's
closing checkpoint because it's the kind of finding the review gate exists to
catch before acceptance-check ever runs — by the time this pass checked AC3,
the fix was already shipped, tested, and independently re-verified twice
(round-2 review, security gate). Nothing further to do here; recorded so the
family's own history reads complete from this terminal point.
