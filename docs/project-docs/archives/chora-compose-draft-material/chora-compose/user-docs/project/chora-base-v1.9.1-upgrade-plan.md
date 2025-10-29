# chora-base v1.9.1 Upgrade Plan - Full Adoption

**Plan Date:** 2025-10-22
**Current Version:** v1.9.0 (100% adoption)
**Target Version:** v1.9.1
**Approach:** Option A - Full Adoption
**Estimated Time:** 3 hours

---

## Objectives

1. Achieve 100% adoption of chora-base v1.9.1
2. Add multi-architecture Docker support (amd64 + arm64)
3. Implement automated Docker verification workflow
4. Add Docker registry push/release commands
5. Enhance Docker documentation with best practices
6. Maintain backward compatibility
7. Test all Docker workflows

---

## Prerequisites

- [ ] Docker Desktop installed with buildx support
- [ ] Access to review chora-base v1.9.1 template files
- [ ] Understanding of current Docker implementation
- [ ] Audit document reviewed ([chora-base-v1.9.1-adoption-audit.md](./chora-base-v1.9.1-adoption-audit.md))

---

## Implementation Plan

### Phase 1: Dockerfile Enhancements (45 minutes)

#### Task 1.1: Add PYTHONDONTWRITEBYTECODE (5 min)
**File:** `Dockerfile`
**Change:** Add to ENV vars in runtime stage
```dockerfile
ENV MCP_TRANSPORT=sse \
    MCP_SERVER_HOST=0.0.0.0 \
    MCP_SERVER_PORT=8000 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
```
**Test:** Build image, verify no .pyc files written

#### Task 1.2: Add Multi-Architecture Support (15 min)
**File:** `Dockerfile`
**Changes:**
1. Add `--platform=$BUILDPLATFORM` to builder stage
2. Add ARG for TARGETPLATFORM
3. Document multi-arch build requirements

```dockerfile
# Stage 1: Builder
FROM --platform=$BUILDPLATFORM python:3.12-slim AS builder

ARG TARGETPLATFORM
ARG BUILDPLATFORM
```

**Test:** `docker buildx build --platform linux/amd64,linux/arm64 .`

#### Task 1.3: Improve Health Check to Import-Based (15 min)
**File:** `Dockerfile`
**Current:**
```dockerfile
HEALTHCHECK CMD curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ | grep -q "[0-9]" || exit 1
```

**New (v1.9.1 pattern):**
```dockerfile
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import chora_compose.mcp; import sys; sys.exit(0)" || exit 1
```

**Benefits:**
- No curl dependency needed (~5MB savings)
- Faster (<100ms vs network roundtrip)
- Tests actual Python import path

**Test:** Build image, verify health check passes

#### Task 1.4: Add Build Metadata Args (10 min)
**File:** `Dockerfile`
**Add to builder stage:**
```dockerfile
ARG VERSION=dev
ARG BUILD_DATE
ARG VCS_REF
LABEL org.opencontainers.image.version="$VERSION" \
      org.opencontainers.image.created="$BUILD_DATE" \
      org.opencontainers.image.revision="$VCS_REF"
```

**Test:** Build with args, inspect labels

---

### Phase 2: docker-compose.yml Enhancements (20 minutes)

#### Task 2.1: Add Service Health Conditions (10 min)
**File:** `docker-compose.yml`
**Add if we have multi-service setup:**
```yaml
depends_on:
  chora-compose:
    condition: service_healthy
```

**Test:** `docker-compose up`, verify dependency ordering

#### Task 2.2: Document n8n Integration Pattern (10 min)
**File:** `docker-compose.yml`
**Add commented-out n8n service example:**
```yaml
# Uncomment to add n8n workflow automation with MCP
# n8n:
#   image: n8nio/n8n:latest
#   ports:
#     - "5678:5678"
#   environment:
#     - N8N_MCP_SERVER_URL=http://chora-compose:8000
#   depends_on:
#     chora-compose:
#       condition: service_healthy
```

**Test:** Documentation review

---

### Phase 3: Justfile Commands (45 minutes)

#### Task 3.1: Add docker-build-multi (10 min)
**File:** `justfile`
**Add command:**
```just
# Build multi-architecture Docker image (amd64 + arm64)
docker-build-multi TAG:
    @echo "Building multi-architecture image: {{TAG}}"
    docker buildx create --use --name chora-builder 2>/dev/null || true
    docker buildx build \
        --platform linux/amd64,linux/arm64 \
        --build-arg VERSION={{TAG}} \
        --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
        --build-arg VCS_REF=$(git rev-parse --short HEAD) \
        -t chora-compose:{{TAG}} \
        --load \
        .
    @echo "Multi-arch build complete: chora-compose:{{TAG}}"
```

**Test:** `just docker-build-multi test`

#### Task 3.2: Add docker-verify (15 min)
**File:** `justfile`
**Add command:**
```just
# Verify Docker image health and functionality
docker-verify TAG:
    @echo "Verifying image: chora-compose:{{TAG}}"
    @echo "1. Starting test container..."
    docker run -d --name chora-test-verify \
        -p 8001:8000 \
        chora-compose:{{TAG}}
    @sleep 5
    @echo "2. Checking health status..."
    docker inspect --format='{{{{.State.Health.Status}}}}' chora-test-verify
    @echo "3. Testing Python import..."
    docker exec chora-test-verify python -c "import chora_compose.mcp; print('✓ Import successful')"
    @echo "4. Checking version..."
    docker exec chora-test-verify python -c "from chora_compose.mcp import __version__; print(f'Version: {{__version__}}')"
    @echo "5. Cleanup..."
    docker stop chora-test-verify >/dev/null
    docker rm chora-test-verify >/dev/null
    @echo "✓ Verification complete"
```

**Test:** `just docker-verify latest`

#### Task 3.3: Add docker-push (10 min)
**File:** `justfile`
**Add command:**
```just
# Push Docker image to registry
docker-push REGISTRY TAG:
    @echo "Pushing to registry: {{REGISTRY}}/chora-compose:{{TAG}}"
    docker tag chora-compose:{{TAG}} {{REGISTRY}}/chora-compose:{{TAG}}
    docker push {{REGISTRY}}/chora-compose:{{TAG}}
    @echo "✓ Push complete"
```

**Test:** `just docker-push localhost:5000 test` (requires local registry)

#### Task 3.4: Add docker-release (10 min)
**File:** `justfile`
**Add command:**
```just
# Complete Docker release workflow (build multi-arch + verify + push)
docker-release VERSION REGISTRY:
    @echo "Starting release workflow for v{{VERSION}}"
    @echo "1. Building multi-architecture image..."
    just docker-build-multi {{VERSION}}
    @echo "2. Verifying image..."
    just docker-verify {{VERSION}}
    @echo "3. Pushing to registry..."
    just docker-push {{REGISTRY}} {{VERSION}}
    @echo "4. Tagging as latest..."
    docker tag chora-compose:{{VERSION}} {{REGISTRY}}/chora-compose:latest
    docker push {{REGISTRY}}/chora-compose:latest
    @echo "✓ Release v{{VERSION}} complete"
```

**Test:** Documentation review (requires registry)

---

### Phase 4: Documentation (60 minutes)

#### Task 4.1: Create DOCKER_BEST_PRACTICES.md (45 min)
**File:** `DOCKER_BEST_PRACTICES.md` (root or docs/reference/)
**Sections to include:**

1. **Introduction** (5 min)
   - Purpose of this guide
   - When to use Docker for MCP servers
   - Overview of chora-compose Docker architecture

2. **Image Optimization** (10 min)
   - Multi-stage builds explained
   - Wheel builds vs editable installs
   - Layer caching strategies
   - Size optimization techniques
   - Benchmark: Our image sizes vs alternatives

3. **Security Best Practices** (10 min)
   - Non-root user (UID 1000)
   - Minimal base images
   - Dependency scanning
   - Secret management
   - Network isolation

4. **Multi-Architecture Builds** (10 min)
   - Why ARM64 matters (Apple Silicon, AWS Graviton)
   - Using docker buildx
   - Platform-specific considerations
   - Testing cross-platform

5. **CI/CD Integration** (10 min)
   - GitHub Actions example
   - Docker layer caching
   - Registry workflows
   - Automated testing

**Source:** Adapt from [chora-base v1.9.1 template](https://github.com/liminalcommons/chora-base/blob/v1.9.1/template/DOCKER_BEST_PRACTICES.md.jinja)

**Test:** Documentation review

#### Task 4.2: Update Existing Docker Docs (15 min)
**Files:**
- `docs/how-to/deployment/deploy-mcp-server-docker.md`
- `docs/reference/deployment/docker-mcp-reference.md`

**Updates:**
- Reference new justfile commands
- Add multi-arch build section
- Link to DOCKER_BEST_PRACTICES.md
- Update examples with v1.9.1 patterns

**Test:** Documentation review

---

### Phase 5: .copier-answers.yml Update (5 minutes)

#### Task 5.1: Update Version Reference
**File:** `.copier-answers.yml`
**Change:**
```yaml
_commit: v1.9.1
```

**Test:** Git diff review

---

### Phase 6: Testing (30 minutes)

#### Task 6.1: Local Build Tests (10 min)
```bash
# Test standard build
just docker-build

# Test multi-arch build
just docker-build-multi 1.6.1-test

# Test verification
just docker-verify 1.6.1-test
```

#### Task 6.2: Health Check Tests (5 min)
```bash
# Start container
just docker-up

# Wait for health
sleep 10

# Check health status
just docker-health

# Test import-based health check
docker exec chora-compose-mcp python -c "import chora_compose.mcp; print('OK')"
```

#### Task 6.3: Integration Tests (10 min)
```bash
# Run existing Docker integration tests
poetry run pytest tests/integration/test_docker_deployment.py -v

# Verify no regressions
poetry run pytest tests/ -k docker -v
```

#### Task 6.4: Documentation Validation (5 min)
- Review all updated docs for accuracy
- Verify all links work
- Test example commands in docs

---

### Phase 7: Commit & Release (15 minutes)

#### Task 7.1: Create Adoption Commits (10 min)

**Commit 1:** Dockerfile enhancements
```bash
git add Dockerfile
git commit -m "feat(docker): adopt chora-base v1.9.1 Dockerfile enhancements

- Add PYTHONDONTWRITEBYTECODE for smaller images
- Add multi-architecture build support (amd64 + arm64)
- Improve health check to import-based (<100ms)
- Add build metadata args (VERSION, BUILD_DATE, VCS_REF)

Based on chora-base v1.9.1 Docker enhancements.
"
```

**Commit 2:** docker-compose enhancements
```bash
git add docker-compose.yml
git commit -m "feat(docker): adopt chora-base v1.9.1 docker-compose patterns

- Add service health conditions for better orchestration
- Document n8n integration pattern
- Enhance environment variable documentation

Based on chora-base v1.9.1 Docker enhancements.
"
```

**Commit 3:** Justfile commands
```bash
git add justfile
git commit -m "feat(docker): add v1.9.1 Docker workflow commands

New commands:
- docker-build-multi: Build multi-architecture images
- docker-verify: Automated health verification
- docker-push: Push to container registry
- docker-release: Complete release workflow

Based on chora-base v1.9.1 Docker enhancements.
"
```

**Commit 4:** Documentation
```bash
git add DOCKER_BEST_PRACTICES.md docs/
git commit -m "docs(docker): add comprehensive Docker best practices guide

- Create DOCKER_BEST_PRACTICES.md (450+ lines)
- Update existing Docker documentation
- Add multi-arch build examples
- Document CI/CD integration patterns

Based on chora-base v1.9.1 Docker enhancements.
"
```

**Commit 5:** Version update
```bash
git add .copier-answers.yml docs/project/
git commit -m "chore(chora-base): complete v1.9.1 adoption

Adopts all chora-base v1.9.1 Docker enhancements:
- Multi-architecture support (amd64 + arm64)
- Automated verification workflow
- Registry push/release commands
- Comprehensive best practices documentation

See docs/project/chora-base-v1.9.1-adoption-audit.md for details.
"
```

#### Task 7.2: Update Adoption Documentation (5 min)
**File:** `docs/project/chora-base-v1.9.1-adoption-audit.md`
**Update:** Change status from 70% to 100%, mark all items as ✅

---

## Success Criteria

- [ ] All v1.9.1 Dockerfile enhancements adopted
- [ ] All v1.9.1 docker-compose enhancements adopted
- [ ] All 5 new justfile commands implemented
- [ ] DOCKER_BEST_PRACTICES.md created
- [ ] All existing Docker docs updated
- [ ] .copier-answers.yml updated to v1.9.1
- [ ] All tests passing
- [ ] Docker builds succeed on both amd64 and arm64
- [ ] Health checks work with import-based approach
- [ ] docker-verify command validates images successfully
- [ ] Documentation is accurate and complete
- [ ] 5 commits created with clear messages
- [ ] Adoption audit updated to 100%

---

## Rollback Plan

If issues arise during adoption:

1. **Dockerfile issues:**
   ```bash
   git checkout HEAD~5 -- Dockerfile
   just docker-rebuild
   ```

2. **docker-compose issues:**
   ```bash
   git checkout HEAD~4 -- docker-compose.yml
   just docker-restart
   ```

3. **Justfile issues:**
   ```bash
   git checkout HEAD~3 -- justfile
   ```

4. **Full rollback:**
   ```bash
   git reset --hard HEAD~5
   just docker-rebuild
   ```

---

## Post-Adoption Tasks

1. **Test in CI/CD:**
   - Verify GitHub Actions still work
   - Test Docker builds in CI
   - Verify no new failures

2. **Update Release Notes:**
   - Add v1.9.1 adoption to next release
   - Highlight multi-arch support
   - Document new Docker commands

3. **Announce to Users:**
   - Blog post or changelog entry
   - Highlight ARM64 support benefit
   - Share best practices guide

4. **Monitor:**
   - Watch for Docker-related issues
   - Gather feedback on new commands
   - Track image sizes and build times

---

## Time Estimate Breakdown

| Phase | Tasks | Time |
|-------|-------|------|
| 1. Dockerfile | 4 tasks | 45 min |
| 2. docker-compose | 2 tasks | 20 min |
| 3. Justfile | 4 tasks | 45 min |
| 4. Documentation | 2 tasks | 60 min |
| 5. .copier-answers | 1 task | 5 min |
| 6. Testing | 4 tasks | 30 min |
| 7. Commit & Release | 2 tasks | 15 min |
| **Total** | **19 tasks** | **3h 40min** |

**Rounded:** 3 hours (accounting for efficiency)

---

## Notes

- This is a **non-breaking upgrade** - all existing functionality preserved
- Many patterns already present in chora-compose (we contributed to v1.9.1!)
- Focus on adding missing commands and documentation
- Multi-arch support is the biggest new capability
- Well-structured commits make review and rollback easy

---

## References

- [Adoption Audit](./chora-base-v1.9.1-adoption-audit.md)
- [chora-base v1.9.1 Release](https://github.com/liminalcommons/chora-base/releases/tag/v1.9.1)
- [chora-base v1.9.1 UPGRADE Guide](https://github.com/liminalcommons/chora-base/blob/v1.9.1/UPGRADE_1.9.0_TO_1.9.1.md)
