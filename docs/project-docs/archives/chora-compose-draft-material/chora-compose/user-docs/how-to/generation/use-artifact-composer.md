# How to Use the Artifact Composer

> **Goal:** Assemble complete artifacts from multiple content configurations efficiently.

## When to Use This

You need the ArtifactComposer when:
- Combining multiple content sections into one output file
- Building complete documents from reusable parts
- Managing complex multi-section artifacts
- Generating consistent structured output
- Automating document assembly workflows

## Prerequisites

- Chora Compose installed via Poetry
- At least one artifact configuration created
- Multiple content configurations available
- Completed [Tutorial: Compose Your First Artifact](../../tutorials/getting-started/04-compose-your-first-artifact.md)

---

## Solution

### Quick Version

```python
from chora_compose.core.composer import ArtifactComposer

# Create composer and assemble
composer = ArtifactComposer()
output_path = composer.assemble("my-artifact")

print(f"✓ Generated: {output_path}")
```

### Detailed Steps

#### 1. Set Up Your Artifact Config

Create an artifact configuration that references content configs:

```json
{
  "type": "artifact",
  "id": "documentation-artifact",
  "schemaRef": {
    "uri": "file://schemas/artifact/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "type": "documentation",
    "version": "1.0",
    "title": "Complete Documentation",
    "purpose": "Assemble all documentation sections",
    "outputs": [
      {
        "file": "docs/COMPLETE.md",
        "format": "markdown"
      }
    ],
    "compositionStrategy": "concat"
  },
  "content": {
    "children": [
      {
        "id": "intro",
        "path": "content/intro/intro-content.json",
        "required": true,
        "order": 1
      },
      {
        "id": "usage",
        "path": "content/usage/usage-content.json",
        "required": true,
        "order": 2
      },
      {
        "id": "api",
        "path": "content/api/api-content.json",
        "required": true,
        "order": 3
      }
    ]
  }
}
```

#### 2. Assemble the Artifact

```python
from chora_compose.core.composer import ArtifactComposer

# Create composer instance
composer = ArtifactComposer()

# Assemble by artifact ID
output_path = composer.assemble("documentation-artifact")

print(f"✓ Artifact generated at: {output_path}")
print(f"✓ Size: {output_path.stat().st_size} bytes")
```

#### 3. Read the Generated Output

```python
# Read and verify the output
content = output_path.read_text(encoding="utf-8")
print(f"Generated {len(content)} characters")
print("\nPreview:")
print(content[:500])
```

---

## Common Patterns

### Pattern: Simple Document Assembly

Combine multiple markdown sections:

```python
from pathlib import Path
from chora_compose.core.composer import ArtifactComposer

def assemble_documentation(artifact_id: str = "docs-artifact") -> Path:
    """Assemble complete documentation."""
    composer = ArtifactComposer()
    return composer.assemble(artifact_id)

# Use it
output = assemble_documentation()
print(f"Documentation generated: {output}")
```

**Use case:** README files, API documentation, user guides

### Pattern: Batch Assembly

Generate multiple artifacts in one run:

```python
from chora_compose.core.composer import ArtifactComposer

def batch_assemble(artifact_ids: list[str]) -> dict[str, Path]:
    """Assemble multiple artifacts."""
    composer = ArtifactComposer()  # Reuse instance
    results = {}

    for artifact_id in artifact_ids:
        try:
            output_path = composer.assemble(artifact_id)
            results[artifact_id] = output_path
            print(f"✓ {artifact_id}: {output_path}")
        except Exception as e:
            print(f"✗ {artifact_id}: {e}")
            results[artifact_id] = None

    return results

# Use it
artifacts = ["readme", "api-docs", "user-guide"]
outputs = batch_assemble(artifacts)

# Check results
successful = [aid for aid, path in outputs.items() if path]
print(f"\n✓ Successfully generated {len(successful)} artifacts")
```

**Use case:** CI/CD documentation generation, batch updates

### Pattern: Custom Output Path

Override the output location:

```python
from pathlib import Path
from chora_compose.core.composer import ArtifactComposer

def assemble_to_custom_location(
    artifact_id: str,
    output_dir: Path
) -> Path:
    """Assemble artifact to custom directory."""
    composer = ArtifactComposer()

    # Generate custom output path
    output_path = output_dir / f"{artifact_id}.md"

    # Assemble with override
    result_path = composer.assemble(
        artifact_id,
        output_override=output_path
    )

    return result_path

# Use it
custom_dir = Path("build/docs")
custom_dir.mkdir(parents=True, exist_ok=True)

output = assemble_to_custom_location("readme", custom_dir)
print(f"Generated at custom location: {output}")
```

**Use case:** Build systems, custom directory structures

### Pattern: Error-Tolerant Assembly

Handle optional content gracefully:

```python
from chora_compose.core.composer import ArtifactComposer, CompositionError

def safe_assemble(artifact_id: str) -> Path | None:
    """Assemble artifact with error handling."""
    composer = ArtifactComposer()

    try:
        output_path = composer.assemble(artifact_id)
        print(f"✓ Success: {output_path}")
        return output_path

    except CompositionError as e:
        if "required content" in str(e):
            print(f"✗ Missing required content: {e}")
        elif "output file" in str(e):
            print(f"✗ Could not write output: {e}")
        else:
            print(f"✗ Composition failed: {e}")
        return None

# Use it with fallback
output = safe_assemble("my-artifact")
if output:
    print(f"Processing {output}...")
else:
    print("Using cached version instead")
```

**Use case:** Robust CI/CD pipelines, production systems

### Pattern: Custom ConfigLoader

Use a custom loader with different directories:

```python
from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.core.composer import ArtifactComposer

def assemble_from_custom_dirs(
    artifact_id: str,
    config_dir: Path,
    schema_dir: Path
) -> Path:
    """Assemble using custom config/schema directories."""
    # Create custom loader
    loader = ConfigLoader(
        schema_dir=schema_dir,
        config_dir=config_dir
    )

    # Create composer with custom loader
    composer = ArtifactComposer(config_loader=loader)

    # Assemble
    return composer.assemble(artifact_id)

# Use it
output = assemble_from_custom_dirs(
    "my-artifact",
    config_dir=Path("custom/configs"),
    schema_dir=Path("custom/schemas")
)
```

**Use case:** Multi-project setups, testing with fixtures

### Pattern: Programmatic Content Order

Dynamically control section ordering:

While you can't change the artifact config at runtime, you can:

1. **Pre-generate variants:**
```bash
# Create multiple artifact configs with different orders
configs/artifacts/report-summary.json    # Brief version
configs/artifacts/report-full.json       # Complete version
configs/artifacts/report-technical.json  # Technical deep-dive
```

2. **Select at runtime:**
```python
def assemble_report(variant: str = "full") -> Path:
    """Assemble report variant."""
    artifact_id = f"report-{variant}"
    composer = ArtifactComposer()
    return composer.assemble(artifact_id)

# Use it
summary = assemble_report("summary")
full = assemble_report("full")
technical = assemble_report("technical")
```

**Use case:** Multiple report formats, audience-specific docs

---

## Real-World Example

**Scenario:** Generate API documentation for a REST API with multiple sections

**Directory structure:**
```
configs/
  content/
    api-overview/api-overview-content.json
    api-auth/api-auth-content.json
    api-endpoints/api-endpoints-content.json
    api-errors/api-errors-content.json
  artifacts/
    api-docs-artifact.json
```

**Artifact config:**
```json
{
  "type": "artifact",
  "id": "api-docs-artifact",
  "metadata": {
    "type": "documentation",
    "title": "REST API Documentation",
    "outputs": [{"file": "docs/API.md", "format": "markdown"}],
    "compositionStrategy": "concat"
  },
  "content": {
    "children": [
      {"id": "api-overview", "path": "content/api-overview/api-overview-content.json", "order": 1},
      {"id": "api-auth", "path": "content/api-auth/api-auth-content.json", "order": 2},
      {"id": "api-endpoints", "path": "content/api-endpoints/api-endpoints-content.json", "order": 3},
      {"id": "api-errors", "path": "content/api-errors/api-errors-content.json", "order": 4}
    ]
  }
}
```

**Assembly script:**
```python
from pathlib import Path
from chora_compose.core.composer import ArtifactComposer
from datetime import datetime

def generate_api_docs() -> Path:
    """Generate complete API documentation."""
    composer = ArtifactComposer()

    print("Generating API documentation...")
    start = datetime.now()

    output_path = composer.assemble("api-docs-artifact")

    elapsed = (datetime.now() - start).total_seconds()
    size = output_path.stat().st_size

    print(f"✓ Generated: {output_path}")
    print(f"✓ Size: {size:,} bytes")
    print(f"✓ Time: {elapsed:.2f}s")

    return output_path

if __name__ == "__main__":
    docs_path = generate_api_docs()

    # Verify output
    content = docs_path.read_text()
    print(f"\n✓ Verified {len(content):,} characters")

    # Check sections present
    required_sections = ["# API Overview", "## Authentication", "## Endpoints", "## Error Codes"]
    missing = [s for s in required_sections if s not in content]

    if missing:
        print(f"⚠ Missing sections: {missing}")
    else:
        print("✓ All sections present")
```

**Output:**
```
Generating API documentation...
✓ Generated: docs/API.md
✓ Size: 15,234 bytes
✓ Time: 0.35s

✓ Verified 15,234 characters
✓ All sections present
```

---

## Advanced Usage

### Reusing Composer Instance

For performance, reuse the composer:

```python
# Good: Reuse composer
composer = ArtifactComposer()
for artifact_id in artifact_ids:
    output = composer.assemble(artifact_id)

# Less efficient: Create new composer each time
for artifact_id in artifact_ids:
    composer = ArtifactComposer()  # Unnecessary
    output = composer.assemble(artifact_id)
```

The composer reuses its ConfigLoader (which caches schemas), making subsequent assemblies faster.

### Programmatic Artifact Assembly

Build artifacts without config files:

**Note:** This is not directly supported - artifacts must have configs. However, you can:

1. **Generate configs programmatically:**
```python
import json
from pathlib import Path

def create_dynamic_artifact_config(sections: list[str]) -> Path:
    """Create artifact config from section list."""
    children = [
        {
            "id": section,
            "path": f"content/{section}/{section}-content.json",
            "required": True,
            "order": i + 1
        }
        for i, section in enumerate(sections)
    ]

    config = {
        "type": "artifact",
        "id": "dynamic-artifact",
        "metadata": {
            "type": "documentation",
            "outputs": [{"file": "output/dynamic.md"}],
            "compositionStrategy": "concat"
        },
        "content": {"children": children}
    }

    # Write config
    config_path = Path("configs/artifacts/dynamic-artifact.json")
    config_path.write_text(json.dumps(config, indent=2))

    return config_path

# Use it
sections = ["intro", "features", "usage"]
config_path = create_dynamic_artifact_config(sections)

# Now assemble
composer = ArtifactComposer()
output = composer.assemble("dynamic-artifact")
```

2. **Template-based config generation:**
Use Jinja2 to generate artifact configs from templates.

---

## Troubleshooting

**Problem:** `CompositionError: Failed to load artifact config`
**Solution:**
- Verify artifact config exists at `configs/artifacts/{id}.json`
- Check JSON syntax with `python -m json.tool config.json`
- Ensure `schemaRef` points to correct schema

**Problem:** `CompositionError: Content config not found`
**Solution:**
- Check `path` in children array is correct
- Paths are relative to project root or `configs/`
- Use `content/{name}/{name}-content.json` pattern
- Verify content config files exist

**Problem:** `CompositionError: Failed to generate required content`
**Solution:**
- Load content config independently to isolate issue
- Check content has valid generation patterns
- If content is truly optional, set `required: false`
- Review content config for validation errors

**Problem:** Empty output file generated
**Solution:**
- Verify content configs have `example_output` populated
- Check generation patterns are defined
- Ensure composition strategy is supported (`concat` currently)
- Test each content config independently

**Problem:** Sections in wrong order
**Solution:**
- Check `order` values in children array (lower = earlier)
- Ensure all children have `order` specified (default is 0)
- Gaps in ordering are fine (can use 10, 20, 30)

**Problem:** `CompositionError: No generator available for type`
**Solution:**
- Currently only `demonstration` type is supported
- Register custom generators with `composer.register_generator()`
- Check content pattern `type` field spelling

**Problem:** Output path permission denied
**Solution:**
- Ensure output directory exists and is writable
- Check parent directories are writable
- Try with `output_override` to different location

**Problem:** Performance is slow
**Solution:**
- Reuse composer instance across multiple assemblies
- ConfigLoader caches schemas automatically
- Consider batch assembly for multiple artifacts
- Profile to find bottleneck (usually file I/O)

---

## Performance Tips

**Measure assembly time:**
```python
import time

start = time.time()
output = composer.assemble("large-artifact")
elapsed = time.time() - start

print(f"Assembly took {elapsed:.2f}s")
```

**Optimize for repeated assemblies:**
```python
# One-time setup
composer = ArtifactComposer()

# Fast repeated assemblies
for artifact_id in many_artifacts:
    output = composer.assemble(artifact_id)  # Reuses cached schemas
```

**Parallel assembly (if needed):**
```python
from concurrent.futures import ThreadPoolExecutor

def assemble_one(artifact_id: str) -> Path:
    composer = ArtifactComposer()
    return composer.assemble(artifact_id)

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(assemble_one, artifact_ids))
```

---

## See Also

- [Tutorial: Compose Your First Artifact](../../tutorials/getting-started/04-compose-your-first-artifact.md) - Learn the basics
- [How to: Composition Strategies](composition-strategies.md) - Different assembly methods
- [How to: Artifact Dependencies](artifact-dependencies.md) - Track relationships
- [ArtifactComposer API Reference](../../reference/api/core/artifact-composer.md) - Complete API
- [Config-Driven Architecture](../../explanation/architecture/config-driven-architecture.md) - Design philosophy
