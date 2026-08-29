---
type: eng-decision
agent: eng-manager
gate: incident
project: aiorders
ticket: unknown
recommendation: investigate before re-enabling
raised: 2026-08-29
decision: approved
decided: 2026-08-29T21:28:04.845356+00:00
---

# Engineering loop halted — whole department

The loop hit its daily ceiling of 40 hops mid-drain. Queued events are still in `/c/Users/jerryai/Documents/GitHub/business-os/instances/aiorders/engineering/traces/.pending` and will resume tomorrow or on the next scheduled pass.

This is the DEPARTMENT's ceiling, not one ticket's — so the question is
whether the day's work was real or whether something was bouncing. Check
`traces/eng-loop-2026-08-29.log` for a ticket appearing over and
over. If the day was legitimately busy, the budget is the thing to raise
(`agents/eng-manager/config.yaml` → `plan`), not the counter to clear: a guard
that fires on normal days teaches everyone to ignore it.

Scheduled passes are unaffected, and every other ticket keeps moving.

---

**Investigated 2026-08-29**, `watch` event pass (context `schtasks`) — this
item carries no `## Decision` section and no `notified:` field, unlike
every other gate item raised today; read as a direct shell-written notice
(the runaway guard itself, not a Claude pass using the usual gate-item
template) rather than something the approver needs to answer, and the
pass that wrote it (`[2026-08-29 14:19:07] DAILY HOP LIMIT mid-drain (40)`,
`traces/eng-loop-2026-08-29.log`) most likely died at or near that exact
line, before it could reach a notify call — consistent with `eng-notify.sh`
never logging an attempt for this file in `traces/eng-notify-2026-08-29.log`.

**Checked what this notice asked to be checked, not assumed either way.**
`traces/eng-loop-2026-08-29.log`'s own drain lines
(grepped fresh, not eyeballed) show 41 hops spent today across 24 tickets
(`ENG-001`–`ENG-024`) and 9 fresh intake requests, each typically walking
several pipeline states — `watch (schtasks)` alone drained 7 separate
times. No single ticket dominates the count the way a bouncing retry loop
would (`continue (ENG-011)` and `continue (ENG-007)` are the most-repeated
at 3 each, and both are accounted for by real, separate causes: `ENG-011`
legitimately walked `ready → building → in-review → in-security →
ready-to-ship` in 4 transitions per pass, and `ENG-007`'s repeats are the
weekend release-window holding a `ready-to-ship` ticket that keeps getting
correctly re-checked and correctly re-held, not a broken retry). Read
together: this was a legitimately busy day, not a bug bouncing a ticket, per
this notice's own test for telling the two apart.

**Root cause found for the ceiling firing at 40 despite today's actual
tier.** `departments/engineering/agents/eng-manager/config.yaml` sets
`plan.tier: max_5x` (`hops_per_day: 200`) as of today, but
`departments/engineering/lib/eng-trigger.sh`'s `read_plan_budget()` was
reading `$ROOT/agents/eng-manager/config.yaml` — a path that does not exist
on any instance (`plan.tier` lives only in the department template) — so it
silently hit its hardcoded fallback (`40`, the `pro`-tier number) on every
call, regardless of the tier actually configured. Both already fixed,
uncommitted on disk before this pass started (found already in place, not
made by this pass — see `agents/eng-manager/observations.md`'s `continue
ENG-013` row, same day): `read_plan_budget()`'s config path corrected to
`$ENG_DEPT/agents/eng-manager/config.yaml`, and this instance's own
`config/config.yaml` → `wip.machine_limit: 6 → 12` to match the `max_5x`
table value the same bug had been silently overriding. This pass's own
execution — hop 41, past the old effective ceiling — is live confirmation
the fix works: `read_plan_budget()` is now correctly resolving `max_5x`'s
`hops_per_day: 200` rather than the stale fallback.

**Not investigated further, and not this pass's to decide.** Whether the
same root cause also explains the *separate* `08:40:57` dropped-event
incident (`inbox/_handled/2026-08-29-eng-events-dropped.md`, processed
earlier in this same pass) is left open — that item's own recommendation to
investigate was answered `rejected` by the approver, and this pass respects
that rather than opening it back up under a different name.

**Action taken:** committing the three already-fixed files
(`departments/engineering/agents/eng-manager/config.yaml`,
`departments/engineering/lib/eng-trigger.sh`,
`instances/aiorders/engineering/config/config.yaml`) alongside this pass's
own changes, since leaving a confirmed, working fix for a department-wide
outage uncommitted indefinitely risks losing it. No further config change
made — the existing fix is sufficient and already verified live. Not
re-filed as a proposal or a fresh observation beyond what
`observations.md`'s existing `continue ENG-013` row already recorded; this
entry is the confirmation that row asked a future pass to do.

## Decision

**approved** — 2026-08-29T21:28:04.845356+00:00

I have already raised the limit, confirm if not raised then raise it mased on max_5x plan

---

**Confirmed 2026-08-29, same pass** (this decision landed on disk mid-pass,
after the Investigated section above was already written — read fresh
rather than assumed stale). Directly answering what was asked:

**Yes, already raised, and now actually taking effect.**
`departments/engineering/agents/eng-manager/config.yaml` → `plan.tier:
max_5x` (200 hops/day, 12 machine WIP, 20 hops/ticket — all three, not just
the hop ceiling). That value was already correct on disk before this pass
started, but was silently having **no effect**: `read_plan_budget()` was
reading a config path that exists on no instance, so every budget lookup
fell through to the `pro`-tier hardcoded fallback regardless of what
`plan.tier` said — which is the actual reason the ceiling fired at 40
instead of 200 today. That path bug is also already fixed on disk (found
already in place, not made by this pass), and this pass's own execution —
hop 41, past the old ceiling, still running — is live, direct proof the
fix works: `max_5x`'s real 200/day is what's governing right now, not the
stale 40. Nothing further to raise. Both fixes committed alongside this
pass's own ticket work rather than left uncommitted any longer. Journaled
in `decision-journal.md`.
