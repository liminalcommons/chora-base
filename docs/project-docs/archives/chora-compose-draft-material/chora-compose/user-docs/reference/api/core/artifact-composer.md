# ArtifactComposer API Reference

> **Purpose:** Orchestrate artifact assembly by loading content configs, generating content, and composing final output files.

## Overview

The `ArtifactComposer` is the top-level orchestrator in Chora Compose. It manages the complete workflow:

1. Load artifact configuration
2. Resolve and load referenced content configs
3. Generate content using appropriate generators
4. Compose content according to strategy
5. Write final output file(s)

This is typically the main entry point for users - everything else is internal.

**Location:** [src/chora_compose/core/composer.py](../../../../src/chora_compose/core/composer.py)

**Since:** Version 0.1.0

---

## Quick Reference

```python
from chora_compose.core.composer import ArtifactComposer

# Create composer
composer = ArtifactComposer()

# Assemble artifact
output_path = composer.assemble("my-artifact")

print(f"Generated: {output_path}")
```

---

## Classes

### Class: ArtifactComposer

```python
class ArtifactComposer:
    """
    Composes final artifacts by loading content configs and generating output.

    The composer orchestrates the full workflow:
    1. Loads artifact configuration
    2. Resolves and loads all referenced content configs
    3. Generates content for each config using appropriate generator
    4. Composes all content according to composition strategy
    5. Writes final output to specified file(s)
    """
```

Main orchestrator for artifact assembly and composition.

**Thread Safety:** Thread-safe if using separate instances per thread (ConfigLoader is stateless)

**Since:** Version 0.1.0

---

#### Constructor

```python
def __init__(
    self,
    config_loader: Optional[ConfigLoader] = None
) -> None
```

Initialize the artifact composer.

**Parameters:**

- `config_loader` (Optional[ConfigLoader]): ConfigLoader instance for loading configurations. If `None`, creates a new `ConfigLoader()` with default settings (schemas in `schemas/`, configs in `configs/`). Providing a custom loader allows using different directories or custom caching strategies.

**Attributes Set:**

- `self.loader` (ConfigLoader): ConfigLoader instance (provided or newly created)
- `self.generators` (dict): Registry mapping `GenerationType` to generator instances. Initially contains:
  - `GenerationType.DEMONSTRATION`: `DemonstrationGenerator()` instance

**Example:**

```python
from chora_compose.core.composer import ArtifactComposer

# Use default directories
composer = ArtifactComposer()

# Use custom config loader
from chora_compose.core.config_loader import ConfigLoader
from pathlib import Path

custom_loader = ConfigLoader(
    schema_dir=Path("custom/schemas"),
    config_dir=Path("custom/configs")
)
composer = ArtifactComposer(config_loader=custom_loader)
```

---

#### Methods

##### assemble()

```python
def assemble(
    self,
    artifact_id: str,
    artifact_path: Optional[Path] = None,
    output_override: Optional[Path] = None
) -> Path
```

Assemble an artifact from its configuration.

This is the main method users call. It performs the complete assembly workflow.

**Parameters:**

- `artifact_id` (str, required): ID of the artifact to assemble. Used to locate the artifact config at `configs/artifacts/{artifact_id}.json` (unless `artifact_path` is provided).

- `artifact_path` (Optional[Path], optional): Optional direct path to the artifact config file. When provided, overrides the default path resolution. Use this for non-standard locations or testing.  Default: `None`.

- `output_override` (Optional[Path], optional): Optional override for the output file path. When provided, overrides the path specified in `artifact.metadata.outputs[0].file`. Useful for testing or custom build systems. Default: `None`.

**Returns:**

`Path`: Path to the generated output file. This is either:
- `output_override` if provided
- `Path(artifact.metadata.outputs[0].file)` from config

**Raises:**

- `CompositionError`: Wraps all errors that occur during assembly:
  - Failed to load artifact config
  - Failed to load required content config
  - Failed to generate required content
  - No output files defined in artifact
  - Failed to write output file

**Workflow:**

1. Load artifact config (by ID or path)
2. Sort children by `order` field (ascending)
3. For each child:
   - Load content config from `child.path`
   - Generate content using appropriate generator
   - If generation fails and `child.required == true`, raise error
   - If generation fails and `child.required == false`, skip and continue
4. Compose all generated content using composition strategy
5. Determine output path (from config or override)
6. Create parent directories if needed
7. Write composed content to output file
8. Return output path

**Example:**

```python
from chora_compose.core.composer import ArtifactComposer

composer = ArtifactComposer()

# Basic usage
output_path = composer.assemble("readme-artifact")
print(f"Generated: {output_path}")

# With custom artifact path
from pathlib import Path
output_path = composer.assemble(
    "test-artifact",
    artifact_path=Path("tests/fixtures/artifacts/test.json")
)

# With output override
output_path = composer.assemble(
    "readme-artifact",
    output_override=Path("build/README.md")
)
```

**Example with error handling:**

```python
from chora_compose.core.composer import ArtifactComposer, CompositionError

composer = ArtifactComposer()

try:
    output_path = composer.assemble("my-artifact")
    print(f"✓ Success: {output_path}")

except CompositionError as e:
    error_msg = str(e)

    if "Failed to load artifact config" in error_msg:
        print("✗ Artifact config not found or invalid")
    elif "required content" in error_msg:
        print("✗ Missing required content section")
    elif "No output files defined" in error_msg:
        print("✗ Artifact config missing outputs")
    elif "Failed to write output" in error_msg:
        print("✗ Cannot write to output location")
    else:
        print(f"✗ Composition failed: {e}")
```

---

##### register_generator()

```python
def register_generator(
    self,
    generation_type: GenerationType,
    generator: object
) -> None
```

Register a custom generator for a generation type.

Use this to add support for new generation types beyond the built-in `DemonstrationGenerator`.

**Parameters:**

- `generation_type` (GenerationType, required): The type of generation this generator handles. Must be a value from the `GenerationType` enum (e.g., `GenerationType.JINJA2`, `GenerationType.CODE_GENERATION`).

- `generator` (object, required): Generator instance that implements the `GeneratorStrategy` interface (has a `generate(config, context)` method). Should be stateless for thread safety.

**Returns:**

`None`

**Example:**

```python
from chora_compose.core.composer import ArtifactComposer
from chora_compose.core.models import GenerationType
from chora_compose.generators.jinja2 import Jinja2Generator

composer = ArtifactComposer()

# Register Jinja2 generator
jinja2_gen = Jinja2Generator(template_dir=Path("templates"))
composer.register_generator(GenerationType.JINJA2, jinja2_gen)

# Now can assemble artifacts using Jinja2 patterns
output = composer.assemble("dynamic-artifact")
```

**Example with custom generator:**

```python
from chora_compose.generators.base import GeneratorStrategy
from chora_compose.core.models import ContentConfig

class CustomGenerator(GeneratorStrategy):
    """Custom content generator."""

    def generate(self, config: ContentConfig, context: dict | None = None) -> str:
        # Your custom generation logic
        return "Custom generated content"

# Register it
composer = ArtifactComposer()
composer.register_generator(GenerationType.CUSTOM, CustomGenerator())
```

---

## Internal Methods

The following methods are implementation details:

### _generate_child_content()

```python
def _generate_child_content(
    self,
    content_path: str,
    content_id: str
) -> str
```

Generate content for a single content config (one child).

**Parameters:**
- `content_path` (str): Path to content config file (from child.path)
- `content_id` (str): ID of content config (from child.id)

**Returns:**
- `str`: Generated content

**Raises:**
- `CompositionError`: If content config cannot be loaded or generation fails

**Path Resolution:**
1. If path is absolute, use it directly
2. If relative, first try relative to current directory
3. If not found, try relative to `configs/` directory
4. If still not found, raise error

**Generator Selection:**
1. Load content config
2. Extract generation pattern type (defaults to `demonstration`)
3. Look up generator in `self.generators`
4. Call `generator.generate(config)`

---

### _compose_content()

```python
def _compose_content(
    self,
    contents: list[str],
    strategy: CompositionStrategy
) -> str
```

Compose multiple content pieces according to composition strategy.

**Parameters:**
- `contents` (list[str]): List of generated content strings (from children)
- `strategy` (CompositionStrategy): Composition strategy from artifact metadata

**Returns:**
- `str`: Final composed content

**Raises:**
- `CompositionError`: If strategy is not supported

**Current Implementation:**
- `CompositionStrategy.CONCAT`: Joins content with `"\n\n"` (double newline)
- Other strategies: Raises `CompositionError`

**Future strategies:** `MERGE`, `OVERLAY`, `CUSTOM`

---

## Exceptions

### Exception: CompositionError

```python
class CompositionError(Exception):
    """Raised when artifact composition fails."""
```

Wraps all errors that occur during artifact assembly.

**Inherits from:** `Exception`

**Common messages:**

- `"Failed to load artifact config: {details}"` - Artifact config not found or invalid
- `"Failed to generate required content '{content_id}': {details}"` - Required content generation failed
- `"Artifact '{artifact_id}' has no output files defined"` - `metadata.outputs` is empty
- `"Failed to write output file: {details}"` - Cannot write to output path
- `"Content config not found: {path}"` - Child content config missing
- `"No generator available for type: {type}"` - Unsupported generation type
- `"Composition strategy not yet supported: {strategy}"` - Unsupported composition strategy

**Example:**

```python
from chora_compose.core.composer import CompositionError

try:
    output = composer.assemble("artifact")
except CompositionError as e:
    print(f"Composition failed: {e}")
    # e.args[0] contains the error message
```

---

## Usage Patterns

### Pattern: Batch Assembly

```python
from chora_compose.core.composer import ArtifactComposer

def batch_assemble(artifact_ids: list[str]) -> dict[str, Path]:
    """Assemble multiple artifacts efficiently."""
    composer = ArtifactComposer()  # Reuse instance
    results = {}

    for artifact_id in artifact_ids:
        try:
            output_path = composer.assemble(artifact_id)
            results[artifact_id] = output_path
        except Exception as e:
            print(f"Failed {artifact_id}: {e}")
            results[artifact_id] = None

    return results

# Use it
artifacts = ["readme", "api-docs", "user-guide"]
outputs = batch_assemble(artifacts)
```

### Pattern: CI/CD Integration

```python
import sys
from pathlib import Path
from chora_compose.core.composer import ArtifactComposer, CompositionError

def ci_assemble(artifact_id: str, output_dir: Path) -> int:
    """Assemble artifact for CI/CD. Returns exit code."""
    composer = ArtifactComposer()

    try:
        output_override = output_dir / f"{artifact_id}.md"
        result = composer.assemble(artifact_id, output_override=output_override)

        print(f"✓ Generated: {result}")
        return 0  # Success

    except CompositionError as e:
        print(f"✗ Failed: {e}", file=sys.stderr)
        return 1  # Failure

if __name__ == "__main__":
    exit_code = ci_assemble("readme", Path("dist"))
    sys.exit(exit_code)
```

### Pattern: Custom Generator Registry

```python
from pathlib import Path
from chora_compose.core.composer import ArtifactComposer
from chora_compose.core.models import GenerationType
from chora_compose.generators.jinja2 import Jinja2Generator

def create_full_composer() -> ArtifactComposer:
    """Create composer with all generators registered."""
    composer = ArtifactComposer()

    # Register additional generators
    composer.register_generator(
        GenerationType.JINJA2,
        Jinja2Generator(template_dir=Path("templates"))
    )

    # Future: Add more generators
    # composer.register_generator(GenerationType.CODE_GENERATION, AIGenerator())

    return composer

# Use it
composer = create_full_composer()
output = composer.assemble("dynamic-artifact")  # Can use Jinja2
```

---

## Performance Considerations

**Composer is Lightweight:**
- Minimal state (just ConfigLoader and generator registry)
- Safe to create multiple instances
- Preferred: Reuse instance for batch operations

**ConfigLoader Caching:**
- Composer's ConfigLoader caches schemas
- Reusing composer = faster subsequent loads
- First assembly: ~100-500ms
- Subsequent assemblies: ~50-200ms (schema cache hit)

**Optimization Tips:**

1. **Reuse composer instance:**
```python
# Good
composer = ArtifactComposer()
for artifact_id in ids:
    output = composer.assemble(artifact_id)

# Less efficient
for artifact_id in ids:
    composer = ArtifactComposer()
    output = composer.assemble(artifact_id)
```

2. **Use custom ConfigLoader for advanced caching:**
```python
loader = ConfigLoader()
# loader has schema cache

composer1 = ArtifactComposer(config_loader=loader)
composer2 = ArtifactComposer(config_loader=loader)
# Both share the same schema cache
```

3. **Parallel assembly (if safe):**
```python
from concurrent.futures import ThreadPoolExecutor

def assemble_one(artifact_id: str) -> Path:
    composer = ArtifactComposer()  # Separate instance per thread
    return composer.assemble(artifact_id)

with ThreadPoolExecutor(max_workers=4) as executor:
    outputs = list(executor.map(assemble_one, artifact_ids))
```

**Typical Performance:**
- Small artifacts (2-3 sections): 50-100ms
- Medium artifacts (5-10 sections): 100-300ms
- Large artifacts (20+ sections): 300-1000ms

Bottlenecks are usually:
- File I/O (loading configs)
- Content generation (complex patterns)
- Output file writing

---

## Thread Safety

✅ **Thread-safe with caveats:**

- Each thread should have its own `ArtifactComposer` instance
- OR share a `ConfigLoader` between composers (ConfigLoader is stateless)
- Generators should be stateless (DemonstrationGenerator is)

**Safe pattern:**
```python
import threading

def worker(artifact_id: str):
    composer = ArtifactComposer()  # Per-thread instance
    output = composer.assemble(artifact_id)

threads = [
    threading.Thread(target=worker, args=(f"artifact{i}",))
    for i in range(10)
]

for t in threads:
    t.start()
for t in threads:
    t.join()
```

---

## Compatibility

**Python Versions:** 3.12+

**Dependencies:**
- `chora_compose.core.config_loader` - ConfigLoader
- `chora_compose.core.models` - Config models, enums
- `chora_compose.generators.demonstration` - DemonstrationGenerator

**Breaking Changes:**
- None yet (initial version)

---

## See Also

- [Tutorial: Compose Your First Artifact](../../../tutorials/getting-started/04-compose-your-first-artifact.md) - Getting started
- [How to: Use Artifact Composer](../../../how-to/generation/use-artifact-composer.md) - Common patterns
- [How to: Composition Strategies](../../../how-to/generation/composition-strategies.md) - Strategy details
- [How to: Artifact Dependencies](../../../how-to/generation/artifact-dependencies.md) - Dependency management
- [ConfigLoader API Reference](config-loader.md) - Underlying config loading
- [Config-Driven Architecture](../../../explanation/architecture/config-driven-architecture.md) - Design philosophy
