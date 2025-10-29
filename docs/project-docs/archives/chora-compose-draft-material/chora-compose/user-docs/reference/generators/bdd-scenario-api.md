# BDD Scenario Generator API Reference

**Generator Type**: `bdd_scenario_assembly`

**Purpose**: Generate Gherkin feature files for Behavior-Driven Development (BDD) testing.

**Stability**: ✅ Stable (v0.8.0+)

**Upstream Dependencies**: None (local generation only)

---

## Overview

The BDD Scenario Generator creates valid Gherkin feature files from structured configuration data. It supports all standard Gherkin constructs including features, backgrounds, scenarios, scenario outlines, tags, and examples tables.

**Use cases**:
- BDD acceptance testing (Cucumber, Behave, SpecFlow)
- Living documentation
- Test-driven development workflows
- User story acceptance criteria

**Not suitable for**:
- Unit test code generation → Use [code_generation](use-code-generation-generator.md)
- General text templating → Use [template_fill](use-template-fill-generator.md)
- API test suites → Use [jinja2](../api/generators/jinja2.md) with custom templates

---

## Class Reference

### `BDDScenarioGenerator`

```python
class BDDScenarioGenerator(GeneratorStrategy):
    """Generate Gherkin feature files from structured configuration."""
```

**Location**: [`src/chora_compose/generators/bdd_scenario.py`](../../../src/chora_compose/generators/bdd_scenario.py)

---

## Constructor

### `__init__()`

```python
def __init__(
    self,
    indent_spaces: int = 2,
    validate_gherkin: bool = True,
) -> None:
    """Initialize the BDD scenario generator."""
```

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `indent_spaces` | `int` | `2` | Number of spaces for indentation in generated Gherkin |
| `validate_gherkin` | `bool` | `True` | Enable Gherkin syntax validation |

**Example**:

```python
from chora_compose.generators.bdd_scenario import BDDScenarioGenerator

# Default settings
generator = BDDScenarioGenerator()

# Custom indentation (4 spaces)
generator = BDDScenarioGenerator(indent_spaces=4)

# Disable validation (faster, less strict)
generator = BDDScenarioGenerator(validate_gherkin=False)
```

**Attributes** (set by `__init__`):

| Attribute | Type | Value | Description |
|-----------|------|-------|-------------|
| `version` | `str` | `"0.8.0"` | Generator version |
| `description` | `str` | `"Assembles BDD scenarios into valid Gherkin feature files."` | Human-readable description |
| `capabilities` | `list[str]` | `["testing", "gherkin"]` | Generator capabilities |
| `upstream_dependencies` | `UpstreamDependencies` | (See below) | Dependency metadata |

**Upstream Dependencies**:
```python
UpstreamDependencies(
    services=[],  # No external services
    credentials_required=[],  # No API keys needed
    concurrency_safe=True,  # Thread-safe
    stability="stable"
)
```

---

## Methods

### `generate()`

Generate Gherkin feature file from configuration.

```python
def generate(
    self,
    config: ContentConfig,
    context: dict[str, Any] | None = None
) -> str:
    """Generate Gherkin feature file from configuration."""
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `config` | `ContentConfig` | Yes | Content configuration with `bdd_scenario_assembly` pattern |
| `context` | `dict[str, Any]` | No | Runtime context for variable substitution (`{{variable}}` syntax) |

**Returns**: `str` - Generated Gherkin feature file as string

**Raises**:
- `BDDScenarioError` - If configuration invalid or generation fails
  - Missing `bdd_scenario_assembly` pattern
  - Missing required fields (`feature`, `scenarios`)
  - Invalid Gherkin syntax (when `validate_gherkin=True`)
  - Empty scenarios or steps

**Example**:

```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.bdd_scenario import BDDScenarioGenerator

# Load config
loader = ConfigLoader()
config = loader.load_content_config("login-tests")

# Context for variable substitution
context = {
    "app_name": "MyApp",
    "version": "2.0"
}

# Generate
generator = BDDScenarioGenerator()
gherkin = generator.generate(config, context)

print(gherkin)
# Feature: MyApp Login (v2.0)
#   ...
```

---

## Configuration Structure

### Pattern Type

The generator requires a `bdd_scenario_assembly` pattern in `config.generation.patterns`:

```json
{
  "generation": {
    "patterns": [
      {
        "id": "bdd-pattern",
        "type": "bdd_scenario_assembly",
        "generation_config": {
          "feature": { ... },
          "background": [ ... ],
          "scenarios": [ ... ],
          "scenario_outlines": [ ... ]
        }
      }
    ]
  }
}
```

### Feature Configuration

**Required**. Defines the feature header.

```json
{
  "feature": {
    "title": "User Authentication",
    "description": "As a user\nI want to log in\nSo that I can access my account",
    "tags": ["@smoke", "@auth"]
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | Yes | Feature title (appears after `Feature:`) |
| `description` | `string` | No | Multi-line feature description (user story) |
| `tags` | `list[string]` | No | Feature-level tags (e.g., `@smoke`, `@regression`) |

**Variable substitution**: Supports `{{variable}}` in `title` and `description`.

**Output**:

```gherkin
@smoke @auth
Feature: User Authentication
  As a user
  I want to log in
  So that I can access my account
```

### Background Configuration

**Optional**. Shared setup steps run before each scenario.

```json
{
  "background": [
    "Given the application is running",
    "And the database is seeded with test data"
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `background` | `list[string]` | No | List of step strings (must start with valid keyword) |

**Step keywords**: `Given`, `When`, `Then`, `And`, `But`, `*`

**Output**:

```gherkin
Background:
  Given the application is running
  And the database is seeded with test data
```

### Scenario Configuration

**Required** (at least one scenario). Individual test cases.

```json
{
  "scenarios": [
    {
      "title": "Successful login with valid credentials",
      "tags": ["@happy-path"],
      "steps": [
        "Given I am on the login page",
        "When I enter username \"{{username}}\" and password \"{{password}}\"",
        "Then I should see the dashboard"
      ]
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | Yes | Scenario title (appears after `Scenario:`) |
| `steps` | `list[string]` | Yes | List of step strings (must be non-empty) |
| `tags` | `list[string]` | No | Scenario-level tags |

**Variable substitution**: Supports `{{variable}}` in `title` and `steps`.

**Validation**:
- Each step must start with valid keyword (`Given`, `When`, `Then`, `And`, `But`, `*`)
- Steps list must be non-empty
- Title must be non-empty

**Output**:

```gherkin
@happy-path
Scenario: Successful login with valid credentials
  Given I am on the login page
  When I enter username "alice@example.com" and password "Test123!"
  Then I should see the dashboard
```

### Scenario Outline Configuration

**Optional**. Parameterized tests with examples tables.

```json
{
  "scenario_outlines": [
    {
      "title": "Login with different credentials",
      "tags": ["@parametrized"],
      "steps": [
        "Given I am on the login page",
        "When I enter username \"<username>\" and password \"<password>\"",
        "Then I should see \"<result>\""
      ],
      "examples": {
        "headers": ["username", "password", "result"],
        "rows": [
          ["alice@example.com", "Test123!", "dashboard"],
          ["bob@example.com", "WrongPass", "error message"]
        ]
      }
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | Yes | Scenario Outline title |
| `steps` | `list[string]` | Yes | Steps with `<placeholder>` syntax |
| `examples` | `object` | Yes | Examples table configuration |
| `examples.headers` | `list[string]` | Yes | Column headers |
| `examples.rows` | `list[list[Any]]` | Yes | Data rows (values auto-converted to strings) |
| `tags` | `list[string]` | No | Scenario-level tags |

**Placeholder syntax**: Use `<placeholder>` in steps (NOT `{{variable}}`).

**Variable substitution**: Supports `{{variable}}` in `title` only (NOT in steps with placeholders).

**Output**:

```gherkin
@parametrized
Scenario Outline: Login with different credentials
  Given I am on the login page
  When I enter username "<username>" and password "<password>"
  Then I should see "<result>"

  Examples:
    | username          | password  | result        |
    | alice@example.com | Test123!  | dashboard     |
    | bob@example.com   | WrongPass | error message |
```

---

## Variable Substitution

### Syntax

Use `{{variable}}` in titles, descriptions, and steps:

```json
{
  "feature": {
    "title": "{{app_name}} Login Tests"
  },
  "scenarios": [{
    "title": "Login as {{user_role}}",
    "steps": [
      "Given I am logged in as \"{{username}}\""
    ]
  }]
}
```

**Context**:

```python
context = {
    "app_name": "MyApp",
    "user_role": "administrator",
    "username": "admin@example.com"
}
```

**Output**:

```gherkin
Feature: MyApp Login Tests

Scenario: Login as administrator
  Given I am logged in as "admin@example.com"
```

### Where Variables Work

| Location | Variable Substitution | Example |
|----------|----------------------|---------|
| `feature.title` | ✅ Yes | `"{{app_name}} Tests"` |
| `feature.description` | ✅ Yes | `"Version: {{version}}"` |
| `background` steps | ✅ Yes | `"Given {{precondition}}"` |
| `scenarios[*].title` | ✅ Yes | `"Test {{feature_name}}"` |
| `scenarios[*].steps` | ✅ Yes | `"When I enter {{value}}"` |
| `scenario_outlines[*].title` | ✅ Yes | `"Test {{feature}}"` |
| `scenario_outlines[*].steps` | ❌ No* | Use `<placeholder>` instead |
| `examples.headers` | ❌ No | Static column names |
| `examples.rows` | ❌ No | Static table data |

**\*Note**: Scenario Outline steps use `<placeholder>` syntax for parameterization, NOT `{{variable}}`.

---

## Tags

### Tag Format

Tags must follow Gherkin tag syntax:

**Valid tags**:
- `@smoke` (no @ prefix needed, auto-added)
- `@regression`
- `@happy-path`
- `@US-1234` (with numbers)
- `@ignore_on_ci` (with underscores)

**Invalid tags**:
- `smoke` (missing @, but auto-corrected)
- `@123-test` (cannot start with number)
- `@test case` (no spaces)
- `@test!` (no special characters except `-` and `_`)

**Validation** (when `validate_gherkin=True`):
```python
# Must match: @[a-zA-Z][a-zA-Z0-9_-]*
if not re.match(r"^@[a-zA-Z][a-zA-Z0-9_-]*$", tag):
    raise BDDScenarioError(f"Invalid tag format: '{tag}'")
```

### Tag Placement

```json
{
  "feature": {
    "title": "Login",
    "tags": ["@smoke", "@auth"]  // Feature-level tags
  },
  "scenarios": [{
    "title": "Successful login",
    "tags": ["@happy-path", "@critical"]  // Scenario-level tags
  }]
}
```

**Output**:

```gherkin
@smoke @auth
Feature: Login

  @happy-path @critical
  Scenario: Successful login
    ...
```

**Tag inheritance**: Scenario tags do NOT inherit feature tags (Gherkin standard).

---

## Step Validation

### Valid Step Keywords

When `validate_gherkin=True` (default), all steps must start with valid keyword:

| Keyword | Purpose | Example |
|---------|---------|---------|
| `Given` | Preconditions, setup | `Given the user is logged in` |
| `When` | Actions, events | `When I click the submit button` |
| `Then` | Expected outcomes | `Then I should see a success message` |
| `And` | Additional steps (same type) | `And I should receive an email` |
| `But` | Additional steps (negation) | `But I should not see an error` |
| `*` | Wildcard (matches any keyword) | `* the system is ready` |

**Valid**:
```json
{
  "steps": [
    "Given I am on the homepage",
    "When I click login",
    "Then I see the dashboard",
    "And I see my profile picture"
  ]
}
```

**Invalid** (when `validate_gherkin=True`):
```json
{
  "steps": [
    "I am on the homepage"  // ❌ Missing keyword
  ]
}
```

**Error**:
```python
BDDScenarioError: Invalid step keyword: 'I'. Must be one of: Given, When, Then, And, But, *
```

### Disabling Validation

For testing or non-standard Gherkin:

```python
generator = BDDScenarioGenerator(validate_gherkin=False)
```

**Use cases**:
- Prototyping scenarios quickly
- Non-standard step definitions
- Performance (skip validation overhead)

**Trade-off**: May generate invalid Gherkin that fails in test runners.

---

## Indentation

### Default Indentation

Default: 2 spaces per level

```gherkin
Feature: Login
  As a user           ← 2 spaces (level 1)

  Scenario: Test
    Given setup       ← 4 spaces (level 2)
```

### Custom Indentation

```python
# 4 spaces per level
generator = BDDScenarioGenerator(indent_spaces=4)
```

**Output**:

```gherkin
Feature: Login
    As a user               ← 4 spaces (level 1)

    Scenario: Test
        Given setup         ← 8 spaces (level 2)
```

**Indentation levels**:
- Level 0: `Feature:`, `Scenario:`, `Background:`
- Level 1: Feature description, Background steps, Scenario steps
- Level 2: Examples table rows

---

## Error Handling

### Common Errors

#### 1. Missing Feature Configuration

```python
BDDScenarioError: No 'feature' configuration provided
```

**Cause**: `generation_config.feature` missing or null.

**Fix**:
```json
{
  "generation_config": {
    "feature": {
      "title": "My Feature"  // ← Required
    }
  }
}
```

#### 2. Empty Scenarios

```python
BDDScenarioError: Gherkin must contain at least one 'Scenario:' or 'Scenario Outline:'
```

**Cause**: Both `scenarios` and `scenario_outlines` are empty or missing.

**Fix**: Add at least one scenario:
```json
{
  "scenarios": [
    {
      "title": "Basic test",
      "steps": ["Given something", "When action", "Then result"]
    }
  ]
}
```

#### 3. Scenario Missing Steps

```python
BDDScenarioError: Scenario 'Login test' has no steps
```

**Cause**: `scenario.steps` is empty list or missing.

**Fix**:
```json
{
  "scenarios": [{
    "title": "Login test",
    "steps": [  // ← Must have at least one step
      "Given I am on the login page"
    ]
  }]
}
```

#### 4. Invalid Step Keyword

```python
BDDScenarioError: Invalid step keyword: 'I'. Must be one of: Given, When, Then, And, But, *
```

**Cause**: Step doesn't start with valid keyword (when `validate_gherkin=True`).

**Fix**: Prefix step with keyword:
```json
{
  "steps": [
    "Given I am on the homepage"  // ← Add "Given"
  ]
}
```

#### 5. Invalid Tag Format

```python
BDDScenarioError: Invalid tag format: '@123test'. Tags must start with @ followed by alphanumeric/underscore/hyphen
```

**Cause**: Tag starts with number or contains invalid characters.

**Fix**:
```json
{
  "tags": ["@test123"]  // ← Letter first, then numbers OK
}
```

#### 6. Missing Pattern

```python
BDDScenarioError: Config 'my-config' has no bdd_scenario_assembly pattern
```

**Cause**: No pattern with `type: "bdd_scenario_assembly"` in config.

**Fix**:
```json
{
  "generation": {
    "patterns": [{
      "type": "bdd_scenario_assembly",  // ← Must be exact string
      "generation_config": { ... }
    }]
  }
}
```

---

## Examples

### Basic Feature

**Config**:

```json
{
  "type": "content",
  "id": "basic-login",
  "generation": {
    "patterns": [{
      "type": "bdd_scenario_assembly",
      "generation_config": {
        "feature": {
          "title": "User Login",
          "description": "Basic login functionality"
        },
        "scenarios": [
          {
            "title": "Successful login",
            "steps": [
              "Given I am on the login page",
              "When I enter valid credentials",
              "Then I should see the dashboard"
            ]
          }
        ]
      }
    }]
  }
}
```

**Output**:

```gherkin
Feature: User Login
  Basic login functionality

Scenario: Successful login
  Given I am on the login page
  When I enter valid credentials
  Then I should see the dashboard
```

### With Background and Tags

**Config**:

```json
{
  "generation_config": {
    "feature": {
      "title": "Shopping Cart",
      "tags": ["@e2e", "@cart"]
    },
    "background": [
      "Given the application is running",
      "And I am logged in as a customer"
    ],
    "scenarios": [
      {
        "title": "Add item to cart",
        "tags": ["@happy-path"],
        "steps": [
          "Given I am viewing a product",
          "When I click 'Add to Cart'",
          "Then the item should appear in my cart",
          "And the cart count should increase by 1"
        ]
      },
      {
        "title": "Remove item from cart",
        "tags": ["@regression"],
        "steps": [
          "Given I have items in my cart",
          "When I click 'Remove' on an item",
          "Then the item should be removed",
          "But other items should remain"
        ]
      }
    ]
  }
}
```

**Output**:

```gherkin
@e2e @cart
Feature: Shopping Cart

Background:
  Given the application is running
  And I am logged in as a customer

@happy-path
Scenario: Add item to cart
  Given I am viewing a product
  When I click 'Add to Cart'
  Then the item should appear in my cart
  And the cart count should increase by 1

@regression
Scenario: Remove item from cart
  Given I have items in my cart
  When I click 'Remove' on an item
  Then the item should be removed
  But other items should remain
```

### Scenario Outline

**Config**:

```json
{
  "generation_config": {
    "feature": {
      "title": "Calculator"
    },
    "scenario_outlines": [
      {
        "title": "Addition",
        "steps": [
          "Given I have entered <num1> into the calculator",
          "And I have entered <num2> into the calculator",
          "When I press add",
          "Then the result should be <result>"
        ],
        "examples": {
          "headers": ["num1", "num2", "result"],
          "rows": [
            [1, 2, 3],
            [5, 7, 12],
            [10, 15, 25]
          ]
        }
      }
    ]
  }
}
```

**Output**:

```gherkin
Feature: Calculator

Scenario Outline: Addition
  Given I have entered <num1> into the calculator
  And I have entered <num2> into the calculator
  When I press add
  Then the result should be <result>

  Examples:
    | num1 | num2 | result |
    | 1    | 2    | 3      |
    | 5    | 7    | 12     |
    | 10   | 15   | 25     |
```

### With Variable Substitution

**Config**:

```json
{
  "generation_config": {
    "feature": {
      "title": "{{app_name}} API Tests"
    },
    "scenarios": [{
      "title": "Get user by ID",
      "steps": [
        "Given the {{app_name}} API is running",
        "When I request user with ID {{user_id}}",
        "Then I should receive a 200 response"
      ]
    }]
  }
}
```

**Context**:

```python
context = {
    "app_name": "UserService",
    "user_id": "12345"
}
```

**Output**:

```gherkin
Feature: UserService API Tests

Scenario: Get user by ID
  Given the UserService API is running
  When I request user with ID 12345
  Then I should receive a 200 response
```

---

## Performance

### Typical Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Simple feature (1 scenario, 5 steps) | <5ms | Without validation |
| Simple feature (1 scenario, 5 steps) | <10ms | With validation |
| Complex feature (10 scenarios, 50 steps) | <20ms | Without validation |
| Complex feature (10 scenarios, 50 steps) | <30ms | With validation |

**Factors affecting performance**:
- Number of scenarios and steps
- Validation overhead (`validate_gherkin=True` adds ~5-10ms)
- Variable substitution (more variables = slightly slower)

### Optimization

**1. Disable validation for large batches**:

```python
# Fast generation (no validation)
generator = BDDScenarioGenerator(validate_gherkin=False)

# Validate separately with Gherkin linter if needed
# (e.g., cucumber --dry-run)
```

**2. Reuse generator instance**:

```python
# ✅ Good: Reuse generator
generator = BDDScenarioGenerator()
for config in configs:
    output = generator.generate(config)

# ❌ Bad: Create new generator each time
for config in configs:
    generator = BDDScenarioGenerator()  # Unnecessary overhead
    output = generator.generate(config)
```

---

## Integration

### With Test Frameworks

#### Cucumber (Ruby/JS)

```bash
# Generate feature file
python generate_features.py  # Uses BDDScenarioGenerator

# Run Cucumber tests
cucumber features/login.feature
```

#### Behave (Python)

```bash
# Generate features
python generate_features.py

# Run Behave
behave features/
```

#### SpecFlow (.NET)

```bash
# Generate features
python generate_features.py

# Add to Visual Studio project
# Run with NUnit/xUnit
```

### CI/CD Integration

```yaml
# .github/workflows/tests.yml
- name: Generate BDD scenarios
  run: |
    python -m chora_compose.cli generate-all --type bdd

- name: Run Cucumber tests
  run: |
    cucumber features/
```

---

## Related Documentation

### How-To Guides
- [Use BDD Scenario Generator](../../how-to/generators/use-bdd-scenario-generator.md) - Step-by-step usage guide
- [Debug Jinja2 Templates](../../how-to/generation/debug-jinja2-templates.md) - Alternative for custom test formats

### Explanation
- [When to Use Which Generator](../../explanation/generators/when-to-use-which.md) - Generator selection guide

### Tutorials
- [Generate Your First Content](../../tutorials/getting-started/03-generate-your-first-content.md) - Basic generation workflow

---

## API Summary

```python
# Import
from chora_compose.generators.bdd_scenario import BDDScenarioGenerator, BDDScenarioError

# Create generator
generator = BDDScenarioGenerator(
    indent_spaces=2,      # Indentation (default: 2)
    validate_gherkin=True # Validation (default: True)
)

# Generate feature file
gherkin: str = generator.generate(
    config=content_config,  # ContentConfig with bdd_scenario_assembly pattern
    context={"var": "val"}  # Optional variable context
)

# Attributes
generator.version              # "0.8.0"
generator.description          # "Assembles BDD scenarios..."
generator.capabilities         # ["testing", "gherkin"]
generator.upstream_dependencies  # UpstreamDependencies(...)

# Exception
try:
    output = generator.generate(config)
except BDDScenarioError as e:
    print(f"Generation failed: {e}")
```

---

**Last Updated**: 2025-10-21 | **Generator Version**: 0.8.0 | **Diataxis Category**: Reference
