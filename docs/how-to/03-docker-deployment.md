# How-To: Docker Deployment for chora-base Projects

**Audience**: Developers deploying chora-base projects to production or using Docker for CI
**Prerequisites**: Docker installed, project generated from chora-base v1.9.0+
**Time**: 15-30 minutes

---

## Quick Start

**Enable Docker during project generation:**

```bash
copier copy gh:liminalcommons/chora-base my-project
# When prompted:
# include_docker: true
# docker_strategy: production  # or ci-only
```

**Or add to existing project:**

```bash
# Add Docker files manually (see "Adding Docker to Existing Projects" below)
```

---

## Table of Contents

1. [When to Use Docker](#when-to-use-docker)
2. [Docker Strategies](#docker-strategies)
3. [Quick Reference](#quick-reference)
4. [CI Testing with Docker](#ci-testing-with-docker)
5. [Production Deployment](#production-deployment)
6. [docker-compose Orchestration](#docker-compose-orchestration)
7. [Adding Docker to Existing Projects](#adding-docker-to-existing-projects)
8. [Troubleshooting](#troubleshooting)

---

## When to Use Docker

### ✅ Use Docker When:

- **CI Isolation**: Prevent system vs pip package conflicts (GitHub Actions)
- **Production Deployment**: Deploy MCP servers or web services to servers
- **Microservices**: Orchestrate multiple services (n8n + MCP gateway + backends)
- **Team Consistency**: "Works on my machine" → "Works in this container"
- **Security**: Non-root user, minimal attack surface

### ❓ Consider Alternatives When:

- **Local Development Only**: venv is faster for iteration
- **Library Projects**: Docker less relevant (consumed by other projects)
- **Learning Python**: venv simpler for beginners

**Recommendation**: Use hybrid approach (venv for dev, Docker for CI/prod)

---

## Docker Strategies

### Production Strategy (`docker_strategy: production`)

**Includes:**
- `Dockerfile` - Multi-stage production build
- `Dockerfile.test` - CI/test build
- `.dockerignore` - Build optimization
- `docker-compose.yml` - Orchestration

**Use Cases:**
- Production deployment (servers, cloud)
- Microservices architecture
- Full CI/CD pipeline

### CI-Only Strategy (`docker_strategy: ci-only`)

**Includes:**
- `Dockerfile.test` - CI/test build only
- `.dockerignore` - Build optimization

**Use Cases:**
- GitHub Actions CI testing only
- No production deployment planned
- Minimal Docker footprint

---

## Quick Reference

### Build Commands

```bash
# Build production image
just docker-build
# or: docker build -t my-project:latest .

# Build test image
just docker-build-test
# or: docker build -t my-project:test -f Dockerfile.test .
```

### Run Commands

```bash
# Run tests in Docker (isolated environment)
just docker-test

# Start production container
just docker-run

# Start all services (docker-compose)
just docker-compose-up
```

### Management Commands

```bash
# View logs
just docker-logs

# Stop services
just docker-compose-down

# Rebuild and restart
just docker-rebuild

# Full cleanup
just docker-clean-all
```

---

## CI Testing with Docker

### Problem: GitHub Actions Package Conflicts

**Symptom:**
```
GitHub Actions installs system package (v1.1.0)
pyproject.toml requires pip package (v1.5.0)
Tests fail: ImportError or wrong version loaded
```

**Solution:** Run tests in isolated Docker container

### Step 1: Enable Docker in Project

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build test Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile.test
          push: false
          load: true
          tags: my-project:test
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Run tests in Docker
        run: docker run --rm my-project:test
```

### Step 2: Verify Isolation

```bash
# Local verification
just docker-build-test
just docker-test

# Should see:
# ✓ All dependencies from pyproject.toml (not system)
# ✓ Tests pass in isolated environment
# ✓ Coverage meets threshold
```

### Benefits

✅ **Guaranteed Isolation**: No system package conflicts
✅ **Faster CI**: Docker layer caching (GitHub Actions)
✅ **Reproducible**: Same environment every time
✅ **Debuggable**: `docker run -it my-project:test bash` for debugging

---

## Production Deployment

### MCP Server Deployment

#### Option A: Single Container

```bash
# Build production image
docker build -t my-mcp-server:1.0.0 .

# Run with environment and volumes
docker run -d \
  --name my-mcp-server \
  --restart unless-stopped \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/.env:/app/.env:ro \
  -v $(pwd)/.chora/memory/events:/app/.chora/memory/events \
  my-mcp-server:1.0.0

# Check health
docker ps
docker logs my-mcp-server
```

#### Option B: docker-compose (Recommended)

```bash
# Start services
docker-compose up -d

# View status
docker-compose ps

# View logs
docker-compose logs -f my-mcp-server

# Stop services
docker-compose down
```

### Web Service Deployment

```bash
# Build image
docker build -t my-web-service:1.0.0 .

# Run with port mapping
docker run -d \
  --name my-web-service \
  --restart unless-stopped \
  -p 8000:8000 \
  -v $(pwd)/.env:/app/.env:ro \
  my-web-service:1.0.0

# Verify health
curl http://localhost:8000/health
```

### Environment Variables

**Create `.env` file:**

```bash
# Application settings
MY_PROJECT_LOG_LEVEL=INFO
MY_PROJECT_LOG_FILE=/app/logs/my-project.log

# API keys (for MCP servers)
ANTHROPIC_API_KEY=sk-ant-...
CODA_API_KEY=...

# Database (if applicable)
DATABASE_URL=postgresql://...
```

**Mount as read-only:**

```bash
-v $(pwd)/.env:/app/.env:ro  # :ro = read-only
```

### Security Best Practices

1. **Non-root user**: Templates use `appuser` (not root)
2. **Read-only volumes**: Mount secrets as `:ro`
3. **Minimal base image**: `python:3.12-slim` (~40MB)
4. **Health checks**: Built-in monitoring
5. **No secrets in image**: Use environment variables

---

## docker-compose Orchestration

### Microservices Architecture

**Example: MCP Gateway + Backend Services**

```yaml
# docker-compose.yml (generated template)
version: "3.8"

services:
  mcp-gateway:
    build: ./mcp-gateway
    ports:
      - "5000:5000"
    environment:
      - BACKEND_URL=http://chora-compose:8000
    networks:
      - mcp-network
    depends_on:
      - chora-compose

  chora-compose:
    build: ./chora-compose
    env_file: .env
    volumes:
      - ./logs:/app/logs
    networks:
      - mcp-network

  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    volumes:
      - ./n8n_data:/home/node/.n8n
    networks:
      - mcp-network

networks:
  mcp-network:
    driver: bridge
```

### Common Commands

```bash
# Start all services
docker-compose up -d

# Scale a service
docker-compose up -d --scale chora-compose=3

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f chora-compose

# Restart a service
docker-compose restart chora-compose

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Networking

**Services communicate via service names:**

```python
# In mcp-gateway code
import requests

# Call chora-compose service by name
response = requests.get("http://chora-compose:8000/tools")
```

**Docker network resolution:**
- Service name → Container IP (automatic)
- `http://chora-compose:8000` → Container's port 8000
- No need to know container IP

---

## Adding Docker to Existing Projects

### Option 1: copier Update (Recommended)

```bash
# Update from chora-base v1.9.0+
copier update

# Answer prompts:
# include_docker: true
# docker_strategy: production  # or ci-only

# Review changes
git diff

# Commit
git add Dockerfile* docker-compose.yml .dockerignore
git commit -m "feat(docker): Add Docker support from chora-base v1.9.0"
```

### Option 2: Manual Addition

**Step 1: Copy template files**

```bash
# Clone chora-base locally
git clone https://github.com/liminalcommons/chora-base

# Copy Docker templates
cp chora-base/template/Dockerfile.jinja myproject/Dockerfile
cp chora-base/template/Dockerfile.test.jinja myproject/Dockerfile.test
cp chora-base/template/.dockerignore.jinja myproject/.dockerignore
cp chora-base/template/docker-compose.yml.jinja myproject/docker-compose.yml
```

**Step 2: Replace template variables**

```bash
# Find and replace in copied files:
{{ project_name }} → My Project Name
{{ project_slug }} → my-project
{{ package_name }} → my_project
{{ python_version }} → 3.12
```

**Step 3: Update justfile (optional)**

Add Docker commands from `template/justfile.jinja` to your `justfile`.

**Step 4: Test**

```bash
# Build test image
docker build -t my-project:test -f Dockerfile.test .

# Run tests
docker run --rm my-project:test

# Build production image
docker build -t my-project:latest .
```

---

## Troubleshooting

### Issue: Docker build fails with "ModuleNotFoundError"

**Symptom:**
```
ERROR: Could not find a version that satisfies the requirement my-package
```

**Cause:** pyproject.toml not copied correctly in Dockerfile.

**Solution:**
```dockerfile
# Dockerfile line order matters!
COPY pyproject.toml README.md ./  # ← Must be BEFORE pip install
COPY src/ ./src/
RUN pip install -e .
```

### Issue: Container exits immediately

**Symptom:**
```bash
$ docker ps
# Container not running
```

**Cause:** No long-running process.

**Solution:**

```bash
# MCP servers should have CMD
CMD ["my-mcp-server"]

# Web services should have CMD
CMD ["uvicorn", "my_project.main:app", "--host", "0.0.0.0"]

# Check logs for error
docker logs my-project
```

### Issue: Tests pass locally but fail in Docker

**Symptom:** `pytest` works in venv but fails in container.

**Possible Causes:**

1. **Missing test dependencies**:
   ```bash
   # Ensure [dev] dependencies installed
   RUN pip install -e ".[dev]"  # ← Note the quotes!
   ```

2. **File not copied**:
   ```dockerfile
   COPY tests/ ./tests/  # ← Must copy test files
   ```

3. **Environment variable missing**:
   ```bash
   docker run --rm -e ANTHROPIC_API_KEY=test my-project:test
   ```

### Issue: docker-compose volumes not persisting

**Symptom:** Data lost when container restarts.

**Solution:**

```yaml
# docker-compose.yml
services:
  my-service:
    volumes:
      # Named volume (persists across restarts)
      - my-data:/app/data

volumes:
  my-data:
    driver: local
```

### Issue: Cannot connect to service from another container

**Symptom:** `Connection refused` when calling service.

**Solution:**

```yaml
# Ensure services on same network
services:
  service-a:
    networks:
      - my-network

  service-b:
    networks:
      - my-network

networks:
  my-network:
    driver: bridge
```

```python
# Use service name (not localhost)
url = "http://service-a:8000"  # ✅ Correct
url = "http://localhost:8000"   # ❌ Wrong (localhost = own container)
```

---

## Advanced Topics

### Multi-Platform Builds

```bash
# Build for multiple architectures
docker buildx build --platform linux/amd64,linux/arm64 \
  -t my-project:latest .
```

### Image Publishing

```bash
# Tag for registry
docker tag my-project:latest ghcr.io/username/my-project:latest

# Push to GitHub Container Registry
docker push ghcr.io/username/my-project:latest
```

### Security Scanning

```bash
# Install Trivy
brew install trivy

# Scan image for vulnerabilities
trivy image my-project:latest
```

---

## References

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [chora-base v1.9.0 CHANGELOG](../../CHANGELOG.md#190---2025-10-21)
- [mcp-n8n Docker Implementation](https://github.com/liminalcommons/mcp-n8n)

---

**Questions?** Open an issue: https://github.com/liminalcommons/chora-base/issues
