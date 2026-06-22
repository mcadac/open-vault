---
name: workspace-dispatch
description: Delegate a task to a specialist profile using a structured 4-field format
metadata:
  hermes:
    tags: [orchestration, delegation, multi-agent]
---

# Workspace Dispatch

Use this skill whenever you need to hand off work to another profile in the dev team.

## When to use

Every time you move between pipeline phases. Never describe a task to a subagent in free-form prose — always use the structured format below.

## Dispatch format

```
To: <profile-name>
Objective: <single sentence — what must be achieved>
Context: <prior phase output pasted verbatim or summarized>
Expected Output: <exact format + success/failure signal>
```

## Rules

- **To** must be a real profile name: `pm`, `architect`, `coder`, `reviewer`, `tester`, `tech-writer`.
- **Objective** is one sentence. If you need more, you're delegating too much at once — split it.
- **Context** must include the prior phase's full output. Subagents have no shared memory by default.
- **Expected Output** must specify the exact format AND what constitutes done (e.g. `APPROVED`, `PASS`, implementation summary).
- Never dispatch without all 4 fields.

## Example

```
To: coder
Objective: Implement the user authentication module per the Architect's design.
Context:
  [Paste full Architect ADR here — Status, Context, Decision, Implementation Plan, Data Models]
Expected Output:
  Implementation Summary + Files Changed + Test Results.
  Tests must pass. If any test fails, output BLOCKED: <reason>.
```

## After dispatch

Wait for the subagent's response. Check the Expected Output format. If the response is malformed or missing the success signal, treat it as a failure and retry (max 2 retries before halting).
