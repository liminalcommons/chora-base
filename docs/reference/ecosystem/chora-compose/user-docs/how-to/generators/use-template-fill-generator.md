# How to Use the Template Fill Generator

> **Goal:** Generate content using simple `{{variable}}` substitution without logic.

## When to Use This

You need the TemplateFillGenerator when:
- You want simple variable replacement (like mail merge)
- No conditional logic (if/else) needed
- No loops (for/each) needed
- Fast performance is critical
- Non-technical users need to edit templates
- Templates should be human-readable
- You're migrating from simple string formatting

**Don't use this if:**
- You need conditional logic → Use [jinja2](../generation/debug-jinja2-templates.md)
- You need loops over data → Use [jinja2](../generation/debug-jinja2-templates.md)
- Content is entirely static → Use [demonstration](../generation/use-demonstration-generator.md)
- You need AI-generated code → Use [code_generation](use-code-generation-generator.md)

## Prerequisites

- Chora Compose installed
- Basic understanding of content configs
- Context data in JSON format
- Completed [Tutorial: Generate Your First Content](../../tutorials/getting-started/03-generate-your-first-content.md) (optional)

---

## Solution

### Quick Version

```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.template_fill import TemplateFillGenerator

# Load config
loader = ConfigLoader()
config = loader.load_content_config("your-content-id")

# Provide context
context = {
    "name": "Alice",
    "version": "1.0.0",
    "date": "2025-10-12"
}

# Generate
generator = TemplateFillGenerator()
output = generator.generate(config, context=context)

print(output)
```

### Detailed Steps

#### 1. Create Content Configuration

Your config needs a `template_fill` pattern:

```json
{
  "type": "content",
  "id": "my-template",
  "schemaRef": {
    "id": "content-schema",
    "version": "3.1"
  },
  "metadata": {
    "description": "Simple template with variables",
    "version": "1.0.0",
    "generation_frequency": "on_demand",
    "output_format": "markdown"
  },
  "elements": [
    {
      "name": "output",
      "description": "Generated content",
      "format": "markdown",
      "example_output": ""
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "fill",
        "type": "template_fill",
        "template": "# {{product_name}} {{version}}\n\nReleased on: {{release_date}}\n\n## Features\n\n{{features}}"
      }
    ]
  }
}
```

**Key points:**
- `type: "template_fill"` - Specifies this generator
- `template` - Your text with `{{variable}}` placeholders
- Variables use double curly braces: `{{name}}`

#### 2. Prepare Context Data

Create a JSON file or dictionary with your variables:

```json
{
  "product_name": "Chora Compose",
  "version": "0.8.0",
  "release_date": "2025-11-10",
  "features": "- Template Fill Generator\n- Code Generation Generator\n- BDD Scenario Generator"
}
```

**Important:**
- Keys must match `{{variable}}` names exactly
- Use `\n` for line breaks in JSON strings
- Can include nested objects (see Advanced section)

#### 3. Generate Content

```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.template_fill import TemplateFillGenerator
import json

# Load config
loader = ConfigLoader()
config = loader.load_content_config("my-template")

# Load context from file
with open("context.json") as f:
    context = json.load(f)

# Generate
generator = TemplateFillGenerator()
result = generator.generate(config, context=context)

# Save or use result
with open("output.md", "w") as f:
    f.write(result)

print("Generated:", len(result), "characters")
```

#### 4. Review Output

The generator replaces all `{{variable}}` placeholders with values from context:

**Input template:**
```markdown
# {{product_name}} {{version}}

Released on: {{release_date}}

## Features

{{features}}
```

**Output:**
```markdown
# Chora Compose 0.8.0

Released on: 2025-11-10

## Features

- Template Fill Generator
- Code Generation Generator
- BDD Scenario Generator
```

---

## Configuration Details

### Template Syntax

**Basic substitution:**
```
{{variable_name}}
```

**Rules:**
- Variable names: letters, numbers, underscores
- Case-sensitive: `{{Name}}` ≠ `{{name}}`
- No spaces: `{{my_var}}` ✅ `{{ my var }}` ❌
- No expressions: `{{name.upper()}}` ❌ (use jinja2 for that)

### Context Data Structure

**Simple variables:**
```json
{
  "title": "Hello World",
  "count": 42,
  "active": true
}
```

**Nested objects** (use dot notation):
```json
{
  "user": {
    "name": "Alice",
    "email": "alice@example.com"
  }
}
```

Access with: `{{user.name}}`, `{{user.email}}`

**Lists** (serialize to string):
```json
{
  "features": "- Feature 1\n- Feature 2\n- Feature 3"
}
```

**Note:** template_fill doesn't have loops. If you need to iterate over arrays, use jinja2 or pre-format the list as a string.

### Undefined Variable Behavior

**Default:** Raise error if variable not in context

**Options:**
```python
# Option 1: Raise error (default)
generator = TemplateFillGenerator(undefined_behavior="strict")

# Option 2: Leave placeholder unchanged
generator = TemplateFillGenerator(undefined_behavior="keep")
# {{missing_var}} stays as "{{missing_var}}"

# Option 3: Replace with empty string
generator = TemplateFillGenerator(undefined_behavior="empty")
# {{missing_var}} becomes ""
```

**Recommendation:** Use "strict" in development, "empty" or "keep" in production with logging.

---

## Advanced Usage

### Working with Nested Objects

**Context:**
```json
{
  "release": {
    "version": "0.8.0",
    "date": "2025-11-10",
    "author": {
      "name": "Development Team",
      "email": "dev@example.com"
    }
  }
}
```

**Template:**
```
Version: {{release.version}}
Date: {{release.date}}
By: {{release.author.name}} ({{release.author.email}})
```

### Multi-line Content

**Context:**
```json
{
  "description": "This is a long description.\n\nIt has multiple paragraphs.\n\nEach separated by blank lines."
}
```

**Template:**
```
## Description

{{description}}
```

**Result:**
```
## Description

This is a long description.

It has multiple paragraphs.

Each separated by blank lines.
```

### Dynamic Context Loading

```python
def load_context_from_multiple_sources():
    """Merge context from multiple sources."""
    context = {}

    # From JSON file
    with open("base.json") as f:
        context.update(json.load(f))

    # From environment
    context["api_key"] = os.getenv("API_KEY", "not-set")

    # From database
    context["user_count"] = get_user_count_from_db()

    # Computed values
    context["generated_at"] = datetime.now().isoformat()

    return context
```

### Conditional Content (Pre-computed)

Since template_fill has no logic, pre-compute conditionals in context:

```python
# In your script
context = {
    "product": "Chora Compose",
    "version": "0.8.0",
    "has_breaking_changes": False
}

# Add conditional text to context
if context["has_breaking_changes"]:
    context["breaking_notice"] = "⚠️ **BREAKING CHANGES** - See migration guide"
else:
    context["breaking_notice"] = ""

# Template just uses the pre-computed value
template = "# {{product}} {{version}}\n\n{{breaking_notice}}"
```

---

## Comparison with Other Generators

### Template Fill vs Jinja2

| Feature | template_fill | jinja2 |
|---------|--------------|--------|
| Variables | `{{var}}` | `{{var}}` |
| Conditionals | No | `{% if %}` |
| Loops | No | `{% for %}` |
| Filters | No | `\|upper, \|default` |
| Complexity | Low | Medium-High |
| Speed | Instant | Fast |

**When to use template_fill:**
- Simple substitution only
- Non-technical users
- Performance critical

**When to use jinja2:**
- Need if/else logic
- Need loops over data
- Need data transformations

### Template Fill vs Demonstration

| Feature | template_fill | demonstration |
|---------|--------------|---------------|
| Variables | Yes | No |
| Static content | Yes | Yes |
| Customization | Yes | No |
| Complexity | Low | Lowest |

**Migration:** If you add variables to demonstration, use template_fill.

---

## Common Patterns

### Release Announcements

```json
{
  "template": "# {{product}} {{version}} Released!\n\n**Date:** {{date}}\n\n## What's New\n\n{{features}}\n\n## Download\n\n{{download_url}}"
}
```

### Email Templates

```json
{
  "template": "Dear {{name}},\n\n{{message_body}}\n\nBest regards,\n{{sender_name}}"
}
```

### Configuration Files

```json
{
  "template": "{\n  \"api_url\": \"{{api_url}}\",\n  \"timeout\": {{timeout}},\n  \"retries\": {{retries}}\n}"
}
```

### Certificates/Documents

```json
{
  "template": "This certifies that {{recipient_name}} has completed {{course_name}} on {{completion_date}}."
}
```

---

## Troubleshooting

### Issue: Variable not substituted (stays as `{{var}}`)

**Cause:** Variable name doesn't match context key

**Debug:**
```python
print("Available variables:", context.keys())
print("Template variables:", re.findall(r'\{\{(\w+)\}\}', template))
```

**Solution:** Ensure exact match (case-sensitive)

### Issue: `TemplateFillError: Undefined variable 'xyz'`

**Cause:** Variable in template but not in context

**Solutions:**
1. Add variable to context
2. Use `undefined_behavior="empty"`
3. Check for typos in variable names

### Issue: Multi-line strings not rendering correctly

**Cause:** JSON doesn't preserve newlines visually

**Solution:** Use `\n` for line breaks:
```json
{
  "text": "Line 1\nLine 2\nLine 3"
}
```

### Issue: Want to include literal `{{braces}}`

**Cause:** template_fill treats all `{{}}` as variables

**Solutions:**
1. Use different delimiters (requires custom generator)
2. Escape in context:
   ```json
   {
     "example": "Use {{{{variable}}}} syntax"
   }
   ```
3. Use jinja2 with escape syntax: `{{ "{{" }}`

### Issue: Performance with large templates

**Cause:** Very large templates (>1MB)

**Solution:**
- template_fill is already optimized
- Consider splitting into multiple smaller templates
- Cache frequently-used templates

---

## Best Practices

### Do ✅

1. **Use clear variable names:**
   ```json
   {"user_first_name": "Alice"}  // Good
   {"ufn": "Alice"}              // Bad
   ```

2. **Provide all variables:**
   ```python
   # Validate before generating
   required_vars = ["name", "version", "date"]
   missing = [v for v in required_vars if v not in context]
   if missing:
       raise ValueError(f"Missing: {missing}")
   ```

3. **Document variables:**
   ```json
   {
     "_comment": "Variables: product_name, version, features",
     "product_name": "Chora Compose"
   }
   ```

4. **Use consistent naming:**
   ```
   snake_case: {{product_name}}
   Not: {{ProductName}}, {{product-name}}
   ```

### Don't ❌

1. **Don't use logic in templates:**
   ```
   ❌ {{if has_feature}}Feature X{{endif}}
   ✅ Pre-compute in context: {"feature_text": "Feature X"}
   ```

2. **Don't modify context during generation:**
   ```python
   ❌ context["date"] = datetime.now()  # During generate()
   ✅ context["date"] = datetime.now()  # Before generate()
   ```

3. **Don't use undefined_behavior="keep" without logging:**
   ```python
   ❌ generator = TemplateFillGenerator(undefined_behavior="keep")
   ✅ generator = TemplateFillGenerator(undefined_behavior="keep")
       # + Log warnings for undefined variables
   ```

---

## Performance Considerations

**Speed:**
- Small templates (<10KB): <1ms
- Medium templates (10-100KB): <5ms
- Large templates (>100KB): <20ms

**Memory:**
- Minimal overhead
- Scales linearly with template size

**Optimization tips:**
- Cache parsed templates if generating repeatedly
- Use string builder for very large outputs
- Consider jinja2 if template compilation helps

---

## Example Workflows

### Batch Generation

```python
# Generate multiple outputs from one template
templates = ["release-v1", "release-v2", "release-v3"]
contexts = [
    {"version": "1.0.0", "date": "2025-01-01"},
    {"version": "2.0.0", "date": "2025-06-01"},
    {"version": "3.0.0", "date": "2025-12-01"},
]

generator = TemplateFillGenerator()

for template_id, context in zip(templates, contexts):
    config = loader.load_content_config(template_id)
    output = generator.generate(config, context=context)
    with open(f"output-{context['version']}.md", "w") as f:
        f.write(output)
```

### CI/CD Integration

```yaml
# .github/workflows/generate-release-notes.yml
- name: Generate release notes
  run: |
    python -c "
    from chora_compose import ConfigLoader, TemplateFillGenerator
    import json

    context = {
        'version': '${{ github.ref_name }}',
        'date': '${{ github.event.created_at }}',
        'features': open('FEATURES.txt').read()
    }

    loader = ConfigLoader()
    config = loader.load_content_config('release-notes')
    generator = TemplateFillGenerator()
    output = generator.generate(config, context=context)

    with open('RELEASE_NOTES.md', 'w') as f:
        f.write(output)
    "
```

---

## Migration Guide

### From Demonstration

**Before (demonstration):**
```json
{
  "type": "demonstration",
  "template": "{{elements.intro.example_output}}\n\n{{elements.body.example_output}}"
}
```

**After (template_fill):**
```json
{
  "type": "template_fill",
  "template": "{{intro}}\n\n{{body}}"
}
```

Context:
```json
{
  "intro": "Welcome to our product!",
  "body": "This is the main content."
}
```

### To Jinja2

**When needed:** You realize you need conditionals or loops

**Migration:**
1. Templates mostly compatible ({{var}} syntax same)
2. Add logic where needed:
   ```jinja2
   {% if has_premium %}
   ## Premium Features
   {{premium_features}}
   {% endif %}
   ```
3. Test thoroughly (jinja2 has different error handling)

---

## Examples

**Full working example:**
- See: [examples/02-template-fill/](../../examples/02-template-fill/)
- Use case: Release announcement
- Includes: Config, context, script, expected output

**Quick links:**
- [README](../../examples/02-template-fill/README.md)
- [Config](../../examples/02-template-fill/configs/content/release-announcement.json)
- [Context](../../examples/02-template-fill/context.json)
- [Script](../../examples/02-template-fill/generate.py)

---

## Related Documentation

- [Generator Comparison Guide](../../reference/generators/generator-comparison.md) - Choose the right generator
- [Jinja2 Generator](../generation/debug-jinja2-templates.md) - When you need logic
- [Demonstration Generator](../generation/use-demonstration-generator.md) - For static content
- [Content Configuration](../../reference/api/core/config-loader.md) - Config structure

---

## API Reference

```python
class TemplateFillGenerator(GeneratorStrategy):
    """Simple {{variable}} substitution generator."""

    def __init__(
        self,
        undefined_behavior: str = "strict"  # "strict" | "keep" | "empty"
    ) -> None:
        """Initialize template fill generator."""

    def generate(
        self,
        config: ContentConfig,
        context: dict[str, Any] | None = None
    ) -> str:
        """Generate content by substituting variables."""
```

**Parameters:**
- `undefined_behavior`: How to handle missing variables
  - `"strict"`: Raise TemplateFillError
  - `"keep"`: Leave `{{var}}` unchanged
  - `"empty"`: Replace with empty string
- `context`: Dictionary of variable values

**Returns:** Generated string with variables substituted

**Raises:**
- `TemplateFillError`: If template invalid or variable undefined (strict mode)

---

**Last Updated:** 2025-10-12 | **Phase:** 3.2 Complete
