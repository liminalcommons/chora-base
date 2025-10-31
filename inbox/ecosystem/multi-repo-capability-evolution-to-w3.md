# Multi-Repo Capability Evolution: Path to Waypoint W3

**Document Type:** Cross-Repository Capability Evolution
**Created:** 2025-10-26
**Target Milestone:** Waypoint W3 - Health Monitoring & Auto-Recovery
**Timeline:** Q4 2025 - Q1 2026
**Maintainer:** Ecosystem Coordination Team

---

## Executive Summary

This document provides coordinated capability evolution across **four repositories** to achieve **Waypoint W3: Health Monitoring and Auto-Recovery** by Q1 2026. It replaces individual repository evolution documents with a single integrated view showing dependencies, timelines, and integration points.

**Goal:** Enable automatic health monitoring where unhealthy backends are detected and isolated, with auto-recovery attempts, while healthy backends continue serving requests unaffected.

**Success Criteria:**
- ✅ Health failure detection in <90 seconds
- ✅ Gateway routing updated in <5 seconds
- ✅ Healthy backends remain unaffected
- ✅ Clear user error messages
- ✅ Automatic recovery attempts logged
- ✅ Service restoration without manual intervention

---

## Repository Scope

### Four Repositories Involved

| Repository | Type | Role | Current State |
|------------|------|------|---------------|
| **ecosystem-manifest** | Standards/Registry | Single source of truth for ecosystem servers | 🆕 New (to be created) |
| **mcp-orchestration** | Service | MCP server lifecycle management | 🆕 New (to be created) |
| **mcp-gateway** | Service | MCP protocol aggregator and router | ✅ Exists (v1.1.0) |
| **chora-base** | Template/Framework | Project scaffolding and standards | ✅ Exists (v3.3.0) |

### Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Claude Desktop                         │
│                  (Single MCP Connection)                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                     mcp-gateway                             │
│              • Aggregates backend tools                     │
│              • Health-aware routing (W3)                    │
│              • Queries orchestration for status             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                  mcp-orchestration                          │
│              • Reads ecosystem-manifest                     │
│              • Deploys Docker containers                    │
│              • Health monitoring (W3)                       │
│              • Auto-recovery (W3)                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                 ecosystem-manifest                          │
│              • Server registry (YAML)                       │
│              • Quality standards                            │
│              • Health check specs (W3)                      │
│              • Update policies                              │
└─────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                     chora-base                              │
│              • MCP server template                          │
│              • Health endpoint standard (W3)                │
│              • DRSO validation                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Wave 1: Foundation (Q4 2025, Weeks 1-8)

**Goal:** Establish core infrastructure for ecosystem discovery and deployment
**Target:** Waypoint W1 validation (Deploy new server in <5 minutes)
**Timeline:** 8 weeks (Sprint 1-4, November-December 2025)

### Week-by-Week Breakdown

#### Weeks 1-2: Repository Creation & Standards

**ecosystem-manifest (NEW REPO)**

```yaml
actions:
  - create_repository:
      org: liminalcommons
      name: ecosystem-manifest
      description: "Single source of truth for Liminal Commons MCP ecosystem"

  - initialize_structure:
      files:
        - README.md
        - ecosystem-manifest.yaml
        - QUALITY_STANDARDS.md
        - TRUST_MODEL.md
        - CONTRIBUTING.md
        - GOVERNANCE.md

  - define_manifest_schema:
      version: "1.0"
      includes:
        - server_metadata
        - docker_configuration
        - config_requirements
        - version_strategy

  - add_initial_servers:
      count: 3
      servers:
        - mcp-server-lightrag
        - mcp-server-n8n
        - mcp-server-coda
```

**Deliverables:**
- ✅ Repository created and initialized
- ✅ Manifest schema v1.0 defined
- ✅ 3 servers declared with complete metadata
- ✅ Quality standards documented (chora-base requirement, 85% coverage, health endpoint)
- ✅ Trust model documented (liminalcommons org only)

**chora-base (EXISTING - UPDATE)**

```yaml
actions:
  - create_mcp_template:
      path: templates/mcp-server/
      includes:
        - pyproject.toml (MCP server metadata)
        - src/server.py (FastMCP skeleton)
        - src/health.py (Health endpoint standard)
        - tests/ (Test structure)
        - Dockerfile (Multi-stage build)
        - docker-compose.yml (Development setup)

  - document_mcp_standards:
      file: docs/mcp-server-template.md
      sections:
        - Project structure
        - Health endpoint requirements
        - Configuration patterns
        - Docker best practices
```

**Deliverables:**
- ✅ MCP server template in chora-base
- ✅ Health endpoint standard defined (`/health` returns JSON with status)
- ✅ Template documentation complete
- ✅ Example server using template (mcp-server-example)

**Dependencies:**
- None (foundational)

**Blockers:**
- None

---

#### Weeks 3-4: Orchestration Core

**mcp-orchestration (NEW REPO)**

```yaml
actions:
  - create_repository:
      org: liminalcommons
      name: mcp-orchestration
      template: chora-base

  - implement_core:
      components:
        - manifest_parser:
            reads: ecosystem-manifest.yaml
            validates: schema v1.0
            caches: server metadata

        - docker_manager:
            uses: docker-py
            manages: container lifecycle
            handles: images, networks, volumes

        - mcp_tools:
            exposes:
              - list_servers()
              - deploy_server()
              - server_status()
              - stop_server()

        - http_api:
            endpoints:
              - GET /servers (list available)
              - POST /servers/{id}/deploy
              - GET /servers/{id}/status
              - DELETE /servers/{id}
```

**Deliverables:**
- ✅ Repository created from chora-base template
- ✅ Manifest parser working with 3 servers
- ✅ Docker container management functional
- ✅ 4 MCP tools implemented and tested
- ✅ HTTP API for gateway integration
- ✅ SQLite state storage

**Dependencies:**
- ✅ ecosystem-manifest repo exists (Weeks 1-2)
- ✅ chora-base MCP template available (Weeks 1-2)

**Blockers:**
- ecosystem-manifest must have valid schema

---

#### Weeks 5-6: Gateway Integration

**mcp-gateway (EXISTING - UPDATE)**

```yaml
actions:
  - add_orchestration_client:
      file: src/mcp_gateway/orchestration.py
      implements:
        - query_available_backends()
        - get_backend_status()
        - subscribe_to_status_updates()

  - update_discovery_loop:
      file: src/mcp_gateway/discovery.py
      changes:
        - Add orchestration as discovery source
        - Poll orchestration every 30s
        - Auto-register discovered backends
        - Remove backends when stopped

  - add_http_transport:
      file: src/mcp_gateway/transports/http.py
      implements:
        - HTTP client for remote MCP servers
        - Connection pooling
        - Timeout handling
        - Error recovery
```

**Deliverables:**
- ✅ Orchestration HTTP client implemented
- ✅ Auto-discovery from orchestration working
- ✅ HTTP transport for remote backends
- ✅ Backends register within 5 seconds of deployment
- ✅ mcp-gateway v1.2.0 released

**Dependencies:**
- ✅ mcp-orchestration HTTP API available (Weeks 3-4)
- ✅ mcp-orchestration deploying servers (Weeks 3-4)

**Blockers:**
- mcp-orchestration must expose HTTP API

---

#### Weeks 7-8: End-to-End Validation

**All Repos - Integration Testing**

```yaml
actions:
  - waypoint_w1_validation:
      test_scenario:
        given: "ecosystem-manifest has mcp-server-github"
        when: "User runs: mcp-orchestration deploy mcp-server-github"
        then:
          - Orchestration pulls GitHub server template
          - Deploys container with health endpoint
          - Gateway detects new backend via polling
          - Gateway loads manifest and registers backend
          - User sees github.* tools in Claude Desktop

      validation_criteria:
        - Deployment completes in <60 seconds
        - Gateway registers backend in <5 seconds
        - Tools appear immediately
        - Health endpoint returns 200 OK
        - Zero manual configuration required

  - documentation:
      create:
        - how-to-setup-mcp-ecosystem.md
        - how-to-deploy-new-mcp-server.md
        - troubleshooting-guide.md

  - release_preparation:
      versions:
        - ecosystem-manifest v1.0.0
        - mcp-orchestration v0.3.0
        - mcp-gateway v1.2.0
        - chora-base v3.4.0
```

**Deliverables:**
- ✅ Waypoint W1 validated end-to-end
- ✅ All how-to guides executable
- ✅ Troubleshooting guide complete
- ✅ All repos tagged with Wave 1 versions

**Dependencies:**
- ✅ All previous weeks complete

**Blockers:**
- Any integration issues must be resolved

---

### Wave 1 Summary

**Repositories:**
- 🆕 ecosystem-manifest v1.0.0
- 🆕 mcp-orchestration v0.3.0
- 🔄 mcp-gateway v1.2.0
- 🔄 chora-base v3.4.0

**Capabilities Delivered:**
- ✅ Ecosystem registry with 3 servers
- ✅ Docker-based server deployment
- ✅ MCP tools for discovery
- ✅ Gateway auto-discovery
- ✅ HTTP transport
- ✅ MCP server template

**Integration Waypoints:**
- ✅ W1: Basic Discovery & Deployment

**Success Metrics:**
- Deployment time: <60 seconds ✅
- Gateway discovery: <5 seconds ✅
- End-to-end: <5 minutes ✅
- Test coverage: 85%+ ✅
- Zero manual config ✅

---

## Wave 2: Lifecycle Management (Q1 2026, Weeks 9-16)

**Goal:** Automatic updates and health monitoring with auto-recovery
**Target:** Waypoints W2 & W3 validation
**Timeline:** 8 weeks (Sprint 5-8, January-February 2026)

### Week-by-Week Breakdown

#### Weeks 9-10: Health Specifications

**ecosystem-manifest (UPDATE)**

```yaml
actions:
  - add_health_specifications:
      manifest_version: "1.1"
      per_server:
        health_check:
          endpoint: /health
          interval_seconds: 30
          timeout_seconds: 5
          failure_threshold: 3
          success_threshold: 2

        restart_policy: always | on-failure | unless-stopped

        health_check_response:
          required_fields:
            - status: "healthy" | "unhealthy" | "degraded"
            - version: semver
            - uptime_seconds: number
          optional_fields:
            - dependencies: object
            - metrics: object

  - add_update_policies:
      per_server:
        auto_update: boolean
        version_strategy: latest | pinned | semantic
        rollback_on_failure: boolean
        notification_channel: string?

  - update_quality_standards:
      requires:
        - Health endpoint implementation
        - Health check response format compliance
        - Graceful shutdown handling (SIGTERM)
```

**Deliverables:**
- ✅ Manifest schema v1.1 with health specs
- ✅ All 3 servers updated with health configs
- ✅ Update policy documentation
- ✅ Health check response format standard

**chora-base (UPDATE)**

```yaml
actions:
  - enhance_health_endpoint:
      file: templates/mcp-server/src/health.py
      adds:
        - Dependency health checks
        - Metrics collection
        - Graceful degradation states
        - Structured logging

  - add_shutdown_handler:
      file: templates/mcp-server/src/server.py
      implements:
        - SIGTERM handler
        - Connection draining
        - State cleanup
        - Graceful exit codes
```

**Deliverables:**
- ✅ Enhanced health endpoint in template
- ✅ Graceful shutdown standard
- ✅ Example implementations
- ✅ chora-base v3.5.0

**Dependencies:**
- Wave 1 complete

**Blockers:**
- None

---

#### Weeks 11-12: Health Monitoring

**mcp-orchestration (UPDATE)**

```yaml
actions:
  - implement_health_monitor:
      component: HealthMonitor
      runs: background process
      checks:
        - Poll all deployed servers every 30s
        - HTTP GET to /health endpoint
        - Track consecutive failures
        - Track consecutive successes
        - State: healthy | degraded | unhealthy

      state_transitions:
        - healthy → degraded: 1 failure
        - degraded → unhealthy: 3 consecutive failures
        - unhealthy → degraded: 1 success
        - degraded → healthy: 2 consecutive successes

  - implement_auto_recovery:
      component: RecoveryManager
      triggers:
        - on: backend marked unhealthy
        - attempts: 3 recovery tries
        - backoff: exponential (30s, 60s, 120s)

      recovery_actions:
        - attempt_restart()
        - redeploy_container()
        - notify_admin()

  - add_mcp_tools:
      new_tools:
        - health_check(server_id: string)
        - health_events(server_id: string, limit: int)
        - restart_server(server_id: string)

  - update_http_api:
      new_endpoints:
        - GET /servers/{id}/health
        - GET /servers/{id}/health/events
        - POST /servers/{id}/restart
        - GET /health/status (all servers)
```

**Deliverables:**
- ✅ Background health monitoring
- ✅ Auto-recovery with backoff
- ✅ Health event logging
- ✅ Recovery attempt tracking
- ✅ HTTP API for gateway integration
- ✅ mcp-orchestration v0.6.0

**Dependencies:**
- ✅ Manifest v1.1 with health specs (Weeks 9-10)
- ✅ Servers have health endpoints (Wave 1)

**Blockers:**
- Health endpoint standard must be finalized

---

#### Weeks 13-14: Gateway Health-Aware Routing

**mcp-gateway (UPDATE)**

```yaml
actions:
  - implement_health_tracking:
      component: HealthTracker
      subscribes_to: orchestration health updates
      maintains:
        - backend_health: Map<backend_id, health_status>
        - last_health_check: Map<backend_id, timestamp>
        - health_transitions: EventLog

  - implement_health_aware_routing:
      updates: src/mcp_gateway/router.py
      routing_logic:
        - if backend.health == "healthy": route normally
        - if backend.health == "degraded": route with warning
        - if backend.health == "unhealthy": return error

      error_responses:
        - error_code: BACKEND_UNHEALTHY
        - message: "Backend '{backend}' is currently unhealthy"
        - suggested_action: "Try again later or contact support"
        - affected_tools: [list of tool names]

  - add_health_endpoints:
      new_endpoints:
        - GET /health (gateway overall health)
        - GET /backends (includes health status)
        - GET /backends/{id}/health

  - implement_hot_reload:
      updates: backend registration
      enables:
        - Update backend without gateway restart
        - Preserve active MCP sessions
        - Zero-downtime backend updates
```

**Deliverables:**
- ✅ Health-aware routing implemented
- ✅ Clear error messages for unhealthy backends
- ✅ Health status in backend list
- ✅ Hot-reload without downtime
- ✅ mcp-gateway v1.3.0

**Dependencies:**
- ✅ Orchestration health monitoring (Weeks 11-12)
- ✅ Health event API available (Weeks 11-12)

**Blockers:**
- Orchestration must expose real-time health updates

---

#### Weeks 15-16: End-to-End Validation & Updates

**All Repos - Integration Testing**

```yaml
actions:
  - waypoint_w2_validation:
      test_scenario: "Automatic Updates"
      given: "mcp-server-github v1.0.0 deployed"
      when: "v1.1.0 released to ecosystem"
      then:
        - Orchestration detects update in <5 minutes
        - Orchestration deploys update automatically
        - Gateway hot-reloads backend without restart
        - Zero downtime during update
        - Active sessions preserved

      validation_criteria:
        - Update detection: <5 minutes
        - Deployment: <30 seconds
        - Gateway downtime: 0 seconds
        - Session preservation: 100%

  - waypoint_w3_validation:
      test_scenario: "Health Monitoring & Auto-Recovery"
      given: "5 backends deployed, 1 becomes unhealthy"
      when: "Backend fails 3 consecutive health checks"
      then:
        - Orchestration marks backend unhealthy (<90 seconds)
        - Gateway stops routing to unhealthy backend (<5 seconds)
        - Users get clear error messages
        - Orchestration attempts auto-recovery (3 tries)
        - Healthy backends unaffected
        - Backend recovers and routing restores

      validation_criteria:
        - Failure detection: <90 seconds
        - Routing update: <5 seconds
        - Healthy backends: 0 impact
        - Error messages: clear and actionable
        - Auto-recovery: attempted and logged

  - update_management_validation:
      test_scenario: "Background Updates"
      features:
        - Background update checking
        - Update policies (auto vs manual)
        - Rollback on failure
        - Audit trail

  - documentation:
      create:
        - how-to-enable-automatic-updates.md
        - how-to-configure-health-monitoring.md
        - health-check-specification.md
        - troubleshooting-unhealthy-backends.md
```

**Deliverables:**
- ✅ Waypoint W2 validated (automatic updates)
- ✅ Waypoint W3 validated (health monitoring)
- ✅ All how-to guides executable and tested
- ✅ Health check specification finalized
- ✅ All repos tagged with Wave 2 versions

**Dependencies:**
- ✅ All previous weeks complete
- ✅ Health monitoring implemented
- ✅ Health-aware routing implemented

**Blockers:**
- Any W2 or W3 validation failures must be fixed

---

### Wave 2 Summary

**Repositories:**
- 🔄 ecosystem-manifest v1.1.0
- 🔄 mcp-orchestration v0.6.0
- 🔄 mcp-gateway v1.3.0
- 🔄 chora-base v3.5.0

**Capabilities Delivered:**
- ✅ Background health monitoring (30s interval)
- ✅ Auto-recovery with exponential backoff
- ✅ Health-aware routing in gateway
- ✅ Hot-reload without downtime
- ✅ Automatic update detection and deployment
- ✅ Update policies and rollback
- ✅ Health event audit trail

**Integration Waypoints:**
- ✅ W2: Automatic Updates
- ✅ W3: Health Monitoring & Auto-Recovery

**Success Metrics:**
- Health failure detection: <90s ✅
- Gateway routing update: <5s ✅
- Healthy backend impact: 0% ✅
- Update detection: <5min ✅
- Update deployment: <30s ✅
- Gateway downtime: 0s ✅
- Auto-recovery attempts: logged ✅

---

## Cross-Repo Dependencies

### Dependency Graph

```
Week 1-2 (Foundation):
  ecosystem-manifest [NEW] ← (defines standards)
       ↓
  chora-base [UPDATE] ← (implements standards)
       ↓
  [READY FOR WEEKS 3-4]

Week 3-4 (Orchestration):
  mcp-orchestration [NEW] ← (reads manifest, uses template)
       ↓
  [READY FOR WEEKS 5-6]

Week 5-6 (Gateway):
  mcp-gateway [UPDATE] ← (queries orchestration)
       ↓
  [READY FOR WEEKS 7-8]

Week 7-8 (W1 Validation):
  All repos integrated and tested
       ↓
  [WAVE 1 COMPLETE - READY FOR WAVE 2]

Week 9-10 (Health Specs):
  ecosystem-manifest [UPDATE] ← (defines health specs)
       ↓
  chora-base [UPDATE] ← (implements health template)
       ↓
  [READY FOR WEEKS 11-12]

Week 11-12 (Health Monitoring):
  mcp-orchestration [UPDATE] ← (monitors health)
       ↓
  [READY FOR WEEKS 13-14]

Week 13-14 (Health Routing):
  mcp-gateway [UPDATE] ← (routes by health)
       ↓
  [READY FOR WEEKS 15-16]

Week 15-16 (W2 & W3 Validation):
  All repos integrated and tested
       ↓
  [WAVE 2 COMPLETE - W3 ACHIEVED]
```

### Critical Path

The **critical path** to W3 is:

1. **Weeks 1-2:** ecosystem-manifest + chora-base (parallel, no blockers)
2. **Weeks 3-4:** mcp-orchestration (blocked by 1-2)
3. **Weeks 5-6:** mcp-gateway (blocked by 3-4)
4. **Weeks 7-8:** W1 validation (blocked by 5-6)
5. **Weeks 9-10:** Health specs (blocked by 7-8)
6. **Weeks 11-12:** Health monitoring (blocked by 9-10)
7. **Weeks 13-14:** Health routing (blocked by 11-12)
8. **Weeks 15-16:** W2 & W3 validation (blocked by 13-14)

**Total Duration:** 16 weeks (4 months)
**Target Completion:** February 2026

---

## Integration Points

### API Contracts

#### mcp-orchestration → ecosystem-manifest

```yaml
integration: Read manifest
protocol: File system
contract:
  reads: ecosystem-manifest.yaml
  validates: schema version
  parses: server metadata

breaking_changes:
  - Schema version change
  - Required field additions

notification: GitHub issue in orchestration repo
```

#### mcp-gateway → mcp-orchestration

```yaml
integration: Query backends
protocol: HTTP REST API
contract:
  endpoints:
    - GET /servers (list available)
    - GET /servers/{id}/status
    - GET /servers/{id}/health
    - GET /health/status (all servers)

  polling:
    - Interval: 30 seconds
    - Timeout: 5 seconds

  response_format:
    - JSON with snake_case keys
    - ISO 8601 timestamps

breaking_changes:
  - Endpoint URL changes
  - Response schema changes
  - Authentication requirements

notification: Slack #ecosystem-dev + GitHub issue
```

#### MCP Servers → Health Standard

```yaml
integration: Health endpoint
protocol: HTTP GET
contract:
  endpoint: /health
  method: GET
  response:
    status_code: 200 | 503
    content_type: application/json
    body:
      status: "healthy" | "degraded" | "unhealthy"
      version: semver
      uptime_seconds: number
      dependencies?: object
      metrics?: object

breaking_changes:
  - Response format changes
  - New required fields

notification: Update chora-base template + ecosystem-manifest
```

---

## Risk Management

### High-Risk Areas

#### Risk 1: Docker Socket Access

**Probability:** Medium
**Impact:** High
**Description:** mcp-orchestration requires Docker socket access to spawn containers

**Mitigation:**
- Document security implications clearly
- Use read-only mounts where possible
- Validate images before deployment
- Implement resource limits
- Provide Docker Desktop installation guide

**Contingency:**
- Fallback to kubernetes/docker-compose if Docker socket unavailable
- Manual deployment mode

#### Risk 2: Health Check False Positives

**Probability:** Medium
**Impact:** Medium
**Description:** Network glitches cause temporary health check failures

**Mitigation:**
- Require 3 consecutive failures before marking unhealthy
- Exponential backoff for recovery attempts
- Configurable thresholds per server
- Detailed health event logging

**Contingency:**
- Manual override to force healthy state
- Increase failure threshold temporarily

#### Risk 3: Gateway Hot-Reload Complexity

**Probability:** Medium
**Impact:** High
**Description:** Hot-reloading backends without dropping sessions is complex

**Mitigation:**
- Extensive testing of session preservation
- Implement connection draining
- Maintain backward compatibility
- Provide rollback mechanism

**Contingency:**
- Fall back to restart-required updates
- Schedule updates during low-traffic windows

#### Risk 4: Cross-Repo Coordination

**Probability:** High
**Impact:** Medium
**Description:** Four repos with dependencies risk schedule slips

**Mitigation:**
- Weekly sync meetings
- Shared project board
- Clear API contracts upfront
- Integration testing every 2 weeks

**Contingency:**
- Extend timeline by 2 weeks if needed
- Reduce Wave 2 scope (defer W2, keep W3)

### Dependency Risks

| Week | Dependency Risk | Mitigation |
|------|----------------|------------|
| 3-4 | Manifest schema unclear | Prototype schema in week 1 |
| 5-6 | Orchestration API changes | Lock API contract in week 3 |
| 7-8 | Integration issues found late | Bi-weekly integration tests |
| 11-12 | Health spec ambiguity | Spec review in week 9 |
| 13-14 | Gateway complexity underestimated | Allocate 1 week buffer |
| 15-16 | Validation failures | Address issues in week 14 |

---

## Communication Plan

### Weekly Updates

**Channel:** Slack #ecosystem-dev
**Format:** Standup-style update
**Content:**
- Progress this week
- Blockers
- Next week plans
- Help needed

**Template:**
```
📅 Week N Update - [Repo Name]

✅ Completed:
- [Achievement 1]
- [Achievement 2]

🚧 In Progress:
- [Task 1]
- [Task 2]

❌ Blocked:
- [Blocker 1] - needs [dependency]

➡️ Next Week:
- [Plan 1]
- [Plan 2]

🆘 Help Needed:
- [Request 1]
```

### Bi-Weekly Integration Sync

**When:** Every 2 weeks (Weeks 2, 4, 6, 8, 10, 12, 14, 16)
**Duration:** 60 minutes
**Attendees:** All repo maintainers + coordinator

**Agenda:**
1. Integration status review (15 min)
2. API contract validation (15 min)
3. Risk assessment (15 min)
4. Next sprint planning (15 min)

### Monthly Stakeholder Update

**When:** End of each month
**Duration:** 30 minutes
**Attendees:** Maintainers + leadership

**Content:**
- Wave progress (% complete)
- Waypoint status
- Timeline health (on track / at risk)
- Decisions needed
- Celebrate wins

---

## Success Metrics Dashboard

### Wave 1 Metrics (Weeks 1-8)

| Metric | Target | Week 8 Status |
|--------|--------|---------------|
| Repos created | 2 | ⏳ Pending |
| Manifest schema version | 1.0 | ⏳ Pending |
| Servers in manifest | 3 | ⏳ Pending |
| MCP tools implemented | 4 | ⏳ Pending |
| Gateway backends supported | 3+ | ⏳ Pending |
| Deployment time | <60s | ⏳ Pending |
| Test coverage | 85%+ | ⏳ Pending |
| W1 validation | Pass | ⏳ Pending |

### Wave 2 Metrics (Weeks 9-16)

| Metric | Target | Week 16 Status |
|--------|--------|----------------|
| Health monitoring interval | 30s | ⏳ Pending |
| Failure detection time | <90s | ⏳ Pending |
| Gateway routing update | <5s | ⏳ Pending |
| Auto-recovery attempts | 3 | ⏳ Pending |
| Update detection time | <5min | ⏳ Pending |
| Update deployment time | <30s | ⏳ Pending |
| Gateway downtime | 0s | ⏳ Pending |
| W2 validation | Pass | ⏳ Pending |
| W3 validation | Pass | ⏳ Pending |

### Quality Gates

All repos must meet these before wave completion:

**Code Quality:**
- ✅ Test coverage ≥85%
- ✅ All tests passing
- ✅ No critical security issues
- ✅ Code review approved
- ✅ DRSO validation passed

**Documentation:**
- ✅ README updated
- ✅ API docs generated
- ✅ How-to guides executable
- ✅ Troubleshooting guide complete

**Integration:**
- ✅ API contracts validated
- ✅ Cross-repo tests passing
- ✅ Waypoint validation complete

---

## Deployment Strategy

### Wave 1 Deployment (Week 8)

```bash
# 1. Tag all repos
cd ecosystem-manifest && git tag v1.0.0 && git push --tags
cd ../mcp-orchestration && git tag v0.3.0 && git push --tags
cd ../mcp-gateway && git tag v1.2.0 && git push --tags
cd ../chora-base && git tag v3.4.0 && git push --tags

# 2. Build Docker images
cd mcp-orchestration && docker build -t liminalcommons/mcp-orchestration:0.3.0 .
cd ../mcp-gateway && docker build -t liminalcommons/mcp-gateway:1.2.0 .

# 3. Publish to registries
docker push liminalcommons/mcp-orchestration:0.3.0
docker push liminalcommons/mcp-gateway:1.2.0
pip publish chora-base  # PyPI

# 4. Release bootstrap container
docker build -t liminalcommons/mcp-ecosystem:1.0 .
docker push liminalcommons/mcp-ecosystem:1.0

# 5. Validate W1
./scripts/validate-waypoint-w1.sh

# 6. Announce
# - GitHub releases for all repos
# - Slack #announcements
# - Update ecosystem status page
```

### Wave 2 Deployment (Week 16)

```bash
# 1. Tag all repos
cd ecosystem-manifest && git tag v1.1.0 && git push --tags
cd ../mcp-orchestration && git tag v0.6.0 && git push --tags
cd ../mcp-gateway && git tag v1.3.0 && git push --tags
cd ../chora-base && git tag v3.5.0 && git push --tags

# 2. Build Docker images
cd mcp-orchestration && docker build -t liminalcommons/mcp-orchestration:0.6.0 .
cd ../mcp-gateway && docker build -t liminalcommons/mcp-gateway:1.3.0 .

# 3. Publish
docker push liminalcommons/mcp-orchestration:0.6.0
docker push liminalcommons/mcp-gateway:1.3.0
pip publish chora-base

# 4. Update bootstrap container
docker build -t liminalcommons/mcp-ecosystem:1.1 .
docker push liminalcommons/mcp-ecosystem:1.1

# 5. Validate W2 & W3
./scripts/validate-waypoint-w2.sh
./scripts/validate-waypoint-w3.sh

# 6. Announce with metrics
# - Health monitoring stats
# - Uptime improvements
# - User testimonials
```

---

## Rollback Plan

### Wave 1 Rollback

If critical issues found after Wave 1 deployment:

```bash
# 1. Identify issue severity
# Critical: rollback immediately
# High: fix within 24h or rollback
# Medium: fix in patch release

# 2. Rollback images
docker tag liminalcommons/mcp-orchestration:0.2.0 :0.3.0
docker tag liminalcommons/mcp-gateway:1.1.0 :1.2.0
docker push --all-tags

# 3. Notify users
# - Slack announcement
# - Update status page
# - Provide migration guide

# 4. Root cause analysis
# - Document issue
# - Add regression test
# - Schedule fix for Week 9
```

### Wave 2 Rollback

More complex due to schema changes:

```bash
# 1. Check manifest compatibility
# If manifest v1.1 breaks v1.0 parsers: CRITICAL

# 2. Rollback with data migration
./scripts/rollback-to-wave1.sh
# - Downgrade images
# - Migrate health data
# - Disable health-aware routing

# 3. Provide upgrade path
# - Fix issues in branch
# - Test thoroughly
# - Gradual re-rollout
```

---

## Post-W3 Roadmap

After achieving Waypoint W3 (end of Wave 2), the ecosystem will have:

✅ **Core Infrastructure:**
- Ecosystem registry with versioning
- Lifecycle management (deploy, update, health, recovery)
- Health-aware routing
- Auto-update capability

**Next Priorities (Wave 3+):**
- Community contribution infrastructure
- Quality validation automation
- Capability-based search
- Registry service (if ecosystem scales to 25+ servers)

**Decision Point:** Q1 2026
Review ecosystem adoption and decide between:
- **Option A:** Focus on stability and refinement (if 5-10 servers)
- **Option B:** Scale infrastructure (if 10-25 servers)
- **Option C:** Build registry service (if 25+ servers)

---

## Appendix: Quick Reference

### Repository URLs

- ecosystem-manifest: https://github.com/liminalcommons/ecosystem-manifest
- mcp-orchestration: https://github.com/liminalcommons/mcp-orchestration
- mcp-gateway: https://github.com/liminalcommons/mcp-gateway
- chora-base: https://github.com/liminalcommons/chora-base

### Key Documents

- [how-to-setup-mcp-ecosystem.md](how-to-setup-mcp-ecosystem.md)
- [how-to-deploy-new-mcp-server.md](how-to-deploy-new-mcp-server.md)
- [how-to-enable-automatic-updates.md](how-to-enable-automatic-updates.md)
- [how-to-configure-health-monitoring.md](how-to-configure-health-monitoring.md)

### Slack Channels

- #ecosystem-dev - Development coordination
- #ecosystem-architecture - Architecture decisions
- #announcements - Release announcements

### Meeting Schedule

- **Weekly standup:** Mondays 10am (async Slack)
- **Bi-weekly sync:** Tuesdays 2pm (Weeks 2, 4, 6, ...)
- **Monthly stakeholder:** Last Friday 3pm

---

**Document Status:** Active
**Last Updated:** 2025-10-26
**Next Review:** 2025-11-01 (Wave 1 kickoff)
**Maintainer:** Ecosystem Coordination Team

---

**Signatures:**

- [ ] ecosystem-manifest maintainer: _______________ Date: ___________
- [ ] mcp-orchestration maintainer: _______________ Date: ___________
- [ ] mcp-gateway maintainer: _______________ Date: ___________
- [ ] chora-base maintainer: _______________ Date: ___________
- [ ] Ecosystem coordinator (Victor): _______________ Date: ___________
