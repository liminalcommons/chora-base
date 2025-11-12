# SAP-046: Composition - Adoption Blueprint

**SAP ID**: SAP-046
**Name**: Composition
**Version**: 1.0.0
**Status**: Pilot
**Created**: 2025-11-12
**Last Updated**: 2025-11-12

---

## Purpose

This adoption blueprint provides a step-by-step guide for implementing SAP-046 (Composition) in your capability server architecture. It includes three adoption tiers (Essential, Recommended, Advanced) with clear prerequisites, effort estimates, and validation steps.

**Core Principle**: "Orchestrate what you control, choreograph what you don't."

---

## Overview

### What You'll Get

**Essential Tier** (2-4 hours):
- Saga orchestration with compensation (rollback)
- In-memory event bus for pub/sub
- Basic circuit breakers
- Dependency resolution (topological sort)
- SQLite persistence

**Recommended Tier** (+2-3 hours):
- Redis-based event bus (production-ready)
- PostgreSQL persistence for sagas
- Retry policies with exponential backoff
- Idempotency patterns (request IDs)
- Prometheus metrics

**Advanced Tier** (+3-5 hours):
- Multi-region event bus (NATS/RabbitMQ)
- Distributed tracing (OpenTelemetry)
- Advanced circuit breaker strategies
- Grafana dashboards
- High availability (HA) Saga orchestrator

---

### Prerequisites

**All Tiers**:
- [x] Python 3.9+ installed
- [x] Docker installed (for containerized services)
- [x] Basic understanding of microservices architecture
- [x] SAP-042 (InterfaceDesign) adopted (capability interfaces)
- [x] SAP-044 (Registry) adopted (service discovery)

**Recommended Tier**:
- [x] Redis 5.0+ installed
- [x] PostgreSQL 12+ installed

**Advanced Tier**:
- [x] NATS/RabbitMQ installed
- [x] OpenTelemetry Collector installed
- [x] Grafana/Prometheus installed

---

## Adoption Tiers

### Tier Comparison

| Feature | Essential | Recommended | Advanced |
|---------|-----------|-------------|----------|
| **Saga Orchestration** | ✅ SQLite | ✅ PostgreSQL | ✅ HA PostgreSQL cluster |
| **Event Bus** | ✅ In-memory | ✅ Redis | ✅ NATS/RabbitMQ (multi-region) |
| **Circuit Breakers** | ✅ Basic | ✅ Metrics-based | ✅ Adaptive thresholds |
| **Dependency Resolution** | ✅ Topological sort | ✅ + Version constraints | ✅ + Health-based validation |
| **Retry Policies** | ❌ | ✅ Exponential backoff | ✅ + Jitter + adaptive |
| **Idempotency** | ❌ | ✅ Request IDs | ✅ + Distributed cache |
| **Monitoring** | ❌ | ✅ Prometheus | ✅ + OpenTelemetry + Grafana |
| **Distributed Tracing** | ❌ | ❌ | ✅ OpenTelemetry |
| **Effort** | 2-4 hours | +2-3 hours | +3-5 hours |
| **Total Effort** | 2-4 hours | 4-7 hours | 7-12 hours |

---

## Essential Tier (2-4 Hours)

**Goal**: Get basic composition patterns working with minimal infrastructure.

**Use Case**: Development environments, proof-of-concept, small-scale deployments.

---

### Phase 1: Installation (30 minutes)

#### 1.1 Install chora-compose Package

```bash
# Install chora-compose with composition support
pip install chora-compose[composition]

# Verify installation
chora-compose --version
# Output: chora-compose 1.0.0 (composition support enabled)
```

#### 1.2 Create Project Structure

```bash
# Create composition configuration directory
mkdir -p config/composition
cd config/composition

# Create directory structure
mkdir -p {sagas,circuit_breakers,events}
```

**Result**: `chora-compose` CLI and Python library installed.

---

### Phase 2: Saga Orchestration Setup (60 minutes)

#### 2.1 Create Saga Configuration

Create `config/composition/composition.yaml`:

```yaml
version: "1.0"

sagas:
  definitions_file: "sagas/definitions.yaml"
  persistence:
    backend: "sqlite"
    connection_string: "saga_state.db"
  timeout_default: 600  # 10 minutes

event_bus:
  backend: "memory"  # In-memory for Essential tier

circuit_breakers:
  definitions_file: "circuit_breakers/definitions.yaml"

dependencies:
  validation:
    enabled: true
    fail_on_circular: true
```

#### 2.2 Define Your First Saga

Create `config/composition/sagas/definitions.yaml`:

```yaml
sagas:
  deploy_environment:
    name: "Deploy Environment"
    description: "Deploy capability server environment"
    timeout: 600  # 10 minutes
    steps:
      # Step 1: Register in manifest
      - id: "register_manifest"
        service: "manifest"
        operation: "register"
        timeout: 30
        compensation: "deregister"
        idempotent: true

      # Step 2: Deploy containers
      - id: "deploy_containers"
        service: "container-engine"
        operation: "deploy"
        timeout: 120
        compensation: "stop"
        idempotent: true
        depends_on: ["register_manifest"]

      # Step 3: Configure gateway
      - id: "configure_gateway"
        service: "gateway"
        operation: "add_routes"
        timeout: 30
        compensation: "remove_routes"
        idempotent: true
        depends_on: ["deploy_containers"]

      # Step 4: Mark environment as ready
      - id: "mark_ready"
        service: "orchestrator"
        operation: "mark_environment_ready"
        timeout: 10
        compensation: "mark_environment_failed"
        idempotent: true
        depends_on: ["configure_gateway"]
```

#### 2.3 Implement Saga Steps

Create `src/composition/saga_steps.py`:

```python
"""
Saga step implementations.
Each step MUST be idempotent and have a compensation operation.
"""
import asyncio
from typing import Dict, Any

class ManifestSteps:
    """Manifest registry saga steps."""

    @staticmethod
    async def register(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register environment in manifest.
        Idempotent: If already registered, return existing entry.
        """
        env_id = data["environment_id"]
        services = data["services"]

        # Check if already registered
        existing = await manifest_client.get_environment(env_id)
        if existing:
            return {"manifest_entry_id": existing["id"], "existed": True}

        # Register new environment
        entry = await manifest_client.register({
            "environment_id": env_id,
            "services": services,
            "status": "provisioning"
        })

        return {"manifest_entry_id": entry["id"], "existed": False}

    @staticmethod
    async def deregister(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deregister environment (compensation for register).
        Idempotent: If not registered, succeed (already deregistered).
        """
        manifest_entry_id = data["manifest_entry_id"]

        try:
            await manifest_client.deregister(manifest_entry_id)
            return {"deregistered": True}
        except NotFoundError:
            # Already deregistered, idempotent success
            return {"deregistered": False, "reason": "not_found"}


class ContainerSteps:
    """Container deployment saga steps."""

    @staticmethod
    async def deploy(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deploy containers.
        Idempotent: If containers already running, return existing.
        """
        services = data["services"]
        deployed = []

        for service in services:
            # Check if container already exists
            existing = await docker_client.containers.get(service["name"])

            if existing and existing.image == service["image"]:
                deployed.append(existing.id)
                continue

            # Remove old container if image changed
            if existing:
                await existing.stop()
                await existing.remove()

            # Create and start new container
            container = await docker_client.containers.create(
                name=service["name"],
                image=service["image"],
                detach=True
            )
            await container.start()
            deployed.append(container.id)

        return {"container_ids": deployed}

    @staticmethod
    async def stop(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Stop containers (compensation for deploy).
        Idempotent: If containers already stopped, succeed.
        """
        container_ids = data["container_ids"]

        for container_id in container_ids:
            try:
                container = await docker_client.containers.get(container_id)
                await container.stop()
                await container.remove()
            except NotFoundError:
                # Container already removed, idempotent success
                pass

        return {"stopped": True}


class GatewaySteps:
    """Gateway configuration saga steps."""

    @staticmethod
    async def add_routes(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Configure gateway routes.
        Idempotent: If routes already exist, succeed.
        """
        services = data["services"]
        routes = []

        for service in services:
            route = await gateway_client.add_route({
                "service": service["name"],
                "port": service["port"],
                "path": f"/{service['name']}"
            })
            routes.append(route["id"])

        return {"route_ids": routes}

    @staticmethod
    async def remove_routes(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove gateway routes (compensation for add_routes).
        Idempotent: If routes already removed, succeed.
        """
        route_ids = data["route_ids"]

        for route_id in route_ids:
            try:
                await gateway_client.remove_route(route_id)
            except NotFoundError:
                # Route already removed, idempotent success
                pass

        return {"removed": True}
```

#### 2.4 Initialize Saga Orchestrator

Create `src/composition/orchestrator.py`:

```python
"""Saga orchestrator initialization."""
from chora_compose.composition import SagaOrchestrator

# Initialize orchestrator
orchestrator = SagaOrchestrator(
    definitions_file="config/composition/sagas/definitions.yaml",
    persistence_backend="sqlite",
    connection_string="saga_state.db"
)

# Register step implementations
orchestrator.register_step("register_manifest", ManifestSteps.register)
orchestrator.register_compensation("register_manifest", ManifestSteps.deregister)

orchestrator.register_step("deploy_containers", ContainerSteps.deploy)
orchestrator.register_compensation("deploy_containers", ContainerSteps.stop)

orchestrator.register_step("configure_gateway", GatewaySteps.add_routes)
orchestrator.register_compensation("configure_gateway", GatewaySteps.remove_routes)

orchestrator.register_step("mark_ready", OrchestratorSteps.mark_ready)
orchestrator.register_compensation("mark_ready", OrchestratorSteps.mark_failed)
```

**Result**: Saga orchestrator configured with SQLite persistence.

---

### Phase 3: Circuit Breakers (30 minutes)

#### 3.1 Configure Circuit Breakers

Create `config/composition/circuit_breakers/definitions.yaml`:

```yaml
circuit_breakers:
  manifest_service:
    failure_threshold: 5
    success_threshold: 3
    timeout: 30
    exceptions:
      - ConnectionError
      - TimeoutError

  analyzer_service:
    failure_threshold: 10  # More tolerant
    success_threshold: 5
    timeout: 60

  executor_service:
    failure_threshold: 5
    success_threshold: 3
    timeout: 30
```

#### 3.2 Wrap Service Calls

Update service clients to use circuit breakers:

```python
from chora_compose.composition import CircuitBreaker

# Initialize circuit breakers
manifest_cb = CircuitBreaker.from_config(
    "manifest_service",
    config_file="config/composition/circuit_breakers/definitions.yaml"
)

analyzer_cb = CircuitBreaker.from_config("analyzer_service", ...)

# Wrap service calls
async def call_manifest_register(data):
    """Call manifest service through circuit breaker."""
    try:
        return await manifest_cb.call(manifest_client.register, data)
    except CircuitOpenError:
        logger.warning("Manifest service unavailable, queuing request")
        # Fallback: queue for later
        await request_queue.enqueue(data)
        raise
```

**Result**: Circuit breakers protect against cascading failures.

---

### Phase 4: Dependency Resolution (30 minutes)

#### 4.1 Declare Service Dependencies

Update `services/executor/manifest.yaml`:

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
```

#### 4.2 Resolve Dependencies

```python
from chora_compose.composition import DependencyResolver

resolver = DependencyResolver()

# Load service manifests
services = [
    load_manifest("services/analyzer/manifest.yaml"),
    load_manifest("services/executor/manifest.yaml"),
    load_manifest("services/storage/manifest.yaml")
]

# Resolve dependencies (topological sort)
try:
    sorted_services = resolver.resolve(services)
    print("Startup order:", [s.name for s in sorted_services])
    # Output: ['analyzer', 'storage', 'executor']
except CircularDependencyError as e:
    logger.error(f"Circular dependency detected: {e}")
```

**Result**: Services start in correct dependency order.

---

### Phase 5: Testing (30 minutes)

#### 5.1 Execute Saga

```python
# Execute saga
saga_instance = await orchestrator.execute(
    saga_name="deploy_environment",
    input_data={
        "environment_id": "env_dev_001",
        "services": [
            {"name": "analyzer", "image": "chora/analyzer:1.2.0", "port": 8080},
            {"name": "executor", "image": "chora/executor:1.5.0", "port": 8081}
        ]
    },
    timeout=600
)

print(f"Saga started: {saga_instance.id}")
```

#### 5.2 Check Status

```bash
# Check saga status
chora-compose saga status {saga_instance_id}

# Expected output:
# Saga: deploy_environment (saga_abc123)
# State: running
# Progress: 2/4 steps completed
#   ✅ register_manifest (completed in 2.1s)
#   ✅ deploy_containers (completed in 45.3s)
#   🔄 configure_gateway (running)
#   ⏳ mark_ready (pending)
```

#### 5.3 Test Compensation (Rollback)

```python
# Simulate failure at step 3
await orchestrator.cancel(saga_instance.id, compensate=True)

# Check compensation executed in reverse order
status = await orchestrator.get_status(saga_instance.id)
assert status.state == "failed"
assert status.compensated == True

# Verify compensations ran:
# 1. Remove gateway routes
# 2. Stop containers
# 3. Deregister from manifest
```

**Result**: Saga executes successfully with automatic rollback on failure.

---

### Phase 6: Validation (30 minutes)

#### Essential Tier Checklist

- [ ] Saga orchestrator initialized with SQLite persistence
- [ ] At least 1 saga defined with 3+ steps
- [ ] All saga steps have compensation logic
- [ ] Circuit breakers configured for critical services
- [ ] Service dependencies declared in manifests
- [ ] Dependency resolution validates no circular dependencies
- [ ] Saga executes successfully end-to-end
- [ ] Compensation (rollback) works when saga fails
- [ ] Circuit breaker opens after failure threshold

**Validation Commands**:

```bash
# Test saga execution
chora-compose saga execute deploy_environment \
  --input '{"environment_id":"env_dev_001","services":[...]}'

# Test dependency resolution
chora-compose deps resolve --manifest services/*/manifest.yaml

# Test circuit breaker
chora-compose circuit-breaker list
```

**Expected Results**:
- ✅ Saga completes in <10 minutes
- ✅ Compensation runs in reverse order on failure
- ✅ Dependencies resolve without circular errors
- ✅ Circuit breaker opens after 5 consecutive failures

---

## Recommended Tier (Essential + 2-3 Hours)

**Goal**: Add production-ready features (Redis, PostgreSQL, monitoring).

**Use Case**: Staging environments, small-to-medium production deployments.

---

### Phase 7: Redis Event Bus (45 minutes)

#### 7.1 Install and Configure Redis

```bash
# Install Redis (macOS)
brew install redis

# Start Redis
redis-server --daemonize yes

# Verify Redis is running
redis-cli ping
# Output: PONG
```

#### 7.2 Update Configuration

Update `config/composition/composition.yaml`:

```yaml
event_bus:
  backend: "redis"  # Changed from "memory"
  redis:
    host: "localhost"
    port: 6379
    db: 0
  persistence:
    enabled: true
    log_file: "logs/event_log.jsonl"
    max_size_mb: 1000
  delivery:
    guarantee: "at-least-once"
    retry_attempts: 3
```

#### 7.3 Test Event Bus

```python
from chora_compose.composition import EventBus

# Initialize Redis-based event bus
event_bus = EventBus(backend="redis", redis_config={"host": "localhost"})

# Publish event
await event_bus.publish(
    type="environment.lifecycle.created",
    source="orchestrator",
    data={"environment_id": "env_prod_001"}
)

# Subscribe to events
async def handle_event(event):
    print(f"Received: {event.type}")

await event_bus.subscribe(
    channels=["environment.lifecycle.*"],
    handler=handle_event
)
```

**Result**: Production-ready event bus with Redis persistence.

---

### Phase 8: PostgreSQL Saga Persistence (45 minutes)

#### 8.1 Install and Configure PostgreSQL

```bash
# Install PostgreSQL (macOS)
brew install postgresql@14

# Start PostgreSQL
brew services start postgresql@14

# Create database
createdb chora_sagas
```

#### 8.2 Update Configuration

Update `config/composition/composition.yaml`:

```yaml
sagas:
  persistence:
    backend: "postgresql"  # Changed from "sqlite"
    connection_string: "postgresql://user:pass@localhost:5432/chora_sagas"
```

#### 8.3 Run Migrations

```bash
# Run database migrations
chora-compose saga migrate --database postgresql://...

# Output:
# ✅ Created table: saga_instances
# ✅ Created table: saga_steps
# ✅ Created indexes
```

**Result**: Saga state persisted in PostgreSQL (supports concurrent access).

---

### Phase 9: Retry Policies (30 minutes)

#### 9.1 Configure Retry Policies

Create `config/composition/retry_policies.yaml`:

```yaml
retry_policies:
  default:
    max_attempts: 5
    initial_delay: 1  # seconds
    max_delay: 60
    backoff_factor: 2
    jitter: 0.1  # ±10% random variation
    retryable_errors:
      - ConnectionError
      - TimeoutError
      - HTTPError.5xx

  critical:
    max_attempts: 10
    initial_delay: 0.5
    max_delay: 30
    backoff_factor: 2
```

Update `config/composition/composition.yaml`:

```yaml
retry_policies:
  definitions_file: "retry_policies.yaml"
```

#### 9.2 Apply Retry Policies

```python
from chora_compose.composition import retry

@retry(policy="default")  # Uses default retry policy
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

**Result**: Transient failures are automatically retried with exponential backoff.

---

### Phase 10: Idempotency with Request IDs (30 minutes)

#### 10.1 Server-Side Idempotency Handler

```python
from chora_compose.composition import idempotent_handler
from datetime import datetime, timedelta
import redis

# Initialize Redis cache for idempotency keys
redis_client = redis.Redis(host="localhost", port=6379, db=1)

@app.post("/api/v1/environments/deploy")
@idempotent_handler(cache=redis_client, ttl=timedelta(hours=24))
async def deploy_environment(request):
    """
    Deploy environment (idempotent).
    X-Idempotency-Key header ensures safe retries.
    """
    env_id = request.json["environment_id"]
    services = request.json["services"]

    # Execute saga (safe to retry with same idempotency key)
    saga_instance = await orchestrator.execute(
        "deploy_environment",
        input_data={"environment_id": env_id, "services": services}
    )

    return {"saga_instance_id": saga_instance.id, "status": "started"}
```

#### 10.2 Client-Side Request ID Generation

```python
import uuid

# Generate idempotency key
idempotency_key = str(uuid.uuid4())

# Make request with idempotency key
response = await http_client.post(
    "http://orchestrator:8080/api/v1/environments/deploy",
    json={"environment_id": "env_prod_001", "services": [...]},
    headers={"X-Idempotency-Key": idempotency_key}
)

# Safe to retry (will return same response)
response2 = await http_client.post(
    "http://orchestrator:8080/api/v1/environments/deploy",
    json={"environment_id": "env_prod_001", "services": [...]},
    headers={"X-Idempotency-Key": idempotency_key}  # Same key
)

assert response == response2  # Guaranteed same response
```

**Result**: Idempotent operations allow safe retries.

---

### Phase 11: Prometheus Metrics (30 minutes)

#### 11.1 Enable Prometheus Exporter

Update `config/composition/composition.yaml`:

```yaml
monitoring:
  prometheus:
    enabled: true
    port: 9090
    path: "/metrics"
```

#### 11.2 Configure Prometheus Scraper

Create `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: "chora_composition"
    static_configs:
      - targets: ["localhost:9090"]
    scrape_interval: 15s
```

Start Prometheus:

```bash
prometheus --config.file=prometheus.yml
```

#### 11.3 View Metrics

```bash
# View metrics endpoint
curl http://localhost:9090/metrics

# Key metrics:
# saga_executions_total{saga_name="deploy_environment",status="success"} 42
# saga_duration_seconds{saga_name="deploy_environment",quantile="0.95"} 45.3
# circuit_breaker_state{name="analyzer_service",state="closed"} 0
# event_bus_published_total{type="environment.lifecycle.created"} 128
```

**Result**: Prometheus metrics for monitoring saga/circuit breaker/event bus.

---

### Phase 12: Validation (30 minutes)

#### Recommended Tier Checklist

- [ ] Redis event bus configured and running
- [ ] PostgreSQL saga persistence configured
- [ ] Retry policies defined and applied
- [ ] Idempotency with request IDs implemented
- [ ] Prometheus metrics enabled and scraped
- [ ] Events published and delivered via Redis
- [ ] Saga state persists across restarts (PostgreSQL)
- [ ] Retries happen with exponential backoff
- [ ] Duplicate requests return same response (idempotency)

**Validation Commands**:

```bash
# Test Redis event bus
chora-compose events publish --type test.event --source test
chora-compose events subscribe --channels "test.*"

# Test PostgreSQL persistence
# (Restart orchestrator, saga state should persist)
chora-compose saga list --state running

# Test Prometheus metrics
curl http://localhost:9090/metrics | grep saga_
```

**Expected Results**:
- ✅ Events delivered via Redis pub/sub
- ✅ Saga state persists after orchestrator restart
- ✅ Failed requests retry automatically (up to 5 times)
- ✅ Duplicate requests (same idempotency key) return same response
- ✅ Prometheus metrics show saga/circuit breaker statistics

---

## Advanced Tier (Recommended + 3-5 Hours)

**Goal**: Add enterprise features (multi-region, distributed tracing, HA).

**Use Case**: Large-scale production deployments, multi-region architectures.

---

### Phase 13: NATS Event Bus (Multi-Region) (60 minutes)

#### 13.1 Install NATS

```bash
# Install NATS server
brew install nats-server

# Start NATS with clustering
nats-server --cluster nats://0.0.0.0:6222 --routes nats://nats-2:6222,nats://nats-3:6222
```

#### 13.2 Update Configuration

Update `config/composition/composition.yaml`:

```yaml
event_bus:
  backend: "nats"  # Changed from "redis"
  nats:
    servers:
      - "nats://localhost:4222"
      - "nats://nats-2:4222"
      - "nats://nats-3:4222"
    cluster_id: "chora-cluster"
  persistence:
    enabled: true
    storage: "file"  # NATS file storage
```

**Result**: Multi-region event bus with NATS clustering.

---

### Phase 14: OpenTelemetry Distributed Tracing (60 minutes)

#### 14.1 Install OpenTelemetry

```bash
# Install OpenTelemetry Collector
brew install opentelemetry-collector

# Install Python SDK
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
```

#### 14.2 Configure OpenTelemetry

Update `config/composition/composition.yaml`:

```yaml
monitoring:
  opentelemetry:
    enabled: true
    endpoint: "http://localhost:4318"  # OTLP/HTTP endpoint
    service_name: "chora-composition"
    sample_rate: 1.0  # 100% sampling for dev
```

#### 14.3 Instrument Saga Steps

```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Initialize tracer
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces"))
)
trace.set_tracer_provider(tracer_provider)

tracer = trace.get_tracer(__name__)

# Instrument saga step
async def register_manifest(data: Dict[str, Any]) -> Dict[str, Any]:
    """Register in manifest (instrumented)."""
    with tracer.start_as_current_span("saga.step.register_manifest") as span:
        span.set_attribute("environment_id", data["environment_id"])
        result = await manifest_client.register(data)
        span.set_attribute("manifest_entry_id", result["manifest_entry_id"])
        return result
```

**Result**: End-to-end distributed tracing for saga execution.

---

### Phase 15: Grafana Dashboards (45 minutes)

#### 15.1 Install Grafana

```bash
# Install Grafana
brew install grafana

# Start Grafana
brew services start grafana

# Access Grafana: http://localhost:3000 (admin/admin)
```

#### 15.2 Import Dashboard

Import pre-built dashboard `dashboards/composition.json`:

**Panels**:
- Saga Execution Rate (requests/sec)
- Saga Success Rate (%)
- Saga Duration (p50, p95, p99)
- Circuit Breaker States (closed/open/half-open)
- Event Bus Throughput (events/sec)
- Active Sagas (gauge)

**Result**: Real-time visualization of composition metrics.

---

### Phase 16: High Availability Saga Orchestrator (90 minutes)

#### 16.1 Deploy PostgreSQL Cluster

```bash
# Setup PostgreSQL cluster (3 nodes)
# - Primary: postgres-1 (read/write)
# - Replicas: postgres-2, postgres-3 (read-only)

# Use Patroni for automatic failover
pip install patroni[etcd]

# Configure Patroni (patroni.yml)
patroni patroni.yml
```

#### 16.2 Deploy HA Orchestrator

Deploy 3 orchestrator instances with shared PostgreSQL:

```yaml
# docker-compose.yml
services:
  orchestrator-1:
    image: chora/orchestrator:latest
    environment:
      - SAGA_DB=postgresql://primary:5432/chora_sagas
      - REDIS_URL=redis://redis-cluster:6379

  orchestrator-2:
    image: chora/orchestrator:latest
    environment:
      - SAGA_DB=postgresql://primary:5432/chora_sagas
      - REDIS_URL=redis://redis-cluster:6379

  orchestrator-3:
    image: chora/orchestrator:latest
    environment:
      - SAGA_DB=postgresql://primary:5432/chora_sagas
      - REDIS_URL=redis://redis-cluster:6379
```

#### 16.3 Configure Leader Election

```python
from chora_compose.composition import SagaOrchestrator
from chora_compose.composition.ha import LeaderElection

# Initialize leader election (using etcd)
leader_election = LeaderElection(
    etcd_endpoints=["etcd-1:2379", "etcd-2:2379", "etcd-3:2379"],
    lock_name="saga_orchestrator_leader",
    ttl=30
)

# Initialize orchestrator with HA
orchestrator = SagaOrchestrator(
    persistence_backend="postgresql",
    leader_election=leader_election
)

# Only leader processes sagas
if orchestrator.is_leader():
    await orchestrator.start()
```

**Result**: High availability orchestrator with automatic failover.

---

### Phase 17: Validation (30 minutes)

#### Advanced Tier Checklist

- [ ] NATS event bus configured with multi-region support
- [ ] OpenTelemetry distributed tracing enabled
- [ ] Grafana dashboard imported and displaying metrics
- [ ] PostgreSQL HA cluster deployed (3 nodes)
- [ ] HA orchestrator deployed (3 instances)
- [ ] Leader election configured (etcd)
- [ ] Automatic failover tested (kill leader, new leader elected)
- [ ] Distributed traces visible in Jaeger/Tempo
- [ ] Grafana dashboard shows real-time metrics

**Validation Commands**:

```bash
# Test NATS clustering
nats-cli pub test.event "hello world"
nats-cli sub test.event

# Test distributed tracing
curl http://localhost:16686  # Jaeger UI

# Test HA orchestrator failover
docker kill orchestrator-1
# Check: orchestrator-2 or orchestrator-3 becomes leader

# View Grafana dashboard
open http://localhost:3000/dashboards
```

**Expected Results**:
- ✅ Events delivered across NATS cluster
- ✅ Distributed traces show saga execution flow
- ✅ Grafana dashboard displays real-time metrics
- ✅ Orchestrator failover happens in <30 seconds
- ✅ Saga execution continues after failover (no data loss)

---

## Post-Adoption Tasks

### Task 1: Update Documentation

**Update `AGENTS.md`** (project root):

```markdown
## Composition Patterns (SAP-046)

**Status**: ✅ Adopted (Tier: Recommended)

**Quick Reference**:
- Execute saga: `chora-compose saga execute {name} --input '{...}'`
- Check status: `chora-compose saga status {id}`
- Publish event: `chora-compose events publish --type {...}`
- Resolve deps: `chora-compose deps resolve --manifest services/*/manifest.yaml`

**Metrics**:
- Saga success rate: 95%+
- Integration time: <4 hours (75% faster)
- Circuit breaker prevented cascading failures: 90%+
```

---

### Task 2: Train Team

**Recommended Training**:
1. Review [AGENTS.md](AGENTS.md) (quick reference)
2. Review [protocol-spec.md](protocol-spec.md) (complete specification)
3. Hands-on workshop: Implement saga for new workflow
4. Failure injection testing: Test compensation logic

**Training Materials**:
- [AGENTS.md](AGENTS.md) - Quick reference
- [protocol-spec.md](protocol-spec.md) - Technical specification
- [capability-charter.md](capability-charter.md) - Design rationale
- Example sagas: `examples/sagas/`

---

### Task 3: Monitor and Optimize

**Key Metrics to Track**:
- Saga success rate (target: ≥95%)
- Saga duration (target: <10 minutes for deployment)
- Circuit breaker open events (target: <5% of requests)
- Event delivery latency (target: <100ms)
- Compensation success rate (target: 100%)

**Optimization Tips**:
- Parallelize independent saga steps (reduce duration)
- Tune circuit breaker thresholds (reduce false positives)
- Batch event publishing (improve throughput)
- Add caching to reduce service calls

---

### Task 4: Contribute Improvements

**Feedback to SAP-046 Maintainers**:
- Report bugs: GitHub Issues
- Suggest features: [ledger.md](ledger.md) (Improvement Backlog)
- Share lessons learned: Update [ledger.md](ledger.md) (Lessons Learned)
- Contribute code: Pull requests

---

## Troubleshooting

### Issue 1: Saga Stuck in "running" State

**Symptom**: Saga shows "running" for hours, no progress.

**Diagnosis**:
```bash
chora-compose saga status {saga_id}
# Check: current_step, last update time
```

**Root Causes**:
1. Step timeout too long (hanging indefinitely)
2. Step not updating progress
3. Database connection lost

**Fix**:
```bash
# Cancel saga (with compensation)
chora-compose saga cancel {saga_id} --compensate

# Review step timeout configuration
# Reduce timeout in saga_definitions.yaml
```

---

### Issue 2: Compensation Failed

**Symptom**: Saga failed, but compensation also failed (partial rollback).

**Diagnosis**:
```bash
chora-compose saga status {saga_id}
# Check: compensated=false, error_message
```

**Root Causes**:
1. Compensation logic not idempotent (fails on retry)
2. Resource already deleted (not handling NotFoundError)
3. Network timeout during compensation

**Fix**:
```python
# Make compensation idempotent
async def deregister(data):
    """Deregister (idempotent)."""
    try:
        await manifest_client.deregister(data["manifest_entry_id"])
    except NotFoundError:
        # Already deregistered, succeed (idempotent)
        pass
```

---

### Issue 3: Circuit Breaker Always Open

**Symptom**: Circuit breaker never closes, all requests fail.

**Diagnosis**:
```bash
chora-compose circuit-breaker status {service}
# Check: state=open, last_failure_time, will_retry_at
```

**Root Causes**:
1. Service actually down (legitimate open circuit)
2. Failure threshold too low (opens prematurely)
3. Success threshold too high (hard to close)

**Fix**:
```bash
# Manually reset circuit breaker
chora-compose circuit-breaker reset {service} --force-state closed

# Or adjust thresholds in circuit_breakers.yaml
failure_threshold: 10  # Increase tolerance
success_threshold: 2   # Reduce close requirement
```

---

### Issue 4: Event Not Delivered

**Symptom**: Published event never reaches subscriber.

**Diagnosis**:
```bash
# Check event log
chora-compose events log --tail 100 | grep {event_type}

# Check subscriber is running
ps aux | grep "chora-compose events subscribe"
```

**Root Causes**:
1. Subscriber not running
2. Channel mismatch (subscriber listening to wrong channel)
3. Redis/NATS connection lost

**Fix**:
```bash
# Restart subscriber with correct channels
chora-compose events subscribe --channels "environment.lifecycle.*"

# Check Redis/NATS connection
redis-cli ping  # Or: nats-cli pub test.ping hello
```

---

### Issue 5: Circular Dependency Error

**Symptom**: Dependency resolution fails with circular dependency.

**Diagnosis**:
```bash
chora-compose deps validate --manifest services/*/manifest.yaml
# Error: Circular dependency involving: [executor, analyzer]
```

**Root Causes**:
1. Service A depends on B, B depends on A (circular)
2. Transitive circular dependency (A → B → C → A)

**Fix**:
```yaml
# Review manifest.yaml for circular deps
# Remove unnecessary dependencies

# Before (circular):
# executor → analyzer → executor

# After (no circular):
# executor → analyzer
```

---

## FAQ

### Q1: When should I use orchestration vs choreography?

**A**: Use orchestration for multi-step workflows YOU control (environment deployment). Use choreography for cross-cutting concerns (logging, monitoring).

**Example**:
- **Orchestration**: Deploy environment (manifest → containers → gateway)
- **Choreography**: Log deployment event (logging service reacts to event)

---

### Q2: How do I make an operation idempotent?

**A**: Design operations so calling them multiple times has the same effect.

**Patterns**:
1. **Check-then-create**: If resource exists, return existing (don't error)
2. **Set value**: PUT operations are naturally idempotent
3. **Delete**: If resource not found, succeed (already deleted)
4. **Request IDs**: Cache response by request ID, return cached response on retry

---

### Q3: What if compensation fails?

**A**: Compensation failures are logged but don't stop other compensations (best effort). Mark saga as "failed (partially compensated)".

**Mitigation**:
- Make compensations idempotent (safe to retry)
- Add retries to compensation logic
- Implement manual compensation workflow (human intervention)

---

### Q4: How do I tune circuit breaker thresholds?

**A**: Balance between fail-fast (low threshold) and tolerance (high threshold).

**Guidelines**:
- **Critical services**: Lower threshold (3-5 failures), shorter timeout (15-30s)
- **Non-critical services**: Higher threshold (10-15 failures), longer timeout (60s)
- **Transient errors**: Increase threshold, use retry policies

---

### Q5: Can I run sagas in parallel?

**A**: Steps within a saga run sequentially (or based on `depends_on`). To parallelize, create multiple saga instances.

**Example**:
```python
# Run 3 deployments in parallel
saga_instances = await asyncio.gather(
    orchestrator.execute("deploy_environment", {"env_id": "env_1"}),
    orchestrator.execute("deploy_environment", {"env_id": "env_2"}),
    orchestrator.execute("deploy_environment", {"env_id": "env_3"})
)
```

---

## Additional Resources

**Documentation**:
- [capability-charter.md](capability-charter.md) - Problem statement, ROI analysis
- [protocol-spec.md](protocol-spec.md) - Complete technical specification
- [AGENTS.md](AGENTS.md) - Quick reference for AI agents
- [ledger.md](ledger.md) - Adoption tracking, metrics, feedback

**Related SAPs**:
- SAP-042 (InterfaceDesign) - Capability interface patterns
- SAP-044 (Registry) - Service discovery and health
- SAP-045 (Bootstrap) - Phased deployment orchestration
- SAP-010 (A-MEM) - Event-sourced memory
- SAP-015 (Beads) - Task tracking

**Standards**:
- CloudEvents 1.0: https://cloudevents.io/
- W3C Trace Context: https://www.w3.org/TR/trace-context/
- Saga Pattern: https://microservices.io/patterns/data/saga.html

---

**Document Version**: 1.0.0
**Status**: Pilot
**Last Updated**: 2025-11-12
