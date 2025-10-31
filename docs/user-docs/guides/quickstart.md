# Quickstart Guide

**Time**: 5 minutes
**Goal**: Create your first feature with chora-base

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

**Output**:
```
tests/test_calculator.py::test_add PASSED                               [100%]

=========================== 1 passed in 0.02s ===========================
```

## 4. Check Coverage

```bash
pytest --cov=src/myproject --cov-report=term
```

## 5. Check Code Quality

```bash
ruff check src/myproject/calculator.py
mypy src/myproject/calculator.py
```

## 6. Commit Your Work

```bash
git add src/myproject/calculator.py tests/test_calculator.py
git commit -m "feat: add calculator module"
```

---

## What's Next?

- [Installation Guide](installation.md) - Full setup details
- [GitHub Actions Guide](github-actions.md) - Enable CI/CD
- [SAP-004: Testing Framework](../../skilled-awareness/testing-framework/) - Advanced testing patterns

---

**Last Updated**: 2025-10-29
