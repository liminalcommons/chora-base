# Wave 2.x Planning Document

**Status**: Active Development
**Last Updated**: 2025-10-25
**Current Wave**: 2.0 (HTTP/SSE Transport Foundation - IN PROGRESS)

---

## Overview

This document defines Wave 2.x development for mcp-orchestration, focusing on **multi-transport architecture** and **ecosystem integration**. Wave 2.x transforms mcp-orchestration from a local stdio-only tool into an HTTP/SSE-capable orchestration platform, enabling integration with mcp-gateway, n8n workflows, and remote MCP clients.

**Strategic Context:** Wave 1.x delivered complete local orchestration (v0.1.0-0.1.5). Wave 2.x positions mcp-orchestration as an ecosystem enabler through HTTP transport and API-first architecture.

---

## Wave 2.0 (v0.2.0) — HTTP/SSE Transport Foundation

**Status**: Planning → Implementation (Starting 2025-10-25)
**Goal**: Multi-transport architecture (stdio + HTTP/SSE) with authentication
**Estimated Timeline**: 6-8 weeks (Jan-Feb 2026)

### Scope

#### HTTP Transport Server Module

**New Module**: `src/mcp_orchestrator/http/`

**1. FastAPI HTTP Server** (`http/server.py`)
```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MCP Orchestration HTTP API",
    version="0.2.0",
    description="Centralized MCP configuration orchestration"
)

# CORS middleware for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configurable
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTTP endpoints wrapping all 10 MCP tools
@app.get("/v1/clients")
async def http_list_clients(auth=Depends(verify_auth)):
    """HTTP endpoint for list_clients MCP tool."""
    return await list_clients()

# ... (10 endpoints total)
```

**2. Authentication Service** (`http/auth.py`)
```python
from typing import Optional
import secrets
import os

class AuthenticationService:
    """Validates bearer tokens and API keys for HTTP transport."""

    def __init__(self):
        self.api_key = os.getenv("MCP_ORCHESTRATION_API_KEY")
        self._tokens: set[str] = set()  # In-memory token store

    def validate_bearer_token(self, token: str) -> bool:
        """Validate bearer token."""
        return token in self._tokens

    def validate_api_key(self, key: str) -> bool:
        """Validate API key from environment."""
        return key == self.api_key if self.api_key else False

    def generate_token(self) -> str:
        """Generate new API token."""
        token = secrets.token_urlsafe(32)
        self._tokens.add(token)
        return token
```

#### HTTP Endpoints (10 tools → 10 endpoints)

**Endpoint Mapping:**
```
GET  /v1/clients                              → list_clients()
GET  /v1/clients/{client_id}/profiles         → list_profiles(client_id)
GET  /v1/config/{client_id}/{profile}         → get_config(client_id, profile)
POST /v1/config/diff                          → diff_config(...)
POST /v1/config/{client_id}/{profile}/draft/add → add_server_to_config(...)
POST /v1/config/{client_id}/{profile}/draft/remove → remove_server_from_config(...)
GET  /v1/config/{client_id}/{profile}/draft   → view_draft_config(...)
DELETE /v1/config/{client_id}/{profile}/draft → clear_draft_config(...)
POST /v1/config/{client_id}/{profile}/validate → validate_config(...)
POST /v1/config/{client_id}/{profile}/publish → publish_config(...)
POST /v1/config/{client_id}/{profile}/deploy  → deploy_config(...)
GET  /v1/servers                              → list_available_servers()
GET  /v1/servers/{server_id}                  → describe_server(server_id)
POST /v1/keys/initialize                      → initialize_keys()
```

**Authentication:**
- Header: `Authorization: Bearer <token>` (primary method)
- Header: `X-API-Key: <key>` (alternative method)
- Environment variable: `MCP_ORCHESTRATION_API_KEY`

#### CLI Commands (2 new)

```bash
# Start HTTP server
mcp-orchestration-serve-http \
  --host 0.0.0.0 \
  --port 8000 \
  --log-level info

# Generate API token
mcp-orchestration-generate-token
# Outputs: token_abc123xyz...
```

#### Dependencies (New)

```toml
# pyproject.toml additions
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    # ... existing deps
]
```

### Deliverables

- [x] Planning documents (WAVE_2X_PLAN.md, capability spec)
- [ ] HTTP transport server module (`src/mcp_orchestrator/http/`)
- [ ] Authentication service with bearer token + API key support
- [ ] 10 HTTP endpoint wrappers (all MCP tools)
- [ ] 2 CLI commands (`serve-http`, `generate-token`)
- [ ] Unit tests (≥30 tests, ≥85% coverage)
- [ ] Integration tests (stdio + HTTP both work)
- [ ] E2E guides:
  - `user-docs/how-to/deploy-http-server.md`
  - `user-docs/how-to/authenticate-http-api.md`
  - `user-docs/how-to/migrate-stdio-to-http.md`
- [ ] API reference: `user-docs/reference/http-api.md`
- [ ] Docker support (optional)

### Spec Coverage

- ✅ NFR-9: Open, documented HTTP APIs (REST endpoints)
- ✅ NFR-7: Authentication with RBAC (bearer token, API key)
- ⚠️ FR-10 (partial): HTTP transport enables push updates (foundation)
- Foundation for Wave 2.1 API enhancements

### Success Criteria

**Functional:**
- ✅ All 10 MCP tools available via HTTP endpoints
- ✅ Bearer token authentication enforced
- ✅ API key authentication alternative works
- ✅ stdio transport backward compatible (no breaking changes)
- ✅ CORS configured for web clients

**Performance:**
- ✅ p95 < 300ms for HTTP artifact retrieval (NFR-3)
- ✅ Server starts in <5 seconds
- ✅ Handles 100 concurrent requests

**Quality:**
- ✅ 30+ unit tests for HTTP transport
- ✅ 3 E2E value scenarios pass
- ✅ Coverage ≥85% for new HTTP code
- ✅ All quality gates passing

**Documentation:**
- ✅ HTTP API reference complete
- ✅ 3 how-to guides (deploy, auth, migrate)
- ✅ Migration path documented

---

## Wave 2.1 (v0.2.1) — API Enhancements

**Status**: Planned
**Goal**: Enhanced HTTP APIs with Universal Loadability Format integration
**Estimated Timeline**: 2-3 weeks (Late Feb 2026)

### Scope

#### Universal Loadability Format Adoption

**Coordination with mcp-gateway:**
- Review mcp-gateway v1.2.0 Universal Loadability spec (Week 6)
- Align endpoint naming conventions
- Adopt shared error code standards
- Implement structured error responses

**Enhanced Error Responses:**
```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Configuration validation failed",
    "details": {
      "field": "mcpServers.filesystem.command",
      "reason": "Missing required field"
    },
    "timestamp": "2026-02-15T10:30:00Z",
    "request_id": "req_abc123"
  }
}
```

#### API Enhancements

**1. Remote Validation API**
```python
POST /v1/config/validate
Content-Type: application/json

{
  "client_id": "claude-desktop",
  "profile_id": "default",
  "payload": { ... },
  "options": {
    "check_schema": true,
    "check_limits": true,
    "check_security": true
  }
}
```

**2. Batch Operations**
```python
POST /v1/config/batch
[
  {"operation": "validate", "payload": {...}},
  {"operation": "publish", "payload": {...}}
]
```

**3. Webhooks (Optional)**
```python
POST /v1/webhooks/subscribe
{
  "url": "https://n8n.example.com/webhook/mcp",
  "events": ["config.published", "config.deployed"]
}
```

### Deliverables

- [ ] Universal Loadability Format implementation
- [ ] Enhanced error responses with error codes
- [ ] Remote validation API improvements
- [ ] Batch operation support (optional)
- [ ] Webhook support (optional)
- [ ] Updated API reference documentation
- [ ] Integration tests with mcp-gateway (if available)

### Spec Coverage

- ✅ FR-6: Enhanced validation API (remote validation)
- ✅ FR-8: Machine-readable validation reports
- ✅ NFR-9: Structured error responses

### Success Criteria

- ✅ Error responses follow Universal Loadability Format
- ✅ Validation API returns detailed error codes
- ✅ Integration tests pass with mcp-gateway endpoints
- ✅ Documentation updated with new error codes

---

## Wave 2.2 (v0.2.2) — Ecosystem Integration

**Status**: Planned
**Goal**: Integration testing with mcp-gateway and n8n workflows
**Estimated Timeline**: 2-3 weeks (Mar 2026)

### Scope

#### mcp-gateway Integration Testing

**Pattern N3b: n8n as Multi-Server MCP Client**

**Integration Scenarios:**
1. n8n fetches MCP configuration via HTTP
2. n8n validates configuration before deployment
3. n8n deploys configuration to multiple clients
4. n8n monitors configuration drift

**Test Environment:**
```
┌─────────────┐      HTTP      ┌──────────────────┐
│     n8n     │ ────────────> │ mcp-orchestration │
│  (Pattern   │   GET /v1/     │   (HTTP server)   │
│    N3b)     │   config       │                   │
└─────────────┘                └──────────────────┘
       │                                │
       │ Deploy                  Store │
       ↓                                ↓
┌─────────────┐                ┌──────────────────┐
│Claude Desktop│                │Content-Addressable│
│  + Cursor   │                │     Storage      │
└─────────────┘                └──────────────────┘
```

#### Example n8n Workflows

**1. Automated Config Deployment Workflow**
```
Trigger (Cron: Daily)
  → HTTP Request: GET /v1/config/{client}/{profile}
  → Validate Response
  → HTTP Request: POST /v1/config/{client}/{profile}/deploy
  → Notify (Slack/Email)
```

**2. Configuration Validation Workflow**
```
Trigger (Webhook)
  → Parse Config Payload
  → HTTP Request: POST /v1/config/validate
  → If Valid: Publish
  → If Invalid: Notify with errors
```

**3. Drift Detection Workflow**
```
Trigger (Cron: Hourly)
  → HTTP Request: GET /v1/config/{client}/{profile}/latest
  → HTTP Request: GET /v1/config/{client}/{profile}/deployed
  → Compare versions
  → If drift: Alert + Auto-deploy (optional)
```

#### Performance Optimization

**Caching:**
- Redis cache for frequently accessed artifacts
- HTTP ETag support for conditional requests
- Artifact metadata caching

**Connection Pooling:**
- Database connection pooling (if moving to DB storage)
- HTTP client connection pooling

**Metrics & Monitoring:**
- Prometheus metrics export
- OpenTelemetry tracing
- Performance dashboards

### Deliverables

- [ ] Integration test suite with mcp-gateway
- [ ] 3+ example n8n workflows
- [ ] Performance optimization (caching, connection pooling)
- [ ] Metrics & monitoring integration
- [ ] Joint documentation with mcp-gateway team
- [ ] Pattern N3b implementation guide

### Spec Coverage

- ✅ UC-2: Routine Update (via n8n automation)
- ✅ NFR-3: Performance optimization (p95 < 300ms maintained)
- ✅ NFR-11: Metrics, logs, traces export

### Success Criteria

- ✅ n8n can fetch, validate, and deploy configs via HTTP
- ✅ 3+ example n8n workflows functional
- ✅ Performance maintains p95 < 300ms under load
- ✅ Integration tests pass with mcp-gateway
- ✅ Pattern N3b documentation complete

---

## Summary Table

| Wave | Version | Goal | Tools | Resources | CLI Cmds | Weeks | Status |
|------|---------|------|-------|-----------|----------|-------|--------|
| 2.0 | v0.2.0 | HTTP Transport | +0 | +0 | +2 | 6-8 | 🚧 In Progress |
| 2.1 | v0.2.1 | API Enhancements | +0 | +0 | +0 | 2-3 | 📋 Planned |
| 2.2 | v0.2.2 | Ecosystem Integration | +0 | +0 | +0 | 2-3 | 📋 Planned |
| **Total** | **2.0-2.2** | | **10 (same)** | **7 (same)** | **9 (+2)** | **10-14** | |

**Note:** Wave 2.x adds HTTP transport layer but doesn't add new MCP tools (all 10 tools now available via both stdio and HTTP).

---

## Post-Wave 2.x (Wave 3.0+)

**Deferred to Wave 3**:
- **FR-7**: Policy enforcement (requires policy DSL design)
- **FR-10**: Subscription/push updates (HTTP foundation enables SSE)
- **FR-12**: Multi-signer approvals
- **FR-14, FR-15**: Client telemetry aggregation
- **UC-4**: Policy tightening workflows
- RBAC integration
- Approval workflows
- Multi-tenant architecture

**Rationale**: Wave 2.x focuses on HTTP transport and ecosystem integration. Wave 3+ adds governance, intelligence, and enterprise features after validating HTTP API with users.

---

## Implementation Strategy

### Incremental Releases

- Wave 2.0 = minor version bump (v0.2.0)
- Wave 2.1 = patch version bump (v0.2.1)
- Wave 2.2 = patch version bump (v0.2.2)
- Version format: `0.MINOR.PATCH`
- Git tags for each release

### Testing Requirements

- **Each wave**: ≥85% coverage for new code
- **Integration tests**: stdio + HTTP both work
- **E2E tests**: Verify user workflows end-to-end
- **Performance tests**: p95 < 300ms for HTTP endpoints
- **Load testing**: 100 concurrent requests (Wave 2.2)

### Documentation Updates

**Per wave, update**:
- `CHANGELOG.md`: Add version entry with features
- `user-docs/how-to/`: Add HTTP-specific guides
- `user-docs/reference/`: Add HTTP API reference
- `ROADMAP.md`: Mark wave complete
- `project-docs/WAVE_2X_PLAN.md`: Update status
- Git tag: `v0.2.X`

### Release Criteria

**Before releasing a wave**:
- [ ] All tests passing (CI green)
- [ ] Coverage ≥85%
- [ ] E2E guides complete and tested
- [ ] Performance tests pass (p95 < 300ms)
- [ ] API reference documentation complete
- [ ] CHANGELOG.md updated
- [ ] Git tag created
- [ ] PyPI package published

---

## Benefits of Wave 2.x

1. **Ecosystem Integration**: HTTP transport enables mcp-gateway, n8n, CI/CD integration
2. **Remote Orchestration**: Not limited to local stdio connections
3. **API-First Architecture**: All tools available via REST API
4. **Multi-Client at Scale**: n8n can orchestrate configs for many clients
5. **Foundation for Future**: Wave 3+ governance features build on HTTP APIs
6. **Pattern N3b Validation**: Proves mcp-orchestration as ecosystem platform
7. **Strategic Positioning**: Early mover in MCP orchestration space

---

## Coordination with mcp-gateway

### Timeline Alignment

| Period | mcp-orchestration | mcp-gateway | Coordination |
|--------|-------------------|-------------|--------------|
| **Week 6 (Early Q1)** | Wave 2.0 planning | v1.2.0 release (Universal Loadability) | Review spec |
| **Weeks 7-12 (Jan-Feb)** | Wave 2.0 implementation | v1.3.0 (HTTP Streamable) | Endpoint alignment |
| **Late Feb - Early Mar** | Wave 2.1 (API enhancements) | Integration testing | Joint testing |
| **Mar 2026** | Wave 2.2 (Ecosystem integration) | Pattern N3b examples | Joint documentation |
| **Q2 2026** | Production monitoring | v2.1.0 (Pattern N3b) | Launch coordination |

### Key Dependencies

**From mcp-gateway:**
- ⏳ v1.2.0 (Week 6): Universal Loadability Format spec
- ⏳ v1.3.0 (Weeks 7-9): HTTP Streamable transport
- ⏳ v2.1.0 (Q2 2026): Pattern N3b implementation

**From mcp-orchestration:**
- ✅ v0.1.5 (Complete): Full local workflow (foundation)
- 🚧 v0.2.0 (Wave 2.0): HTTP transport
- 📋 v0.2.1 (Wave 2.1): API enhancements
- 📋 v0.2.2 (Wave 2.2): Ecosystem integration

### Collaboration Activities

**Active:**
- 📋 GitHub Discussions (async-first)
- 📋 Quarterly sync calls (optional)
- 📋 Joint documentation efforts

**Deliverables:**
- ✅ Integration response sent
- ✅ Coordination tracker created
- ✅ Wave 2.x plan aligned with mcp-gateway roadmap
- 🟡 Awaiting Universal Loadability spec (Week 6)

---

## Wave Status Tracker

| Wave | Version | Status | Started | Completed | Notes |
|------|---------|--------|---------|-----------|-------|
| 2.0 | v0.2.0 | 🚧 In Progress | 2025-10-25 | - | HTTP/SSE transport foundation |
| 2.1 | v0.2.1 | 📋 Planned | - | - | API enhancements + Universal Loadability |
| 2.2 | v0.2.2 | 📋 Planned | - | - | Ecosystem integration testing |

**Legend**:
- ✅ Done
- 🚧 In Progress
- 📋 Planned
- ⏸️ Paused
- ❌ Cancelled

---

## Next Steps

1. ✅ Create `project-docs/WAVE_2X_PLAN.md` (this document)
2. 🚧 Technical spike: FastAPI + FastMCP integration (Day 2)
3. 📋 Create `project-docs/capabilities/http-transport.md`
4. 📋 Write BDD scenarios: `behaviors/mcp-http-transport.feature`
5. 📋 Implement Wave 2.0 (Phases 1-8)
6. 📋 Release v0.2.0 (Feb 2026)
7. 📋 Implement Wave 2.1-2.2 (Mar 2026)
8. 📋 Pattern N3b launch coordination (Q2 2026)

---

**Document Version**: 1.0
**Last Updated**: 2025-10-25
**Template**: Based on WAVE_1X_PLAN.md structure
**Built with**: [chora-base v3.3.0](https://github.com/liminalcommons/chora-base)
