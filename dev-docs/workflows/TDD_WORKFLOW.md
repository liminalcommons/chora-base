---
title: Test Driven Development (TDD) Workflow
type: how-to
status: current
audience: developers, ai-agents
last_updated: 2025-10-25
version: 1.0.0
---

# Test Driven Development (TDD) Workflow

**Purpose:** Write tests BEFORE implementation to drive better design and ensure comprehensive test coverage.

**Core Principle:** RED → GREEN → REFACTOR

**Evidence:** TDD produces 40-80% fewer defects and better-designed code than test-after approaches.

---

## Table of Contents

1. [Overview](#overview)
2. [When to Use TDD](#when-to-use-tdd)
3. [The RED-GREEN-REFACTOR Cycle](#the-red-green-refactor-cycle)
4. [Detailed Process](#detailed-process)
5. [Test Patterns](#test-patterns)
6. [Examples](#examples)
7. [Integration with BDD](#integration-with-bdd)
8. [Best Practices](#best-practices)
9. [Anti-Patterns](#anti-patterns)

---

## Overview

### What is TDD?

**Test Driven Development (TDD)** is a development approach where you:
1. Write a failing test (RED)
2. Write minimal code to pass the test (GREEN)
3. Improve the design while keeping tests passing (REFACTOR)

**The Cycle:**
```
RED (failing test)
    ↓
GREEN (minimal implementation)
    ↓
REFACTOR (improve design)
    ↓
Repeat for next behavior
```

### Why TDD?

**Benefits:**
- ✅ **Better Design** - Tests force you to think about interface before implementation
- ✅ **Comprehensive Coverage** - Every line has a test (by definition)
- ✅ **Fewer Defects** - 40-80% fewer bugs than test-after
- ✅ **Refactoring Confidence** - Tests catch regressions immediately
- ✅ **Living Documentation** - Tests show how code is meant to be used

**Evidence from research:**
- 40-80% defect reduction
- 15-35% increase in development time upfront
- **Net ROI:** 40-90% reduction in total development + maintenance time
- Better code modularity and design

---

## When to Use TDD

### ✅ Use TDD for:

- **Complex logic** (algorithms, calculations, validations)
- **Business-critical code** (payment processing, authentication)
- **Public APIs** (interfaces used by others)
- **Bug fixes** (write failing test, then fix)
- **Refactoring** (preserve existing behavior)

### ⚠️ Consider alternatives for:

- **UI/UX** (use BDD for user workflows)
- **Exploratory prototypes** (don't know requirements yet)
- **Simple CRUD** (trivial data operations)
- **Integration glue** (use integration tests instead)

**Rule of thumb:** If the code has logic or complexity, use TDD.

---

## The RED-GREEN-REFACTOR Cycle

### Overview

```
┌────────────────────────────────────────────────┐
│  RED: Write a Failing Test                    │
│  - Test describes desired behavior            │
│  - Test fails (function doesn't exist yet)    │
│  - Time: 5-15 minutes                         │
└────────┬───────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────────┐
│  GREEN: Make Test Pass (Minimal Code)         │
│  - Write simplest code to pass test           │
│  - Don't worry about perfection               │
│  - Time: 10-30 minutes                        │
└────────┬───────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────────┐
│  REFACTOR: Improve Design                     │
│  - Remove duplication                         │
│  - Improve naming                             │
│  - Optimize performance                       │
│  - Tests must stay GREEN                      │
│  - Time: 5-20 minutes                         │
└────────┬───────────────────────────────────────┘
         ↓
         └──→ Repeat for next behavior
```

### Time per Cycle

| Phase | Time | Output |
|-------|------|--------|
| **RED** | 5-15 min | Failing test |
| **GREEN** | 10-30 min | Passing test + minimal implementation |
| **REFACTOR** | 5-20 min | Improved design, tests still pass |
| **Total Cycle** | 20-65 min | One tested behavior |

**Per Day:** 8-15 RED-GREEN-REFACTOR cycles (depending on complexity)

---

## Detailed Process

### Phase 1: RED - Write a Failing Test (5-15 min)

#### Goal
Write a test that describes ONE behavior and fails because the behavior doesn't exist yet.

#### Process

**Step 1: Choose next behavior**
```python
# From acceptance criteria or API design
# Behavior: "validate_config returns ValidationResult for valid config"
```

**Step 2: Write test**
```python
# tests/unit/test_validation.py
import pytest
from myapp.validation import validate_config


def test_validate_config_returns_result_for_valid_input():
    """Validate config should return ValidationResult for valid input."""
    # Arrange
    config_path = "test_config.yaml"

    # Act
    result = validate_config(config_path)

    # Assert
    assert result is not None
    assert result.valid is True
    assert isinstance(result.errors, list)
    assert len(result.errors) == 0
```

**Step 3: Run test (expect FAILURE)**
```bash
pytest tests/unit/test_validation.py::test_validate_config_returns_result_for_valid_input -v

# Expected output:
# FAILED - ImportError: cannot import name 'validate_config'
# OR
# FAILED - AttributeError: 'ValidationResult' has no attribute 'valid'
```

**What This Proves:**
- ✅ Test fails for the right reason (function doesn't exist)
- ✅ Test is runnable
- ✅ You know what success looks like

#### Guidelines for RED Phase

**1. Test ONE behavior only**
```python
✅ GOOD: test_validate_config_returns_result_for_valid_input()
❌ BAD:  test_validate_config_handles_all_cases()  # Too broad
```

**2. Use Arrange-Act-Assert pattern**
```python
def test_something():
    # Arrange - Setup test data
    input_data = create_test_data()

    # Act - Perform action
    result = function_under_test(input_data)

    # Assert - Verify outcome
    assert result == expected_value
```

**3. Test interface, not implementation**
```python
✅ GOOD: assert result.valid is True
❌ BAD:  assert result._internal_state == "valid"  # Testing private state
```

---

### Phase 2: GREEN - Make Test Pass (10-30 min)

#### Goal
Write the SIMPLEST code that makes the test pass. Don't worry about perfect design yet.

#### Process

**Step 1: Create minimal implementation**
```python
# src/myapp/validation.py
from dataclasses import dataclass
from typing import List


@dataclass
class ValidationResult:
    """Result of configuration validation."""
    valid: bool
    errors: List[str]


def validate_config(config_path: str) -> ValidationResult:
    """
    Validate a configuration file.

    Args:
        config_path: Path to configuration file

    Returns:
        ValidationResult with validation status
    """
    # Minimal implementation - just return success
    return ValidationResult(valid=True, errors=[])
```

**Step 2: Run test (expect SUCCESS)**
```bash
pytest tests/unit/test_validation.py::test_validate_config_returns_result_for_valid_input -v

# Expected output:
# PASSED ✓
```

**Step 3: Run ALL tests (ensure no regression)**
```bash
pytest tests/unit/

# All tests should pass
```

#### Guidelines for GREEN Phase

**1. Write minimal code (simplest thing that passes)**
```python
✅ GOOD: return ValidationResult(valid=True, errors=[])
❌ BAD:  # Write full validation logic on first test
```

**2. Hard-code values if it makes test pass**
```python
def calculate_total(items):
    # First test: calculate_total([10, 20]) == 30
    return 30  # Hard-coded is OK for first test!
```

**3. Generalize only when you have multiple tests**
```python
def calculate_total(items):
    # After second test: calculate_total([5, 10]) == 15
    # Now generalize:
    return sum(items)
```

**4. Don't skip to perfect solution**
- Write code to pass THIS test
- REFACTOR phase will improve design
- More tests will force generalization

---

### Phase 3: REFACTOR - Improve Design (5-20 min)

#### Goal
Improve code quality while keeping all tests GREEN.

#### Process

**Step 1: Identify code smells**
- Duplication
- Long functions
- Poor naming
- Missing error handling
- Performance issues

**Step 2: Refactor**
```python
# Before refactoring
def validate_config(config_path: str) -> ValidationResult:
    return ValidationResult(valid=True, errors=[])


# After refactoring (after more tests added)
def validate_config(config_path: str) -> ValidationResult:
    """Validate configuration file against schema."""
    try:
        config = _load_config(config_path)
        errors = _validate_schema(config)
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors
        )
    except FileNotFoundError:
        return ValidationResult(
            valid=False,
            errors=[f"Configuration file not found: {config_path}"]
        )


def _load_config(config_path: str) -> dict:
    """Load configuration from file."""
    import yaml
    with open(config_path) as f:
        return yaml.safe_load(f)


def _validate_schema(config: dict) -> List[str]:
    """Validate config against schema."""
    errors = []

    if "api_key" not in config:
        errors.append("Missing required field: api_key")

    if "timeout" in config and config["timeout"] < 0:
        errors.append("timeout must be positive")

    return errors
```

**Step 3: Run tests after each change**
```bash
# After EVERY refactoring step, run tests
pytest tests/unit/test_validation.py -v

# All tests must stay GREEN
```

#### Guidelines for REFACTOR Phase

**1. Refactor frequently (after every 2-3 tests)**
```
Test 1 (RED → GREEN) → Refactor
Test 2 (RED → GREEN) → Refactor
Test 3 (RED → GREEN) → Refactor
```

**2. Extract helper functions**
```python
# Before
def validate_config(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)
    if "api_key" not in config:
        return ValidationResult(valid=False, errors=["Missing api_key"])
    # ... more validation ...


# After
def validate_config(config_path):
    config = _load_config(config_path)
    errors = _validate_required_fields(config)
    errors.extend(_validate_field_types(config))
    return ValidationResult(valid=len(errors) == 0, errors=errors)


def _load_config(config_path):
    """Load config from file."""
    with open(config_path) as f:
        return yaml.safe_load(f)


def _validate_required_fields(config):
    """Validate required fields are present."""
    errors = []
    for field in ["api_key", "environment"]:
        if field not in config:
            errors.append(f"Missing required field: {field}")
    return errors
```

**3. Remove duplication**
```python
# Before (duplication)
def test_missing_api_key():
    result = validate_config("no_api_key.yaml")
    assert result.valid is False
    assert "api_key" in result.errors[0]


def test_missing_environment():
    result = validate_config("no_environment.yaml")
    assert result.valid is False
    assert "environment" in result.errors[0]


# After (extracted helper)
def assert_validation_fails_for_missing_field(config_file, field_name):
    """Helper to test missing field validation."""
    result = validate_config(config_file)
    assert result.valid is False
    assert field_name in result.errors[0]


def test_missing_api_key():
    assert_validation_fails_for_missing_field("no_api_key.yaml", "api_key")


def test_missing_environment():
    assert_validation_fails_for_missing_field("no_environment.yaml", "environment")
```

**4. Run tests after EACH refactoring step**
```bash
# Make one change → run tests → make another change → run tests
```

---

## Test Patterns

### Pattern 1: Arrange-Act-Assert (AAA)

**Structure:**
```python
def test_something():
    # Arrange - Setup test data and dependencies
    input_data = {...}
    expected_output = {...}

    # Act - Perform the action being tested
    result = function_under_test(input_data)

    # Assert - Verify the outcome
    assert result == expected_output
```

**Example:**
```python
def test_calculate_total():
    # Arrange
    items = [
        {"price": 10.00, "quantity": 2},
        {"price": 5.00, "quantity": 3},
    ]
    expected_total = 35.00

    # Act
    result = calculate_total(items)

    # Assert
    assert result == expected_total
```

---

### Pattern 2: Given-When-Then (Alternative naming)

**Same as AAA, different names:**
```python
def test_user_login():
    # Given - initial state
    user = create_user(email="test@example.com", password="secret")

    # When - action
    result = login(email="test@example.com", password="secret")

    # Then - expected outcome
    assert result.authenticated is True
    assert result.user_id == user.id
```

---

### Pattern 3: Test Fixtures

**Setup reusable test data:**
```python
import pytest


@pytest.fixture
def sample_config():
    """Provide a sample configuration for tests."""
    return {
        "api_key": "test_key_12345",
        "environment": "test",
        "timeout": 30
    }


def test_valid_config(sample_config):
    """Test validation with valid config."""
    result = validate_config_dict(sample_config)
    assert result.valid is True


def test_config_has_api_key(sample_config):
    """Test config contains API key."""
    assert "api_key" in sample_config
    assert sample_config["api_key"] == "test_key_12345"
```

---

### Pattern 4: Parametrized Tests

**Test same logic with different inputs:**
```python
@pytest.mark.parametrize("input_value,expected", [
    (10, 20),      # 10 * 2 = 20
    (0, 0),        # 0 * 2 = 0
    (-5, -10),     # -5 * 2 = -10
    (3.5, 7.0),    # 3.5 * 2 = 7.0
])
def test_double(input_value, expected):
    """Test double function with various inputs."""
    result = double(input_value)
    assert result == expected
```

---

### Pattern 5: Exception Testing

**Test that exceptions are raised:**
```python
def test_validate_raises_error_for_missing_file():
    """Test validation raises FileNotFoundError for missing file."""
    with pytest.raises(FileNotFoundError):
        validate_config("nonexistent.yaml")


def test_validate_raises_error_with_message():
    """Test error includes helpful message."""
    with pytest.raises(ValueError, match="Invalid format"):
        validate_config("invalid.txt")
```

---

### Pattern 6: Mock External Dependencies

**Isolate unit tests from external systems:**
```python
from unittest.mock import Mock, patch


def test_fetch_user_data():
    """Test fetching user data from API."""
    # Arrange - Mock the API call
    mock_api = Mock()
    mock_api.get_user.return_value = {"id": 1, "name": "Alice"}

    # Act
    result = fetch_user_data(user_id=1, api=mock_api)

    # Assert
    assert result["name"] == "Alice"
    mock_api.get_user.assert_called_once_with(1)


@patch('myapp.external.api_client')
def test_fetch_user_data_with_patch(mock_client):
    """Test with patched dependency."""
    mock_client.get_user.return_value = {"id": 1, "name": "Bob"}

    result = fetch_user_data(user_id=1)

    assert result["name"] == "Bob"
```

---

## Examples

### Example 1: Simple Function (Calculate Total)

**Cycle 1: First Test**

**RED:**
```python
# tests/unit/test_calculator.py
def test_calculate_total_with_single_item():
    """Calculate total should sum item prices."""
    items = [{"price": 10.00, "quantity": 2}]

    result = calculate_total(items)

    assert result == 20.00


# Run: pytest tests/unit/test_calculator.py -v
# FAILED - ImportError: cannot import 'calculate_total'
```

**GREEN:**
```python
# src/myapp/calculator.py
def calculate_total(items):
    """Calculate total price of items."""
    # Minimal implementation for first test
    return 20.00


# Run: pytest tests/unit/test_calculator.py -v
# PASSED ✓
```

**REFACTOR:**
```python
# No refactoring needed yet (too simple)
```

---

**Cycle 2: Second Test (Forces Generalization)**

**RED:**
```python
def test_calculate_total_with_multiple_items():
    """Calculate total with multiple different items."""
    items = [
        {"price": 10.00, "quantity": 2},
        {"price": 5.00, "quantity": 3},
    ]

    result = calculate_total(items)

    assert result == 35.00


# Run: pytest tests/unit/test_calculator.py -v
# FAILED - AssertionError: assert 20.0 == 35.0
```

**GREEN:**
```python
def calculate_total(items):
    """Calculate total price of items."""
    total = 0.0
    for item in items:
        total += item["price"] * item["quantity"]
    return total


# Run: pytest tests/unit/test_calculator.py -v
# PASSED ✓ (both tests pass)
```

**REFACTOR:**
```python
def calculate_total(items):
    """Calculate total price of items."""
    return sum(item["price"] * item["quantity"] for item in items)


# Run: pytest tests/unit/test_calculator.py -v
# PASSED ✓ (still passes after refactoring)
```

---

**Cycle 3: Edge Case**

**RED:**
```python
def test_calculate_total_with_empty_list():
    """Calculate total with no items should return 0."""
    items = []

    result = calculate_total(items)

    assert result == 0.0


# Run: pytest tests/unit/test_calculator.py -v
# PASSED ✓ (our implementation already handles this!)
```

**GREEN:**
```python
# No changes needed - already passes
```

**REFACTOR:**
```python
# Add type hints and docstring
from typing import List, Dict


def calculate_total(items: List[Dict[str, float]]) -> float:
    """
    Calculate total price of items.

    Args:
        items: List of items with 'price' and 'quantity' keys

    Returns:
        Total price (sum of price * quantity for all items)

    Examples:
        >>> calculate_total([{"price": 10, "quantity": 2}])
        20.0
    """
    return sum(item["price"] * item["quantity"] for item in items)
```

---

### Example 2: Complex Class (BackendRegistry)

**Cycle 1: Registration**

**RED:**
```python
# tests/unit/test_backend_registry.py
import pytest
from myapp.gateway import BackendRegistry, BackendConfig


def test_register_backend_stores_backend():
    """Registry should store registered backend."""
    registry = BackendRegistry()
    config = BackendConfig(name="test", namespace="test", type="mock")

    registry.register(config)

    assert len(registry._backends) == 1
    assert "test" in registry._backends


# FAILED - ImportError: cannot import 'BackendRegistry'
```

**GREEN:**
```python
# src/myapp/gateway.py
from dataclasses import dataclass
from typing import Dict


@dataclass
class BackendConfig:
    name: str
    namespace: str
    type: str


class BackendRegistry:
    def __init__(self):
        self._backends: Dict[str, BackendConfig] = {}

    def register(self, config: BackendConfig) -> None:
        self._backends[config.namespace] = config


# PASSED ✓
```

**REFACTOR:**
```python
# No refactoring yet
```

---

**Cycle 2: Tool Routing**

**RED:**
```python
def test_route_tool_call_to_correct_backend():
    """Route tool call to backend by namespace."""
    registry = BackendRegistry()
    config = BackendConfig(name="chora", namespace="chora", type="mock")
    registry.register(config)

    result = registry.route_tool_call("chora:assemble_artifact")

    assert result is not None
    assert result[0].namespace == "chora"
    assert result[1] == "assemble_artifact"


# FAILED - AttributeError: 'BackendRegistry' has no attribute 'route_tool_call'
```

**GREEN:**
```python
from typing import Optional, Tuple


class BackendRegistry:
    def __init__(self):
        self._backends: Dict[str, BackendConfig] = {}

    def register(self, config: BackendConfig) -> None:
        self._backends[config.namespace] = config

    def route_tool_call(
        self,
        tool_name: str
    ) -> Optional[Tuple[BackendConfig, str]]:
        """Route namespaced tool to backend."""
        parts = tool_name.split(":", 1)
        if len(parts) != 2:
            return None

        namespace, tool = parts
        backend = self._backends.get(namespace)

        if backend is None:
            return None

        return (backend, tool)


# PASSED ✓
```

**REFACTOR:**
```python
# Extract parsing logic
def route_tool_call(self, tool_name: str) -> Optional[Tuple[BackendConfig, str]]:
    """Route namespaced tool call to backend."""
    namespace, tool = self._parse_tool_name(tool_name)
    if namespace is None:
        return None

    backend = self._find_backend(namespace)
    if backend is None:
        return None

    return (backend, tool)


def _parse_tool_name(self, tool_name: str) -> Tuple[Optional[str], Optional[str]]:
    """Parse namespace and tool from namespaced string."""
    parts = tool_name.split(":", 1)
    if len(parts) != 2:
        return (None, None)
    return tuple(parts)


def _find_backend(self, namespace: str) -> Optional[BackendConfig]:
    """Find backend by namespace."""
    return self._backends.get(namespace)


# PASSED ✓ (tests still pass after refactoring)
```

---

## Integration with BDD

### How TDD and BDD Work Together

```
BDD (Acceptance Tests)
├─ Feature file: "User validates configuration"
├─ Step definitions (integration-level tests)
└─ Run (RED - all fail because feature not implemented)
    ↓
TDD (Unit Tests) ← Drive implementation
├─ Test 1: validate_config returns result (RED → GREEN → REFACTOR)
├─ Test 2: validate_config detects missing fields (RED → GREEN → REFACTOR)
├─ Test 3: validate_config handles file errors (RED → GREEN → REFACTOR)
└─ ... (continue until BDD scenarios pass)
    ↓
BDD Scenarios
└─ Run (GREEN - all pass because feature is implemented)
```

### Decision Tree

**What to test where:**

```
User-facing behavior?
├─ YES → BDD (Feature files + Step definitions)
│         Example: "User validates config and sees success message"
│
└─ NO → Is it internal logic?
          ├─ YES → TDD (Unit tests)
          │         Example: "parse_yaml returns dict"
          │
          └─ NO → Integration between systems?
                    └─ Integration Tests
                      Example: "Database stores config"
```

---

## Best Practices

### 1. Write Smallest Possible Test

**✅ GOOD:**
```python
def test_add_returns_sum():
    assert add(2, 3) == 5
```

**❌ BAD:**
```python
def test_calculator_does_everything():
    assert add(2, 3) == 5
    assert subtract(5, 2) == 3
    assert multiply(2, 3) == 6
    assert divide(6, 2) == 3
    # Too many behaviors in one test
```

---

### 2. One Assert Per Test (Generally)

**✅ GOOD:**
```python
def test_validation_returns_result():
    result = validate_config("test.yaml")
    assert isinstance(result, ValidationResult)


def test_validation_result_has_valid_field():
    result = validate_config("test.yaml")
    assert hasattr(result, 'valid')
```

**⚠️ ACCEPTABLE (Related Assertions):**
```python
def test_validation_result_structure():
    """Test ValidationResult has correct structure."""
    result = validate_config("test.yaml")
    assert result.valid is True
    assert result.errors == []
    assert result.warnings == []
    # OK because testing one concept: "result structure"
```

---

### 3. Test Behavior, Not Implementation

**✅ GOOD:**
```python
def test_user_can_login():
    result = authenticate(email="test@example.com", password="secret")
    assert result.authenticated is True
```

**❌ BAD:**
```python
def test_authentication_uses_bcrypt():
    # Don't test how it works (implementation)
    assert authentication_module.hash_algorithm == "bcrypt"
```

---

### 4. Keep Tests Independent

**✅ GOOD:**
```python
def test_create_user():
    user = create_user(name="Alice")
    assert user.name == "Alice"


def test_delete_user():
    user = create_user(name="Bob")
    delete_user(user.id)
    assert user_exists(user.id) is False
```

**❌ BAD:**
```python
# Global state shared between tests
created_user = None


def test_create_user():
    global created_user
    created_user = create_user(name="Alice")


def test_delete_user():
    # Depends on test_create_user running first
    delete_user(created_user.id)
```

---

### 5. Use Descriptive Test Names

**✅ GOOD:**
```python
def test_validate_config_raises_error_for_missing_file():
    """Clear what's being tested and expected outcome."""
    pass


def test_calculate_total_returns_zero_for_empty_list():
    pass
```

**❌ BAD:**
```python
def test_1():
    pass


def test_validation():
    pass
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Writing Tests After Code

**Problem:**
```python
# 1. Write implementation
def calculate_total(items):
    return sum(item["price"] * item["quantity"] for item in items)


# 2. Write tests that match implementation
def test_calculate_total():
    # Test just documents what code does, doesn't drive design
    assert calculate_total([{"price": 10, "quantity": 2}]) == 20
```

**Solution:**
```python
# 1. Write test FIRST (RED)
def test_calculate_total():
    assert calculate_total([{"price": 10, "quantity": 2}]) == 20


# 2. Implement to pass test (GREEN)
def calculate_total(items):
    return sum(item["price"] * item["quantity"] for item in items)
```

---

### ❌ Anti-Pattern 2: Skipping RED Phase

**Problem:**
```python
# Write test and implementation at same time
# Never see test fail
```

**Solution:**
```python
# Always see test fail BEFORE writing implementation
# Proves test is actually testing something
```

---

### ❌ Anti-Pattern 3: Skipping REFACTOR Phase

**Problem:**
```python
# Test 1 (RED → GREEN) → immediately write Test 2
# Code becomes messy, duplicated, hard to maintain
```

**Solution:**
```python
# Test 1 (RED → GREEN → REFACTOR) → Test 2 (RED → GREEN → REFACTOR)
# Keep code clean after every test
```

---

### ❌ Anti-Pattern 4: Testing Private Methods

**Problem:**
```python
def test_internal_helper():
    result = object._private_method()  # Testing implementation detail
    assert result == expected
```

**Solution:**
```python
def test_public_behavior():
    result = object.public_method()  # Test public API
    assert result == expected
    # Private method tested indirectly
```

---

### ❌ Anti-Pattern 5: Overly Complex Tests

**Problem:**
```python
def test_everything():
    # 50 lines of setup
    # Complex mocking
    # Assertions on internal state
    # If test breaks, hard to know why
```

**Solution:**
```python
def test_one_simple_behavior():
    # 3-5 lines of setup
    result = function(input)
    assert result == expected
```

---

## Summary

**TDD in 3 Steps:**
1. **RED** (5-15 min) - Write failing test
2. **GREEN** (10-30 min) - Write minimal code to pass
3. **REFACTOR** (5-20 min) - Improve design, keep tests passing

**Key Principles:**
- ✅ Write test BEFORE implementation
- ✅ Write simplest code to pass test
- ✅ Refactor after every 2-3 tests
- ✅ Run tests after every change
- ✅ Keep tests independent and focused

**Integration with BDD:**
- BDD defines WHAT (user-facing behavior)
- TDD defines HOW (internal implementation)
- BDD scenarios drive TDD cycles

**Evidence:**
- 40-80% fewer defects
- Better code design
- Higher test coverage
- Faster debugging (tests pinpoint issues)

---

## Related Documentation

- [DEVELOPMENT_PROCESS.md](DEVELOPMENT_PROCESS.md) - Phase 4: Development
- [BDD_WORKFLOW.md](BDD_WORKFLOW.md) - Write acceptance tests first
- [DDD_WORKFLOW.md](DDD_WORKFLOW.md) - Design API before implementing
- [DEVELOPMENT_LIFECYCLE.md](DEVELOPMENT_LIFECYCLE.md) - How DDD→BDD→TDD integrate

---

**Version:** 1.0.0
**Created:** 2025-10-25
**Last Updated:** 2025-10-25
**Maintained By:** Project team
**Next Review:** Quarterly
