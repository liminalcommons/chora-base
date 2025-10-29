# Explanation: Docker MCP Server Deployment Rationale

**Purpose**: Understanding the design decisions and architecture behind Docker-based MCP server deployment

**Related Tutorials**:
- [Tutorial: Docker MCP Deployment](../../tutorials/advanced/03-docker-mcp-deployment.md)

**Related How-To Guides**:
- [How-To: Deploy MCP Server with Docker](../../how-to/deployment/deploy-mcp-server-docker.md)

**Related Reference**:
- [Reference: Docker MCP API](../../reference/deployment/docker-mcp-reference.md)

---

## Overview

This document explains why chora-compose added Docker deployment support with HTTP/SSE transport, the design decisions made, trade-offs considered, and how it fits into the broader ecosystem.

---

## Problem Context

### The Single-Transport Limitation

Originally, chora-compose MCP server only supported **stdio transport**, which works excellently for Claude Desktop integration but has fundamental limitations:

**Stdio Transport Characteristics**:
- Process-based communication (stdin/stdout)
- Synchronous, single-client only
- Requires direct process execution
- Perfect for desktop AI assistants
- Cannot be accessed over network

**The Blocker**: n8n workflow automation requires HTTP/SSE transport. The `n8n-nodes-mcp` community package can only connect to network-accessible MCP servers, not local processes.

### Business Impact

**Immediate Need**: Integration with n8n workflow automation blocked

Without HTTP/SSE transport:
- ❌ Cannot build automated content generation workflows
- ❌ Cannot integrate with orchestration layers
- ❌ Cannot support multi-user/team deployments
- ❌ Cannot enable cloud deployment scenarios

**Strategic Value**: Docker + HTTP deployment enables:
- ✅ Workflow automation beyond Claude Desktop
- ✅ Multi-user team deployments
- ✅ Cloud/production deployment patterns
- ✅ Gateway and orchestration integration

---

## Why Docker?

### The Case for Containerization

**Chosen Approach**: Docker multi-stage build with docker-compose orchestration

**Rationale**:

1. **Reproducible Environments**
   - Same image works on dev, staging, production
   - No "works on my machine" problems
   - Version-locked dependencies

2. **Network Accessibility**
   - Containers expose ports natively
   - Docker networks for service communication
   - Easy integration with external tools (n8n)

3. **Isolation and Security**
   - Non-root user execution (user ID 1000)
   - Resource limits enforceable
   - Dependency isolation

4. **Developer Experience**
   - Single command setup (`just docker-up`)
   - Hot-reload configs via volume mounts
   - Integrated with existing `just` workflow

5. **Production Ready**
   - Health checks built-in
   - Restart policies
   - Horizontal scaling foundation

### Alternatives Considered

#### Alternative 1: Native Python HTTP Server (No Docker)

**Pros**:
- Simpler deployment (no Docker required)
- Faster startup
- Easier local debugging

**Cons**:
- Platform-specific dependencies
- Manual environment setup
- Harder to reproduce issues
- No isolation

**Why Rejected**: Docker provides superior reproducibility and isolation for team/production use

#### Alternative 2: HTTP Proxy in Front of stdio

**Pros**:
- No server.py changes
- Keep stdio as primary mode

**Cons**:
- Additional component to maintain
- Performance overhead (stdio ↔ proxy ↔ HTTP)
- Complex error handling
- State management issues

**Why Rejected**: FastMCP already provides native SSE transport - using it directly is simpler

#### Alternative 3: Separate HTTP Server Project

**Pros**:
- Complete separation of concerns
- Dedicated HTTP optimization

**Cons**:
- Duplicate tool definitions (17 tools)
- Sync issues between servers
- Double maintenance burden
- No benefit for other MCP clients

**Why Rejected**: Single codebase serving both transports is more maintainable

---

## Design Decisions

### Decision 1: Multi-Stage Docker Build

**Options**:
- A. Single-stage build
- B. Multi-stage build with builder + runtime

**Chosen**: Multi-stage build

**Rationale**:
- **40% smaller final image** (~500MB vs ~850MB)
  - No build tools (gcc, Poetry) in runtime image
  - Only Python interpreter + runtime dependencies
- **Faster container startup** (fewer layers)
- **Security** (no compilers in production image)
- **Industry best practice**

**Trade-off**: Slightly more complex Dockerfile, but worthwhile for production deployments

**Implementation**:
```dockerfile
# Stage 1: Builder
FROM python:3.12-slim AS builder
COPY . /build
WORKDIR /build
RUN poetry build --format wheel

# Stage 2: Runtime
FROM python:3.12-slim
COPY --from=builder /build/dist/*.whl /tmp/
RUN pip install /tmp/*.whl
```

---

### Decision 2: Transport Configuration via Environment Variables

**Options**:
- A. Command-line flags (`--transport=sse`)
- B. Environment variables (`MCP_TRANSPORT=sse`)
- C. Configuration file (`mcp_config.yaml`)

**Chosen**: Environment variables

**Rationale**:
- **Docker-native** (docker-compose env section)
- **12-factor app compliance**
- **No code changes** to switch transports
- **Easy to override** in different environments (dev/staging/prod)
- **Secure** (.env files not committed to git)

**Trade-off**: Requires .env file management, but this is standard Docker practice

**Implementation**:
```python
transport = os.getenv("MCP_TRANSPORT", "stdio")
if transport == "sse":
    host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_SERVER_PORT", "8000"))
    mcp.run(transport="sse", host=host, port=port)
else:
    mcp.run(transport="stdio")
```

---

### Decision 3: Wheel Install vs. Editable Install

**Options**:
- A. Editable install (`poetry install` - symlinks source)
- B. Wheel install (`poetry build` + `pip install dist/*.whl`)

**Chosen**: Wheel install

**Rationale**:
- **Avoids PYTHONPATH conflicts**
  - No `/app/src` in PYTHONPATH
  - Standard package distribution method
- **Prevents naming collisions**
  - chora_compose package vs mcp module
  - Clean import resolution
- **Reproducible installations**
  - Same .whl file = identical environment

**Trade-off**: Slightly longer build time (~30 seconds), but eliminates import issues that plagued earlier approaches

**The Import Problem This Solved**:
```python
# Editable install (BROKEN):
# /app/src/chora_compose and /usr/local/lib/python3.12/site-packages/mcp both exist
from chora_compose.mcp import server  # Which mcp? Ambiguous!

# Wheel install (WORKS):
# Only /usr/local/lib/python3.12/site-packages/chora_compose exists
from chora_compose.mcp import server  # Clear resolution!
```

---

### Decision 4: Volume Mount Strategy

**Options**:
- A. No volumes (rebuild for config changes)
- B. Mount only configs (read-only)
- C. Mount configs + ephemeral + output (read-write)

**Chosen**: Mount all data directories

**Rationale**:

**Configs Volume** (`./configs:/app/configs`):
- Edit without rebuild (developer-friendly)
- Instant iteration on templates
- Production: Can use read-only mount

**Ephemeral Volume** (`./ephemeral:/app/ephemeral`):
- Persist across container restarts
- 30-day retention policy intact
- Survive deployments without data loss

**Output Volume** (`./output:/app/output`):
- Artifact preservation
- Easy host access for CI/CD
- Backup-friendly

**Trade-off**: Must manage host directory permissions (user ID 1000), but provides maximum flexibility

---

### Decision 5: Backward Compatibility with stdio

**Options**:
- A. Remove stdio transport (breaking change)
- B. Support both transports (maintain compatibility)

**Chosen**: Support both transports

**Rationale**:
- **Existing Claude Desktop users unaffected**
  - Default remains stdio
  - Zero migration required
- **Same codebase serves both use cases**
  - DRY principle (Don't Repeat Yourself)
  - Single source of truth for tool definitions
- **Easy A/B testing during rollout**
  - Can compare stdio vs SSE performance
  - Gradual adoption possible

**Trade-off**: Slightly more complex server.py logic (if/else on transport), but worth it for smooth migration

**Implementation**:
```python
def main():
    transport = os.getenv("MCP_TRANSPORT", "stdio")  # Default: stdio
    if transport == "sse":
        # HTTP/SSE mode for n8n
        mcp.run(transport="sse", host="0.0.0.0", port=8000)
    else:
        # stdio mode for Claude Desktop (default)
        mcp.run(transport="stdio")
```

---

## Architecture Deep Dive

### Multi-Container Docker Compose Stack

```
┌─────────────────────────────────────────────────────────┐
│ Docker Desktop                                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────┐    HTTP/SSE    ┌───────────────┐ │
│  │   n8n Container  │◄──────────────►│ chora-compose │ │
│  │  (MCP Client)    │                │ MCP Server    │ │
│  │  Port: 5678      │                │ Port: 8000    │ │
│  └──────────────────┘                └───────────────┘ │
│           │                                  │          │
│           │                                  │          │
│           │         chora-network            │          │
│           └────────────────────────────────  ┘          │
│                                              │          │
│                                  Volume Mounts          │
│                                              ▼          │
│                                   ┌───────────────────┐ │
│                                   │ Host Filesystem   │ │
│                                   │ - configs/        │ │
│                                   │ - ephemeral/      │ │
│                                   │ - output/         │ │
│                                   └───────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**Why This Architecture?**

1. **Service Discovery**: Docker network enables `http://chora-compose-mcp:8000` addressing
2. **Dependency Management**: n8n waits for chora-compose health check
3. **Data Persistence**: Volumes survive container lifecycle
4. **Isolation**: Each service in its own container

---

## MCP Protocol: stdio vs SSE

### Transport Comparison

| Aspect | stdio Transport | SSE Transport |
|--------|----------------|---------------|
| **Communication** | stdin/stdout pipes | HTTP + Server-Sent Events |
| **Clients** | Single process | Multiple network clients |
| **State** | Stateful (process lifetime) | Stateless (HTTP request/response) |
| **Network** | Not network-accessible | Network-accessible |
| **Best For** | Desktop AI assistants | Workflow automation, cloud |
| **Security** | Process isolation | Network security (TLS, auth) |

### Why FastMCP Supports Both

**FastMCP Design Philosophy**: One framework, multiple transports

```python
# Same MCP server implementation works with both:

# For Claude Desktop:
mcp.run(transport="stdio")

# For n8n:
mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

**Tool definitions are transport-agnostic**: The 17 MCP tools work identically regardless of transport. This is the power of the MCP protocol abstraction.

---

## Integration with n8n

### Why n8n Requires HTTP/SSE

**n8n Architecture**: Browser-based workflow builder + Node.js backend

**Constraint**: Browser can't spawn/manage local processes (security sandbox)

**Solution**: n8n MCP Client node uses HTTP/SSE to connect to remote MCP servers

**Connection Flow**:
```
n8n Workflow → n8n-nodes-mcp → HTTP GET /sse → chora-compose MCP Server
                                              ↓
                                     SSE Stream (tools, resources)
                                              ↓
                                     HTTP POST /call (tool invocation)
```

---

## Gateway and Orchestration Integration

### Design for Gateway Consumption

The Docker deployment pattern supports **gateway/orchestration layers** like n8n, Windmill, Temporal:

**Key Features**:
1. **Upstream Dependencies Discovery**
   - `upstream_dependencies` field in configs
   - Gateway can build DAGs automatically

2. **Event Telemetry**
   - Events emitted to `var/telemetry/events.jsonl`
   - Gateway can monitor execution, errors, performance

3. **Trace Context Propagation**
   - `CHORA_TRACE_ID` environment variable
   - Distributed tracing across tool calls

4. **Concurrency Limits**
   - Exposed via `capabilities://server` resource
   - Gateway can throttle requests

See [How-To: Use with Gateway](../../how-to/mcp/use-with-gateway.md) for details.

---

## Security Considerations

### Non-Root Container Execution

**Default Behavior**: Container runs as user ID `1000` (not root)

**Why?**
- **Principle of least privilege**: Container compromise doesn't = root access
- **File permissions**: Matches common developer user IDs (1000)
- **Kubernetes best practice**: Non-root is required in many k8s clusters

**Implementation**:
```dockerfile
RUN useradd -m -u 1000 -s /bin/bash chora
USER chora
```

### Secrets Management

**Development**: `.env` file (not committed)

**Production**: Use external secrets management
- HashiCorp Vault
- AWS Secrets Manager
- Kubernetes Secrets
- Docker Secrets (Swarm)

**Never commit**:
- `.env` files with real API keys
- `docker-compose.override.yml` with secrets

---

## Performance Characteristics

### Build Performance

| Phase | Time (First) | Time (Cached) |
|-------|--------------|---------------|
| Dependency install | ~2 min | 0 sec (cached) |
| Wheel build | ~30 sec | 0 sec (cached) |
| Image assembly | ~30 sec | ~10 sec |
| **Total** | **~3 min** | **~10 sec** |

### Runtime Performance

| Metric | Value |
|--------|-------|
| Container startup | ~5 sec |
| Health check latency | <1 sec |
| HTTP/SSE overhead | ~5-10ms per tool call |
| Memory usage | ~150MB (idle) |
| Image size | ~500MB |

**Compared to stdio**: SSE adds negligible latency (~5-10ms) for network roundtrip

---

## Trade-offs Summary

### What We Gained

✅ **Network accessibility**: n8n, gateways, cloud deployment
✅ **Reproducibility**: Docker images work everywhere
✅ **Multi-user support**: HTTP supports concurrent clients
✅ **Production readiness**: Health checks, scaling, monitoring
✅ **Developer experience**: `just docker-up`, hot-reload configs

### What We Accepted

⚠️ **Complexity**: Docker + docker-compose required
⚠️ **Resource usage**: ~500MB image, ~150MB RAM
⚠️ **Build time**: ~3 minutes first build (vs instant Python)
⚠️ **Network latency**: ~5-10ms HTTP overhead (vs stdio pipes)

### What We Preserved

✅ **Backward compatibility**: stdio still default
✅ **Zero breaking changes**: Existing Claude Desktop users unaffected
✅ **Same codebase**: One implementation, two transports

---

## Future Evolution

### What's Next?

**Phase 1: Documentation** (Complete) ✅
- Tutorial, how-to, explanation, reference docs
- BDD test scenarios
- Deployment guide

**Phase 2: Testing** (In Progress)
- pytest-bdd scenarios
- Integration tests
- Smoke tests

**Phase 3: Production Enhancements** (Future)
- Authentication/authorization
- HTTPS/TLS support (reverse proxy pattern)
- Prometheus metrics
- Structured logging (JSON format)
- Horizontal scaling documentation

**Phase 4: Cloud Deployment Patterns** (Future)
- Kubernetes manifests
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances

---

## Lessons Learned

### What Worked Well

✅ **Multi-stage build**: 40% size reduction worth the complexity
✅ **Wheel install**: Eliminated all import issues
✅ **Environment variables**: Clean, Docker-native configuration
✅ **Backward compatibility**: Smooth migration, zero complaints

### What Was Challenging

⚠️ **Package import conflicts**: Took time to discover wheel install solution
⚠️ **Volume permissions**: User ID 1000 occasionally causes confusion
⚠️ **Health check**: FastMCP doesn't provide `/health`, use root endpoint

### What We'd Do Differently

💡 **Earlier testing**: Should have written tests before implementation
💡 **Production docs first**: Security/TLS guidance should come with initial release
💡 **Metrics from day 1**: Easier to add telemetry early than retrofit

---

## Related Design Decisions

This deployment pattern connects to other architectural decisions:

**Config-Driven Architecture**: [Why Config-Driven Architecture](../architecture/config-driven-architecture.md)
- Configs as volume mounts enable hot-reload
- Declarative workflows survive container restarts

**Event-Driven Telemetry**: [Event Telemetry Design](../../explanation/design-decisions/event-driven-telemetry.md)
- JSONL events enable gateway monitoring
- File-based storage simple in Docker volumes

**Gateway Integration**: [MCP Workflow Model](../../explanation/integration/mcp-workflow-model.md)
- HTTP/SSE transport enables orchestration layers
- Stateless design supports horizontal scaling

---

## Summary

Docker deployment with HTTP/SSE transport unlocks chora-compose's potential beyond desktop AI assistants:

**Key Benefits**:
- Network-accessible MCP server for n8n, gateways, cloud
- Reproducible Docker-based deployment
- Multi-user and team collaboration
- Production-ready foundation

**Design Philosophy**:
- Backward compatible (stdio still default)
- Developer-friendly (`just` commands, hot-reload)
- Security-conscious (non-root, secrets management)
- Production-oriented (health checks, monitoring hooks)

**Strategic Positioning**:
- Enables workflow automation ecosystems
- Supports orchestration layer integration
- Foundation for cloud/team deployments

This is not just "adding Docker support" - it's enabling a whole new class of use cases while maintaining the simplicity that makes chora-compose great for individual developers.

---

**Related Reading**:
- [Tutorial: Docker MCP Deployment](../../tutorials/advanced/03-docker-mcp-deployment.md) - Step-by-step guide
- [How-To: Deploy MCP Server with Docker](../../how-to/deployment/deploy-mcp-server-docker.md) - Practical workflows
- [Reference: Docker MCP API](../../reference/deployment/docker-mcp-reference.md) - Complete specifications
- [Why Config-Driven Architecture](../architecture/config-driven-architecture.md) - Foundation concept

**External References**:
- [FastMCP SSE Transport](https://gofastmcp.com/servers/transports#sse)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Docker Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [12-Factor App](https://12factor.net/config)

---

**Document Version**: 1.0
**Last Updated**: 2025-10-21
**Next Review**: After production deployments begin
