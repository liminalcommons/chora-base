# JSON Schema Validators

This directory contains JSON Schema validators for chora ecosystem capability manifests.

## Purpose

JSON Schema validators ensure capability manifests (YAML files) comply with the unified ontology standards:

- **Namespace format** validation (`chora.domain.capability`)
- **Required fields** enforcement (Dublin Core metadata)
- **Type-specific** validation (Service vs Pattern)
- **Dependency constraints** validation (SemVer)
- **Cross-type relationships** validation

## Schema Files

### 1. capability-common.schema.json

**Purpose**: Shared definitions for both Service-type and Pattern-type capabilities

**Contains**:
- Namespace format regex (`chora.domain.capability`)
- SemVer format and constraint patterns
- ISO 8601 date validation
- Dublin Core metadata fields (15 core elements)
- Dependency structures
- SKOS taxonomy relationships
- Adoption metadata (chora_adoption)

**Usage**: Referenced by Service and Pattern schemas via `$ref`

---

### 2. capability-service.schema.json

**Purpose**: Service-type capability validation

**Validates**:
- `dc_type: "Service"` (required)
- `dc_format: "application/x-executable"` (required)
- `chora_service` specification (required):
  - **interfaces**: At least one interface (CLI/REST/MCP)
  - **health**: Health check configuration
  - **distribution**: PyPI package and Docker image

**Required Fields**:
```yaml
metadata:
  dc_type: "Service"
  dc_format: "application/x-executable"

spec:
  chora_service:
    interfaces: [...]  # At least 1
    health: {...}
    distribution: {...}
```

---

### 3. capability-pattern.schema.json

**Purpose**: Pattern-type capability validation

**Validates**:
- `dc_type: "Pattern"` (required)
- `dc_format: "text/markdown"` (required)
- `chora_pattern` specification (required):
  - **artifacts**: Exactly 5 SAP artifacts (all types present)

**Required Fields**:
```yaml
metadata:
  dc_type: "Pattern"
  dc_format: "text/markdown"

spec:
  chora_pattern:
    artifacts:  # Exactly 5 items
      - type: capability-charter
      - type: protocol-spec
      - type: awareness-guide
      - type: adoption-blueprint
      - type: ledger
```

**Artifact Validation**:
- Exactly 5 artifacts (no more, no less)
- All 5 types must be present (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger)
- Paths must match pattern: `docs/skilled-awareness/{domain}/{file}.md`

---

## Usage

### Validation Script (Week 3 Deliverable)

```bash
# Validate single capability manifest
python scripts/validate-capability.py capabilities/chora.react.form_validation.yaml

# Validate all capability manifests
python scripts/validate-all-capabilities.py capabilities/

# Validate with verbose output
python scripts/validate-capability.py capabilities/chora.registry.lookup.yaml --verbose
```

### Pre-Commit Hook (Week 3 Deliverable)

The pre-commit hook automatically validates capability manifests on commit:

```bash
# Install pre-commit hook
pre-commit install

# Run manually
pre-commit run validate-capabilities --all-files
```

**Hook Configuration** (`.pre-commit-config.yaml`):
```yaml
repos:
  - repo: local
    hooks:
      - id: validate-capabilities
        name: Validate Capability Manifests
        entry: python scripts/validate-capability.py
        language: python
        files: ^capabilities/.*\.yaml$
        additional_dependencies:
          - jsonschema>=4.0.0
          - pyyaml>=6.0.0
```

### CI/CD Workflow (Week 3 Deliverable)

GitHub Actions workflow validates manifests on pull requests:

```yaml
name: Validate Capabilities

on:
  pull_request:
    paths:
      - 'capabilities/**/*.yaml'
      - 'schemas/**/*.json'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install jsonschema pyyaml
      - name: Validate capability manifests
        run: |
          python scripts/validate-all-capabilities.py capabilities/
```

---

## Validation Examples

### Example 1: Valid Service-Type Manifest

```yaml
apiVersion: chora.dev/v1
kind: Capability

metadata:
  dc_identifier: chora.registry.lookup
  dc_title: "Service Registry & Discovery"
  dc_description: "Service mesh with capability discovery"
  dc_type: "Service"
  dc_hasVersion: "1.0.0"
  dc_format: "application/x-executable"

status: pilot

spec:
  chora_service:
    interfaces:
      - type: cli
        command: chora-registry
        entrypoint: chora.registry.cli:main
    health:
      endpoint: /health
      interval: 10s
    distribution:
      pypi_package: chora-registry
```

**Validation**: ✅ PASS

---

### Example 2: Valid Pattern-Type Manifest

```yaml
apiVersion: chora.dev/v1
kind: Capability

metadata:
  dc_identifier: chora.react.form_validation
  dc_title: "React Form Validation Patterns"
  dc_description: "React Hook Form + Zod validation patterns"
  dc_type: "Pattern"
  dc_hasVersion: "1.0.0"
  dc_format: "text/markdown"

status: pilot

spec:
  chora_pattern:
    artifacts:
      - type: capability-charter
        path: docs/skilled-awareness/react-form-validation/capability-charter.md
      - type: protocol-spec
        path: docs/skilled-awareness/react-form-validation/protocol-spec.md
      - type: awareness-guide
        path: docs/skilled-awareness/react-form-validation/awareness-guide.md
      - type: adoption-blueprint
        path: docs/skilled-awareness/react-form-validation/adoption-blueprint.md
      - type: ledger
        path: docs/skilled-awareness/react-form-validation/ledger.md
```

**Validation**: ✅ PASS

---

### Example 3: Invalid Namespace

```yaml
metadata:
  dc_identifier: chora.InvalidDomain.capability  # Invalid: not in domain taxonomy
```

**Validation**: ❌ FAIL
**Error**: `dc_identifier does not match pattern ^chora\.[a-z_]+\.[a-z0-9_]{1,50}$`

---

### Example 4: Invalid SemVer

```yaml
metadata:
  dc_hasVersion: "v1.0.0"  # Invalid: should be "1.0.0" (no 'v' prefix)
```

**Validation**: ❌ FAIL
**Error**: `dc_hasVersion does not match SemVer pattern`

---

### Example 5: Missing Required Fields (Service)

```yaml
spec:
  chora_service:
    interfaces:
      - type: cli
        command: chora-test
    # Missing: health and distribution
```

**Validation**: ❌ FAIL
**Error**: `Missing required properties: health, distribution`

---

### Example 6: Missing Artifacts (Pattern)

```yaml
spec:
  chora_pattern:
    artifacts:
      - type: capability-charter
        path: docs/skilled-awareness/test/capability-charter.md
      # Missing: 4 other required artifacts
```

**Validation**: ❌ FAIL
**Error**: `artifacts array must have exactly 5 items (has 1)`

---

## Common Validation Errors

### Namespace Errors

**Error**: `dc_identifier does not match pattern`

**Fix**: Use `chora.{domain}.{capability}` format with lowercase, snake_case

**Example**:
```yaml
# ❌ Wrong
dc_identifier: Chora.Registry.Lookup

# ✅ Correct
dc_identifier: chora.registry.lookup
```

---

### SemVer Errors

**Error**: `dc_hasVersion does not match SemVer pattern`

**Fix**: Use SemVer 2.0.0 format: `MAJOR.MINOR.PATCH`

**Example**:
```yaml
# ❌ Wrong
dc_hasVersion: "v1.0.0"
dc_hasVersion: "1.0"

# ✅ Correct
dc_hasVersion: "1.0.0"
dc_hasVersion: "2.3.1"
dc_hasVersion: "1.0.0-beta.1"
```

---

### Type Mismatch Errors

**Error**: `dc_type must be 'Service' but dc_format is 'text/markdown'`

**Fix**: Ensure `dc_type` and `dc_format` match

**Example**:
```yaml
# ❌ Wrong
dc_type: "Service"
dc_format: "text/markdown"  # Should be application/x-executable

# ✅ Correct
dc_type: "Service"
dc_format: "application/x-executable"
```

---

### Dependency Errors

**Error**: `version constraint does not match SemVer pattern`

**Fix**: Use valid SemVer operators: `^`, `~`, `>=`, `>`, `<=`, `<`

**Example**:
```yaml
# ❌ Wrong
dc_relation:
  requires:
    - capability: chora.react.foundation
      version: "1.0.0+"  # Invalid operator

# ✅ Correct
dc_relation:
  requires:
    - capability: chora.react.foundation
      version: "^1.0.0"  # Caret range
```

---

## Development

### Adding New Validation Rules

1. **Update common schema** (`capability-common.schema.json`):
   - Add new shared definitions
   - Update metadata_common if adding Dublin Core fields

2. **Update type-specific schema**:
   - Service: `capability-service.schema.json`
   - Pattern: `capability-pattern.schema.json`

3. **Test validation**:
   ```bash
   python scripts/validate-capability.py capabilities/SCHEMA-EXAMPLES.yaml
   ```

4. **Update documentation**:
   - This README
   - `docs/ontology/dublin-core-schema.md`

---

### Testing Schemas

```bash
# Install JSON Schema validator
pip install jsonschema pyyaml

# Validate schema itself (meta-validation)
jsonschema -i schemas/capability-service.schema.json http://json-schema.org/draft-07/schema#

# Test against example manifest
python -c "
import json
import yaml
from jsonschema import validate

with open('capabilities/SCHEMA-EXAMPLES.yaml') as f:
    manifest = yaml.safe_load(f)

with open('schemas/capability-service.schema.json') as f:
    schema = json.load(f)

validate(instance=manifest, schema=schema)
print('✅ Validation passed')
"
```

---

## Related Documentation

- **Dublin Core Schema**: [docs/ontology/dublin-core-schema.md](../docs/ontology/dublin-core-schema.md)
- **Namespace Spec**: [docs/ontology/namespace-spec.md](../docs/ontology/namespace-spec.md)
- **Capability Types**: [docs/ontology/capability-types.md](../docs/ontology/capability-types.md)
- **Migration Guide**: [docs/ontology/migration-guide.md](../docs/ontology/migration-guide.md)

---

## Version History

- **1.0.0** (2025-11-15): Initial JSON Schema validators
  - Common schema with shared definitions
  - Service-type schema with interface/health/distribution validation
  - Pattern-type schema with 5-artifact validation
  - Complete validation examples and error reference

---

**Status**: Schemas complete ✅ | Validation scripts pending ⏳ (Week 3 deliverable)
**Last Updated**: 2025-11-15
