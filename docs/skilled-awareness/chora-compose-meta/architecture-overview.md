# SAP-018: chora-compose Meta - Architecture Overview

**SAP ID**: SAP-018
**Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active

---

## Overview

This document provides a comprehensive architectural overview of chora-compose, a Docker Compose-based orchestration system for AI agent development environments. It covers system architecture, container orchestration patterns, service dependencies, volume management strategies, network topology, health monitoring, and scaling approaches.

**Audience**: Architects, platform engineers, senior developers
**Prerequisites**: Docker/Docker Compose experience, distributed systems basics
**Related**: [SAP-017](../chora-compose-integration/) for integration patterns

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     chora-compose System                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   AI Agent   │  │  MCP Server  │  │   Workflow   │      │
│  │  (Python)    │  │  (FastMCP)   │  │  (n8n/etc)   │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
│                    ┌───────▼───────┐                         │
│                    │  App Network  │                         │
│                    └───────┬───────┘                         │
│                            │                                 │
│         ┌──────────────────┼──────────────────┐              │
│         │                  │                  │              │
│  ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐       │
│  │  PostgreSQL │   │    Redis    │   │  Monitoring │       │
│  │  (Storage)  │   │   (Cache)   │   │ (Prometheus)│       │
│  └─────────────┘   └─────────────┘   └─────────────┘       │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                     Docker Engine                             │
└─────────────────────────────────────────────────────────────┘
         │                                        │
┌────────▼────────┐                      ┌───────▼────────┐
│   Host Volume   │                      │  Named Volume  │
│  (Source Code)  │                      │  (Databases)   │
└─────────────────┘                      └────────────────┘
```

### Component Layers

**Layer 1: Application Services**
- AI agents (Python applications)
- MCP servers (Model Context Protocol servers)
- Workflow automation (n8n, custom workflows)
- Web services (APIs, dashboards)

**Layer 2: Middleware Services**
- Message queues (RabbitMQ, Redis)
- Caching layers (Redis, Memcached)
- API gateways (nginx, Traefik)
- Service mesh (optional - Istio, Linkerd)

**Layer 3: Data Services**
- Relational databases (PostgreSQL, MySQL)
- NoSQL databases (MongoDB, Redis)
- Search engines (Elasticsearch, Meilisearch)
- Object storage (MinIO, S3-compatible)

**Layer 4: Infrastructure Services**
- Monitoring (Prometheus, Grafana)
- Logging (Loki, ELK stack)
- Tracing (Jaeger, Zipkin)
- Service discovery (Consul, etcd)

---

## Container Orchestration

### Service Lifecycle Management

**Startup Sequence**:
```yaml
# docker-compose.yml dependency graph
services:
  postgres:
    # No dependencies - starts first
    healthcheck:
      test: ["CMD", "pg_isready"]

  redis:
    # No dependencies - starts first
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]

  app:
    depends_on:
      postgres:
        condition: service_healthy  # Waits for postgres health check
      redis:
        condition: service_healthy  # Waits for redis health check
    # Starts after postgres and redis are healthy
```

**Dependency Resolution Algorithm**:
1. Parse all service definitions
2. Build dependency graph (topological sort)
3. Start services without dependencies
4. Wait for health checks to pass
5. Start dependent services in order
6. Repeat until all services running

**Failure Handling**:
```yaml
services:
  app:
    restart: unless-stopped  # Restart policy
    deploy:
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
```

### Container Resource Management

**CPU Allocation**:
```yaml
services:
  app:
    cpus: '2.0'       # Limit to 2 CPU cores
    cpu_shares: 1024  # Relative weight (default)

  db:
    cpus: '4.0'       # More CPUs for database
    cpu_shares: 2048  # Higher priority
```

**Memory Management**:
```yaml
services:
  app:
    mem_limit: 2g      # Hard limit (OOM kill if exceeded)
    mem_reservation: 1g # Soft limit (guaranteed minimum)

  db:
    mem_limit: 8g
    mem_reservation: 4g
    shm_size: '1gb'    # Shared memory for postgres
```

**I/O Constraints**:
```yaml
services:
  db:
    blkio_config:
      weight: 500  # I/O priority (100-1000)
      device_read_bps:
        - path: /dev/sda
          rate: '50mb'
      device_write_bps:
        - path: /dev/sda
          rate: '10mb'
```

---

## Service Dependencies

### Dependency Patterns

**Pattern 1: Simple Dependency**
```yaml
services:
  app:
    depends_on:
      - db  # Wait for container start only
```
**Use Case**: Non-critical dependencies, fast-starting services

**Pattern 2: Health Check Dependency**
```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy  # Wait for health check
```
**Use Case**: Critical dependencies, services with initialization time

**Pattern 3: Service Readiness Probes**
```yaml
services:
  db:
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 5s       # Check every 5 seconds
      timeout: 3s        # Fail if takes >3s
      retries: 5         # Try 5 times before marking unhealthy
      start_period: 30s  # Grace period on startup
```

**Pattern 4: Init Containers** (via entrypoint scripts)
```yaml
services:
  app:
    entrypoint: /entrypoint.sh
    command: python -m app.server
```

```bash
#!/bin/bash
# entrypoint.sh - Wait for dependencies

set -e

# Wait for postgres
until pg_isready -h db -U postgres; do
  echo "Waiting for postgres..."
  sleep 2
done

# Wait for redis
until redis-cli -h redis ping; do
  echo "Waiting for redis..."
  sleep 2
done

# Run migrations
python -m app.db.migrate

# Start application
exec "$@"
```

### Dependency Graph Visualization

```
┌─────────────────────────────────────────────────────┐
│                  chora-compose Stack                 │
├─────────────────────────────────────────────────────┤
│                                                       │
│   ┌───────────┐                                      │
│   │  Grafana  │◄────────┐                            │
│   └─────┬─────┘         │                            │
│         │               │                            │
│         ▼               │                            │
│   ┌───────────┐         │                            │
│   │Prometheus │         │                            │
│   └─────┬─────┘         │                            │
│         │               │                            │
│         └───────────────┤                            │
│                         │                            │
│   ┌──────────┐    ┌─────▼──────┐    ┌───────────┐   │
│   │   n8n    │◄───│  MCP Server│◄───│ AI Agent  │   │
│   │(Workflow)│    │  (FastMCP) │    │ (Python)  │   │
│   └────┬─────┘    └─────┬──────┘    └─────┬─────┘   │
│        │                │                  │         │
│        │                │                  │         │
│        │          ┌─────┴──────────────────┘         │
│        │          │                                  │
│        │          ▼                                  │
│        │    ┌───────────┐                            │
│        └───►│PostgreSQL │                            │
│             │  (Data)   │                            │
│             └───────────┘                            │
│                   ▲                                  │
│                   │                                  │
│                   │                                  │
│             ┌─────┴─────┐                            │
│             │   Redis   │                            │
│             │  (Cache)  │                            │
│             └───────────┘                            │
│                                                       │
└─────────────────────────────────────────────────────┘

Legend:
  ─►  depends_on relationship
  ◄── uses/connects to
```

---

## Volume Management

### Volume Types and Use Cases

**1. Named Volumes** (Docker-managed)
```yaml
volumes:
  postgres-data:  # Persistent database storage
  redis-data:     # Persistent cache data
  pip-cache:      # Python dependency cache

services:
  db:
    volumes:
      - postgres-data:/var/lib/postgresql/data
```

**Characteristics**:
- ✅ Managed by Docker (easy backup/restore)
- ✅ Persistent across container recreation
- ✅ Good performance (native filesystem)
- ❌ Not directly accessible from host
- ❌ Manual backup process needed

**Use Cases**: Database storage, cache data, build caches

**2. Bind Mounts** (Host filesystem)
```yaml
services:
  app:
    volumes:
      - .:/workspace:delegated  # Source code
      - ./logs:/app/logs        # Log files
      - ./config:/app/config:ro # Configuration (read-only)
```

**Characteristics**:
- ✅ Directly accessible from host
- ✅ Live code reloading (development)
- ✅ Easy editing (IDE, text editor)
- ❌ Performance issues (macOS/Windows)
- ❌ Permission problems (Linux)

**Use Cases**: Source code, configuration, logs, development

**3. tmpfs Mounts** (In-memory)
```yaml
services:
  test-db:
    tmpfs:
      - /var/lib/postgresql/data  # Ephemeral test database
      - /tmp                       # Temporary files
```

**Characteristics**:
- ✅ Extremely fast (RAM-based)
- ✅ Automatic cleanup on container stop
- ✅ No disk I/O overhead
- ❌ Data lost on restart
- ❌ Consumes RAM

**Use Cases**: Test databases, temporary files, caches

### Volume Performance Optimization

**macOS/Windows: Use Delegated Consistency**
```yaml
services:
  app:
    volumes:
      - .:/workspace:delegated  # Host has authority, faster writes
      # vs. :cached (container has authority)
      # vs. :consistent (strict consistency, slowest)
```

**Performance Comparison**:
| Mode | Write Speed | Read Speed | Consistency | Use Case |
|------|-------------|------------|-------------|----------|
| `consistent` | Slow | Slow | Strong | Production (rarely used) |
| `cached` | Fast | Slow | Eventually | Read-heavy workloads |
| `delegated` | Fast | Fast | Eventually | Development (recommended) |

**Linux: Use User Namespaces**
```yaml
services:
  app:
    user: "${UID}:${GID}"  # Match host user
    volumes:
      - .:/workspace  # No permission issues
```

**Exclude Large Directories**
```yaml
services:
  app:
    volumes:
      - .:/workspace:delegated
      - /workspace/node_modules  # Exclude from mount
      - /workspace/.venv         # Exclude Python venv
      - /workspace/__pycache__   # Exclude bytecode cache
```

### Volume Backup and Restore

**Backup Named Volume**:
```bash
# Create backup tarball
docker run --rm \
  -v postgres-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/postgres-backup-$(date +%Y%m%d).tar.gz -C /data .
```

**Restore Named Volume**:
```bash
# Restore from tarball
docker run --rm \
  -v postgres-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/postgres-backup-20251029.tar.gz -C /data
```

**Automated Backup Strategy**:
```yaml
services:
  backup:
    image: alpine:latest
    volumes:
      - postgres-data:/data:ro  # Read-only access
      - ./backups:/backups
    command: |
      sh -c '
        while true; do
          tar czf /backups/backup-$(date +%Y%m%d-%H%M%S).tar.gz -C /data .
          find /backups -name "backup-*.tar.gz" -mtime +7 -delete
          sleep 86400  # Daily backups
        done
      '
```

---

## Network Topology

### Network Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Docker Host                       │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌────────────────────────────────────────────────┐  │
│  │           frontend-network (bridge)            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │  │
│  │  │   App    │  │  nginx   │  │ Dashboard│    │  │
│  │  │  :8000   │  │  :80     │  │  :3000   │    │  │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘    │  │
│  └───────┼─────────────┼─────────────┼──────────┘  │
│          │             │             │              │
│          └─────────────┼─────────────┘              │
│                        │                            │
│  ┌─────────────────────▼──────────────────────────┐ │
│  │           backend-network (bridge)             │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │ │
│  │  │   App    │  │PostgreSQL│  │  Redis   │    │ │
│  │  │          │  │  :5432   │  │  :6379   │    │ │
│  │  └──────────┘  └──────────┘  └──────────┘    │ │
│  └────────────────────────────────────────────────┘ │
│                                                       │
│  Host Ports:                                          │
│    :80 → nginx:80                                     │
│    :8000 → app:8000                                   │
│    :5432 → postgres:5432 (dev only)                   │
│                                                       │
└─────────────────────────────────────────────────────┘
```

### Network Patterns

**Pattern 1: Single Network** (Simple)
```yaml
networks:
  app-network:

services:
  app:
    networks:
      - app-network
  db:
    networks:
      - app-network
```
**Use Case**: Simple applications, trusted services

**Pattern 2: Multi-Network** (Isolation)
```yaml
networks:
  frontend:  # Public-facing services
  backend:   # Internal services only

services:
  nginx:
    networks:
      - frontend

  app:
    networks:
      - frontend  # Accessible to nginx
      - backend   # Accessible to database

  db:
    networks:
      - backend  # Not accessible from frontend
```
**Use Case**: Security boundaries, microservices

**Pattern 3: Internal Network**
```yaml
networks:
  backend:
    internal: true  # No external access

services:
  db:
    networks:
      - backend  # Only accessible via other containers
```
**Use Case**: Databases, sensitive services

### Service Discovery

**By Service Name**:
```python
# Inside app container
DATABASE_URL = "postgresql://user:pass@db:5432/myapp"
REDIS_URL = "redis://redis:6379"
```

**DNS Resolution**:
```bash
# Inside container
dig db
# Returns: db.app-network (internal DNS)

ping db
# PING db (172.18.0.2): 56 data bytes
```

**Network Aliases**:
```yaml
services:
  db:
    networks:
      backend:
        aliases:
          - database
          - postgres-primary
```

```python
# Can use aliases
DATABASE_URL = "postgresql://user:pass@database:5432/myapp"
# Or: postgresql://user:pass@postgres-primary:5432/myapp
```

---

## Health Monitoring

### Health Check Implementation

**HTTP Health Checks**:
```yaml
services:
  api:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

**Python Health Check Endpoint**:
```python
from fastapi import FastAPI, Response, status

app = FastAPI()

@app.get("/health")
async def health_check():
    # Check dependencies
    try:
        # Database connectivity
        await db.execute("SELECT 1")

        # Redis connectivity
        redis_client.ping()

        return {"status": "healthy", "database": "ok", "cache": "ok"}
    except Exception as e:
        return Response(
            content={"status": "unhealthy", "error": str(e)},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
```

**Database Health Checks**:
```yaml
services:
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5

  mysql:
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s

  mongodb:
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
```

### Monitoring Stack Integration

**Prometheus Metrics Exporter**:
```yaml
services:
  app:
    ports:
      - "8000:8000"  # Application
      - "9090:9090"  # Metrics endpoint
    environment:
      - ENABLE_METRICS=true

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9091:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:latest
    volumes:
      - grafana-data:/var/lib/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

**prometheus.yml**:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'app'
    static_configs:
      - targets: ['app:9090']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

---

## Scaling Strategies

### Horizontal Scaling

**Docker Compose Scale** (Development):
```bash
# Scale app service to 3 instances
docker compose up -d --scale app=3

# With load balancer
docker compose up -d --scale app=3 nginx
```

**docker-compose.yml**:
```yaml
services:
  app:
    build: .
    # No container_name - allows multiple instances
    deploy:
      replicas: 3  # Default replica count
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    ports:
      - "80:80"
    depends_on:
      - app
```

**nginx.conf** (Load Balancer):
```nginx
upstream app_backend {
    server app:8000;  # Docker Compose provides round-robin DNS
}

server {
    listen 80;

    location / {
        proxy_pass http://app_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Vertical Scaling

**Resource Limits**:
```yaml
services:
  db:
    image: postgres:15-alpine
    deploy:
      resources:
        limits:
          cpus: '4.0'    # Increase CPU allocation
          memory: 8G     # Increase memory
        reservations:
          cpus: '2.0'
          memory: 4G
    environment:
      # PostgreSQL tuning for 8GB RAM
      - POSTGRES_SHARED_BUFFERS=2GB
      - POSTGRES_EFFECTIVE_CACHE_SIZE=6GB
      - POSTGRES_WORK_MEM=128MB
```

### Migration to Production Orchestration

**From Docker Compose to Kubernetes**:

**Docker Compose** (Development):
```yaml
services:
  app:
    build: .
    replicas: 3
    ports:
      - "8000:8000"
```

**Kubernetes** (Production):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

**Kompose Tool** (Convert Compose → Kubernetes):
```bash
# Install kompose
curl -L https://github.com/kubernetes/kompose/releases/download/v1.30.0/kompose-linux-amd64 -o kompose

# Convert docker-compose.yml to Kubernetes manifests
kompose convert -f docker-compose.yml
```

---

## Related Documentation

**SAP-018 Artifacts**:
- [design-philosophy.md](design-philosophy.md) - Core principles and design decisions
- [integration-patterns.md](integration-patterns.md) - Integration patterns with chora-base
- [capability-charter.md](capability-charter.md) - Comprehensive capabilities
- [adoption-blueprint.md](adoption-blueprint.md) - Meta-level adoption guide

**Related SAPs**:
- [SAP-017: chora-compose Integration](../chora-compose-integration/) - Lightweight integration guide
- [SAP-003: Project Bootstrap](../project-bootstrap/) - chora-base project structure

**External Resources**:
- [chora-compose Repository](https://github.com/liminalcommons/chora-compose) - Source code and templates
- [Docker Compose Specification](https://docs.docker.com/compose/compose-file/) - Official reference
- [Docker Networking](https://docs.docker.com/network/) - Network architecture

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active
