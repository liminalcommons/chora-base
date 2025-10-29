# Reference: Docker MCP Server Deployment API

**Purpose**: Complete API reference for Docker-based MCP server deployment including environment variables, endpoints, volume mounts, and test specifications.

**Related Documents**:
- [Tutorial: Docker MCP Deployment](../../tutorials/advanced/03-docker-mcp-deployment.md)
- [How-To: Deploy MCP Server with Docker](../../how-to/deployment/deploy-mcp-server-docker.md)
- [Explanation: Docker MCP Rationale](../../explanation/deployment/docker-mcp-rationale.md)

---

## Environment Variables API

### MCP_TRANSPORT

**Type**: `string`
**Required**: No
**Default**: `"stdio"`
**Valid Values**: `"stdio"`, `"sse"`

**Description**: Selects MCP server transport mechanism

**Examples**:
```bash
# Claude Desktop (stdio)
MCP_TRANSPORT=stdio

# n8n/HTTP deployment (SSE)
MCP_TRANSPORT=sse
```

**Behavior**:
- `stdio`: Server uses stdin/stdout for communication (single client)
- `sse`: Server starts HTTP server with Server-Sent Events

---

### MCP_SERVER_HOST

**Type**: `string`
**Required**: No
**Default**: Auto-detected based on `MCP_TRANSPORT`
  - `"127.0.0.1"` if `MCP_TRANSPORT=stdio`
  - `"0.0.0.0"` if `MCP_TRANSPORT=sse`

**Description**: Host address to bind HTTP server

**Examples**:
```bash
# Explicit configuration
MCP_SERVER_HOST=0.0.0.0

# Auto-detection (recommended)
# (omit variable, let server auto-detect)
```

---

### MCP_SERVER_PORT

**Type**: `integer`
**Required**: No
**Default**: `8000`
**Valid Range**: `1024-65535`

**Description**: Port number for HTTP/SSE server (ignored for stdio transport)

**Examples**:
```bash
# Default port
MCP_SERVER_PORT=8000

# Custom port (if 8000 conflicts)
MCP_SERVER_PORT=9000
```

---

### ANTHROPIC_API_KEY

**Type**: `string`
**Required**: No (but required for `code_generation` generator)
**Format**: `sk-ant-api03-...`

**Description**: Anthropic API key for AI-powered code generation

**Examples**:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
```

**Behavior**:
- If set: `code_generation` generator registers
- If not set: Warning logged, generator not available

---

## Docker Image API

### Exposed Ports

**Port 8000**: HTTP/SSE endpoint

**Protocol**: HTTP/1.1, Server-Sent Events

**Endpoint**: `http://container:8000/sse`

### Volume Mounts

#### /app/configs

**Purpose**: Configuration files (content + artifact configs)

**Read/Write**: Read-only recommended for production

**Example**:
```yaml
volumes:
  - ./configs:/app/configs:ro  # Read-only
```

#### /app/ephemeral

**Purpose**: Temporary storage with auto-cleanup (30-day retention)

**Read/Write**: Read-write required

**Example**:
```yaml
volumes:
  - ./ephemeral:/app/ephemeral
```

#### /app/output

**Purpose**: Persistent artifact output

**Read/Write**: Read-write required

**Example**:
```yaml
volumes:
  - ./output:/app/output
```

---

## Docker Compose API

### Service: chora-compose-mcp

**Image**: `chora-compose-mcp:latest` (built from Dockerfile)

**Required Environment Variables**:
- None (all have defaults)

**Recommended Environment Variables**:
- `ANTHROPIC_API_KEY`: For code generation

**Port Mapping**:
```yaml
ports:
  - "8000:8000"
```

**Networks**:
```yaml
networks:
  - chora-network
```

**Health Check**:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

### Service: n8n (Optional)

**Image**: `n8nio/n8n:latest`

**Required Environment Variables**:
- `N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true`

**Port Mapping**:
```yaml
ports:
  - "5678:5678"
```

**Dependencies**:
```yaml
depends_on:
  chora-compose-mcp:
    condition: service_healthy
```

---

## Just Commands API

### just docker-build

**Syntax**: `just docker-build`

**Description**: Build chora-compose MCP server Docker image

**Implementation**:
```bash
docker build -t chora-compose-mcp:latest .
```

**Exit Codes**:
- `0`: Build successful
- `1`: Build failed

### just docker-up

**Syntax**: `just docker-up`

**Description**: Start multi-container stack (detached mode)

**Implementation**:
```bash
docker-compose up -d
```

**Exit Codes**:
- `0`: Containers started
- `1`: Start failed

### just docker-down

**Syntax**: `just docker-down`

**Description**: Stop all containers (preserve volumes)

**Implementation**:
```bash
docker-compose down
```

### just docker-logs

**Syntax**: `just docker-logs`

**Description**: View MCP server logs (follow mode)

**Implementation**:
```bash
docker-compose logs -f chora-compose-mcp
```

### just docker-health

**Syntax**: `just docker-health`

**Description**: Check MCP server health status

**Implementation**:
```bash
curl -f http://localhost:8000/health || echo "Health check failed"
docker-compose ps chora-compose-mcp
```

### just docker-shell

**Syntax**: `just docker-shell`

**Description**: Open interactive shell in MCP container

**Implementation**:
```bash
docker exec -it chora-compose-mcp /bin/bash
```

### just docker-restart

**Syntax**: `just docker-restart`

**Description**: Restart MCP server container

**Implementation**:
```bash
docker-compose restart chora-compose-mcp
```

### just docker-rebuild

**Syntax**: `just docker-rebuild`

**Description**: Rebuild image and restart containers

**Implementation**:
```bash
docker-compose down
docker build -t chora-compose-mcp:latest .
docker-compose up -d
```

### just docker-clean

**Syntax**: `just docker-clean`

**Description**: Remove containers and volumes (WARNING: deletes data)

**Implementation**:
```bash
docker-compose down -v
```

### just docker-ps

**Syntax**: `just docker-ps`

**Description**: Show container status

**Implementation**:
```bash
docker-compose ps
```

### just docker-logs-all

**Syntax**: `just docker-logs-all`

**Description**: View logs from all containers

**Implementation**:
```bash
docker-compose logs -f
```

---

## HTTP/SSE API

### GET /

**Description**: FastMCP home page

**Response**: `200 OK`

**Content-Type**: `text/html`

**Use Case**: Health check, verify server is running

### GET /sse

**Description**: MCP protocol Server-Sent Events endpoint

**Response**: `200 OK`

**Content-Type**: `text/event-stream`

**Behavior**: Opens SSE connection for MCP protocol communication

**Client Requirements**:
- Must support Server-Sent Events
- Should handle reconnection on disconnect
- Must send MCP protocol messages

### POST /mcp/v1/call (Hypothetical)

**Note**: Actual endpoint structure depends on FastMCP implementation. Consult FastMCP docs for exact API.

---

## Test Specifications

### Acceptance Criteria

#### Functional Requirements

| ID | Requirement | Priority | Validation |
|----|-------------|----------|------------|
| FR-1 | Docker image builds successfully | P0 | `docker build` exits 0 |
| FR-2 | Container starts and becomes healthy | P0 | Health check passes in <10s |
| FR-3 | HTTP/SSE endpoint accessible on port 8000 | P0 | `curl http://localhost:8000/sse` returns 200 |
| FR-4 | All 17 MCP tools registered | P0 | Logs show "Tools: 17" |
| FR-5 | stdio transport still works | P0 | `MCP_TRANSPORT=stdio` mode functional |
| FR-6 | Environment variables control transport | P0 | `MCP_TRANSPORT=sse` enables HTTP |
| FR-7 | n8n can connect and call tools | P0 | MCP Client node successful |
| FR-8 | Volume mounts allow config editing | P1 | Edit config without rebuild |
| FR-9 | Ephemeral storage persists across restarts | P1 | Data survives `docker restart` |
| FR-10 | Just commands work as documented | P1 | All commands exit successfully |

#### Non-Functional Requirements

| ID | Requirement | Target | Validation |
|----|-------------|--------|------------|
| NFR-1 | Build time | < 5 min | First build completes in time |
| NFR-2 | Container startup time | < 10 sec | Time to healthy state |
| NFR-3 | Image size | < 1 GB | `docker images` shows size |
| NFR-4 | Test coverage | ≥ 85% | pytest coverage report |
| NFR-5 | Security | Non-root user | Container runs as UID 1000 |
| NFR-6 | Documentation | 100% coverage | All scenarios documented |

### BDD Test Scenarios

#### Feature: docker_deployment.feature

```gherkin
Feature: Docker MCP Server Deployment
  As a developer
  I want to deploy chora-compose MCP server in Docker
  So that n8n workflows can access chora-compose tools

  Background:
    Given Docker Desktop is running
    And I am in the chora-compose project directory

  Scenario: Build Docker image successfully
    When I run "just docker-build"
    Then the build completes in less than 300 seconds
    And the image "chora-compose-mcp:latest" exists
    And the image size is less than 1GB

  Scenario: Start MCP server container
    Given the Docker image is built
    And .env file contains ANTHROPIC_API_KEY
    When I run "just docker-up"
    Then container "chora-compose-mcp" starts
    And the container becomes healthy within 10 seconds
    And logs show "Server ready at http://0.0.0.0:8000/sse"

  Scenario: MCP server exposes HTTP endpoint
    Given the container is running
    When I send GET request to "http://localhost:8000/"
    Then the response status is 200

  Scenario: All 17 MCP tools are registered
    Given the container is running
    When I check the server logs
    Then logs show "Tools: 17 (13 content + 4 config lifecycle)"

  Scenario: Stop containers cleanly
    Given containers are running
    When I run "just docker-down"
    Then all containers stop within 5 seconds
    And no processes remain running

  Scenario: Container restarts preserve ephemeral storage
    Given a container is running
    And ephemeral storage contains file "test-artifact.md"
    When I run "just docker-restart"
    Then the container restarts successfully
    And file "test-artifact.md" still exists in ephemeral storage

  Scenario: Rebuild after code changes
    Given the Docker image is built
    And I modify "src/chora_compose/mcp/server.py"
    When I run "just docker-rebuild"
    Then the image rebuilds with new code
    And the container restarts with updated image
    And new code is active

  Scenario: Environment variable override
    Given .env contains "MCP_SERVER_PORT=9000"
    When I run "just docker-up"
    Then the server listens on port 9000
    And logs show "Listening on: http://0.0.0.0:9000/sse"
```

#### Feature: server_transport.feature

```gherkin
Feature: MCP Server Transport Selection
  As a developer
  I want the MCP server to support both stdio and SSE transports
  So that it works with Claude Desktop and n8n

  Scenario: Default transport is stdio
    Given no MCP_TRANSPORT environment variable
    When the server starts
    Then transport mode is "stdio"
    And no HTTP server is started

  Scenario: SSE transport when configured
    Given MCP_TRANSPORT is set to "sse"
    When the server starts
    Then transport mode is "sse"
    And HTTP server starts on port 8000
    And endpoint "/sse" is available

  Scenario: Host auto-detection for SSE
    Given MCP_TRANSPORT is set to "sse"
    And MCP_SERVER_HOST is not set
    When the server starts
    Then the server binds to "0.0.0.0"

  Scenario: Custom port configuration
    Given MCP_TRANSPORT is set to "sse"
    And MCP_SERVER_PORT is set to "9000"
    When the server starts
    Then the server listens on port 9000

  Scenario: ANTHROPIC_API_KEY detection
    Given ANTHROPIC_API_KEY is set to a valid key
    When the server starts
    Then logs show "✓ ANTHROPIC_API_KEY detected"
    And "code_generation" generator is registered

  Scenario: Missing ANTHROPIC_API_KEY warning
    Given ANTHROPIC_API_KEY is not set
    When the server starts
    Then logs show warning about missing API key
    And "code_generation" generator is not registered
```

#### Feature: n8n_integration.feature

```gherkin
Feature: n8n MCP Client Integration
  As an n8n workflow builder
  I want to connect n8n to chora-compose MCP server
  So that I can use chora-compose tools in workflows

  Background:
    Given chora-compose MCP server is running in Docker
    And n8n is running in the same docker-compose stack

  Scenario: n8n connects to MCP server
    Given n8n MCP Client node is configured with endpoint "http://chora-compose-mcp:8000/sse"
    When I test the connection
    Then connection is successful
    And tools list loads

  Scenario: Call choracompose:list_generators from n8n
    Given n8n MCP Client is connected
    When I execute tool "choracompose:list_generators"
    Then the response includes "jinja2" generator
    And the response includes "code_generation" generator

  Scenario: Call choracompose:generate_content from n8n
    Given n8n MCP Client is connected
    And content config "hello-world-content" exists
    When I execute tool "choracompose:generate_content" with:
      | content_config_id | hello-world-content |
      | context | {"name": "n8n"} |
    Then the response contains generated content
    And the response includes "output" field

  Scenario: n8n waits for MCP server health
    Given docker-compose has depends_on with service_healthy
    When I run "docker-compose up -d"
    Then n8n container waits until chora-compose-mcp is healthy
    And n8n starts after health check passes
```

#### Feature: volume_mounts.feature

```gherkin
Feature: Docker Volume Mounts
  As a developer
  I want to edit configs without rebuilding
  So that I can iterate quickly

  Scenario: Config changes visible in container
    Given containers are running
    And volume mount maps ./configs to /app/configs
    When I create file "configs/content/test/test.json" on host
    Then file exists at "/app/configs/content/test/test.json" in container

  Scenario: Config changes immediately available
    Given containers are running
    When I update "configs/content/hello-world/hello-world-content.json"
    And I call "choracompose:generate_content" with "hello-world-content"
    Then the tool uses the updated config
    And no rebuild is required

  Scenario: Ephemeral storage persists across restarts
    Given container is running
    When I save file to ephemeral storage via MCP tool
    And I restart the container
    Then the file still exists in /app/ephemeral
    And retention policy is intact

  Scenario: Output directory writeable from container
    Given container is running
    When I generate artifact with output path "/app/output/test.md"
    Then file "test.md" appears in "./output/" on host
    And file is readable from host
```

---

## Performance Metrics

### Build Performance

| Phase | First Build | Cached Build |
|-------|-------------|--------------|
| Dependency install | ~2 min | 0 sec |
| Wheel build | ~30 sec | 0 sec |
| Image assembly | ~30 sec | ~10 sec |
| **Total** | **~3 min** | **~10 sec** |

### Runtime Performance

| Metric | Value |
|--------|-------|
| Container startup | ~5 sec |
| Health check latency | <1 sec |
| HTTP/SSE overhead | ~5-10ms per tool call |
| Memory usage (idle) | ~150MB |
| Image size | ~500MB |

---

## Security Specifications

### Container Security

**User**: Non-root execution as UID 1000

**Dockerfile Implementation**:
```dockerfile
RUN useradd -m -u 1000 -s /bin/bash chora
USER chora
```

**Rationale**: Principle of least privilege

### Secrets Management

**Development**: `.env` file (gitignored)

**Production**: External secrets manager required
- Docker Secrets
- Kubernetes Secrets
- HashiCorp Vault
- AWS Secrets Manager

### Network Security

**Development**: Port 8000 exposed to localhost only

**Production Recommendations**:
- Use reverse proxy (nginx, Traefik)
- Enable TLS/HTTPS
- Implement authentication (API keys, OAuth)
- Restrict to internal network

---

## Error Codes and Troubleshooting

### Build Errors

| Exit Code | Cause | Solution |
|-----------|-------|----------|
| 1 | Dockerfile syntax error | Check Dockerfile syntax |
| 1 | Poetry install failed | Check pyproject.toml dependencies |
| 1 | Out of disk space | Free up Docker disk space |

### Runtime Errors

| Symptom | Cause | Solution |
|---------|-------|----------|
| Container exits immediately | Python import error | Check logs for traceback |
| Port 8000 in use | Another process using port | Change MCP_SERVER_PORT |
| Permission denied | Volume mount ownership | chown -R 1000:1000 ephemeral/ |
| Health check fails | No /health endpoint | Use /sse endpoint instead |

---

## Version Compatibility

### Supported Versions

| Component | Version | Notes |
|-----------|---------|-------|
| Docker | ≥20.10 | Docker Desktop or Engine |
| docker-compose | ≥1.29 | Or `docker compose` (v2) |
| Python (container) | 3.12 | Base image python:3.12-slim |
| FastMCP | ≥2.12.4 | SSE transport support |
| n8n | Latest | n8n-nodes-mcp community package |

---

## API Contract Examples

### Successful Responses

**List Generators**:
```json
{
  "generators": [
    {
      "id": "jinja2",
      "name": "Jinja2 Generator",
      "description": "Template-based content generation"
    }
  ]
}
```

**Generate Content**:
```json
{
  "output": "Hello, World!",
  "generator_used": "jinja2",
  "duration_ms": 45,
  "metadata": {
    "template": "hello-world.j2",
    "context": {"name": "World"}
  }
}
```

### Error Responses

**Missing Config**:
```json
{
  "error": "ContentConfigNotFound",
  "message": "Config 'invalid-config' not found",
  "config_id": "invalid-config"
}
```

**Invalid Parameters**:
```json
{
  "error": "ValidationError",
  "message": "Missing required parameter: content_config_id"
}
```

---

## Related Documentation

**Tutorial**:
- [Tutorial: Docker MCP Deployment](../../tutorials/advanced/03-docker-mcp-deployment.md) - Step-by-step guide

**How-To**:
- [How-To: Deploy MCP Server with Docker](../../how-to/deployment/deploy-mcp-server-docker.md) - Practical workflows

**Explanation**:
- [Explanation: Docker MCP Rationale](../../explanation/deployment/docker-mcp-rationale.md) - Design decisions

**External**:
- [FastMCP API](https://gofastmcp.com/api)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)
- [Docker Compose Spec](https://docs.docker.com/compose/compose-file/)

---

**Document Version**: 1.0
**Last Updated**: 2025-10-21
**Next Review**: After test implementation
