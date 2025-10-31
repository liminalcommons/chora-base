# How to Use Composition Strategies

> **Goal:** Understand and apply different strategies for combining content into final artifacts.

## When to Use This

You need to understand composition strategies when:
- Assembling content from multiple sources
- Deciding how to merge sections
- Building complex multi-part documents
- Creating different output formats from same content
- Customizing how content combines

## Prerequisites

- Understanding of artifact configs
- Familiarity with ArtifactComposer
- Multiple content configurations created

---

## Solution

### Quick Version

**Concatenation (currently supported):**
```json
{
  "metadata": {
    "compositionStrategy": "concat"
  }
}
```

Joins content with double newlines (`\n\n`).

### Current Strategy: Concatenation

#### How It Works

The `concat` strategy:
1. Loads all child content configs in order
2. Generates content for each
3. Joins them with `\n\n` (double newline)
4. Writes to output file

**Example:**

**Content 1:**
```
# Introduction

This is the intro.
```

**Content 2:**
```
## Features

- Feature A
- Feature B
```

**Composed Output:**
```
# Introduction

This is the intro.

## Features

- Feature A
- Feature B
```

Note the blank line between sections.

---

## Detailed Steps

### Step 1: Understand Your Content Structure

Before choosing a strategy, understand your content:

```python
# Analyze content structure
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.demonstration import DemonstrationGenerator

loader = ConfigLoader()
generator = DemonstrationGenerator()

# Generate each section independently
sections = ["intro", "body", "conclusion"]
for section_id in sections:
    config = loader.load_content_config(f"{section_id}-content")
    output = generator.generate(config)

    print(f"=== {section_id} ===")
    print(f"Length: {len(output)} chars")
    print(f"Lines: {len(output.splitlines())}")
    print(f"Starts with: {output[:50]}")
    print(f"Ends with: {output[-50:]}")
    print()
```

This helps you understand:
- Whether sections have their own spacing
- If content starts/ends with newlines
- How sections should connect

### Step 2: Configure Concatenation Strategy

**Basic config:**
```json
{
  "type": "artifact",
  "id": "my-artifact",
  "metadata": {
    "compositionStrategy": "concat",
    "outputs": [{"file": "output.md"}]
  },
  "content": {
    "children": [
      {"id": "section1", "path": "...", "order": 1},
      {"id": "section2", "path": "...", "order": 2}
    ]
  }
}
```

**Result:** `section1\n\nsection2`

### Step 3: Control Spacing with Content

Since concatenation adds `\n\n`, you can control spacing in content:

**Tight spacing (no blank line):**

Make second section start with `-\n\n`:
```json
{
  "elements": [{
    "name": "content",
    "example_output": "-\n\n## Section 2\n\nContent..."
  }]
}
```

Result: The `-\n\n` plus concat's `\n\n` = only one blank line.

**Extra spacing:**

Make content end with extra `\n`:
```json
{
  "example_output": "## Section 1\n\nContent...\n\n\n"
}
```

Result: Extra newlines before concat's `\n\n`.

---

## Common Patterns

### Pattern: Standard Document Sections

Multiple independent sections with clear breaks:

**Artifact config:**
```json
{
  "compositionStrategy": "concat",
  "content": {
    "children": [
      {"id": "title", "order": 1},
      {"id": "abstract", "order": 2},
      {"id": "introduction", "order": 3},
      {"id": "methodology", "order": 4},
      {"id": "results", "order": 5},
      {"id": "discussion", "order": 6},
      {"id": "references", "order": 7}
    ]
  }
}
```

**Works well with:** Markdown documents, reports, papers

### Pattern: Nested Sections

Hierarchical content with subsections:

**Structure:**
```
# Main Title
├─ ## Section 1
│  ├─ ### Subsection 1.1
│  └─ ### Subsection 1.2
└─ ## Section 2
   └─ ### Subsection 2.1
```

**Implementation:**
- Each major section is one content config
- Subsections are elements within that config
- Concat assembles major sections

**Artifact config:**
```json
{
  "compositionStrategy": "concat",
  "content": {
    "children": [
      {"id": "section1-with-subs", "order": 1},
      {"id": "section2-with-subs", "order": 2}
    ]
  }
}
```

### Pattern: Front Matter + Content

Documents with metadata header:

**Content 1 (frontmatter):**
```yaml
---
title: My Document
author: John Doe
date: 2025-10-10
---
```

**Content 2 (body):**
```markdown
# My Document

Content here...
```

**Composed:**
```
---
title: My Document
author: John Doe
date: 2025-10-10
---

# My Document

Content here...
```

**Works well with:** Static site generators (Hugo, Jekyll), Jupyter notebooks

### Pattern: Code + Documentation

Combine code and docs:

**Content 1 (code):**
```python
def hello(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"
```

**Content 2 (docs):**
```markdown
## Usage

```python
hello("World")  # Returns "Hello, World!"
```
```

**Composed:**
```
def hello(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"

## Usage

```python
hello("World")  # Returns "Hello, World!"
```
```

**Works well with:** Literate programming, API docs with examples

---

## Future Strategies (Planned)

### Strategy: Merge

**Concept:** Intelligent section merging

```json
{
  "compositionStrategy": "merge",
  "mergeConfig": {
    "duplicateHeaders": "keep-first",
    "blankLines": "normalize"
  }
}
```

**Use cases:**
- Combine sections with overlapping headers
- Normalize spacing across sections
- Smart handling of duplicate content

### Strategy: Overlay

**Concept:** Layer content with priority

```json
{
  "compositionStrategy": "overlay",
  "overlayConfig": {
    "baseLayer": "template",
    "overlays": ["custom-content", "overrides"]
  }
}
```

**Use cases:**
- Template-based documents with customization
- Multi-tenant content with overrides
- Theming and branding

### Strategy: Custom

**Concept:** External composition tool

```json
{
  "compositionStrategy": "custom",
  "customConfig": {
    "tool": "pandoc",
    "arguments": ["-f", "markdown", "-t", "html"]
  }
}
```

**Use cases:**
- Format conversion (MD → HTML, RST, PDF)
- Custom business logic
- Integration with external tools

---

## Working with Current Limitations

### Limitation: Only concat Supported

**Current state:** Only `concat` strategy is implemented.

**Workarounds:**

**1. Pre-process content:**
```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.demonstration import DemonstrationGenerator

def custom_compose(sections: list[str], strategy: str) -> str:
    """Custom composition before artifact assembly."""
    loader = ConfigLoader()
    generator = DemonstrationGenerator()

    contents = []
    for section_id in sections:
        config = loader.load_content_config(section_id)
        output = generator.generate(config)
        contents.append(output)

    if strategy == "tight":
        return "\n".join(contents)  # Single newline
    elif strategy == "spaced":
        return "\n\n\n".join(contents)  # Triple newline
    elif strategy == "custom":
        # Your custom logic
        return custom_merge_logic(contents)
    else:
        return "\n\n".join(contents)  # Default concat

# Use custom composition
composed = custom_compose(["intro", "body"], strategy="tight")

# Then write to file
Path("output.md").write_text(composed)
```

**2. Post-process output:**
```python
from pathlib import Path
from chora_compose.core.composer import ArtifactComposer

# Assemble with concat
composer = ArtifactComposer()
output_path = composer.assemble("my-artifact")

# Post-process the output
content = output_path.read_text()

# Custom transformations
content = content.replace("\n\n\n", "\n\n")  # Normalize spacing
content = content.replace("## ", "\n## ")     # Add space before headers

# Write back
output_path.write_text(content)
```

**3. Use intermediate content configs:**

Create a "wrapper" content config that combines others:

```json
{
  "type": "content",
  "id": "combined-custom",
  "elements": [
    {
      "name": "merged",
      "example_output": "[manually merged content]"
    }
  ]
}
```

Then reference in artifact:
```json
{
  "content": {
    "children": [
      {"id": "combined-custom", "order": 1}
    ]
  }
}
```

---

## Strategy Selection Guide

| Scenario | Best Strategy | Why |
|----------|---------------|-----|
| Standard docs (markdown, reports) | `concat` | Clear section breaks needed |
| Code files | Custom (post-process) | May need specific formatting |
| Multi-format output | Custom (external tool) | Format conversion required |
| Template-based | Future: `overlay` | Layering with overrides |
| Normalized spacing | Future: `merge` | Intelligent blank line handling |
| Simple assembly | `concat` | ✅ Built-in, works well |

---

## Testing Your Strategy

**Verify composition output:**

```python
from chora_compose.core.composer import ArtifactComposer

composer = ArtifactComposer()
output_path = composer.assemble("test-artifact")

# Read and analyze
content = output_path.read_text()

# Check structure
lines = content.splitlines()
print(f"Total lines: {len(lines)}")
print(f"Blank lines: {sum(1 for line in lines if not line.strip())}")
print(f"Non-blank lines: {sum(1 for line in lines if line.strip())}")

# Check sections present
expected_sections = ["# Title", "## Section 1", "## Section 2"]
for section in expected_sections:
    if section in content:
        print(f"✓ Found: {section}")
    else:
        print(f"✗ Missing: {section}")

# Check spacing
double_newlines = content.count("\n\n")
triple_newlines = content.count("\n\n\n")
print(f"Double newlines: {double_newlines}")
print(f"Triple newlines: {triple_newlines}")
```

---

## Troubleshooting

**Problem:** Too many blank lines in output
**Solution:**
- Check if content already has trailing newlines
- Content's trailing `\n` + concat's `\n\n` = `\n\n\n`
- Remove trailing newlines from `example_output`

**Problem:** Sections run together
**Solution:**
- Ensure `compositionStrategy: "concat"` is set
- Verify content doesn't start with `-\n\n` (removes spacing)
- Check content is being loaded correctly

**Problem:** Want different spacing between sections
**Solution:**
- Concat always uses `\n\n`
- For custom spacing, post-process the output
- Or wait for `merge` strategy (future)

**Problem:** Need format conversion
**Solution:**
- Post-process with external tools (pandoc, etc.)
- Use custom script after assembly
- Wait for `custom` strategy implementation (future)

**Problem:** Duplicate headers after composition
**Solution:**
- Currently no automatic deduplication
- Fix in content configs (remove duplicates)
- Post-process to remove duplicates
- Wait for `merge` strategy (future)

---

## See Also

- [How to: Use Artifact Composer](use-artifact-composer.md) - Basic usage
- [How to: Artifact Dependencies](artifact-dependencies.md) - Track relationships
- [Tutorial: Compose Your First Artifact](../../tutorials/getting-started/04-compose-your-first-artifact.md) - Learn basics
- [ArtifactComposer API Reference](../../reference/api/core/artifact-composer.md) - Implementation details
- [Config-Driven Architecture](../../explanation/architecture/config-driven-architecture.md) - Design philosophy
