# GAP-003: Unified Release Workflow Implementation Plan

**GAP ID**: GAP-003
**EVS Score**: 2.55/3.0 (Critical)
**Status**: Ready for Implementation
**Created**: 2025-11-03
**Trace ID**: sap-synergy-2025-001

---

## Executive Summary

**Problem**: SAP-012 publishes PyPI packages but Docker images are built/pushed separately via manual workflow. This causes:
- 20-40 min manual effort per release
- No validation that Docker builds succeed before PyPI release
- Version inconsistencies between PyPI and Docker tags
- 12-24 releases/year = 4-16 hours/year wasted

**Solution**: Create unified release workflow integrating SAP-011 (Docker) + SAP-012 (PyPI) with automated validation in SAP-005 (CI/CD).

**Impact**:
- Time saved: 20-40 min per release
- Quality: Docker builds validated before release
- Consistency: Automated version synchronization
- Frequency: 12-24 releases/year

---

## Current State Analysis

### Existing Release Process

**PyPI Release** (SAP-012 development-lifecycle):
- Manual version bump in `pyproject.toml` or `setup.py`
- Manual CHANGELOG update
- Git tag creation
- PyPI publish (manual or via CI)

**Docker Release** (SAP-011 docker-operations):
- Manual `docker-compose.yml` tag updates
- Manual Docker build
- Manual Docker push to registry
- No validation in CI before release

**Gap**: These are completely separate workflows with no synchronization.

### Expected Future State

**Unified Release Workflow**:
1. Single command: `./scripts/bump-version.sh 1.2.3`
   - Updates `pyproject.toml` version
   - Updates `docker-compose.yml` image tags
   - Updates CHANGELOG.md with release notes template
   - Creates git tag

2. CI validates Docker build: `release.yml` workflow
   - Triggers on tag push
   - Builds Docker image for all platforms (amd64, arm64)
   - Runs health check tests on Docker container
   - Only proceeds to publish if Docker build succeeds

3. Single publish command: `./scripts/publish-prod.sh`
   - Publishes to PyPI
   - Pushes Docker image to registry
   - Creates GitHub release
   - Validates all artifacts published

---

## Implementation Tasks

### Task 1: Create `scripts/bump-version.sh`

**Purpose**: Automate version bumping across PyPI and Docker configurations.

**Pseudocode**:
```bash
#!/usr/bin/env bash
# Usage: ./scripts/bump-version.sh <version>
# Example: ./scripts/bump-version.sh 1.2.3

VERSION="$1"

# Validate semantic version format
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    error "Invalid version format. Use semver: X.Y.Z"
    exit 1
fi

# 1. Update pyproject.toml version
sed -i "s/^version = \".*\"/version = \"$VERSION\"/" pyproject.toml

# 2. Update docker-compose.yml image tags
# Find all image: lines and update version tags
sed -i "s/:v[0-9]\+\.[0-9]\+\.[0-9]\+/:v$VERSION/g" docker-compose.yml
sed -i "s/:latest/:v$VERSION/g" docker-compose.yml  # If using :latest

# 3. Update CHANGELOG.md
DATE=$(date +%Y-%m-%d)
cat > CHANGELOG.tmp <<EOF
## [$VERSION] - $DATE

### Added
- TODO: List new features

### Changed
- TODO: List changes

### Fixed
- TODO: List bug fixes

---

EOF
cat CHANGELOG.md >> CHANGELOG.tmp
mv CHANGELOG.tmp CHANGELOG.md

# 4. Create git tag
git add pyproject.toml docker-compose.yml CHANGELOG.md
git commit -m "chore(release): Bump version to v$VERSION"
git tag -a "v$VERSION" -m "Release v$VERSION"

echo "✅ Version bumped to $VERSION"
echo "Next steps:"
echo "  1. Update CHANGELOG.md with actual changes"
echo "  2. git push && git push --tags"
echo "  3. CI will validate Docker build"
echo "  4. Run ./scripts/publish-prod.sh to publish"
```

**Requirements**:
- Must validate semver format
- Must update all version references atomically
- Must create annotated git tag
- Should provide clear next steps

**Testing**:
```bash
# Test version bump
./scripts/bump-version.sh 1.2.3
git diff  # Verify changes
git tag -d v1.2.3  # Cleanup test tag
git reset HEAD~1  # Undo commit
```

**Acceptance Criteria**:
- [ ] Script validates semver format
- [ ] Updates `pyproject.toml` version field
- [ ] Updates all Docker image tags in `docker-compose.yml`
- [ ] Prepends CHANGELOG template with version and date
- [ ] Creates git commit with conventional commit format
- [ ] Creates annotated git tag
- [ ] Provides clear guidance on next steps
- [ ] Executable and has proper shebang

---

### Task 2: Create `scripts/publish-prod.sh`

**Purpose**: Unified publish script for PyPI + Docker + GitHub Release.

**Pseudocode**:
```bash
#!/usr/bin/env bash
# Usage: ./scripts/publish-prod.sh
# Prerequisites:
#   - Git tag must exist (created by bump-version.sh)
#   - CI must have validated Docker build (release.yml passed)
#   - PyPI token in ~/.pypirc or PYPI_TOKEN env var
#   - Docker registry credentials configured

set -euo pipefail

# 1. Detect version from git tag
VERSION=$(git describe --tags --exact-match 2>/dev/null || echo "")
if [ -z "$VERSION" ]; then
    error "No git tag found. Run ./scripts/bump-version.sh first"
    exit 1
fi

# 2. Verify CI passed for this tag
echo "Checking CI status for $VERSION..."
# Use gh CLI to check workflow status
gh run list --branch "$VERSION" --workflow release.yml --limit 1 --json conclusion
CONCLUSION=$(gh run list --branch "$VERSION" --workflow release.yml --limit 1 --json conclusion -q '.[0].conclusion')
if [ "$CONCLUSION" != "success" ]; then
    error "CI did not pass for $VERSION. Fix issues before publishing."
    exit 1
fi

# 3. Publish to PyPI
echo "Publishing to PyPI..."
python -m build
python -m twine upload dist/*

# 4. Push Docker image to registry
echo "Pushing Docker image to registry..."
docker-compose build
docker tag myproject:v$VERSION myregistry.io/myproject:v$VERSION
docker tag myproject:v$VERSION myregistry.io/myproject:latest
docker push myregistry.io/myproject:v$VERSION
docker push myregistry.io/myproject:latest

# 5. Create GitHub release
echo "Creating GitHub release..."
gh release create "$VERSION" \
    --title "Release $VERSION" \
    --notes-file <(sed -n "/^## \[$VERSION\]/,/^## \[/p" CHANGELOG.md | head -n -1)

# 6. Verify artifacts
echo "Verifying published artifacts..."
# Check PyPI
python -m pip index versions myproject | grep "$VERSION"
# Check Docker registry
docker pull myregistry.io/myproject:v$VERSION

echo "✅ Release $VERSION published successfully!"
echo "  - PyPI: https://pypi.org/project/myproject/$VERSION/"
echo "  - Docker: myregistry.io/myproject:v$VERSION"
echo "  - GitHub: https://github.com/myorg/myproject/releases/tag/$VERSION"
```

**Requirements**:
- Must verify git tag exists
- Must check CI passed before publishing
- Must publish to PyPI first (faster rollback)
- Must push Docker images with version tag + latest
- Must create GitHub release with CHANGELOG notes
- Must verify all artifacts published successfully

**Testing**:
```bash
# Dry run mode for testing
DRY_RUN=1 ./scripts/publish-prod.sh
```

**Acceptance Criteria**:
- [ ] Detects version from git tag
- [ ] Verifies CI workflow passed for this tag
- [ ] Publishes to PyPI using `twine`
- [ ] Builds and pushes Docker images (version + latest tags)
- [ ] Creates GitHub release with CHANGELOG excerpt
- [ ] Verifies all artifacts accessible after publish
- [ ] Provides clear success confirmation with URLs
- [ ] Supports DRY_RUN mode for testing

---

### Task 3: Update SAP-005 `release.yml` Workflow

**Purpose**: CI validation of Docker builds before allowing release.

**File**: `.github/workflows/release.yml` (or create if doesn't exist)

**YAML Workflow**:
```yaml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  validate-docker-build:
    name: Validate Docker Build
    runs-on: ubuntu-latest
    strategy:
      matrix:
        platform: [amd64, arm64]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up QEMU (for multi-platform builds)
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Extract version from tag
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Build Docker image
        run: |
          docker buildx build \
            --platform linux/${{ matrix.platform }} \
            --tag myproject:v${{ steps.version.outputs.VERSION }} \
            --load \
            .

      - name: Run health check
        run: |
          # Start container
          docker run -d --name test-container \
            -p 8080:8080 \
            myproject:v${{ steps.version.outputs.VERSION }}

          # Wait for container to be healthy
          timeout 30 bash -c 'until docker exec test-container curl -f http://localhost:8080/health; do sleep 2; done'

          # Verify health check response
          HEALTH=$(docker exec test-container curl -s http://localhost:8080/health | jq -r '.status')
          if [ "$HEALTH" != "healthy" ]; then
            echo "Health check failed: $HEALTH"
            exit 1
          fi

      - name: Cleanup
        if: always()
        run: docker rm -f test-container || true

  publish-approval:
    name: Ready for Publishing
    runs-on: ubuntu-latest
    needs: validate-docker-build
    steps:
      - name: Success notification
        run: |
          echo "✅ Docker build validated for all platforms"
          echo "Ready to publish with: ./scripts/publish-prod.sh"
```

**Requirements**:
- Must trigger only on version tags (v*.*.*)
- Must validate Docker builds for all target platforms
- Must run health check tests on container
- Must block if any validation fails
- Should provide clear success/failure feedback

**Acceptance Criteria**:
- [ ] Workflow triggers on git tag push (v*.*.*)
- [ ] Builds Docker image for amd64 and arm64
- [ ] Starts container and waits for healthy status
- [ ] Verifies `/health` endpoint returns `{"status": "healthy"}`
- [ ] Fails workflow if health check fails
- [ ] Cleans up test containers
- [ ] Provides clear success message

---

## Integration Points

### SAP-011 (Docker Operations)

**Required**:
- Dockerfile must have health check
- `docker-compose.yml` must use version tags
- Health endpoint must exist at `/health`

**Example Dockerfile Health Check**:
```dockerfile
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
```

### SAP-012 (Development Lifecycle)

**Required**:
- `pyproject.toml` or `setup.py` must exist
- CHANGELOG.md must follow format with version headers
- Build tools (`build`, `twine`) must be in dev dependencies

**Example pyproject.toml**:
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "myproject"
version = "1.2.3"  # Updated by bump-version.sh

[project.optional-dependencies]
dev = [
    "build>=1.0.0",
    "twine>=4.0.0",
]
```

### SAP-005 (CI/CD Workflows)

**Required**:
- `.github/workflows/` directory must exist
- GitHub Actions must be enabled
- Secrets configured: `PYPI_TOKEN`, Docker registry credentials

---

## Dependencies

### External Tools Required

- **git**: Version tagging and commit automation
- **sed**: Text replacement in version files
- **docker**: Image building and pushing
- **docker-compose**: Multi-container builds
- **python**: PyPI publishing
  - `build` package
  - `twine` package
- **gh**: GitHub CLI for release creation and CI checks
- **jq**: JSON parsing for health checks

### Configuration Required

1. **PyPI Token**:
   - Create token at https://pypi.org/manage/account/token/
   - Add to `~/.pypirc` or `PYPI_TOKEN` env var

2. **Docker Registry**:
   - Configure credentials: `docker login myregistry.io`
   - Update image names in scripts

3. **GitHub CLI**:
   - Install: `brew install gh` or `apt install gh`
   - Authenticate: `gh auth login`

---

## Testing Plan

### Unit Testing

**Test 1: Version Bump Script**
```bash
# Setup
git checkout -b test-version-bump

# Test
./scripts/bump-version.sh 9.9.9

# Verify
grep 'version = "9.9.9"' pyproject.toml
grep ':v9.9.9' docker-compose.yml
grep '## \[9.9.9\]' CHANGELOG.md
git tag | grep v9.9.9

# Cleanup
git tag -d v9.9.9
git reset --hard HEAD~1
git checkout main
git branch -D test-version-bump
```

**Test 2: Publish Script (Dry Run)**
```bash
# Create test tag
git tag -a v9.9.8 -m "Test release"

# Dry run (no actual publishing)
DRY_RUN=1 ./scripts/publish-prod.sh

# Verify it would have published
# Should show: "DRY RUN: Would publish to PyPI"
# Should show: "DRY RUN: Would push Docker image"

# Cleanup
git tag -d v9.9.8
```

### Integration Testing

**Test 3: Full Release Workflow (Test Environment)**
```bash
# 1. Bump version
./scripts/bump-version.sh 0.0.1-test

# 2. Update CHANGELOG with test notes
# (manual edit)

# 3. Push tag
git push origin v0.0.1-test

# 4. Wait for CI (should pass)
gh run watch

# 5. Publish to test registries
TEST_PYPI=1 TEST_DOCKER_REGISTRY=test.registry.io ./scripts/publish-prod.sh

# 6. Verify
# - Check test PyPI: https://test.pypi.org/project/myproject/
# - Pull test Docker image: docker pull test.registry.io/myproject:v0.0.1-test
# - Check GitHub release created

# 7. Cleanup
gh release delete v0.0.1-test
git tag -d v0.0.1-test
git push origin :v0.0.1-test
```

---

## Rollout Plan

### Phase 1: Script Creation (Week 1)
- Create `scripts/bump-version.sh`
- Create `scripts/publish-prod.sh`
- Test locally with dry runs

### Phase 2: CI Integration (Week 1)
- Create `.github/workflows/release.yml`
- Test with test tag
- Verify Docker validation works

### Phase 3: Documentation (Week 1)
- Update SAP-011 capability-charter.md (Docker section)
- Update SAP-012 capability-charter.md (Release section)
- Update SAP-005 awareness-guide.md (CI workflows)
- Create how-to guide: `docs/user-docs/how-to/create-release.md`

### Phase 4: Test Release (Week 2)
- Run full workflow for v0.0.1-test
- Validate all steps work
- Document any issues

### Phase 5: Production Release (Week 2)
- Use for next real release (e.g., v4.4.0)
- Monitor for issues
- Iterate based on feedback

---

## Success Criteria

**Must Have**:
- [ ] Single command bumps versions across PyPI and Docker
- [ ] CI validates Docker builds before allowing release
- [ ] Single command publishes to all registries
- [ ] Version consistency guaranteed (PyPI == Docker tags)
- [ ] CHANGELOG automatically updated with template
- [ ] GitHub release created with notes
- [ ] All artifacts verified after publish

**Nice to Have**:
- [ ] Dry run mode for testing
- [ ] Rollback script for failed releases
- [ ] Multi-platform Docker builds (amd64, arm64)
- [ ] Slack/Discord notification on release
- [ ] Automatic CHANGELOG generation from commits

**Metrics**:
- Time to release: <5 min (down from 20-40 min)
- Failed releases: 0% (Docker validation catches issues)
- Version mismatches: 0% (automated synchronization)
- Developer satisfaction: ≥90%

---

## Risk Mitigation

**Risk 1: PyPI publish succeeds but Docker push fails**
- **Mitigation**: Reverse order - validate Docker first, then publish PyPI
- **Recovery**: Manual Docker push, document in runbook

**Risk 2: CI doesn't catch Docker build issues**
- **Mitigation**: Run health check tests in CI
- **Recovery**: Roll back PyPI release if discovered post-publish

**Risk 3: Version mismatch between files**
- **Mitigation**: Atomic updates in bump-version.sh
- **Recovery**: Script validates all files updated before committing

**Risk 4: Secrets not configured**
- **Mitigation**: Pre-flight checks in publish script
- **Recovery**: Clear error messages pointing to setup docs

---

## Related Documents

- [Workflow Continuity Gap Report](workflow-continuity-gap-report.md) - GAP-003 details
- [MCP Ecosystem SAP Synergies](mcp-ecosystem-sap-synergies.md) - Synergy 5 (Docker Deployment)
- SAP-011 Docker Operations capability-charter.md
- SAP-012 Development Lifecycle protocol-spec.md
- SAP-005 CI/CD Workflows awareness-guide.md

---

## Implementation Checklist

Before starting:
- [ ] Review current release process in your repository
- [ ] Identify Docker registry URL
- [ ] Confirm PyPI project name
- [ ] Install required tools (git, docker, gh, build, twine)
- [ ] Configure credentials (PyPI token, Docker registry)

Implementation:
- [ ] Create `scripts/bump-version.sh`
- [ ] Test version bump script locally
- [ ] Create `scripts/publish-prod.sh`
- [ ] Add DRY_RUN support to publish script
- [ ] Create `.github/workflows/release.yml`
- [ ] Test CI workflow with test tag
- [ ] Update SAP documentation (SAP-005, SAP-011, SAP-012)
- [ ] Create how-to guide for releases
- [ ] Run test release (v0.0.1-test)
- [ ] Document lessons learned
- [ ] Use for production release

Post-implementation:
- [ ] Collect metrics (time saved, errors prevented)
- [ ] Update gap report with "resolved" status
- [ ] Share learnings with team
- [ ] Consider automation improvements (CHANGELOG generation, etc.)

---

**Status**: Ready for Implementation
**Estimated Effort**: 12-16 hours
**Expected ROI**: 20-40 min saved × 12-24 releases/year = 4-16 hours/year
**Break-even**: After 1-2 releases
**Next Step**: Begin Phase 1 (Script Creation)
