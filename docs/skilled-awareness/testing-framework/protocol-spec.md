# Protocol Specification: Testing Framework

**SAP ID**: SAP-004
**Version**: 1.0.0
**Status**: Draft (Phase 2)
**Last Updated**: 2025-10-28

---

## 1. Overview

### Purpose

The testing-framework capability provides **pytest-based comprehensive testing** with async support, coverage measurement, and CI integration. It defines test structure, patterns, coverage standards, and quality contracts for all chora-base projects.

### Design Principles

1. **pytest-Based** - Modern Python testing (not unittest)
2. **85% Coverage Minimum** - Industry best practice (80-85% optimal, based on research)
3. **Async-First** - Native async/await support via pytest-asyncio
4. **Pattern-Driven** - Reusable fixtures, parametrized tests, clear organization
5. **Fast Feedback** - Tests complete in <60s locally, provide clear failures

---

## 2. System Architecture

### 2.1 Component Overview

```
Project Root/
├── pyproject.toml                    # pytest configuration
│   └── [tool.pytest.ini_options]    # Test discovery, async mode
│   └── [tool.coverage.run]          # Coverage measurement
├── tests/                            # Test directory
│   ├── conftest.py                   # Shared fixtures (optional)
│   ├── test_*.py                     # Test modules
│   ├── utils/                        # Utility tests
│   │   ├── test_validation.py
│   │   ├── test_errors.py
│   │   ├── test_responses.py
│   │   └── test_persistence.py
│   ├── memory/                       # Memory system tests (future)
│   └── mcp/                          # MCP server tests (future)
└── .github/workflows/test.yml        # CI test workflow
```

### 2.2 Test Execution Flow

```
Developer: pytest [options]
    │
    v
[pytest: test discovery]
    │
    ├─► Find tests/ directory (testpaths = ["tests"])
    ├─► Match test_*.py files (python_files = ["test_*.py"])
    ├─► Match Test* classes (python_classes = ["Test*"])
    ├─► Match test_* functions (python_functions = ["test_*"])
    │
    v
[pytest: async handling]
    │
    ├─► asyncio_mode = "auto" (from pytest-asyncio)
    ├─► Detect async test functions (async def test_*)
    ├─► Wrap in asyncio.run()
    │
    v
[pytest: test execution]
    │
    ├─► Run each test
    ├─► Collect assertions
    ├─► Report pass/fail
    │
    v
[pytest-cov: coverage measurement]
    │
    ├─► Measure line coverage (src/ only, exclude tests/)
    ├─► Calculate percentage
    ├─► Compare to threshold (85%)
    │
    v
[pytest: result reporting]
    │
    ├─► Terminal output (pass/fail/skip counts)
    ├─► Coverage report (percentage, missing lines)
    ├─► Exit code (0 = success, 1 = failure)
```

---

## 3. Data Models

### 3.1 pytest Configuration

**Location**: pyproject.toml

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"          # Enable pytest-asyncio auto mode
testpaths = ["tests"]          # Where to find tests
python_files = ["test_*.py"]   # Test file pattern
python_classes = ["Test*"]     # Test class pattern
python_functions = ["test_*"]  # Test function pattern
addopts = [                    # Default options
    "--cov=src",               # Measure coverage of src/
    "--cov-report=term-missing",  # Show missing lines
    "--cov-fail-under=85",     # Fail if coverage <85%
]
```

### 3.2 Coverage Configuration

**Location**: pyproject.toml (optional, uses pytest-cov defaults)

```toml
[tool.coverage.run]
source = ["src"]               # Measure coverage in src/
omit = [                       # Exclude from coverage
    "*/tests/*",
    "*/__pycache__/*",
    "*/site-packages/*",
]

[tool.coverage.report]
precision = 2                  # Report to 2 decimal places
show_missing = true            # Show missing line numbers
skip_covered = false           # Show all files (not just uncovered)
```

### 3.3 Test Structure

**Test Module** (test_*.py):
```python
"""Tests for {module} functionality.

Description of what this test module covers.
"""

import pytest
from my_package.module import function_to_test


# =============================================================================
# Tests for specific function/class
# =============================================================================

class TestFunctionName:
    """Tests for function_name."""

    def test_happy_path(self):
        """Test normal operation with valid inputs."""
        result = function_to_test("valid input")
        assert result == "expected output"

    def test_edge_case_empty(self):
        """Test edge case: empty input."""
        result = function_to_test("")
        assert result == ""

    def test_error_handling(self):
        """Test error handling for invalid input."""
        with pytest.raises(ValueError, match="expected error message"):
            function_to_test(None)


# =============================================================================
# Parametrized tests
# =============================================================================

@pytest.mark.parametrize("input,expected", [
    ("a", "A"),
    ("hello", "HELLO"),
    ("123", "123"),
])
def test_parametrized(input, expected):
    """Test multiple inputs with parametrization."""
    assert function_to_test(input) == expected
```

**Async Test Module**:
```python
"""Tests for async functionality."""

import pytest


class TestAsyncFunction:
    """Tests for async_function."""

    async def test_async_operation(self):
        """Test async operation (pytest-asyncio handles this)."""
        result = await async_function()
        assert result == "expected"

    async def test_async_with_timeout(self):
        """Test async with timeout."""
        import asyncio
        result = await asyncio.wait_for(
            async_function(),
            timeout=1.0
        )
        assert result is not None
```

---

## 4. Behavior Specification

### 4.1 Test Discovery

**Input**:
- Command: `pytest` (or `pytest tests/`)

**Process**:
1. Read `testpaths = ["tests"]` from pyproject.toml
2. Find all files matching `test_*.py` in tests/
3. Find all classes matching `Test*` in those files
4. Find all functions matching `test_*` in those classes/modules
5. Collect fixtures from conftest.py (if exists)

**Output**:
- List of test items to run
- Example: `collected 47 items`

### 4.2 Test Execution

**For Sync Test**:
```python
def test_example():
    assert function() == expected
```
**Process**:
1. Call function()
2. Compare to expected
3. Raise AssertionError if not equal
4. Mark test as PASSED or FAILED

**For Async Test**:
```python
async def test_async_example():
    result = await async_function()
    assert result == expected
```
**Process**:
1. pytest-asyncio detects `async def`
2. Wrap in `asyncio.run(test_async_example())`
3. Execute async code
4. Collect assertion results
5. Mark test as PASSED or FAILED

### 4.3 Coverage Measurement

**Process**:
1. pytest-cov hooks into test execution
2. Measure which lines in src/ are executed
3. Count total lines vs executed lines
4. Calculate percentage: (executed / total) * 100
5. Compare to threshold (85%)
6. Report coverage: `TOTAL: 85%` (example)

**Output**:
```
---------- coverage: platform linux, python 3.11.0 -----------
Name                          Stmts   Miss  Cover   Missing
-----------------------------------------------------------
src/my_package/__init__.py        5      0   100%
src/my_package/module.py         50      7    86%   45-51
-----------------------------------------------------------
TOTAL                           200     15    92%
```

### 4.4 Result Reporting

**Terminal Output**:
```
======================== test session starts =========================
platform linux -- Python 3.11.0, pytest-8.3.0, pluggy-1.5.0
collected 47 items

tests/test_module.py .......                                    [ 14%]
tests/utils/test_validation.py ......................           [ 62%]
tests/utils/test_errors.py .....                                [ 72%]
tests/utils/test_responses.py ......                            [ 85%]
tests/utils/test_persistence.py .......                         [100%]

========================= 47 passed in 2.34s =========================
```

**Exit Code**:
- `0`: All tests passed, coverage ≥85%
- `1`: Tests failed OR coverage <85%

---

## 5. Interface Contracts

### 5.1 CLI Interface

**Run All Tests**:
```bash
pytest
```

**Run Specific Test File**:
```bash
pytest tests/test_module.py
```

**Run Specific Test Function**:
```bash
pytest tests/test_module.py::test_function_name
```

**Run with Coverage Report**:
```bash
pytest --cov=src --cov-report=term-missing
```

**Run with Verbose Output**:
```bash
pytest -v  # Show each test name
pytest -vv  # Show each test with more detail
```

**Run and Stop at First Failure**:
```bash
pytest -x  # Stop after first failure
pytest --maxfail=3  # Stop after 3 failures
```

### 5.2 CI/CD Interface

**GitHub Actions Workflow** (.github/workflows/test.yml):
```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"

      - name: Run tests with coverage
        run: |
          pytest --cov=src --cov-report=term-missing --cov-report=xml

      - name: Upload coverage to Codecov (optional)
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
```

---

## 6. Guarantees

### 6.1 Test Quality Contracts

When tests pass with coverage ≥85%, the project **guarantees**:

1. **Coverage**:
   - ✅ ≥85% of src/ lines executed
   - ✅ All critical paths tested (happy path + error handling)
   - ✅ No untested public functions

2. **Test Validity**:
   - ✅ All tests have assertions (not just execution)
   - ✅ Tests are independent (no test order dependencies)
   - ✅ Tests are deterministic (no flaky tests)

3. **Async Correctness**:
   - ✅ Async functions properly tested with pytest-asyncio
   - ✅ No race conditions in tests
   - ✅ Proper async cleanup (fixtures)

4. **Error Handling**:
   - ✅ All error paths tested (pytest.raises)
   - ✅ Error messages validated
   - ✅ Edge cases covered

5. **Performance**:
   - ✅ Test suite completes in <60s (local)
   - ✅ No network calls in unit tests (mocked)
   - ✅ Fast feedback loop

### 6.2 Coverage Standards

**Why 85%?**

Based on industry research:
- **80-85%**: Optimal balance (diminishing returns above 85%)
- **<80%**: High risk of untested code
- **>90%**: Excessive effort, often achieved with meaningless tests

**What 85% Means**:
- 85% of lines executed ≈ 80%+ branch coverage
- Critical paths: 100% coverage
- Utility functions: 85%+ coverage
- Boilerplate (__init__, simple getters): May be <85%, acceptable

**What 85% Doesn't Mean**:
- Not "85% of features tested" (could be less if complex features)
- Not "85% quality" (coverage ≠ quality)
- Not "test 85 lines out of 100" (some lines more critical)

---

## 7. Test Patterns

### 7.1 Fixture Pattern

**Purpose**: Share setup code across tests

```python
import pytest


@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {"key": "value", "count": 42}


def test_with_fixture(sample_data):
    """Test using fixture."""
    assert sample_data["key"] == "value"
    assert sample_data["count"] == 42
```

### 7.2 Parametrized Pattern

**Purpose**: Test multiple inputs without duplication

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
])
def test_uppercase(input, expected):
    """Test uppercase conversion."""
    assert input.upper() == expected
```

### 7.3 Error Testing Pattern

**Purpose**: Verify error handling

```python
def test_error_handling():
    """Test that invalid input raises ValueError."""
    with pytest.raises(ValueError, match="expected error"):
        function_that_should_fail(None)
```

### 7.4 Async Testing Pattern

**Purpose**: Test async functions

```python
async def test_async_function():
    """Test async operation."""
    result = await async_function()
    assert result == "expected"
```

### 7.5 Mock Pattern

**Purpose**: Isolate unit under test

```python
from unittest.mock import Mock, AsyncMock


def test_with_mock():
    """Test using mock."""
    mock_api = Mock()
    mock_api.get_data.return_value = {"data": "mocked"}

    result = function_that_calls_api(mock_api)

    assert result == "mocked"
    mock_api.get_data.assert_called_once()


async def test_async_with_mock():
    """Test async function with mock."""
    mock_api = AsyncMock()
    mock_api.fetch.return_value = {"data": "mocked"}

    result = await async_function(mock_api)

    assert result == "mocked"
```

---

## 8. Quality Attributes

### 8.1 Test Organization

**File Structure**:
- `tests/test_<module>.py` - Tests for `src/<package>/<module>.py`
- `tests/<subdir>/test_*.py` - Tests for `src/<package>/<subdir>/`
- Mirror source structure in tests/

**Example**:
```
src/my_package/
  ├── utils/
  │   ├── validation.py
  │   └── errors.py
  └── mcp/
      └── server.py

tests/
  ├── utils/
  │   ├── test_validation.py
  │   └── test_errors.py
  └── mcp/
      └── test_server.py
```

### 8.2 Test Naming

**Descriptive Names**:
- ✅ `test_validation_rejects_empty_string()` - Clear what's tested
- ❌ `test_1()` - Unclear purpose

**Patterns**:
- `test_<function>_<scenario>()`
- `test_<function>_with_<condition>()`
- `test_<function>_raises_<error>()`

### 8.3 Test Independence

**Each test should**:
- Set up its own data (fixtures)
- Not depend on test execution order
- Clean up after itself
- Not modify global state

---

## 9. Related Documents

**SAP-004 Artifacts**:
- [capability-charter.md](capability-charter.md) - This SAP's charter
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [adoption-blueprint.md](adoption-blueprint.md) - How to use testing
- [ledger.md](ledger.md) - Coverage tracking

**Testing Components**:
- [pyproject.toml](../../../../blueprints/pyproject.toml.blueprint) - Lines 45-50
- [static-template/tests/](../../../../static-template/tests/) - Test examples
- [.github/workflows/test.yml](../../../../static-template/.github/workflows/test.yml) - Test workflow

**Related SAPs**:
- [project-bootstrap/](../project-bootstrap/) - SAP-003 (generates test structure)
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (runs tests in CI)
- [quality-gates/](../quality-gates/) - SAP-006 (enforces coverage)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial protocol specification for testing-framework
