# How to Create a Content Config

> **Goal:** Create a new content configuration file from scratch that validates and works with the Chora Compose system.

## When to Use This

You need to create a content config when:
- Defining new text content to generate (docs, comments, etc.)
- Setting up generation patterns for AI or templates
- Specifying validation rules for content
- Building reusable content modules

**Alternative Approach (v1.1.0+):** For conversational config creation through natural language dialogue with Claude, see [Create Config Conversationally](./create-config-conversationally.md). This guide covers manual JSON editing.

## Prerequisites

- Understanding of JSON format
- Familiarity with the [content schema](../../../schemas/content/v3.1/schema.json)
- Text editor or IDE

---

## Solution

### Quick Version

Create a file `configs/content/my-feature/my-feature-content.json`:

```json
{
  "type": "content",
  "id": "my-feature-content",
  "schemaRef": {
    "uri": "file://schemas/content/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "description": "Content for my new feature",
    "version": "1.0",
    "generation_frequency": "on-demand",
    "output_format": "markdown"
  },
  "elements": [
    {
      "name": "introduction",
      "description": "Opening section",
      "format": "markdown",
      "example_output": "# My Feature\n\nThis is the introduction."
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "demo-pattern",
        "type": "demonstration",
        "template": "{{introduction}}",
        "variables": [
          {
            "name": "introduction",
            "source": "elements.introduction.example_output"
          }
        ]
      }
    ]
  }
}
```

Validate it:
```bash
poetry run python -c "from chora_compose.core.config_loader import ConfigLoader; ConfigLoader().load_content_config('my-feature-content')"
```

### Detailed Steps

#### 1. Create Directory Structure

```bash
mkdir -p configs/content/my-feature
cd configs/content/my-feature
touch my-feature-content.json
```

**Naming conventions:**
- Directory name matches ID (kebab-case)
- File name is `{id}.json`
- ID pattern: `^[a-z][a-z0-9-]*$` (lowercase, hyphens, starts with letter)

#### 2. Add Required Top-Level Fields

Start with the minimum required structure:

```json
{
  "type": "content",
  "id": "my-feature-content",
  "schemaRef": {
    "uri": "file://schemas/content/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "description": "Brief description of this content",
    "version": "1.0",
    "generation_frequency": "on-demand",
    "output_format": "markdown"
  },
  "elements": []
}
```

**Required fields:**
- `type`: Always `"content"` for content configs
- `id`: Unique identifier, kebab-case
- `schemaRef`: Points to the schema version
- `metadata.description`: What this content is for
- `metadata.version`: Semantic version string
- `elements`: Array of content elements (min 1)

#### 3. Define Content Elements

Add elements that represent the content pieces to generate:

```json
{
  "elements": [
    {
      "name": "introduction",
      "description": "Opening paragraph introducing the feature",
      "format": "markdown",
      "prompt_guidance": "Write a friendly introduction explaining what this feature does",
      "example_output": "# My Feature\n\nThis feature helps you accomplish X by doing Y.",
      "generation_source": "ai",
      "review_status": "pending"
    },
    {
      "name": "usage-example",
      "description": "Code example showing usage",
      "format": "python",
      "example_output": "from my_module import MyFeature\n\nfeature = MyFeature()\nresult = feature.do_something()",
      "generation_source": "human",
      "review_status": "approved"
    }
  ]
}
```

**Element fields:**
- `name` (required): Kebab-case identifier
- `format` (required): Content format (markdown, python, json, etc.)
- `description`: What this element contains
- `prompt_guidance`: Instructions for AI generation
- `example_output`: Sample or actual content
- `generation_source`: "ai", "human", "template", or "mixed"
- `review_status`: "pending", "approved", or "needs_revision"

#### 4. Add Generation Patterns

Define how to assemble elements into final output:

```json
{
  "generation": {
    "patterns": [
      {
        "id": "main-content",
        "type": "demonstration",
        "template": "{{introduction}}\n\n## Usage\n\n```python\n{{usage-example}}\n```",
        "variables": [
          {
            "name": "introduction",
            "source": "elements.introduction.example_output"
          },
          {
            "name": "usage-example",
            "source": "elements.usage-example.example_output"
          }
        ]
      }
    ]
  }
}
```

**Pattern types:**
- `demonstration`: Uses example_output from elements
- `template_fill`: Uses Jinja2 templates (future)
- `code_generation`: AI-powered code generation (future)
- `custom`: External tool-defined

#### 5. Add Validation Rules (Optional)

Define content-level checks:

```json
{
  "validation": {
    "rules": [
      {
        "id": "introduction-present",
        "check_type": "presence",
        "target": "elements.introduction",
        "severity": "error"
      },
      {
        "id": "markdown-format",
        "check_type": "format",
        "target": "generated_output",
        "check_config": {
          "format": "markdown"
        },
        "severity": "warning"
      }
    ]
  }
}
```

**Check types:**
- `presence`: Element exists and has content
- `format`: Output matches expected format
- `lint`: Run external linter
- `syntax`: Syntax validation for code
- `custom`: External validation tool

#### 6. Add Instructions for Generation (Optional)

Provide guidance for AI or human generators:

```json
{
  "instructions": {
    "global": "This content should be clear, concise, and follow Python documentation standards.",
    "system_prompt": "You are a technical writer creating documentation for a Python library.",
    "user_prompt": "Generate documentation for {{feature_name}} that explains its purpose and usage."
  }
}
```

#### 7. Validate Your Config

Test that it loads successfully:

```bash
# Quick validation
poetry run python -c "from chora_compose.core.config_loader import ConfigLoader; print('Valid!' if ConfigLoader().load_content_config('my-feature-content') else 'Invalid')"

# Detailed validation script
poetry run python -c "
from chora_compose.core.config_loader import ConfigLoader
config = ConfigLoader().load_content_config('my-feature-content')
print(f'✓ Loaded: {config.id}')
print(f'✓ Elements: {len(config.elements)}')
print(f'✓ Patterns: {len(config.generation.patterns if config.generation else 0)}')
"
```

---

## Common Patterns

### Pattern: Multi-Section Documentation

```json
{
  "elements": [
    {"name": "overview", "format": "markdown", ...},
    {"name": "installation", "format": "markdown", ...},
    {"name": "usage", "format": "markdown", ...},
    {"name": "api-reference", "format": "markdown", ...}
  ],
  "generation": {
    "patterns": [{
      "id": "full-doc",
      "type": "demonstration",
      "template": "{{overview}}\n\n## Installation\n\n{{installation}}\n\n## Usage\n\n{{usage}}\n\n## API Reference\n\n{{api-reference}}",
      "variables": [...]
    }]
  }
}
```

### Pattern: Code with Tests

```json
{
  "elements": [
    {
      "name": "implementation",
      "format": "python",
      "description": "Main function implementation"
    },
    {
      "name": "unit-tests",
      "format": "python",
      "description": "Test cases for the function"
    }
  ]
}
```

### Pattern: Child Configs for Complex Content

```json
{
  "id": "main-feature-content",
  "elements": [...],
  "children": [
    {
      "id": "feature-examples",
      "path": "configs/content/feature-examples/feature-examples-content.json",
      "required": true,
      "order": 2
    },
    {
      "id": "feature-api",
      "path": "configs/content/feature-api/feature-api-content.json",
      "required": true,
      "order": 3
    }
  ]
}
```

---

## Troubleshooting

**Problem:** `ValidationError: 'id' does not match pattern`
**Solution:** IDs must be lowercase kebab-case starting with a letter: `my-feature-content`, not `MyFeature` or `my_feature`

**Problem:** `ValidationError: 'elements' must contain at least 1 item`
**Solution:** Add at least one element to the `elements` array

**Problem:** `ValidationError: Additional properties are not allowed`
**Solution:** You've added a field not in the schema. Check [schemas/content/v3.1/schema.json](../../../schemas/content/v3.1/schema.json) for allowed fields

**Problem:** Config loads but generation fails
**Solution:** Check that:
- Variable names in template match variable definitions
- Variable sources point to valid element names
- Element names use kebab-case consistently

**Problem:** Cannot reference element by name in variables
**Solution:** Use the full path syntax: `elements.{name}.example_output`, e.g., `elements.introduction.example_output`

---

## See Also

- [Tutorial: Your First Config](../../tutorials/getting-started/02-your-first-config.md) - Learn the basics
- [How to Create an Artifact Config](create-artifact-config.md) - Assemble content into artifacts
- [Content Schema Reference](../../reference/schemas/content-schema.md) - Full schema docs
- [Content vs Artifact Configs](../../explanation/concepts/content-vs-artifact.md) - Understand the distinction
