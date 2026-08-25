# Observations

"While I was in there, I noticed..." — the thing a good engineer mentions on the
way past. Not a bug, not a ticket, not a request. Cheap to file, no obligation
on anyone, and worth more in aggregate than any single one is alone.

## Rules

- Any agent may append. No permission, no owner, no reply expected.
- One line each, newest last, under the Ledger below.
- An observation is not work. If it needs doing it is a bug or a proposal —
  file it as one instead of writing it here and hoping.
- Nothing reads this on a pass. It is read by the weekly report and by a human.

## Format

`| {date} | {agent} | {project} | {what you noticed} |`

## Ledger

| Date | By | Project | Observation |
|---|---|---|---|
| 2026-08-24 | eng-manager | aiorders | `board/_index.md` carries no "next ID" counter, though `config/templates/ticket.md` says IDs are never reused and the next one lives there — worth adding before ENG-002 gets allocated. |
| 2026-08-25 | product-manager | aiorders | Three approver-filed requests in `inbox/requests/` (`a4-poster-generator-unwired`, `admin-hub-migration-history`, `aiorders-env-hygiene`, all `received: 2026-08-23`) are still unshaped two days later — out of scope for this `continue ENG-001` pass, so left untouched, but worth flagging: `watch` isn't wired on this instance yet (`eng_build_loop.md`'s own note), so nothing but the twice-daily scheduled sweep would otherwise find them. None is P0, but `aiorders-env-hygiene` names a live cost exposure (an unrestricted Google Maps API key) that's worth not leaving to chance. |
| 2026-08-25 | product-manager | aiorders | `config/definition-of-done.md`'s "Ticket states" table lists `intake`'s owner as `eng-manager`, contradicting the paragraph directly beneath it ("`intake` and `shaped` are owned by the **product-manager**... corrected 2026-07-27"), the ticket template's own `owner: product-manager` default, and `agents/product-manager/agent.md`'s description of intake as the PM's job. Went with the prose + template + agent.md (unanimous) over the stale table cell for this pass; the table row itself is still wrong on disk. |
| 2026-08-25 | product-manager | aiorders | Shaping `ENG-003` (env hygiene) hit a ticket-schema gap: the work genuinely spans three repos (`config-site-builder`, `aiorders-admin-hub`, `restaurant-marketplace`), but `config/templates/ticket.md` models `project:`, `branch:` and `links.pr` as singular. Scoped the ticket's primary `project:` to `config-site-builder` (the repo with the actually-tracked secret) and named the other two repos' fixes explicitly in the PRD rather than inventing a multi-project ticket shape unilaterally — left for whoever picks this up at `building` to resolve the branch/PR mechanics. |
| 2026-08-25 | product-manager | aiorders | The architect's blind reading on `ENG-004` (admin-hub migration history) caught that `config/projects.md`'s registry records each repo's stack/deploy-target/autonomy but not which Supabase *project* it's linked to — so "is `aiorders-admin-hub` on the same database as `aiorders-api`" (the actual question ENG-004 needs to answer) isn't answerable from the registry as it stands today. |
| 2026-08-25 | eng-manager | aiorders | The first `scheduled (manual-unblock)` attempt at this pass (three full request-readbacks plus board updates in one session) hit the 1800s pass timeout and was killed mid-edit; the retry (this pass) picked it up from the on-disk state and found the substantive work already complete and consistent — only the board index's In-flight table rows for the three new tickets were missing. Worth a look if intake-heavy scheduled sweeps keep running long: either split business intake across more passes, or the timeout has room to grow — not filed as a proposal since one data point isn't a pattern yet. |
| 2026-08-25 | eng-manager | aiorders | This `watch` pass found `traces/.pending` carrying `1 scheduled instances/aiorders/engineering/agents/eng-manager/board/ENG-001-register-repos-and-prove-the-loop.md` — a `scheduled` event whose context is a ticket board file path. Both plist generators in `lib/eng-schedule.sh` invoke `scheduled` with context `launchd`, and the one manually-fired `scheduled` pass logged today used `manual-unblock`; this entry matches neither. Harmless today — `eng-trigger.sh` gives `scheduled`/`watch` an empty `TICKET_ID` regardless of context — but worth tracing to its source if it recurs. |
