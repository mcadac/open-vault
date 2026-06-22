---
name: test-driven-development
description: RED-GREEN-REFACTOR cycle for writing tested code from the start
metadata:
  hermes:
    tags: [testing, tdd, quality, pytest, jest]
---

# Test-Driven Development

## The cycle

```
RED   → write a failing test for the next piece of behavior
GREEN → write the minimum code to make it pass
REFACTOR → clean up without breaking the test
```

Never write implementation code before the test. If you do, you can't know the test is actually testing anything.

## Step-by-step

1. **Pick one behavior** from the Acceptance Criteria or Implementation Plan
2. **Write the test** — it should fail with a clear error (not an import error)
3. **Run the test** → confirm RED
4. **Write the minimum implementation** — don't solve future requirements
5. **Run the test** → confirm GREEN
6. **Refactor** — remove duplication, clarify names, simplify
7. **Run the test** → still GREEN
8. Repeat for next behavior

## Anti-patterns

| Anti-pattern | Problem |
|-------------|---------|
| Write all code, then all tests | Tests verify what code does, not what it should do |
| Write test and implementation together | Same bias problem |
| Test implementation details | Tests break on refactor; test behavior instead |
| Skip RED step | Test may always pass → tests nothing |
| Giant test covering everything | Failure message is useless; test one behavior |

## pytest patterns

```python
# Arrange-Act-Assert
def test_login_returns_token_on_valid_credentials():
    # Arrange
    user = create_user(email="a@b.com", password="secret")
    # Act
    result = login("a@b.com", "secret")
    # Assert
    assert result.token is not None

# Parametrize for edge cases
@pytest.mark.parametrize("email,password,expected", [
    ("", "secret", AuthError),
    ("a@b.com", "", AuthError),
    ("unknown@b.com", "secret", AuthError),
])
def test_login_rejects_invalid_input(email, password, expected):
    with pytest.raises(expected):
        login(email, password)
```

## Coverage target

Aim for 80%+ branch coverage on new code. 100% is not the goal — untestable branches (e.g. OS errors) are acceptable to skip.

Run coverage: `pytest --cov=. --cov-report=term-missing`
