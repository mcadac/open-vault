---
name: github-pr-workflow
description: Full GitHub PR lifecycle from branch creation to merge using gh CLI
metadata:
  hermes:
    tags: [github, git, pr, workflow]
prerequisites:
  commands: [gh, git]
---

# GitHub PR Workflow

## When to use

After completing an implementation that's ready for review. Also used by Tester after tests pass and Tech-Writer after docs are updated.

## Full lifecycle

### 1. Create branch
```bash
git checkout -b feat/<short-description>
# or fix/, refactor/, docs/ prefix as appropriate
```

### 2. Stage and commit
```bash
git add <specific files>  # never git add -A — review what you're staging
git commit -m "feat: <what and why in 50 chars"
# Multi-line for context:
git commit -m "feat: add JWT authentication

Implements login/logout with short-lived access tokens and
7-day refresh tokens. Refresh token stored in httpOnly cookie."
```

Conventional commit prefixes: `feat:` `fix:` `refactor:` `test:` `docs:` `chore:`

### 3. Push
```bash
git push -u origin HEAD
```

### 4. Create PR
```bash
gh pr create \
  --title "feat: <description>" \
  --body "$(cat <<'EOF'
## Summary
- What changed and why (2-3 bullets)

## Test plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual test: <what to click/call>
EOF
)"
```

### 5. After review approval
```bash
gh pr merge --squash --delete-branch
```

## Check PR status
```bash
gh pr status          # your open PRs
gh pr checks          # CI status on current branch
gh pr view --web      # open in browser
```

## If push is blocked (force push needed)

**Do not force push without user confirmation.** Report the conflict and ask the user how to proceed.
