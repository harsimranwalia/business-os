---
ticket: ENG-007
project: aiorders-api
author: architect
created: 2026-08-29
adrs: []
one_way_doors: ["a live, undocumented third-party loyalty vendor (Walletly) already runs in this codebase; committing to the native loyalty sequence without reconciling against it is expensive to unwind once tickets 3-5 build a competing ledger — escalated to G2 rather than decided here"]
touches_data: true
touches_models: false
---

# Per-restaurant loyalty configuration — earn rates and redemption value — technical design

## Approach

Investigated fresh against the department worktree, `_eng/aiorders-api` —
**this worktree did not exist on this host** (the instance's first pass run
on Windows against a real project repo; `agents/eng-manager/config/projects.md`'s
"all five worktrees already exist" was true only for the earlier Mac
verification). Created it this pass with the same commands
`lib/eng-setup.sh` itself runs (`git worktree add -b eng/base`, from the
human's clean `main` checkout, never touching that checkout) rather than
running the full setup script, since only this one project was needed and
the script also touches scheduler wiring outside this ticket's scope. Noted
in `observations.md`.

**Correction to `ENG-006`'s design doc, found rather than assumed:** its
Approach section states this repo has "no schema in version control at
all." That was true when it was written, but is no longer — commit
`5b3bac2` ("Consolidate remaining migrations from aiorders-admin-hub"), one
commit before `ENG-006`'s own `c3ab50c`, landed a `supabase/migrations/`
directory with 20 pre-existing files moved in from other repos. This design
was read directly from those real migration files rather than reverse-engineered
from edge-function code, which `ENG-006` had to do.

**Confirmed conventions from the real migrations**, not inferred:
`restaurants.id` is `uuid` (RLS policy `USING (auth.uid() = id)` in
`20250729143357_initial_restaurant_rls.sql` — restaurant owners authenticate
as their own restaurant row). A shared trigger function,
`public.update_updated_at_column()`, already exists
(`20250729143432_updated_at_functions.sql`) and is the established way to
maintain `updated_at` — reused here rather than writing a duplicate.
`restaurant_activations` (`20260312000001_restaurant_activations.sql`) is
the closest existing precedent for a small per-restaurant config table:
service-role-only RLS, a trigger-maintained `updated_at`, one index on
`restaurant_id`. This design follows the same shape.

**Requirement 9's "minimal internal write path" already has a home.**
`supabase/functions/admin-portal/index.ts` is a single function with an
existing role-gated auth middleware (`profiles.role`/`additional_roles` in
`('admin','sub-admin', ...)`) and a path-based router to per-concern handler
modules (`handlers/restaurants.ts`, `handlers/brands.ts`, etc.). Adding
`handlers/loyalty-config.ts`, routed at `/admin-portal/loyalty-config`,
reuses this exactly rather than standing up new auth machinery for one
ticket with no frontend — the same reasoning `ENG-006` used to prefer
Supabase's native OTP over hand-rolling one.

**A significant unplanned finding: a live third-party loyalty vendor is
already integrated.** `supabase/functions/external-integrations/handlers/walletly.ts`
is a real, documented, actively-maintained integration (catalogued in
`supabase/functions/README.md`'s function table; last touched 2026-07-07 in
a repo-wide "reconcile duplicate edge functions" cleanup, seven weeks before
this sequence was requested — not dead code) that proxies to
`api.walletly.ai` for a customer's current loyalty points and a brand's
reward catalog, keyed by `brandId` + email. Neither the approver's original
request (`ENG-006`'s `## Input`) nor `knowledge/business-profile.md`
mentions Walletly at all. See One-way doors below — this is escalated, not
decided in this design.

## Components

| Component | Change | Owner agent |
|---|---|---|
| New table `restaurant_loyalty_configs` | New | backend |
| New trigger `enforce_loyalty_config_effective_order` | New — race-safe ordering guard, see Data | backend |
| `admin-portal/handlers/loyalty-config.ts` | New handler module | backend |
| `admin-portal/index.ts` | +1 route (`/admin-portal/loyalty-config`), same pattern as every existing entry | backend |
| `admin-portal/README.md` catalog entry | Update, per this repo's own `CLAUDE.md` instruction (`ENG-006` precedent) | backend |
| `customers`, `platform_customers`, any existing table | **None.** Purely additive. | — |

## Data

### `restaurant_loyalty_configs`

| Column | Type | Notes |
|---|---|---|
| `id` | `uuid primary key default gen_random_uuid()` | |
| `restaurant_id` | `uuid not null references public.restaurants(id) on delete cascade` | No `brand_id` — PRD carries forward `ENG-006`'s single-location assumption; a brand wanting one shared rate across locations configures each restaurant separately today, not solved here |
| `online_earn_pct` | `numeric(5,2) not null check (online_earn_pct >= 0 and online_earn_pct <= 100)` | Percentage; basis (subtotal vs. total) is a ticket-3 question — this ticket only stores the number, ticket 3 (the earn API) is what actually computes against an order |
| `dine_in_earn_pct` | `numeric(5,2) not null check (dine_in_earn_pct >= 0 and dine_in_earn_pct <= 100)` | Same |
| `redemption_value_per_point` | `numeric(10,4) not null check (redemption_value_per_point >= 0)` | Currency credited per point redeemed — PRD requirement 2 ("what a point is worth on redemption") read as a conversion rate, symmetric with the two earn rates, rather than a flat one-time credit |
| `effective_from` | `timestamptz not null default now()` | Open-ended validity — no `effective_to` column, see Alternatives |
| `created_at` | `timestamptz not null default now()` | |
| `created_by` | `uuid references auth.users(id)` | The admin who set this rate — audit trail, same rationale as `api_keys.created_by` |
| `updated_at` | `timestamptz not null default now()` | Maintained by the existing `update_updated_at_column()` trigger. Rows are logically insert-only (a rate change is a new row, never an edit to an old one — PRD requirement 6) but the column exists for schema consistency with every other table in this repo and to timestamp the rare correction of a same-row typo before it takes effect |

Index: `restaurant_loyalty_configs_restaurant_id_effective_from_idx` on
`(restaurant_id, effective_from desc)` — the only query pattern this ticket
or ticket 3/4 will ever run is "latest row for restaurant X with
`effective_from <= T`."

**The "effective as of T" read**, resolving PRD requirement 8 / AC3, is one
query, no helper function needed:

```sql
select * from restaurant_loyalty_configs
where restaurant_id = $1 and effective_from <= $2
order by effective_from desc
limit 1;
```

No rows → AC4's "not enrolled," returned as such by the handler rather than
a default or an error.

**Ordering is enforced at the database, not just the application** (closes
PRD Risk "concurrent writes... needs an explicit design answer"). Two
decisions, both load-bearing for AC2/AC3/AC6:

1. **Future-only.** A new row's `effective_from` must be `>= now()` at
   insert time — never backdated. This is what makes AC3 ("the rate
   actually in effect at a past timestamp is returned, never the current
   one") true by construction: if every row was current-or-future when
   written, no later insert can ever change what a query for a past
   timestamp resolves to.
2. **Strictly increasing per restaurant.** A new row's `effective_from`
   must be later than every existing row's for that same restaurant — this
   is AC6 ("overlapping/conflicting ranges rejected") without needing
   interval/exclusion-constraint machinery, because validity is a single
   point (open until superseded) rather than a closed range with two ends
   to reconcile.

Enforced by a `before insert` trigger using a per-restaurant advisory lock,
so two near-simultaneous writes for the same restaurant serialize instead of
racing (different restaurants proceed independently — no table-wide lock):

```sql
create or replace function public.enforce_loyalty_config_effective_order()
returns trigger
language plpgsql
security definer
set search_path = 'public'
as $$
declare
  current_max timestamptz;
begin
  perform pg_advisory_xact_lock(hashtextextended(new.restaurant_id::text, 0));

  select max(effective_from) into current_max
  from public.restaurant_loyalty_configs
  where restaurant_id = new.restaurant_id;

  if current_max is not null and new.effective_from <= current_max then
    raise exception
      'effective_from (%) must be later than this restaurant''s current latest (%)',
      new.effective_from, current_max;
  end if;

  if new.effective_from < now() then
    raise exception 'effective_from cannot be in the past (got %, now is %)',
      new.effective_from, now();
  end if;

  return new;
end;
$$;

create trigger restaurant_loyalty_configs_enforce_order
  before insert on public.restaurant_loyalty_configs
  for each row execute function public.enforce_loyalty_config_effective_order();
```

The advisory lock is keyed by `hashtextextended(restaurant_id::text, 0)`,
scoped to the transaction (`pg_advisory_xact_lock`, auto-released on
commit/rollback) — no cleanup path needed, no lock table to leak.

## Interfaces

**`POST admin-portal/loyalty-config`** — admin/sub-admin only (existing
`admin-portal` auth middleware, unchanged). Body: `restaurant_id`,
`online_earn_pct`, `dine_in_earn_pct`, `redemption_value_per_point`,
optional `effective_from` (defaults to `now()` if omitted — the common
case, "take effect immediately"). Inserts one row via the service-role
client; the trigger above is what actually rejects a bad `effective_from`,
so the handler's own validation only needs to check the three numeric
fields are present and non-negative before hitting the DB (a friendlier
400 instead of a raw constraint-violation 500 for that specific mistake).

**`GET admin-portal/loyalty-config?restaurant_id=X`** — same auth. Returns
the current effective row (the query above, `$2 = now()`) plus, since
there's no other way to see history yet with no frontend, the full
ordered history for that restaurant. Ticket 5 (admin/support surfaces) is
where a real UI for this eventually belongs; this is the minimal
unblock, not that surface.

**RLS: deny-by-default, service-role only — no client policy at all**,
same choice `ENG-006` made for its own two tables. No restaurant-owner or
diner access exists yet because no frontend exists yet (PRD non-goal for
the whole sequence); when the restaurant-portal ticket for this eventually
gets scoped, it adds a `select` policy scoped to
`user_has_restaurant_access(auth.uid(), restaurant_id)` (the same helper
`restaurants`' own RLS already uses) — not needed today, not built today.

```sql
alter table public.restaurant_loyalty_configs enable row level security;
-- no policies: RLS defaults to deny; only the service-role admin-portal
-- handler and its trigger touch this table.
```

## Alternatives considered

- **Closed date ranges (`effective_from` + `effective_to`) instead of
  open-ended validity.** Rejected: every insert would also need to
  `UPDATE` the previous row's `effective_to`, which breaks the
  insert-only/append-only property PRD requirement 6 explicitly asks for
  ("a rate change creates a new record, never edits the old one") and
  reopens exactly the kind of two-writers-racing problem the trigger above
  exists to close, now on two statements instead of one.
- **App-level-only validation (no DB trigger).** Rejected: the PRD names
  concurrent writes as an explicit open risk; two near-simultaneous
  requests both reading "current max" before either commits is a real race
  an app-level check alone does not close. The advisory lock costs nothing
  extra to write and closes it for real.
- **A dedicated new edge function (`loyalty-config`) instead of an
  `admin-portal` handler.** Rejected here, unlike `ENG-006`'s choice to add
  a new function for its own concern — `ENG-006` needed new auth semantics
  (a diner's own session, not an admin's); this ticket needs exactly the
  admin/sub-admin gate `admin-portal` already has. A new function would
  duplicate that auth middleware for no benefit.

## One-way doors

**One identified this pass, not present in the PRD or `ENG-006`'s own
design — escalated rather than decided.** The Walletly integration
described in Approach is real, live, and documented, and nothing in the
approver's original request or either PRD's Risks section accounts for it.

**What makes this a one-way-door-shaped question rather than a plain risk
note.** `ENG-007` itself is low-stakes either way — an additive,
service-role-only config table that nothing calls yet, trivially droppable
if the answer changes. The exposure is downstream: ticket 3 (the points
ledger) is where a **second, independent points-tracking system** would
start actually running in production alongside Walletly's. Once diners and
restaurants have real point balances in *both* systems, reconciling or
retiring either one is a user-facing/data-migration problem, not a clean
schema change — the same shape of adoption-reversibility `ENG-006`'s own G2
reasoned through, just one ticket further downstream from where the
irreversible step actually happens. Flagging now, before ticket 3 is even
filed, is strictly cheaper than flagging after it ships.

**Not blocking this ticket's own design work on this** — the schema above
is fully specified and ready to build the moment this is answered, same as
`ENG-006`'s G2 didn't require redoing its design.

**Deliberately not guessing an answer.** Three genuinely different
readings are all consistent with what's on disk: Walletly could be a
legacy integration mid-deprecation, a per-brand opt-in add-on that
coexists fine with a platform-native program, or the business's actual
current loyalty offering that this whole five-ticket sequence would
duplicate. Nothing in the repository resolves which, and guessing wrong in
either direction is worse than asking — see the raised gate item for the
actual question and a recommendation.

## Risks

- **Walletly** — see One-way doors; the load-bearing risk of this design.
- **Unit basis for `online_earn_pct`/`dine_in_earn_pct`** (what the
  percentage is taken of — order subtotal, pre- or post-tax) is
  deliberately left open here. It has no bearing on this ticket's schema
  (a `numeric` percentage either way) and is a real question only once
  ticket 3 computes points against an actual order — carried forward
  rather than answered speculatively now.
- **Single-location assumption carried forward from `ENG-006`.** A brand
  with multiple locations configures each restaurant's rate independently;
  no brand-level default or override exists. Matches the PRD's own
  explicit assumption, not reopened here.
- **`effective_from` granularity.** `timestamptz` in Postgres is
  microsecond-precision, so two writes for the same restaurant colliding on
  the exact same instant is not a realistic concern for an internal,
  human-initiated admin action (contrast `ENG-006`'s phone-recycling risk,
  which was about real user-triggered volume) — noted, not mitigated
  further.

## Rollout

Additive migration only — one new table, one new trigger function, zero
`ALTER` on any existing table. No live caller exists (`admin-portal`'s new
route is reachable only by an authenticated admin/sub-admin, and nothing in
any frontend calls it — same "invisible until wired in" shape as
`ENG-006`). $0 infrastructure delta — same Supabase project, no new
service, no interaction with Walletly's paid API either way.

## Out of scope

Per the PRD's own non-goals: the points ledger, earn/redeem history
(ticket 3); redemption execution or QR codes (ticket 4); admin/support UI
(ticket 5); any frontend in any repo; the real $/% numbers for any
restaurant; resolving the Walletly question (escalated, not this design's
call); the order-subtotal-vs-total basis for earn % (ticket 3's question).
