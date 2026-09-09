# 2026-09-09 — ENG-051 closes out (container → verified)

`continue ENG-051` event pass, ~07:14 PDT start. Checkpoint fired in (last log
entry, 06:52 PDT) still described both children `blocked`/`blocked_on:
approver`, PRs #24/#25 `OPEN`. That was ~22 minutes stale by the time this
pass actually read the files — both had already flipped `blocked → shipped`
via the control center's own merge detection, ahead of this pass. Independent
re-verification, not inherited: `wc -l` matched the checkpoint's 2754 exactly
before touching anything; frontmatter read fresh for both children.

## Integrity incident — re-checked, unchanged, not re-derived at length

`inbox/2026-09-08-eng-loop-integrity-check.md`: no `decision:` field.
`decision-journal.md`: 2026-09-08/09 rows are `ENG-048`/`ENG-049` merges,
`ENG-051`'s own G1, `ENG-018`'s G1 `changed` — none names the designed-pool
decision. All four disputed files still `M`, uncommitted (git status, both
`departments/engineering/...` and the instance copies). Same conclusion as
the ~20 prior reconfirmations catalogued in memory
(`project-eng-never-idle-policy`): acute risk closed, policy question still
open, still needs Harry's direct word. Not re-derived further here — this
pass's actual news is unrelated to that dispute (below).

## What actually happened this pass

Both children shipped for real (`git fetch` + `merge-base --is-ancestor`
against `origin/main` from the department's own `_eng/aiorders-api`
worktree, independent of the control center's claim) — ran the full
`acceptance-check/SKILL.md` walk on both, live, not against the test suite.
Full per-criterion reasoning: `agents/product-manager/notebook/2026-09-09-eng052-eng053-acceptance.md`.
Both → `verified`. That settles `ADR-003`'s parent-exemption condition (every
child `shipped`/`verified`/`dropped`, at least one shipped) — `ENG-051`
itself owes no receipts of its own, so it carries `building → shipped →
verified` this same pass, same shape `ENG-027` used for itself once
`ENG-048`/`ENG-049` both verified.

**Side effect worth naming plainly:** this closes the ~20-hop, ~14-fire-since-
midnight `continue ENG-051` saga from a completely different angle than the
06:52 hop's own finding. That hop confirmed `lib/eng-drain-poll.sh`'s IDLE
POLL half fires `continue ENG-051` because it's the only ticket in the
machine's range and the poll can't see the container/Guards rule — a real
bug, correctly left unpatched (live, shared, multi-instance scheduler; not
this session's call to make alone). `ENG-051` reaching `verified` doesn't fix
that bug, but it does remove *this specific instance's* trigger condition:
once `ENG-051` leaves `ready..ready-to-ship` for a terminal state, the
machine's range on this board is empty, so the poll's board-scan has nothing
to pick. Whether it goes fully quiet or falls back to some other behavior
(e.g. a `scheduled auto-idle` per the never-idle-policy memory) is worth
confirming on the next pass rather than assumed here — flagged, not claimed
fixed. The bug itself is still live and would resurface the moment another
lone container ticket sits at `building` with only parked/verified children
and nothing else in range.

## 6b — filing item 5 of the `ENG-006` sequence

`ENG-051` reaching `verified` is itself the trigger `acceptance-check` step
6b names: PRD names a next item (`ENG-006`'s own `## Feature shape and
sequencing`, item 5 — "Admin/support surfaces — internal lookup,
cross-restaurant view for support, and manual ledger adjustment/void.
Depends on ENG-006 and (3)"), and the standing sequence-wide authorization is
`ENG-006`'s own G1 answer (*"the proposed five-ticket sequence stands as
shape to file incrementally"*) — the same authorization already used to file
`ENG-051` itself once `ENG-027` verified. Filed `ENG-054`, step 1b only
(board file + one-line problem, project/type/size/lane set, `Next ID`
counter advanced) — PRD content deliberately left to a dedicated hop, same
reasoning `ENG-051`'s own step-1b stub gave, not a model-tier constraint
(`prd-writer`'s `Model: opus` field is stale department-wide since
2026-08-20). This is the fifth and last item in `ENG-006`'s proposed shape —
no further sequence-filing chain after this one.

## Git operations this pass (full account — ticket logs reference this)

All from `~/Documents/projects/_eng/aiorders-api` (repo-isolation guard —
never the approver's interactive clone at
`~/Documents/projects/aiorders/aiorders-api`, untouched): `git fetch origin
main`; `git merge-base --is-ancestor` (x2, read-only); `git checkout main`
(failed — already checked out in the other worktree, harmless no-op); `git
pull origin main --ff-only`, which — since the failed checkout left the
worktree on its prior branch, `feat/ENG-053-...` — fast-forwarded that
already-merged, now-stale local branch ref from `ec5e099` to `16a4932`
(strict ancestor either way; ff-only guarantees no rewrite, no data loss;
the branch is dead weight post-merge regardless). `supabase migration list
--linked` (read-only), `supabase db query --linked` (exactly one `select
has_function_privilege(...)`, no mutation, three booleans returned), `supabase
functions list` (read-only). No `push`, no force op, no write to
`loyalty_ledger_entries` or any other table. business-os itself: left
uncommitted, standing default per the open commit-convention question
([[project-buildloop-instance-repo-commit-gap]] equivalent), not re-decided
here.

## Board bookkeeping

`_index.md`: In-flight table — `ENG-051`/`ENG-052`/`ENG-053` rows removed
(all terminal), `ENG-054` row added (`intake`). `Next ID` counter
`ENG-054 → ENG-055` with one line of reasoning. Dated-entry roll checked
against the keep-three rule before adding today's entry.
`decision-journal.md`: two new rows, `ENG-052`/`ENG-053` L1 merges (no
written reply — same standing pattern this approver always uses, confirmed
directly via `gh pr view` this pass, not assumed from the control-center
label alone).
