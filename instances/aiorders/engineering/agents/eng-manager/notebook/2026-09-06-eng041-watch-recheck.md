# 2026-09-06 — `ENG-041` watch-event recheck (no change)

`watch` event pass, context `launchd`. Full reasoning for the short ticket-log
entry on `agents/eng-manager/board/ENG-041-customer-questions-and-faq-editor.md`.

## Why this pass fired

The file-watcher fired on `ENG-041`'s own merge-request file
(`inbox/2026-09-06-eng041-merge-request.md`) appearing in `inbox/` — written
directly by the prior `continue ENG-041` pass's own release-runner hop, not
through the notify/decision-poll channel. That is exactly the "gate item...
not through the control center" shape `eng_build_loop.md` defines the `watch`
event for.

Reading map for `watch`: steps 2, 3 and 4 (sweeps all three inboxes) and step
5, since the changed file is a merge-request item, plus the not-negotiable set
(1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*) — read
in full (whole document, ~730 lines). Mode check clean (repo-root `.env` →
`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-041`) and
whole-board: both exit 0, clean.

## Steps 2–4 — swept all three watched inboxes

`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold nothing
but their own `_handled`/`_processed` folders, both already actioned by
earlier passes (nothing new since 2026-09-06 02:48 and 2026-09-01
respectively); `inbox/requests/` is empty.

`inbox/` itself holds six open items. Checked every one's frontmatter
`decision:` field and its own `## Decision` section body directly, not the
field alone (the hand-edit case this event exists to catch):

| File | `decision:` | `## Decision` body |
|---|---|---|
| `2026-09-04-eng016-continue-piece2-question.md` | blank | "Filled in by the approver." |
| `2026-09-06-eng018-g1-scope.md` | blank | "Filled in by the approver." |
| `2026-09-06-eng028-g1-rescope.md` | blank | "Filled in by the approver." |
| `2026-09-06-eng041-merge-request.md` | blank | n/a (release-runner template, no `## Decision` section) |
| `2026-09-06-eng042-g1-scope.md` | blank | "Filled in by the approver." |
| `2026-09-06-eng043-stage-names-clarification.md` | blank | "Filled in by the approver." |

Nothing answered, nothing new to act on under steps 2–4.

## Step 5 — merge detection

`ENG-041`'s own merge request is the item that fired this event, so step 5
runs for this ticket specifically (not a whole-board sweep — that's the
`scheduled` pass's job).

```
cd ~/Documents/projects/aiorders/restaurant-portal
git fetch origin --quiet
git merge-base --is-ancestor origin/feat/ENG-041-customer-questions-and-faq-editor origin/main
# → exit 1, NOT an ancestor
gh pr view 5 --json state,mergedAt,baseRefName,headRefName
# → {"baseRefName":"main","headRefName":"feat/ENG-041-...","mergedAt":null,"state":"OPEN"}
```

PR #5 still open, not merged. No transition. `state`/`owner` unchanged
(`blocked`/`approver`). Machine WIP unaffected — still `1/1` (`ENG-021`
family). Approver-facing WIP unaffected (`unlimited` since 2026-09-02; this
item stays counted, same as before this pass).

## Notify sweep — and the timezone-basis check

Current local time at check: `2026-09-06T11:28:53` PDT (`date` on this host).
`notified:`/`nudged:` frontmatter values on this board are themselves stamped
in local wall-clock time, copied verbatim from `lib/eng-notify.sh`'s own log
(confirmed on `ENG-041`'s own release-readiness entry, which stamped
`notified: 2026-09-06T11:16:37` "copied verbatim from the log"). The
immediately preceding pass (`ENG-041`'s release-readiness hop) filed an
observation that several ticket-log "current time" reads have instead used a
UTC `Z`-suffixed value against those same local stamps, producing a ~7h
over-count. This check deliberately kept both readings on the same (local)
clock to avoid repeating that:

| Item | `notified:` (local) | Age at 11:28:53 |
|---|---|---|
| `ENG-016` | 2026-09-04T10:58:06, `nudged:` 2026-09-05T09:31:45 | already carries its one-ever nudge |
| `ENG-018` | 2026-09-06T03:13:31 | ~8h15m |
| `ENG-028` rescope | 2026-09-06T02:28:29 | ~9h00m |
| `ENG-041` | 2026-09-06T11:16:37 | ~12m |
| `ENG-042` | 2026-09-06T02:28:29 | ~9h00m |
| `ENG-043` | 2026-09-06T02:47:56 | ~8h41m |

All well under the 24h nudge threshold on either basis (the mixed-basis
reading used by earlier passes today would put these at ~14-16h, still under
24h — no wrong nudge decision resulted from the skew today, but it remains a
live risk for anything that ages past ~17h local under the mixed reading
while still under 24h true local age). No nudge due on any.

## Everything else

**Dead-end sweep (scoped to this event):** no other ticket touched — a
`watch` event's own narrower contract, same precedent `ENG-032`'s own
2026-09-03 watch-pass entry set. **Observations:** one filed
(`observations.md`) — most of `ENG-041`'s own ticket-log entries (build,
review, security hops) run 60-90+ lines against `conventions.yaml`'s
`ticket_log.entry.cap_lines: 20`, without falling under any of the three
allowed exceptions (`gate_fail`, `incident`, `approver_answer_verbatim`);
only devops's release-readiness entry on this same ticket explicitly followed
the cap. **Step 6b:** not run — no artifact rule (receipt path, state name,
config key, process file) written or relied on by this hop. **Exceptions/
journal:** n/a — no `exception-request:`, no G1/G2/G3/merge-request answered
this pass.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-041`) and whole-board: both
exit 0, clean.

`chained: none` — waiting on the approver, unchanged (`blocked`,
`blocked_on: approver`; PR #5 still open, no answer). Per `eng_build_loop.md`
step 9, a ticket waiting on the approver is never chained.

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.
