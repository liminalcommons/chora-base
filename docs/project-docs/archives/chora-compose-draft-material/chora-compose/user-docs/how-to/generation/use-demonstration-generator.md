# How to Use the Demonstration Generator

> **Goal:** Generate content using the DemonstrationGenerator with various patterns and configurations.

## When to Use This

You need the DemonstrationGenerator when:
- You have static content examples ready to use
- You want predictable, repeatable output
- You need to assemble pre-written content sections
- You're creating documentation or templates from examples
- You don't need runtime variable substitution (use Jinja2Generator for that)

## Prerequisites

- Chora Compose installed via Poetry
- Content configuration created
- Basic understanding of content configs
- Completed [Tutorial: Generate Your First Content](../../tutorials/getting-started/03-generate-your-first-content.md)

---

## Solution

### Quick Version

```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.demonstration import DemonstrationGenerator

# Load config and generate
loader = ConfigLoader()
config = loader.load_content_config("your-content-id")
generator = DemonstrationGenerator()
output = generator.generate(config)

print(output)
```

### Detailed Steps

#### 1. Set Up Your Content Config

Your config needs elements with `example_output` and a demonstration pattern:

```json
{
  "type": "content",
  "id": "my-content",
  "elements": [
    {
      "name": "section1",
      "format": "markdown",
      "example_output": "# Section 1\n\nThis is the first section."
    },
    {
      "name": "section2",
      "format": "markdown",
      "example_output": "# Section 2\n\nThis is the second section."
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "demo",
        "type": "demonstration",
        "template": "{{section1}}\n\n{{section2}}",
        "variables": [
          {"name": "section1", "source": "elements.section1.example_output"},
          {"name": "section2", "source": "elements.section2.example_output"}
        ]
      }
    ]
  }
}
```

#### 2. Load and Generate

```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.demonstration import DemonstrationGenerator

loader = ConfigLoader()
config = loader.load_content_config("my-content")

generator = DemonstrationGenerator()
result = generator.generate(config)

print(result)
```

**Output:**
```
# Section 1

This is the first section.

# Section 2

This is the second section.
```

#### 3. Save to File

```python
from pathlib import Path

output_path = Path("output/my-content.md")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(result, encoding="utf-8")

print(f"✓ Generated: {output_path}")
```

---

## Common Patterns

### Pattern: Simple Concatenation

Combine multiple sections in order:

```json
{
  "generation": {
    "patterns": [{
      "type": "demonstration",
      "template": "{{intro}}\n\n{{body}}\n\n{{conclusion}}",
      "variables": [
        {"name": "intro", "source": "elements.intro.example_output"},
        {"name": "body", "source": "elements.body.example_output"},
        {"name": "conclusion", "source": "elements.conclusion.example_output"}
      ]
    }]
  }
}
```

**Use case:** Building multi-section documents

### Pattern: Templated Structure

Add formatting around content:

```json
{
  "generation": {
    "patterns": [{
      "type": "demonstration",
      "template": "---\ntitle: {{title}}\n---\n\n{{content}}",
      "variables": [
        {"name": "title", "source": "elements.title.example_output"},
        {"name": "content", "source": "elements.content.example_output"}
      ]
    }]
  }
}
```

**Use case:** Adding frontmatter or wrappers

### Pattern: Code Documentation

Generate code with documentation:

```json
{
  "generation": {
    "patterns": [{
      "type": "demonstration",
      "template": "\"\"\"{{docstring}}\"\"\"\n\n{{code}}",
      "variables": [
        {"name": "docstring", "source": "elements.docstring.example_output"},
        {"name": "code", "source": "elements.code.example_output"}
      ]
    }]
  }
}
```

**Use case:** Generating Python modules with docs

### Pattern: Repeated Sections

Use the same element multiple times:

```json
{
  "generation": {
    "patterns": [{
      "type": "demonstration",
      "template": "# Header\n\n{{description}}\n\n## Details\n\n{{description}}",
      "variables": [
        {"name": "description", "source": "elements.description.example_output"}
      ]
    }]
  }
}
```

**Use case:** Reusing content in different contexts

### Pattern: Access by Index

Reference elements by position instead of name:

```json
{
  "generation": {
    "patterns": [{
      "type": "demonstration",
      "template": "{{first}}\n{{second}}\n{{third}}",
      "variables": [
        {"name": "first", "source": "elements.0.example_output"},
        {"name": "second", "source": "elements.1.example_output"},
        {"name": "third", "source": "elements.2.example_output"}
      ]
    }]
  }
}
```

**Use case:** When element names aren't important

### Pattern: Default Values

Provide fallbacks for missing content:

```json
{
  "generation": {
    "patterns": [{
      "type": "demonstration",
      "template": "{{content}}",
      "variables": [
        {
          "name": "content",
          "source": "elements.content.example_output",
          "default": "[Content not yet written]"
        }
      ]
    }]
  }
}
```

**Use case:** Graceful degradation when content is incomplete

---

## Real-World Example

**Scenario:** Generate README files for multiple projects with consistent structure

**Config:** `configs/content/readme-template/readme-template-content.json`

```json
{
  "type": "content",
  "id": "readme-template-content",
  "metadata": {
    "description": "Standard README structure",
    "output_format": "markdown"
  },
  "elements": [
    {
      "name": "title",
      "format": "markdown",
      "example_output": "# My Project"
    },
    {
      "name": "description",
      "format": "markdown",
      "example_output": "A brief description of what this project does."
    },
    {
      "name": "installation",
      "format": "markdown",
      "example_output": "## Installation\n\n```bash\nnpm install my-project\n```"
    },
    {
      "name": "usage",
      "format": "markdown",
      "example_output": "## Usage\n\n```javascript\nconst myProject = require('my-project');\n```"
    },
    {
      "name": "license",
      "format": "markdown",
      "example_output": "## License\n\nMIT"
    }
  ],
  "generation": {
    "patterns": [{
      "id": "readme-structure",
      "type": "demonstration",
      "template": "{{title}}\n\n{{description}}\n\n{{installation}}\n\n{{usage}}\n\n{{license}}",
      "variables": [
        {"name": "title", "source": "elements.title.example_output"},
        {"name": "description", "source": "elements.description.example_output"},
        {"name": "installation", "source": "elements.installation.example_output"},
        {"name": "usage", "source": "elements.usage.example_output"},
        {"name": "license", "source": "elements.license.example_output"}
      ]
    }]
  }
}
```

**Generation script:**

```python
from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.demonstration import DemonstrationGenerator

def generate_readme(config_id: str, output_path: Path):
    """Generate README from demonstration config."""
    loader = ConfigLoader()
    config = loader.load_content_config(config_id)

    generator = DemonstrationGenerator()
    content = generator.generate(config)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(f"✓ Generated {output_path}")

# Generate README
generate_readme("readme-template-content", Path("output/README.md"))
```

**Result:** `output/README.md`
```markdown
# My Project

A brief description of what this project does.

## Installation

```bash
npm install my-project
```

## Usage

```javascript
const myProject = require('my-project');
```

## License

MIT
```

---

## Advanced Usage

### Multiple Generation Patterns

A config can have multiple patterns for different outputs:

```json
{
  "generation": {
    "patterns": [
      {
        "id": "full-version",
        "type": "demonstration",
        "template": "{{intro}}\n\n{{details}}\n\n{{conclusion}}",
        "variables": [...]
      },
      {
        "id": "summary-version",
        "type": "demonstration",
        "template": "{{intro}}\n\n{{conclusion}}",
        "variables": [...]
      }
    ]
  }
}
```

The generator uses the first `demonstration` pattern by default.

### Whitespace in Template Variables

Variables handle optional whitespace:

```json
{
  "template": "{{ var1 }} {{var2}} {{  var3  }}"
}
```

All three formats work: `{{ var }}`, `{{var}}`, `{{  var  }}`

### Escaped Characters

Templates automatically unescape `\n` and `\t`:

```json
{
  "template": "Line 1\\nLine 2\\tIndented"
}
```

Renders as:
```
Line 1
Line 2	Indented
```

---

## Troubleshooting

**Problem:** `ValueError: Config has no generation patterns defined`
**Solution:**
- Add a `generation.patterns` array to your config
- Ensure at least one pattern exists
- Check JSON syntax is valid

**Problem:** `ValueError: Config has no demonstration generation pattern`
**Solution:**
- Ensure at least one pattern has `"type": "demonstration"`
- Check pattern type is spelled correctly
- Verify pattern is in the `patterns` array

**Problem:** `ValueError: Cannot resolve variable 'varname' from source`
**Solution:**
- Check that element name in source matches exactly (case-sensitive)
- Verify element has `example_output` field populated
- Try using index-based source: `elements.0.example_output`
- Consider adding a `default` value to the variable

**Problem:** Variables not substituted in output
**Solution:**
- Verify variable names in template match variable definitions
- Use `{{varname}}` syntax (double curly braces)
- Check variable source points to valid element
- Ensure no typos in variable names

**Problem:** Output has literal `\n` instead of newlines
**Solution:**
- This is a JSON escaping issue
- The generator automatically unescapes `\n` → newline
- If you see literal `\n`, check your JSON is valid
- May need to double-escape in some contexts: `\\n`

**Problem:** Empty output generated
**Solution:**
- Check that elements have `example_output` populated
- Verify template is not empty
- Ensure variables are correctly mapped
- Look for error messages about missing variables

---

## Performance Tips

**Reuse Generator Instance:**
```python
# Good: Reuse generator
generator = DemonstrationGenerator()
for config_id in config_ids:
    config = loader.load_content_config(config_id)
    output = generator.generate(config)

# Less efficient: Create new generator each time
for config_id in config_ids:
    generator = DemonstrationGenerator()  # Unnecessary
    config = loader.load_content_config(config_id)
    output = generator.generate(config)
```

**Batch Generation:**
```python
def batch_generate(config_ids: list[str]) -> dict[str, str]:
    """Generate content for multiple configs efficiently."""
    loader = ConfigLoader()
    generator = DemonstrationGenerator()

    results = {}
    for config_id in config_ids:
        config = loader.load_content_config(config_id)
        results[config_id] = generator.generate(config)

    return results
```

---

## See Also

- [Tutorial: Generate Your First Content](../../tutorials/getting-started/03-generate-your-first-content.md) - Learn the basics
- [How to: Create Generation Patterns](create-generation-patterns.md) - Design patterns
- [How to: Debug Generation](debug-generation.md) - Troubleshooting guide
- [DemonstrationGenerator API Reference](../../reference/api/generators/demonstration.md) - Complete API
- [Generator Strategy Pattern](../../explanation/architecture/generator-strategy-pattern.md) - Design explanation
