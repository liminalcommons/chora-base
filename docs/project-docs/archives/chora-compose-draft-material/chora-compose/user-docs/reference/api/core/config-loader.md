# ConfigLoader API Reference

> **Purpose:** Load and validate Chora Compose configuration files with two-layer validation (JSON Schema + Pydantic).

## Overview

The `ConfigLoader` class is the primary interface for loading content and artifact configurations in the Chora Compose system. It provides:

- Automatic schema validation against JSON Schema Draft 2020-12
- Type-safe Pydantic model parsing
- Caching for performance
- Flexible loading by ID or path
- Clear error messages for validation failures
- **v1.1.0+:** Support for loading ephemeral draft configs

**Location:** [src/chora_compose/core/config_loader.py](../../../../src/chora_compose/core/config_loader.py)

**Related:** For ephemeral storage management, see [EphemeralConfigManager API](../storage/ephemeral-config-manager.md)

---

## Classes

### Class: ConfigLoader

```python
class ConfigLoader:
    """Loads and validates Chora Compose configuration files."""
```

The main class for loading configurations with two-layer validation.

#### Constructor

```python
def __init__(
    self,
    schema_dir: Optional[Path] = None,
    config_dir: Optional[Path] = None,
) -> None
```

Initialize a new ConfigLoader instance.

**Parameters:**

- `schema_dir` (Optional[Path]): Directory containing schema files. Defaults to `"schemas/"` relative to current working directory. Should contain subdirectories `content/` and `artifact/` with versioned schema files.

- `config_dir` (Optional[Path]): Base directory for configuration files. Defaults to `"configs/"` relative to current working directory. Should contain subdirectories `content/` and `artifacts/`.

**Storage Locations (v1.1.0+):**
- **Permanent configs:** `configs/content/`, `configs/artifact/` (tracked by git)
- **Ephemeral drafts:** `ephemeral/drafts/content/`, `ephemeral/drafts/artifact/` (temporary, 30-day retention)

**Example:**

```python
from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader

# Use default directories (schemas/ and configs/)
loader = ConfigLoader()

# Use custom directories
loader = ConfigLoader(
    schema_dir=Path("/custom/schemas"),
    config_dir=Path("/custom/configs")
)
```

---

#### Methods

##### load_content_config()

```python
def load_content_config(
    self,
    config_id: str,
    version: Optional[str] = None,
    config_path: Optional[Path] = None,
) -> ContentConfig
```

Load and validate a content configuration.

**Parameters:**

- `config_id` (str): ID of the content config to load. Used to construct default path: `configs/content/{config_id}/{config_id}-content.json`. Ignored if `config_path` is provided.

- `version` (Optional[str]): Optional specific version to load. Currently not used in path resolution but reserved for future versioning support. Default: None.

- `config_path` (Optional[Path]): Optional direct path to config file. When provided, overrides the `config_id` path resolution. Use this for loading configs from non-standard locations.

**Returns:**

`ContentConfig`: Validated and parsed content configuration as a Pydantic model with full type safety.

**Raises:**

- `FileNotFoundError`: If the config file doesn't exist at the resolved or provided path.
- `ConfigValidationError`: If validation fails at either the JSON Schema layer or Pydantic layer. Contains detailed error information.
- `json.JSONDecodeError`: If the file is not valid JSON.

**Example:**

```python
from chora_compose.core.config_loader import ConfigLoader

loader = ConfigLoader()

# Load by ID (recommended)
config = loader.load_content_config("readme-content")
print(f"Loaded: {config.id}")
print(f"Elements: {len(config.elements)}")

# Load from custom path
from pathlib import Path
config = loader.load_content_config(
    config_id="my-content",
    config_path=Path("custom/path/my-content.json")
)

# Access typed data
for element in config.elements:
    print(f"Element: {element.name}, Format: {element.format}")
```

---

##### load_artifact_config()

```python
def load_artifact_config(
    self,
    config_id: str,
    version: Optional[str] = None,
    config_path: Optional[Path] = None,
) -> ArtifactConfig
```

Load and validate an artifact configuration.

**Parameters:**

- `config_id` (str): ID of the artifact config to load. Used to construct default path: `configs/artifacts/{config_id}-artifact.json`. Ignored if `config_path` is provided.

- `version` (Optional[str]): Optional specific version to load. Currently not used in path resolution but reserved for future versioning support. Default: None.

- `config_path` (Optional[Path]): Optional direct path to config file. When provided, overrides the `config_id` path resolution.

**Returns:**

`ArtifactConfig`: Validated and parsed artifact configuration as a Pydantic model.

**Raises:**

- `FileNotFoundError`: If the config file doesn't exist.
- `ConfigValidationError`: If validation fails.
- `json.JSONDecodeError`: If the file is not valid JSON.

**Example:**

```python
from chora_compose.core.config_loader import ConfigLoader

loader = ConfigLoader()

# Load artifact by ID
artifact = loader.load_artifact_config("readme-artifact")
print(f"Artifact: {artifact.id}")
print(f"Output: {artifact.metadata.outputs[0].file}")
print(f"Children: {len(artifact.content.children)}")

# Access metadata
print(f"Type: {artifact.metadata.type}")
print(f"Composition: {artifact.metadata.compositionStrategy}")
```

---

##### load_config()

```python
def load_config(
    self,
    config_path: Path
) -> Union[ContentConfig, ArtifactConfig]
```

Load any config type by auto-detecting from the 'type' field in the JSON.

**Parameters:**

- `config_path` (Path): Path to the configuration file.

**Returns:**

`Union[ContentConfig, ArtifactConfig]`: Either a ContentConfig or ArtifactConfig depending on the `type` field in the JSON file.

**Raises:**

- `FileNotFoundError`: If the config file doesn't exist.
- `ConfigValidationError`: If validation fails or the type is unknown.
- `json.JSONDecodeError`: If the file is not valid JSON.

**Example:**

```python
from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.core.models import ContentConfig, ArtifactConfig

loader = ConfigLoader()

# Load any config type
config = loader.load_config(Path("configs/content/readme/readme-content.json"))

# Check type and handle accordingly
if isinstance(config, ContentConfig):
    print(f"Content config: {config.id}")
    print(f"Elements: {len(config.elements)}")
elif isinstance(config, ArtifactConfig):
    print(f"Artifact config: {config.id}")
    print(f"Output: {config.metadata.outputs[0].file}")
```

---

### Class: ConfigValidationError

```python
class ConfigValidationError(Exception):
    """Raised when config fails validation."""
```

Exception raised when configuration validation fails at either the JSON Schema or Pydantic validation layer.

#### Constructor

```python
def __init__(self, errors: Union[list[dict], str]) -> None
```

**Parameters:**

- `errors` (Union[list[dict], str]): Either a string error message or a list of error dictionaries. Each error dict should have `"path"` and `"message"` keys.

**Attributes:**

- `errors` (Union[list[dict], str]): The original errors passed to the constructor.

**Example:**

```python
from chora_compose.core.config_loader import ConfigLoader, ConfigValidationError

loader = ConfigLoader()

try:
    config = loader.load_content_config("invalid-config")
except ConfigValidationError as e:
    print(f"Validation failed:")
    print(e)  # Formatted error message
    print(f"\nRaw errors: {e.errors}")
except FileNotFoundError as e:
    print(f"File not found: {e}")
```

---

## Internal Methods

The following methods are internal implementation details but documented for completeness:

### _load_json_file()

```python
def _load_json_file(self, path: Path) -> dict
```

Load and parse a JSON file. Used internally by all load methods.

---

### _get_schema()

```python
def _get_schema(self, schema_type: str, version: str = "3.1") -> dict
```

Load JSON Schema for validation. Results are cached for performance.

**Parameters:**
- `schema_type`: "content" or "artifact"
- `version`: Schema version (default: "3.1")

---

### _validate_with_schema()

```python
def _validate_with_schema(
    self, config_data: dict, schema_type: str, version: str
) -> None
```

Validate config data against JSON Schema. First layer of two-layer validation.

---

## Two-Layer Validation

ConfigLoader performs validation in two stages:

### Layer 1: JSON Schema Validation

Uses `jsonschema` library to validate against JSON Schema Draft 2020-12:
- Checks required fields
- Validates types (string, number, boolean, etc.)
- Enforces pattern constraints (e.g., `^[a-z][a-z0-9-]*$` for IDs)
- Validates enums
- Checks array constraints (min/max items)

### Layer 2: Pydantic Validation

Parses validated JSON into type-safe Pydantic models:
- Strong typing with Python type hints
- Additional validation rules from Pydantic validators
- Automatic field coercion where appropriate
- Rich IDE support with autocomplete

**Benefits:**
1. Catch errors early with clear messages
2. Ensure configs are valid before processing
3. Provide type safety for Python code
4. Enable IDE autocomplete and type checking

See [Why Two-Layer Validation?](../../../explanation/why-two-layer-validation.md) for design rationale.

---

## Usage Patterns

### Pattern: Validate Multiple Configs

```python
from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader, ConfigValidationError

def validate_all_configs(config_dir: Path) -> tuple[list[Path], list[tuple[Path, str]]]:
    """Validate all configs in directory."""
    loader = ConfigLoader()
    valid = []
    invalid = []

    for config_file in config_dir.rglob("*.json"):
        try:
            loader.load_config(config_file)
            valid.append(config_file)
        except (ConfigValidationError, FileNotFoundError) as e:
            invalid.append((config_file, str(e)))

    return valid, invalid

# Use it
valid, invalid = validate_all_configs(Path("configs"))
print(f"Valid: {len(valid)}, Invalid: {len(invalid)}")
```

### Pattern: Config Metadata Extraction

```python
from chora_compose.core.config_loader import ConfigLoader

def extract_metadata(config_id: str) -> dict:
    """Extract metadata without processing content."""
    loader = ConfigLoader()
    config = loader.load_content_config(config_id)

    return {
        "id": config.id,
        "description": config.metadata.description,
        "version": config.metadata.version,
        "elements": [e.name for e in config.elements],
        "output_format": config.metadata.output_format,
    }

metadata = extract_metadata("readme-content")
print(metadata)
```

### Pattern: Conditional Loading

```python
from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader

def load_config_if_exists(config_id: str) -> Optional[ContentConfig]:
    """Load config only if it exists."""
    loader = ConfigLoader()
    config_path = Path(f"configs/content/{config_id}/{config_id}-content.json")

    if not config_path.exists():
        return None

    try:
        return loader.load_content_config(config_id)
    except Exception:
        return None
```

---

## Performance Considerations

### Schema Caching

Schemas are cached in memory after first load:
```python
loader = ConfigLoader()
# First load reads schema from disk
config1 = loader.load_content_config("config1")
# Subsequent loads use cached schema (faster)
config2 = loader.load_content_config("config2")
```

### Reusing Instances

Reuse ConfigLoader instances when loading multiple configs:
```python
# Good: Reuse loader instance
loader = ConfigLoader()
for config_id in config_ids:
    config = loader.load_content_config(config_id)

# Less efficient: Create new loader each time
for config_id in config_ids:
    loader = ConfigLoader()  # Re-reads schemas
    config = loader.load_content_config(config_id)
```

---

## Error Handling

### Common Errors

**FileNotFoundError:**
```
Config file not found: configs/content/my-config/my-config-content.json
```
- Check file exists at expected location
- Verify working directory
- Use explicit `config_path` parameter

**ConfigValidationError (JSON Schema):**
```
id -> Does not match pattern ^[a-z][a-z0-9-]*$
```
- Fix ID to use lowercase kebab-case
- Check all required fields present
- Verify enum values are valid

**ConfigValidationError (Pydantic):**
```
metadata.version -> Input should be a valid string
```
- Check field types match expectations
- Ensure dates are properly formatted
- Verify nested objects are complete

---

## See Also

- [Tutorial: Your First Config](../../../tutorials/getting-started/02-your-first-config.md) - Hands-on introduction
- [How to Load Configurations](../../../how-to/configs/load-configs.md) - Common recipes
- [ContentConfig Model Reference](../models/content-config.md) - Return type documentation
- [ArtifactConfig Model Reference](../models/artifact-config.md) - Return type documentation
- [Why Two-Layer Validation?](../../../explanation/why-two-layer-validation.md) - Design explanation
