# SAP-043: Multi-Interface Capability Servers - Capability Charter

**SAP ID**: SAP-043
**Domain**: Developer Experience
**Status**: Pilot
**Version**: 1.0.0
**Last Updated**: 2025-11-12
**Adoption Tier**: Essential → Recommended → Advanced

---

## Executive Summary

**SAP-043** provides patterns for building capability servers that expose the same core functionality through **four standardized interfaces**: **Native API** (Python), **CLI** (Command Line), **REST** (HTTP), and **MCP** (Model Context Protocol). This multi-interface approach ensures users can access capabilities in the context that best suits their workflow—whether scripting, API integration, interactive CLI, or AI assistant interaction—while maintaining **consistency** and **avoiding code duplication**.

**Key Innovation**: A **core + adapters** architecture where business logic is implemented once in an interface-agnostic core module, then exposed through thin interface adapters that handle protocol-specific concerns (argument parsing, error translation, output formatting).

**Success Criteria**: All operations available via all four interfaces, passing consistency tests that verify identical behavior, with 80%+ time savings vs duplicating logic per interface.

---

## Problem Statement

### The Challenge: Interface Proliferation Without Consistency

Modern capability servers must support diverse access patterns:

- **Developers** need Python APIs for programmatic access
- **Operators** need CLIs for scripting and automation
- **External systems** need REST APIs for integration
- **AI assistants** need MCP interfaces for tool/resource access

**Without structured guidance**, teams face **three critical anti-patterns**:

#### Anti-Pattern 1: Duplicated Business Logic

**Problem**: Implementing the same operation independently in each interface.

**Example**:
```python
# cli.py - validation in CLI
if replicas < 1:
    sys.stderr.write("Error: replicas must be >= 1\n")
    sys.exit(1)

# api.py - different validation in REST
if data["replicas"] < 1:
    return {"error": "Invalid replicas"}, 400

# mcp.py - yet another validation in MCP
if replicas < 1:
    raise McpError("replicas out of range")
```

**Result**: 3× the code, inconsistent validation logic, 3× the bugs to fix.

#### Anti-Pattern 2: Interface-Specific Features (Drift)

**Problem**: Adding features to one interface that aren't available in others.

**Example**: CLI has `--dry-run` flag, but REST API doesn't support preview mode. Users switching interfaces lose functionality.

**Result**: Fragmented user experience, unclear "source of truth" for what the capability actually does.

#### Anti-Pattern 3: Thick Interface Layers

**Problem**: Business logic leaks into interface code (HTTP handlers, CLI commands, MCP tools).

**Example**:
```python
@app.route("/deployments", methods=["POST"])
def create_deployment():
    data = request.get_json()
    # ❌ Validation in interface layer
    if data["replicas"] < 1:
        return {"error": "Invalid replicas"}, 400
    # ❌ Business logic in interface layer
    deployment = Deployment(...)
    db.session.add(deployment)
    db.session.commit()
    return jsonify(deployment.to_dict()), 201
```

**Result**: Cannot test business logic without HTTP framework, cannot reuse logic in CLI, impossible to add new interfaces without rewriting everything.

### Impact Without SAP-043

**Quantified Costs**:

| Problem | Time Cost | Quality Impact |
|---------|-----------|----------------|
| Duplicated logic across 4 interfaces | 4× implementation time | 4× bug surface area |
| Inconsistent behavior debugging | +40% debugging time | User confusion, trust erosion |
| Interface-specific features | +25% feature scope creep | Fragmented UX |
| No consistency testing | +30% integration issues | Production failures |
| Adding 5th interface | Rewrite everything | Technical debt accumulation |

**Real-World Example**: A team building an orchestration server implemented CLI first, then REST API. When adding MCP interface, they discovered CLI had 12 operations, REST had 9 (missing 3), and error messages were completely different. They spent 2 weeks reconciling interfaces and lost user trust.

**Total Impact**: **3-4 weeks** to implement 4 interfaces vs **1 week** with core + adapters pattern = **75% time waste** + quality issues.

---

## Solution Design

### Core Principle: Interface-Agnostic Core + Thin Adapters

SAP-043 implements a **Ports and Adapters** (Hexagonal Architecture) pattern optimized for capability servers:

```
┌─────────────────────────────────────────────────────┐
│  Native API    CLI    REST API    MCP Interface     │ ← Thin adapters
│  (Python)    (Click)  (FastAPI)   (FastMCP)         │   (parse, format, translate)
└───────────────────────┬─────────────────────────────┘
                        │
                  ┌─────▼─────┐
                  │   Core    │ ← Business logic
                  │  Module   │   (interface-agnostic)
                  └───────────┘
                        │
                  ┌─────▼─────┐
                  │   Data    │ ← Persistence
                  │   Layer   │   (DB, files, etc.)
                  └───────────┘
```

**Key Rule**: **Core module NEVER imports interface frameworks** (no Flask, Click, FastMCP in core).

### Architecture Components

#### 1. Core Module (Business Logic)

**Location**: `core/` directory or `{package}/core.py`

**Responsibility**: Implement all capability operations once, using interface-agnostic inputs/outputs.

**Pattern**:
```python
# core/orchestrator.py
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class Deployment:
    """Domain model (not tied to any interface)."""
    env_id: str
    service: str
    replicas: int
    deployment_id: str = ""

class ValidationError(Exception):
    """Domain exception (not tied to HTTP, CLI, etc.)."""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(message)

class OrchestratorService:
    """Core capability implementation."""

    def create_deployment(self, env_id: str, config: Dict[str, Any]) -> Deployment:
        """Create deployment (interface-agnostic).

        Args:
            env_id: Environment identifier
            config: Deployment configuration dict

        Returns:
            Deployment object

        Raises:
            ValidationError: If config is invalid
            RuntimeError: If deployment fails
        """
        # ✅ Validation in core (single source of truth)
        if config["replicas"] < 1:
            raise ValidationError(
                "replicas must be >= 1",
                field="replicas"
            )

        # ✅ Business logic in core
        deployment = Deployment(
            env_id=env_id,
            service=config["service"],
            replicas=config["replicas"],
            deployment_id=f"deploy-{generate_id()}"
        )

        # ✅ Persistence in core
        deployment_repo.create(deployment)

        return deployment
```

**Benefits**:
- Test without any interface framework
- Reuse across all interfaces
- Easy to add new interfaces (just new adapter)

#### 2. Interface Adapters (Protocol Translation)

**Responsibility**: Translate interface-specific inputs to core calls, format outputs for interface.

##### Native API Adapter (Python)

**Location**: `{package}/__init__.py` or `api/native.py`

**Pattern**: Direct export of core functions/classes.

```python
# myserver/__init__.py
from .core.orchestrator import OrchestratorService, Deployment, ValidationError

# Export for programmatic use
__all__ = ["OrchestratorService", "Deployment", "ValidationError"]

# Usage:
# from myserver import OrchestratorService
# svc = OrchestratorService()
# deployment = svc.create_deployment("prod", {"service": "web", "replicas": 3})
```

##### CLI Adapter (Click)

**Location**: `cli/commands.py` or `{package}/cli.py`

**Pattern**: Parse arguments, call core, format output for terminal.

```python
# cli/commands.py
import click
import sys
from core.orchestrator import OrchestratorService, ValidationError

service = OrchestratorService()

@click.group()
def cli():
    """Orchestrator CLI."""
    pass

@cli.command()
@click.option("--env", required=True, help="Environment ID")
@click.option("--service", required=True, help="Service name")
@click.option("--replicas", type=int, required=True, help="Replica count")
def create_deployment(env, service, replicas):
    """Create deployment."""
    try:
        # ✅ Thin adapter: parse CLI args → core call
        deployment = service.create_deployment(
            env_id=env,
            config={"service": service, "replicas": replicas}
        )

        # ✅ Format output for CLI
        click.echo(f"✓ Deployment {deployment.deployment_id} created")
        click.echo(f"  Environment: {deployment.env_id}")
        click.echo(f"  Service: {deployment.service}")
        click.echo(f"  Replicas: {deployment.replicas}")

    except ValidationError as e:
        # ✅ Translate core exception → CLI error
        click.echo(f"Error: {e.message}", err=True)
        if e.field:
            click.echo(f"  Field: {e.field}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
```

##### REST API Adapter (FastAPI)

**Location**: `api/http.py` or `{package}/api.py`

**Pattern**: Parse JSON, call core, return JSON + HTTP status.

```python
# api/http.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.orchestrator import OrchestratorService, ValidationError

app = FastAPI(title="Orchestrator API")
service = OrchestratorService()

class CreateDeploymentRequest(BaseModel):
    service: str
    replicas: int

class DeploymentResponse(BaseModel):
    deployment_id: str
    env_id: str
    service: str
    replicas: int

@app.post("/api/v1/environments/{env_id}/deployments",
          response_model=DeploymentResponse,
          status_code=201)
def create_deployment_endpoint(env_id: str, request: CreateDeploymentRequest):
    """Create deployment (REST API)."""
    try:
        # ✅ Thin adapter: parse JSON → core call
        deployment = service.create_deployment(
            env_id=env_id,
            config={"service": request.service, "replicas": request.replicas}
        )

        # ✅ Format output as JSON
        return DeploymentResponse(
            deployment_id=deployment.deployment_id,
            env_id=deployment.env_id,
            service=deployment.service,
            replicas=deployment.replicas
        )

    except ValidationError as e:
        # ✅ Translate core exception → HTTP 400
        raise HTTPException(
            status_code=400,
            detail={
                "error": "VALIDATION_ERROR",
                "message": e.message,
                "field": e.field
            }
        )
    except Exception as e:
        # ✅ Translate core exception → HTTP 500
        raise HTTPException(
            status_code=500,
            detail={"error": "INTERNAL_ERROR", "message": str(e)}
        )
```

##### MCP Adapter (FastMCP)

**Location**: `mcp/server.py` or `{package}/mcp.py`

**Pattern**: Define MCP tools/resources, call core, return MCP responses.

```python
# mcp/server.py
from fastmcp import FastMCP
from core.orchestrator import OrchestratorService, ValidationError

mcp = FastMCP("Orchestrator")
service = OrchestratorService()

@mcp.tool()
def create_deployment(env_id: str, service_name: str, replicas: int) -> dict:
    """Create deployment (MCP tool for AI assistants).

    Args:
        env_id: Environment identifier
        service_name: Service to deploy
        replicas: Number of replicas (must be >= 1)

    Returns:
        Deployment details

    Raises:
        ValueError: If validation fails
    """
    try:
        # ✅ Thin adapter: parse MCP args → core call
        deployment = service.create_deployment(
            env_id=env_id,
            config={"service": service_name, "replicas": replicas}
        )

        # ✅ Format output for MCP (JSON-serializable)
        return {
            "status": "created",
            "deployment": {
                "id": deployment.deployment_id,
                "environment": deployment.env_id,
                "service": deployment.service,
                "replicas": deployment.replicas
            }
        }

    except ValidationError as e:
        # ✅ Translate core exception → MCP error (ValueError)
        raise ValueError(f"{e.message} (field: {e.field})")

@mcp.resource(uri="orchestrator://deployments/{deployment_id}")
def get_deployment(deployment_id: str) -> str:
    """Get deployment details (MCP resource for AI assistants)."""
    deployment = deployment_repo.get(deployment_id)
    return f"""# Deployment {deployment_id}

**Environment**: {deployment.env_id}
**Service**: {deployment.service}
**Replicas**: {deployment.replicas}
**Status**: {deployment.status}
"""

if __name__ == "__main__":
    mcp.run()
```

**Key Pattern**: All 4 adapters call `service.create_deployment()` with the SAME inputs, get the SAME result, translate to interface-specific formats.

### Consistency Guarantees

#### 1. Shared Error Handling

**Core Exception** → **Interface-Specific Translation**:

| Core Exception | Native API | CLI | REST API | MCP |
|----------------|------------|-----|----------|-----|
| `ValidationError("replicas must be >= 1", field="replicas")` | Raise exception | Exit 1 + stderr message | HTTP 400 + JSON error | ValueError + message |
| `RuntimeError("deploy failed")` | Raise exception | Exit 1 + stderr message | HTTP 500 + JSON error | RuntimeError + message |

**Implementation**: Error mapping table in documentation, adapters follow consistently.

#### 2. Consistency Testing

**Pattern**: Run same operation through different interfaces, verify identical result.

```python
# tests/test_consistency.py
import pytest
from core.orchestrator import OrchestratorService
from cli.commands import create_deployment as cli_create
from api.http import create_deployment_endpoint
from mcp.server import create_deployment as mcp_create

def test_create_deployment_consistency():
    """Verify all interfaces produce same result."""
    config = {"service": "web", "replicas": 3}

    # Call core directly
    core_result = OrchestratorService().create_deployment("prod", config)

    # Call via CLI adapter (mocked Click context)
    with click_context():
        cli_result = cli_create(env="prod", service="web", replicas=3)

    # Call via REST adapter (mocked FastAPI request)
    rest_result = create_deployment_endpoint("prod", CreateDeploymentRequest(**config))

    # Call via MCP adapter
    mcp_result = mcp_create(env_id="prod", service_name="web", replicas=3)

    # Assert all produce same deployment
    assert cli_result.deployment_id == rest_result.deployment_id
    assert rest_result.deployment_id == mcp_result["deployment"]["id"]
    assert core_result.replicas == 3
    assert cli_result.replicas == rest_result.replicas == mcp_result["deployment"]["replicas"]
```

**Requirement**: Consistency tests must pass for all operations across all interfaces.

### Integration with SAP-042 (InterfaceDesign)

SAP-043 **implements** the patterns defined in SAP-042:

- **SAP-042** defines **what** (contract-first, core-interface separation, error mapping, versioning)
- **SAP-043** defines **how** (concrete implementation with 4 adapters, code examples, testing patterns)

**Dependency**: SAP-043 adopters should read SAP-042 for foundational principles.

### MCP as 4th Interface (SAP-014 Integration)

**Innovation**: SAP-043 treats MCP as a **first-class interface** alongside Native/CLI/REST.

**From SAP-014**:
- FastMCP patterns for tool/resource definitions
- Chora MCP Conventions v1.0 (namespace:tool_name, namespace://type/id)
- MCP-specific testing patterns

**Integration Point**:
```python
# MCP adapter uses same core as other interfaces
@mcp.tool()
def operation_name(...) -> dict:
    return core_service.operation(...)
```

**Benefit**: AI assistants (Claude, GPT-4) access the SAME capability logic as CLI/REST users.

---

## Success Criteria

### Essential Tier (Weeks 1-2)

**Definition**: Minimum viable multi-interface implementation.

**Criteria**:
- [ ] **Core module exists** (interface-agnostic business logic)
- [ ] **All 4 interfaces implemented** (Native, CLI, REST, MCP)
- [ ] **Same operations available** in all interfaces (feature parity)
- [ ] **Consistent error handling** (core exceptions → interface errors)
- [ ] **Consistency tests pass** (verify identical behavior)
- [ ] **Documentation complete** (README with all 4 usage examples)

**Quantified**:
- 100% feature parity (if core has N operations, all interfaces expose N)
- 100% consistency test pass rate
- <5% code duplication (business logic in core only)

**Adoption Time**: 2 weeks for first capability server

### Recommended Tier (Weeks 3-4)

**Definition**: Production-ready with observability and versioning.

**Criteria**:
- [ ] **Correlation IDs propagate** (X-Request-ID through all layers)
- [ ] **Structured logging** (JSON logs with request_id, operation, interface)
- [ ] **Versioned APIs** (REST `/api/v1/`, MCP tool versioning)
- [ ] **Backward compatibility tests** (old clients still work)
- [ ] **Performance baseline** (measure overhead of each interface)
- [ ] **Interface-specific optimizations** (where needed, documented)

**Quantified**:
- 100% request traceability (all logs have correlation ID)
- Zero breaking changes without version bump
- <10ms adapter overhead (thin adapters add minimal latency)

**Adoption Time**: +1 week after Essential Tier

### Advanced Tier (Weeks 5-8)

**Definition**: Ecosystem integration and advanced features.

**Criteria**:
- [ ] **SDKs auto-generated** (OpenAPI → Python/TS clients)
- [ ] **Shell autocompletion** (CLI tab-completion for all commands)
- [ ] **Gateway integration** (all interfaces behind unified gateway)
- [ ] **Multi-protocol load testing** (verify interface parity under load)
- [ ] **Dynamic interface selection** (clients choose best interface automatically)
- [ ] **Interface usage metrics** (track which interfaces are most popular)

**Quantified**:
- 3+ auto-generated SDKs (Python, TypeScript, Go)
- 100% CLI command autocompletion
- Gateway latency <50ms p99

**Adoption Time**: +2-4 weeks after Recommended Tier

---

## Key Metrics

### Baseline (Without SAP-043)

**4-interface implementation without patterns**:
- Implementation time: 4 weeks (1 week per interface)
- Code duplication: 300% (business logic in 4 places)
- Bug surface area: 4× (bug in core requires 4 fixes)
- Consistency issues: 25% of features drift between interfaces
- Time to add 5th interface: 1 week (rewrite everything)

### Target (With SAP-043)

**4-interface implementation with core + adapters**:
- Implementation time: 1 week (core + 4 adapters)
- Code duplication: <5% (core logic once, thin adapters)
- Bug surface area: 1× (fix in core, all interfaces benefit)
- Consistency issues: 0% (enforced by tests)
- Time to add 5th interface: 2 days (new adapter only)

### ROI Calculation

**Time Savings**:
- Initial implementation: 4 weeks → 1 week = **75% savings**
- Maintenance: 4× effort → 1× effort = **75% savings**
- Adding new interface: 1 week → 2 days = **60% savings**

**Quality Improvements**:
- Consistency issues: 25% → 0% = **100% improvement**
- Test coverage: 40% → 85% = **112% improvement**
- Bug fix time: 4× → 1× = **75% improvement**

**Total Value**: **$48,000/year savings** for team of 4 (based on 75% time savings on interface work, assuming 20% of development time on interfaces).

---

## Dependencies

### Required SAPs

**SAP-042 (InterfaceDesign)** [Essential]:
- Foundational principles for contract-first, core-interface separation
- Error mapping patterns
- Versioning strategies

### Recommended SAPs

**SAP-014 (mcp-server-development)** [Recommended]:
- MCP interface patterns (FastMCP, Chora MCP Conventions v1.0)
- MCP tool/resource implementation
- MCP testing patterns

**SAP-004 (testing-framework)** [Recommended]:
- pytest patterns for consistency tests
- Mocking strategies for interface layers
- Test coverage requirements (85%)

**SAP-012 (development-lifecycle)** [Optional]:
- DDD principles for core module design
- BDD scenarios for interface parity validation
- TDD workflow for adapter implementation

### Related SAPs

**SAP-044 (Registry)** [Integration]:
- Service registration via multiple interfaces
- Discovery patterns for multi-interface capability servers

**SAP-047 (CapabilityServer-Template)** [Downstream]:
- Scaffolding tool generates multi-interface structure
- Templates for all 4 adapters

---

## Risks and Mitigations

### Risk 1: Adapter Overhead

**Risk**: Interface adapters add latency vs direct calls.

**Mitigation**:
- Measure adapter overhead (<10ms target)
- Optimize hot paths if needed
- Document performance characteristics

**Likelihood**: Low (adapters are thin, minimal overhead)

### Risk 2: Interface-Specific Edge Cases

**Risk**: Some operations might not map cleanly to all interfaces (e.g., streaming).

**Mitigation**:
- Document interface-specific features (e.g., CLI: progress bars, REST: SSE streaming)
- Core provides hooks (e.g., yield progress events), adapters consume appropriately
- Consistency tests focus on functional equivalence, not implementation

**Likelihood**: Medium (some operations have interface-specific concerns)

### Risk 3: Versioning Complexity

**Risk**: Maintaining backward compatibility across 4 interfaces is hard.

**Mitigation**:
- Version core module (semantic versioning)
- Each interface adapter pins to core version
- Deprecation warnings in all interfaces
- Migration guides for breaking changes

**Likelihood**: Medium (versioning is inherently complex)

### Risk 4: Team Familiarity with All 4 Frameworks

**Risk**: Team may be experts in Python but not Click, FastAPI, FastMCP.

**Mitigation**:
- SAP-043 provides copy-paste adapter templates
- Each adapter is <100 lines (thin by design)
- Focus on core logic (team's domain expertise), adapters follow patterns

**Likelihood**: Low (adapters are simple, templates provided)

---

## Alternatives Considered

### Alternative 1: Single Interface + Auto-Generation

**Approach**: Implement one interface (e.g., REST), auto-generate CLI/MCP from OpenAPI.

**Pros**: Less code to write initially.

**Cons**:
- Generated code may not be idiomatic (ugly CLI flags, poor MCP tool descriptions)
- Hard to customize interface-specific features
- Still duplicates business logic in REST handlers

**Why Not**: Core + adapters provides better control and idiomatic interfaces.

### Alternative 2: Shared Interface Library

**Approach**: Create common interface layer that all protocols call.

**Pros**: Single API for all interfaces.

**Cons**:
- Abstraction overhead (another layer)
- Least common denominator (interface limits what core can do)
- Doesn't solve core logic duplication

**Why Not**: Thin adapters are simpler and more flexible.

### Alternative 3: Interface-First (No Core Module)

**Approach**: Implement each interface independently, share helper functions.

**Pros**: Familiar to most teams (how they currently work).

**Cons**:
- Massive code duplication
- Consistency issues
- Hard to add new interfaces
- SAP-043 anti-patterns

**Why Not**: This is the problem SAP-043 solves.

---

## Adoption Path

### Phase 1: Pilot (First Capability Server)

**Goal**: Validate SAP-043 patterns with one server.

**Steps**:
1. Choose pilot server (e.g., Manifest Registry)
2. Implement core module (1-2 days)
3. Add all 4 adapters (2-3 days)
4. Write consistency tests (1 day)
5. Document lessons learned

**Outcome**: Proven multi-interface implementation, templates for other servers.

### Phase 2: Rollout (Remaining Capability Servers)

**Goal**: Apply SAP-043 to all capability servers (Orchestrator, Gateway, Bootstrap, etc.).

**Steps**:
1. Use pilot as template (copy adapter structure)
2. Implement core module per server
3. Add adapters (faster with templates)
4. Run consistency tests

**Outcome**: Entire ecosystem follows multi-interface pattern.

### Phase 3: Template Integration (SAP-047)

**Goal**: Scaffold new capability servers with multi-interface structure.

**Steps**:
1. Add core + adapter templates to SAP-047
2. Update capability server generator
3. New servers start with all 4 interfaces

**Outcome**: Zero-effort multi-interface for new capability servers.

---

## Version History

**1.0.0** (2025-11-12):
- Initial SAP-043 capability charter
- Core + adapters pattern for 4 interfaces (Native, CLI, REST, MCP)
- Integration with SAP-042 (InterfaceDesign) and SAP-014 (mcp-server-development)
- Essential/Recommended/Advanced adoption tiers
- Success criteria and ROI metrics
- Consistency testing patterns

---

## References

1. **Research Report Part 1**: Multi-Interface Architecture patterns from AWS, Docker, Kubernetes, Terraform
2. **SAP-042**: InterfaceDesign - Foundational principles for interface contracts and core-interface separation
3. **SAP-014**: mcp-server-development - FastMCP patterns and Chora MCP Conventions v1.0
4. **Hexagonal Architecture**: Alistair Cockburn's Ports and Adapters pattern
5. **AWS CLI Design**: Boto3 SDK as thin wrapper over service APIs
6. **Docker Architecture**: CLI as client to Docker Engine REST API

---

**Next Steps**:
1. Read [protocol-spec.md](./protocol-spec.md) for complete implementation details
2. Read [adoption-blueprint.md](./adoption-blueprint.md) for step-by-step guide
3. Review [AGENTS.md](./AGENTS.md) for quick reference and workflows

---

**Feedback**: Submit adoption feedback to [ledger.md](./ledger.md)
