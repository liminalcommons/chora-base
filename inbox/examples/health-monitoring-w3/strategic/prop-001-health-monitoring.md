---
type: strategic-proposal
proposal_id: prop-001
title: "Waypoint W3: Health Monitoring & Auto-Recovery for MCP Ecosystem"
created: 2025-10-27
author: Victor Piper
status: accepted
impact:
  - chora-base
  - ecosystem-manifest
  - mcp-orchestration
  - mcp-gateway
trace_id: ecosystem-w3-health-monitoring
---

# Strategic Proposal: Health Monitoring & Auto-Recovery (W3)

## Summary

Implement comprehensive health monitoring and auto-recovery capabilities across the MCP ecosystem. This enables production-grade reliability by detecting failed servers, automatically recovering them, and providing real-time health status to clients. This is Waypoint W3 in our ecosystem roadmap, building on W1 (Basic Setup) and W2 (Lifecycle Management).

**Strategic Alignment**: Moves ecosystem from "prototype" to "production-ready" by addressing operational reliability.

---

## Problem Statement

Currently, our MCP ecosystem has no systematic way to:
1. **Detect server failures** - If an MCP server crashes, nothing notices
2. **Recover automatically** - Manual intervention required to restart servers
3. **Report health status** - Clients don't know if servers are healthy
4. **Track reliability metrics** - No visibility into uptime, failure rates
5. **Debug production issues** - No structured health events or traces

This means:
- Users experience silent failures (requests timeout with no explanation)
- Developers must manually monitor logs and restart servers
- No SLA measurement or reliability improvements possible
- Production deployments are fragile and require constant manual attention

**Pain Point**: A single MCP server failure can block all work until someone notices and manually restarts it. This is unacceptable for production use.

---

## Proposed Solution

### Overview
Implement a standardized health monitoring system with four components:

1. **Health Endpoint Template** (chora-base)
   - Standardized `/health` endpoint for all MCP servers
   - JSON response format with status, uptime, last_check
   - Template integrated into chora-base MCP server template

2. **Health Check Specification** (ecosystem-manifest)
   - Formal spec defining health endpoint contract
   - JSON schema for health responses
   - Quality standards for ecosystem inclusion

3. **Health Monitoring Service** (mcp-orchestration)
   - Polls all registered servers every 30 seconds
   - Detects failures (no response, error status, timeout)
   - Auto-recovery: restarts failed servers automatically
   - Emits health events to trace context

4. **Health Status Aggregation** (mcp-gateway)
   - Aggregates health status from mcp-orchestration
   - Exposes `/health/ecosystem` endpoint for clients
   - Real-time WebSocket updates on status changes
   - Dashboard view of ecosystem health

### Architecture
```
┌─────────────────┐
│  mcp-gateway    │  Aggregates & exposes health status
│  /health/       │  WebSocket notifications
│  ecosystem      │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ mcp-orchestration│ Monitors all servers
│ Health Monitor  │  Auto-recovery
│ (30s polling)   │  Event emission
└────────┬────────┘
         │
         v
┌─────────────────┐
│  MCP Servers    │  Expose /health endpoint
│  /health        │  Status: ok/degraded/down
│  (FastMCP)      │  Uptime, last_check
└─────────────────┘
```

---

## Business Value

### For Users
- **Reliability**: Silent failures become visible, auto-recovery reduces downtime
- **Transparency**: Real-time health status builds trust
- **Performance**: Faster debugging with health event traces

### For Developers
- **Automation**: No manual server restarts
- **Observability**: Structured health events enable monitoring
- **Standards**: Clear health endpoint contract for all servers

### For Ecosystem
- **Production-Ready**: Waypoint W3 unblocks production deployments
- **Quality Gate**: Health endpoint becomes ecosystem inclusion requirement
- **Metrics**: Foundation for SLA measurement and reliability improvements

**Estimated Impact**: Reduces manual intervention by 80%, enables 99.5% uptime SLA.

---

## Timeline Estimate

**Total Duration**: 16 weeks (4 repos, parallel + sequential work)

### Phase 1: Strategic & Standards (Weeks 1-4)
- Week 1-2: Proposal review and acceptance
- Week 3-4: RFC process, ADR creation

### Phase 2: Coordination (Weeks 5-6)
- Create coordination requests for all 4 repos
- Sprint planning triage

### Phase 3: Implementation (Weeks 7-16)
- **Weeks 7-10**: Foundation
  - chora-base: Health endpoint template (parallel)
  - ecosystem-manifest: Health check spec (parallel)
- **Weeks 11-13**: Monitoring
  - mcp-orchestration: Health monitoring service (depends on spec)
- **Weeks 14-16**: Aggregation & Integration
  - mcp-gateway: Status aggregation (depends on monitoring)
  - Integration testing, W3 validation

---

## Alternatives Considered

### Alternative 1: External Monitoring (Prometheus/Grafana)
**Approach**: Use Prometheus to scrape health endpoints, Grafana for dashboards
**Rejected Because**:
- Adds external infrastructure dependencies
- Doesn't integrate with our trace context system
- No auto-recovery built-in
- Overkill for our current scale

### Alternative 2: No Health Monitoring (Status Quo)
**Approach**: Continue manual monitoring and restarts
**Rejected Because**:
- Blocks production use
- Doesn't scale beyond 2-3 developers
- No path to SLA measurement

### Alternative 3: Health Checks in mcp-gateway Only
**Approach**: Have gateway directly poll MCP servers
**Rejected Because**:
- Gateway shouldn't know about all servers (violates orchestration pattern)
- No auto-recovery (gateway doesn't manage containers)
- Couples gateway to server lifecycle

---

## Success Metrics

1. **Uptime Improvement**
   - Target: 99.5% ecosystem uptime (measured over 30 days)
   - Baseline: ~95% (frequent manual restarts)

2. **Auto-Recovery**
   - Target: 90% of failures recovered automatically within 2 minutes
   - Measure: health events with `recovery_successful: true`

3. **Detection Speed**
   - Target: Failures detected within 30 seconds
   - Measure: Time between `server_down` and `recovery_started` events

4. **Developer Experience**
   - Target: Zero manual server restarts per week
   - Baseline: 5-10 manual restarts per week

5. **Ecosystem Adoption**
   - Target: All MCP servers expose health endpoint
   - Measure: Compliance with ecosystem-manifest quality standards

---

## Open Questions

1. **Health Check Frequency**: 30 seconds or configurable?
   - **Resolution Needed**: Sprint planning discussion
   - **Default**: 30s seems reasonable, make configurable via env var

2. **Auto-Recovery Strategy**: Restart only, or try repair first?
   - **Resolution Needed**: RFC discussion with examples
   - **Proposal**: Phase 1 = simple restart, Phase 2 = smart repair

3. **Health Event Schema**: What fields are required?
   - **Resolution Needed**: ADR with JSON schema
   - **Proposal**: status, uptime, last_check, error (optional)

4. **Notification Mechanism**: WebSocket, SSE, or polling?
   - **Resolution Needed**: mcp-gateway architecture discussion
   - **Proposal**: WebSocket for real-time, fallback to polling

---

## Dependencies

1. **chora-base v3.3.0** - Current template must support FastMCP extensions
2. **ecosystem-manifest v1.0.0** - Registry exists for server discovery
3. **mcp-orchestration basic lifecycle** - Containers can be restarted programmatically
4. **Docker/Podman API** - Health monitoring needs container introspection

---

## Resources Required

### Engineering Effort
- **chora-base**: 1 week (health endpoint template, docs)
- **ecosystem-manifest**: 1 week (health spec, quality standards update)
- **mcp-orchestration**: 2-3 weeks (monitoring service, auto-recovery)
- **mcp-gateway**: 1-2 weeks (aggregation, WebSocket, dashboard)

**Total**: ~6-8 weeks engineering time across 4 repos

### Infrastructure
- No new infrastructure required
- Uses existing Docker/Podman containers
- Uses existing FastMCP framework

---

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Auto-recovery causes restart loops | High | Add backoff strategy: 1s, 5s, 30s, manual |
| Health checks overload servers | Medium | 30s polling, timeout after 5s, exponential backoff on errors |
| False positives (healthy server marked down) | Medium | Require 3 consecutive failures before marking down |
| Implementation takes longer than 16 weeks | Low | Prioritize P0 features (basic health check), defer P1 (advanced recovery) |
| Standards change during implementation | Low | Lock RFC/ADR early, defer changes to v1.1 |

---

## Decision

**Date**: 2025-10-29 (2 days after creation)
**Decision Makers**: Victor Piper, Ecosystem Team
**Outcome**: **Accepted** → Moving to RFC process

**Rationale**:
- Critical blocker for production use (aligns with strategic goal)
- Clear business value (reliability, automation, observability)
- Reasonable scope (16 weeks, 4 repos, well-defined deliverables)
- Builds on existing infrastructure (no new external dependencies)
- Strong ecosystem support (all repos have capacity in Weeks 7-16)

**Next Steps**:
1. Create RFC 0001 with detailed technical design
2. FCP (Final Comment Period) for 1 week
3. Create ADR for health event schema
4. Generate coordination requests for all 4 repos

---

## Related

**RFCs**:
- [0001-health-monitoring-rfc.md](./0001-health-monitoring-rfc.md) (created after acceptance)

**ADRs**:
- [0001-health-check-format-adr.md](./0001-health-check-format-adr.md) (health event schema)

**Coordination Requests**:
- [coord-001-chora-base.json](../coordination/coord-001-chora-base.json)
- [coord-002-ecosystem-manifest.json](../coordination/coord-002-ecosystem-manifest.json)
- [coord-003-mcp-orchestration.json](../coordination/coord-003-mcp-orchestration.json)
- [coord-004-mcp-gateway.json](../coordination/coord-004-mcp-gateway.json)

**Events**: `inbox/examples/health-monitoring-w3/events/complete-timeline.jsonl`
