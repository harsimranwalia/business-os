# Engineering Standards

The bar every change clears before it merges. Owned by `principal-engineer`,
enforced at the code-review gate, read by every engineer before writing code.

These are the department's defaults. **A project's own conventions win.** If a
repo has its own `CLAUDE.md`, `AGENTS.md`, style config, or an obvious house
style in the surrounding code, match it — a consistent codebase beats a
correct-in-the-abstract one.

## The first rule

**Write code that reads like the code around it.** Match naming, file layout,
error handling, comment density, and idiom. A reviewer should not be able to
tell which parts of a file the team wrote.

## Change shape

- **Small, complete, reversible.** One ticket, one concern, one branch. If a
  change can't be described in a sentence, it's two changes.
- **No drive-by refactors.** Cleanup that isn't required by the ticket becomes
  its own ticket. Mixing them makes review impossible and rollback dangerous.
- **No dead code.** Don't leave commented-out blocks, unused exports, or
  feature-flagged paths with no owner and no removal date.
- **No speculative generality.** Build for the requirement in the PRD. The
  second use case is when the abstraction gets made.
- **Delete more than you add when you can.** Fewer lines that do the same thing
  is a better change, not a smaller one.

## Naming and structure

- Names say what a thing *is* or *does*, in the domain's language, not the
  implementation's. `pendingInvoices`, not `arr2`.
- Functions do one thing. If the name needs "and", split it.
- Files stay under ~400 lines as a smell threshold, not a hard rule. Past that,
  ask what wants to be its own module.
- Public interfaces are the smallest thing that satisfies the caller. Export
  deliberately; internal by default.

## Errors and failure

- Handle the error where you can do something about it. Everywhere else, let it
  propagate with context added.
- Never swallow an exception silently. An empty `catch` is a review failure.
- Every failure path a user can hit has a message that tells them what happened
  and what to do next.
- Fail closed on anything touching auth, payments, or data destruction.
- Timeouts and retries on every network call. Retries are bounded and backed off;
  never retry a non-idempotent write without an idempotency key.
- **Failure direction is uniform, and it is a reviewable property.** When a
  function fails closed on one unknown input, every other input it reads in the
  same pass is validated at the boundary or fails closed too — and when one call
  path into it is guarded, the adjacent path carries the same guard. A function
  that fails closed on most inputs is *read* as fail-closed, so the one open path
  inherits that trust and survives review. A half-validated record is a pass with
  extra steps.

  Added 2026-08-03 after three occurrences on one ticket (ENG-006, review rounds
  1–3): an unvalidated `state` beside a validated `lane`; an unvalidated
  `project` beside a validated `id`; then a guarded targeted path beside an
  unguarded sweep. Each fix created or exposed the next, which is the normal
  shape of this class rather than a signal about the engineer. The question that
  catches it: *what else does this function trust, and which other way in skips
  the check I just added?*

### zsh, specifically

The department's own tooling is zsh, so this is a standard and not a footnote:

- **Never `local path`, `cdpath`, `fpath`, `manpath`, or any other lowercase
  parameter zsh ties to an uppercase scalar.** `local path` empties `PATH` for
  the rest of that function and every external command after that line fails with
  `command not found`. Found in `lib/eng-gate-check.sh` on ENG-006 round 2, after
  passing a full review round undetected — with nothing external called below the
  declaration the bug was invisible to reading and the output was correct.
  Fourth `PATH`-shaped surprise in the department's history and the first
  self-inflicted one.

## Types and contracts

- Strict typing on. No `any` in TypeScript, no untyped public function in Python.
  If you need an escape hatch, it gets a comment explaining why.
- Validate at the boundary — every external input (HTTP body, query param, webhook
  payload, LLM output, file, env var) is parsed and validated before use.
- API contracts are versioned and backward-compatible within a version. Breaking
  a contract is an ADR, not a commit.

## Comments

- Comment *why*, not *what*. The code says what.
- A comment that explains a non-obvious constraint, a workaround, or a decision is
  valuable. A comment that restates the line below it is noise.
- No commented-out code. Git remembers.
- Every `TODO` has an owner and a ticket ID or it doesn't get merged.
- **A comment or doc that asserts a property the code does not have is a defect,
  not a nit — and the comment is the thing to trust.** When a comment states an
  invariant, read the code against the sentence rather than the sentence against
  the code: the sentence is what the author meant, so a mismatch means the code
  is wrong until proven otherwise. Promoted 2026-08-17 after the fourth occurrence
  in `lib/eng-trigger.sh` in two weeks — ENG-009 B7, ENG-016 round-1 B1 (a guard
  inserted one rung below the property its own comment claimed), ENG-016 round-1
  N2, and ENG-016 round-2 B1 (two loop docs and one comment saying a
  back-off-suppressed fire "never reaches the lock" and "writes NOTHING to the
  pass log", both false).
- **This applies to `schedules/`, `connections/` and `docs/` prose, not just to
  code comments** — those files outrank a comment, and every pass reads them
  before acting. `schedules/eng_build_loop.md` step 6b's grep is the cheap way to
  find them: start from the artifact's path or key, not from the file you thought
  of.

## Tests

Detail lives in `definition-of-done.md`. The standards position:

- Tests are written by the engineer who wrote the code, reviewed by QA, and
  extended by QA where coverage is thin. QA is not a test-writing service that
  cleans up after untested code.
- Test behaviour, not implementation. A test that breaks on a refactor with no
  behaviour change is a bad test.
- Every bug fix ships with the regression test that would have caught it. No
  exceptions — this is the single highest-leverage rule in this document.
- **A test is not evidence until it has been seen red *for the reason it exists*.**
  Mutate the threat the test is supposed to catch, not the code the assertion
  names — and when a test is parameterised, break one parameter and confirm only
  that case fails. Promoted 2026-08-20 after five instances: ENG-005 (2026-08-12,
  tests that could fail but not for the documented reason), ENG-009 (2026-08-13,
  the glob-charset guard), ENG-002 round 1 (both blocking findings — a suite that
  stayed 10/10 green with the auth gate deleted, and an anon-read assertion that
  ran against empty tables), and ENG-002 round 2, where applying this rule's own
  final clause found a three-route parameterisation that bound nothing. A
  mutation aimed at the assertion proves the assertion is wired up; only a
  mutation aimed at the threat proves the assertion is *about* something.
- No test touches production, sends real email, charges a real card, or calls a
  real LLM endpoint. Mock at the boundary.

## Dependencies

- Adding a dependency is a decision, not a convenience. Justify it in the PR:
  what it does, why not the standard library, how maintained it is.
- New dependencies go through `security` regardless of ticket size — licence,
  maintenance status, transitive weight, known CVEs.
- Pin versions. Lockfiles are committed.
- Prefer the boring, widely-used option. Novel dependencies are a maintenance
  liability that outlives the ticket.

## Git

- Branch: `{type}/{ENG-NNN}-{slug}` — e.g. `feat/ENG-014-invoice-reminders`,
  `fix/ENG-021-null-tenant`.
- Commits are imperative, present tense, and explain *why* in the body when the
  why isn't obvious. No "wip", no "fixes", no "asdf".
- Rebase or merge per the project's convention; don't introduce a new one.
- Never force-push a shared branch. Never commit secrets, `.env`, credentials,
  or generated artifacts.
- Commit messages follow each project's own footer convention where the
  project defines one.

## Performance

- Measure before optimising. A claimed hot path without a number is a guess.
- Never introduce an N+1 query. `database` reviews any change that adds a query
  inside a loop.
- Pagination on any endpoint that can return an unbounded set.
- Frontend: no blocking work on the main thread over 50ms, images sized and
  lazy-loaded, bundle growth over 10% on a single ticket needs justification.

## Observability

- Every new code path that can fail in production gets a log line with enough
  context to debug it — and no PII, no secrets, no tokens in that log line.
- Structured logs where the project supports it.
- New background job, cron, or queue consumer: it reports success/failure
  somewhere `devops` can see, or it doesn't ship.

## AI/LLM code

Architecture-level rules live in `agents/architect/config/ai-architecture-standards.md`.
Code-level:

- Prompts live in version-controlled files, never inline string-concatenated in
  business logic.
- Every model call has a timeout, a retry policy, a token budget, and a defined
  behaviour when the model returns garbage or nothing.
- Model output crossing a trust boundary is validated like any other external
  input — parsed against a schema before it reaches business logic.
- Never interpolate untrusted text into a prompt without delimiting and
  labelling it as untrusted data.
- Model IDs are config, not literals scattered through the codebase.
- No Anthropic API calls at all, on any project this department builds for the
  instance itself. The cost constraint is architectural, not a per-project
  choice.

## Automatic review failures

The code-review gate fails without discussion on any of these:

1. Secret, credential, token, or key committed
2. Silent exception swallow
3. Missing test on a bug fix
4. `any`/untyped public interface without a documented reason
5. Unbounded query or missing pagination on a collection endpoint
6. New dependency with no justification and no security pass
7. Unrelated refactor bundled into a feature change
8. Commented-out code or an unowned `TODO`
9. Direct write to a datastore that bypasses the project's data layer
10. A change to an auth, payment, or data-deletion path with no test covering the failure case
