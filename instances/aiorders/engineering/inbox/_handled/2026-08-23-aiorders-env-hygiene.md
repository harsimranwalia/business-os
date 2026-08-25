---
source: approver
filed_by: Harry
via: manual
received: 2026-08-23
---

# `.env` is tracked in config-site-builder and unignored in aiorders-admin-hub

Found while committing the AIOrders working trees on 2026-08-23. Neither repo's
`.gitignore` mentions `env` at all.

**`config-site-builder/.env` is tracked in git.** It holds `VITE_SUPABASE_URL`,
`VITE_SUPABASE_ANON_KEY` and `VITE_GOOGLE_MAPS_API_KEY` with live values, and
they are in the repo's history, not just its tip. The uncommitted change to it
was left uncommitted: it repoints `VITE_BRAND_ID` at a different brand, which
reads as one developer's local target rather than a new default for everyone.

**`aiorders-admin-hub/.env` is untracked but not ignored**, so it shows up as an
untracked file on every status and is one `git add -A` away from being committed.
It was left alone in this pass for that reason.

## Scale before anyone panics

The Vite variables are public by design — they ship inside the client bundle, so
a browser devtools tab reveals the same values. The Supabase anon key is meant to
be public and is only as strong as the RLS behind it, which is its own question
(see the migration-history request filed the same day — five of the six missing
migrations are RLS hardening).

The Google Maps key is the one worth an actual look: it is billable, and if it
carries no HTTP-referrer restriction in Google Cloud it can be lifted from the
bundle and spent by anyone.

## What this asks for

Three things, in rough priority:

1. Check whether the Google Maps key is referrer-restricted. If not, restrict it.
   This is the only item with a cost attached.
2. Get `.env` out of tracking in `config-site-builder` and add `.env` to both
   repos' `.gitignore`, with a committed `.env.example` naming the variables so
   the untracking does not just make onboarding harder.
3. Decide whether rotation is warranted. Probably not for the anon key, possibly
   for the Maps key depending on what step 1 turns up.

Also minor, same family: `restaurant-marketplace/.claude/projects/` is untracked
Claude session data with no `.gitignore` entry — worth one line in the same pass.
