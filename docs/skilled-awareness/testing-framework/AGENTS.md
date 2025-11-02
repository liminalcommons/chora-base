# AGENTS.md - Testing Framework (SAP-004)

**Domain**: Testing & Quality
**SAP**: SAP-004 (testing-framework)
**Version**: 1.1.0
**Last Updated**: 2025-10-31

---

## Overview

This is the domain-specific AGENTS.md file for the testing framework (SAP-004). It provides context for agents working with pytest, coverage, fixtures, and test patterns.

**Parent**: See [/AGENTS.md](/AGENTS.md) for project-level context

**Pattern**: "Nearest File Wins" - This file provides testing-specific context

---

## User Signal Patterns

### Testing Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "run tests" | pytest_run() | pytest | Full test suite |
| "execute tests" | pytest_run() | Same command | Variation |
| "test" | pytest_run() | Shortened form | Context-dependent |
| "run pytest" | pytest_run() | Explicit | |
| "check coverage" | pytest_coverage_report() | pytest --cov | Target: ≥85% |
| "how's our coverage" | pytest_coverage_report() | Natural variation | |
| "coverage report" | pytest_coverage_report() | Formal term | |
| "coverage stats" | pytest_coverage_report() | Variation | |
| "run tests for FILE" | pytest_run_file(path) | pytest PATH | Single file |
| "test FILE" | pytest_run_file(path) | Shortened | |
| "fix failing test" | identify_and_fix_test() | pytest -v, read failure | Debug workflow |
| "debug test" | identify_and_fix_test() | Same workflow | |
| "add test for FUNCTION" | create_test_function() | Edit test file, follow patterns | Use fixtures |
| "write test for X" | create_test_function() | Variation | |
| "update fixtures" | edit_conftest() | Edit conftest.py | Shared test setup |
| "add fixture" | edit_conftest() | Same action | |

### Coverage Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "coverage below 85" | identify_untested_code() | pytest --cov --cov-report=term-missing | Show gaps |
| "what's not tested" | identify_untested_code() | Same report | |
| "improve coverage" | add_tests_for_gaps() | Target uncovered lines | Prioritize critical paths |
| "increase coverage" | add_tests_for_gaps() | Same action | |
| "coverage report html" | generate_coverage_html() | pytest --cov --cov-report=html | Open htmlcov/index.html |
| "show coverage details" | generate_coverage_html() | Visual report | |

### Test Debugging

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "why is test X failing" | debug_failing_test(name) | pytest -v TEST, read output | Analyze failure |
| "test X failed" | debug_failing_test(name) | Same workflow | |
| "run failing tests" | pytest_run_failed() | pytest --lf (last failed) | Re-run failures only |
| "rerun failed" | pytest_run_failed() | Same command | |
| "verbose test output" | pytest_run_verbose() | pytest -v | Detailed output |
| "show test details" | pytest_run_verbose() | Same | |

### Common Variations

**Test Execution**:
- "run tests" / "execute tests" / "test" / "pytest" → pytest_run()
- "run all tests" / "full test suite" → pytest_run()

**Coverage Queries**:
- "check coverage" / "how's coverage" / "coverage stats" → pytest_coverage_report()
- "what's not tested" / "coverage gaps" / "uncovered code" → identify_untested_code()

**Test Creation**:
- "add test" / "write test" / "create test" → create_test_function()

---

## Testing Framework Quick Reference

### Test Execution

**Run All Tests**:
```bash
pytest
```

**Run With Coverage**:
```bash
pytest --cov=scripts --cov=src --cov-report=term-missing
```

**Run Specific File**:
```bash
pytest tests/test_intent_router.py
```

**Run Specific Test**:
```bash
pytest tests/test_intent_router.py::test_exact_match
```

**Run Failed Tests Only**:
```bash
pytest --lf  # last failed
pytest --ff  # failed first
```

**Verbose Output**:
```bash
pytest -v   # verbose
pytest -vv  # extra verbose
```

### Coverage Targets

**chora-base Standards**:
- **Minimum**: 85% coverage
- **Target**: 90% coverage
- **Critical paths**: 100% coverage

**Check Coverage Threshold**:
```bash
pytest --cov=scripts --cov-fail-under=85
```

**Coverage Reports**:
```bash
# Terminal report
pytest --cov --cov-report=term-missing

# HTML report
pytest --cov --cov-report=html
open htmlcov/index.html
```

### Test Patterns

**1. Arrange-Act-Assert**:
```python
def test_intent_router_exact_match():
    # Arrange
    router = IntentRouter()
    user_input = "show inbox"

    # Act
    matches = router.route(user_input)

    # Assert
    assert matches[0].action == "run_inbox_status"
    assert matches[0].confidence >= 0.70
```

**2. Parameterized Tests**:
```python
@pytest.mark.parametrize("user_input,expected_action", [
    ("show inbox", "run_inbox_status"),
    ("check coverage", "pytest_coverage_report"),
    ("run tests", "pytest_run"),
])
def test_intent_recognition(user_input, expected_action):
    router = IntentRouter()
    matches = router.route(user_input)
    assert matches[0].action == expected_action
```

**3. Fixtures**:
```python
@pytest.fixture
def mock_inbox_status():
    """Provide mock inbox data for testing."""
    return {
        'repositories': {
            'chora-base': {
                'active_work': [
                    {'id': 'coord-001', 'status': 'pending_triage'}
                ]
            }
        }
    }

def test_inbox_suggestions(mock_inbox_status):
    engine = SuggestionEngine()
    suggestions = engine.suggest_inbox_actions(mock_inbox_status)
    assert len(suggestions) > 0
```

**4. Mocking**:
```python
from unittest.mock import patch, MagicMock

def test_glossary_search_with_mock():
    with patch('scripts.chora_search.open') as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = "mock glossary"
        glossary = GlossarySearch()
        # Test continues...
```

**5. Async Testing**:
```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == expected
```

**6. BDD with behave**:
```gherkin
# features/intent-recognition.feature
Scenario: Recognize inbox status query
  Given the intent router is initialized
  When user input is "show inbox"
  Then intent should be "run_inbox_status"
  And confidence should be >= 0.70
```

### Fixtures (conftest.py)

**Common Fixtures**:
```python
# tests/conftest.py

@pytest.fixture
def intent_router():
    """Provide initialized intent router."""
    from scripts.intent_router import IntentRouter
    return IntentRouter()

@pytest.fixture
def glossary_search():
    """Provide initialized glossary search."""
    from scripts.chora_search import GlossarySearch
    return GlossarySearch()

@pytest.fixture
def temp_file(tmp_path):
    """Provide temporary file for testing."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")
    return file_path
```

### Quality Gates

**Before Commit**:
- [ ] All tests passing
- [ ] Coverage ≥85%
- [ ] No new lint errors (ruff)
- [ ] No new type errors (mypy)

**Before PR**:
- [ ] All tests passing
- [ ] Coverage ≥85%
- [ ] All BDD scenarios passing (if applicable)
- [ ] Test for new features added
- [ ] Test for bug fixes added

**CI/CD**:
- [ ] Matrix testing (Python 3.11, 3.12, 3.13)
- [ ] Coverage threshold enforced
- [ ] Lint validation (ruff check)
- [ ] Type checking (mypy --strict)

---

## Integration with Bidirectional Translation Layer

This domain AGENTS.md file integrates with the bidirectional translation layer (SAP-009 v1.1.0):

**Discovery Flow**:
1. User says "check coverage" (casual, conversational)
2. Intent router loads root AGENTS.md (discovers intent-router.py exists)
3. Intent router loads THIS FILE (domain-specific patterns)
4. Matches "check coverage" → `pytest_coverage_report` with high confidence
5. Agent executes `pytest --cov --cov-report=term`
6. Agent parses coverage percentage and formats output

**Context-Aware Suggestions**:
- If coverage <85%, suggestion engine recommends "Improve test coverage"
- Suggests specific files with low coverage from `--cov-report=term-missing`
- Prioritizes critical paths (business logic, API endpoints)

**Progressive Formalization**:
- Week 1: "check our test coverage" → Agent translates and explains
- Week 2-4: "what's coverage?" → Agent teaches 85% target
- Month 2+: "pytest --cov" → Agent executes directly
- Month 3+: User writes pytest commands confidently

**See**: [/AGENTS.md lines 732-944](/AGENTS.md) for bidirectional translation layer overview

---

## Related SAPs

- **SAP-003** (project-bootstrap): Test structure generation
- **SAP-004** (testing-framework): THIS SAP - Testing patterns
- **SAP-005** (ci-cd-workflows): Test automation in GitHub Actions
- **SAP-006** (quality-gates): Coverage enforcement, pre-commit hooks
- **SAP-009** (agent-awareness): AGENTS.md pattern and bidirectional translation
- **SAP-012** (development-lifecycle): BDD→TDD workflow integration

---

**Version History**:
- **1.1.0** (2025-10-31): Added User Signal Patterns section for bidirectional translation layer integration
- **1.0.0** (2025-10-31): Initial domain AGENTS.md for testing framework
