# SAP-017: chora-compose Integration - Adoption Blueprint

**SAP ID**: SAP-017
**Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active

---

## Overview

This blueprint provides step-by-step instructions for integrating [chora-compose](https://github.com/liminalcommons/chora-compose) with your chora-base Python project. It covers prerequisites, Docker Compose setup, service configuration, and troubleshooting.

**Time Estimate**: 30-60 minutes (first integration), 10-15 minutes (subsequent projects)
**Complexity**: Intermediate (requires Docker and Python experience)
**Prerequisites**: Docker Desktop, chora-base project, basic Docker Compose knowledge

---

## Prerequisites

### System Requirements

**Required**:
- Docker Desktop 4.0+ (with Docker Compose v2)
- Python 3.9+ (for chora-base project)
- chora-base project structure (see [SAP-003](../project-bootstrap/))
- Terminal/command line access
- Text editor or IDE

**Recommended**:
- 8GB+ RAM (for multiple containers)
- 10GB+ free disk space (for Docker images)
- Git (version control)
- Make (for automation - optional)

### Knowledge Prerequisites

**Required**:
- Docker basics (images, containers, volumes)
- Docker Compose fundamentals (services, networks, volumes)
- Python project structure
- Command line basics

**Helpful but not required**:
- Docker networking concepts
- Environment variable management
- Volume mount performance tuning
- Container debugging

---

## Installing the SAP

### Quick Install

Use the automated installation script:

```bash
python scripts/install-sap.py SAP-017 --source /path/to/chora-base
```

**What This Installs**:
- chora-compose-integration capability documentation (5 artifacts)
- No system files (this SAP documents integration patterns)

### Part of Sets

This SAP is included in:
- full

To install a complete set:
```bash
python scripts/install-sap.py --set full --source /path/to/chora-base
```

### Validation

Verify all 5 artifacts exist:

```bash
ls docs/skilled-awareness/chora-compose-integration/*.md
```

---

## Installation Steps

### Step 1: Verify Docker Installation

```bash
# Check Docker version
docker --version  # Should be 20.10.0+

# Check Docker Compose version
docker compose version  # Should be v2.0.0+

# Test Docker is running
docker ps  # Should show running containers (or empty list)
```

**Verification**:
```bash
# Run hello-world to verify Docker works
docker run hello-world
```

**Troubleshooting**:
- **Docker not found**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Permission denied**: On Linux, add user to docker group: `sudo usermod -aG docker $USER`
- **Docker daemon not running**: Start Docker Desktop application

---

### Step 2: Create docker-compose.yml

In your chora-base project root, create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # Your chora-base application
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: my-project-app
    volumes:
      # Mount source code for live reloading
      - .:/workspace:delegated
      # Cache pip dependencies
      - pip-cache:/root/.cache/pip
    environment:
      # Python environment
      - PYTHONUNBUFFERED=1
      - PYTHONPATH=/workspace
    env_file:
      - .env.local  # Local overrides (gitignored)
    depends_on:
      - db
      - redis
    networks:
      - app-network
    ports:
      - "8000:8000"  # Expose your app port
    command: python -m your_module.server

  # PostgreSQL database
  db:
    image: postgres:15-alpine
    container_name: my-project-db
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-myapp}
      POSTGRES_USER: ${POSTGRES_USER:-dev}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-dev}
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql  # Optional: initialization
    networks:
      - app-network
    ports:
      - "5432:5432"  # Expose for local development (optional)
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "${POSTGRES_USER:-dev}"]
      interval: 5s
      timeout: 3s
      retries: 5

  # Redis cache
  redis:
    image: redis:7-alpine
    container_name: my-project-redis
    volumes:
      - redis-data:/data
    networks:
      - app-network
    ports:
      - "6379:6379"  # Expose for local development (optional)
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

volumes:
  postgres-data:
  redis-data:
  pip-cache:

networks:
  app-network:
    driver: bridge
```

**Customization Points**:
- Replace `my-project` with your actual project name
- Change `your_module.server` to your Python module path
- Adjust ports if you have conflicts
- Add/remove services based on your needs

---

### Step 3: Create Dockerfile

Create `Dockerfile` in your project root:

```dockerfile
# Use Python 3.11 slim image (adjust version as needed)
FROM python:3.11-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for Docker layer caching
COPY requirements.txt pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install package in development mode (if using pyproject.toml)
RUN if [ -f pyproject.toml ]; then pip install -e .; fi

# Default command (can be overridden in docker-compose.yml)
CMD ["python", "-m", "your_module.server"]
```

**Optimization Options**:
```dockerfile
# For faster rebuilds (multi-stage build)
FROM python:3.11-slim AS builder
WORKDIR /workspace
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /workspace
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "-m", "your_module.server"]
```

---

### Step 4: Configure Environment Variables

Create `.env.local` (gitignored) for local development:

```bash
# .env.local - Local development environment (DO NOT COMMIT)

# Application
DEBUG=true
LOG_LEVEL=DEBUG

# Database
POSTGRES_DB=myapp_dev
POSTGRES_USER=dev
POSTGRES_PASSWORD=dev_password_change_me
DATABASE_URL=postgresql://dev:dev_password_change_me@db:5432/myapp_dev

# Redis
REDIS_URL=redis://redis:6379

# API Keys (example - use real values)
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=your-key-here

# Feature Flags
ENABLE_CACHING=true
ENABLE_METRICS=false
```

Create `.env.defaults` (committed) for default values:

```bash
# .env.defaults - Default values (safe to commit)

# Application
DEBUG=false
LOG_LEVEL=INFO
PORT=8000

# Database
POSTGRES_DB=myapp
POSTGRES_USER=user
# POSTGRES_PASSWORD should be in .env.local or secrets

# Redis
REDIS_URL=redis://redis:6379

# Feature Flags
ENABLE_CACHING=true
ENABLE_METRICS=true
```

Update `.gitignore`:

```gitignore
# Environment files
.env.local
.env.*.local

# Docker
docker-compose.override.yml
*.override.yml

# Secrets
secrets/
*.key
*.pem
```

---

### Step 5: Start Services

```bash
# Start all services (detached mode)
docker compose up -d

# View logs (all services)
docker compose logs -f

# View logs (specific service)
docker compose logs -f app

# Check service status
docker compose ps
```

**Expected Output**:
```
NAME                    IMAGE                   STATUS              PORTS
my-project-app          my-project-app:latest   Up 10 seconds       0.0.0.0:8000->8000/tcp
my-project-db           postgres:15-alpine      Up 30 seconds       0.0.0.0:5432->5432/tcp
my-project-redis        redis:7-alpine          Up 30 seconds       0.0.0.0:6379->6379/tcp
```

**Verification**:
```bash
# Test application endpoint
curl http://localhost:8000

# Test database connection
docker compose exec db psql -U dev -d myapp_dev -c "SELECT 1;"

# Test Redis connection
docker compose exec redis redis-cli ping  # Should return PONG
```

### Step 6: Update Project AGENTS.md (Post-Install Awareness Enablement)

**Why This Step Matters**:
AGENTS.md serves as the **discoverability layer** for installed SAPs. Without this update, agents cannot find the chora-compose Integration capability, making it invisible to AI assistants like Claude. This step ensures:
- Agents can discover installed SAPs by reading root AGENTS.md
- Quick reference for chora-compose integration operations
- Links to detailed documentation

**Quality Requirements** (validated by SAP audit):
- Agent-executable instructions (specify tool, file, location, content)
- Concrete content template (not placeholders)
- Validation command to verify update
- See: [SAP_AWARENESS_INTEGRATION_CHECKLIST.md](../../dev-docs/workflows/SAP_AWARENESS_INTEGRATION_CHECKLIST.md)

**For agents** (use Edit tool):
1. Open: `AGENTS.md`
2. Find appropriate section (e.g., "Project Structure" or "Capabilities")
3. Add:

```markdown
### chora-compose Integration

Docker-based integration capability enabling chora-compose MCP server and content generation workflows.

**Documentation**: [docs/skilled-awareness/chora-compose-integration/](docs/skilled-awareness/chora-compose-integration/)

**Quick Start**:
- Read: [adoption-blueprint.md](docs/skilled-awareness/chora-compose-integration/adoption-blueprint.md)
- Guide: [awareness-guide.md](docs/skilled-awareness/chora-compose-integration/awareness-guide.md)

**Installation Methods**:
- pip: `pip install chora-compose`
- MCP: Configure Claude Desktop with chora-compose server
- CLI: `chora-compose generate --template <template>`
```

**Validation**:
```bash
grep "chora-compose Integration" AGENTS.md && echo "✅ AGENTS.md updated"
```

---

## Configuration Patterns

### Pattern 1: Hybrid Development (Local Python + Docker Services)

**Use Case**: Run Python locally (with IDE/debugger), use Docker for databases/services.

**docker-compose.yml**:
```yaml
services:
  # Comment out or remove 'app' service
  # app:
  #   build: .
  #   ...

  db:
    image: postgres:15-alpine
    ports:
      - "5432:5432"  # Expose to host
    # ... rest of db config

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"  # Expose to host
    # ... rest of redis config
```

**Local Python Connection**:
```python
# Use localhost instead of service names
DATABASE_URL = "postgresql://dev:dev@localhost:5432/myapp_dev"
REDIS_URL = "redis://localhost:6379"
```

**Start Services**:
```bash
# Start only databases/services
docker compose up db redis -d

# Run Python locally
python -m your_module.server
```

---

### Pattern 2: Full Containerization

**Use Case**: Run everything in Docker for production parity.

**docker-compose.yml**: (Use the full example from Step 2)

**Development Workflow**:
```bash
# Start all services
docker compose up -d

# Exec into app container for debugging
docker compose exec app bash

# Run tests in container
docker compose exec app pytest tests/

# View logs
docker compose logs -f app
```

**Code Changes**: Automatically reflected (volume mount)

---

### Pattern 3: Multiple Projects

**Use Case**: Run multiple chora-base projects simultaneously.

**Strategy**: Use unique project names and ports.

**Project 1** (`docker-compose.yml`):
```yaml
services:
  app:
    container_name: project1-app
    ports:
      - "8001:8000"  # Unique external port
    # ...
  db:
    container_name: project1-db
    ports:
      - "5433:5432"  # Unique external port
    # ...
```

**Project 2** (`docker-compose.yml`):
```yaml
services:
  app:
    container_name: project2-app
    ports:
      - "8002:8000"  # Different external port
    # ...
  db:
    container_name: project2-db
    ports:
      - "5434:5432"  # Different external port
    # ...
```

**Alternative**: Use Docker Compose project names:
```bash
# Project 1
cd project1/
docker compose -p project1 up -d

# Project 2
cd project2/
docker compose -p project2 up -d
```

---

### Pattern 4: Integrating chora-compose Templates

**Use Case**: Import pre-configured services from chora-compose repository.

**Step 1**: Clone chora-compose:
```bash
git clone https://github.com/liminalcommons/chora-compose.git ../chora-compose
```

**Step 2**: Reference external compose files:
```yaml
# docker-compose.yml in your project
version: '3.8'

# Include chora-compose services
include:
  - ../chora-compose/stacks/databases.yml
  - ../chora-compose/stacks/monitoring.yml

services:
  app:
    build: .
    depends_on:
      - postgres  # From databases.yml
      - redis     # From databases.yml
    # ...
```

**Step 3**: Override configurations:
```yaml
# docker-compose.override.yml
services:
  postgres:
    environment:
      POSTGRES_DB: my_custom_db
    ports:
      - "5433:5432"  # Custom port
```

---

## Integration with chora-base

### For MCP Servers (SAP-014)

**docker-compose.yml** for MCP server:
```yaml
services:
  mcp-server:
    build: .
    volumes:
      - .:/workspace:delegated
    environment:
      - MCP_SERVER_NAME=my-server
      - MCP_NAMESPACE=myserver
    command: python -m your_mcp_server.server
    # stdio transport - no ports needed
    stdin_open: true
    tty: true

  # Optional: Database for MCP server
  db:
    image: postgres:15-alpine
    # ...
```

**MCP Client Configuration** (Claude Desktop):
```json
{
  "mcpServers": {
    "my-server": {
      "command": "docker",
      "args": [
        "compose",
        "-f", "/path/to/your/project/docker-compose.yml",
        "run", "--rm", "mcp-server"
      ]
    }
  }
}
```

---

### For Testing (SAP-004)

**Run tests in Docker**:
```bash
# Add test service to docker-compose.yml
services:
  test:
    build: .
    volumes:
      - .:/workspace:delegated
    depends_on:
      - db
      - redis
    environment:
      - TESTING=true
      - DATABASE_URL=postgresql://dev:dev@db:5432/test_db
    command: pytest tests/ -v

# Run tests
docker compose run --rm test

# Or exec into running container
docker compose exec app pytest tests/
```

---

## Troubleshooting

### Issue 1: Containers Not Starting

**Symptoms**: `docker compose up` fails, containers immediately exit.

**Diagnosis**:
```bash
# Check logs
docker compose logs app

# Check container status
docker compose ps -a

# Inspect specific container
docker compose logs app --tail=50
```

**Common Causes**:
- **Missing environment variables**: Check `.env.local` exists and has required values
- **Port conflicts**: Another service using the port (change ports in docker-compose.yml)
- **Invalid command**: Check `command:` in docker-compose.yml matches your project structure
- **Dependency not ready**: Add `depends_on` with `condition: service_healthy`

**Fix Example** (add health checks):
```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
```

---

### Issue 2: Code Changes Not Reflected

**Symptoms**: Edit Python code, but container still runs old code.

**Diagnosis**:
```bash
# Check volume mounts
docker compose config | grep volumes -A 5

# Verify file exists in container
docker compose exec app ls -la /workspace
```

**Common Causes**:
- **Volume mount missing**: Add `. :/workspace` to `volumes:`
- **Code copied during build**: Volume mount overridden by COPY in Dockerfile
- **Python bytecode cached**: Restart container to clear `__pycache__`

**Fix**:
```bash
# Restart containers
docker compose restart app

# Rebuild and restart (if Dockerfile changed)
docker compose up -d --build app
```

---

### Issue 3: Database Connection Errors

**Symptoms**: App can't connect to database, `connection refused` errors.

**Diagnosis**:
```bash
# Check database is healthy
docker compose ps db

# Test connection from app container
docker compose exec app python -c "import psycopg2; psycopg2.connect('postgresql://dev:dev@db:5432/myapp_dev')"

# Check database logs
docker compose logs db
```

**Common Causes**:
- **Service name incorrect**: Use `db` (service name) not `localhost` in connection string
- **Database not ready**: Add `depends_on` with health check
- **Wrong credentials**: Check environment variables match

**Fix**:
```yaml
services:
  app:
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
    depends_on:
      db:
        condition: service_healthy
```

---

### Issue 4: Slow Volume Performance (macOS/Windows)

**Symptoms**: File operations very slow, build times excessive.

**Diagnosis**:
```bash
# Check volume mount options
docker compose config | grep volumes -A 2
```

**Common Causes**:
- **Default volume mount**: No performance optimization
- **Many small files**: node_modules, .venv in volume

**Fix** (use delegated consistency):
```yaml
services:
  app:
    volumes:
      - .:/workspace:delegated  # Faster on macOS/Windows
      - /workspace/node_modules  # Exclude if using JS tools
      - /workspace/.venv         # Exclude Python venv
```

**Alternative** (named volumes for dependencies):
```yaml
services:
  app:
    volumes:
      - .:/workspace:delegated
      - pip-cache:/root/.cache/pip
      - node-modules:/workspace/node_modules  # If using Node.js

volumes:
  pip-cache:
  node-modules:
```

---

### Issue 5: Permission Errors (Linux)

**Symptoms**: Files created by container owned by root, can't edit locally.

**Diagnosis**:
```bash
# Check file ownership
ls -la

# Check container user
docker compose exec app id
```

**Common Causes**:
- **Container runs as root**: Default behavior
- **Volume mount permissions**: Host user ≠ container user

**Fix** (run as host user):
```yaml
services:
  app:
    user: "${UID}:${GID}"  # Use host user ID
    volumes:
      - .:/workspace
```

**Set in** `.env.local`:
```bash
UID=1000  # Run `id -u` to get your UID
GID=1000  # Run `id -g` to get your GID
```

---

## Next Steps

### Quick Wins

1. **Add Development Tools**:
   ```yaml
   services:
     app:
       volumes:
         - .:/workspace:delegated
       # Add development tools
       environment:
         - FLASK_ENV=development  # If using Flask
         - DEBUG=true
       # Enable hot reload
       command: python -m your_module.server --reload
   ```

2. **Add Monitoring** (optional):
   ```yaml
   services:
     prometheus:
       image: prom/prometheus:latest
       volumes:
         - ./prometheus.yml:/etc/prometheus/prometheus.yml
       ports:
         - "9090:9090"

     grafana:
       image: grafana/grafana:latest
       ports:
         - "3000:3000"
   ```

3. **Create Makefile** for shortcuts:
   ```makefile
   # Makefile
   .PHONY: up down logs shell test

   up:
       docker compose up -d

   down:
       docker compose down

   logs:
       docker compose logs -f app

   shell:
       docker compose exec app bash

   test:
       docker compose exec app pytest tests/
   ```

### Advanced Topics

**SAP-018: chora-compose Meta**:
- For comprehensive chora-compose architecture understanding
- Advanced patterns (multi-stage builds, orchestration strategies)
- Production deployment considerations

**CI/CD Integration**:
- GitHub Actions with Docker Compose
- GitLab CI Docker-in-Docker
- Automated testing in containers

**Production Deployment**:
- Docker Compose in production (pros/cons)
- Migration to Kubernetes
- Container registry setup

---

## Related Documentation

**SAP-017 Artifacts**:
- [capability-charter.md](capability-charter.md) - Core capabilities and business value
- [awareness-guide.md](awareness-guide.md) - SAPP navigation

**Related SAPs**:
- [SAP-003: Project Bootstrap](../project-bootstrap/) - chora-base project structure
- [SAP-014: MCP Server Development](../mcp-server-development/) - MCP server patterns
- [SAP-018: chora-compose Meta](../chora-compose-meta/) - Comprehensive chora-compose documentation

**User Documentation**:
- [How to Integrate chora-compose](../../user-docs/how-to/integrate-chora-compose.md) - Quick start guide

**External Resources**:
- [chora-compose Repository](https://github.com/liminalcommons/chora-compose) - Pre-configured Docker Compose stacks
- [Docker Compose Documentation](https://docs.docker.com/compose/) - Official reference
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/) - Optimization tips

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active
