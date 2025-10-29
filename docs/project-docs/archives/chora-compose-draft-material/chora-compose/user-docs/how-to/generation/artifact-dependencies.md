# How to Manage Artifact Dependencies

> **Goal:** Track and document relationships between artifacts, content, requirements, and code.

## When to Use This

You need artifact dependencies when:
- Tracking which artifacts document which code
- Managing relationships between artifacts
- Linking generated docs to requirements
- Understanding artifact dependency graphs
- Maintaining traceability in complex systems

## Prerequisites

- Understanding of artifact configs
- Familiarity with artifact structure
- Basic understanding of dependency concepts

---

## Solution

### Quick Version

Add dependencies to your artifact config:

```json
{
  "type": "artifact",
  "id": "api-docs-artifact",
  "dependencies": [
    {
      "id": "api-implementation",
      "type": "code_module",
      "locator": "src/api/routes.py",
      "relationship": "documents"
    }
  ]
}
```

### Understanding Dependencies

**Dependencies answer questions like:**
- What code does this artifact document?
- Which requirements does this artifact implement?
- What other artifacts does this one depend on?
- What external systems are referenced?

**Dependency structure:**
```json
{
  "id": "unique-dep-id",
  "type": "dependency-type",
  "locator": "where-to-find-it",
  "relationship": "how-they-relate",
  "notes": "optional explanation"
}
```

---

## Detailed Steps

### Step 1: Identify Dependency Types

**Available types:**

1. **`artifact`** - Another Chora Compose artifact
2. **`external_system`** - External tool/service
3. **`requirement`** - User story, ticket, spec
4. **`code_module`** - Source code file/module

### Step 2: Define Relationship Types

**Available relationships:**

1. **`tests`** - This artifact tests the dependency
2. **`implements`** - This artifact implements the dependency
3. **`documents`** - This artifact documents the dependency
4. **`based_on`** - This artifact is based on the dependency
5. **`related_to`** - General relationship

### Step 3: Add Dependencies to Config

```json
{
  "type": "artifact",
  "id": "user-guide-artifact",
  "metadata": {
    "type": "documentation",
    "title": "User Guide"
  },
  "dependencies": [
    {
      "id": "user-stories",
      "type": "requirement",
      "locator": "JIRA-PROJECT-123",
      "relationship": "implements",
      "notes": "Implements user stories from sprint 5"
    },
    {
      "id": "main-app",
      "type": "code_module",
      "locator": "src/app/main.py",
      "relationship": "documents",
      "notes": "Documents the main application entry point"
    },
    {
      "id": "api-reference",
      "type": "artifact",
      "locator": "api-reference-artifact",
      "relationship": "related_to",
      "notes": "Companion API documentation"
    }
  ]
}
```

---

## Common Patterns

### Pattern: Documentation → Code Traceability

Link documentation to the code it describes:

```json
{
  "id": "api-docs-artifact",
  "dependencies": [
    {
      "id": "auth-module",
      "type": "code_module",
      "locator": "src/auth/handlers.py",
      "relationship": "documents",
      "notes": "Documents authentication endpoints"
    },
    {
      "id": "user-module",
      "type": "code_module",
      "locator": "src/users/models.py",
      "relationship": "documents",
      "notes": "Documents user data models"
    },
    {
      "id": "api-routes",
      "type": "code_module",
      "locator": "src/api/routes.py",
      "relationship": "documents",
      "notes": "Documents all API routes"
    }
  ]
}
```

**Use case:** Maintain docs in sync with code, identify stale docs

### Pattern: Test Artifact → Code Under Test

Link test suites to what they test:

```json
{
  "id": "integration-tests-artifact",
  "metadata": {
    "type": "test"
  },
  "dependencies": [
    {
      "id": "api-server",
      "type": "code_module",
      "locator": "src/api/server.py",
      "relationship": "tests",
      "notes": "Integration tests for API server"
    },
    {
      "id": "database-layer",
      "type": "code_module",
      "locator": "src/db/connection.py",
      "relationship": "tests",
      "notes": "Tests database connections and queries"
    }
  ]
}
```

**Use case:** Test coverage tracking, impact analysis

### Pattern: Implementation → Requirements

Link generated artifacts to requirements:

```json
{
  "id": "feature-x-artifact",
  "dependencies": [
    {
      "id": "user-story-456",
      "type": "requirement",
      "locator": "JIRA-PROJ-456",
      "relationship": "implements",
      "notes": "Implements user story: As a user, I want to..."
    },
    {
      "id": "spec-document",
      "type": "requirement",
      "locator": "specs/feature-x.md",
      "relationship": "based_on",
      "notes": "Based on technical specification for Feature X"
    }
  ]
}
```

**Use case:** Requirements traceability, compliance

### Pattern: Artifact Composition Chain

Link artifacts that build on each other:

```json
{
  "id": "full-documentation-artifact",
  "dependencies": [
    {
      "id": "api-reference",
      "type": "artifact",
      "locator": "api-reference-artifact",
      "relationship": "based_on",
      "notes": "Includes API reference as a section"
    },
    {
      "id": "user-guide",
      "type": "artifact",
      "locator": "user-guide-artifact",
      "relationship": "based_on",
      "notes": "Includes user guide as a section"
    },
    {
      "id": "tutorials",
      "type": "artifact",
      "locator": "tutorials-artifact",
      "relationship": "based_on",
      "notes": "Includes tutorials as appendix"
    }
  ]
}
```

**Use case:** Complex document assembly, versioning

### Pattern: External System Integration

Link to external tools and services:

```json
{
  "id": "deployment-docs-artifact",
  "dependencies": [
    {
      "id": "kubernetes-cluster",
      "type": "external_system",
      "locator": "https://k8s.example.com",
      "relationship": "documents",
      "notes": "Documents deployment to production K8s cluster"
    },
    {
      "id": "ci-cd-pipeline",
      "type": "external_system",
      "locator": "https://github.com/org/repo/actions",
      "relationship": "documents",
      "notes": "Documents CI/CD workflow configuration"
    },
    {
      "id": "monitoring-system",
      "type": "external_system",
      "locator": "https://grafana.example.com/dashboards",
      "relationship": "related_to",
      "notes": "Related monitoring dashboards"
    }
  ]
}
```

**Use case:** DevOps documentation, system architecture docs

---

## Querying Dependencies

**Currently:** Dependencies are metadata only - not actively used by composer.

**You can read them programmatically:**

```python
from chora_compose.core.config_loader import ConfigLoader

loader = ConfigLoader()
artifact = loader.load_artifact_config("my-artifact")

# List all dependencies
print(f"Artifact: {artifact.id}")
print(f"Dependencies: {len(artifact.dependencies or [])}")

for dep in (artifact.dependencies or []):
    print(f"\n- {dep.id}")
    print(f"  Type: {dep.type}")
    print(f"  Locator: {dep.locator}")
    print(f"  Relationship: {dep.relationship}")
    if dep.notes:
        print(f"  Notes: {dep.notes}")
```

**Example output:**
```
Artifact: api-docs-artifact
Dependencies: 3

- auth-module
  Type: code_module
  Locator: src/auth/handlers.py
  Relationship: documents
  Notes: Documents authentication endpoints

- user-stories
  Type: requirement
  Locator: JIRA-PROJ-123
  Relationship: implements

- api-reference
  Type: artifact
  Locator: api-reference-artifact
  Relationship: related_to
```

---

## Advanced Usage

### Building a Dependency Graph

```python
from chora_compose.core.config_loader import ConfigLoader
from pathlib import Path
from typing import Set, Dict, List

def build_dependency_graph(artifact_ids: List[str]) -> Dict[str, Set[str]]:
    """Build dependency graph for artifacts."""
    loader = ConfigLoader()
    graph = {}

    for artifact_id in artifact_ids:
        artifact = loader.load_artifact_config(artifact_id)
        deps = set()

        for dep in (artifact.dependencies or []):
            if dep.type == "artifact":
                deps.add(dep.locator)

        graph[artifact_id] = deps

    return graph

# Use it
artifacts = ["readme", "api-docs", "user-guide"]
graph = build_dependency_graph(artifacts)

# Print dependencies
for artifact, deps in graph.items():
    print(f"{artifact}:")
    for dep in deps:
        print(f"  → {dep}")
```

### Finding Reverse Dependencies

```python
def find_reverse_dependencies(
    target: str,
    artifact_ids: List[str]
) -> List[str]:
    """Find artifacts that depend on target."""
    loader = ConfigLoader()
    dependents = []

    for artifact_id in artifact_ids:
        artifact = loader.load_artifact_config(artifact_id)

        for dep in (artifact.dependencies or []):
            if dep.locator == target:
                dependents.append(artifact_id)
                break

    return dependents

# Use it
code_file = "src/api/routes.py"
artifacts_documenting_it = find_reverse_dependencies(
    code_file,
    ["api-docs", "user-guide", "integration-tests"]
)

print(f"Artifacts that reference {code_file}:")
for artifact in artifacts_documenting_it:
    print(f"  - {artifact}")
```

### Dependency Impact Analysis

```python
def analyze_code_impact(code_file: str, artifact_ids: List[str]):
    """Analyze which artifacts might be affected by code changes."""
    loader = ConfigLoader()

    print(f"Impact analysis for: {code_file}\n")

    for artifact_id in artifact_ids:
        artifact = loader.load_artifact_config(artifact_id)

        for dep in (artifact.dependencies or []):
            if dep.type == "code_module" and dep.locator == code_file:
                print(f"⚠ {artifact_id}")
                print(f"  Relationship: {dep.relationship}")
                print(f"  Output: {artifact.metadata.outputs[0].file}")
                if dep.notes:
                    print(f"  Notes: {dep.notes}")
                print()

# Use it
analyze_code_impact("src/api/routes.py", all_artifact_ids)
```

**Output:**
```
Impact analysis for: src/api/routes.py

⚠ api-docs-artifact
  Relationship: documents
  Output: docs/API.md
  Notes: Documents all API routes

⚠ integration-tests-artifact
  Relationship: tests
  Output: tests/test_api_integration.py
  Notes: Integration tests for API endpoints
```

---

## Best Practices

### 1. Be Specific with Locators

**Good:**
```json
{
  "type": "code_module",
  "locator": "src/api/v2/users/handlers.py:UserHandler"
}
```

**Better:**
```json
{
  "type": "code_module",
  "locator": "src/api/v2/users/handlers.py:UserHandler.create_user"
}
```

Specific locators help with:
- Precise impact analysis
- Accurate traceability
- Better tooling integration

### 2. Use Consistent ID Naming

**Good pattern:**
```json
[
  {"id": "auth-module", "locator": "src/auth/..."},
  {"id": "user-module", "locator": "src/users/..."},
  {"id": "api-module", "locator": "src/api/..."}
]
```

Consistent naming makes dependencies easier to understand and search.

### 3. Document the Relationship

Always include `notes` for complex dependencies:

```json
{
  "id": "legacy-system",
  "type": "external_system",
  "locator": "http://legacy.internal.com/api",
  "relationship": "related_to",
  "notes": "This artifact references the legacy API for migration documentation. The legacy system is being phased out in Q4 2025."
}
```

### 4. Keep Dependencies Up to Date

When code moves or requirements change, update dependencies:

```python
# Script to validate dependencies
def validate_dependencies(artifact_id: str):
    """Check if dependencies still exist."""
    loader = ConfigLoader()
    artifact = loader.load_artifact_config(artifact_id)

    for dep in (artifact.dependencies or []):
        if dep.type == "code_module":
            if not Path(dep.locator).exists():
                print(f"⚠ Missing: {dep.locator}")

        elif dep.type == "artifact":
            try:
                loader.load_artifact_config(dep.locator)
            except:
                print(f"⚠ Invalid artifact: {dep.locator}")
```

---

## Future Enhancements (Planned)

### Automated Dependency Discovery

```python
# Future: Scan code and auto-detect dependencies
composer.discover_dependencies(
    artifact_id="api-docs",
    scan_paths=["src/api/"],
    update_config=True
)
```

### Dependency Validation

```python
# Future: Validate dependencies exist and are accessible
composer.validate_dependencies("my-artifact")
```

### Dependency Visualization

```bash
# Future: Generate dependency graphs
chora-compose deps graph --artifact my-artifact --output deps.png
```

---

## Troubleshooting

**Problem:** Can't find where dependencies are used
**Solution:**
- Dependencies are currently documentation/metadata only
- Use scripts to query and analyze them
- Wait for tooling features (future)

**Problem:** Dependencies getting stale
**Solution:**
- Set up validation scripts in CI/CD
- Regular dependency audits
- Update during code reviews

**Problem:** Complex dependency graph is confusing
**Solution:**
- Use clear, descriptive IDs
- Add comprehensive notes
- Build visualization tools
- Simplify artifact structure if possible

**Problem:** Want to enforce dependency rules
**Solution:**
- Currently no validation built-in
- Build custom validation scripts
- Use pre-commit hooks
- Wait for dependency validation feature (future)

---

## See Also

- [How to: Use Artifact Composer](use-artifact-composer.md) - Basic usage
- [How to: Composition Strategies](composition-strategies.md) - Content assembly
- [Tutorial: Compose Your First Artifact](../../tutorials/getting-started/04-compose-your-first-artifact.md) - Getting started
- [ArtifactComposer API Reference](../../reference/api/core/artifact-composer.md) - Technical details
- [Config-Driven Architecture](../../explanation/architecture/config-driven-architecture.md) - Design philosophy
