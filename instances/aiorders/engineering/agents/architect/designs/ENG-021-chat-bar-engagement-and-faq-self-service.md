---
ticket: ENG-021
project: restaurant-portal
author: architect
created: 2026-09-03
adrs: [ADR-013, ADR-014]
one_way_doors: []
touches_data: true
touches_models: false
---

# Website chat-bar engagement visibility — customer questions and self-service FAQ editing — technical design

## Approach

Two small, independent additions to the brand portal, joined by one navigation
hop:

1. **A new top-level "Customer Questions" page** (`/questions`) that reads
   `ai_conversations` directly through the Supabase client, bounded to the most
   recent 100 sessions for the selected restaurant, flattens each session's
   `messages` to its `role: 'user'` turns, and renders one question per row,
   newest first.
2. **A third "FAQs" tab on the existing Website page**, editing
   `restaurant_website.faqs` through the `brand-portal` edge function's
   existing `update_website_content` action — which today allow-lists exactly
   two keys and needs a third.

The join is a per-row **"Add to FAQs"** button that navigates to the Website
page with the customer's question carried in react-router location state (not a
URL parameter) and pre-fills a new FAQ entry with it.

No new table, no new column, no migration, no new edge-function action, no new
route on the API router. Four findings from reading `origin/main` shaped this
rather than the version the PRD assumed.

**The PRD's assumed write mechanism does not exist.** The PRD and the ticket
Notes both name `restaurant-portal/src/pages/hiring/Index.tsx` as the precedent
for "the portal already reads and writes `restaurant_website` directly," and
treat that table's RLS as the open question to confirm. `hiring/Index.tsx`
contains no `.from(` call at all — every read and write goes through
`supabase.functions.invoke('brand-portal', { action: 'get_jobs' | 'update_jobs' })`.
The real precedent for "an owner edits `restaurant_website` content from the
brand portal" is `src/pages/website/Index.tsx`, which calls
`get_website_content` / `update_website_content`, implemented in
`aiorders-api/supabase/functions/brand-portal/website.ts`. So the design
question is not "may the owner's own JWT write this table" — it is "which key
may the service-role handler write on their behalf," and the answer is a
one-element widening of an existing allow-list. `restaurant_website`'s own RLS
never becomes load-bearing and does not need to be confirmed (which is
fortunate — it has zero tracked policies in either repo's migration history,
the same untracked gap **ADR-006** recorded for `brands`).

**`ai_conversations`'s RLS is real, and it is the one boundary here that can
actually be read.** `restaurant-portal/supabase/migrations/20250903152559_*.sql`
carries a literal `CREATE POLICY "Restaurant managers can view their restaurant
conversations" ... USING (user_has_restaurant_access(auth.uid(),
restaurant_id::uuid))`, and `user_has_restaurant_access`
(`aiorders-api/supabase/migrations/20250729143357_initial_restaurant_rls.sql`)
resolves to membership in `restaurant_managers` for that exact restaurant.
Correctly scoped, and verified by reading the policy text rather than inferring
it from a sibling page. That asymmetry — a *readable* policy on the read table,
an *unreadable* one on the write table — is what makes the split path in this
design (direct client read; edge-function write) the honest choice rather than
an inconsistency. See **ADR-013**.

**`website.ts`'s ownership check is defeated today, and it is already
ticketed.** `verifyRestaurantAccess` *returns* `{ hasAccess, ... }` and never
throws on denial (`brand-portal/utils.ts`; the throwing variant is the separate
`verifyRestaurantAccessLegacy`). `website.ts` calls
`await verifyRestaurantAccess(restaurant_id, supabase, user)` at both call sites
and discards the result — so a denied caller proceeds. This is **ENG-022**
(P0, `state: blocked`, `owner: approver`, PR #9 on
`fix/ENG-022-brand-portal-tenant-isolation`, confirmed **not** an ancestor of
`origin/main`), which names `website.ts` explicitly among its five files and
fixes it by swapping both call sites to a new throwing `requireRestaurantAccess`
helper. This design does not re-fix it — that is a bundled security fix, which
the standards forbid — but it does mean ENG-021 adds a **new owner write
capability to a handler whose gate is currently open**, and that ordering is a
real constraint, not a footnote. See Risks and Rollout.

**The FAQ column's blast radius is wider than the PRD knew.** `restaurant_website.faqs`
feeds three consumers, not one: the bot
(`ai-search-openrouter` selects `menu, deals, discounts, locations, faqs`
per restaurant), the public site's FAQ section
(`config-site-builder/src/pages/Home.tsx`, `LocationPage.tsx`, resolved by
`get-brand-website` straight from `restaurantData.faqs` with **no**
brand-metadata override — unlike `catering`, per ADR-009), and schema.org
`FAQPage` structured data emitted for search engines
(`config-site-builder/src/utils/structuredData.ts`). An owner-authored FAQ is
therefore published and indexed, not just read by a chatbot. That is good for
AC4/AC5 — one column, one source of truth, provably — but the editor has to
tell the owner what they are publishing.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `aiorders-api`: `supabase/functions/brand-portal/website.ts` | modify — add `'faqs'` to `EDITABLE_PAGES`; add `faqs: data?.faqs ?? null` to `getWebsiteContent`'s returned `content`; export `interface WebsiteFaq { question: string; answer: string }`. Widen the array's comment ("columns", not "pages"). **Three lines of behaviour; no other edit to this file** | backend |
| `aiorders-api`: `supabase/functions/brand-portal/index.ts` | **no change** — `get_website_content` / `update_website_content` are already routed | — |
| `aiorders-api`: `supabase/functions/README.md` | modify — `brand-portal`'s entry gains `faqs` in its DB-columns note. Required in the same commit by the repo's own `CLAUDE.md` ("After changing a function") | backend |
| `restaurant-portal`: `src/types/website.ts` | modify — add `WebsiteFaq` and `WebsiteContent.faqs: WebsiteFaq[] \| null`. **Not** a change to `CateringFaq` | frontend |
| `restaurant-portal`: `src/components/website/WebsiteFaqForm.tsx` | new — the top-level FAQ list editor. Mirrors `CateringPageForm.tsx`'s existing add/edit/remove idiom; seeds from `location.state.faqDraft` when present | frontend |
| `restaurant-portal`: `src/pages/website/Index.tsx` | modify — third `TabsTrigger`/`TabsContent` (`grid-cols-2` → `grid-cols-3`); read `useLocation().state?.faqDraft` to set `defaultValue` to `faqs` and clear the state after consuming it | frontend |
| `restaurant-portal`: `src/pages/questions/Index.tsx` | new — the questions view: bounded query, flatten, sort, render, empty/error states, "Add to FAQs", "Load older" | frontend |
| `restaurant-portal`: `src/App.tsx` | modify — one nested route `questions` under the existing `DashboardLayout` parent | frontend |
| `restaurant-portal`: `src/components/layout/Sidebar.tsx` | modify — one entry in the `navItemsAfter` array, directly above `Feedback` | frontend |
| `restaurant-portal`: `src/components/website/CateringPageForm.tsx` | **no change** — listed so nobody wires the new editor to `CateringFaq`, the catering-page-only nested array. Different field, different consumer | — |
| `aiorders-admin-hub`: `src/pages/RestaurantAIWebsite.tsx` | **no change** — the staff editor already writes the same column; AC5 is satisfied by not building a second store, not by touching it | — |

## Data

`touches_data: true`, but **no schema change of any kind**: no new table, no new
column, no index, no migration, no RPC. `database` is in the chain for a
**read-only verification against the live project** (`bmnmnejwdxbcqinqkwko`),
because three facts this design leans on cannot be established from the repos —
`ai_conversations` has no `CREATE TABLE` in any tracked migration, only an RLS
migration, so its live state is inferred from code and policy text alone.

`database` confirms, before the build hop starts:

1. **RLS is `ENABLED` on `public.ai_conversations` and the SELECT policy
   `"Restaurant managers can view their restaurant conversations"` exists and
   matches the migration text.** This is the load-bearing one. The migration is
   tracked, but nothing in the repos proves it was applied — and if RLS is off,
   default `authenticated` grants make the whole table readable and AC1's
   server-side half is unmet. **If it is not enabled, stop and report** — do not
   enable it inside this ticket, and do not proceed with the direct-read design.
   The contingency is named in Alternatives.
2. **The retention window** — the definition and schedule of
   `cleanup_old_ai_conversations` (referenced in generated types, defined in no
   repo). Informational: the view inherits whatever it leaves and this ticket
   does not change it, but the page's own copy should not promise history the
   job deletes.
3. **Per-restaurant session volume** — `count(*)` grouped by `restaurant_id`,
   plus the max. Sanity-checks the 100-session bound below. This was
   unverifiable at design time (no DB access this pass, and the PRD flagged it);
   the bound is chosen to be correct regardless, not to fit a number.

Also worth capturing while there, purely informational: whether
`public.restaurant_website` has RLS enabled and any policies at all. Nothing in
this design depends on the answer — the write path is a service-role edge
function with a code-side ownership check (ADR-006's pattern) — but it closes a
gap ADR-006 flagged and this design re-encountered.

## Interfaces

### `brand-portal` action `update_website_content` — widened payload

No new action, no new route, no signature change. The `content` object accepts a
third key:

```json
{ "action": "update_website_content",
  "restaurant_id": "<uuid>",
  "content": { "faqs": [ { "question": "Do you cater?", "answer": "Yes — ..." } ] } }
```

The handler's existing loop copies only keys present in `EDITABLE_PAGES`, so
`{ faqs }` is a **partial patch**: saving FAQs never reads, rewrites or clobbers
`catering` or `careers`, and vice versa. This holds because `faqs` is a
*top-level column* on `restaurant_website`, sibling to `catering`/`careers`/
`story`/`menu` — not a nested key — so there is no read-modify-write window
between tabs. `content.faqs = []` persists as `[]` (`?? null` only nulls on
null/undefined), which is how "the owner deleted every FAQ" is stored.

### `get_website_content` — widened response

```json
{ "success": true, "content": { "catering": {...}|null, "careers": {...}|null, "faqs": [...]|null } }
```

`faqs` is `null` when the restaurant has no `restaurant_website` row yet
(PGRST116, already handled) or the column is null; the editor renders an empty
list either way.

Failure responses are unchanged and inherited: `{ success: false, error }` at
HTTP 200 from this handler's own `try/catch`, or HTTP 401 from `index.ts` with
no Bearer JWT. Access denial currently produces **neither** — see Risks
(ENG-022); after ENG-022 merges it produces `{ success: false, error: 'Access
denied to this restaurant' }`.

### Questions query (direct Supabase client)

```
supabase.from('ai_conversations')
  .select('session_id, messages, updated_at')
  .eq('restaurant_id', currentRestaurant.id)
  .order('updated_at', { ascending: false, nullsFirst: false })
  .limit(100)
```

Bounded by construction — never an unfiltered or unlimited select (automatic
review failure #5). Two independent scoping layers: the explicit
`.eq('restaurant_id', ...)`, which is required for correctness anyway because an
owner may manage several restaurants and the page follows the selected one; and
RLS, which is what stops a caller hand-crafting a query for a restaurant they do
not manage. Neither is decorative.

**"Load older"** re-runs the same query with
`.lt('updated_at', <updated_at of the oldest loaded session>)` and appends —
keyset, not offset, because the bot upserts new rows continuously and an offset
window would skip and duplicate. The button is hidden when the last page
returned fewer than 100 rows, or when the oldest loaded session's `updated_at`
is null (both `updated_at` and `created_at` are nullable in the generated types;
a null-dated row is the undatable tail and cannot be a cursor).

### Client-side shaping (AC6)

`messages` is untyped `jsonb` with no schema enforcement, written by the bot as
`{ role, content, timestamp }` and trimmed server-side to the last 20 per
session. A defensive normaliser turns the fetched sessions into a flat
`{ sessionId, text, at }[]`:

| Input | Behaviour |
|---|---|
| `messages` is not an array | that session contributes zero rows; no throw |
| element is not an object, or `role !== 'user'` | skipped — assistant turns are never rendered (AC6, and it halves what is on screen) |
| `content` missing or not a non-empty string | skipped |
| `timestamp` missing or unparseable | falls back to the session's `updated_at`; if that is null too, the row sorts last rather than being dropped |

The flattened set is sorted by `at` descending across sessions — so the ordering
is by *when the customer asked*, not by which session was touched last — and
rendered one row per question with a relative timestamp
(`formatDistanceToNow`, the idiom `feedback/Index.tsx` already uses).

### Questions → FAQ hand-off

`navigate('/website', { state: { faqDraft: { question: text } } })`. The
question text travels in react-router's in-memory location state and **never in
the URL** — a customer's free-text question in a query string would land in
browser history and in every upstream access log, which is the "no PII in log
lines" rule broken by a different door. The Website page consumes the state,
opens the FAQs tab, appends one entry with the question pre-filled and the
answer empty and focused, then clears the state
(`navigate('.', { replace: true, state: null })`) so a refresh does not re-add
it. Nothing is saved until the owner presses Save.

### Portal page

`/questions`, nav label **"Customer Questions"**, placed immediately above
`Feedback` in `navItemsAfter` — both are streams of customer-generated records
scoped to one restaurant, and grouping them is how an owner will look for it.
Deliberately not a tab on Website (that page is content editing) and not part of
Feedback (that is post-order review data with ratings and order joins; merging
two different record types under one heading would make both harder to read).

## Alternatives considered

| Option | Why it lost |
|---|---|
| **A new `get_ai_conversations` action on `brand-portal`** for the read | Adds an endpoint and a deploy step for a query whose RLS policy is *tracked and readable* — the one boundary in this ticket that can actually be verified from the repo. It would also route the read through the very ownership helper that is currently defeated in five of nine handlers (ENG-022), trading a checkable guarantee for an unchecked one. Against the portal's own convention too: 30+ direct `.from()` reads across `Dashboard`, `campaigns`, `updates`, `offers`, `restaurant_managers`. **ADR-013.** This is the named contingency if `database` finds RLS disabled — then RLS is not a boundary and a handler with an explicit `.hasAccess` check becomes the only correct option. |
| **A direct client `.from('restaurant_website').update(...)` for the FAQ write**, mirroring the staff admin-hub editor | Automatic review failure #9 (direct datastore write bypassing the data layer), and it would make `restaurant_website`'s RLS load-bearing — a table with *zero* tracked policies, exactly the unverifiable state ADR-006 refused to depend on. The admin-hub does this, but it is a staff tool at a different trust level; copying it into the owner-facing portal inherits the trust assumption without the trust. |
| **A new `update_faqs` action** rather than widening `EDITABLE_PAGES` | A second write path to the same table, with a second copy of the ownership check to keep correct. The existing action's partial-patch semantics already do exactly what is needed; one array entry beats a new function. |
| **Put the FAQ editor on the questions page itself**, so AC3's "directly from that view" is literal | Two editors over one column inside one app, or the Website page's FAQ tab existing only as a duplicate. AC3's binding text is "directly from the brand portal, with no staff involvement" — the navigation hop with the question pre-filled satisfies that and keeps all website content editing in one place, which is where an owner will look for it the second time. |
| **Carry the question in a URL query parameter** instead of location state | Simpler and survives a refresh, but writes customer free text into browser history and upstream access logs. Location state costs nothing extra and keeps the text in memory. |
| **Fetch every session for the restaurant and paginate client-side** | Unbounded query (automatic review failure #5), unbounded payload, and pointless — the newest 100 sessions is what an owner reads. |
| **Deduplicate or cluster near-identical questions** | Explicit PRD non-goal. It is also the kind of thing that looks free and is not: "similar" needs a threshold, and a wrong one hides the question the owner needed to see. |
| **Copy `feedback/Index.tsx`'s error handling** (toast, then `return []`) | It makes a failed query indistinguishable from a restaurant with no activity, which is precisely the confusion AC2 exists to prevent. The new page throws from `queryFn` and renders a distinct error state with a retry. |
| **Fix `website.ts`'s discarded access check as part of this ticket** | It is ENG-022's, already designed, built, reviewed and sitting in an open PR. Re-fixing it here is automatic review failure #7 and would collide with that branch. Named as a dependency instead. |

## One-way doors

**None.** Each category from the skill's own list, checked:

- **New datastore / vendor / dependency:** none. Two existing tables, one
  existing edge-function action, one existing UI component library.
- **Auth model change:** no. Same principal, same enforcement point, same
  helper. `EDITABLE_PAGES` gains one entry — a widening of *which resource* an
  already-authenticated, already-ownership-checked caller may write, reversible
  by deleting one array element with no data to unwind.
- **Public contract:** no API shape changes; the widened `content` object is
  additive and its only consumer is `restaurant-portal`. The *content* does
  become public (site + schema.org FAQ markup), but that is the existing
  behaviour of an existing column, and it is reversible by editing the entry.
- **Data model painful to migrate:** no schema change at all.
- **Recurring cost:** none. No new infrastructure, no new API calls, no job.

Two decisions were worth a record and were decided here rather than escalated:
**ADR-013** (the read path) and **ADR-014** (showing customer text verbatim).

## Risks

**ENG-021 widens a write path whose gate is currently open — ENG-022 should
merge first.** On `origin/main`, `updateWebsiteContent` discards
`verifyRestaurantAccess`'s result, so any authenticated brand-portal user can
already write any restaurant's `catering` and `careers`. Adding `faqs` to the
allow-list extends that same hole to a column that is rendered on the public
site and emitted as search-engine structured data. **What the design does:** it
changes nothing about the check (that is ENG-022's fix, already built and in
PR #9) and instead states the ordering plainly — ENG-022 merges before ENG-021
ships. Recommended to the EM as a `depends_on: [ENG-022]` on this ticket; that
sequencing call is the EM's, not the architect's, so it is not written into the
frontmatter here.

**Direct textual collision with ENG-022's unmerged branch.**
`fix/ENG-022-brand-portal-tenant-isolation` rewrites `website.ts` — swapping
`verifyRestaurantAccess` for `requireRestaurantAccess` at both call sites and
changing the import. ENG-021 edits the same file, though in different regions
(`EDITABLE_PAGES`, the returned `content` object). This is the sibling-branch
staleness case, not a main-vs-branch one. **What the design does:** ENG-021's
build hop branches from `origin/main` *after* ENG-022 merges, and re-reads
`website.ts` and `utils.ts` at build time rather than trusting this document's
quoted source. If it must start earlier, it branches from ENG-022's branch, not
main, and the merge check is run against that sibling tip.

**Two editors, one column — last write wins.** AC5 asks for one source of truth
and gets it, but the price is that the staff editor
(`aiorders-admin-hub/RestaurantAIWebsite.tsx`) does a **whole-row upsert**
across `story`, `faqs`, and other columns. A staff member with a stale page open
who saves after an owner's FAQ edit overwrites it silently, and there is no
version column, ETag or `updated_at` precondition on the table to detect it with.
**What the design does:** accepts it, and does not build an optimistic-concurrency
layer for a two-writer, low-frequency surface — that is structure for a problem
nobody has reported. Mitigations that cost nothing: the portal's existing
`saveMutation.onSuccess` already invalidates and refetches, so the owner always
sees the stored truth immediately after saving; and the owner-side patch sends
**only** `{ faqs }`, so it can never be the one clobbering `catering`/`careers`.
The exposure is one-directional (staff can overwrite owner, not the reverse) and
named here so a future report of "my FAQ disappeared" has an explanation waiting.

**An owner's FAQ text enters the bot's prompt context.** `touches_models` is
`false` and that is a deliberate call, not an omission: no model call is added,
removed, rerouted or reconfigured, and six of the seven required AI-architecture
subsections would read "unchanged." The one genuine change is prompt
provenance — the set of principals who can write text the bot reads widens from
AIOrders staff to restaurant owners. **What the design does:** notes that this
widens nothing new. `ai-search-openrouter` already builds its context from
`menu`, `deals`, `discounts` and `locations` alongside `faqs`, and the same owner
already edits menus and offers through this same portal (`menus.ts`,
`offers.ts`). An owner writing instruction-shaped text into their own FAQ can
only affect their own restaurant's bot, which they already control by three
other routes. If prompt-injection hardening is wanted, it belongs to the bot's
own ticket and covers all five inputs, not this one.

**PII in customer questions.** Free text; customers type names, phone numbers,
allergies. **What the design does:** ADR-014 — the owner is the custodian the
database's own tracked policy already names, the questions are shown verbatim,
and the concrete controls are that nothing is copied or persisted anywhere new,
the text never enters a URL or a log line, only the customer's own turns are
rendered (never the bot's replies), and there is no export button. Redaction is
a PRD non-goal and would be the wrong first move — a regex scrubber over open
text both over-redacts the allergy question that made the page worth building
and under-redacts most real identifiers.

**Volume and retention are unverifiable from the repos.** No migration creates
`ai_conversations`; `cleanup_old_ai_conversations` is referenced in generated
types and defined nowhere in the four repos. **What the design does:** the query
is bounded at 100 sessions regardless of the true distribution, so it is correct
whether a restaurant has 3 sessions or 30,000, and `database`'s verification pass
(Data, item 3) turns the guess into a number before the build.
**Review trigger:** if the confirmed max sessions per restaurant is under ~20,
the "Load older" control is dead weight and should be dropped; if a single page
of 100 sessions routinely exceeds ~1MB of `messages` payload, the bound moves
down and the select narrows.

**Pre-existing `deno check` noise in `website.ts`.** `.select(EDITABLE_PAGES.join(', '))`
produces a runtime-computed column string that supabase-js's generics cannot
infer, and that error is already one of the 10 known pre-existing failures
`ENG-022`'s build hop catalogued (`observations.md`, 2026-09-03). Adding a third
key does not change its shape or its count. **What the design does:** the build
hop must not "fix" it in passing (automatic review failure #7) and must add no
new errors.

## Rollout

Straight, in two ordered steps, no feature flag — the page does not exist until
its route is added, which is the flag.

0. **Precondition:** ENG-022 merged (see Risks), and `database`'s live-project
   verification returned RLS enabled on `ai_conversations`.
1. **API first.** Deploy `brand-portal` with `faqs` in `EDITABLE_PAGES`. Purely
   additive: no existing caller sends or reads the key, and the response gains a
   field the current portal ignores.
2. **Portal second.** Deploy `restaurant-portal` — route, nav entry, FAQ tab and
   questions page ship together.

If step 2 somehow lands first, the FAQ tab renders an empty list and a save
fails with the handler's existing `content must include at least one of:
catering, careers` error surfaced through the page's existing error toast — a
visible failure, not a silent no-op. The questions page is unaffected by step 1
entirely.

**Rollback:** remove the nav entry, the route and the third tab from
`restaurant-portal` and redeploy. `faqs` may stay in `EDITABLE_PAGES`
harmlessly, or be removed in the same revert; either way no row is migrated and
any FAQ the owner already saved stays live on the site and in the bot, exactly
as a staff-authored one would.

**Verification.** `restaurant-portal`: `npm run test`, `npm run lint`,
`npm run build`. `aiorders-api` has no `package.json`; run
`DENO_NO_PACKAGE_JSON=1 deno test --node-modules-dir=none` and the same env/flag
pair for `deno check` from the function directory, per this board's established
invocation. New code must add zero `deno check` errors to the known 10.

## Out of scope

- **Fixing `website.ts`'s discarded ownership check.** ENG-022, already built,
  PR #9. A dependency, not a task here.
- **Renaming `EDITABLE_PAGES` to something accurate** now that it holds a
  non-page column. Cosmetic, and a needless conflict with ENG-022's unmerged
  edit to the same file. The comment is widened; the identifier is not.
- **Redacting or scrubbing PII from questions.** PRD non-goal; ADR-014 states
  the position. If the security gate wants it, it is a follow-on with its own
  acceptance criteria.
- **Answered/unanswered quality scoring, clustering, deduplication** — PRD
  non-goals, all requiring a measurement layer that does not exist.
- **A staff-facing (admin-hub) mirror of the questions view.** PRD non-goal.
- **Optimistic concurrency between the two FAQ editors.** Named in Risks; needs
  a version column and a conflict UI, and no one has reported the collision.
- **Any change to retention or to `cleanup_old_ai_conversations`.** PRD non-goal;
  `database` reads its definition, changes nothing.
- **Per-location FAQs.** `get-brand-website` already supports
  `location.faqs || restaurantData.faqs`, but nothing in the portal writes the
  per-location variant and no acceptance criterion asks for it.
- **Export/download of questions.** Deliberately absent — see ADR-014.

## Acceptance criteria — walked

**AC1 — the owner views their own restaurant's chat-bar questions, never
another restaurant's.** Satisfied, by two independent layers: the query's
explicit `.eq('restaurant_id', currentRestaurant.id)`, and the tracked RLS
SELECT policy resolving through `user_has_restaurant_access` →
`restaurant_managers`. The policy text was read literally, not inferred. Its
*applied* state on the live project is the one thing this design cannot prove
from the repos, which is why `database` verifies it as a precondition and the
contingency (a `brand-portal` action with an explicit `.hasAccess` check) is
named in Alternatives rather than discovered later.

**AC2 — plain empty state when there is no activity.** Satisfied, and
deliberately distinguished from failure. Three distinct renders: loading; a
successful query returning zero rows *or* zero extractable user messages → the
empty state ("No one has used your website chat yet"); a failed query → a
separate error state with retry. This is why `feedback/Index.tsx`'s
swallow-into-`[]` idiom is not copied.

**AC3 — create or edit a website FAQ directly from the brand portal, no
staff.** Satisfied. The FAQs tab is a full add / edit / reorder-by-delete
editor over `restaurant_website.faqs`, writing through an action the owner's own
JWT already authorises. The stronger reading in the ticket's Outcome —
"directly from that view" — is met by the per-row "Add to FAQs" button that
carries the question across and pre-fills it, so the owner never retypes it and
never leaves the portal.

**AC4 — the FAQ the owner writes is what the bot reads.** Satisfied by
construction, not by synchronisation. `ai-search-openrouter` selects `faqs` from
`restaurant_website` for that `restaurant_id` on every request; the editor writes
that same column. There is no cache between them and no copy: the next customer
question reads the row as saved. (The *public site* additionally goes through
`get-brand-website`'s KV cache, which the `restaurant_website_cache_invalidation`
trigger — repaired by migration `20260807000004` — purges on every UPDATE and
INSERT to that table. So the site follows too, though no AC requires it.)

**AC5 — staff editor and owner editor stay in sync.** Satisfied, for the same
reason: one column, two editors, no second store, no sync process to fail. The
honest caveat is write ordering, not divergence — see Risks (last write wins);
the two surfaces can never hold *different* data, only a later save can replace
an earlier one.

**AC6 — legible, most-recent-first, one question per row, not a raw
transcript.** Satisfied. Assistant turns are never rendered; each user turn is
one row with its own relative timestamp; sorting is on the message's own
`timestamp` across sessions, so ordering reflects when the customer asked rather
than which session was touched most recently. Bounded to 100 sessions with an
explicit "Load older" rather than silent truncation, because AC6's own premise is
"an owner with many logged questions."

## Failure behaviour

| Situation | Behaviour |
|---|---|
| No restaurant selected | "Please select a restaurant" panel, matching `website/Index.tsx`'s existing copy. No query fires (`enabled: !!currentRestaurant?.id`) |
| Restaurant has no `ai_conversations` rows | Empty state, distinct from an error (AC2) |
| Sessions exist but every `messages` array is empty, malformed, or assistant-only | Same empty state — honest: there are no customer questions to show |
| A single session's `messages` is not an array, or an element is malformed | That session or element contributes nothing; every other row still renders. The normaliser never throws |
| A message has no parseable `timestamp` | Falls back to the session's `updated_at`; if that is null too the row sorts last but is still shown |
| Query fails (RLS denies, network, PostgREST error) | Distinct error state with retry. The PostgREST code is logged; the query payload and any question text are not |
| Owner clicks "Load older" at the end of the data | Fewer than 100 rows return, the button hides. No infinite spinner |
| Oldest loaded session has a null `updated_at` | No cursor is derivable; the button hides rather than re-fetching the same page forever |
| Owner saves an FAQ with a blank question or answer | Filtered out before the patch is sent, matching `CateringPageForm`'s existing rule (`f.question.trim() && f.answer.trim()`). A wholly blank list saves as `[]` |
| Owner deletes every FAQ and saves | `faqs: []` persists; the bot falls back to its non-FAQ context and the public site hides the FAQ section. Not an error |
| FAQ save fails (denied, network, handler error) | Existing destructive toast with the handler's message; local form state is preserved so nothing the owner typed is lost |
| Two saves in flight from the two tabs | Each patch carries only its own key, so they cannot clobber each other. Staff-vs-owner is the one real collision — see Risks |
| Owner refreshes after "Add to FAQs" without saving | Location state was cleared on consume; the draft entry is gone, nothing was written. Deliberate — an unsaved draft is not persisted anywhere |
| FAQ item carries keys beyond `question`/`answer` (written by a future staff surface) | The editor patches items by spreading (`{ ...faq, question }`), never by reconstructing `{ question, answer }`, so unknown per-item keys survive a round trip. This is ADR-009's clobber lesson applied one level down |
| ENG-022 unmerged when this ships | The FAQ write is reachable cross-tenant, same as `catering`/`careers` today. Prevented by ordering, not by code in this ticket — see Rollout step 0 |
