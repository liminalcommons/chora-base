# Tutorial: Generate Your First Content

> **Learning Goal:** Use the DemonstrationGenerator to create actual content from configurations, understanding the complete workflow from config to output.

## What You'll Learn

By completing this tutorial, you'll:
- Generate content using the DemonstrationGenerator
- Understand demonstration-based generation patterns
- Create custom content configurations
- Save generated output to files
- Work with templates and variables

## Prerequisites

- [ ] Chora Compose installed ([Installation Guide](01-installation.md))
- [ ] Python 3.12+
- [ ] Completed [Your First Config Tutorial](02-your-first-config.md)
- [ ] Understanding of content configurations

**Time Required:** ~20 minutes

---

## Understanding Demonstration Generation

The **DemonstrationGenerator** is Chora Compose's simplest generation strategy. It works by:

1. Reading `example_output` from elements in your configuration
2. Using a template with `{{variable}}` placeholders
3. Substituting placeholders with actual element data

**Why "demonstration"?** You demonstrate what the output should look like with examples, and the generator assembles them according to your template.

### Visual Flow

```
Content Configuration
  ├─ Element: "introduction"
  │    example_output: "# Welcome to My Project..."
  ├─ Element: "usage"
  │    example_output: "To use this feature..."
  └─ Generation Pattern
       template: "{{introduction}}\n\n{{usage}}"
                    ↓
          DemonstrationGenerator
                    ↓
       Final Output: Combined content
```

---

## Step 1: Examine a Generation Configuration

Open an existing config to see generation patterns in action:

```
configs/content/readme/readme-content.json
```

Look for the `generation` section:

```json
{
  "generation": {
    "patterns": [
      {
        "id": "readme-demo",
        "type": "demonstration",
        "template": "{{introduction}}\n\n{{features}}",
        "variables": [
          {
            "name": "introduction",
            "source": "elements.introduction.example_output"
          },
          {
            "name": "features",
            "source": "elements.features.example_output"
          }
        ]
      }
    ]
  }
}
```

**Understanding the structure:**
- **`type: "demonstration"`** - Specifies which generator to use
- **`template`** - String with `{{variable}}` placeholders
- **`variables`** - Maps each placeholder to element data
- **`source`** - Path to element data (e.g., `elements.{name}.example_output`)

---

## Step 2: Write Your First Generation Script

Create a file `generate_content.py` in your project root:

```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.demonstration import DemonstrationGenerator

# Load configuration
loader = ConfigLoader()
config = loader.load_content_config("readme-content")

# Create generator instance
generator = DemonstrationGenerator()

# Generate content
output = generator.generate(config)

# Display results
print("=" * 60)
print("GENERATED CONTENT")
print("=" * 60)
print(output)
print("\n" + "=" * 60)
print(f"Length: {len(output)} characters")
print("=" * 60)
```

**What this does:**
1. Loads the content configuration
2. Creates a DemonstrationGenerator instance
3. Calls `generate()` to produce content
4. Prints the generated output

---

## Step 3: Run Your First Generation

Execute the script:

```bash
poetry run python generate_content.py
```

**Expected output:**

```
============================================================
GENERATED CONTENT
============================================================
# Chora Compose

## Welcome to Chora Compose

A configuration-driven framework for structured Human-AI
collaborative content and artifact generation...

## How It Works

Define content configurations using JSON, specify generation
patterns, and let Chora Compose handle the execution...

============================================================
Length: 1847 characters
============================================================
```

**Success!** You've generated content from a configuration.

---

## Step 4: Create Your Own Simple Configuration

Let's build a minimal config from scratch to understand the process.

### Create Directory Structure

```bash
mkdir -p configs/content/my-greeting
```

### Create Configuration File

Create `configs/content/my-greeting/my-greeting-content.json`:

```json
{
  "type": "content",
  "id": "my-greeting-content",
  "schemaRef": {
    "uri": "file://schemas/content/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "description": "A simple greeting message",
    "version": "1.0",
    "generation_frequency": "on-demand",
    "output_format": "text"
  },
  "elements": [
    {
      "name": "salutation",
      "description": "Opening greeting",
      "format": "text",
      "example_output": "Hello, Chora Compose User!"
    },
    {
      "name": "message",
      "description": "Main message body",
      "format": "text",
      "example_output": "You're learning to use the DemonstrationGenerator. This is powerful because you can define content structure once and regenerate it anytime."
    },
    {
      "name": "closing",
      "description": "Closing statement",
      "format": "text",
      "example_output": "Happy generating!"
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "greeting-pattern",
        "type": "demonstration",
        "template": "{{salutation}}\n\n{{message}}\n\n{{closing}}",
        "variables": [
          {
            "name": "salutation",
            "source": "elements.salutation.example_output"
          },
          {
            "name": "message",
            "source": "elements.message.example_output"
          },
          {
            "name": "closing",
            "source": "elements.closing.example_output"
          }
        ]
      }
    ]
  }
}
```

---

## Step 5: Generate Your Custom Content

Create `generate_greeting.py`:

```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.demonstration import DemonstrationGenerator

# Load your custom config
loader = ConfigLoader()
config = loader.load_content_config("my-greeting-content")

# Generate content
generator = DemonstrationGenerator()
output = generator.generate(config)

# Display output
print(output)
```

Run it:

```bash
poetry run python generate_greeting.py
```

**Output:**

```
Hello, Chora Compose User!

You're learning to use the DemonstrationGenerator. This is powerful because you can define content structure once and regenerate it anytime.

Happy generating!
```

**You did it!** You created and used your own content configuration.

---

## Step 6: Understanding Variable Sources

The `source` field in variables supports multiple access patterns.

### Pattern 1: By Name (Recommended)

```json
{
  "name": "introduction",
  "source": "elements.introduction.example_output"
}
```

**Breakdown:**
- `elements` - Access the elements array
- `.introduction` - Find element with `name: "introduction"`
- `.example_output` - Extract the example_output field

### Pattern 2: By Index

```json
{
  "name": "first-element",
  "source": "elements.0.example_output"
}
```

**Breakdown:**
- `elements.0` - First element (zero-indexed)
- `.example_output` - Extract the example_output field

**Best practice:** Use name-based sources for clarity and maintainability.

---

## Step 7: Experimenting with Templates

Templates give you full control over output formatting. Try different patterns:

### Markdown Documentation

```json
{
  "template": "# {{title}}\n\n## Overview\n\n{{description}}\n\n## Installation\n\n{{install}}\n\n## Usage\n\n{{usage}}"
}
```

### Code Documentation

```json
{
  "template": "\"\"\"{{docstring}}\n\nArgs:\n    {{args}}\n\nReturns:\n    {{returns}}\n\nExample:\n    {{example}}\n\"\"\""
}
```

### List Format

```json
{
  "template": "# Tasks\n\n- {{task1}}\n- {{task2}}\n- {{task3}}\n\nTotal: 3 tasks"
}
```

### JSON Output

```json
{
  "template": "{\n  \"name\": \"{{name}}\",\n  \"version\": \"{{version}}\",\n  \"description\": \"{{description}}\"\n}"
}
```

The generator performs simple string substitution - you have complete control.

---

## Step 8: Save Generated Content to Files

Extend your script to save output:

```python
from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.demonstration import DemonstrationGenerator

# Generate content
loader = ConfigLoader()
config = loader.load_content_config("my-greeting-content")
generator = DemonstrationGenerator()
output = generator.generate(config)

# Save to file
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

output_file = output_dir / "greeting.txt"
output_file.write_text(output, encoding="utf-8")

# Confirm success
print(f"✓ Content saved to {output_file}")
print(f"✓ Size: {len(output)} characters")
```

Run and verify:

```bash
poetry run python generate_greeting.py
cat output/greeting.txt
```

---

## Step 9: Multiple Patterns (Advanced)

A single config can have multiple generation patterns:

```json
{
  "generation": {
    "patterns": [
      {
        "id": "summary",
        "type": "demonstration",
        "template": "{{title}}: {{brief}}"
      },
      {
        "id": "detailed",
        "type": "demonstration",
        "template": "# {{title}}\n\n{{description}}\n\n{{details}}"
      }
    ]
  }
}
```

The generator will use the first pattern by default, but you can select specific patterns when composing artifacts (covered in next tutorial).

---

## What You Learned

In this tutorial, you successfully:

- ✅ Understood demonstration generation principles
- ✅ Examined generation patterns in configurations
- ✅ Created and used a DemonstrationGenerator
- ✅ Built your own content configuration from scratch
- ✅ Generated and saved custom content
- ✅ Learned variable source syntax
- ✅ Experimented with different template formats
- ✅ Saved generated output to files

---

## Key Concepts Recap

### Demonstration Generation
- Uses `example_output` from elements
- Assembles content via templates
- Simple, predictable, and fast
- No AI or external dependencies needed

### Templates
- Strings with `{{variable}}` placeholders
- Full control over formatting
- Support any text format (Markdown, code, JSON, etc.)
- Can include literal text, newlines, special characters

### Variables
- Map template placeholders to element data
- Use `source` field to specify data location
- Support name-based or index-based access
- Must match placeholder names exactly (case-sensitive)

---

## Next Steps

### Continue Tutorial Series

- **[Compose Your First Artifact →](04-compose-your-first-artifact.md)** - Assemble multiple content pieces into final outputs

### Explore Further

- **[Use Demonstration Generator](../../how-to/generation/use-demonstration-generator.md)** - Advanced techniques and recipes
- **[DemonstrationGenerator API](../../reference/api/generators/demonstration.md)** - Complete API documentation
- **[Generator Strategy Pattern](../../explanation/architecture/generator-strategy-pattern.md)** - Understand the design

---

## Troubleshooting

### Variable Not Substituted

**Symptom:** Template shows `{{variable}}` literally in output

**Solutions:**
- Check template uses `{{variable}}` syntax (double curly braces)
- Verify variable name matches between template and variables array
- Ensure variable name is case-sensitive match
- Check that variable `source` points to valid element

### Element Not Found

**Error:** `KeyError` when accessing element

**Solutions:**
- Verify element name matches exactly (case-sensitive)
- Use correct syntax: `elements.{name}.example_output`
- Check element exists in config's elements array
- Try index-based access: `elements.0.example_output`

### Empty Output

**Symptom:** Generator produces empty string

**Solutions:**
- Verify elements have `example_output` fields populated
- Check generation pattern has `type: "demonstration"`
- Ensure template is not empty string
- Verify all variable sources resolve to data

### Generation Pattern Not Found

**Error:** No generation pattern found

**Solutions:**
- Verify `generation.patterns` array exists in config
- Check at least one pattern has `type: "demonstration"`
- Ensure pattern is properly formatted JSON
- Validate config against schema

### File Save Errors

**Error:** Permission denied or file not found when saving

**Solutions:**
- Ensure output directory exists or use `mkdir(exist_ok=True)`
- Check write permissions on output directory
- Use absolute paths if relative paths fail
- Verify parent directory exists before writing file

---

**Tutorial complete!** You can now generate content from configurations.

**Next:** [Compose Your First Artifact →](04-compose-your-first-artifact.md)
