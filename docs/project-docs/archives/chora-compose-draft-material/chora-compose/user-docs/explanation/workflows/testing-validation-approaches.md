# Testing and Validation Approaches in Chora Compose

**Philosophy**: Validate early, fail fast, and preview before execution.

**Audience**: Developers integrating chora-compose, contributors adding features, users creating content configs.

**Purpose**: Understand the multi-layered validation strategy and testing philosophy that ensures config correctness before execution.

---

## Overview

Chora Compose implements a **defense-in-depth** validation strategy with three layers:

1. **Schema validation** (structure) - JSON Schema validates config structure
2. **Model validation** (business logic) - Pydantic validates business rules
3. **Preview validation** (runtime) - Dry-run execution validates generation

This approach ensures configs are validated progressively, catching errors at the earliest possible stage and providing clear feedback for resolution.

---

## The Problem: Why Multiple Validation Layers?

### The Challenge

Configuration files can be syntactically correct but semantically invalid:

```json
{
  "type": "content",
  "id": "INVALID-ID",  // Valid JSON, invalid business rule (must be kebab-case)
  "schemaRef": {"id": "content-schema", "version": "3.1"},
  "metadata": {
    "description": "Test",
    "version": "not-semver",  // Valid string, invalid semantic version
    "generation_frequency": "manual",
    "output_format": "markdown"
  },
  "elements": [],  // Valid array, but business logic requires at least 1 element
  "generation": {
    "patterns": [{
      "type": "jinja2",
      "template": "{{ undefined_var }}"  // Valid syntax, undefined at runtime
    }]
  }
}
```

**Problems**:
- JSON Schema can't enforce kebab-case IDs
- JSON Schema can't validate semantic versioning
- JSON Schema can't detect runtime template errors
- Static validation can't catch context mismatches

**Solution**: Layer validations from cheapest (structure) to most expensive (runtime preview).

---

## Validation Layer 1: JSON Schema

### Purpose

Validate **structural correctness** and **required fields**.

### What It Validates

**Good at**:
- Required vs optional fields
- Type constraints (`string`, `number`, `boolean`, `array`, `object`)
- Enum values (`generation_frequency: "manual" | "on_demand" | "scheduled"`)
- Min/max constraints (array lengths, string lengths, number ranges)
- Pattern matching (basic regex like `^[a-z0-9-]+$`)

**Not good at**:
- Complex business rules (kebab-case enforcement)
- Cross-field validation (if field A exists, field B is required)
- Semantic validation (semantic versioning, date formats)
- Runtime errors (undefined template variables)

### Implementation

From [config_loader.py:112-146](../../src/chora_compose/core/config_loader.py#L112-L146):

```python
def _validate_with_schema(
    self, config_data: dict, schema_type: str, version: str
) -> None:
    """Validate config data against JSON Schema."""
    schema = self._get_schema(schema_type, version)

    # Create validator to collect all errors
    validator = jsonschema.Draft202012Validator(schema)
    validation_errors = list(validator.iter_errors(config_data))

    if validation_errors:
        # Collect all validation errors
        errors = []
        for error in validation_errors:
            error_dict = {
                "path": list(error.path),
                "message": error.message,
            }
            errors.append(error_dict)

        raise ConfigValidationError(errors)
```

**Key characteristics**:
- **Collects all errors** (not just first failure)
- **Provides error paths** (e.g., `["metadata", "version"]`)
- **Fast** (<5ms for typical configs)
- **Cached schemas** (loaded once, reused)

### Example Error

**Invalid config** (missing required field):

```json
{
  "type": "content",
  "id": "test-config",
  "schemaRef": {"id": "content-schema", "version": "3.1"}
  // Missing 'metadata' and 'elements'
}
```

**Error**:
```python
ConfigValidationError: [
  {
    "path": [],
    "message": "'metadata' is a required property"
  },
  {
    "path": [],
    "message": "'elements' is a required property"
  }
]
```

**Benefits**:
- Immediate feedback (before expensive parsing)
- Clear error paths (exactly which field failed)
- Multiple errors at once (fix all issues in one pass)

---

## Validation Layer 2: Pydantic Models

### Purpose

Validate **business logic** and **semantic constraints** after structure is confirmed valid.

### What It Validates

**Good at**:
- Custom validators (kebab-case IDs, semantic versions)
- Cross-field validation (if `generation` exists, validate `patterns`)
- Type coercion (string → int, loose types → strict types)
- Computed fields (derived values)
- Nested model validation (recursive validation)

**Not good at**:
- Runtime errors (template variable resolution)
- External dependencies (file existence, network resources)

### Implementation

From [config_loader.py:147-170](../../src/chora_compose/core/config_loader.py#L147-L170):

```python
def load_content_config(self, config_id: str) -> ContentConfig:
    """Load and validate content configuration."""
    # Get path
    config_path = self._get_config_path("content", config_id)

    # Load JSON
    config_data = self._load_json_file(config_path)

    # Layer 1: JSON Schema validation
    schema_version = config_data.get("schemaRef", {}).get("version", "3.1")
    self._validate_with_schema(config_data, "content", schema_version)

    # Layer 2: Pydantic validation
    try:
        return ContentConfig.model_validate(config_data)
    except ValidationError as e:
        raise ConfigValidationError(str(e)) from e
```

**Sequential validation**:
1. JSON Schema first (cheap, structure)
2. Pydantic second (expensive, business logic)
3. Only parse if structure is valid (avoid wasted CPU)

### Example Validation

**Invalid ID** (passes JSON Schema, fails Pydantic):

```json
{
  "type": "content",
  "id": "Invalid-ID-With-Capitals",  // Valid string, but not kebab-case
  "schemaRef": {"id": "content-schema", "version": "3.1"},
  "metadata": {
    "description": "Test",
    "version": "1.0.0",
    "generation_frequency": "manual",
    "output_format": "markdown"
  },
  "elements": [{"name": "test", "format": "markdown"}]
}
```

**Pydantic validator** (from `models.py`):

```python
from pydantic import BaseModel, field_validator

class ContentConfig(BaseModel):
    id: str

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Ensure ID is kebab-case lowercase."""
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", v):
            raise ValueError(
                f"ID must be kebab-case lowercase (letters, numbers, hyphens): {v}"
            )
        return v
```

**Error**:
```python
ValidationError: 1 validation error for ContentConfig
id
  ID must be kebab-case lowercase (letters, numbers, hyphens): Invalid-ID-With-Capitals
```

**Benefits**:
- Business rule enforcement (coding standards)
- Type safety (Pydantic models throughout codebase)
- Self-documenting (validators show requirements)

---

## Validation Layer 3: Preview/Dry-Run Execution

### Purpose

Validate **runtime behavior** without side effects (no file writes, no database changes).

### What It Validates

**Good at**:
- Template syntax errors (Jinja2 parsing)
- Undefined template variables (missing context)
- Generator execution (can it run without crashing?)
- Output correctness (does output look right?)

**Trade-off**: More expensive (full generation run) but catches runtime-only errors.

### Implementation Patterns

#### Pattern 1: Preview Generation Tool

From [tools.py:1794-1860](../../src/chora_compose/mcp/tools.py#L1794-L1860):

```python
async def preview_generation(
    content_config_id: str,
    context: dict[str, Any] | str | None = None,
    show_metadata: bool = False,
) -> dict[str, Any]:
    """
    Dry-run content generation without writing to storage.

    Perfect for testing templates, validating context, and previewing
    output before committing to storage.
    """
    start_time = time.time()
    context = context or {}

    # Load config (Layers 1 & 2 validation happen here)
    config_loader = ConfigLoader()
    config = config_loader.load_content_config(content_config_id)

    # Get generator
    registry = GeneratorRegistry()
    generator_type = config.generation.patterns[0].type
    generator = registry.get(generator_type)

    # Layer 3: Execute generation (dry-run)
    try:
        generated_content = generator.generate(config, context)
    except Exception as e:
        # Capture runtime errors (template errors, undefined vars, etc.)
        return {
            "success": False,
            "error": {
                "code": "generation_failed",
                "message": str(e),
                "details": {"generator": generator_type}
            }
        }

    # Return preview (NOT saved to storage)
    return {
        "success": True,
        "content": generated_content,
        "content_length": len(generated_content),
        "generator_used": generator_type,
        "duration_ms": int((time.time() - start_time) * 1000)
    }
```

**Key characteristics**:
- **No side effects** (nothing written to disk)
- **Full execution** (real generator, real template processing)
- **Runtime error capture** (catch template errors, undefined variables)
- **Fast feedback** (typically <100ms)

#### Pattern 2: Test Config Tool (Ephemeral Workflow)

From [config_tools.py:103-179](../../src/chora_compose/mcp/config_tools.py#L103-L179):

```python
async def test_config(
    draft_id: str,
    context: dict[str, Any] | str | None = None,
    dry_run: bool = True,
) -> dict[str, Any]:
    """Test a draft config by running generation without persisting output.

    Useful for validating config before committing to filesystem.
    """
    # Load draft from ephemeral storage
    config_mgr = get_ephemeral_config_manager()
    draft = config_mgr.get_draft(draft_id)

    # Parse to Pydantic model (Layers 1 & 2)
    content_config = ContentConfig(**draft.config_data)

    # Get generator
    generator_type = draft.config_data["generation"]["patterns"][0]["type"]
    registry = GeneratorRegistry()
    generator = registry.get(generator_type)

    # Layer 3: Generate content (dry-run)
    generated_content = generator.generate(content_config, context_dict)

    # Truncate preview if large (max 10000 chars)
    preview_content = generated_content[:10000]
    if len(generated_content) > 10000:
        preview_content += f"\n\n... (truncated, total {len(generated_content)} chars)"

    # Return result WITHOUT saving
    return TestConfigResult(
        success=True,
        draft_id=draft_id,
        preview_content=preview_content,
        content_length=len(generated_content),
        generator_used=generator_type,
        validation_issues=[],  # Could add custom checks here
        duration_ms=duration_ms
    )
```

**Workflow integration**:
1. User creates draft config in ephemeral storage (30-day retention)
2. User tests draft with `test_config` tool (preview output)
3. User iterates (edit draft, test again)
4. User commits draft to filesystem (only when preview looks good)

**Benefits**:
- **Safe iteration** (drafts isolated from production configs)
- **Immediate feedback** (see output before committing)
- **No pollution** (ephemeral storage auto-cleans after 30 days)

### Example: Catching Template Errors

**Config with undefined variable**:

```json
{
  "type": "content",
  "id": "test-template",
  "generation": {
    "patterns": [{
      "type": "jinja2",
      "template": "Hello, {{ user_name }}! Your balance is {{ account_balance }}."
    }]
  }
}
```

**Preview with incomplete context**:

```python
# User provides partial context
context = {"user_name": "Alice"}  # Missing 'account_balance'

# Preview catches the error
result = await preview_generation("test-template", context)
```

**Error**:
```python
{
  "success": False,
  "error": {
    "code": "generation_failed",
    "message": "UndefinedError: 'account_balance' is undefined",
    "details": {
      "generator": "jinja2",
      "missing_variables": ["account_balance"]
    }
  }
}
```

**User fixes context**:

```python
# Add missing variable
context = {
    "user_name": "Alice",
    "account_balance": 1234.56
}

# Preview succeeds
result = await preview_generation("test-template", context)
# {
#   "success": True,
#   "content": "Hello, Alice! Your balance is 1234.56.",
#   "generator_used": "jinja2"
# }
```

---

## Testing Philosophy: Validate Early, Fail Fast

### Progressive Validation

**Principle**: Validate in order of increasing cost.

```
┌─────────────────────────────────────────┐
│ Layer 1: JSON Schema (<5ms)            │ ← Cheapest, catches structure errors
│   ↓ Pass                                │
│ Layer 2: Pydantic (<20ms)              │ ← Mid-cost, catches business logic errors
│   ↓ Pass                                │
│ Layer 3: Preview (<100ms)              │ ← Most expensive, catches runtime errors
│   ✓ Valid config                        │
└─────────────────────────────────────────┘
```

**Why this order?**
1. **JSON Schema first**: Fast rejection of malformed configs (no wasted CPU on parsing)
2. **Pydantic second**: Business rules only applied to well-structured data
3. **Preview last**: Expensive generation only for configs that pass static validation

**Example cost comparison**:

| Validation | Cost | Errors Caught | When to Use |
|------------|------|---------------|-------------|
| JSON Schema | <5ms | Missing fields, wrong types, invalid enums | Every config load |
| Pydantic | <20ms | Kebab-case IDs, semantic versions, cross-field rules | Every config load |
| Preview | <100ms | Template errors, undefined variables, runtime failures | Before committing draft |

**Total overhead**: ~25ms per config load (Layers 1 & 2), acceptable for most use cases.

### Fail Fast Principle

**Principle**: Stop at first validation failure, provide clear error, don't proceed.

**Bad approach** (execute first, validate later):

```python
# ❌ Bad: Generate first, discover errors later
try:
    generated_content = generator.generate(config, context)
    save_to_file(generated_content)  # Too late! Already wrote bad data
except TemplateError as e:
    print(f"Oops, template was invalid: {e}")
```

**Good approach** (validate first, execute only if valid):

```python
# ✅ Good: Validate before expensive operations
try:
    # Layer 1: JSON Schema
    _validate_with_schema(config_data, "content", "3.1")

    # Layer 2: Pydantic
    config = ContentConfig.model_validate(config_data)

    # Layer 3: Preview (optional, for user-facing workflows)
    preview = generator.generate(config, context)  # Dry-run

    # Only execute if all validations pass
    generated_content = generator.generate(config, context)
    save_to_file(generated_content)  # Safe: validated beforehand

except ConfigValidationError as e:
    # Clear, early feedback
    print(f"Config invalid: {e}")
    # No side effects occurred
```

**Benefits**:
- **No partial execution** (all-or-nothing)
- **No cleanup needed** (nothing written on validation failure)
- **Clear error messages** (know exactly what failed and why)

---

## Config Validation Strategies

### Strategy 1: Strict Validation (Production)

**Use case**: Production configs that must be 100% correct.

**Approach**:
- All 3 validation layers
- Fail on any error
- No lenient parsing (strict types)

**Example**:

```python
class ConfigLoader:
    def load_content_config(self, config_id: str) -> ContentConfig:
        """Load with strict validation (production mode)."""
        config_data = self._load_json_file(self._get_config_path("content", config_id))

        # Layer 1: JSON Schema (strict)
        self._validate_with_schema(config_data, "content", "3.1")

        # Layer 2: Pydantic (strict)
        config = ContentConfig.model_validate(config_data)  # Raises on error

        # Implicit Layer 3: Happens at generation time
        return config
```

**When to use**:
- CI/CD pipelines (automated deployments)
- Production artifact generation
- Published configs (shared across team)

### Strategy 2: Lenient Validation (Development)

**Use case**: Rapid iteration during development, drafts, user-facing tools.

**Approach**:
- Layers 1 & 2 required
- Layer 3 optional (preview recommended)
- Warnings instead of errors for minor issues

**Example**:

```python
class EphemeralConfigManager:
    def create_draft(self, config_data: dict) -> Draft:
        """Create draft with lenient validation."""
        # Layer 1: JSON Schema (required)
        try:
            _validate_with_schema(config_data, "content", "3.1")
        except ConfigValidationError as e:
            # Re-raise structural errors (can't proceed without valid structure)
            raise

        # Layer 2: Pydantic (lenient)
        try:
            ContentConfig.model_validate(config_data)
        except ValidationError as e:
            # Log warnings but allow draft creation
            logger.warning(f"Draft has validation issues: {e}")

        # Save draft regardless (user will test_config before committing)
        return self._save_draft(config_data)
```

**When to use**:
- User-facing MCP tools (conversational workflow)
- Exploratory development (trying new templates)
- Ephemeral storage (30-day retention, safe to be lenient)

### Strategy 3: Test-Driven Validation (Integration Tests)

**Use case**: Testing generator implementations, config examples, documentation.

**Approach**:
- Fixture configs with known-good structure
- Validate expected vs actual output
- Test error handling paths

**Example** from [test_config_loader.py:39-60](../../tests/test_config_loader.py#L39-L60):

```python
def test_schema_validation(loader: ConfigLoader, tmp_path: Path) -> None:
    """Should validate against JSON Schema."""
    # Create invalid config (missing required field)
    invalid_config = {
        "type": "content",
        "id": "invalid",
        "schemaRef": {"id": "content-schema", "version": "3.1"},
        # Missing 'metadata' and 'elements' (required fields)
    }

    invalid_path = tmp_path / "invalid.json"
    invalid_path.write_text(json.dumps(invalid_config), encoding="utf-8")

    # Should raise ConfigValidationError
    with pytest.raises(ConfigValidationError) as exc_info:
        loader.load_config(invalid_path)

    # Verify error mentions missing fields
    assert (
        "required" in str(exc_info.value).lower()
        or "metadata" in str(exc_info.value).lower()
    )
```

**Benefits**:
- **Regression prevention** (ensure validation keeps working)
- **Documentation** (tests show expected behavior)
- **Error path coverage** (test failure modes)

---

## MCP Workflow: Draft → Validate → Test → Publish

### The Ephemeral Workspace Pattern

**Problem**: Users need to experiment with configs without polluting production configs.

**Solution**: Ephemeral storage with 30-day retention for drafts.

**Workflow**:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. CREATE DRAFT (Ephemeral Storage)                        │
│    ↓                                                        │
│    User: "Create a content config for release notes"       │
│    Tool: create_draft(config_data)                         │
│    Result: draft_id="draft-abc123"                         │
│                                                             │
│ 2. TEST DRAFT (Preview Generation)                         │
│    ↓                                                        │
│    User: "Test draft-abc123 with sample context"           │
│    Tool: test_config(draft_id, context)                    │
│    Result: preview_content="# Release v1.0.0..."           │
│                                                             │
│ 3. ITERATE (Edit & Re-test)                                │
│    ↓                                                        │
│    User: "Change template to include date"                 │
│    Tool: update_draft(draft_id, changes)                   │
│    Tool: test_config(draft_id, context)  # Test again      │
│    Result: preview_content="# Release v1.0.0 (2025-10-21)..│
│                                                             │
│ 4. COMMIT (Publish to Filesystem)                          │
│    ↓                                                        │
│    User: "Looks good, commit draft-abc123"                 │
│    Tool: commit_draft(draft_id, "release-notes-v1")        │
│    Result: Saved to configs/content/release-notes-v1.json  │
│                                                             │
│ 5. CLEANUP (Automatic)                                     │
│    ↓                                                        │
│    After 30 days: Draft auto-deleted from ephemeral storage│
└─────────────────────────────────────────────────────────────┘
```

**Key benefits**:
1. **Safe experimentation** (drafts isolated from production)
2. **Immediate feedback** (test_config shows output instantly)
3. **Iterative refinement** (edit → test → edit → test)
4. **No manual cleanup** (ephemeral storage auto-expires)

### Validation Touchpoints in MCP Workflow

**create_draft**:
- ✅ Layer 1: JSON Schema (required fields, types)
- ⚠️ Layer 2: Pydantic (warnings logged, not blocking)
- ❌ Layer 3: Not run (user will test_config manually)

**test_config**:
- ✅ Layer 1: JSON Schema (re-validated)
- ✅ Layer 2: Pydantic (strict, must pass to generate preview)
- ✅ Layer 3: Preview generation (catch runtime errors)

**commit_draft**:
- ✅ Layer 1: JSON Schema (final validation before filesystem write)
- ✅ Layer 2: Pydantic (strict, must pass to commit)
- ⚠️ Layer 3: Assumed tested (user should have run test_config first)

**Recommendation**: Always run `test_config` before `commit_draft`.

---

## Integration Testing Approaches

### Unit Tests: Individual Validators

**Goal**: Test each validation layer in isolation.

**Example** from [test_config_loader.py:62-80](../../tests/test_config_loader.py#L62-L80):

```python
def test_pydantic_validation(loader: ConfigLoader, tmp_path: Path) -> None:
    """Should validate with Pydantic models."""
    # Create config that passes JSON Schema but fails Pydantic
    config_with_invalid_id = {
        "type": "content",
        "id": "Invalid-ID-With-Capitals",  # Should be kebab-case lowercase
        "schemaRef": {"id": "content-schema", "version": "3.1"},
        "metadata": {
            "description": "Test",
            "version": "1.0.0",
            "generation_frequency": "manual",
            "output_format": "markdown",
        },
        "elements": [{"name": "test", "format": "markdown"}],
    }

    config_path = tmp_path / "test.json"
    config_path.write_text(json.dumps(config_with_invalid_id), encoding="utf-8")

    # Should raise ValidationError (Pydantic)
    with pytest.raises((ValidationError, ConfigValidationError)):
        loader.load_config(config_path)
```

**What this tests**:
- Layer 2 (Pydantic) catches errors Layer 1 (JSON Schema) misses
- Business rule enforcement (kebab-case IDs)
- Error types are correct

### Integration Tests: Full Workflow

**Goal**: Test complete user workflows (draft → test → commit).

**Example** from [test_phase2_workflow.py:51-99](../../tests/integration/test_phase2_workflow.py#L51-L99):

```python
def test_draft_to_generation_workflow(
    composer: ArtifactComposer,
    storage_manager: EphemeralStorageManager,
    temp_dir: Path
) -> None:
    """Test complete workflow: create draft → test → commit → generate."""
    # 1. Create draft
    draft_config = create_test_content_config(
        "test-content",
        template="{{elements_main_example_output}}",
        example_output="{{external_data}}"
    )
    draft = storage_manager.create_draft("test-content", draft_config)

    # 2. Test draft (preview generation)
    generator = DemonstrationGenerator()
    config = ContentConfig(**draft_config)
    context = {"external_data": "Test data"}

    preview_content = generator.generate(config, context)
    assert "Test data" in preview_content  # Validate preview output

    # 3. Commit draft to filesystem
    config_path = temp_dir / "configs" / "content" / "test-content.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(draft_config), encoding="utf-8")

    # 4. Generate content from committed config
    loader = ConfigLoader(config_dir=temp_dir / "configs")
    final_config = loader.load_content_config("test-content")
    final_content = generator.generate(final_config, context)

    # 5. Verify end-to-end correctness
    assert final_content == preview_content  # Preview matches final output
    assert "Test data" in final_content
```

**What this tests**:
- Complete user journey (all workflow steps)
- Preview accuracy (preview matches final output)
- Config persistence (drafted config → committed config)
- Cross-component integration (storage + loader + generator)

### End-to-End Tests: Real Configs, Real Generators

**Goal**: Test production configs with real generation.

**Example** from [test_jinja2_end_to_end.py](../../tests/integration/test_jinja2_end_to_end.py):

```python
def test_jinja2_generation_end_to_end(tmp_path: Path) -> None:
    """Test Jinja2 generator with real config and context."""
    # Use production config structure
    config = {
        "type": "content",
        "id": "user-greeting",
        "schemaRef": {"id": "content-schema", "version": "3.1"},
        "metadata": {
            "description": "Personalized user greeting",
            "version": "1.0.0",
            "generation_frequency": "on_demand",
            "output_format": "markdown"
        },
        "elements": [{"name": "greeting", "format": "markdown"}],
        "generation": {
            "patterns": [{
                "type": "jinja2",
                "template": """
                {% if is_premium %}
                # Welcome, Premium Member {{ user_name }}! 🌟
                {% else %}
                # Welcome, {{ user_name }}!
                {% endif %}

                You have {{ message_count }} new messages.
                """
            }]
        }
    }

    # Save config
    config_path = tmp_path / "user-greeting.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")

    # Load and validate (all 3 layers)
    loader = ConfigLoader(config_dir=tmp_path.parent)
    validated_config = loader.load_config(config_path)

    # Generate with real context
    generator = Jinja2Generator()
    context = {
        "user_name": "Alice",
        "is_premium": True,
        "message_count": 5
    }
    output = generator.generate(validated_config, context)

    # Verify output correctness
    assert "Premium Member Alice" in output
    assert "🌟" in output
    assert "5 new messages" in output
```

**What this tests**:
- Real-world config structure
- All validation layers (JSON Schema + Pydantic + runtime)
- Actual generator execution (not mocked)
- Output correctness

---

## Validation Error Patterns and Troubleshooting

### Common Error Pattern 1: Missing Required Fields

**Symptom**:
```python
ConfigValidationError: [
  {"path": [], "message": "'metadata' is a required property"}
]
```

**Cause**: JSON Schema validation failed (Layer 1).

**Fix**:

```json
{
  "type": "content",
  "id": "my-config",
  "schemaRef": {"id": "content-schema", "version": "3.1"},
  "metadata": {  // ← Add missing field
    "description": "My config",
    "version": "1.0.0",
    "generation_frequency": "manual",
    "output_format": "markdown"
  },
  "elements": [{"name": "main", "format": "markdown"}]
}
```

**Prevention**: Use schema-aware editor (VS Code with JSON Schema extension).

### Common Error Pattern 2: Invalid Business Rules

**Symptom**:
```python
ValidationError: 1 validation error for ContentConfig
id
  ID must be kebab-case lowercase (letters, numbers, hyphens): MyConfig
```

**Cause**: Pydantic validation failed (Layer 2).

**Fix**:

```json
{
  "id": "my-config"  // ← Change from "MyConfig" to "my-config"
}
```

**Prevention**: Follow naming conventions (kebab-case for IDs, semantic versioning for versions).

### Common Error Pattern 3: Runtime Template Errors

**Symptom**:
```python
{
  "success": False,
  "error": {
    "code": "generation_failed",
    "message": "UndefinedError: 'account_balance' is undefined"
  }
}
```

**Cause**: Preview generation failed (Layer 3) - missing context variable.

**Fix**:

```python
# Add missing variable to context
context = {
    "user_name": "Alice",
    "account_balance": 1234.56  # ← Add missing variable
}
```

**Prevention**: Use `preview_generation` or `test_config` before committing.

### Common Error Pattern 4: Type Mismatches

**Symptom**:
```python
ValidationError: 1 validation error for ContentConfig
metadata.version
  Input should be a valid string
```

**Cause**: JSON has wrong type (e.g., number instead of string).

**Fix**:

```json
{
  "metadata": {
    "version": "1.0.0"  // ← Change from 1.0 (number) to "1.0.0" (string)
  }
}
```

**Prevention**: Follow JSON Schema types (check schema for expected types).

---

## Best Practices

### Do ✅

1. **Validate progressively** (cheap to expensive)
   ```python
   # Layer 1 first (fast)
   _validate_with_schema(config_data, "content", "3.1")
   # Layer 2 second (medium)
   config = ContentConfig.model_validate(config_data)
   # Layer 3 optional (slow, user-facing only)
   preview = generator.generate(config, context)
   ```

2. **Use preview_generation before committing**
   ```python
   # Test before commit
   preview = await preview_generation("my-config", context)
   if preview["success"]:
       # Commit only if preview looks good
       await commit_draft(draft_id, "my-config")
   ```

3. **Collect all errors** (don't stop at first failure)
   ```python
   # JSON Schema collects all errors
   validation_errors = list(validator.iter_errors(config_data))
   # User fixes all issues in one pass
   ```

4. **Provide clear error messages**
   ```python
   raise ConfigValidationError({
       "path": ["metadata", "version"],
       "message": "Version must be semantic version (e.g., '1.0.0')",
       "received": "1.0"
   })
   ```

5. **Test error paths in integration tests**
   ```python
   # Test validation failures
   with pytest.raises(ConfigValidationError):
       loader.load_content_config("invalid-config")
   ```

### Don't ❌

1. **Don't execute before validating**
   ```python
   # ❌ Bad: Execute first
   content = generator.generate(config, context)  # Might fail mid-execution
   save_to_file(content)  # Too late to catch errors

   # ✅ Good: Validate first
   config = loader.load_content_config("my-config")  # Validates
   content = generator.generate(config, context)  # Safe to execute
   ```

2. **Don't skip Layer 3 in user-facing workflows**
   ```python
   # ❌ Bad: Commit without testing
   await commit_draft(draft_id, "my-config")  # User never saw preview

   # ✅ Good: Test first
   preview = await test_config(draft_id, context)
   # User reviews preview
   await commit_draft(draft_id, "my-config")
   ```

3. **Don't ignore validation errors**
   ```python
   # ❌ Bad: Swallow errors
   try:
       config = loader.load_content_config("my-config")
   except ConfigValidationError:
       pass  # Silent failure

   # ✅ Good: Handle explicitly
   try:
       config = loader.load_content_config("my-config")
   except ConfigValidationError as e:
       logger.error(f"Config validation failed: {e}")
       raise  # Re-raise or return error response
   ```

4. **Don't validate in wrong order**
   ```python
   # ❌ Bad: Expensive validation first
   config = ContentConfig.model_validate(config_data)  # Might fail on malformed JSON
   _validate_with_schema(config_data, "content", "3.1")  # Too late

   # ✅ Good: Cheap validation first
   _validate_with_schema(config_data, "content", "3.1")  # Fast rejection
   config = ContentConfig.model_validate(config_data)  # Only if structure valid
   ```

---

## Performance Considerations

### Validation Overhead

| Operation | Layer 1 (Schema) | Layer 2 (Pydantic) | Layer 3 (Preview) | Total |
|-----------|------------------|---------------------|-------------------|-------|
| Load config | ~5ms | ~20ms | N/A | ~25ms |
| Test draft | ~5ms | ~20ms | ~100ms | ~125ms |

**Interpretation**:
- **Config loading**: ~25ms overhead (acceptable for most use cases)
- **Draft testing**: ~125ms total (reasonable for interactive workflows)
- **Layer 3 dominates**: Preview generation is 4-5x slower than static validation

### Optimization Strategies

**1. Cache schemas** (avoid re-loading JSON Schema files):

```python
class ConfigLoader:
    def __init__(self):
        self._schema_cache = {}  # Cache schemas by type + version

    def _get_schema(self, schema_type: str, version: str) -> dict:
        cache_key = f"{schema_type}-{version}"
        if cache_key in self._schema_cache:
            return self._schema_cache[cache_key]  # Return cached

        schema = self._load_json_file(schema_path)
        self._schema_cache[cache_key] = schema  # Cache for reuse
        return schema
```

**Benefit**: 5ms → <1ms for subsequent loads.

**2. Skip Layer 3 in automated workflows** (CI/CD, batch jobs):

```python
# Production artifact generation (no preview needed)
config = loader.load_content_config("my-config")  # Layers 1 & 2 only
content = generator.generate(config, context)  # Direct execution
```

**Benefit**: 125ms → 25ms (5x faster).

**3. Parallelize validation in tests**:

```python
import asyncio

# Validate multiple configs concurrently
async def validate_all_configs(config_ids: list[str]):
    tasks = [validate_config(config_id) for config_id in config_ids]
    results = await asyncio.gather(*tasks)
    return results
```

**Benefit**: N configs in ~125ms (instead of N * 125ms sequentially).

---

## Trade-offs and Alternatives

### Trade-off 1: Validation Strictness

**Strict validation** (production):
- ✅ Catches errors early
- ✅ Prevents bad configs in production
- ❌ Slower iteration (must fix all errors before proceeding)

**Lenient validation** (development):
- ✅ Faster iteration (warnings instead of errors)
- ✅ Allows experimentation
- ❌ Risk of committing invalid configs

**Recommendation**: Strict in CI/CD, lenient in development tools.

### Trade-off 2: Validation Layers

**All 3 layers**:
- ✅ Maximum safety (catch all error types)
- ✅ Best user experience (preview before commit)
- ❌ Slower (~125ms total)

**Layers 1 & 2 only**:
- ✅ Faster (~25ms total)
- ✅ Sufficient for automated workflows
- ❌ Runtime errors not caught until execution

**Recommendation**: All 3 layers for user-facing tools, Layers 1 & 2 for automated workflows.

### Alternative: Single-Layer Validation

**Option**: Use only Pydantic (skip JSON Schema).

**Pros**:
- Simpler (one validation framework)
- Faster (skip Layer 1)

**Cons**:
- Pydantic errors less user-friendly (technical stack traces)
- JSON Schema provides better error paths (field-level errors)
- JSON Schema files serve as documentation (schema.json)

**Why we chose two layers**: Better error messages + documentation value.

---

## Related Documentation

### How-To Guides

- [Debug Jinja2 Templates](../../how-to/generation/debug-jinja2-templates.md) - Troubleshoot template errors
- [Use Template Fill Generator](../../how-to/generators/use-template-fill-generator.md) - Simple variable substitution
- [Create Content Configurations](../../how-to/configs/create-content-config.md) - Config structure

### Explanation

- [JSON Schema Validation](../design-decisions/json-schema-validation.md) - Why two validation layers
- [Event-Driven Telemetry](../design-decisions/event-driven-telemetry.md) - Observability for validation events
- [Config-Driven Architecture](../architecture/config-driven-architecture.md) - Overall design philosophy

### Reference

- [ConfigLoader API](../../reference/api/core/config-loader.md) - Validation API details
- [EphemeralConfigManager API](../../reference/api/storage/ephemeral-config-manager.md) - Draft management
- [MCP Tool Catalog](../../reference/api/mcp/tool-catalog.md) - Preview and test tools

### Tutorials

- [Generate Your First Content](../../tutorials/getting-started/03-generate-your-first-content.md) - Basic workflow
- [Work with Ephemeral Storage](../../tutorials/intermediate/05-work-with-ephemeral-storage.md) - Draft workflow

---

## Summary

**Key Takeaways**:

1. **Three validation layers** (progressive, cheap to expensive):
   - Layer 1: JSON Schema (structure)
   - Layer 2: Pydantic (business logic)
   - Layer 3: Preview (runtime)

2. **Fail fast principle**: Validate before execution, stop at first failure.

3. **Ephemeral workflow**: Draft → Test → Iterate → Commit (safe experimentation).

4. **Testing philosophy**: Unit tests (validators), integration tests (workflows), end-to-end tests (real configs).

5. **Performance**: ~25ms static validation, ~125ms with preview (acceptable for interactive use).

**When to use each layer**:
- **Production configs**: Layers 1 & 2 (automated, fast)
- **User-facing tools**: All 3 layers (preview before commit)
- **Development**: Layers 1 & 2 + manual Layer 3 testing

**Philosophy**: Validate early, fail fast, preview before execution.

---

**Last Updated**: 2025-10-21 | **Phase**: Sprint 3 - Explanation Quadrant Expansion
