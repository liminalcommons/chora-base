# Explanation: Content vs. Artifacts

**Purpose**: Understanding the distinction between content and artifacts, when to use each, and how they work together in chora-compose.

**Related Tutorials**:
- [Your First Config](../../tutorials/getting-started/02-your-first-config.md)
- [Generate Your First Content](../../tutorials/getting-started/03-generate-your-first-content.md)
- [Compose Your First Artifact](../../tutorials/getting-started/04-compose-your-first-artifact.md)

**Related How-To Guides**:
- [Create Content Config](../../how-to/configs/create-content-config.md)
- [Create Artifact Config](../../how-to/configs/create-artifact-config.md)
- [Use Artifact Composer](../../how-to/generation/use-artifact-composer.md)

**Related Reference**:
- [Content Config Schema](../../../schemas/content-schema.json)
- [Artifact Config Schema](../../../schemas/artifact-schema.json)

---

## Overview

Chora-compose uses two distinct types of configurations: **Content Configs** and **Artifact Configs**. Understanding the difference is fundamental to using the framework effectively.

**Simple Analogy**:
- **Content** = Individual ingredients (flour, eggs, sugar)
- **Artifacts** = Complete dish (cake assembled from ingredients)

This separation enables composability, reusability, and clear separation of concerns.

---

## Definitions

### Content

**Content** is a **single, self-contained piece of generated output** created by one generator from one configuration.

**Characteristics**:
- ✅ Single-purpose (generates one thing)
- ✅ Standalone (can be used independently)
- ✅ Generator-specific (uses one generator: jinja2, demonstration, etc.)
- ✅ Context-driven (takes input data, produces output)

**Examples**:
- API documentation for one endpoint
- README file for a project
- Daily engineering metrics report
- Release notes for a version
- Test scenario for a feature

### Artifacts

**Artifacts** are **complex outputs assembled from multiple content pieces** using composition strategies.

**Characteristics**:
- ✅ Multi-part (combines multiple content configs)
- ✅ Compositional (assembled from smaller pieces)
- ✅ Generator-agnostic (doesn't generate directly, just composes)
- ✅ Dependency-aware (understands order and relationships)

**Examples**:
- Complete documentation site (multiple pages)
- Quarterly business report (multiple sections)
- Test suite (multiple test scenarios)
- Multi-chapter book (multiple chapters)
- Release package (changelog + notes + migration guide)

---

## Visual Comparison

```
┌─────────────────────────────────────────────────────────┐
│ CONTENT CONFIG                                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Input Data        Generator        Output              │
│  ┌──────────┐     ┌─────────┐     ┌────────────┐      │
│  │ Context  │────▶│ Jinja2  │────▶│ README.md  │      │
│  │ - name   │     │ Template│     │ (single    │      │
│  │ - version│     │         │     │  file)     │      │
│  └──────────┘     └─────────┘     └────────────┘      │
│                                                          │
│  Single-purpose: One input → One generator → One output │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ ARTIFACT CONFIG                                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Multiple Content Configs    Composition    Artifact    │
│  ┌────────────┐              ┌──────────┐ ┌──────────┐ │
│  │ README     │────┐         │          │ │ Complete │ │
│  │ (content1) │    │         │ Composer │ │ Docs     │ │
│  └────────────┘    ├────────▶│          │▶│ Site     │ │
│  ┌────────────┐    │         │ Strategy │ │ (multi-  │ │
│  │ API Docs   │────┤         │          │ │  file)   │ │
│  │ (content2) │    │         └──────────┘ └──────────┘ │
│  └────────────┘    │                                    │
│  ┌────────────┐    │                                    │
│  │ Tutorial   │────┘                                    │
│  │ (content3) │                                         │
│  └────────────┘                                         │
│                                                          │
│  Multi-part: Multiple contents → Composition → Artifact │
└─────────────────────────────────────────────────────────┘
```

---

## When to Use Each

### Use Content Config When...

✅ **You need a single, specific output**
```
Goal: Generate API documentation for /users endpoint
→ Use: Content config with Jinja2 generator
```

✅ **The output is self-contained**
```
Goal: Create README for new project
→ Use: Content config with demonstration generator
```

✅ **You want to generate one thing at a time**
```
Goal: Daily metrics report
→ Use: Content config with template
```

✅ **The generation logic is straightforward**
```
Goal: Fill template with data
→ Use: Content config (no need for composition)
```

### Use Artifact Config When...

✅ **You need to combine multiple pieces**
```
Goal: Complete documentation site (README + API + Tutorial)
→ Use: Artifact config referencing 3 content configs
```

✅ **Order matters**
```
Goal: Book with chapters in specific sequence
→ Use: Artifact config with section ordering
```

✅ **You have dependencies between parts**
```
Goal: Report where section 2 depends on section 1 data
→ Use: Artifact config with dependency tracking
```

✅ **You want to reuse content in different combinations**
```
Goal: Same content in multiple artifacts
→ Use: Artifact configs referencing shared content configs
```

---

## Configuration Structure Comparison

### Content Config Structure

```json
{
  "metadata": {
    "title": "API Documentation",
    "description": "Generate docs for REST API",
    "version": "1.0.0"
  },
  "generator": "jinja2",
  "generatorSpecific": {
    "jinja2": {
      "template": "templates/api-docs.j2",
      "inputs": {
        "endpoints": "{{endpoints}}",
        "api_version": "{{version}}"
      }
    }
  },
  "outputPath": "docs/api/v{{version}}.md"
}
```

**Key Fields**:
- `generator`: Which generator to use
- `generatorSpecific`: Parameters for that generator
- `outputPath`: Where to save (single file)

### Artifact Config Structure

```json
{
  "metadata": {
    "title": "Complete Documentation",
    "description": "Full docs site with all sections"
  },
  "sections": [
    {
      "contentConfigId": "readme-content",
      "order": 1,
      "context": {"project_name": "MyApp"}
    },
    {
      "contentConfigId": "api-docs-content",
      "order": 2,
      "context": {"version": "1.0"}
    },
    {
      "contentConfigId": "tutorial-content",
      "order": 3
    }
  ],
  "composition": {
    "strategy": "concatenate",
    "separator": "\n\n---\n\n"
  },
  "outputPath": "docs/complete-site.md"
}
```

**Key Fields**:
- `sections`: List of content configs to include
- `order`: Sequence of assembly
- `composition.strategy`: How to combine (concatenate, merge, etc.)
- `outputPath`: Where to save assembled artifact

---

## Composition Strategies

### 1. Concatenate (Simple Joining)

**Use case**: Combine text documents in sequence

```json
{
  "composition": {
    "strategy": "concatenate",
    "separator": "\n\n---\n\n"
  }
}
```

**Result**:
```
[Content 1]
---
[Content 2]
---
[Content 3]
```

### 2. Structured Assembly

**Use case**: Create complex documents with nested sections

```json
{
  "composition": {
    "strategy": "structured",
    "template": "artifact-templates/book.j2"
  }
}
```

**Result**: Sections inserted into template with proper formatting

### 3. Dependency-Aware

**Use case**: Later sections need data from earlier ones

```json
{
  "sections": [
    {
      "contentConfigId": "stats-summary",
      "order": 1,
      "outputs": ["summary_data"]
    },
    {
      "contentConfigId": "detailed-report",
      "order": 2,
      "dependencies": ["summary_data"]
    }
  ]
}
```

---

## Storage Implications

### Content Storage

**Location**: Ephemeral storage (by default)
**Retention**: 30 days auto-cleanup
**Purpose**: Temporary, can be regenerated

**Rationale**: Content is often generated on-demand and doesn't need long-term storage. The config + context can recreate it anytime.

**Example**:
```
ephemeral/
└── content/
    └── daily-report-2025-10-21.md  # Auto-deleted after 30 days
```

### Artifact Storage

**Location**: Output directory (persistent)
**Retention**: Indefinite (manual cleanup)
**Purpose**: Long-term artifacts worth keeping

**Rationale**: Artifacts represent significant assembled work. You want to keep the final product.

**Example**:
```
output/
└── artifacts/
    └── Q3-2025-business-report.pdf  # Kept indefinitely
```

### Configuration Override

Both can override default storage:

```json
{
  "storage": {
    "type": "persistent",
    "path": "output/special/my-content.md"
  }
}
```

---

## Lifecycle Differences

### Content Lifecycle

```
1. Define config (content-config.json)
2. Provide context data
3. Generate content (single execution)
4. Store in ephemeral storage
5. [30 days later] Auto-cleanup
```

**Regeneration**: Easy - just re-run with same config + context

### Artifact Lifecycle

```
1. Define artifact config (artifact-config.json)
2. Reference multiple content configs
3. Generate all content pieces
4. Assemble into artifact
5. Store in persistent output
6. Manual cleanup (if needed)
```

**Regeneration**: More complex - must regenerate all dependent content first

---

## Real-World Examples

### Example 1: Blog Post (Content)

**Scenario**: Generate a blog post

**Content Config** (`blog-post-content.json`):
```json
{
  "metadata": {"title": "Blog Post Generator"},
  "generator": "demonstration",
  "generatorSpecific": {
    "demonstration": {
      "examples": [
        {
          "input": {"title": "My Day", "body": "Today was great"},
          "output": "# My Day\n\nToday was great"
        }
      ]
    }
  },
  "outputPath": "blog/{{slug}}.md"
}
```

**Why Content?**
- Single-purpose (one post)
- Self-contained
- Simple generation

### Example 2: Book (Artifact)

**Scenario**: Assemble a book from multiple chapters

**Artifact Config** (`my-book-artifact.json`):
```json
{
  "metadata": {"title": "My Technical Book"},
  "sections": [
    {"contentConfigId": "chapter-1-intro", "order": 1},
    {"contentConfigId": "chapter-2-basics", "order": 2},
    {"contentConfigId": "chapter-3-advanced", "order": 3},
    {"contentConfigId": "appendix", "order": 4}
  ],
  "composition": {
    "strategy": "concatenate",
    "separator": "\n\n\\pagebreak\n\n"
  },
  "outputPath": "books/my-book.md"
}
```

**Why Artifact?**
- Multi-part (4 chapters)
- Order matters
- Reusable (chapters can be in other books)

### Example 3: API Documentation Suite (Artifact)

**Scenario**: Complete API docs with multiple sections

**Content Configs**:
- `api-overview-content.json` - Introduction
- `api-authentication-content.json` - Auth guide
- `api-endpoints-content.json` - Endpoint reference
- `api-examples-content.json` - Code examples

**Artifact Config** (`api-docs-artifact.json`):
```json
{
  "metadata": {"title": "Complete API Documentation"},
  "sections": [
    {"contentConfigId": "api-overview-content", "order": 1},
    {"contentConfigId": "api-authentication-content", "order": 2},
    {"contentConfigId": "api-endpoints-content", "order": 3},
    {"contentConfigId": "api-examples-content", "order": 4}
  ],
  "composition": {
    "strategy": "structured",
    "template": "artifact-templates/api-docs-site.j2"
  },
  "outputPath": "docs/api/complete.html"
}
```

**Benefits**:
- Each section can be updated independently
- Sections can be reused in other artifacts (e.g., quick start guide uses just overview + examples)
- Easy to add/remove/reorder sections

---

## Reusability Patterns

### Pattern 1: One Content, Multiple Artifacts

**Scenario**: README appears in multiple places

**Content Config**: `readme-content.json` (generates README)

**Artifact Configs**:
- `docs-site-artifact.json` - Includes README as intro
- `github-release-artifact.json` - Includes README in release notes
- `npm-package-artifact.json` - Includes README in package docs

**Benefit**: Update README once, propagates to all artifacts

### Pattern 2: Parameterized Content

**Scenario**: Similar content with different parameters

**Single Content Config**: `report-section-content.json`

**Multiple Artifacts** use it with different context:
```json
{
  "sections": [
    {
      "contentConfigId": "report-section-content",
      "order": 1,
      "context": {"section": "Sales", "metric": "revenue"}
    },
    {
      "contentConfigId": "report-section-content",
      "order": 2,
      "context": {"section": "Marketing", "metric": "leads"}
    }
  ]
}
```

**Benefit**: DRY (Don't Repeat Yourself) - one config, many uses

---

## Common Mistakes

### Mistake 1: Using Artifact for Simple Generation

❌ **Bad**:
```json
{
  "metadata": {"title": "Simple README"},
  "sections": [
    {"contentConfigId": "readme-content", "order": 1}
  ],
  "composition": {"strategy": "concatenate"}
}
```

✅ **Good**: Just use the content config directly
```bash
chora-compose generate readme-content
```

**Why**: Artifacts add unnecessary complexity for single-content outputs.

### Mistake 2: Duplicating Logic in Content Configs

❌ **Bad**: 10 nearly-identical content configs

✅ **Good**: 1 parameterized content config used in artifact with different contexts

### Mistake 3: Putting Composition Logic in Content

❌ **Bad**: Jinja2 template that imports other templates

✅ **Good**: Separate content configs composed via artifact

**Reason**: Separation of concerns - content generates, artifacts compose.

---

## Best Practices

### 1. Start with Content

Always create content configs first, test them individually, then combine into artifacts.

```
1. Create content-a.json → Test it
2. Create content-b.json → Test it
3. Create artifact.json referencing both
```

### 2. Keep Content Single-Purpose

Each content config should do **one thing well**.

**Good naming**:
- `api-endpoint-docs-content.json`
- `user-guide-intro-content.json`

**Bad naming**:
- `all-docs-content.json` (too broad)

### 3. Use Artifacts for Reusability

If you find yourself generating the same content multiple times, make it a content config and reference it from artifacts.

### 4. Version Both Separately

```
configs/
├── content/
│   └── my-content-v2.json  # Independent versioning
└── artifact/
    └── my-artifact-v3.json  # Can reference v2 content
```

---

## Summary

| Aspect | Content | Artifact |
|--------|---------|----------|
| **Purpose** | Generate single output | Compose multiple outputs |
| **Generator** | Uses one (jinja2, etc.) | Uses none (just composes) |
| **Complexity** | Simple, single-purpose | Complex, multi-part |
| **Reusability** | High (ref from artifacts) | Medium (combines contents) |
| **Storage** | Ephemeral (default) | Persistent (default) |
| **Testing** | Easy (one input → one output) | Harder (multiple dependencies) |
| **Use When** | Need one thing | Need multiple things combined |

**Golden Rule**: If it's **one thing**, use **Content**. If it's **multiple things**, use **Artifact**.

---

**Related Reading**:
- [Configuration-Driven Development](configuration-driven-development.md) - Why configs matter
- [Ephemeral Storage Design](ephemeral-storage-design.md) - Storage lifecycle
- [Composition Strategies](../../how-to/generation/composition-strategies.md) - How to compose
- [Tutorial: Compose Your First Artifact](../../tutorials/getting-started/04-compose-your-first-artifact.md) - Hands-on

---

**Document Version**: 1.0
**Last Updated**: 2025-10-21
**Next Review**: After artifact composer v2.0 release
