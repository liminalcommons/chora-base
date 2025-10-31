# Tutorial: Debugging CI Failures

**Difficulty**: Beginner to Intermediate
**Time**: 30-45 minutes
**Prerequisites**: Basic Git and pytest knowledge

---

## Introduction

This tutorial teaches you how to systematically debug GitHub Actions workflow failures. You'll learn to interpret error messages, reproduce failures locally, and fix common issues.

### What You'll Learn

- How to read GitHub Actions logs
- Common failure patterns and their solutions
- Reproducing CI failures on your local machine
- Using debugging tools effectively

---

## Part 1: Understanding the Failure

### Step 1: Navigate to the Failed Workflow

1. Go to your GitHub repository
2. Click the **Actions** tab
3. Find the red ❌ next to your commit
4. Click on the failing workflow run

**What you see**:
```
Test / test (3.11) ❌
Test / test (3.12) ✅
Test / test (3.13) ✅
Lint ✅
```

**Analysis**: Tests fail on Python 3.11 but pass on 3.12 and 3.13. This suggests a Python version-specific issue.

### Step 2: Read the Error Message

Click on the failed job → Expand the failing step

**Example error**:
```
=================================== FAILURES ===================================
____________________________ test_email_validation _____________________________

    def test_email_validation():
        result = validate_email("invalid.email")
>       assert result == {"valid": False, "error": "Invalid format"}
E       AssertionError: assert {'valid': False} == {'valid': False, 'error': 'Invalid format'}
E         Right contains 2 more items:
E         {'error': 'Invalid format'}

tests/test_validation.py:45: AssertionError
```

**Key information**:
- **Test name**: `test_email_validation`
- **File**: `tests/test_validation.py:45`
- **Issue**: Missing `error` key in result dict
- **Python version**: 3.11 (from job matrix)

---

## Part 2: Reproducing Locally

### Step 3: Set Up Local Environment

```bash
# 1. Ensure correct Python version
python --version
# Output: Python 3.11.5

# If wrong version, use pyenv:
pyenv install 3.11.5
pyenv local 3.11.5

# 2. Install dependencies
pip install -e ".[dev]"

# 3. Run the specific failing test
pytest tests/test_validation.py::test_email_validation -v
```

**Expected output** (reproducing the failure):
```
tests/test_validation.py::test_email_validation FAILED                  [100%]

=================================== FAILURES ===================================
____________________________ test_email_validation _____________________________
...
```

✅ **Success**: You've reproduced the failure locally!

---

## Part 3: Common Failure Patterns

### Pattern 1: Test Failures

**Symptom**:
```
FAILED tests/test_api.py::test_get_user - assert 404 == 200
```

**Debugging steps**:

```bash
# 1. Run the test with verbose output
pytest tests/test_api.py::test_get_user -v

# 2. Add print debugging
# In tests/test_api.py:
def test_get_user():
    response = client.get("/users/1")
    print(f"Response: {response.status_code}, {response.json()}")  # Debug
    assert response.status_code == 200

# 3. Run again
pytest tests/test_api.py::test_get_user -s  # -s shows print output

# Output: Response: 404, {'error': 'User not found'}
```

**Common causes**:
- Database not seeded with test data
- Mock not configured correctly
- API endpoint changed but test not updated

**Fix example**:
```python
# tests/test_api.py
def test_get_user(db_session):
    # Seed test user
    user = User(id=1, name="Test User")
    db_session.add(user)
    db_session.commit()

    response = client.get("/users/1")
    assert response.status_code == 200
```

---

### Pattern 2: Coverage Failures

**Symptom**:
```
FAILED coverage: total coverage (78.00%) is below 85%

Missing lines:
src/myproject/api.py: 45-52, 67-70
src/myproject/validation.py: 123-125
```

**Debugging steps**:

```bash
# 1. Generate HTML coverage report
pytest --cov=src --cov-report=html

# 2. Open in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux

# 3. Click on red/yellow files to see uncovered lines
```

**What the report shows**:
- **Green lines**: Covered by tests
- **Red lines**: Not covered (need tests)
- **Yellow lines**: Partially covered (e.g., branch not tested)

**Fix**: Write tests for uncovered code:

```python
# tests/test_api.py
def test_api_error_handling():
    """Test previously uncovered error paths (lines 45-52)"""
    response = client.post("/users", json={"name": ""})  # Invalid data
    assert response.status_code == 400  # Error handling now covered
```

---

### Pattern 3: Lint Failures

**Symptom**:
```
ruff check .
src/myproject/api.py:45:1: E501 Line too long (105 > 100 characters)
src/myproject/api.py:67:5: F401 'typing.Optional' imported but unused
```

**Auto-fix**:
```bash
# Fix most issues automatically
ruff check --fix .

# Check what's left
ruff check .
```

**Manual fixes**:
```python
# Before (line too long)
def create_user(name: str, email: str, address: str, phone: str, preferences: dict) -> User:

# After (use black-style formatting)
def create_user(
    name: str,
    email: str,
    address: str,
    phone: str,
    preferences: dict,
) -> User:

# Before (unused import)
from typing import Optional, List  # Optional unused

# After
from typing import List
```

---

### Pattern 4: Type Checking Failures

**Symptom**:
```
mypy src
src/myproject/api.py:78: error: Argument 1 to "validate" has incompatible type "str"; expected "int"
```

**Debugging**:

```python
# src/myproject/api.py:78
user_id = request.args.get("id")  # Returns str
validate(user_id)  # Expects int

# Fix: Convert type
user_id = int(request.args.get("id"))
validate(user_id)  # Now correct

# Or: Update type hint
def validate(user_id: str | int) -> bool:  # Accept both
    if isinstance(user_id, str):
        user_id = int(user_id)
    return user_id > 0
```

---

### Pattern 5: Dependency Failures

**Symptom**:
```
ERROR: Could not find a version that satisfies the requirement httpx>=0.25.0
```

**Common causes**:
- Package not available for Python version
- Typo in package name
- Version conflict with existing dependencies

**Fix**:

```bash
# 1. Check package exists
pip search httpx  # Or visit PyPI

# 2. Check Python version compatibility
# Visit https://pypi.org/project/httpx/#files
# Ensure wheels exist for Python 3.11, 3.12, 3.13

# 3. Resolve version conflict
pip install httpx==0.24.0  # Try older version
# Or update conflicting package
```

---

## Part 4: Advanced Debugging

### Using pytest Debugging Features

**1. Drop into debugger on failure**:
```bash
pytest --pdb tests/test_api.py::test_get_user
```

When test fails, you'll get a `(Pdb)` prompt:
```python
(Pdb) response.status_code
404
(Pdb) response.json()
{'error': 'User not found'}
(Pdb) db_session.query(User).all()
[]  # Empty! Missing test data
```

**2. Print detailed assertion info**:
```bash
pytest --tb=long tests/test_api.py::test_get_user
```

**3. Show local variables on failure**:
```bash
pytest --showlocals tests/test_api.py::test_get_user
```

Output includes all local variables:
```
test_api.py:45: AssertionError
-------------------------------- Captured locals ---------------------------------
response = <Response 404>
user_id = 1
expected_name = "Test User"
```

---

### Debugging Platform-Specific Failures

**Scenario**: Tests pass on macOS locally but fail on Linux CI

**Common causes**:

**1. Path separators**:
```python
# Wrong (macOS-specific)
path = "data/users/1.json"

# Right (cross-platform)
from pathlib import Path
path = Path("data") / "users" / "1.json"
```

**2. Case-sensitive filesystems**:
```python
# Fails on Linux (case-sensitive)
with open("Data/users.json") as f:  # "Data" != "data"

# Fix: Use consistent casing
with open("data/users.json") as f:
```

**3. Line endings**:
```python
# Configure git to normalize line endings
# In .gitattributes:
* text=auto
*.py text eol=lf
```

---

## Part 5: Preventing Future Failures

### Pre-Push Checks

Create `.git/hooks/pre-push`:
```bash
#!/bin/bash
# Run CI checks locally before pushing

echo "Running pre-push checks..."

# Lint
ruff check . || exit 1

# Type check
mypy src || exit 1

# Tests
pytest --cov=src --cov-fail-under=85 || exit 1

echo "✅ All checks passed!"
```

Make executable:
```bash
chmod +x .git/hooks/pre-push
```

### IDE Integration

**VS Code** (`.vscode/settings.json`):
```json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false
}
```

**PyCharm**:
- Settings → Tools → Python Integrated Tools → Testing → pytest
- Settings → Tools → External Tools → Add `ruff check`

---

## Summary Checklist

When a CI workflow fails:

1. **Identify failure type**
   - [ ] Test failure
   - [ ] Coverage failure
   - [ ] Lint failure
   - [ ] Type check failure
   - [ ] Dependency issue

2. **Reproduce locally**
   - [ ] Correct Python version
   - [ ] Run exact failing command
   - [ ] Failure reproduced

3. **Debug**
   - [ ] Read error message carefully
   - [ ] Use pytest debugging features
   - [ ] Add print/log statements if needed

4. **Fix and verify**
   - [ ] Fix implemented
   - [ ] Tests pass locally
   - [ ] Coverage ≥ 85% locally
   - [ ] Lint passes locally

5. **Push and monitor**
   - [ ] Commit fix
   - [ ] Push to GitHub
   - [ ] Monitor workflow re-run
   - [ ] Verify green checkmark ✅

---

## Related Documentation

- [GitHub Actions Guide](../guides/github-actions.md) - Understanding workflows
- [Customizing Workflows](customizing-workflows.md) - Advanced workflow customization
- [SAP-005: CI/CD Workflows](../../skilled-awareness/ci-cd-workflows/) - Technical specifications
- [SAP-004: Testing Framework](../../skilled-awareness/testing-framework/) - Test patterns

---

**Last Updated**: 2025-10-29
**Version**: 1.0.0
