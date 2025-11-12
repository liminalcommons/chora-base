# SAP-046: Composition - Protocol Specification

**SAP ID**: SAP-046
**Name**: Composition
**Version**: 1.0.0
**Status**: Pilot
**Created**: 2025-11-12
**Last Updated**: 2025-11-12

---

## Purpose

This document provides the complete technical specification for SAP-046 (Composition), including:
- Saga orchestration API and state machine
- Event bus protocol (pub/sub, event schema, delivery guarantees)
- Circuit breaker API and state transitions
- Dependency resolution algorithm
- Idempotency patterns and request ID management
- Retry policies and backoff algorithms
- Configuration file format
- Monitoring and observability integration

---

## 1. Saga Orchestration API

### 1.1 Saga Definition

**File Format**: `saga_definitions.yaml`

```yaml
sagas:
  deploy_environment:
    name: "Deploy Environment"
    description: "Multi-step environment deployment with rollback"
    timeout: 600  # seconds
    steps:
      - id: "register_manifest"
        service: "manifest"
        operation: "register"
        timeout: 30
        compensation: "deregister"
        idempotent: true

      - id: "deploy_containers"
        service: "container-engine"
        operation: "deploy"
        timeout: 120
        compensation: "stop"
        idempotent: true
        depends_on: ["register_manifest"]

      - id: "configure_gateway"
        service: "gateway"
        operation: "add_routes"
        timeout: 30
        compensation: "remove_routes"
        idempotent: true
        depends_on: ["deploy_containers"]

      - id: "mark_ready"
        service: "orchestrator"
        operation: "mark_environment_ready"
        timeout: 10
        compensation: "mark_environment_failed"
        idempotent: true
        depends_on: ["configure_gateway"]
```

---

### 1.2 Saga State Machine

**States**: `pending` → `running` → `compensating` → `completed` | `failed`

**Transitions**:

```python
class SagaState(Enum):
    PENDING = "pending"          # Saga not yet started
    RUNNING = "running"          # Saga in progress
    COMPENSATING = "compensating"  # Rolling back
    COMPLETED = "completed"      # Successfully finished
    FAILED = "failed"            # Failed (compensated or not)
    PAUSED = "paused"            # Paused for manual intervention

class SagaTransition:
    """
    State transition rules:

    PENDING → RUNNING: Start saga execution
    RUNNING → COMPENSATING: Step failed, start rollback
    RUNNING → COMPLETED: All steps succeeded
    RUNNING → PAUSED: Manual pause requested
    COMPENSATING → FAILED: Compensation finished
    PAUSED → RUNNING: Resume execution
    PAUSED → COMPENSATING: Resume with rollback
    """
    pass
```

**Persistence Schema** (PostgreSQL/SQLite):

```sql
CREATE TABLE saga_instances (
    id UUID PRIMARY KEY,
    saga_name VARCHAR(255) NOT NULL,
    state VARCHAR(50) NOT NULL,  -- pending, running, compensating, completed, failed, paused
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    timeout_at TIMESTAMP,
    error_message TEXT,
    metadata JSONB  -- {trace_id, correlation_id, requester, etc.}
);

CREATE TABLE saga_steps (
    id UUID PRIMARY KEY,
    saga_instance_id UUID NOT NULL REFERENCES saga_instances(id) ON DELETE CASCADE,
    step_id VARCHAR(255) NOT NULL,  -- from saga_definitions.yaml
    state VARCHAR(50) NOT NULL,  -- pending, running, completed, failed, compensated
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    input_data JSONB,
    output_data JSONB,
    compensation_data JSONB,  -- data needed for rollback
    retry_count INT DEFAULT 0,
    UNIQUE (saga_instance_id, step_id)
);

CREATE INDEX idx_saga_instances_state ON saga_instances(state);
CREATE INDEX idx_saga_steps_saga_id ON saga_steps(saga_instance_id);
```

---

### 1.3 Saga Execution API

**Endpoint**: `POST /api/v1/sagas/{saga_name}/execute`

**Request**:
```json
{
  "saga_name": "deploy_environment",
  "input_data": {
    "environment_id": "env_prod_001",
    "services": [
      {
        "name": "analyzer",
        "image": "chora/analyzer:1.2.0",
        "port": 8080
      },
      {
        "name": "executor",
        "image": "chora/executor:1.5.0",
        "port": 8081,
        "depends_on": ["analyzer"]
      }
    ],
    "requester": "ops_team"
  },
  "metadata": {
    "trace_id": "trace_xyz789",
    "correlation_id": "workflow_456",
    "idempotency_key": "deploy_prod_001_20251112"
  },
  "timeout": 600
}
```

**Response** (202 Accepted):
```json
{
  "saga_instance_id": "saga_abc123",
  "saga_name": "deploy_environment",
  "state": "running",
  "created_at": "2025-11-12T10:15:00Z",
  "timeout_at": "2025-11-12T10:25:00Z",
  "status_url": "/api/v1/sagas/saga_abc123/status",
  "cancel_url": "/api/v1/sagas/saga_abc123/cancel"
}
```

---

**Endpoint**: `GET /api/v1/sagas/{saga_instance_id}/status`

**Response**:
```json
{
  "saga_instance_id": "saga_abc123",
  "saga_name": "deploy_environment",
  "state": "running",
  "created_at": "2025-11-12T10:15:00Z",
  "started_at": "2025-11-12T10:15:01Z",
  "timeout_at": "2025-11-12T10:25:00Z",
  "current_step": "deploy_containers",
  "steps": [
    {
      "step_id": "register_manifest",
      "state": "completed",
      "started_at": "2025-11-12T10:15:01Z",
      "completed_at": "2025-11-12T10:15:03Z",
      "retry_count": 0
    },
    {
      "step_id": "deploy_containers",
      "state": "running",
      "started_at": "2025-11-12T10:15:03Z",
      "retry_count": 1
    },
    {
      "step_id": "configure_gateway",
      "state": "pending"
    },
    {
      "step_id": "mark_ready",
      "state": "pending"
    }
  ],
  "progress": {
    "completed_steps": 1,
    "total_steps": 4,
    "percent": 25
  }
}
```

---

**Endpoint**: `POST /api/v1/sagas/{saga_instance_id}/cancel`

**Request**:
```json
{
  "reason": "Deployment taking too long, rolling back",
  "compensate": true  // If true, run compensation; if false, just mark failed
}
```

**Response**:
```json
{
  "saga_instance_id": "saga_abc123",
  "state": "compensating",
  "message": "Cancellation requested, rolling back completed steps"
}
```

---

### 1.4 Compensation API

**Automatic Compensation**: Triggered when a step fails

**Manual Compensation**: Triggered via cancel endpoint

**Compensation Order**: Reverse order of completed steps

**Compensation Idempotency**: Each compensation operation MUST be idempotent (can be called multiple times safely)

**Example Compensation Flow**:

```python
async def compensate_saga(saga_instance_id: str):
    """
    Compensate (rollback) a failed saga.
    Steps are compensated in reverse order.
    """
    saga = await db.get_saga_instance(saga_instance_id)
    completed_steps = await db.get_completed_steps(saga_instance_id)

    # Update saga state
    await db.update_saga_state(saga_instance_id, SagaState.COMPENSATING)

    # Compensate in reverse order
    for step in reversed(completed_steps):
        try:
            compensation_func = get_compensation_function(step.step_id)
            await compensation_func(step.compensation_data)

            # Mark step as compensated
            await db.update_step_state(
                saga_instance_id,
                step.step_id,
                state="compensated"
            )
        except Exception as e:
            logger.error(f"Compensation failed for {step.step_id}: {e}")
            # Continue with other compensations (best effort)

    # Mark saga as failed (but compensated)
    await db.update_saga_state(
        saga_instance_id,
        SagaState.FAILED,
        error_message="Saga failed but compensated successfully"
    )
```

---

## 2. Event Bus Protocol

### 2.1 Event Schema (CloudEvents Standard)

**Format**: JSON (CloudEvents 1.0)

```json
{
  "specversion": "1.0",
  "type": "environment.lifecycle.created",
  "source": "orchestrator",
  "id": "evt_abc123",
  "time": "2025-11-12T10:15:00Z",
  "datacontenttype": "application/json",
  "data": {
    "environment_id": "env_prod_001",
    "services": ["analyzer", "executor", "storage"],
    "requester": "ops_team"
  },
  "subject": "environment/env_prod_001",
  "traceparent": "00-trace_xyz789-span_123-01",
  "choracorrelationid": "workflow_456"
}
```

**Required Fields**:
- `specversion`: "1.0" (CloudEvents version)
- `type`: Event type (domain.entity.verb format)
- `source`: Service that emitted the event
- `id`: Unique event ID (UUID or similar)
- `time`: ISO 8601 timestamp

**Optional Fields**:
- `datacontenttype`: Content type of `data` field
- `data`: Event payload
- `subject`: Resource this event is about
- `traceparent`: W3C Trace Context for distributed tracing
- `choracorrelationid`: Chora-specific correlation ID

---

### 2.2 Event Types (Registry)

**Naming Convention**: `{domain}.{entity}.{verb}`

**Examples**:
- `environment.lifecycle.created`
- `environment.lifecycle.deleted`
- `environment.lifecycle.updated`
- `service.health.degraded`
- `service.health.recovered`
- `deployment.status.started`
- `deployment.status.completed`
- `deployment.status.failed`
- `saga.execution.started`
- `saga.execution.completed`
- `saga.execution.failed`
- `saga.execution.compensated`

**Event Type Registry**: `event_types.yaml`

```yaml
event_types:
  environment.lifecycle.created:
    description: "Environment successfully created"
    schema_version: "1.0"
    data_schema:
      type: object
      required: [environment_id, services]
      properties:
        environment_id: {type: string}
        services: {type: array, items: {type: string}}
        requester: {type: string}

  saga.execution.failed:
    description: "Saga execution failed (before or after compensation)"
    schema_version: "1.0"
    data_schema:
      type: object
      required: [saga_instance_id, saga_name, error]
      properties:
        saga_instance_id: {type: string}
        saga_name: {type: string}
        error: {type: string}
        failed_step: {type: string}
        compensated: {type: boolean}
```

---

### 2.3 Pub/Sub API

**Backend Options**: Redis Pub/Sub, NATS, RabbitMQ, in-memory (dev only)

**Recommended**: Redis Pub/Sub for Essential/Recommended tiers

---

**Publish API**: `POST /api/v1/events/publish`

**Request**:
```json
{
  "type": "environment.lifecycle.created",
  "source": "orchestrator",
  "data": {
    "environment_id": "env_prod_001",
    "services": ["analyzer", "executor"]
  },
  "metadata": {
    "trace_id": "trace_xyz789",
    "correlation_id": "workflow_456"
  }
}
```

**Response**:
```json
{
  "event_id": "evt_abc123",
  "published_at": "2025-11-12T10:15:00Z",
  "channel": "environment.lifecycle"
}
```

---

**Subscribe API**: WebSocket or SSE

**WebSocket** (Recommended):

```javascript
// Client subscribes to events
const ws = new WebSocket("ws://orchestrator:8080/api/v1/events/subscribe");

ws.send(JSON.stringify({
  action: "subscribe",
  channels: ["environment.lifecycle.*", "saga.execution.*"]
}));

ws.onmessage = (event) => {
  const cloudEvent = JSON.parse(event.data);
  console.log("Received event:", cloudEvent.type, cloudEvent.data);
};
```

**SSE** (Alternative):

```bash
curl -N http://orchestrator:8080/api/v1/events/stream?channels=environment.lifecycle.*,saga.execution.*
```

---

**CLI Subscribe**:

```bash
# Subscribe to events (blocks, prints events as they arrive)
chora-compose events subscribe --channels "environment.lifecycle.*,saga.execution.*"

# Output (JSONL):
{"type":"environment.lifecycle.created","source":"orchestrator","id":"evt_abc123",...}
{"type":"saga.execution.started","source":"orchestrator","id":"evt_def456",...}
```

---

### 2.4 Event Delivery Guarantees

**At-Least-Once Delivery**:
- Events MAY be delivered multiple times
- Subscribers MUST handle duplicate events idempotently
- Use `id` field to deduplicate

**Ordering**:
- Events from the same source are delivered in order
- Events from different sources have no ordering guarantees

**Persistence**:
- Events are NOT persisted by default (pub/sub is ephemeral)
- Optional: Enable event log (append-only storage for audit/replay)

**Event Log**: `event_log.jsonl` (if enabled)

```jsonl
{"specversion":"1.0","type":"environment.lifecycle.created","source":"orchestrator","id":"evt_abc123","time":"2025-11-12T10:15:00Z","data":{...}}
{"specversion":"1.0","type":"saga.execution.started","source":"orchestrator","id":"evt_def456","time":"2025-11-12T10:15:01Z","data":{...}}
```

**Configuration**:

```yaml
# config.yaml
event_bus:
  backend: "redis"  # redis, nats, rabbitmq, memory
  redis:
    host: "localhost"
    port: 6379
    db: 0

  persistence:
    enabled: true
    log_file: "event_log.jsonl"
    max_size_mb: 1000  # Rotate after 1GB

  delivery:
    guarantee: "at-least-once"  # at-most-once, at-least-once
    retry_attempts: 3
    retry_backoff: 1  # seconds (exponential)
```

---

## 3. Circuit Breaker API

### 3.1 Circuit Breaker State Machine

**States**: `closed` → `open` → `half-open` → `closed`

**Transitions**:
- `closed → open`: Failure threshold exceeded
- `open → half-open`: Timeout expired, allow test requests
- `half-open → closed`: Test requests succeeded
- `half-open → open`: Test requests failed

**Parameters**:
- `failure_threshold`: Number of consecutive failures to open circuit (default: 5)
- `success_threshold`: Number of consecutive successes in half-open to close circuit (default: 3)
- `timeout`: Seconds to wait before transitioning from open to half-open (default: 30)
- `half_open_max_calls`: Max concurrent requests in half-open state (default: 3)

---

### 3.2 Circuit Breaker Configuration

**File**: `circuit_breakers.yaml`

```yaml
circuit_breakers:
  manifest_service:
    failure_threshold: 5
    success_threshold: 3
    timeout: 30
    half_open_max_calls: 3
    exceptions:
      - ConnectionError
      - TimeoutError
      - HTTPError  # Only 5xx errors

  analyzer_service:
    failure_threshold: 10  # More tolerant
    success_threshold: 5
    timeout: 60
    half_open_max_calls: 5

  storage_service:
    failure_threshold: 3  # Less tolerant (critical)
    success_threshold: 2
    timeout: 15
    half_open_max_calls: 1
```

---

### 3.3 Circuit Breaker API

**Programmatic API**:

```python
from chora_compose.composition import CircuitBreaker

# Initialize circuit breaker
cb = CircuitBreaker(
    name="manifest_service",
    failure_threshold=5,
    success_threshold=3,
    timeout=30
)

# Call service through circuit breaker
try:
    result = await cb.call(manifest_client.register, service_config)
except CircuitOpenError:
    logger.error("Circuit open, manifest service unavailable")
    # Fallback: queue request for later
    await request_queue.enqueue(service_config)
```

**Decorator API**:

```python
from chora_compose.composition import circuit_breaker

@circuit_breaker(
    name="analyzer_service",
    failure_threshold=10,
    timeout=60
)
async def call_analyzer(prompt: str) -> str:
    """Call analyzer service (protected by circuit breaker)."""
    response = await http_client.post(
        "http://analyzer:8080/analyze",
        json={"prompt": prompt}
    )
    return response.json()["result"]

# Usage (circuit breaker is transparent)
result = await call_analyzer("Analyze this code...")
```

---

**Status API**: `GET /api/v1/circuit-breakers`

**Response**:
```json
{
  "circuit_breakers": [
    {
      "name": "manifest_service",
      "state": "closed",
      "failure_count": 2,
      "success_count": 0,
      "last_failure_time": "2025-11-12T10:10:00Z",
      "last_state_change": "2025-11-12T10:00:00Z"
    },
    {
      "name": "analyzer_service",
      "state": "open",
      "failure_count": 10,
      "success_count": 0,
      "last_failure_time": "2025-11-12T10:14:30Z",
      "last_state_change": "2025-11-12T10:14:30Z",
      "will_retry_at": "2025-11-12T10:15:30Z"
    }
  ]
}
```

---

**Manual Control**: `POST /api/v1/circuit-breakers/{name}/reset`

**Request**:
```json
{
  "force_state": "closed"  // closed, open, half-open
}
```

**Response**:
```json
{
  "name": "analyzer_service",
  "state": "closed",
  "message": "Circuit breaker manually reset to closed state"
}
```

---

## 4. Dependency Resolution API

### 4.1 Dependency Declaration

**File**: `manifest.yaml` (per service)

```yaml
service:
  name: "executor"
  version: "1.5.0"
  dependencies:
    - name: "analyzer"
      version: ">=1.2.0"
      required: true
      health_check: "http://analyzer:8080/health"

    - name: "storage"
      version: ">=2.0.0"
      required: true
      health_check: "http://storage:8081/health"

    - name: "logging"
      version: ">=1.0.0"
      required: false  # Optional dependency
      health_check: "http://logging:8082/health"
```

---

### 4.2 Dependency Resolution Algorithm

**Topological Sort** (Kahn's Algorithm):

```python
def resolve_dependencies(services: List[Service]) -> List[Service]:
    """
    Resolve service dependencies, return services in startup order.
    Raises CircularDependencyError if cycle detected.
    """
    # Build graph
    graph = {s.name: [d.name for d in s.dependencies] for s in services}
    in_degree = {s.name: 0 for s in services}

    for service in services:
        for dep in service.dependencies:
            if dep.name not in in_degree:
                raise MissingDependencyError(
                    f"Service {service.name} depends on {dep.name}, which is not in manifest"
                )
            in_degree[dep.name] += 1

    # Topological sort
    queue = [s for s in services if in_degree[s.name] == 0]
    sorted_services = []

    while queue:
        service = queue.pop(0)
        sorted_services.append(service)

        for dep_name in graph[service.name]:
            in_degree[dep_name] -= 1
            if in_degree[dep_name] == 0:
                dep_service = next(s for s in services if s.name == dep_name)
                queue.append(dep_service)

    # Check for cycles
    if len(sorted_services) != len(services):
        unresolved = [s.name for s in services if s not in sorted_services]
        raise CircularDependencyError(
            f"Circular dependency detected involving: {unresolved}"
        )

    return sorted_services
```

---

**CLI**: `chora-compose deps resolve`

```bash
# Resolve dependencies from manifest files
chora-compose deps resolve --manifest services/*/manifest.yaml

# Output (startup order):
1. logging (no dependencies)
2. analyzer (no dependencies)
3. storage (no dependencies)
4. executor (depends on: analyzer, storage)
5. orchestrator (depends on: executor)
```

---

**API**: `POST /api/v1/dependencies/resolve`

**Request**:
```json
{
  "services": [
    {
      "name": "executor",
      "dependencies": [
        {"name": "analyzer", "required": true},
        {"name": "storage", "required": true}
      ]
    },
    {
      "name": "analyzer",
      "dependencies": []
    },
    {
      "name": "storage",
      "dependencies": []
    }
  ]
}
```

**Response**:
```json
{
  "startup_order": [
    {"name": "analyzer", "level": 0},
    {"name": "storage", "level": 0},
    {"name": "executor", "level": 1}
  ],
  "dependency_graph": {
    "analyzer": [],
    "storage": [],
    "executor": ["analyzer", "storage"]
  }
}
```

---

### 4.3 Version Constraints

**Supported Operators**:
- `=1.2.0`: Exact version
- `>=1.2.0`: Greater than or equal
- `<=1.5.0`: Less than or equal
- `>=1.2.0,<2.0.0`: Range (AND)
- `^1.2.0`: Compatible (1.2.0 <= version < 2.0.0, semver caret)
- `~1.2.0`: Approximately (1.2.0 <= version < 1.3.0, semver tilde)

**Version Resolution**:

```python
def check_version_constraint(actual: str, constraint: str) -> bool:
    """
    Check if actual version satisfies constraint.
    Uses semantic versioning (semver) rules.
    """
    from packaging.version import Version
    from packaging.specifiers import SpecifierSet

    specifier = SpecifierSet(constraint)
    return Version(actual) in specifier

# Examples:
check_version_constraint("1.2.5", ">=1.2.0")  # True
check_version_constraint("1.2.5", "^1.2.0")   # True (1.2.0 <= 1.2.5 < 2.0.0)
check_version_constraint("2.0.0", "^1.2.0")   # False (2.0.0 >= 2.0.0)
```

---

## 5. Idempotency Patterns

### 5.1 Request ID Pattern

**Header**: `X-Idempotency-Key` or `Chora-Idempotency-Key`

**Server Implementation**:

```python
from datetime import datetime, timedelta

# In-memory cache (production: use Redis)
idempotency_cache = {}

async def idempotent_handler(request):
    """
    Handle idempotent request using X-Idempotency-Key header.
    If request with same key seen before, return cached response.
    """
    idempotency_key = request.headers.get("X-Idempotency-Key")

    if not idempotency_key:
        return await handle_request(request)  # Not idempotent

    # Check cache
    cached = idempotency_cache.get(idempotency_key)
    if cached and cached["expires_at"] > datetime.utcnow():
        return cached["response"]

    # Process request
    response = await handle_request(request)

    # Cache response (24 hour TTL)
    idempotency_cache[idempotency_key] = {
        "response": response,
        "expires_at": datetime.utcnow() + timedelta(hours=24)
    }

    return response
```

**Client Usage**:

```python
import uuid

# Generate idempotency key (UUID or hash of request)
idempotency_key = str(uuid.uuid4())

# Make request with idempotency key
response = await http_client.post(
    "http://orchestrator:8080/api/v1/environments/deploy",
    json={"environment_id": "env_prod_001", ...},
    headers={"X-Idempotency-Key": idempotency_key}
)

# Retry (safe, will return same response)
response2 = await http_client.post(
    "http://orchestrator:8080/api/v1/environments/deploy",
    json={"environment_id": "env_prod_001", ...},
    headers={"X-Idempotency-Key": idempotency_key}  # Same key
)

assert response == response2  # Same response
```

---

### 5.2 Natural Idempotency

**Guideline**: Design operations to be naturally idempotent whenever possible.

**Examples**:

**PUT (Set value)**:
```python
# Idempotent: setting value to X always results in value being X
PUT /api/v1/config/analyzer/max_workers
{"value": 4}

# Calling twice has same effect as calling once
```

**DELETE (Remove resource)**:
```python
# Idempotent: deleting resource X always results in X not existing
DELETE /api/v1/environments/env_prod_001

# Calling twice: first deletes, second returns 404 (but resource is still deleted)
```

**Conditional Operations** (not idempotent):
```python
# NOT idempotent: incrementing depends on current value
POST /api/v1/metrics/increment
{"metric": "request_count", "delta": 1}

# Calling twice increments by 2 (different result)
```

---

### 5.3 Idempotency for Saga Steps

**Requirement**: All Saga steps MUST be idempotent.

**Implementation**:

```python
async def deploy_container_idempotent(service_name: str, image: str):
    """
    Deploy container (idempotent).
    If container already exists with same image, return existing container.
    """
    existing = await docker_client.containers.get(service_name)

    if existing and existing.image == image:
        logger.info(f"Container {service_name} already exists with image {image}")
        return existing  # Idempotent: return existing

    if existing and existing.image != image:
        logger.info(f"Container {service_name} exists with different image, recreating")
        await existing.stop()
        await existing.remove()

    # Create new container
    container = await docker_client.containers.create(
        name=service_name,
        image=image,
        detach=True
    )
    await container.start()
    return container
```

---

## 6. Retry Policies

### 6.1 Exponential Backoff Algorithm

**Formula**: `delay = min(initial_delay * (backoff_factor ** attempt), max_delay)`

**Configuration**:

```yaml
# config.yaml
retry_policies:
  default:
    max_attempts: 5
    initial_delay: 1  # seconds
    max_delay: 60  # seconds
    backoff_factor: 2
    jitter: 0.1  # ±10% random jitter
    retryable_errors:
      - ConnectionError
      - TimeoutError
      - HTTPError.5xx  # Only 5xx errors

  critical:
    max_attempts: 10
    initial_delay: 0.5
    max_delay: 30
    backoff_factor: 2
```

**Delays** (default policy):
- Attempt 1: 1s
- Attempt 2: 2s
- Attempt 3: 4s
- Attempt 4: 8s
- Attempt 5: 16s
- (Capped at 60s for subsequent attempts)

---

### 6.2 Retry Implementation

```python
import asyncio
import random

async def retry_with_backoff(
    func,
    max_attempts=5,
    initial_delay=1,
    max_delay=60,
    backoff_factor=2,
    jitter=0.1,
    retryable_errors=(ConnectionError, TimeoutError)
):
    """
    Retry function with exponential backoff and jitter.
    """
    delay = initial_delay
    last_exception = None

    for attempt in range(max_attempts):
        try:
            return await func()
        except retryable_errors as e:
            last_exception = e

            if attempt < max_attempts - 1:
                # Add jitter (±10% random variation)
                jitter_amount = delay * jitter * random.uniform(-1, 1)
                actual_delay = delay + jitter_amount

                logger.warning(
                    f"Attempt {attempt + 1} failed: {e}. "
                    f"Retrying in {actual_delay:.2f}s..."
                )

                await asyncio.sleep(actual_delay)
                delay = min(delay * backoff_factor, max_delay)
        except Exception as e:
            # Non-retryable error, fail immediately
            logger.error(f"Non-retryable error: {e}")
            raise

    # Max attempts exceeded
    logger.error(f"Max attempts ({max_attempts}) exceeded")
    raise last_exception

# Usage:
result = await retry_with_backoff(
    lambda: http_client.post("http://analyzer:8080/analyze", json={...}),
    max_attempts=5,
    initial_delay=1
)
```

---

### 6.3 Retry Decorator

```python
from chora_compose.composition import retry

@retry(
    max_attempts=5,
    initial_delay=1,
    retryable_errors=(ConnectionError, TimeoutError)
)
async def call_analyzer(prompt: str) -> str:
    """Call analyzer service (with automatic retry)."""
    response = await http_client.post(
        "http://analyzer:8080/analyze",
        json={"prompt": prompt}
    )
    return response.json()["result"]

# Usage (retry is transparent)
result = await call_analyzer("Analyze this code...")
```

---

## 7. Configuration File Format

### 7.1 Main Configuration

**File**: `composition.yaml`

```yaml
# Composition Configuration
version: "1.0"

# Saga Orchestration
sagas:
  definitions_file: "saga_definitions.yaml"
  persistence:
    backend: "postgresql"  # postgresql, sqlite, memory
    connection_string: "postgresql://user:pass@localhost:5432/chora"
  timeout_default: 600  # seconds

# Event Bus
event_bus:
  backend: "redis"  # redis, nats, rabbitmq, memory
  redis:
    host: "localhost"
    port: 6379
    db: 0
  persistence:
    enabled: true
    log_file: "event_log.jsonl"
    max_size_mb: 1000
  delivery:
    guarantee: "at-least-once"
    retry_attempts: 3

# Circuit Breakers
circuit_breakers:
  definitions_file: "circuit_breakers.yaml"
  metrics:
    enabled: true
    export_interval: 60  # seconds

# Dependency Resolution
dependencies:
  validation:
    enabled: true
    fail_on_circular: true
    fail_on_missing: true
  health_checks:
    enabled: true
    timeout: 10  # seconds
    retries: 3

# Retry Policies
retry_policies:
  definitions_file: "retry_policies.yaml"

# Monitoring
monitoring:
  prometheus:
    enabled: true
    port: 9090
    path: "/metrics"
  opentelemetry:
    enabled: true
    endpoint: "http://otel-collector:4318"
  logging:
    level: "INFO"  # DEBUG, INFO, WARNING, ERROR
    format: "json"  # json, text
```

---

### 7.2 Saga Definitions

**File**: `saga_definitions.yaml` (see Section 1.1)

---

### 7.3 Circuit Breaker Definitions

**File**: `circuit_breakers.yaml` (see Section 3.2)

---

### 7.4 Retry Policies

**File**: `retry_policies.yaml`

```yaml
retry_policies:
  default:
    max_attempts: 5
    initial_delay: 1
    max_delay: 60
    backoff_factor: 2
    jitter: 0.1
    retryable_errors:
      - ConnectionError
      - TimeoutError
      - HTTPError.5xx

  critical:
    max_attempts: 10
    initial_delay: 0.5
    max_delay: 30
    backoff_factor: 2
    jitter: 0.05

  non_critical:
    max_attempts: 3
    initial_delay: 2
    max_delay: 60
    backoff_factor: 3
```

---

## 8. Monitoring & Observability

### 8.1 Prometheus Metrics

**Endpoint**: `GET /metrics`

**Metrics**:

```prometheus
# Saga metrics
saga_executions_total{saga_name, status}         # Counter: total saga executions
saga_duration_seconds{saga_name}                 # Histogram: saga duration
saga_step_duration_seconds{saga_name, step_id}   # Histogram: step duration
saga_compensation_total{saga_name}               # Counter: total compensations

# Circuit breaker metrics
circuit_breaker_state{name, state}               # Gauge: current state (0=closed, 1=open, 2=half-open)
circuit_breaker_failures_total{name}             # Counter: total failures
circuit_breaker_successes_total{name}            # Counter: total successes
circuit_breaker_transitions_total{name, from, to} # Counter: state transitions

# Event bus metrics
event_bus_published_total{type}                  # Counter: events published
event_bus_delivered_total{type}                  # Counter: events delivered
event_bus_errors_total{type, error}              # Counter: delivery errors

# Dependency metrics
dependency_check_duration_seconds{service}       # Histogram: health check duration
dependency_check_failures_total{service}         # Counter: health check failures
```

---

### 8.2 OpenTelemetry Tracing

**Spans**:
- `saga.execute`: Top-level saga execution
- `saga.step.{step_id}`: Individual step execution
- `saga.compensate`: Compensation execution
- `circuit_breaker.call`: Circuit breaker call
- `event_bus.publish`: Event publication
- `event_bus.deliver`: Event delivery
- `dependency.resolve`: Dependency resolution

**Trace Propagation**: W3C Trace Context (traceparent header)

**Example Trace**:

```
saga.execute (saga_abc123, deploy_environment)
├── saga.step.register_manifest (2.1s)
│   └── http.post /api/v1/manifest/register
├── saga.step.deploy_containers (45.3s)
│   ├── docker.create (analyzer)
│   ├── docker.start (analyzer)
│   ├── docker.create (executor)
│   └── docker.start (executor)
├── saga.step.configure_gateway (1.8s)
│   └── http.post /api/v1/gateway/routes
└── saga.step.mark_ready (0.5s)
    └── database.update environments SET status='ready'
```

---

### 8.3 Logging

**Log Format** (JSON):

```json
{
  "timestamp": "2025-11-12T10:15:00.123Z",
  "level": "INFO",
  "logger": "chora_compose.composition.saga",
  "message": "Saga execution started",
  "saga_instance_id": "saga_abc123",
  "saga_name": "deploy_environment",
  "trace_id": "trace_xyz789",
  "correlation_id": "workflow_456"
}
```

**Log Levels**:
- `DEBUG`: Detailed debugging information (step inputs/outputs, retry attempts)
- `INFO`: General information (saga started, step completed)
- `WARNING`: Warnings (retry after failure, circuit breaker opened)
- `ERROR`: Errors (step failed, compensation failed)

---

### 8.4 Health Check API

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "components": {
    "database": {
      "status": "healthy",
      "latency_ms": 12
    },
    "event_bus": {
      "status": "healthy",
      "backend": "redis",
      "connected": true
    },
    "circuit_breakers": {
      "status": "degraded",
      "open_circuits": ["analyzer_service"],
      "message": "1 circuit breaker open"
    }
  },
  "metrics": {
    "active_sagas": 3,
    "total_sagas_today": 47,
    "success_rate": 0.95
  }
}
```

---

## 9. CLI Reference

### 9.1 Saga Commands

```bash
# Execute saga
chora-compose saga execute deploy_environment \
  --input '{"environment_id":"env_prod_001","services":[...]}' \
  --timeout 600

# Get saga status
chora-compose saga status saga_abc123

# Cancel saga (with compensation)
chora-compose saga cancel saga_abc123 --compensate

# List sagas
chora-compose saga list --state running --limit 10

# Saga history
chora-compose saga history --saga-name deploy_environment --days 7
```

---

### 9.2 Event Bus Commands

```bash
# Publish event
chora-compose events publish \
  --type environment.lifecycle.created \
  --source orchestrator \
  --data '{"environment_id":"env_prod_001"}'

# Subscribe to events (blocks)
chora-compose events subscribe --channels "environment.*,saga.*"

# Event log
chora-compose events log --tail 100 --follow
```

---

### 9.3 Circuit Breaker Commands

```bash
# List circuit breakers
chora-compose circuit-breaker list

# Get circuit breaker status
chora-compose circuit-breaker status manifest_service

# Reset circuit breaker
chora-compose circuit-breaker reset analyzer_service --force-state closed
```

---

### 9.4 Dependency Commands

```bash
# Resolve dependencies
chora-compose deps resolve --manifest services/*/manifest.yaml

# Validate dependencies (check for cycles, missing deps)
chora-compose deps validate --manifest services/*/manifest.yaml

# Generate dependency graph
chora-compose deps graph --output deps.dot --format dot
```

---

## 10. Python API Reference

### 10.1 Saga API

```python
from chora_compose.composition import SagaOrchestrator

# Initialize orchestrator
orchestrator = SagaOrchestrator(
    definitions_file="saga_definitions.yaml",
    persistence_backend="postgresql",
    connection_string="postgresql://..."
)

# Execute saga
saga_instance = await orchestrator.execute(
    saga_name="deploy_environment",
    input_data={
        "environment_id": "env_prod_001",
        "services": [...]
    },
    timeout=600,
    metadata={
        "trace_id": "trace_xyz789",
        "correlation_id": "workflow_456"
    }
)

# Get saga status
status = await orchestrator.get_status(saga_instance.id)

# Cancel saga
await orchestrator.cancel(saga_instance.id, compensate=True)
```

---

### 10.2 Event Bus API

```python
from chora_compose.composition import EventBus

# Initialize event bus
event_bus = EventBus(backend="redis", redis_config={...})

# Publish event
await event_bus.publish(
    type="environment.lifecycle.created",
    source="orchestrator",
    data={
        "environment_id": "env_prod_001",
        "services": ["analyzer", "executor"]
    },
    metadata={"trace_id": "trace_xyz789"}
)

# Subscribe to events
async def handle_event(event):
    print(f"Received: {event.type}")

await event_bus.subscribe(
    channels=["environment.lifecycle.*"],
    handler=handle_event
)
```

---

### 10.3 Circuit Breaker API

```python
from chora_compose.composition import CircuitBreaker

# Initialize circuit breaker
cb = CircuitBreaker(
    name="manifest_service",
    failure_threshold=5,
    timeout=30
)

# Call through circuit breaker
try:
    result = await cb.call(manifest_client.register, service_config)
except CircuitOpenError:
    # Circuit open, handle fallback
    pass
```

---

### 10.4 Dependency Resolver API

```python
from chora_compose.composition import DependencyResolver

# Initialize resolver
resolver = DependencyResolver()

# Resolve dependencies
sorted_services = resolver.resolve(services)

# Validate dependencies
resolver.validate(services)  # Raises CircularDependencyError if cycle detected
```

---

## 11. Integration with Other SAPs

### 11.1 SAP-042 (InterfaceDesign)

**Integration**: Composition SAP uses capability interfaces defined in InterfaceDesign SAP.

**Example**: Saga steps call capability methods via standardized interfaces:

```python
# Saga step: register in manifest
manifest_client = CapabilityClient("manifest", interface_version="1.0")
result = await manifest_client.call("register", service_config)
```

---

### 11.2 SAP-044 (Registry)

**Integration**: Composition SAP queries Manifest Registry for service discovery.

**Example**: Circuit breaker uses registry to discover service endpoints:

```python
# Discover analyzer service
analyzer_url = await registry.discover("analyzer", version=">=1.2.0")
circuit_breaker = CircuitBreaker("analyzer", url=analyzer_url)
```

---

### 11.3 SAP-045 (Bootstrap)

**Integration**: Bootstrap SAP uses Composition SAP for phased deployment orchestration.

**Example**: Bootstrap phases are implemented as Sagas:

```yaml
# bootstrap_saga.yaml
sagas:
  bootstrap_phase_1:
    steps:
      - deploy_manifest_registry
      - wait_for_manifest_health
```

---

### 11.4 SAP-010 (A-MEM)

**Integration**: Composition SAP emits events to A-MEM for audit/replay.

**Example**: Saga events are recorded in A-MEM:

```python
# Saga execution generates A-MEM events
await amem.record_event({
    "type": "saga.execution.started",
    "saga_instance_id": "saga_abc123",
    "saga_name": "deploy_environment"
})
```

---

### 11.5 SAP-015 (Beads Task Tracking)

**Integration**: Composition SAP can be managed via Beads tasks.

**Example**: Create bead for saga execution:

```bash
bd create "Execute deploy_environment saga" \
  --epic "Environment Deployment" \
  --meta '{"saga":"deploy_environment","env":"prod"}'
```

---

## 12. Security Considerations

### 12.1 Saga Security

**Authorization**: Saga execution requires authenticated user with `saga:execute` permission.

**Credentials**: Saga steps MUST NOT log sensitive data (credentials, API keys).

**Compensation**: Compensation logic MUST clean up any credentials or temporary resources.

---

### 12.2 Event Bus Security

**Authentication**: Event bus connections require authentication token (if Redis AUTH enabled).

**Encryption**: Use TLS for Redis connections in production.

**Event Validation**: Validate event schema to prevent malicious events.

---

### 12.3 Circuit Breaker Security

**Denial of Service**: Circuit breaker prevents cascading failures from overwhelming services.

**Rate Limiting**: Combine circuit breaker with rate limiting for additional protection.

---

## 13. Error Handling

### 13.1 Error Types

**Transient Errors** (Retry):
- `ConnectionError`: Network connection failed
- `TimeoutError`: Request timed out
- `HTTPError 5xx`: Server error (likely transient)

**Permanent Errors** (Fail Immediately):
- `ValidationError`: Invalid input data
- `AuthenticationError`: Invalid credentials
- `HTTPError 4xx` (except 429): Client error (won't succeed on retry)

**Compensation Errors**:
- Log and continue with other compensations (best effort)
- Mark saga as "failed (partially compensated)"

---

### 13.2 Error Responses

**Error Response Format**:

```json
{
  "error": {
    "type": "SagaExecutionError",
    "message": "Saga execution failed at step 'deploy_containers'",
    "saga_instance_id": "saga_abc123",
    "failed_step": "deploy_containers",
    "details": {
      "original_error": "ConnectionError: Failed to connect to docker daemon",
      "retry_count": 5,
      "compensated": true
    },
    "trace_id": "trace_xyz789"
  }
}
```

---

## 14. Performance Tuning

### 14.1 Saga Performance

**Parallel Steps**: Steps with no dependencies can be executed in parallel.

**Configuration**:

```yaml
sagas:
  deploy_environment:
    parallel_execution: true  # Enable parallel steps
    max_concurrency: 5  # Max concurrent steps
```

---

### 14.2 Event Bus Performance

**Batching**: Publish events in batches for better throughput.

```python
# Batch publish
await event_bus.publish_batch([event1, event2, event3])
```

**Compression**: Enable compression for large event payloads.

```yaml
event_bus:
  compression: "gzip"  # gzip, lz4, none
```

---

### 14.3 Circuit Breaker Performance

**Metrics**: Circuit breaker adds <1ms overhead per call.

**Tuning**: Adjust thresholds based on service SLA:
- Critical services: Lower threshold (fail fast)
- Non-critical services: Higher threshold (more tolerant)

---

## 15. Testing

### 15.1 Saga Testing

**Unit Tests**: Test individual steps in isolation.

**Integration Tests**: Test full saga execution with mock services.

**Chaos Testing**: Inject failures to test compensation logic.

**Example**:

```python
async def test_saga_compensation():
    """Test that saga compensates correctly on failure."""
    # Arrange: Create saga with failing step
    saga = SagaOrchestrator(...)

    # Act: Execute saga (will fail at step 2)
    with pytest.raises(SagaExecutionError):
        await saga.execute("deploy_environment", {...})

    # Assert: Check compensation was executed
    assert saga.get_status().state == SagaState.FAILED
    assert saga.get_status().compensated == True
```

---

### 15.2 Circuit Breaker Testing

**Unit Tests**: Test state transitions.

**Integration Tests**: Test with real service calls.

**Example**:

```python
async def test_circuit_breaker_opens_after_failures():
    """Test that circuit breaker opens after failure threshold."""
    cb = CircuitBreaker(failure_threshold=3)

    # Cause 3 failures
    for _ in range(3):
        with pytest.raises(ConnectionError):
            await cb.call(lambda: raise_connection_error())

    # Circuit should be open
    assert cb.state == "open"

    # Next call should fail immediately
    with pytest.raises(CircuitOpenError):
        await cb.call(lambda: successful_call())
```

---

## 16. Migration Guide

### 16.1 Migrating from Ad-Hoc Integration

**Step 1**: Identify existing integration workflows.

**Step 2**: Model workflows as Sagas (define steps, compensations).

**Step 3**: Implement idempotency for all operations.

**Step 4**: Deploy Composition SAP (event bus, Saga orchestrator).

**Step 5**: Migrate workflows one at a time.

---

### 16.2 Migrating from Choreography to Orchestration

**Choreography** (event-driven, no central control):

```python
# Old: Services listen to events and react
@event_listener("environment.created")
async def on_environment_created(event):
    await deploy_containers(event.data["services"])
```

**Orchestration** (Saga-based, central control):

```yaml
# New: Saga defines workflow
sagas:
  deploy_environment:
    steps:
      - create_environment
      - deploy_containers
      - configure_gateway
```

**When to Migrate**: Use orchestration for complex multi-step workflows with compensation requirements.

---

## 17. Versioning

**Protocol Version**: 1.0.0

**Compatibility**:
- **Breaking Changes**: Major version bump (e.g., 1.0.0 → 2.0.0)
- **New Features**: Minor version bump (e.g., 1.0.0 → 1.1.0)
- **Bug Fixes**: Patch version bump (e.g., 1.0.0 → 1.0.1)

**Deprecation Policy**: Deprecated features are supported for 2 minor versions before removal.

---

## 18. Glossary

**Saga**: Distributed transaction pattern with compensating actions for rollback.

**Orchestration**: Central controller coordinates service calls in defined sequence.

**Choreography**: Services react to events independently without central controller.

**Circuit Breaker**: Fail-fast mechanism to prevent cascading failures.

**Idempotency**: Operation produces same result whether run once or multiple times.

**Compensation**: Rollback action to undo a completed step.

**Exponential Backoff**: Retry strategy with increasing delays (1s, 2s, 4s, ...).

**Topological Sort**: Algorithm to order services by dependencies (dependencies first).

**CloudEvents**: Standard event format for interoperability.

**W3C Trace Context**: Standard for distributed tracing (traceparent header).

---

## 19. References

**Standards**:
- CloudEvents 1.0: https://cloudevents.io/
- W3C Trace Context: https://www.w3.org/TR/trace-context/
- Semantic Versioning: https://semver.org/

**Patterns**:
- Saga Pattern: https://microservices.io/patterns/data/saga.html
- Circuit Breaker: https://martinfowler.com/bliki/CircuitBreaker.html

**Related SAPs**:
- SAP-042: InterfaceDesign
- SAP-043: MultiInterface
- SAP-044: Registry
- SAP-045: Bootstrap
- SAP-010: A-MEM (memory-system)
- SAP-015: Beads (task-tracking)

---

## 20. Changelog

### v1.0.0 (2025-11-12) - Initial Release

**Added**:
- Saga orchestration API (execute, status, cancel)
- Event bus protocol (CloudEvents, pub/sub)
- Circuit breaker API (state machine, manual control)
- Dependency resolution (topological sort, version constraints)
- Idempotency patterns (request ID, natural idempotency)
- Retry policies (exponential backoff, jitter)
- Configuration file format (composition.yaml)
- Monitoring integration (Prometheus, OpenTelemetry)
- CLI reference (saga, events, circuit-breaker, deps commands)
- Python API reference

**Status**: Pilot (pending validation)

---

**Document Version**: 1.0.0
**Maintained By**: Infrastructure Team
**Last Review**: 2025-11-12
**Next Review**: 2025-12-12
