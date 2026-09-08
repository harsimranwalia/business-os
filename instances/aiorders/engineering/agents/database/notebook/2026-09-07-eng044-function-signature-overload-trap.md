# CREATE OR REPLACE FUNCTION does not error on a changed argument count — it silently overloads

Found during `ENG-044`'s build hop (`continue ENG-044`, 2026-09-07), while
adding a new defaulted parameter (`p_channel`) to an existing function
(`get_restaurants_optimized`).

**The assumption that turned out wrong:** that `CREATE OR REPLACE FUNCTION`
would either replace the existing function or fail loudly (Postgres's real
"cannot change return type of existing function" error, which the 2024
source migration's own leading `DROP FUNCTION IF EXISTS` already defends
against). Tested directly, disposable container: recreated the live 13-arg
function, then ran `CREATE OR REPLACE FUNCTION` with a 14-arg signature (one
new defaulted parameter appended) and no leading `DROP`. **It succeeded with
no error** — `pg_proc` then showed two coexisting overloads, old and new,
under the same function name.

**Why this is dangerous rather than merely untidy.** Postgres resolves an
overloaded call to the candidate needing the fewest defaulted arguments. A
caller still using the historical positional argument count keeps resolving
to the **old** function — permanently, silently, regardless of how correct
the new one is. For a security- or visibility-gating change (this ticket's
own channel gate), that means the gate is live in the schema but unreachable
by any caller that hasn't been updated to pass the new argument — the kind of
gap that reads as "shipped" everywhere except production behavior.

**What actually closes it:** `DROP FUNCTION IF EXISTS
<name>(<exact old positional type list>)` immediately before the `CREATE OR
REPLACE`, matched on types, not names or defaults. Verified this resolves it
cleanly: re-ran the real migration file against the two-overload state above
and confirmed exactly one function (14 args) remained.

**For the next ticket that adds or removes a parameter on an existing
function** (not just changes its body): this only bites when the *argument
count* changes. A same-arg-count edit (changing a default value, a body-only
change) is the ordinary, safe `CREATE OR REPLACE` case this doesn't apply to.
Check `pg_proc` for the exact live type list before writing the `DROP`, the
same way this ticket confirmed it against a fresh `supabase db dump` rather
than assuming the last-known signature is still current.

## Two small corrections to `2026-09-04-host-tooling-capability.md`

- **Linking is not necessarily persistent across sessions.** That entry
  found `aiorders-api` already linked; this pass found `supabase projects
  list` showing it *not* linked on this run, requiring one non-interactive
  `supabase link --project-ref bmnmnejwdxbcqinqkwko` before `--linked`
  commands worked. Cheap either way (no password prompt either time) — just
  don't assume the prior pass's linked state carried forward; check first.
- **Use the fully-qualified cached tag for the disposable-container image.**
  `docker run ... supabase/postgres:15.8.1.073` (no registry prefix) misses
  the already-pulled `public.ecr.aws/supabase/postgres:15.8.1.073` image
  entirely and triggers a fresh multi-GB pull from Docker Hub under a
  different image ID. Use the full `public.ecr.aws/supabase/postgres:<tag>`
  reference to actually hit the cache `2026-09-04`'s pass left behind.
