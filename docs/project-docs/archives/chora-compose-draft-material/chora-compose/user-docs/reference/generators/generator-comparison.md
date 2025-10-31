# Generator Comparison Guide

**Purpose:** Help you choose the right generator for your content generation needs.

**TL;DR:** Use the decision tree below, then check the feature table for details.

---

## Quick Decision Tree

```
START: What do you need to generate?

├─ Static content (no variables)?
│  └─ Use: demonstration
│     └─ Example: Pre-written documentation sections
│
├─ Content with variables?
│  │
│  ├─ Need conditional logic (if/else) or loops?
│  │  │
│  │  ├─ Yes: Complex templating needed?
│  │  │  ├─ Yes: Use jinja2
│  │  │  │  └─ Example: API docs from OpenAPI spec
│  │  │  │
│  │  │  └─ No: Generating BDD test scenarios?
│  │  │     └─ Yes: Use bdd_scenario_assembly
│  │  │        └─ Example: Gherkin feature files
│  │  │
│  │  └─ No: Just simple substitution?
│  │     └─ Yes: Use template_fill
│  │        └─ Example: Release announcements, email templates
│  │
│  └─ Need AI to generate code from descriptions?
│     └─ Yes: Use code_generation
│        └─ Example: Utility functions, boilerplate code
```

---

## Feature Comparison Table

| Feature | demonstration | jinja2 | template_fill | code_generation | bdd_scenario_assembly |
|---------|---------------|--------|---------------|-----------------|---------------------|
| **Complexity** | Lowest | High | Low | Medium | Medium |
| **Learning Curve** | 5 min | 30 min | 10 min | 20 min | 25 min |
| **Variables** | No | Yes | Yes ({{var}}) | Via context | Yes ({{var}}) |
| **Conditionals (if/else)** | No | Yes ({% if %}) | No | AI-powered | No |
| **Loops (for)** | No | Yes ({% for %}) | No | AI-powered | No |
| **Filters** | No | Yes (\|upper, \|length) | No | No | No |
| **Template Inheritance** | No | Yes (extends/block) | No | No | No |
| **External API Calls** | No | No | No | Yes (Anthropic) | No |
| **Cost** | Free | Free | Free | $0.01-0.10/run | Free |
| **Speed** | Instant (<1ms) | Fast (<10ms) | Instant (<1ms) | Slow (10-30s) | Fast (<5ms) |
| **Requires API Key** | No | No | No | Yes | No |
| **Requires Internet** | No | No | No | Yes | No |
| **Deterministic Output** | Yes | Yes | Yes | Configurable* | Yes |
| **Human-Readable Templates** | Yes | Medium | Yes | N/A | Yes |
| **Best For** | Static content | Complex templates | Simple substitution | Code generation | BDD test scenarios |

*code_generation: Use temperature=0.0 for deterministic output

---

## Detailed Comparison

### 1. demonstration

**What it does:** Assembles pre-written content sections without modification.

**Strengths:**
- ✅ Simplest possible generator
- ✅ No learning curve
- ✅ Perfect for static documentation
- ✅ Instant execution
- ✅ No dependencies

**Limitations:**
- ❌ Cannot use variables
- ❌ No dynamic content
- ❌ Cannot adapt to context
- ❌ Limited to pre-written text

**Typical Use Cases:**
- Pre-written documentation sections
- Boilerplate legal text
- Standard templates (no customization needed)
- Examples and tutorials

**Example:**
```json
{
  "type": "demonstration",
  "template": "{{elements.intro.example_output}}\n\n{{elements.body.example_output}}"
}
```

**When to use:** You have static content that never changes.

**When NOT to use:** You need any kind of customization or variable substitution.

**Migration path:** If you need variables → template_fill or jinja2

---

### 2. template_fill

**What it does:** Simple `{{variable}}` substitution from context data.

**Strengths:**
- ✅ Simple variable replacement
- ✅ Fast execution
- ✅ Human-readable templates
- ✅ Perfect for non-technical users
- ✅ Supports nested objects
- ✅ No external dependencies

**Limitations:**
- ❌ No conditional logic (if/else)
- ❌ No loops (for)
- ❌ No filters or transformations
- ❌ No template inheritance

**Typical Use Cases:**
- Release announcements
- Email templates
- Configuration file generation
- Report templates
- Certificate/document generation
- Simple personalization

**Example:**
```json
{
  "type": "template_fill",
  "template": "# {{product_name}} {{version}} Released!\n\n{{features}}"
}
```

Context:
```json
{
  "product_name": "Chora Compose",
  "version": "0.8.0",
  "features": "- New generators\n- Better docs"
}
```

**When to use:**
- Simple variable substitution only
- Non-technical users edit templates
- Performance is critical

**When NOT to use:**
- Need conditionals or loops
- Need data transformations
- Complex formatting logic

**Migration path:**
- If you need logic → jinja2
- If you have static content → demonstration

---

### 3. jinja2

**What it does:** Full-featured templating with logic, loops, filters, and inheritance.

**Strengths:**
- ✅ Complete templating engine
- ✅ Conditional logic ({% if %})
- ✅ Loops ({% for %})
- ✅ Filters (\|upper, \|default, custom)
- ✅ Template inheritance (extends/block)
- ✅ Macros for reusability
- ✅ Industry-standard syntax
- ✅ Extensive documentation

**Limitations:**
- ❌ Steeper learning curve
- ❌ More complex templates
- ❌ Requires understanding of programming concepts
- ❌ Can become hard to maintain if overused

**Typical Use Cases:**
- API documentation from schemas
- Complex reports with sections
- Multi-format output (HTML, PDF, Markdown)
- Data-driven documentation
- Configuration with conditional sections

**Example:**
```jinja2
{% for endpoint in api.endpoints %}
## {{ endpoint.method }} {{ endpoint.path }}

{{ endpoint.description }}

{% if endpoint.parameters %}
### Parameters
{% for param in endpoint.parameters %}
- **{{ param.name }}** ({{ param.type }}): {{ param.description }}
{% endfor %}
{% endif %}
{% endfor %}
```

**When to use:**
- Complex data structures
- Need conditional logic
- Need loops over data
- Template reusability (inheritance)
- Industry-standard approach needed

**When NOT to use:**
- Simple substitution is enough (use template_fill)
- Non-technical users need to edit (use template_fill)
- Static content only (use demonstration)

**Migration path:**
- If too complex for users → template_fill
- If logic not needed → template_fill

---

### 4. code_generation

**What it does:** AI-powered code generation from natural language using Anthropic Claude.

**Strengths:**
- ✅ Generate code from descriptions
- ✅ Multiple languages supported
- ✅ Intelligent code quality
- ✅ Handles edge cases
- ✅ Includes documentation
- ✅ Adaptive to requirements

**Limitations:**
- ❌ Requires API key (cost)
- ❌ Slow (10-30 seconds)
- ❌ Non-deterministic (use temp=0.0)
- ❌ Requires internet connection
- ❌ Code review always needed
- ❌ Not suitable for production-critical code without review

**Typical Use Cases:**
- Utility function generation
- Boilerplate code scaffolding
- Test case generation
- Data transformation scripts
- Format converters
- Code migration helpers

**Example:**
```json
{
  "type": "code_generation",
  "generation_config": {
    "model": "claude-3-5-sonnet-20241022",
    "temperature": 0.0,
    "prompt": "Generate a Python function to {{function_description}}",
    "language": "python"
  }
}
```

**Cost Breakdown:**
- Claude 3.5 Sonnet: $3/M input, $15/M output (~$0.02-0.05 per function)
- Claude 3 Haiku: $0.25/M input, $1.25/M output (~$0.005-0.01 per function)
- Claude 3 Opus: $15/M input, $75/M output (~$0.10-0.20 per function)

**When to use:**
- Need to generate code from specifications
- Prototyping quickly
- Boilerplate generation
- Have budget for API costs

**When NOT to use:**
- Cost is a concern (frequent generation)
- Need instant results
- Security-critical code
- No internet available
- Budget constraints

**Migration path:**
- If cost too high → Use template_fill with pre-written code snippets
- If need templates → jinja2 with code templates

---

### 5. bdd_scenario_assembly

**What it does:** Generate Gherkin feature files for Behavior-Driven Development testing.

**Strengths:**
- ✅ Gherkin syntax expertise
- ✅ Feature/Scenario/Background structure
- ✅ Scenario Outlines with data tables
- ✅ Tag-based organization
- ✅ Variable substitution
- ✅ Syntax validation
- ✅ Integration with test frameworks

**Limitations:**
- ❌ Gherkin-specific (can't generate other formats)
- ❌ Requires BDD testing knowledge
- ❌ Learning curve for Gherkin syntax
- ❌ Limited to test scenario generation

**Typical Use Cases:**
- Acceptance test scenarios
- BDD feature files
- Living documentation
- User story verification
- Regression test suites
- Behavior specifications

**Example:**
```json
{
  "type": "bdd_scenario_assembly",
  "generation_config": {
    "feature": {
      "title": "{{feature_name}}",
      "tags": ["@smoke", "@critical"]
    },
    "scenarios": [{
      "title": "Successful login",
      "steps": [
        "Given I am on the login page",
        "When I enter username \"{{username}}\"",
        "Then I should see the dashboard"
      ]
    }]
  }
}
```

**When to use:**
- BDD testing approach
- Gherkin feature files needed
- Behavior documentation
- Integration with Cucumber/Behave/SpecFlow

**When NOT to use:**
- Not doing BDD testing
- Need general text generation (use template_fill or jinja2)
- Unit testing (different approach)

**Migration path:**
- If BDD not needed → template_fill for test documentation
- If need test code → code_generation

---

## Use Case Matrix

| Use Case | Best Generator | Alternative | Why |
|----------|---------------|-------------|-----|
| Release announcements | template_fill | jinja2 | Simple variable substitution sufficient |
| API documentation | jinja2 | template_fill | Need loops over endpoints |
| Email templates | template_fill | jinja2 | Simple substitution, human-readable |
| Configuration files | template_fill | jinja2 | Variable substitution, simple logic |
| Legal boilerplate | demonstration | template_fill | Static text, rarely changes |
| Utility functions | code_generation | template_fill | AI generates better edge cases |
| Test scenarios (BDD) | bdd_scenario_assembly | jinja2 | Specialized for Gherkin |
| Complex reports | jinja2 | template_fill | Need conditional sections, loops |
| Code scaffolding | code_generation | jinja2 | AI adapts to requirements |
| Certificates | template_fill | jinja2 | Simple personalization |
| Multi-format docs | jinja2 | template_fill | Template inheritance useful |
| Static tutorials | demonstration | template_fill | No customization needed |

---

## Performance Comparison

| Generator | Speed | Memory | Scalability |
|-----------|-------|--------|-------------|
| demonstration | Instant (<1ms) | Minimal | Excellent |
| template_fill | Instant (<1ms) | Minimal | Excellent |
| jinja2 | Fast (<10ms) | Low | Excellent |
| bdd_scenario_assembly | Fast (<5ms) | Low | Excellent |
| code_generation | Slow (10-30s) | Moderate | Limited by API rate |

**Batch Operations:**
- demonstration, template_fill, jinja2: Can generate 1000s per second
- bdd_scenario_assembly: Can generate 100s per second
- code_generation: Limited to 50-100 requests per minute (API rate limits)

---

## Cost Analysis

### Free Generators (demonstration, jinja2, template_fill, bdd_scenario_assembly)
- **Cost:** $0
- **Operational cost:** Compute time (negligible)
- **Scalability:** Unlimited generations

### Paid Generator (code_generation)
- **Base cost:** $0.01-0.10 per generation (depends on length, model)
- **Monthly estimate:**
  - 10 generations/day × 30 days = ~$6-30/month
  - 100 generations/day × 30 days = ~$60-300/month
- **Optimization strategies:**
  - Use Claude 3 Haiku for cheaper generation ($0.005-0.01 each)
  - Cache common results
  - Batch similar requests
  - Set spending limits

**Cost Monitoring:**
- Track usage: https://console.anthropic.com/settings/usage
- Set alerts for spending thresholds
- Review monthly usage reports

---

## When to Migrate Between Generators

### From demonstration → template_fill
**Trigger:** Need to customize content with variables

**Effort:** Low (1-2 hours)

**Steps:**
1. Identify variable parts in static content
2. Replace with `{{variable}}` placeholders
3. Create context data JSON
4. Test with different contexts

### From template_fill → jinja2
**Trigger:** Need conditional logic or loops

**Effort:** Medium (half day)

**Steps:**
1. Convert `{{variable}}` to Jinja2 syntax (usually same)
2. Add {% if %} conditionals where needed
3. Add {% for %} loops where needed
4. Test with various data structures
5. Consider template inheritance

### From demonstration/template_fill → code_generation
**Trigger:** Need to generate actual code, not templates

**Effort:** Medium (2-4 hours)

**Steps:**
1. Set up Anthropic API key
2. Write clear specifications in natural language
3. Configure model and temperature
4. Test with examples
5. Set up cost monitoring
6. Add code review process

### From jinja2 → template_fill
**Trigger:** Too complex for users, logic not needed

**Effort:** Low (1-2 hours)

**Steps:**
1. Remove {% %} logic tags
2. Simplify to {{variable}} only
3. Pre-compute conditional logic in context
4. Test with simplified context data

---

## Decision Checklist

Use this checklist to choose the right generator:

**Start here:**
- [ ] Do I need variables?
  - No → **demonstration**
  - Yes → Continue

- [ ] Do I need conditional logic (if/else)?
  - No → Go to "Loops"
  - Yes → Go to "Logic needed"

- [ ] Do I need loops (for/each)?
  - No → **template_fill**
  - Yes → Go to "Logic needed"

**Logic needed:**
- [ ] Is this for BDD testing?
  - Yes → **bdd_scenario_assembly**
  - No → Continue

- [ ] Is this for code generation?
  - Yes → **code_generation** (if you have API budget)
  - No → **jinja2**

**Special cases:**
- [ ] Do I have budget for API calls?
  - Yes + need code → **code_generation**
  - No → Use templates

- [ ] Do users need to edit templates?
  - Yes → **template_fill** (simplest)
  - No → **jinja2** (more powerful)

---

## Recommendations by Role

### For Developers
**Primary:** jinja2 (familiar, powerful)
**Secondary:** code_generation (for boilerplate)
**Avoid:** demonstration (too limited)

### For Technical Writers
**Primary:** template_fill (simple, readable)
**Secondary:** jinja2 (if comfortable with logic)
**Avoid:** code_generation (not for prose)

### For QA Engineers
**Primary:** bdd_scenario_assembly (BDD testing)
**Secondary:** jinja2 (test data generation)
**Avoid:** code_generation (too expensive for bulk tests)

### For Product Managers
**Primary:** template_fill (release notes, specs)
**Secondary:** demonstration (static docs)
**Avoid:** jinja2 (too technical), code_generation (unnecessary)

---

## Common Mistakes

### ❌ Using jinja2 when template_fill is enough
**Problem:** Overcomplicating simple substitution
**Solution:** Start with template_fill, upgrade only if needed

### ❌ Using demonstration with variables
**Problem:** demonstration doesn't support variables
**Solution:** Use template_fill for any customization

### ❌ Using code_generation for templates
**Problem:** Expensive, slow, unnecessary
**Solution:** Use template_fill or jinja2 for templates

### ❌ Using template_fill with complex logic needs
**Problem:** Trying to hack conditionals with multiple templates
**Solution:** Use jinja2 when you need logic

### ❌ Not reviewing code_generation output
**Problem:** Generated code may have subtle bugs
**Solution:** Always review, test, and validate AI-generated code

---

## Further Reading

- [Template Fill How-To](template-fill.md)
- [Code Generation How-To](code-generation.md)
- [BDD Scenario How-To](bdd-scenario.md)
- [Jinja2 Generator Guide](../how-to/generation/debug-jinja2-templates.md)
- [Demonstration Generator Guide](../how-to/generation/use-demonstration-generator.md)

### Examples
- [Template Fill Example](../../examples/02-template-fill/)
- [Code Generation Example](../../examples/03-ai-code-generation/)
- [BDD Scenario Example](../../examples/04-bdd-scenarios/)
- [Jinja2 API Docs Example](../../examples/jinja2-api-docs/)

---

**Last Updated:** 2025-10-12 | **Phase:** 3.2 Complete
