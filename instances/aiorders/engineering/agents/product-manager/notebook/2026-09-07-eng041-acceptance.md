# Acceptance — ENG-041 (Customer Questions page + FAQ self-service editor, `ENG-021` sub-ticket 2 of 2)

## Why this ran in full, not as receipt bookkeeping

`ENG-041` is a work-breakdown child of `ENG-021`, not schema-only — it owns
real, checkable UI behaviour (AC1, AC2, AC6 in full, the UI half of AC3), so
the `ENG-031`/`ENG-037`-style 0-criteria carve-out doesn't apply. Per the
department's own standing proposal (filed 2026-09-04), a ticket with real
criteria to check gets the skill run in full.

## Scope

Per `agents/eng-manager/notebook/2026-09-05-eng021-work-breakdown.md`'s own
AC-mapping: `ENG-041` owns **AC1, AC2, AC6 in full, plus the UI half of AC3**
from `ENG-021`'s PRD
(`agents/product-manager/specs/ENG-021-chat-bar-engagement-and-faq-self-service.md`).
AC4 and AC5, and AC3's write half, are `ENG-040`'s — already verified at that
ticket's own acceptance (2026-09-06) — not re-derived here.

## Check against the live result — not the proxies

`restaurant-portal` PR #5 merged directly on GitHub with no written reply
(`decision:` still blank on `inbox/2026-09-06-eng041-merge-request.md`):

```
$ git merge-base --is-ancestor origin/feat/ENG-041-customer-questions-and-faq-editor origin/main
MERGED (is ancestor)
$ gh pr view 5 --json state,mergedAt,baseRefName,headRefName,mergeCommit
{"baseRefName":"main","headRefName":"feat/ENG-041-customer-questions-and-faq-editor",
 "mergeCommit":{"oid":"f64958393eb55b726a3d3c036160dc86c3d0312d"},
 "mergedAt":"2026-09-07T06:18:50Z","state":"MERGED"}
```

**Zero drift on this ticket's own diff.** `git diff 01c6ddb origin/main --stat`
(the QA-reviewed tip — the mutation-verified AC1 test commit — vs. the merged
tree) is empty: nothing landed on `main` beyond what the security gate
reviewed. Merge commit `f649583`'s own parents are `8eea8f1` (`main`'s tip at
merge time, itself `ENG-020`'s already-verified state) and `01c6ddb` (this
ticket's own reviewed tip) — a plain merge, no rebase, no squash.

**Confirmed actually deployed, not just merged.** `restaurant-portal` has no
manual deploy step (unlike `aiorders-api`) — `deploy-cf.yml` fires on every
push to `main`. `gh run list --branch main` shows a "Deploy to Cloudflare
Pages" run at `head_sha f649583`, created `2026-09-07T06:18:53Z` (3 seconds
after the merge), `status: completed`, `conclusion: success`. The build is
live, not just built.

Read the merged source directly (`git show f649583:...`), not any gate's
account of it: `src/pages/questions/Index.tsx`,
`src/components/website/WebsiteFaqForm.tsx`, `src/pages/website/Index.tsx`.

## Walk every owned criterion

| AC | Criterion (owned portion) | Checked against | Result |
|---|---|---|---|
| 1 | Owner sees their own restaurant's chat-bar questions, and never another's | `questions/Index.tsx`'s query: `.from('ai_conversations').select(...).eq('restaurant_id', currentRestaurant.id)` — read directly out of the shipped file, not inferred from the test plan. Server-side RLS (`"Restaurant managers can view their restaurant conversations"`) backs it independently, confirmed live against `bmnmnejwdxbcqinqkwko` by this ticket's own build hop the same day. | **Pass** |
| 2 | No chat-bar activity yet → plain empty state, not an error or blank screen | `questions/Index.tsx`: `questions.length === 0` renders a dedicated card ("No questions yet" / "No one has used your website chat yet..."), distinct from the `isError` branch above it ("Couldn't load your customers' questions..." + retry button). Both read directly from the shipped JSX, not the test names. | **Pass** |
| 3 (UI half) | Owner creates/edits a website FAQ entry directly from the brand portal, from a logged question, with no staff involvement | Three things read directly off the shipped tip: (a) `questions/Index.tsx`'s `handleAddToFaqs` navigates to `/website` with `state: { faqDraft: { question: text, restaurantId: currentRestaurant.id } }` — react-router state, never a URL parameter, matching the design's explicit requirement; (b) `WebsiteFaqForm.tsx`'s effect computes `faqDraft?.restaurantId === currentRestaurantId ? faqDraft : null` before applying it — the round-1 cross-restaurant leak fix, present in the merged code, not just claimed in the log; (c) the form itself supports add/edit/remove (`Add FAQ` button, per-row `Input`/`Textarea`, delete icon) and its `Save FAQs` submit calls `onSave`, which `website/Index.tsx` wires to `saveMutation` → the `brand-portal` edge function's `update_website_content` action — the same real write path `ENG-040` verified, not a stub. | **Pass** |
| 6 | Many questions presented legibly (most-recent-first, one per row), not a raw transcript | `flattenSession` extracts only `role === 'user'` turns (never the assistant) into flat rows; `sortNewestFirst` orders by timestamp descending, nulls last; each row renders as its own `Card` with relative time (`formatDistanceToNow`). Read directly from the shipped `flattenSession`/`sortNewestFirst`/render logic, not the test descriptions. | **Pass** |

**Cross-restaurant leak (round-1 review finding) independently re-verified
fixed on the merged tip**, not taken from the review log's word: the same
`faqDraft?.restaurantId === currentRestaurantId` guard quoted above is the
exact code shipped to `main`. Traced by hand: draft created scoped to
restaurant A, `WebsiteFaqForm` remounts on switch to B with a fresh
`draftConsumedRef`, `'A' !== 'B'` → discarded, never applied.

## Check the non-goals / bundling risk

Ticket's own Notes explicitly forbid touching `CateringPageForm.tsx`/
`CateringFaq` or the admin-hub staff editor. Confirmed on the full merge diff
(`git diff 8eea8f1 f649583 --stat`, 8 files:
`App.tsx`, `Sidebar.tsx`, `WebsiteFaqForm.tsx` + its test,
`pages/questions/Index.tsx` + its test, `pages/website/Index.tsx`,
`types/website.ts`) — no `CateringPageForm.tsx`, no `CateringFaq`, no
admin-hub file (different repo entirely). No scope creep.

## Check the cost

PRD/ticket: `$0/month`, no new dependency. The merge diff touches no
manifest or lockfile (`package.json`/`package-lock.json` absent from the
8-file list above). Matches.

## Route

**All 4 owned criteria (AC1, AC2, AC6 full; AC3 UI-half): pass**, verified
directly against the merged and now-live-deployed source
(`restaurant-portal@f649583`), not against any gate's own summary. State →
`verified`, owner → `eng-manager`.

## Step 6b — continue an approved sequence?

Does not apply — `ENG-021`'s own G1 was a bare approval with no sequence
naming beyond this ticket's own two-child breakdown (`ENG-040`/`ENG-041`),
and there is no further named item in the PRD to auto-file.

## Also worth recording

This is `ENG-021`'s **last** sub-ticket — both children (`ENG-040`,
`ENG-041`) are now `shipped`/`verified`, satisfying the `ADR-003`-class
parent exemption (all children settled, at least one shipped — here, both).
`ENG-021` itself is not touched in this pass — carrying a parent through its
own no-diff exemption is new implementation-adjacent work in the sense this
board's own precedent (`ENG-016`, `ENG-019`) already treats as belonging to
its own dedicated hop, not a whole-board sweep. `continue ENG-021` fired
instead, same handoff shape those two families' own closing passes used.
Machine WIP unaffected — still `1/1`, held by the `ENG-021` family until the
parent's own chained pass carries it to `shipped`.
