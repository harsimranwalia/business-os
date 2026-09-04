---
id: ADR-013
title: The chat-bar questions view reads `ai_conversations` directly under RLS; the FAQ write goes through `brand-portal`
project: restaurant-portal
ticket: ENG-021
status: accepted
decided_by: architect
date: 2026-09-03
supersedes:
superseded_by:
---

# ADR-013: The chat-bar questions view reads `ai_conversations` directly under RLS; the FAQ write goes through `brand-portal`

## Context

`ENG-021` needs two data paths on the brand portal: a read of customers'
chat-bar questions, and a write of the FAQ content the bot answers from. The
obvious instinct is to make them consistent — both direct, or both through the
`brand-portal` edge function. This ADR records why they are deliberately not.

`ADR-006` established this codebase's standing rule: where a table's RLS state
cannot be verified from tracked migration history, do not make RLS the
enforcement boundary — enforce scoping in code, through the service-role client,
and treat the untracked policy state as unknowable rather than assumed. That
rule was written against `brands` and `restaurants`. Applying it here requires
asking the question per-table, and the two tables give opposite answers.

**`ai_conversations` — the policy is tracked and readable.**
`restaurant-portal/supabase/migrations/20250903152559_7f6d7f50-687d-45d0-abcf-a9cf3882cf81.sql`
contains a literal `ALTER TABLE public.ai_conversations ENABLE ROW LEVEL
SECURITY` and `CREATE POLICY "Restaurant managers can view their restaurant
conversations" ON public.ai_conversations FOR SELECT USING
(user_has_restaurant_access(auth.uid(), restaurant_id::uuid))`, and
`user_has_restaurant_access`
(`aiorders-api/supabase/migrations/20250729143357_initial_restaurant_rls.sql`)
resolves to `EXISTS (SELECT 1 FROM restaurant_managers WHERE user_id = ... AND
restaurant_id = ...)`. Read, not inferred. This is exactly the condition
`ADR-006`'s own Review trigger names — "if RLS policies are ever reconciled into
tracked migrations, revisit."

**`restaurant_website` — zero tracked policies.** `git grep` for
`CREATE POLICY` / `ENABLE ROW LEVEL SECURITY` against that table across both
`aiorders-api` and `restaurant-portal` migration histories returns nothing. Its
live RLS state is unknowable from the repos: the same gap `ADR-006` recorded for
`brands`.

Two further facts decided the write side. First, the PRD's stated precedent for
a direct client write — `restaurant-portal/src/pages/hiring/Index.tsx` — does
not exist: that file contains no `.from(` call at all and reaches
`restaurant_website` only through `brand-portal`'s `get_jobs` / `update_jobs`.
The real precedent is `src/pages/website/Index.tsx`, which uses
`get_website_content` / `update_website_content`. Second, a direct client write
would trip automatic review failure #9 (direct datastore write bypassing the
project's data layer).

`restaurant-portal` does have a widespread direct-read convention — 30+
`.from()` call sites across `Dashboard`, `campaigns`, `updates`, `offers`,
`influencers` and `restaurant_managers` — so the read side is not inventing a
pattern either way.

## Decision

**Read:** `src/pages/questions/Index.tsx` queries `ai_conversations` directly
through the ambient RLS-scoped Supabase client, bounded
(`.eq('restaurant_id', ...)`, `.order('updated_at', desc)`, `.limit(100)`, keyset
`.lt()` for older pages). No new `brand-portal` action.

**Write:** the FAQ editor goes through the existing `brand-portal`
`update_website_content` action, whose allow-list gains `'faqs'`. The
service-role client and the handler's code-side ownership check are the
boundary; `restaurant_website`'s own RLS is never depended on.

The split is the point: each path is guarded by whichever boundary is actually
verifiable for that table.

The read path carries **one precondition** the repo cannot satisfy. No tracked
migration creates `ai_conversations` — only the RLS migration exists — so
nothing proves that migration was applied to the live project. If RLS is not
enabled there, default `authenticated` grants make the table wholly readable and
AC1's server-side half is unmet. `database` therefore verifies RLS-enabled and
policy-present against `bmnmnejwdxbcqinqkwko` **before** the build hop, and
**stops and reports** if it is not — at which point this decision inverts and
the read moves to a `brand-portal` action with an explicit `.hasAccess` check.

## Alternatives

| Option | Why not |
|---|---|
| **A new `get_ai_conversations` action on `brand-portal`** for the read | Adds an endpoint, a router case, a README entry and a deploy step to guard a query that a *tracked, readable* policy already guards correctly. It would also move the guarantee from a policy this design read the text of onto `verifyRestaurantAccess`, which is currently defeated in five of nine handlers in that directory (`ENG-022`, P0, unmerged) — trading a checkable boundary for one with a live open bug. Against the portal's own convention for "list my restaurant's records." Retained as the named contingency if the RLS precondition fails. |
| **A direct client `.from('restaurant_website').update(...)`** for the write, mirroring `aiorders-admin-hub/RestaurantAIWebsite.tsx` | Automatic review failure #9, and it makes a zero-tracked-policy table the enforcement boundary — precisely what `ADR-006` refused. The admin-hub does it, but it is a staff tool at a different trust level; copying the code into an owner-facing portal inherits the assumption without the trust. |
| **Route both paths through `brand-portal`,** for consistency | Consistency is not the goal; a verifiable boundary is. This buys an endpoint whose only advantage over RLS here would be uniformity, and pays for it with a deploy step and a second ownership check to keep correct. |
| **Route both paths through the direct client,** for consistency | Same objection from the other side, and strictly worse: it would put a write to a publicly-rendered, search-indexed column behind unverifiable RLS. |
| **Add tracked RLS policies to `restaurant_website`** as part of this ticket | Reasonable defense-in-depth and not rejected on merit — but it is a schema change on a shared table in service of a boundary this design does not use, bundled into a feature ticket. `ADR-006`'s own review trigger already owns this; it belongs to whoever closes the untracked-history gap. |

## Consequences

**Accepted:** one feature reads through RLS and writes through a service-role
edge function, and a future engineer touching this page will see two idioms in
one ticket. The reason has to be legible or it reads as drift — hence this ADR,
and hence the Alternatives table naming the per-table asymmetry explicitly. The
read path also inherits a dependency on live-project state that no repo records,
mitigated by making its verification a build precondition rather than an
assumption.

**Gained:** neither path depends on anything unverifiable. The read leans on a
policy whose text is in tracked history; the write leans on code, exactly as
`ADR-006` prescribes for a table whose policies are not. And the write reuses an
action, a router case and an ownership check that already exist, so `ENG-021`
adds no new endpoint, no migration and no new attack surface to `brand-portal`.

**Reversibility:** cheap in both directions. Moving the read behind an action is
additive — a new handler file, a router case, and swapping one `useQuery` body;
no data changes. Removing `'faqs'` from `EDITABLE_PAGES` reverts the write with
one deleted array element and no row touched.

## Review trigger

Revisit if `ENG-022` is *not* merged before this ships — the write path's guard
is open until it is, and that changes the risk calculus of widening the
allow-list. Revisit if `restaurant_website`'s RLS is ever reconciled into
tracked migrations (`ADR-006`'s own trigger), since the write side could then be
reconsidered on the same evidence basis the read side enjoys. And revisit
immediately if `database`'s precondition check finds RLS disabled on
`ai_conversations`: the read decision inverts to the contingency above, and the
"tracked policy" premise this ADR rests on turns out to describe the repo rather
than the database.
