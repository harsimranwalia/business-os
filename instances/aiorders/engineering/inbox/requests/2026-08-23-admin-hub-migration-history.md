---
source: approver
filed_by: Harry
via: manual
received: 2026-08-23
---

# Six aiorders-admin-hub migrations are deleted from the working tree and exist nowhere else

While committing the AIOrders working trees on 2026-08-23, six migration files
were found deleted from `aiorders-admin-hub`'s working tree but still present in
`HEAD`. The deletion was **not committed** — it is still sitting uncommitted in
the human checkout, deliberately held back pending this decision.

```
supabase/migrations/20250729143432-1040fac4-….sql   search_path hardening on two trigger functions
supabase/migrations/20250814063528_6a950847-….sql   removes public read on profiles, adds owner/admin RLS
supabase/migrations/20250814064923_3be8f472-….sql   fixes infinite recursion in the profiles admin policy
supabase/migrations/20250814065439_d1efe4c6-….sql   restricts public restaurants access, adds restaurants_public view
supabase/migrations/20250814065606_3be00703-….sql   recreates that view as SECURITY INVOKER
20260312000001_restaurant_activations.sql           creates the restaurant_activations table
```

A filesystem sweep across all nine repos under `projects/aiorders/` finds none of
these six filenames anywhere else. Unlike the edge functions removed in the same
pass, they were not consolidated into `aiorders-api` — that repo's migrations
directory holds nine files, all dated 2026-08 or later, and none of these.

## Why this is not a safe deletion to just commit

`20260408000001_google_review_history.sql` — committed on 2026-08-23 in the same
session — runs `ALTER TABLE restaurant_activations`. The only migration that
creates that table is `20260312000001_restaurant_activations.sql`, one of the
six. Committing the deletion breaks a from-scratch replay: the chain would alter
a table nothing creates.

Five of the six are also RLS and `search_path` hardening. Whatever the intent
behind removing them, dropping security migrations out of the tracked history is
not something to do by accident, and four sibling migrations from the same
minute (`20250729143357`, `20250814063455`, `20250814065341`) were kept — so
this was a selective prune, not a stray `rm`.

## What this asks for

Establish what the real migration history is and make the repo match it. The
underlying question the department should answer first: **is
`aiorders-admin-hub/supabase/migrations` still authoritative at all, or did
migrations move to `aiorders-api` the way the edge functions did and only get
half-moved?** Four migrations were added to admin-hub on 2026-08-23, which
suggests it is still live — but that is worth confirming against the actual
Supabase project rather than inferred from the tree.

Nothing here is urgent. The deployed database is unaffected either way; this is
about whether the tracked history can rebuild it.
