---
ticket: ENG-021
project: restaurant-portal
status: draft
size: M
author: product-manager
created: 2026-08-29
decided:
---

# Website chat-bar engagement visibility — customer questions and self-service FAQ editing on the brand portal

## Readback

**You said:** "the search /chat bar engagement on website is not displayed/visible on the brand portal. so unable to show restaurant owner its benefit of help them make their faq's better

restaraut customers visit or questions on the serch/chat bar but we are not able to make it useful for them or the restaurant owners"

**Understood as:** Every restaurant's public website already has a live AI search/chat bar that customers use to ask real questions. None of that activity — the questions themselves, or the fact that it's happening at all — is visible anywhere on the brand portal, so the restaurant owner has no way to see the feature is working or to use real customer questions to improve the FAQ content the bot answers from. This is a visibility and self-service gap, not a missing capability in the chat bar itself.

**Assumed, and worth correcting if wrong:**
- "Search bar" and "chat bar" are the same widget, not two separate features (confirmed in code: one component, `AISearchBar`, opens the chat panel).
- "Make their FAQ's better" means the owner should be able to act on what they see — at minimum add/edit the FAQ content the bot uses — not just view a report and then email AIOrders staff to make the actual change. Read literally against this board's current self-service pattern (ENG-014, ENG-015, ENG-019).
- The relevant "FAQs" are the general website FAQs the chat bot draws its answers from — not the separate, catering-page-specific FAQ list restaurant-portal already lets owners edit today (confirmed these are different fields; see Risks).
- Scope is the brand portal (owner-facing), per the literal request — not a staff-facing admin-hub view. A staff-facing mirror is plausible future value but isn't what was asked.

**Second reading agreed / diverged on:** Ran the full request-readback — this PM's own reading, grounded in live code across `config-site-builder`, `aiorders-api`, `aiorders-admin-hub`, and `restaurant-portal`, plus a blind architect reading (subagent, opus, raw request + business profile only, no repo access). **No material divergence** — both independently converged on the same core shape: capture → surface to the owner → act on it via FAQs, as a closed loop, on the brand portal. The architect's reading, reasoning from first principles with no code access, correctly flagged as open questions several things this PM's code-grounded reading was able to confirm directly: whether queries are already captured at all (yes — durably, per-restaurant), whether the owner already has backend read access to that data (yes, via an existing but entirely unused RLS policy), and who authors the FAQ content today (AIOrders staff only, in the internal admin tool). None of these resolutions changed the shape of the request, only its cost — this is cheaper to build than either reading alone would have suggested, because most of the plumbing already exists. The architect additionally raised PII-in-free-text and an "answered vs. unanswered" quality signal as considerations; both are carried into Risks/Non-goals below rather than the acceptance criteria, since neither is what the literal request asks for.

## Problem

Restaurant owners cannot see that customers are using the AI chat/search bar on their website, and have no way to turn a real customer question into a better FAQ answer — even though every question is already durably logged per-restaurant, and the database already grants the owner's own account read access to that exact data. Separately, the FAQ content the bot actually answers from can only be edited by AIOrders staff in the internal admin tool today; the brand portal has no editor for it at all. The combined cost: AIOrders can't show owners the AI feature is doing anything (a retention/value-demonstration problem for AIOrders), and an owner who wants their bot to answer better has no path to that except asking staff.

## Why now

Same shape this board has already built twice this week: extend an admin-only capability to brand-portal self-service (`ENG-014`, `ENG-015`, `ENG-019`), and surface a capability that's already wired end-to-end but invisible to the person it would help most (`ENG-020`, same day). This ticket is both at once, on a feature — the chat bar — that is already live on restaurant websites today, not something hypothetical.

## Users

Restaurant owners/managers using the brand portal (`restaurant-portal`). AIOrders itself benefits too — this is the first concrete, owner-visible evidence that the chat bar feature it already ships is doing something.

## Proposed change

On the brand portal, a restaurant owner can:
1. See the real questions customers have asked their restaurant's chat bar — their own restaurant's only.
2. Turn one of those questions into a new (or edited) FAQ entry, directly from the brand portal, without contacting AIOrders staff.
3. Trust that the FAQ they just wrote is the same content the bot uses to answer the next customer — not a disconnected copy.

## Acceptance criteria

1. `[stated]` Given a restaurant with the chat bar enabled, when its owner opens the brand portal, then they can view the questions customers have asked via that chat bar for their own restaurant, and never another restaurant's.
2. `[inferred]` Given a restaurant with no chat-bar activity yet, when the owner opens this view, then they see a plain empty state, not an error or a blank screen.
3. `[stated]` Given the owner is viewing customer questions, when they decide one is worth an FAQ, then they can create or edit a website FAQ entry directly from the brand portal, with no staff involvement.
4. `[inferred]` Given an FAQ entry the owner creates or edits from the brand portal, when a customer next asks a related question on that restaurant's chat bar, then the bot's answer draws on that same updated content — the brand-portal editor and the bot read/write the same FAQ data, not a separate list.
5. `[inferred]` Given the existing staff-only FAQ editor in the admin portal, when either surface edits a restaurant's FAQs, then both stay in sync — the same underlying data, two editors, not two sources of truth.
6. `[proposed]` Given a restaurant owner with many logged questions, when they open the view, then questions are presented legibly (e.g., most-recent-first, one question per row) rather than as a raw multi-turn chat transcript the owner has to parse.

## Non-goals

- Scoring or flagging which questions the bot answered *badly* — no "answered vs. unanswered" signal exists today, and building one is a new measurement layer, not this ticket. Ships as a real-questions log; a quality/gap metric is a follow-on if this proves valuable.
- Clustering or de-duplicating near-identical phrasings across sessions. Nice-to-have; the acceptance bar is legible, not analytically summarized.
- A staff-facing (admin-hub) mirror of this same view. Plausible future value for AIOrders' own sales/retention conversations; not what was asked.
- Any change to the chat bar's own runtime behavior, answer quality, or which restaurants have it enabled.
- Any change to how long conversations are retained (an existing `cleanup_old_ai_conversations` job already purges old rows; this ticket doesn't touch it).
- Redacting or scrubbing PII from customer questions before display. See Risks — this is a design/security-gate question, not something this PRD resolves by omission.

## Risks and unknowns

- **PII in free-text queries.** Customers can type anything into the chat bar, including phone numbers, names, or health/allergy details. The owner is arguably the right custodian of their own customers' data (the database's existing access rule already assumes this), but the architect and security gate should look at this plainly rather than it being an accident of shipping a log viewer.
- **RLS on the FAQ table, assumed rather than confirmed.** This PM did not read the literal RLS policy text for the FAQ table (`restaurant_website`) — the assumption that the owner's account already has write access is based on a sibling brand-portal page (`hiring`, careers content) already reading and writing that same table directly. The architect should confirm this at design time rather than carry the assumption further.
- **Retention window is unknown.** A cleanup job already purges old conversation rows on a schedule this PM could not find in any repo (likely configured directly in the database). The questions view is bounded by whatever that job already keeps — worth knowing, not worth blocking on.
- **Query volume per restaurant is unknown.** If most restaurants have very little chat-bar activity, the value story is thinner than the request's framing assumes. Worth a quick data check at design time rather than a guess here.

## Cost

- **Build:** `M` — a day to a day and a half. Touches `restaurant-portal` only: a new view over already-logged conversation data, plus a new FAQ editor against a table the app already reads and writes elsewhere in the same portal. No new backend endpoint or edge function anticipated — both the conversation log and the FAQ content are already reachable by direct, authenticated Supabase queries today. Displaces one slot in an already-full board; see Decision.
- **Run:** $0/month. No new infrastructure, no new API calls — reuses existing tables and the existing direct-Supabase-client pattern already used elsewhere in this portal.

## Decision

Filled in after G1.

- **The approver's answer:**
- **Date:**
- **Notes:**
