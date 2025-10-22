# Upgrade Guide: chora-base v1.9.0 → v1.9.1

**Release Date:** 2025-10-22
**Focus:** Docker Enhancements - Production Patterns from Adopters

## Overview

Version 1.9.1 introduces significant Docker improvements based on production implementations from three chora-base adopters (coda-mcp, chora-compose, mcp-n8n). These enhancements are **backward compatible** and deliver:

- **40% smaller images** (500MB → 150-250MB)
- **6x faster builds** (with GitHub Actions cache)
- **100% CI reliability** (eliminates system package conflicts)
- **Multi-platform support** (native ARM64 for Apple Silicon)

## Who Should Upgrade?

### Immediate Upgrade Recommended:
- ✅ Projects using Docker for production deployment
- ✅ Projects experiencing CI test failures or inconsistencies
- ✅ Projects deploying to ARM64 (Apple Silicon, AWS Graviton)
- ✅ Projects with large Docker images (>300MB)

### Can Wait:
- ⏸️ Projects not using Docker (`include_docker: false`)
- ⏸️ Projects in early development with no deployment yet
- ⏸️ Projects with custom Docker implementations

## What Changed?

### Template Files Updated:
1. `template/Dockerfile.jinja` - Wheel builds, import-based health checks
2. `template/docker-compose.yml.jinja` - Service dependencies, environment defaults
3. `template/justfile.jinja` - 6 new Docker commands (multi-arch, registry, etc.)
4. `template/Dockerfile.test.jinja` - GitHub Actions cache patterns
5. `template/.dockerignore.jinja` - Optimized build context

### No Changes Required:
- ❌ `copier.yml` - No new questions or options
- ❌ Your project code - No code changes needed
- ❌ Existing CI workflows - Will continue working (can be enhanced)

## Upgrade Steps

### Step 1: Backup Your Customizations (If Any)

If you've customized Docker files, save your changes:

```bash
# Backup your custom Docker files
cp Dockerfile Dockerfile.backup
cp docker-compose.yml docker-compose.yml.backup
cp justfile justfile.backup
```

### Step 2: Update Template

```bash
# From your project root
copier update

# Review changes
git diff
```

### Step 3: Review Key Changes

**Dockerfile Changes:**
- Builder stage now creates wheel instead of editable install
- Health check changed to import-based validation
- Added `PYTHONDONTWRITEBYTECODE=1` environment variable

**docker-compose.yml Changes:**
- Added health check conditions to service dependencies
- Added environment variable defaults (`${VAR:-default}`)
- Added commented three-tier volume strategy examples

**justfile Changes:**
- Existing commands now accept optional `TAG` parameter
- New commands: `docker-build-multi`, `docker-verify`, `docker-shell`, `docker-push`, `docker-release`

### Step 4: Rebuild Docker Images

```bash
# Rebuild production image
just docker-build

# Verify the image works
just docker-verify

# Optional: Rebuild test image
just docker-build-test
```

### Step 5: Test Locally

```bash
# Start services
just docker-compose-up

# Check health
docker ps
docker inspect --format='{{.State.Health.Status}}' <container-name>

# View logs
just docker-logs

# Stop when done
just docker-compose-down
```

### Step 6: Update CI (Optional)

If using GitHub Actions, enhance your workflow with caching:

```yaml
# .github/workflows/test.yml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build test image
  uses: docker/build-push-action@v5
  with:
    file: ./Dockerfile.test
    tags: ${{ github.repository }}:test
    cache-from: type=gha
    cache-to: type=gha,mode=max
    load: true

- name: Run tests
  run: docker run --rm ${{ github.repository }}:test
```

### Step 7: Merge Customizations (If Applicable)

If you had custom Docker configurations, carefully merge them with the new templates:

1. Review your backup files
2. Apply your customizations to the new templates
3. Test thoroughly

## New Features Available

### Multi-Architecture Builds

Build for both Intel and ARM:

```bash
# Build for amd64 + arm64
just docker-build-multi latest

# Verify multi-arch support
docker buildx imagetools inspect <your-image>:latest
```

### Registry Operations

Push images to container registries:

```bash
# Push to registry
just docker-push ghcr.io/your-org/your-project v1.0.0

# Full release (build, verify, push)
just docker-release 1.0.0 ghcr.io/your-org
```

### Image Verification

Smoke test your Docker images:

```bash
# Verify image health
just docker-verify latest

# Output: ✓ your_package v1.0.0
```

### Interactive Debugging

Get a shell inside your container:

```bash
# Open interactive shell
just docker-shell latest

# Explore the container environment
```

## Breaking Changes

**None.** All changes are backward compatible.

### If You Customized Health Checks:

Old format still works but consider upgrading:

```dockerfile
# Old (still works)
HEALTHCHECK CMD your-cli --version || exit 1

# New (faster, no CLI overhead)
HEALTHCHECK CMD python -c "import your_pkg; assert your_pkg.__version__" || exit 1
```

### If You Use Editable Install:

The new Dockerfile uses wheel builds. If you need editable install for development:

```dockerfile
# Override for local development
RUN pip install -e .
```

Or use the local venv for development and Docker for deployment.

## Expected Benefits After Upgrade

### Smaller Images
- **Before:** ~500MB typical image size
- **After:** ~150-250MB (40% reduction)
- **Why:** Wheel builds don't include build tools in runtime image

### Faster Builds
- **Before:** ~3 minutes per build
- **After:** ~30 seconds (with cache)
- **Why:** GitHub Actions cache + optimized layer caching

### More Reliable CI
- **Before:** Possible system package conflicts
- **After:** 100% isolated environment
- **Why:** Docker test environment identical to CI runner

### Multi-Platform Support
- **Before:** amd64 only
- **After:** Native amd64 + arm64
- **Why:** Multi-arch build support via buildx

## Troubleshooting

### Issue: "Module not found" after upgrade

**Cause:** Wheel build changed how package is installed

**Solution:**
```bash
# Rebuild from scratch
docker system prune -f
just docker-build
```

### Issue: Health check failing

**Cause:** Import-based health check requires `__version__` attribute

**Solution:** Ensure your package has `__version__` defined:
```python
# src/your_package/__init__.py
__version__ = "1.0.0"  # Or from pyproject.toml
```

### Issue: Larger image than expected

**Cause:** Unnecessary files in build context

**Solution:**
```bash
# Check build context size
docker build --no-cache -t test . 2>&1 | grep "Sending build context"

# Review .dockerignore
cat .dockerignore
```

### Issue: Multi-arch build fails

**Cause:** Buildx not set up

**Solution:**
```bash
# Set up buildx
docker buildx create --use
docker buildx inspect --bootstrap
```

## Rollback Instructions

If you encounter issues, you can rollback:

```bash
# Restore backup files (if you made backups)
cp Dockerfile.backup Dockerfile
cp docker-compose.yml.backup docker-compose.yml

# Or revert to v1.9.0
copier update --vcs-ref v1.9.0

# Rebuild images
just docker-build
```

## Testing Checklist

Before deploying to production:

- [ ] Docker build completes successfully
- [ ] Image verification passes (`just docker-verify`)
- [ ] Container starts and becomes healthy
- [ ] Health check returns healthy status
- [ ] Application functions correctly in container
- [ ] CI tests pass with new Docker images
- [ ] Multi-arch build works (if needed)
- [ ] Registry push works (if configured)

## Performance Benchmarks

Expected improvements based on adopter data:

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Image Size | 500MB | 150-250MB | 40% smaller |
| Build Time (first) | 3 min | 3 min | Same |
| Build Time (cached) | 3 min | 30 sec | 6x faster |
| Build Context | 80MB | 15MB | 81% smaller |
| Health Check | 100-500ms | <100ms | 2-5x faster |

## Questions or Issues?

1. **Review documentation:** See [CHANGELOG.md](CHANGELOG.md) for detailed changes
2. **Check examples:** See adopter implementations in `inbox/`
3. **Open an issue:** If you encounter problems, open a GitHub issue
4. **Community discussion:** Share your experience upgrading

## Additional Resources

- **CHANGELOG.md** - Detailed technical changes
- **inbox/docker-enhancements-v1.9.1-summary.md** - Integration summary
- **inbox/coda-mcp-docker.md** - Adopter implementation example
- **inbox/chora-compose-docker.md** - Adopter implementation example
- **inbox/mcp-n8n-docker.md** - Adopter implementation example

## Acknowledgments

These enhancements were made possible by production implementations from:
- **coda-mcp team** - Multi-arch builds, health check patterns
- **chora-compose team** - Environment-based config, volume strategies
- **mcp-n8n team** - CI isolation solutions, cache optimization

Thank you for improving chora-base for everyone!

---

**Version:** v1.9.1
**Release Date:** 2025-10-22
**Upgrade Difficulty:** Easy (15-30 minutes)
**Breaking Changes:** None
