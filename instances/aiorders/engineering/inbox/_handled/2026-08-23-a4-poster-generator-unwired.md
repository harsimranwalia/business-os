---
source: approver
filed_by: Harry
via: manual
received: 2026-08-23
---

# A4PosterGenerator is committed but not reachable

`src/components/A4PosterGenerator.tsx` was committed to `aiorders-admin-hub` on
2026-08-23 (`bfddffe`) so the work would be tracked rather than sitting loose in
the working tree. Nothing imports it — a grep across `src/` finds no reference
outside the file itself. It is in the repo and unreachable from the running app.

## What this asks for

First decide whether it is wanted, then act on the answer. If it is, wire it into
a route or a surface in the admin hub and say which. If it is not, delete it —
`bfddffe` is a single-file commit specifically so reverting it is clean.

Small, and genuinely low stakes. Worth capturing only so a committed-but-dead
component does not quietly become permanent.
