# Explanation: Separate Config Types Design

**Diataxis Quadrant**: Explanation
**Purpose**: Understand why chora-compose uses separate Content and Artifact config types

---

## Overview

chora-compose uses **two distinct configuration types**:

1. **Content Configs** - Single-output generation (one config → one file)
2. **Artifact Configs** - Multi-part composition (multiple content configs → structured artifact)

This document explains **why** this separation exists, **what** benefits it provides, and **why** a unified config type was rejected.

---

## The Problem: One Config to Rule Them All?

### Two Different Use Cases

**Use Case 1: Generate a single document**
```
Input: README template + project data
Output: README.md
```

**Use Case 2: Compose multi-part documentation**
```
Input: Multiple content configs (README, API docs, guides, changelog)
Output: Complete documentation artifact (combined structure)
```

**Question**: Should these use the same config format?

---

## The Solution: Separation of Concerns

### Content Config (Single Output)

**Purpose**: Generate **one piece of content** using **one generator**

**Structure**:
```json
{
  "type": "content",
  "metadata": {
    "id": "readme-intro",
    "title": "README Introduction"
  },
  "generation": {
    "generator": "jinja2",
    "template": "templates/readme-intro.j2"
  },
  "context": {
    "project_name": "chora-compose",
    "version": "1.4.0"
  }
}
```

**Characteristics**:
- ✅ Single generator
- ✅ Single output
- ✅ Self-contained
- ✅ Reusable across artifacts

### Artifact Config (Multi-Part Composition)

**Purpose**: Compose **multiple content parts** into **structured artifact**

**Structure**:
```json
{
  "type": "artifact",
  "metadata": {
    "id": "project-docs",
    "title": "Complete Project Documentation"
  },
  "parts": [
    {
      "content_id": "readme-intro",
      "order": 1,
      "section": "overview"
    },
    {
      "content_id": "api-reference",
      "order": 2,
      "section": "reference"
    }
  ],
  "assembly": {
    "strategy": "sequential",
    "output_format": "directory"
  }
}
```

**Characteristics**:
- ✅ Multiple content references
- ✅ Composition logic
- ✅ Assembly strategy
- ✅ Higher-level abstraction

---

## Why Separate? (Key Reasons)

### Reason 1: Different Concerns

**Content Configs concern**: "How do I generate THIS piece of content?"
- Generator selection
- Template/prompt specification
- Context data
- Output format

**Artifact Configs concern**: "How do I combine THESE pieces?"
- Which content configs to include
- How to order them
- How to structure the output
- Assembly strategy

**Analogy**:
- **Content Config** = Recipe for one dish (chocolate cake)
- **Artifact Config** = Menu for a meal (appetizer + main + dessert)

### Reason 2: Cognitive Load Reduction

**Unified config example** (what we rejected):
```json
{
  "type": "unified",
  "metadata": {...},

  // Content generation fields (for single output)
  "generation": {...},
  "template": "...",

  // OR artifact composition fields (mutually exclusive)
  "parts": [...],
  "assembly": {...},

  // User must understand both, even when only using one
}
```

**Problems**:
- ❌ Confusing: Which fields apply when?
- ❌ Complex validation: Mutually exclusive fields
- ❌ Cognitive overload: Learn everything upfront

**Separate configs**:
```json
// Content: Only content fields
{
  "type": "content",
  "generation": {...}  // Clear purpose
}

// Artifact: Only artifact fields
{
  "type": "artifact",
  "parts": [...]  // Clear purpose
}
```

**Benefits**:
- ✅ Clear purpose at a glance
- ✅ Learn one concept at a time
- ✅ Simpler validation (no mutual exclusivity)

### Reason 3: Different Schemas

**Content Config Schema**:
- 150 lines
- 20 properties
- 3 required fields
- Focus: Generation parameters

**Artifact Config Schema**:
- 120 lines
- 15 properties
- 4 required fields
- Focus: Composition parameters

**Unified Config Schema** (hypothetical):
- 250+ lines
- 35 properties
- Complex conditional requirements ("if type=content, then..., else if type=artifact, then...")
- Harder to maintain

**Verdict**: Separate schemas are simpler and easier to understand.

### Reason 4: Composition Patterns

**Content configs are reusable building blocks**:

```
Content Configs (reusable):
  ├─ readme-intro.json
  ├─ api-reference.json
  ├─ changelog.json
  └─ contributing-guide.json

Used in multiple artifacts:
  ├─ Artifact 1 (project-docs): readme-intro + api-reference + changelog
  ├─ Artifact 2 (developer-docs): api-reference + contributing-guide
  └─ Artifact 3 (release-notes): readme-intro + changelog
```

**Key insight**: Content configs are **building blocks**, artifacts are **compositions**.

**Analogy**:
- **Content Configs** = LEGO bricks
- **Artifact Configs** = LEGO instruction manuals (how to combine bricks)

**With unified configs**, this pattern would be unclear (is this a brick or an instruction manual?).

---

## Rejected Alternative: Single Config Type

### Approach: Discriminated Union

**Idea**: Use a single config type with a discriminator field

```json
{
  "configType": "content",  // Discriminator

  // Content-specific fields (only when configType=content)
  "generation": {...},

  // Artifact-specific fields (only when configType=artifact)
  "parts": [...]
}
```

### Why We Rejected It

#### Problem 1: Validation Complexity

**JSON Schema with discriminator**:
```json
{
  "oneOf": [
    {
      "if": {"properties": {"configType": {"const": "content"}}},
      "then": {
        "required": ["generation"],
        "not": {"required": ["parts"]}
      }
    },
    {
      "if": {"properties": {"configType": {"const": "artifact"}}},
      "then": {
        "required": ["parts"],
        "not": {"required": ["generation"]}
      }
    }
  ]
}
```

**Complexity**: 3x more complex than separate schemas.

**Error messages**: Confusing ("Required field 'generation' missing OR required field 'parts' missing").

#### Problem 2: IDE Support

**VS Code autocomplete** with unified config:
```json
{
  "configType": "content",
  "|  <-- Suggests ALL fields (content + artifact), user must know which apply
}
```

**VS Code autocomplete** with separate configs:
```json
// File: my-content.json
{
  "type": "content",
  "|  <-- Suggests ONLY content fields
}

// File: my-artifact.json
{
  "type": "artifact",
  "|  <-- Suggests ONLY artifact fields
}
```

**Verdict**: Separate configs provide better IDE experience.

#### Problem 3: File Organization

**With unified configs**:
```
configs/
  ├─ readme.json (content)
  ├─ api-docs.json (content)
  ├─ project-docs.json (artifact)
  └─ ...

  // Can't tell at a glance which is which
```

**With separate configs**:
```
configs/
  ├─ content/
  │   ├─ readme.json
  │   └─ api-docs.json
  ├─ artifact/
  │   └─ project-docs.json

  // Clear distinction by directory
```

**Verdict**: Separate directories improve discoverability.

#### Problem 4: API Design

**With unified configs**:
```python
# Load any config (user must check type)
config = loader.load_config("my-config")
if config.config_type == "content":
    # Handle content
elif config.config_type == "artifact":
    # Handle artifact
```

**With separate configs**:
```python
# Type-safe, clear intent
content_config = loader.load_content_config("my-content")
artifact_config = loader.load_artifact_config("my-artifact")

# No runtime type checking needed
```

**Verdict**: Separate types provide better API and type safety.

---

## Benefits of Separation

### 1. Progressive Disclosure

**Learning path**:

**Week 1**: Learn Content Configs
- Generate your first content
- Understand generators
- Work with templates

**Week 2**: Learn Artifact Configs
- Compose multiple contents
- Understand assembly strategies
- Build complex artifacts

**Alternative** (unified): Learn everything at once (overwhelming).

### 2. Clear Mental Model

**Mental model with separation**:

```
Content Config = Single Building Block
  ↓
Artifact Config = Combination of Blocks
  ↓
Final Output = Assembled Artifact
```

**Mental model with unified config**: Confusing (sometimes single output, sometimes multi-part?).

### 3. Type Safety

**Python types with separation**:
```python
def generate_content(config: ContentConfig) -> str:
    """Generate single content piece."""
    # Type checker knows: config has 'generation' field
    return generator.generate(config.generation)

def assemble_artifact(config: ArtifactConfig) -> Artifact:
    """Assemble multi-part artifact."""
    # Type checker knows: config has 'parts' field
    return assembler.assemble(config.parts)
```

**Python types with unified**:
```python
def process_config(config: UnifiedConfig) -> str | Artifact:
    """Process any config type."""
    if config.config_type == "content":
        # Type checker can't verify 'generation' exists
        return generator.generate(config.generation)  # ⚠️ Type error
    else:
        # Type checker can't verify 'parts' exists
        return assembler.assemble(config.parts)  # ⚠️ Type error
```

**Verdict**: Separate types enable static type checking.

### 4. Validation Clarity

**Content Config validation**:
```python
@field_validator("generation")
@classmethod
def validate_generation(cls, v):
    """Ensure generator config matches generator type."""
    # Clear: This validator ONLY runs for content configs
    if v.generator == "jinja2" and not v.jinja2_config:
        raise ValueError("jinja2 requires jinja2_config")
    return v
```

**Artifact Config validation**:
```python
@field_validator("parts")
@classmethod
def validate_parts(cls, v):
    """Ensure all referenced content configs exist."""
    # Clear: This validator ONLY runs for artifact configs
    for part in v:
        if not content_exists(part.content_id):
            raise ValueError(f"Content '{part.content_id}' not found")
    return v
```

**Unified Config validation**:
```python
@field_validator("generation")
@classmethod
def validate_generation(cls, v, values):
    """Validate generation field (if applicable)."""
    # Confusing: Must check if this field even applies
    if values.get("config_type") == "content":
        # Validation logic here
        pass
    # Otherwise, ignore this field
    return v
```

**Verdict**: Separate validators are clearer and simpler.

---

## Real-World Scenarios

### Scenario 1: Generate Single README

**Use Case**: Generate project README from template

**Config Type**: Content Config

**Why Content?**
- Single output (README.md)
- One generator (jinja2)
- Self-contained

**Config**:
```json
{
  "type": "content",
  "metadata": {
    "id": "readme",
    "title": "Project README"
  },
  "generation": {
    "generator": "jinja2",
    "template": "templates/readme.j2",
    "context": {
      "project_name": "chora-compose",
      "version": "1.4.0",
      "description": "Configuration-driven content generation"
    }
  }
}
```

**Result**: `output/README.md`

---

### Scenario 2: Compose Complete Documentation

**Use Case**: Generate full project documentation (README + API docs + guides + changelog)

**Config Type**: Artifact Config

**Why Artifact?**
- Multiple outputs (4 documents)
- Composition logic (order, structure)
- References existing content configs

**Config**:
```json
{
  "type": "artifact",
  "metadata": {
    "id": "project-docs",
    "title": "Complete Project Documentation"
  },
  "parts": [
    {"content_id": "readme", "order": 1, "section": "overview"},
    {"content_id": "api-reference", "order": 2, "section": "reference"},
    {"content_id": "user-guide", "order": 3, "section": "guides"},
    {"content_id": "changelog", "order": 4, "section": "history"}
  ],
  "assembly": {
    "strategy": "directory",
    "output_path": "docs/"
  }
}
```

**Result**: `docs/` directory with 4 files

---

### Scenario 3: Reusable Content Across Artifacts

**Use Case**: Use same API reference in multiple artifacts

**Content Config** (reusable):
```json
// configs/content/api-reference.json
{
  "type": "content",
  "metadata": {"id": "api-reference", "title": "API Reference"},
  "generation": {...}
}
```

**Artifact Configs** (different compositions):

**Artifact 1** (Developer Docs):
```json
{
  "type": "artifact",
  "metadata": {"id": "dev-docs"},
  "parts": [
    {"content_id": "api-reference"},
    {"content_id": "contributing-guide"},
    {"content_id": "architecture-guide"}
  ]
}
```

**Artifact 2** (Public Docs):
```json
{
  "type": "artifact",
  "metadata": {"id": "public-docs"},
  "parts": [
    {"content_id": "readme"},
    {"content_id": "api-reference"},
    {"content_id": "quick-start"}
  ]
}
```

**Key insight**: `api-reference` content config is reused in both artifacts (DRY principle).

**With unified configs**: Less clear which configs are reusable building blocks.

---

## Migration Between Types

### When to Promote Content → Artifact

**Scenario**: Started with single content config, now need multi-part composition

**Before** (single content):
```json
// configs/content/documentation.json
{
  "type": "content",
  "generation": {
    "generator": "jinja2",
    "template": "all-docs.j2"  // One big template
  }
}
```

**After** (split into artifact):

**Step 1**: Split into multiple content configs:
```json
// configs/content/readme.json
{"type": "content", "generation": {...}}

// configs/content/api-docs.json
{"type": "content", "generation": {...}}

// configs/content/guides.json
{"type": "content", "generation": {...}}
```

**Step 2**: Create artifact config:
```json
// configs/artifact/documentation.json
{
  "type": "artifact",
  "parts": [
    {"content_id": "readme"},
    {"content_id": "api-docs"},
    {"content_id": "guides"}
  ]
}
```

**Benefits**:
- Each content config is focused (single responsibility)
- Easier to maintain and update
- Reusable across artifacts

### When to Demote Artifact → Content

**Scenario**: Artifact has only one part (over-engineered)

**Before** (artifact):
```json
// configs/artifact/readme.json
{
  "type": "artifact",
  "parts": [
    {"content_id": "readme-content"}  // Only one part!
  ]
}
```

**After** (content):
```json
// configs/content/readme.json
{
  "type": "content",
  "generation": {...}  // Simpler!
}
```

**Benefit**: Reduced complexity when composition isn't needed.

---

## Design Patterns

### Pattern 1: Atomic Content Configs

**Principle**: Each content config should generate ONE coherent piece of content.

**Good** (atomic):
```
configs/content/
  ├─ readme-intro.json       (Introduction section)
  ├─ readme-installation.json (Installation section)
  └─ readme-usage.json       (Usage section)
```

**Bad** (monolithic):
```
configs/content/
  └─ readme-all-sections.json (All sections in one massive template)
```

**Why atomic?** Reusable, easier to maintain, composable.

### Pattern 2: Hierarchical Artifacts

**Principle**: Artifacts can reference other artifacts (nested composition).

**Example**:
```json
// Artifact 1: API Documentation
{
  "type": "artifact",
  "parts": [
    {"content_id": "api-overview"},
    {"content_id": "api-endpoints"},
    {"content_id": "api-auth"}
  ]
}

// Artifact 2: Complete Docs (includes Artifact 1)
{
  "type": "artifact",
  "parts": [
    {"content_id": "readme"},
    {"artifact_id": "api-documentation"},  // Reference to Artifact 1
    {"content_id": "changelog"}
  ]
}
```

**Note**: Currently not implemented, but possible future enhancement.

### Pattern 3: Content Config Naming Convention

**Convention**:
- Content configs: `{topic}-{section}.json`
- Artifact configs: `{artifact-name}.json`

**Examples**:
- Content: `readme-intro.json`, `api-endpoints.json`, `user-guide-basics.json`
- Artifact: `project-docs.json`, `developer-handbook.json`

**Benefit**: Clear distinction by filename.

---

## Comparison with Other Tools

### Make/Zapier (No Separation)

**Approach**: Workflows can be simple or complex (no distinction)

**Problem**: Hard to reuse workflow components

### n8n (Workflow Composition)

**Approach**: Nodes (atomic) + Workflows (composition)

**Similar to chora-compose**:
- Nodes ≈ Content Configs (atomic actions)
- Workflows ≈ Artifact Configs (composition)

**Difference**: n8n separates by UI design, we separate by config type.

### Terraform (Resource vs Module)

**Approach**: Resources (atomic) + Modules (composition)

**Very similar to chora-compose**:
- Resources ≈ Content Configs
- Modules ≈ Artifact Configs

**Key insight**: Separation of atomic vs composite is a proven pattern.

---

## Guidelines for Users

### When to Use Content Config

✅ **Use Content Config when**:
- Generating a single file
- Using one generator
- Output is self-contained
- Want to reuse across artifacts

**Examples**:
- README sections
- API documentation pages
- Email templates
- Configuration files

### When to Use Artifact Config

✅ **Use Artifact Config when**:
- Combining multiple content pieces
- Need specific ordering/structure
- Building a complex deliverable
- Want to compose reusable parts

**Examples**:
- Complete project documentation
- Multi-page websites
- Release packages
- Documentation websites

### Decision Tree

```
START: What are you generating?

├─ Single output?
│  └─ YES → Use Content Config
│     └─ Example: One README, one API doc, one email
│
└─ Multiple outputs?
   └─ YES → Use Artifact Config
      └─ Example: Full docs site, complete package, documentation suite
```

---

## Conclusion

**Separate config types** (Content vs Artifact) provide:

✅ **Clear mental model** - Building blocks vs compositions
✅ **Cognitive load reduction** - Learn one at a time
✅ **Type safety** - Static type checking in Python
✅ **Simpler validation** - No conditional logic
✅ **Better IDE support** - Context-specific autocomplete
✅ **Reusability** - Content configs as building blocks
✅ **Progressive disclosure** - Start simple, grow complex

**Trade-off**: Two schemas to maintain vs one unified schema.

**Verdict**: Benefits far outweigh the maintenance cost.

**Key principle**: **Atomic content configs** + **Compositional artifact configs** = Flexible, reusable content generation system.

---

## Related Documentation

**Diataxis References**:
- [Tutorial: Understanding Content Configs](../../tutorials/getting-started/03-content-configs.md) - Learn content configs
- [Tutorial: Understanding Artifact Configs](../../tutorials/getting-started/04-artifact-configs.md) - Learn artifact configs
- [How-To: Create Content Configs](../../how-to/configs/create-content-configs.md) - Practical guide
- [How-To: Create Artifact Configs](../../how-to/configs/create-artifact-configs.md) - Practical guide

**Conceptual Relationships**:
- [Explanation: Content vs Artifacts](../concepts/content-vs-artifacts.md) - Conceptual distinction
- [Explanation: Configuration-Driven Development](../concepts/configuration-driven-development.md) - Why configs?
- [Explanation: JSON Schema Validation](json-schema-validation.md) - How validation works

**Reference**:
- [Content Config Schema](../../reference/schemas/content-schema.md) - Schema documentation
- [Artifact Config Schema](../../reference/schemas/artifact-schema.md) - Schema documentation

---

**Document Version**: 1.0
**Last Updated**: 2025-10-21
**Author**: Generated via chora-compose documentation sprint
