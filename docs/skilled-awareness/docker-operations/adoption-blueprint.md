---
sap_id: SAP-011
version: 1.0.0
status: Draft
last_updated: 2025-10-28
type: adoption-blueprint
---

# Adoption Blueprint: Docker Operations

**SAP ID**: SAP-011
**Capability Name**: docker-operations
**Version**: 1.0.0
**Last Updated**: 2025-10-28

---

## Quick Start (15 Minutes)

Get Docker running in your chora-base project:

### Step 1: Verify Docker Installed

```bash
docker --version  # Requires 20.10+
docker-compose --version  # Requires v2.0+
```

### Step 2: Copy Docker Files

If project doesn't have Docker files:

```bash
# From chora-base static-template
cp <chora-base>/static-template/Dockerfile .
cp <chora-base>/static-template/Dockerfile.test .
cp <chora-base>/static-template/docker-compose.yml .
cp <chora-base>/static-template/.dockerignore .
```

### Step 3: Customize Templates

Replace Jinja2 variables in copied files:
- `{{ project_name }}` → Your project name
- `{{ project_slug }}` → Your project slug (kebab-case)
- `{{ package_name }}` → Your package name (snake_case)
- `{{ python_version }}` → Your Python version (e.g., 3.11)

### Step 4: Build and Test

```bash
# Build production image
docker build -t myproject:latest .

# Run
docker run --rm myproject:latest mycommand --version

# Or use docker-compose
docker-compose up -d
docker-compose ps
```

### Step 5: Verify Success

```bash
# Check image size (target: ≤250MB)
docker images myproject:latest

# Check health (if using docker-compose)
docker inspect --format='{{.State.Health.Status}}' myproject
```

**Success**: Container runs, image ≤250MB, health check passes

---

## Adoption Levels

### Level 1: Basic Docker (Day 1) - 30 minutes

**Goal**: Run project in Docker container

**Steps**:
1. ✅ Copy Dockerfile (production multi-stage)
2. ✅ Customize project variables
3. ✅ Build image: `docker build -t <project>:latest .`
4. ✅ Run container: `docker run <project>:latest`

**Validation**:
- Image builds without errors
- Container starts and runs command
- Image size ≤250MB

**Deliverables**:
- Working Dockerfile
- Built Docker image

---

### Level 2: Orchestration (Week 1) - 2 hours

**Goal**: Multi-service deployment with docker-compose

**Steps**:
1. ✅ Copy docker-compose.yml
2. ✅ Configure volumes (logs, data, memory)
3. ✅ Set up .env file with secrets
4. ✅ Configure health checks
5. ✅ Start services: `docker-compose up -d`

**Validation**:
- All services start (`docker-compose ps`)
- Volumes persist data across restarts
- Health checks pass
- Logs accessible (`docker-compose logs`)

**Deliverables**:
- Working docker-compose.yml
- Persistent volumes configured
- .env.example for reference

---

### Level 3: CI/CD Integration (Week 2) - 4 hours

**Goal**: Optimized Docker builds in CI pipeline

**Steps**:
1. ✅ Copy Dockerfile.test
2. ✅ Add GitHub Actions workflow with Docker cache
3. ✅ Configure coverage extraction
4. ✅ Set up multi-architecture builds (optional)
5. ✅ Add security scanning (Trivy)

**Validation**:
- CI builds succeed
- Build time ≤45 seconds (with cache)
- Tests run in isolated environment
- Coverage report extracted

**Deliverables**:
- Working Dockerfile.test
- GitHub Actions workflow with cache
- Multi-arch support (amd64 + arm64)

---

### Level 4: Production Deployment (Month 1) - 8 hours

**Goal**: Production-ready deployment with monitoring

**Steps**:
1. ✅ Set up container registry (ghcr.io, Docker Hub)
2. ✅ Configure automated releases (tag → build → push)
3. ✅ Set up health monitoring
4. ✅ Configure reverse proxy (Nginx) if web service
5. ✅ Document deployment procedures

**Validation**:
- Images pushed to registry
- Automated releases working
- Health monitoring active
- Deployment documented

**Deliverables**:
- Container registry setup
- Automated release pipeline
- Production deployment guide

---

## Helper Scripts

### Build Script (build.sh)

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT="myproject"
VERSION="${1:-latest}"

echo "Building ${PROJECT}:${VERSION}..."
docker build -t ${PROJECT}:${VERSION} .

echo "Image built successfully:"
docker images ${PROJECT}:${VERSION} --format "Size: {{.Size}}"

# Tag as latest if version provided
if [ "$VERSION" != "latest" ]; then
    docker tag ${PROJECT}:${VERSION} ${PROJECT}:latest
fi
```

### Test Script (test-docker.sh)

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT="myproject"

echo "Building test image..."
docker build -t ${PROJECT}:test -f Dockerfile.test .

echo "Running tests..."
docker run --rm ${PROJECT}:test

echo "Extracting coverage..."
container_id=$(docker create ${PROJECT}:test)
docker cp $container_id:/app/coverage.xml ./coverage.xml || echo "No coverage found"
docker rm $container_id

echo "Tests complete!"
```

### Cleanup Script (clean-docker.sh)

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "Stopping containers..."
docker-compose down

echo "Removing images..."
docker rmi $(docker images -q myproject) 2>/dev/null || true

echo "Pruning system..."
docker system prune -f

echo "Cleanup complete!"
```

---

## Validation Checklist

### Image Quality

- [ ] Image size ≤250MB
- [ ] Multi-stage build (builder + runtime)
- [ ] Non-root user (UID 1000)
- [ ] No secrets in image (`docker history <image>`)
- [ ] Health check configured and passing
- [ ] .dockerignore excludes unnecessary files

### Security

- [ ] Base image: `python:X.Y-slim` (not `latest`)
- [ ] No HIGH/CRITICAL vulnerabilities (Trivy scan)
- [ ] Secrets via environment variables (not baked in)
- [ ] .git directory excluded from build context

### Performance

- [ ] Build context <20MB
- [ ] GitHub Actions cache enabled (if using CI)
- [ ] Cached builds ≤45 seconds
- [ ] Multi-architecture builds (amd64 + arm64)

### Operations

- [ ] docker-compose.yml for orchestration
- [ ] Volumes configured for persistence
- [ ] Logs accessible (`docker-compose logs`)
- [ ] Health monitoring working
- [ ] Documentation updated (DOCKER_BEST_PRACTICES.md)

---

## Troubleshooting

### Issue: Image >500MB

**Solution**:
1. Verify multi-stage build: `grep "FROM.*as builder" Dockerfile`
2. Check .dockerignore: Exclude `.git`, `venv/`, `docs/`
3. Rebuild: `docker build --no-cache -t test .`

### Issue: CI builds slow (>2 minutes)

**Solution**:
1. Add Docker Buildx: `uses: docker/setup-buildx-action@v3`
2. Enable cache: `cache-from: type=gha`, `cache-to: type=gha,mode=max`
3. Verify layer ordering: Dependencies before code

### Issue: Health check failing

**Solution**:
1. Test manually: `docker exec <container> python -c "import pkg; assert pkg.__version__"`
2. Add `__version__` to `__init__.py` if missing
3. Check logs: `docker logs <container>`

### Issue: Volume permission errors

**Solution**:
```bash
chown -R 1000:1000 ./logs ./data ./.chora/memory
```

---

## Related Documents

- [capability-charter.md](capability-charter.md) - Problem statement
- [protocol-spec.md](protocol-spec.md) - Technical contracts
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [ledger.md](ledger.md) - Adoption tracking
- [DOCKER_BEST_PRACTICES.md](../../../static-template/DOCKER_BEST_PRACTICES.md) - Detailed guidance

---

**Version History**:
- **1.0.0** (2025-10-28): Initial adoption blueprint for docker-operations SAP
