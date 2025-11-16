# Skilled Awareness Package (SAP) Index

**Purpose**: Central registry of all capabilities packaged as SAPs in chora-base.

**Last Updated**: 2025-11-16
**Framework Version**: 1.0.0
**Organization**: Domain-Based Taxonomy (6 domains)

---

## Overview

This index tracks all **48 capabilities** organized across **6 domains** for improved discoverability and progressive adoption.

**Total Coverage**: 48/48 SAPs (100%)

**Domain Distribution**:
- Infrastructure: 3 SAPs (6%) - Core framework and coordination
- Developer Experience: 15 SAPs (31%) - Development workflow tools + capability server architecture
- Foundation: 6 SAPs (13%) - Technology stack foundations (React + auth + database + forms)
- User-Facing: 6 SAPs (13%) - User interaction patterns (state, styling, uploads, errors)
- Advanced: 8 SAPs (17%) - Optimizations and integrations (real-time, i18n, e2e, monorepo)
- Specialized: 12 SAPs (25%) - Meta-capabilities, process patterns, and awareness systems

**Status Distribution**:
- Active: 24 SAPs (50%)
- Pilot: 18 SAPs (38%) - SAP-015, SAP-028, SAP-029, SAP-033-047 (including capability server suite)
- Draft: 5 SAPs (10%) - SAP-048, SAP-049, SAP-050 (new), 2 historical
- Deprecated: 1 SAP (2%) - SAP-014 (replaced by SAP-047)

---

## Infrastructure Domain

**Purpose**: Universal framework and coordination capabilities for any project

**SAPs**: 3 (10% of catalog)

### SAP-000: SAP Framework

- **Status**: active | **Version**: 1.0.0 | **Domain**: Infrastructure
- **Description**: Core SAP framework and protocols defining how Skilled Awareness Packages work
- **Dependencies**: None (foundational)
- **Location**: [sap-framework/](sap-framework/)
- **Key Features**: SAP protocol specification, governance standards, document templates, installation patterns, awareness integration

### SAP-001: Inbox Coordination Protocol

- **Status**: active | **Version**: 1.1.0 | **Domain**: Infrastructure
- **Description**: Production-ready cross-repo coordination protocol with 5 CLI tools, AI-powered generation, and formalized SLAs reducing coordination effort by 90%
- **Dependencies**: None
- **Location**: [inbox/](inbox/)
- **Key Features**: Cross-repo coordination with event logging, one-command installation (5min setup), AI-powered coordination generator (50% faster), query and filter tools (<100ms), status dashboard with visual reporting

### SAP-002: Chora-Base Meta Package

- **Status**: active | **Version**: 1.0.0 | **Domain**: Infrastructure
- **Description**: Meta-capability describing chora-base itself using SAP framework (dogfooding demonstration)
- **Dependencies**: SAP-000
- **Location**: [chora-base/](chora-base/)
- **Key Features**: Project charter, architecture overview, 4-domain documentation, SAP Framework integration, universal foundation patterns

---

## Developer Experience Domain

**Purpose**: Accelerate development with testing, CI/CD, quality gates, tooling, and capability server architecture patterns

**SAPs**: 15 (31% of catalog)

### SAP-003: Project Bootstrap & Scaffolding

- **Status**: active | **Version**: 1.0.0 | **Domain**: Developer Experience
- **Description**: Copier-based project generation from static-template with variable substitution
- **Dependencies**: SAP-000
- **Location**: [project-bootstrap/](project-bootstrap/)
- **Key Features**: Project scaffolding, template generation, variable substitution, directory structure setup

### SAP-004: Testing Framework

- **Status**: active | **Version**: 1.0.0 | **Domain**: Developer Experience
- **Description**: pytest-based testing framework with 85%+ coverage patterns and async support
- **Dependencies**: SAP-000, SAP-003
- **Location**: [testing-framework/](testing-framework/)
- **Key Features**: pytest configuration, coverage enforcement (85%+), test fixtures, async testing patterns, 6 test pattern templates

### SAP-005: CI/CD Workflows

- **Status**: active | **Version**: 1.0.0 | **Domain**: Developer Experience
- **Description**: GitHub Actions workflows for testing, linting, security, and release automation
- **Dependencies**: SAP-000, SAP-004
- **Location**: [ci-cd-workflows/](ci-cd-workflows/)
- **Key Features**: Matrix testing (Python 3.11-3.13), automated linting, security scanning (CodeQL), dependency review, release automation

### SAP-006: Quality Gates

- **Status**: active | **Version**: 1.0.0 | **Domain**: Developer Experience
- **Description**: Pre-commit hooks, ruff linting, mypy type checking, and coverage enforcement
- **Dependencies**: SAP-000, SAP-004
- **Location**: [quality-gates/](quality-gates/)
- **Key Features**: Pre-commit hooks (7 hooks), Ruff linting (200x faster), Mypy type checking, coverage enforcement, security scanning

### SAP-007: Documentation Framework

- **Status**: active | **Version**: 1.0.0 | **Domain**: Developer Experience
- **Description**: Diátaxis-based 4-domain documentation architecture with frontmatter schema and test extraction
- **Dependencies**: SAP-000
- **Location**: [documentation-framework/](documentation-framework/)
- **Key Features**: Diátaxis 4-domain structure, frontmatter schema validation, executable how-to guides, test extraction from docs, DOCUMENTATION_STANDARD.md (700 lines)

### SAP-008: Automation Scripts

- **Status**: active | **Version**: 1.0.0 | **Domain**: Developer Experience
- **Description**: 25 automation scripts (shell + Python) with justfile unified interface and safety contracts
- **Dependencies**: SAP-000, SAP-012
- **Location**: [automation-scripts/](automation-scripts/)
- **Key Features**: 25 automation scripts, justfile with 30+ commands, idempotent operations, safety contracts, 8 script categories

### SAP-011: Docker Operations

- **Status**: active | **Version**: 1.0.0 | **Domain**: Developer Experience
- **Description**: Multi-stage Dockerfiles, docker-compose patterns, and container optimization (150-250MB images)
- **Dependencies**: SAP-000
- **Location**: [docker-operations/](docker-operations/)
- **Key Features**: Multi-stage builds, CI-optimized test containers, GitHub Actions cache integration, non-root execution, 81% build context reduction

---

### Capability Server Architecture (6 SAPs)

**Purpose**: Comprehensive architectural patterns for building capability servers with multi-interface support, service discovery, startup orchestration, and resilience patterns.

**SAPs**: 6 (SAP-042 through SAP-047) | **Status**: All pilot (verified and ready for dogfooding)

**Overview**: This suite of SAPs provides battle-tested patterns for building production-ready capability servers. Together they reduce capability server development time from 40-60 hours to 4-8 hours (85-92% savings).

---

#### SAP-042: Interface Design & Core/Interface Separation

- **Status**: pilot | **Version**: 1.0.0 | **Domain**: Developer Experience
- **Description**: Core/interface separation pattern reducing coupling by 80% and enabling true multi-interface capability servers
- **Dependencies**: SAP-000
- **Location**: [interface-design/](interface-design/)
- **Key Features**: Business logic isolation (core/), interface layer (CLI/REST/MCP), adapter pattern, interface-agnostic testing, onboarding time reduction (2-3 days → 4-8 hours)

#### SAP-043: Multi-Interface Patterns

- **Status**: pilot | **Version**: 1.0.0 | **Domain**: Developer Experience
- **Description**: CLI, REST API, and MCP server interfaces sharing single core implementation, reducing development time by 75%
- **Dependencies**: SAP-000, SAP-042
- **Location**: [multi-interface/](multi-interface/)
- **Key Features**: Click CLI, FastAPI REST, FastMCP server, unified core execution, interface-specific adaptations, 3-interface development in 6-8 hours (vs 24-32 hours)

#### SAP-044: Registry & Service Discovery

- **Status**: pilot | **Version**: 1.0.0 | **Domain**: Developer Experience
- **Description**: Service mesh with manifest-based registration, health checks, dependency resolution, and service discovery
- **Dependencies**: SAP-000, SAP-042
- **Location**: [registry/](registry/)
- **Key Features**: Manifest registry server (OpenAPI 3.0), manifest.yaml schema, health/readiness endpoints, dependency resolution DAG, heartbeat monitoring (10s interval), service discovery queries

#### SAP-045: Bootstrap & Startup Sequence

- **Status**: pilot | **Version**: 1.0.0 | **Domain**: Developer Experience
- **Description**: Dependency-ordered startup orchestration reducing initialization failures by 90% with health checks and graceful shutdown
- **Dependencies**: SAP-000, SAP-042, SAP-044
- **Location**: [bootstrap/](bootstrap/)
- **Key Features**: Startup phases (validate, deps, init, register, ready), dependency DAG resolution, health check integration, graceful shutdown (SIGTERM/SIGINT), 60s timeout with retries

#### SAP-046: Composition Patterns

- **Status**: pilot | **Version**: 1.0.0 | **Domain**: Developer Experience
- **Description**: Saga orchestration, circuit breakers, and event bus patterns for resilient multi-step workflows with 1,141% projected ROI
- **Dependencies**: SAP-000, SAP-042
- **Location**: [composition/](composition/)
- **Key Features**: Saga pattern (multi-step workflows with rollback), circuit breaker (5-fault threshold, 60s recovery), event bus (async pub/sub), saga compensation logic, failure recovery patterns

#### SAP-047: CapabilityServer Template

- **Status**: pilot | **Version**: 1.0.0 | **Domain**: Developer Experience
- **Description**: Jinja2-based template generation producing production-ready capability servers in 5 minutes with all architectural patterns integrated (2,271% projected ROI)
- **Dependencies**: SAP-000, SAP-042, SAP-043, SAP-044, SAP-045, SAP-046
- **Location**: [capability-server-template/](capability-server-template/)
- **Key Features**: Jinja2 template generation, multi-interface scaffolding (CLI/REST/MCP), manifest integration, bootstrap startup, composition patterns (saga/circuit breaker/events), test suite (≥80% coverage), CI/CD pipelines, Docker builds (<250MB), comprehensive docs (AGENTS/API/CLI)
- **⚠️ Note**: Replaces SAP-014 for new projects. Use `python scripts/create-capability-server.py` for generation.

#### SAP-048: Capability Registry & Service Discovery

- **Status**: draft | **Version**: 1.0.0 | **Domain**: Awareness
- **Description**: Formalizes agent awareness patterns for discovering and querying capabilities from the Chora distributed registry built on etcd. Provides standardized patterns for capability discovery, dependency resolution, service health monitoring, and artifact search.
- **Dependencies**: SAP-000, SAP-009, SAP-047
- **Location**: [capability-registry-discovery/](capability-registry-discovery/)
- **Key Features**: Capability discovery (list all capabilities by type/domain/status), service health monitoring (check TTL lease status), dependency resolution (traverse dependency graph), artifact search (full-text search through SAP documentation), event monitoring (watch etcd for real-time registry changes), registry query patterns (Python/Go/Bash examples)

#### SAP-049: Namespace Resolution & Ontology Navigation

- **Status**: draft | **Version**: 1.0.0 | **Domain**: Awareness
- **Description**: Formalizes agent awareness patterns for resolving legacy SAP-XXX identifiers to modern chora.domain.capability namespaces. Provides standardized patterns for backward compatibility, alias resolution, deprecation warnings, and ontology exploration during the 6-month transition period (sunset: 2026-06-01).
- **Dependencies**: SAP-000, SAP-009
- **Location**: [namespace-resolution/](namespace-resolution/)
- **Key Features**: Alias resolution (SAP-XXX → modern namespace), deprecation warning generation (days until sunset), ontology navigation (find capabilities by domain), migration guidance and progress tracking, reverse lookup (namespace → SAP-XXX), input normalization (SAP-015, sap-015, 015, SAP015), fallback to local file (no API dependency)

#### SAP-050: SAP Adoption Verification & Quality Assurance

- **Status**: draft | **Version**: 1.0.0 | **Domain**: Developer Experience
- **Description**: Formalizes agent awareness patterns for validating SAP structure, completeness, and quality. Provides automated verification patterns, quality gates for status promotion (draft → pilot → production), and adoption metrics tracking.
- **Dependencies**: SAP-000, SAP-009
- **Location**: [sap-adoption-verification/](sap-adoption-verification/)
- **Key Features**: Structure verification (validate 5 required artifacts), completeness verification (check required sections), link validation (detect broken cross-references), quality gate evaluation (objective criteria for status promotion), adoption metrics tracking (usage, feedback, issues), Python CLI tool (sap-verify), CI/CD integration patterns, pre-commit hook patterns

---

## Foundation Domain

**Purpose**: Technology stack foundations for React projects with Next.js 15 + TypeScript + Vitest + authentication + database + forms

**SAPs**: 6 (13% of catalog) - 3 active, 3 pilot

### SAP-020: React Project Foundation

- **Status**: active | **Version**: 1.0.0 | **Domain**: Foundation
- **Description**: Next.js 15 + TypeScript foundation stack with App Router, RSC, and modern React patterns reducing setup from 8-12h to 45min
- **Dependencies**: SAP-000, SAP-003
- **Location**: [react-foundation/](react-foundation/)
- **Key Features**: Next.js 15 with App Router, TypeScript strict mode, project structure (feature-based + layer-based), basic state management setup, 8-12 starter templates

### SAP-021: React Testing & Quality

- **Status**: active | **Version**: 1.0.0 | **Domain**: Foundation
- **Description**: Vitest v4 + React Testing Library + MSW for comprehensive React testing with 80-90% coverage targets
- **Dependencies**: SAP-000, SAP-004, SAP-020
- **Location**: [react-testing/](react-testing/)
- **Key Features**: Vitest v4 configuration, React Testing Library patterns, MSW v2 API mocking, component + hook test templates, integration testing patterns

### SAP-022: React Linting & Formatting

- **Status**: active | **Version**: 1.0.0 | **Domain**: Foundation
- **Description**: ESLint 9 flat config + Prettier 3 + pre-commit hooks for React 19 with 182x faster linting and 20-minute setup
- **Dependencies**: SAP-000, SAP-006, SAP-020
- **Location**: [react-linting/](react-linting/)
- **Key Features**: ESLint 9 flat config (182x faster incremental builds), Prettier 3.6.2, pre-commit hooks (Husky + lint-staged), VS Code integration (8 extensions + auto-fix on save), TypeScript strict mode enforcement, accessibility linting (WCAG 2.2 Level AA)

---

### SAP-033: React Authentication & Authorization

**Path**: [docs/skilled-awareness/react-authentication](docs/skilled-awareness/react-authentication)

Production-ready authentication with 4 providers (NextAuth v5, Clerk, Supabase Auth, Auth0) reducing setup from 3-4h to 15min (93.75% time savings)

**Status**: 🟡 Pilot
**Version**: 1.0.0

---

### SAP-034: React Database Integration

**Path**: [docs/skilled-awareness/react-database-integration](docs/skilled-awareness/react-database-integration)

PostgreSQL integration with Prisma/Drizzle ORM decision framework reducing setup from 3-4h to 25min (89.6% time savings)

**Status**: 🟡 Pilot
**Version**: 1.0.0

---

### SAP-041: React Form Validation

**Path**: [docs/skilled-awareness/react-form-validation](docs/skilled-awareness/react-form-validation)

React Hook Form + Zod reducing setup from 2-3h to 20min (88.9% time savings), type-safe validation, WCAG 2.2 Level AA accessibility

**Status**: 🟡 Pilot
**Version**: 1.0.0

---


## User-Facing Domain

**Purpose**: User interaction patterns including state management, styling, file uploads, and error handling for user interfaces

**SAPs**: 6 (13% of catalog) - 2 active, 4 pilot

### SAP-023: React State Management Patterns

- **Status**: active | **Version**: 1.0.0 | **Domain**: User-Facing
- **Description**: Three-pillar state architecture (server/client/form) with TanStack Query v5 + Zustand v4 + React Hook Form v7 + Zod, reducing setup from 4-6h to 30min (85-90% savings)
- **Dependencies**: SAP-000, SAP-020
- **Location**: [react-state-management/](react-state-management/)
- **Key Features**: TanStack Query v5.62.7 for server state (GET/POST/optimistic updates), Zustand v4.5.2 for client state (zero-boilerplate stores), React Hook Form v7.54.0 + Zod v3.24.1 (type-safe validation), 10 production templates, SSR hydration patterns (Next.js 15), optimistic update patterns

### SAP-024: React Styling Architecture

- **Status**: active | **Version**: 1.0.0 | **Domain**: User-Facing
- **Description**: Tailwind CSS v4 + shadcn/ui component library with RSC compatibility and responsive design patterns
- **Dependencies**: SAP-000, SAP-020
- **Location**: [react-styling/](react-styling/)
- **Key Features**: Tailwind CSS v4 (CSS-first), shadcn/ui installation + components, component variant patterns (CVA), responsive design templates, CSS Modules escape hatch

---

### SAP-035: React File Upload & Storage

**Path**: [docs/skilled-awareness/react-file-upload](docs/skilled-awareness/react-file-upload)

File upload with 4 providers (UploadThing, Vercel Blob, Supabase Storage, AWS S3) reducing setup from 6h to 30min (91.7% time savings)

**Status**: 🟡 Pilot
**Version**: 1.0.0

---

### SAP-036: React Error Handling

**Path**: [docs/skilled-awareness/react-error-handling](docs/skilled-awareness/react-error-handling)

Error boundaries + Sentry monitoring reducing setup from 3-4h to 30min (87.5% time savings), GDPR/CCPA compliant PII scrubbing

**Status**: 🟡 Pilot
**Version**: 1.0.0

---


## Advanced Domain

**Purpose**: Advanced integrations, performance optimization, accessibility compliance, real-time sync, internationalization, E2E testing, and monorepo architecture

**SAPs**: 8 (18% of catalog) - 4 active, 4 pilot

### SAP-017: Chora-Compose Integration

- **Status**: active | **Version**: 1.0.0 | **Domain**: Advanced
- **Description**: How to adopt chora-compose for content generation (pip, MCP, CLI) with role-based usage patterns
- **Dependencies**: SAP-003
- **Location**: [chora-compose-integration/](chora-compose-integration/)
- **Key Features**: Installation methods (pip, MCP, CLI), Docker integration, MCP server configuration, role-based patterns, content generation workflows

### SAP-018: chora-compose Meta

- **Status**: active | **Version**: 2.0.0 | **Domain**: Advanced
- **Description**: Complete technical specification: 24 MCP tools, Collections architecture (3-tier model), 5 generators, context resolution (6 sources), event emission for advanced adoption
- **Dependencies**: SAP-000, SAP-017
- **Location**: [chora-compose-meta/](chora-compose-meta/)
- **Key Features**: 24 MCP tools (7 categories), 3-tier Collections architecture, context propagation (MERGE/OVERRIDE/ISOLATE), SHA-256 caching (94%+ hit rate), 6 context source types, event emission (OpenTelemetry), JSON schemas v3.1/v1.0, stigmergic context links

### SAP-025: React Performance Optimization

- **Status**: active | **Version**: 1.0.0 | **Domain**: Advanced
- **Description**: Core Web Vitals optimization with RSC, code splitting, image/font optimization, and bundle size limits
- **Dependencies**: SAP-000, SAP-020
- **Location**: [react-performance/](react-performance/)
- **Key Features**: Core Web Vitals targets (LCP, INP, CLS), code splitting patterns, image optimization (AVIF), font optimization (WOFF2), Lighthouse CI integration

### SAP-026: React Accessibility (WCAG 2.2)

- **Status**: active | **Version**: 1.0.0 | **Domain**: Advanced
- **Description**: WCAG 2.2 Level AA compliance with eslint-plugin-jsx-a11y, Radix UI primitives, and axe-core testing
- **Dependencies**: SAP-000, SAP-020, SAP-021
- **Location**: [react-accessibility/](react-accessibility/)
- **Key Features**: WCAG 2.2 Level AA compliance, eslint-plugin-jsx-a11y (85% coverage), Radix UI accessible components, jest-axe/axe-core testing, focus management patterns

---

### SAP-037: React Real-Time Synchronization

**Path**: [docs/skilled-awareness/react-realtime-synchronization](docs/skilled-awareness/react-realtime-synchronization)

WebSocket/real-time with 4 providers (Socket.IO, Pusher, Ably, Supabase Realtime) reducing setup from 7h to 30min (92.9% time savings)

**Status**: 🟡 Pilot
**Version**: 1.0.0

---

### SAP-038: React Internationalization (i18n)

**Path**: [docs/skilled-awareness/react-internationalization](docs/skilled-awareness/react-internationalization)

next-intl framework reducing setup from 5h to 30min (90% time savings), 20+ languages, Server Components support, type-safe translations

**Status**: 🟡 Pilot
**Version**: 1.0.0

---

### SAP-039: React E2E Testing

**Path**: [docs/skilled-awareness/react-e2e-testing](docs/skilled-awareness/react-e2e-testing)

Playwright E2E testing reducing setup from 3.5h to 30min (85.7% time savings), cross-browser support, parallel execution, CI/CD integration

**Status**: 🟡 Pilot
**Version**: 1.0.0

---

### SAP-040: React Monorepo Architecture

**Path**: [docs/skilled-awareness/react-monorepo-architecture](docs/skilled-awareness/react-monorepo-architecture)

Turborepo monorepo reducing setup from 7.5h to 30min (93.3% time savings), incremental builds, remote caching, pnpm workspaces

**Status**: 🟡 Pilot
**Version**: 1.0.0

---


## Specialized Domain

**Purpose**: Meta-capabilities, process patterns, memory systems, task tracking, awareness systems, and SAP ecosystem tools

**SAPs**: 12 (26% of catalog)

### SAP-009: Agent Awareness System

- **Status**: active | **Version**: 1.1.0 | **Domain**: Specialized
- **Description**: AGENTS.md/CLAUDE.md patterns with bidirectional translation layer, 5 domain AGENTS.md files, and inbox protocol integration
- **Dependencies**: SAP-000, SAP-007
- **Location**: [agent-awareness/](agent-awareness/)
- **Key Features**: Dual-file pattern (AGENTS + CLAUDE), nested awareness hierarchy (5 domain AGENTS.md files), nearest file wins, progressive context loading (200k token budget management), bidirectional translation (conversational ↔ formal), intent routing (confidence thresholds), glossary search (fuzzy matching)

### SAP-010: Memory System (A-MEM)

- **Status**: active | **Version**: 1.0.0 | **Domain**: Specialized
- **Description**: Agent Memory Architecture with event log, knowledge graph, profiles, and trace correlation
- **Dependencies**: SAP-000
- **Location**: [memory-system/](memory-system/)
- **Key Features**: 4 memory types (event, knowledge, profile, trace), Zettelkasten knowledge graph, cross-session learning, event schema v1.0, 30% reduction in repeated mistakes

### SAP-012: Development Lifecycle

- **Status**: active | **Version**: 1.2.0 | **Domain**: Specialized
- **Description**: 8-phase lifecycle (Vision → Monitoring) with Documentation-Driven Development, L3 Documentation-First workflow, Diataxis framework, and BDD → TDD integration
- **Dependencies**: SAP-000, SAP-007
- **Location**: [development-lifecycle/](development-lifecycle/)
- **Key Features**: 8-phase development lifecycle, Documentation-Driven Development (L2/L3 patterns), Documentation-First workflow (L3+): Executable how-tos → BDD extraction, Diataxis framework integration (4 doc types), BDD → TDD integration, 40-80% defect reduction, sprint/release templates, ANTI_PATTERNS.md (1,309 lines)

### SAP-013: Metrics Tracking

- **Status**: active | **Version**: 1.0.0 | **Domain**: Specialized
- **Description**: ClaudeROICalculator, process metrics, sprint velocity tracking with $109k/year savings estimates
- **Dependencies**: SAP-000
- **Location**: [metrics-tracking/](metrics-tracking/)
- **Key Features**: Claude ROI calculation, quality/velocity/adherence tracking, research-backed targets, sprint dashboards, $109k/year savings estimate
- **⚠️ Note**: Incomplete structure (no README.md) - marked for cleanup in Feature 7

### SAP-015: Task Tracking with Beads

- **Status**: pilot | **Version**: 1.1.0 | **Domain**: Specialized
- **Description**: Git-backed persistent task memory for multi-agent coordination with hash-based collision-free IDs, dependency tracking, and A-MEM integration
- **Dependencies**: SAP-000, SAP-010
- **Location**: [task-tracking/](task-tracking/)
- **Key Features**: Git-backed task persistence (.beads/issues.jsonl), hash-based collision-free task IDs (e.g., chora-base-o4b), multi-agent coordination (git sync), dependency tracking (blocks/depends relationships), A-MEM integration (bidirectional traceability), CLI interface (bd create/list/update/close/dep), setup time ≤30 min (avg 9.9 min across 5 projects)

### SAP-016: Link Validation & Reference Management

- **Status**: active | **Version**: 1.0.0 | **Domain**: Specialized
- **Description**: Automated markdown link validation (internal + external) preventing broken documentation references
- **Dependencies**: None (foundational)
- **Location**: [link-validation-reference-management/](link-validation-reference-management/)
- **Key Features**: Internal link validation (100%), external link health checks, CI/CD integration, 4-domain architecture validation, SAP audit workflow support

### SAP-019: SAP Self-Evaluation Framework

- **Status**: active | **Version**: 1.0.0 | **Domain**: Specialized
- **Description**: Progressive evaluation framework for assessing SAP adoption depth, identifying gaps, and generating actionable roadmaps
- **Dependencies**: SAP-000
- **Location**: [sap-self-evaluation/](sap-self-evaluation/)
- **Key Features**: Quick check validation (30s), deep dive gap analysis (5min), strategic roadmap generation (30min), timeline tracking and trend analysis, multi-format reporting (terminal, JSON, markdown, YAML)

### SAP-027: Dogfooding Patterns

- **Status**: active | **Version**: 1.0.0 | **Domain**: Specialized
- **Description**: Formalized 5-week dogfooding pilot methodology for validating patterns through internal use before ecosystem adoption
- **Dependencies**: SAP-000, SAP-029
- **Location**: [dogfooding-patterns/](dogfooding-patterns/)
- **Key Features**: 3-phase pilot design (build, validate, decide), GO/NO-GO criteria framework (time savings, satisfaction, bugs, adoption), ROI analysis with break-even calculation, metrics collection templates (time tracking, validation reports), pilot documentation structure (weekly metrics, final summary)

### SAP-028: Publishing Automation

- **Status**: pilot | **Version**: 1.0.0 | **Domain**: Specialized
- **Description**: Secure PyPI publishing with OIDC trusted publishing as default, eliminating long-lived API tokens for chora-base generated projects
- **Dependencies**: SAP-003, SAP-005
- **Location**: [publishing-automation/](publishing-automation/)
- **Key Features**: OIDC trusted publishing (recommended default), token-based publishing (backward compatibility), manual publishing (local development), PEP 740 attestations for build provenance, GitHub Actions workflow integration, migration protocols (token → trusted publishing)

### SAP-029: SAP Generation Automation

- **Status**: pilot | **Version**: 1.0.0 | **Domain**: Specialized
- **Description**: Template-based SAP artifact generation to reduce creation time from 10 hours to 2 hours (80% savings)
- **Dependencies**: SAP-000
- **Location**: [sap-generation/](sap-generation/)
- **Key Features**: Jinja2 template system (5 templates for 5 artifacts), MVP generation schema (9 fields), generator script (scripts/generate-sap.py), INDEX.md auto-update, validation integration

---

## Domain Statistics

### By Domain

| Domain | SAPs | Percentage | Status Breakdown |
|--------|------|------------|------------------|
| Infrastructure | 3 | 7% | 3 active |
| Developer Experience | 14 | 31% | 7 active, 6 pilot, 1 deprecated |
| Foundation | 6 | 13% | 3 active, 3 pilot |
| User-Facing | 6 | 13% | 2 active, 4 pilot |
| Advanced | 8 | 18% | 4 active, 4 pilot |
| Specialized | 10 | 22% | 7 active, 3 pilot |
| **Total** | **45** | **100%** | **24 active, 12 pilot, 8 draft, 1 deprecated** |

### By Status

| Status | Count | Percentage | Domains |
|--------|-------|------------|---------|
| Active | 24 | 53% | All domains |
| Pilot | 12 | 27% | Specialized (SAP-015, 028, 029), Foundation (SAP-033, 034, 041), User-Facing (SAP-035, 036), Advanced (SAP-037-040) |
| Draft | 8 | 18% | Developer Experience (SAP-042-047: template implementation in progress), 2 historical |
| Deprecated | 1 | 2% | Developer Experience (SAP-014) |

---

## Progressive Adoption Path

Choose your starting point based on project type and goals:

### Path 1: Capability Server Development (NEW)

**Goal**: Build production-ready capability servers with multi-interface support (CLI, REST, MCP)

1. **Infrastructure** (SAP-000) - Framework foundation
2. **Capability Server Architecture** (SAP-042-047) - Use SAP-047 template to generate in 5 minutes
3. **Developer Experience** (SAP-004, 005, 006) - Testing, CI/CD, quality gates (included in template)
4. **Specialized** (SAP-009, 010, 015) - Agent awareness, memory, task tracking (optional)

**Estimated Setup**: 4-8 hours (with template) vs 40-60 hours (manual)

**Quick Start**: `python scripts/create-capability-server.py --name "YourCapability" --enable-mcp --enable-saga --output ~/projects/your-capability`

---

### Path 2: React Application Development

**Goal**: Build modern React apps with Next.js 15

1. **Infrastructure** (SAP-000, 001, 002) - Universal foundation
2. **Developer Experience** (SAP-003, 004, 005, 006, 007) - Testing, CI/CD, docs
3. **Foundation** (SAP-020, 021, 022, 033, 034, 041) - React foundation stack + auth + database + forms
4. **User-Facing** (SAP-023, 024, 035, 036) - State management, styling, uploads, errors
5. **Advanced** (SAP-025, 026, 037-040) - Performance, accessibility, real-time, i18n, e2e, monorepo

**Estimated Setup**: 3-5 days

---

### Path 3: Legacy MCP Server Development

**Goal**: Build Model Context Protocol servers with FastMCP (legacy approach)

**⚠️ Note**: For new projects, use **Path 1 (Capability Server Development)** with SAP-047 template instead. This path is for maintaining existing SAP-014-based projects.

1. **Infrastructure** (SAP-000, 001, 002) - Universal foundation
2. **Developer Experience** (SAP-003, 004, 005, 006, 011, SAP-014) - MCP tooling (deprecated)
3. **Specialized** (SAP-009, 010, 015) - Agent awareness, memory, task tracking

**Estimated Setup**: 2-3 days

---

### Path 4: Cross-Repository Coordination

**Goal**: Coordinate work across multiple repositories

1. **Infrastructure** (SAP-000, 001, 002) - Framework + Inbox protocol
2. **Specialized** (SAP-009, 010, 015) - Agent awareness, memory, task tracking
3. **Developer Experience** (SAP-007, 008) - Documentation, automation

**Estimated Setup**: 1-2 days

---

### Path 5: Process Maturity & Best Practices

**Goal**: Improve development processes and team productivity

1. **Infrastructure** (SAP-000, 002) - Framework foundation
2. **Developer Experience** (SAP-004, 005, 006, 007, 008) - Testing, CI/CD, quality, docs
3. **Specialized** (SAP-009, 010, 012, 013, 019, 027) - Full process stack

**Estimated Setup**: 4-6 days

---

## SAP Dependency Graph

```
Infrastructure Domain (Foundational Layer)
├─ SAP-000 (sap-framework) ────────────────┐
│  └─ Required by: All other SAPs          │
├─ SAP-001 (inbox)                         │
└─ SAP-002 (chora-base)                    │
                                           │
Developer Experience Domain                │
├─ SAP-003 (project-bootstrap) ◄───────────┤
│  └─ Required by: SAP-004, SAP-014        │
├─ SAP-004 (testing-framework) ◄───────────┤
│  └─ Required by: SAP-005, SAP-006        │
├─ SAP-005 (ci-cd-workflows) ◄─────────────┤
├─ SAP-006 (quality-gates) ◄───────────────┤
├─ SAP-007 (documentation-framework) ◄─────┤
├─ SAP-008 (automation-scripts) ◄──────────┤
├─ SAP-011 (docker-operations) ◄───────────┤
├─ SAP-014 (mcp-server-development) ◄──────┤ [DEPRECATED → Use SAP-047]
│                                           │
├─ Capability Server Architecture ◄────────┤
│  ├─ SAP-042 (interface-design) ◄─────────┤
│  │  └─ Required by: SAP-043-047         │
│  ├─ SAP-043 (multi-interface) ◄──────────┤ (depends: SAP-042)
│  ├─ SAP-044 (registry) ◄─────────────────┤ (depends: SAP-042)
│  ├─ SAP-045 (bootstrap) ◄────────────────┤ (depends: SAP-042, SAP-044)
│  ├─ SAP-046 (composition) ◄──────────────┤ (depends: SAP-042)
│  └─ SAP-047 (template) ◄─────────────────┘ (depends: SAP-042-046)
                                           │
Foundation Domain (React Stack)            │
├─ SAP-020 (react-foundation) ◄────────────┤
│  └─ Required by: SAP-021, 022, 023, 024  │
├─ SAP-021 (react-testing) ◄───────────────┤
└─ SAP-022 (react-linting) ◄───────────────┤
                                           │
User-Facing Domain                         │
├─ SAP-023 (react-state-management) ◄──────┤
└─ SAP-024 (react-styling) ◄───────────────┤
                                           │
Advanced Domain                            │
├─ SAP-017 (chora-compose-integration) ◄───┤
├─ SAP-018 (chora-compose-meta) ◄──────────┤
├─ SAP-025 (react-performance) ◄───────────┤
└─ SAP-026 (react-accessibility) ◄─────────┤
                                           │
Specialized Domain                         │
├─ SAP-009 (agent-awareness) ◄─────────────┤
├─ SAP-010 (memory-system) ◄───────────────┤
├─ SAP-012 (development-lifecycle) ◄───────┤
├─ SAP-013 (metrics-tracking) ◄────────────┤
├─ SAP-015 (task-tracking) ◄───────────────┤
├─ SAP-016 (link-validation) ◄─────────────┘
├─ SAP-019 (sap-self-evaluation)
├─ SAP-027 (dogfooding-patterns)
├─ SAP-028 (publishing-automation)
└─ SAP-029 (sap-generation)
```

**Key Dependencies**:
- **SAP-000** is foundational; all SAPs depend on it
- **SAP-003 → SAP-004**: Testing depends on project structure
- **SAP-004 → SAP-005, SAP-006**: CI/CD and quality depend on testing
- **SAP-020 → SAP-021-026**: All React SAPs depend on foundation

---

## Domain Navigation Shortcuts

### Building a Capability Server? (NEW - RECOMMENDED)
→ Use **SAP-047 template** for 5-minute generation with all patterns included
→ See: [Progressive Adoption Path 1](#path-1-capability-server-development-new)
→ Quick start: `python scripts/create-capability-server.py --name "YourCapability" --enable-mcp --output ~/projects/your-capability`

### Building a React App?
→ Start with **Infrastructure** + **Developer Experience** + **Foundation** (SAP-020-022, 033-034, 041) + **User-Facing** (SAP-023-024, 035-036)
→ See: [Progressive Adoption Path 2](#path-2-react-application-development)

### Building a Legacy MCP Server?
→ ⚠️ Use **Path 1 (Capability Server)** for new projects. This is for existing SAP-014-based projects only.
→ See: [Progressive Adoption Path 3](#path-3-legacy-mcp-server-development)

### Coordinating Across Repos?
→ Start with **Infrastructure** (SAP-001 Inbox) + **Specialized** (SAP-015 Beads)
→ See: [Progressive Adoption Path 4](#path-4-cross-repository-coordination)

### Improving Process Maturity?
→ Adopt **Specialized** domain (SAP-009, 010, 012, 015, 027)
→ See: [Progressive Adoption Path 5](#path-5-process-maturity--best-practices)

### Need Performance Optimization?
→ **Advanced** domain (SAP-025 react-performance, SAP-026 react-accessibility)

### Need Content Generation?
→ **Advanced** domain (SAP-017, 018 chora-compose)

---

## Status Legend

| Status | Meaning | Next Action |
|--------|---------|-------------|
| **Active** | Production-ready, recommended for all adopters | Maintain, enhance, support |
| **Pilot** | Ready for limited adoption, feedback phase | Collect pilot feedback, iterate |
| **Draft** | In development, artifacts incomplete | Complete artifacts, test with agent |
| **Deprecated** | Superseded, upgrade recommended | Migrate to replacement SAP |
| **Archived** | No longer maintained | Reference only |

**Symbols**:
- ✅ Complete / In use
- 🔄 In progress
- 📋 Planned / Not started
- ⚠️ Warning / Incomplete

---

## Quick Links

**Framework**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](../../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root protocol
- [sap-framework/](sap-framework/) - Framework SAP (SAP-000)
- [document-templates.md](document-templates.md) - SAP artifact templates
- [sap-catalog.json](../../sap-catalog.json) - Machine-readable catalog

**Domain Entry Points**:
- **Infrastructure**: [SAP-000 sap-framework/](sap-framework/), [SAP-001 inbox/](inbox/)
- **Developer Experience**: [SAP-003 project-bootstrap/](project-bootstrap/), [SAP-014 mcp-server-development/](mcp-server-development/)
- **Foundation**: [SAP-020 react-foundation/](react-foundation/)
- **Specialized**: [SAP-009 agent-awareness/](agent-awareness/), [SAP-015 task-tracking/](task-tracking/)

**Examples**:
- [inbox/examples/health-monitoring-w3/](inbox/examples/health-monitoring-w3/) - Complete capability evolution example

---

## How to Use This Index

### For AI Agents

**Finding SAPs by Domain**:
1. Identify your project type (Python MCP, React, coordination, process maturity)
2. Navigate to relevant domain section
3. Review SAP descriptions and features
4. Check dependencies before adoption

**Installing SAPs**:
1. Find SAP in domain section
2. Navigate to SAP directory using location link
3. Read `adoption-blueprint.md` in SAP directory
4. Execute installation steps
5. Verify with post-install validation

**Progressive Context Loading**:
1. Read domain section (10k tokens) for overview
2. Read specific SAP `AGENTS.md` (5k tokens) for quick reference
3. Read `protocol-spec.md` (10-30k tokens) for implementation
4. Read `capability-charter.md` (5-15k tokens) for design rationale (if needed)

### For Humans

**Roadmap Planning**:
- Review "Progressive Adoption Path" for your use case
- Check effort estimates (1-6 days depending on path)
- Plan sprint allocation based on domain priorities

**Dependency Management**:
- Review "SAP Dependency Graph" before installation
- Install dependencies first (SAP-000 is always first)
- Track blockers using SAP-015 (beads task tracking)

**Domain-Based Adoption**:
- Choose starting domain (Infrastructure for all projects)
- Add Developer Experience for tooling
- Choose Foundation (React) or continue with Developer Experience (Python/MCP)
- Expand to User-Facing, Advanced, Specialized as needed

---

## Deprecated SAPs

**Purpose**: Historical record of deprecated SAPs for reference and migration guidance.

### SAP-014: MCP Server Development

- **Status**: deprecated (replaced by SAP-047) | **Version**: 1.0.0 | **Domain**: Developer Experience | **Deprecated**: 2025-11-12
- **Description**: FastMCP-based Model Context Protocol server development patterns with 11 templates and 8 guides. **Deprecated in favor of SAP-047 (CapabilityServer-Template)** for new projects.
- **Dependencies**: SAP-000, SAP-003, SAP-004, SAP-012
- **Location**: [mcp-server-development/](mcp-server-development/)
- **Key Features**: FastMCP patterns, 11 MCP templates, tool definition patterns, testing strategies, deployment workflows
- **⚠️ Migration Path**: Use SAP-047 for new capability server projects. SAP-047 provides multi-interface architecture (CLI, REST, MCP) vs MCP-only approach. Existing SAP-014 projects supported until 2025-12-31.
- **Why Deprecated**: SAP-014 focused on MCP-only servers. SAP-047 supersedes with multi-interface capability servers that include MCP as optional interface alongside CLI and REST APIs.
- **Replacement**: [SAP-047 (CapabilityServer-Template)](capability-server-template/)

---

## Changelog

| Date | Change | Author | Trace ID |
|------|--------|--------|----------|
| 2025-11-12 | SAP-042-047: Capability Server Architecture - Added 6 new SAPs for capability server development (30 → 45 SAPs total). Deprecated SAP-014 in favor of SAP-047 template. Added Path 1 (Capability Server Development) with 5-minute template generation. Updated all domain statistics and dependency graph. | Claude Code | chora-base-4if |
| 2025-11-11 | Feature 6: Domain taxonomy organization - Reorganized 30 SAPs into 6 domains (Infrastructure, Developer Experience, Foundation, User-Facing, Advanced, Specialized) for improved discoverability | Claude Code | DISCO-V5 |
| 2025-11-03 | SAP-027 (dogfooding-patterns) generated - Formalized 5-week dogfooding pilot methodology | Claude Code | - |
| 2025-11-02 | SAP-029 (sap-generation) generated - Template-based SAP artifact generation (80% time savings) | Claude Code | - |
| 2025-11-02 | SAP-028 (publishing-automation) complete - Secure PyPI publishing with OIDC trusted publishing (93% coverage) | Claude Code | - |
| 2025-11-01 | Wave 4: SAP-025 (react-performance) complete - Core Web Vitals optimization (92% coverage) | Claude Code | - |
| 2025-11-01 | Wave 4: SAP-022 (react-linting) complete - ESLint 9 + Prettier 3 (81% coverage) | Claude Code | - |
| 2025-10-31 | SAP-009 v1.1.0 complete: Bidirectional translation layer with 5 domain AGENTS.md files | Claude Code | COORD-2025-004 |
| 2025-10-28 | Wave 2: SAP-016 (link-validation-reference-management) complete - Foundational QA capability | Claude Code | - |
| 2025-10-28 | 🎉 100% COMPLETE! SAP-013 (metrics-tracking) completes Phase 4 - ALL 14 SAPs DONE! | Claude Code | - |
| 2025-10-27 | Initial index creation with phase-based organization (14 capabilities identified) | Claude Code | - |

---

**Maintainer**: Victor (chora-base owner)
**Review Cycle**: Updated with each SAP release
**Organization**: Domain-Based Taxonomy (v1.0.0)
**Last Domain Update**: 2025-11-11 (Feature 6: SAP-DISCO-V5)
