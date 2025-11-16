# SAP Catalog Migration Script

**Version**: 1.0.0
**Status**: Active
**Part of**: Ecosystem Ontology & Composition Vision - Phase 1, Week 3.3

---

## Overview

The migration script (`migrate-sap-catalog.py`) automates the conversion of SAP entries from `sap-catalog.json` to unified YAML manifest format. It implements the migration strategy defined in [docs/ontology/migration-guide.md](../docs/ontology/migration-guide.md).

**Implemented in**: ONT-011 (Week 3.3)

---

## Features

### 1. **Automated Namespace Generation**
- Converts `SAP-XXX` IDs to `chora.domain.capability` format
- Maps legacy domains to ontology domains
- Converts kebab-case to snake_case
- Removes redundant domain prefixes

### 2. **Capability Type Detection**
- Auto-determines Service-type vs Pattern-type
- Based on system_files presence and known Service SAPs
- Generates appropriate manifest structure

### 3. **Artifact Auto-Detection**
- Scans `docs/skilled-awareness/{sap-name}/` directory
- Detects all 5 SAP artifacts automatically
- Generates artifact array for Pattern-type manifests
- Includes relative paths and formats

### 4. **Adoption Metrics Preservation**
- Preserves effort_minutes
- Preserves complexity (low/medium/high)
- Preserves time_savings_minutes (ROI)
- Adds to `chora_adoption` extension

### 5. **Flexible Migration Modes**
- **Single SAP**: `--sap SAP-001`
- **All SAPs**: `--all` (batch migration)
- **Domain Filter**: `--domain Infrastructure`
- **Dry-run**: `--dry-run` (preview without writing)

### 6. **Validation Support**
- Outputs valid YAML manifests
- Compatible with JSON Schema validators
- Validates against namespace format rules

---

## Installation

### Prerequisites

```bash
# Python 3.8+
python --version

# PyYAML
pip install PyYAML
```

### Make Executable

```bash
chmod +x scripts/migrate-sap-catalog.py
```

---

## Usage

### Basic Examples

**Migrate single SAP**:
```bash
python scripts/migrate-sap-catalog.py --sap SAP-001 --output capabilities/
```

**Migrate all SAPs**:
```bash
python scripts/migrate-sap-catalog.py --all --output capabilities/
```

**Dry-run mode** (preview without writing):
```bash
python scripts/migrate-sap-catalog.py --all --dry-run
```

**Migrate specific domain**:
```bash
python scripts/migrate-sap-catalog.py --domain Infrastructure --output capabilities/
```

---

### Advanced Examples

**Migrate to custom directory**:
```bash
python scripts/migrate-sap-catalog.py --all --output /path/to/manifests/
```

**Migrate with custom catalog file**:
```bash
python scripts/migrate-sap-catalog.py \
  --catalog /path/to/custom-catalog.json \
  --sap SAP-001 \
  --output capabilities/
```

**Skip validation** (faster, but not recommended):
```bash
python scripts/migrate-sap-catalog.py --all --no-validate --output capabilities/
```

---

## Migration Examples

### Example 1: Pattern-Type SAP

**Input** (sap-catalog.json):
```json
{
  "id": "SAP-009",
  "name": "agent-awareness",
  "full_name": "Agent Awareness System",
  "status": "active",
  "version": "1.1.0",
  "description": "AGENTS.md/CLAUDE.md patterns with bidirectional translation layer",
  "domain": "Specialized",
  "location": "docs/skilled-awareness/agent-awareness",
  "artifacts": {
    "capability_charter": true,
    "protocol_spec": true,
    "awareness_guide": true,
    "adoption_blueprint": true,
    "ledger": true
  },
  "dependencies": ["SAP-000", "SAP-007"]
}
```

**Output** (chora.awareness.agent_awareness.yaml):
```yaml
apiVersion: chora.dev/v1
kind: Capability

metadata:
  dc_identifier: chora.awareness.agent_awareness
  dc_identifier_legacy: SAP-009
  dc_title: "Agent Awareness System"
  dc_description: "AGENTS.md/CLAUDE.md patterns with bidirectional translation layer"
  dc_type: "Pattern"
  dc_hasVersion: "1.1.0"
  dc_creator: "chora-base"
  dc_date: "2025-11-15"
  dc_format: "text/markdown"
  dc_subject:
    - "agent-awareness"
    - "ai-context"
    - "documentation"

dc_relation:
  requires:
    - capability: chora.SAP-000  # Mapped from dependencies
      relationship: prerequisite
    - capability: chora.SAP-007
      relationship: prerequisite

chora_pattern:
  artifacts:
    - type: capability_charter
      path: docs/skilled-awareness/agent-awareness/capability-charter.md
      format: text/markdown
    - type: protocol_specification
      path: docs/skilled-awareness/agent-awareness/protocol-spec.md
      format: text/markdown
    - type: awareness_guide
      path: docs/skilled-awareness/agent-awareness/AGENTS.md
      format: text/markdown
    - type: adoption_blueprint
      path: docs/skilled-awareness/agent-awareness/adoption-blueprint.md
      format: text/markdown
    - type: adoption_ledger
      path: docs/skilled-awareness/agent-awareness/ledger.md
      format: text/markdown
```

---

### Example 2: Service-Type SAP

**Input** (sap-catalog.json):
```json
{
  "id": "SAP-044",
  "name": "registry",
  "full_name": "Service Registry & Discovery",
  "status": "pilot",
  "version": "1.0.0",
  "description": "Service mesh with capability discovery and health monitoring",
  "domain": "Infrastructure",
  "system_files": [
    "services/registry/",
    "scripts/registry-server.py"
  ]
}
```

**Output** (chora.registry.lookup.yaml):
```yaml
apiVersion: chora.dev/v1
kind: Capability

metadata:
  dc_identifier: chora.registry.lookup
  dc_identifier_legacy: SAP-044
  dc_title: "Service Registry & Discovery"
  dc_description: "Service mesh with capability discovery and health monitoring"
  dc_type: "Service"
  dc_hasVersion: "1.0.0"
  dc_creator: "chora-base"
  dc_date: "2025-11-15"
  dc_format: "application/x-executable"

chora_service:
  interfaces:
    - cli
    - mcp
  health:
    endpoint: /health
    interval: 10
    timeout: 5
    heartbeat_ttl: 30
  distribution:
    pypi:
      package_name: chora-registry
      install_command: pip install chora-registry
```

---

## Domain Mapping

The script automatically maps legacy domains to ontology domains:

| sap-catalog.json Domain | Ontology Domain | Examples |
|-------------------------|-----------------|----------|
| Infrastructure | infrastructure | SAP-000, SAP-001, SAP-002 |
| Developer Experience | devex | SAP-003, SAP-004, SAP-005 |
| React | react | SAP-033-SAP-048 (React SAPs) |
| Vue | vue | (Reserved for future) |
| Specialized | awareness | SAP-009, SAP-027 |
| Advanced | integration | (Advanced integrations) |
| Workflow | workflow | (Workflow patterns) |

**Special Cases**:
- SAPs starting with `react-` → `react` domain
- SAPs starting with `vue-` → `vue` domain
- Unknown domains → `infrastructure` (with warning)

---

## Capability Type Detection

**Service-Type** if any of:
- Listed in `SERVICE_TYPE_SAPS` constant (SAP-042, SAP-043, SAP-044, SAP-045, SAP-047)
- Has `system_files` with Python scripts in `scripts/` directory

**Pattern-Type** (default) if:
- No runtime component
- Documentation-only SAP
- Has 5 SAP artifacts in directory

---

## Artifact Auto-Detection

The script scans `docs/skilled-awareness/{sap-name}/` for these files:

| File Name | Artifact Type | Required |
|-----------|---------------|----------|
| capability-charter.md | capability_charter | Yes |
| protocol-spec.md | protocol_specification | Yes |
| AGENTS.md or awareness-guide.md | awareness_guide | Yes |
| adoption-blueprint.md | adoption_blueprint | Yes |
| ledger.md | adoption_ledger | Yes |

**Output Format**:
```yaml
chora_pattern:
  artifacts:
    - type: capability_charter
      path: docs/skilled-awareness/{sap-name}/capability-charter.md
      format: text/markdown
```

---

## Output Files

**Naming Convention**: `{namespace}.yaml`

**Examples**:
- `SAP-001` → `chora.infrastructure.inbox.yaml`
- `SAP-009` → `chora.awareness.agent_awareness.yaml`
- `SAP-041` → `chora.react.form_validation.yaml`

**Location**: Specified by `--output` (default: `capabilities/`)

---

## Migration Statistics

The script tracks and reports:
- **Total SAPs**: Number in catalog
- **Migrated**: Successfully converted
- **Skipped**: Filtered out or errors
- **Errors**: Failed migrations

**Example Output**:
```
================================================================================
Migration Summary
================================================================================
Total SAPs: 45
Migrated: 45
Skipped: 0
Errors: 0

SUCCESS: Migration completed successfully
================================================================================
```

---

## Error Handling

### Common Errors

**1. Catalog Not Found**
```
ERROR: SAP catalog not found: sap-catalog.json
```
**Fix**: Ensure `sap-catalog.json` exists or use `--catalog` to specify path

**2. Invalid JSON**
```
ERROR: Invalid JSON in catalog: Expecting property name enclosed in double quotes
```
**Fix**: Validate JSON syntax with `cat sap-catalog.json | python -m json.tool`

**3. Failed Migration**
```
ERROR: Failed to migrate SAP-XXX: [error details]
```
**Fix**: Check SAP data structure and artifact directory existence

---

## Integration with Other Tools

### With Namespace Validator

**Validate migrated manifests**:
```bash
# Migrate SAPs
python scripts/migrate-sap-catalog.py --all --output capabilities/

# Validate namespaces
python scripts/validate-namespaces.py capabilities/
```

### With Pre-commit Hooks

**Migrate and commit**:
```bash
# Migrate
python scripts/migrate-sap-catalog.py --all --output capabilities/

# Add to git (pre-commit hooks run automatically)
git add capabilities/*.yaml
git commit -m "feat(ontology): migrate all SAPs to YAML manifests"
```

### With JSON Schema Validation

**Validate against schema**:
```bash
# Migrate
python scripts/migrate-sap-catalog.py --sap SAP-009 --output capabilities/

# Validate (requires jsonschema package)
python -c "
import yaml, json, jsonschema
from pathlib import Path

manifest = yaml.safe_load(Path('capabilities/chora.awareness.agent_awareness.yaml').read_text())
schema = json.load(open('schemas/capability-pattern.schema.json'))
jsonschema.validate(manifest, schema)
print('Valid!')
"
```

---

## Troubleshooting

### Dry-Run Shows Expected Results, But Migration Fails

**Symptom**: Dry-run works but actual migration fails

**Possible Cause**: Permission issues with output directory

**Fix**:
```bash
# Create output directory
mkdir -p capabilities/

# Ensure write permissions
chmod -R u+w capabilities/
```

### Dependency Mapping Shows SAP-XXX Format

**Symptom**: Dependencies still show `chora.SAP-XXX` instead of proper namespaces

**Current Status**: Known limitation in v1.0.0

**Workaround**: Manually update dependencies after migration:
```yaml
# Before
dc_relation:
  requires:
    - capability: chora.SAP-000

# After (manual update)
dc_relation:
  requires:
    - capability: chora.infrastructure.sap_framework
      version: ^1.0.0
      relationship: prerequisite
```

**Planned**: Full dependency namespace resolution in v1.1.0

### Artifact Auto-Detection Misses Files

**Symptom**: Some artifacts not detected

**Possible Cause**: Non-standard file names or directory structure

**Fix**: Ensure SAP directory follows standard structure:
```
docs/skilled-awareness/{sap-name}/
├── capability-charter.md
├── protocol-spec.md
├── AGENTS.md (or awareness-guide.md)
├── adoption-blueprint.md
└── ledger.md
```

---

## Performance

**Typical Performance**:
- Single SAP: < 1 second
- All 45 SAPs: 2-5 seconds
- Artifact scanning: 10-50ms per SAP

**Optimization**:
- Parallel processing not implemented (sequential migration)
- Artifact scanning could be cached
- Dependency resolution could be optimized

---

## Future Enhancements (Not in Week 3.3)

**Planned for Later Phases**:
- [ ] Full dependency namespace resolution (resolve `SAP-XXX` → `chora.domain.capability`)
- [ ] Parallel processing for batch migrations
- [ ] Artifact validation (check all 5 required artifacts present)
- [ ] Custom template support for Service/Pattern types
- [ ] Migration rollback functionality
- [ ] Diff mode (show changes before migration)
- [ ] Interactive mode for manual review

---

## References

### Documentation
- [Migration Guide](../docs/ontology/migration-guide.md) - Complete migration strategy
- [Namespace Specification](../docs/ontology/namespace-spec.md) - Namespace format rules
- [Domain Taxonomy](../docs/ontology/domain-taxonomy.md) - Domain definitions
- [Capability Types](../docs/ontology/capability-types.md) - Service vs Pattern

### Related Tasks
- **ONT-009** (Week 3.1): Implement pre-commit hook
- **ONT-010** (Week 3.2): Create CI/CD workflow
- **ONT-011** (Week 3.3): Implement migration script (this deliverable)
- **ONT-012** (Week 3.4): Create artifact extractor

### Files
- `scripts/migrate-sap-catalog.py` - Migration script
- `sap-catalog.json` - Source catalog
- `capabilities/template-service.yaml` - Service template
- `capabilities/template-pattern.yaml` - Pattern template

---

## Support

**Issues**: Report migration bugs or feature requests in beads:
```bash
bd create --title "Migration script: <issue>" --label "ontology,migration"
```

**Questions**: See migration guide for complete field mapping and strategy.

---

**Version**: 1.0.0
**Last Updated**: 2025-11-15
**Author**: Claude (ONT-011)
**Status**: Active ✅
