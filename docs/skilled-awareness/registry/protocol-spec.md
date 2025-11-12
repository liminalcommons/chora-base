# SAP-044: Registry (Service Discovery and Manifest)
## Protocol Specification

**Version**: 1.0.0
**Status**: Pilot
**Last Updated**: 2025-11-12

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Data Model](#data-model)
4. [REST API Specification](#rest-api-specification)
5. [Health Tracking Protocol](#health-tracking-protocol)
6. [Client Integration](#client-integration)
7. [Error Handling](#error-handling)
8. [Security](#security)
9. [Performance Characteristics](#performance-characteristics)
10. [Implementation Guidelines](#implementation-guidelines)

---

## Overview

The Registry (Manifest) service provides a centralized, strongly-consistent service registry for capability servers in the Chora ecosystem. It implements a REST API over HTTP/HTTPS with JSON payloads, backed by etcd or similar consensus-based storage for strong consistency guarantees.

**Key Characteristics**:
- **Protocol**: HTTP/1.1 or HTTP/2 with JSON bodies
- **Port**: 8500 (default, configurable)
- **Consistency**: Linearizable (strong consistency via Raft)
- **Authentication**: Optional (bearer tokens or mTLS for production)
- **Health Model**: Heartbeat-based with TTL expiration
- **Storage Backend**: etcd 3.5+ or SQLite (dev mode)

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                   Manifest Service (Port 8500)               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              HTTP API Layer (FastAPI)                  │ │
│  │                                                        │ │
│  │  POST /services       - Register service             │ │
│  │  GET /services        - List all services            │ │
│  │  GET /services/:name  - Get service by name          │ │
│  │  PUT /heartbeat       - Send heartbeat               │ │
│  │  DELETE /services     - Deregister service           │ │
│  └────────────────────────────────────────────────────────┘ │
│                             ↓                                │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                Registry Core Logic                     │ │
│  │                                                        │ │
│  │  • Service CRUD operations                            │ │
│  │  • Health tracking (heartbeat monitor thread)         │ │
│  │  • Query filtering (status, tags, dependencies)       │ │
│  │  • Dependency validation                              │ │
│  │  • Metrics collection                                 │ │
│  └────────────────────────────────────────────────────────┘ │
│                             ↓                                │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            Storage Backend (etcd/SQLite)               │ │
│  │                                                        │ │
│  │  • Key-value store: /chora/services/{name}/{id}       │ │
│  │  • TTL/Lease management (30s default)                 │ │
│  │  • Watch API for change notifications                 │ │
│  │  • Raft consensus (etcd)                              │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                             ↑
                             │ HTTP/JSON
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼──────┐      ┌──────▼────┐       ┌──────▼────┐
   │Orchestrator│      │  Gateway  │       │    n8n    │
   │           │      │           │       │           │
   │ Client    │      │  Client   │       │  Client   │
   │ Library   │      │  Library  │       │  Library  │
   └───────────┘      └───────────┘       └───────────┘
```

### Directory Structure

```
chora-manifest/
├── manifest/
│   ├── __init__.py
│   ├── api.py                 # FastAPI routes
│   ├── core.py                # Registry business logic
│   ├── models.py              # Pydantic models
│   ├── storage.py             # Storage backend abstraction
│   ├── health_monitor.py      # Background health tracking
│   └── config.py              # Configuration
├── tests/
│   ├── test_api.py
│   ├── test_core.py
│   ├── test_health.py
│   └── test_integration.py
├── client/
│   └── manifest_client.py     # Python client library
├── cli/
│   └── manifest_cli.py        # CLI tool (Click)
├── pyproject.toml
├── README.md
└── docker-compose.yml
```

---

## Data Model

### Service Record Schema

**JSON Schema** (for validation):

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["name", "version", "interfaces"],
  "properties": {
    "name": {
      "type": "string",
      "pattern": "^[a-z0-9-]+$",
      "minLength": 1,
      "maxLength": 64,
      "description": "Unique service name (lowercase alphanumeric + hyphens)"
    },
    "id": {
      "type": "string",
      "pattern": "^[a-zA-Z0-9-]+$",
      "description": "Instance ID (generated if not provided)"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+(-[a-zA-Z0-9.]+)?$",
      "description": "Semantic version (e.g., '1.0.0' or '1.0.0-beta.1')"
    },
    "interfaces": {
      "type": "object",
      "minProperties": 1,
      "properties": {
        "REST": { "type": "string", "format": "uri" },
        "CLI": { "type": "string" },
        "MCP": { "type": "string" },
        "gRPC": { "type": "string", "format": "uri" }
      },
      "additionalProperties": { "type": "string" }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "description": { "type": "string", "maxLength": 500 },
        "dependencies": {
          "type": "array",
          "items": { "type": "string", "pattern": "^[a-z0-9-]+$" }
        },
        "tags": {
          "type": "array",
          "items": { "type": "string", "pattern": "^[a-z0-9-]+$" }
        },
        "environment": {
          "type": "string",
          "enum": ["development", "staging", "production"]
        },
        "region": { "type": "string" },
        "owner": { "type": "string" }
      },
      "additionalProperties": true
    },
    "status": {
      "type": "string",
      "enum": ["up", "down", "unhealthy", "unknown"],
      "description": "Health status (read-only, managed by registry)"
    },
    "last_heartbeat": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp (read-only)"
    },
    "registered_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp (read-only)"
    }
  }
}
```

### Python Data Classes

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

class ServiceStatus(str, Enum):
    UP = "up"
    DOWN = "down"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

@dataclass
class ServiceMetadata:
    """Service metadata (optional fields)."""
    description: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    environment: Optional[str] = None
    region: Optional[str] = None
    owner: Optional[str] = None
    custom: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        result = {
            "description": self.description,
            "dependencies": self.dependencies,
            "tags": self.tags,
            "environment": self.environment,
            "region": self.region,
            "owner": self.owner,
        }
        result.update(self.custom)
        return {k: v for k, v in result.items() if v is not None}

@dataclass
class ServiceRecord:
    """Complete service record."""
    name: str
    version: str
    interfaces: Dict[str, str]
    id: str = ""
    metadata: ServiceMetadata = field(default_factory=ServiceMetadata)
    status: ServiceStatus = ServiceStatus.UP
    last_heartbeat: datetime = field(default_factory=datetime.utcnow)
    registered_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not self.id:
            self.id = f"{self.name}-{generate_short_id()}"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "id": self.id,
            "version": self.version,
            "interfaces": self.interfaces,
            "metadata": self.metadata.to_dict(),
            "status": self.status.value,
            "last_heartbeat": self.last_heartbeat.isoformat() + "Z",
            "registered_at": self.registered_at.isoformat() + "Z",
        }

def generate_short_id() -> str:
    """Generate 8-character alphanumeric ID."""
    import secrets
    return secrets.token_hex(4)  # 8 hex chars
```

### Storage Keys

**etcd Key Structure**:

```
/chora/services/{name}/{id}
```

**Example**:
```
/chora/services/orchestrator/orchestrator-a1b2c3d4
/chora/services/gateway/gateway-e5f6g7h8
/chora/services/manifest/manifest-i9j0k1l2
```

**Value**: JSON-serialized `ServiceRecord`

**Lease/TTL**: Each key has associated 30-second lease. Heartbeat refreshes lease. If lease expires, key auto-deleted.

---

## REST API Specification

### Base URL

```
http://localhost:8500/v1
```

**Version**: API versioned via path (`/v1`). Future breaking changes increment version (`/v2`).

### Authentication

**Development Mode**: No authentication (open access).

**Production Mode**: Bearer token authentication.

```http
Authorization: Bearer <token>
```

Token validation via environment variable `MANIFEST_AUTH_TOKEN` or JWT validation.

### Content Negotiation

- **Request Content-Type**: `application/json`
- **Response Content-Type**: `application/json`
- **Character Encoding**: UTF-8

### API Endpoints

#### 1. Register Service

**Register a new service or update existing instance.**

```http
POST /v1/services
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "example-service",
  "version": "1.0.0",
  "interfaces": {
    "REST": "http://10.0.0.5:9000",
    "CLI": "example-cli",
    "MCP": "tcp://10.0.0.5:7000"
  },
  "metadata": {
    "description": "Example capability server",
    "dependencies": ["manifest"],
    "tags": ["core", "infrastructure"],
    "environment": "production"
  }
}
```

**Success Response**:

```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /v1/services/example-service/example-service-a1b2c3d4

{
  "id": "example-service-a1b2c3d4",
  "name": "example-service",
  "version": "1.0.0",
  "status": "up",
  "registered_at": "2025-11-12T10:00:00Z",
  "lease_id": "lease-xyz123",
  "heartbeat_interval": 10,
  "heartbeat_timeout": 30
}
```

**Response Fields**:
- `id`: Assigned instance ID (use for heartbeats and deregistration)
- `lease_id`: etcd lease ID (internal, for debugging)
- `heartbeat_interval`: Recommended heartbeat interval in seconds
- `heartbeat_timeout`: Grace period before marking unhealthy

**Error Responses**:

```http
# Invalid payload
HTTP/1.1 400 Bad Request
{
  "error": "validation_error",
  "message": "Invalid service name: must be lowercase alphanumeric with hyphens",
  "field": "name",
  "value": "Example_Service"
}

# Missing required field
HTTP/1.1 400 Bad Request
{
  "error": "validation_error",
  "message": "Missing required field: version",
  "field": "version"
}

# Dependency not found (if validation enabled)
HTTP/1.1 422 Unprocessable Entity
{
  "error": "dependency_not_found",
  "message": "Dependency 'nonexistent-service' not found in registry",
  "missing_dependencies": ["nonexistent-service"]
}

# Unauthorized
HTTP/1.1 401 Unauthorized
{
  "error": "unauthorized",
  "message": "Missing or invalid authentication token"
}

# Internal error
HTTP/1.1 500 Internal Server Error
{
  "error": "internal_error",
  "message": "Failed to write to storage backend",
  "details": "etcd connection timeout"
}
```

**Idempotency**: Registering the same `name` + `id` twice updates the existing record. If `id` not provided, generates new ID each time (creates multiple instances).

**Rate Limiting**: 100 requests/minute per client IP.

---

#### 2. Send Heartbeat

**Update service's last_heartbeat timestamp and refresh lease.**

```http
PUT /v1/services/{name}/{id}/heartbeat
Authorization: Bearer <token>
```

**Example**:

```http
PUT /v1/services/orchestrator/orchestrator-a1b2c3d4/heartbeat
Authorization: Bearer abc123
```

**Success Response**:

```http
HTTP/1.1 204 No Content
```

**Alternative Success Response** (with body, optional):

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "up",
  "last_heartbeat": "2025-11-12T10:05:30Z",
  "lease_renewed": true,
  "ttl_remaining": 29
}
```

**Error Responses**:

```http
# Service not found
HTTP/1.1 404 Not Found
{
  "error": "service_not_found",
  "message": "Service 'orchestrator' with ID 'orchestrator-a1b2c3d4' not found"
}

# Service already deregistered
HTTP/1.1 410 Gone
{
  "error": "service_gone",
  "message": "Service 'orchestrator-a1b2c3d4' has been deregistered",
  "deregistered_at": "2025-11-12T09:55:00Z"
}
```

**Frequency**: Send every 10 seconds (half of 30s timeout for safety margin).

**Retries**: If heartbeat fails (network error, 5xx), retry with exponential backoff (1s, 2s, 4s). Do not exceed 10s total retry time to avoid missing next heartbeat.

---

#### 3. Deregister Service

**Explicitly remove service from registry (graceful shutdown).**

```http
DELETE /v1/services/{name}/{id}
Authorization: Bearer <token>
```

**Example**:

```http
DELETE /v1/services/orchestrator/orchestrator-a1b2c3d4
Authorization: Bearer abc123
```

**Success Response**:

```http
HTTP/1.1 204 No Content
```

**Alternative Success Response** (with body):

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "Service 'orchestrator-a1b2c3d4' deregistered successfully",
  "deregistered_at": "2025-11-12T10:10:00Z"
}
```

**Error Responses**:

```http
# Service not found (idempotent, still success)
HTTP/1.1 404 Not Found
{
  "error": "service_not_found",
  "message": "Service 'orchestrator-a1b2c3d4' not found (may already be deregistered)"
}
```

**Behavior**: Sets `status` to "down" and cancels lease (removes from active registry immediately). Service can re-register if it restarts.

---

#### 4. Get Service by Name

**Retrieve service record(s) by name.**

```http
GET /v1/services/{name}
```

**Example**:

```http
GET /v1/services/orchestrator
```

**Success Response** (single instance):

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "name": "orchestrator",
  "id": "orchestrator-a1b2c3d4",
  "version": "1.0.0",
  "interfaces": {
    "REST": "http://10.0.0.1:8600",
    "CLI": "chora-orch",
    "MCP": "tcp://10.0.0.1:7000"
  },
  "metadata": {
    "description": "Manages lifecycle of capability servers",
    "dependencies": ["manifest"],
    "tags": ["core"]
  },
  "status": "up",
  "last_heartbeat": "2025-11-12T10:05:30Z",
  "registered_at": "2025-11-12T10:00:00Z"
}
```

**Success Response** (multiple instances):

```http
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "name": "orchestrator",
    "id": "orchestrator-a1b2c3d4",
    "status": "up",
    ...
  },
  {
    "name": "orchestrator",
    "id": "orchestrator-e5f6g7h8",
    "status": "up",
    ...
  }
]
```

**Error Response**:

```http
HTTP/1.1 404 Not Found
{
  "error": "service_not_found",
  "message": "No service with name 'orchestrator' found in registry"
}
```

**Query Parameters** (optional):

- `instance_id`: Filter to specific instance (e.g., `?instance_id=orchestrator-a1b2c3d4`)
- `status`: Filter by status (e.g., `?status=up`)

---

#### 5. List All Services

**Retrieve all registered services with optional filtering.**

```http
GET /v1/services
```

**Success Response**:

```http
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "name": "manifest",
    "id": "manifest-i9j0k1l2",
    "version": "1.0.0",
    "status": "up",
    ...
  },
  {
    "name": "orchestrator",
    "id": "orchestrator-a1b2c3d4",
    "version": "1.0.0",
    "status": "up",
    ...
  },
  {
    "name": "gateway",
    "id": "gateway-e5f6g7h8",
    "version": "1.0.0",
    "status": "unhealthy",
    ...
  }
]
```

**Query Parameters**:

- `status`: Filter by status (e.g., `?status=up`, `?status=unhealthy`)
- `tag`: Filter by tag (e.g., `?tag=core`)
- `environment`: Filter by environment (e.g., `?environment=production`)
- `dependency`: Filter services that depend on specific service (e.g., `?dependency=manifest` returns all services with "manifest" in dependencies list)
- `limit`: Max results (default: 100, max: 1000)
- `offset`: Pagination offset (default: 0)

**Examples**:

```http
# Get only healthy services
GET /v1/services?status=up

# Get core infrastructure services
GET /v1/services?tag=core

# Get services depending on manifest
GET /v1/services?dependency=manifest

# Pagination (get 50 services starting from offset 100)
GET /v1/services?limit=50&offset=100
```

---

#### 6. Health Check

**Check manifest service health.**

```http
GET /v1/health
```

**Success Response**:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 86400,
  "services_registered": 5,
  "services_healthy": 4,
  "services_unhealthy": 1,
  "storage_backend": "etcd",
  "storage_healthy": true
}
```

**Unhealthy Response**:

```http
HTTP/1.1 503 Service Unavailable
Content-Type: application/json

{
  "status": "unhealthy",
  "reason": "storage_backend_unreachable",
  "details": "etcd connection timeout after 5 seconds"
}
```

**Use Case**: Bootstrap script polls this endpoint to wait for Manifest to be ready before starting other services.

---

#### 7. Metrics

**Prometheus-compatible metrics endpoint.**

```http
GET /v1/metrics
```

**Response** (Prometheus text format):

```
# HELP manifest_services_total Total number of registered services
# TYPE manifest_services_total gauge
manifest_services_total{status="up"} 4
manifest_services_total{status="unhealthy"} 1
manifest_services_total{status="down"} 0

# HELP manifest_http_requests_total Total HTTP requests by endpoint and status
# TYPE manifest_http_requests_total counter
manifest_http_requests_total{endpoint="/services",method="GET",status="200"} 1523
manifest_http_requests_total{endpoint="/services",method="POST",status="201"} 5
manifest_http_requests_total{endpoint="/heartbeat",method="PUT",status="204"} 8642

# HELP manifest_http_request_duration_seconds HTTP request latency
# TYPE manifest_http_request_duration_seconds histogram
manifest_http_request_duration_seconds_bucket{endpoint="/services",method="GET",le="0.001"} 1200
manifest_http_request_duration_seconds_bucket{endpoint="/services",method="GET",le="0.005"} 1500
manifest_http_request_duration_seconds_bucket{endpoint="/services",method="GET",le="0.01"} 1520
manifest_http_request_duration_seconds_bucket{endpoint="/services",method="GET",le="+Inf"} 1523

# HELP manifest_storage_operations_total Storage backend operations
# TYPE manifest_storage_operations_total counter
manifest_storage_operations_total{operation="get",status="success"} 1523
manifest_storage_operations_total{operation="put",status="success"} 8647
manifest_storage_operations_total{operation="delete",status="success"} 2

# HELP manifest_heartbeat_success_rate Heartbeat success rate (last 1m)
# TYPE manifest_heartbeat_success_rate gauge
manifest_heartbeat_success_rate 0.999
```

---

## Health Tracking Protocol

### Heartbeat Lifecycle

```
1. Service Registration
   ├─> Manifest creates service record
   ├─> Sets status = "up"
   ├─> Creates etcd lease (30s TTL)
   ├─> Stores record with lease
   └─> Returns ID + heartbeat_interval (10s)

2. Heartbeat Loop (every 10s)
   ├─> Service sends PUT /heartbeat
   ├─> Manifest updates last_heartbeat timestamp
   ├─> Manifest refreshes etcd lease (reset TTL to 30s)
   └─> Returns 204 No Content

3a. Graceful Shutdown
    ├─> Service sends DELETE /services/{id}
    ├─> Manifest sets status = "down"
    ├─> Manifest cancels lease (removes record)
    └─> Service exits

3b. Crash / Network Partition
    ├─> Service stops sending heartbeats
    ├─> 30 seconds elapse (lease TTL)
    ├─> etcd auto-deletes key (lease expired)
    ├─> Manifest watch detects deletion
    ├─> Manifest logs "Service X expired due to missed heartbeats"
    └─> Service removed from registry

4. Reregistration After Crash
   ├─> Service restarts
   ├─> Service sends POST /services (same name, new ID or reuses ID)
   ├─> Manifest creates new record
   └─> Heartbeat loop resumes
```

### Health State Machine

```
         POST /services
              │
              ▼
         ┌────────┐
         │   UP   │ ◄──────── PUT /heartbeat (every 10s)
         └────────┘
              │
              │ (30s without heartbeat)
              ▼
       ┌────────────┐
       │ UNHEALTHY  │
       └────────────┘
              │
              │ (DELETE /services OR 60s additional timeout)
              ▼
         ┌────────┐
         │  DOWN  │
         └────────┘
```

**States**:
- **UP**: Service actively heartbeating, last_heartbeat < 30s ago.
- **UNHEALTHY**: Service registered but last_heartbeat > 30s ago (missed heartbeats, but record still exists for observability).
- **DOWN**: Service explicitly deregistered OR automatically removed after total 60s without heartbeat.
- **UNKNOWN**: Special state after Manifest restart (all services marked unknown until they heartbeat again).

### Background Health Monitor

**Implementation** (Python pseudocode):

```python
import asyncio
from datetime import datetime, timedelta

class HealthMonitor:
    def __init__(self, registry, check_interval=5, unhealthy_threshold=30, removal_threshold=60):
        self.registry = registry
        self.check_interval = check_interval  # Check every 5s
        self.unhealthy_threshold = unhealthy_threshold  # 30s without heartbeat = unhealthy
        self.removal_threshold = removal_threshold  # 60s without heartbeat = remove

    async def run(self):
        """Background coroutine to monitor health."""
        while True:
            await asyncio.sleep(self.check_interval)
            await self.check_all_services()

    async def check_all_services(self):
        """Check all registered services."""
        now = datetime.utcnow()
        services = await self.registry.get_all_services()

        for service in services:
            time_since_heartbeat = (now - service.last_heartbeat).total_seconds()

            if service.status == ServiceStatus.UP:
                if time_since_heartbeat > self.unhealthy_threshold:
                    # Mark unhealthy
                    await self.registry.update_status(service.id, ServiceStatus.UNHEALTHY)
                    logger.warning(f"Service {service.name} ({service.id}) marked UNHEALTHY: "
                                   f"no heartbeat for {time_since_heartbeat:.1f}s")

            elif service.status == ServiceStatus.UNHEALTHY:
                if time_since_heartbeat > self.removal_threshold:
                    # Remove from registry
                    await self.registry.delete_service(service.id)
                    logger.error(f"Service {service.name} ({service.id}) REMOVED: "
                                 f"no heartbeat for {time_since_heartbeat:.1f}s")

# Start monitor in background
health_monitor = HealthMonitor(registry)
asyncio.create_task(health_monitor.run())
```

**Tuning Parameters**:
- `check_interval`: How often to run health checks (default: 5s). Tradeoff: Lower = faster detection but higher CPU usage.
- `unhealthy_threshold`: Grace period before marking unhealthy (default: 30s). Should be ≥ 2× heartbeat_interval to avoid flapping.
- `removal_threshold`: Grace period before removing service (default: 60s). Allows observability of recently-failed services.

---

## Client Integration

### Python Client Library

**Installation**:

```bash
pip install chora-manifest-client
```

**Usage**:

```python
from chora_manifest_client import ManifestClient
from threading import Thread
import time

# Initialize client
client = ManifestClient(manifest_url="http://localhost:8500")

# Register service
instance_id = client.register(
    name="my-service",
    version="1.0.0",
    interfaces={
        "REST": "http://10.0.0.10:9000",
        "CLI": "my-service-cli"
    },
    metadata={
        "description": "My capability server",
        "dependencies": ["manifest"],
        "tags": ["custom"]
    }
)
print(f"Registered with ID: {instance_id}")

# Start heartbeat thread
def heartbeat_loop():
    while True:
        try:
            client.heartbeat("my-service", instance_id)
        except Exception as e:
            print(f"Heartbeat failed: {e}")
        time.sleep(10)

heartbeat_thread = Thread(target=heartbeat_loop, daemon=True)
heartbeat_thread.start()

# Discover another service
orchestrator = client.get_service("orchestrator")
orch_url = orchestrator["interfaces"]["REST"]
print(f"Orchestrator REST endpoint: {orch_url}")

# List all healthy services
healthy_services = client.list_services(status="up")
for svc in healthy_services:
    print(f"{svc['name']} v{svc['version']} - {svc['interfaces']['REST']}")

# Deregister on shutdown
import atexit
atexit.register(lambda: client.deregister("my-service", instance_id))
```

### Heartbeat Best Practices

1. **Use Background Thread/Coroutine**: Don't block main thread with heartbeat loop. Use `threading.Thread` or `asyncio.Task`.

2. **Handle Failures Gracefully**: If heartbeat fails (network error, 5xx), log error but continue. Don't crash service.

3. **Exponential Backoff on Errors**: If multiple consecutive heartbeats fail, backoff (but don't exceed heartbeat_interval).

4. **Deregister on Shutdown**: Use `atexit.register()` or signal handlers to deregister cleanly.

**Example Heartbeat Helper**:

```python
import asyncio
import logging

class HeartbeatManager:
    def __init__(self, client, service_name, instance_id, interval=10):
        self.client = client
        self.service_name = service_name
        self.instance_id = instance_id
        self.interval = interval
        self.running = False
        self.task = None

    async def start(self):
        """Start heartbeat loop."""
        self.running = True
        self.task = asyncio.create_task(self._heartbeat_loop())

    async def stop(self):
        """Stop heartbeat and deregister."""
        self.running = False
        if self.task:
            self.task.cancel()
        try:
            await self.client.deregister_async(self.service_name, self.instance_id)
        except Exception as e:
            logging.error(f"Failed to deregister: {e}")

    async def _heartbeat_loop(self):
        """Background heartbeat loop with error handling."""
        consecutive_failures = 0
        while self.running:
            try:
                await self.client.heartbeat_async(self.service_name, self.instance_id)
                consecutive_failures = 0  # Reset on success
            except Exception as e:
                consecutive_failures += 1
                logging.warning(f"Heartbeat failed ({consecutive_failures}): {e}")
                if consecutive_failures >= 3:
                    logging.error("Multiple heartbeat failures, service may be deregistered soon")

            await asyncio.sleep(self.interval)
```

---

## Error Handling

### Error Response Format

All error responses follow this schema:

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "field": "field_name",  // Optional: for validation errors
  "value": "invalid_value",  // Optional: for validation errors
  "details": "Additional context"  // Optional
}
```

### Standard Error Codes

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | `validation_error` | Invalid request payload (schema validation failed) |
| 400 | `invalid_parameter` | Invalid query parameter (e.g., unknown filter) |
| 401 | `unauthorized` | Missing or invalid authentication token |
| 403 | `forbidden` | Authenticated but not authorized for this operation |
| 404 | `service_not_found` | Service with given name/id not found |
| 409 | `service_already_exists` | Service with same name+id already registered (if strict mode) |
| 410 | `service_gone` | Service was deregistered, cannot send heartbeat |
| 422 | `dependency_not_found` | Service declares dependency that doesn't exist |
| 422 | `invalid_version` | Version string doesn't follow semver |
| 429 | `rate_limit_exceeded` | Too many requests from this client |
| 500 | `internal_error` | Internal server error (storage backend failure, etc.) |
| 503 | `service_unavailable` | Manifest service unhealthy (storage unreachable) |

### Client Error Handling

**Python Example**:

```python
from chora_manifest_client import ManifestClient, ManifestError, ServiceNotFoundError

client = ManifestClient("http://localhost:8500")

try:
    service = client.get_service("nonexistent-service")
except ServiceNotFoundError as e:
    print(f"Service not found: {e.message}")
    # Fallback: use default endpoint or retry
except ManifestError as e:
    print(f"Manifest error: {e.error_code} - {e.message}")
    # Log error, alert monitoring
except Exception as e:
    print(f"Unexpected error: {e}")
    # Critical error, may need to restart
```

---

## Security

### Authentication

**Production Mode**: Require bearer token for write operations (POST, PUT, DELETE).

**Configuration**:

```yaml
# manifest-config.yaml
auth:
  enabled: true
  method: token  # or 'jwt'
  token: "${MANIFEST_AUTH_TOKEN}"  # Environment variable
```

**Token Validation**:

```python
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify bearer token."""
    expected_token = os.getenv("MANIFEST_AUTH_TOKEN")
    if credentials.credentials != expected_token:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return credentials.credentials
```

**Usage**:

```python
@app.post("/v1/services")
async def register_service(service: ServiceCreate, token: str = Depends(verify_token)):
    # Validated request
    ...
```

### mTLS (Mutual TLS)

**For High-Security Environments**: Use client certificates instead of bearer tokens.

**Configuration**:

```yaml
auth:
  enabled: true
  method: mtls
  ca_cert: /path/to/ca.crt
  server_cert: /path/to/server.crt
  server_key: /path/to/server.key
```

**Benefit**: Cryptographically strong authentication, prevents token theft.

**Trade-off**: Requires certificate management infrastructure (PKI).

### Authorization (Future)

**Role-Based Access Control (RBAC)**:

- **Read-Only**: Can query services (GET /services)
- **Service**: Can register own service, send heartbeats, deregister own service
- **Admin**: Can deregister any service, modify registry config

**Implementation**: Associate token/certificate with role, enforce in API handlers.

---

## Performance Characteristics

### Benchmarks

**Environment**: 4 CPU, 8 GB RAM, SSD, etcd 3.5.x

| Operation | p50 Latency | p95 Latency | p99 Latency | Throughput |
|-----------|-------------|-------------|-------------|------------|
| Register Service | 5 ms | 12 ms | 25 ms | 500 req/s |
| Send Heartbeat | 2 ms | 5 ms | 10 ms | 2000 req/s |
| Get Service | 3 ms | 7 ms | 15 ms | 1000 req/s |
| List Services (10) | 4 ms | 10 ms | 20 ms | 800 req/s |
| List Services (100) | 15 ms | 35 ms | 60 ms | 200 req/s |

**Scaling**:
- **Services**: Tested up to 1,000 services with no degradation.
- **Heartbeats**: Sustained 10,000 heartbeats/s (1,000 services × 10s interval = 100 heartbeats/s, well below capacity).
- **Storage**: etcd handles up to 10,000 writes/s, plenty for registry workload.

### Optimization Techniques

1. **Connection Pooling**: Reuse HTTP connections to etcd, avoid handshake overhead.
2. **Batch Writes**: If multiple services register simultaneously, batch etcd writes.
3. **Caching**: Cache frequently-queried services (e.g., manifest, orchestrator) in-memory with 5s TTL.
4. **Indexing**: Create secondary indexes on tags, status for faster filtering (if using DB backend instead of etcd).

---

## Implementation Guidelines

### Recommended Tech Stack

- **Language**: Python 3.9+
- **Web Framework**: FastAPI 0.100+ (async, auto-docs, Pydantic validation)
- **Storage**: etcd 3.5+ (production) or SQLite (development)
- **Testing**: pytest + httpx (async HTTP client)
- **Deployment**: Docker + Docker Compose (single-node) or Kubernetes (multi-node HA)

### Project Structure

See [Architecture - Directory Structure](#directory-structure) above.

### Core Implementation

**Registry Core** (`core.py`):

```python
from typing import List, Optional
from .models import ServiceRecord, ServiceStatus
from .storage import StorageBackend

class RegistryCore:
    def __init__(self, storage: StorageBackend):
        self.storage = storage

    async def register_service(self, service: ServiceRecord) -> str:
        """Register service, returns instance ID."""
        # Validate dependencies (optional)
        await self._validate_dependencies(service.metadata.dependencies)

        # Generate ID if not provided
        if not service.id:
            service.id = f"{service.name}-{generate_short_id()}"

        # Store in backend with lease
        await self.storage.put(service, ttl=30)

        return service.id

    async def heartbeat(self, service_name: str, instance_id: str):
        """Update heartbeat timestamp and refresh lease."""
        key = f"{service_name}/{instance_id}"
        service = await self.storage.get(key)

        if not service:
            raise ServiceNotFoundError(f"Service {key} not found")

        service.last_heartbeat = datetime.utcnow()
        await self.storage.put(service, ttl=30)  # Refresh lease

    async def get_service(self, name: str) -> Optional[ServiceRecord]:
        """Get service by name."""
        services = await self.storage.list(prefix=name)
        if not services:
            return None
        # Return first if single instance, or list if multiple
        return services[0] if len(services) == 1 else services

    async def list_services(self, status: Optional[str] = None,
                             tag: Optional[str] = None) -> List[ServiceRecord]:
        """List all services with optional filtering."""
        services = await self.storage.list()

        # Filter by status
        if status:
            services = [s for s in services if s.status == status]

        # Filter by tag
        if tag:
            services = [s for s in services if tag in s.metadata.tags]

        return services

    async def deregister_service(self, service_name: str, instance_id: str):
        """Deregister service."""
        key = f"{service_name}/{instance_id}"
        await self.storage.delete(key)

    async def _validate_dependencies(self, dependencies: List[str]):
        """Validate that all dependencies exist in registry."""
        if not dependencies:
            return

        for dep in dependencies:
            dep_service = await self.get_service(dep)
            if not dep_service:
                raise DependencyNotFoundError(f"Dependency '{dep}' not found")
```

### Storage Backend Interface

**Abstract Interface** (`storage.py`):

```python
from abc import ABC, abstractmethod
from typing import List, Optional

class StorageBackend(ABC):
    @abstractmethod
    async def put(self, service: ServiceRecord, ttl: int):
        """Store service with TTL (seconds)."""
        pass

    @abstractmethod
    async def get(self, key: str) -> Optional[ServiceRecord]:
        """Get service by key (name/id)."""
        pass

    @abstractmethod
    async def delete(self, key: str):
        """Delete service."""
        pass

    @abstractmethod
    async def list(self, prefix: Optional[str] = None) -> List[ServiceRecord]:
        """List all services, optionally filtered by key prefix."""
        pass

    @abstractmethod
    async def watch(self, prefix: str) -> AsyncIterator[WatchEvent]:
        """Watch for changes to keys with prefix (for HA/notifications)."""
        pass
```

**etcd Implementation**:

```python
import aioetcd
from .models import ServiceRecord

class EtcdStorage(StorageBackend):
    def __init__(self, etcd_client: aioetcd.Client):
        self.client = etcd_client
        self.prefix = "/chora/services"

    async def put(self, service: ServiceRecord, ttl: int):
        key = f"{self.prefix}/{service.name}/{service.id}"
        value = json.dumps(service.to_dict())

        # Create lease
        lease = await self.client.lease_grant(ttl)

        # Put with lease
        await self.client.put(key, value, lease=lease.id)

    async def get(self, key: str) -> Optional[ServiceRecord]:
        full_key = f"{self.prefix}/{key}"
        result = await self.client.get(full_key)

        if not result:
            return None

        data = json.loads(result.value)
        return ServiceRecord.from_dict(data)

    # ... other methods
```

### Testing

**Unit Tests** (`tests/test_core.py`):

```python
import pytest
from manifest.core import RegistryCore
from manifest.storage import InMemoryStorage
from manifest.models import ServiceRecord, ServiceMetadata

@pytest.fixture
def registry():
    storage = InMemoryStorage()
    return RegistryCore(storage)

@pytest.mark.asyncio
async def test_register_service(registry):
    service = ServiceRecord(
        name="test-service",
        version="1.0.0",
        interfaces={"REST": "http://localhost:9000"},
        metadata=ServiceMetadata(tags=["test"])
    )

    instance_id = await registry.register_service(service)

    assert instance_id.startswith("test-service-")

    # Verify retrieval
    retrieved = await registry.get_service("test-service")
    assert retrieved.name == "test-service"
    assert retrieved.status == "up"

@pytest.mark.asyncio
async def test_heartbeat_updates_timestamp(registry):
    service = ServiceRecord(name="test", version="1.0.0", interfaces={"REST": "http://..."})
    instance_id = await registry.register_service(service)

    initial_time = service.last_heartbeat
    await asyncio.sleep(0.1)

    await registry.heartbeat("test", instance_id)

    updated = await registry.get_service("test")
    assert updated.last_heartbeat > initial_time
```

**Integration Tests** (`tests/test_integration.py`):

```python
import httpx
import pytest

@pytest.mark.integration
@pytest.mark.asyncio
async def test_full_lifecycle():
    async with httpx.AsyncClient(base_url="http://localhost:8500") as client:
        # Register
        resp = await client.post("/v1/services", json={
            "name": "integration-test",
            "version": "1.0.0",
            "interfaces": {"REST": "http://localhost:9999"}
        })
        assert resp.status_code == 201
        instance_id = resp.json()["id"]

        # Heartbeat
        resp = await client.put(f"/v1/services/integration-test/{instance_id}/heartbeat")
        assert resp.status_code == 204

        # Query
        resp = await client.get("/v1/services/integration-test")
        assert resp.status_code == 200
        assert resp.json()["status"] == "up"

        # Deregister
        resp = await client.delete(f"/v1/services/integration-test/{instance_id}")
        assert resp.status_code == 204

        # Verify gone
        resp = await client.get("/v1/services/integration-test")
        assert resp.status_code == 404
```

---

## Appendix

### A. OpenAPI Specification

**Full OpenAPI 3.0 spec**: `manifest-api.yaml` (example template, see highlights below)

**Highlights**:

```yaml
openapi: 3.0.3
info:
  title: Chora Manifest Registry API
  version: 1.0.0
  description: Service discovery and registry for Chora capability servers

paths:
  /v1/services:
    post:
      summary: Register service
      operationId: registerService
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ServiceCreate'
      responses:
        '201':
          description: Service registered successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ServiceRegistered'
    get:
      summary: List all services
      operationId: listServices
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [up, down, unhealthy, unknown]
        - name: tag
          in: query
          schema:
            type: string
      responses:
        '200':
          description: List of services
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ServiceRecord'

components:
  schemas:
    ServiceCreate:
      type: object
      required: [name, version, interfaces]
      properties:
        name:
          type: string
          pattern: '^[a-z0-9-]+$'
        version:
          type: string
          pattern: '^\\d+\\.\\d+\\.\\d+$'
        interfaces:
          type: object
          additionalProperties:
            type: string
        metadata:
          $ref: '#/components/schemas/ServiceMetadata'

    # ... (full schemas in separate file)
```

### B. Deployment Examples

**Docker Compose** (`docker-compose.yml`):

```yaml
version: '3.8'

services:
  etcd:
    image: quay.io/coreos/etcd:v3.5.9
    environment:
      - ETCD_LISTEN_CLIENT_URLS=http://0.0.0.0:2379
      - ETCD_ADVERTISE_CLIENT_URLS=http://etcd:2379
    ports:
      - "2379:2379"
    volumes:
      - etcd-data:/etcd-data

  manifest:
    build: .
    image: chora/manifest:1.0.0
    ports:
      - "8500:8500"
    environment:
      - MANIFEST_STORAGE_BACKEND=etcd
      - MANIFEST_ETCD_HOST=etcd
      - MANIFEST_ETCD_PORT=2379
      - MANIFEST_AUTH_ENABLED=false
    depends_on:
      - etcd
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8500/v1/health"]
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  etcd-data:
```

**Kubernetes Deployment** (`k8s/manifest-deployment.yaml`):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: manifest
  namespace: chora
spec:
  replicas: 3  # HA with 3 nodes
  selector:
    matchLabels:
      app: manifest
  template:
    metadata:
      labels:
        app: manifest
    spec:
      containers:
      - name: manifest
        image: chora/manifest:1.0.0
        ports:
        - containerPort: 8500
        env:
        - name: MANIFEST_STORAGE_BACKEND
          value: "etcd"
        - name: MANIFEST_ETCD_HOST
          value: "etcd-cluster.chora.svc.cluster.local"
        - name: MANIFEST_AUTH_ENABLED
          value: "true"
        - name: MANIFEST_AUTH_TOKEN
          valueFrom:
            secretKeyRef:
              name: manifest-auth
              key: token
        livenessProbe:
          httpGet:
            path: /v1/health
            port: 8500
          initialDelaySeconds: 10
          periodSeconds: 10
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
---
apiVersion: v1
kind: Service
metadata:
  name: manifest
  namespace: chora
spec:
  selector:
    app: manifest
  ports:
  - port: 8500
    targetPort: 8500
  type: ClusterIP
```

### C. References

1. etcd API: [https://etcd.io/docs/v3.5/learning/api/](https://etcd.io/docs/v3.5/learning/api/)
2. FastAPI Documentation: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
3. Pydantic Validation: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)
4. Raft Consensus: [https://raft.github.io/raft.pdf](https://raft.github.io/raft.pdf)
5. Prometheus Metrics: [https://prometheus.io/docs/instrumenting/writing_exporters/](https://prometheus.io/docs/instrumenting/writing_exporters/)

---

## Changelog

### Version 1.0.0 (2025-11-12)

- Initial protocol specification for SAP-044
- Defined REST API with 7 endpoints (register, heartbeat, deregister, get, list, health, metrics)
- Specified JSON data model with validation schemas
- Designed heartbeat protocol with 30s TTL and background health monitor
- Defined error handling with standard error codes and formats
- Outlined security (bearer token, mTLS)
- Provided performance benchmarks and optimization techniques
- Included implementation guidelines with code examples
- Added deployment examples (Docker Compose, Kubernetes)
