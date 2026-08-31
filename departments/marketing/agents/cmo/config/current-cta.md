# Current CTA — TEMPLATE

**This is a template.** The live copy lives at
`$MKT_INSTANCE/agents/cmo/config/current-cta.md`. Edit that copy any time; the
CMO reads it on every planning run and it takes effect on the next one. No
config change, no redeploy.

This file exists so that changing what the business is currently asking for is
a one-file edit rather than a hunt through drafts, briefs and skill prompts.
That is its entire job.

---

## The CTA

> _Write it here, in the business's own voice, as it would appear in a piece._
>
> Two to four sentences. What the business is doing right now, who it is for,
> and the single action to take. One action — a CTA offering two paths gets
> neither.

_[Replace this with the live CTA.]_

---

## Rules that bind every use of it

- **Roughly one CTA per four pieces, hard-capped at one per week** regardless of
  how many pieces run or how many channels they span. Which archetype carries it
  rotates — never the same archetype twice running. Exact numbers:
  `$MKT_INSTANCE/config/config.yaml` → the channel's `cta_rotation`.
- **Never in body copy: price.** The offer's shape can be named; the number
  cannot. Price belongs in a conversation, not in a piece that gets screenshotted.
- **Not "DM me to learn more."** That is on the anti-patterns list because it
  asks for effort without saying what the reader gets for it.
- **One CTA per piece, at the end.** On a multi-part format it goes on the last
  part only, never mid-thread.
- **The CTA is not the point of the piece.** A piece that only exists to carry
  a CTA reads exactly like one. If the piece would not be worth publishing
  without the last paragraph, the CTA is not the problem.

## When to update

- The offer changed, or a new one launched
- Capacity sold out — an unchanged CTA asking for work that cannot be taken is
  worse than no CTA
- The ICP language shifted after an M1 revision to the positioning statement
- The preferred response changed ("reply here" vs "book a call" vs "reach out")

## When *not* to update

Not for variety. A CTA that changes every few weeks reads as a business that
does not know what it sells. Repetition is how a reader eventually notices it —
the fifth exposure is usually the one that converts, and it only works if the
first four said the same thing.
