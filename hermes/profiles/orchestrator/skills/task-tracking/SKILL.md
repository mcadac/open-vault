---
name: task-tracking
description: Track pipeline phase state and loop counts to prevent runaway retries
metadata:
  hermes:
    tags: [orchestration, state-management, pipeline]
---

# Task Tracking

Use this skill to track where each task is in the pipeline and how many times it has been retried.

## When to use

At the start of every pipeline run and after every phase transition.

## State machine

```
backlog → pm → architect → coder → review-loop → test-loop → docs → done
                                         ↑___↓            ↑___↓
                                      (max 3)          (max 3)
```

## Tracking format

Maintain a task record in your working memory:

```
Task: <task name>
Phase: <current phase>
Review loops: <n>/3
Test loops: <n>/3
Status: in-progress | blocked | done
Last output: <brief summary of last subagent response>
```

## Loop rules

- Increment `Review loops` every time you dispatch back to `coder` after a `REJECTED`.
- Increment `Test loops` every time you dispatch back to `coder` after a `FAIL`.
- If either counter reaches 3 without resolution: set Status to `blocked`, stop the pipeline, report to user with full history.

## Phase transition checklist

Before advancing to the next phase:
- [ ] Current phase produced the expected output format
- [ ] Output written to memory (so the next agent has context)
- [ ] Loop counter within limit

## Halting

When halting, report:
1. Which phase failed
2. How many loops were attempted
3. The last subagent output verbatim
4. What the user should do next (manual fix, clarify requirements, etc.)
