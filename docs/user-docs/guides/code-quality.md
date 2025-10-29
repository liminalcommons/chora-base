# Code Quality Guide

**Audience**: Developers maintaining high code quality
**Related**: [SAP-006: Quality Gates](../../skilled-awareness/quality-gates/)

---

## Overview

Chora-base projects enforce code quality through:
1. **Linting** (ruff) - Style and best practices
2. **Type Checking** (mypy) - Type safety
3. **Test Coverage** (pytest + coverage) - ≥85% coverage
4. **Security Scanning** (CodeQL) - Vulnerability detection

---

## Linting with Ruff

### Quick Start

```bash
# Check for issues
ruff check .

# Auto-fix issues
ruff check --fix .
```

### Common Issues

**Line too long**:
```python
# Bad
def create_user(name, email, address, phone, preferences, metadata, created_at):
    pass

# Good
def create_user(
    name, email, address, phone,
    preferences, metadata, created_at
):
    pass
```

**Unused imports**:
```python
# Bad
from typing import Optional, List  # List unused

# Good
from typing import Optional
```

**Import sorting**:
```python
# Bad
import myproject
import os
from typing import Optional

# Good (ruff check --fix auto-fixes this)
import os
from typing import Optional

import myproject
```

### Configuration

**pyproject.toml**:
```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I"]  # pycodestyle, pyflakes, isort
ignore = ["E501"]  # Allow long lines in docstrings
```

---

## Type Checking with Mypy

### Quick Start

```bash
# Check types
mypy src
```

### Adding Type Hints

```python
# Before (no types)
def process(data):
    return data.upper()

# After (with types)
def process(data: str) -> str:
    return data.upper()
```

### Common Type Patterns

**Optional values**:
```python
from typing import Optional

def find_user(id: int) -> Optional[User]:
    """Returns User or None if not found."""
    return db.get(id)
```

**Lists and dicts**:
```python
from typing import List, Dict

def get_users() -> List[User]:
    return [User(...), User(...)]

def get_config() -> Dict[str, str]:
    return {"key": "value"}
```

**Union types** (Python 3.10+):
```python
def process(value: str | int) -> str:
    if isinstance(value, int):
        return str(value)
    return value
```

### Configuration

**pyproject.toml**:
```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

---

## Test Coverage

### Quick Start

```bash
# Run with coverage
pytest --cov=src --cov-report=term-missing

# Generate HTML report
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### Coverage Standards

- **Minimum**: 85% (enforced in CI)
- **Target**: 90%+
- **Critical paths**: 100% (auth, payments, security)

### Improving Coverage

**Identify uncovered code**:
```bash
pytest --cov=src --cov-report=term-missing
```

**Output shows**:
```
src/myproject/api.py    45    12    73%   78-80, 145-151
```

**Write tests for lines 78-80, 145-151**:
```python
def test_api_error_handling():
    """Test error paths (lines 78-80)."""
    response = client.post("/users", json={})
    assert response.status_code == 400
```

---

## Pre-Commit Checks

### Local Hook

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
echo "Running code quality checks..."

ruff check . || exit 1
mypy src || exit 1
pytest --cov=src --cov-fail-under=85 || exit 1

echo "✅ All checks passed!"
```

```bash
chmod +x .git/hooks/pre-commit
```

### IDE Integration

**VS Code**:
```json
{
  "python.linting.ruffEnabled": true,
  "python.linting.mypyEnabled": true,
  "editor.formatOnSave": true
}
```

---

## CI/CD Integration

All quality checks run automatically in GitHub Actions:

- **test.yml**: Runs tests + coverage (≥85%)
- **lint.yml**: Runs ruff + mypy
- **codeql.yml**: Security scanning

See [GitHub Actions Guide](github-actions.md) for details.

---

## Best Practices

1. **Run checks locally before pushing**
2. **Fix linting issues immediately** (don't accumulate debt)
3. **Add type hints to new code**
4. **Write tests alongside features** (not after)
5. **Review coverage reports regularly**

---

## Related Documentation

- [SAP-004: Testing Framework](../../skilled-awareness/testing-framework/)
- [SAP-005: CI/CD Workflows](../../skilled-awareness/ci-cd-workflows/)
- [SAP-006: Quality Gates](../../skilled-awareness/quality-gates/)

---

**Last Updated**: 2025-10-29
