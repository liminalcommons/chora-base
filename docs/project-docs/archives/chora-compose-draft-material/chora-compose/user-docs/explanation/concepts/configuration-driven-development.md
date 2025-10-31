# Explanation: Configuration-Driven Development

**Purpose**: Understanding what configuration-driven development means, why chora-compose uses it, and when this approach makes sense.

**Related Tutorials**:
- [Your First Config](../../tutorials/getting-started/02-your-first-config.md)
- [Conversational Config Creation](../../tutorials/intermediate/02-conversational-config-creation.md)

**Related How-To Guides**:
- [Create Content Config](../../how-to/configs/create-content-config.md)
- [Create Artifact Config](../../how-to/configs/create-artifact-config.md)

**Related Reference**:
- [Content Config Schema](../../../schemas/content-schema.json)
- [Artifact Config Schema](../../../schemas/artifact-schema.json)

---

## Overview

Configuration-driven development (CDD) is an architectural pattern where **behavior is defined through data (configurations) rather than code**. In chora-compose, instead of writing Python code to generate content, you write JSON configurations that describe **what** you want to generate and **how** it should be generated.

This document explains the philosophy behind this approach, its benefits and trade-offs, and why it's particularly well-suited for Human-AI collaborative workflows.

---

## What is Configuration-Driven Development?

### The Core Concept

**Traditional Imperative Approach** (code-first):
```python
# You write code to describe HOW to do something
def generate_readme(project_name, description, features):
    content = f"# {project_name}\n\n"
    content += f"{description}\n\n"
    content += "## Features\n\n"
    for feature in features:
        content += f"- {feature}\n"
    return content

# To generate different content, you modify code
```

**Configuration-Driven Approach** (data-first):
```json
{
  "metadata": {
    "title": "Generate README"
  },
  "generator": "jinja2",
  "generatorSpecific": {
    "jinja2": {
      "template": "templates/readme.j2",
      "inputs": {
        "project_name": "{{project_name}}",
        "description": "{{description}}",
        "features": "{{features}}"
      }
    }
  }
}
```

```jinja2
{# templates/readme.j2 #}
# {{ project_name }}

{{ description }}

## Features

{% for feature in features %}
- {{ feature }}
{% endfor %}
```

**Key Difference**: In CDD, you separate **what** (configuration) from **how** (code). The code is generic and reusable; the configuration is specific to your use case.

---

## The Declarative Philosophy

### Declarative vs. Imperative

**Imperative** (tell the computer HOW):
```python
# Step-by-step instructions
content = ""
content += "# " + title + "\n"
content += "\n"
content += body + "\n"
# ... more steps
```

**Declarative** (tell the computer WHAT):
```json
{
  "title": "My Document",
  "body": "This is the content",
  "generator": "jinja2",
  "template": "document.j2"
}
```

**Why Declarative?**
- **Clarity**: Configurations are easier to read and understand
- **Composability**: Configurations can be combined, versioned, shared
- **Validation**: Schemas can ensure correctness before execution
- **Separation of Concerns**: Content authors don't need to be programmers

---

## Chora Compose's Implementation

### Two Types of Configurations

#### 1. Content Configurations

**Purpose**: Define how to generate individual pieces of content

**Structure**:
```json
{
  "metadata": {
    "title": "API Documentation",
    "description": "Generate API docs from OpenAPI spec"
  },
  "generator": "jinja2",
  "generatorSpecific": {
    "jinja2": {
      "template": "templates/api-docs.j2",
      "inputs": {
        "api_spec": "{{api_spec}}",
        "api_version": "{{version}}"
      }
    }
  },
  "outputPath": "docs/api/{{version}}.md"
}
```

**Key Elements**:
- **Metadata**: Human-readable information
- **Generator**: Which generation strategy to use
- **Generator-specific config**: Parameters for that generator
- **Output path**: Where to save the result

#### 2. Artifact Configurations

**Purpose**: Define how to assemble multiple content pieces into complex artifacts

**Structure**:
```json
{
  "metadata": {
    "title": "Complete Documentation Site"
  },
  "sections": [
    {
      "contentConfigId": "api-docs",
      "order": 1
    },
    {
      "contentConfigId": "user-guide",
      "order": 2
    }
  ],
  "composition": {
    "strategy": "concatenate",
    "separator": "\n\n---\n\n"
  },
  "outputPath": "docs/complete-site.md"
}
```

**Key Elements**:
- **Sections**: Which content configs to include
- **Composition strategy**: How to combine them
- **Dependencies**: Ordering and relationships

### JSON Schema Validation

Every configuration is validated against a JSON Schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["metadata", "generator", "generatorSpecific"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["title"],
      "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"}
      }
    },
    "generator": {
      "type": "string",
      "enum": ["jinja2", "demonstration", "code_generation", "bdd_scenario"]
    }
  }
}
```

**Benefits**:
- Catch errors before execution
- IDE autocomplete and validation
- Self-documenting structure
- Version compatibility checking

---

## Why Configuration-Driven?

### 1. Separation of Concerns

**Problem without CDD**:
```python
# Everything mixed together
def generate_report(data):
    # Business logic
    stats = calculate_stats(data)

    # Formatting logic
    output = "<h1>Report</h1>\n"
    output += f"<p>Total: {stats['total']}</p>\n"

    # File I/O logic
    with open("report.html", "w") as f:
        f.write(output)

    return output
```

**Solution with CDD**:
```json
{
  "metadata": {"title": "Stats Report"},
  "generator": "jinja2",
  "generatorSpecific": {
    "jinja2": {
      "template": "report.j2",
      "inputs": {"stats": "{{stats}}"}
    }
  },
  "outputPath": "report.html"
}
```

**Separation Achieved**:
- **Business logic**: Separate Python module
- **Presentation logic**: Template file
- **Configuration**: JSON file
- **Execution**: Generic engine

Each can evolve independently.

### 2. Non-Programmers Can Contribute

**Traditional Approach** (requires coding):
```python
# Content author must write Python
def my_custom_generator(data):
    # ... 50 lines of code ...
```

**CDD Approach** (no coding required):
```json
{
  "metadata": {"title": "My Content"},
  "generator": "jinja2",
  "generatorSpecific": {
    "jinja2": {
      "template": "my-template.j2",
      "inputs": {"data": "{{context}}"}
    }
  }
}
```

**Impact**: Technical writers, product managers, and other non-programmers can create and modify content generation workflows.

### 3. Versioning and Auditing

**Configuration as Code** benefits:

```bash
# Configurations are version-controlled
git log configs/content/daily-report/

# See what changed
git diff v1.0..v2.0 configs/content/daily-report/report-content.json

# Rollback if needed
git checkout v1.0 configs/content/daily-report/
```

**Benefits**:
- Track who changed what and when
- Understand evolution of content generation
- Revert to previous versions easily
- Audit trail for compliance

### 4. Testing and Validation

**Configurations can be tested without execution**:

```python
# Validate schema
from chora_compose import ConfigLoader

config = ConfigLoader.load("configs/content/my-config.json")
# Raises ValidationError if invalid

# Test with mock data
result = config.test({"name": "Test"})
assert "Test" in result
```

**Benefits**:
- Fast feedback loop
- Catch errors early
- Test edge cases easily
- No side effects during testing

### 5. AI-Friendly

**Configurations are easier for AI to generate than code**:

**Human**: "Create a config to generate API documentation from OpenAPI specs"

**AI** (can generate valid JSON):
```json
{
  "metadata": {
    "title": "API Documentation Generator",
    "description": "Generates markdown API docs from OpenAPI 3.0 specs"
  },
  "generator": "jinja2",
  "generatorSpecific": {
    "jinja2": {
      "template": "templates/api-docs.j2",
      "inputs": {
        "openapi_spec": "{{spec}}",
        "api_title": "{{spec.info.title}}",
        "api_version": "{{spec.info.version}}"
      }
    }
  },
  "outputPath": "docs/api/v{{spec.info.version}}.md"
}
```

**Why easier**:
- Structured format (JSON)
- Schema-validated (prevents errors)
- Clear conventions
- No syntax ambiguity

This is why chora-compose has **conversational config creation** - AI can generate valid configs through conversation.

---

## Trade-offs and Limitations

### What You Gain

✅ **Accessibility**: Non-programmers can create workflows
✅ **Maintainability**: Changes to configs don't require code changes
✅ **Testability**: Validate configs without execution
✅ **Versioning**: Git-friendly configuration files
✅ **AI-Friendliness**: Easier for AI to generate and modify
✅ **Reusability**: Configs can be shared and composed
✅ **Clarity**: Intent is clear from configuration structure

### What You Sacrifice

❌ **Flexibility**: Can't express arbitrary logic in configs
❌ **Learning Curve**: Need to learn JSON Schema and structure
❌ **Verbosity**: Configs can be longer than equivalent code
❌ **Indirection**: One more layer between intent and execution
❌ **Dynamic Behavior**: Complex runtime logic is harder

### When NOT to Use CDD

**1. Highly Dynamic Behavior**

If your logic is:
```python
if user.is_premium() and date.today().weekday() < 5:
    content = complex_calculation(user.history)
else:
    content = simple_template(user.name)
```

This is hard to express in config. Better as code.

**2. Unique One-Off Scripts**

If you'll only run something once:
```python
# Quick data migration
for record in database:
    record.update(transform(record))
```

Creating a config is overkill. Just write the script.

**3. Performance-Critical Paths**

Configs add parsing/validation overhead:
```python
# Hot path - runs millions of times
for item in huge_dataset:
    result = fast_transform(item)  # Direct code is faster
```

For bulk processing, code may be more efficient.

### The Sweet Spot

CDD works best when:
- ✅ **Repeatable**: You'll run it multiple times
- ✅ **Structured**: Clear inputs → outputs
- ✅ **Collaborative**: Multiple people need to understand/modify
- ✅ **Evolving**: Requirements change over time
- ✅ **Validated**: Need schema checking before execution

**chora-compose use case**: Generating documentation, reports, artifacts - all fit this profile perfectly.

---

## Real-World Example

### Traditional Approach

**Problem**: Generate weekly engineering reports

```python
# weekly_report.py (changes every week)
def generate_report():
    commits = get_git_commits(last_week())
    prs = get_merged_prs(last_week())
    issues = get_closed_issues(last_week())

    output = "# Weekly Engineering Report\n\n"
    output += f"## Commits ({len(commits)})\n\n"
    for commit in commits:
        output += f"- {commit.message} by {commit.author}\n"

    output += f"\n## Merged PRs ({len(prs)})\n\n"
    for pr in prs:
        output += f"- #{pr.number}: {pr.title}\n"

    # ... more formatting ...

    with open(f"reports/week-{week_number}.md", "w") as f:
        f.write(output)
```

**Problems**:
- Code changes every time format changes
- Non-programmers can't modify
- Hard to test without running
- Difficult to version templates

### Configuration-Driven Approach

**Step 1: Define Config** (`configs/content/reports/weekly-engineering.json`)

```json
{
  "metadata": {
    "title": "Weekly Engineering Report",
    "description": "Generates report from git, PR, and issue data"
  },
  "generator": "jinja2",
  "generatorSpecific": {
    "jinja2": {
      "template": "templates/weekly-report.j2",
      "inputs": {
        "week_number": "{{week}}",
        "commits": "{{commits}}",
        "prs": "{{prs}}",
        "issues": "{{issues}}"
      }
    }
  },
  "outputPath": "reports/week-{{week}}.md"
}
```

**Step 2: Create Template** (`templates/weekly-report.j2`)

```jinja2
# Weekly Engineering Report - Week {{ week_number }}

## Commits ({{ commits|length }})

{% for commit in commits %}
- {{ commit.message }} by {{ commit.author }}
{% endfor %}

## Merged PRs ({{ prs|length }})

{% for pr in prs %}
- #{{ pr.number }}: {{ pr.title }}
{% endfor %}

## Closed Issues ({{ issues|length }})

{% for issue in issues %}
- #{{ issue.number }}: {{ issue.title }}
{% endfor %}
```

**Step 3: Use** (via CLI or MCP tool)

```bash
# Via CLI
chora-compose generate weekly-engineering --context '{"week": 42, "commits": [...], "prs": [...], "issues": [...]}'

# Or via n8n workflow
# 1. HTTP Request: Fetch git data
# 2. MCP Tool: choracompose:generate_content with config ID
# 3. Slack: Post report
```

**Benefits Achieved**:
- Template can be edited by non-programmers
- Config is version-controlled
- Easy to test with sample data
- Format changes don't require code changes
- Can be triggered from n8n, CLI, or conversationally

---

## Comparison with Other Approaches

### vs. Code-First (Traditional)

| Aspect | Code-First | Config-Driven |
|--------|------------|---------------|
| **Flexibility** | ✅ Unlimited | ⚠️ Limited by schema |
| **Accessibility** | ❌ Requires programming | ✅ Non-programmers can use |
| **Testability** | ⚠️ Must execute code | ✅ Validate before execution |
| **Versioning** | ⚠️ Code changes | ✅ Config changes |
| **AI Generation** | ❌ Complex | ✅ Straightforward |

**When to choose**: Config-driven for repeatable, structured workflows; code-first for one-off scripts or complex logic.

### vs. Low-Code Platforms

| Aspect | Low-Code Platform | Config-Driven |
|--------|-------------------|---------------|
| **Vendor Lock-in** | ❌ High | ✅ Open standards (JSON) |
| **Version Control** | ⚠️ Platform-specific | ✅ Git-friendly |
| **Customization** | ⚠️ Limited | ✅ Extensible via plugins |
| **Cost** | ❌ Often expensive | ✅ Free/open-source |

**When to choose**: Config-driven for developer teams who want control; low-code for business users prioritizing ease of use.

### vs. Template Engines Alone

| Aspect | Template Engine | Config + Template |
|--------|-----------------|-------------------|
| **Structure** | ❌ No standard | ✅ JSON Schema |
| **Validation** | ❌ Runtime only | ✅ Pre-execution |
| **Composition** | ⚠️ Manual | ✅ Artifact configs |
| **Metadata** | ❌ None | ✅ Built-in |

**When to choose**: Config + template for production workflows; template alone for quick prototypes.

---

## Best Practices

### 1. Keep Configs Focused

**Bad** (too much in one config):
```json
{
  "metadata": {"title": "Everything Generator"},
  "generator": "jinja2",
  "generatorSpecific": {
    "jinja2": {
      "template": "all-the-things.j2",
      "inputs": {
        "docs": "{{docs}}",
        "tests": "{{tests}}",
        "reports": "{{reports}}",
        "emails": "{{emails}}"
      }
    }
  }
}
```

**Good** (single responsibility):
```json
{
  "metadata": {"title": "API Documentation"},
  "generator": "jinja2",
  "generatorSpecific": {
    "jinja2": {
      "template": "api-docs.j2",
      "inputs": {"spec": "{{spec}}"}
    }
  }
}
```

**Principle**: One config, one purpose. Use artifact configs to combine.

### 2. Use Descriptive Metadata

**Bad**:
```json
{
  "metadata": {"title": "Config 1"}
}
```

**Good**:
```json
{
  "metadata": {
    "title": "Daily Engineering Metrics Report",
    "description": "Generates HTML dashboard with git stats, PR velocity, and issue trends",
    "tags": ["reporting", "engineering", "daily"],
    "version": "2.1.0"
  }
}
```

### 3. Version Your Configurations

```bash
configs/
└── content/
    └── reports/
        ├── weekly-engineering-v1.json  # Legacy
        ├── weekly-engineering-v2.json  # Current
        └── weekly-engineering.json     # Symlink to v2
```

### 4. Test Configs in Isolation

```python
# tests/test_configs.py
def test_weekly_report_config():
    config = ConfigLoader.load("configs/content/reports/weekly-engineering.json")

    test_data = {
        "week": 42,
        "commits": [{"message": "Test", "author": "Alice"}],
        "prs": [],
        "issues": []
    }

    result = config.test(test_data)
    assert "Week 42" in result
    assert "Alice" in result
```

---

## Summary

Configuration-driven development is not just a technical choice - it's a **philosophy of separation** between what you want to achieve (config) and how it's achieved (code).

**For chora-compose**, CDD enables:
- ✅ **Conversational workflows**: AI can generate/modify configs through conversation
- ✅ **Human-AI collaboration**: Humans define intent, AI executes
- ✅ **Accessibility**: Non-programmers can create sophisticated workflows
- ✅ **Maintainability**: Changes to content don't require code changes
- ✅ **Composability**: Configs can be combined into complex artifacts

**The key insight**: When you separate **what** from **how**, you unlock new forms of collaboration - especially with AI.

---

**Related Reading**:
- [Content vs. Artifacts](content-vs-artifacts.md) - Understanding the two config types
- [Human-AI Collaboration Philosophy](human-ai-collaboration-philosophy.md) - Why this matters for AI workflows
- [Config-Driven Architecture](../architecture/config-driven-architecture.md) - Implementation details
- [Tutorial: Your First Config](../../tutorials/getting-started/02-your-first-config.md) - Hands-on practice

**External References**:
- [The Twelve-Factor App](https://12factor.net/config) - Config management principles
- [JSON Schema](https://json-schema.org/) - Configuration validation
- [Declarative vs. Imperative Programming](https://en.wikipedia.org/wiki/Declarative_programming)

---

**Document Version**: 1.0
**Last Updated**: 2025-10-21
**Next Review**: After user feedback on accessibility
