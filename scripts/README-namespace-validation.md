# Namespace Validation Hook

**Version**: 1.0.0
**Status**: Active
**Part of**: Ecosystem Ontology & Composition Vision - Phase 1, Week 3

---

## Overview

The namespace validation hook ensures all capability YAML manifests comply with the chora ecosystem ontology specification. It validates namespace format, domain validity, uniqueness, and SemVer compliance automatically on every commit.

**Implemented in**: ONT-009 (Week 3.1)

---

## Features

### 1. Format Validation

Ensures namespaces match the required pattern:

```regex
^chora\.[a-z_]+\.[a-z0-9_]{1,50}$
```

**Examples**:
- ✅ `chora.registry.lookup` (valid)
- ✅ `chora.react.form_validation` (valid)
- ❌ `chora.Registry.Lookup` (uppercase not allowed)
- ❌ `chora.react.formValidation` (camelCase not allowed)
- ❌ `registry.lookup` (missing `chora` prefix)

### 2. Domain Validation

Verifies the domain component exists in [docs/ontology/domain-taxonomy.md](../docs/ontology/domain-taxonomy.md).

**Valid Domains** (21 total):
- `infrastructure`, `registry`, `bootstrap`, `devex`, `interface`, `composition`
- `templates`, `react`, `vue`, `angular`, `awareness`, `workflow`, `integration`
- `optimization`, `database`, `security`, `monitoring`, `mobile`, `desktop`, `api`
- `domain` (reserved for testing)

**Error Example**:
```
[DOMAIN_INVALID] Domain 'invalid_domain' in namespace 'chora.invalid_domain.test'
is not defined in domain-taxonomy.md.
Valid domains: ['angular', 'api', 'awareness', ...]
```

### 3. Uniqueness Validation

Detects duplicate namespaces across all `capabilities/*.yaml` files.

**Error Example**:
```
[NAMESPACE_DUPLICATE] Duplicate namespace 'chora.registry.lookup' found.
Already defined in: capabilities/chora.registry.lookup.yaml
```

### 4. Version Validation

Validates `dc_hasVersion` field uses valid SemVer 2.0.0 format.

**Valid Versions**:
- ✅ `1.0.0`
- ✅ `2.3.1`
- ✅ `1.0.0-beta.1`
- ✅ `2.0.0-rc.1+build.123`
- ❌ `1.0` (missing patch version)
- ❌ `v1.0.0` (v prefix not allowed)

---

## Installation

### Prerequisites

```bash
# Python 3.8+
python --version

# PyYAML
pip install PyYAML

# Pre-commit framework
pip install pre-commit
```

### Install Pre-commit Hooks

```bash
# Install git hooks (run once per repository clone)
pre-commit install

# Verify installation
pre-commit --version
```

---

## Usage

### Automatic Validation (Recommended)

Pre-commit runs automatically when you commit:

```bash
git add capabilities/chora.example.capability.yaml
git commit -m "feat(ontology): add example capability"
# Hook runs automatically, blocks commit if validation fails
```

### Manual Validation

**Validate all capabilities**:
```bash
python scripts/validate-namespaces.py capabilities/
```

**Validate specific file**:
```bash
python scripts/validate-namespaces.py capabilities/chora.react.form_validation.yaml
```

**Validate with pre-commit**:
```bash
# Run namespace validation hook only
pre-commit run validate-namespaces --all-files

# Run all hooks
pre-commit run --all-files
```

**Quiet mode** (suppress success output):
```bash
python scripts/validate-namespaces.py capabilities/ --quiet
```

---

## Error Messages and Fixes

### Format Errors

**Error**:
```
[NAMESPACE_FORMAT_INVALID] Namespace 'chora.React.FormValidation' does not match
required format: chora.{domain}.{capability} (lowercase, snake_case, capability 1-50 chars)
```

**Fix**: Use lowercase snake_case:
```yaml
# Before
metadata:
  dc_identifier: chora.React.FormValidation

# After
metadata:
  dc_identifier: chora.react.form_validation
```

### Domain Errors

**Error**:
```
[DOMAIN_INVALID] Domain 'backend' in namespace 'chora.backend.api' is not defined
in domain-taxonomy.md.
```

**Fix**: Use a valid domain (see [domain-taxonomy.md](../docs/ontology/domain-taxonomy.md)):
```yaml
# Before
metadata:
  dc_identifier: chora.backend.api

# After (use 'api' domain)
metadata:
  dc_identifier: chora.api.rest_endpoints
```

### Uniqueness Errors

**Error**:
```
[NAMESPACE_DUPLICATE] Duplicate namespace 'chora.registry.lookup' found.
Already defined in: capabilities/chora.registry.lookup.yaml
```

**Fix**: Choose a unique capability name or modify existing capability:
```yaml
# Option 1: Different capability name
metadata:
  dc_identifier: chora.registry.advanced_lookup

# Option 2: Different domain (if semantically correct)
metadata:
  dc_identifier: chora.infrastructure.lookup
```

### Version Errors

**Error**:
```
[VERSION_FORMAT_INVALID] Version '1.0' for namespace 'chora.registry.lookup' is not
valid SemVer. Expected format: MAJOR.MINOR.PATCH (e.g., '1.0.0', '2.3.1')
```

**Fix**: Use full SemVer format:
```yaml
# Before
metadata:
  dc_hasVersion: "1.0"

# After
metadata:
  dc_hasVersion: "1.0.0"
```

---

## CI/CD Integration

The namespace validation hook is automatically run in CI/CD pipelines via pre-commit.

**GitHub Actions** (future Week 3.2):
```yaml
# .github/workflows/validate-capabilities.yml
- name: Validate Capability Namespaces
  run: pre-commit run validate-namespaces --all-files
```

---

## Development

### Adding New Validation Rules

Edit `scripts/validate-namespaces.py`:

```python
def validate_custom_rule(self, namespace: str, file_path: Path) -> bool:
    """Add new validation logic here"""
    if some_condition:
        self.errors.append(ValidationError(
            file_path,
            "ERROR_TYPE",
            f"Error message: {namespace}",
            namespace
        ))
        return False
    return True
```

### Running Tests

```bash
# Create test files
echo "..." > capabilities/test-valid.yaml
echo "..." > capabilities/test-invalid.yaml

# Run validation
python scripts/validate-namespaces.py capabilities/

# Clean up
rm capabilities/test-*.yaml
```

---

## Troubleshooting

### Hook Not Running

**Symptom**: Pre-commit hook doesn't run on `git commit`

**Fix**:
```bash
# Reinstall hooks
pre-commit install

# Verify .git/hooks/pre-commit exists
ls -la .git/hooks/pre-commit
```

### PyYAML Import Error

**Symptom**:
```
ERROR: PyYAML not installed. Run: pip install PyYAML
```

**Fix**:
```bash
pip install PyYAML

# Or install all project dependencies
pip install -r requirements.txt  # If exists
```

### Domain Taxonomy Not Found

**Symptom**:
```
[DOMAIN_FILE_MISSING] Domain taxonomy file not found: docs/ontology/domain-taxonomy.md
```

**Fix**: Run from repository root or specify path:
```bash
# Option 1: cd to repository root
cd /path/to/chora-base
python scripts/validate-namespaces.py capabilities/

# Option 2: Specify domain taxonomy path
python scripts/validate-namespaces.py capabilities/ \
  --domain-taxonomy docs/ontology/domain-taxonomy.md
```

### Skipping Validation (Emergency Only)

**Skip all hooks** (not recommended):
```bash
git commit --no-verify -m "Emergency commit (skip validation)"
```

**Skip specific hook**:
```bash
SKIP=validate-namespaces git commit -m "Bypass namespace validation"
```

⚠️ **Warning**: Skipping validation can introduce namespace collisions and break the ontology integrity. Only use in emergencies and fix violations immediately.

---

## Performance

**Typical Performance**:
- 0-10 files: < 1 second
- 10-50 files: 1-3 seconds
- 50-100 files: 3-5 seconds

**Optimization Tips**:
- Validation only runs on `capabilities/*.yaml` files (configured in `.pre-commit-config.yaml`)
- Uses efficient regex matching and dict lookups
- Pre-commit caches results between runs

---

## References

### Documentation
- [Namespace Specification](../docs/ontology/namespace-spec.md) - Complete namespace format rules
- [Domain Taxonomy](../docs/ontology/domain-taxonomy.md) - Valid domain definitions
- [Capability Types](../docs/ontology/capability-types.md) - Service vs Pattern types
- [Migration Guide](../docs/ontology/migration-guide.md) - SAP-XXX → chora.domain.capability

### Related Tasks
- **ONT-009** (Week 3.1): Implement pre-commit hook (this deliverable)
- **ONT-010** (Week 3.2): Create CI/CD duplicate detection workflow
- **ONT-011** (Week 3.3): Implement migration script (sap-catalog.json → YAML)
- **ONT-012** (Week 3.4): Create SAP artifact reference extractor

### Files
- `scripts/validate-namespaces.py` - Validation script
- `.pre-commit-config.yaml` - Pre-commit hook configuration
- `.markdownlint.json` - Markdown linting rules

---

## Support

**Issues**: Report namespace validation bugs or feature requests in beads:
```bash
bd create --title "Namespace validation: <issue>" --label "ontology,validation"
```

**Questions**: See [docs/ontology/namespace-spec.md](../docs/ontology/namespace-spec.md) for complete specification.

---

**Version**: 1.0.0
**Last Updated**: 2025-11-15
**Author**: Claude (ONT-009)
**Status**: Active ✅
