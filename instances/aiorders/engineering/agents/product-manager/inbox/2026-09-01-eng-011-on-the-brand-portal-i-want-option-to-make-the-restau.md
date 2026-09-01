---
source: approver
via: control-center
received: 2026-09-01T13:57:15.083927+00:00
---

# ENG-011 on the brand portal i want option to make the restaurant visible on order food, dine in and catering separately

Further enhancement to this section i want more filter to be able to be assigned to the restaurant .Act as Lead Architect on FoodSwipe (consumer discovery platform connected to AIOrders.io backend).

We are extending our current platform with (Multi-Channel Filters & Dynamic Promo Engine). Do not rebuild existing core ordering or video feed logic—extend our existing data structures and UI components.

Task: Generate code modifications for three specific enhancements:

1. Dynamic Operational Time-Clocks (Real-Time State Engine):
   - Extend existing venue objects with channel-specific cutoffs: `kitchen_cutoff_minutes`, `alcohol_license_time`, `happy_hour_schedule`.
   - Write a helper utility function `getVenueOperationalStatus(venueId, channelType)` that returns live status states for UI chips: "Kitchen closing soon", "Happy Hour Active", or "Alcohol Service Closed".

2. Smart Filter Engine (Dine-In & Catering Contexts):
   - Extend our current search/filter state bar to support channel-based context switching:
     * Dine-In: Filter by group capacity (`min_capacity`), AV amenities (`has_tv_screens`, `soundproof`), and private rooms (`has_private_space`).
     * Catering: Filter by lead time (`advance_notice_hours`), service types (`box_lunches`, `live_chef`), and minimum order spend (`min_catering_spend`).

3. Promo Badge Overlay for Video Feed & Venue Cards:
   - Inject a promotional metadata layer into existing store card components.
   - Render dynamic conversion badges (e.g., "BOGO Free", "$0 Delivery", "2x Loyalty Points") directly over video reels and venue listings based on active store campaigns.
Act as Senior Lead Developer working on our internal FoodSwipe / AIOrders.io staff management portal.

We already have an existing internal store edit form. We need to EXTEND our current codebase to append settings (Multi-Channel Filters, Amenities) without rewriting or breaking existing store management components.

Generate modular React/TypeScript extension components and state handlers to add the following field groups to our existing internal admin interface:

### 1. New Field Groups to Append:

Group A: Channel Operational Cutoffs & Throttling
- Order Food: Throttling Cap (Max orders/30-min window), Preparation Lead Time (mins).
- Dine-In: Kitchen Last Order Cutoff (mins before close), Alcohol License Cutoff (time picker), Happy Hour Window (start/end time schedule).
- Catering: Required Advance Notice (hours/days picker), Minimum Spend Threshold ($).

Group B: Venue & Service Amenities Tagging
- Dine-In Amenities: Ordering Mode (Pay at Table / Counter QR / View-Only), Private Space Seating Capacity (number), AV Specs Chips (TV/Screens, Soundproof, Custom Music, Decor Allowed).
- Catering Service Specs: Service Format Chips (Box Lunches, Platters, Live Chef, Food Truck), Fulfillment Options (Pickup, Delivery, Setup/Teardown).

Group C: Active Promotional Hooks(to be controlled from brand portal not admin portal)
- Dynamic Promo Toggles: BOGO Active, Welcome Offer (% off), Spend Threshold ($X off $Y), Free Item Trigger, Loyalty Multiplier.

### 2. Integration & Architectural Rules:
- Non-Destructive Extension: Export these new sections as isolated, reusable UI components (e.g., `<ChannelCutoffsSection />`, `<VenueAmenitiesSection />`, `<PromoHooksSection />`) so we can mount them directly into our existing layout.
- High-Density Compact Layout: Use inline form controls, compact chip-selectors for array tags, and minimal spacing so internal staff can scan and update fields rapidly.
- State & Schema Schema Mapping: Extend our existing `StoreFormValues` interface with an optional `eSettings` sub-object to maintain backward compatibility with existing API endpoints.
- Basic Guardrails: Add client-side validation for operational cutoffs (e.g., alert if Last Order Time exceeds business closing hours).
