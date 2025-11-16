# Capability Type Definitions

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-11-15
**Part of**: Ecosystem Ontology & Composition Vision (SAP-048)

---

## Purpose

This document defines the **two unified capability types** in the chora ecosystem: **Service-type** and **Pattern-type**. Understanding these types is critical for:

- Classifying new capabilities correctly
- Choosing appropriate metadata schemas
- Configuring dependency relationships
- Implementing discovery and registry features
- Designing user experiences

---

## Overview

The chora ecosystem manages two fundamentally different kinds of capabilities:

| Aspect | Service-Type | Pattern-Type |
|--------|--------------|--------------|
| **Definition** | Runtime capability servers | Knowledge documentation |
| **Purpose** | Provide executable functionality | Provide learning paths and patterns |
| **Interfaces** | CLI, REST, MCP (SAP-043) | None (documentation only) |
| **Health** | Monitored via heartbeat (10s interval) | N/A (static documentation) |
| **Distribution** | PyPI package + Docker image | Documentation in repository |
| **Adoption** | `pip install chora-*` + configuration | Read 5 SAP artifacts + implement |
| **Dependencies** | `runtime`, `optional`, `conditional` | `prerequisite`, `complementary`, `mutually_exclusive`, `extends` |
| **Examples** | Registry service, Bootstrap orchestrator | React patterns, Testing frameworks |
| **Count (v5.1.0)** | 6 capabilities | 39 capabilities |

---

## Service-Type Capabilities

### Definition

**Service-type capabilities** are runtime capability servers that provide executable functionality via multiple interfaces (CLI, REST, MCP). They are:

- **Deployed** as running services
- **Monitored** for health and availability
- **Discovered** via registry lookup
- **Composed** into workflows and orchestrations

### Characteristics

#### 1. Runtime Execution

Service-type capabilities run as:
- **CLI tools** (e.g., `chora-registry lookup`)
- **REST APIs** (e.g., `GET /api/v1/capabilities`)
- **MCP servers** (e.g., stdio transport for Claude Desktop)
- **Background services** (e.g., heartbeat monitoring daemon)

#### 2. Multi-Interface (SAP-043)

All Service-type capabilities SHOULD provide at least one interface:

**CLI Interface**:
```yaml
chora_service:
  interfaces:
    - type: cli
      command: chora-registry
      entrypoint: chora.registry.cli:main
      description: "CLI for capability lookup"
```

**REST Interface**:
```yaml
chora_service:
  interfaces:
    - type: rest
      port: 8000
      openapi: /api/v1/openapi.json
      description: "REST API for programmatic access"
```

**MCP Interface**:
```yaml
chora_service:
  interfaces:
    - type: mcp
      transport: stdio
      server_info:
        name: chora-registry
        version: "1.0.0"
      description: "MCP server for Claude Desktop"
```

#### 3. Health Monitoring

Service-type capabilities provide health endpoints:

```yaml
chora_service:
  health:
    endpoint: /health
    interval: 10s          # Health check frequency
    timeout: 5s            # Max response time
    heartbeat_ttl: 30s     # Registry heartbeat TTL
    liveness_probe: /health/live
    readiness_probe: /health/ready
```

**Health States**:
- **Healthy**: Service responding within timeout
- **Degraded**: Service slow or partial failure
- **Unhealthy**: Service not responding or failing checks
- **Unknown**: No recent heartbeat (expired TTL)

#### 4. Distribution

Service-type capabilities are distributed via:

**PyPI Package**:
```yaml
chora_service:
  distribution:
    pypi_package: chora-registry
    pypi_classifiers:
      - "Development Status :: 4 - Beta"
      - "Intended Audience :: Developers"
```

**Docker Image**:
```yaml
chora_service:
  distribution:
    docker_image: ghcr.io/chora-base/registry:1.0.0
    docker_platforms:
      - linux/amd64
      - linux/arm64
```

#### 5. Dependency Types (Service → X)

**Service → Service** (runtime dependency):
```yaml
dc_relation:
  requires:
    - capability: chora.bootstrap.initialize
      version: ^1.0.0
      relationship: runtime
      description: "Bootstrap must start before registry"
```

**Service → Service** (optional composition):
```yaml
dc_relation:
  optional:
    - capability: chora.composition.saga
      version: ^1.0.0
      relationship: optional
      description: "Integrates with saga orchestration if available"
```

**Service → Pattern** (knowledge prerequisite):
```yaml
dc_relation:
  requires:
    - capability: chora.interface.multi
      version: ^1.0.0
      relationship: prerequisite
      description: "⚠️ Read multi-interface patterns before deploying"
```

**Validation**: Advisory warning only (not enforced)

### Metadata Profile (Service-Type)

```yaml
apiVersion: chora.dev/v1
kind: Capability

metadata:
  # REQUIRED: Dublin Core core elements
  dc_identifier: chora.domain.capability
  dc_title: "Service Display Name"
  dc_description: "One-sentence service description"
  dc_type: "Service"                        # Fixed: "Service"
  dc_hasVersion: "x.y.z"                    # SemVer

  # OPTIONAL: Dublin Core extended elements
  dc_creator: "Chora Core Team"
  dc_date: "2025-11-15"
  dc_format: "application/x-executable"     # MIME type for services

  # OPTIONAL: Typed dependencies
  dc_relation:
    requires:                                # Hard dependencies
      - capability: chora.bootstrap.initialize
        version: ^1.0.0
        relationship: runtime
    optional:                                # Soft dependencies
      - capability: chora.composition.saga
        version: ^1.0.0
        relationship: optional

status: active | pilot | draft | deprecated

spec:
  chora_service:
    # Multi-interface specification (REQUIRED)
    interfaces:
      - type: cli | rest | mcp
        # ... interface details

    # Health monitoring (REQUIRED)
    health:
      endpoint: /health
      interval: 10s
      timeout: 5s

    # Distribution (REQUIRED)
    distribution:
      pypi_package: chora-domain-capability
      docker_image: ghcr.io/chora-base/domain-capability:x.y.z
```

### Service-Type Examples

#### Example 1: chora.registry.lookup (SAP-044)

**Purpose**: Service discovery and health monitoring

**Interfaces**: CLI, REST, MCP

**Dependencies**:
- `chora.bootstrap.initialize` (runtime, must start first)
- `chora.composition.saga` (optional, integrates if available)

**Health**: `/health` endpoint, 10s interval, 30s TTL

**Distribution**: `pip install chora-registry`, Docker image

---

#### Example 2: chora.bootstrap.initialize (SAP-045)

**Purpose**: Dependency-ordered service startup

**Interfaces**: CLI, Library API

**Dependencies**:
- None (foundational service, no runtime deps)

**Health**: `/health/ready` checks all dependencies started

**Distribution**: `pip install chora-bootstrap`

---

#### Example 3: chora.composition.saga (SAP-046)

**Purpose**: Saga orchestration with circuit breakers

**Interfaces**: REST, MCP

**Dependencies**:
- `chora.registry.lookup` (runtime, discovers services)
- `chora.bootstrap.initialize` (runtime, startup coordination)

**Health**: `/health/circuit-breaker` checks all sagas healthy

**Distribution**: `pip install chora-composition`, Docker image

---

## Pattern-Type Capabilities

### Definition

**Pattern-type capabilities** are knowledge documentation that provides learning paths, adoption methodologies, and best practices. They are:

- **Documented** as SAP artifacts (5 standard files)
- **Adopted** by reading and implementing patterns
- **Referenced** via documentation links
- **Validated** through adoption metrics

### Characteristics

#### 1. Documentation-Only

Pattern-type capabilities are **not runtime services**. They consist of:

- **5 SAP Artifacts** (SAP-000 framework):
  1. Capability Charter (problem, solution, success criteria)
  2. Protocol Spec (complete technical specification)
  3. Awareness Guide (agent operating patterns)
  4. Adoption Blueprint (step-by-step installation)
  5. Ledger (adoption tracking, feedback, versions)

- **Supplementary Documentation**:
  - Code examples
  - Templates and boilerplate
  - Tutorial videos
  - API references (generated)

#### 2. Artifact References

Pattern-type capabilities link to their 5 SAP artifacts:

```yaml
chora_pattern:
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
```

**Validation**: All artifact paths MUST exist and be accessible

#### 3. Adoption Metadata

Pattern-type capabilities track adoption metrics:

```yaml
chora_pattern:
  chora_adoption:
    effort_minutes: 120              # Time to adopt pattern
    complexity: low | medium | high  # Adoption complexity
    time_savings_minutes: 480        # Time saved after adoption
    roi_percentage: 300.0            # ROI calculation
    success_criteria:
      - "React Hook Form v7+ integrated"
      - "Zod schema validation operational"
      - "Form submission handles async errors"
```

#### 4. Learning Paths

Pattern-type capabilities form dependency graphs for learning:

```yaml
dc_relation:
  requires:                             # Hard prerequisites
    - capability: chora.react.foundation
      version: ^1.0.0
      relationship: prerequisite
      description: "Foundation stack required first"
  optional:                             # Recommended enhancements
    - capability: chora.react.state_management
      version: ^1.0.0
      relationship: complementary
      description: "Enhances with state persistence"
```

**Validation**: Topological sort for adoption order

#### 5. Dependency Types (Pattern → X)

**Pattern → Pattern** (prerequisite):
```yaml
dc_relation:
  requires:
    - capability: chora.react.foundation
      version: ^1.0.0
      relationship: prerequisite
      description: "Must adopt foundation first"
```

**Validation**: Topological sort, error if cycle detected

**Pattern → Pattern** (complementary):
```yaml
dc_relation:
  optional:
    - capability: chora.react.state_management
      version: ^1.0.0
      relationship: complementary
      description: "Recommended for state persistence"
```

**Validation**: Suggestion only (not enforced)

**Pattern → Pattern** (mutually exclusive):
```yaml
dc_relation:
  conflicts:
    - capability: chora.react.formik_validation
      version: "*"
      relationship: mutually_exclusive
      description: "Cannot use both validation approaches"
```

**Validation**: Error if both patterns adopted

**Pattern → Pattern** (extends):
```yaml
dc_relation:
  extends:
    - capability: chora.sap.framework_fundamentals
      version: ^1.0.0
      relationship: extends
      description: "Inherits parent properties"
```

**Validation**: Inherit parent metadata

**Pattern → Service** (hard requirement):
```yaml
dc_relation:
  requires:
    - capability: chora.integration.compose
      version: ">=3.0.0"
      relationship: runtime
      description: "chora-compose service must be running"
```

**Validation**: Check service health (error if unhealthy)

### Metadata Profile (Pattern-Type)

```yaml
apiVersion: chora.dev/v1
kind: Capability

metadata:
  # REQUIRED: Dublin Core core elements
  dc_identifier: chora.domain.capability
  dc_title: "Pattern Display Name"
  dc_description: "One-sentence pattern description"
  dc_type: "Pattern"                        # Fixed: "Pattern"
  dc_hasVersion: "x.y.z"                    # SemVer

  # OPTIONAL: Dublin Core extended elements
  dc_creator: "Chora Core Team"
  dc_date: "2025-11-15"
  dc_format: "text/markdown"                # MIME type for docs

  # OPTIONAL: Typed dependencies
  dc_relation:
    requires:                                # Prerequisites
      - capability: chora.react.foundation
        version: ^1.0.0
        relationship: prerequisite
    optional:                                # Complements
      - capability: chora.react.state_management
        version: ^1.0.0
        relationship: complementary
    conflicts:                               # Mutually exclusive
      - capability: chora.react.formik_validation
        relationship: mutually_exclusive

status: active | pilot | draft | deprecated

spec:
  chora_pattern:
    # SAP artifacts (REQUIRED for Pattern-type)
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

    # Adoption metadata (OPTIONAL)
    chora_adoption:
      effort_minutes: 120
      complexity: medium
      time_savings_minutes: 480
      roi_percentage: 300.0
      success_criteria:
        - "Artifact 1 adopted successfully"
        - "Pattern validated in pilot"
```

### Pattern-Type Examples

#### Example 1: chora.react.form_validation (SAP-041)

**Purpose**: React Hook Form + Zod validation patterns

**Artifacts**: 5 SAP artifacts in `docs/skilled-awareness/react-form-validation/`

**Dependencies**:
- `chora.react.foundation` (prerequisite, must adopt first)
- `chora.react.state_management` (complementary, enhances)

**Adoption**: 120 minutes, medium complexity, 300% ROI

**Success Criteria**:
- React Hook Form v7+ integrated
- Zod schema validation operational
- Form submission handles async errors

---

#### Example 2: chora.awareness.nested_pattern (SAP-009)

**Purpose**: Nested AGENTS.md/CLAUDE.md awareness pattern

**Artifacts**: 5 SAP artifacts in `docs/skilled-awareness/agent-awareness/`

**Dependencies**:
- `chora.infrastructure.sap_framework` (prerequisite, SAP fundamentals)

**Adoption**: 60 minutes, low complexity, 500% ROI

**Success Criteria**:
- Root AGENTS.md created
- Domain AGENTS.md files created
- Progressive context loading operational

---

#### Example 3: chora.devex.testing_framework (SAP-004)

**Purpose**: pytest + 85% coverage patterns

**Artifacts**: 5 SAP artifacts in `docs/skilled-awareness/testing-framework/`

**Dependencies**:
- `chora.devex.quality_gates` (complementary, integrates with pre-commit)

**Adoption**: 180 minutes, high complexity, 250% ROI

**Success Criteria**:
- pytest 8.0+ configured
- Coverage ≥85% achieved
- Test suite runs in CI/CD

---

## Cross-Type Dependencies

### Service → Pattern (Advisory)

**Use Case**: Inform developers to read documentation before using a service

**Example**:
```yaml
# chora.composition.saga (Service)
metadata:
  dc_type: "Service"
  dc_relation:
    requires:
      - capability: chora.composition.saga_patterns
        version: ^1.0.0
        relationship: prerequisite
        description: "⚠️ Read saga pattern docs before deploying"
```

**Validation**: Warning message only (not enforced)

**User Experience**:
```bash
$ chora registry resolve chora.composition.saga

⚠️  Knowledge Prerequisites:
- chora.composition.saga_patterns (^1.0.0)
  Read saga pattern documentation before deploying this service.
  Docs: docs/skilled-awareness/composition/saga-patterns/

Proceed with deployment? [y/N]: _
```

---

### Pattern → Service (Hard Requirement)

**Use Case**: Patterns that require services to execute adoption steps

**Example**:
```yaml
# chora.workflow.sap_generation (Pattern)
metadata:
  dc_type: "Pattern"
  dc_relation:
    requires:
      - capability: chora.integration.compose
        version: ">=3.0.0"
        relationship: runtime
        description: "chora-compose service must be running"
```

**Validation**: Check service health (error if unhealthy)

**User Experience**:
```bash
$ chora registry adopt chora.workflow.sap_generation

Checking runtime dependencies...
✗ chora.integration.compose (>=3.0.0) - UNHEALTHY
  Service not running. Start with: pip install chora-compose && chora-compose start

Cannot adopt pattern until all runtime dependencies are healthy.
```

---

## Type Detection Rules

### Automatic Type Detection

The migration script (`scripts/migrate-sap-catalog.py`) uses these rules to determine capability type:

**Service-Type Indicators**:
1. Has `runtime: true` field in sap-catalog.json
2. Has `interfaces` field (cli, rest, mcp)
3. PyPI package name starts with `chora-` (installable)
4. Has `health` configuration
5. Has Docker image in distribution

**Pattern-Type Indicators**:
1. Has `artifacts` field (5 SAP files)
2. Has `effort_minutes` or `adoption` metadata
3. No `runtime: true` flag
4. No `interfaces` field
5. Located in `docs/skilled-awareness/*/`

**Example Detection Logic**:
```python
def detect_capability_type(sap_data: dict) -> str:
    """Detect Service-type vs Pattern-type."""

    # Service-type indicators
    if sap_data.get("runtime") is True:
        return "Service"
    if "interfaces" in sap_data:
        return "Service"
    if "health" in sap_data:
        return "Service"

    # Pattern-type indicators (default)
    if "artifacts" in sap_data:
        return "Pattern"
    if "effort_minutes" in sap_data:
        return "Pattern"

    # Default to Pattern if ambiguous
    return "Pattern"
```

---

## Capability Type Statistics

### Current Distribution (v5.1.0)

**Service-Type Capabilities** (6 total, 13.3%):
- chora.interface.design (SAP-042, pilot)
- chora.interface.multi (SAP-043, pilot)
- chora.registry.lookup (SAP-044, pilot)
- chora.bootstrap.initialize (SAP-045, pilot)
- chora.composition.saga (SAP-046, pilot)
- chora.integration.compose (SAP-017, active)
- chora.integration.compose_meta (SAP-018, active)

**Pattern-Type Capabilities** (39 total, 86.7%):
- Infrastructure (3): sap_framework, inbox, meta_package
- DevEx (7): project_bootstrap, testing_framework, ci_cd, quality_gates, documentation, automation, docker
- React (15): foundation, testing, linting, state_management, styling, performance, accessibility, authentication, database_integration, file_upload, error_handling, realtime, i18n, e2e_testing, monorepo, form_validation
- Awareness (4): nested_pattern, event_memory, task_tracking, sap_evaluation
- Workflow (6): lifecycle, metrics, link_validation, dogfooding, publishing, sap_generation
- Templates (1): capability_server

**Future Growth Target** (v6.0.0, Q2 2026):
- **Service-Type**: 30 capabilities (30%)
- **Pattern-Type**: 70 capabilities (70%)
- **Total**: 100 capabilities

---

## Type-Specific Validation Rules

### Service-Type Validation

**Pre-Commit Hook** (`scripts/validate-service-capability.py`):

1. **Interfaces Required**:
   ```python
   if capability["dc_type"] == "Service":
       assert "chora_service.interfaces" in capability["spec"]
       assert len(capability["spec"]["chora_service"]["interfaces"]) >= 1
   ```

2. **Health Endpoint Required**:
   ```python
   if capability["dc_type"] == "Service":
       assert "chora_service.health" in capability["spec"]
       assert "endpoint" in capability["spec"]["chora_service"]["health"]
   ```

3. **Distribution Required**:
   ```python
   if capability["dc_type"] == "Service":
       assert "chora_service.distribution" in capability["spec"]
       assert "pypi_package" in capability["spec"]["chora_service"]["distribution"]
   ```

4. **MIME Type Validation**:
   ```python
   if capability["dc_type"] == "Service":
       assert capability["metadata"]["dc_format"] == "application/x-executable"
   ```

### Pattern-Type Validation

**Pre-Commit Hook** (`scripts/validate-pattern-capability.py`):

1. **Artifacts Required**:
   ```python
   if capability["dc_type"] == "Pattern":
       assert "chora_pattern.artifacts" in capability["spec"]
       assert len(capability["spec"]["chora_pattern"]["artifacts"]) == 5
   ```

2. **Artifact Types Required**:
   ```python
   REQUIRED_ARTIFACTS = {
       "capability-charter",
       "protocol-spec",
       "awareness-guide",
       "adoption-blueprint",
       "ledger"
   }
   artifact_types = {a["type"] for a in capability["spec"]["chora_pattern"]["artifacts"]}
   assert artifact_types == REQUIRED_ARTIFACTS
   ```

3. **Artifact Paths Exist**:
   ```python
   for artifact in capability["spec"]["chora_pattern"]["artifacts"]:
       path = artifact["path"]
       assert os.path.exists(path), f"Artifact not found: {path}"
   ```

4. **MIME Type Validation**:
   ```python
   if capability["dc_type"] == "Pattern":
       assert capability["metadata"]["dc_format"] == "text/markdown"
   ```

---

## Type Migration Examples

### Converting Pattern → Service

**Scenario**: A Pattern-type capability (documentation) evolves into a Service-type capability (runtime implementation).

**Example**: SAP-047 (capability-server-template) could evolve from documentation to a generator service.

**Migration Steps**:

1. **Update `dc_type`**:
   ```yaml
   metadata:
     dc_type: "Service"  # Was: "Pattern"
   ```

2. **Add Service Specification**:
   ```yaml
   spec:
     chora_service:
       interfaces:
         - type: cli
           command: chora-generate
           entrypoint: chora.templates.cli:main
       health:
         endpoint: /health
       distribution:
         pypi_package: chora-templates
   ```

3. **Keep Pattern Artifacts** (backward compatibility):
   ```yaml
   spec:
     chora_pattern:
       artifacts:  # Keep for documentation
         - type: capability-charter
           path: docs/skilled-awareness/templates/capability-charter.md
         # ... all 5 artifacts
   ```

4. **Update Dependencies**:
   ```yaml
   dc_relation:
     requires:
       - capability: chora.bootstrap.initialize
         version: ^1.0.0
         relationship: runtime  # Was: prerequisite
   ```

5. **Increment Major Version**:
   ```yaml
   dc_hasVersion: "2.0.0"  # Breaking change (Pattern → Service)
   ```

---

## Best Practices

### When to Create Service-Type Capabilities

**✅ Create Service-Type When**:
- Capability provides runtime functionality
- Users need to `pip install` and run the service
- Health monitoring is required
- Service composition is needed (saga, circuit breakers)
- Multiple interfaces are beneficial (CLI + REST + MCP)

**Examples**:
- Registry for service discovery
- Bootstrap for startup orchestration
- Composition for saga workflows
- Integration for LLM orchestration

---

### When to Create Pattern-Type Capabilities

**✅ Create Pattern-Type When**:
- Capability is documentation or methodology
- Users adopt by reading and implementing
- No runtime component is required
- Learning path dependencies make sense
- Success is measured by adoption metrics

**Examples**:
- React patterns (form validation, authentication, database)
- Process patterns (dogfooding, development lifecycle)
- Meta-capabilities (SAP generation, metrics tracking)
- Agent awareness (nested pattern, memory system)

---

### When to Use Cross-Type Dependencies

**Service → Pattern** (advisory):
- Inform developers about required reading
- Link to architecture documentation
- Warn about complexity or prerequisites

**Pattern → Service** (hard requirement):
- Pattern adoption requires tools to be running
- Code generation needs generator service
- Orchestration requires runtime services

---

## Version History

- **1.0.0** (2025-11-15): Initial capability type definitions
  - Service-type specification
  - Pattern-type specification
  - Cross-type dependency rules
  - Validation rules for both types
  - Migration examples (Pattern → Service)
  - Best practices and guidelines

---

## Related Documentation

- [Domain Taxonomy](./domain-taxonomy.md) (Week 1.1, ONT-001)
- [Namespace Format Specification](./namespace-spec.md) (Week 1.2, ONT-002)
- [Migration Guide](./migration-guide.md) (Week 1.3, ONT-003)
- [Dublin Core Metadata Schema](./dublin-core-schema.md) (Week 2.1, ONT-005)
- [YAML Manifest Templates](../capabilities/template-service.yaml) (Week 2.2, ONT-006)

---

**Next Steps**:
1. Week 2.1: Define Dublin Core schema with chora extensions (ONT-005)
2. Week 2.2: Create YAML manifest templates (ONT-006)
3. Week 2.3: Implement JSON Schema validators (ONT-007)
