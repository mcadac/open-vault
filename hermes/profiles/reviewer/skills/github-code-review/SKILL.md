---
name: github-code-review
description: Structured code review checklist for correctness, security, test coverage, and design adherence
metadata:
  hermes:
    tags: [code-review, quality, security, github]
---

# GitHub Code Review

## When to use

When reviewing a Coder's implementation against the Architect's design and PM's Acceptance Criteria.

## Review checklist

Run through every item. Do not skip sections.

### 1. Acceptance Criteria (from PM spec)
- [ ] Every criterion has a corresponding implementation
- [ ] Every criterion has a corresponding test
- [ ] No criterion is partially implemented

### 2. Design adherence (from Architect ADR)
- [ ] Data models match the ADR schema
- [ ] API contracts match (endpoint names, request/response shapes)
- [ ] Component boundaries respected (no cross-cutting concerns)
- [ ] Breaking changes flagged if present

### 3. Correctness
- [ ] No off-by-one errors in loops/slices
- [ ] Null/None/undefined handled at boundaries
- [ ] Error paths return appropriate errors, not silently swallow them
- [ ] Async operations awaited correctly

### 4. Security (OWASP Top 10)
- [ ] No hardcoded secrets or credentials
- [ ] User input validated/sanitized at system boundaries
- [ ] SQL uses parameterized queries (no string concatenation)
- [ ] Auth checks on every protected endpoint
- [ ] No sensitive data in logs

### 5. Test quality
- [ ] Tests cover happy path AND error paths
- [ ] Tests are independent (no shared mutable state)
- [ ] Tests test behavior, not implementation details
- [ ] Coverage adequate (80%+ for new code)

### 6. Code clarity
- [ ] Complex invariants have a comment explaining WHY
- [ ] No dead code
- [ ] No TODO comments left in (file issues instead)

## Output

Produce ONLY:

```
APPROVED
```

or:

```
REJECTED

Issues:
1. <file>:<line> — <problem> — <required fix>
2. ...
```

Security issues always block approval. Style issues without correctness impact do not.
