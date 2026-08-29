---
id: ENG-021
title: Website chat-bar engagement visibility — customer questions and self-service FAQ editing on the brand portal
project: restaurant-portal
type: feature
size: M
time_estimate: a day to a day and a half
time_spent:
time_remaining:
severity: P2
priority:
state: shaped
owner: product-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-08-29
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-021-chat-bar-engagement-and-faq-self-service.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

Restaurant owners can't see that customers are using the AI chat/search bar on
their website, and have no way to turn a real customer question into a better
FAQ answer — even though every question is already logged per-restaurant and
the database already grants the owner's own account read access to it. The
FAQ content the bot answers from is staff-only to edit today; the brand
portal has no editor for it at all.

## Outcome

A restaurant owner, on the brand portal, can see the real questions customers
asked their chat bar (their own restaurant only), and create or edit a
website FAQ entry directly from that view — writing to the same data the bot
already reads, so the fix takes effect on the next customer question, with no
staff involvement required.

## Notes

Grounded in a live-code investigation across four repos before writing the
PRD — see `agents/product-manager/specs/ENG-021-chat-bar-engagement-and-faq-self-service.md`
Readback for the full comparison. The load-bearing facts for whoever designs
this next:

- The widget is `config-site-builder`'s `AISearchBar`/`ChatPanel`, rendered
  site-wide via `Layout.tsx` behind a per-restaurant `showAIChat` flag —
  live today, not hypothetical.
- Every turn is written by `aiorders-api`'s `ai-search-openrouter` edge
  function to `ai_conversations` (`session_id`, `restaurant_id`, `messages`
  jsonb, timestamps) — one row per session, full transcript in `messages`,
  not one row per question.
- `ai_conversations` already carries an RLS policy titled "Restaurant
  managers can view their restaurant conversations" (`restaurant-portal`
  migration `20250903152559_...sql`) — the read-access grant for this exact
  feature already exists and nothing reads it.
- The bot's FAQ source is `restaurant_website.faqs`, edited today only in
  `aiorders-admin-hub`'s `RestaurantAIWebsite.tsx` via direct Supabase
  `.from('restaurant_website')` calls — no edge function in the write path.
  `restaurant-portal` has a same-named but **unrelated** FAQ list
  (`CateringFaq`, in `CateringPageForm.tsx`) scoped to the catering landing
  page only — do not confuse the two or wire the new editor to the wrong
  field.
- `restaurant-portal` already reads/writes `restaurant_website` directly
  today for a different section (`src/pages/hiring/Index.tsx`, careers
  content) — that's the precedent pattern for the new FAQ editor, and
  evidence (not proof — the literal RLS policy on `restaurant_website` was
  not read) that the owner's account can already write to this table.
- No "answered / unanswered" or confidence signal is stored anywhere today —
  don't assume one exists when designing the questions view.
- A `cleanup_old_ai_conversations` DB function exists (referenced in
  generated Supabase types) but its definition/schedule isn't in any of the
  four repos' migrations — likely configured directly in the database.
  Retention isn't something this ticket controls either way.

## Log

- 2026-08-29 `intake → shaped` (product-manager) — sized M, project
  `restaurant-portal`. Ran the full request-readback
  (`skills/request-readback/SKILL.md`): this PM's own reading, grounded in
  live code across `config-site-builder`, `aiorders-api`,
  `aiorders-admin-hub`, and `restaurant-portal` (all four worktrees already
  present on this host at `~/Documents/_eng/`, per `ENG_WORKTREES`
  resolution — no worktree creation needed this pass); a blind architect
  reading (subagent, opus, raw request + `knowledge/business-profile.md`
  only, no repo access, no exposure to this PM's own reading). **No material
  divergence** — both independently converged on the same core shape:
  capture → surface to the owner → act via FAQs, on the brand portal. Full
  comparison in the PRD's Readback section.
  **Caps checked fresh from `inbox/` directly, not the cached board header:**
  found `ENG-014`'s and `ENG-015`'s G1s (`inbox/2026-08-29-eng014-g1-scope.md`,
  `inbox/2026-08-29-eng015-g1-scope.md`) both now carry `decision: approved`
  (decided 15:54:50 and 16:12:24 respectively) — answered, but neither
  ticket's own frontmatter has been advanced past `state: awaiting-scope,
  owner: approver` yet by a `decision` pass. Per this event's own narrower
  contract (act on the intake card given, not the whole board) this pass
  does not process those two decisions itself — that's a `decision` event's
  job and appears to already be in flight independently. For this ticket's
  own purposes, treated conservatively as **still occupying both
  approver-facing WIP slots** (mechanical ticket state, not the answered-but
  -unprocessed G1 text) — logged as an observation for the dead-end/decision
  sweep rather than acted on here. Approver-facing WIP therefore read as
  2/2, at cap, going into this pass.
  **Held at `shaped`, not advanced to `awaiting-scope`** — same reason and
  same move as `ENG-020` earlier today: nothing new should start down a path
  that needs the approver until `ENG-014` or `ENG-015` actually clears.
  G1 content (readback, both readings, non-goals, recommendation) is fully
  drafted in the PRD's Decision section and ready to raise the moment a slot
  frees. 1 transition (`intake → shaped`), well under the 4-transition cap.
  No `inbox/` item raised this pass (no G1 yet), so no `lib/eng-notify.sh`
  call. `chained: none` — held by the approver-facing WIP cap, not blocked
  or waiting on a human for this ticket specifically; re-check once a
  `decision`/`watch`/`scheduled` pass actually clears `ENG-014` or `ENG-015`.
