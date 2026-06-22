---
name: github-issues
description: Create and manage GitHub issues for features using the gh CLI
metadata:
  hermes:
    tags: [github, issues, project-management]
prerequisites:
  commands: [gh]
---

# GitHub Issues

Use this skill to create a GitHub issue for every feature spec produced.

## When to use

After producing a PM spec, if `GH_TOKEN` is set in the environment.

## Check GH_TOKEN

```bash
[ -n "$GH_TOKEN" ] && echo "GH available" || echo "skip — no GH_TOKEN"
```

If no token, skip silently. Do not fail.

## Create issue

```bash
gh issue create \
  --title "<Goal — one sentence>" \
  --body "$(cat <<'EOF'
## Goal
<paste>

## Acceptance Criteria
- [ ] ...

## Out of Scope
- ...

## Open Questions
- ...
EOF
)" \
  --label "feature"
```

## Label conventions

| Type | Label |
|------|-------|
| New feature | `feature` |
| Bug fix | `bug` |
| Refactor | `refactor` |
| Docs | `documentation` |

## Output

After creating the issue, include the issue URL in your spec output:

```
GitHub Issue: https://github.com/<owner>/<repo>/issues/<n>
```
