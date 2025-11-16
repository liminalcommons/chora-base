# Domain Taxonomy

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-11-15
**Part of**: Ecosystem Ontology & Composition Vision (SAP-048)

---

## Purpose

This document defines the **20 domain categories** used in the chora ecosystem's unified ontology framework. Domains organize capabilities under the 3-level hierarchical namespace format: `chora.domain.capability`.

All capabilities (both Service-type and Pattern-type) must belong to exactly one primary domain, with optional cross-domain relationships via Dublin Core's `dc:coverage` field (SKOS broader/narrower/related).

---

## Taxonomy Overview

The taxonomy contains **20 domains** organized into **4 tiers**:

- **Tier 1: Core Infrastructure** (3 domains) - Universal framework capabilities
- **Tier 2: Development & Operations** (7 domains) - Developer-facing tools and workflows
- **Tier 3: Application & UI** (6 domains) - User-facing application capabilities
- **Tier 4: Specialized & Advanced** (4 domains) - Meta-capabilities and optimizations

**Current Coverage**: 45 SAPs across 6 domains
**Future Expansion**: 14 additional domains for growth

---

## Tier 1: Core Infrastructure (3 Domains)

### 1.1 Domain: `infrastructure`

**Purpose**: Universal framework capabilities that underpin the entire ecosystem

**Scope**:
- SAP framework and protocols
- Cross-repo coordination (inbox)
- Meta-packages and bootstrapping

**Namespace Examples**:
- `chora.infrastructure.sap_framework` (SAP-000)
- `chora.infrastructure.inbox` (SAP-001)
- `chora.infrastructure.meta_package` (SAP-002)

**Current SAPs**: 3 (SAP-000, SAP-001, SAP-002)

**Characteristics**:
- Type: Both Service and Pattern
- Distribution: Core to all projects
- Dependencies: Minimal (foundational)

---

### 1.2 Domain: `registry`

**Purpose**: Service discovery, capability lookup, and runtime health monitoring

**Scope**:
- Service mesh and service discovery
- Capability registry (etcd, Git, PyPI)
- Health monitoring and heartbeat tracking
- Dependency resolution

**Namespace Examples**:
- `chora.registry.lookup` (SAP-044, pilot)
- `chora.registry.health_monitor` (future)
- `chora.registry.dependency_resolver` (future)

**Current SAPs**: 1 (SAP-044)

**Characteristics**:
- Type: Primarily Service-type
- Distribution: Runtime services with CLI/REST/MCP
- Dependencies: Requires infrastructure domain

---

### 1.3 Domain: `bootstrap`

**Purpose**: System initialization, dependency-ordered startup, and configuration management

**Scope**:
- Dependency-ordered startup (topological sort)
- Configuration loading and validation
- Service initialization hooks
- Environment setup

**Namespace Examples**:
- `chora.bootstrap.initialize` (SAP-045, pilot)
- `chora.bootstrap.config_loader` (future)
- `chora.bootstrap.env_validator` (future)

**Current SAPs**: 1 (SAP-045)

**Characteristics**:
- Type: Service-type (runtime orchestration)
- Distribution: CLI + library integration
- Dependencies: Requires registry for service discovery

---

## Tier 2: Development & Operations (7 Domains)

### 2.1 Domain: `devex`

**Purpose**: Developer experience tools, testing, CI/CD, quality gates, and automation

**Scope**:
- Project scaffolding and bootstrapping
- Testing frameworks (pytest, coverage)
- CI/CD workflows (GitHub Actions)
- Quality gates (pre-commit, ruff, mypy)
- Documentation frameworks (Diátaxis)
- Automation scripts and justfile commands
- Container operations (Docker)

**Namespace Examples**:
- `chora.devex.project_bootstrap` (SAP-003)
- `chora.devex.testing_framework` (SAP-004)
- `chora.devex.ci_cd` (SAP-005)
- `chora.devex.quality_gates` (SAP-006)
- `chora.devex.documentation` (SAP-007)
- `chora.devex.automation` (SAP-008)
- `chora.devex.docker` (SAP-011)

**Current SAPs**: 7 (SAP-003, 004, 005, 006, 007, 008, 011)

**Characteristics**:
- Type: Both Service and Pattern
- Distribution: CLI tools + documentation
- Dependencies: Infrastructure domain

---

### 2.2 Domain: `interface`

**Purpose**: Interface design patterns and multi-interface capability servers

**Scope**:
- Core/interface separation architecture
- CLI interface patterns (Click, Typer)
- REST API patterns (FastAPI, Flask)
- MCP server patterns (FastMCP)
- Multi-interface composition

**Namespace Examples**:
- `chora.interface.design` (SAP-042, pilot)
- `chora.interface.multi` (SAP-043, pilot)
- `chora.interface.cli_patterns` (future)
- `chora.interface.rest_patterns` (future)
- `chora.interface.mcp_patterns` (future)

**Current SAPs**: 2 (SAP-042, SAP-043)

**Characteristics**:
- Type: Pattern-type (design patterns)
- Distribution: Documentation + templates
- Dependencies: Devex domain for scaffolding

---

### 2.3 Domain: `composition`

**Purpose**: Service orchestration, workflow management, and event-driven patterns

**Scope**:
- Saga orchestration patterns
- Circuit breakers and resilience
- Event bus and pub/sub
- Workflow state machines
- Distributed transactions

**Namespace Examples**:
- `chora.composition.saga` (SAP-046, pilot)
- `chora.composition.circuit_breaker` (future)
- `chora.composition.event_bus` (future)
- `chora.composition.state_machine` (future)

**Current SAPs**: 1 (SAP-046)

**Characteristics**:
- Type: Both Service and Pattern
- Distribution: Runtime services + pattern docs
- Dependencies: Registry, bootstrap

---

### 2.4 Domain: `templates`

**Purpose**: Project templates, code generation, and scaffolding tools

**Scope**:
- Capability server templates (Cookiecutter)
- MCP server templates (deprecated via SAP-014)
- Project generators
- Boilerplate automation

**Namespace Examples**:
- `chora.templates.capability_server` (SAP-047, pilot)
- `chora.templates.react_app` (future)
- `chora.templates.python_lib` (future)

**Current SAPs**: 1 (SAP-047)

**Characteristics**:
- Type: Pattern-type with tooling
- Distribution: Cookiecutter templates + docs
- Dependencies: Devex, interface domains

---

### 2.5 Domain: `database`

**Purpose**: Database integration, ORM patterns, and data persistence

**Scope**:
- ORM patterns (Prisma, Drizzle, SQLAlchemy)
- Database clients (PostgreSQL, MySQL, MongoDB)
- Migration management
- Query optimization

**Namespace Examples**:
- `chora.database.postgresql_client` (future)
- `chora.database.prisma_patterns` (future)
- `chora.database.migration_manager` (future)

**Current SAPs**: 0 (covered in react-database-integration SAP-034)

**Characteristics**:
- Type: Both Service and Pattern
- Distribution: Libraries + pattern docs
- Dependencies: None (foundational)

---

### 2.6 Domain: `security`

**Purpose**: Authentication, authorization, and security patterns

**Scope**:
- Authentication providers (NextAuth, Clerk, Supabase, Auth0)
- Authorization patterns (RBAC, ABAC)
- Security scanning and auditing
- Secrets management

**Namespace Examples**:
- `chora.security.nextauth` (future)
- `chora.security.clerk` (future)
- `chora.security.rbac` (future)
- `chora.security.secrets_manager` (future)

**Current SAPs**: 0 (covered in react-authentication SAP-033)

**Characteristics**:
- Type: Both Service and Pattern
- Distribution: Libraries + pattern docs
- Dependencies: Database domain

---

### 2.7 Domain: `monitoring`

**Purpose**: Observability, logging, metrics, and error tracking

**Scope**:
- Application monitoring (Sentry, Datadog)
- Logging frameworks (Winston, Pino)
- Metrics collection (Prometheus, StatsD)
- Distributed tracing (OpenTelemetry)

**Namespace Examples**:
- `chora.monitoring.sentry` (future)
- `chora.monitoring.prometheus` (future)
- `chora.monitoring.opentelemetry` (future)

**Current SAPs**: 0 (covered in react-error-handling SAP-036)

**Characteristics**:
- Type: Service-type (runtime monitoring)
- Distribution: Runtime services + integration libs
- Dependencies: Registry for service health

---

## Tier 3: Application & UI (6 Domains)

### 3.1 Domain: `react`

**Purpose**: React application patterns, state management, and UI libraries

**Scope**:
- Foundation stack (Next.js, TypeScript, Vitest)
- Testing patterns (Vitest, RTL, MSW)
- Linting and formatting (ESLint 9, Prettier 3)
- State management (TanStack Query, Zustand, RHF)
- Styling (Tailwind CSS, shadcn/ui)
- Performance optimization (Core Web Vitals)
- Accessibility (WCAG 2.2)
- Form validation (React Hook Form, Zod)
- File uploads (UploadThing, Vercel Blob)
- Error boundaries

**Namespace Examples**:
- `chora.react.foundation` (SAP-020)
- `chora.react.testing` (SAP-021)
- `chora.react.linting` (SAP-022)
- `chora.react.state_management` (SAP-023)
- `chora.react.styling` (SAP-024)
- `chora.react.performance` (SAP-025)
- `chora.react.accessibility` (SAP-026)
- `chora.react.authentication` (SAP-033, pilot)
- `chora.react.database_integration` (SAP-034, pilot)
- `chora.react.file_upload` (SAP-035, pilot)
- `chora.react.error_handling` (SAP-036, pilot)
- `chora.react.realtime` (SAP-037, pilot)
- `chora.react.i18n` (SAP-038, pilot)
- `chora.react.e2e_testing` (SAP-039, pilot)
- `chora.react.monorepo` (SAP-040, pilot)
- `chora.react.form_validation` (SAP-041, pilot)

**Current SAPs**: 15 (SAP-020-026, 033-041)

**Characteristics**:
- Type: Pattern-type (knowledge + templates)
- Distribution: Documentation + starter kits
- Dependencies: Devex domain for tooling

---

### 3.2 Domain: `vue`

**Purpose**: Vue.js application patterns and Nuxt.js frameworks

**Scope**:
- Vue 3 composition API patterns
- Nuxt.js application architecture
- Pinia state management
- Vue testing patterns

**Namespace Examples**:
- `chora.vue.foundation` (future)
- `chora.vue.nuxt_patterns` (future)
- `chora.vue.pinia` (future)

**Current SAPs**: 0

**Characteristics**:
- Type: Pattern-type
- Distribution: Documentation + templates
- Dependencies: Devex domain

---

### 3.3 Domain: `angular`

**Purpose**: Angular application patterns and enterprise frameworks

**Scope**:
- Angular 17+ patterns
- RxJS reactive patterns
- NgRx state management
- Angular testing patterns

**Namespace Examples**:
- `chora.angular.foundation` (future)
- `chora.angular.ngrx` (future)
- `chora.angular.rxjs_patterns` (future)

**Current SAPs**: 0

**Characteristics**:
- Type: Pattern-type
- Distribution: Documentation + templates
- Dependencies: Devex domain

---

### 3.4 Domain: `mobile`

**Purpose**: Mobile application patterns (React Native, Flutter)

**Scope**:
- React Native patterns
- Flutter patterns
- Mobile CI/CD
- App store deployment

**Namespace Examples**:
- `chora.mobile.react_native` (future)
- `chora.mobile.flutter` (future)
- `chora.mobile.app_store_deploy` (future)

**Current SAPs**: 0

**Characteristics**:
- Type: Pattern-type
- Distribution: Documentation + templates
- Dependencies: Devex, react domains

---

### 3.5 Domain: `desktop`

**Purpose**: Desktop application patterns (Electron, Tauri)

**Scope**:
- Electron application patterns
- Tauri application patterns
- Desktop packaging and distribution
- Auto-update mechanisms

**Namespace Examples**:
- `chora.desktop.electron` (future)
- `chora.desktop.tauri` (future)
- `chora.desktop.auto_update` (future)

**Current SAPs**: 0

**Characteristics**:
- Type: Pattern-type
- Distribution: Documentation + templates
- Dependencies: Devex, react domains

---

### 3.6 Domain: `api`

**Purpose**: Backend API patterns and microservices

**Scope**:
- REST API design patterns
- GraphQL patterns
- gRPC patterns
- API gateway patterns
- Microservices architecture

**Namespace Examples**:
- `chora.api.rest_design` (future)
- `chora.api.graphql` (future)
- `chora.api.grpc` (future)
- `chora.api.gateway` (future)

**Current SAPs**: 0

**Characteristics**:
- Type: Both Service and Pattern
- Distribution: Libraries + pattern docs
- Dependencies: Interface domain

---

## Tier 4: Specialized & Advanced (4 Domains)

### 4.1 Domain: `awareness`

**Purpose**: Agent awareness, memory systems, and task tracking

**Scope**:
- Agent awareness patterns (AGENTS.md, CLAUDE.md)
- Event-sourced memory (A-MEM)
- Task tracking (beads)
- Cross-session context preservation
- SAP self-evaluation frameworks

**Namespace Examples**:
- `chora.awareness.nested_pattern` (SAP-009)
- `chora.awareness.event_memory` (SAP-010)
- `chora.awareness.task_tracking` (SAP-015)
- `chora.awareness.sap_evaluation` (SAP-019)

**Current SAPs**: 4 (SAP-009, 010, 015, 019)

**Characteristics**:
- Type: Pattern-type (process patterns)
- Distribution: Documentation + tools
- Dependencies: Infrastructure domain

---

### 4.2 Domain: `workflow`

**Purpose**: Development lifecycle, metrics, and process patterns

**Scope**:
- Development lifecycle (DDD→BDD→TDD)
- Metrics tracking and ROI calculation
- Link validation and reference management
- Dogfooding and validation patterns
- Publishing automation (PyPI, npm)
- SAP generation and templating

**Namespace Examples**:
- `chora.workflow.lifecycle` (SAP-012)
- `chora.workflow.metrics` (SAP-013)
- `chora.workflow.link_validation` (SAP-016)
- `chora.workflow.dogfooding` (SAP-027)
- `chora.workflow.publishing` (SAP-028, pilot)
- `chora.workflow.sap_generation` (SAP-029, pilot)

**Current SAPs**: 6 (SAP-012, 013, 016, 027, 028, 029)

**Characteristics**:
- Type: Pattern-type (process patterns)
- Distribution: Documentation + automation
- Dependencies: Awareness, devex domains

---

### 4.3 Domain: `integration`

**Purpose**: Third-party integrations and content generation tools

**Scope**:
- chora-compose integration (pip, MCP, CLI)
- chora-compose meta-capabilities (24 MCP tools)
- LLM integrations (Claude, GPT-4)
- External service integrations

**Namespace Examples**:
- `chora.integration.compose` (SAP-017)
- `chora.integration.compose_meta` (SAP-018)
- `chora.integration.llm_orchestration` (future)

**Current SAPs**: 2 (SAP-017, SAP-018)

**Characteristics**:
- Type: Service-type (runtime integration)
- Distribution: MCP servers + CLI tools
- Dependencies: Interface domain

---

### 4.4 Domain: `optimization`

**Purpose**: Performance optimization, caching, and advanced patterns

**Scope**:
- Performance profiling and optimization
- Caching strategies (Redis, CDN)
- Code splitting and lazy loading
- Real-time synchronization (WebSocket, SSE)
- Internationalization (i18n)
- End-to-end testing (Playwright)
- Monorepo architecture (Turborepo)

**Namespace Examples**:
- `chora.optimization.caching` (future)
- `chora.optimization.code_splitting` (future)
- `chora.optimization.cdn_integration` (future)

**Current SAPs**: 0 (some covered in react domain)

**Characteristics**:
- Type: Pattern-type (optimization patterns)
- Distribution: Documentation + tooling
- Dependencies: React, devex domains

---

## Domain Allocation Guidelines

### Choosing a Domain for New Capabilities

**Step 1: Determine Capability Type**
- **Service-type**: Runtime capability servers (CLI/REST/MCP)
- **Pattern-type**: Knowledge documentation (SAP artifacts)

**Step 2: Identify Primary Domain**

Use this decision tree:

```
Is it foundational infrastructure?
├─ Yes → infrastructure, registry, or bootstrap
└─ No ↓

Is it developer-facing tooling?
├─ Yes → devex, interface, composition, templates, database, security, or monitoring
└─ No ↓

Is it application/UI-focused?
├─ Yes → react, vue, angular, mobile, desktop, or api
└─ No ↓

Is it meta-capability or process pattern?
└─ Yes → awareness, workflow, integration, or optimization
```

**Step 3: Validate Namespace Uniqueness**

```bash
# Check for namespace collisions
grep "dc_identifier: chora.domain.capability" capabilities/*.yaml
```

**Step 4: Document Cross-Domain Relationships**

Use Dublin Core's `dc:coverage` for SKOS taxonomy:

```yaml
metadata:
  dc_coverage:
    broader: chora.devex.testing_framework  # Parent capability
    narrower:
      - chora.react.testing                  # Child capabilities
    related:
      - chora.workflow.lifecycle             # Related capabilities
```

---

## Domain Coverage Statistics

**Current Distribution** (45 SAPs across 6 domains):

| Domain | Service-Type | Pattern-Type | Total | Percentage |
|--------|--------------|--------------|-------|------------|
| infrastructure | 1 | 2 | 3 | 6.7% |
| devex | 7 | 7 | 14 | 31.1% |
| react | 0 | 15 | 15 | 33.3% |
| awareness | 0 | 4 | 4 | 8.9% |
| workflow | 0 | 6 | 6 | 13.3% |
| integration | 2 | 0 | 2 | 4.4% |
| registry | 1 | 0 | 1 | 2.2% |
| bootstrap | 1 | 0 | 1 | 2.2% |
| composition | 1 | 0 | 1 | 2.2% |
| templates | 0 | 1 | 1 | 2.2% |
| **Total** | **6** | **39** | **45** | **100%** |

**Future Growth Targets** (v6.0.0, Q2 2026):

- **20 domains** fully documented with examples
- **100+ capabilities** (30 Service-type, 70 Pattern-type)
- **Balanced distribution** across Tier 2-3 domains

---

## Domain Migration Policy

### Renaming or Merging Domains

If a domain needs to be renamed or merged:

1. Create coordination request (SAP-001 inbox)
2. Update namespace aliases in registry (backward compatibility)
3. Migrate capability manifests to new domain
4. Deprecate old domain with 2-version grace period
5. Archive old domain in v{major}.0.0 release

**Example**: `devex` + `templates` → `developer_experience`

```yaml
# Old namespace (deprecated in v6.0.0)
dc_identifier: chora.templates.capability_server

# New namespace (alias for 2 versions)
dc_identifier: chora.developer_experience.capability_server

# Registry lookup supports both until v8.0.0
```

---

## Cross-Domain Dependencies

### Allowed Dependency Patterns

**1. Service → Service** (within same domain or cross-domain):
- Relationship: `runtime`, `optional`, `conditional`
- Validation: Topological sort, health check

**2. Pattern → Pattern** (within same domain preferred):
- Relationship: `prerequisite`, `complementary`, `mutually_exclusive`, `extends`
- Validation: Topological sort for learning paths

**3. Service → Pattern** (cross-domain allowed):
- Relationship: `prerequisite` (advisory)
- Validation: Warning message only

**4. Pattern → Service** (cross-domain common):
- Relationship: `runtime` (hard requirement)
- Validation: Health check required

### Cross-Domain Example

```yaml
# chora.react.form_validation (Pattern in react domain)
metadata:
  dc_identifier: chora.react.form_validation
  dc_type: "Pattern"
  dc_relation:
    requires:
      - capability: chora.react.foundation  # Same domain
        version: ^1.0.0
        relationship: prerequisite
      - capability: chora.integration.compose  # Cross-domain
        version: ">=3.0.0"
        relationship: runtime
```

---

## Domain Documentation Requirements

Each domain MUST have:

1. **Domain README** (`docs/ontology/domains/{domain}/README.md`)
   - Purpose and scope
   - Namespace examples (at least 3)
   - Current and planned capabilities
   - Integration patterns

2. **Domain Examples** (at least 2 capabilities per domain)
   - 1 Service-type example (if applicable)
   - 1 Pattern-type example

3. **SKOS Taxonomy** (`dc:coverage` relationships)
   - Broader/narrower domain relationships
   - Related domains for cross-cutting concerns

---

## Version History

- **1.0.0** (2025-11-15): Initial domain taxonomy
  - 20 domains across 4 tiers
  - 45 SAPs mapped to 10 domains
  - 10 domains reserved for future growth
  - Domain allocation guidelines
  - Cross-domain dependency patterns

---

## Related Documentation

- [Namespace Format Specification](./namespace-spec.md) (Week 1.2, ONT-002)
- [Capability Type Definitions](./capability-types.md) (Week 1.4, ONT-004)
- [Migration Guide](./migration-guide.md) (Week 1.3, ONT-003)
- [SKOS Coverage Specification](./skos-coverage.md) (future)

---

**Next Steps**:
1. Week 1.2: Document 3-level namespace format (ONT-002)
2. Week 1.3: Create migration mapping (ONT-003)
3. Week 1.4: Define unified capability types (ONT-004)
