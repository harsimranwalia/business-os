# Acceptance — ENG-040 (Brand-portal FAQ write path, `ENG-021` sub-ticket 1 of 2)

## Why this ran in full, not as receipt bookkeeping

`ENG-040` is a work-breakdown child of `ENG-021`, not schema-only — the
`ENG-031`/`ENG-037`-style 0-criteria carve-out doesn't apply (this ticket owns
real, checkable behaviour). Per the department's own standing proposal (filed
2026-09-04, after ten ship events ran receipt-bookkeeping only), a ticket with
real criteria to check gets the skill run in full.

## Scope

Per `agents/eng-manager/notebook/2026-09-05-eng021-work-breakdown.md`'s own
AC-mapping (the design didn't map ACs to components itself), `ENG-040` owns
**AC4 and AC5 in full, plus the write half of AC3** from `ENG-021`'s PRD
(`agents/product-manager/specs/ENG-021-chat-bar-engagement-and-faq-self-service.md`).
AC1, AC2, AC6, and the UI half of AC3 belong to `ENG-041` (still `ready`, not
checked here — neither child owns AC3 alone, so a check of only this diff
finds it incomplete by design).

## Check against the live result — not the proxies

`aiorders-api` PR #18 merged directly on GitHub with no written reply
(`decision:` still blank on `inbox/2026-09-05-eng040-merge-request.md`):

```
$ git merge-base --is-ancestor origin/feat/ENG-040-brand-portal-faq-write-path origin/main
MERGED (is ancestor)
$ gh pr view 18 --json state,mergedAt,baseRefName,headRefName,mergeCommit
{"baseRefName":"main","headRefName":"feat/ENG-040-brand-portal-faq-write-path",
 "mergeCommit":{"oid":"5e36648b08c32443e287ea75fc2d5877124a75e5"},
 "mergedAt":"2026-09-06T16:11:40Z","state":"MERGED"}
```

**Zero drift on this ticket's own diff.** `git diff 104b057 origin/main --stat`
(the QA-reviewed tip vs. the merged tree) shows one file touched beyond
`104b057`, `supabase/functions/README.md`, +2/-1 — read the actual diff rather
than assuming corruption: it's `ENG-020`'s own already-verified
`get_acquisition_report` line landing in the same shared file, not anything of
this ticket's. `website.ts` itself: identical to the reviewed tip, byte for
byte (not in the diff stat at all).

**Confirmed live, not just merged:** `supabase functions list` shows
`brand-portal` at version 84, `UPDATED_AT 2026-09-06 16:29:25 UTC` — ~18
minutes after the merge, no tracked workflow on this repo, same by-hand-deploy
pattern every prior `aiorders-api` release on this board has shown. No
migration to check — this ticket has none.

Read the merged source directly (`git show origin/main:...`), not any gate's
account of it: `supabase/functions/brand-portal/website.ts`.

## Walk every owned criterion

| AC | Criterion (owned portion) | Checked against | Result |
|---|---|---|---|
| 3 (write half) | Owner can create/edit an FAQ entry "with no staff involvement" — the write capability must exist | `EDITABLE_PAGES = ['catering', 'careers', 'faqs']`; `updateWebsiteContent`'s generic per-key loop (`if (page in content) updates[page] = content[page] ?? null`) now covers `faqs` with no new branch. `content.faqs = []` persists as `[]`, not dropped — `in` check (not truthiness) plus `?? null` only nulling `null`/`undefined`, confirmed by reading the loop directly. Guarded by `requireRestaurantAccess(restaurant_id, supabase, user)` (the throwing, post-`ENG-022` version — confirmed by reading the call site, not assumed from the ticket's own claim) | **Pass** |
| 4 | Bot's answer draws on the *same* FAQ data the brand-portal editor writes, not a separate list | `update_website_content` persists to `restaurant_website.faqs`. Grepped every chat-bot search function in `aiorders-api`: `ai-search/index.ts`, `ai-search-intelligent/index.ts`, `ai-search-openrouter/index.ts` all `.from('restaurant_website').select('faqs, ...')` and read `restaurantData.faqs` directly into the bot's answer-formatting path — same table, same column, no second store | **Pass** |
| 5 | Brand-portal editor and the existing staff-only admin-hub editor stay in sync — one source of truth | Read `aiorders-admin-hub/src/pages/RestaurantAIWebsite.tsx` directly: its own save path (`~line 632`) is `.from('restaurant_website').upsert({..., faqs: updatedWebsiteData.faqs})` — same table, same column as `ENG-040`'s new edge-function path. Two editors (direct DB write for staff, JWT-gated edge function for owners), one row per restaurant, no divergent schema | **Pass** |

## Check the non-goals / bundling risk

Ticket's own Notes explicitly forbid touching `verifyRestaurantAccess`/
`requireRestaurantAccess` itself (that's `ENG-022`'s fix) and forbid "fixing"
the pre-existing `deno check` noise in passing. Confirmed on the merged diff:
only `EDITABLE_PAGES`, `getWebsiteContent`'s returned object, the `WebsiteFaq`
export, and the README line changed in `website.ts`'s own commit
(`104b057`) — no edit to `utils.ts`, no unrelated `deno check` fix. `deno
check website.ts` errors: 7→8 (one new, same-shape `GenericStringError`),
matches the build hop's own account exactly, not chased further.

## Check the cost

PRD/ticket: `$0/month`, no new dependency. `git diff origin/main...104b057 --
'*.json' '*.lock'` (re-run fresh this pass): empty. Matches.

## Route

**All 3 owned criteria (AC4, AC5 full; AC3 write-half): pass**, verified
directly against the merged and now-live source
(`aiorders-api@5e36648b`), not against any gate's own summary. AC3's UI half
and AC1/AC2/AC6 remain `ENG-041`'s to establish — not claimed here. State →
`verified`, owner → `eng-manager`.

## Step 6b — continue an approved sequence?

Does not apply at the child level — `ENG-021`'s own G1 was a bare approval
with no sequence naming beyond this ticket's own two-child breakdown, and
`ENG-041` (the remaining child) is already filed and sequenced, not a fresh
item to auto-file.

## Also worth recording

Shipping this ticket satisfies `ENG-041`'s sole `depends_on: [ENG-040]` —
`ENG-041` was already `ready` (dispatched as part of this work-breakdown
family, not a fresh WIP slot), so this doesn't start a second machine-WIP
occupant. `continue ENG-041` fired this same pass rather than building it
inline — new implementation work belongs in its own dedicated session, same
precedent `ENG-032`/`ENG-038`/`ENG-039` already set. `ENG-021` (parent) still
cannot reach `shipped` until `ENG-041` is settled too (`ADR-003`-class
exemption, one child down, one to go). Machine WIP unaffected throughout —
still `1/1`, held by the `ENG-021` family.
