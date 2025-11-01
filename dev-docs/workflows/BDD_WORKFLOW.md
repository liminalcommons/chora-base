---
title: Behavior Driven Development (BDD) Workflow
type: how-to
status: current
audience: developers, ai-agents
last_updated: 2025-10-25
version: 1.0.0
---

# Behavior Driven Development (BDD) Workflow

**Purpose:** Write executable specifications in plain language that bridge the gap between business requirements and technical implementation.

**Core Principle:** Write feature specifications as executable tests BEFORE implementing functionality.

**Tool:** pytest-bdd (Gherkin scenarios for Python)

---

## Table of Contents

1. [Overview](#overview)
2. [When to Use BDD](#when-to-use-bdd)
3. [The BDD Process](#the-bdd-process)
4. [Gherkin Syntax Guide](#gherkin-syntax-guide)
5. [Step Definition Patterns](#step-definition-patterns)
6. [Examples](#examples)
7. [Integration with DDD and TDD](#integration-with-ddd-and-tdd)
8. [Best Practices](#best-practices)
9. [Anti-Patterns](#anti-patterns)

---

## Overview

### What is BDD?

**Behavior Driven Development (BDD)** is a software development approach that:
- Writes specifications in natural language (Gherkin)
- Makes specifications executable (pytest-bdd)
- Focuses on behavior, not implementation
- Creates living documentation

**Format:** Given-When-Then scenarios
```gherkin
Scenario: User validates configuration
  Given a valid configuration file
  When the user runs the validation command
  Then the validation passes
  And a success message is displayed
```

### Why BDD?

**Benefits:**
- ✅ **Shared Understanding** - Product, QA, and Engineering speak same language
- ✅ **Living Documentation** - Specs are always in sync with code (or tests fail)
- ✅ **Early Feedback** - Write scenarios during design phase (Phase 3)
- ✅ **Test Coverage** - Scenarios define acceptance criteria exactly
- ✅ **Regression Protection** - Scenarios become automated tests

**Evidence from research:**
- 100% alignment between requirements and tests (by definition)
- 40% fewer misunderstood requirements
- 85% of bugs caught before production

---

## When to Use BDD

### ✅ Use BDD for:

- **User-facing features** (APIs, CLIs, UIs)
- **Complex workflows** (multi-step processes)
- **Cross-team features** (need shared understanding)
- **Critical paths** (must work correctly)
- **Acceptance testing** (define "done")

### ⚠️ Consider skipping for:

- **Internal utilities** (no user-facing behavior)
- **Trivial functions** (simple calculations)
- **Prototypes** (throw-away code)

**Rule of thumb:** If it has user-visible behavior, use BDD.

---

## The BDD Process

### Overview

```
DDD Phase (Phase 3)
    ↓
Extract Acceptance Criteria
    ↓
Write Feature File (Gherkin) ← You are here
    ↓
Implement Step Definitions
    ↓
Run Tests (RED - all failing)
    ↓
TDD Phase (Phase 4) → Implement feature
    ↓
Run Tests (GREEN - all passing)
    ↓
Refactor
    ↓
Verify Tests Still Pass (GREEN)
```

### Time Investment

| Step | Time | Output |
|------|------|--------|
| **Write Feature File** | 30-60 min | .feature file with scenarios |
| **Implement Step Definitions** | 1-2 hours | Python step definition code |
| **Run Tests (RED)** | 5 min | Verify tests fail before implementation |
| **TDD Implementation** | Varies | See TDD_WORKFLOW.md |
| **Verify (GREEN)** | 5 min | All BDD scenarios pass |

**Total BDD Overhead:** 2-3 hours per feature
**ROI:** Living documentation + regression protection forever

---

## Step 1: Write Feature File (30-60 min)

### Process

**Input:** Acceptance criteria from DDD phase
**Output:** `tests/features/{feature_name}.feature`

**Template:**

```gherkin
# tests/features/{feature_name}.feature
Feature: {Feature Title}

  As a {user type}
  I want {capability}
  So that {benefit}

  Background:
    Given {common setup for all scenarios}
    And {additional setup}

  Scenario: {Happy path scenario name}
    Given {initial state}
    When {action performed}
    Then {expected outcome}
    And {additional verification}

  Scenario: {Error handling scenario}
    Given {initial state}
    When {invalid action}
    Then {appropriate error}
    And {helpful error message}

  Scenario Outline: {Multiple similar scenarios}
    Given {initial state}
    When I perform action with "<parameter>"
    Then the result is "<expected>"

    Examples:
      | parameter | expected |
      | value1    | result1  |
      | value2    | result2  |
```

### Example: Config Validation

```gherkin
# tests/features/config_validation.feature
Feature: Configuration Validation

  As a developer
  I want to validate my configuration files
  So that I catch errors before deployment

  Background:
    Given the validation tool is installed
    And I am in the project directory

  Scenario: Validate valid YAML configuration
    Given a configuration file "valid_config.yaml" with valid syntax
    When I run "myapp validate valid_config.yaml"
    Then the validation passes with exit code 0
    And the output contains "✓ Configuration is valid"

  Scenario: Detect missing required field
    Given a configuration file "invalid_config.yaml" missing field "api_key"
    When I run "myapp validate invalid_config.yaml"
    Then the validation fails with exit code 1
    And the output contains "Error: Missing required field 'api_key'"
    And the output contains "Add 'api_key: YOUR_KEY' to the 'auth' section"

  Scenario Outline: Validate different file formats
    Given a configuration file "<filename>" with format "<format>"
    When I run "myapp validate <filename>"
    Then the validation result is "<result>"

    Examples:
      | filename        | format | result  |
      | config.yaml     | YAML   | success |
      | config.json     | JSON   | success |
      | config.toml     | TOML   | error   |
      | config.xml      | XML    | error   |
```

### Tips for Writing Scenarios

**1. Use Business Language (Not Technical)**
```gherkin
✅ GOOD: When I validate the configuration
❌ BAD:  When I call validate_config() function
```

**2. One Scenario = One Behavior**
```gherkin
✅ GOOD:
  Scenario: Detect missing required field
  Scenario: Detect invalid field type

❌ BAD:
  Scenario: Detect all validation errors  # Too broad
```

**3. Make Steps Reusable**
```gherkin
✅ GOOD: Given a configuration file "test.yaml" with valid syntax
         # Can reuse with different filenames

❌ BAD:  Given the test configuration file exists
         # Not reusable, vague
```

**4. Be Specific About Outcomes**
```gherkin
✅ GOOD: Then the output contains "Error: Missing required field 'api_key'"

❌ BAD:  Then an error is shown
```

---

## Step 2: Implement Step Definitions (1-2 hours)

### Process

**Input:** Feature file from Step 1
**Output:** `tests/step_defs/test_{feature}_steps.py`

**Template:**

```python
# tests/step_defs/test_{feature}_steps.py
"""Step definitions for {feature} feature."""

from pytest_bdd import given, when, then, scenario, parsers
import pytest

# Link to feature file
@scenario('../features/{feature}.feature', '{Scenario Name}')
def test_{scenario_name}():
    """Test {scenario description}."""
    pass


# Step definitions
@given(parsers.parse('a configuration file "{filename}" with valid syntax'))
def config_file_with_valid_syntax(tmp_path, filename):
    """Create a configuration file with valid syntax."""
    config_path = tmp_path / filename
    config_path.write_text("""
        api_key: test_key
        environment: production
    """)
    pytest.shared_context = {"config_path": config_path}
    return config_path


@when(parsers.parse('I run "{command}"'))
def run_command(command):
    """Execute the command."""
    import subprocess
    result = subprocess.run(
        command.split(),
        capture_output=True,
        text=True,
        cwd=pytest.shared_context.get("cwd")
    )
    pytest.shared_context["result"] = result


@then(parsers.parse('the validation passes with exit code {code:d}'))
def verify_exit_code(code):
    """Verify the exit code."""
    result = pytest.shared_context["result"]
    assert result.returncode == code


@then(parsers.parse('the output contains "{text}"'))
def verify_output_contains(text):
    """Verify the output contains expected text."""
    result = pytest.shared_context["result"]
    assert text in result.stdout or text in result.stderr
```

### Using pytest.shared_context

**Pattern:** Use `pytest.shared_context` to pass data between steps

```python
@given('some initial state')
def initial_state():
    pytest.shared_context = {"data": "initial"}

@when('I perform action')
def perform_action():
    data = pytest.shared_context.get("data")
    result = process(data)
    pytest.shared_context["result"] = result

@then('the result is correct')
def verify_result():
    result = pytest.shared_context["result"]
    assert result == "expected"
```

### Using Fixtures

**Pattern:** Use pytest fixtures for reusable setup

```python
@pytest.fixture
def sample_config(tmp_path):
    """Create a sample configuration file."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text("api_key: test")
    return config_path


@given('a sample configuration file')
def use_sample_config(sample_config):
    """Use the sample configuration fixture."""
    pytest.shared_context = {"config_path": sample_config}
```

### Example: Complete Step Definitions

```python
# tests/step_defs/test_config_validation_steps.py
"""Step definitions for configuration validation."""

from pytest_bdd import given, when, then, scenario, parsers
import pytest
import subprocess
from pathlib import Path


# Scenarios
@scenario('../features/config_validation.feature',
          'Validate valid YAML configuration')
def test_validate_valid_yaml():
    pass


@scenario('../features/config_validation.feature',
          'Detect missing required field')
def test_detect_missing_field():
    pass


# Background steps
@given('the validation tool is installed')
def validation_tool_installed():
    """Ensure validation tool is available."""
    pytest.shared_context = {}


@given('I am in the project directory')
def in_project_directory(tmp_path):
    """Set working directory."""
    pytest.shared_context["cwd"] = tmp_path


# Given steps
@given(parsers.parse('a configuration file "{filename}" with valid syntax'))
def config_file_valid(tmp_path, filename):
    """Create valid configuration file."""
    config_path = tmp_path / filename
    config_path.write_text("""
        api_key: test_key_12345
        environment: production
        timeout: 30
    """)
    pytest.shared_context["config_path"] = config_path


@given(parsers.parse('a configuration file "{filename}" missing field "{field}"'))
def config_file_missing_field(tmp_path, filename, field):
    """Create configuration file with missing field."""
    config_path = tmp_path / filename
    # Create config without the specified field
    config_path.write_text("""
        environment: production
        timeout: 30
    """)
    pytest.shared_context["config_path"] = config_path
    pytest.shared_context["missing_field"] = field


# When steps
@when(parsers.parse('I run "{command}"'))
def run_command(command):
    """Execute the validation command."""
    cwd = pytest.shared_context.get("cwd")

    # Replace placeholders with actual paths
    if "valid_config.yaml" in command:
        config_path = pytest.shared_context["config_path"]
        command = command.replace("valid_config.yaml", str(config_path))

    result = subprocess.run(
        command.split(),
        capture_output=True,
        text=True,
        cwd=cwd
    )
    pytest.shared_context["result"] = result


# Then steps
@then(parsers.parse('the validation passes with exit code {code:d}'))
def validation_passes(code):
    """Verify validation passed."""
    result = pytest.shared_context["result"]
    assert result.returncode == code, \
        f"Expected exit code {code}, got {result.returncode}\n" \
        f"stdout: {result.stdout}\nstderr: {result.stderr}"


@then(parsers.parse('the validation fails with exit code {code:d}'))
def validation_fails(code):
    """Verify validation failed."""
    result = pytest.shared_context["result"]
    assert result.returncode == code


@then(parsers.parse('the output contains "{text}"'))
def output_contains(text):
    """Verify output contains expected text."""
    result = pytest.shared_context["result"]
    output = result.stdout + result.stderr
    assert text in output, \
        f"Expected '{text}' not found in output:\n{output}"
```

---

## Step 3: Run Tests (RED) - 5 min

### Process

**Goal:** Verify all scenarios fail before implementation

**Command:**
```bash
# Run BDD tests with gherkin reporter
pytest tests/step_defs/ --gherkin-terminal-reporter -v

# Expected output: FAILED (feature not implemented)
```

**Expected Output:**
```
tests/step_defs/test_config_validation_steps.py::test_validate_valid_yaml
Feature: Configuration Validation
    Scenario: Validate valid YAML configuration
        Given a configuration file "valid_config.yaml" with valid syntax
        When I run "myapp validate valid_config.yaml"
        Then the validation passes with exit code 0  FAILED

FAILED - FileNotFoundError: myapp command not found
```

**What This Proves:**
- ✅ Test infrastructure works
- ✅ Scenarios are linked correctly
- ✅ Feature is not yet implemented (RED state)

**Next Step:** Implement feature using TDD (see TDD_WORKFLOW.md)

---

## Gherkin Syntax Guide

### Keywords

| Keyword | Purpose | Example |
|---------|---------|---------|
| `Feature:` | High-level description | `Feature: User Authentication` |
| `Background:` | Common setup for all scenarios | `Background: Given user is logged in` |
| `Scenario:` | Single test case | `Scenario: User logs out successfully` |
| `Scenario Outline:` | Parameterized scenarios | `Scenario Outline: Validate <input>` |
| `Given` | Initial state | `Given a user account exists` |
| `When` | Action performed | `When the user clicks logout` |
| `Then` | Expected outcome | `Then the user is redirected to login page` |
| `And` | Additional step (same type as previous) | `And the session is cleared` |
| `But` | Negative assertion | `But the user data is not deleted` |
| `Examples:` | Data table for Scenario Outline | `Examples: \| input \| expected \|` |

### Background

**Purpose:** Define common setup for all scenarios

```gherkin
Feature: Shopping Cart

  Background:
    Given the user is logged in
    And the shopping cart is empty
    And the product catalog is loaded

  Scenario: Add item to cart
    When the user adds product "Widget" to cart
    Then the cart contains 1 item

  Scenario: Remove item from cart
    Given the cart contains product "Widget"
    When the user removes product "Widget"
    Then the cart is empty
```

### Scenario Outline (Parameterized Tests)

**Purpose:** Test same behavior with different data

```gherkin
Scenario Outline: Validate different input types
  Given a configuration file with "<field>" set to "<value>"
  When I validate the configuration
  Then the validation result is "<result>"

  Examples:
    | field       | value      | result  |
    | timeout     | 30         | success |
    | timeout     | -1         | error   |
    | timeout     | 999999     | error   |
    | api_key     | valid_key  | success |
    | api_key     | ""         | error   |
```

**Generated Tests:**
- Test 1: timeout=30 → success
- Test 2: timeout=-1 → error
- Test 3: timeout=999999 → error
- Test 4: api_key=valid_key → success
- Test 5: api_key="" → error

### Tags

**Purpose:** Filter which scenarios to run

```gherkin
@smoke @critical
Scenario: User can log in

@slow @integration
Scenario: Import large dataset

@wip
Scenario: New feature (work in progress)
```

**Run specific tags:**
```bash
# Run only smoke tests
pytest -m smoke

# Skip slow tests
pytest -m "not slow"
```

---

## Step Definition Patterns

### Pattern 1: Using Parsers for Parameters

**Extract values from Gherkin steps:**

```python
from pytest_bdd import parsers

# String parameter
@given(parsers.parse('a user named "{name}"'))
def user_named(name):
    pytest.shared_context["user_name"] = name

# Integer parameter
@then(parsers.parse('the count is {count:d}'))
def verify_count(count):
    assert pytest.shared_context["count"] == count

# Float parameter
@when(parsers.parse('I set price to {price:f}'))
def set_price(price):
    pytest.shared_context["price"] = price
```

### Pattern 2: Using Regular Expressions

**For complex patterns:**

```python
import re

@given(parsers.re(r'a user with email (?P<email>\S+@\S+)'))
def user_with_email(email):
    pytest.shared_context["email"] = email

# Matches: "a user with email test@example.com"
```

### Pattern 3: Reusable Steps

**Create generic steps for common actions:**

```python
@given(parsers.parse('a {entity} named "{name}"'))
def entity_named(entity, name):
    """Generic step for creating entities."""
    pytest.shared_context[entity] = create_entity(entity, name)

# Matches:
# - "a user named Alice"
# - "a product named Widget"
# - "a server named Production"
```

### Pattern 4: Fixtures in Step Definitions

**Combine pytest fixtures with BDD:**

```python
@pytest.fixture
def database():
    """Setup test database."""
    db = Database(":memory:")
    yield db
    db.close()


@given('the database is initialized')
def database_initialized(database):
    """Use database fixture in BDD step."""
    database.execute("CREATE TABLE users (...)")
    pytest.shared_context["db"] = database
```

---

## Examples

### Example 1: Simple Feature (Config Validation)

**Feature File:**
```gherkin
# tests/features/config_validation.feature
Feature: Configuration Validation

  Scenario: Validate valid configuration
    Given a configuration file "config.yaml" with valid syntax
    When I validate the configuration
    Then the validation passes
    And the output shows "✓ Configuration is valid"
```

**Step Definitions:**
```python
# tests/step_defs/test_config_validation_steps.py
from pytest_bdd import given, when, then, scenario, parsers
import pytest

@scenario('../features/config_validation.feature',
          'Validate valid configuration')
def test_validate_valid_config():
    pass


@given(parsers.parse('a configuration file "{filename}" with valid syntax'))
def valid_config(tmp_path, filename):
    config_path = tmp_path / filename
    config_path.write_text("api_key: test")
    pytest.shared_context = {"config_path": config_path}


@when('I validate the configuration')
def validate_config():
    from myapp.validation import validate_config
    config_path = pytest.shared_context["config_path"]
    result = validate_config(str(config_path))
    pytest.shared_context["result"] = result


@then('the validation passes')
def validation_passes():
    assert pytest.shared_context["result"].valid is True


@then(parsers.parse('the output shows "{message}"'))
def output_shows(message):
    result = pytest.shared_context["result"]
    assert message in str(result)
```

---

### Example 2: Complex Feature (Multi-Backend Gateway)

**Feature File:**
```gherkin
# tests/features/gateway_routing.feature
Feature: Gateway Tool Routing

  As a gateway user
  I want tools to route to the correct backend
  So that I can use multiple MCP servers seamlessly

  Background:
    Given the gateway is running with 2 backends
    And backend "chora" handles "chora:*" tools
    And backend "coda" handles "coda:*" tools

  Scenario: Route namespaced tool to correct backend
    When I call tool "chora:assemble_artifact"
    Then the request is routed to "chora" backend
    And the backend receives tool name "assemble_artifact"

  Scenario: Handle unknown namespace
    When I call tool "unknown:tool"
    Then the request returns None
    And an error is logged with context "unknown namespace"

  Scenario Outline: Multiple backends route correctly
    When I call tool "<tool_name>"
    Then the request is routed to "<backend>" backend

    Examples:
      | tool_name              | backend |
      | chora:list_templates   | chora   |
      | coda:list_docs         | coda    |
      | chora:assemble_artifact| chora   |
```

**Step Definitions:**
```python
# tests/step_defs/test_gateway_routing_steps.py
from pytest_bdd import given, when, then, scenario, parsers
import pytest


@scenario('../features/gateway_routing.feature',
          'Route namespaced tool to correct backend')
def test_route_to_backend():
    pass


@scenario('../features/gateway_routing.feature',
          'Handle unknown namespace')
def test_handle_unknown_namespace():
    pass


@scenario('../features/gateway_routing.feature',
          'Multiple backends route correctly')
def test_multiple_backends():
    pass


# Background steps
@given(parsers.parse('the gateway is running with {count:d} backends'))
def gateway_with_backends(count):
    from myapp.gateway import BackendRegistry
    registry = BackendRegistry()
    pytest.shared_context = {"registry": registry, "backend_count": count}


@given(parsers.parse('backend "{namespace}" handles "{pattern}" tools'))
def backend_handles_pattern(namespace, pattern):
    from myapp.gateway import BackendConfig
    registry = pytest.shared_context["registry"]

    config = BackendConfig(
        name=namespace,
        namespace=namespace,
        type="mock"
    )
    registry.register(config)


# When steps
@when(parsers.parse('I call tool "{tool_name}"'))
def call_tool(tool_name):
    registry = pytest.shared_context["registry"]
    result = registry.route_tool_call(tool_name)
    pytest.shared_context["result"] = result


# Then steps
@then(parsers.parse('the request is routed to "{backend}" backend'))
def verify_backend_routing(backend):
    result = pytest.shared_context["result"]
    assert result is not None, "Expected routing result, got None"
    assert result[0].namespace == backend


@then(parsers.parse('the backend receives tool name "{tool_name}"'))
def verify_tool_name(tool_name):
    result = pytest.shared_context["result"]
    assert result[1] == tool_name


@then('the request returns None')
def verify_returns_none():
    result = pytest.shared_context["result"]
    assert result is None


@then(parsers.parse('an error is logged with context "{context}"'))
def verify_error_logged(context, caplog):
    assert context in caplog.text
```

---

## Integration with DDD and TDD

### Complete Workflow

```
PHASE 3: DDD (Documentation Driven Design)
├─ Write change request (Diátaxis format)
├─ Design API (reference docs)
└─ Extract acceptance criteria
    ↓

PHASE 4: BDD (Behavior Driven Development)
├─ Write feature file (Gherkin) ← From acceptance criteria
├─ Implement step definitions
└─ Run tests (RED - all fail)
    ↓

PHASE 4: TDD (Test Driven Development)
├─ Write unit test (RED)
├─ Implement minimal code (GREEN)
├─ Refactor
└─ Verify BDD scenarios pass (GREEN)
    ↓

PHASE 5: Testing & Quality
└─ All tests pass (unit + BDD + integration)
```

### Decision Tree: Which Test Type?

```
What are you testing?
│
├─ User-facing behavior?
│  └─ BDD (Feature file + Step definitions)
│     Examples: "User validates config", "API returns result"
│
├─ Internal logic/algorithms?
│  └─ TDD (Unit tests)
│     Examples: "Calculate total", "Parse input"
│
└─ Integration between systems?
   └─ Integration tests
      Examples: "Database connection", "API call"
```

---

## Best Practices

### 1. Write Scenarios During Design Phase

**✅ DO:**
```
Phase 3 (DDD) → Extract acceptance criteria → Write BDD scenarios
Phase 4 (Dev) → Run BDD tests (RED) → Implement → Tests pass (GREEN)
```

**❌ DON'T:**
```
Phase 4 (Dev) → Implement feature → Write BDD scenarios after
```

**Why:** BDD scenarios define what "done" looks like. Write them first.

---

### 2. Keep Scenarios Independent

**✅ GOOD:**
```gherkin
Scenario: Create user
  Given no users exist
  When I create user "Alice"
  Then user "Alice" exists

Scenario: Delete user
  Given user "Bob" exists
  When I delete user "Bob"
  Then user "Bob" does not exist
```

**❌ BAD:**
```gherkin
Scenario: Create user
  When I create user "Alice"
  Then user "Alice" exists

Scenario: Delete user (depends on previous)
  When I delete user "Alice"  # Assumes Alice exists from previous scenario
  Then no users exist
```

**Why:** Independent scenarios can run in any order and don't cascade failures.

---

### 3. Use Background for Common Setup

**✅ GOOD:**
```gherkin
Background:
  Given the database is initialized
  And sample data is loaded

Scenario: Query users
  When I query all users
  Then 10 users are returned

Scenario: Add user
  When I add user "Alice"
  Then 11 users exist
```

**❌ BAD:**
```gherkin
Scenario: Query users
  Given the database is initialized
  And sample data is loaded
  When I query all users
  Then 10 users are returned

Scenario: Add user
  Given the database is initialized  # Duplicate setup
  And sample data is loaded
  When I add user "Alice"
  Then 11 users exist
```

---

### 4. Make Steps Reusable

**✅ GOOD:**
```python
@given(parsers.parse('a {entity} named "{name}" exists'))
def entity_exists(entity, name):
    """Generic step for any entity."""
    create_entity(entity, name)

# Works for:
# - "a user named Alice exists"
# - "a product named Widget exists"
# - "a server named Production exists"
```

**❌ BAD:**
```python
@given('user Alice exists')
def user_alice_exists():
    create_user("Alice")

@given('user Bob exists')
def user_bob_exists():
    create_user("Bob")

# Not reusable, duplicates code
```

---

### 5. Use Scenario Outline for Similar Cases

**✅ GOOD:**
```gherkin
Scenario Outline: Validate different inputs
  When I validate "<input>"
  Then the result is "<expected>"

  Examples:
    | input  | expected |
    | valid  | success  |
    | empty  | error    |
    | null   | error    |
```

**❌ BAD:**
```gherkin
Scenario: Validate valid input
  When I validate "valid"
  Then the result is "success"

Scenario: Validate empty input
  When I validate "empty"
  Then the result is "error"

Scenario: Validate null input
  When I validate "null"
  Then the result is "error"
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Testing Implementation Details

**Problem:**
```gherkin
❌ BAD:
Scenario: Call validate_config function
  When I call validate_config() with parameter config_path="test.yaml"
  Then the function returns ValidationResult object with valid=True
```

**Solution:**
```gherkin
✅ GOOD:
Scenario: Validate configuration
  When I validate the configuration file
  Then the validation passes
```

**Why:** BDD tests behavior, not implementation. Users don't care about function names.

---

### ❌ Anti-Pattern 2: Overly Detailed Steps

**Problem:**
```gherkin
❌ BAD:
Scenario: User logs in
  Given a user account with username "alice" and password "secret123"
  And the password is hashed using bcrypt with salt rounds 12
  And the session token is generated using JWT with HS256 algorithm
  When the user submits login form
  Then the authentication service validates credentials
  And a session cookie is set with httpOnly and secure flags
```

**Solution:**
```gherkin
✅ GOOD:
Scenario: User logs in
  Given a user account exists for "alice"
  When the user logs in with valid credentials
  Then the user is authenticated
  And a secure session is created
```

**Why:** Too much detail makes scenarios brittle and hard to read.

---

### ❌ Anti-Pattern 3: No Scenario Outline for Similar Cases

**Problem:**
```gherkin
❌ BAD: 20 nearly identical scenarios for different inputs
```

**Solution:**
```gherkin
✅ GOOD: 1 Scenario Outline with Examples table
```

---

### ❌ Anti-Pattern 4: Writing Scenarios After Implementation

**Problem:**
```markdown
❌ BAD: Implement feature → Write scenarios that match implementation
```

**Solution:**
```markdown
✅ GOOD: Write scenarios (acceptance criteria) → Implement to match scenarios
```

**Why:** Scenarios should drive implementation, not document it after the fact.

---

## Summary

**BDD in 3 Steps:**
1. **Write Feature File** (30-60 min) - Gherkin scenarios
2. **Implement Step Definitions** (1-2 hours) - pytest-bdd Python code
3. **Run Tests (RED)** (5 min) - Verify failures before implementation

**Integration with DDD/TDD:**
- **DDD** (Phase 3) → Acceptance criteria → **BDD** scenarios
- **BDD** scenarios (RED) → **TDD** implementation → **BDD** scenarios (GREEN)

**Key Principles:**
- ✅ Write scenarios during design (Phase 3), not after coding
- ✅ Test behavior, not implementation
- ✅ Make scenarios independent and reusable
- ✅ Use natural language (business domain)
- ✅ Keep scenarios focused (one behavior per scenario)

---

## Related Documentation

- [DEVELOPMENT_PROCESS.md](DEVELOPMENT_PROCESS.md) - Phase 4: Development
- [DDD_WORKFLOW.md](DDD_WORKFLOW.md) - Write acceptance criteria (input to BDD)
- [TDD_WORKFLOW.md](TDD_WORKFLOW.md) - Implement features to pass BDD scenarios
- [DEVELOPMENT_LIFECYCLE.md](DEVELOPMENT_LIFECYCLE.md) - How DDD→BDD→TDD integrate

---

**Version:** 1.0.0
**Created:** 2025-10-25
**Last Updated:** 2025-10-25
**Maintained By:** Project team
**Next Review:** Quarterly
