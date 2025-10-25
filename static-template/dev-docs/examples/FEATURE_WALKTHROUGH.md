---
title: Complete Feature Walkthrough Example
category: examples
audience: human-developers, ai-agents
lifecycle_phase: all-phases
created: 2025-10-25
updated: 2025-10-25
---

# Complete Feature Walkthrough: User Authentication with OAuth2

**Purpose**: Demonstrate the complete 8-phase development lifecycle using a real-world example.

**Feature**: Add OAuth2 authentication (Google + GitHub providers) to a web application

**Timeline**: 14 days (2 sprints across Phases 1-8)

**Outcome**: Production deployment with ≥90% test coverage, zero critical bugs, 89% user satisfaction

---

## Overview

This walkthrough shows the **complete end-to-end process** from vision to monitoring, following the chora-base development framework:

**Phases Covered**:
1. Vision & Strategy (Strategic alignment)
2. Planning & Prioritization (Sprint planning)
3. Requirements & Design (DDD workflow)
4. Development (BDD/TDD workflow)
5. Testing & Quality (Integration testing)
6. Review & Integration (Code review, CI/CD)
7. Release & Deployment (Production release)
8. Monitoring & Feedback (Metrics, iteration)

**Evidence-Based Results**:
- **DDD** saved 8 hours of rework (designed API before coding)
- **BDD** prevented 3 acceptance issues (scenarios defined upfront)
- **TDD** resulted in 94% test coverage, 0 production bugs
- **Process metrics** tracked throughout (sprint velocity 86%, cycle time 2.5 days)

---

## Phase 1: Vision & Strategy (Months → Strategic Context)

### Background

**Product Roadmap** (Q1 2025):

```markdown
## Q1 2025 Strategic Priorities

**Theme**: User Experience & Security

**Committed Capabilities**:
1. User Authentication (Wave 1)
   - OAuth2 login (Google, GitHub)
   - Session management
   - User profile system

2. Analytics Dashboard (Wave 1)
   - Daily active users
   - User session tracking

**Future Vision** (Wave 2, Q2 2025):
- Multi-factor authentication
- Single sign-on (SSO)
- Role-based access control (RBAC)
```

**Strategic Decision**: OAuth2 authentication is Wave 1 (committed work), not Wave 2 (future vision)

### Ecosystem Alignment

**Related Projects**:
- `chora-platform` needs consistent auth across all services
- `mcp-n8n` will integrate with OAuth2 API
- `chora-compose` will use same authentication pattern

**Design Constraint**: Use standard OAuth2 flow (enables ecosystem interoperability)

### Market Research

**User Feedback** (from last quarter):
- 78% of users requested "Sign in with Google"
- 52% of users requested "Sign in with GitHub"
- Security audit recommended OAuth2 over custom auth

**Competitive Analysis**:
- Industry standard: OAuth2 + JWT tokens
- Average implementation time: 2-4 weeks
- Typical bugs: Token refresh, CSRF protection

---

## Phase 2: Planning & Prioritization (2 Weeks)

### Sprint Planning (Sprint 5)

**Sprint Goal**: Complete OAuth2 authentication feature

**Sprint Duration**: 2025-02-01 → 2025-02-14 (2 weeks)

**Sprint Template**: [project-docs/sprints/sprint-5.md](../../project-docs/sprints/sprint-5.md)

### User Stories & Prioritization

**High Priority (Must Have)**:

#### Story 1: OAuth2 Login Flow

**As a** user
**I want** to sign in with Google or GitHub
**So that** I don't need to create another password

**Acceptance Criteria**:
- [ ] User can click "Sign in with Google" button
- [ ] User is redirected to Google OAuth consent screen
- [ ] User is redirected back with access token
- [ ] User session is created and persisted
- [ ] Same flow works for GitHub

**Effort Estimate**: 14 hours
- DDD: 3 hours
- BDD: 2 hours
- TDD: 6 hours
- Review: 1 hour
- Docs: 2 hours

**Priority**: P0 (Blocker for analytics dashboard)

---

#### Story 2: User Profile Management

**As a** user
**I want** to view my profile information
**So that** I can verify my account details

**Acceptance Criteria**:
- [ ] User can access `/profile` endpoint
- [ ] Profile shows name, email, avatar from OAuth provider
- [ ] User can log out

**Effort Estimate**: 8 hours
- DDD: 2 hours
- BDD: 1 hour
- TDD: 4 hours
- Review: 0.5 hours
- Docs: 0.5 hours

**Priority**: P0

---

#### Story 3: Session Management

**As a** system
**I want** to manage user sessions securely
**So that** users remain authenticated across requests

**Acceptance Criteria**:
- [ ] Sessions expire after 24 hours
- [ ] Sessions are stored server-side (Redis)
- [ ] Session IDs are cryptographically secure
- [ ] CSRF protection implemented

**Effort Estimate**: 10 hours
- DDD: 2 hours
- BDD: 2 hours
- TDD: 5 hours
- Review: 0.5 hours
- Docs: 0.5 hours

**Priority**: P0

---

**Medium Priority (Should Have)**:

#### Story 4: Error Handling

**Effort Estimate**: 6 hours
**Priority**: P1

---

### Capacity Planning

**Team**:
- Alice (Developer): 80 hours → 64 committed (80%)
- Bob (AI Agent): 80 hours → 64 committed (80%)
- **Total**: 128 committed hours

**Story Allocation**:
| Priority | Stories | Hours | % Capacity |
|----------|---------|-------|------------|
| Must Have | 3 | 32 | 50% |
| Should Have | 1 | 6 | 9% |
| Tech Debt | Refactoring | 10 | 16% |
| Buffer | Unknowns | 16 | 25% |
| **Total** | **5** | **64** | **100%** |

**Capacity Health**: ✅ Green (75% committed, 25% buffer)

### Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| OAuth provider API changes | Low | High | Use official SDKs, version lock |
| Session storage complexity | Medium | Medium | Spike Redis integration (2 hours) |
| CSRF attack vectors | Low | Critical | Security review before merge |

---

## Phase 3: Requirements & Design (DDD Workflow, Day 1-2)

### Step 1: Understand the Need (Day 1, 9:00-10:00 AM)

**Change Request**:

```markdown
# Feature Request: OAuth2 Authentication

## Problem Statement

Users currently authenticate with username/password, which is:
- **Insecure**: Password reuse across sites
- **Inconvenient**: Another password to remember
- **Support burden**: "Forgot password" requests

## Proposed Solution

Implement OAuth2 authentication with Google and GitHub providers:
- Standard OAuth2 flow (authorization code grant)
- JWT tokens for session management
- Secure token storage (HttpOnly cookies)

## Alignment

- Roadmap: Wave 1 committed work ✅
- Security audit: Recommended approach ✅
- User feedback: 78% requested Google login ✅
```

**Questions Answered**:
- Why OAuth2? (Industry standard, user-requested, secure)
- Which providers? (Google + GitHub, per user feedback)
- How to store tokens? (HttpOnly cookies, CSRF-protected)

---

### Step 2: Define Acceptance Criteria (Day 1, 10:00-11:00 AM)

**Functional Criteria**:
- User can sign in with Google OAuth2
- User can sign in with GitHub OAuth2
- User session persists for 24 hours
- User can log out
- User can view profile

**Non-Functional Criteria**:
- Response time <200ms for auth check
- Test coverage ≥90%
- Security: CSRF protection, secure token storage
- Error messages: Clear, actionable

**Edge Cases**:
- OAuth provider returns error → Show user-friendly error
- Token expires → Redirect to login
- Concurrent login attempts → Last wins (overwrite session)

---

### Step 3: Design the API (Day 1, 11:00 AM - Day 2, 1:00 PM)

**API Reference Documentation** (Written FIRST, before code):

```markdown
## auth.login()

**Canonical Name:** `login`
**Category:** Authentication
**Status:** ✅ Stable

### Signature

```python
async def login(
    provider: Literal["google", "github"],
    redirect_uri: str,
) -> AuthorizationURL:
    """Initiate OAuth2 login flow.

    Args:
        provider: OAuth provider ('google' or 'github')
        redirect_uri: URL to redirect after successful auth

    Returns:
        AuthorizationURL with 'url' to redirect user

    Raises:
        ValueError: If provider not supported
        ConfigurationError: If provider credentials not configured

    Examples:
        >>> auth_url = await login(provider="google", redirect_uri="https://example.com/callback")
        >>> print(auth_url.url)
        'https://accounts.google.com/o/oauth2/v2/auth?client_id=...'
    """
```

### Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `provider` | `Literal["google", "github"]` | Yes | N/A | OAuth provider to use |
| `redirect_uri` | `str` | Yes | N/A | Callback URL after authentication |

### Returns

| Type | Description |
|------|-------------|
| `AuthorizationURL` | Object with `url` field containing OAuth provider URL |

### Errors

| Error | Condition | HTTP Status |
|-------|-----------|-------------|
| `ValueError` | Unsupported provider | 400 |
| `ConfigurationError` | Missing OAuth credentials | 500 |

### Security

- CSRF state parameter included in URL
- State validated on callback
- Redirect URI must match registered URIs

### Performance

- Cold start: <50ms (URL generation only)
- No database queries

### Examples

**Basic Usage:**
```python
# Initiate Google login
auth_url = await login(provider="google", redirect_uri="https://app.com/callback")
# Redirect user to auth_url.url
```

**Error Handling:**
```python
try:
    auth_url = await login(provider="invalid", redirect_uri="https://app.com/callback")
except ValueError as e:
    print(f"Invalid provider: {e}")
```
```

**Complete API Designed** (Day 2, 1:00 PM):
- `login()` - Initiate OAuth flow
- `callback()` - Handle OAuth callback
- `get_profile()` - Retrieve user profile
- `logout()` - End user session
- `check_auth()` - Verify authentication

**DDD Investment**: 3 hours
**DDD Outcome**: Clear API contract before writing any code

---

### Step 4: Document Examples & Edge Cases (Day 2, 1:00-2:00 PM)

**Example Scenarios**:

```gherkin
Scenario: User signs in with Google (happy path)
  Given user is on login page
  When user clicks "Sign in with Google"
  Then user is redirected to Google OAuth consent screen
  And user approves permissions
  And user is redirected back to app
  And user session is created
  And user sees "Welcome, [Name]"

Scenario: OAuth provider returns error
  Given user is on login page
  When user clicks "Sign in with Google"
  And Google returns "access_denied" error
  Then user sees "Authentication cancelled. Please try again."
  And user remains on login page

Scenario: Token expired during session
  Given user is authenticated
  And user session has expired (24 hours passed)
  When user accesses protected resource
  Then user is redirected to login page
  And user sees "Session expired. Please sign in again."
```

---

### Step 5: Review & Validate (Day 2, 2:00-3:00 PM)

**Review Checklist**:
- [x] API design aligns with OAuth2 standard
- [x] All acceptance criteria addressed
- [x] Edge cases documented
- [x] Security considerations included
- [x] Performance targets defined

**Stakeholder Approval**:
- Product Owner: ✅ Approved
- Security Lead: ✅ Approved (pending CSRF review in code)
- Engineering Lead: ✅ Approved

**DDD Phase Complete**: Proceed to Phase 4 (BDD/TDD)

---

## Phase 4: Development (BDD/TDD Workflow, Day 3-8)

### BDD Phase (Day 3, 9:00 AM - 12:00 PM)

**Step 1: Write Feature File**

`features/auth.feature`:
```gherkin
Feature: OAuth2 Authentication
  As a user
  I want to sign in with Google or GitHub
  So that I don't need another password

  Scenario: User signs in with Google
    Given the OAuth provider is configured
    When I request login with provider "google"
    Then I receive an authorization URL
    And the URL contains "accounts.google.com"
    And the URL contains a CSRF state parameter

  Scenario: User completes OAuth callback
    Given I have initiated login with provider "google"
    And the OAuth provider returns a valid code
    When I submit the callback with code and state
    Then a user session is created
    And I receive a session token
    And the token is HttpOnly

  Scenario: User signs in with invalid provider
    When I request login with provider "invalid"
    Then I receive an error "Unsupported provider"
    And the HTTP status is 400
```

**Step 2: Implement Step Definitions**

`tests/bdd/step_defs/test_auth.py`:
```python
from pytest_bdd import scenario, given, when, then, parsers
import pytest

@scenario('../features/auth.feature', 'User signs in with Google')
def test_google_login():
    pass

@given('the OAuth provider is configured')
def oauth_configured(monkeypatch):
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "test_client_id")
    monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "test_client_secret")

@when(parsers.parse('I request login with provider "{provider}"'))
def request_login(provider):
    from myapp.auth import login
    pytest.shared_context = {"result": login(provider, "http://localhost/callback")}

@then('I receive an authorization URL')
def check_auth_url():
    result = pytest.shared_context["result"]
    assert "url" in result
    assert result["url"].startswith("http")

@then(parsers.parse('the URL contains "{substring}"'))
def check_url_contains(substring):
    result = pytest.shared_context["result"]
    assert substring in result["url"]
```

**BDD Investment**: 2 hours
**BDD Outcome**: 15 Gherkin scenarios, all failing (RED state)

---

### TDD Phase (Day 3, 2:00 PM - Day 7, 5:00 PM)

**Feature 1: OAuth Login Flow** (Day 3-5, 18 hours)

#### Iteration 1: `login()` function (Day 3, 2:00-4:00 PM)

**RED** (Write failing test):
```python
# tests/test_auth.py
def test_login_returns_google_url():
    result = login(provider="google", redirect_uri="http://localhost/callback")
    assert "accounts.google.com" in result["url"]
    assert "client_id" in result["url"]
    assert "state" in result["url"]
```

**Run**: `pytest tests/test_auth.py::test_login_returns_google_url`
**Result**: `FAILED - ImportError: cannot import name 'login'`

**GREEN** (Minimal implementation):
```python
# src/myapp/auth.py
import secrets
from urllib.parse import urlencode

def login(provider: str, redirect_uri: str) -> dict:
    """Initiate OAuth2 login flow."""
    if provider == "google":
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        state = secrets.token_urlsafe(32)

        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
        }

        url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
        return {"url": url, "state": state}

    raise ValueError(f"Unsupported provider: {provider}")
```

**Run**: `pytest tests/test_auth.py::test_login_returns_google_url`
**Result**: `PASSED ✓`

**REFACTOR** (Improve design):
```python
# Extract provider config to separate module
# Add type hints
# Add docstring (from DDD API reference)

from typing import Literal
from myapp.config import OAuthConfig

def login(
    provider: Literal["google", "github"],
    redirect_uri: str,
) -> dict:
    """Initiate OAuth2 login flow.

    [Full docstring from DDD phase]
    """
    config = OAuthConfig.get(provider)
    state = secrets.token_urlsafe(32)

    params = {
        "client_id": config.client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": config.scope,
        "state": state,
    }

    url = f"{config.auth_url}?{urlencode(params)}"
    return {"url": url, "state": state}
```

**Run**: `pytest tests/test_auth.py`
**Result**: `PASSED ✓`

---

#### Iteration 2: GitHub provider support (Day 4, 9:00-11:00 AM)

**RED**:
```python
def test_login_returns_github_url():
    result = login(provider="github", redirect_uri="http://localhost/callback")
    assert "github.com/login/oauth" in result["url"]
```

**Run**: `pytest tests/test_auth.py::test_login_returns_github_url`
**Result**: `FAILED - ValueError: Unsupported provider: github`

**GREEN**:
```python
# Add GitHub to OAuthConfig
class OAuthConfig:
    PROVIDERS = {
        "google": {...},
        "github": {
            "auth_url": "https://github.com/login/oauth/authorize",
            "token_url": "https://github.com/login/oauth/access_token",
            "scope": "user:email",
        },
    }
```

**Run**: `pytest tests/test_auth.py::test_login_returns_github_url`
**Result**: `PASSED ✓`

**REFACTOR**: (Already clean, no changes needed)

---

#### Iteration 3-10: Remaining functions (Day 4-7)

[Similar RED-GREEN-REFACTOR cycles for:]
- `callback()` - Handle OAuth callback (6 iterations, Day 4-5)
- `get_profile()` - Retrieve user profile (3 iterations, Day 6)
- `logout()` - End session (2 iterations, Day 7 AM)
- `check_auth()` - Verify authentication (3 iterations, Day 7 PM)

**TDD Investment**: 24 hours
**TDD Outcome**: 42 unit tests, 94% coverage, all GREEN ✓

---

### Integration Testing (Day 8, 9:00 AM - 3:00 PM)

**Test OAuth Flow End-to-End**:

```python
# tests/integration/test_auth_flow.py
@pytest.mark.integration
async def test_complete_oauth_flow():
    """Test complete OAuth flow with mock provider."""
    # 1. Initiate login
    auth_url_response = await login(provider="google", redirect_uri="http://localhost/callback")
    assert "url" in auth_url_response
    state = auth_url_response["state"]

    # 2. Simulate OAuth provider callback
    mock_code = "mock_auth_code_123"
    callback_response = await callback(code=mock_code, state=state)
    assert "session_token" in callback_response

    # 3. Verify session created
    token = callback_response["session_token"]
    profile = await get_profile(token=token)
    assert profile["email"] == "test@example.com"

    # 4. Logout
    logout_response = await logout(token=token)
    assert logout_response["success"] is True

    # 5. Verify session destroyed
    with pytest.raises(Unauthorized):
        await get_profile(token=token)
```

**Integration Test Results**:
- 8 integration tests written
- 8 integration tests passing ✓
- E2E flow validated

---

## Phase 5: Testing & Quality (Day 9, 9:00 AM - 5:00 PM)

### Test Coverage Analysis

**Run Coverage Report**:
```bash
pytest --cov=src/myapp/auth --cov-report=term-missing

----------- coverage: platform darwin, python 3.11.1 -----------
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
src/myapp/auth.py          85      5    94%   142-145
src/myapp/config.py        22      0   100%
src/myapp/session.py       48      3    94%   78-80
-----------------------------------------------------
TOTAL                     155      8    95%
```

**Coverage Target**: ≥90% ✅ PASSED (95% actual)

**Missing Coverage Analysis**:
- Lines 142-145: Error handling for invalid OAuth response (edge case)
- Lines 78-80: Session cleanup task (background process)

**Decision**: Acceptable (edge cases + background tasks, no critical paths)

---

### Security Review

**Security Checklist**:
- [x] CSRF protection: State parameter validated on callback
- [x] Token storage: HttpOnly cookies (prevents XSS)
- [x] Session expiry: 24-hour timeout implemented
- [x] Redirect URI validation: Whitelist enforced
- [x] Secrets management: Environment variables, not hardcoded
- [x] SQL injection: Using ORM (no raw SQL)
- [x] Dependency vulnerabilities: `pip-audit` passing

**Security Scan**: `bandit -r src/`
```
Run started: 2025-02-09 14:30:00
Test results:
  No issues identified.

Code scanned:
  Total lines of code: 155
  Total lines skipped (#nosec): 0

Run metrics:
  Total issues (by severity):
    Undefined: 0
    Low: 0
    Medium: 0
    High: 0
  Total issues (by confidence):
    Undefined: 0
    Low: 0
    Medium: 0
    High: 0
```

**Security Review**: ✅ PASSED (0 issues)

---

### Performance Testing

**Load Test Script**:
```python
# tests/performance/test_auth_performance.py
import pytest
import asyncio
import time

@pytest.mark.performance
async def test_auth_check_performance():
    """Verify auth check <200ms (95th percentile)."""

    # Create session
    token = await create_test_session()

    # Run 100 auth checks
    times = []
    for _ in range(100):
        start = time.perf_counter()
        await check_auth(token=token)
        elapsed = (time.perf_counter() - start) * 1000  # Convert to ms
        times.append(elapsed)

    # Calculate p95
    times.sorted()
    p95 = times[94]  # 95th percentile

    assert p95 < 200, f"p95 auth check time {p95:.2f}ms exceeds 200ms target"
```

**Performance Results**:
```
Test: test_auth_check_performance
Results:
  p50: 12ms
  p95: 18ms
  p99: 25ms

Target: <200ms (p95)
Status: ✅ PASSED (18ms vs 200ms target, 91% faster)
```

**Performance**: ✅ PASSED (All benchmarks met)

---

### Quality Gates Summary

| Gate | Target | Actual | Status |
|------|--------|--------|--------|
| **Unit Tests** | 100% pass | 42/42 pass | ✅ |
| **Integration Tests** | 100% pass | 8/8 pass | ✅ |
| **Test Coverage** | ≥90% | 95% | ✅ |
| **Security Scan** | 0 high/critical | 0 issues | ✅ |
| **Performance (p95)** | <200ms | 18ms | ✅ |
| **Linting** | 0 errors | 0 errors | ✅ |
| **Type Checking** | 100% typed | 100% typed | ✅ |

**Phase 5 Complete**: All quality gates PASSED ✅

---

## Phase 6: Review & Integration (Day 10, 9:00 AM - 3:00 PM)

### Code Review Process

**Pull Request Created**: `PR #142: feat(auth): Add OAuth2 authentication`

**PR Description**:
```markdown
## Summary

Implements OAuth2 authentication with Google and GitHub providers.

## Changes

- Add `auth.py` module with login flow
- Add session management with Redis
- Add user profile endpoints
- Add comprehensive test suite (95% coverage)
- Add API documentation

## Testing

- [x] 42 unit tests (all passing)
- [x] 8 integration tests (all passing)
- [x] Security scan (0 issues)
- [x] Performance test (18ms p95, target: <200ms)

## Checklist

- [x] Tests added/updated
- [x] Documentation updated
- [x] CHANGELOG.md entry added
- [x] All CI checks passing
```

---

### Code Review Feedback

**Reviewer**: Engineering Lead

**Feedback**:

1. **Comment on `auth.py:45`**:
   ```python
   # TODO: Add token refresh logic
   ```
   **Feedback**: "Remove TODO or create follow-up issue. Don't ship TODOs to production."

   **Resolution**: Created issue #143 "Add OAuth token refresh", removed TODO comment

2. **Comment on `session.py:78`**:
   ```python
   await redis.setex(f"session:{token}", 86400, user_id)
   ```
   **Feedback**: "Magic number 86400. Use named constant SESSION_EXPIRY_SECONDS."

   **Resolution**: ✅ Fixed
   ```python
   SESSION_EXPIRY_SECONDS = 86400  # 24 hours
   await redis.setex(f"session:{token}", SESSION_EXPIRY_SECONDS, user_id)
   ```

3. **Comment on error handling**:
   **Feedback**: "Excellent error messages with clear next steps. Well done!"

**Review Time**: 1.5 hours
**Changes Requested**: 2 (both addressed)
**Re-review**: ✅ APPROVED

---

### CI/CD Pipeline

**GitHub Actions Workflow**:
```yaml
name: Test & Lint

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -e ".[dev]"
      - run: pytest --cov=src --cov-report=xml
      - run: ruff check src/
      - run: mypy src/
      - run: bandit -r src/
```

**CI Results (PR #142)**:
```
✅ Test (Python 3.11): 50/50 tests passed (2m 15s)
✅ Lint: 0 errors (15s)
✅ Type Check: 100% coverage (22s)
✅ Security Scan: 0 issues (18s)
✅ Coverage: 95% (target: 90%)
```

**CI/CD**: ✅ ALL CHECKS PASSED

---

### Merge to Main

**Merge Strategy**: Squash and merge

**Final Commit**:
```
feat(auth): Add OAuth2 authentication

Implements OAuth2 login with Google and GitHub providers.

Features:
- OAuth2 authorization code flow
- Session management (Redis)
- User profile endpoints
- CSRF protection
- Token security (HttpOnly cookies)

Testing:
- 95% test coverage
- 0 security issues
- 18ms p95 auth check (target: <200ms)

Closes #128

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Merged**: Day 10, 3:00 PM

**Sprint Progress**:
- Story Points Completed: 32/37 (86%)
- Stories Completed: 3/4 (OAuth complete, error handling deferred to Sprint 6)
- Sprint Velocity: 86% ✅

---

## Phase 7: Release & Deployment (Day 11-14)

### Release Planning

**Release Version**: v1.6.0 (MINOR - new feature, backward compatible)

**Release Template**: [project-docs/releases/release-v1.6.0.md](../../project-docs/releases/release-v1.6.0.md)

**Release Scope**:
- OAuth2 authentication (Sprint 5)
- Analytics dashboard (Sprint 6, from Story 2)
- Performance improvements (Sprint 6)

---

### Release Candidate Testing (Day 11-13)

**RC1 Deployed to Staging** (Day 11, 10:00 AM):
```bash
# Tag RC1
git tag v1.6.0-rc.1
git push origin v1.6.0-rc.1

# Deploy to staging
just deploy-staging

# Run smoke tests
just test-smoke-staging
```

**RC Testing Plan** (Day 11-13):

1. **Automated Tests** (Day 11, 2 hours):
   - Full test suite on staging ✅
   - Performance benchmarks ✅
   - Security scan ✅

2. **Manual Testing** (Day 11-12, 1 day):
   - Test Google OAuth flow: ✅ Works
   - Test GitHub OAuth flow: ✅ Works
   - Test error scenarios: ✅ Handled correctly
   - Cross-browser testing: ✅ Chrome, Firefox, Safari

3. **UAT** (Day 12-13, 2 days):
   - Product owner testing: ✅ Approved
   - Beta user testing (5 users): ✅ 5/5 successful logins
   - Feedback: "Much easier than creating another password!"

4. **Go/No-Go Meeting** (Day 13, 3:00 PM):
   - All tests passing: ✅
   - Stakeholder approval: ✅
   - **DECISION**: 🚀 GO FOR PRODUCTION

---

### Production Deployment (Day 14, 10:00 AM)

**Pre-Deployment Checklist**:
- [x] RC testing completed
- [x] Go/No-Go approval obtained
- [x] Deployment window scheduled (Tuesday, 10 AM)
- [x] On-call team notified
- [x] Rollback plan reviewed

**Deployment Steps**:

```bash
# 1. Tag final release (5 min)
git tag v1.6.0
git push origin v1.6.0

# 2. Create GitHub release (5 min)
gh release create v1.6.0 \
  --title "v1.6.0 - OAuth2 Authentication" \
  --notes-file project-docs/releases/release-v1.6.0-notes.md

# 3. Build artifacts (15 min)
just build-package
just publish-package  # PyPI

# 4. Deploy to production (20 min)
just deploy-production

# 5. Run smoke tests (5 min)
just test-smoke-production
# Result: ✅ ALL PASSED

# 6. Verify deployment (5 min)
just verify-production
# Result: ✅ Healthy
```

**Deployment Time**: 55 minutes (target: <60 min) ✅

**Downtime**: 0 minutes (blue-green deployment) ✅

---

### Post-Deployment Monitoring (Day 14, 11:00 AM - 5:00 PM)

**First Hour Monitoring**:

```markdown
## Production Health (v1.6.0) - 11:00 AM - 12:00 PM

| Metric | Baseline | Current | Alert Threshold | Status |
|--------|----------|---------|-----------------|--------|
| Error Rate | 0.05% | 0.04% | >0.1% | ✅ |
| Response Time (p95) | 150ms | 145ms | >200ms | ✅ |
| Memory Usage | 480MB | 495MB | >550MB | ✅ |
| CPU Usage | 40% | 43% | >70% | ✅ |
| Active Users | 1,200 | 1,250 | <1,000 | ✅ |
| OAuth Logins | 0/hour | 45/hour | N/A | ✅ New! |

**Status**: ✅ Healthy (All metrics within normal range)
```

**First 6 Hours Summary** (Day 14, 5:00 PM):
- Error rate: 0.04% (stable)
- OAuth logins: 280 successful (0 failures)
- Support tickets: 1 (user question, not bug)
- User feedback: 8 positive comments on social media

**Deployment Status**: ✅ SUCCESS

---

### Release Communication (Day 14, 12:00 PM)

**GitHub Release**:
```markdown
# Release v1.6.0: OAuth2 Authentication

We're excited to announce v1.6.0, featuring OAuth2 authentication!

## Highlights

- ✨ **Sign in with Google**: One-click authentication with your Google account
- ✨ **Sign in with GitHub**: Developers can use their GitHub account
- 🔒 **Enhanced Security**: Industry-standard OAuth2 protocol
- ⚡ **Fast**: <20ms authentication checks (10x faster than password hashing)

## Upgrading

```bash
pip install --upgrade myapp
```

## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete details.

## Questions?

- Documentation: https://docs.example.com/auth
- GitHub Issues: https://github.com/org/myapp/issues
```

**Blog Post**: Published to company blog
**Email**: Sent to 5,000 users
**Social Media**: Posted to Twitter, LinkedIn

---

## Phase 8: Monitoring & Feedback (Day 15-21, 1 Week Post-Release)

### Adoption Metrics (1 Week Post-Release)

**Download/Usage Metrics**:
```markdown
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **OAuth Logins** | 40% of logins | 58% of logins | ✅ (+45% over target) |
| **Google vs GitHub** | 60/40 split | 72/28 split | ✅ (Google preferred) |
| **Upgrade Rate** | 60% | 72% | ✅ |
| **Support Tickets** | <10 | 4 | ✅ |
| **Bug Reports** | <3 | 0 | ✅ |
```

**User Feedback** (1 week):
- Positive feedback: 58 comments
- Negative feedback: 3 comments (2 wanted more providers, 1 UX suggestion)
- Neutral feedback: 5 comments
- **User Satisfaction**: 89% (58/65 positive)

---

### Quality Metrics (1 Week Post-Release)

```markdown
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **Error Rate** | <0.1% | 0.04% | ✅ |
| **Response Time (p95)** | <200ms | 18ms | ✅ |
| **Production Bugs** | <3 | 0 | ✅ |
| **Security Incidents** | 0 | 0 | ✅ |
| **Rollbacks** | 0 | 0 | ✅ |
```

**Defect Analysis**: 0 production bugs in first week ✅

---

### Sprint Metrics Summary

**Sprint 5 Final Metrics**:
```markdown
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **Story Points Completed** | 37 | 32 | 86% ✅ |
| **Test Coverage** | ≥90% | 95% | ✅ |
| **Defects Found** | <3 | 0 | ✅ |
| **Cycle Time (avg)** | <3 days | 2.5 days | ✅ |

**Sprint Rating**: ⭐⭐⭐⭐⭐ (5/5)
```

**Process Adherence**:
```markdown
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **DDD Adherence** | ≥90% | 100% | ✅ |
| **BDD Adherence** | ≥80% | 100% | ✅ |
| **TDD Adherence** | ≥80% | 100% | ✅ |

**ROI**: Saved 8 hours of rework (DDD), prevented 3 acceptance issues (BDD)
```

---

### Release Retrospective (Day 21)

**What Went Well** ✅:
1. **DDD saved 8 hours**: Designed API before coding, zero rework
2. **BDD caught issues early**: 3 acceptance criteria refined before implementation
3. **TDD resulted in zero bugs**: 95% coverage, 0 production defects
4. **RC testing caught edge case**: OAuth error handling improved before production
5. **Smooth deployment**: 55-minute deployment, 0 downtime, 0 rollbacks
6. **Strong user adoption**: 58% of logins using OAuth (vs 40% target)

**What Could Be Improved** ⚠️:
1. **RC testing took 3 days** (target: 2 days)
   - Issue: UAT scheduling delays
   - Solution: Pre-schedule UAT testers 1 week before RC

2. **Deferred Story 4** (error handling improvements)
   - Impact: Minor, not critical path
   - Plan: Completed in Sprint 6

**Lessons Learned**:
1. **DDD/BDD/TDD workflow pays off**: 100% adherence → 0 bugs, 89% user satisfaction
2. **Evidence-based metrics guide decisions**: Sprint velocity 86% (predictable)
3. **Quality gates prevent production issues**: All gates passed → smooth release
4. **User-centered design wins**: 72% chose Google (matched user feedback)

**Action Items for Next Sprint**:
- [ ] Pre-schedule UAT testers 1 week before RC (Owner: PM, Due: Sprint 6 planning)
- [ ] Complete Story 4 (error handling) in Sprint 6 (Owner: Alice, Due: Sprint 6)
- [ ] Add more OAuth providers based on feedback (Owner: Product, Due: Q2 planning)

---

## ROI Analysis

### Time Investment Breakdown

| Phase | Activity | Time Invested | Key Output |
|-------|----------|---------------|------------|
| **Phase 1** | Vision & Strategy | 2 hours | Strategic alignment |
| **Phase 2** | Sprint Planning | 3 hours | Sprint backlog |
| **Phase 3** | DDD (Requirements & Design) | 8 hours | API reference docs |
| **Phase 4** | BDD (Scenarios) | 4 hours | 15 Gherkin scenarios |
| **Phase 4** | TDD (Implementation) | 24 hours | 42 unit tests, 95% coverage |
| **Phase 5** | Testing & Quality | 8 hours | Security scan, performance test |
| **Phase 6** | Code Review & CI/CD | 3 hours | Approved PR, CI passing |
| **Phase 7** | Release & Deployment | 6 hours | Production deployment |
| **Phase 8** | Monitoring & Retrospective | 4 hours | Metrics, lessons learned |
| **Total** | | **62 hours** | |

### Time Savings from Process

**Without DDD/BDD/TDD** (Traditional approach):
- Rework from unclear requirements: 12 hours
- Bugs found in production: 8 hours
- Emergency patches: 6 hours
- Support tickets (bug-related): 4 hours
- **Total waste**: 30 hours

**With DDD/BDD/TDD** (chora-base approach):
- DDD upfront investment: 8 hours
- BDD upfront investment: 4 hours
- Rework: 0 hours (clear API design)
- Production bugs: 0 hours (caught in tests)
- Emergency patches: 0 hours
- Support tickets: 1 hour (user question, not bug)
- **Total waste**: 1 hour

**Net Savings**: 30 - 1 - 12 (DDD/BDD overhead) = **17 hours saved**

**ROI**: 17 hours saved / 62 hours invested = **27% efficiency gain**

---

### Quality Improvements

| Metric | Before DDD/BDD/TDD | After DDD/BDD/TDD | Improvement |
|--------|-------------------|-------------------|-------------|
| **Defects** | 5 bugs/feature (avg) | 0 bugs | 100% reduction |
| **Test Coverage** | 65% (typical) | 95% | +46% |
| **Rework Time** | 12 hours | 0 hours | 100% reduction |
| **User Satisfaction** | 70% (typical) | 89% | +27% |
| **Deployment Success** | 85% (typical) | 100% | +18% |

---

## Key Takeaways

### For Human Developers

1. **DDD saves rework**: 8 hours upfront design → 0 hours rework (vs 12 hours typical)
2. **BDD clarifies expectations**: 15 scenarios → 0 acceptance issues
3. **TDD builds confidence**: 95% coverage → 0 production bugs
4. **Metrics guide decisions**: 86% sprint velocity (predictable planning)
5. **Process discipline pays off**: 100% adherence → 89% user satisfaction

### For AI Agents

**Decision Tree for New Features**:
```
START: New feature requested
    ↓
Q1: Is feature in current sprint?
    NO → Add to backlog, skip to END
    YES → Continue
    ↓
PHASE 3: DDD
    - Write API reference docs (3-8 hours)
    - Get stakeholder approval
    ↓
PHASE 4: BDD
    - Write Gherkin scenarios (2-4 hours)
    - Implement step definitions
    ↓
PHASE 4: TDD
    - RED: Write failing test
    - GREEN: Minimal implementation
    - REFACTOR: Improve design
    - Repeat until BDD scenarios pass
    ↓
PHASE 5: Quality Gates
    - Coverage ≥90%?
    - Security scan 0 issues?
    - Performance targets met?
    - ALL YES → Continue
    - ANY NO → Fix before proceeding
    ↓
PHASE 6: Code Review
    - Create PR with checklist
    - Address feedback
    - CI/CD all green?
    ↓
PHASE 7: Release
    - RC testing (3-7 days)
    - Production deployment
    ↓
PHASE 8: Monitor
    - Track metrics (1 week)
    - Retrospective
    ↓
END: Feature complete
```

**Evidence-Based Targets**:
- DDD time: 3-8 hours per feature (saves 8-15 hours of rework)
- BDD time: 2-4 hours per feature (prevents 2-5 acceptance issues)
- TDD time: 4-24 hours per feature (achieves 90-95% coverage)
- Quality gates: 100% pass rate required (prevents production issues)
- Sprint velocity: 80-90% (predictable, sustainable)

---

## References

**Workflow Documentation**:
- [8-Phase Development Process](../workflows/DEVELOPMENT_PROCESS.md)
- [DDD Workflow](../workflows/DDD_WORKFLOW.md)
- [BDD Workflow](../workflows/BDD_WORKFLOW.md)
- [TDD Workflow](../workflows/TDD_WORKFLOW.md)
- [Development Lifecycle Integration](../workflows/DEVELOPMENT_LIFECYCLE.md)

**Anti-Patterns**:
- [Common Mistakes to Avoid](../ANTI_PATTERNS.md)

**Process Metrics**:
- [KPIs & Measurement](../../project-docs/metrics/PROCESS_METRICS.md)

**Sprint & Release Planning**:
- [Sprint Planning Guide](../../project-docs/sprints/README.md)
- [Release Planning Guide](../../project-docs/releases/RELEASE_PLANNING_GUIDE.md)

---

**Document Version**: 1.0
**Last Updated**: 2025-10-25
**Maintained By**: chora-base v3.0.0
**License**: MIT
