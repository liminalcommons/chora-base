# Jinja2Generator API Reference

> **Purpose:** Generate dynamic content using Jinja2 templates with context data from configurations or external sources.

## Overview

The `Jinja2Generator` is a content generator that uses Jinja2 templates to produce dynamic output. Unlike `DemonstrationGenerator` (which uses static `example_output`), Jinja2Generator:

1. Loads a Jinja2 template file
2. Merges template with context data
3. Renders template to produce final output
4. Supports template inheritance, macros, filters, and control structures

This enables complex, data-driven content generation where the same template can produce different output based on context.

**Location:** [src/chora_compose/generators/jinja2.py](../../../../src/chora_compose/generators/jinja2.py)

**Since:** Version 0.2.0 (planned)

---

## Quick Reference

```python
from pathlib import Path
from chora_compose.generators.jinja2 import Jinja2Generator

# Create generator
generator = Jinja2Generator(template_dir=Path("templates"))

# Generate from config
config = loader.load_content_config("my-content")
output = generator.generate(config)

# Generate with custom context
output = generator.generate(config, context={"extra": "data"})

print(output)
```

---

## Classes

### Class: Jinja2Generator

```python
class Jinja2Generator(GeneratorStrategy):
    """
    Generates content using Jinja2 templates.

    This generator loads Jinja2 templates and renders them with context data.
    Supports template inheritance, macros, filters, and all Jinja2 features.

    The generator uses context from content config's generation.patterns[].context
    or from explicitly provided context parameter.
    """
```

Content generator using Jinja2 template engine.

**Inherits from:** `GeneratorStrategy` (base class for all generators)

**Thread Safety:** Thread-safe if each thread has its own generator instance, OR if sharing instance and Jinja2 templates are stateless (no mutable global state).

**Since:** Version 0.2.0 (planned)

---

#### Constructor

```python
def __init__(
    self,
    template_dir: Path | None = None,
    **jinja_options
) -> None
```

Initialize the Jinja2 generator.

**Parameters:**

- `template_dir` (Path | None, optional): Directory containing Jinja2 template files. Templates are loaded from this directory. If `None`, uses current working directory. Templates referenced in configs should be relative to this directory. Default: `None`.

- `**jinja_options` (keyword arguments, optional): Additional options passed to `jinja2.Environment()`. Common options:
  - `autoescape` (bool): Enable auto-escaping (default: `False`)
  - `trim_blocks` (bool): Remove first newline after block (default: `False`)
  - `lstrip_blocks` (bool): Strip leading whitespace from blocks (default: `False`)
  - `extensions` (list[str]): Jinja2 extensions to enable
  - See [Jinja2 Environment docs](https://jinja.palletsprojects.com/api/#jinja2.Environment) for full options

**Attributes Set:**

- `self.template_dir` (Path): Template directory (provided or `Path.cwd()`)
- `self.env` (jinja2.Environment): Jinja2 environment instance configured with:
  - `FileSystemLoader` pointing to `template_dir`
  - Any provided `jinja_options`

**Example:**

```python
from pathlib import Path
from chora_compose.generators.jinja2 import Jinja2Generator

# Use default directory (current working directory)
generator = Jinja2Generator()

# Use specific template directory
generator = Jinja2Generator(template_dir=Path("templates"))

# With Jinja2 options
generator = Jinja2Generator(
    template_dir=Path("templates"),
    autoescape=True,  # Enable HTML auto-escaping
    trim_blocks=True,  # Cleaner output
    lstrip_blocks=True
)

# With extensions
generator = Jinja2Generator(
    template_dir=Path("templates"),
    extensions=['jinja2.ext.do', 'jinja2.ext.loopcontrols']
)
```

---

#### Methods

##### generate()

```python
def generate(
    self,
    config: ContentConfig,
    context: dict[str, Any] | None = None
) -> str
```

Generate content by rendering a Jinja2 template with context data.

This is the main method called by `ArtifactComposer` and users.

**Parameters:**

- `config` (ContentConfig, required): Content configuration containing generation pattern. The config must have `config.generation.patterns` with at least one pattern where `pattern.type == "jinja2"`. The pattern should specify:
  - `pattern.template` (str): Path to Jinja2 template (relative to `template_dir`)
  - `pattern.context` (dict): Context data for template rendering

- `context` (dict[str, Any] | None, optional): Additional context to merge with config's context. If provided, these values override config context values for the same keys. Use this to inject runtime data or override config values. Default: `None`.

**Returns:**

`str`: Generated content from rendered template. The exact output depends on the template and context data.

**Raises:**

- `GenerationError`: Wraps all errors that occur during generation:
  - No Jinja2 pattern found in config
  - Template file not found
  - Template syntax error
  - Undefined variable in template (if using StrictUndefined)
  - Template rendering error
  - Context data type mismatch
  - Any Jinja2 exception

**Workflow:**

1. Validate config has generation patterns
2. Find first pattern where `pattern.type == "jinja2"`
3. Load context from `pattern.context`
4. Merge with provided `context` parameter (if any)
5. Resolve context data sources:
   - If `context[key]` is dict with `{"source": "file", "path": "..."}`, load file content
   - If `context[key]` is dict with `{"source": "config", "id": "..."}`, load config
   - Otherwise, use value directly
6. Load template from `pattern.template`
7. Render template with merged context
8. Return rendered output

**Example:**

```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.jinja2 import Jinja2Generator

loader = ConfigLoader()
generator = Jinja2Generator(template_dir=Path("templates"))

# Basic generation
config = loader.load_content_config("readme-content")
output = generator.generate(config)

print(output)
```

**Example with custom context:**

```python
# Generate with runtime data override
config = loader.load_content_config("report-content")

# Override context at runtime
runtime_context = {
    "generated_date": datetime.now().strftime("%Y-%m-%d"),
    "version": "2.0",
    "author": "System"
}

output = generator.generate(config, context=runtime_context)
```

**Example with file loading:**

```python
# Content config with file reference
# configs/content/api-docs/api-docs-content.json
{
  "generation": {
    "patterns": [{
      "type": "jinja2",
      "template": "api-reference.j2",
      "context": {
        "api_spec": {
          "source": "file",
          "path": "data/openapi-spec.json"
        },
        "base_url": "https://api.example.com"
      }
    }]
  }
}

# Generate - api_spec will be loaded from file
output = generator.generate(config)
```

**Example error handling:**

```python
from chora_compose.generators.jinja2 import Jinja2Generator, GenerationError

generator = Jinja2Generator(template_dir=Path("templates"))

try:
    output = generator.generate(config)
    print(f"✓ Generated {len(output)} characters")

except GenerationError as e:
    error_msg = str(e)

    if "No jinja2 pattern" in error_msg:
        print("✗ Config missing jinja2 generation pattern")
    elif "Template not found" in error_msg:
        print("✗ Template file missing")
    elif "is undefined" in error_msg:
        print("✗ Template references undefined variable")
    else:
        print(f"✗ Generation failed: {e}")
```

---

##### register_filter()

```python
def register_filter(
    self,
    name: str,
    filter_func: Callable
) -> None
```

Register a custom Jinja2 filter.

Use this to add domain-specific or utility filters for use in templates.

**Parameters:**

- `name` (str, required): Name of the filter. Use this name in templates with pipe syntax: `{{ value | filter_name }}`.

- `filter_func` (Callable, required): Function implementing the filter. Should accept at least one argument (the value to filter) and return the filtered result. Can accept additional arguments for parameterized filters.

**Returns:**

`None`

**Example:**

```python
from chora_compose.generators.jinja2 import Jinja2Generator

generator = Jinja2Generator(template_dir=Path("templates"))

# Simple filter
def uppercase_first(text: str) -> str:
    """Uppercase first letter."""
    return text[0].upper() + text[1:] if text else text

generator.register_filter('uppercase_first', uppercase_first)

# Template can now use:
# {{ title | uppercase_first }}
```

**Example with parameters:**

```python
def truncate_words(text: str, count: int = 10, suffix: str = "...") -> str:
    """Truncate text to specified word count."""
    words = text.split()
    if len(words) <= count:
        return text
    return ' '.join(words[:count]) + suffix

generator.register_filter('truncate_words', truncate_words)

# Template usage:
# {{ description | truncate_words(5) }}
# {{ description | truncate_words(5, '…') }}
```

**Example with type conversion:**

```python
def format_bytes(size: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

generator.register_filter('format_bytes', format_bytes)

# Template:
# File size: {{ file_size | format_bytes }}
```

---

##### register_global()

```python
def register_global(
    self,
    name: str,
    value: Any
) -> None
```

Register a global variable or function available in all templates.

Use this to provide utility functions or constants accessible without context.

**Parameters:**

- `name` (str, required): Name of the global. Reference in templates without context: `{{ global_name }}` or `{{ global_func() }}`.

- `value` (Any, required): Value of the global. Can be any Python object:
  - Simple value (str, int, etc.): Used as constant
  - Function/callable: Can be called from template
  - Complex object: Access attributes/methods in template

**Returns:**

`None`

**Example with constants:**

```python
from chora_compose.generators.jinja2 import Jinja2Generator
from datetime import datetime

generator = Jinja2Generator(template_dir=Path("templates"))

# Register constants
generator.register_global('SITE_NAME', 'Chora Compose Documentation')
generator.register_global('CURRENT_YEAR', datetime.now().year)
generator.register_global('VERSION', '1.0.0')

# Template can use:
# Copyright © {{ CURRENT_YEAR }} {{ SITE_NAME }}
# Version: {{ VERSION }}
```

**Example with functions:**

```python
def now():
    """Get current datetime."""
    return datetime.now()

def random_id():
    """Generate random ID."""
    import uuid
    return str(uuid.uuid4())

generator.register_global('now', now)
generator.register_global('random_id', random_id)

# Template:
# Generated: {{ now().strftime('%Y-%m-%d %H:%M:%S') }}
# Request ID: {{ random_id() }}
```

**Example with objects:**

```python
class Utils:
    """Utility functions for templates."""

    @staticmethod
    def format_date(date_str):
        """Format ISO date to readable format."""
        from datetime import datetime
        dt = datetime.fromisoformat(date_str)
        return dt.strftime('%B %d, %Y')

    @staticmethod
    def pluralize(count, singular, plural=None):
        """Pluralize word based on count."""
        if count == 1:
            return singular
        return plural or f"{singular}s"

generator.register_global('utils', Utils())

# Template:
# Published: {{ utils.format_date('2025-10-11') }}
# Found {{ count }} {{ utils.pluralize(count, 'result') }}
```

---

## Internal Methods

The following methods are implementation details:

### _resolve_context_sources()

```python
def _resolve_context_sources(
    self,
    context: dict[str, Any]
) -> dict[str, Any]:
```

Resolve context values that reference external sources.

**Parameters:**
- `context` (dict): Context dictionary potentially containing source references

**Returns:**
- `dict`: Context with all sources resolved to actual values

**Resolves:**
- `{"source": "file", "path": "..."}` → Load and parse file (JSON/YAML)
- `{"source": "config", "id": "..."}` → Load content config
- Other values → Pass through unchanged

**Example:**
```python
# Input context
context = {
    "data": {"source": "file", "path": "data/users.json"},
    "title": "My Document"
}

# Resolved context
resolved = generator._resolve_context_sources(context)
# {
#     "data": {...parsed JSON content...},
#     "title": "My Document"
# }
```

---

## Exceptions

### Exception: GenerationError

```python
class GenerationError(Exception):
    """Raised when Jinja2 template generation fails."""
```

Wraps all errors that occur during Jinja2 generation.

**Inherits from:** `Exception`

**Common messages:**

- `"No jinja2 generation pattern found in config"` - Config missing Jinja2 pattern
- `"Template not found: {template}"` - Template file doesn't exist
- `"Template syntax error in {template}: {details}"` - Invalid Jinja2 syntax
- `"Undefined variable in template: {variable}"` - Template references missing variable
- `"Template rendering failed: {details}"` - Generic rendering error
- `"Failed to load context source: {details}"` - Cannot load file/config reference

**Example:**

```python
from chora_compose.generators.jinja2 import GenerationError

try:
    output = generator.generate(config)
except GenerationError as e:
    print(f"Generation failed: {e}")
    # e.args[0] contains the error message
    # Original exception available as e.__cause__
```

---

## Usage Patterns

### Pattern: Template with External Data

Load data from files for template rendering:

```python
from pathlib import Path
import json

# Create content config
config_data = {
    "type": "content",
    "id": "user-report",
    "generation": {
        "patterns": [{
            "type": "jinja2",
            "template": "user-report.j2",
            "context": {
                "users": {
                    "source": "file",
                    "path": "data/users.json"
                },
                "report_title": "User Activity Report",
                "generated_date": "2025-10-11"
            }
        }]
    }
}

# Save config
config_path = Path("configs/content/reports/user-report-content.json")
config_path.write_text(json.dumps(config_data, indent=2))

# Generate
config = loader.load_content_config("user-report")
output = generator.generate(config)
```

**Template** (`templates/user-report.j2`):
```jinja2
# {{ report_title }}

**Generated:** {{ generated_date }}

## User Summary

Total users: {{ users | length }}

{% for user in users %}
### {{ user.name }}

- Email: {{ user.email }}
- Status: {{ user.status }}
- Last login: {{ user.last_login }}

{% endfor %}
```

### Pattern: Dynamic Context Override

Override config context at generation time:

```python
from datetime import datetime

# Load config (has default context)
config = loader.load_content_config("daily-report")

# Generate with today's data
today_context = {
    "report_date": datetime.now().strftime("%Y-%m-%d"),
    "stats": fetch_daily_stats(),  # Get fresh data
    "author": get_current_user()
}

output = generator.generate(config, context=today_context)

# Save with date in filename
output_path = Path(f"reports/daily-{today_context['report_date']}.md")
output_path.write_text(output)
```

### Pattern: Batch Generation with Variants

Generate multiple outputs from one template:

```python
from pathlib import Path

# Load base config
config = loader.load_content_config("product-page")

# Generate for each product
products = [
    {"id": "widget-a", "name": "Widget A", "price": 29.99},
    {"id": "widget-b", "name": "Widget B", "price": 39.99},
    {"id": "widget-c", "name": "Widget C", "price": 49.99},
]

for product in products:
    # Generate with product-specific context
    output = generator.generate(config, context=product)

    # Save product-specific page
    output_path = Path(f"output/products/{product['id']}.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output)

    print(f"✓ Generated {product['id']}")
```

### Pattern: Custom Filters for Domain Logic

Add domain-specific formatting:

```python
from chora_compose.generators.jinja2 import Jinja2Generator

generator = Jinja2Generator(template_dir=Path("templates"))

# Domain-specific filters
def format_currency(amount, currency='USD'):
    """Format amount as currency."""
    symbol = {'USD': '$', 'EUR': '€', 'GBP': '£'}.get(currency, currency)
    return f"{symbol}{amount:,.2f}"

def status_badge(status):
    """Convert status to badge markdown."""
    colors = {
        'active': 'green',
        'inactive': 'gray',
        'pending': 'yellow',
        'error': 'red'
    }
    color = colors.get(status, 'blue')
    return f"![{status}](https://img.shields.io/badge/-{status}-{color})"

def format_list(items, style='bullet'):
    """Format list with specified style."""
    if style == 'bullet':
        return '\n'.join(f"- {item}" for item in items)
    elif style == 'numbered':
        return '\n'.join(f"{i}. {item}" for i, item in enumerate(items, 1))
    elif style == 'checkbox':
        return '\n'.join(f"- [ ] {item}" for item in items)
    return '\n'.join(items)

# Register filters
generator.register_filter('currency', format_currency)
generator.register_filter('status_badge', status_badge)
generator.register_filter('format_list', format_list)

# Template can use:
# Price: {{ product.price | currency }}
# Status: {{ product.status | status_badge }}
# {{ todos | format_list('checkbox') }}
```

---

## Performance Considerations

**Jinja2 Template Compilation:**
- Templates are compiled on first use
- Compiled templates are cached in `env.cache`
- Subsequent renders are fast (no re-parsing)
- First render: ~10-50ms
- Cached renders: ~1-5ms

**Context Resolution:**
- File loading (`{"source": "file"}`) adds I/O overhead
- JSON parsing adds processing time
- Cache external data if generating multiple times

**Optimization Tips:**

1. **Reuse generator instance:**
```python
# Good
generator = Jinja2Generator(template_dir=Path("templates"))
for config_id in config_ids:
    config = loader.load_content_config(config_id)
    output = generator.generate(config)

# Less efficient (re-initializes Jinja2 environment)
for config_id in config_ids:
    generator = Jinja2Generator(template_dir=Path("templates"))
    output = generator.generate(config)
```

2. **Pre-load context data:**
```python
# Load data once
data = json.loads(Path("data/users.json").read_text())

# Generate many times with same data
for variant in variants:
    context = {**data, **variant}
    output = generator.generate(config, context=context)
```

3. **Use template inheritance to reduce duplication:**
```jinja2
{# base.j2 - loaded once, cached #}
{% block content %}{% endblock %}

{# specific.j2 - extends base #}
{% extends "base.j2" %}
{% block content %}...{% endblock %}
```

**Typical Performance:**
- Simple templates (< 100 lines): 1-5ms
- Medium templates (100-500 lines): 5-20ms
- Complex templates (500+ lines, loops): 20-100ms
- Template inheritance adds minimal overhead (~1-2ms)

**Bottlenecks:**
- Large context data serialization
- Complex loops (e.g., nested loops over 1000+ items)
- File I/O for external context sources
- Custom filters with heavy computation

---

## Thread Safety

**Thread-safe with caveats:**

- ✅ Safe: Each thread has own `Jinja2Generator` instance
- ✅ Safe: Sharing generator IF templates are stateless
- ⚠️ Unsafe: Modifying `generator.env` from multiple threads
- ⚠️ Unsafe: Custom filters with mutable state

**Safe pattern:**
```python
import threading

def worker(config_id: str):
    generator = Jinja2Generator(template_dir=Path("templates"))
    config = loader.load_content_config(config_id)
    output = generator.generate(config)
    # Process output...

threads = [
    threading.Thread(target=worker, args=(f"config{i}",))
    for i in range(10)
]

for t in threads:
    t.start()
for t in threads:
    t.join()
```

**Shared generator (safe if templates stateless):**
```python
# Create once
generator = Jinja2Generator(template_dir=Path("templates"))

def worker(config_id: str):
    config = loader.load_content_config(config_id)
    # Safe: Jinja2 env is thread-safe for rendering
    output = generator.generate(config)

# Use from multiple threads
```

---

## Compatibility

**Python Versions:** 3.12+

**Dependencies:**
- `jinja2` >= 3.1.0
- `chora_compose.core.models` - ContentConfig model
- `chora_compose.generators.base` - GeneratorStrategy interface

**Jinja2 Version:** Tested with Jinja2 3.1.x

**Breaking Changes:**
- None yet (initial version)

---

## See Also

- [Tutorial: Dynamic Content with Jinja2](../../../tutorials/intermediate/01-dynamic-content-with-jinja2.md) - Learn basics
- [How to: Generate API Docs from OpenAPI](../../../how-to/generation/generate-api-docs-from-openapi.md) - Real-world example
- [How to: Use Template Inheritance](../../../how-to/generation/use-template-inheritance.md) - Advanced templates
- [How to: Debug Jinja2 Templates](../../../how-to/generation/debug-jinja2-templates.md) - Fix errors
- [DemonstrationGenerator API Reference](demonstration.md) - Alternative generator
- [Why Jinja2 for Dynamic Generation](../../../explanation/architecture/why-jinja2-for-dynamic-generation.md) - Design rationale
- [Jinja2 Official Documentation](https://jinja.palletsprojects.com) - Complete Jinja2 reference
