---
name: plan
description: Write Architecture Decision Records (ADRs) that developers can implement without further design decisions
metadata:
  hermes:
    tags: [architecture, adr, design, planning]
---

# Plan (ADR Format)

Use this skill to produce a complete technical design from a PM spec.

## When to use

After receiving a PM spec with a clear Goal and Acceptance Criteria.

## ADR sections — what goes where

| Section | Content | Common mistake |
|---------|---------|---------------|
| **Status** | `Proposed` always at this stage | Setting `Accepted` before review |
| **Context** | The problem and constraints, referencing the PM spec | Restating the solution instead of the problem |
| **Decision** | The chosen approach — tech stack, patterns, key components | Being too vague ("use a database") or too specific ("use this exact SQL") |
| **Alternatives Considered** | 2-3 options you rejected and why | Strawmanning alternatives |
| **Implementation Plan** | Numbered steps a developer follows | Skipping steps, assuming knowledge |
| **Data Models / Interfaces** | Types, schemas, API contracts | Omitting this — it's the most critical handoff to the Coder |
| **Risks & Mitigations** | What could go wrong and how to handle it | Ignoring risks to seem decisive |

## The developer handoff test

Before finalizing, ask: "Could a developer implement this without asking me any questions?" If the answer is no, identify which section is incomplete and fill it.

Typical gaps:
- Missing data model → Coder invents their own → Reviewer rejects it
- Vague implementation steps → Coder makes wrong tech choices
- No API contract → frontend/backend integration breaks

## Scope discipline

Stay at the interface level. Define WHAT components do and HOW they connect, not HOW they work internally. Example:

- ✓ `POST /auth/login → returns JWT + refresh token`
- ✗ `Use bcrypt with salt rounds 12 inside the password comparison function`

The first is an interface contract. The second is implementation — leave it to the Coder.
