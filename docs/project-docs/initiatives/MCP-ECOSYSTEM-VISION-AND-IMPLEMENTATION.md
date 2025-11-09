# MCP Ecosystem: Vision and Implementation Guide

**Version**: 1.0.0
**Status**: Approved
**Date Created**: 2025-11-03
**Document Type**: Vision & Implementation Guide
**Trace ID**: CHORA-COORD-2025-003

**Purpose**: This document synthesizes the complete vision, design principles, and implementation roadmap for the chora-workspace MCP ecosystem lifecycle automation. It serves as the single source of truth for understanding and implementing the full vision.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [The Vision](#the-vision)
3. [Core Architecture](#core-architecture)
4. [Key Principles](#key-principles)
5. [The 12-Step Lifecycle](#the-12-step-lifecycle)
6. [Automation Maturity Path](#automation-maturity-path)
7. [16-Week Phased Roadmap](#16-week-phased-roadmap)
8. [Implementation Details](#implementation-details)
9. [Getting Started](#getting-started)
10. [References](#references)

---

## Executive Summary

### The Transformation

We are building an end-to-end MCP server lifecycle automation system that transforms the process of creating, deploying, and managing MCP servers from a multi-day manual process into a **5-10 minute automated workflow**.

**Current State (Manual)**:
```
User intent → Manual project setup (2 days) → Manual coding (1-2 weeks) →
Manual deployment → Manual client config → Operational
```

**Target State (Automated)**:
```
User intent → MCP tool calls via gateway (5-10 min) →
Operational and discoverable
```

### What This Enables

1. **Developer Productivity**: Create production-ready MCP servers in minutes, not weeks
2. **Client Flexibility**: Use ANY tool (Claude Code, n8n, Python, Bash) to orchestrate
3. **Auto-Discovery**: New servers automatically available to all clients
4. **Quality Standards**: AI-generated code following best practices
5. **Scalable Ecosystem**: Support 100+ MCP servers with minimal overhead

### The Key Innovation

**Unified Gateway Architecture**: ALL clients connect to a single mcp-gateway that routes to ALL servers. This client-agnostic design means the same 12 MCP tool calls work identically whether invoked from Claude Code, n8n, Python scripts, or Bash.

```
Claude Desktop ──┐
Claude Code ─────┼─→ mcp-gateway (localhost:8679) ─┬─→ chora-compose
n8n ─────────────┤                                  ├─→ mcp-orchestration
Python scripts ──┤                                  ├─→ mcp-server-n8n
Bash scripts ────┘                                  └─→ mcp-server-github
```

### Timeline

- **v1.0 (Manual, Today)**: ~30 min, 40% automated - Documentation complete
- **v2.0 (Semi-Auto, Q1 2026)**: ~10 min, 70% automated - n8n orchestration
- **v3.0 (Fully Auto, Q2 2026)**: ~5 min, 95% automated - AI-driven implementation

### Success Metrics

- **Time to Production**: From 2 weeks → 10 minutes (99% reduction)
- **Cost**: $0.50 API fees vs $1,200 developer time (99.96% reduction)
- **Quality**: Consistent AI-generated code following best practices
- **Scale**: Support 100+ MCP servers (vs ~5 manageable manually)

---

## The Vision

### The Problem We're Solving

Creating and deploying MCP servers today is fragmented and manual:

1. **Deployment**: Manual Docker commands, custom scripts
2. **Discovery**: Configure each client individually (Claude, n8n)
3. **Tool Access**: Different patterns per client
4. **State Management**: No single source of truth
5. **Health Monitoring**: Ad-hoc checks, no automation

This creates:
- **Client Lock-In**: Each client needs custom integration
- **Configuration Drift**: Multiple configs out of sync
- **Poor DX**: Complex setup for new servers
- **Limited Automation**: Hard to orchestrate workflows
- **Scalability Issues**: Manual processes don't scale

### The Solution

A **unified MCP ecosystem** with:

1. **Single Entry Point** (mcp-gateway): ALL clients → one endpoint → ALL servers
2. **Source of Truth** (ecosystem-manifest): Declarative registry of all servers
3. **Lifecycle Automation** (chora-compose): AI-powered code generation
4. **Deployment Manager** (mcp-orchestration): Docker lifecycle management
5. **Client-Agnostic Design**: Same tool calls work across Claude, n8n, Python, Bash

### The Vision Statement

> **"If there is a way that we can have our full lifecycle from chora-base through MCP server development through CI/CD, end to end testing, release, publishing, ops, and provisioning... i mean that is a really cool vision"**
>
> — Vision articulated during architecture discussions

We envision:

- **MCP orchestration** managing the full server lifecycle
- **Unified mcp-gateway** presenting capabilities with well-designed namespacing
- **Easy discovery** - clients can find and use what's available
- **Eventually run it in n8n** - full automation via visual workflows
- **Leverage code generation** - chora-compose goes beyond boilerplate to implementation

### What Success Looks Like

**For Developers**:
- Say "Create a task management MCP server" in Claude Code
- 10 minutes later: Production-ready server deployed, tested, documented
- Use immediately: `taskmgr.create("Review docs", "high")`

**For Platform Engineers**:
- Add entry to `registry.yaml`
- Auto-discovered by gateway
- Auto-deployed via orchestration
- Auto-available to all clients

**For End Users**:
- New capabilities appear automatically
- Consistent interface across clients
- High quality, tested tools

---

## Core Architecture

### Unified Gateway Pattern

The cornerstone of our architecture is the **unified gateway** - a single entry point for ALL MCP interactions.

#### Architecture Diagram

```
┌───────────────────────────────────────────────────────────────┐
│                    MCP CLIENTS                                │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Claude Code  │  │ Claude       │  │     n8n      │       │
│  │              │  │  Desktop     │  │              │       │
│  │ (Interactive)│  │(Conversational)│ │  (Automated) │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                  │                  │               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │    Python    │  │   Bash       │  │   Custom     │       │
│  │   Scripts    │  │   Scripts    │  │   Clients    │       │
│  │  (Batch)     │  │   (CLI)      │  │              │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
└─────────┼──────────────────┼──────────────────┼───────────────┘
          │                  │                  │
          │     All clients connect to single endpoint
          │                  │                  │
          └──────────────────┼──────────────────┘
                             ↓
              ┌──────────────────────────────┐
              │       mcp-gateway            │
              │    (localhost:8679)          │
              │                              │
              │  • Auto-discovery (registry) │
              │  • Health-aware routing      │
              │  • Namespace management      │
              │  • Load balancing            │
              │  • Fail-over                 │
              └──────────────┬───────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ↓                  ↓                  ↓
┌─────────────────────────────────────────────────────────────┐
│                    MCP SERVERS                              │
│                                                             │
│  ┌────────────────────┐  ┌────────────────────┐           │
│  │  chora-compose     │  │ mcp-orchestration  │           │
│  │  (Generation)      │  │  (Deployment)      │           │
│  │                    │  │                    │           │
│  │ Tools:             │  │ Tools:             │           │
│  │ • bootstrap_project│  │ • deploy_server    │           │
│  │ • generate_code    │  │ • health_check     │           │
│  │ • regenerate_      │  │ • scale_server     │           │
│  │   configs          │  │ • update_server    │           │
│  │ Namespace:         │  │ Namespace:         │           │
│  │  chora-compose.*   │  │  orchestration.*   │           │
│  └────────────────────┘  └────────────────────┘           │
│                                                             │
│  ┌────────────────────┐  ┌────────────────────┐           │
│  │  mcp-server-n8n    │  │ mcp-server-github  │           │
│  │  (Workflows)       │  │  (GitHub API)      │           │
│  │                    │  │                    │           │
│  │ Tools:             │  │ Tools:             │           │
│  │ • trigger_workflow │  │ • create_repo      │           │
│  │ • list_workflows   │  │ • commit_files     │           │
│  │ • get_execution    │  │ • tag_release      │           │
│  │ Namespace:         │  │ Namespace:         │           │
│  │  n8n.*             │  │  github.*          │           │
│  └────────────────────┘  └────────────────────┘           │
│                                                             │
│  ┌────────────────────┐                                    │
│  │ ecosystem-manifest │                                    │
│  │  (Registry)        │                                    │
│  │                    │                                    │
│  │ Tools:             │                                    │
│  │ • register_server  │                                    │
│  │ • list_servers     │                                    │
│  │ • update_registry  │                                    │
│  │ Namespace:         │                                    │
│  │  ecosystem.*       │                                    │
│  └────────────────────┘                                    │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. mcp-gateway (Universal Router)

**Purpose**: Single entry point for ALL MCP clients to access ALL MCP servers

**Key Features**:
- REST API for tool discovery: `GET /tools`
- REST API for tool invocation: `POST /tools/{namespace}/{tool}`
- Health-aware routing (auto-failover to healthy instances)
- Auto-discovery from ecosystem-manifest registry
- Namespace-based routing: `namespace.tool_name → server`
- Load balancing across multiple server instances

**Status**: Planned (Phase 4, Weeks 9-12)

#### 2. ecosystem-manifest (Source of Truth)

**Purpose**: Declarative registry of all MCP servers in the ecosystem

**Key Features**:
- Single YAML file: `registry.yaml`
- Schema-validated server definitions
- Versioned entries (semver)
- Metadata for discovery and filtering
- Health check configuration
- Deployment specifications

**Registry Entry Example**:
```yaml
servers:
  - name: mcp-server-taskmgr
    namespace: taskmgr
    description: Task management MCP server with CRUD operations
    endpoint: http://localhost:8082
    health_url: http://localhost:8082/health
    capabilities:
      - task-management
      - persistence
    tools:
      - name: taskmgr.create
        description: Create a new task
      - name: taskmgr.list
        description: List all tasks
      - name: taskmgr.update
        description: Update an existing task
      - name: taskmgr.delete
        description: Delete a task
    quality_tier: gold
    version: 0.1.0
    docker_image: liminalcommons/mcp-server-taskmgr:0.1.0
    repository: https://github.com/liminalcommons/mcp-server-taskmgr
    maintainers:
      - chora-workspace
    health_spec_version: "1.0"
```

**Status**: Planned (Phase 2, Weeks 3-4)

#### 3. chora-compose (Generation Engine)

**Purpose**: AI-powered MCP server generation from intent to implementation

**Key Features**:
- **3-Tier Generation Architecture**:
  - Content Layer: Files (Jinja2, AI code generation, inline)
  - Artifact Layer: Multi-file units (dependency tracking)
  - Collection Layer: Full projects (SAP template integration)
- **AI Code Generation** (CodeGenerationGenerator):
  - 499 lines production code
  - Claude API integration
  - Token tracking, cost calculation
  - Retry with exponential backoff
  - Fallback templates
- **Incremental Regeneration**: 180x efficiency via dependency tracking
- **SAP-003 Templates**: FastMCP server structure

**Tools**:
- `chora-compose.bootstrap_project`: Generate project structure
- `chora-compose.generate_code`: AI-powered implementation
- `chora-compose.regenerate_configs`: Update client configs from registry

**Status**: ✅ Production (v3.2.0+)

#### 4. mcp-orchestration (Deployment Manager)

**Purpose**: Deploy, monitor, and manage MCP server lifecycle

**Key Features**:
- Docker-based deployment
- Health monitoring and auto-recovery
- Resource management (CPU, memory limits)
- Volume and network management
- Multi-instance support (load balancing)
- Graceful shutdown and upgrades

**Tools**:
- `orchestration.deploy_server`: Deploy from Docker image
- `orchestration.health_check`: Check server health
- `orchestration.scale_server`: Scale instances
- `orchestration.restart_server`: Restart unhealthy servers
- `orchestration.stop_server`: Graceful shutdown

**Status**: Planned (Phase 3, Weeks 5-8)

#### 5. mcp-server-n8n (Workflow Integration)

**Purpose**: Expose n8n workflows as MCP tools (n8n as server)

**Pattern N2**: `ANY client → mcp-gateway → mcp-server-n8n → n8n API`

**Tools**:
- `n8n.trigger_workflow`: Execute n8n workflow
- `n8n.list_workflows`: List available workflows
- `n8n.check_execution`: Check workflow execution status

**Status**: Planned (Phase 5, Weeks 13-16)

#### 6. n8n MCP Gateway Node (n8n as Client)

**Purpose**: Enable n8n workflows to call MCP servers (n8n as client)

**Pattern N3b**: `n8n workflow → mcp-gateway → ANY MCP server`

**Custom Node**: `@chora/n8n-node-mcp-gateway`

**Operations**:
- List Tools: Discover available MCP tools
- Call Tool: Invoke MCP tool via gateway
- Health Check: Check gateway and server health

**Status**: Planned (Phase 5, Weeks 13-16)

### n8n Dual Role

n8n uniquely serves **TWO roles** in the ecosystem:

1. **Pattern N2 (n8n as Server)**: Other clients call n8n workflows via mcp-server-n8n
2. **Pattern N3b (n8n as Client)**: n8n workflows call other MCP servers via gateway

**Recursive Pattern**: n8n can call itself via gateway
```
n8n workflow A → mcp-gateway → mcp-server-n8n → n8n workflow B
```

This enables:
- Workflow composition (build complex from simple)
- Meta-orchestration (workflow of workflows)
- Versioned sub-workflows
- Abstraction (n8n doesn't know it's calling itself)

---

## Key Principles

### 1. Unified Gateway Architecture

**Principle**: ALL clients connect to mcp-gateway (single connection point)

**Rationale**:
- Eliminates O(N×M) configuration problem (N clients × M servers)
- Single source of truth for discovery
- Health-aware routing
- Future-proof (new clients just need HTTP)

**Implementation**:
```
Claude Desktop:   http://localhost:8679
Claude Code:      http://localhost:8679
n8n:              http://localhost:8679
Python scripts:   http://localhost:8679
Bash scripts:     http://localhost:8679
```

### 2. Client-Agnostic Design

**Principle**: Same MCP tool calls work identically across ALL clients

**Rationale**:
- Consistent developer experience
- Portable workflows
- Client choice flexibility
- Documentation once, use everywhere

**Example**: Create GitHub repo (same across all clients)
```python
# Python
gateway.call("github.create_repo", name="mcp-server-taskmgr")

# Bash
curl -X POST http://localhost:8679/tools/github/create_repo \
     -d '{"name":"mcp-server-taskmgr"}'

# Claude Code
"Create a GitHub repo named mcp-server-taskmgr"
# → Calls github.create_repo via gateway

# n8n
{
  "operation": "callTool",
  "toolName": "github.create_repo",
  "parameters": {"name": "mcp-server-taskmgr"}
}
```

### 3. Namespace Isolation

**Principle**: Tools namespaced to prevent collisions

**Format**: `namespace.tool_name`

**Examples**:
- `chora-compose.bootstrap_project`
- `orchestration.deploy_server`
- `github.create_repo`
- `n8n.trigger_workflow`
- `taskmgr.create`

**Benefits**:
- Prevents tool name conflicts
- Clear ownership (namespace → server)
- Easy routing (gateway maps namespace → endpoint)
- Discoverability (list all `github.*` tools)

### 4. Declarative Registry

**Principle**: `registry.yaml` is the single source of truth

**Rationale**:
- Version controlled (Git history)
- Schema validated
- Human readable
- Machine parseable
- Single update propagates to all clients

**Workflow**:
1. Add server to `registry.yaml`
2. Commit to ecosystem-manifest repo
3. Gateway auto-discovers (polls every 60s)
4. Clients refresh tools (GET /tools)
5. New tools available everywhere

### 5. Health-Aware Routing

**Principle**: Gateway only routes to healthy servers

**Implementation**:
- Each server exposes `/health` endpoint
- Gateway polls health every 30s
- Unhealthy servers removed from routing table
- Auto-failover to healthy instances
- Health status exposed via GET /health

**Health Endpoint Spec** (from ecosystem-manifest):
```json
{
  "status": "healthy",        // or "unhealthy"
  "version": "0.1.0",
  "uptime_seconds": 3600,
  "dependencies": [
    {"name": "postgres", "status": "healthy"},
    {"name": "redis", "status": "healthy"}
  ],
  "tools_available": 4,
  "health_spec_version": "1.0"
}
```

### 6. Incremental Automation

**Principle**: v1.0 (manual) → v2.0 (semi-auto) → v3.0 (full-auto)

**Rationale**:
- Deliver value early (v1.0 manual workflow useful today)
- Learn from each phase
- Avoid over-engineering
- Incremental investment

**Phases**:
- **v1.0**: Documentation + manual execution (Ship now)
- **v2.0**: n8n orchestration + workflow templates (Q1 2026)
- **v3.0**: AI-driven implementation + continuous deployment (Q2 2026)

### 7. AI-Powered Implementation

**Principle**: chora-compose generates implementation, not just boilerplate

**Rationale**:
- Faster time to production (minutes vs hours)
- Consistent quality (follows best practices)
- Cost-effective ($0.50 API vs $1,200 labor)
- Enables v3.0 full automation

**Implementation**:
- `CodeGenerationGenerator`: 499 lines production code
- Claude API integration (Sonnet 4.5)
- Natural language prompts
- Type hints, docstrings, error handling
- Token tracking, cost calculation

### 8. Observable by Default

**Principle**: All interactions logged, traced, metered

**Implementation**:
- **CHORA_TRACE_ID**: Every request tagged with trace ID
- **OpenTelemetry**: Distributed tracing across components
- **Prometheus**: Metrics (request count, latency, errors)
- **Structured Logging**: JSON logs for easy parsing

**Example Trace**:
```
CHORA_TRACE_ID: CHORA-COORD-2025-003

1. Client → mcp-gateway: chora-compose.bootstrap_project
2. Gateway → chora-compose: bootstrap_project
3. chora-compose → Jinja2: render templates
4. chora-compose → Response (17 files created)
5. Gateway → Client: Success
```

---

## The 12-Step Lifecycle

The MCP server lifecycle is a **sequence of MCP tool calls** orchestrated by any client via mcp-gateway. This section provides a high-level overview; see [LIFECYCLE-STEPS-DETAILED.md](lifecycle/LIFECYCLE-STEPS-DETAILED.md) for exhaustive details.

### Lifecycle Overview Table

| Step | MCP Tool | Purpose | Time | Status |
|------|----------|---------|------|--------|
| **1** | `chora-compose.bootstrap_project` | Create project structure (17 files) | 30s | ✅ Ready |
| **2** | `chora-compose.generate_code` | AI-powered implementation (5 files) | 3 min | ✅ Ready |
| **3** | `github.create_repo` | Create GitHub repository | 5s | ⚠️ Needs mcp-server-github |
| **4** | `github.commit_files` | Commit generated files | 15s | ⚠️ Needs mcp-server-github |
| **5** | `n8n.trigger_workflow` | Run CI/CD pipeline (pytest, Docker build) | 5-10 min | ⚠️ Needs mcp-server-n8n |
| **6** | `ecosystem.register_server` | Add to registry.yaml | 5s | ⚠️ Needs implementation |
| **7** | `chora-compose.regenerate_configs` | Update client configs from registry | 10s | ✅ Ready |
| **8** | `orchestration.deploy_server` | Deploy Docker container | 30s | ⚠️ Needs MCP wrapper |
| **9** | `orchestration.health_check` | Verify deployment healthy | 5s | ⚠️ Needs MCP wrapper |
| **10** | `mcp-gateway` auto-discovery | Gateway discovers new server (automatic) | 0-60s | ⚠️ Needs implementation |
| **11** | Client refresh | Client queries updated tool list (GET /tools) | 1s | ✅ Ready |
| **12** | Use new tools | Client calls new server's tools (e.g., `taskmgr.create`) | <1s | ✅ Ready |

**Total Time**:
- **Interactive (Claude Code)**: 25-30 min (includes human review)
- **Automated (n8n)**: 8-10 min (no human in loop)
- **Programmatic (Python)**: 7-8 min (optimized)

**Bottleneck**: Step 5 (CI/CD) takes 5-10 minutes (pytest + Docker build)

### Step-by-Step Walkthrough

#### Step 1: Bootstrap Project Structure

**Tool**: `chora-compose.bootstrap_project`

**Purpose**: Generate complete MCP server project structure using SAP-003 templates

**Input**:
```json
{
  "namespace": "taskmgr",
  "description": "Task management MCP server with CRUD operations",
  "tools": ["create", "list", "update", "delete"],
  "template_source": "SAP-003",
  "framework": "fastmcp"
}
```

**Output**:
```json
{
  "status": "success",
  "project_path": "mcp-server-taskmgr/",
  "files_created": [
    "src/mcp_server_taskmgr/server.py",
    "src/mcp_server_taskmgr/tools/create.py",
    "src/mcp_server_taskmgr/tools/list.py",
    "tests/test_tools.py",
    "Dockerfile",
    ".github/workflows/test.yml",
    "README.md"
    // ... 10 more files
  ],
  "structure": {
    "total_files": 17,
    "total_lines": 523,
    "sap_compliance": "100%"
  }
}
```

**What's Generated**:
- FastMCP server boilerplate
- Tool stubs (4 tools)
- Health endpoint (ecosystem-manifest compliant)
- Docker configuration (multi-stage, multi-arch)
- CI/CD workflows (GitHub Actions)
- Test scaffolding (pytest)
- Documentation (README, docstrings)

#### Step 2: Generate Implementation Code

**Tool**: `chora-compose.generate_code`

**Purpose**: Use AI to generate production-quality implementation code

**Input**:
```json
{
  "file": "src/mcp_server_taskmgr/tools/create.py",
  "language": "python",
  "prompt": "Generate a function to create a new task with validation. Include:\n- Input: title (str), description (str), priority (enum: low/medium/high), due_date (optional datetime)\n- Validation: title required, max 200 chars\n- Generate UUID\n- Store in SQLite database (table: tasks)\n- Return created task as dict\n- Include type hints and docstrings",
  "style_hints": [
    "Use Python 3.12+ type hints",
    "Follow PEP 8",
    "Use FastMCP @mcp.tool() decorator"
  ]
}
```

**Output**:
```json
{
  "status": "success",
  "code": "import uuid\nfrom datetime import datetime\nfrom typing import Optional\nfrom fastmcp import FastMCP\n\nmcp = FastMCP(\"taskmgr\")\n\n@mcp.tool()\ndef create(title: str, description: str, priority: str = \"medium\", due_date: Optional[str] = None) -> dict:\n    \"\"\"Create a new task...",
  "tokens": {
    "input": 423,
    "output": 512,
    "total": 935
  },
  "cost": {
    "usd": 0.0089
  },
  "model": "claude-3-5-sonnet-20241022"
}
```

**Cost Analysis** (5 files generated):
- Total cost: $0.20-$0.50
- Time saved: ~10 hours manual coding
- ROI: 240,000% (cost-based)

#### Step 3-5: GitHub & CI/CD

**Step 3**: `github.create_repo` - Create GitHub repository
**Step 4**: `github.commit_files` - Commit all 17 generated files
**Step 5**: `n8n.trigger_workflow` - Trigger CI/CD pipeline (tests, Docker build, push to registry)

**CI/CD Workflow** (GitHub Actions):
1. Run pytest (target: 85% coverage)
2. Build Docker image (multi-stage, multi-arch: amd64, arm64)
3. Push to Docker Hub: `liminalcommons/mcp-server-taskmgr:0.1.0`
4. Tag release on GitHub

**Duration**: 5-10 minutes (bottleneck)

#### Step 6-7: Registry & Config

**Step 6**: `ecosystem.register_server` - Add to `ecosystem-manifest/registry.yaml`
**Step 7**: `chora-compose.regenerate_configs` - Update `claude_desktop_config.json` from registry

**Registry Entry Created**:
```yaml
servers:
  - namespace: taskmgr
    name: mcp-server-taskmgr
    version: 0.1.0
    docker_image: liminalcommons/mcp-server-taskmgr:0.1.0
    tools: [taskmgr.create, taskmgr.list, taskmgr.update, taskmgr.delete]
    health_url: http://localhost:8082/health
```

**Config Generated** (claude_desktop_config.json):
```json
{
  "mcpServers": {
    "liminal-gateway": {
      "url": "http://localhost:8679",
      "servers": [
        {"namespace": "chora-compose", "tools": 22},
        {"namespace": "orchestration", "tools": 8},
        {"namespace": "taskmgr", "tools": 4}
      ]
    }
  }
}
```

#### Step 8-9: Deploy & Verify

**Step 8**: `orchestration.deploy_server` - Deploy Docker container
**Step 9**: `orchestration.health_check` - Verify deployment

**Deployment**:
```json
{
  "server_name": "mcp-server-taskmgr",
  "image": "liminalcommons/mcp-server-taskmgr:0.1.0",
  "port": 8082,
  "environment": {
    "DATABASE_URL": "sqlite:///data/tasks.db",
    "LOG_LEVEL": "info"
  },
  "health_check": {
    "endpoint": "/health",
    "interval": "10s",
    "timeout": "5s",
    "retries": 3
  }
}
```

**Health Check Response**:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "uptime_seconds": 12,
  "tools_available": 4,
  "health_spec_version": "1.0"
}
```

#### Step 10-12: Discover & Use

**Step 10**: mcp-gateway auto-discovery (automatic, polls registry every 60s)
**Step 11**: Client refresh (`GET /tools`)
**Step 12**: Use new tools

**Client Usage** (Claude Code):
```
User: "Create a task to review lifecycle documentation"

Claude Code: I'll create a task using the new taskmgr server.
[Calls: mcp-gateway/taskmgr.create]

Claude Code: ✓ Task created successfully

Task ID: 550e8400-e29b-41d4-a716-446655440000
Title: Review lifecycle documentation
Priority: high
Created: 2025-11-03T11:00:00Z
```

### Client-Agnostic Examples

The SAME lifecycle can be orchestrated via ANY client:

**Claude Code** (Interactive):
```
User: "Create a task management MCP server"
Claude: [Orchestrates 12 steps with human feedback at each stage]
Time: ~25-30 min
```

**n8n** (Automated):
```json
{
  "name": "MCP Server Lifecycle - Automated",
  "nodes": [
    {"name": "Step 1: Bootstrap", "type": "mcpGateway", ...},
    {"name": "Step 2: Generate Code", "type": "mcpGateway", ...},
    {"name": "Step 3: Create Repo", "type": "mcpGateway", ...},
    // ... 9 more nodes
  ]
}
```
Time: ~8-10 min (fully automated)

**Python** (Programmatic):
```python
from mcp_client import Gateway

gateway = Gateway("http://localhost:8679")

# Step 1: Bootstrap
result = gateway.call("chora-compose.bootstrap_project",
    namespace="taskmgr",
    tools=["create", "list", "update", "delete"]
)

# Step 2: Generate code
gateway.call("chora-compose.generate_code", ...)

# Steps 3-12...
```
Time: ~7-8 min (batch mode)

---

## Automation Maturity Path

We deliver incrementally across three automation tiers:

### v1.0: Manual Workflow (Ship Now)

**Timeline**: Today (Nov 2025)
**Time to Create MCP Server**: ~30 minutes
**Automation**: 40%

**What's Automated**:
- ✅ Code generation (chora-compose AI)
- ✅ Template filling (Jinja2)
- ✅ CI/CD pipelines (GitHub Actions)
- ✅ Docker builds (multi-stage, multi-arch)

**What's Manual**:
- ❌ Project bootstrap (copy template manually)
- ❌ GitHub repo creation (web UI or `gh` CLI)
- ❌ Registry update (edit YAML file, commit)
- ❌ Client config update (manual regeneration)
- ❌ Deployment (docker-compose up)

**Workflow**:
1. Developer follows documentation
2. Runs chora-compose tools via Claude Code
3. Manually creates GitHub repo
4. Manually updates registry
5. Runs chora-compose to regenerate configs
6. Deploys via docker-compose

**Status**: ✅ Documentation complete, ready to implement

**Success Criteria**:
- [ ] User can create MCP server in <30 min following docs
- [ ] Documentation covers all 12 lifecycle steps
- [ ] Examples demonstrate 3+ client types
- [ ] BDD scenarios validate workflow end-to-end

### v2.0: Semi-Automated (Q1 2026)

**Timeline**: Weeks 9-16 (after Phase 4-5 completion)
**Time to Create MCP Server**: ~10 minutes
**Automation**: 70%

**Additional Automation**:
- ✅ Project bootstrap via MCP tool (`chora-compose.bootstrap_project`)
- ✅ GitHub integration via MCP server (`mcp-server-github`)
- ✅ Registry update via MCP tool (`ecosystem.register_server`)
- ✅ Deployment via orchestration (`orchestration.deploy_server`)
- ✅ n8n orchestration workflows (visual automation)

**What's Manual**:
- ❌ Code review before deployment (human judgment)
- ❌ Manual approval for production deploy (governance)
- ❌ Custom implementation beyond boilerplate (complex logic)

**Workflow**:
1. Developer triggers n8n workflow OR runs Python script
2. Automated steps 1-9 (bootstrap through health check)
3. Manual review of generated code
4. Manual approval to deploy
5. Automated deployment

**Key Deliverables**:
- mcp-gateway at localhost:8679
- ecosystem-manifest registry with 5+ servers
- mcp-orchestration Docker lifecycle management
- mcp-server-github (GitHub API wrapper)
- mcp-server-n8n (n8n workflow wrapper)
- @chora/n8n-node-mcp-gateway (custom n8n node)
- n8n workflow templates for lifecycle automation

**Success Criteria**:
- [ ] User can create MCP server in <10 min (n8n workflow)
- [ ] n8n workflow JSON templates available
- [ ] GitHub, ecosystem, orchestration MCP servers operational
- [ ] Zero manual file edits (all via MCP tools)
- [ ] Batch creation: 10 servers in <90 min

### v3.0: Fully Automated (Q2 2026)

**Timeline**: Post Phase 5 (16+ weeks)
**Time to Create MCP Server**: ~5 minutes
**Automation**: 95%

**Additional Automation**:
- ✅ AI-driven implementation (not just boilerplate, full logic)
- ✅ Automated test generation (pytest + scenarios)
- ✅ Automated code review (AI + linters + security scans)
- ✅ Continuous deployment with rollback
- ✅ Auto-scaling based on usage

**What's Manual**:
- ❌ High-level design decisions (architecture choices)
- ❌ Complex business logic (domain-specific rules)
- ❌ Edge case handling (unexpected scenarios)

**Workflow**:
1. User provides intent: "Create expense tracking MCP server with receipt OCR"
2. AI generates full implementation (tests, docs, deploy configs)
3. Automated review + security scan
4. Automated deployment with canary release
5. MCP server live in 5 minutes

**Key Enhancements**:
- Multi-turn AI refinement (generate → test → refine loop)
- Syntax validation (parse code before deploying)
- Integration testing (automated end-to-end tests)
- Performance benchmarking (latency, throughput)
- Cost optimization (right-sizing resources)

**Success Criteria**:
- [ ] User can create MCP server in <5 min (AI-driven)
- [ ] Generated code passes 85%+ test coverage
- [ ] Automated deployment with rollback on failure
- [ ] AI code review provides actionable feedback
- [ ] 95% automation rate (only strategic decisions manual)

### ROI Analysis

**Scenario**: Create MCP server with 5 implementation files

| Metric | v1.0 Manual | v2.0 Semi-Auto | v3.0 Full-Auto |
|--------|-------------|----------------|----------------|
| **Time** | ~30 min | ~10 min | ~5 min |
| **Developer Effort** | 30 min | 2 min (review) | 0 min |
| **API Cost** | $0.50 | $0.50 | $0.75 |
| **Labor Cost** (@ $100/hr) | $50 | $3.33 | $0 |
| **Total Cost** | $50.50 | $3.83 | $0.75 |
| **vs Manual (2 weeks)** | 99% savings | 99.97% savings | 99.99% savings |
| **Time Saved** | 11.5 hours | 11.83 hours | 11.92 hours |
| **Servers/Day** (1 person) | 16 | 48 | 96 |

**Key Insight**: Even v1.0 delivers massive ROI. Each tier amplifies productivity further.

---

## 16-Week Phased Roadmap

Implementation follows a phased approach delivering incremental value:

### Phase 1: Production Foundation (Weeks 1-2) - P0

**Goal**: Stable chora-compose as first production MCP server

**Deliverables**:
- ✅ chora-compose MCP server with 24 tools (generation)
- ✅ Docker SSE/HTTP transport
- ✅ stdio bridge for Claude Desktop (via Supergateway)
- ✅ Production secrets management
- ✅ SQLite persistence (dependency tracking)
- ✅ CodeGenerationGenerator (AI code generation)

**What Works**:
- Generate project structure (bootstrap_project)
- Generate implementation code (generate_code)
- Regenerate configs from templates
- Docker deployment (manual)

**What's Manual**:
- Client configuration (per-client setup)
- Server deployment (docker-compose)
- No auto-discovery yet

**Success Criteria**:
- [ ] chora-compose accessible via Claude Code
- [ ] Generate MCP server project structure (17 files)
- [ ] AI code generation working ($0.50 per server)
- [ ] Documentation complete (this guide + lifecycle docs)

**Status**: ✅ chora-compose team implementing (Nov 2025)

### Phase 2: Registry & Manual Lifecycle (Weeks 3-4) - P1

**Goal**: Prove manual 12-step lifecycle end-to-end

**Deliverables**:
- ecosystem-manifest repository
- registry.yaml schema and validation
- Manual lifecycle documentation (<30 min)
- 2-3 MCP servers deployed and registered
- Bridge configuration tested (Claude Desktop ↔ Supergateway ↔ SSE servers)

**What Works**:
- Declarative server registry (registry.yaml)
- Manual execution of all 12 steps
- chora-compose.regenerate_configs reads registry
- Documented workflow for v1.0

**What's Manual**:
- All 12 steps executed individually (no orchestration)
- Registry updates via git commits
- Deployment via docker-compose

**Success Criteria**:
- [ ] ecosystem-manifest repo created
- [ ] registry.yaml schema validated
- [ ] Manual lifecycle <30 min (documented)
- [ ] 3 servers deployed: chora-compose, taskmgr, another
- [ ] Claude Desktop can access all servers via Supergateway

**Status**: ⏳ Planned after Phase 1

### Phase 3: Orchestration Layer (Weeks 5-8) - P2

**Goal**: Automated deployment and health monitoring

**Deliverables**:
- mcp-orchestration MCP server
- `orchestration.deploy_server` tool (automated Step 8)
- `orchestration.health_check` tool (automated Step 9)
- Auto-recovery for unhealthy servers
- Multi-instance support (load balancing prep)

**What Works**:
- Deploy server from Docker image (1 tool call)
- Health monitoring (automated checks every 30s)
- Restart unhealthy servers (auto-recovery)
- Deployment time <2 min (vs 10 min manual docker-compose)

**What's Manual**:
- Steps 1-7 still manual (generation, GitHub, registry)
- Steps 10-12 still manual (discovery, client refresh)
- Gateway not yet available (direct connections to orchestration)

**Success Criteria**:
- [ ] orchestration.deploy_server deploys from image
- [ ] orchestration.health_check returns health status
- [ ] Auto-restart unhealthy servers (test by killing container)
- [ ] Deployment <2 min (vs 10 min manual)

**Status**: 📋 Designed, pending Phase 2 completion

### Phase 4: Gateway Layer (Weeks 9-12) - P3

**Goal**: Unified client access and auto-discovery

**Deliverables**:
- mcp-gateway at localhost:8679
- Auto-discovery from registry.yaml (poll every 60s)
- `GET /tools` shows all servers
- `POST /tools/{namespace}/{tool}` unified invocation
- Health-aware routing (failover to healthy instances)
- ALL clients tested (Claude, n8n, Python, Bash)

**What Works**:
- Single connection point for all clients
- Auto-discovery (no manual client config)
- Health-aware routing (gateway routes only to healthy servers)
- Namespace-based routing (taskmgr.* → localhost:8082)
- Cross-client consistency (same tool calls everywhere)

**What's Manual**:
- Still 12 individual tool calls per lifecycle
- No workflow orchestration yet (that's Phase 5)

**Success Criteria**:
- [ ] mcp-gateway running at localhost:8679
- [ ] GET /tools lists all servers and tools
- [ ] Claude Code can call tools via gateway
- [ ] Python script can call tools via gateway
- [ ] n8n (via HTTP Request) can call tools
- [ ] Auto-discovery: Add server to registry → available <60s
- [ ] Health failover: Kill server → gateway routes to backup

**Status**: 📋 Designed, pending Phase 3 completion

### Phase 5: Advanced Automation (Weeks 13-16) - P4

**Goal**: Full lifecycle automation via n8n

**Deliverables**:
- mcp-server-n8n (n8n workflows as MCP tools - Pattern N2)
- @chora/n8n-node-mcp-gateway (n8n calls MCP tools - Pattern N3b)
- v2.0 semi-automated lifecycle (8-10 min via workflow)
- n8n workflow templates (lifecycle automation, batch creation)
- Meta-orchestration (workflow of workflows)

**What Works**:
- Entire 12-step lifecycle in single n8n workflow
- Batch creation (10 servers in <90 min)
- CI/CD trigger on git push
- Human-in-the-loop approvals (optional)
- Recursive pattern: n8n calling n8n via gateway

**What's Automated**:
- Bootstrap through deployment (Steps 1-9)
- Registry update (Step 6)
- Health verification (Step 9)

**What's Manual**:
- Code review before deploy (optional)
- Production approval (optional)
- Complex business logic (AI limitations)

**Success Criteria**:
- [ ] mcp-server-n8n exposes n8n workflows as tools
- [ ] n8n-node-mcp-gateway custom node installed
- [ ] n8n workflow template creates MCP server in <10 min
- [ ] Batch creation: 10 servers in <90 min
- [ ] Recursive pattern: n8n calls n8n via gateway

**Status**: 📋 Planned for Q1 2026

### Current Recommendations (Nov 2025)

**If Phase 1 Complete** (chora-compose production):
- ✅ Use chora-compose directly for manual code generation
- ✅ Connect Claude Desktop via Supergateway bridge
- ✅ Deploy servers manually using docker-compose
- ✅ Document as you go (improve this documentation)

**If Phase 2-5 Pending**:
- ⏳ Use this documentation to understand target architecture
- ⏳ Contribute to ecosystem-manifest registry schema
- ⏳ Provide feedback on lifecycle steps
- ⏳ Test manual workflows to identify automation opportunities

---

## Implementation Details

This section provides technical depth on key components. For full details, see the linked documentation.

### chora-compose Code Generation

**Purpose**: AI-powered implementation code generation

**Implementation**: `CodeGenerationGenerator` class (499 lines)

**Key Features**:
- **Claude API Integration**: Uses claude-3-5-sonnet-20241022
- **Natural Language Prompts**: "Generate a function that validates task input..."
- **Variable Substitution**: `{{namespace}}`, `{{tool_specifications}}` in prompts
- **Retry Logic**: Exponential backoff for rate limits
- **Cost Tracking**: Tracks tokens and USD per generation
- **Fallback Templates**: Use template if AI fails
- **Response Parsing**: Auto-strips markdown code fences

**Example**:
```python
from chora_compose.generators.code_generation import CodeGenerationGenerator

generator = CodeGenerationGenerator(api_key="sk-ant-...")

config = ContentConfig(
    id="task_validator",
    output_path="utils/validators.py",
    generation=GenerationConfig(
        patterns=[Pattern(
            type="code_generation",
            generation_config={
                "prompt": "Create a function validate_task that checks title non-empty, due_date ISO 8601...",
                "language": "python",
                "temperature": 0.0,
                "max_tokens": 2048
            }
        )]
    )
)

code = generator.generate(config)
cost = generator.get_total_cost()

print(f"Cost: ${cost['total_cost_usd']:.6f}")
# Cost: $0.004235
```

**Cost Analysis**:
- Simple function: $0.005 (300 tokens out)
- MCP tool: $0.012 (600 tokens out)
- Full server: $0.045 (2500 tokens out)
- **5-file server**: $0.20-$0.50 total

**ROI**: $0.50 API cost vs $1,200 manual labor = 240,000% ROI

See: [CODE-GENERATION-CAPABILITIES.md](lifecycle/CODE-GENERATION-CAPABILITIES.md)

### mcp-gateway API Specification

**Endpoint**: `http://localhost:8679`

**API Routes**:

#### 1. Discover Tools
```http
GET /tools
```

**Response**:
```json
{
  "tools": [
    {
      "namespace": "chora-compose",
      "server": "mcp-server-chora-compose",
      "tools": [
        {"name": "chora-compose.bootstrap_project", "status": "healthy"},
        {"name": "chora-compose.generate_code", "status": "healthy"}
      ]
    },
    {
      "namespace": "taskmgr",
      "server": "mcp-server-taskmgr",
      "tools": [
        {"name": "taskmgr.create", "status": "healthy"},
        {"name": "taskmgr.list", "status": "healthy"}
      ]
    }
  ],
  "total_tools": 34,
  "servers_healthy": 3,
  "servers_unhealthy": 0
}
```

#### 2. Invoke Tool
```http
POST /tools/{namespace}/{tool_name}
Content-Type: application/json

{
  "param1": "value1",
  "param2": "value2"
}
```

**Example**:
```http
POST /tools/taskmgr/create
Content-Type: application/json

{
  "title": "Review lifecycle docs",
  "description": "Review the 12-step lifecycle",
  "priority": "high",
  "due_date": "2025-11-08"
}
```

**Response**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Review lifecycle docs",
  "priority": "high",
  "created_at": "2025-11-03T11:00:00Z"
}
```

#### 3. Health Check
```http
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "gateway_version": "1.0.0",
  "servers": [
    {"namespace": "chora-compose", "status": "healthy"},
    {"namespace": "orchestration", "status": "healthy"},
    {"namespace": "taskmgr", "status": "healthy"}
  ],
  "uptime_seconds": 86400
}
```

**Error Handling**:
```json
{
  "error": "SERVER_UNHEALTHY",
  "message": "Server 'taskmgr' is unhealthy",
  "retry_after": 30,
  "failover_available": false
}
```

See: [GATEWAY-ORCHESTRATION.md](lifecycle/GATEWAY-ORCHESTRATION.md)

### ecosystem-manifest Registry Schema

**File**: `ecosystem-manifest/registry.yaml`

**Schema**:
```yaml
version: "1.0"

servers:
  - name: string              # Unique server name
    namespace: string         # Namespace for tools (must be unique)
    description: string       # Human-readable description
    version: string           # Semver version (e.g., "0.1.0")

    # Deployment
    docker_image: string      # Docker Hub image (e.g., "chora/mcp-server-taskmgr:0.1.0")
    endpoint: string          # HTTP endpoint (e.g., "http://localhost:8082")

    # Health
    health_url: string        # Health check endpoint (e.g., "http://localhost:8082/health")
    health_spec_version: string  # Health spec version (e.g., "1.0")

    # Metadata
    capabilities: [string]    # Feature tags (e.g., ["task-management", "persistence"])
    quality_tier: string      # bronze | silver | gold | platinum
    maintainers: [string]     # GitHub usernames or team names
    repository: string        # GitHub repo URL

    # Tools
    tools:
      - name: string          # Tool name (e.g., "taskmgr.create")
        description: string   # Tool description

    # Timestamps
    created_at: string        # ISO 8601 timestamp
    updated_at: string        # ISO 8601 timestamp
```

**Example Entry**:
```yaml
servers:
  - name: mcp-server-taskmgr
    namespace: taskmgr
    description: Task management MCP server with CRUD operations
    version: 0.1.0
    docker_image: liminalcommons/mcp-server-taskmgr:0.1.0
    endpoint: http://localhost:8082
    health_url: http://localhost:8082/health
    health_spec_version: "1.0"
    capabilities:
      - task-management
      - persistence
    quality_tier: gold
    maintainers:
      - chora-workspace
    repository: https://github.com/liminalcommons/mcp-server-taskmgr
    tools:
      - name: taskmgr.create
        description: Create a new task
      - name: taskmgr.list
        description: List all tasks
      - name: taskmgr.update
        description: Update an existing task
      - name: taskmgr.delete
        description: Delete a task
    created_at: "2025-11-01T10:45:00Z"
    updated_at: "2025-11-01T10:45:00Z"
```

**Quality Tiers**:
- **Bronze**: Basic functionality, <50% test coverage
- **Silver**: Complete functionality, 50-75% coverage
- **Gold**: Production-ready, 75-90% coverage, health endpoint
- **Platinum**: Gold + docs + examples + 90%+ coverage

### n8n Integration Patterns

**Dual Role**: n8n operates as both client AND server

#### Pattern N2: n8n as Server

**Component**: `mcp-server-n8n`

**Purpose**: Expose n8n workflows as MCP tools

**Architecture**:
```
Claude Code → mcp-gateway → mcp-server-n8n → n8n API
```

**Tools**:
- `n8n.trigger_workflow`: Execute workflow
- `n8n.list_workflows`: List available workflows
- `n8n.check_execution`: Check workflow status

**Use Case**:
```
User (in Claude Code): "Trigger the CI/CD pipeline for mcp-server-taskmgr"

Claude Code: I'll trigger the n8n CI/CD workflow.
[Calls: mcp-gateway/n8n.trigger_workflow]

Input:
{
  "workflow_id": "cicd-mcp-servers",
  "input_data": {
    "repo": "chora-workspace/mcp-server-taskmgr",
    "branch": "main"
  }
}

Output:
{
  "execution_id": "exec_abc123",
  "status": "running"
}
```

#### Pattern N3b: n8n as Client

**Component**: `@chora/n8n-node-mcp-gateway` (custom n8n node)

**Purpose**: Enable n8n workflows to call MCP servers

**Architecture**:
```
n8n workflow → MCP Gateway Node → mcp-gateway → ANY MCP server
```

**Node Configuration**:
```javascript
{
  "operation": "callTool",
  "gatewayUrl": "http://localhost:8679",
  "toolName": "chora-compose.bootstrap_project",
  "parameters": "{\"namespace\": \"taskmgr\", ...}"
}
```

**Use Case**: n8n workflow orchestrates full 12-step lifecycle
```json
{
  "name": "MCP Server Lifecycle - Automated",
  "nodes": [
    {"name": "Step 1: Bootstrap", "type": "mcpGateway", "toolName": "chora-compose.bootstrap_project"},
    {"name": "Step 2: Generate Code", "type": "mcpGateway", "toolName": "chora-compose.generate_code"},
    {"name": "Step 3: Create Repo", "type": "mcpGateway", "toolName": "github.create_repo"},
    // ... 9 more nodes
  ]
}
```

#### Recursive Pattern: n8n Calling n8n

```
n8n workflow A → mcp-gateway → mcp-server-n8n → n8n workflow B
```

**Benefits**:
- Workflow composition (complex from simple)
- Meta-orchestration (workflow of workflows)
- Abstraction (n8n doesn't know it's calling itself)

See: [N8N-DUAL-ROLE.md](lifecycle/N8N-DUAL-ROLE.md)

---

## Getting Started

### Prerequisites

**For v1.0 (Manual Workflow)**:
- ✅ chora-base v2.0.3+ (SAP framework)
- ✅ chora-compose v3.2.0+ (with code_generation)
- ⚠️ GitHub account + API access
- ⚠️ Docker Desktop installed

**For v2.0 (Semi-Auto)**:
- ✅ All v1.0 prerequisites
- ❌ mcp-gateway (Phase 4 delivery)
- ❌ ecosystem-manifest repository (Phase 2 delivery)
- ❌ mcp-server-github (Phase 4 delivery)
- ❌ mcp-server-n8n (Phase 5 delivery)
- ❌ n8n with custom MCP client node (Phase 5 delivery)

### Quick Start: v1.0 Manual Workflow

**Goal**: Create and deploy an MCP server in ~30 minutes

**Step-by-Step**:

1. **Bootstrap Project** (use chora-compose)
   ```bash
   # Assuming chora-compose is available via Claude Code or CLI
   # Call: chora-compose.bootstrap_project
   # Input: namespace=taskmgr, tools=[create, list, update, delete]
   # Output: mcp-server-taskmgr/ directory with 17 files
   ```

2. **Generate Implementation** (AI code generation)
   ```bash
   # Call: chora-compose.generate_code
   # Input: prompt describing requirements
   # Output: 5 implementation files, cost ~$0.50
   ```

3. **Create GitHub Repo** (manual via web UI or gh CLI)
   ```bash
   gh repo create mcp-server-taskmgr --public
   ```

4. **Commit Files** (git)
   ```bash
   cd mcp-server-taskmgr
   git init
   git add .
   git commit -m "Initial commit: MCP server generated via chora-compose"
   git push
   ```

5. **CI/CD** (GitHub Actions auto-triggers on push)
   - Wait 5-10 min for tests + Docker build

6. **Update Registry** (manual edit)
   ```bash
   # Edit ecosystem-manifest/registry.yaml
   # Add entry for mcp-server-taskmgr
   git commit -m "Register mcp-server-taskmgr"
   git push
   ```

7. **Regenerate Configs** (chora-compose)
   ```bash
   # Call: chora-compose.regenerate_configs
   # Input: registry source URL
   # Output: Updated claude_desktop_config.json
   ```

8. **Deploy** (docker-compose)
   ```bash
   docker-compose up -d mcp-server-taskmgr
   ```

9. **Health Check** (curl)
   ```bash
   curl http://localhost:8082/health | jq
   # Should return: {"status": "healthy", ...}
   ```

10-12. **Discover & Use** (Claude Code)
   ```
   User: "List all available MCP tools"
   Claude: [Shows taskmgr.create, taskmgr.list, etc.]

   User: "Create a task to test the new server"
   Claude: [Calls taskmgr.create, returns task ID]
   ```

**Time**: ~30 minutes

### Learning Path

**New to the Ecosystem?**

1. **Start Here**: Read this document (MCP-ECOSYSTEM-VISION-AND-IMPLEMENTATION.md)
2. **Architecture Deep Dive**: [LIFECYCLE-OVERVIEW.md](lifecycle/LIFECYCLE-OVERVIEW.md)
3. **Detailed Steps**: [LIFECYCLE-STEPS-DETAILED.md](lifecycle/LIFECYCLE-STEPS-DETAILED.md)
4. **Client Patterns**: [GATEWAY-ORCHESTRATION.md](lifecycle/GATEWAY-ORCHESTRATION.md)
5. **n8n Integration**: [N8N-DUAL-ROLE.md](lifecycle/N8N-DUAL-ROLE.md)
6. **Code Generation**: [CODE-GENERATION-CAPABILITIES.md](lifecycle/CODE-GENERATION-CAPABILITIES.md)

**Want to Contribute?**

1. **Understand Vision**: This document + [ARCHITECTURE_CLARIFICATION.md](../inbox/ecosystem/ARCHITECTURE_CLARIFICATION.md)
2. **Review Roadmap**: [16-Week Phased Roadmap](#16-week-phased-roadmap)
3. **Pick a Phase**: See current phase status, identify gaps
4. **Follow Process**: Use inbox protocol for coordination
5. **Test & Document**: BDD scenarios in [WORKFLOW-VALIDATION-SCENARIOS.md](lifecycle/WORKFLOW-VALIDATION-SCENARIOS.md)

### Example Workflows

**Interactive (Claude Code)**:
```
User: "Create a task management MCP server with SQLite persistence"

Claude Code: I'll help you create a task management MCP server. Let me break this down into steps:

1. Bootstrap the project structure
2. Generate implementation code with AI
3. Create GitHub repository
4. Set up CI/CD
5. Deploy and test

Let's start with step 1...

[Calls: chora-compose.bootstrap_project]

✓ Created mcp-server-taskmgr/ with 17 files

Next, I'll generate the implementation code...

[Calls: chora-compose.generate_code]

✓ Generated 5 implementation files ($0.42 API cost)

[... continues through all 12 steps ...]

Done! Your MCP server is deployed at http://localhost:8082

Try it:
User: "Create a task to review documentation"
[Calls: taskmgr.create]
✓ Task created with ID: 550e8400-...
```

**Automated (n8n workflow)**:
```
Trigger: Webhook POST /create-mcp-server
Input:
{
  "namespace": "taskmgr",
  "description": "Task management server",
  "tools": ["create", "list", "update", "delete"]
}

Workflow executes 12 nodes sequentially:
  Node 1: chora-compose.bootstrap_project → 17 files created
  Node 2: chora-compose.generate_code → 5 files implemented
  Node 3: github.create_repo → Repo created
  Node 4: github.commit_files → Initial commit pushed
  Node 5: n8n.trigger_workflow (CI/CD) → Tests + Docker build
  Node 6: ecosystem.register_server → Registry updated
  Node 7: chora-compose.regenerate_configs → Configs updated
  Node 8: orchestration.deploy_server → Container deployed
  Node 9: orchestration.health_check → Health verified
  Node 10: Slack notification → "MCP server deployed successfully"

Duration: 8-10 minutes
```

**Batch (Python script)**:
```python
from mcp_client import Gateway
import yaml

gateway = Gateway("http://localhost:8679")

# Load server specs from YAML
servers = yaml.safe_load(open("servers.yaml"))

for server in servers:
    print(f"Creating {server['namespace']}...")

    # Step 1-2: Bootstrap + Generate
    gateway.call("chora-compose.bootstrap_project", **server)
    gateway.call("chora-compose.generate_code", **server)

    # Steps 3-12: GitHub, CI/CD, Deploy
    gateway.call("github.create_repo", name=f"mcp-server-{server['namespace']}")
    # ... etc

    print(f"✓ {server['namespace']} deployed")

print(f"Created {len(servers)} MCP servers in {elapsed_time:.1f} minutes")
# Created 10 MCP servers in 72.3 minutes
```

---

## References

### Vision & Strategy

- **[ARCHITECTURE_CLARIFICATION.md](../inbox/ecosystem/ARCHITECTURE_CLARIFICATION.md)**: Unified gateway vision (authoritative)
- **[UNIFIED-VISION-MCP-ECOSYSTEM.md](lifecycle/UNIFIED-VISION-MCP-ECOSYSTEM.md)**: 16-week phased roadmap
- **[COORD-2025-003](../inbox/incoming/coordination/COORD-2025-003-lifecycle-docs.json)**: Coordination tracking for this documentation

### Lifecycle Documentation

- **[LIFECYCLE-OVERVIEW.md](lifecycle/LIFECYCLE-OVERVIEW.md)**: Architecture overview (entry point)
- **[LIFECYCLE-STEPS-DETAILED.md](lifecycle/LIFECYCLE-STEPS-DETAILED.md)**: Exhaustive 12-step breakdown
- **[GATEWAY-ORCHESTRATION.md](lifecycle/GATEWAY-ORCHESTRATION.md)**: Client-agnostic patterns
- **[N8N-DUAL-ROLE.md](lifecycle/N8N-DUAL-ROLE.md)**: n8n as client + server
- **[CODE-GENERATION-CAPABILITIES.md](lifecycle/CODE-GENERATION-CAPABILITIES.md)**: chora-compose AI generation
- **[WORKFLOW-VALIDATION-SCENARIOS.md](lifecycle/WORKFLOW-VALIDATION-SCENARIOS.md)**: BDD validation scenarios
- **[ADR-001-unified-gateway-orchestration.md](lifecycle/adrs/ADR-001-unified-gateway-orchestration.md)**: Architecture decision record

### Examples (Planned)

- **[claude-code-session.md](lifecycle/examples/claude-code-session.md)**: Interactive manual lifecycle
- **[n8n-workflow-automated.json](lifecycle/examples/n8n-workflow-automated.json)**: Automated workflow (Phase 5)
- **[python-script-batch.py](lifecycle/examples/python-script-batch.py)**: Batch orchestration (Phase 4)

### Implementation Resources

- **chora-compose README**: Generator framework overview
- **chora-base SAP-003**: MCP server templates
- **FastMCP Documentation**: Framework docs
- **n8n Documentation**: Workflow automation

---

## Appendix: Decision Record Summary

**From ADR-001: Unified Gateway Orchestration Architecture**

**Decision**: Adopt unified gateway pattern (ALL clients → mcp-gateway → ALL servers)

**Alternatives Considered**:
1. ❌ Direct client-to-server connections (poor scalability, O(N×M) configs)
2. ❌ Client-specific gateways (fragmented ecosystem, duplicate effort)
3. ❌ MCP server mesh P2P (too complex for <100 servers)
4. ❌ Monolithic MCP server (poor isolation, cannot scale tools independently)

**Consequences**:

**Positive**:
- Client flexibility (choose your orchestration tool)
- Single source of truth (registry.yaml)
- Auto-discovery (no manual client config)
- Consistent experience (same tool calls everywhere)
- Scalability (supports 100+ servers)
- Health awareness (automatic failover)
- Future-proof (new clients just need HTTP)

**Negative**:
- Single point of failure (mitigated: HA mode)
- Performance overhead (~5-10ms, negligible)
- Implementation effort (4-6 weeks MVP)

**Accepted**: Nov 2025

---

## Summary

This document captures the complete vision for the chora-workspace MCP ecosystem lifecycle automation:

1. **Vision**: Full lifecycle from chora-base through deployment, operations, and provisioning
2. **Architecture**: Unified gateway (ALL clients → mcp-gateway → ALL servers)
3. **Lifecycle**: 12-step MCP tool call sequence (client-agnostic)
4. **Automation**: v1.0 (30 min manual) → v2.0 (10 min semi-auto) → v3.0 (5 min full-auto)
5. **Timeline**: 16-week phased roadmap (5 phases, incremental delivery)
6. **ROI**: 99%+ time/cost reduction vs manual coding

**Key Insight**: The unified gateway transforms MCP server development from a weeks-long manual process into a minutes-long automated workflow, orchestrable via ANY tool (Claude, n8n, Python, Bash).

**Next Steps**:
- Phase 1 (Weeks 1-2): Production chora-compose
- Phase 2 (Weeks 3-4): Registry & manual lifecycle proof
- Phase 3 (Weeks 5-8): Orchestration layer
- Phase 4 (Weeks 9-12): Gateway layer
- Phase 5 (Weeks 13-16): n8n automation

**Status**: ✅ Documentation complete, ready for implementation

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-03
**Maintainer**: chora-workspace team
**Next Review**: After Phase 1 completion (Week 2, 2025)
