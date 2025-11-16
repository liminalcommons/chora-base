# Migration Guide: sap-catalog.json → Unified YAML Manifests

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-11-15
**Part of**: Ecosystem Ontology & Composition Vision (SAP-048)

---

## Purpose

This guide provides step-by-step instructions for migrating capabilities from the legacy `sap-catalog.json` format to the unified ontology YAML manifest format.

**Migration Scope**: 45 SAPs (6 Service-type + 39 Pattern-type)

**Timeline**:
- **v5.2.0** (Week 4): Pilot migration (8 capabilities)
- **v5.3.0** (Week 8): Full migration (all 45 SAPs)
- **v5.5.0** (Week 16): Deprecation warnings for legacy format
- **v6.0.0** (Q2 2026): Legacy format removal

---

## Field Mapping: sap-catalog.json → YAML Manifest

### Complete Mapping Table

| sap-catalog.json Field | YAML Manifest Field | Dublin Core Element | Type | Required | Notes |
|------------------------|---------------------|---------------------|------|----------|-------|
| `id` | `dc_identifier` | `dc:identifier` | String | Yes | `SAP-XXX` → `chora.domain.capability` |
| `id` | `dc_identifier_legacy` | (custom) | String | Optional | Alias during migration: `SAP-XXX` |
| `name` | (derived from `dc_identifier`) | - | - | - | Converted to snake_case capability name |
| `title` | `dc_title` | `dc:title` | String | Yes | Human-readable display name |
| `description` | `dc_description` | `dc:description` | String | Yes | One-sentence summary |
| `status` | `status` | (custom) | Enum | Yes | `active`, `pilot`, `draft`, `deprecated` |
| `version` | `dc_hasVersion` | `dc:hasVersion` | String | Yes | SemVer format (x.y.z) |
| `domain` | (part of `dc_identifier`) | - | - | - | Maps to 2nd level of namespace |
| `created_at` | `dc_date` | `dc:date` | ISO 8601 | Optional | Publication date |
| `updated_at` | `updated_at` | (custom) | ISO 8601 | Optional | Last modification |
| `dependencies` | `dc_relation.requires` | `dc:relation` | Array | Optional | Typed relationships |
| `optional_dependencies` | `dc_relation.optional` | `dc:relation` | Array | Optional | Soft dependencies |
| `effort_minutes` | `chora_adoption.effort_minutes` | (chora extension) | Integer | Optional | Adoption time |
| `complexity` | `chora_adoption.complexity` | (chora extension) | Enum | Optional | `low`, `medium`, `high` |
| `time_savings_minutes` | `chora_adoption.time_savings_minutes` | (chora extension) | Integer | Optional | ROI metric |
| (new) | `dc_type` | `dc:type` | Enum | Yes | `"Service"` or `"Pattern"` |
| (new) | `dc_format` | `dc:format` | MIME | Optional | `application/x-executable` or `text/markdown` |
| (new) | `chora_service.interfaces` | (chora extension) | Array | Service only | `cli`, `rest`, `mcp` |
| (new) | `chora_service.health.endpoint` | (chora extension) | String | Service only | Health check URL |
| (new) | `chora_pattern.artifacts` | (chora extension) | Array | Pattern only | 5 SAP artifacts |

---

## Migration Strategy

### Strategy Overview

**Two-Phase Approach**:

1. **Phase 1 (Weeks 1-4)**: Pilot migration
   - Migrate 8 capabilities (5 Service + 3 Pattern)
   - Validate tooling and processes
   - Gather feedback and adjust

2. **Phase 2 (Weeks 5-8)**: Full migration
   - Migrate remaining 37 capabilities
   - Batch processing with automation
   - Final validation and cleanup

**Dual-Mode Registry**: Support both old and new formats during transition (2-version grace period)

---

## Step-by-Step Migration Process

### Step 1: Identify Capability Type

**Determine if capability is Service-type or Pattern-type**:

**Service-Type Indicators**:
- Has runtime implementation (server, CLI tool, MCP server)
- Provides interfaces (CLI, REST, MCP)
- Requires health monitoring
- Listed in PyPI with installable package

**Pattern-Type Indicators**:
- Documentation-only (SAP artifacts)
- No runtime component
- Learning path or adoption methodology
- Process pattern or best practice

**Examples**:
- Service-type: SAP-042 (interface-design implementation), SAP-044 (registry service), SAP-047 (capability-server generator)
- Pattern-type: SAP-009 (agent-awareness docs), SAP-041 (react-form-validation patterns), SAP-027 (dogfooding methodology)

---

### Step 2: Determine Target Namespace

**Formula**: `chora.{domain}.{capability}`

**2.1: Choose Domain**

Use [domain-taxonomy.md#domain-allocation-guidelines](./domain-taxonomy.md#domain-allocation-guidelines)

**Decision Tree**:
```
SAP domain in sap-catalog.json → Target domain in ontology

Infrastructure → infrastructure
Developer Experience → devex
React → react
Specialized (process patterns) → awareness or workflow
Specialized (meta-capabilities) → awareness
Advanced (integrations) → integration
Advanced (optimizations) → optimization
```

**2.2: Choose Capability Name**

**Conversion Rules**:
1. Take `name` field from sap-catalog.json
2. Convert kebab-case to snake_case: `react-form-validation` → `form_validation`
3. Remove domain prefix if redundant: `react-form-validation` → `form_validation`
4. Keep capability name within 50 characters
5. Use action verbs for Service-type, noun phrases for Pattern-type

**Examples**:
```json
// sap-catalog.json
{
  "id": "SAP-041",
  "name": "react-form-validation",
  "domain": "React"
}

// Target namespace
dc_identifier: chora.react.form_validation
```

---

### Step 3: Create YAML Manifest

**3.1: Use Template**

```bash
# For Service-type capabilities
cp capabilities/template-service.yaml capabilities/chora.domain.capability.yaml

# For Pattern-type capabilities
cp capabilities/template-pattern.yaml capabilities/chora.domain.capability.yaml
```

**3.2: Fill Required Fields**

```yaml
apiVersion: chora.dev/v1
kind: Capability

metadata:
  # REQUIRED FIELDS
  dc_identifier: chora.domain.capability      # New namespace
  dc_identifier_legacy: SAP-XXX               # Legacy SAP ID (alias)
  dc_title: "Human-Readable Title"            # From sap-catalog.json "title"
  dc_description: "One-sentence summary"      # From sap-catalog.json "description"
  dc_type: "Service" | "Pattern"              # NEW: Capability type
  dc_hasVersion: "x.y.z"                      # From sap-catalog.json "version"

  # OPTIONAL FIELDS
  dc_creator: "Chora Core Team"               # Author/team
  dc_date: "2025-11-15"                       # From sap-catalog.json "created_at"
  updated_at: "2025-11-15"                    # From sap-catalog.json "updated_at"

status: active | pilot | draft | deprecated   # From sap-catalog.json "status"
```

---

### Step 4: Migrate Dependencies

**4.1: Map Dependency Types**

| sap-catalog.json | YAML Manifest | Relationship Type | Validation |
|------------------|---------------|-------------------|------------|
| `dependencies` (Service → Service) | `dc_relation.requires` | `runtime` | Health check |
| `dependencies` (Pattern → Pattern) | `dc_relation.requires` | `prerequisite` | Topological sort |
| `optional_dependencies` | `dc_relation.optional` | `optional` | Opportunistic discovery |
| (new) | `dc_relation.conflicts` | `mutually_exclusive` | Error if both present |

**4.2: Convert Dependency References**

**Old Format**:
```json
{
  "dependencies": ["SAP-020", "SAP-023"],
  "optional_dependencies": ["SAP-025"]
}
```

**New Format**:
```yaml
metadata:
  dc_relation:
    requires:
      - capability: chora.react.foundation      # SAP-020
        version: ^1.0.0
        relationship: prerequisite
        description: "Foundation stack required"
      - capability: chora.react.state_management # SAP-023
        version: ^1.0.0
        relationship: prerequisite
        description: "State management patterns"
    optional:
      - capability: chora.react.performance      # SAP-025
        version: ^1.0.0
        relationship: complementary
        description: "Enhances with performance optimizations"
```

**Dependency Lookup Table**: See [Appendix A: SAP-XXX → chora.domain.capability Mapping](#appendix-a-sap-xxx--choradomaincapability-mapping)

---

### Step 5: Add Type-Specific Fields

#### Service-Type Capabilities

```yaml
metadata:
  dc_type: "Service"
  dc_format: "application/x-executable"

spec:
  chora_service:
    # Multi-interface specification (SAP-043)
    interfaces:
      - type: cli
        command: chora-registry
        entrypoint: chora.registry.cli:main
      - type: rest
        port: 8000
        openapi: /api/v1/openapi.json
      - type: mcp
        transport: stdio
        server_info:
          name: chora-registry
          version: "1.0.0"

    # Health monitoring (SAP-044)
    health:
      endpoint: /health
      interval: 10s
      timeout: 5s
      heartbeat_ttl: 30s

    # Distribution
    distribution:
      pypi_package: chora-registry
      docker_image: ghcr.io/chora-base/registry:1.0.0
```

#### Pattern-Type Capabilities

```yaml
metadata:
  dc_type: "Pattern"
  dc_format: "text/markdown"

spec:
  chora_pattern:
    # SAP artifact references (5 standard artifacts)
    artifacts:
      - type: capability-charter
        path: docs/skilled-awareness/domain/capability-charter.md
      - type: protocol-spec
        path: docs/skilled-awareness/domain/protocol-spec.md
      - type: awareness-guide
        path: docs/skilled-awareness/domain/awareness-guide.md
      - type: adoption-blueprint
        path: docs/skilled-awareness/domain/adoption-blueprint.md
      - type: ledger
        path: docs/skilled-awareness/domain/ledger.md

    # Adoption metadata (from sap-catalog.json)
    chora_adoption:
      effort_minutes: 120
      complexity: medium
      time_savings_minutes: 480
      roi_percentage: 300.0
      success_criteria:
        - "Artifact paths are valid and accessible"
        - "Adoption steps tested with real projects"
        - "Time savings validated in pilot"
```

---

### Step 6: Validate Manifest

```bash
# JSON Schema validation (Week 3 deliverable)
python scripts/validate-capability.py capabilities/chora.domain.capability.yaml

# Pre-commit hook (runs automatically on commit)
git add capabilities/chora.domain.capability.yaml
git commit -m "feat(ontology): migrate SAP-XXX to chora.domain.capability"
# Hook validates:
# - JSON Schema compliance
# - Namespace uniqueness
# - Dependency version constraints
# - Cross-type relationship rules
```

---

### Step 7: Update Cross-References

**7.1: Update Documentation Links**

```bash
# Find all references to SAP-XXX
grep -r "SAP-041" docs/

# Replace with new namespace
# SAP-041 → chora.react.form_validation
```

**7.2: Update Code References**

```bash
# Python code
# Old: from chora.saps.sap_041 import FormValidation
# New: from chora.react.form_validation import FormValidation

# JavaScript code
# Old: import { formValidation } from '@chora/sap-041'
# New: import { formValidation } from '@chora/react-form-validation'
```

---

## Migration Examples

### Example 1: Pattern-Type Capability (SAP-041)

#### Before (sap-catalog.json)

```json
{
  "id": "SAP-041",
  "name": "react-form-validation",
  "title": "React Form Validation Patterns",
  "description": "React Hook Form + Zod validation patterns for production apps",
  "status": "pilot",
  "version": "1.0.0",
  "domain": "Foundation",
  "created_at": "2025-11-01T00:00:00Z",
  "updated_at": "2025-11-10T00:00:00Z",
  "dependencies": ["SAP-020"],
  "optional_dependencies": ["SAP-023"],
  "effort_minutes": 120,
  "complexity": "medium",
  "time_savings_minutes": 480,
  "artifacts": [
    "docs/skilled-awareness/react-form-validation/capability-charter.md",
    "docs/skilled-awareness/react-form-validation/protocol-spec.md",
    "docs/skilled-awareness/react-form-validation/awareness-guide.md",
    "docs/skilled-awareness/react-form-validation/adoption-blueprint.md",
    "docs/skilled-awareness/react-form-validation/ledger.md"
  ]
}
```

#### After (capabilities/chora.react.form_validation.yaml)

```yaml
apiVersion: chora.dev/v1
kind: Capability

metadata:
  dc_identifier: chora.react.form_validation
  dc_identifier_legacy: SAP-041
  dc_title: "React Form Validation Patterns"
  dc_description: "React Hook Form + Zod validation patterns for production apps"
  dc_type: "Pattern"
  dc_hasVersion: "1.0.0"
  dc_creator: "Chora Core Team"
  dc_date: "2025-11-01"
  dc_format: "text/markdown"
  updated_at: "2025-11-10"

  dc_relation:
    requires:
      - capability: chora.react.foundation
        version: ^1.0.0
        relationship: prerequisite
        description: "Foundation stack (Next.js, TypeScript, Vitest)"
    optional:
      - capability: chora.react.state_management
        version: ^1.0.0
        relationship: complementary
        description: "Enhances with Zustand form state persistence"

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

    chora_adoption:
      effort_minutes: 120
      complexity: medium
      time_savings_minutes: 480
      roi_percentage: 300.0
      success_criteria:
        - "React Hook Form v7+ integrated"
        - "Zod schema validation operational"
        - "Form submission handles async errors"
        - "Accessibility compliance (WCAG 2.2)"
```

---

### Example 2: Service-Type Capability (SAP-044)

#### Before (sap-catalog.json)

```json
{
  "id": "SAP-044",
  "name": "registry",
  "title": "Service Registry & Discovery",
  "description": "Service mesh with capability discovery, health monitoring, and dependency resolution",
  "status": "pilot",
  "version": "1.0.0",
  "domain": "Developer Experience",
  "created_at": "2025-11-12T00:00:00Z",
  "dependencies": ["SAP-045"],
  "optional_dependencies": ["SAP-046"],
  "runtime": true,
  "interfaces": ["cli", "rest", "mcp"]
}
```

#### After (capabilities/chora.registry.lookup.yaml)

```yaml
apiVersion: chora.dev/v1
kind: Capability

metadata:
  dc_identifier: chora.registry.lookup
  dc_identifier_legacy: SAP-044
  dc_title: "Service Registry & Discovery"
  dc_description: "Service mesh with capability discovery, health monitoring, and dependency resolution"
  dc_type: "Service"
  dc_hasVersion: "1.0.0"
  dc_creator: "Chora Core Team"
  dc_date: "2025-11-12"
  dc_format: "application/x-executable"

  dc_relation:
    requires:
      - capability: chora.bootstrap.initialize
        version: ^1.0.0
        relationship: runtime
        description: "Bootstrap service must start before registry"
    optional:
      - capability: chora.composition.saga
        version: ^1.0.0
        relationship: optional
        description: "Integrates with saga orchestration if available"

status: pilot

spec:
  chora_service:
    interfaces:
      - type: cli
        command: chora-registry
        entrypoint: chora.registry.cli:main
        description: "CLI for capability lookup and health checks"
      - type: rest
        port: 8000
        openapi: /api/v1/openapi.json
        description: "REST API for programmatic discovery"
      - type: mcp
        transport: stdio
        server_info:
          name: chora-registry
          version: "1.0.0"
        description: "MCP server for Claude Desktop integration"

    health:
      endpoint: /health
      interval: 10s
      timeout: 5s
      heartbeat_ttl: 30s
      liveness_probe: /health/live
      readiness_probe: /health/ready

    distribution:
      pypi_package: chora-registry
      pypi_classifiers:
        - "Development Status :: 4 - Beta"
        - "Intended Audience :: Developers"
        - "Topic :: Software Development :: Libraries"
      docker_image: ghcr.io/chora-base/registry:1.0.0
      docker_platforms:
        - linux/amd64
        - linux/arm64
```

---

## Automated Migration Script

### Script Usage (Week 3 Deliverable)

```bash
# Migrate single SAP
python scripts/migrate-sap-catalog.py \
    --input sap-catalog.json \
    --output capabilities/ \
    --sap-id SAP-041

# Migrate all SAPs
python scripts/migrate-sap-catalog.py \
    --input sap-catalog.json \
    --output capabilities/ \
    --all

# Migrate specific domain
python scripts/migrate-sap-catalog.py \
    --input sap-catalog.json \
    --output capabilities/ \
    --domain react

# Dry run (validate only, don't write)
python scripts/migrate-sap-catalog.py \
    --input sap-catalog.json \
    --output capabilities/ \
    --all \
    --dry-run
```

### Script Features

**Automated Processing**:
1. Reads sap-catalog.json
2. Determines capability type (Service vs Pattern)
3. Maps fields to Dublin Core metadata
4. Converts dependencies to typed relationships
5. Validates namespace uniqueness
6. Generates YAML manifest
7. Validates with JSON Schema
8. Writes to `capabilities/chora.domain.capability.yaml`

**Error Handling**:
- Namespace collision detection
- Invalid SemVer version warnings
- Missing required fields
- Broken dependency references
- Invalid domain names

---

## Pilot Migration Plan (Week 4)

### Pilot Capabilities (8 total: 5 Service + 3 Pattern)

**Service-Type** (5):
1. **SAP-042** (`interface-design`) → `chora.interface.design`
2. **SAP-043** (`multi-interface`) → `chora.interface.multi`
3. **SAP-044** (`registry`) → `chora.registry.lookup`
4. **SAP-045** (`bootstrap`) → `chora.bootstrap.initialize`
5. **SAP-046** (`composition`) → `chora.composition.saga`

**Pattern-Type** (3):
1. **SAP-041** (`react-form-validation`) → `chora.react.form_validation`
2. **SAP-009** (`agent-awareness`) → `chora.awareness.nested_pattern`
3. **SAP-004** (`testing-framework`) → `chora.devex.testing_framework`

### Pilot Validation Steps

**Week 4.1: Migrate 8 Capabilities**
```bash
# Batch migrate pilot capabilities
for sap in SAP-042 SAP-043 SAP-044 SAP-045 SAP-046 SAP-041 SAP-009 SAP-004; do
  python scripts/migrate-sap-catalog.py \
      --input sap-catalog.json \
      --output capabilities/ \
      --sap-id $sap
done
```

**Week 4.2: Validate Dual-Mode Lookups**
```bash
# Test old namespace resolution
chora registry lookup SAP-041
# Should return: chora.react.form_validation (with deprecation warning)

# Test new namespace resolution
chora registry lookup chora.react.form_validation
# Should return: Capability details (no warning)
```

**Week 4.3: Test Cross-Type Dependencies**
```bash
# Service → Pattern (advisory)
chora registry resolve chora.composition.saga
# Should warn about Pattern prerequisites

# Pattern → Service (hard requirement)
chora registry resolve chora.awareness.task_tracking
# Should check Service health status
```

**Week 4.4: Document Lessons Learned**
```bash
# Capture feedback in retrospective
vim docs/project-docs/retrospectives/phase-1-pilot-retrospective.md
```

---

## Full Migration Plan (Week 8)

### Batch Migration (37 remaining SAPs)

**Week 8.1-8.2: Migrate All SAPs**
```bash
# Full batch migration
python scripts/migrate-sap-catalog.py \
    --input sap-catalog.json \
    --output capabilities/ \
    --all
```

**Week 8.3: Validate All Manifests**
```bash
# JSON Schema validation
python scripts/validate-all-capabilities.py capabilities/

# Dependency resolution test
python scripts/test-dependency-resolution.py capabilities/

# Namespace uniqueness check
python scripts/check-namespace-collisions.py capabilities/
```

**Week 8.4: PyPI Publishing**
```bash
# Publish all 6 Service-type capabilities to PyPI
for pkg in registry bootstrap composition interface multi templates; do
  cd packages/chora-$pkg
  poetry publish --build
done
```

---

## Appendix A: SAP-XXX → chora.domain.capability Mapping

### Infrastructure Domain (3 SAPs)

| SAP ID | Old Name | New Namespace | Type |
|--------|----------|---------------|------|
| SAP-000 | sap-framework | chora.infrastructure.sap_framework | Pattern |
| SAP-001 | inbox | chora.infrastructure.inbox | Pattern |
| SAP-002 | chora-base | chora.infrastructure.meta_package | Pattern |

### DevEx Domain (14 SAPs)

| SAP ID | Old Name | New Namespace | Type |
|--------|----------|---------------|------|
| SAP-003 | project-bootstrap | chora.devex.project_bootstrap | Pattern |
| SAP-004 | testing-framework | chora.devex.testing_framework | Pattern |
| SAP-005 | ci-cd-workflows | chora.devex.ci_cd | Pattern |
| SAP-006 | quality-gates | chora.devex.quality_gates | Pattern |
| SAP-007 | documentation-framework | chora.devex.documentation | Pattern |
| SAP-008 | automation-scripts | chora.devex.automation | Pattern |
| SAP-011 | docker-operations | chora.devex.docker | Pattern |
| SAP-014 | mcp-server-development | chora.devex.mcp_server (deprecated) | Pattern |
| SAP-042 | interface-design | chora.interface.design | Pattern |
| SAP-043 | multi-interface | chora.interface.multi | Pattern |
| SAP-044 | registry | chora.registry.lookup | Service |
| SAP-045 | bootstrap | chora.bootstrap.initialize | Service |
| SAP-046 | composition | chora.composition.saga | Service |
| SAP-047 | capability-server-template | chora.templates.capability_server | Pattern |

### React Domain (15 SAPs)

| SAP ID | Old Name | New Namespace | Type |
|--------|----------|---------------|------|
| SAP-020 | react-foundation | chora.react.foundation | Pattern |
| SAP-021 | react-testing | chora.react.testing | Pattern |
| SAP-022 | react-linting | chora.react.linting | Pattern |
| SAP-023 | react-state-management | chora.react.state_management | Pattern |
| SAP-024 | react-styling | chora.react.styling | Pattern |
| SAP-025 | react-performance | chora.react.performance | Pattern |
| SAP-026 | react-accessibility | chora.react.accessibility | Pattern |
| SAP-033 | react-authentication | chora.react.authentication | Pattern |
| SAP-034 | react-database-integration | chora.react.database_integration | Pattern |
| SAP-035 | react-file-upload | chora.react.file_upload | Pattern |
| SAP-036 | react-error-handling | chora.react.error_handling | Pattern |
| SAP-037 | react-realtime-synchronization | chora.react.realtime | Pattern |
| SAP-038 | react-internationalization | chora.react.i18n | Pattern |
| SAP-039 | react-e2e-testing | chora.react.e2e_testing | Pattern |
| SAP-040 | react-monorepo-architecture | chora.react.monorepo | Pattern |
| SAP-041 | react-form-validation | chora.react.form_validation | Pattern |

### Awareness Domain (4 SAPs)

| SAP ID | Old Name | New Namespace | Type |
|--------|----------|---------------|------|
| SAP-009 | agent-awareness | chora.awareness.nested_pattern | Pattern |
| SAP-010 | memory-system | chora.awareness.event_memory | Pattern |
| SAP-015 | task-tracking | chora.awareness.task_tracking | Pattern |
| SAP-019 | sap-self-evaluation | chora.awareness.sap_evaluation | Pattern |

### Workflow Domain (6 SAPs)

| SAP ID | Old Name | New Namespace | Type |
|--------|----------|---------------|------|
| SAP-012 | development-lifecycle | chora.workflow.lifecycle | Pattern |
| SAP-013 | metrics-tracking | chora.workflow.metrics | Pattern |
| SAP-016 | link-validation-reference-management | chora.workflow.link_validation | Pattern |
| SAP-027 | dogfooding-patterns | chora.workflow.dogfooding | Pattern |
| SAP-028 | publishing-automation | chora.workflow.publishing | Pattern |
| SAP-029 | sap-generation | chora.workflow.sap_generation | Pattern |

### Integration Domain (2 SAPs)

| SAP ID | Old Name | New Namespace | Type |
|--------|----------|---------------|------|
| SAP-017 | chora-compose-integration | chora.integration.compose | Service |
| SAP-018 | chora-compose-meta | chora.integration.compose_meta | Service |

---

## Appendix B: Validation Checklist

### Pre-Migration Checklist

- [ ] SAP type determined (Service vs Pattern)
- [ ] Target domain selected from taxonomy
- [ ] Capability name follows naming conventions
- [ ] Namespace uniqueness verified
- [ ] All dependencies mapped to new namespaces
- [ ] Artifact paths validated (Pattern-type only)
- [ ] Interface specs documented (Service-type only)

### Post-Migration Checklist

- [ ] YAML manifest passes JSON Schema validation
- [ ] Pre-commit hook passes all checks
- [ ] Namespace resolves in registry
- [ ] Legacy alias resolves correctly
- [ ] Dependencies resolve without errors
- [ ] Cross-references updated in documentation
- [ ] Code imports updated (if applicable)
- [ ] PyPI package published (Service-type only)

---

## Version History

- **1.0.0** (2025-11-15): Initial migration guide
  - Field mapping table (sap-catalog.json → YAML)
  - Step-by-step migration process
  - Two migration examples (Service + Pattern)
  - Automated script usage
  - Complete SAP-XXX → namespace mapping (45 SAPs)
  - Pilot and full migration plans

---

## Related Documentation

- [Domain Taxonomy](./domain-taxonomy.md) (Week 1.1, ONT-001)
- [Namespace Format Specification](./namespace-spec.md) (Week 1.2, ONT-002)
- [Capability Type Definitions](./capability-types.md) (Week 1.4, ONT-004)
- [YAML Manifest Templates](../capabilities/template-service.yaml) (Week 2.2, ONT-006)
- [Migration Script](../../scripts/migrate-sap-catalog.py) (Week 3.3, ONT-011)

---

**Next Steps**:
1. Week 1.4: Define unified capability types (ONT-004)
2. Week 2: Create YAML templates and JSON Schema validators
3. Week 3: Implement migration script and automation
4. Week 4: Execute pilot migration (8 capabilities)
