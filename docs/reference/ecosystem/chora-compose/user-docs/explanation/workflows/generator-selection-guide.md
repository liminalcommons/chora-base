# Explanation: Generator Selection Guide

**Diataxis Quadrant**: Explanation
**Purpose**: Understand when to use each generator and how to choose the right one for your use case

---

## Overview

chora-compose provides **four built-in generators**, each optimized for different content generation scenarios. Choosing the wrong generator leads to complexity, poor performance, or unnatural outputs. Choosing the right one unlocks simplicity and power.

This guide explains:

- **What each generator does** (and doesn't do)
- **When to use** each generator (decision criteria)
- **How to choose** between generators (decision tree)
- **Real-world examples** for each generator
- **Performance characteristics** and trade-offs

**The Four Generators**:

1. **template_fill**: Simple variable substitution (`{{name}}` → `"Alice"`)
2. **jinja2**: Advanced templating with logic (loops, conditionals, filters)
3. **code_generation**: AI-powered natural language generation via Claude API
4. **demonstration**: BDD-style examples with generative patterns

---

## Generator Comparison Table

| Generator | Best For | Complexity | Speed | Requires API Key | Deterministic |
|-----------|----------|------------|-------|-----------------|---------------|
| **template_fill** | Simple substitution | Lowest | Fastest | No | Yes |
| **jinja2** | Structured templates | Medium | Fast | No | Yes |
| **code_generation** | Natural language, code | Highest | Slower | Yes (Anthropic) | No |
| **demonstration** | Examples, patterns | Medium | Fast | No | Yes |

**Quick decision**:
- Need simple text replacement? → **template_fill**
- Need loops, conditionals, filters? → **jinja2**
- Need AI-generated natural language or code? → **code_generation**
- Need BDD scenarios or example-driven content? → **demonstration**

---

## Generator 1: template_fill

### What It Does

**Simple string substitution** using `{{variable}}` syntax:

```
Input template: "Hello, {{name}}!"
Input context:  {"name": "Alice"}
Output:         "Hello, Alice!"
```

**No logic**: No loops, no conditionals, no filters — just direct replacement.

### When to Use

✅ **Use template_fill when**:

1. **Simple variable replacement**: Names, dates, single values
2. **Static structure**: Template structure never changes
3. **No logic needed**: No "if this, then that"
4. **Fast execution required**: Milliseconds matter
5. **Guaranteed output**: Must be deterministic

**Examples**:
- Email templates ("Hello {{recipient}}, your order #{{order_id}} shipped")
- Configuration files with placeholders (API endpoints, credentials)
- Simple documentation stubs ("Project: {{project_name}}, Version: {{version}}")

### When NOT to Use

❌ **Don't use template_fill when**:

1. **Loops required**: Iterating over lists
2. **Conditional logic**: Different outputs based on input
3. **Complex formatting**: Date formatting, string manipulation
4. **Natural language**: Want fluent, AI-generated text

**Wrong tool examples**:
- Generating a report with variable number of sections (use jinja2)
- Code generation (use code_generation)
- Human-like descriptions (use code_generation)

### Example: Simple Email Template

**Config**:
```json
{
  "metadata": {
    "id": "welcome-email",
    "title": "Welcome Email"
  },
  "generatorSpecific": {
    "template_fill": {
      "template": "Welcome to {{product_name}}, {{user_name}}!\n\nYour account ({{email}}) is ready.",
      "inputs": {
        "context": {
          "product_name": "chora-compose",
          "user_name": "{{user_name}}",
          "email": "{{email}}"
        }
      }
    }
  }
}
```

**Usage**:
```bash
choracompose:generate_content --config-id welcome-email --context '{"user_name": "Alice", "email": "alice@example.com"}'
```

**Output**:
```
Welcome to chora-compose, Alice!

Your account (alice@example.com) is ready.
```

**Why template_fill?**
- No loops (single user)
- No conditionals (same structure every time)
- Fast execution (< 1ms)

---

## Generator 2: jinja2

### What It Does

**Advanced templating** with Python-like syntax:

- **Loops**: `{% for item in items %}`
- **Conditionals**: `{% if condition %}`
- **Filters**: `{{ name|upper }}`
- **Includes**: `{% include 'header.j2' %}`

**Logic without code**: Express complex structure declaratively.

### When to Use

✅ **Use jinja2 when**:

1. **Iterating over lists**: Generate sections from array
2. **Conditional content**: Include/exclude based on data
3. **Structured documents**: Multi-section reports, documentation
4. **Reusable components**: Shared headers, footers, snippets
5. **Formatting logic**: Date formatting, case conversion, filtering

**Examples**:
- Multi-section reports (daily standups, changelogs)
- Documentation with conditional sections (API docs, README)
- Configuration files with repeated structures (CI/CD configs)
- HTML emails with dynamic content

### When NOT to Use

❌ **Don't use jinja2 when**:

1. **No logic needed**: Use template_fill (simpler)
2. **Natural language required**: Use code_generation (AI-powered)
3. **Template is complex**: 500+ lines (use code_generation or multiple templates)

### Example: Daily Standup Report

**Template** (`templates/standup.j2`):
```jinja2
# Daily Standup - {{ date }}

## Team: {{ team_name }}

{% if achievements %}
## Achievements
{% for item in achievements %}
- {{ item }}
{% endfor %}
{% endif %}

{% if blockers %}
## Blockers
{% for blocker in blockers %}
- **{{ blocker.title }}**: {{ blocker.description }}
  - Owner: {{ blocker.owner }}
{% endfor %}
{% endif %}

## Priorities for Today
{% for priority in priorities %}
{{ loop.index }}. {{ priority }}
{% endfor %}

---
Generated on {{ date }} | Attendees: {{ attendees|join(', ') }}
```

**Config**:
```json
{
  "metadata": {
    "id": "daily-standup",
    "title": "Daily Standup Report"
  },
  "generatorSpecific": {
    "jinja2": {
      "template": "templates/standup.j2",
      "inputs": {
        "context": {
          "date": "{{date}}",
          "team_name": "Engineering",
          "achievements": "{{achievements}}",
          "blockers": "{{blockers}}",
          "priorities": "{{priorities}}",
          "attendees": "{{attendees}}"
        }
      }
    }
  }
}
```

**Usage**:
```bash
choracompose:generate_content --config-id daily-standup --context '{
  "date": "2025-10-21",
  "achievements": ["Shipped v1.4.2", "Fixed critical bug"],
  "blockers": [
    {"title": "API timeout", "description": "3rd party API slow", "owner": "Alice"}
  ],
  "priorities": ["Deploy v1.4.3", "Write release notes"],
  "attendees": ["Alice", "Bob", "Carol"]
}'
```

**Output**:
```markdown
# Daily Standup - 2025-10-21

## Team: Engineering

## Achievements
- Shipped v1.4.2
- Fixed critical bug

## Blockers
- **API timeout**: 3rd party API slow
  - Owner: Alice

## Priorities for Today
1. Deploy v1.4.3
2. Write release notes

---
Generated on 2025-10-21 | Attendees: Alice, Bob, Carol
```

**Why jinja2?**
- Loops (achievements, blockers, priorities)
- Conditionals (only show sections if data exists)
- Filters (join attendees with commas)
- Structured, deterministic output

---

## Generator 3: code_generation

### What It Does

**AI-powered generation** using Claude API:

- **Natural language**: Fluent, human-like text
- **Code generation**: Python, JavaScript, SQL, etc.
- **Context-aware**: Uses conversation history, examples
- **Non-deterministic**: Same prompt ≠ same output (by design)

**AI creativity**: Generates content you didn't explicitly template.

### When to Use

✅ **Use code_generation when**:

1. **Natural language required**: Documentation, explanations, summaries
2. **Code generation**: Python scripts, SQL queries, API clients
3. **Complex reasoning**: Multi-step logic, inference
4. **Flexible structure**: Output structure varies by context
5. **High-quality prose**: Blog posts, release notes, API descriptions

**Examples**:
- API documentation with natural language descriptions
- Code snippets based on specifications
- Release notes summarizing git commits
- Blog posts from bullet points
- Explanatory documentation

### When NOT to Use

❌ **Don't use code_generation when**:

1. **Determinism required**: Same input must produce same output
2. **Speed critical**: Need < 100ms response time (jinja2 is faster)
3. **Simple substitution**: Use template_fill or jinja2
4. **No API key**: Requires Anthropic API access (paid)
5. **Offline required**: Must work without internet

### Example: API Documentation

**Config**:
```json
{
  "metadata": {
    "id": "api-docs-generator",
    "title": "API Documentation Generator"
  },
  "generatorSpecific": {
    "code_generation": {
      "prompt": "Generate API documentation for the following endpoint:\n\nEndpoint: {{endpoint}}\nMethod: {{method}}\nDescription: {{description}}\nParameters: {{parameters}}\n\nInclude:\n- Overview paragraph\n- Parameter descriptions\n- Example request\n- Example response\n- Error codes\n\nWrite in friendly, conversational tone for developers.",
      "inputs": {
        "context": {
          "endpoint": "/api/users",
          "method": "POST",
          "description": "Create a new user",
          "parameters": {
            "name": "string (required)",
            "email": "string (required)",
            "role": "string (optional, default: 'user')"
          }
        }
      },
      "model": "claude-3-5-sonnet-20241022",
      "max_tokens": 2000
    }
  }
}
```

**Output** (example, non-deterministic):
```markdown
## POST /api/users

Create a new user account in the system. This endpoint handles user registration and returns the newly created user object with a unique ID.

### Parameters

- **name** (string, required): The user's full name. This will be displayed in the UI and used for identification.
- **email** (string, required): A valid email address. Must be unique across the system. Used for login and notifications.
- **role** (string, optional): User role determining permissions. Defaults to 'user'. Valid values: 'user', 'admin', 'moderator'.

### Example Request

```bash
curl -X POST https://api.example.com/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "role": "user"
  }'
```

### Example Response

```json
{
  "id": "usr_abc123",
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "role": "user",
  "created_at": "2025-10-21T10:30:00Z"
}
```

### Error Codes

- **400 Bad Request**: Missing required fields (name or email) or invalid email format
- **409 Conflict**: Email already exists in the system
- **500 Internal Server Error**: Unexpected server error during user creation
```

**Why code_generation?**
- Natural language descriptions (not just template placeholders)
- Example code generated contextually (curl command with actual values)
- Error codes explained with helpful context
- Conversational tone (as requested in prompt)

---

## Generator 4: demonstration

### What It Does

**BDD-style scenario generation** using Given-When-Then:

```
Scenario: User login
  Given a user account exists
  When the user submits valid credentials
  Then the user is redirected to dashboard
```

**Example-driven**: Define behavior through concrete examples.

### When to Use

✅ **Use demonstration when**:

1. **BDD scenarios**: Test scenarios, acceptance criteria
2. **Example-driven docs**: Show usage through examples
3. **Pattern libraries**: Reusable scenario templates
4. **QA documentation**: Test cases, user flows
5. **Behavior specifications**: Define system behavior

**Examples**:
- Cucumber/Gherkin test scenarios
- User acceptance criteria
- API usage examples
- Workflow documentation

### When NOT to Use

❌ **Don't use demonstration when**:

1. **Not example-driven**: Narrative documentation (use jinja2 or code_generation)
2. **No scenarios**: Simple text generation (use template_fill)
3. **Prose required**: Natural language paragraphs (use code_generation)

### Example: API Test Scenarios

**Config**:
```json
{
  "metadata": {
    "id": "api-test-scenarios",
    "title": "API Test Scenarios"
  },
  "generatorSpecific": {
    "demonstration": {
      "scenario_template": "Feature: {{feature_name}}\n\nScenario: {{scenario_name}}\n  Given {{given}}\n  When {{when}}\n  Then {{then}}",
      "examples": [
        {
          "feature_name": "User Authentication",
          "scenario_name": "Successful login",
          "given": "a user account exists with email 'alice@example.com'",
          "when": "the user submits correct credentials",
          "then": "the user receives an auth token"
        },
        {
          "feature_name": "User Authentication",
          "scenario_name": "Invalid credentials",
          "given": "a user account exists",
          "when": "the user submits incorrect password",
          "then": "the user receives a 401 Unauthorized error"
        }
      ]
    }
  }
}
```

**Output**:
```gherkin
Feature: User Authentication

Scenario: Successful login
  Given a user account exists with email 'alice@example.com'
  When the user submits correct credentials
  Then the user receives an auth token

Scenario: Invalid credentials
  Given a user account exists
  When the user submits incorrect password
  Then the user receives a 401 Unauthorized error
```

**Why demonstration?**
- BDD format (Given-When-Then)
- Example-driven (concrete test cases)
- Repeatable pattern (same structure for all scenarios)

---

## Decision Tree: Which Generator?

```
START: What are you generating?

┌─────────────────────────────────────────────────┐
│ 1. Do you need LOOPS or CONDITIONALS?          │
│    (e.g., iterate over a list, show/hide sections) │
└─────────┬───────────────────────────────────────┘
          │
          ├─ NO ───┐
          │        │
          │   ┌────▼────────────────────────────────┐
          │   │ 2. Is it simple text replacement?   │
          │   │    (e.g., "Hello {{name}}")         │
          │   └────┬────────────────────────────────┘
          │        │
          │        ├─ YES → USE **template_fill**
          │        │
          │        └─ NO ──┐
          │                │
          │           ┌────▼─────────────────────────┐
          │           │ 3. Is it BDD scenarios?      │
          │           │    (Given-When-Then)         │
          │           └────┬─────────────────────────┘
          │                │
          │                ├─ YES → USE **demonstration**
          │                │
          │                └─ NO ──→ USE **code_generation**
          │                          (natural language, code)
          │
          └─ YES ──┐
                   │
              ┌────▼───────────────────────────────┐
              │ 4. Is structure deterministic?     │
              │    (same structure every time)     │
              └────┬───────────────────────────────┘
                   │
                   ├─ YES → USE **jinja2**
                   │         (structured templates)
                   │
                   └─ NO ──→ USE **code_generation**
                             (flexible, AI-driven)
```

---

## Real-World Scenarios

### Scenario 1: Weekly Newsletter

**Requirements**:
- Fixed sections: "This Week", "Upcoming Events", "Featured Projects"
- Variable number of events/projects each week
- Structured, consistent format

**Decision**:
- **Loops**: Yes (iterate over events, projects)
- **Conditionals**: Yes (show "Upcoming Events" only if events exist)
- **Natural language**: No (structured format)

**Chosen generator**: ✅ **jinja2**

**Why not others?**
- ❌ template_fill: Can't handle loops
- ❌ code_generation: Overkill, deterministic structure is fine
- ❌ demonstration: Not BDD scenarios

---

### Scenario 2: API Client Code Generation

**Requirements**:
- Generate Python API client from OpenAPI spec
- Includes docstrings, type hints, error handling
- Natural, Pythonic code

**Decision**:
- **Code output**: Yes
- **Natural language**: Yes (docstrings)
- **Complex reasoning**: Yes (generate error handling logic)

**Chosen generator**: ✅ **code_generation**

**Why not others?**
- ❌ template_fill: Can't handle code complexity
- ❌ jinja2: Template would be too complex (500+ lines)
- ❌ demonstration: Not BDD scenarios

---

### Scenario 3: Configuration File with Placeholders

**Requirements**:
- Simple substitution: `{{API_URL}}`, `{{API_KEY}}`
- Fast execution (part of CI/CD pipeline)
- Deterministic output

**Decision**:
- **Loops**: No
- **Conditionals**: No
- **Simple replacement**: Yes

**Chosen generator**: ✅ **template_fill**

**Why not others?**
- ❌ jinja2: Overkill for simple substitution
- ❌ code_generation: Too slow, non-deterministic
- ❌ demonstration: Not BDD scenarios

---

### Scenario 4: Test Scenarios for User Flows

**Requirements**:
- BDD format (Given-When-Then)
- Multiple scenarios per feature
- Consistent structure

**Decision**:
- **BDD scenarios**: Yes
- **Example-driven**: Yes
- **Structured format**: Yes

**Chosen generator**: ✅ **demonstration**

**Why not others?**
- ❌ template_fill: No BDD support
- ❌ jinja2: Could work, but demonstration is purpose-built
- ❌ code_generation: Overkill, don't need AI creativity

---

## Performance Characteristics

### Execution Speed

| Generator | Typical Speed | Use Case |
|-----------|--------------|----------|
| **template_fill** | < 1ms | High-frequency generation (1000s/sec) |
| **jinja2** | 1-10ms | Medium-frequency (100s/sec) |
| **demonstration** | 1-5ms | Medium-frequency |
| **code_generation** | 500-3000ms | Low-frequency (1-10/sec) |

**Key insight**: If speed matters, avoid code_generation unless AI is essential.

### Cost Considerations

| Generator | Cost | Notes |
|-----------|------|-------|
| **template_fill** | Free | CPU only |
| **jinja2** | Free | CPU only |
| **demonstration** | Free | CPU only |
| **code_generation** | $$$ | Anthropic API ($0.003/1K input tokens, $0.015/1K output tokens) |

**Example cost**:
- Generating 1000 API docs with code_generation: ~$5-$10
- Generating 1000 reports with jinja2: ~$0 (negligible CPU cost)

### Output Quality

| Generator | Quality | Deterministic | Natural Language |
|-----------|---------|---------------|-----------------|
| **template_fill** | Fixed (template quality) | Yes | No |
| **jinja2** | Fixed (template quality) | Yes | No |
| **demonstration** | Fixed (template quality) | Yes | No |
| **code_generation** | Variable (AI-dependent) | No | Yes |

**Key insight**: code_generation is the only generator that produces natural language, but quality varies.

---

## Combining Generators: Artifact Configs

### Strategy: Different Generators for Different Parts

**Scenario**: Generate comprehensive project documentation

**Artifact structure**:
```json
{
  "artifact_id": "project-docs",
  "parts": [
    {
      "content_config_id": "readme-intro",
      "generator": "code_generation"  // AI-written intro
    },
    {
      "content_config_id": "api-reference",
      "generator": "jinja2"  // Structured API docs
    },
    {
      "content_config_id": "test-scenarios",
      "generator": "demonstration"  // BDD scenarios
    },
    {
      "content_config_id": "config-example",
      "generator": "template_fill"  // Simple variable substitution
    }
  ]
}
```

**Why this works**:
- Intro needs natural language → code_generation
- API reference is structured → jinja2
- Test scenarios are BDD → demonstration
- Config example is simple → template_fill

**Key insight**: Use the right tool for each part, not one generator for everything.

---

## Advanced: Custom Generators

### When Built-in Generators Aren't Enough

chora-compose supports **custom generators** via plugin system:

**Example use cases**:
- Database query generation (SQL from schema)
- GraphQL schema generation (from JSON schema)
- Diagram generation (PlantUML from data)
- Localization (i18n from base language)

**Implementation** (simplified):
```python
from chora_compose.generators import BaseGenerator

class SQLGenerator(BaseGenerator):
    def generate(self, context: dict) -> str:
        table = context["table"]
        columns = context["columns"]
        return f"CREATE TABLE {table} ({', '.join(columns)});"

# Register custom generator
chora_compose.register_generator("sql", SQLGenerator())
```

**Config usage**:
```json
{
  "generatorSpecific": {
    "sql": {
      "table": "users",
      "columns": ["id INT PRIMARY KEY", "name VARCHAR(255)"]
    }
  }
}
```

---

## Troubleshooting: Wrong Generator Chosen

### Symptom: Template is 500+ lines of jinja2

**Problem**: Template too complex, hard to maintain

**Solution**: Switch to code_generation
```json
{
  "generatorSpecific": {
    "code_generation": {
      "prompt": "Generate {{document_type}} with sections: {{sections}}",
      ...
    }
  }
}
```

### Symptom: code_generation output inconsistent

**Problem**: Need deterministic output, but using AI

**Solution**: Switch to jinja2
```json
{
  "generatorSpecific": {
    "jinja2": {
      "template": "structured-report.j2",
      ...
    }
  }
}
```

### Symptom: template_fill can't handle lists

**Problem**: Need loops, but using simple substitution

**Solution**: Switch to jinja2
```jinja2
{% for item in items %}
- {{ item }}
{% endfor %}
```

---

## Conclusion

**Choosing the right generator**:

1. **Simple substitution?** → template_fill
2. **Loops/conditionals?** → jinja2
3. **Natural language/code?** → code_generation
4. **BDD scenarios?** → demonstration

**Key principles**:
- Start simple (template_fill, jinja2) before using AI (code_generation)
- Use deterministic generators (template_fill, jinja2) when possible (faster, cheaper)
- Reserve code_generation for natural language or complex code
- Combine generators in artifact configs (best tool for each part)

**When in doubt**:
- Prototype with code_generation (fast to draft)
- Migrate to jinja2 if output is consistent (cheaper, faster)
- Keep code_generation if output benefits from AI creativity

---

## Related Documentation

**Diataxis References**:
- [Tutorial: Choosing Generators](../../tutorials/intermediate/03-choosing-generators.md) - Hands-on practice
- [How-To: Switch Between Generators](../../how-to/generators/switch-generators.md) - Migration guide
- [Reference: Generator API](../../reference/generators/generator-api.md) - Technical specifications

**Generator-Specific Docs**:
- [Reference: template_fill](../../reference/generators/template-fill.md)
- [Reference: jinja2](../../reference/generators/jinja2.md)
- [Reference: code_generation](../../reference/generators/code-generation.md)
- [Reference: demonstration](../../reference/generators/demonstration.md)

**Conceptual Relationships**:
- [Explanation: Configuration-Driven Development](../concepts/configuration-driven-development.md) - Why generators exist
- [Explanation: Content vs Artifacts](../concepts/content-vs-artifacts.md) - Combining generators

---

**Document Version**: 1.0
**Last Updated**: 2025-10-21
**Author**: Generated via chora-compose documentation sprint
