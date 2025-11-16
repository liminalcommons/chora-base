# Chora Extensions Specification

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-11-15

---

## Overview

This document specifies the **chora extension namespaces** for capability manifests. These extensions complement Dublin Core metadata with chora-specific fields for Service-type capabilities, Pattern-type capabilities, and adoption tracking.

### Extension Namespaces

| Namespace | Purpose | Used By | Required |
|-----------|---------|---------|----------|
| `chora_service` | Runtime service specification | Service-type capabilities | Yes (for Service) |
| `chora_pattern` | Knowledge artifact specification | Pattern-type capabilities | Yes (for Pattern) |
| `chora_adoption` | Adoption metrics and tracking | Both types | Optional |

### Design Principles

1. **Separation of Concerns**: Dublin Core for metadata, chora extensions for implementation
2. **Type-Specific**: Each capability type has its own extension namespace
3. **Optional Metrics**: Adoption tracking is opt-in for both types
4. **Validation-Ready**: All fields have JSON Schema definitions
5. **Forward-Compatible**: Reserved fields for future extensions

---

## 1. chora_service Extension

**Purpose**: Specify runtime characteristics for Service-type capabilities

**Scope**: Multi-interface support, health monitoring, distribution packaging

**Required For**: All Service-type capabilities (`dc_type: "Service"`)

**Schema Location**: `schemas/capability-service.schema.json`

---

### 1.1 Structure Overview

```yaml
spec:
  chora_service:
    # REQUIRED: Interface specifications
    interfaces:
      - type: cli | rest | mcp
        # ... interface-specific fields

    # REQUIRED: Health monitoring
    health:
      endpoint: /health
      interval: 10s
      # ... health fields

    # REQUIRED: Distribution packaging
    distribution:
      pypi_package: chora-*
      # ... distribution fields
```

---

### 1.2 Field: interfaces

**Type**: Array (minimum 1 item)
**Required**: Yes
**Purpose**: Define all interfaces this service provides

**Schema**:
```json
{
  "type": "array",
  "minItems": 1,
  "items": {
    "type": "object",
    "required": ["type"],
    "properties": {
      "type": {"enum": ["cli", "rest", "mcp"]}
    }
  }
}
```

**Validation Rules**:
- At least one interface required
- Each interface must have unique `type`
- Interface-specific fields required based on `type`

---

#### 1.2.1 CLI Interface

**Type**: Command-line interface via executable or entry point

**Required Fields**:
```yaml
- type: cli
  command: string         # Executable command name (e.g., "chora-registry")
  entrypoint: string      # Python entry point (e.g., "chora.registry.cli:main")
```

**Optional Fields**:
```yaml
  description: string     # Human-readable description
  help_url: uri          # URL to CLI documentation
  config_file: string     # Default config file path (e.g., "~/.chora/registry.yaml")
```

**Example**:
```yaml
interfaces:
  - type: cli
    command: chora-registry
    entrypoint: chora.registry.cli:main
    description: "CLI for service registry operations"
    help_url: https://docs.chora.dev/registry/cli
    config_file: ~/.chora/registry.yaml
```

**Validation**:
- `command` must be lowercase, alphanumeric + hyphens
- `entrypoint` must match Python module:function format
- `entrypoint` must exist in distribution package

---

#### 1.2.2 REST Interface

**Type**: HTTP REST API server

**Required Fields**:
```yaml
- type: rest
  port: integer           # HTTP port (1-65535)
```

**Optional Fields**:
```yaml
  host: string            # Bind address (default: "0.0.0.0")
  openapi: string         # OpenAPI spec path (e.g., "/api/v1/openapi.json")
  description: string     # Human-readable description
  cors_enabled: boolean   # CORS support (default: false)
  auth_required: boolean  # Authentication required (default: true)
```

**Example**:
```yaml
interfaces:
  - type: rest
    port: 8000
    host: 0.0.0.0
    openapi: /api/v1/openapi.json
    description: "REST API for programmatic registry access"
    cors_enabled: true
    auth_required: true
```

**Validation**:
- `port` must be in range 1-65535
- `port` must not conflict with other services
- `openapi` path must be valid URI path
- If `openapi` specified, file must exist in package

---

#### 1.2.3 MCP Interface

**Type**: Model Context Protocol for Claude Desktop integration

**Required Fields**:
```yaml
- type: mcp
  transport: stdio | sse   # Transport protocol
  server_info:
    name: string           # MCP server name
    version: string        # MCP server version (SemVer)
```

**Optional Fields**:
```yaml
  description: string      # Human-readable description
  capabilities:            # MCP capabilities
    tools: boolean         # Supports tools (default: true)
    resources: boolean     # Supports resources (default: false)
    prompts: boolean       # Supports prompts (default: false)
  config_schema: uri       # JSON Schema for MCP config
```

**Example**:
```yaml
interfaces:
  - type: mcp
    transport: stdio
    server_info:
      name: chora-registry
      version: "1.0.0"
    description: "MCP server for registry operations"
    capabilities:
      tools: true
      resources: true
      prompts: false
    config_schema: https://schemas.chora.dev/registry/mcp-config.json
```

**Validation**:
- `transport` must be "stdio" or "sse"
- `server_info.version` must match `dc_hasVersion`
- `server_info.name` should match PyPI package name
- If `config_schema` specified, must be valid URI

---

### 1.3 Field: health

**Type**: Object
**Required**: Yes
**Purpose**: Define health check and monitoring configuration

**Schema**:
```json
{
  "type": "object",
  "required": ["endpoint", "interval"],
  "properties": {
    "endpoint": {"type": "string"},
    "interval": {"type": "string", "pattern": "^[0-9]+(s|m|h)$"}
  }
}
```

**Required Fields**:
```yaml
health:
  endpoint: string        # Health check HTTP endpoint (e.g., "/health")
  interval: duration      # Check frequency (e.g., "10s", "1m")
```

**Optional Fields**:
```yaml
  timeout: duration       # Maximum response time (default: interval / 2)
  heartbeat_ttl: duration # Registry TTL (default: interval * 3)
  liveness_probe: string  # Kubernetes liveness endpoint (e.g., "/health/live")
  readiness_probe: string # Kubernetes readiness endpoint (e.g., "/health/ready")
  startup_probe: string   # Kubernetes startup endpoint (e.g., "/health/startup")
```

**Example**:
```yaml
health:
  endpoint: /health
  interval: 10s
  timeout: 5s
  heartbeat_ttl: 30s
  liveness_probe: /health/live
  readiness_probe: /health/ready
  startup_probe: /health/startup
```

**Validation**:
- `endpoint` must be valid URI path
- `interval` must be duration format (number + s/m/h)
- `timeout` must be less than `interval`
- `heartbeat_ttl` should be at least 2x `interval`
- Kubernetes probe endpoints must be distinct

**Duration Format**:
- `s` - seconds (e.g., "10s", "30s")
- `m` - minutes (e.g., "1m", "5m")
- `h` - hours (e.g., "1h", "24h")

**Health Endpoint Requirements**:
- Must return HTTP 200 when healthy
- Must return HTTP 503 when unhealthy
- Response should include JSON status (optional):
  ```json
  {
    "status": "healthy" | "unhealthy",
    "timestamp": "2025-11-15T10:30:00Z",
    "dependencies": {
      "database": "healthy",
      "redis": "healthy"
    }
  }
  ```

---

### 1.4 Field: distribution

**Type**: Object
**Required**: Yes
**Purpose**: Define how service is packaged and distributed

**Schema**:
```json
{
  "type": "object",
  "required": ["pypi_package"],
  "properties": {
    "pypi_package": {"type": "string", "pattern": "^chora-.*"}
  }
}
```

**Required Fields**:
```yaml
distribution:
  pypi_package: string    # PyPI package name (must start with "chora-")
```

**Optional Fields**:
```yaml
  pypi_classifiers: array # PyPI trove classifiers
  docker_image: uri       # Docker image URL (e.g., "ghcr.io/chora-base/registry:1.0.0")
  docker_platforms: array # Supported platforms (e.g., ["linux/amd64", "linux/arm64"])
  install_requires: array # Python dependencies (for reference only, use pyproject.toml)
  extras_require: object  # Optional dependency groups
```

**Example**:
```yaml
distribution:
  pypi_package: chora-registry
  pypi_classifiers:
    - "Development Status :: 4 - Beta"
    - "Intended Audience :: Developers"
    - "Topic :: Software Development :: Libraries"
    - "Programming Language :: Python :: 3"
    - "Programming Language :: Python :: 3.11"
    - "Programming Language :: Python :: 3.12"
  docker_image: ghcr.io/chora-base/registry:1.0.0
  docker_platforms:
    - linux/amd64
    - linux/arm64
  extras_require:
    postgres:
      - psycopg2-binary>=2.9.0
    redis:
      - redis>=5.0.0
```

**Validation**:
- `pypi_package` must start with "chora-"
- `pypi_package` must be lowercase, alphanumeric + hyphens
- `pypi_package` should match `dc_identifier` (chora.domain.capability → chora-domain-capability or chora-capability)
- `pypi_classifiers` must be valid PyPI classifiers (see https://pypi.org/classifiers/)
- `docker_image` must be valid URI with version tag
- `docker_platforms` must be valid Docker platform identifiers
- Docker image tag should match `dc_hasVersion`

**Naming Convention**:
- **Full format**: `chora-{domain}-{capability}` (e.g., `chora-registry-lookup`)
- **Short format**: `chora-{capability}` (e.g., `chora-registry`) - use when domain is redundant
- **Avoid**: `chora-{domain}` without capability suffix

---

### 1.5 Complete Service Example

```yaml
apiVersion: chora.dev/v1
kind: Capability

metadata:
  dc_identifier: chora.registry.lookup
  dc_title: "Service Registry & Discovery"
  dc_description: "Service mesh with capability discovery, health monitoring, and dependency resolution"
  dc_type: "Service"
  dc_hasVersion: "1.0.0"
  dc_format: "application/x-executable"
  dc_creator: "Chora Core Team"
  dc_date: "2025-11-15"

status: pilot

spec:
  chora_service:
    interfaces:
      - type: cli
        command: chora-registry
        entrypoint: chora.registry.cli:main
        description: "CLI for registry operations"
        config_file: ~/.chora/registry.yaml

      - type: rest
        port: 8000
        openapi: /api/v1/openapi.json
        description: "REST API for programmatic access"
        cors_enabled: true

      - type: mcp
        transport: stdio
        server_info:
          name: chora-registry
          version: "1.0.0"
        description: "MCP server for Claude Desktop"
        capabilities:
          tools: true
          resources: true

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
        - "Programming Language :: Python :: 3.12"
      docker_image: ghcr.io/chora-base/registry:1.0.0
      docker_platforms:
        - linux/amd64
        - linux/arm64
```

---

## 2. chora_pattern Extension

**Purpose**: Specify knowledge artifacts for Pattern-type capabilities

**Scope**: SAP artifact references, learning path metadata

**Required For**: All Pattern-type capabilities (`dc_type: "Pattern"`)

**Schema Location**: `schemas/capability-pattern.schema.json`

---

### 2.1 Structure Overview

```yaml
spec:
  chora_pattern:
    # REQUIRED: SAP artifacts (exactly 5)
    artifacts:
      - type: capability-charter | protocol-spec | awareness-guide | adoption-blueprint | ledger
        path: string
        # ... artifact fields
```

---

### 2.2 Field: artifacts

**Type**: Array (exactly 5 items)
**Required**: Yes
**Purpose**: Reference the 5 standard SAP artifacts

**Schema**:
```json
{
  "type": "array",
  "minItems": 5,
  "maxItems": 5,
  "items": {
    "type": "object",
    "required": ["type", "path"],
    "properties": {
      "type": {
        "enum": [
          "capability-charter",
          "protocol-spec",
          "awareness-guide",
          "adoption-blueprint",
          "ledger"
        ]
      },
      "path": {
        "type": "string",
        "pattern": "^docs/skilled-awareness/[a-z_-]+/[a-z_-]+\\.md$"
      }
    }
  }
}
```

**Validation Rules**:
- Exactly 5 artifacts required (no more, no less)
- All 5 types must be present (one of each)
- Paths must point to existing markdown files
- Paths must follow pattern: `docs/skilled-awareness/{domain}/{filename}.md`
- No duplicate types allowed

---

#### 2.2.1 Artifact Types

**1. capability-charter**

**Purpose**: Problem statement, solution design, success criteria
**Required Sections**:
- Problem Statement: What problem does this capability solve?
- Solution Design: How does the capability solve it?
- Success Criteria: How do we measure successful adoption?

**Example**:
```yaml
- type: capability-charter
  path: docs/skilled-awareness/react-form-validation/capability-charter.md
  description: "Problem, solution, and success criteria for React form validation"
  last_updated: "2025-11-15"
```

---

**2. protocol-spec**

**Purpose**: Complete technical specification, commands, API reference
**Required Sections**:
- Commands/API Reference: All interfaces and entry points
- Configuration: Required settings and options
- Workflows: Step-by-step technical procedures

**Example**:
```yaml
- type: protocol-spec
  path: docs/skilled-awareness/react-form-validation/protocol-spec.md
  description: "Complete technical specification for React Hook Form + Zod patterns"
  last_updated: "2025-11-15"
```

---

**3. awareness-guide**

**Purpose**: Operating patterns for AI agents (AGENTS.md)
**Required Sections**:
- Quick Reference: High-level patterns and commands
- Integration Patterns: How to combine with other SAPs
- Common Workflows: Step-by-step guides

**Note**: This can be named `awareness-guide.md` or `AGENTS.md` (both acceptable)

**Example**:
```yaml
- type: awareness-guide
  path: docs/skilled-awareness/react-form-validation/awareness-guide.md
  description: "Agent patterns for form validation adoption"
  last_updated: "2025-11-15"
```

---

**4. adoption-blueprint**

**Purpose**: Step-by-step installation and setup guide
**Required Sections**:
- Prerequisites: Required dependencies and setup
- Installation Steps: Numbered installation procedures
- Verification: How to confirm successful adoption

**Example**:
```yaml
- type: adoption-blueprint
  path: docs/skilled-awareness/react-form-validation/adoption-blueprint.md
  description: "Step-by-step installation guide"
  last_updated: "2025-11-15"
```

---

**5. ledger**

**Purpose**: Adoption tracking, metrics, feedback, version history
**Required Sections**:
- Adoption Log: Who adopted, when, project context
- Metrics: Time savings, complexity, ROI
- Feedback: Lessons learned and improvements
- Version History: Changes and updates

**Example**:
```yaml
- type: ledger
  path: docs/skilled-awareness/react-form-validation/ledger.md
  description: "Adoption tracking and metrics"
  last_updated: "2025-11-15"
```

---

#### 2.2.2 Artifact Fields

**Required Fields**:
```yaml
artifacts:
  - type: string          # One of 5 artifact types
    path: string          # File path relative to repo root
```

**Optional Fields**:
```yaml
    description: string   # Human-readable description
    last_updated: date    # ISO 8601 date (YYYY-MM-DD)
    word_count: integer   # Approximate word count
    estimated_read_time: integer  # Minutes to read
```

---

### 2.3 Complete Pattern Example

```yaml
apiVersion: chora.dev/v1
kind: Capability

metadata:
  dc_identifier: chora.react.form_validation
  dc_title: "React Form Validation Patterns"
  dc_description: "React Hook Form + Zod validation patterns with type safety and accessibility"
  dc_type: "Pattern"
  dc_hasVersion: "1.0.0"
  dc_format: "text/markdown"
  dc_creator: "Chora Core Team"
  dc_date: "2025-11-15"

status: pilot

spec:
  chora_pattern:
    artifacts:
      - type: capability-charter
        path: docs/skilled-awareness/react-form-validation/capability-charter.md
        description: "Problem, solution, and success criteria"
        last_updated: "2025-11-15"
        estimated_read_time: 10

      - type: protocol-spec
        path: docs/skilled-awareness/react-form-validation/protocol-spec.md
        description: "React Hook Form + Zod technical specification"
        last_updated: "2025-11-15"
        estimated_read_time: 20

      - type: awareness-guide
        path: docs/skilled-awareness/react-form-validation/awareness-guide.md
        description: "Agent patterns for form validation"
        last_updated: "2025-11-15"
        estimated_read_time: 15

      - type: adoption-blueprint
        path: docs/skilled-awareness/react-form-validation/adoption-blueprint.md
        description: "Step-by-step installation guide"
        last_updated: "2025-11-15"
        estimated_read_time: 25

      - type: ledger
        path: docs/skilled-awareness/react-form-validation/ledger.md
        description: "Adoption tracking and metrics"
        last_updated: "2025-11-15"
        estimated_read_time: 10
```

---

## 3. chora_adoption Extension

**Purpose**: Track adoption metrics and ROI for both Service and Pattern types

**Scope**: Effort estimation, complexity rating, time savings, success tracking

**Required For**: Neither (optional for both types)

**Schema Location**: Both `capability-service.schema.json` and `capability-pattern.schema.json`

---

### 3.1 Structure Overview

```yaml
spec:
  chora_adoption:
    # Effort to adopt capability
    effort_minutes: integer
    complexity: low | medium | high

    # Return on investment
    time_savings_minutes: integer
    roi_percentage: number

    # Success tracking (optional)
    adoptions: array
```

---

### 3.2 Field Definitions

**effort_minutes**

**Type**: Integer (positive)
**Required**: No
**Purpose**: Estimated time to adopt this capability (setup + learning)

**Examples**:
- Service-type: `effort_minutes: 60` (1 hour to install and configure)
- Pattern-type: `effort_minutes: 120` (2 hours to read artifacts and adopt patterns)

**Validation**:
- Must be positive integer
- Should be realistic estimate (not marketing)
- Should include setup time + first-use learning curve

---

**complexity**

**Type**: Enum (low | medium | high)
**Required**: No
**Purpose**: Subjective complexity rating for adoption

**Definitions**:
- `low`: Minimal prerequisites, straightforward adoption (e.g., SAP-016 link validation)
- `medium`: Some prerequisites, moderate learning curve (e.g., SAP-041 form validation)
- `high`: Complex prerequisites, steep learning curve (e.g., SAP-046 saga composition)

**Example**:
```yaml
complexity: medium
```

---

**time_savings_minutes**

**Type**: Integer (positive)
**Required**: No
**Purpose**: Estimated time saved per usage after adoption

**Calculation**:
- **Service-type**: Time saved by automation vs manual operations
- **Pattern-type**: Time saved by reusing patterns vs building from scratch

**Examples**:
- Service-type: `time_savings_minutes: 480` (8 hours saved by automated deployment vs manual)
- Pattern-type: `time_savings_minutes: 150` (2.5 hours saved by form validation patterns vs custom implementation)

**Validation**:
- Must be positive integer
- Should be per-usage estimate (not lifetime)
- Should be conservative estimate based on actual data

---

**roi_percentage**

**Type**: Number (positive)
**Required**: No
**Purpose**: Return on investment percentage

**Formula**:
```
ROI % = (time_savings_minutes / effort_minutes) × 100
```

**Example**:
```yaml
effort_minutes: 60
time_savings_minutes: 480
roi_percentage: 800.0  # (480 / 60) × 100 = 800%
```

**Interpretation**:
- **< 100%**: Net loss (more effort than savings)
- **100-500%**: Good ROI (5x return or less)
- **500-1000%**: Excellent ROI (5-10x return)
- **> 1000%**: Outstanding ROI (10x+ return)

---

**adoptions**

**Type**: Array of objects
**Required**: No
**Purpose**: Track adoption instances for metrics validation

**Schema**:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "project": {"type": "string"},
      "date": {"type": "string", "format": "date"},
      "adopter": {"type": "string"},
      "feedback": {"type": "string"}
    }
  }
}
```

**Example**:
```yaml
adoptions:
  - project: chora-base
    date: "2025-11-15"
    adopter: "Chora Core Team"
    actual_effort_minutes: 55
    actual_savings_minutes: 520
    feedback: "Form validation patterns saved significant development time"

  - project: example-app
    date: "2025-11-20"
    adopter: "External Developer"
    actual_effort_minutes: 75
    actual_savings_minutes: 450
    feedback: "Documentation excellent, Zod integration tricky"
```

**Optional Adoption Fields**:
- `actual_effort_minutes`: Actual time to adopt (vs estimated)
- `actual_savings_minutes`: Actual time saved (vs estimated)
- `feedback`: Qualitative feedback and lessons learned
- `url`: Link to adoption evidence (PR, blog post, etc.)

---

### 3.3 Complete Adoption Example (Service)

```yaml
spec:
  chora_service:
    # ... service fields

  chora_adoption:
    effort_minutes: 60
    complexity: low
    time_savings_minutes: 480
    roi_percentage: 800.0
    adoptions:
      - project: chora-base
        date: "2025-11-15"
        adopter: "Chora Core Team"
        actual_effort_minutes: 55
        actual_savings_minutes: 520
```

---

### 3.4 Complete Adoption Example (Pattern)

```yaml
spec:
  chora_pattern:
    # ... pattern fields

  chora_adoption:
    effort_minutes: 120
    complexity: medium
    time_savings_minutes: 150
    roi_percentage: 125.0
    adoptions:
      - project: chora-base
        date: "2025-11-15"
        adopter: "Chora Core Team"
        actual_effort_minutes: 110
        actual_savings_minutes: 160
        feedback: "Zod integration more complex than expected"

      - project: example-app
        date: "2025-11-20"
        adopter: "External Developer"
        actual_effort_minutes: 130
        actual_savings_minutes: 140
        feedback: "Documentation excellent"
```

---

## 4. Cross-Extension Integration

### 4.1 Service + Adoption

**Use Case**: Track ROI for runtime capability servers

**Example**: Registry service saves 8 hours per deployment cycle

```yaml
spec:
  chora_service:
    interfaces:
      - type: cli
        command: chora-registry

  chora_adoption:
    effort_minutes: 30          # 30 minutes to install and configure
    time_savings_minutes: 480   # 8 hours saved per deployment cycle
    roi_percentage: 1600.0      # 16x return on investment
    complexity: low
```

---

### 4.2 Pattern + Adoption

**Use Case**: Track ROI for knowledge patterns

**Example**: Form validation patterns save 2.5 hours per form implementation

```yaml
spec:
  chora_pattern:
    artifacts:
      - type: capability-charter
        path: docs/skilled-awareness/react-form-validation/capability-charter.md
      # ... 4 more artifacts

  chora_adoption:
    effort_minutes: 120         # 2 hours to read artifacts and learn
    time_savings_minutes: 150   # 2.5 hours saved per form
    roi_percentage: 125.0       # 1.25x return on first use, compounds with multiple forms
    complexity: medium
```

---

### 4.3 Adoption Metrics Best Practices

**For Service-Type**:
1. Measure setup time (installation + configuration + first healthy deployment)
2. Measure time savings per operational cycle (deployment, monitoring, troubleshooting)
3. Calculate ROI based on frequency of operations
4. Update metrics based on actual adoption feedback

**For Pattern-Type**:
1. Measure learning time (reading all 5 artifacts + understanding examples)
2. Measure time savings per pattern application (vs building from scratch)
3. Calculate ROI based on pattern reuse (compounds with multiple applications)
4. Update metrics based on adopter feedback

**Common Pitfalls**:
- **Over-optimistic estimates**: Use conservative numbers
- **Ignoring learning curve**: Include first-use overhead
- **Missing compounding**: Pattern ROI improves with reuse
- **Outdated metrics**: Update based on real adoption data

---

## 5. Extension Versioning

### 5.1 Version Compatibility

**Current Version**: 1.0.0
**Schema Version**: chora.dev/v1
**JSON Schema Draft**: 07

**Compatibility Matrix**:

| chora.dev API | chora_service | chora_pattern | chora_adoption |
|---------------|---------------|---------------|----------------|
| v1 | 1.0.0 | 1.0.0 | 1.0.0 |

**Future API Versions**:
- `chora.dev/v2`: May introduce new extension namespaces
- `chora.dev/v1alpha1`: Experimental extensions
- `chora.dev/v1beta1`: Beta extensions

---

### 5.2 Breaking Changes Policy

**What constitutes a breaking change**:
- Removing required fields
- Changing field types
- Changing validation rules (stricter)
- Removing enum values

**What is NOT a breaking change**:
- Adding optional fields
- Adding enum values
- Relaxing validation rules
- Adding new extension namespaces

**Deprecation Process**:
1. **Deprecation announcement**: Mark field as deprecated in schema
2. **Deprecation period**: Minimum 6 months with warnings
3. **Removal**: Next major version (v2.0.0)

---

### 5.3 Reserved Fields

**Reserved for future extensions**:

```yaml
spec:
  # Reserved: Future extension namespaces
  chora_workflow:         # Workflow orchestration metadata (planned v1.1.0)
  chora_security:         # Security and compliance metadata (planned v1.2.0)
  chora_observability:    # Observability and telemetry (planned v1.3.0)
  chora_cost:             # Cost tracking and optimization (planned v2.0.0)
```

**Do NOT use these namespaces** - they are reserved for future official extensions.

**Custom Extensions**:
- Use vendor-specific namespace: `vendor_mycompany_*`
- Example: `vendor_acme_deployment` for Acme Corp-specific deployment metadata
- Custom extensions not validated by official JSON Schema

---

## 6. JSON Schema Integration

### 6.1 Schema Files

**Location**: `schemas/`

**Files**:
- `capability-common.schema.json` - Shared definitions (used by both)
- `capability-service.schema.json` - Service-type + chora_service + chora_adoption
- `capability-pattern.schema.json` - Pattern-type + chora_pattern + chora_adoption

---

### 6.2 Schema Validation

**Command**:
```bash
python scripts/validate-capability.py capabilities/chora.domain.capability.yaml
```

**Pre-commit Hook**:
```bash
pre-commit run validate-capabilities --all-files
```

**CI/CD Workflow**:
```yaml
- name: Validate capability manifests
  run: python scripts/validate-all-capabilities.py capabilities/
```

---

### 6.3 Validation Examples

**Valid Service-Type**:
```yaml
spec:
  chora_service:  # ✅ REQUIRED for Service
    interfaces:   # ✅ At least 1 interface
      - type: cli
        command: chora-registry
        entrypoint: chora.registry.cli:main
    health:       # ✅ Health monitoring
      endpoint: /health
      interval: 10s
    distribution: # ✅ Distribution info
      pypi_package: chora-registry
```

**Invalid Service-Type** (missing required fields):
```yaml
spec:
  chora_service:
    interfaces:
      - type: cli
        command: chora-registry
        # ❌ Missing: entrypoint
    # ❌ Missing: health
    # ❌ Missing: distribution
```

**Valid Pattern-Type**:
```yaml
spec:
  chora_pattern:  # ✅ REQUIRED for Pattern
    artifacts:    # ✅ Exactly 5 artifacts
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

**Invalid Pattern-Type** (wrong artifact count):
```yaml
spec:
  chora_pattern:
    artifacts:  # ❌ Only 3 artifacts (need exactly 5)
      - type: capability-charter
        path: docs/skilled-awareness/test/capability-charter.md
      - type: protocol-spec
        path: docs/skilled-awareness/test/protocol-spec.md
      - type: awareness-guide
        path: docs/skilled-awareness/test/awareness-guide.md
    # ❌ Missing: adoption-blueprint, ledger
```

---

## 7. Migration from sap-catalog.json

### 7.1 Mapping Legacy Fields

**sap-catalog.json → YAML manifest**:

| sap-catalog.json | YAML spec field | Notes |
|------------------|-----------------|-------|
| N/A (implicit) | `chora_service` or `chora_pattern` | Derived from SAP type |
| N/A | `chora_service.interfaces` | All SAPs support CLI (future: MCP) |
| N/A | `chora_service.health` | Default: `endpoint: /health, interval: 10s` |
| N/A | `chora_service.distribution.pypi_package` | Derived from `name` field |
| N/A | `chora_pattern.artifacts` | Generated from SAP directory structure |
| `metrics.effort_minutes` | `chora_adoption.effort_minutes` | Direct mapping |
| `metrics.complexity` | `chora_adoption.complexity` | Direct mapping |
| `metrics.time_savings_minutes` | `chora_adoption.time_savings_minutes` | Direct mapping |
| `metrics.roi_percentage` | `chora_adoption.roi_percentage` | Direct mapping |

---

### 7.2 Migration Script

**Command**:
```bash
python scripts/migrate-sap-catalog.py \
  --input sap-catalog.json \
  --output capabilities/ \
  --sap-id SAP-041
```

**Output**:
```
capabilities/chora.react.form_validation.yaml
```

**Auto-generated Fields**:
- `chora_pattern.artifacts` - Scans `docs/skilled-awareness/react-form-validation/`
- `chora_adoption.*` - Copies from sap-catalog.json `metrics` field
- `dc_identifier` - Converts SAP-041 → chora.react.form_validation

---

### 7.3 Dual-Mode Support (v5.2.0 - v6.0.0)

**During migration period**, both systems coexist:

**Legacy Lookup** (sap-catalog.json):
```bash
cat sap-catalog.json | jq '.saps[] | select(.id == "SAP-041")'
```

**Unified Lookup** (YAML manifest):
```bash
cat capabilities/chora.react.form_validation.yaml
```

**Deprecation Timeline**:
- **v5.2.0** (Week 4): Pilot migration (8 capabilities)
- **v5.3.0** (Week 8): Full migration (45 capabilities)
- **v5.5.0** (Week 16): Deprecation warnings for sap-catalog.json lookups
- **v6.0.0** (Q2 2026): Remove sap-catalog.json

---

## 8. Related Documentation

**Ontology Framework**:
- [Domain Taxonomy](./domain-taxonomy.md) - 20 domain definitions
- [Namespace Specification](./namespace-spec.md) - 3-level namespace format
- [Dublin Core Schema](./dublin-core-schema.md) - Metadata element set
- [Capability Types](./capability-types.md) - Service vs Pattern distinction
- [Migration Guide](./migration-guide.md) - sap-catalog.json migration

**Templates**:
- [Service Template](../capabilities/template-service.yaml) - Service-type template
- [Pattern Template](../capabilities/template-pattern.yaml) - Pattern-type template

**Validation**:
- [JSON Schema README](../schemas/README.md) - Validation usage and examples
- [Common Schema](../schemas/capability-common.schema.json) - Shared definitions
- [Service Schema](../schemas/capability-service.schema.json) - Service validation
- [Pattern Schema](../schemas/capability-pattern.schema.json) - Pattern validation

---

## 9. Version History

- **1.0.0** (2025-11-15): Initial chora extensions specification
  - `chora_service` - Multi-interface, health, distribution
  - `chora_pattern` - SAP artifacts (5 types)
  - `chora_adoption` - Effort, complexity, ROI
  - Complete field definitions with validation rules
  - Migration mapping from sap-catalog.json
  - Reserved fields for future extensions

---

**Status**: Complete ✅
**JSON Schema Integration**: Available in `schemas/` directory
**Last Updated**: 2025-11-15
