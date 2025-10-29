---
sap_id: SAP-011
version: 1.0.0
status: Draft
last_updated: 2025-10-28
type: awareness-guide
---

# Awareness Guide: Docker Operations

**SAP ID**: SAP-010
**Capability Name**: docker-operations
**Version**: 1.0.1
**Last Updated**: 2025-10-28
**Audience**: AI agents (Claude Code, Aider, Cursor)

---

## 1. Overview

### When to Use This SAP

**Use the Docker Operations SAP when**:
- Production deployment of MCP servers or web services (Docker provides isolation)
- CI/CD testing in isolated environment (avoid system conflicts, reproducible builds)
- Multi-architecture builds for Apple Silicon (ARM64) and x86 (AMD64)
- Local integration testing with docker-compose (orchestrate multiple services)
- Optimizing Docker images (reduce size, improve build performance)

**Don't use for**:
- Local development - use venv instead for faster iteration (no Docker rebuild overhead)
- Quick prototyping - Docker overhead not justified for throwaway code
- Simple scripts - containerization adds complexity without benefit
- Projects without deployment needs - Docker is for deployment, not development

---

## 2. Agent Workflows

### 2.1 Build Production Image

**Context**: User requests "build Docker image" or "containerize this project"

**Workflow**:

1. **Verify Dockerfile exists**:
   ```bash
   ls Dockerfile
   ```
   - If missing → copy from blueprints or reference SAP-011

2. **Build image**:
   ```bash
   docker build -t <project-slug>:latest .
   ```
   - Replace `<project-slug>` with actual project name

3. **Verify build success**:
   ```bash
   docker images <project-slug>:latest
   ```
   - Check image size (target: ≤250MB)

4. **Test image**:
   ```bash
   # MCP Server (STDIO)
   docker run --rm <project-slug>:latest <command> --version

   # Web Service
   docker run --rm -p 8000:8000 <project-slug>:latest
   ```

**Success Criteria**:
- Image builds without errors
- Size ≤ 250MB
- Container starts and responds to commands

**Common Issues**:
- "Module not found" → Verify `pyproject.toml` package name matches `src/<package>/`
- Image >500MB → Check `.dockerignore`, ensure multi-stage build
- Permission errors → Ensure UID 1000 (non-root user)

---

### 2.2 Run Tests in Docker (CI Environment)

**Context**: User requests "run tests in Docker" or CI build failing

**Workflow**:

1. **Verify Dockerfile.test exists**:
   ```bash
   ls Dockerfile.test
   ```

2. **Build test image**:
   ```bash
   docker build -t <project-slug>:test -f Dockerfile.test .
   ```

3. **Run tests**:
   ```bash
   docker run --rm <project-slug>:test
   ```
   - This runs `pytest` with coverage (default CMD)

4. **Extract coverage** (if needed):
   ```bash
   container_id=$(docker create <project-slug>:test)
   docker cp $container_id:/app/coverage.xml ./coverage.xml
   docker rm $container_id
   ```

**Success Criteria**:
- Tests pass (100% pass rate in isolated environment)
- Coverage report generated (`coverage.xml`)

**Common Issues**:
- Tests pass locally but fail in Docker → System dependency missing in Dockerfile.test
- Coverage not extracted → Ensure tests ran (check `docker logs`)

---

### 2.3 Deploy with docker-compose

**Context**: User requests "deploy locally" or "run with docker-compose"

**Workflow**:

1. **Verify docker-compose.yml exists**:
   ```bash
   ls docker-compose.yml
   ```

2. **Create .env file** (if not exists):
   ```bash
   cp .env.example .env
   # Edit .env with actual values
   ```

3. **Start services**:
   ```bash
   docker-compose up -d
   ```

4. **Verify health**:
   ```bash
   docker-compose ps
   # Check "State" column: should be "Up" or "Up (healthy)"
   ```

5. **View logs** (if issues):
   ```bash
   docker-compose logs -f <project-slug>
   ```

**Success Criteria**:
- All services start (`docker-compose ps` shows "Up")
- Health checks pass (if configured)
- Application accessible (e.g., `curl http://localhost:8000/health`)

**Common Issues**:
- Port conflicts → Change host port in docker-compose.yml (`8001:8000`)
- Health check failing → Check logs, verify health check command
- Volume permission errors → Run `chown -R 1000:1000 ./logs ./data`

---

### 2.4 Optimize Image Size

**Context**: User reports "image too large" or requests optimization

**Workflow**:

1. **Check current size**:
   ```bash
   docker images <project-slug>:latest --format "{{.Size}}"
   ```

2. **Verify multi-stage build**:
   ```bash
   grep "FROM.*as builder" Dockerfile
   ```
   - If missing → Add builder stage (see protocol-spec.md)

3. **Check .dockerignore**:
   ```bash
   cat .dockerignore | grep -E "^\.git$|^venv/|^docs/"
   ```
   - Should exclude: `.git`, `venv/`, `docs/`, `.vscode/`, `*.md` (except README)

4. **Check build context size**:
   ```bash
   docker build --no-cache -t test . 2>&1 | grep "Sending build context"
   ```
   - Target: <20MB

5. **Rebuild and verify**:
   ```bash
   docker build --no-cache -t <project-slug>:latest .
   docker images <project-slug>:latest
   ```

**Success Criteria**:
- Image size ≤ 250MB
- Build context <20MB
- Multi-stage build (builder + runtime)

**Common Fixes**:
- Add missing .dockerignore entries (`.git/`, `venv/`, `docs/`, `*.md`)
- Convert single-stage to multi-stage (see protocol-spec.md §11.1)
- Use `--no-cache-dir` in `pip install` commands

---

### 2.5 Debug Container Issues

**Context**: Container crashes, health check fails, or unexpected behavior

**Workflow**:

1. **Check container logs**:
   ```bash
   docker logs <container-name>
   # or
   docker-compose logs -f <service-name>
   ```

2. **Run interactive shell**:
   ```bash
   docker run -it --rm <project-slug>:latest /bin/bash
   ```
   - Test commands manually inside container

3. **Check health status**:
   ```bash
   docker inspect --format='{{json .State.Health}}' <container-name> | jq
   ```

4. **Verify environment variables**:
   ```bash
   docker exec <container-name> env
   ```

5. **Check file permissions**:
   ```bash
   docker exec <container-name> ls -la /app/logs
   # Should be owned by appuser (UID 1000)
   ```

**Common Issues**:

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| "Module not found" | `docker run -it <image> python -c "import <pkg>"` | Rebuild with correct package name in pyproject.toml |
| "Permission denied" on /app/logs | `docker exec <container> ls -la /app/logs` | `chown -R 1000:1000 ./logs` on host |
| Health check failing | `docker exec <container> python -c "import <pkg>; print(<pkg>.__version__)"` | Add `__version__` to `__init__.py` |
| Container exits immediately | `docker logs <container>` | Check CMD, verify entrypoint script |

---

### 2.6 Set Up Multi-Architecture Builds

**Context**: User requests "build for ARM64" or "support Apple Silicon"

**Workflow**:

1. **Set up buildx** (one-time):
   ```bash
   docker buildx create --use
   docker buildx inspect --bootstrap
   ```

2. **Build for multiple platforms**:
   ```bash
   docker buildx build --platform linux/amd64,linux/arm64 \
     -t <project-slug>:latest --load .
   ```
   - `--load` loads image into local Docker (single platform only)
   - For multi-platform push: Use `--push` instead of `--load`

3. **Verify platforms**:
   ```bash
   docker buildx imagetools inspect <project-slug>:latest
   ```
   - Should show: `linux/amd64`, `linux/arm64`

**Success Criteria**:
- Image builds for both amd64 and arm64
- No architecture-specific dependencies

**Common Issues**:
- "multiple platforms feature is not supported" → Run `docker buildx create --use`
- Build fails for ARM64 → Check for x86-only dependencies (rare in Python)

---

### 2.7 Enable GitHub Actions Cache

**Context**: CI builds slow (2-3 minutes), user requests optimization

**Workflow**:

1. **Check current workflow**:
   ```yaml
   # .github/workflows/test.yml (current)
   - name: Build
     run: docker build -t test -f Dockerfile.test .
   ```

2. **Add buildx setup**:
   ```yaml
   - name: Set up Docker Buildx
     uses: docker/setup-buildx-action@v3
   ```

3. **Replace docker build with build-push-action**:
   ```yaml
   - name: Build test image
     uses: docker/build-push-action@v5
     with:
       file: ./Dockerfile.test
       tags: ${{ github.repository }}:test
       cache-from: type=gha
       cache-to: type=gha,mode=max
       load: true
   ```

4. **Run workflow and verify speedup**:
   - First build: 2-3 minutes (populates cache)
   - Subsequent builds: ~30 seconds (6x faster)

**Success Criteria**:
- First build completes (cache populated)
- Second build shows "CACHED" in logs
- Build time <45 seconds (cached)

**Common Issues**:
- No speedup → Ensure `cache-to: type=gha,mode=max` (not just `cache-from`)
- Cache misses → Check layer ordering (dependencies before code)

---

### 2.8 Troubleshoot Volume Mounts

**Context**: Data not persisting, config changes not reflected

**Workflow**:

1. **Check volume mounts** (docker-compose.yml):
   ```yaml
   volumes:
     - ./logs:/app/logs
     - ./data:/app/data
     - ./.chora/memory:/app/.chora/memory
   ```

2. **Verify directories exist on host**:
   ```bash
   ls -la logs/ data/ .chora/memory/
   ```
   - If missing → Create: `mkdir -p logs data .chora/memory/{events,knowledge}`

3. **Check ownership** (UID 1000):
   ```bash
   ls -lan logs/
   # Should show UID 1000, not 0 (root) or your user ID
   ```

4. **Fix ownership** (if needed):
   ```bash
   chown -R 1000:1000 logs/ data/ .chora/memory/
   ```

5. **Test persistence**:
   ```bash
   docker-compose up -d
   docker exec <project-slug> sh -c "echo 'test' > /app/logs/test.log"
   docker-compose down
   docker-compose up -d
   docker exec <project-slug> cat /app/logs/test.log
   # Should output: "test"
   ```

**Success Criteria**:
- Data persists across container restarts
- Files owned by UID 1000 inside container
- Config changes reflected (if using read-only mount)

---

## 3. Quick Reference

### Common Commands

**Build**:
```bash
docker build -t <project-slug>:latest .
docker build -t <project-slug>:test -f Dockerfile.test .
```

**Run**:
```bash
docker run -d --name <project-slug> -p 8000:8000 <project-slug>:latest
docker run --rm <project-slug>:test  # Run tests
```

**docker-compose**:
```bash
docker-compose up -d       # Start services
docker-compose ps          # Check status
docker-compose logs -f     # View logs
docker-compose down        # Stop services
```

**Debug**:
```bash
docker logs <container>              # View logs
docker exec -it <container> /bin/bash  # Interactive shell
docker inspect <container>            # Full config
```

**Cleanup**:
```bash
docker system prune -f              # Remove unused images/containers
docker-compose down -v              # Remove containers + volumes (WARNING: deletes data)
```

---

## 4. Decision Trees

### When to use Dockerfile vs Dockerfile.test?

```
Is this for production deployment?
├─ Yes → Use Dockerfile (multi-stage, wheel build)
└─ No → Is this for CI/CD testing?
    ├─ Yes → Use Dockerfile.test (editable install, dev deps)
    └─ No → Use Dockerfile (safer default)
```

### When to use docker-compose vs docker run?

```
Does the project need multiple services (e.g., n8n, nginx)?
├─ Yes → Use docker-compose (orchestration)
└─ No → Does it need volume persistence?
    ├─ Yes → Use docker-compose (easier volume management)
    └─ No → Use docker run (simpler for single service)
```

### When to enable multi-architecture builds?

```
Will this run on Apple Silicon (M1/M2)?
├─ Yes → Enable multi-arch (amd64 + arm64)
└─ No → Will this run on AWS Graviton (ARM64)?
    ├─ Yes → Enable multi-arch
    └─ No → Single-arch (amd64) sufficient
```

---

## 5. Agent Tips

### Tip 1: Always check Dockerfile exists before building

```python
# Good: Check first
if os.path.exists("Dockerfile"):
    run("docker build -t myproject:latest .")
else:
    print("Error: Dockerfile not found")
    # Suggest: Copy from SAP-011 or generate
```

### Tip 2: Use `just` commands when available

```bash
# Instead of:
docker build -t myproject:latest .
docker run --rm myproject:test

# Use (if justfile exists):
just docker-build
just docker-test
```

### Tip 3: Verify image size after build

```bash
# Always check size after building
docker build -t myproject:latest .
docker images myproject:latest --format "{{.Size}}"
# Alert user if >250MB
```

### Tip 4: Test health check before deploying

```bash
# Test health check command manually
docker run -it --rm myproject:latest python -c "import mypackage; assert mypackage.__version__"
# Should exit 0 (success)
```

### Tip 5: Check logs first when debugging

```bash
# Before interactive debugging, check logs
docker logs <container>
# Often reveals the root cause immediately
```

---

## 6. Common Pitfalls

### Pitfall 1: Building Without .dockerignore

**Scenario**: Agent builds Docker image without creating `.dockerignore`, sends huge build context (includes .git/, venv/, docs/).

**Example**:
```bash
# Agent runs docker build:
docker build -t myproject:latest .

# Output shows:
# Sending build context to Docker daemon: 850MB...

# Build takes 5 minutes!
# Image size: 950MB

# Why so slow/large? Build context includes:
# - .git/ (300MB)
# - venv/ (200MB)
# - docs/ (150MB)
# - node_modules/ (200MB)
```

**Fix**: Create .dockerignore BEFORE building:
```bash
# Create .dockerignore:
cat > .dockerignore <<EOF
.git/
venv/
__pycache__/
*.pyc
.pytest_cache/
docs/
*.md
!README.md
node_modules/
.DS_Store
.vscode/
.idea/
EOF

# Now rebuild:
docker build -t myproject:latest .
# Sending build context: 15MB (57x smaller!)
# Build time: 30 seconds (10x faster!)
```

**Why it matters**: Build context affects build speed and image size. Protocol Section 9.2 mandates .dockerignore. Without it, builds take 5-10 minutes instead of 30-60 seconds. Large context also increases image size unnecessarily.

### Pitfall 2: Not Using Multi-Stage Builds

**Scenario**: Agent uses single-stage Dockerfile, includes build tools in production image, creates 500MB+ images.

**Example**:
```dockerfile
# Single-stage Dockerfile (WRONG):
FROM python:3.12
WORKDIR /app

# Install build tools (100MB)
RUN apt-get update && apt-get install -y gcc build-essential

# Copy all code
COPY . .

# Install dependencies
RUN pip install -e .

# Run app
CMD ["python", "-m", "mypackage"]

# Result: Image size 520MB (includes gcc, build-essential)
```

**Fix**: Use multi-stage build (builder + runtime):
```dockerfile
# Multi-stage Dockerfile (CORRECT):

# Stage 1: Builder (includes build tools)
FROM python:3.12 as builder
WORKDIR /app
COPY pyproject.toml .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels .

# Stage 2: Runtime (only runtime dependencies)
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/*
COPY src/ /app/src/
CMD ["python", "-m", "mypackage"]

# Result: Image size 180MB (65% smaller!)
```

**Why it matters**: Multi-stage builds separate build tools from runtime. Protocol Section 11.1 mandates multi-stage for production. Single-stage images are 2-3x larger, slower to pull, larger attack surface.

### Pitfall 3: Running as Root User

**Scenario**: Agent creates Dockerfile without non-root user, container runs as root (UID 0), security issue.

**Example**:
```dockerfile
# Dockerfile without non-root user (WRONG):
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -e .
CMD ["python", "-m", "mypackage"]

# Container runs as root:
$ docker exec mycontainer whoami
# root

# Security issues:
# - If container compromised, attacker has root
# - File permissions issues on volume mounts
```

**Fix**: Create and use non-root user (UID 1000):
```dockerfile
# Dockerfile with non-root user (CORRECT):
FROM python:3.12-slim

# Create non-root user
RUN useradd --create-home --uid 1000 appuser

WORKDIR /app
COPY . .
RUN pip install -e .

# Change ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

CMD ["python", "-m", "mypackage"]

# Container runs as appuser (UID 1000):
$ docker exec mycontainer whoami
# appuser
```

**Why it matters**: Running as root violates security best practices. Protocol Section 11.3 mandates non-root user (UID 1000). Root containers have full system access if compromised. Volume permissions also fail (root writes, user can't read).

### Pitfall 4: Not Testing Locally Before CI

**Scenario**: Agent pushes Dockerfile changes to GitHub, CI fails, wastes 5-10 minutes waiting for CI feedback.

**Example**:
```bash
# Agent modifies Dockerfile:
# - Changes Python version 3.11 → 3.12
# - Updates dependencies

# Agent commits and pushes:
git add Dockerfile
git commit -m "update: upgrade Python to 3.12"
git push origin feature-branch

# Wait 5 minutes for CI...
# CI fails: "Module 'xyz' not compatible with Python 3.12"

# Now must:
# - Fix Dockerfile
# - Push again
# - Wait another 5 minutes for CI

# Total wasted time: 10-15 minutes
```

**Fix**: Test Docker build LOCALLY before pushing:
```bash
# Before committing Dockerfile changes:

# 1. Build locally:
docker build -t test:latest .
# Shows errors immediately (30 seconds)

# 2. Test image:
docker run --rm test:latest python --version
# Verify: Python 3.12.0

# 3. Run tests in Docker:
docker build -t test:test -f Dockerfile.test .
docker run --rm test:test
# Tests pass locally

# 4. NOW commit and push:
git add Dockerfile
git commit -m "update: upgrade Python to 3.12"
git push origin feature-branch

# CI will pass (already tested locally)
```

**Why it matters**: Local Docker testing provides instant feedback. Protocol Section 2.2 workflow includes local testing. Waiting for CI wastes 5-10 minutes per iteration. Local testing takes 30-60 seconds.

### Pitfall 5: Forgetting Volume Permissions (UID Mismatch)

**Scenario**: Agent uses docker-compose with volume mounts, container can't write to volumes because of UID mismatch.

**Example**:
```yaml
# docker-compose.yml
services:
  app:
    image: myproject:latest
    volumes:
      - ./logs:/app/logs  # Host directory

# Agent runs:
docker-compose up -d

# Container tries to write log:
# Error: Permission denied writing to /app/logs/app.log

# Why?
# - Host directory owned by user (UID 501 on macOS)
# - Container runs as appuser (UID 1000)
# - UID 501 ≠ UID 1000 → Permission denied!
```

**Fix**: Set correct permissions on host volumes BEFORE starting:
```bash
# Before docker-compose up:

# 1. Create directories:
mkdir -p logs data .chora/memory

# 2. Set ownership to UID 1000 (container user):
sudo chown -R 1000:1000 logs/ data/ .chora/memory/

# 3. Verify:
ls -lan logs/
# drwxr-xr-x  2 1000 1000  64 Oct 28 12:00 logs/

# 4. NOW start containers:
docker-compose up -d

# Container can now write to volumes (UID match)
```

**Why it matters**: UID mismatch breaks volume writes. Protocol Section 11.3 specifies UID 1000 for consistency. Permission errors block development, require sudo to fix. Setting permissions correctly takes 1 minute, debugging permission errors takes 10-30 minutes.

---

## 7. Integration with Other SAPs

### SAP-003 (project-bootstrap)

When generating projects with Docker:
```bash
# Project includes Dockerfile, docker-compose.yml, .dockerignore
chora-base generate myproject --include-docker
```

### SAP-008 (automation-scripts)

Use `just` commands for Docker operations:
```bash
just docker-build         # Build production image
just docker-test          # Build and run tests in Docker
just docker-run           # Run via docker-compose
just docker-clean         # Clean up images/containers
```

### SAP-010 (memory-system)

Enable A-MEM volume mounts:
```yaml
# docker-compose.yml
volumes:
  - ./.chora/memory/events:/app/.chora/memory/events
  - ./.chora/memory/knowledge:/app/.chora/memory/knowledge
```

---

## 8. Related Content

### Within This SAP (skilled-awareness/docker-operations/)

- [capability-charter.md](capability-charter.md) - Problem statement, scope, outcomes for SAP-010
- [protocol-spec.md](protocol-spec.md) - Complete technical contract (Dockerfile specs, docker-compose config)
- [adoption-blueprint.md](adoption-blueprint.md) - Step-by-step guide for Docker setup
- [ledger.md](ledger.md) - Docker adoption tracking, version history
- **This document** (awareness-guide.md) - Agent workflows for Docker operations

### Developer Process (dev-docs/)

**Workflows**:
- [dev-docs/workflows/docker-development.md](../../dev-docs/workflows/docker-development.md) - Developing with Docker
- [dev-docs/workflows/multi-arch-builds.md](../../dev-docs/workflows/multi-arch-builds.md) - Multi-architecture build process

**Tools**:
- [dev-docs/tools/docker.md](../../dev-docs/tools/docker.md) - Docker CLI reference
- [dev-docs/tools/docker-compose.md](../../dev-docs/tools/docker-compose.md) - docker-compose usage
- [dev-docs/tools/buildx.md](../../dev-docs/tools/buildx.md) - Docker buildx for multi-platform

**Development Guidelines**:
- [dev-docs/development/dockerfile-standards.md](../../dev-docs/development/dockerfile-standards.md) - Dockerfile best practices
- [dev-docs/development/container-security.md](../../dev-docs/development/container-security.md) - Container security guidelines

### Project Lifecycle (project-docs/)

**Implementation Components**:
- [static-template/Dockerfile](/static-template/Dockerfile) - Production Dockerfile (multi-stage)
- [static-template/Dockerfile.test](/static-template/Dockerfile.test) - Test Dockerfile
- [static-template/docker-compose.yml](/static-template/docker-compose.yml) - docker-compose configuration
- [static-template/.dockerignore](/static-template/.dockerignore) - Docker build context exclusions
- [static-template/DOCKER_BEST_PRACTICES.md](/static-template/DOCKER_BEST_PRACTICES.md) - Docker best practices guide

**Guides**:
- [project-docs/guides/docker-setup.md](../../project-docs/guides/docker-setup.md) - Setting up Docker in projects
- [project-docs/guides/container-deployment.md](../../project-docs/guides/container-deployment.md) - Deploying containers

**Audits & Releases**:
- [project-docs/audits/](../../project-docs/audits/) - SAP audits including SAP-010 validation
- [project-docs/releases/](../../project-docs/releases/) - Version release documentation

### User Guides (user-docs/)

**Getting Started**:
- [user-docs/guides/docker-basics.md](../../user-docs/guides/docker-basics.md) - Docker basics for chora-base

**Tutorials**:
- [user-docs/tutorials/building-docker-images.md](../../user-docs/tutorials/building-docker-images.md) - Build Docker images
- [user-docs/tutorials/docker-compose-local.md](../../user-docs/tutorials/docker-compose-local.md) - Local development with docker-compose
- [user-docs/tutorials/optimizing-images.md](../../user-docs/tutorials/optimizing-images.md) - Optimize Docker image size

**Reference**:
- [user-docs/reference/dockerfile-reference.md](../../user-docs/reference/dockerfile-reference.md) - Dockerfile reference
- [user-docs/reference/docker-compose-reference.md](../../user-docs/reference/docker-compose-reference.md) - docker-compose.yml reference

### Other SAPs (skilled-awareness/)

**Core Framework**:
- [sap-framework/](../sap-framework/) - SAP-000 (defines SAP structure)
- [chora-base/protocol-spec.md](../chora-base/protocol-spec.md) - SAP-002 Meta-SAP Section 3.2.8 (documents SAP-010)

**Dependent Capabilities**:
- [project-bootstrap/](../project-bootstrap/) - SAP-003 (generates Docker files)
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (CI builds Docker images)
- [automation-scripts/](../automation-scripts/) - SAP-008 (`just docker-build`, `just docker-test`)

**Supporting Capabilities**:
- [memory-system/](../memory-system/) - SAP-009 (volume mounts for .chora/memory/)
- [quality-gates/](../quality-gates/) - SAP-006 (Dockerfile linting)

**Core Documentation**:
- [README.md](/README.md) - chora-base overview
- [AGENTS.md](/AGENTS.md) - Agent guidance for using chora-base
- [CHANGELOG.md](/CHANGELOG.md) - Version history including SAP-010 updates
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root SAP protocol

---

**Version History**:
- **1.0.1** (2025-10-28): Reformatted "When to Use" section, added "Common Pitfalls" with Wave 2 learnings (5 scenarios: .dockerignore, multi-stage builds, root user, local testing, volume permissions), enhanced "Related Content" with 4-domain coverage (dev-docs/, project-docs/, user-docs/, skilled-awareness/)
- **1.0.0** (2025-10-28): Initial awareness guide for docker-operations SAP
