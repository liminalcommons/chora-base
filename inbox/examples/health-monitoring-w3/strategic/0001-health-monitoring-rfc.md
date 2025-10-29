---
rfc: "0001"
title: "Health Monitoring & Auto-Recovery Technical Design"
status: accepted
created: 2025-10-30
fcp_start: 2025-11-03
fcp_end: 2025-11-10
authors:
  - Victor Piper
related_proposal: prop-001
trace_id: ecosystem-w3-health-monitoring
---

# RFC 0001: Health Monitoring & Auto-Recovery Technical Design

## Summary

Technical design for Waypoint W3: Health Monitoring & Auto-Recovery. Defines health endpoint contract, monitoring service architecture, auto-recovery strategy, and event schema.

**Based on**: [Strategic Proposal prop-001](./prop-001-health-monitoring.md) (Accepted 2025-10-29)

---

## Motivation

Strategic Proposal prop-001 established **why** we need health monitoring. This RFC defines **how** to implement it with specific technical decisions that enable coordination across 4 repositories.

---

## Guide-level Explanation

### For MCP Server Developers
Every MCP server will expose a `/health` endpoint:

```python
# In your FastMCP server
from fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("my-server")

@mcp.tool()
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "ok",  # ok | degraded | down
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": get_uptime(),
        "version": "1.0.0",
        "checks": {
            "database": "ok",
            "cache": "ok"
        }
    }
```

The health endpoint is called every 30 seconds by mcp-orchestration. If it fails 3 times in a row, auto-recovery attempts to restart your server.

### For Orchestration Developers
The health monitoring service polls registered servers:

```python
# Pseudocode for monitoring service
async def monitor_health():
    while True:
        for server in get_registered_servers():
            health = await check_health(server)
            if health.failed:
                await handle_failure(server)
        await asyncio.sleep(30)
```

### For Gateway Developers
The gateway aggregates health status:

```python
# Gateway exposes ecosystem health
@app.get("/health/ecosystem")
async def ecosystem_health():
    return {
        "status": "ok",
        "servers": [
            {"name": "server-a", "status": "ok"},
            {"name": "server-b", "status": "degraded"}
        ]
    }
```

---

## Reference-level Explanation

### 1. Health Endpoint Contract

#### Endpoint
- **Path**: `/health` (or `GET /` with `Accept: application/health+json`)
- **Method**: `GET`
- **Timeout**: 5 seconds
- **Authentication**: None (health checks are unauthenticated)

#### Response Schema
```json
{
  "status": "ok",
  "timestamp": "2025-10-27T10:30:00Z",
  "uptime_seconds": 86400,
  "version": "1.0.0",
  "checks": {
    "component_name": "ok"
  }
}
```

**Required Fields**:
- `status` (string): One of `"ok"`, `"degraded"`, `"down"`
- `timestamp` (string): ISO 8601 timestamp
- `uptime_seconds` (integer): Seconds since server started

**Optional Fields**:
- `version` (string): Server version
- `checks` (object): Per-component health status
- `error` (string): Error message if status != "ok"

**Status Definitions**:
- `ok`: All systems operational
- `degraded`: Server running but some components unhealthy
- `down`: Server unable to process requests

#### Error Handling
If health endpoint returns:
- **200 OK** with `status: "ok"` → Healthy
- **200 OK** with `status: "degraded"` → Degraded (warning, no restart)
- **200 OK** with `status: "down"` → Failed (trigger recovery)
- **500/503** → Failed (trigger recovery)
- **Timeout (>5s)** → Failed (trigger recovery)
- **Connection refused** → Failed (trigger recovery)

### 2. Health Monitoring Service (mcp-orchestration)

#### Architecture
```
┌───────────────────────────────────────┐
│  Health Monitoring Service            │
│                                       │
│  ┌─────────────────────────────────┐ │
│  │  Health Checker                 │ │
│  │  - Poll every 30s               │ │
│  │  - Timeout after 5s             │ │
│  │  - Track failure count          │ │
│  └─────────────────────────────────┘ │
│                                       │
│  ┌─────────────────────────────────┐ │
│  │  Recovery Manager               │ │
│  │  - Exponential backoff          │ │
│  │  - Container restart            │ │
│  │  - Event emission               │ │
│  └─────────────────────────────────┘ │
│                                       │
│  ┌─────────────────────────────────┐ │
│  │  State Manager                  │ │
│  │  - Server registry              │ │
│  │  - Failure counts               │ │
│  │  - Last check timestamps        │ │
│  └─────────────────────────────────┘ │
└───────────────────────────────────────┘
```

#### State Machine
```
     [Healthy]
         │
         │ 3 consecutive failures
         v
    [Degraded] ────────┐
         │             │
         │ recovery    │ 3 successes
         v             │
   [Recovering]────────┘
         │
         │ 5 failures
         v
      [Failed]
         │
         │ manual intervention
         v
     [Disabled]
```

#### Configuration
```yaml
# health-monitor-config.yaml
health_check:
  interval_seconds: 30
  timeout_seconds: 5
  failure_threshold: 3  # Mark degraded after 3 failures
  success_threshold: 3  # Mark healthy after 3 successes

recovery:
  enabled: true
  strategy: restart  # restart | recreate | manual
  backoff:
    initial_delay: 1    # seconds
    max_delay: 300      # seconds (5 minutes)
    multiplier: 2.0     # exponential backoff
  max_attempts: 5       # After 5 failures, require manual intervention

event_emission:
  enabled: true
  trace_context: true   # Include CHORA_TRACE_ID
  jsonl_log: /var/log/health-events.jsonl
```

### 3. Auto-Recovery Strategy

#### Recovery Algorithm
```python
async def recover_server(server: Server):
    """
    Attempt to recover a failed server
    """
    attempts = 0
    delay = INITIAL_DELAY

    while attempts < MAX_ATTEMPTS:
        emit_event({
            "event_type": "recovery_started",
            "server_name": server.name,
            "attempt": attempts + 1,
            "trace_id": server.trace_id
        })

        try:
            # Strategy 1: Restart container
            await docker.restart(server.container_id)
            await asyncio.sleep(delay)

            # Verify recovery
            if await check_health(server):
                emit_event({
                    "event_type": "recovery_successful",
                    "server_name": server.name,
                    "attempts": attempts + 1
                })
                return True
        except Exception as e:
            emit_event({
                "event_type": "recovery_failed",
                "server_name": server.name,
                "error": str(e)
            })

        attempts += 1
        delay = min(delay * MULTIPLIER, MAX_DELAY)

    # Exhausted attempts
    emit_event({
        "event_type": "recovery_exhausted",
        "server_name": server.name,
        "requires_manual": true
    })
    return False
```

#### Backoff Schedule
- Attempt 1: 1 second
- Attempt 2: 2 seconds
- Attempt 3: 4 seconds
- Attempt 4: 8 seconds
- Attempt 5: 16 seconds
- **Total**: ~31 seconds before manual intervention required

### 4. Health Status Aggregation (mcp-gateway)

#### Aggregation Logic
```python
def aggregate_health(servers: List[ServerHealth]) -> EcosystemHealth:
    """
    Aggregate health status across all servers
    """
    total = len(servers)
    healthy = sum(1 for s in servers if s.status == "ok")
    degraded = sum(1 for s in servers if s.status == "degraded")
    down = sum(1 for s in servers if s.status == "down")

    # Ecosystem status logic
    if down > 0:
        status = "degraded"  # Any server down = degraded
    elif degraded > total * 0.5:
        status = "degraded"  # >50% degraded = degraded
    else:
        status = "ok"

    return {
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "servers": {
            "total": total,
            "healthy": healthy,
            "degraded": degraded,
            "down": down
        },
        "details": [s.to_dict() for s in servers]
    }
```

#### WebSocket Notifications
```python
# Real-time health updates
@websocket("/health/stream")
async def health_stream(websocket: WebSocket):
    await websocket.accept()

    async for event in health_event_stream():
        await websocket.send_json({
            "event_type": event.type,
            "server": event.server_name,
            "status": event.status,
            "timestamp": event.timestamp
        })
```

Clients can subscribe:
```javascript
const ws = new WebSocket('ws://gateway/health/stream');
ws.onmessage = (event) => {
    const update = JSON.parse(event.data);
    console.log(`${update.server}: ${update.status}`);
};
```

### 5. Event Schema

#### Health Check Event
```json
{
  "event_type": "health_check_completed",
  "trace_id": "ecosystem-w3-health-monitoring",
  "timestamp": "2025-10-27T10:30:00Z",
  "repo": "mcp-orchestration",
  "server_name": "mcp-server-a",
  "status": "ok",
  "response_time_ms": 150,
  "checks": {
    "database": "ok",
    "cache": "ok"
  }
}
```

#### Recovery Event
```json
{
  "event_type": "recovery_started",
  "trace_id": "ecosystem-w3-health-monitoring",
  "timestamp": "2025-10-27T10:31:00Z",
  "repo": "mcp-orchestration",
  "server_name": "mcp-server-a",
  "reason": "3_consecutive_failures",
  "attempt": 1,
  "strategy": "restart"
}
```

---

## Drawbacks

1. **Polling Overhead**: Every 30s, monitoring service makes HTTP requests to all servers
   - Mitigation: 30s is reasonable, configurable if needed

2. **False Positives**: Network blips could trigger unnecessary restarts
   - Mitigation: Require 3 consecutive failures before recovery

3. **Restart Loops**: Broken server could restart infinitely
   - Mitigation: Exponential backoff + max 5 attempts

4. **No Predictive Monitoring**: Only detects failures after they happen
   - Accepted: Predictive monitoring is Phase 2 (v1.1)

---

## Rationale and Alternatives

### Why not Kubernetes liveness probes?
- We're container-agnostic (Docker, Podman, systemd)
- Want consistent behavior across all environments
- Need custom recovery logic with trace context

### Why not external monitoring (Prometheus)?
- Adds infrastructure dependency
- Doesn't integrate with our event system
- No auto-recovery built-in

### Why 30-second polling?
- Fast enough to detect issues quickly
- Slow enough to avoid overhead
- Industry standard (matches Kubernetes default)

---

## Prior Art

### Kubernetes Health Checks
- **Liveness probe**: Detects if container should be restarted
- **Readiness probe**: Detects if container ready for traffic
- **Startup probe**: Detects if app has started (slow startups)

**Our approach**: Single health endpoint, similar to liveness probe

### Spring Boot Actuator
- `/actuator/health` endpoint with hierarchical checks
- Aggregates component health (database, disk, etc.)

**Our approach**: Similar structure, simpler (no actuator framework)

### HashiCorp Consul
- Service registry with health checks
- TTL-based checks, HTTP checks, script checks

**Our approach**: HTTP-only, simpler (no service registry)

---

## Unresolved Questions

1. **Should health checks be authenticated?**
   - Proposal: No (simplicity, health is not sensitive)
   - Alternative: Optional bearer token via env var
   - **Resolution**: No auth in v1.0, add in v1.1 if needed

2. **Should we support TTL-based checks?**
   - Proposal: No (polling-only for v1.0)
   - Alternative: Server sends heartbeat, timeout = failure
   - **Resolution**: Polling-only, revisit in v1.1

3. **How to handle server startup time?**
   - Proposal: Grace period (don't check for 30s after start)
   - Alternative: Startup probe separate from health probe
   - **Resolution**: Grace period for v1.0

---

## Future Possibilities

### Phase 2 (v1.1) - Advanced Recovery
- Smart recovery (analyze logs before restart)
- Graceful degradation (route around failed servers)
- Circuit breaker pattern (stop checking failed servers)

### Phase 3 (v2.0) - Predictive Monitoring
- Metrics collection (CPU, memory, request latency)
- Anomaly detection (predict failures before they happen)
- Auto-scaling based on health metrics

---

## FCP (Final Comment Period)

**Start**: 2025-11-03
**End**: 2025-11-10 (1 week)

During FCP:
- Review technical design
- Raise concerns or alternatives
- Request clarifications

**After FCP**: If no blocking concerns, accept RFC and create ADRs.

---

## Decision

**Date**: 2025-11-10 (end of FCP)
**Decision Makers**: Victor Piper, Ecosystem Team
**Outcome**: **Accepted** → Moving to ADR creation

**Rationale**:
- Technical design is sound and implementable
- Addresses all concerns from strategic proposal
- Clear contracts for cross-repo coordination
- No blocking concerns raised during FCP

**Next Steps**:
1. Create ADR 0001 for health check format
2. Generate coordination requests
3. Begin implementation (Week 7)

---

## Related

**Proposal**: [prop-001-health-monitoring.md](./prop-001-health-monitoring.md)

**ADRs**:
- [0001-health-check-format-adr.md](./0001-health-check-format-adr.md)

**Implementation**:
- Task 001: Health endpoint template (chora-base)
- Task 002: Health check spec (ecosystem-manifest)
- Task 003: Monitoring service (mcp-orchestration)
- Task 004: Status aggregation (mcp-gateway)
