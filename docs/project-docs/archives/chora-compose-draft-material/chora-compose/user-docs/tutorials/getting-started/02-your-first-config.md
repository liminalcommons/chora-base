# Tutorial: Your First Configuration

> **Learning Goal:** Load and validate a content configuration using ConfigLoader, understanding how Chora Compose reads and validates your generation instructions.

## What You'll Learn

By completing this tutorial, you'll be able to:
- Load content configurations from JSON files
- Understand two-layer validation (JSON Schema + Pydantic)
- Access configuration data in Python
- Handle validation errors effectively

## Prerequisites

- [ ] Chora Compose installed ([Installation Guide](01-installation.md))
- [ ] Python 3.12+
- [ ] Basic JSON knowledge
- [ ] Python familiarity

**Time Required:** ~15 minutes

---

## Understanding Content Configurations

Before loading configs, let's understand what they contain. A **content configuration** defines what content to generate and how.

### Configuration Structure

Content configs have this basic structure:

```json
{
  "type": "content",
  "id": "my-content",
  "schemaRef": {
    "uri": "file://schemas/content/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "description": "What this content is for"
  },
  "elements": [
    {
      "name": "section-1",
      "format": "markdown",
      "description": "First section"
    }
  ]
}
```

**Key sections:**
- **`type`** - Must be `"content"` (distinguishes from artifact configs)
- **`id`** - Unique identifier in kebab-case format
- **`schemaRef`** - Points to the validation schema
- **`metadata`** - Descriptive information about the config
- **`elements`** - The content pieces to generate

---

## Step 1: Explore an Existing Config

Let's examine a real configuration. Open this file in your editor:

```
configs/content/readme/readme-content.json
```

This config defines content for generating a README file. Notice:
- Clear element names (like `"introduction"`, `"features"`)
- Each element has format, description, and generation instructions
- Metadata provides context about the config's purpose

---

## Step 2: Write Your First Loader Script

Create a file called `load_config.py` in your project root:

```python
from chora_compose.core.config_loader import ConfigLoader

# Initialize the loader
loader = ConfigLoader()

# Load configuration by ID
config = loader.load_content_config("readme-content")

# Explore the loaded configuration
print(f"Config ID: {config.id}")
print(f"Description: {config.metadata.description}")
print(f"Elements: {len(config.elements)}")
print(f"\nFirst element name: {config.elements[0].name}")
print(f"First element format: {config.elements[0].format}")
```

**What this does:**
1. Imports `ConfigLoader` from Chora Compose
2. Creates a loader instance (uses default paths: `schemas/` and `configs/`)
3. Loads config by ID - automatically finds `configs/content/readme/readme-content.json`
4. Accesses the parsed data through type-safe Pydantic models

---

## Step 3: Run Your Script

Execute the script:

```bash
poetry run python load_config.py
```

**Expected output:**
```
Config ID: readme-content
Description: Content for the main README.md file
Elements: 2

First element name: introduction
First element format: markdown
```

**Success!** You've loaded your first configuration and accessed its data.

---

## Step 4: Understand Two-Layer Validation

chora-compose validates configurations twice for maximum safety:

### Layer 1: JSON Schema Validation
Checks structure, data types, required fields, and format patterns.

### Layer 2: Pydantic Validation
Provides type-safe Python models with additional validation logic.

### See Validation in Action

Create an invalid config file `invalid_config.json`:

```json
{
  "type": "content",
  "id": "Invalid ID With Spaces",
  "schemaRef": {
    "uri": "file://schemas/content/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "description": "This config has validation errors"
  },
  "elements": []
}
```

**This config has problems:**
- ID contains spaces (must be kebab-case: `my-config-id`)
- Empty elements array (requires at least 1 element)

### Try Loading It

Create `test_validation.py`:

```python
from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader

loader = ConfigLoader()

try:
    config = loader.load_config(Path("invalid_config.json"))
    print("Config loaded successfully")
except Exception as e:
    print(f"Validation failed!")
    print(f"Error: {e}")
```

Run it:

```bash
poetry run python test_validation.py
```

**You'll see a validation error** explaining exactly what's wrong. The two-layer validation catches errors early with helpful messages.

---

## Step 5: Two Ways to Load Configs

### Method 1: Load by ID (Recommended)

```python
loader = ConfigLoader()
config = loader.load_content_config("readme-content")
```

**Advantages:**
- Cleaner code
- Follows convention: `configs/{type}/{id}/{id}.json`
- Automatic path resolution

### Method 2: Load by Explicit Path

```python
from pathlib import Path

loader = ConfigLoader()
config = loader.load_config(
    Path("configs/content/readme/readme-content.json")
)
```

**When to use:**
- Non-standard file locations
- Configs outside the main structure
- Dynamic path construction

**Best practice:** Use Method 1 (by ID) for standard project configs.

---

## Step 6: Explore Configuration Data

Loaded configs are strongly-typed Pydantic models. You get autocomplete and type checking!

### Access All Configuration Properties

```python
from chora_compose.core.config_loader import ConfigLoader

loader = ConfigLoader()
config = loader.load_content_config("readme-content")

# Basic properties
print(f"Config ID: {config.id}")
print(f"Schema version: {config.schemaRef.version}")
print(f"Description: {config.metadata.description}")

# Iterate through elements
print(f"\n{'='*50}")
print("CONTENT ELEMENTS:")
print('='*50)

for i, element in enumerate(config.elements, 1):
    print(f"\n{i}. {element.name}")
    print(f"   Format: {element.format}")
    print(f"   Description: {element.description}")

    if element.example_output:
        length = len(element.example_output)
        print(f"   Has example output: {length} characters")

# Check generation patterns
if config.generation and config.generation.patterns:
    print(f"\n{'='*50}")
    print("GENERATION PATTERNS:")
    print('='*50)

    for pattern in config.generation.patterns:
        print(f"\n- Pattern ID: {pattern.id}")
        print(f"  Type: {pattern.type}")
        if pattern.variables:
            print(f"  Variables: {len(pattern.variables)}")
```

### Type Safety Benefits

Because configs are Pydantic models:
- **Autocomplete** in your IDE
- **Type checking** with mypy
- **Runtime validation** prevents bad data
- **Clear error messages** when things go wrong

---

## What You Learned

In this tutorial, you successfully:

- ✅ Understood content configuration structure
- ✅ Created and used a ConfigLoader instance
- ✅ Loaded configurations by ID
- ✅ Explored two-layer validation (JSON Schema + Pydantic)
- ✅ Accessed config data through type-safe models
- ✅ Handled validation errors effectively
- ✅ Learned two loading methods (ID vs path)

---

## Next Steps

### Continue Learning

Progress through the tutorial series:
- **[Generate Your First Content →](03-generate-your-first-content.md)** - Use configs to generate content
- **[Compose Your First Artifact](04-compose-your-first-artifact.md)** - Assemble final outputs

### Explore Further

- **[How to Create a Content Config](../../how-to/configs/create-content-config.md)** - Build your own configurations
- **[ConfigLoader API Reference](../../reference/api/core/config-loader.md)** - Complete API documentation
- **[Why Two-Layer Validation?](../../explanation/architecture/why-two-layer-validation.md)** - Design rationale

---

## Troubleshooting

### Config Not Found

**Error:** `FileNotFoundError: Config 'my-config' not found`

**Solutions:**
- Verify you're running from project root
- Check config exists at expected path: `configs/content/{id}/{id}.json`
- Try explicit path loading instead of ID loading
- Pass custom config directory to ConfigLoader constructor:
  ```python
  loader = ConfigLoader(config_dir=Path("/custom/path"))
  ```

### Validation Errors

**Error:** `ValidationError: [detailed pydantic error]`

**Solutions:**
- Read the error message carefully - it pinpoints the problem
- Common issues:
  - Missing required fields
  - Wrong data types (string vs number)
  - Pattern violations (IDs must be kebab-case)
  - Empty arrays where items are required
- Compare your config against working examples in `configs/`

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'chora_compose'`

**Solutions:**
- Run `poetry install` from project root
- Always use `poetry run python your_script.py`
- Or activate Poetry shell: `poetry shell`
- Verify installation: `poetry run python -c "import chora_compose"`

### Schema Validation Fails

**Error:** JSON Schema validation errors

**Solutions:**
- Ensure `schemaRef.uri` points to existing schema file
- Verify schema version matches your Chora Compose version
- Check that `schemas/content/v3.1/schema.json` exists
- Don't modify schema files manually

---

**Tutorial complete!** You now know how to load and validate configurations.

**Next:** [Generate Your First Content →](03-generate-your-first-content.md)
