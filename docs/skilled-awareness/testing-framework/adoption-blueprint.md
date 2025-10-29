# Adoption Blueprint: Testing Framework

**SAP ID**: SAP-004
**Version**: 1.0.0
**Status**: Draft (Phase 2)
**Last Updated**: 2025-10-28

---

## 1. Overview

This blueprint guides **developers** (humans and AI agents) through using chora-base's testing framework to write tests, achieve coverage, and maintain quality.

**What You'll Learn**:
- How to run tests
- How to write tests (sync and async)
- How to achieve 85%+ coverage
- How to debug test failures
- How to integrate with CI/CD

**Time Estimate**: 10-20 minutes to learn, 5-10 minutes per test

---

## 2. Prerequisites

### Required Software

- **Python**: 3.11 or later
- **pytest**: 8.3.0 (installed via `pip install -e ".[dev]"`)
- **pytest-asyncio**: 0.24.0 (async test support)
- **pytest-cov**: 6.0.0 (coverage measurement)

### Required Knowledge

- Basic Python testing concepts
- pytest basics (test discovery, assertions)
- Async/await (for async tests)

### Project Setup

- Generated project from chora-base (SAP-003)
- Dependencies installed (`pip install -e ".[dev]"`)
- Tests directory exists (tests/)

---

## 3. Quick Start

### Step 1: Run Existing Tests

```bash
cd my-project
pytest
```

**Expected Output**:
```
======================== test session starts =========================
collected 5 items

tests/utils/test_validation.py .....                           [100%]

========================= 5 passed in 0.23s ==========================
```

**Success**: All tests pass (5/5)

### Step 2: Run Tests with Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

**Expected Output**:
```
---------- coverage: platform linux, python 3.11.0 -----------
Name                          Stmts   Miss  Cover   Missing
-----------------------------------------------------------
src/my_package/__init__.py        5      0   100%
src/my_package/utils/validation.py   50      0   100%
-----------------------------------------------------------
TOTAL                           55      0   100%

========================= 5 passed in 0.34s ==========================
```

**Success**: 100% coverage (example tests cover utils/)

### Step 3: Write Your First Test

**Create tests/test_my_module.py**:
```python
"""Tests for my_package.my_module."""

import pytest
from my_package.my_module import my_function


class TestMyFunction:
    """Tests for my_function."""

    def test_happy_path(self):
        """Test normal operation."""
        result = my_function("input")
        assert result == "expected output"

    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError, match="error message"):
            my_function(None)
```

**Run your test**:
```bash
pytest tests/test_my_module.py -v
```

**Success**: Your test passes

---

## 4. Writing Tests

### 4.1 Basic Test Structure

```python
"""Tests for module_name.

Description of what this module tests.
"""

import pytest
from my_package.module import function_to_test


class TestFunctionName:
    """Tests for function_name."""

    def test_descriptive_name(self):
        """Describe what this test verifies."""
        # Arrange: Set up test data
        input_data = "test input"

        # Act: Call function
        result = function_to_test(input_data)

        # Assert: Verify result
        assert result == "expected"
```

### 4.2 Async Tests

```python
async def test_async_function():
    """Test async operation."""
    result = await async_function()
    assert result == "expected"
```

**Note**: No special setup needed - pytest-asyncio handles it automatically.

### 4.3 Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
])
def test_multiple_inputs(input, expected):
    """Test multiple inputs."""
    assert function(input) == expected
```

### 4.4 Error Testing

```python
def test_error_handling():
    """Test that invalid input raises ValueError."""
    with pytest.raises(ValueError, match="expected error"):
        function_that_should_fail(None)
```

### 4.5 Fixtures

```python
@pytest.fixture
def sample_data():
    """Provide sample data."""
    return {"key": "value"}


def test_with_fixture(sample_data):
    """Test using fixture."""
    assert sample_data["key"] == "value"
```

---

## 5. Achieving Coverage

### 5.1 Check Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

**Interpret Output**:
```
Name                    Stmts   Miss  Cover   Missing
---------------------------------------------------
src/my_package/module.py   50      8    84%   45-51, 67
```

- **Stmts**: Total lines of code
- **Miss**: Lines not executed
- **Cover**: Percentage covered (84%)
- **Missing**: Line numbers not covered (45-51, 67)

**Target**: ≥85% coverage

### 5.2 Increase Coverage

**Steps**:
1. Identify missing lines (from coverage report)
2. Determine what triggers those lines
3. Write test for that scenario
4. Re-run coverage

**Example**:
```python
# In src/my_package/module.py, lines 45-51 are uncovered:
def process_data(input: str, validate: bool = False):
    if validate:  # Line 45
        if not input:  # Line 46
            raise ValueError("Input required")  # Line 47
        # ... more validation (lines 48-51)
    return input.upper()

# Write test to cover lines 45-51:
def test_validation_error():
    """Test validation with empty input."""
    with pytest.raises(ValueError, match="Input required"):
        process_data("", validate=True)  # Triggers lines 45-47
```

### 5.3 Coverage Best Practices

**DO**:
- ✅ Test all public functions
- ✅ Test both happy path and error paths
- ✅ Test edge cases (empty input, None, etc.)
- ✅ Aim for 85-90% coverage (not 100%)

**DON'T**:
- ❌ Write tests without assertions (meaningless coverage)
- ❌ Test private functions (test public API)
- ❌ Aim for 100% (diminishing returns)
- ❌ Skip error path testing (common gap)

---

## 6. Running Tests

### 6.1 Local Development

**Run all tests**:
```bash
pytest
```

**Run specific file**:
```bash
pytest tests/test_module.py
```

**Run specific test**:
```bash
pytest tests/test_module.py::TestClass::test_function
```

**Run with verbose output**:
```bash
pytest -v  # Show each test name
pytest -vv  # Show more details
```

**Stop at first failure**:
```bash
pytest -x
```

### 6.2 CI/CD Integration

Tests run automatically on:
- Every push to GitHub
- Every pull request
- Before deployment

**Workflow** (.github/workflows/test.yml):
- Runs pytest
- Measures coverage
- Fails if tests fail OR coverage <85%

**View Results**:
- GitHub Actions tab → Test workflow
- See test output and coverage report

---

## 7. Debugging Test Failures

### 7.1 Common Failures

**Assertion Failure**:
```
AssertionError: assert 'HELLO' == 'hello'
```
**Fix**: Check function logic or test expectation

**Import Error**:
```
ImportError: cannot import name 'function'
```
**Fix**: Verify function exists, import path correct

**Async Error**:
```
RuntimeWarning: coroutine was never awaited
```
**Fix**: Add `await` before async function call

### 7.2 Debugging Tools

**Print debugging**:
```python
def test_function():
    result = function()
    print(f"Result: {result}")  # Shows in pytest output
    assert result == expected
```

**Pytest debugging**:
```bash
pytest -s  # Show print() output
pytest --pdb  # Drop into debugger on failure
```

**Coverage details**:
```bash
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
# Visual line-by-line coverage
```

---

## 8. Best Practices

### 8.1 Test Organization

**File structure**:
```
src/my_package/
  ├── utils/
  │   └── validation.py
  └── mcp/
      └── server.py

tests/
  ├── utils/
  │   └── test_validation.py
  └── mcp/
      └── test_server.py
```

**Mirror source structure in tests/**

### 8.2 Test Naming

**Good**:
- `test_validation_rejects_empty_string()`
- `test_process_data_with_invalid_input()`
- `test_async_fetch_returns_dict()`

**Bad**:
- `test_1()`
- `test_function()`
- `test_it_works()`

### 8.3 Test Independence

**Each test should**:
- Set up its own data
- Not depend on other tests
- Clean up after itself
- Be deterministic (same result every time)

---

## 9. Troubleshooting

### Problem: Tests not found

**Symptom**:
```
collected 0 items
```

**Solution**:
- Check file names: `test_*.py` (not `tests_*.py`)
- Check function names: `test_*()` (not `check_*()`)
- Check directory: tests/ exists

### Problem: Coverage below 85%

**Symptom**:
```
FAILED: coverage threshold not met (actual: 78%, required: 85%)
```

**Solution**:
- Run: `pytest --cov=src --cov-report=term-missing`
- Identify missing lines
- Write tests for uncovered code paths
- Re-run coverage check

### Problem: Async tests failing

**Symptom**:
```
RuntimeWarning: coroutine 'test_func' was never awaited
```

**Solution**:
- Ensure test function is `async def test_*()`
- Ensure async calls use `await`
- Check pytest-asyncio is installed (`pip list | grep pytest-asyncio`)

### Problem: Slow tests

**Symptom**:
- Test suite takes >60 seconds

**Solution**:
- Run: `pytest --durations=10` (show slowest tests)
- Mock external calls (network, database)
- Reduce test data size
- Parallelize tests (pytest-xdist plugin, optional)

---

## 10. Next Steps

### After Writing Tests

**Immediate**:
1. ✅ Ensure all tests pass locally
2. ✅ Verify coverage ≥85%
3. ✅ Commit tests with code changes
4. ✅ Watch CI/CD pipeline (tests run automatically)

**Ongoing**:
1. Write tests for new features (TDD approach)
2. Maintain 85%+ coverage
3. Fix flaky tests immediately
4. Review test patterns periodically

### Learn More

1. Read [SAP-005 (ci-cd-workflows)](../ci-cd-workflows/) - CI/CD integration
2. Read [SAP-006 (quality-gates)](../quality-gates/) - Pre-commit hooks
3. Read [static-template/dev-docs/workflows/TDD_WORKFLOW.md](../../../../static-template/dev-docs/workflows/TDD_WORKFLOW.md) - TDD workflow

---

## 11. Related Documents

**SAP-004 Artifacts**:
- [capability-charter.md](capability-charter.md) - This SAP's charter
- [protocol-spec.md](protocol-spec.md) - Technical contract
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [ledger.md](ledger.md) - Coverage tracking

**Testing Components**:
- [pyproject.toml](../../../../blueprints/pyproject.toml.blueprint) - pytest configuration
- [static-template/tests/](../../../../static-template/tests/) - Example tests
- [.github/workflows/test.yml](../../../../static-template/.github/workflows/test.yml) - Test workflow

**Related SAPs**:
- [project-bootstrap/](../project-bootstrap/) - SAP-003 (generates test structure)
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (runs tests in CI)
- [quality-gates/](../quality-gates/) - SAP-006 (enforces coverage)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial adoption blueprint for testing-framework
