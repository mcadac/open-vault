---
name: codebase-inspection
description: Navigate an unfamiliar codebase to find entry points, key interfaces, and relevant code before implementing
metadata:
  hermes:
    tags: [codebase, navigation, inspection, understanding]
---

# Codebase Inspection

Run this before touching any code in an unfamiliar codebase.

## When to use

- First time implementing in a repo
- When the Architect's design references existing components
- Before reviewing code you didn't write

## Inspection steps

### 1. Get the lay of the land
```bash
# Directory structure (top 2 levels)
find . -not -path "*/\.*" -not -path "*/node_modules/*" -not -path "*/.venv/*" \
  | head -60

# Language breakdown
find . -name "*.py" -o -name "*.ts" -o -name "*.go" | wc -l
```

### 2. Find the entry point
```bash
# Python
grep -r "if __name__ == '__main__'" --include="*.py" -l
cat pyproject.toml | grep -A5 "\[tool.poetry.scripts\]"

# Node/TS
cat package.json | grep '"main"\|"start"'

# Go
find . -name "main.go"
```

### 3. Trace the request path
Follow the request from entry point to the component you're changing. Read the actual code — don't guess.

### 4. Find relevant existing code
```bash
# Find functions/classes by name
grep -r "def authenticate\|class Auth\|function auth" --include="*.py" --include="*.ts" -l

# Find where a module is imported
grep -r "from auth import\|import auth" --include="*.py" -l
```

### 5. Check existing tests
```bash
find . -path "*/test*" -name "*.py" -o -path "*/spec*" -name "*.ts" | head -20
```

Look at 1-2 existing tests to understand the testing conventions before writing new ones.

## What to capture

Before implementing, note:
- Entry point file + function
- The component you're changing and its current interface
- Any existing tests for that component
- Any utility functions you can reuse
