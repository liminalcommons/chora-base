# How-To: Deploy chora-compose MCP Server with Docker

**Purpose**: Run chora-compose as an MCP server accessible to n8n workflows via HTTP/SSE transport in Docker containers.

**Target Audience**: DevOps engineers, workflow developers, system administrators deploying chora-compose for team use.

**Prerequisites**:
- Docker Desktop installed and running
- Basic familiarity with docker-compose
- n8n instance (existing or will be deployed with this guide)
- Anthropic API key (for code_generation generator)

**Time**: 10-15 minutes for initial setup

---

## Quick Start (3 Commands)

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY=your_key_here

# 2. Build and start containers
just docker-build
just docker-up

# 3. Verify MCP server is running
curl http://localhost:8000/health
```

**Result**: chora-compose MCP server running at `http://localhost:8000/sse`, accessible from n8n.

---

## Architecture Overview

This deployment creates a multi-container environment:

```
┌─────────────────────────────────────────────────────────────┐
│ Docker Desktop                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐    HTTP/SSE    ┌──────────────────┐  │
│  │   n8n Container  │◄──────────────►│ chora-compose    │  │
│  │  (MCP Client)    │                │ MCP Server       │  │
│  │                  │                │ Container        │  │
│  │ Port: 5678       │                │ Port: 8000       │  │
│  └──────────────────┘                └──────────────────┘  │
│         │                                     │             │
│         │                                     │             │
│         ▼                                     ▼             │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Shared Docker Network: chora-network               │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│                                     Volume Mounts:           │
│                                     - configs/               │
│                                     - templates/             │
│                                     - ephemeral/             │
│                                     - output/                │
└─────────────────────────────────────────────────────────────┘
```

**Key Components**:
1. **chora-compose-mcp**: MCP server container (port 8000)
2. **n8n**: Workflow automation (port 5678) - optional
3. **chora-network**: Bridge network for inter-container communication
4. **Volume mounts**: Persistent storage for configs, templates, outputs

---

## Step-by-Step Setup

### Step 1: Configure Environment Variables

Create `.env` file from template:

```bash
cp .env.example .env
```

Edit `.env` and configure:

```bash
# Required: Anthropic API key for code_generation generator
ANTHROPIC_API_KEY=sk-ant-api03-xxx

# Optional: MCP server configuration (defaults shown)
MCP_TRANSPORT=sse
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8000
MCP_LOG_LEVEL=INFO
```

**Important**: Keep `.env` private - it contains API keys. Never commit to version control.

### Step 2: Build Docker Image

Build the chora-compose MCP server image:

```bash
just docker-build
```

**What this does**:
- Multi-stage Docker build using Python 3.12
- Installs Poetry and Python dependencies
- Copies source code, configs, templates
- Creates non-root user for security
- Exposes port 8000 for HTTP/SSE transport
- Sets up health check endpoint

**Expected output**:
```
Successfully built 3f2a1b9c8d4e
Successfully tagged chora-compose-mcp:latest
```

### Step 3: Start Containers

Start the multi-container stack:

```bash
just docker-up
```

**What this starts**:
1. **chora-compose-mcp**: MCP server on port 8000
2. **n8n**: Workflow automation on port 5678 (if included in docker-compose.yml)

**Expected output**:
```
Creating network "chora-network" with driver "bridge"
Creating volume "n8n-data" with default driver
Creating chora-compose-mcp ... done
Creating n8n               ... done
```

### Step 4: Verify MCP Server

Check that the MCP server is running:

```bash
# Option 1: Health check endpoint
curl http://localhost:8000/health

# Option 2: Just command (shows health + container status)
just docker-health

# Option 3: View logs
just docker-logs
```

**Expected health check response**:
```json
{
  "status": "healthy",
  "server": "chora-compose",
  "version": "1.1.0",
  "transport": "sse",
  "tools": 17
}
```

**Expected log output**:
```
Starting chora-compose MCP server...
Server: chora-compose v1.1.0
Transport: sse
Listening on: http://0.0.0.0:8000/sse
Tools: 17 (13 content + 4 config lifecycle)
------------------------------------------------------------
✓ ANTHROPIC_API_KEY detected - code_generation available
------------------------------------------------------------
Server ready at http://0.0.0.0:8000/sse
Waiting for connections...
```

---

## Configuring n8n MCP Client

### Option A: n8n Running in Docker (Same docker-compose Stack)

If using the provided docker-compose.yml with n8n included:

1. **Access n8n**: Open http://localhost:5678
2. **Install MCP Client node**:
   - Go to Settings → Community Nodes
   - Install: `n8n-nodes-mcp`
3. **Create MCP Client node** in workflow:
   - Add node: "MCP Client"
   - **Connection Type**: HTTP Streamable
   - **HTTP Endpoint**: `http://chora-compose-mcp:8000/sse`
   - **Headers**: Leave empty (no authentication required)
4. **Test connection**: Use "Test" button
5. **Use MCP tools**: Select tool from dropdown (e.g., `choracompose:list_generators`)

### Option B: n8n Running in External Docker Container

If n8n is running in a separate Docker container:

**Challenge**: n8n container can't reach `localhost:8000` because localhost refers to the container itself.

**Solution**: Use Docker networking:

**Method 1: Add n8n to chora-network** (recommended)

Edit your n8n docker-compose.yml:

```yaml
services:
  n8n:
    image: n8nio/n8n:latest
    # ... other config ...
    networks:
      - chora-network

networks:
  chora-network:
    external: true  # Use existing network from chora-compose
```

Then configure MCP Client:
- **HTTP Endpoint**: `http://chora-compose-mcp:8000/sse`

**Method 2: Use host.docker.internal** (macOS/Windows Docker Desktop)

Configure MCP Client:
- **HTTP Endpoint**: `http://host.docker.internal:8000/sse`

**Method 3: Use host network mode** (Linux only)

Edit chora-compose docker-compose.yml:

```yaml
services:
  chora-compose-mcp:
    network_mode: "host"
    # Remove ports section (not needed with host mode)
```

Then configure MCP Client:
- **HTTP Endpoint**: `http://localhost:8000/sse`

### Option C: n8n Running Outside Docker (Host Machine)

If n8n is installed directly on host machine (not in Docker):

Configure MCP Client:
- **HTTP Endpoint**: `http://localhost:8000/sse`

---

## Volume Mounts Explained

The docker-compose.yml mounts several directories for persistence and editability:

### `/app/configs` - Configuration Files

**Purpose**: Artifact and content configurations

**Host path**: `./configs`

**Why mount**: Edit configs from host without rebuilding container

**Example**:
```bash
# Edit config on host
vim configs/content/my-report/my-report-content.json

# Changes immediately available to MCP server (no restart needed)
```

### `/app/templates` - Jinja2 Templates

**Purpose**: Template files for content generation

**Host path**: `./templates`

**Why mount**: Update templates without rebuilding

**Example**:
```bash
# Edit template
vim templates/daily-report.jinja2

# Changes available immediately
```

### `/app/ephemeral` - Temporary Storage

**Purpose**: Ephemeral artifacts with auto-cleanup

**Host path**: `./ephemeral`

**Why mount**: Persist ephemeral content across container restarts

**Behavior**:
- Files retained for configured retention period (default: 30 days)
- Survives container restarts
- Cleaned up automatically by `EphemeralStorageManager`

### `/app/output` - Persistent Artifacts

**Purpose**: Long-term artifact storage

**Host path**: `./output`

**Why mount**: Keep generated artifacts even if container is removed

**Example**:
```bash
# Artifacts saved here persist forever
ls output/reports/
```

---

## Environment Variable Reference

### Required Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | None | Anthropic API key for code_generation generator (required) |

### MCP Server Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_TRANSPORT` | `stdio` | Transport type: `stdio` (Claude Desktop) or `sse` (HTTP) |
| `MCP_SERVER_HOST` | `0.0.0.0` | Host to bind to (use `0.0.0.0` for Docker) |
| `MCP_SERVER_PORT` | `8000` | HTTP/SSE port (only used if `MCP_TRANSPORT=sse`) |
| `MCP_LOG_LEVEL` | `INFO` | Log level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |

### n8n Configuration (if using included n8n service)

| Variable | Default | Description |
|----------|---------|-------------|
| `N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE` | `false` | Allow MCP Client node to use tools in AI Agents (set to `true`) |

---

## Common Just Commands

### Development Workflow

```bash
# Build image
just docker-build

# Start containers
just docker-up

# View logs (follow mode)
just docker-logs

# Full dev workflow (build + start + logs)
just docker-dev
```

### Operations

```bash
# Restart MCP server
just docker-restart

# Stop all containers
just docker-down

# Check health status
just docker-health

# View container status
just docker-ps
```

### Debugging

```bash
# Open shell in MCP container
just docker-shell

# View all logs (n8n + chora-compose)
just docker-logs-all
```

### Cleanup

```bash
# Remove containers and volumes (WARNING: deletes data)
just docker-clean

# Rebuild after code changes
just docker-rebuild
```

---

## Troubleshooting

### Problem: Health check fails (404 Not Found)

**Symptom**:
```bash
curl http://localhost:8000/health
# 404 Not Found
```

**Cause**: FastMCP doesn't automatically create `/health` endpoint.

**Solution**: Use SSE endpoint for testing instead:

```bash
# Test SSE endpoint
curl http://localhost:8000/sse
# Should return MCP protocol handshake
```

**Alternative**: Remove health check from Dockerfile (line 71-73) or implement custom `/health` endpoint.

### Problem: n8n can't connect to MCP server

**Symptom**: "Could not connect to your MCP server" error in n8n

**Diagnosis**:

1. **Check network connectivity**:
   ```bash
   # From n8n container
   docker exec n8n curl http://chora-compose-mcp:8000/sse
   ```

2. **Verify both containers on same network**:
   ```bash
   docker network inspect chora-network
   # Should show both containers
   ```

3. **Check MCP server logs**:
   ```bash
   just docker-logs
   ```

**Solutions**:
- If containers on different networks: Add n8n to `chora-network`
- If using external n8n: Use `http://host.docker.internal:8000/sse` (macOS/Windows) or `http://localhost:8000/sse` (Linux with host network mode)
- If firewall blocks port 8000: Check Docker Desktop network settings

### Problem: ANTHROPIC_API_KEY not detected

**Symptom**:
```
⚠️  Warning: ANTHROPIC_API_KEY not found in environment.
   code_generation generator will not be registered.
```

**Diagnosis**:
```bash
# Check if .env file exists
ls -la .env

# Verify env var in container
docker exec chora-compose-mcp env | grep ANTHROPIC_API_KEY
```

**Solutions**:
1. Create `.env` file from `.env.example`
2. Set `ANTHROPIC_API_KEY=your_key_here` in `.env`
3. Restart containers: `just docker-down && just docker-up`

### Problem: Container exits immediately

**Symptom**: Container shows "Exited (1)" status

**Diagnosis**:
```bash
# View container logs
just docker-logs

# Check exit code
docker inspect chora-compose-mcp --format='{{.State.ExitCode}}'
```

**Common causes**:
- Missing dependencies: Check Dockerfile poetry install step
- Python import errors: Check logs for traceback
- Port already in use: Change `MCP_SERVER_PORT` in `.env`

**Solution**: Fix error shown in logs and rebuild:
```bash
just docker-rebuild
```

### Problem: Volume mounts not working (configs not syncing)

**Symptom**: Editing `configs/` on host doesn't affect MCP server

**Diagnosis**:
```bash
# Check volume mounts
docker inspect chora-compose-mcp --format='{{json .Mounts}}' | jq

# Verify file exists in container
docker exec chora-compose-mcp ls /app/configs/content/
```

**Solutions**:
- Verify paths in docker-compose.yml are correct
- Check file permissions (container runs as user `choracompose:1000`)
- On Windows: Ensure Docker Desktop has access to drive with configs

### Problem: Permission denied errors in container

**Symptom**: `PermissionError: [Errno 13] Permission denied: '/app/ephemeral'`

**Cause**: Volume mount ownership mismatch

**Solution**:
```bash
# Fix permissions on host
chmod -R 755 ephemeral/
chown -R 1000:1000 ephemeral/  # Match container user ID

# Or run container as root (not recommended for production)
# Edit docker-compose.yml:
# user: "0:0"
```

---

## Production Considerations

### Secrets Management

**Development** (current setup):
- Secrets in `.env` file (gitignored)
- Environment variables passed via docker-compose

**Production** (recommended):
- Use Docker secrets or Kubernetes secrets
- Store API keys in HashiCorp Vault, AWS Secrets Manager, etc.
- Inject secrets at runtime, not in `.env` file

**Example with Docker secrets**:

```yaml
services:
  chora-compose-mcp:
    secrets:
      - anthropic_api_key
    environment:
      - ANTHROPIC_API_KEY=/run/secrets/anthropic_api_key

secrets:
  anthropic_api_key:
    external: true
```

### Data Persistence

**Current setup**: Host volume mounts

**Considerations**:
- **Ephemeral storage**: Set retention policy in production (e.g., 7 days)
- **Configs**: Version control with git, mount read-only in production
- **Templates**: Same as configs, read-only recommended
- **Output**: Use external storage (S3, NFS) for long-term artifacts

**Example read-only mount**:

```yaml
volumes:
  - ./configs:/app/configs:ro  # Read-only
  - ./templates:/app/templates:ro
```

### Monitoring & Logging

**Logging**:
- Centralize logs with Docker logging drivers (e.g., `json-file`, `syslog`)
- Use log aggregation (ELK, Splunk, CloudWatch)

**Monitoring**:
- Add Prometheus metrics endpoint to FastMCP server
- Monitor container health with Docker health checks
- Set up alerts for container failures

**Example logging driver**:

```yaml
services:
  chora-compose-mcp:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Scaling & High Availability

**Current setup**: Single container

**Production options**:
1. **Horizontal scaling**: Deploy multiple MCP server replicas behind load balancer
2. **Vertical scaling**: Increase container resources (CPU, memory)
3. **Kubernetes**: Use Deployment with replicas + Service for load balancing

**Limitations**:
- Ephemeral storage is local (not shared across replicas)
- Consider external storage (Redis, S3) for shared ephemeral artifacts

### Network Security

**Development**: Port 8000 exposed to host

**Production**:
- Use reverse proxy (nginx, Traefik) with TLS
- Implement authentication (API keys, OAuth)
- Restrict network access (internal network only, no public exposure)

**Example with Traefik reverse proxy**:

```yaml
services:
  chora-compose-mcp:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.mcp.rule=Host(`mcp.example.com`)"
      - "traefik.http.routers.mcp.tls=true"
```

---

## Testing the Integration

### Test 1: List Available Generators

**n8n workflow**:
1. Add "MCP Client" node
2. Select tool: `choracompose:list_generators`
3. Execute

**Expected response**:
```json
{
  "generators": [
    {
      "id": "jinja2",
      "name": "Jinja2 Generator",
      "description": "Template-based content generation using Jinja2"
    },
    {
      "id": "code_generation",
      "name": "AI Code Generation",
      "description": "Generate code using Claude API"
    }
  ]
}
```

### Test 2: Generate Content

**n8n workflow**:
1. Add "MCP Client" node
2. Select tool: `choracompose:generate_content`
3. Parameters:
   ```json
   {
     "content_config_id": "hello-world-content",
     "context": {
       "name": "n8n"
     }
   }
   ```
4. Execute

**Expected response**:
```json
{
  "output": "Hello, n8n!",
  "generator_used": "jinja2",
  "duration_ms": 45
}
```

### Test 3: List Content Configs

**n8n workflow**:
1. Add "MCP Client" node
2. Select tool: `choracompose:list_content_configs`
3. Execute

**Expected response**:
```json
{
  "configs": [
    {
      "id": "hello-world-content",
      "path": "configs/content/hello-world/hello-world-content.json",
      "generator": "jinja2"
    }
  ]
}
```

---

## Next Steps

After deploying the MCP server:

1. **Explore MCP tools**: Try all 17 tools from n8n MCP Client
2. **Create workflows**: Build n8n workflows using chora-compose tools
3. **Add configurations**: Create content and artifact configs for your use cases
4. **Monitor performance**: Check logs, health status, resource usage
5. **Iterate**: Update configs/templates and test changes (no rebuild needed)

---

## Additional Workflows

### Update Configs Without Rebuild

**Scenario**: You need to iterate quickly on config changes without rebuilding Docker images.

**Steps**:
1. Edit config file on host:
   ```bash
   vim configs/content/my-report/my-report-content.json
   ```

2. Changes are immediately visible in container (volume mount):
   ```bash
   docker exec chora-compose-mcp ls /app/configs/content/my-report/
   ```

3. Test changes from n8n - no rebuild or restart needed!

**Why this works**: Volume mounts and dynamic config loading

### Rebuild After Code Changes

**Scenario**: You've modified source code in `src/chora_compose/` and need to deploy changes.

**Quick method**:
```bash
just docker-rebuild
```

**Manual method**:
```bash
just docker-down
just docker-build
just docker-up
```

**Verify**:
```bash
just docker-logs
# Check for new version, log messages, etc.
```

### Debug MCP Server Issues

**Scenario**: MCP server isn't working as expected.

**Steps**:

1. Check container status:
   ```bash
   just docker-ps
   ```

2. View real-time logs:
   ```bash
   just docker-logs
   ```

3. Open shell in container:
   ```bash
   just docker-shell
   ```

   Inside container:
   ```bash
   # Check package installation
   pip show chora-compose

   # Check environment variables
   env | grep MCP

   # Test Python imports
   python -c "from chora_compose.mcp import server"

   # Check file permissions
   ls -la /app/configs/
   ```

4. Test HTTP endpoint directly:
   ```bash
   curl -v http://localhost:8000/
   curl -N http://localhost:8000/sse
   ```

---

## Related Documentation

**Tutorial**:
- [Tutorial: Docker MCP Deployment](../../tutorials/advanced/03-docker-mcp-deployment.md) - Step-by-step deployment guide

**Explanation**:
- [Explanation: Docker MCP Rationale](../../explanation/deployment/docker-mcp-rationale.md) - Design decisions and architecture

**Reference**:
- [Reference: Docker MCP API](../../reference/deployment/docker-mcp-reference.md) - Complete API specifications

**Other How-Tos**:
- [How-To: Use with Gateway](../mcp/use-with-gateway.md) - Gateway integration
- [How-To: Manage Ephemeral Storage](../storage/manage-ephemeral-storage.md) - Storage management

**External Resources**:
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [n8n MCP Client Node](https://www.npmjs.com/package/n8n-nodes-mcp)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

---

**Need help?** Open an issue on GitHub or consult the troubleshooting section above.
