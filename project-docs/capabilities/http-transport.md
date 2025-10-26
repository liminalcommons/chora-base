# Capability: HTTP/SSE Transport for MCP Tools

**Version:** 1.0
**Status:** @status:planned
**Wave:** 2.0
**Owner:** mcp-orchestration
**Last Updated:** 2025-10-26

---

## Overview

This capability adds **HTTP/SSE transport** to mcp-orchestration, enabling all 10 MCP tools to be accessed via RESTful HTTP API in addition to the existing stdio transport. This transforms mcp-orchestration from a local-only tool into a remotely accessible orchestration platform.

**Strategic Value:**
- Enables mcp-gateway integration (Pattern N3b)
- Enables n8n workflow automation
- Enables web application integration
- Foundation for Wave 3 enterprise features (RBAC, multi-tenancy)
- Positions mcp-orchestration as ecosystem platform

---

## Domain Model

### Entities

#### 1. HTTPTransportServer
**Description:** FastAPI application that exposes all MCP tools as HTTP endpoints.

**Attributes:**
- `app: FastAPI` - The FastAPI application instance
- `host: str` - Server bind address (default: "0.0.0.0")
- `port: int` - Server port (default: 8000)
- `auth_service: AuthenticationService` - Authentication provider
- `running: bool` - Server running state

**Behaviors:**
- @behavior:http-transport-expose - Exposes all 10 MCP tools via HTTP endpoints
- @behavior:http-transport-lifecycle - Starts/stops HTTP server
- @behavior:http-transport-backward-compat - stdio transport continues to work

#### 2. AuthenticationService
**Description:** Validates bearer tokens and API keys for HTTP requests.

**Attributes:**
- `api_key: str | None` - API key from environment (MCP_ORCHESTRATION_API_KEY)
- `_tokens: set[str]` - In-memory token store
- `_token_metadata: dict[str, TokenMetadata]` - Token creation time, expiry

**Behaviors:**
- @behavior:http-transport-auth - Enforces authentication on all endpoints
- @behavior:http-transport-token-generate - Generates new API tokens
- @behavior:http-transport-token-validate - Validates bearer tokens and API keys

### Value Objects

#### HTTPEndpoint
**Description:** Maps an MCP tool to an HTTP route.

**Attributes:**
- `method: Literal["GET", "POST", "DELETE"]` - HTTP method
- `path: str` - URL path (e.g., "/v1/clients")
- `mcp_tool: str` - MCP tool name (e.g., "list_clients")
- `auth_required: bool` - Whether authentication is required
- `params: list[HTTPParameter]` - Path/query/body parameters

#### TokenMetadata
**Description:** Metadata about an API token.

**Attributes:**
- `token_id: str` - Unique token identifier
- `created_at: datetime` - When token was generated
- `expires_at: datetime | None` - Optional expiration time
- `last_used: datetime | None` - Last usage timestamp
- `usage_count: int` - Number of times token was used

#### CORSConfiguration
**Description:** CORS settings for web client access.

**Attributes:**
- `allow_origins: list[str]` - Allowed origins (default: ["*"])
- `allow_credentials: bool` - Allow credentials (default: True)
- `allow_methods: list[str]` - Allowed HTTP methods (default: ["*"])
- `allow_headers: list[str]` - Allowed headers (default: ["*"])

### Services

#### HTTPServerService
**Description:** Domain service for managing HTTP transport lifecycle.

**Methods:**
- `start_server(host, port, auth_service)` - Starts HTTP server
- `stop_server()` - Gracefully shuts down server
- `health_check()` - Returns server health status
- `get_openapi_schema()` - Returns OpenAPI schema

### Repositories

#### TokenStore (In-Memory)
**Description:** Stores and retrieves API tokens.

**Methods:**
- `generate_token() -> str` - Creates new token
- `validate_token(token: str) -> bool` - Checks if token exists
- `revoke_token(token: str)` - Invalidates token
- `list_tokens() -> list[TokenMetadata]` - Lists all tokens

---

## Behaviors

### @behavior:http-transport-expose
**Description:** All 10 MCP tools accessible via HTTP endpoints

**Acceptance Criteria:**
- Given the HTTP server is running
- When I send requests to /v1/* endpoints
- Then all 10 MCP tools respond correctly
- And stdio transport still works

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

### @behavior:http-transport-auth
**Description:** Bearer token and API key authentication enforced

**Acceptance Criteria:**
- Given a request to any /v1/* endpoint
- When no Authorization header is provided
- Then I receive 401 Unauthorized
- And error message explains authentication requirement

**Authentication Methods:**
1. **Bearer Token** (primary):
   ```
   Authorization: Bearer <token>
   ```

2. **API Key** (alternative):
   ```
   X-API-Key: <key>
   ```

### @behavior:http-transport-token-generate
**Description:** Generate new API tokens

**Acceptance Criteria:**
- Given I run `mcp-orchestration-generate-token`
- When the command executes
- Then a new 32-character token is generated
- And the token is stored in token store
- And the token is printed to stdout

**Security:**
- Tokens are cryptographically secure (secrets.token_urlsafe)
- Tokens are 32 characters (43 base64 characters)
- Tokens are unique (collision probability negligible)

### @behavior:http-transport-cors
**Description:** CORS configured for web client access

**Acceptance Criteria:**
- Given a web browser sends OPTIONS request
- When the preflight check occurs
- Then CORS headers are returned
- And POST/GET requests are allowed from any origin

**CORS Headers:**
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, DELETE, OPTIONS
Access-Control-Allow-Headers: *
```

### @behavior:http-transport-backward-compat
**Description:** stdio transport continues to work (no breaking changes)

**Acceptance Criteria:**
- Given mcp-orchestration is configured as stdio server
- When Claude Desktop connects via stdio
- Then all 10 MCP tools work as before
- And HTTP server is optional (not started by default)
- And no existing functionality is broken

### @behavior:http-transport-lifecycle
**Description:** Start and stop HTTP server gracefully

**Acceptance Criteria:**
- Given I run `mcp-orchestration-serve-http`
- When the server starts
- Then it binds to specified host:port
- And it logs "Server running on http://host:port"
- And it accepts requests within 5 seconds

**Shutdown:**
- Given the server is running
- When I send SIGINT (Ctrl+C)
- Then the server shuts down gracefully
- And in-flight requests complete
- And logs "Server shut down gracefully"

---

## Value Scenarios

### Scenario 1: Developer Tests HTTP API with curl
**User Story:** As a developer, I want to test the HTTP API locally using curl.

**Steps:**
1. Start HTTP server: `mcp-orchestration-serve-http --port 8000`
2. Generate token: `mcp-orchestration-generate-token`
3. Test endpoint: `curl -H "Authorization: Bearer <token>" http://localhost:8000/v1/clients`
4. Verify response: List of clients returned

**Success Criteria:**
- Server starts in < 5 seconds
- Token generation works
- Endpoint returns valid JSON
- Response time < 300ms

### Scenario 2: n8n Workflow Fetches Config
**User Story:** As an automation engineer, I want n8n to fetch MCP configurations via HTTP.

**Steps:**
1. n8n HTTP Request node: GET http://mcp-orchestration:8000/v1/config/claude-desktop/default
2. Set Authorization header with API key
3. Parse JSON response
4. Use config data in downstream nodes

**Success Criteria:**
- n8n can authenticate with API key
- Config is returned in JSON format
- n8n can parse and use the data
- Workflow completes successfully

### Scenario 3: Web App Integrates with HTTP API
**User Story:** As a web developer, I want my React app to fetch MCP servers via HTTP API.

**Steps:**
1. React app makes fetch() request to /v1/servers
2. CORS headers allow browser request
3. Bearer token in Authorization header
4. Display servers in UI

**Success Criteria:**
- CORS preflight succeeds
- Fetch request succeeds from browser
- JSON data renders in React components
- No CORS errors in console

---

## Technical Design

### FastAPI Application Structure

```python
# src/mcp_orchestrator/http/server.py

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MCP Orchestration HTTP API",
    version="0.2.0",
    description="Centralized MCP configuration orchestration",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configurable via env var
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication dependency
async def verify_auth(authorization: str = Header(None), x_api_key: str = Header(None)):
    """Verify bearer token or API key."""
    if not authorization and not x_api_key:
        raise HTTPException(401, "Authentication required")

    # Bearer token
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
        if auth_service.validate_bearer_token(token):
            return {"auth_type": "bearer", "token": token}

    # API key
    if x_api_key:
        if auth_service.validate_api_key(x_api_key):
            return {"auth_type": "api_key", "key": x_api_key}

    raise HTTPException(401, "Invalid authentication credentials")

# Example endpoint
@app.get("/v1/clients")
async def http_list_clients(auth=Depends(verify_auth)):
    """HTTP endpoint for list_clients MCP tool."""
    from mcp_orchestrator.mcp.server import list_clients
    result = await list_clients()
    return result
```

### Authentication Service

```python
# src/mcp_orchestrator/http/auth.py

import secrets
import os
from datetime import datetime

class AuthenticationService:
    """Validates bearer tokens and API keys."""

    def __init__(self):
        self.api_key = os.getenv("MCP_ORCHESTRATION_API_KEY")
        self._tokens: dict[str, TokenMetadata] = {}

    def generate_token(self) -> str:
        """Generate new API token."""
        token = secrets.token_urlsafe(32)  # 43 characters
        self._tokens[token] = TokenMetadata(
            token_id=token[:8],
            created_at=datetime.utcnow(),
            expires_at=None,  # No expiration in v0.2.0
            last_used=None,
            usage_count=0,
        )
        return token

    def validate_bearer_token(self, token: str) -> bool:
        """Validate bearer token."""
        if token in self._tokens:
            # Update usage metadata
            self._tokens[token].last_used = datetime.utcnow()
            self._tokens[token].usage_count += 1
            return True
        return False

    def validate_api_key(self, key: str) -> bool:
        """Validate API key from environment."""
        return key == self.api_key if self.api_key else False
```

### CLI Commands

```python
# src/mcp_orchestrator/cli_http.py

import click
import uvicorn

@click.command()
@click.option("--host", default="0.0.0.0", help="Server bind address")
@click.option("--port", default=8000, help="Server port")
@click.option("--log-level", default="info", help="Log level")
def serve_http(host: str, port: int, log_level: str):
    """Start HTTP server for MCP tools."""
    print(f"Starting HTTP server on http://{host}:{port}")
    print(f"API docs: http://{host}:{port}/docs")
    print(f"OpenAPI schema: http://{host}:{port}/openapi.json")

    uvicorn.run(
        "mcp_orchestrator.http.server:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=False,  # No reload in production
    )

@click.command()
def generate_token():
    """Generate new API token."""
    from mcp_orchestrator.http.auth import AuthenticationService

    auth_service = AuthenticationService()
    token = auth_service.generate_token()

    print(f"Generated token: {token}")
    print(f"\nUse in requests:")
    print(f'  Authorization: Bearer {token}')
    print(f"\nOr set as environment variable:")
    print(f'  export MCP_ORCHESTRATION_API_KEY={token}')
```

---

## Dependencies

### New Dependencies (pyproject.toml)

```toml
dependencies = [
    # ... existing dependencies
    "fastapi>=0.104.0",          # HTTP framework
    "uvicorn[standard]>=0.24.0", # ASGI server
    "python-multipart>=0.0.6",   # For file uploads (future)
]
```

**Justification:**
- **FastAPI**: Modern, fast, auto-generates OpenAPI docs
- **Uvicorn**: Production-grade ASGI server with WebSockets support
- **python-multipart**: Handles multipart/form-data (needed for file uploads in future)

---

## Integration Points

### 1. MCP Server Module
**Location:** `src/mcp_orchestrator/mcp/server.py`

**Integration:** HTTP endpoints wrap existing MCP tool functions
- No changes to MCP tool implementations
- HTTP layer is pure adapter/wrapper
- Reuses all validation, error handling, domain logic

### 2. CLI Module
**Location:** `src/mcp_orchestrator/cli.py`

**Integration:** Register new HTTP commands
- `mcp-orchestration-serve-http` added to CLI
- `mcp-orchestration-generate-token` added to CLI
- Both use existing Click framework

### 3. Configuration
**Environment Variables:**
- `MCP_ORCHESTRATION_API_KEY` - API key for X-API-Key header
- `MCP_ORCHESTRATION_HOST` - Server bind address (default: 0.0.0.0)
- `MCP_ORCHESTRATION_PORT` - Server port (default: 8000)
- `MCP_ORCHESTRATION_LOG_LEVEL` - Logging level (default: info)
- `MCP_ORCHESTRATION_CORS_ORIGINS` - Allowed CORS origins (default: *)

---

## Non-Functional Requirements

### NFR-3: Performance (p95 latency)
**Target:** p95 < 300ms for HTTP artifact retrieval

**Validation:**
- Load test with 100 concurrent requests
- Measure p95, p99 latencies
- Ensure < 300ms for GET /v1/config/*

### NFR-7: Authentication with RBAC
**Target:** Bearer token and API key authentication

**Validation:**
- Unauthorized requests rejected (401)
- Valid tokens accepted
- API key from environment works
- Token usage tracked

### NFR-9: Open, documented HTTP APIs
**Target:** REST endpoints with OpenAPI documentation

**Validation:**
- OpenAPI schema auto-generated by FastAPI
- Swagger UI available at /docs
- ReDoc UI available at /redoc
- All endpoints documented with descriptions

### NFR-11: Metrics, logs, traces
**Target:** Structured logging and request tracking

**Validation:**
- Request logging middleware
- Response time logging
- Error logging with stack traces
- Request ID tracking (X-Request-ID header)

---

## Testing Strategy

### Unit Tests (30+ tests)
**File:** `tests/test_http_server.py`

**Test scenarios:**
- Server initialization
- Endpoint routing
- Authentication middleware
- CORS headers
- Error handling

### Integration Tests (10+ tests)
**File:** `tests/integration/test_http_stdio_both.py`

**Test scenarios:**
- stdio transport still works
- HTTP transport works
- Both can run simultaneously
- No interference between transports

### E2E Value Scenarios (3 tests)
**File:** `tests/value-scenarios/test_http_transport.py`

**Test scenarios:**
1. Developer workflow: start server → generate token → call endpoints
2. n8n workflow: authenticate → fetch config → deploy
3. Web app workflow: CORS preflight → authenticated request → JSON response

### Performance Tests
**File:** `tests/performance/test_http_performance.py`

**Test scenarios:**
- 100 concurrent requests to /v1/clients
- Measure p95, p99 latencies
- Ensure < 300ms response time
- No memory leaks

---

## Success Criteria

### Functional Success
- ✅ All 10 MCP tools accessible via HTTP endpoints
- ✅ Bearer token authentication enforced
- ✅ API key authentication works
- ✅ stdio transport backward compatible
- ✅ CORS configured for web clients
- ✅ OpenAPI docs auto-generated
- ✅ Server starts/stops gracefully

### Performance Success
- ✅ p95 < 300ms for HTTP endpoints
- ✅ Server starts in < 5 seconds
- ✅ Handles 100 concurrent requests
- ✅ No memory leaks under load

### Quality Success
- ✅ 30+ unit tests, ≥85% coverage
- ✅ 3 E2E value scenarios pass
- ✅ Integration tests pass
- ✅ Performance tests pass
- ✅ Linting/type checking pass

### Documentation Success
- ✅ HTTP API reference complete
- ✅ 3 how-to guides (deploy, auth, migrate)
- ✅ OpenAPI schema published
- ✅ Migration guide tested

---

## Future Evolution (Wave 2.1+)

### Wave 2.1: API Enhancements
- Enhanced error responses (Universal Loadability Format)
- Batch operations
- Webhooks for config events
- Request/response validation improvements

### Wave 2.2: Ecosystem Integration
- mcp-gateway integration testing
- n8n workflow examples
- Performance optimization (caching, connection pooling)
- Metrics export (Prometheus)

### Wave 3.0+: Enterprise Features
- RBAC (role-based access control)
- Multi-tenancy
- Rate limiting
- Token expiration and rotation
- Audit logging

---

## Risks and Mitigations

### Risk 1: Token Security
**Risk:** In-memory tokens lost on server restart

**Mitigation (Wave 2.0):**
- Document that tokens are ephemeral
- Provide easy token regeneration
- Consider Redis persistence in Wave 2.1

### Risk 2: HTTPS/TLS
**Risk:** Users deploy without HTTPS, exposing tokens

**Mitigation:**
- Document reverse proxy setup (nginx, Caddy)
- Add warning if server runs on HTTP in production
- Consider built-in TLS in Wave 2.1

### Risk 3: Rate Limiting
**Risk:** API abuse without rate limiting

**Mitigation (Wave 2.0):**
- Document as known limitation
- Monitor for abuse in production
- Add rate limiting in Wave 2.2

### Risk 4: Breaking Changes
**Risk:** HTTP transport breaks stdio users

**Mitigation:**
- HTTP server is opt-in (not started by default)
- stdio transport unchanged
- Comprehensive integration tests
- Clear migration guide

---

## Related Documents

- **Wave Plan:** [WAVE_2X_PLAN.md](../WAVE_2X_PLAN.md)
- **Coordination:** [WAVE_2X_COORDINATION_PLAN.md](../WAVE_2X_COORDINATION_PLAN.md)
- **BDD Scenarios:** [behaviors/mcp-http-transport.feature](behaviors/mcp-http-transport.feature) (to be created)
- **Process Guide:** [END_TO_END_PROCESS.md](../END_TO_END_PROCESS.md)

---

**Document Version:** 1.0
**Created:** 2025-10-26
**Last Updated:** 2025-10-26
**Status:** @status:planned
**Wave:** 2.0
**Next Phase:** BDD Scenario Writing (Phase 2)
