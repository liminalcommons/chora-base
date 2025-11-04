# MCP Ecosystem: Workflow Continuity Gap Analysis

> **⚠️ SUPERSEDED**: This document has been superseded by [mcp-ecosystem-sap-synergies.md](../mcp-ecosystem-sap-synergies.md)
>
> **Reason**: This document incorrectly focused on architectural gaps (missing components like mcp-gateway, mcp-orchestration) rather than SAP synergies. The correct approach is to identify how existing SAPs integrate to enable the MCP ecosystem vision, not to identify missing architectural components. SAPs create context for ecosystem repos to adopt and implement, not a requirements list for new systems to build.
>
> **What to use instead**: See [mcp-ecosystem-sap-synergies.md](../mcp-ecosystem-sap-synergies.md) for analysis of 8 SAP synergies that show how existing SAPs work together to enable the MCP vision.
>
> **Archived**: 2025-11-03

---

# ORIGINAL CONTENT (SUPERSEDED)

---

**Date**: 2025-11-03
**Type**: Gap Analysis (MCP Vision Context)
**Status**: Active
**Impact**: Critical - Identifies blockers for 12-step MCP lifecycle automation
**Related Vision**: [MCP-ECOSYSTEM-VISION-AND-IMPLEMENTATION.md](initiatives/MCP-ECOSYSTEM-VISION-AND-IMPLEMENTATION.md)
**Trace ID**: CHORA-COORD-2025-003

---

## Executive Summary

This document re-evaluates workflow continuity gaps through the lens of the **MCP Ecosystem 12-Step Lifecycle Vision**, which aims to transform MCP server creation from 2 weeks → 10 minutes via unified gateway automation.

**Key Findings**:
- **20 total gaps identified**: 10 existing (GAP-001 to GAP-010) + 10 new MCP-specific (GAP-011 to GAP-020)
- **3 Absolute Blockers** (EVS 3.0): ecosystem-manifest registry, mcp-orchestration, mcp-gateway
- **5 Critical Enablers** (EVS 2.5+): Unified release, GitHub/n8n servers, trace injection, n8n custom node
- **Phase 1 Quick Wins**: GAP-019, GAP-017, GAP-005 can be implemented immediately

**Recommendation**: Focus on phase-specific blockers while delivering Phase 1 quick wins to establish observable, quality-gated v1.0 manual workflow.

---

## MCP Vision Context

### The 12-Step Lifecycle

The MCP ecosystem vision defines a **12-step MCP tool call sequence** orchestrable via ANY client (Claude Code, n8n, Python, Bash):

| Step | MCP Tool | Purpose | Current Status |
|------|----------|---------|----------------|
| 1 | `chora-compose.bootstrap_project` | Generate project structure | ✅ Ready |
| 2 | `chora-compose.generate_code` | AI-powered implementation | ✅ Ready |
| 3 | `github.create_repo` | Create GitHub repository | ⚠️ **GAP-012** |
| 4 | `github.commit_files` | Commit generated files | ⚠️ **GAP-012** |
| 5 | `n8n.trigger_workflow` | Run CI/CD pipeline | ⚠️ **GAP-013** |
| 6 | `ecosystem.register_server` | Add to registry.yaml | ⚠️ **GAP-011** |
| 7 | `chora-compose.regenerate_configs` | Update client configs | ⚠️ **GAP-016** |
| 8 | `orchestration.deploy_server` | Deploy Docker container | ⚠️ **GAP-014** |
| 9 | `orchestration.health_check` | Verify deployment | ⚠️ **GAP-014** |
| 10 | mcp-gateway auto-discovery | Gateway discovers new server | ⚠️ **GAP-015** |
| 11 | Client refresh | Query updated tool list | ⚠️ **GAP-015** |
| 12 | Use new tools | Call new server's tools | ✅ Ready |

**Gaps Block**: 9 of 12 steps have gaps preventing automation.

### Core Principles

Eight principles guide the MCP ecosystem:

1. **Unified Gateway Architecture**: ALL clients → mcp-gateway → ALL servers
2. **Client-Agnostic Design**: Same tool calls work across all clients
3. **Namespace Isolation**: Tools namespaced (`namespace.tool_name`) - **GAP-018**
4. **Declarative Registry**: `registry.yaml` single source of truth - **GAP-011**
5. **Health-Aware Routing**: Gateway only routes to healthy servers - **GAP-015, GAP-017**
6. **Incremental Automation**: v1.0 (manual) → v2.0 (semi-auto) → v3.0 (full-auto)
7. **AI-Powered Implementation**: chora-compose generates code, not just boilerplate
8. **Observable by Default**: CHORA_TRACE_ID through all steps - **GAP-001, GAP-019**

---

## Existing Gaps Mapped to MCP Lifecycle

| Gap ID | Gap Name | EVS | MCP Steps Affected | Blocker/Friction | Blocks Phase | New Priority |
|--------|----------|-----|-------------------|------------------|-------------|-------------|
| **GAP-001** | CHORA_TRACE_ID Not Propagated | 2.75 | Steps 1-12 (ALL) | Quality (Observable) | N/A (enhancement) | **CRITICAL** (Principle #8) |
| **GAP-002** | Manual Coordination → Documentation | 2.60 | Steps 1-2 | Friction (manual handoff) | Phase 1 (DDD flow) | **High** (v1.0 UX) |
| **GAP-003** | Unified Release Workflow (Docker + PyPI) | 2.55 | Steps 5, 8 | Blocker (unified deploy) | Phase 3 | **CRITICAL** (Step 8) |
| **GAP-004** | CI Metrics Not Exported | 2.45 | Step 5 | Quality (observability) | N/A (post-deploy) | **Medium** (v2.0+) |
| **GAP-005** | Pre-Commit Hooks Not Auto-Installed | 2.30 | Steps 1, 4 | Friction (manual setup) | Phase 1 | **High** (v1.0) |
| **GAP-006** | Coverage Threshold Duplication | 2.05 | Step 5 | Quality (config drift) | N/A | **Low** |
| **GAP-007** | Link Validation Not in DDD | 1.95 | Steps 1-2 | Friction (late feedback) | N/A | **Low** |
| **GAP-008** | BDD Scenarios Not Validated | 1.85 | Steps 1-2 | Friction (no enforcement) | N/A | **Low** |
| **GAP-009** | Test Pyramid Ratios Not Validated | 1.75 | Step 5 | Quality (test strategy) | N/A | **Low** |
| **GAP-010** | Docker Health Checks Not Tested | 1.70 | Steps 5, 9 | Quality (reliability) | Phase 3 | **High** (Step 9) |

**Key Insights**:
- **GAP-001, GAP-003** become CRITICAL in MCP context (enable observability and deployment)
- **GAP-002, GAP-005** affect Phase 1 v1.0 manual workflow quality
- **GAP-006 to GAP-009** remain low priority (don't block lifecycle)
- **GAP-010** elevated to High (critical for Step 9 health validation)

---

## New MCP-Specific Gaps Discovered

### GAP-011: No ecosystem-manifest Registry Implementation ⚠️ ABSOLUTE BLOCKER

**EVS: 3.0/3.0** (WI: 3, AM: 3, DP: 3, GS: 3, EL: 3)

**Description**:
The MCP vision requires `ecosystem-manifest/registry.yaml` as single source of truth for all MCP servers (Principle #4), but this repository and schema don't exist yet. Without it, Steps 6-7 (register_server, regenerate_configs) cannot function.

**MCP Steps Affected**: Steps 6, 7, 10, 11
- Step 6: `ecosystem.register_server` has no registry to write to
- Step 7: `chora-compose.regenerate_configs` has no registry to read from
- Step 10: mcp-gateway has no registry to poll for auto-discovery
- Step 11: Clients have no centralized tool list to refresh from

**Blocker For**: Phase 2 (Weeks 3-4) - Manual lifecycle depends entirely on registry

**Current Workaround**: None - absolute blocker

**Evidence from Vision**:
- Lines 249-286: Registry schema definition
- Lines 454-470: Declarative registry principle
- Lines 1305-1377: Detailed registry.yaml specification

**Implementation Roadmap**:

**Week 1-2** (Phase 2 Start):
1. Create `ecosystem-manifest` repository
   ```bash
   gh repo create liminalcommons/ecosystem-manifest --public
   cd ecosystem-manifest
   mkdir -p schemas examples docs
   ```

2. Define `registry.yaml` schema
   ```yaml
   # schemas/registry-v1.0.schema.yaml
   version: "1.0"
   servers:
     - name: string           # Unique server name
       namespace: string      # Namespace (must be unique)
       description: string
       version: string        # Semver
       docker_image: string
       endpoint: string
       health_url: string
       health_spec_version: string
       capabilities: [string]
       quality_tier: string   # bronze|silver|gold|platinum
       maintainers: [string]
       repository: string
       tools:
         - name: string
           description: string
       created_at: string     # ISO 8601
       updated_at: string
   ```

3. Create validation script
   ```python
   # scripts/validate-registry.py
   import yaml
   import jsonschema

   def validate_registry(registry_path, schema_path):
       registry = yaml.safe_load(open(registry_path))
       schema = yaml.safe_load(open(schema_path))
       jsonschema.validate(registry, schema)

       # Check namespace uniqueness (GAP-018)
       namespaces = [s['namespace'] for s in registry['servers']]
       if len(namespaces) != len(set(namespaces)):
           raise ValueError("Duplicate namespaces detected")
   ```

4. Implement `ecosystem.register_server` MCP tool (as part of ecosystem-manifest server)
   ```python
   @mcp.tool()
   def register_server(
       name: str,
       namespace: str,
       description: str,
       version: str,
       docker_image: str,
       endpoint: str,
       health_url: str,
       tools: list[dict]
   ) -> dict:
       """Add server to ecosystem-manifest/registry.yaml"""
       # Validate namespace uniqueness (GAP-018)
       # Load registry.yaml
       # Append new entry
       # Validate schema
       # Commit to Git
       # Return confirmation
   ```

5. Add Git hooks for validation
   ```bash
   # .git/hooks/pre-commit
   #!/bin/bash
   python scripts/validate-registry.py registry.yaml schemas/registry-v1.0.schema.yaml
   ```

**Success Criteria**:
- [ ] ecosystem-manifest repo created and public
- [ ] registry.yaml schema validated (JSON Schema)
- [ ] `ecosystem.register_server` tool functional
- [ ] Git hooks enforce schema on commit
- [ ] 3+ servers registered (chora-compose, taskmgr, example)

**Dependencies**: None (foundational component)

**Unblocks**: GAP-015 (gateway needs registry), GAP-016 (regenerate_configs needs registry)

---

### GAP-012: mcp-server-github Missing (Steps 3-4 Blocked)

**EVS: 2.50/3.0** (WI: 3, AM: 2, DP: 2, GS: 2, EL: 3)

**Description**:
Steps 3-4 require `github.create_repo` and `github.commit_files` MCP tools to automate repository creation and initial commit. Without mcp-server-github, these steps are manual (requires `gh` CLI or web UI), breaking the automated 12-step flow.

**MCP Steps Affected**: Steps 3, 4
- Step 3: `github.create_repo` - Create GitHub repository
- Step 4: `github.commit_files` - Commit all 17 generated files

**Blocker For**: Phase 4-5 (full automation requires GitHub API integration)

**Current Workaround**: Manual via `gh` CLI or GitHub web UI

**Evidence from Vision**:
- Line 562: Step 3 status "⚠️ Needs mcp-server-github"
- Line 563: Step 4 status "⚠️ Needs mcp-server-github"
- Lines 675-677: GitHub integration in lifecycle

**Implementation Roadmap**:

**Week 5-6** (Phase 3-4):
1. Bootstrap `mcp-server-github` using chora-compose
   ```bash
   # Use our own tools to create GitHub server!
   chora-compose.bootstrap_project(
       namespace="github",
       tools=["create_repo", "commit_files", "tag_release", "create_pr"]
   )
   ```

2. Implement tools
   ```python
   # src/mcp_server_github/tools/create_repo.py
   @mcp.tool()
   def create_repo(
       name: str,
       description: str = "",
       private: bool = False,
       org: str | None = None
   ) -> dict:
       """Create GitHub repository using GitHub API"""
       gh = Github(os.environ['GITHUB_TOKEN'])
       if org:
           repo = gh.get_organization(org).create_repo(name, description, private)
       else:
           repo = gh.get_user().create_repo(name, description, private)
       return {"url": repo.html_url, "clone_url": repo.clone_url}

   # src/mcp_server_github/tools/commit_files.py
   @mcp.tool()
   def commit_files(
       repo: str,
       files: dict[str, str],  # path -> content
       message: str,
       branch: str = "main"
   ) -> dict:
       """Commit multiple files to GitHub repository"""
       gh = Github(os.environ['GITHUB_TOKEN'])
       repository = gh.get_repo(repo)

       for path, content in files.items():
           repository.create_file(path, message, content, branch)

       return {"committed": len(files), "branch": branch}
   ```

3. Add to registry.yaml
   ```yaml
   servers:
     - namespace: github
       name: mcp-server-github
       version: 0.1.0
       docker_image: liminalcommons/mcp-server-github:0.1.0
       endpoint: http://localhost:8083
       health_url: http://localhost:8083/health
       tools:
         - name: github.create_repo
           description: Create GitHub repository
         - name: github.commit_files
           description: Commit files to repository
         - name: github.tag_release
           description: Tag a release
         - name: github.create_pr
           description: Create pull request
   ```

4. Deploy and test
   ```bash
   # Test Step 3-4 automation
   github.create_repo(name="mcp-server-test")
   github.commit_files(
       repo="liminalcommons/mcp-server-test",
       files={"README.md": "# Test", "src/server.py": "..."},
       message="Initial commit via MCP"
   )
   ```

**Success Criteria**:
- [ ] mcp-server-github deployed
- [ ] Step 3 (create_repo) functional
- [ ] Step 4 (commit_files) commits 17 files in single call
- [ ] Integrated into 12-step lifecycle examples

**Dependencies**: GAP-011 (registry must exist to register server)

**Unblocks**: v2.0 semi-automated workflow (removes 2 manual steps)

---

### GAP-013: mcp-server-n8n Missing (Step 5 Not Orchestrable)

**EVS: 2.25/3.0** (WI: 2, AM: 2, DP: 3, GS: 2, EL: 2)

**Description**:
Step 5 (CI/CD) needs `n8n.trigger_workflow` to automate pipeline execution. Without mcp-server-n8n (Pattern N2: n8n as server), workflows must be triggered manually or via webhooks (no MCP integration), reducing lifecycle automation.

**MCP Steps Affected**: Step 5
- Step 5: `n8n.trigger_workflow` - Execute CI/CD pipeline (pytest, Docker build)

**Blocker For**: Phase 5 (Weeks 13-16) - n8n as server (Pattern N2)

**Current Workaround**: Trigger via n8n webhooks or manual workflow start

**Evidence from Vision**:
- Line 564: Step 5 status "⚠️ Needs mcp-server-n8n"
- Lines 335-345: mcp-server-n8n component definition
- Lines 1388-1420: Pattern N2 (n8n as server)

**Implementation Roadmap**:

**Week 13-14** (Phase 5):
1. Create `mcp-server-n8n` project
   ```python
   # src/mcp_server_n8n/tools/trigger_workflow.py
   @mcp.tool()
   def trigger_workflow(
       workflow_id: str,
       input_data: dict,
       wait_for_completion: bool = False
   ) -> dict:
       """Trigger n8n workflow via API"""
       n8n_api = f"{N8N_URL}/api/v1/workflows/{workflow_id}/execute"
       response = requests.post(
           n8n_api,
           json={"data": input_data},
           headers={"X-N8N-API-KEY": N8N_API_KEY}
       )
       execution_id = response.json()['executionId']

       if wait_for_completion:
           # Poll execution status until complete
           status = poll_execution_status(execution_id)
           return {"execution_id": execution_id, "status": status}

       return {"execution_id": execution_id, "status": "triggered"}
   ```

2. Implement additional tools
   ```python
   @mcp.tool()
   def list_workflows() -> list[dict]:
       """List all n8n workflows"""
       # GET /api/v1/workflows

   @mcp.tool()
   def check_execution(execution_id: str) -> dict:
       """Check n8n workflow execution status"""
       # GET /api/v1/executions/{execution_id}
   ```

3. Add to registry
   ```yaml
   servers:
     - namespace: n8n
       name: mcp-server-n8n
       tools:
         - name: n8n.trigger_workflow
         - name: n8n.list_workflows
         - name: n8n.check_execution
   ```

4. Example usage (Step 5 automation)
   ```python
   # Trigger CI/CD pipeline for new MCP server
   result = n8n.trigger_workflow(
       workflow_id="cicd-mcp-servers",
       input_data={
           "repo": "liminalcommons/mcp-server-taskmgr",
           "branch": "main"
       },
       wait_for_completion=True
   )
   # Result: {"execution_id": "exec_123", "status": "success"}
   ```

**Success Criteria**:
- [ ] mcp-server-n8n deployed
- [ ] n8n.trigger_workflow functional
- [ ] Step 5 automated (CI/CD triggered via MCP)
- [ ] Pattern N2 documented in lifecycle examples

**Dependencies**: GAP-011 (registry), GAP-015 (gateway for routing)

**Unblocks**: GAP-020 (recursive n8n pattern), v3.0 full automation

---

### GAP-014: mcp-orchestration Missing (Steps 8-9 Blocked) ⚠️ ABSOLUTE BLOCKER

**EVS: 2.85/3.0** (WI: 3, AM: 3, DP: 2, GS: 3, EL: 3)

**Description**:
Steps 8-9 require `orchestration.deploy_server` and `orchestration.health_check` to automate Docker deployment and health verification. Without mcp-orchestration, deployment is manual via `docker-compose` (no MCP automation), blocking Phase 3.

**MCP Steps Affected**: Steps 8, 9
- Step 8: `orchestration.deploy_server` - Deploy Docker container
- Step 9: `orchestration.health_check` - Verify deployment healthy

**Blocker For**: Phase 3 (Weeks 5-8) - Orchestration layer

**Current Workaround**: Manual `docker-compose up -d` (not MCP-orchestrable)

**Evidence from Vision**:
- Lines 567-568: Steps 8-9 status "⚠️ Needs MCP wrapper"
- Lines 316-332: mcp-orchestration component definition
- Lines 1027-1052: Phase 3 orchestration layer goals

**Implementation Roadmap**:

**Week 5-8** (Phase 3):
1. Create `mcp-orchestration` project
   ```python
   # src/mcp_orchestration/tools/deploy_server.py
   import docker

   @mcp.tool()
   def deploy_server(
       server_name: str,
       image: str,
       port: int,
       environment: dict[str, str] = {},
       health_check: dict = {}
   ) -> dict:
       """Deploy MCP server Docker container"""
       client = docker.from_env()

       container = client.containers.run(
           image=image,
           name=server_name,
           ports={f"{port}/tcp": port},
           environment=environment,
           detach=True,
           healthcheck={
               "test": ["CMD", "curl", "-f", health_check.get("endpoint", "/health")],
               "interval": int(health_check.get("interval", "10s").rstrip("s")) * 1000000000,
               "timeout": int(health_check.get("timeout", "5s").rstrip("s")) * 1000000000,
               "retries": health_check.get("retries", 3)
           }
       )

       return {
           "container_id": container.id,
           "name": server_name,
           "status": "running",
           "port": port
       }
   ```

2. Implement health check tool
   ```python
   @mcp.tool()
   def health_check(server_name: str) -> dict:
       """Check MCP server health status"""
       client = docker.from_env()
       container = client.containers.get(server_name)

       health = container.attrs['State']['Health']

       return {
           "status": health['Status'],  # "healthy" | "unhealthy"
           "checks": health['Log'][-5:],  # Last 5 health checks
           "uptime_seconds": (
               datetime.now() -
               datetime.fromisoformat(container.attrs['State']['StartedAt'].rstrip('Z'))
           ).total_seconds()
       }
   ```

3. Additional orchestration tools
   ```python
   @mcp.tool()
   def restart_server(server_name: str) -> dict:
       """Restart unhealthy MCP server"""

   @mcp.tool()
   def stop_server(server_name: str) -> dict:
       """Gracefully stop MCP server"""

   @mcp.tool()
   def scale_server(server_name: str, instances: int) -> dict:
       """Scale MCP server instances (load balancing)"""
   ```

4. Add to registry
   ```yaml
   servers:
     - namespace: orchestration
       name: mcp-orchestration
       tools:
         - name: orchestration.deploy_server
         - name: orchestration.health_check
         - name: orchestration.restart_server
         - name: orchestration.stop_server
         - name: orchestration.scale_server
   ```

5. Example usage (Steps 8-9 automation)
   ```python
   # Step 8: Deploy
   orchestration.deploy_server(
       server_name="mcp-server-taskmgr",
       image="liminalcommons/mcp-server-taskmgr:0.1.0",
       port=8082,
       environment={"DATABASE_URL": "sqlite:///data/tasks.db"},
       health_check={"endpoint": "/health", "interval": "10s"}
   )

   # Step 9: Verify
   health = orchestration.health_check("mcp-server-taskmgr")
   assert health["status"] == "healthy"
   ```

**Success Criteria**:
- [ ] mcp-orchestration deployed
- [ ] deploy_server functional (Step 8 automated)
- [ ] health_check functional (Step 9 automated)
- [ ] Auto-recovery tested (restart unhealthy containers)
- [ ] Deployment time <2 min (vs 10 min manual docker-compose)

**Dependencies**: GAP-011 (registry), GAP-017 (health endpoint standard)

**Unblocks**: GAP-015 (gateway needs orchestration for health-aware routing), Phase 3 completion

---

### GAP-015: mcp-gateway Missing (Step 10 Blocked) ⚠️ ABSOLUTE BLOCKER

**EVS: 3.0/3.0** (WI: 3, AM: 3, DP: 3, GS: 3, EL: 3)

**Description**:
Step 10 (auto-discovery) requires mcp-gateway to poll registry.yaml every 60s and expose unified API (`GET /tools`, `POST /tools/{namespace}/{tool}`). Without gateway, clients must connect directly to each server (O(N×M) configuration problem), defeating the entire unified vision.

**MCP Steps Affected**: Steps 10, 11, 12
- Step 10: mcp-gateway auto-discovery (polls registry every 60s)
- Step 11: Client refresh (queries `GET /tools`)
- Step 12: Tool invocation (calls `POST /tools/{namespace}/{tool}`)

**Blocker For**: Phase 4 (Weeks 9-12) - Gateway layer (core of unified vision)

**Current Workaround**: None - entire unified gateway architecture blocked

**Evidence from Vision**:
- Lines 145-227: Core architecture diagram (gateway as hub)
- Lines 232-243: mcp-gateway key features
- Lines 384-401: Unified gateway principle (#1)
- Lines 1054-1086: Phase 4 gateway layer goals

**Implementation Roadmap**:

**Week 9-12** (Phase 4):
1. Create `mcp-gateway` project (FastAPI-based REST gateway)
   ```python
   # src/mcp_gateway/main.py
   from fastapi import FastAPI, HTTPException
   import httpx
   import asyncio

   app = FastAPI()

   # Global state
   registry = {}  # namespace -> {endpoint, health_url, tools}
   health_status = {}  # namespace -> "healthy" | "unhealthy"

   async def poll_registry():
       """Poll ecosystem-manifest/registry.yaml every 60s"""
       while True:
           registry_url = "https://raw.githubusercontent.com/liminalcommons/ecosystem-manifest/main/registry.yaml"
           registry_data = yaml.safe_load(httpx.get(registry_url).text)

           for server in registry_data['servers']:
               registry[server['namespace']] = {
                   "endpoint": server['endpoint'],
                   "health_url": server['health_url'],
                   "tools": [t['name'] for t in server['tools']]
               }

           await asyncio.sleep(60)

   async def check_health():
       """Check health of all servers every 30s"""
       while True:
           for namespace, config in registry.items():
               try:
                   response = httpx.get(config['health_url'], timeout=5)
                   health_status[namespace] = "healthy" if response.json()['status'] == "healthy" else "unhealthy"
               except:
                   health_status[namespace] = "unhealthy"

           await asyncio.sleep(30)

   @app.on_event("startup")
   async def startup():
       asyncio.create_task(poll_registry())
       asyncio.create_task(check_health())
   ```

2. Implement REST API
   ```python
   @app.get("/tools")
   def list_tools():
       """Discover all available MCP tools"""
       tools = []
       for namespace, config in registry.items():
           tools.append({
               "namespace": namespace,
               "server": f"mcp-server-{namespace}",
               "status": health_status.get(namespace, "unknown"),
               "tools": [
                   {"name": tool, "status": health_status.get(namespace, "unknown")}
                   for tool in config['tools']
               ]
           })

       return {
           "tools": tools,
           "total_tools": sum(len(c['tools']) for c in registry.values()),
           "servers_healthy": sum(1 for s in health_status.values() if s == "healthy"),
           "servers_unhealthy": sum(1 for s in health_status.values() if s == "unhealthy")
       }

   @app.post("/tools/{namespace}/{tool_name}")
   async def invoke_tool(namespace: str, tool_name: str, payload: dict):
       """Invoke MCP tool via unified gateway"""
       if namespace not in registry:
           raise HTTPException(404, f"Namespace '{namespace}' not found")

       if health_status.get(namespace) != "healthy":
           raise HTTPException(503, f"Server '{namespace}' is unhealthy")

       # Route to server
       server_endpoint = registry[namespace]['endpoint']
       tool_path = f"{server_endpoint}/tools/{tool_name}"

       response = httpx.post(tool_path, json=payload, timeout=30)
       return response.json()

   @app.get("/health")
   def gateway_health():
       """Gateway health endpoint"""
       return {
           "status": "healthy",
           "gateway_version": "1.0.0",
           "servers": [
               {"namespace": ns, "status": health_status.get(ns, "unknown")}
               for ns in registry.keys()
           ]
       }
   ```

3. Deploy gateway
   ```bash
   # docker-compose.yml
   services:
     mcp-gateway:
       image: liminalcommons/mcp-gateway:1.0.0
       ports:
         - "8679:8679"
       environment:
         - REGISTRY_URL=https://raw.githubusercontent.com/liminalcommons/ecosystem-manifest/main/registry.yaml
         - POLL_INTERVAL=60
         - HEALTH_CHECK_INTERVAL=30
   ```

4. Test unified access
   ```bash
   # List all tools
   curl http://localhost:8679/tools | jq

   # Invoke tool via gateway
   curl -X POST http://localhost:8679/tools/chora-compose/bootstrap_project \
        -H "Content-Type: application/json" \
        -d '{"namespace": "taskmgr", "tools": ["create", "list"]}'

   # Gateway health
   curl http://localhost:8679/health | jq
   ```

**Success Criteria**:
- [ ] mcp-gateway running at localhost:8679
- [ ] GET /tools lists all registered servers and tools
- [ ] POST /tools/{namespace}/{tool} routes to correct server
- [ ] Auto-discovery: Add server to registry → available <60s
- [ ] Health-aware routing: Kill server → gateway returns 503
- [ ] ALL clients tested (Claude Code, Python, Bash, n8n HTTP Request)

**Dependencies**: GAP-011 (registry must exist), GAP-014 (orchestration for deployments)

**Unblocks**: Entire unified gateway vision, Phase 4 completion, v2.0 semi-automation

---

### GAP-016: chora-compose.regenerate_configs Doesn't Support Gateway

**EVS: 2.30/3.0** (WI: 2, AM: 3, DP: 1, GS: 2, EL: 3)

**Description**:
Step 7 requires `chora-compose.regenerate_configs` to update client configs from registry.yaml. Current implementation generates `claude_desktop_config.json` for direct server connections, not for unified gateway pattern. Need gateway-aware config generation.

**MCP Steps Affected**: Step 7
- Step 7: `chora-compose.regenerate_configs` must generate gateway configs

**Blocker For**: Phase 4 (gateway adoption requires config migration)

**Current Workaround**: Manually edit configs to point to gateway

**Evidence from Vision**:
- Line 566: Step 7 status "✅ Ready" (but only for direct connections)
- Lines 689-717: Config generation example (direct connections)
- Lines 397-401: ALL clients must connect to single gateway endpoint

**Implementation**:

**Week 10-11** (Phase 4):
1. Add `--gateway` flag to regenerate_configs
   ```python
   # chora-compose tool enhancement
   @mcp.tool()
   def regenerate_configs(
       registry_url: str,
       gateway_mode: bool = False,  # NEW
       gateway_endpoint: str = "http://localhost:8679"  # NEW
   ) -> dict:
       """Regenerate client configs from registry"""
       registry = fetch_registry(registry_url)

       if gateway_mode:
           # Gateway-aware config (single endpoint)
           config = generate_gateway_config(gateway_endpoint, registry)
       else:
           # Direct connections (legacy, pre-Phase 4)
           config = generate_direct_config(registry)

       write_config("claude_desktop_config.json", config)
       return {"mode": "gateway" if gateway_mode else "direct", "servers": len(registry['servers'])}
   ```

2. Create gateway config template
   ```jinja2
   {# templates/claude_desktop_config_gateway.json.j2 #}
   {
     "mcpServers": {
       "liminal-gateway": {
         "command": "node",
         "args": ["stdio-gateway-bridge.js"],
         "env": {
           "GATEWAY_URL": "{{ gateway_endpoint }}"
         },
         "metadata": {
           "mode": "unified-gateway",
           "servers": [
             {% for server in servers %}
             {
               "namespace": "{{ server.namespace }}",
               "tools": {{ server.tools | length }},
               "version": "{{ server.version }}"
             }{% if not loop.last %},{% endif %}
             {% endfor %}
           ]
         }
       }
     }
   }
   ```

3. Example output (gateway mode)
   ```json
   {
     "mcpServers": {
       "liminal-gateway": {
         "command": "node",
         "args": ["stdio-gateway-bridge.js"],
         "env": {
           "GATEWAY_URL": "http://localhost:8679"
         },
         "metadata": {
           "mode": "unified-gateway",
           "servers": [
             {"namespace": "chora-compose", "tools": 24, "version": "3.2.0"},
             {"namespace": "orchestration", "tools": 8, "version": "0.1.0"},
             {"namespace": "taskmgr", "tools": 4, "version": "0.1.0"}
           ]
         }
       }
     }
   }
   ```

4. Migration path
   ```python
   # Support both modes during Phase 4 transition
   chora-compose.regenerate_configs(
       registry_url="https://raw.githubusercontent.com/.../registry.yaml",
       gateway_mode=True  # Use gateway (Phase 4+)
   )

   # Legacy direct connections (pre-Phase 4)
   chora-compose.regenerate_configs(
       registry_url="...",
       gateway_mode=False  # Direct connections
   )
   ```

**Success Criteria**:
- [ ] regenerate_configs supports `--gateway` flag
- [ ] Gateway config generated correctly (single endpoint)
- [ ] Migration guide documented (direct → gateway)
- [ ] Both modes tested and working

**Dependencies**: GAP-015 (gateway must exist)

**Unblocks**: Phase 4 gateway adoption, client migration

---

### GAP-017: No Health Check Endpoint Standard in SAP-003 Templates

**EVS: 2.30/3.0** (WI: 2, AM: 3, DP: 1, GS: 2, EL: 3)

**Description**:
Vision requires all MCP servers to expose `/health` endpoint (ecosystem-manifest health spec). Current SAP-003 templates don't include health endpoint boilerplate. Step 9 (health_check) will fail without standardized endpoints, and gateway (Step 10) can't perform health-aware routing.

**MCP Steps Affected**: Steps 1, 9
- Step 1: `chora-compose.bootstrap_project` generates servers without health endpoints
- Step 9: `orchestration.health_check` expects standard `/health` endpoint

**Blocker For**: Phase 3 (health monitoring requires standard endpoints)

**Current Workaround**: Manually add health endpoints to generated servers

**Evidence from Vision**:
- Lines 482-495: Health endpoint spec definition
- Lines 742-752: Health check response example
- Lines 1047-1051: Phase 3 auto-recovery requires health checks

**Implementation**:

**Week 3-4** (Phase 2, prepare for Phase 3):
1. Update SAP-003 server template
   ```python
   # static-template/mcp-templates/server.py.template
   from fastapi import FastAPI
   from datetime import datetime

   app = FastAPI()
   START_TIME = datetime.now()

   @app.get("/health")
   def health_check():
       """Ecosystem-manifest v1.0 health endpoint"""
       uptime = (datetime.now() - START_TIME).total_seconds()

       # Check dependencies (database, Redis, etc.)
       dependencies = []
       {% if has_database %}
       db_status = check_database_connection()
       dependencies.append({"name": "database", "status": db_status})
       {% endif %}

       # Overall health: healthy if all dependencies healthy
       all_healthy = all(d['status'] == 'healthy' for d in dependencies)

       return {
           "status": "healthy" if all_healthy else "unhealthy",
           "version": "{{ version }}",
           "uptime_seconds": int(uptime),
           "dependencies": dependencies,
           "tools_available": {{ tools | length }},
           "health_spec_version": "1.0"
       }
   ```

2. Add health check tests
   ```python
   # tests/test_health.py
   def test_health_endpoint():
       response = client.get("/health")
       assert response.status_code == 200

       data = response.json()
       assert data['status'] in ['healthy', 'unhealthy']
       assert 'version' in data
       assert 'uptime_seconds' in data
       assert data['health_spec_version'] == '1.0'
   ```

3. Update bootstrap to include health by default
   ```python
   # chora-compose enhancement
   @mcp.tool()
   def bootstrap_project(...):
       # Generate health endpoint by default
       files.append({
           "path": "src/{namespace}/health.py",
           "content": render_template("health_endpoint.py.j2", ...)
       })
   ```

**Success Criteria**:
- [ ] SAP-003 templates include `/health` endpoint by default
- [ ] Health spec v1.0 implemented (status, version, uptime, dependencies, tools_available)
- [ ] Generated servers pass health check tests
- [ ] All new servers (via bootstrap_project) have health endpoints

**Dependencies**: None (template enhancement)

**Unblocks**: GAP-014 (orchestration needs health endpoints), GAP-015 (gateway needs health-aware routing)

---

### GAP-018: No Namespace Collision Detection

**EVS: 2.10/3.0** (WI: 2, AM: 2, DP: 1, GS: 2, EL: 3)

**Description**:
Principle #3 (Namespace Isolation) requires unique namespaces per server (e.g., `taskmgr.*`, `github.*`). But Step 6 (register_server) has no validation to prevent collisions. Developer could register two servers with same namespace, breaking gateway routing.

**MCP Steps Affected**: Step 6
- Step 6: `ecosystem.register_server` must validate namespace uniqueness

**Blocker For**: Phase 2 (registry implementation needs validation)

**Current Workaround**: Manual review during PR (error-prone)

**Evidence from Vision**:
- Lines 435-451: Namespace isolation principle
- Lines 1315: Registry schema shows `namespace` field (but no uniqueness constraint documented)

**Implementation**:

**Week 3-4** (Phase 2):
1. Add uniqueness validation to register_server
   ```python
   @mcp.tool()
   def register_server(namespace: str, ...) -> dict:
       """Add server to ecosystem-manifest/registry.yaml"""
       registry = load_registry()

       # GAP-018: Validate namespace uniqueness
       existing_namespaces = [s['namespace'] for s in registry['servers']]
       if namespace in existing_namespaces:
           raise ValueError(
               f"Namespace '{namespace}' already registered. "
               f"Choose a different namespace or update existing entry."
           )

       # Add server entry
       registry['servers'].append({
           "namespace": namespace,
           ...
       })

       save_registry(registry)
       return {"namespace": namespace, "status": "registered"}
   ```

2. Create validation script
   ```python
   # scripts/validate-registry.sh
   #!/usr/bin/env python3
   import yaml
   from collections import Counter

   registry = yaml.safe_load(open('registry.yaml'))
   namespaces = [s['namespace'] for s in registry['servers']]

   # Check for duplicates
   duplicates = [ns for ns, count in Counter(namespaces).items() if count > 1]
   if duplicates:
       print(f"ERROR: Duplicate namespaces: {duplicates}")
       exit(1)

   print(f"✓ All {len(namespaces)} namespaces unique")
   ```

3. Add Git pre-commit hook
   ```bash
   # .git/hooks/pre-commit
   #!/bin/bash
   python scripts/validate-registry.sh
   if [ $? -ne 0 ]; then
       echo "Registry validation failed. Fix namespace collisions."
       exit 1
   fi
   ```

4. Error messaging
   ```python
   # Helpful error with suggestions
   if namespace in existing_namespaces:
       suggestions = [
           f"{namespace}-v2",
           f"{namespace}-alt",
           f"my-{namespace}"
       ]
       raise ValueError(
           f"Namespace '{namespace}' already exists.\n"
           f"Suggestions: {', '.join(suggestions)}\n"
           f"Or update existing entry if you own it."
       )
   ```

**Success Criteria**:
- [ ] register_server validates namespace uniqueness
- [ ] scripts/validate-registry.sh detects duplicates
- [ ] Git hook prevents commits with duplicate namespaces
- [ ] Error messages provide helpful suggestions

**Dependencies**: GAP-011 (registry must exist)

**Unblocks**: Reliable namespace isolation (prevents gateway routing bugs)

---

### GAP-019: No CHORA_TRACE_ID Injection in chora-compose Tools

**EVS: 2.40/3.0** (WI: 2, AM: 2, DP: 3, GS: 2, EL: 3)

**Description**:
Principle #8 (Observable by Default) requires CHORA_TRACE_ID propagation through all 12 steps. But Steps 1-2 (chora-compose.bootstrap_project, generate_code) don't accept trace_id parameter or inject it into generated files. Breaks observability chain from SAP-001 coordination → MCP lifecycle.

**MCP Steps Affected**: Steps 1, 2, 7
- Step 1: `bootstrap_project` should accept/inject trace_id
- Step 2: `generate_code` should log trace_id
- Step 7: `regenerate_configs` should log trace_id

**Blocker For**: Phase 1 (observable v1.0 workflow)

**Current Workaround**: Manual trace tracking (unreliable)

**Evidence from Vision**:
- Lines 529-548: Observable by Default principle (#8)
- Lines 540-548: Example trace showing CHORA_TRACE_ID flow
- Line 8: Vision document itself has Trace ID: CHORA-COORD-2025-003

**Implementation**:

**Week 1-2** (Phase 1):
1. Add trace_id parameter to bootstrap_project
   ```python
   @mcp.tool()
   def bootstrap_project(
       namespace: str,
       tools: list[str],
       trace_id: str | None = None,  # NEW
       ...
   ) -> dict:
       """Generate MCP server project structure"""
       # Log trace_id
       logger.info(
           "bootstrap_project",
           extra={
               "trace_id": trace_id,
               "namespace": namespace,
               "tools": tools
           }
       )

       # Inject trace_id into generated files
       template_vars = {
           "namespace": namespace,
           "tools": tools,
           "trace_id": trace_id,  # Available in templates
           ...
       }

       # Generate files
       files = generate_from_templates(template_vars)

       return {
           "status": "success",
           "trace_id": trace_id,
           "files_created": len(files)
       }
   ```

2. Inject trace_id into generated files
   ```python
   # Generated README.md includes trace
   # README.md.j2 template
   # {{ namespace }}

   {% if trace_id %}
   **Trace ID**: `{{ trace_id }}`
   **Generated**: {{ timestamp }}
   {% endif %}

   # Generated pyproject.toml metadata
   [tool.chora]
   trace_id = "{{ trace_id }}"
   generated_at = "{{ timestamp }}"
   ```

3. Add trace_id to generate_code
   ```python
   @mcp.tool()
   def generate_code(
       file: str,
       prompt: str,
       trace_id: str | None = None,  # NEW
       ...
   ) -> dict:
       """AI-powered code generation"""
       logger.info(
           "generate_code",
           extra={
               "trace_id": trace_id,
               "file": file,
               "tokens": {...}
           }
       )

       # Claude API call includes trace in metadata
       response = anthropic.messages.create(
           model="claude-3-5-sonnet-20241022",
           messages=[...],
           metadata={
               "user_id": "chora-compose",
               "trace_id": trace_id
           }
       )

       return {
           "code": response.content[0].text,
           "trace_id": trace_id,
           "cost": {...}
       }
   ```

4. Coordinate with SAP-001 (inbox)
   ```python
   # Example: MCP server creation from coordination request
   # inbox/incoming/coordination/COORD-2025-042.json
   {
     "trace_id": "mcp-taskmgr-2025-003",
     "title": "Create task management MCP server",
     ...
   }

   # Agent extracts trace_id, passes to chora-compose
   chora-compose.bootstrap_project(
       namespace="taskmgr",
       tools=["create", "list", "update", "delete"],
       trace_id="mcp-taskmgr-2025-003"  # From coordination request
   )
   ```

**Success Criteria**:
- [ ] bootstrap_project accepts trace_id parameter
- [ ] generate_code accepts trace_id parameter
- [ ] Generated files include trace_id in metadata
- [ ] Structured logs include trace_id
- [ ] Documented in SAP-009 (agent awareness)

**Dependencies**: Coordinate with GAP-001 (full trace propagation protocol)

**Unblocks**: Observable v1.0 workflow, end-to-end trace from SAP-001 → MCP lifecycle

---

### GAP-020: n8n MCP Gateway Custom Node Not Implemented

**EVS: 2.50/3.0** (WI: 3, AM: 2, DP: 2, GS: 3, EL: 2)

**Description**:
Pattern N3b (n8n as Client) requires custom n8n node `@chora/n8n-node-mcp-gateway` to enable n8n workflows to call MCP servers via gateway. Without this, n8n can only use HTTP Request node (verbose, no type safety, no tool discovery), reducing automation quality.

**MCP Steps Affected**: Steps 1-12 (when orchestrated via n8n workflow)

**Blocker For**: Phase 5 (Weeks 13-16) - Full n8n automation

**Current Workaround**: HTTP Request node (manual URL construction, no validation)

**Evidence from Vision**:
- Lines 346-361: n8n MCP Gateway Node definition
- Lines 1421-1453: Pattern N3b (n8n as client)
- Lines 1619-1641: n8n workflow example

**Implementation**:

**Week 14-16** (Phase 5):
1. Create n8n custom node package
   ```typescript
   // nodes/McpGateway/McpGateway.node.ts
   import { IExecuteFunctions, INodeType, INodeTypeDescription } from 'n8n-workflow';

   export class McpGateway implements INodeType {
       description: INodeTypeDescription = {
           displayName: 'MCP Gateway',
           name: 'mcpGateway',
           group: ['transform'],
           version: 1,
           description: 'Call MCP tools via unified gateway',
           defaults: {
               name: 'MCP Gateway',
           },
           inputs: ['main'],
           outputs: ['main'],
           properties: [
               {
                   displayName: 'Gateway URL',
                   name: 'gatewayUrl',
                   type: 'string',
                   default: 'http://localhost:8679',
               },
               {
                   displayName: 'Operation',
                   name: 'operation',
                   type: 'options',
                   options: [
                       { name: 'List Tools', value: 'listTools' },
                       { name: 'Call Tool', value: 'callTool' },
                       { name: 'Health Check', value: 'healthCheck' },
                   ],
                   default: 'callTool',
               },
               {
                   displayName: 'Tool Name',
                   name: 'toolName',
                   type: 'string',
                   displayOptions: {
                       show: { operation: ['callTool'] },
                   },
                   placeholder: 'chora-compose.bootstrap_project',
               },
               {
                   displayName: 'Parameters',
                   name: 'parameters',
                   type: 'json',
                   displayOptions: {
                       show: { operation: ['callTool'] },
                   },
               },
           ],
       };

       async execute(this: IExecuteFunctions) {
           const items = this.getInputData();
           const returnData = [];

           for (let i = 0; i < items.length; i++) {
               const operation = this.getNodeParameter('operation', i) as string;
               const gatewayUrl = this.getNodeParameter('gatewayUrl', i) as string;

               if (operation === 'callTool') {
                   const toolName = this.getNodeParameter('toolName', i) as string;
                   const parameters = JSON.parse(this.getNodeParameter('parameters', i) as string);

                   const [namespace, tool] = toolName.split('.');
                   const response = await this.helpers.request({
                       method: 'POST',
                       url: `${gatewayUrl}/tools/${namespace}/${tool}`,
                       body: parameters,
                       json: true,
                   });

                   returnData.push({ json: response });
               }
           }

           return [returnData];
       }
   }
   ```

2. Publish to npm
   ```bash
   # package.json
   {
     "name": "@chora/n8n-node-mcp-gateway",
     "version": "1.0.0",
     "description": "n8n node for calling MCP tools via unified gateway",
     "main": "dist/index.js",
     "types": "dist/index.d.ts",
     "n8n": {
       "nodes": ["dist/nodes/McpGateway/McpGateway.node.js"]
     }
   }

   npm publish --access public
   ```

3. Create workflow templates
   ```json
   {
     "name": "MCP Server Lifecycle - Automated",
     "nodes": [
       {
         "name": "Step 1: Bootstrap",
         "type": "mcpGateway",
         "parameters": {
           "operation": "callTool",
           "toolName": "chora-compose.bootstrap_project",
           "parameters": "{\"namespace\": \"taskmgr\", \"tools\": [\"create\", \"list\"]}"
         }
       },
       {
         "name": "Step 2: Generate Code",
         "type": "mcpGateway",
         "parameters": {
           "operation": "callTool",
           "toolName": "chora-compose.generate_code",
           "parameters": "{\"file\": \"src/tools/create.py\", \"prompt\": \"...\"}"
         }
       }
       // ... 10 more nodes for full lifecycle
     ]
   }
   ```

4. Document Pattern N3b
   ```markdown
   # Pattern N3b: n8n as MCP Client

   n8n workflows can call ANY MCP server via the unified gateway using the custom MCP Gateway node.

   **Installation**:
   ```bash
   npm install -g @chora/n8n-node-mcp-gateway
   ```

   **Usage**:
   1. Add "MCP Gateway" node to workflow
   2. Select operation: "Call Tool"
   3. Enter tool name: `chora-compose.bootstrap_project`
   4. Enter parameters as JSON
   ```

**Success Criteria**:
- [ ] @chora/n8n-node-mcp-gateway published to npm
- [ ] Custom node installable in n8n
- [ ] n8n workflow template for 12-step lifecycle
- [ ] Pattern N3b documented with examples

**Dependencies**: GAP-015 (gateway must exist)

**Unblocks**: v3.0 full automation (n8n-driven lifecycle), recursive n8n pattern

---

## Priority Summary: Critical Path for MCP Vision

### 3 Absolute Blockers (EVS 3.0)

Must be implemented in their respective phases:

1. **GAP-011: ecosystem-manifest Registry** (Phase 2)
   - No registry = no Steps 6, 7, 10, 11
   - Entire MCP lifecycle depends on registry as single source of truth

2. **GAP-014: mcp-orchestration** (Phase 3)
   - No orchestration = no Steps 8-9
   - Manual docker-compose defeats automation vision

3. **GAP-015: mcp-gateway** (Phase 4)
   - No gateway = no Steps 10-12
   - Core of unified vision (ALL clients → gateway → ALL servers)

### 5 Critical Enablers (EVS 2.5+)

Significantly accelerate vision:

1. **GAP-003: Unified Release Workflow** (Phase 3) - EVS 2.55
   - Enables Step 8 (Docker + PyPI unified release)

2. **GAP-012: mcp-server-github** (Phase 4-5) - EVS 2.50
   - Automates Steps 3-4 (GitHub repo creation/commits)

3. **GAP-013: mcp-server-n8n** (Phase 5) - EVS 2.25
   - Enables Step 5 (CI/CD via n8n workflows)
   - Unlocks Pattern N2 (n8n as server)

4. **GAP-019: CHORA_TRACE_ID in chora-compose** (Phase 1) - EVS 2.40
   - Observable v1.0 workflow from Day 1

5. **GAP-020: n8n Custom Node** (Phase 5) - EVS 2.50
   - Enables Pattern N3b (n8n as client)
   - Required for v3.0 full automation

### 4 High Priority (EVS 2.0-2.49)

Improve quality/UX:

1. **GAP-001: Full Trace Propagation** (All phases) - EVS 2.75
   - Observable by Default (Principle #8)

2. **GAP-016: Gateway Config Support** (Phase 4) - EVS 2.30
   - Clients need gateway configs (migration)

3. **GAP-017: Health Endpoint Standard** (Phase 1-3) - EVS 2.30
   - Required for Step 9, gateway health-aware routing

4. **GAP-018: Namespace Collision Detection** (Phase 2) - EVS 2.10
   - Prevents registry corruption

### 7 Medium/Low Priority (EVS <2.0)

Quality improvements, don't block lifecycle:

- GAP-002, GAP-004, GAP-005: Improve v1.0 UX but not blockers
- GAP-006, GAP-007, GAP-008, GAP-009, GAP-010: Quality enhancements

---

## Phase-Specific Recommendations

### Phase 1 (Weeks 1-2): chora-compose Production

**Must-Fix**:
1. **GAP-019** - CHORA_TRACE_ID injection (EVS 2.40) - Observable v1.0
2. **GAP-017** - Health endpoint standard (EVS 2.30) - Prepare for Phase 3
3. **GAP-005** - Pre-commit auto-install (EVS 2.30) - Quality gates

**Nice-to-Have**:
4. **GAP-002** - Coordination → Doc (EVS 2.60) - Improves UX

**Defer**: GAP-001 (full trace), GAP-006 through GAP-010 (quality improvements)

**Success Criteria**:
- [ ] chora-compose accepts trace_id parameter
- [ ] Generated servers have /health endpoints
- [ ] Pre-commit hooks auto-installed on bootstrap
- [ ] v1.0 manual workflow documented (<30 min)

---

### Phase 2 (Weeks 3-4): Registry + Manual Lifecycle

**Must-Fix**:
1. **GAP-011** - ecosystem-manifest (EVS 3.0) - ABSOLUTE BLOCKER
2. **GAP-018** - Namespace collision (EVS 2.10) - Prevents corruption
3. **GAP-001** - Trace propagation (EVS 2.75) - Enable retrospectives

**Nice-to-Have**:
4. **GAP-002** - Coordination → Doc (EVS 2.60) - Streamline workflow

**Defer**: GAP-012 through GAP-015 (manual workarounds exist)

**Success Criteria**:
- [ ] ecosystem-manifest repo with validated registry.yaml
- [ ] ecosystem.register_server tool functional
- [ ] Namespace uniqueness enforced
- [ ] Manual 12-step lifecycle <30 min
- [ ] 3+ servers registered

---

### Phase 3 (Weeks 5-8): Orchestration Layer

**Must-Fix**:
1. **GAP-014** - mcp-orchestration (EVS 2.85) - ABSOLUTE BLOCKER
2. **GAP-003** - Unified release (EVS 2.55) - Docker + PyPI
3. **GAP-010** - Docker health CI (EVS 1.70) - Validate health checks

**Already Fixed** (from Phase 1):
4. **GAP-017** - Health endpoints (implemented in Phase 1)

**Defer**: GAP-012, GAP-013, GAP-015 (not needed for orchestration)

**Success Criteria**:
- [ ] mcp-orchestration deployed
- [ ] orchestration.deploy_server functional (Step 8)
- [ ] orchestration.health_check functional (Step 9)
- [ ] Unified release workflow (Docker + PyPI)
- [ ] Deployment time <2 min

---

### Phase 4 (Weeks 9-12): Gateway Layer

**Must-Fix**:
1. **GAP-015** - mcp-gateway (EVS 3.0) - ABSOLUTE BLOCKER
2. **GAP-016** - Gateway config support (EVS 2.30) - Client migration

**Nice-to-Have**:
3. **GAP-012** - mcp-server-github (EVS 2.50) - Automate Steps 3-4

**Already Fixed** (from previous phases):
4. **GAP-001** - Trace propagation (Phase 2)

**Defer**: GAP-013, GAP-020 (Phase 5 - n8n integration)

**Success Criteria**:
- [ ] mcp-gateway at localhost:8679
- [ ] GET /tools lists all servers
- [ ] POST /tools/{namespace}/{tool} routes correctly
- [ ] Auto-discovery <60s (poll registry)
- [ ] Health-aware routing functional
- [ ] ALL clients tested

---

### Phase 5 (Weeks 13-16): n8n Automation

**Must-Fix**:
1. **GAP-013** - mcp-server-n8n (EVS 2.25) - Pattern N2
2. **GAP-020** - n8n custom node (EVS 2.50) - Pattern N3b

**Nice-to-Have**:
3. **GAP-012** - mcp-server-github (EVS 2.50) - Complete automation
4. **GAP-004** - CI metrics export (EVS 2.45) - Retrospectives

**Already Fixed** (from previous phases):
5. **GAP-015** - Gateway (Phase 4)

**Defer**: GAP-006 through GAP-009 (quality improvements)

**Success Criteria**:
- [ ] mcp-server-n8n deployed (Pattern N2)
- [ ] @chora/n8n-node-mcp-gateway published (Pattern N3b)
- [ ] n8n workflow template for 12-step lifecycle
- [ ] Batch creation: 10 servers in <90 min
- [ ] v2.0 semi-automated workflow <10 min

---

## Next Steps

### Immediate Actions (This Week)

1. **Document MCP gaps** - ✅ DONE (this document)

2. **Plan Phase 1 implementation**:
   - GAP-019: Add trace_id to chora-compose tools
   - GAP-017: Update SAP-003 templates with health endpoints
   - GAP-005: Auto-install pre-commit hooks

3. **Prepare for Phase 2**:
   - Create ecosystem-manifest repository structure
   - Draft registry.yaml schema
   - Design ecosystem.register_server tool spec

### Week 1-2 (Phase 1)

Focus on quick wins that enable observable, quality-gated v1.0 workflow:

1. Implement GAP-019 (trace injection)
2. Implement GAP-017 (health endpoints)
3. Implement GAP-005 (pre-commit auto-install)
4. Update v1.0 manual workflow documentation
5. Test end-to-end with trace propagation

### Week 3-4 (Phase 2)

Build foundational registry:

1. Implement GAP-011 (ecosystem-manifest)
2. Implement GAP-018 (namespace validation)
3. Complete GAP-001 (trace propagation)
4. Prove manual 12-step lifecycle <30 min
5. Register 3+ servers

### Long-Term (Phases 3-5)

Execute critical path:

- **Phase 3**: GAP-014 (orchestration), GAP-003 (unified release)
- **Phase 4**: GAP-015 (gateway), GAP-016 (gateway configs)
- **Phase 5**: GAP-013 (mcp-server-n8n), GAP-020 (n8n node)

---

## Success Metrics

### Phase 1 (v1.0 Manual)

- [ ] Time to create MCP server: <30 min
- [ ] Trace IDs propagated: 100% of Steps 1-2
- [ ] Health endpoints: 100% of generated servers
- [ ] Documentation quality: 3+ examples across clients

### Phase 2 (Registry Foundation)

- [ ] Registry servers registered: 3+
- [ ] Namespace collisions: 0
- [ ] Manual lifecycle time: <30 min
- [ ] Trace coverage: Steps 1-7

### Phase 3 (Orchestration)

- [ ] Deployment automation: Steps 8-9
- [ ] Deployment time: <2 min (vs 10 min manual)
- [ ] Health check reliability: 99%+
- [ ] Unified release: Docker + PyPI in one step

### Phase 4 (Gateway)

- [ ] Gateway uptime: 99.9%
- [ ] Auto-discovery latency: <60s
- [ ] Client types supported: 4+ (Claude, n8n, Python, Bash)
- [ ] Health-aware routing: 100%

### Phase 5 (n8n Automation)

- [ ] Time to create MCP server (n8n): <10 min
- [ ] Batch creation rate: 10 servers in <90 min
- [ ] Automation percentage: 95%+
- [ ] Recursive n8n pattern: Proven

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-03
**Maintainer**: chora-workspace team
**Next Review**: After Phase 1 completion (Week 2)
**Related Documents**:
- [MCP-ECOSYSTEM-VISION-AND-IMPLEMENTATION.md](initiatives/MCP-ECOSYSTEM-VISION-AND-IMPLEMENTATION.md)
- [workflow-continuity-gap-report.md](workflow-continuity-gap-report.md)
- [context-flow-diagram.md](context-flow-diagram.md)
