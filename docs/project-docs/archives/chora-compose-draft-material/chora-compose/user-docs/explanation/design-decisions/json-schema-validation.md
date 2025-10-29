# Explanation: JSON Schema Validation Design

**Diataxis Quadrant**: Explanation
**Purpose**: Understand why chora-compose uses JSON Schema + Pydantic for configuration validation

---

## Overview

chora-compose employs a **two-layer validation approach** for configuration files:

1. **Layer 1: JSON Schema** (structure and format validation)
2. **Layer 2: Pydantic** (business logic and type safety)

This document explains **why** this design was chosen, **what** benefits it provides, and **how** it compares to alternative approaches.

---

## The Problem: Validating Configuration Files

### Requirements

chora-compose configurations are JSON files that define content generation and artifact composition. These configs must be:

✅ **Structurally valid**: Correct JSON syntax, required fields present
✅ **Type-safe**: Fields have correct types (string, number, boolean, etc.)
✅ **Semantically correct**: Business rules enforced (e.g., generator exists)
✅ **User-friendly**: Clear error messages when validation fails
✅ **IDE-supported**: Autocompletion and validation in editors
✅ **Version-aware**: Support multiple schema versions

### The Challenge

**No single validation approach satisfies all requirements**:

| Approach | Structural | Type-Safe | IDE Support | Business Rules | Error Messages |
|----------|-----------|-----------|-------------|----------------|----------------|
| **JSON only** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Pydantic only** | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| **JSON Schema only** | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |
| **JSON Schema + Pydantic** | ✅ | ✅ | ✅ | ✅ | ✅ |

**Solution**: Use **both** JSON Schema and Pydantic, each for what it does best.

---

## The Solution: Two-Layer Validation

### Layer 1: JSON Schema (Structure & Format)

**Purpose**: Validate structure, data types, and format using standardized JSON Schema Draft 2020-12

**What it validates**:
- Required fields present
- Correct data types (string, number, array, object)
- String formats (email, uri, date-time)
- Array constraints (minItems, maxItems, uniqueItems)
- Enum values (allowed options)
- Schema compliance (refs, definitions)

**Example** (content config schema):
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["metadata", "generation"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["id", "title"],
      "properties": {
        "id": {"type": "string", "minLength": 1},
        "title": {"type": "string", "minLength": 1},
        "version": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"}
      }
    },
    "generation": {
      "type": "object",
      "required": ["generator"],
      "properties": {
        "generator": {
          "type": "string",
          "enum": ["jinja2", "template_fill", "code_generation", "demonstration"]
        }
      }
    }
  }
}
```

**Benefits**:
- ✅ **IDE support**: VS Code, IntelliJ, etc. provide autocompletion
- ✅ **Standardized**: JSON Schema is an industry standard (IETF draft)
- ✅ **Tooling**: Many validators, generators, documentation tools
- ✅ **Version tracking**: Schema versions explicitly declared

### Layer 2: Pydantic (Business Logic & Type Safety)

**Purpose**: Validate business rules, relationships, and provide type-safe Python objects

**What it validates**:
- Cross-field validation (e.g., generator-specific config matches generator type)
- Complex business rules (e.g., artifact parts reference existing content configs)
- Type coercion (convert strings to Path, datetime, etc.)
- Default values
- Computed fields

**Example** (Pydantic model):
```python
from pydantic import BaseModel, Field, field_validator

class ContentConfig(BaseModel):
    """Content configuration with business logic validation."""

    metadata: MetadataConfig
    generation: GenerationConfig

    @field_validator("generation")
    @classmethod
    def validate_generator_config(cls, v: GenerationConfig) -> GenerationConfig:
        """Ensure generator-specific config matches generator type."""
        if v.generator == "jinja2" and not v.jinja2_config:
            raise ValueError("jinja2 generator requires jinja2_config")
        return v

    @field_validator("metadata")
    @classmethod
    def validate_version_format(cls, v: MetadataConfig) -> MetadataConfig:
        """Ensure version follows semver."""
        if v.version and not re.match(r"^\d+\.\d+\.\d+$", v.version):
            raise ValueError("Version must be semver (e.g., '1.2.3')")
        return v
```

**Benefits**:
- ✅ **Type safety**: Python code gets typed objects (not dicts)
- ✅ **Business rules**: Complex validation logic in Python
- ✅ **Auto-completion**: IDEs provide Python autocomplete
- ✅ **Defaults**: Automatic default value assignment

---

## Why Both Layers?

### Complementary Strengths

**JSON Schema is better at**:
- ✅ Standard format validation (email, uri, regex patterns)
- ✅ IDE integration (VS Code JSON validation)
- ✅ Documentation generation
- ✅ Cross-language compatibility

**Pydantic is better at**:
- ✅ Complex business logic
- ✅ Cross-field validation
- ✅ Python type safety
- ✅ Default value handling

### The Validation Flow

```
┌─────────────────────────────────────────────────────────┐
│ USER EDITS CONFIG                                        │
│  File: configs/content/my-config.json                   │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ LAYER 1: JSON SCHEMA VALIDATION                         │
│  - Check required fields                                │
│  - Validate types (string, number, array)               │
│  - Check enum values                                    │
│  - Validate formats (email, uri)                        │
│  Library: jsonschema (Draft 2020-12)                    │
└─────────────────┬───────────────────────────────────────┘
                  │
                  │ ✅ Pass
                  ▼
┌─────────────────────────────────────────────────────────┐
│ LAYER 2: PYDANTIC VALIDATION                            │
│  - Cross-field validation                               │
│  - Business rules (generator config matches generator)  │
│  - Type coercion (str → Path, datetime)                 │
│  - Default values                                       │
│  Library: Pydantic v2                                   │
└─────────────────┬───────────────────────────────────────┘
                  │
                  │ ✅ Pass
                  ▼
┌─────────────────────────────────────────────────────────┐
│ VALIDATED CONFIG OBJECT                                 │
│  Type: ContentConfig (Pydantic model)                   │
│  Ready for use in generation                            │
└─────────────────────────────────────────────────────────┘
```

**Fail-fast behavior**: If Layer 1 fails, Layer 2 is never reached (saves time).

---

## Benefits of Two-Layer Validation

### 1. Better Error Messages

**Single-layer approach** (Pydantic only):
```
ValidationError: 1 validation error for ContentConfig
metadata.version
  string does not match regex '^[0-9]+\.[0-9]+\.[0-9]+$'
```

**Two-layer approach**:
```
Layer 1 (JSON Schema):
  metadata.version: '1.2' does not match pattern '^[0-9]+\.[0-9]+\.[0-9]+$'
  Hint: Version must be semver (e.g., '1.2.3')

Layer 2 (Pydantic):
  generation.jinja2_config: Required when generator='jinja2'
  Hint: Add 'jinja2_config' field with template path
```

**Key difference**: JSON Schema provides **structural** errors, Pydantic provides **business logic** errors.

### 2. IDE Support

**VS Code** with JSON Schema:
- ✅ Autocomplete for field names
- ✅ Inline validation errors
- ✅ Hover documentation
- ✅ Schema-driven snippets

**Example** (VS Code autocomplete):
```json
{
  "metadata": {
    "id": "my-config",
    "ti|  <-- VS Code suggests: "title", "version", "description"
  }
}
```

### 3. Version Management

**JSON Schema versions** are explicit:
```json
{
  "schemaRef": {
    "id": "content-schema",
    "version": "3.1"  // <-- Explicit schema version
  }
}
```

**Benefits**:
- Support multiple schema versions concurrently
- Migrate configs gradually (v3.0 → v3.1 → v4.0)
- Clear breaking change communication

### 4. Tooling Ecosystem

**JSON Schema ecosystem**:
- Schema validators (online, CLI, IDE plugins)
- Documentation generators (JSON Schema → Markdown)
- Faker/mock data generators
- Migration tools

**Pydantic ecosystem**:
- Type checkers (mypy, pyright)
- Auto-documentation (pydantic-docs)
- FastAPI integration
- Serialization (JSON, YAML, TOML)

**Leverage both ecosystems!**

---

## Trade-offs

### Verbosity vs Precision

**Cost**: Maintaining two validation layers = more code

**File count**:
- JSON Schema files: `schemas/content/v3.1/schema.json` (~300 lines)
- Pydantic models: `core/models.py` (~400 lines)
- **Total**: ~700 lines of validation code

**Benefit**: **Precision** and **clarity**
- JSON Schema: "What structure is allowed?"
- Pydantic: "What business rules apply?"

**Verdict**: Worth the verbosity for production systems

### Performance

**Validation overhead**:
- JSON Schema validation: ~5-10ms per config
- Pydantic validation: ~2-5ms per config
- **Total**: ~10-15ms per config load

**Comparison**:
- Pydantic-only: ~5-7ms
- **Overhead**: ~5-8ms (60% slower)

**Verdict**: Acceptable for config loading (not hot path)

### Learning Curve

**Developers must learn**:
1. JSON Schema syntax (Draft 2020-12)
2. Pydantic models and validators
3. When to use which layer

**Mitigation**:
- Clear documentation (this doc!)
- Examples in `/examples/`
- IDE autocomplete reduces learning curve

---

## Alternatives Considered

### Alternative 1: Pydantic Only

**Approach**: Use Pydantic models with extensive validators

**Pros**:
- ✅ Simpler (one tool)
- ✅ Faster validation
- ✅ Python-native

**Cons**:
- ❌ No IDE support for config editing
- ❌ No standard schema format
- ❌ Harder to generate documentation
- ❌ No cross-language support

**Why rejected**: IDE support is critical for user experience

### Alternative 2: JSON Schema Only

**Approach**: Use JSON Schema with custom validators

**Pros**:
- ✅ Standard format
- ✅ IDE support
- ✅ Cross-language

**Cons**:
- ❌ Complex business rules hard to express
- ❌ No Python type safety
- ❌ Poor error messages for logic errors
- ❌ Verbose for cross-field validation

**Why rejected**: Business rules too complex for pure JSON Schema

### Alternative 3: Custom Validation Framework

**Approach**: Build custom validator combining features

**Pros**:
- ✅ Tailored to needs
- ✅ Potentially optimal

**Cons**:
- ❌ Reinventing the wheel
- ❌ No ecosystem support
- ❌ Maintenance burden
- ❌ No IDE integration

**Why rejected**: Not worth the effort when standards exist

---

## Real-World Examples

### Example 1: Structural Error (JSON Schema catches)

**Config**:
```json
{
  "metadata": {
    "id": "my-config"
    // Missing required "title" field
  }
}
```

**Error** (Layer 1 - JSON Schema):
```
ValidationError: metadata: 'title' is a required property
Location: metadata
Hint: Add "title" field to metadata object
```

**Why Layer 1?** Missing required field is structural.

### Example 2: Business Logic Error (Pydantic catches)

**Config**:
```json
{
  "metadata": {"id": "test", "title": "Test"},
  "generation": {
    "generator": "jinja2"
    // Missing jinja2_config when generator is jinja2
  }
}
```

**Error** (Layer 2 - Pydantic):
```
ValidationError: generation.jinja2_config: Required when generator='jinja2'
Hint: Add 'jinja2_config' field with template path

Example:
  "jinja2_config": {
    "template": "templates/my-template.j2"
  }
```

**Why Layer 2?** Cross-field dependency is business logic.

### Example 3: Both Layers Working Together

**Config**:
```json
{
  "metadata": {
    "id": "",  // Empty string (fails Layer 1)
    "title": "Test",
    "version": "1.2"  // Invalid semver (fails Layer 1)
  },
  "generation": {
    "generator": "invalid-generator",  // Not in enum (fails Layer 1)
    "jinja2_config": {}  // Wrong config for wrong generator (fails Layer 2)
  }
}
```

**Errors** (both layers):
```
Layer 1 (JSON Schema) - 3 errors:
  metadata.id: '' does not satisfy minLength: 1
  metadata.version: '1.2' does not match pattern '^[0-9]+\.[0-9]+\.[0-9]+$'
  generation.generator: 'invalid-generator' is not one of ['jinja2', 'template_fill', ...]

Layer 2 would catch additional errors, but Layer 1 fails first (fail-fast)
```

---

## Future Evolution

### JSON Schema 2020-12 Features

chora-compose uses **Draft 2020-12** (latest stable):

**New features we use**:
- `$defs` for reusable definitions
- `unevaluatedProperties` for strict validation
- `prefixItems` for tuple validation
- `$dynamicRef` for recursive schemas

**Future possibilities**:
- `contentSchema` for validating string content
- `contentMediaType` for binary validation

### Pydantic v2 Features

chora-compose uses **Pydantic v2**:

**Features we use**:
- `field_validator` for custom validation
- `model_validator` for cross-field validation
- `Field()` for metadata and constraints
- `model_validate()` for dict → model conversion

**Future possibilities**:
- Strict mode (fail on extra fields)
- Discriminated unions (polymorphic configs)
- Computed fields (derived values)

---

## Guidelines for Contributors

### When to Use JSON Schema

✅ **Add to JSON Schema when**:
- Validating structure (required fields, types)
- Enforcing formats (email, uri, regex)
- Enum values (fixed options)
- Array constraints (minItems, uniqueItems)

**Example**:
```json
{
  "properties": {
    "email": {"type": "string", "format": "email"},
    "priority": {"type": "string", "enum": ["low", "medium", "high"]}
  }
}
```

### When to Use Pydantic

✅ **Add to Pydantic when**:
- Cross-field validation (field A depends on field B)
- Complex business rules (conditional logic)
- Type coercion (string → Path, datetime)
- Computed values (derived from other fields)

**Example**:
```python
@field_validator("artifact_parts")
@classmethod
def validate_parts_exist(cls, v):
    """Ensure referenced content configs exist."""
    for part in v:
        if not config_exists(part.content_id):
            raise ValueError(f"Content config '{part.content_id}' not found")
    return v
```

### Updating Validation

**When adding a new field**:

1. **Update JSON Schema** (`schemas/content/v3.1/schema.json`):
   ```json
   {
     "properties": {
       "newField": {"type": "string", "description": "..."}
     }
   }
   ```

2. **Update Pydantic Model** (`core/models.py`):
   ```python
   class ContentConfig(BaseModel):
       new_field: str | None = None
   ```

3. **Add validator if needed**:
   ```python
   @field_validator("new_field")
   @classmethod
   def validate_new_field(cls, v):
       # Business logic here
       return v
   ```

4. **Test both layers**:
   ```python
   # Test JSON Schema
   def test_schema_validation():
       invalid_config = {"newField": 123}  # Wrong type
       with pytest.raises(ConfigValidationError):
           loader.load_content_config(...)

   # Test Pydantic
   def test_business_logic():
       invalid_config = {"newField": "invalid-value"}
       with pytest.raises(ConfigValidationError):
           loader.load_content_config(...)
   ```

---

## Conclusion

The **two-layer validation approach** (JSON Schema + Pydantic) provides:

✅ **Best-in-class IDE support** (JSON Schema)
✅ **Python type safety** (Pydantic)
✅ **Clear error messages** (both layers)
✅ **Industry standards** (JSON Schema Draft 2020-12)
✅ **Business logic flexibility** (Pydantic validators)
✅ **Version management** (explicit schema versions)

**Trade-off**: Slightly more code and validation overhead, but worth it for production systems.

**Key principle**: Use JSON Schema for **structure**, Pydantic for **semantics**.

---

## Related Documentation

**Diataxis References**:
- [How-To: Validate Configs](../../how-to/configs/validate-configs.md) - Practical validation guide
- [Reference: ConfigLoader API](../../reference/api/core/config-loader.md) - API documentation
- [Tutorial: Understanding Content Configs](../../tutorials/getting-started/03-content-configs.md) - Learn configs

**Conceptual Relationships**:
- [Explanation: Configuration-Driven Development](../concepts/configuration-driven-development.md) - Why configs?
- [Explanation: Separate Config Types](separate-config-types.md) - Content vs Artifact configs
- [Explanation: Testing & Validation Approaches](../workflows/testing-validation-approaches.md) - Testing philosophy

**Technical References**:
- [JSON Schema 2020-12 Specification](https://json-schema.org/draft/2020-12/json-schema-validation.html)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)

---

**Document Version**: 1.0
**Last Updated**: 2025-10-21
**Author**: Generated via chora-compose documentation sprint
