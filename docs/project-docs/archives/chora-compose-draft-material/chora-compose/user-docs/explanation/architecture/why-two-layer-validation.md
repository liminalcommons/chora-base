# Why Two-Layer Validation?

> **Purpose:** Understand the rationale behind Chora Compose's dual validation strategy using both JSON Schema and Pydantic.

## The Problem

Configuration-driven systems face a fundamental challenge: **how do you ensure configurations are valid before using them in production?**

Without validation, systems can fail at runtime with cryptic errors:
```python
# Config has typo: "elemets" instead of "elements"
config = json.load(open("my-config.json"))
for element in config["elements"]:  # KeyError!
    process(element)
```

Traditional approaches have limitations:

### Approach 1: Manual Validation
```python
if "elements" not in config:
    raise ValueError("Missing elements")
if not isinstance(config["elements"], list):
    raise ValueError("Elements must be a list")
# ... dozens more checks ...
```

**Problems:**
- Tedious and error-prone
- Hard to maintain
- Inconsistent error messages
- No standardization

### Approach 2: JSON Schema Only
```python
jsonschema.validate(config, schema)
# Config is valid, but...
element_name = config["elements"][0]["name"]  # Type: Any
# No IDE autocomplete, no type safety
```

**Problems:**
- Runtime validation only
- No type safety in Python code
- No IDE support
- Still dealing with dicts and lists

### Approach 3: Pydantic Only
```python
class Config(BaseModel):
    elements: list[Element]

config = Config.model_validate(json_data)
# Great type safety, but...
```

**Problems:**
- No standardized JSON Schema output
- Harder to share schemas with other tools
- Pydantic-specific annotations
- Less explicit about validation rules

---

## The Solution: Two-Layer Validation

Chora Compose combines **JSON Schema (Layer 1)** and **Pydantic (Layer 2)** to get the best of both worlds:

```
User Config (JSON)
       ↓
[Layer 1: JSON Schema Validation]
  - Structure checks
  - Type validation
  - Pattern matching
  - Enum validation
       ↓
  Valid JSON
       ↓
[Layer 2: Pydantic Parsing]
  - Type-safe models
  - Additional validation
  - IDE autocomplete
  - Runtime type checking
       ↓
  Type-Safe Python Objects
```

### How It Works

```python
# Layer 1: JSON Schema validates structure
schema = {
    "type": "object",
    "required": ["id", "elements"],
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^[a-z][a-z0-9-]*$"
        },
        "elements": {
            "type": "array",
            "minItems": 1
        }
    }
}
jsonschema.validate(config_data, schema)  # Catches structural issues

# Layer 2: Pydantic provides type safety
class ContentConfig(BaseModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9-]*$")
    elements: list[ContentElement] = Field(min_length=1)

config = ContentConfig.model_validate(config_data)  # Type-safe object
```

---

## Why This Approach?

### 1. Standards Compliance

**JSON Schema** is an IETF standard (Draft 2020-12) for describing JSON data:
- Industry-wide adoption
- Tool ecosystem support
- Language-agnostic
- Well-documented specifications

**Benefit:** Other tools (validators, code generators, documentation tools) can use our schemas without needing Python.

**Example:**
```bash
# External validation tool
jsonschema -i my-config.json schemas/content/v3.1/schema.json
```

### 2. Early Error Detection

**JSON Schema catches errors before Python parsing:**

```json
{
  "id": "Invalid ID With Spaces",
  "elements": []
}
```

**Layer 1 (JSON Schema) fails:**
```
Validation error at $.id: Does not match pattern ^[a-z][a-z0-9-]*$
Validation error at $.elements: Must contain at least 1 item
```

**Without Layer 1,** these errors would only be caught when Pydantic parses, losing the opportunity for schema-level validation that external tools can also perform.

### 3. Type Safety and IDE Support

**Pydantic provides rich Python integration:**

```python
from chora_compose.core.config_loader import ConfigLoader

loader = ConfigLoader()
config = loader.load_content_config("my-content")

# IDE knows config is ContentConfig
config.id  # Autocomplete available
config.elements[0].name  # Type hints work
config.metadata.description  # No runtime errors

# Catches errors at development time
config.nonexistent_field  # IDE shows error before running
```

**Benefits:**
- Autocomplete in IDEs (VS Code, PyCharm)
- Type checking with mypy
- Refactoring support
- Self-documenting code

### 4. Clear Error Messages

**Two layers = Two chances to give helpful errors**

**Layer 1 error (structural):**
```
ConfigValidationError: JSON Schema validation failed:
  id: Does not match pattern ^[a-z][a-z0-9-]*$
  elements: [] is too short (minimum 1)
```

**Layer 2 error (type/logic):**
```
ConfigValidationError: Pydantic validation failed:
  metadata.version: Input should be a valid string
  elements.0.format: Input should be 'markdown', 'python', ...
```

### 5. Defense in Depth

**Two validators catch different classes of errors:**

| Error Type | JSON Schema | Pydantic | Example |
|------------|-------------|----------|---------|
| Missing field | ✅ | ✅ | `"elements"` required |
| Wrong type | ✅ | ✅ | `"version": 3.1` should be string |
| Pattern mismatch | ✅ | ✅ | ID must be kebab-case |
| Enum violation | ✅ | ✅ | Invalid generation type |
| Custom logic | ❌ | ✅ | Date format validation |
| Cross-field | Limited | ✅ | Field A requires field B |
| Type coercion | ❌ | ✅ | Auto-convert compatible types |

**Example of Pydantic-only validation:**
```python
class ContentElement(BaseModel):
    name: str
    example_output: Optional[str] = None

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        if len(v) > 100:
            raise ValueError('Name too long')
        return v.lower()  # Normalize to lowercase
```

---

## Trade-offs

### Advantages

✅ **Standards compliance** - JSON Schema is IETF standard
✅ **External tool support** - Any tool can validate using schemas
✅ **Type safety** - Pydantic provides rich Python types
✅ **IDE integration** - Autocomplete, type checking, refactoring
✅ **Better errors** - Two layers catch different error types
✅ **Documentation** - Schemas self-document the format
✅ **Validation before parsing** - Fail fast on structural issues

### Disadvantages

❌ **Slight complexity** - Two validation systems to maintain
❌ **Performance overhead** - Validate twice instead of once
❌ **Schema duplication** - Some validation rules appear in both layers

### Mitigations

**Schema duplication:**
We accept some duplication (pattern in JSON Schema + Pydantic Field) because:
1. JSON Schema is shareable with external tools
2. Pydantic enables type safety
3. Duplication is minimal and maintainable

**Performance:**
- Schema caching reduces overhead
- Validation is fast (<50ms for typical configs)
- Performance is acceptable for config loading (not in hot paths)

**Complexity:**
- Abstracted behind ConfigLoader - users don't see it
- Clear separation of concerns
- Well-documented for maintainers

---

## Alternatives Considered

### Alternative 1: JSON Schema Only

**Pros:**
- Standards-based
- External tool support
- Single source of truth

**Cons:**
- No type safety in Python
- No IDE support
- Working with dicts forever
- Manual type checking in code

**Why rejected:** Type safety is critical for maintainability in Python codebases.

### Alternative 2: Pydantic Only

**Pros:**
- Type-safe Python
- Great IDE support
- Single validation layer

**Cons:**
- No standard JSON Schema output
- External tools can't validate
- Less explicit validation rules
- Pydantic-specific ecosystem

**Why rejected:** Need to support external tooling and MCP integration with standard schemas.

### Alternative 3: Generate Pydantic from JSON Schema

**Pros:**
- Single source (JSON Schema)
- Automatic model generation

**Cons:**
- Generated code is hard to customize
- Build-time generation complexity
- Less control over model structure
- Generated models may not match design

**Why rejected:** Hand-crafted Pydantic models provide better control and customization.

### Alternative 4: Generate JSON Schema from Pydantic

Tools like `pydantic2schema` can export schemas from Pydantic models.

**Pros:**
- Single source (Pydantic)
- Automatic schema generation

**Cons:**
- Generated schemas less explicit
- Lose control over schema structure
- Harder to document for external users
- Pydantic changes affect schema

**Why rejected:** Need explicit, stable, well-documented JSON Schemas as primary contract.

---

## When to Use Each Layer

### Use JSON Schema For:
- Structural validation (required fields, types)
- Pattern matching (regex constraints)
- Enum validation
- Array constraints (min/max items)
- External tool integration
- Documentation generation

### Use Pydantic For:
- Type-safe Python code
- Custom validation logic
- Cross-field validation
- Type coercion
- Default values
- Computed properties

---

## How It Works in ConfigLoader

The `ConfigLoader` orchestrates both layers:

```python
class ConfigLoader:
    def load_content_config(self, config_id: str) -> ContentConfig:
        # 1. Load JSON from file
        config_data = self._load_json_file(path)

        # 2. LAYER 1: Validate with JSON Schema
        schema = self._get_schema("content", version)
        jsonschema.validate(config_data, schema)
        # Raises jsonschema.ValidationError if invalid

        # 3. LAYER 2: Parse with Pydantic
        config = ContentConfig.model_validate(config_data)
        # Raises pydantic.ValidationError if invalid

        # 4. Return type-safe object
        return config  # Type: ContentConfig
```

**Result:** Users get a validated, type-safe `ContentConfig` object that:
- Passed JSON Schema structural validation
- Passed Pydantic type validation
- Has full IDE autocomplete support
- Can't have runtime type errors

---

## Real-World Impact

### Before Two-Layer Validation

```python
# Load config (no validation)
with open("config.json") as f:
    config = json.load(f)

# Runtime error - typo in config
for elem in config["elemets"]:  # KeyError!
    print(elem["name"])

# No IDE support
config["metadata"]["descripton"]  # Typo not caught

# Type errors at runtime
process(config["version"])  # Expected int, got string
```

### After Two-Layer Validation

```python
# Load with validation
loader = ConfigLoader()
config = loader.load_content_config("my-content")
# Any issues caught immediately with clear errors

# Type-safe access
for elem in config.elements:  # IDE autocomplete
    print(elem.name)  # Can't typo - IDE shows error

# Type checking works
config.metadata.description  # Type: str
config.metadata.version  # Type: str

# mypy catches errors before runtime
reveal_type(config)  # Type: ContentConfig
```

---

## Future Considerations

### Potential Enhancements

1. **Schema generation from Pydantic**
   - Auto-generate reference schemas
   - Keep hand-written schemas as source of truth
   - Use generation for testing schema/model alignment

2. **Validation profiles**
   - Strict mode: Both layers required
   - Fast mode: Skip JSON Schema for trusted sources
   - External mode: JSON Schema only for external validators

3. **Incremental validation**
   - Validate only changed fields
   - Cache validation results
   - Optimize for large configs

4. **Custom validators**
   - Plugin system for domain-specific validation
   - External validation services
   - AI-powered validation

---

## Conclusion

Two-layer validation provides the best balance of:
- **Standards compliance** (JSON Schema)
- **Type safety** (Pydantic)
- **External tool support** (JSON Schema)
- **Developer experience** (Pydantic)

While it adds slight complexity, the benefits far outweigh the costs:
- Configs are validated before use
- Python code is type-safe
- External tools can validate independently
- IDEs provide excellent support
- Errors are caught early with clear messages

This approach makes Chora Compose both **robust** (validated configs) and **productive** (type-safe code).

---

## Related Topics

- [ConfigLoader API Reference](../../reference/api/core/config-loader.md) - Implementation details
- [Tutorial: Your First Config](../../tutorials/getting-started/02-your-first-config.md) - See validation in action
- [How to Load Configurations](../../how-to/configs/load-configs.md) - Practical usage
- [Content Schema Reference](../../reference/schemas/content-schema.md) - Layer 1 specification
- [ContentConfig Model](../../reference/api/models/content-config.md) - Layer 2 models
