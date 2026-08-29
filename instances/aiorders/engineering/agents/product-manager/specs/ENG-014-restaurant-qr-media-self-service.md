---
ticket: ENG-014
project: restaurant-portal
status: awaiting-scope
size: M
author: product-manager
created: 2026-08-29
decided:
---

# Brand portal self-service: restaurant QR codes and marketing media downloads

## Readback

**You said:** "on the brand portal restaurant is not able to see or genereate
the qr codes or the media downloads they have

nor are they able to make changes to timing or anythings related to their
website from the brand portal. all of this has be be done from admin portal
which the restaurant owners dont have access to. aware that these are
onboarding task but there can be no self onboarding if the restaurant
owner/user is not able to do this."

**Understood as:** Restaurant owners log into the brand portal
(`restaurant-portal` — confirmed the right repo: it ships its own
`brandPortalApi.ts` and calls the `brand-portal` Supabase function), which is
a different app and a different user role from the staff-only admin portal
(`aiorders-admin-hub`). Today two categories of onboarding tasks only exist
in admin: (1) generating/viewing a restaurant's QR codes and downloading its
printable marketing materials, and (2) editing the restaurant's website
settings, including hours. Because owners have no admin-portal login by
design (a different role, not a bug), staff has to do both on the owner's
behalf for every single restaurant — which is staff-assisted onboarding, not
self-onboarding.

**Evidence checked, not assumed.** Read both portals and the backend before
writing anything:
- `restaurant-portal/src/pages/website/Index.tsx` (brand portal) only edits
  two jsonb columns — `catering` and `careers` — via the `brand-portal`
  function's `website.ts` handler. Nothing about hours, location, or general
  site settings exists there. `restaurant-portal/src/pages/settings/Index.tsx`
  is a literal unimplemented stub: "Settings will be implemented here."
- `aiorders-admin-hub/src/pages/RestaurantAIWebsite.tsx` (staff-only, 3,298
  lines) is where "Opening Hours" / "Restaurant Hours" / "Pickup Hours" and
  the rest of the public-website configuration actually live today.
- `aiorders-admin-hub/src/pages/Activation.tsx` (staff-only onboarding
  checklist) has a "Step 7 — QR Codes" that generates a Dine-in QR and a
  Bag-Insert QR (`getRestaurantQR`, calling the `url-shortener` function),
  and a "Step 8" literally titled **"Share Bag Insert & QR with Owner"** —
  today's workaround, in the code, matching the report exactly: staff
  generates it, then manually hands it to the owner.
- The bag-insert flyer (`BagInsertGenerator.tsx`) and A4 poster
  (`A4PosterGenerator.tsx`, wired into `RestaurantDetails.tsx`) are the two
  live "media downloads" staff can already produce. No equivalent exists
  anywhere in `restaurant-portal`.
- `aiorders-api`'s `url-shortener` function — which creates the shortened
  link and calls the QR image API — is hard-gated to `profile.role ===
  'admin'` exactly (`verifyAdminAccess`), stricter than the brand-portal
  function's own admin check. This is a real backend authorization gap to
  close, not only a missing frontend screen.
- QR images come from `api.qrserver.com`, a free public API — no vendor
  contract, no published cost.
- Owners' inaccessibility to admin is by design: brand-portal users hold
  `brand_manager` / `restaurant_manager` roles (`brand_managers` /
  `restaurant_managers` tables); admin roles are a separate set
  (`admin`/`sub-admin`/`partner-admin`/`partner-user`). The fix is building
  the missing self-service surface, never widening owner access to admin.

**Second reading (blind architect, no repo access) agreed on direction —
independently arrived at the same two-portal, same-audience-split picture,
the same read that QR/media already exist and this is an access/surfacing
gap, and the same read of "timing" as operating hours. It flagged one thing
on its own, which checking the code confirmed as real and did not resolve:
"anythings related to their website" has no natural bound from the text
alone, and some admin-editable fields (pricing, payouts, domain/DNS) must
stay staff-only regardless of how this is scoped. Both readings independently
called this open rather than guessing at a boundary — a joint gap, not a
disagreement, so it is not a blocking question for this ticket. It is the
open edge of item 2 below, to be scoped when item 2 is actually shaped.**

## Feature shape and sequencing

The raw request is one message describing two separable capability gaps.
**Only item 1 is this ticket:**

1. **This ticket (ENG-014)** — restaurant self-service for QR codes and
   marketing media downloads. Reuses the existing QR/media generation logic
   and designs; the new work is a restaurant-scoped access path plus a brand
   portal UI for it. Independently useful today, and it's the half of the
   request with a clean, evidence-confirmed boundary (the two existing
   generators, restricted to the caller's own restaurant).
2. **Brand portal website settings, including hours ("timing")** —
   `[proposed]`, not yet filed, not yet sized. To be filed once this ticket
   verifies, per the same incremental-sequence mechanism `ENG-006`/`ENG-007`/
   `ENG-008` established (`skills/acceptance-check/SKILL.md` step 6b): this
   is the other half of the same request already made, not new
   agent-invented scope. Its own scoping question — how far "anythings
   related to their website" should extend beyond hours, and which
   admin-only fields stay staff-only — gets asked when item 2 is actually
   shaped, not now, since it doesn't gate this ticket's work.

**Recommendation: build ENG-014 now.** It's independently shippable, it's
the more concretely bounded half of the request (two named, already-live
generators, not an open-ended settings surface), and it directly targets the
exact sentence the requester closed on: self-onboarding is blocked while
these are staff-only.

## Problem

Restaurant owners onboarding onto the brand portal cannot see, generate, or
download their own QR codes or marketing materials (bag insert, A4 poster) —
confirmed in code as entirely admin-only, both the UI and the backend
authorization. Every restaurant's onboarding depends on a staff member
completing this step and manually handing the result to the owner
(`Activation.tsx`'s own "Share Bag Insert & QR with Owner" step names this
exactly). That does not scale past however many restaurants staff can walk
through by hand, and it means the brand portal cannot deliver true
self-onboarding for this piece regardless of how good the rest of it is.

## Why now

Raised directly by the approver, framed against a concrete operational
consequence: self-onboarding does not work while this piece requires staff.
Not manufactured urgency — the gap is confirmed in code, not just reported.

## Users

Restaurant owners and brand managers using the brand portal
(`restaurant_manager` / `brand_manager` roles) — both during initial
onboarding and afterward, any time they need to reprint a poster or recover
a QR code.

## Proposed change

A restaurant/brand-manager user on the brand portal can, for each restaurant
they manage: see their existing dine-in and bag-insert QR codes, generate
one if it doesn't exist yet, and download the same bag-insert and A4-poster
marketing materials staff can already generate for that restaurant — all
without an admin-portal login. Behavior only; how it's built is the
architect's call.

## Acceptance criteria

1. `[stated]` Given a restaurant/brand-manager user logged into the brand
   portal, when they open their restaurant's QR/media section, then they can
   view and download the existing dine-in QR code and bag-insert QR code for
   that restaurant.
2. `[stated]` Given the same user, when no QR code exists yet for their
   restaurant, then they can generate one themselves from the brand portal,
   with no staff action required.
3. `[inferred]` Given the same user, when they request their restaurant's
   bag-insert flyer or A4 poster, then they can download a print-ready file
   themselves, matching what staff can already produce for that restaurant
   today.
4. `[inferred]` Given a brand/restaurant-manager user attempting to view or
   generate a QR code or media asset for a restaurant they do not manage,
   then the request is denied — the negative case, using the same
   restaurant-scoping already enforced elsewhere in the `brand-portal`
   function.
5. `[proposed]` Given a restaurant owner completes self-service QR/media
   generation for their restaurant, then their onboarding checklist reflects
   that this step is done without a staff member having to mark it
   complete on their behalf. Flagged proposed, not stated: it's the literal
   fulfillment of "self onboarding" from the request's own closing sentence,
   but the mechanism is a design decision — the approver may decide it's a
   fast-follow instead.

## Non-goals

- Item 2 above (website settings, hours/"timing") — separately sequenced,
  not this ticket.
- Any new QR type beyond what `Activation.tsx` already produces (dine-in,
  bag-insert). No general-purpose/arbitrary-link QR generator for owners.
- Any change to the admin hub's own QR/media tooling or to the Activation
  checklist's staff-facing UI.
- Widening `url-shortener`'s admin gate for any action beyond what this
  ticket needs (fetching/creating a QR scoped to the caller's own
  restaurant). Its `list`/`update`/`delete`/analytics actions stay
  admin-only.
- Brand-wide or multi-restaurant bulk generation — one restaurant at a time,
  matching how the rest of the brand portal already scopes to
  `currentRestaurant`.
- New marketing-collateral designs or templates — reuses the existing
  bag-insert and A4-poster designs as-is.
- Granting restaurant owners any admin-portal access or admin role. The fix
  is a self-service surface in the brand portal, never opening up admin.

## Risks and unknowns

- **Real backend authorization work, not just a new screen.** `url-shortener`
  checks `profile.role === 'admin'` with nothing else recognized. The
  architect needs a restaurant-scoped path (the `brand-portal` function's own
  `verifyRestaurantAccess` — `brand_manager` / `restaurant_manager` — is
  already the right pattern, used elsewhere in that same function) rather
  than loosening the existing admin check, which would let any authenticated
  admin-adjacent caller reach every restaurant's shortened links.
- **Third-party dependency**, unchanged by this ticket but now user-facing:
  QR images come from `api.qrserver.com`, a free public API with no stated
  SLA. Staff already carries this risk today; this ticket exposes it to
  owners too.
- **Assumption worth correcting if wrong:** "media downloads" is read as the
  two existing generators (bag insert, A4 poster). If the requester actually
  meant something broader — raw menu photos, logo files — that's not covered
  here.
- Whether AC5 (checklist auto-completion) belongs in this ticket or a
  fast-follow is genuinely open — see AC5's own note.

## Cost

- Build: `M` — spans two repos (`restaurant-portal` for the brand-portal UI,
  `aiorders-api` for the new restaurant-scoped backend path), each
  individually bounded since both reuse existing generation logic and
  designs rather than building new ones. Rough estimate: a day and a half to
  two days.
- Run: $0/month — no new vendor. Reuses the existing free QR provider and
  existing Supabase functions.

## Decision

Filled in after G1.

- **The approver's answer:**
- **Date:**
- **Notes:**
