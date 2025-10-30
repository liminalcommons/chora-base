# SAP-017: chora-compose Integration - Awareness Guide

**SAP ID**: SAP-017
**Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active

---

## Overview

This guide provides comprehensive awareness for AI agents and developers working with the chora-compose Integration capability package (SAP-017). It covers common integration scenarios, decision trees, troubleshooting patterns, and cross-domain integration.

**Audience**: AI agents (Claude, GPT-4, etc.), developers integrating Docker Compose with chora-base projects
**Prerequisite SAPs**: SAP-003 (Project Bootstrap), SAP-014 (MCP Server Development - optional)

---

## When to Use SAP-017

### Use Case 1: Multi-Service Development Environments

**Scenario**: Your chora-base project needs databases, caching, message queues, or other services.

**Why SAP-017**:
- ✅ Docker Compose orchestrates multiple services with one command
- ✅ Consistent environments across machines ("works on my machine" eliminated)
- ✅ Service dependencies managed automatically
- ✅ Volume management for persistent data

**Example**:
```yaml
services:
  app:
    build: .
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD", "pg_isready"]
```

**Alternatives**:
- Local installation (postgres, redis locally) - inconsistent across machines, hard to version
- Cloud services (AWS RDS, Redis Cloud) - costs money, requires internet, slower iteration

---

### Use Case 2: MCP Server Deployment

**Scenario**: You've built an MCP server (SAP-014) and want to deploy it with Docker.

**Why SAP-017**:
- ✅ Containerized MCP servers are portable and reproducible
- ✅ Easy to include service dependencies (databases, APIs)
- ✅ Can be orchestrated with other MCP servers
- ✅ Production-ready deployment pattern

**Example**:
```yaml
services:
  mcp-server:
    build: .
    volumes:
      - .:/workspace:delegated
    command: python -m your_mcp_server.server
    stdin_open: true  # For MCP stdio transport
    tty: true
```

**MCP Client Configuration**:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "docker",
      "args": ["compose", "run", "--rm", "mcp-server"]
    }
  }
}
```

**Alternatives**:
- Local Python execution - works, but not reproducible
- Manual Docker commands - complex, not documented
- Kubernetes - overkill for development, steep learning curve

---

### Use Case 3: Team Onboarding

**Scenario**: New team members need to set up development environments quickly.

**Why SAP-017**:
- ✅ One command setup: `docker compose up`
- ✅ No local installation of databases, tools
- ✅ Version-controlled environment (docker-compose.yml in git)
- ✅ Consistent across macOS, Linux, Windows

**Onboarding Steps**:
1. Clone repository
2. Copy `.env.example` to `.env.local`
3. Run `docker compose up -d`
4. Start coding!

**Time Savings**: 2-4 hours (manual setup) → 5-10 minutes (Docker Compose)

**Alternatives**:
- Manual setup documentation - outdated quickly, error-prone
- Virtual machines - heavy, slow
- Dev containers (VS Code) - good, but editor-specific

---

### Use Case 4: Integration Testing

**Scenario**: You need to test your application with real databases, APIs, services.

**Why SAP-017**:
- ✅ Spin up test infrastructure on-demand
- ✅ Isolated test environments (no conflicts)
- ✅ Teardown after tests (`docker compose down`)
- ✅ Fast iteration (cached images)

**Example**:
```yaml
services:
  test:
    build: .
    depends_on:
      test-db:
        condition: service_healthy
    environment:
      - DATABASE_URL=postgresql://test:test@test-db:5432/test_db
    command: pytest tests/ -v

  test-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: test_db
```

**Run Tests**:
```bash
docker compose run --rm test
```

**Alternatives**:
- Mock everything - fast but not realistic
- Shared test database - flaky, not isolated
- Cloud test environments - slow, expensive

---

### Use Case 5: chora-compose Ecosystem Integration

**Scenario**: You want to use pre-configured stacks from chora-compose repository.

**Why SAP-017**:
- ✅ chora-compose provides battle-tested configurations
- ✅ Import common stacks (databases, monitoring, n8n integration)
- ✅ Customize for your project
- ✅ Stay updated with chora-compose improvements

**Example**:
```yaml
# Your project's docker-compose.yml
include:
  - ../chora-compose/stacks/databases.yml
  - ../chora-compose/stacks/monitoring.yml

services:
  app:
    build: .
    depends_on:
      - postgres  # From databases.yml
```

**See**: [chora-compose Repository](https://github.com/liminalcommons/chora-compose)

**Alternatives**:
- Copy-paste configurations - no updates, maintenance burden
- Write from scratch - reinvent wheel, time-consuming

---

## Anti-Patterns (When NOT to Use SAP-017)

### Anti-Pattern 1: Simple Scripts

**Scenario**: You have a simple Python script with no dependencies.

**Why NOT SAP-017**:
- ❌ Docker overhead not justified
- ❌ Slower iteration (container startup time)
- ❌ Added complexity

**Alternative**: Run Python locally, use virtual environments

---

### Anti-Pattern 2: Production at Scale

**Scenario**: You're deploying to production with >10 services, high availability requirements.

**Why NOT SAP-017**:
- ❌ Docker Compose not designed for production orchestration
- ❌ No built-in load balancing, auto-scaling, rolling updates
- ❌ Single-host limitation

**Alternative**: Use Kubernetes, ECS, or managed container services

---

### Anti-Pattern 3: Windows Without WSL2

**Scenario**: Running Docker Desktop on Windows without WSL2.

**Why NOT SAP-017**:
- ❌ Poor performance (Hyper-V backend slower than WSL2)
- ❌ Volume mount issues
- ❌ Path translation problems

**Alternative**: Install WSL2, use Docker Desktop with WSL2 backend, or use Linux VM

---

## Agent Workflows

### Workflow 1: Integrating chora-compose with Existing Project

**Goal**: Add Docker Compose to existing chora-base project.

**Steps**:

1. **Verify Prerequisites**:
   ```bash
   docker --version  # 20.10.0+
   docker compose version  # v2.0.0+
   ```

2. **Create docker-compose.yml**:
   ```yaml
   version: '3.8'
   services:
     app:
       build: .
       volumes:
         - .:/workspace:delegated
       environment:
         - PYTHONUNBUFFERED=1
   ```

3. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /workspace
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "-m", "your_module.server"]
   ```

4. **Create .env.local**:
   ```bash
   # .env.local
   DEBUG=true
   DATABASE_URL=postgresql://dev:dev@db:5432/myapp
   ```

5. **Test**:
   ```bash
   docker compose up -d
   docker compose logs -f app
   docker compose ps
   ```

6. **Iterate**: Make code changes, see them reflected immediately (volume mount)

**Decision Points**:
- **Q**: Run Python locally or in container?
  - **A**: Container for consistency, local for debugging (use hybrid pattern)
- **Q**: Expose database ports to host?
  - **A**: Yes for hybrid development (local Python needs access)

---

### Workflow 2: Debugging Container Issues

**Goal**: Diagnose and fix container startup or runtime issues.

**Steps**:

1. **Check Container Status**:
   ```bash
   docker compose ps -a
   # Look for "Exited" or "Unhealthy" status
   ```

2. **View Logs**:
   ```bash
   docker compose logs app --tail=100
   # Look for error messages, stack traces
   ```

3. **Exec into Container**:
   ```bash
   docker compose exec app bash
   # Or if container crashed:
   docker compose run --rm app bash
   ```

4. **Test Inside Container**:
   ```bash
   # Inside container
   python -c "import your_module"  # Test imports
   env | grep DATABASE  # Check environment variables
   ping db  # Test service connectivity
   ```

5. **Common Issues**:
   - **"Connection refused"**: Service name wrong (use `db` not `localhost`)
   - **"No such file or directory"**: Volume mount issue (check paths)
   - **"Module not found"**: Dependencies not installed (rebuild image)
   - **"Permission denied"**: File ownership issue (use `user:` in compose file)

6. **Fix and Restart**:
   ```bash
   # After fixing docker-compose.yml or Dockerfile
   docker compose down
   docker compose up -d --build
   ```

**Decision Points**:
- **Q**: When to rebuild vs. restart?
  - **A**: Rebuild if Dockerfile/requirements changed, restart for code/config changes
- **Q**: When to use `docker compose run` vs. `exec`?
  - **A**: `run` creates new container (debugging), `exec` enters running container

---

### Workflow 3: Adding a New Service

**Goal**: Add a new service (e.g., Redis cache) to existing Docker Compose setup.

**Steps**:

1. **Add Service to docker-compose.yml**:
   ```yaml
   services:
     app:
       # ... existing config
       depends_on:
         - db
         - redis  # Add dependency

     # ... existing db service

     redis:  # New service
       image: redis:7-alpine
       container_name: my-project-redis
       volumes:
         - redis-data:/data
       networks:
         - app-network
       ports:
         - "6379:6379"  # For local development
       healthcheck:
         test: ["CMD", "redis-cli", "ping"]
         interval: 5s

   volumes:
     redis-data:  # New volume
   ```

2. **Update Application Code**:
   ```python
   import redis

   redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379"))
   ```

3. **Update .env.local**:
   ```bash
   REDIS_URL=redis://redis:6379
   ```

4. **Start New Service**:
   ```bash
   docker compose up -d redis
   docker compose logs redis  # Verify startup
   ```

5. **Test Connection**:
   ```bash
   docker compose exec redis redis-cli ping
   # Should return: PONG

   docker compose exec app python -c "import redis; print(redis.from_url('redis://redis:6379').ping())"
   # Should return: True
   ```

6. **Update Documentation**: Add Redis to README.md services list

**Decision Points**:
- **Q**: Use named volume or bind mount?
  - **A**: Named volume for data persistence, bind mount for config files
- **Q**: Expose port to host?
  - **A**: Yes for local development/debugging, no for container-only access

---

### Workflow 4: Hybrid Development (Local Python + Docker Services)

**Goal**: Run Python locally (fast iteration, IDE support) with Docker services (databases, caches).

**Steps**:

1. **Create docker-compose.yml** (services only):
   ```yaml
   services:
     db:
       image: postgres:15-alpine
       ports:
         - "5432:5432"  # Expose to host
       environment:
         POSTGRES_DB: myapp_dev
         POSTGRES_USER: dev
         POSTGRES_PASSWORD: dev
       volumes:
         - postgres-data:/var/lib/postgresql/data

     redis:
       image: redis:7-alpine
       ports:
         - "6379:6379"  # Expose to host
       volumes:
         - redis-data:/data

   volumes:
     postgres-data:
     redis-data:
   ```

2. **Start Services**:
   ```bash
   docker compose up -d
   ```

3. **Configure Local Python**:
   ```bash
   # .env.local (for local Python)
   DATABASE_URL=postgresql://dev:dev@localhost:5432/myapp_dev
   REDIS_URL=redis://localhost:6379
   ```

4. **Run Python Locally**:
   ```bash
   python -m your_module.server
   # Or use your IDE's run configuration
   ```

5. **Benefits**:
   - Fast code reloading (no container restart)
   - IDE debugging (breakpoints, step-through)
   - Direct file access (logs, outputs)
   - Services still containerized (consistency)

6. **Trade-offs**:
   - Need to manage local Python environment
   - Different from production (less parity)
   - Network: `localhost` locally, `db`/`redis` in containers

**Decision Points**:
- **Q**: When to switch to full containerization?
  - **A**: When deploying, testing production parity, or debugging container-specific issues

---

## Common Pitfalls

### Pitfall 1: Forgetting Volume Mounts

**Scenario**: Edit code, rebuild container, changes still not reflected.

**Example (Broken)**:
```yaml
services:
  app:
    build: .
    # ❌ No volume mount - code baked into image
```

**Fix**:
```yaml
services:
  app:
    build: .
    volumes:
      - .:/workspace:delegated  # ✅ Mount source code
```

**Why This Happens**: Without volume mount, code is copied during `docker build`. Changes require rebuild.

**Prevention**: Always mount source code directory for development.

---

### Pitfall 2: Using `localhost` Instead of Service Names

**Scenario**: App can't connect to database, "connection refused" errors.

**Example (Broken)**:
```python
# ❌ Inside container, localhost points to container itself, not host
DATABASE_URL = "postgresql://user:pass@localhost:5432/db"
```

**Fix**:
```python
# ✅ Use service name from docker-compose.yml
DATABASE_URL = "postgresql://user:pass@db:5432/db"
```

**Exception**: Hybrid development (Python on host) should use `localhost`.

**Prevention**: Use environment variables, configure per environment:
```python
DATABASE_URL = os.getenv("DATABASE_URL")
```

---

### Pitfall 3: Missing `depends_on` with Health Checks

**Scenario**: App starts before database is ready, crashes with connection errors.

**Example (Broken)**:
```yaml
services:
  app:
    depends_on:
      - db  # ❌ Only waits for container start, not readiness
  db:
    image: postgres:15-alpine
```

**Fix**:
```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy  # ✅ Wait for health check
  db:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "dev"]
      interval: 5s
      timeout: 3s
      retries: 5
```

**Why This Happens**: `depends_on` only ensures startup order, not readiness. Databases take seconds to initialize.

**Prevention**: Always add health checks for dependencies (databases, APIs).

---

### Pitfall 4: Committing Secrets to Git

**Scenario**: `.env` file with API keys committed to git repository.

**Example (Broken)**:
```bash
# .env (committed)
DATABASE_PASSWORD=super_secret_password
OPENAI_API_KEY=sk-real-api-key-here
```

**Fix**:
```bash
# .gitignore
.env.local
.env.*.local
secrets/
```

```bash
# .env.defaults (committed - safe defaults)
DATABASE_URL=postgresql://user:password@db:5432/myapp

# .env.local (gitignored - real secrets)
DATABASE_URL=postgresql://user:super_secret_password@db:5432/myapp
OPENAI_API_KEY=sk-real-api-key-here
```

**Why This Happens**: `.env` files are convenient but easy to accidentally commit.

**Prevention**:
- Use `.env.local` for secrets (gitignored)
- Use `.env.defaults` for safe defaults (committed)
- Use Docker secrets for production

---

### Pitfall 5: Slow macOS/Windows Volume Performance

**Scenario**: File operations in container are extremely slow.

**Example (Broken)**:
```yaml
services:
  app:
    volumes:
      - .:/workspace  # ❌ Default consistency (slow on macOS/Windows)
```

**Fix**:
```yaml
services:
  app:
    volumes:
      - .:/workspace:delegated  # ✅ Delegated consistency (faster)
      - /workspace/node_modules  # ✅ Exclude large dirs
      - /workspace/.venv          # ✅ Exclude Python venv
      - pip-cache:/root/.cache/pip  # ✅ Use named volume for cache

volumes:
  pip-cache:
```

**Why This Happens**: Docker Desktop on macOS/Windows uses filesystem translation (osxfs/virtfs), which is slow for many small files.

**Prevention**:
- Use `:delegated` or `:cached` consistency modes
- Exclude large directories (node_modules, .venv, __pycache__)
- Use named volumes for caches

---

## Installation

### Quick Install

Install this SAP with its dependencies:

```bash
python scripts/install-sap.py SAP-017 --source /path/to/chora-base
```

This will automatically install:
- SAP-017 (Chora-Compose Integration)
- SAP-003 (Project Bootstrap & Scaffolding)
- SAP-000 (SAP Framework)

### Part of Sets

This SAP is included in the following [standard sets](../../user-docs/reference/standard-sap-sets.md):

- `full` - All 18 SAPs (complete capability suite)

To install a complete set:

```bash
python scripts/install-sap.py --set full --source /path/to/chora-base
```

### Dependencies

This SAP depends on:
- SAP-003 (Project Bootstrap & Scaffolding)

All dependencies are automatically installed.

### Validation

After installation, verify the SAP artifacts exist:

```bash
ls docs/skilled-awareness/chora-compose-integration/
# Should show: capability-charter.md, protocol-spec.md, awareness-guide.md, adoption-blueprint.md, ledger.md
```

### Custom Installation

For custom installation paths or options, see:
- [Install SAP Set How-To](../../user-docs/how-to/install-sap-set.md)
- [Install SAP Script Reference](../../user-docs/reference/install-sap-script.md)

---

## Related Content

### 4-Domain Cross-References

**Development Documentation** (`docs/dev-docs/`):
- (No specific dev-docs for Docker Compose yet - future SAP-018)

**User Documentation** (`docs/user-docs/`):
- [How to Integrate chora-compose](../../user-docs/how-to/integrate-chora-compose.md) - Quick start guide

**Project Documentation** (`docs/project-docs/`):
- [Wave 3 Track 2 Summary](../../project-docs/wave-3-track-2-summary.md) - SAP-017 creation context

**SAP Documentation** (`docs/skilled-awareness/`):
- [SAP-003: Project Bootstrap](../project-bootstrap/) - chora-base project structure
- [SAP-014: MCP Server Development](../mcp-server-development/) - MCP server patterns
- [SAP-018: chora-compose Meta](../chora-compose-meta/) - Comprehensive chora-compose documentation

### External References

**chora-compose**:
- [chora-compose Repository](https://github.com/liminalcommons/chora-compose) - Pre-configured Docker Compose stacks

**Docker**:
- [Docker Compose Documentation](https://docs.docker.com/compose/) - Official Docker Compose reference
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/) - Optimization tips
- [Compose File Reference](https://docs.docker.com/compose/compose-file/) - Full specification

---

## Quick Reference

### Essential Commands

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f app

# Stop services
docker compose down

# Restart service
docker compose restart app

# Rebuild and restart
docker compose up -d --build app

# Exec into container
docker compose exec app bash

# Run one-off command
docker compose run --rm app pytest tests/

# Check status
docker compose ps

# View resource usage
docker compose stats
```

### Essential Patterns

```yaml
# Basic service with health check
services:
  app:
    build: .
    volumes:
      - .:/workspace:delegated
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app-network
    ports:
      - "8000:8000"

  db:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 5s
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

volumes:
  postgres-data:

networks:
  app-network:
```

---

## Version History

### v1.0.0 (2025-10-29) - Initial Release

**Features**:
- When to Use / Anti-Patterns (5 use cases, 3 anti-patterns)
- Agent Workflows (4 detailed workflows)
- Common Pitfalls (5 scenarios with fixes)
- Related Content (cross-references)

---

## Related Documentation

**SAP-017 Artifacts**:
- [capability-charter.md](capability-charter.md) - Business value, ROI, core capabilities
- [adoption-blueprint.md](adoption-blueprint.md) - Step-by-step integration guide

**SAP Framework**:
- [SAP-000](../sap-framework/) - SAP framework overview
- [INDEX.md](../INDEX.md) - SAP registry

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active
