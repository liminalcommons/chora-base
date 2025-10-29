# Awareness Guide: Testing Framework

**SAP ID**: SAP-004
**Version**: 1.0.0
**Target Audience**: AI agents (Claude Code, Cursor, etc.)
**Last Updated**: 2025-10-28

---

## 1. Quick Reference

### Common Agent Tasks

**Run tests**:
```bash
pytest                                 # Run all tests
pytest --cov=src --cov-report=term-missing  # With coverage
pytest -v                              # Verbose output
```

**Write test**:
```python
def test_function_name():
    """Test description."""
    result = function()
    assert result == expected
```

**Write async test**:
```python
async def test_async_function():
    """Test async operation."""
    result = await async_function()
    assert result == expected
```

### Quick Commands

**Check coverage**:
```bash
pytest --cov=src --cov-report=term
```

**Find untested code**:
```bash
pytest --cov=src --cov-report=term-missing
```

**Test specific file**:
```bash
pytest tests/test_module.py
```

---

## 2. Agent Context Loading

### Essential Context (2-4k tokens)

**For writing tests**:
1. [protocol-spec.md](protocol-spec.md) Sections 3.3, 7 (2k tokens) - Test structure, patterns
2. Example test file (static-template/tests/utils/test_validation.py, 1k tokens)

**For debugging test failures**:
1. [protocol-spec.md](protocol-spec.md) Section 8 (1k tokens) - Test quality
2. pytest error output (analyze directly)

**For achieving coverage**:
1. [protocol-spec.md](protocol-spec.md) Section 6.2 (1k tokens) - Coverage standards
2. Coverage report (pytest --cov output)

### What to Skip

- ❌ Full pytest documentation (use Protocol patterns)
- ❌ pytest internals (just use patterns)
- ❌ All example tests (read 1-2 examples only)

---

## 3. Common Workflows

### 3.1 Write Test for New Function

**Context**: 2k tokens (Protocol Section 7.1-7.3)

**Steps**:
1. **Identify function to test**:
   ```python
   # In src/my_package/module.py
   def process_data(input: str) -> str:
       if not input:
           raise ValueError("Input required")
       return input.upper()
   ```

2. **Create test file** (tests/test_module.py):
   ```python
   """Tests for my_package.module."""

   import pytest
   from my_package.module import process_data


   class TestProcessData:
       """Tests for process_data function."""

       def test_happy_path(self):
           """Test normal operation with valid input."""
           result = process_data("hello")
           assert result == "HELLO"

       def test_error_empty_input(self):
           """Test error handling for empty input."""
           with pytest.raises(ValueError, match="Input required"):
               process_data("")
   ```

3. **Run test**:
   ```bash
   pytest tests/test_module.py -v
   ```

4. **Success Criteria**:
   - Tests pass
   - Coverage of new function ≥85%
   - Both happy path and error path tested

**Time**: 5-10 minutes per function

### 3.2 Write Async Test

**Context**: 2k tokens (Protocol Section 7.4)

**Steps**:
1. **Identify async function**:
   ```python
   # In src/my_package/async_module.py
   async def fetch_data(url: str) -> dict:
       # Async operation
       return {"data": "result"}
   ```

2. **Create async test**:
   ```python
   """Tests for my_package.async_module."""

   import pytest
   from my_package.async_module import fetch_data


   class TestFetchData:
       """Tests for fetch_data function."""

       async def test_fetch_success(self):
           """Test successful fetch."""
           result = await fetch_data("https://example.com")
           assert "data" in result
           assert result["data"] == "result"
   ```

3. **Run async test**:
   ```bash
   pytest tests/test_async_module.py -v
   # pytest-asyncio automatically handles async tests
   ```

**Note**: pytest-asyncio (asyncio_mode = "auto") handles async/await automatically.

### 3.3 Achieve 85% Coverage

**Context**: 3k tokens (Protocol Section 6.2, coverage report)

**Steps**:
1. **Run coverage check**:
   ```bash
   pytest --cov=src --cov-report=term-missing
   ```

2. **Analyze output**:
   ```
   Name                    Stmts   Miss  Cover   Missing
   ---------------------------------------------------
   src/my_package/module.py   50      8    84%   45-51, 67
   ---------------------------------------------------
   TOTAL                     200     16    92%
   ```

3. **Identify missing lines**:
   - Open src/my_package/module.py
   - Go to lines 45-51, 67
   - Determine what code paths are untested

4. **Write tests for missing lines**:
   ```python
   def test_previously_untested_path(self):
       """Test code path that was missing coverage."""
       # Test the specific scenario that executes lines 45-51
       result = function_with_specific_condition()
       assert result is not None
   ```

5. **Verify coverage improved**:
   ```bash
   pytest --cov=src --cov-report=term-missing
   # Now shows 86% (above 85% threshold)
   ```

**Time**: 10-20 minutes to go from 75% → 85%

### 3.4 Debug Failing Test

**Context**: 2k tokens (test code + error output)

**Steps**:
1. **Run test with verbose output**:
   ```bash
   pytest tests/test_module.py::test_function -vv
   ```

2. **Analyze failure**:
   ```
   FAILED tests/test_module.py::test_function - AssertionError: assert 'HELLO' == 'hello'
   ```

3. **Common failure types**:

   **Assertion Failure**:
   ```
   AssertionError: assert result == expected
   # Fix: Check function logic or test expectation
   ```

   **Import Error**:
   ```
   ImportError: cannot import name 'function' from 'module'
   # Fix: Check function exists, import path correct
   ```

   **Async Error**:
   ```
   RuntimeWarning: coroutine 'async_function' was never awaited
   # Fix: Add 'await' before async function call
   ```

4. **Fix issue**:
   - Update function logic (if bug)
   - Update test expectation (if test wrong)
   - Add await (if async issue)

5. **Re-run test**:
   ```bash
   pytest tests/test_module.py::test_function -v
   # Should pass now
   ```

---

## 4. Integration Patterns

### 4.1 With Project Bootstrap

**Pattern**: Generated project includes test structure

```
Generated project includes:
  - tests/ directory (from static-template)
  - tests/utils/test_*.py (example tests)
  - pyproject.toml [tool.pytest.ini_options] (configuration)

Agent validates:
  - pytest --collect-only (tests loadable)
  - pytest (tests pass)
  - Coverage ≥85% (quality gate)
```

### 4.2 With CI/CD Workflows

**Pattern**: Tests run automatically in GitHub Actions

```
.github/workflows/test.yml:
  - Runs pytest on every push
  - Runs pytest on every PR
  - Fails if tests fail OR coverage <85%
  - Reports coverage to Codecov (optional)

Agent ensures:
  - Tests pass locally before commit
  - Coverage ≥85% before commit
  - No flaky tests (consistent results)
```

### 4.3 With Quality Gates

**Pattern**: Tests are a quality gate

```
Pre-commit hooks (SAP-006):
  - Run pytest before commit
  - Block commit if tests fail
  - Block commit if coverage <85%

Agent workflow:
  1. Write feature code
  2. Write tests (coverage ≥85%)
  3. Run pytest locally (must pass)
  4. Commit (pre-commit runs tests)
  5. Push (CI runs tests)
```

---

## 5. Best Practices

### DO

- ✅ Write tests for all public functions
- ✅ Test happy path AND error paths
- ✅ Use descriptive test names (test_function_with_condition)
- ✅ Use pytest.raises for error testing
- ✅ Use async def for async function tests
- ✅ Aim for 85%+ coverage
- ✅ Keep tests fast (<60s total)

### DON'T

- ❌ Skip error path testing (common coverage gap)
- ❌ Write tests without assertions (meaningless coverage)
- ❌ Forget 'await' in async tests (silent failure)
- ❌ Test implementation details (test behavior, not internals)
- ❌ Make tests depend on each other (test order)
- ❌ Leave flaky tests (intermittent failures)
- ❌ Aim for 100% coverage (diminishing returns)

---

## 6. Claude-Specific Optimizations

### Context Management

**Load Order** (progressive):
1. Protocol Sections 3.3, 7 (2k) → Test structure, patterns
2. Example test (1k) → See patterns in action
3. Coverage standards (1k) → Understand 85% requirement

**Token Budget**:
- Essential: 2-4k (patterns + example)
- Extended: 5-7k (+ coverage standards + CI integration)
- Full: 8-10k (+ all quality attributes)

### Parallel Operations

**When Writing Multiple Tests**:
```
Parallel:
  - Read function to test
  - Read similar existing test (pattern reference)
  - Prepare test structure

Sequential:
  - Write test code
  - Run pytest
  - Fix issues
  - Verify coverage
```

**Result**: 5-10 min per test (vs 10-15 min sequential)

---

## 7. Troubleshooting Reference

### Quick Diagnostics

**Tests not found**:
```bash
pytest --collect-only
# Shows: collected 0 items
# Fix: Check test file names (test_*.py), function names (test_*)
```

**Async tests failing**:
```bash
pytest -v
# Shows: RuntimeWarning: coroutine 'test_func' was never awaited
# Fix: Add 'async def' to test function, ensure 'await' on async calls
```

**Coverage below 85%**:
```bash
pytest --cov=src --cov-report=term-missing
# Shows missing lines (e.g., "45-51")
# Fix: Write tests for uncovered code paths
```

**Slow tests**:
```bash
pytest --durations=10
# Shows slowest 10 tests
# Fix: Mock network calls, reduce test data size
```

---

## 8. Related Resources

**SAP-004 Artifacts**:
- [capability-charter.md](capability-charter.md) - This SAP's charter
- [protocol-spec.md](protocol-spec.md) - Technical contract
- [adoption-blueprint.md](adoption-blueprint.md) - How to use testing
- [ledger.md](ledger.md) - Coverage tracking

**Testing Components**:
- [pyproject.toml](../../../../blueprints/pyproject.toml.blueprint) - pytest config (lines 45-50)
- [static-template/tests/](../../../../static-template/tests/) - Example tests
- [.github/workflows/test.yml](../../../../static-template/.github/workflows/test.yml) - CI workflow

**Related SAPs**:
- [project-bootstrap/](../project-bootstrap/) - SAP-003 (generates test structure)
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (runs tests in CI)
- [quality-gates/](../quality-gates/) - SAP-006 (enforces coverage)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial awareness guide for testing-framework
