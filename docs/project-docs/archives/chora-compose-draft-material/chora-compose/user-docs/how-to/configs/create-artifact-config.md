# How to Create an Artifact Config

> **Goal:** Create an artifact configuration that assembles content configs into a final output file.

## When to Use This

You need to create an artifact config when:
- Assembling multiple content pieces into a complete document
- Defining the final output format and location
- Specifying how to compose content (concatenation, merging, etc.)
- Setting up validation for the final artifact
- Tracking dependencies between artifacts

**Alternative Approach (v1.1.0+):** For conversational config creation with preview testing before saving, see [Create Config Conversationally](./create-config-conversationally.md). This guide covers manual JSON editing.

## Prerequisites

- At least one content config created
- Understanding of composition strategies
- Familiarity with the [artifact schema](../../../schemas/artifact/v3.1/schema.json)

---

## Solution

### Quick Version

Create `configs/artifacts/my-doc-artifact.json`:

```json
{
  "type": "artifact",
  "id": "my-doc-artifact",
  "schemaRef": {
    "uri": "file://schemas/artifact/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "type": "documentation",
    "version": "1.0",
    "title": "My Documentation",
    "purpose": "Complete documentation for my feature",
    "outputs": [
      {
        "file": "docs/MY_FEATURE.md",
        "format": "markdown"
      }
    ],
    "compositionStrategy": "concat"
  },
  "content": {
    "children": [
      {
        "id": "my-feature-content",
        "path": "configs/content/my-feature/my-feature-content.json",
        "required": true,
        "order": 1,
        "retrievalStrategy": "latest"
      }
    ]
  }
}
```

Generate the artifact:
```bash
poetry run python -c "from chora_compose.core.composer import ArtifactComposer; ArtifactComposer().assemble('my-doc-artifact')"
```

### Detailed Steps

#### 1. Create the Artifact Config File

```bash
mkdir -p configs/artifacts
touch configs/artifacts/my-doc-artifact.json
```

**Naming conventions:**
- File name is `{id}.json`
- ID pattern: `^[a-z][a-z0-9-]*$`
- Use descriptive names: `readme-artifact`, `api-docs-artifact`, `test-suite-artifact`

#### 2. Define Basic Metadata

```json
{
  "type": "artifact",
  "id": "my-doc-artifact",
  "schemaRef": {
    "uri": "file://schemas/artifact/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "type": "documentation",
    "version": "1.0",
    "title": "My Feature Documentation",
    "purpose": "Complete user-facing documentation for my-feature",
    "description": "Combines overview, installation, usage, and API reference"
  }
}
```

**Metadata fields:**
- `type`: Artifact type (documentation, test, code, configuration, etc.)
- `version`: Semantic version for this artifact
- `title`: Human-readable title
- `purpose`: Brief explanation of what this artifact is for
- `description` (optional): More detailed explanation

#### 3. Define Output Files

Specify where the final artifact should be written:

```json
{
  "metadata": {
    "outputs": [
      {
        "file": "docs/MY_FEATURE.md",
        "format": "markdown",
        "language_dialect": null,
        "encoding": "utf-8"
      }
    ]
  }
}
```

**For code outputs:**
```json
{
  "outputs": [
    {
      "file": "src/my_module/feature.py",
      "format": "code",
      "language_dialect": "python",
      "encoding": "utf-8"
    }
  ]
}
```

**For multiple outputs:**
```json
{
  "outputs": [
    {
      "file": "README.md",
      "format": "markdown"
    },
    {
      "file": "docs/API.md",
      "format": "markdown"
    }
  ]
}
```

#### 4. Specify Composition Strategy

Define how to merge content from multiple children:

```json
{
  "metadata": {
    "compositionStrategy": "concat"
  }
}
```

**Available strategies:**
- `concat`: Join content with double newlines
- `merge`: Intelligent merging (future)
- `overlay`: Layer content (future)
- `custom`: External tool-defined

#### 5. Reference Content Configs

Add content children that provide the data:

```json
{
  "content": {
    "children": [
      {
        "id": "feature-overview",
        "path": "configs/content/feature-overview/feature-overview-content.json",
        "required": true,
        "order": 1,
        "retrievalStrategy": "latest",
        "expected_source": "ai",
        "review_required": false
      },
      {
        "id": "feature-examples",
        "path": "configs/content/feature-examples/feature-examples-content.json",
        "required": true,
        "order": 2,
        "retrievalStrategy": "latest",
        "expected_source": "human",
        "review_required": true
      }
    ]
  }
}
```

**Child fields:**
- `id` (required): Reference to the content config ID
- `path` (required): Path to content config file
- `required`: If true, generation fails if content unavailable
- `order`: Determines sequence in final output
- `retrievalStrategy`: How to get content ("latest", "specific_version", etc.)
- `expected_source`: Typical source (ai, human, template, mixed, any)
- `review_required`: Whether human review is mandatory

#### 6. Add Dependencies (Optional)

Track relationships to other artifacts or systems:

```json
{
  "dependencies": [
    {
      "id": "api-reference",
      "type": "artifact",
      "locator": "api-docs-artifact",
      "relationship": "documents",
      "notes": "This documentation describes the API in api-docs-artifact"
    },
    {
      "id": "user-story-123",
      "type": "requirement",
      "locator": "US-123",
      "relationship": "implements",
      "notes": "Implements user story US-123"
    },
    {
      "id": "feature-module",
      "type": "code_module",
      "locator": "src/my_module/feature.py",
      "relationship": "documents",
      "notes": "Documents the feature module"
    }
  ]
}
```

**Dependency types:**
- `artifact`: References another artifact config
- `external_system`: Links to external tool/system
- `requirement`: Traces to requirements (stories, tickets)
- `code_module`: Links to source code

**Relationships:**
- `tests`: This artifact tests the dependency
- `implements`: This artifact implements the dependency
- `documents`: This artifact documents the dependency
- `based_on`: This artifact is based on the dependency
- `related_to`: General relationship

#### 7. Add Validation Rules (Optional)

Define checks for the final artifact:

```json
{
  "validation": {
    "rules": [
      {
        "id": "completeness-check",
        "check_type": "completeness",
        "target": "content.children",
        "severity": "error"
      },
      {
        "id": "markdown-lint",
        "check_type": "lint",
        "target": "output[0]",
        "check_config": {
          "linter": "markdownlint",
          "config_file": ".markdownlint.json"
        },
        "severity": "warning"
      },
      {
        "id": "format-check",
        "check_type": "format",
        "target": "output[0]",
        "check_config": {
          "format": "markdown"
        },
        "severity": "error"
      }
    ]
  }
}
```

#### 8. Test Your Artifact Config

Validate and generate:

```bash
# Validate config loads
poetry run python -c "
from chora_compose.core.config_loader import ConfigLoader
config = ConfigLoader().load_artifact_config('my-doc-artifact')
print(f'✓ Valid artifact: {config.id}')
print(f'✓ Output: {config.metadata.outputs[0].file}')
print(f'✓ Children: {len(config.content.children)}')
"

# Generate the artifact
poetry run python -c "
from chora_compose.core.composer import ArtifactComposer
path = ArtifactComposer().assemble('my-doc-artifact')
print(f'✓ Generated: {path}')
"
```

---

## Common Patterns

### Pattern: Multi-File Documentation Suite

```json
{
  "id": "docs-suite-artifact",
  "metadata": {
    "outputs": [
      {
        "file": "README.md",
        "format": "markdown"
      },
      {
        "file": "docs/USAGE.md",
        "format": "markdown"
      },
      {
        "file": "docs/API.md",
        "format": "markdown"
      }
    ]
  },
  "content": {
    "children": [
      {
        "id": "readme-content",
        "path": "configs/content/readme/readme-content.json",
        "order": 1
      },
      {
        "id": "usage-content",
        "path": "configs/content/usage/usage-content.json",
        "order": 2
      },
      {
        "id": "api-content",
        "path": "configs/content/api/api-content.json",
        "order": 3
      }
    ]
  }
}
```

### Pattern: Test Suite Artifact

```json
{
  "id": "test-suite-artifact",
  "metadata": {
    "type": "test",
    "outputs": [
      {
        "file": "tests/test_feature.py",
        "format": "code",
        "language_dialect": "python"
      }
    ],
    "compositionStrategy": "concat"
  },
  "content": {
    "children": [
      {
        "id": "unit-tests",
        "path": "configs/content/unit-tests/unit-tests-content.json",
        "order": 1,
        "expected_source": "ai"
      },
      {
        "id": "integration-tests",
        "path": "configs/content/integration-tests/integration-tests-content.json",
        "order": 2,
        "expected_source": "human",
        "review_required": true
      }
    ]
  },
  "dependencies": [
    {
      "id": "implementation",
      "type": "code_module",
      "locator": "src/my_module/feature.py",
      "relationship": "tests"
    }
  ]
}
```

### Pattern: Conditional Content Inclusion

```json
{
  "content": {
    "children": [
      {
        "id": "core-content",
        "path": "configs/content/core/core-content.json",
        "required": true,
        "order": 1
      },
      {
        "id": "advanced-content",
        "path": "configs/content/advanced/advanced-content.json",
        "required": false,
        "order": 2,
        "conditions": "include_advanced_topics"
      }
    ]
  }
}
```

---

## Troubleshooting

**Problem:** `FileNotFoundError: Content config not found`
**Solution:**
- Verify the `path` in each child points to an existing content config
- Use relative paths from project root
- Check that content config IDs match the files

**Problem:** `Output file already exists`
**Solution:**
- ArtifactComposer overwrites by default
- Ensure you want to regenerate, or use `output_override` parameter
- Back up important files before generation

**Problem:** Content appears in wrong order
**Solution:**
- Set explicit `order` values on each child (lower numbers first)
- Children without `order` default to 0
- Use increments of 10 (10, 20, 30) to leave room for insertions

**Problem:** Generated file is empty or incomplete
**Solution:**
- Check that content configs have `example_output` in elements
- Verify generation patterns are correctly defined
- Check that retrievalStrategy matches available content

**Problem:** Validation errors about missing children
**Solution:**
- Ensure `content.children` array has at least one child
- Check that `required: true` children are accessible
- Verify content config paths are correct

---

## See Also

- [How to Create a Content Config](create-content-config.md) - Create the content first
- [How to Use ArtifactComposer](../generation/use-artifact-composer.md) - Generate artifacts
- [Artifact Schema Reference](../../reference/schemas/artifact-schema.md) - Full schema docs
- [Composition Strategies](../../explanation/concepts/composition-strategies.md) - How content is merged
- [Content vs Artifact](../../explanation/concepts/content-vs-artifact.md) - Understand the distinction
