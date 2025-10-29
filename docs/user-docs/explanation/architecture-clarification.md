# MCP Ecosystem Setup Architecture - Clarification

**Date:** 2025-10-26  
**In Response To:** Victor's setup flow conceptualization

---

## Your Question Summarized

> "I download Docker Desktop, run commands to get mcp-orchestration running, then maybe connect Claude Desktop to mcp-orchestration via custom connector or stdio bridge, then mcp-orchestration sets up mcp-gateway, and then Claude Desktop also connects to gateway... does that sound right?"

## TL;DR Answer

**Almost, but simpler!** Claude Desktop connects to **mcp-gateway ONLY** (one connection). mcp-orchestration runs "behind" the gateway as infrastructure. You never connect directly to orchestration.

---

## Architecture Comparison

### ❌ Your Initial Conceptualization (More Complex)

```
┌─────────────────┐
│ Claude Desktop  │
└──┬───────────┬──┘
   │           │
   │           └──────────┐
   │                      │
   │ Connection 1         │ Connection 2
   │                      │
   ↓                      ↓
┌─────────────────┐   ┌─────────────────┐
│ mcp-orchestr... │   │  mcp-gateway    │
└─────────────────┘   └─────────────────┘
        │                     │
        └──────────┬──────────┘
                   │
                   ↓
        ┌─────────────────────┐
        │ Individual Servers  │
        └─────────────────────┘
```

**Issues:**
- Two connections to manage
- Chicken-and-egg problem (which to set up first?)
- Confusing mental model
- Orchestration exposed to clients

### ✅ Recommended Architecture (Simpler)

```
┌─────────────────┐
│ Claude Desktop  │  ← You configure ONCE
└────────┬────────┘
         │ Single HTTP connection
         │ http://localhost:8679
         ↓
┌──────────────────────────────────────┐
│ Docker: mcp-ecosystem container      │
│                                      │
│  ┌────────────────────────────────┐ │
│  │ mcp-gateway (port 8679)        │ │  ← Public API
│  │ • Aggregates all backends      │ │
│  │ • MCP protocol facade          │ │
│  └───────────────┬────────────────┘ │
│                  │ Internal                  │
│                  ↓                           │
│  ┌────────────────────────────────┐ │
│  │ mcp-orchestration (internal)   │ │  ← Private infrastructure
│  │ • Lifecycle management         │ │
│  │ • Health monitoring            │ │
│  │ • Docker-in-Docker spawning    │ │
│  └───────────────┬────────────────┘ │
└──────────────────┼───────────────────┘
                   │ Spawns sibling containers
                   ↓
         ┌─────────────────────┐
         │ mcp-server-github   │  ← Deployed as needed
         ├─────────────────────┤
         │ mcp-server-coda     │
         ├─────────────────────┤
         │ mcp-server-slack    │
         └─────────────────────┘
```

**Benefits:**
- Single connection point
- Clear layering: gateway = frontend, orchestration = backend
- Orchestration is never exposed to clients
- Simple mental model

---

## Setup Flow Comparison

### Your Proposed Flow

1. Install Docker Desktop ✓
2. Run commands to start mcp-orchestration
3. Connect Claude Desktop to orchestration (custom connector or stdio)
4. mcp-orchestration orchestrates mcp-gateway
5. Connect Claude Desktop to gateway too (custom connector or stdio)
6. Deploy MCP servers
7. For n8n: have n8n connect to orchestration and gateway

### Recommended Flow (Simpler)

1. **Install Docker Desktop** ✓
2. **Run ONE command:**
   ```bash
   docker run -d -p 8679:8679 -v /var/run/docker.sock:/var/run/docker.sock \
     liminalcommons/mcp-ecosystem
   ```
   This starts a single container with BOTH gateway + orchestration
   
3. **Connect Claude Desktop to gateway (ONE connection):**
   - Custom Connector: `http://localhost:8679`
   - Or JSON config with mcp-remote bridge
   
4. **Done!** Now deploy servers:
   ```bash
   docker exec mcp-ecosystem mcp-orchestration deploy mcp-server-github
   ```

---

## Connection Details

### Claude Desktop → Gateway

**Option A: Custom Connector (Recommended)**

Using the UI you showed in the screenshot:
```
Name: Liminal Commons
Remote MCP server URL: http://localhost:8679
Advanced settings: [none needed initially]
```

**Pros:**
- Clean UI
- HTTP native
- No additional tools needed
- Easy to debug

**Option B: JSON Config with mcp-remote Bridge**

```json
{
  "mcpServers": {
    "liminal": {
      "command": "mcp-remote",
      "args": ["http://localhost:8679"]
    }
  }
}
```

**Pros:**
- Familiar to existing MCP users
- Version controllable
- Can be distributed easily

**Cons:**
- Requires mcp-remote tool installed
- stdio → HTTP translation layer
- Extra moving part

### Why NOT Connect to Orchestration?

**mcp-orchestration is infrastructure, not an MCP server.** 

Think of it like:
- **mcp-gateway** = nginx/API Gateway (frontend, clients connect here)
- **mcp-orchestration** = kubernetes/systemd (backend, manages lifecycle)

You wouldn't connect your browser directly to kubernetes, you'd connect to the service exposed through an API gateway. Same principle here.

---

## n8n Integration Architecture

Your intuition about n8n was close but needs clarification on which component connects where.

### Pattern N2: n8n AS Backend (Expose n8n to Claude)

```
Claude Desktop → mcp-gateway → mcp-server-n8n → n8n API
                                 (converts n8n     (running in
                                  to MCP tools)     Docker)
```

**Setup:**
```bash
# Deploy n8n container
docker run -d -p 5678:5678 n8nio/n8n

# Deploy mcp-server-n8n (connects to n8n)
docker exec mcp-ecosystem mcp-orchestration deploy mcp-server-n8n

# Automatically configured to talk to n8n container
# Tools appear in Claude Desktop as: n8n.workflow.execute, n8n.workflow.list, etc.
```

### Pattern N3b: n8n AS Client (n8n calls MCP tools)

```
n8n workflow → mcp-gateway → [any MCP backend]
 (custom MCP    (same gateway     (github, coda,
  client node)   Claude uses)      slack, etc.)
```

**Setup:**
```bash
# In n8n UI, add custom node: @liminalcommons/mcp-client
# Configure node:
#   MCP Gateway URL: http://host.docker.internal:8679
#   (or http://mcp-gateway:8679 if on same Docker network)

# Now n8n workflows can call:
#   - github.repos.search
#   - coda.doc.create  
#   - slack.message.post
#   - ANY tool exposed by gateway
```

**Key Point:** n8n connects to **mcp-gateway**, NOT mcp-orchestration.

### Why This Matters

```
Correct:
  n8n → mcp-gateway → backends

Wrong:
  n8n → mcp-orchestration  (orchestration is not an MCP server!)
```

---

## Bootstrap Container Contents

The `liminalcommons/mcp-ecosystem` container includes:

```dockerfile
FROM ubuntu:24.04

# Install Docker CLI (for Docker-in-Docker spawning)
RUN apt-get update && apt-get install -y docker.io

# Install mcp-gateway
COPY mcp-gateway /usr/local/bin/
EXPOSE 8679

# Install mcp-orchestration
COPY mcp-orchestration /usr/local/bin/

# Supervisor to run both
COPY supervisord.conf /etc/supervisor/conf.d/

# Start script
COPY start.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/start.sh"]
```

**What runs inside:**
- `mcp-gateway` on port 8679 (HTTP)
- `mcp-orchestration` (internal, no exposed port)
- Docker CLI to spawn sibling containers

**Docker socket mount:** `-v /var/run/docker.sock:/var/run/docker.sock`
- Allows container to spawn siblings (other MCP servers)
- Uses Docker-out-of-Docker pattern (not DinD)
- Safer than nested Docker

---

## Ergonomic Improvements Roadmap

### Wave 1 (Q4 2025): Manual Bootstrap

```bash
# User runs:
docker run -d -p 8679:8679 -v /var/run/docker.sock:/var/run/docker.sock \
  liminalcommons/mcp-ecosystem

# User configures Claude Desktop manually
# Custom Connector: http://localhost:8679
```

**Ergonomics: 6/10** (requires Docker + terminal comfort)

### Wave 2 (Q1 2026): CLI Wrapper

```bash
# Install CLI
brew install liminalcommons/tap/mcp

# One command bootstrap
mcp setup

# Automatically:
# ✓ Checks Docker Desktop
# ✓ Starts ecosystem container  
# ✓ Configures Claude Desktop
# ✓ Tests connection
```

**Ergonomics: 8/10** (still requires brew + terminal)

### Wave 3 (Q2 2026): Desktop App

```
Download: LiminalCommonsSetup.dmg
Double-click installer:
  [→] Install Docker Desktop (if needed)
  [→] Start MCP Ecosystem
  [→] Configure Claude Desktop
  [→] Test connection
  [✓] Launch Claude Desktop

Total time: 2 minutes
```

**Ergonomics: 9/10** (one download, one click)

### Wave 4 (Q3+ 2026): Claude Desktop Plugin

```
Claude Desktop → Settings → Plugins
→ Search: "Liminal Commons"
→ Click: Install
→ One-click setup wizard
→ Everything configured automatically
```

**Ergonomics: 10/10** (native integration)

---

## Answers to Your Specific Questions

### Q: "Maybe connecting Claude Desktop to mcp-orchestration uses custom connector?"

**A:** No, connect to **mcp-gateway** instead. Orchestration is backend infrastructure.

### Q: "Perhaps installing mcp-orchestration sets up a bridge?"

**A:** The bootstrap container includes BOTH gateway and orchestration. Gateway is the bridge - it translates MCP protocol to HTTP internally.

### Q: "mcp-orchestration would orchestrate the setup of mcp-gateway?"

**A:** Both start together in the same bootstrap container. No ordering dependency - they're siblings that coordinate.

### Q: "mcp-orchestration appropriately deploying an mcp remote server?"

**A:** mcp-orchestration deploys **backend MCP servers** (github, coda, etc.). The gateway is already running in the bootstrap container.

### Q: "when n8n is running, there would be some steps to have n8n also connect to mcp-orchestration?"

**A:** n8n connects to **mcp-gateway**, not orchestration. n8n is a client (like Claude Desktop), and clients always connect to the gateway.

---

## Mental Model Summary

Think of it like a web application:

```
Browser          → nginx               → app servers
                   (load balancer)       (backends)

Claude Desktop   → mcp-gateway          → MCP servers
                   (aggregator)          (github, coda, etc.)

                   kubernetes            → manages deployments
                   (orchestration)
                   
                   mcp-orchestration     → manages MCP servers
```

**Key principles:**
1. **Clients connect to gateway** (never to orchestration)
2. **Gateway routes to backends** (aggregation layer)
3. **Orchestration manages lifecycle** (infrastructure layer)
4. **Backends provide capabilities** (domain layer)

---

## Implementation Timeline

### Sprint 17 (Now): Document the Vision
- ✅ Capability evolution with waypoints
- ✅ How-to guides for waypoints
- ✅ This architecture clarification

### Sprint 18-20 (Q4 2025): Build Bootstrap
- Create `mcp-ecosystem` Docker image
- Implement basic orchestration (deploy, list, remove)
- Implement gateway auto-discovery
- Test Waypoint W1

### Sprint 21-23 (Q1 2026): Add Lifecycle
- Background updates (Wave 2)
- Health monitoring (Wave 2)
- Hot-reload (Wave 3)
- Test Waypoints W2 & W3

### Sprint 24+ (Q2+ 2026): Improve Ergonomics
- CLI wrapper (`mcp setup`)
- Desktop app installer
- Eventually: Claude Desktop plugin

---

## Files Created

**[View Setup Guide](computer:///mnt/user-data/outputs/how-to-setup-mcp-ecosystem.md)** - Complete 10-minute setup walkthrough

This guide should be completed BEFORE attempting any waypoint guides, as it establishes the foundation.

---

## Questions This Clarifies

✅ **Do I connect Claude Desktop to orchestration?** No, only to gateway  
✅ **Do I need two connections?** No, just one (to gateway)  
✅ **What's the bootstrap flow?** One Docker command, one Claude Desktop config  
✅ **Where does n8n connect?** To gateway (not orchestration)  
✅ **How do backends get deployed?** Orchestration deploys, gateway discovers  
✅ **What's in the bootstrap container?** Both gateway + orchestration  
✅ **Do I need mcp-remote?** Optional, can use custom connector instead

---

**Bottom Line:** Your conceptualization was close, but the key simplification is **single connection to gateway**. Everything else (orchestration, backends) is managed behind the gateway automatically.
