# ADR index

**Next ID: ADR-021.** Numbered sequentially, never reused — same discipline as
`agents/eng-manager/board/_index.md`'s ticket counter.

| ID | Title | Ticket | Status | Date |
|---|---|---|---|---|
| ADR-001 | Verification tickets satisfy `building` and receipts without a diff | ENG-001 | accepted | 2026-08-25 |
| ADR-002 | Verification tickets still owe `ready-to-ship` and G3 — the gate stays, only its content changes | ENG-001 | accepted | 2026-08-26 |
| ADR-003 | `aiorders-api` is authoritative for AIOrders' Supabase migration history, not `aiorders-admin-hub` | ENG-004 | accepted | 2026-08-26 |
| ADR-004 | `ENG-004` is a verification ticket for its full remaining lane — second occurrence, different root cause than `ADR-001` | ENG-004 | accepted | 2026-08-26 |
| ADR-005 | `url-shortener` trusts a per-action restaurant-scoped check, not only platform-admin, for one new action | ENG-014 | accepted | 2026-08-31 |
| ADR-006 | admin-portal restaurants handler enforces brand scoping in code, not via RLS/client-branch | ENG-015 | accepted | 2026-08-31 |
| ADR-007 | Recurring feedback summary uses an all-time window and a >1 threshold for "recurring" | ENG-025 | accepted | 2026-08-31 |
| ADR-008 | Catering fulfillment stays on `delivery_method` — configurable copy, not new values | ENG-016 | accepted | 2026-09-03 |
| ADR-009 | The catering order form is an owner opt-in, default off, stored in `restaurant_website.catering` | ENG-016 | accepted | 2026-09-03 |
| ADR-010 | "Open Now" filtering runs post-query in the edge function, not as a SQL predicate | ENG-026 | accepted | 2026-09-03 |
| ADR-011 | The acquisition report is a `brand-portal` action, not an extension of the `analytics` function | ENG-020 | accepted | 2026-09-03 |
| ADR-012 | Acquisition channels are classified post-query in TypeScript; SQL only aggregates | ENG-020 | accepted | 2026-09-03 |
| ADR-013 | The chat-bar questions view reads `ai_conversations` directly under RLS; the FAQ write goes through `brand-portal` | ENG-021 | accepted | 2026-09-03 |
| ADR-014 | Customer chat-bar questions are shown to the owner verbatim — no redaction, no new copy, no export, never in a URL or a log line | ENG-021 | accepted | 2026-09-03 |
| ADR-015 | `autopilot`'s ownership check imports `_shared/restaurantAccess.ts`, not `brand-portal/utils.ts`'s | ENG-029 | accepted | 2026-09-03 |
| ADR-016 | `autopilot`'s `systemTriggered` marketing branch authenticates via the service-role key as a bearer credential, not a new secret or the existing publishable key | ENG-035 | accepted | 2026-09-03 |
| ADR-017 | `outgoing-communications`' `systemTriggered` gate reuses `ADR-016`'s service-role-bearer mechanism, as its own per-function file, not a shared one | ENG-036 | accepted | 2026-09-03 |
| ADR-018 | Broadcast scheduling and mass dispatch use a pg_cron poller claiming due rows, not per-recipient QStash messages | ENG-019 | accepted | 2026-09-03 |
| ADR-019 | Coupon-code ROI matches `orders.promos` against the campaign's code; no redemption-tracking table exists to reuse | ENG-019 | accepted | 2026-09-03 |
| ADR-020 | Broadcast opt-out reuses `customers.consent_email`/`consent_sms` via a new public unsubscribe function, not a new column or an `outgoing-communications` action | ENG-019 | accepted | 2026-09-03 |
