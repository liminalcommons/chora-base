---
title: "How to Set Up the MCP Ecosystem in 10 Minutes"
type: how-to
test_extraction: true
execution_mode: local
e2e_test_id: mcp-ecosystem-initial-setup
audience: end-users
category: setup
last_updated: 2025-10-26
validates:
  - feature: Initial MCP Ecosystem Bootstrap
  - components: [mcp-gateway, mcp-orchestration]
prerequisites_for: 
  - how-to-deploy-new-mcp-server.md (Waypoint W1)
related:
  - docs/explanation/ecosystem-architecture.md
  - docs/how-to/deploy-new-mcp-server.md
---

# How to Set Up the MCP Ecosystem in 10 Minutes

Set up the complete MCP ecosystem (gateway + orchestration) and connect Claude Desktop with a single connection point for all your MCP tools.

## Prerequisites

Before you begin, ensure you have:

- [ ] macOS, Windows, or Linux computer
- [ ] Docker Desktop installed ([download](https://www.docker.com/products/docker-desktop))
- [ ] Claude Desktop installed ([download](https://claude.ai/download))
- [ ] Internet connection for downloading containers
- [ ] Basic familiarity with terminal/command line

## What You'll Do

1. Start Docker Desktop
2. Run the MCP ecosystem bootstrap container
3. Verify the ecosystem is running
4. Connect Claude Desktop to the gateway
5. Test the connection
6. Deploy your first MCP server

## Architecture Overview

```
┌─────────────────┐
│ Claude Desktop  │ (You connect here ONCE)
└────────┬────────┘
         │ HTTP
         ↓
┌─────────────────┐
│  mcp-gateway    │ (Port 8679 - Single entry point)
│  (Aggregator)   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ mcp-orchestr... │ (Background - Lifecycle management)
└────────┬────────┘
         │
         ↓
┌─────────────────────────────────────┐
│ Individual MCP Servers              │
│ (github, coda, n8n, slack, etc.)   │
└─────────────────────────────────────┘
```

**Key Insight:** You only connect Claude Desktop to mcp-gateway. Everything else is managed automatically behind the scenes.

## Steps

### Step 1: Start Docker Desktop

Launch Docker Desktop and wait for it to be ready.

**macOS:**
```bash
open -a Docker
```

**Windows:**
```bash
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

**Linux:**
```bash
systemctl --user start docker-desktop
```

**Expected Output:**
```
Docker Desktop is starting...
Docker Desktop is running
```

**Validation:**
```bash
docker ps && echo "Docker ready"
```

### Step 2: Pull MCP Ecosystem Bootstrap Image

Download the complete ecosystem container image.

**Command:**
```bash
docker pull liminalcommons/mcp-ecosystem:latest
```

**Expected Output:**
```
latest: Pulling from liminalcommons/mcp-ecosystem
a1b2c3d4e5f6: Pull complete
...
Status: Downloaded newer image for liminalcommons/mcp-ecosystem:latest
```

**Validation:**
```bash
docker images | grep mcp-ecosystem && echo "Image downloaded"
```

### Step 3: Start MCP Ecosystem Container

Run the bootstrap container with Docker socket access (for spawning MCP servers).

**Command:**
```bash
docker run -d \
  --name mcp-ecosystem \
  -p 8679:8679 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --restart unless-stopped \
  liminalcommons/mcp-ecosystem:latest
```

**Expected Output:**
```
a7f8e9d0c1b2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8
```

**Validation:**
```bash
docker ps | grep mcp-ecosystem && echo "Container running"
```

### Step 4: Verify Gateway is Responding

Check that mcp-gateway is accepting HTTP connections.

**Command:**
```bash
curl -s http://localhost:8679/health
```

**Expected Output:**
```json
{
  "status": "healthy",
  "gateway_version": "1.2.0",
  "orchestration_version": "1.0.0",
  "backends": 0,
  "uptime": 5
}
```

**Validation:**
```bash
curl -s http://localhost:8679/health | grep -q '"status": "healthy"' && echo "Gateway healthy"
```

### Step 5: View Ecosystem Logs

Check logs to confirm both gateway and orchestration started successfully.

**Command:**
```bash
docker logs mcp-ecosystem --tail 20
```

**Expected Output:**
```
[2025-10-26 23:15:00] Starting MCP Ecosystem Bootstrap...
[2025-10-26 23:15:01] ✓ mcp-gateway started on port 8679
[2025-10-26 23:15:02] ✓ mcp-orchestration started (internal)
[2025-10-26 23:15:03] ✓ Health monitoring enabled
[2025-10-26 23:15:04] ✓ Auto-update service enabled
[2025-10-26 23:15:05] Ready to accept connections
```

**Validation:**
```bash
docker logs mcp-ecosystem | grep -q "Ready to accept connections" && echo "Ecosystem ready"
```

### Step 6: Connect Claude Desktop (Option A - Custom Connector)

Use Claude Desktop's custom connector feature to connect via HTTP.

**Steps:**
1. Open Claude Desktop
2. Go to Settings → Capabilities
3. Click "Add custom connector"
4. Fill in:
   - **Name:** `Liminal Commons`
   - **Remote MCP server URL:** `http://localhost:8679`
5. Click "Add"

**Expected Result:**
```
✓ Connected to Liminal Commons
Status: Healthy
Backends: 0
```

**Validation:**
```bash
# Check Claude Desktop connection in logs
docker logs mcp-ecosystem --tail 5 | grep -q "New MCP client connected" && echo "Claude Desktop connected"
```

### Step 6 (Alternative): Connect Claude Desktop via JSON Config

If you prefer JSON configuration, use mcp-remote to bridge stdio to HTTP.

**Command:**
```bash
cat > ~/.config/claude/config.json <<EOF
{
  "mcpServers": {
    "liminal": {
      "command": "mcp-remote",
      "args": ["http://localhost:8679"],
      "env": {}
    }
  }
}
EOF
```

**Expected Output:**
```
[file created successfully]
```

**Restart Claude Desktop:**
```bash
# macOS
osascript -e 'quit app "Claude"' && sleep 2 && open -a Claude

# Windows
taskkill /IM claude.exe /F && timeout /t 2 && start claude

# Linux
pkill claude && sleep 2 && claude &
```

**Validation:**
```bash
test -f ~/.config/claude/config.json && grep -q "liminal" ~/.config/claude/config.json && echo "Config updated"
```

### Step 7: Verify Connection in Claude Desktop

Ask Claude to list available tools (should be empty initially).

**In Claude Desktop, type:**
```
List all available MCP tools
```

**Expected Response:**
```
Currently, there are no MCP tools available because no backends are deployed yet. 
The MCP gateway is running and ready to discover backends as they're deployed.

To deploy your first backend, you can:
1. Use the CLI: mcp-orchestration deploy mcp-server-github
2. Or ask me to set up a specific integration
```

**Validation:**
```bash
curl -s http://localhost:8679/tools | grep -q '"tools": \[\]' && echo "Connection verified, no tools yet"
```

### Step 8: Deploy Your First MCP Server (GitHub)

Deploy the GitHub integration server to test the complete flow.

**Command:**
```bash
docker exec mcp-ecosystem mcp-orchestration deploy mcp-server-github
```

**Expected Output:**
```
🚀 Deploying mcp-server-github...
✓ Pulling image: liminalcommons/mcp-server-github:latest
✓ Starting container on port 8680
✓ Health check passed
✓ Notifying gateway
✓ Backend registered: github (8 tools)
✓ Deployment complete in 12 seconds
```

**Validation:**
```bash
docker exec mcp-ecosystem mcp-orchestration list | grep -q "github" && echo "GitHub server deployed"
```

### Step 9: Verify Gateway Auto-Discovery

Check that mcp-gateway automatically discovered the GitHub backend.

**Command:**
```bash
curl -s http://localhost:8679/backends
```

**Expected Output:**
```json
{
  "backends": [
    {
      "name": "github",
      "namespace": "github",
      "url": "http://mcp-server-github:8680",
      "status": "connected",
      "health": "healthy",
      "capabilities": {
        "tools": 8,
        "resources": 2,
        "prompts": 0
      },
      "discovered_at": "2025-10-26T23:20:15Z"
    }
  ]
}
```

**Validation:**
```bash
curl -s http://localhost:8679/backends | grep -q '"name": "github"' && echo "GitHub backend discovered"
```

### Step 10: Test GitHub Tools in Claude Desktop

Ask Claude to use a GitHub tool to confirm end-to-end functionality.

**In Claude Desktop, type:**
```
Search GitHub for repositories about "model context protocol"
```

**Expected Response:**
```
I'll search GitHub for repositories about "model context protocol" using the github.repos.search tool.

[Results showing MCP-related repositories with stars, descriptions, etc.]
```

**Validation:**
```bash
curl -s http://localhost:8679/tools | grep -q "github.repos.search" && echo "GitHub tools available"
```

### Step 11: View Complete Ecosystem Status

Check the full ecosystem status including all backends and health.

**Command:**
```bash
docker exec mcp-ecosystem mcp-orchestration status
```

**Expected Output:**
```
┌──────────────────────────────────────────────────────────┐
│          MCP Ecosystem Status                            │
├──────────────────────────────────────────────────────────┤
│ Gateway:         Running (v1.2.0)                        │
│ Orchestration:   Running (v1.0.0)                        │
│ Health Monitor:  Enabled                                 │
│ Auto-Updates:    Enabled                                 │
├──────────────────────────────────────────────────────────┤
│ Backends Deployed:                                       │
│   • github       v1.0.0    healthy    8 tools           │
├──────────────────────────────────────────────────────────┤
│ MCP Clients Connected:                                   │
│   • Claude Desktop (via HTTP)                           │
└──────────────────────────────────────────────────────────┘
```

**Validation:**
```bash
docker exec mcp-ecosystem mcp-orchestration status | grep -q "github.*healthy" && echo "Ecosystem fully operational"
```

## Troubleshooting

### Docker Socket Permission Denied (Linux)

**Cause:** Docker socket requires specific permissions

**Fix:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or use sudo for docker commands
sudo docker run -d ...
```

### Port 8679 Already in Use

**Cause:** Another service is using port 8679

**Fix:**
```bash
# Find what's using the port
lsof -i :8679

# Stop the mcp-ecosystem container and use different port
docker stop mcp-ecosystem
docker rm mcp-ecosystem
docker run -d --name mcp-ecosystem -p 8680:8679 ...

# Update Claude Desktop to use http://localhost:8680
```

### Gateway Health Check Fails

**Cause:** Container didn't start properly

**Fix:**
```bash
# Check container logs
docker logs mcp-ecosystem

# Common issues:
# - Docker socket not mounted: Add -v /var/run/docker.sock:/var/run/docker.sock
# - Port conflict: Change -p 8679:8679 to different port
# - Image pull failed: Check internet connection

# Restart container
docker restart mcp-ecosystem
```

### Claude Desktop Can't Connect

**Cause:** Firewall or network configuration

**Fix:**
```bash
# Test connection manually
curl http://localhost:8679/health

# If that works, issue is in Claude Desktop config
# Check ~/.config/claude/config.json syntax

# Try custom connector instead of JSON config
# (See Step 6 Option A)
```

### Backend Deployment Fails

**Cause:** Image not available or Docker socket issues

**Fix:**
```bash
# Check orchestration logs
docker exec mcp-ecosystem mcp-orchestration logs

# Manually test Docker-in-Docker
docker exec mcp-ecosystem docker ps

# If "docker: command not found":
# Recreate with proper Docker socket mount
docker stop mcp-ecosystem
docker rm mcp-ecosystem
# Re-run Step 3 with correct -v flag
```

## What's Running?

After completing this setup, you have:

```
┌─────────────────────────────────────────────────┐
│ Docker Desktop                                  │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ mcp-ecosystem (container)                 │ │
│  │  ├─ mcp-gateway (port 8679)               │ │
│  │  └─ mcp-orchestration (internal)          │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ mcp-server-github (container)             │ │
│  │  └─ GitHub API integration                │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  [More MCP servers as you deploy them...]     │
└─────────────────────────────────────────────────┘
```

**Single Connection:** Claude Desktop → `http://localhost:8679` (gateway) → all backends

## Next Steps

Now that your ecosystem is set up, you can:

1. **Deploy more MCP servers:**
   ```bash
   docker exec mcp-ecosystem mcp-orchestration deploy mcp-server-coda
   docker exec mcp-ecosystem mcp-orchestration deploy mcp-server-slack
   ```

2. **Follow Waypoint W1:**
   See [How to Deploy a New MCP Server in 5 Minutes](how-to-deploy-new-mcp-server.md)

3. **Enable automatic updates:**
   See [How to Enable Automatic MCP Server Updates](how-to-enable-automatic-updates.md)

4. **Configure health monitoring:**
   See [How to Configure Health Monitoring](how-to-configure-health-monitoring.md)

5. **Explore available servers:**
   ```bash
   docker exec mcp-ecosystem mcp-orchestration catalog
   ```

## Uninstalling

To completely remove the MCP ecosystem:

**Command:**
```bash
# Stop and remove containers
docker stop mcp-ecosystem
docker rm mcp-ecosystem

# Remove deployed MCP servers
docker rm $(docker ps -a -q -f "label=mcp.ecosystem=liminalcommons")

# Remove images (optional)
docker rmi liminalcommons/mcp-ecosystem

# Remove Claude Desktop config
rm ~/.config/claude/config.json
# Or manually remove "liminal" entry if you have other MCP servers
```

**Validation:**
```bash
docker ps -a | grep -q mcp-ecosystem || echo "Ecosystem removed"
```

## See Also

- [Ecosystem Architecture](../explanation/ecosystem-architecture.md)
- [mcp-gateway Documentation](../mcp-gateway/README.md)
- [mcp-orchestration Documentation](../mcp-orchestration/README.md)
- [Waypoint W1: Deploy New Servers](how-to-deploy-new-mcp-server.md)

## Success Metrics

This guide achieves initial setup when:

- ✅ Docker Desktop running
- ✅ mcp-ecosystem container started
- ✅ Gateway responding on port 8679
- ✅ Claude Desktop connected to gateway
- ✅ At least one backend deployed and discovered
- ✅ Tools available in Claude Desktop
- ✅ Complete setup in <10 minutes

**Note:** This is the prerequisite for all waypoint guides. Once this setup is complete, you can follow the waypoint how-to guides to validate advanced integration patterns.
