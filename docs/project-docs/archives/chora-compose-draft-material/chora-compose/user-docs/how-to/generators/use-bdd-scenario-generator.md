# How to Use the BDD Scenario Generator

> **Goal:** Generate Gherkin feature files for Behavior-Driven Development testing.

## When to Use This

You need the BDDScenarioGenerator when:
- You practice Behavior-Driven Development (BDD)
- You need Gherkin feature files for testing
- You're using Cucumber, Behave, or SpecFlow
- You want living documentation
- You need acceptance test scenarios
- You're documenting user stories with test scenarios

**Don't use this if:**
- Not doing BDD testing → Use [template_fill](use-template-fill-generator.md) for test documentation
- Need unit test code → Use [code_generation](use-code-generation-generator.md)
- Need general text generation → Use [template_fill](use-template-fill-generator.md) or [jinja2](../generation/debug-jinja2-templates.md)
- Writing non-test documentation → Use [jinja2](../generation/debug-jinja2-templates.md)

## Prerequisites

- Chora Compose installed
- Basic understanding of BDD and Gherkin syntax
- Testing framework (Cucumber, Behave, or SpecFlow)
- Familiarity with Given-When-Then format

---

## Gherkin Quick Primer

Gherkin is a business-readable DSL for behavior specifications:

```gherkin
Feature: User Login
  As a user
  I want to log in
  So that I can access my account

  Background:
    Given the application is running

  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials
    Then I should see the dashboard

  Scenario Outline: Login with different users
    Given I am on the login page
    When I enter username "<username>" and password "<password>"
    Then I should see "<result>"

    Examples:
      | username | password | result |
      | alice    | pass123  | dashboard |
      | bob      | wrongpass | error |
```

**Keywords:**
- **Feature**: High-level description
- **Background**: Steps run before each scenario
- **Scenario**: Individual test case
- **Scenario Outline**: Parameterized test
- **Given**: Preconditions/setup
- **When**: Actions/events
- **Then**: Expected outcomes
- **And/But**: Additional steps

---

## Solution

### Quick Version

```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.bdd_scenario import BDDScenarioGenerator

# Load config
loader = ConfigLoader()
config = loader.load_content_config("login-feature")

# Context
context = {
    "feature_title": "User Login",
    "valid_username": "testuser@example.com",
    "valid_password": "Test123!"
}

# Generate
generator = BDDScenarioGenerator()
output = generator.generate(config, context=context)

# Save
with open("login.feature", "w") as f:
    f.write(output)
```

### Detailed Steps

#### 1. Create Content Configuration

```json
{
  "type": "content",
  "id": "login-feature",
  "schemaRef": {
    "id": "content-schema",
    "version": "3.1"
  },
  "metadata": {
    "description": "Login feature with test scenarios",
    "version": "1.0.0",
    "generation_frequency": "on_demand",
    "output_format": "gherkin"
  },
  "elements": [
    {
      "name": "feature",
      "description": "Login feature file",
      "format": "gherkin",
      "example_output": ""
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "login-bdd",
        "type": "bdd_scenario_assembly",
        "generation_config": {
          "feature": {
            "title": "{{feature_title}}",
            "description": "As a user\nI want to log in\nSo that I can access my account",
            "tags": ["@authentication", "@critical"]
          },
          "background": [
            "Given the application is running",
            "And the database is populated with test users"
          ],
          "scenarios": [
            {
              "title": "Successful login with valid credentials",
              "tags": ["@happy-path"],
              "steps": [
                "Given I am on the login page",
                "When I enter username \"{{valid_username}}\"",
                "And I enter password \"{{valid_password}}\"",
                "And I click the login button",
                "Then I should be redirected to the dashboard"
              ]
            }
          ]
        }
      }
    ]
  }
}
```

#### 2. Prepare Context

```json
{
  "feature_title": "User Login",
  "feature_description": "As a user\nI want to log in\nSo that I can access my account",
  "valid_username": "testuser@example.com",
  "valid_password": "Test123!"
}
```

#### 3. Generate Feature File

```python
from chora_compose.generators.bdd_scenario import BDDScenarioGenerator

generator = BDDScenarioGenerator(
    indent_spaces=2,           # Indentation (default: 2)
    validate_gherkin=True      # Validate syntax (default: True)
)

result = generator.generate(config, context=context)

with open("features/login.feature", "w") as f:
    f.write(result)
```

#### 4. Run Tests

```bash
# Using Behave (Python)
behave features/login.feature

# Using Cucumber (JavaScript/Ruby)
cucumber features/login.feature

# Using SpecFlow (.NET)
specflow features/login.feature
```

---

## Configuration Structure

### Feature Section

```json
{
  "feature": {
    "title": "User Authentication",
    "description": "As a user\nI want to authenticate\nSo that I can access the system",
    "tags": ["@authentication", "@critical", "@smoke"]
  }
}
```

**Output:**
```gherkin
@authentication @critical @smoke
Feature: User Authentication
  As a user
  I want to authenticate
  So that I can access the system
```

### Background Section

```json
{
  "background": [
    "Given the application is running",
    "And the database is in a clean state",
    "And test users exist"
  ]
}
```

**Output:**
```gherkin
Background:
  Given the application is running
  And the database is in a clean state
  And test users exist
```

### Scenarios

```json
{
  "scenarios": [
    {
      "title": "Successful operation",
      "tags": ["@happy-path"],
      "steps": [
        "Given precondition",
        "When action occurs",
        "Then expected outcome"
      ]
    }
  ]
}
```

**Output:**
```gherkin
@happy-path
Scenario: Successful operation
  Given precondition
  When action occurs
  Then expected outcome
```

### Scenario Outlines (Data-Driven)

```json
{
  "scenario_outlines": [
    {
      "title": "Login with different users",
      "tags": ["@parametrized"],
      "steps": [
        "Given I am on the login page",
        "When I enter username \"<username>\" and password \"<password>\"",
        "Then I should see \"<result>\""
      ],
      "examples": {
        "headers": ["username", "password", "result"],
        "rows": [
          ["alice@example.com", "pass123", "dashboard"],
          ["bob@example.com", "wrongpass", "error"],
          ["charlie@example.com", "pass456", "dashboard"]
        ]
      }
    }
  ]
}
```

**Output:**
```gherkin
@parametrized
Scenario Outline: Login with different users
  Given I am on the login page
  When I enter username "<username>" and password "<password>"
  Then I should see "<result>"

  Examples:
    | username | password | result |
    | alice@example.com | pass123 | dashboard |
    | bob@example.com | wrongpass | error |
    | charlie@example.com | pass456 | dashboard |
```

---

## Variable Substitution

### In Feature Description

```json
{
  "feature": {
    "title": "{{feature_name}} Management"
  }
}
```

Context: `{"feature_name": "User"}`
Result: `Feature: User Management`

### In Steps

```json
{
  "steps": [
    "Given I am logged in as \"{{username}}\"",
    "When I navigate to {{page_url}}",
    "Then I should see {{expected_count}} items"
  ]
}
```

Context:
```json
{
  "username": "admin@example.com",
  "page_url": "/dashboard",
  "expected_count": "5"
}
```

---

## Tag Organization

### Purpose of Tags

Tags help organize and filter tests:
- **@smoke**: Core functionality tests
- **@regression**: Full test suite
- **@wip**: Work in progress
- **@slow**: Long-running tests
- **@integration**: Integration tests
- **@unit**: Unit-level tests

### Multiple Tags

```json
{
  "tags": ["@authentication", "@critical", "@smoke"]
}
```

**Output:**
```gherkin
@authentication @critical @smoke
Feature: ...
```

### Running Tagged Tests

```bash
# Run only smoke tests
behave --tags=@smoke

# Run critical but not slow tests
behave --tags=@critical --tags=~@slow

# Cucumber
cucumber --tags '@smoke and not @wip'
```

---

## Testing Framework Integration

### Behave (Python)

**1. Install:**
```bash
pip install behave
```

**2. Create step definitions:**
```python
# features/steps/login_steps.py
from behave import given, when, then

@given('I am on the login page')
def step_impl(context):
    context.browser.get('/login')

@when('I enter username "{username}"')
def step_impl(context, username):
    context.browser.find_element_by_id('username').send_keys(username)

@then('I should see the dashboard')
def step_impl(context):
    assert 'dashboard' in context.browser.current_url
```

**3. Run:**
```bash
behave features/
```

### Cucumber (JavaScript)

**1. Install:**
```bash
npm install @cucumber/cucumber
```

**2. Create step definitions:**
```javascript
// features/step_definitions/login_steps.js
const { Given, When, Then } = require('@cucumber/cucumber');

Given('I am on the login page', async function () {
  await this.page.goto('/login');
});

When('I enter username {string}', async function (username) {
  await this.page.type('#username', username);
});

Then('I should see the dashboard', async function () {
  const url = await this.page.url();
  assert(url.includes('dashboard'));
});
```

**3. Run:**
```bash
npx cucumber-js
```

### SpecFlow (.NET)

**1. Install:**
```bash
dotnet add package SpecFlow
```

**2. Create step definitions:**
```csharp
[Given("I am on the login page")]
public void GivenIAmOnTheLoginPage()
{
    _driver.Navigate().GoToUrl("/login");
}

[When("I enter username {string}")]
public void WhenIEnterUsername(string username)
{
    _driver.FindElement(By.Id("username")).SendKeys(username);
}

[Then("I should see the dashboard")]
public void ThenIShouldSeeTheDashboard()
{
    Assert.Contains("dashboard", _driver.Url);
}
```

**3. Run:**
```bash
dotnet test
```

---

## Best Practices

### Do ✅

**1. Write from user perspective:**
```gherkin
✅ When I click the "Submit" button
❌ When the form submission handler is triggered
```

**2. Use business language:**
```gherkin
✅ Given I have an active subscription
❌ Given the subscription_status field is "active"
```

**3. Keep scenarios focused:**
```gherkin
✅ Scenario: User can log in
      Given I am on the login page
      When I enter valid credentials
      Then I should see the dashboard

❌ Scenario: User can log in and view profile and edit settings
      Given I am on the login page
      When I enter valid credentials
      And I click on profile
      And I edit my name
      ...
```

**4. Use descriptive scenario names:**
```gherkin
✅ Scenario: Login fails with invalid password
❌ Scenario: Test 1
```

**5. Organize with tags:**
```gherkin
@authentication @critical
Feature: User Login
```

### Don't ❌

**1. Don't include implementation details:**
```gherkin
❌ When I click the button with ID "submit_btn"
✅ When I submit the form
```

**2. Don't make scenarios depend on each other:**
```gherkin
❌ Scenario: Create user (must run first)
❌ Scenario: Login with created user (depends on above)

✅ Scenario: Login with existing user
      Given a user exists with credentials...
```

**3. Don't use technical jargon:**
```gherkin
❌ When I POST to /api/login with JSON payload
✅ When I attempt to log in
```

**4. Don't test multiple features in one scenario:**
```gherkin
❌ Scenario: Complete user workflow
      # Tests login, profile, settings, logout all together

✅ Multiple focused scenarios:
      Scenario: User can log in
      Scenario: User can update profile
      Scenario: User can change settings
      Scenario: User can log out
```

---

## Advanced Usage

### Multiple Example Tables

```json
{
  "scenario_outlines": [
    {
      "title": "Login validation",
      "steps": ["..."],
      "examples": {
        "name": "Valid Users",
        "headers": ["username", "password"],
        "rows": [["alice", "pass1"], ["bob", "pass2"]]
      }
    },
    {
      "title": "Login validation",
      "steps": ["..."],
      "examples": {
        "name": "Invalid Users",
        "headers": ["username", "password"],
        "rows": [["hacker", "wrong"], ["", ""]]
      }
    }
  ]
}
```

### Complex Data Tables

```gherkin
Scenario: User registration with profile
  Given I am on the registration page
  When I fill in the form with:
    | field      | value              |
    | Name       | Alice Smith        |
    | Email      | alice@example.com  |
    | Password   | SecurePass123!     |
    | Age        | 28                 |
  Then the account should be created
```

### Gherkin Validation

```python
generator = BDDScenarioGenerator(
    validate_gherkin=True  # Default
)

# Validates:
# - Step keywords (Given, When, Then, And, But)
# - Tag format (@tag_name)
# - Feature/Scenario structure
```

**Invalid scenarios will raise `BDDScenarioError`**

---

## Common Patterns

### Login Feature

```json
{
  "feature": {
    "title": "User Authentication",
    "tags": ["@authentication"]
  },
  "scenarios": [
    {
      "title": "Successful login",
      "tags": ["@happy-path"],
      "steps": [...]
    },
    {
      "title": "Failed login - invalid password",
      "tags": ["@error-handling"],
      "steps": [...]
    },
    {
      "title": "Failed login - account locked",
      "tags": ["@error-handling"],
      "steps": [...]
    }
  ]
}
```

### E-commerce Checkout

```json
{
  "feature": {
    "title": "Shopping Cart Checkout",
    "tags": ["@checkout", "@critical"]
  },
  "background": [
    "Given I am logged in",
    "And I have items in my cart"
  ],
  "scenarios": [
    {
      "title": "Successful checkout with credit card",
      "steps": [...]
    },
    {
      "title": "Checkout fails with invalid card",
      "steps": [...]
    }
  ]
}
```

### API Testing

```json
{
  "feature": {
    "title": "User API",
    "tags": ["@api", "@integration"]
  },
  "scenarios": [
    {
      "title": "GET /users returns user list",
      "steps": [
        "Given the API is running",
        "When I send a GET request to \"/users\"",
        "Then the response status should be 200",
        "And the response should contain a list of users"
      ]
    }
  ]
}
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Invalid Gherkin syntax | Incorrect step keywords | Use Given/When/Then/And/But |
| Steps not matching | Missing step definitions | Implement step definitions |
| Tags not working | Wrong tag format | Use @tag_name format |
| Scenarios not running | Tag filters | Check behave/cucumber tag filters |
| Background not executing | Framework issue | Verify framework setup |
| Variables not substituted | Missing context key | Add variable to context.json |

---

## Example Workflows

### Generate from User Stories

```python
def generate_feature_from_user_story(story):
    """Convert user story to BDD feature."""
    context = {
        "feature_title": story.title,
        "feature_description": story.description,
        "acceptance_criteria": story.acceptance_criteria
    }

    # Generate scenarios from acceptance criteria
    scenarios = []
    for criterion in story.acceptance_criteria:
        scenarios.append({
            "title": criterion.title,
            "steps": criterion_to_steps(criterion)
        })

    config = create_bdd_config(context, scenarios)
    generator = BDDScenarioGenerator()
    return generator.generate(config, context)
```

### CI/CD Integration

```yaml
# .github/workflows/generate-features.yml
- name: Generate BDD features
  run: |
    python scripts/generate_features.py \
      --stories stories/*.json \
      --output features/

- name: Run BDD tests
  run: behave features/

- name: Publish test results
  uses: actions/upload-artifact@v2
  with:
    name: test-results
    path: reports/
```

---

## Examples

**Full working example:**
- See: [examples/04-bdd-scenarios/](../../examples/04-bdd-scenarios/)
- Use case: Login feature with multiple scenarios
- Includes: Config, context, expected output

**Quick links:**
- [README](../../examples/04-bdd-scenarios/README.md)
- [Config](../../examples/04-bdd-scenarios/configs/content/login-feature.json)
- [Context](../../examples/04-bdd-scenarios/context.json)
- [Generated Feature](../../examples/04-bdd-scenarios/login.feature)

---

## Related Documentation

- [Generator Comparison Guide](comparison.md) - Choose the right generator
- [Template Fill Generator](template-fill.md) - For test documentation
- [Code Generation](code-generation.md) - For test code generation
- [Cucumber Documentation](https://cucumber.io/docs) - Official Cucumber guide
- [Behave Documentation](https://behave.readthedocs.io/) - Official Behave guide
- [SpecFlow Documentation](https://specflow.org/documentation/) - Official SpecFlow guide

---

## API Reference

```python
class BDDScenarioGenerator(GeneratorStrategy):
    """Generate Gherkin feature files for BDD testing."""

    def __init__(
        self,
        indent_spaces: int = 2,
        validate_gherkin: bool = True
    ) -> None:
        """Initialize BDD scenario generator."""

    def generate(
        self,
        config: ContentConfig,
        context: dict[str, Any] | None = None
    ) -> str:
        """Generate Gherkin feature file from configuration."""
```

**Parameters:**
- `indent_spaces`: Number of spaces for indentation (default: 2)
- `validate_gherkin`: Validate Gherkin syntax (default: True)
- `context`: Variable context for substitution

**Returns:** Complete Gherkin feature file as string

**Raises:**
- `BDDScenarioError`: If configuration invalid or Gherkin validation fails

---

**Last Updated:** 2025-10-12 | **Phase:** 3.2 Complete
