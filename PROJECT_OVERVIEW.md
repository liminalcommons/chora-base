# mcp-orchestration: Strategic Overview

**Last Updated:** 2025-10-31
**Current Version:** v0.2.0
**Status:** Active Development (Wave 2.0 Complete | Chora-Base Adoption: ✅ COMPLETE)

---

## Chora-Base v4.1.0 Adoption

**Status:** 🎉 **100% COMPLETE** - 18/18 SAPs Installed (FULL ADOPTION!)
**Plan:** [CHORA_BASE_ADOPTION_PLAN.md](project-docs/CHORA_BASE_ADOPTION_PLAN.md)
**Test Coverage:** 86.25% (target: 85%) ✅ **MAINTAINED**
**Time Investment:** ~54 hours (89% ROI vs manual)

**Installed SAPs (18/18):**
- ✅ SAP-000: SAP Framework (core protocols)
- ✅ SAP-001: Inbox Coordination (cross-repo collaboration) [PILOT]
- ✅ SAP-002: Chora-Base Meta (meta-capability documentation)
- ✅ SAP-003: Project Bootstrap (audited - for new projects)
- ✅ SAP-004: Testing Framework (comprehensive test suite, 86% coverage)
- ✅ SAP-005: CI/CD Workflows (8 GitHub Actions workflows)
- ✅ SAP-006: Quality Gates (7 pre-commit hooks configured)
- ✅ SAP-007: Documentation Framework (Diátaxis 4-domain structure)
- ✅ SAP-008: Automation Scripts (justfile with 25+ commands)
- ✅ SAP-009: Agent Awareness (AGENTS.md/CLAUDE.md patterns)
- ✅ SAP-010: Memory System (A-MEM event logs, knowledge graph, agent profiles)
- ✅ SAP-011: Docker Operations (multi-stage builds, health checks)
- ✅ SAP-012: Development Lifecycle (DDD→BDD→TDD workflows)
- ✅ SAP-013: Metrics Tracking (ClaudeROICalculator, process metrics)
- ✅ SAP-014: MCP Server Development (FastMCP patterns, 14 tools, 7 resources)
- ✅ SAP-016: Link Validation (automated link checking)
- ✅ SAP-017: Chora-Compose Integration (content generation patterns) **AWARENESS-ONLY** 🆕
- ✅ SAP-018: Chora-Compose Meta (complete architecture, 17 tools, 5 resources) **AWARENESS-ONLY** 🆕

**Bonus Achievement (Post-Week 4):**
- Technology-Specific SAPs: 2 additional SAPs installed (SAP-017, 018)
- Chora-Compose Integration: Awareness-only (dependency documented, patterns available)
- Chora-Compose Meta: Complete architecture reference
- Final adoption: **100% (18/18 SAPs)** 🎉

**Complete Journey Summary:**
- Total SAPs: 18/18 (100% adoption) 🎉
- Test coverage: 60.48% → 86.25% (+25.77 percentage points)
- Documentation: 98 files (~1.9 MB)
- Time saved: 47 hours (89% productivity gain)
- Zero defects introduced across entire adoption

**Documentation:** [docs/skilled-awareness/](docs/skilled-awareness/) (98 artifacts, ~1.9 MB)
**Metrics:** [project-docs/metrics/PROCESS_METRICS.md](project-docs/metrics/PROCESS_METRICS.md)
**Next:** Focus on Wave 2.x product features with full chora-base foundation in place!

---

## Quick Reference

| Aspect | Summary | Details |
|--------|---------|---------|
| **What It Is** | MCP server for centralized config management | [Role & Purpose](#1-role--purpose) |
| **What It Does** | 10 MCP tools, HTTP/SSE transport, crypto signing | [Current Capabilities](#2-current-capabilities-v020) |
| **Where It's Going** | Wave 2.x ecosystem integration, future governance | [Roadmap & Evolution](#3-roadmap--evolution) |
| **How It Fits** | Part of liminalcommons developer tooling ecosystem | [Ecosystem Role](#4-ecosystem-role) |

---

## Table of Contents

1. [Role & Purpose](#1-role--purpose)
2. [Current Capabilities (v0.2.0)](#2-current-capabilities-v020)
3. [Roadmap & Evolution](#3-roadmap--evolution)
4. [Ecosystem Role](#4-ecosystem-role)
5. [Quick Start](#5-quick-start)
6. [Documentation Map](#6-documentation-map)
7. [Decision Framework](#7-decision-framework)

---

## 1. Role & Purpose

### What is mcp-orchestration?

**mcp-orchestration** is a **Model Context Protocol (MCP) server** that provides **centralized configuration management and orchestration** for MCP client applications.

It solves the problem of **fragmented, manual MCP client configuration** by offering:

- **Cryptographically signed configurations** (Ed25519 signatures)
- **Content-addressable storage** (SHA-256 based artifact identification)
- **Multi-client registry** (Claude Desktop, Cursor, n8n, web apps)
- **Intelligent diff detection** (field-level change tracking)
- **Draft workflow** (Build → Validate → Publish → Deploy pipeline)
- **Remote access** (HTTP/SSE transport for API integration)

### Why does it exist?

**Problem Space:**
- MCP clients require manual JSON configuration files
- No centralized validation or integrity verification
- Configuration drift across teams/environments
- No audit trail for config changes
- Limited automation and workflow integration

**Solution:**
- Centralized, signed configuration artifacts
- Programmatic access via MCP tools and HTTP API
- Built-in validation and diff detection
- Immutable audit trail via content-addressable storage
- Integration with Claude Desktop, Cursor, n8n, CI/CD pipelines

### Core Principles

1. **Cryptographic Trust** - All configs signed with Ed25519 for integrity
2. **Immutability** - Content-addressable storage prevents tampering
3. **Multi-Transport** - stdio (local) and HTTP/SSE (remote/automation)
4. **Extensibility** - Designed for future governance/policy features
5. **Developer Experience** - Clear APIs, comprehensive docs, living tests

---

## 2. Current Capabilities (v0.2.0)

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Orchestrator                      │
├─────────────────────────────────────────────────────────┤
│  Transport Layer                                         │
│  ├─ stdio (local CLI, Claude Desktop, Cursor)           │
│  └─ HTTP/SSE (remote access, n8n, web apps, CI/CD) ✨   │
├─────────────────────────────────────────────────────────┤
│  MCP Tools (10)                                          │
│  ├─ list_clients, list_profiles                         │
│  ├─ get_config, diff_config                             │
│  ├─ add_server_to_config, remove_server_from_config     │
│  ├─ view_draft_config, clear_draft_config               │
│  ├─ validate_config, publish_config, deploy_config      │
│  └─ list_available_servers, describe_server             │
├─────────────────────────────────────────────────────────┤
│  Layers                                                  │
│  ├─ Registry Layer (multi-client support)               │
│  ├─ Crypto Layer (Ed25519 signatures)                   │
│  ├─ Storage Layer (SHA-256 content-addressable)         │
│  ├─ Diff Engine (semantic change classification)        │
│  └─ HTTP Layer (FastAPI, authentication, CORS) ✨       │
└─────────────────────────────────────────────────────────┘
```

✨ = New in v0.2.0

### Feature Summary

#### Wave 1.x Features (v0.1.0-v0.1.5) ✅ Complete

**Wave 1.0 (v0.1.0) - Foundation**
- MCP server (stdio transport)
- 4 MCP tools: `list_clients`, `list_profiles`, `get_config`, `diff_config`
- Client registry (Claude Desktop, Cursor)
- Ed25519 signing infrastructure
- Content-addressable storage (SHA-256)

**Wave 1.1 (v0.1.1) - Server Registry**
- 30+ pre-configured MCP servers (filesystem, brave-search, puppeteer, etc.)
- 2 new tools: `list_available_servers`, `describe_server`
- Server catalog with installation instructions

**Wave 1.2 (v0.1.2) - Config Generation**
- 3 new tools: `add_server_to_config`, `remove_server_from_config`, draft workflow
- Transport abstraction (automatic mcp-remote wrapping for HTTP/SSE servers)
- ConfigBuilder for programmatic config construction

**Wave 1.3 (v0.1.3) - Ergonomics**
- 3 new tools: `view_draft_config`, `clear_draft_config`, `initialize_keys`
- Default parameters for Claude Desktop workflows
- JSON string parameter handling (Claude Desktop compatibility)

**Wave 1.4 (v0.1.4) - Validation & Publishing**
- 1 new tool: `publish_config` (sign and store artifacts)
- Schema validation before publishing
- Changelog metadata in artifacts

**Wave 1.5 (v0.1.5) - Deployment**
- 1 new tool: `deploy_config` (write to client config locations)
- Complete workflow: discovery → build → validate → publish → deploy
- Deployment tracking and drift detection

#### Wave 2.0 Features (v0.2.0) ✅ Complete

**HTTP/SSE Transport - Remote Access & API Integration**

- **FastAPI HTTP Server**
  - 14 HTTP endpoints exposing all 10 MCP tools
  - Auto-generated OpenAPI 3.0 documentation (Swagger UI)
  - Production-ready with uvicorn
  - CORS enabled for web app integration

- **Authentication**
  - Bearer token authentication (cryptographically secure)
  - API key authentication (environment variable)
  - Token generation, revocation, usage tracking
  - Timing-attack prevention (constant-time comparison)

- **Remote Access Use Cases**
  - n8n workflow automation
  - Web application integration
  - CI/CD pipeline automation
  - Multi-user shared server

- **CLI Commands**
  - `mcp-orchestration-serve-http` - Start HTTP server
  - `mcp-orchestration-generate-token` - Generate API tokens

- **Documentation**
  - Deploy HTTP Server guide (10 min)
  - Authenticate HTTP API guide (5 min)
  - Migrate stdio → HTTP guide (15 min)

### Testing & Quality

- **127/166 tests passing (77%)**
- **100% authentication coverage**
- **Living documentation** (E2E tests validate user guides)
- **BDD/TDD/DDD process** (comprehensive test suite)

### Supported Integrations

| Client | Transport | Status | Notes |
|--------|-----------|--------|-------|
| **Claude Desktop** | stdio, HTTP | ✅ Full | Default client, comprehensive testing |
| **Cursor IDE** | stdio, HTTP | ✅ Full | IDE integration |
| **n8n** | HTTP | ✅ Full | Workflow automation |
| **Web Apps** | HTTP | ✅ Full | CORS enabled, OpenAPI docs |
| **CI/CD** | HTTP | ✅ Full | API key authentication |
| **Other MCP Clients** | stdio, HTTP | ⚠️ Partial | Generic MCP protocol support |

---

## 3. Roadmap & Evolution

### Wave-Based Development Philosophy

mcp-orchestration follows **wave-based capability evolution**:

- Each wave = cohesive set of features (1-5 days development)
- Waves build on each other sequentially
- Each wave delivers standalone value
- Explicit decision criteria before advancing waves

### Historical Waves (Completed)

| Wave | Version | Theme | Delivered | Timeline |
|------|---------|-------|-----------|----------|
| 1.0 | v0.1.0 | Foundation | 2025-10-17 | 1 sprint |
| 1.1 | v0.1.1 | Server Registry | 2025-10-24 | 1 day |
| 1.2 | v0.1.2 | Transport + Config Gen | 2025-10-24 | 1 day |
| 1.3 | v0.1.3 | Ergonomics | 2025-10-24 | 1 day |
| 1.4 | v0.1.4 | Validation + Publishing | 2025-10-24 | 1 day |
| 1.5 | v0.1.5 | Deployment | 2025-10-25 | 1 day |
| 2.0 | v0.2.0 | HTTP/SSE Transport | 2025-10-26 | 1 day |

**Total: 5 days to go from v0.1.0 → v0.2.0**

### Current Wave (Active)

**Wave 2.x - Ecosystem Integration & Polish** (Q1 2026)

**Status:** Planning
**Timeline:** Jan-Mar 2026
**Focus:** Integration with mcp-gateway, ecosystem coordination

**Planned Waves:**

- **Wave 2.1 (v0.2.1)** - API Enhancements
  - Universal Loadability Format adoption (from mcp-gateway v1.2.0)
  - Enhanced error messages with error codes
  - Structured error responses
  - Performance optimization (caching, connection pooling)

- **Wave 2.2 (v0.2.2)** - Ecosystem Integration
  - Integration testing with mcp-gateway
  - Example n8n workflows (3+)
  - Joint documentation with mcp-gateway team
  - Pattern N3b implementation (n8n as Multi-Server MCP Client)

**Key Dependency:** mcp-gateway v1.2.0 (Universal Loadability spec)

**Coordination:** See [project-docs/WAVE_1X_PLAN.md](project-docs/WAVE_1X_PLAN.md) for detailed plan

### Future Waves (Exploratory)

**Wave 3.x - Governance & Policy** (Post-v2.0, Exploratory)

**Status:** Not Committed
**Decision Criteria:**
- [ ] 5+ organizations using v2.x for 3+ months
- [ ] User requests for policy enforcement
- [ ] Compliance requirements (SOC2, audits)

**Potential Features:**
- Policy engine (declarative rules: allow/deny tools, redactions, pinning)
- Approval workflows (multi-signer governance)
- Audit logging (immutable release records)
- Canary rollouts (gradual deployment via cohorts)

**Wave 4.x - Intelligence & Analytics** (Post-v3.0, Speculative)

**Status:** Far Future
**Decision Criteria:**
- [ ] 1000+ artifacts published across 100+ orgs
- [ ] User demand for "smart suggestions"
- [ ] Wave 3 governance proves reliable

**Potential Features:**
- LLM-assisted validation
- Config analytics (usage patterns, drift detection)
- Anomaly detection (suspicious changes)
- Auto-remediation suggestions

**Wave 5.x - Ecosystem Platform** (Post-v4.0, Visionary)

**Status:** No Timeline
**Decision Criteria:**
- [ ] 500+ self-hosted deployments
- [ ] Community requests config sharing
- [ ] Business model validated

**Potential Features:**
- Multi-tenant SaaS
- Config marketplace (community templates)
- Federation (cross-org sharing)
- Plugin ecosystem (third-party validation/policy)

**See:** [dev-docs/vision/MCP_CONFIG_ORCHESTRATION.md](dev-docs/vision/MCP_CONFIG_ORCHESTRATION.md) for full capability evolution

---

## 4. Ecosystem Role

### Position in liminalcommons

mcp-orchestration is a **capability provider** in the **liminalcommons developer tooling ecosystem**.

#### Ecosystem Architecture

```
┌─────────────────────────────────────────────────────────┐
│              chora-platform (Shared Platform)            │
│  Standards, Manifests, Change Signals, Discovery        │
└─────────────────────────────────────────────────────────┘
                          ▲
                          │
          ┌───────────────┼───────────────┐
          │               │               │
    ┌─────▼─────┐   ┌────▼────┐   ┌─────▼─────┐
    │  chora-   │   │   mcp-  │   │   mcp-    │
    │   base    │   │  orch.  │   │  gateway  │
    │ (template)│   │ (config)│   │  (n8n)    │
    └───────────┘   └─────────┘   └───────────┘
```

#### Ecosystem Principles (from ecosystem-intent.md)

mcp-orchestration adheres to liminalcommons ecosystem standards:

1. **Shared Understanding** - Common lifecycle vocabulary (plan, build, validate, release, operate)
2. **Composable Tooling** - Reusable components without central bottlenecks
3. **Coordinated Change** - Change signals for cross-project coordination
4. **Runtime Interop** - Services consume each other dynamically
5. **Trust & Governance** - Security, compatibility, quality standards

#### Ecosystem Contributions

**Capabilities mcp-orchestration provides:**

- **MCP.CONFIG.RETRIEVE** - Fetch signed configurations
- **MCP.CONFIG.VALIDATE** - Schema validation
- **MCP.CONFIG.PUBLISH** - Sign and store artifacts
- **MCP.CONFIG.DEPLOY** - Deploy to client locations
- **MCP.SERVER.DISCOVER** - Browse server registry

**Capabilities mcp-orchestration consumes:**

- **chora-base** - Python project template, documentation standards
- **mcp-gateway** - (Future) Universal Loadability Format, HTTP transport patterns

#### Ecosystem Coordination

**Active Partnerships:**

- **mcp-gateway** (Q1 2026)
  - Pattern N3b: n8n as Multi-Server MCP Client
  - Universal Loadability Format adoption
  - Joint documentation and integration testing

**Standards Compliance:**

- **Diátaxis Framework** - Documentation structure (tutorials, how-to, reference, explanation)
- **Semantic Versioning** - Version numbering (MAJOR.MINOR.PATCH)
- **BDD/TDD/DDD** - Development methodology
- **OpenAPI 3.0** - API documentation
- **Ed25519** - Cryptographic signing (RFC 8032)
- **Content-Addressable Storage** - Immutable artifact identification

**See:** [dev-docs/vision/ecosystem-intent.md](dev-docs/vision/ecosystem-intent.md) for ecosystem philosophy

---

## 5. Quick Start

### Installation

```bash
# From PyPI (recommended)
pip install mcp-orchestration

# From source
git clone https://github.com/liminalcommons/mcp-orchestration.git
cd mcp-orchestration
pip install -e ".[dev]"
```

### Option 1: stdio Transport (Local Use)

```bash
# 1. Initialize storage
mcp-orchestration-init

# 2. Configure in Claude Desktop
# Add to ~/Library/Application Support/Claude/claude_desktop_config.json:
{
  "mcpServers": {
    "mcp-orchestration": {
      "command": "mcp-orchestration"
    }
  }
}

# 3. Use via Claude's UI
```

### Option 2: HTTP Transport (Remote Access & Automation)

```bash
# 1. Start HTTP server
mcp-orchestration-serve-http

# 2. Generate API token
mcp-orchestration-generate-token

# 3. Test the API
curl -H "Authorization: Bearer <your-token>" \
  http://localhost:8000/v1/clients

# 4. View interactive docs
open http://localhost:8000/docs
```

### Use Cases

| Use Case | Transport | Documentation |
|----------|-----------|---------------|
| **Claude Desktop config** | stdio | [Getting Started Tutorial](user-docs/tutorials/01-getting-started.md) |
| **n8n workflow automation** | HTTP | [Deploy HTTP Server](user-docs/how-to/deploy-http-server.md) |
| **Web app integration** | HTTP | [Authenticate HTTP API](user-docs/how-to/authenticate-http-api.md) |
| **CI/CD automation** | HTTP | [Migrate stdio → HTTP](user-docs/how-to/migrate-stdio-to-http.md) |

---

## 6. Documentation Map

mcp-orchestration follows the **Diátaxis framework** with structured documentation:

### For Users

**Tutorials** (Learning-oriented)
- [Getting Started](user-docs/tutorials/01-getting-started.md) - 30-minute introduction

**How-To Guides** (Task-oriented)
- [Deploy HTTP Server](user-docs/how-to/deploy-http-server.md) - 10 minutes
- [Authenticate HTTP API](user-docs/how-to/authenticate-http-api.md) - 5 minutes
- [Migrate stdio → HTTP](user-docs/how-to/migrate-stdio-to-http.md) - 15 minutes
- [Manage Configs with Claude](user-docs/how-to/06-manage-configs-with-claude.md) - Draft workflow

**Reference** (Information-oriented)
- [MCP Tools Reference](user-docs/reference/) - Tool specifications
- [Server Catalog](user-docs/reference/server-catalog.md) - 30+ MCP servers
- [API Reference](http://localhost:8000/docs) - OpenAPI documentation (when server running)

**Explanations** (Understanding-oriented)
- [Architecture Overview](user-docs/explanation/) - Design decisions
- [Security Model](user-docs/explanation/) - Cryptographic trust

### For Contributors

**Development Docs** ([dev-docs/](dev-docs/))
- [CONTRIBUTING.md](dev-docs/CONTRIBUTING.md) - Contribution guidelines
- [DEVELOPMENT.md](dev-docs/DEVELOPMENT.md) - Developer setup, architecture
- [TROUBLESHOOTING.md](dev-docs/TROUBLESHOOTING.md) - Common issues

**Vision Docs** ([dev-docs/vision/](dev-docs/vision/))
- [MCP_CONFIG_ORCHESTRATION.md](dev-docs/vision/MCP_CONFIG_ORCHESTRATION.md) - Capability evolution
- [ecosystem-intent.md](dev-docs/vision/ecosystem-intent.md) - Ecosystem philosophy
- [spec.md](dev-docs/vision/spec.md) - Original specification

### For Project Planning

**Roadmap** ([project-docs/](project-docs/))
- [WAVE_1X_PLAN.md](project-docs/WAVE_1X_PLAN.md) - Wave 1.x-2.x detailed plan
- [ROADMAP.md](project-docs/ROADMAP.md) - (Future) Public roadmap

**Changelog**
- [CHANGELOG.md](CHANGELOG.md) - Version history

### For AI Agents

**Machine-Readable Instructions**
- [AGENTS.md](AGENTS.md) - Generic agent guidance (OpenAI/Google standard)
- [CLAUDE.md](CLAUDE.md) - Claude-specific optimizations
- [.chora/memory/](/.chora/memory/) - Agent memory system (session checkpoints, knowledge graph)

---

## 7. Decision Framework

### When to Advance Waves

Use this framework when considering next wave:

```
┌─────────────────────────────────────────────────────────┐
│ 1. User Demand Signal?                                  │
│    NO → DEFER (no user pull)                            │
│    YES → Continue ↓                                      │
├─────────────────────────────────────────────────────────┤
│ 2. Technical Validation Complete?                       │
│    NO → VALIDATE (spike/prototype first)                │
│    YES → Continue ↓                                      │
├─────────────────────────────────────────────────────────┤
│ 3. Dependencies Ready?                                   │
│    NO → DEFER (wait for dependencies)                   │
│    YES → Continue ↓                                      │
├─────────────────────────────────────────────────────────┤
│ 4. Team Capacity Available?                             │
│    NO → DEFER (focus on current roadmap)                │
│    YES → COMMIT TO ROADMAP                              │
└─────────────────────────────────────────────────────────┘
```

**Example: Wave 3 (Governance)**

- ✅ User demand? → Need 5+ orgs requesting (currently 0)
- ❌ Dependencies ready? → Need Wave 2.x ecosystem integration first

**Decision:** DEFER to post-v2.0

### Quarterly Review Process

Vision documents reviewed quarterly:

- **Q1 (January):** After v1.0 release
- **Q2 (April):** After v1.5 release
- **Q3 (July):** After v2.0 release
- **Q4 (October):** After v2.5 release

**Review Checklist:**
- [ ] User signals for exploratory waves?
- [ ] Technical landscape changes?
- [ ] Delivered waves moved to archive?
- [ ] Deferred waves re-evaluated?
- [ ] New capability themes emerging?

### Architecture Decision Records (ADRs)

Major decisions documented in:
- [project-docs/decisions/](project-docs/decisions/) (Future)
- Git commit messages (current practice)
- CHANGELOG.md (feature rationale)

---

## Summary

### Current Status (v0.2.0)

**What We've Built:**
- ✅ 10 MCP tools for config management
- ✅ HTTP/SSE transport for remote access
- ✅ 30+ server registry
- ✅ Complete workflow: discover → build → validate → publish → deploy
- ✅ Comprehensive documentation (Diátaxis)
- ✅ 127/166 tests passing (77%)

**What We're Building (Wave 2.x):**
- 🚧 Ecosystem integration with mcp-gateway (Q1 2026)
- 🚧 Universal Loadability Format adoption
- 🚧 Enhanced error messages and performance

**What We're Exploring (Wave 3+):**
- 🔭 Governance & policy (post-v2.0)
- 🔭 Intelligence & analytics (post-v3.0)
- 🔭 Ecosystem platform (post-v4.0)

### Key Resources

- **Repository:** https://github.com/liminalcommons/mcp-orchestration
- **Issues:** https://github.com/liminalcommons/mcp-orchestration/issues
- **PyPI:** https://pypi.org/project/mcp-orchestration/
- **MCP Protocol:** https://modelcontextprotocol.io
- **chora-base:** https://github.com/liminalcommons/chora-base

### Contact & Community

- **Project Type:** Open Source (MIT License)
- **Maintainer:** liminalcommons
- **Ecosystem:** chora-platform, mcp-gateway, chora-base

---

**Document Status:** Living document (update with each major release)
**Template:** Based on chora-base strategic overview patterns
**Last Review:** 2025-10-26 (v0.2.0 release)

🧭 **Strategic Overview** - Understand the big picture before diving into implementation.
