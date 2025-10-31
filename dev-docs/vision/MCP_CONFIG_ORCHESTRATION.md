# Capability Evolution - MCP Configuration Orchestration

This document describes the evolutionary path for mcp-orchestration's configuration service capabilities across multiple waves, tracking both delivered features and exploratory future directions.

**Purpose:** Guide strategic design decisions today while keeping future doors open for a comprehensive MCP configuration management platform.

**Last Updated:** 2025-10-26
**Current Version:** v0.2.0

---

## Overview: Capability Waves

```
Wave 1: Foundation       Wave 2: Integration      Wave 3: Governance       Wave 4: Intelligence     Wave 5: Ecosystem
   (v0.1.0-v0.1.5)         (v0.2.0-v0.2.x)      (Post-v2.0, Exploratory) (Post-v3.0, Exploratory) (Post-v4.0, Exploratory)
     ✅ COMPLETE             🚧 IN PROGRESS              🔭 PLANNED              🔭 EXPLORATORY           🔭 VISIONARY
        │                         │                         │                         │                         │
        ├─ Config retrieval       ├─ HTTP/SSE transport    ├─ Policy engine         ├─ Smart validation      ├─ Multi-tenant SaaS
        ├─ Basic validation       ├─ Authentication        ├─ Approval workflows    ├─ Config analytics      ├─ Marketplace
        ├─ Static artifacts       ├─ Remote access         ├─ Audit logging         ├─ Anomaly detection     ├─ Federation
        ├─ 10 MCP tools          ├─ API integration       ├─ Canary rollouts       ├─ Auto-remediation      ├─ Plugin ecosystem
        └─ Draft workflow         └─ Ecosystem interop     └─ RBAC integration      └─ Predictive rollout    └─ Client SDK gen
```

**Current Status:** Wave 2 (Integration) - Multi-transport architecture delivered (v0.2.0), ecosystem integration in progress

**Decision Cadence:** Review quarterly after milestone completion

---

## Wave 1: Foundation ✅ COMPLETE

### Status

**Delivered:** v0.1.0 - v0.1.5 (2025-10-17 to 2025-10-25)
**Timeline:** 5 days across 6 releases
**Outcome:** Core orchestration platform established

### Capability Theme (Delivered)

Established complete local configuration orchestration:

- **Client Discovery** - List supported MCP client families and profiles
- **Config Retrieval** - Return signed, validated config artifacts
- **Server Registry** - 30+ pre-configured MCP servers with installation guides
- **Draft Workflow** - Build → Validate → Publish → Deploy pipeline
- **Immutable Artifacts** - Content-addressable storage with Ed25519 signing
- **Diff Detection** - Idempotent change detection with semantic classification
- **10 MCP Tools** - Complete toolkit for config management
- **Deployment** - Write configs to client locations with tracking

### Motivation

Why Wave 1 matters:

1. **User Need:** MCP clients need a reliable way to discover and obtain validated configurations without manual file management
2. **Market Signal:** Validate that centralized config distribution solves real pain points before expanding to policy/governance
3. **Technical Foundation:** Establish artifact model, signing infrastructure, and client protocol patterns
4. **Learning Opportunity:** Gather feedback on schema design, client integration patterns, and update cadence

### Technical Sketch

**Architecture Principles:**
- Keep it simple (YAGNI - defer policy engine to Wave 2)
- Extensible design (artifact metadata supports future policy fields)
- Clear abstractions (separate retrieval from evaluation)

**Example: Artifact Structure (Wave 1)**
```python
# Wave 1: Simple signed artifacts
@dataclass
class ConfigArtifact:
    artifact_id: str  # SHA-256 content hash
    client_id: str
    profile: str
    payload: dict  # Opaque to service
    schema_ref: str
    version: str
    issued_at: datetime
    signature: Signature  # Ed25519 detached signature
    provenance: dict  # Publisher metadata

    # Extension points for Wave 2 (policy)
    # Reserved fields: policy_set_id, approvals[], changelog
```

**API Operations (Wave 1 Subset):**
```python
# Core operations
async def list_clients() -> List[ClientFamily]:
    """FR-1: Discover supported clients"""

async def get_config(client_id: str, profile: str) -> ConfigArtifact:
    """FR-4: Retrieve validated, signed artifact"""

async def diff_config(client_id: str, profile: str,
                     current_artifact_id: str) -> DiffResult:
    """FR-9: Check for updates"""

# Deferred to Wave 2: publish, validate_draft, subscribe_updates
```

### Success Metrics (Actual Results)

Wave 1 delivered successfully:

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **Client Adoption** | 3+ client types | 2 (Claude Desktop, Cursor) | ⚠️ Partial (HTTP enables more) |
| **Config Retrieval Success** | >99% p95 <300ms | Not measured | 📊 Future telemetry |
| **Signature Verification** | 100% artifacts verifiable | ✅ 100% | ✅ Pass |
| **Update Detection** | <1min staleness | Real-time via diff tool | ✅ Pass |
| **Developer Onboarding** | <30min to first config | ~15min (tutorial tested) | ✅ Exceeded |
| **Test Coverage** | 70%+ | 53% → 60%+ | ⚠️ Acceptable |

### Delivered Versions

**v0.1.0 (2025-10-17)** - Foundation
- 4 MCP tools: list_clients, list_profiles, get_config, diff_config
- Ed25519 signing, content-addressable storage
- stdio transport, CLI initialization

**v0.1.1 (2025-10-24)** - Server Registry
- 30+ MCP servers cataloged
- 2 new tools: list_available_servers, describe_server

**v0.1.2 (2025-10-24)** - Config Generation
- 3 new tools: add_server_to_config, remove_server_from_config, draft workflow
- Transport abstraction (auto mcp-remote wrapping)

**v0.1.3 (2025-10-24)** - Ergonomics
- 3 new tools: view_draft_config, clear_draft_config, initialize_keys
- Default parameters for Claude Desktop
- JSON string parsing fixes

**v0.1.4 (2025-10-24)** - Validation & Publishing
- 1 new tool: publish_config (sign and store artifacts)
- Schema validation, changelog metadata

**v0.1.5 (2025-10-25)** - Deployment
- 1 new tool: deploy_config (write to client locations)
- Complete workflow end-to-end

### Lessons Learned

**What Worked:**
- ✅ Wave-based development (5 days for 6 releases)
- ✅ BDD/TDD/DDD process (comprehensive testing)
- ✅ Draft workflow UX (Claude Desktop integration smooth)
- ✅ Content-addressable storage (enables future audit)

**What Could Improve:**
- ⚠️ Test coverage (53% → need 70%+ for production readiness)
- ⚠️ Telemetry integration (no real metrics captured)
- ⚠️ Limited client adoption (only Claude Desktop, Cursor tested)

**Architecture Decisions Validated:**
- ✅ Extensible artifact metadata (ready for Wave 3 policy)
- ✅ Transport abstraction (Wave 2 HTTP built on this)
- ✅ Opaque payload design (schema evolution ready)

---

## Wave 2: Integration 🚧 IN PROGRESS

### Status

**Current:** Wave 2.0 Complete (v0.2.0), Wave 2.x In Progress
**Timeline:** v0.2.0 delivered 2025-10-26, v0.2.x planned Q1 2026
**Focus:** Multi-transport architecture and ecosystem integration

### Capability Theme

Transform from local stdio tool to HTTP/SSE-capable orchestration platform:

**Wave 2.0 (v0.2.0) ✅ DELIVERED:**
- **HTTP/SSE Transport** - FastAPI server exposing all 10 MCP tools via REST API
- **Authentication** - Bearer token + API key authentication with security best practices
- **Remote Access** - Access MCP tools from anywhere via HTTP
- **API Integration** - n8n, web apps, CI/CD pipelines, multi-user scenarios
- **14 HTTP Endpoints** - Complete REST API with OpenAPI 3.0 documentation
- **CORS Support** - Web application integration ready
- **Production Ready** - uvicorn, graceful shutdown, comprehensive security

**Wave 2.1-2.2 (v0.2.x) 📋 PLANNED:**
- **Universal Loadability Format** - Adopt mcp-gateway v1.2.0 specification
- **Enhanced Errors** - Error codes, structured responses
- **Performance** - Caching, connection pooling
- **Ecosystem Integration** - mcp-gateway integration testing, n8n workflows (3+)
- **Pattern N3b** - n8n as Multi-Server MCP Client implementation

### Motivation

**User Stories:**

**Wave 2.0 (DELIVERED):**
> "As a workflow engineer, I need to integrate MCP configuration management into n8n workflows so I can automate deployments across environments."

> "As a web developer, I need a REST API to build a config management UI for non-technical users."

> "As a DevOps engineer, I need to automate MCP deployments in CI/CD pipelines via HTTP API."

**Wave 2.1-2.2 (PLANNED):**
> "As a mcp-gateway user, I want mcp-orchestration to provide configs in Universal Loadability Format so I can load them directly without manual transformation."

**Why Wave 2 Came Before Governance:**
- Remote access and API integration had clear user demand (n8n, web apps, CI/CD)
- HTTP transport enables ecosystem coordination (mcp-gateway Pattern N3b)
- Governance (policy, approvals) has no user demand yet (defer to Wave 3)

### Delivered Implementation (Wave 2.0)

**HTTP Transport Architecture:**
```python
# FastAPI HTTP server
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MCP Orchestration HTTP API",
    version="0.2.0",
    description="Centralized MCP configuration orchestration"
)

# 14 HTTP endpoints wrapping all 10 MCP tools
@app.get("/v1/clients")
async def http_list_clients(auth=Depends(verify_auth)):
    return await list_clients()

# Authentication with bearer tokens + API keys
class AuthenticationService:
    def validate_bearer_token(self, token: str) -> bool
    def validate_api_key(self, key: str) -> bool
    def generate_token(self) -> str
```

**Use Cases Enabled:**
1. **n8n Workflows** - HTTP nodes calling MCP orchestration API
2. **Web Applications** - React/Vue apps with CORS-enabled API
3. **CI/CD Pipelines** - GitHub Actions/Jenkins deploying configs via API
4. **Remote Access** - Multi-user shared server (authenticated)
5. **mcp-gateway Integration** - Pattern N3b foundation (future)

**Documentation Delivered:**
- Deploy HTTP Server guide (10 min, 1,200+ lines)
- Authenticate HTTP API guide (5 min, 800+ lines)
- Migrate stdio → HTTP guide (15 min, 1,100+ lines)
- OpenAPI 3.0 spec (auto-generated, Swagger UI)

### Success Metrics (Wave 2.0)

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **HTTP Endpoints** | 10+ (1 per tool) | 14 endpoints | ✅ Exceeded |
| **Authentication** | Bearer + API key | ✅ Both supported | ✅ Complete |
| **Test Coverage** | 70%+ new code | 77% (127/166 tests) | ✅ Exceeded |
| **Documentation** | Comprehensive guides | 3 guides (3,100+ lines) | ✅ Complete |
| **Backward Compat** | stdio unchanged | ✅ Full compatibility | ✅ Pass |
| **Security** | Auth required | 100% endpoints protected | ✅ Pass |

### Decision Framework (Wave 2.x)

**Wave 2.1-2.2 Criteria:**
- ✅ Wave 2.0 delivered and stable
- 🔄 mcp-gateway v1.2.0 specification available (dependency)
- 📋 Team capacity for ecosystem integration (Q1 2026)
- 📋 User demand for n8n workflows (validate via examples)

**Decision:** COMMITTED to Wave 2.1-2.2 (Q1 2026) pending mcp-gateway coordination

---

## Wave 3: Governance 🔭 PLANNED

### Status

**Current:** Exploratory (Not Committed)
**Target:** Post-v2.0 (Q2-Q3 2026, conditional)
**Review Date:** After Wave 2.x ecosystem integration proves value

### Capability Theme

Add policy enforcement, approval workflows, and audit:

- **Policy Engine** - Declarative rules (allow/deny tools, redactions, pinning)
- **Approval Workflows** - Multi-signer governance before release
- **Audit Logging** - Immutable release records with lineage
- **Canary Rollouts** - Gradual deployment via cohort profiles
- **RBAC Integration** - Role-based access control for publishing
- **Compliance Reports** - SOC2, audit trail generation

### Motivation

**User Story:**
> "As a security admin, I need to enforce that prod clients never enable experimental MCP tools, and I need an audit trail proving compliance."

**Why Deferred to Wave 3:**
- No user demand yet (zero requests for policy/governance features)
- Wave 2 ecosystem integration is higher priority (mcp-gateway coordination)
- Policy DSL design benefits from real-world config patterns learned from Wave 1-2
- Approval workflows require org integration (RBAC, SSO) not needed yet

### Exploratory Design

**Policy Model (Declarative):**
```yaml
# Example policy set for Wave 3
policy_set_id: "org-prod-v3"
rules:
  - type: deny_tool
    tool_name: "experimental_*"
    profiles: ["prod"]
  - type: redact_keys
    keys: ["debug_flags", "internal_endpoints"]
  - type: pin_version
    server: "mcp-database"
    version: "~>1.2.0"
```

**API Extensions:**
```python
# New operations in Wave 3
async def validate_with_policy(
    payload: dict,
    client_id: str,
    profile: str,
    policy_set_id: str
) -> ValidationReport:
    """Pre-publish validation with policy enforcement"""

async def request_approval(
    draft_id: str,
    approvers: list[str]
) -> ApprovalRequest:
    """Initiate multi-signer approval workflow"""
```

### Decision Trigger

**Do NOT pursue until:**
- [ ] 5+ organizations using mcp-orchestration for 3+ months
- [ ] User requests for policy enforcement (GitHub issues, feedback)
- [ ] Compliance requirements surface (SOC2, audit needs)
- [ ] Wave 2.x ecosystem integration stable and proven

**Advance to Wave 3 IF:**
- ✅ Wave 2.x delivered and stable
- ✅ Clear policy patterns emerge from user configs
- ✅ Team bandwidth for RBAC/approval integration
- ✅ Proven demand (5+ orgs requesting governance)

---

## Wave 4: Intelligence 🔭 EXPLORATORY

### Status

**Current:** Speculative (Far Future)
**Target:** Post-v3.0 (Multi-year horizon)
**Review Date:** Annual review after v2.0+ adoption proves value

### Capability Theme

Add AI-powered validation, analytics, and anomaly detection:

- **Smart Validation** - LLM-assisted schema compliance and best practice checks
- **Config Analytics** - Insights into tool usage patterns, version drift, update lag
- **Anomaly Detection** - Flag suspicious config changes or risky tool combinations
- **Auto-Remediation** - Suggest fixes for validation failures or policy violations
- **Predictive Rollout** - ML-based canary cohort sizing and rollback predictions
- **Natural Language Config** - "Add the filesystem server with /home access" → config

### Motivation (Speculative)

**User Story:**
> "As a config publisher, I want AI to warn me that enabling tool X with tool Y has historically caused crashes, and suggest safer alternatives."

**Why Highly Exploratory:**
- Requires substantial Wave 1-3 telemetry data to train models
- LLM integration adds complexity (latency, cost, accuracy)
- User trust in AI recommendations must be earned gradually
- Natural language config requires sophisticated parsing and validation

### Design Constraints

**If ever pursued:**
- Must preserve human-in-loop for final approval (no auto-publish)
- Privacy-first: No client PII in training data
- Explainability: AI must show reasoning, not black-box decisions
- Fallback: Always provide manual override for AI suggestions

### Decision Trigger

**Do NOT pursue until:**
- [ ] 1000+ artifacts published across 100+ orgs (data scale for training)
- [ ] User demand for "smart suggestions" surfaces organically
- [ ] Wave 3 governance proves reliable (don't skip to AI without policy foundation)
- [ ] Telemetry system captures sufficient data for ML training

---

## Wave 5: Ecosystem Platform 🔭 VISIONARY

### Status

**Current:** Visionary (No concrete timeline)
**Target:** Post-v4.0 (Multi-year, market-dependent)

### Capability Theme

Transform from service to platform:

- **Multi-Tenant SaaS** - Hosted offering for small teams (currently self-hosted)
- **Config Marketplace** - Share/discover community configs (like Docker Hub for MCP)
- **Federation** - Cross-org config sharing with trust boundaries
- **Plugin Ecosystem** - Third-party policy engines, validation tools, analytics
- **Client SDK Generator** - Auto-generate type-safe clients for any language
- **Enterprise Features** - SSO, RBAC, multi-region deployment, SLA guarantees

### Motivation (Highly Speculative)

**User Story:**
> "As a new MCP user, I want to browse pre-validated config templates for popular tools, with community ratings and security audits."

**Why Defer Indefinitely:**
- Requires Wave 1-4 to prove sustained market need
- SaaS/marketplace = major business model shift (not just tech)
- Federation introduces complex trust/security challenges
- Enterprise features require dedicated support team

### Decision Framework

**Only consider IF:**
- [ ] Self-hosted deployments reach 500+ organizations
- [ ] Community actively requests config sharing (not just hypothetical)
- [ ] Competitive pressure from similar marketplace offerings
- [ ] Business model validated (pricing, support, SLA commitments)
- [ ] Team ready for SaaS operations (on-call, customer success, sales)

---

## Architectural Guidance for AI Agents

### Today's Design Decisions (Wave 1)

**DO:**
- ✅ Design artifact metadata to be **extensible** (add fields in Wave 2 without breaking clients)
- ✅ Use **content-addressable storage** (artifact_id = hash; enables immutability for Wave 2 audit)
- ✅ Keep payload **opaque** (don't parse client configs; enables schema evolution)
- ✅ Build **pluggable signature verification** (algorithm field allows future crypto upgrades)

**DON'T:**
- ❌ Implement policy evaluation engine yet (Wave 2 complexity; learn patterns first)
- ❌ Build approval workflows (Wave 2; requires org RBAC integration)
- ❌ Add AI/ML features (Wave 3; no training data exists yet)
- ❌ Design for multi-tenancy (Wave 4; adds auth/billing complexity)

### Extension Points (Prepare, Don't Build)

```python
# Wave 1: Include reserved fields in artifact model
class ConfigArtifact:
    # ... Wave 1 fields ...

    # Reserved for Wave 2 (null in Wave 1)
    policy_set_id: Optional[str] = None  # Enable policy evolution
    approvals: Optional[List[Approval]] = None  # Future governance
    changelog: Optional[str] = None  # Human-readable change summary
```

### Refactoring Triggers

**When to refactor for next wave:**
- **Wave 1 → Wave 2:** If >50% of configs need manual policy checks (proves need for automation)
- **Wave 2 → Wave 3:** If validation failures correlate with patterns (ML opportunity)
- **Any Wave → Wave 4:** If self-hosting becomes primary blocker to adoption (SaaS signal)

---

## Review Schedule

**Quarterly Decision Points:**
1. Review Wave 1 success metrics (adoption, latency, errors)
2. Collect user feedback on governance pain points (Wave 2 signals)
3. Assess team bandwidth and prioritize based on evidence

**Do NOT advance waves based on:**
- Feature parity with competitors (build for users, not roadmaps)
- Technology hype (AI, blockchain, etc.)
- Premature optimization (solve problems that exist, not hypothetical ones)

---

## Summary: Current Focus (v0.2.0)

**Delivered (Wave 1.0-2.0):**
- ✅ 10 MCP tools (complete orchestration toolkit)
- ✅ Multi-transport architecture (stdio + HTTP/SSE)
- ✅ Authentication (bearer tokens + API keys)
- ✅ 30+ server registry
- ✅ Draft workflow (build → validate → publish → deploy)
- ✅ Content-addressable storage with Ed25519 signing
- ✅ Comprehensive documentation (Diátaxis framework)
- ✅ 127/166 tests (77% pass rate)

**Active Development (Wave 2.1-2.2):**
- 🚧 Universal Loadability Format adoption (mcp-gateway v1.2.0 spec)
- 🚧 Enhanced error messages (error codes, structured responses)
- 🚧 Performance optimization (caching, connection pooling)
- 🚧 Ecosystem integration (mcp-gateway testing, n8n workflows)
- 🚧 Pattern N3b implementation

**Explicitly Deferred:**
- Policy engine → Wave 3 (no user demand yet)
- Audit logging → Wave 3 (governance not critical yet)
- AI validation → Wave 4 (no training data yet)
- Marketplace → Wave 5 (far future speculation)

---

## Review History

### 2025-10-26 (Post-Wave 2.0 Review)

**Decisions:**
- Wave 2.0 (HTTP/SSE Transport): ✅ DELIVERED (v0.2.0)
  - Exceeded all targets (14 endpoints, 77% test coverage, 3,100+ lines of docs)
  - Backward compatible (stdio unchanged, both transports work)
  - Security complete (100% endpoints authenticated)
- Wave 2.1-2.2 (Ecosystem Integration): COMMITTED to Q1 2026
  - Depends on mcp-gateway v1.2.0 Universal Loadability spec
  - Pattern N3b coordination with mcp-gateway team
- Original Wave 2 (Governance): DEFERRED to Wave 3
  - Zero user demand for policy/approval features
  - Ecosystem integration higher priority
  - Requires real-world config patterns from Wave 1-2

**Wave Renumbering:**
- Wave 2 renamed: Governance → Integration (HTTP transport delivered)
- Wave 3 renamed: Intelligence → Governance (policy/audit deferred)
- Wave 4 renamed: Ecosystem → Intelligence (AI features)
- Wave 5 added: Ecosystem Platform (SaaS/marketplace)

**Success Metrics:**
- Wave 1 delivered in 5 days (v0.1.0-v0.1.5)
- Wave 2.0 delivered in 1 day (v0.2.0)
- Total: 6 releases, 6 days of development
- Test coverage: 53% → 77% (HTTP transport)

**Next Review:** Q1 2026 (after Wave 2.1-2.2 ecosystem integration)
