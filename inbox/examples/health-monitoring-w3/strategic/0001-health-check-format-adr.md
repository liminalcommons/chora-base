---
adr: "0001"
title: "Health Check JSON Schema and Response Format"
status: accepted
created: 2025-11-10
decision_date: 2025-11-10
decision_makers:
  - Victor Piper
  - Ecosystem Team
supersedes: null
superseded_by: null
related_rfc: "0001"
trace_id: ecosystem-w3-health-monitoring
---

# ADR 0001: Health Check JSON Schema and Response Format

## Status
**Accepted** (2025-11-10)

## Context

RFC 0001 defined the overall health monitoring architecture. This ADR makes a specific technical decision: the exact JSON schema for health check responses.

**Decision Point**: What fields are required vs optional? What status values are allowed? How to handle component-level checks?

**Why This Matters**:
- All 4 repos must use the same schema for interoperability
- Monitoring service needs to parse responses reliably
- Schema must be forward-compatible (add fields without breaking)

---

## Decision

We will use the following JSON schema for health check responses:

### Schema Definition
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "MCP Health Check Response",
  "type": "object",
  "required": ["status", "timestamp", "uptime_seconds"],
  "properties": {
    "status": {
      "type": "string",
      "enum": ["ok", "degraded", "down"],
      "description": "Overall health status"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp of this health check"
    },
    "uptime_seconds": {
      "type": "integer",
      "minimum": 0,
      "description": "Seconds since server started"
    },
    "version": {
      "type": "string",
      "description": "Server version (semantic versioning recommended)"
    },
    "checks": {
      "type": "object",
      "patternProperties": {
        "^[a-z_]+$": {
          "type": "string",
          "enum": ["ok", "degraded", "down"]
        }
      },
      "description": "Component-level health checks"
    },
    "error": {
      "type": "string",
      "description": "Error message if status != ok"
    },
    "metadata": {
      "type": "object",
      "description": "Additional server-specific metadata"
    }
  }
}
```

### Example Responses

#### Healthy Server
```json
{
  "status": "ok",
  "timestamp": "2025-10-27T10:30:00Z",
  "uptime_seconds": 86400,
  "version": "1.2.3",
  "checks": {
    "database": "ok",
    "cache": "ok",
    "filesystem": "ok"
  }
}
```

#### Degraded Server
```json
{
  "status": "degraded",
  "timestamp": "2025-10-27T10:35:00Z",
  "uptime_seconds": 86700,
  "version": "1.2.3",
  "checks": {
    "database": "ok",
    "cache": "degraded",
    "filesystem": "ok"
  },
  "error": "Redis connection pool at 90% capacity"
}
```

#### Failed Server
```json
{
  "status": "down",
  "timestamp": "2025-10-27T10:40:00Z",
  "uptime_seconds": 87000,
  "version": "1.2.3",
  "checks": {
    "database": "down",
    "cache": "ok",
    "filesystem": "ok"
  },
  "error": "PostgreSQL connection failed: FATAL password authentication failed"
}
```

---

## Consequences

### Positive
1. **Clear Contract**: All repos know exactly what to implement
2. **Forward Compatible**: Can add new optional fields without breaking
3. **Component Visibility**: `checks` object shows which component failed
4. **Machine Readable**: JSON schema enables validation tools
5. **Human Readable**: Status values are self-explanatory

### Negative
1. **Verbose**: JSON is more verbose than "ok\n"
   - Accepted: Clarity > brevity for health checks
2. **Schema Validation Overhead**: Monitoring service must validate responses
   - Accepted: Validation catches bugs early
3. **No Custom Status Values**: Only "ok", "degraded", "down" allowed
   - Accepted: Simple is better, extensions via `checks` and `metadata`

---

## Rationale

### Why JSON?
- Language-agnostic (works with Python, Node.js, Go, Rust)
- Well-supported libraries for parsing and validation
- Easy to extend with new fields

**Alternatives Considered**:
- Plain text "ok\n" → Too simple, can't show component health
- YAML → More complex to parse, no benefit over JSON
- Protocol Buffers → Overkill for simple health checks

### Why 3 Status Values?
- **ok**: Server healthy, processing requests normally
- **degraded**: Server running but some issues (warning, no restart)
- **down**: Server unable to process requests (trigger recovery)

**Alternatives Considered**:
- Binary (healthy/unhealthy) → Can't distinguish warning from failure
- Numeric (0-100) → Ambiguous what threshold triggers recovery
- Custom strings → No interoperability

### Why Required Fields?
- **status**: Without status, health check is meaningless
- **timestamp**: Enables staleness detection (old timestamp = broken check)
- **uptime_seconds**: Helps detect restart loops

**Why Optional Fields?**:
- **version**: Useful but not critical for health determination
- **checks**: Advanced feature, not all servers have components
- **error**: Only needed when status != "ok"
- **metadata**: Server-specific extensions

---

## Implementation Notes

### For MCP Server Developers (chora-base template)
```python
from datetime import datetime, timezone
import time

class HealthCheck:
    def __init__(self):
        self.start_time = time.time()

    def check(self) -> dict:
        """
        Health check endpoint handler
        """
        checks = {
            "database": self._check_database(),
            "cache": self._check_cache(),
        }

        # Aggregate component status
        if all(status == "ok" for status in checks.values()):
            overall_status = "ok"
        elif any(status == "down" for status in checks.values()):
            overall_status = "down"
        else:
            overall_status = "degraded"

        response = {
            "status": overall_status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": int(time.time() - self.start_time),
            "version": "1.0.0",
            "checks": checks
        }

        if overall_status != "ok":
            response["error"] = self._get_error_message(checks)

        return response
```

### For Monitoring Service (mcp-orchestration)
```python
import jsonschema
from datetime import datetime, timezone

# Load schema once at startup
HEALTH_SCHEMA = load_json_schema("health-check.schema.json")

async def check_server_health(server: Server) -> HealthStatus:
    """
    Check server health and validate response
    """
    try:
        response = await http_client.get(
            f"{server.url}/health",
            timeout=5.0
        )

        # Parse JSON
        data = response.json()

        # Validate against schema
        jsonschema.validate(data, HEALTH_SCHEMA)

        # Check for stale response
        timestamp = datetime.fromisoformat(data["timestamp"])
        age_seconds = (datetime.now(timezone.utc) - timestamp).total_seconds()
        if age_seconds > 60:
            return HealthStatus.STALE

        # Return status
        return HealthStatus(data["status"])

    except (httpx.TimeoutError, httpx.ConnectError):
        return HealthStatus.DOWN
    except jsonschema.ValidationError as e:
        logger.warning(f"Invalid health response from {server.name}: {e}")
        return HealthStatus.DOWN
    except Exception as e:
        logger.error(f"Health check failed for {server.name}: {e}")
        return HealthStatus.DOWN
```

---

## Validation

### Test Cases
1. **Valid "ok" response**: Passes validation
2. **Missing required field**: Fails validation
3. **Invalid status value**: Fails validation
4. **Extra fields**: Passes (forward compatibility)
5. **Component checks with mixed status**: Passes

### JSON Schema File Location
- **ecosystem-manifest**: `schemas/health-check-v1.0.json`
- **chora-base**: Copy to template docs
- **mcp-orchestration**: Load from ecosystem-manifest repo

---

## Future Evolution

### v1.1 (Potential Additions)
- `response_time_ms`: Response time of last request
- `request_count`: Total requests processed
- `error_count`: Total errors encountered

**Breaking Changes**: None. These are optional fields.

### v2.0 (Potential Breaking Changes)
- Add `startup_check` separate from `health_check`
- Add `ready_check` for traffic readiness (Kubernetes-style)
- Add `metrics` array with time-series data

**Migration Path**: Monitoring service checks version field, falls back to v1.0 schema if version < 2.0

---

## Related Decisions

**Supersedes**: None (first health check ADR)

**Superseded By**: None (current)

**Related**:
- RFC 0001: Health Monitoring & Auto-Recovery (parent RFC)
- Proposal prop-001: Strategic proposal that started this work

---

## Approval

**Date**: 2025-11-10
**Approved By**:
- Victor Piper (Lead Maintainer)
- Ecosystem Team

**Dissenting Opinions**: None

**Implementation Start**: Week 7 (2025-11-11)

---

## Changelog

- **2025-11-10**: ADR created and accepted
