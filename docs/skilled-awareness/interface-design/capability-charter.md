# SAP-042: Interface Design Patterns - Capability Charter

**SAP ID**: SAP-042
**Name**: Interface Design Patterns
**Status**: Pilot
**Version**: 1.0.0
**Last Updated**: 2025-11-12
**Domain**: Developer Experience

---

## Overview

This Skilled Awareness Package (SAP) establishes **prescriptive patterns for designing clean, consistent interfaces** for capability servers in the chora ecosystem. It addresses the critical challenge of exposing capability functionality through multiple protocols (REST, CLI, gRPC, MCP) while maintaining consistency, avoiding interface drift, and preventing internal implementation details from leaking into public contracts.

**Core Principle**: Interfaces are **contracts** between capability servers and their clients (services, AI agents, humans). Well-designed interfaces enable interoperability, ease of adoption, and system evolution without breaking existing integrations.

---

## Problem Statement

### The Challenge

Capability servers must expose their functionality to diverse clients through multiple interface types:
- **REST APIs** for service-to-service communication and web clients
- **CLI tools** for human operators and scripting
- **MCP (Model Context Protocol)** for AI agent integration
- **Native Python APIs** for direct programmatic access
- **gRPC** (optionally) for high-performance streaming

Without standardized design patterns, teams face:

1. **Interface Drift**: Different interfaces for the same capability expose inconsistent operations, naming, or behavior
   - Example: REST API calls an operation "create_deployment" but CLI uses "add-service"
   - Result: Confusion, increased learning curve, harder AI agent integration

2. **Leaked Implementation Details**: Interfaces expose internal state, database keys, or technology choices
   - Example: API returns Docker-specific configuration when capability might switch to other runtimes
   - Result: Tight coupling, inability to evolve implementation without breaking clients

3. **Inconsistent Error Handling**: Same error condition produces different responses across interfaces
   - Example: REST returns generic "500 Internal Server Error", CLI prints Python traceback, MCP gives cryptic code
   - Result: Poor developer experience, difficult debugging, AI agents cannot learn error patterns

4. **No Versioning Strategy**: Interface changes break existing clients without warning or migration path
   - Example: Required field added to API without backward compatibility, scripts break
   - Result: Fragile integrations, fear of changes, technical debt accumulation

5. **Poor Observability**: No correlation between requests across interfaces, difficult to trace issues
   - Example: User reports CLI command failure, but logs don't connect it to underlying API call
   - Result: Extended debugging time, inability to diagnose distributed failures

6. **Lack of Contract-First Design**: Interfaces implemented ad-hoc without formal specification
   - Example: REST API evolved through code-first approach, documentation lags reality
   - Result: Unclear contracts, integration guesswork, version mismatches

### Business Impact

**Without standardized interface design patterns**:

- **Development Velocity**: 40-60% time overhead maintaining multiple inconsistent interfaces
- **Integration Cost**: 2-3x longer for clients to integrate (guessing semantics, handling inconsistencies)
- **Support Burden**: 50%+ support tickets related to interface confusion or error interpretation
- **AI Agent Effectiveness**: 70% failure rate when agents encounter inconsistent interfaces or unclear errors
- **Refactoring Risk**: Fear of breaking changes leads to technical debt, interfaces ossify around first implementation
- **Time to Market**: 3-5 weeks additional delay per capability server for interface stabilization

### Real-World Examples

**Negative Example - Inconsistent Interfaces**:
```python
# REST API (orchestrator)
POST /environments/env-123/deployments
{"service": "webapp", "replicas": 3}

# CLI (same operation)
$ chora-orch add-service --env env-123 --name webapp --count 3

# Problems:
# - Different terminology: "deployments" vs "add-service"
# - Different parameter names: "replicas" vs "count"
# - No obvious connection between REST and CLI
```

**Negative Example - Leaked Implementation**:
```python
# API exposes Docker-specific details
POST /deployments
{
  "docker_image": "nginx:latest",
  "docker_network": "bridge",
  "docker_volumes": ["/var/data"]
}

# Problem: If we switch from Docker to Kubernetes, API must change
# Better: Abstract as "container_image", "network_mode", "volumes"
```

**Negative Example - Inconsistent Errors**:
```python
# REST API
{"error": "Internal server error"}  # Unhelpful, generic

# CLI (same error condition)
Traceback (most recent call last):
  File "orchestrator.py", line 42, in create_deployment
    replicas = int(config["replicas"])
ValueError: invalid literal for int() with base 10: 'three'

# Problems:
# - REST hides error, CLI exposes stack trace (security risk)
# - Different error messages for same validation failure
# - No structured error code for programmatic handling
```

---

## Solution Design

### Core Principles

**1. Domain-Driven Design (DDD) for Capabilities**

Each capability server is a **bounded context** with its own **ubiquitous language**:
- Define domain concepts (e.g., Orchestrator: "Environment", "Deployment", "Service Instance")
- Use consistent terminology across ALL interfaces (REST paths, CLI commands, error messages)
- Model aggregates properly (e.g., Deployments belong to Environments, not standalone)
- Respect capability boundaries (Manifest handles service discovery, not Orchestrator)

**2. Contract-First Interface Design**

Define interfaces **before implementation**:
- **REST**: Write OpenAPI 3.x specification first, validate with stakeholders
- **gRPC**: Define `.proto` files with service and message definitions
- **CLI**: Document commands, flags, and help text before coding
- **MCP**: Define action schemas and message formats

Benefits:
- Collaborative design review before code lock-in
- Auto-generate server stubs, client SDKs, and documentation
- Single source of truth for interface contracts

**3. Core-Interface Separation**

Keep core logic **interface-agnostic**:
```
┌─────────────────────────────────────────────┐
│          Client Layer (Thin Adapters)        │
├─────────┬─────────┬─────────┬───────────────┤
│ REST API│   CLI   │  gRPC   │     MCP       │
│ (Flask) │ (Click) │ (proto) │  (FastMCP)    │
└────┬────┴────┬────┴────┬────┴────┬──────────┘
     │         │         │         │
     └─────────┴─────────┴─────────┘
                  │
     ┌────────────▼────────────┐
     │    Core Domain Logic     │
     │  (Interface-agnostic)    │
     │  - Business rules        │
     │  - Validation            │
     │  - Domain exceptions     │
     └──────────────────────────┘
```

- Core raises domain exceptions (e.g., `DeploymentConfigError`)
- Interface adapters translate to protocol-specific responses (HTTP 400, CLI exit code 1, gRPC INVALID_ARGUMENT)

**4. Standardized Error Handling**

Define consistent error format across interfaces:

**Core Exception**:
```python
class DeploymentConfigError(Exception):
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
```

**REST API Response**:
```json
{
  "error": {
    "code": "INVALID_DEPLOYMENT_CONFIG",
    "message": "replicas must be >= 1",
    "field": "replicas"
  }
}
```
HTTP Status: `400 Bad Request`

**CLI Output**:
```
Error: Invalid deployment config: replicas must be >= 1 (field: replicas)
Exit code: 1
```

**gRPC Status**:
```
Code: INVALID_ARGUMENT
Message: "replicas must be >= 1"
Details: field=replicas
```

**5. Versioning Strategy**

**Semantic Versioning for Interfaces**:
- **Major version** (v1 → v2): Breaking changes (removed fields, changed semantics)
- **Minor version** (v1.1 → v1.2): Additive changes (new optional fields, new endpoints)
- **Patch version** (v1.1.0 → v1.1.1): Bug fixes, documentation updates

**Implementation Approaches**:
- **REST**: `/api/v1/`, `/api/v2/` URL paths
- **gRPC**: Package names `chora.orchestrator.v1`, `chora.orchestrator.v2`
- **CLI**: Deprecation warnings before removing commands (`--foo` deprecated, use `--bar`)

**Backward Compatibility Guidelines**:
- Support old API version for ≥6 months after new version launch
- Provide migration guide in documentation
- Use feature flags to enable gradual rollout

**6. Observability Across Interfaces**

**Distributed Tracing**:
- Propagate `X-Request-ID` header through all calls
- Log correlation ID at every layer (REST → Core → gRPC calls to other services)
- Use structured logging (JSON format) for easy parsing

**Audit Logging**:
- Record: Who (user/service), What (operation), When (timestamp), Result (success/failure)
- Example: `{"actor": "user-123", "operation": "deployment.create", "env": "prod", "status": "success", "timestamp": "2025-11-12T10:30:00Z"}`

**Metrics**:
- Track per-interface: request rate, error rate, latency (p50, p95, p99)
- Track per-operation: which endpoints/commands are most used, which error most frequently

---

## Solution Architecture

### Interface Layer Responsibilities

Each interface layer (REST, CLI, gRPC, MCP) is a **thin adapter** responsible for:

1. **Protocol Handling**: Parse incoming requests (JSON, CLI args, proto messages)
2. **Input Validation**: Basic syntax checks (e.g., JSON well-formed, required flags present)
3. **Translation to Core**: Convert protocol-specific input to core domain types
4. **Core Invocation**: Call core domain logic functions/methods
5. **Output Translation**: Convert core results/exceptions to protocol-specific responses
6. **Observability Injection**: Add request IDs, log entry/exit, emit metrics

### Core Layer Responsibilities

The core domain logic is **interface-agnostic** and responsible for:

1. **Business Logic**: Implement capability-specific operations (orchestration, registry, routing)
2. **Domain Validation**: Enforce business rules (e.g., replicas >= 1, environment exists)
3. **State Management**: Interact with databases, external services (via repositories/adapters)
4. **Exception Handling**: Raise domain-specific exceptions (e.g., `ResourceNotFound`, `ConfigurationError`)
5. **Domain Events**: Emit events for composition patterns (e.g., `DeploymentCreated` event)

**Core does NOT**:
- Know about HTTP status codes, CLI exit codes, or gRPC status
- Parse JSON, YAML, or command-line arguments
- Format output for specific interfaces (no "pretty printing" in core)
- Handle protocol-specific concerns (authentication headers, TLS, etc.)

### Interface Contract Artifacts

For each capability server, maintain:

**1. OpenAPI Specification (`openapi.yaml`)**:
```yaml
openapi: 3.0.0
info:
  title: Orchestrator API
  version: 1.0.0
paths:
  /environments/{envId}/deployments:
    post:
      summary: Create deployment
      parameters:
        - name: envId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DeploymentConfig'
      responses:
        '201':
          description: Deployment created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Deployment'
        '400':
          description: Invalid configuration
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
```

**2. CLI Documentation (`cli-spec.md`)**:
```markdown
## Command: `chora-orch deployment create`

**Usage**: `chora-orch deployment create --env <env-id> --config <json>`

**Flags**:
- `--env <env-id>` (required): Environment ID
- `--config <json>` (required): Deployment configuration as JSON

**Example**:
```bash
chora-orch deployment create --env prod --config '{"service":"webapp","replicas":3}'
```

**Exit Codes**:
- `0`: Success
- `1`: General error (invalid config, deployment failed)
- `2`: Usage error (missing required flag)
```

**3. gRPC Proto (if applicable)**:
```protobuf
syntax = "proto3";
package chora.orchestrator.v1;

service OrchestratorService {
  rpc CreateDeployment(CreateDeploymentRequest) returns (Deployment);
}

message CreateDeploymentRequest {
  string env_id = 1;
  DeploymentConfig config = 2;
}
```

**4. MCP Action Schema (if applicable)**:
```json
{
  "action": "deployment.create",
  "description": "Create a new deployment in an environment",
  "parameters": {
    "env_id": {"type": "string", "required": true},
    "config": {"type": "object", "required": true}
  }
}
```

---

## Success Criteria

### Essential Success Criteria

1. **Contract-First Adoption**: 100% of new capability servers define interface contracts (OpenAPI, CLI spec) before implementation
2. **Consistent Naming**: All interfaces for a capability use the same terminology (verified via automated tests)
3. **Error Mapping**: All core exceptions map to consistent errors across interfaces (REST, CLI, gRPC)
4. **Documentation**: Every interface has complete documentation (OpenAPI UI, CLI help text, proto comments)

### Recommended Success Criteria

5. **Backward Compatibility**: 0 breaking changes in minor/patch releases, all major releases provide migration guide
6. **Observability**: All requests tagged with correlation ID, 100% of operations logged with structured format
7. **Versioning**: All APIs versioned explicitly (`/api/v1/`), deprecation warnings for CLI commands
8. **Testing**: Interface consistency tests validate that REST, CLI, and other interfaces produce same results for same operations

### Advanced Success Criteria

9. **Hypermedia (HATEOAS)**: REST APIs include links to related resources (e.g., deployment response includes link to environment)
10. **SDK Generation**: Auto-generate client SDKs (Python, TypeScript) from OpenAPI/proto specs
11. **Shell Autocompletion**: CLI tools provide shell completion for commands and flags
12. **API Gateways**: Use Envoy or similar to provide protocol translation (REST → gRPC, gRPC-Web support)

---

## Key Metrics

### Development Metrics

- **Interface Development Time**: Target 2-3 hours per interface (with contract-first approach)
- **Consistency Defects**: <5% of interfaces have naming or behavior inconsistencies
- **Documentation Coverage**: 100% of endpoints/commands documented before release

### Operational Metrics

- **Error Clarity Score**: >90% of errors include actionable message and error code
- **Integration Time**: 1-2 hours for new client to integrate with capability (down from 8-12 hours)
- **API Breaking Changes**: <1 breaking change per year per capability
- **Tracing Coverage**: 100% of requests have correlation ID in logs

### User Experience Metrics

- **Developer Satisfaction**: >4.0/5.0 rating on interface clarity and consistency
- **Support Ticket Reduction**: 50% reduction in interface-related support requests
- **AI Agent Success Rate**: >85% successful task completion (up from 30% with inconsistent interfaces)

---

## Dependencies

### Prerequisite SAPs

- **SAP-000** (sap-framework): Provides 5-artifact structure for SAP documentation

### Related SAPs (to be created)

- **SAP-043** (multi-interface): Implements core + adapters pattern using these design principles
- **SAP-044** (registry): Defines Manifest API following these interface patterns
- **SAP-045** (bootstrap): Bootstrap scripts interact with interfaces defined using these patterns
- **SAP-046** (composition): Orchestration calls across interfaces rely on consistent contracts

### External Dependencies

- **OpenAPI 3.x**: Specification format for REST APIs
- **gRPC**: Protocol for high-performance interfaces (optional)
- **FastAPI/Flask**: REST API frameworks that support OpenAPI generation
- **Click/Argparse**: CLI frameworks for Python
- **FastMCP**: MCP server framework for AI agent integration

---

## Risks & Mitigations

### Risk 1: Over-Engineering Interfaces

**Description**: Teams spend too much time designing perfect interfaces, delaying delivery

**Mitigation**:
- Use tiered adoption: Essential tier (OpenAPI + CLI) sufficient for initial release
- Recommended/Advanced tiers add sophistication over time
- Provide templates and examples to accelerate contract definition

### Risk 2: Contract Drift

**Description**: Implementation diverges from documented contract over time

**Mitigation**:
- Automated contract testing (e.g., Dredd for OpenAPI, CLI integration tests)
- CI/CD gates: Fail builds if implementation doesn't match contract
- Regular audits via SAP-019 self-evaluation

### Risk 3: Backward Compatibility Burden

**Description**: Supporting multiple API versions increases maintenance cost

**Mitigation**:
- Limit to 2 concurrent major versions (v1 and v2)
- Define clear sunset policy (6-12 months after new major version)
- Use feature flags to share code between versions where possible

### Risk 4: Observability Overhead

**Description**: Adding tracing/logging increases latency or complexity

**Mitigation**:
- Use async logging (don't block requests)
- Sample tracing if volume high (e.g., trace 10% of requests in production)
- Provide minimal observability in Essential tier, full tracing in Recommended

---

## Alternatives Considered

### Alternative 1: Code-First Interface Design

**Approach**: Implement interfaces first, generate documentation later

**Rejected Because**:
- Documentation often lags or becomes inaccurate
- Harder to get design feedback before implementation lock-in
- Doesn't enforce consistency across interfaces

**When to Use**: Rapid prototyping, internal-only tools where contract isn't critical

### Alternative 2: GraphQL for All Interfaces

**Approach**: Use GraphQL as single interface, avoid REST/CLI

**Rejected Because**:
- GraphQL complexity high for simple operations (orchestration is more RPC than query-oriented)
- AI agents may struggle with query construction
- CLI doesn't map naturally to GraphQL queries

**When to Use**: UI-heavy applications needing flexible querying, when clients need to fetch from multiple capabilities in one request

### Alternative 3: No Versioning (Always Backward Compatible)

**Approach**: Never break compatibility, always add new fields/endpoints

**Rejected Because**:
- Eventually leads to bloated interfaces with deprecated fields
- Hard to remove technical debt or bad design decisions
- Limits ability to simplify or refactor

**When to Use**: Internal services with controlled client base, where coordination is easy

---

## References

### Industry Standards

- [OpenAPI Specification 3.x](https://spec.openapis.org/oas/v3.0.0)
- [gRPC Core Concepts](https://grpc.io/docs/what-is-grpc/core-concepts/)
- [RESTful API Design Best Practices](https://restfulapi.net/)
- [Domain-Driven Design (Eric Evans)](https://www.domainlanguage.com/ddd/)

### Related Documentation

- [docs/dev-docs/research/capability-server-architecture-research-report.md](../../dev-docs/research/capability-server-architecture-research-report.md) (Part 4: Interface Design)
- SAP-000 (sap-framework): 5-artifact structure
- SAP-043 (multi-interface): Implementation patterns using these principles

---

## Changelog

### Version 1.0.0 (2025-11-12)

- Initial charter for SAP-042 (Interface Design Patterns)
- Extracted from capability server architecture research (Part 4)
- Defined problem statement, solution design, and success criteria
- Established tiered adoption approach (Essential/Recommended/Advanced)

---

**Next Artifact**: [protocol-spec.md](./protocol-spec.md) - Complete technical specification for interface design patterns
