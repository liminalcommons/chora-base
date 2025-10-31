# Understanding Metrics

**Audience**: Developers tracking project health
**Related**: [SAP-013: Metrics Tracking](../../skilled-awareness/metrics-tracking/)

---

## Overview

Chora-base projects track key metrics to monitor:
- Code quality (coverage, linting)
- Test performance (speed, reliability)
- Development velocity (commits, PRs)
- Project health (technical debt, dependencies)

---

## Code Quality Metrics

### Test Coverage

**What it measures**: Percentage of code executed by tests

**Target**: ≥85%

**Check coverage**:
```bash
pytest --cov=src --cov-report=term
```

**Interpretation**:
- 90-100%: Excellent
- 85-90%: Good (chora-base target)
- 70-85%: Acceptable
- <70%: Needs improvement

### Linting Issues

**What it measures**: Code style and quality violations

**Target**: 0 violations

**Check issues**:
```bash
ruff check .
```

**Common categories**:
- **E**: PEP 8 style errors
- **F**: Pyflakes errors (undefined names, unused imports)
- **I**: Import sorting issues
- **C**: McCabe complexity

### Type Coverage

**What it measures**: Percentage of functions with type hints

**Target**: 100% for public APIs

**Check type coverage**:
```bash
mypy src --strict
```

---

## Test Performance Metrics

### Test Execution Time

**Target**: <30 seconds for unit tests

**Measure**:
```bash
pytest --durations=10  # Show 10 slowest tests
```

**Optimization strategies**:
- Mock external calls
- Use fixtures efficiently
- Parallelize with `pytest-xdist`

### Test Flakiness

**What it measures**: Tests that intermittently fail

**Target**: 0 flaky tests

**Detect flaky tests**:
```bash
pytest --count=10 tests/test_api.py  # Run 10 times
```

**Common causes**:
- Race conditions
- Time-dependent logic
- External dependencies

---

## Development Velocity Metrics

### Commit Frequency

**Healthy pattern**: Regular, small commits

**Check**:
```bash
git log --oneline --since="1 week ago" | wc -l
```

### Pull Request Metrics

**Metrics to track**:
- Time to merge (target: <24 hours)
- PR size (target: <500 lines)
- Review cycles (target: 1-2 cycles)

### Code Churn

**What it measures**: Code added + deleted

**High churn indicators**:
- Frequent rewrites
- Unclear requirements
- Technical debt

---

## Project Health Metrics

### Dependency Freshness

**Check outdated dependencies**:
```bash
pip list --outdated
```

**Update dependencies**:
```bash
pip install --upgrade <package>
```

### Security Vulnerabilities

**Check vulnerabilities**:
```bash
# Via GitHub Dependabot (automatic)
# View: GitHub → Security → Dependabot alerts
```

### Documentation Coverage

**Metrics**:
- % of functions with docstrings
- % of modules with documentation
- 0 broken links (target)

**Check docstrings**:
```bash
pydocstyle src/
```

---

## Tracking Metrics

### Local Dashboard

Create `scripts/metrics.py`:
```python
#!/usr/bin/env python3
"""Display project metrics."""

import subprocess

def get_coverage():
    result = subprocess.run(
        ["pytest", "--cov=src", "--cov-report=term"],
        capture_output=True, text=True
    )
    # Parse coverage from output
    return "94%"  # Example

def get_lint_issues():
    result = subprocess.run(
        ["ruff", "check", "."],
        capture_output=True, text=True
    )
    return len(result.stdout.split("\n")) - 1

def main():
    print("Project Metrics")
    print("=" * 40)
    print(f"Coverage:      {get_coverage()}")
    print(f"Lint Issues:   {get_lint_issues()}")
    print(f"Type Coverage: 95%")  # From mypy

if __name__ == "__main__":
    main()
```

### CI/CD Tracking

GitHub Actions automatically tracks:
- Test pass rate
- Coverage trends
- Build times
- Deployment frequency

View in: Actions tab → Workflow runs → Insights

---

## Setting Goals

### Code Quality Goals (3 months)

```markdown
- [ ] Increase coverage from 85% to 90%
- [ ] Reduce lint issues from 50 to 0
- [ ] Add type hints to all public APIs
```

### Performance Goals

```markdown
- [ ] Reduce test execution time from 2min to 1min
- [ ] Eliminate all flaky tests (currently 3)
```

### Process Goals

```markdown
- [ ] Reduce PR merge time from 48h to 24h
- [ ] Increase commit frequency from 5/week to 10/week
```

---

## Best Practices

1. **Track trends, not just current values**
2. **Set realistic targets** (don't aim for 100% coverage on legacy code)
3. **Automate tracking** (use CI/CD, not manual checks)
4. **Review metrics weekly**
5. **Celebrate improvements**

---

## Related Documentation

- [SAP-013: Metrics Tracking](../../skilled-awareness/metrics-tracking/)
- [SAP-004: Testing Framework](../../skilled-awareness/testing-framework/)
- [SAP-006: Quality Gates](../../skilled-awareness/quality-gates/)
- [Code Quality Guide](code-quality.md)

---

**Last Updated**: 2025-10-29
