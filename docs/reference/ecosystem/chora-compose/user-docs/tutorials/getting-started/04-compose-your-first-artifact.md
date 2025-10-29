# Tutorial: Compose Your First Artifact

> **Learning Goal:** Assemble a complete artifact from multiple content pieces, experiencing the full end-to-end workflow of Chora Compose.

## What You'll Build

By completing this tutorial, you'll:
- Create an artifact configuration
- Reference multiple content configs as components
- Use ArtifactComposer to assemble outputs
- Write composed artifacts to files
- Understand the complete generation workflow

## Prerequisites

- [ ] Chora Compose installed ([Installation Guide](01-installation.md))
- [ ] Python 3.12+
- [ ] Completed [Generate Your First Content Tutorial](03-generate-your-first-content.md)
- [ ] Understanding of content configurations

**Time Required:** ~20 minutes

---

## Understanding the Complete Workflow

Chora Compose's power comes from **composability** - assembling final artifacts from modular content pieces.

### The Composition Flow

```
Content Configurations      Artifact Configuration      ArtifactComposer
        ↓                           ↓                           ↓
┌──────────────┐            ┌──────────────┐           ┌──────────────┐
│ Introduction │            │  Artifact    │           │ Load artifact│
│    config    │───┐        │  config      │      ┌───→│ configuration│
└──────────────┘   │        │              │      │    └──────────────┘
                   │        │ References   │      │           ↓
┌──────────────┐   ├───────→│  multiple    │──────┤    ┌──────────────┐
│   Features   │   │        │  children    │      ├───→│  Generate    │
│    config    │───┘        │              │      │    │ each content │
└──────────────┘            └──────────────┘      │    │    piece     │
                                                  │    └──────────────┘
┌──────────────┐                                  │           ↓
│  Conclusion  │                                  │    ┌──────────────┐
│    config    │──────────────────────────────────┘    │   Compose    │
└──────────────┘                                       │ and write to │
                                                       │     file     │
                                                       └──────────────┘
```

**Key components:**
- **Content configs** - Individual sections or pieces
- **Artifact config** - Blueprint specifying what to combine
- **ArtifactComposer** - Orchestrates generation and assembly
- **Output file** - Final assembled artifact

---

## Step 1: Create Content Configurations

Let's build three content pieces: introduction, features list, and conclusion.

### Create Introduction Content

Create directory and file:
```bash
mkdir -p configs/content/intro
```

Create `configs/content/intro/intro-content.json`:

```json
{
  "type": "content",
  "id": "intro-content",
  "schemaRef": {
    "uri": "file://schemas/content/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "description": "Introduction section for artifact",
    "version": "1.0",
    "generation_frequency": "on-demand",
    "output_format": "markdown"
  },
  "elements": [
    {
      "name": "introduction",
      "description": "Opening paragraph",
      "format": "markdown",
      "example_output": "# Welcome to Chora Compose\n\nThis document was generated using Chora Compose, a configuration-driven framework for Human-AI collaborative content generation."
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "intro-pattern",
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

### Create Features Content

```bash
mkdir -p configs/content/features
```

Create `configs/content/features/features-content.json`:

```json
{
  "type": "content",
  "id": "features-content",
  "schemaRef": {
    "uri": "file://schemas/content/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "description": "Features section",
    "version": "1.0",
    "generation_frequency": "on-demand",
    "output_format": "markdown"
  },
  "elements": [
    {
      "name": "features",
      "description": "Key features list",
      "format": "markdown",
      "example_output": "## Key Features\n\n- **Configuration-Driven**: Define content structure using JSON Schema-validated configs\n- **Composable**: Assemble complex artifacts from modular content pieces\n- **Type-Safe**: Full Pydantic models with comprehensive validation\n- **Extensible**: Plugin system for custom generators and validators"
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "features-pattern",
        "type": "demonstration",
        "template": "{{features}}",
        "variables": [
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

### Create Conclusion Content

```bash
mkdir -p configs/content/conclusion
```

Create `configs/content/conclusion/conclusion-content.json`:

```json
{
  "type": "content",
  "id": "conclusion-content",
  "schemaRef": {
    "uri": "file://schemas/content/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "description": "Conclusion section",
    "version": "1.0",
    "generation_frequency": "on-demand",
    "output_format": "markdown"
  },
  "elements": [
    {
      "name": "conclusion",
      "description": "Closing statement",
      "format": "markdown",
      "example_output": "## Get Started\n\nThank you for exploring Chora Compose! This framework demonstrates composable, configuration-driven content generation.\n\nLearn more: https://github.com/liminalcommons/chora-compose"
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "conclusion-pattern",
        "type": "demonstration",
        "template": "{{conclusion}}",
        "variables": [
          {
            "name": "conclusion",
            "source": "elements.conclusion.example_output"
          }
        ]
      }
    ]
  }
}
```

---

## Step 2: Create an Artifact Configuration

Now create an artifact that combines all three content pieces.

```bash
mkdir -p configs/artifacts
```

Create `configs/artifacts/my-first-artifact.json`:

```json
{
  "type": "artifact",
  "id": "my-first-artifact",
  "schemaRef": {
    "uri": "file://schemas/artifact/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "type": "documentation",
    "version": "1.0",
    "title": "My First Chora Compose Artifact",
    "purpose": "Demonstrate end-to-end artifact composition",
    "outputs": [
      {
        "file": "output/my-first-artifact.md",
        "format": "markdown"
      }
    ],
    "compositionStrategy": "concat"
  },
  "content": {
    "children": [
      {
        "id": "intro-content",
        "path": "content/intro/intro-content.json",
        "required": true,
        "order": 1,
        "retrievalStrategy": "latest"
      },
      {
        "id": "features-content",
        "path": "content/features/features-content.json",
        "required": true,
        "order": 2,
        "retrievalStrategy": "latest"
      },
      {
        "id": "conclusion-content",
        "path": "content/conclusion/conclusion-content.json",
        "required": true,
        "order": 3,
        "retrievalStrategy": "latest"
      }
    ]
  }
}
```

**Understanding artifact config:**
- **`type: "artifact"`** - Distinguishes from content configs
- **`outputs`** - Where to write final file(s)
- **`compositionStrategy`** - How to combine pieces (`concat` = join with newlines)
- **`children`** - Array of content configs to include
- **`order`** - Sequence control (lower numbers first)
- **`required`** - Whether content must exist for composition to succeed

---

## Step 3: Compose the Artifact

Create `compose_artifact.py`:

```python
from pathlib import Path
from chora_compose.core.composer import ArtifactComposer

# Initialize the composer
composer = ArtifactComposer()

# Assemble the artifact
output_path = composer.assemble("my-first-artifact")

# Report success
print(f"✓ Artifact assembled successfully!")
print(f"✓ Output: {output_path}")
print(f"✓ Size: {output_path.stat().st_size} bytes")

# Display the generated content
content = output_path.read_text(encoding="utf-8")
print("\n" + "="*60)
print("GENERATED ARTIFACT")
print("="*60)
print(content)
print("="*60)
```

---

## Step 4: Run the Composer

Execute the composition:

```bash
poetry run python compose_artifact.py
```

**Expected output:**

```
✓ Artifact assembled successfully!
✓ Output: output/my-first-artifact.md
✓ Size: 548 bytes

============================================================
GENERATED ARTIFACT
============================================================
# Welcome to Chora Compose

This document was generated using Chora Compose, a configuration-driven
framework for Human-AI collaborative content generation.

## Key Features

- **Configuration-Driven**: Define content structure using JSON Schema-validated configs
- **Composable**: Assemble complex artifacts from modular content pieces
- **Type-Safe**: Full Pydantic models with comprehensive validation
- **Extensible**: Plugin system for custom generators and validators

## Get Started

Thank you for exploring Chora Compose! This framework demonstrates
composable, configuration-driven content generation.

Learn more: https://github.com/liminalcommons/chora-compose
============================================================
```

**Success!** You've assembled your first artifact from three content configurations.

---

## Step 5: Verify the Output File

Check that the file was written:

```bash
cat output/my-first-artifact.md
```

You should see the same assembled content. The composer wrote it to the file specified in `metadata.outputs[0].file`.

---

## Step 6: Understanding Order Control

The `order` field determines sequence. Let's experiment by changing the order.

### Swap Features and Conclusion

Edit `configs/artifacts/my-first-artifact.json`:

```json
{
  "content": {
    "children": [
      {
        "id": "intro-content",
        "path": "content/intro/intro-content.json",
        "required": true,
        "order": 1
      },
      {
        "id": "conclusion-content",
        "path": "content/conclusion/conclusion-content.json",
        "required": true,
        "order": 2
      },
      {
        "id": "features-content",
        "path": "content/features/features-content.json",
        "required": true,
        "order": 3
      }
    ]
  }
}
```

Run again:

```bash
poetry run python compose_artifact.py
```

**Result:** Conclusion now appears before features! The `order` field controls assembly sequence, regardless of position in the `children` array.

---

## Step 7: Making Content Optional

Not all content must be present. Let's make features optional.

### Mark Features as Optional

Edit `configs/artifacts/my-first-artifact.json`:

```json
{
  "id": "features-content",
  "path": "content/features/features-content.json",
  "required": false,  // Changed to optional
  "order": 2
}
```

### Temporarily Hide Features

```bash
mv configs/content/features/features-content.json configs/content/features/features-content.json.backup
```

### Run Composer

```bash
poetry run python compose_artifact.py
```

**What happens:**
- Composer tries to load features config
- File doesn't exist
- Since `required: false`, composer skips it without error
- Only intro and conclusion are assembled

**Output:**
```
✓ Artifact assembled successfully!
...
# Welcome to Chora Compose
...

## Get Started
...
```

The features section is missing, but composition succeeded!

### Restore Features

```bash
mv configs/content/features/features-content.json.backup configs/content/features/features-content.json
```

---

## Step 8: Adding More Content Dynamically

Let's add a new section to demonstrate adding content.

### Create Installation Instructions

```bash
mkdir -p configs/content/installation
```

Create `configs/content/installation/installation-content.json`:

```json
{
  "type": "content",
  "id": "installation-content",
  "schemaRef": {
    "uri": "file://schemas/content/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "description": "Installation instructions",
    "version": "1.0",
    "generation_frequency": "on-demand",
    "output_format": "markdown"
  },
  "elements": [
    {
      "name": "installation",
      "format": "markdown",
      "example_output": "## Installation\n\n```bash\n# Clone the repository\ngit clone https://github.com/liminalcommons/chora-compose.git\ncd chora-compose\n\n# Install dependencies\npoetry install\n```"
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "install-pattern",
        "type": "demonstration",
        "template": "{{installation}}",
        "variables": [
          {"name": "installation", "source": "elements.installation.example_output"}
        ]
      }
    ]
  }
}
```

### Update Artifact Config

Edit `configs/artifacts/my-first-artifact.json` to add installation between features and conclusion:

```json
{
  "content": {
    "children": [
      {
        "id": "intro-content",
        "path": "content/intro/intro-content.json",
        "required": true,
        "order": 1
      },
      {
        "id": "features-content",
        "path": "content/features/features-content.json",
        "required": true,
        "order": 2
      },
      {
        "id": "installation-content",
        "path": "content/installation/installation-content.json",
        "required": true,
        "order": 3
      },
      {
        "id": "conclusion-content",
        "path": "content/conclusion/conclusion-content.json",
        "required": true,
        "order": 4
      }
    ]
  }
}
```

### Regenerate

```bash
poetry run python compose_artifact.py
```

The artifact now includes installation instructions in the correct position!

---

## What You Learned

In this tutorial, you successfully:

- ✅ Created multiple content configurations
- ✅ Created an artifact configuration referencing content pieces
- ✅ Used ArtifactComposer to assemble an artifact
- ✅ Wrote composed content to output files
- ✅ Controlled section ordering with `order` field
- ✅ Handled optional vs required content
- ✅ Dynamically added new sections
- ✅ Regenerated artifacts after configuration changes

---

## Key Concepts Recap

### Artifact Configuration
- References multiple content configs as children
- Specifies output file location(s)
- Defines composition strategy (how to combine)
- Controls ordering and dependencies
- Distinguishes required vs optional content

### ArtifactComposer
- Loads artifact configuration
- Resolves and loads child content configs
- Generates content for each child using appropriate generator
- Composes content using specified strategy
- Writes final output to file(s)

### Composition Strategies
- **`concat`** - Join content pieces with `\n\n` separator (most common)
- **`merge`** - Intelligent merging for structured formats (future)
- **`custom`** - User-defined composition logic (future)

### Content Organization
- **`order`** field controls sequence (lower = earlier)
- **`required`** field controls error handling
- **`path`** points to content config (relative to configs/)
- **`retrievalStrategy`** determines version to use (`latest`, `pinned`, etc.)

---

## Next Steps

### Explore Advanced Topics

- **[Use Artifact Composer](../../how-to/generation/use-artifact-composer.md)** - Advanced composition patterns
- **[Composition Strategies](../../how-to/generation/composition-strategies.md)** - Different assembly methods
- **[Artifact Dependencies](../../how-to/generation/artifact-dependencies.md)** - Track content relationships
- **[Dynamic Content with Jinja2](../intermediate/01-dynamic-content-with-jinja2.md)** - Template-based generation

### Deep Dive

- **[ArtifactComposer API Reference](../../reference/api/core/artifact-composer.md)** - Complete API documentation
- **[Config-Driven Architecture](../../explanation/architecture/config-driven-architecture.md)** - Design philosophy
- **[Generator Strategy Pattern](../../explanation/architecture/generator-strategy-pattern.md)** - How generators work

---

## Troubleshooting

### Artifact Config Not Found

**Error:** `CompositionError: Failed to load artifact config 'my-first-artifact'`

**Solutions:**
- Verify file exists at `configs/artifacts/my-first-artifact.json`
- Check JSON syntax is valid (use a JSON validator)
- Ensure `schemaRef` points to correct schema version
- Verify `type: "artifact"` is set correctly

### Content Config Not Found

**Error:** `CompositionError: Content config 'intro-content' not found`

**Solutions:**
- Check `path` in child reference is correct
- Paths are relative to `configs/` directory
- Verify content config file exists at specified path
- Use `required: false` if content is optional

### Required Content Generation Failed

**Error:** `CompositionError: Failed to generate required content 'features-content'`

**Solutions:**
- Validate content config loads successfully independently
- Verify generation patterns are correctly defined
- Check element `example_output` fields are populated
- Test content generation separately to isolate issue
- Set `required: false` if failure should be tolerated

### Wrong Section Order

**Symptom:** Sections appear in unexpected sequence

**Solutions:**
- Check all `order` values in children array
- Lower numbers appear first in output
- Children without `order` field default to 0
- Ensure no duplicate `order` values (behavior undefined)

### Empty Output File

**Symptom:** File created but contains no content

**Solutions:**
- Verify at least one child content config exists
- Check content configs have valid `example_output`
- Ensure composition strategy is set (`concat` is default)
- Validate generation patterns produce non-empty output

### File Write Permission Error

**Error:** Permission denied when writing output file

**Solutions:**
- Check output directory exists (create with `mkdir -p output/`)
- Verify write permissions on output directory
- Ensure output path in config is valid
- Try absolute path instead of relative path

---

**Tutorial complete!** You now understand the complete Chora Compose workflow from content to artifact.

**Next:** [Dynamic Content with Jinja2 →](../intermediate/01-dynamic-content-with-jinja2.md)
