---
name: requirements-decomposition
description: Break down vague user requests into unambiguous, machine-parseable specs
metadata:
  hermes:
    tags: [requirements, product-management, decomposition]
---

# Requirements Decomposition

## When to use

Every time you receive a user request. No exceptions — even "obvious" requests hide ambiguity.

## Decomposition steps

1. **Extract the goal**: What is the user trying to achieve? One sentence, no tech.
2. **Enumerate observables**: What would a tester check to know it's done? Each criterion must be independently verifiable.
3. **Draw the boundary**: What is explicitly NOT being built? State it clearly.
4. **Surface ambiguity**: What would you need to know to avoid making an assumption?

## Anti-patterns

| Anti-pattern | Why it breaks the pipeline |
|-------------|--------------------------|
| "Implement using React" | Tech decision — Architect's job |
| "Make it fast" | Not measurable — ask: faster than what? by how much? |
| Assuming auth exists | Unstated dependency → Coder blocked |
| Skipping open questions | Architect makes assumptions → wrong design → Coder rework |
| Scope creep in criteria | Criteria should match the goal, not expand it |

## Scope boundary technique

Ask: "If the user asked for ONLY what they said, what would NOT be included?"

List those things explicitly in **Out of Scope**. This prevents scope creep in later phases.

## When in pipeline mode (no user to ask)

If open questions cannot be resolved interactively:
1. State the assumption explicitly in the spec: `Assumption: X is true because Y`
2. Flag it in Open Questions for the user to review
3. Proceed — don't block the pipeline waiting for input that may never come
