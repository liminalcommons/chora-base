# SAP-018: chora-compose Meta - Integration Patterns

**SAP ID**: SAP-018
**Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active

---

## Overview

This document catalogs integration patterns for chora-compose with chora-base projects, MCP servers, multi-project setups, CI/CD pipelines, development workflows, and production considerations. Each pattern includes implementation examples, trade-offs, and best practices.

**Audience**: Developers, DevOps engineers, architects implementing chora-compose integrations
**Prerequisites**: Familiarity with Docker Compose, chora-base project structure
**Related**: [SAP-017](../chora-compose-integration/) for basic integration steps

---

## chora-base Integration Patterns

### Pattern 1: Minimal Integration

**Use Case**: Add Docker support to existing chora-base project with minimal changes.

**Implementation**:

**docker-compose.yml**:
```yaml
services:
  app:
    build: .
    volumes:
      - .:/workspace:delegated
    environment:
      - PYTHONUNBUFFERED=1
    ports:
      - "8000:8000"
    command: python -m your_module.server
```

**Dockerfile**:
```dockerfile
FROM python:3.11-slim
WORKDIR /workspace
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "your_module.server"]
```

**Benefits**:
- ✅ Minimal file changes (2 new files)
- ✅ Existing project structure unchanged
- ✅ Quick to implement (< 15 min)

**Trade-offs**:
- ❌ No service dependencies
- ❌ No environment configuration
- ❌ Single-service only

**When to Use**: Simple projects, proof-of-concept, learning Docker Compose

---

### Pattern 2: Full Stack Integration

**Use Case**: chora-base project with database, cache, and supporting services.

**Implementation**:

**docker-compose.yml**:
```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - .:/workspace:delegated
      - pip-cache:/root/.cache/pip
    environment:
      - PYTHONUNBUFFERED=1
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      - REDIS_URL=redis://redis:6379
    env_file:
      - .env.local
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app-network
    ports:
      - "8000:8000"
    command: python -m your_module.server

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-myapp}
      POSTGRES_USER: ${POSTGRES_USER:-dev}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-dev}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "${POSTGRES_USER:-dev}"]
      interval: 5s
      timeout: 3s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s

volumes:
  postgres-data:
  redis-data:
  pip-cache:

networks:
  app-network:
```

**Benefits**:
- ✅ Complete development environment
- ✅ Service dependencies managed
- ✅ Production-like architecture

**Trade-offs**:
- ❌ More complex setup
- ❌ More resources required

**When to Use**: Production-like development, team projects, complex applications

---

### Pattern 3: Hybrid Development

**Use Case**: Run Python locally (IDE debugging), services in Docker.

**Implementation**:

**docker-compose.yml** (services only):
```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp_dev
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"  # Exposed for local Python

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    ports:
      - "6379:6379"  # Exposed for local Python

volumes:
  postgres-data:
  redis-data:
```

**Local Python Configuration**:
```bash
# .env.local (for local Python)
DATABASE_URL=postgresql://dev:dev@localhost:5432/myapp_dev
REDIS_URL=redis://localhost:6379
```

**Workflow**:
```bash
# Start services
docker compose up -d

# Run Python locally
python -m your_module.server

# Or use IDE run configuration
```

**Benefits**:
- ✅ Fast iteration (no container restart)
- ✅ IDE debugging (breakpoints, step-through)
- ✅ Direct file access

**Trade-offs**:
- ❌ Less production parity
- ❌ Need to manage local Python environment

**When to Use**: Active development, debugging, performance-sensitive iteration

---

## MCP Server Integration Patterns

### Pattern 4: Single MCP Server

**Use Case**: Deploy one MCP server with chora-compose.

**Implementation**:

**docker-compose.yml**:
```yaml
services:
  mcp-server:
    build: .
    volumes:
      - .:/workspace:delegated
    environment:
      - MCP_SERVER_NAME=my-server
      - MCP_NAMESPACE=myserver
      - DATABASE_URL=postgresql://user:pass@db:5432/mcp_db
    depends_on:
      db:
        condition: service_healthy
    stdin_open: true  # MCP stdio transport
    tty: true
    command: python -m my_mcp_server.server

  db:
    image: postgres:15-alpine
    # ... database config
```

**MCP Client Configuration** (Claude Desktop):
```json
{
  "mcpServers": {
    "my-server": {
      "command": "docker",
      "args": [
        "compose",
        "-f", "/path/to/project/docker-compose.yml",
        "run", "--rm", "mcp-server"
      ]
    }
  }
}
```

**Benefits**:
- ✅ Reproducible MCP server
- ✅ Service dependencies managed
- ✅ Easy testing

**When to Use**: MCP server development, deployment

---

### Pattern 5: Multi-MCP Server Orchestration

**Use Case**: Multiple MCP servers working together.

**Implementation**:

**docker-compose.yml**:
```yaml
services:
  # MCP Server 1: Task Management
  mcp-tasks:
    build: ./servers/tasks
    volumes:
      - ./servers/tasks:/workspace:delegated
    environment:
      - MCP_NAMESPACE=tasks
      - DATABASE_URL=postgresql://user:pass@db:5432/tasks_db
    depends_on:
      - db
    stdin_open: true
    tty: true

  # MCP Server 2: Documentation
  mcp-docs:
    build: ./servers/docs
    volumes:
      - ./servers/docs:/workspace:delegated
    environment:
      - MCP_NAMESPACE=docs
      - DATABASE_URL=postgresql://user:pass@db:5432/docs_db
    depends_on:
      - db
    stdin_open: true
    tty: true

  # Gateway (n8n workflow automation)
  gateway:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=admin
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=db
    depends_on:
      - db
      - mcp-tasks
      - mcp-docs
    volumes:
      - n8n-data:/home/node/.n8n

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: mcp_platform
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
  n8n-data:
```

**MCP Client Configuration**:
```json
{
  "mcpServers": {
    "tasks": {
      "command": "docker",
      "args": ["compose", "run", "--rm", "mcp-tasks"]
    },
    "docs": {
      "command": "docker",
      "args": ["compose", "run", "--rm", "mcp-docs"]
    }
  }
}
```

**Benefits**:
- ✅ Multiple MCP servers coordinated
- ✅ Shared infrastructure (database)
- ✅ Workflow automation (n8n)

**When to Use**: MCP server ecosystem, complex integrations

---

## Multi-Project Patterns

### Pattern 6: Project-Scoped Compose

**Use Case**: Multiple chora-base projects on same machine, isolated.

**Implementation**:

**Project 1** (project1/docker-compose.yml):
```yaml
services:
  app:
    container_name: project1-app
    ports:
      - "8001:8000"
    # ...

  db:
    container_name: project1-db
    ports:
      - "5433:5432"
    # ...

networks:
  default:
    name: project1-network
```

**Project 2** (project2/docker-compose.yml):
```yaml
services:
  app:
    container_name: project2-app
    ports:
      - "8002:8000"
    # ...

  db:
    container_name: project2-db
    ports:
      - "5434:5432"
    # ...

networks:
  default:
    name: project2-network
```

**Workflow**:
```bash
# Start Project 1
cd ~/projects/project1
docker compose up -d

# Start Project 2
cd ~/projects/project2
docker compose up -d

# Both running simultaneously
curl http://localhost:8001  # Project 1
curl http://localhost:8002  # Project 2
```

**Benefits**:
- ✅ Complete isolation (networks, volumes)
- ✅ No port conflicts
- ✅ Independent scaling

**When to Use**: Multi-project development, testing integrations

---

### Pattern 7: Shared Services Pattern

**Use Case**: Multiple projects share common services (database, cache).

**Implementation**:

**Shared Services** (~/docker/shared-services.yml):
```yaml
services:
  shared-db:
    image: postgres:15-alpine
    container_name: shared-postgres
    environment:
      POSTGRES_PASSWORD: dev
    volumes:
      - shared-postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - shared-network

  shared-redis:
    image: redis:7-alpine
    container_name: shared-redis
    volumes:
      - shared-redis-data:/data
    ports:
      - "6379:6379"
    networks:
      - shared-network

volumes:
  shared-postgres-data:
  shared-redis-data:

networks:
  shared-network:
    name: shared-network
    external: false
```

**Project 1** (project1/docker-compose.yml):
```yaml
services:
  app:
    build: .
    environment:
      - DATABASE_URL=postgresql://postgres:dev@shared-postgres:5432/project1_db
      - REDIS_URL=redis://shared-redis:6379/0
    networks:
      - shared-network

networks:
  shared-network:
    external: true
    name: shared-network
```

**Workflow**:
```bash
# Start shared services once
cd ~/docker
docker compose -f shared-services.yml up -d

# Start projects (connect to shared services)
cd ~/projects/project1
docker compose up -d

cd ~/projects/project2
docker compose up -d
```

**Benefits**:
- ✅ Resource sharing (one database for multiple projects)
- ✅ Faster startup (services already running)
- ✅ Consistent data access

**Trade-offs**:
- ❌ Tighter coupling
- ❌ Shared failure domain

**When to Use**: Resource-constrained environments, integration testing

---

## CI/CD Integration Patterns

### Pattern 8: GitHub Actions with Docker Compose

**Use Case**: Run tests in CI using Docker Compose.

**Implementation**:

**.github/workflows/test.yml**:
```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Create .env.test
        run: |
          cat > .env.local <<EOF
          DATABASE_URL=postgresql://test:test@db:5432/test_db
          REDIS_URL=redis://redis:6379
          TESTING=true
          EOF

      - name: Build containers
        run: docker compose build

      - name: Start services
        run: docker compose up -d db redis

      - name: Wait for services
        run: |
          timeout 30 bash -c 'until docker compose exec -T db pg_isready; do sleep 1; done'

      - name: Run migrations
        run: docker compose run --rm app python -m app.db.migrate

      - name: Run tests
        run: docker compose run --rm app pytest tests/ -v

      - name: Collect coverage
        run: docker compose run --rm app pytest --cov=app --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

      - name: Cleanup
        if: always()
        run: docker compose down -v
```

**docker-compose.yml** (test configuration):
```yaml
services:
  app:
    build: .
    volumes:
      - .:/workspace:delegated
    environment:
      - TESTING=true
      - DATABASE_URL=postgresql://test:test@db:5432/test_db
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "test"]
      interval: 2s
    tmpfs:
      - /var/lib/postgresql/data  # Faster tests (in-memory)
```

**Benefits**:
- ✅ Consistent CI environment
- ✅ Parallel test runs (matrix builds)
- ✅ Easy debugging (reproduce locally)

---

### Pattern 9: GitLab CI with Docker-in-Docker

**Use Case**: GitLab CI pipeline with Docker Compose.

**Implementation**:

**.gitlab-ci.yml**:
```yaml
variables:
  DOCKER_HOST: tcp://docker:2376
  DOCKER_TLS_CERTDIR: "/certs"
  DOCKER_TLS_VERIFY: 1
  DOCKER_CERT_PATH: "$DOCKER_TLS_CERTDIR/client"

services:
  - docker:24-dind

stages:
  - test
  - build

test:
  stage: test
  image: docker/compose:latest
  before_script:
    - echo "DATABASE_URL=postgresql://test:test@db:5432/test_db" > .env.local
    - docker compose build
  script:
    - docker compose up -d db redis
    - sleep 10  # Wait for services
    - docker compose run --rm app pytest tests/ -v
  after_script:
    - docker compose down -v
  only:
    - branches
```

**Benefits**:
- ✅ Docker-in-Docker support
- ✅ Isolated pipeline environments
- ✅ Artifact caching

---

## Development Workflow Patterns

### Pattern 10: Feature Branch Workflow

**Use Case**: Each feature branch has isolated environment.

**Implementation**:

**docker-compose.override.yml** (per-branch):
```yaml
# Branch: feature/auth
services:
  app:
    container_name: auth-feature-app
    ports:
      - "8010:8000"
    environment:
      - BRANCH=feature/auth

  db:
    container_name: auth-feature-db
    ports:
      - "5442:5432"
```

**Workflow**:
```bash
# Developer 1 (feature/auth)
git checkout feature/auth
docker compose up -d  # Uses override, ports 8010/5442

# Developer 2 (feature/payments)
git checkout feature/payments
docker compose up -d  # Uses different override, ports 8020/5452
```

**Benefits**:
- ✅ Parallel feature development
- ✅ No conflicts
- ✅ Easy switching

---

### Pattern 11: Hot Reload Development

**Use Case**: Instant feedback on code changes.

**Implementation**:

**docker-compose.yml**:
```yaml
services:
  app:
    build: .
    volumes:
      - .:/workspace:delegated
      - /workspace/__pycache__  # Exclude bytecode cache
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1
    command: flask run --host=0.0.0.0 --reload  # Hot reload enabled

  # Or for FastAPI
  # command: uvicorn app:app --host 0.0.0.0 --reload
```

**Benefits**:
- ✅ Sub-second reload times
- ✅ No manual restart
- ✅ Preserved application state (when possible)

---

## Production Considerations

### Pattern 12: Production-Ready Compose

**Use Case**: Deploy to single-host production with Docker Compose.

**Implementation**:

**docker-compose.prod.yml**:
```yaml
services:
  app:
    image: registry.example.com/myapp:${VERSION}
    restart: always
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    secrets:
      - app_secret_key
      - db_password
    networks:
      - frontend
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    restart: always
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - app
    networks:
      - frontend

  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - /data/postgres:/var/lib/postgresql/data
    secrets:
      - db_password
    networks:
      - backend

secrets:
  app_secret_key:
    file: ./secrets/app_secret_key.txt
  db_password:
    file: ./secrets/db_password.txt

networks:
  frontend:
  backend:
    internal: true
```

**Deployment**:
```bash
# Deploy
export VERSION=1.2.3
docker compose -f docker-compose.prod.yml up -d

# Update
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d --no-deps app
```

**Trade-offs**:
- ✅ Simple deployment
- ✅ Good for single-host production
- ❌ No auto-scaling
- ❌ No rolling updates (without orchestration)

**When to Use**: Small-scale production, VPS deployments, cost-sensitive environments

---

## Best Practices

### 1. Environment Configuration

**Recommended Structure**:
```
.env.defaults      # Committed (safe defaults)
.env.local         # Gitignored (local overrides)
.env.test          # Committed (test config)
.env.production    # Never committed (managed via secrets)
```

### 2. Volume Management

**Guidelines**:
- Use named volumes for data (databases, caches)
- Use bind mounts for code (development)
- Use tmpfs for ephemeral data (test databases)
- Always use `:delegated` on macOS/Windows

### 3. Service Dependencies

**Pattern**:
```yaml
depends_on:
  service:
    condition: service_healthy  # Always use health checks for critical dependencies
```

### 4. Resource Limits

**Always set in production**:
```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
```

---

## Related Documentation

**SAP-018 Artifacts**:
- [architecture-overview.md](architecture-overview.md) - System architecture
- [design-philosophy.md](design-philosophy.md) - Design principles
- [capability-charter.md](capability-charter.md) - Comprehensive capabilities

**Related SAPs**:
- [SAP-017: chora-compose Integration](../chora-compose-integration/) - Basic integration guide
- [SAP-014: MCP Server Development](../mcp-server-development/) - MCP patterns
- [SAP-004: Testing Framework](../testing-framework/) - Testing patterns

**External Resources**:
- [chora-compose Repository](https://github.com/liminalcommons/chora-compose) - Source code and templates
- [Docker Compose Samples](https://github.com/docker/awesome-compose) - Official examples

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active
