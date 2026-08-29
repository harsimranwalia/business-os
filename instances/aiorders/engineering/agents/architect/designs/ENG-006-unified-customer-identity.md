---
ticket: ENG-006
project: aiorders-api
author: architect
created: 2026-08-28
adrs: []
one_way_doors: ["phone/OTP platform identity, once diners adopt it, is expensive to unwind — escalated to G2 rather than decided here"]
touches_data: true
touches_models: true
---

# Unified cross-restaurant customer identity, phone/OTP auth, and legacy-customer mapping — technical design

## Approach

Investigated fresh against the department worktree (`~/Documents/projects/_eng/aiorders-api`,
`git fetch origin` first; clean tree, no prior work in progress). This repo
has **no schema in version control at all** — no `supabase/migrations/`, no
generated types file, no `deno.json`. The only way to learn the live shape of
`customers` was to read the edge functions that query it
(`crm/customers.ts`, `crm/utils.ts`, `website-submissions/customer-signup.ts`,
`get-customers/index.ts`, `brand-portal/customers.ts`) rather than trusting
the PRD's inferences about it secondhand.

**What the legacy `customers` table actually looks like**, confirmed from
code rather than assumed: `id`, `restaurant_id`, `brand_id`, `cw_id`
(external CloudWaitress id), `phone`, `email`, `name`, `meta` (jsonb),
`stats` (jsonb), `consent_sms` / `consent_email` (jsonb: consent, consent_at,
channel, source, method), `first_touch_at/source/medium/campaign`,
`first_referrer`, `last_touch_at/source`. Matching today is already
phone-first (`crm/customers.ts`'s `findOrCreateCustomer`: try `cw_id`, then
`phone`, then `email`, scoped to `restaurant_id` **or** `brand_id`), using an
existing `normalizePhone()` helper (`crm/utils.ts`).

**Correction to one of the PRD's assumptions, found rather than guessed:**
"Restaurant means one location, not a multi-location brand" is not what the
live schema says. `customers` is already scoped by `restaurant_id` **or**
`brand_id` as alternatives, and `proxy-login/index.ts` confirms a real
`brands` / `brand_managers` table structure sitting above individual
restaurants. So a legacy customer record can already be brand-scoped, not
just restaurant-scoped. This design's mapping table carries both columns
rather than assuming every legacy row is restaurant-scoped — see Data below.

**Auth mechanism: Supabase's native phone/OTP auth, not a hand-rolled OTP
table.** `proxy-login/index.ts` shows this codebase already knows how to
hand-sign a Supabase-compatible JWT for a non-standard login (admin
impersonation), so a custom OTP+JWT path is technically possible here — but
it exists there for a reason that doesn't apply to this ticket (impersonating
an *existing* authenticated admin, not verifying a new phone). For genuine
phone/OTP signup and login, Supabase Auth's built-in phone provider
(`auth.signInWithOtp({ phone })` / `verifyOtp`) already does exactly what
this ticket asks: send a code, verify it, create or reuse the
`auth.users` row keyed on `phone`, issue a real session with refresh. Using
it means this ticket adds no custom OTP generation, hashing, storage, or
expiry logic, and no hand-rolled JWT signing — all of that is exactly the
kind of security-sensitive code worth not writing twice. `proxy-login`'s
approach is precedent that the *team* can do this by hand, not a reason this
*ticket* should.

**Naming:** the PRD's "platform customer" placeholder is adopted as the real
name (`platform_customers`) — neutral, descriptive, not a brand word, per the
approver's own instruction, and already the term used throughout the PRD and
this ticket's Non-goals, so introducing a different real name at this point
would only cost a rename with no benefit.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `supabase` project config (Auth settings) | Enable phone provider; configure SMS provider (vendor TBD — see Risks); set OTP expiry and per-phone send-rate limits | backend / devops |
| New table `platform_customers` | New | backend |
| New table `platform_customer_legacy_links` | New | backend |
| New edge function `platform-customer-auth` | New — post-verification linking, called by the client immediately after `verifyOtp` succeeds | backend |
| `customers` (legacy table) | **None.** Read-only from this ticket's perspective. | — |
| `crm/utils.ts`'s `normalizePhone()` | **Not reused as-is for this flow** — see Risks; a stricter validator is needed ahead of it | backend |

## Data

### `platform_customers`

| Column | Type | Notes |
|---|---|---|
| `id` | `uuid primary key references auth.users(id)` | 1:1 with the Supabase Auth user created by phone sign-in |
| `phone` | `text not null unique` | Canonical E.164, mirrored from `auth.users.phone` at creation — `auth.users` isn't directly queryable under RLS from app code, same reason this codebase already keeps a separate `profiles` table alongside it |
| `display_name` | `text null` | Not collected by this ticket; column exists so a later ticket doesn't need a migration to add it |
| `consent_recorded_at` | `timestamptz null` | See Risks — cross-restaurant consent, not inherited from legacy `consent_sms`/`consent_email` |
| `created_at` | `timestamptz not null default now()` | |
| `updated_at` | `timestamptz not null default now()` | |

### `platform_customer_legacy_links`

| Column | Type | Notes |
|---|---|---|
| `id` | `uuid primary key default gen_random_uuid()` | |
| `platform_customer_id` | `uuid not null references platform_customers(id)` | |
| `legacy_customer_id` | `uuid not null references customers(id)` | **unique** — a legacy record links to at most one platform customer, closing the double-link race |
| `restaurant_id` | `uuid null` | Denormalized copy from the legacy row at link time, not authoritative |
| `brand_id` | `uuid null` | Same — legacy rows can be scoped either way (see Approach) |
| `matched_via` | `text not null check (matched_via in ('phone_auto','manual'))` | |
| `needs_review` | `boolean not null default false` | See below |
| `review_reason` | `text null` | e.g. `"name mismatch"`, `"duplicate phone within one restaurant"` |
| `linked_at` | `timestamptz not null default now()` | |

Indexes: `platform_customer_id` (AC4's "read back together with linked
restaurants"), `restaurant_id`, `brand_id`.

**What "ambiguous" means here, precisely** (PRD requirement 9 / AC-adjacent,
not literally an acceptance criterion but load-bearing for this table's
design): spanning multiple *different* restaurants on one phone is the
**normal, expected case** — that's the entire point of the feature — and
auto-links freely. `needs_review` is reserved for actual data-quality
conflicts: two-plus legacy rows at the **same** restaurant/brand sharing one
phone (which one is canonical?), or a legacy row's stored `name` diverging
meaningfully from names already linked to the same platform customer. Both
get linked (not silently dropped — AC8's spirit is "reject the OTP request
itself when input is bad, not the linking of good input"), just flagged for
a human to look at later (ticket 5's admin surface, see the frontend
knowledge-capture doc).

## Interfaces

**`POST platform-customer-auth/verify`** — called by the client with its
freshly-issued Supabase session (`Authorization: Bearer <token>`) immediately
after `verifyOtp` succeeds client-side. Runs with the caller's own JWT
(`supabase.auth.getUser(token)`, the same pattern `proxy-login` already uses
to identify a caller):
1. Upserts `platform_customers` (id = `auth.uid()`, phone from the verified
   session) — no-op on a returning login, matching AC2.
2. Looks up `customers` by normalized phone across every `restaurant_id` /
   `brand_id`, links whatever matches per the rules above.
3. Returns the platform customer plus its current links.

No separate "read my links" endpoint — `platform_customer_legacy_links` is
directly readable by its own owner under RLS (below), so a client can query
it with the Supabase SDK the same way it already queries anything else RLS
lets it see. One less thing to build.

**RLS:**
- `platform_customers`: owner (`auth.uid() = id`) may `select`/`update` their
  own row. No client `insert`/`delete` — only the service-role edge function
  creates rows.
- `platform_customer_legacy_links`: owner (`platform_customer_id = auth.uid()`)
  may `select`. No client `insert`/`update`/`delete` — service-role only.
- `customers` (legacy): **unchanged**. Not touched, not newly exposed.

## Alternatives considered

- **Hand-rolled OTP table + custom JWT signing, following `proxy-login`'s
  pattern.** Rejected: strictly more security-sensitive code (OTP hashing,
  expiry, rate-limiting, JWT signing) than the native path, for the same
  outcome. `proxy-login` does this because it has no real phone to verify
  (it's impersonation); this ticket does.
- **Reuse `profiles` for platform customers instead of a new table.**
  Rejected: `profiles` is built around staff/admin/brand roles and RLS
  written for that population. Mixing in a diner population with a
  completely different access model is a real risk for no benefit over a
  dedicated table.
- **Skip the denormalized `restaurant_id`/`brand_id` on the link table,
  join through `customers` instead.** Rejected: cheap columns, and every
  read this feature does (a platform customer's restaurants) wants them
  directly without an extra join or trusting the legacy row not to change
  scope later.

## One-way doors

**One identified, escalated rather than decided here.** A phone/OTP
platform-level identity, once real diners have verified a number and started
linking their order history to it, is expensive to walk back — not because
the *schema* is hard to reverse (it isn't: `platform_customers` and
`platform_customer_legacy_links` are both purely additive, and dropping them
touches nothing in `customers`), but because diners would have real sessions
and real expectations built on it. Unwinding after adoption means a
user-facing regression, not just a migration.

This ticket's own PRD flagged this twice for exactly this evaluation
("flagged for the architect to evaluate for G2 — not decided here," in both
Risks and the ticket's own Notes) rather than asking the architect to settle
it quietly. Given that, and given this is the department's largest
new-subsystem decision to date with no prior G2 precedent to lean on, this
design escalates rather than deciding unilaterally — see the raised gate
item for the actual question put to the approver.

**Explicitly not re-litigating:** the PRD's separate "marketplace owns the
identity vs. restaurant owns their customer" positioning tension. That was
already surfaced in the PRD's own Risks and classified there as "a
positioning fact worth having on the record... not a build question, so it
isn't a fork to ask about" — the G1 approval already passed that classification
without pushback. This escalation is about adoption-reversibility only, not
reopening a question the PRD itself already resolved as non-gating.

## Risks

- **SMS OTP delivery is not wired to any real vendor yet, despite the cost
  question being resolved.** The approver's G1 note says the vendor
  relationship (unlimited SMS, fixed monthly cost) is already in place, but
  nothing in this repo currently sends real SMS — `outgoing-communications/services/sms.ts`
  has only a `MockSMSService` behind a `SMS_PROVIDER` env switch, with
  Twilio/MessageBird/Vonage all stubbed as `// TODO`. **That module is not
  what would power this feature anyway** — Supabase Auth's own phone
  provider needs its SMS vendor configured at the Supabase project level
  (dashboard or `supabase/config.toml`'s `[auth.sms]`), entirely separate
  from this repo's marketing-SMS scaffold. Flagging explicitly so a future
  build doesn't wire OTP through the wrong (mocked) path by following the
  nearest-looking existing code. Which vendor, concretely, and its Supabase
  provider config remain open integration work for build time.
- **`normalizePhone()` never actually rejects anything except empty input**
  (confirmed reading `crm/utils.ts`) — unrecognized lengths fall through to
  a best-effort `+1` prefix rather than failing. Reusing it as-is would make
  AC7 ("a phone that can't be normalized is rejected with a clear reason")
  effectively unreachable. This design calls for a **separate, stricter
  validator** ahead of the OTP call (E.164 shape + plausible length check)
  rather than tightening the existing lenient one — marketing-capture phone
  data has different tolerance needs than a security-relevant auth key, and
  changing shared behavior for this ticket risks regressing the marketing
  capture path for no reason.
- **Phone number recycling** (carried from the PRD, not resolved here): a
  reassigned number could auto-link to a stranger's legacy history. A
  proportionate mitigation — flag `needs_review` rather than auto-link when
  the matched legacy row has been dormant past some threshold (a specific
  number is a product judgment call, not fixed here) — is offered as a
  build-time refinement, not a requirement this ticket must satisfy before
  shipping.
- **Consent**: `consent_recorded_at` on `platform_customers` is proposed as
  its own cross-restaurant consent capture, deliberately not inherited from
  legacy `consent_sms`/`consent_email` (captured for a different,
  per-restaurant marketing purpose, by a different flow). The actual consent
  copy/legal language is outside this department's lane and needs the
  approver or counsel, not assumed here.
- **No schema in version control for this repo at all.** Not introduced by
  this ticket, but worth naming: this design's migration, once written, will
  be the first tracked schema artifact this repo has ever had. No blocker,
  just a first.

## Rollout

Additive migration only — two new tables, zero `ALTER` on `customers` or any
other existing table. No live caller exists yet (this ticket is backend-only;
the earliest frontend consumer is a later, unscheduled discussion per the
approver), so there is no traffic to cut over and no feature flag needed —
the tables and function simply don't get called until something calls them.
$0 infrastructure delta beyond the already-resolved SMS vendor cost — same
Supabase project, no new service.

## Out of scope

Per the PRD's own non-goals: points, balances, the ledger, redemption, QR
codes, per-restaurant config, admin endpoints, and all frontend work in every
repo. This design also does not specify the SMS vendor, the exact phone-
dormancy threshold for the recycling mitigation, or consent copy — all
named above as open, not silently assumed.
