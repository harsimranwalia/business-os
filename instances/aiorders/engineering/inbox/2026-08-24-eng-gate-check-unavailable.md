---
type: eng-decision
agent: eng-manager
gate: incident
project: life-os
ticket: ENG-001
recommendation: investigate before the next release
raised: 2026-08-24
decision: approved
decided: 2026-08-24T17:00:57.276371+00:00
---

# The receipt check could not run

`lib/eng-gate-check.sh` is absent or unreadable, so passes are running with the receipt invariant unenforced. The loop deliberately continues rather than halting — but until this is restored, `shipped` is only as true as the pass that wrote it.

Raised by the receipt check wired into `lib/eng-trigger.sh` (ENG-008). The
check reads the filesystem, never the frontmatter — a ticket cannot satisfy it
by writing `test_plan: done`.

## Decision

**approved** — 2026-08-24T17:00:57.276371+00:00

Root cause fixed in business-os 9366b84 — nine $ROOT/lib/ call sites repointed to $ENG_DEPT/lib/ after the carve-out, plus ENG_ROOT pinned to the instance so the check reads the real board. Verified: exits 0 clean on this board.
