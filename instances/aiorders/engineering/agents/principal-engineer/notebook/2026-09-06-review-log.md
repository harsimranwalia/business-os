# 2026-09-06 — Review log

## ENG-041 (round 1, restaurant-portal) — REVIEW pass

M, 578 insertions / 2 deletions across 8 files (2 new, 6 modified) on
`feat/ENG-041-customer-questions-and-faq-editor`
(`restaurant-portal@81b00b1`, off `origin/main@8eea8f1`). **0/10 automatic
failures.** The diff matches the design's own Components table file-for-
file: `WebsiteFaqForm.tsx` mirrors `CateringPageForm.tsx`'s existing add/
edit/remove idiom closely enough that a reader can't tell which pass wrote
it — including reusing its `key={index}`/no-`id`-pairing convention on
repeated rows (checked directly against `CateringPageForm`'s own venue
block: same pattern there too, not a new deviation this ticket
introduced). `questions/Index.tsx`'s query is the design's own
`## Interfaces` query verbatim, down to the `nullsFirst: false` subtlety.
`flattenSession`/`sortNewestFirst` implement the design's normaliser table
field-for-field, including the "unparseable timestamp falls back to
`updated_at`; still-null sorts last" case.

Independently re-ran rather than trusting the build entry's own numbers:
`npm run test` → 40/40 (confirmed, not just cited); `npm run build` →
clean, same pre-existing >500kB chunk warning; `npm run lint` → 96 problems
(62 errors/34 warnings), all in files this ticket never touches
(`onlineOrdersService.ts`, `proxyAuth.ts`, `jwtUtils.ts`,
`tailwind.config.ts`) — matches the claimed baseline-identical count.

**The blocking finding, traced end to end before writing it up** (three
files acting together, so I wanted to be sure it was real before failing an
otherwise clean-looking diff on it):

1. `src/context/restaurant/RestaurantContext.tsx` — `RestaurantProvider` is
   a top-level context provider. `currentRestaurant` is app-global state,
   not scoped to a route.
2. `src/components/layout/Sidebar.tsx:187` — `<RestaurantSelector />` is
   mounted permanently inside the layout every route renders through.
   Reachable from `/website` at any time, with no navigation away required.
3. `src/pages/website/Index.tsx:42-62` — the `content` query is keyed on
   `['website_content', currentRestaurant?.id]`. Grepped the whole repo for
   `placeholderData`/`keepPreviousData`: zero hits anywhere. So switching
   restaurants (new query key, no cached data for it) flips `isLoading`
   back to `true` for at least one render.
4. Same file, line 111: `if (isLoading) return (...)` sits **above** the
   `<Tabs>` return. Every restaurant switch therefore unmounts and remounts
   `<Tabs>` and everything inside it, including `WebsiteFaqForm`.
5. `src/components/website/WebsiteFaqForm.tsx:15` — the guard against
   re-appending the draft a second time is `useRef(false)`
   (`draftConsumedRef`). A ref resets to its initializer on every fresh
   mount, by construction — there's no way for a `useRef` to survive an
   unmount/remount, guard or not.
6. `src/pages/website/Index.tsx:24-30` — `faqDraft` itself lives one level
   up, in `Website`'s own `useState` with a lazy initializer reading
   `location.state` once. `Website` the component does **not** unmount on a
   restaurant switch (same route, same component instance — only its
   conditionally-rendered `<Tabs>` subtree does). So `faqDraft` survives the
   switch completely unchanged while `WebsiteFaqForm`'s guard against
   reusing it does not.

Net, ordinary reproduction: an owner who manages 2+ restaurants (explicitly
a supported, designed-for case — the query's own `.eq('restaurant_id',
...)` filter exists specifically because "an owner may manage several
restaurants and the page follows the selected one," per the design doc's
own Interfaces section) opens Restaurant A's Customer Questions page,
clicks "Add to FAQs" on a question, lands on `/website` with the FAQ tab
open and the question pre-filled and unsaved, then switches to Restaurant B
via the always-mounted sidebar selector without saving first.
`WebsiteFaqForm` remounts against Restaurant B's own content,
`draftConsumedRef` resets to `false`, and Restaurant A's customer's
question is silently re-appended — pre-filled, focused — onto Restaurant
B's FAQ editor. No test exercises this: both cases in
`WebsiteFaqForm.test.tsx` use `rerender()` on one already-mounted instance
(correct for the case they're actually testing — a post-save content
refetch on the *same* restaurant — and proof the guard works for that case)
rather than an unmount/remount with different `content`, so this is a real
gap, not a missed assertion on an existing test.

Full finding text (what's wrong, why it matters, the fix) is written in
full on the ticket's own round-1 log entry
(`agents/eng-manager/board/ENG-041-customer-questions-and-faq-editor.md`)
per `conventions.yaml`'s `ticket_log.entry` gate-fail exception — not
duplicated here; this section is the trace behind it.

**Two non-blocking notes, meant to be picked up in the same fix round
rather than filed separately:**
- The `{ question: string }` draft shape is currently declared inline three
  times (`WebsiteFaqForm.tsx`'s prop type, `website/Index.tsx`'s
  `FaqDraftState`, and implicitly at the `navigate()` call site in
  `questions/Index.tsx`). The fix already touches all three to add a
  restaurant id — worth exporting one `FaqDraft` type from
  `types/website.ts` in the same edit rather than leaving a fourth inline
  literal to drift out of sync later. Preference, not a standards
  candidate — first time this exact shape has been triplicated on this
  board.
- `WebsiteFaqForm`'s `draftRowIndex` state is set once and never reset to
  `null`. Harmless in practice — `autoFocus` only fires at DOM-node
  creation, and nothing re-keys that row afterward — so not worth a line
  in the ticket log, noted here only for completeness.

**Genuinely good work, worth saying plainly:** throwing from `queryFn`
instead of copying `feedback/Index.tsx`'s swallow-into-`[]` idiom is
exactly right, and done against local precedent on the design's own
explicit instruction not to copy it — the kind of thing that's easy to
"helpfully" match instead. The live-RLS verification run before any code
was written (Notes' required first step) is exactly the gate the design
asked for, and it's logged with the actual policy text, not just "checked."

**Verdict: FAIL, round 1.** No receipt written
(`agents/principal-engineer/reviews/ENG-041.md` stays absent — pass-only,
per `code-review-gate/SKILL.md` step 8). QA's side of this combined hop
discarded per step 9 before a test-plan would have mattered; no
`agents/qa/test-plans/ENG-041.md` written. The build/lint/test
independent re-verification above stands as this pass's own due diligence,
not a quality-gate receipt.

## ENG-041 (round 2, restaurant-portal) — REVIEW pass

Fix-only delta `81b00b1..64f9e82`, 6 files, +79/-16. Re-derived round 1's
own repro against the new code by hand rather than trusting "restaurantId
now flows through": A → add-to-FAQs → land on `/website` scoped to A →
switch to B → `WebsiteFaqForm` remounts against B with a fresh
`draftConsumedRef` → `faqDraft.restaurantId ('A') !== currentRestaurantId
('B')` → discarded. Holds.

**Verified the regression test, not assumed.** Swapped in the pre-fix
`WebsiteFaqForm.tsx` (`git show 81b00b1:src/components/website/WebsiteFaqForm.tsx`
over the working copy), ran `WebsiteFaqForm.test.tsx` alone: the new
"does not surface a draft scoped to a different restaurant" case fails —
the mismatched draft's input renders where the fix discards it — and only
that case; the other three stay green. Restored via `git checkout --`,
confirmed the worktree clean before moving on. This is the first time this
notebook has mutation-tested a fix against the *literal* prior commit
rather than a hand-edited local mutation — cheaper when the "old code" and
the "new code" are both already sitting in the branch's own history.

One coverage gap surfaced (AC1's scoping had no test of its own) — QA's
finding, not a review fail, logged in `agents/qa/test-plans/ENG-041.md` and
closed there this same hop.

**Verdict: PASS, round 2.** Receipt: `agents/principal-engineer/reviews/ENG-041.md`.
0/10 automatic failures, independent build/lint/test/typecheck
re-verification all match the ticket log's own numbers exactly. Full
trace in the receipt itself — this entry is the notebook pointer per
`skills/code-review-gate/SKILL.md`'s output table, not a duplicate.
