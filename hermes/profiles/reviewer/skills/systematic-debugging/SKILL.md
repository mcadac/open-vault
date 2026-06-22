---
name: systematic-debugging
description: Isolate and fix bugs using a structured hypothesis-verification loop
metadata:
  hermes:
    tags: [debugging, troubleshooting, testing]
---

# Systematic Debugging

Never guess at a fix. Always verify your hypothesis first.

## When to use

When a test fails, code doesn't behave as expected, or an error needs root cause analysis.

## The loop

```
OBSERVE → HYPOTHESIZE → VERIFY → FIX → CONFIRM
```

1. **Observe**: Read the exact error message and stack trace. Don't paraphrase — the exact text matters.
2. **Hypothesize**: Form one specific hypothesis. "I think X is happening because Y."
3. **Verify**: Add a minimal reproduction or diagnostic (print/log/assert) to confirm or deny the hypothesis. Do not fix yet.
4. **Fix**: Only after the hypothesis is confirmed, apply the minimal fix.
5. **Confirm**: Re-run the failing test. It must pass. Run the full test suite. Nothing new must fail.

## Binary search approach

For complex bugs with many possible causes:
1. Find the midpoint where behavior changes from correct to incorrect
2. Add a check at the midpoint
3. If correct at midpoint → bug is in the second half
4. If incorrect at midpoint → bug is in the first half
5. Repeat until isolated

## Common causes to check first

| Symptom | Common cause |
|---------|-------------|
| `AttributeError: NoneType` | Function returns None when caller expects an object |
| `KeyError` | Dict key assumed to exist — check with `.get()` |
| Off-by-one | Loop bounds, list slicing, index math |
| Async race condition | Missing `await`, wrong event loop |
| Import error | Circular import, wrong package installed |
| Test passes locally, fails in CI | Environment variable missing, timezone difference, file path |

## Rules

- Never suppress an exception to make a test pass
- Never modify test assertions to match wrong behavior
- If you can't reproduce the bug, you can't fix it reliably — stop and report
