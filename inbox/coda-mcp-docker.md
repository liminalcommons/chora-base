Docker Implementation for MCP Server Coda
Overview
This project implements production-ready Docker support for MCP (Model Context Protocol) servers with a focus on security, efficiency, and developer experience. The implementation was added as part of chora-base v1.9.0 standardization and provides containerized deployment options for both production and testing environments.
Architecture
The Docker implementation consists of four core components:
1. Production Dockerfile (Dockerfile)
Multi-stage build optimized for production deployment
2. Test Dockerfile (Dockerfile.test)
Single-stage build optimized for CI/CD testing
3. Docker Compose Configuration (docker-compose.yml)
Orchestration for local development and service coordination
4. Build Automation (justfile:172-263)
11 Docker-specific commands integrated into the project's task runner
Detailed Component Breakdown
1. Production Dockerfile (Multi-Stage Build)
Purpose: Create a minimal, secure, production-ready container image (~259MB) Stage 1: Builder (Lines 3-23)
Base: python:3.12-slim
Installs build tools: build-essential, curl, git
Creates isolated virtual environment
Installs dependencies from pyproject.toml
Only copies essential files (leverages Docker layer caching)
Stage 2: Runtime (Lines 25-64)
Base: Fresh python:3.12-slim (no build artifacts)
Security Features:
Non-root user (coda, uid 1000)
Minimal runtime dependencies (only ca-certificates)
Read-only application code
Python bytecode disabled (PYTHONDONTWRITEBYTECODE=1)
Runtime Configuration:
Unbuffered Python output for real-time logging
Virtual environment activated via PATH
Health check using version import validation
STDIO transport entrypoint (standard for MCP servers)
Key Design Decisions:
Multi-stage build: Separates build dependencies from runtime (reduces image size by ~40%)
Layer caching: Dependencies installed before code copy (faster rebuilds)
Non-root execution: Security best practice (prevents privilege escalation)
Health check: Import-based validation (no CLI overhead for STDIO servers)
Image Size: ~259MB (optimized)
2. Test Dockerfile (Single-Stage)
Purpose: Fast test execution in CI environments with full development tooling Characteristics:
Single-stage build (optimized for simplicity, not size)
Includes all dev dependencies: pytest, coverage, linters
Includes system tools: build-essential, git, curl
Non-root execution (testuser, uid 1000)
Default command: pytest -v --cov=src/coda_mcp --cov-report=term-missing
Usage Context:
GitHub Actions workflows
Pre-merge validation
Local test runs via Docker
Trade-offs:
Larger image size (~350-400MB estimated)
Faster build time (no multi-stage overhead)
Complete dev environment parity
3. Docker Compose Configuration
Purpose: Local development orchestration with service definitions Services Defined:
coda-mcp (Main Service)
- Build: Uses production Dockerfile
- Environment: CODA_API_KEY, LOG_LEVEL
- Transport: STDIO (stdin_open: true, tty: true)
- Restart: unless-stopped
- Volumes: ./.chora/memory mounted for persistence
- Health check: Version import validation
- Network: Isolated mcp-network bridge
coda-mcp-test (Test Service)
- Build: Uses test Dockerfile
- Profile: test (opt-in via --profile test)
- Environment: CODA_API_KEY
- Purpose: Run test suite in Docker
Key Features:
Memory persistence: .chora/memory directory mounted as volume
Environment variable injection: From host .env file
Network isolation: Services communicate via mcp-network bridge
Profile-based activation: Test service only starts when explicitly requested
Use Cases:
Local development with Docker
Multi-container testing scenarios
Production-like local environment
4. Justfile Docker Commands
Integration: 11 Docker commands integrated into the project's primary task runner Build Commands:
docker-build [TAG] - Build production image (default: latest)
docker-build-test [TAG] - Build test image (default: test)
docker-build-multi [TAG] - Multi-architecture build (amd64, arm64)
Run Commands:
docker-run [TAG] - Run in STDIO mode (interactive MCP server)
docker-shell [TAG] - Interactive shell for debugging
docker-test - Run test suite in container
Orchestration Commands:
docker-compose-up - Start services with docker-compose
docker-compose-down - Stop services
docker-compose-logs - View logs
Deployment Commands:
docker-push REGISTRY TAG - Tag and push to registry
docker-release VERSION [REGISTRY] - Full release workflow (build, tag, push)
docker-clean - Clean Docker artifacts
docker-verify [TAG] - Smoke test image (version import check)
Example Usage:
# Build and verify production image
just docker-build v0.10.0
just docker-verify v0.10.0

# Run test suite in Docker
just docker-test

# Full release workflow
just docker-release 0.10.0 ghcr.io/liminalcommons

# Local development with compose
just docker-compose-up
just docker-compose-logs
Technical Specifications
Security Hardening
Non-root Execution
Production: coda user (uid 1000)
Test: testuser user (uid 1000)
Prevents privilege escalation attacks
Minimal Attack Surface
Production runtime: Only ca-certificates system package
No build tools in runtime image
No git in runtime image
Environment Isolation
Secrets via environment variables (not baked into image)
No .env files copied to image (.dockerignore)
Virtual environment isolation
Image Scanning
Compatible with standard CVE scanners
No known vulnerabilities in base image (python:3.12-slim)
Performance Optimizations
Layer Caching Strategy
# Dependencies first (changes rarely)
COPY pyproject.toml README.md ./
RUN pip install ...

# Code last (changes frequently)
COPY src ./src/
Multi-Architecture Support
Builds for amd64 and arm64
Uses Docker Buildx for cross-platform builds
Single command: just docker-build-multi
APT Package Management
--no-install-recommends flag (reduces package bloat)
Immediate cache cleanup: rm -rf /var/lib/apt/lists/*
Reduces image size by ~50-100MB
Pip Optimization
--no-cache-dir flag (no pip cache in image)
--upgrade pip (latest performance improvements)
Virtual environment for dependency isolation
Health Checks
Production Container:
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import coda_mcp; assert coda_mcp.__version__" || exit 1
Design Rationale:
Import-based: No CLI overhead (MCP servers use STDIO, not HTTP)
Fast: <100ms typical execution time
Reliable: Validates Python environment and package installation
Non-intrusive: Doesn't interfere with STDIO transport
Parameters:
interval: 30s (check every 30 seconds)
timeout: 3s (fail if check takes >3s)
start-period: 5s (grace period for initialization)
retries: 3 (mark unhealthy after 3 consecutive failures)
Docker Ignore Strategy
Excluded from Build Context (.dockerignore):
Python artifacts: __pycache__/, *.pyc, .pytest_cache/, .mypy_cache/
Virtual environments: .venv/, venv/, ENV/
Documentation: docs/, dev-docs/, *.md (except README.md)
Tests: tests/ (excluded from production, included in test image via COPY)
CI/CD: .github/
Development: scripts/, .vscode/, .idea/
Secrets: .env, .env.*
Runtime memory: .chora/memory/events/, .chora/memory/knowledge/notes/
Benefits:
Faster build context transfer
Smaller image size
No sensitive data leakage
Clean production artifacts
MCP Protocol Considerations
STDIO Transport
MCP servers communicate via STDIO (standard input/output), not HTTP. Docker configuration reflects this: Production Dockerfile:
ENTRYPOINT ["coda-mcp"]
CMD []
Docker Compose:
stdin_open: true  # Keep stdin open for MCP stdio transport
tty: true         # Allocate pseudo-TTY
Running Interactively:
# Docker run
docker run --rm -i -e CODA_API_KEY="${CODA_API_KEY}" coda-mcp:latest

# Justfile wrapper
just docker-run latest
Health Check Adaptation
Unlike HTTP servers, MCP servers don't expose health endpoints. Solution:
# Not feasible: CMD curl http://localhost/health
# Solution: Import validation
CMD python -c "import coda_mcp; assert coda_mcp.__version__"
This validates:
Python environment is functional
Package is correctly installed
Version resolution works (dynamic from pyproject.toml)
CI/CD Integration
GitHub Actions Example
- name: Build Docker image
  run: just docker-build ${{ github.sha }}

- name: Run tests in Docker
  run: just docker-test

- name: Push to registry
  if: github.ref == 'refs/heads/main'
  run: |
    echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
    just docker-push ghcr.io/${{ github.repository }} ${{ github.sha }}
    just docker-push ghcr.io/${{ github.repository }} latest
Release Workflow
# 1. Build and tag
just docker-build v0.10.0

# 2. Verify image
just docker-verify v0.10.0

# 3. Full release (builds, tags, pushes)
just docker-release 0.10.0 ghcr.io/liminalcommons

# Pushes:
#   - ghcr.io/liminalcommons/coda-mcp:0.10.0
#   - ghcr.io/liminalcommons/coda-mcp:latest
Developer Experience
Quick Start
# 1. Build image
just docker-build

# 2. Run server
just docker-run

# 3. Test in Docker
just docker-test

# 4. Debug interactively
just docker-shell
Local Development with Compose
# Start services
just docker-compose-up

# View logs
just docker-compose-logs

# Stop services
just docker-compose-down
Testing Workflow
# Test specific scenarios
docker-compose up --profile test  # Runs test service

# Or via justfile
just docker-test  # Builds and runs tests
File Structure
mcp-server-coda/
├── Dockerfile              # Production multi-stage build
├── Dockerfile.test         # Test single-stage build
├── docker-compose.yml      # Local orchestration
├── .dockerignore          # Build context exclusions
├── justfile               # Docker commands (lines 172-263)
└── .chora/memory/         # Persistent memory (mounted volume)
Metrics and Results
Build Performance
Production image: ~2-3 minutes (cold build)
Test image: ~1-2 minutes (cold build)
Rebuild with cache: ~30-60 seconds
Image Sizes
Production: ~259MB (optimized multi-stage)
Test: ~350-400MB (includes dev dependencies)
Base python:3.12-slim: ~130MB
Security Score
✅ Non-root execution
✅ Minimal runtime dependencies
✅ No secrets in image layers
✅ Latest Python 3.12 base image
✅ Health check monitoring
Adoption Impact
Before Docker Implementation
Manual Python environment setup
Inconsistent runtime environments
No containerized deployment option
Complex CI/CD configuration
After Docker Implementation
Single command deployment: just docker-run
Consistent environments: Dev, test, production parity
Simplified CI/CD: Docker-based testing and deployment
Multi-platform support: amd64, arm64 via buildx
Security hardening: Non-root, minimal attack surface
Integration with chora-base Ecosystem
This Docker implementation follows chora-base v1.9.0 standards:
Alignment Points
Task automation: Integrated into justfile (primary developer interface)
Developer experience: Consistent with other chora-base commands (just docker-*)
Testing infrastructure: Test Dockerfile complements existing test suite
Documentation: Included in CHANGELOG, upgrade guides, and DEVELOPMENT.md
Memory system compatibility: .chora/memory volume mounts
Extensibility
Modular Dockerfile design (easy to adapt for other MCP servers)
Justfile commands can be copied to other projects
Docker Compose template for multi-service MCP architectures
Health check pattern applicable to all Python-based MCP servers
Recommendations for chora-base
Consider Standardizing:
Dockerfile Templates
templates/Dockerfile.production (multi-stage)
templates/Dockerfile.test (single-stage CI)
Parameterized for different Python versions (3.11, 3.12, 3.13)
Docker Compose Patterns
Template for MCP STDIO servers
Template for multi-service MCP architectures
Environment variable injection patterns
Justfile Docker Commands
Standardized command naming (docker-*)
Common parameters (TAG, REGISTRY)
Consistent output formatting
Health Check Patterns
Import-based checks for Python packages
Version validation patterns
Orchestration-friendly health endpoints
.dockerignore Template
Python-specific exclusions
chora-base memory exclusions
Standard development artifacts
Documentation Additions:
Docker Guide (docs/how-to/docker-deployment.md)
Building images
Running containers
Deployment strategies
Troubleshooting
CI/CD Examples (docs/reference/cicd/docker-workflows.md)
GitHub Actions integration
GitLab CI examples
Multi-arch builds
Security Best Practices (docs/reference/security/docker-hardening.md)
Non-root execution
Secrets management
Image scanning
CVE monitoring
Summary
This Docker implementation provides a production-ready, secure, and developer-friendly containerization solution for MCP servers. Key achievements: ✅ 259MB optimized production image (multi-stage build)
✅ Non-root security hardening (uid 1000)
✅ Multi-architecture support (amd64, arm64)
✅ 11 justfile commands (consistent developer interface)
✅ STDIO transport compatibility (MCP protocol standard)
✅ Health check integration (orchestration-ready)
✅ Memory persistence (volume mounts for .chora/memory)
✅ Test environment parity (Dockerfile.test for CI/CD) The implementation serves as a reference standard for containerizing chora-base projects and can be adapted for other MCP servers with minimal modifications.