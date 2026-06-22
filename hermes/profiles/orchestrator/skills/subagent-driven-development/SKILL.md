---
name: subagent-driven-development
description: Patterns for passing context between subagents and validating their outputs in a dev pipeline
metadata:
  hermes:
    tags: [orchestration, multi-agent, context-passing]
---

# Subagent-Driven Development

## Context passing

Each subagent starts with no memory of prior phases. You must pass all relevant context in every dispatch.

**Minimum context per phase:**

| Phase | Required context |
|-------|-----------------|
| PM | Raw user request |
| Architect | Full PM spec (Goal + Criteria + Scope + Questions) |
| Coder | Full Architect ADR (Decision + Implementation Plan + Data Models) |
| Reviewer | Architect ADR + Coder's implementation summary + changed files |
| Tester | PM Acceptance Criteria + Coder's test summary |
| Tech-Writer | Architect ADR + Coder's files changed + PM Goal |

Never summarize prior phases — pass verbatim output. Summaries lose precision.

## Two-stage output validation

After each subagent responds, validate:

**Stage 1 — Format check**: Does the output match the expected format?
- PM: contains `## Goal`, `## Acceptance Criteria`, `## Out of Scope`
- Architect: contains `## Status`, `## Decision`, `## Implementation Plan`
- Coder: contains `## Implementation Summary`, `## Test Results`
- Reviewer: starts with `APPROVED` or `REJECTED`
- Tester: starts with `PASS` or `FAIL`
- Tech-Writer: contains `## Documentation Summary`

**Stage 2 — Quality check**: Does the output actually satisfy the phase goal?
- PM: are open questions listed (not silently assumed)?
- Architect: is every Acceptance Criterion addressed in the plan?
- Coder: do tests pass? Are deviations from design flagged?
- Reviewer: is rejection feedback specific (file:line:issue)?
- Tester: are all Acceptance Criteria covered by tests?

If Stage 1 fails → retry with format reminder.
If Stage 2 fails → treat as a REJECTED/FAIL and enter the retry loop.

## Fresh subagent per task

Each dispatch is a fresh conversation. Do not assume the subagent remembers anything from a previous dispatch. This is by design — it prevents context contamination between pipeline runs.
