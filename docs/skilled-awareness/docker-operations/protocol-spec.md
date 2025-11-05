---
sap_id: SAP-011
version: 1.0.0
status: Draft
last_updated: 2025-10-28
type: protocol-spec
---

# Protocol Specification: Docker Operations

**SAP ID**: SAP-011
**Capability Name**: docker-operations
**Version**: 1.0.0
**Last Updated**: 2025-10-28

---

## 1. Overview

This protocol defines the **Docker operations capability** for chora-base projects, providing standard patterns for containerization, orchestration, and deployment.

### Purpose

Enable **reproducible, secure, and optimized** container deployments across chora-base projects with:
- Multi-stage production Dockerfiles (150-250MB images)
- CI-optimized test Dockerfiles (6x faster builds with cache)
- Docker Compose orchestration (volumes, networks, health checks)
- Build context optimization (81% size reduction via .dockerignore)
- Production best practices (non-root, security scanning, multi-arch)

### Scope

**5 Docker Artifacts**:
1. `Dockerfile` - Production multi-stage build
2. `Dockerfile.test` - CI/CD test environment
3. `docker-compose.yml` - Service orchestration
4. `.dockerignore` - Build context optimization
5. `DOCKER_BEST_PRACTICES.md` - Guidance and troubleshooting

---

## 2. Architecture

### 2.1 Multi-Stage Build Pattern

**Production Dockerfile** uses 2-stage build:

```
┌─────────────────────────────────────────────────┐
│ Stage 1: Builder (python:3.11-slim)             │
│ ┌─────────────────────────────────────────────┐ │
│ │ 1. Install build dependencies (git, gcc)    │ │
│ │ 2. Copy pyproject.toml, README.md          │ │
│ │ 3. Copy src/                                │ │
│ │ 4. Build wheel: python -m build --wheel    │ │
│ │ 5. Output: /dist/<package>.whl             │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
                      ↓ (COPY wheel only)
┌─────────────────────────────────────────────────┐
│ Stage 2: Runtime (python:3.11-slim)             │
│ ┌─────────────────────────────────────────────┐ │
│ │ 1. Install runtime dependencies            │ │
│ │ 2. Create non-root user (UID 1000)         │ │
│ │ 3. COPY --from=builder /dist/*.whl         │ │
│ │ 4. pip install wheel (not editable)        │ │
│ │ 5. Set up health check                     │ │
│ │ 6. USER appuser (non-root)                 │ │
│ │ 7. CMD <entrypoint>                        │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
Final Image: 150-250MB (vs 500MB+ with editable install)
```

**Why Wheel Distribution**:
- Eliminates import path conflicts (namespace packages)
- Matches PyPI distribution format
- Enables clean separation of build/runtime dependencies
- 40% smaller images (no build tools in production)

### 2.2 Test Dockerfile Pattern

**CI-optimized Dockerfile.test** uses single-stage:

```
┌─────────────────────────────────────────────────┐
│ Stage: Test Environment (python:3.11-slim)      │
│ ┌─────────────────────────────────────────────┐ │
│ │ 1. Install test dependencies (git)          │ │
│ │ 2. Copy pyproject.toml, README.md          │ │
│ │ 3. Copy src/                                │ │
│ │ 4. pip install -e .[dev] (editable)        │ │
│ │ 5. COPY tests/                              │ │
│ │ 6. CMD pytest with coverage                │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
GitHub Actions Cache: 6x faster (3 min → 30 sec)
```

**Why Editable Install for Tests**:
- Faster iteration (no wheel rebuild)
- Full dev dependencies included
- Matches local development environment
- Coverage extraction simplified

### 2.3 Docker Compose Architecture

```
┌───────────────────────────────────────────────────────┐
│ docker-compose.yml (Service Orchestration)            │
│ ┌───────────────────────────────────────────────────┐ │
│ │ Service: <project-slug> (main application)        │ │
│ │ ├─ Build: context=., dockerfile=Dockerfile       │ │
│ │ ├─ Volumes: logs, data, memory (optional)        │ │
│ │ ├─ Network: <project-slug>-network (isolated)    │ │
│ │ ├─ Health Check: Import-based or HTTP            │ │
│ │ └─ Restart: unless-stopped (production)          │ │
│ └───────────────────────────────────────────────────┘ │
│ ┌───────────────────────────────────────────────────┐ │
│ │ Optional: n8n (workflow orchestration)            │ │
│ │ ├─ Depends on: <project-slug> (health check)     │ │
│ │ ├─ Ports: 5678 (web UI)                          │ │
│ │ └─ Volumes: n8n_data (workflow persistence)      │ │
│ └───────────────────────────────────────────────────┘ │
│ ┌───────────────────────────────────────────────────┐ │
│ │ Optional: nginx (reverse proxy)                   │ │
│ │ ├─ Depends on: <project-slug>                    │ │
│ │ ├─ Ports: 80, 443                                │ │
│ │ └─ Volumes: nginx.conf, ssl                      │ │
│ └───────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────┘
```

**Volume Strategy** (3-tier pattern from chora-compose):
1. **Configs** (read-mostly): `./configs:/app/configs:ro` - Hot-reload without rebuild
2. **Ephemeral** (session data): `./ephemeral:/app/ephemeral` - Survives restarts
3. **Persistent** (long-term): `./logs:/app/logs`, `./data:/app/data`, `./.chora/memory:/app/.chora/memory`

---

## 3. Interfaces

### 3.1 Dockerfile Interface

#### Production Dockerfile

**Location**: `static-template/Dockerfile`

**Build Interface**:
```bash
# Standard build
docker build -t <project-slug>:latest .

# With build cache
docker build --cache-from <project-slug>:latest -t <project-slug>:latest .

# Multi-architecture (amd64 + arm64)
docker buildx build --platform linux/amd64,linux/arm64 -t <project-slug>:latest --load .
```

**Run Interface**:
```bash
# MCP Server (STDIO transport)
docker run -d --name <project-slug> \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/.env:/app/.env:ro \
  <project-slug>:latest

# MCP Server (SSE transport, with memory)
docker run -d --name <project-slug> \
  -p 8000:8000 \
  -v $(pwd)/.chora/memory:/app/.chora/memory \
  -v $(pwd)/.env:/app/.env:ro \
  <project-slug>:latest

# Web Service
docker run -d --name <project-slug> \
  -p 8000:8000 \
  -v $(pwd)/.env:/app/.env:ro \
  <project-slug>:latest

# CLI Tool
docker run -it --rm <project-slug>:latest <command>
```

**Environment Variables**:
```bash
# Project-specific (from pyproject.toml)
<PACKAGE_NAME_UPPER>_LOG_LEVEL=INFO|DEBUG|WARNING|ERROR

# Python runtime
PYTHONUNBUFFERED=1            # Real-time logs
PYTHONDONTWRITEBYTECODE=1     # No .pyc files

# Project type specific
# MCP Server:
MCP_TRANSPORT=stdio|sse       # Transport protocol
MCP_SERVER_HOST=0.0.0.0       # Host (SSE only)
MCP_SERVER_PORT=8000          # Port (SSE only)

# Web Service:
PORT=8000                     # HTTP port
```

#### Test Dockerfile

**Location**: `static-template/Dockerfile.test`

**Build Interface**:
```bash
# Standard build
docker build -t <project-slug>:test -f Dockerfile.test .

# With GitHub Actions cache
docker buildx build \
  --file ./Dockerfile.test \
  --tag <project-slug>:test \
  --cache-from type=gha \
  --cache-to type=gha,mode=max \
  --load .
```

**Run Interface**:
```bash
# Run tests with coverage
docker run --rm <project-slug>:test

# Override test command
docker run --rm <project-slug>:test pytest tests/unit/ -v

# Extract coverage report
container_id=$(docker create <project-slug>:test)
docker cp $container_id:/app/coverage.xml ./coverage.xml
docker rm $container_id
```

---

### 3.2 docker-compose.yml Interface

**Location**: `static-template/docker-compose.yml`

**CLI Interface**:
```bash
# Start services
docker-compose up -d

# View logs (follow)
docker-compose logs -f <project-slug>

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# Remove containers and volumes (WARNING: deletes data)
docker-compose down -v

# Run CLI command (for CLI tool projects)
docker-compose run --rm <project-slug> <command>
```

**Configuration Interface** (environment-based):
```yaml
# docker-compose.yml (excerpt)
environment:
  # With defaults
  - LOG_LEVEL=${LOG_LEVEL:-INFO}
  - PORT=${PORT:-8000}

  # Required (fails if not set)
  - DATABASE_URL=${DATABASE_URL}
  - API_KEY=${API_KEY}

env_file:
  - .env  # Load from file
```

**Volume Mounts**:
```yaml
volumes:
  # Persistent (committed)
  - ./logs:/app/logs
  - ./data:/app/data

  # Memory system (committed)
  - ./.chora/memory/events:/app/.chora/memory/events
  - ./.chora/memory/knowledge:/app/.chora/memory/knowledge

  # Config hot-reload (optional)
  - ./configs:/app/configs:ro
```

**Health Check Interface**:
```yaml
# Import-based (MCP servers, CLI tools)
healthcheck:
  test: ["CMD", "python", "-c", "import <package>; assert <package>.__version__"]
  interval: 30s
  timeout: 3s
  retries: 3
  start_period: 5s

# HTTP-based (web services)
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

**Service Dependency Interface**:
```yaml
# n8n depends on MCP server health
depends_on:
  <project-slug>:
    condition: service_healthy  # Wait for health check to pass
```

---

### 3.3 .dockerignore Interface

**Location**: `static-template/.dockerignore`

**Purpose**: Exclude files from Docker build context

**Structure** (81% size reduction, mcp-n8n pattern):
```
# Version control (never in context)
.git
.gitignore
.github/

# Python cache (recursive glob)
**/__pycache__
**/*.py[cod]

# Testing artifacts
.pytest_cache/
.coverage
htmlcov/

# Secrets (critical exclusion)
.env
.env.*
!.env.example  # Exception: include example
*.pem
*.key

# Documentation (not needed in runtime)
docs/
*.md
!README.md  # Exception: include README

# Docker files (no recursion)
Dockerfile
Dockerfile.*
docker-compose.yml

# Virtual environments
venv/
.venv/
```

**Key Patterns**:
- Use `**` for recursive matching (e.g., `**/__pycache__`)
- Use `!` for exceptions (e.g., `!README.md`)
- Exclude secrets unconditionally (`.env`, `*.pem`, `*.key`)
- Exclude dev tools (`.vscode/`, `.idea/`, `.pre-commit-config.yaml`)

**Verification**:
```bash
# Check build context size
docker build --no-cache -t test . 2>&1 | grep "Sending build context"

# Expected: <20MB (with .dockerignore)
# Without: 80MB+ (includes .git, venv, docs)
```

---

### 3.4 DOCKER_BEST_PRACTICES.md Interface

**Location**: `static-template/DOCKER_BEST_PRACTICES.md`

**Purpose**: Human-readable guidance for Docker operations

**Structure** (10 sections):
1. Quick Reference - Common commands
2. Image Optimization - Multi-stage, wheel builds
3. Health Checks - Import-based vs HTTP
4. CI/CD Integration - GitHub Actions cache
5. Multi-Architecture Builds - ARM64 support
6. Development Workflows - Local vs Docker
7. Security Best Practices - Non-root, scanning
8. Production Deployment - Registry, environment config
9. Troubleshooting - Common issues and fixes
10. Volume Management - Data persistence, cleanup

**Key Patterns**:
- Starts with Quick Reference (15 minute quick start)
- Includes copy-paste commands
- Explains "why" behind each pattern
- Troubleshooting section with solutions

---

## 4. Data Models

### 4.1 Dockerfile Manifest Model

```yaml
dockerfile:
  type: enum  # production | test | dev
  base_image: string  # python:3.11-slim
  stages:
    - name: builder
      purpose: string  # Build wheel distribution
      dependencies: array[string]  # [git, build-essential, curl]
      outputs: array[string]  # [/dist/*.whl]
    - name: runtime
      purpose: string  # Minimal runtime environment
      dependencies: array[string]  # [curl, ca-certificates]
      user: string  # appuser (UID 1000)
      health_check:
        type: enum  # import | http | none
        command: string
        interval: duration  # 30s
        timeout: duration  # 3s
        retries: int  # 3
        start_period: duration  # 5s
  entrypoint:
    type: enum  # mcp_server | web_service | cli_tool | library
    command: array[string]  # ["<project-slug>"]
  environment:
    PYTHONUNBUFFERED: "1"
    PYTHONDONTWRITEBYTECODE: "1"
    <PACKAGE>_LOG_LEVEL: string  # INFO
  expected_size: string  # 150-250MB
```

### 4.2 docker-compose.yml Service Model

```yaml
service:
  name: string  # <project-slug>
  build:
    context: path  # .
    dockerfile: string  # Dockerfile
  image: string  # <project-slug>:latest
  container_name: string  # <project-slug>
  restart: enum  # unless-stopped | always | no
  ports: array[string]  # ["8000:8000"]
  env_file: array[path]  # [.env]
  environment: map[string, string]
    LOG_LEVEL: "${LOG_LEVEL:-INFO}"
  volumes: array[volume_mount]
    - type: bind
      source: ./logs
      target: /app/logs
      mode: rw
    - type: bind
      source: ./configs
      target: /app/configs
      mode: ro  # read-only
  networks: array[string]  # [<project-slug>-network]
  healthcheck:
    test: array[string]  # ["CMD", "python", "-c", "..."]
    interval: duration  # 30s
    timeout: duration  # 3s
    retries: int  # 3
    start_period: duration  # 5s
  depends_on:
    - service: string
      condition: enum  # service_started | service_healthy
```

### 4.3 .dockerignore Pattern Model

```yaml
dockerignore_entry:
  pattern: string  # .git | **/__pycache__ | *.md
  type: enum  # exclude | include
  scope: enum  # recursive | single_level
  reason: string  # "Exclude version control history"

examples:
  - pattern: "**/__pycache__"
    type: exclude
    scope: recursive
    reason: "No Python cache in image"

  - pattern: "!README.md"
    type: include
    scope: single_level
    reason: "Include README for documentation"

  - pattern: ".env"
    type: exclude
    scope: single_level
    reason: "Never include secrets in build context"
```

---

## 5. Behavior Contracts

### 5.1 Multi-Stage Build Contract

**Guarantees**:
1. **Builder stage** produces wheel distribution (`.whl` format)
2. **Runtime stage** installs wheel (not editable `-e`)
3. **Final image** contains no build tools (gcc, git, build-essential)
4. **Image size** ≤ 250MB for typical Python projects
5. **Import paths** match PyPI distribution (no conflicts)

**Implementation Pattern**:
```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder
RUN apt-get update && apt-get install -y git build-essential && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml README.md ./
COPY src/ ./src/
RUN pip install build && python -m build --wheel --outdir /dist

# Stage 2: Runtime
FROM python:3.11-slim
COPY --from=builder /dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm -rf /tmp/*.whl
```

### 5.2 Security Contract

**Guarantees**:
1. **Non-root execution**: All processes run as UID 1000 (appuser)
2. **Minimal base**: `python:X.Y-slim` (not `python:X.Y`)
3. **No secrets in image**: Use `.env` files or environment variables
4. **No sensitive files in context**: `.dockerignore` excludes `.git`, `.env`, keys
5. **Vulnerability scanning**: Image passes Trivy HIGH/CRITICAL scan

**Implementation Pattern**:
```dockerfile
# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash appuser && chown -R appuser:appuser /app

# Switch to non-root
USER appuser

# Never bake secrets
# ❌ WRONG: ENV API_KEY=secret123
# ✅ RIGHT: Use docker run -e API_KEY=$API_KEY or .env file
```

### 5.3 Health Check Contract

**Guarantees**:
1. **MCP Servers (STDIO)**: Import-based health check (<100ms overhead)
2. **Web Services (HTTP)**: `/health` endpoint check (<500ms overhead)
3. **CLI Tools / Libraries**: Optional health check (import-based if long-lived)
4. **Health intervals**: 30 seconds (default), configurable via docker-compose.yml
5. **Startup grace period**: 5-10 seconds (allows initialization)

**Implementation Pattern**:
```dockerfile
# MCP Server (STDIO) - Import-based
HEALTHCHECK CMD python -c "import <package>; assert <package>.__version__" || exit 1

# Web Service (HTTP) - Endpoint-based
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1
```

**Why Import-Based for MCP**:
- STDIO transport has no HTTP endpoint
- CLI invocation adds 100-500ms overhead per check
- Import validation sufficient (checks Python env + dependencies)

### 5.4 CI/CD Cache Contract

**Guarantees**:
1. **GitHub Actions**: 6x faster builds with proper cache config
2. **First build**: ~2-3 minutes (populates cache)
3. **Cached builds**: ~30 seconds (uses cached layers)
4. **Cache mode**: `type=gha,mode=max` (all layers, not just final)
5. **Layer ordering**: Dependencies before code (better cache hits)

**Implementation Pattern** (GitHub Actions workflow):
```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build test image
  uses: docker/build-push-action@v5
  with:
    file: ./Dockerfile.test
    tags: ${{ github.repository }}:test
    cache-from: type=gha  # Read from cache
    cache-to: type=gha,mode=max  # Write all layers
    load: true  # Load into Docker
```

### 5.5 Volume Persistence Contract

**Guarantees**:
1. **Logs**: Persisted to `./logs` (safe to commit)
2. **Data**: Persisted to `./data` (backup regularly, not committed)
3. **Memory** (optional): Persisted to `./.chora/memory` (version controlled)
4. **Configs** (optional): Hot-reload from `./configs:ro` (read-only)
5. **Ephemeral** (optional): Session data in `./ephemeral` (survives restarts, not committed)

**Implementation Pattern** (docker-compose.yml):
```yaml
volumes:
  # Logs (persistent, committed)
  - ./logs:/app/logs

  # Data (persistent, not committed)
  - ./data:/app/data

  # Memory (persistent, committed via .chora/memory/)
  - ./.chora/memory/events:/app/.chora/memory/events
  - ./.chora/memory/knowledge:/app/.chora/memory/knowledge

  # Configs (hot-reload, committed)
  - ./configs:/app/configs:ro

  # Ephemeral (session data, not committed)
  - ./ephemeral:/app/ephemeral
```

---

## 6. Quality Attributes

### 6.1 Performance

**Image Size**:
- Target: ≤ 250MB for typical Python projects
- Multi-stage pattern: 40% smaller than single-stage
- Baseline: 150MB (minimal dependencies) to 250MB (common libraries)

**Build Speed**:
- Uncached: 2-3 minutes (first build)
- Cached (GitHub Actions): 30 seconds (6x faster)
- Cache hit rate: ≥80% (proper layer ordering)

**Runtime Performance**:
- Startup time: <5 seconds (non-web) to <10 seconds (web services)
- Health check overhead: <100ms (import-based), <500ms (HTTP)
- Memory footprint: Base image ~60MB + dependencies + application

### 6.2 Security

**Attack Surface Reduction**:
- Minimal base image: `python:X.Y-slim` (~150MB vs `python:X.Y` ~1GB)
- Non-root execution: UID 1000 (prevents privilege escalation)
- No build tools in production: gcc, git excluded from runtime

**Secrets Management**:
- Zero secrets in image layers (auditable via `docker history`)
- Environment-based config (12-factor app pattern)
- .dockerignore excludes: `.env`, `.git`, `*.pem`, `*.key`

**Vulnerability Scanning**:
- Target: Zero HIGH/CRITICAL CVEs (Trivy scan)
- Quarterly base image updates (Python security releases)
- Automated scanning in CI (GitHub Actions)

### 6.3 Reliability

**Health Monitoring**:
- Health checks: 30 second intervals (default)
- Startup grace period: 5-10 seconds
- Retry attempts: 3 before marking unhealthy

**Restart Policies**:
- Production: `restart: unless-stopped`
- Development: `restart: no` (manual control)

**Dependency Management**:
- Service dependencies via `depends_on` with health checks
- Wait for upstream services before starting
- Graceful degradation if optional services unavailable

### 6.4 Maintainability

**Standardization**:
- Consistent Dockerfile structure across all projects
- Common naming: `<project-slug>:latest`, `<project-slug>:test`
- Predictable volume mounts: `./logs`, `./data`, `./.chora/memory`

**Documentation**:
- Inline comments in Dockerfiles (explains "why")
- DOCKER_BEST_PRACTICES.md (comprehensive guide)
- Quick Reference section (15 minute quickstart)

**Troubleshooting**:
- Common issues documented with solutions
- Health check debugging commands
- Build context verification commands

---

## 7. Error Handling

### 7.1 Build Errors

**Error**: "Module not found" after wheel install
**Cause**: Import path mismatch (editable vs wheel)
**Solution**: Rebuild from scratch, verify `pyproject.toml` package name

**Error**: Build context >100MB
**Cause**: Missing `.dockerignore` entries
**Solution**: Check `docker build` output, add large directories to `.dockerignore`

**Error**: Multi-architecture build fails (ARM64)
**Cause**: Missing buildx setup
**Solution**: Run `docker buildx create --use && docker buildx inspect --bootstrap`

### 7.2 Runtime Errors

**Error**: Health check failing immediately
**Cause**: Missing `__version__` in `__init__.py` (import-based check)
**Solution**: Add `__version__ = "X.Y.Z"` to package `__init__.py`

**Error**: "Permission denied" on volume mounts
**Cause**: Host directory permissions mismatch with UID 1000
**Solution**: `chown -R 1000:1000 ./logs ./data` on host

**Error**: Container exits immediately
**Cause**: Invalid CMD or missing entrypoint
**Solution**: Check logs (`docker logs <container>`), verify entrypoint script

### 7.3 Network Errors

**Error**: Service cannot connect to dependent service
**Cause**: Missing network configuration
**Solution**: Verify `networks` section in docker-compose.yml

**Error**: Port already in use
**Cause**: Another container using same host port
**Solution**: Change host port in docker-compose.yml (`8001:8000`)

---

## 8. Versioning

### 8.1 Image Tagging Strategy

**Tags**:
- `latest` - Latest stable build (production)
- `test` - CI test image (Dockerfile.test)
- `vX.Y.Z` - Specific version (e.g., `v1.2.3`)
- `vX.Y` - Minor version (e.g., `v1.2` → latest `v1.2.Z`)
- `vX` - Major version (e.g., `v1` → latest `v1.Y.Z`)

**Example**:
```bash
# Build specific version
docker build -t myproject:v1.2.3 .

# Tag as latest
docker tag myproject:v1.2.3 myproject:latest

# Tag major/minor versions
docker tag myproject:v1.2.3 myproject:v1.2
docker tag myproject:v1.2.3 myproject:v1
```

### 8.2 Dockerfile Versioning

**Pattern**: Dockerfiles evolve with chora-base template versions

**Version Tracking**:
```dockerfile
# Multi-stage Dockerfile for <project>
# Generated by chora-base template v3.3.0
# Optimized for production deployment with security best practices
```

**Upgrade Path**:
- chora-base v3.3.0: Multi-stage wheel build (current)
- chora-base v3.4.0: (future) Potential improvements (distroless base, layer caching enhancements)

---

## 9. Dependencies

### 9.1 External Dependencies

**Required**:
- Docker Engine 20.10+ or Docker Desktop
- docker-compose v2.0+ (or Docker Compose plugin)

**Optional**:
- Docker Buildx (multi-architecture builds)
- GitHub Actions (CI/CD cache optimization)
- Container registry (ghcr.io, Docker Hub, ECR)

### 9.2 chora-base SAP Dependencies

**Foundational**:
- **SAP-000** (sap-framework): Provides SAP structure, governance

**Integration Points** (not blocking):
- **SAP-003** (project-bootstrap): Generates Docker files via `--include-docker` flag
- **SAP-008** (automation-scripts): `just docker-*` commands (build, test, run, clean)
- **SAP-010** (memory-system): `.chora/memory` volume mounts (optional)

---

## 9.5. Self-Evaluation Criteria

### Awareness File Requirements (SAP-009 Phase 4)

**Both AGENTS.md and CLAUDE.md Required** (Equivalent Support):
- [ ] Both files exist in `docs/skilled-awareness/docker-operations/`
- [ ] Both files have YAML frontmatter with progressive loading metadata
- [ ] Workflow coverage equivalent (±30%): AGENTS.md ≈ CLAUDE.md workflows

**Required Sections (Both Files)**:
- [ ] Quick Start / Quick Start for Claude
- [ ] Common Workflows / Claude Code Workflows
- [ ] Best Practices / Claude-Specific Tips
- [ ] Common Pitfalls / Troubleshooting
- [ ] Related Content / Support & Resources

**Source Artifact Coverage (Both Files)**:
- [ ] capability-charter.md problem statement → "When to Use" section
- [ ] protocol-spec.md technical contracts → "Technical Patterns" (AGENTS) / "Tool Usage" (CLAUDE)
- [ ] awareness-guide.md workflows → "Common Workflows" section
- [ ] adoption-blueprint.md installation → "Quick Start" section
- [ ] ledger.md metrics → referenced in "Evidence of Use"

**YAML Frontmatter Fields** (Required):
```yaml
sap_id: SAP-011
version: X.Y.Z
status: active | pilot | draft
last_updated: YYYY-MM-DD
type: reference
audience: agents | claude_code
complexity: beginner | intermediate | advanced
estimated_reading_time: N
progressive_loading:
  phase_1: "lines 1-X"
  phase_2: "lines X-Y"
  phase_3: "full"
phase_1_token_estimate: NNNN
phase_2_token_estimate: NNNN
phase_3_token_estimate: NNNN
```

**Validation Commands**:
```bash
# Check both files exist
test -f docs/skilled-awareness/docker-operations/AGENTS.md && \
test -f docs/skilled-awareness/docker-operations/CLAUDE.md

# Validate YAML frontmatter
grep -A 10 "^---$" docs/skilled-awareness/docker-operations/AGENTS.md | grep "progressive_loading:"
grep -A 10 "^---$" docs/skilled-awareness/docker-operations/CLAUDE.md | grep "progressive_loading:"

# Check workflow count equivalence (should be within ±30%)
agents_workflows=$(grep "^### Workflow" docs/skilled-awareness/docker-operations/AGENTS.md | wc -l)
claude_workflows=$(grep "^### Workflow" docs/skilled-awareness/docker-operations/CLAUDE.md | wc -l)
echo "AGENTS workflows: $agents_workflows, CLAUDE workflows: $claude_workflows"

# Run comprehensive evaluation
python scripts/sap-evaluator.py --deep SAP-011
```

**Expected Workflow Coverage**:
- AGENTS.md: 8 generic agent workflows (Build, Test, docker-compose, Optimize, Debug, Multi-arch, CI cache, Volumes)
- CLAUDE.md: 3 Claude Code workflows (Containerize, docker-compose setup, Debugging)
- Rationale: Different granularity acceptable - AGENTS.md is comprehensive, CLAUDE.md focuses on high-level tool patterns

---

## 10. Testing and Validation

### 10.1 Image Validation

**Size Check**:
```bash
docker images <project-slug>:latest --format "{{.Size}}"
# Expected: ≤250MB
```

**Health Check Validation**:
```bash
docker run -d --name test <project-slug>:latest
sleep 10  # Allow startup
docker inspect --format='{{.State.Health.Status}}' test
# Expected: "healthy"
docker rm -f test
```

**Security Scan**:
```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image <project-slug>:latest --severity HIGH,CRITICAL
# Expected: 0 vulnerabilities
```

### 10.2 Build Cache Validation

**First Build**:
```bash
time docker build --no-cache -t test .
# Expected: 2-3 minutes
```

**Cached Build**:
```bash
# Change src/ file (not pyproject.toml)
echo "# comment" >> src/<package>/__init__.py

time docker build -t test .
# Expected: <1 minute (layers cached up to COPY src/)
```

### 10.3 docker-compose Validation

**Service Startup**:
```bash
docker-compose up -d
docker-compose ps
# Expected: All services "Up" or "Up (healthy)"
```

**Volume Persistence**:
```bash
docker-compose up -d
docker exec <project-slug> sh -c "echo 'test' > /app/logs/test.log"
docker-compose down
docker-compose up -d
docker exec <project-slug> cat /app/logs/test.log
# Expected: "test" (volume persisted)
docker-compose down
```

---

## 11. Migration and Upgrades

### 11.1 Upgrading from Single-Stage to Multi-Stage

**Before** (single-stage):
```dockerfile
FROM python:3.11-slim
COPY . .
RUN pip install -e .
CMD ["<project-slug>"]
```

**After** (multi-stage):
```dockerfile
FROM python:3.11-slim as builder
COPY pyproject.toml README.md ./
COPY src/ ./src/
RUN pip install build && python -m build --wheel --outdir /dist

FROM python:3.11-slim
COPY --from=builder /dist/*.whl /tmp/
RUN pip install /tmp/*.whl && rm /tmp/*.whl
CMD ["<project-slug>"]
```

**Migration Steps**:
1. Add builder stage (build wheel)
2. Change runtime to install wheel (not editable)
3. Remove `-e` flag from pip install
4. Test: `docker build -t test . && docker run test <project-slug> --version`

### 11.2 Adopting GitHub Actions Cache

**Before** (no cache):
```yaml
- name: Build
  run: docker build -t test -f Dockerfile.test .
```

**After** (with cache):
```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build
  uses: docker/build-push-action@v5
  with:
    file: ./Dockerfile.test
    tags: test
    cache-from: type=gha
    cache-to: type=gha,mode=max
    load: true
```

**Migration Steps**:
1. Add buildx setup step
2. Replace `docker build` with `docker/build-push-action`
3. Add cache config (`cache-from`, `cache-to`)
4. Monitor build times (expect 6x speedup)

---

## 12. Related Documents

**This SAP (docker-operations)**:
- [capability-charter.md](capability-charter.md) - Problem statement, ROI
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [adoption-blueprint.md](adoption-blueprint.md) - Installation guide
- [ledger.md](ledger.md) - Adoption tracking

**Docker Artifacts** (in static-template):
- [Dockerfile](../../../static-template/Dockerfile) - Production image
- [Dockerfile.test](../../../static-template/Dockerfile.test) - CI image
- [docker-compose.yml](../../../static-template/docker-compose.yml) - Orchestration
- [.dockerignore](../../../static-template/.dockerignore) - Build optimization
- [DOCKER_BEST_PRACTICES.md](../../../static-template/DOCKER_BEST_PRACTICES.md) - Guidance

**Related SAPs**:
- [SAP-000: sap-framework](../sap-framework/) - Framework foundation
- [SAP-003: project-bootstrap](../project-bootstrap/) - Project generation
- [SAP-008: automation-scripts](../automation-scripts/) - `just docker-*` commands
- [SAP-010: memory-system](../memory-system/) - A-MEM volume mounts

**External Documentation**:
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Buildx](https://docs.docker.com/buildx/working-with-buildx/)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial protocol specification for docker-operations SAP
