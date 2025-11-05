# Quickstart Guide: Python TDD Workflow

**Time**: 5 minutes
**Goal**: Create your first feature using chora-base's TDD workflow
**For**: Developers new to Python development or chora-base

**Last Updated**: 2025-11-05

---

## Overview

This quickstart demonstrates chora-base's Python development workflow:
1. Write a function
2. Write tests
3. Run tests with pytest
4. Check coverage
5. Check code quality (ruff + mypy)
6. Commit

**This is NOT a SAP-focused guide** - for SAP adoption, see:
- [Quickstart: Generic AI Agent](../how-to/quickstart-generic-ai-agent.md) - SAP navigation (15 min)
- [Quickstart: Claude Code](../how-to/quickstart-claude.md) - Claude-optimized SAP exploration (12 min)

---

## 1. Create a Simple Function

```python
# src/myproject/calculator.py
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
```

## 2. Write a Test

```python
# tests/test_calculator.py
from myproject.calculator import add

def test_add():
    """Test addition function."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

## 3. Run Tests

```bash
pytest tests/test_calculator.py -v
```

**Expected Output**:
```
tests/test_calculator.py::test_add PASSED                               [100%]

=========================== 1 passed in 0.02s ===========================
```

## 4. Check Coverage

```bash
pytest --cov=src/myproject --cov-report=term
```

**Expected**: 100% coverage for calculator.py

## 5. Check Code Quality

```bash
# Linting with ruff
ruff check src/myproject/calculator.py

# Type checking with mypy
mypy src/myproject/calculator.py
```

**Expected**: No errors or warnings

## 6. Commit Your Work

```bash
git add src/myproject/calculator.py tests/test_calculator.py
git commit -m "feat: add calculator module with tests"
```

---

## What's Next?

### For Python Development
- [Installation Guide](installation.md) - Full Python project setup
- [GitHub Actions Guide](github-actions.md) - Enable CI/CD
- [Testing Framework](../../skilled-awareness/testing-framework/AGENTS.md) - Advanced pytest patterns (SAP-004)

### For SAP Adoption (AI Agents)
- [Generic AI Agent Quickstart](../how-to/quickstart-generic-ai-agent.md) - Navigate all 29 SAPs (15 min)
- [Claude Code Quickstart](../how-to/quickstart-claude.md) - Claude-optimized exploration (12 min)
- [Understanding SAPs](../explanation/understanding-saps.md) - Conceptual overview

### For Understanding chora-base
- [Root AGENTS.md](/AGENTS.md) - Project-wide agent patterns
- [Root CLAUDE.md](/CLAUDE.md) - Claude navigation strategy (if using Claude)
- [SAP Catalog](../../../sap-catalog.json) - All 29 available SAPs

---

**Version**: 1.1.0
**Changes**: Clarified as Python TDD workflow (not SAP-focused), fixed SAP-004 reference path, added clear navigation to SAP quickstarts
