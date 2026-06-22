---
name: browser-harness
description: E2E test patterns using Playwright for UI testing, screenshot capture, and assertion strategies
metadata:
  hermes:
    tags: [e2e, playwright, testing, browser, automation]
prerequisites:
  commands: [playwright, npx]
---

# Browser Harness (Playwright)

Use this skill for E2E and smoke tests that require a real browser.

## When to use

When Acceptance Criteria include UI behavior, user flows, or API interactions that only make sense end-to-end.

## Setup check
```bash
npx playwright --version 2>/dev/null || pip show playwright 2>/dev/null || echo "playwright not installed"
```

If not installed: `pip install playwright && playwright install chromium` or `npm install @playwright/test`.

## Basic test structure (Python)

```python
from playwright.sync_api import sync_playwright

def test_login_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("http://localhost:3000/login")
        page.fill('[name="email"]', "test@example.com")
        page.fill('[name="password"]', "secret")
        page.click('[type="submit"]')

        # Assert redirect to dashboard
        page.wait_for_url("**/dashboard", timeout=5000)
        assert "/dashboard" in page.url

        browser.close()
```

## Screenshot on failure

```python
try:
    page.wait_for_url("**/dashboard", timeout=5000)
except:
    page.screenshot(path="failure-screenshot.png")
    raise
```

## Smoke test pattern

Smoke tests verify critical paths work — not every edge case. Target:
1. App loads (200 response, no console errors)
2. Auth flow completes (login → protected page)
3. Core feature works (the main Acceptance Criterion)

## Assertion strategies

| What to assert | How |
|----------------|-----|
| Page loaded | `expect(page).to_have_url(...)` |
| Element visible | `expect(page.locator("...")).to_be_visible()` |
| Text present | `expect(page.locator("...")).to_have_text(...)` |
| No errors | `page.on("console", lambda msg: assert msg.type != "error")` |
| API response | Intercept with `page.route(...)` |

## Rules

- Always run headless (`headless=True`) in CI/automated contexts
- Clean up browser state between tests (new context per test)
- Never modify implementation code to make E2E tests pass
