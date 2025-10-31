# When to Use Which Generator: A Decision Framework

**Purpose**: Understand the underlying principles for selecting the right generator, going beyond feature comparison to explore trade-offs, migration paths, and decision frameworks.

**Audience**: Developers integrating chora-compose, technical leads making architecture decisions, users evaluating generator options.

---

## Overview

Chora Compose provides five built-in generators, each optimized for different use cases. Choosing the wrong generator leads to:
- Overcomplex configs (using jinja2 for simple substitution)
- Underpowered generation (using demonstration for dynamic content)
- Cost/performance issues (using code_generation for templates)
- Maintenance burden (fighting against generator limitations)

This guide explains **WHY** each generator exists, **WHEN** to use it, and **HOW** to decide between similar options.

---

## The Complexity-Capability Spectrum

Generators exist on a spectrum from simple/limited to complex/powerful:

```
Simple ←─────────────────────────────────────────────→ Complex
       (Fast, Limited)                    (Slow, Powerful)

demonstration → template_fill → bdd_scenario → jinja2 → code_generation
   │                │               │            │            │
   Static        Variables      Structured    Logic &     AI-powered
   only          only           assembly      loops       generation
```

**Key principle**: Use the **simplest** generator that meets your needs.

**Why?**
- Simpler = faster execution
- Simpler = easier to debug
- Simpler = fewer dependencies
- Simpler = lower maintenance cost

**Anti-pattern**: "I might need loops later, so I'll use jinja2 from the start"
- **Better**: Start with template_fill, migrate to jinja2 if/when needed

---

## Generator Decision Framework

### Step 1: Is Content Static or Dynamic?

**Question**: Does the output change based on input data?

```
└─ Static (always the same)?
   └─ Use: demonstration
   └─ Example: Legal disclaimers, standard templates, boilerplate

└─ Dynamic (changes with input)?
   └─ Continue to Step 2
```

**Key insight**: If you answer "static," stop here. `demonstration` is always the right choice for unchanging content.

**Why `demonstration` for static?**
- Zero overhead (no parsing, no substitution)
- Impossible to have runtime errors
- Human-readable (what you see is what you get)
- Version controlled (content in config, not code)

**Example scenarios**:

| Scenario | Static or Dynamic? | Generator |
|----------|-------------------|-----------|
| MIT License text | Static | `demonstration` |
| Release notes template | Dynamic (version, date) | `template_fill` |
| README boilerplate | Static | `demonstration` |
| API documentation from schema | Dynamic (endpoints, schemas) | `jinja2` |

---

### Step 2: What Kind of Dynamic Content?

**Question**: What type of customization do you need?

```
└─ Simple variable substitution only?
   └─ Use: template_fill
   └─ Example: "Hello, {{name}}! Your balance is {{amount}}."

└─ Need conditional logic (if/else)?
   └─ Use: jinja2
   └─ Example: "{% if is_premium %}Premium features{% else %}Basic features{% endif %}"

└─ Need loops over data?
   └─ Use: jinja2
   └─ Example: "{% for item in items %}{{ item }}{% endfor %}"

└─ Generating code from natural language?
   └─ Use: code_generation
   └─ Example: "Create a function that validates email addresses"

└─ Generating BDD test scenarios?
   └─ Use: bdd_scenario_assembly
   └─ Example: Gherkin feature files with Given/When/Then
```

**Decision matrix**:

| Need | template_fill | jinja2 | code_generation | bdd_scenario |
|------|--------------|--------|-----------------|--------------|
| Variables | ✅ | ✅ | ✅ | ✅ |
| Conditionals (if/else) | ❌ | ✅ | ✅ (via AI) | ❌ |
| Loops (for/each) | ❌ | ✅ | ✅ (via AI) | ❌ |
| Filters (\|upper, \|length) | ❌ | ✅ | ❌ | ❌ |
| Template inheritance | ❌ | ✅ | ❌ | ❌ |
| AI-powered generation | ❌ | ❌ | ✅ | ❌ |
| Gherkin structure | ❌ | ❌* | ❌ | ✅ |

*You can generate Gherkin with jinja2, but bdd_scenario provides structure and validation

---

### Step 3: Consider Non-Functional Requirements

Even if multiple generators meet functional requirements, non-functional factors matter:

#### Performance

| Generator | Typical Speed | Use When |
|-----------|--------------|----------|
| `demonstration` | <1ms | Always fast (no processing) |
| `template_fill` | <1ms | Small templates, few variables |
| `bdd_scenario` | <5ms | Small to medium Gherkin files |
| `jinja2` | <10ms | Complex templates acceptable |
| `code_generation` | 10-30s | Quality > speed |

**Decision rule**: If you need <100ms response time (e.g., real-time generation), avoid `code_generation`.

#### Cost

| Generator | Cost per Generation | Monthly Cost (1000 runs/day) |
|-----------|---------------------|------------------------------|
| `demonstration` | $0 | $0 |
| `template_fill` | $0 | $0 |
| `bdd_scenario` | $0 | $0 |
| `jinja2` | $0 | $0 |
| `code_generation` | $0.01-0.10 | $300-3000 |

**Decision rule**: If cost is a concern, avoid `code_generation` unless AI is essential.

#### Connectivity

| Generator | Requires Internet? | Fallback if Offline? |
|-----------|-------------------|----------------------|
| `demonstration` | No | N/A (always works) |
| `template_fill` | No | N/A (always works) |
| `bdd_scenario` | No | N/A (always works) |
| `jinja2` | No | N/A (always works) |
| `code_generation` | Yes | None (fails) |

**Decision rule**: If offline operation required, avoid `code_generation`.

#### Determinism

| Generator | Deterministic? | Notes |
|-----------|----------------|-------|
| `demonstration` | Always | Same input → same output |
| `template_fill` | Always | Same input → same output |
| `bdd_scenario` | Always | Same input → same output |
| `jinja2` | Always | Same input → same output |
| `code_generation` | Configurable | Use `temperature=0.0` for determinism |

**Decision rule**: If reproducibility required (e.g., CI/CD), use `temperature=0.0` with `code_generation` or prefer other generators.

---

## Deep Dive: Generator Selection Scenarios

### Scenario 1: Release Announcements

**Requirements**:
- Title with product name and version
- Release date
- List of features
- Download links

**Analysis**:

```
├─ Static? No (version, date, features change)
├─ Need conditionals? No
├─ Need loops? No (features pre-formatted as string)
└─ Need variables? Yes
```

**Choice**: `template_fill`

**Why not jinja2?** No loops needed (features already formatted as "- Feature 1\n- Feature 2").

**Config**:

```json
{
  "type": "template_fill",
  "template": "# {{product_name}} {{version}} Released!\n\n**Date**: {{release_date}}\n\n## What's New\n\n{{features}}\n\n[Download]({{download_url}})"
}
```

**Context**:

```json
{
  "product_name": "Chora Compose",
  "version": "1.0.0",
  "release_date": "2025-11-01",
  "features": "- Template Fill Generator\n- BDD Scenario Generator",
  "download_url": "https://example.com/download"
}
```

### Scenario 2: API Documentation from OpenAPI Spec

**Requirements**:
- Loop over endpoints
- Conditional sections (if endpoint has parameters, show parameters table)
- Filter: capitalize HTTP methods
- Nested loops (endpoints → parameters)

**Analysis**:

```
├─ Static? No (endpoints change)
├─ Need conditionals? Yes (if parameters exist)
├─ Need loops? Yes (over endpoints, over parameters)
└─ Need filters? Yes (capitalize, default values)
```

**Choice**: `jinja2`

**Why not template_fill?** Needs loops and conditionals (too complex for simple substitution).

**Why not code_generation?** Documentation structure is predictable (no AI needed).

**Template** (jinja2):

```jinja2
# API Documentation

{% for endpoint in endpoints %}
## {{ endpoint.method|upper }} {{ endpoint.path }}

{{ endpoint.description }}

{% if endpoint.parameters %}
**Parameters**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
{% for param in endpoint.parameters %}
| {{ param.name }} | {{ param.type }} | {{ param.required|default("No") }} | {{ param.description }} |
{% endfor %}
{% endif %}

**Response**: {{ endpoint.response_code }}

---

{% endfor %}
```

**Context**:

```json
{
  "endpoints": [
    {
      "method": "get",
      "path": "/users",
      "description": "List all users",
      "parameters": [
        {"name": "limit", "type": "int", "required": false, "description": "Max results"}
      ],
      "response_code": 200
    }
  ]
}
```

### Scenario 3: Utility Function Generation

**Requirements**:
- Generate Python function from natural language description
- Handle edge cases (email validation, phone parsing, etc.)
- Idiomatic code (not template-based)

**Analysis**:

```
├─ Static? No (different functions)
├─ Need logic? Yes (complex validation logic)
├─ Can be templated? No (logic too complex for templates)
└─ Need AI? Yes (understand intent, handle edge cases)
```

**Choice**: `code_generation`

**Why not jinja2?** Code logic too complex to template effectively.

**Why code_generation?** AI excels at generating idiomatic code from descriptions.

**Config**:

```json
{
  "type": "code_generation",
  "generation_config": {
    "instructions": {
      "system_prompt": "Generate production-ready Python functions with docstrings and type hints.",
      "user_prompt": "Create a function that validates email addresses according to RFC 5322. Handle edge cases like plus addressing, subdomains, and international domains."
    },
    "temperature": 0.0,
    "max_tokens": 1000
  }
}
```

**Output** (AI-generated):

```python
import re
from typing import Optional

def validate_email(email: str) -> bool:
    """
    Validate email address according to RFC 5322.

    Supports:
    - Plus addressing (user+tag@example.com)
    - Subdomains (user@mail.example.com)
    - International domains (user@example.co.uk)

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

### Scenario 4: BDD Test Scenarios

**Requirements**:
- Gherkin syntax (Feature, Scenario, Given/When/Then)
- Multiple scenarios per feature
- Background steps
- Scenario outlines with examples tables
- Tags for test organization

**Analysis**:

```
├─ Static? No (scenarios change)
├─ Need structure? Yes (Gherkin format)
├─ Can use jinja2? Yes (but verbose, error-prone)
└─ Specialized generator available? Yes (bdd_scenario_assembly)
```

**Choice**: `bdd_scenario_assembly`

**Why not jinja2?** bdd_scenario provides:
- Gherkin validation (ensures valid syntax)
- Structured config (less error-prone)
- Step keyword validation (Given, When, Then)
- Built-in indentation (correct formatting)

**Why not template_fill?** Gherkin structure is complex (nested indentation, examples tables).

**Config**:

```json
{
  "type": "bdd_scenario_assembly",
  "generation_config": {
    "feature": {
      "title": "User Login",
      "tags": ["@smoke"]
    },
    "scenarios": [{
      "title": "Successful login",
      "steps": [
        "Given I am on the login page",
        "When I enter valid credentials",
        "Then I should see the dashboard"
      ]
    }]
  }
}
```

**Output**:

```gherkin
@smoke
Feature: User Login

Scenario: Successful login
  Given I am on the login page
  When I enter valid credentials
  Then I should see the dashboard
```

---

## Common Decision Patterns

### Pattern 1: Start Simple, Migrate Later

**Principle**: Begin with the simplest generator, upgrade when you hit limitations.

**Example**:

```
Start: demonstration (static boilerplate)
  ↓ (need to add version number)
Upgrade: template_fill (add {{version}} variable)
  ↓ (need conditional premium features section)
Upgrade: jinja2 (add {% if is_premium %})
```

**Why this works**:
- Migration is straightforward (add complexity incrementally)
- Avoid premature complexity (YAGNI principle)
- Each migration has clear motivation (hit actual limitation)

**Migration example**:

**demonstration → template_fill**:

```json
// Before (demonstration)
{
  "type": "demonstration",
  "template": "# MyApp v1.0.0\n\nReleased: 2025-01-01"
}

// After (template_fill)
{
  "type": "template_fill",
  "template": "# {{app_name}} v{{version}}\n\nReleased: {{date}}"
}
```

**template_fill → jinja2**:

```json
// Before (template_fill, features as pre-formatted string)
{
  "type": "template_fill",
  "template": "# Features\n\n{{features}}"
}
// Context: {"features": "- Feature 1\n- Feature 2"}

// After (jinja2, features as list)
{
  "type": "jinja2",
  "template": "# Features\n\n{% for feature in features %}- {{ feature }}\n{% endfor %}"
}
// Context: {"features": ["Feature 1", "Feature 2"]}
```

### Pattern 2: Choose by Output Format

**Principle**: Some generators are optimized for specific output formats.

| Output Format | Recommended Generator | Why |
|---------------|----------------------|-----|
| Markdown | `template_fill` or `jinja2` | Human-readable templates |
| Gherkin | `bdd_scenario_assembly` | Built-in validation |
| Python code | `code_generation` or `jinja2` | AI for logic, templates for boilerplate |
| JSON/YAML | `jinja2` | Precise control over structure |
| HTML | `jinja2` | Template inheritance, conditionals |
| Plain text | `template_fill` | Simple substitution |

**Example**: Generating JSON

**Bad** (template_fill, easy to create invalid JSON):

```json
{
  "type": "template_fill",
  "template": "{\n  \"name\": \"{{name}}\",\n  \"age\": {{age}}\n}"
}
```

**Problem**: If `name` contains `"`, JSON is invalid.

**Good** (jinja2, with escaping):

```jinja2
{
  "name": "{{ name|tojson }}",
  "age": {{ age }}
}
```

**Benefit**: jinja2's `tojson` filter handles escaping automatically.

### Pattern 3: Choose by Audience

**Principle**: Non-technical users need simpler generators.

| User Technical Level | Recommended Generator | Why |
|----------------------|----------------------|-----|
| Non-technical (marketing, PMs) | `demonstration` or `template_fill` | Human-readable, no programming |
| Semi-technical (QA, docs writers) | `template_fill` or `bdd_scenario` | Structured but approachable |
| Technical (developers) | `jinja2` or `code_generation` | Full power, comfortable with code |

**Example**: Marketing team creating release emails

**Bad** (jinja2, too complex for non-devs):

```jinja2
{% if user.is_premium %}
  {% for feature in premium_features %}
    {{ feature|capitalize }}
  {% endfor %}
{% endif %}
```

**Good** (template_fill, simple substitution):

```
Hi {{customer_name}},

{{product_name}} {{version}} is now available!

{{features}}

Download: {{download_link}}
```

**Benefit**: Marketing can edit variables without understanding loops/conditionals.

---

## Trade-off Analysis

### Trade-off 1: Simplicity vs Power

**Axis**: Ease of use ↔ Capability

```
Ease of use ←──────────────────────────→ Capability

demonstration                         jinja2/code_generation
   │                                          │
   ├─ ✅ Zero learning curve                  ├─ ✅ Unlimited capability
   ├─ ✅ No syntax errors                     ├─ ✅ Handles any logic
   ├─ ❌ No customization                     ├─ ❌ Steep learning curve
   └─ ❌ Limited use cases                    └─ ❌ Complex debugging
```

**When to favor simplicity**:
- Non-technical users
- Simple use cases
- Fast iteration needed
- Maintenance burden a concern

**When to favor power**:
- Complex requirements
- Technical users
- One-time setup (complexity amortized)
- Flexibility critical

### Trade-off 2: Template-Based vs AI-Powered

**Axis**: Predictability ↔ Intelligence

```
Predictable ←──────────────────────────→ Intelligent

template_fill/jinja2                 code_generation
   │                                          │
   ├─ ✅ Deterministic                        ├─ ✅ Understands intent
   ├─ ✅ No API costs                         ├─ ✅ Handles complexity
   ├─ ✅ Fast (<10ms)                         ├─ ❌ Non-deterministic*
   ├─ ❌ Requires explicit templates          ├─ ❌ Costs $0.01-0.10/run
   └─ ❌ Cannot handle novel scenarios        └─ ❌ Slow (10-30s)
```

*Use `temperature=0.0` for determinism

**When to use templates**:
- Predictable output structure
- Cost-sensitive
- Fast response required
- Offline operation needed

**When to use AI**:
- Complex logic generation
- Novel scenarios (not templatable)
- Quality > cost
- Internet connectivity available

### Trade-off 3: Specialized vs General-Purpose

**Axis**: Specialized ↔ General-purpose

```
Specialized ←──────────────────────────→ General-purpose

bdd_scenario                         jinja2
   │                                          │
   ├─ ✅ Optimized for Gherkin                ├─ ✅ Works for any format
   ├─ ✅ Built-in validation                  ├─ ✅ Maximum flexibility
   ├─ ✅ Structured config                    ├─ ❌ No domain validation
   ├─ ❌ Only for BDD tests                   ├─ ❌ More verbose configs
   └─ ❌ Cannot customize format              └─ ❌ Easier to make mistakes
```

**When to use specialized**:
- Exact use case match (e.g., Gherkin for bdd_scenario)
- Want validation/structure
- Prefer concise configs

**When to use general-purpose**:
- No specialized generator available
- Need full control
- Custom format required

---

## Migration Strategies

### Strategy 1: Incremental Complexity

Add complexity only when needed.

**Step 1**: Start with `demonstration`
- All content is static

**Step 2**: Migrate to `template_fill`
- Trigger: Need to parameterize (version, date, names)
- Effort: Low (wrap variables in `{{}}`)

**Step 3**: Migrate to `jinja2`
- Trigger: Need conditionals or loops
- Effort: Medium (learn jinja2 syntax)

**Example progression**:

```
Version 1 (demonstration):
"# MyApp v1.0.0\n\nReleased: 2025-01-01"

Version 2 (template_fill):
"# {{app_name}} v{{version}}\n\nReleased: {{date}}"

Version 3 (jinja2):
"# {{app_name}} v{{version}}\n\n{% if has_breaking_changes %}⚠️ Breaking changes{% endif %}\n\nReleased: {{date}}"
```

### Strategy 2: Hybrid Approach

Use multiple generators in one artifact.

**Pattern**: Combine specialized generators with general-purpose ones.

**Example**: Documentation artifact

```json
{
  "type": "artifact",
  "parts": [
    {
      "content_config_id": "license",
      "generator": "demonstration"  // Static legal text
    },
    {
      "content_config_id": "readme",
      "generator": "template_fill"  // Parameterized intro
    },
    {
      "content_config_id": "api-docs",
      "generator": "jinja2"  // Complex API documentation
    },
    {
      "content_config_id": "tests",
      "generator": "bdd_scenario_assembly"  // BDD scenarios
    }
  ]
}
```

**Benefit**: Use the right tool for each part (no compromises).

### Strategy 3: Fallback Hierarchy

Prefer simple generators, fall back to complex ones.

**Hierarchy**:

```
1. demonstration (if static)
   ↓ (if not static)
2. template_fill (if variables only)
   ↓ (if logic needed)
3. bdd_scenario_assembly (if Gherkin)
   OR
3. jinja2 (if templates work)
   ↓ (if templates insufficient)
4. code_generation (if AI needed)
```

**Example decision**:

```
Q: Is output static?
   ├─ Yes → demonstration ✓
   └─ No
      Q: Need loops/conditionals?
         ├─ No → template_fill ✓
         └─ Yes
            Q: Generating Gherkin?
               ├─ Yes → bdd_scenario ✓
               └─ No
                  Q: Can be templated?
                     ├─ Yes → jinja2 ✓
                     └─ No → code_generation ✓
```

---

## Performance Considerations

### Generator Performance Profiles

| Generator | Startup | Per-Generation | Scalability |
|-----------|---------|----------------|-------------|
| `demonstration` | Instant | <1ms | Linear (no overhead) |
| `template_fill` | Instant | <1ms | Linear (regex parsing) |
| `bdd_scenario` | Instant | <5ms | Linear (validation overhead) |
| `jinja2` | <10ms (template compile) | <10ms | Sub-linear (template cached) |
| `code_generation` | N/A (API call) | 10-30s | Constant (API latency) |

**Key insights**:

1. **Batch operations**: jinja2 has compilation overhead, but amortizes over multiple runs
   ```python
   # ❌ Bad: Compile template 1000 times
   for data in datasets:
       generator = Jinja2Generator()  # Re-compiles template
       output = generator.generate(config, data)

   # ✅ Good: Compile once, reuse
   generator = Jinja2Generator()
   for data in datasets:
       output = generator.generate(config, data)  # Reuses compiled template
   ```

2. **Real-time generation**: Avoid `code_generation` for <100ms response requirements

3. **High-volume**: Prefer `demonstration` or `template_fill` for 1000+ generations/sec

### Cost-Performance Optimization

**Scenario**: Generate 10,000 API documentation pages

**Option 1**: `code_generation`
- Cost: 10,000 × $0.05 = **$500**
- Time: 10,000 × 20s = **55 hours**

**Option 2**: `jinja2`
- Cost: **$0** (local)
- Time: 10,000 × 10ms = **100 seconds**

**Decision**: Use jinja2 (unless AI understanding is critical).

**When AI is worth it**: Generating code where logic is non-trivial (not simple templating).

---

## Best Practices

### Do ✅

1. **Start simple, migrate when needed**
   ```
   demonstration → template_fill → jinja2
   (Only upgrade when you hit a limitation)
   ```

2. **Choose by audience**
   - Non-technical → `demonstration` or `template_fill`
   - Technical → `jinja2` or `code_generation`

3. **Use specialized generators when available**
   - Gherkin → `bdd_scenario_assembly` (NOT jinja2)
   - Simple substitution → `template_fill` (NOT jinja2)

4. **Consider non-functional requirements**
   - Cost-sensitive → Avoid `code_generation`
   - Offline operation → Avoid `code_generation`
   - Real-time (<100ms) → Avoid `code_generation`

5. **Validate assumptions**
   - "I think I need loops" → Try `template_fill` with pre-formatted strings first
   - "This is too complex to template" → Try `jinja2` before jumping to `code_generation`

### Don't ❌

1. **Don't use jinja2 for simple substitution**
   ```json
   // ❌ Bad: Overkill
   {"type": "jinja2", "template": "Hello, {{ name }}!"}

   // ✅ Good: Simple and fast
   {"type": "template_fill", "template": "Hello, {{name}}!"}
   ```

2. **Don't use `code_generation` for templatable content**
   ```json
   // ❌ Bad: Slow and costly
   {
     "type": "code_generation",
     "user_prompt": "Generate release notes for v{{version}} with features {{features}}"
   }

   // ✅ Good: Fast and free
   {
     "type": "template_fill",
     "template": "# Release v{{version}}\n\n{{features}}"
   }
   ```

3. **Don't fight against generator limitations**
   - If you need loops in `template_fill` → Migrate to `jinja2`
   - If you need AI in `jinja2` → Migrate to `code_generation`

4. **Don't choose by familiarity alone**
   - "I know jinja2, so I'll use it for everything" → Consider simpler options
   - "I've never used jinja2, so I'll use `code_generation`" → Learn jinja2 first

---

## Summary

**Decision framework**:

1. **Is content static?** → `demonstration`
2. **Need variables only?** → `template_fill`
3. **Generating Gherkin?** → `bdd_scenario_assembly`
4. **Need loops/conditionals?** → `jinja2`
5. **Need AI for code?** → `code_generation`

**Key principles**:

- **Simplicity first**: Use the simplest generator that works
- **Migrate incrementally**: Start simple, add complexity when needed
- **Consider non-functional**: Cost, speed, offline operation matter
- **Use specialized tools**: bdd_scenario for Gherkin (not jinja2)
- **Match audience**: Non-technical users need simpler generators

**Migration paths**:

```
demonstration → template_fill → jinja2 → code_generation
(Add complexity only when justified)
```

**Quick reference**:

| Use Case | Generator | Why |
|----------|-----------|-----|
| Static boilerplate | `demonstration` | Fastest, simplest |
| Release announcements | `template_fill` | Variables only |
| Email templates | `template_fill` | Simple substitution |
| API documentation | `jinja2` | Loops over endpoints |
| Report generation | `jinja2` | Conditionals + loops |
| BDD test scenarios | `bdd_scenario_assembly` | Gherkin validation |
| Utility function code | `code_generation` | AI understands logic |

---

## Related Documentation

### Reference
- [Generator Comparison Guide](../../reference/generators/generator-comparison.md) - Feature comparison table
- [Jinja2 Generator API](../../reference/api/generators/jinja2.md) - jinja2 reference
- [BDD Scenario API](../../reference/generators/bdd-scenario-api.md) - bdd_scenario reference

### How-To
- [Use Template Fill Generator](../../how-to/generators/use-template-fill-generator.md) - Simple substitution guide
- [Debug Jinja2 Templates](../../how-to/generation/debug-jinja2-templates.md) - jinja2 usage guide
- [Use BDD Scenario Generator](../../how-to/generators/use-bdd-scenario-generator.md) - Gherkin generation

### Tutorials
- [Custom Generator Creation](../../tutorials/advanced/04-custom-generator-creation.md) - Build your own generator

---

**Last Updated**: 2025-10-21 | **Phase**: Sprint 3 - Explanation Quadrant Expansion
