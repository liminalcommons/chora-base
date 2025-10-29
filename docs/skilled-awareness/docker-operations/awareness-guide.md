---
sap_id: SAP-011
version: 1.0.0
status: Draft
last_updated: 2025-10-28
type: awareness-guide
---

# Awareness Guide: Docker Operations

**SAP ID**: SAP-011
**Capability Name**: docker-operations
**Version**: 1.0.0
**Last Updated**: 2025-10-28
**Audience**: AI agents (Claude Code, Aider, Cursor)

---

## 1. Overview

This guide provides **agent workflows** for Docker operations in chora-base projects.

**When to use Docker**:
- ✅ Production deployment (MCP servers, web services)
- ✅ CI/CD testing (isolated environment, avoid system conflicts)
- ✅ Multi-architecture builds (Apple Silicon + x86)
- ✅ Local integration testing (with docker-compose)

**When NOT to use Docker**:
- ❌ Local development (use venv instead - faster iteration)
- ❌ Quick prototyping (overhead not justified)

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

## 6. Integration with Other SAPs

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

## 7. Related Documents

**This SAP (docker-operations)**:
- [capability-charter.md](capability-charter.md) - Problem statement, ROI
- [protocol-spec.md](protocol-spec.md) - Technical contracts
- [adoption-blueprint.md](adoption-blueprint.md) - Installation guide
- [ledger.md](ledger.md) - Adoption tracking

**Docker Artifacts**:
- [Dockerfile](../../../static-template/Dockerfile)
- [Dockerfile.test](../../../static-template/Dockerfile.test)
- [docker-compose.yml](../../../static-template/docker-compose.yml)
- [.dockerignore](../../../static-template/.dockerignore)
- [DOCKER_BEST_PRACTICES.md](../../../static-template/DOCKER_BEST_PRACTICES.md)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial awareness guide for docker-operations SAP
