# PRD — FoodSwipe channel-visibility toggles and capability-based discovery (ENG-026)

## Readback

**You said** (original request title, `agents/product-manager/inbox/_handled/2026-09-01-eng-011-on-the-brand-portal-i-want-option-to-make-the-restau.md`):
> on the brand portal i want option to make the restaurant visible on order food, dine in and catering separately

**The body's three tasks** (operational time-clocks, smart dine-in/catering filters, promo badge overlay) never added a per-channel on/off toggle — both the PM's own reading and a blind architect reading converged on that gap independently, raised as `inbox/2026-09-01-eng026-visibility-toggle-question.md`, two readings offered (A: the three tasks are the whole ask; B: a real toggle is also wanted alongside them).

**You answered** (`decided: 2026-09-03T00:58:19Z`, full text preserved in the question item's own `## Decision`):
> 1. MASTER CAPABILITY TOGGLES... `has_order_food` (default: true), `has_dine_in` (default: false), `has_catering` (default: false)... 2. CONSUMER DISCOVERY... Channel tabs/filters must display all merchants where the corresponding toggle is true. Do NOT automatically hide closed restaurants... 3. "OPEN NOW" USER FILTER (OPT-IN ONLY)... 4. API QUERY LOGIC... [full text in the question item]

**Understood as:** Reading B, confirmed — and specified precisely enough that no further interpretation is needed. This isn't a bare "yes, add a toggle": it names the exact fields, exact defaults, exact discovery behavior (capability-gated, not availability-gated), and exact query semantics. Nothing about this answer needs a second blind reading — an approver-authored spec doesn't get re-interpreted, per the same precedent `ENG-009` set reusing `ENG-008`'s already-a-spec answer rather than re-running a fresh readback on it.

**Not re-litigated:** whether a toggle should exist at all. That's settled. What follows is scoping *only* what this answer actually specifies, versus what the original request's other three tasks still ask for.

## Why this ticket is narrower than the original request

The original raw request bundled four materially different capabilities behind one title:
1. **Channel-visibility toggles + capability-based discovery** — what your answer above fully specifies.
2. **Operational status engine** (kitchen cutoffs, alcohol-license time, happy-hour schedule, a live `getVenueOperationalStatus` helper).
3. **Smart dine-in/catering filters** (capacity, AV amenities, lead time, minimum spend).
4. **Promo badge overlay** on venue cards/video feed.

Items 2–4 have their own risk profiles and don't depend on each other, and your own answer only speaks to item 1. Per this department's standard practice for a multi-part request (the same reasoning `ENG-008`/`ENG-009`/`ENG-010` split three capabilities out of one influencer-board ask), this ticket is scoped to **item 1 only**. Items 2–4 are named as deferred follow-on work below, not dropped — filing them as separate tickets now would be scope beyond what this event actually unblocked; a future intake pass can pick them up individually once this foundation ships, since 3 and (arguably) 2 read as UI layered on top of a channel that already has to exist first.

## Problem

FoodSwipe (the consumer discovery app) and the tools that manage what appears on it have no way to say a merchant participates in one ordering channel (order food) but not another (dine-in, catering). Every merchant is implicitly "in" everywhere, so there's no way to keep a merchant that only does delivery out of a "Dine-In" tab, or vice versa.

## Outcome

A merchant's participation in each of three channels (order food, dine-in, catering) is an explicit, staff-set flag. FoodSwipe's channel tabs/filters show exactly the merchants enabled for that channel — including ones currently closed or past their cutoff, marked with their status — unless the consumer explicitly opts into an "Open Now" filter, which then hides closed ones for that channel only.

## Requirements

1. **[Confirmed]** Three independent boolean fields per merchant: `has_order_food` (default `true`), `has_dine_in` (default `false`), `has_catering` (default `false`).
2. **[Confirmed]** Consumer-facing channel tabs/filters (Order Food, Dine-In, Catering) on FoodSwipe display all merchants where the corresponding flag is `true` — this is the *only* gate on inclusion; open/closed status is not.
3. **[Confirmed]** A merchant that is closed or past its cutoff still appears (when its flag is true), shown with a status string (e.g. "Closed — Pre-order for tomorrow", "Opens at 5 PM") rather than being hidden.
4. **[Confirmed]** "Open Now" is an explicit, user-initiated filter chip, default off. Only when a consumer turns it on does the query additionally exclude merchants currently closed or past cutoff *for that channel*.
5. **[Confirmed]** API query shape: base filter `WHERE has_[channel] = true`; when `open_now = true`, additionally evaluate operating hours/cutoffs for that channel against the current time and exclude closed ones; when `open_now = false` (default), return every capability-true merchant regardless of current open/closed state.
6. **[Proposed]** The three flags are set by staff via `aiorders-admin-hub`'s existing merchant/store admin surface, not by the restaurant owner via the self-service brand portal (`restaurant-portal`). Reasoning: the original request's own second half explicitly frames this as "internal FoodSwipe / AIOrders.io staff management portal" work, and every prior FoodSwipe-adjacent ticket on this board (`ENG-008`/`009`/`010`) is staff-managed via `aiorders-admin-hub`, not owner-self-service. **Flag this at G1 if wrong** — self-service editing via `restaurant-portal` is a materially different, larger surface (auth, a new form, restaurant-scoped write access) and would change this ticket's shape, not just its detail.
7. **[Inferred, flagged as a risk, not resolved here]** Existing merchants have no current value for these three flags. A straight column-default migration would set every existing merchant to `has_order_food: true, has_dine_in: false, has_catering: false` — which, if any currently-active merchant actually does dine-in or catering today, would silently drop them out of those tabs the moment this ships, the opposite of the "don't hide" principle requirement 3 just established. This needs an actual backfill decision against live data (is there *any* existing signal — a `service_type`/`tags` field, a boolean elsewhere — worth defaulting from, or does every existing merchant genuinely start from a blank slate and wait for staff to opt them in?), which is design-time work against the live schema, not PM-level scoping. Named here so the architect doesn't skip it the way `ENG-010`'s own RLS gap slipped past design and round-1 review.

## Non-goals (this ticket)

- Operational time-clocks, cutoffs, happy-hour scheduling, or the `getVenueOperationalStatus` engine — deferred, future ticket.
- Smart dine-in/catering filters (capacity, amenities, lead time, spend) — deferred, future ticket.
- Promo badge overlay — deferred, future ticket. (Also worth a design-time look: the raw request lists this under the *internal admin* field-groups section but annotates it "to be controlled from brand portal not admin portal" — an internal inconsistency in the original request itself, not something this PRD resolves.)
- Restaurant self-service editing of the three flags via `restaurant-portal` — see requirement 6's proposed default.

## Risks

- **Rollout/backfill** — requirement 7 above. The one thing this ticket cannot get wrong the same way `ENG-010`'s PRD named its own: shipping this must not make an already-active merchant disappear from a channel it's actually doing business in today.
- **Scope surface** — likely the board's first **three-repo** ticket (`aiorders-api` for schema + query, `aiorders-admin-hub` for the staff-facing toggle UI, `restaurant-marketplace` for consumer discovery/filtering), one more than `ENG-011`'s two. Named explicitly rather than discovered mid-build.

## Cost

Rough band: **half a day to a day** — a three-boolean migration plus query-shape change (`aiorders-api`), a small toggle UI on an existing admin surface (`aiorders-admin-hub`), and a discovery-query/filter-chip change on the consumer app (`restaurant-marketplace`). No new infrastructure, no new dependency expected.

## Acceptance criteria

1. Migration adds all three flags with the stated defaults; existing behavior for `has_order_food` (default `true`) does not regress current Order Food discovery.
2. Staff can view and set all three flags per merchant from `aiorders-admin-hub`.
3. FoodSwipe's Dine-In and Catering tabs show only merchants with the respective flag `true`; a merchant with the flag `false` never appears there regardless of "Open Now" state (negative case).
4. A flag-enabled merchant that is currently closed still appears by default, with a status string, and is excluded only when "Open Now" is explicitly on.
5. The rollout/backfill question (Risk, above) has an explicit, evidence-based answer on file before this reaches `building` — not silently defaulted.
