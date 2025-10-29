# How to Debug Generation Issues

> **Goal:** Diagnose and fix problems when content generation fails or produces unexpected output.

## When to Use This

You need this when:
- Generation produces errors
- Output is empty or incomplete
- Variables aren't being substituted
- Content structure looks wrong
- Performance is slow

## Prerequisites

- Content configuration and elements defined
- DemonstrationGenerator being used
- Basic understanding of generation patterns

---

## Solution

### Quick Debugging Checklist

```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.demonstration import DemonstrationGenerator

loader = ConfigLoader()

# 1. Can you load the config?
try:
    config = loader.load_content_config("your-config-id")
    print("✓ Config loads successfully")
except Exception as e:
    print(f"✗ Config load failed: {e}")
    exit(1)

# 2. Does config have generation patterns?
if not config.generation or not config.generation.patterns:
    print("✗ No generation patterns found")
    exit(1)
print(f"✓ Found {len(config.generation.patterns)} pattern(s)")

# 3. Is there a demonstration pattern?
demo_patterns = [p for p in config.generation.patterns if p.type.value == "demonstration"]
if not demo_patterns:
    print("✗ No demonstration pattern found")
    exit(1)
print(f"✓ Found demonstration pattern: {demo_patterns[0].id}")

# 4. Do elements have example_output?
empty_elements = [e.name for e in config.elements if not e.example_output]
if empty_elements:
    print(f"⚠ Elements without example_output: {empty_elements}")

# 5. Can you generate?
try:
    generator = DemonstrationGenerator()
    output = generator.generate(config)
    print(f"✓ Generation successful ({len(output)} chars)")
    print("\n=== Output Preview ===")
    print(output[:200] + ("..." if len(output) > 200 else ""))
except Exception as e:
    print(f"✗ Generation failed: {e}")
```

---

## Common Errors and Solutions

### Error: "Config has no generation patterns defined"

**Full error:**
```
ValueError: Config 'my-config' has no generation patterns defined
```

**Cause:** The config is missing the `generation.patterns` section.

**Solution:**

Add a generation section to your config:

```json
{
  "type": "content",
  "id": "my-config",
  "elements": [...],
  "generation": {
    "patterns": [
      {
        "id": "demo-pattern",
        "type": "demonstration",
        "template": "{{content}}",
        "variables": [
          {"name": "content", "source": "elements.content.example_output"}
        ]
      }
    ]
  }
}
```

**Verify:**
```python
config = loader.load_content_config("my-config")
assert config.generation is not None
assert len(config.generation.patterns) > 0
```

---

### Error: "Config has no demonstration generation pattern"

**Full error:**
```
ValueError: Config 'my-config' has no demonstration generation pattern
```

**Cause:** The config has patterns, but none with `"type": "demonstration"`.

**Solution:**

Ensure at least one pattern has the correct type:

```json
{
  "generation": {
    "patterns": [
      {
        "id": "my-pattern",
        "type": "demonstration",  // Must be exactly this
        "template": "{{content}}",
        "variables": [...]
      }
    ]
  }
}
```

**Common mistakes:**
- `"type": "demo"` ❌
- `"type": "Demonstration"` ❌ (case-sensitive)
- `"type": "template"` ❌

**Verify:**
```python
config = loader.load_content_config("my-config")
demo_pattern = next((p for p in config.generation.patterns if p.type.value == "demonstration"), None)
assert demo_pattern is not None, "No demonstration pattern found"
```

---

### Error: "Cannot resolve variable 'X' from source 'Y'"

**Full error:**
```
ValueError: Cannot resolve variable 'intro' from source 'elements.intro.example_output'
```

**Cause:** The variable source points to an element that doesn't exist or has no `example_output`.

**Solution 1: Check element exists**

```python
# Debug script
config = loader.load_content_config("my-config")
element_names = [e.name for e in config.elements]
print(f"Available elements: {element_names}")

# Check if your element is there
if "intro" not in element_names:
    print("✗ Element 'intro' not found")
```

**Solution 2: Check example_output populated**

```python
for element in config.elements:
    if not element.example_output:
        print(f"⚠ Element '{element.name}' has no example_output")
```

**Solution 3: Add default value**

```json
{
  "variables": [
    {
      "name": "intro",
      "source": "elements.intro.example_output",
      "default": "[Introduction pending]"
    }
  ]
}
```

**Solution 4: Fix source path**

Common mistakes:
- `"source": "elements.intro"` ❌ (missing `.example_output`)
- `"source": "element.intro.example_output"` ❌ (should be "elements" plural)
- `"source": "elements.Intro.example_output"` ❌ (case mismatch)

Correct:
```json
{"source": "elements.intro.example_output"} ✓
```

---

### Problem: Variables Not Substituted in Output

**Symptom:** Output contains literal `{{varname}}` instead of content.

**Cause:** Variable name in template doesn't match variable definition.

**Debug:**

```python
config = loader.load_content_config("my-config")
pattern = config.generation.patterns[0]

# Check template variables
import re
template_vars = re.findall(r'\{\{\s*(\w+)\s*\}\}', pattern.template)
print(f"Variables in template: {template_vars}")

# Check defined variables
defined_vars = [v.name for v in pattern.variables]
print(f"Defined variables: {defined_vars}")

# Find mismatches
missing = set(template_vars) - set(defined_vars)
if missing:
    print(f"✗ Template uses undefined variables: {missing}")
```

**Solution:**

Ensure exact match:

```json
{
  "template": "{{intro}}\n{{body}}",
  "variables": [
    {"name": "intro", "source": "..."},  // Must match template
    {"name": "body", "source": "..."}    // Must match template
  ]
}
```

**Common mistakes:**
- Template: `{{introduction}}`, Variable: `{"name": "intro"}` ❌
- Template: `{{body}}`, Variable: `{"name": "Body"}` ❌ (case mismatch)

---

### Problem: Empty Output

**Symptom:** Generator succeeds but produces empty string.

**Cause:** Template is empty or all variables resolve to empty strings.

**Debug:**

```python
config = loader.load_content_config("my-config")
pattern = config.generation.patterns[0]

# Check template
if not pattern.template or pattern.template.strip() == "":
    print("✗ Template is empty")

# Check elements
for element in config.elements:
    content = element.example_output or ""
    print(f"Element '{element.name}': {len(content)} chars")
    if len(content) == 0:
        print(f"  ⚠ Empty!")
```

**Solution:**

Ensure template and elements have content:

```json
{
  "elements": [
    {
      "name": "intro",
      "example_output": "Some actual content here"  // Not empty
    }
  ],
  "generation": {
    "patterns": [{
      "template": "{{intro}}"  // Not empty
    }]
  }
}
```

---

### Problem: Extra Newlines or Spacing Issues

**Symptom:** Output has unexpected blank lines or spacing.

**Cause:** Template has explicit `\n` characters that may not align with content.

**Debug:**

```python
# Visualize template with escaped characters
pattern = config.generation.patterns[0]
print(repr(pattern.template))  # Shows \n explicitly
```

**Solution 1: Adjust template newlines**

```json
// Before
{"template": "{{intro}}\n\n\n{{body}}"}  // Too many newlines

// After
{"template": "{{intro}}\n\n{{body}}"}    // Just right
```

**Solution 2: Check element content**

Elements might already include trailing newlines:

```json
{
  "elements": [
    {
      "name": "intro",
      "example_output": "Introduction\n\n"  // Has trailing newlines
    }
  ]
}
```

If template also adds newlines: `{{intro}}\n\n{{body}}`, you get 4 newlines total.

---

### Problem: JSON Syntax Errors

**Symptom:** Config won't load, JSON parsing fails.

**Common mistakes:**

**Missing comma:**
```json
{
  "name": "intro"
  "source": "..."  // ❌ Missing comma after "intro"
}
```

**Extra comma:**
```json
{
  "variables": [
    {"name": "intro", "source": "..."},
    {"name": "body", "source": "..."},  // ❌ Extra comma before ]
  ]
}
```

**Unescaped quotes:**
```json
{
  "template": "He said "hello""  // ❌ Should be \"hello\"
}
```

**Newlines in strings:**
```json
{
  "template": "Line 1
Line 2"  // ❌ Can't have literal newlines
}
```

Should be:
```json
{
  "template": "Line 1\nLine 2"  // ✓ Use \n
}
```

**Solution:** Use a JSON validator or linter:

```bash
# Validate JSON
python -m json.tool configs/content/my-config/my-config-content.json

# Or use jq
jq . configs/content/my-config/my-config-content.json
```

---

## Debugging Techniques

### Technique 1: Incremental Building

Start minimal, add complexity gradually:

**Step 1: Minimal config**
```json
{
  "elements": [{"name": "test", "example_output": "Hello"}],
  "generation": {
    "patterns": [{
      "type": "demonstration",
      "template": "{{test}}",
      "variables": [{"name": "test", "source": "elements.test.example_output"}]
    }]
  }
}
```

**Test:** Does this work?

**Step 2: Add second element**
```json
{
  "elements": [
    {"name": "test", "example_output": "Hello"},
    {"name": "test2", "example_output": "World"}
  ],
  "generation": {
    "patterns": [{
      "type": "demonstration",
      "template": "{{test}} {{test2}}",
      "variables": [
        {"name": "test", "source": "elements.test.example_output"},
        {"name": "test2", "source": "elements.test2.example_output"}
      ]
    }]
  }
}
```

**Test:** Does this work?

Continue adding one thing at a time.

### Technique 2: Inspect Loaded Config

```python
config = loader.load_content_config("my-config")

# Inspect config object
print(f"Config ID: {config.id}")
print(f"Elements: {len(config.elements)}")
for elem in config.elements:
    print(f"  - {elem.name}: {len(elem.example_output or '')} chars")

print(f"\nPatterns: {len(config.generation.patterns if config.generation else 0)}")
if config.generation:
    for pattern in config.generation.patterns:
        print(f"  - {pattern.id} (type: {pattern.type})")
        print(f"    Variables: {[v.name for v in pattern.variables]}")
        print(f"    Template length: {len(pattern.template or '')} chars")
```

### Technique 3: Manual Variable Resolution

```python
def debug_variable_resolution(config):
    """Manually resolve variables to see what's happening."""
    pattern = config.generation.patterns[0]

    element_data = {
        elem.name: elem.example_output or ""
        for elem in config.elements
    }

    print("=== Element Data ===")
    for name, content in element_data.items():
        print(f"{name}: {repr(content[:50])}")

    print("\n=== Variable Resolution ===")
    for var in pattern.variables:
        print(f"\nVariable: {var.name}")
        print(f"  Source: {var.source}")

        # Try to resolve
        if var.source.startswith("elements."):
            parts = var.source.split(".")
            elem_name = parts[1]
            if elem_name in element_data:
                print(f"  Resolved: {repr(element_data[elem_name][:50])}")
            else:
                print(f"  ✗ Element '{elem_name}' not found")
                print(f"  Available: {list(element_data.keys())}")

# Run it
config = loader.load_content_config("my-config")
debug_variable_resolution(config)
```

### Technique 4: Compare Expected vs Actual

```python
def compare_output(config, expected: str):
    """Generate and compare with expected output."""
    generator = DemonstrationGenerator()
    actual = generator.generate(config)

    if actual == expected:
        print("✓ Output matches expected")
    else:
        print("✗ Output differs from expected")
        print(f"\nExpected ({len(expected)} chars):")
        print(repr(expected))
        print(f"\nActual ({len(actual)} chars):")
        print(repr(actual))

        # Character-by-character diff
        for i, (e, a) in enumerate(zip(expected, actual)):
            if e != a:
                print(f"\nFirst difference at position {i}:")
                print(f"  Expected: {repr(e)}")
                print(f"  Actual: {repr(a)}")
                break
```

---

## Performance Debugging

### Problem: Slow Generation

**Measure:**
```python
import time

start = time.time()
output = generator.generate(config)
elapsed = time.time() - start

print(f"Generation took {elapsed:.3f}s for {len(output)} chars")
```

**Common causes:**

1. **Large configs:** Many elements (50+)
2. **Complex templates:** Very long template strings
3. **Repeated generator creation:**

```python
# Bad: Creates new generator each time
for config_id in config_ids:
    generator = DemonstrationGenerator()  # Wasteful
    output = generator.generate(config)

# Good: Reuse generator
generator = DemonstrationGenerator()
for config_id in config_ids:
    output = generator.generate(config)  # Faster
```

**Solution:** DemonstrationGenerator is stateless and fast. If slow:
- Check ConfigLoader caching (should cache schemas)
- Profile your code to find actual bottleneck
- Most time is usually in file I/O (loading configs)

---

## See Also

- [How to: Use Demonstration Generator](use-demonstration-generator.md) - Common patterns
- [How to: Create Generation Patterns](create-generation-patterns.md) - Pattern design
- [DemonstrationGenerator API Reference](../../reference/api/generators/demonstration.md) - Technical details
- [Tutorial: Generate Your First Content](../../tutorials/getting-started/03-generate-your-first-content.md) - Basic walkthrough
