# Dublin Core Metadata Schema

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-11-15
**Part of**: Ecosystem Ontology & Composition Vision (SAP-048)
**Standard**: ISO 15836:2009 - Dublin Core Metadata Element Set v1.1

---

## Purpose

This document defines the metadata schema for chora ecosystem capabilities using **Dublin Core Metadata Element Set v1.1** (DCMES) with **chora-specific extensions** for Service-type and Pattern-type capabilities.

Dublin Core provides a standardized, interoperable metadata framework recognized internationally (ISO 15836:2009), enabling:

- **Interoperability**: Metadata recognized across systems
- **Discoverability**: Standard search and indexing
- **Extensibility**: Domain-specific extensions (chora namespace)
- **Versioning**: Clear evolution of metadata schemas

---

## Schema Overview

### Core Elements (15 elements from Dublin Core v1.1)

| Element | Property | Description | Required | Repeatable |
|---------|----------|-------------|----------|------------|
| **Identifier** | `dc:identifier` | Unique capability namespace | ✅ Yes | ❌ No |
| **Title** | `dc:title` | Human-readable display name | ✅ Yes | ❌ No |
| **Description** | `dc:description` | One-sentence summary | ✅ Yes | ❌ No |
| **Type** | `dc:type` | Capability type (Service/Pattern) | ✅ Yes | ❌ No |
| **Has Version** | `dc:hasVersion` | SemVer version (x.y.z) | ✅ Yes | ❌ No |
| **Creator** | `dc:creator` | Author or team | ⬜ Optional | ✅ Yes |
| **Date** | `dc:date` | Publication date (ISO 8601) | ⬜ Optional | ❌ No |
| **Relation** | `dc:relation` | Typed dependencies | ⬜ Optional | ✅ Yes |
| **Coverage** | `dc:coverage` | SKOS taxonomy relationships | ⬜ Optional | ✅ Yes |
| **Format** | `dc:format` | MIME type | ⬜ Optional | ❌ No |
| **Subject** | `dc:subject` | Keywords/tags | ⬜ Optional | ✅ Yes |
| **Contributor** | `dc:contributor` | Contributors | ⬜ Optional | ✅ Yes |
| **Publisher** | `dc:publisher` | Publishing entity | ⬜ Optional | ❌ No |
| **Rights** | `dc:rights` | License information | ⬜ Optional | ❌ No |
| **Language** | `dc:language` | ISO 639 language code | ⬜ Optional | ✅ Yes |

### Chora Extensions (3 namespaces)

| Namespace | Purpose | Applies To |
|-----------|---------|------------|
| `chora_service` | Service-type capabilities | Service only |
| `chora_pattern` | Pattern-type capabilities | Pattern only |
| `chora_adoption` | Adoption metrics | Both types |

---

## Core Dublin Core Elements

### 1. dc:identifier (REQUIRED)

**Property**: Unique capability identifier

**Format**: `chora.domain.capability` (3-level hierarchical namespace)

**YAML Mapping**:
```yaml
metadata:
  dc_identifier: chora.react.form_validation
```

**Validation Rules**:
- MUST match regex: `^chora\.[a-z_]+\.[a-z0-9_]{1,50}$`
- MUST be globally unique (checked at commit time)
- MUST use snake_case for capability name
- Maximum length: 100 characters

**Examples**:
```yaml
dc_identifier: chora.registry.lookup
dc_identifier: chora.react.form_validation
dc_identifier: chora.awareness.nested_pattern
```

**Related Spec**: [namespace-spec.md](./namespace-spec.md)

---

### 2. dc:title (REQUIRED)

**Property**: Human-readable display name

**Format**: Free text (max 100 characters)

**YAML Mapping**:
```yaml
metadata:
  dc_title: "React Form Validation Patterns"
```

**Validation Rules**:
- MUST be between 10-100 characters
- SHOULD use Title Case
- SHOULD be descriptive and specific
- SHOULD NOT duplicate `dc_identifier`

**Examples**:
```yaml
dc_title: "Service Registry & Discovery"
dc_title: "React Form Validation Patterns"
dc_title: "Nested Agent Awareness Pattern"
```

---

### 3. dc:description (REQUIRED)

**Property**: One-sentence summary (elevator pitch)

**Format**: Free text (1-2 sentences, max 250 characters)

**YAML Mapping**:
```yaml
metadata:
  dc_description: "React Hook Form + Zod validation patterns for production apps"
```

**Validation Rules**:
- MUST be 1-2 sentences
- MUST be between 20-250 characters
- SHOULD end with period
- SHOULD describe what the capability does (not how)

**Examples**:
```yaml
dc_description: "Service mesh with capability discovery, health monitoring, and dependency resolution"
dc_description: "React Hook Form + Zod validation patterns for production apps"
dc_description: "Nested AGENTS.md/CLAUDE.md awareness pattern for progressive context loading"
```

---

### 4. dc:type (REQUIRED)

**Property**: Capability type classification

**Format**: Enumeration (`"Service"` | `"Pattern"`)

**YAML Mapping**:
```yaml
metadata:
  dc_type: "Service"  # or "Pattern"
```

**Validation Rules**:
- MUST be exactly `"Service"` or `"Pattern"`
- Case-sensitive (use quoted strings)
- MUST match capability implementation:
  - `"Service"`: Runtime capability server (CLI/REST/MCP)
  - `"Pattern"`: Knowledge documentation (5 SAP artifacts)

**Examples**:
```yaml
# Service-type
dc_type: "Service"

# Pattern-type
dc_type: "Pattern"
```

**Related Spec**: [capability-types.md](./capability-types.md)

---

### 5. dc:hasVersion (REQUIRED)

**Property**: Semantic version number

**Format**: SemVer 2.0.0 (`x.y.z`)

**YAML Mapping**:
```yaml
metadata:
  dc_hasVersion: "1.2.3"
```

**Validation Rules**:
- MUST follow SemVer 2.0.0 format: `MAJOR.MINOR.PATCH`
- MUST be quoted string (not number)
- Pre-release versions allowed: `1.0.0-beta.1`
- Build metadata allowed: `1.0.0+20250115`

**SemVer Semantics**:
- **MAJOR**: Breaking changes (e.g., Pattern → Service migration)
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, no API changes

**Examples**:
```yaml
dc_hasVersion: "1.0.0"           # Initial release
dc_hasVersion: "1.2.3"           # Stable version
dc_hasVersion: "2.0.0-beta.1"    # Pre-release
dc_hasVersion: "1.0.0+20250115"  # Build metadata
```

**Related Spec**: https://semver.org/

---

### 6. dc:creator (OPTIONAL)

**Property**: Author or team responsible for capability

**Format**: Free text (person or organization name)

**YAML Mapping**:
```yaml
metadata:
  dc_creator: "Chora Core Team"
```

**Repeatable**: Yes (multiple creators allowed)

**YAML Mapping (Multiple)**:
```yaml
metadata:
  dc_creator:
    - "Alice Johnson"
    - "Bob Smith"
    - "Chora Core Team"
```

**Examples**:
```yaml
dc_creator: "Chora Core Team"
dc_creator: "Alice Johnson <alice@example.com>"
dc_creator:
  - "Alice Johnson"
  - "Bob Smith"
```

---

### 7. dc:date (OPTIONAL)

**Property**: Publication or creation date

**Format**: ISO 8601 date (`YYYY-MM-DD`)

**YAML Mapping**:
```yaml
metadata:
  dc_date: "2025-11-15"
```

**Validation Rules**:
- MUST be ISO 8601 format: `YYYY-MM-DD`
- SHOULD be capability first publication date (not last updated)
- Use `updated_at` (chora extension) for modification tracking

**Examples**:
```yaml
dc_date: "2025-11-15"              # Full date
dc_date: "2025-11"                  # Year-month
dc_date: "2025"                     # Year only
```

---

### 8. dc:relation (OPTIONAL)

**Property**: Typed relationships to other capabilities

**Format**: Structured object with relationship types

**YAML Mapping**:
```yaml
metadata:
  dc_relation:
    requires:                        # Hard dependencies
      - capability: chora.react.foundation
        version: ^1.0.0
        relationship: prerequisite
        description: "Foundation stack required"
    optional:                        # Soft dependencies
      - capability: chora.react.state_management
        version: ^1.0.0
        relationship: complementary
        description: "Enhances with state persistence"
    conflicts:                       # Mutually exclusive
      - capability: chora.react.formik_validation
        relationship: mutually_exclusive
        description: "Cannot use both validation approaches"
```

**Relationship Types**:

**For Service-Type**:
1. **runtime**: Service → Service (hard dependency, must be running)
2. **optional**: Service → Service (soft dependency, can compose)
3. **conditional**: Service → Service (environment-dependent)
4. **prerequisite**: Service → Pattern (advisory, knowledge prereq)

**For Pattern-Type**:
1. **prerequisite**: Pattern → Pattern (hard learning path)
2. **complementary**: Pattern → Pattern (recommended enhancement)
3. **mutually_exclusive**: Pattern ↔ Pattern (conflicts)
4. **extends**: Pattern → Pattern (inheritance)
5. **runtime**: Pattern → Service (hard requirement, service must run)

**Repeatable**: Yes (multiple relationships allowed)

**Validation Rules**:
- All referenced capabilities MUST exist
- Version constraints MUST use valid SemVer operators (`^`, `~`, `>=`, etc.)
- Relationship type MUST be valid for capability type
- Circular dependencies MUST be detected and rejected

**Examples**:

**Service → Service (runtime)**:
```yaml
dc_relation:
  requires:
    - capability: chora.bootstrap.initialize
      version: ^1.0.0
      relationship: runtime
      description: "Bootstrap must start before registry"
```

**Pattern → Pattern (prerequisite)**:
```yaml
dc_relation:
  requires:
    - capability: chora.react.foundation
      version: ^1.0.0
      relationship: prerequisite
      description: "Foundation stack must be adopted first"
```

**Pattern → Service (runtime)**:
```yaml
dc_relation:
  requires:
    - capability: chora.integration.compose
      version: ">=3.0.0"
      relationship: runtime
      description: "chora-compose service must be running"
```

**Related Spec**: [ADDENDUM-SAP-DEPENDENCY-MANAGEMENT.md](../../research/prompts/ADDENDUM-SAP-DEPENDENCY-MANAGEMENT.md)

---

### 9. dc:coverage (OPTIONAL)

**Property**: SKOS taxonomy relationships (broader/narrower/related)

**Format**: Structured object with SKOS properties

**YAML Mapping**:
```yaml
metadata:
  dc_coverage:
    broader:                         # Parent capability
      - chora.devex.testing_framework
    narrower:                        # Child capabilities
      - chora.react.testing
      - chora.vue.testing
    related:                         # Related capabilities
      - chora.workflow.lifecycle
```

**SKOS Relationship Types**:
1. **broader**: Parent in taxonomy hierarchy
2. **narrower**: Children in taxonomy hierarchy
3. **related**: Cross-cutting relationships

**Repeatable**: Yes (multiple relationships allowed)

**Use Cases**:
- Organize capabilities into hierarchies
- Enable faceted search and filtering
- Support "related capabilities" discovery

**Examples**:

**Generic testing framework (parent)**:
```yaml
dc_coverage:
  narrower:
    - chora.react.testing
    - chora.vue.testing
    - chora.angular.testing
```

**React testing (child)**:
```yaml
dc_coverage:
  broader:
    - chora.devex.testing_framework
  related:
    - chora.react.foundation
```

**Related Spec**: W3C SKOS (Simple Knowledge Organization System)

---

### 10. dc:format (OPTIONAL)

**Property**: MIME type of capability

**Format**: MIME type string

**YAML Mapping**:
```yaml
metadata:
  dc_format: "application/x-executable"  # Service-type
  # or
  dc_format: "text/markdown"             # Pattern-type
```

**Standard Values**:
- **Service-type**: `application/x-executable`
- **Pattern-type**: `text/markdown`

**Examples**:
```yaml
# Service-type capability
dc_type: "Service"
dc_format: "application/x-executable"

# Pattern-type capability
dc_type: "Pattern"
dc_format: "text/markdown"
```

---

### 11. dc:subject (OPTIONAL)

**Property**: Keywords or tags for discovery

**Format**: Array of strings

**YAML Mapping**:
```yaml
metadata:
  dc_subject:
    - "form validation"
    - "React"
    - "Zod"
    - "TypeScript"
```

**Repeatable**: Yes (multiple keywords)

**Use Cases**:
- Full-text search indexing
- Tag-based filtering
- Related capability discovery

**Examples**:
```yaml
dc_subject:
  - "service discovery"
  - "health monitoring"
  - "registry"
  - "microservices"
```

---

### 12-15. Other Dublin Core Elements (OPTIONAL)

**dc:contributor**: Additional contributors (beyond `dc:creator`)

**dc:publisher**: Publishing organization (e.g., "Chora Ecosystem")

**dc:rights**: License information (e.g., "MIT", "Apache-2.0")

**dc:language**: ISO 639 language code (e.g., "en", "es", "fr")

**YAML Mapping**:
```yaml
metadata:
  dc_contributor:
    - "Jane Doe <jane@example.com>"
  dc_publisher: "Chora Ecosystem"
  dc_rights: "MIT License"
  dc_language: "en"
```

---

## Chora Extensions

### Extension Namespace: `chora_service` (Service-Type Only)

**Purpose**: Service-type specific metadata

#### chora_service.interfaces (REQUIRED for Service)

**Property**: Multi-interface specification (CLI, REST, MCP)

**YAML Mapping**:
```yaml
spec:
  chora_service:
    interfaces:
      - type: cli
        command: chora-registry
        entrypoint: chora.registry.cli:main
        description: "CLI for capability lookup"
      - type: rest
        port: 8000
        openapi: /api/v1/openapi.json
        description: "REST API for programmatic access"
      - type: mcp
        transport: stdio
        server_info:
          name: chora-registry
          version: "1.0.0"
        description: "MCP server for Claude Desktop"
```

**Interface Types**:
1. **cli**: Command-line interface
2. **rest**: REST API (HTTP)
3. **mcp**: Model Context Protocol server

**Related SAP**: SAP-043 (multi-interface patterns)

---

#### chora_service.health (REQUIRED for Service)

**Property**: Health monitoring configuration

**YAML Mapping**:
```yaml
spec:
  chora_service:
    health:
      endpoint: /health
      interval: 10s
      timeout: 5s
      heartbeat_ttl: 30s
      liveness_probe: /health/live
      readiness_probe: /health/ready
```

**Fields**:
- **endpoint**: Health check HTTP endpoint
- **interval**: Check frequency (duration)
- **timeout**: Max response time (duration)
- **heartbeat_ttl**: Registry heartbeat expiration (duration)
- **liveness_probe**: Liveness check endpoint (Kubernetes-compatible)
- **readiness_probe**: Readiness check endpoint (Kubernetes-compatible)

---

#### chora_service.distribution (REQUIRED for Service)

**Property**: Distribution packaging information

**YAML Mapping**:
```yaml
spec:
  chora_service:
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

**Fields**:
- **pypi_package**: PyPI package name (`chora-*`)
- **pypi_classifiers**: PyPI trove classifiers
- **docker_image**: Docker image URL
- **docker_platforms**: Supported platforms

---

### Extension Namespace: `chora_pattern` (Pattern-Type Only)

**Purpose**: Pattern-type specific metadata

#### chora_pattern.artifacts (REQUIRED for Pattern)

**Property**: SAP artifact references (5 standard files)

**YAML Mapping**:
```yaml
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

**Required Artifact Types** (all 5 must be present):
1. **capability-charter**: Problem statement, solution design
2. **protocol-spec**: Complete technical specification
3. **awareness-guide**: Agent operating patterns
4. **adoption-blueprint**: Step-by-step installation
5. **ledger**: Adoption tracking, feedback, versions

**Validation**:
- All 5 artifact types MUST be present
- All paths MUST exist and be readable
- Paths MUST be relative to repository root

**Related SAP**: SAP-000 (sap-framework)

---

#### chora_pattern.chora_adoption (OPTIONAL)

**Property**: Adoption metrics and success criteria

**YAML Mapping**:
```yaml
spec:
  chora_pattern:
    chora_adoption:
      effort_minutes: 120
      complexity: medium
      time_savings_minutes: 480
      roi_percentage: 300.0
      success_criteria:
        - "React Hook Form v7+ integrated"
        - "Zod schema validation operational"
        - "Form submission handles async errors"
```

**Fields**:
- **effort_minutes**: Time to adopt pattern (integer)
- **complexity**: Adoption complexity (`low` | `medium` | `high`)
- **time_savings_minutes**: Time saved after adoption (integer)
- **roi_percentage**: Return on investment (float)
- **success_criteria**: Testable success conditions (array of strings)

**ROI Calculation**:
```
ROI % = ((time_savings_minutes - effort_minutes) / effort_minutes) * 100
```

**Example**:
```
effort_minutes: 120
time_savings_minutes: 480
ROI % = ((480 - 120) / 120) * 100 = 300%
```

---

### Extension Namespace: `chora_adoption` (Both Types)

**Purpose**: Shared adoption metadata

**YAML Mapping**:
```yaml
spec:
  chora_adoption:
    effort_minutes: 60
    complexity: low
```

**Use Cases**:
- Service-type capabilities with adoption complexity
- Pattern-type capabilities (more common)

---

## Complete Schema Examples

### Example 1: Service-Type Capability (chora.registry.lookup)

```yaml
apiVersion: chora.dev/v1
kind: Capability

metadata:
  # REQUIRED: Dublin Core core elements
  dc_identifier: chora.registry.lookup
  dc_title: "Service Registry & Discovery"
  dc_description: "Service mesh with capability discovery, health monitoring, and dependency resolution"
  dc_type: "Service"
  dc_hasVersion: "1.0.0"

  # OPTIONAL: Dublin Core extended elements
  dc_creator: "Chora Core Team"
  dc_date: "2025-11-12"
  dc_format: "application/x-executable"
  dc_subject:
    - "service discovery"
    - "health monitoring"
    - "registry"
    - "microservices"

  # OPTIONAL: Typed dependencies
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

  # OPTIONAL: SKOS taxonomy
  dc_coverage:
    narrower:
      - chora.registry.health_monitor
      - chora.registry.dependency_resolver

status: pilot

spec:
  chora_service:
    # Multi-interface specification (REQUIRED)
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

    # Health monitoring (REQUIRED)
    health:
      endpoint: /health
      interval: 10s
      timeout: 5s
      heartbeat_ttl: 30s

    # Distribution (REQUIRED)
    distribution:
      pypi_package: chora-registry
      docker_image: ghcr.io/chora-base/registry:1.0.0
```

---

### Example 2: Pattern-Type Capability (chora.react.form_validation)

```yaml
apiVersion: chora.dev/v1
kind: Capability

metadata:
  # REQUIRED: Dublin Core core elements
  dc_identifier: chora.react.form_validation
  dc_title: "React Form Validation Patterns"
  dc_description: "React Hook Form + Zod validation patterns for production apps"
  dc_type: "Pattern"
  dc_hasVersion: "1.0.0"

  # OPTIONAL: Dublin Core extended elements
  dc_creator: "Chora Core Team"
  dc_date: "2025-11-01"
  dc_format: "text/markdown"
  dc_subject:
    - "form validation"
    - "React"
    - "Zod"
    - "TypeScript"
    - "React Hook Form"

  # OPTIONAL: Typed dependencies
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

  # OPTIONAL: SKOS taxonomy
  dc_coverage:
    broader:
      - chora.react.foundation
    related:
      - chora.react.state_management
      - chora.react.accessibility

status: pilot

spec:
  chora_pattern:
    # SAP artifacts (REQUIRED)
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

    # Adoption metadata (OPTIONAL)
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

## Schema Validation

### JSON Schema Validators (Week 2.3 Deliverable)

**Service-Type Validator** (`schemas/capability-service.schema.json`):
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Service-Type Capability Schema",
  "type": "object",
  "required": ["apiVersion", "kind", "metadata", "status", "spec"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["dc_identifier", "dc_title", "dc_description", "dc_type", "dc_hasVersion"],
      "properties": {
        "dc_type": {
          "const": "Service"
        }
      }
    },
    "spec": {
      "type": "object",
      "required": ["chora_service"],
      "properties": {
        "chora_service": {
          "type": "object",
          "required": ["interfaces", "health", "distribution"]
        }
      }
    }
  }
}
```

**Pattern-Type Validator** (`schemas/capability-pattern.schema.json`):
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Pattern-Type Capability Schema",
  "type": "object",
  "required": ["apiVersion", "kind", "metadata", "status", "spec"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["dc_identifier", "dc_title", "dc_description", "dc_type", "dc_hasVersion"],
      "properties": {
        "dc_type": {
          "const": "Pattern"
        }
      }
    },
    "spec": {
      "type": "object",
      "required": ["chora_pattern"],
      "properties": {
        "chora_pattern": {
          "type": "object",
          "required": ["artifacts"]
        }
      }
    }
  }
}
```

---

## Version History

- **1.0.0** (2025-11-15): Initial Dublin Core schema
  - 15 core Dublin Core elements documented
  - 3 chora extension namespaces (service, pattern, adoption)
  - Complete schema examples (Service + Pattern)
  - Validation rules for all fields
  - JSON Schema validator outlines

---

## Related Documentation

- [Domain Taxonomy](./domain-taxonomy.md) (Week 1.1, ONT-001)
- [Namespace Format Specification](./namespace-spec.md) (Week 1.2, ONT-002)
- [Migration Guide](./migration-guide.md) (Week 1.3, ONT-003)
- [Capability Type Definitions](./capability-types.md) (Week 1.4, ONT-004)
- [YAML Manifest Templates](../capabilities/template-service.yaml) (Week 2.2, ONT-006)
- [JSON Schema Validators](../../schemas/) (Week 2.3, ONT-007)

---

**Next Steps**:
1. Week 2.2: Create YAML manifest templates (ONT-006)
2. Week 2.3: Implement JSON Schema validators (ONT-007)
3. Week 2.4: Define SAP-specific metadata fields (ONT-008)
