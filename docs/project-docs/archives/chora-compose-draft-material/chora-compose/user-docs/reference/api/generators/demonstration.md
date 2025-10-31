# DemonstrationGenerator API Reference

> **Purpose:** Generate content by extracting `example_output` from elements and substituting into templates.

## Overview

The `DemonstrationGenerator` is the simplest content generator in Chora Compose. It extracts `example_output` fields from content elements and performs straightforward template substitution using `{{variable}}` placeholders.

This generator is ideal when:
- Content is pre-written and static
- No runtime variable substitution needed
- Simple assembly of pre-existing sections
- Predictable, repeatable output is required

**Location:** [src/chora_compose/generators/demonstration.py](../../../../src/chora_compose/generators/demonstration.py)

**Since:** Version 0.1.0

---

## Quick Reference

```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.demonstration import DemonstrationGenerator

# Load config
loader = ConfigLoader()
config = loader.load_content_config("my-content")

# Generate
generator = DemonstrationGenerator()
output = generator.generate(config)

print(output)
```

---

## Classes

### Class: DemonstrationGenerator

```python
class DemonstrationGenerator(GeneratorStrategy):
    """
    Generator that uses example_output from elements.

    This is the simplest generation type - it extracts the example_output
    field from elements and substitutes them into a template using simple
    {{variable}} placeholder replacement.
    """
```

Content generator using static example content from config elements.

**Inheritance:** [GeneratorStrategy](base.md)

**Thread Safety:** Thread-safe (stateless)

**Since:** Version 0.1.0

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

Generate content by extracting `example_output` from elements and substituting into template.

**Parameters:**

- `config` (ContentConfig, required): Content configuration containing:
  - `elements`: List of content elements with `example_output` fields
  - `generation.patterns`: At least one pattern with `type="demonstration"`

- `context` (dict[str, Any] | None, optional): Optional additional context data. **Note:** Currently not used by DemonstrationGenerator (reserved for future generators like Jinja2Generator). Default: `None`.

**Returns:**

`str`: Generated content with all template variables substituted with element `example_output` values.

**Raises:**

- `ValueError`: If config has no generation patterns defined
- `ValueError`: If config has no demonstration-type pattern
- `ValueError`: If a required variable cannot be resolved from its source
- `ValueError`: If variable source points to non-existent element

**Example:**

```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.demonstration import DemonstrationGenerator

# Load config with demonstration pattern
loader = ConfigLoader()
config = loader.load_content_config("readme-content")

# Generate content
generator = DemonstrationGenerator()
output = generator.generate(config)

print(f"Generated {len(output)} characters")
print(output)
```

**Example with error handling:**

```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.demonstration import DemonstrationGenerator

loader = ConfigLoader()
generator = DemonstrationGenerator()

try:
    config = loader.load_content_config("my-content")
    output = generator.generate(config)
    print("Success!")
except ValueError as e:
    if "no generation patterns" in str(e):
        print("Error: Config missing generation.patterns section")
    elif "no demonstration" in str(e):
        print("Error: No pattern with type='demonstration' found")
    elif "Cannot resolve variable" in str(e):
        print(f"Error: Variable resolution failed - {e}")
    else:
        print(f"Error: {e}")
```

**Example reusing generator:**

```python
# Efficient: Reuse generator instance
generator = DemonstrationGenerator()

for config_id in ["config1", "config2", "config3"]:
    config = loader.load_content_config(config_id)
    output = generator.generate(config)
    print(f"{config_id}: {len(output)} chars")
```

---

## Internal Methods

The following methods are implementation details but documented for completeness and debugging:

### _resolve_variable_source()

```python
def _resolve_variable_source(
    self,
    source: str,
    element_data: dict[str, str],
    config: ContentConfig
) -> str | None
```

Resolve a variable source path to actual element data.

**Parameters:**
- `source` (str): Source path like `"elements.intro.example_output"` or `"elements.0.example_output"`
- `element_data` (dict[str, str]): Pre-extracted mapping of element names to their `example_output`
- `config` (ContentConfig): Full config for indexed element access

**Returns:**
- `str | None`: Resolved value from element, or `None` if not found

**Source Path Formats:**

**By name (recommended):**
```
"elements.{element_name}.example_output"
```
Example: `"elements.introduction.example_output"`

**By index:**
```
"elements.{index}.example_output"
```
Example: `"elements.0.example_output"` (first element)

**Resolution Logic:**

1. Parse source path: `elements.{identifier}.example_output`
2. Try resolving by name first: Look up `identifier` in `element_data`
3. If not found, try parsing `identifier` as integer index
4. If index valid (0 ≤ index < len(elements)), return `config.elements[index].example_output`
5. Otherwise return `None`

**Example:**

```python
# Given config with elements: [{"name": "intro", ...}, {"name": "body", ...}]
element_data = {"intro": "Introduction text", "body": "Body text"}

# By name
result = generator._resolve_variable_source(
    "elements.intro.example_output",
    element_data,
    config
)
# Returns: "Introduction text"

# By index
result = generator._resolve_variable_source(
    "elements.0.example_output",
    element_data,
    config
)
# Returns: "Introduction text" (first element)

# Not found
result = generator._resolve_variable_source(
    "elements.nonexistent.example_output",
    element_data,
    config
)
# Returns: None
```

---

### _substitute_template()

```python
def _substitute_template(
    self,
    template: str,
    variables: dict[str, str]
) -> str
```

Substitute `{{variable}}` placeholders in template with actual values.

**Parameters:**
- `template` (str): Template string with `{{variable}}` placeholders
- `variables` (dict[str, str]): Mapping of variable names to replacement values

**Returns:**
- `str`: Template with all variables substituted

**Substitution Rules:**

1. Finds all `{{varname}}` patterns (with optional whitespace)
2. Replaces each with corresponding value from `variables` dict
3. Unescapes `\n` → newline
4. Unescapes `\t` → tab

**Regex Pattern:** `\{\{\s*{varname}\s*\}\}`

**Supports whitespace variations:**
- `{{var}}` ✓
- `{{ var }}` ✓
- `{{  var  }}` ✓

**Example:**

```python
template = "# {{title}}\n\n{{intro}}\n\n## Details\n\n{{ details }}"
variables = {
    "title": "My Document",
    "intro": "Welcome!",
    "details": "Here are the details..."
}

result = generator._substitute_template(template, variables)

# Result:
# # My Document
#
# Welcome!
#
# ## Details
#
# Here are the details...
```

**Example with escaped characters:**

```python
template = "Line 1\\nLine 2\\tIndented"
variables = {}

result = generator._substitute_template(template, variables)

# Result:
# Line 1
# Line 2	Indented
```

---

### _extract_element_data()

Inherited from [GeneratorStrategy](base.md#_extract_element_data).

```python
def _extract_element_data(self, config: ContentConfig) -> dict[str, str]
```

Extract element data into dictionary for easy access.

**Parameters:**
- `config` (ContentConfig): Content configuration with elements

**Returns:**
- `dict[str, str]`: Mapping of element names to their `example_output` (empty string if `None`)

**Example:**

```python
# Config has elements: [
#   {"name": "intro", "example_output": "Welcome"},
#   {"name": "body", "example_output": "Content here"},
#   {"name": "footer", "example_output": None}
# ]

element_data = generator._extract_element_data(config)

# Returns:
# {
#   "intro": "Welcome",
#   "body": "Content here",
#   "footer": ""  # None converted to empty string
# }
```

---

## Usage Patterns

### Pattern: Simple Document Generation

```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.demonstration import DemonstrationGenerator

def generate_readme(config_id: str = "readme-content") -> str:
    """Generate README from config."""
    loader = ConfigLoader()
    config = loader.load_content_config(config_id)

    generator = DemonstrationGenerator()
    return generator.generate(config)

# Use it
readme = generate_readme()
print(readme)
```

### Pattern: Batch Generation

```python
def batch_generate(config_ids: list[str]) -> dict[str, str]:
    """Generate content for multiple configs."""
    loader = ConfigLoader()
    generator = DemonstrationGenerator()

    results = {}
    for config_id in config_ids:
        try:
            config = loader.load_content_config(config_id)
            output = generator.generate(config)
            results[config_id] = output
        except Exception as e:
            print(f"Failed to generate {config_id}: {e}")
            results[config_id] = None

    return results

# Use it
outputs = batch_generate(["config1", "config2", "config3"])
```

### Pattern: Save to File

```python
from pathlib import Path

def generate_and_save(config_id: str, output_path: Path) -> None:
    """Generate content and save to file."""
    loader = ConfigLoader()
    config = loader.load_content_config(config_id)

    generator = DemonstrationGenerator()
    content = generator.generate(config)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(f"✓ Generated {output_path} ({len(content)} chars)")

# Use it
generate_and_save("readme-content", Path("output/README.md"))
```

### Pattern: Conditional Generation

```python
def generate_if_valid(config_id: str) -> str | None:
    """Generate only if config is valid."""
    loader = ConfigLoader()

    try:
        config = loader.load_content_config(config_id)
    except Exception:
        return None  # Config invalid

    # Check if has demonstration pattern
    if not config.generation or not config.generation.patterns:
        return None

    has_demo = any(
        p.type.value == "demonstration"
        for p in config.generation.patterns
    )
    if not has_demo:
        return None

    generator = DemonstrationGenerator()
    return generator.generate(config)
```

---

## Error Handling

### Common Exceptions

**ValueError: "Config has no generation patterns defined"**

Raised when `config.generation` is `None` or `config.generation.patterns` is empty.

**Fix:** Add `generation.patterns` to config:
```json
{
  "generation": {
    "patterns": [
      {
        "type": "demonstration",
        "template": "...",
        "variables": [...]
      }
    ]
  }
}
```

---

**ValueError: "Config has no demonstration generation pattern"**

Raised when no pattern has `type="demonstration"`.

**Fix:** Ensure at least one pattern has correct type:
```json
{
  "patterns": [
    {
      "type": "demonstration",  // Must be this exact string
      "template": "...",
      "variables": [...]
    }
  ]
}
```

---

**ValueError: "Cannot resolve variable '{name}' from source '{source}'"**

Raised when variable source cannot be resolved to actual data.

**Causes:**
- Element doesn't exist
- Element has no `example_output`
- Source path syntax incorrect

**Fix:**
- Verify element name matches source
- Populate `example_output` fields
- Use correct source syntax: `elements.{name}.example_output`
- Add default value: `{"name": "var", "source": "...", "default": "fallback"}`

---

## Performance Considerations

**Stateless and Fast:**
- DemonstrationGenerator has no internal state
- Safe to reuse across multiple generations
- Each `generate()` call is independent

**Typical Performance:**
- Small configs (< 10 elements): < 10ms
- Medium configs (10-50 elements): < 50ms
- Large configs (50+ elements): < 200ms

**Optimization Tips:**

1. **Reuse generator instance:**
```python
# Good
generator = DemonstrationGenerator()
for config in configs:
    output = generator.generate(config)

# Less efficient
for config in configs:
    generator = DemonstrationGenerator()  # Unnecessary
    output = generator.generate(config)
```

2. **Reuse ConfigLoader:**
```python
loader = ConfigLoader()  # Caches schemas
for config_id in config_ids:
    config = loader.load_content_config(config_id)
```

3. **Parallel generation (if needed):**
```python
from concurrent.futures import ThreadPoolExecutor

def generate_one(config_id: str) -> str:
    loader = ConfigLoader()
    config = loader.load_content_config(config_id)
    generator = DemonstrationGenerator()
    return generator.generate(config)

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(generate_one, config_ids))
```

---

## Thread Safety

✅ **Thread-safe:** DemonstrationGenerator is completely stateless and safe for concurrent use from multiple threads.

```python
import threading

generator = DemonstrationGenerator()  # Shared across threads

def worker(config_id: str):
    config = loader.load_content_config(config_id)
    output = generator.generate(config)  # Thread-safe
    print(f"Generated {config_id}")

threads = [
    threading.Thread(target=worker, args=(f"config{i}",))
    for i in range(10)
]

for t in threads:
    t.start()
for t in threads:
    t.join()
```

---

## Compatibility

**Python Versions:** 3.12+

**Dependencies:**
- `chora_compose.core.models` - ContentConfig, GenerationType
- `chora_compose.generators.base` - GeneratorStrategy

**Breaking Changes:**
- None yet (initial version)

---

## See Also

- [Tutorial: Generate Your First Content](../../../tutorials/getting-started/03-generate-your-first-content.md) - Learn the basics
- [How to: Use Demonstration Generator](../../../how-to/generation/use-demonstration-generator.md) - Common patterns
- [How to: Create Generation Patterns](../../../how-to/generation/create-generation-patterns.md) - Design patterns
- [How to: Debug Generation](../../../how-to/generation/debug-generation.md) - Troubleshooting
- [GeneratorStrategy Base Class](base.md) - Abstract base
- [Generator Strategy Pattern Explanation](../../../explanation/architecture/generator-strategy-pattern.md) - Design rationale
