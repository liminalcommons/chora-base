# How to Debug Jinja2 Template Errors

> **Goal:** Diagnose and fix common Jinja2 template errors quickly and effectively.

## When to Use This

You need this guide when:
- Templates fail to render
- Getting cryptic Jinja2 error messages
- Variables not appearing in output
- Templates rendering incorrectly
- Syntax errors in templates

## Prerequisites

- Chora Compose installed with Jinja2Generator
- Basic understanding of Jinja2 syntax
- Template file and content configuration

---

## Solution

### Quick Debugging Checklist

When template generation fails, check in order:

1. **Template exists and is readable**
   ```python
   from pathlib import Path
   template_path = Path("templates/my-template.j2")
   assert template_path.exists(), f"Template not found: {template_path}"
   ```

2. **Template syntax is valid**
   ```python
   from jinja2 import Environment, FileSystemLoader
   env = Environment(loader=FileSystemLoader("templates"))
   template = env.get_template("my-template.j2")  # Will raise if syntax error
   ```

3. **Context has required variables**
   ```python
   context = config.generation.patterns[0].context
   required_vars = ["title", "content", "author"]
   for var in required_vars:
       assert var in context, f"Missing context variable: {var}"
   ```

4. **Variables are correct type**
   ```python
   assert isinstance(context["items"], list), "items must be a list"
   ```

5. **Template logic is sound**
   - Check for infinite loops
   - Verify conditional logic
   - Test filters with sample data

---

## Common Errors and Solutions

### Error: `TemplateNotFound`

**Full error:**
```
jinja2.exceptions.TemplateNotFound: my-template.j2
```

**Cause:** Jinja2 cannot find the template file.

**Solution 1: Check template path**

```python
from pathlib import Path

# Verify template exists
template_path = Path("templates/my-template.j2")
print(f"Template exists: {template_path.exists()}")
print(f"Absolute path: {template_path.absolute()}")

# List available templates
template_dir = Path("templates")
available = list(template_dir.glob("*.j2"))
print(f"Available templates: {[t.name for t in available]}")
```

**Solution 2: Verify template_dir configuration**

```python
from chora_compose.generators.jinja2 import Jinja2Generator

# Ensure template_dir is correct
generator = Jinja2Generator(template_dir=Path("templates"))

# Check loader is configured
print(f"Template loader: {generator.env.loader}")
```

**Solution 3: Use absolute paths (testing only)**

```python
# For testing, use absolute path
template_path = Path(__file__).parent / "templates" / "my-template.j2"
generator = Jinja2Generator(template_dir=template_path.parent)
```

---

### Error: `TemplateSyntaxError`

**Full error:**
```
jinja2.exceptions.TemplateSyntaxError: unexpected 'end of template'
```

**Cause:** Syntax error in template (unclosed tag, invalid syntax, etc.)

**Common syntax issues:**

#### Issue 1: Unclosed blocks

**Bad:**
```jinja2
{% for item in items %}
    {{ item }}
{# Missing {% endfor %} #}
```

**Good:**
```jinja2
{% for item in items %}
    {{ item }}
{% endfor %}
```

#### Issue 2: Unclosed expressions

**Bad:**
```jinja2
{{ title }
{# Missing closing } #}
```

**Good:**
```jinja2
{{ title }}
```

#### Issue 3: Invalid filter syntax

**Bad:**
```jinja2
{{ text | upper lower }}
{# Can't chain filters without | #}
```

**Good:**
```jinja2
{{ text | upper | lower }}
```

#### Issue 4: Mixing template syntax

**Bad:**
```jinja2
{% if condition {{ expression }} %}
{# Can't mix {% %} and {{ }} #}
```

**Good:**
```jinja2
{% if condition %}
    {{ expression }}
{% endif %}
```

**Debugging approach:**

```python
from jinja2 import Environment, TemplateSyntaxError

try:
    env = Environment()
    template_source = Path("templates/my-template.j2").read_text()
    env.parse(template_source)
    print("✓ Template syntax is valid")
except TemplateSyntaxError as e:
    print(f"✗ Syntax error at line {e.lineno}: {e.message}")
    print(f"  Template: {e.name}")

    # Show context around error
    lines = template_source.splitlines()
    start = max(0, e.lineno - 3)
    end = min(len(lines), e.lineno + 2)

    print("\nContext:")
    for i in range(start, end):
        marker = "→" if i == e.lineno - 1 else " "
        print(f"{marker} {i+1:3d}: {lines[i]}")
```

---

### Error: `UndefinedError`

**Full error:**
```
jinja2.exceptions.UndefinedError: 'title' is undefined
```

**Cause:** Template references a variable that doesn't exist in context.

**Solution 1: Check context has variable**

```python
# Debug context
context = config.generation.patterns[0].context
print(f"Available variables: {list(context.keys())}")

# Check specific variable
if "title" not in context:
    print("✗ Missing 'title' in context")
    print(f"  Add it to your content config")
```

**Solution 2: Use default filter**

```jinja2
{# Instead of #}
{{ title }}

{# Use #}
{{ title | default('Untitled') }}

{# Or check first #}
{% if title %}
{{ title }}
{% else %}
Untitled
{% endif %}
```

**Solution 3: Make undefined errors silent (not recommended)**

```python
from jinja2 import Environment, Undefined

# Custom undefined that returns empty string
class SilentUndefined(Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        return ''

generator = Jinja2Generator()
generator.env.undefined = SilentUndefined
```

---

### Error: `TypeError` in filters

**Full error:**
```
TypeError: can only concatenate str (not "int") to str
```

**Cause:** Type mismatch in template operation.

**Example:**

```jinja2
{# Bad: count is integer #}
There are {{ count }} items  {# OK #}
There are {{ count + " items" }}  {# ERROR: int + str #}
```

**Solution: Convert types explicitly**

```jinja2
{# Good #}
There are {{ count | string + " items" }}

{# Or use string formatting #}
There are {{ "%d items" | format(count) }}
```

**Common type issues:**

```jinja2
{# Lists #}
{{ items | length }}  {# OK #}
{{ items + 5 }}  {# ERROR: can't add int to list #}

{# Dictionaries #}
{{ user.name }}  {# OK #}
{{ user + " name" }}  {# ERROR: can't add str to dict #}

{# None #}
{{ value | default('N/A') }}  {# OK: handles None #}
{{ value.upper() }}  {# ERROR if value is None #}
```

---

### Error: Template renders but output is wrong

**Symptom:** No error, but generated output is incorrect.

**Debugging technique 1: Print variables**

```jinja2
{# Add debug output at top of template #}
{# DEBUG: title = {{ title }} #}
{# DEBUG: items count = {{ items | length }} #}
{# DEBUG: context keys = {{ context.keys() | list }} #}

{# Your actual template #}
# {{ title }}

{% for item in items %}
- {{ item }}
{% endfor %}
```

**Debugging technique 2: Isolate sections**

```jinja2
{# Comment out sections to find problem #}

# {{ title }}  {# Section 1: Works #}

{# Section 2: Commented out to test
{% for item in items %}
- {{ item }}
{% endfor %}
#}

{# Section 3: Commented out to test
{{ footer }}
#}
```

**Debugging technique 3: Render step-by-step**

```python
from jinja2 import Environment

env = Environment()

# Test each part independently
parts = [
    "{{ title }}",
    "{{ items | length }}",
    "{% for item in items %}{{ item }}{% endfor %}"
]

context = {
    "title": "Test",
    "items": ["a", "b", "c"]
}

for part in parts:
    template = env.from_string(part)
    result = template.render(context)
    print(f"Part: {part}")
    print(f"Result: {result}")
    print()
```

---

### Error: Loop issues

**Problem: Loop not iterating**

```jinja2
{# Items is not iterable #}
{% for item in items %}
    {{ item }}
{% endfor %}
```

**Solution: Check items is a list**

```python
# Debug
context = config.generation.patterns[0].context
print(f"items type: {type(context.get('items'))}")
print(f"items value: {context.get('items')}")

# items should be a list or tuple
assert isinstance(context["items"], (list, tuple)), "items must be iterable"
```

**Problem: Loop counter not working**

**Bad:**
```jinja2
{% for item in items %}
{{ i }}. {{ item }}  {# i is undefined #}
{% endfor %}
```

**Good:**
```jinja2
{% for item in items %}
{{ loop.index }}. {{ item }}  {# Use loop.index #}
{% endfor %}
```

**Problem: Nested loops**

```jinja2
{% for category in categories %}
## {{ category.name }}

{% for item in category.items %}
    {# Access outer loop: #}
    Category {{ loop.parent.loop.index }}, Item {{ loop.index }}
    {{ item }}
{% endfor %}
{% endfor %}
```

---

### Error: Filter issues

**Problem: Filter not found**

**Error:**
```
jinja2.exceptions.UndefinedError: No filter named 'custom_filter'
```

**Solution: Register custom filter**

```python
from chora_compose.generators.jinja2 import Jinja2Generator

def custom_filter(value):
    """Custom filter implementation."""
    return value.upper()

generator = Jinja2Generator()
generator.env.filters['custom_filter'] = custom_filter

# Now can use in template
# {{ text | custom_filter }}
```

**Problem: Filter arguments wrong**

```jinja2
{# Bad: join requires a string argument #}
{{ items | join }}  {# ERROR: missing required argument #}

{# Good #}
{{ items | join(', ') }}
```

**Problem: Chaining filters incorrectly**

```jinja2
{# Bad: order matters #}
{{ text | length | upper }}  {# ERROR: length returns int, int has no upper() #}

{# Good #}
{{ text | upper | length }}  {# upper returns str, length works on str #}
```

---

## Debugging Techniques

### Technique 1: Minimal Reproduction

Create simplest possible test case:

**minimal-template.j2:**
```jinja2
{{ title }}
```

**Test:**
```python
from jinja2 import Environment

env = Environment()
template = env.from_string("{{ title }}")

# Test with minimal context
result = template.render({"title": "Test"})
print(result)  # Should print: Test

# If this works, gradually add complexity
```

### Technique 2: Template Linting

Use external tools to check templates:

```bash
# Install jinja2-cli
pip install jinja2-cli

# Lint template
jinja2 templates/my-template.j2 --format=json data/context.json
```

### Technique 3: Context Inspection

Print full context before rendering:

```python
import json
from pathlib import Path

# Load config
config = loader.load_content_config("my-content")

# Inspect context
context = config.generation.patterns[0].context
print("Context:")
print(json.dumps(context, indent=2, default=str))

# Save for external testing
Path("debug-context.json").write_text(
    json.dumps(context, indent=2, default=str)
)

# Now generate
output = generator.generate(config)
```

### Technique 4: Template Diff

Compare working vs broken template:

```bash
# If you have a working version
diff templates/working-template.j2 templates/broken-template.j2

# Or use git
git diff templates/my-template.j2
```

### Technique 5: Render in Steps

Break complex template into steps:

```jinja2
{# Step 1: Just title #}
# {{ title }}

{# Verify step 1 works, then add step 2 #}

{# Step 2: Add metadata #}
**Author:** {{ author }}
**Date:** {{ date }}

{# Verify step 2 works, then add step 3 #}

{# Step 3: Add content #}
{{ content }}
```

---

## Advanced Debugging

### Debug Mode

Enable Jinja2 debug mode:

```python
from jinja2 import Environment, DebugUndefined

generator = Jinja2Generator()

# Use DebugUndefined to get helpful error messages
generator.env.undefined = DebugUndefined

# Enable line statements for debugging
generator.env.line_statement_prefix = '##'
```

**Now can use line statements in template:**

```jinja2
## set debug_var = "value"
Debug var: {{ debug_var }}

## for item in items
- {{ item }}
## endfor
```

### Custom Exception Handler

Wrap generation with custom error handling:

```python
from jinja2 import TemplateError
from pathlib import Path

def debug_generate(config):
    """Generate with detailed error reporting."""
    try:
        output = generator.generate(config)
        return output

    except TemplateError as e:
        print(f"✗ Template error: {e}")

        # Show template source
        template_name = config.generation.patterns[0].template
        template_path = Path("templates") / template_name

        if template_path.exists():
            print(f"\nTemplate source ({template_name}):")
            print("=" * 60)
            source = template_path.read_text()
            for i, line in enumerate(source.splitlines(), 1):
                marker = "→" if hasattr(e, 'lineno') and i == e.lineno else " "
                print(f"{marker} {i:3d}: {line}")
            print("=" * 60)

        # Show context
        print("\nContext:")
        context = config.generation.patterns[0].context
        for key, value in context.items():
            print(f"  {key}: {type(value).__name__} = {str(value)[:50]}")

        raise

# Use it
try:
    output = debug_generate(config)
except:
    print("\n✗ Generation failed. See details above.")
```

### Interactive Debugging

Use iPython/Jupyter for interactive debugging:

```python
# In Jupyter notebook or iPython
from jinja2 import Environment
env = Environment()

# Test template interactively
template_source = """
# {{ title }}

{% for item in items %}
- {{ item }}
{% endfor %}
"""

template = env.from_string(template_source)

# Try different contexts
context1 = {"title": "Test", "items": ["a", "b"]}
print(template.render(context1))

context2 = {"title": "Test", "items": []}
print(template.render(context2))

# Iterate quickly
```

---

## Troubleshooting Checklist

When debugging Jinja2 templates, work through this checklist:

**File Issues:**
- [ ] Template file exists at expected path
- [ ] Template file is readable (permissions)
- [ ] Template path is correct in config
- [ ] Template directory is correctly configured

**Syntax Issues:**
- [ ] All `{% %}` blocks are closed
- [ ] All `{{ }}` expressions are closed
- [ ] All `{# #}` comments are closed
- [ ] Block names match (e.g., `{% block content %}...{% endblock content %}`)
- [ ] No mixing of syntax types

**Context Issues:**
- [ ] All referenced variables exist in context
- [ ] Variable types are correct (list, dict, str, etc.)
- [ ] Nested access paths are valid (e.g., `user.profile.name`)
- [ ] Variables are not `None` where operations expected

**Logic Issues:**
- [ ] Loops iterate over iterables (list, tuple, dict)
- [ ] Conditionals reference boolean-convertible values
- [ ] Filters are chained in correct order
- [ ] Filter arguments are correct type

**Output Issues:**
- [ ] Special characters are escaped correctly
- [ ] Whitespace control is as expected
- [ ] Line endings are consistent
- [ ] Output encoding is correct (UTF-8)

---

## Best Practices

### 1. Use Strict Undefined

Catch undefined variables early:

```python
from jinja2 import StrictUndefined

generator = Jinja2Generator()
generator.env.undefined = StrictUndefined

# Now any undefined variable raises error immediately
# Better than silently rendering empty string
```

### 2. Validate Context Before Rendering

```python
def validate_context(context: dict, required_keys: list[str]) -> None:
    """Validate context has required keys."""
    missing = [key for key in required_keys if key not in context]

    if missing:
        raise ValueError(f"Missing required context keys: {missing}")

# Use it
required = ["title", "content", "author"]
validate_context(config.generation.patterns[0].context, required)

output = generator.generate(config)
```

### 3. Add Helpful Comments to Templates

```jinja2
{#
Template: api-reference.j2
Purpose: Generate API documentation from OpenAPI schema

Required context variables:
- api (dict): OpenAPI specification
- base_url (str): API base URL
- version (str): API version

Example:
    context = {
        "api": {...},
        "base_url": "https://api.example.com",
        "version": "1.0"
    }
#}

# API Reference v{{ version }}

...
```

### 4. Test Templates Independently

```python
# Create test suite for templates
import pytest
from jinja2 import Environment

@pytest.fixture
def env():
    return Environment()

def test_minimal_template(env):
    """Test template with minimal context."""
    template = env.from_string("{{ title }}")
    result = template.render({"title": "Test"})
    assert result == "Test"

def test_loop_template(env):
    """Test template with loop."""
    template = env.from_string("{% for i in items %}{{ i }}{% endfor %}")
    result = template.render({"items": [1, 2, 3]})
    assert result == "123"

def test_missing_variable_raises(env):
    """Test undefined variable raises error."""
    from jinja2 import StrictUndefined
    env.undefined = StrictUndefined

    template = env.from_string("{{ missing }}")

    with pytest.raises(Exception):
        template.render({})
```

### 5. Use Jinja2 Extensions Carefully

Only enable extensions you need:

```python
from jinja2 import Environment

env = Environment(
    extensions=[
        'jinja2.ext.do',  # {% do %} statement
        'jinja2.ext.loopcontrols',  # {% break %} and {% continue %}
    ]
)
```

---

## See Also

- [How to: Generate API Docs from OpenAPI](generate-api-docs-from-openapi.md) - Real-world template examples
- [How to: Use Template Inheritance](use-template-inheritance.md) - Complex template structures
- [Tutorial: Dynamic Content with Jinja2](../../tutorials/intermediate/01-dynamic-content-with-jinja2.md) - Learn Jinja2 basics
- [Jinja2Generator API Reference](../../reference/api/generators/jinja2.md) - Technical details
- [Jinja2 Official Documentation](https://jinja.palletsprojects.com) - Complete Jinja2 reference
