# SAP-044: Registry (Service Discovery and Manifest)
## Adoption Blueprint

**Version**: 1.0.0
**Status**: Pilot
**Last Updated**: 2025-11-12

---

## Overview

This blueprint provides a step-by-step guide for adopting SAP-044 (Registry) in your Chora environment. It covers three adoption tiers with progressive complexity and implementation timelines.

**Adoption Tiers**:
- **Essential** (1-2 weeks): Core registry with single-node deployment, basic service discovery
- **Recommended** (2-4 weeks): Production-ready with etcd, dependency validation, metrics
- **Advanced** (4-8 weeks): High availability, monitoring, security, performance optimization

**Prerequisites**:
- Python 3.9+ environment
- Docker (for containerized deployment)
- Basic understanding of REST APIs and microservices

---

## Adoption Tier Selection

### Essential Tier (Recommended Starting Point)

**Choose if**:
- First-time Registry adoption
- Development or staging environment
- Team size: 1-5 developers
- Service count: 3-10 services
- Uptime requirement: 95% (dev/test workloads)

**Delivers**:
- Working service registry with SQLite backend
- Service registration, heartbeat, discovery
- REST API for basic queries
- Single-node deployment (Docker Compose)

**Estimated Effort**: 40-80 hours (1-2 weeks)

---

### Recommended Tier (Production Baseline)

**Choose if**:
- Production environment
- Team size: 5-20 developers
- Service count: 10-50 services
- Uptime requirement: 99% (business-critical)
- Need for metrics and monitoring

**Delivers**:
- Essential tier +
- etcd backend for strong consistency
- Dependency validation
- Prometheus metrics
- CLI tooling
- Client library (Python)

**Estimated Effort**: 80-160 hours (2-4 weeks)

---

### Advanced Tier (Enterprise Scale)

**Choose if**:
- Large-scale production environment
- Team size: 20+ developers
- Service count: 50+ services
- Uptime requirement: 99.9% (mission-critical)
- Multi-region or high availability needed

**Delivers**:
- Recommended tier +
- High availability (3-node Raft cluster)
- Authentication (bearer token or mTLS)
- Advanced monitoring and alerting
- Performance optimization
- Security hardening

**Estimated Effort**: 160-320 hours (4-8 weeks)

---

## Essential Tier: Step-by-Step Guide

### Phase 1: Setup Development Environment (Day 1-2)

**Objective**: Prepare development environment with necessary tools and dependencies.

#### Step 1.1: Install Prerequisites

```bash
# Python 3.9+
python3 --version  # Should be >= 3.9

# Docker & Docker Compose
docker --version
docker-compose --version

# Poetry (for Python dependency management)
curl -sSL https://install.python-poetry.org | python3 -
```

#### Step 1.2: Clone Chora-Base (if using as template)

```bash
git clone https://github.com/chora-base/chora-base.git
cd chora-base
```

#### Step 1.3: Create Project Structure

```bash
mkdir -p chora-manifest
cd chora-manifest

# Create directory structure
mkdir -p manifest/{api,core,storage,models,config}
mkdir -p tests/{unit,integration}
mkdir -p client
mkdir -p cli
mkdir -p docs
```

#### Step 1.4: Initialize Poetry Project

```bash
poetry init --name chora-manifest --python "^3.9"

# Add dependencies
poetry add fastapi uvicorn pydantic aiosqlite
poetry add --group dev pytest pytest-asyncio httpx black ruff

# Install
poetry install
```

**Quality Gate 1.1**: Verify environment

```bash
# Check Python version
python3 --version

# Check Poetry
poetry --version

# Check Docker
docker run hello-world
```

**Expected Output**: All commands succeed without errors.

---

### Phase 2: Implement Core Registry (Day 3-5)

**Objective**: Implement core registry logic with in-memory/SQLite storage.

#### Step 2.1: Define Data Models

Create `manifest/models.py`:

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
    description: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    environment: Optional[str] = None
    custom: Dict[str, str] = field(default_factory=dict)

@dataclass
class ServiceRecord:
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
            import secrets
            self.id = f"{self.name}-{secrets.token_hex(4)}"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "id": self.id,
            "version": self.version,
            "interfaces": self.interfaces,
            "metadata": {
                "description": self.metadata.description,
                "dependencies": self.metadata.dependencies,
                "tags": self.metadata.tags,
                "environment": self.metadata.environment,
                **self.metadata.custom
            },
            "status": self.status.value,
            "last_heartbeat": self.last_heartbeat.isoformat() + "Z",
            "registered_at": self.registered_at.isoformat() + "Z"
        }
```

#### Step 2.2: Implement Storage Backend

Create `manifest/storage.py`:

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from .models import ServiceRecord
import asyncio
import aiosqlite
import json

class StorageBackend(ABC):
    @abstractmethod
    async def put(self, service: ServiceRecord, ttl: int):
        """Store service with TTL."""
        pass

    @abstractmethod
    async def get(self, key: str) -> Optional[ServiceRecord]:
        """Get service by key."""
        pass

    @abstractmethod
    async def delete(self, key: str):
        """Delete service."""
        pass

    @abstractmethod
    async def list(self, prefix: Optional[str] = None) -> List[ServiceRecord]:
        """List all services."""
        pass

class SQLiteStorage(StorageBackend):
    """SQLite-based storage for development."""

    def __init__(self, db_path: str = "manifest.db"):
        self.db_path = db_path
        self.db = None

    async def initialize(self):
        """Create table if not exists."""
        self.db = await aiosqlite.connect(self.db_path)
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS services (
                key TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                ttl_expires_at REAL NOT NULL
            )
        """)
        await self.db.commit()

    async def put(self, service: ServiceRecord, ttl: int):
        key = f"{service.name}/{service.id}"
        data = json.dumps(service.to_dict())
        import time
        expires_at = time.time() + ttl

        await self.db.execute(
            "INSERT OR REPLACE INTO services (key, data, ttl_expires_at) VALUES (?, ?, ?)",
            (key, data, expires_at)
        )
        await self.db.commit()

    async def get(self, key: str) -> Optional[ServiceRecord]:
        import time
        now = time.time()

        cursor = await self.db.execute(
            "SELECT data FROM services WHERE key = ? AND ttl_expires_at > ?",
            (key, now)
        )
        row = await cursor.fetchone()

        if not row:
            return None

        data = json.loads(row[0])
        return ServiceRecord(**data)

    async def delete(self, key: str):
        await self.db.execute("DELETE FROM services WHERE key = ?", (key,))
        await self.db.commit()

    async def list(self, prefix: Optional[str] = None) -> List[ServiceRecord]:
        import time
        now = time.time()

        if prefix:
            cursor = await self.db.execute(
                "SELECT data FROM services WHERE key LIKE ? AND ttl_expires_at > ?",
                (f"{prefix}%", now)
            )
        else:
            cursor = await self.db.execute(
                "SELECT data FROM services WHERE ttl_expires_at > ?",
                (now,)
            )

        rows = await cursor.fetchall()
        services = []
        for row in rows:
            data = json.loads(row[0])
            services.append(ServiceRecord(**data))

        return services

    async def cleanup_expired(self):
        """Remove expired services."""
        import time
        now = time.time()
        await self.db.execute("DELETE FROM services WHERE ttl_expires_at <= ?", (now,))
        await self.db.commit()
```

#### Step 2.3: Implement Registry Core

Create `manifest/core.py`:

```python
from typing import List, Optional
from .models import ServiceRecord, ServiceStatus
from .storage import StorageBackend
import asyncio
import logging

logger = logging.getLogger(__name__)

class RegistryCore:
    def __init__(self, storage: StorageBackend):
        self.storage = storage
        self.health_monitor_task = None

    async def initialize(self):
        """Initialize registry."""
        await self.storage.initialize()
        # Start health monitor
        self.health_monitor_task = asyncio.create_task(self._health_monitor_loop())

    async def register_service(self, service: ServiceRecord) -> str:
        """Register service, returns instance ID."""
        if not service.id:
            import secrets
            service.id = f"{service.name}-{secrets.token_hex(4)}"

        await self.storage.put(service, ttl=30)
        logger.info(f"Registered service: {service.name} ({service.id})")
        return service.id

    async def heartbeat(self, service_name: str, instance_id: str):
        """Update heartbeat timestamp."""
        key = f"{service_name}/{instance_id}"
        service = await self.storage.get(key)

        if not service:
            raise ValueError(f"Service {key} not found")

        from datetime import datetime
        service.last_heartbeat = datetime.utcnow()
        service.status = ServiceStatus.UP
        await self.storage.put(service, ttl=30)

    async def get_service(self, name: str) -> Optional[List[ServiceRecord]]:
        """Get service(s) by name."""
        services = await self.storage.list(prefix=name)
        return services if services else None

    async def list_services(self, status: Optional[str] = None,
                           tag: Optional[str] = None) -> List[ServiceRecord]:
        """List all services with optional filters."""
        services = await self.storage.list()

        if status:
            services = [s for s in services if s.status == status]

        if tag:
            services = [s for s in services if tag in s.metadata.tags]

        return services

    async def deregister_service(self, service_name: str, instance_id: str):
        """Deregister service."""
        key = f"{service_name}/{instance_id}"
        await self.storage.delete(key)
        logger.info(f"Deregistered service: {service_name} ({instance_id})")

    async def _health_monitor_loop(self):
        """Background task to clean up expired services."""
        while True:
            await asyncio.sleep(5)
            await self.storage.cleanup_expired()
```

**Quality Gate 2.1**: Unit tests for core logic

```python
# tests/unit/test_core.py
import pytest
from manifest.core import RegistryCore
from manifest.storage import SQLiteStorage
from manifest.models import ServiceRecord

@pytest.mark.asyncio
async def test_register_service():
    storage = SQLiteStorage(":memory:")
    registry = RegistryCore(storage)
    await registry.initialize()

    service = ServiceRecord(
        name="test-service",
        version="1.0.0",
        interfaces={"REST": "http://localhost:9000"}
    )

    instance_id = await registry.register_service(service)
    assert instance_id.startswith("test-service-")

    # Verify retrieval
    services = await registry.get_service("test-service")
    assert services is not None
    assert len(services) == 1
    assert services[0].name == "test-service"
```

Run tests:

```bash
poetry run pytest tests/unit/
```

**Expected**: All tests pass.

---

### Phase 3: Implement REST API (Day 6-8)

**Objective**: Expose registry via FastAPI REST endpoints.

#### Step 3.1: Create API Routes

Create `manifest/api.py`:

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict
from .core import RegistryCore
from .models import ServiceRecord, ServiceMetadata

app = FastAPI(title="Chora Manifest Registry", version="1.0.0")

# Global registry instance (initialized at startup)
registry: Optional[RegistryCore] = None

class ServiceCreate(BaseModel):
    name: str
    version: str
    interfaces: Dict[str, str]
    metadata: Optional[Dict] = None

class ServiceRegistered(BaseModel):
    id: str
    name: str
    version: str
    status: str
    registered_at: str
    heartbeat_interval: int = 10
    heartbeat_timeout: int = 30

@app.on_event("startup")
async def startup():
    global registry
    from .storage import SQLiteStorage
    storage = SQLiteStorage("manifest.db")
    registry = RegistryCore(storage)
    await registry.initialize()

@app.post("/v1/services", status_code=status.HTTP_201_CREATED, response_model=ServiceRegistered)
async def register_service(service_create: ServiceCreate):
    """Register a new service."""
    metadata_dict = service_create.metadata or {}
    metadata = ServiceMetadata(
        description=metadata_dict.get("description"),
        dependencies=metadata_dict.get("dependencies", []),
        tags=metadata_dict.get("tags", []),
        environment=metadata_dict.get("environment")
    )

    service = ServiceRecord(
        name=service_create.name,
        version=service_create.version,
        interfaces=service_create.interfaces,
        metadata=metadata
    )

    instance_id = await registry.register_service(service)

    return ServiceRegistered(
        id=instance_id,
        name=service.name,
        version=service.version,
        status=service.status.value,
        registered_at=service.registered_at.isoformat() + "Z"
    )

@app.put("/v1/services/{name}/{id}/heartbeat", status_code=status.HTTP_204_NO_CONTENT)
async def heartbeat(name: str, id: str):
    """Send heartbeat to keep service alive."""
    try:
        await registry.heartbeat(name, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/v1/services/{name}/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deregister_service(name: str, id: str):
    """Deregister a service."""
    await registry.deregister_service(name, id)

@app.get("/v1/services/{name}")
async def get_service(name: str):
    """Get service by name."""
    services = await registry.get_service(name)
    if not services:
        raise HTTPException(status_code=404, detail=f"Service '{name}' not found")

    # Return single service if only one instance, otherwise list
    if len(services) == 1:
        return services[0].to_dict()
    return [s.to_dict() for s in services]

@app.get("/v1/services")
async def list_services(status: Optional[str] = None, tag: Optional[str] = None):
    """List all services."""
    services = await registry.list_services(status=status, tag=tag)
    return [s.to_dict() for s in services]

@app.get("/v1/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services_registered": len(await registry.list_services())
    }
```

#### Step 3.2: Run Development Server

Create `manifest/__main__.py`:

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run("manifest.api:app", host="0.0.0.0", port=8500, reload=True)
```

Start server:

```bash
poetry run python -m manifest
```

**Quality Gate 3.1**: API integration tests

```python
# tests/integration/test_api.py
import pytest
import httpx

@pytest.mark.asyncio
async def test_service_lifecycle():
    async with httpx.AsyncClient(base_url="http://localhost:8500") as client:
        # Register
        resp = await client.post("/v1/services", json={
            "name": "test-service",
            "version": "1.0.0",
            "interfaces": {"REST": "http://localhost:9999"}
        })
        assert resp.status_code == 201
        instance_id = resp.json()["id"]

        # Heartbeat
        resp = await client.put(f"/v1/services/test-service/{instance_id}/heartbeat")
        assert resp.status_code == 204

        # Get
        resp = await client.get("/v1/services/test-service")
        assert resp.status_code == 200
        assert resp.json()["status"] == "up"

        # Deregister
        resp = await client.delete(f"/v1/services/test-service/{instance_id}")
        assert resp.status_code == 204

        # Verify gone
        resp = await client.get("/v1/services/test-service")
        assert resp.status_code == 404
```

Run integration tests:

```bash
# Start server in background
poetry run python -m manifest &
sleep 2

# Run tests
poetry run pytest tests/integration/

# Stop server
pkill -f "python -m manifest"
```

**Expected**: All tests pass.

---

### Phase 4: Create Client Library (Day 9-10)

**Objective**: Provide Python client library for easy integration.

#### Step 4.1: Implement Client

Create `client/manifest_client.py`:

```python
import requests
from typing import Dict, List, Optional

class ManifestError(Exception):
    """Base exception for Manifest client errors."""
    pass

class ServiceNotFoundError(ManifestError):
    """Service not found in registry."""
    pass

class ManifestClient:
    """Python client for Chora Manifest registry."""

    def __init__(self, manifest_url: str, auth_token: Optional[str] = None, timeout: float = 5.0):
        self.base_url = manifest_url.rstrip('/')
        self.timeout = timeout
        self.headers = {}
        if auth_token:
            self.headers["Authorization"] = f"Bearer {auth_token}"

    def register(self, name: str, version: str, interfaces: Dict[str, str],
                 metadata: Optional[Dict] = None) -> str:
        """Register service, returns instance ID."""
        payload = {
            "name": name,
            "version": version,
            "interfaces": interfaces,
            "metadata": metadata or {}
        }

        resp = requests.post(
            f"{self.base_url}/v1/services",
            json=payload,
            headers=self.headers,
            timeout=self.timeout
        )

        if resp.status_code != 201:
            raise ManifestError(f"Registration failed: {resp.status_code} {resp.text}")

        return resp.json()["id"]

    def heartbeat(self, name: str, instance_id: str):
        """Send heartbeat to keep service alive."""
        resp = requests.put(
            f"{self.base_url}/v1/services/{name}/{instance_id}/heartbeat",
            headers=self.headers,
            timeout=self.timeout
        )

        if resp.status_code == 404:
            raise ServiceNotFoundError(f"Service '{name}/{instance_id}' not found")
        elif resp.status_code not in (200, 204):
            raise ManifestError(f"Heartbeat failed: {resp.status_code} {resp.text}")

    def deregister(self, name: str, instance_id: str):
        """Deregister service."""
        resp = requests.delete(
            f"{self.base_url}/v1/services/{name}/{instance_id}",
            headers=self.headers,
            timeout=self.timeout
        )

        if resp.status_code not in (200, 204, 404):
            raise ManifestError(f"Deregistration failed: {resp.status_code} {resp.text}")

    def get_service(self, name: str) -> Dict:
        """Get service by name."""
        resp = requests.get(
            f"{self.base_url}/v1/services/{name}",
            headers=self.headers,
            timeout=self.timeout
        )

        if resp.status_code == 404:
            raise ServiceNotFoundError(f"Service '{name}' not found")
        elif resp.status_code != 200:
            raise ManifestError(f"Get service failed: {resp.status_code} {resp.text}")

        return resp.json()

    def list_services(self, status: Optional[str] = None, tag: Optional[str] = None) -> List[Dict]:
        """List all services with optional filters."""
        params = {}
        if status:
            params["status"] = status
        if tag:
            params["tag"] = tag

        resp = requests.get(
            f"{self.base_url}/v1/services",
            params=params,
            headers=self.headers,
            timeout=self.timeout
        )

        if resp.status_code != 200:
            raise ManifestError(f"List services failed: {resp.status_code} {resp.text}")

        return resp.json()
```

**Quality Gate 4.1**: Client library tests

```python
# tests/unit/test_client.py
import pytest
from client.manifest_client import ManifestClient, ServiceNotFoundError

def test_client_initialization():
    client = ManifestClient("http://localhost:8500")
    assert client.base_url == "http://localhost:8500"

# Integration test with live server
@pytest.mark.integration
def test_client_lifecycle():
    client = ManifestClient("http://localhost:8500")

    # Register
    instance_id = client.register(
        name="client-test",
        version="1.0.0",
        interfaces={"REST": "http://localhost:9999"}
    )
    assert instance_id.startswith("client-test-")

    # Heartbeat
    client.heartbeat("client-test", instance_id)

    # Get
    service = client.get_service("client-test")
    assert service["name"] == "client-test"
    assert service["status"] == "up"

    # Deregister
    client.deregister("client-test", instance_id)

    # Verify not found
    with pytest.raises(ServiceNotFoundError):
        client.get_service("client-test")
```

---

### Phase 5: Deployment and Validation (Day 11-12)

**Objective**: Deploy Manifest service and validate with real capability servers.

#### Step 5.1: Create Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY manifest ./manifest
COPY client ./client

# Install dependencies
RUN poetry install --no-dev

# Expose port
EXPOSE 8500

# Run server
CMD ["poetry", "run", "python", "-m", "manifest"]
```

#### Step 5.2: Create Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  manifest:
    build: .
    ports:
      - "8500:8500"
    volumes:
      - manifest-data:/app/data
    environment:
      - MANIFEST_DB_PATH=/app/data/manifest.db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8500/v1/health"]
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  manifest-data:
```

#### Step 5.3: Deploy

```bash
# Build and start
docker-compose up -d

# Check health
curl http://localhost:8500/v1/health

# View logs
docker-compose logs -f manifest
```

#### Step 5.4: Integrate Example Service

Create `example_service.py`:

```python
import time
from threading import Thread
from client.manifest_client import ManifestClient

# Initialize client
client = ManifestClient("http://localhost:8500")

# Register
instance_id = client.register(
    name="example-service",
    version="1.0.0",
    interfaces={"REST": "http://localhost:9000"},
    metadata={"description": "Example service", "tags": ["demo"]}
)
print(f"Registered with ID: {instance_id}")

# Heartbeat loop
def heartbeat_loop():
    while True:
        try:
            client.heartbeat("example-service", instance_id)
            print("Heartbeat sent")
        except Exception as e:
            print(f"Heartbeat failed: {e}")
        time.sleep(10)

heartbeat_thread = Thread(target=heartbeat_loop, daemon=True)
heartbeat_thread.start()

# Keep alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    client.deregister("example-service", instance_id)
    print("Deregistered")
```

Run example:

```bash
python example_service.py
```

**Quality Gate 5.1**: End-to-end validation

```bash
# 1. Check example service registered
curl http://localhost:8500/v1/services/example-service | jq

# Expected: Service with status "up"

# 2. Wait 40 seconds (miss heartbeats)
sleep 40

# 3. Check service expired
curl http://localhost:8500/v1/services/example-service

# Expected: 404 Not Found (service removed due to TTL expiration)
```

**Expected**: Example service registers, heartbeats, and is automatically removed after missing heartbeats.

---

### Essential Tier Summary

**Completion Checklist**:

- [x] Development environment set up
- [x] Core registry logic implemented (models, storage, core)
- [x] REST API exposed via FastAPI
- [x] Python client library created
- [x] Docker deployment configured
- [x] Integration with example service validated
- [x] Unit tests passing (>80% coverage)
- [x] Integration tests passing

**Deliverables**:
- Working Manifest service (Docker container)
- SQLite-based registry storage
- REST API with 7 endpoints (register, heartbeat, deregister, get, list, health, metrics placeholder)
- Python client library
- Example service integration

**Next Steps**:
- Move to Recommended Tier for production readiness (etcd, metrics, CLI)
- OR use Essential tier for development and integrate with more capability servers

---

## Recommended Tier: Step-by-Step Guide

### Phase 6: Replace SQLite with etcd (Day 13-16)

**Objective**: Add strong consistency and HA preparation with etcd backend.

#### Step 6.1: Add etcd to Docker Compose

Update `docker-compose.yml`:

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
    ports:
      - "8500:8500"
    environment:
      - MANIFEST_STORAGE_BACKEND=etcd
      - MANIFEST_ETCD_HOST=etcd
      - MANIFEST_ETCD_PORT=2379
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

#### Step 6.2: Implement etcd Storage Backend

```python
# manifest/storage.py (add EtcdStorage class)
import etcd3
from .models import ServiceRecord
import json

class EtcdStorage(StorageBackend):
    """etcd-based storage for production."""

    def __init__(self, host: str = "localhost", port: int = 2379):
        self.client = etcd3.client(host=host, port=port)
        self.prefix = "/chora/services"

    async def put(self, service: ServiceRecord, ttl: int):
        key = f"{self.prefix}/{service.name}/{service.id}"
        value = json.dumps(service.to_dict())

        # Create lease
        lease = self.client.lease(ttl)

        # Put with lease
        self.client.put(key, value, lease=lease)

    async def get(self, key: str) -> Optional[ServiceRecord]:
        full_key = f"{self.prefix}/{key}"
        value, metadata = self.client.get(full_key)

        if not value:
            return None

        data = json.loads(value.decode('utf-8'))
        return ServiceRecord(**data)

    async def list(self, prefix: Optional[str] = None) -> List[ServiceRecord]:
        search_prefix = f"{self.prefix}/{prefix}" if prefix else self.prefix

        services = []
        for value, metadata in self.client.get_prefix(search_prefix):
            data = json.loads(value.decode('utf-8'))
            services.append(ServiceRecord(**data))

        return services

    async def delete(self, key: str):
        full_key = f"{self.prefix}/{key}"
        self.client.delete(full_key)
```

**Quality Gate 6.1**: etcd integration tests

```bash
# Start etcd + manifest
docker-compose up -d

# Run integration tests
poetry run pytest tests/integration/ -v

# Expected: All tests pass with etcd backend
```

---

### Phase 7: Add Prometheus Metrics (Day 17-19)

**Objective**: Instrument Manifest with metrics for monitoring.

#### Step 7.1: Add Metrics Endpoint

```python
# manifest/api.py (add metrics)
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

# Define metrics
http_requests_total = Counter(
    'manifest_http_requests_total',
    'Total HTTP requests',
    ['endpoint', 'method', 'status']
)

http_request_duration_seconds = Histogram(
    'manifest_http_request_duration_seconds',
    'HTTP request latency',
    ['endpoint', 'method']
)

services_registered = Gauge(
    'manifest_services_registered',
    'Number of registered services',
    ['status']
)

@app.get("/v1/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    # Update gauges
    all_services = await registry.list_services()
    services_registered.labels(status="up").set(len([s for s in all_services if s.status == "up"]))
    services_registered.labels(status="unhealthy").set(len([s for s in all_services if s.status == "unhealthy"]))

    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Add middleware to track metrics
@app.middleware("http")
async def track_metrics(request, call_next):
    import time
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    endpoint = request.url.path
    method = request.method
    status = response.status_code

    http_requests_total.labels(endpoint=endpoint, method=method, status=status).inc()
    http_request_duration_seconds.labels(endpoint=endpoint, method=method).observe(duration)

    return response
```

#### Step 7.2: Configure Prometheus

Create `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'manifest'
    static_configs:
      - targets: ['manifest:8500']
    metrics_path: '/v1/metrics'
```

Add to `docker-compose.yml`:

```yaml
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  prometheus-data:
  grafana-data:
```

**Quality Gate 7.1**: Verify metrics

```bash
# Check metrics endpoint
curl http://localhost:8500/v1/metrics

# Check Prometheus UI
open http://localhost:9090

# Check Grafana
open http://localhost:3000  # admin/admin
```

---

### Phase 8: Create CLI Tool (Day 20-22)

**Objective**: Provide CLI for operators to interact with Manifest.

#### Step 8.1: Implement CLI

Create `cli/manifest_cli.py`:

```python
import click
import json
from client.manifest_client import ManifestClient

@click.group()
@click.option('--url', default='http://localhost:8500', envvar='MANIFEST_URL', help='Manifest URL')
@click.pass_context
def cli(ctx, url):
    """Chora Manifest CLI."""
    ctx.obj = ManifestClient(url)

@cli.command()
@click.pass_obj
def list(client):
    """List all services."""
    services = client.list_services()
    for svc in services:
        click.echo(f"{svc['name']} v{svc['version']} - {svc['status']} - {svc['interfaces'].get('REST', 'N/A')}")

@cli.command()
@click.argument('name')
@click.pass_obj
def get(client, name):
    """Get service by name."""
    try:
        service = client.get_service(name)
        click.echo(json.dumps(service, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@cli.command()
@click.option('--status', help='Filter by status')
@click.option('--tag', help='Filter by tag')
@click.pass_obj
def query(client, status, tag):
    """Query services with filters."""
    services = client.list_services(status=status, tag=tag)
    click.echo(f"Found {len(services)} services:")
    for svc in services:
        click.echo(f"  {svc['name']} ({svc['status']})")

if __name__ == '__main__':
    cli()
```

Add to `pyproject.toml`:

```toml
[tool.poetry.scripts]
manifest = "cli.manifest_cli:cli"
```

**Quality Gate 8.1**: Test CLI

```bash
# Install CLI
poetry install

# List services
manifest list

# Get specific service
manifest get orchestrator

# Query
manifest query --status=up --tag=core
```

---

### Recommended Tier Summary

**Completion Checklist**:

- [x] Essential tier completed
- [x] etcd backend implemented and tested
- [x] Prometheus metrics instrumented
- [x] CLI tool created
- [x] Monitoring stack (Prometheus + Grafana) deployed
- [x] Integration tests updated for etcd

**Deliverables**:
- etcd-backed registry (strong consistency)
- Prometheus metrics endpoint
- CLI tool for operators
- Monitoring dashboards (Grafana)

**Next Steps**:
- Move to Advanced Tier for HA and security
- OR deploy to production with current setup

---

## Advanced Tier: Step-by-Step Guide

### Phase 9: High Availability (Day 23-28)

**Objective**: Deploy 3-node Manifest + etcd cluster for 99.9% uptime.

_(Detailed steps omitted for brevity - includes etcd cluster setup, load balancing, failure testing)_

### Phase 10: Security Hardening (Day 29-32)

**Objective**: Add authentication, authorization, TLS encryption.

_(Detailed steps omitted for brevity - includes mTLS, RBAC, secret management)_

### Phase 11: Performance Optimization (Day 33-35)

**Objective**: Optimize for high load (1000+ services, 10k qps).

_(Detailed steps omitted for brevity - includes connection pooling, caching, profiling)_

---

## Rollback Plan

If adoption encounters issues, follow this rollback procedure:

### Rollback from Essential to No Registry

1. **Gracefully Deregister All Services**:
   ```bash
   # For each service
   manifest list | xargs -I {} manifest get {} | jq -r '.id' | xargs -I {} curl -X DELETE http://localhost:8500/v1/services/{}/{id}
   ```

2. **Stop Manifest Service**:
   ```bash
   docker-compose down
   ```

3. **Revert Services to Static Configuration**:
   - Update environment variables with hardcoded addresses
   - Remove Manifest client library calls
   - Restart services

**Data Loss**: Service registration data lost. No impact on service functionality if reverted to static config.

---

## Success Criteria and Validation

### Essential Tier Validation

- [ ] Manifest service running and healthy (`/v1/health` returns 200)
- [ ] 3+ services registered successfully
- [ ] Heartbeats functioning (services show `status: "up"`)
- [ ] Discovery working (clients can query and find services)
- [ ] Services automatically removed after 30s without heartbeat
- [ ] Integration tests passing (>95% pass rate)

### Recommended Tier Validation

- [ ] Essential tier validation passing
- [ ] etcd backend operational (data persists across Manifest restarts)
- [ ] Metrics endpoint returning data
- [ ] Prometheus scraping metrics successfully
- [ ] CLI tool functional
- [ ] Load test: 100 services, 1000 qps for 10 minutes without errors

### Advanced Tier Validation

- [ ] Recommended tier validation passing
- [ ] HA cluster survives 1-node failure with <5s downtime
- [ ] Authentication working (unauthorized requests rejected)
- [ ] Load test: 1000 services, 10k qps for 1 hour
- [ ] Chaos engineering tests passed (network partitions, node failures)

---

## Support and Resources

- **Documentation**: See [protocol-spec.md](./protocol-spec.md) for API details
- **Troubleshooting**: See [AGENTS.md](./AGENTS.md) for common issues
- **Community**: chora-base GitHub Discussions
- **Commercial Support**: Contact chora-base enterprise team

---

## Changelog

### Version 1.0.0 (2025-11-12)

- Initial adoption blueprint for SAP-044
- Three-tier adoption path (Essential, Recommended, Advanced)
- Step-by-step guides for Essential and Recommended tiers
- Quality gates and validation checklists
- Rollback procedures
- Success criteria definitions
