# How to Load Configurations

> **Goal:** Load content and artifact configurations using various methods and handle common scenarios.

## When to Use This

You need to load configuration files in your Python code for:
- Generating content from configs
- Validating configuration structure
- Building workflows that process multiple configs
- Debugging configuration issues

## Prerequisites

- Chora Compose installed via Poetry
- Basic Python knowledge
- Understanding of content vs. artifact configs

---

## Solution

### Quick Version

```python
from chora_compose.core.config_loader import ConfigLoader

loader = ConfigLoader()

# Load content config by ID
content = loader.load_content_config("readme-content")

# Load artifact config by ID
artifact = loader.load_artifact_config("readme-artifact")

# Load any config by path (auto-detects type)
config = loader.load_config(Path("configs/content/readme/readme-content.json"))
```

### Detailed Steps

#### 1. Load by ID (Recommended)

The cleanest way to load configs is by their ID:

```python
from chora_compose.core.config_loader import ConfigLoader

loader = ConfigLoader()

# For content configs
content_config = loader.load_content_config(
    config_id="readme-content"
)

# For artifact configs
artifact_config = loader.load_artifact_config(
    artifact_id="readme-artifact"
)
```

**How it works:**
- Automatically searches in `configs/content/{id}/{id}.json` or `configs/artifacts/{id}.json`
- Returns strongly-typed Pydantic models
- Performs two-layer validation

#### 2. Load by Path

When you need to load from a specific location:

```python
from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader

loader = ConfigLoader()

# Auto-detects type (content or artifact)
config = loader.load_config(
    Path("configs/content/readme/readme-content.json")
)

# Check what type you got
from chora_compose.core.models import ContentConfig, ArtifactConfig

if isinstance(config, ContentConfig):
    print(f"Content config: {config.id}")
elif isinstance(config, ArtifactConfig):
    print(f"Artifact config: {config.id}")
```

#### 3. Load with Custom Directories

If your configs are in non-standard locations:

```python
from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader

loader = ConfigLoader(
    schema_dir=Path("custom/schemas"),
    config_dir=Path("custom/configs")
)

# Now loads from custom directories
config = loader.load_content_config("my-content")
```

#### 4. Load Specific Version

To load a specific version of a config:

```python
loader = ConfigLoader()

# Load specific version
config = loader.load_content_config(
    config_id="readme-content",
    version="3.1"
)

# Or use explicit path with version in filename
config = loader.load_content_config(
    config_id="readme-content",
    config_path=Path("configs/content/readme/readme-content-v3.1.json")
)
```

#### 5. Handle Loading Errors

```python
from chora_compose.core.config_loader import ConfigLoader
from jsonschema.exceptions import ValidationError
from pydantic import ValidationError as PydanticValidationError

loader = ConfigLoader()

try:
    config = loader.load_content_config("my-content")
except FileNotFoundError as e:
    print(f"Config file not found: {e}")
except ValidationError as e:
    print(f"JSON Schema validation failed: {e.message}")
except PydanticValidationError as e:
    print(f"Pydantic validation failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

#### 6. Load Multiple Configs

```python
from chora_compose.core.config_loader import ConfigLoader

loader = ConfigLoader()

config_ids = ["readme-content", "kernel-content"]
configs = []

for config_id in config_ids:
    try:
        config = loader.load_content_config(config_id)
        configs.append(config)
        print(f"✓ Loaded {config_id}")
    except Exception as e:
        print(f"✗ Failed to load {config_id}: {e}")

print(f"\nSuccessfully loaded {len(configs)} configs")
```

---

## Common Patterns

### Pattern: Load All Configs in Directory

```python
from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader

loader = ConfigLoader()
content_dir = Path("configs/content")

all_configs = []
for config_file in content_dir.rglob("*.json"):
    try:
        config = loader.load_config(config_file)
        all_configs.append(config)
    except Exception as e:
        print(f"Skipped {config_file}: {e}")

print(f"Loaded {len(all_configs)} configs")
```

### Pattern: Validate Without Processing

```python
from chora_compose.core.config_loader import ConfigLoader

def validate_config(config_path: Path) -> bool:
    """Check if a config is valid without processing it."""
    loader = ConfigLoader()
    try:
        loader.load_config(config_path)
        return True
    except Exception:
        return False

# Use it
if validate_config(Path("configs/content/test/test.json")):
    print("Config is valid!")
else:
    print("Config has errors")
```

### Pattern: Extract Metadata Only

```python
from chora_compose.core.config_loader import ConfigLoader

loader = ConfigLoader()
config = loader.load_content_config("readme-content")

# Access only metadata
print(f"ID: {config.id}")
print(f"Description: {config.metadata.description}")
print(f"Version: {config.metadata.version}")
print(f"Output Format: {config.metadata.output_format}")

# No need to process elements if you just want metadata
```

---

## Troubleshooting

**Problem:** `FileNotFoundError: Config file not found at configs/content/{id}/{id}.json`
**Solution:**
- Check that the file exists at the expected location
- Use explicit path with `config_path` parameter
- Verify your working directory is the project root

**Problem:** `JSON Schema validation failed: 'type' is a required property`
**Solution:**
- Ensure your config has all required top-level fields: `type`, `id`, `schemaRef`, `metadata`, `elements`
- Check the schema at [schemas/content/v3.1/schema.json](../../../schemas/content/v3.1/schema.json)

**Problem:** `Pydantic validation failed: validation error for ContentConfig`
**Solution:**
- The JSON Schema passed, but Pydantic found type issues
- Check field types match expectations (e.g., strings for enums, proper date formats)
- Review the full error message for the specific field causing issues

**Problem:** `SchemaRef version mismatch`
**Solution:**
- Ensure `schemaRef.version` in config matches the schema version (e.g., "3.1")
- Update configs to use the latest schema version

---

## See Also

- [Tutorial: Your First Config](../../tutorials/getting-started/02-your-first-config.md) - Step-by-step guide
- [How to Create a Content Config](create-content-config.md) - Build new configs
- [ConfigLoader API Reference](../../reference/api/core/config-loader.md) - Complete API
- [Why Two-Layer Validation?](../../explanation/why-two-layer-validation.md) - Design rationale
