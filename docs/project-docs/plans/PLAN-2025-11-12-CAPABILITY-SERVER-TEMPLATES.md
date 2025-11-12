# Capability Server Template Implementation Plan

**Plan ID**: PLAN-2025-11-12-CAPABILITY-SERVER-TEMPLATES
**Created**: 2025-11-12
**Status**: Active
**Owner**: chora-base team
**Target Completion**: 2-3 weeks

---

## Executive Summary

Build production-ready capability server templates (SAP-042-047) to enable 5-minute generation of multi-interface servers with architectural patterns. This replaces the current MCP-only templates (SAP-014) with a comprehensive multi-interface approach supporting CLI, REST, and optionally MCP.

**Current State**: Documentation complete (SAP-042-047), templates missing
**Target State**: Templates built, verified, and promoted to pilot status
**Timeline**: 2-3 weeks (build → verify → pilot)

---

## Problem Statement

### What's Missing

**Documentation exists** for SAP-042-047:
- ✅ Capability charters (problem/solution/ROI)
- ✅ Protocol specs (complete technical details)
- ✅ Adoption blueprints (installation guides)
- ✅ AGENTS.md (agent patterns)

**Templates don't exist**:
- ❌ Multi-interface scaffolding (CLI, REST, MCP)
- ❌ Core/interface separation structure
- ❌ Service registry integration (`manifest.yaml`)
- ❌ Bootstrap initialization logic
- ❌ Composition patterns (saga, circuit breaker, events)
- ❌ Comprehensive test templates

**Script mismatch**:
- `create-capability-server.py` renamed but still uses MCP-only templates
- Points to `static-template/mcp-templates/` (SAP-014)
- Missing `static-template/capability-server-templates/` (SAP-042-047)

### Impact

**User Experience**:
- Documentation promises 5-minute multi-interface setup
- Script delivers 30-minute MCP-only setup
- Credibility gap between promise and reality

**SAP Status**:
- SAP-042-047 marked "pilot" but not implemented
- Cannot verify what doesn't exist
- Blocks promotion to "active" status

---

## Goals & Success Criteria

### Primary Goals

1. **Build Templates** (Week 1-2)
   - Multi-interface scaffolding (CLI, REST, MCP)
   - Architectural patterns (SAP-042-046)
   - Comprehensive documentation
   - Test suite (≥80% coverage)

2. **Update Script** (Week 2)
   - Point to new templates
   - Add CLI arguments (`--enable-mcp`, `--enable-saga`, etc.)
   - Update variable mappings

3. **Verify Implementation** (Week 3)
   - Generate test projects
   - Validate all interfaces work
   - Test architectural patterns
   - Measure setup time

4. **Promote to Pilot** (Week 3)
   - Update status: draft → pilot
   - Begin 5-week dogfooding per SAP-027
   - Collect pilot feedback

### Success Criteria

**Functional**:
- ✅ Generated project has working CLI, REST, and MCP interfaces
- ✅ Core/interface separation enforced
- ✅ Service registry integration works
- ✅ Bootstrap sequence executes correctly
- ✅ Saga/circuit breaker patterns functional
- ✅ Test suite passes with ≥80% coverage

**Performance**:
- ✅ Generation time: ≤5 minutes
- ✅ Docker build time: ≤3 minutes
- ✅ Test execution time: ≤30 seconds

**Quality**:
- ✅ All SAP-042-047 verification tests pass
- ✅ Generated code passes pre-commit hooks
- ✅ Documentation accurate and complete

---

## Architecture Overview

### Template Structure

```
static-template/
├── capability-server-templates/        # NEW (Jinja2 templates)
│   ├── core/                           # SAP-042: Core/interface separation
│   │   ├── __init__.py.template
│   │   ├── models.py.template          # Shared data models
│   │   ├── services.py.template        # Business logic
│   │   └── exceptions.py.template      # Error handling
│   │
│   ├── interfaces/                     # SAP-043: Multi-interface
│   │   ├── __init__.py.template
│   │   ├── cli/                        # Click CLI
│   │   │   ├── __init__.py.template
│   │   │   ├── main.py.template
│   │   │   └── commands.py.template
│   │   ├── rest/                       # FastAPI REST
│   │   │   ├── __init__.py.template
│   │   │   ├── app.py.template
│   │   │   ├── routes.py.template
│   │   │   └── schemas.py.template
│   │   └── mcp/                        # FastMCP (optional)
│   │       ├── __init__.py.template
│   │       └── server.py.template
│   │
│   ├── infrastructure/                 # SAP-044-046
│   │   ├── registry.py.template        # SAP-044: Service registry client
│   │   ├── bootstrap.py.template       # SAP-045: Startup orchestration
│   │   ├── saga.py.template            # SAP-046: Saga pattern
│   │   ├── circuit_breaker.py.template # SAP-046: Circuit breaker
│   │   └── event_bus.py.template       # SAP-046: Event bus
│   │
│   ├── config/
│   │   ├── manifest.yaml.template      # SAP-044: Service manifest
│   │   ├── settings.py.template        # Pydantic settings
│   │   └── logging.yaml.template
│   │
│   ├── tests/
│   │   ├── core/                       # Core logic tests
│   │   ├── interfaces/                 # Interface tests
│   │   └── infrastructure/             # Infrastructure tests
│   │
│   ├── docs/
│   │   ├── AGENTS.md.template          # SAP-009
│   │   ├── API.md.template             # REST API docs
│   │   ├── CLI.md.template             # CLI reference
│   │   └── ARCHITECTURE.md.template    # Design docs
│   │
│   ├── .github/
│   │   └── workflows/
│   │       ├── test.yml.template       # SAP-005
│   │       ├── lint.yml.template
│   │       └── release.yml.template
│   │
│   ├── pyproject.toml.template
│   ├── Dockerfile.template             # SAP-011
│   ├── README.md.template
│   ├── .gitignore.template
│   └── .pre-commit-config.yaml.template
```

### Component Breakdown

#### Core (SAP-042)
- **models.py**: Pydantic data models (interface-agnostic)
- **services.py**: Business logic classes
- **exceptions.py**: Custom error types
- **Purpose**: Shared logic across all interfaces

#### Interfaces (SAP-043)
- **CLI**: Click-based command-line interface
  - Commands grouped by domain
  - JSON/YAML output formats
  - Configuration file support
- **REST**: FastAPI REST API
  - OpenAPI 3.0 spec
  - Pydantic schemas for validation
  - Health/readiness endpoints
- **MCP**: FastMCP server (optional, enabled with `--enable-mcp`)
  - Tool/resource definitions
  - Chora MCP Conventions v1.0
  - Claude Desktop integration

#### Infrastructure (SAP-044-046)
- **Registry** (SAP-044): Manifest-based service discovery
  - `manifest.yaml` with capability metadata
  - Health check integration
  - Dependency declaration
- **Bootstrap** (SAP-045): Dependency-ordered startup
  - Validate config → Resolve deps → Initialize → Register → Ready
  - Graceful shutdown (SIGTERM/SIGINT)
  - 60s timeout with retries
- **Composition** (SAP-046): Resilience patterns
  - Saga: Multi-step workflows with rollback
  - Circuit breaker: 5-fault threshold, 60s recovery
  - Event bus: Async pub/sub for decoupling

---

## Implementation Phases

### Phase 1: Core Templates (Days 1-3)

**Goal**: Build foundation (SAP-042)

**Tasks**:
- [ ] Create `core/` directory structure
- [ ] Build `models.py.template` with Pydantic base models
- [ ] Build `services.py.template` with example service class
- [ ] Build `exceptions.py.template` with error hierarchy
- [ ] Create unit tests for core logic

**Deliverables**:
- Core templates with Jinja2 variables
- Test templates for core logic
- Example business logic patterns

**Success Criteria**:
- Core templates render correctly
- Generated code passes type checking (mypy)
- Tests provide ≥80% coverage of core

---

### Phase 2: Interface Templates (Days 4-7)

**Goal**: Build multi-interface support (SAP-043)

**Tasks**:
- [ ] **CLI Interface** (Day 4)
  - Click command groups
  - JSON/YAML formatters
  - Config file loader
- [ ] **REST Interface** (Day 5-6)
  - FastAPI app structure
  - Route definitions
  - Pydantic request/response schemas
  - Health/readiness endpoints
- [ ] **MCP Interface** (Day 7)
  - FastMCP server template
  - Tool/resource definitions
  - Conditional inclusion (`--enable-mcp`)
- [ ] **Interface Tests**
  - CLI: Test command execution
  - REST: Test endpoints with TestClient
  - MCP: Test tool invocation

**Deliverables**:
- 3 interface templates (CLI, REST, MCP)
- Interface-specific tests
- Integration tests (core → interface)

**Success Criteria**:
- All interfaces can be generated independently or together
- CLI outputs correct JSON/YAML
- REST API serves OpenAPI spec
- MCP server lists tools correctly

---

### Phase 3: Infrastructure Templates (Days 8-10)

**Goal**: Build architectural patterns (SAP-044-046)

**Tasks**:
- [ ] **Registry** (Day 8)
  - `manifest.yaml.template` with schema
  - Registry client for service discovery
  - Health check integration
- [ ] **Bootstrap** (Day 9)
  - Startup phase orchestration
  - Dependency resolution (DAG)
  - Graceful shutdown handlers
- [ ] **Composition** (Day 10)
  - Saga pattern template
  - Circuit breaker template
  - Event bus template
  - Conditional inclusion (`--enable-saga`, etc.)

**Deliverables**:
- Infrastructure templates
- Integration tests
- Example workflows (saga, circuit breaker)

**Success Criteria**:
- Bootstrap executes phases in correct order
- Saga handles rollback correctly
- Circuit breaker trips after 5 faults
- Event bus delivers messages

---

### Phase 4: Documentation & Configuration (Days 11-12)

**Goal**: Complete project scaffolding

**Tasks**:
- [ ] Documentation templates
  - AGENTS.md with all interfaces
  - API.md with OpenAPI reference
  - CLI.md with command reference
  - ARCHITECTURE.md with design overview
- [ ] Configuration templates
  - `pyproject.toml` with all dependencies
  - `Dockerfile` with multi-stage build
  - `.pre-commit-config.yaml`
  - `.github/workflows/` (test, lint, release)
- [ ] README.md with quickstart guide

**Deliverables**:
- Complete documentation suite
- CI/CD pipeline templates
- Docker build configuration

**Success Criteria**:
- Generated README includes all interfaces
- Dockerfile builds successfully (≤3 min)
- CI/CD workflows execute in GitHub Actions

---

### Phase 5: Script Integration (Days 13-14)

**Goal**: Update `create-capability-server.py` to use new templates

**Tasks**:
- [ ] Update `template_dir` path
- [ ] Add CLI arguments:
  - `--enable-mcp` (include MCP interface)
  - `--enable-saga` (include saga pattern)
  - `--enable-circuit-breaker`
  - `--enable-events`
- [ ] Update template mappings (30+ templates)
- [ ] Add variable validation
- [ ] Update generation output messages

**Deliverables**:
- Updated script with new template path
- Enhanced CLI arguments
- Comprehensive validation

**Success Criteria**:
- Script generates projects with all interfaces
- Optional features work correctly
- Generated projects pass all checks

---

### Phase 6: Verification (Days 15-18)

**Goal**: Run full SAP verification process

**Tasks**:
- [ ] **L1 Verification: Basic Generation** (Day 15)
  - Generate 3 test projects (minimal, standard, full)
  - Verify all files created
  - Verify no template errors
- [ ] **L2 Verification: Interface Testing** (Day 16)
  - Test CLI commands
  - Test REST endpoints
  - Test MCP tools (if enabled)
  - Verify core/interface separation
- [ ] **L3 Verification: Architectural Patterns** (Day 17)
  - Test bootstrap sequence
  - Test saga workflow
  - Test circuit breaker
  - Test event bus
- [ ] **L4 Verification: Integration** (Day 18)
  - Run full test suite
  - Build Docker image
  - Execute CI/CD pipeline
  - Measure performance (setup time, build time, test time)

**Deliverables**:
- Verification report (like existing SAP verification reports)
- Performance benchmarks
- Issue list (if any)

**Success Criteria**:
- All L1-L4 checks pass
- Setup time ≤5 minutes
- Docker build ≤3 minutes
- Tests execute ≤30 seconds

---

### Phase 7: Promotion & Dogfooding (Days 19-21 + 5 weeks)

**Goal**: Promote to pilot and begin dogfooding

**Tasks**:
- [ ] Update status: draft → pilot (sap-catalog.json, INDEX.md)
- [ ] Create pilot project for internal use
- [ ] Set up 5-week dogfooding plan per SAP-027
  - Week 1: Setup and onboarding
  - Week 2-4: Active use, collect feedback
  - Week 5: Analysis and GO/NO-GO decision
- [ ] Document pilot feedback
- [ ] Address critical issues
- [ ] Plan promotion to "active"

**Deliverables**:
- Pilot status updates
- Dogfooding project
- Pilot feedback log
- GO/NO-GO recommendation

**Success Criteria**:
- SAP-042-047 marked "pilot"
- Dogfooding project running
- Positive pilot feedback
- Clear path to "active"

---

## Risk Assessment

### High Risk

**Template Complexity**
- **Risk**: 30+ templates to build, high chance of bugs
- **Mitigation**: Build incrementally, test each phase before proceeding
- **Contingency**: Use existing MCP templates as reference, copy proven patterns

**Script Integration**
- **Risk**: Many template mappings, easy to miss files
- **Mitigation**: Create checklist, validate generated output comprehensively
- **Contingency**: Add automated validation in script

### Medium Risk

**Performance Targets**
- **Risk**: 5-minute setup may be hard to achieve with complex templates
- **Mitigation**: Optimize template rendering, minimize I/O operations
- **Contingency**: Accept 7-10 minutes if quality maintained

**Documentation Accuracy**
- **Risk**: SAP-042-047 docs written before implementation, may have inaccuracies
- **Mitigation**: Update docs as implementation reveals issues
- **Contingency**: Mark docs as "under revision" during build

### Low Risk

**Verification Process**
- **Risk**: Verification may find issues requiring rework
- **Mitigation**: Use existing SAP verification methodology (proven)
- **Contingency**: Budget extra week for fixes

---

## Dependencies

### Internal Dependencies

- **SAP-004** (testing-framework): Test templates must follow pytest patterns
- **SAP-005** (ci-cd-workflows): CI/CD templates must match GitHub Actions patterns
- **SAP-006** (quality-gates): Pre-commit hooks, ruff, mypy configurations
- **SAP-009** (agent-awareness): AGENTS.md structure and content
- **SAP-011** (docker-operations): Dockerfile patterns

### External Dependencies

- **Python libraries**: Click, FastAPI, FastMCP, Pydantic (already in use)
- **Jinja2**: Template rendering (already installed)
- **No new dependencies**: Use existing chora-base infrastructure

---

## Resource Requirements

### Time

- **Developer time**: 15-18 days of focused work (2-3 weeks calendar)
- **Review time**: 2-3 days for verification and testing
- **Total**: 3 weeks from start to pilot promotion

### Tools

- **Existing**: Jinja2, pytest, mypy, ruff (already configured)
- **New**: None required

### Knowledge

- **Required expertise**:
  - Jinja2 templating
  - Multi-interface architecture patterns
  - Click, FastAPI, FastMCP APIs
  - pytest testing patterns
  - Docker multi-stage builds

---

## Timeline & Milestones

### Week 1: Core & Interfaces

- **Day 1-3**: Core templates (SAP-042)
- **Day 4-7**: Interface templates (SAP-043)
- **Milestone 1**: Core and interfaces rendering correctly

### Week 2: Infrastructure & Integration

- **Day 8-10**: Infrastructure templates (SAP-044-046)
- **Day 11-12**: Documentation & configuration
- **Day 13-14**: Script integration
- **Milestone 2**: Complete template suite, script updated

### Week 3: Verification & Promotion

- **Day 15-18**: Full SAP verification (L1-L4)
- **Day 19-21**: Status promotion, dogfooding setup
- **Milestone 3**: SAP-042-047 promoted to pilot

### Weeks 4-8: Dogfooding

- **5 weeks**: Active dogfooding per SAP-027
- **Milestone 4**: GO/NO-GO decision for "active" promotion

---

## Success Metrics

### Quantitative

- **Setup time**: ≤5 minutes (target from SAP-047 docs)
- **Docker build time**: ≤3 minutes
- **Test execution time**: ≤30 seconds
- **Test coverage**: ≥80%
- **Templates count**: 30-40 templates (all patterns covered)

### Qualitative

- **Documentation accuracy**: Generated projects match SAP-042-047 docs
- **User experience**: Developers can generate and understand projects easily
- **Code quality**: Generated code passes all quality gates
- **Maintainability**: Templates are easy to update and extend

---

## Next Steps

### Immediate Actions (Today)

1. ✅ Mark SAP-042-047 as "draft" in sap-catalog.json
2. ✅ Update INDEX.md status references
3. ✅ Create this implementation plan
4. **Begin Phase 1**: Create core templates directory structure

### This Week

1. Build core templates (SAP-042)
2. Build CLI interface (SAP-043, part 1)
3. Build REST interface (SAP-043, part 2)
4. Begin MCP interface (SAP-043, part 3)

### Next Week

1. Complete infrastructure templates (SAP-044-046)
2. Build documentation templates
3. Update create-capability-server.py
4. Begin verification process

---

## Review & Approval

**Plan Status**: ✅ Approved for execution (2025-11-12)

**Reviewers**:
- **chora-base team**: Approved Option 1 approach
- **Claude Code**: Created implementation plan

**Approvals**:
- [x] Technical approach reviewed
- [x] Timeline feasible
- [x] Resources available
- [x] Risk assessment complete

**Next Review**: End of Week 1 (Milestone 1 checkpoint)

---

## References

- [SAP-042: Interface Design](../../skilled-awareness/interface-design/)
- [SAP-043: Multi-Interface Patterns](../../skilled-awareness/multi-interface/)
- [SAP-044: Registry & Service Discovery](../../skilled-awareness/registry/)
- [SAP-045: Bootstrap & Startup Sequence](../../skilled-awareness/bootstrap/)
- [SAP-046: Composition Patterns](../../skilled-awareness/composition/)
- [SAP-047: Capability Server Template](../../skilled-awareness/capability-server-template/)
- [SAP-027: Dogfooding Patterns](../../skilled-awareness/dogfooding-patterns/)
- [SAP Verification Methodology](../verification/COMPREHENSIVE_SAP_VERIFICATION_PLAN.md)

---

**Last Updated**: 2025-11-12
**Plan Owner**: chora-base team
**Status**: Active - Phase 1 Ready to Start
