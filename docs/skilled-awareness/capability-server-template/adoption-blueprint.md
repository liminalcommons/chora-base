# SAP-047: CapabilityServer-Template - Adoption Blueprint

**SAP ID**: SAP-047
**Name**: CapabilityServer-Template
**Version**: 1.0.0
**Status**: Pilot
**Created**: 2025-11-12
**Last Updated**: 2025-11-12

---

## Purpose

This adoption blueprint provides a step-by-step guide for using SAP-047 (CapabilityServer-Template) to generate production-ready capability servers. It includes clear prerequisites, validation steps, and troubleshooting guidance.

---

## Overview

### What You'll Get

**Generated Project Includes**:
- ✅ Multi-interface support (CLI, REST, optional MCP)
- ✅ Core/interface separation (SAP-042)
- ✅ Manifest registry integration (SAP-044)
- ✅ Bootstrap startup sequence (SAP-045)
- ✅ Composition patterns (SAP-046: Saga, circuit breaker, events)
- ✅ Test suite with ≥80% coverage
- ✅ CI/CD pipelines (GitHub Actions)
- ✅ Documentation (AGENTS.md, API.md, CLI.md)
- ✅ Docker support (multi-stage production image)
- ✅ Pre-commit quality gates

---

### Prerequisites

**Required**:
- [x] Python 3.9+ installed
- [x] Jinja2 installed (`pip install jinja2`)
- [x] Git installed
- [x] Docker installed (for local testing)
- [x] Basic understanding of capability server patterns
- [x] Access to chora-base repository (contains generation script)

**Recommended**:
- [x] Poetry installed (or use `./scripts/dev-setup.sh` to auto-install)
- [x] Docker Compose installed
- [x] kubectl installed (if deploying to Kubernetes)

---

## Adoption Workflow

### Phase 1: Template Generation (5 minutes)

#### 1.1 Install Jinja2 (if needed)

```bash
# Install Jinja2
pip install jinja2

# Verify installation
python -c "import jinja2; print(jinja2.__version__)"
# Expected: 3.0.0 or higher
```

#### 1.2 Generate Project

```bash
# Navigate to chora-base repository
cd /path/to/chora-base

# Generate new capability server
python scripts/create-capability-server.py \
    --name "Analyzer" \
    --namespace chora \
    --description "AI code analysis service" \
    --author "Infrastructure Team" \
    --email "infra@example.com" \
    --python-version 3.11 \
    --enable-mcp \
    --enable-saga \
    --enable-circuit-breaker \
    --license MIT \
    --output ~/projects/analyzer
```

**CLI Arguments Guidance**:

```
--name "Analyzer"
  ← Human-readable capability name (will generate project_slug automatically)

--namespace chora
  ← Python namespace (default: chora)

--description "AI code analysis service"
  ← Short project description (default: "A capability server")

--author "Infrastructure Team"
  ← Author name or team name (default: "Your Name")

--email "infra@example.com"
  ← Contact email (default: "your.email@example.com")

--python-version 3.11
  ← Python version: 3.11, 3.10, or 3.9 (default: 3.11)

--enable-mcp
  ← Include flag to enable MCP server interface (omit to disable)

--enable-saga
  ← Include flag to enable Saga orchestration (omit to disable)

--enable-circuit-breaker
  ← Include flag to enable circuit breakers (omit to disable)

--enable-event-bus
  ← Include flag to enable event bus integration (omit to disable)

--license MIT
  ← License: MIT, Apache-2.0, BSD-3-Clause, or Proprietary (default: MIT)

--output ~/projects/analyzer
  ← Output directory for generated project (required)
```

**Example Session**:

```
project_name: Analyzer
namespace: chora
project_description: AI code analysis service
author_name: Infrastructure Team
python_version: 3.11
enable_mcp: yes
enable_saga: yes
enable_circuit_breaker: yes
enable_event_bus: no
```

**Result**: Project generated in `analyzer/` directory.

---

#### 1.3 Navigate to Project

```bash
cd analyzer

# Verify structure
tree -L 2

# Expected output:
# analyzer/
# ├── src/chora/analyzer/
# ├── tests/
# ├── config/
# ├── docs/
# ├── .github/
# ├── scripts/
# ├── pyproject.toml
# ├── README.md
# ├── Dockerfile
# └── docker-compose.yml
```

**Validation**:
- [ ] Project directory created
- [ ] All expected files present (pyproject.toml, Dockerfile, etc.)
- [ ] src/chora/analyzer/ directory exists

---

### Phase 2: Development Environment Setup (10 minutes)

#### 2.1 Run Dev Setup Script

```bash
# Run automated setup script
./scripts/dev-setup.sh

# This will:
# 1. Check Python version
# 2. Install Poetry (if not installed)
# 3. Create virtual environment
# 4. Install dependencies
# 5. Setup pre-commit hooks
# 6. Initialize git repository (if not already)
```

**Script Output**:

```
✓ Python 3.11 found
✓ Poetry installed
✓ Virtual environment created
✓ Dependencies installed (24 packages)
✓ Pre-commit hooks installed
✓ Git repository initialized
✓ Development environment ready!

Next steps:
  1. Implement core logic in src/chora/analyzer/core/capability.py
  2. Run tests: pytest tests/
  3. Run locally: docker-compose up
```

**Manual Setup** (if script fails):

```bash
# Install Poetry manually
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Setup pre-commit hooks
poetry run pre-commit install
```

**Validation**:
- [ ] Poetry installed (`poetry --version`)
- [ ] Dependencies installed (`poetry show`)
- [ ] Pre-commit hooks installed (`.git/hooks/pre-commit` exists)

---

#### 2.2 Verify Installation

```bash
# Run tests (should pass out-of-box)
poetry run pytest tests/ --cov=src/

# Expected output:
# ========== test session starts ==========
# collected 12 items
#
# tests/test_core/test_capability.py ...     [ 25%]
# tests/test_interfaces/test_cli.py ...      [ 50%]
# tests/test_interfaces/test_rest.py ...     [ 75%]
# tests/test_interfaces/test_mcp.py ...      [100%]
#
# ---------- coverage: 82% -----------
# ========== 12 passed in 2.1s ==========
```

**Validation**:
- [ ] All tests pass
- [ ] Coverage ≥80%
- [ ] No import errors

---

### Phase 3: Implement Core Logic (30-60 minutes)

#### 3.1 Edit Core Capability

**File**: `src/chora/analyzer/core/capability.py`

**Step 1: Define Input/Output Models**

```python
"""Core capability implementation."""
from typing import Dict, Any, List
from pydantic import BaseModel, Field

class AnalyzeInput(BaseModel):
    """Input for code analysis."""
    code: str = Field(..., description="Source code to analyze")
    language: str = Field("python", description="Programming language")
    rules: List[str] = Field(default_factory=list, description="Analysis rules")

class AnalyzeOutput(BaseModel):
    """Output from code analysis."""
    status: str
    result: Dict[str, Any]
```

**Step 2: Implement Execute Method**

```python
class AnalyzerCapability(BaseCapability):
    """AI code analysis capability."""

    async def execute(self, input_data: AnalyzeInput) -> AnalyzeOutput:
        """
        Analyze source code for issues and suggestions.

        Args:
            input_data: Code and analysis configuration

        Returns:
            Analysis result with issues and suggestions
        """
        # 1. Parse code
        ast_tree = await self._parse_code(input_data.code, input_data.language)

        # 2. Run analysis rules
        issues = await self._analyze_ast(ast_tree, input_data.rules)

        # 3. Generate suggestions
        suggestions = await self._generate_suggestions(issues)

        # 4. Return result
        return AnalyzeOutput(
            status="success",
            result={
                "language": input_data.language,
                "issues": issues,
                "suggestions": suggestions,
                "metrics": {
                    "total_lines": len(input_data.code.split("\n")),
                    "issue_count": len(issues)
                }
            }
        )

    async def _parse_code(self, code: str, language: str):
        """Parse source code into AST."""
        # TODO: Implement actual parsing logic
        # Example: use tree-sitter, ast module, etc.
        return {"type": "module", "body": []}

    async def _analyze_ast(self, ast_tree, rules):
        """Analyze AST for issues."""
        # TODO: Implement analysis logic
        return []

    async def _generate_suggestions(self, issues):
        """Generate fix suggestions."""
        # TODO: Implement suggestion generation
        return []

    async def health_check(self) -> Dict[str, str]:
        """Health check."""
        # Check if analysis engine is ready
        return {"status": "healthy"}
```

**Step 3: Update Tests**

**File**: `tests/test_core/test_capability.py`

```python
"""Tests for core capability."""
import pytest
from chora.analyzer.core.capability import AnalyzerCapability, AnalyzeInput

@pytest.fixture
def capability():
    """Create test capability."""
    return AnalyzerCapability(config={})

@pytest.mark.asyncio
async def test_analyze_python_code(capability):
    """Test Python code analysis."""
    input_data = AnalyzeInput(
        code="def foo():\n    pass",
        language="python"
    )

    result = await capability.execute(input_data)

    assert result.status == "success"
    assert "issues" in result.result
    assert "suggestions" in result.result
    assert result.result["metrics"]["total_lines"] == 2

@pytest.mark.asyncio
async def test_analyze_with_issues(capability):
    """Test code with known issues."""
    input_data = AnalyzeInput(
        code="def foo():\n    x = 1  # unused variable",
        language="python",
        rules=["unused_variables"]
    )

    result = await capability.execute(input_data)

    assert result.status == "success"
    # Add assertions for expected issues
```

**Step 4: Run Tests**

```bash
poetry run pytest tests/test_core/ -v

# Expected:
# tests/test_core/test_capability.py::test_analyze_python_code PASSED
# tests/test_core/test_capability.py::test_analyze_with_issues PASSED
```

**Validation**:
- [ ] Core logic implemented
- [ ] Tests updated and passing
- [ ] Type hints added (mypy clean)

---

### Phase 4: Update Configuration (10 minutes)

#### 4.1 Update Service Manifest

**File**: `config/manifest.yaml`

```yaml
service:
  name: "analyzer"
  version: "1.0.0"
  description: "AI code analysis service"

  # Update endpoints with actual ports
  endpoints:
    rest:
      url: "http://analyzer:8080"
      health_check: "/health"

  # Declare dependencies
  dependencies:
    - name: "manifest-registry"
      version: ">=1.0.0"
      required: true

    # Add any additional dependencies
    - name: "storage"
      version: ">=1.0.0"
      required: false  # Optional dependency
```

#### 4.2 Update Runtime Configuration

**File**: `config/config.yaml`

```yaml
service:
  name: "analyzer"
  port: 8080
  log_level: "INFO"

registry:
  manifest_url: "http://manifest:8080"
  heartbeat_interval: 10

# Analyzer-specific settings
analyzer:
  max_file_size_mb: 10
  supported_languages:
    - python
    - javascript
    - typescript
  analysis_timeout: 30  # seconds
```

**Validation**:
- [ ] Manifest updated with correct service name
- [ ] Dependencies declared
- [ ] Runtime configuration customized

---

### Phase 5: Test Locally (15 minutes)

#### 5.1 Run Unit Tests

```bash
# Run all tests with coverage
poetry run pytest tests/ --cov=src/ --cov-report=html

# Open coverage report
open htmlcov/index.html
```

**Expected Results**:
- All tests pass
- Coverage ≥80%
- No import errors

---

#### 5.2 Run Locally with Docker Compose

```bash
# Start services
docker-compose up -d

# Check logs
docker-compose logs -f analyzer

# Expected log output:
# analyzer_1  | INFO:     Started server process
# analyzer_1  | INFO:     Uvicorn running on http://0.0.0.0:8080
# analyzer_1  | INFO:     Registered with manifest: service_analyzer_001
```

#### 5.3 Test REST API

```bash
# Health check
curl http://localhost:8080/health

# Expected: {"status": "healthy"}

# Execute capability
curl -X POST http://localhost:8080/api/v1/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "code": "def foo():\n    pass",
      "language": "python"
    }
  }'

# Expected: {"status": "success", "result": {...}}
```

#### 5.4 Test CLI

```bash
# Using Poetry
poetry run analyzer --help

# Expected: CLI help output

# Execute via CLI
echo '{"code": "def foo(): pass", "language": "python"}' > input.json
poetry run analyzer execute input.json

# Expected: Analysis result printed
```

#### 5.5 Test MCP Server (if enabled)

```bash
# Start MCP server
poetry run python -m chora.analyzer.interfaces.mcp

# In another terminal, test with MCP client
# (Requires MCP client installation)
```

**Validation**:
- [ ] Services start successfully
- [ ] REST API responds to /health
- [ ] Execute endpoint works
- [ ] CLI commands work
- [ ] MCP server starts (if enabled)

---

### Phase 6: CI/CD Integration (10 minutes)

#### 6.1 Push to GitHub

```bash
# Initialize git (if not done by setup script)
git init
git add .
git commit -m "Initial commit: Generated from capability-server-template"

# Add remote
git remote add origin https://github.com/your-org/analyzer.git

# Push
git push -u origin main
```

#### 6.2 Verify CI Pipeline

**GitHub Actions** will automatically run:
1. **Linting**: Black, Ruff, Mypy
2. **Tests**: Pytest with coverage
3. **Build**: Docker image build

**Check Pipeline Status**:
- Navigate to GitHub Actions tab
- Verify "CI" workflow passed
- Check coverage report uploaded to Codecov (if configured)

**Expected Results**:
- ✅ All linting checks pass
- ✅ All tests pass (≥80% coverage)
- ✅ Docker image builds successfully

---

### Phase 7: Deployment (20-30 minutes)

#### 7.1 Build Production Image

```bash
# Build Docker image
docker build -t chora/analyzer:1.0.0 .

# Verify image size (should be <250MB)
docker images chora/analyzer:1.0.0

# Expected:
# REPOSITORY      TAG     SIZE
# chora/analyzer  1.0.0   180MB
```

#### 7.2 Deploy to Staging

**Using Deployment Script**:

```bash
./scripts/deploy.sh staging

# This will:
# 1. Build Docker image
# 2. Tag for registry
# 3. Push to registry
# 4. Deploy to Kubernetes/Docker Swarm
# 5. Verify health checks
```

**Manual Deployment** (Kubernetes):

```bash
# Tag for registry
docker tag chora/analyzer:1.0.0 registry.example.com/chora/analyzer:1.0.0

# Push to registry
docker push registry.example.com/chora/analyzer:1.0.0

# Create Kubernetes deployment (if not exists)
kubectl create deployment analyzer \
  --image=registry.example.com/chora/analyzer:1.0.0 \
  --port=8080

# Expose service
kubectl expose deployment analyzer \
  --type=LoadBalancer \
  --port=80 \
  --target-port=8080

# Verify deployment
kubectl rollout status deployment/analyzer

# Check health
kubectl get pods -l app=analyzer
# Expected: STATUS = Running
```

#### 7.3 Verify Deployment

```bash
# Get service URL
export ANALYZER_URL=$(kubectl get service analyzer -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# Health check
curl http://$ANALYZER_URL/health

# Expected: {"status": "healthy"}

# Test execute
curl -X POST http://$ANALYZER_URL/api/v1/execute \
  -H "Content-Type: application/json" \
  -d '{"input_data": {"code": "...", "language": "python"}}'
```

**Validation**:
- [ ] Docker image built (<250MB)
- [ ] Deployed to staging
- [ ] Health checks pass
- [ ] Execute endpoint works
- [ ] Service registered in manifest

---

## Validation Checklist

### Essential Tier Checklist

**Project Generation**:
- [ ] Template generated successfully in <5 minutes
- [ ] All files present (pyproject.toml, Dockerfile, tests, etc.)
- [ ] No generation errors

**Development Environment**:
- [ ] Dependencies installed via `./scripts/dev-setup.sh`
- [ ] Pre-commit hooks configured
- [ ] All tests pass out-of-box (≥80% coverage)

**Core Implementation**:
- [ ] Core logic implemented in `core/capability.py`
- [ ] Input/output models defined (Pydantic)
- [ ] Tests updated and passing

**Configuration**:
- [ ] `config/manifest.yaml` updated with service info
- [ ] Dependencies declared correctly
- [ ] Runtime configuration customized

**Local Testing**:
- [ ] REST API responds to /health
- [ ] Execute endpoint works
- [ ] CLI commands work
- [ ] Docker Compose runs successfully

**CI/CD**:
- [ ] GitHub Actions pipeline passes
- [ ] Linting checks pass (Black, Ruff, Mypy)
- [ ] Tests pass in CI (≥80% coverage)
- [ ] Docker image builds in CI

**Deployment**:
- [ ] Docker image built (<250MB)
- [ ] Deployed to staging environment
- [ ] Health checks pass in staging
- [ ] Service registered in manifest

---

### Recommended Tier Checklist

(Essential Tier +)

**Saga Orchestration** (if `enable_saga=yes`):
- [ ] Saga defined in `config/sagas.yaml`
- [ ] Saga steps implemented in `composition/saga.py`
- [ ] Compensation logic implemented (idempotent)
- [ ] Saga tested (success and failure scenarios)

**Circuit Breakers** (if `enable_circuit_breaker=yes`):
- [ ] Circuit breakers configured in `config/circuit_breakers.yaml`
- [ ] External service calls wrapped in circuit breakers
- [ ] Fallback behavior implemented
- [ ] Circuit breaker tested (open/close transitions)

**Event Bus** (if `enable_event_bus=yes`):
- [ ] Event bus configured (Redis/NATS)
- [ ] Event publishers implemented
- [ ] Event subscribers implemented
- [ ] Events tested (pub/sub working)

**Monitoring**:
- [ ] Prometheus metrics endpoint (`/metrics`) working
- [ ] Metrics exported (request count, duration, errors)
- [ ] Grafana dashboard imported (optional)

**Documentation**:
- [ ] `docs/AGENTS.md` updated with actual commands
- [ ] `docs/API.md` generated (OpenAPI spec)
- [ ] `docs/CLI.md` updated with CLI reference
- [ ] README updated with project-specific info

---

### Advanced Tier Checklist

(Recommended Tier +)

**High Availability**:
- [ ] Multi-replica deployment (≥3 replicas)
- [ ] Health checks configured (liveness + readiness)
- [ ] Graceful shutdown implemented

**Security**:
- [ ] Authentication middleware added (if needed)
- [ ] Input validation (Pydantic models)
- [ ] Rate limiting configured
- [ ] Secrets managed via secrets manager (not env vars)

**Performance**:
- [ ] Caching implemented (for expensive operations)
- [ ] Connection pooling configured (database, Redis, etc.)
- [ ] Request timeout configured
- [ ] Load tested (≥1000 req/sec)

**Observability**:
- [ ] Distributed tracing (OpenTelemetry) configured
- [ ] Structured logging (JSON format)
- [ ] Log aggregation (ELK, Datadog, etc.)
- [ ] Grafana dashboard deployed

---

## Troubleshooting

### Issue 1: Template Generation Fails

**Symptom**: `python scripts/create-capability-server.py` fails with error.

**Diagnosis**:
```bash
# Check Jinja2 installed
python -c "import jinja2; print(jinja2.__version__)"
# Should be ≥3.0.0

# Check script exists
ls scripts/create-capability-server.py

# Check you're in chora-base directory
pwd
# Should be: /path/to/chora-base
```

**Fix**:
```bash
# Install Jinja2
pip install jinja2

# Or if in chora-base development environment:
poetry install

# Ensure you're in chora-base root:
cd /path/to/chora-base
```

---

### Issue 2: Dependencies Install Fails

**Symptom**: `poetry install` fails with dependency conflict.

**Diagnosis**:
```bash
# Check Poetry version
poetry --version

# Should be ≥1.7.0
```

**Fix**:
```bash
# Update Poetry
curl -sSL https://install.python-poetry.org | python3 - --uninstall
curl -sSL https://install.python-poetry.org | python3 -

# Clear cache and reinstall
poetry cache clear . --all
poetry install
```

---

### Issue 3: Tests Fail After Generation

**Symptom**: `pytest tests/` fails with import errors.

**Diagnosis**:
```bash
# Check if module installed in editable mode
pip list | grep analyzer
```

**Fix**:
```bash
# Install in editable mode
poetry install

# Or activate virtual environment
poetry shell
pytest tests/
```

---

### Issue 4: Docker Build Fails

**Symptom**: `docker build` fails with "No such file" error.

**Diagnosis**:
```bash
# Check if all files exist
ls src/chora/analyzer/core/capability.py
ls pyproject.toml
```

**Fix**:
```bash
# Ensure you're in project root
pwd
# Should show: .../analyzer

# Rebuild with verbose output
docker build --progress=plain -t analyzer:latest .
```

---

### Issue 5: Service Won't Start

**Symptom**: `docker-compose up` fails, service exits immediately.

**Diagnosis**:
```bash
# Check logs
docker-compose logs analyzer

# Common errors:
# - ImportError: Module not found
# - ConnectionError: Cannot connect to manifest
# - PermissionError: Cannot write to /app/logs
```

**Fix (ImportError)**:
```bash
# Rebuild Docker image
docker-compose build analyzer
docker-compose up
```

**Fix (ConnectionError)**:
```bash
# Check if manifest service is running
docker-compose ps manifest

# If not running, start it
docker-compose up -d manifest

# Wait 10 seconds, then start analyzer
sleep 10
docker-compose up analyzer
```

**Fix (PermissionError)**:
```bash
# Update Dockerfile to create logs directory
# Already fixed in template, rebuild:
docker-compose build --no-cache analyzer
```

---

## FAQ

### Q1: Can I customize the generated project structure?

**A**: Yes, but stick to conventions for maintainability:
- ✅ Add new modules under `src/chora/analyzer/`
- ✅ Add new tests under `tests/`
- ✅ Add new configs under `config/`
- ❌ Don't rename core modules (`core/`, `interfaces/`, etc.)
- ❌ Don't move files outside conventions

---

### Q2: Should I enable all features (Saga, circuit breaker, event bus)?

**A**: Depends on your needs:
- **Saga**: Only if you have multi-step workflows requiring rollback
- **Circuit breaker**: Yes if calling external services
- **Event bus**: Only if you need pub/sub messaging
- **MCP**: Yes if AI agent integration needed

You can always add features later manually.

---

### Q3: How do I add authentication to the generated project?

**A**: Add middleware to REST API:
1. Create `src/chora/analyzer/middleware/auth.py`
2. Implement auth logic (JWT, OAuth, etc.)
3. Add middleware to `interfaces/rest.py`: `app.add_middleware(AuthMiddleware)`
4. Update tests to mock authentication

---

### Q4: Can I use the template for non-Python projects?

**A**: No, the template is Python-specific. For other languages:
- Create language-specific template following same patterns
- Or manually implement patterns from SAP-042 through SAP-046

---

### Q5: How do I update a project generated from an older template version?

**A**: Two options:
1. **Manual update**: Cherry-pick changes from new template
2. **Regenerate**: Use `--overwrite-if-exists`, then merge changes

Recommended: Manual update for production projects.

---

## Next Steps

After completing adoption:

1. **Customize Implementation**: Add business logic specific to your capability
2. **Write More Tests**: Aim for ≥90% coverage for production
3. **Add Monitoring**: Configure Prometheus + Grafana dashboards
4. **Deploy to Production**: Follow deployment checklist above
5. **Update Documentation**: Keep AGENTS.md, API.md in sync with code
6. **Collect Feedback**: Share experience with template maintainers

---

**Document Version**: 1.0.0
**Status**: Pilot
**Last Updated**: 2025-11-12
