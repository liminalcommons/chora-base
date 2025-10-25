---
title: MCP-n8n Strategic Roadmap (Unified)
type: strategic-plan
date: 2025-10-24
status: active
version: 3.0.0
supersedes: [ROADMAP.md, ROADMAP-V2.md]
---

# MCP-n8n Strategic Roadmap

**Vision:** Transform mcp-n8n from prototype to production-grade universal MCP gateway with comprehensive documentation pipeline, multi-backend aggregation, and ecosystem integration.

**Current Status:** v1.0.0 released (Oct 2025) - Production deployment ready
**Next Milestone:** v2.0.0 (MCP Gateway) - Q1 2026

---

## Executive Summary

This unified roadmap consolidates three strategic plans:
1. **ROADMAP.md** - Original sprint-based development (v0.1-v0.5)
2. **ROADMAP-V2.md** - MCP Gateway evolution research (v2.0 vision)
3. **RELEASE_PHASES_OVERVIEW.md** - Documentation pipeline phases (v1.0)

**Key Insight:** v1.0.0 delivered **production infrastructure** (docs, deployment, monitoring) but deferred **core gateway functionality fixes** (Pattern P5). The v1.x series will layer gateway capabilities onto the v1.0.0 foundation, culminating in v2.0.0 rename to `mcp-gateway`.

---

## Strategic Timeline

```
┌─────────────────────────────────────────────────────────────────┐
│ Phase 1: Foundation (v0.1-v0.5, Completed 2025-10)             │
├─────────────────────────────────────────────────────────────────┤
│ ✅ Sprints 1-5: Gateway routing, memory, workflows             │
│ ✅ Pattern N2 validated                                         │
│ ✅ Agent memory system                                          │
└─────────────────────────────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────────────────────┐
│ Phase 2: Production Infrastructure (v1.0, Completed 2025-10)   │
├─────────────────────────────────────────────────────────────────┤
│ ✅ Documentation pipeline (living docs)                         │
│ ✅ CI/CD with E2E testing                                       │
│ ✅ Docker + Kubernetes deployment                               │
│ ✅ Monitoring (Prometheus + Grafana)                            │
│ ✅ Security (auth, TLS, rate limiting)                          │
│ ✅ Performance (caching, load testing)                          │
└─────────────────────────────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────────────────────┐
│ Phase 3: Gateway Evolution (v1.1-v1.5, 2025-11 to 2026-01)    │
├─────────────────────────────────────────────────────────────────┤
│ 🚧 v1.0.1: Quality fixes (pre-commit, mypy, ruff)              │
│ 📋 v1.1.0: Pattern P5 fixes (6 root causes)                    │
│ 📋 v1.2.0: Universal Loadability Format                        │
│ 📋 v1.3.0: HTTP Streamable transport                           │
│ 📋 v1.4.0: chora-base template                                 │
│ 📋 v1.5.0: Advanced workflow capabilities                      │
└─────────────────────────────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────────────────────┐
│ Phase 4: MCP Gateway Launch (v2.0, 2026-02)                    │
├─────────────────────────────────────────────────────────────────┤
│ 📋 Repository migration (mcp-n8n → mcp-gateway)                │
│ 📋 Extract mcp-server-n8n package                              │
│ 📋 PyPI redirect (mcp-n8n → mcp-gateway)                       │
│ 📋 Community communication campaign                            │
└─────────────────────────────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────────────────────┐
│ Phase 5: Ecosystem & Scale (v2.1+, 2026-03+)                   │
├─────────────────────────────────────────────────────────────────┤
│ 📋 n8n integration (Patterns N3, N5)                           │
│ 📋 Claude Desktop marketplace listing                          │
│ 📋 VS Code extension                                           │
│ 📋 Multi-region deployment                                     │
│ 📋 Enterprise features (multi-tenancy, SSO)                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Version Strategy

### v1.x Series: mcp-n8n (Gateway Enhancement)
**Goal:** Layer gateway evolution onto v1.0.0 infrastructure without breaking existing deployments.

**Versioning Philosophy:**
- **v1.0.x** - Patches (bug fixes only)
- **v1.1-v1.5** - Minor releases (new features, backward compatible)
- **v2.0** - Major release (breaking changes, rename)

### v2.x Series: mcp-gateway (Universal Gateway)
**Goal:** Production-grade universal MCP gateway with ecosystem integration.

**Key Transition:**
- **v2.0.0** marks rename from `mcp-n8n` to `mcp-gateway`
- PyPI redirect package: `mcp-n8n` → `mcp-gateway`
- Separate package: `mcp-server-n8n` (n8n backend extracted)

---

## Integration Pattern Status

| Pattern | Status | Version | Description | Priority |
|---------|--------|---------|-------------|----------|
| **P5** | ✅ Implemented (bugs) | v0.2.0 | FastMCP Gateway & Aggregator | **High** - Fixes in v1.1.0 |
| **N2** | ✅ Production Ready | v1.0.0 | Standalone n8n MCP Server | **Complete** |
| **N3** | 📋 Planned | v2.1+ | n8n as MCP Client (custom node) | **Low** |
| **N3b** | 🔬 Design Phase | v2.1+ | n8n as Multi-Server MCP Client | **Medium** - Ecosystem coordination |
| **N4** | ❌ Rejected | N/A | n8n as MCP Gateway | **Not viable** (45% feasibility) |
| **N5** | ⚠️ Partial | v0.5.0 | Artifact Assembly Pipelines | **Medium** - v1.5.0 |

**Key Research Findings (2025-10-23/24):**
- **Pattern P5:** 6 root causes identified affecting multi-backend tool exposure (to be fixed in v1.1.0)
- **Pattern N4:** Comprehensive feasibility analysis shows 45% feasibility - NOT recommended for production
- **Pattern N2:** Successfully implemented in Sprint 7A - production-ready standalone server
- **Pattern N3b:** NEW - Enables n8n workflows to consume from BOTH mcp-gateway AND mcp-orchestration simultaneously
- **Universal Loadability Format:** Specified for v1.2.0 to enable cross-gateway compatibility

**Ecosystem Integration (Pattern N3b):**
- Requires mcp-gateway v1.3.0+ (HTTP transport) and mcp-orchestration Wave 2.0+ (HTTP transport)
- Custom n8n node: `@chora/mcp-client` (generic MCP client)
- Enables dynamic server discovery (orchestration) + multi-backend execution (gateway) in single workflows
- Timeline: Q2 2026 (~5-6 months from now)
- See: [Ecosystem Integration Briefing](../docs/ecosystem/integration-briefing-for-mcp-orchestration.md)

**References:**
- [Integration Patterns Explanation](../docs/explanation/integration-patterns.md)
- [Pattern N4 Feasibility Analysis](../docs/explanation/pattern-n4-feasibility-analysis.md)
- [MCP-Gateway Evolution Research](../dev-docs/research/MCP-n8n to MCP-Gateway Evolution.md)
- [Ecosystem Integration Briefing](../docs/ecosystem/integration-briefing-for-mcp-orchestration.md)

---

## Detailed Roadmap

### ✅ Completed: Foundation Phase (v0.1-v0.5)

**Sprint 1: Validation & Foundation (v0.1-v0.2)**
- Gateway architecture (Pattern P5)
- Backend registry with namespace routing
- Chora Composer integration
- Coda MCP integration
- Date: Completed 2025-09

**Sprint 2: Chora Foundation (v0.2)**
- Event emission system
- Trace context propagation
- Generator dependency metadata
- Date: Completed 2025-09

**Sprint 3: Event Monitoring (v0.3)**
- EventWatcher class
- `get_events` MCP tool
- Webhook forwarding to n8n
- Date: Completed 2025-09

**Sprint 4: Agent Memory (v0.4, Phase 4.5-4.6)**
- LLM-intelligent developer experience (AGENTS.md)
- Event log storage and querying
- Knowledge graph (Zettelkasten)
- Agent profiles
- `chora-memory` CLI tool
- Date: Completed 2025-10

**Sprint 5: Production Workflows (v0.5)**
- Daily Report workflow
- EventWorkflowRouter (event-driven automation)
- YAML event mapping with hot-reload
- Date: Completed 2025-10

### ✅ Completed: Infrastructure Phase (v1.0)

**Phase 1: Documentation Pipeline**
- E2E test extraction from How-Tos
- DDD intent generation
- BDD scenario generation
- Research ingestion automation
- Documentation coverage validation
- Bidirectional traceability
- Date: Completed 2025-10-23

**Phase 2: Pattern Validation & CI**
- Pattern N2 validated (standalone n8n MCP server)
- Claude Desktop quick start validated
- GitHub Actions E2E testing
- Coverage metrics (66% E2E coverage)
- How-To authoring guide
- Date: Completed 2025-10-24

**Phase 3: Production Readiness**
- Optimized Docker image (<150MB target)
- Complete K8s manifests (HPA 3-10 replicas)
- Prometheus monitoring (15+ metrics, 20+ alerts)
- Security hardening (Bearer auth, TLS, rate limiting)
- Redis caching + connection pooling
- Locust load testing
- Date: Completed 2025-10-24

**Release:** v1.0.0 (2025-10-24)
- 3/4 phases complete (75%)
- 23/23 goals achieved
- 91 files, 22,260 insertions
- Production-ready deployment

### 🚧 In Progress: Gateway Evolution Phase (v1.1-v1.5)

#### Sprint 15: v1.0.1 Patch (Week 1)
**Status:** Planned
**Duration:** 1-2 days
**Priority:** High (blocks v1.1.0)

**Deliverables:**
- Fix K8s YAML multi-document format issues
- Fix mypy type errors (51 errors in Phase 3 modules)
- Fix ruff linting errors (line length violations)
- Fix pre-commit hook failures
- Add type stubs (`types-redis`, `types-httpx`)

**Success Criteria:**
- ✅ All pre-commit hooks pass
- ✅ mypy type checking passes (0 errors)
- ✅ ruff linting passes
- ✅ All tests still pass

**Intent Document:** `project/sprints/sprint-15-v1.0.1-patch-intent.md`

---

#### Sprint 16: v1.1.0 Pattern P5 Fixes (Weeks 2-4)
**Status:** Planned
**Duration:** 2-3 weeks
**Priority:** Critical (core gateway functionality)
**Source:** `dev-docs/research/MCP-n8n to MCP-Gateway Evolution.md`

**Problem:** Backend tools fail to expose through FastMCP gateway (6 root causes)

**Deliverables:**

1. **Fix Silent Tool Loading Failures (Cause 1)**
   - Add `MCP_RAISE_LOAD_ERRORS` environment variable
   - Fail-fast mode (development) vs. degrade gracefully (production)
   - Enhanced error logging

2. **Fix Async Context Manager Failures (Cause 2)**
   - Immediate session validation in `__aenter__()`
   - Proper cleanup on connection failures
   - ConnectionError on session failures

3. **Implement Eager Validation (Cause 3)**
   - `create_validated_proxy()` helper function
   - Force tool discovery at gateway startup
   - Validate backends before mounting

4. **Fix Tool Prefix Double-Underscore Bug (Cause 4)**
   - Normalize prefixes (strip trailing `_`)
   - Clean tool names: `weather_get_forecast` not `weather__get_forecast`

5. **Fix Mount Path Propagation (Cause 5)**
   - `MountPathMiddleware` for FastAPI nesting
   - Correct path context for MCP endpoints

6. **Enhanced Error Context (Cause 6)**
   - `BackendToolError` exception class
   - Include backend, tool, request_id in errors

**Testing:**
- Multi-backend integration tests (3-5 backends)
- Tool aggregation tests (100+ tools)
- Failure mode tests
- Load testing (100 concurrent requests, <1s p95)

**Success Criteria:**
- ✅ 0% tool loading failures
- ✅ Gateway aggregates 10+ backends successfully
- ✅ All tool names normalized (no double underscores)
- ✅ Multi-backend tests passing

**Intent Document:** `project/sprints/sprint-16-v1.1.0-pattern-p5-fixes-intent.md`

---

#### Sprint 17: v1.2.0 Universal Loadability (Weeks 5-6)
**Status:** Planned
**Duration:** 2 weeks
**Source:** `ROADMAP-V2.md` Section 2

**Goal:** Universal MCP server discovery format for cross-gateway compatibility

**Deliverables:**

1. **MCP Server Loadability Specification v1.0**
   - JSON schema for `mcp-server.json`
   - Endpoint definitions (stdio, http)
   - Capability advertisement
   - Authentication requirements
   - Discovery tags and categories

2. **Example Specification:**
   ```json
   {
     "mcpVersion": "2025-03-26",
     "server": {
       "name": "weather-service",
       "version": "1.2.0",
       "description": "Real-time weather data"
     },
     "endpoints": {
       "http": {
         "url": "https://api.weather.com/mcp",
         "method": "POST"
       }
     },
     "capabilities": {
       "tools": {"supported": true, "count": 5}
     },
     "discovery": {
       "tags": ["weather", "forecast", "public"]
     }
   }
   ```

3. **Gateway Auto-Discovery**
   - `discover_and_register()` function
   - Fetch `mcp-server.json` from URL
   - Parse and validate schema
   - Auto-mount backend with tags

4. **Generator Utilities**
   - `generate_loadability_file()` CLI command
   - Auto-detection of capabilities
   - Template-based generation

**Compatibility Targets:**
- MCP Gateway (this project)
- Claude Desktop configuration
- n8n MCP Server Trigger
- VS Code MCP extensions

**Success Criteria:**
- ✅ Loadability JSON schema validated
- ✅ Auto-discovery working for HTTP backends
- ✅ Generator CLI functional
- ✅ mcp_server_n8n.py updated to use format

---

#### Sprint 18: v1.3.0 HTTP Streamable Transport (Weeks 7-9)
**Status:** Planned
**Duration:** 3 weeks
**Source:** `ROADMAP-V2.md` Section 1 (Decision 1)

**Goal:** Replace STDIO transport with HTTP Streamable for multi-tenant support

**Background:**
- SSE transport deprecated in MCP spec (post-2024-11-05)
- HTTP Streamable provides bidirectional communication
- Better session management and scaling
- DNS rebinding protection

**Deliverables:**

1. **Transport Layer Migration**
   ```python
   from fastmcp import FastMCP

   gateway = FastMCP("MCP Gateway")
   gateway.run(
       transport="http",  # Was: "stdio"
       host="0.0.0.0",
       port=8000,
       path="/mcp"
   )
   ```

2. **Multi-Tenant Support**
   - Per-tenant backend configurations
   - Tenant isolation
   - Authentication per tenant

3. **Updated Deployment Configs**
   - K8s manifests for HTTP transport
   - Docker Compose with HTTP endpoints
   - nginx reverse proxy configuration
   - Health check updates

4. **Migration Guide**
   - STDIO → HTTP Streamable upgrade path
   - Configuration changes required
   - Backward compatibility notes

**Success Criteria:**
- ✅ HTTP Streamable transport working
- ✅ Multi-tenant isolation functional
- ✅ All deployment configs updated
- ✅ Migration guide complete

---

#### Sprint 19: v1.4.0 chora-base Template (Weeks 10-12)
**Status:** Planned
**Duration:** 2-3 weeks
**Source:** `ROADMAP-V2.md` Section 5

**Goal:** Production-ready MCP server template reducing boilerplate by 70%

**Design Goals:**
1. Minimize boilerplate: ~200 lines → ~30 lines
2. Transport flexibility: stdio + HTTP out-of-box
3. Configuration management: YAML/JSON with env vars
4. Testing utilities: Built-in test client
5. Deployment ready: Docker + K8s templates
6. Gateway compatible: Universal Loadability Format

**API Example:**

**Before (Raw SDK) - ~200 lines:**
```python
from fastmcp import FastMCP
import logging

logging.basicConfig(level=logging.INFO)
mcp = FastMCP("my-server")

@mcp.tool()
async def execute_query(query: str, params: dict = {}) -> dict:
    try:
        result = await db.query(query, params)
        return {"content": [{"type": "text", "text": json.dumps(result)}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error: {e}"}], "isError": True}

if __name__ == "__main__":
    async def main():
        async with stdio_server() as (read, write):
            await mcp.run(read, write, mcp.create_initialization_options())
    asyncio.run(main())
```

**After (chora-base) - ~30 lines:**
```python
from chora_base import ChoraServer, tool

server = ChoraServer(config_file="config/development.yaml")

@tool(name="execute_query", description="Execute database query")
async def execute_query(query: str, params: dict = {}) -> dict:
    result = await db.query(query, params)
    return {"rows": result.rows, "count": result.rowcount}

if __name__ == "__main__":
    server.run()  # Auto-selects transport from config
```

**Key Features:**
- Declarative tool registration with `@tool()` decorator
- Built-in authentication (`@requires_auth(roles=["admin"])`)
- Automatic error handling (`ToolError` exceptions)
- Testing utilities (`TestClient` for pytest)
- Loadability generation (`server.generate_loadability()`)

**Success Criteria:**
- ✅ 70% boilerplate reduction achieved
- ✅ All transport types supported (stdio, http)
- ✅ Built-in auth working
- ✅ Testing utilities functional
- ✅ Docker + K8s templates included

---

#### Sprint 20: v1.5.0 Advanced Workflows (Weeks 13-15)
**Status:** Planned
**Duration:** 2-3 weeks
**Source:** Original ROADMAP.md Sprint 6

**Goal:** Template-based workflow library and enhanced execution capabilities

**Deliverables:**

1. **Template-based Workflow Library**
   - Pre-built workflow templates (daily reports, error summaries, etc.)
   - Template parameter injection
   - Workflow catalog

2. **Workflow Versioning**
   - Semantic versioning for workflows
   - Rollback capabilities
   - Change tracking

3. **Enhanced Error Handling**
   - Retry logic with exponential backoff
   - Circuit breakers
   - Graceful degradation

4. **Parallel Execution**
   - Concurrent workflow steps
   - Dependency resolution
   - Result aggregation

5. **Workflow Composition**
   - Workflows calling other workflows
   - Nested execution context
   - Result passing

**Success Criteria:**
- ✅ 5+ workflow templates in library
- ✅ Versioning system working
- ✅ Retry + circuit breaker functional
- ✅ Parallel execution tested

---

### 📋 Planned: Gateway Launch Phase (v2.0)

#### Sprint 21: v2.0.0 Repository Migration (Weeks 16-17)
**Status:** Planned
**Duration:** 1-2 weeks
**Source:** `ROADMAP-V2.md` Section 6
**Type:** BREAKING CHANGE

**Goal:** Complete transition to `mcp-gateway` identity

**Deliverables:**

1. **Extract mcp-server-n8n Repository**
   ```bash
   # Using git filter-repo (20s vs 12min with filter-branch)
   git clone https://github.com/liminalcommons/mcp-n8n.git mcp-server-n8n
   cd mcp-server-n8n
   git filter-repo --path src/mcp_n8n/backends/n8n_backend.py --path mcp_server_n8n.py
   git remote add origin git@github.com:liminalcommons/mcp-server-n8n.git
   git push -u origin --all
   ```

2. **Rename Main Repository**
   ```bash
   cd mcp-n8n
   git checkout -b rename-to-gateway

   # Update package name
   sed -i 's/name = "mcp-n8n"/name = "mcp-gateway"/' pyproject.toml
   sed -i 's/version = "1.5.0"/version = "2.0.0"/' pyproject.toml

   # Update imports
   find src -type f -name "*.py" -exec sed -i 's/from mcp_n8n/from mcp_gateway/g' {} \;
   mv src/mcp_n8n src/mcp_gateway

   git commit -m "feat!: rename package to mcp-gateway

   BREAKING CHANGE: Package renamed from mcp-n8n to mcp-gateway"
   ```

3. **PyPI Package Migration**
   - Publish `mcp-gateway@2.0.0` to PyPI
   - Create `mcp-n8n@2.0.0` redirect stub (depends on `mcp-gateway`)
   - Publish `mcp-server-n8n@1.0.0` standalone package

4. **Migration Guide**
   ```bash
   # For users
   pip uninstall mcp-n8n
   pip install mcp-gateway

   # Update imports
   # OLD: from mcp_n8n import Server
   # NEW: from mcp_gateway import Server
   ```

5. **Communication Campaign**
   - GitHub announcement
   - PyPI metadata updates
   - Social media campaign
   - Email known users

**Breaking Changes:**
- Package name: `mcp-n8n` → `mcp-gateway`
- Import path: `mcp_n8n` → `mcp_gateway`
- n8n backend: Now separate package `mcp-server-n8n`

**Migration Timeline:**
- Week 1-2: Both packages available
- Week 3-4: `mcp-n8n` is redirect only
- Month 2+: All users on `mcp-gateway`

**Success Criteria:**
- ✅ `mcp-gateway@2.0.0` published to PyPI
- ✅ `mcp-server-n8n@1.0.0` published to PyPI
- ✅ `mcp-n8n` redirect working
- ✅ Migration guide complete
- ✅ 80% of users migrated within Month 1

---

### 📋 Future: Ecosystem Phase (v2.1+)

#### Sprint 22: n8n Integration Patterns (v2.1)
**Source:** Original ROADMAP.md Sprint 7 + Pattern N3b Ecosystem Integration
**Duration:** 4-6 weeks
**Ecosystem Coordination:** Requires mcp-orchestration Wave 2.0+ (HTTP transport)

**Goals:**

1. **Pattern N3: n8n as MCP Client (Single-Server)**
   - Custom n8n node `@chora/mcp-client` (generic MCP client)
   - Call MCP tools from n8n workflows
   - Visual workflow builder integration

2. **Pattern N3b: n8n as Multi-Server MCP Client** 🌟 NEW
   - Same `@chora/mcp-client` node connects to multiple MCP servers
   - Dual integration: mcp-gateway + mcp-orchestration
   - Dynamic server discovery via orchestration
   - Multi-backend tool execution via gateway
   - Complete automation: discover → configure → execute

3. **Pattern N5: Artifact Assembly Pipelines**
   - Visual workflow orchestration
   - Multi-source data aggregation
   - Scheduled report generation

**Pattern N3b Deliverables:**
- Generic `@chora/mcp-client` n8n node (works with any HTTP-based MCP server)
- Example workflows:
  - "Onboard Engineer MCP Environment" (dynamic server config)
  - "Environment-Specific MCP Configuration" (dev/staging/prod)
  - "MCP Server Health Monitor" (automated failover)
- Integration briefing for mcp-orchestration team
- Cross-project testing with mcp-orchestration

**Dependencies:**
- ✅ mcp-gateway v1.3.0 (HTTP transport) - from Sprint 18
- ⏳ mcp-orchestration Wave 2.0 (HTTP transport) - external dependency
- ✅ Universal Loadability Format (v1.2.0) - from Sprint 17

**Success Criteria:**
- ✅ Generic `@chora/mcp-client` node published to npm
- ✅ Single workflow can consume from both mcp-gateway AND mcp-orchestration
- ✅ 3+ example workflows demonstrating Pattern N3b
- ✅ Integration validated with mcp-orchestration team
- ✅ Documentation complete

**References:**
- [Pattern N3b Specification](../docs/explanation/integration-patterns.md#pattern-n3b)
- [Ecosystem Integration Briefing](../docs/ecosystem/integration-briefing-for-mcp-orchestration.md)

---

#### Sprint 23: Ecosystem Integrations (v2.2)
**Source:** RELEASE_PHASES_OVERVIEW.md Phase 4
**Duration:** 3-4 weeks

**Goals:**

1. **Claude Desktop Marketplace**
   - Submit listing
   - Installation instructions
   - Usage examples

2. **VS Code Extension**
   - MCP tool visualization
   - How-To guide executor
   - Documentation validator

3. **Community Infrastructure**
   - Contribution guides
   - Issue templates
   - Community support channels

**Success Criteria:**
- ✅ Listed in Claude Desktop marketplace
- ✅ VS Code extension published
- ✅ 10+ external contributors

---

#### Sprint 24: Multi-Region & Enterprise (v2.3+)
**Source:** RELEASE_PHASES_OVERVIEW.md Phase 4
**Duration:** Ongoing

**Goals:**

1. **Multi-Region Deployment**
   - Deploy to multiple cloud regions
   - Geographic routing
   - Latency optimization (<200ms global)

2. **Enterprise Features**
   - Multi-tenancy support
   - SSO authentication (SAML, OAuth)
   - Audit logging
   - Compliance features (SOC2, GDPR)
   - SLA monitoring

**Success Criteria:**
- ✅ Multi-region deployment operational
- ✅ Enterprise features documented
- ✅ 3+ enterprise customers

---

## Success Metrics

### Phase 1 (v0.1-v0.5) ✅ ACHIEVED
- ✅ Gateway routing functional
- ✅ Memory system operational
- ✅ Workflows executing
- ✅ 49 unit tests passing

### Phase 2 (v1.0) ✅ ACHIEVED
**Documentation Pipeline:**
- ✅ 5 automation scripts (125% of target)
- ✅ 9 auto-generated docs (180% of target)
- ✅ 100% pipeline coverage

**Pattern Validation:**
- ✅ 2 high-quality patterns validated
- ✅ 66% E2E coverage (exceeds 60% target)

**Production Readiness:**
- ✅ Docker image optimized
- ✅ 15+ Prometheus metrics
- ✅ Security hardening complete
- ✅ Load testing operational

### Phase 3 (v1.1-v1.5) 📋 PLANNED
**Gateway Evolution:**
- 🎯 0% tool loading failures (from ~100%)
- 🎯 Gateway aggregates 10+ backends
- 🎯 100+ tools from multiple backends
- 🎯 <1s p95 latency under load

**Universal Loadability:**
- 🎯 JSON schema validated
- 🎯 Auto-discovery working
- 🎯 Compatible with Claude Desktop, n8n, VS Code

**HTTP Streamable:**
- 🎯 Transport migration complete
- 🎯 Multi-tenant support functional
- 🎯 All deployments updated

**chora-base Template:**
- 🎯 70% boilerplate reduction
- 🎯 Production-ready templates
- 🎯 10+ community adoptions

### Phase 4 (v2.0) 📋 PLANNED
**Repository Migration:**
- 🎯 `mcp-gateway` published to PyPI
- 🎯 `mcp-server-n8n` extracted successfully
- 🎯 80% user migration within Month 1

### Phase 5 (v2.1+) 📋 FUTURE
**Ecosystem:**
- 🎯 10+ production deployments
- 🎯 50+ community-created MCP servers
- 🎯 Listed in major marketplaces

**Enterprise:**
- 🎯 Multi-region operational
- 🎯 3+ enterprise customers
- 🎯 <200ms global p95 latency

---

## Risk Management

### Technical Risks

**Risk:** Pattern P5 fixes require FastMCP API changes
- **Probability:** High
- **Impact:** High
- **Mitigation:** Fork FastMCP temporarily, upstream patches, maintain compatibility layer

**Risk:** HTTP Streamable migration breaks existing deployments
- **Probability:** Medium
- **Impact:** High
- **Mitigation:** Phased rollout, maintain STDIO compatibility in v1.x, clear migration guide

**Risk:** Repository rename causes user confusion
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** PyPI redirect package, comprehensive migration guide, extended support period

### Adoption Risks

**Risk:** Low community adoption of Universal Loadability
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** Partner with FastMCP/Claude Desktop teams, provide tooling, showcase benefits

**Risk:** Enterprise customers don't upgrade from v1.0
- **Probability:** Low
- **Impact:** Low
- **Mitigation:** v1.0.x LTS support, phased deprecation, enterprise migration assistance

---

## Dependencies & Constraints

### External Dependencies
- **FastMCP SDK** - Core gateway functionality (may require fork)
- **chora-compose** - Template rendering (v1.5.0+)
- **n8n** - Workflow integration (v1.0+)
- **Kubernetes** - Production deployment (v1.28+)

### Internal Constraints
- **Team Size:** 1-2 developers (AI-assisted)
- **Timeline:** 4-5 months to v2.0.0
- **Budget:** Open source (no funding constraints)

### Quality Gates
- ≥95% test coverage for new code
- Zero critical security issues (Snyk scan)
- All pre-commit hooks passing
- Performance benchmarks met

---

## Communication Plan

### Stakeholder Updates

**Weekly (Internal):**
- Sprint progress review
- Blocker identification
- Metric tracking

**Monthly (Public):**
- Release notes
- Blog posts
- Community updates

**Quarterly (Strategic):**
- Roadmap reviews
- Success metric analysis
- Strategic pivots if needed

### Key Milestones Announcements

**v1.0.1 (Week 1):**
- GitHub release notes
- Bug fix highlights

**v1.1.0 (Month 1):**
- Blog post: "Pattern P5 Fixes - Gateway Evolution Begins"
- Technical deep-dive article

**v1.3.0 (Month 2):**
- Blog post: "HTTP Streamable Transport - Multi-Tenant Ready"
- Migration guide promotion

**v2.0.0 (Month 4):**
- Major announcement: "mcp-n8n becomes mcp-gateway"
- Migration campaign
- Community celebration

---

## Related Documents

### Strategic Planning
- `project/RELEASE_PHASES_OVERVIEW.md` - Original v1.0 release plan
- `dev-docs/research/MCP-n8n to MCP-Gateway Evolution.md` - Gateway evolution research

### Sprint Intents
- `project/sprints/sprint-15-v1.0.1-patch-intent.md` - v1.0.1 quality fixes
- `project/sprints/sprint-16-v1.1.0-pattern-p5-fixes-intent.md` - v1.1.0 gateway fixes
- `project/sprints/sprint-10-3-pattern-p5-fix-implementation-plan.md` - Original P5 research

### Architecture
- `dev-docs/ARCHITECTURE.md` - System architecture
- `docs/reference/specs/2-mcp-server-loadability-specification.md` - Loadability spec
- `docs/reference/specs/5-chora-base-mcp-server-template-specification.md` - Template spec

### Historical Roadmaps (Superseded)
- `project/ROADMAP.md` - Original sprint-based roadmap (v0.1-v0.8)
- `project/ROADMAP-V2.md` - Gateway evolution research roadmap

---

## Conclusion

This unified strategic roadmap consolidates three previous planning documents into a coherent v1.0 → v2.0 evolution path. The v1.x series will incrementally add gateway capabilities (Pattern P5 fixes, Universal Loadability, HTTP transport, templates) to the v1.0.0 infrastructure foundation. v2.0.0 will mark the official transition to `mcp-gateway` with full ecosystem integration.

**Key Insight:** v1.0.0 delivered production infrastructure but deferred core gateway fixes. This was the right call - we now have comprehensive monitoring, deployment, and testing infrastructure to support the gateway evolution in v1.1-v1.5.

**Next Actions:**
1. Complete Sprint 15 (v1.0.1 quality fixes)
2. Begin Sprint 16 (v1.1.0 Pattern P5 fixes)
3. Retire ROADMAP.md and ROADMAP-V2.md in favor of this unified plan

---

**Created:** 2025-10-24
**Status:** Active
**Version:** 3.0.0 (unified)
**Last Updated:** 2025-10-24
**Maintained By:** mcp-n8n core team
**Next Review:** 2025-11-24 (monthly)
